"""Audit one situation adjustment with vanilla job and mining-station technologies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_resource_source_saves import income_by_source, read_block
from audit_rs04_mixed_species import EVIDENCE, ROOT, SAVES as CONTROL_SAVES, field, miner_job, require, snapshot


TECHS = ("tech_synthetic_thought_patterns", "tech_space_mining_1")
ANCHOR = EVIDENCE / "rs04-tech-anchor-2203.09.24.sav"
SAVES = {stage: EVIDENCE / f"rs04-tech-stage{stage}-2203.10.08.sav" for stage in (1, 3, 5)}


def game_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("gamestate").decode("utf-8-sig")


def player_techs(game: str) -> dict[str, bool]:
    player = player_country(game)
    return {tech: f'technology="{tech}"' in player for tech in TECHS}


def player_country(game: str) -> str:
    countries = read_block(game, game.index("\ncountry="))
    return read_block(countries, countries.index("0="))


def source(path: Path) -> dict[str, float]:
    income = income_by_source(path)
    return {
        "job_minerals": income["planet_miners"]["minerals"],
        "station_minerals": income["orbital_mining_deposits"]["minerals"],
        "station_energy": income["orbital_mining_deposits"]["energy"],
    }


def research_points(path: Path) -> dict[str, float]:
    income = income_by_source(path)
    return {
        key: income[key]["engineering_research"]
        for key in ("country_base", "orbital_research_deposits", "planet_engineers")
    }


def close(actual: float, expected: float, reason: str) -> None:
    require(abs(actual - expected) <= 0.0001, f"{reason}: {actual} != {expected}")


def modifier_value(block: str, key: str) -> float:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(-?\d+(?:\.\d+)?)", block)
    require(match is not None, f"modifier {key} missing")
    return float(match.group(1))


def audit() -> dict:
    anchor_game = game_text(ANCHOR)
    require(field(anchor_game, "date") == "2203.09.24", "wrong technology anchor date")
    require(all(player_techs(anchor_game).values()), "technology missing from player anchor")
    anchor_job = miner_job(anchor_game)
    require(anchor_job["assigned"] == {14: 2300, 50331648: 500}, "technology anchor miner assignment changed")
    require(anchor_job["bonus_workforce"] == 280, "technology anchor bonus workforce changed")
    modifier_text = (ROOT / "shishan_code_origin" / "mod" / "common" / "static_modifiers" / "shishan_code_stages.txt").read_text(encoding="utf-8")
    vivhite_speed = read_block(modifier_text, modifier_text.index("shishan_code_vivhite_base ="))
    close(modifier_value(vivhite_speed, "country_engineering_tech_research_speed"), 0.10, "Vivhite engineering research speed")
    close(modifier_value(vivhite_speed, "country_society_tech_research_speed"), -0.05, "Vivhite society research speed")

    stages = {}
    for stage, path in SAVES.items():
        row = snapshot(stage, path)
        require(row["date"] == "2203.10.08", f"stage {stage} date differs")
        game = game_text(path)
        player = player_country(game)
        require(all(player_techs(game).values()), f"stage {stage} lost a vanilla technology")
        require(not any(player_techs(game_text(CONTROL_SAVES[stage])).values()), "control save has technology")
        require(player.count('modifier="shishan_code_vivhite_base"') == 1, f"stage {stage} Vivhite speed modifier missing or doubled")
        close(float(field(player, "shishan_code_maintenance_count")), 0, f"stage {stage} maintenance count")
        row["income"] = source(path)
        row["engineering_research_point_sources"] = research_points(path)
        control = source(CONTROL_SAVES[stage])
        row["control_income"] = control
        row["technology_gain"] = {
            key: round(row["income"][key] - control[key], 5) for key in row["income"]
        }
        close(row["technology_gain"]["job_minerals"], 123.2 * 0.025, "vanilla job technology gain")
        for key in ("station_minerals", "station_energy"):
            close(row["technology_gain"][key], 10 * 0.10, f"vanilla {key} technology gain")
        stages[str(stage)] = row

    gaps = {}
    for key, expected in (("job_minerals", 123.2 * 0.5), ("station_minerals", 10 * 0.5), ("station_energy", 10 * 0.5)):
        first = round(stages["1"]["income"][key] - stages["3"]["income"][key], 5)
        second = round(stages["3"]["income"][key] - stages["5"]["income"][key], 5)
        close(first, expected, f"{key} I-to-III adjustment")
        close(second, expected, f"{key} III-to-V adjustment")
        gaps[key] = [first, second]

    research_gaps = {}
    for key, expected in (("country_base", 5.0), ("orbital_research_deposits", 1.5), ("planet_engineers", 1.98)):
        first = round(stages["1"]["engineering_research_point_sources"][key] - stages["3"]["engineering_research_point_sources"][key], 5)
        second = round(stages["3"]["engineering_research_point_sources"][key] - stages["5"]["engineering_research_point_sources"][key], 5)
        close(first, expected, f"{key} engineering research-point I-to-III adjustment")
        close(second, expected, f"{key} engineering research-point III-to-V adjustment")
        research_gaps[key] = [first, second]

    return {
        "status": "PASS",
        "method": "Vanilla technology anchor plus independent I/III/V branches on 2203.10.08; no-technology controls are 2203.10.06 with identical miner assignments.",
        "technologies": list(TECHS),
        "anchor": {"path": str(ANCHOR.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(ANCHOR.read_bytes()).hexdigest()},
        "stages": stages,
        "stage_gaps": gaps,
        "engineering_research_point_gaps": research_gaps,
        "vivhite_research_speed": {"engineering": 0.10, "society": -0.05},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'{result["status"]}: stage gaps {result["stage_gaps"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
