"""Read-only reviewed-source migration v2; never rewrites v1 evidence or SAVs."""
import argparse
import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile

import check_1019 as v1

SCHEMA = "eep.1019.migration-case.v2"
EXE = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
RC7_TREE = "61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0"
SOURCE_REVISIONS = {TREE: "0.4.0-rc.6", RC7_TREE: "0.4.0-rc.7"}
SOURCE_CERT = Path(__file__).resolve().parents[1] / "docs/evidence/1020-migration-rc7-source/source-certificate-v1.json"
SOURCE_CERT_SHA = "29742bf394cf83d0b1fd3b9f8221bf06f0c359b40668afea30e3aaa82a946046"
OLD_TOOL = "681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc"
OLD_TREE = "abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8"
MODE = "single_player_postload_layout_repair"
POLICY = {"step_signed_ratio_min": -0.000021, "step_signed_ratio_max": 0.000001,
          "v1_absolute_tolerance": 0.000001, "relative_tolerance": 0}
DEFENSES = {"hull": ("hitpoints", "max_hitpoints"),
            "armor": ("armor_hitpoints", "max_armor_hitpoints"),
            "shield": ("shield_hitpoints", "max_shield_hitpoints")}
ARTIFACTS = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts")
FIXTURES = {
    "public031": {
        "fixture_source": str(ARTIFACTS / "single-homeworld-20261019/runs/20261019T053917Z/bmm00.sav"),
        "fixture_sha256": "af5f64e2eaadb164e87796d2a9261ac97ef7d716cc3f8b3cec5f4a2f23f787f8",
        "before_name": "p031before", "before_sha256": "d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2",
        "expected_fleet_id": 128, "expected_ship_id": 1008, "expected_starbase_id": 15,
        "expected_shipyard_queue_id": 50, "queue_mode": "empty", "expected_queued_items": 0,
    },
    "paid11": {
        "fixture_source": str(ARTIFACTS / "1015-implementation/runs/20261014T223819Z/j13ten.sav"),
        "fixture_sha256": "834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e",
        "before_name": "ppaidbefore", "before_sha256": "40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1",
        "expected_fleet_id": 146, "expected_ship_id": 822, "expected_starbase_id": 13,
        "expected_shipyard_queue_id": 54, "queue_mode": "paid", "expected_queued_items": 11,
    },
}


def number(value, label):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("missing/nonfinite native numeric value: " + label)
    return Decimal(str(value))


def template(kind, candidate_tree=TREE):
    if candidate_tree not in SOURCE_REVISIONS:
        raise ValueError("unreviewed candidate source tree")
    known = FIXTURES[kind]
    return {"schema": SCHEMA, "status": "PENDING", "fixture_kind": kind,
            "execution_mode": MODE, "policy": dict(POLICY),
            **{k: v for k, v in known.items() if k != "before_name"},
            "before": str(ARTIFACTS / "1019-legacy-damage/runs/20261019T130448Z" /
                          (known["before_name"] + ".sav")),
            "after": None, "reload": None, "after_load_receipt": None,
            "reload_load_receipt": None, "repeat_before": None, "repeat_after": None,
            "repeat_load_source": None, "repeat_before_load_receipt": None,
            "contract": "native-migration-roundoff-contract-1019.md",
            "candidate_tree_sha256": candidate_tree, "game_exe_sha256": EXE}


def validate_case(case):
    if case.get("schema") != SCHEMA or case.get("execution_mode") != MODE:
        raise ValueError("explicit v2 schema and single-player postload repair mode required")
    kind = case.get("fixture_kind")
    if kind not in FIXTURES:
        raise ValueError("only the two independently bound genuine old fixtures are supported")
    policy = case.get("policy")
    if not isinstance(policy, dict) or set(policy) != set(POLICY) or any(
            number(policy[k], "policy." + k) != Decimal(str(v)) for k, v in POLICY.items()):
        raise ValueError("the predeclared policy cannot be missing, replaced or enlarged")
    for key, expected in FIXTURES[kind].items():
        if key not in ("before_name", "fixture_source") and case.get(key) != expected:
            raise ValueError("fixed fixture binding mismatch: " + key)
    if case.get("candidate_tree_sha256") not in SOURCE_REVISIONS or case.get("game_exe_sha256") != EXE:
        raise ValueError("fixed reviewed tree/EXE binding required")
    return FIXTURES[kind]


