"""Verify the normal July 1 Kira full-system survey order and same-day save."""
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
stage = "terravore-kira39-fullsystem-survey-order-guard-22890701"
assert not list(run.glob(stage + "*"))
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
before = "terravore-kira39-vermilion-survey-july-boundary-native-22890701"
after = "terravore-kira39-fullsystem-survey-order-native-22890701"
b, a = (read_state(run, name) for name in (before, after))
previous = load("terravore-kira39-vermilion-survey-completion-july-budget-guard-22890701-proof.json")
menu = load("terravore-kira39-july01-science-kira-full-survey-menu.ocr.json")
hover = load("terravore-kira39-july01-science-full-survey-menu-second-hover.ocr.json")
post = load("terravore-kira39-july01-science-full-survey-after-click.ocr.json")
action = load("terravore-kira39-july01-science-full-survey-click.action.json")
saved = load(after + "-observation.json")
save_exec = load("terravore-kira39-fullsystem-survey-order-exec-22890701-execution.json")
old, new = b["fleets"]["166"], a["fleets"]["166"]
old_move, new_move = (q.block(f, "movement_manager") for f in (old, new))
old_queue = re.findall(r"\bid=(\d+)", q.block(old, "order"))
new_queue = re.findall(r"\bid=(\d+)", q.block(new, "order"))
current = re.findall(r"\bid=(\d+)", q.block(new, "current_order"))
all_targets = list(map(int, current + new_queue))
other_fleet_ids = set(b["fleets"]) - {"166"}
changed_fleet_fields = {"movement_manager", "order_id", "current_order", "order"}
checks = {
    "prior_544_completion_and_same_day_native_save_chain":
        previous["status"] == "PASS_NATIVE_VERMILION_SURVEY_COMPLETE_JULY_BUDGET"
        and all(previous["checks"].values())
        and previous["after_sha256"] == b["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and b["audit"]["date"] == a["audit"]["date"] == "2289.07.01",
    "chinese_fullsystem_menu_one_click_save_actual0":
        menu["image_sha256"] == h.sha256(run / "terravore-kira39-july01-science-kira-full-survey-menu.jpg")
        == "a7da8d411627a5ebbcefdb7cf57e7aa5a37a88972e65a156de2cb513d39c19db"
        and hover["image_sha256"] == h.sha256(run / "terravore-kira39-july01-science-full-survey-menu-second-hover.jpg")
        == "31cfe0e348d54190c0377f3d030331b81aed543008c75ef4d1bd2cdab74374b6"
        and post["image_sha256"] == h.sha256(run / "terravore-kira39-july01-science-full-survey-after-click.jpg")
        == "1b89c64f382eecd0e84782fd6b753a75a85259fb54d9c4512ecedb5786c9eb4c"
        and action["action"] == "click_point" and action["client_point"] == [550, 435]
        and save_exec["returncode"] == 0
        and save_exec["helper_sha256"] == h.sha256(Path(save_exec["command"][1]))
        and saved["status"] == "OBSERVED_NATIVE_KIRA39_FULLSYSTEM_SURVEY_ORDER_AND_SAVE"
        and saved["after_sha256"] == a["audit"]["save_sha256"],
    "exact_twelve_other_kira_bodies_without_544":
        q.block(old, "current_order").strip() == "" and old_queue == []
        and current == ["546"]
        and new_queue == ["545", "552", "553", "547", "543", "549", "554", "555", "550", "551", "548"]
        and sorted(all_targets) == sorted(set(range(543, 556)) - {544})
        and "progress=0" in q.block(new, "current_order")
        and "can_reach=yes" in q.block(new, "current_order")
        and q.scalars(q.block(old_move, "coordinate")) == q.scalars(q.block(new_move, "coordinate"))
        and q.scalars(q.block(new_move, "target_coordinate"))
        == {"x": -84.2173, "y": 2.69112, "origin": 39},
    "only_original_science_fleet_route_and_order_changed":
        {k for k in set(b["roots"]) | set(a["roots"])
         if b["roots"].get(k) != a["roots"].get(k)} == {"fleet"}
        and set(b["fleets"]) == set(a["fleets"])
        and all(b["fleets"][k] == a["fleets"][k] for k in other_fleet_ids)
        and [(k, v, obj) for k, v, obj in q.fields(old) if k not in changed_fleet_fields]
        == [(k, v, obj) for k, v, obj in q.fields(new) if k not in changed_fleet_fields]
        and q.ids(q.block(new, "ships")) == q.ids(q.block(old, "ships")) == [1049],
    "cash_eep_paid_reinforcement_messages_error_stable":
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
    "status": "PASS_NATIVE_KIRA39_FULLSYSTEM_SURVEY_ORDER" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "current_target": 546,
    "queued_targets": list(map(int, new_queue)),
    "scope": "Twelve remaining Kira bodies queued once; actual travel, full survey completion and outpost require separate native checks.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
