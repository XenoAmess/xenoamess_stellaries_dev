"""Field-controlled clone fixture regressions, without native engine claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("shishan_clone_checks", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py")
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)
MOD = ROOT / "shishan_code_origin/mod"


def fixture_script():
    source = '''shishan_code_apply_domestic_template_effect={
        every_owned_pop_group={limit={is_exact_same_species=event_target:shishan_code_reward_old_species pop_group_size>0} change_species=event_target:shishan_code_reward_new_species}
        every_owned_leader={limit={is_exact_same_species=event_target:shishan_code_reward_old_species} change_species=event_target:shishan_code_reward_new_species
            if={limit={has_leader_flag=shishan_code_vivhite} change_leader_portrait=shishan_code_vivhite}}
        every_envoy={limit={is_exact_same_species=event_target:shishan_code_reward_old_species} change_species=event_target:shishan_code_reward_new_species}
        if={limit={owner_main_species={is_exact_same_species=event_target:shishan_code_reward_old_species}}
            change_dominant_species={species=event_target:shishan_code_reward_new_species change_all=no}}
    }'''
    for name, changes in (("shishan_code_modify_domestic_template_effect", "add_trait=$ADD_TRAIT$"),
                          ("shishan_code_architecture_refactor_template_effect", "remove_trait=trait_shishan_code add_trait=trait_shishan_refactored"),
                          ("shishan_code_architecture_relapse_template_effect", "remove_trait=trait_shishan_refactored add_trait=trait_shishan_code")):
        source += f''' {name}={{
            save_event_target_as=shishan_code_reward_old_species
            modify_species={{species=this change_scoped_species=no inherit_parent_rights=yes {changes}
                effect={{save_event_target_as=shishan_code_reward_new_species}}}}
            if={{limit={{exists=event_target:shishan_code_reward_country}}
                event_target:shishan_code_reward_country={{shishan_code_apply_domestic_template_effect=yes}}}}
            else={{log="SHISHAN_CODE_TEMPLATE_COUNTRY_TARGET_MISSING"}}
        }}'''
    return source


class CloneFixtureTests(unittest.TestCase):
    def test_controlled_rights_domestic_foreign_identity_envoy_and_empty_target(self):
        result = c.check_domestic_template_model(c.parse(fixture_script()))
        self.assertEqual(9, result["field_controlled_scenarios"])
        self.assertEqual("NOT RUN", result["engine_rights_and_clone_behavior"])

    def test_missing_inheritance_really_uses_defaults_and_is_rejected(self):
        faulty = fixture_script().replace("inherit_parent_rights=yes", "")
        definitions = c.parse(faulty)
        engine, actor, _, main, _ = c.domestic_template_fixture(definitions)
        engine.event_targets["shishan_code_reward_country"] = actor
        engine.named("shishan_code_modify_domestic_template_effect", main, parameters={"ADD_TRAIT": "trait_added"})
        self.assertEqual({"citizenship": "purge", "living_standard": "subsistence"}, actor.species_rights[id(engine.clone_models[0])])
        with self.assertRaisesRegex(c.ContractError, "clone preserves explicit parent rights"):
            c.check_domestic_template_model(definitions)

    def test_missing_envoy_migration_really_leaves_old_template_and_is_rejected(self):
        faulty = fixture_script().replace("every_envoy={limit={is_exact_same_species=event_target:shishan_code_reward_old_species} change_species=event_target:shishan_code_reward_new_species}", "")
        definitions = c.parse(faulty)
        engine, actor, _, main, _ = c.domestic_template_fixture(definitions)
        engine.event_targets["shishan_code_reward_country"] = actor
        engine.named("shishan_code_modify_domestic_template_effect", main, parameters={"ADD_TRAIT": "trait_added"})
        self.assertIs(actor.envoys[0].species, main)
        with self.assertRaisesRegex(c.ContractError, "envoy domestic exact-template migration"):
            c.check_domestic_template_model(definitions)

    def test_missing_country_target_guard_raises_before_owner_main_species(self):
        faulty = fixture_script().replace("exists=event_target:shishan_code_reward_country", "always=yes")
        with self.assertRaisesRegex(c.ContractError, "unsupported/missing scope event_target:shishan_code_reward_country"):
            c.check_domestic_template_model(c.parse(faulty))

    def test_missing_country_target_is_diagnosed_without_applying_clone(self):
        definitions = c.parse(fixture_script())
        engine, actor, _, main, _ = c.domestic_template_fixture(definitions)
        engine.named("shishan_code_modify_domestic_template_effect", main, parameters={"ADD_TRAIT": "trait_added"})
        self.assertEqual(["SHISHAN_CODE_TEMPLATE_COUNTRY_TARGET_MISSING"], engine.logs)
        self.assertIs(actor.main_species, main)
        self.assertTrue(all(item.species is main for item in actor.envoys))

    def test_portrait_restore_is_observable_and_omission_rejected(self):
        faulty = fixture_script().replace("change_leader_portrait=shishan_code_vivhite", "")
        with self.assertRaisesRegex(c.ContractError, "special leader portrait retained"):
            c.check_domestic_template_model(c.parse(faulty))

    def test_shared_source_mutation_is_rejected(self):
        faulty = fixture_script().replace("change_scoped_species=no", "change_scoped_species=yes")
        with self.assertRaisesRegex(c.ContractError, "fixture requires isolated clone"):
            c.check_domestic_template_model(c.parse(faulty))

    def test_empty_country_target_diagnosis_must_exist(self):
        faulty = fixture_script().replace('log="SHISHAN_CODE_TEMPLATE_COUNTRY_TARGET_MISSING"', '')
        with self.assertRaisesRegex(c.ContractError, "missing target is guarded and diagnosed"):
            c.check_domestic_template_model(c.parse(faulty))


class EmittedCloneTests(unittest.TestCase):
    def test_actual_helpers_follow_domestic_rights_envoy_target_contract(self):
        result = c.check_domestic_templates(c.load_definitions(MOD, "scripted_effects"))
        self.assertEqual(9, result["clone_fixture"]["field_controlled_scenarios"])

    def test_actual_three_helpers_cannot_drop_inheritance(self):
        definitions = c.load_definitions(MOD, "scripted_effects")
        names = ("shishan_code_modify_domestic_template_effect", "shishan_code_architecture_refactor_template_effect", "shishan_code_architecture_relapse_template_effect")
        for name in names:
            def mutate(entries):
                return [c.Entry(e.key, e.op, mutate(e.value) if isinstance(e.value, list) else e.value) for e in entries if e.key != "inherit_parent_rights"]
            faulty = [c.Entry(e.key, e.op, mutate(e.value)) if e.key == name else e for e in definitions]
            with self.subTest(helper=name), self.assertRaisesRegex(c.ContractError, "parent rights"):
                c.check_domestic_template_model(faulty)


if __name__ == "__main__":
    unittest.main()
