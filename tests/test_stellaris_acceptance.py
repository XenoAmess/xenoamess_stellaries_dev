import json
import re
import tempfile
import unittest
from pathlib import Path

from tools import stellaris_acceptance as acceptance


class ManifestTests(unittest.TestCase):
    def test_frozen_mod_tree_matches_runtime_contract(self) -> None:
        files, tree_hash = acceptance.tree_manifest(acceptance.MOD_ROOT)

        self.assertEqual(6, len(files))
        self.assertEqual(acceptance.EXPECTED_MOD_TREE_SHA256, tree_hash)
        self.assertEqual(
            sorted(item["path"] for item in files),
            [item["path"] for item in files],
        )

    def test_write_json_is_utf8_and_newline_terminated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "result.json"
            acceptance.write_json(path, {"label": "计划10"})

            self.assertEqual('{\n  "label": "计划10"\n}\n', path.read_text(encoding="utf-8"))


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_root = acceptance.ROOT / "fixtures" / "iteration-1"
        cls.contract = json.loads((fixture_root / "mod-contract.json").read_text(encoding="utf-8"))
        cls.scenarios = json.loads((fixture_root / "scenarios.json").read_text(encoding="utf-8"))

    def test_contract_covers_all_decisions_once(self) -> None:
        decisions = self.contract["decisions"]

        self.assertEqual(list(range(13)), [entry["index"] for entry in decisions])
        self.assertEqual(13, len({entry["decision"] for entry in decisions}))
        self.assertEqual(13, len({entry["deposit"] for entry in decisions}))
        self.assertEqual(1000, self.contract["common_decision_contract"]["cost"]["minerals"])
        self.assertEqual(180, self.contract["common_decision_contract"]["enactment_days"])
        self.assertEqual(
            "vivhite_workplace_supported_colony",
            self.contract["common_decision_contract"]["potential_trigger"],
        )

    def test_i1002_runtime_fixture_matches_frozen_mod_contract(self) -> None:
        run = self.scenarios["i1_002_run"]

        self.assertEqual(self.contract["mod"]["tree_sha256"], run["mod_tree_sha256"])
        self.assertEqual(
            self.contract["mod"]["modded_checksum_observed"],
            run["modded_checksum"],
        )
        self.assertEqual(0, run["attributable_error_count"])
        self.assertEqual(
            {
                "ordinary_colony_expanded",
                "pc_ark_collapsed",
            },
            set(run["saves"]),
        )

    def test_scenarios_preserve_pass_fail_and_not_executed_states(self) -> None:
        statuses = {entry["id"]: entry["status"] for entry in self.scenarios["scenarios"]}

        self.assertEqual("failed", statuses["S01"])
        self.assertEqual("passed", statuses["S02"])
        self.assertEqual("passed_with_followup", statuses["S03"])
        self.assertEqual("not_executed", statuses["S04"])
        self.assertEqual("not_executed", statuses["S05"])
        self.assertEqual("partially_passed", statuses["S06"])

        implementation = {
            entry["id"]: entry for entry in self.scenarios["implementation_requirements"]
        }
        self.assertEqual("passed", implementation["I1-001"]["status"])
        self.assertEqual("passed", implementation["I1-002"]["status"])
        scenario_statuses = {
            entry["id"]: entry["status"]
            for entry in implementation["I1-001"]["scenarios"]
        }
        self.assertEqual("passed", scenario_statuses["I1-001-LOAD"])
        self.assertEqual("passed", scenario_statuses["I1-001-NORMAL-CATALOG"])
        self.assertEqual("passed", scenario_statuses["I1-001-NOMAD-CATALOG"])
        self.assertEqual(
            "passed_with_cost_ui_limit",
            scenario_statuses["I1-001-NOMAD-EXECUTE"],
        )
        i1002_scenario_statuses = {
            entry["id"]: entry["status"]
            for entry in implementation["I1-002"]["scenarios"]
        }
        self.assertEqual(
            {
                "I1-002-DEFAULT-COLLAPSED": "passed",
                "I1-002-EXPAND": "passed",
                "I1-002-COLLAPSE": "passed",
                "I1-002-PERSISTENCE": "passed",
            },
            i1002_scenario_statuses,
        )


