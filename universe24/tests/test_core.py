"""Fixed-divisor-six arithmetic, reference, locality and performance tests.

Run from the repository root:
    python -m unittest universe24.tests.test_core -v
Each test writes its current measurements to runs/tests/<test>.json.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import (AcyclicityError, Engine, LocalityError, State, Tensor, TensorBuilder,
                                             build, reference_block, reference_names)
from universe24.tests.l0_oracle import REFERENCE_VACUUM_R, reference_arrays
from universe24.core.engine import OBJ
from universe24.core.lattice import DIRECTIONS, ZERO, lattice
from universe24.core.tensor import Block, reference_block_receiver_form
from universe24.tests import randgen
from universe24.tests.l0_oracle import RefEngine
from universe24.tests.l0_oracle import VACUUM, Channel, Cube, RefState
from universe24.tests.l0_oracle import ref_clicks

RESULTS = Path("runs/tests")


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True, check=True).stdout.strip()


def record(name: str, data: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    data = {"test": name, "written_utc": stamp(), **data}
    (RESULTS / f"{name}.json").write_text(json.dumps(data, indent=1, default=str) + "\n")


def ref_random_state(seed: int, L: int, lo: int, hi: int, sparse: int | None = None,
                     background: Channel = VACUUM) -> RefState:
    rng = random.Random(seed)
    cells = {}
    if sparse is None:
        for x in range(L):
            for y in range(L):
                for z in range(L):
                    for g in range(48):
                        cells[(x, y, z, g)] = Channel(rng.randint(lo, hi), rng.randint(lo, hi), rng.randint(0, 5))
    else:
        while len(cells) < sparse:
            addr = (rng.randrange(L), rng.randrange(L), rng.randrange(L), rng.randrange(48))
            ch = Channel(rng.randint(lo, hi), rng.randint(lo, hi), rng.randint(0, 5))
            if ch != background:
                cells[addr] = ch
    return RefState(Cube(L), background, cells)


T01_STATES = [  # (name, seed, lo, hi, sparse, background)
    ("dense_seed1", 1, -50, 50, None, VACUUM),
    ("dense_seed2", 2, -50, 50, None, VACUUM),
    ("dense_seed3", 3, -50, 50, None, VACUUM),
    ("dense_big2^80", 7, -2 ** 80, 2 ** 80, None, VACUUM),
    ("sparse_seed4", 4, -50, 50, 20, VACUUM),
    ("sparse_seed5", 5, -50, 50, 20, VACUUM),
    ("sparse_bg005_seed6", 6, -50, 50, 20, Channel(0, 0, 5)),
]
L01 = 5
STEPS01 = 25


def official_rows(log):
    return [((*xyz, g), k, q) for _, xyz, g, k, q, _lab in log.rows()]


def full_state_from_ref(ref: RefState) -> State:
    return State(ref.cube.side, *reference_arrays(ref))


class T01ReferenceIdentity(unittest.TestCase):
    def test_reference_block_is_reciprocal_and_matches_receiver_form(self):
        sender = build(reference_block())
        receiver = build(reference_block_receiver_form())
        self.assertEqual(sender, receiver)
        self.assertEqual(sender.census(), {"node": 0, "link": 288, "by_degree": [0, 288, 0, 0]})

    def test_T01(self):
        tensor = build(reference_block())
        eng = Engine(tensor)
        ref = RefEngine()
        out = {"L": L01, "steps": STEPS01, "states": []}
        for name, seed, lo, hi, sparse, bg in T01_STATES:
            rs = ref_random_state(seed, L01, lo, hi, sparse, bg)
            st = full_state_from_ref(rs)
            n_cmp = n_bad = n_clicks = n_click_bad = n_dropped = n_rewind_bad = 0
            for k in range(1, STEPS01 + 1):
                rs2 = ref.advance(rs)
                st2 = eng.step(st)
                a, b, r = reference_arrays(rs2)
                bad = int(np.sum(st2.a != a) + np.sum(st2.b != b) + np.sum(st2.r != r))
                n_cmp += 3 * a.size
                n_bad += bad
                mine = official_rows(eng.clicks(st, st2, k))
                theirs = [(c.address, c.kind, c.quotient) for c in ref_clicks(rs, rs2, k)]
                n_clicks += len(theirs)
                n_click_bad += 0 if mine == theirs else max(1, len(set(mine) ^ set(theirs)))
                raw = eng.clicks(st, st2, k, stream="raw")
                n_dropped += int(np.sum(~raw.changed))
                back = eng.inverse_step(st2)
                ref_back = full_state_from_ref(ref.rewind(rs2))
                n_rewind_bad += 0 if (back.same_as(st) and back.same_as(ref_back)) else 1
                rs, st = rs2, st2
            out["states"].append({"name": name, "component_comparisons": n_cmp, "mismatches": n_bad,
                                  "official_clicks": n_clicks, "click_step_mismatches": n_click_bad,
                                  "raw_rows_dropped_as_unchanged": n_dropped,
                                  "inverse_vs_rewind_mismatches": n_rewind_bad})
            self.assertEqual(n_bad, 0, name)
            self.assertEqual(n_click_bad, 0, name)
            self.assertEqual(n_rewind_bad, 0, name)
        out["engine_stats"] = eng.stats
        record("T0.1", out)
        self.assertGreater(eng.stats["pyint_steps"], 0)   # the 2^80 state used the Python-int path

    def test_T01_fixed_point_row(self):
        """a = b = 1 with six +1 inputs: ell = 2 but the triple is unchanged -> no official click (universe24 rule)."""
        tensor = build(reference_block())
        eng = Engine(tensor)
        from universe24.algebra.coupling import Coupling
        c = Coupling((1, 1, 1))
        L, y, h = 5, (1, 1, 3), 0
        cells = {(*y, h): Channel(1, 1, 2)}
        for d, e in enumerate(DIRECTIONS):
            if c.weights[d][h] != 1:
                self.skipTest("needs +1 weights")
            nb = tuple((y[i] + e[i]) % L for i in range(3))
            cells[(*nb, c.ports[d][h])] = Channel(0, 1, 2)
        rs = RefState(Cube(L), VACUUM, cells)
        rs2 = RefEngine().advance(rs)
        st = full_state_from_ref(rs)
        st2 = eng.step(st)
        n = lattice(L).index(*y)
        self.assertEqual(st2.gear(h, n), (1, 1, 2))
        theirs = [(cl.address, cl.kind, cl.quotient) for cl in ref_clicks(rs, rs2, 1)]
        mine = official_rows(eng.clicks(st, st2, 1))
        raw = [(row, ch) for row, ch in zip(official_rows(eng.clicks(st, st2, 1, "raw")),
                                             eng.clicks(st, st2, 1, "raw").changed)]
        self.assertEqual(mine, theirs)
        self.assertNotIn(((*y, h), 0, 2), mine)
        self.assertIn((((*y, h), 0, 2), False), raw)
        record("T0.1_fixed_point", {"address": [*y, h], "after": st2.gear(h, n), "official_rows": len(mine),
                                    "universe24_rows": len(theirs), "raw_row_present_unchanged": True})


class T02FixedDivisor(unittest.TestCase):
    def test_fixed_divisor_and_roundtrip(self):
        tensor = build(reference_block())
        engine = Engine(tensor)
        self.assertEqual(engine.D, 6)
        self.assertFalse(hasattr(engine, "Q"))
        self.assertFalse(hasattr(tensor, "Q"))
        with self.assertRaises(TypeError):
            Engine(tensor, 2)
        self.assertEqual(Tensor.from_json(tensor.to_json()), tensor)
        self.assertNotIn("Q", tensor.to_dict())
        with self.assertRaises(ValueError):
            Tensor.from_dict(dict(tensor.to_dict(), Q=1))
        from universe24.core.engine import extract_clicks, handedness_kind
        state = engine.vacuum(3, [2] * tensor.G)
        with self.assertRaises(ValueError):
            extract_clicks(tensor, 12, state, state)
        with self.assertRaises(ValueError):
            handedness_kind(np.array([0, 2, 4]), 12)

    def test_legacy_nonunit_law_is_rejected(self):
        tensor = build(reference_block())
        legacy = tensor.to_dict()
        legacy["format"] = "metric_variant_v1/tensor/1"
        legacy["Q"] = 1
        self.assertEqual(Tensor.from_dict(legacy), tensor)
        for scale in (None, 0, 2, True, 8589934593):
            with self.subTest(scale=scale), self.assertRaises(ValueError):
                Tensor.from_dict(dict(legacy, Q=scale))
        del legacy["Q"]
        with self.assertRaises(ValueError):
            Tensor.from_dict(legacy)


def _nonlinear_subtensor(tensor: Tensor) -> Tensor:
    return Tensor(tensor.gears, [m for m in tensor.monomials if m.degree >= 2])


class T03ExactRewind(unittest.TestCase):
    def _run(self, tensor, s0, steps):
        eng = Engine(tensor)
        hist = eng.run(s0, steps, history=True)
        ell_nonzero = 0
        for k in range(steps):
            ell_nonzero += int(np.sum(hist[k + 1].b + hist[k].a != 0))
        back_bad = 0
        s = hist[-1]
        for k in range(steps, 0, -1):
            s = eng.inverse_step(s)
            if not s.same_as(hist[k - 1]):
                back_bad += 1
        nl = Engine(_nonlinear_subtensor(tensor))
        nl_nonzero = sum(int(np.sum(nl.inputs(h) != 0)) for h in hist[:: max(1, steps // 5)])
        return eng, hist, s, ell_nonzero, back_bad, nl_nonzero

    def test_T03_random(self):
        out = {"divisor": 6, "steps": 5, "runs": []}
        for seed in range(10, 16):
            L = (4, 5, 6)[(seed - 10) % 3]
            for fam, a_reads in (("A_b_only", False), ("B_a_reads", True)):
                tensor = build(randgen.random_tensor_block(seed, G=6, a_reads=a_reads))
                self.assertEqual(tensor.b_only, not a_reads)
                s0 = randgen.random_state(1000 + seed, tensor.G, L, 6, -2, 2)
                eng, hist, s, ell_nz, back_bad, nl_nz = self._run(tensor, s0, 5)
                row = {"seed": seed, "family": fam, "L": L, "monomials": len(tensor), "rank": tensor.rank,
                       "stages": len(tensor.stages), "returned_exactly": s.same_as(s0),
                       "inverse_step_mismatches": back_bad, "ell_nonzero_events": ell_nz,
                       "nonlinear_nonzero_values": nl_nz, "max_abs_seen": max(h.max_abs() for h in hist),
                       "stats": dict(eng.stats)}
                out["runs"].append(row)
                self.assertTrue(row["returned_exactly"], row)
                self.assertEqual(back_bad, 0, row)
                self.assertGreater(ell_nz, 0, row)
                self.assertGreater(nl_nz, 0, row)
                if a_reads:
                    self.assertGreater(len(tensor.stages), 1)
        record("T0.3", out)

    def test_T03_bigint_and_guard_switch(self):
        out = {"cases": []}
        # (a) |a|, |b| ~ 2^70, degree-3 tensor with a-reads: Python-int path, 6 forward + 6 back
        tensor = build(randgen.random_tensor_block(31, G=5, a_reads=True))
        s0 = randgen.random_state(2031, tensor.G, 4, 6, -2 ** 70, 2 ** 70)
        eng, hist, s, ell_nz, back_bad, nl_nz = self._run(tensor, s0, 6)
        out["cases"].append({"case": "bigint_2^70", "returned_exactly": s.same_as(s0), "inverse_step_mismatches":
                             back_bad, "max_bits": max(h.max_abs() for h in hist).bit_length(), "stats": eng.stats})
        self.assertTrue(s.same_as(s0))
        self.assertEqual(back_bad, 0)
        self.assertEqual(eng.stats["int64_steps"], 0)
        # (b) Cubic growth from small values crosses the int64 limit mid-run: 8 forward + 8 back
        tensor = build(randgen.random_tensor_block(32, G=5, a_reads=True, small=5))
        s0 = randgen.random_state(2032, tensor.G, 4, 6, -3, 3)
        eng, hist, s, ell_nz, back_bad, nl_nz = self._run(tensor, s0, 8)
        out["cases"].append({"case": "divisor_six_cubic_crossing", "returned_exactly": s.same_as(s0),
                             "inverse_step_mismatches": back_bad,
                             "max_bits_per_step": [h.max_abs().bit_length() for h in hist], "stats": eng.stats})
        self.assertTrue(s.same_as(s0))
        self.assertEqual(back_bad, 0)
        self.assertGreater(eng.stats["int64_steps"], 0)
        self.assertGreater(eng.stats["pyint_steps"], 0)
        record("T0.3_extra", out)


class T04Mirror(unittest.TestCase):
    def test_T04(self):
        out = {"divisor": 6, "n": 5, "runs": []}
        for seed in range(20, 25):
            L = (4, 5, 6)[(seed - 20) % 3]
            tensor = build(randgen.random_tensor_block(seed, G=6, a_reads=False))
            self.assertTrue(tensor.b_only)
            eng = Engine(tensor)
            s0 = randgen.random_state(3000 + seed, tensor.G, L, 6, -2, 2)
            hist = eng.run(s0, 5, history=True)
            s = eng.run(eng.mirror(hist[-1]), 5)
            s = eng.mirror(s)
            fmf_bad = sum(0 if eng.step(eng.mirror(eng.step(h))).same_as(eng.mirror(h)) else 1 for h in hist)
            row = {"seed": seed, "L": L, "monomials": len(tensor), "MFnMFn_identity": s.same_as(s0),
                   "FMF_eq_M_failures": fmf_bad, "visited_states": len(hist)}
            out["runs"].append(row)
            self.assertTrue(row["MFnMFn_identity"], row)
            self.assertEqual(fmf_bad, 0, row)
        record("T0.4", out)


class T05Locality(unittest.TestCase):
    def _tb(self):
        tb = TensorBuilder()
        for n in ("p", "q", "s"):
            tb.gear(n)
        return tb

    def test_T05(self):
        ex, ey = (1, 0, 0), (0, 1, 0)
        rejects = {
            "edge_offset_(1,1,0)": ("p", 1, ("q", (1, 1, 0), "b")),
            "diagonal_offset_(1,1,1)": ("p", 1, ("q", (1, 1, 1), "b")),
            "offset_(2,0,0)": ("p", 1, ("q", (2, 0, 0), "b")),
            "three_nodes_+ex_+ey": ("p", 1, ("q", ex, "b"), ("s", ey, "b")),
            "three_nodes_+ex_-ex": ("p", 1, ("q", ex, "b"), ("s", (-1, 0, 0), "b")),
            "three_nodes_degree3": ("p", 1, ("q", ZERO, "b"), ("s", (0, 0, 1), "b"), ("q", (0, -1, 0), "a")),
            "four_factors": ("p", 1, ("q", ZERO, "b"), ("s", ZERO, "b"), ("q", ZERO, "b"), ("s", ZERO, "b")),
            "unknown_gear": ("p", 1, ("zz", ZERO, "b")),
            "bad_field": ("p", 1, ("q", ZERO, "r")),
            "float_coefficient": ("p", 1.0, ("q", ZERO, "b")),
            "bool_coefficient": ("p", True, ("q", ZERO, "b")),
        }
        results = {}
        for name, (t, c, *facs) in rejects.items():
            tb = self._tb()
            with self.assertRaises((LocalityError, ValueError, TypeError), msg=name) as cm:
                tb.term(t, c, *facs)
            results[name] = f"REJECTED ({type(cm.exception).__name__})"
            with self.assertRaises((LocalityError, ValueError, TypeError), msg=name):
                Tensor(["p", "q", "s"], [(t, c, tuple(facs))])
        for name, mons in {"a_read_self_loop": [("p", 1, (("p", ZERO, "a"),))],
                           "a_read_self_loop_on_link": [("p", 1, (("p", ex, "a"),))],
                           "a_read_2_cycle": [("p", 1, (("q", ZERO, "a"),)), ("q", 1, (("p", ey, "a"),))]}.items():
            with self.assertRaises(AcyclicityError, msg=name):
                Tensor(["p", "q", "s"], mons)
            results[name] = "REJECTED (AcyclicityError)"
        accepts = {"constant": ("p", 3), "on_site_deg1": ("p", 2, ("q", ZERO, "b")),
                   "on_site_deg3_with_a": ("p", -1, ("q", ZERO, "b"), ("s", ZERO, "a"), ("q", ZERO, "b"))}
        for d, e in enumerate(DIRECTIONS):
            accepts[f"link_{d}_deg1"] = ("p", 1, ("q", e, "b"))
            accepts[f"link_{d}_deg2_mixed"] = ("p", 1, ("q", e, "b"), ("s", ZERO, "b"))
            accepts[f"link_{d}_deg3_all_on_neighbour"] = ("s", 5, ("q", e, "b"), ("p", e, "a"), ("q", e, "b"))
        for name, (t, c, *facs) in accepts.items():
            tb = self._tb()
            tb.term(t, c, *facs)
            T = tb.build()
            results[name] = f"ACCEPTED (stages={len(T.stages)})"
        # a-read acyclic chain is accepted and staged
        T = Tensor(["p", "q", "s"], [("q", 1, (("p", ZERO, "a"),)), ("s", 1, (("q", ex, "a"), ("p", ex, "b")))])
        self.assertEqual(T.stages, ((0,), (1,), (2,)))
        results["a_read_chain_p_q_s"] = f"ACCEPTED (stages={T.stages})"
        record("T0.5", {"cases": results})


class T06Vacuum(unittest.TestCase):
    L, STEPS = 5, 100

    def _system(self, seed, deviation):
        ref = reference_block()
        new, back = randgen.coupled_new_block(seed, reference_names(), deviation=deviation)
        tensor = build(ref, new, Block((), tuple(back)))
        self.assertFalse(tensor.has_constant)
        return tensor, new

    def _r0(self, seed, tensor):
        rng = random.Random(seed)
        D = 6
        return {n: (REFERENCE_VACUUM_R if n.startswith("R") else rng.randrange(D)) for n in tensor.names}

    def test_T06a_vacuum(self):
        tensor, new = self._system(61, deviation=False)
        eng = Engine(tensor)
        s0 = eng.vacuum(self.L, self._r0(161, tensor))
        s = s0
        ref = RefEngine()
        rs = RefState(Cube(self.L))
        changed = clicks_new = raw_new = refbad = 0
        new_idx = np.array([tensor.gear_index(g.name) for g in new.gears])
        for k in range(1, self.STEPS + 1):
            s2 = eng.step(s)
            rs = ref.advance(rs)
            changed += 0 if s2.same_as(s0) else 1
            off = eng.clicks(s, s2, k)
            raw = eng.clicks(s, s2, k, "raw")
            clicks_new += int(np.isin(off.gear, new_idx).sum())
            raw_new += int(np.isin(raw.gear, new_idx).sum())
            a, b, r = reference_arrays(rs)
            refbad += int(np.sum(s2.a[:48] != a) + np.sum(s2.b[:48] != b) + np.sum(s2.r[:48] != r))
            s = s2
        out = {"divisor": 6, "L": self.L, "steps": self.STEPS, "G": tensor.G, "monomials": len(tensor),
               "steps_with_any_change": changed, "official_clicks_new": clicks_new, "raw_rows_new": raw_new,
               "reference_mismatches_vs_universe24": refbad}
        record("T0.6a", out)
        self.assertEqual(changed, 0)
        self.assertEqual(clicks_new + raw_new, 0)
        self.assertEqual(refbad, 0)

    def test_T06b_deviation_form(self):
        tensor, new = self._system(62, deviation=True)
        eng = Engine(tensor)
        rs = ref_random_state(62, self.L, -20, 20)
        r0 = self._r0(162, tensor)
        vac = eng.vacuum(self.L, r0)
        a, b, r = reference_arrays(rs)
        A, B, R = vac.a.astype(OBJ), vac.b.astype(OBJ), vac.r.astype(OBJ)
        A[:48], B[:48], R[:48] = a, b, r
        s = State(self.L, A, B, R)
        new_idx = np.array([tensor.gear_index(g.name) for g in new.gears])
        ref = RefEngine()
        newbad = clicks_new = raw_new = refbad = ref_clicks_total = 0
        for k in range(1, self.STEPS + 1):
            s2 = eng.step(s)
            rs = ref.advance(rs)
            newbad += int(np.sum(s2.a[new_idx] != 0) + np.sum(s2.b[new_idx] != 0)
                          + np.sum(s2.r[new_idx] != vac.r[new_idx]))
            off = eng.clicks(s, s2, k)
            raw = eng.clicks(s, s2, k, "raw")
            clicks_new += int(np.isin(off.gear, new_idx).sum())
            raw_new += int(np.isin(raw.gear, new_idx).sum())
            ref_clicks_total += len(off)
            a, b, r = reference_arrays(rs)
            refbad += int(np.sum(s2.a[:48] != a) + np.sum(s2.b[:48] != b) + np.sum(s2.r[:48] != r))
            s = s2
        out = {"divisor": 6, "L": self.L, "steps": self.STEPS, "G": tensor.G, "monomials": len(tensor),
               "new_gear_component_deviations": newbad, "official_clicks_new": clicks_new, "raw_rows_new": raw_new,
               "reference_mismatches_vs_universe24": refbad, "reference_official_clicks": ref_clicks_total}
        record("T0.6b", out)
        self.assertEqual(newbad, 0)
        self.assertEqual(clicks_new + raw_new, 0)
        self.assertEqual(refbad, 0)
        self.assertGreater(ref_clicks_total, 0)


class T07Performance(unittest.TestCase):
    def test_T07(self):
        L, warm, timed = 16, 3, int(os.environ.get("MV1_T07_STEPS", "40"))
        tensor = build(reference_block(), randgen.perf_new_block(71, reference_names()))
        eng = Engine(tensor)
        rs = ref_random_state(71, L, -20, 20)
        a, b, r = reference_arrays(rs)
        new = randgen.random_state(171, 32, L, 6, -2, 2)
        s0 = State(L, np.concatenate([a, new.a.astype(OBJ)]), np.concatenate([b, new.b.astype(OBJ)]),
                   np.concatenate([r, new.r.astype(OBJ)]))
        s = eng.run(s0, warm)
        start_state = s
        t0 = time.perf_counter()
        s = eng.run(s, timed)
        dt = time.perf_counter() - t0
        stats = dict(eng.stats)
        back = eng.rewind(s, timed)
        out = {"divisor": 6, "L": L, "gears_per_node": tensor.G, "monomials": len(tensor), "rank": tensor.rank,
               "timed_updates": timed, "seconds": dt, "updates_per_second": timed / dt,
               "gear_updates_per_second": timed * tensor.G * L ** 3 / dt, "forward_stats": stats,
               "max_abs_end": s.max_abs(), "rewind_exact": back.same_as(start_state),
               "threads_env": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                                              "MKL_NUM_THREADS")}}
        record("T0.7", out)
        self.assertEqual(stats["int64_steps"] + stats["pyint_steps"], warm + timed)
        self.assertGreater(stats["int64_steps"], 0)
        # The fixed-six law can outgrow int64. Promotion preserves the exact
        # trajectory; an old large-divisor stability claim does not apply.
        if s.max_abs() > np.iinfo(np.int64).max:
            self.assertGreater(stats["pyint_steps"], 0)
        self.assertTrue(out["rewind_exact"])
        print(f"\nT0.7: {out['updates_per_second']:.2f} updates/s, "
              f"{out['gear_updates_per_second']:.3e} gear-updates/s (L={L}, G={tensor.G}, M={len(tensor)})")


if __name__ == "__main__":
    unittest.main()
