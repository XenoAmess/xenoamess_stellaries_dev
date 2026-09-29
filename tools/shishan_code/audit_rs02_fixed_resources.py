"""Audit five vanilla fixed monthly resource sources across situation stages."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from audit_pr04_natural_relapse import inspect
from audit_resource_source_saves import income_by_source
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVES = {
    "anchor": EVIDENCE / "rs02-fixed-five-anchor-2229.10.15.sav",
    "I": EVIDENCE / "rs02-fixed-five-stage1-2229.11.20.sav",
    "III": EVIDENCE / "rs02-fixed-five-stage3-2229.11.20.sav",
    "V": EVIDENCE / "rs02-fixed-five-stage5-2229.11.20.sav",
}
VANILLA_MODIFIERS = {
    "volatile_motes": ("relic_vacuum_flower_T_dwarf", 30.0),
    "exotic_gases": ("relic_vacuum_flower_lightbringer", 30.0),
    "rare_crystals": ("relic_vacuum_flower_M", 30.0),
    "sr_zro": ("relic_vacuum_flower_pulsar", 15.0),
    "astral_threads": ("relic_vacuum_flower_rift_star", 15.0),
}
STAGES = {"I": (7.0, 1.25), "III": (507.0, 0.75), "V": (957.0, 0.25)}


def audit() -> dict:
    details = {}
    for stage, path in SAVES.items():
        with zipfile.ZipFile(path) as archive:
            game = archive.read("gamestate").decode("utf-8-sig")
        country = player_country(game)
        state = inspect(path)
        sources = income_by_source(path)
        values = sources.get("country_base", {})
        details[stage] = {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "date": state["date"],
            "situation_count": state["situation_count"],
            "situation_progress": state["situation_progress"],
            "maintenance_count": state["maintenance_count"],
            "modifier_counts": {
                resource: country.count(modifier)
                for resource, (modifier, _) in VANILLA_MODIFIERS.items()
            },
            "country_base_income": {
                resource: values.get(resource) for resource in VANILLA_MODIFIERS
            },
            "other_income_sources": {
                resource: {
                    source: source_values[resource]
                    for source, source_values in sources.items()
                    if source != "country_base" and resource in source_values
                }
                for resource in VANILLA_MODIFIERS
            },
        }
    checks = {
        "same_anchor_and_date": details["anchor"]["date"] == "2229.10.15"
        and all(details[stage]["date"] == "2229.11.20" for stage in STAGES),
        "same_maintenance_count": all(item["maintenance_count"] == 2 for item in details.values()),
        "one_situation_each": all(item["situation_count"] == 1 for item in details.values()),
        "stage_progress": all(
            details[stage]["situation_progress"] == progress
            for stage, (progress, _) in STAGES.items()
        ),
        "one_vanilla_modifier_each": all(
            count == 1
            for item in details.values()
            for count in item["modifier_counts"].values()
        ),
        "five_fixed_resources_exact": all(
            details[stage]["country_base_income"][resource] == base * factor
            for stage, (_, factor) in STAGES.items()
            for resource, (_, base) in VANILLA_MODIFIERS.items()
        ),
        "no_other_source_for_five": all(
            not extra
            for stage in STAGES
            for extra in details[stage]["other_income_sources"].values()
        ),
    }
    return {"pass": all(checks.values()), "checks": checks, "details": details}


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
