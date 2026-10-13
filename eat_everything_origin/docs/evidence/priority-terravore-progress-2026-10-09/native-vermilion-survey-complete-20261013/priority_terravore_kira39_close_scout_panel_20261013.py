"""Close the selected science-fleet panel to expose the Kira system map."""
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
stage = "terravore-kira39-arrived-scout-panel-closed-22890511"
previous = "terravore-kira39-arrived-enter-system-e-22890511"
prior = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (previous + "-execution.json")).read_text("utf-8-sig"))
assert prior["status"] == "PASS_NATIVE_KIRA_E_VIEW_INPUT"
assert all(prior["checks"].values()) and receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
r.gpu_click(387, 482, stage + "-panel-x")
frame = r.gpu_capture(stage + "-after")
checks = {
    "paused_same_date":
        any(x["text"] == "2289.05.11" for x in frame["rows"])
        and any(x["text"] == "暂停" for x in frame["rows"]),
    "no_new_error": (user / "logs/error.log").read_bytes() == error,
}
result = {
    "status": "PASS_NATIVE_KIRA_SCOUT_PANEL_CLOSED" if all(checks.values()) else "FAIL",
    "checks": checks,
    "image_sha256": frame["image_sha256"],
    "client_point": [387, 482],
    "scope": "Close one selected fleet panel only; no order or calendar.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert all(checks.values())
