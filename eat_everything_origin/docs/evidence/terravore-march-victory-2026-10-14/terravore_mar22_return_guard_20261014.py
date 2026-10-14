"""Same-date two-fleet return-order and owned repair-base guard."""
import json
import logging
import sys
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
a = read_state(run, "hope-route-mar22-market5000-native-22940322")
b = read_state(run, "hope-route-mar22-return2-native-22940322")
prior = json.loads((run / "hope-route-mar22-market5000-guard-22940322-proof.json").read_text("utf-8"))
partial = json.loads((run / "hope-route-mar22-return-fleets-20261014-execution.json").read_text("utf-8"))
resume = json.loads((run / "hope-route-mar22-return-resume-20261014-execution.json").read_text("utf-8"))
ac, bc = a["audit"]["countries"]["0"], b["audit"]["countries"]["0"]
target_base = q.scalars(q.block(q.block(b["roots"]["starbase_mgr"], "starbases"), "153"))
orders = {fid: q.block(b["fleets"][fid], "current_order") for fid in ("50332250", "917")}
checks = {
    "bound_native_same_date_sources": meta["language"] == "l_simp_chinese" and prior["pass"]
    and a["audit"]["save_sha256"] == prior["after_save_sha256"]
    and a["audit"]["date"] == b["audit"]["date"] == "2294.03.22"
    and partial["returncode"] == 1 and resume["returncode"] == 0
    and all(h.sha256(Path(e["command"][1])) == e["helper_sha256"] for e in (partial, resume))
    and h.sha256(run / "hope-route-mar22-return2-native-22940322.sav") == b["audit"]["save_sha256"],
    "two_exact_owned_base_return_orders": all(
        "return_fleet_order" in order and "starbase=153" in order
        and "home_base=yes" in order and "origin=97" in order and "can_reach=yes" in order
        for order in orders.values())
    and str(target_base["station"]) in b["ships"]
    and all(omit(a["fleets"][fid], {"order_id", "current_order", "movement_manager"})
            == omit(b["fleets"][fid], {"order_id", "current_order", "movement_manager"})
            for fid in orders)
    and len(q.ids(q.block(b["fleets"]["50332250"], "ships"))) == 13
    and len(q.ids(q.block(b["fleets"]["917"], "ships"))) == 9,
    "all_ships_other_fleets_construction_held": a["ships"] == b["ships"]
    and set(a["fleets"]) == set(b["fleets"])
    and all(a["fleets"][fid] == b["fleets"][fid] for fid in a["fleets"] if fid not in orders)
    and a["queues"] == b["queues"] and a["items"] == b["items"],
    "resources_colonies_mod_and_crisis_held": ac["effective_stockpile"] == bc["effective_stockpile"]
    and ac["variables"] == bc["variables"] and ac["owned_colonies"] == bc["owned_colonies"] == [0, 40]
    and a["audit"]["colonies"] == b["audit"]["colonies"]
    and q.block(a["country"], "crisis_progression") == q.block(b["country"], "crisis_progression"),
    "messages_pending_error_held": a["messages"] == b["messages"]
    and a["pending"] == b["pending"] == []
    and (run / "hope-route-mar22-return2-native-22940322-error-before.log").read_bytes()
    == (run / "hope-route-mar22-return2-native-22940322-error-after.log").read_bytes()
    == (user / "logs/error.log").read_bytes(),
}
proof = {"stage": "hope-route-mar22-return-guard-22940322", "pass": all(checks.values()),
         "before_save_sha256": a["audit"]["save_sha256"],
         "after_save_sha256": b["audit"]["save_sha256"], "checks": checks,
         "target_base": 153, "target_system": 97,
         "fleet_etas": {fid: q.scalars(q.block(q.block(b["fleets"][fid], "movement_manager"), "path")).get("date")
                        for fid in orders}}
out = run / (proof["stage"] + "-proof.json")
assert not out.exists()
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
sys.exit(0 if proof["pass"] else 1)
