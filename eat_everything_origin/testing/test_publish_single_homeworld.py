"""Exercise missing/changed runtime evidence and formal-package drift guards."""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import publish_single_homeworld as release


class SingleHomeworldReleaseGuards(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        proof = self.root / "proof.json"
        proof.write_text('{"synthetic_guard_test": true}', encoding="utf-8")
        entry = {"path": "proof.json", "sha256": hashlib.sha256(proof.read_bytes()).hexdigest()}
        self.runtime = {"schema": "eep-single-homeworld-acceptance-v1", "status": "PASS_SCOPED",
                        "version": release.CANDIDATE_VERSION, "language": "l_simp_chinese",
                        "game_exe_sha256": release.update.EXE_SHA, "fully_accepted_civics": [],
                        "cases": {key: {"status": "PASS_SCOPED", "evidence": [entry]} for key in release.CASES},
                        "economy": {key: {"baseline_months": 12, "candidate_months": 12,
                                          "candidate_energy_nonnegative_all_months": True}
                                    for key in ("hive", "machine", "purifier")},
                        "additional_checks": {"lithoid_startup_first_month": {"status": "PASS_SCOPED", "evidence": [entry]}},
                        "archives": [entry]}

    def test_complete_synthetic_guard_input(self):
        release.validate_runtime_index(self.runtime, self.root)

    def test_reject_missing_failed_or_wrong_scope(self):
        for field, value in (("status", "PENDING"), ("version", "0.3.1"),
                             ("language", "l_english"), ("fully_accepted_civics", ["all"])):
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                release.validate_runtime_index({**self.runtime, field: value}, self.root)
        bad = copy.deepcopy(self.runtime)
        del bad["cases"]["old_save_compatibility"]
        with self.assertRaises(RuntimeError):
            release.validate_runtime_index(bad, self.root)
        for value in ({}, {"lithoid_startup_first_month": {"status": "FAIL", "evidence": []}}):
            with self.subTest(variant=value), self.assertRaises(RuntimeError):
                release.validate_runtime_index({**self.runtime, "additional_checks": value}, self.root)

    def test_reject_incomplete_or_negative_economy(self):
        for field, value in (("candidate_months", 11), ("baseline_months", 0),
                             ("candidate_energy_nonnegative_all_months", False)):
            bad = copy.deepcopy(self.runtime)
            bad["economy"]["machine"][field] = value
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                release.validate_runtime_index(bad, self.root)

    def test_reject_changed_or_external_proof(self):
        (self.root / "proof.json").write_text("changed", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            release.validate_runtime_index(self.runtime, self.root)
        for path in ("../outside.json", str((self.root / "proof.json").resolve())):
            with self.subTest(path=path), self.assertRaises((RuntimeError, ValueError, FileNotFoundError)):
                release.verify_references([{"path": path, "sha256": "x"}], self.root)

    def test_only_version_metadata_may_differ(self):
        candidate = f'version="{release.CANDIDATE_VERSION}"\nname="test"\n'
        digest = release.update.digest
        runtime = {"production_files": {"descriptor.mod": digest(candidate.encode()), "body.txt": digest(b"body")},
                   "candidate_descriptor": candidate}
        files = {**runtime["production_files"], "descriptor.mod": digest(candidate.replace(release.CANDIDATE_VERSION, release.VERSION).encode())}
        release.validate_candidate_files(files, runtime)
        for bad in ({**files, "body.txt": digest(b"changed")}, {**files, "extra.txt": digest(b"extra")},
                    {**files, "descriptor.mod": digest(b'version="0.3.3"')}):
            with self.assertRaises(RuntimeError):
                release.validate_candidate_files(bad, runtime)


if __name__ == "__main__":
    unittest.main()
