"""Player-facing reward tooltips must not expose internal executable effects."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "reward_option_visibility_checks", ROOT / "shishan_code_origin/tools/validate_feedback_redesign.py"
)
checks = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checks
SPEC.loader.exec_module(checks)
GENERATOR_SPEC = importlib.util.spec_from_file_location("reward_visibility_generator", ROOT / "tools/shishan_code/generate_rewards.py")
generator = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(generator)

EVENTS = ROOT / "shishan_code_origin/mod/events/shishan_code_rewards_events.txt"
VISIBLE_FIELDS = {"name", "trigger", "allow", "custom_tooltip", "ai_chance", "hidden_effect"}
METADATA = VISIBLE_FIELDS - {"custom_tooltip", "hidden_effect"}


def assert_public_surface(test: unittest.TestCase, option: list) -> None:
    """Public fields describe the choice; execution has a separate hidden area."""
    test.assertLessEqual({entry.key for entry in option}, VISIBLE_FIELDS)
    name = checks.one(option, "name")
    if re.fullmatch(r"shishan_code_reward_option_\d+", name):
        test.assertEqual(name + "_tooltip", checks.one(option, "custom_tooltip"))
    hidden = checks.block(checks.one(option, "hidden_effect"))
    test.assertTrue(hidden, "execution cannot silently disappear")
    test.assertFalse(any(entry.key == "custom_tooltip" for entry in checks.walk(hidden)), "player explanation cannot be hidden")


class RewardOptionVisibilityTests(unittest.TestCase):
    def setUp(self):
        events = [entry for entry in checks.read_script(EVENTS) if entry.key == "country_event"]
        self.event = checks.find_country_event(events, "shishan_code.1000")
        self.options = [checks.block(entry.value) for entry in self.event if entry.key == "option"]
        self.by_name = {checks.one(option, "name"): option for option in self.options}

    def test_all_39_claims_keep_public_explanation_and_hidden_execution(self):
        expected = {f"shishan_code_reward_option_{index:02d}" for index in range(1, 40)}
        actual = {name for name in self.by_name if re.fullmatch(r"shishan_code_reward_option_\d+", name)}
        self.assertEqual(expected, actual)
        for name in sorted(expected):
            with self.subTest(option=name):
                option = self.by_name[name]
                assert_public_surface(self, option)
                self.assertTrue(checks.block(checks.one(option, "trigger")), "eligibility remains public")
                self.assertEqual("1", checks.one(checks.block(checks.one(option, "ai_chance")), "factor"))

    def test_reroll_failure_reason_stays_public(self):
        option = self.by_name["shishan_code_reward_reroll"]
        assert_public_surface(self, option)
        allow = checks.block(checks.one(option, "allow"))
        tooltip = checks.block(checks.one(allow, "custom_tooltip"))
        self.assertEqual("shishan_code_reward_reroll_unavailable", checks.one(tooltip, "fail_text"))
        self.assertEqual("yes", checks.one(tooltip, "shishan_code_reward_can_reroll"))

    def test_later_remains_an_executable_hidden_option(self):
        assert_public_surface(self, self.by_name["shishan_code_reward_later"])

    def test_visible_state_mutation_is_rejected(self):
        # Independent failure fixture models the original UI leak, not a copy
        # of the generator's rendering code or reward implementation.
        faulty = checks.block(checks.one(checks.parse("option={name=shishan_code_reward_option_01 custom_tooltip=shishan_code_reward_option_01_tooltip set_variable={which=private_counter value=0} hidden_effect={always=yes}}"), "option"))
        with self.assertRaises(AssertionError):
            assert_public_surface(self, faulty)

    def test_hidden_or_missing_player_explanation_is_rejected(self):
        for description in ("", "custom_tooltip=shishan_code_reward_option_01_tooltip"):
            faulty = checks.block(checks.one(checks.parse("option={name=shishan_code_reward_option_01 hidden_effect={" + description + " private_action=yes}}"), "option"))
            with self.subTest(description=description), self.assertRaises((AssertionError, checks.ContractError)):
                assert_public_surface(self, faulty)

    def test_hidden_claim_wrappers_still_invoke_each_action_once(self):
        for index in range(1, 40):
            calls = []
            action = f"shishan_code_reward_claim_{index:02d}_effect"
            interpreter = checks.Effects([], effect_hooks={action: lambda interpreter, country, parameters: calls.append("claimed")})
            option = self.by_name[f"shishan_code_reward_option_{index:02d}"]
            interpreter.execute([entry for entry in option if entry.key not in METADATA], checks.Scope())
            self.assertEqual(["claimed"], calls)

    def test_hidden_reroll_still_dispatches_and_later_only_unlocks(self):
        calls = []
        interpreter = checks.Effects([], effect_hooks={"shishan_code_reward_reroll_effect": lambda interpreter, country, parameters: calls.append("rerolled")})
        option = self.by_name["shishan_code_reward_reroll"]
        interpreter.execute([entry for entry in option if entry.key not in METADATA], checks.Scope())
        self.assertEqual(["rerolled"], calls)
        country = checks.Scope(flags={"shishan_code_reward_pending", "shishan_code_reward_window_open"}, variables={"shishan_code_reroll_cooldown": checks.Decimal(2), "shishan_code_reward_slot_1": checks.Decimal(5)})
        option = self.by_name["shishan_code_reward_later"]
        before = dict(country.variables)
        interpreter.execute([entry for entry in option if entry.key not in METADATA], country)
        self.assertEqual({"shishan_code_reward_pending"}, country.flags)
        self.assertEqual(before, country.variables)

    def test_generated_events_are_reproducible(self):
        self.assertEqual(generator.generate_scripts()[2], EVENTS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
