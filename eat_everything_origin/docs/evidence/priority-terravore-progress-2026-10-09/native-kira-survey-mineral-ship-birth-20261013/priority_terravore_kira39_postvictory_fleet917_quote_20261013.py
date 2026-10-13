"""Select the damaged paid destroyer fleet and inspect its native quote."""
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
previous = "terravore-kira39-postvictory-manager-open-22881115"
stage = "terravore-kira39-postvictory-fleet917-quote-22881115"
proof = json.loads((run / (previous + "-observation.json")).read_text("utf-8-sig"))
execution = json.loads((run / (previous + "-action-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "OBSERVED_NATIVE_FLEET_MANAGER"
assert execution["returncode"] == 0
assert execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert pre["resolution"] == [1024, 768]
assert pre["image_sha256"] == proof["after_image_sha256"] or any(
    row["text"] == "舰队管理" for row in pre["rows"])
assert any(row["text"] == "2288.11.15" for row in pre["rows"])
assert any(row["text"] == "暂停" for row in pre["rows"])
assert any(row["text"] == "舰队管理" for row in pre["rows"])
click = r.gpu_click(100, 281, stage + "-select-third-fleet")
assert click
post = r.gpu_capture(stage + "-after")
assert any(row["text"] == "舰队管理" for row in post["rows"])
assert any(row["text"] == "2288.11.15" for row in post["rows"])
assert any(row["text"] == "暂停" for row in post["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_FLEET917_QUOTE",
    "before_image_sha256": pre["image_sha256"],
    "after_image_sha256": post["image_sha256"],
    "click_point": [100, 281],
    "date": "2288.11.15",
    "scope": "Selected third fleet in native manager only; no paid order.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_FLEET917_QUOTE",
                  "after_image_sha256": post["image_sha256"]},
                 ensure_ascii=False), flush=True)
