"""Test one native middle-button map pan after the left-drag failure."""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

stage = sys.argv[1]
assert stage == "terravore-kira39-middle-pan"
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "eat_everything_origin/tools")
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
assert meta["language"] == "l_simp_chinese"
original = json.loads((run / "terravore-kira39-support50332250-native-pan-execution.json").read_text("utf-8"))
assert original["returncode"] == 1
assert original["helper_sha256"] == h.sha256(Path(original["command"][1]))

def paused(frame):
    return frame["resolution"] == [1024, 768] and all(
        any(v["text"] == label and v["score"] >= .9 for v in frame["rows"])
        for label in ["2288.09.02", "暂停"])

before = r.gpu_capture(stage + "-before")
assert paused(before)
hwnd = h.focus_pid(int(h.process_record(run)["pid"]))
first = h.win32gui.ClientToScreen(hwnd, (430, 500))
last = h.win32gui.ClientToScreen(hwnd, (760, 500))
h.pyautogui.moveTo(*first, duration=.15)
h.pyautogui.dragTo(*last, duration=.8, button="middle")
action = {"action": "native_middle_button_map_drag", "stage": stage,
          "client_from": [430, 500], "client_to": [760, 500],
          "desktop_from": list(first), "desktop_to": list(last),
          "duration_seconds": .8, "at_utc": datetime.now(timezone.utc).isoformat(),
          "foreground_after": h.win32gui.GetForegroundWindow(), "expected_hwnd": hwnd}
assert action["foreground_after"] == hwnd
h.write_json(run / (stage + "-middle-drag.action.json"), action)
after = r.gpu_capture(stage + "-after")
assert paused(after)
print(json.dumps({"status": "MIDDLE_PAN_OBSERVED_NO_CALENDAR", "before": before["image_sha256"],
                  "after": after["image_sha256"], "action": action}), flush=True)
