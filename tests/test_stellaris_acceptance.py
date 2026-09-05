import json
import tempfile
import unittest
from pathlib import Path

from tools import stellaris_acceptance as acceptance


class ManifestTests(unittest.TestCase):
    def test_frozen_mod_tree_matches_runtime_contract(self) -> None:
        files, tree_hash = acceptance.tree_manifest(acceptance.MOD_ROOT)

        self.assertEqual(5, len(files))
        self.assertEqual(acceptance.EXPECTED_MOD_TREE_SHA256, tree_hash)
        self.assertEqual(
            sorted(item["path"] for item in files),
            [item["path"] for item in files],
        )

    def test_write_json_is_utf8_and_newline_terminated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "result.json"
            acceptance.write_json(path, {"label": "计划10"})

            self.assertEqual('{\n  "label": "计划10"\n}\n', path.read_text(encoding="utf-8"))


class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_root = acceptance.ROOT / "fixtures" / "iteration-1"
        cls.contract = json.loads((fixture_root / "mod-contract.json").read_text(encoding="utf-8"))
        cls.scenarios = json.loads((fixture_root / "scenarios.json").read_text(encoding="utf-8"))

    def test_contract_covers_all_decisions_once(self) -> None:
        decisions = self.contract["decisions"]

        self.assertEqual(list(range(13)), [entry["index"] for entry in decisions])
        self.assertEqual(13, len({entry["decision"] for entry in decisions}))
        self.assertEqual(13, len({entry["deposit"] for entry in decisions}))
        self.assertEqual(1000, self.contract["common_decision_contract"]["cost"]["minerals"])
        self.assertEqual(180, self.contract["common_decision_contract"]["enactment_days"])

    def test_scenarios_preserve_pass_fail_and_not_executed_states(self) -> None:
        statuses = {entry["id"]: entry["status"] for entry in self.scenarios["scenarios"]}

        self.assertEqual("failed", statuses["S01"])
        self.assertEqual("passed", statuses["S02"])
        self.assertEqual("passed_with_followup", statuses["S03"])
        self.assertEqual("not_executed", statuses["S04"])
        self.assertEqual("not_executed", statuses["S05"])
        self.assertEqual("partially_passed", statuses["S06"])


if __name__ == "__main__":
    unittest.main()
