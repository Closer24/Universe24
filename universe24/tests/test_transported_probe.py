"""Transport, independent continuum checks, negative controls, and exact replay."""
import importlib.util
import json
import unittest

import numpy as np

from universe24.core import Engine
from universe24.layers.transported_probe import build, CLOCKS
from universe24.prepare.transported_probe import prepare
from universe24.observe.transported_probe import sample, assess
from experiments.geometry.transported_probe_clock import execute, run, replay, seam_control


class TransportedProbeTests(unittest.TestCase):
    def test_closed_form_transport_and_clock_cycles(self):
        tensor = build()
        self.assertEqual((tensor.G, tensor.rank, tensor.b_only), (26, 4, True))
        self.assertFalse(tensor.support_violations())
        # Exact closed finite orbits, independent of production recurrence.
        phases = {"control": [(1,0), (0,1), (-1,0), (0,-1)],
                  "candidate": [(1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)]}
        for amplitude in (1, 2**90+7):
            seed = prepare(tensor, curvature=1, amplitude=amplitude)
            # Divisible inputs preserve every allowed remainder, including odd ones.
            seed.r[:] = np.arange(seed.G*seed.N).reshape(seed.G, seed.N) % 6
            engine, state = Engine(tensor), seed
            for step in range(25):
                obs = sample(state, tensor, step)
                self.assertEqual(obs["board_xyz"], [2,2,((step+1)//2) % 5])
                self.assertEqual(obs["bank"], "Y" if step % 2 else "X")
                for clock in CLOCKS:
                    phase = phases[clock][(step//2) % len(phases[clock])]
                    self.assertEqual(obs["clock_phases"][clock], [amplitude*v for v in phase])
                self.assertTrue(np.array_equal(state.r, seed.r))
                if step < 24:
                    state = engine.step(state)
            self.assertTrue(engine.rewind(state, 24).same_as(seed))

    def test_joint_metric_gate_rejects_off_axis(self):
        report = run(macrosteps=12)
        self.assertFalse(report["common_metric_validated"])
        flat, flat_offset, axis, off_axis, other_axis = [c["assessment"] for c in report["cases"]]
        for case in (flat, flat_offset, axis):
            self.assertTrue(case["common_metric_passes"])
        self.assertTrue(axis["nonflat_at_probe"])
        for case in (off_axis, other_axis):
            self.assertTrue(case["actual_board_transport"])
            self.assertFalse(case["geodesic_matches"])
            self.assertFalse(case["common_metric_passes"])
        self.assertEqual(off_axis["predicted_proper_rate_squared"], {"numerator":1,"denominator":4})
        self.assertEqual(off_axis["clocks"]["candidate"]["measured_rate_squared"][0], {"numerator":3,"denominator":1})
        self.assertFalse(off_axis["clocks"]["control"]["matches_metric"])
        self.assertTrue(other_axis["clocks"]["candidate"]["insufficient_ticks"])
        # Full exported evidence is replayable and detects corruption.
        saved = json.loads(json.dumps(report))
        self.assertTrue(replay(saved)["exact"])
        saved["cases"][0]["state_sha256"][-1] = "corrupt"
        with self.assertRaisesRegex(ValueError, "state_sha256"):
            replay(saved)

    def test_geometry_changes_clock_with_identical_complete_packet_seed(self):
        tensor = build()
        flat = prepare(tensor, curvature=0, x=1)
        curved = prepare(tensor, curvature=1, x=1)
        # Deliberately use identical (a,b,r) for every non-geometric channel.
        for field in ("a", "b", "r"):
            getattr(curved, field)[16:] = getattr(flat, field)[16:]
        engine = Engine(tensor)
        a, b = engine.step(flat), engine.step(curved)
        self.assertFalse(np.array_equal(a.b[22:], b.b[22:]))
        self.assertTrue(np.array_equal(a.b[16:22], b.b[16:22]))
        self.assertTrue(engine.inverse_step(b).same_as(curved))

    def test_seams_off_preparation_and_insufficient_samples(self):
        tensor = build()
        seed = prepare(tensor)
        seam = seam_control(seed, tensor)
        self.assertEqual(seam["interior_nonzero_laplacians"], 0)
        self.assertGreater(seam["seam_nonzero_laplacians"], 0)
        short = execute(tensor, seed, 2)["assessment"]
        self.assertFalse(short["common_metric_passes"])
        bad = seed.copy()
        bad.a[tensor.gear_index("probe.X"), 0] += 1
        following = Engine(tensor).step(bad)
        with self.assertRaises(ValueError):
            sample(following, tensor, 1)
        self.assertTrue(Engine(tensor).inverse_step(following).same_as(bad))
        # Static coframe preparation is essential; a mismatch gives exact drift.
        drifting = seed.copy()
        gear = tensor.gear_index("E11")
        drifting.a[gear] -= 1
        after = Engine(tensor).run(drifting, 8)
        self.assertTrue(np.array_equal(after.b[gear], seed.b[gear]+8))
        self.assertTrue(Engine(tensor).rewind(after, 8).same_as(drifting))

    @unittest.skipUnless(importlib.util.find_spec("sympy"), "requires validation extra")
    def test_independent_metric_to_christoffel_and_clock_norm(self):
        import sympy as s
        t, x, y, z, c = s.symbols("t x y z c", real=True)
        coords = (t,x,y,z)
        ell = s.Matrix([1,0,0,-1])
        g = s.diag(-1,1,1,1) + 2*c*(x*x-y*y)*ell*ell.T
        inverse, v = g.inv(), s.Matrix([2,0,0,1])
        residual = []
        for mu in range(4):
            value = sum(inverse[mu,d]*(s.diff(g[d,b], coords[a])+s.diff(g[d,a], coords[b])
                        -s.diff(g[a,b], coords[d]))*v[a]*v[b]/2
                        for d in range(4) for a in range(4) for b in range(4))
            residual.append(s.simplify(value))
        self.assertEqual(residual, [0,-2*c*x,2*c*y,0])
        self.assertEqual(s.expand((v.T*g*v)[0]), -3+2*c*x*x-2*c*y*y)
        # Compare observer residuals against the independent continuum expressions.
        tensor = build()
        for curvature,x0,y0 in ((0,1,0),(1,0,0),(1,1,0),(1,0,1)):
            state = prepare(tensor, curvature=curvature, x=x0, y=y0)
            actual = assess(state, tensor, [sample(state,tensor,0)])
            expected = [int(value.subs({c:curvature,x:x0,y:y0})) if hasattr(value,"subs") else value for value in residual]
            self.assertEqual(actual["transverse_geodesic_residual"],
                             [{"numerator":v,"denominator":1} for v in expected])


if __name__ == "__main__":
    unittest.main()
