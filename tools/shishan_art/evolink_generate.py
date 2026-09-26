"""Generate and archive transparent Shishan Code art with EvoLink.

The API key and signed download URL remain in memory. The checked-in attempt
directory contains only the public request, prompt, task ID and final PNG.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "assets" / "shishan-code-origin"
API = "https://api.evolink.ai/v1"
REFERENCE = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/"
    "bf77061/assets/shishan-code-origin/reference/vivhite-concept.png"
)
ASSETS = {
    "A01": ("origin-icon", "1:1", "1K", "medium"),
    "A03": ("broken-trait", "1:1", "1K", "medium"),
    "A04": ("refactored-trait", "1:1", "1K", "medium"),
    "A06": ("maintain-project", "1:1", "1K", "medium"),
    "A07": ("refactor-project", "1:1", "1K", "medium"),
    "A08": ("maintenance-building", "1:1", "1K", "medium"),
    "A09": ("maintainer-job", "1:1", "1K", "medium"),
    "A10": ("vivhite-portrait", "2:3", "2K", "high"),
    "A11": ("vivhite-leader-trait", "1:1", "1K", "medium"),
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def api_request(method: str, path: str, payload: dict | None = None) -> dict:
    key = os.environ.get("EVOLINK_API_KEY")
    if not key:
        raise RuntimeError("EVOLINK_API_KEY is not set")
    request = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        # The body can contain an account identifier or temporary URL.
        raise RuntimeError(f"EvoLink returned HTTP {error.code}") from None
    if not isinstance(result, dict):
        raise RuntimeError("EvoLink returned a non-object response")
    return result


def task_id_from(result: dict) -> str:
    task_id = result.get("id")
    if not isinstance(task_id, str) or not re.fullmatch(r"task-[A-Za-z0-9-]+", task_id):
        raise RuntimeError("EvoLink response has no valid task ID")
    return task_id


def find_result_url(value: object) -> str | None:
    if isinstance(value, dict):
        for key in ("results", "output", "images", "data", "url", "image_url"):
            if key in value:
                found = find_result_url(value[key])
                if found:
                    return found
    if isinstance(value, list):
        for item in value:
            found = find_result_url(item)
            if found:
                return found
    if isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme == "https" and parsed.path.lower().endswith(".png"):
            return value
    return None


def attempt_dir(asset_id: str) -> Path:
    return ART / "generated" / f"{asset_id}-attempt-01"


def submit(asset_id: str) -> None:
    name, size, resolution, quality = ASSETS[asset_id]
    attempt = attempt_dir(asset_id)
    if attempt.exists():
        raise RuntimeError(f"Attempt already exists: {attempt}")
    prompt_path = ART / "prompts" / f"{asset_id}-{name}.txt"
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    public_request = {
        "endpoint": API + "/images/generations",
        "model": "gpt-image-2",
        "prompt_file": "original.prompt.txt",
        "size": size,
        "resolution": resolution,
        "quality": quality,
        "background": "transparent",
        "output_format": "png",
        "n": 1,
        "image_urls": [REFERENCE],
    }
    payload = {k: v for k, v in public_request.items() if k not in ("endpoint", "prompt_file")}
    payload["prompt"] = prompt
    attempt.mkdir(parents=True)
    (attempt / "original.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(attempt / "original.request.json", public_request)
    try:
        result = api_request("POST", "/images/generations", payload)
        task_id = task_id_from(result)
    except Exception as error:
        write_json(attempt / "result.status.json", {"status": "submission_failed", "error": str(error)})
        raise
    write_json(attempt / "original.task.json", {"task_id": task_id})
    print(f"{asset_id}: submitted {task_id}", flush=True)


def poll(asset_id: str) -> str:
    attempt = attempt_dir(asset_id)
    if (attempt / "original.png").exists():
        return "downloaded"
    task = json.loads((attempt / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown")).lower()
    if status in ("failed", "error", "cancelled", "canceled"):
        write_json(attempt / "result.status.json", {"task_id": task_id, "status": status})
        return status
    if status not in ("completed", "succeeded", "success"):
        return status
    url = find_result_url(result)
    if not url:
        write_json(attempt / "result.status.json", {"task_id": task_id, "status": "no_png_url"})
        return "no_png_url"
    if urlsplit(url).netloc != "files.evolink.ai":
        write_json(attempt / "result.status.json", {"task_id": task_id, "status": "unexpected_file_host"})
        return "unexpected_file_host"
    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        return f"download_http_{response.status_code}"
    content = response.content
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        write_json(attempt / "result.status.json", {"task_id": task_id, "status": "invalid_png"})
        return "invalid_png"
    output = attempt / "original.png"
    output.write_bytes(content)
    write_json(attempt / "result.status.json", {
        "task_id": task_id,
        "status": "downloaded",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    })
    return "downloaded"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "submit-all", "poll", "poll-all"))
    parser.add_argument("asset_id", nargs="?", choices=ASSETS)
    args = parser.parse_args()
    if args.action in ("submit", "poll") and not args.asset_id:
        parser.error("asset_id required")
    if args.action == "submit":
        submit(args.asset_id)
    elif args.action == "submit-all":
        for asset_id in ASSETS:
            submit(asset_id)
    elif args.action == "poll":
        print(f"{args.asset_id}: {poll(args.asset_id)}", flush=True)
    else:
        pending = set(ASSETS)
        deadline = time.monotonic() + 1200
        while pending and time.monotonic() < deadline:
            for asset_id in sorted(pending):
                try:
                    status = poll(asset_id)
                except Exception as error:
                    status = f"poll_error: {error}"
                print(f"{asset_id}: {status}", flush=True)
                if status in {"downloaded", "failed", "error", "cancelled", "canceled", "no_png_url", "unexpected_file_host", "invalid_png"}:
                    pending.remove(asset_id)
            if pending:
                time.sleep(20)
        if pending:
            raise RuntimeError("Timed out waiting for: " + ", ".join(sorted(pending)))


if __name__ == "__main__":
    main()
