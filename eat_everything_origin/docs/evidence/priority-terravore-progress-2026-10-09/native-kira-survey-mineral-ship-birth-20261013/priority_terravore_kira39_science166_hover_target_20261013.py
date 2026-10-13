"""Verify Kira's real native target while the original science ship is selected."""
import json
import logging
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
previous = "terravore-kira39-science166-selected-22881115"
stage = "terravore-kira39-science166-target-hover-22881115"
proof = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (previous + "-action-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "OBSERVED_NATIVE_SCIENCE166_SELECTED"
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
h.pyautogui.moveTo(*r.desktop_point(467, 608), duration=.2)
time.sleep(.7)
frame = r.gpu_capture(stage + "-tooltip")
assert frame["resolution"] == [1024, 768]
assert any(row["text"] == "2288.11.15" for row in frame["rows"])
assert any(row["text"] == "暂停" for row in frame["rows"])
assert any("德雷克" in row["text"] for row in frame["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_SCIENCE166_KIRA_TARGET_HOVER",
    "image_sha256": frame["image_sha256"],
    "hover_point": [467, 608],
    "date": "2288.11.15",
    "scope": "Target tooltip only; no route, survey or calendar.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_SCIENCE166_KIRA_TARGET_HOVER",
                  "image_sha256": frame["image_sha256"]},
                 ensure_ascii=False), flush=True)
