"""Independent native per-ship guard for March 15 combat during enemy return."""
import json
import logging
import sys
from decimal import Decimal
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
start, stage = "hope-route-mar14-native-22940314", "hope-route-mar15-native-22940315"
a, b = read_state(run, start), read_state(run, stage)
prior = json.loads((run / "hope-route-mar14-enemy-return-guard-v2-22940314-proof.json").read_text("utf-8"))
pre = json.loads((run / (stage + "-preflight.json")).read_text("utf-8"))
receipt = json.loads((run / (stage + "-calendar-receipt.json")).read_text("utf-8"))
execution = json.loads((run / "hope-route-mar15-defense-calendar-20261014-execution.json").read_text("utf-8"))
dist = json.loads((run / "hope-route-mar15-damage-distribution-22940315.json").read_text("utf-8"))
review = json.loads((run / "hope-route-mar15-defense-review-22940315.json").read_text("utf-8"))
month = json.loads((run / "hope-route-mar15-month-review-22940315.json").read_text("utf-8"))
ac, bc = a["audit"]["countries"]["0"], b["audit"]["countries"]["0"]
fleet_ids = ("50332250", "917", "50332411", "69")

def members(state, fid):
    return [str(sid) for sid in q.ids(q.block(q.block(state["roots"]["fleet"], fid), "ships"))]

ids_a = {fid: members(a, fid) for fid in fleet_ids}
ids_b = {fid: members(b, fid) for fid in fleet_ids}
all_ids = {sid for ids in ids_b.values() for sid in ids}
ships_a = {k: q.scalars(v) for k, v, nested in q.fields(a["roots"]["ships"])
           if nested and k in all_ids}
ships_b = {k: q.scalars(v) for k, v, nested in q.fields(b["roots"]["ships"])
           if nested and k in all_ids}
ours = set(ids_b["50332250"] + ids_b["917"])
enemy = set(ids_b["50332411"])
damage_fields = ("hitpoints", "armor_hitpoints", "shield_hitpoints")
expected = {
    "50333149": {"shield_hitpoints": (143.51006, 144.31006)},
    "33554923": {"shield_hitpoints": (86.98999, 87.78999)},
    "16777920": {"hitpoints": (693.70301, 694.45301)},
    "33555010": {"shield_hitpoints": (465.2546, 461.65678)},
    "33554925": {"hitpoints": (712.99752, 713.74752)},
    "33556327": {"shield_hitpoints": (456.39386, 458.79386)},
    "33554922": {"armor_hitpoints": (256.94727, None),
                 "hitpoints": (1500, 1305.38946)},
    "50333131": {"shield_hitpoints": (443.7075, 438.92115)},
    "50333394": {"shield_hitpoints": (455.36978, 457.76978)},
    "16779175": {"hitpoints": (726.70701, 727.45701)},
    "50332133": {"shield_hitpoints": (412.82415, 415.22415)},
    "67109347": {"armor_hitpoints": (176.625, None)},
    "33556352": {"armor_hitpoints": (251.0691, None),
                 "hitpoints": (280, 226.80382)},
    "33556025": {"hitpoints": (246.3833, 231.1481)},
    "16778219": {"hitpoints": (204.0436, 24.31355)},
    "67110711": {"hitpoints": (234.48408, 197.51388)},
}

def exact_damage(sid):
    x, y = ships_a[sid], ships_b[sid]
    return x.get("fleet") == y.get("fleet") and all(
        (x.get(field), y.get(field)) == expected.get(sid, {}).get(
            field, (x.get(field), x.get(field))) for field in damage_fields)

