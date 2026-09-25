"""Verify the published v0.1.2 thumbnail and preserved gameplay screenshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone

from publish_workshop import APP_ID, MEDIA, MOD, ROOT, TITLE
from update_workshop import ITEM_ID, PREVIOUS_CONTENT, PREVIOUS_UPDATED, STATE, THUMBNAIL_SHA256, VERSION
from verify_workshop import additional_preview_urls, community_page, public_details


EVIDENCE = ROOT / "evidence/v0.1.2/workshop-update-verification.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"Image HTTP status was {response.status}")
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-community", action="store_true", help="also verify the public page and complete Change Note")
    args = parser.parse_args()
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("submit_result") != 1 or state.get("submit_item_id") != ITEM_ID:
        raise RuntimeError("v0.1.2 Steamworks update receipt is incomplete")
    details = public_details(ITEM_ID)
    description = (ROOT / "workshop/description.bbcode").read_text(encoding="utf-8")
    files = {path.relative_to(MOD).as_posix(): path for path in MOD.rglob("*") if path.is_file()}
    local_bytes = sum(path.stat().st_size for path in files.values())
    if (
        details.get("result") != 1
        or details.get("creator_app_id") != APP_ID
        or details.get("consumer_app_id") != APP_ID
        or details.get("title") != TITLE
        or details.get("visibility") != 0
        or details.get("banned") != 0
        or details.get("description") != description
        or details.get("time_updated", 0) <= PREVIOUS_UPDATED
        or str(details.get("hcontent_file")) == PREVIOUS_CONTENT
        or int(details.get("file_size", -1)) != local_bytes
    ):
        raise RuntimeError("Remote item metadata or package size differs from the v0.1.2 release")

    thumbnail = (MOD / "thumbnail.png").read_bytes()
    primary = download(details["preview_url"])
    if sha256(thumbnail) != THUMBNAIL_SHA256 or primary != thumbnail:
        raise RuntimeError("Steam primary preview is not the user's original PNG")
    additional = additional_preview_urls(ITEM_ID)
    if len(additional) != 2:
        raise RuntimeError(f"Expected two full gameplay screenshots, found {len(additional)}")
    previews = []
    for preview in additional:
        data = download(preview["url"])
        previews.append({**preview, "bytes": len(data), "sha256": sha256(data)})
    expected = {sha256(path.read_bytes()): path.name for path in MEDIA}
    if {item["sha256"] for item in previews} != set(expected):
        raise RuntimeError("Steam additional previews do not match both original Steam F12 screenshots")
    for item in previews:
        item["local_file"] = expected[item["sha256"]]
        item["exact_bytes_match"] = True

    community = None
    if args.check_community:
        page_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM_ID}&l=english"
        note_url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{ITEM_ID}?l=english"
        page_status, page_html = community_page(page_url)
        note_status, note_html = community_page(note_url)
        note = (ROOT / "workshop/change-note-v0.1.2.txt").read_text(encoding="utf-8").strip()
        if page_status != 200 or note_status != 200 or note not in note_html or "孩子们，我终于回到了你们的身边" not in page_html:
            raise RuntimeError("Public page or exact v0.1.2 Change Note could not be verified")
        community = {"page_http_status": page_status, "change_note_http_status": note_status, "change_note_exact_visible": True}

    result = {
        "schema": "laoda-workshop-thumbnail-update-verification-v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "item_id": ITEM_ID,
        "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM_ID}",
        "public_details": {
            "result": details["result"],
            "creator_app_id": details["creator_app_id"],
            "consumer_app_id": details["consumer_app_id"],
            "title": details["title"],
            "visibility": details["visibility"],
            "banned": details["banned"],
            "file_size": int(details["file_size"]),
            "hcontent_file": str(details["hcontent_file"]),
            "time_updated": details["time_updated"],
            "description_sha256": sha256(description.encode("utf-8")),
            "description_exact_match": True,
        },
        "primary_preview": {"source": "mod/thumbnail.png", "url": details["preview_url"], "bytes": len(primary), "sha256": sha256(primary), "exact_bytes_match": True},
        "additional_previews": previews,
    }
    if community is not None:
        result["community_page"] = community
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"item_id": ITEM_ID, "version": VERSION, "main_thumbnail_exact": True, "gameplay_screenshots_exact": 2}, ensure_ascii=False))


if __name__ == "__main__":
    main()
