"""Prove the one native planet right-click did not change game state."""
import json
import logging
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "terravore-kira39-vermilion-rightclick-guard-22890511"
assert not list(run.glob(stage + "*"))
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
before = "terravore-kira39-transit-day02-native-22890511"
after = "terravore-kira39-vermilion-rightclick-native-22890511"
b, a = (read_state(run, name) for name in (before, after))
arrival = load("terravore-kira39-system-arrival-guard-22890511-proof.json")
right = load("terravore-kira39-vermilion-scout-rightclick-22890511-execution.json")
input_action = load("terravore-kira39-vermilion-scout-rightclick-22890511.action.json")
capture = load("terravore-kira39-vermilion-scout-context-22890511-observation.json")
saved = load(after + "-observation.json")
save_exec = load(after + "-execution.json")
fleet = a["fleets"]["166"]
current = re.findall(r"\bid=(\d+)", q.block(fleet, "current_order"))
queued = re.findall(r"\bid=(\d+)", q.block(fleet, "order"))
checks = {
    "real_arrival_before_rightclick_sav_chain":
        arrival["status"] == "PASS_NATIVE_KIRA39_SCIENCE_SHIP_SYSTEM_ARRIVAL"
        and all(arrival["checks"].values())
        and arrival["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and b["audit"]["date"] == a["audit"]["date"] == "2289.05.11",
    "one_native_rightclick_capture_and_same_day_save_actual0":
        right["returncode"] == save_exec["returncode"] == 0
        and right["helper_sha256"] == h.sha256(Path(right["command"][1]))
        and save_exec["helper_sha256"] == h.sha256(Path(save_exec["command"][1]))
        and input_action["action"] == "right-click"
        and input_action["client_point"] == [596, 414]
        and capture["status"] == "PASS_READ_ONLY_PAUSED_NATIVE_CAPTURE"
        and all(capture["checks"].values())
        and saved["status"] == "OBSERVED_SAME_DAY_NATIVE_SAVE_AFTER_AMBIGUOUS_RIGHTCLICK"
        and saved["save_sha256"] == a["audit"]["save_sha256"],
    "all_native_gamestate_root_objects_byte_identical":
        b["roots"] == a["roots"],
    "full_survey_queue_including_ninth_vermilion_stable":
        current == ["550"]
        and queued == ["555", "554", "549", "548", "547", "553", "552",
                       "545", "544", "546", "543", "551"]
        and q.block(b["fleets"]["166"], "current_order")
            == q.block(fleet, "current_order")
        and q.block(b["fleets"]["166"], "order") == q.block(fleet, "order"),
    "no_new_error_cash_eep_fleet_or_ship":
        saved["error_unchanged"]
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
        and b["audit"]["countries"]["0"]["effective_stockpile"]
            == a["audit"]["countries"]["0"]["effective_stockpile"]
        and b["audit"]["countries"]["0"]["variables"]
            == a["audit"]["countries"]["0"]["variables"]
        and set(b["ships"]) == set(a["ships"])
        and set(b["fleets"]) == set(a["fleets"]),
}
proof = {
    "status": "PASS_NATIVE_RIGHTCLICK_NO_ORDER_CHANGE" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "current_target": current,
    "queued_targets": queued,
    "scope": "One native right-click changed no parsed game state; no survey or colony acceptance.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
