"""Audit the vanilla Power of Will popup interrupting the Kira battle."""
import json
import logging
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
before = "terravore-kira39-battle-day10-native-22881111"
after = "terravore-kira39-battle-day11-native-22881112"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, name) for name in (before, after))
prior = load(before + "-kira39-post-loss-active-battle-day-proof-v6.json")
review = load("terravore-kira39-battle-day11-22881112-postloss-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observer = load(after + "-construction-boundary-observation-v4.json")
failed = load(after + "-kira39-post-loss-active-battle-day-proof-v6.json")
receipts = [load(stage + "-execution.json") for stage in [
    before + "-postloss-guard-v6",
    review["execution_stage"],
    after + "-calendar",
    after + "-boundary-observation",
    after + "-postloss-guard-v6",
]]

def valid_source(receipt):
    return receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))

pending = [q.scalars(raw) for raw in a["pending"]]
messages = [q.scalars(raw) for raw in a["messages"]]
old_flags = q.scalars(q.block(b["country"], "flags"))
new_flags = q.scalars(q.block(a["country"], "flags"))
event_file = h.GAME_EXE.parent / "events/shroud_events.txt"
on_actions_file = h.GAME_EXE.parent / "common/on_actions/00_on_actions.txt"
loc_file = h.GAME_EXE.parent / "localisation/simp_chinese/shroud_l_simp_chinese.yml"
events = [raw for key, raw, obj in q.fields(event_file.read_text("utf-8-sig"))
          if key == "country_event" and obj
          and q.scalars(raw).get("id") == "shroud.1550"]
event = events[0] if len(events) == 1 else ""
options = [raw for key, raw, obj in q.fields(event)
           if key == "option" and obj]
event_scalars = q.scalars(event)

checks = {
    "original_previous_PASS_and_11day_one_day_source_chain":
        prior["status"] == "PASS_NATIVE_KIRA39_POST_LOSS_ACTIVE_BATTLE_DAY"
        and all(v is True for v in prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(v is True for v in review["checks"].values())
        and observer["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and all(v is True for v in observer["checks"].values())
        and [x["returncode"] for x in receipts] == [0, 0, 0, 0, 1]
        and all(valid_source(x) for x in receipts)
        and prior["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observer["after_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "original_V6_FAIL_only_message_pending_check_preserved":
        failed["status"] == "FAIL" and len(failed["checks"]) == 12
        and {key for key, value in failed["checks"].items() if value is False}
            == {"no_battle_end_news_pending_or_error"}
        and failed["enemy_killed_original_ship_ids"] == ["1942", "33555262"]
        and failed["menace_delta"] == failed["crisis_objective_delta"] == 30,
    "vanilla_shroud_event_unique_trigger_and_single_option":
        len(events) == len(options) == 1
        and event_scalars["is_triggered_only"] == "yes"
        and event_scalars["title"] == "shroud.1550.title"
        and q.scalars(options[0])["name"] == "shroud.1550.a"
        and "set_country_flag = power_of_will" in q.block(event, "immediate")
        and "tech = tech_psionic_aura" in options[0]
        and "progress = 0.1" in options[0]
        and "shroud.1550" in on_actions_file.read_text("utf-8-sig"),
    "Chinese_original_title_and_option":
        'shroud.1550.title: "意志之力"' in loc_file.read_text("utf-8-sig")
        and 'shroud.1550.a: "很有潜力。"' in loc_file.read_text("utf-8-sig"),
    "one_live_popup_and_corresponding_message":
        len(b["pending"]) == len(b["messages"]) == 0
        and len(pending) == len(messages) == 1
        and pending[0]["id"] == messages[0]["event"] == 306
        and pending[0]["event"] == "shroud.1550"
        and pending[0]["country"] == messages[0]["receiver"] == 0
        and pending[0]["date"] == "2291.02.11"
        and messages[0]["date"] == "2288.11.11"
        and "意志之力" in messages[0]["text"],
    "only_vanilla_new_flag_and_unchanged_EEP":
        "power_of_will" not in old_flags
        and "power_of_will" in new_flags
        and b["audit"]["countries"]["0"]["variables"]
            == a["audit"]["countries"]["0"]["variables"],
    "one_day_battle_rewards_and_production_error_still_valid":
        b["audit"]["date"] == calendar["start_date"] == "2288.11.11"
        and a["audit"]["date"] == calendar["date"] == "2288.11.12"
        and a["audit"]["countries"]["0"]["effective_stockpile"]["menace"] == 3290
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes()
        and meta["language"] == "l_simp_chinese"
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-shroud1550-boundary-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_VANILLA_SHROUD1550_EVENT_BOUNDARY" if passed else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "event_file_sha256": h.sha256(event_file),
    "on_actions_sha256": h.sha256(on_actions_file),
    "localisation_sha256": h.sha256(loc_file),
    "boundaries": ["normal_UI_ack_shroud1550_option0_same_paused_day"],
    "scope": "Vanilla popup boundary only; option click and resumed battle unaccepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True]},
                 ensure_ascii=False), flush=True)
assert passed
