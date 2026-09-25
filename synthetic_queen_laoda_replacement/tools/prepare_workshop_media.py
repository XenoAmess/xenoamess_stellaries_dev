"""Copy the user-supplied thumbnail and original in-game Workshop screenshots."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
THUMBNAIL_SOURCE = ROOT / "assets/reference/thumbnail-v0.1.2.png"
THUMBNAIL_SHA256 = "89269b3da6cea8a0071fbd61b285414e8e04ac69a4dcfad6545ed55399efc520"
EVIDENCE = ROOT / "evidence/portrait-acceptance-rc1"
MEDIA = ROOT / "workshop/media"
SOURCE_IMAGES = (
    ("after-restart.jpg", "01-children-returned.jpg"),
    ("cetana-dialogue.jpg", "02-first-dialogue.jpg"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sha256(THUMBNAIL_SOURCE) != THUMBNAIL_SHA256:
        raise ValueError("user-supplied thumbnail changed")
    with Image.open(THUMBNAIL_SOURCE) as source:
        if source.mode != "RGBA" or source.size != (800, 800) or source.getchannel("A").getextrema() != (255, 255):
            raise ValueError("unexpected user-supplied thumbnail format")
    thumbnail = ROOT / "mod/thumbnail.png"
    shutil.copyfile(THUMBNAIL_SOURCE, thumbnail)
    if thumbnail.stat().st_size >= 1_000_000 or sha256(thumbnail) != THUMBNAIL_SHA256:
        raise ValueError("thumbnail copy differs from user file or exceeds preview size")

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
