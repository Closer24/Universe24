"""Reject errors hidden by intact state digests or unchanged detector input sums."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from research.component_review.audit import Snapshot
from research.staged_blocks.audit import ROOT, audit_manifest, audit_record, file_digest, load, read_states, source_control


class StagedAuditIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = Path(__file__).resolve().parents[1]/"research/message_mechanism/evidence/baseline_v1/records"
        cls.on = load(folder/"packet-r42-on.json.gz")
        cls.off = load(folder/"packet-r42-off.json.gz")

    def test_forged_display_routing_rejected_despite_valid_fingerprint(self):
        record = copy.deepcopy(self.on)
        row = record["experiment"]["coupling"]["ports"][0]
        row[0], row[1] = row[1], row[0]
        with self.assertRaisesRegex(AssertionError, "Recorded ports differ"):
            audit_record(record)

    def test_suppressed_waiting_phase_arithmetic_event_rejected(self):
        record = copy.deepcopy(self.on)
        trace = record["detector_observations"]["receiver.node"]["trace"]
        frame = next(row for row in trace if row["arithmetic_events"])
        frame["arithmetic_events"].pop()
        with self.assertRaisesRegex(AssertionError, "arithmetic C was hidden"):
            audit_record(record)

    def test_balanced_forged_port_contributions_rejected(self):
        record = copy.deepcopy(self.on)
        terms = record["detector_observations"]["receiver.node"]["trace"][0]["six_inputs"][0]
        terms[0]["b"] = str(int(terms[0]["b"])+1)
        terms[1]["b"] = str(int(terms[1]["b"])-1)
        with self.assertRaisesRegex(AssertionError, "six-port contributions mismatch"):
            audit_record(record)

    def test_stationary_source_off_with_changed_halo_is_not_a_matched_control(self):
        on, off = read_states(self.on["experiment"])[0], read_states(self.off["experiment"])[0]
        cells = dict(off.cells)
        address = next(a for a in cells if a[1:3] != (64, 64))
        a, b, r = cells[address]
        cells[address] = (a, b, (r+2) % 6)
        wrong = Snapshot(off.side, off.background, cells)
        allowed = [(x, 64, 64, g) for x in range(32, 36) for g in (0, 14)]
        with self.assertRaisesRegex(AssertionError, "apparatus remainder"):
            source_control(on, wrong, allowed)

    def test_manifest_hash_failure_retains_honest_incomplete_scope(self):
        folder = ROOT/'research/staged_blocks/evidence/composition'
        manifest = {'format': 'universe24-staged-independent-audit-manifest-v1',
                    'base_commit': 'b552f90dd8e19f836424411019dccd573c10fa6c',
                    'studies': [{'id': 'corrupt_input', 'kind': 'composition',
                                 'protocol': {'path': str(folder/'protocol.json'), 'sha256': '0'*64},
                                 'result': {'path': str(folder/'result.json'), 'sha256': file_digest(folder/'result.json')},
                                 'records': []}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'manifest.json'
            path.write_text(json.dumps(manifest))
            report = audit_manifest(path, max_cpu_seconds=30)
        self.assertFalse(report['passed'])
        self.assertEqual(report['studies'], [])
        self.assertEqual(report['failure']['study'], 'corrupt_input')
        self.assertIn('Manifest hash mismatch', report['failure']['message'])
        self.assertEqual(report['failure']['incomplete_study_dynamical_replay_progress']['complete_dynamical_records'], 0)


if __name__ == "__main__":
    unittest.main()
