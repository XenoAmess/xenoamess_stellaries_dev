"""Frozen formal update of this project's own item; never CreateItem."""
import argparse
import ctypes as C
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request

from PIL import Image
import publish as base
import workshop_images

ROOT, REPO, MOD = base.ROOT, base.REPO, base.MOD
VERSION = "0.3.1"
ITEM = 3815707212
CANDIDATE = "62e273a504a817be3c4037340557c4f1e3e2e522"
EXE_SHA = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
PROOFS = ROOT / "docs/evidence/1015-2026-10-15"
EVIDENCE = ROOT / f"docs/evidence/publication-{VERSION}"
STATE = EVIDENCE / "publish-state.json"
ACCEPTANCE = EVIDENCE / "acceptance.json"
STATIC = EVIDENCE / "open-kaishek.json"
DOWNLOAD = EVIDENCE / "workshop-download.json"
VERIFIED = EVIDENCE / "workshop-verification.json"
INLINE = EVIDENCE / "inline-images.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def candidate_bytes(path):
    return git("show", f"{CANDIDATE}:{path.relative_to(REPO).as_posix()}")


def release_entry():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"^## {re.escape(VERSION)} — [^\n]+\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not match:
        raise RuntimeError("formal changelog entry missing")
    entry = match.group(1).strip()
    for label in ("新增", "变更", "修复", "兼容", "验收", "已知限制"):
        if f"- {label}：" not in entry:
            raise RuntimeError("incomplete changelog")
    return entry


def change_note():
    return f"[v{VERSION}]\n" + release_entry()


def validate_target(item, version, prior, state):
    if item != ITEM or item == base.FORBIDDEN_ID:
        raise RuntimeError("only this project's existing Workshop item may be updated")
    if version != VERSION or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise RuntimeError("only the frozen unused formal version may be published")
    if prior.get("status") != "PASS" or prior.get("item_id") != item or prior.get("version") == version:
        raise RuntimeError("previous verified release identity differs or version was already published")
    if state and (state.get("item_id") != item or state.get("version") != version):
        raise RuntimeError("retry identity differs")
    if state.get("submit_result") == 1:
        raise RuntimeError("successful version must not be uploaded again")
    if state.get("submit_started") and "submit_result" not in state:
        raise RuntimeError("previous upload outcome unknown; reconcile remote before any retry")


def accepted_files():
    files = base.manifest(MOD)
    names = git("ls-tree", "-r", "--name-only", CANDIDATE, "--", "eat_everything_origin/mod").decode().splitlines()
    original = {name.removeprefix("eat_everything_origin/mod/"): git("show", f"{CANDIDATE}:{name}") for name in names}
    if set(files) != set(original):
        raise RuntimeError("formal package file set differs from accepted candidate")
    for name, raw in original.items():
        if name == "descriptor.mod":
            raw = raw.replace(b'version="0.3.0-rc.1"', f'version="{VERSION}"'.encode())
        if files[name] != digest(raw):
            raise RuntimeError("formal content drift from accepted candidate: " + name)
    index_path = PROOFS / "final-evidence-index.json"
    if index_path.read_bytes() != candidate_bytes(index_path):
        raise RuntimeError("candidate evidence index changed")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if (index.get("status") != "PASS_SCOPED" or index.get("mod_version") != "0.3.0-rc.1"
            or len(index.get("proofs", [])) != 8 or not index.get("original_stopped_campaign_source_unchanged")):
        raise RuntimeError("final scoped acceptance index differs")
    for entry in index["proofs"] + index["archives"]:
        path = (PROOFS / entry["path"]).resolve()
        path.relative_to(PROOFS.resolve())
        if digest(path.read_bytes()) != entry["sha256"]:
            raise RuntimeError("accepted proof or archive index changed")
    for name in index["strict_failures_retained"]:
        path = PROOFS / name
        if path.read_bytes() != candidate_bytes(path):
            raise RuntimeError("original strict failure evidence changed")
    package = json.loads(STATIC.read_text(encoding="utf-8"))
    if (package.get("status") != "PASS" or package.get("game_exe_sha256") != EXE_SHA
            or package.get("p_scripts") != 24 or package.get("p_parsed") != 24
            or len(package.get("languages", [])) != 10 or package.get("localization_keys") != 101):
        raise RuntimeError("formal open_kaishek gate incomplete")
    return {"status": "PASS_SCOPED", "version": VERSION, "candidate": CANDIDATE,
            "production_files": files, "static_sha256": digest(STATIC.read_bytes()),
            "candidate_index_sha256": digest(index_path.read_bytes()),
            "scope": index["scope"], "proofs": index["proofs"],
            "only_mod_change_from_candidate": "descriptor version metadata"}


