"""Installed click-observer input/output contracts, not new physical claims."""
from copy import deepcopy
import gzip
import hashlib
from pathlib import Path
import tempfile
import unittest

from universe24.core import Engine, exact_json
from universe24.detection import make_detector_bundle
from universe24.light import light_tensor
from universe24.observer import (read_clicks, observed_payload, inspect_click_file,
                                 reconstruct_memory_from_clicks)
from universe24.system.decoder import make_transition, decode_transition


class ClickObserverContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = make_detector_bundle(L=3, root=0, light_position=0,
                                          arm_position=1, amplitude=2)
        cls.memory = cls.bundle.model['roles']['memory']
        engine = Engine(cls.bundle.tensor)
        state = cls.bundle.seed
        cls.records, cls.other_records, cls.accounts = [], [], []
        for tick in range(1, 6):
            after = engine.step(state)
            for run_id, target in [('observer-contract', cls.records),
                                   ('another-run', cls.other_records)]:
                record = make_transition(cls.bundle.tensor, state, after,
                                         run_id=run_id, step=tick)
                target.extend(decode_transition(record, cls.bundle.tensor))
            cls.accounts.append({'step': tick, 'memory_account': str(
                sum(int(v)**2 for v in after.b[cls.memory]))})
            state = after

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name)/'clicks.jsonl.gz'

    def write_records(self, records):
        with gzip.open(self.path, 'wt', encoding='utf-8') as stream:
            for record in records:
                stream.write(exact_json.dumps(record)+'\n')

    def observe(self, **kwargs):
        calibration = dict(memory_channel=self.memory, node_count=27, steps=5)
        calibration.update(kwargs)
        return reconstruct_memory_from_clicks(self.path, **calibration)

    def test_click_file_only_recovers_calibrated_memory_and_quiet_intervals(self):
        self.write_records(self.records)
        before = self.path.read_bytes()
        observed = self.observe()
        self.assertEqual(observed['accounts'], self.accounts)
        self.assertEqual(observed['outcomes'], {'capture': 9, 'release': 9, 'exchange': 0})
        self.assertEqual(observed['memory_arithmetic_clicks'], 36)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(Path(self.temporary.name).iterdir()), [self.path])
        self.assertEqual(inspect_click_file(self.path)['events'], len(self.records))

    def test_cross_run_projection_excludes_only_provenance(self):
        self.assertNotEqual(self.records, self.other_records)
        self.assertEqual(observed_payload(self.records), observed_payload(self.other_records))
        changed = deepcopy(self.records)
        changed[0]['quotient'] += 1
        self.assertNotEqual(observed_payload(self.records), observed_payload(changed))
        self.assertIn('quotient', observed_payload(self.records)[0])

    def test_mixed_run_and_duplicate_records_are_rejected(self):
        for records in (self.records+self.other_records, self.records+self.records):
            with self.subTest(mixed=records is not self.records):
                self.write_records(records)
                with self.assertRaises(ValueError):
                    self.observe()

    def test_reordered_events_are_rejected(self):
        records = deepcopy(self.records)
        records[0], records[1] = records[1], records[0]
        self.write_records(records)
        with self.assertRaisesRegex(ValueError, 'canonical chronological order'):
            read_clicks(self.path)

    def test_mixed_tensor_and_uncalibrated_law_are_rejected(self):
        changed = deepcopy(self.records)
        for record in changed:
            record['tensor_hash'] = light_tensor().fingerprint
            identity = {key: record[key] for key in ('run_id', 'tensor_hash', 'step', 'node', 'channel')}
            record['event_id'] = hashlib.sha256(exact_json.dumps(identity, sort_keys=True).encode('ascii')).hexdigest()
        self.write_records(self.records+changed)
        with self.assertRaises(ValueError):
            read_clicks(self.path)
        self.write_records(changed)
        with self.assertRaisesRegex(ValueError, 'calibrated detector law'):
            self.observe()

    def test_malformed_json_fields_and_sign_are_rejected(self):
        serialized = exact_json.dumps(self.records[0])
        duplicate_key = '{"step":999,'+serialized[1:]
        with gzip.open(self.path, 'wt', encoding='utf-8') as stream:
            stream.write(duplicate_key+'\n')
        with self.assertRaisesRegex(ValueError, 'duplicate click JSON field'):
            read_clicks(self.path)
        records = deepcopy(self.records)
        records[0]['sign'] = -1
        self.write_records(records)
        with self.assertRaises(ValueError):
            read_clicks(self.path)

    def test_calibration_bounds_and_nonnegative_history_are_enforced(self):
        self.write_records(self.records)
        for calibration in ({'steps': 1}, {'node_count': 1}, {'memory_channel': True},
                            {'steps': -1}, {'memory_channel': 48}):
            with self.subTest(calibration=calibration), self.assertRaises(ValueError):
                self.observe(**calibration)
        records = deepcopy(self.records)
        release = next(e for e in records if e['step'] == 4 and e['channel'] == self.memory)
        release['quotient'] = 1
        self.write_records(records)
        with self.assertRaisesRegex(ValueError, 'negative retained memory'):
            self.observe()

    def test_unbounded_integer_observations_do_not_change_global_digit_limits(self):
        import sys
        limit = sys.get_int_max_str_digits()
        record = deepcopy(next(e for e in self.records
                               if e['step'] == 1 and e['channel'] == self.memory))
        record['quotient'] = 10**5000
        self.write_records([record])
        result = self.observe(steps=1)
        self.assertEqual(result['events'][0]['memory_after'], '1'+'0'*5000)
        self.assertEqual(result['accounts'][0]['memory_account'], '1'+'0'*10000)
        self.assertEqual(inspect_click_file(self.path)['signed_quotient_sum'], '1'+'0'*5000)
        self.assertEqual(sys.get_int_max_str_digits(), limit)


if __name__ == '__main__':
    unittest.main()
