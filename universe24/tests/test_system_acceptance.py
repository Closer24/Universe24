"""Adversarial joins must inspect saved states and preserve physical scope."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from universe24.system.runtime import run_bundle
from validation.sourced_map import native, runtime
from validation.system_acceptance.run import inspect_saved_run, inspect_claimed_run, require_same_run, run, source_hashes, _anisotropic_run


class SystemAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)
        program = native.build_native(24)
        seed = native.prepare_native(program)
        cls.path = cls.out / 'original'
        run_bundle(runtime.make_bundle(program, seed), cls.path, 3)
        changed = seed.copy()
        changed.r[0, 0] = (int(changed.r[0, 0]) + 1) % 6
        cls.changed = cls.out / 'changed'
        run_bundle(runtime.make_bundle(program, changed), cls.changed, 3)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_equal_physical_fields_do_not_authorize_complete_state_join(self):
        left, _ = inspect_saved_run(self.path)
        same, _ = inspect_saved_run(self.path)
        changed, _ = inspect_saved_run(self.changed)
        self.assertTrue(require_same_run(left, same))
        self.assertEqual(left.tensor_sha256, changed.tensor_sha256)
        first_physical = runtime.inspect_run(self.path)[0].final_rational_fields
        other_physical = runtime.inspect_run(self.changed)[0].final_rational_fields
        self.assertEqual(first_physical, other_physical)
        self.assertNotEqual(left.seed_sha256, changed.seed_sha256)
        with self.assertRaises(ValueError):
            require_same_run(left, changed)
        for field, value in (('steps', left.steps + 1), ('protocol_sha256', 'altered'),
                             ('current_source_sha256', 'stale')):
            with self.assertRaises(ValueError):
                require_same_run(left, replace(left, **{field: value}))
        with self.assertRaises(TypeError):
            require_same_run(left, dict(run_id=left.run_id))

    def test_corrupt_saved_bytes_cannot_issue_a_receipt(self):
        import shutil
        broken = self.out / 'corrupt'
        shutil.copytree(self.path, broken)
        trace = broken / 'full_trace.jsonl.gz'
        trace.write_bytes(b'not a saved complete trace')
        with self.assertRaises((ValueError, OSError, EOFError)):
            inspect_saved_run(broken)

    def test_research_summary_cannot_substitute_another_complete_run(self):
        receipt, _ = inspect_saved_run(self.path)
        claim = dict(run_id=receipt.run_id, bundle_id=receipt.bundle_id,
                     tensor_hash=receipt.tensor_sha256)
        self.assertEqual(inspect_claimed_run(self.path, claim), receipt)
        with self.assertRaises(ValueError):
            inspect_claimed_run(self.changed, claim)
        for key in claim:
            with self.assertRaises(ValueError):
                inspect_claimed_run(self.path, {**claim, key: 'incorrect'})

    def test_existing_output_is_rejected_before_any_research_runs(self):
        marker = self.out / 'retained.txt'
        marker.write_text('preserve this evidence')
        with self.assertRaises(ValueError):
            run(self.out)
        self.assertEqual(marker.read_text(), 'preserve this evidence')

    def test_provenance_includes_indirect_tensor_oracle_and_locality_sources(self):
        sources = source_hashes()
        for name in ('universe24/core/lattice.py',
                     'validation/geometry/team48/refinement_integer_projective.py',
                     'validation/completion/formulation.py',
                     'validation/research_eight/07_hyperbolic_symbol.py'):
            self.assertIn(name, sources)
            self.assertEqual(len(sources[name]), 64)

    def test_anisotropic_saved_source_metric_and_distinct_calibration(self):
        destination = self.out / 'anisotropic'
        report, receipts = _anisotropic_run(destination)
        self.assertTrue(report['exact_shared_physical_endpoint'])
        self.assertEqual([row['N'] for row in report['runs']], [24, 48, 96])
        self.assertEqual(len({receipt.tensor_sha256 for receipt in receipts}), 1)
        self.assertEqual(len({receipt.seed_sha256 for receipt in receipts}), 3)
        for row in report['runs']:
            self.assertEqual(row['saved_samples'][-1]['source_elapsed_proper_time'], '1/8')
            for sample in row['saved_samples']:
                self.assertEqual(sample['normalized_diagonal_errors'], ['0'] * 4)
                self.assertEqual(sample['off_diagonal_errors'], ['0'] * 12)
        isotropic, _ = inspect_saved_run(self.path)
        with self.assertRaises(ValueError):
            require_same_run(receipts[0], isotropic)
        with self.assertRaises(ValueError):
            require_same_run(receipts[0], receipts[1])
        with self.assertRaises(ValueError):
            _anisotropic_run(destination)


if __name__ == '__main__':
    unittest.main()
