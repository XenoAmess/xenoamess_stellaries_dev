"""Finite v2 fixture shape guards; never emulate native stability clamping."""
import copy
import importlib.util
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("stability_fixture_native_reader", ROOT / "shishan_code_origin/tools/audit_feedback_runtime_save.py")
reader = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reader
SPEC.loader.exec_module(reader)
FIXTURE = ROOT / "shishan_code_origin/testing/mod"
EVENT = FIXTURE / "events/shishan_econ_stability_probe_events.txt"
MODIFIER = FIXTURE / "common/static_modifiers/shishan_econ_stability_probe_modifiers.txt"
KEY = "shishan_econ_probe_stability_control"
FLAGS = {"shishan_code_reward_pending", "shishan_code_reward_ticket_ready", "shishan_code_reward_window_open",
         "shishan_code_maintain_success_pending", "shishan_code_clean_success_pending",
         "shishan_code_optimize_success_pending", "shishan_code_relapse_pending"}
PROJECTS = {"SHISHAN_CODE_MAINTAIN", "SHISHAN_CODE_CLEAN", "SHISHAN_CODE_OPTIMIZE"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard(doc, block, replay):
    require(doc.scalar(block, "has_origin") == "origin_shishan_code", "origin guard")
    require(doc.scalar(block, "is_country_type") == "default", "default/alive country guard")
    require(doc.values(block, "exists") == ["owner_main_species", "capital_scope"], "scope-existence guard")
    require(doc.scalar(doc.section(block, "capital_scope"), "is_owned_by") == "prev", "capital owner guard")
    actual = doc.native(doc.section(block, "any_owned_pop_group"))
    example = reader.Document("x={is_same_species=prev pop_group_size > 0}")
    require(actual == example.native(example.section(example.root, "x")), "actual positive population guard")
    denied = doc.section(block, "NOR")
    require(set(doc.values(denied, "has_country_flag")) == FLAGS and len(doc.entries(denied)) == len(FLAGS), "all pending/ticket guards")
    negative = doc.values(block, "NOT")
    require(len(negative) == 3 + int(replay), "single-child NOT guards")
    projects, repeat = set(), 0
    for neg in negative:
        require(len(doc.entries(neg)) == 1, "ambiguous multiple-child NOT")
        project = doc.scalar(neg, "is_researching_special_project", False)
        if project:
            projects.add(project)
        else:
            scope = doc.section(neg, "capital_scope")
            require(doc.scalar(scope, "has_modifier") == KEY, "replay target must be actual capital")
            repeat += 1
    require(projects == PROJECTS and repeat == int(replay), "project/replay guard")


def validate_sources(event_text, modifier_text):
    doc = reader.Document(event_text)
    require(doc.scalar(doc.root, "namespace") == "shishan_econ_probe", "namespace")
    event = doc.section(doc.root, "country_event")
    require(doc.scalar(event, "id") == "shishan_econ_probe.40", "event ID")
    require(doc.scalar(event, "hide_window") == doc.scalar(event, "is_triggered_only") == "yes", "hidden triggered-only")
    guard(doc, doc.section(event, "trigger"), False)
    immediate = doc.section(event, "immediate")
    require([e.key for e in doc.entries(immediate)] == ["if", "else"], "unregistered immediate action")
    body = doc.section(immediate, "if")
    guard(doc, doc.section(body, "limit"), True)
    require([e.key for e in doc.entries(body)] == ["limit", "capital_scope", "log"], "only actual capital may be modified")
    capital = doc.section(body, "capital_scope")
    require([e.key for e in doc.entries(capital)] == ["add_modifier"], "unexpected capital mutation")
    mutation = doc.section(capital, "add_modifier")
    require(doc.native(mutation) == [{"key": "modifier", "value": KEY}, {"key": "days", "value": "-1"}], "single permanent input")
    require(doc.scalar(body, "log") == "SHISHAN_ECON_PROBE_40_READY_STABILITY_CONTROL", "READY marker")
    failure = doc.section(immediate, "else")
    require(doc.native(failure) == [{"key": "log", "value": "SHISHAN_ECON_PROBE_40_BLOCKED_PREREQUISITE_OR_REPLAY"}], "BLOCKED marker")
    mods = reader.Document(modifier_text)
    require([e.key for e in mods.entries()] == [KEY], "single isolated modifier")
    require(mods.native(mods.section(mods.root, KEY)) == [{"key": "planet_stability_add", "value": "100"}], "no direct output/upkeep/state writing")


class StabilityFixtureTests(unittest.TestCase):
    def test_actual_fixture_contract(self):
        validate_sources(EVENT.read_text(encoding="utf-8"), MODIFIER.read_text(encoding="utf-8"))

    def test_missing_replay_guard_rejected(self):
        text = EVENT.read_text(encoding="utf-8").replace("    NOT = { capital_scope = { has_modifier = shishan_econ_probe_stability_control } }\n", "")
        with self.assertRaises(ValueError):
            validate_sources(text, MODIFIER.read_text(encoding="utf-8"))

    def test_wrong_mutation_scope_rejected(self):
        text = EVENT.read_text(encoding="utf-8").replace("   capital_scope = {\n    add_modifier", "   owner = {\n    add_modifier")
        with self.assertRaises(ValueError):
            validate_sources(text, MODIFIER.read_text(encoding="utf-8"))

    def test_output_or_upkeep_smuggling_rejected(self):
        for field in ("planet_jobs_produces_mult", "planet_jobs_upkeep_mult"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_sources(EVENT.read_text(encoding="utf-8"), MODIFIER.read_text(encoding="utf-8").replace("planet_stability_add = 100", "planet_stability_add = 100\n " + field + " = .4"))

    def test_missing_pending_guard_rejected(self):
        text = EVENT.read_text(encoding="utf-8").replace("has_country_flag = shishan_code_clean_success_pending", "has_country_flag = unrelated_flag")
        with self.assertRaises(ValueError):
            validate_sources(text, MODIFIER.read_text(encoding="utf-8"))

    def test_direct_variable_or_resource_write_rejected(self):
        text = EVENT.read_text(encoding="utf-8").replace('   log = "SHISHAN_ECON_PROBE_40_READY_STABILITY_CONTROL"', '   set_variable = { which = fake_expected_output value = 100 }\n   log = "SHISHAN_ECON_PROBE_40_READY_STABILITY_CONTROL"')
        with self.assertRaises(ValueError):
            validate_sources(text, MODIFIER.read_text(encoding="utf-8"))

    def test_all_localisations_have_bom_header_and_exact_key(self):
        for language in ("braz_por", "english", "french", "german", "japanese", "korean", "polish", "russian", "simp_chinese", "spanish"):
            with self.subTest(language=language):
                path = FIXTURE / "localisation" / language / f"shishan_econ_stability_probe_l_{language}.yml"
                raw = path.read_bytes()
                self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
                lines = raw.decode("utf-8-sig").splitlines()
                self.assertEqual(f"l_{language}:", lines[0])
                self.assertEqual(2, len(lines))
                self.assertRegex(lines[1], '^ ' + KEY + r':0 "[^"\r\n]+"$')
                if language != "simp_chinese":
                    self.assertIsNone(re.search("\u7ecf\u6d4e|\u7a33\u5b9a|\u63a7\u5236", lines[1]))


if __name__ == "__main__":
    unittest.main()
