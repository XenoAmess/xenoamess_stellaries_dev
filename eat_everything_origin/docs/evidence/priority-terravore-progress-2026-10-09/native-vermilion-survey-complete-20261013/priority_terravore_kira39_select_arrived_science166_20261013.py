"""Select original science fleet 166 in the paused Chinese outliner."""
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
stage = "terravore-kira39-arrived-science166-selected-22890511"
prior_stage = "terravore-kira39-arrival-ui-22890511"
prior = json.loads((run / (prior_stage + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (prior_stage + "-execution.json")).read_text("utf-8-sig"))
assert prior["status"] == "PASS_READ_ONLY_NATIVE_ARRIVAL_UI_CAPTURE"
assert all(prior["checks"].values()) and receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert pre["resolution"] == [1024, 768]
assert any(x["text"] == "2289.05.11" for x in pre["rows"])
assert any(x["text"] == "EEP德雷克" for x in pre["rows"])
r.gpu_click(884, 445, stage + "-science-outliner-click")
post = r.gpu_capture(stage + "-after")
checks = {
    "paused_current_date":
        any(x["text"] == "2289.05.11" for x in post["rows"])
        and any(x["text"] == "暂停" for x in post["rows"]),
    "science_fleet_still_visible":
        any(x["text"] == "EEP德雷克" for x in post["rows"]),
    "selection_did_not_append_error": (user / "logs/error.log").read_bytes() == error,
}
proof = {
    "status": "PASS_NATIVE_SCIENCE166_SELECTED_UI" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_image_sha256": pre["image_sha256"],
    "after_image_sha256": post["image_sha256"],
    "click_point": [884, 445],
    "scope": "Select one original science fleet in paused UI; no order, date or save change.",
}
h.write_json(run / (stage + "-observation.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
