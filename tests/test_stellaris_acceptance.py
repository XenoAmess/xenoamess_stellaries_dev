import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools import stellaris_acceptance as acceptance


class ManifestTests(unittest.TestCase):
    def test_windows_acceptance_process_is_per_monitor_dpi_aware(self) -> None:
        self.assertEqual(
            "per_monitor_aware",
            acceptance.DPI_AWARENESS["effective"],
            acceptance.DPI_AWARENESS,
        )

    def test_frozen_mod_tree_matches_runtime_contract(self) -> None:
        files, tree_hash = acceptance.tree_manifest(acceptance.MOD_ROOT)

        self.assertEqual(7, len(files))
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

    def test_runtime_settings_freeze_the_selected_supported_language(self) -> None:
        for language in acceptance.SUPPORTED_LANGUAGES:
            settings = acceptance.render_pdx_settings(language)
            self.assertIn(f'value="{language}"', settings)
            self.assertEqual(1, settings.count('"language"='))

        with self.assertRaisesRegex(ValueError, "unsupported acceptance language"):
            acceptance.render_pdx_settings("english")

    def test_scheduled_commands_are_strict_and_newline_terminated(self) -> None:
        self.assertEqual(
            '2200.01.02 = "minerals 5000"\n',
            acceptance.render_scheduled_commands(
                ["2200.01.02=minerals 5000"]
            ),
        )
        for invalid in ("minerals 5000", "2200-01-02=minerals 5000", "2200.01.02="):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    acceptance.render_scheduled_commands([invalid])

    def test_save_inspection_hashes_container_and_counts_exact_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            save = Path(directory) / "fixture.sav"
            gamestate = (
                'planet={ deposits={ 1={ type="mod_extend_bio_trophy_workplace" } '
                '2={ type="mod_extend_bio_trophy_workplace_extra" } } }'
            ).encode("utf-8")
            with zipfile.ZipFile(save, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("gamestate", gamestate)
                archive.writestr("meta", "name=fixture")

            result = acceptance.inspect_save_file(
                save,
                ['type="mod_extend_bio_trophy_workplace"'],
            )

            self.assertEqual(save.resolve(), Path(result["save"]))
            self.assertEqual(["gamestate", "meta"], result["zip_members"])
            self.assertEqual(len(gamestate), result["gamestate_bytes"])
            self.assertEqual(
                1,
                result["token_counts"]['type="mod_extend_bio_trophy_workplace"'],
            )

    def test_save_inspection_rejects_non_zip_or_missing_gamestate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plain = root / "plain.sav"
            plain.write_text("not a zip", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not a ZIP"):
                acceptance.inspect_save_file(plain, [])

            missing = root / "missing.sav"
            with zipfile.ZipFile(missing, "w") as archive:
                archive.writestr("meta", "name=fixture")
            with self.assertRaisesRegex(RuntimeError, "no gamestate"):
                acceptance.inspect_save_file(missing, [])

    def test_seed_save_is_copied_with_frozen_hash_into_fixture_slot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source" / "fixture.sav"
            source.parent.mkdir()
            with zipfile.ZipFile(source, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("gamestate", "planet={ id=3 }")
                archive.writestr("meta", "name=fixture")

            result = acceptance.copy_seed_save(source, root / "save games")
            copied = root / "save games" / "acceptance-fixtures" / "fixture.sav"

            self.assertEqual(copied.resolve(), Path(result["copied"]))
            self.assertEqual(source.resolve(), Path(result["source"]))
            self.assertEqual(acceptance.sha256(source), result["sha256"])
            self.assertEqual(source.read_bytes(), copied.read_bytes())

    def test_seed_save_requires_sav_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "fixture.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("gamestate", "planet={}")
            with self.assertRaisesRegex(ValueError, r"\.sav extension"):
                acceptance.copy_seed_save(source, root / "save games")


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_root = acceptance.ROOT / "fixtures" / "iteration-1"
        cls.contract = json.loads((fixture_root / "mod-contract.json").read_text(encoding="utf-8"))
        cls.scenarios = json.loads((fixture_root / "scenarios.json").read_text(encoding="utf-8"))

    def test_contract_covers_all_decisions_once(self) -> None:
        decisions = self.contract["decisions"]

        self.assertEqual(list(range(14)), [entry["index"] for entry in decisions])
        self.assertEqual(14, len({entry["decision"] for entry in decisions}))
        self.assertEqual(14, len({entry["deposit"] for entry in decisions}))
        self.assertEqual(1000, self.contract["common_decision_contract"]["cost"]["minerals"])
        self.assertEqual(180, self.contract["common_decision_contract"]["enactment_days"])
        self.assertEqual(
            "vivhite_workplace_supported_colony",
            self.contract["common_decision_contract"]["potential_trigger"],
        )

    def test_i1002_runtime_fixture_matches_frozen_mod_contract(self) -> None:
        run = self.scenarios["i1_002_run"]

        self.assertEqual(
            self.contract["mod"]["i1_002_tree_sha256"],
            run["mod_tree_sha256"],
        )
        self.assertEqual(
            self.contract["mod"]["previous_tree_modded_checksum"],
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
        self.assertEqual("passed", implementation["I1-003"]["status"])
        i1003_statuses = {
            entry["id"]: entry["status"]
            for entry in implementation["I1-003"]["scenarios"]
        }
        self.assertEqual("passed", i1003_statuses["I1-003-VISIBILITY"])
        self.assertEqual("passed", i1003_statuses["I1-003-EXECUTE"])
        self.assertEqual("passed", i1003_statuses["I1-003-REPEAT"])
        self.assertEqual("passed", i1003_statuses["I1-003-PERSISTENCE"])
        self.assertEqual(
            "passed_chinese_runtime_english_static",
            i1003_statuses["I1-003-LOCALISATION"],
        )
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

        version = (acceptance.ROOT / "VERSION").read_text(encoding="utf-8").strip()
        contract = json.loads(
            (acceptance.ROOT / "fixtures" / "iteration-1" / "mod-contract.json")
            .read_text(encoding="utf-8")
        )
        changelog = (acceptance.ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual("1.0.0", version)
        self.assertIn(f'version="{version}"', descriptor)
        self.assertEqual(version, contract["mod"]["declared_version"])
        self.assertIn(f"## [{version}]", changelog)
        self.assertEqual("3710613857", contract["upstream_workshop_id"])
        self.assertNotIn('remote_file_id="3710613857"', descriptor)
        release_workshop_id = contract["release_workshop_id"]
        if release_workshop_id is None:
            self.assertNotIn("remote_file_id=", descriptor)
        else:
            self.assertIn(f'remote_file_id="{release_workshop_id}"', descriptor)
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


class I1003SourceContractTests(unittest.TestCase):
    def test_plan13_is_restricted_to_valid_rogue_servitor_civic(self) -> None:
        text = (
            acceptance.MOD_ROOT / "common" / "decisions" / "workplace.txt"
        ).read_text(encoding="utf-8")
        marker = "decision_13_extend_bio_trophy_workplace = {"
        body = text[text.index(marker):]

        self.assertEqual(1, text.count(marker))
        self.assertIn(
            "owner = { has_valid_civic = civic_machine_servitor }",
            body,
        )
        self.assertIn("enactment_time = 180", body)
        self.assertIn("minerals = 1000", body)
        self.assertIn("add_deposit = mod_extend_bio_trophy_workplace", body)

    def test_bio_trophy_deposit_has_guarded_expected_modifiers(self) -> None:
        text = (
            acceptance.MOD_ROOT
            / "common"
            / "deposits"
            / "extend_workplace.txt"
        ).read_text(encoding="utf-8")
        marker = "mod_extend_bio_trophy_workplace = {"
        body = text[text.index(marker):]

        self.assertEqual(1, text.count(marker))
        self.assertIn("owner = { has_valid_civic = civic_machine_servitor }", body)
        self.assertIn("planet_housing_add = 600", body)
        self.assertIn("job_bio_trophy_add = 600", body)
        self.assertIn("pop_bio_trophy_bonus_workforce_mult = 0.1", body)

    def test_i1003_required_localisation_exists_in_both_languages(self) -> None:
        localisation_root = acceptance.MOD_ROOT / "localisation"
        chinese_path = localisation_root / "more_workplace_l_simp_chinese.yml"
        english_path = localisation_root / "more_workplace_l_english.yml"
        chinese = chinese_path.read_text(encoding="utf-8-sig")
        english = english_path.read_text(encoding="utf-8-sig")
        required_keys = {
            "decision_extend_workplace_expand",
            "decision_extend_workplace_expand_desc",
            "decision_extend_workplace_collapse",
            "decision_extend_workplace_collapse_desc",
            "mod_extend_bio_trophy_workplace",
            "mod_extend_bio_trophy_workplace_desc",
            "decision_13_extend_bio_trophy_workplace",
            "decision_13_extend_bio_trophy_workplace_desc",
        }

        self.assertTrue(chinese_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertTrue(english_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertTrue(chinese.startswith("l_simp_chinese:"))
        self.assertTrue(english.startswith("l_english:"))
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", english))
        for key in required_keys:
            self.assertIn(f" {key}:", chinese)
            self.assertIn(f" {key}:", english)

    def test_runtime_language_scope_is_chinese_only(self) -> None:
        scenarios = json.loads(
            (acceptance.ROOT / "fixtures" / "iteration-1" / "scenarios.json")
            .read_text(encoding="utf-8")
        )
        i1003 = next(
            item
            for item in scenarios["implementation_requirements"]
            if item["id"] == "I1-003"
        )
        localisation = next(
            item for item in i1003["scenarios"] if item["id"] == "I1-003-LOCALISATION"
        )
        s06 = next(item for item in scenarios["scenarios"] if item["id"] == "S06")

        self.assertEqual(["l_simp_chinese"], localisation["runtime_languages"])
        self.assertEqual(["l_english"], localisation["static_translation_languages"])
        self.assertEqual({"l_simp_chinese": "passed"}, s06["runtime_variants"])
        self.assertEqual("out_of_scope", localisation["non_chinese_runtime"])
        self.assertEqual("out_of_scope", s06["non_chinese_runtime"])


if __name__ == "__main__":
    unittest.main()
