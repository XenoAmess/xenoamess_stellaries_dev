"""Verify main fleet's normal Kira order with both paid supports already ordered."""
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
before = "terravore-kira39-support917-ordered-22880902"
after = "terravore-kira39-main83886903-ordered-22880902"
b, a = (read_state(run, stage) for stage in [before, after])
load = lambda stage: json.loads((run / stage).read_text("utf-8-sig"))
first = load(before + "-kira39-order-proof.json")
first_run = load(before + "-guard-execution.json")
click = load("terravore-kira39-main83886903-order39-22880902-execution.json")
save = load(after + "-save-execution.json")
hover = load("terravore-kira39-main83886903-correct-star-hover.ocr.json")
route = load("terravore-kira39-main83886903-order-result-ui.ocr.json")
checked = lambda receipt: receipt["returncode"] == 0 and receipt["helper_sha256"] == h.sha256(
    Path(receipt["command"][1]))
bf, af = b["fleets"]["83886903"], a["fleets"]["83886903"]
bm, am = q.block(bf, "movement_manager"), q.block(af, "movement_manager")
order = q.block(q.block(af, "current_order"), "orbit_planet_order")
sub = q.block(q.block(order, "sub_order"), "move_to_system_point_order")
path = q.block(am, "path")
nodes = [q.scalars(q.block(v, "coordinate"))["origin"]
         for k, v, obj in q.fields(path) if k == "node" and obj]
bp, ap = ({k: v for k, v, obj in q.fields(q.block(s["roots"]["planets"], "planet"))
           if obj} for s in [b, a])
changed_roots = {k for k in b["roots"] | a["roots"]
                 if b["roots"].get(k) != a["roots"].get(k)}
metadata = {"save", "save_sha256", "gamestate_sha256", "gamestate_bytes"}
checks = {
    "prior_second_support_7PASS_source_SAV_and_native_main_click_save":
        first["status"] == "PASS_NATIVE_KIRA39_SECOND_PAID_SUPPORT_ORDER"
        and len(first["checks"]) == 7 and all(v is True for v in first["checks"].values())
        and checked(first_run) and checked(click) and checked(save)
        and first["after_sha256"] == b["audit"]["save_sha256"]
        and b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and b["audit"]["date"] == a["audit"]["date"] == "2288.09.02",
    "Chinese_target_star_and_selected_main16_fleet_UI":
        meta["language"] == "l_simp_chinese"
        and any(v["text"] == "奇拉" and v["score"] >= .9 for v in hover["rows"])
        and any(v["text"] == "第7舰队" and v["box"][0][0] < 400
                and v["score"] >= .9 for v in hover["rows"])
        and any("正在前往奇拉星系" in v["text"] and v["score"] >= .8
                for v in route["rows"])
        and all(x["image_sha256"] == h.sha256(Path(x["image"])) for x in [hover, route]),
    "only_fleet_and_planets_raw_changed_all_country_and_other_roots_held":
        changed_roots == {"fleet", "planets"}
        and b["country"] == a["country"]
        and omit(b["roots"]["fleet"], {"83886903"})
            == omit(a["roots"]["fleet"], {"83886903"})
        and omit(b["roots"]["planets"], {"planet"})
            == omit(a["roots"]["planets"], {"planet"}),
    "only_main83886903_of35_and_all75_original_ships_exact_held":
        len(b["ships"]) == len(a["ships"]) == 75 and b["ships"] == a["ships"]
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and {k for k in b["fleets"] if b["fleets"][k] != a["fleets"][k]} == {"83886903"}
        and omit(bf, {"auto_movement", "movement_manager", "order_id", "current_order"})
            == omit(af, {"auto_movement", "movement_manager", "order_id", "current_order"})
        and q.scalars(af)["order_id"] == q.scalars(bf)["order_id"] + 1 == 6,
    "only_original_planet1732_main_orbit_index0_released":
        bp.keys() == ap.keys()
        and {k for k in bp if bp[k] != ap[k]} == {"1732"}
        and omit(bp["1732"], {"planet_orbitals"})
            == omit(ap["1732"], {"planet_orbitals"})
        and q.scalars(q.block(bp["1732"], "planet_orbitals"))
            == {"0": 83886903}
        and q.scalars(q.block(ap["1732"], "planet_orbitals")) == {},
    "native_direct_Kira39_order_route_can_reach_and_actual_position164":
        not q.block(bf, "current_order") and not q.block(af, "auto_movement")
        and q.scalars(q.block(bm, "coordinate"))["origin"]
            == q.scalars(q.block(am, "coordinate"))["origin"] == 164
        and q.scalars(q.block(order, "orbitable"))
            == q.scalars(q.block(order, "star")) == {"planet": 543}
        and q.scalars(order)["can_reach"] == q.scalars(sub)["can_reach"] == "yes"
        and q.scalars(q.block(sub, "coordinate"))
            == q.scalars(q.block(am, "target_coordinate"))
            == {"x": 12.6, "y": 12.6, "origin": 39}
        and nodes == [164, 39, 39]
        and q.scalars(path)["date"] == "2288.11.23"
        and re.search(r"\bto\s*=\s*39\b",
                      q.block(q.block(a["roots"]["galactic_object"], "164"),
                              "hyperlane")) is not None,
    "all_business_audit_notifications_error_and_production_mod_held":
        all(v == a["audit"].get(k) for k, v in b["audit"].items() if k not in metadata)
        and b["messages"] == a["messages"] and b["pending"] == a["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes()
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
    "all_three_normal_paid_military_fleets_have_Kira_orders_no_calendar":
        all(q.scalars(q.block(q.block(q.block(a["fleets"][fid], "current_order"),
                                    "orbit_planet_order"), "orbitable")) == {"planet": 543}
            and q.scalars(q.block(q.block(a["fleets"][fid], "movement_manager"),
                                  "target_coordinate"))["origin"] == 39
            and q.scalars(q.block(q.block(a["fleets"][fid], "movement_manager"),
                                  "coordinate"))["origin"] == 164
            for fid in ["83886903", "917", "50332250"])
        and q.scalars(q.block(q.block(a["fleets"]["917"], "movement_manager"),
                              "path"))["date"] == "2288.11.22"
        and q.scalars(q.block(q.block(a["fleets"]["50332250"], "movement_manager"),
                              "path"))["date"] == "2288.11.23",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-kira39-order-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_MAIN_ORDER_ALL_THREE_STAGED" if passed else "FAIL",
    "checks": checks, "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"], "date": a["audit"]["date"],
    "changed_roots": sorted(changed_roots), "route_nodes": nodes,
    "future_eta_not_arrival_proof": q.scalars(path)["date"],
    "scope": "All three normally ordered at the same paused date; future travel and combat unaccepted.",
    "native_devour_calendar_ready": False, "maximum_days_to_native_bite_boundary": 0,
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed
