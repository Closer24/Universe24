"""WAVE 5 registry additions (r21): planar blocks, the wave-5 builders, recorded initial states (tracked data only)."""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from universe24.experiments import from_dict

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose, init_data

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / "research/matter_light_blocks_v1/blocks"
MPP, PPP = [-1, 1, 1], [1, 1, 1]

# recorded initial-state hashes: E09 (r23 experiment.json; redshift_flux_check_16 equals redshift_clock_in_flux and
# is dropped), E11 (r25 experiment.json), E10's lamp (r22 experiment.json)
E09 = {"shapiro_k0": "e69f586fde6a6ca1b2ba5176582460bd95dcc8edd3d16c7b05ace33efc857619",
       "shapiro_k1": "5c91a1d54151532271da7b1c223e8a9d1f8f1ae7706c6c403425a5ba00c508dd",
       "shapiro_k2": "4b060392866eaaf918286a605f5bff456d6bb36fbee68448e13ba45bdb8688e5",
       "shapiro_k3": "58b0942dbf540190564cd86ce677c410e737b62ce9ecf1cf17e00326630fbc6e",
       "shapiro_k4": "ad2ea20598edb252b118e33bc7181f3d7b9a98b4e6f1ae3eba91d33938dd4158",
       "shapiro_k5": "0a5132fdd8ce5905f3f04e9299474380f726433220aa8a722eddfab9abf11980",
       "shapiro_k6": "7452c46b526ed56571913279cfb8ded04896b7e803b74fe6f120c9a1730dcd9c",
       "shapiro_flux_only": "32fdd4eaf14c0ab5df38aecb14423a83e81894ebdd361b80b7fa5b0c95fc4888",
       "river_comoving": "81fa3a5b6b03c0017dd3835d1b2a5ebdf5f9780d72ba9343e2dacd4bbc4320cd",
       "river_comoving_no_flux": "03d64e48c17041ceb74e07da4f27affb6f048eb7dadfef8e293f08b30f6d02ef",
       "bending_k0": "913778608606547c3c35234d8f3e743607e026c7d7b0501dbbf3e738e562172d",
       "bending_k1": "2f44b39a44a514c469cccb1f2d5d766fc5600b092f07b0336aaf3ca67b1e9197",
       "bending_k2": "805e9ed96e558b8cb50c041276a75a981e3a074d0593842a90055708a0ce3d48",
       "bending_k3": "d7752a72c1f421787160d54cb3d67f03d26cc519e591bac4bd5a77070141590d",
       "bending_k4": "7d9bbdc35a007cd8b17ab49b13b5360412fffc2402f6df35bc7fa9343b84bccb",
       "bending_k5": "998eeebc83dd4ec109d8b4832332818def8f3528b6f4ef98dc793221e5d4aaee",
       "bending_flux_only": "ee84719a18dcb42a44d4b9becaa2abcf6bbaf9fd69b6133c615fd747b5d924b8",
       "redshift_far_clock": "d5fb2621dd74b68d87b00b7bcb4d66242e10235cfd0aadceb45c784e413b8b10",
       "redshift_clock_in_flux": "51ae4fb9ea8d9c373d2ff8f04e85ea0c21d9d1ec4b5fd3a224b9c80778c7925c",
       "redshift_no_packets": "15c23f9f6d3aa7aa90d30399da12a2bb0b8ff1e35bf892ef74905e87c1d296db"}
E11 = {"main_diagonal_L6": "27016cc96ccc237fa9d921c7c4f1c7ffcb5e606a8032f74d2bf1417f6468916b",
       "control_generic_L5": "09c742269302ed56f7b930e8b4c2e7fa609851d7047122b215dc572a11eec164"}
E10_LAMP = "8174014c0acdbebdce42f59fe789fbdbff0a121bd6b5b368d3dcd75430ca5e16"


def state_sha256(state):
    blob = json.dumps([state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())], separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def board(side, signs, placements, **extra):
    return {"format": FORMAT, "id": "t", "placements": placements,
            "board": {"side": side, "background": [0, 0, 2], "coupling": {"signs": list(signs), "variant": None}},
            **extra}


def composed(spec):
    prepared, rep = compose(spec)
    bad = [k for k, v in rep.items() if k.endswith("_ok") and not v]
    if bad:
        raise AssertionError(f"{spec['id']}: assertions failed {bad}")
    return prepared


class Wave5Registry(unittest.TestCase):
    def test_published_planar_blocks_regenerate(self):
        cases = {"moving_matter/planar_glider_100.json": CP.r18_planar_spec([("G-", 5)], L=12),
                 "charge/planar_glider_100_J.json": CP.r18_planar_spec([("JG-", 5)], L=12),
                 "seeds_big_bang/planar_bigbang_L16.json": board(16, PPP, [{
                     "name": "seed_plane", "block": "all48_planes@1", "params": {"planes": [[-1, -1, 0]], "size": 16},
                     "at": [8, 0, 0], "wrap": True}])}
        for rel, spec in cases.items():
            data = json.loads((BLOCKS / rel).read_text(encoding="utf-8"))
            prepared = composed(spec)
            self.assertEqual(prepared.initial, from_dict(data).initial, rel)
            self.assertEqual(init_data(prepared, data["steps"]), data, rel)

    def test_wave5_builders_compose(self):
        specs = [CP.r28_reg9b_spec("Zr"), CP.r28_reg9b_spec("Hr"),
                 board(320, MPP, CP.r28_module_readers(320)),
                 board(640, MPP, [CP.ring_tap_placement("tap", (0, 624, 3), "hz", 7, 4, 80),
                                  CP.mirror_bridge_placement("bridge", (69, 12, 4), 4, [[4, 4], [3, 24]], wrap=True)]),
                 board(640, MPP, [CP.ring_tap_placement("tap", (0, 624, 3), "hz", 7, 4, 80, (0,))]),
                 CP.ring_clock_h1_spec(64, (3,)), CP.wu_half_cross_spec((-1, 1, -1), 1, "V2"),
                 CP.wu_half_cross_spec((-1, 1, 1), 1, "V1"), CP.r19_race_spec(Hh=2),
                 CP.r19_heralded_z6_spec(trials=[(0, 1, 2, 1), (3, 3, 0, 0)]), CP.e10_lamp_spec()]
        for sp in specs:
            self.assertGreater(len(composed(sp).initial.cells), 0, sp["id"])
        e10 = CP.e10_spec_all()
        self.assertEqual(len(e10["placements"]), 45)
        self.assertGreater(len(composed(e10).initial.cells), 5000)
        dark = apply_control(e10, e10["controls"][0])
        self.assertTrue(all(not p["params"].get("packets") for p in dark["placements"]))

    def test_recorded_initial_states(self):
        cases = CP.r23_e09_cases()
        self.assertEqual(set(cases), set(E09))
        for name in ("shapiro_k6", "shapiro_flux_only", "river_comoving", "bending_k5", "bending_flux_only",
                     "redshift_clock_in_flux", "redshift_no_packets"):       # every builder and branch (< 5 s)
            self.assertEqual(state_sha256(composed(cases[name]).initial), E09[name], name)
        for name, spec in CP.r25_e11_cases().items():
            self.assertEqual(state_sha256(composed(spec).initial), E11[name], name)
        self.assertEqual(state_sha256(composed(CP.e10_lamp_spec()).initial), E10_LAMP)


if __name__ == "__main__":
    unittest.main()
