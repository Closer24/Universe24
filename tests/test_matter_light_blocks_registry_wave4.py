"""WAVE 4 registry additions (r21): published clock-rate blocks, @2 generators, composer additions."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from universe24 import Coupling
from universe24.experiments import from_dict

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import generators as GN
from research.matter_light_blocks_v1.registry import guides as G
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose, init_data

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / "research/matter_light_blocks_v1/blocks/clocks_and_gravity"
MPP = [-1, 1, 1]


def board(side, signs=MPP):
    return {"side": side, "signs": list(signs), "background": [0, 0, 2]}


def spec(side, placements, signs=MPP, **extra):
    return {"format": FORMAT, "id": "t", "placements": placements,
            "board": {"side": side, "background": [0, 0, 2], "coupling": {"signs": list(signs), "variant": None}},
            **extra}


def patch_cells(p):
    return {k: (v.a, v.b, v.r) if hasattr(v, "a") else tuple(v) for k, v in dict(p.cells).items()}


class Wave4Registry(unittest.TestCase):
    def test_clockrate_blocks_regenerate(self):
        for stem, sp in CP.r08_clockrates_cases().items():
            path = BLOCKS / f"{stem}.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            prepared, _ = compose(sp)
            self.assertEqual(prepared.initial, from_dict(data).initial, stem)
            self.assertEqual(init_data(prepared, data["steps"]), data, stem)

    def test_appended_published_blocks_regenerate(self):
        pub = ROOT / "research/matter_light_blocks_v1/blocks"
        for stem, sp in CP.published_appended_specs().items():
            path = pub / ("seeds_big_bang" if stem.startswith("d1_") else "atoms") / f"{stem}.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            prepared, _ = compose(sp)
            self.assertEqual(prepared.initial, from_dict(data).initial, stem)
            self.assertEqual(init_data(prepared, data["steps"]), data, stem)

    def test_v2_generators_reduce_to_v1(self):
        b = board(40)
        for hit in ("SLOW", "SLOW_LEFT"):
            self.assertEqual(patch_cells(GN.BLOCKS["slow_glider@2"](b, start=9, hit=hit)),
                             patch_cells(GN.BLOCKS["slow_glider@1"](b, start=9, hit=hit)))
        self.assertEqual(patch_cells(GN.BLOCKS["matter_line@2"](b, length=40, sockets=[3, 4, 5])),
                         patch_cells(GN.BLOCKS["matter_line@1"](b, length=40, sockets=[3, 4, 5])))
        self.assertEqual(patch_cells(GN.BLOCKS["light_line@2"](b, length=40, gauge_phase=1)),
                         patch_cells(GN.BLOCKS["light_line@1"](b, length=40, gauge_phase=1)))
        cat = GN.BLOCKS["slow_glider@2"](b, start=9, hit=CP.R06_CATALOG["0"])
        window = sorted(v for k, v in patch_cells(cat).items() if k[3] == 41 and k[0] == 0 and k[2] == 0)
        self.assertEqual(window, sorted([(-1, -1, 2), (-1, 1, 0), (0, 0, 2)]))
        med = GN.BLOCKS["matter_line@2"](b, length=8, medium=[0, 0, 0, 2], medium_origin=3)
        self.assertEqual(sorted(v[2] for v in patch_cells(med).values()), [0, 0, 0, 0, 0, 0, 4, 4])

    def test_all48_planes(self):
        p = GN.BLOCKS["all48_planes@1"](board(5, [1, 1, 1]), planes=CP.R18_OBJ["G-"], size=5)
        cells = patch_cells(p)
        self.assertEqual(len(cells), 2 * 25 * 48)
        self.assertEqual({v for k, v in cells.items() if k[0] == 0}, {(0, -1, 4)})
        self.assertEqual({v for k, v in cells.items() if k[0] == 1}, {(-1, 0, 0)})

    def test_apply_control_without_assertions(self):
        sp = spec(12, [{"name": "a", "block": "single_channel@1", "params": {"channel": 3, "triple": [0, 1, 4]},
                        "at": [1, 1, 1]},
                       {"name": "b", "block": "single_channel@1", "params": {"channel": 3, "triple": [0, 1, 4]},
                        "at": [6, 6, 6]}])
        out = apply_control(sp, {"name": "no_b", "remove": ["b"]})
        self.assertNotIn("assertions", out)
        self.assertEqual([p["name"] for p in out["placements"]], ["a"])
        compose(out)

    def test_guide_halo_clear_and_h1_ring(self):
        L, J = 24, [4, 12, 4]
        line = {"name": "A", "block": "matter_line@1", "params": {"length": L}, "at": [J[0], 0, J[2]]}
        ring = CP.h1_ring_placement("h1", J)
        asr = {"guide_halo_clear": [{"port": "h1.R_nodes", "closed": True, "allow": [J + [41]]}]}
        prepared, rep = compose(spec(L, [line, ring], assertions=asr))
        self.assertTrue(rep["guide_halo_clear_ok"])
        nodes = [(tuple(k[:3]), k[3], 1) for k in prepared.ports["h1.R_nodes"]]
        self.assertEqual(len(nodes), 14)
        c = Coupling(tuple(MPP))
        last = ring["params"]["paths"][0]["dirs"][-1][0]
        self.assertEqual(G.add(nodes[-1][0], last, L), nodes[0][0])
        self.assertEqual(c.ports[last][nodes[-1][1]], nodes[0][1])          # holonomy 1: closes after one lap
        halo = sorted({rec for hm in G.halo_map(c, nodes, L, True) for rec, _, _ in hm} - {tuple(J + [41])})
        x, y, z, g = halo[0]
        probe = {"name": "p", "block": "single_channel@1", "params": {"channel": g, "triple": [0, 1, 4]},
                 "at": [x, y, z]}
        _, rep2 = compose(spec(L, [line, ring, probe], assertions=asr))
        self.assertFalse(rep2["guide_halo_clear_ok"])

    def test_bridge_ends_on_the_lower_partner(self):
        c = Coupling(tuple(MPP))
        for side, z0 in (("up", 5), ("down", 3)):
            pl = CP.r20_bridge_placement("br", 41, side=side, h=2, phase=1)
            path = pl["params"]["paths"][0]
            nodes = G.channel_path(c, tuple(pl["at"]), path["g0"], G.expand_dirs(path["dirs"]), 256,
                                   sigma0=path["sigma0"])
            self.assertEqual(nodes[-1][0], (41, (-12) % 256, z0))
            self.assertEqual(nodes[-1][1], path["g0"])


if __name__ == "__main__":
    unittest.main()
