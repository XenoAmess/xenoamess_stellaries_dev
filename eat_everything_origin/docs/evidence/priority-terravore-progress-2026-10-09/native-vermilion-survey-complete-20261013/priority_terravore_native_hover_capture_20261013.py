"""Read-only hover and capture at a paused native GUI client point."""
import json
import logging
import sys
import time
from pathlib import Path

stage, date, prior_stage, raw_x, raw_y = sys.argv[1:]
x, y = int(raw_x), int(raw_y)
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
assert meta["language"] == "l_simp_chinese"
assert 0 <= x < 1024 and 0 <= y < 768
assert not list(run.glob(stage + "*"))
prior = json.loads((run / (prior_stage + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (prior_stage + "-execution.json")).read_text("utf-8-sig"))
assert prior["status"].startswith("PASS") and all(prior["checks"].values())
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
error = (user / "logs/error.log").read_bytes()
point = r.desktop_point(x, y)
h.win32api.SetCursorPos(point)
time.sleep(0.7)
frame = r.gpu_capture(stage + "-hover")
checks = {
    "paused_expected_date":
        any(z["text"] == date for z in frame["rows"])
        and any(z["text"] == "暂停" for z in frame["rows"]),
    "error_unchanged": (user / "logs/error.log").read_bytes() == error,
}
proof = {
    "status": "PASS_READ_ONLY_NATIVE_HOVER" if all(checks.values()) else "FAIL",
    "checks": checks,
    "image_sha256": frame["image_sha256"],
    "client_point": [x, y],
    "rows": frame["rows"],
    "scope": "Mouse move and screenshot only; target identity requires visual review.",
}
h.write_json(run / (stage + "-observation.json"), proof)
print(json.dumps({"status": proof["status"], "checks": checks,
                  "image_sha256": frame["image_sha256"],
                  "labels": [z["text"] for z in frame["rows"] if z["score"] >= .8]},
                 ensure_ascii=False), flush=True)
assert all(checks.values())
