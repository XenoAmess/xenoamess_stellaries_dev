"""Independent same-date native market payment and Mod-state guard."""
import json
import logging
import sys
from decimal import Decimal
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
start, stage = "hope-route-mar22-native-22940322", "hope-route-mar22-market5000-native-22940322"
a, b = read_state(run, start), read_state(run, stage)
prior = json.loads((run / "hope-route-mar22-victory-guard-22940322-proof.json").read_text("utf-8"))
execution = json.loads((run / "hope-route-mar22-market5000-20261014-execution.json").read_text("utf-8"))
action = json.loads((run / (stage + "-action-proof.json")).read_text("utf-8"))
click = json.loads((run / (stage + "-buy.action.json")).read_text("utf-8"))
result = json.loads((run / (stage + "-purchase-result.ocr.json")).read_text("utf-8"))
ac, bc = a["audit"]["countries"]["0"], b["audit"]["countries"]["0"]
resources = set(ac["effective_stockpile"]) | set(bc["effective_stockpile"])
delta = {resource: Decimal(str(bc["effective_stockpile"].get(resource, 0)))
         - Decimal(str(ac["effective_stockpile"].get(resource, 0))) for resource in resources}
labels = [row["text"] for row in result["rows"]]
checks = {
    "source_native_same_date": prior["pass"] and execution["returncode"] == 0
    and h.sha256(Path(execution["command"][1])) == execution["helper_sha256"]
    and prior["after_save_sha256"] == a["audit"]["save_sha256"] == action["before_save_sha256"]
    and b["audit"]["save_sha256"] == action["after_save_sha256"]
    and h.sha256(run / (start + ".sav")) == a["audit"]["save_sha256"]
    and h.sha256(run / (stage + ".sav")) == b["audit"]["save_sha256"]
    and a["audit"]["date"] == b["audit"]["date"] == "2294.03.22"
    and meta["language"] == "l_simp_chinese",
    "single_quoted_5000_purchase": click["client_point"] == [76, 407]
    and action["quoted_minerals"] == 5000 and action["quoted_trade"] == 15032
    and result["image_sha256"] == action["result_image_sha256"]
    and any("购买矿物的总额：14500" in label for label in labels),
    "exact_minerals_trade_only": delta["minerals"] == 5000
    and abs(delta["trade"] + Decimal(15032)) <= 1
    and delta["trade"] < 0 and bc["effective_stockpile"]["trade"] > 0
    and all(value == 0 for resource, value in delta.items() if resource not in ("minerals", "trade"))
    and ac["budget_categories"]["current_month"] == bc["budget_categories"]["current_month"],
    "ships_fleets_orders_construction_held": a["ships"] == b["ships"]
    and a["fleets"] == b["fleets"] and a["queues"] == b["queues"] and a["items"] == b["items"],
    "mod_colonies_native_crisis_held": ac["variables"] == bc["variables"]
    and ac["owned_colonies"] == bc["owned_colonies"] == [0, 40]
    and a["audit"]["colonies"] == b["audit"]["colonies"]
    and q.block(a["country"], "crisis_progression") == q.block(b["country"], "crisis_progression"),
    "messages_pending_error_held": a["messages"] == b["messages"]
    and a["pending"] == b["pending"] == []
    and (run / (stage + "-error-before.log")).read_bytes()
    == (run / (stage + "-error-after.log")).read_bytes()
    == (user / "logs/error.log").read_bytes(),
}
proof = {"stage": "hope-route-mar22-market5000-guard-22940322", "pass": all(checks.values()),
         "before_save_sha256": a["audit"]["save_sha256"],
         "after_save_sha256": b["audit"]["save_sha256"], "checks": checks,
         "cash_delta": {resource: str(value) for resource, value in delta.items() if value != 0},
         "minerals_after": bc["effective_stockpile"]["minerals"],
         "trade_after": bc["effective_stockpile"]["trade"]}
out = run / (proof["stage"] + "-proof.json")
assert not out.exists()
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
sys.exit(0 if proof["pass"] else 1)
