"""One explicitly quoted native mineral purchase, followed by native save."""
import json
import logging
import sys
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "hope-route-mar22-market5000-native-22940322"
a = read_state(run, "hope-route-mar22-native-22940322")
prior = json.loads((run / "hope-route-mar22-victory-guard-22940322-proof.json").read_text("utf-8"))
quote = json.loads((run / "hope-route-mar22-market-quote5000-ui-proof.json").read_text("utf-8"))
execution = json.loads((run / "hope-route-mar22-market-quote5000-20261014-execution.json").read_text("utf-8"))
assert prior["pass"] and quote["pass"] and execution["returncode"] == 0
assert a["audit"]["save_sha256"] == prior["after_save_sha256"]
assert execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
assert quote["image_sha256"] == h.sha256(run / "hope-route-mar22-market-quote5000-after.jpg")
required = ("购买5000.00矿物", "获得：5000", "失去：15032", "国内贸易市场", "2294.03.22", "暂停")
assert all(label in quote["labels"] for label in required)
assert a["audit"]["countries"]["0"]["effective_stockpile"]["trade"] > 15032
assert a["audit"]["countries"]["0"]["effective_stockpile"]["minerals"] == 485.93268
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
assert error == (run / "hope-route-mar22-native-22940322-error-after.log").read_bytes()
pre = r.gpu_capture(stage + "-quote-preflight")
assert all(label in [row["text"] for row in pre["rows"]] for label in required)
(run / (stage + "-error-before.log")).write_bytes(error)
r.gpu_click(76, 407, stage + "-buy")
h.pyautogui.moveTo(*r.desktop_point(730, 625), duration=0.2)
result = r.gpu_capture(stage + "-purchase-result")
saved = r.native_save(stage, "2294.03.22", (0, 1, 15))
after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after)
h.write_json(run / (stage + "-action-proof.json"), {
    "before_save_sha256": a["audit"]["save_sha256"],
    "after_save_sha256": saved["save_sha256"], "quoted_minerals": 5000,
    "quoted_trade": 15032, "quote_image_sha256": pre["image_sha256"],
    "result_image_sha256": result["image_sha256"], "date": saved["date"],
    "error_unchanged": after == error,
    "scope": "Single normal purchase; independent saved-state postcondition required."})
print(json.dumps({"date": saved["date"], "save_sha256": saved["save_sha256"],
                  "error_unchanged": after == error}), flush=True)
assert after == error
