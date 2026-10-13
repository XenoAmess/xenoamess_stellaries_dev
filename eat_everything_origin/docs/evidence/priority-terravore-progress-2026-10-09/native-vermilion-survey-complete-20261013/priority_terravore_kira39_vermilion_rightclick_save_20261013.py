"""Save the paused native game once after the ambiguous planet right-click."""
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
stage = "terravore-kira39-vermilion-rightclick-native-22890511"
right = "terravore-kira39-vermilion-scout-rightclick-22890511"
capture = "terravore-kira39-vermilion-scout-context-22890511"
receipt = json.loads((run / (right + "-execution.json")).read_text("utf-8-sig"))
action = json.loads((run / (right + ".action.json")).read_text("utf-8-sig"))
proof = json.loads((run / (capture + "-observation.json")).read_text("utf-8-sig"))
assert receipt["returncode"] == 0
assert receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
assert action["action"] == "right-click" and action["client_point"] == [596, 414]
assert proof["status"] == "PASS_READ_ONLY_PAUSED_NATIVE_CAPTURE"
assert all(proof["checks"].values())
assert meta["language"] == "l_simp_chinese"
assert not list(run.glob(stage + "*"))
before = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-before.log")).write_bytes(before)
saved = r.native_save(stage, "2289.05.11", (0,))
after = (user / "logs/error.log").read_bytes()
(run / (stage + "-error-after.log")).write_bytes(after)
result = {
    "status": "OBSERVED_SAME_DAY_NATIVE_SAVE_AFTER_AMBIGUOUS_RIGHTCLICK",
    "date": saved["date"],
    "save_sha256": saved["save_sha256"],
    "error_unchanged": after == before,
    "scope": "No further planet click or calendar; order change requires independent SAV comparison.",
}
h.write_json(run / (stage + "-observation.json"), result)
print(json.dumps(result, ensure_ascii=False), flush=True)
assert after == before
