"""Audit first actual paid mineral crisis destroyer loss in Kira battle."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-battle-day6-native-22881107"
after = "terravore-kira39-battle-day7-native-22881108"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = [read_state(run, stage) for stage in [before, after]]
ba, aa = b["audit"], a["audit"]
bc, ac = ba["countries"]["0"], aa["countries"]["0"]
prior = load(before + "-kira39-active-battle-day-proof-v5.json")
review = load("terravore-kira39-battle-day7-22881108-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
failed = load(after + "-active-guard-v5-execution.json")
receipts = [load(name + "-execution.json") for name in [
    before + "-active-guard-v5", review["execution_stage"],
    after + "-calendar", after + "-boundary-observation"]]

def source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def dec(value):
    return D(str(value))

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def objectives(country):
    return {q.scalars(raw)["objective"]: q.scalars(raw)["progress"]
            for key, raw, obj in q.fields(q.block(country, "crisis_progression"))
            if key == "objective" and obj}

own = ["83886903", "917", "50332250"]
enemy = ["33554515", "854"]
own_ids = {int(i) for i in own}
enemy_ids = {int(i) for i in enemy}
lost = "16777244"
lost_ship = b["ships"][lost]
lost_design = q.scalars(q.block(lost_ship, "ship_design_implementation"))["design"]
old_members = {fid: set(q.ids(q.block(b["fleets"][fid], "ships"))) for fid in own}
new_members = {fid: set(q.ids(q.block(a["fleets"][fid], "ships"))) for fid in own}
old_enemy = {fid: {str(i) for i in
             q.ids(q.block(q.block(b["roots"]["fleet"], fid), "ships"))}
             for fid in enemy}
new_enemy = {fid: {str(i) for i in
             q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships"))}
             for fid in enemy}
bo, ao = objectives(b["country"]), objectives(a["country"])
ship_health_changes = {}

def survivor_ok(sid, old):
    now = a["ships"][sid]
    os, ns = q.scalars(old), q.scalars(now)
    changes = {key: [os.get(key, 0), ns.get(key, 0)]
               for key in ["hitpoints", "armor_hitpoints", "shield_hitpoints"]
               if os.get(key, 0) != ns.get(key, 0)}
    if changes:
        ship_health_changes[sid] = changes
    return (q.block(old, "ship_design_implementation")
                == q.block(now, "ship_design_implementation")
            and q.block(old, "name") == q.block(now, "name")
            and all(os.get(key) == ns.get(key) for key in
                    ["fleet", "construction_date", "killed", "max_hitpoints",
                     "max_armor_hitpoints", "max_shield_hitpoints"])
            and D(0) < dec(ns.get("hitpoints", 0)) <= dec(ns.get("max_hitpoints", 0))
            and D(0) <= dec(ns.get("armor_hitpoints", 0))
                <= dec(ns.get("max_armor_hitpoints", 0))
            and D(0) <= dec(ns.get("shield_hitpoints", 0))
                <= dec(ns.get("max_shield_hitpoints", 0)))

army_ids = q.ids(q.block(b["country"], "owned_armies"))
non_science = ["energy", "minerals", "food", "alloys", "unity",
               "rare_crystals", "influence", "trade"]
science = ["physics_research", "society_research", "engineering_research"]
checks = {
    "prior12_review7_observer6_actual0_source_original_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_ACTIVE_BATTLE_DAY"
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and [len(v["checks"]) for v in [prior, review, observed]] == [12, 7, 6]
        and all(flag is True for v in [prior, review, observed]
                for flag in v["checks"].values())
        and all(source_ok(receipt) for receipt in receipts)
        and prior["after_sha256"] == review["after_sha256"]
            == observed["before_sha256"] == ba["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == aa["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "original_no_loss_guard_FAIL_retained_and_one_normal_day":
        failed["returncode"] == 1
        and load(after + "-kira39-active-battle-day-proof-v5.json")["status"] == "FAIL"
        and ba["date"] == review["start_date"] == calendar["start_date"] == "2288.11.07"
        and aa["date"] == review["end_date"] == calendar["date"] == "2288.11.08"
        and review["days"] == calendar["days"] == 1
        and calendar["review_sha256"]
            == h.sha256(run / "terravore-kira39-battle-day7-22881108-preflight.json"),
    "only_paid_fleet917_original_crisis_destroyer16777244_died":
        lost_design == 83887141
        and q.scalars(lost_ship)["fleet"] == 917
        and 'ship_size="crisis_destroyer"' in b["designs"][str(lost_design)]
        and lost in b["ships"] and lost not in a["ships"]
        and not q.block(a["roots"]["ships"], lost)
        and len(b["ships"]) == 75 and len(a["ships"]) == 74
        and set(b["ships"]) - set(a["ships"]) == {lost}
        and not (set(a["ships"]) - set(b["ships"])),
    "fleet917_only_one_member_lost_main_and_other_support_held":
        len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and len(old_members["917"]) == 9 and len(new_members["917"]) == 8
        and old_members["917"] - new_members["917"] == {int(lost)}
        and new_members["917"] <= old_members["917"]
        and all(old_members[fid] == new_members[fid] for fid in
                ["83886903", "50332250"])
        and all(q.ids(q.block(old, "ships")) == q.ids(q.block(a["fleets"][fid], "ships"))
                for fid, old in b["fleets"].items() if fid != "917"),
    "all74_survivors_original_identity_and_valid_health":
        all(survivor_ok(sid, old) for sid, old in b["ships"].items()
            if sid != lost),
    "fleet_template_still_targets_nine_no_auto_replacement":
        q.block(b["roots"]["fleet_template"], "268435546")
            == q.block(a["roots"]["fleet_template"], "268435546")
        and "count=9" in q.block(a["roots"]["fleet_template"], "268435546")
        and not q.ids(q.block(a["queues"].get("3", ""), "items")),
    "one_enemy_33554915_kill_15_native_objective_and_menace":
        old_enemy["33554515"] - new_enemy["33554515"]
            == {"33554915", "16778916"}
        and q.scalars(q.block(b["roots"]["ships"], "16778916")).get("killed")
            == "yes"
        and not q.block(a["roots"]["ships"], "16778916")
        and old_enemy["854"] == new_enemy["854"]
        and not q.block(a["roots"]["ships"], "33554915")
        and ao["crisobj_destroy_enemy_ships"]
            - bo["crisobj_destroy_enemy_ships"] == 15
        and ac["effective_stockpile"]["menace"]
            - bc["effective_stockpile"]["menace"] == 15
        and {k: v for k, v in bo.items() if k != "crisobj_destroy_enemy_ships"}
            == {k: v for k, v in ao.items() if k != "crisobj_destroy_enemy_ships"},
    "three_paid_fleets_and_two_real_enemies_still_in_Kira_combat":
        all(enemy_ids <= combat_ids(a["fleets"][fid])
                and all(not q.block(a["roots"]["fleet"], str(i))
                        for i in combat_ids(a["fleets"][fid]) - enemy_ids)
                and q.scalars(q.block(q.block(a["fleets"][fid], "movement_manager"),
                                      "coordinate"))["origin"] == 39
                for fid in own)
        and all(combat_ids(q.block(a["roots"]["fleet"], fid)) == own_ids
                and q.scalars(q.block(q.block(q.block(a["roots"]["fleet"], fid),
                                          "movement_manager"), "coordinate"))["origin"] == 39
                for fid in enemy),
    "no_same_day_monthly_cash_research_or_population_jump":
        all(bc["effective_stockpile"][key] == ac["effective_stockpile"][key]
                for key in non_science)
        and all(bc["research_stockpile"][key] == ac["research_stockpile"][key]
                for key in science)
        and ba["colonies"]["0"]["actual_pop_sum"]
            == aa["colonies"]["0"]["actual_pop_sum"] == 13081
        and bc["budget_categories"]["current_month"]["expenses"]["ships"]
            == ac["budget_categories"]["current_month"]["expenses"]["ships"],
    "paid_hive_daily1point4_queue_same_no_completion":
        q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and dec(q.scalars(a["items"]["117440553"])["progress"])
            - dec(q.scalars(b["items"]["117440553"])["progress"]) == D("1.4")
        and omit(b["items"]["117440553"], {"progress"})
            == omit(a["items"]["117440553"], {"progress"}),
    "EEP_queen_15_armies_war_truce_no_new_event_or_error":
        bc["variables"] == ac["variables"]
        and len(army_ids) == 15
        and army_ids == q.ids(q.block(a["country"], "owned_armies"))
        and b["roots"]["war"] == a["roots"]["war"]
        and b["roots"]["truce"] == a["roots"]["truce"]
        and b["messages"] == a["messages"] == []
        and not a["pending"]
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "CN41_live_production_mod_same":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-kira39-first-paid-ship-loss-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FIRST_PAID_CRISIS_DESTROYER_LOSS" if passed else "FAIL",
    "checks": checks, "before_sha256": ba["save_sha256"],
    "after_sha256": aa["save_sha256"], "date": aa["date"],
    "lost_paid_ship_id": lost, "lost_design_id": lost_design,
    "surviving_player_ship_health_changes": ship_health_changes,
    "enemy_killed_ship_id": "33554915", "menace_delta": 15,
    "boundaries": ["active_kira39_post_loss_single_day_review"],
    "native_devour_calendar_ready": False,
    "maximum_days_to_native_bite_boundary": 0,
    "scope": "One real mineral crisis destroyer lost; battle ongoing, replacement and monthly upkeep not yet accepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True],
                  "date": aa["date"], "lost_paid_ship": lost,
                  "survivors": len(a["ships"]), "enemy_kill": "33554915"}), flush=True)
assert passed
