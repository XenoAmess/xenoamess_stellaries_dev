"""Development-only oracle/counterexamples; these are never native acceptance."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import weakref
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("additive_matrix_test_subject", ROOT / "tools/audit_additive_runtime_matrix.py")
matrix = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = matrix
SPEC.loader.exec_module(matrix)
D = matrix.D
PROFILE = {"status": "PASS", "unity_source_isolated": True,
           "planet_biologists_job_types": ["biologist", "shishan_code_maintainer"]}


def development_matrix(q="1.23"):
    """Compact observations with Q deliberately unequal to the draft's q=1."""
    result = {}
    for branch in matrix.BRANCHES:
        dummy = matrix.TRAITS.get(branch)
        traits = ["t" + str(n) for n in range(7)] + ([dummy] if dummy else [])
        u = D(len(traits))
        variables = {matrix.PREFIX + "repeat_count": "0", matrix.PREFIX + "trait_average": str(u),
                     matrix.PREFIX + "total": str(u), matrix.PREFIX + "bonus": str(u * D(".05")),
                     matrix.PREFIX + "multiplier": str(1 + u * D(".05")), "shishan_code_maintenance_count": "1"}
        modifiers = [{"modifier": matrix.ARCH, "multiplier": str(u), "days": "-1"}]
        if branch in ("F00", "F10"):
            modifiers.append({"modifier": matrix.COUNTER, "multiplier": str(u), "days": "-1"})
            variables["shishan_econ_probe_counter_t"] = str(u)
        a = D(".4") if branch in ("F10", "F11", "FP", "FN", "FH") else D(0)
        b = D(0) if branch in ("F00", "F10") else D(".05") * u
        if a:
            modifiers.append({"modifier": matrix.OTHER, "multiplier": "1", "days": "-1"})
        unity = D(q) * (D("1.6") + a + b) * D("1.1")
        society = D(q) * 3 * (D("1.6") + a + b) * D("1.76")
        jobs = []
        for index, name, workforce, bonus in ((1, "shishan_code_maintainer", "100", "10"), (2, "biologist", "60", "6")):
            jobs.append({"id": index, "colony_id": 0, "type": name, "workforce": workforce,
                         "bonus_workforce": bonus, "automated_workforce": "0", "max_workforce": workforce,
                         "workforce_limit": workforce, "automated_workforce_limit": str(D(workforce) - 1),
                         "allocations": [{"group_id": 1, "species_id": 48, "category": "specialist",
                                          "amount": workforce, "base_traits": ["t" + str(n) for n in range(7)]}]})
        period = {"income": {"planet_biologists": {"unity": str(unity), "society_research": str(society)},
                             "country_base": {"unity": "12.5", "energy": "25"}},
                  "expenses": {"planet_biologists": {"consumer_goods": "1.98"}}}
        snapshot = {"version": "Cygnus v4.5.2", "actor_id": 0, "mods": ["isolated"],
                    "origin": "origin_shishan_code", "variables": variables, "modifiers": modifiers,
                    "projects": [], "jobs": jobs, "context": {"stability": "72", "stage": "0"},
                    "population": {"population": 1000, "trait_average_decimal": str(u),
                        "populated_templates": [{"id": 48, "distinct_trait_keys": traits,
                                                  "distinct_trait_count": len(traits), "duplicate_trait_keys": []}]},
                    "strict_cache": {"status": "PASS", "checks": [], "comparisons": {}},
                    "budget": {"current_month": copy.deepcopy(period), "last_month": period}}
        result[branch] = {}
        for phase, date in zip(matrix.PHASES, ("2209.11.28", "2209.12.02", "2210.01.02")):
            result[branch][phase] = {**copy.deepcopy(snapshot), "date": date}
    return result


