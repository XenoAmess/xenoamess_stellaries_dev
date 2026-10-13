"""Read-only capture of paused Chinese UI after native arrival in Kira 39."""
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
stage = "terravore-kira39-arrival-ui-22890511"
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
before = (user / "logs/error.log").read_bytes()
frame = r.gpu_capture(stage + "-capture")
after = (user / "logs/error.log").read_bytes()
checks = {
    "simplified_chinese_1024x768": frame["resolution"] == [1024, 768],
    "paused_current_native_date":
        any(row["text"] == "2289.05.11" for row in frame["rows"])
        and any(row["text"] == "暂停" for row in frame["rows"]),
    "read_only_no_new_error": before == after,
}
proof = {
    "status": "PASS_READ_ONLY_NATIVE_ARRIVAL_UI_CAPTURE" if all(checks.values()) else "FAIL",
    "checks": checks,
    "image_sha256": frame["image_sha256"],
    "visible_rows": frame["rows"],
    "scope": "No click, map move, calendar input or save.",
}
h.write_json(run / (stage + "-observation.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
