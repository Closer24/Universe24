"""The independent audit must reject both unrehashable and rehashed corruption."""
import copy
import gzip
import json
from pathlib import Path
import unittest

from research.light_approval.audit import audit_recording, digest


class IndependentLightApprovalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        path = root/'research/light_approval/evidence/primary_v1/records/shared-0-00.json.gz'
        cls.recording = json.loads(gzip.decompress(path.read_bytes()))['experiment']
        cls.receivers = {'A': [32, 24, 48], 'B': [32, 72, 48]}

    def corrupt(self):
        recording = copy.deepcopy(self.recording)
        frame = recording['frames'][1]
        frame['cells'][0][4] = str(int(frame['cells'][0][4])+1)
        return recording

    def test_changed_state_with_original_digest_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'state hash mismatch'):
            audit_recording(self.corrupt(), self.receivers)

    def test_changed_state_with_new_digest_is_rejected_by_matrix_oracle(self):
        recording = self.corrupt()
        frame = recording['frames'][1]
        frame['state_sha256'] = digest({'side': recording['side'],
            'background': recording['background'], 'cells': frame['cells']})
        with self.assertRaisesRegex(AssertionError, 'matrix forward mismatch'):
            audit_recording(recording, self.receivers)


if __name__ == '__main__':
    unittest.main()
