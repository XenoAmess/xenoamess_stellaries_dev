"""Pan the paused native map so Kira is clear of the selected-fleet panel."""
import json
import logging
import sys

stage = sys.argv[1]
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "eat_everything_origin/tools")
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
assert meta["language"] == "l_simp_chinese"
assert stage == "terravore-kira39-support50332250-native-pan"

def selected(frame):
    rows = frame["rows"]
    return all(any(v["text"] == label and v["score"] >= .9 for v in rows)
               for label in ["2288.09.02", "暂停"]) and any(
        v["text"] == "第2舰队" and v["score"] >= .9 and v["box"][0][0] < 400
        for v in rows)

before = r.gpu_capture(stage + "-before")
assert before["resolution"] == [1024, 768] and selected(before)
action = r.gpu_drag(430, 500, 760, 500, .7, stage + "-normal-map-drag")
assert action
after = r.gpu_capture(stage + "-after")
assert after["resolution"] == [1024, 768] and selected(after)
print(json.dumps({"status": "NATIVE_PAUSED_PAN_ONLY", "before": before["image_sha256"],
                  "after": after["image_sha256"], "drag": [430, 500, 760, 500]}), flush=True)
