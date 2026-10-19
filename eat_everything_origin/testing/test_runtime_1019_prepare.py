"""Prepare guards use a fake base; never import native UI or create a live run."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import test_publish_1019 as fixtures


class RuntimePrepareNumericTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.Release1019Guards("test_complete_synthetic_input_and_later_release_candidate")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.report = copy.deepcopy(self.fixture.report)
        self.report_path = self.fixture.json("prepare/report.json", self.report)
        self.fixture.json("prepare/candidate-gate.json", {"mod": str(self.root / "mod"), "report": str(self.report_path)})
        self.fixture.json("prepared/manifest.json", {"scope": "synthetic original prepare"})
        self.result = {"artifact_dir": str(self.root / "prepared"), "run_id": "synthetic-only"}
        self.original_prepare = Mock(return_value=self.result)
        fake = SimpleNamespace(prepare=self.original_prepare, console_visible=Mock(return_value=False),
                               h=SimpleNamespace(write_json=lambda p, d: p.write_text(json.dumps(d), encoding="utf-8")))
        source = Path(__file__).resolve().parents[1] / "tools/runtime_1019.py"
        spec = importlib.util.spec_from_file_location("synthetic_runtime_1019_prepare", source)
        self.runtime = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"runtime_single_homeworld": fake}):
            spec.loader.exec_module(self.runtime)
        fake.ARTIFACTS = self.root / "prepare"

    def save_report(self, report):
        self.fixture.json("prepare/report.json", report)

    def test_inline_zero_csv_59_file_package_reaches_original_prepare(self):
        self.assertEqual(len(fixtures.release.update.base.manifest(self.root / "mod")), 59)
        self.assertIs(self.runtime.prepare_1019("candidate", "synthetic-seed.sav"), self.result)
        self.original_prepare.assert_called_once_with("candidate", "synthetic-seed.sav")
        manifest = json.loads((self.root / "prepared/manifest.json").read_text(encoding="utf-8"))
        self.assertIn("Chinese runtime only", manifest["scope"])

    def test_legacy_csv_syntax_pass_is_rejected_before_original_prepare(self):
        legacy = {key: value for key, value in self.report.items()
                  if not key.startswith("planet_killer_numeric_")
                  and key not in {"weapon_csv_loader_contract", "weapon_csv_unsupported_files"}}
        legacy.update(weapon_csv_files=1, weapon_csv_keys=1, weapon_csv_applicability="checked")
        self.save_report(legacy)
        with self.assertRaisesRegex(RuntimeError, "CSV loader contract"):
            self.runtime.prepare_1019("candidate")
        self.original_prepare.assert_not_called()

    def test_unresolved_numeric_or_callback_contract_cannot_prepare(self):
        for field, value in (("planet_killer_numeric_resolved", 0),
                             ("planet_killer_numeric_contract", "old_csv_syntax_v0"),
                             ("planet_killer_callbacks_resolved", 2)):
            self.save_report({**self.report, field: value})
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                self.runtime.prepare_1019("candidate")
            self.original_prepare.assert_not_called()

    def test_actual_unsupported_csv_or_changed_source_cannot_prepare(self):
        table = self.fixture.write("mod/common/component_templates/unloaded.csv", b"key;end\nEEP_SYNTHETIC_GUARD;\n")
        with self.assertRaisesRegex(RuntimeError, "CSV loader contract"):
            self.runtime.prepare_1019("candidate")
        self.original_prepare.assert_not_called()
        table.unlink()
        self.fixture.write("mod/common/component_templates/synthetic.txt",
                           (self.root / "mod/common/component_templates/synthetic.txt").read_bytes() + b"# stale report\n")
        with self.assertRaisesRegex(RuntimeError, "source bytes differ"):
            self.runtime.prepare_1019("candidate")
        self.original_prepare.assert_not_called()


if __name__ == "__main__":
    unittest.main()
