"""WAVE 7 registry additions (r21c): atoms inside the cycles and the bounces, each seed ONE composition (tracked data)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import symmetry as SY
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose
from research.matter_light_blocks_v1.registry.generators import BLOCKS

# initial-state SHA-256 (the experiments verifier's rule) of the proposers' init files, each regenerated exactly by
# these builders (r21c verify_w67, wave 7: 22/22 files)
RECORDED = {
    "c3c_seed_L256": "cd50d49a64bd1170a70ed9834695b859ad221d5db4ea758fdf6dd5f74881870f",
    "at_seed_L256": "5273686a15fa1fc25845fe953bb49d00e63613f2ceb2234d356ba55e29cf3a73",
    "at_k5_L256": "c20bc6cdaa574a9b5f9f7d66bb4d0f902d098e8f2210ca8ede8494a8ceea5e38",
    "at_k6_L256": "0530a68e5da3352fd987d687439be2608d05f1d5ae86211f99be6b916b6343df",
    "c3a_seed_L256": "05f4063538acd05b50d09eb8162d00bea899f448f209c7c96dadd0eb91f99e10",
    "mod82_L128": "5929f0699a60629aee8588f107e687447728bb4bce495f5334ff201fc03956fd",
    "u82_L256": "416b59b840ca999323e97c174d6bb6334eccf242a78ac0f01352974d8c00feea",
    "sstar_c_L640": "58b0e397957d3aa447771fbbb4205bdca7719adfb134e5fdb60e4c97a7a46a33",
    "sstar_c_k1_L640": "bd39f237c25bbd0c207f7cb60b732ec86d3f7333deb5c19b24279002d75b7f19",
    "sstar_c_k2_L640": "413b859ad1e8016cc8cb9dce3b197efa554debd17d4d9f23766bc9381d692b03",
    "hbpg_L640": "fa155eca9784a93b0d2994607cd45dd460946fcfed7cefc68700fa274658b2f9",
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


def evolved(spec, n):
    p = composed(spec)
    st = p.initial
    for _ in range(n):
        st = p.engine.advance(st)
    return st


class Wave7Registry(unittest.TestCase):
    def test_c3c_is_one_composition_of_existing_generators(self):
        spec = CP.cyclic_universe_c3c_spec(256)
        self.assertLessEqual({p["block"] for p in spec["placements"]},
                             {"light_line_s@1", "matter_line@1", "guide_net@1", "literal_patch@1"})
        st = composed(spec).initial
        self.assertEqual(state_sha256(st), RECORDED["c3c_seed_L256"])
        self.assertEqual(SY.time_reverse_state(st), st)                    # one integer moment for all six parts
        self.assertEqual(sum(1 for v in st.cells.values() if v.a or v.b), 8)
        self.assertTrue(all(v.a == -v.b for v in st.cells.values()))

    def test_twin_cavity_atoms_and_controls(self):
        spec = CP.twin_cavity_atoms_spec(256)
        for key, ctl in (("at_seed_L256", None), ("at_k5_L256", "no_escorts"), ("at_k6_L256", "right_inarm_plus1")):
            self.assertEqual(state_sha256(composed(spec, ctl).initial), RECORDED[key], key)
        # every moment patch is its sub-part's own moment: the escort's (1,-1) packet 15 updates later, the bang pair 11
        A = CP.R36B_ATOMS
        board = CP._board(256, CP.MPP)
        for n in (A["p_in"][1], A["p_in"][1] + 1):
            arm = CP._atoms_arm("in", A["d"], 3, n, A["O"])
            arm["params"]["packets"] = [{"path": "A", "f": [1, -1], "lead": n - 13}]
            moment = [p for p in CP.twin_cavity_atoms_placements(p_in=(n, n), data=False)
                      if p["name"] in ("atoms_inR", "atoms_escortR")]
            st = evolved({"format": FORMAT, "id": "escort", "board": board, "placements": [arm]}, 15)
            self.assertEqual(st, composed({"format": FORMAT, "id": "m", "board": board, "placements": moment}).initial)
            self.assertEqual(SY.time_reverse_state(st), st)
        O, d = A["O"], A["d"]
        data = [CP._atoms_piece("ante", -d + 1, d - 1, O, [8, 9, 10, 26, 27, 28])]
        data += [{"name": n, "block": "fibre_packet@1", "params": {"front": f, "direction": s, "gauge_phase": 0},
                  "at": [O[0] - d + 1, O[1], O[2]], "wrap": False} for n, f, s in (("Pp", 10, 1), ("Pm", 26, -1))]
        moment = [p for p in CP.twin_cavity_atoms_placements() if p["name"] in ("atoms_ante", "atoms_bang")]
        self.assertEqual(evolved({"format": FORMAT, "id": "data", "board": board, "placements": data}, 11),
                         composed({"format": FORMAT, "id": "m", "board": board, "placements": moment}).initial)

    def test_c3a_without_a_recipe(self):
        st = composed(CP.cyclic_spin_moment_spec(256)).initial
        self.assertEqual(state_sha256(st), RECORDED["c3a_seed_L256"])
        self.assertEqual(evolved(CP.cyclic_spin_spec(256, "incoming"), 11), st)
        self.assertEqual(SY.time_reverse_state(st), st)

    def test_mod82_and_u82(self):
        self.assertEqual(state_sha256(composed(CP.twin_xcavity_module_spec(128)).initial), RECORDED["mod82_L128"])
        st = composed(CP.cyclic_spin_atoms_spec(256)).initial
        self.assertEqual(state_sha256(st), RECORDED["u82_L256"])
        self.assertEqual(SY.time_reverse_state(st), st)
        self.assertEqual(len(st.cells), len(composed(CP.cyclic_spin_moment_spec(256)).initial.cells) +
                         len(composed(CP.twin_xcavity_module_spec(256)).initial.cells))      # disjoint supports

    def test_bounce_with_atoms(self):
        spec = CP.bigbang_bounce_atoms_spec(640)
        st = composed(spec).initial
        self.assertEqual(state_sha256(st), RECORDED["sstar_c_L640"])
        self.assertEqual(SY.time_reverse_state(st), st)
        self.assertEqual(state_sha256(composed(spec, "no_escorts").initial), RECORDED["sstar_c_k1_L640"])
        self.assertEqual(state_sha256(composed(spec, "up_escort_late").initial), RECORDED["sstar_c_k2_L640"])

    def test_half_integer_bang(self):
        p = composed(CP.half_integer_bang_spec(640))
        st = p.initial
        self.assertEqual(state_sha256(st), RECORDED["hbpg_L640"])
        self.assertTrue(all(v.b == 0 for v in st.cells.values()))           # a half moment: b = 0 everywhere
        self.assertEqual(p.engine.advance(st), SY.time_reverse_state(st))    # F(S*) = JR(S*)
        self.assertIn("all48_site@1", {q["block"] for q in CP.half_integer_bang_spec(320)["placements"]})
        self.assertTrue(all(q["block"] in BLOCKS for q in CP.half_integer_bang_spec(320)["placements"]))


if __name__ == "__main__":
    unittest.main()
