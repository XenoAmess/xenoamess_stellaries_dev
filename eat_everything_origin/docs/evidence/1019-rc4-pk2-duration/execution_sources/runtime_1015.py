"""Single production Mod, Chinese-only 1015 regression; independent run pointer."""
import json
import logging
import sys
import time
from pathlib import Path
import runtime as r

sys.stdout.reconfigure(encoding="utf-8")
logging.disable(logging.INFO)
h = r.harness
root = Path.home() / "AppData/Local/xenoamess_stellaries_dev/artifacts/1015-implementation"
root.mkdir(parents=True, exist_ok=True)
h.RUNTIME_ROOT = root / "runs"
h.CURRENT_RUN = root / "current-run.json"
h.WORKSHOP_ID = "eep-1015"
h.PROFILE_ID = "1015-single-production-mod-4.5.2"


def held_click(x, y, stage):
    artifacts, _, _ = h.load_run()
    hwnd = h.focus_pid(int(h.process_record(artifacts)["pid"]))
    rect = h.win32gui.GetClientRect(hwnd)
    assert 0 <= x < rect[2] and 0 <= y < rect[3]
    point = h.win32gui.ClientToScreen(hwnd, (x, y))
    h.pyautogui.moveTo(*point, duration=.1)
    time.sleep(.25)
    h.pyautogui.mouseDown()
    try:
        time.sleep(.15)
    finally:
        h.pyautogui.mouseUp()
    result = {"stage": stage, "client_point": [x, y], "desktop_point": list(point), "hold_seconds": .15}
    h.write_json(artifacts / (stage + ".action.json"), result)
    return result


h.click_point = held_click
r.gpu_click = held_click


def exact_click_text(target, stage):
    frame = h.capture(stage)
    needle = h.normalized(target)
    rows = [row for row in frame["rows"]
            if h.normalized(row["text"]) == needle and row["score"] >= .8]
    if len(rows) != 1:
        raise RuntimeError("Native UI label is missing or ambiguous: " + target)
    box = rows[0]["box"]
    return held_click(round(sum(p[0] for p in box) / 4),
                      round(sum(p[1] for p in box) / 4), stage + "-click")


h.click_text = exact_click_text
r.gpu_click_text = exact_click_text


def acknowledge_notifications(labels, stage, limit=8):
    """Acknowledge only caller-supplied exact native option labels."""
    allowed = {h.normalized(label) for label in labels}
    for index in range(limit):
        h.pyautogui.moveTo(20, 650)
        frame = h.capture(f"{stage}-{index}")
        rows = [row for row in frame["rows"]
                if h.normalized(row["text"]) in allowed and row["score"] >= .8]
        if not rows:
            return {"acknowledged": index, "last_image": frame["image"],
                    "unrecognized_windows": "Require caller inspection before further input"}
        if len(rows) != 1:
            raise RuntimeError("Multiple native acknowledgement labels are visible")
        box = rows[0]["box"]
        held_click(round(sum(p[0] for p in box) / 4),
                   round(sum(p[1] for p in box) / 4), f"{stage}-{index}-ack")
    raise RuntimeError("Notification acknowledgement limit reached")


def wait_for_native_date(expected, stage, timeout_seconds=600):
    """Observe the real HUD date after fast_forward; never infer completion."""
    artifacts, _, _ = h.load_run()
    deadline = time.monotonic() + timeout_seconds
    index = 0
    while time.monotonic() < deadline:
        frame = h.capture(f"{stage}-{index}")
        if any(row["text"] == expected and row["score"] >= .8
               for row in frame["rows"]):
            h.write_json(artifacts / (stage + ".wait.json"), {
                "status": "UI_DATE_OBSERVED", "expected": expected,
                "frame": frame["image"], "polls": index + 1,
            })
            return frame
        index += 1
        time.sleep(min(10, max(0, deadline - time.monotonic())))
    h.write_json(artifacts / (stage + ".wait.json"), {
        "status": "TIMEOUT", "expected": expected, "polls": index,
    })
    raise RuntimeError("Native date was not observed before timeout: " + expected)


def prepare(seed=None, large=False):
    gate = json.loads((root / "static-gate.json").read_text(encoding="utf-8"))
    assert gate["status"] == "PASS"
    assert gate["source_tree_sha256"] == h.tree_manifest(h.MOD_ROOT)[1], "Stale package check"
    report = Path(gate["report"])
    assert h.sha256(report) == gate["report_sha256"]
    assert json.loads(report.read_text(encoding="utf-8"))["status"] == "PASS"
    h.EXPECTED_MOD_TREE_SHA256 = gate["source_tree_sha256"]
    data = h.prepare("l_simp_chinese", [], Path(seed) if seed else None)
    user = Path(data["userdir"])
    settings = Path.home() / "AppData/Local/xenoamess_stellaries_dev/runs/20261014T163036Z/settings.txt"
    text = settings.read_text(encoding="utf-8")
    if large:
        text = text.replace("x=1024", "x=1920").replace("y=768", "y=1080").replace("gui_scale=0.750000", "gui_scale=1.000000")
    (user / "settings.txt").write_text(text, encoding="utf-8")
    designs = r.ROOT / "testing/1015-user-empires.txt"
    (user / "user_empire_designs_v3.4.txt").write_bytes(designs.read_bytes())
    data["test_empire_designs_sha256"] = h.sha256(designs)
    data["static_gate"] = gate
    data["display"] = {"settings_size": [1920, 1080] if large else [1024, 768], "gui_scale": 1.0 if large else .75}
    data["scope"] = "1015 only; old natural Terravore acceptance remains stopped."
    h.write_json(Path(data["artifact_dir"]) / "manifest.json", data)
    return {"run_id": data["run_id"], "userdir": data["userdir"], "artifact_dir": data["artifact_dir"]}


if __name__ == "__main__":
    if sys.argv[1] == "prepare-1015":
        print(json.dumps(prepare(sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "new" else None, "--large" in sys.argv)))
    elif sys.argv[1] == "native-save":
        print(json.dumps(r.native_save(sys.argv[2], sys.argv[3], (0,)), ensure_ascii=False))
    elif sys.argv[1] == "native-load":
        print(json.dumps(r.native_load(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    else:
        h.main()
