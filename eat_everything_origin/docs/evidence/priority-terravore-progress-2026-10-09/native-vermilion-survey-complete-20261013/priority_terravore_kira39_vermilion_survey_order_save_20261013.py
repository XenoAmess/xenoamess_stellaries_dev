"""Save after one visible native survey command on Vermilion."""
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
stage = "terravore-kira39-vermilion-survey-order-native-22890511"
clicked = "terravore-kira39-vermilion-survey-click-22890511"
menu = "terravore-kira39-vermilion-body-context-22890511"
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
receipt = json.loads((run / (clicked + "-execution.json")).read_text("utf-8-sig"))
proof = json.loads((run / (clicked + "-observation.json")).read_text("utf-8-sig"))
menu_receipt = json.loads((run / (menu + "-execution.json")).read_text("utf-8-sig"))
assert receipt["returncode"] == menu_receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert menu_receipt["helper_sha256"] == h.sha256(Path(menu_receipt["command"][1]))
assert proof["status"] == "PASS_NATIVE_PAUSED_CLICK_CAPTURE"
assert all(proof["checks"].values()) and proof["client_point"] == [510, 425]
ocr = json.loads((run / (clicked + "-after.ocr.json")).read_text("utf-8-sig"))
assert any(x["text"] == "正在调查维米里恩：0%" for x in ocr["rows"])
before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(before)
saved = r.native_save(stage, "2289.05.11", (0,))
after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after)
result = {
    "status": "OBSERVED_ONE_NATIVE_VERMILION_SURVEY_ORDER_SAVED",
    "date": saved["date"],
    "save_sha256": saved["save_sha256"],
    "error_unchanged": before == after,
    "scope": "One normal survey-menu click and same-day save; actual order delta needs independent guard.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert before == after
