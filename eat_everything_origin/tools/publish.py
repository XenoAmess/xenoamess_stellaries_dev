"""Publish only an accepted formal release to its own new Workshop item."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ctypes as C
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import workshop_images
import release_acceptance
from change_note_html import exact_change_note

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
STATE = ROOT / "docs/evidence/publish-state.json"
APP_ID = 281990
TITLE = "吞噬之心"
FORBIDDEN_ID = 3710613857
DOWNLOAD_RECEIPT = ROOT / "docs/evidence/workshop-download.json"
sys.path.insert(0, str(REPO / "synthetic_queen_laoda_replacement/tools"))
import publish_workshop as native
native.DLL = Path(r"C:\SteamLibrary\steamapps\common\Stellaris\steam_api64.dll")


class CallbackMessage(C.Structure):
    _pack_ = 8
    _fields_ = [("user", C.c_int32), ("callback", C.c_int32),
                ("data", C.c_void_p), ("size", C.c_int32)]


class DownloadResult(C.Structure):
    _pack_ = 8
    _fields_ = [("app", C.c_uint32), ("item", C.c_uint64), ("result", C.c_int32)]


def wait_download(steam, pipe, item_id, timeout):
    """Only consume manual callbacks; never mix this with RunCallbacks."""
    deadline = time.monotonic() + timeout
    message = CallbackMessage()
    while time.monotonic() < deadline:
        steam.dll.SteamAPI_ManualDispatch_RunFrame(pipe)
        while steam.dll.SteamAPI_ManualDispatch_GetNextCallback(pipe, C.byref(message)):
            try:
                if message.callback != 3406:
                    continue
                if message.size != C.sizeof(DownloadResult) or not message.data:
                    raise RuntimeError("download callback structure differs from the Windows ABI")
                result = DownloadResult.from_buffer_copy(C.string_at(message.data, message.size))
                if result.app != APP_ID or result.item != item_id:
                    continue
                if result.result != 1:
                    raise RuntimeError(f"Workshop download returned EResult {result.result}")
                return {"callback": 3406, "app_id": result.app, "item_id": result.item,
                        "result": result.result, "callback_bytes": message.size}
            finally:
                steam.dll.SteamAPI_ManualDispatch_FreeLastCallback(pipe)
        time.sleep(.1)
    raise RuntimeError("Workshop download callback timed out")


def download_item(timeout):
    state = json.loads(STATE.read_text(encoding="utf-8"))
    item_id = int(state["item_id"])
    if item_id == FORBIDDEN_ID or state.get("submit_result") != 1 or state.get("submit_item_id") != item_id:
        raise RuntimeError("a successful upload to this mod's new item is required")
    if state["inputs"]["content"] != manifest(MOD):
        raise RuntimeError("production differs from the successfully uploaded content")
    steam = native.Steam()
    try:
        steam.fn("SteamAPI_GetHSteamPipe", [], C.c_int32)
        steam.fn("SteamAPI_ManualDispatch_Init", [], None)
        steam.fn("SteamAPI_ManualDispatch_RunFrame", [C.c_int32], None)
        steam.fn("SteamAPI_ManualDispatch_GetNextCallback", [C.c_int32, C.POINTER(CallbackMessage)], C.c_bool)
        steam.fn("SteamAPI_ManualDispatch_FreeLastCallback", [C.c_int32], None)
        steam.fn("SteamAPI_ISteamUGC_DownloadItem", [C.c_void_p, C.c_uint64, C.c_bool], C.c_bool)
        steam.fn("SteamAPI_ISteamUGC_GetItemState", [C.c_void_p, C.c_uint64], C.c_uint32)
        steam.fn("SteamAPI_ISteamUGC_GetItemInstallInfo", [C.c_void_p, C.c_uint64, C.POINTER(C.c_uint64),
                                                          C.c_void_p, C.c_uint32, C.POINTER(C.c_uint32)], C.c_bool)
        pipe = steam.dll.SteamAPI_GetHSteamPipe()
        if not pipe:
            raise RuntimeError("Steam client pipe unavailable")
        steam.dll.SteamAPI_ManualDispatch_Init()
        if not steam.call("DownloadItem", item_id, False):
            raise RuntimeError("Steam refused to start the Workshop download")
        callback = wait_download(steam, pipe, item_id, timeout)
        item_state = steam.call("GetItemState", item_id)
        if not item_state & 4 or item_state & (2 | 8 | 16 | 32):
            raise RuntimeError(f"Workshop install is incomplete: state {item_state}")
        size, timestamp = C.c_uint64(), C.c_uint32()
        folder = C.create_string_buffer(32768)
        if not steam.call("GetItemInstallInfo", item_id, C.byref(size), folder, C.sizeof(folder), C.byref(timestamp)):
            raise RuntimeError("Steam did not return the downloaded install folder")
        installed = Path(folder.value.decode("utf-8")).resolve(strict=True)
        if not installed.is_dir() or installed == MOD.resolve() or MOD.resolve() in installed.parents:
            raise RuntimeError("download folder is not an independent installed Workshop directory")
        content = manifest(installed)
        if content != state["inputs"]["content"]:
            raise RuntimeError("downloaded Workshop files differ from the uploaded manifest")
        receipt = {"status": "DOWNLOADED", "version": state["version"], "item_id": item_id,
                   "callback": callback, "state": item_state, "folder": str(installed),
                   "size_on_disk": size.value, "install_timestamp": timestamp.value,
                   "content": content, "downloaded_at_utc": datetime.now(timezone.utc).isoformat()}
        write_json(DOWNLOAD_RECEIPT, receipt)
        print(json.dumps({k: receipt[k] for k in ("status", "version", "item_id", "folder")}))
    finally:
        steam.close()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def manifest(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob("*")) if p.is_file()}


def preflight():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise RuntimeError("public publication requires a formal SemVer")
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8")
    if f'version="{version}"' not in descriptor or f'name="{TITLE}"' not in descriptor:
        raise RuntimeError("descriptor differs from VERSION or title")
    if "remote_file_id" in descriptor or str(FORBIDDEN_ID) in descriptor:
        raise RuntimeError("production descriptor must not route to an existing upstream item")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    heading = re.search(rf"^## {re.escape(version)}\s.*$", changelog, re.M)
    if not heading:
        raise RuntimeError("formal changelog entry missing")
    next_heading = re.search(r"^## ", changelog[heading.end():], re.M)
    changelog_entry = changelog[heading.start():heading.end() + next_heading.start()] if next_heading else changelog[heading.start():]
    package = json.loads((ROOT / "docs/evidence/package-release.json").read_text(encoding="utf-8"))
    runtime = json.loads((ROOT / "docs/evidence/runtime-acceptance.json").read_text(encoding="utf-8"))
    files = manifest(MOD)
    if package["status"] != "PASS":
        raise RuntimeError("package acceptance is incomplete")
    if any("eep_probe" in p or p.startswith("testing/") for p in files):
        raise RuntimeError("test fixtures leaked into production")
    note = (WORKSHOP / f"change-note-v{version}.txt").read_text(encoding="utf-8").strip()
    if not note.startswith(f"[v{version}]"):
        raise RuntimeError("Change Note version prefix mismatch")
    description = (WORKSHOP / "description.bbcode").read_text(encoding="utf-8")
    acceptance = release_acceptance.validate_runtime(runtime, files, version, description, note, changelog_entry, ROOT)
    images = workshop_images.local_images(ROOT, version)
    gallery = [entry for entry in images if entry["role"] == "gallery"]
    description += "\n[b]" + "\u56fe\u5e93\u8bf4\u660e" + "[/b]\n" + "\n".join(
        f"{index}. {entry['caption']}" for index, entry in enumerate(gallery, 1)) + "\n"
    if len(description.encode("utf-8")) >= 8000:
        raise RuntimeError("Workshop description exceeds the accepted API limit")
    thumbnail = MOD / "thumbnail.png"
    if thumbnail.stat().st_size >= 1_000_000:
        raise RuntimeError("Workshop thumbnail too large")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO):
        raise RuntimeError("commit task changes before publication")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    return {"version": version, "head": head, "content": files, "description": description,
            "note": note, "images": images, "gallery": gallery, "acceptance": acceptance}


def publish(inputs):
    steam = native.Steam()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {
        "schema": "heart-of-devouring-workshop-v1", "started_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        if state.get("submit_result") == 1:
            raise RuntimeError("this successful version must not be uploaded again")
        if state.get("item_id"):
            if state.get("version") != inputs["version"]:
                raise RuntimeError("retry state belongs to a different version")
        else:
            result = steam.wait(steam.call("CreateItem", APP_ID, 0), native.CreateItemResult, 3403)
            state.update(version=inputs["version"], create_result=result.result, item_id=result.item_id, legal_agreement_required=bool(result.legal))
            write_json(STATE, state)
            if result.result != 1 or not result.item_id:
                raise RuntimeError("CreateItem failed")
        item_id = int(state["item_id"])
        if item_id == FORBIDDEN_ID:
            raise RuntimeError("read-only upstream ID is forbidden")
        if state.get("legal_agreement_required"):
            raise RuntimeError("the account must accept the Workshop agreement before public upload")
        existing_previews = workshop_images.remote_previews(steam, item_id)
        update = steam.call("StartItemUpdate", APP_ID, item_id)
        if not update or update == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")
        for method, value in [
            ("SetItemTitle", TITLE.encode("utf-8")),
            ("SetItemDescription", inputs["description"].encode("utf-8")),
            ("SetItemContent", os.fsencode(str(MOD.resolve()))),
            ("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve()))),
            ("SetItemVisibility", 0),
        ]:
            if not steam.call(method, update, value):
                raise RuntimeError(f"{method} failed")
        strings = (C.c_char_p * 3)(b"Origins", b"Events", b"Gameplay")
        tags = native.StringArray(strings, 3)
        if not steam.call("SetItemTags", update, C.byref(tags)):
            raise RuntimeError("SetItemTags failed")
        workshop_images.replace_previews(steam, update, existing_previews, inputs["gallery"], ROOT)
        state.update(inputs=inputs)
        write_json(STATE, state)
        result = steam.wait(steam.call("SubmitItemUpdate", update, inputs["note"].encode("utf-8")), native.SubmitItemUpdateResult, 3404)
        state.update(submit_result=result.result, submit_item_id=result.item_id, submit_legal_required=bool(result.legal), submitted_at_utc=datetime.now(timezone.utc).isoformat())
        write_json(STATE, state)
        if result.result != 1 or result.item_id != item_id:
            raise RuntimeError("Workshop upload failed; recorded item ID is retained for retry")
        (WORKSHOP / "item-id.txt").write_text(f"{item_id}\n", encoding="ascii")
        print(f"published {item_id}; remote verification still required")
    finally:
        steam.close()


def verify(download):
    state = json.loads(STATE.read_text(encoding="utf-8"))
    item_id = int(state["item_id"])
    if item_id == FORBIDDEN_ID or state.get("submit_result") != 1:
        raise RuntimeError("successful new-item upload receipt missing")
    receipt = json.loads(DOWNLOAD_RECEIPT.read_text(encoding="utf-8"))
    if (receipt.get("status") != "DOWNLOADED" or receipt.get("item_id") != item_id
            or receipt.get("version") != state["version"]
            or Path(receipt["folder"]).resolve() != download.resolve()
            or receipt.get("content") != state["inputs"]["content"]):
        raise RuntimeError("actual Steam Workshop download receipt differs")
    body = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    req = urllib.request.Request("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=body)
    with urllib.request.urlopen(req, timeout=30) as response:
        details = json.load(response)["response"]["publishedfiledetails"][0]
    expected = state["inputs"]
    current_images = workshop_images.local_images(ROOT, expected["version"])
    if current_images != expected["images"]:
        raise RuntimeError("Workshop image manifest changed after upload")
    if any([details.get("result") != 1, details.get("consumer_app_id") != APP_ID, details.get("creator_app_id") != APP_ID, details.get("title") != TITLE, details.get("description") != expected["description"], details.get("visibility") != 0, details.get("banned") != 0]):
        raise RuntimeError("public Workshop metadata differs")
    with urllib.request.urlopen(details["preview_url"], timeout=30) as response:
        if response.read() != (MOD / "thumbnail.png").read_bytes():
            raise RuntimeError("remote preview differs")
    url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=english"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        page = response.read().decode("utf-8", "replace")
    if not exact_change_note(page, expected["note"]):
        raise RuntimeError("versioned Change Note not visible")
    if manifest(download) != expected["content"] or manifest(MOD) != expected["content"]:
        raise RuntimeError("download content differs from frozen production")
    steam = native.Steam()
    try:
        previews = workshop_images.remote_previews(steam, item_id)
    finally:
        steam.close()
    gallery = workshop_images.verify_previews(previews, expected["gallery"])
    report = {"status": "PASS", "version": expected["version"], "item_id": item_id, "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}", "public_metadata_exact": True, "change_note_exact": True, "download_files": len(expected["content"]), "production_files": expected["content"], "gallery_exact": True, "gallery": gallery, "verified_at_utc": datetime.now(timezone.utc).isoformat()}
    write_json(ROOT / "docs/evidence/workshop-verification.json", report)
    print(json.dumps({k: report[k] for k in ["status", "version", "item_id", "url", "download_files"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["preflight", "publish", "download", "verify"])
    parser.add_argument("--download", type=Path)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    if args.command == "download":
        if args.timeout < 1:
            raise ValueError("download timeout must be positive")
        download_item(args.timeout)
    elif args.command == "verify":
        if not args.download or not args.download.is_dir():
            raise RuntimeError("an actual downloaded Workshop folder is required")
        verify(args.download)
    else:
        inputs = preflight()
        if args.command == "publish":
            publish(inputs)
        else:
            print(json.dumps({"status": "PASS", "version": inputs["version"], "files": len(inputs["content"])}))


if __name__ == "__main__":
    main()
