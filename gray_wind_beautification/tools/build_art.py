"""Build deterministic legacy BGRA8 DDS files for the standalone Gray Wind mod."""

from __future__ import annotations

import hashlib
import shutil
import struct
from pathlib import Path

from PIL import Image


DIST_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = DIST_ROOT.parent
MOD_ROOT = DIST_ROOT / "mod"

SOURCES = {
    "portrait": (
        REPO_ROOT
        / "assets/workshop-2976454692/generated/evolink-paid/2026-09-13"
        / "gray-portrait-attempt-03/candidate-800x350.png",
        "BEE88ED2DD5C9A7330777BE807D1D8310F514A3A6D2B19ABACDB1B1FD3490C4C",
        MOD_ROOT / "gfx/models/portraits/xenoamess_gray_wind_portrait.dds",
        (800, 350),
    ),
    "first_contact": (
        REPO_ROOT
        / "assets/workshop-2976454692/generated/codex-native/2026-09-13"
        / "gray-first-contact-attempt-01/candidate-450x150.png",
        "753AC24D2365207F1069D5A4F5DE0A3BDC079BAD5268A23CCF3C51F8E81450F5",
        MOD_ROOT / "gfx/event_pictures/xenoamess_gray_wind_first_contact.dds",
        (450, 150),
    ),
    "defeated": (
        REPO_ROOT
        / "assets/workshop-2976454692/generated/codex-native/2026-09-13"
        / "gray-defeated-attempt-01/candidate-450x150.png",
        "BEC4C7EA74D1D2CC0B79366EB2138E3CC285EB7A5596269AADE1CF4C269C2024",
        MOD_ROOT / "gfx/event_pictures/xenoamess_gray_wind_defeated.dds",
        (450, 150),
    ),
    "return": (
        REPO_ROOT
        / "assets/workshop-2976454692/generated/codex-native/2026-09-13"
        / "gray-return-attempt-01/candidate-450x150.png",
        "155747F3C5CE49D17DB1149728E650B97CB01D8053976FC3ACF81D6ACC82E9A4",
        MOD_ROOT / "gfx/event_pictures/xenoamess_gray_wind_return.dds",
        (450, 150),
    ),
}

THUMBNAIL_SOURCE = (
    REPO_ROOT
    / "assets/workshop-2976454692/generated/codex-native/2026-09-13"
    / "gray-thumbnail-attempt-01/candidate-351x313.png"
)
THUMBNAIL_SHA256 = "BAACCACA753870319B003A1ED86E733A935EEA3BD4D3C5B7EDA21D6B25902A2C"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def dds_header(width: int, height: int) -> bytes:
    # DDS_HEADER + DDS_PIXELFORMAT for a top-down, uncompressed BGRA8 texture.
    values = [
        124,
        0x0000100F,  # CAPS | HEIGHT | WIDTH | PITCH | PIXELFORMAT
        height,
        width,
        width * 4,
        0,
        0,
        *([0] * 11),
        32,
        0x00000041,  # RGB | ALPHAPIXELS
        0,
        32,
        0x00FF0000,
        0x0000FF00,
        0x000000FF,
        0xFF000000,
        0x00001000,  # DDSCAPS_TEXTURE
        0,
        0,
        0,
        0,
    ]
    header = struct.pack("<31I", *values)
    assert len(header) == 124
    return b"DDS " + header


def build_dds(source: Path, expected_sha: str, output: Path, size: tuple[int, int]) -> None:
    actual_sha = sha256(source)
    if actual_sha != expected_sha:
        raise ValueError(f"Unexpected source hash for {source}: {actual_sha}")
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        if rgba.size != size:
            raise ValueError(f"Unexpected dimensions for {source}: {rgba.size}")
        red, green, blue, alpha = rgba.split()
        bgra = Image.merge("RGBA", (blue, green, red, alpha)).tobytes()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(dds_header(*size) + bgra)


def main() -> None:
    for source, expected_sha, output, size in SOURCES.values():
        build_dds(source, expected_sha, output, size)
        print(f"built {output.relative_to(REPO_ROOT)} {sha256(output)}")

    if sha256(THUMBNAIL_SOURCE) != THUMBNAIL_SHA256:
        raise ValueError("Unexpected thumbnail source hash")
    thumbnail_output = MOD_ROOT / "thumbnail.png"
    shutil.copyfile(THUMBNAIL_SOURCE, thumbnail_output)
    print(f"copied {thumbnail_output.relative_to(REPO_ROOT)} {sha256(thumbnail_output)}")


if __name__ == "__main__":
    main()
