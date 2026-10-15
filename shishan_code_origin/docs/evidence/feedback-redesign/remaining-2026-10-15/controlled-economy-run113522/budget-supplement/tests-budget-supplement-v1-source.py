"""Development inputs only. No native saves, primary tests or GUI are run."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


subject = load("budget_supplement_development", ROOT / "tools/audit_additive_budget_supplement.py")
# Only reuse its explicitly development-only data constructor; do not run cases.
helpers = load("budget_supplement_input_constructor", ROOT / "tests/test_additive_runtime_matrix.py")


def data():
    snapshots = helpers.development_matrix()
    for phases in snapshots.values():
        for snapshot in phases.values():
            expenses = snapshot["budget"]["last_month"]["expenses"]
            expenses["planet_pops"] = {"energy": "3"}
            expenses["leader_officials"] = {"energy": "4"}
    return {"status": "PASS", "limited_economy": {"status": "PASS"},
            "strict_cache_audit": {"status": "PASS"}, "setup_input_audit": {"status": "PASS"},
            "snapshots": snapshots, "common_snapshot": copy.deepcopy(snapshots["F00"]["input"])}


def graph():
    parents = {"country": None, "planets": "country", "planet_jobs": "planets",
               "planet_biologists": "planet_jobs", "planet_pops": "planets",
               "leaders": "country", "leader_officials": "leaders", "country_base": "country"}
    return {"definitions": {key: [{"parent": parent, "error": None, "category": key}]
                            for key, parent in parents.items()}, "files": []}


def row(result, kind, category, resource):
    return next(r for r in result[kind] if r["category"] == category and r["resource"] == resource)


class BudgetSupplementDevelopmentTests(unittest.TestCase):
    def test_raw_q_and_nonzero_fee_sources_are_observed(self):
        result = subject.derive(data(), graph())
        self.assertEqual("PASS", result["status"])
        self.assertEqual(subject.D("1.353"), subject.D(row(result, "income", "planet_biologists", "unity")["response"]["Q0"]))
        self.assertEqual("PASS", result["focused_expense_coverage"]["population_upkeep"]["status"])
        self.assertEqual("PASS", result["focused_expense_coverage"]["leader_officials"]["status"])

    def test_population_fee_difference_fails_without_normalization(self):
        report = data()
        report["snapshots"]["FH"]["measured"]["budget"]["last_month"]["expenses"]["planet_pops"]["energy"] = "3.01"
        result = subject.derive(report, graph())
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("FAIL", row(result, "expenses", "planet_pops", "energy")["arithmetic_status"])

    def test_missing_leader_fee_never_becomes_zero(self):
        report = data()
        del report["snapshots"]["FN"]["measured"]["budget"]["last_month"]["expenses"]["leader_officials"]
        found = row(subject.derive(report, graph()), "expenses", "leader_officials", "energy")
        self.assertEqual("NOT COVERED", found["status"])
        self.assertNotIn("FN", found["values"])

    def test_zero_job_response_is_not_positive_bonus_evidence(self):
        report = data()
        for phases in report["snapshots"].values():
            phases["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["unity"] = "10"
        found = row(subject.derive(report, graph()), "income", "planet_biologists", "unity")
        self.assertEqual("NOT COVERED", found["status"])
        self.assertEqual(subject.D(0), subject.D(found["response"]["Q0"]))

    def test_secondary_or_independent_raw_difference_is_not_swallowed(self):
        report = data()
        report["snapshots"]["FP"]["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["society_research"] = "999"
        self.assertEqual("FAIL", subject.derive(report, graph())["status"])

    def test_unknown_and_mixed_income_sources_are_not_inferred(self):
        for name in ("unknown_source", "planets"):
            report = data()
            for phases in report["snapshots"].values():
                phases["measured"]["budget"]["last_month"]["income"][name] = {"energy": "100"}
            self.assertEqual("NOT COVERED", row(subject.derive(report, graph()), "income", name, "energy")["status"])

    def test_parent_duplicates_cycles_and_unknown_parent_fail_closed(self):
        for mode in ("duplicate", "cycle", "unknown"):
            source = graph()
            if mode == "duplicate":
                source["definitions"]["planet_biologists"] *= 2
            else:
                source["definitions"]["planet_biologists"][0]["parent"] = "planet_biologists" if mode == "cycle" else "absent"
            self.assertEqual("NOT COVERED", subject.classify("planet_biologists", source)["status"])

    def test_primary_invalid_and_zero_only_fees_cannot_turn_into_pass(self):
        report = data()
        report["status"] = "INVALID"
        result = subject.derive(report, graph())
        self.assertEqual("INVALID", result["status"])
        self.assertEqual("PASS", result["arithmetic_status"])
        report = data()
        for phases in report["snapshots"].values():
            phases["measured"]["budget"]["last_month"]["expenses"]["leader_officials"]["energy"] = "0"
        self.assertEqual("NOT COVERED", row(subject.derive(report, graph()), "expenses", "leader_officials", "energy")["status"])

    def test_no_growth_additional_guard_checks_all_domestic_jobs(self):
        report = data()
        for phases in report["snapshots"].values():
            for phase in subject.PHASES:
                job = copy.deepcopy(phases[phase]["jobs"][0])
                job.update(id=9, type="civilian", workforce="10", bonus_workforce="0")
                job["allocations"][0]["amount"] = "10"
                if phase == "warm":
                    job["workforce"] = job["allocations"][0]["amount"] = "11"
                phases[phase]["jobs"].append(job)
        self.assertEqual("INVALID", subject.derive(report, graph())["status"])


if __name__ == "__main__":
    unittest.main()
