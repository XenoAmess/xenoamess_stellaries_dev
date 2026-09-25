"""Reproducibly prepare the Workshop thumbnail and JPEGs from accepted art."""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ART = ROOT / "assets/generated/evolink-paid/2026-09-25/cetana-portrait-attempt-02/candidate-800x350.png"
EVIDENCE = ROOT / "evidence/portrait-acceptance-rc2"
MEDIA = ROOT / "workshop/media"
SCREENSHOTS = (
    ("rc2-cetana-dialogue.png", "01-dialogue.jpg"),
    ("rc2-cetana-second-response.png", "02-second-response.jpg"),
    ("rc2-after-restart.png", "03-after-restart.jpg"),
)


def main() -> None:
    art = Image.open(SOURCE_ART)
    if art.mode != "RGBA" or art.size != (800, 350):
        raise ValueError("accepted portrait source changed")

    # The accepted subject occupies the central 400 px, including the crown.
    crop = art.crop((200, 0, 600, 350)).resize((351, 313), Image.Resampling.LANCZOS)
    background = Image.new("RGBA", (351, 313), (13, 18, 27, 255))
    background.alpha_composite(crop)
    thumbnail = ROOT / "mod/thumbnail.png"
    background.convert("RGB").save(thumbnail, format="PNG", optimize=True)
    print(f"{thumbnail}: {thumbnail.stat().st_size} bytes")

    MEDIA.mkdir(parents=True, exist_ok=True)
    for source_name, output_name in SCREENSHOTS:
        source = Image.open(EVIDENCE / source_name)
        if source.size != (2560, 1440):
            raise ValueError(f"unexpected screenshot size: {source_name} {source.size}")
        output = MEDIA / output_name
        source.convert("RGB").save(output, format="JPEG", quality=80, optimize=True)
        if output.stat().st_size >= 1_000_000:
            raise ValueError(f"Steam preview limit exceeded: {output}")
        print(f"{output}: {output.stat().st_size} bytes")


if __name__ == "__main__":
    main()
