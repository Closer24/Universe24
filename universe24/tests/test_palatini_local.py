"""Restricted Palatini experiment: exact geometry and explicit failure controls."""
import hashlib
import json
from pathlib import Path
import unittest

import numpy as np

from validation.geometry import ppwave_palatini_local as pp
from universe24.core import Engine

ROOT = Path(__file__).resolve().parents[2]


class PalatiniLocalTests(unittest.TestCase):
    def test_arbitrary_remainders_preserve_macro_encoding(self):
        tensor = pp.build()
        seed, _ = pp.prepare(tensor, L=5, P=256)
        seed.r[:] = np.arange(seed.G*seed.N).reshape(seed.G, seed.N) % 6
        engine = Engine(tensor)
        after = engine.run(seed, 2)
        shifted = seed.lattice.shift_index(pp.MINUS_Z)
        self.assertTrue(np.array_equal(after.b[:44], seed.b[:44, shifted]))
        self.assertTrue(np.array_equal(after.a[:44], seed.a[:44, shifted]))
        self.assertTrue(np.array_equal(after.r, seed.r))
        self.assertTrue(engine.rewind(after, 2).same_as(seed))

    def test_large_integer_seed_and_nonharmonic_ricci(self):
        tensor = pp.build()
        P, L = 2**70, 5
        seed, preparation = pp.prepare(tensor, L, P, "nonharmonic")
        engine = Engine(tensor)
        h = [seed]
        for _ in range(4):
            h.append(engine.step(h[-1]))
        E, T2, R2, palatini = pp.cartan(h[0], h[2], h[4], P)
        _, ricci, normal, momentum = pp.exact_inverse_metric_and_ricci(E, R2, P)
        coords = seed.lattice.all_coords()
        bulk = np.array([0 < x < L-1 and 0 < y < L-1 for x,y,z in coords])
        A = np.array(preparation["profile_A"], dtype=object)[(coords[:,2]-1) % L]
        expected = -8*P**3*A[:,None,None]*np.outer(pp.NULL, pp.NULL)
        self.assertTrue(np.array_equal(ricci[bulk], expected[bulk]))
        self.assertTrue(np.array_equal(normal[bulk], (-16*P**8*A)[bulk]))
        self.assertTrue(np.array_equal(momentum[bulk,2], (16*P**7*A)[bulk]))
        self.assertEqual(pp.peak(T2[bulk]), 0)
        self.assertGreater(pp.peak(palatini[bulk]), 0)
        self.assertTrue(engine.rewind(h[-1], 4).same_as(seed))

    def test_reproduce_local_report(self):
        expected = json.loads((ROOT/"docs/evidence/ppwave_palatini_local.json").read_text())
        self.assertEqual(expected.pop("source_sha256"),
                         hashlib.sha256(Path(pp.__file__).read_bytes()).hexdigest())
        self.assertEqual(pp.run(), expected)


if __name__ == "__main__":
    unittest.main()
