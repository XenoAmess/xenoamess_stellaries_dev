"""Check that situation production modifiers leave commercial pact trade unchanged."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_resource_source_saves import income_by_source, read_block


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "anchor": EVIDENCE / "rs03-commercial-anchor-2203.11.08.sav",
    "II": EVIDENCE / "rs03-commercial-stage2-2203.12.13.sav",
    "V": EVIDENCE / "rs03-commercial-stage5-2203.12.13.sav",
}


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    date = re.search(r'(?m)^date="([^"]+)"', game)
    situation = re.search(r'type="situation_shishan_code"\s+progress=([0-9.]+)', game)
    if not date or not situation:
        raise ValueError(f"Missing game date or origin situation in {path}")
    budget = read_block(game, game.index("budget="))
    month = read_block(budget, budget.index("current_month="))
    expense = read_block(month, month.index("expenses="))
    pact = re.search(r"commercial_pacts=\s*\{\s*influence=([0-9.]+)", expense)
    if not pact:
        raise ValueError(f"Missing commercial pact influence upkeep in {path}")
    income = income_by_source(path)
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "date": date.group(1),
        "situation_progress": float(situation.group(1)),
        "commercial_pact_trade": income["commercial_pacts"]["trade"],
        "commercial_pact_influence_upkeep": float(pact.group(1)),
        "country_base_energy": income["country_base"]["energy"],
        "country_base_minerals": income["country_base"]["minerals"],
        "orbital_mining_energy": income["orbital_mining_deposits"]["energy"],
        "trade_policy_energy": income["trade_policy"]["energy"],
    }


def audit() -> dict:
    result = {stage: inspect(path) for stage, path in SAVES.items()}
    second, fifth = result["II"], result["V"]
    checks = {
        "same_day": second["date"] == fifth["date"] == "2203.12.13",
        "correct_stages": 250 <= second["situation_progress"] < 500
        and fifth["situation_progress"] >= 950,
        "pact_income_nonzero_and_equal": second["commercial_pact_trade"] > 0
        and abs(second["commercial_pact_trade"] - fifth["commercial_pact_trade"]) < 0.00001,
        "pact_upkeep_nonzero_and_equal": second["commercial_pact_influence_upkeep"] > 0
        and second["commercial_pact_influence_upkeep"] == fifth["commercial_pact_influence_upkeep"],
        "country_base_follows_stage": all(
            second[f"country_base_{resource}"] == 4 * fifth[f"country_base_{resource}"]
            for resource in ("energy", "minerals")
        ),
        "station_production_changes": second["orbital_mining_energy"] > fifth["orbital_mining_energy"],
    }
    return {"pass": all(checks.values()), "checks": checks, "saves": result}


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["pass"] else 1)
