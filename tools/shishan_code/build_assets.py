"""Build Stellaris DDS assets from the archived Shishan Code source images."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "assets" / "shishan-code-origin" / "generated"
MOD = ROOT / "shishan_code_origin" / "mod"


ASSETS = (
    ("A01-layerize-01/layer-01.png", "gfx/interface/icons/origins/origin_shishan_code.dds", (40, 40), True),
    ("A02-attempt-01/original.png", "gfx/event_pictures/origins/shishan_origin.dds", (220, 115), False),
    ("A03-layerize-01/layer-01.png", "gfx/interface/icons/traits/trait_shishan_code.dds", (29, 29), True),
    ("A04-layerize-01/layer-01.png", "gfx/interface/icons/traits/trait_shishan_refactored.dds", (29, 29), True),
    ("A05-attempt-02/original.png", "gfx/event_pictures/shishan_event.dds", (450, 150), False),
    ("A06-layerize-01/layer-01.png", "gfx/interface/icons/situation_log/shishan_maintain.dds", (39, 39), True),
    ("A07-layerize-01/layer-01.png", "gfx/interface/icons/situation_log/shishan_clean.dds", (39, 39), True),
    ("A08-layerize-01/layer-01.png", "gfx/interface/icons/buildings/building_shishan_code_institute.dds", (78, 78), True),
    ("A09-layerize-01/layer-01.png", "gfx/interface/icons/jobs/job_shishan_code_maintainer.dds", (30, 30), True),
    ("A09-layerize-01/layer-01.png", "gfx/interface/icons/modifiers/mod_job_shishan_code_maintainer_add.dds", (30, 30), True),
    ("A09-layerize-01/layer-01.png", "gfx/interface/icons/modifiers/mod_job_shishan_code_maintainer_drone_add.dds", (30, 30), True),
    ("A10-layerize-03/layer-01.png", "gfx/models/portraits/shishan_code/vivhite.dds", (512, 384), True),
    ("A11-layerize-01/layer-01.png", "gfx/interface/icons/traits/leader_trait_icons/shishan_code_vivhite.dds", (29, 29), True),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(source: Path, target: Path, size: tuple[int, int], transparent: bool) -> None:
    with Image.open(source) as original:
        image = original.convert("RGBA")
        if target.name == "vivhite.dds":
            image = image.crop((0, 0, image.width, round(image.height * 0.62)))
        if transparent:
            bounds = image.getbbox()
            if bounds:
                image = image.crop(bounds)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", size, (0, 0, 0, 0))
            canvas.alpha_composite(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
        else:
            ratio = max(size[0] / image.width, size[1] / image.height)
            image = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
            x = (image.width - size[0]) // 2
            y = (image.height - size[1]) // 2
            canvas = image.crop((x, y, x + size[0], y + size[1]))
        target.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(target, format="DDS", pixel_format="DXT5")


def main() -> None:
    manifest: list[dict[str, object]] = []
    for source_name, output_name, size, transparent in ASSETS:
        source = SOURCES / source_name
        output = MOD / output_name
        render(source, output, size, transparent)
        with Image.open(output) as check:
            if check.size != size:
                raise RuntimeError(f"bad DDS size: {output}")
        manifest.append({
            "source": str(source.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": sha256(source),
            "output": str(output.relative_to(ROOT)).replace("\\", "/"),
            "output_sha256": sha256(output),
            "size": list(size),
            "transparent": transparent,
        })
    cover = SOURCES / "A12-attempt-01" / "original.png"
    with Image.open(cover) as image:
        image.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS).save(MOD / "thumbnail.png")
    manifest.append({
        "source": str(cover.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha256(cover),
        "output": str((MOD / "thumbnail.png").relative_to(ROOT)).replace("\\", "/"),
        "output_sha256": sha256(MOD / "thumbnail.png"),
        "size": [512, 512],
        "transparent": False,
    })
    (MOD / "asset-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
