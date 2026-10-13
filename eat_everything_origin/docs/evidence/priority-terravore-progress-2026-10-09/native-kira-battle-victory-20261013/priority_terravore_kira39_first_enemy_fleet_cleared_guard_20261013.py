"""Audit the first real enemy fleet disappearing during Kira combat."""
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
before = "terravore-kira39-battle-day12-native-22881113"
after = "terravore-kira39-battle-day13-native-22881114"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, stage) for stage in (before, after))
prior = load(before + "-kira39-post-loss-active-battle-day-proof-v7.json")
review = load("terravore-kira39-battle-day13-22881114-postloss-preflight-v2.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
failed = load(after + "-kira39-post-loss-active-battle-day-proof-v7.json")
receipts = [load(stage + "-execution.json") for stage in [
    before + "-postloss-guard-v7", review["execution_stage"],
    after + "-calendar", after + "-boundary-observation",
    after + "-postloss-guard-v7"]]

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def objectives(s):
    return {q.scalars(raw)["objective"]: q.scalars(raw)["progress"]
            for key, raw, obj in q.fields(q.block(s["country"], "crisis_progression"))
            if key == "objective" and obj}

own = ["83886903", "917", "50332250"]
remaining = "33554515"
removed = "854"
old_removed_fleet = q.block(b["roots"]["fleet"], removed)
new_remaining_fleet = q.block(a["roots"]["fleet"], remaining)
own_ids = {int(i) for i in own}
old_obj, new_obj = objectives(b), objectives(a)
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
checks = {
    "original_PASS_review_observer_and_calendar_source_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_POST_LOSS_ACTIVE_BATTLE_DAY"
        and all(v is True for v in prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and all(v is True for proof in (review, observed)
                for v in proof["checks"].values())
        and [receipt["returncode"] for receipt in receipts] == [0, 0, 0, 0, 1]
        and all(receipt["helper_sha256"]
                == h.sha256(Path(receipt["command"][1])) for receipt in receipts)
        and prior["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "original_double_enemy_guard_FAIL_only_two_expected_checks":
        failed["status"] == "FAIL" and len(failed["checks"]) == 12
        and {key for key, value in failed["checks"].items() if value is False}
            == {"two_hostile_fleets_continue_and_only_real_original_enemy_ships_can_die",
                "three_original_paid_player_fleets_still_in_Kira_combat_and_no_real_extra_fleet"},
    "one_real_day_and_enemy854_ship1943_removed_only":
        b["audit"]["date"] == calendar["start_date"] == "2288.11.13"
        and a["audit"]["date"] == calendar["date"] == "2288.11.14"
        and q.ids(q.block(old_removed_fleet, "ships")) == [1943]
        and not q.block(a["roots"]["fleet"], removed)
        and q.block(b["roots"]["ships"], "1943")
        and not q.block(a["roots"]["ships"], "1943")
        and failed["enemy_killed_original_ship_ids"] == ["1943"],
    "remaining_enemy33554515_one_live_ship39_and_reciprocal_combat":
        q.ids(q.block(q.block(b["roots"]["fleet"], remaining), "ships"))
            == q.ids(q.block(new_remaining_fleet, "ships")) == [33554917]
        and q.scalars(q.block(a["roots"]["ships"], "33554917")).get("killed") != "yes"
        and combat_ids(new_remaining_fleet) == own_ids
        and q.scalars(q.block(q.block(new_remaining_fleet, "movement_manager"),
                              "coordinate"))["origin"] == 39,
    "all74_paid_player_ships_and_three_fleets_continue_single_real_enemy_battle":
        len(b["ships"]) == len(a["ships"]) == 74
        and set(b["ships"]) == set(a["ships"])
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and all(q.ids(q.block(b["fleets"][fid], "ships"))
                == q.ids(q.block(a["fleets"][fid], "ships"))
                and len(q.ids(q.block(a["fleets"][fid], "ships")))
                    == {"83886903": 16, "917": 8, "50332250": 14}[fid]
                and remaining in {str(i) for i in combat_ids(a["fleets"][fid])}
                and all(not q.block(a["roots"]["fleet"], str(i))
                        for i in combat_ids(a["fleets"][fid]) - {int(remaining)})
                and q.scalars(q.block(q.block(a["fleets"][fid],
                                      "movement_manager"), "coordinate"))["origin"] == 39
                for fid in own),
    "one_native_kill_grants15_objective_and_menace":
        new_obj["crisobj_destroy_enemy_ships"]
            - old_obj["crisobj_destroy_enemy_ships"] == 15
        and ac["effective_stockpile"]["menace"]
            - bc["effective_stockpile"]["menace"] == 15
        and ac["effective_stockpile"]["menace"] == 3320
        and failed["menace_delta"] == failed["crisis_objective_delta"] == 15
        and {key: value for key, value in old_obj.items()
             if key != "crisobj_destroy_enemy_ships"}
            == {key: value for key, value in new_obj.items()
                if key != "crisobj_destroy_enemy_ships"},
    "EEP_pop_queues_cash_messages_error_unchanged":
        bc["variables"] == ac["variables"]
        and b["audit"]["colonies"]["0"]["actual_pop_sum"]
            == a["audit"]["colonies"]["0"]["actual_pop_sum"] == 13081
        and q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and not a["pending"] and not a["messages"]
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "CN41_live_production_tree_unchanged":
        meta["language"] == "l_simp_chinese"
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(value is True for value in checks.values())
out = run / (after + "-first-enemy-fleet-cleared-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FIRST_ENEMY_FLEET_CLEARED" if passed else "FAIL",
    "checks": checks, "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "cleared_enemy_fleet": removed, "remaining_enemy_fleet": remaining,
    "remaining_enemy_ship": "33554917",
    "boundaries": ["active_kira39_last_enemy_single_day_review"],
    "scope": "First enemy fleet cleared; final enemy, battle victory and follow-up unaccepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]},
                 ensure_ascii=False), flush=True)
assert passed
