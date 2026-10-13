"""Acknowledge the one reviewed native L-Gate event in Chinese UI."""
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
review_stage = "terravore-kira39-apoc3-vanilla-error-review-22890501"
before = "terravore-kira39-scout-month04-native-22890501"
stage = "terravore-kira39-apoc3-ack-native-22890501"
assert not list(run.glob(stage + "*"))
review = json.loads((run / (review_stage + "-proof.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (review_stage + "-execution.json")).read_text("utf-8-sig"))
assert review["status"] == "PASS_REVIEWED_VANILLA_APOC3_SKY_DRAGON_LOC_BOUNDARY"
assert all(review["checks"].values())
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert review["after_sha256"] == h.sha256(run / (before + ".sav"))
assert meta["language"] == "l_simp_chinese"
error_before = (user / "logs/error.log").read_bytes()
assert error_before == (run / (before + "-error-after.log")).read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
frame = r.gpu_capture(stage + "-pre-click")
labels = [row["text"] for row in frame["rows"]]
for label in ["2289.05.01", "暂停", "遗弃星门", "有意思。"]:
    assert label in labels, label
assert [row["text"] for row in frame["rows"]].count("有意思。") == 1
r.gpu_click(510, 545, stage + "-only-native-option")
post = r.gpu_capture(stage + "-post-click")
saved = r.native_save(stage, "2289.05.01", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
result = {
    "status": "OBSERVED_ONE_NATIVE_APOC3_OPTION_AND_SAME_DAY_SAVE",
    "before_sha256": review["after_sha256"],
    "after_sha256": saved["save_sha256"],
    "date": saved["date"],
    "pre_ui_sha256": frame["image_sha256"],
    "post_ui_sha256": post["image_sha256"],
    "option": "有意思。",
    "client_point": [510, 545],
    "error_unchanged": error_before == error_after,
    "scope": "One normal official L-Gate event option, paused same-day save; effects require independent SAV guard.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert error_before == error_after
