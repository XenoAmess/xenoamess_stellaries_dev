"""Validate one bounded native Kira full-system survey interval."""
import json
import logging
import re
import sys
from decimal import Decimal as D
from pathlib import Path

before, after, stage, prior_proof_file, review_stage = sys.argv[1:]
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
out = run / (stage + "-proof.json")
assert not out.exists()
frozen = run / Path(vanilla.__file__).name
raw = Path(vanilla.__file__).read_bytes()
if frozen.exists(): assert frozen.read_bytes() == raw
else: frozen.write_bytes(raw)
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
prior, review = load(prior_proof_file), load(review_stage + "-review.json")
calendar, execution = load(after + "-calendar-receipt.json"), load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
old, new = (s["fleets"]["166"] for s in (b, a))
old_order, new_order = (q.block(f, "current_order") for f in (old, new))
target = lambda f: list(map(int, re.findall(r"\bid=(\d+)", q.block(f, "current_order"))))
queue = lambda f: list(map(int, re.findall(r"\bid=(\d+)", q.block(f, "order"))))
old_targets, new_targets = target(old) + queue(old), target(new) + queue(new)
consumed = len(old_targets) - len(new_targets)
original = [546, 545, 552, 553, 547, 543, 549, 554, 555, 550, 551, 548]
crossed = b["audit"]["date"][:7] != a["audit"]["date"][:7]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
budget = ac["budget_categories"]["current_month"]
net = {k: sum((D(str(v.get(k, 0))) for v in budget["income"].values()), D(0))
       - sum((D(str(v.get(k, 0))) for v in budget["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
stable_cash = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
reinforcement = a["fleets"]["50331731"]
checks = {
    "prior_review_calendar_actual0_exact_sav_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and review["remaining_targets"] == old_targets
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == review["days"]
        and (calendar["start_date"], calendar["date"])
        == (b["audit"]["date"], a["audit"]["date"])
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == review["after_sha256"] == b["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "survey_keeps_original_ordered_suffix_and_consumes_at_most_one":
        old_targets and old_targets == original[original.index(old_targets[0]):]
        and 0 <= consumed <= 1
        and new_targets == old_targets[consumed:]
        and (not new_targets or
             (len(target(new)) == 1
              and "survey_planet_order" in new_order
              and "can_reach=yes" in new_order))
        and (consumed > 0 or
             D(str(q.scalars(q.block(new_order, "survey_planet_order")).get("progress", 0)))
             >= D(str(q.scalars(q.block(old_order, "survey_planet_order")).get("progress", 0))))
        and q.scalars(q.block(q.block(new, "movement_manager"), "coordinate"))["origin"] == 39
        and q.ids(q.block(new, "ships")) == [1049]
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
        == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "same_month_cash_or_one_exact_monthly_budget":
        ((not crossed
          and all(ac["effective_stockpile"].get(k) == bc["effective_stockpile"].get(k)
                  for k in stable_cash)
          and ac["budget_categories"]["current_month"]
              == bc["budget_categories"]["current_month"])
         or (crossed and a["audit"]["date"].endswith(".01")
             and all(abs(v) <= D("0.00002") for v in residual.values())
             and ac["budget_categories"]["last_month"]
             == bc["budget_categories"]["current_month"])),
    "paid_reinforcement_all_ship_memberships_stable":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and q.scalars(q.block(q.block(reinforcement, "current_order"), "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships")) for k in b["fleets"]),
    "eep_pending_reviewed_vanilla_message_error_stable":
        all(ac["variables"].get(k) == bc["variables"].get(k)
            for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["pending"] == b["pending"] == []
        and vanilla.transition(b["messages"], a["messages"], a["audit"]["date"])
        and (run / (after + "-error-before.log")).read_bytes()
        == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_FULLSYSTEM_SURVEY_ROLL" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "old_targets": old_targets,
    "new_targets": new_targets,
    "consumed_targets": old_targets[:consumed] if 0 <= consumed <= len(old_targets) else [],
    "current_progress": q.scalars(q.block(new_order, "survey_planet_order")).get("progress"),
    "crossed_month": crossed,
    "cash_residuals": {k: str(v) for k, v in residual.items()} if crossed else None,
    "scope": "One bounded native full-system survey window; at most one queued body consumed and one monthly settlement. Outpost still needs UI acceptance.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
