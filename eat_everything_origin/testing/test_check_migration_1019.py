"""Synthetic contract tests only: these do not certify any native SAV."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_migration_1019 as checker
from test_check_1019_migration import observations


def synthetic_case(paid=False):
    kind = "paid11" if paid else "public031"
    case = checker.template(kind)
    known = checker.FIXTURES[kind]
    fixture, before, after = observations(paid)
    if paid:
        for obs in (fixture, before, after):
            original_item = copy.deepcopy(obs["construction_items_1019"]["0"])
            obs["queues_1019"]["54"]["items"] = list(range(11))
            obs["construction_items_1019"] = {str(i): copy.deepcopy(original_item) for i in range(11)}
            for i, item in obs["construction_items_1019"].items():
                item["native"]["progress"] = 10 if int(i) < 10 else 0
    else:
        for obs in (fixture, before, after):
            obs["fleets_1019"]["128"] = obs["fleets_1019"].pop("146")
            fleet = obs["fleets_1019"]["128"]
            fleet["ships"]["1008"] = fleet["ships"].pop("822")
            obs["starbases_1019"]["15"] = obs["starbases_1019"].pop("13")
            base = obs["starbases_1019"]["15"]["native"]
            base.update(station=1008, build_queue=49, shipyard_build_queue=50)
            obs["queues_1019"]["49"] = obs["queues_1019"].pop("53")
            obs["queues_1019"]["50"] = obs["queues_1019"].pop("54")
    fid, sid, bid = (str(known[k]) for k in ("expected_fleet_id", "expected_ship_id", "expected_starbase_id"))
    for obs in (fixture, before, after):
        obs["country"].update(research_stockpile={}, effective_stockpile=copy.deepcopy(obs["country"]["stockpile"]))
        obs["language"] = "l_simp_chinese"
        obs["production_tree_sha256"] = checker.OLD_TREE
        obs["provenance_1019"]["version"] = "0.3.1"
        fleet = obs["fleets_1019"][fid]
        fleet.update(variables={}, timed_modifier={"raw": "", "items": []})
        ship = fleet["ships"][sid]
        ship.update(flags={}, variables={}, timed_modifier={"raw": "", "items": []})
        ship["native"] = {"hitpoints": 900, "max_hitpoints": 1000,
                          "armor_hitpoints": 22500, "max_armor_hitpoints": 25000,
                          "shield_hitpoints": 40000, "max_shield_hitpoints": 50000}
        obs["migration_v2_native"] = {
            "manifest_game_exe_sha256": checker.EXE, "actual_game_exe_sha256": checker.EXE,
            "players": [{"country": 0}], "definition": {"body": "SYNTHETIC_DEFINITION_NOT_NATIVE"},
            "attached_starbase_raw": "SYNTHETIC_RAW_NOT_NATIVE",
            "attached_starbase_implementation": {"design": 1725},
        }
    fixture["save_sha256"] = known["fixture_sha256"]
    fixture["provenance_1019"]["save_sha256"] = fixture["save_sha256"]
    before["save_sha256"] = known["before_sha256"]
    before["provenance_1019"]["save_sha256"] = before["save_sha256"]
    for current, maximum in checker.DEFENSES.values():
        fixture["fleets_1019"][fid]["ships"][sid]["native"][current] = fixture["fleets_1019"][fid]["ships"][sid]["native"][maximum]
    ship = after["fleets_1019"][fid]["ships"][sid]
    components = [{"slot": "AUX_UTILITY_" + str(i + 6), "template": "EEP_ADAPTIVE_" + k.upper() + "_CORE"}
                  for i, k in enumerate(checker.v1.CORE_TYPES)]
    components += [{"slot": "SYNTHETIC_" + str(i), "template": "SYNTHETIC_COMPONENT"} for i in range(44)]
    ship["design"] = {"name": checker.v1.DESIGN_NAME, "body_sha256": "synthetic_new",
        "stages": [{"native": {"ship_size": "juggernaut"},
                    "sections": [{"native": {"template": "eep_mothership_section_1019", "slot": "core"},
                                  "components": components}],
                    "required_components": ["SYNTHETIC_REQUIRED_" + str(i) for i in range(6)]}]}
    ship["design_id"] = "1800"
    ship["native"].update(hitpoints=899.99, max_hitpoints=1000,
                          armor_hitpoints=44787.6 * .89999, max_armor_hitpoints=44787.6,
                          shield_hitpoints=167310 * .79999, max_shield_hitpoints=167310)
    after["save_sha256"] = "a" * 64
    after["provenance_1019"].update(version="0.4.0-rc.6", save_sha256=after["save_sha256"])
    after["production_tree_sha256"] = checker.TREE
    shape = checker.v1.design_shape(ship["design"])
    for obs in (fixture, before, after):
        obs["migration_v2_native"]["expected_design_shape"] = copy.deepcopy(shape)
    reloaded = copy.deepcopy(after)
    reloaded["save_sha256"] = "c" * 64
    reloaded["provenance_1019"]["save_sha256"] = reloaded["save_sha256"]
    rs = reloaded["fleets_1019"][fid]["ships"][sid]
    rs["design_id"] = "1801"
    for current, maximum in checker.DEFENSES.values():
        rs["native"][current] -= rs["native"][maximum] * .00001
    for obs, source in ((after, before), (reloaded, after)):
        obs["migration_v2_native"]["load_evidence"] = {
            "raw": {"source_sha256": source["save_sha256"], "date": source["date"],
                    "ui_date_verified": True, "loaded_at_utc": "2026-10-19T15:00:00+00:00"},
            "source_byte_sha256": source["save_sha256"]}
    return case, fixture, before, after, reloaded, copy.deepcopy(reloaded), copy.deepcopy(reloaded)


class MigrationV2Contracts(unittest.TestCase):
    def report(self, data):
        return checker.evaluate(*data)

    def test_native_player_unnamed_record_list_is_parsed_without_defaults(self):
        self.assertEqual(checker.native_players('date="2200.01.01" player={ {name="unknown" country=0} }'),
                         [{"name": "unknown", "country": 0}])
        self.assertEqual(checker.native_players('player={{country=0}{country=1}}'), [{"country": 0}, {"country": 1}])
        self.assertEqual(checker.native_players('player={}'), [])
        for raw in ('player={ country=0 }', 'player={{country=0} junk}', 'player={{country=0}', 'player=0'):
            with self.subTest(raw=raw), self.assertRaises(ValueError): checker.native_players(raw)

    def test_v2_pass_retains_original_v1_precision_fail_public_and_paid(self):
        for paid in (False, True):
            with self.subTest(paid=paid):
                report = self.report(synthetic_case(paid))
                self.assertEqual(report["status"], "PASS_SCOPED", [k for k, v in report["checks"].items() if not v])
                self.assertEqual(report["v1_original_diagnostic"]["status"], "FAIL")
                self.assertFalse(report["v1_original_diagnostic"]["checks"]["damage_preserved_in_declared_mode"])
                self.assertFalse(report["v1_original_diagnostic"]["checks"]["reload_migration_snapshot_preserved"])
                self.assertTrue(report["strict_comparisons"]["after_to_reload"]["differences"])

    def test_fixed_budget_boundaries_are_signed_and_step_local(self):
        for delta, allowed in ((-.000021, True), (.000001, True), (-.00002101, False), (.00000101, False)):
            data = synthetic_case()
            for obs, ratio in ((data[2], .8), (data[3], float(DecimalValue('.8') + DecimalValue(str(delta))))):
                ship = checker.mother_ship(obs)
                for current, maximum in checker.DEFENSES.values():
                    ship["native"].update({current: ratio, maximum: 1})
            with self.subTest(delta=delta):
                self.assertEqual(all(checker.ratio_step(data[2], data[3])["checks"].values()), allowed)

    def test_missing_repeat_stays_pending(self):
        data = synthetic_case()
        report = checker.evaluate(*data[:5])
        self.assertEqual(report["status"], "PENDING")
        self.assertFalse(report["checks"]["repeat_sync_samples_present"])

    def test_policy_schema_mode_and_fixture_cannot_be_reinterpreted(self):
        for key, value in (("schema", "eep.1019.migration-case.v1"), ("execution_mode", "multiplayer"),
                           ("fixture_kind", "unknown"), ("candidate_tree_sha256", "x" * 64)):
            data = list(synthetic_case()); data[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.report(data)
        for value in (-.000022, True, float("nan"), None):
            data = list(synthetic_case()); data[0]["policy"]["step_signed_ratio_min"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.report(data)

    def test_absent_invalid_and_nonfinite_native_defenses_reject(self):
        for field, value in (("hitpoints", None), ("hitpoints", True), ("hitpoints", float("nan")),
                             ("max_hitpoints", 0), ("max_hitpoints", -1), ("max_hitpoints", float("inf")),
                             ("hitpoints", -1), ("hitpoints", 1001)):
            data = list(synthetic_case()); checker.mother_ship(data[3])["native"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.report(data)

    def test_wrong_native_source_or_player_never_passes(self):
        for field, value in (("actual_game_exe_sha256", "x" * 64), ("manifest_game_exe_sha256", "x" * 64),
                             ("players", []), ("players", [{"country": 0}, {"country": 1}]),
                             ("players", [{"country": 1}])):
            data = list(synthetic_case()); data[3]["migration_v2_native"][field] = value
            with self.subTest(field=field, value=value):
                self.assertEqual(self.report(data)["status"], "FAIL")
        for key, value in (("production_tree_sha256", "x" * 64), ("language", "l_english")):
            data = list(synthetic_case()); data[3][key] = value
            self.assertEqual(self.report(data)["status"], "FAIL")

    def test_load_receipts_require_native_source_bytes_and_ui_date(self):
        for field, value in (("ui_date_verified", False), ("source_sha256", "d" * 64),
                             ("date", "2200.01.02"), ("loaded_at_utc", "")):
            data = list(synthetic_case()); data[4]["migration_v2_native"]["load_evidence"]["raw"][field] = value
            with self.subTest(field=field):
                self.assertEqual(self.report(data)["status"], "FAIL")
        data = list(synthetic_case()); data[3]["migration_v2_native"]["load_evidence"]["source_byte_sha256"] = "d" * 64
        self.assertEqual(self.report(data)["status"], "FAIL")

    def test_missing_definition_or_core_or_wrong_real_design_rejects(self):
        data = list(synthetic_case()); del data[3]["migration_v2_native"]["definition"]
        with self.assertRaises(ValueError): self.report(data)
        for mutation in ("core", "name", "slot", "required", "shape"):
            data = list(synthetic_case()); design = checker.mother_ship(data[4])["design"]
            if mutation == "core": design["stages"][0]["sections"][0]["components"][0]["template"] = "MISSING_CORE"
            elif mutation == "name": design["name"] = checker.v1.MOTHER_NAME
            elif mutation == "slot": design["stages"][0]["sections"][0]["components"].pop()
            elif mutation == "required": design["stages"][0]["required_components"].pop()
            else: design["stages"][0]["native"]["ship_size"] = "corvette"
            with self.subTest(mutation=mutation): self.assertEqual(self.report(data)["status"], "FAIL")

    def test_maximum_stat_fraud_is_not_a_roundoff_exemption(self):
        data = list(synthetic_case()); sh = checker.mother_ship(data[3])
        sh["native"]["max_armor_hitpoints"] *= 2; sh["native"]["armor_hitpoints"] *= 2
        self.assertEqual(self.report(data)["status"], "FAIL")

    def test_resources_jobs_layout_names_position_rewards_cannot_change(self):
        for mutation in ("stock", "research", "jobs", "layout", "name", "position", "reward", "startup", "identity"):
            data = list(synthetic_case()); obs = data[4]; ship = checker.mother_ship(obs)
            if mutation == "stock": obs["country"]["stockpile"]["energy"] += 1
            elif mutation == "research": obs["country"]["research_stockpile"]["physics"] = 1
            elif mutation == "jobs": obs["pop_jobs"]["new"] = {"amount": 1}
            elif mutation == "layout": obs["worlds"]["new"] = {"planet_class": "pc_machine"}
            elif mutation == "name": ship["name"]["key"] = "CHANGED"
            elif mutation == "position": ship["coordinate"]["origin"] = 7
            elif mutation == "reward": obs["country"]["variables"]["eep_c"] += 1
            elif mutation == "startup": obs["country"]["flags"]["eep_startup_granted"] = 999
            else: obs["fleets_1019"]["128"]["ships"]["1009"] = obs["fleets_1019"]["128"]["ships"].pop("1008")
            with self.subTest(mutation=mutation):
                if mutation == "identity":
                    with self.assertRaises(ValueError): self.report(data)
                else:
                    self.assertEqual(self.report(data)["status"], "FAIL")

    def test_each_paid_payment_progress_and_civilian_queue_field_is_strict(self):
        for mutation in ("cost", "payer", "progress", "design", "orbitable", "civilian"):
            data = list(synthetic_case(True)); obs = data[4]; item = obs["construction_items_1019"]["0"]
            if mutation == "cost": item["resources"]["alloys"] += 1
            elif mutation == "payer": item["native"]["paying_country"] = 1
            elif mutation == "progress": item["native"]["progress"] += 1
            elif mutation == "design": item["queued_ship_design"]["name"] = "DIFFERENT"
            elif mutation == "orbitable": item["orbitable"]["starbase"] = 99
            else: obs["queues_1019"]["66"]["items"] = [999]
            with self.subTest(mutation=mutation): self.assertEqual(self.report(data)["status"], "FAIL")

    def test_repeat_sync_has_no_roundoff_budget_or_unanchored_branch(self):
        data = list(synthetic_case()); checker.mother_ship(data[6])["native"]["hitpoints"] -= .00001
        self.assertEqual(self.report(data)["status"], "FAIL")

    def test_return_to_public_branch_requires_its_own_bounded_native_load(self):
        data = list(synthetic_case())
        data[0]["repeat_load_source"] = "reload"
        for obs in data[5:]:
            obs["save_sha256"] = "d" * 64
            ship = checker.mother_ship(obs)
            ship["design_id"] = "1802"
            for current, maximum in checker.DEFENSES.values():
                ship["native"][current] -= ship["native"][maximum] * .00001
        data[5]["migration_v2_native"]["load_evidence"] = {
            "raw": {"source_sha256": data[4]["save_sha256"], "date": data[4]["date"],
                    "ui_date_verified": True, "loaded_at_utc": "2026-10-19T15:30:00+00:00"},
            "source_byte_sha256": data[4]["save_sha256"]}
        report = self.report(data)
        self.assertEqual(report["status"], "PASS_SCOPED")
        self.assertIn("extra_native_load_before_repeat", report["steps"])
        checker.mother_ship(data[5])["native"]["hitpoints"] -= .1
        self.assertEqual(self.report(data)["status"], "FAIL")
        data = list(synthetic_case())
        for obs in data[5:]: checker.mother_ship(obs)["coordinate"]["origin"] = 77
        self.assertEqual(self.report(data)["status"], "FAIL")

    def test_inputs_and_legacy_fail_booleans_are_not_mutated(self):
        data = synthetic_case(); saved = copy.deepcopy(data); report = self.report(data)
        self.assertEqual(data, saved)
        self.assertFalse(report["v1_original_diagnostic"]["checks"]["damage_preserved_in_declared_mode"])


from decimal import Decimal as DecimalValue

if __name__ == "__main__":
    unittest.main()
