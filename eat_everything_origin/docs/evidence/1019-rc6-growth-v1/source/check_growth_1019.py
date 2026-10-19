"""Prepare growth collection commands or check original native observations offline."""
import argparse
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile

import audit_save as a
import runtime_growth_1019 as collector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "testing"))
import inspect_1019 as native

KINDS = ("shield", "armor", "hull", "damage", "tracking", "regen")
TIERS = tuple("eep_component_" + kind + "_level" for kind in KINDS)
HEALTH = ("hitpoints", "max_hitpoints", "armor_hitpoints", "max_armor_hitpoints",
          "shield_hitpoints", "max_shield_hitpoints")
CORE_SLOTS = {"AUX_UTILITY_" + str(i): "EEP_ADAPTIVE_" + kind.upper() + "_CORE"
              for i, kind in enumerate(KINDS, 6)}
TOLERANCE = .01
HP_ULPS = 8
HP_TOLERANCE_CONTRACT = "max_0p01_or_8_binary32_ulp_expected_v1"
MODEL_HASHES = (
    "bd3b4d48eeb5de98b34a8ba104f55c23f17cb43a723a216934f2c2a1c4a2099f",
    "a191eea40464ef3fde5f7ec64f33ac2d7012ef74d6b6cdea900d441a16371bc8",
    "942b98c2aea0022ff7ffa017944abbf873d36331fd26c89862f83a37e31e4dd2",
    "6eb5ef0ef58fb353edd6e3f31b932ddc4bbf6b8b42b3bb6eaf2881fe51bd4c7f")
SOURCE_TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
SOURCE_REVISIONS = {
    "1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52": (3, "frozen_rc5"),
    SOURCE_TREE: (4, "frozen_rc6")}
HISTORICAL_RC4_TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
HISTORICAL_RC4_SOURCE_COPY_SHA = "4d948c9782197108c2703b89a4e65d3fc1e4636a322a9497a5ba88ca408b6a2d"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def check(rows, name, actual, expected):
    rows.append({"check": name, "passed": actual == expected, "actual": actual, "expected": expected})


def binary32_ulp(expected):
    """Engineering reference spacing, not a claim about the engine's storage type."""
    if type(expected) not in (int, float) or not math.isfinite(expected):
        return None
    try:
        bits = struct.unpack(">I", struct.pack(">f", abs(expected)))[0]
    except (OverflowError, struct.error):
        return None
    exponent = (bits >> 23) & 255
    if exponent == 255:
        return None
    return math.ldexp(1.0, exponent - 127 - 23) if exponent else math.ldexp(1.0, -149)


def numeric_comparison(rows, name, actual, expected, hp=False):
    finite = (type(actual) in (int, float) and type(expected) in (int, float)
              and math.isfinite(actual) and math.isfinite(expected))
    ulp = binary32_ulp(expected)
    tolerance = max(TOLERANCE, HP_ULPS * ulp) if hp and ulp is not None else TOLERANCE if not hp else None
    delta = actual - expected if finite else None
    if delta is not None and not math.isfinite(delta):
        delta = None
    ulp_error = abs(delta) / ulp if delta is not None and ulp else None
    if ulp_error is not None and not math.isfinite(ulp_error):
        ulp_error = None

    def recorded(value):
        return repr(value) if isinstance(value, float) and not math.isfinite(value) else value

    rows.append({"check": name, "passed": delta is not None and tolerance is not None and abs(delta) <= tolerance,
                 "actual": recorded(actual), "observed": recorded(actual), "expected": recorded(expected),
                 "raw_delta": delta, "applied_tolerance": tolerance,
                 "ulp32_expected": ulp, "ulp_error": ulp_error,
                 "tolerance_kind": "hp_binary32_ulp_engineering" if hp else "fixed_absolute",
                 "absolute_tolerance": tolerance, "relative_tolerance": 0})


def close(rows, name, actual, expected):
    numeric_comparison(rows, name, actual, expected)


def close_hp(rows, name, actual, expected):
    numeric_comparison(rows, name, actual, expected, hp=True)


def scope(rows):
    return {"status": "PASS_SCOPED" if rows and all(row["passed"] for row in rows) else "FAIL",
            "checks": rows}


