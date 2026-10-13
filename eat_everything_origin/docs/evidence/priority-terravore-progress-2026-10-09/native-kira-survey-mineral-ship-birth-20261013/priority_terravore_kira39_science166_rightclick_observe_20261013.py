"""Read native UI after one science-ship right click on Kira."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
hover = "terravore-kira39-science166-target-hover-22881115"
click = "terravore-kira39-science166-target-rightclick-22881115"
stage = "terravore-kira39-science166-rightclick-observed-22881115"
hover_proof = json.loads((run / (hover + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (click + "-wrapper-execution.json")).read_text("utf-8-sig"))
action = json.loads((run / (click + ".action.json")).read_text("utf-8-sig"))
assert hover_proof["status"] == "OBSERVED_NATIVE_SCIENCE166_KIRA_TARGET_HOVER"
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert action["action"] == "right-click" and action["client_point"] == [467, 608]
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
frame = r.gpu_capture(stage + "-after")
assert frame["resolution"] == [1024, 768]
assert any(row["text"] == "2288.11.15" for row in frame["rows"])
assert any(row["text"] == "暂停" for row in frame["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_SCIENCE166_RIGHTCLICK_RESULT",
    "image_sha256": frame["image_sha256"],
    "date": "2288.11.15",
    "scope": "One original right-click result only; no assumption about route or survey.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_SCIENCE166_RIGHTCLICK_RESULT",
                  "image_sha256": frame["image_sha256"]},
                 ensure_ascii=False), flush=True)
