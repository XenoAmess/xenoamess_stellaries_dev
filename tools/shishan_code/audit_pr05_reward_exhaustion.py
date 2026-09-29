"""Reconcile the exhausted reward save with the current reward whitelist."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from audit_pr03_mixed_refactor import species_traits
from audit_rs04_vanilla_bonuses import player_country
from generate_rewards import OTHER, ROBOTIC, compatible_name


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
EXHAUSTED = EVIDENCE / "shishan_reward_exhausted.sav"
REPORT = EVIDENCE / "pr05-reward-closure-audit-2026-09-30.json"
GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris")
ITERATIONS = {
    "output": ("iteration-output1-2207.12.05.sav", "iteration-output2-2207.12.05.sav"),
    "energy": ("iteration-energy1-2207.12.05.sav", "iteration-energy2-2207.12.05.sav"),
    "assembly": ("iteration-housing1-2207.12.05.sav", "iteration-housing2-2207.12.05.sav"),
    "experience": ("iteration-research1-2208.02.06.sav", "iteration-research2-2208.02.06.sav"),
}


def state(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    founder = re.search(r"founder_species_ref=(\d+)", player)
    if founder is None:
        raise ValueError(f"player founder species missing: {path}")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "species_id": int(founder.group(1)),
        "traits": species_traits(game, int(founder.group(1))),
        "iteration_counts": {
            suffix: int(match.group(1)) if (match := re.search(
                rf"shishan_code_iteration_{suffix}=(\d+)", player
            )) else 0
            for suffix in ITERATIONS
        },
    }


def static_check(script: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "shishan_code" / script), "--game", str(GAME)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "pass": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def audit() -> dict:
    exhausted = state(EXHAUSTED)
    traits = exhausted["traits"]
    have = set(traits)
    other_names = {item[0] for item in OTHER}
    robotic_present = [name for name, *_ in ROBOTIC if name in have]
    robotic_absent = [
        {"name": name, "blocking_traits": [opposite for opposite in conflicts if opposite in have]}
        for name, conflicts, *_ in ROBOTIC
        if name not in have
    ]
    compatible_present = [compatible_name(name) for name, *_ in OTHER if compatible_name(name) in have]
    compatible_absent = []
    for name, conflicts, *_ in OTHER:
        mapped = compatible_name(name)
        if mapped in have:
            continue
        blockers = [opposite for opposite in conflicts if opposite in have]
        blockers.extend(
            compatible_name(opposite)
            for opposite in conflicts
            if opposite in other_names and compatible_name(opposite) in have
        )
        compatible_absent.append({"name": mapped, "blocking_traits": blockers})
    iterations = {
        suffix: [state(EVIDENCE / name) for name in files]
        for suffix, files in ITERATIONS.items()
    }
    static = {
        "reward_contract": static_check("audit_reward_contract.py"),
        "compatible_values": static_check("audit_compat_traits.py"),
    }
    checks = {
        "native_save_expected": exhausted["sha256"]
        == "554504e65d4b14d70fd91be3cb66c434c7c232ea37c109e70b7e2ebe93f4fccf"
        and exhausted["species_id"] == 855638017,
        "one_unique_main_species_template": len(traits) == len(have) == 43
        and "trait_machine_unit" in have
        and "trait_shishan_code" in have,
        "mechanical_tier_complete_with_conflict_exclusions": len(robotic_present) == 17
        and len(robotic_absent) == 3
        and all(entry["blocking_traits"] for entry in robotic_absent),
        "compatible_tier_complete_with_conflict_exclusions": len(compatible_present) == 16
        and len(compatible_absent) == 3
        and all(entry["blocking_traits"] for entry in compatible_absent),
        "iteration_tier_present_and_accumulated": all(
            traits.count(f"trait_shishan_iteration_{suffix}") == 1
            and exhausted["iteration_counts"][suffix] > 2
            for suffix in ITERATIONS
        ),
        "four_iteration_one_to_two_saves": all(
            all(
                row["iteration_counts"][suffix] == layer
                and row["traits"].count(f"trait_shishan_iteration_{suffix}") == 1
                for layer, row in enumerate(rows, start=1)
            ) for suffix, rows in iterations.items()
        ),
        "static_pool_guards_weights_and_target": static["reward_contract"]["pass"],
        "nineteen_compatible_values_match_vanilla": static["compatible_values"]["pass"],
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "exhausted": exhausted,
        "robotic_present": robotic_present,
        "robotic_absent": robotic_absent,
        "compatible_present": compatible_present,
        "compatible_absent": compatible_absent,
        "iterations": iterations,
        "static": static,
        "runtime_numeric_limits": "One mechanical-compatible miner trait and all four iteration types have controlled numeric game samples; this audit does not claim 39 individual numeric game comparisons or statistical RNG validation.",
    }


if __name__ == "__main__":
    result = audit()
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": result["pass"], "checks": result["checks"], "report": str(REPORT)}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
