"""Update the existing Laoda Workshop item to v0.1.2; never create an item."""

from __future__ import annotations

import argparse
import ctypes as C
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from publish_workshop import APP_ID, MEDIA, MOD, ROOT, TITLE, Steam, StringArray, SubmitItemUpdateResult
from verify_workshop import public_details


ITEM_ID = 3807817109
VERSION = "0.1.2"
PREVIOUS_UPDATED = 1790345259
PREVIOUS_CONTENT = "1456108296541887760"
PREVIOUS_DESCRIPTION_SHA256 = "bf52dad7b935493c2ec8daef1583c318354974c9d213ea7b41cf57ee7cf80392"
THUMBNAIL_SHA256 = "89269b3da6cea8a0071fbd61b285414e8e04ac69a4dcfad6545ed55399efc520"
DDS_SHA256 = "a35c0431498c6b8511bed0604517ba629695edad86e0556c277019d0bbbbf071"
PORTRAIT_SHA256 = "70c05b267415576635831cef640283f7df3c1d1f719e1fd8ba444bd7323e51b4"
STATE = ROOT / "evidence/v0.1.2/update-state.json"
DESCRIPTION = ROOT / "workshop/description.bbcode"
NOTE = ROOT / "workshop/change-note-v0.1.2.txt"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preflight() -> dict:
    if (ROOT / "workshop/item-id.txt").read_text(encoding="utf-8").strip() != str(ITEM_ID):
        raise RuntimeError("Local item ID does not match the existing Laoda Workshop item")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    note = NOTE.read_text(encoding="utf-8").strip()
    description = DESCRIPTION.read_bytes()
    if version != VERSION or f'version="{VERSION}"' not in descriptor or f"## [{VERSION}]" not in changelog:
        raise RuntimeError("VERSION, descriptor, or formal changelog differs from v0.1.2")
    if f'name="{TITLE}"' not in descriptor or 'picture="thumbnail.png"' not in descriptor or 'supported_version="4.5.*"' not in descriptor:
        raise RuntimeError("Descriptor title, thumbnail, or supported version changed unexpectedly")
    if "remote_file_id" in descriptor:
        raise RuntimeError("Release descriptor must match remote package without a local Workshop ID")
    if not note.startswith("[v0.1.2]") or len(description) >= 8000 or len(re.findall(rb"\[img\].*?\[/img\]", description)) != 2:
        raise RuntimeError("Change Note or BBCode does not meet release contract")
    if "这张原始 Steam F12 截图也是工坊主预览图" in description.decode("utf-8"):
        raise RuntimeError("Description still claims the old screenshot is the main preview")
    expected = {
        "descriptor.mod",
        "thumbnail.png",
        "gfx/models/portraits/xenoamess_cetana_laoda_portrait.dds",
        "gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt",
    }
    actual = {path.relative_to(MOD).as_posix() for path in MOD.rglob("*") if path.is_file()}
    if actual != expected:
        raise RuntimeError(f"Unexpected release files: {actual ^ expected}")
    source = ROOT / "assets/reference/thumbnail-v0.1.2.png"
    thumbnail = MOD / "thumbnail.png"
    if source.read_bytes() != thumbnail.read_bytes() or sha256(thumbnail.read_bytes()) != THUMBNAIL_SHA256 or thumbnail.stat().st_size >= 1_000_000:
        raise RuntimeError("Thumbnail differs from the user ZIP or exceeds Steam preview size")
    portrait = MOD / "gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt"
    dds = MOD / "gfx/models/portraits/xenoamess_cetana_laoda_portrait.dds"
    if sha256(portrait.read_bytes()) != PORTRAIT_SHA256 or sha256(dds.read_bytes()) != DDS_SHA256:
        raise RuntimeError("Game portrait content differs from v0.1.1")
    accepted = (
        ROOT / "evidence/portrait-acceptance-rc1/after-restart.jpg",
        ROOT / "evidence/portrait-acceptance-rc1/cetana-dialogue.jpg",
    )
    if any(media.read_bytes() != original.read_bytes() for media, original in zip(MEDIA, accepted)):
        raise RuntimeError("Original in-game screenshots differ from accepted evidence")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT.parent):
        raise RuntimeError("Git worktree must be clean before updating the public item")

    details = public_details(ITEM_ID)
    if (
        details.get("result") != 1
        or details.get("creator_app_id") != APP_ID
        or details.get("consumer_app_id") != APP_ID
        or details.get("title") != TITLE
        or details.get("visibility") != 0
        or str(details.get("hcontent_file")) != PREVIOUS_CONTENT
        or details.get("time_updated") != PREVIOUS_UPDATED
        or sha256(details.get("description", "").encode("utf-8")) != PREVIOUS_DESCRIPTION_SHA256
    ):
        raise RuntimeError("Existing Workshop item differs from the reviewed v0.1.1 baseline")
    with urllib.request.urlopen(details["preview_url"], timeout=30) as response:
        old_preview = response.read()
    if old_preview != MEDIA[0].read_bytes():
        raise RuntimeError("Existing main preview differs from the reviewed F12 screenshot")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT.parent, text=True).strip()
    return {
        "item_id": ITEM_ID,
        "version": VERSION,
        "head": head,
        "previous_time_updated": PREVIOUS_UPDATED,
        "previous_content_handle": PREVIOUS_CONTENT,
        "content": {name: sha256((MOD / name).read_bytes()) for name in sorted(expected)},
        "description_sha256": sha256(description),
        "note_sha256": sha256(note.encode("utf-8")),
        "thumbnail_sha256": THUMBNAIL_SHA256,
    }


