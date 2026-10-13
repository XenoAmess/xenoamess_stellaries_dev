"""Capture a paused Chinese native screen after a separately recorded UI action."""
import json
import logging
import sys
from pathlib import Path

stage, date, previous = sys.argv[1:]
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
receipt = json.loads((run / (previous + "-execution.json")).read_text("utf-8-sig"))
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
error = (user / "logs/error.log").read_bytes()
frame = r.gpu_capture(stage + "-capture")
checks = {
    "expected_resolution_chinese": frame["resolution"] == [1024, 768],
    "paused_expected_date":
        any(x["text"] == date for x in frame["rows"])
        and any(x["text"] == "暂停" for x in frame["rows"]),
    "no_new_error": (user / "logs/error.log").read_bytes() == error,
}
proof = {
    "status": "PASS_READ_ONLY_PAUSED_NATIVE_CAPTURE" if all(checks.values()) else "FAIL",
    "checks": checks,
    "image_sha256": frame["image_sha256"],
    "date": date,
    "previous_execution": previous,
    "visible_rows": frame["rows"],
    "scope": "Read-only OCR and screenshot after already recorded input; no click or calendar.",
}
h.write_json(run / (stage + "-observation.json"), proof)
print(json.dumps({"status": proof["status"], "checks": checks,
                  "image_sha256": frame["image_sha256"]}, ensure_ascii=False), flush=True)
assert all(checks.values())
