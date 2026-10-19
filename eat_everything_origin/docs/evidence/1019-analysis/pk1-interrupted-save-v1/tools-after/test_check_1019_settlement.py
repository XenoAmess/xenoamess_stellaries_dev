"""Settlement-only regression checks using genuine recovered native observations.

Negative inputs modify in-memory observations, never source SAV files.
"""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check_1019 as checker

EVIDENCE = ROOT / "docs/evidence/1019-analysis"


def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


class SettlementLiveness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = read("rc3-pk1queued-observation-v1.json")
        cls.after = read("rc3-pk1-recovered-fired-observation-v1.json")
        cls.case = read("pk1-queued-recovered-fired-settlement-case-v1.json")

    def evaluate(self, after=None):
        return checker.settlement(self.case, self.before, after or self.after)

    def reject(self, modify):
        observed = copy.deepcopy(self.after)
        modify(observed["worlds_1019"]["17"])
        result = self.evaluate(observed)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["checks"]["source_colony_destroyed"])

    def test_real_native_retained_colony_cache_is_not_live(self):
        source = self.after["worlds_1019"]["17"]
        self.assertEqual(source["native"]["colony"], 1)
        self.assertGreater(source["colony_native"]["civilian"], 0)
        self.assertIn("species_information", source["colony_raw"])
        result = self.evaluate()
        self.assertEqual(result["status"], "PASS_SCOPED")
        self.assertTrue(all(result["actual"]["source_colony_liveness"].values()))

    def test_original_checker_retains_real_native_failure(self):
        old_path = EVIDENCE / "pk1-readonly-toolchain-v1/tools/check_1019.py"
        spec = importlib.util.spec_from_file_location("pk1_original_settlement_checker", old_path)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        result = old.settlement(self.case, self.before, self.after)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual([k for k, v in result["checks"].items() if not v],
                         ["source_colony_destroyed"])

    def test_reference_may_also_be_absent(self):
        observed = copy.deepcopy(self.after)
        del observed["worlds_1019"]["17"]["native"]["colony"]
        self.assertEqual(self.evaluate(observed)["status"], "PASS_SCOPED")

    def test_owner_is_not_ignored(self):
        self.reject(lambda w: w["native"].update(owner=1))

    def test_controller_is_not_ignored(self):
        self.reject(lambda w: w["native"].update(controller=1))

    def test_actual_population_is_not_ignored(self):
        self.reject(lambda w: w.update(actual_pop_sum=1))

    def test_actual_population_group_is_not_ignored(self):
        self.reject(lambda w: w["pop_groups"].update({"999": {"native": {"size": 1}}}))

    def test_colony_population_group_list_is_not_ignored(self):
        self.reject(lambda w: w.update(colony_raw=w["colony_raw"] + "\npop_groups={999}\n"))

    def test_actual_job_list_is_not_ignored(self):
        self.reject(lambda w: w.update(colony_raw=w["colony_raw"] + "\npop_jobs={999}\n"))

    def test_live_population_counter_is_not_ignored(self):
        self.reject(lambda w: w["colony_native"].update(num_sapient_pops=1))

    def test_live_employable_counter_is_not_ignored(self):
        self.reject(lambda w: w["colony_native"].update(employable_pops=1))

    def test_wrong_planet_class_is_not_ignored(self):
        self.reject(lambda w: w["native"].update(planet_class="pc_alpine"))

    def test_only_settlement_function_source_changed(self):
        before = (EVIDENCE / "pk1-interrupted-save-v1/tools-before/check_1019.py").read_bytes()
        after = (ROOT / "tools/check_1019.py").read_bytes()

        def masked(raw):
            node = next(n for n in ast.parse(raw.decode("utf-8")).body
                        if isinstance(n, ast.FunctionDef) and n.name == "settlement")
            lines = raw.splitlines(keepends=True)
            return b"".join(lines[:node.lineno - 1]) + b"SETTLEMENT\n" + b"".join(lines[node.end_lineno:])

        self.assertEqual(masked(before), masked(after))


if __name__ == "__main__":
    unittest.main()
