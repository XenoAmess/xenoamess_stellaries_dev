"""Publish the first Synthetic Queen item with the installed Steamworks DLL.

Run without arguments for a read-only preflight, or with --publish exactly once.
The new item ID is recorded immediately after CreateItem returns so a failure
cannot silently create a duplicate on the next invocation.
"""

from __future__ import annotations

import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone


APP_ID = 281990
VERSION = "0.1.0"
TITLE = "XenoAmess的合成女王美化"
UPSTREAM_ID = 3710613857
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
STATE = ROOT / "evidence/v0.1.0/publish-state.json"
DLL = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris\steam_api64.dll")
MEDIA = (
    WORKSHOP / "media/01-dialogue.jpg",
    WORKSHOP / "media/02-second-response.jpg",
    WORKSHOP / "media/03-after-restart.jpg",
)


class CreateItemResult(C.Structure):
    _fields_ = [("result", C.c_int32), ("item_id", C.c_uint64), ("legal", C.c_bool)]


class SubmitItemUpdateResult(C.Structure):
    _fields_ = [("result", C.c_int32), ("legal", C.c_bool), ("item_id", C.c_uint64)]


class StringArray(C.Structure):
    _fields_ = [("strings", C.POINTER(C.c_char_p)), ("count", C.c_int32)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight() -> dict:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8")
    description = (WORKSHOP / "description.bbcode").read_bytes()
    note = (WORKSHOP / "change-note-v0.1.0.txt").read_text(encoding="utf-8").strip()
    if version != VERSION or f'version="{VERSION}"' not in descriptor:
        raise RuntimeError("VERSION and descriptor do not match the frozen release")
    if f'name="{TITLE}"' not in descriptor or 'picture="thumbnail.png"' not in descriptor:
        raise RuntimeError("title or thumbnail is missing from descriptor")
    if "remote_file_id" in descriptor:
        raise RuntimeError("content descriptor must not carry a remote item ID")
    if not note.startswith(f"[v{VERSION}]") or len(description) >= 8000:
        raise RuntimeError("change note or description violates Steam limits")
    if len(re.findall(rb"\[img\].*?\[/img\]", description)) != len(MEDIA):
        raise RuntimeError("BBCode must contain all three screenshot links")
    actual = {str(p.relative_to(MOD)).replace("\\", "/") for p in MOD.rglob("*") if p.is_file()}
    expected = {
        "descriptor.mod", "thumbnail.png",
        "gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt",
        "gfx/models/portraits/xenoamess_cetana_portrait.dds",
    }
    if actual != expected:
        raise RuntimeError(f"unexpected production files: {actual ^ expected}")
    if sha256(MOD / "gfx/models/portraits/xenoamess_cetana_portrait.dds") != "5225d045670268844f539ef1ec21eec094149efcaf796af1667d82145a4732d4":
        raise RuntimeError("accepted portrait DDS changed")
    for image in (MOD / "thumbnail.png", *MEDIA):
        if not image.is_file() or image.stat().st_size >= 1_000_000:
            raise RuntimeError(f"invalid Workshop preview: {image}")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO):
        raise RuntimeError("Git worktree must be clean before publication")
    return {
        "version": version,
        "head": head,
        "content": {name: sha256(MOD / name) for name in sorted(expected)},
        "description_sha256": hashlib.sha256(description).hexdigest(),
        "description_bytes": len(description),
        "note_sha256": hashlib.sha256(note.encode("utf-8")).hexdigest(),
        "preview": {p.name: sha256(p) for p in (MOD / "thumbnail.png", *MEDIA)},
    }


def save_state(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE)


