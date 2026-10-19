"""Offline intake boundaries; no synthetic SAV or game actions are created."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import receive_functional_1019 as receiver


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def write(self, name, value):
        path = self.directory / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_template_has_eighteen_groups_and_no_future_true(self):
        value = receiver.template()
        self.assertEqual(len(value["final_case_matrix"]), 18)
        self.assertTrue(all(row["status"] == "PENDING" for row in value["final_case_matrix"].values()))
        self.assertTrue(all(check is None for row in value["final_case_matrix"].values()
                            for check in row["checks"].values()))
        self.assertIsNone(value["expected_tree_sha256"])

    def test_template_cannot_be_received(self):
        with self.assertRaisesRegex(ValueError, "actual run"):
            receiver.receive(receiver.template(), self.directory / "cache")

    def test_exact_reference_detects_file_change(self):
        path = self.write("evidence.json", {"a": 1})
        ref = {"path": str(path), "sha256": receiver.digest(path)}
        self.assertEqual(receiver.reference(ref), path)
        path.write_text('{"a":2}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA changed"):
            receiver.reference(ref)

    def test_no_overwrite(self):
        path = self.directory / "fixed.json"
        receiver.write_new(path, {"first": 1})
        with self.assertRaises(FileExistsError):
            receiver.write_new(path, {"second": 2})
        self.assertEqual(receiver.read(path), {"first": 1})

    def test_gate_is_parsed_without_importing_it(self):
        self.assertNotIn("publish_1019", sys.modules)
        contract = receiver.case_contract()
        self.assertIn("owned_noncore_colony_fire", contract["colossus_enemy_fire"])
        self.assertIn("colonizing_rejected", contract["colossus_guards"])
        self.assertIn("no_extra_civilian_queue", contract["repeat_initialization"])
        self.assertNotIn("publish_1019", sys.modules)

    def manifest(self):
        value = {"schema": "xenoamess.stellaris.acceptance-run.v1", "run_id": "test-run",
                 "repository_mod_tree_sha256": "a" * 64, "copied_mod_tree_sha256": "a" * 64,
                 "language": "l_simp_chinese", "game_exe_sha256": receiver.EXE_SHA,
                 "static_gate": {"status": "PASS", "version": "0.4.0-rc.7"},
                 "profile_id": "eep-0.4.0-single-production-mod", "enabled_mods": ["mod/ugc_eep-1019.mod"]}
        intake = {"expected_run_id": "test-run", "expected_tree_sha256": "a" * 64,
                  "expected_version": "0.4.0-rc.7"}
        return value, intake

    def test_manifest_rejects_wrong_run_tree_version_language(self):
        value, intake = self.manifest()
        for key, wrong in [("run_id", "another-run"), ("copied_mod_tree_sha256", "b" * 64),
                           ("language", "l_english"), ("game_exe_sha256", "c" * 64)]:
            changed = copy.deepcopy(value)
            changed[key] = wrong
            path = self.write(key + ".json", changed)
            with self.subTest(key=key), self.assertRaises(ValueError):
                receiver.package({"path": str(path), "sha256": receiver.digest(path)}, intake)
        changed = copy.deepcopy(value)
        changed["static_gate"]["version"] = "0.4.0-rc.6"
        path = self.write("version.json", changed)
        with self.assertRaisesRegex(ValueError, "version"):
            receiver.package({"path": str(path), "sha256": receiver.digest(path)}, intake)

    def test_additional_run_requires_explicit_allowlist(self):
        value, intake = self.manifest()
        value["run_id"] = "restart-run"
        path = self.write("restart.json", value)
        ref = {"path": str(path), "sha256": receiver.digest(path)}
        with self.assertRaisesRegex(ValueError, "run not"):
            receiver.package(ref, intake)
        intake["additional_run_ids"] = ["restart-run"]
        self.assertEqual(receiver.package(ref, intake)[1]["run_id"], "restart-run")

    def cache_inputs(self):
        bound = {"save": self.directory / "not-created-native-path.sav", "save_sha256": "a" * 64,
                 "manifest_sha256": "b" * 64, "date": "2200.01.01"}
        observation = {"status": "OBSERVATION_ONLY", "save_sha256": "a" * 64,
                       "manifest_sha256": "b" * 64, "date": "2200.01.01", "worlds_1019": {"4": {}}}
        return bound, observation

    def test_observation_cache_reuses_only_identical_identity(self):
        bound, observation = self.cache_inputs()
        calls = []
        def observe(path, worlds):
            calls.append((path, worlds))
            return observation
        first, ref = receiver.cached_observation(bound, [4], self.directory, observe)
        second, next_ref = receiver.cached_observation(bound, [4], self.directory, observe)
        self.assertEqual(len(calls), 1)
        self.assertEqual(first, second)
        self.assertFalse(ref["reused"])
        self.assertTrue(next_ref["reused"])

    def test_changed_cache_is_rejected_without_reparse_or_overwrite(self):
        bound, observation = self.cache_inputs()
        _, ref = receiver.cached_observation(bound, [4], self.directory, lambda *_: observation)
        path = Path(ref["path"])
        changed = receiver.read(path)
        changed["observation"]["date"] = "2201.01.01"
        path.write_text(json.dumps(changed), encoding="utf-8")
        fixed_bytes = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "cache changed"):
            receiver.cached_observation(bound, [4], self.directory,
                                        lambda *_: self.fail("corruption must not trigger fallback reparse"))
        self.assertEqual(fixed_bytes, path.read_bytes())

    def test_missing_physical_world_cannot_fill_zero_or_write_cache(self):
        bound, observation = self.cache_inputs()
        with self.assertRaisesRegex(ValueError, "world missing"):
            receiver.cached_observation(bound, [5], self.directory, lambda *_: observation)
        self.assertEqual(list(self.directory.glob("*.json")), [])

    def test_unknown_task_and_missing_role_cannot_pass(self):
        with self.assertRaisesRegex(ValueError, "unknown task"):
            receiver.execute_task({"kind": "native-fire"}, {}, {})
        with self.assertRaises(KeyError):
            receiver.execute_task({"kind": "compare", "before": "missing", "after": "missing"}, {}, {})

    def test_original_strict_function_gets_no_relaxation_argument(self):
        before, after = {"date": "2200.01.01"}, {"date": "2200.01.02"}
        with patch.object(receiver.original, "compare", return_value={"status": "FAIL"}) as compare:
            result = receiver.execute_task({"kind": "compare", "before": "b", "after": "a"},
                                           {"b": before, "a": after}, {})
        compare.assert_called_once_with(before, after)
        self.assertEqual(result["status"], "FAIL")

    def test_missing_intake_writes_incomplete(self):
        output = self.directory / "result.json"
        code = receiver.main(["receive", "--intake", str(self.directory / "absent.json"),
                              "--cache-dir", str(self.directory / "cache"), "--output", str(output)])
        self.assertEqual(code, 2)
        self.assertEqual(receiver.read(output)["status"], "INCOMPLETE")


class ActualNativeReceiptTests(unittest.TestCase):
    """Use an immutable real SAV for role validation; no new SAV is written."""
    RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")

    def setUp(self):
        if not (self.RUN / "r6mcinit2.sav").exists():
            self.skipTest("fixed local native fixture is unavailable")
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        manifest = self.RUN / "manifest.json"
        self.intake = {"expected_run_id": "20261019T150008Z",
                       "expected_tree_sha256": "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a",
                       "expected_version": "0.4.0-rc.6",
                       "manifest": {"path": str(manifest), "sha256": receiver.digest(manifest)}}
        self.role = {"kind": "native_ui_save"}
        for key, suffix in [("save", ".sav"), ("receipt", ".native-save.json"), ("audit", ".audit.json")]:
            path = self.RUN / ("r6mcinit2" + suffix)
            self.role[key] = {"path": str(path), "sha256": receiver.digest(path)}

    def changed_receipt(self, value):
        path = self.directory / "changed-receipt.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        self.role["receipt"] = {"path": str(path), "sha256": receiver.digest(path)}

    def test_real_exact_ui_save_role(self):
        bound = receiver.validate_role(self.role, self.intake)
        self.assertEqual(bound["date"], "2201.01.01")
        self.assertEqual(bound["save"], (self.RUN / "r6mcinit2.sav").resolve())

    def test_equal_sha_another_name_receipt_is_rejected(self):
        receipt = self.RUN / "r6mcyearui.native-save.json"
        self.assertEqual(receiver.read(receipt)["sha256"], self.role["save"]["sha256"])
        self.role["receipt"] = {"path": str(receipt), "sha256": receiver.digest(receipt)}
        with self.assertRaisesRegex(ValueError, "exact archived SAV"):
            receiver.validate_role(self.role, self.intake)

    def test_autosave_must_postdate_command(self):
        value = receiver.read(self.RUN / "r6mcinit2.native-save.json")
        value.update(source="actual-auto-source", command_started_ns=20, source_mtime_ns=19)
        self.changed_receipt(value)
        self.role["kind"] = "native_autosave"
        with self.assertRaisesRegex(ValueError, "newer"):
            receiver.validate_role(self.role, self.intake)

    def test_ui_save_cannot_be_invented_from_autosave_fields(self):
        value = receiver.read(self.RUN / "r6mcinit2.native-save.json")
        del value["written_at"]
        del value["history"]
        self.changed_receipt(value)
        with self.assertRaisesRegex(ValueError, "UI-save receipt"):
            receiver.validate_role(self.role, self.intake)


if __name__ == "__main__":
    unittest.main()
