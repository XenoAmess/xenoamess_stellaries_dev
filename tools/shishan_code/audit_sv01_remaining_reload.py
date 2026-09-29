"""Compare five native save states with same-day in-game reloads."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr04_natural_relapse import projects
from audit_resource_source_saves import read_block
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
PAIRS = {
    "refactored": (
        "pr04_optimize_natural_no_relapse_post_22290727.sav",
        "sv01-refactored-reloaded-2229.07.27.sav",
    ),
    "relapsed": (
        "pr04-relapse-natural-post-2229.08.05.sav",
        "sv01-relapse-reloaded-2229.08.05.sav",
    ),
    "iteration": (
        "iteration-output2-2207.12.05.sav",
        "sv01-iteration-reloaded-2207.12.05.sav",
    ),
    "vivhite_pending": (
        "vivhite-zero-xp-pending.sav",
        "sv01-vivhite-pending-reloaded-2203.06.03.sav",
    ),
    "vivhite_revived": (
        "vivhite-zero-xp-revived.sav",
        "sv01-vivhite-revived-reloaded-2203.06.03.sav",
    ),
}
VIVHITE_TRAIT = "leader_trait_shishan_code_vivhite"
SITUATION = re.compile(r'type="?situation_shishan_code"?')


def state(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    country = player_country(game)
    species = read_block(game, game.index("species_db="))
    leaders = read_block(game, game.index("\nleaders="))
    owned_text = read_block(country, country.index("owned_leaders="))
    owned_ids = set(map(int, re.findall(r"\b\d+\b", owned_text)))
    vivhite_ids = [
        int(match.group(1))
        for match in re.finditer(r"(?m)^\s*(\d+)=\s*\{", leaders)
        if VIVHITE_TRAIT in read_block(leaders, match.start())
    ]
    progress = re.search(
        r'type="?situation_shishan_code"?[\s\S]{0,200}?\bprogress=([\d.]+)',
        game,
    )
    count = re.search(r"shishan_code_maintenance_count=(\d+)", country)
    iterations = {
        name: int(value)
        for name, value in re.findall(r"(shishan_code_iteration_\w+)=(\d+)", country)
    }
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": re.search(r'(?m)^date="([^"]+)"', game).group(1),
        "origin": 'origin="origin_shishan_code"' in country,
        "maintenance_count": int(count.group(1)) if count else None,
        "projects": projects(game),
        "situation_count": len(SITUATION.findall(game)),
        "situation_progress": float(progress.group(1)) if progress else None,
        "species_db_sha256": hashlib.sha256(species.encode()).hexdigest(),
        "leader_db_sha256": hashlib.sha256(leaders.encode()).hexdigest(),
        "owned_leaders": sorted(owned_ids),
        "vivhite_employed_ids": sorted(set(vivhite_ids) & owned_ids),
        "vivhite_leader_ids": sorted(vivhite_ids),
        "vivhite_base_count": country.count('modifier="shishan_code_vivhite_base"'),
        "refactored_modifier_count": country.count('modifier="shishan_code_refactored_jobs"'),
        "pending_reboot": "shishan_code_vivhite_pending_reboot=" in country,
        "backup_xp": (
            float(re.search(r"shishan_code_vivhite_backup_xp=([\d.]+)", country).group(1))
            if "shishan_code_vivhite_backup_xp=" in country
            else None
        ),
        "iterations": iterations,
        "mod_country_lines": sorted(line.strip() for line in country.splitlines() if "shishan_code" in line),
        "empty_timed_modifier_count": country.count('modifier=""'),
        "temporary_boost_refs": game.count("shishan_test_society_boost"),
    }


def audit() -> dict:
    rows = {}
    checks = {}
    stable_fields = tuple(
        key
        for key in state(EVIDENCE / PAIRS["refactored"][0])
        if key not in ("path", "sha256", "empty_timed_modifier_count")
    )
    for label, (before_name, after_name) in PAIRS.items():
        before = state(EVIDENCE / before_name)
        after = state(EVIDENCE / after_name)
        differences = {
            field: {"before": before[field], "after": after[field]}
            for field in stable_fields
            if before[field] != after[field]
        }
        checks[f"{label}_same_day_state"] = before["origin"] and not differences
        checks[f"{label}_no_duplicates"] = before["situation_count"] <= 1 and len(before["vivhite_employed_ids"]) <= 1
        rows[label] = {"before": before, "after": after, "differences": differences}

    refactored = rows["refactored"]["after"]
    checks["refactored_expected_state"] = (
        refactored["situation_count"] == 0
        and refactored["refactored_modifier_count"] == 1
        and refactored["maintenance_count"] == 1
        and "SHISHAN_CODE_OPTIMIZE" in refactored["projects"]
    )
    relapsed = rows["relapsed"]["after"]
    checks["relapsed_expected_state"] = (
        relapsed["situation_count"] == 1
        and relapsed["situation_progress"] == 0
        and relapsed["refactored_modifier_count"] == 0
        and relapsed["maintenance_count"] == 2
        and {"SHISHAN_CODE_MAINTAIN", "SHISHAN_CODE_CLEAN"}.issubset(relapsed["projects"])
    )
    iteration = rows["iteration"]["after"]
    checks["iteration_two_layers"] = iteration["iterations"] == {"shishan_code_iteration_output": 2}
    pending = rows["vivhite_pending"]["after"]
    checks["pending_reboot_state"] = (
        pending["pending_reboot"]
        and pending["backup_xp"] == 0
        and pending["vivhite_employed_ids"] == []
        and pending["vivhite_base_count"] == 0
    )
    revived = rows["vivhite_revived"]["after"]
    checks["revived_state"] = (
        not revived["pending_reboot"]
        and revived["backup_xp"] is None
        and len(revived["vivhite_employed_ids"]) == 1
        and revived["vivhite_base_count"] == 1
    )
    checks["no_fixture_refs"] = all(row["after"]["temporary_boost_refs"] == 0 for row in rows.values())
    checks["preexisting_empty_modifier_discarded"] = (
        rows["refactored"]["before"]["empty_timed_modifier_count"] == 1
        and all(row["after"]["empty_timed_modifier_count"] == 0 for row in rows.values())
        and all(row["before"]["empty_timed_modifier_count"] == 0 for label, row in rows.items() if label != "refactored")
    )
    return {"pass": all(checks.values()), "checks": checks, "states": rows}


if __name__ == "__main__":
    report = audit()
    output = EVIDENCE / "sv01-remaining-reload-audit-2026-09-30.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": report["pass"], "checks": report["checks"], "output": str(output)}, indent=2))
    raise SystemExit(0 if report["pass"] else 1)
