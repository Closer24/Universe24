"""Installed observer boundary: clicks suffice; calibration is explicit."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from universe24.model import make_model_bundle, prepare_occupation
from universe24.system.bundle import create_bundle
from universe24.runtime import main
from universe24.system.runtime import run_bundle


class ObserverCLIContractTests(unittest.TestCase):
    def test_standalone_clicks_and_calibration_without_hidden_state_access(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            base = make_model_bundle(L=3, pattern='vacuum')
            occupation = np.zeros((48, 27), dtype=object)
            occupation[0] = 1
            bundle = create_bundle(base.tensor, prepare_occupation(L=3, occupation=occupation),
                                   channels=base.channels, protocol=base.protocol, model=base.model)
            run_bundle(bundle, root / 'run', 3)
            standalone = root / 'only-clicks.jsonl.gz'
            shutil.copyfile(root / 'run' / 'clicks.jsonl.gz', standalone)
            with (patch('universe24.system.runtime.verify_run', side_effect=AssertionError('hidden replay')),
                  patch('universe24.system.bundle.load_bundle', side_effect=AssertionError('hidden bundle'))):
                summary = main(['observe-clicks', '--clicks', str(standalone)])
                self.assertGreater(summary['events'], 0)
                report = main(['observe-clicks', '--clicks', str(standalone),
                               '--channel', '0',
                               '--nodes', '27', '--steps', '3',
                               '--initial-a', '1', '--initial-b', '2',
                               '--out', str(root / 'observation.json')])
            channel = report['calibrated_channel']
            self.assertEqual(channel['values_by_step'], [['1'] * 27] * 3)
            self.assertEqual(len(channel['changes']), 27)
            self.assertEqual(report, json.loads((root / 'observation.json').read_text()))
            with self.assertRaises(SystemExit):
                main(['observe-clicks', '--clicks', str(standalone), '--out', str(root / 'observation.json')])

    def test_partial_calibration_is_rejected_before_opening_a_file(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(['observe-clicks', '--clicks', 'missing.jsonl.gz', '--channel', '1'])
        self.assertEqual(caught.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