def source_certificate():
    if v1.n.digest(SOURCE_CERT) != SOURCE_CERT_SHA:
        raise ValueError("reviewed migration source certificate changed")
    certificate = json.loads(SOURCE_CERT.read_text(encoding="utf-8"))
    if (certificate.get("schema") != "eep.migration.reviewed_source_revisions.v1"
            or set(certificate.get("revisions", {})) != set(SOURCE_REVISIONS)
            or any(certificate["revisions"][tree].get("version") != version
                   for tree, version in SOURCE_REVISIONS.items())):
        raise ValueError("source certificate does not match the reviewed revision registry")
    return certificate


def validate_candidate_source(manifest, expected_tree):
    """Bind all copied bytes to an independently pinned complete source index."""
    if expected_tree not in SOURCE_REVISIONS:
        raise ValueError("unreviewed candidate source tree")
    certificate = source_certificate()
    revision = certificate["revisions"][expected_tree]
    mod, actual, tree = Path(manifest["copied_mod"]), [], hashlib.sha256()
    for path in sorted(p for p in mod.rglob("*") if p.is_file()):
        raw, relative = path.read_bytes(), path.relative_to(mod).as_posix()
        actual.append({"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        tree.update(relative.encode("utf-8")); tree.update(b"\0"); tree.update(raw)
    gate = manifest["static_gate"]
    if (len(actual) != 59 or actual != revision["files"] or tree.hexdigest() != expected_tree
            or actual != sorted(manifest["repository_mod_files"], key=lambda row: row["path"])
            or actual != sorted(gate["files"], key=lambda row: row["path"])
            or manifest["copied_mod_tree_sha256"] != expected_tree
            or manifest["repository_mod_tree_sha256"] != expected_tree
            or gate.get("source_tree_sha256") != expected_tree
            or gate.get("version") != revision["version"] or gate.get("status") != "PASS"):
        raise ValueError("candidate bytes differ from the complete reviewed source revision")
    versions = [v1.a.unquote(raw) for key, raw, obj in v1.a.fields(
        (mod / "descriptor.mod").read_text(encoding="utf-8-sig")) if key == "version" and not obj]
    if versions != [revision["version"]]:
        raise ValueError("candidate descriptor differs from reviewed version")
    report = Path(gate["report"])
    if v1.n.digest(report) != gate["report_sha256"] or json.loads(report.read_text(encoding="utf-8")).get("status") != "PASS":
        raise ValueError("original static report binding differs")
    shared = certificate["shared_migration_sources"]
    if v1.n.digest(mod / shared["design"]["path"]) != shared["design"]["sha256"]:
        raise ValueError("shared migration design bytes changed")
    helper = shared["layout_repair_helper"]
    body = v1.a.block((mod / helper["path"]).read_text(encoding="utf-8-sig"), helper["key"])
    if hashlib.sha256(body.encode("utf-8")).hexdigest() != helper["body_sha256"]:
        raise ValueError("shared migration guard helper changed")
    return {"schema": "eep.migration.candidate_source_identity.v1", "tree_sha256": expected_tree,
            "version": revision["version"], "file_count": 59, "files": actual, "copied_mod": str(mod),
            "source_certificate": {"path": str(SOURCE_CERT), "sha256": SOURCE_CERT_SHA},
            "shared_migration_sources": shared}


def load_receipt(path, source):
    receipt_path = Path(path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    source_path = Path(receipt["source"])
    return {"path": str(receipt_path), "sha256": v1.n.digest(receipt_path),
            "raw": receipt, "source_byte_sha256": v1.n.digest(source_path),
            "expected_source_sha256": source["save_sha256"]}


def native_players(raw):
    """Native player is a list of unnamed records, not a named-field map."""
    players = []
    for key, body, block in v1.a.fields(raw):
        if key != "player":
            continue
        if not block:
            raise ValueError("native player must be an anonymous-record list")
        iterator = iter(v1.a.tokens(body))
        for token, _, end in iterator:
            if token != "{":
                raise ValueError("unexpected native player list token")
            start, depth, stop = end, 1, None
            for nested, position, _ in iterator:
                if nested == "{":
                    depth += 1
                elif nested == "}":
                    depth -= 1
                    if not depth:
                        stop = position
                        break
            if stop is None:
                raise ValueError("unclosed native player record")
            players.append(v1.a.scalars(body[start:stop]))
    return players


def load_native(path):
    observation = v1.n.observe(Path(path))
    manifest = json.loads(Path(observation["manifest"]).read_text(encoding="utf-8"))
    with zipfile.ZipFile(path) as archive:
        raw = archive.read("gamestate").decode("utf-8-sig")
    players = native_players(raw)
    definition = v1.mod_definition(observation, "common/global_ship_designs/eep_mothership.txt", "ship_design")
    snapshot = v1.migration_snapshot(observation)
    base = observation["starbases_1019"][snapshot["starbase_id"]]
    observation["migration_v2_native"] = {
        "manifest_game_exe_sha256": manifest["game_exe_sha256"],
        "actual_game_exe_sha256": v1.n.digest(Path(manifest["game_exe"])),
        "players": players, "definition": definition,
        "expected_design_shape": v1.design_shape(v1.n.design(definition["body"])),
        "attached_starbase_raw": base["raw"],
        "attached_starbase_implementation": v1.a.scalars(v1.a.block(base["raw"], "ship_design_implementation")),
        "candidate_source_identity": validate_candidate_source(manifest, observation["production_tree_sha256"])
            if observation["production_tree_sha256"] in SOURCE_REVISIONS else None,
    }
    return observation


def mother_ship(observation):
    snapshot = v1.migration_snapshot(observation)
    return observation["fleets_1019"][snapshot["fleet_id"]]["ships"][snapshot["ship_id"]]


def defense(observation):
    native = mother_ship(observation)["native"]
    values = {}
    for layer, (current, maximum) in DEFENSES.items():
        now, limit = number(native.get(current), current), number(native.get(maximum), maximum)
        if limit <= 0 or now < 0 or now > limit:
            raise ValueError("illegal native current/maximum defense: " + layer)
        values[layer] = {"current": native[current], "maximum": native[maximum],
                         "fraction_decimal": str(now / limit)}
    return values


def ratio_step(before, after):
    readings = {"before": defense(before), "after": defense(after)}
    checks, deltas, old_diagnostic = {}, {}, {}
    for layer in DEFENSES:
        delta = (Decimal(readings["after"][layer]["fraction_decimal"]) -
                 Decimal(readings["before"][layer]["fraction_decimal"]))
        deltas[layer] = str(delta)
        checks[layer + "_signed_ratio_in_predeclared_budget"] = (
            Decimal("-0.000021") <= delta <= Decimal("0.000001"))
        old_diagnostic[layer] = abs(delta) <= Decimal("0.000001")
    return {"checks": checks, "signed_ratio_deltas_decimal": deltas,
            "original_1e_6_diagnostic": old_diagnostic, "raw_readings": readings,
            "minimum_delta": "-0.000021", "maximum_delta": "0.000001"}


def no_precision_snapshot(snapshot):
    return {key: value for key, value in snapshot.items() if key not in ("design_id", "damage")}


def ordinary_ships(observation, mother_id):
    return {sid: {"name": ship["name"], "native": ship["native"],
                  "shape": v1.design_shape(ship["design"]), "coordinate": ship["coordinate"],
                  "target_coordinate": ship["target_coordinate"], "variables": ship["variables"],
                  "flags": ship["flags"], "timed_modifier": ship["timed_modifier"]}
            for fleet in observation["fleets_1019"].values() for sid, ship in fleet["ships"].items()
            if sid != mother_id}


def context_checks(before, after):
    bs, ass = v1.migration_snapshot(before), v1.migration_snapshot(after)
    return {
        "same_date": before["date"] == after["date"],
        "all_population_jobs_colonies_worlds_zones_preserved": all(
            before[k] == after[k] for k in ("pop_groups", "pop_jobs", "colonies", "worlds", "zones", "districts")),
        "all_stockpiles_preserved": all(before["country"][k] == after["country"][k]
            for k in ("stockpile", "research_stockpile", "effective_stockpile")),
        "all_country_variables_preserved": before["country_variables_all"] == after["country_variables_all"],
        "all_audit_country_variables_preserved": before["country"]["variables"] == after["country"]["variables"],
        "all_country_flags_preserved": before["country"]["flags"] == after["country"]["flags"],
        "all_queues_payment_progress_civilian_items_preserved": all(bs[k] == ass[k]
            for k in ("all_owned_queues", "all_owned_queue_items")),
        "all_queued_design_names_preserved": {
            key: item["queued_ship_design"]["name"] if item["queued_ship_design"] else None
            for key, item in before["construction_items_1019"].items()} == {
            key: item["queued_ship_design"]["name"] if item["queued_ship_design"] else None
            for key, item in after["construction_items_1019"].items()},
        "all_ordinary_ship_states_and_shapes_preserved": ordinary_ships(before, bs["ship_id"]) == ordinary_ships(after, ass["ship_id"]),
    }


def source_checks(observation, candidate, expected_tree=TREE):
    proof = observation["migration_v2_native"]
    players = proof["players"]
    checks = {"fixed_manifest_exe": proof["manifest_game_exe_sha256"] == EXE,
              "fixed_actual_exe": proof["actual_game_exe_sha256"] == EXE,
              "single_root_player_country0": len(players) == 1 and type(players[0].get("country")) is int and players[0]["country"] == 0,
              "simplified_chinese": observation["language"] == "l_simp_chinese",
              "attached_starbase_raw_implementation_recorded": bool(proof["attached_starbase_raw"]) and
                  type(proof["attached_starbase_implementation"].get("design")) is int}
    if candidate:
        certificate = source_certificate()
        identity = proof.get("candidate_source_identity") or {}
        revision = certificate["revisions"].get(expected_tree, {})
        # Retain serialized v2 check names for the historical 174/158 checksets.
        checks["fixed_rc6_tree"] = (expected_tree in SOURCE_REVISIONS
            and observation["production_tree_sha256"] == expected_tree
            and identity.get("schema") == "eep.migration.candidate_source_identity.v1"
            and identity.get("tree_sha256") == expected_tree and identity.get("file_count") == 59
            and identity.get("files") == revision.get("files")
            and identity.get("source_certificate", {}).get("sha256") == SOURCE_CERT_SHA
            and identity.get("shared_migration_sources") == certificate["shared_migration_sources"])
        checks["fixed_rc6_version"] = (observation["provenance_1019"]["version"] == SOURCE_REVISIONS.get(expected_tree)
            and identity.get("version") == SOURCE_REVISIONS.get(expected_tree))
    return checks


def layout_checks(observation, before):
    ship = mother_ship(observation)
    shape = v1.design_shape(ship["design"])
    proof = observation["migration_v2_native"]
    if not proof.get("definition", {}).get("body") or not proof.get("expected_design_shape"):
        raise ValueError("missing independently verified frozen native design definition")
    components = [c for stage in shape for section in stage["sections"] for c in section["components"]]
    readings, old = defense(observation), defense(before)
    return {"actual_new_design_name": ship["design"]["name"] == v1.DESIGN_NAME,
            "entire_actual_layout_matches_frozen_source": shape == proof["expected_design_shape"],
            "fifty_actual_slots": len(components) == 50,
            "six_actual_required_components": sum(len(s["required_components"]) for s in shape) == 6,
            "six_real_core_slots": all({"slot": "AUX_UTILITY_" + str(i + 6),
                "template": "EEP_ADAPTIVE_" + kind.upper() + "_CORE"} in components
                for i, kind in enumerate(v1.CORE_TYPES)),
            "existing_hull_maximum_preserved": readings["hull"]["maximum"] == old["hull"]["maximum"],
            "source_bound_c0_armor_maximum": readings["armor"]["maximum"] == 44787.6,
            "source_bound_c0_shield_maximum": readings["shield"]["maximum"] == 167310}


def receipt_checks(proof, source, destination):
    receipt = proof["raw"]
    return {"actual_native_load_ui_date_verified": receipt.get("ui_date_verified") is True,
            "actual_native_load_correct_source_sha": receipt.get("source_sha256") == source["save_sha256"] == proof["source_byte_sha256"],
            "actual_native_load_correct_date": receipt.get("date") == source["date"] == destination["date"],
            "actual_native_load_timestamp_recorded": isinstance(receipt.get("loaded_at_utc"), str) and bool(receipt["loaded_at_utc"])}


def evaluate(case, fixture, before, after, reload_observation, repeat_before=None, repeat_after=None):
    known = validate_case(case)
    if v1.n.digest(Path(v1.__file__)) != OLD_TOOL:
        raise ValueError("original v1 checker fingerprint changed")
    observations = {"fixture": fixture, "before": before, "after": after, "reload": reload_observation}
    for observation in observations.values():
        defense(observation)
    old_case = {**case, "schema": "eep.1019.migration-case.v1", "require_damaged_before": True,
                "damage_mode": "fraction", "damage_metrics": list(DEFENSES), "damage_tolerance": 0.000001}
    legacy = v1.migration(old_case, before, after, reload_observation, fixture)
    checks = {"fixture_sha_binding": fixture["save_sha256"] == known["fixture_sha256"],
              "genuine_partial_old_before_sha_binding": before["save_sha256"] == known["before_sha256"],
              "genuine_public031_before_tree": before["production_tree_sha256"] == OLD_TREE,
              "genuine_public031_before_version": before["provenance_1019"]["version"] == "0.3.1",
              "all_three_old_layers_genuinely_partial": all(0 < x["current"] < x["maximum"] for x in defense(before).values())}
    # Preserve the legacy result as returned. Only two v2 replacement contracts
    # are evaluated independently below; legacy FAIL/booleans are never edited.
    for key, value in legacy["checks"].items():
        if key not in ("damage_preserved_in_declared_mode", "reload_migration_snapshot_preserved"):
            checks["v1_nonprecision." + key] = value
    for name, observation in observations.items():
        checks.update({name + "." + k: v for k, v in source_checks(
            observation, name in ("after", "reload"), case["candidate_tree_sha256"]).items()})
    for name, observation, source in (("after", after, before), ("reload", reload_observation, after)):
        checks.update({name + "." + k: v for k, v in layout_checks(observation, before).items()})
        checks.update({name + "." + k: v for k, v in context_checks(before, observation).items()})
        checks.update({name + "." + k: v for k, v in receipt_checks(observation["migration_v2_native"]["load_evidence"], source, observation).items()})
    steps = {"old_to_after": ratio_step(before, after), "after_to_reload": ratio_step(after, reload_observation)}
    for name, step in steps.items():
        checks.update({name + "." + k: v for k, v in step["checks"].items()})
    a, r = v1.migration_snapshot(after), v1.migration_snapshot(reload_observation)
    checks["reload_snapshot_exact_except_design_index_and_defenses"] = no_precision_snapshot(a) == no_precision_snapshot(r)
    checks["reload_all_maximum_defenses_exact"] = all(a["damage"][k]["maximum"] == r["damage"][k]["maximum"] for k in DEFENSES)
    checks["reload_mother_flags_and_variables_exact"] = all(mother_ship(after)[k] == mother_ship(reload_observation)[k] for k in ("flags", "variables", "timed_modifier"))
    checks["reload_fleet_variables_and_modifiers_exact"] = all(after["fleets_1019"][a["fleet_id"]][k] == reload_observation["fleets_1019"][r["fleet_id"]][k] for k in ("variables", "timed_modifier"))
    present = repeat_before is not None and repeat_after is not None
    checks["repeat_sync_samples_present"] = present
    repeat_report = None
    repeat_load_report = None
    if (repeat_before is None) != (repeat_after is None):
        raise ValueError("repeat sync requires both actual native SAVs")
    if present:
        extra_source = case.get("repeat_load_source")
        if extra_source is None:
            checks["repeat_sync_before_is_actual_reload_save"] = repeat_before["save_sha256"] == reload_observation["save_sha256"]
            checks["repeat_sync_starts_from_exact_reloaded_snapshot"] = v1.migration_snapshot(repeat_before) == r
        elif extra_source in ("after", "reload"):
            source = observations[extra_source]
            extra_snapshot = v1.migration_snapshot(repeat_before)
            source_snapshot = v1.migration_snapshot(source)
            steps["extra_native_load_before_repeat"] = ratio_step(source, repeat_before)
            checks.update({"extra_repeat_load." + k: v for k, v in steps["extra_native_load_before_repeat"]["checks"].items()})
            checks.update({"extra_repeat_load." + k: v for k, v in context_checks(source, repeat_before).items()})
            checks.update({"extra_repeat_load." + k: v for k, v in receipt_checks(repeat_before["migration_v2_native"]["load_evidence"], source, repeat_before).items()})
            checks["extra_repeat_load.snapshot_except_index_and_defenses_preserved"] = no_precision_snapshot(source_snapshot) == no_precision_snapshot(extra_snapshot)
            repeat_load_report = v1.compare(source, repeat_before)
        else:
            raise ValueError("repeat_load_source must be after, reload or null")
        checks["repeat_sync_same_date_as_reload"] = repeat_before["date"] == reload_observation["date"]
        for name, observation in (("repeat_before", repeat_before), ("repeat_after", repeat_after)):
            defense(observation)
            checks.update({name + "." + k: v for k, v in source_checks(
                observation, True, case["candidate_tree_sha256"]).items()})
            checks.update({name + "." + k: v for k, v in layout_checks(observation, before).items()})
            for key in ("pop_groups", "pop_jobs", "colonies", "worlds"):
                checks[name + "." + key + "_preserved"] = observation[key] == before[key]
            checks[name + ".economic_ledger_preserved"] = all(observation["country"]["variables"][k] == before["country"]["variables"][k] for k in v1.ECONOMIC_VARIABLES)
            checks[name + ".all_stockpiles_preserved"] = all(observation["country"][k] == before["country"][k]
                for k in ("stockpile", "research_stockpile", "effective_stockpile"))
        repeat_report = v1.compare(repeat_before, repeat_after)
        checks["repeat_sync_strict_zero_differences"] = not repeat_report["differences"]
        checks["repeat_sync_snapshot_exact"] = v1.migration_snapshot(repeat_before) == v1.migration_snapshot(repeat_after)
    required_ok = all(v for k, v in checks.items() if k != "repeat_sync_samples_present")
    status = "PASS_SCOPED" if required_ok and present else "PENDING" if required_ok else "FAIL"
    return {"schema": "eep.1019.migration-report.v2", "status": status,
            "scope": "Exact EXE/reviewed-source single-player postload layout repair, fixed genuine damaged fixture, step-local asymmetric engineering budget, exact nonprecision invariants and exact repeated sync only.",
            "candidate_source_identity": after["migration_v2_native"].get("candidate_source_identity"),
            "checks": checks, "case": copy.deepcopy(case), "policy": dict(POLICY),
            "policy_classification": "Predeclared engineering budget, not a universal engine precision guarantee.",
            "steps": steps, "v1_original_diagnostic": legacy,
            "native_sources": {k: o["migration_v2_native"] for k, o in observations.items()},
            "snapshots": {k: v1.migration_snapshot(o) for k, o in observations.items()},
            "provenance": {k: o["provenance_1019"] for k, o in observations.items()},
            "strict_comparisons": {"old_to_after": v1.compare(before, after), "after_to_reload": v1.compare(after, reload_observation), "old_to_reload": v1.compare(before, reload_observation)},
            "repeat_sync_strict_comparison": repeat_report,
            "extra_native_load_before_repeat_strict_comparison": repeat_load_report,
            "repeat_native_sources": None if not present else {
                name: {"native": state["migration_v2_native"], "provenance": state["provenance_1019"],
                       "snapshot": v1.migration_snapshot(state)}
                for name, state in (("before", repeat_before), ("after", repeat_after))},
            "v1_checker_sha256": OLD_TOOL,
            "limitations": ["All original v1 FAILs remain unchanged; v2 is not a v1 pass.",
                "The associated mobile-starbase implementation is reported raw, not certified updated.",
                "Root-player count plus declared single-player UI load provenance does not assert a hidden multiplayer boolean.",
                "Repeated native loads can incur bounded tiny damage losses; this is not mathematically lossless migration."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("template")
    prepare.add_argument("fixture_kind", choices=FIXTURES)
    prepare.add_argument("--candidate-tree", choices=SOURCE_REVISIONS, default=TREE)
    sub.add_parser("check").add_argument("case", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("refusing to overwrite existing evidence: " + str(args.output))
    try:
        if args.command == "template":
            report = template(args.fixture_kind, args.candidate_tree)
        else:
            case = json.loads(args.case.read_text(encoding="utf-8"))
            validate_case(case)
            required = ("fixture_source", "before", "after", "reload", "after_load_receipt", "reload_load_receipt")
            if any(not isinstance(case.get(k), str) or not case[k] for k in required):
                raise ValueError("PENDING template: four native saves and both actual load receipts required")
            states = {k: load_native(case[k]) for k in ("before", "after", "reload")}
            fixture = load_native(case["fixture_source"])
            states["after"]["migration_v2_native"]["load_evidence"] = load_receipt(case["after_load_receipt"], states["before"])
            states["reload"]["migration_v2_native"]["load_evidence"] = load_receipt(case["reload_load_receipt"], states["after"])
            repeats = [load_native(case[k]) if case.get(k) else None for k in ("repeat_before", "repeat_after")]
            if case.get("repeat_load_source") is not None:
                source_key = case["repeat_load_source"]
                if source_key not in ("after", "reload") or repeats[0] is None or not case.get("repeat_before_load_receipt"):
                    raise ValueError("an extra repeat load requires a supported source, native before and actual load receipt")
                repeats[0]["migration_v2_native"]["load_evidence"] = load_receipt(case["repeat_before_load_receipt"], states[source_key])
            report = evaluate(case, fixture, states["before"], states["after"], states["reload"], *repeats)
            report["case_sha256"] = v1.n.digest(args.case)
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation, zipfile.BadZipFile) as error:
        report = {"schema": "eep.1019.migration-report.v2", "status": "FAIL",
                  "scope": "v2 native evidence/contract prerequisite", "error_type": type(error).__name__, "error": str(error)}
    report["checker_sha256"] = v1.n.digest(Path(__file__))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": report["status"], "output": str(args.output), "error": report.get("error")}, ensure_ascii=False))
    return 0 if report["status"] == "PASS_SCOPED" or args.command == "template" else 2 if report["status"] == "PENDING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
