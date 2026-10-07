"""Freeze local Workshop images and verify their actual remote previews."""
import ctypes as C
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from PIL import Image

FORBIDDEN_ID = 3710613857
INVALID_HANDLE = 0xFFFFFFFFFFFFFFFF


class QueryCompleted(C.Structure):
    _pack_ = 8
    _fields_ = [("handle", C.c_uint64), ("result", C.c_int32),
                ("returned", C.c_uint32), ("total", C.c_uint32),
                ("cached", C.c_bool)]


API = {
    "CreateQueryUGCDetailsRequest": ([C.c_void_p, C.POINTER(C.c_uint64), C.c_uint32], C.c_uint64),
    "SetReturnAdditionalPreviews": ([C.c_void_p, C.c_uint64, C.c_bool], C.c_bool),
    "SetAllowCachedResponse": ([C.c_void_p, C.c_uint64, C.c_uint32], C.c_bool),
    "SendQueryUGCRequest": ([C.c_void_p, C.c_uint64], C.c_uint64),
    "GetQueryUGCNumAdditionalPreviews": ([C.c_void_p, C.c_uint64, C.c_uint32], C.c_uint32),
    "GetQueryUGCAdditionalPreview": ([C.c_void_p, C.c_uint64, C.c_uint32, C.c_uint32,
                                    C.c_char_p, C.c_uint32, C.c_char_p, C.c_uint32,
                                    C.POINTER(C.c_int32)], C.c_bool),
    "ReleaseQueryUGCRequest": ([C.c_void_p, C.c_uint64], C.c_bool),
    "RemoveItemPreview": ([C.c_void_p, C.c_uint64, C.c_uint32], C.c_bool),
    "AddItemPreviewFile": ([C.c_void_p, C.c_uint64, C.c_char_p, C.c_int32], C.c_bool),
}


def bind_api(steam):
    for method, (arguments, result) in API.items():
        steam.fn("SteamAPI_ISteamUGC_" + method, arguments, result)


