"""Publish and read back the three frozen Stellaris 4.5.1 maintenance releases.

Only update the existing owned items. Snapshot before promotion, commit and push
the release inputs, then publish/verify one package at a time. Never create items.
"""

from __future__ import annotations

import argparse
import ctypes as C
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import urllib.error

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "synthetic_queen_laoda_replacement/tools"))
from publish_workshop import Steam, SubmitItemUpdateResult
from verify_workshop import additional_preview_urls, public_details

APP_ID = 281990
EVIDENCE = REPO / "docs/evidence/steam-compatibility-releases-2026-09-30"
CONTRACT = REPO / "fixtures/compatibility-4.5.1/mod-contract.json"
RELEASES = {
    "vivhite_infinite_positions": (3797257579, "1.2.1", REPO, "v1.2.1"),
    "gray_wind_beautification": (3800996999, "1.0.2", REPO / "gray_wind_beautification", "gray-wind-v1.0.2"),
    "synthetic_queen_beautification": (3807768508, "0.1.1", REPO / "synthetic_queen_beautification", "synthetic-queen-v0.1.1"),
}
UPSTREAM_IDS = (3710613857, 2976454692)
STABLE_FIELDS = ("publishedfileid", "creator", "consumer_app_id", "creator_app_id", "title",
                 "description", "time_updated", "hcontent_file", "file_size", "visibility", "banned", "preview_url")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def public_notes(item_id: int) -> tuple[int, str]:
    url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=schinese&insideClient=1"
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, html.unescape(response.read().decode("utf-8", "replace"))


def files(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): {"bytes": p.stat().st_size, "sha256": digest(p.read_bytes())}
            for p in sorted(root.rglob("*")) if p.is_file()}


def tree(root: Path) -> str:
    result = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        result.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0" + path.read_bytes())
    return result.hexdigest()


def description_payload(package: str, before: dict) -> bytes:
    """Retain the author's exact remote CRLF prefix and the committed appendix."""
    root = RELEASES[package][2]
    text = (root / "workshop/description.bbcode").read_text(encoding="utf-8")
    if package == "vivhite_infinite_positions":
        original = before["upstreams"]["3710613857"]["description"]
        normalized = original.replace("\r\n", "\n")
        if not text.startswith(normalized):
            raise RuntimeError("Original author's description prefix must remain exact")
        text = original + text[len(normalized):]
    return text.encode("utf-8")


def snapshot(package: str) -> None:
    item_id, version, root, _ = RELEASES[package]
    folder = EVIDENCE / package
    path = folder / "before.json"
    if path.exists():
        raise RuntimeError("Snapshot already exists; do not overwrite the pre-release baseline")
    details = public_details(item_id)
    try:
        _, notes = public_notes(item_id)
        note_status = "public_html_read"
    except urllib.error.HTTPError as error:
        if error.code != 429:
            raise
        notes = ""
        note_status = "http_429; verify published note through Steam client"
    if details.get("result") != 1 or details.get("consumer_app_id") != APP_ID or details.get("visibility") != 0:
        raise RuntimeError("Existing target is not a public Stellaris Workshop item")
    if f"[v{version}]" in notes:
        raise RuntimeError("Formal version is already present in remote Change Notes; do not reuse")
    upstream = {str(i): public_details(i) for i in UPSTREAM_IDS}
    gallery = additional_preview_urls(item_id)
    for preview in gallery:
        preview["sha256"] = digest(fetch(preview["url"]))
    primary = digest(fetch(details["preview_url"]))
    save(path, {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "item_id": item_id,
                "planned_version": version, "details": details, "gallery": gallery,
                "primary_preview_sha256": primary, "upstreams": upstream,
                "accepted_candidate_files": files(REPO / package / "mod"),
                "previous_change_notes_status": note_status,
                "previous_change_notes_sha256": digest(notes.encode("utf-8"))})
    (folder / "before-change-notes.html").write_text(notes, encoding="utf-8", newline="\n")
    print(json.dumps({"snapshot": package, "item_id": item_id, "gallery": len(gallery),
                      "previous_updated": details["time_updated"]}, ensure_ascii=False), flush=True)


