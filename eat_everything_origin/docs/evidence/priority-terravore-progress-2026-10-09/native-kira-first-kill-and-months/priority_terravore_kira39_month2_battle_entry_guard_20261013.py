"""Verify the natural Nov 1 Kira battle entry without declaring victory."""
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
before = "terravore-kira39-month1-native-22881001"
after = "terravore-kira39-month2-native-22881101"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = [read_state(run, stage) for stage in [before, after]]
ba, aa = b["audit"], a["audit"]
bc, ac = ba["countries"]["0"], aa["countries"]["0"]
prior = load(before + "-kira39-month1-proof-v2.json")
review = load("terravore-kira39-month2-22881101-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
receipts = [load(name + "-execution.json") for name in [
    before + "-guard-v2-recorded", review["execution_stage"],
    after + "-calendar", after + "-boundary-observation"]]

def source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def dec(value):
    return D(str(value))

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

own = ["83886903", "917", "50332250"]
enemy = ["33554515", "854"]
own_ids = {int(v) for v in own}
enemy_ids = {int(v) for v in enemy}
resources = ["energy", "minerals", "food", "alloys", "unity", "rare_crystals",
             "influence", "trade"]
net = {key: sum((dec(v.get(key, 0)) for v in
                 ac["budget_categories"]["current_month"]["balance"].values()), D(0))
       for key in resources}
expected = {key: dec(bc["effective_stockpile"].get(key, 0)) + net[key]
            for key in resources}
expected["influence"] = min(D(1000), expected["influence"])
expected["trade"] = min(D(50000), expected["trade"])
residual = {key: dec(ac["effective_stockpile"].get(key, 0)) - expected[key]
            for key in resources}
science = ["physics_research", "society_research", "engineering_research"]
science_residual = {
    key: dec(ac["research_stockpile"][key]) - dec(bc["research_stockpile"][key])
         - sum((dec(v.get(key, 0)) for v in
                bc["budget_categories"]["current_month"]["income"].values()), D(0))
             * D("1.35")
    for key in science}
army_ids = q.ids(q.block(b["country"], "owned_armies"))
old_enemy = {str(i) for fid in enemy for i in
             q.ids(q.block(q.block(b["roots"]["fleet"], fid), "ships"))}
new_enemy = {str(i) for fid in enemy for i in
             q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships"))}
old_all_ships = {k: v for k, v, obj in q.fields(b["roots"]["ships"])
                 if obj and k in old_enemy}
new_all_ships = {k: v for k, v, obj in q.fields(a["roots"]["ships"])
                 if obj and k in new_enemy}
health = ["hitpoints", "armor_hitpoints", "shield_hitpoints"]

def own_ship_health_ok(sid, raw):
    now = a["ships"][sid]
    old, current = q.scalars(raw), q.scalars(now)
    if sid == "33554922":
        return (old["hitpoints"] == current["hitpoints"] == 1500
                and old["armor_hitpoints"] == 765
                and current["armor_hitpoints"] == 739.54
                and old.get("shield_hitpoints") == current.get("shield_hitpoints")
                and current.get("experience") == 15
                and current.get("last_damage") == current.get("last_combat_activity")
                    == "2288.11.01")
    return all(old.get(key) == current.get(key) for key in health)

def enemy_ship_health_ok(sid, raw):
    old, now = q.scalars(raw), q.scalars(new_all_ships[sid])
    if sid == "1941":
        return (old["hitpoints"] == 400 and now["hitpoints"] == 190.71938
                and all(old.get(key) == now.get(key) for key in health[1:]))
    return all(old.get(key) == now.get(key) for key in health)

def fleet_in_battle(fid):
    fleet = a["fleets"][fid]
    movement = q.block(fleet, "movement_manager")
    return (combat_ids(fleet) == enemy_ids
            and q.scalars(movement).get("state") == "move_system"
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 39
            and q.scalars(q.block(movement, "target_coordinate"))["origin"] == 39
            and q.scalars(q.block(q.block(q.block(fleet, "current_order"),
                                        "orbit_planet_order"), "orbitable")) == {"planet": 543})

delay = [v for k, v, obj in q.fields(q.block(q.block(a["country"], "modules"),
                                       "standard_event_module"))
         if obj and k == "delayed_event"]
checks = {
    "month1_12PASS_review8_observer6_calendar_source_original_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_MONTH1_PRECONTACT"
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and [len(x["checks"]) for x in [prior, review, observed]] == [12, 8, 6]
        and all(v is True for x in [prior, review, observed]
                for v in x["checks"].values())
        and all(source_ok(x) for x in receipts)
        and prior["after_sha256"] == review["after_sha256"]
            == observed["before_sha256"] == ba["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == aa["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "one_native_30day_boundary_Nov1_no_error":
        ba["date"] == calendar["start_date"] == review["start_date"] == "2288.10.01"
        and aa["date"] == calendar["date"] == review["end_date"] == "2288.11.01"
        and calendar["days"] == review["days"] == 30
        and calendar["review_sha256"]
            == h.sha256(run / "terravore-kira39-month2-22881101-preflight.json")
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "eight_month_cash_categories_new_current_month_balance_exact":
        all(abs(v) < D(".00005") for v in residual.values())
        and all(ac["effective_stockpile"][key] >= 0 for key in resources),
    "one_native_Oct2_science_tick_all_three_idle_banks_exact":
        all(abs(v) < D(".00005") for v in science_residual.values())
        and all(not bc["research_queues"].get(k) and not ac["research_queues"].get(k)
                for k in ["physics_queue", "society_queue", "engineering_queue"]),
    "three_paid_hives_only_front_plus42_no_completion":
        q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and dec(q.scalars(a["items"]["117440553"])["progress"])
            - dec(q.scalars(b["items"]["117440553"])["progress"]) == D(42)
        and q.scalars(a["items"]["117440553"])["progress"] == 421.4
        and omit(b["items"]["117440553"], {"progress"})
            == omit(a["items"]["117440553"], {"progress"})
        and all(b["items"][str(i)] == a["items"][str(i)]
                for i in [1476395019, 117440546]),
    "mother_species73_natural_six_growth_only_colony":
        bc["owned_colonies"] == ac["owned_colonies"] == [0]
        and ba["colonies"]["0"]["actual_pop_sum"] == 13075
        and aa["colonies"]["0"]["actual_pop_sum"] == 13081
        and set(ba["pop_groups"]) == set(aa["pop_groups"]),
    "all75_original_ship_fleet_members_design_and_only_one_own_damage":
        len(b["ships"]) == len(a["ships"]) == 75
        and set(b["ships"]) == set(a["ships"])
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and all(q.ids(q.block(v, "ships")) == q.ids(q.block(a["fleets"][fid], "ships"))
                for fid, v in b["fleets"].items())
        and all(q.block(v, "ship_design_implementation")
                    == q.block(a["ships"][sid], "ship_design_implementation")
                and q.block(v, "name") == q.block(a["ships"][sid], "name")
                and own_ship_health_ok(sid, v) for sid, v in b["ships"].items()),
    "all_three_original_paid_fleets_in_Kira_real_combat_with_both_enemies":
        all(fleet_in_battle(fid) for fid in own),
    "both_hostile_fleets_18_ships_same_and_reciprocal_combat":
        old_enemy == new_enemy and len(new_enemy) == 18
        and all(len(q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships"))) == 9
                and combat_ids(q.block(a["roots"]["fleet"], fid)) == own_ids
                and q.scalars(q.block(q.block(q.block(a["roots"]["fleet"], fid),
                                          "movement_manager"), "coordinate"))["origin"] == 39
                for fid in enemy),
    "only_enemy_1941_native_hull_damage_without_kill":
        set(old_all_ships) == set(new_all_ships) == new_enemy
        and all(enemy_ship_health_ok(sid, raw) for sid, raw in old_all_ships.items()),
    "15_armies_war_truce_crisis_queen_EEP_menace_no_payout_yet":
        len(army_ids) == 15
        and army_ids == q.ids(q.block(a["country"], "owned_armies"))
        and all(q.block(b["roots"]["army"], str(i))
                == q.block(a["roots"]["army"], str(i)) for i in army_ids)
        and b["roots"]["war"] == a["roots"]["war"]
        and b["roots"]["truce"] == a["roots"]["truce"]
        and q.block(b["country"], "crisis_progression")
            == q.block(a["country"], "crisis_progression")
        and bc["variables"] == ac["variables"]
        and ac["effective_stockpile"]["menace"] == 3065,
    "no_battle_end_message_pending_delayed_event":
        b["messages"] == a["messages"] == []
        and not a["pending"] and not delay,
    "CN41_live_production_0point2point0":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-kira39-battle-entry-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_BATTLE_STARTED" if passed else "FAIL",
    "checks": checks, "before_sha256": ba["save_sha256"],
    "after_sha256": aa["save_sha256"], "date": aa["date"],
    "cash_residual": {k: str(v) for k, v in residual.items()},
    "science_residual": {k: str(v) for k, v in science_residual.items()},
    "boundaries": ["active_kira39_combat_single_day_review"],
    "native_devour_calendar_ready": False,
    "maximum_days_to_native_bite_boundary": 0,
    "scope": "Battle begun and both sides alive. Only a separately reviewed single day may follow.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, value in checks.items() if value is not True],
                  "date": aa["date"], "enemy_ships": len(new_enemy),
                  "cash_residual": {k: str(v) for k, v in residual.items()},
                  "science_residual": {k: str(v) for k, v in science_residual.items()}}),
      flush=True)
assert passed
