"""Chinese artificial-world regression; reuse the verified native UI harness."""
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import runtime_1019 as previous
import runtime_title_load_1020 as title

b = previous.base
h = b.h
b.ARTIFACTS = Path.home() / "AppData/Local/xenoamess_stellaries_dev/artifacts/artificial-worlds-20261023"
h.RUNTIME_ROOT = b.ARTIFACTS / "runs"
h.CURRENT_RUN = b.ARTIFACTS / "current-run.json"
h.WORKSHOP_ID = "eep-artificial-1023"
h.PROFILE_ID = "eep-0.5.0-artificial-worlds"


def prepare(role, seed=None):
    result = previous.original_prepare(role, seed)
    artifacts = Path(result["artifact_dir"])
    user = Path(result["userdir"])
    settings = user / "settings.txt"
    text = settings.read_text(encoding="utf-8").replace("renderer=1", "renderer=0").replace("multi_sampling=4", "multi_sampling=0")
    settings.write_text(text, encoding="utf-8", newline="\n")
    manifest = json.loads((artifacts / "manifest.json").read_text(encoding="utf-8"))
    manifest.update(scope="0.5.0 artificial-worlds; Chinese habitat functional regression",
                    window_settings_sha256=h.sha256(settings),
                    display={"settings_size": [1024, 768], "gui_scale": .75, "renderer": 0, "multi_sampling": 0})
    h.write_json(artifacts / "manifest.json", manifest)
    return result


b.prepare = prepare


def held_click(x, y, stage, button="left"):
    artifacts, _, _ = h.load_run()
    hwnd = h.focus_pid(int(h.process_record(artifacts)["pid"]))
    rect = h.win32gui.GetClientRect(hwnd)
    if not (0 <= x < rect[2] and 0 <= y < rect[3]):
        raise ValueError("point outside the verified game client")
    point = h.win32gui.ClientToScreen(hwnd, (x, y))
    h.pyautogui.failSafeCheck()
    h.pyautogui.moveTo(*point, duration=.1)
    time.sleep(.25)
    packed = x + (y << 16)
    down = h.win32con.WM_LBUTTONDOWN if button == "left" else h.win32con.WM_RBUTTONDOWN
    up = h.win32con.WM_LBUTTONUP if button == "left" else h.win32con.WM_RBUTTONUP
    key = h.win32con.MK_LBUTTON if button == "left" else h.win32con.MK_RBUTTON
    h.win32gui.SendMessageTimeout(hwnd, h.win32con.WM_MOUSEMOVE, 0, packed, h.win32con.SMTO_ABORTIFHUNG, 2000)
    h.win32gui.SendMessageTimeout(hwnd, down, key, packed, h.win32con.SMTO_ABORTIFHUNG, 2000)
    try:
        time.sleep(.1)
    finally:
        h.win32gui.SendMessageTimeout(hwnd, up, 0, packed, h.win32con.SMTO_ABORTIFHUNG, 2000)
    action = {"stage": stage, "client_point": [x, y], "desktop_point": list(point),
              "method": "standard Win32 mouse messages", "button": button, "pid": int(h.process_record(artifacts)["pid"]),
              "hold_seconds": .1}
    h.write_json(artifacts / (stage + ".action.json"), action)
    return action


def click_text(target, stage):
    frame = h.capture(stage)
    rows = [row for row in frame["rows"]
            if h.normalized(row["text"]) == h.normalized(target) and row["score"] >= .8]
    if len(rows) != 1:
        raise RuntimeError("Native UI label is missing or ambiguous: " + target)
    box = rows[0]["box"]
    return held_click(round(sum(p[0] for p in box) / 4), round(sum(p[1] for p in box) / 4), stage + "-click")


def scroll(clicks, x, y, stage, repeat):
    artifacts, _, _ = h.load_run()
    hwnd = h.focus_pid(int(h.process_record(artifacts)["pid"]))
    rect = h.win32gui.GetClientRect(hwnd)
    if not (0 <= x < rect[2] and 0 <= y < rect[3]) or not 1 <= repeat <= 100:
        raise ValueError("invalid native scroll point or repeat")
    point = h.win32gui.ClientToScreen(hwnd, (x, y))
    h.pyautogui.moveTo(*point, duration=.1)
    delta = int(clicks) * 120
    for _ in range(repeat):
        h.pyautogui.failSafeCheck()
        h.win32gui.SendMessageTimeout(hwnd, h.win32con.WM_MOUSEWHEEL, (delta & 0xffff) << 16,
                                     point[0] + (point[1] << 16), h.win32con.SMTO_ABORTIFHUNG, 2000)
        time.sleep(.1)
    action = {"stage": stage, "method": "standard Win32 WM_MOUSEWHEEL", "client_point": [x, y],
              "wheel_delta": delta, "repeat": repeat}
    h.write_json(artifacts / (stage + ".action.json"), action)
    return action