enemy_fleet = q.block(b["roots"]["fleet"], "50332411")
cash = ("energy", "minerals", "alloys", "trade", "unity", "astral_threads")
checks = {
    "bound_native_calendar_and_sources": meta["language"] == "l_simp_chinese"
    and meta["version"] == "0.2.0" and prior["pass"]
    and a["audit"]["date"] == "2294.03.14" and b["audit"]["date"] == "2294.03.15"
    and a["audit"]["save_sha256"] == prior["after_save_sha256"]
    and h.sha256(run / (start + ".sav")) == a["audit"]["save_sha256"]
    and h.sha256(run / (stage + ".sav")) == b["audit"]["save_sha256"]
    and pre["status"] == "PASS_BOUND_1_DAY_COMBAT_PREFLIGHT"
    and pre["start_sha256"] == a["audit"]["save_sha256"]
    and pre["start_date"] == "2294.03.14" and pre["end_date"] == "2294.03.15"
    and pre["days"] == 1
    and receipt["status"] == "CALENDAR_CONFIRMED" and receipt["days"] == 1
    and receipt["start_date"] == "2294.03.14" and receipt["date"] == "2294.03.15"
    and execution["returncode"] == 0
    and h.sha256(Path(execution["command"][1])) == execution["helper_sha256"]
    and dist["before_date"] == review["before_date"] == month["before_date"] == "2294.03.14"
    and dist["after_date"] == review["after_date"] == month["after_date"] == "2294.03.15"
    and month["save_sha256"] == review["after_save_sha256"] == b["audit"]["save_sha256"],
    "fleet_members_and_neutral_unchanged": ids_a == ids_b == dist["members"]
    and len(ours) == 22 and len(enemy) == 17 and set(ships_a) == set(ships_b) == all_ids
    and dist["neutral_ship_unchanged"] and a["fleets"]["83886903"] == b["fleets"]["83886903"],
    "our_exact_per_ship_damage": all(exact_damage(sid) for sid in ours)
    and q.scalars(b["fleets"]["50332250"]).get("hit_points") == 9158.2005
    and q.scalars(b["fleets"]["917"]).get("hit_points") == 12601.58499,
    "enemy_exact_per_ship_damage_and_target": all(exact_damage(sid) for sid in enemy)
    and q.scalars(enemy_fleet).get("hit_points") == 4488.64154
    and "return_fleet_order" in q.block(enemy_fleet, "current_order")
    and "starbase=101" in q.block(enemy_fleet, "current_order")
    and q.scalars(q.block(q.block(enemy_fleet, "movement_manager"), "coordinate")).get("origin") == 30,
    "same_month_colony_cash_war_stable": ac["owned_colonies"] == bc["owned_colonies"] == [0, 40]
    and month["mother_pop_before"] == month["mother_pop_after"] == 13473
    and month["colony_pop_before"] == month["colony_pop_after"] == 15
    and all(Decimal(month["cash_delta"][k]) == 0 for k in cash)
    and month["war_unchanged"] and a["roots"]["war"] == b["roots"]["war"]
    and ac["effective_stockpile"]["menace"] == bc["effective_stockpile"]["menace"] == 3365,
    "mod_messages_and_error_stable": ac["variables"] == bc["variables"]
    and ac["crisis"] == bc["crisis"] and a["messages"] == b["messages"] == []
    and a["pending"] == b["pending"] == []
    and (run / (stage + "-error-before.log")).read_bytes()
    == (run / (stage + "-error-after.log")).read_bytes()
    == (user / "logs" / "error.log").read_bytes(),
}
proof = {"stage": "hope-route-mar15-battle-return-guard-22940315",
         "pass": all(checks.values()),
         "status": "PASS_NATIVE_HEAVY_BATTLE_DAY" if all(checks.values()) else "FAIL",
         "before_save_sha256": a["audit"]["save_sha256"],
         "after_save_sha256": b["audit"]["save_sha256"],
         "checks": checks}
out = run / (proof["stage"] + "-proof.json")
assert not out.exists()
out.write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n",
               encoding="utf-8", newline="\n")
print(json.dumps(proof, ensure_ascii=False), flush=True)
sys.exit(0 if proof["pass"] else 1)
