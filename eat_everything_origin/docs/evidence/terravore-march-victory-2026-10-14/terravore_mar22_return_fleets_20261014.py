"""Normal Chinese return orders for the two already selected combat fleets."""
import json
import logging
import sys

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "hope-route-mar22-return-native-22940322"
a = read_state(run, "hope-route-mar22-market5000-native-22940322")
proof = json.loads((run / "hope-route-mar22-market5000-guard-22940322-proof.json").read_text("utf-8"))
selected = json.loads((run / "hope-route-mar22-select-fleet3-ui-proof.json").read_text("utf-8"))
tip = json.loads((run / "hope-route-mar22-fleet3-return-tooltip-ui-proof.json").read_text("utf-8"))
assert proof["pass"] and proof["after_save_sha256"] == a["audit"]["save_sha256"]
assert selected["pass"] and "第3舰队" in selected["labels"] and tip["pass"] and "返回" in tip["labels"]
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
assert error == (run / "hope-route-mar22-market5000-native-22940322-error-after.log").read_bytes()
pre = r.gpu_capture(stage + "-before-orders")
assert all(label in [row["text"] for row in pre["rows"]] for label in ("2294.03.22", "暂停", "返回"))
(run / (stage + "-error-before.log")).write_bytes(error)
r.gpu_click(94, 191, stage + "-return-fleet3")
r.gpu_capture(stage + "-fleet3-returned-order")
r.gpu_click(887, 449, stage + "-select-fleet2")
selection = r.gpu_capture(stage + "-fleet2-selection")
header = [row["text"] for row in selection["rows"]
          if min(p[0] for p in row["box"]) < 300
          and 190 < min(p[1] for p in row["box"]) < 250]
assert "第2舰队" in header
r.gpu_click(94, 191, stage + "-return-fleet2")
r.gpu_capture(stage + "-fleet2-returned-order")
saved = r.native_save(stage, "2294.03.22", (0, 1, 15))
after_error = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after_error)
print(json.dumps({"date": saved["date"], "save_sha256": saved["save_sha256"],
                  "error_unchanged": error == after_error}), flush=True)
assert error == after_error
