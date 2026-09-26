"""Generate the V2 Vivhite cutout on EvoLink and archive public evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

from evolink_generate import API, ART, api_request, find_result_url, task_id_from, write_json


REFERENCE = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/"
    "0ff99e5/assets/shishan-code-origin/reference/vivhite-concept-v2.png"
)
ATTEMPT = ART / "generated" / "A10-attempt-03"
PROMPT = ART / "prompts" / "A10-vivhite-portrait-concept-v2.txt"


def submit() -> None:
    if ATTEMPT.exists():
        raise FileExistsError(ATTEMPT)
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    public_request = {
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
    payload = {k: v for k, v in public_request.items() if k not in ("endpoint", "prompt_file")}
    payload["prompt"] = prompt
    ATTEMPT.mkdir(parents=True)
    (ATTEMPT / "original.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(ATTEMPT / "original.request.json", public_request)
    result = api_request("POST", "/images/generations", payload)
    task_id = task_id_from(result)
    write_json(ATTEMPT / "original.task.json", {"task_id": task_id})
    print(f"submitted {task_id}", flush=True)


def poll() -> str:
    if (ATTEMPT / "original.png").exists():
        return "downloaded"
    task = json.loads((ATTEMPT / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown")).lower()
    if status not in ("completed", "succeeded", "success"):
        if status in ("failed", "error", "cancelled", "canceled"):
            write_json(ATTEMPT / "result.status.json", {"task_id": task_id, "status": status})
        return status
    url = find_result_url(result)
    if not url or urlsplit(url).netloc != "files.evolink.ai":
        raise RuntimeError("EvoLink returned no supported PNG URL")
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    content = response.content
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("EvoLink returned a non-PNG image")
    (ATTEMPT / "original.png").write_bytes(content)
    write_json(ATTEMPT / "result.status.json", {
        "task_id": task_id,
        "status": "downloaded",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    })
    return "downloaded"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "poll"))
    args = parser.parse_args()
    print(poll() if args.action == "poll" else submit(), flush=True)
