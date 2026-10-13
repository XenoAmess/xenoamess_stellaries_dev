"""Audit Kira's native final battle report, original kills and paid losses."""
import json
import logging
import re
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
before = "terravore-kira39-battle-day13-native-22881114"
after = "terravore-kira39-battle-day14-native-22881115"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, stage) for stage in (before, after))
prior = load(before + "-first-enemy-fleet-cleared-proof.json")
review = load("terravore-kira39-battle-day14-22881115-last-enemy-preflight.json")
calendar = load(after + "-calendar-receipt.json")
observed = load(after + "-construction-boundary-observation-v4.json")
receipts = [load(stage + "-execution.json") for stage in [
    before + "-first-enemy-fleet-cleared-guard", review["execution_stage"],
    after + "-calendar", after + "-boundary-observation"]]

def objectives(s):
    return {q.scalars(raw)["objective"]: q.scalars(raw)["progress"]
            for key, raw, obj in q.fields(q.block(s["country"], "crisis_progression"))
            if key == "objective" and obj}

own = ["83886903", "917", "50332250"]
last_fleet = "33554515"
last_ship = "33554917"
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
bo, ao = objectives(b), objectives(a)
messages = [q.scalars(raw) for raw in a["messages"]]
message = a["messages"][0] if len(a["messages"]) == 1 else ""
stats = q.block(message, "combat_stats")
stats_fleets = q.block(stats, "fleets")
reported = [(fid, [int(x) for x in counts.split()]) for fid, counts in
            re.findall(r"\bfleet=(\d+).*?\bship_size_count_lost=\s*\{([^}]*)\}",
                       stats_fleets, re.S)]
original_counts = [(fid, [int(x) for x in counts.split()]) for fid, counts in
                   re.findall(r"\bfleet=(\d+).*?\bship_size_count=\s*\{([^}]*)\}",
                              stats_fleets, re.S)]
non_science = ["energy", "minerals", "food", "alloys", "unity",
               "rare_crystals", "influence", "trade"]
science = ["physics_research", "society_research", "engineering_research"]
checks = {
    "prior8_review7_observer6_actual0_sources_original_SAV":
        prior["status"] == "PASS_NATIVE_KIRA39_FIRST_ENEMY_FLEET_CLEARED"
        and [len(x["checks"]) for x in [prior, review, observed]] == [8, 7, 6]
        and all(v is True for proof in [prior, review, observed]
                for v in proof["checks"].values())
        and all(receipt["returncode"] == 0
                and receipt["helper_sha256"]
                    == h.sha256(Path(receipt["command"][1])) for receipt in receipts)
        and prior["after_sha256"] == b["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav"))
        and observed["after_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "exactly_one_normal_day_to_Nov15":
        b["audit"]["date"] == review["start_date"]
            == calendar["start_date"] == "2288.11.14"
        and a["audit"]["date"] == review["end_date"]
            == calendar["date"] == "2288.11.15"
        and review["days"] == calendar["days"] == 1
        and calendar["review_sha256"]
            == h.sha256(run / "terravore-kira39-battle-day14-22881115-last-enemy-preflight.json"),
    "last_original_enemy_ship_and_both_real_fleets_gone":
        q.ids(q.block(q.block(b["roots"]["fleet"], last_fleet), "ships"))
            == [int(last_ship)]
        and q.block(b["roots"]["ships"], last_ship)
        and not q.block(a["roots"]["ships"], last_ship)
        and not q.block(a["roots"]["fleet"], last_fleet)
        and not q.block(a["roots"]["fleet"], "854"),
    "all74_player_ships_35_fleets_own38_survivors_leave_combat_in39":
        len(b["ships"]) == len(a["ships"]) == 74
        and set(b["ships"]) == set(a["ships"])
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and set(b["fleets"]) == set(a["fleets"])
        and all(q.ids(q.block(old, "ships"))
                == q.ids(q.block(a["fleets"][fid], "ships"))
                for fid, old in b["fleets"].items())
        and {fid: len(q.ids(q.block(a["fleets"][fid], "ships"))) for fid in own}
            == {"83886903": 16, "917": 8, "50332250": 14}
        and all(not q.ids(q.block(q.block(a["fleets"][fid], "combat"),
                                  "in_combat_with"))
                and q.scalars(q.block(q.block(a["fleets"][fid],
                                      "movement_manager"), "coordinate"))["origin"] == 39
                for fid in own),
    "last_one_enemy_kill_15_native_objective_and_menace":
        ao["crisobj_destroy_enemy_ships"]
            - bo["crisobj_destroy_enemy_ships"] == 15
        and ac["effective_stockpile"]["menace"]
            - bc["effective_stockpile"]["menace"] == 15
        and ac["effective_stockpile"]["menace"] == sum(ao.values()) == 3335
        and {key: value for key, value in bo.items()
             if key != "crisobj_destroy_enemy_ships"}
            == {key: value for key, value in ao.items()
                if key != "crisobj_destroy_enemy_ships"},
    "one_vanilla_combat_report_no_more_enemies_and_only_fleet917_one_loss":
        len(messages) == 1
        and messages[0]["type"] == "COMBAT_STATS"
        and messages[0]["receiver"] == 0
        and messages[0]["date"] == "2288.11.14"
        and messages[0]["message_type"] == "combat_stats"
        and q.scalars(stats) == {"date": "2288.10.28", "reason": "no_more_enemies"}
        and sorted(reported) == sorted([("50332250", [0, 0]),
                                        ("83886903", [0]), ("917", [1])])
        and sorted(original_counts) == sorted([("50332250", [7, 7]),
                                               ("83886903", [16]), ("917", [9])])
        and not a["pending"],
    "no_same_day_cash_research_pop_jump_and_hive_queue_plus1point4":
        all(bc["effective_stockpile"][key] == ac["effective_stockpile"][key]
            for key in non_science)
        and all(bc["research_stockpile"][key] == ac["research_stockpile"][key]
                for key in science)
        and b["audit"]["colonies"]["0"]["actual_pop_sum"]
            == a["audit"]["colonies"]["0"]["actual_pop_sum"] == 13081
        and q.ids(q.block(b["queues"]["0"], "items"))
            == q.ids(q.block(a["queues"]["0"], "items"))
            == [117440553, 1476395019, 117440546]
        and D(str(q.scalars(a["items"]["117440553"])["progress"]))
            - D(str(q.scalars(b["items"]["117440553"])["progress"])) == D("1.4"),
    "EEP_queen_error_and_CN41_production_unchanged":
        bc["variables"] == ac["variables"]
        and (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes()
        and meta["language"] == "l_simp_chinese"
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-kira39-final-battle-victory-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FINAL_BATTLE_VICTORY" if passed else "FAIL",
    "checks": checks, "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"], "native_reported_losses": reported,
    "menace_delta": 15, "menace_after": 3335,
    "scope": "Kira's two original hostile fleets cleared; survey, mineral-ship replenishment and planet devour unaccepted.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]},
                 ensure_ascii=False), flush=True)
assert passed
