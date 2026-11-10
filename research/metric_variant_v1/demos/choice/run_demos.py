"""Headline demos of the CHOICE layer (B1-CHOICE). Prints exact tables; nothing is written.

    OMP_NUM_THREADS=2 nice -n 10 python research/metric_variant_v1/demos/choice/run_demos.py [router|token|seq|f7|dec|m22|ba|all]

* router : Born router (paired link clock), P(d+) = cos^2(phi/2) exactly, one click, Grangier alpha;
* token  : the board-made token (equal remainders born from the vacuum; sigma-delta Born over readout times);
* seq    : sequential n-exit router, all compositions, and the parallel-read control that fails;
* f7     : the light-cone choice: E(a - b) per readout time, max S, the cone, the bit gate (about 90 s);
* dec    : the QM-deviating which-path toy (P(+|record) = 1, 1, 1, 0);
* m22    : decoherence with S5-P2R's definitions (N = 1, 2 exhaustive);
* ba     : back-acting reciprocal detectors (exclusivity after the first click, growth);
* oddq   : Born routers at ODD Q (parity obstruction, n = 2 sequential, near-matched pairs, gauge Q = 2^19 + 1);
* copy   : F7's spacelike photon-copy reader (S = 5/4) and the odd-Q one-shot F7 (S = 5/2 on coincidences).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.metric_variant_v1.demos.choice import experiments as E  # noqa: E402


def router():
    r = E.exp_router(1, "opposite")
    print("BORN ROUTER (paired link clock: equal remainders, inputs +I+, -I-), A = 1, D = 48, all 48 tokens:")
    for row in r["rows"]:
        print(f"  s = {row['s']} (phi = {60 * row['s']:3d} deg): I+ = {row['I+']}, I- = {row['I-']}: P(d+) = "
              f"{row['P(d+)']:>4}, P(d-) = {row['P(d-)']:>4}, both = {row['both']}, none = {row['none']}")
    print(f"  r+ = r- at every update: {r['r_plus_eq_r_minus_every_update']}; one click per update: "
          f"{r['one_click_per_update']}; rewind: {r['rewind']}")
    g = E.exp_grangier(1)
    al = sorted({row["alpha"] for row in g["rows"] if row["alpha"]})
    print(f"  Grangier: independent tokens alpha = {al}; shared token P(both) = 0 -> alpha = 0")


def token():
    r = E.exp_token()
    print("BOARD-MADE TOKEN:", {k: v for k, v in r["drive"].items() if k != "recip"})
    print("  unstaged:", {k: v for k, v in r["unstaged"].items() if k != "rows"})
    for row in r["unstaged"]["rows"]:
        print("   ", row)


def seq():
    for n in (3, 4):
        r = E.exp_sequential(9, 3, 1, n)
        c = E.exp_parallel(9, 3, 1, n)
        print(f"SEQUENTIAL n = {n}, D_I = 9 (Q = 3, odd): {r['compositions']} compositions x {r['tokens']} tokens: "
              f"non-exclusive {r['non_exclusive_cases']}, non-Born {r['non_Born_compositions']} | PARALLEL control: "
              f"{c['failing_compositions']}/{c['compositions']} compositions fail")


def f7():
    r = E.exp_f7()
    print(f"F7 LIGHT-CONE CHOICE (Q = 4, D = 24, d = {r['d']}, Alice's click at update t_A = {r['t_A']}):")
    for tB in sorted(r["maxS_per_tB"], key=int):
        E_ = [v[0] if len(v) == 1 else v for v in r["E_by_(a-b)_per_tB"][tB]]
        print(f"  Bob reads snapshot {int(tB):2d} ({r['cone_per_tB'][tB]:9s}): E(a-b = 0..300 deg) = {E_}, "
              f"max S = {r['maxS_per_tB'][tB]}")
    print(f"  bit gate (designed reader of the same front): S = {r['bit_gate_S']}; marginals: Alice "
          f"{r['Alice_marginals']}; Bob's clock click sizes {r['Bob_clock_B0_click_sizes']}")


def dec():
    for c in (0, 1, 2):
        r = E.exp_dec(1, c)
        print(f"D12b kick {90 * c:3d} deg: " + "; ".join(f"s={x['s']}: P(+|s)={x['P(+|s)']}, P(+|s,W1)={x['P(+|s,W1)']}"
                                                      for x in r["rows"])
              + f"; I(s;exit) = {r['I(s;exit)']}, I(s;exit,record) = {r['I(s;exit,record)']}")


def m22():
    for N in (1, 2):
        r = E.exp_m22(N, "exhaustive", L=16)
        print(f"M2-2 N = {N}: V_ens {r['V_ens']}, V_single {r['V_single']}, V_eraser {r['V_eraser']}, V_1 {r['V_1']}")


def oddq():
    r = E.exp_odd_q()
    print("ODD Q: matched polarization routers exist for odd Q <= 999:", r["parity"]["odd_Q_with_matched_router"])
    for x in r["sequential_n2"]:
        print(f"  n = 2 sequential, D_I = {x['D_I']}, Q = {x['Q']}: non-exclusive {x['non_exclusive_cases']}, "
              f"non-Born {x['non_Born_compositions']} of {x['compositions']}")
    for x in r["near_matched"] + [E.exp_gauge_q_router()]:
        print(f"  near-matched pair Q = {x['Q']}: P(none) = {x['pred_P(none)']}, P(+|detected) = "
              f"{[row['P(+|detected)'] for row in x['rows']]}, P(both) = 0: {all(row['P(both)'] == '0' for row in x['rows'])}")


def copy():
    r = E.exp_f7_copy_reader()
    print(f"F7 spacelike photon-copy reader: E(a-b) = {r['E_by_(a-b)']}, max S = {r['maxS']}")
    g = E.exp_f7_gated()
    for tB, x in g["per_tB"].items():
        print(f"F7 odd Q = {g['Q']}, one-shot Bob at t_B = {tB} ({x['cone']}): E_cond = {x['E_cond_by_(a-b)']}, "
              f"max S = {x['maxS_cond']}, detection A/B = {x['P_alice_detects']}/{x['P_bob_detects']}")


def ba():
    for g in (0, 6):
        r = E.exp_backaction(g)
        print(f"BACK-ACTION (reciprocal, rank {r['rank']}, g = {g}): first update P(d+) = "
              f"{[x['P(d+)'] for x in r['first_update']]}; exactly-one per update "
              f"{[x['exactly_one'] for x in r['per_update']]} of {r['members']}; bits of max|b| {r['max_abs_arm_b_bits']}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["router", "token", "seq", "dec", "m22", "ba"]
    if which == ["all"]:
        which = ["router", "token", "seq", "f7", "dec", "m22", "ba", "oddq", "copy"]
    for w in which:
        {"router": router, "token": token, "seq": seq, "f7": f7, "dec": dec, "m22": m22, "ba": ba, "oddq": oddq,
         "copy": copy}[w]()
