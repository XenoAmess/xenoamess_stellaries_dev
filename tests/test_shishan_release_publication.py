"""Release-gate negative cases use temporary packages and never load Steamworks."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "shishan_code_origin/tools/update_workshop_current.py"
SPEC = importlib.util.spec_from_file_location("shishan_release_current", SOURCE)
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.root = root
        self.mod = root / "mod"
        self.workshop = root / "workshop"
        self.evidence = root / "evidence/v0.2.1"
        self.mod.mkdir()
        self.workshop.mkdir()
        (self.evidence / "acceptance").mkdir(parents=True)
        for key, value in {"ROOT": root, "REPO": root, "MOD": self.mod, "WORKSHOP": self.workshop}.items():
            p = patch.object(release, key, value)
            p.start()
            self.addCleanup(p.stop)
        (root / "VERSION").write_text("0.2.1\n")
        (root / "CHANGELOG.md").write_text("## [0.2.1] - 2026-10-15\n" + "\n".join(
            f"### {x}\nDocumented" for x in ["Added", "Changed", "Fixed", "Compatibility", "Validation", "Known limitations"]))
        (self.mod / "descriptor.mod").write_text('version="0.2.1"\nsupported_version="4.5.*"\n')
        for i in range(89):
            (self.mod / f"fixture-content-{i}.txt").write_text("production sample")
        (self.workshop / "item-id.txt").write_text(str(release.ITEM_ID))
        (self.workshop / "description.bbcode").write_text("Mod v0.2.1 [img]https://example.invalid/a.png[/img]")
        (self.workshop / "change-note-v0.2.1.txt").write_text("[v0.2.1] Documented changes")
        self.write_json(self.evidence / "before.json", {"planned_version": "0.2.1", "item_id": release.ITEM_ID,
                        "details": {"description": "Mod v0.1.3 [img]https://example.invalid/a.png[/img]"}})
        self.write_json(self.evidence / "acceptance/package-open-kaishek.json",
                        {"status": "PASS", "game_exe_sha256": release.EXE_SHA, "errors": []})
        self.write_identity()

    def write_json(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def write_identity(self):
        self.write_json(self.evidence / "acceptance/release-identity.json",
                        {"status": "PASS", "version": "0.2.1", "content": release.files(self.mod)})

    def preflight(self):
        with patch.object(release.subprocess, "check_output", return_value="a" * 40):
            return release.preflight(require_committed=False)

    def test_stable_accepted_package_passes_without_steam(self):
        result = self.preflight()
        self.assertEqual(len(result["content"]), 90)
        self.assertEqual(result["item_id"], 3810136486)

    def test_prerelease_cannot_be_published(self):
        (self.root / "VERSION").write_text("0.2.1-rc.1")
        with self.assertRaisesRegex(RuntimeError, "stable SemVer"):
            self.preflight()

    def test_readonly_upstream_cannot_be_update_target(self):
        (self.workshop / "item-id.txt").write_text(str(release.UPSTREAM_ID))
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            self.preflight()

    def test_descriptor_cannot_override_workshop_identity(self):
        with (self.mod / "descriptor.mod").open("a") as f:
            f.write('remote_file_id="3710613857"')
        with self.assertRaisesRegex(RuntimeError, "Descriptor"):
            self.preflight()

    def test_changelog_requires_limitations(self):
        p = self.root / "CHANGELOG.md"
        p.write_text(p.read_text().replace("### Known limitations", "### Omitted"))
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            self.preflight()

    def test_change_note_requires_same_version(self):
        (self.workshop / "change-note-v0.2.1.txt").write_text("[v0.1.3] old note")
        with self.assertRaisesRegex(RuntimeError, "Change Note"):
            self.preflight()

    def test_existing_inline_images_must_be_preserved(self):
        (self.workshop / "description.bbcode").write_text("Mod v0.2.1 [img]https://example.invalid/b.png[/img]")
        with self.assertRaisesRegex(RuntimeError, "inline image"):
            self.preflight()

    def test_test_save_is_rejected_even_at_expected_file_count(self):
        (self.mod / "fixture-content-0.txt").rename(self.mod / "test.sav")
        self.write_identity()
        with self.assertRaisesRegex(RuntimeError, "test contamination"):
            self.preflight()

    def test_changes_after_acceptance_are_rejected(self):
        (self.mod / "fixture-content-0.txt").write_text("changed after acceptance")
        with self.assertRaisesRegex(RuntimeError, "accepted release identity"):
            self.preflight()

    def test_failed_package_gate_cannot_be_bypassed(self):
        self.write_json(self.evidence / "acceptance/package-open-kaishek.json",
                        {"status": "FAIL", "game_exe_sha256": release.EXE_SHA, "errors": ["unknown scope"]})
        with self.assertRaisesRegex(RuntimeError, "acceptance is not PASS"):
            self.preflight()

    def test_uncommitted_release_inputs_are_rejected(self):
        with patch.object(release.subprocess, "check_output", side_effect=["a" * 40, b" M mod/descriptor.mod"]):
            with self.assertRaisesRegex(RuntimeError, "committed"):
                release.preflight()

    def test_unpushed_release_commit_is_rejected(self):
        with patch.object(release.subprocess, "check_output", side_effect=["a" * 40, b"", "b" * 40]):
            with self.assertRaisesRegex(RuntimeError, "pushed"):
                release.preflight()

    def test_existing_receipt_refuses_duplicate_submission_before_network(self):
        self.write_json(self.evidence / "publish-state.json", {"submit_result": 1})
        with patch.object(release, "details", side_effect=AssertionError("No network expected")):
            with self.assertRaisesRegex(RuntimeError, "receipt already exists"):
                release.publish()


if __name__ == "__main__":
    unittest.main()
