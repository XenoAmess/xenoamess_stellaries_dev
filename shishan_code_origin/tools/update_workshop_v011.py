"""Update owned Shishan Code Workshop item to the frozen v0.1.1 release."""

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

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from synthetic_queen_laoda_replacement.tools.publish_workshop import Steam, SubmitItemUpdateResult


APP_ID = 281990
ITEM_ID = 3810136486
VERSION = "0.1.1"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
STATE = ROOT / f"evidence/v{VERSION}/publish-state.json"
MANIFEST = WORKSHOP / f"screenshots-v{VERSION}.json"
RAW_PREFIX = "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/main/"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preflight() -> dict:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise RuntimeError("VERSION mismatch")
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8")
    if f'version="{VERSION}"' not in descriptor or 'supported_version="4.5.*"' not in descriptor:
        raise RuntimeError("descriptor version or compatibility mismatch")
    if "remote_file_id" in descriptor:
        raise RuntimeError("production descriptor must not carry a Workshop ID")
    if f"## [{VERSION}]" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        raise RuntimeError("formal changelog missing")
    if int((WORKSHOP / "item-id.txt").read_text(encoding="ascii").strip()) != ITEM_ID:
        raise RuntimeError("item ID mismatch")
    description = (WORKSHOP / "description.bbcode").read_bytes()
    if len(description) >= 8000 or b"Mod v0.1.1" not in description:
        raise RuntimeError("description length or version invalid")
    note = (WORKSHOP / f"change-note-v{VERSION}.txt").read_bytes().strip()
    if not note.startswith(b"[v0.1.1]"):
        raise RuntimeError("Change Note does not start with [v0.1.1]")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    images = manifest["images"]
    urls = re.findall(r"\[img\](https://[^\s\[]+)\[/img\]", description.decode("utf-8"))
    if len(images) < 5 or urls != [image["url"] for image in images]:
        raise RuntimeError("BBCode images do not match screenshot manifest")
    for image in images:
        source = image["source"]
        if not source.startswith("assets/shishan-code-origin/evidence/") or image["url"] != RAW_PREFIX + source:
            raise RuntimeError(f"unsafe screenshot source or URL: {source}")
        path = REPO / source
        data = path.read_bytes()
        if len(data) >= 1_000_000 or not data.startswith(b"\xff\xd8\xff"):
            raise RuntimeError(f"Workshop preview must be JPEG under 1 MB: {source}")
        if sha(data) != image["sha256"] or len(data) != image["bytes"]:
            raise RuntimeError(f"screenshot differs from manifest: {source}")
        if subprocess.run(["git", "ls-files", "--error-unmatch", "--", source], cwd=REPO,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            raise RuntimeError(f"screenshot not committed: {source}")
    files = {p.relative_to(MOD).as_posix(): sha(p.read_bytes())
             for p in MOD.rglob("*") if p.is_file()}
    if len(files) != 64 or not (MOD / "thumbnail.png").is_file():
        raise RuntimeError("unexpected production Mod package")
    changed = subprocess.check_output(
        ["git", "status", "--porcelain", "--", str(ROOT.relative_to(REPO) / "mod"),
         str(ROOT.relative_to(REPO) / "VERSION"), str(ROOT.relative_to(REPO) / "CHANGELOG.md"),
         str(ROOT.relative_to(REPO) / "workshop"), "assets/shishan-code-origin/evidence"],
        cwd=REPO, text=True,
    )
    if changed.strip():
        raise RuntimeError("release source or evidence must be committed before publication")
    return {
        "version": VERSION,
        "item_id": ITEM_ID,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "content": dict(sorted(files.items())),
        "description_sha256": sha(description),
        "description_bytes": len(description),
        "note_sha256": sha(note),
        "primary_preview_sha256": sha((MOD / "thumbnail.png").read_bytes()),
        "screenshots": images,
    }


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temp = STATE.with_suffix(".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(STATE)


def publish(inputs: dict) -> None:
    if STATE.exists():
        raise RuntimeError(f"existing submission receipt; refusing duplicate update: {STATE}")
    steam = Steam()
    state = {"schema": "shishan-workshop-update-v1",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs}
    try:
        handle = steam.call("StartItemUpdate", APP_ID, ITEM_ID)
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")

        def checked(method: str, *args: object) -> None:
            if not steam.call(method, handle, *args):
                raise RuntimeError(f"Steamworks {method} returned false")

        checked("SetItemDescription", (WORKSHOP / "description.bbcode").read_bytes())
        checked("SetItemContent", os.fsencode(str(MOD.resolve())))
        checked("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve())))
        checked("SetItemVisibility", 0)
        for image in inputs["screenshots"]:
            checked("AddItemPreviewFile", os.fsencode(str((REPO / image["source"]).resolve())), 0)
        state["staged_preview_count"] = len(inputs["screenshots"])
        save_state(state)
        note = (WORKSHOP / f"change-note-v{VERSION}.txt").read_bytes().strip()
        result = steam.wait(steam.call("SubmitItemUpdate", handle, note), SubmitItemUpdateResult, 3404)
        state.update(submit_result=result.result, submit_item_id=result.item_id,
                     legal_agreement_required=bool(result.legal),
                     completed_at_utc=datetime.now(timezone.utc).isoformat())
        save_state(state)
        print(json.dumps({"result": result.result, "item_id": result.item_id,
                          "legal": bool(result.legal)}, ensure_ascii=False), flush=True)
        if result.result != 1 or result.item_id != ITEM_ID or result.legal:
            raise RuntimeError("Workshop update did not complete safely")
    finally:
        steam.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection-check", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    inputs = preflight()
    print(json.dumps({"version": VERSION, "item_id": ITEM_ID, "head": inputs["head"],
                      "mod_files": len(inputs["content"]), "screenshots": len(inputs["screenshots"]),
                      "description_bytes": inputs["description_bytes"]}, ensure_ascii=False), flush=True)
    if args.connection_check:
        steam = Steam()
        try:
            print("Steamworks: logged on", flush=True)
        finally:
            steam.close()
    if args.publish:
        publish(inputs)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"update_workshop_v011: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
