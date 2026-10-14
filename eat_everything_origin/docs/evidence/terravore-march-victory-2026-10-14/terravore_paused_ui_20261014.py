"""One recorded normal UI navigation while paused; meaning checked separately."""
import json
import logging
import sys

mode, stage, date, x_text, y_text = sys.argv[1:]
x, y = int(x_text), int(y_text)
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
assert meta["language"] == "l_simp_chinese" and mode in ("click", "hover", "capture")
assert 0 <= x < 1024 and 0 <= y < 768 and not list(run.glob(stage + "*"))
error = (user / "logs/error.log").read_bytes()
pre = r.gpu_capture(stage + "-before")
assert date in [row["text"] for row in pre["rows"]]
assert "暂停" in [row["text"] for row in pre["rows"]]
if mode == "click":
    r.gpu_click(x, y, stage + "-click")
elif mode == "hover":
    h.pyautogui.moveTo(*r.desktop_point(x, y), duration=0.2)
frame = r.gpu_capture(stage + "-after")
labels = [row["text"] for row in frame["rows"]]
checks = {"date_paused": date in labels and "暂停" in labels,
          "error_unchanged": (user / "logs/error.log").read_bytes() == error}
h.write_json(run / (stage + "-ui-proof.json"), {
    "pass": all(checks.values()), "checks": checks, "mode": mode,
    "image_sha256": frame["image_sha256"], "labels": labels})
print(json.dumps({"checks": checks, "image_sha256": frame["image_sha256"], "labels": labels},
                 ensure_ascii=False), flush=True)
assert all(checks.values())
