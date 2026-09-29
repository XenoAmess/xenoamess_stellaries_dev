"""Compare native saves before and after canceling an active maintenance project."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr04_natural_relapse import EVIDENCE, ROOT, inspect
from audit_resource_source_saves import read_block


BEFORE = EVIDENCE / "pr02-n2-cancel-in-progress-2229.09.10.sav"
AFTER = EVIDENCE / "pr02-n2-cancel-post-2229.09.10.sav"
PROJECT = "SHISHAN_CODE_MAINTAIN"


def queue(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    block = read_block(game, game.index("society_queue="))
    project = re.search(r"special_project=(\d+)", block)
    progress = re.search(r"progress=([\d.]+)", block)
    technology = re.search(r'technology="([^"]+)"', block)
    return {
        "project_id": int(project.group(1)) if project else None,
        "progress": float(progress.group(1)) if progress else None,
        "technology": technology.group(1) if technology else None,
    }


def audit() -> dict:
    before, after = inspect(BEFORE), inspect(AFTER)
    before_queue, after_queue = queue(BEFORE), queue(AFTER)
    checks = {
        "same_day": before["date"] == after["date"] == "2229.09.10",
        "active_project_had_real_research": before["projects"][PROJECT]["status"] == "in_progress"
        and before_queue["project_id"] == before["projects"][PROJECT]["id"]
        and before_queue["progress"] > 0,
        "canceled_and_available_again": after["projects"][PROJECT]["status"] is None
        and after["projects"][PROJECT]["id"] == before["projects"][PROJECT]["id"]
        and after_queue["project_id"] is None,
        "no_settlement_or_reward": before["maintenance_count"] == after["maintenance_count"] == 2
        and before["last_completed_project"] == after["last_completed_project"]
        == "SHISHAN_CODE_OPTIMIZE"
        and before["main_traits"] == after["main_traits"],
        "situation_untouched": before["situation_count"] == after["situation_count"] == 1
        and before["situation_progress"] == after["situation_progress"] == 7.0,
        "national_and_vivhite_modifiers_untouched": all(
            before[key] == after[key]
            for key in (
                "refactored_job_modifiers",
                "vivhite_base_modifiers",
                "vivhite_engineering_layers",
                "vivhite_society_layers",
            )
        ),
        "no_fixture_modifier": before["temporary_boost_refs"] == after["temporary_boost_refs"] == 0,
    }
    screenshots = {}
    for name in (
        "pr02-n2-cancel-in-progress-2229.09.10.jpg",
        "pr02-n2-cancel-post-2229.09.10.jpg",
    ):
        path = EVIDENCE / name
        screenshots[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "before": before,
        "after": after,
        "before_queue": before_queue,
        "after_queue": after_queue,
        "screenshots_sha256": screenshots,
    }


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
