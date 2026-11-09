"""WAVE 12 registry additions (r67): builder B QM-B8's triple gate (gate.triple_x_gate@1), three unit fibre packets meeting
at one vacuum gap node shared by an x-, a y- and a z-fibre, and the two-time counting rule (exp.two_time_counting_rule@1)."""
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

# SHA-256 of builder B's triple-gate init files (research/matter_light_v1/remote/builderB_QMB3/qmb/preparations, archived
# at 3ca4977; QMB_INIT_SHA256): member (Dy, Dz, sy, sz) = (-4, 0, +, +), gear 2, T = 80, in the harness form
INIT_FILES = {128: "23099a09eb8db5d8adf1914f55e3d7213003243c90ec66d51131c0c29dc4f03d",
              256: "2b4b65343d13c2074ccd0f0eecbe3caaacdc1d71071f1634f05b2c8e39b3d535"}
# SHA-256 of all 12 of E25's mirrored init files: JR of run 1's final state at T = 80, compact JSON and one newline
MIRROR_INIT = {
    (0, 0, 1, 1, 2): "a3612cfae8aec0dcd6f6a3631c334aaa070bd7fb10cbc4a6003fd35fd466223f",
    (0, 0, 1, 1, 3): "440f6d85b464b9689667861d278b4b520a454d2f57595292faf9f48da54e1b89",
    (0, 0, 1, 1, 4): "8181e222af7cbe68f676ff6eb9af22324cde6b6923e87770d28058a1a3dd93fa",
    (-4, 2, 1, 1, 2): "7631e6b8b87c4cdb8267b2c8e05a06b55d15ae16037c9207470d321953c6174f",
    (-4, 2, 1, 1, 3): "49f5e5c376ad992d8e0011cbdb00c081e613ade4c752859afb8b8c0fd1b5b34e",
    (-4, 2, 1, 1, 4): "cfb26276557804ef2266647fbeba3ebd381b8bdc7fd7ee02294ae50bfb14cfb7",
    (-4, -3, 1, -1, 2): "714bc8da278f916c8159e99ba9fe1acaa206d027a4902fd7e453fc9002034609",
    (-4, -3, 1, -1, 3): "9f0dcfe352a6ab1fe026eec021d2a0cb038c46eb04f47aaeb5a0286c158856a2",
    (-4, -3, 1, -1, 4): "6726aa031ac202042932ca70f88df5b6f8b7e7388815d26d5316d5342aece7bd",
    (1, -1, -1, 1, 2): "ad5d6b205ae679aab9246e35f2d8daf4cad1ab478bc08fec48e57cdf16b45840",
    (1, -1, -1, 1, 3): "593246dad9277658c409b02d75c98b4eef6c0308f87b7b814d9aabdbc17e8615",
    (1, -1, -1, 1, 4): "7e2aa44a35f6ce9c51006e47a9540182f3c09fddab67fc347439ac71feba4437"}
T = 80
GATE = (*CP.TRIPLE_GATE_AT, 1)


def composed(member, L=128):
    spec = CP.triple_gate_spec([member], L=L)
    prepared, rep = compose(apply_control(spec, spec["controls"][0]))
    bad = [k for k, v in rep.items() if k.endswith("_ok") and not v]
    if bad:
        raise AssertionError(f"assertions failed {bad}")
    return prepared


def run(engine, state):
    recs = []
    for t in range(1, T + 1):
        nxt = engine.advance(state)
        if engine.rewind(nxt) != state:
            raise ArithmeticError(t)
        recs += [(t, tuple(c.address), c.kind, c.quotient) for c in clicks(state, nxt, t)]
        state = nxt
    return state, recs


class Wave12Registry(unittest.TestCase):
    def test_builder_bs_init_files(self):
        for L, sha in INIT_FILES.items():
            data = init_data(composed((-4, 0, 1, 1, 2), L), T)
            self.assertEqual(hashlib.sha256((json.dumps(data, indent=1) + "\n").encode()).hexdigest(), sha, L)
        small, big = (CP.triple_gate_spec([(-4, 0, 1, 1, 3)], L=L) for L in (128, 256))
        self.assertEqual(small["placements"], big["placements"])              # 2L: every part at the same site

    def test_members_and_controls(self):
        members = [(Dy, Dz, sy, sz, g) for sy in (1, -1) for sz in (1, -1) for Dy in (-4, 0, 4) for Dz in (-3, 2)
                   for g in (2, 3, 4)]
        spec = CP.triple_gate_spec(members)
        self.assertEqual(len({c["name"] for c in spec["controls"]}), len(members))
        for m, c in zip(members, spec["controls"]):
            self.assertEqual(c.get("remove", []), ["tri_gear"] if m[4] == 2 else [])
            hw = c["override"]["tri"]
            self.assertEqual([p["sigma0"] for p in hw["paths"] if p["name"] in ("Y0", "Z0")], [-m[2], -m[3]])
            self.assertEqual([q["f"] for q in hw["packets"]], [[1, -1]] * 3)
        st = composed((0, 0, 1, 1, 4)).initial
        self.assertEqual(st.cells[GATE].r, 4)                                   # the prepared gate gear
        self.assertNotIn(GATE, composed((0, 0, 1, 1, 2)).initial.cells)         # g = 2: the vacuum
        self.assertEqual(max(max(abs(v.a), abs(v.b)) for v in st.cells.values()), 1)   # unit packets
        with self.assertRaises(ValueError):
            CP.triple_gate_placements("x", CP.TRIPLE_GATE_AT, 0, 0, 1, 1, g=5)

    def test_mirrored_run_is_run_one_read_backwards(self):
        for m, sha in MIRROR_INIT.items():
            p = composed(m)
            xT, rf = run(p.engine, p.initial)
            mir0 = SY.time_reverse_state(xT)                                    # JR of run 1's complete final state
            data = checkpoint_data(mir0, p.engine, 0)["experiment"]
            data["steps"] = T
            blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True) + "\n"
            self.assertEqual(hashlib.sha256(blob.encode()).hexdigest(), sha, m)  # E25's init file
            xB, rb = run(p.engine, mir0)                                        # a second FORWARD run
            self.assertEqual(xB, SY.time_reverse_state(p.initial))
            self.assertEqual(Counter(rb), Counter((T + 1 - t, x, (-k) % 3, -q) for t, x, k, q in rf))
            first = min(r for r in rf if r[1] == GATE)
            last = max(r for r in rb if r[1] == GATE)
            self.assertEqual((T + 1 - last[0], (-last[2]) % 3, -last[3]), (first[0], first[2], first[3]))   # k-bar = k

    def test_epsilon_twin(self):
        p2, p3 = composed((-4, 2, 1, 1, 2)), composed((-4, 2, 1, 1, 3))
        (s2, r2), (s3, r3) = run(p2.engine, p2.initial), run(p3.engine, p3.initial)
        self.assertEqual(r2, r3)                                                # every click (t, x, k, q) identical
        diff = {k for k in set(s2.cells) | set(s3.cells) if s2.cells.get(k) != s3.cells.get(k)}
        self.assertEqual(diff, {GATE})
        self.assertEqual(s3.cells[GATE].r - s2.cells.get(GATE, s2.background).r, 1)


if __name__ == "__main__":
    unittest.main()
