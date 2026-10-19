"""Synthetic observation contracts only; these are not native migration results."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_1019 as checker


def design(name, section):
    return {"name": name, "body_sha256": section, "stages": [{
        "native": {"ship_size": "juggernaut"},
        "sections": [{"native": {"template": section, "slot": "mid"},
                      "components": [{"slot": "LARGE_GUN_01", "template": "SYNTHETIC_WEAPON"}]}],
        "required_components": ["SYNTHETIC_REACTOR"]}]}


def observations(paid):
    """One active and one waiting synthetic item; unrelated queues may exist."""
    old_design = design("SYNTHETIC_OLD_MOTHER", "old_section")
    queued_design = design("SYNTHETIC_PAID_SHIP", "paid_section")
    queue_items = [0, 1] if paid else []
    items = {str(i): {"native": {"paying_country": 0, "progress": 10 if i == 0 else 0,
                                 "progress_needed": 60},
                      "resources": {"alloys": 81}, "ship_implementation": {"design": 1702},
                      "orbitable": {"starbase": 13}, "queued_ship_design": queued_design,
                      "district": None, "building": None} for i in queue_items}
    base = {key: {} for key in (
        "worlds", "colonies", "districts", "pop_groups", "pop_jobs", "situations", "event_targets",
        "zones", "queues", "construction_items", "fleets", "starbases", "worlds_1019",
        "crisis_progression_raw", "country_variables_all", "country_timed_modifier", "crisis_objectives", "crisis_levels")}
    base.update({"date": "2200.01.12", "save_sha256": "b" * 64, "production_tree_sha256": "tree",
        "provenance_1019": {"version": "0.4.0-rc.3", "save_sha256": "b" * 64},
        "country": {"stockpile": {"energy": 200, "alloys": 1000},
                    "variables": {key: 0 for key in checker.ECONOMIC_VARIABLES},
                    "flags": {"eep_initialized": 1, "eep_startup_granted": 1, "eep_mothership_granted": 1},
                    "owned_colonies": [1], "ascension_perks": [], "native": {}},
        "fleets_1019": {"146": {"name": checker.MOTHER_NAME,
            "movement": {"coordinate": {"origin": 2}, "target_coordinate": {}, "orbit_raw": "starbase=2"},
            "ships": {"822": {"name": {"key": checker.MOTHER_NAME}, "coordinate": {"origin": 2},
                "target_coordinate": {}, "design_id": "1725", "design": old_design,
                "native": {"hitpoints": 900, "max_hitpoints": 1000,
                           "armor_hitpoints": 450, "max_armor_hitpoints": 500,
                           "shield_hitpoints": 400, "max_shield_hitpoints": 500}}}}},
        "starbases_1019": {"13": {"native": {"station": 822, "build_queue": 53, "shipyard_build_queue": 54}}},
        "queues_1019": {"53": {"items": [], "simultaneous": 1},
                        "54": {"items": queue_items, "simultaneous": 10},
                        "66": {"items": [], "simultaneous": 1}},
        "construction_items_1019": items})
    fixture = copy.deepcopy(base)
    fixture["save_sha256"] = "f" * 64
    fixture["provenance_1019"] = {"version": "0.3.0-rc.1" if paid else "0.3.1", "save_sha256": "f" * 64}
    original_ship = fixture["fleets_1019"]["146"]["ships"]["822"]["native"]
    for current, maximum in (("hitpoints", "max_hitpoints"), ("armor_hitpoints", "max_armor_hitpoints"),
                             ("shield_hitpoints", "max_shield_hitpoints")):
        original_ship[current] = original_ship[maximum]
    after = copy.deepcopy(base)
    after["save_sha256"] = "a" * 64
    after["provenance_1019"]["save_sha256"] = "a" * 64
    ship = after["fleets_1019"]["146"]["ships"]["822"]
    ship["design"] = design(checker.DESIGN_NAME, "new_section")
    ship["design_id"] = "1800"
    # A changed maximum with the declared life fraction preserved, never healed.
    ship["native"] = {key: value * 2 for key, value in ship["native"].items()}
    return fixture, base, after


class MigrationQueueContracts(unittest.TestCase):
    def make_case(self, paid=True, explicit=True):
        fixture, before, after = observations(paid)
        case = {"schema": "eep.1019.migration-case.v1", "fixture_sha256": fixture["save_sha256"],
                "require_damaged_before": True, "damage_mode": "fraction",
                "damage_metrics": ["hull", "armor", "shield"], "damage_tolerance": .001,
                "expected_ship_id": 822, "expected_fleet_id": 146, "expected_starbase_id": 13,
                "expected_shipyard_queue_id": 54, "expected_queued_items": 2 if paid else 0}
        if explicit:
            case["queue_mode"] = "paid" if paid else "empty"
        return case, fixture, before, after

    def report(self, data, reload_observation=None):
        case, fixture, before, after = data
        return checker.migration(case, before, after, reload_observation, fixture)

    def test_existing_paid_case_without_new_parameter_still_passes(self):
        report = self.report(self.make_case(explicit=False))
        self.assertEqual(report["status"], "PASS_SCOPED")
        self.assertEqual(report["queue_mode"], "paid")
        self.assertTrue(report["checks"]["nonempty_recorded_queue_costs_and_payer_before"])
        self.assertTrue(report["checks"]["real_queue_progress_before"])
        self.assertNotIn("before_mother_shipyard_queue_empty", report["checks"])

    def test_explicit_paid_and_waiting_item_are_preserved(self):
        report = self.report(self.make_case())
        self.assertEqual(report["status"], "PASS_SCOPED")
        self.assertEqual(report["before_snapshot"]["all_owned_queues"]["54"]["items"], [0, 1])
        self.assertEqual(report["before_snapshot"]["all_owned_queue_items"]["1"]["native"]["progress"], 0)
        self.assertTrue(report["all_differences"])  # Real design/damage changes are still reported.

    def test_public_empty_case_passes_without_claiming_paid_coverage(self):
        report = self.report(self.make_case(paid=False))
        self.assertEqual(report["status"], "PASS_SCOPED")
        self.assertEqual(report["queue_mode"], "empty")
        self.assertEqual(report["original_fixture"]["version"], "0.3.1")
        for stage in ("original", "before", "after"):
            self.assertTrue(report["checks"][stage + "_mother_shipyard_queue_empty"])
        self.assertNotIn("nonempty_recorded_queue_costs_and_payer_before", report["checks"])
        self.assertNotIn("real_queue_progress_before", report["checks"])
        self.assertIn("no paid-queue preservation is claimed", report["limitations"][0])

    def test_queue_mode_and_declared_count_must_agree(self):
        for mode, count in (("empty", 2), ("paid", 0), ("paid", -1), ("paid", True),
                            ("empty", False), ("empty", 0.0), ("paid", "2"), ("empty", None),
                            ("unknown", 0), (None, 0)):
            data = self.make_case()
            data[0].update(queue_mode=mode, expected_queued_items=count)
            with self.subTest(mode=mode, count=count), self.assertRaises(ValueError):
                self.report(data)

    def test_missing_count_is_rejected(self):
        data = self.make_case(paid=False)
        del data[0]["expected_queued_items"]
        with self.assertRaisesRegex(ValueError, "expected_queued_items"):
            self.report(data)

    def test_empty_records_cannot_certify_default_or_explicit_paid_case(self):
        for explicit in (False, True):
            data = self.make_case(paid=False, explicit=explicit)
            if explicit:
                data[0]["queue_mode"] = "paid"
            data[0]["expected_queued_items"] = 2
            with self.subTest(explicit=explicit):
                report = self.report(data)
                self.assertEqual(report["status"], "FAIL")
                for name in ("expected_mother_queue_count", "nonempty_recorded_queue_costs_and_payer_before",
                             "real_queue_progress_before"):
                    self.assertFalse(report["checks"][name])

    def test_paid_records_cannot_certify_empty_case(self):
        data = self.make_case()
        data[0].update(queue_mode="empty", expected_queued_items=0)
        report = self.report(data)
        self.assertEqual(report["status"], "FAIL")
        for stage in ("original", "before", "after"):
            self.assertFalse(report["checks"][stage + "_mother_shipyard_queue_empty"])

    def test_removing_original_paid_queue_before_migration_does_not_make_empty_case(self):
        data = list(self.make_case(paid=False))
        data[1] = observations(paid=True)[0]
        report = self.report(data)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["original_mother_shipyard_queue_empty"])
        self.assertFalse(report["checks"]["original_fixture_queue_members_binding"])

    def test_item_added_to_after_empty_queue_is_rejected(self):
        data = self.make_case(paid=False)
        paid_after = observations(paid=True)[2]
        data[3]["queues_1019"]["54"] = paid_after["queues_1019"]["54"]
        data[3]["construction_items_1019"] = paid_after["construction_items_1019"]
        report = self.report(data)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["after_mother_shipyard_queue_empty"])
        self.assertFalse(report["checks"]["all_owned_queues_preserved"])
        self.assertFalse(report["checks"]["all_queue_costs_progress_designs_orbitables_preserved"])

    def test_paid_case_requires_original_identity_and_expected_count(self):
        for mutation in ("fixture_id", "count"):
            data = self.make_case()
            if mutation == "fixture_id":
                data[1]["queues_1019"]["54"]["items"] = [8, 9]
            else:
                data[0]["expected_queued_items"] = 1
            with self.subTest(mutation=mutation):
                report = self.report(data)
                self.assertEqual(report["status"], "FAIL")
                self.assertFalse(report["checks"]["original_fixture_queue_members_binding" if mutation == "fixture_id"
                                                    else "expected_mother_queue_count"])

    def test_paid_before_requires_cost_payer_and_real_progress(self):
        for mutation in ("cost", "payer", "progress"):
            data = self.make_case()
            for observation in data[2:]:
                for item in observation["construction_items_1019"].values():
                    if mutation == "cost":
                        item["resources"] = {}
                    elif mutation == "payer":
                        item["native"]["paying_country"] = 1
                    else:
                        item["native"]["progress"] = 0
            with self.subTest(mutation=mutation):
                report = self.report(data)
                self.assertEqual(report["status"], "FAIL")
                self.assertFalse(report["checks"]["real_queue_progress_before" if mutation == "progress"
                                                    else "nonempty_recorded_queue_costs_and_payer_before"])

    def test_paid_item_recreated_with_new_identity_is_rejected(self):
        data = self.make_case()
        after = data[3]
        after["queues_1019"]["54"]["items"] = [8, 1]
        after["construction_items_1019"]["8"] = after["construction_items_1019"].pop("0")
        report = self.report(data)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["all_owned_queues_preserved"])
        self.assertFalse(report["checks"]["all_queue_costs_progress_designs_orbitables_preserved"])

    def test_any_paid_item_field_changed_after_is_rejected(self):
        for field in ("progress", "cost", "payer", "design", "orbitable"):
            data = self.make_case()
            item = data[3]["construction_items_1019"]["0"]
            if field == "progress":
                item["native"]["progress"] += 1
            elif field == "cost":
                item["resources"]["alloys"] += 1
            elif field == "payer":
                item["native"]["paying_country"] = 1
            elif field == "design":
                item["queued_ship_design"] = design("CHANGED", "replacement_section")
            else:
                item["orbitable"]["starbase"] = 20
            with self.subTest(field=field):
                report = self.report(data)
                self.assertEqual(report["status"], "FAIL")
                self.assertFalse(report["checks"]["all_queue_costs_progress_designs_orbitables_preserved"])

    def test_empty_mother_does_not_exempt_other_owned_queues(self):
        data = self.make_case(paid=False)
        for observation in data[1:]:
            observation["queues_1019"]["66"]["items"] = [90]
            observation["construction_items_1019"]["90"] = observations(paid=True)[1]["construction_items_1019"]["0"]
        self.assertEqual(self.report(data)["status"], "PASS_SCOPED")
        data[3]["construction_items_1019"]["90"]["native"]["progress"] = 0
        report = self.report(data)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["checks"]["all_queue_costs_progress_designs_orbitables_preserved"])

    def test_neither_mode_allows_new_charge_refund_or_reward(self):
        for paid in (False, True):
            for mutation in ("charge", "refund", "reward"):
                data = self.make_case(paid=paid)
                if mutation == "reward":
                    data[3]["country"]["variables"]["eep_c"] += 1
                else:
                    data[3]["country"]["stockpile"]["alloys"] += -81 if mutation == "charge" else 81
                with self.subTest(paid=paid, mutation=mutation):
                    report = self.report(data)
                    self.assertEqual(report["status"], "FAIL")
                    self.assertFalse(report["checks"]["ledger_not_awarded_again" if mutation == "reward"
                                                        else "no_additional_charge_or_refund"])

    def test_healed_layer_is_rejected_in_both_queue_modes(self):
        for paid in (False, True):
            data = self.make_case(paid=paid)
            ship = data[3]["fleets_1019"]["146"]["ships"]["822"]["native"]
            ship["armor_hitpoints"] = ship["max_armor_hitpoints"]
            with self.subTest(paid=paid):
                report = self.report(data)
                self.assertEqual(report["status"], "FAIL")
                self.assertFalse(report["checks"]["damaged_layers_remain_damaged"])
                self.assertFalse(report["checks"]["damage_preserved_in_declared_mode"])

    def test_same_day_reload_retains_each_queue_contract(self):
        for paid in (False, True):
            data = self.make_case(paid=paid)
            reloaded = copy.deepcopy(data[3])
            with self.subTest(paid=paid):
                self.assertEqual(self.report(data, reloaded)["status"], "PASS_SCOPED")
                reloaded["queues_1019"]["54"]["items"] = [999]
                report = self.report(data, reloaded)
                self.assertEqual(report["status"], "FAIL")
                self.assertFalse(report["checks"]["reload_migration_snapshot_preserved"])
                self.assertEqual(report["reload_check"]["strict_comparison"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
