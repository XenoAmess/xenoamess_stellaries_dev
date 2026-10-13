"""Review one bounded native Kira full-system survey interval before GUI input."""
import json
import logging
import re
import sys
from pathlib import Path

before, end, raw_days, stage, prior_proof_file, prior_execution_stage = sys.argv[1:]
days = int(raw_days)
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state
import priority_terravore_vanilla_leader_message_20261014 as vanilla

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
out = run / (stage + "-review.json")
assert not out.exists()
frozen = run / Path(vanilla.__file__).name
raw = Path(vanilla.__file__).read_bytes()
if frozen.exists(): assert frozen.read_bytes() == raw
else: frozen.write_bytes(raw)
s = read_state(run, before)
prior = json.loads((run / prior_proof_file).read_text("utf-8-sig"))
execution = json.loads((run / (prior_execution_stage + "-execution.json")).read_text("utf-8-sig"))
science = s["fleets"]["166"]
move = q.block(science, "movement_manager")
reinforcement = s["fleets"]["50331731"]
cash = s["audit"]["countries"]["0"]["effective_stockpile"]
original = [546, 545, 552, 553, 547, 543, 549, 554, 555, 550, 551, 548]
current = list(map(int, re.findall(r"\bid=(\d+)", q.block(science, "current_order"))))
queued = list(map(int, re.findall(r"\bid=(\d+)", q.block(science, "order"))))
remaining = current + queued

def ordinal(date):
    year, month, day = map(int, date.split("."))
    assert 1 <= month <= 12 and 1 <= day <= 30
    return (year * 12 + month - 1) * 30 + day - 1

start_date = s["audit"]["date"]
start_parts, end_parts = (list(map(int, x.split("."))) for x in (start_date, end))
same_month = start_parts[:2] == end_parts[:2]
one_boundary_to_first = end_parts[2] == 1 and ordinal(end) - ordinal(start_date) == days
checks = {
    "prior_pass_actual0_source_and_exact_start_sav":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == s["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav")),
    "one_bounded_interval_no_pending_error":
        1 <= days <= 30 and ordinal(end) - ordinal(start_date) == days
        and (same_month or one_boundary_to_first)
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == [] and vanilla.admissible(s["messages"])
        and (run / (before + "-error-after.log")).read_bytes()
        == (user / "logs/error.log").read_bytes(),
    "science_ship_in_39_original_ordered_suffix":
        q.scalars(q.block(move, "coordinate"))["origin"] == 39
        and len(current) == 1 and current[0] in original
        and remaining == original[original.index(current[0]):]
        and len(set(remaining)) == len(remaining)
        and "survey_planet_order" in q.block(science, "current_order")
        and "can_reach=yes" in q.block(science, "current_order")
        and q.ids(q.block(science, "ships")) == [1049],
    "paid_crisis_destroyer_still_mia_with_ship_membership":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8
        and len(s["ships"]) == 75,
    "cash_runway":
        cash["energy"] > 1000 and cash["minerals"] > 300,
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": prior["after_sha256"],
    "after_sha256": prior["after_sha256"],
    "start_date": start_date,
    "end_date": end,
    "days": days,
    "maximum_days": days,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["fullsystem_survey_ordered_suffix", "at_most_one_monthly_budget", "mia_reinforcement"],
    "execution_stage": stage,
    "route_origin": 39,
    "remaining_targets": remaining,
    "scope": "One at-most-30-day native full-system survey interval. Any event or order/budget divergence requires independent postcheck.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
