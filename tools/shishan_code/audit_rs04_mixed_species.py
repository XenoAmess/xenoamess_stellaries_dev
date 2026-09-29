"""Verify one situation resource adjustment across two working machine templates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_resource_source_saves import income_by_source, read_block


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {stage: EVIDENCE / f"rs04-mixed-stage{stage}-2203.10.06.sav" for stage in (1, 3, 5)}
MAIN_GROUP = 14
VARIANT_GROUP = 50331648
MAIN_SPECIES = 3321888769
VARIANT_SPECIES = 48
NUMBER = r"-?\d+(?:\.\d+)?"


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise AssertionError(reason)


def field(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}=(\S+)", text)
    require(match is not None, f"missing {key}")
    return match.group(1).strip('"')


def group(game: str, group_id: int) -> dict:
    pop_groups = read_block(game, game.index("pop_groups="))
    match = re.search(rf"(?m)^\s*{group_id}=\s*\{{", pop_groups)
    require(match is not None, f"missing pop group {group_id}")
    block = read_block(pop_groups, match.start())
    return {
        "id": group_id,
        "species": int(field(block, "species")),
        "size": int(field(block, "size")),
        "worker_eligible": "can_fill_worker_job=yes" in block,
        "planet": int(field(block, "planet")),
    }


def miner_job(game: str) -> dict:
    for match in re.finditer(r'(?m)^\s*type="miner"', game):
        # The job is a nested object, whose closing brace follows planet=0.
        nearby = game[match.start() : match.start() + 1400]
        assignment = re.search(r"pop_groups=\s*\{(.*?)\}\s*planet=(\d+)", nearby, re.S)
        if assignment and assignment.group(2) == "0":
            return {
                "workforce": int(field(nearby, "workforce")),
                "bonus_workforce": int(field(nearby, "bonus_workforce")),
                "assigned": {
                    int(group_id): int(amount)
                    for group_id, amount in re.findall(r"pop_group=(\d+)\s+amount=(\d+)", assignment.group(1))
                },
            }
    raise AssertionError("missing capital miner job")


def check_rights(game: str) -> dict:
    module = read_block(game, game.index("standard_species_rights_module="))
    primary = read_block(module, module.index("primary="))
    require(int(field(primary, "species_index")) == MAIN_SPECIES, "unexpected main species")
    require(field(primary, "citizenship") == "citizenship_full", "main species cannot work")
    rights = read_block(module, module.index("species_rights="))
    match = re.search(rf"species_index={VARIANT_SPECIES}\b", rights)
    require(match is not None, "variant has no explicit rights")
    variant = rights[match.start() : match.start() + 700]
    require(field(variant, "citizenship") == "citizenship_full", "variant is not a citizen")
    require(field(variant, "living_standard") != "living_standard_tech_assimilation", "variant is assimilating")
    species_db = read_block(game, game.index("species_db="))
    variant_match = re.search(rf"(?m)^\s*{VARIANT_SPECIES}=\s*\{{", species_db)
    require(variant_match is not None, "variant species missing")
    species = read_block(species_db, variant_match.start())
    require(int(field(species, "base_ref")) == MAIN_SPECIES, "variant is not a main-species template")
    require('trait="trait_robot_learning_algorithms"' in species, "variant test trait missing")
    return {"main": MAIN_SPECIES, "variant": VARIANT_SPECIES, "variant_citizenship": "citizenship_full"}


def snapshot(stage: int, path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    progress_match = re.search(r'type="situation_shishan_code"\s+progress=(' + NUMBER + r")", game)
    require(progress_match is not None, "situation missing")
    main = group(game, MAIN_GROUP)
    variant = group(game, VARIANT_GROUP)
    require(main["species"] == MAIN_SPECIES and variant["species"] == VARIANT_SPECIES, "group species mismatch")
    require(main["planet"] == variant["planet"] == 0, "groups are on different planets")
    require(main["worker_eligible"] and variant["worker_eligible"], "one template cannot work")
    require(variant["size"] == 500, "variant population changed")
    job = miner_job(game)
    require(job["assigned"] == {MAIN_GROUP: 2300, VARIANT_GROUP: 500}, "miner assignment changed")
    require(job["workforce"] == 2800 and job["bonus_workforce"] == 280, "effective workforce changed")
    progress = float(progress_match.group(1))
    require({1: 0, 3: 500, 5: 950}[stage] <= progress < {1: 250, 3: 750, 5: 10000}[stage], "wrong situation stage")
    income = income_by_source(path)
    minerals = income.get("planet_miners", {}).get("minerals")
    require(minerals is not None, "miner mineral income missing")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": field(game, "date"),
        "progress": progress,
        "groups": [main, variant],
        "rights": check_rights(game),
        "miner_job": job,
        "planet_miners_minerals": minerals,
    }


def audit() -> dict:
    data = {str(stage): snapshot(stage, path) for stage, path in SAVES.items()}
    require({item["date"] for item in data.values()} == {"2203.10.06"}, "branches have different dates")
    amounts = [data[str(stage)]["planet_miners_minerals"] for stage in (1, 3, 5)]
    gaps = [round(amounts[0] - amounts[1], 5), round(amounts[1] - amounts[2], 5)]
    neutral_base = (2800 + 280) / 100 * 4
    expected_gap = neutral_base * 0.5
    require(all(abs(gap - expected_gap) < 0.0001 for gap in gaps), "stage gain differs from one base adjustment")
    return {
        "status": "PASS",
        "stages": data,
        "income_gaps": gaps,
        "vanilla_miner_base": neutral_base,
        "expected_single_adjustment_gap": expected_gap,
        "method": "Three independent runtime branches from one mixed-template save, each settled on 2203.10.06.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'{result["status"]}: gaps {result["income_gaps"]}, expected {result["expected_single_adjustment_gap"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
