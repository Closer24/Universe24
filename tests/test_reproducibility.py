"""Evidence validation must reject ambiguity and must never rewrite old runs."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from research.reproducibility.bundle import (ROOT, canonical, compare_bundles, digest,
    first_difference, read_json, validate, validate_named, write_json)
from research.reproducibility.run import check_engine, checked_case, negative_claim, run
import time


class ReproducibilityTests(unittest.TestCase):
    def test_versioned_protocol_and_engine_pin(self):
        p = read_json(ROOT / 'research/reproducibility/protocol.json')
        validate_named(p, 'protocol')
        self.assertEqual(check_engine()['engine_commit'], p['base_engine_commit'])
        for edit in ({'schema_version': 2}, {'budget_wall_seconds': True}, {'extra': 1}, {'budget_wall_seconds': 601}):
            bad = {**p, **edit}
            with self.assertRaises(ValueError):
                validate_named(bad, 'protocol')
        duplicate = deepcopy(p)
        duplicate['cases'].append(deepcopy(duplicate['cases'][0]))
        with self.assertRaises(ValueError):
            validate_named(duplicate, 'protocol')
        bad = deepcopy(p)
        del bad['observation']
        with self.assertRaises(ValueError):
            validate_named(bad, 'protocol')

    def test_json_validation_is_explicit_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'result.json'
            write_json(path, {'a': 1})
            with self.assertRaises(FileExistsError):
                write_json(path, {'a': 2})
            self.assertEqual(read_json(path), {'a': 1})
            for text in ('{"a":1,"a":2}', '{"a":NaN}', '{'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    read_json(path)
        with self.assertRaises(ValueError):
            validate(1, {'type': 'integer', 'unsupported_constraint': True})

    def test_exact_comparison_reports_structure_and_large_integers(self):
        x = {'state': [10**100, -10**100, 5]}
        self.assertEqual(digest(x), digest(json.loads(json.dumps(x))))
        y = deepcopy(x)
        y['state'][0] += 1
        self.assertEqual(first_difference(x, y)['path'], '$.state[0]')
        self.assertIsNotNone(first_difference({'x': 1}, {'x': True}))
        self.assertIsNone(first_difference(x, deepcopy(x)))

    def test_negative_result_is_not_an_execution_failure(self):
        result = negative_claim()
        self.assertEqual(result['scientific_outcome'], 'refuted')
        self.assertEqual(result['observed_delta_Q'], -8)
        self.assertTrue(result['implementation_check_pass'])

    def test_frozen_example_periods(self):
        protocol = read_json(ROOT / 'research/reproducibility/protocol.json')
        with tempfile.TemporaryDirectory() as tmp:
            for case in protocol['cases']:
                result, _ = checked_case(case, Path(tmp) / case['id'], time.monotonic() + 30)
                self.assertTrue(result['pass'], result)
                self.assertEqual(result['first_full_state_return'], case['expected_first_return'])

    def test_bundle_comparison_preserves_source_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            run(a, allow_dirty=True, skip_tests=True)
            run(b, allow_dirty=True, skip_tests=True)
            self.assertIsNone(compare_bundles(a,b))
            trace = b/'cases/positive_impulse/trace.jsonl'
            original = trace.read_text()
            trace.write_text('{"t":99,"t":0}\n')
            with self.assertRaises(ValueError):
                compare_bundles(a,b)
            trace.write_text(original)
            result = read_json(b/'result.json')
            bad = {**result, 'execution_status':'error'}
            with self.assertRaises(ValueError):
                validate_named(bad, 'result')
            bad = {**result, 'scope':'full'}
            with self.assertRaises(ValueError):
                validate_named(bad, 'result')
            bad = {**result, 'cases':[]}
            with self.assertRaises(ValueError):
                validate_named(bad, 'result')
            final = b/'cases/positive_impulse/final.json'
            checkpoint = read_json(final); checkpoint['completed_steps'] += 1
            final.write_text(json.dumps(checkpoint))
            self.assertEqual(compare_bundles(a,b)['file'],'cases/positive_impulse/final.json')
            manifest = read_json(b/'manifest.json')
            key = next(iter(manifest['source_sha256']))
            manifest['source_sha256'][key] = '0'*64
            (b/'manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(compare_bundles(a,b)['file'],'manifest.json')


if __name__ == '__main__':
    unittest.main()
