"""Launch an isolated Simplified Chinese Stellaris run for this mod."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "shishan_code_origin" / "mod"
GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    args = parser.parse_args()
    if any(proc.info["name"] and proc.info["name"].lower() == "stellaris.exe"
           for proc in psutil.process_iter(["name"])):
        raise RuntimeError("Stellaris is already running")
    userdir = Path(os.environ["LOCALAPPDATA"]) / "xenoamess_stellaries_dev" / "shishan_runs" / args.id
    evidence = ROOT / "_runtime" / "shishan_code" / args.id
    if userdir.exists() or evidence.exists():
        raise FileExistsError(args.id)
    evidence.mkdir(parents=True)
    (userdir / "logs").mkdir(parents=True)
    (userdir / "save games").mkdir(parents=True)
    copy = userdir / "mod" / "shishan_code_origin"
    shutil.copytree(MOD, copy)
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8-sig")
    (userdir / "mod" / "shishan_code_origin.mod").write_text(
        descriptor.rstrip() + f'\npath="{copy.as_posix()}"\n', encoding="utf-8"
    )
    (userdir / "dlc_load.json").write_text(
        json.dumps({"enabled_mods": ["mod/shishan_code_origin.mod"], "disabled_dlcs": []}),
        encoding="utf-8",
    )
    (userdir / "pdx_settings.txt").write_text(
        '"game"={\n\t"cloud_save"={ version=0 enabled=no }\n}\n'
        '"Graphics"={\n\t"display_mode"={ version=0 value="borderless_fullscreen" }\n}\n'
        '"System"={\n\t"language"={ version=0 value="l_simp_chinese" }\n}\n',
        encoding="utf-8",
    )
    command = [str(GAME), "-gdpr-compliant", "-debug_mode", f"-userdir={userdir}"]
    process = subprocess.Popen(command, cwd=GAME.parent)
    record = {
        "pid": process.pid,
        "userdir": str(userdir),
        "evidence": str(evidence),
        "game_sha256": sha256(GAME),
        "mod_files": len(list(copy.rglob("*"))),
        "command": command,
    }
    (evidence / "launch.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
