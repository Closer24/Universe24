"""WAVE 6 registry additions (r21b; r21c with r16c's fixes): cyclic universes, bounce, E13 / E13b on the generator
field_line_bundle@1, fused movers, X-gates, routers (tracked data)."""
from __future__ import annotations

import hashlib
import json
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import symmetry as SY
from research.matter_light_blocks_v1.registry.compose import FORMAT, apply_control, compose
from research.matter_light_blocks_v1.registry.generators import BLOCKS

# initial-state SHA-256 (the experiments verifier's rule) of the proposers' init files and E13's manifest, each
# regenerated exactly by these builders (r21c verify_w67, wave 6: 78/78 files and run hashes)
RECORDED = {
    "c1": "e4708970a3f84be4de7affbe1165e2fc05ad17cbe691964fcd81e06189cf1cff",
    "c1_dark": "0425fb4e47769a2e073d1a0d8b41c71c29e504cfb2c59a2ee87c952368b12c25",
    "c1_one_packet": "3e7de42464dbb9cafda199e08fd764cdd31dfb2843b59098989c62f97b35c74f",
    "c1_asymmetric": "1ee8d7c745470f2b7969c6e54ac6f1318106c9f5ae062fd1e58cf9c2f062ec5b",
    "c2": "15b9492823ec861ed463beb0a73adc673d48ffad3672f47eecb4f54f8db23e20",
    "c2_dark": "d584b48733ee1f7180e53a915df1c88218c0ddcd45336aa8dee624fa4d6b8997",
    "c2_no_matter": "90fd218873a2c5c8506e2d3cd5482942e052d1b2de8558b3dccf26eb97e83f17",
    "c3a_seed_L256": "05f4063538acd05b50d09eb8162d00bea899f448f209c7c96dadd0eb91f99e10",
    "bounce640": "ae0a7109ed0005dfc121b9e64f752448614657687ef9a7f5d09ad2d5dfe52d25",
    "beta1": "8bd803801f2935f4f94e1b3f81b8eb329df475d5990e30daf3caa81e8d2d9347",
    "beta2": "271ce8003b4687c390fa1fb620b943e8e63803a94785583b21482ed5018b8d9c",
    "beta3": "8735747d3f5c4cf75798b7933c7f6c40846e8fc13567cbe5173ccebf3dc525a8",
    "beta4": "698c0991823fcd149a1a97802b36bbee352d8e5baa50948e96c65564925720a6",
    "tow": "6f4c389234e3d233d9e85496b3b196ab33f2dbff138045759a0fc2ef90d11954",
    "xgate_delta0": "edbd3c28f10a27348996662cc554be4156d3367c59dc6a1430e97f272eadefba",
    "xcavity_release": "aee02fd07fc55309fdaf4427e8bce8bb4dee232d171d084123b2f2398878821e",
    "xrouter_B": "284a5d4275e80215c92661de97cc367f35293e7497239796ddfa341b58f6c583",
    "xr1_S0_lam0": "e26de09755f03ff6cd08ac27244de64b326406923f5cd774642c62f205852790",
    "e13_dark": "d3970ce932e473ca70dc88accdd1c65554fefe555a7be8a6bf1c04af685f2fa0",
    "e13_probe_r96": "0052684cf535b55a9324ade87e51a14309f4f6c22dbe7cc4f52beb69c9acec53",
    "e13b_cores_only": "fe1a7857e97981dc299a1d0a501743eadc7cb4ea0dcee0cc2f44d53be37b7e90",
    "router_R1_lam0": "7ae1f05a2b9953a83c82210b2d10f8e1bc06514f3c4b535a0ca6af7532e936f9",
    "router_R2_lam1": "eeb1992784d7689c426b82da43ac34166f66399adf457ab6d1e6a43de2d59755",
    "pair_R3_lam0": "034442bb5007cc585a780cc6f8729470a841900e5912abe2f586dc43e1870f2a",
    "g1_seed_L256": "77bcdff7d6284d91cbf67c8713a666529a78a84e82688ca08a8663aecc638126",
    "c3b_seed_L256": "8377de27ac4ae6fcdb66a4350cbf329389e5de32987c2b6007c4ec945efc0029",
    "g1_dark_L256": "2933fdf0e9b93045289af174990cdac13b716c4edc824177bf980c58ef4bb356",
    "cal_clock_two_L64": "9213f782c01debc5315281645b4fc175ae2f717a7667efaaef9bb402e5c23786",
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


class Wave6Registry(unittest.TestCase):
    def test_cyclic_seeds_and_controls(self):
        for key, spec, ctl in (("c1", CP.cyclic_light_spec(64), None), ("c1_dark", CP.cyclic_light_spec(64), "dark"),
                               ("c1_one_packet", CP.cyclic_light_spec(64), "one_packet"),
                               ("c1_asymmetric", CP.cyclic_light_spec(64), "asymmetric"),
                               ("c2", CP.cyclic_matter_spec(256), None),
                               ("c2_dark", CP.cyclic_matter_spec(256), "dark"),
                               ("c2_no_matter", CP.cyclic_matter_spec(256), "no_matter")):
            st = composed(spec, ctl).initial
            self.assertEqual(state_sha256(st), RECORDED[key], key)
            if ctl is None:
                self.assertEqual(SY.time_reverse_state(st), st, key)       # the seed is an integer moment

    def test_c3a_recipes_agree(self):
        inc, out = composed(CP.cyclic_spin_spec(256, "incoming")), composed(CP.cyclic_spin_spec(256, "outgoing"))
        self.assertEqual(SY.time_reverse_state(inc.initial), out.initial)
        fwd, back = inc.initial, out.initial
        for _ in range(11):
            fwd = inc.engine.advance(fwd)
            earlier = out.engine.rewind(back)
            self.assertEqual(out.engine.advance(earlier), back)
            back = earlier
        self.assertEqual(fwd, back)
        self.assertEqual(state_sha256(back), RECORDED["c3a_seed_L256"])
        self.assertEqual(SY.time_reverse_state(back), back)

    def test_gravity_inside_the_cycle(self):
        for key, spec in (("g1_seed_L256", CP.cyclic_gravity_spec(256, "g1")),
                          ("c3b_seed_L256", CP.cyclic_gravity_spec(256, "c3b")),
                          ("g1_dark_L256", CP.cyclic_gravity_spec(256, "g1", dark=True)),
                          ("cal_clock_two_L64", CP.r36b_part_spec("clock", 64, back=True, at=(20, 32, 20)))):
            st = composed(spec).initial
            self.assertEqual(state_sha256(st), RECORDED[key], key)
            if key.endswith("seed_L256"):
                self.assertEqual(SY.time_reverse_state(st), st, key)        # one moment for all five parts
        p = composed(CP.r36b_part_spec("clock"))                            # the clock part reaches its moment
        st = p.initial
        for _ in range(CP.R36B_MOMENTS["clock"]["t_m"]):
            st = p.engine.advance(st)
        self.assertEqual(SY.time_reverse_state(st), st)

    def test_bounce_is_time_symmetric(self):
        st = composed(CP.bigbang_bounce_v6_spec(640)).initial
        self.assertEqual(state_sha256(st), RECORDED["bounce640"])
        self.assertEqual(SY.time_reverse_state(st), st)
        self.assertEqual(len(CP.bigbang_bounce_v6_spec(320)["placements"]), 12)

    def test_e13_bundle(self):
        geo = CP.e13_geometry()
        self.assertEqual([len(geo["radii"][r]) for r in CP.E13["radii"]], [64, 36, 16, 4])     # 36864 / r^2
        spec = CP.e13_spec()
        self.assertEqual(([p["block"] for p in spec["placements"]], len(spec["controls"]), spec["steps"]),
                         (["field_line_bundle@1"], 10, 111))
        self.assertLess(len(json.dumps(spec, separators=(",", ":"))), 3000)               # parametric, not 86.6 kB
        self.assertEqual(state_sha256(composed(spec, "dark").initial), RECORDED["e13_dark"])
        probe = composed(spec, "probe_r96").initial
        self.assertEqual(state_sha256(probe), RECORDED["e13_probe_r96"])
        self.assertEqual(state_sha256(composed(CP.e13b_spec()).initial), RECORDED["e13b_cores_only"])
        # the generator equals the explicit guide_net@1 form (64 paths, the same packet list)
        lines = CP.field_line_bundle_lines(4, 16, 100)
        names = sorted(lines)
        pk = [{"path": n, "f": [1, 0, -1], "lead": 5} for n in names]
        pk += [{"path": "~" + n, "f": [1, 0, -1], "lead": len(lines[n]["sites"]) - 1 - p}
               for n, p in sorted(geo["radii"][96].items())]
        explicit = {"format": FORMAT, "id": "e13_explicit", "board": spec["board"], "placements": [
            {"name": "field", "block": "guide_net@1", "at": list(CP.E13["O"]), "params": {
                "paths": [{"name": n, "g0": 0, "start": list(lines[n]["start"]), "dirs": CP._run_length(lines[n]["dirs"])}
                          for n in names], "packets": pk}}]}
        self.assertEqual(composed(explicit).initial, probe)
        with self.assertRaises(ValueError):                                 # r04's halo condition is checked
            CP.field_line_bundle_placement("f", (0, 50, 50), rho=4, x_root=8, x_end=30)
        bad = {"format": FORMAT, "id": "bad", "board": spec["board"], "placements": [
            {"name": "f", "block": "field_line_bundle@1", "at": [0, 50, 50], "params": {"x_root": 8, "x_end": 30}}]}
        with self.assertRaises(ValueError):
            compose(bad)

    def test_fused_movers_and_rails(self):
        for n in (1, 2, 3, 4):
            self.assertEqual(state_sha256(composed(CP.fused_mover_line_spec(n)).initial), RECORDED[f"beta{n}"], n)
        self.assertEqual(state_sha256(composed(CP.towed_pair_spec()).initial), RECORDED["tow"])
        # beta_1 is the registered SLOW_LEFT glider one update after its registered phase
        sl = {"format": FORMAT, "id": "slow_left", "board": CP._board(30, CP.MPP),
              "placements": [{"name": "A", "block": "matter_line@1", "params": {"length": 30, "sockets": [8, 9, 10]},
                              "at": [4, 0, 4], "wrap": True},
                             {"name": "G", "block": "slow_glider@1", "params": {"start": 10, "hit": "SLOW_LEFT"},
                              "at": [4, 0, 4], "wrap": True}]}
        p = composed(sl)
        self.assertEqual(p.engine.advance(p.initial), composed(CP.fused_mover_line_spec(1)).initial)
        board = {"side": 40, "signs": (-1, 1, 1), "background": (0, 0, 2)}
        self.assertEqual(BLOCKS["matter_line@3"](board, length=40).cells,
                         BLOCKS["matter_line@1"](board, length=40).cells)
        self.assertEqual(len(CP.leapfrog_pair_spec()["placements"][1]["params"]["marks"]), 20)

    def test_split_guides(self):
        for key, spec in (("xgate_delta0", CP.x_gate_spec(True, 0)),
                          ("xcavity_release", CP.x_cavity_spec(True, (20,), 88)),
                          ("xrouter_B", CP.escorted_junction_spec("B")),
                          ("xr1_S0_lam0", CP.escort_pair_router_spec("S0", 0))):
            st = composed(spec).initial
            self.assertEqual(state_sha256(st), RECORDED[key], key)
        st = composed(CP.x_gate_spec(True, 0)).initial
        self.assertNotIn((32, 32, 32, 0), st.cells)                         # the gate node is the vacuum gap
        with self.assertRaises(ValueError):                                 # a packet may not sit on a gap at t = 0
            CP.x_gate_spec(True, None, t_D=0)
        with self.assertRaises(ValueError):                                 # not a holonomy-z rectangle
            CP.holonomy_ring_counterpair_placement("R", (0, 0, 0), (1, 2), n1=3, n2=36, g0=0)

    def test_routers_with_halo_core_registers(self):
        for key, spec in (("router_R1_lam0", CP.conserving_router_spec(0)),
                          ("router_R2_lam1", CP.conserving_router_spec(1, "R2")),
                          ("pair_R3_lam0", CP.conserving_pair_router_spec(0))):
            self.assertEqual(state_sha256(composed(spec).initial), RECORDED[key], key)
        spec = CP.conserving_router_spec(0)
        cores = {p["name"]: p["params"]["state"] for p in spec["placements"] if p["block"] == "slot_clock@1"}
        self.assertEqual(cores, {"EA": [0, -1, 4], "EB": [0, -1, 4], "DA": [0, 1, 4], "DB": [0, 1, 4]})


if __name__ == "__main__":
    unittest.main()
