"""Read back the published item and compare both Steam image assets byte-for-byte."""

from __future__ import annotations

import argparse
import ctypes as C
import hashlib
import html
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from publish_workshop import APP_ID, MEDIA, ROOT, STATE, TITLE, Steam


DETAILS_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
EVIDENCE = ROOT / "evidence/v0.1.1/workshop-publication.json"


class QueryComplete(C.Structure):
    _fields_ = [
        ("handle", C.c_uint64),
        ("result", C.c_int32),
        ("returned", C.c_uint32),
        ("total", C.c_uint32),
        ("cached", C.c_bool),
    ]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get(url: str) -> tuple[int, str, bytes]:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.status, response.headers.get("Content-Type", ""), response.read()


def public_details(item_id: int) -> dict:
    body = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": item_id}).encode()
    request = urllib.request.Request(DETAILS_URL, data=body)
    with urllib.request.urlopen(request, timeout=30) as response:
        details = json.load(response)["response"]["publishedfiledetails"][0]
    return details


def community_page(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, html.unescape(response.read().decode("utf-8", "replace"))


def additional_preview_urls(item_id: int) -> list[dict]:
    steam = Steam()
    query = None
    try:
        steam.fn("SteamAPI_ISteamUGC_CreateQueryUGCDetailsRequest", [C.c_void_p, C.POINTER(C.c_uint64), C.c_uint32], C.c_uint64)
        steam.fn("SteamAPI_ISteamUGC_SetReturnAdditionalPreviews", [C.c_void_p, C.c_uint64, C.c_bool], C.c_bool)
        steam.fn("SteamAPI_ISteamUGC_SendQueryUGCRequest", [C.c_void_p, C.c_uint64], C.c_uint64)
        steam.fn("SteamAPI_ISteamUGC_GetQueryUGCNumAdditionalPreviews", [C.c_void_p, C.c_uint64, C.c_uint32], C.c_uint32)
        steam.fn(
            "SteamAPI_ISteamUGC_GetQueryUGCAdditionalPreview",
            [C.c_void_p, C.c_uint64, C.c_uint32, C.c_uint32, C.c_void_p, C.c_uint32, C.c_void_p, C.c_uint32, C.POINTER(C.c_int32)],
            C.c_bool,
        )
        steam.fn("SteamAPI_ISteamUGC_ReleaseQueryUGCRequest", [C.c_void_p, C.c_uint64], C.c_bool)
        ids = (C.c_uint64 * 1)(item_id)
        query = steam.call("CreateQueryUGCDetailsRequest", ids, 1)
        if not query or query == 0xFFFFFFFFFFFFFFFF:
            raise RuntimeError("Steam UGC details query was not created")
        if not steam.call("SetReturnAdditionalPreviews", query, True):
            raise RuntimeError("Steam UGC refused additional preview query")
        completed = steam.wait(steam.call("SendQueryUGCRequest", query), QueryComplete, 3401)
        if completed.handle != query or completed.result != 1 or completed.returned != 1:
            raise RuntimeError(f"Steam UGC details query failed: result={completed.result}, returned={completed.returned}")
        count = steam.call("GetQueryUGCNumAdditionalPreviews", query, 0)
        previews = []
        for index in range(count):
            url = C.create_string_buffer(2048)
            filename = C.create_string_buffer(512)
            kind = C.c_int32()
            ok = steam.call("GetQueryUGCAdditionalPreview", query, 0, index, url, len(url), filename, len(filename), C.byref(kind))
            if not ok or kind.value != 0:
                raise RuntimeError(f"Steam additional preview {index} was not a readable image")
            previews.append({"index": index, "url": url.value.decode("utf-8"), "original_name": filename.value.decode("utf-8"), "type": kind.value})
        return previews
    finally:
        if query is not None and query not in (0, 0xFFFFFFFFFFFFFFFF):
            steam.call("ReleaseQueryUGCRequest", query)
        steam.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-community", action="store_true", help="also check public item and Change Note HTML")
    args = parser.parse_args()
    state = json.loads(STATE.read_text(encoding="utf-8"))
    item_id = int(state["item_id"])
    if state.get("submit_result") != 1 or state.get("submit_item_id") != item_id:
        raise RuntimeError("Workshop submission receipt is incomplete")
    details = public_details(item_id)
    description = (ROOT / "workshop/description.bbcode").read_text(encoding="utf-8")
    if (
        details.get("result") != 1
        or details.get("creator_app_id") != APP_ID
        or details.get("consumer_app_id") != APP_ID
        or details.get("title") != TITLE
        or details.get("description") != description
        or details.get("visibility") != 0
        or details.get("banned") != 0
    ):
        raise RuntimeError("Public Workshop metadata differs from the reviewed release")

    primary_status, primary_type, primary_data = get(details["preview_url"])
    if primary_status != 200 or "image/jpeg" not in primary_type or primary_data != MEDIA[0].read_bytes():
        raise RuntimeError("The primary screenshot is not the requested in-game image")
    additional = additional_preview_urls(item_id)
    if len(additional) != 1:
        raise RuntimeError(f"Expected exactly one additional screenshot, found {len(additional)}")
    secondary_status, secondary_type, secondary_data = get(additional[0]["url"])
    if secondary_status != 200 or "image/jpeg" not in secondary_type or secondary_data != MEDIA[1].read_bytes():
        raise RuntimeError("Additional in-game screenshot differs from accepted evidence")
    community = None
    if args.check_community:
        page_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}&l=english"
        changelog_url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{item_id}?l=english"
        page_status, page_html = community_page(page_url)
        changelog_status, changelog_html = community_page(changelog_url)
        note = (ROOT / "workshop/change-note-v0.1.1.txt").read_text(encoding="utf-8").strip()
        if page_status != 200 or "孩子们，我终于回到了你们的身边" not in page_html:
            raise RuntimeError("Public Workshop page does not show the requested screenshot caption")
        if changelog_status != 200 or note not in changelog_html:
            raise RuntimeError("The versioned Steam Change Note is not visible on the public page")
        community = {"page_http_status": page_status, "change_note_http_status": changelog_status, "change_note_exact_visible": True}

    result = {
        "schema": "laoda-workshop-publication-v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "workshop_url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}",
        "item_id": item_id,
        "public_details": {
            "result": details["result"],
            "creator_app_id": details["creator_app_id"],
            "consumer_app_id": details["consumer_app_id"],
            "title": details["title"],
            "visibility": details["visibility"],
            "banned": details["banned"],
            "file_size": int(details["file_size"]),
            "hcontent_file": str(details["hcontent_file"]),
            "time_created": details["time_created"],
            "time_updated": details["time_updated"],
            "tags": [item["tag"] for item in details.get("tags", [])],
            "description_sha256": sha256(description.encode("utf-8")),
            "description_exact_match": True,
        },
        "primary_preview": {"local_file": MEDIA[0].name, "url": details["preview_url"], "bytes": len(primary_data), "sha256": sha256(primary_data), "exact_bytes_match": True},
        "additional_previews": [
            {**additional[0], "local_file": MEDIA[1].name, "bytes": len(secondary_data), "sha256": sha256(secondary_data), "exact_bytes_match": True}
        ],
    }
    if community is not None:
        result["community_page"] = community
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"item_id": item_id, "public": True, "description_exact": True, "main_screenshot_exact": True, "additional_screenshot_exact": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
