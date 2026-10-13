"""Open native Chinese fleet management after Kira victory to read the quote."""
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
stage = "terravore-kira39-postvictory-manager-open-22881115"
before = "terravore-kira39-battle-day14-native-22881115"
proof = json.loads((run / (before + "-kira39-final-battle-victory-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (before + "-final-victory-guard-execution.json")).read_text("utf-8-sig"))
assert proof["status"] == "PASS_NATIVE_KIRA39_FINAL_BATTLE_VICTORY"
assert all(v is True for v in proof["checks"].values())
assert execution["returncode"] == 0
assert execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
assert proof["after_sha256"] == h.sha256(run / (before + ".sav"))
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert pre["resolution"] == [1024, 768]
assert any(row["text"] == "2288.11.15" for row in pre["rows"])
assert any(row["text"] == "暂停" for row in pre["rows"])
h.press_scan_code(0x43, stage + "-f9-native-manager", 1)
post = r.gpu_capture(stage + "-after")
assert any(row["text"] == "舰队管理" and row["score"] >= .8
           for row in post["rows"])
assert any(row["text"] == "2288.11.15" for row in post["rows"])
assert any(row["text"] == "暂停" for row in post["rows"])
assert (user / "logs/error.log").read_bytes() == error
out = run / (stage + "-observation.json")
h.write_json(out, {"status": "OBSERVED_NATIVE_FLEET_MANAGER",
                   "date": "2288.11.15",
                   "before_image_sha256": pre["image_sha256"],
                   "after_image_sha256": post["image_sha256"],
                   "source_save_sha256": proof["after_sha256"],
                   "scope": "Native manager opened only; no reinforcement ordered."})
print(json.dumps({"status": "OBSERVED_NATIVE_FLEET_MANAGER",
                  "date": "2288.11.15", "after_image_sha256": post["image_sha256"]},
                 ensure_ascii=False), flush=True)
