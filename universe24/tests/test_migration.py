"""Complete-state regression against ONE before the repository migration.

Fixtures were captured at d73f78e827e3d7b15c06f729c52fa3c2cc241ed2,
with the original package path, before any restructuring. Every hash covers
all a,b,r values, not only clicks or a plotted observable.
"""
import hashlib
import json
from pathlib import Path
import unittest
from universe24.demos.one.run_one import build


def digest(state):
    h = hashlib.sha256()
    for arr in (state.a, state.b, state.r):
        h.update(','.join(str(int(v)) for v in arr.ravel()).encode())
    return h.hexdigest()


class TestMigration(unittest.TestCase):
    def test_default_full_state_traces(self):
        fixtures = json.loads((Path(__file__).parent / 'fixtures/one_before_migration.json').read_text())
        for row in fixtures:
            with self.subTest(L=row['L'], seed=row['seed']):
                system, tensor, engine, state, _ = build(row['L'], 'jpure', row['seed'])
                initial = state.copy()
                self.assertEqual(tensor.dynamics_fingerprint, row['dynamics'])
                self.assertEqual((tensor.G, len(tensor), len(tensor.designations)),
                                 (row['G'], row['terms'], row['designations']))
                actual = [digest(state)]
                for _ in row['hashes'][1:]:
                    state = engine.step(state)
                    actual.append(digest(state))
                self.assertEqual(actual, row['hashes'])
                self.assertTrue(engine.rewind(state, len(actual)-1).same_as(initial))
