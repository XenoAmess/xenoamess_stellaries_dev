"""Extract central subject layers from archived EvoLink art attempts.

Every provider output is saved. No credential or temporary signed URL is
written to disk. Inputs are immutable raw GitHub URLs from commit 642ba08.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

from evolink_generate import API, ART, ASSETS, api_request, task_id_from, write_json


SOURCE_COMMIT = "642ba08"
SOURCE_BASE = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/"
    + SOURCE_COMMIT + "/assets/shishan-code-origin/generated/"
)
PORTRAIT_V2_URL = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/"
    "7bcbbde/assets/shishan-code-origin/generated/A10-attempt-02/original.png"
)
SUBJECTS = {
    "A01": "the single complete central patched processor origin symbol, including all attached gold cables and floating violet circuit shards",
    "A03": "the single complete central broken robotic processor trait emblem, including its cracked ceramic shell and attached tangled cables",
    "A04": "the single complete central repaired robotic processor trait emblem",
    "A06": "the single complete maintenance emblem: the cracked processor, attached violet patch plate and the repair spanner together",
    "A07": "the single complete refactor emblem: both halves of the old processor and the clean rising center core together",
    "A08": "the single complete research institute building, including its antennas and side structures",
    "A09": "the single complete robotic maintainer worker with both hands, repair tools and the processor held in front of it",
    "A10": "Vivhite, the single complete white-haired android woman, including all hair strands, black-gold hair ornaments, glasses, arms, hands and upper torso",
    "A11": "the single complete Vivhite leader trait emblem, including her head, wing ornaments and the damaged violet heart core",
}


def prompt_for(asset_id: str) -> str:
    return (
        "Isolate " + SUBJECTS[asset_id] + " as ONE coherent foreground layer with a clean exact cutout. "
        "Separate away the entire dark vignette, gray or purple gradient background, ambient glow cloud, "
        "lighting haze and ground shadow. Keep only the physical object and its directly attached details; "
        "preserve the original drawing, colors, silhouette and facial identity without redesign. "
        "Everything outside the subject must be fully transparent."
    )


def attempt_dir(asset_id: str, portrait_v2: bool = False) -> Path:
    name = "A10-layerize-02" if portrait_v2 else f"{asset_id}-layerize-01"
    return ART / "generated" / name


def submit(asset_id: str, portrait_v2: bool = False) -> None:
    if portrait_v2 and asset_id != "A10":
        raise ValueError("--portrait-v2 is only valid for A10")
    attempt = attempt_dir(asset_id, portrait_v2)
    if attempt.exists():
        raise RuntimeError(f"Attempt already exists: {attempt}")
    input_url = PORTRAIT_V2_URL if portrait_v2 else SOURCE_BASE + f"{asset_id}-attempt-01/original.png"
    prompt = (
        (ART / "prompts" / "A10-vivhite-layerize-hair-edge-v2.txt").read_text(encoding="utf-8").strip()
        if portrait_v2 else prompt_for(asset_id)
    )
    public = {
        "endpoint": API + "/images/generations",
        "model": "doubao-seedream-5.0-pro-layerize",
        "prompt_file": "original.prompt.txt",
        "image_urls": [input_url],
        "quality": "2K" if asset_id == "A10" else "1K",
        "output_format": "png",
    }
    payload = {k: v for k, v in public.items() if k not in ("endpoint", "prompt_file")}
    payload["prompt"] = prompt
    attempt.mkdir(parents=True)
    (attempt / "original.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(attempt / "original.request.json", public)
    try:
        result = api_request("POST", "/images/generations", payload)
        task_id = task_id_from(result)
    except Exception as error:
        write_json(attempt / "result.status.json", {"status": "submission_failed", "error": str(error)})
        raise
    write_json(attempt / "original.task.json", {"task_id": task_id})
    print(f"{asset_id}: submitted {task_id}", flush=True)


def image_url(value: object) -> str | None:
    if isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme == "https" and parsed.path.lower().endswith((".png", ".jpg", ".jpeg")):
            return value
    if isinstance(value, dict):
        for key in ("url", "image_url", "file_url", "output", "image"):
            if key in value:
                found = image_url(value[key])
                if found:
                    return found
    return None


def result_items(value: object) -> list[dict]:
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        if any("z_index" in item or image_url(item) for item in value):
            return value
    if isinstance(value, dict):
        for key in ("result_data", "results", "output", "data"):
            if key in value:
                found = result_items(value[key])
                if found:
                    return found
    return []


def poll(asset_id: str, portrait_v2: bool = False) -> str:
    attempt = attempt_dir(asset_id, portrait_v2)
    status_file = attempt / "result.status.json"
    if status_file.exists():
        old = json.loads(status_file.read_text(encoding="utf-8"))
        if old.get("status") == "downloaded":
            return "downloaded"
    task = json.loads((attempt / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown")).lower()
    if status in {"failed", "error", "cancelled", "canceled"}:
        write_json(status_file, {"task_id": task_id, "status": status})
        return status
    if status not in {"completed", "succeeded", "success"}:
        return status
    items = result_items(result)
    if not items:
        return "no_layers"
    saved = []
    for index, item in enumerate(items):
        url = image_url(item)
        if not url:
            raise RuntimeError(f"layer {index} has no image URL")
        if urlsplit(url).netloc not in {
            "files.evolink.ai", "ark-acg-cn-beijing.tos-cn-beijing.volces.com"
        }:
            raise RuntimeError(f"layer {index} has an unexpected file host")
        response = requests.get(url, timeout=120)
        if response.status_code != 200:
            return f"download_http_{response.status_code}"
        content = response.content
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            suffix = ".png"
        elif content.startswith(b"\xff\xd8\xff"):
            suffix = ".jpg"
        else:
            raise RuntimeError(f"layer {index} has an unexpected file format")
        output = attempt / f"layer-{index:02d}{suffix}"
        if output.exists():
            if hashlib.sha256(output.read_bytes()).digest() != hashlib.sha256(content).digest():
                raise RuntimeError(f"existing layer differs: {output}")
        else:
            output.write_bytes(content)
        saved.append({
            "file": output.name,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
            "z_index": item.get("z_index"),
            "name": item.get("name"),
            "description": item.get("description"),
            "bounding_box": item.get("bounding_box"),
        })
    write_json(status_file, {
        "task_id": task_id,
        "status": "downloaded",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "layers": saved,
    })
    return "downloaded"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "submit-all", "poll", "poll-all"))
    parser.add_argument("asset_id", nargs="?", choices=ASSETS)
    parser.add_argument("--portrait-v2", action="store_true")
    args = parser.parse_args()
    if args.action in ("submit", "poll") and not args.asset_id:
        parser.error("asset_id required")
    if args.portrait_v2 and args.action in ("submit-all", "poll-all"):
        parser.error("--portrait-v2 requires a single A10 task")
    if args.action == "submit":
        submit(args.asset_id, args.portrait_v2)
    elif args.action == "submit-all":
        for asset_id in ASSETS:
            submit(asset_id)
    elif args.action == "poll":
        print(f"{args.asset_id}: {poll(args.asset_id, args.portrait_v2)}", flush=True)
    else:
        pending = set(ASSETS)
        deadline = time.monotonic() + 1800
        while pending and time.monotonic() < deadline:
            for asset_id in sorted(pending):
                try:
                    status = poll(asset_id)
                except Exception as error:
                    status = f"poll_error: {error}"
                print(f"{asset_id}: {status}", flush=True)
                if status in {"downloaded", "failed", "error", "cancelled", "canceled"}:
                    pending.remove(asset_id)
            if pending:
                time.sleep(20)
        if pending:
            raise RuntimeError("Timed out waiting for: " + ", ".join(sorted(pending)))


if __name__ == "__main__":
    main()
