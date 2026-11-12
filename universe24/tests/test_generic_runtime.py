"""The restricted sector remains attached to canonical bundles and clicks."""
from pathlib import Path
import tempfile
import unittest

from validation.generic_couplings.runtime import run_runtime_pair


class GenericRuntimeTests(unittest.TestCase):
    def test_saved_sector_reconstructs_full_states_and_source_clicks(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_runtime_pair(Path(tmp) / 'audit', steps=2)
            self.assertEqual(report['full_channels'], 45)
            self.assertEqual(report['reduced_channels'], 6)
            self.assertEqual(report['reconstructed_transitions'], 2)
            self.assertGreater(report['reconstructed_source_clicks'], 0)
            self.assertEqual(report['physics_acceptance'], 'not_established')

    def test_invalid_horizon_and_existing_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for steps in (0, 9, True, 1.0):
                with self.assertRaises(ValueError):
                    run_runtime_pair(Path(tmp) / 'never-created', steps=steps)
            self.assertFalse((Path(tmp) / 'never-created').exists())
            with self.assertRaises(ValueError):
                run_runtime_pair(Path(tmp))
