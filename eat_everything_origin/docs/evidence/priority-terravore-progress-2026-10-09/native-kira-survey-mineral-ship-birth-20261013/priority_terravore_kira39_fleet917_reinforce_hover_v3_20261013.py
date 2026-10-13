"""Read the fleet manager's top reinforcement button tooltip."""
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
previous = "terravore-kira39-postvictory-fleet917-row-hover-v2-22881115"
stage = "terravore-kira39-postvictory-manager-top-hover-v3-22881115"
proof = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
execution = json.loads((run / (previous + "-action-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "OBSERVED_NATIVE_FLEET917_ROW_TOOLTIP"
assert execution["returncode"] == 0
assert execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
h.pyautogui.moveTo(*r.desktop_point(685, 88), duration=.2)
time.sleep(.7)
frame = r.gpu_capture(stage + "-tooltip")
assert frame["resolution"] == [1024, 768]
assert any(row["text"] == "2288.11.15" for row in frame["rows"])
assert any(row["text"] == "暂停" for row in frame["rows"])
assert any(row["text"] == "舰队管理" for row in frame["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_MANAGER_TOP_TOOLTIP",
    "image_sha256": frame["image_sha256"],
    "hover_point": [685, 88],
    "date": "2288.11.15",
    "scope": "Tooltip only; no click, payment or construction order.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_MANAGER_TOP_TOOLTIP",
                  "image_sha256": frame["image_sha256"]},
                 ensure_ascii=False), flush=True)
