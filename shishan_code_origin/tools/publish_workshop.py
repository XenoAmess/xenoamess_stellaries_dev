"""Create the first Shishan Code Workshop item through the logged-in Steam client."""

from __future__ import annotations

import argparse
import ctypes as C
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from synthetic_queen_laoda_replacement.tools.publish_workshop import (
    CreateItemResult,
    Steam,
    StringArray,
    SubmitItemUpdateResult,
)


APP_ID = 281990
VERSION = "0.1.0"
TITLE = "屎山代码"
FORBIDDEN_IDS = {3710613857, 3797257579, 3800996999, 3807768508}
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
STATE = ROOT / "evidence/v0.1.0/publish-state.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_state(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE)


def preflight() -> dict:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise RuntimeError("VERSION does not match release")
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8")
    if f'version="{VERSION}"' not in descriptor or f'name="{TITLE}"' not in descriptor:
        raise RuntimeError("descriptor version or title differs from release")
    if 'supported_version="4.5.*"' not in descriptor or "remote_file_id" in descriptor:
        raise RuntimeError("descriptor compatibility or Workshop identity is unsafe")
    if f"## [{VERSION}]" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        raise RuntimeError("formal changelog entry is missing")
    description = (WORKSHOP / "description.bbcode").read_bytes()
    note = (WORKSHOP / f"change-note-v{VERSION}.txt").read_text(encoding="utf-8").strip()
    if len(description) >= 8000 or not note.startswith(f"[v{VERSION}]"):
        raise RuntimeError("Workshop description or Change Note is invalid")
    if not (MOD / "thumbnail.png").is_file() or (MOD / "thumbnail.png").stat().st_size >= 1_000_000:
        raise RuntimeError("main preview is missing or too large")
    files = {p.relative_to(MOD).as_posix(): p for p in MOD.rglob("*") if p.is_file()}
    if len(files) != 64 or any(re.search(r"(^|/)(?:test|fixture|evidence|_runtime)(?:/|$)|\.(?:sav|log|py)$", name) for name in files):
        raise RuntimeError("unexpected production package contents")
    if any("shishan_test_society_boost" in p.read_text(encoding="utf-8", errors="ignore") for name, p in files.items() if name.endswith((".txt", ".mod"))):
        raise RuntimeError("test research modifier leaked into the production package")
    changed = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "shishan_code_origin/mod", "shishan_code_origin/VERSION", "shishan_code_origin/CHANGELOG.md", "shishan_code_origin/workshop"],
        cwd=REPO, text=True,
    )
    if changed.strip():
        raise RuntimeError("release source must be committed before publication")
    return {
        "version": VERSION,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "content": {name: digest(p) for name, p in sorted(files.items())},
        "description_sha256": hashlib.sha256(description).hexdigest(),
        "change_note_sha256": hashlib.sha256(note.encode("utf-8")).hexdigest(),
        "preview_sha256": digest(MOD / "thumbnail.png"),
    }


def publish(inputs: dict) -> None:
    if STATE.exists():
        raise RuntimeError(f"creation receipt already exists; refusing a second item: {STATE}")
    steam = Steam()
    state = {"schema": "shishan-workshop-v1", "created_at_utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs}
    try:
        created = steam.wait(steam.call("CreateItem", APP_ID, 0), CreateItemResult, 3403)
        state.update(create_result=created.result, item_id=created.item_id, legal_agreement_required=bool(created.legal))
        save_state(state)
        print(f"CreateItem: result={created.result}, id={created.item_id}, legal={bool(created.legal)}", flush=True)
        if created.result != 1 or not created.item_id or created.item_id in FORBIDDEN_IDS:
            raise RuntimeError("Steam did not safely create a new item")
        if created.legal:
            raise RuntimeError("Workshop legal agreement requires the user to accept it")
        handle = steam.call("StartItemUpdate", APP_ID, created.item_id)
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")

        def checked(method: str, *args) -> None:
            if not steam.call(method, handle, *args):
                raise RuntimeError(f"Steamworks {method} returned false")

        checked("SetItemTitle", TITLE.encode("utf-8"))
        checked("SetItemDescription", (WORKSHOP / "description.bbcode").read_bytes())
        checked("SetItemContent", os.fsencode(str(MOD.resolve())))
        checked("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve())))
        checked("SetItemVisibility", 0)
        strings = (C.c_char_p * 3)(b"Origin", b"Events", b"Leaders")
        checked("SetItemTags", C.byref(StringArray(strings, 3)))
        note = (WORKSHOP / f"change-note-v{VERSION}.txt").read_text(encoding="utf-8").strip()
        submitted = steam.wait(steam.call("SubmitItemUpdate", handle, note.encode("utf-8")), SubmitItemUpdateResult, 3404)
        state.update(submit_result=submitted.result, submit_item_id=submitted.item_id, submit_legal_agreement_required=bool(submitted.legal))
        save_state(state)
        print(f"SubmitItemUpdate: result={submitted.result}, id={submitted.item_id}, legal={bool(submitted.legal)}", flush=True)
        if submitted.result != 1 or submitted.item_id != created.item_id or submitted.legal:
            raise RuntimeError("Workshop content submission failed")
    finally:
        steam.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connection-check", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    inputs = preflight()
    print(json.dumps({"version": inputs["version"], "head": inputs["head"], "file_count": len(inputs["content"]), "description_sha256": inputs["description_sha256"]}, ensure_ascii=False), flush=True)
    if args.connection_check:
        steam = Steam()
        try:
            print("Steamworks: logged on; App ID 281990", flush=True)
        finally:
            steam.close()
    if args.publish:
        publish(inputs)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"publish_workshop: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
