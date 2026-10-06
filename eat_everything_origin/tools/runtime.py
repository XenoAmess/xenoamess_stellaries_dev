"""Chinese-only isolated runtime entry; reuses the repository's desktop harness."""
import sys
import json
import time
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "tools"))
import stellaris_acceptance as harness

harness.MOD_ROOT = ROOT / "mod"
harness.GAME_EXE = Path(r"C:\SteamLibrary\steamapps\common\Stellaris\stellaris.exe")
harness.EXPECTED_EXE_SHA256 = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
harness.EXPECTED_MOD_TREE_SHA256 = harness.tree_manifest(harness.MOD_ROOT)[1]
harness.WORKSHOP_ID = "eep-local"
harness.PROFILE_ID = "heart-of-devouring-4.5.2"
harness.RUNTIME_ROOT = REPO / "_runtime/heart-of-devouring/runs"
harness.CURRENT_RUN = harness.RUNTIME_ROOT / "current-run.json"
harness.DIRECTX_REDIST_CAB = Path(r"D:\program files (x86)\steam\steamapps\common\Steamworks Shared\_CommonRedist\DirectX\Jun2010\Jun2010_d3dx9_43_x64.cab")

# Explicit opt-in; the manifest hashes the resulting fixture package.
if "--fixture" in sys.argv:
    sys.argv.remove("--fixture")
    fixture = json.loads((REPO / "_runtime/heart-of-devouring/current-fixture.json").read_text(encoding="utf-8"))
    harness.MOD_ROOT = Path(fixture["root"]) / "mod"
    harness.EXPECTED_MOD_TREE_SHA256 = harness.tree_manifest(harness.MOD_ROOT)[1]

base_settings = harness.render_pdx_settings
def windowed_settings(language):
    return base_settings(language).replace('value="borderless_fullscreen"', 'value="windowed"').replace('value="2560x1440"', 'value="1600x900"')
harness.render_pdx_settings = windowed_settings

