"""Compare mechanical reward mappings against the pinned vanilla trait effects."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from generate_rewards import OTHER, compatible_name


ROOT = Path(__file__).resolve().parents[2]
COMPAT = ROOT / "shishan_code_origin/mod/common/traits/shishan_code_compat.txt"
ASSIGNMENT = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(-?\d+(?:\.\d+)?)\s*$")


def block(source: str, key: str) -> str:
    start = re.search(rf"(?m)^{re.escape(key)}\s*=\s*\{{", source)
    if start is None:
        raise ValueError(f"missing trait: {key}")
    depth = 1
    for index in range(start.end(), len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start.end():index]
    raise ValueError(f"unclosed trait: {key}")


def modifiers(trait: str) -> dict[str, str]:
    match = re.search(r"(?m)^\s*modifier\s*=\s*\{", trait)
    if match is None:
        raise ValueError("trait has no modifier")
    end = trait.find("}", match.end())
    if end < 0:
        raise ValueError("unclosed modifier")
    return dict(ASSIGNMENT.findall(trait[match.end():end]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", required=True, type=Path)
    args = parser.parse_args()
    vanilla = (args.game / "common/traits/04_species_traits.txt").read_text(encoding="utf-8-sig")
    mapped = COMPAT.read_text(encoding="utf-8")
    failures = []
    for original, *_ in OTHER:
        base = block(vanilla, original)
        compat = block(mapped, compatible_name(original))
        if modifiers(base) != modifiers(compat):
            failures.append(f"{original}: modifier drift")
        if "MACHINE" not in compat or "ROBOT" not in compat:
            failures.append(f"{original}: missing machine archetype")
        if "MACHINE" in base or "ROBOT" in base:
            failures.append(f"{original}: vanilla archetype changed")
    required_keys = {key for original, *_ in OTHER for key in (original, original + "_desc")}
    for directory in sorted((args.game / "localisation").iterdir()):
        if not directory.is_dir():
            continue
        found: set[str] = set()
        for path in directory.glob(f"*_l_{directory.name}.yml"):
            with path.open("r", encoding="utf-8-sig", errors="replace") as stream:
                for line in stream:
                    key = line.partition(":")[0].strip()
                    if key in required_keys:
                        found.add(key)
        for missing in sorted(required_keys - found):
            failures.append(f"{directory.name}: missing vanilla localization {missing}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"compat traits: PASS ({len(OTHER)} vanilla effects and machine archetypes)")


if __name__ == "__main__":
    main()
