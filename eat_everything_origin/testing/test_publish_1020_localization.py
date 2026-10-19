"""Offline source-integrity negative controls; these are never native UI evidence."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import publish_1020_localization as release


class NotificationPatchGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eep-notification-guards-")
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)
        project = Path(__file__).resolve().parents[1]
        shutil.copytree(project / "mod", self.root / "mod")
        self.runtime = json.loads((project / "docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json").read_text(encoding="utf-8"))
        name = "docs/evidence/1020-notification-localization-patch-v1/source-certificate-v1.json"
        certificate = json.loads((project / name).read_text(encoding="utf-8"))
        entries = [certificate["before_descriptor"], certificate["after_descriptor"]]
        for row in certificate["changes"]:
            entries.extend([row["before"], row["after"]])
        for path in {name, *(entry["path"] for entry in entries)}:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((project / path).read_bytes())
        self.runtime["notification_localization_patch"] = {
            "source_certificate": {"path": name, "sha256": release.CERTIFICATE_SHA}}

    def rejected(self):
        with self.assertRaises(RuntimeError):
            release.source_contract(self.runtime, self.root)

    def test_exact_ten_language_append_is_accepted(self):
        certificate, child, formal = release.source_contract(self.runtime, self.root)
        self.assertEqual(59, len(child))
        self.assertEqual(10, len(certificate["changes"]))
        self.assertEqual(set(child), set(formal))

    def test_script_change_is_rejected(self):
        path = self.root / "mod/common/component_templates/eep_planet_killer.txt"
        path.write_bytes(path.read_bytes() + b"\n# unreviewed script change\n")
        self.rejected()

    def test_existing_translation_change_is_rejected(self):
        path = self.root / "mod/localisation/english/eep_l_english.yml"
        path.write_bytes(path.read_bytes().replace(b"Heart", b"Unreviewed", 1))
        self.rejected()

    def test_extra_localization_key_is_rejected(self):
        path = self.root / "mod/localisation/english/eep_l_english.yml"
        path.write_bytes(path.read_bytes() + b' extra_unreviewed:0 "extra"\n')
        self.rejected()

    def test_missing_one_language_repair_is_rejected(self):
        name = "localisation/english/eep_l_english.yml"
        old = self.root / "docs/evidence/1020-notification-localization-patch-v1/before" / name
        (self.root / "mod" / name).write_bytes(old.read_bytes())
        self.rejected()

    def test_new_production_file_is_rejected(self):
        (self.root / "mod/unreviewed.txt").write_bytes(b"extra=yes\n")
        self.rejected()

    def test_changed_certificate_cannot_repin_itself(self):
        entry = self.runtime["notification_localization_patch"]["source_certificate"]
        path = self.root / entry["path"]
        path.write_bytes(path.read_bytes() + b"\n")
        entry["sha256"] = release.digest(path.read_bytes())
        self.rejected()

    def test_unknown_parent_tree_is_rejected(self):
        self.runtime["production_tree_sha256"] = "0" * 64
        self.rejected()

    def test_unknown_child_version_is_rejected(self):
        path = self.root / "mod/descriptor.mod"
        path.write_bytes(path.read_bytes().replace(b'0.4.0-rc.8', b'0.4.0-rc.9').replace(
            b'version="0.4.0"', b'version="0.4.0-rc.9"'))
        self.rejected()

    def test_source_certificate_alone_is_not_runtime_acceptance(self):
        certificate, child, formal = release.source_contract(self.runtime, self.root)
        with self.assertRaises(RuntimeError):
            release.runtime_contract(self.runtime, self.root, certificate, child)


if __name__ == "__main__":
    unittest.main()
