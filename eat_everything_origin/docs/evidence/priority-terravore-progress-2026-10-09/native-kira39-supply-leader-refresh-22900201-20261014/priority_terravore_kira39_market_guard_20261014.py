"""Verify two native market purchases without advancing the game calendar."""
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
before = "terravore-kira39-fullsystem-roll02-native-22891001"
after = "terravore-kira39-market-two-buys-22891001"
stage = "terravore-kira39-market-two-buys-guard-22891001"
out = run / (stage + "-proof.json")
assert not out.exists()
b, a = read_state(run, before), read_state(run, after)
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
prior = json.loads((run / "terravore-kira39-fullsystem-roll02-guard-22891001-proof.json").read_text("utf-8-sig"))
snapshot = json.loads((run / (after + ".native-save.json")).read_text("utf-8-sig"))

def targets(s):
    fleet = s["fleets"]["166"]
    order = q.block(fleet, "current_order")
    ids = re.findall(r"\bid=(\d+)", order + q.block(fleet, "order"))
    return list(map(int, ids)), q.scalars(q.block(order, "survey_planet_order")).get("progress")

old_targets, old_progress = targets(b)
new_targets, new_progress = targets(a)
cash = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
delta = {k: D(str(ac["effective_stockpile"].get(k, 0)))
         - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
checks = {
    "prior_fullsystem_guard_and_exact_native_sav_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and prior["after_sha256"] == b["audit"]["save_sha256"]
        and b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav"))
        and snapshot["save_sha256"] == a["audit"]["save_sha256"],
    "same_day_two_paid_1000_mineral_purchases":
        b["audit"]["date"] == a["audit"]["date"] == "2289.10.01"
        and delta["minerals"] == D("2000")
        and delta["trade"] == D("-3204.7535")
        and all(delta[k] == 0 for k in cash if k not in ("minerals", "trade"))
        and all((run / (name + ".action.json")).exists() for name in (
            "terravore-kira39-market-buy-1000-minerals-01-22891001",
            "terravore-kira39-market-buy-1000-minerals-02-22891001")),
    "survey_fleet_and_all_ship_memberships_unchanged":
        old_targets == new_targets and old_progress == new_progress
        and q.ids(q.block(a["fleets"]["166"], "ships")) == [1049]
        and set(a["fleets"]) == set(b["fleets"])
        and set(a["ships"]) == set(b["ships"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships")) for k in b["fleets"]),
    "budget_eep_pending_and_errors_unchanged":
        ac["budget_categories"]["current_month"] == bc["budget_categories"]["current_month"]
        and all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["pending"] == b["pending"] == []
        and a["messages"] == b["messages"] == []
        and (run / (before + "-error-after.log")).read_bytes()
        == (user / "logs/error.log").read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_MARKET_MINERAL_SUPPLY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "cash_delta": {k: str(v) for k, v in delta.items()},
    "survey_targets": new_targets,
    "survey_progress": new_progress,
    "scope": "Two normal domestic market purchases; same-day native save. Calendar not advanced.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
