"""Collect native growth observations; desktop imports require explicit --execute."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import time
import zipfile
import zlib

import audit_save as a

NODES = (0, 9, 10, 19, 20, 49, 50, 200, 10000)
TIERS = tuple("eep_component_" + k + "_level" for k in
              ("shield", "armor", "hull", "damage", "tracking", "regen"))
MODIFIERS = ("ship_hull_add", "ship_hull_mult", "ship_armor_add", "ship_armor_mult",
             "ship_shield_add", "ship_shield_mult", "ship_weapon_damage",
             "ship_tracking_add", "ship_hull_regen_add_static", "ship_armor_regen_add_static")
PROBES = tuple("eep_probe_" + key for key in MODIFIERS) + (
    "eep_probe_max_hull", "eep_probe_max_armor")
TREE = "178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116"
EXE = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    with Path(path).open("xb") as stream:
        stream.write(raw)


def next_month(date):
    match = re.fullmatch(r"(\d{4})\.(0[1-9]|1[0-2])\.01", date)
    if not match:
        raise ValueError("growth autosave anchor must be a native month-first date")
    year, month = map(int, match.groups())
    return f"{year + (month == 12):04}.{month % 12 + 1:02}.01"


def export_command():
    effects = ["export_modifier_to_variable={modifier=" + key
               + " variable=eep_probe_" + key + "}" for key in MODIFIERS]
    effects += ["export_trigger_value_to_variable={trigger=has_max_hp variable=eep_probe_max_hull}",
                "export_trigger_value_to_variable={trigger=has_max_armor_hp variable=eep_probe_max_armor}"]
    return "effect event_target:eep_mothership0={every_owned_ship={" + " ".join(effects) + "}}"


def native_state(raw, country, fleet, ship):
    """Read actual state, including duplicate event-target root fields; never edit ZIP."""
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        native = archive.read("gamestate")
        if archive.testzip() is not None:
            raise ValueError("incomplete native ZIP")
    roots = list(a.fields(native.decode("utf-8-sig")))
    containers = {k: v for k, v, obj in roots if obj and k in ("country", "fleet", "ships", "ship_design")}
    countries = a.block(containers.get("country", ""), str(country))
    mother = a.block(containers.get("fleet", ""), str(fleet))
    vessel = a.block(containers.get("ships", ""), str(ship))
    if not countries or not mother or not vessel:
        raise ValueError("expected native country/Mother fleet/ship absent")
    targets = [a.scalars(v) for k, v, obj in roots if k == "saved_event_target" and obj
               and a.scalars(v).get("name") == "eep_mothership" + str(country)]
    fleet_data, ship_data = a.scalars(mother), a.scalars(vessel)
    owners = []
    for identity, body, obj in a.fields(containers["country"]):
        if obj:
            owned = a.block(a.block(body, "fleets_manager"), "owned_fleets")
            if fleet in {int(value) for value in re.findall(r"\bfleet\s*=\s*(\d+)", owned)}:
                owners.append(int(identity))
    if (len(targets) != 1 or targets[0].get("id") != fleet
            or owners != [country] or fleet_data.get("owner", country) != country
            or ship_data.get("fleet") != fleet
            or a.ids(a.block(mother, "ships")) != [ship]):
        raise ValueError("Mother target/ownership/unique ship binding differs")
    health_keys = ("hitpoints", "max_hitpoints", "armor_hitpoints", "max_armor_hitpoints",
                   "shield_hitpoints", "max_shield_hitpoints")
    if not all(key in ship_data for key in health_keys):
        raise ValueError("actual native ship health fields are missing")
    design_id = a.scalars(a.block(vessel, "ship_design_implementation")).get("design")
    design = a.block(containers.get("ship_design", ""), str(design_id))
    core_counts = {"EEP_ADAPTIVE_" + k.upper() + "_CORE": len(re.findall(
        r'\btemplate\s*=\s*"?' + "EEP_ADAPTIVE_" + k.upper() + r'_CORE"?(?=\s|})', design))
        for k in ("shield", "armor", "hull", "damage", "tracking", "regen")}
    return {"status": "OBSERVATION_ONLY",
            "date": next(a.unquote(v) for k, v, obj in roots if k == "date" and not obj),
            "save_sha256": digest(raw), "gamestate_sha256": digest(native),
            "country_id": country, "fleet_id": fleet, "ship_id": ship,
            "ownership_source": "country.fleets_manager.owned_fleets", "owner_country_ids": owners,
            "country_variables": a.scalars(a.block(countries, "variables")),
            "fleet_variables": a.scalars(a.block(mother, "variables")),
            "ship_variables": a.scalars(a.block(vessel, "variables")),
            "government_raw": a.block(countries, "government"),
            "design_id": design_id, "design_body_sha256": digest(design.encode("utf-8")),
            "core_counts": core_counts,
            "native_ship": {key: ship_data[key] for key in health_keys}}


def require_clean(state):
    cv, fv = state["country_variables"], state["fleet_variables"]
    if (cv.get("eep_c") != 0 or cv.get("eep_mothership_level", 0) != 0
            or fv.get("eep_applied_level", 0) != 0
            or any(fv.get(k, 0) != 0 or cv.get(k, 0) != 0 for k in (*TIERS, "eep_component_rewards"))
            or cv.get("eep_component_entitled", 0) != 0 or cv.get("eep_component_pending", 0) != 0):
        raise ValueError("dirty C0: nonzero matter, growth, tier, reward or pending state")
    if "civic_machine_terminator" not in state["government_raw"]:
        raise ValueError("the expected Machine terminator government is absent")
    if any(value != 1 for value in state["core_counts"].values()):
        raise ValueError("all six actual hardware cores must be installed exactly once")


def make_plan(anchor_receipt, prefix, country=0, fleet=159, ship=997, expected_tree=TREE,
              autosave_dir=None):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,20}", prefix):
        raise ValueError("prefix must be 1-20 safe ASCII characters")
    if country != 0:
        raise ValueError("console root is player country0; other countries are unsupported")
    receipt_path = Path(anchor_receipt).resolve(strict=True)
    artifacts = receipt_path.parent
    if list(artifacts.glob(prefix + "*")):
        raise FileExistsError("prefix already has artifacts; use a new prefix")
    receipt = read_json(receipt_path)
    archive = Path(receipt["archived"]).resolve(strict=True)
    raw = archive.read_bytes()
    if digest(raw) != receipt["sha256"]:
        raise ValueError("anchor SHA differs from native receipt")
    state = native_state(raw, country, fleet, ship)
    require_clean(state)
    if state["date"] != receipt["date"]:
        raise ValueError("native anchor date differs from receipt")
    next_month(state["date"])
    manifest_path = artifacts / "manifest.json"
    manifest = read_json(manifest_path)
    if (manifest.get("language") != "l_simp_chinese" or manifest.get("game_exe_sha256") != EXE
            or manifest.get("profile_id") != "eep-0.4.0-single-production-mod"
            or manifest.get("repository_mod_tree_sha256") != expected_tree
            or manifest.get("copied_mod_tree_sha256") != expected_tree):
        raise ValueError("anchor run differs from the Chinese gated candidate")
    user = Path(manifest["userdir"]).resolve(strict=True)
    actual_anchor = Path(receipt.get("history", receipt["written_at"])).resolve(strict=True)
    if digest(actual_anchor.read_bytes()) != receipt["sha256"]:
        raise ValueError("actual native load anchor differs from archived bytes")
    folder = Path(autosave_dir).resolve(strict=True) if autosave_dir else actual_anchor.parent
    folder.relative_to((user / "save games").resolve(strict=True))
    phases, date = [], state["date"]
    for index, matter in enumerate(NODES):
        stage = f"{prefix}-n{index:02}-c{matter}"
        for phase in ("refresh", "final"):
            input_date = date
            date = next_month(date)
            phases.append({"node": index, "C": matter, "phase": phase,
                           "stage": stage + "-" + phase, "date": date, "input_date": input_date,
                           "fast_forward": "fast_forward 30",
                           "before_forward": ("effect root={set_variable={which=eep_c value=" + str(matter)
                                              + "} eep_sync_mothership=yes}")
                           if phase == "refresh" else export_command()})
    return {"status": "OBSERVATION_ONLY", "mode": "PLAN_ONLY", "prefix": prefix,
            "anchor_receipt": str(receipt_path), "anchor_receipt_sha256": digest(receipt_path.read_bytes()),
            "anchor_sha256": receipt["sha256"], "anchor_date": state["date"],
            "manifest": str(manifest_path), "manifest_sha256": digest(manifest_path.read_bytes()),
            "run_id": manifest["run_id"], "artifacts": str(artifacts), "userdir": str(user),
            "autosave_dir": str(folder), "expected_tree_sha256": expected_tree,
            "country": country, "fleet": fleet, "ship": ship,
            "phases": phases, "nodes": list(NODES), "20500": "manual same-day counts-only branch"}


def fresh_native(path, prior_mtime_ns, started_ns, expected_date, identity):
    """One stable read; the caller polls this while the native ZIP is being written."""
    path = Path(path)
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    if (before.st_mtime_ns != after.st_mtime_ns or before.st_size != after.st_size
            or len(raw) != after.st_size or after.st_mtime_ns <= prior_mtime_ns
            or after.st_mtime_ns < started_ns):
        raise ValueError("native autosave is stale or still changing")
    state = native_state(raw, *identity)
    if state["date"] != expected_date:
        raise ValueError("native ZIP root date differs from observed HUD date")
    return raw, state, {"source": str(path.resolve()), "source_prior_mtime_ns": prior_mtime_ns,
                        "source_mtime_ns": after.st_mtime_ns, "bytes": len(raw),
                        "command_started_ns": started_ns, "date": state["date"],
                        "sha256": state["save_sha256"]}


class LiveBackend:
    def __init__(self, plan):
        # No desktop imports, pointer reads or artifact directories in dry-run mode.
        import runtime_1019 as runtime
        self.base, self.h = runtime.base, runtime.base.h
        self.plan, self.confirmed = plan, None
        artifacts, user, manifest = self.h.load_run()
        if (artifacts.resolve() != Path(plan["artifacts"]) or user.resolve() != Path(plan["userdir"])
                or manifest["run_id"] != plan["run_id"]
                or digest((artifacts / "manifest.json").read_bytes()) != plan["manifest_sha256"]):
            raise RuntimeError("active run differs from the verified native anchor")
        gate = manifest.get("static_gate", {})
        report_path = Path(gate["report"])
        report = read_json(report_path)
        copied_mod = Path(manifest["copied_mod"])
        if (gate.get("status") != "PASS" or gate.get("source_tree_sha256") != plan["expected_tree_sha256"]
                or digest(report_path.read_bytes()) != gate.get("report_sha256")
                or report.get("status") != "PASS"
                or self.h.tree_manifest(copied_mod)[1] != plan["expected_tree_sha256"]
                or self.h.sha256(Path(manifest["game_exe"])) != EXE):
            raise RuntimeError("current copied candidate or repaired package gate differs")
        runtime.release_gate.validate_weapon_csv_contract(report, copied_mod)
        runtime.release_gate.validate_planet_killer_contract(report, copied_mod)
        settings = (user / "settings.txt").read_text(encoding="utf-8-sig")
        if not re.search(r"(?m)^autosave\s*=\s*2\s*$", settings):
            raise RuntimeError("native monthly autosave setting is not enabled")

    def confirm(self, stage):
        artifacts, user, manifest = self.h.load_run()
        if (artifacts.resolve() != Path(self.plan["artifacts"])
                or user.resolve() != Path(self.plan["userdir"])
                or manifest["run_id"] != self.plan["run_id"]):
            raise RuntimeError("active run changed before physical input")
        frame = self.confirmed or self.h.capture(stage + "-console-state")
        if not self.base.console_visible(frame):
            self.h.press_scan_code(0x29, stage + "-console-open", 1)
            frame = self.h.capture(stage + "-console-ready")
        if not self.base.console_visible(frame) or frame["resolution"] != [1024, 768]:
            raise RuntimeError("observed console/geometry missing; refusing physical input")
        self.confirmed = frame
        return frame

    def initial(self):
        frame = self.h.capture(self.plan["prefix"] + "-initial")
        if not any(r["text"] == self.plan["anchor_date"] and r["score"] >= .8 for r in frame["rows"]):
            raise RuntimeError("loaded native HUD date differs from clean anchor")
        self.confirmed = frame

    def command(self, command, stage):
        frame = self.confirm(stage)
        self.h.click_point(120, 322, stage + "-focus")
        action = self.h.type_text(command, True, stage + "-command")
        return {"command": command, "console_frame": frame["image"],
                "console_frame_sha256": frame["image_sha256"], "input_action": action,
                "frame_reuse": "only known commands retaining the native console; refreshed at every HUD observation"}

    def wait_date(self, date, stage):
        frame = self.base.previous.wait_for_native_date(date, stage, 180)
        self.confirmed = frame
        return {"date": date, "image": frame["image"], "image_sha256": frame["image_sha256"],
                "ocr": str(Path(frame["image"]).with_suffix(".ocr.json"))}

    def cleanup(self):
        errors = []
        for callback, label in ((self.base.close_console, "console"),
                                (self.base.close_debug_overlay, "debug")):
            try:
                callback(self.plan["prefix"] + "-exit-" + label)
            except Exception as error:
                errors.append(label + ": " + str(error))
        return errors


def collect(plan, backend_factory=LiveBackend, autosave_timeout=25):
    artifacts = Path(plan["artifacts"])
    if list(artifacts.glob(plan["prefix"] + "*")):
        raise FileExistsError("refusing to overwrite an existing growth prefix")
    receipt_path = artifacts / (plan["prefix"] + "-growth-receipt.json")
    receipt = {"status": "OBSERVATION_ONLY", "state": "STARTING", "plan": plan,
               "collector_sha256": digest(Path(__file__).read_bytes()), "snapshots": [], "commands": []}
    write_new(receipt_path, receipt)

    def progress():
        # This invocation owns this new progress receipt; snapshots themselves are immutable.
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    backend = None
    try:
        backend = backend_factory(plan)
        backend.initial()
        for phase in plan["phases"]:
            stage, expected = phase["stage"], phase["date"]
            source = Path(plan["autosave_dir"]) / ("autosave_" + expected + ".sav")
            old_mtime = source.stat().st_mtime_ns if source.exists() else 0
            command = backend.command(phase["before_forward"], stage + "-effect")
            receipt["commands"].append(command)
            started = time.time_ns()
            receipt["commands"].append(backend.command("fast_forward 30", stage + "-advance"))
            receipt["inflight"] = {"stage": stage, "expected_date": expected,
                                   "source": str(source), "prior_mtime_ns": old_mtime,
                                   "command_started_ns": started}
            progress()
            print(json.dumps({"status": "OBSERVATION_ONLY", "phase": stage, "awaiting_hud": expected}), flush=True)
            hud = backend.wait_date(expected, stage + "-hud")
            deadline = time.monotonic() + autosave_timeout
            last_error = None
            while time.monotonic() < deadline:
                try:
                    raw, state, binding = fresh_native(source, old_mtime, started, expected,
                                                       (plan["country"], plan["fleet"], plan["ship"]))
                    break
                except (OSError, ValueError, KeyError, EOFError, zipfile.BadZipFile, zlib.error) as error:
                    last_error = str(error)
                    time.sleep(.2)
            else:
                raise RuntimeError("fresh complete native autosave unavailable: " + str(last_error))
            target = artifacts / (stage + ".sav")
            with target.open("xb") as stream:
                stream.write(raw)
            binding.update({"archived": str(target), "phase": phase["phase"], "C": phase["C"],
                            "effect_input_hud_date": phase["input_date"],
                            "diagnostics_from_date": phase["input_date"] if phase["phase"] == "final" else None,
                            "hud": hud, "observed_at_utc": datetime.now(timezone.utc).isoformat()})
            receipt["snapshots"].append(binding)
            progress()
            audit = a.audit(target, (plan["country"],))
            if audit["save_sha256"] != binding["sha256"] or audit["date"] != expected:
                raise RuntimeError("archive/audit SHA or date differs from native input")
            write_new(target.with_suffix(".audit.json"), audit)
            write_new(target.with_suffix(".growth-observation.json"), state)
            receipt.pop("inflight", None)
            progress()
            if state["country_variables"].get("eep_c") != phase["C"]:
                raise RuntimeError("actual native matter differs from requested controlled node")
            if phase["node"] == 0:
                require_clean(state)
            if phase["phase"] == "final" and not all(k in state["ship_variables"] for k in PROBES):
                raise RuntimeError("final native autosave is missing requested diagnostic exports")
            print(json.dumps({"status": "OBSERVATION_ONLY", "phase": stage, "date": expected,
                              "sha256": binding["sha256"], "archived": str(target)}), flush=True)
        receipt["state"] = "COLLECTED_NOT_ACCEPTED"
    except Exception as error:
        receipt.update(state="ABORTED", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        receipt["cleanup_errors"] = backend.cleanup() if backend else []
        if receipt["cleanup_errors"]:
            receipt["state"] = "CLEANUP_REQUIRED"
        progress()
    if receipt["cleanup_errors"]:
        raise RuntimeError("native cleanup needs inspection: " + "; ".join(receipt["cleanup_errors"]))
    return {"status": "OBSERVATION_ONLY", "receipt": str(receipt_path),
            "snapshots": len(receipt["snapshots"]), "acceptance": "NOT_PERFORMED"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor-receipt", required=True, type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--country", type=int, default=0)
    parser.add_argument("--fleet", type=int, default=159)
    parser.add_argument("--ship", type=int, default=997)
    parser.add_argument("--expected-tree", default=TREE)
    parser.add_argument("--autosave-dir", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    plan = make_plan(args.anchor_receipt, args.prefix, args.country, args.fleet, args.ship,
                     args.expected_tree, args.autosave_dir)
    result = collect(plan) if args.execute else plan
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
