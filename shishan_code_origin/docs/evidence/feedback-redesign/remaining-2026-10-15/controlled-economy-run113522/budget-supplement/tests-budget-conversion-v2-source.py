"""Synthetic conversion counterexamples only; no native save is created."""
from pathlib import Path
import importlib.util
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


subject = load("budget_conversion_development", ROOT / "tools/audit_additive_budget_conversion.py")
helper = load("budget_conversion_input_helper", ROOT / "tests/test_additive_budget_supplement.py")


def fixture():
    report, graph = helper.data(), helper.graph()
    graph["definitions"]["planet_civilians"] = [{"parent": "planet_jobs", "error": None}]
    graph["definitions"]["pop_category_civilians"] = [{"parent": "planet_pops", "error": None}]
    graph["definitions"]["trade_policy"] = [{"parent": None, "error": None}]
    policies = [[{"key": "policy", "value": "trade_policy"}, {"key": "selected", "value": "trade_policy_default"}]]
    job_values = {"F00": "80", "F10": "112", "F01": "108", "F11": "140", "FP": "144", "FN": "144", "FH": "144"}
    for branch, phases in report["snapshots"].items():
        for snapshot in phases.values():
            snapshot["context"]["policies"] = policies
            budget = snapshot["budget"]["last_month"]
            budget["income"]["planet_civilians"] = {"trade": job_values[branch]}
            budget["income"]["pop_category_civilians"] = {"trade": "8"}
            total = subject.D(job_values[branch]) + 8
            budget["expenses"]["trade_policy"] = {"trade": str(total)}
            budget["income"]["trade_policy"] = {"trade": str(total / 2), "energy": str(total / 2)}
    report["common_snapshot"]["context"]["policies"] = policies
    source = {"status": "PASS", "option": "trade_policy_default", "coefficients": {"trade": ".5", "energy": ".5"}, "kind": "development source, not native"}
    return report, graph, source


class ConversionDevelopmentTests(unittest.TestCase):
    def test_verified_conversion_is_separate_and_v1_fail_is_preserved(self):
        result = subject.derive_v2(*fixture())
        self.assertEqual("PASS", result["status"])
        self.assertEqual("FAIL", result["v1_status_preserved"])
        self.assertEqual(subject.D(80), subject.D(result["derived_conversion"]["job_trade_response"]["Q0"]))
        self.assertTrue(all(r["category"] != "trade_policy" for r in result["ordinary_expenses"]))
        self.assertEqual(3, len(result["trade_policy_v1_rows_preserved"]))

    def test_wrong_input_throughput_fails(self):
        report, graph, source = fixture()
        report["snapshots"]["FH"]["measured"]["budget"]["last_month"]["expenses"]["trade_policy"]["trade"] = "153"
        self.assertEqual("FAIL", subject.derive_v2(report, graph, source)["status"])

    def test_wrong_output_share_fails(self):
        report, graph, source = fixture()
        report["snapshots"]["FN"]["measured"]["budget"]["last_month"]["income"]["trade_policy"]["energy"] = "76.01"
        self.assertEqual("FAIL", subject.derive_v2(report, graph, source)["status"])

    def test_unknown_policy_is_not_covered(self):
        report, graph, source = fixture()
        source["option"] = "unreviewed_trade_policy"
        self.assertEqual("NOT COVERED", subject.derive_v2(report, graph, source)["status"])

    def test_missing_or_extra_conversion_output_is_not_zero(self):
        for missing in (True, False):
            report, graph, source = fixture()
            table = report["snapshots"]["FP"]["measured"]["budget"]["last_month"]["income"]["trade_policy"]
            if missing:
                del table["trade"]
            else:
                table["consumer_goods"] = "1"
            self.assertEqual("NOT COVERED", subject.derive_v2(report, graph, source)["status"])

    def test_ordinary_fee_drift_is_never_exempt(self):
        report, graph, source = fixture()
        report["snapshots"]["FP"]["measured"]["budget"]["last_month"]["expenses"]["planet_pops"]["energy"] = "3.01"
        self.assertEqual("FAIL", subject.derive_v2(report, graph, source)["status"])

    def test_other_nonjob_income_drift_is_never_exempt(self):
        report, graph, source = fixture()
        report["snapshots"]["FP"]["measured"]["budget"]["last_month"]["income"]["country_base"]["energy"] = "25.01"
        self.assertEqual("FAIL", subject.derive_v2(report, graph, source)["status"])


if __name__ == "__main__":
    unittest.main()