def read_save(path, expected_sha=None):
    path = Path(path).resolve(strict=True)
    save_sha = sha(path)
    if expected_sha is not None and save_sha != expected_sha:
        raise ValueError("native archive SHA differs from original receipt")
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("native archive CRC failure")
        raw = archive.read("gamestate")
    roots = list(a.fields(raw.decode("utf-8-sig")))
    objects = {key: body for key, body, obj in roots if obj}
    target = [a.scalars(body) for key, body, obj in roots if obj and key == "saved_event_target"
              and a.scalars(body).get("name") == "eep_mothership0"]
    if len(target) != 1:
        raise ValueError("expected exactly one saved Mother target")
    fleet_id = target[0]["id"]
    fleet = a.block(objects["fleet"], str(fleet_id))
    ship_ids = a.ids(a.block(fleet, "ships"))
    if len(ship_ids) != 1:
        raise ValueError("Mother fleet must contain exactly one actual ship")
    owners = [int(identity) for identity, body, obj in a.fields(objects["country"]) if obj
              and fleet_id in {int(value) for value in re.findall(
                  r"\bfleet\s*=\s*(\d+)", a.block(a.block(body, "fleets_manager"), "owned_fleets"))}]
    country = a.block(objects["country"], "0")
    ship = a.block(objects["ships"], str(ship_ids[0]))
    ship_data = a.scalars(ship)
    if owners != [0] or a.scalars(fleet).get("owner", 0) != 0 or ship_data.get("fleet") != fleet_id:
        raise ValueError("Mother fleet ownership or reverse ship binding differs")
    design_id = a.scalars(a.block(ship, "ship_design_implementation"))["design"]
    design = native.design(a.block(objects["ship_design"], str(design_id)))
    layout = [{"ship_size": stage["native"].get("ship_size"),
               "required_components": stage["required_components"],
               "sections": [{"native": section["native"], "components": section["components"]}
                            for section in stage["sections"]]} for stage in design["stages"]]
    ordinary = {}
    for other in {int(value) for value in re.findall(r"\bfleet\s*=\s*(\d+)", a.block(
            a.block(country, "fleets_manager"), "owned_fleets"))} - {fleet_id}:
        for identity in a.ids(a.block(a.block(objects["fleet"], str(other)), "ships")):
            data = a.scalars(a.block(objects["ships"], str(identity)))
            ordinary[str(identity)] = {key: data.get(key) for key in HEALTH if key.startswith("max_")}
    return {"path": str(path), "sha256": save_sha,
            "gamestate_sha256": hashlib.sha256(raw).hexdigest(),
            "date": next(a.unquote(body) for key, body, obj in roots if key == "date" and not obj),
            "fleet": fleet_id, "ship": ship_ids[0], "owners": owners,
            "country_variables": a.scalars(a.block(country, "variables")),
            "fleet_variables": a.scalars(a.block(fleet, "variables")),
            "ship_variables": a.scalars(a.block(ship, "variables")),
            "health": {key: ship_data.get(key) for key in HEALTH},
            "government": a.block(country, "government"),
            "fleet_modifiers": native.modifiers(fleet)["items"],
            "ship_modifiers": native.modifiers(ship)["items"],
            "country_modifiers": native.modifiers(country)["items"],
            "aura_modifier": a.scalars(a.block(ship, "aura_modifier")),
            "design_id": design_id, "design_body_sha256": design["body_sha256"], "layout": layout,
            "ordinary_ships": ordinary}


def receipt_save(path):
    receipt = load(path)
    state = read_save(receipt["archived"], receipt["sha256"])
    if state["date"] != receipt["date"]:
        raise ValueError("native receipt root date differs")
    state["receipt"] = {"path": str(Path(path).resolve()), "sha256": sha(path)}
    return state


def applicable_model_hashes(tree):
    if tree in SOURCE_REVISIONS:
        return MODEL_HASHES[:SOURCE_REVISIONS[tree][0]]
    if tree == HISTORICAL_RC4_TREE:
        return MODEL_HASHES[:2]
    raise ValueError("no predeclared six-core source model for this candidate tree")


