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

    def test_logical_scroll_clicks_use_windows_wheel_delta(self) -> None:
        self.assertEqual(120, acceptance.windows_wheel_delta(1))
        self.assertEqual(-720, acceptance.windows_wheel_delta(-6))
        self.assertEqual(0, acceptance.windows_wheel_delta(0))

    def test_frozen_mod_tree_matches_runtime_contract(self) -> None:
        files, tree_hash = acceptance.tree_manifest(acceptance.MOD_ROOT)

        self.assertEqual(15, len(files))
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
        self.assertEqual(("l_simp_chinese",), acceptance.SUPPORTED_LANGUAGES)
        for language in acceptance.SUPPORTED_LANGUAGES:
            settings = acceptance.render_pdx_settings(language)
            self.assertIn(f'value="{language}"', settings)
            self.assertEqual(1, settings.count('"language"='))

        for language in ("english", *acceptance.STATIC_TRANSLATION_LANGUAGES):
            with self.subTest(language=language):
                with self.assertRaisesRegex(ValueError, "unsupported acceptance language"):
                    acceptance.render_pdx_settings(language)

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

    def test_i1r02_closes_from_only_mod_baseline_without_overclaiming(self) -> None:
        regressions = {
            entry["id"]: entry
            for entry in self.scenarios["regression_requirements"]
        }
        closure = regressions["I1-R02"]

        self.assertEqual(
            "passed_baseline_no_third_party_guarantee", closure["status"]
        )
        self.assertEqual("I1-002", closure["source_requirement"])
        self.assertEqual(
            self.scenarios["i1_002_run"]["run_id"], closure["runtime_run_id"]
        )
        self.assertEqual([], closure["environment"]["third_party_ui_mods"])
        self.assertFalse(
            closure["observed"]["named_reproducible_ui_conflict_available"]
        )
        self.assertEqual(
            "not_tested_no_specific_reproduction_target",
            closure["third_party_ui_compatibility"],
        )

    def test_i1r01_freezes_hive_employment_and_reload_evidence(self) -> None:
        regressions = {
            entry["id"]: entry
            for entry in self.scenarios["regression_requirements"]
        }
        closure = regressions["I1-R01"]

        self.assertEqual("passed", closure["status"])
        self.assertEqual("20260907T063145Z", closure["runtime_run_id"])
        self.assertEqual(["l_simp_chinese"], closure["runtime_languages"])
        self.assertEqual(
            "9a0e6189a86db3eb5bb118ccd35d26333154dc98034892ec557771490fc9040e",
            closure["environment"]["mod_tree_sha256"],
        )
        self.assertEqual(
            ["mod/ugc_3797257579.mod"], closure["environment"]["enabled_mods"]
        )
        jobs = closure["observed"]["jobs"]
        self.assertEqual(
            (920, 920),
            (jobs["coordinator"]["current"], jobs["coordinator"]["maximum"]),
        )
        for job in ("physics", "society", "engineering"):
            with self.subTest(job=job):
                self.assertEqual(60, jobs[job]["before_maximum"])
                self.assertEqual(660, jobs[job]["current"])
                self.assertEqual(660, jobs[job]["maximum"])
        deposits = closure["observed"]["save"]["deposit_occurrences"]
        self.assertEqual({1}, set(deposits.values()))
        self.assertEqual(4, len(deposits))
        self.assertTrue(closure["observed"]["persistence_passed"])
        self.assertEqual(0, closure["observed"]["attributable_error_count"])

    def test_scenarios_preserve_current_execution_states(self) -> None:
        statuses = {entry["id"]: entry["status"] for entry in self.scenarios["scenarios"]}

        self.assertEqual("passed", statuses["S01"])
        self.assertEqual("passed", statuses["S02"])
        self.assertEqual("passed", statuses["S03"])
        self.assertEqual("passed", statuses["S04"])
        self.assertEqual("passed_by_linked_requirements", statuses["S05"])
        self.assertEqual("passed_chinese_runtime_non_chinese_static", statuses["S06"])

        s03 = next(
            entry for entry in self.scenarios["scenarios"] if entry["id"] == "S03"
        )
        self.assertEqual(1, s03["observed"]["deposit_occurrences"])
        self.assertEqual(1000, s03["observed"]["miner_capacity_after"])
        self.assertEqual(1000, s03["observed"]["miner_capacity_after_reload"])
        self.assertTrue(s03["observed"]["persistence_passed"])

        s04 = next(
            entry for entry in self.scenarios["scenarios"] if entry["id"] == "S04"
        )
        self.assertTrue(s04["observed"]["decision_selectable_after_first"])
        self.assertEqual(2, s04["observed"]["deposit_occurrences_after_second"])
        self.assertEqual(600, s04["observed"]["stable_capacity_delta"])
        self.assertEqual(1600, s04["observed"]["miner_capacity_after_reload"])
        self.assertEqual(
            "delayed_until_save_reload",
            s04["observed"]["immediate_job_ui_refresh"],
        )
        self.assertEqual(2, s04["observed"]["efficiency_source_occurrences_after_reload"])
        self.assertTrue(s04["observed"]["persistence_passed"])

        s0304_run = self.scenarios["s03_s04_run"]
        self.assertEqual("20260907T093411Z", s0304_run["run_id"])
        self.assertEqual(["l_simp_chinese"], s0304_run["runtime_languages"])
        self.assertEqual(1, s0304_run["saves"]["after_first_execution"]["deposit_occurrences"])
        self.assertEqual(2, s0304_run["saves"]["after_second_execution"]["deposit_occurrences"])
        self.assertEqual(0, s0304_run["attributable_error_count"])

        s05 = next(
            entry for entry in self.scenarios["scenarios"] if entry["id"] == "S05"
        )
        self.assertEqual(
            {"hive", "machine", "rogue_servitor", "nomad_or_ark"},
            set(s05["observed"]["variant_results"]),
        )
        self.assertEqual(["l_simp_chinese"], s05["observed"]["runtime_languages"])

        implementation = {
            entry["id"]: entry for entry in self.scenarios["implementation_requirements"]
        }
        self.assertEqual("passed", implementation["I1-001"]["status"])
        self.assertEqual("passed", implementation["I1-002"]["status"])
        self.assertEqual("passed", implementation["I1-003"]["status"])
        self.assertEqual(
            "passed_non_chinese_static_only", implementation["I1-004"]["status"]
        )
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
        self.assertEqual("1.0.1", version)
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
        i1004 = next(
            item
            for item in scenarios["implementation_requirements"]
            if item["id"] == "I1-004"
        )
        s06 = next(item for item in scenarios["scenarios"] if item["id"] == "S06")

        self.assertEqual(["l_simp_chinese"], localisation["runtime_languages"])
        self.assertEqual(["l_english"], localisation["static_translation_languages"])
        self.assertEqual(["l_simp_chinese"], i1004["runtime_languages"])
        self.assertEqual(
            list(acceptance.STATIC_TRANSLATION_LANGUAGES),
            i1004["static_translation_languages"],
        )
        self.assertEqual(
            list(acceptance.LOCALISATION_LANGUAGES),
            i1004["official_supported_languages"],
        )
        self.assertEqual({"l_simp_chinese": "passed"}, s06["runtime_variants"])
        self.assertEqual(
            set(acceptance.STATIC_TRANSLATION_LANGUAGES),
            set(s06["static_translation_variants"]),
        )
        self.assertEqual(
            {"passed"}, set(s06["static_translation_variants"].values())
        )
        self.assertEqual("out_of_scope", localisation["non_chinese_runtime"])
        self.assertEqual("out_of_scope", i1004["non_chinese_runtime"])
        self.assertEqual("out_of_scope", s06["non_chinese_runtime"])


