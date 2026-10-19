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
                   self.weapon("EEP_SYNTHETIC_GUARD").encode())
        self.write("mod/common/on_actions/synthetic.txt", self.callbacks("EEP_SYNTHETIC_GUARD").encode())
        self.write("mod/gfx/synthetic.dds", b"synthetic guard bytes, not a DDS")
        for language in release.LANGUAGES:
            self.write(f"mod/localisation/{language}/synthetic_l_{language}.yml",
                        f'l_{language}:\n synthetic_one:0 "one"\n synthetic_two:0 "two"\n'.encode("utf-8-sig"))
        # A 59-file synthetic package exercises rc4's CSV-free shape without
        # making production script/localization counts into acceptance constants.
        for index in range(44):
            self.write(f"mod/gfx/synthetic-{index:02}.png", b"synthetic image guard bytes")
        self.write("VERSION", b"0.4.0-rc.2\n")
        self.report = {"status": "PASS", "game_exe_sha256": release.update.EXE_SHA,
                       "p_scripts": 4, "p_parsed": 4, "dds": 1,
                       "languages": sorted(release.LANGUAGES), "localization_keys": 2,
                       "localization_applicability": "checked", "weapon_csv_files": 0,
                       "weapon_csv_keys": 0, "weapon_csv_applicability": "not_applicable_no_weapon_csv_files",
                       "weapon_csv_loader_contract": release.WEAPON_CSV_LOADER_CONTRACT,
                       "weapon_csv_unsupported_files": 0,
                       "planet_killer_callback_contract": release.PLANET_KILLER_CALLBACK_CONTRACT,
                       "planet_killer_components": 1, "planet_killer_callbacks_required": 3,
                       "planet_killer_callbacks_resolved": 3, "planet_killer_callback_applicability": "checked",
                       "planet_killer_numeric_contract": release.PLANET_KILLER_NUMERIC_CONTRACT,
                       "planet_killer_numeric_components": 1, "planet_killer_numeric_resolved": 1,
                       "planet_killer_numeric_applicability": "checked",
                       "planet_killer_numeric_sources": self.numeric_sources(),
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

    def implemented_components(self, runtime=None):
        runtime = copy.deepcopy(self.runtime) if runtime is None else runtime
        # This package is synthetic guard input, never the real RC5 source tree.
        source_tree = patch.object(release, "COMPONENT_SOURCE_TREE", runtime["production_tree_sha256"])
        source_tree.start()
        self.addCleanup(source_tree.stop)
        runtime["component_rewards"].update(status="IMPLEMENTED", reason="Synthetic six-core guard input only")
        case = self.case(release.COMPONENT_CHECKS)
        runtime["cases"]["random_components"] = case
        native = []
        for index in range(2 * len(release.COMPONENT_NODES)):
            name = f"proofs/synthetic-growth-{index:02}.sav"
            self.write(name, f"synthetic guard bytes, never native SAV: {index}".encode())
            entry = self.reference(name, "native_save")
            case["evidence"].append(entry)
            native.append({"sha256": entry["sha256"], "phase": {
                "C": release.COMPONENT_NODES[index // 2], "phase": "refresh" if index % 2 == 0 else "final"}})
        passed = {"status": "PASS_SCOPED", "checks": [{"check": "synthetic guard input only", "passed": True}]}
        tiers = dict.fromkeys(release.COMPONENT_KINDS, 33)
        tiers["shield"] = 35
        report = {"schema": "eep.six-core-growth-report.v1", "status": "PASS_SCOPED",
            "component_attribution_contract": release.COMPONENT_ATTRIBUTION_CONTRACT,
            "run_id": "synthetic-run", "production_tree_sha256": runtime["production_tree_sha256"],
            "absolute_tolerance": .01, "source_models_sha256": list(release.COMPONENT_SOURCE_MODELS),
            "hp_tolerance_contract": release.COMPONENT_HP_TOLERANCE_CONTRACT,
            "hp_tolerance": copy.deepcopy(release.COMPONENT_HP_TOLERANCE),
            **{name: copy.deepcopy(passed) for name in ("matrix", "repeat", "reload", "budget", "ordinary_controls")},
            "nonzero_tier_coverage": dict.fromkeys(release.COMPONENT_KINDS, True),
            "final_native_tiers": tiers, "native_evidence": native,
            "C0_baseline": {"C": 0, "L": 0, "tiers": dict.fromkeys(release.COMPONENT_KINDS, 0),
                "actual_native_intercept": True, "save_sha256": native[1]["sha256"],
                "modifier_exports": dict.fromkeys(release.COMPONENT_MODIFIERS, 0.0),
                "native_maximums": dict.fromkeys(("max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints"), 1000)}}
        report["ordinary_controls"]["ship_ids"] = ["synthetic-ordinary-control"]
        self.attribution_report(runtime, report)
        return runtime, report

    def attribution_report(self, runtime, report):
        name = "proofs/synthetic-component-attribution.json"
        self.json(name, report)
        case = runtime["cases"]["random_components"]
        case["evidence"] = [entry for entry in case["evidence"] if entry["path"] != name]
        case["evidence"].append(self.reference(name, "analysis"))
        case["component_attribution_report"] = self.reference(name)

    def callbacks(self, key):
        return "\n".join(f"on_destroy_planet_with_{key}{suffix} = {{}}" for suffix in ("", "_queued", "_unqueued")) + "\n"

    def weapon(self, key, quoted_type=False):
        kind = '"planet_killer"' if quoted_type else "planet_killer"
        return (f'weapon_component_template = {{ key = "{key}" type = {kind} '
                'windup = { min = 90 max = 90 } total_fire_time = 30 power = 0 }\n')

    def numeric_sources(self, keys=("EEP_SYNTHETIC_GUARD",),
                        name="mod/common/component_templates/synthetic.txt", kind="literal_component_txt"):
        path = self.root / name
        return [{"key": key, "kind": kind, "path": str(path.resolve()), "line": 1,
                 "sha256": release.update.digest(path.read_bytes()),
                 "values": {"windup_min": 90.0, "windup_max": 90.0, "total_fire_time": 30.0, "power": 0.0}}
                for key in keys]

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

    def test_migration_v2_routes_only_its_explicit_strict_damage_failure(self):
        case = self.runtime["cases"]["old_save_migration"]
        case["checks"]["damage_preserved"] = False
        with self.assertRaisesRegex(RuntimeError, "old_save_migration"):
            self.validate()
        case["migration_contract"] = {"schema": "synthetic routing only"}
        case["checks"]["damage_within_predeclared_v2_budget"] = True
        with patch.object(release, "validate_migration_contract") as typed:
            self.validate()
            typed.assert_called_once()
            case["checks"]["identity_preserved"] = False
            with self.assertRaisesRegex(RuntimeError, "old_save_migration"):
                self.validate()
        case["checks"]["identity_preserved"] = True
        with self.assertRaises(RuntimeError):
            self.validate()  # The real typed validator rejects an unknown scope.

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
        self.implemented_components(bad)
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

    def test_real_component_tier_upgrade_requires_native_ownership_and_source_attribution(self):
        runtime, _ = self.implemented_components()
        self.validate(runtime)
        required = ("equipped_component_present_in_native_design", "component_owns_dynamic_bonus",
                    "no_external_reward_modifier", "native_component_effects_source_attributed",
                    "growth_component_contributions_separated", "cross_threshold_catchup")
        for check in required:
            for value in (None, False):
                bad = copy.deepcopy(runtime)
                if value is None:
                    del bad["cases"]["random_components"]["checks"][check]
                else:
                    bad["cases"]["random_components"]["checks"][check] = value
                with self.subTest(check=check, value=value), self.assertRaisesRegex(RuntimeError, "random_components"):
                    self.validate(bad)

    def test_old_fixed_level_check_names_cannot_substitute_for_rng_attribution(self):
        runtime, _ = self.implemented_components()
        for new, old in (("native_component_effects_source_attributed", "native_tier_zero_one_two_effect"),
                         ("growth_component_contributions_separated", "growth_modifier_held_constant_during_component_probe")):
            bad = copy.deepcopy(runtime)
            bad["cases"]["random_components"]["checks"][old] = bad["cases"]["random_components"]["checks"].pop(new)
            with self.subTest(new=new), self.assertRaisesRegex(RuntimeError, "random_components"):
                self.validate(bad)

    def test_each_of_six_channels_needs_actual_nonzero_rng_tier_and_coverage(self):
        runtime, report = self.implemented_components()
        self.validate(runtime)
        for kind in release.COMPONENT_KINDS:
            for field, value in (("nonzero_tier_coverage", False), ("nonzero_tier_coverage", 1),
                                 ("final_native_tiers", 0), ("final_native_tiers", True),
                                 ("final_native_tiers", 1.0), ("final_native_tiers", None)):
                bad, claim = copy.deepcopy(runtime), copy.deepcopy(report)
                if value is None:
                    del claim[field][kind]
                else:
                    claim[field][kind] = value
                self.attribution_report(bad, claim)
                with self.subTest(kind=kind, field=field, value=value), self.assertRaisesRegex(RuntimeError, "random_components"):
                    self.validate(bad)

    def test_attribution_rejects_missing_intercept_exports_models_controls_and_raw_samples(self):
        runtime, report = self.implemented_components()
        changes = {
            "old run": lambda r: r.update(run_id="old-rc3"),
            "old source": lambda r: r.update(production_tree_sha256="0" * 64),
            "incomplete": lambda r: r.update(status="INCOMPLETE"),
            "old contract": lambda r: r.update(component_attribution_contract="fixed_level_probe"),
            "fitted models": lambda r: r.update(source_models_sha256=["0" * 64, "1" * 64]),
            "missing RC5 model": lambda r: r.update(source_models_sha256=list(release.COMPONENT_SOURCE_MODELS[:2])),
            "unknown RC5 model": lambda r: r.update(source_models_sha256=[*release.COMPONENT_SOURCE_MODELS[:2], "0" * 64]),
            "missing RC6 model": lambda r: r.update(source_models_sha256=list(release.COMPONENT_SOURCE_MODELS[:3])),
            "unknown RC6 model": lambda r: r.update(source_models_sha256=[*release.COMPONENT_SOURCE_MODELS[:3], "0" * 64]),
            "missing RC7 model": lambda r: r.update(source_models_sha256=list(release.COMPONENT_SOURCE_MODELS[:4])),
            "unknown RC7 model": lambda r: r.update(source_models_sha256=[*release.COMPONENT_SOURCE_MODELS[:4], "0" * 64]),
            "relaxed tolerance": lambda r: r.update(absolute_tolerance=.1),
            "not actual baseline": lambda r: r["C0_baseline"].update(actual_native_intercept=False),
            "nonzero baseline": lambda r: r["C0_baseline"].update(C=50),
            "boolean baseline": lambda r: r["C0_baseline"].update(L=False),
            "baseline reward": lambda r: r["C0_baseline"]["tiers"].update(shield=1),
            "missing export": lambda r: r["C0_baseline"]["modifier_exports"].pop("ship_tracking_add"),
            "invalid export": lambda r: r["C0_baseline"]["modifier_exports"].update(ship_weapon_damage=float("nan")),
            "boolean export": lambda r: r["C0_baseline"]["modifier_exports"].update(ship_weapon_damage=True),
            "missing maximum": lambda r: r["C0_baseline"]["native_maximums"].pop("max_armor_hitpoints"),
            "no controls": lambda r: r["ordinary_controls"].update(ship_ids=[]),
            "control failure": lambda r: r["ordinary_controls"]["checks"][0].update(passed=False),
            "no matrix": lambda r: r["matrix"].update(checks=[]),
            "integer pass": lambda r: r["matrix"]["checks"][0].update(passed=1),
            "missing reload": lambda r: r["reload"].update(status="NOT_PROVIDED"),
            "missing raw": lambda r: r["native_evidence"].pop(),
            "unbound raw": lambda r: r["native_evidence"][0].update(sha256="0" * 64),
            "duplicate raw": lambda r: r["native_evidence"][0].update(sha256=r["native_evidence"][1]["sha256"]),
            "wrong phase": lambda r: r["native_evidence"][0]["phase"].update(C=10),
            "wrong C0 raw": lambda r: r["C0_baseline"].update(save_sha256=r["native_evidence"][-1]["sha256"]),
        }
        for label, mutate in changes.items():
            bad, claim = copy.deepcopy(runtime), copy.deepcopy(report)
            mutate(claim)
            self.attribution_report(bad, claim)
            with self.subTest(label=label), self.assertRaisesRegex(RuntimeError, "random_components"):
                self.validate(bad)

    def test_attribution_report_must_be_hash_bound_case_analysis(self):
        runtime, report = self.implemented_components()
        bad = copy.deepcopy(runtime)
        del bad["cases"]["random_components"]["component_attribution_report"]
        with self.assertRaisesRegex(RuntimeError, "random_components"):
            self.validate(bad)
        bad = copy.deepcopy(runtime)
        bad["cases"]["random_components"]["evidence"] = [entry for entry in bad["cases"]["random_components"]["evidence"]
            if entry["path"] != "proofs/synthetic-component-attribution.json"]
        with self.assertRaisesRegex(RuntimeError, "random_components"):
            self.validate(bad)

    def test_hp_engineering_policy_accepts_hp_spacing_without_relaxing_modifier_exports(self):
        runtime, report = self.implemented_components()
        # At 2**20 the binary32 spacing is .125. A .5 HP difference is within
        # the predeclared 8-ULP allowance; a flat modifier remains at .01.
        hp = {"check": "refresh 8 max_hitpoints", "passed": True, "expected": 1048576.,
            "actual": 1048576.5, "observed": 1048576.5, "raw_delta": .5,
            "ulp32_expected": .125, "ulp_error": 4., "tolerance_kind": "hp_binary32_ulp_engineering",
            "absolute_tolerance": 1., "applied_tolerance": 1., "relative_tolerance": 0}
        actual, expected = -70000.005, -70000.
        modifier = {"check": "export 8 eep_probe_ship_hull_add", "passed": True, "expected": expected,
            "actual": actual, "observed": actual, "raw_delta": actual - expected,
            "ulp32_expected": .0078125, "ulp_error": abs(actual - expected) / .0078125,
            "tolerance_kind": "fixed_absolute", "absolute_tolerance": .01, "applied_tolerance": .01,
            "relative_tolerance": 0}
        report["matrix"]["checks"].extend([hp, modifier])
        ordinary_hp = copy.deepcopy(hp)
        ordinary_hp["check"] = "ordinary native max 17/5/max_hitpoints"
        report["ordinary_controls"]["checks"].append(ordinary_hp)
        self.attribution_report(runtime, report)
        self.validate(runtime)
        changes = {
            "old report": lambda r: r.pop("hp_tolerance_contract"),
            "old contract": lambda r: r.update(hp_tolerance_contract="unknown"),
            "larger floor": lambda r: r["hp_tolerance"].update(absolute_floor=.1),
            "more ULPs": lambda r: r["hp_tolerance"].update(binary32_ulps=16),
            "float ULP count": lambda r: r["hp_tolerance"].update(binary32_ulps=8.),
            "relative allowance": lambda r: r["hp_tolerance"].update(relative_tolerance=.001),
            "false storage claim": lambda r: r["hp_tolerance"].update(classification="proven_engine_float32"),
            "HP on modifier": lambda r: r["matrix"]["checks"][-2].update(check="export 8 eep_probe_ship_hull_add"),
            "HP ordinary modifier": lambda r: r["ordinary_controls"]["checks"][-1].update(
                check="ordinary native max 17/5/eep_probe_ship_hull_add"),
            "HP policy under fixed label": lambda r: r["matrix"]["checks"][-2].update(tolerance_kind="fixed_absolute"),
            "larger row allowance": lambda r: r["matrix"]["checks"][-2].update(absolute_tolerance=2., applied_tolerance=2.),
            "wrong row spacing": lambda r: r["matrix"]["checks"][-2].update(ulp32_expected=.25),
            "hidden relative row": lambda r: r["matrix"]["checks"][-2].update(relative_tolerance=False),
            "boolean allowance": lambda r: r["matrix"]["checks"][-2].update(absolute_tolerance=True),
            "nonfinite expected": lambda r: r["matrix"]["checks"][-2].update(expected=float("inf")),
            "missing row policy": lambda r: r["matrix"]["checks"][-2].pop("tolerance_kind"),
            "non HP modifier delta": lambda r: r["matrix"]["checks"][-1].update(
                actual=-69999.98, observed=-69999.98, raw_delta=-69999.98 + 70000,
                ulp_error=abs(-69999.98 + 70000) / .0078125),
            "outside HP allowance": lambda r: r["matrix"]["checks"][-2].update(
                actual=1048578., observed=1048578., raw_delta=2., ulp_error=16.),
        }
        for label, mutate in changes.items():
            bad, claim = copy.deepcopy(runtime), copy.deepcopy(report)
            mutate(claim)
            self.attribution_report(bad, claim)
            with self.subTest(label=label), self.assertRaisesRegex(RuntimeError, "random_components"):
                self.validate(bad)

    def test_component_source_models_and_final_tree_match_the_frozen_certificate(self):
        import check_growth_1019 as growth
        folder = release.ROOT / "docs/evidence/1019-analysis"
        self.assertEqual(release.COMPONENT_SOURCE_MODELS, growth.MODEL_HASHES)
        self.assertNotEqual(release.COMPONENT_SOURCE_TREE, growth.SOURCE_TREE)  # historical RC6 default remains intact
        version, frozen_key = growth.SOURCE_REVISIONS[release.COMPONENT_SOURCE_TREE]
        self.assertEqual((version, frozen_key), (5, "frozen_rc7"))
        model = json.loads((folder / f"six-core-source-expectations-v{version}.json").read_text(encoding="utf-8"))
        self.assertEqual(model[frozen_key]["production_tree_sha256"], release.COMPONENT_SOURCE_TREE)
        self.assertEqual(model[frozen_key]["file_count"], 59)
        self.assertEqual(growth.SOURCE_REVISIONS[growth.SOURCE_TREE], (4, "frozen_rc6"))
        self.assertEqual(tuple(release.update.digest((folder / f"six-core-source-expectations-v{i}.json").read_bytes())
                               for i in range(1, len(growth.MODEL_HASHES) + 1)), growth.MODEL_HASHES)
        runtime, _ = self.implemented_components()
        with patch.object(release, "COMPONENT_SOURCE_TREE", "0" * 64):
            with self.assertRaisesRegex(RuntimeError, "random_components"):
                self.validate(runtime)

    def test_rc7_final_component_scope_rejects_rc6_and_unknown_actual_bytes(self):
        final_tree = release.COMPONENT_SOURCE_TREE
        runtime, report = self.implemented_components()
        case = runtime["cases"]["random_components"]
        with patch.object(release, "COMPONENT_SOURCE_TREE", final_tree):
            for tree in ("cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a", "0" * 64):
                old = copy.deepcopy(report)
                old["production_tree_sha256"] = tree
                self.attribution_report(runtime, old)
                with self.subTest(tree=tree), self.assertRaisesRegex(RuntimeError, "current candidate run and source"):
                    release.validate_component_attribution(case, tree, self.root)
            # Correct-looking headers cannot turn this synthetic package's
            # different actual bytes into the pinned RC7 production tree.
            bad = copy.deepcopy(runtime)
            bad["production_tree_sha256"] = final_tree
            with self.assertRaisesRegex(RuntimeError, "candidate production tree differs"):
                self.validate(bad)
        self.write("mod/events/synthetic.txt", b"# unexpected candidate source bytes\n")
        with self.assertRaises(RuntimeError):
            self.validate(runtime)

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
        component = self.weapon("EEP_SYNTHETIC_GUARD")
        ignored = ('utility_component_template = { key = "UTILITY" type = planet_killer }\n'
                   '# weapon_component_template = { key = "COMMENT" type = planet_killer }\n'
                   'wrapper = { weapon_component_template = { key = "NESTED" type = planet_killer } }\n'
                   'text = "weapon_component_template = { key = FAKE type = planet_killer }"\n')
        self.write("mod/common/component_templates/synthetic.txt", (component + ignored).encode())
        self.assertEqual(release.planet_killer_component_keys(self.root / "mod/common/component_templates"), {"EEP_SYNTHETIC_GUARD"})
        report = {**self.report, "planet_killer_numeric_sources": self.numeric_sources()}
        release.validate_static_report(report, self.root)
        self.write("mod/common/component_templates/synthetic.txt", (component + ignored +
            self.weapon("SECOND_SYNTHETIC", quoted_type=True)).encode())
        self.write("mod/common/on_actions/synthetic.txt", (self.callbacks("EEP_SYNTHETIC_GUARD") + self.callbacks("SECOND_SYNTHETIC")).encode())
        report = {**self.report, "planet_killer_components": 2,
                  "planet_killer_callbacks_required": 6, "planet_killer_callbacks_resolved": 6,
                  "planet_killer_numeric_components": 2, "planet_killer_numeric_resolved": 2,
                  "planet_killer_numeric_sources": self.numeric_sources(("EEP_SYNTHETIC_GUARD", "SECOND_SYNTHETIC"))}
        release.validate_static_report(report, self.root)
        for field, value in (("planet_killer_components", 1), ("planet_killer_callbacks_required", 3),
                             ("planet_killer_callbacks_resolved", 3)):
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, "planet-killer callback contract"):
                release.validate_static_report({**report, field: value}, self.root)

    def test_weapon_csv_report_must_cover_actual_files_and_component_keys(self):
        self.write("mod/common/component_templates/weapon_components.csv", b"key;cost;end\nEEP_SYNTHETIC_GUARD;0;\n")
        report = {**self.report, "weapon_csv_files": 1, "weapon_csv_keys": 1, "weapon_csv_applicability": "checked"}
        for field, value in (("weapon_csv_files", 0), ("weapon_csv_keys", 0),
                             ("weapon_csv_files", 2), ("weapon_csv_keys", 2),
                             ("weapon_csv_files", True), ("weapon_csv_keys", True),
                             ("weapon_csv_applicability", "not_applicable_no_weapon_csv_files")):
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "weapon CSV"):
                release.validate_static_report({**report, field: value}, self.root)
        for field in ("weapon_csv_files", "weapon_csv_keys", "weapon_csv_applicability"):
            missing = {key: value for key, value in report.items() if key != field}
            with self.subTest(missing=field), self.assertRaisesRegex(RuntimeError, "weapon CSV"):
                release.validate_static_report(missing, self.root)
        self.write("mod/common/component_templates/weapon_components.csv", b"key;cost;end\nEEP_SYNTHETIC_GUARD;0;\nEEP_SYNTHETIC_GUARD;0;\n")
        with self.assertRaisesRegex(RuntimeError, "component keys"):
            release.validate_static_report(report, self.root)

    def test_inline_numeric_contract_accepts_59_file_csv_free_package(self):
        self.assertEqual(len(release.update.base.manifest(self.root / "mod")), 59)
        self.assertEqual(self.report["weapon_csv_files"], 0)
        self.assertEqual(self.report["planet_killer_numeric_sources"][0]["values"],
                         {"windup_min": 90.0, "windup_max": 90.0, "total_fire_time": 30.0, "power": 0.0})
        release.validate_static_report(self.report, self.root)

    def test_numeric_contract_rejects_legacy_missing_wrong_or_unresolved_fields(self):
        fields = ("planet_killer_numeric_contract", "planet_killer_numeric_components", "planet_killer_numeric_resolved",
                  "planet_killer_numeric_applicability", "planet_killer_numeric_sources")
        for field in fields:
            bad = {key: value for key, value in self.report.items() if key != field}
            with self.subTest(missing=field), self.assertRaisesRegex(RuntimeError, "numeric"):
                release.validate_static_report(bad, self.root)
        for field, value in (("planet_killer_numeric_contract", "csv_syntax_only_v0"),
                             ("planet_killer_numeric_components", True), ("planet_killer_numeric_components", 0),
                             ("planet_killer_numeric_components", 2), ("planet_killer_numeric_resolved", True),
                             ("planet_killer_numeric_resolved", -1), ("planet_killer_numeric_resolved", 0),
                             ("planet_killer_numeric_resolved", 1.0),
                             ("planet_killer_numeric_applicability", "not_applicable_no_planet_killer_components"),
                             ("planet_killer_numeric_sources", []), ("planet_killer_numeric_sources", None)):
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "numeric"):
                release.validate_static_report({**self.report, field: value}, self.root)

    def test_numeric_sources_require_actual_keys_finite_values_and_source_identity(self):
        for field, value in (("key", "UNKNOWN"), ("key", []), ("kind", "arbitrary_csv"), ("line", True),
                             ("line", 0), ("sha256", "A" * 64), ("path", "relative/synthetic.txt"),
                             ("path", str(self.root / "mod/common/component_templates/wrong.txt")),
                             ("values", {}), ("values", {"windup_min": 90})):
            bad = copy.deepcopy(self.report)
            bad["planet_killer_numeric_sources"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "numeric|TXT source"):
                release.validate_static_report(bad, self.root)
        for key, value in (("power", True), ("power", float("nan")), ("power", float("inf")),
                           ("windup_min", -1), ("windup_max", -1), ("total_fire_time", -1)):
            bad = copy.deepcopy(self.report)
            bad["planet_killer_numeric_sources"][0]["values"][key] = value
            with self.subTest(key=key, value=value), self.assertRaisesRegex(RuntimeError, "finite literal"):
                release.validate_static_report(bad, self.root)

    def test_numeric_sentinel_power_and_copied_source_directory_are_supported(self):
        raw = self.weapon("EEP_SYNTHETIC_GUARD").replace("max = 90", "max = 0").replace("power = 0", "power = -1").encode()
        self.write("mod/common/component_templates/synthetic.txt", raw)
        sources = self.numeric_sources()
        sources[0]["values"].update(windup_max=0.0, power=-1.0)
        copied = self.write("prior-build/common/component_templates/synthetic.txt", raw)
        sources[0]["path"] = str(copied.resolve())
        report = {**self.report, "planet_killer_numeric_sources": sources}
        release.validate_static_report(report, self.root)
        self.write("mod/common/component_templates/synthetic.txt", raw + b"# changed after check\n")
        with self.assertRaisesRegex(RuntimeError, "source bytes differ"):
            release.validate_static_report(report, self.root)

    def test_fixed_csv_can_include_native_keys_without_mod_txt_redeclarations(self):
        name = "mod/common/component_templates/weapon_components.csv"
        self.write(name, b"key;windup_min;windup_max;cooldown;power;end\nPLANET_KILLER_CRACKER;1;1;10;5;\nEEP_SYNTHETIC_GUARD;90;90;30;0;\n")
        sources = self.numeric_sources(name=name, kind="mod_fixed_csv")
        sources[0]["line"] = 3
        report = {**self.report, "weapon_csv_files": 1, "weapon_csv_keys": 2,
                  "weapon_csv_applicability": "checked", "planet_killer_numeric_sources": sources}
        release.validate_static_report(report, self.root)
        self.write(name, (self.root / name).read_bytes() + b"PLANET_KILLER_SHIELDER;1;1;10;5;\n")
        with self.assertRaisesRegex(RuntimeError, "weapon CSV|source bytes"):
            release.validate_static_report(report, self.root)

    def test_native_fixed_csv_source_need_not_belong_to_mod(self):
        name = "base/common/component_templates/mutation_weapon_components.csv"
        self.write(name, b"key;windup_min;windup_max;cooldown;power;end\nEEP_SYNTHETIC_GUARD;90;90;30;0;\n")
        report = {**self.report, "planet_killer_numeric_sources": self.numeric_sources(name=name, kind="native_fixed_csv")}
        release.validate_static_report(report, self.root)
        report["planet_killer_numeric_sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "source bytes differ"):
            release.validate_static_report(report, self.root)

    def test_loader_contract_rejects_arbitrary_csv_and_legacy_reports(self):
        for field in ("weapon_csv_loader_contract", "weapon_csv_unsupported_files"):
            bad = {key: value for key, value in self.report.items() if key != field}
            with self.subTest(missing=field), self.assertRaisesRegex(RuntimeError, "CSV loader contract"):
                release.validate_static_report(bad, self.root)
        for field, value in (("weapon_csv_loader_contract", "glob_any_csv_v0"),
                             ("weapon_csv_unsupported_files", True), ("weapon_csv_unsupported_files", 1)):
            with self.subTest(field=field, value=value), self.assertRaisesRegex(RuntimeError, "CSV loader contract"):
                release.validate_static_report({**self.report, field: value}, self.root)
        self.write("mod/common/component_templates/arbitrary.csv", b"key;cost;end\nEEP_SYNTHETIC_GUARD;0;\n")
        for count in (0, 1):
            with self.subTest(unsupported=count), self.assertRaisesRegex(RuntimeError, "CSV loader contract"):
                release.validate_static_report({**self.report, "weapon_csv_files": 1, "weapon_csv_keys": 1,
                    "weapon_csv_applicability": "checked", "weapon_csv_unsupported_files": count}, self.root)

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


class MigrationV2ReleaseGuards(unittest.TestCase):
    """Report-shape fixtures with synthetic bytes; no native results are created."""

    originals = {
        "public031": ("rc6-public031-migration-v2-complete-report-v1.json",
            "bff7b26f3ebc089f1f863aca341f94fc5688a5bb0c9ea145ab504832a6d33c7e"),
        "paid11": ("rc6-paid11-migration-v2-cli-report-v1.json",
            "d85667777cdd77940067baa0fcf3ffe55d357a6d6fd040660f9ff023bf315ec7")}

    def setUp(self):
        import check_migration_1019 as migration
        self.migration = migration
        self.project = Path(__file__).resolve().parents[1]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.case = {"checks": {"damage_preserved": False,
            "damage_within_predeclared_v2_budget": True}, "evidence": [], "run_ids": ["synthetic-rc6"]}
        self.run_proofs = {"synthetic-rc6": "e" * 64}
        self.target_tree = migration.TREE
        scope = self.case["migration_contract"] = {
            "schema": "eep.1019.migration-release-scope.v2", "execution_mode": migration.MODE,
            "classification": release.MIGRATION_V2_CLASSIFICATION,
            "policy": dict(release.MIGRATION_V2_POLICY), "limitations": list(release.MIGRATION_V2_LIMITS),
            "fixtures": {}}
        archived = self.project / "docs/evidence/1019-rc6-migration-checkpoint-v1/source-tools/eat_everything_origin/tools/check_migration_1019.py"
        self.assertEqual(release.update.digest(archived.read_bytes()), release.MIGRATION_V2_LEGACY_CHECKER)
        scope["checker"] = self.bind("proofs/legacy-migration-checker.py", archived.read_bytes(), "analysis")
        name = "docs/native-migration-roundoff-contract-1019.md"
        scope["contract_document"] = self.bind(name, (self.project / name).read_bytes(), "analysis")
        name = "mod/common/global_ship_designs/eep_mothership.txt"
        self.write(name, (self.project / name).read_bytes())
        self.reports, self.sources = {}, {}
        known = copy.deepcopy(migration.FIXTURES)
        for kind, (filename, original_sha) in self.originals.items():
            raw = (self.project / "docs/evidence/1019-analysis" / filename).read_bytes()
            self.assertEqual(release.update.digest(raw), original_sha)
            report = json.loads(raw)
            source = copy.deepcopy(report["case"])
            bundle = scope["fixtures"][kind] = {"native_saves": {}, "audits": {},
                "save_receipts": {}, "load_receipts": {}}
            roles = {**report["provenance"], **{"repeat_" + k: v["provenance"]
                     for k, v in report["repeat_native_sources"].items()}}
            natives = {**report["native_sources"], **{"repeat_" + k: v["native"]
                       for k, v in report["repeat_native_sources"].items()}}
            for role, proof in roles.items():
                prefix = "synthetic/" + kind + "-" + role
                save = self.bind(prefix + ".sav", ("SYNTHETIC NOT NATIVE: " + prefix).encode(), "native_save")
                audit = self.bind(prefix + ".audit.json", b'{"synthetic":true}\n', "analysis")
                receipt = self.bind_json(prefix + ".receipt.json", {"synthetic": True,
                    "sha256": save["sha256"]}, "actions")
                bundle["native_saves"][role] = save
                bundle["audits"][role] = audit
                bundle["save_receipts"][role] = [receipt]
                proof.update(save_sha256=save["sha256"], audit_sha256=audit["sha256"],
                             receipts=[{"sha256": receipt["sha256"]}])
                if role not in ("fixture", "before"):
                    proof.update(run_id="synthetic-rc6", manifest_sha256="e" * 64)
            for role in ("fixture", "before"):
                known[kind][role + "_sha256"] = roles[role]["save_sha256"]
                source[role + "_sha256"] = roles[role]["save_sha256"]
            for role, input_role in (("after", "before"), ("reload", "after"),
                                    *(([("repeat_before", "after")]) if source.get("repeat_load_source") else [])):
                proof = natives[role]["load_evidence"]
                raw = copy.deepcopy(proof["raw"])
                raw["source_sha256"] = roles[input_role]["save_sha256"]
                ref = self.bind_json("synthetic/" + kind + "-" + role + ".load.json", raw, "actions")
                proof.update(sha256=ref["sha256"], raw=raw,
                    source_byte_sha256=raw["source_sha256"], expected_source_sha256=raw["source_sha256"])
                bundle["load_receipts"][role] = ref
            bundle["repeat_action"] = self.bind_json("synthetic/" + kind + "-repeat.action.json", {
                "text": "effect root={eep_repair_existing_mothership_design=yes eep_repair_existing_mothership_design=yes}",
                "submitted": True, "submit_input": "physical scan code 0x1c"}, "actions")
            self.sources[kind], self.reports[kind] = source, report
            self.refresh(kind)
        self.fixture_patch = patch.object(migration, "FIXTURES", known)
        self.fixture_patch.start()
        self.addCleanup(self.fixture_patch.stop)

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path

    def bind(self, name, raw, kind):
        self.write(name, raw)
        ref = {"path": name, "sha256": release.update.digest(raw), "kind": kind}
        self.case["evidence"] = [row for row in self.case["evidence"] if row["path"] != name] + [ref]
        return ref

    def bind_json(self, name, data, kind):
        return self.bind(name, (json.dumps(data, ensure_ascii=False) + "\n").encode(), kind)

    def refresh(self, kind):
        bundle = self.case["migration_contract"]["fixtures"][kind]
        bundle["case"] = self.bind_json("synthetic/" + kind + "-case.json", self.sources[kind], "analysis")
        self.reports[kind].update(case=copy.deepcopy(self.sources[kind]), case_sha256=bundle["case"]["sha256"])
        bundle["report"] = self.bind_json("synthetic/" + kind + "-report.json", self.reports[kind], "analysis")

    def validate(self):
        release.validate_migration_contract(self.case, self.target_tree, self.root, self.run_proofs)

    def use_current_producer(self, tree):
        """Change only synthetic report shapes, never archived native evidence."""
        self.target_tree = tree
        scope = self.case["migration_contract"]
        name = "tools/check_migration_1019.py"
        scope["checker"] = self.bind(name, (self.project / name).read_bytes(), "analysis")
        name = "docs/evidence/1020-migration-rc7-source/source-certificate-v1.json"
        raw = (self.project / name).read_bytes()
        scope["source_certificate"] = self.bind(name, raw, "analysis")
        certificate = json.loads(raw)
        revision = certificate["revisions"][tree]
        identity = {"schema": "eep.migration.candidate_source_identity.v1", "tree_sha256": tree,
            "version": revision["version"], "file_count": 59, "files": revision["files"],
            "copied_mod": str(self.root / "synthetic-not-native"),
            "source_certificate": {"path": str((self.project / name).resolve()),
                                   "sha256": release.MIGRATION_SOURCE_CERTIFICATE},
            "shared_migration_sources": certificate["shared_migration_sources"]}
        for kind, report in self.reports.items():
            self.sources[kind]["candidate_tree_sha256"] = tree
            report.update(checker_sha256=release.MIGRATION_V2_CHECKER,
                          candidate_source_identity=copy.deepcopy(identity))
            roles = {key: report["provenance"][key] for key in ("after", "reload")}
            roles.update({"repeat_" + key: row["provenance"]
                          for key, row in report["repeat_native_sources"].items()})
            natives = {key: report["native_sources"][key] for key in ("after", "reload")}
            natives.update({"repeat_" + key: row["native"]
                            for key, row in report["repeat_native_sources"].items()})
            for role, proof in roles.items():
                proof.update(production_tree_sha256=tree, version=revision["version"])
                natives[role]["candidate_source_identity"] = copy.deepcopy(identity)
            self.refresh(kind)

    def test_separate_v2_scope_accepts_report_shapes_and_keeps_real_v1_failure(self):
        self.validate()
        self.assertIs(self.case["checks"]["damage_preserved"], False)
        for filename, sha in self.originals.values():
            raw = (self.project / "docs/evidence/1019-analysis" / filename).read_bytes()
            self.assertEqual(release.update.digest(raw), sha)
            self.assertEqual(json.loads(raw)["v1_original_diagnostic"]["status"], "FAIL")
            self.assertIs(json.loads(raw)["v1_original_diagnostic"]["checks"]["damage_preserved_in_declared_mode"], False)

    def test_unknown_scope_policy_or_missing_independent_fixture_rejected(self):
        scope = self.case["migration_contract"]
        for key, value in (("schema", "unknown"), ("execution_mode", "multiplayer"),
                           ("classification", "lossless"),
                           ("policy", {**scope["policy"], "step_signed_ratio_min": -.000022}),
                           ("limitations", []), ("fixtures", {"public031": scope["fixtures"]["public031"]})):
            old = scope[key]
            scope[key] = value
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                self.validate()
            scope[key] = old
        for field in ("damage_preserved", "damage_within_predeclared_v2_budget"):
            old = self.case["checks"][field]
            self.case["checks"][field] = not old
            with self.subTest(check=field), self.assertRaises(RuntimeError):
                self.validate()
            self.case["checks"][field] = old

    def test_report_forgery_missing_raw_source_or_nonprecision_failure_rejected(self):
        original = copy.deepcopy(self.reports["public031"])
        edits = {
            "claimed_v1_pass": lambda r: r["v1_original_diagnostic"].update(status="PASS_SCOPED"),
            "strict_damage_true": lambda r: r["v1_original_diagnostic"]["checks"].update(damage_preserved_in_declared_mode=True),
            "missing_check": lambda r: r["checks"].pop(next(iter(r["checks"]))),
            "failed_check": lambda r: r["checks"].update({next(iter(r["checks"])): False}),
            "wrong_checker": lambda r: r.update(checker_sha256="0" * 64),
            "wrong_run": lambda r: r["provenance"]["after"].update(run_id="historical-run"),
            "wrong_manifest": lambda r: r["provenance"]["after"].update(manifest_sha256="0" * 64),
            "wrong_tree": lambda r: r["provenance"]["after"].update(production_tree_sha256="0" * 64),
            "wrong_exe": lambda r: r["native_sources"]["after"].update(actual_game_exe_sha256="0" * 64),
            "multiplayer": lambda r: r["native_sources"]["after"].update(players=[{"country": 0}, {"country": 1}]),
            "wrong_actual_design": lambda r: r["snapshots"]["after"].update(design_shape={}),
            "queue_changed": lambda r: r["snapshots"]["after"].update(all_owned_queue_items={"synthetic": "changed"}),
            "wrong_maximum": lambda r: r["snapshots"]["after"]["damage"]["shield"].update(maximum=167311),
            "missing_readings": lambda r: r["steps"]["old_to_after"].pop("raw_readings"),
            "fabricated_delta": lambda r: r["steps"]["old_to_after"]["signed_ratio_deltas_decimal"].update(armor="0"),
            "lost_strict_diagnostic": lambda r: r["steps"]["old_to_after"]["original_1e_6_diagnostic"].update(armor=True),
            "larger_step_budget": lambda r: r["steps"]["old_to_after"].update(minimum_delta=-.000022),
            "nonidempotent_repeat": lambda r: r["repeat_sync_strict_comparison"].update(differences=[{"synthetic": True}]),
            "no_actual_mobilebase_record": lambda r: r["native_sources"]["after"].pop("attached_starbase_raw"),
        }
        for label, edit in edits.items():
            self.reports["public031"] = copy.deepcopy(original)
            edit(self.reports["public031"])
            self.refresh("public031")
            with self.subTest(label=label), self.assertRaises(RuntimeError):
                self.validate()

    def test_native_roles_receipts_and_case_bound_evidence_required(self):
        bundle = self.case["migration_contract"]["fixtures"]["paid11"]
        for field, key in (("native_saves", "reload"), ("audits", "before"),
                           ("save_receipts", "after"), ("load_receipts", "reload")):
            old = bundle[field].pop(key)
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                self.validate()
            bundle[field][key] = old
        evidence = self.case["evidence"]
        self.case["evidence"] = [r for r in evidence if r != bundle["native_saves"]["after"]]
        with self.assertRaises(RuntimeError):
            self.validate()
        self.case["evidence"] = evidence
        self.write(bundle["repeat_action"]["path"], b'{"submitted":false}')
        with self.assertRaises(RuntimeError):
            self.validate()

    def test_recomputed_raw_loss_or_gain_cannot_exceed_predeclared_step_budget(self):
        from decimal import Decimal
        original = copy.deepcopy(self.reports["public031"])
        for shift in (Decimal("-.001"), Decimal(".001")):
            report = self.reports["public031"] = copy.deepcopy(original)
            step = report["steps"]["old_to_after"]
            before = step["raw_readings"]["before"]["armor"]
            after = step["raw_readings"]["after"]["armor"]
            old_ratio = Decimal(str(before["current"])) / Decimal(str(before["maximum"]))
            current = (old_ratio + shift) * Decimal(str(after["maximum"]))
            ratio = current / Decimal(str(after["maximum"]))
            after.update(current=str(current), fraction_decimal=str(ratio))
            report["snapshots"]["after"]["damage"]["armor"]["current_absolute"] = str(current)
            step["signed_ratio_deltas_decimal"]["armor"] = str(ratio - old_ratio)
            step["original_1e_6_diagnostic"]["armor"] = False
            self.refresh("public031")
            with self.subTest(shift=str(shift)), self.assertRaisesRegex(RuntimeError, "recomputed per-step budget"):
                self.validate()

    def test_boolean_native_count_and_wrong_candidate_tree_rejected(self):
        self.sources["public031"]["expected_queued_items"] = False
        self.refresh("public031")
        with self.assertRaisesRegex(RuntimeError, "nonboolean"):
            self.validate()
        self.sources["public031"]["expected_queued_items"] = 0
        self.refresh("public031")
        with self.assertRaisesRegex(RuntimeError, "explicit known-revision"):
            release.validate_migration_contract(self.case, "0" * 64, self.root, self.run_proofs)

    def test_current_producer_accepts_exact_registered_rc6_and_rc7_shapes(self):
        self.assertEqual(release.MIGRATION_SOURCE_VERSIONS, {
            self.migration.TREE: "0.4.0-rc.6", self.migration.RC7_TREE: "0.4.0-rc.7"})
        self.assertEqual(release.MIGRATION_V2_CHECKER,
                         release.update.digest(Path(self.migration.__file__).read_bytes()))
        for tree in (self.migration.TREE, self.migration.RC7_TREE):
            with self.subTest(tree=tree):
                self.use_current_producer(tree)
                self.validate()
                for report in self.reports.values():
                    self.assertEqual(report["v1_original_diagnostic"]["status"], "FAIL")
                    self.assertIs(report["v1_original_diagnostic"]["checks"]["damage_preserved_in_declared_mode"], False)

    def test_rc7_rejects_mixed_candidate_roles_and_source_identity(self):
        self.use_current_producer(self.migration.RC7_TREE)
        original = copy.deepcopy(self.reports["public031"])
        edits = {
            "old_role_tree": lambda r: r["provenance"]["after"].update(production_tree_sha256=self.migration.TREE),
            "old_role_version": lambda r: r["provenance"]["reload"].update(version="0.4.0-rc.6"),
            "old_repeat_tree": lambda r: r["repeat_native_sources"]["after"]["provenance"].update(production_tree_sha256=self.migration.TREE),
            "missing_report_identity": lambda r: r.pop("candidate_source_identity"),
            "missing_native_identity": lambda r: r["native_sources"]["after"].pop("candidate_source_identity"),
            "mixed_native_identity": lambda r: r["repeat_native_sources"]["before"]["native"]["candidate_source_identity"].update(tree_sha256=self.migration.TREE),
            "unknown_file_bytes": lambda r: r["candidate_source_identity"]["files"][0].update(sha256="0" * 64),
            "missing_file": lambda r: r["candidate_source_identity"]["files"].pop(),
            "boolean_file_count": lambda r: r["candidate_source_identity"].update(file_count=True),
            "unknown_shared_source": lambda r: r["candidate_source_identity"]["shared_migration_sources"]["design"].update(sha256="0" * 64),
            "unknown_certificate": lambda r: r["native_sources"]["reload"]["candidate_source_identity"]["source_certificate"].update(sha256="0" * 64),
            "legacy_producer_claim": lambda r: r.update(checker_sha256=release.MIGRATION_V2_LEGACY_CHECKER),
        }
        for label, edit in edits.items():
            self.reports["public031"] = copy.deepcopy(original)
            edit(self.reports["public031"])
            self.refresh("public031")
            with self.subTest(label=label), self.assertRaises(RuntimeError):
                self.validate()

    def test_rc7_rejects_unknown_producer_or_certificate_and_old_case_revision(self):
        self.use_current_producer(self.migration.RC7_TREE)
        scope = self.case["migration_contract"]
        certificate_ref = scope.pop("source_certificate")
        with self.assertRaises(RuntimeError):
            self.validate()
        scope["source_certificate"] = certificate_ref
        checker = scope["checker"]
        scope["checker"] = self.bind("proofs/unknown-checker.py", b"synthetic unknown checker", "analysis")
        with self.assertRaisesRegex(RuntimeError, "reviewed v2 checker bytes"):
            self.validate()
        scope["checker"] = self.bind("proofs/legacy-migration-checker.py",
            (self.root / "proofs/legacy-migration-checker.py").read_bytes(), "analysis")
        with self.assertRaisesRegex(RuntimeError, "reviewed v2 checker bytes"):
            self.validate()
        scope["checker"] = checker
        self.sources["public031"]["candidate_tree_sha256"] = self.migration.TREE
        self.refresh("public031")
        with self.assertRaisesRegex(RuntimeError, "case revision"):
            self.validate()
        self.sources["public031"]["candidate_tree_sha256"] = self.migration.RC7_TREE
        self.refresh("public031")
        modified = json.loads((self.root / certificate_ref["path"]).read_bytes())
        modified["revisions"][self.migration.RC7_TREE]["files"][0]["sha256"] = "0" * 64
        scope["source_certificate"] = self.bind_json(certificate_ref["path"], modified, "analysis")
        with self.assertRaisesRegex(RuntimeError, "exact reviewed source certificate"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
