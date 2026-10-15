"""Chinese isolated desktop runner for the documented feedback regression.

Game/Steam paths are explicit overrides. Importing this module configures the
existing desktop harness; only commands under main perform desktop actions.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "tools"))
import stellaris_acceptance as harness

harness.MOD_ROOT = Path(os.environ.get("SHISHAN_RUNTIME_MOD", str(ROOT / "mod"))).resolve()
harness.GAME_EXE = Path(os.environ.get("STELLARIS_EXE", r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe")).resolve()
harness.EXPECTED_EXE_SHA256 = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
harness.EXPECTED_MOD_TREE_SHA256 = harness.tree_manifest(harness.MOD_ROOT)[1]
harness.WORKSHOP_ID = "shishan-feedback-local"
harness.PROFILE_ID = "shishan-feedback-4.5.2-20261015"
harness.RUNTIME_ROOT = REPO / "_runtime/shishan_code/20261015-runtime/runs"
harness.CURRENT_RUN = harness.RUNTIME_ROOT / "current-run.json"
STEAM_ROOT = Path(os.environ.get("STEAM_ROOT", r"C:\Program Files (x86)\Steam")).resolve()
os.environ.setdefault("STEAM_EXE", str(STEAM_ROOT / "steam.exe"))
harness.DIRECTX_REDIST_CAB = STEAM_ROOT / "steamapps/common/Steamworks Shared/_CommonRedist/DirectX/Jun2010/Jun2010_d3dx9_43_x64.cab"

original_settings = harness.render_pdx_settings
harness.render_pdx_settings = lambda language: original_settings(language).replace('value="borderless_fullscreen"', 'value="windowed"').replace('value="2560x1440"', 'value="1600x900"')
original_prepare = harness.prepare


def prepare(*args, **kwargs):
    result = original_prepare(*args, **kwargs)
    settings = ('language="l_simp_chinese"\n'
                'graphics={ size={ x=1600 y=900 } gui_scale=0.75 '
                'fullScreen=no borderless=no renderer=1 }\n')
    destination = Path(result["userdir"]) / "settings.txt"
    destination.write_text(settings, encoding="utf-8", newline="\n")
    result["display"] = {"requested_mode": "windowed", "requested_size": [1600, 900],
                         "requested_gui_scale": .75, "observed": "recorded by captures"}
    result["window_settings_sha256"] = harness.sha256(destination)
    result["scope"] = "feedback regression; no other mod enabled; Chinese only"
    result["role"] = ("formal production candidate" if harness.MOD_ROOT == (ROOT / "mod").resolve()
                      else "controlled fixture package; inspect manifest file hashes")
    harness.write_json(Path(result["artifact_dir"]) / "manifest.json", result)
    return result


harness.prepare = prepare
OCR = None


def capture(stage):
    """Capture a new Steam GPU frame; fail rather than reuse an earlier image."""
    global OCR
    artifacts, _, _ = harness.load_run()
    pid = int(harness.process_record(artifacts)["pid"])
    hwnd = harness.focus_pid(pid)
    pattern = "*/760/remote/281990/screenshots/*.jpg"
    screenshot_root = STEAM_ROOT / "userdata"
    before = {str(p): p.stat().st_mtime_ns for p in screenshot_root.glob(pattern)}
    harness.press_scan_code(0x58, stage + "-f12", 1)
    deadline = time.monotonic() + 12
    source = None
    while time.monotonic() < deadline:
        fresh = [p for p in screenshot_root.glob(pattern)
                 if p.stat().st_mtime_ns > before.get(str(p), 0)]
        if fresh:
            source = max(fresh, key=lambda p: p.stat().st_mtime_ns)
            time.sleep(.3)
            break
        time.sleep(.2)
    if source is None:
        raise RuntimeError("Steam F12 did not create a fresh game image")
    image_path = artifacts / (stage + ".jpg")
    if image_path.exists():
        raise FileExistsError("capture stage already exists: " + stage)
    shutil.copyfile(source, image_path)
    from PIL import Image
    frame = Image.open(image_path)
    if OCR is None:
        OCR = harness.RapidOCR()
    output = OCR(frame)
    rows = []
    for box, label, score in zip(output.boxes if output.boxes is not None else [],
                                 output.txts if output.txts is not None else [],
                                 output.scores if output.scores is not None else [], strict=True):
        rows.append({"text": str(label), "score": round(float(score), 5),
                     "box": [[round(float(x), 2), round(float(y), 2)] for x, y in box]})
    result = {"stage": stage, "image": str(image_path), "image_sha256": harness.sha256(image_path),
              "captured_at_utc": harness.datetime.now(harness.timezone.utc).isoformat(),
              "pid": pid, "resolution": list(frame.size), "capture": "fresh Steam F12 GPU backbuffer",
              "client_origin": list(harness.win32gui.ClientToScreen(hwnd, (0, 0))),
              "client_rect": list(harness.win32gui.GetClientRect(hwnd)), "rows": rows}
    harness.write_json(artifacts / (stage + ".ocr.json"), result)
    return result


base_click = harness.click_point
base_scroll = harness.scroll
base_drag = harness.drag


def desktop_point(x, y):
    artifacts, _, _ = harness.load_run()
    hwnd = harness.focus_pid(int(harness.process_record(artifacts)["pid"]))
    return harness.win32gui.ClientToScreen(hwnd, (x, y))


def click_point(x, y, stage):
    result = base_click(*desktop_point(x, y), stage)
    result["client_point"] = [x, y]
    return result


def click_text(target, stage):
    frame = capture(stage)
    needle = harness.normalized(target)
    matches = [r for r in frame["rows"] if needle in harness.normalized(r["text"]) and r["score"] >= .6]
    if len(matches) != 1:
        raise RuntimeError(f"OCR target missing or ambiguous: {target}: {len(matches)}")
    box = matches[0]["box"]
    return click_point(round(sum(p[0] for p in box) / 4), round(sum(p[1] for p in box) / 4), stage + "-click")


harness.capture = capture
harness.click_point = click_point
harness.click_text = click_text
harness.scroll = lambda clicks, x, y, stage, repeat: base_scroll(clicks, *desktop_point(x, y), stage, repeat)
harness.drag = lambda x1, y1, x2, y2, duration, stage: base_drag(*desktop_point(x1, y1), *desktop_point(x2, y2), duration, stage)


def console(command, stage):
    """Caller verifies the console is closed before this recorded command."""
    if not command.isascii() or "\n" in command or "\r" in command:
        raise ValueError("console command must be one ASCII line")
    artifacts, _, _ = harness.load_run()
    hwnd = harness.focus_pid(int(harness.process_record(artifacts)["pid"]))
    # An expanded sidebar can retain keyboard focus after the console opens.
    # Reset modifiers/layout before opening and focus the observed input field.
    for key in ("ctrl", "shift", "alt", "winleft", "winright"):
        harness.pyautogui.keyUp(key)
    import ctypes
    english = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 0x00000001)
    harness.win32gui.PostMessage(hwnd, 0x0050, 0, english)
    harness.pyautogui.moveTo(*desktop_point(1200, 750))
    time.sleep(.2)
    harness.press_scan_code(0x29, stage + "-open", 1)
    time.sleep(.3)
    click_point(200, 317, stage + "-input-focus")
    harness.press(["ctrl", "a"], 1)
    harness.pyautogui.write(command, interval=.025)
    harness.press_scan_code(0x1c, stage + "-enter", 1)
    time.sleep(.4)
    result = capture(stage + "-result")
    harness.press_scan_code(0x29, stage + "-close", 1)
    harness.write_json(artifacts / (stage + ".console.json"), {"command": command, "result_image": result["image"]})
    return result


def native_save(name):
    """Save through the actual Chinese menu, archive new ZIP bytes and hash."""
    import re
    import zipfile
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name):
        raise ValueError("native save name must be a short unique ASCII label")
    artifacts, userdir, _ = harness.load_run()
    destination = artifacts / (name + ".sav")
    if destination.exists():
        raise FileExistsError(destination)
    save_root = userdir / "save games"
    before = {str(p): p.stat().st_mtime_ns for p in save_root.rglob("*.sav")}

    def exact(frame, text):
        rows = [r for r in frame["rows"] if r["text"] == text and r["score"] >= .75]
        if len(rows) != 1:
            raise RuntimeError(f"native save UI label missing/ambiguous: {text}")
        box = rows[0]["box"]
        return round(sum(p[0] for p in box) / 4), round(sum(p[1] for p in box) / 4)

    for attempt in range(4):
        frame = capture(f"{name}-menu-{attempt}")
        if "保存游戏" in {r["text"] for r in frame["rows"]}:
            click_point(*exact(frame, "保存游戏"), name + "-open-save")
            break
        harness.press_scan_code(0x01, f"{name}-esc-{attempt}", 1)
    else:
        raise RuntimeError("native Chinese save menu did not open")
    time.sleep(.4)
    frame = capture(name + "-save-dialog")
    x, y = exact(frame, "保存")
    click_point(x - 240, y, name + "-name-field")
    harness.press(["ctrl", "a"], 1)
    harness.pyautogui.write(name, interval=.04)
    click_point(x, y, name + "-save-click")
    source = None
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        fresh = [p for p in save_root.rglob(name + ".sav")
                 if p.stat().st_mtime_ns > before.get(str(p), 0)]
        if fresh:
            source = max(fresh, key=lambda p: p.stat().st_mtime_ns)
            time.sleep(1)
            break
        time.sleep(.2)
    if source is None:
        capture(name + "-not-written")
        raise RuntimeError("native save filename was not written; inspect UI")
    shutil.copyfile(source, destination)
    with zipfile.ZipFile(destination) as archive:
        meta = archive.read("meta").decode("utf-8-sig")
        game = archive.read("gamestate").decode("utf-8-sig")
    result = {"source": str(source), "archived": str(destination),
              "sha256": harness.sha256(destination), "bytes": destination.stat().st_size,
              "meta": meta, "gamestate_bytes": len(game.encode("utf-8")),
              "provenance": "new file written by native Chinese Save UI"}
    harness.write_json(artifacts / (name + ".native-save.json"), result)
    harness.press_scan_code(0x01, name + "-close-save-menu", 1)
    return result


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "console":
        if len(sys.argv) != 4:
            raise SystemExit("console requires COMMAND STAGE")
        print(json.dumps(console(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2))
    elif len(sys.argv) >= 2 and sys.argv[1] == "native-save":
        if len(sys.argv) != 3:
            raise SystemExit("native-save requires NAME")
        print(json.dumps(native_save(sys.argv[2]), ensure_ascii=False, indent=2))
    else:
        raise SystemExit(harness.main())
