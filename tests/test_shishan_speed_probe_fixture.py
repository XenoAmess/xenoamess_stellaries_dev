"""Static input/observation separation; does not simulate native employment."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "speed_fixture_parser", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py"
)
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)
FIXTURE = ROOT / "shishan_code_origin/testing/mod"
NATIVE = Path("C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T090720Z/logs/script_documentation")


def audit_observation_separation(entries):
    forbidden = {
        "last_month_progress", "set_situation_progress", "add_situation_progress",
        "set_assigned_jobs", "set_workforce", "assign_pop_job", "set_pop_job",
    }
    if any(e.key in forbidden for e in c.walk(entries)):
        raise c.ContractError("fixture writes an output or invents an employment setter")
    for entry in c.walk(entries):
        if entry.key in {"set_variable", "change_variable"}:
            body = c.block(entry.value)
            target = c.one(body, "which")
            source = str(c.one(body, "value"))
            if str(target).startswith("shishan_speed_probe_observed") and "requested" in source:
                raise c.ContractError("observed count copied from requested input")
            if str(target).startswith("shishan_code_") and target != "shishan_code_maintenance_count":
                raise c.ContractError("fixture writes a production output variable")


def audit_snapshot(entries):
    audit_observation_separation(entries)
    snapshot = c.block(c.one(entries, "shishan_speed_probe_snapshot_effect"))
    exports = [c.block(e.value) for e in snapshot if e.key == "export_trigger_value_to_variable"]
    observed = {
        (c.one(e, "variable"), c.one(c.block(c.one(e, "parameters")), "job"))
        for e in exports if c.one(e, "trigger") == "num_assigned_jobs"
    }
    if observed != {
        ("shishan_speed_probe_observed_individual", "shishan_code_maintainer"),
        ("shishan_speed_probe_observed_drone", "shishan_code_maintainer_drone"),
    }:
        raise c.ContractError("both observed employment counts must originate in native exports")


class SpeedProbeFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = c.read_script(FIXTURE / "events/shishan_speed_probe_events.txt")
        cls.effects = c.read_script(FIXTURE / "common/scripted_effects/shishan_speed_probe_effects.txt")
        cls.modifiers = c.read_script(FIXTURE / "common/static_modifiers/shishan_speed_probe_modifiers.txt")
        cls.by_id = {
            int(str(c.one(c.block(e.value), "id")).split(".")[-1]): c.block(e.value)
            for e in cls.events if e.key == "country_event"
        }

    def test_only_triggered_hidden_entries_and_documented_boundary_inputs(self):
        self.assertEqual({1, 2, 3, 4, 50, 51, 52, 99, 100, 199, 200, 299, 300,
                          399, 400, 499, 500, 700, 800, 899, 900, 1200, 9000}, set(self.by_id))
        for event in self.by_id.values():
            self.assertEqual("yes", c.one(event, "is_triggered_only"))
            self.assertEqual("yes", c.one(event, "hide_window"))

    def test_no_output_writes_and_exports_are_native(self):
        audit_observation_separation(self.events)
        audit_snapshot(self.effects)
        verify = c.block(c.one(self.effects, "shishan_speed_probe_verify_effect"))
        ready = c.block(c.one(verify, "if"))
        limit = c.block(c.one(ready, "limit"))
        comparisons = [c.block(e.value) for e in c.walk(limit) if e.key == "check_variable"]
        self.assertTrue(any(c.one(x, "which") == "shishan_speed_probe_observed_individual"
                            and c.one(x, "value") == "this.shishan_speed_probe_requested_j" for x in comparisons))
        self.assertTrue(any(c.one(x, "which") == "shishan_speed_probe_observed_drone"
                            and c.one(x, "value") == "this.shishan_speed_probe_requested_j" for x in comparisons))

    def test_n_changes_only_after_confirmed_zero_employment(self):
        for number, expected in [(1, "0"), (2, "1"), (3, "10"), (4, "5")]:
            outer = c.block(c.one(c.block(c.one(self.by_id[number], "immediate")), "if"))
            keys = [e.key for e in outer]
            self.assertLess(keys.index("shishan_speed_probe_reset_capacity_effect"),
                            keys.index("shishan_speed_probe_verify_effect"))
            confirm = c.block(c.one(outer, "if"))
            self.assertEqual("shishan_speed_probe_j_ready", c.one(c.block(c.one(confirm, "limit")), "has_country_flag"))
            n = [c.block(e.value) for e in confirm if e.key == "set_variable"
                 and c.one(c.block(e.value), "which") == "shishan_code_maintenance_count"]
            self.assertEqual([expected], [c.one(e, "value") for e in n])

    def test_capacity_is_only_job_input_and_real_population(self):
        self.assertEqual({"shishan_speed_probe_individual_capacity", "shishan_speed_probe_drone_capacity"},
                         {e.key for e in self.modifiers})
        self.assertEqual({("job_shishan_code_maintainer_add", "1"), ("job_shishan_code_maintainer_drone_add", "1")},
                         {(e.key, e.value) for top in self.modifiers for e in c.block(top.value)})
        prepare = c.block(c.one(self.effects, "shishan_speed_probe_prepare_colony_effect"))
        pops = [c.block(e.value) for e in c.walk(prepare) if e.key == "create_pop_group"]
        self.assertEqual({"specialist", "complex_drone"}, {c.one(e, "category") for e in pops})
        self.assertEqual({"2000"}, {c.one(e, "size") for e in pops})
        self.assertEqual("check_planet_employment", prepare[-1].key)

    def test_cross_colony_preconditions_and_per_colony_observations(self):
        for number in (50, 51, 52):
            outer = c.block(c.one(c.block(c.one(self.by_id[number], "immediate")), "if"))
            limit = c.block(c.one(outer, "limit"))
            self.assertIn(c.Entry("num_owned_colonies", ">=", "2"), limit)
            self.assertIn(c.Entry("is_capital", "=", "no"), c.block(c.one(c.block(c.one(outer, "random_owned_colony")), "limit")))
        verify = c.block(c.one(self.effects, "shishan_speed_probe_verify_effect"))
        per_colony = [c.block(e.value) for e in c.walk(c.block(c.one(c.block(c.one(verify, "if")), "limit"))) if e.key == "any_owned_colony"]
        self.assertEqual(2, len(per_colony))
        self.assertEqual({"owner.shishan_speed_probe_requested_a", "owner.shishan_speed_probe_requested_b"},
                         {c.one(c.block(c.one(e, "check_variable")), "value") for e in per_colony})

    def test_observe_entry_does_not_reassign_or_create(self):
        outer = c.block(c.one(c.block(c.one(self.by_id[9000], "immediate")), "if"))
        self.assertEqual(["shishan_speed_probe_verify_effect"], [e.key for e in outer if e.key != "limit"])
        verify = c.block(c.one(self.effects, "shishan_speed_probe_verify_effect"))
        self.assertFalse({"check_planet_employment", "create_pop_group", "add_modifier"} & {e.key for e in c.walk(verify)})

    def test_native_api_evidence_and_production_identity(self):
        effects = (NATIVE / "effects.log").read_text(encoding="utf-8-sig")
        triggers = (NATIVE / "triggers.log").read_text(encoding="utf-8-sig")
        for key in ("check_planet_employment", "create_pop_group", "add_modifier", "export_trigger_value_to_variable",
                    "remove_all_buildings", "remove_all_districts", "remove_building", "every_owned_colony"):
            self.assertRegex(effects, re.compile(r"^" + key + r" -", re.M))
        self.assertRegex(triggers, re.compile(r"^num_assigned_jobs -", re.M))
        identity = json.loads((ROOT / "shishan_code_origin/evidence/v0.2.1/acceptance/release-identity.json").read_text(encoding="utf-8"))
        production = ROOT / "shishan_code_origin/mod"
        actual = {p.relative_to(production).as_posix(): {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                  for p in production.rglob("*") if p.is_file()}
        self.assertEqual(identity["content"], actual)

    def test_reject_forged_output_and_employment_setter_negative(self):
        for source in ("last_month_progress=0.75", "set_situation_progress=1", "set_workforce=99",
                       "set_variable={which=shishan_speed_probe_observed_individual value=this.shishan_speed_probe_requested_j}"):
            with self.assertRaises(c.ContractError):
                audit_observation_separation(c.parse(source))

    def test_reject_missing_native_export_negative(self):
        snapshot = c.block(c.one(self.effects, "shishan_speed_probe_snapshot_effect"))
        broken = [c.Entry(e.key, e.op, [x for x in snapshot if x.key != "export_trigger_value_to_variable"])
                  if e.key == "shishan_speed_probe_snapshot_effect" else e for e in self.effects]
        with self.assertRaises(c.ContractError):
            audit_snapshot(broken)


if __name__ == "__main__":
    unittest.main()
