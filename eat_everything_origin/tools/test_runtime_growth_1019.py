"""Native block parsing and synthetic sequence tests; no desktop or live game."""
import contextlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unittest
import zipfile
import zlib

import runtime_growth_1019 as g


def native_zip(date="2200.01.01", matter=0, tier=0, probes=False, wrong_binding=False,
               rewards=0, level=0):
    cv = ("eep_c=" + str(matter) + " eep_mothership_level=" + str(level)
          + " eep_component_rewards=" + str(rewards))
    fv = "eep_component_rewards=" + str(rewards) + " " + " ".join(k + "=" + str(tier if i == 0 else 0)
                                                for i, k in enumerate(g.TIERS))
    sv = " ".join(k + "=0" for k in g.PROBES) if probes else ""
    components = " ".join('component={template="EEP_ADAPTIVE_' + k.upper() + '_CORE"}'
                          for k in ("shield", "armor", "hull", "damage", "tracking", "regen"))
    text = ('date="%s" saved_event_target={name=eep_mothership0 id=%s}'
            ' country={0={fleets_manager={owned_fleets={{fleet=159}}}'
            ' variables={%s} government={civics={civic_machine_terminator}}}}'
            ' fleet={159={ships={997} variables={%s}}}'
            ' ships={997={fleet=159 hitpoints=93960 max_hitpoints=93960'
            ' armor_hitpoints=44787.6 max_armor_hitpoints=44787.6'
            ' shield_hitpoints=167310 max_shield_hitpoints=167310'
            ' ship_design_implementation={design=1} variables={%s}}}'
            ' ship_design={1={growth_stages={{section={%s}}}}}') % (
                date, 158 if wrong_binding else 159, cv, fv, sv, components)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("gamestate", text)
        archive.writestr("meta", 'date="' + date + '"')
    return stream.getvalue()


class FakeBackend:
    """Writes observations for orchestration only; deliberately does not simulate growth/RNG."""
    def __init__(self, plan, omit_probes=False, dirty_live=False):
        self.plan, self.commands = plan, []
        self.matter, self.probes, self.closed = 0, False, False
        self.omit_probes, self.dirty_live = omit_probes, dirty_live

    def initial(self):
        return None

    def command(self, command, stage):
        self.commands.append(command)
        if "which=eep_c value=" in command:
            self.matter = int(re.search(r"which=eep_c value=(\d+)", command)[1])
        if command == g.export_command():
            self.probes = True
        return {"command": command, "stage": stage, "synthetic": True}

    def wait_date(self, date, stage):
        path = Path(self.plan["autosave_dir"]) / ("autosave_" + date + ".sav")
        path.write_bytes(native_zip(date, self.matter, 1 if self.dirty_live else 0,
                                   self.probes and not self.omit_probes))
        # Model a completed new filesystem write, not engine timing or gameplay.
        now = time.time_ns()
        os.utime(path, ns=(now, now))
        return {"date": date, "image": "synthetic-frame", "synthetic": True}

    def cleanup(self):
        self.closed = True
        return []


class GrowthCollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="eep-growth-1019-")
        self.root = Path(self.tmp.name)
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.user = self.root / "user"
        self.folder = self.user / "save games/history"
        self.folder.mkdir(parents=True)
        self.campaign = self.user / "save games/native-campaign"
        self.campaign.mkdir()
        self.anchor = self.artifacts / "clean.sav"
        self.receipt = self.artifacts / "clean.native-save.json"
        self.set_anchor()
        manifest = {"run_id": "synthetic-growth", "userdir": str(self.user),
                    "language": "l_simp_chinese", "game_exe_sha256": g.EXE,
                    "profile_id": "eep-0.4.0-single-production-mod",
                    "repository_mod_tree_sha256": g.TREE, "copied_mod_tree_sha256": g.TREE}
        (self.artifacts / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def set_anchor(self, date="2200.01.01", matter=0, tier=0, rewards=0, level=0):
        raw = native_zip(date, matter, tier, rewards=rewards, level=level)
        self.anchor.write_bytes(raw)
        history = self.folder / "clean.sav"
        history.write_bytes(raw)
        self.receipt.write_text(json.dumps({"archived": str(self.anchor), "history": str(history),
            "written_at": str(self.campaign / "clean.sav"),
            "sha256": g.digest(raw), "date": date}), encoding="utf-8")

    def plan(self, **kwargs):
        return g.make_plan(self.receipt, "growth", **kwargs)

    def test_real_fmm00_blocks_supply_ownership_health_and_hardware(self):
        fixture = g.read_json(Path(__file__).parent / "fixtures/fmm00-growth-native-extract.json")
        self.assertEqual(fixture["source_save_sha256"],
                         "18cae5e75b189ee8739cdadd3fc63d5c2929fad7a1d892e5382d0750d36c33d9")
        blocks = fixture["blocks"]
        for key, body in blocks.items():
            self.assertEqual(g.digest(body.encode("utf-8")), fixture["block_sha256"][key])
        self.assertNotIn("owner", g.a.scalars(blocks["fleet159"]))

        def packaged(extra_country="", omit_health=False):
            vessel = blocks["ship997"]
            if omit_health:
                vessel = re.sub(r"(?m)^\s*max_shield_hitpoints=.*$", "", vessel)
            text = ('date="2200.01.01" saved_event_target={' + blocks["saved_event_target"]
                    + '} country={0={'
                    + " ".join(key + "={" + blocks["country0_" + key] + "}" for key in
                               ("fleets_manager", "government", "variables"))
                    + '} ' + extra_country + '} fleet={159={' + blocks["fleet159"]
                    + '}} ships={997={' + vessel + '}} ship_design={1379={'
                    + blocks["design1379"] + '}}')
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("gamestate", text)
            return stream.getvalue()

        # The payload is copied from native fmm00, not a layout generated by the collector.
        state = g.native_state(packaged(), 0, 159, 997)
        g.require_clean(state)
        self.assertEqual(state["owner_country_ids"], [0])
        self.assertEqual(state["ownership_source"], "country.fleets_manager.owned_fleets")
        self.assertEqual(state["native_ship"], {
            "hitpoints": 93960, "max_hitpoints": 93960,
            "armor_hitpoints": 44787.6, "max_armor_hitpoints": 44787.6,
            "shield_hitpoints": 167310, "max_shield_hitpoints": 167310})
        self.assertEqual(state["design_id"], 1379)
        self.assertTrue(all(value == 1 for value in state["core_counts"].values()))
        with self.assertRaisesRegex(ValueError, "ownership"):
            g.native_state(packaged('1={fleets_manager={owned_fleets={{fleet=159}}}}'), 0,159,997)
        with self.assertRaisesRegex(ValueError, "health fields"):
            g.native_state(packaged(omit_health=True), 0,159,997)

    def test_plan_is_two_separate_months_per_node_and_crosses_year(self):
        plan = self.plan()
        self.assertEqual(len(plan["phases"]), 18)
        self.assertEqual(plan["phases"][0]["date"], "2200.02.01")
        self.assertEqual(plan["phases"][-1]["date"], "2201.07.01")
        self.assertEqual(plan["autosave_dir"], str(self.campaign))
        self.assertEqual(g.next_month("2200.12.01"), "2201.01.01")
        for i, matter in enumerate(g.NODES):
            refresh, final = plan["phases"][i*2:i*2+2]
            self.assertEqual(refresh["C"], matter)
            self.assertEqual(final["C"], matter)
            self.assertIn("eep_sync_mothership=yes", refresh["before_forward"])
            self.assertTrue(refresh["before_forward"].startswith("effect root={"))
            self.assertEqual(final["before_forward"], g.export_command())
            self.assertTrue(final["before_forward"].startswith("effect event_target:eep_mothership0="))
            self.assertNotIn("@this", final["before_forward"])
            self.assertEqual(refresh["fast_forward"], "fast_forward 30")
            self.assertEqual(final["fast_forward"], "fast_forward 30")
        self.assertNotIn("runtime_1019", sys.modules)
        self.assertEqual(len(list(self.artifacts.glob("growth*"))), 0)

    def test_default_uses_ui_campaign_after_history_move_and_override_supports_reload(self):
        receipt = g.read_json(self.receipt)
        self.assertFalse(Path(receipt["written_at"]).exists())
        self.assertTrue(Path(receipt["history"]).is_file())
        self.assertNotEqual(self.campaign, self.folder)
        self.assertEqual(self.plan()["autosave_dir"], str(self.campaign))
        self.assertEqual(self.plan(autosave_dir=self.folder)["autosave_dir"], str(self.folder))

    def test_clean_year1_economy_anchor_keeps_its_actual_calendar(self):
        self.set_anchor(date="2201.01.01")
        plan = self.plan()
        self.assertEqual(plan["anchor_date"], "2201.01.01")
        self.assertEqual(plan["phases"][0]["date"], "2201.02.01")
        self.assertEqual(plan["phases"][-1]["date"], "2202.07.01")

    def test_plan_rejects_dirty_tier_matter_and_non_month_first(self):
        for args in ({"tier": 1}, {"matter": 50}, {"rewards": 1}, {"level": 1},
                     {"date": "2200.01.07"}):
            with self.subTest(args=args):
                self.set_anchor(**args)
                with self.assertRaises(ValueError):
                    self.plan()

    def test_other_country_is_not_silently_mutated_through_player_root(self):
        with self.assertRaisesRegex(ValueError, "country0"):
            self.plan(country=1)

    def test_dry_run_main_does_not_import_live_runtime_or_create_outputs(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            g.main(["--anchor-receipt", str(self.receipt), "--prefix", "growth", "--dry-run"])
        plan = json.loads(output.getvalue())
        self.assertEqual(plan["mode"], "PLAN_ONLY")
        self.assertEqual(len(plan["phases"]), 18)
        self.assertNotIn("runtime_1019", sys.modules)
        self.assertFalse(list(self.artifacts.glob("growth*")))

    def test_refuses_existing_prefix_and_changed_anchor(self):
        (self.artifacts / "growth-old.jpg").write_bytes(b"prior evidence")
        with self.assertRaises(FileExistsError):
            self.plan()
        self.set_anchor()
        self.anchor.write_bytes(b"changed archive")
        with self.assertRaises(ValueError):
            g.make_plan(self.receipt, "different")

    def test_freshness_date_crc_and_identity_fail_closed(self):
        path = self.folder / "autosave_2200.02.01.sav"
        raw = native_zip("2200.02.01")
        path.write_bytes(raw)
        mtime = path.stat().st_mtime_ns
        with self.assertRaises(ValueError):
            g.fresh_native(path, mtime, 0, "2200.02.01", (0,159,997))
        with self.assertRaises(ValueError):
            g.fresh_native(path, 0, 0, "2200.03.01", (0,159,997))
        with self.assertRaises(ValueError):
            g.fresh_native(path, 0, mtime + 1, "2200.02.01", (0,159,997))
        with self.assertRaises(ValueError):
            g.native_state(native_zip(wrong_binding=True), 0,159,997)
        path.write_bytes(b"not a native zip")
        with self.assertRaises(zipfile.BadZipFile):
            g.fresh_native(path, 0, 0, "2200.02.01", (0,159,997))
        corrupt = bytearray(raw)
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            info = archive.getinfo("gamestate")
            offset = info.header_offset + 30 + len(info.filename.encode()) + len(info.extra)
            corrupt[offset + info.compress_size // 2] ^= 0xff
        with self.assertRaises((zipfile.BadZipFile, zlib.error, ValueError)):
            g.native_state(bytes(corrupt), 0,159,997)

    def test_collect_preserves_eighteen_native_observations_and_never_accepts(self):
        plan = self.plan()
        backends = []
        def factory(value):
            backends.append(FakeBackend(value))
            return backends[-1]
        with contextlib.redirect_stdout(io.StringIO()):
            result = g.collect(plan, factory)
        self.assertEqual(result["status"], "OBSERVATION_ONLY")
        self.assertEqual(result["snapshots"], 18)
        self.assertEqual(result["acceptance"], "NOT_PERFORMED")
        self.assertTrue(backends[0].closed)
        commands = backends[0].commands
        self.assertEqual(commands.count("fast_forward 30"), 18)
        self.assertEqual(commands.count(g.export_command()), 9)
        self.assertEqual(sum("which=eep_c value=" in cmd for cmd in commands), 9)
        self.assertNotIn("fast_forward 60", commands)
        self.assertFalse(any("which=eep_component_" in cmd for cmd in commands))
        self.assertEqual(len(list(self.artifacts.glob("growth*.sav"))), 18)
        receipt = g.read_json(result["receipt"])
        self.assertEqual(receipt["state"], "COLLECTED_NOT_ACCEPTED")
        self.assertEqual(receipt["snapshots"][-1]["date"], "2201.07.01")
        self.assertEqual(receipt["snapshots"][-1]["diagnostics_from_date"], "2201.06.01")
        # The fake deliberately leaves growth L/R wrong; collection must not claim gameplay PASS.
        self.assertNotIn('"PASS"', json.dumps(receipt))
        for row in receipt["snapshots"]:
            self.assertEqual(g.digest(Path(row["archived"]).read_bytes()), row["sha256"])
        with self.assertRaises(FileExistsError):
            g.collect(plan, factory)

    def test_live_dirty_C0_aborts_after_preserving_first_actual_save(self):
        plan = self.plan()
        backend = FakeBackend(plan, dirty_live=True)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(ValueError, "dirty C0"):
            g.collect(plan, lambda _: backend)
        receipt = g.read_json(self.artifacts / "growth-growth-receipt.json")
        self.assertEqual(receipt["state"], "ABORTED")
        self.assertEqual(len(receipt["snapshots"]), 1)
        self.assertTrue(backend.closed)

    def test_missing_exports_stops_and_keeps_observations(self):
        plan = self.plan()
        backend = FakeBackend(plan, omit_probes=True)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, "missing requested"):
            g.collect(plan, lambda _: backend)
        receipt = g.read_json(self.artifacts / "growth-growth-receipt.json")
        self.assertEqual(receipt["state"], "ABORTED")
        self.assertEqual(len(receipt["snapshots"]), 2)
        self.assertTrue(backend.closed)


if __name__ == "__main__":
    unittest.main()
