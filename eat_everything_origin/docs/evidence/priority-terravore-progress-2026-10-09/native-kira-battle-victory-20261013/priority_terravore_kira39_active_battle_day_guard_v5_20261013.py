"""Audit one continuing Kira battle day against actual kills and native rewards."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

before, after, prior_file, prior_stage, review_file = sys.argv[1:]
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = [read_state(run, stage) for stage in [before, after]]
ba, aa = b["audit"], a["audit"]
bc, ac = ba["countries"]["0"], aa["countries"]["0"]
prior, review = load(prior_file), load(review_file)
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
receipts = [load(name + "-execution.json") for name in [
    prior_stage, review["execution_stage"], after + "-calendar",
    after + "-boundary-observation"]]

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
own_ids = {int(fid) for fid in own}
enemy_ids = {int(fid) for fid in enemy}
before_enemy = {fid: {str(i) for i in
                q.ids(q.block(q.block(b["roots"]["fleet"], fid), "ships"))}
                for fid in enemy}
after_enemy = {fid: {str(i) for i in
               q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships"))}
               for fid in enemy}
before_ids = set.union(*before_enemy.values())
after_ids = set.union(*after_enemy.values())
before_raw = {sid: raw for sid, raw, obj in q.fields(b["roots"]["ships"])
              if obj and sid in before_ids}
after_raw = {sid: raw for sid, raw, obj in q.fields(a["roots"]["ships"])
             if obj and sid in before_ids}
removed = before_ids - after_ids
fresh_removed = {sid for sid in removed
                 if q.scalars(before_raw[sid]).get("killed") != "yes"
                 and (sid not in after_raw or
                      (q.scalars(after_raw[sid]).get("killed") == "yes"
                       and dec(q.scalars(after_raw[sid]).get("hitpoints", 0)) <= 0))}
later_cleanup = {sid for sid in removed
                 if q.scalars(before_raw[sid]).get("killed") == "yes"
                 and (sid not in after_raw or
                      q.scalars(after_raw[sid]).get("killed") == "yes")}
fresh_flagged = {sid for sid in before_ids & after_ids
                 if q.scalars(before_raw[sid]).get("killed") != "yes"
                 and q.scalars(after_raw[sid]).get("killed") == "yes"
                 and dec(q.scalars(after_raw[sid]).get("hitpoints", 0)) <= 0}
killed = sorted(fresh_removed | fresh_flagged, key=int)
old_objective, new_objective = objectives(b["country"]), objectives(a["country"])
health_keys = ["hitpoints", "armor_hitpoints", "shield_hitpoints"]
max_keys = ["max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints"]
damage = {}

def own_ship_ok(sid, old):
    new = a["ships"][sid]
    os, ns = q.scalars(old), q.scalars(new)
    deltas = {key: [os.get(key, 0), ns.get(key, 0)] for key in health_keys
              if os.get(key, 0) != ns.get(key, 0)}
    if deltas:
        damage[sid] = deltas
    return (q.block(old, "ship_design_implementation")
                == q.block(new, "ship_design_implementation")
            and q.block(old, "name") == q.block(new, "name")
            and all(os.get(key) == ns.get(key) for key in
                    ["fleet", "construction_date", "killed"] + max_keys)
            and D(0) < dec(ns.get("hitpoints", 0)) <= dec(ns.get("max_hitpoints", 0))
            and D(0) <= dec(ns.get("armor_hitpoints", 0))
                <= dec(ns.get("max_armor_hitpoints", 0))
            and (D(0) <= dec(ns.get("shield_hitpoints", 0))
                 <= dec(ns.get("max_shield_hitpoints", 0))))

def enemy_fleet_ok(fid):
    old = q.block(b["roots"]["fleet"], fid)
    new = q.block(a["roots"]["fleet"], fid)
    movement = q.block(new, "movement_manager")
    return (bool(old) and bool(new)
            and any(q.scalars(after_raw[sid]).get("killed") != "yes"
                    for sid in after_enemy[fid])
            and after_enemy[fid] <= before_enemy[fid]
            and combat_ids(new) == own_ids
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 39)

def own_fleet_ok(fid):
    old, new = b["fleets"][fid], a["fleets"][fid]
    movement = q.block(new, "movement_manager")
    extra = combat_ids(new) - enemy_ids
    return (q.ids(q.block(old, "ships")) == q.ids(q.block(new, "ships"))
            and enemy_ids <= combat_ids(new)
            and all(not q.block(a["roots"]["fleet"], str(i)) for i in extra)
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 39)

def ordinal(date):
    year, month, day = map(int, date.split("."))
    assert 1 <= month <= 12 and 1 <= day <= 30
    return year * 360 + (month - 1) * 30 + day - 1

army_ids = q.ids(q.block(b["country"], "owned_armies"))
non_science = ["energy", "minerals", "food", "alloys", "unity",
               "rare_crystals", "influence", "trade"]
science = ["physics_research", "society_research", "engineering_research"]
objective_source = Path("C:/SteamLibrary/steamapps/common/Stellaris/common/crisis_objectives/00_crisis_objectives.txt")
reward = q.scalars(q.block(q.block(objective_source.read_text("utf-8-sig"),
                                   "crisobj_destroy_enemy_ships"), "reward"))
checks = {
    "prior_PASS_review_PASS_observer6_all_source_original_SAV":
        prior["status"].startswith("PASS_NATIVE_KIRA39_")
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and prior["checks"] and review["checks"] and len(observed["checks"]) == 6
        and all(flag is True for proof in [prior, review, observed]
                for flag in proof["checks"].values())
        and all(source_ok(receipt) for receipt in receipts)
        and prior["after_sha256"] == review["after_sha256"]
            == observed["before_sha256"] == ba["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == aa["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "one_normal_native_single_day_not_after_Nov15":
        ba["date"] == calendar["start_date"] == review["start_date"]
        and aa["date"] == calendar["date"] == review["end_date"]
        and ordinal(aa["date"]) - ordinal(ba["date"]) == 1
        and calendar["days"] == review["days"] == 1
        and "2288.11.02" <= ba["date"] < aa["date"] <= "2288.11.15"
        and calendar["review_sha256"] == h.sha256(run / review_file),
    "original_Nemesis_destroy_ship_reward_rule_unchanged":
        reward == {"base": 3000, "divide": "trigger:num_galaxy_systems",
                   "round": "yes", "min": 3}
        and meta["requested_galaxy_settings"]["stars"] == 200,
    "two_hostile_fleets_continue_and_only_real_original_enemy_ships_can_die":
        all(enemy_fleet_ok(fid) for fid in enemy)
        and set(before_raw) == before_ids
        and removed == fresh_removed | later_cleanup
        and all(sid in after_raw for sid in fresh_flagged)
        and all(sid not in after_raw or
                q.scalars(after_raw[sid]).get("killed") == "yes"
                for sid in removed),
    "destroyed_ship_count_times15_equals_objective_and_menace_delta":
        new_objective["crisobj_destroy_enemy_ships"]
            - old_objective["crisobj_destroy_enemy_ships"] == 15 * len(killed)
        and ac["effective_stockpile"]["menace"]
            - bc["effective_stockpile"]["menace"] == 15 * len(killed)
        and {k: v for k, v in old_objective.items() if k != "crisobj_destroy_enemy_ships"}
            == {k: v for k, v in new_objective.items() if k != "crisobj_destroy_enemy_ships"},
    "all75_original_player_ships_identity_valid_health_and_same_fleet_members":
        len(b["ships"]) == len(a["ships"]) == 75
        and set(b["ships"]) == set(a["ships"])
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and all(q.ids(q.block(old, "ships")) == q.ids(q.block(a["fleets"][fid], "ships"))
                for fid, old in b["fleets"].items())
        and all(own_ship_ok(sid, raw) for sid, raw in b["ships"].items()),
    "three_original_paid_player_fleets_still_in_Kira_combat_and_no_real_extra_fleet":
        all(own_fleet_ok(fid) for fid in own),
    "no_monthly_cash_population_or_unexpected_research_tick":
        all(bc["effective_stockpile"][key] == ac["effective_stockpile"][key]
                for key in non_science)
        and all(bc["research_stockpile"][key] == ac["research_stockpile"][key]
                for key in science)
        and ba["colonies"]["0"]["actual_pop_sum"]
            == aa["colonies"]["0"]["actual_pop_sum"] == 13081,
    "paid_hive_only_front_one_day_work_no_completion":
        q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and dec(q.scalars(a["items"]["117440553"])["progress"])
            - dec(q.scalars(b["items"]["117440553"])["progress"]) == D("1.4")
        and dec(q.scalars(a["items"]["117440553"])["progress"]) < D(480)
        and omit(b["items"]["117440553"], {"progress"})
            == omit(a["items"]["117440553"], {"progress"})
        and all(b["items"][str(i)] == a["items"][str(i)]
                for i in [1476395019, 117440546]),
    "EEP_queen_15_armies_war_truce_no_new_country_event":
        bc["variables"] == ac["variables"]
        and len(army_ids) == 15
        and army_ids == q.ids(q.block(a["country"], "owned_armies"))
        and b["roots"]["war"] == a["roots"]["war"]
        and b["roots"]["truce"] == a["roots"]["truce"]
        and q.block(b["country"], "events") == q.block(a["country"], "events"),
    "no_battle_end_news_pending_or_error":
        b["messages"] == a["messages"] == []
        and not a["pending"]
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "CN41_production_mod_same":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(value is True for value in checks.values())
out = run / (after + "-kira39-active-battle-day-proof-v5.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_ACTIVE_BATTLE_DAY" if passed else "FAIL",
    "checks": checks, "before_sha256": ba["save_sha256"],
    "after_sha256": aa["save_sha256"], "date": aa["date"],
    "enemy_killed_original_ship_ids": killed,
    "newly_removed_killed_ship_ids": sorted(fresh_removed, key=int),
    "newly_flagged_killed_ship_ids": sorted(fresh_flagged, key=int),
    "previously_killed_cleaned_up_ids": sorted(later_cleanup, key=int),
    "player_ship_health_changes": damage,
    "crisis_objective_delta": new_objective["crisobj_destroy_enemy_ships"]
                              - old_objective["crisobj_destroy_enemy_ships"],
    "menace_delta": ac["effective_stockpile"]["menace"]
                    - bc["effective_stockpile"]["menace"],
    "boundaries": ["active_kira39_combat_single_day_review"],
    "native_devour_calendar_ready": False,
    "maximum_days_to_native_bite_boundary": 0,
    "scope": "One still-active two-enemy-fleet battle day; final victory and later days unaccepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True],
                  "date": aa["date"], "enemy_killed": killed,
                  "player_health_change_ships": sorted(damage, key=int),
                  "menace_delta": ac["effective_stockpile"]["menace"]
                                  - bc["effective_stockpile"]["menace"]}), flush=True)
assert passed
