"""Ask EvoLink Layerize for a person layer with true alpha, without logging credentials or URLs."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

from evolink_generate import REFERENCE_URL, api_request, task_id_from, write_json


MOD_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPT = MOD_ROOT / "assets/prompts/laoda-layerize-v1.txt"


def submit(attempt: Path, prompt_path: Path) -> None:
    if attempt.exists():
        raise FileExistsError(attempt)
    prompt = prompt_path.read_text(encoding="utf-8")
    public_request: dict[str, object] = {
        "endpoint": "https://api.evolink.ai/v1/images/generations",
        "model": "doubao-seedream-5.0-pro-layerize",
        "prompt_file": "original.prompt.txt",
        "image_urls": [REFERENCE_URL],
        "quality": "1K",
        "output_format": "png",
    }
    payload = {key: value for key, value in public_request.items() if key not in {"endpoint", "prompt_file"}}
    payload["prompt"] = prompt
    attempt.mkdir(parents=True)
    (attempt / "original.prompt.txt").write_text(prompt, encoding="utf-8")
    write_json(attempt / "original.request.json", public_request)
    result = api_request("POST", "/images/generations", payload)
    task_id = task_id_from(result)
    write_json(attempt / "original.task.json", {"task_id": task_id})
    print(f"submitted {task_id}")


def image_url(value: object) -> str | None:
    if isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme == "https" and parsed.path.lower().endswith((".png", ".jpg", ".jpeg")):
            return value
    elif isinstance(value, dict):
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


def poll(attempt: Path) -> None:
    task = json.loads((attempt / "original.task.json").read_text(encoding="utf-8"))
    task_id = task_id_from({"id": task["task_id"]})
    result = api_request("GET", "/tasks/" + task_id)
    status = str(result.get("status", "unknown"))
    print(f"{task_id}: {status}")
    if status.lower() in {"failed", "error", "cancelled", "canceled"}:
        write_json(attempt / "result.status.json", {"task_id": task_id, "status": status})
        raise RuntimeError("EvoLink task failed; inspect the provider console using the task ID")
    if status.lower() not in {"completed", "succeeded", "success"}:
        return
    items = result_items(result)
    if not items:
        print("completed task has no recognized layers; top-level fields: " + ", ".join(result))
        return
    manifest: list[dict[str, object]] = []
    for index, item in enumerate(items):
        url = image_url(item)
        if not url:
            raise RuntimeError(f"layer {index} has no recognized image URL")
        if urlsplit(url).netloc not in {
            "files.evolink.ai",
            "ark-acg-cn-beijing.tos-cn-beijing.volces.com",
        }:
            raise RuntimeError(f"layer {index} is not hosted on the expected file domain")
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        content = response.content
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            extension = ".png"
        elif content.startswith(b"\xff\xd8\xff"):
            extension = ".jpg"
        else:
            raise RuntimeError(f"layer {index} has an unexpected image type")
        output = attempt / f"layer-{index:02d}{extension}"
        if output.exists():
            raise FileExistsError(output)
        output.write_bytes(content)
        manifest.append({
            "file": output.name,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
            "z_index": item.get("z_index"),
            "name": item.get("name"),
            "description": item.get("description"),
            "bounding_box": item.get("bounding_box"),
        })
        print(f"saved {output.name} ({len(content)} bytes)")
    write_json(attempt / "result.status.json", {
        "task_id": task_id,
        "status": status,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "layers": manifest,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("submit", "poll"))
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    arguments = parser.parse_args()
    if arguments.action == "submit":
        submit(arguments.attempt, arguments.prompt)
    else:
        poll(arguments.attempt)


if __name__ == "__main__":
    main()