def local_images(root, version, require_frozen=True):
    """No Steam initialization. Reject drafts before an upload can start."""
    root = Path(root).resolve()
    workshop = root / "workshop"
    manifest = json.loads((workshop / "images-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != "heart-of-devouring-workshop-images-v1":
        raise RuntimeError("Workshop image manifest schema differs")
    if manifest.get("language") != "l_simp_chinese" or manifest.get("version") != version:
        raise RuntimeError("Workshop image language or version differs")
    if require_frozen and (manifest.get("status") != "FROZEN"
                           or manifest.get("final_release_selection") is not True):
        raise RuntimeError("Workshop images have not been frozen")
    images = manifest.get("images", [])
    if [entry.get("id") for entry in images] != [f"WS-{i:02}" for i in range(7)]:
        raise RuntimeError("Workshop images must cover the seven ordered IDs")
    checked, used = [], set()
    for entry in images:
        if require_frozen and entry.get("status") != "READY":
            raise RuntimeError("Workshop image is not ready: " + entry["id"])
        if "file" not in entry:
            if require_frozen:
                raise RuntimeError("Workshop image file is missing")
            continue
        expected_role = "cover" if entry["id"] == "WS-00" else "gallery"
        if entry.get("role") != expected_role or not entry.get("caption", "").strip():
            raise RuntimeError("Workshop image role or caption differs")
        path = (workshop / entry["file"]).resolve()
        source = (workshop / entry["source"]).resolve()
        path.relative_to(root)
        source.relative_to(root)
        if path in used:
            raise RuntimeError("duplicate Workshop image")
        used.add(path)
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if (digest != entry.get("sha256") or len(raw) != entry.get("bytes")
                or raw != source.read_bytes()):
            raise RuntimeError("Workshop image differs from its source")
        if not raw or len(raw) >= 1_000_000:
            raise RuntimeError("Workshop image must be under 1MB")
        with Image.open(path) as picture:
            size, kind = picture.size, picture.format
            picture.verify()
        if (size != (entry.get("width"), entry.get("height"))
                or kind != entry.get("format") or kind not in ("JPEG", "PNG")):
            raise RuntimeError("Workshop image dimensions or format differ")
        if expected_role == "cover" and path != root / "mod/thumbnail.png":
            raise RuntimeError("Workshop cover must match the production thumbnail")
        if entry.get("evidence_kind") == "native_screenshot":
            evidence = json.loads(source.with_suffix(".ocr.json").read_text(encoding="utf-8"))
            labels = [row["text"] for row in evidence["rows"]]
            if evidence.get("image_sha256") != digest or entry.get("game_date") not in labels:
                raise RuntimeError("native Workshop screenshot lacks matching GPU evidence")
            if any(re.search(r"\beep_[a-z]|Debug Controls|Debug View", text) for text in labels):
                raise RuntimeError("debug controls or untranslated keys in Workshop screenshot")
            save = (workshop / entry["native_save"]).resolve()
            save.relative_to(root)
            audit = json.loads(save.with_suffix(".audit.json").read_text(encoding="utf-8"))
            if (hashlib.sha256(save.read_bytes()).hexdigest() != audit.get("save_sha256")
                    or audit.get("date") != entry.get("native_save_date")):
                raise RuntimeError("Workshop screenshot native save evidence differs")
        checked.append({**entry, "file": str(path.relative_to(root)).replace("\\", "/")})
    return checked


def remote_previews(steam, item_id):
    """Read an uncached query and always release its native handle."""
    if item_id <= 0 or item_id == FORBIDDEN_ID:
        raise RuntimeError("invalid or read-only Workshop item")
    bind_api(steam)
    ids = (C.c_uint64 * 1)(item_id)
    query = steam.call("CreateQueryUGCDetailsRequest", ids, 1)
    if query in (0, INVALID_HANDLE):
        raise RuntimeError("Workshop preview query handle is invalid")
    try:
        if not steam.call("SetReturnAdditionalPreviews", query, True):
            raise RuntimeError("Workshop preview query configuration failed")
        if not steam.call("SetAllowCachedResponse", query, 0):
            raise RuntimeError("Workshop preview query cache configuration failed")
        completed = steam.wait(steam.call("SendQueryUGCRequest", query), QueryCompleted, 3401)
        if (completed.handle != query or completed.result != 1 or completed.returned != 1
                or completed.cached):
            raise RuntimeError("Workshop preview query result differs or is cached")
        count = steam.call("GetQueryUGCNumAdditionalPreviews", query, 0)
        result = []
        for index in range(count):
            url, name, kind = C.create_string_buffer(8192), C.create_string_buffer(1024), C.c_int32()
            if not steam.call("GetQueryUGCAdditionalPreview", query, 0, index,
                              url, len(url), name, len(name), C.byref(kind)):
                raise RuntimeError("Workshop additional preview read failed")
            result.append({"index": index, "url": url.value.decode("utf-8"),
                           "filename": name.value.decode("utf-8"), "type": kind.value})
        return result
    finally:
        if not steam.call("ReleaseQueryUGCRequest", query):
            raise RuntimeError("Workshop preview query handle release failed")


def replace_previews(steam, update, existing, gallery, root):
    """Replace this mod's selected gallery, including a failed-upload retry."""
    root = Path(root).resolve()
    for index in range(len(existing) - 1, -1, -1):
        if not steam.call("RemoveItemPreview", update, index):
            raise RuntimeError("Workshop old preview removal failed")
    for image in gallery:
        path = (root / image["file"]).resolve()
        path.relative_to(root)
        if hashlib.sha256(path.read_bytes()).hexdigest() != image["sha256"]:
            raise RuntimeError("Workshop gallery changed after preflight")
        if not steam.call("AddItemPreviewFile", update, str(path).encode("utf-8"), 0):
            raise RuntimeError("Workshop gallery upload configuration failed")


def verify_previews(actual, expected, fetch=None):
    """A remote mismatch never produces a PASS receipt."""
    if len(actual) != len(expected):
        raise RuntimeError("remote Workshop gallery count differs")
    if fetch is None:
        def fetch(url):
            with urllib.request.urlopen(url, timeout=30) as response:
                return response.read(1_000_001)
    checked = []
    for index, (remote, local) in enumerate(zip(actual, expected, strict=True)):
        if (remote["index"] != index or remote["type"] != 0
                or remote["filename"] != Path(local["file"]).name):
            raise RuntimeError("remote Workshop gallery order, type or filename differs")
        raw = fetch(remote["url"])
        if (len(raw) != local["bytes"] or hashlib.sha256(raw).hexdigest() != local["sha256"]):
            raise RuntimeError("remote Workshop gallery bytes differ")
        checked.append({**remote, "sha256": local["sha256"], "bytes": len(raw)})
    return checked
