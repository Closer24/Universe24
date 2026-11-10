"""WAVE 13 registry additions (r67): r70's rung-E9 boards (light.flrw_relay_lattice@1), a prescribed flat FLRW universe of
fibre light whose tape clocks carry a written a(eta), and its experiment (exp.flrw_in_clicks@1)."""
from __future__ import annotations

import hashlib
import json
import math
import unittest

from research.matter_light_blocks_v1.registry import compositions as CP
from research.matter_light_blocks_v1.registry import guides as G
from research.matter_light_blocks_v1.registry.compose import apply_control, compose, init_data

# SHA-256 of r70's DARK init file (flrw.py write; results/run_manifest.json, archived at 3ee08d7), harness form
DARK_INIT = "b542c6da9597f4981729992660a2b0d2187b6e9f8e78e87bb6ab2b6a37a44cfc"
F = CP.FLRW


class Wave13Registry(unittest.TestCase):
    def test_dark_board_is_r70s_init_file(self):
        spec = CP.flrw_spec([("DARK", None)], 4096, "v1")
        self.assertEqual([q["block"] for q in spec["placements"]], ["guide_net@1"])
        prepared, _ = compose(apply_control(spec, spec["controls"][0]))
        data = init_data(prepared, F["T"])
        self.assertEqual(hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest(), DARK_INIT)
        self.assertEqual(CP.flrw_spec([("DARK", None)], 8192, "v1")["placements"], spec["placements"])   # 2L: same sites

    def test_schedules_are_r70s(self):
        tk = {k: list(v) for k, v in CP.FLRW_TICKS.items()}
        self.assertEqual({k: len(v) for k, v in tk.items()}, {"EdS": 48, "RAD": 50, "STATIC": 33, "CYC": 72})
        C3, C2 = (25 * F["T"] ** 2) ** (1 / 3), math.sqrt(24 * F["T"])
        self.assertEqual(tk["EdS"], [round(C3 * k ** (1 / 3)) for k in range(1, 49)])
        self.assertEqual(tk["RAD"], [round(C2 * math.sqrt(k)) for k in range(1, 51)])
        self.assertEqual(tk["STATIC"], [36 * k for k in range(1, 34)])
        cyc = tk["CYC"]
        self.assertEqual([e + F["LAM"] for e in cyc if e + F["LAM"] <= F["T"]], [e for e in cyc if e > F["LAM"]])
        self.assertTrue(all(b - a >= 8 for a, b in zip(tk["EdS"], tk["EdS"][1:])))   # K3: A-pulses >= 8 apart

    def test_tapes_carry_the_schedule(self):
        for version, sched in (("v1", "EdS"), ("v1", "RAD"), ("v2", "STATIC"), ("v3", "CYC")):
            p = CP.flrw_params(version, sched)
            tapes = [q["name"] for q in p["paths"] if q["name"].startswith("tape_")]
            self.assertEqual(tapes, ["tape_O", "tape_S100", "tape_S300", "tape_S600", "tape_S160"])
            ticks = [e for e in CP.FLRW_TICKS[sched] if version != "v3" or e < F["LAM"]]
            leads = [(F["RING_TICK"] - e) % F["LAM"] if version == "v3" else F["JI"] - e for e in ticks]
            for t in tapes:
                self.assertEqual([q["lead"] for q in p["packets"] if q["path"] == t], leads)
            self.assertEqual([q["lead"] for q in p["packets"] if q["path"].startswith("ring_")], [3, 3])
            self.assertEqual({tuple(q["f"]) for q in p["packets"]}, {(1, 0, -1)})          # A-pulses
            self.assertEqual(sorted(p["closed"]), sorted(["ring_O", "ring_S600"] + (tapes if version == "v3" else [])))
        self.assertEqual(CP.flrw_params("v1", None)["packets"], [])                        # DARK

    def test_geometry(self):
        p = CP.flrw_params("v1", None)
        by = {q["name"]: q for q in p["paths"]}
        for m, d, h in F["radar"]:                                                        # chi = d + 3
            dirs = G.expand_dirs(by[f"radar{m}"]["dirs"])
            self.assertEqual((by[f"radar{m}"]["branch_of"], by[f"radar{m}"]["at_node"]), ("tape_O", F["JI"] + 12 * m))
            self.assertEqual(dirs[:h - 1 + 2 * d + F["U"]], [4] * (h - 1) + [2] * d + [0] * F["U"] + [3] * d)
        for chi, h in F["emit"]:
            self.assertEqual(G.expand_dirs(by[f"emit{chi}"]["dirs"])[:h - 1 + chi], [4] * (h - 1) + [3] * chi)
        for name, _ in F["rings"]:
            self.assertEqual(len(G.expand_dirs(by[name]["dirs"])) + 1, 16)               # 16-node closed rings
        v3 = {q["name"]: q for q in CP.flrw_params("v3", None)["paths"]}
        self.assertEqual(len(G.expand_dirs(v3["tape_O"]["dirs"])) + 1, F["LAM"])          # 600-node tape rings


if __name__ == "__main__":
    unittest.main()
