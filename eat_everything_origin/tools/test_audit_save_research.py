"""Guard against confusing the native research bank with its stale economy mirror."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

import audit_save


class ResearchBankTests(unittest.TestCase):
    def audit_country(self, bank='stored_techpoints={100 200.25 300}', mirror='10 20 30'):
        physics, society, engineering = mirror.split()
        tech_status = bank + ' stored_techpoints_for_tech={tech_psionic_theory=1929.19999}'
        native = ('date="2200.01.01" country={0={modules={standard_economy_module={resources={'
                  'energy=123.5 minerals=400 unity=87 physics_research=' + physics +
                  ' society_research=' + society + ' engineering_research=' + engineering +
                  '}}} tech_status={' + tech_status + '} owned_planets={}}}')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'native.sav'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('gamestate', native)
            original = path.read_bytes()
            result = audit_save.audit(path, (0,))
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(result['save_sha256'], hashlib.sha256(original).hexdigest())
        return result, tech_status

    def test_stale_mirror_does_not_change_effective_bank(self):
        before, _ = self.audit_country(mirror='10 20 30')
        after, _ = self.audit_country(mirror='100 200.25 300')
        before = before['countries']['0']
        after = after['countries']['0']
        self.assertNotEqual(before['stockpile'], after['stockpile'])
        self.assertEqual(before['research_stockpile'], after['research_stockpile'])
        self.assertEqual(before['effective_stockpile'], after['effective_stockpile'])
        self.assertEqual(before['research_stockpile'], {
            'physics_research': 100, 'society_research': 200.25, 'engineering_research': 300})

    def test_actual_research_consumption_is_visible_with_unchanged_mirror(self):
        before, _ = self.audit_country()
        after, _ = self.audit_country(bank='stored_techpoints={100 130.25 300}')
        before = before['countries']['0']
        after = after['countries']['0']
        self.assertEqual(before['stockpile'], after['stockpile'])
        self.assertEqual(after['effective_stockpile']['society_research'] -
                         before['effective_stockpile']['society_research'], -70)

    def test_raw_text_nonresearch_stocks_and_partial_progress_are_preserved(self):
        result, tech_status = self.audit_country()
        country = result['countries']['0']
        self.assertEqual(country['tech_status'], tech_status)
        self.assertEqual(country['research_progress_by_tech'], {'tech_psionic_theory': 1929.19999})
        self.assertEqual(country['stockpile_source'], 'modules.standard_economy_module.resources')
        self.assertEqual(country['research_stockpile_source'], 'tech_status.stored_techpoints')
        self.assertEqual({k: country['effective_stockpile'][k] for k in ('energy', 'minerals', 'unity')},
                         {'energy': 123.5, 'minerals': 400, 'unity': 87})
        self.assertEqual(result['audit_schema_version'], 2)
        self.assertEqual(result['audit_tool_sha256'],
                         hashlib.sha256(Path(audit_save.__file__).read_bytes()).hexdigest())

    def test_missing_bank_is_unavailable_without_cached_fallback(self):
        result, _ = self.audit_country(bank='')
        country = result['countries']['0']
        self.assertIsNone(country['research_stockpile'])
        self.assertIsNone(country['effective_stockpile'])
        self.assertEqual(country['stockpile']['society_research'], 20)
        self.assertEqual(country['research_progress_by_tech']['tech_psionic_theory'], 1929.19999)

    def test_malformed_bank_fails_instead_of_manufacturing_values(self):
        invalid = ('stored_techpoints={1 2}', 'stored_techpoints={1 2 3 4}',
                   'stored_techpoints={1 no 3}', 'stored_techpoints={1 "2" 3}',
                   'stored_techpoints={1 1e999 3}', 'stored_techpoints=1',
                   'stored_techpoints={1 2 3} stored_techpoints={4 5 6}',
                   'stored_techpoints={1 {2} 3}')
        for bank in invalid:
            with self.subTest(bank=bank), self.assertRaises(ValueError):
                self.audit_country(bank=bank)

    def test_signed_and_exponent_values_keep_native_numeric_meaning(self):
        result, _ = self.audit_country(bank='stored_techpoints={-1.25 2e2 3}')
        self.assertEqual(result['countries']['0']['research_stockpile'], {
            'physics_research': -1.25, 'society_research': 200.0, 'engineering_research': 3})


if __name__ == '__main__':
    unittest.main()
