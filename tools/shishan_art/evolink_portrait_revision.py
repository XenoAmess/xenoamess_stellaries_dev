"""Archive the second EvoLink Vivhite portrait attempt with sharp hair edges."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

from evolink_generate import API, ART, REFERENCE, api_request, find_result_url, task_id_from, write_json


ATTEMPT = ART / "generated" / "A10-attempt-02"
PROMPT = ART / "prompts" / "A10-vivhite-portrait-hair-edge-v2.txt"


def submit() -> None:
    if ATTEMPT.exists():
        raise FileExistsError(ATTEMPT)
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    public = {
        "endpoint": API + "/images/generations",
        "model": "gpt-image-2.5-sunburst",
        "prompt_file": "original.prompt.txt",
        "size": "2:3",
        "resolution": "2K",
        "quality": "xhigh",
        "background": "transparent",
        "output_format": "png",
        "n": 1,
        "image_urls": [REFERENCE],
    }
    payload = {k: v for k, v in public.items() if k not in ("endpoint", "prompt_file")}
    payload["prompt"] = prompt
    ATTEMPT.mkdir(parents=True)
    (ATTEMPT / "original.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(ATTEMPT / "original.request.json", public)
    try:
        result = api_request("POST", "/images/generations", payload)
        task_id = task_id_from(result)
    except Exception as error:
        write_json(ATTEMPT / "result.status.json", {"status": "submission_failed", "error": str(error)})
        raise
    write_json(ATTEMPT / "original.task.json", {"task_id": task_id})
    print(f"submitted {task_id}")


def poll() -> str:
    output = ATTEMPT / "original.png"
    if output.exists():
        return "downloaded"
    task = json.loads((ATTEMPT / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown")).lower()
    if status in {"failed", "error", "cancelled", "canceled"}:
        write_json(ATTEMPT / "result.status.json", {"task_id": task_id, "status": status})
        return status
    if status not in {"completed", "succeeded", "success"}:
        return status
    url = find_result_url(result)
    if not url:
        return "no_png_url"
    if urlsplit(url).netloc != "files.evolink.ai":
        return "unexpected_file_host"
    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        return f"download_http_{response.status_code}"
    content = response.content
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "invalid_png"
    output.write_bytes(content)
    write_json(ATTEMPT / "result.status.json", {
        "task_id": task_id,
        "status": "downloaded",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    })
    return "downloaded"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "poll"))
    args = parser.parse_args()
    if args.action == "submit":
        submit()
    else:
        print(poll())


if __name__ == "__main__":
    main()
