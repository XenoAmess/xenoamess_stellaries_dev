"""Observe and save the one native Kira survey order at the paused date."""
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
stage = "terravore-kira39-science166-survey-ordered-native-v2-22881115"
clicked = "terravore-kira39-science166-survey-click-22881115"
menu = "terravore-kira39-science166-context-revealed-22881115"
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
receipt = json.loads((run / (clicked + "-execution.json")).read_text("utf-8-sig"))
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
action = json.loads((run / (clicked + ".action.json")).read_text("utf-8-sig"))
assert action["action"] == "left-click" and action["client_point"] == [500, 538]
menu_proof = json.loads((run / (menu + "-observation.json")).read_text("utf-8-sig"))
assert menu_proof["status"] == "OBSERVED_NATIVE_SCIENCE166_KIRA_CONTEXT_MENU"
menu_ocr = json.loads((run / (menu + "-menu.ocr.json")).read_text("utf-8-sig"))
assert any(x["text"] == "调查恒星系" for x in menu_ocr["rows"])
error_before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
frame = r.gpu_capture(stage + "-post-click")
assert frame["resolution"] == [1024, 768]
assert any(x["text"] == "2288.11.15" for x in frame["rows"])
assert any(x["text"] == "暂停" for x in frame["rows"])
saved = r.native_save(stage, "2288.11.15", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
result = {
    "status": "OBSERVED_NATIVE_SCIENCE166_SURVEY_CHOICE_AND_SAVE",
    "menu_image_sha256": menu_proof["image_sha256"],
    "post_click_image_sha256": frame["image_sha256"],
    "save_sha256": saved["save_sha256"],
    "date": saved["date"],
    "error_unchanged": error_after == error_before,
    "scope": "One normal context choice, paused same-day save. Actual survey path and target require independent SAV guard.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert error_after == error_before
