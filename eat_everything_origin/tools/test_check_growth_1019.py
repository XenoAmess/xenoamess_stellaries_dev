"""Offline original-block parsing and independently fixed growth arithmetic checks."""
import contextlib
import copy
import io
import json
import math
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import check_growth_1019 as c


class GrowthReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="eep-growth-report-")
        self.folder = Path(self.tmp.name)
        fixture = c.load(Path(__file__).parent / "fixtures/fmm00-growth-native-extract.json")
        blocks = fixture["blocks"]
        text = ('date="2200.01.01" saved_event_target={' + blocks["saved_event_target"]
                + '} country={0={' + " ".join(key + "={" + blocks["country0_" + key] + "}"
                    for key in ("fleets_manager", "government", "variables"))
                + '}} fleet={159={' + blocks["fleet159"] + '}} ships={997={' + blocks["ship997"]
                + '}} ship_design={1379={' + blocks["design1379"] + '}}')
        self.save = self.folder / "derived-blocks.zip"
        with zipfile.ZipFile(self.save, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("gamestate", text)
        self.base = c.read_save(self.save)
        intercepts = {key: 0 for key in c.collector.MODIFIERS}
        intercepts.update(ship_hull_add=-70000, ship_hull_mult=2.132, ship_armor_mult=.74,
                          ship_shield_mult=3, ship_weapon_damage=4.05, ship_tracking_add=15,
                          ship_hull_regen_add_static=1.392, ship_armor_regen_add_static=2.088)
        # These are explicit arithmetic test inputs, never a claim about a future native C0 export.
        self.base["ship_variables"] = {"eep_probe_" + key: value for key, value in intercepts.items()}
        self.base["ship_variables"].update(eep_probe_max_hull=93960, eep_probe_max_armor=44787.6)

    def tearDown(self):
        self.tmp.cleanup()

    def evolved(self, matter, ranks, rewards=None):
        state = copy.deepcopy(self.base)
        reward = sum(ranks) if rewards is None else rewards
        cv, fv = state["country_variables"], state["fleet_variables"]
        cv.update(eep_c=matter, eep_mothership_level=matter//10, eep_mothership_next=10-matter%10,
                  eep_component_entitled=matter//50, eep_component_rewards=reward,
                  eep_component_pending=max(matter//50-reward, 0))
        fv.update(eep_applied_level=matter//10, eep_component_rewards=reward)
        for key, value in zip(c.TIERS, ranks):
            cv[key] = fv[key] = value
        if matter//10:
            state["fleet_modifiers"].append({"modifier": "eep_mothership_evolution", "days": -1,
                                             "multiplier": matter//10})
        return state

    def test_original_native_layout_and_c0_counts(self):
        self.assertEqual(self.base["fleet"], 159)
        self.assertEqual(self.base["ship"], 997)
        self.assertEqual(self.base["health"]["max_shield_hitpoints"], 167310)
        self.assertTrue(all(row["passed"] for row in c.counts(self.base, 0)))
        with self.assertRaisesRegex(ValueError, "SHA"):
            c.read_save(self.save, "0"*64)
        self.assertNotIn("runtime_1019", sys.modules)

    def test_fixed_source_deltas_use_actual_baseline_and_all_six_ranks(self):
        state = self.evolved(10000, [40, 30, 20, 50, 25, 35])
        result = c.prediction(self.base, state)
        self.assertEqual(result["max_hitpoints"], 1653960)
        self.assertEqual(result["max_armor_hitpoints"], 1409007.6)
        self.assertEqual(result["max_shield_hitpoints"], 2425995)
        self.assertAlmostEqual(result["eep_probe_ship_weapon_damage"], 56.55)
        self.assertEqual(result["eep_probe_ship_tracking_add"], 90)
        self.assertAlmostEqual(result["eep_probe_ship_hull_regen_add_static"], 108.392)
        self.assertAlmostEqual(result["eep_probe_ship_armor_regen_add_static"], 109.088)
        self.assertEqual(result["eep_probe_ship_hull_add"], -70000)
        self.assertTrue(all(row["passed"] for row in c.counts(state, 10000)))

    def test_integer_mirrors_and_duplicate_reward_modifiers_fail(self):
        state = self.evolved(50, [1, 0, 0, 0, 0, 0])
        self.assertTrue(all(row["passed"] for row in c.counts(state, 50)))
        state["country_variables"][c.TIERS[0]] = 2
        state["fleet_modifiers"].append({"modifier": "eep_component_shield_reward", "days": -1})
        failed = [row["check"] for row in c.counts(state, 50) if not row["passed"]]
        self.assertIn("country mirrors " + c.TIERS[0], failed)
        self.assertIn("fleet has only base and growth modifiers", failed)

    def test_budget_400_pending10_and_410_pending0_are_not_interchanged(self):
        first = self.evolved(20500, [80, 70, 60, 80, 50, 60])
        second = self.evolved(20500, [82, 72, 62, 82, 51, 61])
        self.assertTrue(all(row["passed"] for row in c.counts(first, 20500, 400, 10)))
        self.assertTrue(all(row["passed"] for row in c.counts(second, 20500, 410, 0)))
        self.assertFalse(all(row["passed"] for row in c.counts(second, 20500, 400, 10)))

    def test_native_next_month_and_manual_budget_paths_are_distinct(self):
        before = self.evolved(10000, [40, 35, 30, 40, 25, 30])
        first = self.evolved(20500, [80, 70, 60, 80, 50, 60])
        second = self.evolved(20500, [82, 72, 62, 82, 51, 61])
        before["date"] = first["date"] = "2201.12.01"
        second["date"] = "2202.01.01"
        self.assertEqual(c.budget_comparison(before, first, second, "monthly")["status"], "PASS_SCOPED")
        self.assertEqual(c.budget_comparison(before, first, second, "manual")["status"], "FAIL")
        second["date"] = first["date"]
        self.assertEqual(c.budget_comparison(before, first, second, "monthly")["status"], "FAIL")
        self.assertEqual(c.budget_comparison(before, first, second, "manual")["status"], "PASS_SCOPED")

    def test_single_auto_receipt_needs_no_ui_save_history_fields(self):
        path = self.folder / "auto.receipt.json"
        path.write_text(json.dumps({"date": "2200.01.01", "sha256": c.sha(self.save),
                                    "archived": str(self.save)}), encoding="utf-8")
        state = c.receipt_save(path)
        self.assertEqual(state["date"], "2200.01.01")
        self.assertEqual(state["receipt"]["sha256"], c.sha(path))

    def test_absolute_tolerance_is_fixed_and_missing_exports_do_not_pass(self):
        rows = []
        c.close(rows, "rounded", 10.009, 10)
        c.close(rows, "wrong", 10.011, 10)
        c.close(rows, "missing", None, 0)
        self.assertEqual([row["passed"] for row in rows], [True, False, False])
        self.assertEqual(c.scope(rows)["status"], "FAIL")

    def test_hp_engineering_budget_accepts_predeclared_level1000_and2050_quantization(self):
        rows = []
        for expected in (1331787.6, 2683137.6, 4454628.75):
            observed = struct.unpack(">f", struct.pack(">f", expected))[0]
            c.close_hp(rows, "source-only large HP", observed, expected)
        self.assertTrue(all(row["passed"] for row in rows))
        self.assertEqual([row["ulp32_expected"] for row in rows], [.125, .25, .5])
        self.assertEqual([row["applied_tolerance"] for row in rows], [1, 2, 4])
        self.assertGreater(abs(rows[0]["raw_delta"]), .01)
        self.assertEqual(rows[0]["observed"], 1331787.625)
        self.assertEqual(rows[0]["tolerance_kind"], "hp_binary32_ulp_engineering")

    def test_large_hp_missing_whole_level_or_core_is_rejected(self):
        rows = []
        for expected, one_level, one_core in ((1653960, 1500, 3000),
                                               (2683137.6, 1287, 2574),
                                               (4454628.75, 2091.375, 4182.75)):
            for missing in (one_level, one_core):
                observed = struct.unpack(">f", struct.pack(">f", expected - missing))[0]
                c.close_hp(rows, "missing full source contribution", observed, expected)
        self.assertFalse(any(row["passed"] for row in rows))

    def test_modifier_exports_keep_point_zero_one_and_small_hp_keeps_old_floor(self):
        rows = []
        c.close(rows, "wrong damage component", 56.5, 56.55)
        c.close(rows, "wrong tracking component", 87, 90)
        c.close(rows, "flat hull remains a modifier", -69999.98, -70000)
        c.close_hp(rows, "small old baseline accepted", 100.009, 100)
        c.close_hp(rows, "small old baseline rejected", 100.011, 100)
        self.assertEqual([row["passed"] for row in rows], [False, False, False, True, False])
        self.assertTrue(all(row["applied_tolerance"] == .01 for row in rows))
        self.assertTrue(all(row["tolerance_kind"] == "fixed_absolute" for row in rows[:3]))

    def test_hp_missing_nonfinite_and_out_of_binary32_range_never_get_infinite_tolerance(self):
        rows = []
        for observed, expected in ((None, 100), (math.nan, 100), (math.inf, 100),
                                   (100, math.inf), (1e40, 1e40)):
            c.close_hp(rows, "invalid HP", observed, expected)
        self.assertFalse(any(row["passed"] for row in rows))
        self.assertIsNone(rows[-1]["applied_tolerance"])
        json.dumps(rows, allow_nan=False)

    def test_reload_hp_budget_does_not_relax_modifier_diagnostics(self):
        before = copy.deepcopy(self.base)
        before["health"]["max_armor_hitpoints"] = 1331787.6
        before["ship_variables"]["eep_probe_max_armor"] = 1331787.6
        after = copy.deepcopy(before)
        after["health"]["max_armor_hitpoints"] = 1331787.625
        after["ship_variables"]["eep_probe_max_armor"] = 1331787.625
        self.assertEqual(c.comparison(before, after, "large reload")["status"], "PASS_SCOPED")
        after["ship_variables"]["eep_probe_ship_weapon_damage"] -= .05
        self.assertEqual(c.comparison(before, after, "large reload")["status"], "FAIL")

    def test_reload_business_and_strict_gamestate_are_separate(self):
        after = copy.deepcopy(self.base)
        after.update(design_id=9999, design_body_sha256="different native metadata",
                     gamestate_sha256="different full gamestate")
        result = c.comparison(self.base, after, "reload")
        self.assertEqual(result["status"], "PASS_SCOPED")
        self.assertFalse(result["strict_gamestate_equal"])
        after["fleet_variables"][c.TIERS[0]] = 1
        self.assertEqual(c.comparison(self.base, after, "reload")["status"], "FAIL")

    def test_same_day_repeat_and_reload_keep_government_progress_raw_exact(self):
        before, after = copy.deepcopy(self.base), copy.deepcopy(self.base)
        before["government"] += '\n council_agenda_progress=6750.75\n'
        after["government"] += '\n council_agenda_progress=6808.5\n'
        for name in ("same-day repeated sync", "same-day reload"):
            with self.subTest(name=name):
                result = c.comparison(before, after, name)
                self.assertEqual(result["status"], "FAIL")
                self.assertFalse(next(row["passed"] for row in result["checks"]
                                      if row["check"].endswith("discrete business signature")))

    def test_report_failure_is_preserved_and_never_overwritten(self):
        receipt = self.folder / "bad.json"
        receipt.write_text('{}', encoding="utf-8")
        output = self.folder / "report.json"
        argv = ["report", "--receipt", str(receipt), "--output", str(output)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(argv), 1)
        self.assertEqual(c.load(output)["status"], "FAIL")
        with self.assertRaises(FileExistsError):
            c.main(argv)

    def test_revision_certificates_preserve_formula_objects_and_hp_policy(self):
        folder = c.ROOT / "docs/evidence/1019-analysis"
        models = [c.load(folder / f"six-core-source-expectations-v{i}.json")
                  for i in range(1, len(c.MODEL_HASHES) + 1)]
        self.assertEqual(tuple(c.sha(folder / f"six-core-source-expectations-v{i}.json")
                               for i in range(1, len(c.MODEL_HASHES) + 1)), c.MODEL_HASHES)
        for version, model in enumerate(models[2:], 3):
            for name, value in model["retained_v1_expectations"].items():
                self.assertEqual(value, models[0][name])
            for name, value in model["retained_v2_expectations"].items():
                self.assertEqual(value, models[1][name])
            for region in model["source_equivalence"]:
                self.assertIs(region["exactly_equal"], True)
                self.assertEqual(region["predecessor_sha256"], region[f"rc{version + 2}_sha256"])
            self.assertEqual(model["hp_policy_unchanged"], {
                "hp_tolerance_contract": c.HP_TOLERANCE_CONTRACT,
                "absolute_floor": c.TOLERANCE, "binary32_ulps": c.HP_ULPS, "relative_tolerance": 0,
                "classification": "predeclared_engineering_allowance_not_engine_storage_proof",
                "all_ten_modifier_exports_absolute_tolerance": .01, "ledger_identity_slots": "exact"})


class GovernmentIdentityTests(unittest.TestCase):
    RAW = ('type="gov_machine_intelligence" authority="auth_machine_intelligence" '
           'civics={"civic_machine_terminator"} origin="origin_eep" '
           'unknown_scalar=7 unknown_object={value=8 council_agenda_progress=9} '
           'council_agenda_progress=6750.75')

    def compare(self, raw, same_date=False):
        rows = []
        observation = c.matrix_government_comparison(rows, "stable government",
            {"date": "2201.02.01", "government": self.RAW},
            {"date": "2201.02.01" if same_date else "2201.03.01", "government": raw})
        return rows[0], observation

    def test_cross_month_progress_only_passes_and_raw_difference_is_retained(self):
        row, observed = self.compare(self.RAW.replace("6750.75", "6808.5"))
        self.assertTrue(row["passed"])
        self.assertEqual(observed["mode"], "cross_date_structural_identity")
        self.assertFalse(observed["raw_equal"])
        self.assertTrue(observed["raw_diff"])
        self.assertEqual(observed["progress_delta"], 57.75)
        self.assertEqual(observed["before"]["raw"], self.RAW)
        self.assertEqual(observed["before"]["council_agenda_progress"]["raw"], "6750.75")
        self.assertEqual(observed["before"]["identity"], observed["after"]["identity"])

    def test_real_government_civic_origin_authority_and_unknown_changes_fail(self):
        for old, new in (("gov_machine_intelligence", "gov_hive_mind"),
                         ("auth_machine_intelligence", "auth_hive_mind"),
                         ("civic_machine_terminator", "civic_machine_servitor"),
                         ("origin_eep", "origin_other"), ("unknown_scalar=7", "unknown_scalar=8"),
                         ("value=8", "value=9")):
            with self.subTest(field=old):
                self.assertFalse(self.compare(self.RAW.replace(old, new))[0]["passed"])

    def test_nested_same_named_progress_is_not_excluded(self):
        self.assertFalse(self.compare(self.RAW.replace("council_agenda_progress=9}",
                                                       "council_agenda_progress=10}"))[0]["passed"])

    def test_duplicate_object_or_nonfinite_direct_progress_is_rejected(self):
        for invalid in ("6750.75 council_agenda_progress=6808.5", "{value=6750.75}",
                        "NaN", "inf", "-inf", "1e9999", '"6750.75"', "yes"):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "council_agenda_progress"):
                self.compare(self.RAW.replace("6750.75", invalid))

    def test_same_date_matrix_progress_change_still_fails(self):
        row, observed = self.compare(self.RAW.replace("6750.75", "6808.5"), same_date=True)
        self.assertFalse(row["passed"])
        self.assertEqual(observed["mode"], "same_date_raw_exact")

    def test_unknown_duplicate_fields_and_nested_raw_values_remain_verbatim(self):
        raw = 'unknown=1 unknown=2 nested={ x = 1 council_agenda_progress={bad=yes} }'
        parsed = c.government_identity(raw)
        self.assertEqual(parsed["identity"], [
            {"key": "unknown", "raw": "1", "object": False},
            {"key": "unknown", "raw": "2", "object": False},
            {"key": "nested", "raw": " x = 1 council_agenda_progress={bad=yes} ", "object": True}])
        self.assertEqual(parsed["council_agenda_progress"], {"present": False, "raw": None, "value": None})
        self.assertFalse(self.compare(self.RAW.replace("unknown_scalar=7", "unknown_scalar=7 unknown_scalar=7"))[0]["passed"])


class SourceRevisionTests(unittest.TestCase):
    """Temporary synthetic source indexes, never native Mod acceptance evidence."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eep-source-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "docs/evidence/1019-analysis"
        self.folder.mkdir(parents=True)
        native = self.root / "synthetic-native.txt"
        native.write_text("synthetic native source guard", encoding="utf-8")
        self.native = native
        self.packages = {}
        def sources(label):
            mod = self.root / label
            for index in range(59):
                path = mod / "sources" / (str(index) + ".txt")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(label + " synthetic bytes " + str(index), encoding="utf-8")
            actual = [{"path": path.relative_to(mod).as_posix(), "bytes": path.stat().st_size,
                       "sha256": c.sha(path)} for path in sorted(mod.rglob("*")) if path.is_file()]
            return mod, actual
        historical = sources("historical")
        self.packages[c.HISTORICAL_RC4_TREE] = historical
        models = [{"frozen_rc3": {"selected_frozen_files_verified_against_manifest": historical[1][:6]},
                   "source_evidence": {"native_references": [{"source": str(native), "sha256": c.sha(native)}]}},
                  {"scope": "synthetic second model, no runtime claim"}]
        for tree, (version, frozen_key) in sorted(c.SOURCE_REVISIONS.items(), key=lambda item: item[1][0]):
            mod, actual = sources("revision" + str(version))
            self.packages[tree] = (mod, actual)
            models.append({frozen_key: {"production_tree_sha256": tree, "file_count": 59,
                           "files": actual, "selected_frozen_files_verified_against_manifest": actual[:6]}})
        for index, model in enumerate(models, 1):
            (self.folder / f"six-core-source-expectations-v{index}.json").write_text(json.dumps(model), encoding="utf-8")
        index_path = self.root / "docs/evidence/1019-requirements/rc4-source-copy.json"
        index_path.parent.mkdir(parents=True)
        index_path.write_text(json.dumps({"tree_sha256": c.HISTORICAL_RC4_TREE, "files": historical[1]}), encoding="utf-8")
        self.source_copy = index_path
        self.hashes = tuple(c.sha(self.folder / f"six-core-source-expectations-v{i}.json")
                            for i in range(1, len(models) + 1))
        for option, value in (("ROOT", self.root), ("MODEL_HASHES", self.hashes),
                              ("HISTORICAL_RC4_SOURCE_COPY_SHA", c.sha(index_path))):
            guard = patch.object(c, option, value)
            guard.start()
            self.addCleanup(guard.stop)

    def validate(self, tree=None, actual=None):
        tree = c.SOURCE_TREE if tree is None else tree
        mod, rows = self.packages.get(tree, self.packages[c.SOURCE_TREE])
        c.validate_source_package(mod, rows if actual is None else actual, tree)

    def test_each_reviewed_tree_uses_its_exact_index_and_model_prefix(self):
        for tree, (version, _) in c.SOURCE_REVISIONS.items():
            self.validate(tree)
            self.assertEqual(c.applicable_model_hashes(tree), self.hashes[:version])
        self.validate(c.HISTORICAL_RC4_TREE)
        self.assertEqual(c.applicable_model_hashes(c.HISTORICAL_RC4_TREE), self.hashes[:2])

    def test_unknown_tree_cannot_register_itself_from_an_index(self):
        with self.assertRaisesRegex(ValueError, "no predeclared"):
            self.validate("0" * 64)

    def test_selected_and_unselected_source_changes_both_fail(self):
        for index in (0, 58):
            actual = copy.deepcopy(self.packages[c.SOURCE_TREE][1])
            actual[index]["sha256"] = "0" * 64
            with self.subTest(index=index), self.assertRaisesRegex(ValueError, "exact predeclared"):
                self.validate(actual=actual)

    def test_changed_selected_disk_bytes_cannot_hide_behind_the_supplied_index(self):
        mod, actual = self.packages[c.SOURCE_TREE]
        (mod / actual[0]["path"]).write_text("unknown modified source", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no longer applies"):
            self.validate()

    def test_missing_file_or_duplicate_index_fails(self):
        actual = self.packages[c.SOURCE_TREE][1]
        for rows in (actual[:-1], [*actual[:-1], actual[0]]):
            with self.assertRaisesRegex(ValueError, "exact predeclared"):
                self.validate(actual=rows)

    def test_changed_or_missing_revision_certificate_fails(self):
        path = self.folder / f"six-core-source-expectations-v{len(self.hashes)}.json"
        raw = path.read_bytes()
        path.write_bytes(raw + b"\n")
        with self.assertRaisesRegex(ValueError, "models changed"):
            self.validate()
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            self.validate()

    def test_historical_index_and_native_source_remain_byte_bound(self):
        self.source_copy.write_bytes(self.source_copy.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "historical RC4 source index changed"):
            self.validate(c.HISTORICAL_RC4_TREE)
        self.native.write_text("unknown native source", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "native source model bytes changed"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
