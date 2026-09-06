"""Isolated desktop harness for the iteration-1 Stellaris baseline.

The harness copies the unmodified production mod into a disposable userdir,
starts the exact pinned game build, and records screenshots/OCR beside a
machine-readable manifest. It never reads or writes the player's real
Documents profile.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def configure_dpi_awareness() -> dict[str, object]:
    """Keep screenshot pixels and UI input coordinates in the same space."""
    if sys.platform != "win32":
        return {"requested": "not_applicable", "effective": "not_windows"}

    requested = "per_monitor_v2"
    request_succeeded = False
    try:
        setter = ctypes.windll.user32.SetProcessDpiAwarenessContext
        setter.argtypes = [ctypes.c_void_p]
        setter.restype = ctypes.c_bool
        request_succeeded = bool(setter(ctypes.c_void_p(-4)))
    except (AttributeError, OSError):
        try:
            setter = ctypes.windll.shcore.SetProcessDpiAwareness
            setter.argtypes = [ctypes.c_int]
            setter.restype = ctypes.c_long
            request_succeeded = setter(2) == 0
            requested = "per_monitor_v1"
        except (AttributeError, OSError):
            requested = "system_aware_fallback"
            request_succeeded = bool(ctypes.windll.user32.SetProcessDPIAware())

    effective = "unknown"
    try:
        get_context = ctypes.windll.user32.GetThreadDpiAwarenessContext
        get_context.restype = ctypes.c_void_p
        get_awareness = ctypes.windll.user32.GetAwarenessFromDpiAwarenessContext
        get_awareness.argtypes = [ctypes.c_void_p]
        get_awareness.restype = ctypes.c_int
        effective = {
            0: "unaware",
            1: "system_aware",
            2: "per_monitor_aware",
        }.get(get_awareness(get_context()), "invalid")
    except (AttributeError, OSError):
        pass
    return {
        "requested": requested,
        "request_succeeded": request_succeeded,
        "effective": effective,
    }


# This must happen before importing screenshot and input libraries.
DPI_AWARENESS = configure_dpi_awareness()

import psutil
import pyautogui
import win32api
import win32con
import win32gui
import win32process
from PIL import ImageGrab
from rapidocr import RapidOCR


ROOT = Path(__file__).resolve().parents[1]
MOD_ROOT = ROOT / "vivhite_infinite_positions" / "mod"
GAME_EXE = Path(os.environ.get(
    "STELLARIS_EXE",
    r"D:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe",
)).resolve()
EXPECTED_EXE_SHA256 = (
    "bc451c72d9654c8901f1bb0bee1dd78d76f415465c2fbf746e9f98ade333173a"
)
EXPECTED_MOD_TREE_SHA256 = (
    "1e676c6d592e6ec093ac2390a71418fede5d9206d6fcf26510501ec8d41a286d"
)
WORKSHOP_ID = "3710613857"
STEAM_APP_ID = "281990"
PROFILE_ID = "stellaris-4.4.6"
SUPPORTED_LANGUAGES = ("l_simp_chinese", "l_english")
RUNTIME_ROOT = ROOT / "_runtime"
CURRENT_RUN = RUNTIME_ROOT / "current-run.json"
DIRECTX_REDIST_CAB = Path(
    r"D:\Program Files (x86)\Steam\steamapps\common\Steamworks Shared"
    r"\_CommonRedist\DirectX\Jun2010\Jun2010_d3dx9_43_x64.cab"
)
pyautogui.FAILSAFE = True

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    files: list[dict[str, object]] = []
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix()
        payload = path.read_bytes()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(payload)
        files.append({
            "path": relative,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    return files, digest.hexdigest()


def inspect_save_file(path: Path, tokens: list[str]) -> dict[str, object]:
    """Inspect one Stellaris ZIP save without extracting it or mutating the run."""
    resolved = path.resolve()
    if not resolved.is_file():
        raise RuntimeError(f"save not found: {resolved}")
    if not zipfile.is_zipfile(resolved):
        raise RuntimeError(f"save is not a ZIP container: {resolved}")
    if any(not token or "\r" in token or "\n" in token for token in tokens):
        raise ValueError("save inspection tokens must be non-empty single-line strings")

    with zipfile.ZipFile(resolved, "r") as archive:
        members = archive.namelist()
        if "gamestate" not in members:
            raise RuntimeError(f"save has no gamestate member: {resolved}")
        gamestate = archive.read("gamestate")
    counts = {
        token: gamestate.count(token.encode("utf-8"))
        for token in tokens
    }
    return {
        "schema": "xenoamess.stellaris.save-inspection.v1",
        "save": str(resolved),
        "bytes": resolved.stat().st_size,
        "sha256": sha256(resolved),
        "zip_members": members,
        "gamestate_bytes": len(gamestate),
        "gamestate_sha256": hashlib.sha256(gamestate).hexdigest(),
        "token_counts": counts,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def copy_seed_save(source: Path, save_root: Path) -> dict[str, object]:
    """Validate and copy one frozen save into an isolated acceptance profile."""
    source_inspection = inspect_save_file(source, [])
    resolved_source = Path(source_inspection["save"])
    if resolved_source.suffix.lower() != ".sav":
        raise ValueError(f"seed save must use the .sav extension: {resolved_source}")

    destination_dir = (save_root / "acceptance-fixtures").resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / resolved_source.name
    shutil.copy2(resolved_source, destination)
    copied_inspection = inspect_save_file(destination, [])
    if (
        source_inspection["bytes"] != copied_inspection["bytes"]
        or source_inspection["sha256"] != copied_inspection["sha256"]
    ):
        raise RuntimeError("copied seed save differs from source")
    return {
        "source": str(resolved_source),
        "copied": str(destination),
        "bytes": copied_inspection["bytes"],
        "sha256": copied_inspection["sha256"],
        "zip_members": copied_inspection["zip_members"],
        "gamestate_bytes": copied_inspection["gamestate_bytes"],
        "gamestate_sha256": copied_inspection["gamestate_sha256"],
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def running_stellaris() -> list[int]:
    return sorted(
        process.pid
        for process in psutil.process_iter(["name"])
        if (process.info.get("name") or "").lower() == "stellaris.exe"
    )


def ensure_runtime_dependencies() -> tuple[Path, list[dict[str, object]]]:
    """Materialize app-local legacy DirectX dependencies without elevation."""
    dependency_dir = (
        Path(os.environ["LOCALAPPDATA"])
        / "xenoamess_stellaries_dev" / "runtime_dependencies" / "directx_jun2010_x64"
    ).resolve()
    dependency = dependency_dir / "d3dx9_43.dll"
    dependency_dir.mkdir(parents=True, exist_ok=True)
    if not dependency.is_file():
        if not DIRECTX_REDIST_CAB.is_file():
            raise RuntimeError(f"DirectX redist CAB not found: {DIRECTX_REDIST_CAB}")
        subprocess.run(
            ["expand.exe", "-F:d3dx9_43.dll", str(DIRECTX_REDIST_CAB), str(dependency_dir)],
            check=True,
            capture_output=True,
        )
    return dependency_dir, [{
        "path": str(dependency),
        "bytes": dependency.stat().st_size,
        "sha256": sha256(dependency),
        "source": str(DIRECTX_REDIST_CAB),
    }]


def render_pdx_settings(language: str) -> str:
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"unsupported acceptance language: {language}")
    return (
        '"game"={\n'
        '\t"cloud_save"={ version=0 enabled=no }\n'
        '}\n'
        '"Graphics"={\n'
        '\t"display_mode"={ version=0 value="borderless_fullscreen" }\n'
        '\t"display_index"={ version=0 value="0" }\n'
        '\t"fullscreen_resolution"={ version=0 value="2560x1440" }\n'
        '}\n'
        '"System"={\n'
        f'\t"language"={{ version=0 value="{language}" }}\n'
        '}\n'
    )


def render_scheduled_commands(entries: list[str]) -> str:
    lines = []
    for entry in entries:
        date, separator, command = entry.partition("=")
        date = date.strip()
        command = command.strip()
        if not separator or not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", date):
            raise ValueError(
                f"scheduled command must use YYYY.MM.DD=COMMAND: {entry}"
            )
        if not command or any(character in command for character in '\r\n"'):
            raise ValueError(f"unsafe scheduled command: {entry}")
        lines.append(f'{date} = "{command}"')
    return "\n".join(lines) + ("\n" if lines else "")


def prepare(
    language: str,
    scheduled_commands: list[str],
    seed_save: Path | None = None,
) -> dict[str, object]:
    if running_stellaris():
        raise RuntimeError("refusing to prepare while stellaris.exe is running")
    if not GAME_EXE.is_file():
        raise RuntimeError(f"Stellaris executable not found: {GAME_EXE}")
    exe_hash = sha256(GAME_EXE)
    if exe_hash != EXPECTED_EXE_SHA256:
        raise RuntimeError(
            f"Stellaris executable hash drift: {exe_hash} != {EXPECTED_EXE_SHA256}"
        )
    if not (MOD_ROOT / "descriptor.mod").is_file():
        raise RuntimeError(f"production mod is incomplete: {MOD_ROOT}")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_dir = (RUNTIME_ROOT / run_id).resolve()
    local_app_data = Path(os.environ["LOCALAPPDATA"]).resolve()
    userdir = (local_app_data / "xenoamess_stellaries_dev" / "runs" / run_id).resolve()
    if artifact_dir.exists() or userdir.exists():
        raise RuntimeError(f"run id collision: {run_id}")

    artifact_dir.mkdir(parents=True)
    (userdir / "logs").mkdir(parents=True)
    (userdir / "save games").mkdir(parents=True)
    copied_mod = userdir / "mod" / WORKSHOP_ID
    copied_mod.parent.mkdir(parents=True)
    shutil.copytree(MOD_ROOT, copied_mod)

    descriptor = (copied_mod / "descriptor.mod").read_text(encoding="utf-8-sig")
    if not descriptor.endswith("\n"):
        descriptor += "\n"
    outer_descriptor = descriptor + f'path="{copied_mod.as_posix()}"\n'
    (userdir / "mod" / f"ugc_{WORKSHOP_ID}.mod").write_text(
        outer_descriptor, encoding="utf-8", newline="\n"
    )
    write_json(userdir / "dlc_load.json", {
        "enabled_mods": [f"mod/ugc_{WORKSHOP_ID}.mod"],
        "disabled_dlcs": [],
    })
    (userdir / "pdx_settings.txt").write_text(
        render_pdx_settings(language), encoding="utf-8", newline="\n"
    )
    if scheduled_commands:
        (userdir / "commands_at_date.txt").write_text(
            render_scheduled_commands(scheduled_commands),
            encoding="utf-8",
            newline="\n",
        )
    seeded_save = (
        copy_seed_save(seed_save, userdir / "save games")
        if seed_save is not None
        else None
    )

    source_files, source_tree_hash = tree_manifest(MOD_ROOT)
    copied_files, copied_tree_hash = tree_manifest(copied_mod)
    if source_tree_hash != EXPECTED_MOD_TREE_SHA256:
        raise RuntimeError(
            "production mod drifted from the iteration-1 baseline: "
            f"{source_tree_hash} != {EXPECTED_MOD_TREE_SHA256}"
        )
    if source_tree_hash != copied_tree_hash or source_files != copied_files:
        raise RuntimeError("copied production mod differs from repository source")

    launch_args = [
        str(GAME_EXE),
        "-gdpr-compliant",
        "-debug_mode",
        f"-userdir={userdir}",
    ]
    manifest: dict[str, object] = {
        "schema": "xenoamess.stellaris.acceptance-run.v1",
        "run_id": run_id,
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile_id": PROFILE_ID,
        "game_exe": str(GAME_EXE),
        "game_exe_sha256": exe_hash,
        "workshop_id": WORKSHOP_ID,
        "repository_mod": str(MOD_ROOT),
        "repository_mod_tree_sha256": source_tree_hash,
        "repository_mod_files": source_files,
        "copied_mod": str(copied_mod),
        "copied_mod_tree_sha256": copied_tree_hash,
        "userdir": str(userdir),
        "artifact_dir": str(artifact_dir),
        "launch_args": launch_args,
        "enabled_mods": [f"mod/ugc_{WORKSHOP_ID}.mod"],
        "language": language,
        "scheduled_commands": scheduled_commands,
        "seeded_save": seeded_save,
        "display": {"mode": "borderless_fullscreen", "resolution": [2560, 1440]},
    }
    write_json(artifact_dir / "manifest.json", manifest)
    write_json(CURRENT_RUN, {"artifact_dir": str(artifact_dir), "userdir": str(userdir)})
    return manifest


def load_run() -> tuple[Path, Path, dict[str, object]]:
    if not CURRENT_RUN.is_file():
        raise RuntimeError("no prepared run; invoke prepare first")
    pointer = json.loads(CURRENT_RUN.read_text(encoding="utf-8"))
    artifact_dir = Path(pointer["artifact_dir"]).resolve()
    userdir = Path(pointer["userdir"]).resolve()
    manifest = json.loads((artifact_dir / "manifest.json").read_text(encoding="utf-8"))
    return artifact_dir, userdir, manifest


def inspect_save(save_name: str | None, tokens: list[str]) -> dict[str, object]:
    artifact_dir, userdir, _ = load_run()
    save_root = (userdir / "save games").resolve()
    candidates = sorted(
        (path.resolve() for path in save_root.rglob("*.sav") if path.is_file()),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    if save_name:
        candidates = [
            path for path in candidates
            if path.name == save_name or path.stem == save_name
        ]
    if not candidates:
        label = save_name or "latest *.sav"
        raise RuntimeError(f"no matching save under isolated userdir: {label}")
    if save_name and len(candidates) > 1:
        raise RuntimeError(f"multiple isolated saves match {save_name}: {candidates}")

    result = inspect_save_file(candidates[0], tokens)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", candidates[0].stem)
    write_json(artifact_dir / f"save-inspection-{safe_name}.json", result)
    return result


def windows_for_pid(pid: int) -> list[int]:
    found: list[int] = []

    def callback(hwnd: int, _: object) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, owner_pid = win32process.GetWindowThreadProcessId(hwnd)
        if owner_pid == pid and win32gui.GetWindowText(hwnd):
            found.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return found


def focus_pid(pid: int) -> int:
    foreground = win32gui.GetForegroundWindow()
    if foreground:
        _, foreground_pid = win32process.GetWindowThreadProcessId(foreground)
        try:
            foreground_process = psutil.Process(foreground_pid).name().lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            foreground_process = ""
        if foreground_process == "lockapp.exe":
            raise RuntimeError(
                "the Windows desktop is locked; unlock it before UI capture/input"
            )
    windows = windows_for_pid(pid)
    if not windows:
        raise RuntimeError(f"no visible window belongs to Stellaris PID {pid}")
    hwnd = windows[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        pyautogui.press("alt")
        win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    return hwnd


def process_record(artifact_dir: Path) -> dict[str, object]:
    path = artifact_dir / "process.json"
    if not path.is_file():
        raise RuntimeError("run has not been launched")
    return json.loads(path.read_text(encoding="utf-8"))


def capture(stage: str) -> dict[str, object]:
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    pid = int(record["pid"])
    if not psutil.pid_exists(pid):
        raise RuntimeError(f"Stellaris PID {pid} is not running")
    hwnd = focus_pid(pid)
    image = ImageGrab.grab()
    image_path = artifact_dir / f"{stage}.png"
    image.save(image_path)
    output = RapidOCR()(image)
    rows: list[dict[str, object]] = []
    boxes = output.boxes if output.boxes is not None else []
    texts = output.txts if output.txts is not None else []
    scores = output.scores if output.scores is not None else []
    for box, text, score in zip(boxes, texts, scores, strict=True):
        points = [[round(float(x), 2), round(float(y), 2)] for x, y in box]
        rows.append({"text": str(text), "score": round(float(score), 5), "box": points})
    result = {
        "stage": stage,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "pid": pid,
        "window_title": win32gui.GetWindowText(hwnd),
        "image": str(image_path),
        "image_sha256": sha256(image_path),
        "resolution": list(image.size),
        "input_desktop_size": list(pyautogui.size()),
        "dpi_awareness": DPI_AWARENESS,
        "ocr_seconds": round(float(output.elapse or 0), 3),
        "rows": rows,
    }
    write_json(artifact_dir / f"{stage}.ocr.json", result)
    return result


def normalized(text: str) -> str:
    return "".join(text.lower().split())


def click_text(target: str, stage: str) -> dict[str, object]:
    result = capture(stage)
    needle = normalized(target)
    candidates = [
        row for row in result["rows"]
        if needle in normalized(str(row["text"])) and float(row["score"]) >= 0.5
    ]
    if not candidates:
        raise RuntimeError(f"OCR target not found: {target}")
    selected = max(candidates, key=lambda row: float(row["score"]))
    box = selected["box"]
    x = round(sum(point[0] for point in box) / len(box))
    y = round(sum(point[1] for point in box) / len(box))
    pyautogui.click(x, y)
    action = {
        "action": "click_text",
        "target": target,
        "matched": selected,
        "point": [x, y],
        "clicked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    artifact_dir, _, _ = load_run()
    write_json(artifact_dir / f"{stage}.action.json", action)
    return action


def click_point(x: int, y: int, stage: str) -> dict[str, object]:
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    width, height = pyautogui.size()
    if not 0 <= x < width or not 0 <= y < height:
        raise ValueError(f"point outside desktop {width}x{height}: ({x}, {y})")
    pyautogui.click(x, y)
    action = {
        "action": "click_point",
        "stage": stage,
        "point": [x, y],
        "clicked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", action)
    return action


def scroll(clicks: int, x: int, y: int, stage: str, repeat: int) -> dict[str, object]:
    if repeat < 1:
        raise ValueError("scroll repeat must be at least one")
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    width, height = pyautogui.size()
    if not 0 <= x < width or not 0 <= y < height:
        raise ValueError(f"point outside desktop {width}x{height}: ({x}, {y})")
    pyautogui.moveTo(x, y)
    for _ in range(repeat):
        pyautogui.scroll(clicks)
        time.sleep(0.02)
    action = {
        "action": "scroll",
        "stage": stage,
        "clicks": clicks,
        "repeat": repeat,
        "point": [x, y],
        "scrolled_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", action)
    return action


def drag(x1: int, y1: int, x2: int, y2: int, duration: float, stage: str) -> dict[str, object]:
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    width, height = pyautogui.size()
    for x, y in ((x1, y1), (x2, y2)):
        if not 0 <= x < width or not 0 <= y < height:
            raise ValueError(f"point outside desktop {width}x{height}: ({x}, {y})")
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y2, duration=duration, button="left")
    action = {
        "action": "drag",
        "stage": stage,
        "from": [x1, y1],
        "to": [x2, y2],
        "duration_seconds": duration,
        "dragged_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", action)
    return action


def type_text(value: str, submit: bool, stage: str) -> dict[str, object]:
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    pyautogui.write(value, interval=0.01)
    if submit:
        pyautogui.press("enter")
    action = {
        "action": "type_text",
        "stage": stage,
        "text": value,
        "submitted": submit,
        "typed_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", action)
    return action


def launch(timeout: float, via_steam: bool) -> dict[str, object]:
    artifact_dir, _, manifest = load_run()
    before_pids = set(running_stellaris())
    if before_pids:
        raise RuntimeError("refusing to launch while stellaris.exe is already running")
    args = [str(item) for item in manifest["launch_args"]]
    dependency_dir, dependencies = ensure_runtime_dependencies()
    if via_steam:
        steam_exe = Path(os.environ.get(
            "STEAM_EXE", r"D:\Program Files (x86)\Steam\steam.exe"
        )).resolve()
        if not steam_exe.is_file():
            raise RuntimeError(f"Steam executable not found: {steam_exe}")
        command = [str(steam_exe), "-applaunch", STEAM_APP_ID, *args[1:]]
        launcher = subprocess.Popen(command, cwd=str(steam_exe.parent))
        process = None
    else:
        command = args
        child_environment = os.environ.copy()
        child_environment["PATH"] = str(dependency_dir) + os.pathsep + child_environment["PATH"]
        process = subprocess.Popen(
            command, cwd=str(GAME_EXE.parent), env=child_environment
        )
        launcher = process
    record: dict[str, object] = {
        "launcher_pid": launcher.pid,
        "transport": "steam-applaunch" if via_steam else "direct",
        "command": command,
        "runtime_dependencies": dependencies,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / "process.json", record)
    deadline = time.monotonic() + timeout
    pid: int | None = process.pid if process is not None else None
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            record["early_exit_code"] = process.returncode
            write_json(artifact_dir / "process.json", record)
            raise RuntimeError(f"Stellaris exited before a visible window: {process.returncode}")
        if pid is None:
            candidates = [item for item in running_stellaris() if item not in before_pids]
            if candidates:
                pid = candidates[0]
                record["pid"] = pid
                write_json(artifact_dir / "process.json", record)
        if pid is not None and not psutil.pid_exists(pid):
            raise RuntimeError(f"Stellaris PID {pid} exited before a visible window")
        windows = windows_for_pid(pid) if pid is not None else []
        if windows:
            record["pid"] = pid
            record["window_title"] = win32gui.GetWindowText(windows[0])
            record["window_ready_at_utc"] = datetime.now(timezone.utc).isoformat()
            write_json(artifact_dir / "process.json", record)
            return record
        time.sleep(1)
    raise RuntimeError(f"Stellaris window was not visible within {timeout} seconds")


def status() -> dict[str, object]:
    artifact_dir, userdir, _ = load_run()
    record = process_record(artifact_dir)
    pid = int(record["pid"])
    windows = windows_for_pid(pid) if psutil.pid_exists(pid) else []
    logs = {}
    for name in ("debug.log", "error.log", "game.log", "system.log", "setup.log"):
        path = userdir / "logs" / name
        logs[name] = {"exists": path.is_file(), "bytes": path.stat().st_size if path.is_file() else 0}
    return {
        "pid": pid,
        "running": psutil.pid_exists(pid),
        "windows": [win32gui.GetWindowText(hwnd) for hwnd in windows],
        "logs": logs,
        "userdir": str(userdir),
        "artifact_dir": str(artifact_dir),
    }


def press(keys: list[str], repeat: int) -> dict[str, object]:
    if repeat < 1:
        raise ValueError("key repeat must be at least one")
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    if len(keys) == 1:
        pyautogui.press(keys[0], presses=repeat, interval=0.05)
    else:
        for _ in range(repeat):
            pyautogui.hotkey(*keys)
    result = {
        "action": "press",
        "keys": keys,
        "repeat": repeat,
        "at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"press-{int(time.time() * 1000)}.json", result)
    return result


def press_scan_code(scan_code: int, stage: str, repeat: int) -> dict[str, object]:
    """Send a physical-key scan code to software that ignores virtual keys."""
    if not 0 <= scan_code <= 0xFF:
        raise ValueError(f"scan code outside one-byte range: {scan_code}")
    if repeat < 1:
        raise ValueError("scan-code repeat must be at least one")
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    for _ in range(repeat):
        win32api.keybd_event(0, scan_code, 0x0008, 0)
        time.sleep(0.05)
        win32api.keybd_event(
            0, scan_code, 0x0008 | win32con.KEYEVENTF_KEYUP, 0
        )
        time.sleep(0.03)
    result = {
        "action": "press_scan_code",
        "stage": stage,
        "scan_code": scan_code,
        "repeat": repeat,
        "at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", result)
    return result


def press_scan_chord(scan_codes: list[int], stage: str) -> dict[str, object]:
    """Send a physical-key chord, keeping modifiers held until the last key lifts."""
    if not scan_codes:
        raise ValueError("a physical-key chord requires at least one scan code")
    invalid = [code for code in scan_codes if not 0 <= code <= 0xFF]
    if invalid:
        raise ValueError(f"scan codes outside one-byte range: {invalid}")
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    focus_pid(int(record["pid"]))
    for scan_code in scan_codes:
        win32api.keybd_event(0, scan_code, 0x0008, 0)
        time.sleep(0.03)
    for scan_code in reversed(scan_codes):
        win32api.keybd_event(
            0, scan_code, 0x0008 | win32con.KEYEVENTF_KEYUP, 0
        )
        time.sleep(0.03)
    result = {
        "action": "press_scan_chord",
        "stage": stage,
        "scan_codes": scan_codes,
        "at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(artifact_dir / f"{stage}.action.json", result)
    return result


def stop(timeout: float) -> dict[str, object]:
    artifact_dir, _, _ = load_run()
    record = process_record(artifact_dir)
    pid = int(record["pid"])
    for hwnd in windows_for_pid(pid):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    deadline = time.monotonic() + timeout
    while psutil.pid_exists(pid) and time.monotonic() < deadline:
        time.sleep(0.5)
    forced = False
    if psutil.pid_exists(pid):
        psutil.Process(pid).terminate()
        forced = True
        try:
            psutil.Process(pid).wait(10)
        except psutil.TimeoutExpired:
            psutil.Process(pid).kill()
    result = {
        "pid": pid,
        "stopped_at_utc": datetime.now(timezone.utc).isoformat(),
        "forced": forced,
        "running_after": psutil.pid_exists(pid),
    }
    write_json(artifact_dir / "stop.json", result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument(
        "--language", choices=SUPPORTED_LANGUAGES, default="l_simp_chinese"
    )
    prepare_parser.add_argument(
        "--scheduled-command",
        action="append",
        default=[],
        help="write a userdir commands_at_date entry as YYYY.MM.DD=COMMAND",
    )
    prepare_parser.add_argument(
        "--seed-save",
        type=Path,
        help="copy one validated Stellaris .sav into the isolated profile",
    )
    launch_parser = commands.add_parser("launch")
    launch_parser.add_argument("--timeout", type=float, default=180)
    launch_parser.add_argument("--via-steam", action="store_true")
    capture_parser = commands.add_parser("capture")
    capture_parser.add_argument("stage")
    click_parser = commands.add_parser("click-text")
    click_parser.add_argument("target")
    click_parser.add_argument("--stage", default="before-click")
    click_point_parser = commands.add_parser("click-point")
    click_point_parser.add_argument("x", type=int)
    click_point_parser.add_argument("y", type=int)
    click_point_parser.add_argument("--stage", default="point-click")
    scroll_parser = commands.add_parser("scroll")
    scroll_parser.add_argument("clicks", type=int)
    scroll_parser.add_argument("--x", type=int, default=1400)
    scroll_parser.add_argument("--y", type=int, default=600)
    scroll_parser.add_argument("--stage", default="scroll")
    scroll_parser.add_argument("--repeat", type=int, default=1)
    drag_parser = commands.add_parser("drag")
    drag_parser.add_argument("x1", type=int)
    drag_parser.add_argument("y1", type=int)
    drag_parser.add_argument("x2", type=int)
    drag_parser.add_argument("y2", type=int)
    drag_parser.add_argument("--duration", type=float, default=0.5)
    drag_parser.add_argument("--stage", default="drag")
    type_parser = commands.add_parser("type-text")
    type_parser.add_argument("text")
    type_parser.add_argument("--submit", action="store_true")
    type_parser.add_argument("--stage", default="type-text")
    press_parser = commands.add_parser("press")
    press_parser.add_argument("keys", nargs="+")
    press_parser.add_argument("--repeat", type=int, default=1)
    scan_parser = commands.add_parser("press-scan")
    scan_parser.add_argument("scan_code", type=lambda value: int(value, 0))
    scan_parser.add_argument("--stage", default="press-scan")
    scan_parser.add_argument("--repeat", type=int, default=1)
    chord_parser = commands.add_parser("press-scan-chord")
    chord_parser.add_argument(
        "scan_codes", nargs="+", type=lambda value: int(value, 0)
    )
    chord_parser.add_argument("--stage", default="press-scan-chord")
    save_parser = commands.add_parser("inspect-save")
    save_parser.add_argument(
        "--save",
        help="exact filename or stem under the isolated userdir; defaults to latest",
    )
    save_parser.add_argument(
        "--token",
        action="append",
        default=[],
        help="count an exact UTF-8 token in the gamestate member",
    )
    commands.add_parser("status")
    stop_parser = commands.add_parser("stop")
    stop_parser.add_argument("--timeout", type=float, default=30)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    action = {
        "prepare": lambda: prepare(
            arguments.language,
            arguments.scheduled_command,
            arguments.seed_save,
        ),
        "launch": lambda: launch(arguments.timeout, arguments.via_steam),
        "capture": lambda: capture(arguments.stage),
        "click-text": lambda: click_text(arguments.target, arguments.stage),
        "click-point": lambda: click_point(arguments.x, arguments.y, arguments.stage),
        "scroll": lambda: scroll(
            arguments.clicks,
            arguments.x,
            arguments.y,
            arguments.stage,
            arguments.repeat,
        ),
        "drag": lambda: drag(
            arguments.x1,
            arguments.y1,
            arguments.x2,
            arguments.y2,
            arguments.duration,
            arguments.stage,
        ),
        "type-text": lambda: type_text(
            arguments.text, arguments.submit, arguments.stage
        ),
        "press": lambda: press(arguments.keys, arguments.repeat),
        "press-scan": lambda: press_scan_code(
            arguments.scan_code, arguments.stage, arguments.repeat
        ),
        "press-scan-chord": lambda: press_scan_chord(
            arguments.scan_codes, arguments.stage
        ),
        "inspect-save": lambda: inspect_save(arguments.save, arguments.token),
        "status": lambda: status(),
        "stop": lambda: stop(arguments.timeout),
    }[arguments.command]
    try:
        print(json.dumps(action(), ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        print(json.dumps({
            "status": "ERROR",
            "type": type(error).__name__,
            "message": str(error),
        }, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
