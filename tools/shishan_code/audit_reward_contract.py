"""Read-only audit of candidate data and emitted three-choice reward state.

Candidate identities come from the generated pool; their allowed archetypes
and positive tags are checked against installed vanilla data. Reward behavior
is checked independently by the feedback validator's emitted-AST interpreter.
No game process, desktop automation, or runtime probe is used.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import sys

from audit_compat_traits import block
from generate_rewards import OUTPUT, ROBOTIC


ROOT = Path(__file__).resolve().parents[2]


def feedback_validator():
    path = ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py"
    spec = importlib.util.spec_from_file_location("shishan_feedback_reward_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load read-only validator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def audit_vanilla_candidates(game: Path) -> int:
    vanilla = (game / "common/traits/05_species_traits_robotic.txt").read_text(encoding="utf-8-sig")
    seen = set()
    for name, *_ in ROBOTIC:
        if name in seen:
            raise AssertionError(f"duplicate robotic candidate: {name}")
        seen.add(name)
        definition = block(vanilla, name)
        if not re.search(r"allowed_archetypes\s*=\s*\{\s*ROBOT\s+MACHINE\s*\}", definition):
            raise AssertionError(f"candidate archetype mismatch: {name}")
        if not re.search(r"tags\s*=\s*\{[^}]*\bpositive\b", definition):
            raise AssertionError(f"candidate is not a vanilla positive: {name}")
    return len(seen)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", required=True, type=Path)
    args = parser.parse_args()
    robotic_count = audit_vanilla_candidates(args.game)
    result = feedback_validator().check_rewards(OUTPUT.parents[2])
    print(
        "reward contract: PASS (static/offline AST only; "
        f"{robotic_count} vanilla robotic positives; "
        f"{result['seeded_candidate_cases']} seeded candidate cases; "
        "cooldown 3 -> 2 -> 1 -> 0; engine runtime NOT RUN)"
    )


if __name__ == "__main__":
    main()