def inline_images(description, fetch=False):
    urls = re.findall(r"\[img\](.*?)\[/img\]", description)
    if len(urls) != 4 or len(set(urls)) != 4:
        raise RuntimeError("four distinct inline screenshots required")
    prefix = f"https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/{CANDIDATE}/"
    result = []
    for url in urls:
        if not url.startswith(prefix):
            raise RuntimeError("inline image must use the frozen public candidate commit")
        relative = url[len(prefix):]
        path = (REPO / relative).resolve()
        path.relative_to(PROOFS.resolve())
        raw = path.read_bytes()
        if raw != candidate_bytes(path):
            raise RuntimeError("inline screenshot changed from public candidate")
        with Image.open(io.BytesIO(raw)) as picture:
            size = picture.size
            picture.verify()
        entry = {"url": url, "file": relative, "sha256": digest(raw), "bytes": len(raw), "size": size}
        if fetch:
            with urllib.request.urlopen(url, timeout=45) as response:
                remote = response.read()
                if response.status != 200 or not response.headers.get("Content-Type", "").startswith("image/") or remote != raw:
                    raise RuntimeError("public inline image differs or is inaccessible")
            entry["public_bytes_exact"] = True
        result.append(entry)
    return result


def description_inputs():
    description = (ROOT / "workshop/description.bbcode").read_text(encoding="utf-8")
    if not description or len(description.encode("utf-8")) >= 8000:
        raise RuntimeError("Steam description byte limit exceeded")
    for required in (f"v{VERSION}", "changelog", "纵火本能", "其它路线开放但未完成完整实机验收", "默认", "关闭", "运行时不在范围内"):
        if required not in description:
            raise RuntimeError("description omits current gameplay or acceptance boundary")
    # Parse paired BBCode while allowing Steam's [*] list marker.
    stack = []
    for closing, tag in re.findall(r"\[(/?)(h[123]|b|i|u|list|olist|img|url)(?:=[^\]]*)?\]", description):
        if closing:
            if not stack or stack.pop() != tag:
                raise RuntimeError("unbalanced Workshop BBCode")
        else:
            stack.append(tag)
    if stack:
        raise RuntimeError("unclosed Workshop BBCode")
    return description, inline_images(description)


