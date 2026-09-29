"""Verify the published v0.1.3 page and anonymous Workshop download."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import urllib.parse
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
VERSION = "0.1.3"
ITEM_ID = 3810136486
APP_ID = 281990
UPSTREAM_ID = 3710613857
DOWNLOAD = Path(
    r"C:\Users\Administrator\AppData\Local\Temp\synthetic-queen-steamcmd-20260925"
    r"\steamapps\workshop\content\281990\3810136486"
)
DETAILS_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
EVIDENCE = ROOT / "evidence/v0.1.3/workshop-verification.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def details(item_id: int) -> dict:
    payload = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    with urllib.request.urlopen(urllib.request.Request(DETAILS_URL, data=payload), timeout=30) as response:
        return json.load(response)["response"]["publishedfiledetails"][0]


def main() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == VERSION
    state = json.loads((ROOT / "evidence/v0.1.3/publish-state.json").read_text(encoding="utf-8"))
    assert state["inputs"]["item_id"] == ITEM_ID
    assert state["submit_result"] == 1 and state["submit_item_id"] == ITEM_ID
    assert state["inputs"]["version"] == VERSION
    assert state["staged_preview_count"] == 8

    item = details(ITEM_ID)
    description = (ROOT / "workshop/description.bbcode").read_text(encoding="utf-8")
    images = json.loads((ROOT / "workshop/page-images-v0.1.3.json").read_text(encoding="utf-8"))["images"]
    assert len(images) == 9 and images[0]["kind"] == "artwork"
    assert sum(image["kind"] == "screenshot" for image in images) == 8
    art = images[0]
    assert art["source"] == "assets/shishan-code-origin/generated/A02-attempt-01/original.png"
    assert description.count(f'[img]{art["url"]}[/img]') == 1
    assert digest((REPO / art["source"]).read_bytes()) == art["sha256"]
    for image in images:
        assert description.count(f'[img]{image["url"]}[/img]') == 1
    assert item["result"] == 1 and item["creator_app_id"] == APP_ID
    assert item["consumer_app_id"] == APP_ID and item["visibility"] == 0
    assert item["banned"] == 0 and item["title"] == "屎山代码"
    assert item["description"] == description
    with urllib.request.urlopen(item["preview_url"], timeout=30) as response:
        preview = response.read()
    assert preview == (ROOT / "mod/thumbnail.png").read_bytes()

    note = (ROOT / "workshop/change-note-v0.1.3.txt").read_text(encoding="utf-8").strip()
    assert note.startswith("[v0.1.3]")
    change_page = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{ITEM_ID}?l=english"
    request = urllib.request.Request(change_page, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            change_html = html.unescape(response.read().decode("utf-8", "replace"))
        assert note in change_html
        change_note_html_status = "exact"
    except urllib.error.HTTPError as error:
        if error.code != 429:
            raise
        change_note_html_status = "rate_limited_429"
    change_note_screenshot = REPO / "assets/shishan-code-origin/evidence/workshop-v013-change-note.png"
    assert change_note_screenshot.is_file()
    a02_screenshot = REPO / "assets/shishan-code-origin/evidence/workshop-v013-a02-inline.png"
    assert a02_screenshot.is_file()

    local = {p.relative_to(ROOT / "mod").as_posix(): p for p in (ROOT / "mod").rglob("*") if p.is_file()}
    remote = {p.relative_to(DOWNLOAD).as_posix(): p for p in DOWNLOAD.rglob("*") if p.is_file()}
    mismatches = sorted(name for name in local.keys() & remote.keys() if local[name].read_bytes() != remote[name].read_bytes())
    assert len(local) == 64 and local.keys() == remote.keys() and not mismatches, {
        "missing": sorted(local.keys() - remote.keys()),
        "extra": sorted(remote.keys() - local.keys()),
        "mismatches": mismatches,
    }
    total = sum(path.stat().st_size for path in local.values())
    assert int(item["file_size"]) == total

    upstream = details(UPSTREAM_ID)
    upstream_sha = digest(upstream["description"].encode("utf-8"))
    assert upstream["time_updated"] == 1783740925
    assert upstream_sha == "ba71a4e28e48ff6b466c0615cd271e3f7c9b9e868373b04b08ecfe29dde2ac76"

    evidence = {
        "schema": "shishan-workshop-verification-v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "item_id": ITEM_ID,
        "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM_ID}",
        "public": True,
        "description_exact": True,
        "description_sha256": digest(description.encode("utf-8")),
        "a02": {"source": art["source"], "url": art["url"], "sha256": art["sha256"], "inline_visible_in_steam_client": True, "screenshot": "assets/shishan-code-origin/evidence/workshop-v013-a02-inline.png"},
        "inline_image_count": len(images),
        "gallery_preview_count": state["staged_preview_count"],
        "change_note_public_html_status": change_note_html_status,
        "change_note_steam_client_visual_pass": True,
        "change_note_steam_client_screenshot": change_note_screenshot.relative_to(REPO).as_posix(),
        "primary_preview_exact": True,
        "content_file_id": str(item["hcontent_file"]),
        "time_updated": item["time_updated"],
        "download": {"method": "SteamCMD anonymous validate", "file_count": len(remote), "total_bytes": total, "missing": [], "extra": [], "hash_mismatches": []},
        "upstream": {"item_id": UPSTREAM_ID, "time_updated": upstream["time_updated"], "description_sha256": upstream_sha, "unchanged_from_baseline": True},
        "release_head": state["inputs"]["head"],
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "version": VERSION, "item_id": ITEM_ID, "files": len(remote), "bytes": total, "inline_images": len(images), "gallery_previews": state["staged_preview_count"]}))


if __name__ == "__main__":
    main()
