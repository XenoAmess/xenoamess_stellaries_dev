"""Keep the real rc4 stale-cache counterexample and check rc5 pop-driven AST."""

from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path
import sys
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


c = module("cache_feedback_checks", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py")
reader = module("cache_native_reader", ROOT / "shishan_code_origin/tools/audit_feedback_runtime_save.py")
MOD = ROOT / "shishan_code_origin/mod"
NATIVE = ROOT / "_runtime/shishan_code/20261015-runtime/runs/20261015T080652Z/fb454_clean_pending.sav"
FROZEN = Path("C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T080652Z/mod/shishan-feedback-local")


@lru_cache(maxsize=1)
def native_inputs():
    """Read immutable raw input once; every execution builds fresh scopes."""
    with zipfile.ZipFile(NATIVE) as archive:
        doc = reader.Document(archive.read("gamestate").decode("utf-8-sig"))
    actor_id, raw, _ = reader.locate_player(doc)
    main_id, _ = reader.locate_main_species(doc, raw)
    records = reader.species_records(doc)
    population = reader.inspect_populations(doc, raw, actor_id, records, main_id)
    variables = reader.mod_fields(doc, doc.section(raw, "variables"))
    flags = reader.mod_fields(doc, doc.section(raw, "flags"))
    refs = reader.integer_list(doc, doc.section(raw, "owned_species_refs"), "saved cached species")
    return main_id, records, population, variables, flags, refs


def fixture(definitions, values, snapshot=True):
    """Actual cached refs and population/traits, explicit scope/rights fixtures."""
    main_id, records, population, variables, flags, refs = native_inputs()
    actor = c.Scope(variables={k: c.Decimal(v) for k, v in variables.items()}, flags=set(flags), lineage=str(records[main_id]["lineage_root"]),
                    default_rights={"citizenship": "purge"})
    species = {key: c.Scope(kind="species", owner=actor, lineage=str(value["lineage_root"]), traits=set(value["raw_trait_keys"]), archetype="MACHINE") for key, value in records.items()}
    actor.species_templates = [species[index] for index in refs]
    actor.main_species = species[main_id]
    actor.groups = [c.Scope(kind="pop_group", owner=actor, lineage=str(row["lineage_root"]), population=row["size"], species=species[row["species_id"]], traits=species[row["species_id"]].traits) for row in population["included_groups"]]
    for row in population["populated_templates"]:
        actor.species_rights[id(species[row["id"]])] = {"citizenship": "full"}
    # Explicit extra ownership and empty fixtures, not claimed saved records.
    foreign = c.Scope(origin="origin_default")
    actor.groups.extend([c.Scope(kind="pop_group", owner=foreign, lineage=actor.lineage, species=actor.main_species, traits=actor.main_species.traits, population=200),
                         c.Scope(kind="pop_group", owner=actor, lineage=actor.lineage, species=actor.main_species, traits=actor.main_species.traits, population=0)])
    actor.leaders = [c.Scope(kind="leader", owner=actor, species=actor.main_species, variables={"identity": 9, "experience": 90})]
    actor.envoys = [c.Scope(kind="envoy", owner=actor, species=actor.main_species, variables={"identity": 10})]
    engine = c.Effects(definitions, values, host_dlcs={"The Machine Age"}, snapshot_pop_group_limits=snapshot)
    engine.root = actor
    return engine, actor, population, refs


def change_recheck(definitions, key, path):
    def rewrite(entries, remaining):
        return [c.Entry(e.key, e.op, c.parse("always=yes") if len(remaining) == 1 else rewrite(e.value, remaining[1:])) if e.key == remaining[0] else e for e in entries]
    return [c.Entry(e.key, e.op, rewrite(e.value, path)) if e.key == key else e for e in definitions]


@unittest.skipUnless(NATIVE.is_file(), "real rc4 clean_pending native evidence required")
class NativeSpeciesCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definitions = c.load_definitions(MOD, "scripted_effects") + c.load_definitions(MOD, "scripted_triggers")
        cls.values = c.load_definitions(MOD, "script_values")

    def test_native_cache_and_actual_populations_remain_independent(self):
        engine, actor, population, refs = fixture(self.definitions, self.values)
        self.assertEqual([53, 54], refs)
        self.assertEqual({55, 56}, {r["id"] for r in population["populated_templates"]})
        self.assertEqual(5593, population["population"])
        self.assertEqual(50890, population["trait_weight"])
        self.assertEqual({}, engine.trigger_overrides)
        for index in (11, 9, 12):
            self.assertTrue(engine.trigger(c.block(c.one(self.definitions, f"shishan_code_reward_eligible_{index:02d}")), actor))

    def test_frozen_real_rc4_loses_legal_ticket_and_awards_repeat(self):
        if not FROZEN.is_dir():
            self.skipTest("frozen actual rc4 package unavailable")
        defs = c.load_definitions(FROZEN, "scripted_effects") + c.load_definitions(FROZEN, "scripted_triggers")
        vals = c.load_definitions(FROZEN, "script_values")
        engine, actor, _, _ = fixture(defs, vals)
        engine.named("shishan_code_reward_refresh_effect", actor)
        self.assertEqual(c.Decimal(1), actor.variables["shishan_code_architecture_repeat_count"])
        self.assertEqual((0, 0, 0), c.reward_slots(actor))
        self.assertNotIn("shishan_code_reward_pending", actor.flags)

    def test_new_refresh_keeps_same_legal_ticket_and_cooldown(self):
        engine, actor, _, _ = fixture(self.definitions, self.values)
        engine.named("shishan_code_reward_refresh_effect", actor)
        self.assertEqual((11, 9, 12), c.reward_slots(actor))
        self.assertEqual(c.Decimal(0), actor.variables["shishan_code_architecture_repeat_count"])
        self.assertEqual(c.Decimal(3), actor.variables["shishan_code_reroll_cooldown"])
        self.assertIn("shishan_code_reward_pending", actor.flags)

    def test_claim_clones_each_current_template_once_with_stale_refs(self):
        engine, actor, _, _ = fixture(self.definitions, self.values)
        refs = list(actor.species_templates)
        foreign = next(g for g in actor.groups if g.owner is not actor)
        old_foreign = foreign.species
        engine.named("shishan_code_reward_claim_09_effect", actor)
        self.assertEqual(2, len(engine.clone_models))
        self.assertEqual(refs, actor.species_templates)
        self.assertIs(old_foreign, foreign.species)
        self.assertEqual(c.Decimal(2), actor.variables["shishan_code_reroll_cooldown"])
        self.assertEqual(c.Decimal(4), actor.variables["shishan_code_maintenance_count"])
        self.assertEqual(c.Decimal(0), actor.variables["shishan_code_architecture_repeat_count"])
        self.assertEqual(c.Decimal(56483), actor.variables["shishan_code_architecture_trait_weight"])
        self.assertTrue(all("trait_robot_emotion_emulators" in g.species.traits for g in actor.groups if g.owner is actor and g.population > 0))

    def test_mixed_owned_trait_clones_only_one_uncovered_template(self):
        engine, actor, _, _ = fixture(self.definitions, self.values)
        engine.named("shishan_code_reward_claim_11_effect", actor)
        self.assertEqual(1, len(engine.clone_models))
        self.assertEqual(c.Decimal(55930), actor.variables["shishan_code_architecture_trait_weight"])

    def test_state_swaps_use_actual_groups_once_per_template_with_stale_refs(self):
        engine, actor, _, _ = fixture(self.definitions, self.values)
        engine.named("shishan_code_architecture_relapse_species_effect", actor)
        self.assertEqual(2, len(engine.clone_models))
        self.assertTrue(all("trait_shishan_code" in g.species.traits for g in actor.groups if g.owner is actor and g.population > 0))
        engine.named("shishan_code_architecture_refactor_species_effect", actor)
        self.assertEqual(4, len(engine.clone_models))
        self.assertTrue(all("trait_shishan_refactored" in g.species.traits for g in actor.groups if g.owner is actor and g.population > 0))
        self.assertEqual(c.Decimal(50890), actor.variables["shishan_code_architecture_trait_weight"])

    def test_missing_claim_inner_recheck_really_clones_repeated_templates(self):
        defs = change_recheck(self.definitions, "shishan_code_reward_claim_09_effect", ("if", "every_owned_pop_group", "if", "limit"))
        engine, actor, _, _ = fixture(defs, self.values)
        engine.named("shishan_code_reward_claim_09_effect", actor)
        self.assertGreater(len(engine.clone_models), 2)
        with self.assertRaisesRegex(c.ContractError, "claim rechecks current population"):
            c.check_claim_population_recheck(defs, 9)

    def test_missing_state_inner_recheck_really_clones_repeated_templates(self):
        defs = change_recheck(self.definitions, "shishan_code_architecture_relapse_species_effect", ("if", "every_owned_pop_group", "if", "limit"))
        engine, actor, _, _ = fixture(defs, self.values)
        engine.named("shishan_code_architecture_relapse_species_effect", actor)
        self.assertGreater(len(engine.clone_models), 2)
        with self.assertRaisesRegex(c.ContractError, "state rechecks current population"):
            c.check_domestic_templates(defs)

    def test_preflight_preserves_native_clean_ticket_without_empty_ui(self):
        engine, actor, _, _ = fixture(self.definitions, self.values)
        events = c.country_events(MOD)
        engine.named("shishan_code_reward_open_window_effect", actor)
        self.assertTrue(c.run_country_event(engine, events, "shishan_code.1004", actor))
        self.assertEqual(1, engine.events.count("shishan_code.1000"))
        self.assertEqual((11, 9, 12), c.reward_slots(actor))
        self.assertEqual(c.Decimal(0), actor.variables["shishan_code_architecture_repeat_count"])


class PreflightNegativeTests(unittest.TestCase):
    def test_preflight_rejects_unconditional_visible_window_after_exhaustion(self):
        defs = c.load_definitions(MOD, "scripted_effects") + c.load_definitions(MOD, "scripted_triggers")
        vals = c.load_definitions(MOD, "script_values")
        events = []
        for entry in c.country_events(MOD):
            body = c.block(entry.value)
            if c.one(body, "id") == "shishan_code.1004":
                body = [c.Entry(e.key, e.op, c.parse("shishan_code_reward_refresh_effect=yes country_event={id=shishan_code.1000}")) if e.key == "immediate" else e for e in body]
            events.append(c.Entry(entry.key, entry.op, body))
        with self.assertRaisesRegex(c.ContractError, "cannot schedule empty visible reward"):
            c.check_reward_preflight(MOD, defs, vals, events)


if __name__ == "__main__":
    unittest.main()
