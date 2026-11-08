"""Independent-auditor regression tests for hidden state and control failures."""
import hashlib
import json
from pathlib import Path
import unittest

from research.clock_selection.audit import (
    Snapshot, all_events, assess_case, assess_group, expected_initial, load,
    matches, native_digest, observations, packet, planned_cases,
)
from research.staged_blocks.audit import read_states

ROOT = Path(__file__).resolve().parents[1]


class ClockSelectionAuditTests(unittest.TestCase):
    def test_native_hash_retains_decimal_strings_and_arbitrary_integers(self):
        n = 10**90+7
        state = Snapshot(7, (0, 0, 2), {(3, 3, 3, 47): (n, -n, 5)})
        raw = {'side': 7, 'background': ['0', '0', 2],
               'cells': [[3, 3, 3, 47, str(n), str(-n), 5]]}
        expected = hashlib.sha256(json.dumps(raw, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(native_digest(state), expected)

    def test_complete_carrier_rejects_hidden_channel_remainder(self):
        cells = packet(321, 120, 160, 160)
        state = Snapshot(321, (0, 0, 2), cells)
        self.assertTrue(matches(state, 120, 160, 160))
        damaged = dict(cells)
        damaged[(121, 160, 160, 47)] = (0, 0, 3)
        self.assertFalse(matches(Snapshot(321, (0, 0, 2), damaged), 120, 160, 160))

    def test_source_ablation_retains_the_ghost_remainder_footprint(self):
        case = next(c for c in planned_cases() if c['stage'] == 'encounter' and c['phase'] == 1 and c['gap'] == 34)
        on = expected_initial({**case, 'control': '11'})
        off = expected_initial({**case, 'control': '01'})
        writer_x = 160-17
        self.assertEqual(off.at((writer_x, 160, 160, 0)), (0, 0, 4))
        self.assertEqual(off.at((writer_x, 160, 160, 14)), (0, 0, 0))
        for address in set(on.cells) | set(off.cells):
            self.assertEqual(on.at(address)[2], off.at(address)[2])

    def test_no_guarded_C_does_not_mean_zero_quotient(self):
        stationary = Snapshot(3, (0, 0, 2), {(1, 1, 1, 0): (1, 1, 2)})
        self.assertEqual(all_events([stationary, stationary])[0], [])
        self.assertEqual(stationary.at((1, 1, 1, 0))[0]+stationary.at((1, 1, 1, 0))[1], 2)

    def test_favorable_joint_output_cannot_rescue_invalid_probe_control(self):
        folder = ROOT/'research/clock_selection/evidence/write_probe_v1_run01'
        rows = []
        for mask in ('00', '10', '01', '11'):
            saved = load(folder/f'records/write-probe-L321-r0-p1-d1-gap34-{mask}.json.gz')
            states = read_states(saved['experiment'])
            out = observations(saved['case'], states)
            rows.append({'case': saved['case'], 'states': states, 'observations': out,
                         'assessment': assess_case(saved['case'], out)})
        self.assertTrue(rows[3]['assessment']['carrier_plus_C'])
        self.assertFalse(rows[2]['assessment']['incoming_contract'])
        group = assess_group(rows, load(folder/'protocol.json')['claim'])
        self.assertFalse(group['carrier_discriminator'])
        self.assertFalse(group['carrier_and_C_discriminator'])


if __name__ == '__main__':
    unittest.main()
