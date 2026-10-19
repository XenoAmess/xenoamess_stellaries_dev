"""Offline collection guards; derived native blocks never certify real economy."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unittest
from unittest import mock
import zipfile

import audit_save as audit
import runtime_economy_1019 as e


TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
EXE = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
CIVICS = {"machine": "civic_machine_terminator", "hive": "civic_hive_devouring_swarm",
          "purifier": "civic_fanatic_purifiers"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def native_zip(date="2200.01.01", government="machine", dirty=False, budget_delta=0):
    """Keep original Mother layout; changed IDs/government/budget are parser inputs only."""
    fixture = load(Path(__file__).parent / "fixtures/fmm00-growth-native-extract.json")
    blocks = fixture["blocks"]

    def rebound(body):
        return re.sub(r"\b997\b", "1401", re.sub(r"\b159\b", "271", body))

    variables = blocks["country0_variables"]
    if dirty:
        variables = re.sub(r"\beep_c=0\b", "eep_c=1", variables)
    # Synthetic numbers exercise extraction and same-date comparison, not game income.
    period = ("income={country={energy=10}} expenses={country={energy=8}} "
              "balance={country={energy=" + str(2 + budget_delta) + "}}")
    text = ('date="' + date + '" saved_event_target={' + rebound(blocks["saved_event_target"])
            + '} country={0={fleets_manager={' + rebound(blocks["country0_fleets_manager"])
            + '} government={origin="origin_heart_of_devouring" civics={"'
            + CIVICS[government] + '"}} variables={' + variables + '}'
            + ' used_naval_capacity=3 owned_planets={1} budget={current_month={' + period
            + '} last_month={' + period + '}} modules={standard_economy_module={'
            + 'resources={energy=200}}}}} fleet={271={' + rebound(blocks["fleet159"])
            + '}} ships={1401={' + rebound(blocks["ship997"])
            + '}} ship_design={1379={' + blocks["design1379"] + '}}')
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("gamestate", text)
        archive.writestr("meta", 'date="' + date + '"')
    return stream.getvalue()


class FakeBackend:
    """Filesystem orchestration only; does not launch a game or model its economy."""
    def __init__(self, plan, dirty_month=None, mismatched_ui=False):
        self.plan, self.commands, self.month = plan, [], 0
        self.dirty_month, self.mismatched_ui = dirty_month, mismatched_ui
        self.closed, self.final_call, self.monthly_receipts_at_final = False, None, {}

    def initial(self):
        return None

    def command(self, command, stage):
        self.commands.append(command)
        return {"command": command, "stage": stage, "synthetic": True}

    def wait_date(self, date, stage):
        self.month += 1
        source = Path(self.plan["autosave_dir"]) / ("autosave_" + date + ".sav")
        source.write_bytes(native_zip(date, self.plan["government"], self.month == self.dirty_month))
        now = time.time_ns()
        os.utime(source, ns=(now, now))
        return {"date": date, "image": "synthetic-frame", "synthetic": True}

    def final_save(self, stage, date):
        self.final_call = (stage, date)
        artifacts = Path(self.plan["artifacts"])
        self.monthly_receipts_at_final = {path.name: path.read_bytes()
                                        for path in artifacts.glob(self.plan["prefix"] + "m??-receipt.json")}
        target = artifacts / (stage + ".sav")
        raw = native_zip(date, self.plan["government"], budget_delta=int(self.mismatched_ui))
        with target.open("xb") as stream:
            stream.write(raw)
        result = audit.audit(target, (0,))
        target.with_suffix(".audit.json").write_text(json.dumps(result), encoding="utf-8")
        target.with_suffix(".native-save.json").write_text(json.dumps({
            "archived": str(target), "sha256": result["save_sha256"], "date": date,
            "written_at": str(Path(self.plan["autosave_dir"]) / target.name),
            "synthetic": True}), encoding="utf-8")
        return result

    def cleanup(self):
        self.closed = True
        return []


class EconomyCollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="eep-economy-1019-")
        self.root = Path(self.tmp.name)
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.user = self.root / "user"
        self.campaign = self.user / "save games/native-campaign"
        self.history = self.user / "save games/history"
        self.campaign.mkdir(parents=True)
        self.history.mkdir()
        self.prefix = "econ"
        self.anchor = self.artifacts / "econm00.sav"
        self.receipt = self.artifacts / "econm00.native-save.json"
        self.manifest = {"run_id": "synthetic-economy", "userdir": str(self.user),
                         "language": "l_simp_chinese", "game_exe_sha256": EXE,
                         "profile_id": "eep-0.4.0-single-production-mod",
                         "repository_mod_tree_sha256": TREE, "copied_mod_tree_sha256": TREE}
        self.manifest_path = self.artifacts / "manifest.json"
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        # Actual RC4 package gates have separate tests; this suite isolates collection.
        self.gate = mock.patch.object(e, "validate_package", side_effect=lambda path: load(path))
        self.gate.start()
        self.addCleanup(self.gate.stop)
        self.addCleanup(self.tmp.cleanup)
        self.set_anchor()

    def set_anchor(self, government="machine", date="2200.01.01", dirty=False):
        raw = native_zip(date, government, dirty)
        self.anchor.write_bytes(raw)
        history = self.history / self.anchor.name
        history.write_bytes(raw)
        self.receipt.write_text(json.dumps({"archived": str(self.anchor), "history": str(history),
            "written_at": str(self.campaign / self.anchor.name),
            "sha256": hashlib.sha256(raw).hexdigest(), "date": date}), encoding="utf-8")

    def plan(self, government="machine", **kwargs):
        return e.make_plan(self.receipt, self.prefix, government, **kwargs)

    def test_three_governments_discover_native_mother_and_reject_dirty_or_wrong_civic(self):
        for government in CIVICS:
            with self.subTest(government=government):
                self.set_anchor(government)
                plan = self.plan(government)
                self.assertEqual((plan["fleet"], plan["ship"]), (271, 1401))
                self.assertEqual(plan["government"], government)
                wrong = "hive" if government == "machine" else "machine"
                with self.assertRaises(ValueError):
                    self.plan(wrong)
                self.set_anchor(government, dirty=True)
                with self.assertRaises(ValueError):
                    self.plan(government)

    def test_each_core_once_does_not_accept_a_core_in_the_wrong_native_slot(self):
        state = e.growth.read_save(self.anchor)
        e.require_pristine(state, "machine")
        components = [item for stage in state["layout"] for section in stage["sections"]
                      for item in section["components"]]
        shield = next(item for item in components if item.get("template") == "EEP_ADAPTIVE_SHIELD_CORE")
        self.assertEqual(shield["slot"], "AUX_UTILITY_6")
        shield["slot"] = "AUX_UTILITY_1"
        # Counts stay valid, so this specifically exercises actual slot validation.
        self.assertTrue(all(sum(item.get("template") == core for item in components) == 1
                            for core in e.growth.CORE_SLOTS.values()))
        with self.assertRaisesRegex(ValueError, "slots"):
            e.require_pristine(state, "machine")

    def test_default_and_explicit_dry_run_never_import_live_or_write_artifacts(self):
        before = {path.name: path.read_bytes() for path in self.artifacts.iterdir()}
        for mode in ([], ["--dry-run"]):
            with self.subTest(mode=mode), contextlib.redirect_stdout(io.StringIO()) as output:
                e.main(["--anchor-receipt", str(self.receipt), "--prefix", self.prefix,
                        "--government", "machine"] + mode)
                plan = json.loads(output.getvalue())
                self.assertEqual(len(plan["months"]), 12)
                self.assertEqual(plan["months"][0]["date"], "2200.02.01")
                self.assertEqual(plan["months"][-1]["date"], "2201.01.01")
        self.assertNotIn("runtime_1019", sys.modules)
        self.assertEqual(before, {path.name: path.read_bytes() for path in self.artifacts.iterdir()})

    def test_autosave_default_tracks_written_campaign_and_override_stays_inside_userdir(self):
        receipt = load(self.receipt)
        self.assertFalse(Path(receipt["written_at"]).exists())
        self.assertTrue(Path(receipt["history"]).is_file())
        self.assertEqual(self.plan()["autosave_dir"], str(self.campaign.resolve()))
        self.assertEqual(self.plan(autosave_dir=self.history)["autosave_dir"], str(self.history.resolve()))
        outside = self.root / "outside"
        outside.mkdir()
        with self.assertRaises(ValueError):
            self.plan(autosave_dir=outside)

    def test_existing_m00_is_allowed_but_future_stage_or_receipt_cannot_be_overwritten(self):
        self.assertEqual(self.plan()["anchor_date"], "2200.01.01")
        before = self.anchor.read_bytes()
        for suffix in ("m01.sav", "m12.audit.json", "yearui.sav", "-economy-receipt.json",
                       "-auto-ui-comparison-m12.json"):
            path = self.artifacts / (self.prefix + suffix)
            path.write_bytes(b"existing evidence")
            with self.subTest(suffix=suffix), self.assertRaises(FileExistsError):
                self.plan()
            self.assertEqual(path.read_bytes(), b"existing evidence")
            path.unlink()
        self.assertEqual(self.anchor.read_bytes(), before)

    def test_collect_keeps_twelve_single_months_immutable_receipts_and_ui_comparison(self):
        plan = self.plan()
        backend = FakeBackend(plan)
        with contextlib.redirect_stdout(io.StringIO()):
            result = e.collect(plan, lambda _: backend)
        self.assertEqual(backend.commands, ["fast_forward 30"] * 12)
        self.assertEqual(backend.final_call, (self.prefix + "yearui", "2201.01.01"))
        self.assertTrue(backend.closed)
        self.assertEqual(result["status"], "OBSERVATION_ONLY")
        total = load(self.artifacts / (self.prefix + "-economy-receipt.json"))
        self.assertEqual(total["state"], "COLLECTED_NOT_ACCEPTED")
        self.assertEqual(len(backend.monthly_receipts_at_final), 12)
        for index in range(1, 13):
            stage = self.prefix + f"m{index:02}"
            raw = (self.artifacts / (stage + ".sav")).read_bytes()
            monthly = load(self.artifacts / (stage + "-receipt.json"))
            self.assertEqual(monthly["sha256"], hashlib.sha256(raw).hexdigest())
            summary = load(self.artifacts / (stage + ".economy.json"))
            self.assertEqual(summary["energy"]["last_month"]["balance"], 2)
        for name, raw in backend.monthly_receipts_at_final.items():
            self.assertEqual((self.artifacts / name).read_bytes(), raw)
        comparison = load(self.artifacts / (self.prefix + "-auto-ui-comparison-m12.json"))
        self.assertEqual(comparison["status"], "OBSERVATION_ONLY")
        self.assertTrue(comparison["all_fields_equal"])
        with self.assertRaises(FileExistsError):
            e.collect(plan, lambda _: backend)

    def test_dirty_month_preserves_actual_archive_and_stops_before_next_command(self):
        plan = self.plan()
        backend = FakeBackend(plan, dirty_month=3)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            e.collect(plan, lambda _: backend)
        self.assertEqual(backend.commands, ["fast_forward 30"] * 3)
        self.assertTrue(backend.closed)
        self.assertIsNone(backend.final_call)
        for suffix in (".sav", ".audit.json", ".economy.json", "-receipt.json"):
            self.assertTrue((self.artifacts / (self.prefix + "m03" + suffix)).is_file())
        actual = audit.audit(self.artifacts / (self.prefix + "m03.sav"), (0,))
        self.assertEqual(actual["countries"]["0"]["variables"]["eep_c"], 1)
        self.assertFalse((self.artifacts / (self.prefix + "m04.sav")).exists())
        self.assertEqual(load(self.artifacts / (self.prefix + "-economy-receipt.json"))["state"], "ABORTED")

    def test_final_ui_difference_is_saved_as_failure_with_cleanup(self):
        plan = self.plan()
        backend = FakeBackend(plan, mismatched_ui=True)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            e.collect(plan, lambda _: backend)
        comparison = load(self.artifacts / (self.prefix + "-auto-ui-comparison-m12.json"))
        self.assertEqual(comparison["status"], "OBSERVATION_ONLY")
        self.assertFalse(comparison["all_fields_equal"])
        self.assertTrue(backend.closed)
        self.assertEqual(len(backend.commands), 12)
        self.assertTrue((self.artifacts / (self.prefix + "yearui.sav")).is_file())
        self.assertEqual(load(self.artifacts / (self.prefix + "-economy-receipt.json"))["state"], "ABORTED")


if __name__ == "__main__":
    unittest.main()
