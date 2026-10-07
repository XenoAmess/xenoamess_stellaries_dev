"""Offline gate tests with synthetic receipts in a disposable directory."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import release_acceptance as gate


class ReleaseAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.proof = self.root / 'docs/proof.json'
        self.proof.parent.mkdir()
        self.proof.write_text('{"status":"SYNTHETIC_TEST_ONLY"}\n', encoding='utf-8')
        self.evidence = [{'path': 'docs/proof.json', 'sha256': hashlib.sha256(self.proof.read_bytes()).hexdigest()}]
        self.files = {'descriptor.mod': 'synthetic-production-hash'}
        self.disclosure = '。'.join(gate.DISCLOSURES)
        self.receipt = {
            'status': 'PASS_SCOPED', 'acceptance_mode': gate.SCOPED_MODE,
            'scope': gate.FOCUS_SCOPE, 'version': '0.2.0',
            'game_exe_sha256': gate.EXE_SHA256, 'language': 'l_simp_chinese',
            'production_files': self.files, 'fully_accepted_civics': [gate.FOCUS_CIVIC],
            'open_civics': sorted(gate.OPEN_CIVICS),
            'deferred_civics': {key: {'status': 'NOT_COMPLETE', 'remaining': 'Independent natural combinations remain.'}
                                for key in gate.OPEN_CIVICS - {gate.FOCUS_CIVIC}},
            'cases': {key: ({'scope': gate.FOCUS_SCOPE, 'status': 'NOT_APPLICABLE',
                            'reason': 'The Scorched Hive focus uses the generic branch.'}
                           if key in gate.NOT_APPLICABLE else
                           {'scope': gate.FOCUS_SCOPE, 'status': 'PASS_SCOPED', 'evidence': self.evidence})
                      for key in gate.CASES},
            'production_smoke': {'status': 'PASS', 'production_files': self.files, 'evidence': self.evidence},
        }

    def validate(self, receipt=None, **texts):
        return gate.validate_runtime(receipt or self.receipt, self.files, '0.2.0',
                                     texts.get('description', self.disclosure),
                                     texts.get('note', '[v0.2.0] ' + self.disclosure),
                                     texts.get('changelog', self.disclosure), self.root)

    def reject(self, receipt):
        with self.assertRaises(RuntimeError):
            self.validate(receipt)

    def test_explicit_scoped_receipt_accepts_only_one_fully_accepted_civic(self):
        accepted = self.validate()
        self.assertEqual(accepted['status'], 'PASS_SCOPED')
        self.assertEqual(accepted['fully_accepted_civics'], [gate.FOCUS_CIVIC])
        self.assertEqual(len(accepted['deferred_civics']), 4)

    def test_missing_required_case_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        del receipt['cases']['EAT-14']
        self.reject(receipt)

    def test_pending_common_case_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['cases']['EAT-14']['status'] = 'PENDING'
        self.reject(receipt)

    def test_only_two_designated_cases_may_be_not_applicable(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['cases']['EAT-16'] = {'scope': gate.FOCUS_SCOPE, 'status': 'NOT_APPLICABLE', 'reason': 'skip'}
        self.reject(receipt)

    def test_not_applicable_reason_required(self):
        for identity in gate.NOT_APPLICABLE:
            with self.subTest(identity=identity):
                receipt = copy.deepcopy(self.receipt)
                receipt['cases'][identity]['reason'] = ' '
                self.reject(receipt)

    def test_other_civic_cannot_be_claimed_fully_accepted(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['fully_accepted_civics'].append('civic_machine_terminator')
        self.reject(receipt)
        receipt = copy.deepcopy(self.receipt)
        receipt['deferred_civics']['civic_machine_terminator']['status'] = 'PASS'
        self.reject(receipt)

    def test_missing_deferred_route_or_remaining_work_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        del receipt['deferred_civics']['civic_machine_terminator']
        self.reject(receipt)
        receipt = copy.deepcopy(self.receipt)
        receipt['deferred_civics']['civic_machine_terminator']['remaining'] = ''
        self.reject(receipt)

    def test_all_five_entrances_must_remain_open(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['open_civics'].remove('civic_machine_terminator')
        self.reject(receipt)

    def test_scope_version_exe_and_language_drift_rejected(self):
        for key, bad in [('scope', 'all'), ('version', '0.2.0-rc.6'),
                         ('game_exe_sha256', 'different'), ('language', 'l_english'),
                         ('acceptance_mode', 'skip'), ('status', 'PASS')]:
            with self.subTest(key=key):
                receipt = copy.deepcopy(self.receipt)
                receipt[key] = bad
                self.reject(receipt)

    def test_production_drift_and_missing_smoke_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['production_files'] = {}
        self.reject(receipt)
        receipt = copy.deepcopy(self.receipt)
        receipt['production_smoke']['production_files'] = {}
        self.reject(receipt)
        receipt = copy.deepcopy(self.receipt)
        del receipt['production_smoke']
        self.reject(receipt)

    def test_evidence_is_required_confined_and_byte_exact(self):
        for evidence in [[], [{'path': 'docs/proof.json', 'sha256': 'different'}],
                         [{'path': '../outside.json', 'sha256': 'different'}],
                         [{'path': str(self.proof.resolve()), 'sha256': self.evidence[0]['sha256']}]]:
            with self.subTest(evidence=evidence):
                receipt = copy.deepcopy(self.receipt)
                receipt['cases']['EAT-14']['evidence'] = evidence
                self.reject(receipt)

    def test_every_public_text_must_disclose_scope(self):
        for field in ['description', 'note', 'changelog']:
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                self.validate(**{field: 'Gameplay features only.'})

    def test_full_mode_still_requires_all_cases(self):
        receipt = copy.deepcopy(self.receipt)
        receipt.update(acceptance_mode='full', status='PASS')
        receipt['cases'] = {identity: {'status': 'PASS'} for identity in gate.CASES}
        self.assertEqual(self.validate(receipt)['status'], 'PASS')
        receipt['cases']['EAT-05']['status'] = 'NOT_APPLICABLE'
        self.reject(receipt)


if __name__ == '__main__':
    unittest.main()
