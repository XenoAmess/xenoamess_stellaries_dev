"""Publish and independently read back the owned Shishan release; no item creation."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
MOD = ROOT / "mod"
WORKSHOP = ROOT / "workshop"
APP_ID = 281990
ITEM_ID = 3810136486
UPSTREAM_ID = 3710613857
EXE_SHA = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"


def version() -> str:
    value = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise RuntimeError("Only a stable SemVer may be published")
    return value


def folder() -> Path:
    return ROOT / "evidence" / f"v{version()}"


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    temp.replace(path)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def files(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
            for p in sorted(root.rglob("*")) if p.is_file()}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def details(item_id: int) -> dict:
    data = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    request = urllib.request.Request("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=data)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["response"]["publishedfiledetails"][0]


def public_notes() -> str:
    raw = fetch(f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{ITEM_ID}?l=schinese&insideClient=1")
    return html.unescape(re.sub(r"<br\s*/?>", "\n", raw.decode("utf-8", "replace"), flags=re.I))


def snapshot() -> None:
    path = folder() / "before.json"
    if path.exists():
        raise RuntimeError("Before snapshot already exists; preserve original remote evidence")
    item = details(ITEM_ID)
    upstream = details(UPSTREAM_ID)
    if item.get("result") != 1 or item.get("consumer_app_id") != APP_ID or item.get("visibility") != 0:
        raise RuntimeError("Target is not the existing public Stellaris item")
    if f"Mod v{version()}" in item.get("description", ""):
        raise RuntimeError("Release version is already remote")
    try:
        notes = public_notes()
        if f"[v{version()}]" in notes:
            raise RuntimeError("Version already has a published Change Note")
        note_status = "public HTML read"
    except urllib.error.HTTPError as error:
        if error.code != 429:
            raise
        notes = ""
        note_status = "HTTP429; previous local receipt and current public version retained; readback required"
    save(path, {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "planned_version": version(),
                "item_id": ITEM_ID, "details": item, "upstream": upstream,
                "primary_preview_sha256": digest(fetch(item["preview_url"])),
                "previous_change_notes_status": note_status, "previous_change_notes_sha256": digest(notes.encode())})
    print(json.dumps({"snapshot": str(path.relative_to(REPO)), "item_id": ITEM_ID,
                      "time_updated": item["time_updated"], "notes_status": note_status}))


def preflight(require_committed: bool = True) -> dict:
    v = version()
    if int((WORKSHOP / "item-id.txt").read_text().strip()) != ITEM_ID or ITEM_ID == UPSTREAM_ID:
        raise RuntimeError("Owned item identity mismatch")
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8-sig")
    if f'version="{v}"' not in descriptor or 'supported_version="4.5.*"' not in descriptor or "remote_file_id" in descriptor:
        raise RuntimeError("Descriptor version, compatibility or identity mismatch")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8-sig")
    if f"## [{v}] - " not in changelog:
        raise RuntimeError("Formal changelog missing")
    section = changelog.split(f"## [{v}] - ", 1)[1].split("\n## [", 1)[0]
    if any(f"### {name}" not in section for name in ["Added", "Changed", "Fixed", "Compatibility", "Validation", "Known limitations"]):
        raise RuntimeError("Formal changelog is incomplete")
    note = (WORKSHOP / f"change-note-v{v}.txt").read_text(encoding="utf-8").strip()
    description = (WORKSHOP / "description.bbcode").read_bytes()
    if not note.startswith(f"[v{v}]") or f"Mod v{v}".encode() not in description or len(description) >= 8000:
        raise RuntimeError("Change Note or public description is invalid")
    before = json.loads((folder() / "before.json").read_text(encoding="utf-8"))
    if before["planned_version"] != v or before["item_id"] != ITEM_ID:
        raise RuntimeError("Remote snapshot identity mismatch")
    image_urls = lambda s: re.findall(r"\[img\](.*?)\[/img\]", s)
    if image_urls(description.decode()) != image_urls(before["details"]["description"]):
        raise RuntimeError("Existing inline image URLs/order changed")
    content = files(MOD)
    if len(content) != 90 or any(re.search(r"(^|/)(testing|tests|fixture|evidence|_runtime)(/|$)|\.(sav|log|py)$", p) for p in content):
        raise RuntimeError("Production package count or test contamination mismatch")
    acceptance = json.loads((folder() / "acceptance/package-open-kaishek.json").read_text(encoding="utf-8-sig"))
    if acceptance.get("status") != "PASS" or acceptance.get("game_exe_sha256") != EXE_SHA or acceptance.get("errors"):
        raise RuntimeError("Formal package acceptance is not PASS for this game")
    identity = json.loads((folder() / "acceptance/release-identity.json").read_text(encoding="utf-8-sig"))
    if identity.get("status") != "PASS" or identity.get("version") != v or identity.get("content") != content:
        raise RuntimeError("Current package differs from the accepted release identity")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    if require_committed:
        paths = [str(ROOT.relative_to(REPO) / p) for p in ["mod", "VERSION", "CHANGELOG.md", "workshop", "tools/update_workshop_current.py", f"evidence/v{v}"]]
        if subprocess.check_output(["git", "status", "--porcelain", "--", *paths], cwd=REPO).strip():
            raise RuntimeError("Release inputs and acceptance must be committed before publication")
        upstream = subprocess.check_output(["git", "rev-parse", "@{upstream}"], cwd=REPO, text=True).strip()
        if head != upstream:
            raise RuntimeError("Release input commit must be pushed before publication")
    return {"version": v, "item_id": ITEM_ID, "head": head, "content": content,
            "description_sha256": digest(description), "note_sha256": digest(note.encode()),
            "note": note, "inline_image_count": len(image_urls(description.decode()))}


def publish() -> None:
    state_path = folder() / "publish-state.json"
    if state_path.exists():
        raise RuntimeError("Submission receipt already exists; inspect before any retry")
    inputs = preflight()
    before = json.loads((folder() / "before.json").read_text())
    current = details(ITEM_ID)
    if any(current.get(k) != before["details"].get(k) for k in ["time_updated", "hcontent_file", "description", "creator"]):
        raise RuntimeError("Remote item changed after snapshot; do not overwrite")
    sys.path.insert(0, str(REPO))
    from synthetic_queen_laoda_replacement.tools.publish_workshop import Steam, SubmitItemUpdateResult
    steam = Steam()
    state = {"schema": "shishan-owned-stable-update-v1", "created_at_utc": datetime.now(timezone.utc).isoformat(), "inputs": inputs}
    try:
        handle = steam.call("StartItemUpdate", APP_ID, ITEM_ID)
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")
        if not steam.call("SetItemDescription", handle, (WORKSHOP / "description.bbcode").read_bytes()):
            raise RuntimeError("SetItemDescription failed")
        if not steam.call("SetItemContent", handle, os.fsencode(str(MOD.resolve()))):
            raise RuntimeError("SetItemContent failed")
        # Existing visibility, title, tags, primary preview and gallery are preserved.
        save(state_path, state)
        result = steam.wait(steam.call("SubmitItemUpdate", handle, inputs["note"].encode()), SubmitItemUpdateResult, 3404)
        state.update(submit_result=result.result, submit_item_id=result.item_id,
                     legal_agreement_required=bool(result.legal), completed_at_utc=datetime.now(timezone.utc).isoformat())
        save(state_path, state)
        if result.result != 1 or result.item_id != ITEM_ID or result.legal:
            raise RuntimeError("Steamworks update did not succeed safely")
        print(json.dumps({"submitted": True, "version": inputs["version"], "item_id": ITEM_ID, "result": result.result}), flush=True)
    finally:
        steam.close()


def verify(download: Path, client_notes: Path | None) -> None:
    state = json.loads((folder() / "publish-state.json").read_text(encoding="utf-8"))
    if state.get("submit_result") != 1 or state.get("submit_item_id") != ITEM_ID or state.get("legal_agreement_required"):
        raise RuntimeError("Successful submission receipt required")
    before = json.loads((folder() / "before.json").read_text(encoding="utf-8"))
    content = files(MOD)
    if content != state["inputs"]["content"] or files(download.resolve()) != content:
        raise RuntimeError("Fresh downloaded content differs from submitted source")
    item = details(ITEM_ID)
    description = (WORKSHOP / "description.bbcode").read_text(encoding="utf-8")
    total = sum(f["bytes"] for f in content.values())
    if (item.get("result") != 1 or item.get("consumer_app_id") != APP_ID or item.get("creator_app_id") != APP_ID
            or item.get("visibility") != 0 or item.get("banned") != 0 or item["description"] != description
            or item["time_updated"] <= before["details"]["time_updated"]
            or item["hcontent_file"] == before["details"]["hcontent_file"] or int(item["file_size"]) != total):
        raise RuntimeError("Public remote metadata does not match release")
    if digest(fetch(item["preview_url"])) != before["primary_preview_sha256"]:
        raise RuntimeError("Primary preview changed")
    if client_notes is None:
        notes = public_notes()
        source = "anonymous public HTML"
    else:
        notes = client_notes.read_text(encoding="utf-8")
        source = "Steam client rendered public Change Notes page; copied text"
    if re.sub(r"\s+", " ", state["inputs"]["note"]) not in re.sub(r"\s+", " ", notes):
        raise RuntimeError("Complete submitted Change Note has not been read back")
    upstream = details(UPSTREAM_ID)
    if any(upstream.get(k) != before["upstream"].get(k) for k in ["time_updated", "hcontent_file", "description", "title"]):
        raise RuntimeError("Read-only upstream changed")
    save(folder() / "published-change-notes.json", {"source": source, "text": notes, "sha256": digest(notes.encode())})
    save(folder() / "workshop-verification.json", {"status": "PASS", "version": version(), "item_id": ITEM_ID,
         "verified_at_utc": datetime.now(timezone.utc).isoformat(), "release_head": state["inputs"]["head"],
         "description_exact": True, "complete_change_note_read_back": True, "change_note_source": source,
         "primary_preview_unchanged": True, "gallery_update_interfaces_called": False,
         "readonly_upstream_unchanged": True, "download_method": "isolated SteamCMD anonymous validate",
         "file_count": len(content), "total_bytes": total, "files": content,
         "missing_files": [], "extra_files": [], "hash_mismatches": [],
         "time_updated": item["time_updated"], "content_file_id": item["hcontent_file"]})
    print(json.dumps({"verified": True, "version": version(), "item_id": ITEM_ID, "files": len(content), "bytes": total}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--snapshot", action="store_true")
    mode.add_argument("--publish", action="store_true")
    mode.add_argument("--verify", type=Path, metavar="DOWNLOADED_MOD")
    parser.add_argument("--client-notes", type=Path)
    args = parser.parse_args()
    if args.snapshot:
        snapshot()
    elif args.publish:
        publish()
    elif args.verify:
        verify(args.verify, args.client_notes)
    else:
        data = preflight()
        print(json.dumps({"preflight": "PASS", "version": data["version"], "item_id": ITEM_ID, "files": len(data["content"])}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"update_workshop_current: {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
