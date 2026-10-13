"""Bind the July 1 native full-system survey choice and save the paused game."""
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
stage = "terravore-kira39-fullsystem-survey-order-native-22890701"
before = "terravore-kira39-vermilion-survey-july-boundary-native-22890701"
prior_stage = "terravore-kira39-vermilion-survey-completion-july-budget-guard-22890701"
menu = "terravore-kira39-july01-science-kira-full-survey-menu"
hover = "terravore-kira39-july01-science-full-survey-menu-second-hover"
clicked = "terravore-kira39-july01-science-full-survey-click"
post = "terravore-kira39-july01-science-full-survey-after-click"
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
proof = json.loads((run / (prior_stage + "-proof.json")).read_text("utf-8-sig"))
assert proof["status"] == "PASS_NATIVE_VERMILION_SURVEY_COMPLETE_JULY_BUDGET"
assert all(proof["checks"].values())
assert proof["after_sha256"] == h.sha256(run / (before + ".sav"))
menu_image = json.loads((run / (menu + ".ocr.json")).read_text("utf-8-sig"))
hover_image = json.loads((run / (hover + ".ocr.json")).read_text("utf-8-sig"))
post_image = json.loads((run / (post + ".ocr.json")).read_text("utf-8-sig"))
assert menu_image["image_sha256"] == h.sha256(run / (menu + ".jpg")) == "a7da8d411627a5ebbcefdb7cf57e7aa5a37a88972e65a156de2cb513d39c19db"
assert hover_image["image_sha256"] == h.sha256(run / (hover + ".jpg")) == "31cfe0e348d54190c0377f3d030331b81aed543008c75ef4d1bd2cdab74374b6"
assert post_image["image_sha256"] == h.sha256(run / (post + ".jpg")) == "1b89c64f382eecd0e84782fd6b753a75a85259fb54d9c4512ecedb5786c9eb4c"
assert any(x["text"] == "2289.07.01" for x in post_image["rows"])
assert any(x["text"] == "暂停" for x in post_image["rows"])
action = json.loads((run / (clicked + ".action.json")).read_text("utf-8-sig"))
assert action["action"] == "click_point" and action["client_point"] == [550, 435]
error_before = (user / "logs/error.log").read_bytes()
assert error_before == (run / (before + "-error-after.log")).read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
saved = r.native_save(stage, "2289.07.01", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
result = {
    "status": "OBSERVED_NATIVE_KIRA39_FULLSYSTEM_SURVEY_ORDER_AND_SAVE" if error_after == error_before else "FAIL",
    "before_sha256": proof["after_sha256"],
    "after_sha256": saved["save_sha256"],
    "date": saved["date"],
    "menu_image_sha256": menu_image["image_sha256"],
    "hover_image_sha256": hover_image["image_sha256"],
    "post_image_sha256": post_image["image_sha256"],
    "error_unchanged": error_after == error_before,
    "scope": "One native full-system survey command and same-day save; exact queue and business effects require independent guard.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert error_after == error_before
