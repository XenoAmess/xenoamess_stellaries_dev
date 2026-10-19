"""Offline original-block parsing and independently fixed growth arithmetic checks."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
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

    def test_reload_business_and_strict_gamestate_are_separate(self):
        after = copy.deepcopy(self.base)
        after.update(design_id=9999, design_body_sha256="different native metadata",
                     gamestate_sha256="different full gamestate")
        result = c.comparison(self.base, after, "reload")
        self.assertEqual(result["status"], "PASS_SCOPED")
        self.assertFalse(result["strict_gamestate_equal"])
        after["fleet_variables"][c.TIERS[0]] = 1
        self.assertEqual(c.comparison(self.base, after, "reload")["status"], "FAIL")

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


if __name__ == "__main__":
    unittest.main()
