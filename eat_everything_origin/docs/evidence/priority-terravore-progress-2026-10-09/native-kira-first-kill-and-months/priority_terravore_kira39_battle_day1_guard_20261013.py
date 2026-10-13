"""Audit the first native Kira kill and crisis objective transaction."""
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
before = "terravore-kira39-month2-native-22881101"
after = "terravore-kira39-battle-day1-native-22881102"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = [read_state(run, stage) for stage in [before, after]]
ba, aa = b["audit"], a["audit"]
bc, ac = ba["countries"]["0"], aa["countries"]["0"]
prior = load(before + "-kira39-battle-entry-proof.json")
review = load("terravore-kira39-battle-day1-22881102-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
receipts = [load(name + "-execution.json") for name in [
    before + "-battle-entry-guard", review["execution_stage"],
    after + "-calendar", after + "-boundary-observation"]]

def source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def dec(value):
    return D(str(value))

def objectives(country):
    return {q.scalars(raw)["objective"]: q.scalars(raw)["progress"]
            for key, raw, obj in q.fields(q.block(country, "crisis_progression"))
            if key == "objective" and obj}

science = ["physics_research", "society_research", "engineering_research"]
science_residual = {
    key: dec(ac["research_stockpile"][key]) - dec(bc["research_stockpile"][key])
         - sum((dec(v.get(key, 0)) for v in
                bc["budget_categories"]["current_month"]["income"].values()), D(0))
             * D("1.35")
    for key in science}
non_science = ["energy", "minerals", "food", "alloys", "unity", "rare_crystals",
               "influence", "trade"]
old_enemy = {str(i) for fid in ["33554515", "854"] for i in
             q.ids(q.block(q.block(b["roots"]["fleet"], fid), "ships"))}
new_enemy = {str(i) for fid in ["33554515", "854"] for i in
             q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships"))}
health = ["hitpoints", "armor_hitpoints", "shield_hitpoints"]
damage = {
    "16777244": (D("765"), D("702.8625")),
    "33554922": (D("739.54"), D("691.1825")),
    "100665071": (D("765"), D("678.1825")),
}

def ship_held(sid, old):
    now = a["ships"][sid]
    os, ns = q.scalars(old), q.scalars(now)
    identity = (q.block(old, "ship_design_implementation")
                == q.block(now, "ship_design_implementation")
                and q.block(old, "name") == q.block(now, "name")
                and all(os.get(key) == ns.get(key) for key in
                        ["fleet", "construction_date", "max_hitpoints",
                         "max_armor_hitpoints", "max_shield_hitpoints", "killed"]))
    if sid in damage:
        return (identity and dec(os["armor_hitpoints"]) == damage[sid][0]
                and dec(ns["armor_hitpoints"]) == damage[sid][1]
                and os.get("hitpoints") == ns.get("hitpoints")
                and os.get("shield_hitpoints") == ns.get("shield_hitpoints"))
    return identity and all(os.get(key) == ns.get(key) for key in health)

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

bo, ao = objectives(b["country"]), objectives(a["country"])
army_ids = q.ids(q.block(b["country"], "owned_armies"))
ghost = "385875972"
objective_source = Path("C:/SteamLibrary/steamapps/common/Stellaris/common/crisis_objectives/00_crisis_objectives.txt")
objective_raw = q.block(objective_source.read_text("utf-8-sig"),
                        "crisobj_destroy_enemy_ships")
reward = q.scalars(q.block(objective_raw, "reward"))
checks = {
    "battle_entry13_review7_observer6_calendar_actual0_source_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_BATTLE_STARTED"
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and [len(v["checks"]) for v in [prior, review, observed]] == [13, 7, 6]
        and all(flag is True for v in [prior, review, observed]
                for flag in v["checks"].values())
        and all(source_ok(v) for v in receipts)
        and prior["after_sha256"] == review["after_sha256"]
            == observed["before_sha256"] == ba["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == aa["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "one_only_native_battle_day_Nov1_to_Nov2":
        ba["date"] == review["start_date"] == calendar["start_date"] == "2288.11.01"
        and aa["date"] == review["end_date"] == calendar["date"] == "2288.11.02"
        and review["days"] == calendar["days"] == 1
        and calendar["review_sha256"]
            == h.sha256(run / "terravore-kira39-battle-day1-22881102-preflight.json"),
    "original_crisis_ship_objective_reward_3000_divide_systems_round_min3":
        reward == {"base": 3000, "divide": "trigger:num_galaxy_systems",
                   "round": "yes", "min": 3}
        and meta["requested_galaxy_settings"]["stars"] == 200
        and objective_source.exists(),
    "exact_one_real_enemy_ship1941_removed_without_own_ship_loss":
        len(old_enemy) == 18 and new_enemy == old_enemy - {"1941"}
        and not q.block(a["roots"]["ships"], "1941")
        and len(b["ships"]) == len(a["ships"]) == 75
        and set(b["ships"]) == set(a["ships"]),
    "native_destroy_ship_objective_and_menace_each_plus15":
        bo["crisobj_destroy_enemy_ships"] == 270
        and ao["crisobj_destroy_enemy_ships"] == 285
        and {k: v for k, v in bo.items() if k != "crisobj_destroy_enemy_ships"}
            == {k: v for k, v in ao.items() if k != "crisobj_destroy_enemy_ships"}
        and bc["effective_stockpile"]["menace"] == 3065
        and ac["effective_stockpile"]["menace"] == 3080,
    "all75_original_ship_design_membership_and_exact_three_armor_damages":
        len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and all(q.ids(q.block(v, "ships")) == q.ids(q.block(a["fleets"][fid], "ships"))
                for fid, v in b["fleets"].items())
        and all(ship_held(sid, raw) for sid, raw in b["ships"].items()),
    "original_paid_fleet39_both_actual_enemies_still_in_combat":
        all({854, 33554515} <= combat_ids(a["fleets"][fid])
                and q.scalars(q.block(q.block(a["fleets"][fid], "movement_manager"),
                                      "coordinate"))["origin"] == 39
                for fid in ["83886903", "917", "50332250"])
        and all(len(q.ids(q.block(q.block(a["roots"]["fleet"], fid), "ships")))
                    == (9 if fid == "33554515" else 8)
                for fid in ["33554515", "854"]),
    "combat_cache_extra_ID_not_a_real_third_fleet":
        combat_ids(a["fleets"]["50332250"]) == {854, 33554515, 385875972}
        and not q.block(a["roots"]["fleet"], ghost)
        and not q.block(b["roots"]["fleet"], ghost),
    "one_native_Nov2_research_tick_exact_no_monthly_cash_or_pop":
        all(abs(value) < D(".00005") for value in science_residual.values())
        and all(bc["effective_stockpile"][key] == ac["effective_stockpile"][key]
                for key in non_science)
        and ba["colonies"]["0"]["actual_pop_sum"]
            == aa["colonies"]["0"]["actual_pop_sum"] == 13081,
    "paid_hive_front_one_native_day_plus1point4_no_completion":
        q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and dec(q.scalars(b["items"]["117440553"])["progress"]) == D("421.4")
        and dec(q.scalars(a["items"]["117440553"])["progress"]) == D("422.8")
        and omit(b["items"]["117440553"], {"progress"})
            == omit(a["items"]["117440553"], {"progress"})
        and all(b["items"][str(i)] == a["items"][str(i)]
                for i in [1476395019, 117440546]),
    "queen_EEP_government_war_truce_15_armies_still_held":
        bc["variables"] == ac["variables"]
        and all(bc[key] == ac[key] for key in
                ["government", "ascension_perks", "traditions"])
        and b["roots"]["war"] == a["roots"]["war"]
        and b["roots"]["truce"] == a["roots"]["truce"]
        and len(army_ids) == 15
        and army_ids == q.ids(q.block(a["country"], "owned_armies")),
    "no_false_battle_end_message_pending_or_new_error":
        b["messages"] == a["messages"] == []
        and not a["pending"]
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "CN41_production_0point2point0_unchanged":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(value is True for value in checks.values())
out = run / (after + "-kira39-first-kill-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FIRST_KILL_MENACE15" if passed else "FAIL",
    "checks": checks, "before_sha256": ba["save_sha256"],
    "after_sha256": aa["save_sha256"], "date": aa["date"],
    "objective_source_sha256": h.sha256(objective_source),
    "destroy_enemy_ships_progress": [bo["crisobj_destroy_enemy_ships"],
                                     ao["crisobj_destroy_enemy_ships"]],
    "science_residual": {k: str(v) for k, v in science_residual.items()},
    "boundaries": ["active_kira39_combat_single_day_review"],
    "native_devour_calendar_ready": False,
    "maximum_days_to_native_bite_boundary": 0,
    "scope": "First one-ship original menace payout only; Kira battle still active.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, value in checks.items() if value is not True],
                  "date": aa["date"], "enemy_ships": len(new_enemy),
                  "menace": ac["effective_stockpile"]["menace"]}), flush=True)
assert passed