def prepare():
    acceptance = accepted_files()
    description, _ = description_inputs()
    pictures = inline_images(description, fetch=True)
    base.write_json(ACCEPTANCE, acceptance)
    base.write_json(INLINE, {"status": "PASS", "version": VERSION, "images": pictures})
    (ROOT / f"workshop/change-note-v{VERSION}.txt").write_text(change_note() + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS_SCOPED", "version": VERSION, "files": len(acceptance["production_files"]), "inline_images": len(pictures)}))


def preflight(require_clean=True):
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    prior = json.loads((ROOT / "docs/evidence/workshop-verification.json").read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    validate_target(int((ROOT / "workshop/item-id.txt").read_text().strip()), version, prior, state)
    acceptance = accepted_files()
    if acceptance != json.loads(ACCEPTANCE.read_text(encoding="utf-8")):
        raise RuntimeError("formal package or acceptance changed after freeze")
    description, pictures = description_inputs()
    remote = json.loads(INLINE.read_text(encoding="utf-8"))
    if remote.get("status") != "PASS" or [{k: v for k, v in p.items() if k != "public_bytes_exact"} for p in remote.get("images", [])] != json.loads(json.dumps(pictures)):
        raise RuntimeError("inline image validation changed")
    if not all(p.get("public_bytes_exact") for p in remote["images"]):
        raise RuntimeError("inline public images have not been verified")
    note = (ROOT / f"workshop/change-note-v{VERSION}.txt").read_text(encoding="utf-8").strip()
    if note != change_note():
        raise RuntimeError("Change Note differs from canonical formal changelog")
    images = workshop_images.local_images(ROOT, version)
    if require_clean and git("status", "--porcelain"):
        raise RuntimeError("commit and push frozen inputs before publication")
    head = git("rev-parse", "HEAD").decode().strip()
    if require_clean and git("rev-parse", "@{upstream}").decode().strip() != head:
        raise RuntimeError("frozen publication commit has not been pushed")
    return {"version": version, "head": head, "content": acceptance["production_files"], "description": description,
            "note": note, "images": images, "gallery": [p for p in images if p["role"] == "gallery"],
            "acceptance": acceptance, "inline_images": pictures}


def public_details():
    body = urllib.parse.urlencode({"itemcount": 1, "publishedfileids[0]": ITEM}).encode()
    req = urllib.request.Request("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/", data=body)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)["response"]["publishedfiledetails"][0]


def publish(inputs):
    # Repeat all offline guards immediately before native initialization.
    if inputs != preflight():
        raise RuntimeError("publication inputs changed")
    before = public_details()
    if (before.get("result") != 1 or before.get("title") != base.TITLE or before.get("consumer_app_id") != base.APP_ID
            or f"v{VERSION}" in before.get("description", "")):
        raise RuntimeError("remote identity differs or formal version is already visible")
    steam = base.native.Steam()
    try:
        existing = workshop_images.remote_previews(steam, ITEM)
        update = steam.call("StartItemUpdate", base.APP_ID, ITEM)
        if update in (0, 0xFFFFFFFFFFFFFFFF):
            raise RuntimeError("StartItemUpdate failed")
        for method, value in [("SetItemTitle", base.TITLE.encode("utf-8")),
                              ("SetItemDescription", inputs["description"].encode("utf-8")),
                              ("SetItemContent", os.fsencode(str(MOD.resolve()))),
                              ("SetItemPreview", os.fsencode(str((MOD / "thumbnail.png").resolve()))),
                              ("SetItemVisibility", 0)]:
            if not steam.call(method, update, value):
                raise RuntimeError(method + " failed")
        strings = (C.c_char_p * 3)(b"Origins", b"Events", b"Gameplay")
        if not steam.call("SetItemTags", update, C.byref(base.native.StringArray(strings, 3))):
            raise RuntimeError("SetItemTags failed")
        gallery_actions = workshop_images.update_previews_in_place(steam, update, existing, inputs["gallery"], ROOT)
        state = {"schema": "heart-of-devouring-workshop-update-v1", "version": VERSION, "item_id": ITEM,
                 "inputs": inputs, "previous_public_version": "0.3.0", "gallery_actions": gallery_actions, "submit_started": True,
                 "started_at_utc": datetime.now(timezone.utc).isoformat()}
        base.write_json(STATE, state)
        result = steam.wait(steam.call("SubmitItemUpdate", update, inputs["note"].encode("utf-8")), base.native.SubmitItemUpdateResult, 3404)
        state.update(submit_result=result.result, submit_item_id=result.item_id,
                     submit_legal_required=bool(result.legal), submitted_at_utc=datetime.now(timezone.utc).isoformat())
        base.write_json(STATE, state)
        if result.result != 1 or result.item_id != ITEM or result.legal:
            raise RuntimeError("Workshop update failed or requires legal agreement; receipt retained")
        print(json.dumps({"status": "UPLOADED", "version": VERSION, "item_id": ITEM}))
    finally:
        steam.close()


class PageImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs = dict(attrs)
            if attrs.get("src"):
                self.sources.append(attrs["src"])


def verify(download):
    base.STATE, base.DOWNLOAD_RECEIPT = STATE, DOWNLOAD
    core_report = EVIDENCE / "core-verification.json"
    base.verify(download, core_report)
    state = json.loads(STATE.read_text(encoding="utf-8"))
    with urllib.request.urlopen(f"https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM}&l=schinese", timeout=45) as response:
        raw = response.read()
    page = PageImages()
    page.feed(raw.decode("utf-8", "replace"))
    checks = []
    for image in state["inputs"]["inline_images"]:
        matches = [url for url in page.sources if image["url"] == url or image["url"] in urllib.parse.unquote(url)]
        if not matches:
            raise RuntimeError("inline screenshot was not rendered as an image in Workshop HTML")
        with urllib.request.urlopen(matches[0], timeout=45) as response:
            if digest(response.read()) != image["sha256"]:
                raise RuntimeError("rendered inline image bytes differ")
        checks.append({"source": image["url"], "rendered_src": matches[0], "sha256": image["sha256"]})
    report = json.loads(core_report.read_text(encoding="utf-8"))
    report.update(inline_images_exact=True, inline_images=checks, public_page_sha256=digest(raw))
    base.write_json(EVIDENCE / "public-page.json", {"url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={ITEM}&l=schinese", "sha256": digest(raw), "inline_images": checks})
    base.write_json(VERIFIED, report)
    print(json.dumps({"status": "PASS", "inline_images": len(checks), "gallery": len(report["gallery"])}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "preflight", "publish", "download", "verify"))
    parser.add_argument("--download", type=Path)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "download":
        base.STATE, base.DOWNLOAD_RECEIPT = STATE, DOWNLOAD
        base.download_item(args.timeout)
    elif args.command == "verify":
        if not args.download or not args.download.is_dir():
            raise RuntimeError("independent installed Workshop directory required")
        verify(args.download)
    else:
        inputs = preflight()
        if args.command == "publish":
            publish(inputs)
        else:
            print(json.dumps({"status": "PASS", "version": VERSION, "files": len(inputs["content"])}))


if __name__ == "__main__":
    main()