def save_state(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE)


def update(inputs: dict) -> None:
    if STATE.exists():
        raise RuntimeError(f"Update state already exists; inspect the remote item before retrying: {STATE}")
    steam = Steam()
    state = {"schema": "laoda-workshop-update-v1", "started_at_utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs}
    try:
        handle = steam.call("StartItemUpdate", APP_ID, ITEM_ID)
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed for the existing Laoda item")
        state["stage"] = "started"
        save_state(state)

        def checked(method: str, *args) -> None:
            if not steam.call(method, handle, *args):
                raise RuntimeError(f"Steamworks {method} returned false")

        checked("SetItemTitle", TITLE.encode("utf-8"))
        checked("SetItemDescription", DESCRIPTION.read_bytes())
        checked("SetItemContent", os.fsencode(str(MOD.resolve())))
        checked("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve())))
        checked("SetItemVisibility", 0)
        strings = (C.c_char_p * 2)(b"Graphics", b"Leaders")
        checked("SetItemTags", C.byref(StringArray(strings, 2)))
        checked("AddItemPreviewFile", os.fsencode(str(MEDIA[0].resolve())), 0)
        state["stage"] = "staged"
        state["new_primary_preview"] = "thumbnail.png"
        state["new_additional_preview"] = MEDIA[0].name
        save_state(state)

        state["stage"] = "submitting"
        save_state(state)
        note = NOTE.read_text(encoding="utf-8").strip()
        submitted = steam.wait(steam.call("SubmitItemUpdate", handle, note.encode("utf-8")), SubmitItemUpdateResult, 3404)
        state.update(
            stage="submitted",
            submit_result=submitted.result,
            submit_item_id=submitted.item_id,
            legal_agreement_required=bool(submitted.legal),
            submitted_at_utc=datetime.now(timezone.utc).isoformat(),
        )
        save_state(state)
        print(json.dumps({"result": submitted.result, "item_id": submitted.item_id, "legal": bool(submitted.legal)}, ensure_ascii=False), flush=True)
        if submitted.result != 1 or submitted.item_id != ITEM_ID or submitted.legal:
            raise RuntimeError("Workshop update did not complete successfully")
    finally:
        steam.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="submit the prepared v0.1.2 update")
    parser.add_argument("--connection-check", action="store_true", help="also check the Steam account without uploading")
    args = parser.parse_args()
    inputs = preflight()
    print(json.dumps(inputs, ensure_ascii=False, indent=2), flush=True)
    if args.connection_check:
        steam = Steam()
        try:
            print("Steamworks: logged on; App ID 281990", flush=True)
        finally:
            steam.close()
    if args.update:
        update(inputs)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"update_workshop: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
