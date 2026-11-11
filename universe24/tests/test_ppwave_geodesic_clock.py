"""Exact prepared geodesic arithmetic, decoder limits, and bigint reversal."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

import numpy as np

from experiments.geometry import ppwave_geodesic_clock as gc
from universe24.core import Engine

ROOT = Path(__file__).resolve().parents[2]


class GeodesicClockTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("sympy"), "requires validation extra")
    def test_independent_continuum_geodesic_audit(self):
        from experiments.geometry.ppwave_geodesic_audit import audit
        report = audit()
        self.assertTrue(report["all_residuals_zero"])
        self.assertEqual(report["samples_compared"], 51)

    def test_long_integer_orbit_and_arbitrary_remainders(self):
        tensor = gc.build()
        seed, node = gc.prepare(tensor)
        seed.r[:] = np.arange(seed.G*seed.N).reshape(seed.G, seed.N) % 6
        engine, state = Engine(tensor), seed
        # Independent first-order integer target, including negative previous
        # history already supplied by preparation. No rounded continuum oracle.
        q, p = 1, 0
        for n in range(1, 101):
            state = engine.step(state)
            q, p = 2*q+3*p, q+2*p
            self.assertEqual(list(map(int, state.b[44:, node])), [q,p,q*p,n])
            self.assertEqual(q*q-3*p*p, 1)
            self.assertTrue(np.array_equal(state.r, seed.r))
        self.assertGreater(state.max_abs(), 2**128)
        self.assertTrue(engine.rewind(state, 100).same_as(seed))

    def test_geometry_input_is_a_face_neighbor_read(self):
        tensor = gc.build()
        seed, node = gc.prepare(tensor)
        changed = seed.copy()
        neighbor = seed.lattice.shift_index(gc.PLUS_X)[node]
        gear = tensor.gear_index("X.W01")
        changed.b[gear, neighbor] += 2
        engine = Engine(tensor)
        self.assertEqual(int(engine.step(changed).b[44,node])-int(engine.step(seed).b[44,node]), 2)
        self.assertFalse(tensor.support_violations())
        self.assertEqual(tensor.rank, 4)

    def test_preparation_and_click_failures_are_reported(self):
        controls = gc.negative_controls(gc.build())
        self.assertEqual(controls["nonbinary_curvature"]["product_defect"], -48)
        self.assertFalse(controls["naive_missing_row_decoder"]["passes"])
        case = gc.run_case(gc.build(), 1, 1, 4, 2**30)
        corrupted = [dict(row) for row in case["official_rows"]]
        corrupted[-1]["probe.product"] += 1
        with self.assertRaises(AssertionError):
            gc.decode_official(corrupted, case["initial_probe_a_b"], 1)

    def test_reproduce_checked_evidence(self):
        expected = json.loads((ROOT/"docs/evidence/ppwave_geodesic_clock.json").read_text())
        for source, digest in expected.pop("source_sha256").items():
            self.assertEqual(hashlib.sha256((ROOT/source).read_bytes()).hexdigest(), digest)
        self.assertEqual(gc.run(), expected)


if __name__ == "__main__":
    unittest.main()