class Steam:
    def __init__(self) -> None:
        if not DLL.is_file():
            raise RuntimeError(f"Steamworks DLL missing: {DLL}")
        os.environ["SteamAppId"] = str(APP_ID)
        os.environ["SteamGameId"] = str(APP_ID)
        self.dll = C.WinDLL(str(DLL))
        self.dll.SteamAPI_Init.restype = C.c_bool
        if not self.dll.SteamAPI_Init():
            raise RuntimeError("SteamAPI_Init failed; verify the Steam client is logged in")
        self.dll.SteamAPI_GetHSteamUser.restype = C.c_int32
        user = self.dll.SteamAPI_GetHSteamUser()
        interface = self.dll.SteamInternal_FindOrCreateUserInterface
        interface.argtypes = [C.c_int32, C.c_char_p]
        interface.restype = C.c_void_p
        self.ugc = interface(user, b"STEAMUGC_INTERFACE_VERSION017")
        self.utils = interface(user, b"SteamUtils009")
        self.user = interface(user, b"SteamUser020")
        if not self.ugc or not self.utils or not self.user:
            raise RuntimeError("Steamworks UGC, Utils, or User interface unavailable")
        self.fn("SteamAPI_ISteamUtils_GetAppID", [C.c_void_p], C.c_uint32)
        self.fn("SteamAPI_ISteamUser_BLoggedOn", [C.c_void_p], C.c_bool)
        if self.dll.SteamAPI_ISteamUtils_GetAppID(self.utils) != APP_ID:
            raise RuntimeError("Steamworks App ID does not match Stellaris")
        if not self.dll.SteamAPI_ISteamUser_BLoggedOn(self.user):
            raise RuntimeError("Steam client is in Offline Mode or the account is not logged on")
        self.fn("SteamAPI_ISteamUGC_CreateItem", [C.c_void_p, C.c_uint32, C.c_int32], C.c_uint64)
        self.fn("SteamAPI_ISteamUGC_StartItemUpdate", [C.c_void_p, C.c_uint32, C.c_uint64], C.c_uint64)
        for method in ("SetItemTitle", "SetItemDescription", "SetItemContent", "SetItemPreview"):
            self.fn(f"SteamAPI_ISteamUGC_{method}", [C.c_void_p, C.c_uint64, C.c_char_p], C.c_bool)
        self.fn("SteamAPI_ISteamUGC_SetItemVisibility", [C.c_void_p, C.c_uint64, C.c_int32], C.c_bool)
        self.fn("SteamAPI_ISteamUGC_SetItemTags", [C.c_void_p, C.c_uint64, C.POINTER(StringArray)], C.c_bool)
        self.fn("SteamAPI_ISteamUGC_AddItemPreviewFile", [C.c_void_p, C.c_uint64, C.c_char_p, C.c_int32], C.c_bool)
        self.fn("SteamAPI_ISteamUGC_SubmitItemUpdate", [C.c_void_p, C.c_uint64, C.c_char_p], C.c_uint64)
        self.fn("SteamAPI_ISteamUtils_IsAPICallCompleted", [C.c_void_p, C.c_uint64, C.POINTER(C.c_bool)], C.c_bool)
        self.fn("SteamAPI_ISteamUtils_GetAPICallResult", [C.c_void_p, C.c_uint64, C.c_void_p, C.c_int32, C.c_int32, C.POINTER(C.c_bool)], C.c_bool)

    def fn(self, name: str, args: list, result: type):
        function = getattr(self.dll, name)
        function.argtypes = args
        function.restype = result
        return function

    def call(self, name: str, *args):
        return getattr(self.dll, f"SteamAPI_ISteamUGC_{name}")(self.ugc, *args)

    def wait(self, handle: int, result_type: type, callback_id: int, timeout: int = 600):
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("Steam API returned invalid call handle")
        deadline = time.monotonic() + timeout
        failed = C.c_bool()
        while time.monotonic() < deadline:
            self.dll.SteamAPI_RunCallbacks()
            done = self.dll.SteamAPI_ISteamUtils_IsAPICallCompleted(self.utils, handle, C.byref(failed))
            if done:
                result = result_type()
                ok = self.dll.SteamAPI_ISteamUtils_GetAPICallResult(
                    self.utils, handle, C.byref(result), C.sizeof(result), callback_id, C.byref(failed)
                )
                if not ok or failed.value:
                    raise RuntimeError(f"Steam API callback {callback_id} failed")
                return result
            time.sleep(0.1)
        raise TimeoutError(f"Steam API callback {callback_id} timed out")

    def close(self) -> None:
        self.dll.SteamAPI_Shutdown()


def publish(inputs: dict) -> dict:
    if STATE.exists():
        raise RuntimeError(f"publication state already exists; refusing to create another item: {STATE}")
    steam = Steam()
    state = {"schema": "synthetic-queen-workshop-v1", "created_at_utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs}
    try:
        created = steam.wait(steam.call("CreateItem", APP_ID, 0), CreateItemResult, 3403)
        state.update(create_result=created.result, item_id=created.item_id, legal_agreement_required=bool(created.legal))
        save_state(state)
        print(f"CreateItem: result={created.result}, id={created.item_id}, legal={bool(created.legal)}", flush=True)
        if created.result != 1 or not created.item_id or created.item_id == UPSTREAM_ID:
            raise RuntimeError("new Workshop item was not created safely")
        if created.legal:
            raise RuntimeError("Workshop legal agreement requires the user to accept it before public upload")
        handle = steam.call("StartItemUpdate", APP_ID, created.item_id)
        if handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")

        def checked(method: str, *args) -> None:
            if not steam.call(method, handle, *args):
                raise RuntimeError(f"Steamworks {method} returned false")

        checked("SetItemTitle", TITLE.encode("utf-8"))
        checked("SetItemDescription", (WORKSHOP / "description.bbcode").read_bytes())
        checked("SetItemContent", os.fsencode(str(MOD.resolve())))
        checked("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve())))
        checked("SetItemVisibility", 0)  # Public
        strings = (C.c_char_p * 2)(b"Graphics", b"Leaders")
        tags = StringArray(strings, 2)
        checked("SetItemTags", C.byref(tags))
        for image in MEDIA:
            checked("AddItemPreviewFile", os.fsencode(str(image.resolve())), 0)
        state["staged_preview_files"] = [p.name for p in MEDIA]
        save_state(state)
        note = (WORKSHOP / "change-note-v0.1.0.txt").read_text(encoding="utf-8").strip()
        submitted = steam.wait(steam.call("SubmitItemUpdate", handle, note.encode("utf-8")), SubmitItemUpdateResult, 3404)
        state.update(submit_result=submitted.result, submit_item_id=submitted.item_id, submit_legal_agreement_required=bool(submitted.legal))
        save_state(state)
        print(f"SubmitItemUpdate: result={submitted.result}, id={submitted.item_id}, legal={bool(submitted.legal)}", flush=True)
        if submitted.result != 1 or submitted.item_id != created.item_id or submitted.legal:
            raise RuntimeError("Workshop submission did not complete successfully")
        return state
    finally:
        steam.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="create and submit a new public item")
    args = parser.parse_args()
    inputs = preflight()
    print(json.dumps(inputs, ensure_ascii=False, indent=2), flush=True)
    if args.publish:
        publish(inputs)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"publish_workshop: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
