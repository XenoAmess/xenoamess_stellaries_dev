"""Bounded same-month native calendar; no retry and no game-state edits."""
import json
import logging
import re
import sys
import time
from pathlib import Path

start, stage, days_text, prior_file, prior_execution = sys.argv[1:]
days = int(days_text)
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
for value in (start, stage):
    assert re.fullmatch(r"hope-route-[a-z0-9-]+-native-\d{8}", value)
for value in (prior_file, prior_execution):
    assert Path(value).name == value and value.endswith(".json")
assert 1 <= days <= 7
old = read_state(run, start)
proof = json.loads((run / prior_file).read_text("utf-8"))
execution = json.loads((run / prior_execution).read_text("utf-8"))
start_date = old["audit"]["date"]
year, month, day = map(int, start_date.split("."))
assert day + days <= 30
end_date = f"{year:04d}.{month:02d}.{day + days:02d}"
assert stage.endswith(end_date.replace(".", ""))
assert proof["pass"] and execution["returncode"] == 0
assert proof.get("calendar_ready", True)
assert old["audit"]["save_sha256"] == proof["after_save_sha256"]
assert h.sha256(Path(execution["command"][1])) == execution["helper_sha256"]
assert h.sha256(run / (start + ".sav")) == old["audit"]["save_sha256"]
assert meta["language"] == "l_simp_chinese" and meta["version"] == "0.2.0"
assert h.tree_manifest(Path(meta["copied_mod"]))[1] == meta["copied_mod_tree_sha256"]
assert h.tree_manifest(r.ROOT / "mod")[1] == meta["repository_mod_tree_sha256"]
assert not old["pending"] and not list(run.glob(stage + "*"))
assert old["audit"]["countries"]["0"]["owned_colonies"] == [0, 40]
before_error = (user / "logs" / "error.log").read_bytes()
assert before_error == (run / (start + "-error-after.log")).read_bytes()
frame = r.gpu_capture(stage + "-preflight-ui")
labels = [row["text"] for row in frame["rows"]]
assert start_date in labels and "暂停" in labels
(run / (stage + "-error-before.log")).write_bytes(before_error)
h.write_json(run / (stage + "-preflight.json"), {
    "status": "PASS_BOUND_SAME_MONTH_BATTLE_PREFLIGHT", "days": days,
    "start_date": start_date, "end_date": end_date,
    "start_sha256": old["audit"]["save_sha256"], "prior_proof": prior_file,
    "prior_execution": prior_execution, "ui_sha256": frame["image_sha256"]})
h.press_scan_code(0x29, stage + "-console-open", 1)
h.type_text(f"fast_forward {days}", True, stage + "-native-days")
for poll in range(45):
    if poll:
        time.sleep(8)
    frame = r.gpu_capture(stage + "-calendar-poll-" + str(poll))
    labels = [row["text"] for row in frame["rows"]]
    complete = end_date in labels and "暂停" in labels and any(
        h.normalized(label).startswith(f"fastforwarded{days}day")
        or h.normalized(label) == f"fastforwarded{days}d" for label in labels)
    print(json.dumps({"poll": poll, "date_seen": end_date in labels,
                      "complete": complete}), flush=True)
    if complete:
        h.write_json(run / (stage + "-calendar-receipt.json"), {
            "status": "CALENDAR_CONFIRMED", "start_date": start_date,
            "date": end_date, "days": days, "image_sha256": frame["image_sha256"],
            "receipt_labels": [label for label in labels if "fastforward" in h.normalized(label)]})
        break
else:
    raise RuntimeError("calendar receipt missing; do not retry")
h.press_scan_code(0x29, stage + "-console-close", 1)
saved = r.native_save(stage, end_date, (0, 1, 15))
after_error = (user / "logs" / "error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after_error)
h.write_json(run / (stage + "-state.json"), {
    "date": saved["date"], "save_sha256": saved["save_sha256"],
    "new_error_bytes": len(after_error) - len(before_error),
    "status": "OBSERVED_BOUNDED_NATIVE_BATTLE"})
print(json.dumps({"date": saved["date"], "save_sha256": saved["save_sha256"],
                  "new_error_bytes": len(after_error) - len(before_error)}), flush=True)
assert after_error == before_error
