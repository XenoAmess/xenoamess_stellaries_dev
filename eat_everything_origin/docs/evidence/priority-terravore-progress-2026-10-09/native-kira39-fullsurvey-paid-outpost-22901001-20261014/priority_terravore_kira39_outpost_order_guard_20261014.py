"""Verify one paid native Kira outpost order without advancing the calendar."""
import json
import logging
import sys
from decimal import Decimal as D

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-fullsystem-roll14-native-22901001"
after = "terravore-kira39-outpost-ordered-native-22901001"
stage = "terravore-kira39-outpost-order-guard-22901001"
out = run / (stage + "-proof.json")
assert not out.exists()
b, a = read_state(run, before), read_state(run, after)
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
prior = json.loads((run / "terravore-kira39-fullsystem-roll14-v9guard-22901001-proof.json").read_text("utf-8-sig"))
execution = json.loads((run / "terravore-kira39-fullsystem-roll14-v9guard-22901001-execution.json").read_text("utf-8-sig"))
receipt = json.loads((run / (after + ".native-save.json")).read_text("utf-8-sig"))
station = q.block(q.block(a["fleets"]["2"], "current_order"), "build_orbital_station_order")
cash = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
delta = {k: D(str(ac["effective_stockpile"].get(k, 0)))
         - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
checks = {
    "reviewed_fullsystem_sav_and_native_order_source":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and execution["returncode"] == 0
        and prior["after_sha256"] == b["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav"))
        and receipt["sha256"] == a["audit"]["save_sha256"]
        == h.sha256(run / (after + ".sav"))
        and (run / "terravore-kira39-order-outpost-native-22901001.action.json").exists(),
    "same_day_exact_influence_and_alloy_payment_only":
        b["audit"]["date"] == a["audit"]["date"] == "2290.10.01"
        and delta["influence"] == D(-187) and delta["alloys"] == D(-100)
        and all(delta[k] == 0 for k in cash if k not in ("influence", "alloys"))
        and bc["budget_categories"]["current_month"]
            == ac["budget_categories"]["current_month"],
    "engineering_ship_has_single_reachable_unstarted_kira_outpost_order":
        q.block(b["fleets"]["2"], "current_order") == ""
        and q.block(a["fleets"]["2"], "order") == ""
        and q.ids(q.block(a["fleets"]["2"], "ships")) == [2]
        and q.scalars(q.block(q.block(a["fleets"]["2"], "movement_manager"), "coordinate"))["origin"] == 0
        and q.scalars(station)["progress"] == 0
        and q.scalars(station)["in_progress"] == "no"
        and q.scalars(station)["class"] == "shipclass_starbase"
        and q.scalars(q.block(station, "deposit_holder"))["id"] == 543
        and q.scalars(q.block(station, "resources"))
            == {"influence": 187, "alloys": 100}
        and q.scalars(q.block(q.block(q.block(station, "sub_order"),
                                    "move_to_system_point_order"), "coordinate"))["origin"] == 39
        and "can_reach=yes" in station
        and q.block(a["fleets"]["166"], "current_order") == ""
        and q.block(a["fleets"]["166"], "order") == "",
    "all_other_fleet_orders_memberships_and_eep_messages_error_stable":
        set(a["fleets"]) == set(b["fleets"])
        and set(a["ships"]) == set(b["ships"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships")) for k in b["fleets"])
        and all(q.block(b["fleets"][k], "current_order")
                == q.block(a["fleets"][k], "current_order")
                for k in b["fleets"] if k != "2")
        and all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["messages"] == b["messages"]
        and a["pending"] == b["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_PAID_OUTPOST_ORDER" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "cash_delta": {k: str(v) for k, v in delta.items()},
    "scope": "One paid native order; not yet arrival, construction start or completion.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
