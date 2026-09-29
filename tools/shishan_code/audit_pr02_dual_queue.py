"""Verify that two society special projects research sequentially."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from audit_pr04_natural_relapse import EVIDENCE, inspect
from audit_resource_source_saves import read_block


BEFORE = EVIDENCE / "pr02-dual-projects-queued-2229.09.10.sav"
AFTER = EVIDENCE / "pr02-dual-projects-after35d-2229.10.15.sav"
MAINTAIN = "SHISHAN_CODE_MAINTAIN"
CLEAN = "SHISHAN_CODE_CLEAN"


def queue(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    block = read_block(game, game.index("society_queue="))
    entries = []
    for match in re.finditer(r"\{[^{}]*\}", block):
        item = match.group(0)
        project = re.search(r"special_project=(\d+)", item)
        technology = re.search(r'technology="([^"]+)"', item)
        progress = re.search(r"progress=([\d.]+)", item)
        if project or technology:
            entries.append({
                "project_id": int(project.group(1)) if project else None,
                "technology": technology.group(1) if technology else None,
                "progress": float(progress.group(1)) if progress else 0.0,
            })
    return entries


def audit() -> dict:
    before, after = inspect(BEFORE), inspect(AFTER)
    before_queue, after_queue = queue(BEFORE), queue(AFTER)
    ids = [before["projects"][MAINTAIN]["id"], before["projects"][CLEAN]["id"]]
    expected = [ids[0], ids[1], None]
    checks = {
        "date_and_single_instances": before["date"] == "2229.09.10"
        and after["date"] == "2229.10.15"
        and before["projects"][MAINTAIN]["id"] == after["projects"][MAINTAIN]["id"]
        and before["projects"][CLEAN]["id"] == after["projects"][CLEAN]["id"],
        "both_ui_researching_means_queued": all(
            record["projects"][name]["status"] == "in_progress"
            for record in (before, after)
            for name in (MAINTAIN, CLEAN)
        ),
        "stable_order_and_one_of_each": [entry["project_id"] for entry in before_queue]
        == [entry["project_id"] for entry in after_queue] == expected
        and before_queue[2]["technology"] == after_queue[2]["technology"]
        == "tech_planetary_unification",
        "only_head_receives_research": [entry["progress"] for entry in before_queue]
        == [0.0, 0.0, 0.0]
        and [entry["progress"] for entry in after_queue]
        == [28.33912, 0.0, 0.0],
        "no_completion_or_reward": before["maintenance_count"] == after["maintenance_count"] == 2
        and before["last_completed_project"] == after["last_completed_project"]
        and before["main_traits"] == after["main_traits"],
        "natural_situation_advance_only": before["situation_count"] == after["situation_count"] == 1
        and before["situation_progress"] == 7.0
        and after["situation_progress"] == 14.0,
        "vivhite_and_refactor_unchanged": all(
            before[key] == after[key]
            for key in (
                "refactored_job_modifiers",
                "vivhite_base_modifiers",
                "vivhite_engineering_layers",
                "vivhite_society_layers",
            )
        ),
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "before": before,
        "after": after,
        "before_queue": before_queue,
        "after_queue": after_queue,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
