"""Approve only the first pre-contact native calendar interval toward Kira."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
start = "terravore-kira39-main83886903-ordered-22880902"
stage = "terravore-kira39-month1-22881001-preflight"
state = read_state(run, start)
audit = state["audit"]
country = audit["countries"]["0"]
proof = json.loads((run / (start + "-kira39-order-proof.json")).read_text("utf-8"))
execution = json.loads((run / (start + "-guard-execution.json")).read_text("utf-8"))
own = ["83886903", "917", "50332250"]
enemy = ["33554515", "854"]

def original_source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def origin(fleet):
    return q.scalars(q.block(q.block(fleet, "movement_manager"), "coordinate"))["origin"]

def own_route_ok(fid):
    fleet = state["fleets"][fid]
    order = q.block(q.block(fleet, "current_order"), "orbit_planet_order")
    movement = q.block(fleet, "movement_manager")
    return (origin(fleet) == 164
            and q.scalars(q.block(order, "orbitable")) == {"planet": 543}
            and q.scalars(order).get("can_reach") == "yes"
            and q.scalars(q.block(movement, "target_coordinate"))["origin"] == 39
            and not q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def enemy_idle_ok(fid):
    fleet = q.block(state["roots"]["fleet"], fid)
    movement = q.block(fleet, "movement_manager")
    return (origin(fleet) == 39 and len(q.ids(q.block(fleet, "ships"))) == 9
            and q.scalars(movement).get("state") == "move_idle"
            and not q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

head = q.scalars(state["items"]["117440553"])
queue_ids = q.ids(q.block(state["queues"]["0"], "items"))
delayed = [v for k, v, obj in q.fields(q.block(q.block(state["country"], "modules"),
                                         "standard_event_module"))
           if obj and k == "delayed_event"]
checks = {
    "main_order_8PASS_actual0_source_SAV":
        proof["status"] == "PASS_NATIVE_KIRA39_MAIN_ORDER_ALL_THREE_STAGED"
        and len(proof["checks"]) == 8 and all(v is True for v in proof["checks"].values())
        and original_source_ok(execution)
        and proof["after_sha256"] == audit["save_sha256"] == h.sha256(run / (start + ".sav")),
    "exact_first_native_29day_window":
        audit["date"] == "2288.09.02" and proof.get("boundaries", []) == []
        and head["progress"] == 338.8 and head["progress"] + 29 * 1.4 < 480,
    "all_three_original_fleets_still_moving_to_Kira":
        len(state["fleets"]) == 35 and len(state["ships"]) == 75
        and all(own_route_ok(fid) for fid in own),
    "two_hostile_crystal_fleets_idle_in_Kira": all(enemy_idle_ok(fid) for fid in enemy),
    "paid_hive_queue_below_completion_no_research_or_delayed_event":
        queue_ids == [117440553, 1476395019, 117440546]
        and all(q.scalars(q.block(state["items"][str(i)], "resources")) == {"minerals": 400}
                for i in queue_ids)
        and not country["research_queues"].get("society_queue")
        and not country["research_queues"].get("engineering_queue")
        and not delayed,
    "no_pending_message_current_battle_or_changed_menace":
        not state["pending"] and not state["messages"]
        and not any(q.ids(q.block(q.block(v, "combat"), "in_combat_with"))
                    for v in state["fleets"].values())
        and country["effective_stockpile"]["menace"] == 3065,
    "queen_EEP_crisis_state_held":
        all(country["variables"].get(k) == v for k, v in {
            "eep_c": 76, "eep_d": 21, "eep_crisis": 3, "eep_stage": 2,
            "eep_worlds": 5, "eep_fleet_stage": 3}.items()),
    "CN_production41_same_live_error":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7"
        and (user / "logs/error.log").read_bytes()
            == (run / (start + "-error-after.log")).read_bytes(),
}
passed = all(v is True for v in checks.values())
out = run / (stage + ".json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if passed else "FAIL",
    "checks": checks, "before_sha256": audit["save_sha256"],
    "after_sha256": audit["save_sha256"], "start_date": audit["date"],
    "end_date": "2288.10.01", "days": 29, "maximum_days": 29,
    "allowed_boundaries": [], "execution_stage": stage,
    "scope": "Only one 29-day native interval, no combat or construction completion accepted in advance.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True],
                  "start": audit["date"], "end": "2288.10.01"}), flush=True)
assert passed
