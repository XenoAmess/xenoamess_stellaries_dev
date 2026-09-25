"""Build a deterministic static Synthetic Queen DDS from the reviewed image."""

from __future__ import annotations

import hashlib
import struct
from pathlib import Path

from PIL import Image


MOD_ROOT = Path(__file__).resolve().parents[1]
SOURCE = MOD_ROOT / "assets/generated/cetana-portrait-opaque-v1.png"
SOURCE_SHA256 = "ED268792522A368C53F5DCF3CBF97CA346A6EE19178AF9DEC9A60CFB4395AFA2"
PREVIEW = MOD_ROOT / "assets/generated/cetana-portrait-800x350.png"
OUTPUT = MOD_ROOT / "mod/gfx/models/portraits/xenoamess_cetana_portrait.dds"
SIZE = (800, 350)


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
        if source.size != (1896, 830) or source.mode != "RGB":
            raise ValueError(f"Unexpected source layout: {source.size} {source.mode}")
        # The generation canvas matches 800:350 to within two source pixels.
        resized = source.resize(SIZE, Image.Resampling.LANCZOS)
        resized.save(PREVIEW)
        rgba = resized.convert("RGBA")
        red, green, blue, alpha = rgba.split()
        bgra = Image.merge("RGBA", (blue, green, red, alpha)).tobytes()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(dds_header(*SIZE) + bgra)
    print(f"{PREVIEW.relative_to(MOD_ROOT)} {sha256(PREVIEW)}")
    print(f"{OUTPUT.relative_to(MOD_ROOT)} {sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
