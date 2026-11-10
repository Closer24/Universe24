"""Stage 1, CHOICE-CLICK layer acceptance tests TC.1-TC.12 (pre-registered in NOTES_choice.md, 09:33:04 UTC) and
TC.11b, TC.13, TC.14 (pre-registration 2, 09:54:36 UTC, after the manager's rulings), TC.15 (pre-registration 3,
10:12:01 UTC), TC.15b (5, 10:17:35), TC.16 (4, 10:13:00 UTC) and the status probe TC.17 (6, 10:30:05 UTC).
F7 WARNING (manager ruling 10:2x): the C0-fibre F7 (TC.7, TC.15b, TC.16) runs on the TAXICAB cone and is a MECHANISM
TEST ONLY; TC.17 probes the round-cone (headroom light) carrier.

Run from the repository root (numpy required; nice, <= 2 threads):
    OMP_NUM_THREADS=2 nice -n 10 python -m unittest universe24.tests.test_choice -v
Every test writes results/choice/TC.<n>.json with a `date -u` stamp. Exact integers; probabilities are exact
Fractions (M2-2 visibilities are floats compared at 3 decimals, as S5-P2R reported them). Every run is rewound.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from universe24.demos.choice import experiments as E  # noqa: E402

RES = Path("runs/tests") / "choice"
BORN = ["1", "3/4", "1/4", "0", "1/4", "3/4"]


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def save(name: str, payload: dict, started: str) -> None:
    RES.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload["_started"] = started
    payload["_finished"] = stamp()
    (RES / f"{name}.json").write_text(json.dumps(payload, indent=1, default=str))


def assert_recip(tc: unittest.TestCase, rec: dict, designated: bool | None = None):
    tc.assertTrue(rec["ok"], rec)
    tc.assertEqual(rec["violations"], 0)
    tc.assertEqual(rec["support_violations"], 0)
    if designated is False:
        tc.assertEqual(rec["designated"], 0)
    if designated is True:
        tc.assertGreater(rec["designated"], 0)
        tc.assertTrue(all(j.strip() for j in rec["justifications"]))


class TestChoice(unittest.TestCase):
    maxDiff = None

    def test_TC01_carriers(self):
        t0 = stamp()
        r = E.exp_carriers()
        save("TC.1", r, t0)
        for row in r["ring"]:
            self.assertTrue(row["exact_period6"] and row["remainder_0"] and row["sum_b2_2A2"] and row["rewind"], row)
            self.assertEqual(row["click_kinds"], [0])
        for row in r["pair4"]:
            self.assertTrue(row["period4"] and row["rewind"], row)
        for row in r["fibre"]:
            self.assertTrue(row["exact_transport_2L"] and row["remainder_0"] and row["rewind"], row)
            self.assertEqual(row["click_kinds"], [0])
        for rec in r["recip"].values():
            assert_recip(self, rec, designated=False)

    def test_TC02_born_router(self):
        t0 = stamp()
        out = []
        for A in (1, 2, 3, 10):
            for form in ("opposite", "mirror"):
                r = E.exp_router(A, form, mirror=A in (1, 2))
                out.append(r)
                self.assertEqual([row["P(d+)"] for row in r["rows"]], BORN, (A, form))
                self.assertTrue(all(row["both"] == 0 and row["none"] == 0 for row in r["rows"]))
                self.assertEqual([row["I+"] for row in r["rows"]], [x * A * A for x in (8, 6, 2, 0, 2, 6)])
                self.assertTrue(r["I_static"] and r["one_click_per_update"] and r["rewind"], (A, form))
                if form == "opposite":
                    self.assertTrue(r["r_plus_eq_r_minus_every_update"])
                if A in (1, 2):
                    self.assertTrue(r["mirror_M_F7_M_F7_id"] and r["mirror_log_reversed_same_kinds"])
                assert_recip(self, r["recip"], designated=True)
        save("TC.2", {"runs": out}, t0)

    def test_TC03_grangier(self):
        t0 = stamp()
        out = [E.exp_grangier(A) for A in (1, 2)]
        save("TC.3", {"runs": out}, t0)
        for r in out:
            self.assertTrue(r["rewind_mirror"] and r["rewind_opposite"])
            for row in r["rows"]:
                if row["s"] in (1, 2, 4, 5):
                    self.assertEqual(row["alpha"], "1", row)
        router = [E.exp_router(1, f, steps=1) for f in ("opposite", "mirror")]
        for r in router:                                   # shared token: P(both) = 0 -> alpha = 0
            self.assertTrue(all(row["both"] == 0 for row in r["rows"]))

    def test_TC04_mismatch(self):
        t0 = stamp()
        r = E.exp_mismatch()
        save("TC.4", r, t0)
        self.assertTrue(r["rows"])
        for row in r["rows"]:
            self.assertEqual(row["P(both)"], row["pred_both"], row)
            self.assertEqual(row["P(none)"], row["pred_none"], row)
            self.assertTrue(row["rewind"])
            if row["S"] <= row["D"]:
                self.assertEqual(row["P(+|one)"], row["I+/(I++I-)"], row)

    def test_TC05_token(self):
        t0 = stamp()
        r = E.exp_token()
        save("TC.5", r, t0)
        d, u = r["drive"], r["unstaged"]
        self.assertTrue(d["r+ == r- every update"] and d["visited_over_24_birth_times"] and d["rewind"])
        assert_recip(self, d["recip"], designated=True)
        self.assertTrue(u["r+ == r- every update"] and u["exactly one click every update"])
        self.assertTrue(u["N+ over any D consecutive updates == 6 I+"] and u["rewind"])
        self.assertEqual([row["P(+) over D readout times (every r0)"] for row in u["rows"]], [[p] for p in BORN])

    def test_TC06_sequential_router(self):
        t0 = stamp()
        out, ctrl = [], []
        for D_I, Q, kappa in ((8, 8, 3), (9, 3, 1), (12, 4, 1), (15, 5, 1)):
            for n in (3, 4):
                r = E.exp_sequential(D_I, Q, kappa, n)
                out.append(r)
                self.assertEqual(r["compositions"], {3: (D_I + 2) * (D_I + 1) // 2,
                                                     4: (D_I + 3) * (D_I + 2) * (D_I + 1) // 6}[n])
                self.assertEqual(r["non_exclusive_cases"], 0, r)
                self.assertEqual(r["non_Born_compositions"], 0, r)
                self.assertTrue(r["rewind"])
                assert_recip(self, r["recip"], designated=True)
        for n in (3, 4):
            c = E.exp_parallel(9, 3, 1, n, offsets_search=(n == 3))
            ctrl.append(c)
            self.assertGreater(c["failing_compositions"], 0, c)          # the control must FAIL
            self.assertTrue(c["rewind"])
            if n == 3:
                self.assertGreater(c["fixed_offset_min_failing_compositions"], 0, c)
        save("TC.6", {"sequential": out, "parallel_control": ctrl}, t0)

    def test_TC07_f7(self):
        t0 = stamp()
        r = E.exp_f7()
        save("TC.7", r, t0)
        cos = [["1"], ["1/2"], ["-1/2"], ["-1"], ["-1/2"], ["1/2"]]
        tB_front = E.F7_TA + 3 + E.F7_DIST
        self.assertEqual(r["first_snapshot_with_front_at_Bob"], tB_front)
        for tB, cone in r["cone_per_tB"].items():
            tB = int(tB)
            if tB >= tB_front:
                self.assertEqual(r["E_by_(a-b)_per_tB"][str(tB)], cos, tB)
                self.assertEqual(r["maxS_per_tB"][str(tB)], "5/2")
            else:
                self.assertEqual(r["E_by_(a-b)_per_tB"][str(tB)], [["0"]] * 6, tB)
                self.assertEqual(r["maxS_per_tB"][str(tB)], "0")
            if cone == "spacelike":
                self.assertLessEqual(abs(Fr(r["maxS_per_tB"][str(tB)])), 2)
            self.assertEqual(r["Bob_marginals_per_tB"][str(tB)], ["0"])
        self.assertEqual(r["Alice_marginals"], ["0"])
        self.assertEqual(r["bit_gate_S"], "4")
        self.assertTrue(r["alice_one_click_at_tA_only_and_bob_one_click_per_update"])
        self.assertTrue(r["front_zero_through_snapshot_tA+2"] and r["front_fibres_C0"] and r["rewind_all_runs"])
        assert_recip(self, r["recip"], designated=True)

    def test_TC08_all_or_nothing(self):
        t0 = stamp()
        r = E.exp_all_or_nothing()
        save("TC.8", r, t0)
        self.assertEqual((r["clicking"], r["configs"]), (72, 180))
        self.assertEqual(r["silent_bit_identical"], r["silent"])
        self.assertEqual(r["clicking_changed"], r["clicking"])
        self.assertGreaterEqual(r["min_final_disturbance_clicking"], 2)
        self.assertTrue(r["rewind"])
        assert_recip(self, r["recip"], designated=True)

    def test_TC09_m22_decoherence(self):
        t0 = stamp()
        out = {}
        for N, want in ((1, 0.808), (2, 0.833), (3, 0.650), (6, 0.262)):
            r = E.exp_m22(N, "exhaustive" if N <= 2 else "sample", L=16)
            out[N] = r
            self.assertEqual(r["V_ens"], want, (N, r["V_ens"]))
            self.assertTrue(r["rewind_checked_batches_ok"])
            assert_recip(self, r["recip"], designated=True)
        self.assertEqual(out[1]["V_single"], 0.915)
        self.assertEqual(out[1]["V_eraser"], 0.915)
        save("TC.9", {str(k): v for k, v in out.items()}, t0)

    def test_TC10_qm_deviation(self):
        t0 = stamp()
        out = []
        for A in (1, 2, 3):
            for c in (0, 1, 2):
                r = E.exp_dec(A, c)
                out.append(r)
                self.assertTrue(r["one_W_and_one_exit_click"] and r["rewind"] and r["M_F2_M_F2_id"], (A, c))
                assert_recip(self, r["recip"], designated=True)
                if c == 1:
                    self.assertEqual([x["P(+|s)"] for x in r["rows"]], ["1/2"] * 4)
                    self.assertEqual([x["P(+|s,W1)"] for x in r["rows"]], ["1", "1", "1", "0"])
                    self.assertEqual([x["P(+|s,W2)"] for x in r["rows"]], ["0", "0", "0", "1"])
                    self.assertEqual(r["I(s;exit)"], 0.0)
                    self.assertEqual(r["I(s;exit,record)"], 0.8113)
                if c == 0:
                    self.assertEqual([x["P(+|s)"] for x in r["rows"]], ["1", "1/2", "0", "1/2"])
                if c == 2:
                    self.assertEqual([x["P(+|s)"] for x in r["rows"]], ["0", "1/2", "1", "1/2"])
        save("TC.10", {"runs": out}, t0)

    def test_TC11_backaction(self):
        """OPEN item: reported as found; the asserted parts are the pre-registered ones (gradient, first update
        Born, rewind)."""
        t0 = stamp()
        out = [E.exp_backaction(g) for g in (0, 6)]
        save("TC.11", {"runs": out}, t0)
        for r in out:
            assert_recip(self, r["recip"], designated=False)
            self.assertEqual([x["P(d+)"] for x in r["first_update"]], BORN)
            self.assertTrue(all(x["both"] == 0 and x["none"] == 0 for x in r["first_update"]))
            self.assertTrue(r["rewind"])

    def test_TC11b_complete_spring_exploratory(self):
        """EXPLORATORY (manager ruling 2, pre-registered 09:54:36): the COMPLETE OD4 spring. Asserted: gradient with no
        designation, first click Born and exclusive, rewind exact (over the updates run). Reported: exclusivity after
        the first click and growth (runs stop once any value exceeds 256 bits)."""
        t0 = stamp()
        out = []
        for A in (1, 2, 3):
            for lam in (1, 2, 3, 6):
                r = E.exp_backaction(0, steps=12, A=A, spring_lam=lam, cap_bits=256)
                out.append(r)
                assert_recip(self, r["recip"], designated=False)
                self.assertEqual([x["P(d+)"] for x in r["first_update"]], BORN)
                self.assertTrue(all(x["both"] == 0 and x["none"] == 0 for x in r["first_update"]))
                self.assertTrue(r["rewind"])
        save("TC.11b", {"runs": out}, t0)

    def test_TC13_odd_q_routers(self):
        t0 = stamp()
        r = E.exp_odd_q()
        g = E.exp_gauge_q_router()
        r["gauge_Q"] = g
        save("TC.13", r, t0)
        self.assertEqual(r["parity"]["odd_Q_with_matched_router"], [])
        for x in r["sequential_n2"]:
            self.assertEqual((x["non_exclusive_cases"], x["non_Born_compositions"]), (0, 0), x)
            self.assertTrue(x["rewind"])
        self.assertEqual([x["compositions"] for x in r["sequential_n2"]], [10, 16])
        for x in r["near_matched"] + [g]:
            self.assertTrue(x["odd"] and x["rewind"], x)
            self.assertEqual([row["P(both)"] for row in x["rows"]], ["0"] * 6)
            self.assertEqual({row["P(none)"] for row in x["rows"]}, {x["pred_P(none)"]})
            self.assertEqual([row["P(+|detected)"] for row in x["rows"]], BORN)
        self.assertEqual([x["pred_P(none)"] for x in r["near_matched"]], ["1/9", "1/33", "1/33"])
        self.assertEqual(g["pred_P(none)"], "1/524289")

    def test_TC14_designation_audit(self):
        t0 = stamp()
        out = E.audit_all()
        save("TC.14", {"audits": out}, t0)
        for a in out:
            self.assertEqual(a["designated_coinciding_with_force"], [], a["experiment"])
            if a["experiment"] in ("all-or-nothing", "M2-2 N=6"):          # the declared two-way W pair
                self.assertTrue(a["partners_present"])
                self.assertTrue(all(p["partner_designated"] for p in a["partners_present"]))
                self.assertTrue(all("W." in p["partner"] or "W." in p["designated"] for p in a["partners_present"]))
            else:
                self.assertEqual(a["partners_present"], [], a["experiment"])
        r4 = {a["experiment"]: a["rank4_designated"] for a in out}
        self.assertEqual((r4["F7"], r4["M2-2 N=6"], r4["D12b c=1"]), (18, 18, 24))

    @unittest.expectedFailure
    def test_TC15_f7_odd_q(self):
        """F7 at ODD Q = 11 with near-matched pairs (pre-registration 3, 10:12:01): coincidence correlations.
        The pre-registered prediction FAILED (NOTES_choice.md, TC.15 DEVIATION): Bob's continuously exposed pair cannot
        be matched at odd Q and loses its equal-remainder lock; coincidence-conditioned E becomes +-1 (S = 4, a
        detection-loophole artefact). Kept, unchanged, as an expectedFailure record; TC.15b is the one-shot fix.
        Set CHOICE_FAST=1 to skip this 4-5 minute record run."""
        if os.environ.get("CHOICE_FAST"):
            self.skipTest("CHOICE_FAST")
        t0 = stamp()
        r = E.exp_f7_odd()
        save("TC.15", r, t0)
        self.assertTrue(r["odd"] and r["never_two_clicks"] and r["rewind_all_runs"])
        self.assertEqual(r["P_alice_detects"], ["32/33"])
        self.assertEqual(r["P_bob_no_click_per_update"], ["1/33"])
        cos = [["1"], ["1/2"], ["-1/2"], ["-1"], ["-1/2"], ["1/2"]]
        for tB in range(14):
            if tB >= E.F7_TA + 3 + E.F7_DIST:
                self.assertEqual(r["E_cond_by_(a-b)_per_tB"][str(tB)], cos, tB)
                self.assertEqual(r["maxS_cond_per_tB"][str(tB)], "5/2")
                self.assertEqual(r["E_uncond_at_a_eq_b_per_tB"][str(tB)], [str(Fr(32, 33) ** 2)])
            else:
                self.assertEqual(r["E_cond_by_(a-b)_per_tB"][str(tB)], [["0"]] * 6, tB)
                self.assertEqual(r["maxS_cond_per_tB"][str(tB)], "0")
        assert_recip(self, r["recip"], designated=True)

    def test_TC15b_f7_odd_q_gated_bob(self):
        """F7 at ODD Q = 3 with a ONE-SHOT (flash-gated) Bob (pre-registration 5, 10:17:35)."""
        t0 = stamp()
        r = E.exp_f7_gated()
        save("TC.15b", r, t0)
        self.assertTrue(r["odd"] and r["rewind_all_runs"])
        cos = [["1"], ["1/2"], ["-1/2"], ["-1"], ["-1/2"], ["1/2"]]
        for tB, want_E, want_S in (("9", cos, "5/2"), ("6", [["0"]] * 6, "0")):
            x = r["per_tB"][tB]
            self.assertEqual((x["P_alice_detects"], x["P_bob_detects"]), (["8/9"], ["8/9"]))
            self.assertEqual(x["bob_clicks_outside_gate"], 0)
            self.assertFalse(x["two_clicks_in_a_pair"])
            self.assertEqual(x["E_cond_by_(a-b)"], want_E)
            self.assertEqual(x["maxS_cond"], want_S)
        self.assertEqual(r["per_tB"]["6"]["cone"], "spacelike")
        assert_recip(self, r["recip"], designated=True)

    def test_TC16_f7_spacelike_copy_reader(self):
        """S5-M2's spacelike photon-copy reader (pre-registration 4, 10:13:00): an LHV reader gives S = 5/4 <= 2."""
        t0 = stamp()
        r = E.exp_f7_copy_reader()
        save("TC.16", r, t0)
        self.assertEqual(r["E_by_(a-b)"], [["1/2"], ["1/4"], ["-1/4"], ["-1/2"], ["-1/4"], ["1/4"]])
        self.assertEqual(r["maxS"], "5/4")
        self.assertEqual(r["Bob_marginals"], ["0"])
        self.assertTrue(r["one_click_each_at_update_1"] and r["no_front_at_Bob"] and r["rewind_all_runs"])

    def test_TC17_f7_light_carrier_probe(self):
        """STATUS PROBE (pre-registration 6, 10:30:05): the F7 front on the headroom light gear (round cone), odd Q,
        A = 30, 100, 300. Asserted: (i) E = 0 exactly for t_B <= 8, (ii) max|S| <= 2 in the gap t_B = 9, 10, (iv) exact
        rewind, reciprocity. NOT asserted (pre-registered as not claimed, and found NOT met): E -> cos(a - b) (beating
        front; reader clipping gives S up to 3.4 where the front exceeds Bob's clock)."""
        t0 = stamp()
        out = []
        for A in (30, 100, 300):
            r = E.exp_f7_light(A)
            out.append(r)
            self.assertTrue(r["odd"] and r["rewind_all_runs"], A)
            for t in range(0, 9):
                self.assertEqual(r["per_tB"][str(t)]["max|E|"], 0.0, (A, t))
            for t in (9, 10):
                self.assertLessEqual(r["per_tB"][str(t)]["maxS"], 2.0, (A, t))
            self.assertLess(r["round_first_snapshot"], 11)
            assert_recip(self, r["recip"], designated=True)
        save("TC.17", {"runs": out}, t0)

    def test_TC12_census_and_reversors(self):
        t0 = stamp()
        r = E.exp_reversors()
        save("TC.12", r, t0)
        self.assertEqual(r["router_Q8"]["Mp_failures"], 0)
        self.assertEqual(r["all_or_nothing_Q5"]["Mp_failures"], 0)
        self.assertEqual(r["Mp_fixed_remainders_Q3"], [8, 9])
        self.assertEqual(r["Mp_fixed_remainders_Q5"], [14, 15])
        self.assertEqual(r["Mp_fixed_remainders_Q4"], [])
        self.assertEqual(r["Mp_fixed_remainders_Q8"], [])
        self.assertTrue(r["vacuum_3Q-1_Mp_fixed_Q5"] and r["vacuum_run_Q5_stays_vacuum"])
        self.assertGreater(r["f7_Q4"]["Mp_failures"], 0)        # declared: no per-gear mirror for the a-read F7 block


if __name__ == "__main__":
    unittest.main()
