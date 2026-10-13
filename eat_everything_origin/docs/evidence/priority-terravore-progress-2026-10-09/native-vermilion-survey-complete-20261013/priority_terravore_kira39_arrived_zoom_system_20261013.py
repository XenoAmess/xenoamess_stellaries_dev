"""Zoom the paused galaxy camera into Kira after locating fleet 166."""
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
stage = "terravore-kira39-arrived-zoom-system-22890511"
previous = "terravore-kira39-arrived-science166-goto-ui-v2-22890511"
proof = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (previous + "-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "PASS_READ_ONLY_PAUSED_NATIVE_CAPTURE"
assert all(proof["checks"].values()) and receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
r.gpu_scroll(3, 510, 383, stage + "-scroll", 1)
frame = r.gpu_capture(stage + "-after")
checks = {
    "paused_same_date":
        any(x["text"] == "2289.05.11" for x in frame["rows"])
        and any(x["text"] == "暂停" for x in frame["rows"]),
    "no_new_error": (user / "logs/error.log").read_bytes() == error,
}
result = {
    "status": "PASS_NATIVE_KIRA_CAMERA_ZOOM" if all(checks.values()) else "FAIL",
    "checks": checks,
    "image_sha256": frame["image_sha256"],
    "scroll": {"clicks": 3, "client_point": [510, 383]},
    "scope": "Camera zoom only. System view and planet labels require visual review.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert all(checks.values())
