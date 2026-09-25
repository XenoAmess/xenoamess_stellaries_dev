"""Build the Laoda portrait from original RGB and EvoLink-generated alpha."""

from __future__ import annotations

import hashlib
import struct
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


MOD_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = MOD_ROOT / "assets/reference/laoda-reference.jpg"
REFERENCE_SHA256 = "872d656b3af25b3952321f5e7976acd7df205a662d387db7cd7b39ed29f138d2"
LAYER = MOD_ROOT / "assets/generated/evolink-paid/2026-09-25/laoda-layerize-attempt-01/layer-01.png"
LAYER_SHA256 = "c46511f05e2e62b87cd2a5a5c9bc1cde6d880422393b6cd9670f49063dda6f74"
CUTOUT = MOD_ROOT / "assets/generated/laoda-cutout-720x900.png"
PREVIEW = MOD_ROOT / "assets/generated/laoda-portrait-800x350.png"
OUTPUT = MOD_ROOT / "mod/gfx/models/portraits/xenoamess_cetana_laoda_portrait.dds"
LAYER_BASE_SIZE = (832, 1248)
LAYER_OFFSET = (0, 43)
CROP_HEIGHT = 900
SIZE = (800, 350)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def clean_edge_rgb(reference: Image.Image, alpha: Image.Image) -> Image.Image:
    """Replace JPEG blue spill only near the service-generated silhouette edge."""
    rgb = np.asarray(reference).copy()
    alpha_pixels = np.asarray(alpha)
    opaque = (alpha_pixels > 127).astype(np.uint8)
    interior = cv2.erode(opaque, np.ones((11, 11), dtype=np.uint8))
    if not interior.any():
        raise ValueError("EvoLink alpha has no stable person interior")
    distance_input = np.where(interior != 0, 0, 1).astype(np.uint8)
    _, labels = cv2.distanceTransformWithLabels(
        distance_input, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL
    )
    source_colors = np.zeros((int(labels.max()) + 1, 3), dtype=np.uint8)
    source_colors[labels[interior != 0]] = rgb[interior != 0]
    edge = (alpha_pixels > 0) & (interior == 0)
    if np.any(labels[edge] == 0):
        raise ValueError("EvoLink edge has no nearest subject pixel")
    rgb[edge] = source_colors[labels[edge]]
    if not np.array_equal(rgb[500:700, 220:510], np.asarray(reference)[500:700, 220:510]):
        raise ValueError("The original 冰红茶 advertisement was modified")
    return Image.fromarray(rgb, "RGB")


def main() -> None:
    if sha256(REFERENCE) != REFERENCE_SHA256 or sha256(LAYER) != LAYER_SHA256:
        raise ValueError("Reference or EvoLink layer differs from reviewed source")

    with Image.open(REFERENCE) as image:
        reference = image.convert("RGB")
    with Image.open(LAYER) as image:
        layer = image.convert("RGBA")
    if reference.size != (720, 1078) or layer.size != (832, 1205):
        raise ValueError("Unexpected reference or layer dimensions")

    layer_alpha = Image.new("L", LAYER_BASE_SIZE, 0)
    layer_alpha.paste(layer.getchannel("A"), LAYER_OFFSET)
    original_alpha = layer_alpha.resize(reference.size, Image.Resampling.LANCZOS)
    reference_crop = reference.crop((0, 0, reference.width, CROP_HEIGHT))
    alpha_crop = original_alpha.crop((0, 0, 720, CROP_HEIGHT))
    cleaned_rgb = clean_edge_rgb(reference_crop, alpha_crop)
    cutout = Image.merge("RGBA", (*cleaned_rgb.split(), alpha_crop))
    CUTOUT.parent.mkdir(parents=True, exist_ok=True)
    cutout.save(CUTOUT)
    with Image.open(CUTOUT) as reloaded:
        if not np.array_equal(
            np.asarray(reloaded.convert("RGB"))[500:700, 220:510],
            np.asarray(reference_crop)[500:700, 220:510],
        ):
            raise ValueError("Cutout altered original advertisement pixels")

    figure_width = round(reference.width * SIZE[1] / CROP_HEIGHT)
    figure = cutout.resize((figure_width, SIZE[1]), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(figure, ((SIZE[0] - figure_width) // 2, 0))
    canvas.save(PREVIEW)

    alpha = canvas.getchannel("A")
    if alpha.getextrema() != (0, 255) or any(
        alpha.getpixel(point) != 0
        for point in ((0, 0), (SIZE[0] - 1, 0), (0, SIZE[1] - 1), (SIZE[0] - 1, SIZE[1] - 1))
    ):
        raise ValueError("Transparent canvas validation failed")

    red, green, blue, alpha = canvas.split()
    bgra = Image.merge("RGBA", (blue, green, red, alpha)).tobytes()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(dds_header(*SIZE) + bgra)
    with Image.open(OUTPUT) as dds:
        if dds.convert("RGBA").tobytes() != canvas.tobytes():
            raise ValueError("DDS differs from preview pixels")
    for path in (CUTOUT, PREVIEW, OUTPUT):
        print(f"{path.relative_to(MOD_ROOT)} {sha256(path)}")


if __name__ == "__main__":
    main()
