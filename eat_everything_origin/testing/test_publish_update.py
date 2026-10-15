"""Negative publication guards: no native Steam or external mutations."""
import importlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
release = importlib.import_module("publish_update")


class PublicationGuards(unittest.TestCase):
    def setUp(self):
        self.prior = {"status": "PASS", "item_id": release.ITEM, "version": "0.2.0"}

    def test_upstream_and_other_items_are_rejected(self):
        for item in (release.base.FORBIDDEN_ID, 1, release.ITEM + 1):
            with self.subTest(item=item), self.assertRaises(RuntimeError):
                release.validate_target(item, release.VERSION, self.prior, {})

    def test_successful_or_unknown_upload_cannot_be_retried(self):
        release.validate_target(release.ITEM, release.VERSION, self.prior, {})
        identity = {"version": release.VERSION, "item_id": release.ITEM}
        for state in (dict(identity, submit_result=1), dict(identity, submit_started=True)):
            with self.subTest(state=state), self.assertRaises(RuntimeError):
                release.validate_target(release.ITEM, release.VERSION, self.prior, state)
        release.validate_target(release.ITEM, release.VERSION, self.prior, dict(identity, submit_started=True, submit_result=2))

    def test_prerelease_and_already_published_versions_rejected(self):
        for version in ("0.3.0-rc.1", "0.2.0", "0.3.1"):
            with self.subTest(version=version), self.assertRaises(RuntimeError):
                release.validate_target(release.ITEM, version, self.prior, {})
        with self.assertRaises(RuntimeError):
            release.validate_target(release.ITEM, release.VERSION, dict(self.prior, version=release.VERSION), {})

    def test_production_drift_rejected(self):
        original = release.base.manifest(release.MOD)
        for name in ("events/eep_events.txt", "unexpected-fixture.txt"):
            drift = dict(original)
            drift[name] = "0" * 64
            with self.subTest(name=name), patch.object(release.base, "manifest", return_value=drift), self.assertRaises(RuntimeError):
                release.accepted_files()

    def test_changed_evidence_rejected(self):
        original = release.candidate_bytes
        def changed(path):
            data = original(path)
            return data + b" " if path.name == "final-evidence-index.json" else data
        with patch.object(release, "candidate_bytes", side_effect=changed), self.assertRaises(RuntimeError):
            release.accepted_files()

    def test_inline_images_must_be_immutable_and_four_distinct(self):
        description = (release.ROOT / "workshop/description.bbcode").read_text(encoding="utf-8")
        self.assertEqual(len(release.inline_images(description)), 4)
        for invalid in (description.replace(release.CANDIDATE, "main"), description.replace("[img]", "[image]", 1)):
            with self.assertRaises(RuntimeError):
                release.inline_images(invalid)

    def test_canonical_changelog_and_note(self):
        note = release.change_note()
        self.assertTrue(note.startswith("[v0.3.0]\n"))
        self.assertNotIn("## 0.3.0-rc.1", note)
        for label in ("新增", "变更", "修复", "兼容", "验收", "已知限制"):
            self.assertIn(f"- {label}：", note)
        description, _ = release.description_inputs()
        self.assertLess(len(description.encode("utf-8")), 8000)

    def test_altered_note_cannot_reach_native_upload(self):
        original = Path.read_text
        def altered(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            return text + "different release content" if path.name == "change-note-v0.3.0.txt" else text
        with patch.object(Path, "read_text", altered), self.assertRaisesRegex(RuntimeError, "canonical formal changelog"):
            release.preflight(require_clean=False)


if __name__ == "__main__":
    unittest.main()
