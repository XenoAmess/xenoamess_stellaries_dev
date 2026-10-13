"""Permit exactly one native day in the already observed Kira battle."""
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
start = "terravore-kira39-month2-native-22881101"
stage = "terravore-kira39-battle-day1-22881102-preflight"
s = read_state(run, start)
audit = s["audit"]
country = audit["countries"]["0"]
proof = json.loads((run / (start + "-kira39-battle-entry-proof.json")).read_text("utf-8"))
execution = json.loads((run / (start + "-battle-entry-guard-execution.json")).read_text("utf-8"))
own = ["83886903", "917", "50332250"]
enemy = ["33554515", "854"]
enemy_ids = {int(i) for i in enemy}
own_ids = {int(i) for i in own}

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def source_ok(receipt):
    return (receipt["returncode"] == 0
            and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1])))

def own_ok(fid):
    fleet = s["fleets"][fid]
    movement = q.block(fleet, "movement_manager")
    expected = {"83886903": 16, "917": 9, "50332250": 14}[fid]
    return (len(q.ids(q.block(fleet, "ships"))) == expected
            and combat_ids(fleet) == enemy_ids
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 39)

def enemy_ok(fid):
    fleet = q.block(s["roots"]["fleet"], fid)
    movement = q.block(fleet, "movement_manager")
    return (len(q.ids(q.block(fleet, "ships"))) == 9
            and combat_ids(fleet) == own_ids
            and q.scalars(q.block(movement, "coordinate"))["origin"] == 39)

head = q.scalars(s["items"]["117440553"])
checks = {
    "battle_entry_13PASS_actual0_source_original_SAV":
        proof["status"] == "PASS_NATIVE_KIRA39_BATTLE_STARTED"
        and len(proof["checks"]) == 13
        and all(value is True for value in proof["checks"].values())
        and source_ok(execution)
        and proof["after_sha256"] == audit["save_sha256"]
            == h.sha256(run / (start + ".sav")),
    "only_Nov1_to_Nov2_one_native_day":
        audit["date"] == "2288.11.01"
        and proof["boundaries"] == ["active_kira39_combat_single_day_review"]
        and head["progress"] == 421.4 and head["progress"] + 1.4 < 480,
    "three_paid_original_fleets39_in_battle":
        len(s["fleets"]) == 35 and len(s["ships"]) == 75
        and all(own_ok(fid) for fid in own),
    "two_hostiles18_in_reciprocal_battle": all(enemy_ok(fid) for fid in enemy),
    "no_pending_research_build_or_cash_block":
        not s["pending"] and not s["messages"]
        and not country["research_queues"].get("society_queue")
        and not country["research_queues"].get("engineering_queue")
        and country["effective_stockpile"]["energy"] > 20000
        and country["effective_stockpile"]["minerals"] > 1000
        and country["effective_stockpile"]["alloys"] > 3000,
    "EEP_queen_crisis3_menace3065":
        all(country["variables"].get(k) == value for k, value in {
            "eep_c": 76, "eep_d": 21, "eep_crisis": 3,
            "eep_stage": 2, "eep_worlds": 5}.items())
        and country["effective_stockpile"]["menace"] == 3065,
    "CN41_production_and_live_error_same":
        meta["language"] == "l_simp_chinese" and meta["version"] == "0.2.0"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7"
        and (user / "logs/error.log").read_bytes()
            == (run / (start + "-error-after.log")).read_bytes(),
}
passed = all(value is True for value in checks.values())
out = run / (stage + ".json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if passed else "FAIL",
    "checks": checks, "before_sha256": audit["save_sha256"],
    "after_sha256": audit["save_sha256"], "start_date": audit["date"],
    "end_date": "2288.11.02", "days": 1, "maximum_days": 1,
    "allowed_boundaries": proof["boundaries"], "execution_stage": stage,
    "scope": "Only one active battle day. No victory or reward is presumed.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, v in checks.items() if v is not True],
                  "start": audit["date"], "end": "2288.11.02"}), flush=True)
assert passed
