"""Audit natural optimization relapse from native Stellaris saves."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr01_optimize_n2 import modifier_layers
from audit_pr03_mixed_refactor import species_traits
from audit_resource_source_saves import read_block
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
BEFORE = EVIDENCE / "pr01-optimize-n1-in-progress-2229.07.27.sav"
AFTER = EVIDENCE / "pr04-relapse-natural-post-2229.08.05.sav"
MAIN_SPECIES = 855638017


def projects(game: str) -> dict[str, dict]:
    result = {}
    for match in re.finditer(r"special_project=\s*\{\s*id=(\d+)\s+special_project=\"(SHISHAN_CODE_[A-Z_]+)\"", game):
        block = read_block(game, match.start())
        status = re.search(r"status=(\w+)", block)
        result[match.group(2)] = {
            "id": int(match.group(1)),
            "status": status.group(1) if status else None,
        }
    return result


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    date = re.search(r'(?m)^date="([^"]+)"', game).group(1)
    count = re.search(r"shishan_code_maintenance_count=(\d+)", player)
    last = re.search(r'last_completed_special_project="([^"]+)"', player)
    situation_progress = re.search(
        r'type="?situation_shishan_code"?[\s\S]{0,200}?\bprogress=([\d.]+)',
        game,
    )
    queue = read_block(game, game.index("society_queue="))
    available = projects(game)
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": date,
        "maintenance_count": int(count.group(1)),
        "last_completed_project": last.group(1) if last else None,
        "projects": available,
        "society_queue_on_optimize": (
            "SHISHAN_CODE_OPTIMIZE" in available
            and f"special_project={available['SHISHAN_CODE_OPTIMIZE']['id']}" in queue
        ),
        "main_traits": species_traits(game, MAIN_SPECIES),
        "situation_count": len(re.findall(r'type="?situation_shishan_code"?', game)),
        "situation_progress": float(situation_progress.group(1)) if situation_progress else None,
        "refactored_job_modifiers": modifier_layers(player, "shishan_code_refactored_jobs"),
        "vivhite_base_modifiers": modifier_layers(player, "shishan_code_vivhite_base"),
        "vivhite_engineering_layers": modifier_layers(player, "shishan_code_vivhite_engineering_step"),
        "vivhite_society_layers": modifier_layers(player, "shishan_code_vivhite_society_step"),
        "temporary_boost_refs": game.count("shishan_test_society_boost"),
    }


def audit() -> dict:
    before, after = inspect(BEFORE), inspect(AFTER)
    added = sorted(set(after["main_traits"]) - set(before["main_traits"]))
    removed = sorted(set(before["main_traits"]) - set(after["main_traits"]))
    source = (ROOT / "shishan_code_origin" / "mod" / "events" / "shishan_code_events.txt").read_text(encoding="utf-8-sig")
    checks = {
        "formal_branch_still_90_to_10": '90 = { country_event = { id = shishan_code.32 } }' in source
        and '10 = { country_event = { id = shishan_code.31 } }' in source,
        "natural_project_completion_once": before["maintenance_count"] == 1
        and after["maintenance_count"] == 2
        and before["society_queue_on_optimize"]
        and not after["society_queue_on_optimize"]
        and after["last_completed_project"] == "SHISHAN_CODE_OPTIMIZE",
        "relapse_starts_at_zero": before["situation_count"] == 0
        and after["situation_count"] == 1
        and after["situation_progress"] == 0,
        "species_transition_and_single_reward": "trait_shishan_refactored" in removed
        and "trait_shishan_code" in added
        and len(added) == 2
        and len(removed) == 1,
        "national_refactor_removed": before["refactored_job_modifiers"] == [1]
        and after["refactored_job_modifiers"] == [],
        "vivhite_exactly_two_steps": after["vivhite_base_modifiers"] == [1]
        and after["vivhite_engineering_layers"] == [2]
        and after["vivhite_society_layers"] == [2],
        "projects_switched": "SHISHAN_CODE_OPTIMIZE" not in after["projects"]
        and "SHISHAN_CODE_MAINTAIN" in after["projects"]
        and "SHISHAN_CODE_CLEAN" in after["projects"],
        "fixture_removed_before_save": after["temporary_boost_refs"] == 0,
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "added_traits": added,
        "removed_traits": removed,
        "before": before,
        "after": after,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