def validate_source_package(mod, actual, tree):
    """Exact reviewed source revisions, plus the indexed historical RC4 API."""
    expected_models = applicable_model_hashes(tree)
    models = [ROOT / "docs/evidence/1019-analysis" / ("six-core-source-expectations-v" + str(i) + ".json")
              for i in range(1, len(expected_models) + 1)]
    if tuple(sha(path) for path in models) != expected_models:
        raise ValueError("predeclared source models changed")
    v1 = load(models[0])
    if tree in SOURCE_REVISIONS:
        model_version, frozen_key = SOURCE_REVISIONS[tree]
        frozen = load(models[model_version - 1])[frozen_key]
        expected_files = frozen["files"]
        selected = frozen["selected_frozen_files_verified_against_manifest"]
        if frozen["production_tree_sha256"] != tree or frozen["file_count"] != len(expected_files):
            raise ValueError("predeclared source revision index differs")
    else:
        source_copy = ROOT / "docs/evidence/1019-requirements/rc4-source-copy.json"
        if sha(source_copy) != HISTORICAL_RC4_SOURCE_COPY_SHA:
            raise ValueError("historical RC4 source index changed")
        frozen = load(source_copy)
        if frozen["tree_sha256"] != tree:
            raise ValueError("historical RC4 source tree differs")
        expected_files = frozen["files"]
        selected = v1["frozen_rc3"]["selected_frozen_files_verified_against_manifest"]
    if sorted(actual, key=lambda item: item["path"]) != sorted(expected_files, key=lambda item: item["path"]):
        raise ValueError("copied package differs from the exact predeclared source tree")
    for source in selected:
        if sha(mod / source["path"]) != source["sha256"]:
            raise ValueError("fixed six-core source model no longer applies: " + source["path"])
    for source in v1["source_evidence"]["native_references"]:
        if sha(source["source"]) != source["sha256"]:
            raise ValueError("native source model bytes changed")


def package(manifest_path):
    """Verify the current copied bytes and the shared source-loading gate; no desktop imports."""
    import publish_1019 as gates
    manifest = load(manifest_path)
    mod = Path(manifest["copied_mod"])
    actual = [{"path": path.relative_to(mod).as_posix(), "bytes": path.stat().st_size,
               "sha256": sha(path)} for path in sorted(mod.rglob("*")) if path.is_file()]
    if sorted(actual, key=lambda item: item["path"]) != sorted(
            manifest["repository_mod_files"], key=lambda item: item["path"]):
        raise ValueError("actual copied package differs from original manifest")
    gate = manifest["static_gate"]
    if (manifest["language"] != "l_simp_chinese" or manifest["game_exe_sha256"] != collector.EXE
            or sha(manifest["game_exe"]) != collector.EXE
            or manifest["repository_mod_tree_sha256"] != manifest["copied_mod_tree_sha256"]
            or gate["source_tree_sha256"] != manifest["copied_mod_tree_sha256"]
            or gate["status"] != "PASS" or sha(gate["report"]) != gate["report_sha256"]):
        raise ValueError("Chinese run, executable, tree or original static report differs")
    report = load(gate["report"])
    if report.get("status") != "PASS":
        raise ValueError("the original static report did not pass")
    gates.validate_weapon_csv_contract(report, mod)
    gates.validate_planet_killer_contract(report, mod)
    validate_source_package(mod, actual, manifest["copied_mod_tree_sha256"])
    return manifest


def counts(state, matter, reward=None, pending=None):
    cv, fv, rows = state["country_variables"], state["fleet_variables"], []
    level, entitled = matter // 10, matter // 50
    reward = entitled if reward is None else reward
    pending = max(entitled - reward, 0) if pending is None else pending
    for key, value in {"eep_c": matter, "eep_mothership_level": level,
                       "eep_mothership_next": 10 - matter % 10, "eep_component_entitled": entitled,
                       "eep_component_rewards": reward, "eep_component_pending": pending,
                       "eep_component_snapshot_state": 0}.items():
        check(rows, key, cv.get(key), value)
    check(rows, "fleet applied level", fv.get("eep_applied_level"), level)
    check(rows, "fleet rewards", fv.get("eep_component_rewards"), reward)
    ranks = [fv.get(key) for key in TIERS]
    check(rows, "six nonnegative integral ranks", all(type(value) in (int, float)
          and math.isfinite(value) and value >= 0 and value == int(value) for value in ranks), True)
    check(rows, "R equals sum ranks", sum(ranks) if all(type(v) in (int, float) for v in ranks) else None, reward)
    for key in TIERS:
        check(rows, "country mirrors " + key, cv.get(key), fv.get(key))
    check(rows, "temporary component budget cleared",
          [key for key in fv if key.startswith("eep_component_") and key not in (*TIERS, "eep_component_rewards")], [])
    growth = [item for item in state["fleet_modifiers"] if item.get("modifier") == "eep_mothership_evolution"]
    check(rows, "one fleet growth modifier", len(growth), int(level > 0))
    if growth:
        check(rows, "growth multiplier", growth[0].get("multiplier", 1), level)
        check(rows, "growth is permanent", growth[0].get("days"), -1)
    check(rows, "fleet has only base and growth modifiers", sorted(item.get("modifier") for item in
          state["fleet_modifiers"]), sorted(["eep_mothership"] + (["eep_mothership_evolution"] if level else [])))
    check(rows, "no ship reward modifiers", state["ship_modifiers"], [])
    components = [component for stage in state["layout"] for section in stage["sections"]
                  for component in section["components"]]
    for slot, core in CORE_SLOTS.items():
        check(rows, core + " actual slot", [(item.get("slot"), item.get("template")) for item in components
              if item.get("template") == core], [(slot, core)])
    return rows


