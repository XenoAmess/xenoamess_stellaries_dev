import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_artificial_worlds_1023 import compare


class SettlementEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.ledger = dict(eep_c=6, eep_g=6, eep_d=3, eep_made=100, eep_worlds=1)
        self.before = {"save_sha256": "before", "date": "2200.01.01",
            "planets": {"9": {"planet_class": "pc_habitat", "colony": 4}, "2": {"flags": "habitat9=yes"}},
            "colonies": {"4": {"population": 100}}, "countries": {}, "situations": {},
            "fleets": {"22": {}}, "megastructures": {}}
        self.after = {"save_sha256": "after", "date": "2201.01.01",
            "planets": {"2": {"flags": "habitat_build_site=yes"}}, "colonies": {},
            "countries": {"0": self.ledger}, "situations": {}, "fleets": {},
            "megastructures": {"5": {"type": "habitat_central_complex_ruined"}}}
        self.contract = {"actor": 0, "source": 9, "colony": 4, "anchor": 2,
                         "removed_fleets": [22], "expected_ledger": self.ledger}

    def result(self, after):
        return compare(self.before, after, self.contract)["status"]

    def test_complete_evidence(self):
        self.assertEqual(self.result(self.after), "PASS_SCOPED")

    def test_remaining_planet_rejected(self):
        self.after["planets"]["9"] = {}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_remaining_colony_rejected(self):
        self.after["colonies"]["4"] = {"owner": 1, "pop_groups": [11]}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_duplicate_reward_rejected(self):
        self.after["countries"] = copy.deepcopy(self.after["countries"])
        self.after["countries"]["0"]["eep_c"] = 12
        self.assertEqual(self.result(self.after), "FAIL")

    def test_empty_colony_still_owned_by_country_zero_rejected(self):
        self.after["colonies"]["4"] = {"owner": 0, "pop_groups": []}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_remaining_defence_fleet_rejected(self):
        self.after["fleets"]["22"] = {}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_missing_source_precondition_rejected(self):
        self.before["planets"] = {}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_old_unrelated_ruin_is_not_proof(self):
        self.before["megastructures"] = copy.deepcopy(self.after["megastructures"])
        self.assertEqual(self.result(self.after), "FAIL")

    def test_native_serialized_link_still_present_rejected(self):
        self.after["planets"]["2"]["flags"] = "habitat9=62808000"
        self.assertEqual(self.result(self.after), "FAIL")

    def test_orbital_still_present_rejected(self):
        self.before["megastructures"]["6"] = {"type": "habitat_major_orbital"}
        self.after["megastructures"]["6"] = {"type": "habitat_major_orbital"}
        self.contract["removed_megastructures"] = [6]
        self.assertEqual(self.result(self.after), "FAIL")

    def test_native_situation_target_id_still_live_rejected(self):
        self.after["situations"]["8"] = {"target": {"type": "planet", "id": 9}}
        self.assertEqual(self.result(self.after), "FAIL")

    def test_native_killed_situation_history_allowed(self):
        self.after["situations"]["8"] = {"killed": "yes", "target": {"type": "planet", "id": 9}}
        self.assertEqual(self.result(self.after), "PASS_SCOPED")

    def month_boundary(self):
        self.after["colonies"]["0"] = {"population": 5100}
        self.after["receipts"] = {"0": {"eep_last_return": 130, "eep_last_manufactured": 100}}
        self.contract.update(core_colony=0, core_population_interval=[5097,5103],
                             source_return_interval=[129,131], expected_manufactured=100)

    def test_month_boundary_predeclared_range(self):
        self.month_boundary()
        self.assertEqual(self.result(self.after), "PASS_SCOPED")

    def test_month_boundary_extra_population_rejected(self):
        self.month_boundary()
        self.after["colonies"]["0"]["population"] = 5200
        self.assertEqual(self.result(self.after), "FAIL")

    def test_month_boundary_receipt_alone_cannot_cover_population_loss(self):
        self.month_boundary()
        self.after["colonies"]["0"]["population"] = 4900
        self.assertEqual(self.result(self.after), "FAIL")


if __name__ == "__main__":
    unittest.main()
