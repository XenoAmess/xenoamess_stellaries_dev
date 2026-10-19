"""Pending-only index collection; all input bytes here are synthetic fixtures."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import runtime_index_1019 as progress
import test_publish_1019 as fixtures


class PendingIndexCollectorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.Release1019Guards("test_complete_synthetic_input_and_later_release_candidate")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.data = copy.deepcopy(self.fixture.runtime)
        self.data["status"] = "PENDING"
        self.data["component_rewards"]["status"] = "PENDING"
        for case in self.data["cases"].values():
            case["status"] = "PENDING"
            case["checks"] = {name: None for name in case["checks"]}
        for budget in self.data["economy"].values():
            budget["candidate_months"], budget["baseline_months"] = [], []
        self.index = self.fixture.json("docs/evidence/progress.json", self.data)

    def read(self):
        return progress.load_progress(self.index, self.root)[1]

    def test_attachment_is_idempotent_and_cannot_promote_cases(self):
        source = self.fixture.evidence[0]
        operation = lambda data: progress.attach(data, "hive_startup", "synthetic-run", source["kind"], source["path"], self.root)
        # This reference already exists in the fixture: repeating it changes nothing.
        self.assertFalse(progress.update_progress(self.index, self.root, "attach", operation)["changed"])
        self.assertEqual(self.read()["cases"]["hive_startup"]["status"], "PENDING")
        with self.assertRaisesRegex(RuntimeError, "cannot accept"):
            progress.update_progress(self.index, self.root, "illegal", lambda data: data.update(status="PASS_SCOPED"))
        self.assertEqual(self.read()["status"], "PENDING")

    def test_individual_observation_always_keeps_whole_case_pending(self):
        key = next(iter(self.data["cases"]["hive_startup"]["checks"]))
        source = next(entry["path"] for entry in self.fixture.evidence if entry["kind"] == "analysis")
        progress.update_progress(self.index, self.root, "observe-check", lambda data: progress.observe_check(
            data, "hive_startup", key, True, source, "synthetic-run", self.root))
        data = self.read()
        self.assertIs(data["cases"]["hive_startup"]["checks"][key], True)
        self.assertEqual(data["cases"]["hive_startup"]["status"], "PENDING")
        self.assertEqual(data["component_rewards"]["status"], "PENDING")
        self.assertEqual(len(data["_progress"]["history"]), 1)
        with self.assertRaises(RuntimeError):
            progress.observe_check(data, "hive_startup", "not-a-check", True, source, "synthetic-run", self.root)

    def test_budget_imports_real_report_value_and_preserves_negative_energy(self):
        save = next(entry for entry in self.fixture.evidence if entry["kind"] == "native_save")
        self.fixture.json("proofs/month.json", {"status": "OBSERVATION_ONLY", "date": "2200.02.01",
            "save_sha256": save["sha256"], "energy": {"current_month": {"balance": -2.75}}})
        progress.update_progress(self.index, self.root, "budget", lambda data: progress.add_budget(
            data, "machine", "candidate", "proofs/month.json", save["path"], self.root, "synthetic-run"))
        row = self.read()["economy"]["machine"]["candidate_months"][0]
        self.assertEqual(row["net_energy"], -2.75)
        self.assertEqual(row["evidence"]["sha256"], save["sha256"])
        bad = self.fixture.json("proofs/wrong.json", {"status": "OBSERVATION_ONLY", "date": "2200.03.01",
            "save_sha256": "0" * 64, "energy": {"current_month": {"balance": 100}}})
        with self.assertRaisesRegex(RuntimeError, "save SHA differs"):
            progress.add_budget(self.read(), "machine", "candidate", bad.relative_to(self.root).as_posix(), save["path"], self.root, "synthetic-run")

    def test_old_run_and_unknown_case_cannot_be_attached(self):
        run = json.loads((self.root / "proofs/manifest.json").read_text())
        for field, value in (("profile_id", "historical-profile"), ("static_gate", {})):
            self.fixture.json("proofs/old-run.json", {**run, field: value})
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, "does not bind"):
                progress.bind_run(self.read(), "proofs/old-run.json", self.root)
        with self.assertRaisesRegex(RuntimeError, "register"):
            progress.attach(self.read(), "hive_startup", "unknown-run", "analysis", self.fixture.evidence[0]["path"], self.root)

    def test_changed_evidence_is_rejected_without_rebinding_the_index(self):
        source = self.fixture.evidence[0]
        self.fixture.write(source["path"], b"changed synthetic evidence")
        before = self.index.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "bytes changed"):
            progress.update_progress(self.index, self.root, "attach", lambda data: progress.attach(
                data, "hive_startup", "synthetic-run", source["kind"], source["path"], self.root))
        self.assertEqual(before, self.index.read_bytes())

    def test_final_and_nonpending_indexes_are_protected(self):
        final = self.fixture.json("docs/evidence/final-result.json", self.data)
        with self.assertRaisesRegex(RuntimeError, "final acceptance"):
            progress.load_progress(final, self.root)
        data = self.read(); data["cases"]["hive_startup"]["status"] = "PASS_SCOPED"
        self.fixture.json("docs/evidence/progress.json", data)
        with self.assertRaisesRegex(RuntimeError, "wholly PENDING"):
            progress.load_progress(self.index, self.root)

    def test_source_bindings_cannot_be_rewritten_by_a_progress_operation(self):
        original = self.index.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "frozen source bindings"):
            progress.update_progress(self.index, self.root, "bad-source-change", lambda data: data.update(version="0.4.0-rc.99"))
        self.assertEqual(self.index.read_bytes(), original)

    def test_missing_summary_never_claims_pass(self):
        summary = progress.missing(self.read())
        self.assertEqual(summary["status"], "PENDING")
        self.assertTrue(summary["cases"]["hive_startup"]["missing_or_failed_checks"])
        self.assertEqual(summary["months"]["machine"]["candidate"], 0)


if __name__ == "__main__":
    unittest.main()