def prediction(baseline, state):
    level = state["country_variables"]["eep_mothership_level"]
    rank = {kind: state["fleet_variables"][key] for kind, key in zip(KINDS, TIERS)}
    old = baseline["ship_variables"]
    result = {"max_hitpoints": baseline["health"]["max_hitpoints"] + 1500*level + 3000*rank["hull"],
              "max_armor_hitpoints": baseline["health"]["max_armor_hitpoints"] + 1287*level + 2574*rank["armor"],
              "max_shield_hitpoints": baseline["health"]["max_shield_hitpoints"] + 2091.375*level + 4182.75*rank["shield"]}
    for key in collector.MODIFIERS:
        delta = 0
        if key in ("ship_hull_mult", "ship_armor_mult", "ship_shield_mult"):
            delta = .05*level + .1*rank[key.split("_")[1]]
        elif key == "ship_weapon_damage":
            delta = .05*level + .05*rank["damage"]
        elif key == "ship_tracking_add":
            delta = 3*rank["tracking"]
        elif key in ("ship_hull_regen_add_static", "ship_armor_regen_add_static"):
            delta = .1*level + .2*rank["regen"]
        result["eep_probe_" + key] = old["eep_probe_" + key] + delta
    return result


def business(state):
    keys = ("eep_c", "eep_mothership_level", "eep_mothership_next", "eep_component_entitled",
            "eep_component_rewards", "eep_component_pending", "eep_component_snapshot_state", *TIERS)
    return {"country": {key: state["country_variables"].get(key) for key in keys},
            "fleet_variables": state["fleet_variables"], "health": state["health"],
            "layout": state["layout"], "government": state["government"],
            "modifiers": [state[key] for key in ("fleet_modifiers", "ship_modifiers", "country_modifiers", "aura_modifier")],
            "diagnostics": {key: state["ship_variables"].get(key) for key in collector.PROBES},
            "identity": [state["fleet"], state["ship"], state["owners"]]}


def comparison(before, after, name):
    rows = []
    check(rows, name + " same native date", after["date"], before["date"])
    previous, current = business(before), business(after)
    for key in ("health", "diagnostics"):
        old_values, new_values = previous.pop(key), current.pop(key)
        for field, value in old_values.items():
            compare = close_hp if key == "health" or field in ("eep_probe_max_hull", "eep_probe_max_armor") else close
            compare(rows, name + " " + field, new_values.get(field), value)
    check(rows, name + " discrete business signature", current, previous)
    result = scope(rows)
    result.update(strict_gamestate_equal=after["gamestate_sha256"] == before["gamestate_sha256"],
                  strict_scope="Exact unedited gamestate bytes; false does not become a full-save PASS.",
                  before={key: before[key] for key in ("path", "sha256", "design_id", "design_body_sha256")},
                  after={key: after[key] for key in ("path", "sha256", "design_id", "design_body_sha256")})
    return result


def government_identity(raw):
    """Keep direct native fields verbatim except one finite scalar time counter."""
    identity, progress = [], {"present": False, "raw": None, "value": None}
    for key, body, obj in a.fields(raw):
        if key != "council_agenda_progress":
            identity.append({"key": key, "raw": body, "object": obj})
            continue
        if progress["present"]:
            raise ValueError("duplicate direct council_agenda_progress")
        if obj or not re.fullmatch(r"-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", body):
            raise ValueError("direct council_agenda_progress must be a finite numeric scalar")
        value = float(body)
        if not math.isfinite(value):
            raise ValueError("direct council_agenda_progress must be a finite numeric scalar")
        progress = {"present": True, "raw": body, "value": value}
    return {"identity": identity, "council_agenda_progress": progress}


