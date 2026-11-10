"""WAVE 14 registry additions (r67): builder B's QM-SHOW single X-gate with two quanta (gate.x_gate_pair_router@1) and its
experiment (exp.gate_two_quanta@1): additivity until the meeting, the recorded meeting, the mirror runs."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import symmetry as SY
from research.matter_light_blocks_v1.registry.compose import apply_control, compose, init_data
from universe24.experiments import checkpoint_data
from universe24.observation import clicks

# builder B's CLI init files (qmshow_cli.json, archived at fd49c09), harness form, T = 80
INIT_FILES = {(0, 1): "907ee87ec965133efdea4e9bb4045e544b788a9e8da5791ef827a7ed38cf5f9e",
              (5, 1): "b0f6db9982b7bec210efb74aec044452b0aa0eff9ff8944890c97b1869b1caf2"}
# E26's mirror init files: JR of the board's final state at T = 80, compact JSON and one newline
MIRROR_INIT = {(-4, 1): "15f6beef0226057329b4cd73252f7ea8399b5189bb59ee23173827da580491e8",
               (0, 1): "246a68eb84fccd39da3987c6d0d4a4c61afedd4e630727903199f4ae751066fe",
               (4, 1): "405835dfcb7a30bc11c92ded1fcd3e980fba604aca66bc802bfe00b79b3d68d7",
               (-2, -1): "8cc444ce3310b10eecba718831f9bb6421cab6f52e1b5a5e8a452892234f3a75",
               (2, -1): "9d9b8a52abab777a9518417c95fea09f0792b6aaf392b2e5a1e924f957dd5444",
               (8, -1): "41b0a25236c7b12ad64d94970382fd248dffc5239ae803090673445fde176492",
               (5, 1): "dc923f8fe484420effdbd27bfc41b9aec60e9292c2ce3766dec467aae9512191",
               (-6, -1): "1d6421519d0c702a76eaf3961dd53324c66b4708a5a6915ec3dccde1e7ac2654"}
T = 80
GATE = (*CP.TRIPLE_GATE_AT, 1)


def composed(m):
    spec = CP.x_gate_pair_spec([m])
    return compose(apply_control(spec, spec["controls"][0]))[0]


def run(engine, state):
    recs = []
    for t in range(1, T + 1):
        nxt = engine.advance(state)
        if engine.rewind(nxt) != state:
            raise ArithmeticError(t)
        recs += [(t, tuple(c.address), c.kind, c.quotient) for c in clicks(state, nxt, t)]
        state = nxt
    return state, recs


class Wave14Registry(unittest.TestCase):
    def test_builder_bs_init_files(self):
        for (D, s), sha in INIT_FILES.items():
            data = init_data(composed((D, s, True, True)), T)
            self.assertEqual(hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest(), sha)

    def test_packet_masks(self):
        p = CP.x_gate_pair_params(3, -1)
        self.assertEqual([q["lead"] for q in p["packets"]], [8, 5])                     # Q 12 before X, K 12 + D
        self.assertEqual(CP.x_gate_pair_params(3, -1, q=False)["paths"], p["paths"])     # masks keep the hardware
        self.assertEqual([q["sigma0"] for q in p["paths"] if q["name"] == "Y0"], [1])    # gauge s = -1
        self.assertEqual(CP.x_gate_pair_key(-2, -1, False, True), "D-2-_K")
        with self.assertRaises(ValueError):
            CP.x_gate_pair_params(9, 1)

    def test_union_until_the_meeting_and_the_mirror(self):
        for (D, s), sha in MIRROR_INIT.items():
            p = composed((D, s, True, True))
            xT, rb = run(p.engine, p.initial)
            mir0 = SY.time_reverse_state(xT)
            data = checkpoint_data(mir0, p.engine, 0)["experiment"]
            data["steps"] = T
            blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True) + "\n"
            self.assertEqual(hashlib.sha256(blob.encode()).hexdigest(), sha, (D, s))
            xB, rm = run(p.engine, mir0)                                                  # a second forward run
            self.assertEqual(xB, SY.time_reverse_state(p.initial))
            self.assertEqual(Counter(rm), Counter((T + 1 - t, x, (-k) % 3, -q) for t, x, k, q in rb))
            if not any(r[1] == GATE for r in rb):                                         # no meeting: exact union
                pq, pk = composed((D, s, True, False)), composed((D, s, False, True))
                rq, rk = run(pq.engine, pq.initial)[1], run(pk.engine, pk.initial)[1]
                self.assertEqual(Counter(rb), Counter(rq) + Counter(rk))


if __name__ == "__main__":
    unittest.main()
