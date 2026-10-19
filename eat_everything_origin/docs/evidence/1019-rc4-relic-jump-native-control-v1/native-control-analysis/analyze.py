"""Read stable RC4 control artifacts only; never read a live log or modify a save."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import sys
import zipfile

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[2]
sys.path.insert(0, str(PROJECT / "tools"))
import audit_save as native

RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
EXPECTED = {"pk2base": "be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2",
            "pk2nativecontrol": "49b3405d5265de6b9b471f778b67a573c521f2988499b6b7c7d4d45b7d6fe208"}
SOURCES = {}


def read(path):
    data = path.read_bytes()
    SOURCES[str(path)] = {"source": str(path), "bytes": len(data), "sha256": sha256(data).hexdigest()}
    return data


def js(name):
    return json.loads(read(RUN / name))


def saves(name):
    path = RUN / (name + ".sav")
    data = read(path)
    assert sha256(data).hexdigest() == EXPECTED[name]
    receipt = js(name + ".native-save.json")
    audit = js(name + ".audit.json")
    assert receipt["sha256"] == audit["save_sha256"] == EXPECTED[name]
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate")
    assert sha256(game).hexdigest() == audit["gamestate_sha256"]
    text = game.decode("utf-8-sig")
    roots = list(native.fields(text))
    selected = {k: v for k, v, obj in roots if obj and k in ("country", "planets", "colony")}
    countries = {k: (v, obj) for k, v, obj in native.fields(selected["country"])}
    colonies = {k: (v, obj) for k, v, obj in native.fields(selected["colony"])}
    planets = {k: (v, obj) for k, v, obj in native.fields(native.block(selected["planets"], "planet"))}
    c0 = countries["0"][0]
    progression = native.block(c0, "crisis_progression")
    objectives = [native.scalars(v) for k, v, obj in native.fields(progression) if k == "objective" and obj]
    country1, country1_obj = countries.get("1", ("ABSENT", False))
    colony1, colony1_obj = colonies.get("1", ("ABSENT", False))
    p17 = planets["17"][0]
    targets = [native.scalars(v) for k, v, obj in roots if k == "saved_event_target" and obj]
    return {"source": str(path), "sha256": EXPECTED[name], "native_date": audit["date"],
            "native_receipt": receipt, "audit_matches_save_and_gamestate": True,
            "event_targets": [x for x in targets if x.get("name") in ("eep_mothership0", "eep_colossus_probe_target")],
            "country0_eep_variables": {k: v for k, v in native.scalars(native.block(c0, "variables")).items() if k.startswith("eep")},
            "country0_eep_flags_raw": {k: v for k, v, obj in native.fields(native.block(c0, "flags")) if k.startswith("eep")},
            "country0_crisis_progression_raw": progression, "country0_crisis_path_and_level": native.scalars(progression),
            "native_objectives": objectives,
            "country1_is_object": country1_obj, "country1_raw_scalar_if_not_object": country1 if not country1_obj else None,
            "colony1_is_object": colony1_obj, "colony1_scalars_if_object": native.scalars(colony1) if colony1_obj else None,
            "colony1_raw_sha256": sha256(colony1.encode("utf-8")).hexdigest(),
            "planet17_is_object": planets["17"][1], "planet17_scalars": native.scalars(p17),
            "planet17_deposits": native.ids(native.block(p17, "deposits")),
            "planet17_eep_variables": {k: v for k, v in native.scalars(native.block(p17, "variables")).items() if k.startswith("eep")},
            "planet17_eep_flags_raw": {k: v for k, v, obj in native.fields(native.block(p17, "flags")) if k.startswith("eep")}}


def records(data):
    rows = []
    for number, line in enumerate(data.decode("utf-8-sig").splitlines(), 1):
        if re.match(r"^\[\d\d:\d\d:\d\d\]", line) or not rows:
            rows.append({"line_start": number, "lines": [line]})
        else:
            rows[-1]["lines"].append(line)
    for row in rows:
        text = row["lines"][0]
        if "nomads_events_1.txt line: 2268" in text and "Invalid context switch [from]" in text:
            category = "nomads_94_invalid_from"
        elif "Could not find files for mod:" in text:
            category = "preexisting_mod_discovery_warning"
        elif "decision_lithoid_swarm_consume_world already exists" in text:
            category = "preexisting_native_decision_override"
        elif "Could not find on action 'on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE'" in text:
            category = "preexisting_missing_dismantle_callback_origin_not_attributed_here"
        else:
            category = "unknown_retained"
        row["category"] = category
    return rows


def objective(state, key):
    entries = [x for x in state["native_objectives"] if x.get("objective") == key]
    assert len(entries) <= 1, entries
    assert state["country0_crisis_path_and_level"]["path"] == "nemesis_path"
    return {"block_present": bool(entries), "progress_if_present": entries[0]["progress"] if entries else None,
            "scoped_value_absent_is_zero_on_confirmed_nemesis_path": entries[0]["progress"] if entries else 0}


def main():
    total = js("pk2nativecontrol-log-receipt.json")
    assert total["status"] == "OBSERVATION_ONLY" and total["state"] == "COLLECTED_NOT_ACCEPTED"
    assert total["native_weapon_firing"] is False and len(total["snapshots"]) == 4
    names = ["B-before-load", "P-before-dispatch", "Q-after-settlement", "R-after-restore"]
    snapshots = []
    previous = None
    baseline = None
    for stage, embedded in zip(names, total["snapshots"]):
        receipt = js("pk2nativecontrol-" + stage + "-log-receipt.json")
        assert receipt == embedded and receipt["stage"] == stage
        assert receipt["active_log_observation"] is True and receipt["final_log_freeze"] is False
        archived = Path(receipt["archived"])
        assert archived.parent == RUN and archived.name == "pk2nativecontrol-" + stage + ".error.log"
        data = read(archived)
        assert len(data) == receipt["bytes"] and sha256(data).hexdigest() == receipt["sha256"]
        snapshot = {"stage": stage, "utc": receipt["utc"], "source_receipt": str(RUN / ("pk2nativecontrol-" + stage + "-log-receipt.json")),
                    "bytes": len(data), "sha256": sha256(data).hexdigest()}
        if previous is None:
            baseline = data
        else:
            assert data[:len(previous)] == previous and receipt["previous_prefix_unchanged"] is True
            delta = data[len(previous):]
            raw_delta = read(RUN / ("pk2nativecontrol-" + stage + ".delta.log"))
            assert delta == raw_delta and receipt["range_start"] == len(previous) and receipt["range_end"] == len(data)
            assert sha256(delta).hexdigest() == receipt["delta_sha256"]
            snapshot.update(range_start=len(previous), range_end=len(data), delta_bytes=len(delta),
                            delta_sha256=sha256(delta).hexdigest(), delta_records=records(delta))
        previous = data
        snapshots.append(snapshot)
    before = saves("pk2base")
    after = saves("pk2nativecontrol")
    target_map = {x["name"]: (x["type"], x["id"]) for x in before["event_targets"]}
    assert target_map == {"eep_mothership0": ("fleet", 159), "eep_colossus_probe_target": ("planet", 17)}
    load = js("pk2nativecontrol-load-base.load.json")
    restore = js("pk2nativecontrol-restore-base.load.json")
    for item in (load, restore):
        assert item["source_sha256"] == EXPECTED["pk2base"] and item["ui_date_verified"] is True
    command = js("pk2nativecontrol-original-cracker-command.action.json")
    ff = js("pk2nativecontrol-settle-two-days-command.action.json")
    assert command["submitted"] is True and ff["submitted"] is True and ff["text"] == "fast_forward 2"
    assert re.sub(r"\s+", "", command["text"]) == re.sub(r"\s+", "", total["command"])
    assert "on_destroy_planet_with_PLANET_KILLER_CRACKER" in command["text"]
    assert "from=event_target:eep_mothership0" in command["text"]
    for name in ("pk2nativecontrol-original-cracker-command-enter.action.json", "pk2nativecontrol-settle-two-days-command-enter.action.json",
                 "pk2nativecontrol-date.wait.json", "pk2nativecontrol-load-base-loaded.ocr.json", "pk2nativecontrol-restore-base-loaded.ocr.json",
                 "manifest.json", "process.json"):
        read(RUN / name)
    read(PROJECT / "tools/audit_save.py")
    native_root = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")
    for name in ("common/on_actions/01_planet_destruction.txt", "events/planet_destruction_events.txt",
                 "events/nemesis_crisis_menace_objective_events.txt", "events/nomads_events_1.txt", "common/on_actions/00_on_actions.txt"):
        read(native_root / name)
    world_before = objective(before, "crisobj_destroy_worlds")
    world_after = objective(after, "crisobj_destroy_worlds")
    empire_before = objective(before, "crisobj_destroy_empires")
    empire_after = objective(after, "crisobj_destroy_empires")
    q = snapshots[2]
    q_nomads = [x for x in q["delta_records"] if x["category"] == "nomads_94_invalid_from"]
    checks = {"all_B_P_Q_R_receipts_and_raw_bytes_hash_match": True,
              "all_three_prefixes_and_delta_files_match_exact_offsets": True,
              "base_native_target_planet17_and_mother_fleet159": True,
              "explicit_original_callback_and_two_day_advance_submitted": True,
              "native_dates_base_Mar7_post_Mar9": before["native_date"] == "2200.03.07" and after["native_date"] == "2200.03.09",
              "physical_planet17_remains_as_shattered_without_owner": after["planet17_is_object"] and after["planet17_scalars"].get("planet_class") == "pc_shattered" and "owner" not in after["planet17_scalars"],
              "country1_native_entry_none": not after["country1_is_object"] and after["country1_raw_scalar_if_not_object"] == "none",
              "historical_colony1_object_remains": after["colony1_is_object"],
              "country0_all_eep_variables_unchanged": before["country0_eep_variables"] == after["country0_eep_variables"],
              "EEP_C_and_worlds_still_zero": after["country0_eep_variables"].get("eep_c") == 0 and after["country0_eep_variables"].get("eep_worlds") == 0,
              "native_worlds_delta_750": world_after["scoped_value_absent_is_zero_on_confirmed_nemesis_path"] - world_before["scoped_value_absent_is_zero_on_confirmed_nemesis_path"] == 750,
              "native_empires_block_absent_before_and_after": not empire_before["block_present"] and not empire_after["block_present"],
              "one_new_nomads_error_in_P_Q_only": len(q_nomads) == 1 and len(q["delta_records"]) == 1 and snapshots[1]["delta_bytes"] == snapshots[3]["delta_bytes"] == 0,
              "restore_load_action_and_ui_date_proven_only": restore["ui_date_verified"] is True and restore["state_verified"] is False}
    report = {"schema": "eep.rc4.native-cracker-control-analysis.v1", "status": "SCOPED_CALLBACK_OBSERVATION_WITH_NATIVE_ERROR_REPRODUCED",
              "analyzed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": RUN.name,
              "source_scope": "Stable saved stage artifacts only; no current/live log read; not a final whole-run log freeze",
              "checks": checks, "checks_all_true": all(checks.values()), "snapshots": snapshots,
              "baseline_records_retained": records(baseline), "baseline_categories": dict(Counter(x["category"] for x in records(baseline))),
              "before": before, "after": after, "native_objectives": {"worlds_before": world_before, "worlds_after": world_after,
                    "empires_before": empire_before, "empires_after": empire_after, "native_empires_delta": 0,
                    "note": "Observed empires block absent, interpreted as zero only on the confirmed Nemesis path. Do not invent or require 600 for this manual callback control."},
              "load_receipt": load, "restore_receipt": restore, "command_receipt": command, "advance_receipt": ff,
              "causal_scope": ["The same native nomads.94 invalid FROM diagnostic is newly present in the exact P-to-Q interval after the original CRACKER completion callback with explicit Mother fleet FROM plus two days.",
                    "The submitted command directly dispatches only the original CRACKER completion callback, not the EEP completion callback; all country0 EEP variables remain at base, including C0 and worlds0.",
                    "Therefore the diagnostic can occur on this native completed-callback path and is not uniquely attributable to the EEP settlement callback.",
                    "No claim about the precise engine hook/ROOT-FROM propagation, harmlessness, or absence of EEP bugs follows from this reproduction.",
                    "This is a manual completed callback, not an actual native weapon shot or 90-day charge test; native rewards/Carrier context/timing may differ. Observed worlds750/empires0 are retained.",
                    "Base restoration has an actual load receipt and verified UI date; state_verified=false remains false, without a new post-restore save audit no complete state-restoration PASS is claimed."],
              "limitations": ["Only error.log stage snapshots were collected; game.log offsets are not present in this control receipt.",
                    "The EEP Mod remains enabled in this run; this is a native-callback control inside the candidate game, not a Mod-free vanilla campaign or a no-callback two-day control.",
                    "Baseline already contains a missing DISMANTLE callback diagnostic and one nomads error; both are retained separately and excluded from the new-interval count only by proven byte offsets.",
                    "No all-fields strict save-difference PASS or zero native-side-effect claim; relevant native state is extracted directly and complete originals are referenced.",
                    "No inference from later r4relic or current log activity; original RC3 22-file payload is untouched."],
              "sources": list(SOURCES.values())}
    (OUT / "analysis.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    assert all(checks.values()), checks
    print(json.dumps({"status": report["status"], "checks_all_true": report["checks_all_true"],
                      "worlds": world_after, "empires": empire_after,
                      "snapshot_sizes": [x["bytes"] for x in snapshots], "sources": len(SOURCES)}, indent=2))


if __name__ == "__main__":
    main()