def matrix_government_comparison(rows, name, before, after):
    previous, current = government_identity(before["government"]), government_identity(after["government"])
    same_date = before["date"] == after["date"]
    check(rows, name, after["government"] if same_date else current["identity"],
          before["government"] if same_date else previous["identity"])
    old_progress, new_progress = previous["council_agenda_progress"], current["council_agenda_progress"]
    return {"check": name, "mode": "same_date_raw_exact" if same_date else "cross_date_structural_identity",
            "before": {"date": before["date"], "raw": before["government"], **previous},
            "after": {"date": after["date"], "raw": after["government"], **current},
            "raw_equal": before["government"] == after["government"],
            "raw_diff": list(difflib.unified_diff(before["government"].splitlines(keepends=True),
                                                  after["government"].splitlines(keepends=True),
                                                  fromfile="before_government", tofile="after_government")),
            "progress_delta": new_progress["value"] - old_progress["value"]
                if old_progress["present"] and new_progress["present"] else None}


def budget_comparison(before, first, second, mode):
    rows = counts(first, 20500, 400, 10) + counts(second, 20500, 410, 0)
    check(rows, "single budget source rewards", before["fleet_variables"].get("eep_component_rewards"), 200)
    check(rows, "same-day controlled budget", first["date"], before["date"])
    expected_date = collector.next_month(first["date"]) if mode == "monthly" else first["date"]
    check(rows, "next-month native compensation" if mode == "monthly" else "same-day manual second sync",
          second["date"], expected_date)
    for label, previous, after, gain in (("first", before, first, 200), ("second", first, second, 10)):
        check(rows, label + " total tier gain", sum(after["fleet_variables"][key] - previous["fleet_variables"][key] for key in TIERS), gain)
        check(rows, label + " no tier reductions", all(after["fleet_variables"][key] >= previous["fleet_variables"][key] for key in TIERS), True)
        check(rows, label + " equipment unchanged", after["layout"], previous["layout"])
        check(rows, label + " Mother identity unchanged", [after["fleet"], after["ship"]], [previous["fleet"], previous["ship"]])
    result = scope(rows)
    result.update(path=("native next-month automatic compensation" if mode == "monthly" else "manual same-day compensation"),
                  attributes="Counts only; newly awarded triggered modifiers need their own refresh window.",
                  first={key: first[key] for key in ("path", "sha256", "date", "receipt") if key in first},
                  second={key: second[key] for key in ("path", "sha256", "date", "receipt") if key in second})
    return result


def entry(args):
    receipt = Path(args.anchor_receipt).resolve(strict=True)
    manifest = package(receipt.parent / "manifest.json")
    state = receipt_save(receipt)
    plan = collector.make_plan(receipt, args.prefix, 0, state["fleet"], state["ship"],
                               manifest["copied_mod_tree_sha256"], args.autosave_dir)
    command = [sys.executable, str(ROOT / "tools/runtime_growth_1019.py"), "--anchor-receipt", str(receipt),
               "--prefix", args.prefix, "--fleet", str(state["fleet"]), "--ship", str(state["ship"]),
               "--expected-tree", plan["expected_tree_sha256"], "--autosave-dir", plan["autosave_dir"]]
    return {"status": "PLAN_ONLY", "plan": plan, "dry_run_command": subprocess.list2cmdline(command + ["--dry-run"]),
            "execute_command_for_root_only": subprocess.list2cmdline(command + ["--execute"]),
            "desktop_runtime_imported": "runtime_1019" in sys.modules}


