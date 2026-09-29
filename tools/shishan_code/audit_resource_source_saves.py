"""Audit stage resource income by economic source in archived Stellaris saves."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "I": EVIDENCE / "resource-mixed-stage1-2207.12.05.sav",
    "II": EVIDENCE / "power-projection-stage2-2207.11.05.sav",
    "III": EVIDENCE / "resource-mixed-stage3-2207.12.05.sav",
    "V": EVIDENCE / "resource-mixed-stage5-2207.12.05.sav",
}
STABLE_CATEGORIES = {
    "country_base",
    "country_power_projection",
    "orbital_mining_deposits",
    "orbital_research_deposits",
    "starbase_modules",
}
NUMBER = re.compile(r"(?m)^\s*([a-z_]+)=(-?\d+(?:\.\d+)?)\s*$")
CATEGORY = re.compile(r"(?m)^\s*([a-z_]+)=\s*\{")


def read_block(text: str, offset: int) -> str:
    opening = text.find("{", offset)
    if opening < 0:
        raise ValueError("No opening brace")
    depth = 0
    for position in range(opening, len(text)):
        if text[position] == "{":
            depth += 1
        elif text[position] == "}":
            depth -= 1
            if depth == 0:
                return text[opening + 1 : position]
    raise ValueError("Unclosed block")


def income_by_source(path: Path) -> dict[str, dict[str, float]]:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    # These archived saves have the player country as the first budget owner.
    budget = read_block(game, game.index("budget="))
    month = read_block(budget, budget.index("current_month="))
    income = read_block(month, month.index("income="))
    sources = {}
    for match in CATEGORY.finditer(income):
        values = {key: float(value) for key, value in NUMBER.findall(read_block(income, match.start()))}
        if values:
            sources[match.group(1)] = values
    return sources


def audit() -> dict:
    data = {stage: income_by_source(path) for stage, path in SAVES.items()}
    keys = sorted(
        set.intersection(
            *(
                {(source, resource) for source, resources in data[stage].items() for resource in resources}
                for stage in ("I", "III", "V")
            )
        )
    )
    entries = []
    for source, resource in keys:
        values = {stage: data[stage].get(source, {}).get(resource) for stage in SAVES}
        first_gap = round(values["I"] - values["III"], 5)
        second_gap = round(values["III"] - values["V"], 5)
        equal_gaps = abs(first_gap - second_gap) <= 0.0001
        stable_ratio = None
        if source in STABLE_CATEGORIES and values["II"]:
            stable_ratio = all(
                abs(values[stage] - values["II"] * factor) <= 0.0001
                for stage, factor in (("I", 1.25), ("III", 0.75), ("V", 0.25))
            )
        entries.append(
            {
                "source": source,
                "resource": resource,
                "income": values,
                "gap_I_to_III": first_gap,
                "gap_III_to_V": second_gap,
                "equal_gaps": equal_gaps,
                "stable_base_ratio": stable_ratio,
            }
        )
    return {
        "input_saves": {
            stage: {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for stage, path in SAVES.items()
        },
        "method": "I/III/V share the same 2207.12.05 month; II is a prior-month reference only.",
        "source_resource_count": len(entries),
        "equal_gap_count": sum(entry["equal_gaps"] for entry in entries),
        "stable_base_count": sum(entry["stable_base_ratio"] is True for entry in entries),
        "stable_base_failed": [
            f'{entry["source"]}.{entry["resource"]}'
            for entry in entries
            if entry["stable_base_ratio"] is False
        ],
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write full JSON audit to this path")
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f'{result["equal_gap_count"]}/{result["source_resource_count"]} equal stage gaps; '
        f'{result["stable_base_count"]} stable sources match II base; '
        f'{len(result["stable_base_failed"])} stable failures'
    )
    return 0 if result["equal_gap_count"] == result["source_resource_count"] and not result["stable_base_failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