h.click_point = held_click
h.click_text = click_text
h.scroll = scroll
b.r.gpu_click = held_click
b.r.gpu_click_text = click_text
b.r.gpu_scroll = scroll


def install_fixture(name):
    if not re.fullmatch(r"[a-z_]+", name):
        raise ValueError("explicit fixture basename required")
    source = b.ROOT / "testing/artificial_worlds_1023" / (name + ".txt")
    cli = Path("D:/workspace/open_kaishek/kaishek-cli/target/kaishek-cli-0.1.0-SNAPSHOT.jar")
    parsed = json.loads(subprocess.check_output(["java", "-jar", str(cli), "parse", str(source)]))
    if parsed.get("status") != "PARSED" or parsed.get("diagnostics") or parsed.get("roundTrip") is not True:
        raise RuntimeError("fixture did not pass open_kaishek")
    # Native run consumes console commands, one per line, rather than P effects.
    command = "effect " + " ".join(line.strip() for line in source.read_text(encoding="utf-8").splitlines()
                                   if line.strip() and not line.lstrip().startswith("#"))
    artifacts, user, _ = h.load_run()
    target = user / ("art_" + name + ".txt")
    target.write_text(command, encoding="utf-8", newline="\n")
    h.write_json(artifacts / ("fixture-" + name + ".json"), {
        "source": str(source), "source_sha256": h.sha256(source), "parser": parsed,
        "console_file": str(target), "console_file_sha256": h.sha256(target),
        "command": command, "bytes": len(command.encode("utf-8"))})
    return "run " + target.name


def hud_date_visible(frame, date):
    rows = [row for row in frame["rows"] if row["score"] >= .8]
    dates = [row for row in rows if row["text"] == date
             and min(point[0] for point in row["box"]) > 700
             and max(point[1] for point in row["box"]) <= 40]
    paused = [row for row in rows if row["text"] == "暂停"
              and max(point[1] for point in row["box"]) <= 45]
    resources = [row for row in rows if re.search(r"\d.*\+\d", row["text"])
                 and min(point[0] for point in row["box"]) < 700
                 and max(point[1] for point in row["box"]) <= 40]
    return len(dates) == 1 and (bool(paused) or len(resources) >= 3)


def title_load(save_name, stage):
    artifacts, user, _ = h.load_run()
    paths = list((user / "save games").rglob(save_name + ".sav"))
    if len(paths) != 1:
        raise RuntimeError("source native save is missing or ambiguous")
    import audit_save
    expected = audit_save.audit(paths[0])["date"]
    try:
        title_frame = title.return_to_title(stage)
    except RuntimeError:
        current = h.capture(stage + "-return-diagnostic")
        text = title.labels(current)
        if not (any("放弃游戏并返回主菜单" in value for value in text) and title.EXIT in text):
            raise
        h.press_scan_code(0x1c, stage + "-confirm-visible-exit-enter", 1)
        time.sleep(2)
        title_frame = h.capture(stage + "-title-confirmed")
        if not title.title_visible(title_frame):
            raise RuntimeError("native title menu still not visible")
    original = b.r.native_load(save_name, stage)
    deadline = time.monotonic() + 180
    enter_sent = False
    index = 0
    while time.monotonic() < deadline:
        frame = h.capture(stage + f"-strict-hud-{index}")
        index += 1
        if hud_date_visible(frame, expected):
            result = {"status": "HUD_DATE_VERIFIED_STATE_REQUIRES_NEW_NATIVE_SAVE", "source": str(paths[0]),
                      "source_sha256": h.sha256(paths[0]), "date": expected,
                      "original_receipt": original, "title_image": title_frame["image"],
                      "hud_image": frame["image"], "hud_image_sha256": frame["image_sha256"]}
            h.write_json(artifacts / (stage + ".strict-load.json"), result)
            return result
        text = title.labels(frame)
        if not enter_sent and "读取存档" in text:
            h.press_scan_code(0x1c, stage + "-visible-load-enter", 1)
            enter_sent = True
        time.sleep(1)
    raise RuntimeError("strict native load never reached the real top HUD date")


if __name__ == "__main__":
    if sys.argv[1] == "install-fixture":
        print(install_fixture(sys.argv[2]))
    elif sys.argv[1] == "title-load":
        print(json.dumps(title_load(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif sys.argv[1] == "console-open":
        previous.command_open(sys.argv[2], sys.argv[3])
    else:
        b.main()
