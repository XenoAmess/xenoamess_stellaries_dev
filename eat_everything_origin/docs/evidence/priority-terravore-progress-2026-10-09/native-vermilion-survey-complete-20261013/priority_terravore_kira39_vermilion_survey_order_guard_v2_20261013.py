"""Verify one native direct survey order replaced the long Kira queue."""
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
stage = "terravore-kira39-vermilion-survey-order-guard-v2-22890511"
assert not list(run.glob(stage + "*"))
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
before = "terravore-kira39-vermilion-rightclick-native-22890511"
after = "terravore-kira39-vermilion-survey-order-native-22890511"
b, a = (read_state(run, name) for name in (before, after))
previous = load("terravore-kira39-vermilion-rightclick-guard-22890511-proof.json")
menu = load("terravore-kira39-vermilion-body-context-22890511-capture.ocr.json")
click = load("terravore-kira39-vermilion-survey-click-22890511-observation.json")
click_exec = load("terravore-kira39-vermilion-survey-click-22890511-execution.json")
action = load("terravore-kira39-vermilion-survey-click-22890511-click.action.json")
saved = load(after + "-observation.json")
save_exec = load(after + "-execution.json")
old, new = b["fleets"]["166"], a["fleets"]["166"]
old_move, new_move = (q.block(f, "movement_manager") for f in (old, new))
old_queue = re.findall(r"\bid=(\d+)", q.block(old, "order"))
new_queue = re.findall(r"\bid=(\d+)", q.block(new, "order"))
other_fleet_ids = set(b["fleets"]) - {"166"}
changed_fleet_fields = {"movement_manager", "order_id", "current_order", "order"}
checks = {
    "prior_noop_and_original_same_day_native_save_chain":
        previous["status"] == "PASS_NATIVE_RIGHTCLICK_NO_ORDER_CHANGE"
        and all(previous["checks"].values())
        and previous["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and b["audit"]["date"] == a["audit"]["date"] == "2289.05.11",
    "real_chinese_planet_survey_menu_one_click_and_save_actual0":
        menu["image_sha256"] == "a5747dfdddc8447c2414650c56be2cf49c09a3118295e5547fef71fe42e10757"
        and click["status"] == "PASS_NATIVE_PAUSED_CLICK_CAPTURE"
        and all(click["checks"].values())
        and click["client_point"] == [510, 425]
        and action["action"] == "click_point"
        and action["client_point"] == [510, 425]
        and click_exec["returncode"] == save_exec["returncode"] == 0
        and click_exec["helper_sha256"] == h.sha256(Path(click_exec["command"][1]))
        and save_exec["helper_sha256"] == h.sha256(Path(save_exec["command"][1]))
        and saved["status"] == "OBSERVED_ONE_NATIVE_VERMILION_SURVEY_ORDER_SAVED"
        and saved["save_sha256"] == a["audit"]["save_sha256"],
    "full_old_queue_replaced_by_one_reachable_544_survey":
        re.findall(r"\bid=(\d+)", q.block(old, "current_order")) == ["550"]
        and old_queue == ["555", "554", "549", "548", "547", "553", "552",
                          "545", "544", "546", "543", "551"]
        and re.findall(r"\bid=(\d+)", q.block(new, "current_order")) == ["544"]
        and "progress=0" in q.block(new, "current_order")
        and "can_reach=yes" in q.block(new, "current_order")
        and new_queue == []
        and q.scalars(q.block(old_move, "coordinate"))
            == q.scalars(q.block(new_move, "coordinate"))
        and q.scalars(q.block(new_move, "target_coordinate"))
            == {"x": -101.97178, "y": 9.3, "origin": 39},
    "only_original_fleet_order_and_route_changed":
        {k for k in set(b["roots"]) | set(a["roots"])
            if b["roots"].get(k) != a["roots"].get(k)} == {"fleet"}
        and set(b["fleets"]) == set(a["fleets"])
        and all(b["fleets"][k] == a["fleets"][k] for k in other_fleet_ids)
        and [(k, v, obj) for k, v, obj in q.fields(old)
             if k not in changed_fleet_fields]
            == [(k, v, obj) for k, v, obj in q.fields(new)
                if k not in changed_fleet_fields]
        and q.ids(q.block(new, "ships")) == q.ids(q.block(old, "ships")) == [1049],
    "cash_eep_mineral_reinforcement_error_stable":
        b["audit"]["countries"]["0"]["effective_stockpile"]
            == a["audit"]["countries"]["0"]["effective_stockpile"]
        and b["audit"]["countries"]["0"]["variables"]
            == a["audit"]["countries"]["0"]["variables"]
        and a["fleets"]["50331731"] == b["fleets"]["50331731"]
        and set(a["ships"]) == set(b["ships"])
        and a["pending"] == b["pending"] == []
        and a["messages"] == b["messages"] == []
        and saved["error_unchanged"]
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_VERMILION_DIRECT_SURVEY_ORDER" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "current_target": 544,
    "cleared_queue": old_queue,
    "scope": "Direct normal survey of Vermilion ordered. Arrival, survey completion, border and colonization remain separate.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
