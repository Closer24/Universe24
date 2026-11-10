"""WAVE 10 registry additions (r67): builder D R5's device CC7-M, one prepared hardware with two outcomes
(select.escort_end_junction@1), its member h = 1 at its integer moment, and that member beside r36b's C3c (tracked data)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import symmetry as SY
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose, init_data

# SHA-256 of builder D's init files (rebuild_r5.py in research/matter_light_v1/remote/builderD_R5, archived at 96b1c0f;
# the files r10r ran, R10R-0), which these builders write byte for byte in the harness's form (indent 1, one newline)
INIT_FILES = {"cc7m_h0_L256": "f447088869b47d4664b8dec7838915263a1a2bc528e5f569d2e8a44fdef71727",
              "cc7m_h1_L256": "9b44e620eebb2717b02af4a9a865661af067b5987aaa4653cd650763fd7eec23",
              "c3c_cc7m_h1_L256": "f0a5a6be2710228cc4e5805f763fdab81a55fff8f3417aab37f167231da6b153"}
# initial-state SHA-256 (the experiments verifier's rule) of the controls, as E20 and E20b record them
RECORDED = {
    "h0_no_quantum": "a404183bf6b448ff0136d05dd87f380b51479b88d7a00e28aee0189e98c66fa9",
    "h1_no_quantum": "cb763cbc056b87c0d9f44d43f6ca14beec01950f5e12cfbdcc6c86f01324e399",
    "no_escorts": "fad6df884db801a24c06e251602f0516f4c027d141b2d5a337ba53b7eee058ef",
    "c3c_alone": "cd50d49a64bd1170a70ed9834695b859ad221d5db4ea758fdf6dd5f74881870f",        # C3c's seed (E18)
    "device_alone": "03e6c52ceea14f3bd94c2b8c1ba469c0e68fb7f1f199cdb3e49ba81a9f5eac6c",
}


def state_sha256(state):
    blob = json.dumps([state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())], separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def composed(spec, control=None):
    if control is not None:
        spec = apply_control(spec, next(c for c in spec["controls"] if c["name"] == control))
    prepared, rep = compose(spec)
    bad = [k for k, v in rep.items() if k.endswith("_ok") and not v]
    if bad:
        raise AssertionError(f"{spec['id']}: assertions failed {bad}")
    return prepared


def init_file_sha256(spec):
    """The SHA-256 of the composed board's official init file in the harness's form (json indent 1, one newline)."""
    data = init_data(composed(spec), spec["steps"])
    return hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest()


class Wave10Registry(unittest.TestCase):
    def test_members_are_builder_ds_init_files(self):
        for h in (0, 1):
            spec = CP.cc7m_spec(h)
            self.assertEqual([q["block"] for q in spec["placements"]], ["guide_net@1"])
            self.assertEqual(spec["steps"], (270, 960)[h])
            self.assertEqual(init_file_sha256(spec), INIT_FILES[f"cc7m_h{h}_L256"], h)
        with self.assertRaises(ValueError):
            CP.cc7m_router_placement("x", CP.CC7M_AT, h=2)

    def test_one_hardware_two_prepared_states(self):
        p0, p1 = (CP.cc7m_spec(h)["placements"][0]["params"] for h in (0, 1))
        self.assertEqual(p0["paths"], p1["paths"])                         # the hardware does not depend on h
        self.assertEqual([q for q in p0["packets"] if q not in p1["packets"]], [{"path": "eB_lo", "f": [1, -1], "lead": 5}])
        self.assertEqual([q for q in p1["packets"] if q not in p0["packets"]], [{"path": "eB_hi", "f": [1, -1], "lead": 22}])
        s0, s1 = (composed(CP.cc7m_spec(h)).initial for h in (0, 1))
        dark = [composed(CP.cc7m_spec(h), "no_quantum").initial for h in (0, 1)]
        self.assertEqual(state_sha256(dark[0]), RECORDED["h0_no_quantum"])
        self.assertEqual(state_sha256(dark[1]), RECORDED["h1_no_quantum"])
        self.assertEqual(state_sha256(composed(CP.cc7m_spec(0), "no_escorts").initial), RECORDED["no_escorts"])
        diff = {k for k in set(s0.cells) | set(s1.cells) if s0.cells.get(k) != s1.cells.get(k)}
        self.assertEqual(len(diff), 14)                                   # R10R-1
        prepared = composed(CP.cc7m_spec(0))
        line = {a[:3] for k in ("cc7m.eB_lo_nodes", "cc7m.eB_hi_nodes") for a in prepared.ports[k]}
        near = {(x + dx, y + dy, z + dz) for x, y, z in line
                for dx, dy, dz in ((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))}
        self.assertTrue(all(k[:3] in near for k in diff))
        X = CP.CC7M_AT
        for st in (s0, s1):                                               # the doors are vacuum (gap nodes)
            self.assertFalse([k for k in st.cells if k[:3] in ((X[0] + 1, X[1], X[2]), (X[0], X[1] + 1, X[2]))])

    def test_moment_form_is_the_member_nine_updates_later(self):
        p = composed(CP.cc7m_spec(1))
        st = p.initial
        for _ in range(CP.CC7M_H1_MOMENT["t_m"]):
            nxt = p.engine.advance(st)
            self.assertEqual(p.engine.rewind(nxt), st)
            st = nxt
        moment = {"format": FORMAT, "id": "cc7m_h1_moment", "board": CP._board(256, CP.PPP),
                  "placements": CP.cc7m_moment_placements(CP.CC7M_AT)}
        self.assertEqual(composed(moment).initial, st)
        self.assertEqual(SY.time_reverse_state(st), st)                    # an integer moment: a = -b everywhere
        self.assertEqual(sorted((v.a, v.b) for v in st.cells.values() if v.a or v.b), [(-1, 1)] * 3)

    def test_member_beside_c3c(self):
        spec = CP.cc7m_in_c3c_spec(256)
        self.assertEqual(init_file_sha256(spec), INIT_FILES["c3c_cc7m_h1_L256"])
        self.assertEqual(SY.gauge_for((1, 1, 1), (-1, 1, 1)), (True, True))   # class B: character and staggered
        union = composed(spec).initial
        self.assertEqual(SY.time_reverse_state(union), union)
        c3c, dev = (composed(spec, c).initial for c in ("c3c_alone", "device_alone"))
        self.assertEqual(state_sha256(c3c), RECORDED["c3c_alone"])
        self.assertEqual(c3c, composed(CP.cyclic_universe_c3c_spec(256)).initial)
        self.assertEqual(state_sha256(dev), RECORDED["device_alone"])
        self.assertFalse(set(c3c.cells) & set(dev.cells))                 # disjoint supports
        self.assertEqual(union.cells, {**c3c.cells, **dev.cells})
        big = CP.cc7m_in_c3c_spec(512)
        self.assertEqual(big["placements"], spec["placements"])            # 2L: every part at the same site


if __name__ == "__main__":
    unittest.main()