# GDI/PrintWindow on this machine return an empty or stale desktop. Steam's
# screenshot hook captures the actual D3D9 backbuffer. Require a fresh file.
STEAM_SCREENSHOTS = Path(r"D:\program files (x86)\steam\userdata")
def gpu_capture(stage):
    artifacts, _, _ = harness.load_run()
    pid = int(harness.process_record(artifacts)["pid"])
    hwnd = harness.focus_pid(pid)
    pattern = "*/760/remote/281990/screenshots/*.jpg"
    before = {str(p): p.stat().st_mtime_ns for p in STEAM_SCREENSHOTS.glob(pattern)}
    harness.press_scan_code(0x58, stage + "-f12", 1)
    deadline = time.monotonic() + 12
    source = None
    while time.monotonic() < deadline:
        fresh = [p for p in STEAM_SCREENSHOTS.glob(pattern)
                 if p.stat().st_mtime_ns > before.get(str(p), 0)]
        if fresh:
            source = max(fresh, key=lambda p: p.stat().st_mtime_ns)
            time.sleep(0.2)
            break
        time.sleep(0.1)
    if source is None:
        raise RuntimeError("Steam F12 did not produce a fresh GPU screenshot")
    image_path = artifacts / (stage + ".jpg")
    shutil.copyfile(source, image_path)
    from PIL import Image
    frame = Image.open(image_path)
    output = harness.RapidOCR()(frame)
    rows = []
    boxes = output.boxes if output.boxes is not None else []
    texts = output.txts if output.txts is not None else []
    scores = output.scores if output.scores is not None else []
    for box, label, score in zip(boxes, texts, scores, strict=True):
        rows.append({"text": str(label), "score": round(float(score), 5),
                     "box": [[round(float(x), 2), round(float(y), 2)] for x, y in box]})
    result = {"stage": stage, "captured_at_utc": datetime.now(timezone.utc).isoformat(),
              "pid": pid, "window_title": harness.win32gui.GetWindowText(hwnd),
              "image": str(image_path), "image_sha256": harness.sha256(image_path),
              "capture": "fresh Steam F12 GPU backbuffer", "resolution": list(frame.size),
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
def gpu_click(x, y, stage):
    action = base_click(*desktop_point(x, y), stage)
    action["client_point"] = [x, y]
    artifacts, _, _ = harness.load_run()
    harness.write_json(artifacts / (stage + ".action.json"), action)
    return action
def gpu_click_text(target, stage):
    result = gpu_capture(stage)
    needle = harness.normalized(target)
    choices = [r for r in result["rows"] if needle in harness.normalized(r["text"]) and r["score"] >= .5]
    if not choices:
        raise RuntimeError("OCR target not found: " + target)
    row = max(choices, key=lambda r: r["score"])
    return gpu_click(round(sum(p[0] for p in row["box"]) / 4),
                     round(sum(p[1] for p in row["box"]) / 4), stage + "-click")
def gpu_scroll(clicks, x, y, stage, repeat):
    return base_scroll(clicks, *desktop_point(x, y), stage, repeat)
def gpu_drag(x1, y1, x2, y2, duration, stage):
    return base_drag(*desktop_point(x1, y1), *desktop_point(x2, y2), duration, stage)
harness.capture = gpu_capture
harness.click_point = gpu_click
harness.click_text = gpu_click_text
harness.scroll = gpu_scroll
harness.drag = gpu_drag

base_type = harness.type_text
def physical_submit(value, submit, stage):
    artifacts, _, _ = harness.load_run()
    harness.focus_pid(int(harness.process_record(artifacts)["pid"]))
    harness.pyautogui.write(value, interval=0.04)
    action = {"action": "type_text", "stage": stage, "text": value, "submitted": False,
              "typed_at_utc": datetime.now(timezone.utc).isoformat(), "key_interval_seconds": .04}
    if submit:
        harness.press_scan_code(0x1c, stage + "-enter", 1)
        action["submitted"] = True
        action["submit_input"] = "physical scan code 0x1c"
    harness.write_json(artifacts / (stage + ".action.json"), action)
    return action
harness.type_text = physical_submit

def native_save(stage, expected_date):
    """Save through Chinese native UI, then audit the newly written file."""
    import re
    import audit_save
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", stage):
        raise ValueError("save stage must be a unique ASCII filename")
    artifacts, userdir, _ = harness.load_run()
    destination = artifacts / (stage + ".sav")
    if destination.exists():
        raise RuntimeError("refusing to overwrite an archived native save")
    before = {str(p): p.stat().st_mtime_ns for p in (userdir / "save games").rglob("*.sav")}
    def exact(frame, label):
        rows = [r for r in frame["rows"] if r["text"] == label and r["score"] >= .8]
        if len(rows) != 1:
            raise RuntimeError("native UI label is missing or ambiguous: " + label)
        return rows[0]
    def click_row(row, action):
        return gpu_click(round(sum(p[0] for p in row["box"]) / 4),
                         round(sum(p[1] for p in row["box"]) / 4), action)
    for attempt in range(4):
        frame = gpu_capture(f"{stage}-menu-{attempt}")
        labels = {r["text"] for r in frame["rows"]}
        if "恢复游戏" in labels and "载入游戏" in labels:
            click_row(exact(frame, "保存游戏"), stage + "-open-save")
            break
        harness.press_scan_code(0x01, f"{stage}-esc-{attempt}", 1)
    else:
        raise RuntimeError("Chinese native main menu did not open")
    dialog = gpu_capture(stage + "-save-dialog")
    save_button = exact(dialog, "保存")
    x = round(sum(p[0] for p in save_button["box"]) / 4)
    y = round(sum(p[1] for p in save_button["box"]) / 4)
    # The name edit and save button share a row in the original save window.
    gpu_click(x - 240, y, stage + "-name-field")
    harness.press(["ctrl", "a"], 1)
    harness.type_text(stage, False, stage + "-name")
    click_row(save_button, stage + "-save-click")
    deadline = time.monotonic() + 15
    source = None
    while time.monotonic() < deadline:
        changed = [p for p in (userdir / "save games").rglob(stage + ".sav")
                   if p.stat().st_mtime_ns > before.get(str(p), 0)]
        if changed:
            source = max(changed, key=lambda p: p.stat().st_mtime_ns)
            time.sleep(1)
            break
        time.sleep(.2)
    if source is None:
        gpu_capture(stage + "-save-not-written")
        raise RuntimeError("native UI did not write the requested new save")
    shutil.copyfile(source, destination)
    result = audit_save.audit(destination)
    harness.write_json(artifacts / (stage + ".audit.json"), result)
    if result["date"] != expected_date:
        raise RuntimeError(f"native save date differs: {result['date']} != {expected_date}")
    harness.press_scan_code(0x01, stage + "-close-menu", 1)
    return result

vanilla = "--vanilla" in sys.argv
quick = "--quick" in sys.argv
if vanilla: sys.argv.remove("--vanilla")
if quick: sys.argv.remove("--quick")
base_prepare = harness.prepare
def prepared_variant(*args, **kwargs):
    data = base_prepare(*args, **kwargs)
    # Windowed dimensions use the game's generated legacy graphics.size,
    # independently of fullscreen_resolution in pdx_settings.txt.
    legacy_settings = ('language="l_simp_chinese"\n'
                       'graphics={ size={ x=1600 y=900 } gui_scale=1.0 '
                       'fullScreen=no borderless=no renderer=1 }\n')
    legacy_path = Path(data["userdir"]) / "settings.txt"
    legacy_path.write_text(legacy_settings, encoding="utf-8", newline="\n")
    data["window_settings_sha256"] = harness.sha256(legacy_path)
    data["display"] = {"requested_mode": "windowed", "fullscreen_resolution_setting": [1600, 900], "actual": "recorded by GPU capture/client rectangle"}
    if vanilla:
        data["enabled_mods"] = []
        data["role"] = "vanilla Chinese environment control"
        harness.write_json(Path(data["userdir"]) / "dlc_load.json", {"enabled_mods": [], "disabled_dlcs": []})
    if quick:
        data["launch_args"].append("-quick")
        data["experimental_quick"] = True
    harness.write_json(Path(data["artifact_dir"]) / "manifest.json", data)
    return data
harness.prepare = prepared_variant

if __name__ == "__main__":
    harness.main()
