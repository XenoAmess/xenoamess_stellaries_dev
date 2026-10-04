"""Non-GUI checks and independently constructed negative contract examples."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py"
SPEC = importlib.util.spec_from_file_location("feedback_redesign_checks", MODULE_PATH)
checks = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checks
SPEC.loader.exec_module(checks)
MOD = ROOT / "shishan_code_origin/mod"


class ParserTests(unittest.TestCase):
    def test_repeated_entries_bare_members_comments_and_comparisons_preserved(self):
        parsed = checks.parse('thing={ add=1 add=2 tags={ positive hidden } check={ value>=3 } text="a#b" } # comment\n')
        body = checks.block(checks.one(parsed, "thing"))
        self.assertEqual(["add", "add", "tags", "check", "text"], [entry.key for entry in body])
        self.assertEqual(["positive", "hidden"], [entry.key for entry in checks.block(checks.one(body, "tags"))])
        self.assertEqual(">=", checks.block(checks.one(body, "check"))[0].op)

    def test_bad_braces_missing_value_and_duplicate_definition_fail(self):
        for source in ("thing={ base=1", "thing=}", "}", "thing={ =1 }"):
            with self.subTest(source=source), self.assertRaises(checks.ContractError):
                checks.parse(source)
        with self.assertRaisesRegex(checks.ContractError, "exactly one"):
            checks.one(checks.parse("a=1 a=2"), "a")

    def test_unknown_arithmetic_and_trigger_fail_closed(self):
        with self.assertRaisesRegex(checks.ContractError, "unsupported"):
            checks.Values(checks.parse("v={ base=1 mystery=4 }")).named("v")
        with self.assertRaisesRegex(checks.ContractError, "unsupported"):
            checks.Effects([]).trigger(checks.parse("mystery=yes"), checks.Scope())
        with self.assertRaisesRegex(checks.ContractError, "unsupported"):
            checks.Effects([]).execute(checks.parse("mystery=yes"), checks.Scope())


class ArithmeticTests(unittest.TestCase):
    # Constructed from prose contract, independent of production generators.
    SOURCE = """
    count_step = { base=0 add=owner.shishan_code_maintenance_count mult=0.25 }
    reduction = { base=0
      complex_trigger_modifier={ trigger=num_assigned_jobs trigger_scope=owner parameters={job=shishan_code_maintainer} mode=add }
      complex_trigger_modifier={ trigger=num_assigned_jobs trigger_scope=owner parameters={job=shishan_code_maintainer_drone} mode=add }
      divide=100 floor=yes mult=0.25 }
    monthly = { base=1 add=value:count_step subtract=value:reduction min=0.2 }
    """

    def test_independent_boundary_and_cross_job_examples(self):
        ast = checks.parse(self.SOURCE)
        for n, human, drone, expected in ((0, 0, 0, "1"), (0, 99, 0, "1"), (0, 100, 0, ".75"), (0, 50, 50, ".75"), (0, 99, 1, ".75"), (0, 400, 0, ".2"), (5, 0, 0, "2.25"), (5, 700, 0, ".5"), (5, 900, 0, ".2")):
            with self.subTest(n=n, human=human, drone=drone):
                result = checks.Values(ast, {"shishan_code_maintenance_count": n}, {"shishan_code_maintainer": human, "shishan_code_maintainer_drone": drone}).named("monthly")
                self.assertEqual(checks.Decimal(expected), result)

    def test_wrong_coefficient_or_floor_order_breaks_contract(self):
        wrong_coefficient = self.SOURCE.replace("mult=0.25", "mult=0.03")
        result = checks.Values(checks.parse(wrong_coefficient), {"shishan_code_maintenance_count": 1}).named("monthly")
        self.assertNotEqual(checks.Decimal("1.25"), result)
        wrong_floor = self.SOURCE.replace("divide=100 floor=yes", "floor=yes divide=100")
        result = checks.Values(checks.parse(wrong_floor), {"shishan_code_maintenance_count": 0}, {"shishan_code_maintainer": 99}).named("monthly")
        self.assertNotEqual(checks.Decimal(1), result)

    def test_paradox_min_is_lower_bound(self):
        self.assertEqual(checks.Decimal(".2"), checks.Values(checks.parse("v={base=-50 min=0.2}")).named("v"))
        self.assertEqual(checks.Decimal(50), checks.Values(checks.parse("v={base=50 min=0.2}")).named("v"))


class LocalisationNegativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.mod = Path(self.temp.name)
        self.key = "shishan_code_architecture_name"
        for language in checks.LANGUAGES:
            path = self.mod / "localisation" / language / "fixture.yml"
            path.parent.mkdir(parents=True)
            value = checks.FULL_NAME if language == "simp_chinese" else "Integrated legacy architecture"
            path.write_text(f'l_{language}:\n {self.key}:0 "{value}"\n shishan_code_fixture_desc:0 "${self.key}$"\n', encoding="utf-8-sig")

    def change(self, language, mutate):
        path = self.mod / "localisation" / language / "fixture.yml"
        path.write_text(mutate(path.read_text(encoding="utf-8-sig")), encoding="utf-8-sig")

    def test_complete_name_and_all_languages_pass_static_only(self):
        result = checks.check_localisation(self.mod)
        self.assertEqual(18, result["full_name_characters"])
        self.assertEqual(54, result["full_name_utf8_bytes"])
        self.assertEqual("out_of_scope", result["non_chinese_runtime"])

    def test_truncated_name_fails(self):
        self.change("simp_chinese", lambda text: text.replace(checks.FULL_NAME, checks.FULL_NAME[:-1]))
        with self.assertRaisesRegex(checks.ContractError, "name missing or truncated"):
            checks.check_localisation(self.mod)

    def test_missing_language_key_fails(self):
        self.change("german", lambda text: "\n".join(text.splitlines()[:-1]) + "\n")
        with self.assertRaisesRegex(checks.ContractError, "completeness"):
            checks.check_localisation(self.mod)

    def test_chinese_placeholder_fails(self):
        self.change("english", lambda text: text.replace("Integrated legacy architecture", checks.FULL_NAME))
        with self.assertRaisesRegex(checks.ContractError, "Chinese placeholder"):
            checks.check_localisation(self.mod)

    def test_duplicate_key_and_no_bom_fail(self):
        self.change("english", lambda text: text + f' {self.key}:0 "duplicate"\n')
        with self.assertRaisesRegex(checks.ContractError, "duplicate"):
            checks.check_localisation(self.mod)
        path = self.mod / "localisation/english/fixture.yml"
        path.write_text(f'l_english:\n {self.key}:0 "value"\n', encoding="utf-8")
        with self.assertRaisesRegex(checks.ContractError, "BOM"):
            checks.check_localisation(self.mod)

    def test_missing_internal_reference_fails(self):
        self.change("english", lambda text: text.replace(f"${self.key}$", "$shishan_code_missing$"))
        with self.assertRaisesRegex(checks.ContractError, "unresolved"):
            checks.check_localisation(self.mod)

    def test_reference_cycle_fails(self):
        self.change("english", lambda text: text.replace('"Integrated legacy architecture"', '"$shishan_code_fixture_desc$"'))
        with self.assertRaisesRegex(checks.ContractError, "cycle"):
            checks.check_localisation(self.mod)


class EmittedArtifactTests(unittest.TestCase):
    def test_actual_emitted_numeric_contract(self):
        checks.check_numeric(MOD)

    def test_actual_emitted_architecture_weight_migration_and_infinite_arithmetic(self):
        checks.check_architecture(MOD)

    def test_actual_emitted_reward_candidate_and_receipt_state(self):
        checks.check_rewards(MOD)

    def test_rejected_options_unlock_and_capital_wrapper_reopen(self):
        definitions = checks.load_definitions(MOD, "scripted_effects") + checks.load_definitions(MOD, "scripted_triggers")
        values = checks.load_definitions(MOD, "script_values")
        result = checks.check_reward_windows(MOD, definitions, values)
        self.assertEqual(2, result["rejected_option_unlock_and_reopen_cases"])

    def test_actual_emitted_receipt_reload_recovery_and_cross_state_queue(self):
        checks.check_receipt_recovery(MOD)

    def test_actual_eligibility_guards_without_override(self):
        definitions = checks.load_definitions(MOD, "scripted_effects") + checks.load_definitions(MOD, "scripted_triggers")
        values = checks.load_definitions(MOD, "script_values")
        interpreter, country = checks.reward_fixture(definitions, values, set(range(1, 40)))
        interpreter.trigger_overrides.clear()
        def eligible(index):
            return interpreter.trigger([checks.Entry(f"shishan_code_reward_eligible_{index:02d}", "=", "yes")], country)
        self.assertTrue(eligible(1))
        country.main_species.traits.add("trait_robot_power_drills")
        self.assertFalse(eligible(1))
        variant = checks.Scope(kind="species", owner=country, traits={"trait_shishan_code"})
        country.species_templates.append(variant)
        # An unapplied template does not make an already-owned reward eligible.
        self.assertFalse(eligible(1))
        group = checks.Scope(kind="pop_group", owner=country, species=variant, traits=variant.traits, population=200)
        country.groups.append(group)
        self.assertTrue(eligible(1))
        group.population = 0
        self.assertFalse(eligible(1))
        variant.lineage = "external"
        group.lineage = "external"
        group.population = 200
        self.assertFalse(eligible(1))
        country.food = False
        self.assertFalse(eligible(2))
        country.gestalt = True
        self.assertFalse(eligible(6))
        country.main_species.traits.add("trait_robot_bulky")
        self.assertFalse(eligible(7))
        country.main_species.traits.add("trait_agrarian")
        country.food = True
        self.assertFalse(eligible(21))
        country.main_species.traits.remove("trait_agrarian")
        country.main_species.traits.add("trait_shishan_compat_agrarian")
        self.assertFalse(eligible(21))

    def test_abstract_grant_fixture_keeps_foreign_shared_template(self):
        definitions = checks.load_definitions(MOD, "scripted_effects") + checks.load_definitions(MOD, "scripted_triggers")
        values = checks.load_definitions(MOD, "script_values")
        interpreter, country = checks.reward_fixture(definitions, values, {1, 2, 3, 4})
        old = country.main_species
        foreign_country = checks.Scope(origin="origin_default")
        shared_foreign = checks.Scope(kind="pop_group", owner=foreign_country, species=old, traits=old.traits, population=10000)
        country.groups.append(shared_foreign)
        before = set(old.traits)
        interpreter.named("shishan_code_award_reward", country)
        selected = next(index for index in checks.reward_slots(country) if index)
        interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
        self.assertEqual(before, shared_foreign.traits)
        self.assertIs(shared_foreign.species, old)
        self.assertIsNot(country.main_species, old)
        self.assertEqual(checks.Decimal(100), country.variables["shishan_code_architecture_population"])

    def test_actual_emitted_full_name_and_localisation(self):
        checks.check_localisation(MOD)

    def test_wrong_initial_speed_artifact_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/script_values/shishan_code_values.txt"
            text = path.read_text(encoding="utf-8")
            marker = "shishan_code_monthly_progress = {\n\tbase = 1"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "shishan_code_monthly_progress = {\n\tbase = 3"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "monthly n=0"):
                checks.check_numeric(candidate)

    def test_architecture_wrong_coefficient_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/script_values/shishan_code_architecture_values.txt"
            text = path.read_text(encoding="utf-8")
            self.assertIn("0.05", text)
            path.write_text(text.replace("0.05", "0.03"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "per trait"):
                checks.check_architecture(candidate)

    def test_migration_first_layer_double_count_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_architecture_effects.txt"
            text = path.read_text(encoding="utf-8")
            marker = "which = shishan_code_architecture_legacy_extra value = -1"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "which = shishan_code_architecture_legacy_extra value = 0"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "legacy repetitions"):
                checks.check_architecture(candidate)

    def test_shared_species_mutation_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_architecture_effects.txt"
            text = path.read_text(encoding="utf-8")
            self.assertIn("change_scoped_species = no", text)
            path.write_text(text.replace("change_scoped_species = no", "change_scoped_species = yes"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "shared source template"):
                checks.check_architecture(candidate)

    def test_additive_fallback_cannot_also_change_upkeep(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/static_modifiers/shishan_code_architecture_modifiers.txt"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("planet_jobs_produces_mult = 0.05", "planet_jobs_produces_mult = 0.05\n\tplanet_jobs_upkeep_mult = 0.05"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "additive-only"):
                checks.check_architecture(candidate)

    def test_duplicate_reward_candidates_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_rewards.txt"
            text = path.read_text(encoding="utf-8")
            def duplicate_slot(match):
                return match[0] if int(match[1]) == 0 else "set_variable = { which = shishan_code_reward_slot_2 value = this.shishan_code_reward_slot_1 }"
            text, count = checks.re.subn(r"set_variable = \{ which = shishan_code_reward_slot_2 value = (\d+) \}", duplicate_slot, text)
            self.assertGreater(count, 0)
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "uniqueness|candidate count"):
                checks.check_rewards(candidate)

    def test_wrong_reroll_cooldown_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_rewards.txt"
            text = path.read_text(encoding="utf-8")
            marker = "set_variable = { which = shishan_code_reroll_cooldown value = 3 }"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "set_variable = { which = shishan_code_reroll_cooldown value = 2 }"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "three-choice cooldown"):
                checks.check_rewards(candidate)

    def test_missing_window_lock_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_rewards.txt"
            text = path.read_text(encoding="utf-8")
            marker = "NOT = { has_country_flag = shishan_code_reward_window_open }"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "always = yes"), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "duplicate windows"):
                checks.check_rewards(candidate)

    def test_rejected_claim_missing_unlock_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_rewards.txt"
            text = path.read_text(encoding="utf-8")
            marker = "shishan_code_reward_claim_01_effect = {\nremove_country_flag = shishan_code_reward_window_open\n"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "shishan_code_reward_claim_01_effect = {\n", 1), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "rejected claim must release window lock"):
                checks.check_rewards(candidate)

    def test_rejected_reroll_missing_unlock_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "common/scripted_effects/shishan_code_rewards.txt"
            text = path.read_text(encoding="utf-8")
            marker = "shishan_code_reward_reroll_effect = {\nremove_country_flag = shishan_code_reward_window_open\n"
            self.assertIn(marker, text)
            path.write_text(text.replace(marker, "shishan_code_reward_reroll_effect = {\n", 1), encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "rejected reroll must release window lock"):
                checks.check_rewards(candidate)

    def test_missing_saved_success_recovery_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "mod"
            shutil.copytree(MOD, candidate)
            path = candidate / "events/shishan_code_events.txt"
            text = path.read_text(encoding="utf-8")
            prefix, recovery = text.split("country_event = {\n\tid = shishan_code.60", 1)
            marker = "country_event = { id = shishan_code.10 }"
            self.assertIn(marker, recovery)
            recovery = recovery.replace(marker, "country_event = { id = shishan_code.11 }", 1)
            path.write_text(prefix + "country_event = {\n\tid = shishan_code.60" + recovery, encoding="utf-8")
            with self.assertRaisesRegex(checks.ContractError, "receipt not recovered"):
                checks.check_receipt_recovery(candidate)


if __name__ == "__main__":
    unittest.main()
