"""Synthetic offline guard inputs only: never native or Steam acceptance evidence."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import publish_1019 as release


class Release1019Guards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("mod/descriptor.mod", b'version="0.4.0-rc.2"\nname="synthetic guard input"\n')
        self.write("mod/events/synthetic.txt", b"# synthetic guard input\n")
        self.write("mod/common/component_templates/synthetic.txt",
                   b'weapon_component_template = { key = "EEP_SYNTHETIC_GUARD" type = planet_killer }\n')
        self.write("mod/common/on_actions/synthetic.txt", self.callbacks("EEP_SYNTHETIC_GUARD").encode())
        self.write("mod/common/component_templates/synthetic.csv", b"key;cost;end\nEEP_SYNTHETIC_GUARD;0;\n")
        self.write("mod/gfx/synthetic.dds", b"synthetic guard bytes, not a DDS")
        for language in release.LANGUAGES:
            self.write(f"mod/localisation/{language}/synthetic_l_{language}.yml",
                       f'l_{language}:\n synthetic_one:0 "one"\n synthetic_two:0 "two"\n'.encode("utf-8-sig"))
        self.write("VERSION", b"0.4.0-rc.2\n")
        self.report = {"status": "PASS", "game_exe_sha256": release.update.EXE_SHA,
                       "p_scripts": 4, "p_parsed": 4, "dds": 1,
                       "languages": sorted(release.LANGUAGES), "localization_keys": 2,
                       "localization_applicability": "checked", "weapon_csv_files": 1,
                       "weapon_csv_keys": 1, "weapon_csv_applicability": "checked",
                       "planet_killer_callback_contract": release.PLANET_KILLER_CALLBACK_CONTRACT,
                       "planet_killer_components": 1, "planet_killer_callbacks_required": 3,
                       "planet_killer_callbacks_resolved": 3, "planet_killer_callback_applicability": "checked",
                       "errors": []}
        self.json("proofs/synthetic-static.json", self.report)
        self.evidence = []
        for kind in sorted(release.EVIDENCE_KINDS):
            path = f"proofs/synthetic-{kind}.txt"
            self.write(path, ("synthetic guard test: " + kind).encode())
            self.evidence.append(self.reference(path, kind))
        self.runtime = {"schema": "eep-1019-acceptance-v1", "status": "PASS_SCOPED",
            "version": "0.4.0-rc.2", "formal_version": release.VERSION,
            "language": "l_simp_chinese", "game_exe_sha256": release.update.EXE_SHA,
            "profile_id": release.PROFILE, "enabled_mods": release.ENABLED_MODS,
            "fully_accepted_civics": [], "production_files": release.update.base.manifest(self.root / "mod"),
            "candidate_descriptor": (self.root / "mod/descriptor.mod").read_bytes().decode("utf-8"),
            "component_rewards": {"status": "DEFERRED", "interval_levels": 5,
                "reason": "Synthetic deferred-scope guard test only", "evidence": [self.evidence[0]],
                "release_scope_authorization": {"decision": "USER_APPROVED_SCOPE_CHANGE",
                    "evidence": [self.evidence[0]]}},
            "growth_samples": [{"C": count, "L": level} for count, level in release.GROWTH_SAMPLES],
            "archives": [self.evidence[0]]}
        tree = release.candidate_tree(self.runtime, self.root)
        self.runtime["production_tree_sha256"] = tree
        self.runtime["static_gate"] = {"report": self.reference("proofs/synthetic-static.json"),
            "production_files": self.runtime["production_files"], "production_tree_sha256": tree}
        manifest = {"schema": "xenoamess.stellaris.acceptance-run.v1", "run_id": "synthetic-run",
            "profile_id": release.PROFILE, "language": "l_simp_chinese",
            "enabled_mods": release.ENABLED_MODS, "game_exe_sha256": release.update.EXE_SHA,
            "repository_mod_files": [{"path": name, "sha256": sha} for name, sha in self.runtime["production_files"].items()],
            "repository_mod_tree_sha256": tree, "copied_mod_tree_sha256": tree,
            "static_gate": {"status": "PASS", "version": "0.4.0-rc.2", "source_tree_sha256": tree,
                            "report_sha256": self.runtime["static_gate"]["report"]["sha256"]}}
        self.json("proofs/manifest.json", manifest)
        self.runtime["runs"] = [self.reference("proofs/manifest.json")]
        self.runtime["cases"] = {name: self.case(checks) for name, checks in release.CASE_CHECKS.items()}
        self.runtime["economy"] = {}
        for branch in ("hive", "machine", "purifier"):
            budget = {}
            for role in ("baseline", "candidate"):
                rows = []
                for index in range(12):
                    month = index + 2
                    date = f"2200.{month:02}.01" if month <= 12 else "2201.01.01"
                    name = f"proofs/{branch}-{role}-{index}.sav"
                    self.write(name, ("synthetic guard bytes: " + name).encode())
                    entry = self.reference(name, "native_save")
                    rows.append({"date": date, "net_energy": -10.0 if role == "baseline" else 0.1,
                                 "evidence": entry})
                    if role == "candidate":
                        self.runtime["cases"][f"{branch}_economy"]["evidence"].append(entry)
                budget[role + "_months"] = rows
            self.runtime["economy"][branch] = budget
        self.evidence_root = self.root / "docs/evidence/publication-0.4.0"
        self.runtime_path = self.root / "docs/evidence/1019-requirements/final-result.json"

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path

    def json(self, name, data):
        return self.write(name, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    def reference(self, name, kind=None):
        entry = {"path": name, "sha256": release.update.digest((self.root / name).read_bytes())}
        if kind:
            entry["kind"] = kind
        return entry

    def case(self, checks):
        return {"status": "PASS_SCOPED", "production_tree_sha256": self.runtime["production_tree_sha256"],
                "checks": {check: True for check in checks}, "run_ids": ["synthetic-run"],
                "evidence": copy.deepcopy(self.evidence)}

    def callbacks(self, key):
        return "\n".join(f"on_destroy_planet_with_{key}{suffix} = {{}}" for suffix in ("", "_queued", "_unqueued")) + "\n"

    def validate(self, runtime=None):
        return release.validate_runtime_index(self.runtime if runtime is None else runtime, self.root)

    def formalize(self):
        raw = (self.root / "mod/descriptor.mod").read_bytes().replace(b"0.4.0-rc.2", b"0.4.0")
        self.write("mod/descriptor.mod", raw)
        self.write("VERSION", b"0.4.0\n")
        self.json("docs/evidence/1019-requirements/final-result.json", self.runtime)
        self.json("docs/evidence/publication-0.3.1/workshop-verification.json",
                  {"status": "PASS", "version": "0.3.1", "item_id": release.update.ITEM})
        self.json("docs/evidence/publication-0.4.0/open-kaishek.json", self.report)

    def module_paths(self):
        return patch.multiple(release, ROOT=self.root, EVIDENCE=self.evidence_root, RUNTIME=self.runtime_path)

    def test_complete_synthetic_input_and_later_release_candidate(self):
        self.assertEqual(self.validate()["version"], "0.4.0-rc.2")
        self.assertEqual(len(self.runtime["cases"]), 17)

    def test_requires_exact_environment_and_candidate_version(self):
        fields = (("status", "PENDING"), ("schema", "eep-single-homeworld-acceptance-v1"),
                  ("version", "0.3.2-rc.2"), ("version", "0.4.0"), ("formal_version", "0.3.2"),
                  ("language", "l_english"), ("game_exe_sha256", "0" * 64),
                  ("profile_id", "eep-0.3.2-single-homeworld"), ("enabled_mods", ["one", "two"]),
                  ("fully_accepted_civics", ["all"]), ("production_tree_sha256", "0" * 64))
        for field, value in fields:
            with self.subTest(field=field, value=value), self.assertRaises(RuntimeError):
                self.validate({**self.runtime, field: value})

    def test_every_required_group_and_check_must_pass(self):
        for name in release.CASE_CHECKS:
            for mode in ("missing", "failed", "false-check", "missing-check", "wrong-run", "old-tree"):
                bad = copy.deepcopy(self.runtime)
                if mode == "missing":
                    del bad["cases"][name]
                elif mode == "failed":
                    bad["cases"][name]["status"] = "FAIL"
                elif mode == "false-check":
                    bad["cases"][name]["checks"][next(iter(release.CASE_CHECKS[name]))] = False
                elif mode == "missing-check":
                    del bad["cases"][name]["checks"][next(iter(release.CASE_CHECKS[name]))]
                elif mode == "wrong-run":
                    bad["cases"][name]["run_ids"] = ["old-032-run"]
                else:
                    bad["cases"][name]["production_tree_sha256"] = "0" * 64
                with self.subTest(case=name, mode=mode), self.assertRaises(RuntimeError):
                    self.validate(bad)

    def test_case_requires_all_native_evidence_kinds(self):
        for kind in release.EVIDENCE_KINDS:
            bad = copy.deepcopy(self.runtime)
            bad["cases"]["colossus_enemy_fire"]["evidence"] = [entry for entry in self.evidence if entry["kind"] != kind]
            with self.subTest(kind=kind), self.assertRaises(RuntimeError):
                self.validate(bad)

    def test_changed_external_and_duplicate_evidence_is_rejected(self):
        entries = [self.evidence[0]]
        for path in ("../outside", "C:/outside", "C:\\outside", "/outside", "proofs\\escape", "//server/share"):
            with self.subTest(path=path), self.assertRaises(RuntimeError):
                release.verify_references([{**entries[0], "path": path}], self.root)
        with self.assertRaises(RuntimeError):
            release.verify_references(entries * 2, self.root)
        self.write(entries[0]["path"], b"changed synthetic proof")
        with self.assertRaises(RuntimeError):
            self.validate()

    def test_run_manifest_cannot_reuse_old_candidate_or_other_mod(self):
        original = json.loads((self.root / "proofs/manifest.json").read_text())
        for field, value in (("profile_id", "eep-0.3.2-single-homeworld"), ("language", "l_english"),
                             ("enabled_mods", ["another"]), ("repository_mod_files", []),
                             ("copied_mod_tree_sha256", "0" * 64), ("static_gate", {})):
            self.json("proofs/manifest.json", {**original, field: value})
            bad = {**self.runtime, "runs": [self.reference("proofs/manifest.json")]}
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                self.validate(bad)

    def test_all_months_must_be_finite_nonnegative_consecutive_and_distinct(self):
        mutations = (lambda rows: rows.pop(), lambda rows: rows[0].update(net_energy=-0.01),
                     lambda rows: rows[0].update(net_energy=float("nan")),
                     lambda rows: rows[0].update(net_energy=float("inf")),
                     lambda rows: rows[0].update(net_energy=True),
                     lambda rows: rows[1].update(date=rows[0]["date"]),
                     lambda rows: rows[1].update(date="2200.04.01"),
                     lambda rows: rows[1].update(evidence=rows[0]["evidence"]))
        for index, mutation in enumerate(mutations):
            bad = copy.deepcopy(self.runtime)
            mutation(bad["economy"]["machine"]["candidate_months"])
            with self.subTest(index=index), self.assertRaises(RuntimeError):
                self.validate(bad)
        bad = copy.deepcopy(self.runtime)
        bad["economy"]["hive"]["candidate_months"] = bad["economy"]["hive"]["baseline_months"]
        for row in bad["economy"]["hive"]["candidate_months"]:
            row["net_energy"] = 1
        with self.assertRaises(RuntimeError):
            self.validate(bad)

    def test_growth_samples_cannot_be_capped(self):
        for value in ([], [{"C": 200, "L": 3}], [{"C": count, "L": min(level, 3)} for count, level in release.GROWTH_SAMPLES]):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                self.validate({**self.runtime, "growth_samples": value})

    def test_component_scope_must_be_explicit_and_extra_case_is_required(self):
        for change in ({"status": "PASS"}, {"interval_levels": 10}, {"reason": ""}, {"evidence": []}):
            bad = copy.deepcopy(self.runtime)
            bad["component_rewards"].update(change)
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                self.validate(bad)
        bad = copy.deepcopy(self.runtime)
        bad["component_rewards"]["status"] = "IMPLEMENTED"
        with self.assertRaises(RuntimeError):
            self.validate(bad)
        bad["cases"]["random_components"] = self.case(release.COMPONENT_CHECKS)
        self.validate(bad)
        bad["cases"]["random_components"]["checks"]["positive_effect_observed"] = False
        with self.assertRaises(RuntimeError):
            self.validate(bad)

    def test_relic_auxiliary_preservation_allows_an_extra_real_component_slot(self):
        case = self.runtime["cases"]["mothership_configuration"]
        self.assertIn("five_relic_auxiliary_components_preserved", case["checks"])
        self.assertNotIn("five_auxiliary_slots", case["checks"])
        # Synthetic observations document that the contract preserves the five
        # Relic components; it imposes no total-slot cap on extra real hardware.
        case["observations"] = {"auxiliary_slots": 6, "relic_auxiliary_components": 5,
                                "extra_component": "EEP_ADAPTIVE_SHIELD_CORE"}
        self.validate()
        case["checks"]["five_auxiliary_slots"] = case["checks"].pop("five_relic_auxiliary_components_preserved")
        with self.assertRaisesRegex(RuntimeError, "mothership_configuration"):
            self.validate()

    def test_real_component_tier_upgrade_requires_native_ownership_and_probe_evidence(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["component_rewards"]["status"] = "IMPLEMENTED"
        runtime["cases"]["random_components"] = self.case(release.COMPONENT_CHECKS)
        runtime["cases"]["random_components"]["observations"] = {
            "delivery": "PREINSTALLED_COMPONENT_TIER_UPGRADE", "tiers_observed": [0, 1, 2]}
        self.validate(runtime)
        required = ("equipped_component_present_in_native_design", "component_owns_dynamic_bonus",
                    "no_external_reward_modifier", "native_tier_zero_one_two_effect",
                    "growth_modifier_held_constant_during_component_probe", "cross_threshold_catchup")
        for check in required:
            for value in (None, False):
                bad = copy.deepcopy(runtime)
                if value is None:
                    del bad["cases"]["random_components"]["checks"][check]
                else:
                    bad["cases"]["random_components"]["checks"][check] = value
                with self.subTest(check=check, value=value), self.assertRaisesRegex(RuntimeError, "random_components"):
                    self.validate(bad)

    def test_conditional_alternative_authorization_does_not_select_fallback(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["component_rewards"].update(status="AUTHORIZED_ALTERNATIVE")
        with self.assertRaisesRegex(RuntimeError, "implementation scope"):
            self.validate(runtime)
        runtime["component_rewards"].update(status="DEFERRED", release_scope_authorization={
            "decision": "CONDITIONAL_ALTERNATIVE_APPROVED", "evidence": [self.evidence[0]]})
        with self.assertRaisesRegex(RuntimeError, "explicit user scope-change"):
            self.validate(runtime)

    def test_deferred_scope_disclosure_never_substitutes_for_user_authorization(self):
        for authorization in ({}, {"decision": "ASSUMED_APPROVAL", "evidence": [self.evidence[0]]},
                              {"decision": "USER_APPROVED_SCOPE_CHANGE", "evidence": []}):
            bad = copy.deepcopy(self.runtime)
            bad["component_rewards"]["release_scope_authorization"] = authorization
            with self.subTest(authorization=authorization), self.assertRaises(RuntimeError):
                self.validate(bad)

    def test_scaffold_contains_no_acceptance_claim_or_predicted_observation(self):
        pending = release.build_pending_index(self.root)
        self.assertEqual(pending["status"], "PENDING")
        self.assertFalse(pending["_scaffold"]["acceptance_claims"])
        self.assertEqual(pending["component_rewards"]["status"], "PENDING")
        self.assertNotIn("release_scope_authorization", pending["component_rewards"])
        self.assertEqual(pending["growth_samples"], [])
        self.assertEqual(len(pending["cases"]), 18)
        self.assertEqual(pending["cases"]["random_components"]["status"], "PENDING")
        self.assertIsNone(pending["static_gate"]["report"])
        for case in pending["cases"].values():
            self.assertEqual(case["status"], "PENDING")
            self.assertTrue(all(value is None for value in case["checks"].values()))
            self.assertEqual(case["evidence"], [])
        for budget in pending["economy"].values():
            self.assertEqual(budget, {"baseline_months": [], "candidate_months": []})
        with self.assertRaises(RuntimeError):
            self.validate(pending)

    def test_scaffold_can_repeat_and_refresh_untouched_inventory(self):
        result = release.write_pending_index(self.root)
        output = self.root / result["output"]
        self.assertTrue(result["changed"])
        original = output.read_bytes()
        repeated = release.write_pending_index(self.root)
        self.assertFalse(repeated["changed"])
        self.assertEqual(original, output.read_bytes())
        self.write("mod/events/synthetic.txt", b"# changed inventory, still not native evidence\n")
        refreshed = release.write_pending_index(self.root)
        self.assertTrue(refreshed["changed"])
        self.assertNotEqual(result["production_tree_sha256"], refreshed["production_tree_sha256"])
        self.assertEqual(json.loads(output.read_text())["status"], "PENDING")

    def test_scaffold_collects_only_real_reference_hashes_without_promoting_pass(self):
        plan = {"static_report": "proofs/synthetic-static.json", "runs": ["proofs/manifest.json"],
                "cases": {"hive_startup": {"run_ids": ["synthetic-run"],
                    "evidence": [{"path": self.evidence[0]["path"], "kind": self.evidence[0]["kind"]}]}},
                "component_evidence": [{"path": self.evidence[1]["path"], "kind": self.evidence[1]["kind"]}],
                "archives": ["proofs/manifest.json"]}
        self.json("docs/reference-plan.json", plan)
        result = release.write_pending_index(self.root, reference_plan="docs/reference-plan.json")
        pending = json.loads((self.root / result["output"]).read_text())
        self.assertEqual(pending["static_gate"]["report"], self.reference("proofs/synthetic-static.json"))
        self.assertEqual(pending["runs"], [self.reference("proofs/manifest.json")])
        self.assertEqual(pending["cases"]["hive_startup"]["run_ids"], ["synthetic-run"])
        self.assertEqual(pending["cases"]["hive_startup"]["evidence"], [self.evidence[0]])
        self.assertEqual(pending["status"], "PENDING")
        self.assertTrue(all(value is None for value in pending["cases"]["hive_startup"]["checks"].values()))

    def test_scaffold_rejects_plan_results_or_missing_external_references(self):
        plans = ({"status": "PASS_SCOPED"}, {"growth_samples": [{"C": 0, "L": 0}]},
                 {"economy": {}}, {"cases": {"hive_startup": {"checks": {"single_homeworld": True}}}},
                 {"cases": {"not-a-case": {}}}, {"runs": ["../outside"]},
                 {"static_report": "proofs/missing.json"}, {"runs": [{"path": "proofs/manifest.json", "sha256": "0" * 64}]})
        for plan in plans:
            with self.subTest(plan=plan), self.assertRaises(RuntimeError):
                release.build_pending_index(self.root, plan)

    def test_scaffold_never_overwrites_reviewed_index_or_production(self):
        result = release.write_pending_index(self.root)
        output = self.root / result["output"]
        for mutation in (lambda data: data["cases"]["hive_startup"]["checks"].update(single_homeworld=True),
                         lambda data: data.update(status="PASS_SCOPED"),
                         lambda data: data["component_rewards"].update(reason="manually researched conclusion")):
            output.unlink()
            release.write_pending_index(self.root)
            data = json.loads(output.read_text())
            mutation(data)
            output.write_text(json.dumps(data), encoding="utf-8")
            preserved = output.read_bytes()
            with self.assertRaisesRegex(RuntimeError, "refuse to overwrite"):
                release.write_pending_index(self.root)
            self.assertEqual(output.read_bytes(), preserved)
        for target in ("docs/evidence/1019-requirements/final-result.json", "mod/unwanted.json", "../outside.json"):
            with self.subTest(target=target), self.assertRaises(RuntimeError):
                release.write_pending_index(self.root, output=target)

    def test_formal_content_only_allows_descriptor_version(self):
        self.formalize()
        files = release.update.base.manifest(self.root / "mod")
        release.validate_candidate_files(files, self.runtime)
        self.validate()
        for name in ("events/synthetic.txt", "unexpected.txt", "descriptor.mod"):
            changed = {**files, name: "0" * 64}
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                release.validate_candidate_files(changed, self.runtime)

    def test_candidate_descriptor_and_production_paths_are_validated(self):
        for value in ("version=\"0.4.0-rc.2\"\n" * 2, 'version="0.3.2-rc.2"\n',
                      'version="0.4.0-rc.2"\nremote_file_id="3815707212"\n'):
            bad = {**self.runtime, "candidate_descriptor": value}
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                release.candidate_files(bad)
        for name in ("../outside", "C:/outside", "eep_probe.txt", "testing/fixture.txt"):
            bad = {**self.runtime, "production_files": {**self.runtime["production_files"], name: "0" * 64}}
            with self.subTest(path=name), self.assertRaises(RuntimeError):
                release.candidate_files(bad)

    def test_static_counts_are_derived_from_current_package(self):
        release.validate_static_report(self.report, self.root)
        self.write("mod/common/synthetic.gui", b"# synthetic GUI guard test")
        with self.assertRaises(RuntimeError):
            release.validate_static_report(self.report, self.root)
        release.validate_static_report({**self.report, "p_scripts": 5, "p_parsed": 5}, self.root)

    def test_planet_killer_contract_rejects_old_reports_or_unresolved_callbacks(self):
        fields = ("planet_killer_callback_contract", "planet_killer_components", "planet_killer_callbacks_required",
                  "planet_killer_callbacks_resolved", "planet_killer_callback_applicability")
        for field in fields:
            missing = {key: value for key, value in self.report.items() if key != field}
            with self.subTest(missing=field), self.assertRaisesRegex(RuntimeError, "planet-killer callback contract"):
                release.validate_static_report(missing, self.root)
        for field, value in (("planet_killer_callback_contract", "csv_only_v0"),
                             ("planet_killer_components", 0), ("planet_killer_components", 2),
                             ("planet_killer_components", True), ("planet_killer_callbacks_required", 2),
                             ("planet_killer_callbacks_resolved", 2), ("planet_killer_callbacks_resolved", 0),
                             ("planet_killer_callback_applicability", "not_applicable_no_planet_killer_components")):
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "planet-killer callback contract"):
                release.validate_static_report({**self.report, field: value}, self.root)

    def test_planet_killer_source_requires_all_three_actual_root_callbacks(self):
        names = [f"on_destroy_planet_with_EEP_SYNTHETIC_GUARD{suffix}" for suffix in ("", "_queued", "_unqueued")]
        for missing in names:
            for fake in (f"# {missing} = {{}}", f"wrapper = {{ {missing} = {{}} }}", f'text = "{missing} = {{}}"'):
                source = "\n".join(f"{name} = {{}}" for name in names if name != missing) + "\n" + fake + "\n"
                self.write("mod/common/on_actions/synthetic.txt", source.encode())
                with self.subTest(missing=missing, fake=fake), self.assertRaisesRegex(RuntimeError, "callback definitions missing"):
                    release.validate_static_report(self.report, self.root)

    def test_planet_killer_counts_only_real_weapon_blocks_and_scales_to_multiple_components(self):
        component = 'weapon_component_template = { key = "EEP_SYNTHETIC_GUARD" type = planet_killer }\n'
        ignored = ('utility_component_template = { key = "UTILITY" type = planet_killer }\n'
                   '# weapon_component_template = { key = "COMMENT" type = planet_killer }\n'
                   'wrapper = { weapon_component_template = { key = "NESTED" type = planet_killer } }\n'
                   'text = "weapon_component_template = { key = FAKE type = planet_killer }"\n')
        self.write("mod/common/component_templates/synthetic.txt", (component + ignored).encode())
        self.assertEqual(release.planet_killer_component_keys(self.root / "mod/common/component_templates"), {"EEP_SYNTHETIC_GUARD"})
        release.validate_static_report(self.report, self.root)
        self.write("mod/common/component_templates/synthetic.txt", (component + ignored +
            'weapon_component_template = { key = "SECOND_SYNTHETIC" type = "planet_killer" }\n').encode())
        self.write("mod/common/component_templates/synthetic.csv", b"key;cost;end\nEEP_SYNTHETIC_GUARD;0;\nSECOND_SYNTHETIC;0;\n")
        self.write("mod/common/on_actions/synthetic.txt", (self.callbacks("EEP_SYNTHETIC_GUARD") + self.callbacks("SECOND_SYNTHETIC")).encode())
        report = {**self.report, "weapon_csv_keys": 2, "planet_killer_components": 2,
                  "planet_killer_callbacks_required": 6, "planet_killer_callbacks_resolved": 6}
        release.validate_static_report(report, self.root)
        for field, value in (("planet_killer_components", 1), ("planet_killer_callbacks_required", 3),
                             ("planet_killer_callbacks_resolved", 3)):
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, "planet-killer callback contract"):
                release.validate_static_report({**report, field: value}, self.root)

    def test_weapon_csv_report_must_cover_actual_files_and_component_keys(self):
        for field, value in (("weapon_csv_files", 0), ("weapon_csv_keys", 0),
                             ("weapon_csv_files", 2), ("weapon_csv_keys", 2),
                             ("weapon_csv_applicability", "not_applicable_no_weapon_csv_files")):
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "weapon CSV"):
                release.validate_static_report({**self.report, field: value}, self.root)
        for field in ("weapon_csv_files", "weapon_csv_keys", "weapon_csv_applicability"):
            missing = {key: value for key, value in self.report.items() if key != field}
            with self.subTest(missing=field), self.assertRaisesRegex(RuntimeError, "weapon CSV"):
                release.validate_static_report(missing, self.root)
        self.write("mod/common/component_templates/synthetic.csv", b"key;cost;end\nMISSING_COMPONENT;0;\n")
        with self.assertRaisesRegex(RuntimeError, "component keys"):
            release.validate_static_report(self.report, self.root)

    def test_static_report_requires_whole_package_pass(self):
        for field, value in (("status", "FAIL"), ("game_exe_sha256", "0" * 64),
                             ("p_parsed", 1), ("dds", 2), ("languages", ["english"]),
                             ("localization_keys", 101), ("localization_applicability", "unchecked"),
                             ("errors", ["synthetic failure"])):
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                release.validate_static_report({**self.report, field: value}, self.root)

    def test_static_localization_headers_bom_and_coverage(self):
        path = "mod/localisation/english/synthetic_l_english.yml"
        for raw in (b'l_english:\n synthetic_one:0 "one"\n',
                    'l_french:\n synthetic_one:0 "one"\n'.encode("utf-8-sig"),
                    'l_english:\n synthetic_one:0 "one"\n'.encode("utf-8-sig")):
            self.write(path, raw)
            with self.subTest(raw=raw), self.assertRaises(RuntimeError):
                release.validate_static_report(self.report, self.root)

    def test_formal_static_record_and_acceptance_bind_report_and_package(self):
        self.formalize()
        with self.module_paths():
            release.record_static()
            acceptance = release.accepted_files()
            self.assertEqual(acceptance["candidate_version"], "0.4.0-rc.2")
            self.assertEqual(acceptance["previous_public_version"], "0.3.1")
            self.write("docs/evidence/publication-0.4.0/open-kaishek.json",
                       (json.dumps(self.report) + "\n ").encode())
            with self.assertRaisesRegex(RuntimeError, "formal static source or report changed"):
                release.accepted_files()

    def test_record_static_rejects_prerelease_and_unaccepted_candidate(self):
        with self.module_paths(), self.assertRaisesRegex(RuntimeError, "formal VERSION"):
            release.record_static()
        self.formalize()
        self.runtime["cases"]["colossus_enemy_fire"]["status"] = "PENDING"
        self.json("docs/evidence/1019-requirements/final-result.json", self.runtime)
        with self.module_paths(), self.assertRaises(RuntimeError):
            release.record_static()

    def test_ws06_requires_new_name_final_candidate_run_and_accepted_sources(self):
        screenshot = next(entry for entry in self.evidence if entry["kind"] == "screenshot")
        save = next(entry for entry in self.evidence if entry["kind"] == "native_save")
        gallery = [{"id": f"WS-{index:02}", "role": "gallery"} for index in range(1, 7)]
        gallery[-1].update(file="images/new-04-single-homeworld.jpg", sha256="1" * 64,
            evidence_kind="native_screenshot", run_id="synthetic-run",
            source="../" + screenshot["path"], native_save="../" + save["path"])
        prior = {"gallery": [{"sha256": "0" * 64, "filename": "old-opening.jpg"}] * 6}
        release.validate_gallery(gallery, self.runtime, prior, self.root)
        for field, value in (("file", "images/old-opening.jpg"), ("sha256", "0" * 64),
                             ("run_id", "old-032-run"), ("source", "../wrong.jpg"),
                             ("native_save", "../wrong.sav")):
            bad = copy.deepcopy(gallery)
            bad[-1][field] = value
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                release.validate_gallery(bad, self.runtime, prior, self.root)

    def test_deferred_component_scope_requires_public_disclosure_and_old_inline_urls(self):
        pictures = [{"url": f"https://immutable.invalid/{index}", "sha256": str(index) * 64} for index in range(4)]
        prior = {"inline_images": [{"source": picture["url"], "sha256": picture["sha256"]} for picture in pictures]}
        with (patch.object(release, "load_runtime", return_value=self.runtime),
              patch.object(release, "prior_release", return_value=prior),
              patch.object(release.update, "release_entry", return_value="每5级随机组件未实现")):
            with patch.object(release, "_description_inputs", return_value=("每5级随机组件未实现", pictures)):
                release.description_inputs()
            with (patch.object(release, "_description_inputs", return_value=("every feature passed", pictures)),
                  self.assertRaisesRegex(RuntimeError, "deferred component")):
                release.description_inputs()
            with (patch.object(release, "_description_inputs", return_value=("每5级随机组件未实现", pictures[:-1])),
                  self.assertRaisesRegex(RuntimeError, "historical immutable")):
                release.description_inputs()

    def test_adapter_configuration_restores_historical_globals_even_on_failure(self):
        version = release.update.VERSION
        accepted = release.update.accepted_files
        with self.assertRaisesRegex(RuntimeError, "synthetic exception"):
            with release.configured():
                self.assertEqual(release.update.VERSION, "0.4.0")
                self.assertIs(release.update.accepted_files, release.accepted_files)
                raise RuntimeError("synthetic exception")
        self.assertEqual(release.update.VERSION, version)
        self.assertIs(release.update.accepted_files, accepted)

    def test_untested_candidate_and_missing_remote_receipts_cannot_reach_tag(self):
        self.formalize()
        with self.module_paths():
            release.record_static()
            self.json("docs/evidence/publication-0.4.0/publish-state.json", {})
            self.json("docs/evidence/publication-0.4.0/workshop-verification.json", {})
            self.json("docs/evidence/publication-0.4.0/workshop-download.json", {})
            with self.assertRaisesRegex(RuntimeError, "before tag"):
                release.tag_check()

    def test_tag_check_is_read_only_and_binds_media_and_actual_download(self):
        self.write("download/synthetic.bin", b"synthetic independent download")
        files = release.update.base.manifest(self.root / "download")
        acceptance = {"production_files": files, "synthetic_guard_test": True}
        gallery = [{"file": f"workshop/{index}.jpg", "sha256": "1" * 64, "bytes": 10}
                   for index in range(6)]
        pictures = [{"url": f"https://synthetic.invalid/{index}", "sha256": "2" * 64} for index in range(4)]
        inputs = {"acceptance": acceptance, "content": files, "gallery": gallery,
                  "images": gallery, "inline_images": pictures, "description": "synthetic description",
                  "note": "[v0.4.0]\nsynthetic guard input"}
        state = {"version": "0.4.0", "item_id": release.update.ITEM, "submit_result": 1,
                 "submit_item_id": release.update.ITEM, "submit_legal_required": False, "inputs": inputs}
        verified = {"status": "PASS", "version": "0.4.0", "item_id": release.update.ITEM,
            "production_files": files, "download_files": len(files), "public_metadata_exact": True,
            "change_note_exact": True, "gallery_exact": True, "inline_images_exact": True,
            "gallery": [{"index": index, "type": 0, "filename": f"{index}.jpg", "sha256": "1" * 64, "bytes": 10}
                        for index in range(6)],
            "inline_images": [{"source": picture["url"], "sha256": picture["sha256"]} for picture in pictures]}
        downloaded = {"status": "DOWNLOADED", "version": "0.4.0", "item_id": release.update.ITEM,
                      "content": files, "folder": str(self.root / "download")}
        self.json("docs/evidence/publication-0.4.0/publish-state.json", state)
        self.json("docs/evidence/publication-0.4.0/workshop-verification.json", verified)
        self.json("docs/evidence/publication-0.4.0/workshop-download.json", downloaded)
        with (self.module_paths(), patch.object(release, "accepted_files", return_value=acceptance),
              patch.object(release, "description_inputs", return_value=(inputs["description"], pictures)),
              patch.object(release.update, "change_note", return_value=inputs["note"]),
              patch.object(release.update.workshop_images, "local_images", return_value=gallery),
              patch.object(release.update, "git", side_effect=lambda *args: b"" if args[0] == "status" else b"synthetic-head"),
              patch.object(release.update.base.native, "Steam", side_effect=AssertionError("no native Steam in tag check"))):
            self.assertEqual(release.tag_check()["status"], "READY_TO_TAG")
            with (patch.object(release.update.workshop_images, "local_images", return_value=[]),
                  self.assertRaisesRegex(RuntimeError, "frozen images changed")):
                release.tag_check()
            self.write("download/synthetic.bin", b"changed synthetic download")
            with self.assertRaisesRegex(RuntimeError, "downloaded bytes changed"):
                release.tag_check()


if __name__ == "__main__":
    unittest.main()
