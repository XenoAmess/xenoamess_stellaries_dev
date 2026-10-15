"""Read-only canonical vanilla eligibility and emitted reward AST audit.

Expectations come from installed trait definitions, including every repeated
opposites field and reverse edges across all vanilla trait files. No game,
desktop automation, or runtime probe is used. Engine behavior remains outside
this deliberately narrow offline interpreter.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

from generate_rewards import OUTPUT, ROBOTIC, ROBOTIC_REQUIRED_DLC


ROOT = Path(__file__).resolve().parents[2]
_CHECKS = None


def feedback_validator():
    global _CHECKS
    if _CHECKS is None:
        path = ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py"
        spec = importlib.util.spec_from_file_location("shishan_feedback_reward_validator", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load read-only validator: {path}")
        _CHECKS = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = _CHECKS
        spec.loader.exec_module(_CHECKS)
    return _CHECKS


def unquote(value: str) -> str:
    return value.strip('"')


def members(definition, key: str) -> set[str]:
    """Merge repeated list assignments; never collapse the AST into a dict."""
    c = feedback_validator()
    result = set()
    for entry in definition:
        if entry.key == key:
            for item in c.block(entry.value):
                c.require(item.op is None and item.value is None, f"non-list {key}: {item}")
                result.add(unquote(item.key))
    return result


def canonical_traits(sources: list[tuple[str, str]], selected: list[str]) -> dict:
    """Build metadata from independently supplied P files, not pool constants."""
    c = feedback_validator()
    definitions, paths, source_hashes = {}, {}, {}
    for path, text in sources:
        source_hashes[path] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        for entry in c.parse(text):
            if not entry.key.startswith("trait_"):
                continue
            c.require(entry.key not in definitions, f"ambiguous vanilla trait definition: {entry.key}")
            definitions[entry.key] = c.block(entry.value)
            paths[entry.key] = path
    direct = {name: members(body, "opposites") for name, body in definitions.items()}
    result = {}
    for name in selected:
        c.require(name in definitions, f"vanilla candidate missing: {name}")
        body = definitions[name]
        reverse = {other for other, conflicts in direct.items() if name in conflicts}
        dlcs = [unquote(str(entry.value)) for entry in body if entry.key == "host_has_dlc"]
        c.require(len(dlcs) <= 1, f"unsupported multiple DLC gates: {name}")
        forbidden = members(body, "forbidden_ethics")
        c.require(forbidden <= {"ethic_gestalt_consciousness"}, f"unmodeled forbidden ethics: {name}: {forbidden}")
        c.require(not any(e.key in {"forbidden_civics", "species_possible_add", "potential"} for e in body), f"unmodeled native eligibility field: {name}")
        potential = [entry for entry in body if entry.key == "species_potential_add"]
        potential_keys = []
        if potential:
            c.equal(len(potential), 1, f"native species_potential_add count: {name}")
            alternatives = c.block(c.one(c.block(potential[0].value), "OR"))
            allowed = {"can_add_droid_traits", "can_add_synth_traits", "owner_is_machine_intelligence", "owner_is_individual_machine"}
            c.require(all(entry.key in allowed and entry.op == "=" and entry.value == "yes" for entry in alternatives), f"unmodeled native species_potential_add: {name}")
            potential_keys = [entry.key for entry in alternatives]
            c.require("owner_is_individual_machine" in potential_keys, f"native potential excludes individual machines: {name}")
            if "ethic_gestalt_consciousness" not in forbidden:
                c.require("owner_is_machine_intelligence" in potential_keys, f"native potential excludes machine intelligence: {name}")
        result[name] = {
            "source": paths[name], "allowed_archetypes": sorted(members(body, "allowed_archetypes")),
            "tags": sorted(members(body, "tags")), "direct_opposites": sorted(direct[name]),
            "reverse_opposites": sorted(reverse), "opposites": sorted(direct[name] | reverse),
            "required_dlc": dlcs[0] if dlcs else None, "forbidden_ethics": sorted(forbidden),
            "species_potential_add_or": potential_keys,
        }
    return {"traits": result, "source_sha256": source_hashes, "files": len(sources)}


def check_declarations(canonical: dict, robotic, required_dlc: dict) -> list[str]:
    c = feedback_validator()
    names = [item[0] for item in robotic]
    c.equal(len(names), len(set(names)), "unique robotic candidate identities")
    c.equal(set(names), set(canonical["traits"]), "canonical candidate identities")
    conservative = []
    for name, opposites, individual, _ in robotic:
        native = canonical["traits"][name]
        c.equal(set(native["allowed_archetypes"]), {"ROBOT", "MACHINE"}, f"native archetypes: {name}")
        c.require("positive" in native["tags"], f"native candidate is not positive: {name}")
        c.equal(set(opposites), set(native["opposites"]), f"canonical opposite declaration: {name}")
        c.equal(required_dlc.get(name), native["required_dlc"], f"canonical DLC declaration: {name}")
        forbidden = "ethic_gestalt_consciousness" in native["forbidden_ethics"]
        c.require(not forbidden or individual, f"canonical forbidden ethic omitted: {name}")
        if individual and not forbidden:
            conservative.append(name)
    c.require(set(required_dlc) <= set(names), "DLC map contains unknown candidate")
    return conservative


def guard_fixture(definitions, *, traits=(), archetype="MACHINE", gestalt=False, dlcs=(), food=True, population=100):
    """Independent populated domestic template; no candidate eligibility override."""
    c = feedback_validator()
    country = c.Scope(kind="country", gestalt=gestalt, food=food,
                      flags={"shishan_code_reward_pending"})
    species = c.Scope(kind="species", owner=country, traits=set(traits), archetype=archetype)
    country.main_species = species
    country.species_templates = [species]
    group = c.Scope(kind="pop_group", owner=country, species=species, traits=species.traits, population=population)
    country.groups = [group]
    interpreter = c.Effects(definitions, host_dlcs=set(dlcs))
    interpreter.root = country
    return interpreter, country, species, group


def check_emitted_guards(canonical: dict, definitions, robotic) -> dict:
    """Check actual eligibility, claim guards, per-template grant and coverage."""
    c = feedback_validator()
    coverage = c.block(c.one(definitions, "shishan_code_reward_coverage_effect"))
    coverage_ifs = [entry for entry in coverage if entry.key == "if"]
    c.equal(len(coverage_ifs), 39, "coverage candidate guards")
    cases = 0
    for index, (name, _, individual, food_only) in enumerate(robotic, 1):
        native = canonical["traits"][name]
        eligibility = c.block(c.one(definitions, f"shishan_code_reward_eligible_{index:02d}"))
        claim = c.block(c.one(definitions, f"shishan_code_reward_claim_{index:02d}_effect"))
        claim_branch = c.block(c.one(claim, "if"))
        claim_country = c.block(c.one(claim_branch, "limit"))
        grant = c.block(c.one(claim_branch, "every_owned_pop_group"))
        grant_limit = c.block(c.one(grant, "limit"))
        recheck = c.block(c.one(grant, "if"))
        template = c.block(c.one(recheck, "limit"))
        cover = c.block(c.one(c.block(coverage_ifs[index - 1].value), "every_owned_pop_group"))
        cover_limit = c.block(c.one(cover, "limit"))
        required_dlcs = {native["required_dlc"]} if native["required_dlc"] else set()
        scenarios = [("eligible machine", {}, True, True),
                     ("eligible robot", {"archetype": "ROBOT"}, True, True),
                     ("wrong archetype", {"archetype": "BIOLOGICAL"}, False, False),
                     ("already owned", {"traits": {name}}, False, False),
                     ("empty template", {"population": 0}, False, False)]
        scenarios.extend(("canonical conflict " + opposite, {"traits": {opposite}}, False, False) for opposite in native["opposites"])
        if required_dlcs:
            scenarios.append(("missing required DLC", {"dlcs": set()}, False, True))
        if individual:
            scenarios.append(("forbidden or conservative gestalt", {"gestalt": True}, False, True))
        else:
            scenarios.append(("eligible machine intelligence", {"gestalt": True}, True, True))
        if food_only:
            scenarios.append(("food economy absent", {"food": False}, False, True))
        for label, changes, expected_country, expected_template in scenarios:
            settings = {"dlcs": required_dlcs, **changes}
            engine, country, species, group = guard_fixture(definitions, **settings)
            country.variables["shishan_code_reward_slot_1"] = index
            c.equal(engine.trigger(eligibility, country), expected_country, f"actual eligibility {name}: {label}")
            c.equal(engine.trigger(claim_country, country), expected_country, f"actual claim country guard {name}: {label}")
            c.equal(engine.scoped_trigger(grant_limit, group, country), expected_template, f"actual claim population guard {name}: {label}")
            c.equal(engine.scoped_trigger(template, group, country), expected_template, f"actual claim template guard {name}: {label}")
            c.equal(engine.scoped_trigger(cover_limit, group, country), expected_template, f"actual coverage guard {name}: {label}")
            cases += 1
    return {"deterministic_scenarios": cases, "guard_assertions": cases * 5,
            "eligibility_overrides": False, "cloning_engine": "NOT RUN"}


def audit_vanilla_candidates(game: Path, mod: Path | None = None) -> dict:
    c = feedback_validator()
    paths = sorted((game / "common/traits").glob("*.txt"))
    c.require(bool(paths), f"no installed vanilla traits: {game}")
    sources = [(str(path), path.read_text(encoding="utf-8-sig")) for path in paths]
    canonical = canonical_traits(sources, [item[0] for item in ROBOTIC])
    canonical["source_sha256"] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    c.equal(len(ROBOTIC), 20, "robotic pool size")
    conservative = check_declarations(canonical, ROBOTIC, ROBOTIC_REQUIRED_DLC)
    mod = OUTPUT.parents[2] if mod is None else mod
    definitions = c.load_definitions(mod, "scripted_effects") + c.load_definitions(mod, "scripted_triggers")
    result = check_emitted_guards(canonical, definitions, ROBOTIC)
    return {"status": "PASS", "scope": "STATIC/OFFLINE ONLY", "canonical": canonical,
            "conservative_gestalt_filters": conservative, "emitted_guards": result,
            "native_species_potential": "machine-owner OR alternatives checked; editor technology/FROM alternatives not executed",
            "runtime": "NOT RUN"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", required=True, type=Path)
    parser.add_argument("--mod", type=Path, default=OUTPUT.parents[2])
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = audit_vanilla_candidates(args.game, args.mod)
    result["reward_contract"] = feedback_validator().check_rewards(args.mod)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("reward contract: PASS (static/offline AST only; "
          f"{len(result['canonical']['traits'])} vanilla robotic positives; "
          f"{result['canonical']['files']} native trait files; "
          f"{result['emitted_guards']['guard_assertions']} deterministic guard assertions; "
          f"{result['reward_contract']['seeded_candidate_cases']} seeded candidate cases; "
          "cooldown 3 -> 2 -> 1 -> 0; engine runtime NOT RUN)")


if __name__ == "__main__":
    main()
