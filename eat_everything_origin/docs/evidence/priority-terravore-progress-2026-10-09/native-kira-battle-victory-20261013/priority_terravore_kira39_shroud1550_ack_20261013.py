"""Acknowledge the sole vanilla Power of Will option in paused Chinese UI."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-battle-day11-native-22881112"
stage = "terravore-kira39-shroud1550-ack-native-22881112"
proof_file = before + "-shroud1550-boundary-proof.json"
proof = json.loads((run / proof_file).read_text("utf-8-sig"))
receipt = json.loads((run / (before + "-shroud1550-boundary-guard-execution.json")).read_text("utf-8-sig"))
state = read_state(run, before)
assert meta["language"] == "l_simp_chinese"
assert proof["status"] == "PASS_NATIVE_VANILLA_SHROUD1550_EVENT_BOUNDARY"
assert all(v is True for v in proof["checks"].values())
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert proof["after_sha256"] == state["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
assert state["audit"]["date"] == "2288.11.12"
assert q.scalars(state["pending"][0])["event"] == "shroud.1550"
assert not list(run.glob(stage + "*"))

frame = r.gpu_capture(stage + "-pre-click")
assert frame["resolution"] == [1024, 768]
rows = frame["rows"]
for label in ["2288.11.12", "暂停", "意志之力"]:
    assert any(row["text"] == label and row["score"] >= 0.8 for row in rows), label
choice = [row for row in rows if row["text"] == "很有潜力。" and row["score"] >= .8]
assert len(choice) == 1, choice
assert frame["image_sha256"] == h.sha256(Path(frame["image"]))

error_before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
point = [round(sum(c[i] for c in choice[0]["box"]) / 4) for i in [0, 1]]
click_receipt = r.gpu_click(*point, stage + "-sole-vanilla-option0")
assert click_receipt
post = r.gpu_capture(stage + "-post-click")
assert not any(row["text"] == "意志之力" and row["score"] >= .8
               for row in post["rows"])
saved = r.native_save(stage, "2288.11.12", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
print(json.dumps({"status": "NATIVE_SHROUD1550_OPTION0_CLICK_AND_SAVE",
                  "date": saved["date"],
                  "before_sha256": state["audit"]["save_sha256"],
                  "after_sha256": saved["save_sha256"],
                  "pre_ui_image_sha256": frame["image_sha256"],
                  "post_ui_image_sha256": post["image_sha256"],
                  "point": point,
                  "error_unchanged": error_after == error_before},
                 ensure_ascii=False), flush=True)
assert error_after == error_before