class I1004OfficialLocalisationTests(unittest.TestCase):
    @staticmethod
    def _parse_entries(path: Path) -> tuple[str, dict[str, str]]:
        text = path.read_text(encoding="utf-8-sig")
        lines = text.splitlines()
        entries: dict[str, str] = {}
        entry_pattern = re.compile(r'^\s+([A-Za-z0-9_]+):\s+"(.*)"\s*$')
        for line in lines[1:]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = entry_pattern.fullmatch(line)
            if match is None:
                raise AssertionError(f"malformed localisation line: {line!r}")
            key, value = match.groups()
            if key in entries:
                raise AssertionError(f"duplicate localisation key: {key}")
            entries[key] = value
        return lines[0], entries

    def test_all_official_languages_have_complete_readable_key_parity(self) -> None:
        localisation_root = acceptance.MOD_ROOT / "localisation"
        chinese_path = localisation_root / "more_workplace_l_simp_chinese.yml"
        chinese_header, chinese = self._parse_entries(chinese_path)

        self.assertTrue(chinese_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertEqual("l_simp_chinese:", chinese_header)
        self.assertEqual(60, len(chinese))

        expected_files = {
            f"more_workplace_{language}.yml"
            for language in acceptance.LOCALISATION_LANGUAGES
        }
        self.assertEqual(
            expected_files,
            {path.name for path in localisation_root.glob("more_workplace_l_*.yml")},
        )

        script_patterns = {
            "l_english": r"[A-Za-z]",
            "l_braz_por": r"[A-Za-zÀ-ž]",
            "l_german": r"[A-Za-zÀ-ž]",
            "l_french": r"[A-Za-zÀ-ž]",
            "l_spanish": r"[A-Za-zÀ-ž]",
            "l_polish": r"[A-Za-zÀ-ž]",
            "l_russian": r"[\u0400-\u04ff]",
            "l_japanese": r"[\u3040-\u30ff\u3400-\u9fff]",
            "l_korean": r"[\uac00-\ud7a3]",
        }
        cjk_forbidden = set(acceptance.STATIC_TRANSLATION_LANGUAGES) - {
            "l_japanese",
            "l_korean",
        }

        for language in acceptance.LOCALISATION_LANGUAGES:
            path = localisation_root / f"more_workplace_{language}.yml"
            header, entries = self._parse_entries(path)
            with self.subTest(language=language):
                self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
                self.assertEqual(f"{language}:", header)
                self.assertEqual(set(chinese), set(entries))
                self.assertEqual(60, len(entries))
            if language == "l_simp_chinese":
                continue
            for key, value in entries.items():
                with self.subTest(language=language, key=key):
                    self.assertTrue(value.strip())
                    self.assertNotEqual(key, value.strip())
                    self.assertNotEqual(chinese[key], value)
                    self.assertRegex(value, script_patterns[language])
                    if language in cjk_forbidden:
                        self.assertIsNone(re.search(r"[\u3400-\u9fff]", value))

    def test_every_plan_has_decision_and_deposit_name_description_pairs(self) -> None:
        for language in acceptance.LOCALISATION_LANGUAGES:
            path = (
                acceptance.MOD_ROOT
                / "localisation"
                / f"more_workplace_{language}.yml"
            )
            _, entries = self._parse_entries(path)

            for index in range(14):
                decision_prefix = f"decision_{index:02d}_extend_"
                decision_names = [
                    key
                    for key in entries
                    if key.startswith(decision_prefix) and not key.endswith("_desc")
                ]
                with self.subTest(language=language, plan=index):
                    self.assertEqual(1, len(decision_names))
                    self.assertIn(f"{decision_names[0]}_desc", entries)

            deposit_names = [
                key
                for key in entries
                if key.startswith("mod_extend_") and not key.endswith("_desc")
            ]
            with self.subTest(language=language):
                self.assertEqual(14, len(deposit_names))
            for key in deposit_names:
                self.assertIn(f"{key}_desc", entries)

    def test_plan13_numeric_effects_are_preserved_in_every_translation(self) -> None:
        localisation_root = acceptance.MOD_ROOT / "localisation"
        key = "decision_13_extend_bio_trophy_workplace_desc"
        for language in acceptance.LOCALISATION_LANGUAGES:
            _, entries = self._parse_entries(
                localisation_root / f"more_workplace_{language}.yml"
            )
            with self.subTest(language=language):
                self.assertGreaterEqual(entries[key].count("600"), 2)
                if language == "l_simp_chinese":
                    self.assertIn("提高10%", entries[key])
                else:
                    self.assertIn("+10", entries[key])


if __name__ == "__main__":
    unittest.main()
