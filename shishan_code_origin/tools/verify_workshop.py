"""Read back the public item and compare the anonymous SteamCMD download."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import urllib.parse
import urllib.request

from publish_workshop import APP_ID, MOD, ROOT, STATE, TITLE, VERSION, WORKSHOP


DETAILS_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
DOWNLOAD_ROOT = Path(r"C:\Users\Administrator\AppData\Local\Temp\synthetic-queen-steamcmd-20260925\steamapps\workshop\content\281990")
EVIDENCE = ROOT / "evidence/v0.1.0/workshop-verification.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def details(item_id: int) -> dict:
    data = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    request = urllib.request.Request(DETAILS_URL, data=data)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["response"]["publishedfiledetails"][0]


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    item_id = int(state["item_id"])
    if state.get("submit_result") != 1 or state.get("submit_item_id") != item_id:
        raise RuntimeError("upload receipt is incomplete")
    item = details(item_id)
    description = (WORKSHOP / "description.bbcode").read_text(encoding="utf-8")
    if any((
        item.get("result") != 1,
        item.get("creator_app_id") != APP_ID,
        item.get("consumer_app_id") != APP_ID,
        item.get("title") != TITLE,
        item.get("description") != description,
        item.get("visibility") != 0,
        item.get("banned") != 0,
    )):
        raise RuntimeError("public item metadata differs from the frozen release")
    with urllib.request.urlopen(item["preview_url"], timeout=30) as response:
        preview = response.read()
    if preview != (MOD / "thumbnail.png").read_bytes():
        raise RuntimeError("Workshop preview differs from release thumbnail")
    note = (WORKSHOP / f"change-note-v{VERSION}.txt").read_text(encoding="utf-8").strip()
    page = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=english"
    request = urllib.request.Request(page, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        changelog_html = html.unescape(response.read().decode("utf-8", "replace"))
    if note not in changelog_html:
        raise RuntimeError("versioned Change Note is not visible on the public page")

    remote_root = DOWNLOAD_ROOT / str(item_id)
    local = {p.relative_to(MOD).as_posix(): p for p in MOD.rglob("*") if p.is_file()}
    remote = {p.relative_to(remote_root).as_posix(): p for p in remote_root.rglob("*") if p.is_file()}
    mismatches = sorted(name for name in local.keys() & remote.keys() if local[name].read_bytes() != remote[name].read_bytes())
    if local.keys() != remote.keys() or mismatches or len(local) != 64:
        raise RuntimeError(f"download differs: missing={sorted(local.keys()-remote.keys())}, extra={sorted(remote.keys()-local.keys())}, mismatches={mismatches}")
    total = sum(p.stat().st_size for p in local.values())
    if int(item.get("file_size", -1)) != total:
        raise RuntimeError("published file size differs from downloaded package")

    upstream = details(3710613857)
    upstream_sha = digest(upstream["description"].encode("utf-8"))
    if upstream.get("time_updated") != 1783740925 or upstream_sha != "ba71a4e28e48ff6b466c0615cd271e3f7c9b9e868373b04b08ecfe29dde2ac76":
        raise RuntimeError("read-only upstream changed relative to recorded baseline")

    result = {
        "schema": "shishan-workshop-verification-v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "item_id": item_id,
        "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}",
        "public": True,
        "title_exact": True,
        "description_sha256": digest(description.encode("utf-8")),
        "description_exact": True,
        "change_note_exact_visible": True,
        "primary_preview_sha256": digest(preview),
        "primary_preview_exact": True,
        "content_file_id": str(item["hcontent_file"]),
        "time_updated": item["time_updated"],
        "download": {"method": "SteamCMD anonymous", "file_count": len(remote), "total_bytes": total, "missing": [], "extra": [], "hash_mismatches": []},
        "upstream": {"item_id": 3710613857, "time_updated": upstream["time_updated"], "description_sha256": upstream_sha, "unchanged_from_baseline": True},
        "release_head": state["inputs"]["head"],
        "files": state["inputs"]["content"],
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (WORKSHOP / "item-id.txt").write_text(f"{item_id}\n", encoding="ascii")
    print(json.dumps({"status": "PASS", "item_id": item_id, "files": len(remote), "bytes": total, "upstream_unchanged": True}))


if __name__ == "__main__":
    main()