def report(args):
    original = load(args.receipt)
    plan, rows = original["plan"], []
    manifest = package(plan["manifest"])
    check(rows, "original collection completed", original.get("state"), "COLLECTED_NOT_ACCEPTED")
    check(rows, "expected nine nodes", plan.get("nodes"), list(collector.NODES))
    check(rows, "same run", plan["run_id"], manifest["run_id"])
    check(rows, "manifest SHA", sha(plan["manifest"]), plan["manifest_sha256"])
    check(rows, "artifact run", str(Path(plan["artifacts"]).resolve()), str(Path(manifest["artifact_dir"]).resolve()))
    check(rows, "anchor receipt SHA", sha(plan["anchor_receipt"]), plan["anchor_receipt_sha256"])
    check(rows, "plan candidate tree", plan["expected_tree_sha256"], manifest["copied_mod_tree_sha256"])
    check(rows, "expected eighteen ZIPs", len(original["snapshots"]), 18)
    check(rows, "expected thirty-six commands", len(original["commands"]), 36)
    check(rows, "native cleanup", original.get("cleanup_errors"), [])
    anchor_state = receipt_save(plan["anchor_receipt"])
    check(rows, "original clean anchor SHA", anchor_state["sha256"], plan["anchor_sha256"])
    rows.extend(counts(anchor_state, 0))
    date_cursor = anchor_state["date"]
    states, evidence, government_observations, government_comparisons = [], [], [], []
    for index, binding in enumerate(original["snapshots"]):
        state = read_save(binding["archived"], binding["sha256"])
        government_observations.append({"snapshot": index, "date": state["date"],
                                        "raw": state["government"], **government_identity(state["government"])})
        if index >= len(plan["phases"]):
            raise ValueError("more actual snapshots than declared phases")
        phase = plan["phases"][index]
        date_cursor = collector.next_month(date_cursor)
        check(rows, "native thirty-day calendar " + str(index), state["date"], date_cursor)
        check(rows, "declared phase date " + str(index), phase["date"], date_cursor)
        check(rows, "declared node C " + str(index), phase["C"], collector.NODES[index//2])
        check(rows, "declared refresh-final sequence " + str(index), phase["phase"], "refresh" if index % 2 == 0 else "final")
        check(rows, "binding date " + str(index), binding["date"], state["date"])
        check(rows, "phase " + str(index), binding["phase"], phase["phase"])
        check(rows, "matter binding " + str(index), binding["C"], phase["C"])
        check(rows, "fresh native mtime " + str(index), binding["source_mtime_ns"] > max(
            binding["source_prior_mtime_ns"], binding["command_started_ns"] - 1), True)
        check(rows, "HUD date " + str(index), binding["hud"]["date"], state["date"])
        check(rows, "GPU bytes " + str(index), sha(binding["hud"]["image"]), binding["hud"]["image_sha256"])
        ocr = load(binding["hud"]["ocr"])
        check(rows, "OCR native date " + str(index), any(row.get("text") == state["date"] and row.get("score", 0) >= .8
              for row in ocr["rows"]), True)
        check(rows, "OCR image binding " + str(index), ocr["image_sha256"], binding["hud"]["image_sha256"])
        check(rows, "GPU geometry " + str(index), ocr["resolution"], [1024, 768])
        for offset, expected_command in enumerate((phase["before_forward"], "fast_forward 30")):
            command = original["commands"][index*2+offset]
            check(rows, "actual command " + str(index) + "/" + str(offset), command["command"], expected_command)
            check(rows, "console evidence " + str(index) + "/" + str(offset), sha(command["console_frame"]),
                  command["console_frame_sha256"])
        check(rows, "effect explicit source scope " + str(index), phase["before_forward"],
              "effect root={set_variable={which=eep_c value=" + str(phase["C"]) + "} eep_sync_mothership=yes}"
              if index % 2 == 0 else collector.export_command())
        evidence.append({"phase": phase, "archive": state["path"], "sha256": state["sha256"],
                         "gamestate_sha256": state["gamestate_sha256"],
                         "hud": binding["hud"], "ocr_sha256": sha(binding["hud"]["ocr"])})
        rows.extend(counts(state, phase["C"]))
        if states:
            check(rows, "stable equipment " + str(index), state["layout"], states[0]["layout"])
            government_comparisons.append(matrix_government_comparison(
                rows, "stable government " + str(index), states[0], state))
            check(rows, "stable Mother identity " + str(index), [state["fleet"], state["ship"]],
                  [states[0]["fleet"], states[0]["ship"]])
            check(rows, "tiers never decrease " + str(index), all(state["fleet_variables"][key] >=
                  states[-1]["fleet_variables"][key] for key in TIERS), True)
        states.append(state)
    if len(states) == 18:
        baseline = states[1]
        check(rows, "baseline Machine civic", "civic_machine_terminator" in baseline["government"], True)
        for index in range(9):
            refresh, final = states[index*2:index*2+2]
            check(rows, "refresh-final counters " + str(index),
                  {key: refresh["fleet_variables"].get(key) for key in (*TIERS, "eep_component_rewards", "eep_applied_level")},
                  {key: final["fleet_variables"].get(key) for key in (*TIERS, "eep_component_rewards", "eep_applied_level")})
            expected = prediction(baseline, final)
            for key, value in expected.items():
                if key.startswith("max_"):
                    close_hp(rows, "refresh " + str(index) + " " + key, refresh["health"].get(key), value)
                    close_hp(rows, "final " + str(index) + " " + key, final["health"].get(key), value)
                else:
                    close(rows, "export " + str(index) + " " + key, final["ship_variables"].get(key), value)
            for probe, health in (("eep_probe_max_hull", "max_hitpoints"), ("eep_probe_max_armor", "max_armor_hitpoints")):
                close_hp(rows, "refresh-day trigger " + str(index) + " " + probe,
                         final["ship_variables"].get(probe), refresh["health"][health])
            check(rows, "diagnostic input date " + str(index), original["snapshots"][index*2+1]["diagnostics_from_date"], refresh["date"])
    matrix = scope(rows)
    if len(states) != 18:
        matrix["status"] = "INCOMPLETE"
    controls = []
    ordinary_base = states[0]["ordinary_ships"] if states else {}
    check(controls, "at least one owned ordinary ship", bool(ordinary_base), True)
    ordinary_channels = {key: any(type(values.get(key)) in (int, float) and values[key] > 0
                                   for values in ordinary_base.values()) for key in HEALTH if key.startswith("max_")}
    for key, covered in ordinary_channels.items():
        check(controls, "positive ordinary native maximum " + key, covered, True)
    for index, state in enumerate(states):
        check(controls, "ordinary identities " + str(index), sorted(state["ordinary_ships"]), sorted(ordinary_base))
        for identity in sorted(set(ordinary_base) & set(state["ordinary_ships"])):
            for key, value in ordinary_base[identity].items():
                actual = state["ordinary_ships"][identity][key]
                if value is None:
                    check(controls, "ordinary absent native field " + str(index) + "/" + identity + "/" + key, actual, None)
                else:
                    close_hp(controls, "ordinary native max " + str(index) + "/" + identity + "/" + key, actual, value)
    ordinary_controls = scope(controls)
    ordinary_controls.update(ship_ids=sorted(ordinary_base), native_maximum_channel_coverage=ordinary_channels,
                             scope="Same-owned ordinary ships native maximum hull/armor/shield throughout all eighteen snapshots; no ordinary damage/tracking/regen export claim.")
    supplements = {"repeat": {"status": "NOT_PROVIDED"}, "reload": {"status": "NOT_PROVIDED"},
                   "budget": {"status": "NOT_PROVIDED"}}

    def manual(path):
        if Path(path).resolve().parent != Path(plan["artifacts"]).resolve():
            raise ValueError("manual native receipt belongs to another run")
        state = receipt_save(path)
        if Path(state["path"]).parent != Path(plan["artifacts"]).resolve():
            raise ValueError("manual native archive belongs to another run")
        return state

    if states and args.repeat_receipt:
        repeated = manual(args.repeat_receipt)
        supplements["repeat"] = comparison(states[-1], repeated, "same-day repeated sync")
        if args.reload_receipt:
            supplements["reload"] = comparison(repeated, manual(args.reload_receipt), "same-day reload")
    if states and args.budget_first_receipt and args.budget_second_receipt:
        first, second = manual(args.budget_first_receipt), manual(args.budget_second_receipt)
        supplements["budget"] = budget_comparison(states[-1], first, second, args.budget_second_mode)
    statuses = [matrix["status"], ordinary_controls["status"], *(item["status"] for item in supplements.values())]
    coverage = {kind: bool(states and states[-1]["fleet_variables"].get(key, 0) > 0)
                for kind, key in zip(KINDS, TIERS)}
    status = "FAIL" if "FAIL" in statuses else "PASS_SCOPED" if all(s == "PASS_SCOPED" for s in statuses) else "INCOMPLETE"
    if status == "PASS_SCOPED" and not all(coverage.values()):
        status = "INCOMPLETE"
    startup = {"status": "NOT_PROVIDED"}
    if args.startup_receipt:
        initial, anchor = manual(args.startup_receipt), receipt_save(plan["anchor_receipt"])
        stability = []
        check(stability, "startup and year1 Mother identity", [initial["fleet"], initial["ship"]],
              [anchor["fleet"], anchor["ship"]])
        for key in HEALTH:
            if key.startswith("max_"):
                close_hp(stability, "startup-year1 Mother " + key, anchor["health"][key], initial["health"][key])
        check(stability, "ordinary ship identities", sorted(anchor["ordinary_ships"]), sorted(initial["ordinary_ships"]))
        for identity in sorted(set(initial["ordinary_ships"]) & set(anchor["ordinary_ships"])):
            for key, value in initial["ordinary_ships"][identity].items():
                label = "startup-year1 ordinary " + identity + " " + key
                if value is None:
                    check(stability, label + " absent native field", anchor["ordinary_ships"][identity][key], None)
                else:
                    close_hp(stability, label, anchor["ordinary_ships"][identity][key], value)
        startup = scope(stability)
        startup.update(initial={key: initial[key] for key in ("path", "sha256", "date")},
                       year1_anchor={key: anchor[key] for key in ("path", "sha256", "date")})
        if startup["status"] == "FAIL":
            status = "FAIL"
    baseline_summary = None
    if len(states) == 18:
        baseline_summary = {"C": states[1]["country_variables"].get("eep_c"),
                            "L": states[1]["country_variables"].get("eep_mothership_level"),
                            "tiers": {kind: states[1]["fleet_variables"].get(key) for kind, key in zip(KINDS, TIERS)},
                            "actual_native_intercept": True,
                            "modifier_exports": {key: states[1]["ship_variables"].get("eep_probe_" + key) for key in collector.MODIFIERS},
                            "native_maximums": {key: states[1]["health"][key] for key in HEALTH if key.startswith("max_")},
                            "path": states[1]["path"], "save_sha256": states[1]["sha256"], "date": states[1]["date"],
                            "diagnostics_from_date": states[0]["date"]}
    return {"status": status, "schema": "eep.six-core-growth-report.v1", "absolute_tolerance": TOLERANCE,
            "hp_tolerance_contract": HP_TOLERANCE_CONTRACT,
            "hp_tolerance": {"absolute_floor": TOLERANCE, "binary32_ulps": HP_ULPS, "relative_tolerance": 0,
                             "classification": "predeclared_engineering_allowance_not_engine_storage_proof"},
            "component_attribution_contract": "source_separated_native_rng_v1",
            "government_identity_contract": "cross_date_direct_finite_agenda_progress_observation_v1",
            "government_observations": government_observations, "government_comparisons": government_comparisons,
            "run_id": manifest["run_id"], "production_tree_sha256": manifest["copied_mod_tree_sha256"],
            "C0_baseline": baseline_summary,
            "final_native_tiers": {kind: states[-1]["fleet_variables"].get(key) if states else None for kind, key in zip(KINDS, TIERS)},
            "receipt": {"path": str(Path(args.receipt).resolve()), "sha256": sha(args.receipt)},
            "tool_sha256": sha(__file__), "source_models_sha256": applicable_model_hashes(manifest["copied_mod_tree_sha256"]),
            "matrix": matrix, **supplements, "ordinary_controls": ordinary_controls,
            "startup_stability": startup, "native_evidence": evidence,
            "nonzero_tier_coverage": coverage,
            "limits": ["Scoped native max HP and exported modifier channels; no panel DPS or actual healing claim.",
                       "External unexported modifiers, report UI, destroyed-Mother behavior and ordinary-ship controls require separate evidence.",
                       "Exact full gamestate equality remains separate from business reload equality."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("entry")
    prepare.add_argument("--anchor-receipt", required=True, type=Path)
    prepare.add_argument("--prefix", required=True)
    prepare.add_argument("--autosave-dir", type=Path)
    review = commands.add_parser("report")
    review.add_argument("--receipt", required=True, type=Path)
    for label in ("repeat", "reload", "budget-first", "budget-second"):
        review.add_argument("--" + label + "-receipt", type=Path)
    review.add_argument("--startup-receipt", type=Path)
    review.add_argument("--budget-second-mode", choices=("monthly", "manual"), default="monthly")
    review.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "entry":
        result = entry(args)
    else:
        if args.output.exists():
            raise FileExistsError("refusing to overwrite a growth report")
        try:
            result = report(args)
        except Exception as error:
            result = {"status": "FAIL", "error_type": type(error).__name__, "error": str(error),
                      "receipt": {"path": str(args.receipt.resolve()), "sha256": sha(args.receipt)},
                      "tool_sha256": sha(__file__), "acceptance": "No missing or invalid evidence inferred."}
        collector.write_new(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
