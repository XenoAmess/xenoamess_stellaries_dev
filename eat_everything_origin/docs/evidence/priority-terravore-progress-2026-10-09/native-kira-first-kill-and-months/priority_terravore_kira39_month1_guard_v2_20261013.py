"""Check native first Kira travel month, resources, construction and identities."""
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
before = "terravore-kira39-main83886903-ordered-22880902"
after = "terravore-kira39-month1-native-22881001"
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = [read_state(run, st) for st in [before, after]]
ba, aa = b["audit"], a["audit"]
bc, ac = ba["countries"]["0"], aa["countries"]["0"]
prior = load(before + "-kira39-order-proof.json")
review = load("terravore-kira39-month1-22881001-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
failed = load("terravore-kira39-month1-22881001-calendar-execution.json")
receipts = [load(s + "-execution.json") for s in [
    before + "-guard", review["execution_stage"], after + "-calendar",
    after + "-boundary-observation"]]

def source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def decimal(value):
    return D(str(value))

resources = ["energy", "minerals", "food", "alloys", "unity", "rare_crystals",
             "influence", "trade"]
net = {key: sum((decimal(v.get(key, 0)) for v in
                 ac["budget_categories"]["current_month"]["balance"].values()), D(0))
       for key in resources}
expected = {key: decimal(bc["effective_stockpile"].get(key, 0)) + net[key]
            for key in resources}
expected["influence"] = min(D(1000), expected["influence"])
expected["trade"] = min(D(50000), expected["trade"])
residual = {key: decimal(ac["effective_stockpile"].get(key, 0)) - expected[key]
            for key in resources}

head = "117440553"
ids = q.ids(q.block(b["queues"]["0"], "items"))
paid = ["83886903", "917", "50332250"]
enemies = ["33554515", "854"]
own_members = all(q.ids(q.block(v, "ships")) == q.ids(q.block(a["fleets"][fid], "ships"))
                  for fid, v in b["fleets"].items())
ship_life = all(
    q.block(ship, "ship_design_implementation")
        == q.block(a["ships"][sid], "ship_design_implementation")
    and q.block(ship, "name") == q.block(a["ships"][sid], "name")
    and all(q.scalars(ship).get(key) == q.scalars(a["ships"][sid]).get(key)
            for key in ["construction_date", "killed", "max_hitpoints",
                        "max_armor_hitpoints", "max_shield_hitpoints", "hitpoints",
                        "armor_hitpoints", "shield_hitpoints"])
    for sid, ship in b["ships"].items())

def paid_fleet_native_windup(fid):
    fleet = a["fleets"][fid]
    movement = q.block(fleet, "movement_manager")
    order = q.block(q.block(fleet, "current_order"), "orbit_planet_order")
    path = q.block(movement, "path")
    return (q.scalars(movement)["state"] == "move_wind_up"
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 164
            and q.scalars(q.block(movement, "target_coordinate"))["origin"] == 39
            and q.scalars(q.block(order, "orbitable")) == {"planet": 543}
            and q.scalars(order).get("can_reach") == "yes"
            and q.scalars(path).get("date") in ["2288.11.22", "2288.11.23"]
            and not q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def enemy_held(fid):
    old = q.block(b["roots"]["fleet"], fid)
    now = q.block(a["roots"]["fleet"], fid)
    return (old == now and len(q.ids(q.block(now, "ships"))) == 9
            and q.scalars(q.block(q.block(now, "movement_manager"), "coordinate"))
                ["origin"] == 39)

army_ids = q.ids(q.block(b["country"], "owned_armies"))
delay = [v for k, v, obj in q.fields(q.block(q.block(a["country"], "modules"),
                                       "standard_event_module"))
         if obj and k == "delayed_event"]
checks = {
    "prior8_review8_observer6_calendar_all_actual0_source_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_MAIN_ORDER_ALL_THREE_STAGED"
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and observed["status"] == "OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY"
        and [len(v["checks"]) for v in [prior, review, observed]] == [8, 8, 6]
        and all(flag is True for v in [prior, review, observed]
                for flag in v["checks"].values())
        and all(source_ok(v) for v in receipts)
        and prior["after_sha256"] == review["after_sha256"] == observed["before_sha256"]
            == ba["save_sha256"] == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == aa["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "failed_preimport_no_GUI_original_retained":
        failed["returncode"] == 1
        and b"ModuleNotFoundError: No module named 'priority_native_reviewed_error_baseline'"
            in (run / "terravore-kira39-month1-22881001-calendar-stderr.txt").read_bytes()
        and not (run / "terravore-kira39-month1-22881001.sav").exists(),
    "one_native_29day_date_review_receipt":
        ba["date"] == calendar["start_date"] == review["start_date"] == "2288.09.02"
        and aa["date"] == calendar["date"] == review["end_date"] == "2288.10.01"
        and calendar["days"] == review["days"] == 29
        and calendar["review_sha256"] == h.sha256(
            run / "terravore-kira39-month1-22881001-preflight.json"),
    "all_eight_monthly_cash_balances_and_caps_reconcile":
        all(abs(v) < D(".00005") for v in residual.values())
        and all(ac["effective_stockpile"][k] >= 0 for k in resources),
    "three_research_banks_unchanged_before_Oct2_tick_and_empty_queues":
        all(bc["effective_stockpile"][k] == ac["effective_stockpile"][k]
                and bc["research_stockpile"][k] == ac["research_stockpile"][k]
                for k in ["physics_research", "society_research", "engineering_research"])
        and all(not bc["research_queues"].get(k) and not ac["research_queues"].get(k)
                for k in ["physics_queue", "society_queue", "engineering_queue"]),
    "three_paid_hives_only_front_plus40point6_no_completion":
        ids == q.ids(q.block(a["queues"]["0"], "items"))
        == [117440553, 1476395019, 117440546]
        and decimal(q.scalars(a["items"][head])["progress"])
            - decimal(q.scalars(b["items"][head])["progress"]) == D("40.6")
        and q.scalars(a["items"][head])["progress"] == 379.4
        and omit(b["items"][head], {"progress"}) == omit(a["items"][head], {"progress"})
        and all(b["items"][str(i)] == a["items"][str(i)] for i in ids[1:])
        and all(q.scalars(q.block(a["items"][str(i)], "resources")) == {"minerals": 400}
                for i in ids),
    "mother_original_species73_natural_growth_six_no_new_colony":
        bc["owned_colonies"] == ac["owned_colonies"] == [0]
        and ba["colonies"]["0"]["actual_pop_sum"] == 13069
        and aa["colonies"]["0"]["actual_pop_sum"] == 13075
        and set(aa["pop_groups"]) == set(ba["pop_groups"]),
    "all75_ship_original_identity_members_and_unchanged_combat_health":
        len(b["ships"]) == len(a["ships"]) == 75
        and set(b["ships"]) == set(a["ships"])
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and own_members and ship_life,
    "all_three_paid_fleets_real164_to39_windup_and_enemy18_held":
        all(paid_fleet_native_windup(fid) for fid in paid)
        and all(enemy_held(fid) for fid in enemies),
    "15_original_armies_war_truce_crisis_EEP_queen_menace_held":
        len(army_ids) == 15
        and army_ids == q.ids(q.block(a["country"], "owned_armies"))
        and all(q.block(b["roots"]["army"], str(i))
                == q.block(a["roots"]["army"], str(i)) for i in army_ids)
        and b["roots"]["war"] == a["roots"]["war"]
        and b["roots"]["truce"] == a["roots"]["truce"]
        and q.block(b["country"], "crisis_progression")
            == q.block(a["country"], "crisis_progression")
        and bc["variables"] == ac["variables"]
        and ac["variables"]["eep_c"] == 76
        and ac["variables"]["eep_d"] == 21
        and ac["variables"]["eep_crisis"] == 3
        and ac["variables"]["eep_stage"] == 2
        and ac["effective_stockpile"]["menace"] == 3065,
    "no_new_notifications_pending_battle_delayed_event_or_error":
        b["messages"] == a["messages"] == [] and not a["pending"] and not delay
        and not any(q.ids(q.block(q.block(v, "combat"), "in_combat_with"))
                    for v in a["fleets"].values())
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "CN41_production_mod_0point2point0_held":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-kira39-month1-proof-v2.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_MONTH1_PRECONTACT" if passed else "FAIL",
    "checks": checks, "before_sha256": ba["save_sha256"],
    "after_sha256": aa["save_sha256"], "date": aa["date"],
    "cash_residual": {k: str(v) for k, v in residual.items()},
    "hive_front_work": q.scalars(a["items"][head])["progress"],
    "boundaries": ["kira39_precontact_bounded_calendar_review"],
    "native_devour_calendar_ready": False,
    "maximum_days_to_native_bite_boundary": 0,
    "scope": "Only first native travel month; no Kira combat, colony or full Terravore route acceptance.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, value in checks.items() if value is not True],
                  "date": aa["date"], "hive": q.scalars(a["items"][head])["progress"],
                  "cash_residual": {k: str(v) for k, v in residual.items()}}), flush=True)
assert passed
