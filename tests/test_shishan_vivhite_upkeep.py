"""Native upkeep-rule regressions; no economic multiplier is free-fee proof."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vivhite_upkeep_checks", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py")
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)
MOD = ROOT / "shishan_code_origin/mod"
GAME = Path("C:/Program Files (x86)/Steam/steamapps/common/Stellaris")
FROZEN = Path("C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T084453Z/mod/shishan-feedback-local")


def update_refresh(definitions, mode):
    def transform(entries):
        result = []
        for e in entries:
            if mode == "remove_grant" and e.key == "set_leader_flag" and e.value == "should_not_have_upkeep":
                continue
            if mode == "broaden_filter" and e.key == "every_owned_leader":
                body = [c.Entry(child.key, child.op, []) if child.key == "limit" else child for child in e.value]
            else:
                body = transform(e.value) if isinstance(e.value, list) else e.value
            result.append(c.Entry(e.key, e.op, body))
        return result
    return [c.Entry(e.key, e.op, transform(e.value)) if e.key == "shishan_code_refresh_vivhite_effect" else e for e in definitions]


class VivhiteUpkeepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definitions = c.load_definitions(MOD, "scripted_effects")
        cls.values = c.load_definitions(MOD, "script_values")
        cls.events = c.country_events(MOD)

    def test_actual_native_rule_exempts_only_flagged_vivhite(self):
        if not GAME.is_dir():
            self.skipTest("installed canonical native rule required")
        result = c.check_vivhite_upkeep(MOD, GAME)
        self.assertEqual("PASS", result["installed_native_rule_model"]["status"])
        self.assertTrue(result["installed_native_rule_model"]["ordinary_leader_pays"])
        self.assertTrue(result["installed_native_rule_model"]["Vivhite_without_native_flag_pays"])
        self.assertFalse(result["installed_native_rule_model"]["Vivhite_with_native_flag_pays"])

    def test_actual_monthly_event_repairs_old_save_without_changing_growth(self):
        engine, actor, white, ordinary, foreign, backup = c.vivhite_upkeep_fixture(self.definitions, self.values)
        before = (dict(white.variables), set(white.traits), white.portrait)
        self.assertTrue(c.run_country_event(engine, self.events, "shishan_code.60", actor))
        self.assertIn("should_not_have_upkeep", white.flags)
        self.assertEqual(before, (white.variables, white.traits, white.portrait))
        self.assertTrue(all("should_not_have_upkeep" not in leader.flags for leader in (ordinary, foreign, backup)))

    def test_missing_native_grant_really_leaves_paid_leader_and_fails(self):
        faulty = update_refresh(self.definitions, "remove_grant")
        engine, actor, white, *_ = c.vivhite_upkeep_fixture(faulty, self.values)
        engine.named("shishan_code_refresh_vivhite_effect", actor)
        self.assertNotIn("should_not_have_upkeep", white.flags)
        with self.assertRaises(c.ContractError):
            c.check_vivhite_upkeep(MOD, definitions=faulty)

    def test_missing_vivhite_filter_really_exempts_unrelated_leader_and_fails(self):
        faulty = update_refresh(self.definitions, "broaden_filter")
        engine, actor, white, ordinary, *_ = c.vivhite_upkeep_fixture(faulty, self.values)
        engine.named("shishan_code_refresh_vivhite_effect", actor)
        self.assertIn("should_not_have_upkeep", ordinary.flags)
        with self.assertRaisesRegex(c.ContractError, "limited to Vivhite"):
            c.check_vivhite_upkeep(MOD, definitions=faulty)

    def test_backup_must_explicitly_remove_inherited_exemption(self):
        def remove(entries):
            return [c.Entry(e.key, e.op, remove(e.value) if isinstance(e.value, list) else e.value)
                    for e in entries if not (e.key == "remove_leader_flag" and e.value == "should_not_have_upkeep")]
        events = [c.Entry(e.key, e.op, remove(e.value)) if c.one(c.block(e.value), "id") == "shishan_code.40" else e for e in self.events]
        with self.assertRaisesRegex(c.ContractError, "backup must remove inherited upkeep exemption"):
            c.check_vivhite_upkeep_lifecycle(MOD, events)

    def test_reboot_cannot_depend_on_inherited_flag_instead_of_refresh(self):
        def remove(entries):
            return [c.Entry(e.key, e.op, remove(e.value) if isinstance(e.value, list) else e.value)
                    for e in entries if e.key != "shishan_code_refresh_vivhite_effect"]
        events = [c.Entry(e.key, e.op, remove(e.value)) if c.one(c.block(e.value), "id") == "shishan_code.41" else e for e in self.events]
        with self.assertRaisesRegex(c.ContractError, "reboot must refresh native upkeep exemption"):
            c.check_vivhite_upkeep_lifecycle(MOD, events)

    def test_native_rule_scope_fields_fail_closed(self):
        engine = c.Effects([])
        with self.assertRaisesRegex(c.ContractError, "is_gestalt requires country scope"):
            engine.trigger(c.parse("is_gestalt=yes"), c.Scope(kind="leader"))
        with self.assertRaisesRegex(c.ContractError, "is_councilor requires leader scope"):
            engine.trigger(c.parse("is_councilor=yes"), c.Scope())
        self.assertFalse(engine.trigger(c.parse("exists=owner"), c.Scope(kind="leader")))
        self.assertTrue(engine.trigger(c.parse("exists=owner"), c.Scope(kind="leader", owner=c.Scope())))

    def test_frozen_actual_rc5_minus_one_modifier_does_not_grant_native_exemption(self):
        if not FROZEN.is_dir() or not GAME.is_dir():
            self.skipTest("actual frozen rc5 and installed native rule required")
        defs, vals = c.load_definitions(FROZEN, "scripted_effects"), c.load_definitions(FROZEN, "script_values")
        engine, actor, white, *_ = c.vivhite_upkeep_fixture(defs, vals)
        engine.named("shishan_code_refresh_vivhite_effect", actor)
        rule = c.block(c.one(c.parse((GAME / "common/game_rules/00_rules.txt").read_text(encoding="utf-8-sig")), "should_pay_for_leader_upkeep"))
        self.assertNotIn("should_not_have_upkeep", white.flags)
        self.assertTrue(engine.trigger(rule, white))
        with self.assertRaises(c.ContractError):
            c.check_vivhite_upkeep(FROZEN, GAME)


if __name__ == "__main__":
    unittest.main()
