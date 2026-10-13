"""Verify the sole vanilla event option without advancing the battle date."""
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
before = "terravore-kira39-battle-day11-native-22881112"
after = "terravore-kira39-shroud1550-ack-native-22881112"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, name) for name in (before, after))
proof = load(before + "-shroud1550-boundary-proof.json")
pre_exec = load(before + "-shroud1550-boundary-guard-execution.json")
action = load(after + "-action-execution.json")
assert pre_exec["helper_sha256"] == h.sha256(Path(pre_exec["command"][1]))
assert action["helper_sha256"] == h.sha256(Path(action["command"][1]))
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
old_tech = q.block(b["country"], "tech_status")
new_tech = q.block(a["country"], "tech_status")
added_lines = [line.strip() for line in new_tech.splitlines()
               if "tech_psionic_aura" in line]
stripped_new = "\n".join(line for line in new_tech.splitlines()
                         if "tech_psionic_aura" not in line)
selection_pattern = re.compile(r"\{\s*player_event=(\d+)\s*human=(\d+)\s*option=(\d+)\s*\}")
old_selected = selection_pattern.findall(
    q.block(b["roots"]["open_player_event_selection_history"], "selected"))
new_selected = selection_pattern.findall(
    q.block(a["roots"]["open_player_event_selection_history"], "selected"))
unchanged_audit = {key: value for key, value in b["audit"].items()
                   if key not in {"save", "save_sha256", "gamestate_sha256",
                                  "gamestate_bytes", "countries"}}
after_audit = {key: value for key, value in a["audit"].items()
               if key not in {"save", "save_sha256", "gamestate_sha256",
                              "gamestate_bytes", "countries"}}
unchanged_country = {key: value for key, value in bc.items()
                     if key not in {"tech_status", "research_progress_by_tech"}}
after_country = {key: value for key, value in ac.items()
                 if key not in {"tech_status", "research_progress_by_tech"}}
checks = {
    "event_boundary_PASS_and_one_normal_action_original_SAV":
        proof["status"] == "PASS_NATIVE_VANILLA_SHROUD1550_EVENT_BOUNDARY"
        and all(v is True for v in proof["checks"].values())
        and pre_exec["returncode"] == action["returncode"] == 0
        and proof["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "same_paused_native_date_and_event_fully_cleared":
        b["audit"]["date"] == a["audit"]["date"] == "2288.11.12"
        and len(b["pending"]) == len(b["messages"]) == 1
        and not a["pending"] and not a["messages"],
    "exactly_one_human_option0_for_event306":
        new_selected == old_selected + [("306", "1", "0")],
    "vanilla_psionic_aura_only_added_tech_progress":
        "tech_psionic_aura" not in bc["research_progress_by_tech"]
        and ac["research_progress_by_tech"]
            == {**bc["research_progress_by_tech"], "tech_psionic_aura": 260}
        and added_lines == ["tech_psionic_aura=260",
                            '"tech_psionic_aura"',
                            'always_available_tech="tech_psionic_aura"']
        and stripped_new.split() == old_tech.split(),
    "all_other_country_and_native_audit_state_unchanged":
        unchanged_country == after_country and unchanged_audit == after_audit,
    "all_other_raw_roots_and_paid_fleet_state_unchanged":
        {key: value for key, value in b["roots"].items()
         if key not in {"country", "open_player_event_selection_history"}}
        == {key: value for key, value in a["roots"].items()
            if key not in {"country", "open_player_event_selection_history"}}
        and b["fleets"] == a["fleets"]
        and b["ships"] == a["ships"]
        and len(a["ships"]) == 74
        and q.scalars(b["items"]["117440553"])["progress"]
            == q.scalars(a["items"]["117440553"])["progress"] == 436.8,
    "only_country_raw_tech_status_changed_and_error_unchanged":
        q.block(b["country"], "flags") == q.block(a["country"], "flags")
        and q.block(b["country"], "events") == q.block(a["country"], "events")
        and q.block(b["country"], "crisis_progression")
            == q.block(a["country"], "crisis_progression")
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "same_CN41_live_production_tree":
        meta["language"] == "l_simp_chinese"
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-shroud1550-option0-ack-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_VANILLA_SHROUD1550_OPTION0_ACK" if passed else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "added_technology_lines": added_lines,
    "selected_history_delta": new_selected[len(old_selected):],
    "boundaries": ["active_kira39_post_loss_single_day_review"],
    "scope": "Single vanilla popup option; continuing battle next day unaccepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]},
                 ensure_ascii=False), flush=True)
assert passed
