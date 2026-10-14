"""Resume only the unissued second return order after UI panel relocation."""
import json
import logging
import sys
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "hope-route-mar22-return2-native-22940322"
partial = json.loads((run / "hope-route-mar22-return-fleets-20261014-execution.json").read_text("utf-8"))
selection = json.loads((run / "hope-route-mar22-return-native-22940322-fleet2-selection.ocr.json").read_text("utf-8"))
tip = json.loads((run / "hope-route-mar22-fleet2-return-tooltip-ui-proof.json").read_text("utf-8"))
assert partial["returncode"] == 1 and h.sha256(Path(partial["command"][1])) == partial["helper_sha256"]
assert selection["image_sha256"] == h.sha256(run / "hope-route-mar22-return-native-22940322-fleet2-selection.jpg")
assert any(row["text"] == "第2舰队" and max(p[0] for p in row["box"]) < 300 for row in selection["rows"])
assert tip["pass"] and "返回" in tip["labels"] and "2294.03.22" in tip["labels"]
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
assert error == (run / "hope-route-mar22-market5000-native-22940322-error-after.log").read_bytes()
pre = r.gpu_capture(stage + "-before-second-order")
assert all(label in [row["text"] for row in pre["rows"]] for label in ("返回", "2294.03.22", "暂停"))
(run / (stage + "-error-before.log")).write_bytes(error)
r.gpu_click(94, 64, stage + "-return-fleet2")
r.gpu_capture(stage + "-after-second-order")
saved = r.native_save(stage, "2294.03.22", (0, 1, 15))
after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after)
print(json.dumps({"date": saved["date"], "save_sha256": saved["save_sha256"],
                  "error_unchanged": after == error}), flush=True)
assert after == error
