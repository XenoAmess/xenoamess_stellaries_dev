"""Submit and archive Heart of Devouring art through the user's EvoLink service.

Each asset is a separate immutable attempt. Credentials and signed URLs stay
outside the repository. This module never edits provider image pixels.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit
import winreg

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets/queen-baiqi"
sys.path.insert(0, str(ROOT.parent / "tools/shishan_art"))
from evolink_generate import api_request, find_result_url, task_id_from

CACHE = Path(os.environ["LOCALAPPDATA"]) / "heart-of-devouring/evolink-uploads.json"
REFERENCES = [
    "generated/QBA-02-layerize-05/layer-01.png",
    "generated/QBA-01-layerize-03/layer-01.png",
]
SCENES = {
    "QBA-03-core": "A vast homeworld core sanctuary. Queen Baiqi dominates the foreground at the left, coldly surveying a curved observation aperture showing the civilization's one enormous homeworld with concentric cities and mining districts. Her amethyst heart jewel echoes a controlled planetary intake nexus. Proud absolute command, subjects and infrastructure subordinated to her will. No biological organ.",
    "QBA-04-devouring": "Queen Baiqi calmly commands the destruction of a whole rocky planet. She is in the left foreground, half-lidded eyes contemptuous, one gloved hand directing enormous controlled planetary plates and mineral streams toward the single visible homeworld on the right. Keep a legible planet being devoured and a living homeworld receiving its matter. No pity, frenzy or gore.",
    "QBA-05-growth": "Queen Baiqi surveys the colossal productive homeworld after many devourings from an elevated imperial balcony. Her face and shoulders are in the left foreground, with vast concentric city, research and mining districts, orbital cargo lanes and real construction on the right. The amethyst-and-gold central nexus links those districts. Arrogant and cold, an empire concentrated on one growing world.",
    "QBA-06-psionic": "The same Queen Baiqi after the civilization's legitimate psionic awakening. A deep violet cosmic Shroud surrounds her and the homeworld. Many fine points of consciousness form orderly luminous threads toward her and the amethyst heart nexus, under one overwhelming royal will. Her face and glasses remain clear at left foreground, radiant psychic structure at right. No changed species anatomy or fused bodies.",
    "QBA-07-fleet": "Queen Baiqi at the left foreground on an imperial command balcony, calmly ordering angular mineral-built crisis warships to launch from her single homeworld's orbital foundries. Legible fleets, mineral cargo and rock-rich hulls connect the homeworld economy to the next campaign. Gold and violet command lights against cold space. No wounded queen, shouting, pity or heroic benevolence.",
}


def write_json(path: Path, value: object) -> None:
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def credentials() -> None:
    if not os.environ.get("EVOLINK_API_KEY"):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            os.environ["EVOLINK_API_KEY"] = winreg.QueryValueEx(key, "EVOLINK_API_KEY")[0]


def uploaded_url(value: object) -> str | None:
    if isinstance(value, dict):
        for key in ("file_url", "url", "data", "result"):
            if key in value:
                found = uploaded_url(value[key])
                if found:
                    return found
    if isinstance(value, list):
        for item in value:
            found = uploaded_url(item)
            if found:
                return found
    if isinstance(value, str) and value.startswith("https://"):
        return value
    return None


def upload(relative: str) -> str:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    if relative in cache:
        return cache[relative]
    source = ART / relative
    with source.open("rb") as stream:
        response = requests.post(
            "https://files-api.evolink.ai/api/v1/files/upload/stream",
            headers={"Authorization": "Bearer " + os.environ["EVOLINK_API_KEY"]},
            files={"file": (source.name, stream, "image/png")}, timeout=90,
        )
    if response.status_code != 200:
        raise RuntimeError(f"Upload HTTP {response.status_code}")
    url = uploaded_url(response.json())
    if not url:
        raise RuntimeError("Upload returned no HTTPS image URL")
    cache[relative] = url
    write_json(CACHE, cache)
    return url


def prompt_for(asset: str) -> str:
    identity = (
        "Use case: illustration-story. Premium painted 2D anime science-fiction game art for Heart of Devouring. "
        "Reference image 1 is the chosen Queen Baiqi full-body outfit and stance; reference image 2 locks facial identity. "
        "Keep the same adult queen, silver-white lavender-shadowed bob and bangs, violet-pink eyes, delicate gold circular glasses, "
        "black-gold wing ornaments and sharp dark crown, black/gold imperial open coat, deep-purple rear cape and faceted amethyst heart jewel. "
        "She is evil, icily indifferent, merciless, contemptuous of alien outsiders, decisive about any sacrifice and proudly imperious. "
        "Cold half-lidded gaze, chin lifted, closed restrained mouth. No friendly smile, innocent heroine, cutesy head tilt or guilt. "
        "Precise original facial identity; no screenshot lettering, UI, watermark, extra unrelated heroine, gore or exposed biological heart. "
    )
    if asset in SCENES:
        return identity + (
            "Composition: opaque 16:9 master, designed for a panoramic 3:1 event crop. Place her entire head, face, crown, heart jewel "
            "and the scene's key action in the CENTRAL HORIZONTAL BAND between 32% and 68% of image height. "
            "Her upper-body portrait occupies the left third, scene occupies the right two-thirds. All essential narrative features "
            "must survive cropping the top and bottom. Upper and lower margins contain only expendable architecture or space. "
            "No text anywhere. " + SCENES[asset]
        )
    if asset == "QBA-08-icon":
        return (
            "Use case: stylized-concept. A single crisp origin emblem for the Stellaris mod Heart of Devouring, on a genuinely transparent background. "
            "A faceted violet amethyst heart-core tightly enclosed by an angular cold-gold broken orbital ring, swallowing a few dark planetary fragments. "
            "Obsidian, gold and deep purple, sharp imperial silhouette matching Queen Baiqi's heart jewel. Readable at 40x40 pixels, generous transparent margins. "
            "One simple emblem, no person, no scene, no letters, no border box, no glow cloud, no vignette, no flesh or biological heart. Real transparent PNG alpha."
        )
    if asset == "QBA-09-cover":
        return identity + (
            "A polished opaque square Steam Workshop cover. Queen Baiqi's head, crown and upper torso dominate the center, "
            "with a cracked rocky planet under her controlled gloved hand, a colossal single homeworld and disciplined warships behind. "
            "Keep face, gold glasses and purple heart jewel exceptionally clear at thumbnail scale. Dark obsidian/gold/violet imperial mood. "
            "The only text is the exact Chinese title 吞噬之心, elegantly typeset across the lower area, readable and accurately formed. No other lettering."
        )
    raise ValueError(asset)


def submit(asset: str) -> None:
    attempt = ART / "generated" / f"{asset}-attempt-01"
    if attempt.exists():
        print(f"{asset}: existing attempt retained; poll it", flush=True)
        return
    prompt = prompt_for(asset)
    references = REFERENCES
    payload = {
        "model": "gpt-image-2.5-sunburst", "size": "16:9" if asset in SCENES else "1:1",
        "resolution": "2K", "quality": "xhigh", "output_format": "png", "n": 1,
        "background": "transparent" if asset == "QBA-08-icon" else "opaque",
        "prompt": prompt, "image_urls": [upload(name) for name in references],
    }
    public = {key: value for key, value in payload.items() if key not in {"prompt", "image_urls"}}
    public.update(
        provider="EvoLink", endpoint="https://api.evolink.ai/v1/images/generations",
        prompt_file="original.prompt.txt", temporary_url_redaction=True,
        image_urls=[f"<temporary-upload-url:{name}>" for name in references],
        reference_fingerprints=[{"file": name, "sha256": hashlib.sha256((ART / name).read_bytes()).hexdigest()} for name in references],
    )
    attempt.mkdir(parents=True)
    (attempt / "original.prompt.txt").write_bytes((prompt + "\n").encode())
    (ART / "prompts" / f"{asset}.prompt.txt").write_bytes((prompt + "\n").encode())
    write_json(attempt / "original.request.json", public)
    result = api_request("POST", "/images/generations", payload)
    task = task_id_from(result)
    write_json(attempt / "original.task.json", {"task_id": task, "submitted_at_utc": datetime.now(timezone.utc).isoformat()})
    print(f"{asset}: submitted {task}", flush=True)


def poll() -> None:
    for attempt in sorted((ART / "generated").glob("QBA-0[3-9]-*-attempt-01")):
        if (attempt / "original.png").exists():
            continue
        task = json.loads((attempt / "original.task.json").read_text(encoding="utf-8"))["task_id"]
        result = api_request("GET", "/tasks/" + task)
        status = result.get("status")
        if status not in {"completed", "succeeded", "success"}:
            print(f"{attempt.name}: {status}, {result.get('progress')}%", flush=True)
            if status in {"failed", "error", "cancelled"}:
                write_json(attempt / "result.status.json", {"task_id": task, "status": status})
            continue
        url = find_result_url(result)
        if not url or urlsplit(url).netloc not in {"files.evolink.ai", "cdn.evolink.ai", "ark-acg-cn-beijing.tos-cn-beijing.volces.com"}:
            raise RuntimeError("Missing or unexpected image download host")
        response = requests.get(url, timeout=120)
        if response.status_code != 200 or not response.content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError("Provider output is not a downloadable PNG")
        output = attempt / "original.png"
        output.write_bytes(response.content)
        with Image.open(output) as image:
            dimensions = {"width": image.width, "height": image.height, "mode": image.mode}
        write_json(attempt / "result.status.json", {
            "task_id": task, "status": "downloaded", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(response.content).hexdigest(), "bytes": len(response.content), **dimensions,
        })
        print(f"{attempt.name}: downloaded {dimensions['width']}x{dimensions['height']}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["submit", "poll"])
    args = parser.parse_args()
    credentials()
    if args.action == "submit":
        for asset in [*SCENES, "QBA-08-icon", "QBA-09-cover"]:
            submit(asset)
    else:
        poll()
