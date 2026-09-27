"""Generate the audited, ordered species-trait reward pools for Stellaris 4.5.1.

The lists contain ordinary vanilla positives with modifiers that function for a
machine pop/leader. Story, ascension, DLC-special, habitability-at-100%, and
organic growth traits are deliberately absent. The organic pool is reached only
after the robotic pool has no eligible entry.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "shishan_code_origin/mod/common/scripted_effects/shishan_code_effects.txt"
LOCALIZATION = ROOT / "shishan_code_origin/mod/localisation"

# (trait, incompatible traits, individual-only, food-economy-only)
ROBOTIC = [
    ("trait_robot_power_drills", [], False, False),
    ("trait_robot_harvesters", [], False, True),
    ("trait_robot_superconductive", [], False, False),
    ("trait_robot_efficient_processors", [], False, False),
    ("trait_robot_logic_engines", [], False, False),
    ("trait_robot_loyalty_circuits", [], True, False),
    ("trait_robot_double_jointed", ["trait_robot_bulky", "trait_interconnected"], False, False),
    ("trait_robot_enhanced_memory", [], False, False),
    ("trait_robot_emotion_emulators", ["trait_robot_uncanny"], False, False),
    ("trait_robot_durable", ["trait_robot_high_maintenance"], False, False),
    ("trait_robot_learning_algorithms", ["trait_robot_repurposed_hardware"], False, False),
    ("trait_robot_mass_produced", ["trait_robot_custom_made"], False, False),
    ("trait_robot_recycled", ["trait_robot_luxurious"], False, False),
    ("trait_robot_propaganda_machines", [], True, False),
    ("trait_robot_streamlined_protocols", ["trait_robot_high_bandwidth"], False, False),
    ("trait_robot_trading_algorithms", [], True, False),
    ("trait_robot_artificial_engineers", [], False, False),
    ("trait_robot_artificial_physicists", [], False, False),
    ("trait_robot_artificial_sociologists", [], False, False),
    ("trait_robot_integrated_weaponry", [], False, False),
]

OTHER = [
    ("trait_agrarian", [], False, True),
    ("trait_ingenious", [], False, False),
    ("trait_industrious", [], False, False),
    ("trait_intelligent", ["trait_nerve_stapled", "trait_erudite", "trait_enigmatic_intelligence_poor"], False, False),
    ("trait_thrifty", ["trait_cyborg_scarcity_algorithms"], True, False),
    ("trait_natural_engineers", ["trait_natural_physicists", "trait_natural_sociologists", "trait_nerve_stapled", "trait_recursive_learners"], False, False),
    ("trait_natural_physicists", ["trait_natural_engineers", "trait_natural_sociologists", "trait_nerve_stapled", "trait_camouflage", "trait_chromalogs", "trait_recursive_learners"], False, False),
    ("trait_natural_sociologists", ["trait_natural_engineers", "trait_natural_physicists", "trait_nerve_stapled", "trait_recursive_learners"], False, False),
    ("trait_talented", ["trait_nerve_stapled", "trait_syncretic_proles"], False, False),
    ("trait_quick_learners", ["trait_slow_learners", "trait_syncretic_proles"], False, False),
    ("trait_traditional", ["trait_quarrelsome"], False, False),
    ("trait_docile", ["trait_unruly"], False, False),
    ("trait_strong", ["trait_weak", "trait_very_strong", "trait_hollow_bones"], False, False),
    ("trait_very_strong", ["trait_weak", "trait_strong", "trait_hollow_bones"], False, False),
    ("trait_nomadic", ["trait_sedentary", "trait_rooted", "trait_wilderness"], False, False),
    ("trait_communal", ["trait_solitary", "trait_shelled", "trait_spatial_mastery"], False, False),
    ("trait_charismatic", ["trait_repugnant", "trait_reavers"], False, False),
    ("trait_resilient", ["trait_pc_ark_preference"], False, False),
    ("trait_conservational", ["trait_wasteful", "trait_hive_mind"], True, False),
]


def compatible_name(name: str) -> str:
    return "trait_shishan_compat_" + name.removeprefix("trait_")


def condition(item: tuple[str, list[str], bool, bool], compatible: bool = False) -> str:
    name, opposite, individual, food = item
    excluded = [name, *opposite]
    if compatible:
        excluded.append(compatible_name(name))
        other_names = {entry[0] for entry in OTHER}
        excluded.extend(compatible_name(entry) for entry in opposite if entry in other_names)
    checks = [f"owner_main_species = {{ NOR = {{ {' '.join('has_trait = ' + n for n in dict.fromkeys(excluded))} }} }}"]
    if individual:
        checks.append("NOT = { has_ethic = ethic_gestalt_consciousness }")
    if food:
        checks.append("country_uses_food = yes")
    return " ".join(checks)


def generate_pool(items: list[tuple[str, list[str], bool, bool]], compatible: bool = False) -> list[str]:
    lines = ["\tOR = {"]
    lines.extend(f"\t\tAND = {{ {condition(item, compatible)} }}" for item in items)
    lines.extend(["\t}", "\trandom_list = {"])
    for item in items:
        name = compatible_name(item[0]) if compatible else item[0]
        lines.extend([
            "\t\t1 = {",
            f"\t\t\tmodifier = {{ factor = 0 NOT = {{ {condition(item, compatible)} }} }}",
            f"\t\t\towner_main_species = {{ change_species_characteristics = {{ add_trait = {name} }} }}",
            "\t\t}",
        ])
    lines.append("\t}")
    return lines


def main() -> None:
    existing = OUTPUT.read_text(encoding="utf-8")
    prefix = existing.split("\nshishan_code_award_reward = {", 1)[0].rstrip()
    robotic = generate_pool(ROBOTIC)
    other = generate_pool(OTHER, compatible=True)
    lines = [prefix, "", "shishan_code_award_reward = {", "\tif = {", "\t\tlimit = { "+robotic[0].strip()]
    lines.extend("\t" + line for line in robotic[1:robotic.index("\trandom_list = {")])
    lines.append("\t\t}" )
    lines.extend("\t" + line for line in robotic[robotic.index("\trandom_list = {"):])
    lines.extend(["\t}", "\telse_if = {", "\t\tlimit = { "+other[0].strip()])
    lines.extend("\t" + line for line in other[1:other.index("\trandom_list = {")])
    lines.append("\t\t}")
    lines.extend("\t" + line for line in other[other.index("\trandom_list = {"):])
    lines.extend(["\t}", "\telse = {", "\t\trandom_list = {"])
    for suffix in ("output", "energy", "assembly", "experience"):
        lines.append(
            "\t\t\t1 = { change_variable = { which = shishan_code_iteration_"
            + suffix
            + " value = 1 } owner_main_species = { change_species_characteristics = { add_trait = trait_shishan_iteration_"
            + suffix
            + " } } }"
        )
    lines.extend(["\t\t}", "\t}", "}", ""])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    # The compatibility traits reuse each official language's vanilla name and
    # description. They add no untranslated prose to the MiniMax corpus.
    for directory in LOCALIZATION.iterdir():
        if not directory.is_dir():
            continue
        language = directory.name
        path = directory / f"shishan_code_compat_l_{language}.yml"
        references = [f"l_{language}:"]
        for original, *_ in OTHER:
            mapped = compatible_name(original)
            references.append(f' {mapped}:0 "${original}$"')
            references.append(f' {mapped}_desc:0 "${original}_desc$"')
        path.write_text("\n".join(references) + "\n", encoding="utf-8-sig")


if __name__ == "__main__":
    main()
