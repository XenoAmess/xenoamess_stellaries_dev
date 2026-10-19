"""Static Mod contract only; native single-sync counts remain a separate check."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import audit_save as native

SOURCE = ROOT / "mod/common/scripted_effects/eep_mothership_effects.txt"
KINDS = ("shield", "armor", "hull", "damage", "tracking", "regen")


def one(fields, key, obj):
    matches = [body for name, body, block in fields if name == key and block == obj]
    if len(matches) != 1 or sum(name == key for name, _, _ in fields) != 1:
        raise ValueError("expected one direct " + key)
    return matches[0]


def tokens(raw):
    return [value for value, _, _ in native.tokens(raw)]


def require_component_budget(text):
    effect = list(native.fields(one(list(native.fields(text)), "eep_sync_mothership_components", True)))
    loop = list(native.fields(one(effect, "while", True)))
    if one(loop, "count", False) != "200":
        raise ValueError("native while must declare literal count 200")
    index = next(i for i, field in enumerate(effect) if field[0] == "while")
    if (index == 0 or effect[index - 1][0::2] != ("set_variable", True)
            or native.scalars(effect[index - 1][1]) != {"which": "eep_component_work_budget", "value": 200}):
        raise ValueError("work budget 200 must directly precede while")
    if effect[index + 1] != ("clear_variable", "eep_component_work_budget", False):
        raise ValueError("temporary work budget must be cleared after while")
    expected_limit = ("check_variable={which=eep_component_rewards value < owner.eep_component_entitled} "
                      "check_variable={which=eep_component_work_budget value > 0}")
    if tokens(one(loop, "limit", True)) != tokens(expected_limit):
        raise ValueError("both unpaid-reward and positive-work-budget guards must remain")
    lottery = list(native.fields(one(loop, "random_list", True)))
    if len(lottery) != 6:
        raise ValueError("expected all six equal reward outcomes")
    for (weight, body, obj), kind in zip(lottery, KINDS):
        if weight != "1" or not obj:
            raise ValueError("reward outcomes must keep equal weights")
        change = one(list(native.fields(body)), "change_variable", True)
        if native.scalars(change) != {"which": "eep_component_" + kind + "_level", "value": 1}:
            raise ValueError("each outcome must add exactly one component rank")
    changes = [native.scalars(body) for key, body, obj in loop if key == "change_variable" and obj]
    if changes != [{"which": "eep_component_rewards", "value": 1},
                   {"which": "eep_component_work_budget", "value": -1}]:
        raise ValueError("each iteration must pay one reward and consume one work unit")
    if [key for key, _, _ in loop] != ["count", "limit", "random_list", "change_variable", "change_variable"]:
        raise ValueError("unexpected direct reward-loop effect")


class ComponentBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SOURCE.read_text(encoding="utf-8-sig")

    def reject(self, old, new):
        self.assertIn(old, self.text)
        with self.assertRaises(ValueError):
            require_component_budget(self.text.replace(old, new, 1))

    def test_production_declares_explicit_200_iteration_budget(self):
        require_component_budget(self.text)

    def test_missing_lower_variable_duplicate_and_object_count_are_rejected(self):
        for replacement in ("", "count = 100", "count = eep_component_work_budget",
                            "count = 200 count = 200", "count = { value = 200 }"):
            with self.subTest(replacement=replacement):
                self.reject("count = 200", replacement)

    def test_nested_count_cannot_impersonate_direct_native_count(self):
        self.reject("count = 200", "if = { limit = { always = yes } count = 200 }")

    def test_work_budget_and_cleanup_must_remain(self):
        self.reject("which = eep_component_work_budget value = 200", "which = eep_component_work_budget value = 100")
        self.reject("clear_variable = eep_component_work_budget", "clear_variable = unrelated_budget")

    def test_both_limits_remain_mandatory(self):
        for guard in ("check_variable = { which = eep_component_rewards value < owner.eep_component_entitled }",
                      "check_variable = { which = eep_component_work_budget value > 0 }"):
            with self.subTest(guard=guard):
                self.reject(guard, "")

    def test_reward_and_work_unit_increments_cannot_change(self):
        self.reject("change_variable = { which = eep_component_rewards value = 1 }",
                    "change_variable = { which = eep_component_rewards value = 2 }")
        self.reject("change_variable = { which = eep_component_work_budget value = -1 }",
                    "change_variable = { which = eep_component_work_budget value = -2 }")

    def test_six_reward_outcomes_and_equal_weights_remain(self):
        self.reject("1 = { change_variable = { which = eep_component_tracking_level value = 1 } }", "")
        self.reject("1 = { change_variable = { which = eep_component_regen_level value = 1 } }",
                    "2 = { change_variable = { which = eep_component_regen_level value = 1 } }")


if __name__ == "__main__":
    unittest.main()
