"""Compare an active first-stage save with its same-day in-game reload."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr02_dual_queue import queue
from audit_pr04_natural_relapse import inspect
from audit_resource_source_saves import income_by_source, read_block


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
BEFORE = EVIDENCE / "rs01-food-anchor-2230.10.17.sav"
AFTER = EVIDENCE / "sv01-stage1-reloaded-2230.10.17.sav"
STATE_FIELDS = (
    "date",
    "maintenance_count",
    "last_completed_project",
    "projects",
    "main_traits",
    "situation_count",
    "situation_progress",
    "refactored_job_modifiers",
    "vivhite_base_modifiers",
    "vivhite_engineering_layers",
    "vivhite_society_layers",
    "temporary_boost_refs",
)


def game_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("gamestate").decode("utf-8-sig")


def vivhite(game: str) -> dict:
    trait = "leader_trait_shishan_code_vivhite"
    position = game.index(trait)
    leaders = list(re.finditer(r"(?m)^\t(\d+)=\s*\{", game[:position]))
    match = leaders[-1]
    block = read_block(game, match.start())
    if block.count(trait) != 1 or "shishan_code_vivhite" not in block:
        raise ValueError("The matched leader is not Vivhite")
    return {"id": int(match.group(1)), "block_sha256": hashlib.sha256(block.encode()).hexdigest()}


def audit() -> dict:
    before, after = inspect(BEFORE), inspect(AFTER)
    before_game, after_game = game_text(BEFORE), game_text(AFTER)
    before_income, after_income = income_by_source(BEFORE), income_by_source(AFTER)
    before_leader, after_leader = vivhite(before_game), vivhite(after_game)
    income_changes = {
        source: {"before": before_income.get(source), "after": after_income.get(source)}
        for source in sorted(set(before_income) | set(after_income))
        if before_income.get(source) != after_income.get(source)
    }
    checks = {
        "same_date_first_stage": before["date"] == after["date"] == "2230.10.17"
        and before["situation_count"] == after["situation_count"] == 1
        and before["situation_progress"] == after["situation_progress"] == 48.0,
        "state_fields_unchanged": all(before[field] == after[field] for field in STATE_FIELDS),
        "maintenance_three_and_projects_stable": before["maintenance_count"] == 3
        and before["projects"] == after["projects"]
        and queue(BEFORE) == queue(AFTER),
        "one_identical_vivhite": before_game.count("leader_trait_shishan_code_vivhite") == 1
        and after_game.count("leader_trait_shishan_code_vivhite") == 1
        and before_leader == after_leader,
        "food_bay_income_stable": before_income["starbase_buildings"]["food"]
        == after_income["starbase_buildings"]["food"] == 12.5,
        "no_duplicate_or_fixture": before["vivhite_base_modifiers"]
        == after["vivhite_base_modifiers"] == [1]
        and before["vivhite_engineering_layers"]
        == after["vivhite_engineering_layers"] == [3]
        and before["vivhite_society_layers"]
        == after["vivhite_society_layers"] == [3]
        and before["temporary_boost_refs"] == after["temporary_boost_refs"] == 0,
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "before": before,
        "after": after,
        "before_queue": queue(BEFORE),
        "after_queue": queue(AFTER),
        "vivhite": {"before": before_leader, "after": after_leader},
        "monthly_income_categories_recomputed_on_reload": income_changes,
    }


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