class I1001SourceContractTests(unittest.TestCase):
    def test_every_decision_uses_the_carrier_compatibility_trigger(self) -> None:
        decision_path = (
            acceptance.MOD_ROOT / "common" / "decisions" / "workplace.txt"
        )
        decision_text = decision_path.read_text(encoding="utf-8")
        contract = json.loads(
            (
                acceptance.ROOT
                / "fixtures"
                / "iteration-1"
                / "mod-contract.json"
            ).read_text(encoding="utf-8")
        )

        declarations = list(
            re.finditer(r"(?m)^([a-z0-9_]+) = \{$", decision_text)
        )
        bodies = {}
        for position, match in enumerate(declarations):
            end = declarations[position + 1].start() if position + 1 < len(declarations) else len(decision_text)
            bodies[match.group(1)] = decision_text[match.start():end]

        for decision in contract["decisions"]:
            body = bodies[decision["decision"]]
            self.assertIn("owned_planets_only = yes", body)
            self.assertIn("vivhite_workplace_supported_colony = yes", body)
            self.assertIn("has_carrier_flag = vivhite_workplace_menu_expanded", body)

    def test_carrier_trigger_accepts_ordinary_colonies_and_pc_ark(self) -> None:
        trigger_path = (
            acceptance.MOD_ROOT
            / "common"
            / "scripted_triggers"
            / "vivhite_workplace_triggers.txt"
        )
        trigger_text = trigger_path.read_text(encoding="utf-8")

        self.assertIn("vivhite_workplace_supported_colony", trigger_text)
        self.assertIn("owner = { is_nomadic = no }", trigger_text)
        self.assertIn("is_planet_class = pc_ark", trigger_text)
        self.assertIn("OR = {", trigger_text)

    def test_descriptor_targets_stellaris_4_4(self) -> None:
        descriptor = (acceptance.MOD_ROOT / "descriptor.mod").read_text(
            encoding="utf-8-sig"
        )

        self.assertIn('version="4.4.6-i1.2"', descriptor)
        self.assertIn('supported_version="4.4.*"', descriptor)


class I1002SourceContractTests(unittest.TestCase):
    def test_menu_toggle_decisions_are_zero_cost_mutually_exclusive_pair(self) -> None:
        text = (
            acceptance.MOD_ROOT / "common" / "decisions" / "workplace.txt"
        ).read_text(encoding="utf-8")

        self.assertEqual(1, text.count("decision_extend_workplace_expand = {"))
        self.assertEqual(1, text.count("decision_extend_workplace_collapse = {"))
        self.assertEqual(2, text.count("enactment_time = 0"))
        self.assertEqual(1, text.count("set_carrier_flag = vivhite_workplace_menu_expanded"))
        self.assertEqual(1, text.count("remove_carrier_flag = vivhite_workplace_menu_expanded"))
        self.assertIn(
            "NOT = { has_carrier_flag = vivhite_workplace_menu_expanded }",
            text,
        )
        self.assertNotIn("planet_flag", text)

    def test_menu_toggle_localisation_is_not_placeholder_text(self) -> None:
        localisation = (
            acceptance.MOD_ROOT
            / "localisation"
            / "more_workplace_l_simp_chinese.yml"
        ).read_text(encoding="utf-8-sig")

        self.assertIn('decision_extend_workplace_expand: "展开岗位扩展计划"', localisation)
        self.assertIn('decision_extend_workplace_collapse: "收起岗位扩展计划"', localisation)
        self.assertNotIn('decision_extend_workplace_expand_desc: "准备大建"', localisation)
        self.assertNotIn('decision_extend_workplace_collapse_desc: "结束大建"', localisation)


if __name__ == "__main__":
    unittest.main()
