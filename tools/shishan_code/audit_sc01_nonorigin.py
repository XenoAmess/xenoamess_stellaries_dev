"""Check that a normal organic empire receives no Shishan origin content."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from audit_pr03_mixed_refactor import species_traits
from audit_resource_source_saves import read_block
from audit_rs04_vanilla_bonuses import player_country


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "assets" / "shishan-code-origin" / "evidence"
SAVE = EVIDENCE / "sc01-une-nonorigin-2200.01.01.sav"
MOD = ROOT / "shishan_code_origin" / "mod"


def audit() -> dict:
    with zipfile.ZipFile(SAVE) as archive:
        game = archive.read("gamestate").decode("utf-8-sig")
    player = player_country(game)
    origin = re.search(r'\borigin="([^"]+)"', player)
    founder = re.search(r"\bfounder_species_ref=(\d+)", player)
    if not origin or not founder:
        raise ValueError("Player origin or founder species absent from native save")
    traits = species_traits(game, int(founder.group(1)))
    origin_source = (MOD / "common/governments/civics/shishan_code_origin.txt").read_text(encoding="utf-8-sig")
    building_source = (MOD / "common/buildings/shishan_code_buildings.txt").read_text(encoding="utf-8-sig")
    situation_source = (MOD / "common/situations/shishan_code_situation.txt").read_text(encoding="utf-8-sig")
    events_source = (MOD / "events/shishan_code_events.txt").read_text(encoding="utf-8-sig")
    checks = {
        "standard_organic_origin": origin.group(1) == "origin_default",
        "organic_founder_has_no_shishan_trait": "trait_shishan_code" not in traits,
        "no_shishan_runtime_objects_in_new_game": "shishan" not in game.lower(),
        "origin_requires_machine_species": "species_archetype = { value = MACHINE }" in origin_source,
        "building_requires_origin": "owner = { has_origin = origin_shishan_code }" in building_source,
        "situation_aborts_without_origin": "abort_trigger = { owner = { NOT = { has_origin = origin_shishan_code } } }" in situation_source,
        "initialization_requires_origin": "has_origin = origin_shishan_code" in events_source,
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "save": str(SAVE.relative_to(ROOT)).replace("\\", "/"),
        "sha256": hashlib.sha256(SAVE.read_bytes()).hexdigest(),
        "date": re.search(r'(?m)^date="([^"]+)"', game).group(1),
        "player_origin": origin.group(1),
        "founder_species_id": int(founder.group(1)),
        "founder_traits": traits,
        "runtime_shishan_string_count": game.lower().count("shishan"),
    }


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
