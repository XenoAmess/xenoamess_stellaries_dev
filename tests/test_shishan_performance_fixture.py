"""Reversible calculation gate tests; no performance or native-time simulation."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


b = module("performance_fixture_builder", ROOT / "shishan_code_origin/testing/tools/build_performance_fixture.py")
c = module("performance_fixture_ast", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py")
SOURCE = ROOT / "shishan_code_origin/mod"
EVENT_BYTES = (ROOT / "shishan_code_origin/testing/performance/mod" / b.EVENT).read_bytes()


class TraceEffects(c.Effects):
    """Explicit active-project facts only; all gate/refresh AST executes normally."""
    visits = 0
    modifier_writes = 0

    def trigger(self, entries, current, previous=None):
        normalized = [c.Entry("always", "=", "yes" if e.value in current.projects else "no")
                      if e.key == "is_researching_special_project" else e for e in entries]
        return super().trigger(normalized, current, previous)

    def execute(self, entries, current, previous=None):
        self.visits += sum(e.key == "every_owned_pop_group" for e in entries)
        self.modifier_writes += sum(e.key in {"add_modifier", "remove_modifier"} for e in entries)
        return super().execute(entries, current, previous)


def actor():
    result = c.Scope()
    result.groups = [c.Scope(kind="pop_group", owner=result, population=100, traits={"a", "b"}),
                     c.Scope(kind="pop_group", owner=result, population=100, traits={"a", "b", "c", "d"})]
    return result


class PerformanceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.production = c.load_definitions(SOURCE, "scripted_effects")
        cls.values = c.load_definitions(SOURCE, "script_values")
        cls.original = (SOURCE / b.OVERRIDE).read_bytes()
        cls.wrapped = b.wrap_refresh(cls.original)
        changed = c.block(c.one(c.parse(cls.wrapped.decode("utf-8")), b.EFFECT.decode()))
        cls.definitions = [c.Entry(e.key, e.op, changed) if e.key == b.EFFECT.decode() else e for e in cls.production]
        cls.events = {str(c.one(c.block(e.value), "id")): c.block(e.value)
                      for e in c.parse(EVENT_BYTES.decode()) if e.key == "country_event"}
        b.ALLOWED_OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="performance-static-tests-", dir=b.ALLOWED_OUTPUT_ROOT)
        cls.temp_root = Path(cls.temp.name).resolve()
        assert cls.temp_root.is_relative_to(b.ALLOWED_OUTPUT_ROOT.resolve())
        cls.package = cls.temp_root / "mod"
        shutil.copytree(SOURCE, cls.package)
        (cls.package / b.OVERRIDE).write_bytes(cls.wrapped)
        (cls.package / b.EVENT).write_bytes(EVENT_BYTES)

    @classmethod
    def tearDownClass(cls):
        assert cls.temp_root.is_relative_to(b.ALLOWED_OUTPUT_ROOT.resolve())
        cls.temp.cleanup()

    def ready(self):
        country = actor()
        engine = TraceEffects(self.definitions, self.values)
        engine.named(b.EFFECT.decode(), country)
        engine.visits = engine.modifier_writes = 0
        return engine, country

    def call(self, engine, country, number):
        engine.execute(c.block(c.one(self.events[f"shishan_perf_probe.{number}"], "immediate")), country)

    def test_on_executes_actual_production_ast_with_identical_values(self):
        control, subject = actor(), actor()
        c.Effects(self.production, self.values).named(b.EFFECT.decode(), control)
        engine = TraceEffects(self.definitions, self.values)
        engine.named(b.EFFECT.decode(), subject)
        self.assertEqual(control.variables, subject.variables)
        self.assertEqual(control.modifiers, subject.modifiers)
        self.assertEqual(control.flags, subject.flags)
        self.assertEqual(c.Decimal("3"), subject.modifiers["shishan_code_architecture_jobs"])
        self.assertEqual(1, engine.visits)

    def test_off_skips_real_body_and_preserves_existing_b_and_cache(self):
        engine, country = self.ready()
        self.call(engine, country, 1)
        variables, modifiers = copy.deepcopy(country.variables), country.modifiers.copy()
        country.groups[0].population = 50
        country.groups[1].population = 200
        self.call(engine, country, 3)
        self.assertIn(b.OFF_FLAG, country.flags)
        self.assertEqual(variables, country.variables)
        self.assertEqual(modifiers, country.modifiers)
        self.assertEqual((0, 0), (engine.visits, engine.modifier_writes))

    def test_reenable_then_next_actual_call_recomputes(self):
        engine, country = self.ready()
        self.call(engine, country, 1)
        country.groups[0].population = 50
        country.groups[1].population = 200
        self.call(engine, country, 2)
        self.assertNotIn(b.OFF_FLAG, country.flags)
        self.assertEqual(c.Decimal(3), country.modifiers["shishan_code_architecture_jobs"])
        self.call(engine, country, 3)
        self.assertEqual(c.Decimal("3.6"), country.modifiers["shishan_code_architecture_jobs"])
        self.assertEqual(1, engine.visits)

    def test_nonorigin_with_off_flag_still_cleans_stale_bonus(self):
        engine, country = self.ready()
        country.flags.add(b.OFF_FLAG)
        country.origin = "origin_default"
        engine.named(b.EFFECT.decode(), country)
        self.assertNotIn("shishan_code_architecture_jobs", country.modifiers)
        self.assertEqual(0, engine.visits)

    def test_control_events_are_personal_origin_guarded_and_do_not_touch_foreign(self):
        engine, country = self.ready()
        foreign = c.Scope(origin="origin_default", variables={"sentinel": 42}, modifiers={"foreign": 7})
        before = (foreign.flags.copy(), foreign.variables.copy(), foreign.modifiers.copy())
        self.call(engine, country, 1)
        self.assertEqual(before, (foreign.flags, foreign.variables, foreign.modifiers))
        self.call(engine, foreign, 1)
        self.assertEqual(before, (foreign.flags, foreign.variables, foreign.modifiers))
        for event in self.events.values():
            self.assertEqual("yes", c.one(event, "is_triggered_only"))
            self.assertEqual("yes", c.one(event, "hide_window"))
        writes = [e for e in c.walk(c.parse(EVENT_BYTES.decode())) if e.key in {"set_country_flag", "remove_country_flag"}]
        self.assertEqual({b.OFF_FLAG}, {e.value for e in writes})

    def test_missing_baseline_pending_and_active_projects_reject_off(self):
        for missing in ("modifier", "cache", "migration", "pending", "project"):
            engine, country = self.ready()
            if missing == "modifier": country.modifiers.clear()
            elif missing == "cache": country.variables.pop("shishan_code_architecture_bonus")
            elif missing == "migration": country.flags.remove("shishan_code_architecture_migrated")
            elif missing == "pending": country.flags.add("shishan_code_reward_pending")
            else: country.projects.add("SHISHAN_CODE_MAINTAIN")
            self.call(engine, country, 1)
            self.assertNotIn(b.OFF_FLAG, country.flags)

    def test_package_projection_and_mechanical_roundtrip(self):
        result = b.validate_fixture(SOURCE, self.package, EVENT_BYTES)
        self.assertEqual((91, 89), (result["file_count"], result["unchanged_production_files"]))
        self.assertEqual(self.original, b.unwrap_refresh(self.wrapped))

    def test_reject_source_pollution_duplicate_effect_and_bad_wrapper(self):
        identity = json.loads((ROOT / "shishan_code_origin/evidence/v0.2.1/acceptance/release-identity.json").read_text(encoding="utf-8"))
        identity["content"]["descriptor.mod"]["sha256"] = "0" * 64
        with self.assertRaises(b.FixtureError): b.validate_source(SOURCE, identity, "0.2.1")
        with self.assertRaises(b.FixtureError): b.wrap_refresh(self.original + b"\n" + b.EFFECT + b"={}\n")
        with self.assertRaises(b.FixtureError): b.unwrap_refresh(self.wrapped.replace(b"NOT = { has_origin", b"AND = { has_origin", 1))

    def test_reject_changed_other_production_file_and_changed_original_body(self):
        for name, payload in [("descriptor.mod", b"# unauthorized\n"), (b.OVERRIDE, self.wrapped.replace(b"floor_variable", b"ceil_variable", 1))]:
            path = self.package / name
            original = path.read_bytes()
            try:
                path.write_bytes(payload)
                with self.assertRaises(b.FixtureError): b.validate_fixture(SOURCE, self.package, EVENT_BYTES)
            finally: path.write_bytes(original)

    def test_reject_existing_or_nested_output_and_controller_timing_mutation(self):
        with self.assertRaises(b.FixtureError): b.validate_output_path(self.temp_root, SOURCE)
        with self.assertRaises(b.FixtureError): b.validate_output_path(self.package / "nested", SOURCE)
        with self.assertRaises(b.FixtureError): b.validate_output_path(ROOT / "shishan_code_origin/testing/unsafe", SOURCE)
        with self.assertRaises(b.FixtureError): b.validate_event_asset(EVENT_BYTES + b"set_variable={which=expected_timing value=1}\n")


if __name__ == "__main__":
    unittest.main()
