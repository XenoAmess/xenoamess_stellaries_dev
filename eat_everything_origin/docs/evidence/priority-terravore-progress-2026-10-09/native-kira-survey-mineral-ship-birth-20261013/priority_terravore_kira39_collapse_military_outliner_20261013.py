"""Reveal native civilian ships by folding the military outliner group."""
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
before = "terravore-kira39-fleet917-reinforce-paid-native-22881115"
failed_stage = "terravore-kira39-postpaid-close-manager-for-scout-22881115-action"
stage = "terravore-kira39-postpaid-military-outliner-fold-22881115"
proof = json.loads((run / (before + "-fleet917-mineral-payment-proof.json")).read_text("utf-8-sig"))
failed = json.loads((run / (failed_stage + "-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "PASS_NATIVE_KIRA39_FLEET917_MINERAL_PAYMENT"
assert all(v is True for v in proof["checks"].values())
assert failed["returncode"] == 1
assert failed["helper_sha256"] == h.sha256(Path(failed["command"][1]))
assert proof["after_sha256"] == h.sha256(run / (before + ".sav"))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert pre["resolution"] == [1024, 768]
assert any(row["text"] == "2288.11.15" for row in pre["rows"])
assert any(row["text"] == "暂停" for row in pre["rows"])
assert any(row["text"] == "军用舰队" for row in pre["rows"])
assert any(row["text"] == "通用舰船" for row in pre["rows"])
assert not any(row["text"] == "舰队管理" for row in pre["rows"])
click = r.gpu_click(879, 269, stage + "-fold-military")
assert click
post = r.gpu_capture(stage + "-after")
assert any(row["text"] == "2288.11.15" for row in post["rows"])
assert any(row["text"] == "暂停" for row in post["rows"])
assert (user / "logs/error.log").read_bytes() == error
h.write_json(run / (stage + "-observation.json"), {
    "status": "OBSERVED_NATIVE_CIVILIAN_OUTLINER",
    "before_image_sha256": pre["image_sha256"],
    "after_image_sha256": post["image_sha256"],
    "click_point": [879, 269],
    "date": "2288.11.15",
    "scope": "Folded only the military outliner group; no ship orders or calendar.",
})
print(json.dumps({"status": "OBSERVED_NATIVE_CIVILIAN_OUTLINER",
                  "after_image_sha256": post["image_sha256"]},
                 ensure_ascii=False), flush=True)
