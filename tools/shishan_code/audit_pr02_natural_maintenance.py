"""Audit the archived pre/post saves of a naturally finished maintenance project."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_resource_source_saves import read_block


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "pre": EVIDENCE / "pr02-maintain-natural-pre-2226.11.17.sav",
    "post": EVIDENCE / "pr02-maintain-natural-post-2227.05.17.sav",
}


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    date = re.search(r'(?m)^date="([^"]+)"', game)
    count = re.search(r"shishan_code_maintenance_count=(\d+)", game)
    situation = re.search(
        r'type="situation_shishan_code"\s+progress=([0-9.]+)\s+last_month_progress=([0-9.]+)',
        game,
    )
    if not date or not count or not situation:
        raise ValueError(f"Missing required save fields in {path}")
    first_country = game[: game.find("last_completed_special_project=", game.find("budget=")) + 100]
    last = re.search(r'last_completed_special_project="([^"]+)"', first_country)
    project_queue = re.search(r"progress=([0-9.]+)\s+special_project=5", game)
    species = read_block(game, game.index("species_db="))
    # The player's main machine species has the same native ID in both branches.
    main_species = read_block(species, species.index("855638017="))
    main_traits = read_block(main_species, main_species.index("traits="))
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": date.group(1),
        "maintenance_count": int(count.group(1)),
        "situation_progress": float(situation.group(1)),
        "last_month_progress": float(situation.group(2)),
        "maintenance_society_progress": float(project_queue.group(1)) if project_queue else None,
        "last_completed_project": last.group(1) if last else None,
        "main_species_id": 855638017,
        "shishan_trait_occurrences": main_traits.count('trait="trait_shishan_code"'),
        "new_robot_sociologist_trait_occurrences": main_traits.count(
            'trait="trait_robot_artificial_sociologists"'
        ),
        "temporary_society_boost_occurrences": game.count("shishan_test_society_boost"),
    }


def audit() -> dict:
    pre, post = (inspect(SAVES[key]) for key in ("pre", "post"))
    checks = {
        "pre_research_in_progress": pre["maintenance_society_progress"] == 56.43412
        and pre["maintenance_count"] == 1,
        "normal_project_completion": post["maintenance_society_progress"] is None
        and post["last_completed_project"] == "SHISHAN_CODE_MAINTAIN",
        "exactly_one_maintenance": post["maintenance_count"] - pre["maintenance_count"] == 1,
        "monthly_speed_increased_by_one": post["last_month_progress"] - pre["last_month_progress"] == 1,
        "situation_reset_then_advanced": post["situation_progress"] == 28
        and post["last_month_progress"] == 7,
        "one_valid_reward_added": pre["new_robot_sociologist_trait_occurrences"] == 0
        and post["new_robot_sociologist_trait_occurrences"] == 1,
        "original_trait_remains": pre["shishan_trait_occurrences"]
        == post["shishan_trait_occurrences"]
        == 1,
        "fixture_only_in_post": pre["temporary_society_boost_occurrences"] == 0
        and post["temporary_society_boost_occurrences"] == 1,
    }
    return {"pass": all(checks.values()), "checks": checks, "saves": {"pre": pre, "post": post}}


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
