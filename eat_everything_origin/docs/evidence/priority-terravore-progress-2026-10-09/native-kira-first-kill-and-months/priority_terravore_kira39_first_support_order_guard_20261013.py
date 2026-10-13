"""Verify one normal paid mineral fleet order from Veyer to Kira, same date."""
import json
import logging
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "eat_everything_origin/tools")
sys.path.insert(0, "_runtime/heart-of-devouring")
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import omit, read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-support50332250-first-order-attempt"
after = "terravore-kira39-support50332250-ordered-22880902"
old, new = (read_state(run, name) for name in [before, after])
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
ack = load("terravore-project3-crisis4130-ack-22880902-event-ack-v2-proof.json")
ack_run = load("terravore-project3-crisis4130-ack-22880902-guard-v2-execution.json")
first_save = load(before + "-save-execution.json")
second_save = load(after + "-save-execution.json")
click = load("terravore-kira39-support50332250-star-order-22880902-execution.json")
hover = load("terravore-kira39-support50332250-star-center-hover.ocr.json")
route_ui = load("terravore-kira39-support50332250-star-order-result-ui.ocr.json")

def checked(receipt):
    return receipt["returncode"] == 0 and receipt["helper_sha256"] == h.sha256(
        Path(receipt["command"][1]))

bf, af = old["fleets"]["50332250"], new["fleets"]["50332250"]
bm, am = q.block(bf, "movement_manager"), q.block(af, "movement_manager")
order = q.block(q.block(af, "current_order"), "orbit_planet_order")
sub = q.block(q.block(order, "sub_order"), "move_to_system_point_order")
path = q.block(am, "path")
nodes = [(q.scalars(q.block(value, "coordinate"))["origin"],
          q.scalars(value).get("ftl")) for key, value, obj in q.fields(path)
         if key == "node" and obj]
old_planets, new_planets = (
    {key: value for key, value, obj in q.fields(q.block(state["roots"]["planets"], "planet"))
     if obj} for state in [old, new])
old_p, new_p = old_planets["1732"], new_planets["1732"]
changed_roots = {key for key in old["roots"] | new["roots"]
                 if old["roots"].get(key) != new["roots"].get(key)}
metadata = {"save", "save_sha256", "gamestate_sha256", "gamestate_bytes"}
checks = {
    "prior_ack_v2_10PASS_and_first_noop_save_exact_original_SHA":
        ack["status"] == "PASS_NATIVE_PROJECT3_HIVE_EVENT_ACK"
        and len(ack["checks"]) == 10 and all(x is True for x in ack["checks"].values())
        and checked(ack_run) and checked(first_save)
        and ack["after_sha256"] == old["audit"]["save_sha256"]
        and h.sha256(run / (before + ".sav")) == old["audit"]["save_sha256"],
    "normal_CN_UI_star_hover_route_and_same_date_save_actual0":
        meta["language"] == "l_simp_chinese"
        and all(checked(x) for x in [click, second_save])
        and old["audit"]["date"] == new["audit"]["date"] == "2288.09.02"
        and new["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and any(x["text"] == "奇拉" and x["score"] >= .9 for x in hover["rows"])
        and any("正在前往奇拉星系" in x["text"] and x["score"] >= .8
                for x in route_ui["rows"])
        and all(frame["image_sha256"] == h.sha256(Path(frame["image"]))
                for frame in [hover, route_ui]),
    "only_planets_and_fleet_roots_exact_other_country_raw_held":
        changed_roots == {"planets", "fleet"}
        and old["country"] == new["country"]
        and omit(old["roots"]["fleet"], {"50332250"})
            == omit(new["roots"]["fleet"], {"50332250"})
        and omit(old["roots"]["planets"], {"planet"})
            == omit(new["roots"]["planets"], {"planet"}),
    "only_original_14_ship_fleet_order_changed_all75_ships_held":
        len(old["ships"]) == len(new["ships"]) == 75
        and old["ships"] == new["ships"]
        and len(old["fleets"]) == len(new["fleets"]) == 35
        and {key for key in old["fleets"]
             if old["fleets"][key] != new["fleets"][key]} == {"50332250"}
        and omit(bf, {"auto_movement", "movement_manager", "order_id", "current_order"})
            == omit(af, {"auto_movement", "movement_manager", "order_id", "current_order"})
        and q.scalars(af)["order_id"] == q.scalars(bf)["order_id"] + 1 == 6,
    "only_planet1732_old_paid_orbit_index2_released":
        old_planets.keys() == new_planets.keys()
        and {key for key in old_planets if old_planets[key] != new_planets[key]}
            == {"1732"}
        and omit(old_p, {"planet_orbitals"}) == omit(new_p, {"planet_orbitals"})
        and q.scalars(q.block(old_p, "planet_orbitals"))
            == {"0": 83886903, "1": 917, "2": 50332250}
        and q.scalars(q.block(new_p, "planet_orbitals"))
            == {"0": 83886903, "1": 917},
    "new_native_orbit_order_Kira_star543_can_reach_and_direct_hyperlane":
        not q.block(bf, "current_order")
        and q.scalars(q.block(bf, "auto_movement"))
            == {"type": "auto_move_planet", "auto_move_target": 1732,
                "clear_on_new_orders": "yes", "has_arrived": "yes"}
        and not q.block(af, "auto_movement")
        and q.scalars(q.block(bm, "coordinate"))["origin"]
            == q.scalars(q.block(am, "coordinate"))["origin"] == 164
        and q.scalars(q.block(order, "orbitable"))
            == q.scalars(q.block(order, "star")) == {"planet": 543}
        and q.scalars(order)["can_reach"] == q.scalars(sub)["can_reach"] == "yes"
        and q.scalars(q.block(sub, "coordinate"))
            == q.scalars(q.block(am, "target_coordinate"))
            == {"x": 12.6, "y": 12.6, "origin": 39}
        and nodes == [(164, "jump_hyperlane"), (39, "jump_hyperlane"),
                      (39, "jump_hyperlane")]
        and q.scalars(path)["date"] == "2288.11.23"
        and re.search(r"\bto\s*=\s*39\b",
                      q.block(q.block(new["roots"]["galactic_object"], "164"),
                              "hyperlane")) is not None,
    "all_business_audit_messages_pending_error_and_mod_held":
        all(value == new["audit"].get(key) for key, value in old["audit"].items()
            if key not in metadata)
        and old["messages"] == new["messages"]
        and old["pending"] == new["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes()
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(value is True for value in checks.values())
out = run / (after + "-kira39-order-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FIRST_PAID_SUPPORT_ORDER" if passed else "FAIL",
    "checks": checks, "before_sha256": old["audit"]["save_sha256"],
    "after_sha256": new["audit"]["save_sha256"], "date": new["audit"]["date"],
    "changed_roots": sorted(changed_roots), "route_nodes": nodes,
    "future_ui_eta_not_arrival_proof": q.scalars(path)["date"],
    "scope": "One actual paid mineral fleet order only; two other player fleets remain at 164.",
    "native_devour_calendar_ready": False, "maximum_days_to_native_bite_boundary": 0,
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]}), flush=True)
assert passed
