"""Audit a second naturally researched optimization from archived native saves."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr03_mixed_refactor import species_traits
from audit_resource_source_saves import read_block
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "anchor": EVIDENCE / "pr04_optimize_natural_no_relapse_post_22290727.sav",
    "researching": EVIDENCE / "pr01-optimize-n1-in-progress-2229.07.27.sav",
    "completed": EVIDENCE / "pr01-optimize-n2-natural-post-2229.09.02.sav",
}
MAIN_SPECIES = 855638017
OPTIMIZE = "SHISHAN_CODE_OPTIMIZE"


def modifier_layers(player: str, name: str) -> list[int]:
    timed = read_block(player, player.index("timed_modifier="))
    entries = re.findall(
        rf"(?:multiplier=(\d+)\s+)?modifier=\"{re.escape(name)}\"",
        timed,
    )
    return [int(entry) if entry else 1 for entry in entries]


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    project = re.search(
        rf'special_project=\s*\{{\s*id=(\d+)\s+special_project="{OPTIMIZE}"',
        game,
    )
    if not project:
        raise ValueError(f"Missing optimize project in {path}")
    project_block = read_block(game, project.start())
    queue = read_block(game, game.index("society_queue="))
    count = re.search(r"shishan_code_maintenance_count=(\d+)", player)
    date = re.search(r'(?m)^date="([^"]+)"', game)
    last = re.search(r'last_completed_special_project="([^"]+)"', player)
    if not count or not date:
        raise ValueError(f"Missing count/date in {path}")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": date.group(1),
        "maintenance_count": int(count.group(1)),
        "optimize_project_id": int(project.group(1)),
        "optimize_in_progress": "status=in_progress" in project_block,
        "society_queue_on_optimize": f"special_project={project.group(1)}" in queue,
        "last_completed_project": last.group(1) if last else None,
        "main_traits": species_traits(game, MAIN_SPECIES),
        "situation_count": len(re.findall(r'type="situation_shishan_code"', game)),
        "refactored_flag": "shishan_code_refactored=" in player,
        "refactored_job_modifiers": modifier_layers(player, "shishan_code_refactored_jobs"),
        "vivhite_base_modifiers": modifier_layers(player, "shishan_code_vivhite_base"),
        "vivhite_engineering_layers": modifier_layers(
            player, "shishan_code_vivhite_engineering_step"
        ),
        "vivhite_society_layers": modifier_layers(
            player, "shishan_code_vivhite_society_step"
        ),
        "temporary_boost_refs": game.count("shishan_test_society_boost"),
    }


def audit() -> dict:
    saves = {key: inspect(path) for key, path in SAVES.items()}
    anchor, researching, completed = (saves[key] for key in SAVES)
    added = sorted(set(completed["main_traits"]) - set(researching["main_traits"]))
    removed = sorted(set(researching["main_traits"]) - set(completed["main_traits"]))
    checks = {
        "same_day_formal_research_start": anchor["date"] == researching["date"]
        == "2229.07.27"
        and anchor["maintenance_count"] == researching["maintenance_count"] == 1
        and not anchor["optimize_in_progress"]
        and researching["optimize_in_progress"]
        and researching["society_queue_on_optimize"],
        "natural_project_end": completed["date"] == "2229.09.02"
        and not completed["optimize_in_progress"]
        and not completed["society_queue_on_optimize"]
        and completed["last_completed_project"] == OPTIMIZE,
        "exactly_one_count_and_reward": completed["maintenance_count"] == 2
        and researching["main_traits"] == anchor["main_traits"]
        and added == ["trait_robot_harvesters"]
        and not removed
        and len(completed["main_traits"]) == len(researching["main_traits"]) + 1,
        "no_relapse_or_duplicate_refactor": completed["situation_count"] == 0
        and completed["refactored_flag"]
        and completed["main_traits"].count("trait_shishan_refactored") == 1
        and completed["refactored_job_modifiers"] == [1],
        "vivhite_exactly_two_steps": completed["vivhite_base_modifiers"] == [1]
        and completed["vivhite_engineering_layers"] == [2]
        and completed["vivhite_society_layers"] == [2],
        "fixture_removed_before_save": researching["temporary_boost_refs"] == 0
        and completed["temporary_boost_refs"] == 0,
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "added_traits": added,
        "removed_traits": removed,
        "saves": saves,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
