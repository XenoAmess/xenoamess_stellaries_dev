"""Extract the EvoLink V2 Vivhite figure; archive prompt, task, and layers."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

from evolink_generate import API, ART, api_request, task_id_from, write_json
from evolink_layerize import image_url, result_items


SOURCE = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/"
    "8d69c82/assets/shishan-code-origin/generated/A10-attempt-03/original.png"
)
ATTEMPT = ART / "generated" / "A10-layerize-03"
PROMPT = ART / "prompts" / "A10-vivhite-concept-v2-layerize.txt"


def submit() -> None:
    if ATTEMPT.exists():
        raise FileExistsError(ATTEMPT)
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    public = {
        "endpoint": API + "/images/generations",
        "model": "doubao-seedream-5.0-pro-layerize",
        "prompt_file": "original.prompt.txt",
        "image_urls": [SOURCE],
        "quality": "2K",
        "output_format": "png",
    }
    payload = {k: v for k, v in public.items() if k not in ("endpoint", "prompt_file")}
    payload["prompt"] = prompt
    ATTEMPT.mkdir(parents=True)
    (ATTEMPT / "original.prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(ATTEMPT / "original.request.json", public)
    task_id = task_id_from(api_request("POST", "/images/generations", payload))
    write_json(ATTEMPT / "original.task.json", {"task_id": task_id})
    print(f"submitted {task_id}", flush=True)


def poll() -> str:
    status_file = ATTEMPT / "result.status.json"
    if status_file.exists() and json.loads(status_file.read_text(encoding="utf-8")).get("status") == "downloaded":
        return "downloaded"
    task = json.loads((ATTEMPT / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown")).lower()
    if status not in ("completed", "succeeded", "success"):
        if status in ("failed", "error", "cancelled", "canceled"):
            write_json(status_file, {"task_id": task_id, "status": status})
        return status
    items = result_items(result)
    if not items:
        return "no_layers"
    saved = []
    for index, item in enumerate(items):
        url = image_url(item)
        if not url or urlsplit(url).netloc not in {
            "files.evolink.ai", "ark-acg-cn-beijing.tos-cn-beijing.volces.com"
        }:
            raise RuntimeError(f"layer {index} has no supported image URL")
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        content = response.content
        if not content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError(f"layer {index} is not PNG")
        output = ATTEMPT / f"layer-{index:02d}.png"
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "poll"))
    args = parser.parse_args()
    if args.action == "submit":
        submit()
    else:
        print(poll(), flush=True)
