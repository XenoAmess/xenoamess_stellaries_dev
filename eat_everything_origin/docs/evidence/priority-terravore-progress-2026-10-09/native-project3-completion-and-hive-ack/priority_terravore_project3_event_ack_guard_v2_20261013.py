"""Supplement the original ACK guard with the correct Queen-stage variable."""
import json
import logging
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "eat_everything_origin/tools")
sys.path.insert(0, "_runtime/heart-of-devouring")
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-project3-completion-22880902"
after = "terravore-project3-crisis4130-ack-22880902"
old, new = (read_state(run, stage) for stage in (before, after))
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
prior = load(before + "-project3-completion-proof.json")
prior_run = load(before + "-guard-execution.json")
click_run = load(after + "-click-execution.json")
v1 = load(after + "-event-ack-proof.json")
v1_run = load(after + "-guard-execution.json")
pre = load(after + "-pre-click.ocr.json")
post = load(after + "-post-click.ocr.json")
source = h.GAME_EXE.parent / "events" / "nemesis_crisis_events.txt"
event = [v for k, v, obj in q.fields(source.read_text("utf-8-sig"))
         if obj and q.scalars(v).get("id") == "crisis.4130"]
options = [v for k, v, obj in q.fields(event[0]) if k == "option" and obj] if len(event) == 1 else []
after_effect = [v for k, v, obj in q.fields(event[0]) if k == "after" and obj] if len(event) == 1 else []
history = lambda state: [q.scalars(v) for v in re.findall(
    r"\{([^{}]*)\}", state["roots"]["open_player_event_selection_history"])]
old_history, new_history = history(old), history(new)
removed_message = [v for v in old["messages"] if q.scalars(v).get("event") == 305]
metadata = {"save", "save_sha256", "gamestate_sha256", "gamestate_bytes"}
changed_roots = {key for key in old["roots"] | new["roots"]
                 if old["roots"].get(key) != new["roots"].get(key)}
pre_rows, post_rows = pre["rows"], post["rows"]
has_row = lambda rows, label: any(v["text"] == label and v["score"] >= .8 for v in rows)
checks = {
    "original_V1_exact_single_false_preserved_with_source_and_SAV":
        v1["status"] == "FAIL"
        and len(v1["checks"]) == 9
        and [key for key, value in v1["checks"].items() if value is not True]
            == ["crisis_still3_Queen_stage2_Menace3065"]
        and v1_run["returncode"] == 1
        and v1_run["helper_sha256"] == h.sha256(Path(v1_run["command"][1]))
        and v1["before_sha256"] == old["audit"]["save_sha256"]
        and v1["after_sha256"] == new["audit"]["save_sha256"],
    "original_completion_guard_7PASS_source_and_SAV_bound":
        prior["status"] == "PASS_NATIVE_PROJECT3_COMPLETED_EVENT_PENDING"
        and len(prior["checks"]) == 7 and all(v is True for v in prior["checks"].values())
        and prior_run["returncode"] == 0
        and prior_run["helper_sha256"] == h.sha256(Path(prior_run["command"][1]))
        and prior["after_sha256"] == old["audit"]["save_sha256"]
        and old["audit"]["save_sha256"] == h.sha256(run / (before + ".sav")),
    "normal_click_once_and_native_save_actual0_same_paused_date":
        click_run["returncode"] == 0
        and click_run["helper_sha256"] == h.sha256(Path(click_run["command"][1]))
        and (run / (after + "-option3-normal.action.json")).exists()
        and (run / (after + ".native-save.json")).exists()
        and new["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and old["audit"]["date"] == new["audit"]["date"] == "2288.09.02",
    "Chinese_UI_exact_event_date_option_and_post_click_closed":
        meta["language"] == "l_simp_chinese"
        and all(has_row(pre_rows, label) for label in
                ["2288.09.02", "暂停", "异界注能", "此举必为正道。"])
        and sum(v["text"] == "此举必为正道。" and v["score"] >= .9 for v in pre_rows) == 1
        and not has_row(post_rows, "此举必为正道。")
        and pre["image_sha256"] == h.sha256(Path(pre["image"]))
        and post["image_sha256"] == h.sha256(Path(post["image"])),
    "original_hive_option3_no_gameplay_effect_and_source_bound":
        h.sha256(source) == "7c037b46e8b6cb8e31dab8dd69bbd34d5902cf212a5fb5c206d175aa676e7d13"
        and len(options) == 4 and q.scalars(options[3]).get("name") == "crisis.4130.hive.a"
        and {k for k, v, obj in q.fields(options[3])} == {"name", "trigger"}
        and len(after_effect) == 1
        and {k for k, v, obj in q.fields(after_effect[0])} == {"custom_tooltip"},
    "only_pending305_and_matching_event_message_consumed":
        len(old["pending"]) == 1
        and q.scalars(old["pending"][0]).get("id") == 305
        and q.scalars(old["pending"][0]).get("event") == "crisis.4130"
        and not new["pending"]
        and len(removed_message) == 1
        and q.scalars(removed_message[0]).get("type") == "EVENT_MESSAGE_TYPE"
        and new["messages"] == [v for v in old["messages"] if v not in removed_message],
    "selection_history_only_original305_human1_option3_added":
        new_history == old_history + [{"player_event": 305, "human": 1, "option": 3}],
    "all_other_raw_roots_and_country_economy_mother_ships_held":
        changed_roots == {"message", "player_event", "open_player_event_selection_history"}
        and old["country"] == new["country"]
        and all(old[key] == new[key] for key in
                ["fleets", "ships", "queues", "items", "designs", "templates"]),
    "all_business_audit_fields_and_original_error_bytes_held":
        all(value == new["audit"].get(key) for key, value in old["audit"].items()
            if key not in metadata)
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "crisis_still3_Queen_stage2_Menace3065":
        [q.unquote(v) for k, v, obj in q.fields(q.block(new["country"], "crisis_progression"))
         if k == "level" and not obj] ==
        ["crisis_level_1", "crisis_level_2", "crisis_level_3"]
        and new["audit"]["countries"]["0"]["variables"]["eep_stage"] == 2
        and old["audit"]["countries"]["0"]["variables"]["eep_stage"] == 2
        and old["audit"]["countries"]["0"]["variables"]["eep_fleet_stage"]
            == new["audit"]["countries"]["0"]["variables"]["eep_fleet_stage"] == 3
        and new["audit"]["countries"]["0"]["effective_stockpile"]["menace"] == 3065,
}
passed = all(value is True for value in checks.values())
out = run / (after + "-event-ack-v2-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_PROJECT3_HIVE_EVENT_ACK" if passed else "FAIL",
    "checks": checks, "before_sha256": old["audit"]["save_sha256"],
    "after_sha256": new["audit"]["save_sha256"], "date": new["audit"]["date"],
    "changed_roots": sorted(changed_roots), "history_added": new_history[len(old_history):],
    "native_source": {"path": str(source), "sha256": h.sha256(source)},
    "boundary": "Menace 1935 still required before native crisis level4; Queen stage3 pending",
    "native_devour_calendar_ready": False, "maximum_days_to_native_bite_boundary": 0,
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]},
                 ensure_ascii=False), flush=True)
assert passed
