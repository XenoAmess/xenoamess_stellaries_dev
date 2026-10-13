"""Order exactly one normal paid reinforcement for fleet 917 in Chinese UI."""
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
before = "terravore-kira39-battle-day14-native-22881115"
quote = "terravore-kira39-postvictory-fleet917-reinforce-quote-v5-22881115"
stage = "terravore-kira39-fleet917-reinforce-paid-native-22881115"
proof = json.loads((run / (before + "-kira39-final-battle-victory-proof.json")).read_text("utf-8-sig"))
quote_proof = json.loads((run / (quote + "-observation.json")).read_text("utf-8-sig"))
quote_exec = json.loads((run / (quote + "-action-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "PASS_NATIVE_KIRA39_FINAL_BATTLE_VICTORY"
assert all(v is True for v in proof["checks"].values())
assert proof["after_sha256"] == h.sha256(run / (before + ".sav"))
assert quote_proof["status"] == "OBSERVED_NATIVE_FLEET917_REINFORCE_QUOTE"
assert quote_exec["returncode"] == 0
assert quote_exec["helper_sha256"] == h.sha256(Path(quote_exec["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error_before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
frame = r.gpu_capture(stage + "-pre-click")
assert frame["resolution"] == [1024, 768]
for label in ["2288.11.15", "暂停", "舰队管理", "补充舰队", "412.50", "8/9"]:
    assert any(row["text"] == label and row["score"] >= .8 for row in frame["rows"]), label
assert any(row["text"] == "第3舰队" and row["score"] >= .8 for row in frame["rows"])
assert frame["image_sha256"] == quote_proof["image_sha256"] or (
    any(row["text"] == "点击以在最近的船坞补充舰队" for row in frame["rows"]))
click = r.gpu_click(583, 251, stage + "-single-fleet917-click")
assert click
post = r.gpu_capture(stage + "-post-click")
saved = r.native_save(stage, "2288.11.15", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
h.write_json(run / (stage + "-order-observation.json"), {
    "status": "OBSERVED_NATIVE_ONE_FLEET917_REINFORCEMENT_CLICK",
    "before_sha256": proof["after_sha256"],
    "after_sha256": saved["save_sha256"],
    "date": saved["date"],
    "pre_ui_image_sha256": frame["image_sha256"],
    "post_ui_image_sha256": post["image_sha256"],
    "quote_ui_image_sha256": quote_proof["image_sha256"],
    "quote_ui_text": "补充舰队 412.50",
    "click_point": [583, 251],
    "error_unchanged": error_after == error_before,
    "scope": "One normal click and same-day save; payment, queue and ship birth require independent guard.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_ONE_FLEET917_REINFORCEMENT_CLICK",
                  "date": saved["date"], "after_sha256": saved["save_sha256"],
                  "error_unchanged": error_after == error_before},
                 ensure_ascii=False), flush=True)
assert error_after == error_before
