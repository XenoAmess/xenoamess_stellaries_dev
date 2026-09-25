"""Prepare the launcher thumbnail and original in-game Workshop screenshots."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PORTRAIT = ROOT / "assets/generated/laoda-portrait-800x350.png"
EVIDENCE = ROOT / "evidence/portrait-acceptance-rc1"
MEDIA = ROOT / "workshop/media"
SOURCE_IMAGES = (
    ("after-restart.jpg", "01-children-returned.jpg"),
    ("cetana-dialogue.jpg", "02-first-dialogue.jpg"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with Image.open(PORTRAIT) as source:
        if source.mode != "RGBA" or source.size != (800, 350):
            raise ValueError("accepted portrait image changed")
        crop = source.crop((200, 0, 600, 350)).resize((351, 313), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (351, 313), (13, 18, 27, 255))
    canvas.alpha_composite(crop)
    thumbnail = ROOT / "mod/thumbnail.png"
    canvas.convert("RGB").save(thumbnail, format="PNG", optimize=True)
    if thumbnail.stat().st_size >= 1_000_000:
        raise ValueError("launcher thumbnail exceeds Workshop preview size")

    MEDIA.mkdir(parents=True, exist_ok=True)
    for source_name, output_name in SOURCE_IMAGES:
        original = EVIDENCE / source_name
        destination = MEDIA / output_name
        with Image.open(original) as source:
            if source.size != (2560, 1440) or source.format != "JPEG":
                raise ValueError(f"unexpected Steam F12 screenshot: {original}")
        shutil.copyfile(original, destination)
        if destination.stat().st_size >= 1_000_000 or sha256(original) != sha256(destination):
            raise ValueError(f"screenshot copy differs from accepted evidence: {original}")
        print(f"{destination.relative_to(ROOT)} {sha256(destination)}")
    print(f"{thumbnail.relative_to(ROOT)} {sha256(thumbnail)}")


if __name__ == "__main__":
    main()
