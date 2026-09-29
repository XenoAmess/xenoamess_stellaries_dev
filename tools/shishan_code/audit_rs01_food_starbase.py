"""Audit native hydroponics-bay food income in one formal Mod campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from audit_pr04_natural_relapse import inspect
from audit_resource_source_saves import income_by_source, read_block
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "anchor_I": EVIDENCE / "rs01-food-anchor-2230.10.17.sav",
    "II": EVIDENCE / "rs01-food-stage2-2230.11.01.sav",
    "V": EVIDENCE / "rs01-food-stage5-2230.11.01.sav",
}
EXPECTED_FOOD = {"anchor_I": 12.5, "II": 10.0, "V": 2.5}


def audit() -> dict:
    details = {}
    for stage, path in SAVES.items():
        with zipfile.ZipFile(path) as archive:
            game = archive.read("gamestate").decode("utf-8-sig")
        country = player_country(game)
        starbase_manager = read_block(game, game.index("\nstarbase_mgr="))
        starbases = read_block(starbase_manager, starbase_manager.index("starbases="))
        capital_starbase = read_block(starbases, starbases.index("0="))
        buildings = read_block(capital_starbase, capital_starbase.index("buildings="))
        state = inspect(path)
        sources = income_by_source(path)
        details[stage] = {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "date": state["date"],
            "situation_count": state["situation_count"],
            "situation_progress": state["situation_progress"],
            "maintenance_count": state["maintenance_count"],
            "main_traits": state["main_traits"],
            "origin": "origin_shishan_code" in country,
            "hydroponics_tech": 'technology="tech_hydroponics"' in country,
            "capital_starbase_level": "starbase_level_starhold" in capital_starbase,
            "capital_hydroponics_bays": buildings.count("hydroponics_bay"),
            "food_sources": {
                source: values["food"]
                for source, values in sources.items()
                if "food" in values
            },
            "fixture_refs": game.count("shishan_test_society_boost"),
        }

    checks = {
        "formal_origin_and_vanilla_tech": all(
            item["origin"] and item["hydroponics_tech"]
            for item in details.values()
        ),
        "one_built_bay_each": all(
            item["capital_starbase_level"] and item["capital_hydroponics_bays"] == 1
            for item in details.values()
        ),
        "same_founder_traits_and_maintenance": all(
            item["main_traits"] == details["anchor_I"]["main_traits"]
            and item["maintenance_count"] == 3
            for item in details.values()
        ),
        "situation_stage_progress": (
            details["anchor_I"]["situation_count"] == 1
            and 0 <= details["anchor_I"]["situation_progress"] < 250
            and details["II"]["situation_count"] == 1
            and 250 <= details["II"]["situation_progress"] < 500
            and details["V"]["situation_count"] == 1
            and details["V"]["situation_progress"] == 1000
        ),
        "same_monthly_settlement_date": (
            details["anchor_I"]["date"] == "2230.10.17"
            and details["II"]["date"] == details["V"]["date"] == "2230.11.01"
        ),
        "food_only_from_one_starbase_bay": all(
            item["food_sources"] == {"starbase_buildings": EXPECTED_FOOD[stage]}
            for stage, item in details.items()
        ),
        "no_fixture_references": all(item["fixture_refs"] == 0 for item in details.values()),
    }
    return {"pass": all(checks.values()), "checks": checks, "details": details}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
