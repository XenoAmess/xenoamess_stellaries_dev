"""Audit country wide refactor output with two machine templates in one job."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_resource_source_saves import income_by_source, read_block
from audit_rs04_mixed_species import (
    MAIN_GROUP,
    MAIN_SPECIES,
    VARIANT_GROUP,
    VARIANT_SPECIES,
    check_rights,
    group,
    miner_job,
)
from audit_rs04_vanilla_bonuses import player_country, player_techs


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "before": EVIDENCE / "pr03-mixed-before-2203.10.09.sav",
    "control": EVIDENCE / "pr03-mixed-control-2203.11.09.sav",
    "refactored": EVIDENCE / "pr03-mixed-refactored-2203.11.09.sav",
}


def species_traits(game: str, species_id: int) -> list[str]:
    species_db = read_block(game, game.index("species_db="))
    match = re.search(rf"(?m)^\s*{species_id}=\s*\{{", species_db)
    if not match:
        raise ValueError(f"Missing species {species_id}")
    species = read_block(species_db, match.start())
    traits = read_block(species, species.index("traits="))
    return re.findall(r'trait="([^"]+)"', traits)


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    budget = read_block(player, player.index("budget="))
    month = read_block(budget, budget.index("current_month="))
    expenses = read_block(month, month.index("expenses="))
    physicist = re.search(r"planet_physicists=\s*\{\s*consumer_goods=([0-9.]+)", expenses)
    if not physicist:
        raise ValueError(f"Missing physicist upkeep in {path}")
    income = income_by_source(path)
    date = re.search(r'(?m)^date="([^"]+)"', game)
    if not date:
        raise ValueError(f"Missing date in {path}")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": date.group(1),
        "miner_job": miner_job(game),
        "groups": [group(game, MAIN_GROUP), group(game, VARIANT_GROUP)],
        "rights": check_rights(game),
        "vanilla_technologies": player_techs(game),
        "main_traits": species_traits(game, MAIN_SPECIES),
        "variant_traits": species_traits(game, VARIANT_SPECIES),
        "situation_count": len(re.findall(r'type="situation_shishan_code"', game)),
        "refactor_modifier_count": player.count('modifier="shishan_code_refactored_jobs"'),
        "planet_miners_minerals": income["planet_miners"]["minerals"],
        "planet_physicists_physics": income["planet_physicists"]["physics_research"],
        "physicist_consumer_goods_upkeep": float(physicist.group(1)),
        "country_base_minerals": income["country_base"]["minerals"],
        "orbital_mining_minerals": income["orbital_mining_deposits"]["minerals"],
    }


def audit() -> dict:
    results = {name: inspect(path) for name, path in SAVES.items()}
    before, control, refactored = (results[name] for name in ("before", "control", "refactored"))
    job = control["miner_job"]
    basic_miner_output = (job["workforce"] + job["bonus_workforce"]) / 100 * 4
    expected_miner_gain = basic_miner_output * 0.25
    actual_miner_gain = round(refactored["planet_miners_minerals"] - control["planet_miners_minerals"], 5)
    checks = {
        "same_settlement_date": control["date"] == refactored["date"] == "2203.11.09",
        "same_two_template_job": before["miner_job"] == control["miner_job"] == refactored["miner_job"]
        and job["assigned"] == {MAIN_GROUP: 2300, VARIANT_GROUP: 500},
        "same_groups_and_rights": before["groups"] == control["groups"] == refactored["groups"]
        and before["rights"] == control["rights"] == refactored["rights"],
        "same_vanilla_technology": before["vanilla_technologies"]
        == control["vanilla_technologies"]
        == refactored["vanilla_technologies"]
        and all(control["vanilla_technologies"].values()),
        "one_country_refactor_no_situation": control["refactor_modifier_count"] == 0
        and refactored["refactor_modifier_count"] == 1
        and control["situation_count"] == 1
        and refactored["situation_count"] == 0,
        "main_trait_switched_once": control["main_traits"].count("trait_shishan_code") == 1
        and control["main_traits"].count("trait_shishan_refactored") == 0
        and refactored["main_traits"].count("trait_shishan_code") == 0
        and refactored["main_traits"].count("trait_shishan_refactored") == 1,
        "variant_template_unchanged": control["variant_traits"] == refactored["variant_traits"],
        "whole_mixed_job_gains_once": abs(actual_miner_gain - expected_miner_gain) < 0.0001,
        "physicist_output_rises_upkeep_equal": refactored["planet_physicists_physics"]
        > control["planet_physicists_physics"]
        and refactored["physicist_consumer_goods_upkeep"]
        == control["physicist_consumer_goods_upkeep"],
        "nonjob_sources_unchanged": all(
            refactored[key] == control[key]
            for key in ("country_base_minerals", "orbital_mining_minerals")
        ),
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "expected_miner_gain": expected_miner_gain,
        "actual_miner_gain": actual_miner_gain,
        "saves": results,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