def preflight(package: str) -> dict:
    item_id, version, root, tag = RELEASES[package]
    mod = REPO / package / "mod"
    folder = EVIDENCE / package
    before = json.loads((folder / "before.json").read_text(encoding="utf-8"))
    descriptor = (mod / "descriptor.mod").read_text(encoding="utf-8")
    if (root / "VERSION").read_text(encoding="utf-8").strip() != version:
        raise RuntimeError("Formal VERSION mismatch")
    if f'version="{version}"' not in descriptor or 'supported_version="4.5.*"' not in descriptor:
        raise RuntimeError("Descriptor version/compatibility mismatch")
    if "remote_file_id" in descriptor and f'remote_file_id="{item_id}"' not in descriptor:
        raise RuntimeError("Descriptor points to a different Workshop item")
    title = re.search(r'^name="(.*)"', descriptor, re.M).group(1)
    if before["details"]["title"] != title or before["item_id"] != item_id or item_id in UPSTREAM_IDS:
        raise RuntimeError("Target title or item ID mismatch")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        raise RuntimeError("Formal changelog missing")
    description = description_payload(package, before)
    note = (root / f"workshop/change-note-v{version}.txt").read_bytes().strip()
    if len(description) >= 8000 or not note.startswith(f"[v{version}]".encode("ascii")):
        raise RuntimeError("Description limit or Change Note prefix invalid")
    if f"v{version}" not in description.decode("utf-8") or "4.5.*" not in description.decode("utf-8"):
        raise RuntimeError("Formal description version/compatibility missing")
    current_files = files(mod)
    candidate = before["accepted_candidate_files"]
    if set(current_files) != set(candidate) or any(current_files[n] != candidate[n] for n in current_files if n != "descriptor.mod"):
        raise RuntimeError("Accepted non-metadata production content changed")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))["packages"][package]
    if contract["version"] != version or contract["tree_sha256"] != tree(mod):
        raise RuntimeError("Current compatibility contract does not match formal release")
    report = json.loads((folder / "static-acceptance.json").read_text(encoding="utf-8"))
    if report["status"] != "PASS" or report["p_scripts"] != report["p_parsed"]:
        raise RuntimeError("Formal package has not passed open_kaishek")
    scoped = [mod, root / "VERSION", root / "CHANGELOG.md", root / "workshop", CONTRACT,
              Path(__file__), folder / "before.json", folder / "static-acceptance.json"]
    changed = subprocess.check_output(["git", "status", "--porcelain", "--", *[str(p.relative_to(REPO)) for p in scoped]], cwd=REPO)
    if changed.strip():
        raise RuntimeError("Release inputs must be committed before publication")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    upstream_head = subprocess.check_output(["git", "rev-parse", "@{upstream}"], cwd=REPO, text=True).strip()
    if head != upstream_head:
        raise RuntimeError("Release commit must be pushed before publication")
    actual = public_details(item_id)
    if any(actual.get(f) != before["details"].get(f) for f in STABLE_FIELDS):
        raise RuntimeError("Remote item changed since the saved pre-release snapshot")
    return {"package": package, "item_id": item_id, "version": version, "tag": tag, "head": head,
            "content": current_files, "tree_sha256": tree(mod), "description_sha256": digest(description),
            "note_sha256": digest(note), "title": title}


