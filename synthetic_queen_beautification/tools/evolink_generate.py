"""Submit and retrieve an audited EvoLink transparent portrait generation.

Only public request parameters and task IDs are persisted. The API key and
temporary result URL stay in memory and are never printed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests


API_ROOT = "https://api.evolink.ai/v1"
REFERENCE_URL = (
    "https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/main/"
    "synthetic_queen_beautification/assets/reference/cetana-reference.jpg"
)
DEFAULT_PROMPT = Path(__file__).resolve().parents[1] / "assets/prompts/cetana-transparent-v3.txt"


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def api_request(method: str, path: str, payload: dict[str, object] | None = None) -> dict:
    key = os.environ.get("EVOLINK_API_KEY")
    if not key:
        raise RuntimeError("EVOLINK_API_KEY is not set")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        API_ROOT + path,
        data=data,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method=method,
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise RuntimeError("EvoLink returned a non-object response")
    return result


def task_id_from(result: dict) -> str:
    task_id = result.get("id")
    if not isinstance(task_id, str) or not re.fullmatch(r"task-[A-Za-z0-9-]+", task_id):
        raise RuntimeError("EvoLink response did not contain a valid task ID")
    return task_id


def submit(attempt: Path, prompt_path: Path) -> None:
    if attempt.exists():
        raise FileExistsError(f"attempt already exists: {attempt}")
    prompt = prompt_path.read_text(encoding="utf-8")
    public_request: dict[str, object] = {
        "endpoint": API_ROOT + "/images/generations",
        "model": "gpt-image-2",
        "prompt_file": "original.prompt.txt",
        "size": "16:9",
        "resolution": "2K",
        "quality": "high",
        "background": "transparent",
        "output_format": "png",
        "n": 1,
        "image_urls": [REFERENCE_URL],
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


def find_result_url(value: object) -> str | None:
    if isinstance(value, dict):
        for key in ("results", "output", "images", "data", "url", "image_url"):
            if key in value:
                found = find_result_url(value[key])
                if found:
                    return found
    elif isinstance(value, list):
        for item in value:
            found = find_result_url(item)
            if found:
                return found
    elif isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme == "https" and parsed.netloc and parsed.path.lower().endswith((".png", ".webp")):
            return value
    return None


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
    url = find_result_url(result)
    if not url:
        print("completed task has no recognized PNG URL; top-level fields: " + ", ".join(result))
        return
    output = attempt / "original.png"
    if output.exists():
        print("original.png already exists; refusing to overwrite")
        return
    if urlsplit(url).netloc != "files.evolink.ai":
        raise RuntimeError("EvoLink result is not hosted on the expected file domain")
    response = requests.get(url, timeout=90)
    if response.status_code != 200:
        raise RuntimeError(f"EvoLink file download returned HTTP {response.status_code}")
    content = response.content
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("EvoLink result is not a PNG")
    output.write_bytes(content)
    write_json(attempt / "result.status.json", {
        "task_id": task_id,
        "status": status,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "file": output.name,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    })
    print(f"saved {output} ({len(content)} bytes)")


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