class ArithmeticTests(unittest.TestCase):
    def test_unknown_common_factor_is_derived_not_hardcoded(self):
        data = development_matrix("1.23")
        result = matrix.audit_matrix(data, PROFILE, common=copy.deepcopy(data["F01"]["input"]))
        self.assertEqual("PASS", result["status"])
        self.assertEqual(D("1.23"), D(result["limited_economy"]["unity"]["Q0"]))
        self.assertEqual(D("3.69"), D(result["limited_economy"]["society_secondary"]["Q0"]))

    def test_independent_interaction_is_rejected(self):
        snapshots = development_matrix()
        for branch in ("F01", "F11", "FP", "FN", "FH"):
            for phase in matrix.PHASES:
                s = snapshots[branch][phase]
                a = D(".4") if branch != "F01" else D(0)
                b = D(".4") if branch in matrix.TRAITS else D(".35")
                s["budget"]["last_month"]["income"]["planet_biologists"]["unity"] = str(D("1.23") * (D("1.6") + a) * (1 + b) * D("1.1"))
        result = matrix.audit_matrix(snapshots, PROFILE)
        self.assertEqual("FAIL", result["limited_economy"]["status"])
        checks = result["limited_economy"]["unity"]["checks"]
        self.assertTrue(any(c["code"] == "INTERACTION" and c["status"] == "FAIL" for c in checks))

    def test_wrong_counter_scale_is_rejected(self):
        data = development_matrix()
        next(m for m in data["F00"]["measured"]["modifiers"] if m["modifier"] == matrix.COUNTER)["multiplier"] = "6"
        result = matrix.audit_matrix(data, PROFILE)
        self.assertTrue(any(g["code"] == "CONTROL_MODIFIER" for g in result["limited_economy"]["guards"]))

    def test_raw_hidden_key_required_not_only_average(self):
        data = development_matrix()
        t = data["FH"]["measured"]["population"]["populated_templates"][0]
        t["distinct_trait_keys"][-1] = "unrelated_eighth_key"
        result = matrix.audit_matrix(data, PROFILE)
        self.assertTrue(any(g["code"] == "ACTUAL_TEMPLATE_INPUT" for g in result["limited_economy"]["guards"]))

    def test_repeat_and_architecture_scale_must_be_observed(self):
        for key in (matrix.PREFIX + "repeat_count", matrix.PREFIX + "total"):
            with self.subTest(key=key):
                data = development_matrix()
                data["FP"]["warm"]["variables"][key] = "9"
                result = matrix.audit_matrix(data, PROFILE)
                self.assertEqual("FAIL", result["limited_economy"]["status"])

    def test_employment_drift_invalidates_arithmetic_pass(self):
        data = development_matrix()
        data["F00"]["warm"]["jobs"][0]["bonus_workforce"] = "12"
        result = matrix.audit_matrix(data, PROFILE)
        self.assertEqual("INVALID", result["limited_economy"]["status"])
        self.assertEqual("PASS", result["limited_economy"]["unity"]["arithmetic_status"])

    def test_capacity_and_allocation_drift_are_observed(self):
        for field in ("max_workforce", "workforce_limit", "automated_workforce_limit"):
            data = development_matrix()
            data["F01"]["input"]["jobs"][0][field] = "101"
            self.assertEqual("INVALID", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_period_or_calendar_drift_invalidates(self):
        for phase, date in (("warm", "2209.12.20"), ("measured", "2209.12.03"), ("input", "2209.12.01")):
            with self.subTest(phase=phase):
                data = development_matrix()
                data["FN"][phase]["date"] = date
                self.assertEqual("INVALID", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_expiring_modifier_and_stability_change_invalid(self):
        data = development_matrix()
        data["F01"]["warm"]["modifiers"].append({"modifier": "game_start", "multiplier": "1", "days": "20"})
        self.assertEqual("INVALID", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])
        data = development_matrix()
        data["F00"]["warm"]["context"]["stability"] = "72.01"
        self.assertEqual("INVALID", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_common_warmup_can_settle_before_stable_measured_window(self):
        data = development_matrix()
        for rows in data.values():
            rows["input"]["context"]["stability"] = "71"
        self.assertEqual("PASS", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_absent_unity_never_defaults_to_zero(self):
        data = development_matrix()
        del data["F00"]["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["unity"]
        self.assertEqual("NOT COVERED", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_maintenance_and_nonjob_negative_controls_fail(self):
        for kind, category, resource in (("expenses", "planet_biologists", "consumer_goods"), ("income", "country_base", "unity")):
            with self.subTest(category=category):
                data = development_matrix()
                data["FP"]["measured"]["budget"]["last_month"][kind][category][resource] = "99"
                self.assertEqual("FAIL", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_missing_nonzero_negative_source_not_covered(self):
        data = development_matrix()
        for row in data.values():
            row["measured"]["budget"]["last_month"]["income"]["country_base"] = {"unity": "0"}
        self.assertEqual("NOT COVERED", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_pw_strict_failure_does_not_erase_fixed_u_economy(self):
        data = development_matrix()
        strict = data["F11"]["measured"]["strict_cache"]
        strict["checks"] = [matrix.issue("FAIL", "STRICT_CACHE_MISMATCH", key=matrix.PREFIX + "population")]
        strict["comparisons"][matrix.PREFIX + "population"] = {"status": "MISMATCH", "observed": "999", "expected": "1000"}
        result = matrix.audit_matrix(data, PROFILE)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual("FAIL", result["strict_cache_audit"]["status"])
        self.assertEqual("PASS", result["limited_economy"]["status"])

    def test_unresolved_source_or_automated_workforce_not_covered(self):
        self.assertEqual("NOT COVERED", matrix.audit_matrix(development_matrix(), {"status": "NOT COVERED"})["limited_economy"]["status"])
        data = development_matrix()
        for row in data.values():
            for snap in row.values():
                snap["jobs"][0]["automated_workforce"] = "1"
        self.assertEqual("NOT COVERED", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_missing_job_field_is_not_implicitly_zero(self):
        data = development_matrix()
        for row in data.values():
            for snap in row.values():
                snap["jobs"][0]["bonus_workforce"] = None
        self.assertEqual("NOT COVERED", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_clone_group_merge_keeps_semantically_equal_allocation(self):
        data = development_matrix()
        allocation = data["FP"]["measured"]["jobs"][0]["allocations"][0]
        allocation["amount"] = "60"
        data["FP"]["measured"]["jobs"][0]["allocations"].append({**copy.deepcopy(allocation), "group_id": 999, "species_id": 999, "amount": "40"})
        self.assertEqual("PASS", matrix.audit_matrix(data, PROFILE)["limited_economy"]["status"])

    def test_unreviewed_trait_profile_or_other_category_job_not_covered(self):
        profile = {**PROFILE, "permitted_base_trait_keys": ["a_different_seed"]}
        self.assertEqual("NOT COVERED", matrix.audit_matrix(development_matrix(), profile)["limited_economy"]["status"])
        profile = {**PROFILE, "planet_biologists_job_types": PROFILE["planet_biologists_job_types"] + ["third_party_unity_job"]}
        data = development_matrix()
        for row in data.values():
            for snapshot in row.values():
                job = copy.deepcopy(snapshot["jobs"][0])
                job.update(id=3, type="third_party_unity_job")
                snapshot["jobs"].append(job)
        self.assertEqual("NOT COVERED", matrix.audit_matrix(data, profile)["limited_economy"]["status"])

    def test_epsilon_is_fixed_before_observing_results(self):
        self.assertTrue(matrix.close(".1", ".10009"))
        self.assertFalse(matrix.close(".1", ".10011"))
        self.assertEqual(D("1"), matrix.epsilon("1000000"))


class SourceAndSecondaryGateTests(unittest.TestCase):
    def test_isolated_society_failure_blocks_limited_and_overall_pass(self):
        data = development_matrix()
        data["FP"]["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["society_research"] = "999"
        profile = {**PROFILE, "society_source_isolated": True}
        result = matrix.audit_matrix(data, profile, copy.deepcopy(data["F01"]["input"]))
        self.assertEqual("FAIL", result["limited_economy"]["society_secondary"]["arithmetic_status"])
        self.assertEqual("PASS", result["limited_economy"]["unity"]["arithmetic_status"])
        self.assertEqual("FAIL", result["limited_economy"]["status"])
        self.assertEqual("FAIL", result["status"])

    def test_missing_or_unisolated_secondary_is_explicit_not_covered(self):
        for isolated, missing in ((False, False), (True, True)):
            with self.subTest(isolated=isolated, missing=missing):
                data = development_matrix()
                if missing:
                    del data["FP"]["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["society_research"]
                else:
                    data["FP"]["measured"]["budget"]["last_month"]["income"]["planet_biologists"]["society_research"] = "999"
                result = matrix.audit_matrix(data, {**PROFILE, "society_source_isolated": isolated}, copy.deepcopy(data["F01"]["input"]))
                self.assertEqual("NOT COVERED", result["limited_economy"]["society_secondary"]["status"])
                self.assertEqual("PASS", result["limited_economy"]["unity"]["status"])
                self.assertEqual("PASS", result["limited_economy"]["status"])

    @staticmethod
    def with_extra_category_job(channel, amount):
        data = development_matrix()
        profile = {**PROFILE, "planet_biologists_job_types": PROFILE["planet_biologists_job_types"] + ["unreviewed_category_job"]}
        for rows in data.values():
            for snapshot in rows.values():
                job = copy.deepcopy(snapshot["jobs"][0])
                job.update(id=9, type="unreviewed_category_job", workforce="0", bonus_workforce="0", automated_workforce="0")
                job[channel] = amount
                job["allocations"] = []
                snapshot["jobs"].append(job)
        return data, profile

    def test_extra_category_only_bonus_or_automation_cannot_hide_behind_zero_base(self):
        for channel in ("bonus_workforce", "automated_workforce"):
            with self.subTest(channel=channel):
                data, profile = self.with_extra_category_job(channel, "100")
                result = matrix.audit_matrix(data, profile, copy.deepcopy(data["F01"]["input"]))
                self.assertEqual("NOT COVERED", result["limited_economy"]["status"])
                self.assertEqual("NOT COVERED", result["status"])
                isolation = [g for g in result["limited_economy"]["guards"] if g["code"] == "UNITY_SOURCE_NOT_ISOLATED"]
                self.assertTrue(isolation)
                self.assertIn("unreviewed_category_job", isolation[0]["other_category_jobs"])

    def test_unknown_extra_category_workforce_channel_fails_closed(self):
        for channel in ("workforce", "bonus_workforce", "automated_workforce"):
            for value in (None, "unserialized"):
                with self.subTest(channel=channel, value=value):
                    data, profile = self.with_extra_category_job(channel, value)
                    result = matrix.audit_matrix(data, profile, copy.deepcopy(data["F01"]["input"]))
                    self.assertEqual("NOT COVERED", result["limited_economy"]["status"])
                    self.assertTrue(any(g["code"] == "CATEGORY_WORKFORCE_CHANNEL_UNKNOWN" for g in result["limited_economy"]["guards"]))


class EmploymentBoundaryTests(unittest.TestCase):
    @staticmethod
    def natural_growth():
        data = development_matrix()
        for rows in data.values():
            for phase, amount in zip(matrix.PHASES, ("2390", "2396", "2402")):
                job = copy.deepcopy(rows[phase]["jobs"][0])
                job.update(id=3, type="civilian", workforce=amount, bonus_workforce=str(D(amount) / 10),
                           automated_workforce="-1", max_workforce="-1", workforce_limit="-1", automated_workforce_limit="-1")
                job["allocations"][0].update(category="civilian", amount=amount)
                rows[phase]["jobs"].append(job)
        return data

    def test_other_jobs_can_grow_naturally_in_common_across_months(self):
        data = self.natural_growth()
        result = matrix.audit_matrix(data, PROFILE, common=copy.deepcopy(data["F01"]["input"]))
        self.assertEqual("PASS", result["status"])
        self.assertEqual("PASS", result["limited_economy"]["status"])
        self.assertEqual("PASS", result["setup_input_audit"]["status"])

    def test_other_job_same_phase_branch_difference_is_invalid(self):
        data = self.natural_growth()
        data["FP"]["warm"]["jobs"][-1]["workforce"] = "2397"
        result = matrix.audit_matrix(data, PROFILE)
        self.assertEqual("INVALID", result["limited_economy"]["status"])
        self.assertTrue(any(g["code"] == "OTHER_DOMESTIC_EMPLOYMENT_CHANGED" for g in result["limited_economy"]["guards"]))

    def test_measured_biologist_workforce_change_across_months_is_invalid(self):
        data = self.natural_growth()
        for rows in data.values():
            rows["warm"]["jobs"][1]["workforce"] = "61"
            rows["warm"]["jobs"][1]["allocations"][0]["amount"] = "61"
        result = matrix.audit_matrix(data, PROFILE)
        self.assertEqual("INVALID", result["limited_economy"]["status"])
        self.assertTrue(any(g["code"] == "EMPLOYMENT_OR_CAPACITY_CHANGED" for g in result["limited_economy"]["guards"]))

    def test_unknown_same_category_job_also_requires_cross_month_stability(self):
        data = self.natural_growth()
        profile = {**PROFILE, "planet_biologists_job_types": PROFILE["planet_biologists_job_types"] + ["unknown_category_job"]}
        for rows in data.values():
            for phase in matrix.PHASES:
                job = copy.deepcopy(rows[phase]["jobs"][1])
                job.update(id=4, type="unknown_category_job")
                rows[phase]["jobs"].append(job)
            rows["warm"]["jobs"][-1]["bonus_workforce"] = "7"
        result = matrix.audit_matrix(data, profile)
        self.assertEqual("INVALID", result["limited_economy"]["status"])
        self.assertTrue(any(g["code"] == "EMPLOYMENT_OR_CAPACITY_CHANGED" for g in result["limited_economy"]["guards"]))

    def test_absent_source_s_keeps_setup_not_covered_separate(self):
        result = matrix.audit_matrix(self.natural_growth(), PROFILE)
        self.assertEqual("PASS", result["limited_economy"]["status"])
        self.assertEqual("NOT COVERED", result["setup_input_audit"]["status"])
        self.assertEqual("NOT COVERED", result["status"])

    def test_common_source_detects_shared_setup_employment_change(self):
        data = self.natural_growth()
        common = copy.deepcopy(data["F01"]["input"])
        common["jobs"][-1]["workforce"] = "2389"
        result = matrix.audit_matrix(data, PROFILE, common)
        self.assertEqual("PASS", result["limited_economy"]["status"])
        self.assertEqual("INVALID", result["setup_input_audit"]["status"])
        self.assertEqual("INVALID", result["status"])
        self.assertTrue(all(c["code"] == "SETUP_EMPLOYMENT_OR_CAPACITY_CHANGED" for c in result["setup_input_audit"]["checks"]))

    def test_common_source_must_be_same_day_and_same_identity(self):
        data = self.natural_growth()
        for key, value, code in (("date", "2209.11.27", "COMMON_SOURCE_CALENDAR_MISMATCH"),
                                 ("actor_id", 9, "COMMON_SOURCE_IDENTITY_MISMATCH")):
            with self.subTest(key=key):
                common = copy.deepcopy(data["F01"]["input"])
                common[key] = value
                result = matrix.audit_matrix(data, PROFILE, common)
                self.assertEqual("INVALID", result["setup_input_audit"]["status"])
                self.assertTrue(all(c["code"] == code for c in result["setup_input_audit"]["checks"]))


DEVELOPMENT_NATIVE = '''version="Cygnus v4.5.2" date="2209.11.28"
player={{country=3}}
species_db={10={traits={trait=t0 trait=t1 trait=t2 trait=t3 trait=t4 trait=t5 trait=t6}}}
country={3={founder_species_ref=10 owned_planets={0}
 government={origin=origin_shishan_code} variables={} flags={}
 budget={current_month={income={country_base={unity=12.5}} expenses={}}
 last_month={income={planet_biologists={unity=2 society_research=9} country_base={unity=12.5}}
 expenses={planet_biologists={consumer_goods=1.98}}}}
}}
colony={0={carrier={type=planet reference=8} pop_groups={1} stability=72 final_designation=col_capital}}
planets={planet={8={colony=0 owner=3}}}
pop_groups={1={planet=0 key={species=10 category=specialist} size=1000}}
pop_jobs={1={planet=0 type=shishan_code_maintainer workforce=100 bonus_workforce=10
 automated_workforce=0 max_workforce=100 workforce_limit=100 automated_workforce_limit=99
 pop_groups={{pop_group=1 amount=100}}}}
situations={situations={}}
'''


def write_development_zip(path, game_text=DEVELOPMENT_NATIVE):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("meta", 'version="Cygnus v4.5.2" date="2209.11.28" mods={"development_only"}')
        archive.writestr("gamestate", game_text)


class NativeBoundaryTests(unittest.TestCase):
    def test_carrier_modifier_context_observes_identity_and_scale_without_days(self):
        def snapshot(base, name, modifier, multiplier, days):
            planet = "8={colony=0 owner=3 timed_modifier={items={{modifier=" + modifier + " multiplier=" + multiplier + " days=" + days + "}}}}"
            game_text = DEVELOPMENT_NATIVE.replace("8={colony=0 owner=3}", planet)
            path = base / name
            write_development_zip(path, game_text)
            return matrix.extract_snapshot(path)

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = snapshot(base, "first.sav", "shishan_econ_probe_stability_control", "1", "5")
            elapsed = snapshot(base, "elapsed.sav", "shishan_econ_probe_stability_control", "1", "4")
            renamed = snapshot(base, "renamed.sav", "different_carrier_modifier", "1", "4")
            rescaled = snapshot(base, "rescaled.sav", "shishan_econ_probe_stability_control", "2", "4")
        self.assertEqual([{"modifier": "shishan_econ_probe_stability_control", "multiplier": "1"}],
                         first["context"]["colonies"][0]["carrier_modifiers"])
        self.assertTrue(matrix.equivalent(first["context"], elapsed["context"]))
        self.assertFalse(matrix.equivalent(first["context"], renamed["context"]))
        self.assertFalse(matrix.equivalent(first["context"], rescaled["context"]))

    def test_development_zip_uses_native_population_job_and_budget_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "development.sav"
            write_development_zip(path)
            snapshot = matrix.extract_snapshot(path)
        self.assertEqual(3, snapshot["actor_id"])
        self.assertEqual(1000, snapshot["population"]["population"])
        self.assertEqual(7, snapshot["population"]["populated_templates"][0]["distinct_trait_count"])
        self.assertEqual("10", snapshot["jobs"][0]["bonus_workforce"])
        self.assertEqual("2", snapshot["budget"]["last_month"]["income"]["planet_biologists"]["unity"])
        self.assertEqual("FAIL", snapshot["strict_cache"]["status"])

    def test_missing_manifest_or_any_one_snapshot_is_not_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            self.assertEqual("NOT RUN", matrix.audit_manifest(path)["status"])
            path.write_text(json.dumps({"branches": {b: {p: "absent.sav" for p in matrix.PHASES} for b in matrix.BRANCHES}}), encoding="utf-8")
            self.assertEqual("NOT RUN", matrix.audit_manifest(path)["native_execution"])

    def test_malformed_manifest_does_not_crash_or_claim_not_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            for value in ([], {"branches": []}, {"branches": {"F00": []}}):
                path.write_text(json.dumps(value), encoding="utf-8")
                self.assertEqual("INVALID", matrix.audit_manifest(path)["status"])

    def test_21_snapshot_reads_release_documents_before_next_read(self):
        original, references, calls = matrix.native.Document, [], []

        class TrackedDocument(original):
            def __init__(self, text):
                super().__init__(text)
                references.append(weakref.ref(self))

        def tracked_loader(path):
            self.assertTrue(all(r() is None for r in references), "a prior full Document was retained")
            calls.append(path)
            return matrix.extract_snapshot(path)

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            write_development_zip(base / "development.sav")
            manifest = base / "manifest.json"
            manifest.write_text(json.dumps({"branches": {b: {p: "development.sav" for p in matrix.PHASES} for b in matrix.BRANCHES}}), encoding="utf-8")
            with mock.patch.object(matrix.native, "Document", TrackedDocument):
                matrix.audit_manifest(manifest, tracked_loader)
        self.assertEqual(21, len(calls))
        self.assertEqual(42, len(references))
        self.assertTrue(all(r() is None for r in references))

    def test_optional_common_native_save_is_read_sequentially_and_never_invented(self):
        original, references, calls = matrix.native.Document, [], []

        class TrackedDocument(original):
            def __init__(self, text):
                super().__init__(text)
                references.append(weakref.ref(self))

        def tracked_loader(path):
            self.assertTrue(all(r() is None for r in references), "a prior full Document was retained")
            calls.append(path.name)
            return matrix.extract_snapshot(path)

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            write_development_zip(base / "development.sav")
            write_development_zip(base / "common.sav")
            manifest = base / "manifest.json"
            content = {"common": "common.sav", "branches": {b: {p: "development.sav" for p in matrix.PHASES} for b in matrix.BRANCHES}}
            manifest.write_text(json.dumps(content), encoding="utf-8")
            with mock.patch.object(matrix.native, "Document", TrackedDocument):
                result = matrix.audit_manifest(manifest, tracked_loader)
            self.assertEqual("common.sav", calls[0])
            self.assertEqual(22, len(calls))
            self.assertEqual(44, len(references))
            self.assertTrue(all(r() is None for r in references))
            self.assertIsNotNone(result["common_snapshot"])
            self.assertEqual("PASS", result["setup_input_audit"]["status"])
            content["common"] = "absent.sav"
            manifest.write_text(json.dumps(content), encoding="utf-8")
            with mock.patch.object(matrix, "extract_snapshot", side_effect=AssertionError("must not read any saves")):
                missing = matrix.audit_manifest(manifest, lambda path: self.fail("must not read any saves"))
            self.assertEqual("NOT RUN", missing["status"])
            self.assertEqual("COMMON_SNAPSHOT_MISSING", missing["diagnostics"][0]["code"])


if __name__ == "__main__":
    unittest.main()
