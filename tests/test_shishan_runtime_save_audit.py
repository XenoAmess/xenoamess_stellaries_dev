"""Read-only native-save audits plus isolated in-memory P-data boundaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("native_feedback_save_audit", ROOT / "shishan_code_origin/tools/audit_feedback_runtime_save.py")
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)

META = 'version="Cygnus v4.5.2" date="2200.01.01"'
GAME = '''
version="Cygnus v4.5.2" date="2200.01.01"
player={ { name="a string { country=0 } # literal" country=7 } }
species_db={
 0={traits={}}
 10={portrait="portrait_is_not_a_trait" traits={trait="positive" trait="negative" trait="preference"}}
 11={base_ref=10 traits={trait="positive" trait="negative" trait="preference" trait="hidden_third_party"}}
 20={traits={trait="foreign"}}
}
country={
 7={
  founder_species_ref=10
  government={origin="origin_shishan_code"}
  owned_planets={0}
  modules={standard_species_rights_module={primary={species_index=10}}}
  variables={}
  flags={shishan_code_initialized=1234}
  timed_modifier={items={ {modifier="shishan_code_vivhite_base" days=-1} }}
  events={
   special_project={id=4 special_project="SHISHAN_CODE_MAINTAIN" status=active}
   special_project={id=5 special_project="SHISHAN_CODE_CLEAN" status=available}
  }
 }
 9={owned_planets={1}}
}
colony={
 0={carrier={type=planet reference=8} pop_groups={1 2 4 5}}
 1={carrier={type=planet reference=9} pop_groups={3}}
}
planets={planet={
 0={planet_class="pc_star"}
 8={colony=0 owner=7}
 9={colony=1 owner=9}
}}
pop_groups={
 1={key={species=10 category=worker} planet=0 size=8}
 2={key={species=11 category=worker} planet=0 size=2}
 3={key={species=10 category=worker} planet=1 size=10000}
 4={key={species=20 category=worker} planet=0 size=3}
 5={key={species=11 category=worker} planet=0 size=0}
}
'''


class ReaderTests(unittest.TestCase):
    def test_founder_pointer_wins_over_stale_same_lineage_rights_primary(self):
        result = audit.inspect_text(META, GAME.replace("founder_species_ref=10", "founder_species_ref=11"))
        self.assertEqual(11, result["actor"]["main_species_id"])
        self.assertEqual("country.founder_species_ref", result["actor"]["main_species_source"])
        self.assertEqual("10", result["actor"]["main_species_evidence"]["rights_primary_species_index"])
        self.assertEqual(10, result["population"]["population"])
        self.assertEqual("16/5", result["population"]["trait_average_exact"])

    def test_founder_pointer_selects_actual_lineage_instead_of_rights_primary(self):
        result = audit.inspect_text(META, GAME.replace("founder_species_ref=10", "founder_species_ref=20"))
        self.assertEqual(20, result["actor"]["main_species_id"])
        self.assertEqual(3, result["population"]["population"])
        self.assertEqual(3, result["population"]["trait_weight"])

    def test_missing_or_duplicate_founder_never_falls_back_to_rights(self):
        for text in (GAME.replace("founder_species_ref=10", ""), GAME.replace("founder_species_ref=10", "founder_species_ref=10 founder_species_ref=11")):
            with self.subTest(text=text), self.assertRaisesRegex(audit.AuditError, "founder_species_ref"):
                audit.inspect_text(META, text)

    def test_unknown_founder_pointer_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.inspect_text(META, GAME.replace("founder_species_ref=10", "founder_species_ref=999"))

    def test_cached_species_references_preserved_without_replacing_main(self):
        text = GAME.replace("founder_species_ref=10", "founder_species_ref=11 default_species={10=11} owned_species_refs={10}")
        evidence = audit.inspect_text(META, text)["actor"]["main_species_evidence"]
        self.assertEqual([{"key": "10", "value": "11"}], evidence["default_species_raw"])
        self.assertEqual(["10"], evidence["owned_species_refs_raw"])

    def test_strings_comments_bare_members_and_duplicate_assignments(self):
        doc = audit.Document('a={ key="{ quoted } # literal \\"" # real } comment\n repeated=1 repeated=2 list={ 7 9 {country=5} } }')
        body = doc.section(doc.root, "a")
        self.assertIn("quoted", doc.scalar(body, "key"))
        self.assertEqual(["1", "2"], doc.values(body, "repeated"))
        with self.assertRaisesRegex(audit.AuditError, "duplicate"):
            doc.field(body, "repeated")
        self.assertEqual(3, len(doc.entries(doc.section(body, "list"))))

    def test_malformed_blocks_and_strings_fail(self):
        for text in ('a={key=1', 'a={key="unfinished}', 'a=}', '=2'):
            with self.subTest(text=text), self.assertRaises(audit.AuditError):
                audit.Document(text).entries()

    def test_dynamic_nonzero_player_and_colony_carrier_resolution(self):
        report = audit.inspect_text(META, GAME)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(7, report["actor"]["country_id"])
        self.assertEqual("origin_shishan_code", report["actor"]["origin"])
        self.assertEqual(8, report["population"]["ownership_links"][0]["carrier_reference"])
        self.assertEqual(10, report["population"]["population"])
        self.assertEqual(32, report["population"]["trait_weight"])
        self.assertEqual("32/10", report["population"]["trait_average_expression"])
        self.assertEqual("16/5", report["population"]["trait_average_exact"])
        self.assertEqual(1, report["population"]["foreign_colony_groups_excluded"])
        self.assertEqual(2, len(report["population"]["excluded_domestic_groups"]))
        self.assertEqual(["4", "5"], [str(row["id"]) for row in report["observed"]["special_projects"]])
        self.assertEqual("1", report["observed"]["modifiers"][0]["effective_multiplier"])
        self.assertEqual("NOT OBSERVED", report["redesign_observation_status"])
        self.assertIsNone(report["independent_expected"]["total"])
        for row in report["independent_expected"]["comparisons"].values():
            self.assertEqual("MISSING", row["status"])

    def test_foreign_template_and_empty_group_do_not_change_u(self):
        result = audit.inspect_text(META, GAME)
        rows = result["population"]["populated_templates"]
        self.assertEqual([(10, 8, 3), (11, 2, 4)], [(row["id"], row["population"], row["distinct_trait_count"]) for row in rows])
        self.assertTrue(all("portrait_is_not_a_trait" not in row["distinct_trait_keys"] for row in rows))

    def test_current_redesign_observations_are_compared_not_filled(self):
        variables = '''variables={
         shishan_code_architecture_population=10 shishan_code_architecture_trait_weight=32
         shishan_code_architecture_trait_average=3.2 shishan_code_architecture_repeat_count=2
         shishan_code_architecture_total=5.2 shishan_code_architecture_bonus=0.26
         shishan_code_architecture_multiplier=1.26 }'''
        source = GAME.replace("variables={}", variables).replace("shishan_code_initialized=1234", "shishan_code_initialized=1234 shishan_code_architecture_migrated=2345")
        result = audit.inspect_text(META, source)
        self.assertEqual("PASS", result["status"])
        for row in result["independent_expected"]["comparisons"].values():
            self.assertEqual("MATCH", row["status"])
        broken = source.replace("shishan_code_architecture_trait_average=3.2", "shishan_code_architecture_trait_average=3.3")
        self.assertEqual("FAIL", audit.inspect_text(META, broken)["status"])

    def test_unknown_carrier_or_wrong_owner_fail_closed(self):
        for text in (GAME.replace("type=planet reference=8", "type=ship reference=8"), GAME.replace("8={colony=0 owner=7}", "8={colony=0 owner=9}"), GAME.replace("8={colony=0 owner=7}", "8={colony=1 owner=7}")):
            with self.subTest(text=text), self.assertRaises(audit.AuditError):
                audit.inspect_text(META, text)

    def test_unknown_player_or_ambiguous_players_fail(self):
        for text in (GAME.replace("country=7 }", "country=77 }"), GAME.replace('name="a string { country=0 } # literal" country=7', 'country=7 } { country=9')):
            with self.subTest(text=text), self.assertRaises(audit.AuditError):
                audit.inspect_text(META, text)

    def test_population_list_or_missing_species_fail(self):
        for text in (GAME.replace("pop_groups={1 2 4 5}", "pop_groups={1 4 5}"), GAME.replace("species=11 category=worker", "species=99 category=worker"), GAME.replace("planet=0 size=8", "planet=999 size=8")):
            with self.subTest(text=text), self.assertRaises(audit.AuditError):
                audit.inspect_text(META, text)

    def test_unknown_species_identity_and_cycle_fail(self):
        for text in (GAME.replace("11={base_ref=10", "11={identity=10 base_ref=10"), GAME.replace("10={portrait=", "10={base_ref=11 portrait=")):
            with self.subTest(text=text), self.assertRaises(audit.AuditError):
                audit.inspect_text(META, text)

    def test_meta_disagreement_fails(self):
        with self.assertRaisesRegex(audit.AuditError, "meta/gamestate"):
            audit.inspect_text(META.replace("4.5.2", "4.5.1"), GAME)


class ArchivedNativeSaveTests(unittest.TestCase):
    def test_actual_rc4_claim_main_pointer_differs_from_rights_primary(self):
        path = ROOT / "_runtime/shishan_code/20261015-runtime/runs/20261015T080652Z/fb454_claim1.sav"
        if not path.is_file():
            self.skipTest("native rc4 claim evidence not present")
        result = audit.audit_save(path)
        self.assertEqual("PASS", result["status"], result.get("diagnostics"))
        self.assertEqual(50, result["actor"]["main_species_id"])
        self.assertEqual("3321888769", result["actor"]["main_species_evidence"]["rights_primary_species_index"])
        self.assertEqual(5551, result["population"]["population"])
        self.assertEqual(39368, result["population"]["trait_weight"])

    def test_original_mixed_templates_weight_actual_population(self):
        path = ROOT / "assets/shishan-code-origin/evidence/rs04-variant-anchor-2203.09.24.sav"
        result = audit.audit_save(path)
        self.assertEqual("PASS", result["status"], result.get("diagnostics"))
        self.assertEqual("33817/5551", result["population"]["trait_average_expression"])
        self.assertEqual([(48, 511, 7), (3321888769, 5040, 6)], [(row["id"], row["population"], row["distinct_trait_count"]) for row in result["population"]["populated_templates"]])
        self.assertIn("4.5.1", result["native_version"])

    def test_original_exhausted_save_43_keys_and_expected_23_extra_layers(self):
        path = ROOT / "assets/shishan-code-origin/evidence/shishan_reward_exhausted.sav"
        result = audit.audit_save(path)
        self.assertEqual("PASS", result["status"], result.get("diagnostics"))
        self.assertEqual("554504e65d4b14d70fd91be3cb66c434c7c232ea37c109e70b7e2ebe93f4fccf", result["save_sha256"])
        self.assertEqual("43/1", result["population"]["trait_average_exact"])
        self.assertEqual(43, result["population"]["populated_templates"][0]["distinct_trait_count"])
        self.assertEqual("23", result["independent_expected"]["legacy_extra_repeat_migration"])
        self.assertEqual("NOT OBSERVED", result["redesign_observation_status"])
        self.assertIsNone(result["independent_expected"]["total"])


if __name__ == "__main__":
    unittest.main()
