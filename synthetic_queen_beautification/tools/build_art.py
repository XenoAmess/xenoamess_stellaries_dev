"""Build a deterministic straight-alpha Synthetic Queen DDS from the reviewed image."""

from __future__ import annotations

import hashlib
import struct
from pathlib import Path

from PIL import Image


MOD_ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    MOD_ROOT
    / "assets/generated/evolink-paid/2026-09-25/cetana-portrait-attempt-02/original.png"
)
SOURCE_SHA256 = "2DE5A76AC2974404381BE70EC7C4CA9F363F3FCEEB93E827C6FFAC261C8D5591"
PREVIEW = MOD_ROOT / "assets/generated/cetana-portrait-800x350.png"
PREVIEW_SHA256 = "5C873D7A43C725976B7315B3A4B0C50F2676CCBEF3AB4509B039BE5658CB0A9A"
OUTPUT = MOD_ROOT / "mod/gfx/models/portraits/xenoamess_cetana_portrait.dds"
SIZE = (800, 350)
CROP = (0, 0, 2736, 1197)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def dds_header(width: int, height: int) -> bytes:
    values = [
        124,
        0x0000100F,
        height,
        width,
        width * 4,
        0,
        0,
        *([0] * 11),
        32,
        0x00000041,
        0,
        32,
        0x00FF0000,
        0x0000FF00,
        0x000000FF,
        0xFF000000,
        0x00001000,
        0,
        0,
        0,
        0,
    ]
    return b"DDS " + struct.pack("<31I", *values)


def main() -> None:
    if sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError("Generated source image does not match the reviewed candidate")

    with Image.open(SOURCE) as source:
        if source.size != (2736, 1536) or source.mode != "RGBA":
            raise ValueError(f"Unexpected source layout: {source.size} {source.mode}")
        resized = source.crop(CROP).resize(SIZE, Image.Resampling.LANCZOS)
        resized.save(PREVIEW)
        if sha256(PREVIEW) != PREVIEW_SHA256:
            raise ValueError("Transparent preview does not match the reviewed candidate")
        red, green, blue, alpha = resized.split()
        if alpha.getextrema() != (0, 255) or any(
            alpha.getpixel(point) != 0
            for point in ((0, 0), (SIZE[0] - 1, 0), (0, SIZE[1] - 1), (SIZE[0] - 1, SIZE[1] - 1))
        ):
            raise ValueError("Generated source lost transparent corners")
        bgra = Image.merge("RGBA", (blue, green, red, alpha)).tobytes()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(dds_header(*SIZE) + bgra)
    print(f"{PREVIEW.relative_to(MOD_ROOT)} {sha256(PREVIEW)}")
    print(f"{OUTPUT.relative_to(MOD_ROOT)} {sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
