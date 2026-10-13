"""Select original science fleet 166 from the Chinese civilian outliner."""
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
previous = "terravore-kira39-postpaid-military-outliner-fold-22881115"
stage = "terravore-kira39-science166-selected-22881115"
proof = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (previous + "-action-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "OBSERVED_NATIVE_CIVILIAN_OUTLINER"
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert pre["resolution"] == [1024, 768]
for label in ["2288.11.15", "暂停", "EEP德雷克", "通用舰船"]:
    assert any(row["text"] == label and row["score"] >= .8
               for row in pre["rows"]), label
click = r.gpu_click(884, 445, stage + "-select-Drake")
assert click
post = r.gpu_capture(stage + "-after")
assert any(row["text"] == "2288.11.15" for row in post["rows"])
assert any(row["text"] == "暂停" for row in post["rows"])
assert any("德雷克" in row["text"] for row in post["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_SCIENCE166_SELECTED",
    "before_image_sha256": pre["image_sha256"],
    "after_image_sha256": post["image_sha256"],
    "click_point": [884, 445],
    "date": "2288.11.15",
    "scope": "Science Drake outliner selection only; no route or survey order.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_SCIENCE166_SELECTED",
                  "after_image_sha256": post["image_sha256"]},
                 ensure_ascii=False), flush=True)