def publish(package: str) -> None:
    inputs = preflight(package)
    item_id, version, root, _ = RELEASES[package]
    path = EVIDENCE / package / "publish-state.json"
    if path.exists():
        raise RuntimeError("Submission state exists; inspect remote before any retry")
    before = json.loads((EVIDENCE / package / "before.json").read_text(encoding="utf-8"))
    steam = Steam()
    state = {"inputs": inputs, "started_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        user_id = steam.fn("SteamAPI_ISteamUser_GetSteamID", [C.c_void_p], C.c_uint64)(steam.user)
        if str(user_id) != str(before["details"]["creator"]):
            raise RuntimeError("Logged-in account does not own the target Workshop item")
        handle = steam.call("StartItemUpdate", APP_ID, item_id)
        if not handle or handle == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("StartItemUpdate failed")
        state["stage"] = "started"
        save(path, state)
        for method, value in (("SetItemDescription", description_payload(package, before)),
                              ("SetItemContent", str((REPO / package / "mod").resolve()).encode("utf-8"))):
            if not steam.call(method, handle, value):
                raise RuntimeError(f"Steamworks {method} failed")
        # Title, visibility, tags, primary and gallery previews remain untouched.
        state["stage"] = "submitting"
        save(path, state)
        note = (root / f"workshop/change-note-v{version}.txt").read_bytes().strip()
        result = steam.wait(steam.call("SubmitItemUpdate", handle, note), SubmitItemUpdateResult, 3404)
        state.update(stage="submitted", submit_result=result.result, submit_item_id=result.item_id,
                     legal_agreement_required=bool(result.legal), completed_at_utc=datetime.now(timezone.utc).isoformat())
        save(path, state)
        if result.result != 1 or result.item_id != item_id or result.legal:
            raise RuntimeError("Steamworks submission did not complete successfully")
        print(json.dumps({"published": package, "version": version, "item_id": item_id, "result": result.result}), flush=True)
    finally:
        steam.close()


def verify(package: str, download: Path, client_notes: Path | None = None) -> None:
    item_id, version, root, _ = RELEASES[package]
    folder = EVIDENCE / package
    before = json.loads((folder / "before.json").read_text(encoding="utf-8"))
    state = json.loads((folder / "publish-state.json").read_text(encoding="utf-8"))
    if state.get("submit_result") != 1 or state.get("submit_item_id") != item_id or state.get("legal_agreement_required"):
        raise RuntimeError("Successful Steamworks receipt missing")
    local = files(REPO / package / "mod")
    remote = files(download.resolve())
    if not local or local != remote or local != state["inputs"]["content"]:
        raise RuntimeError("Downloaded package differs from frozen submitted source")
    details = public_details(item_id)
    description = description_payload(package, before).decode("utf-8")
    expected_bytes = sum(f["bytes"] for f in local.values())
    if (details.get("result") != 1 or details.get("title") != state["inputs"]["title"]
            or details.get("visibility") != 0 or details.get("banned") != 0
            or details.get("description") != description or int(details["file_size"]) != expected_bytes
            or details["time_updated"] <= before["details"]["time_updated"]
            or details["hcontent_file"] == before["details"]["hcontent_file"]
            or details.get("consumer_app_id") != APP_ID or details.get("creator_app_id") != APP_ID):
        raise RuntimeError("Public Workshop metadata/description does not match the release")
    note = (root / f"workshop/change-note-v{version}.txt").read_text(encoding="utf-8").strip()
    if client_notes is None:
        _, notes = public_notes(item_id)
        normalized = re.sub(r"<br\s*/?>", "\n", notes, flags=re.I)
        note_source = "anonymous public HTML"
    else:
        notes = client_notes.read_text(encoding="utf-8")
        normalized = notes.replace("\r\n", "\n")
        note_source = "Steam client public Change Notes page; copied rendered text"
    if re.sub(r"\s+", " ", note) not in re.sub(r"\s+", " ", normalized):
        raise RuntimeError("Complete submitted Change Note is not visible on the public page")
    gallery = additional_preview_urls(item_id)
    for preview in gallery:
        preview["sha256"] = digest(fetch(preview["url"]))
    if gallery != before["gallery"] or digest(fetch(details["preview_url"])) != before["primary_preview_sha256"]:
        raise RuntimeError("Existing preview images changed")
    upstream = {str(i): public_details(i) for i in UPSTREAM_IDS}
    for item in upstream:
        if any(upstream[item].get(f) != before["upstreams"][item].get(f) for f in STABLE_FIELDS):
            raise RuntimeError("Read-only upstream changed")
    save(folder / "workshop-verification.json", {
        "status": "PASS", "verified_at_utc": datetime.now(timezone.utc).isoformat(), "package": package,
        "version": version, "item_id": item_id, "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}",
        "release_head": state["inputs"]["head"], "details": details, "description_exact": True,
        "complete_change_note_public": True, "change_note_readback_source": note_source,
        "change_note_url": f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=schinese&insideClient=1",
        "primary_preview_unchanged": True, "gallery_unchanged": gallery,
        "readonly_upstreams_unchanged": list(upstream), "download_method": "isolated SteamCMD anonymous validate",
        "files": remote, "file_count": len(remote), "total_bytes": expected_bytes,
        "missing_files": [], "extra_files": [], "hash_mismatches": [],
    })
    (folder / ("published-change-notes.txt" if client_notes else "published-change-notes.html")).write_text(notes, encoding="utf-8", newline="\n")
    print(json.dumps({"verified": package, "version": version, "item_id": item_id, "files": len(remote), "bytes": expected_bytes}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", choices=RELEASES)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--snapshot", action="store_true")
    mode.add_argument("--publish", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--download", type=Path)
    parser.add_argument("--client-notes", type=Path, help="Steam client rendered page text when anonymous HTML is rate limited")
    args = parser.parse_args()
    if args.snapshot:
        snapshot(args.package)
    elif args.publish:
        publish(args.package)
    elif args.verify:
        if args.download is None:
            parser.error("--verify requires --download")
        verify(args.package, args.download, args.client_notes)
    else:
        print(json.dumps(preflight(args.package), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
