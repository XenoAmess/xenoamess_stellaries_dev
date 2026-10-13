"""Verify first native post-birth month, budget and capacity effect."""
import json
import logging
import sys
from decimal import Decimal as D
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
pre = "terravore-kira39-shipyard-precompletion-native-22881224"
before = "terravore-kira39-shipyard-birth-native-22881225"
after = "terravore-kira39-postbirth-month-native-22890101"
prior = "terravore-kira39-shipyard-birth-guard-22881225"
review_stage = "terravore-kira39-postbirth-month-review-22881225"
stage = "terravore-kira39-postbirth-month-guard-22890101"
assert not (run / (stage + "-proof.json")).exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
p, b, a = (read_state(run, s) for s in (pre, before, after))
previous, review = (load(n + suffix) for n, suffix in
                    [(prior, "-proof.json"), (review_stage, "-review.json")])
calendar, execution = load(after + "-calendar-receipt.json"), load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
cur = ac["budget_categories"]["current_month"]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
net = {k: sum((D(str(v.get(k, 0))) for v in cur["income"].values()), D(0))
       - sum((D(str(v.get(k, 0))) for v in cur["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
old_ships = bc["budget_categories"]["current_month"]["expenses"]["ships"]
new_ships = cur["expenses"]["ships"]
old_cap = q.scalars(p["country"])["used_naval_capacity"]
new_cap = q.scalars(a["country"])["used_naval_capacity"]
factor = D(new_cap) / D(old_cap)
upkeep_residual = {}
for k in ["energy", "minerals", "alloys"]:
    civilian = D(3) if k == "energy" else D(0)
    expected = (D(str(old_ships[k])) - civilian) * factor + civilian
    upkeep_residual[k] = D(str(new_ships[k])) - expected
science = a["fleets"]["166"]
move = q.block(science, "movement_manager")
reinforcement = a["fleets"]["50331731"]
old_message = q.scalars(b["messages"][0]) if len(b["messages"]) == 1 else {}
checks = {
    "birth_review_calendar_native_saves_exact_sha_chain":
        previous["status"] == "PASS_NATIVE_KIRA39_MINERAL_CRISIS_DESTROYER_BIRTH"
        and all(previous["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 6
        and calendar["start_date"] == "2288.12.25"
        and calendar["date"] == "2289.01.01"
        and previous["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "first_month_five_cash_resources_equal_actual_new_month_net":
        all(abs(v) <= D("0.00002") for v in residual.values())
        and ac["budget_categories"]["last_month"]
            == bc["budget_categories"]["current_month"]
        and actual["minerals"] == D("-100.15561")
        and actual["alloys"] == D("-7.44595"),
    "new_capacity_explains_total_ships_alloy_maintenance_change":
        old_cap == 243 and new_cap == 251
        and all(abs(v) <= D("0.0001") for v in upkeep_residual.values())
        and new_ships["alloys"] == 18.20219
        and new_ships["minerals"] == 70.89311,
    "science166_safe_windup_and_new_ship_still_mia_for_fleet917":
        q.scalars(q.block(move, "coordinate"))["origin"] == 97
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and q.scalars(move)["state"] == "move_wind_up"
        and "can_reach=yes" in q.block(science, "current_order")
        and q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.scalars(q.block(q.block(reinforcement, "current_order"),
                              "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8,
    "all_75_ships_rosters_eep_and_expired_original_battle_report":
        set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ["eep_c", "eep_d", "eep_stage", "eep_crisis"])
        and old_message.get("type") == "COMBAT_STATS"
        and old_message.get("end") == "2288.12.29"
        and a["messages"] == []
        and b["pending"] == a["pending"] == [],
    "no_new_error":
        (run / (after + "-error-before.log")).read_bytes()
        == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_POSTBIRTH_FIRST_MONTH" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "cash_residuals": {k: str(v) for k, v in residual.items()},
    "upkeep_overcap_residuals": {k: str(v) for k, v in upkeep_residual.items()},
    "scope": "First monthly MIA reinforcement capacity effect and scout travel; not return, individual MIA ship upkeep, survey or devour.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
