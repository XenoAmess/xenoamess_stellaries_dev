"""Publish only an accepted formal release to its own new Workshop item."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ctypes as C
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
STATE = ROOT / "docs/evidence/publish-state.json"
APP_ID = 281990
TITLE = "吞噬之心"
FORBIDDEN_ID = 3710613857
sys.path.insert(0, str(REPO / "synthetic_queen_laoda_replacement/tools"))
import publish_workshop as native
native.DLL = Path(r"C:\SteamLibrary\steamapps\common\Stellaris\steam_api64.dll")


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
    if not re.search(rf"^## {re.escape(version)}\s", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M):
        raise RuntimeError("formal changelog entry missing")
    package = json.loads((ROOT / "docs/evidence/package-release.json").read_text(encoding="utf-8"))
    runtime = json.loads((ROOT / "docs/evidence/runtime-acceptance.json").read_text(encoding="utf-8"))
    files = manifest(MOD)
    if package["status"] != "PASS" or runtime["status"] != "PASS" or runtime["production_files"] != files:
        raise RuntimeError("acceptance is incomplete or production files drifted")
    if runtime.get("language") != "l_simp_chinese":
        raise RuntimeError("runtime must be Simplified Chinese")
    if any(runtime["cases"].get(f"EAT-{number:02}", {}).get("status") != "PASS" for number in range(1, 34)):
        raise RuntimeError("required runtime cases are incomplete")
    if any("eep_probe" in p or p.startswith("testing/") for p in files):
        raise RuntimeError("test fixtures leaked into production")
    note = (WORKSHOP / f"change-note-v{version}.txt").read_text(encoding="utf-8").strip()
    if not note.startswith(f"[v{version}]"):
        raise RuntimeError("Change Note version prefix mismatch")
    description = (WORKSHOP / "description.bbcode").read_text(encoding="utf-8")
    if len(description.encode("utf-8")) >= 8000:
        raise RuntimeError("Workshop description exceeds the accepted API limit")
    thumbnail = MOD / "thumbnail.png"
    if thumbnail.stat().st_size >= 1_000_000:
        raise RuntimeError("Workshop thumbnail too large")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO):
        raise RuntimeError("commit task changes before publication")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    return {"version": version, "head": head, "content": files, "description": description, "note": note}


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
    body = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    req = urllib.request.Request("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=body)
    with urllib.request.urlopen(req, timeout=30) as response:
        details = json.load(response)["response"]["publishedfiledetails"][0]
    expected = state["inputs"]
    if any([details.get("result") != 1, details.get("consumer_app_id") != APP_ID, details.get("creator_app_id") != APP_ID, details.get("title") != TITLE, details.get("description") != expected["description"], details.get("visibility") != 0, details.get("banned") != 0]):
        raise RuntimeError("public Workshop metadata differs")
    with urllib.request.urlopen(details["preview_url"], timeout=30) as response:
        if response.read() != (MOD / "thumbnail.png").read_bytes():
            raise RuntimeError("remote preview differs")
    url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=english"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        page = html.unescape(response.read().decode("utf-8", "replace"))
    if expected["note"] not in page:
        raise RuntimeError("versioned Change Note not visible")
    if manifest(download) != expected["content"] or manifest(MOD) != expected["content"]:
        raise RuntimeError("download content differs from frozen production")
    report = {"status": "PASS", "version": expected["version"], "item_id": item_id, "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}", "public_metadata_exact": True, "change_note_exact": True, "download_files": len(expected["content"]), "production_files": expected["content"], "verified_at_utc": datetime.now(timezone.utc).isoformat()}
    write_json(ROOT / "docs/evidence/workshop-verification.json", report)
    print(json.dumps({k: report[k] for k in ["status", "version", "item_id", "url", "download_files"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["preflight", "publish", "verify"])
    parser.add_argument("--download", type=Path)
    args = parser.parse_args()
    if args.command == "verify":
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
