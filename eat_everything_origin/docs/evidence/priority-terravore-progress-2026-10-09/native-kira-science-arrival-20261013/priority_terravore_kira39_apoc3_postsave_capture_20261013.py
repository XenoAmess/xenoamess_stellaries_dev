"""Capture the untouched native Chinese L-Gate popup after failed error guard."""
import json
import logging
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "terravore-kira39-apoc3-postsave-capture-22890501"
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(before)
frame = r.gpu_capture(stage + "-native-ui")
after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after)
labels = [x["text"] for x in frame["rows"]]
result = {
    "status": "OBSERVED_NATIVE_APOC3_POSTSAVE_UI",
    "date_seen": "2289.05.01" in labels,
    "paused_seen": "暂停" in labels,
    "l_gate_title_seen": "遗弃星门" in labels,
    "image_sha256": frame["image_sha256"],
    "error_before_sha256": h.sha256(run / (stage + "-error-before.log")),
    "error_after_sha256": h.sha256(run / (stage + "-error-after.log")),
    "new_error_bytes": len(after) - len(before),
    "scope": "Fresh GPU/OCR observation only, no click/calendar/save/event ACK.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert result["date_seen"] and result["paused_seen"] and result["l_gate_title_seen"]
