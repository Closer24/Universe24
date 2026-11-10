"""WAVE 11 registry additions (r67): builder D QM-3's device CC8 (select.escort_lattice_router@1), CC7-M's hardware with
one elementary quantum and two escorts in flight on an 8-update lattice, and its ensemble (exp.one_quantum_one_exit@1)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry.compose import apply_control, compose, init_data
from universe24.observation import clicks

# SHA-256 of builder D's representative init files (qm3.py in research/matter_light_v1/remote/builderD_QMA_final,
# archived at 6c0798c; results/qm3.json "init_sha"; reproduced by fresh machine 2, QM-F4 (h)), which cc8_spec writes byte
# for byte in the harness's form (indent 1, one newline)
INIT_FILES = {(6, 8): "709a16519d6a59e5ec3ae68925ac47d6274636b02420bb83bef77c0d3f75f9fb",
              (70, 8): "026cb29dc98ef37f20348b9f7331602dc056d5c77d645f067c2fc91436ae4f27"}
# N_B = the number of the 14 hidden phases with exit B, per device phase D' (builder D QM-3; fresh machine 2 QM-F4 (g))
N_B = dict(zip((1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16), (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13)))
EXIT_B = {(x, 128, 128) for x in range(130, 135)}                 # the declared exits (E22's detectors.json)
EXIT_C = {(128, y, 128) for y in range(130, 136)}


def composed(spec, control=None):
    if control is not None:
        spec = apply_control(spec, next(c for c in spec["controls"] if c["name"] == control))
    prepared, rep = compose(spec)
    bad = [k for k, v in rep.items() if k.endswith("_ok") and not v]
    if bad:
        raise AssertionError(f"{spec['id']}: assertions failed {bad}")
    return prepared


class Wave11Registry(unittest.TestCase):
    def test_representatives_are_builder_ds_init_files(self):
        for (tau, d), sha in INIT_FILES.items():
            spec = CP.cc8_spec([(tau, d)])
            self.assertEqual([q["block"] for q in spec["placements"]], ["guide_net@1"])
            self.assertEqual(spec["steps"], 2100)
            data = init_data(composed(spec), spec["steps"])
            self.assertEqual(hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest(), sha)
            self.assertEqual(CP.cc8_spec([(tau, d)], 512)["placements"], spec["placements"])   # 2L: X at the same site

    def test_one_hardware_three_quanta(self):
        base = CP.cc8_router_placement("cc8", CP.CC7M_AT, 6, 1)["params"]
        for d in CP.CC8_ESCORT_C:
            for tau in CP.CC8_QUANTUM:
                p = CP.cc8_router_placement("cc8", CP.CC7M_AT, tau, d)["params"]
                self.assertEqual(p["paths"], base["paths"])                # the hardware depends on no datum
                self.assertEqual([q["f"] for q in p["packets"]], [[1, -1]] * 3)
                self.assertEqual([q["path"].lstrip("~") for q in p["packets"]], ["A", "eB_lo", "eC_lo"])
                self.assertEqual(p["packets"][1], base["packets"][1])      # escort B never changes
        members = [(6, 1), (70, 8), (118, 16)]
        spec = CP.cc8_spec(members)
        for tau, d in members:                                            # the controls are packet masks
            st = composed(spec, f"tau{tau}_D{d}").initial
            self.assertEqual(st, composed(CP.cc8_spec([(tau, d)])).initial)
            self.assertEqual(max(max(abs(v.a), abs(v.b)) for v in st.cells.values()), 1)   # unit quanta
            X = CP.CC7M_AT                                                # the doors are vacuum (gap nodes)
            self.assertFalse([k for k in st.cells if k[:3] in ((X[0] + 1, X[1], X[2]), (X[0], X[1] + 1, X[2]))])

    def test_prediction_is_the_sawtooth(self):
        for d, n in N_B.items():
            preds = [CP.cc8_prediction(tau, d) for tau in CP.CC8_QUANTUM]
            self.assertEqual(sum(1 for ex, _ in preds if ex == "B"), n, d)
            self.assertEqual({ex for ex, _ in preds} - {"B", "C"}, set())  # no ties for D' != 0
            for tau, (ex, _) in zip(CP.CC8_QUANTUM, preds):              # exit B iff the quantum's lattice phase < D'
                self.assertEqual(ex == "B", ((tau - 6) // 8 - 3) % 17 < d)
        self.assertEqual({CP.cc8_prediction(tau, 0)[0] for tau in CP.CC8_QUANTUM}, {"TIE"})
        self.assertEqual(CP.cc8_prediction(6, 8), ("C", 774))
        self.assertEqual(CP.cc8_prediction(70, 8), ("B", 710))

    def test_first_exit_click_two_updates_after_the_coincidence(self):
        for tau, d in ((30, 1), (22, 16)):
            ex, tc = CP.cc8_prediction(tau, d)
            p = composed(CP.cc8_spec([(tau, d)]))
            lit = {k: {a[:3] for a in p.ports[f"cc8.{k}_nodes"]} for k in ("A", "eB_lo", "eC_lo")}
            st, first, seen = p.initial, {"B": None, "C": None}, set()
            for t in range(1, tc + 5):
                nxt = p.engine.advance(st)
                self.assertEqual(p.engine.rewind(nxt), st)
                for c in clicks(st, nxt, t):
                    site = tuple(c.address[:3])
                    for e, sites in (("B", EXIT_B), ("C", EXIT_C)):
                        if site in sites and first[e] is None:
                            first[e] = t
                    if t == 1:
                        seen |= {k for k, v in lit.items() if site in v}
                    self.assertNotEqual(c.kind, 0)                       # no C0 click (unit-quantum regime)
                st = nxt
            self.assertEqual(seen, set(lit))                              # all three packets lit at update 1
            self.assertEqual(first[ex], tc + 2, (tau, d))
            self.assertIsNone(first["C" if ex == "B" else "B"])


if __name__ == "__main__":
    unittest.main()
