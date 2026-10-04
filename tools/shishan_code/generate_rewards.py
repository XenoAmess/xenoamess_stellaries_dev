"""Generate the audited, ordered species-trait reward pools for Stellaris 4.5.1.

The lists contain ordinary vanilla positives with modifiers that function for a
machine pop/leader. Story, ascension, DLC-special, habitability-at-100%, and
organic growth traits are deliberately absent. The organic pool is reached only
after the robotic pool has no eligible entry.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "shishan_code_origin/mod/common/scripted_effects/shishan_code_rewards.txt"
TRIGGERS = ROOT / "shishan_code_origin/mod/common/scripted_triggers/shishan_code_rewards.txt"
EVENTS = ROOT / "shishan_code_origin/mod/events/shishan_code_rewards_events.txt"
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


def species_condition(item: tuple[str, list[str], bool, bool], compatible: bool = False) -> str:
    name, opposite, individual, food = item
    excluded = [name, *opposite]
    if compatible:
        excluded.append(compatible_name(name))
        other_names = {entry[0] for entry in OTHER}
        excluded.extend(compatible_name(entry) for entry in opposite if entry in other_names)
    return "NOR = { " + " ".join("has_trait = " + n for n in dict.fromkeys(excluded)) + " }"


def condition(item: tuple[str, list[str], bool, bool], compatible: bool = False) -> str:
    _, _, individual, food = item
    checks = [
        "any_owned_species = { is_same_species = prev " + species_condition(item, compatible)
        + " prev = { any_owned_pop_group = { is_exact_same_species = prevprev pop_amount > 0 } } }"
    ]
    if individual:
        checks.append("NOT = { has_ethic = ethic_gestalt_consciousness }")
    if food:
        checks.append("country_uses_food = yes")
    return " ".join(checks)


ENTRIES = [(index, item, False, 1) for index, item in enumerate(ROBOTIC, 1)] + [
    (index, item, True, 2) for index, item in enumerate(OTHER, len(ROBOTIC) + 1)
]


def eligible(index: int) -> str:
    return f"shishan_code_reward_eligible_{index:02d} = yes"


def has_candidate(index: int) -> str:
    return "OR = { " + " ".join(
        f"check_variable = {{ which = shishan_code_reward_slot_{slot} value = {index} }}"
        for slot in (1, 2, 3)
    ) + " }"


def available(index: int, tier: int, fresh: bool = False) -> str:
    clauses = [eligible(index), f"check_variable = {{ which = shishan_code_reward_tier value = {tier} }}"]
    clauses.extend(
        f"NOT = {{ check_variable = {{ which = shishan_code_reward_slot_{slot} value = {index} }} }}"
        for slot in (1, 2, 3)
    )
    if fresh:
        clauses.extend(
            f"NOT = {{ check_variable = {{ which = shishan_code_reward_old_{slot} value = {index} }} }}"
            for slot in (1, 2, 3)
        )
    return " ".join(clauses)


def any_available(fresh: bool = False) -> str:
    return "OR = { " + " ".join(f"AND = {{ {available(i, tier, fresh)} }}" for i, _, _, tier in ENTRIES) + " }"


def random_draw(slot: int, fresh: bool = False) -> str:
    draws = ["random_list = {"]
    for index, _, _, tier in ENTRIES:
        draws.append(
            f"1 = {{ modifier = {{ factor = 0 NOT = {{ {available(index, tier, fresh)} }} }} "
            f"set_variable = {{ which = shishan_code_reward_slot_{slot} value = {index} }} }}"
        )
    draws.append("}")
    return "\n".join(draws)


def zeros(prefix: str) -> str:
    return "\n".join(f"set_variable = {{ which = {prefix}_{slot} value = 0 }}" for slot in (1, 2, 3))


def generate_scripts() -> tuple[str, str, str]:
    triggers = ["# Generated by tools/shishan_code/generate_rewards.py; do not hand edit."]
    for index, item, compatible, _ in ENTRIES:
        triggers.append(f"shishan_code_reward_eligible_{index:02d} = {{ {condition(item, compatible)} }}")
    triggers.append("shishan_code_reward_can_reroll = {\n"
                    "has_origin = origin_shishan_code\nhas_country_flag = shishan_code_reward_pending\n"
                    "NOT = { has_country_flag = shishan_code_reward_rerolled }\n"
                    "check_variable = { which = shishan_code_reroll_cooldown value = 0 }\n"
                    + any_available() + "\n}")

    effects = ["# Generated by tools/shishan_code/generate_rewards.py; country scope."]
    effects.append("shishan_code_reward_initialize_effect = {\n"
                   "if = { limit = { NOT = { is_variable_set = shishan_code_reroll_cooldown } }\n"
                   "set_variable = { which = shishan_code_reroll_cooldown value = 0 } }\n}")
    effects.append("shishan_code_reward_open_window_effect = {\n"
                   "if = { limit = { has_origin = origin_shishan_code has_country_flag = shishan_code_reward_pending "
                   "NOT = { has_country_flag = shishan_code_reward_window_open } }\n"
                   "set_country_flag = shishan_code_reward_window_open\n"
                   "country_event = { id = shishan_code.1000 } }\n}")
    tier_one = "OR = { " + " ".join(eligible(i) for i, _, _, tier in ENTRIES if tier == 1) + " }"
    tier_two = "OR = { " + " ".join(eligible(i) for i, _, _, tier in ENTRIES if tier == 2) + " }"
    effects.append("shishan_code_reward_choose_tier_effect = {\n"
                   f"if = {{ limit = {{ {tier_one} }} set_variable = {{ which = shishan_code_reward_tier value = 1 }} }}\n"
                   f"else_if = {{ limit = {{ {tier_two} }} set_variable = {{ which = shishan_code_reward_tier value = 2 }} }}\n"
                   "else = { set_variable = { which = shishan_code_reward_tier value = 0 } }\n}")
    for slot in (1, 2, 3):
        effects.append(f"shishan_code_reward_pick_{slot}_effect = {{\n"
                       f"if = {{ limit = {{ has_country_flag = shishan_code_reward_prefer_new {any_available(True)} }}\n"
                       + random_draw(slot, True) + "\n}\n"
                       f"else_if = {{ limit = {{ {any_available()} }}\n" + random_draw(slot) + "\n}\n}")

    # Pure redraw helper: only award/reroll callers may clear an entire group.
    effects.append("shishan_code_reward_draw_effect = {\n" + zeros("shishan_code_reward_slot") + "\n"
                   + "\n".join(f"shishan_code_reward_pick_{s}_effect = yes" for s in (1, 2, 3)) + "\n}")
    effects.append("shishan_code_award_reward = {\nif = { limit = {\n"
                   "has_origin = origin_shishan_code\nhas_country_flag = shishan_code_reward_ticket_ready\n"
                   "NOT = { has_country_flag = shishan_code_reward_pending } }\n"
                   "remove_country_flag = shishan_code_reward_ticket_ready\n"
                   "shishan_code_reward_initialize_effect = yes\n"
                   "remove_country_flag = shishan_code_reward_rerolled\n"
                   "remove_country_flag = shishan_code_reward_prefer_new\n" + zeros("shishan_code_reward_old") + "\n"
                   "shishan_code_reward_choose_tier_effect = yes\n"
                   "if = { limit = { check_variable = { which = shishan_code_reward_tier value > 0 } }\n"
                   "set_country_flag = shishan_code_reward_pending\nshishan_code_reward_draw_effect = yes\n"
                   "shishan_code_reward_open_window_effect = yes }\n"
                   "else = { shishan_code_architecture_award_repeat_effect = yes country_event = { id = shishan_code.1002 } }\n}\n}")

    effects.append("shishan_code_reward_finish_effect = {\n"
                   "remove_country_flag = shishan_code_reward_pending\n"
                   "remove_country_flag = shishan_code_reward_window_open\n"
                   "remove_country_flag = shishan_code_reward_rerolled\n"
                   "remove_country_flag = shishan_code_reward_prefer_new\n"
                   + zeros("shishan_code_reward_slot") + "\n" + zeros("shishan_code_reward_old") + "\n"
                   "shishan_code_architecture_refresh_effect = yes\ncountry_event = { id = shishan_code.11 days = 1 }\n}")
    for index, item, compatible, _ in ENTRIES:
        trait = compatible_name(item[0]) if compatible else item[0]
        effects.append(f"shishan_code_reward_claim_{index:02d}_effect = {{\n"
                       "remove_country_flag = shishan_code_reward_window_open\n"
                       f"if = {{ limit = {{ has_origin = origin_shishan_code has_country_flag = shishan_code_reward_pending {has_candidate(index)} {eligible(index)} }}\n"
                       "save_event_target_as = shishan_code_reward_country\n"
                       "every_owned_species = { limit = { is_same_species = prev " + species_condition(item, compatible)
                       + " prev = { any_owned_pop_group = { is_exact_same_species = prevprev pop_amount > 0 } } }\n"
                       f"shishan_code_modify_domestic_template_effect = {{ ADD_TRAIT = {trait} }} }}\n"
                       "if = { limit = { check_variable = { which = shishan_code_reroll_cooldown value > 0 } }\n"
                       "change_variable = { which = shishan_code_reroll_cooldown value = -1 } }\n"
                       "shishan_code_reward_finish_effect = yes\ncountry_event = { id = shishan_code.1003 }\n}\n}")

    # Invalidate only the affected slot; preserved candidates never get redrawn.
    refresh = ["shishan_code_reward_refresh_effect = {", "shishan_code_reward_initialize_effect = yes",
               "if = { limit = { has_origin = origin_shishan_code has_country_flag = shishan_code_reward_pending }"]
    for slot in (1, 2, 3):
        for index, _, _, _ in ENTRIES:
            refresh.append(f"if = {{ limit = {{ check_variable = {{ which = shishan_code_reward_slot_{slot} value = {index} }} NOT = {{ {eligible(index)} }} }} "
                           f"set_variable = {{ which = shishan_code_reward_slot_{slot} value = 0 }} }}")
    refresh.append("if = { limit = { " + " ".join(f"check_variable = {{ which = shishan_code_reward_slot_{s} value = 0 }}" for s in (1, 2, 3))
                   + " } shishan_code_reward_choose_tier_effect = yes }")
    for slot in (1, 2, 3):
        refresh.append(f"if = {{ limit = {{ check_variable = {{ which = shishan_code_reward_slot_{slot} value = 0 }} }} shishan_code_reward_pick_{slot}_effect = yes }}")
    refresh.append("if = { limit = { check_variable = { which = shishan_code_reward_tier value = 0 } }\n"
                   "shishan_code_architecture_award_repeat_effect = yes\nshishan_code_reward_finish_effect = yes\ncountry_event = { id = shishan_code.1002 } }")
    refresh.extend(["}", "}"])
    effects.append("\n".join(refresh))

    reroll = ["shishan_code_reward_reroll_effect = {", "remove_country_flag = shishan_code_reward_window_open",
              "if = { limit = { shishan_code_reward_can_reroll = yes }"]
    for slot in (1, 2, 3):
        reroll.append(f"set_variable = {{ which = shishan_code_reward_old_{slot} value = this.shishan_code_reward_slot_{slot} }}")
    reroll.extend(["set_country_flag = shishan_code_reward_rerolled", "set_country_flag = shishan_code_reward_prefer_new",
                   "set_variable = { which = shishan_code_reroll_cooldown value = 3 }", "shishan_code_reward_draw_effect = yes",
                   "remove_country_flag = shishan_code_reward_prefer_new", "remove_country_flag = shishan_code_reward_window_open",
                   "shishan_code_reward_open_window_effect = yes", "}", "}"])
    effects.append("\n".join(reroll))

    coverage = ["shishan_code_reward_coverage_effect = {", "shishan_code_architecture_refresh_effect = yes"]
    for index, item, compatible, _ in ENTRIES:
        var = f"shishan_code_reward_coverage_{index:02d}"
        coverage.extend([f"set_variable = {{ which = {var} value = 0 }}", f"if = {{ limit = {{ {has_candidate(index)} }}",
                         "every_owned_pop_group = { limit = { is_same_species = prev pop_amount > 0 species = { " + species_condition(item, compatible) + " } }",
                         f"prev = {{ change_variable = {{ which = {var} value = prev.trigger:pop_amount }} }} }}",
                         "if = { limit = { check_variable = { which = shishan_code_architecture_population value > 0 } }",
                         f"divide_variable = {{ which = {var} value = this.shishan_code_architecture_population }}",
                         f"multiply_variable = {{ which = {var} value = 100 }}", "}", "}"])
    coverage.append("}")
    effects.append("\n".join(coverage))

    events = ["# Generated by tools/shishan_code/generate_rewards.py.", "namespace = shishan_code",
              "country_event = {", "id = shishan_code.1000", "title = shishan_code_reward_title", "desc = shishan_code_reward_desc",
              "picture = GFX_shishan_event", "is_triggered_only = yes",
              "trigger = { has_origin = origin_shishan_code has_country_flag = shishan_code_reward_pending has_country_flag = shishan_code_reward_window_open }",
              "immediate = { shishan_code_reward_refresh_effect = yes shishan_code_reward_coverage_effect = yes }"]
    for index, _, _, _ in ENTRIES:
        events.extend(["option = {", f"name = shishan_code_reward_option_{index:02d}",
                       f"trigger = {{ has_country_flag = shishan_code_reward_pending {has_candidate(index)} }}",
                       f"custom_tooltip = shishan_code_reward_option_{index:02d}_tooltip", "ai_chance = { factor = 1 }",
                       f"shishan_code_reward_claim_{index:02d}_effect = yes", "}"])
    events.extend(["option = { name = shishan_code_reward_reroll",
                   "allow = { custom_tooltip = { fail_text = shishan_code_reward_reroll_unavailable shishan_code_reward_can_reroll = yes } }",
                   "ai_chance = { factor = 0 } shishan_code_reward_reroll_effect = yes }",
                   "option = { name = shishan_code_reward_later ai_chance = { factor = 0 } remove_country_flag = shishan_code_reward_window_open }", "}",
                   "country_event = { id = shishan_code.1001 title = shishan_code_architecture_title desc = shishan_code_architecture_summary",
                   "picture = GFX_shishan_event is_triggered_only = yes trigger = { has_origin = origin_shishan_code }",
                   "immediate = { shishan_code_architecture_refresh_effect = yes }",
                   "option = { name = shishan_code_feedback_close } }",
                   "country_event = { id = shishan_code.1002 title = shishan_code_architecture_title desc = shishan_code_reward_repeat_result",
                   "picture = GFX_shishan_event is_triggered_only = yes trigger = { has_origin = origin_shishan_code }",
                   "option = { name = shishan_code_feedback_close } }",
                   "country_event = { id = shishan_code.1003 title = shishan_code_architecture_title desc = shishan_code_architecture_summary",
                   "picture = GFX_shishan_event is_triggered_only = yes trigger = { has_origin = origin_shishan_code }",
                   "option = { name = shishan_code_feedback_close } }", ""])
    return "\n\n".join(effects) + "\n", "\n\n".join(triggers) + "\n", "\n".join(events)


def main() -> None:
    for path, source in zip((OUTPUT, TRIGGERS, EVENTS), generate_scripts(), strict=True):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8", newline="\n")
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
        path.write_text("\n".join(references) + "\n", encoding="utf-8-sig", newline="\n")
        reward_references = [f"l_{language}:"]
        for index, item, compatible, _ in ENTRIES:
            trait = compatible_name(item[0]) if compatible else item[0]
            reward_references.append(f' shishan_code_reward_option_{index:02d}:0 "${trait}$"')
            reward_references.append(
                f' shishan_code_reward_option_{index:02d}_tooltip:0 "${trait}_desc$\\n'
                f'$shishan_code_reward_claim_tooltip$\\n$shishan_code_reward_coverage_label$ '
                f'[Root.shishan_code_reward_coverage_{index:02d}]%"'
            )
        (directory / f"shishan_code_rewards_l_{language}.yml").write_text("\n".join(reward_references) + "\n", encoding="utf-8-sig", newline="\n")


if __name__ == "__main__":
    main()
