"""Canonical native metadata and deterministic emitted qualification negatives."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/shishan_code"))
import audit_reward_contract as audit
from generate_rewards import ROBOTIC, ROBOTIC_REQUIRED_DLC

c = audit.feedback_validator()
MOD = ROOT / "shishan_code_origin/mod"
GAME = Path("C:/Program Files (x86)/Steam/steamapps/common/Stellaris")


class CanonicalMetadataTests(unittest.TestCase):
    def metadata(self):
        return audit.canonical_traits([("independent.txt", '''
            trait_core_a={ allowed_archetypes={ROBOT MACHINE} tags={positive}
                opposites={"trait_core_b"} opposites={trait_structural}
                forbidden_ethics={ethic_gestalt_consciousness}
                host_has_dlc="Independent DLC"
                species_potential_add={OR={can_add_synth_traits=yes owner_is_individual_machine=yes}}
            }
            trait_core_b={opposites={trait_core_a}}
            trait_reverse_only={opposites={trait_core_a}}
        ''')], ["trait_core_a"])

    def test_repeated_and_reverse_opposites_are_all_preserved(self):
        native = self.metadata()["traits"]["trait_core_a"]
        self.assertEqual(["trait_core_b", "trait_structural"], native["direct_opposites"])
        self.assertEqual(["trait_core_b", "trait_reverse_only"], native["reverse_opposites"])
        self.assertEqual(["trait_core_b", "trait_reverse_only", "trait_structural"], native["opposites"])

    def test_omitted_core_canonical_opposite_fails_deterministically(self):
        with self.assertRaisesRegex(c.ContractError, "canonical opposite declaration"):
            audit.check_declarations(self.metadata(), [("trait_core_a", [], True, False)], {"trait_core_a": "Independent DLC"})

    def test_omitted_canonical_dlc_fails(self):
        native = self.metadata()
        robotic = [("trait_core_a", native["traits"]["trait_core_a"]["opposites"], True, False)]
        with self.assertRaisesRegex(c.ContractError, "canonical DLC declaration"):
            audit.check_declarations(native, robotic, {})

    def test_omitted_canonical_forbidden_ethic_fails(self):
        native = self.metadata()
        robotic = [("trait_core_a", native["traits"]["trait_core_a"]["opposites"], False, False)]
        with self.assertRaisesRegex(c.ContractError, "canonical forbidden ethic omitted"):
            audit.check_declarations(native, robotic, {"trait_core_a": "Independent DLC"})

    def test_unknown_native_eligibility_fails_closed(self):
        for source in ("trait_x={forbidden_ethics={ethic_new}}", "trait_x={species_potential_add={mystery=yes}}"):
            with self.subTest(source=source), self.assertRaises(c.ContractError):
                audit.canonical_traits([("unknown.txt", source)], ["trait_x"])

    def test_archetype_requires_species_and_dlc_is_explicit(self):
        engine = c.Effects([])
        with self.assertRaisesRegex(c.ContractError, "requires species scope"):
            engine.trigger(c.parse("is_archetype=MACHINE"), c.Scope())
        self.assertFalse(engine.trigger(c.parse('host_has_dlc="Independent DLC"'), c.Scope()))
        enabled = c.Effects([], host_dlcs={"Independent DLC"})
        self.assertTrue(enabled.trigger(c.parse('host_has_dlc="Independent DLC"'), c.Scope()))
        self.assertTrue(engine.trigger(c.parse("is_archetype=ROBOT"), c.Scope(kind="species", archetype="ROBOT")))
        self.assertFalse(engine.trigger(c.parse("is_archetype=MACHINE"), c.Scope(kind="species", archetype="BIOLOGICAL")))


@unittest.skipUnless((GAME / "common/traits/05_species_traits_robotic.txt").is_file(), "installed canonical vanilla required")
class EmittedCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = audit.canonical_traits(
            [(str(path), path.read_text(encoding="utf-8-sig")) for path in sorted((GAME / "common/traits").glob("*.txt"))],
            [item[0] for item in ROBOTIC])
        cls.definitions = c.load_definitions(MOD, "scripted_effects") + c.load_definitions(MOD, "scripted_triggers")

    def test_installed_canonical_declarations_and_actual_guards(self):
        policies = audit.check_declarations(self.canonical, ROBOTIC, ROBOTIC_REQUIRED_DLC)
        self.assertEqual({"trait_robot_propaganda_machines", "trait_robot_trading_algorithms"}, set(policies))
        result = audit.check_emitted_guards(self.canonical, self.definitions, ROBOTIC)
        self.assertGreater(result["guard_assertions"], 300)
        self.assertFalse(result["eligibility_overrides"])

    def remove_core_conflict(self, section):
        """Mutate the actual physicists guard, retaining independent vanilla truth."""
        key = {"eligible": "shishan_code_reward_eligible_18", "claim": "shishan_code_reward_claim_18_effect", "coverage": "shishan_code_reward_coverage_effect"}[section]
        opposite = "trait_robot_artificial_sociologists"

        def mutate(entries):
            return [c.Entry(entry.key, entry.op, mutate(entry.value) if isinstance(entry.value, list) else entry.value)
                    for entry in entries if not (entry.key == "has_trait" and entry.value == opposite)]

        definitions = []
        for entry in self.definitions:
            if entry.key != key:
                definitions.append(entry)
            elif section == "eligible":
                definitions.append(c.Entry(entry.key, entry.op, mutate(entry.value)))
            elif section == "claim":
                def at_path(entries, path):
                    return [c.Entry(e.key, e.op, mutate(e.value) if len(path) == 1 else at_path(e.value, path[1:])) if e.key == path[0] else e for e in entries]
                definitions.append(c.Entry(entry.key, entry.op, at_path(entry.value, ("if", "every_owned_pop_group", "if", "limit"))))
            else:
                # Coverage contains all 39 candidates; mutate only candidate 18.
                body, ordinal, result = c.block(entry.value), 0, []
                for child in body:
                    if child.key == "if":
                        ordinal += 1
                    result.append(c.Entry(child.key, child.op, mutate(child.value)) if child.key == "if" and ordinal == 18 else child)
                definitions.append(c.Entry(entry.key, entry.op, result))
        return definitions

    def test_missing_actual_core_eligibility_guard_is_rejected(self):
        with self.assertRaisesRegex(c.ContractError, "actual eligibility trait_robot_artificial_physicists: canonical conflict"):
            audit.check_emitted_guards(self.canonical, self.remove_core_conflict("eligible"), ROBOTIC)

    def test_missing_actual_core_claim_template_guard_is_rejected(self):
        with self.assertRaisesRegex(c.ContractError, "actual claim template guard trait_robot_artificial_physicists: canonical conflict"):
            audit.check_emitted_guards(self.canonical, self.remove_core_conflict("claim"), ROBOTIC)

    def test_missing_actual_core_coverage_guard_is_rejected(self):
        with self.assertRaisesRegex(c.ContractError, "actual coverage guard trait_robot_artificial_physicists: canonical conflict"):
            audit.check_emitted_guards(self.canonical, self.remove_core_conflict("coverage"), ROBOTIC)

    def test_frozen_rc3_core_eligibility_is_rejected(self):
        frozen = Path("C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T074214Z/mod/shishan-feedback-local")
        if not frozen.is_dir():
            self.skipTest("actual frozen rc3 package unavailable")
        definitions = c.load_definitions(frozen, "scripted_effects") + c.load_definitions(frozen, "scripted_triggers")
        engine, country, _, _ = audit.guard_fixture(definitions,
            traits={"trait_robot_artificial_sociologists"}, dlcs={"The Machine Age"})
        guard = c.block(c.one(definitions, "shishan_code_reward_eligible_18"))
        with self.assertRaisesRegex(c.ContractError, "frozen rc3 mutually exclusive research core: expected False, got True"):
            c.equal(engine.trigger(guard, country), False, "frozen rc3 mutually exclusive research core")


if __name__ == "__main__":
    unittest.main()
