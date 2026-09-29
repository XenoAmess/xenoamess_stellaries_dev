"""Audit the native save sequence for maintenance project engine abort recovery."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr02_dual_queue import CLEAN, MAINTAIN, queue
from audit_pr04_natural_relapse import EVIDENCE, inspect
from audit_rs04_vanilla_bonuses import player_country


NAMES = {
    "before": "pr02-dual-projects-after35d-2229.10.15.sav",
    "abort_same_day": "pr02-engine-abort-same-day-2229.10.15.sav",
    "abort_after_six_days": "pr02-engine-abort-after6d-2229.10.21.sav",
    "published_after_month": "pr02-engine-abort-after-month-2229.11.12.sav",
    "candidate_restored": "pr02-engine-abort-recovered-2229.12.04.sav",
    "candidate_next_month": "pr02-engine-abort-stable-2230.01.01.sav",
    "candidate_three_months": "pr02-engine-abort-stable-2230.03.28.sav",
    "candidate_reabort_restored": "pr02-engine-reabort-recovered-2230.04.11.sav",
}
SHOTS = {
    "first_abort_console": "pr02-engine-abort-console-2229.10.15.jpg",
    "first_restore_ui": "pr02-engine-abort-recovered-ui-2229.12.04.jpg",
    "second_abort_console": "pr02-engine-reabort-console-2230.03.28.jpg",
    "second_restore_ui": "pr02-engine-reabort-recovered-ui-2230.04.11.jpg",
}
REPORT = EVIDENCE / "pr02-engine-abort-audit-2026-09-30.json"


def snapshot(path: Path) -> dict:
    data = inspect(path)
    data["queue"] = queue(path)
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    data["maintenance_project_instances"] = len(
        re.findall(r'special_project="SHISHAN_CODE_MAINTAIN"', game)
    )
    data["cleanup_project_instances"] = len(
        re.findall(r'special_project="SHISHAN_CODE_CLEAN"', game)
    )
    data["success_pending_flags"] = sorted(
        set(re.findall(r"shishan_code_(?:maintain|optimize)_success_pending", player))
    )
    return data


def audit() -> dict:
    states = {key: snapshot(EVIDENCE / name) for key, name in NAMES.items()}
    before = states["before"]
    aborted = states["abort_same_day"]
    published_month = states["published_after_month"]
    restored = states["candidate_restored"]
    next_month = states["candidate_next_month"]
    three_months = states["candidate_three_months"]
    reaborted_restored = states["candidate_reabort_restored"]
    invariant_fields = (
        "maintenance_count",
        "last_completed_project",
        "main_traits",
        "refactored_job_modifiers",
        "vivhite_base_modifiers",
        "vivhite_engineering_layers",
        "vivhite_society_layers",
        "situation_count",
        "temporary_boost_refs",
    )
    dates = {
        "before": "2229.10.15",
        "abort_same_day": "2229.10.15",
        "abort_after_six_days": "2229.10.21",
        "published_after_month": "2229.11.12",
        "candidate_restored": "2229.12.04",
        "candidate_next_month": "2230.01.01",
        "candidate_three_months": "2230.03.28",
        "candidate_reabort_restored": "2230.04.11",
    }
    checks = {
        "expected_native_save_dates": all(
            states[key]["date"] == date for key, date in dates.items()
        ),
        "baseline_maintenance_actively_researching": (
            before["projects"][MAINTAIN] == {"id": 5, "status": "in_progress"}
            and before["queue"][0]["project_id"] == 5
            and before["queue"][0]["progress"] > 0
        ),
        "engine_abort_removes_maintenance_without_reward": (
            MAINTAIN not in aborted["projects"]
            and aborted["maintenance_project_instances"] == 0
            and all(aborted[key] == before[key] for key in invariant_fields)
            and aborted["situation_progress"] == before["situation_progress"] == 14.0
            and aborted["success_pending_flags"] == []
        ),
        "published_version_defect_reproduced": all(
            MAINTAIN not in states[key]["projects"]
            and states[key]["maintenance_project_instances"] == 0
            for key in ("abort_after_six_days", "published_after_month")
        ) and published_month["situation_progress"] == 21.0,
        "candidate_restores_exactly_one_available_project": (
            restored["projects"][MAINTAIN] == {"id": 7, "status": None}
            and restored["maintenance_project_instances"] == 1
            and restored["situation_progress"] == 28.0
        ),
        "next_month_and_later_are_idempotent": all(
            states[key]["projects"][MAINTAIN] == {"id": 7, "status": None}
            and states[key]["maintenance_project_instances"] == 1
            for key in ("candidate_next_month", "candidate_three_months")
        ) and next_month["situation_progress"] == 35.0
        and three_months["situation_progress"] == 49.0,
        "second_abort_recovers_new_single_project": (
            reaborted_restored["projects"][MAINTAIN] == {"id": 8, "status": None}
            and reaborted_restored["maintenance_project_instances"] == 1
            and reaborted_restored["situation_progress"] == 56.0
        ),
        "cleanup_queue_and_research_preserved": all(
            state["projects"][CLEAN] == {"id": 6, "status": "in_progress"}
            and state["cleanup_project_instances"] == 1
            and state["queue"][0]["project_id"] == 6
            for key, state in states.items()
            if key != "before"
        ) and [before["queue"][1]["project_id"], aborted["queue"][0]["project_id"]]
        == [6, 6],
        "no_rewards_or_vivhite_changes": all(
            all(state[field] == before[field] for field in invariant_fields)
            and not state["success_pending_flags"]
            for state in states.values()
        ),
    }
    screenshots = {}
    for key, filename in SHOTS.items():
        path = EVIDENCE / filename
        screenshots[key] = {
            "path": str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    result = {
        "pass": all(checks.values()),
        "checks": checks,
        "states": states,
        "screenshots": screenshots,
    }
    return result


if __name__ == "__main__":
    report = audit()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": report["pass"], "checks": report["checks"], "report": str(REPORT)}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
