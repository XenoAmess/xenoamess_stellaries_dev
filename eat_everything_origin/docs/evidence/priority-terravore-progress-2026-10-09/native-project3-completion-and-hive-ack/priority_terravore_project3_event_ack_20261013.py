"""Acknowledge the original project-3 hive event once through the Chinese UI."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "eat_everything_origin/tools")
sys.path.insert(0, "_runtime/heart-of-devouring")
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-project3-completion-22880902"
stage = "terravore-project3-crisis4130-ack-22880902"
proof = json.loads((run / (before + "-project3-completion-proof.json")).read_text("utf-8"))
execution = json.loads((run / (before + "-guard-execution.json")).read_text("utf-8"))
state = read_state(run, before)
source = h.GAME_EXE.parent / "events" / "nemesis_crisis_events.txt"
events = [v for k, v, obj in q.fields(source.read_text("utf-8-sig"))
          if obj and q.scalars(v).get("id") == "crisis.4130"]
assert len(events) == 1
options = [v for k, v, obj in q.fields(events[0]) if k == "option" and obj]
assert len(options) == 4
assert q.scalars(options[3]).get("name") == "crisis.4130.hive.a"
assert not [(k, obj) for k, v, obj in q.fields(options[3]) if k not in {"name", "trigger"}]
assert meta["language"] == "l_simp_chinese"
assert proof["status"] == "PASS_NATIVE_PROJECT3_COMPLETED_EVENT_PENDING"
assert all(v is True for v in proof["checks"].values())
assert execution["returncode"] == 0
assert execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
assert state["audit"]["save_sha256"] == proof["after_sha256"] == h.sha256(run / (before + ".sav"))
assert state["audit"]["date"] == "2288.09.02"
assert len(state["pending"]) == 1
assert q.scalars(state["pending"][0])["id"] == 305
assert q.scalars(state["pending"][0])["event"] == "crisis.4130"
assert not (run / (stage + ".sav")).exists()

frame = r.gpu_capture(stage + "-pre-click")
rows = frame["rows"]
for label in ["2288.09.02", "暂停", "异界注能"]:
    assert any(row["text"] == label and row["score"] >= .8 for row in rows), label
choice = [row for row in rows if row["text"] == "此举必为正道。" and row["score"] >= .9]
assert len(choice) == 1, choice
assert frame["resolution"] == [1024, 768]
assert frame["image_sha256"] == h.sha256(Path(frame["image"]))
error_before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(error_before)
point = [round(sum(c[i] for c in choice[0]["box"]) / 4) for i in [0, 1]]
receipt = r.gpu_click(*point, stage + "-option3-normal")
assert receipt
r.gpu_capture(stage + "-post-click")
saved = r.native_save(stage, "2288.09.02", (0,))
error_after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(error_after)
print(json.dumps({"status": "NATIVE_CLICK_AND_SAVE", "date": saved["date"],
                  "before_sha256": state["audit"]["save_sha256"],
                  "after_sha256": saved["save_sha256"], "option_index": 3,
                  "source_sha256": h.sha256(source), "point": point,
                  "error_unchanged": error_after == error_before}, ensure_ascii=False), flush=True)
