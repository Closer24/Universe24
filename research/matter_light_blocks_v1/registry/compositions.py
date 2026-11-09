"""Reference compositions: r11's D1 module written as placements of registered blocks (r21).

``d1_main_spec(100)`` regenerates the published block ``d1_local_atom_L100``,
``d1_main_spec(200, tiles=2)`` regenerates ``d1_local_atom_L200``, its ``no_seed`` control
regenerates ``d1_control_no_seed_L100``, and ``d1_skeleton_spec(160)`` regenerates
``d1_skeleton_atom_spin_clocks_L160`` (same complete initial state and coupling).
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import math

from universe24 import Coupling
from universe24.core.group_2o import group as _group

from . import guides as G
from .compose import FORMAT
from .generators import bundle_halo_ok, field_line, field_line_bundle_lines, staircase_dirs  # noqa: F401


def d1_skeleton_spec(L=160, tiles=1):
    """The r11 'flagship v3 skeleton': atom module, four recorder clocks and a holonomy-z ring."""
    Lb = L // tiles
    pl = []
    for i in range(tiles):
        for x in (0, 13):
            pl.append({"name": f"A{x}_{i}", "block": "matter_line@1",
                       "params": {"length": L, "sockets": [4, 5, 6] if (x == 0 and i == 0) else []},
                       "at": [x + i * Lb, 0, 3], "wrap": True})
    for j in range(tiles):
        for y, ph in ((0, 1), (12, 0)):
            pl.append({"name": f"B{y}_{j}", "block": "light_line@1", "params": {"length": L, "gauge_phase": ph},
                       "at": [0, y + j * Lb, 4], "wrap": True})
    clocks = []
    for i in range(tiles):
        for j in range(tiles):
            for x, st, role in ((10, [-1, 0, 0], "core"), (18, [-1, 0, 0], "core"), (25, [0, -1, 4], "rec"),
                                (29, [0, -1, 4], "rec"), (33, [0, -1, 4], "rec"), (37, [0, -1, 4], "rec")):
                name = f"{role}{x}_{i}{j}"
                clocks.append(name)
                pl.append({"name": name, "block": "slot_clock@1", "params": {"state": st},
                           "at": [x + i * Lb, 12 + j * Lb, 4]})
            pl.append({"name": f"ring_{i}{j}", "block": "spin_ring_z@1", "params": {},
                       "at": [13 + i * Lb, (-20 + j * Lb) % L, 3], "wrap": True})
    pl.append({"name": "seed", "block": "slow_glider@1", "params": {"start": 6, "hit": "SLOW"},
               "at": [0, 0, 3], "wrap": True})
    want = {}
    for i in range(tiles):
        for j in range(tiles):
            for xa, yb, cls in ((0, 0, 2), (13, 0, 0), (13, 12, 2), (0, 12, 0)):
                want[f"{xa + i * Lb},{yb + j * Lb}"] = cls
    return {"format": FORMAT, "id": f"d1_v3_skeleton_L{L}",
            "board": {"side": L, "background": [0, 0, 2], "coupling": {"signs": [-1, 1, 1], "variant": None}},
            "placements": pl,
            "assertions": {"junction_classes": want, "slot_clocks_silent": clocks},
            "timing": {"t0": 0, "declared": {"t_A1": 29, "t_c": 80, "trap_period": 20, "ring_lap": 18,
                                             "recorder_clicks": [[81, 82], [85, 86], [89, 90], [93, 94]]}},
            "steps": 240,
            "observables": {"decoder": "r17 generic click decoder (version recorded at run time)"}}


def d1_main_spec(L=100, tiles=1):
    """The D1 local atom alone: the skeleton without recorders and spin ring, with three controls."""
    spec = d1_skeleton_spec(L, tiles)
    spec["id"] = f"d1_main_L{L}"
    spec["placements"] = [p for p in spec["placements"]
                          if not (p["name"].startswith("rec") or p["name"].startswith("ring"))]
    spec["assertions"]["slot_clocks_silent"] = [n for n in spec["assertions"]["slot_clocks_silent"]
                                                if n.startswith("core")]
    spec["steps"] = 240
    spec["controls"] = [
        {"name": "no_seed", "remove": ["seed"], "unfill_sockets": True},
        {"name": "no_cores", "remove": [p["name"] for p in spec["placements"] if p["name"].startswith("core")]},
        {"name": "B0_phase0", "override": {f"B0_{j}": {"gauge_phase": 0} for j in range(tiles)},
         "assertions": {"junction_classes": None}},
    ]
    return spec


# ===================================================================== WAVE 2 (r21)
PPP, MPP = [1, 1, 1], [-1, 1, 1]
F = [1, 0, -1]


def _board(side, signs, bg=(0, 0, 2)):
    return {"side": side, "background": list(bg), "coupling": {"signs": list(signs), "variant": None}}


def plus_fibre(name, x0, x1, y, z, arrivals=(), g0=0, sigma0=1):
    """r08 fibre as ``pulse_train@1``: channel g0 along +x from x0 to x1 at (y, z), rest (0,0,4) (sigma +1);
    each arrival (m, t_arr) is a (1,0,-1) pulse whose head reaches board node x = m at update t_arr."""
    return {"name": name, "block": "pulse_train@1",
            "params": {"length": x1 - x0 + 1, "arrivals": [[m - x0, t] for m, t in arrivals], "g0": g0,
                       "sigma0": sigma0},
            "at": [x0, y, z]}


# ---------------------------------------------------------------------------- r08 W9
def w9_chsh_spec(arrangement, x, y, lam, mA=96, mB=56, yA=40, yB=56, side=256, zc=64):
    """r08 clicktime.chsh_cells as a composition (2 fibres, 2 phase gates, source / setting pulses)."""
    t_set = mA - (mB + 4)
    tA = 16 + 2 * lam if arrangement == "separated" else t_set + 20 + 2 * lam
    arrA = ([(mA, t_set)] if y else []) + [(mA, tA)]
    pl = [plus_fibre("FA", 1, side - 2, yA, zc, arrA), plus_fibre("FB", 1, side - 2, yB, zc, [(mB, 28 + 2 * lam)]),
          {"name": "GA", "block": "phase_gate@2", "params": {"phase": 2 if x == 0 else 0, "offset": [0, 2, 0]},
           "at": [mA, yA, zc]},
          {"name": "GB", "block": "phase_gate@2", "params": {"phase": 2, "offset": [0, 2, 0]}, "at": [mB, yB, zc]}]
    return {"format": FORMAT, "id": f"w9_chsh_{arrangement}_x{x}_y{y}_lam{lam}", "board": _board(side, PPP),
            "placements": pl, "assertions": {"beside_fibre": [["GA", "FA.F_nodes"], ["GB", "FB.F_nodes"]]},
            "timing": {"t0": 0, "declared": {"t_set": t_set if y else None, "tA": tA, "tB": 28 + 2 * lam}},
            "steps": 80, "observables": {"decoder": "research.click_decoder_v1 (version in its report)"},
            "settings": {"x": x, "y": y, "lambda": lam, "arrangement": arrangement}}


def w9_two_detector_spec(t_arr=41, m=60, y1=40, y2=50, side=256, zc=64, x0=1, x1=None):
    """r08 W9 single approval: gates half a period apart beside two fibres; one approval each at t_arr."""
    x1 = side - 2 if x1 is None else x1
    pl = [plus_fibre("F1", x0, x1, y1, zc, [(m, t_arr)]), plus_fibre("F2", x0, x1, y2, zc, [(m, t_arr)]),
          {"name": "D1", "block": "phase_gate@2", "params": {"phase": 0, "offset": [0, 2, 0]}, "at": [m, y1, zc]},
          {"name": "D2", "block": "phase_gate@2", "params": {"phase": 2, "offset": [0, 2, 0]}, "at": [m, y2, zc]}]
    return {"format": FORMAT, "id": f"w9_two_detector_tarr{t_arr}", "board": _board(side, PPP), "placements": pl,
            "assertions": {"beside_fibre": [["D1", "F1.F_nodes"], ["D2", "F2.F_nodes"]]},
            "timing": {"t0": 0, "declared": {"t_arr": t_arr, "exactly_one_of": ["D1", "D2"],
                                             "D1_if_t_arr_mod4_in": [1, 2], "D2_if_t_arr_mod4_in": [3, 0]}},
            "controls": [{"name": "no_gates", "remove": ["D1", "D2"]},
                         {"name": "no_approval", "override": {"F1": {"packets": []}, "F2": {"packets": []}}}],
            "steps": 70}


# ---------------------------------------------------------------------------- r03 Q1c selector
def q1c_selector_spec(t_q=36, approval=True, q1=True, q2=True, side=160, M=80, T_A=22, GAP=16, dy_B=40, z=None):
    """r03 Q1c: two arms (r08 absorber blocks: fibres y=c, c+4 and an all-48 gate at (M, c+2, c)), the
    approval on arm A's fibre 1, quanta on fibre 1 of both arms; arm B is shifted +dy_B in y (r03 joint)."""
    c = side // 2
    z = c if z is None else z
    pl = []
    for arm, dy in (("A", 0), ("B", dy_B)):
        arr = ([(M, T_A)] if (approval and arm == "A") else []) + ([(M, t_q)] if q1 else []) + \
              ([(M, t_q + GAP)] if q2 else [])
        pl.append(plus_fibre(f"F1{arm}", 1, side - 2, c + dy, z, arr))
        pl.append(plus_fibre(f"F2{arm}", 1, side - 2, c + 4 + dy, z, []))
        pl.append({"name": f"G{arm}", "block": "phase_gate@2", "params": {"phase": 0, "offset": [0, 2, 0]},
                   "at": [M, c + dy, z]})
    return {"format": FORMAT, "id": f"q1c_selector_tq{t_q}", "board": _board(side, PPP), "placements": pl,
            "assertions": {"beside_fibre": [["GA", "F1A.F_nodes"], ["GB", "F1B.F_nodes"]]},
            "timing": {"t0": 0, "declared": {"t_q": t_q, "approval_at": T_A,
                                             "selected": "A if t_q mod 4 in {3,0} else B (with approval)"}},
            "steps": t_q + GAP + 24}


# ---------------------------------------------------------------------------- r12 approval router
def junction_y_paths(J=18, main_len=37, branch_len=30):
    return [{"name": "main", "g0": 0, "dirs": [[0, main_len - 1]]},
            {"name": "B", "branch_of": "main", "at_node": J, "dir": 2, "length": branch_len}]


def approval_router_spec(arm="x", signal=True, approval=True, side=64, origin=(2, 32, 32), J=18, mirror=14, f=F,
                         signal_mask=None):
    """r12 E7: r04 junction_Y + a stem signal (lead len(f)+1) + an inward approval on ``arm`` at the mirror
    position (``mirror`` sites out): both reach the junction at the same update; only the other arm transmits."""
    packets = [{"path": "main", "f": f, "lead": len(f) + 1}] if signal else []
    if signal_mask == "halo":       # r12's controls: signal node cells at rest, its halo remainders kept
        packets = [{"path": "main", "f": f, "lead": len(f) + 1, "keep": "halo"}]
    if approval:
        if arm == "x":
            packets.append({"path": "~main", "f": f, "lead": (36 - J) - mirror})
        else:
            packets.append({"path": ["~B", f"main[{J}:{J + 1}]", f"~main[:{J}]"], "f": f, "lead": 30 - mirror})
    return {"format": FORMAT, "id": f"approval_router_{arm}" + ("" if signal else "_approval_only") +
            ("" if approval else "_no_approval"),
            "board": _board(side, PPP),
            "placements": [{"name": "router", "block": "guide_net@1",
                            "params": {"paths": junction_y_paths(J), "packets": packets}, "at": list(origin)}],
            "timing": {"t0": 0, "declared": {"meeting_update": J - (len(f) + 1) + 1 if signal else None}},
            "steps": 32}


# ---------------------------------------------------------------------------- r13 approved beam splitter
def r13_device_spec(q_arrival=None, appr_arrival=None, phases=None, L=200, X0=10, XJ=70, nA=110, nB=90, k=20,
                    k2=None, steps=94, name=None, extra_packets=()):
    """r13 Device: input line + junction (r04 degree 3) + arms A, B; all-48 gates two sites below arm nodes at
    path length k (and k2); the quantum is one packet on the main line; the approval one packet on arm A."""
    c = L // 2
    iJ = XJ - X0
    packets = []
    if q_arrival is not None:
        packets.append({"path": "main", "f": F, "lead": iJ + k - q_arrival})
    if appr_arrival is not None:
        packets.append({"path": f"main[{iJ + 1}:]", "f": F, "lead": (k - 1) - appr_arrival})
    for ep in extra_packets:       # e.g. an inward packet: {"path": ["~armB", "main[60:61]", "~main[:60]"], "lead": n}
        packets.append({"path": ep["path"], "f": ep.get("f", F), "lead": ep["lead"]})
    paths = [{"name": "main", "g0": 0, "dirs": [[0, iJ + nA]]},
             {"name": "armB", "branch_of": "main", "at_node": iJ, "dir": 2, "length": nB}]
    pl = [{"name": "dev", "block": "guide_net@1", "params": {"paths": paths, "packets": packets}, "at": [X0, c, c]}]
    phases = phases or {}
    sites = {"A": (XJ + k, c, c), "B": (XJ, c + k, c)}
    if k2 is not None:
        sites.update({"A2": (XJ + k2, c, c), "B2": (XJ, c + k2, c)})
    for nm, ph in phases.items():
        pl.append({"name": "D" + nm, "block": "phase_gate@2", "params": {"phase": ph, "offset": [0, 0, -2]},
                   "at": list(sites[nm])})
    return {"format": FORMAT, "id": name or "r13_device", "board": _board(L, PPP), "placements": pl,
            "assertions": {"beside_fibre": [["D" + nm, "dev.main_nodes" if nm.startswith("A") else "dev.armB_nodes"]
                                            for nm in phases]},
            "steps": steps}


def r13_cases():
    """The seven r13/make_preps.py init files as compositions (arrival times, not leads)."""
    return {
        "E1_F_app_tq24_selects_A": r13_device_spec(24, 10, {"A": 0, "B": 0}, k2=28, steps=94),
        "E1_F_app_tq25_selects_B": r13_device_spec(25, 10, {"A": 0, "B": 0}, k2=28, steps=95),
        "E1_F_app_control_no_quantum": r13_device_spec(None, 10, {"A": 0, "B": 0}, k2=28, steps=100),
        "E1_F_none_tq25_both": r13_device_spec(25, None, {"A": 0, "B": 0}, k2=28, steps=95),
        "E1_F_ind_pA2_pB0_tq23_complementary": r13_device_spec(23, None, {"A": 2, "B": 0}, k2=28, steps=53),
        "E2_R_delta0_tq23_repeat": r13_device_spec(23, None, {"A": 2, "B": 0, "A2": 2, "B2": 0}, k2=28, steps=63),
        "E2_R_delta2_tq23_collapse_test": r13_device_spec(23, None, {"A": 2, "B": 0, "A2": 0, "B2": 2}, k2=28,
                                                          steps=63),
        # junction merge law (time reverse of the copy): the quantum and an inward packet on arm B meet at the
        # junction at the same update and leave as one packet on arm A (r13 T1 / T-B; same law as r12's router)
        "E3_T1_single_arm_by_rewind": r13_device_spec(30, None, None, steps=50, extra_packets=[
            {"path": ["~armB", "main[60:61]", "~main[:60]"], "lead": 80}]),
        "E3_T2_collapsed_history_by_rewind": r13_device_spec(24, 10, {"A": 0, "B": 0}, steps=94, extra_packets=[
            {"path": ["~armB", "main[60:61]", "~main[:60]"], "lead": 86}]),
    }


# ---------------------------------------------------------------------------- r11 twins
def twins_spec(L=160, tiles=1, q2=12, a=3, s1=(-1, 0, 0), s2=(-1, 0, 0), XA=3, XB=150):
    """r11 W2 twin created atoms: D1 + a segment light line B-1 at y = -q2 (phase 0) on x in [XA, XB] with
    two cores at x = 13 - a and 13 - a + 8 (r11 twins2.seg_cells); every element tiled with the pitch."""
    spec = d1_main_spec(L, tiles)
    spec.pop("controls", None)
    spec["id"] = f"twins_seg_q2{q2}_a{a}_L{L}"
    Lb = L // tiles
    for i in range(tiles):
        for j in range(tiles):
            y = (-q2 + j * Lb) % L
            spec["placements"].append({"name": f"Bm{q2}_{i}{j}", "block": "light_line@1",
                                       "params": {"length": XB - XA + 1, "gauge_phase": (0 + XA) % 2},
                                       "at": [XA + i * Lb, y, 4]})
            for x, st in ((13 - a, s1), (13 - a + 8, s2)):
                nm = f"lcore{x}_{i}{j}"
                spec["placements"].append({"name": nm, "block": "slot_clock@1", "params": {"state": list(st)},
                                           "at": [x + i * Lb, y, 4]})
                spec["assertions"]["slot_clocks_silent"].append(nm)
            spec["assertions"]["junction_classes"][f"{13 + i * Lb},{y}"] = 2
    spec["steps"] = 260
    spec["timing"] = {"t0": 0, "declared": {"t_c_upper": 80, "t_c_lower": 80 - 3 * (12 - q2), "period": 20}}
    return spec


# ---------------------------------------------------------------------------- r06b flagship v3
def flagship_v3_spec(L=160, w9_z=80, q1c_z=(110, 130), with_twins=True, with_w9=True, with_q1c=True,
                     w9_t_arr=41, q1c_t_q=36):
    """D1 skeleton (atom + recorders + spin ring) + twin lower trap + r08's W9 two-detector device and r03's
    Q1c selector moved by gauge transport (+++ -> (-,+,+): character + staggered, even L) into planes far
    from the network. One board, one coupling; every part a registered block."""
    spec = d1_skeleton_spec(L, 1)
    spec["id"] = f"flagship_v3_L{L}"
    if with_twins:
        tw = twins_spec(L, 1, 12, 3)
        names = {p["name"] for p in spec["placements"]}
        for p in tw["placements"]:
            if p["name"] not in names:
                spec["placements"].append(p)
        spec["assertions"]["slot_clocks_silent"] += [n for n in tw["assertions"]["slot_clocks_silent"]
                                                     if n.startswith("lcore")]
        spec["assertions"]["junction_classes"].update(tw["assertions"]["junction_classes"])
    gauge = {"character": True, "staggered": True}
    groups = {}
    if with_w9:
        w9 = w9_two_detector_spec(w9_t_arr, m=60, y1=40, y2=50, side=L, zc=0, x0=1, x1=L - 2)
        spec["placements"].append({"name": "w9", "include": w9, "at": [0, 0, w9_z], "gauge": gauge, "prefix": "w9_"})
        groups["w9"] = ["w9_" + p["name"] for p in w9["placements"]]
    if with_q1c:
        q = q1c_selector_spec(q1c_t_q, side=L, z=0, dy_B=0)
        for arm, z in zip(("A", "B"), q1c_z):
            sub = {**q, "placements": [p for p in q["placements"] if p["name"].endswith(arm)],
                   "assertions": {"beside_fibre": [[f"G{arm}", f"F1{arm}.F_nodes"]]}}
            spec["placements"].append({"name": "q1c" + arm, "include": sub, "at": [0, 0, z], "gauge": gauge,
                                       "prefix": f"q1c{arm}_"})
            groups["q1c" + arm] = [f"q1c{arm}_" + p["name"] for p in sub["placements"]]
    net = [p["name"] for p in spec["placements"] if "include" not in p]
    spec["assertions"]["clearance"] = [{"a": net, "b": g, "min": 20} for g in groups.values()]
    spec["steps"] = 240
    spec["timing"]["declared"].update({"w9_t_arr": w9_t_arr, "q1c_t_q": q1c_t_q,
                                       "note": "W9/Q1c run as independent modules (no light link to the network)"})
    spec["limits"] = ["the twins' lower trap (13,-12) lies on the created -y glider's path to the ring at (13,-20): "
                      "this combination is not yet run natively (r06b to test)",
                      "D1 debris starts near t = L+34; it may reach the gauged modules late in a 240-update run",
                      "gauge transport swaps C1<->C2 on flipped channels of the W9/Q1c modules (decoder note)"]
    return spec


# ---------------------------------------------------------------------------- r12 Bell device
def bell_router_spec(phi_A=0, phi_B=0, q_arrival_A=None, approval_arrival=None, router_arm=None, L=200,
                     kA=60, kB=60, X0=10, XJ=70, nA=110, nB=90, steps=None):
    """Superposition / which-path / correlation device (r12): one quantum on the input line, a degree-3 junction
    (beam splitter), two long arms to distant stations A and B; each station a phase gate whose orbit phase is
    the local SETTING (phi_A, phi_B in 0..3); optional approval packet on arm A (r03/r13 approval), or an
    approval_router (r12) that sends the quantum into one arm only (router_arm = 'A' or 'B')."""
    c = L // 2
    iJ = XJ - X0
    qa = q_arrival_A if q_arrival_A is not None else iJ + kA - 4      # default: quantum head at input node 4
    packets = [{"path": "main", "f": F, "lead": iJ + kA - qa}]
    if approval_arrival is not None:
        packets.append({"path": f"main[{iJ + 1}:]", "f": F, "lead": (kA - 1) - approval_arrival})
    if router_arm is not None:
        lead_q = packets[0]["lead"]
        t_meet = iJ - lead_q
        if router_arm == "A":       # inward packet on arm B so that the quantum leaves on arm A
            packets.append({"path": ["~armB", f"main[{iJ}:{iJ + 1}]", f"~main[:{iJ}]"], "f": F, "lead": nB - t_meet})
        else:                       # inward packet on arm A so that the quantum leaves on arm B
            packets.append({"path": "~main", "f": F, "lead": nA - t_meet})
    paths = [{"name": "main", "g0": 0, "dirs": [[0, iJ + nA]]},
             {"name": "armB", "branch_of": "main", "at_node": iJ, "dir": 2, "length": nB}]
    pl = [{"name": "dev", "block": "guide_net@1", "params": {"paths": paths, "packets": packets}, "at": [X0, c, c]},
          {"name": "DA", "block": "phase_gate@2", "params": {"phase": phi_A, "offset": [0, 0, -2]},
           "at": [XJ + kA, c, c]},
          {"name": "DB", "block": "phase_gate@2", "params": {"phase": phi_B, "offset": [0, 0, -2]},
           "at": [XJ, c + kB, c]}]
    return {"format": FORMAT, "id": f"bell_router_phiA{phi_A}_phiB{phi_B}" + (f"_route{router_arm}" if router_arm else ""),
            "board": _board(L, PPP), "placements": pl,
            "assertions": {"beside_fibre": [["DA", "dev.main_nodes"], ["DB", "dev.armB_nodes"]]},
            "settings": {"phi_A": phi_A, "phi_B": phi_B, "router_arm": router_arm},
            "timing": {"t0": 0, "declared": {"q_arrival_A": qa, "q_arrival_B": qa - kA + kB}},
            "steps": steps or (qa + 40)}


# ---------------------------------------------------------------------------- r27 targets
def target_quiet_clocks_spec(L=40):
    """Target T_B (control for the backward method): disjoint periodic matter blocks in the quiet +++ vacuum.
    Every part is an exact periodic orbit, so its backward image is the same set at earlier phases: no
    Big Bang can be found from such a target (N2, periodic orbits have no birth)."""
    pl = [{"name": "M4", "block": "all48_site@1", "params": {"triple": [-1, -1, 0]}, "at": [5, 5, 5]},
          {"name": "D5", "block": "k_core@1", "params": {"shape": "dimer", "phase": 3}, "at": [5, 20, 5]},
          {"name": "C6", "block": "k_core@1", "params": {"shape": "cube", "phase": 4, "core_remainder": 0},
           "at": [20, 5, 20]},
          {"name": "B10", "block": "all48_site@1", "params": {"triple": [2, 2, 2]}, "at": [20, 25, 5]},
          {"name": "I6", "block": "single_channel@1", "params": {"channel": 0, "triple": [0, 2, 2]}, "at": [30, 30, 30]}]
    names = [p["name"] for p in pl]
    return {"format": FORMAT, "id": "target_quiet_clocks", "board": _board(L, PPP), "placements": pl,
            "assertions": {"clearance": [{"a": [names[i]], "b": [names[j]], "min": 5}
                                         for i in range(len(names)) for j in range(i + 1, len(names))]},
            "backward": {"rule": "S0 = JR(F^N(JR(T))) (THEORY S6); run JR(T) forward N updates natively",
                         "N": 60, "expected": "periodic parts only: S0 is T at earlier phases (no seed)"},
            "steps": 60}


def target_d1_products_spec(L=100):
    """Target T_A: the products of a local creation on D1 hardware, composed directly at time T:
    a SLOW / SLOW_LEFT glider pair on A1 moving apart from the class-0 junction (13,0), and the D1
    hardware with its trap. Its backward image converges the gliders on the junction (r27 searches
    for targets whose backward image is a small seed)."""
    spec = d1_main_spec(L, 1)
    spec.pop("controls", None)
    spec["id"] = f"target_d1_products_L{L}"
    spec["placements"] = [p for p in spec["placements"] if p["name"] != "seed"]
    for p in spec["placements"]:
        if p["name"] == "A0_0":
            p["params"]["sockets"] = []
        if p["name"] == "A13_0":
            p["params"]["sockets"] = [3, 4, 5, (-5) % L, (-4) % L, (-3) % L]
    # SLOW moves -y and SLOW_LEFT +y on label 41; windows are {start, start-1, start-2}
    spec["placements"].append({"name": "g_down", "block": "slow_glider@1",
                               "params": {"start": (-3) % L, "hit": "SLOW"}, "at": [13, 0, 3], "wrap": True})
    spec["placements"].append({"name": "g_up", "block": "slow_glider@1", "params": {"start": 5, "hit": "SLOW_LEFT"},
                               "at": [13, 0, 3], "wrap": True})
    spec["backward"] = {"rule": "S0 = JR(F^N(JR(T)))", "N": 40,
                        "question": "is the backward image small (a seed) or extended (no simple past)?"}
    spec["steps"] = 40
    return spec


# ---------------------------------------------------------------------------- r20 SR2 shared rotor
def sr2_spec(design="S", times=(41, 57, 73, 89), side=256, zc=64, M=110, Y1=40, Y2=44, steps=None):
    """r20 SR2: F1 = channel 0 (rest (0,0,4), sigma +1) at y = Y1 and F2 = its K-image fibre (channel 14 = z*0,
    rest (0,0,0), sigma -1) at y = Y2 = Y1 + 4, each carrying one approval per time in ``times`` (heads at x = M);
    design 'S': ONE all-48 clock (-1,-1,0) between them at (M, Y1+2), read by both fibres; design 'I' (control):
    two separate clocks on the outer sides (M, Y1-2) and (M, Y2+2)."""
    arr = [(M, t) for t in times]
    f1 = plus_fibre("F1", 1, side - 2, Y1, zc, arr)
    f2 = plus_fibre("F2", 1, side - 2, Y2, zc, arr, g0=14, sigma0=-1)        # K-image fibre: channel z*0
    if design == "S":
        gates = [{"name": "R", "block": "phase_gate@2", "params": {"phase": 0, "offset": [0, 2, 0]}, "at": [M, Y1, zc]}]
        beside = [["R", "F1.F_nodes"]]
    else:
        gates = [{"name": "R1", "block": "phase_gate@2", "params": {"phase": 0, "offset": [0, -2, 0]}, "at": [M, Y1, zc]},
                 {"name": "R2", "block": "phase_gate@2", "params": {"phase": 0, "offset": [0, 2, 0]}, "at": [M, Y2, zc]}]
        beside = [["R1", "F1.F_nodes"], ["R2", "F2.F_nodes"]]
    return {"format": FORMAT, "id": f"sr2_{design}_" + ("_".join(str(t) for t in times) or "no_pulses"),
            "board": _board(side, PPP), "placements": [f1, f2] + gates, "assertions": {"beside_fibre": beside},
            "timing": {"t0": 0, "declared": {"approvals": list(times),
                                             "slip_rule": "D1 fires at approval k iff (t_k - 2k) mod 4 in {1,2}"}},
            "steps": steps or ((max(times) if times else 104) + 16)}



# ---------------------------------------------------------------------------- published guide instances
def _guide(name, start, g0, dirs, leads=(), closed=False, sigma0=1):
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "P", "g0": g0, "dirs": dirs, "sigma0": sigma0}],
                       "packets": [{"path": "P", "f": F, "lead": l} for l in leads],
                       "closed": ["P"] if closed else []},
            "at": list(start)}


def _rect(n1, n2, laps=1):
    one = [[0, n1], [2, n2], [1, n1], [3, n2]]
    return one * (laps - 1) + one[:-1] + [[3, n2 - 1]]          # closed: the last step returns to the start


def published_guide_specs():
    """Specs that regenerate tracked published blocks exactly (r04 guides via guide_net@1)."""
    def sp(i, L, signs, pl, steps):
        return {"format": FORMAT, "id": i, "board": _board(L, signs), "placements": pl, "steps": steps}
    core = lambda nm, x: {"name": nm, "block": "single_channel@1", "params": {"channel": 25, "triple": [0, -1, 4]},
                          "at": [x, 48, 49]}
    return {
        "fiber_x_packet": sp("fiber_x_packet", 48, PPP, [_guide("f", (2, 24, 24), 0, [[0, 43]], [3])], 36),
        "fiber_x_control": sp("fiber_x_control", 48, PPP, [_guide("f", (2, 24, 24), 0, [[0, 43]])], 12),
        "fiber_x_gauged_sx_minus": sp("fiber_x_gauged_sx_minus", 40, MPP, [_guide("f", (2, 20, 20), 0, [[0, 33]], [3])], 26),
        "fiber_diag_110": sp("fiber_diag_110", 48, PPP, [_guide("f", (4, 4, 4), 0, [[0, 1], [2, 1]] * 20, [3])], 33),
        "ring16": sp("ring16", 24, PPP, [_guide("r", (6, 6, 6), 0, _rect(4, 4), [3], closed=True)], 32),
        "spin720_ring": sp("spin720_ring", 24, PPP, [_guide("r", (6, 6, 6), 2, _rect(3, 4, laps=2), [3], closed=True)], 28),
        "atom_trap_d6": sp("atom_trap_d6", 96, PPP, [_guide("f", (2, 48, 48), 0, [[0, 87]], [35]),
                                                    core("c1", 32), core("c2", 38)], 32),
        "junction_Y": approval_router_spec("x", signal=True, approval=False),
    }


# ---------------------------------------------------------------------------- r15 selectors and stations
def _core(name, node_at, slot_direction, node_label=0, state=(1, 0, 4)):
    """r15 'halo core register' = slot_clock@1: one silent channel in a halo slot of a fibre node."""
    return {"name": name, "block": "slot_clock@1",
            "params": {"state": list(state), "node_label": node_label, "slot_direction": slot_direction},
            "at": list(node_at)}


def d2_selector_spec(approval=True, t_q=36, q2=52, cores=True, steps=80, side=160, M=80, Z=80, T_A=20,
                     arms=(("A", 80), ("B", 92))):
    """r15 D2: two arm fibres (r08 +++ channel 0), a halo-core register in the -y slot of node M of each arm
    (state (1,0,4)); approval on arm A at T_A, quanta at t_q and q2 on both arms (heads reach node M)."""
    pl = []
    for arm, y in arms:
        arr = ([(M, T_A)] if (approval and arm == "A") else []) + ([(M, t_q)] if t_q is not None else []) + \
              ([(M, q2)] if q2 is not None else [])
        pl.append(plus_fibre("F" + arm, 1, side - 2, y, Z, arr))
        if cores:
            pl.append(_core("X" + arm, (M, y, Z), 3))
    return {"format": FORMAT, "id": f"d2_selector_app{int(approval)}_tq{t_q}", "board": _board(side, PPP),
            "placements": pl, "steps": steps,
            "timing": {"t0": 0, "declared": {"t_A": T_A if approval else None, "t_q": t_q, "q2": q2}}}


def d2j_selector_spec(t_q=40, approval=True, cores=True, K=21, T_A=16, signs=PPP, steps=None):
    """r15 D2J: r13's device (input + degree-3 junction + arms) with halo-core registers in the -z slots of the
    arm nodes at odd path length K; ``signs`` = (-1,1,1) places the same composition by gauge transport."""
    from universe24 import Coupling
    from .guides import channel_path
    spec = r13_device_spec(t_q, T_A if approval else None, None, k=K, steps=steps or (t_q + 64), name="d2j")
    spec["id"] = f"d2j_selector_app{int(approval)}_tq{t_q}"
    if cores:
        c = Coupling((1, 1, 1))
        branch = channel_path(c, (70, 101, 100), c.ports[2][0], [2] * (K - 1))
        spec["placements"].append(_core("XA", (70 + K, 100, 100), 5))
        spec["placements"].append(_core("XB", branch[K - 1][0], 5, node_label=branch[K - 1][1]))
    spec["assertions"] = {}
    if tuple(signs) != tuple(PPP):
        spec["board"]["coupling"]["signs"] = list(signs)
        for p in spec["placements"]:
            p["native_signs"], p["gauge"] = list(PPP), "auto"
    return spec


R15_STATIONS = {"A": {"M": 170, "arms": {1: 80, 2: 92}, "t_app": 20, "t_q0": 120},
                "B": {"M": 50, "arms": {1: 104, 2: 116}, "t_app": 20, "t_q0": 36}}
R15_SET_A = {1: (98, 106), 2: (100, 108)}        # Bob's SET doublets on Alice's arms (arrivals at x = 170)


def chsh_d2_spec(x, y, lam, arrangement="SEP", side=200, Z=80):
    """r15 CHSH with D2 stations: settings = approval arm (x for Alice, y for Bob), shared lambda shifts the
    quanta by 2 updates; SIG with y = 1 adds Bob's SET doublets on Alice's arms (board signalling)."""
    pl = []
    for st, setting in (("A", x), ("B", y)):
        S = R15_STATIONS[st]
        for arm, ya in S["arms"].items():
            ts = [S["t_q0"] + 2 * lam] + ([S["t_app"]] if arm == setting + 1 else [])
            if st == "A" and arrangement == "SIG" and y == 1:
                ts += list(R15_SET_A[arm])
            pl.append(plus_fibre(f"F{st}{arm}", 1, side - 2, ya, Z, [(S["M"], t) for t in ts]))
            pl.append(_core(f"X{st}{arm}", (S["M"], ya, Z), 3))
    return {"format": FORMAT, "id": f"chsh_d2_{arrangement}_x{x}_y{y}_lam{lam}", "board": _board(side, PPP),
            "placements": pl, "steps": R15_STATIONS["A"]["t_q0"] + 2 + 14,
            "settings": {"x": x, "y": y, "lambda": lam, "arrangement": arrangement}}


# ---------------------------------------------------------------------------- r24 A1 core (light.flash family)
def a1_core_spec(M=1000, L=101, steps=0, at=None):
    """light.flash@1 at amplitude M = r24's 'A1 core': all 48 channels of one site at (0, M, 2) under +++
    (flash_kick is the M = 10**6 point). One burst sends the whole account into an A1 shell."""
    c = L // 2
    return {"format": FORMAT, "id": f"a1_core_M{M}_L{L}", "board": _board(L, PPP),
            "placements": [{"name": "core", "block": "all48_site@1", "params": {"triple": [0, int(M), 2]},
                            "at": list(at or (c, c, c))}], "steps": steps}


def a1_core_clock_probes_spec(core=True, M=30, L=21, probes=((4, 10, 10), (14, 10, 10)), core_at=(10, 10, 10),
                              steps=10):
    """r24 experiment: two B10 breathers (all-48 (2,2,2), matter.breather) as clock probes at distances 6 and 4
    from an A1 core (light.flash at amplitude M); ``core=False`` is the probes-alone control."""
    pl = [{"name": f"B10_{i}", "block": "all48_site@1", "params": {"triple": [2, 2, 2]}, "at": list(p)}
          for i, p in enumerate(probes)]
    if core:
        pl.append({"name": "core", "block": "all48_site@1", "params": {"triple": [0, int(M), 2]}, "at": list(core_at)})
    return {"format": FORMAT, "id": "a1core_clock_probes" + ("" if core else "_alone"), "board": _board(L, PPP),
            "placements": pl, "steps": steps}


# ---------------------------------------------------------------------------- r27 Big Bang built backwards
def _registry_data(name):
    import json
    from pathlib import Path
    return json.loads((Path(__file__).resolve().parent / "data" / name).read_text(encoding="utf-8"))


_BB27_T = {"bb27_T24_rings2": 24, "bb27_T24": 24, "bb27_T12": 12, "bb27_T24_focusP": 24}


def bb27_target_spec(variant="bb27_T24_rings2", L=160):
    """r27's target at time T, composed from registered blocks (copied from r27/compositions, provenance there)."""
    return _registry_data(f"compositions/{variant}_target_T{_BB27_T[variant]}_L{L}.composition.json")


def bb27_dark_spec(spec):
    """The target's dark network: every mover removed, every socket returned to rest (r27 design.dark)."""
    import json
    out = json.loads(json.dumps(spec))
    out["id"] = spec["id"] + "__dark"
    out["placements"] = [p for p in out["placements"]
                         if p["block"] not in ("slow_glider@1", "fibre_packet@1") and not p.get("lit")]
    for p in out["placements"]:
        if p["block"] in ("matter_line@1", "light_line_s@1", "light_line@2"):
            p["params"]["sockets"] = []
    return out


def bb27_seed_spec(variant="bb27_T24_rings2", L=160, star=True, O=(0, 0, 3)):
    """seed.bb27_point@1 (star=True: the 14-cell seed*, T+4 updates before the target; star=False: the 28-cell
    seed, T updates before) placed on the A0 x B0 junction O of the dark network, as a literal patch that fills
    sockets of A0 (matter line, label 41) and B0 (light line, label 1). Its forward run reaches the target."""
    return _bb27_seed_from(bb27_target_spec(variant, L), _BB27_T[variant], L, star, O,
                           f"{variant}_{'seedstar' if star else 'seed'}_L{L}")


def _bb27_seed_from(target, T, L, star=True, O=(0, 0, 3), sid="bb27_seed"):
    """seed.bb27_point@1 on the dark network of ``target`` (WAVE 4: shared by bb27_seed_spec and bb27v2)."""
    data = _registry_data("bb27_point.json")
    rel = data["cells_relative_to_O"] if star else data["seed_28_relative_to_O"]
    cells = [[(O[0] + c[0]) % L, (O[1] + c[1]) % L, O[2] + c[2], c[3], c[4], c[5], c[6]] for c in rel]
    spec = bb27_dark_spec(target)
    spec["id"] = sid
    for p in spec["placements"]:
        if p["name"] == "A0":
            p["params"]["sockets"] = sorted({c[1] for c in cells if c[0] == O[0] and c[2] == O[2] and c[3] == 41})
        if p["name"] == "B0":
            p["params"]["sockets"] = sorted({c[0] for c in cells if c[1] == O[1] and c[2] == O[2] + 1 and c[3] == 1})
    spec["placements"].append({"name": "seed", "block": "literal_patch@1", "params": {"kind": "glider-seed",
                                                                                   "cells": cells},
                               "at": [0, 0, 0], "wrap": True})
    spec["timing"] = {"t0": 0, "declared": {"target_at": T + (4 if star else 0)}}
    return spec


# ===================================================================== WAVE 4 (r21)
# ---------------------------------------------------------------------------- r06b flagship v3 / v4
H1_RING_DIRS = [[0, 4], [4, 3], [1, 4], [5, 2]]     # r04 W6 control: d = +x, a2 = +z, n1 = 4, n2 = 3 (closed)


def _ports(signs):
    from universe24 import Coupling
    return Coupling(tuple(signs)).ports


def h1_ring_placement(name, J, signs=MPP, wrap=True):
    """spin.holonomy_ring_h1@1: r04's WAVE 6 holonomy-1 control ring (P = 14 nodes, one lap = 22 updates, no
    C relation) joined to the matter-line node J (label 41): a closed guide_net@1 path from J + x on channel
    ports[+x][41], sigma0 = +1 (r04 wave6_control.vector_candidates; r06b h1_ring_fragment.json)."""
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "R", "start": [1, 0, 0], "g0": _ports(signs)[0][41], "dirs": H1_RING_DIRS,
                                  "sigma0": 1}], "closed": ["R"]},
            "at": list(J), "wrap": wrap}


R06B_FAR = ("twins_far", "v4a", "v4c", "v4c_swap", "v4c2", "v4c2_swap")
R06B_NAMES = ("skeleton", "e1", "twins", "twins_clocks") + R06B_FAR


def r06b_flagship_spec(name="v4c2", L=256, tiles=1):
    """r06b's flagship v3 / v4 compositions (r06b compose_v3.composition(name)) from registered blocks, on side
    L with hardware pitch L // tiles (the seed once): d1 skeleton (atom, recorders, holonomy-z ring at y_J =
    -20, or -32 for the 'far' family) + the twin lower segment and cores (twins*, far, v4*) + its recorder
    clocks (all but 'twins') + the holonomy-1 control ring at J1 = (13, 44, 3) (v4*) + two phase gates two
    sites above B1 / B-1 at x = m (v4c*: m = 45; v4c2*: m = 121; phase 0 above, 2 below, '_swap' swapped);
    'e1': r08's two trap cores on B0 (x = -3, 5). ``controls`` are r06b's (same names as its init files)."""
    if name not in R06B_NAMES:
        raise ValueError(name)
    far = name in R06B_FAR
    sp = d1_skeleton_spec(L, tiles)
    sp["id"] = f"flagship_v3_{name}_L{L}"
    Lb = L // tiles
    pl, asr = sp["placements"], sp["assertions"]
    for p in pl:
        if p["name"].startswith("ring_"):
            i, j = int(p["name"][5]), int(p["name"][6])
            p["at"] = [13 + i * Lb, ((-32 if far else -20) + j * Lb) % L, 3]
    halo = []
    for i in range(tiles):
        for j in range(tiles):
            y = (-12 + j * Lb) % L
            if name == "e1":
                for x in (-3, 5):
                    nm = f"r08core{x}_{i}{j}"
                    pl.append({"name": nm, "block": "slot_clock@1", "params": {"state": [-1, 0, 0]},
                               "at": [(x + i * Lb) % L, (j * Lb) % L, 4]})
                    asr["slot_clocks_silent"].append(nm)
            if name in ("skeleton", "e1"):
                continue
            pl.append({"name": f"Bm12_{i}{j}", "block": "light_line@1", "params": {"length": 148, "gauge_phase": 1},
                       "at": [3 + i * Lb, y, 4]})
            clocks = [(10, [-1, 0, 0], "lcore"), (18, [-1, 0, 0], "lcore")]
            if name != "twins":
                clocks += [(x, [0, -1, 4], "lrec") for x in (25, 29, 33, 37)]
            for x, st, role in clocks:
                nm = f"{role}{x}_{i}{j}"
                pl.append({"name": nm, "block": "slot_clock@1", "params": {"state": st}, "at": [x + i * Lb, y, 4]})
                asr["slot_clocks_silent"].append(nm)
            asr["junction_classes"][f"{13 + i * Lb},{y}"] = 2
            if name.startswith("v4"):
                J1 = [13 + i * Lb, (44 + j * Lb) % L, 3]
                pl.append(h1_ring_placement(f"h1_{i}{j}", J1))
                halo.append({"port": f"h1_{i}{j}.R_nodes", "closed": True, "allow": [J1 + [41]]})
            if name.startswith("v4c"):
                m = 121 if name.startswith("v4c2") else 45
                up, lo = (2, 0) if name.endswith("_swap") else (0, 2)
                pl.append({"name": f"gate_up_{i}{j}", "block": "phase_gate@2",
                           "params": {"phase": up, "offset": [0, 0, 2]}, "at": [m + i * Lb, (12 + j * Lb) % L, 4]})
                pl.append({"name": f"gate_lo_{i}{j}", "block": "phase_gate@2",
                           "params": {"phase": lo, "offset": [0, 0, 2]}, "at": [m + i * Lb, y, 4]})
    if halo:
        asr["guide_halo_clear"] = halo
    names = [p["name"] for p in pl]

    def rm(*prefixes, **extra):
        return {"remove": [n for n in names if n.startswith(prefixes)], **extra}
    ctl = {"no_seed": {"remove": ["seed"], "unfill_sockets": True}, "no_cores": rm("core", "lcore"),
           "no_ring": rm("ring_"), "no_clocks": rm("rec", "lrec")}
    if name not in ("skeleton", "e1"):
        ctl["no_lower_cores"] = rm("lcore")
    if name.startswith("v4"):
        ctl["no_h1"] = rm("h1_", assertions={"guide_halo_clear": None})
    if name.startswith("v4c"):
        ctl["no_gates"] = rm("gate_")
    sp["controls"] = [{"name": k, **v} for k, v in ctl.items()] if name != "e1" else []
    sp["steps"] = 300 if far else 240
    sp["timing"] = {"t0": 0, "declared": {"note": "r06b NOTES / RESULT_v4.json (decoder v1.0 readings)"}}
    return sp


def r06b_link_y_placement(name, x, phase, segment, z=3, label=41):
    """medium.light_segment@1 along y (r06b V4-3 Einstein link, compose_v3.light_fibre_line_y): label 41 at
    z = 3, light gauge class 0 where y + phase is even, nodes y in [ya, yb] at x (light_line@1, axis 'y')."""
    ya, yb = int(segment[0]), int(segment[1])
    return {"name": name, "block": "light_line@1",
            "params": {"length": yb - ya + 1, "label": label, "axis": "y", "gauge_phase": (phase + ya) % 2},
            "at": [x, ya, z], "wrap": True}


def r20_bridge_placement(name, XL, side="up", h=2, phase=1, y_up=12, y_down=-12, signs=MPP):
    """medium.guide_bridge@1 (r20 S8 bridge, as used by r06b V4-3b, compose_v3.bridge_nodes / light_bridge): an
    open guide_net@1 path from the +z slot partner ('up', z = 5) or the -z partner ('down', z = 3) of the upper
    line's node at x = XL, h sites out of the plane, -y for y_up - y_down sites and back h sites to the same
    partner of the lower line's node; guide gauge sigma0 = phase (r = 4 where sigma * phase = +1)."""
    ports = _ports(signs)
    n = int(y_up) - int(y_down)
    if side == "up":
        g0, z0, dirs = ports[4][1], 5, [[4, h], [3, n], [5, h]]
    elif side == "down":
        g0, z0, dirs = ports[5][1], 3, [[5, h], [3, n], [4, h]]
    else:
        raise ValueError("side must be 'up' or 'down'")
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "W", "g0": g0, "dirs": dirs, "sigma0": int(phase)}]},
            "at": [XL, y_up, z0], "wrap": True}


# ---------------------------------------------------------------------------- r23 slow clocks and long links
M4 = [-1, -1, 0]                      # matter.silent_monomer@1 / all-48 dark clock (r08 lmi.all48)
R23_ORBIT = ([0, -1, 4], [-1, 0, 4], [0, 1, 4], [1, 0, 4])     # r04 slot-core orbit (T9 cores)


def _x_fibre(name, L, y, z, fwd=(), bwd=(), x0=1, x1=None):
    """r23 kit.x_path + fibre_cells + packet_cells: a +++ channel-0 guide along +x from x0 to x1 (default
    L - 2, rest r = 4), packets (1,0,-1) moving +x (head at node index l on 'P') and moving -x (head at index
    l counted from the x1 end, on '~P')."""
    x1 = L - 2 if x1 is None else x1
    pk = [{"path": "P", "f": F, "lead": int(v)} for v in fwd] + [{"path": "~P", "f": F, "lead": int(v)} for v in bwd]
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "P", "g0": 0, "dirs": [[0, x1 - x0]]}], "packets": pk},
            "at": [x0, y, z], "wrap": True}


def _site(name, at, triple=M4):
    return {"name": name, "block": "all48_site@1", "params": {"triple": list(triple)}, "at": list(at)}


def _r23(i, L, pl, steps, declared=None):
    return {"format": FORMAT, "id": i, "board": _board(L, PPP), "placements": pl, "steps": steps,
            "timing": {"t0": 0, "declared": declared or {}},
            "observables": {"decoder": "click_decoder_v1 v1.0 (r23: difference layers, station first clicks)"}}


def r23_gate_window_spec(L=90, dist=2, source=True, lead=None, probe=True, x_probe=40, steps=100):
    """gravity.gate_window_clock@1 (r23 T3b, w1_compose.gate_window): signal fibre at y0 = z0 = L//2 with one
    calibrated packet (head at node index ``lead``; None = no signal), probe monomer (-1,-1,0) at distance
    ``dist`` in +y from node x_probe (dist 2 = gate.phase_gate@2 phase 0) and an optional source monomer
    behind it (distance dist + 1)."""
    y0 = L // 2
    pl = [_x_fibre("F", L, y0, y0, fwd=() if lead is None else (lead,))]
    if probe:
        pl.append(_site("probe", (x_probe, y0 + dist, y0)))
    if source:
        pl.append(_site("source", (x_probe, y0 + dist + 1, y0)))
    return _r23(f"r23_gate_window_L{L}_d{dist}_s{int(source)}_lead{lead}", L, pl, steps,
                {"clean_pass": "joint log == region log + signal log", "monitor": [75, y0, y0, 0]})


def r23_counter_train_spec(L=160, k=3, P=8, x_first=60, signal=True, signal_lead=4, steps=150):
    """gravity.counter_flux_link@1 (r23 T4m / T5, w1_compose.counter_train): one fibre carrying k packets moving
    -x (heads at x_first + j P) and one calibrated packet moving +x (head at node ``signal_lead``)."""
    y0 = L // 2
    bwd = [(L - 2) - (x_first + j * P) for j in range(k)]
    pl = [_x_fibre("F", L, y0, y0, fwd=(signal_lead,) if signal else (), bwd=bwd)]
    return _r23(f"r23_counter_train_L{L}_P{P}_k{k}_s{int(signal)}", L, pl, steps,
                {"delay_law": "Delta = 4 k (head-on crossings, r22 C3)", "monitor": [100, y0, y0, 0]})


def r23_t5_spec(P=16, signal=True, L=480, xE=5, xR=105):
    """r23 T5 stationary counter-flux over [xE, xR]: the train is long enough to fill the segment during the
    signal's transit (k and the horizon as in r23 w1_run.T5)."""
    from fractions import Fraction
    t_R = int((xR - xE) * Fraction(P + 4, P - 4)) + 40
    k = (xR + t_R + P - (xE + 3)) // P + 1
    return r23_counter_train_spec(L, k, P, xE + 3, signal, signal_lead=xE - 1, steps=t_R + 10)


def r23_lamp_flux_spec(L=160, xl=80, k=6, P=8, x_first=100, flux=True, lamp=True, flux_gap=3, steps=150):
    """r23 T7 (w1_compose.lamp_beside_flux): an M4 lamp touching its read-out fibre R (y0 = z0 = L//2) at
    distance flux_gap - 1 from a flux fibre F (y0 + flux_gap) carrying k packets moving -x."""
    y0 = L // 2
    bwd = [(L - 2) - (x_first + j * P) for j in range(k)] if flux else []
    pl = [_x_fibre("R", L, y0, y0), _x_fibre("F", L, y0 + flux_gap, y0, bwd=bwd)]
    if lamp:
        pl.append(_site("lamp", (xl, y0 + 1, y0)))
    return _r23(f"r23_lamp_flux_x{x_first}_f{int(flux)}_l{int(lamp)}", L, pl, steps, {"monitor": [xl - 30, y0, y0, 0]})


def r23_core_pair_spec(L=96, d=3, ph1=0, ph2=3, lead=13, cores=True, packet=True, D=90, I1=40, steps=120):
    """gravity.core_pair_delay@1 (r23 T9, w1_run.core_pair_cells): +++ fibre of D nodes from (2, 48, 48) along +x,
    two r04 slot cores ((0,-1,4) orbit, phases ph1 / ph2) in the +z halo channels of nodes I1 and I1 + d
    (slot_clock@1 on channel-0 nodes), one packet with head at node ``lead``."""
    pl = [{"name": "F", "block": "guide_net@1",
           "params": {"paths": [{"name": "P", "g0": 0, "dirs": [[0, D - 1]]}],
                      "packets": [{"path": "P", "f": F, "lead": int(lead)}] if packet else []},
           "at": [2, 48, 48], "wrap": True}]
    if cores:
        for nm, i, ph in (("c1", I1, ph1), ("c2", I1 + d, ph2)):
            pl.append({"name": nm, "block": "slot_clock@1",
                       "params": {"state": R23_ORBIT[ph % 4], "node_label": 0, "slot_direction": 4},
                       "at": [2 + i, 48, 48]})
    return _r23(f"r23_core_pair_L{L}_d{d}_ph{ph1}{ph2}_lead{lead}", L, pl, steps,
                {"law": "transmitted copy delayed by 2d+4 at this arrival phase (exploration)",
                 "monitors": [[82, 48, 48, 0], [10, 48, 48, 0]]})


def _ring(name, start, n1, n2, leads=(3,), counter_leads=(), tap=None, probe=None):
    """r04 square ring (guide_net@1 closed rectangle n1 x n2 in the x-y plane, channel 0, +++) with packets
    (1,0,-1) at ring indices ``leads``; ``counter_leads`` = counter-circulating packets on the same ring
    traversed backwards (r04 ring2 / r23 ``rev`` node order). ``tap`` = (ring node, direction, length): the
    r04 ring-emitter exit fibre ('exit'); ``probe`` = ('in' | 'out', exit-fibre index of the head)."""
    paths = [{"name": "ring", "start": list(start), "g0": 0, "dirs": _rect(n1, n2)}]
    closed = ["ring"]
    pk = [{"path": "ring", "f": F, "lead": int(v)} for v in leads]
    if counter_leads:
        paths.append({"name": "back", "start": list(start), "g0": 0,
                      "dirs": [[2, n2], [0, n1], [3, n2], [1, n1 - 1]]})
        closed.append("back")
        pk += [{"path": "back", "f": F, "lead": int(v)} for v in counter_leads]
    if tap is not None:
        node, d, M = tap
        paths.append({"name": "exit", "branch_of": "ring", "at_node": node, "dir": d, "length": M})
        if probe is not None:
            kind, idx = probe
            pk.append({"path": "~exit" if kind == "in" else "exit", "f": F,
                       "lead": (M - 1) - idx if kind == "in" else idx})
    return {"name": name, "block": "guide_net@1", "params": {"paths": paths, "packets": pk, "closed": closed},
            "at": [0, 0, 0], "wrap": True}


R23_EI = {"L": 400, "M": 330, "start": (10, 10, 70), "tap_node": 6, "exit_dir": 5}


def r23_emitter_probe_spec(n1=4, n2=4, emitter=True, probe=("in", 320), steps=420):
    """exp.alpha_flux_matched@1 hardware (r23 ei_run.cells_for): r04 ring emitter (n1 x n2 ring at (10,10,70),
    tap at ring node 6, exit fibre of 330 nodes along -z, L = 400) with its ring packet (``emitter``) and one
    probe packet on the exit fibre ('in': moving up the fibre, head at exit index; 'out': moving out)."""
    E = R23_EI
    ring = _ring("E", E["start"], n1, n2, leads=(3,) if emitter else (), tap=(E["tap_node"], E["exit_dir"], E["M"]),
                 probe=probe)
    return _r23(f"r23_emitter_s{2 * (n1 + n2)}_e{int(emitter)}_{probe[0] if probe else 'none'}", E["L"], [ring], steps,
                {"stations": "exit-fibre indices 300, 260, ..., 20 (decoder detectors)"})


def r23_ring_counter_spec(R=16, L=40, counter=False, heads=None, start=(6, 6, 6), steps=None):
    """r23 T6 / E-I ring clocks: r04 square ring of perimeter R with one packet (lead 3) and counter-circulating
    packets: ``counter`` = one half a lap away (T6), or explicit ``heads`` on the backward ring (E-I ring64)."""
    n = R // 4
    back = list(heads) if heads is not None else ([(3 + R // 2) % R] if counter else [])
    return _r23(f"r23_ring_R{R}_L{L}_counter{len(back)}", L, [_ring("ring", start, n, n, counter_leads=back)],
                steps or 4 * (R + 8) + 8)


def r23_lamp_beside_exit_spec(fidx=100, emitter=True, n1=4, n2=4, steps=200):
    """r23 E-I.7 (ei_run.EI_lamps): an M4 lamp two sites (+y) from exit-fibre node ``fidx`` of the s = 16 emitter,
    touching its own read-out fibre (channel 0 along x at y = 15, x in [fx - 60, fx + 60])."""
    E = R23_EI
    ring = _ring("E", E["start"], n1, n2, leads=(3,) if emitter else (), tap=(E["tap_node"], E["exit_dir"], E["M"]))
    fx, fy, fz = E["start"][0] + n1, E["start"][1] + 2, (E["start"][2] - 1 - fidx) % E["L"]
    pl = [ring, _x_fibre("RO", E["L"], fy + 3, fz, x0=fx - 60, x1=fx + 60), _site("lamp", (fx, fy + 2, fz))]
    return _r23(f"r23_lamp_exit_f{fidx}_e{int(emitter)}", E["L"], pl, steps)


def r23_cases():
    """Every kept r23 preparation file (research/matter_light_v1/r23/preparations) as a composition."""
    out = {"T3b_joint_L90_d2_s1_lead2": r23_gate_window_spec(90, 2, True, 2),
           "T3b_joint_L90_d2_s1_lead3": r23_gate_window_spec(90, 2, True, 3),
           "T3b_region_L90_d2_s1": r23_gate_window_spec(90, 2, True, None),
           "T3b_signal_L90_lead3": r23_gate_window_spec(90, 2, False, 3, probe=False),
           "T4m_free_L160": r23_counter_train_spec(160, 0, 8, 60),
           "T4m_train_L160_P8_k3": r23_counter_train_spec(160, 3, 8, 60),
           "T4m_trainonly_L160_P8_k3": r23_counter_train_spec(160, 3, 8, 60, signal=False),
           "T5_flux_L480_P16": r23_t5_spec(16),
           "T5_fluxonly_L480_P16": r23_t5_spec(16, signal=False),
           "T7_lamp_flux_P8_k6_ph0": r23_lamp_flux_spec(x_first=100),
           "T7_lamp_flux_P8_k6_ph1": r23_lamp_flux_spec(x_first=101),
           "T7_lamp_noflux": r23_lamp_flux_spec(flux=False),
           "T9_joint_L96_d3_ph03_lead13": r23_core_pair_spec(),
           "T9_free_L96_d3_ph03_lead13": r23_core_pair_spec(cores=False),
           "T9_cores_L96_d3_ph03_lead13": r23_core_pair_spec(packet=False),
           "EI_s16_in_joint": r23_emitter_probe_spec(4, 4, True, ("in", 320)),
           "EI_s16_in_emitter": r23_emitter_probe_spec(4, 4, True, None),
           "EI_s16_in_free": r23_emitter_probe_spec(4, 4, False, ("in", 320)),
           "EI_s20_in_joint": r23_emitter_probe_spec(4, 6, True, ("in", 320)),
           "EI_s20_in_emitter": r23_emitter_probe_spec(4, 6, True, None),
           "EI_s20_in_free": r23_emitter_probe_spec(4, 6, False, ("in", 320)),
           "EI_s16_out_joint": r23_emitter_probe_spec(4, 4, True, ("out", 12), steps=330),
           "EI_ring64_counter1_h35": r23_ring_counter_spec(64, 40, heads=(35,), steps=384),
           "EI_ring64_counter2_h24_46": r23_ring_counter_spec(64, 40, heads=(24, 46), steps=384),
           "EI_lamp_ph0_lampalone": r23_lamp_beside_exit_spec(100, emitter=False),
           "EI_lamp_ph1_joint": r23_lamp_beside_exit_spec(101, emitter=True)}
    for R in (16, 64):
        for c in (False, True):
            out[f"T6_ring_L40_R{R}_counter{int(c)}"] = r23_ring_counter_spec(R, 40, counter=c)
    return out


def r08_clockrates_spec(source_at="A", L=300, a=130, b=170, clock=M4, source=M4, steps=150):
    """exp.rate_by_light@1 instances (r08 clockrates; r23 w1_compose.lamp_pair) with the clock half registered as
    gravity.contact_slow_clock@1: two +++ channel-0 read-out fibres (y = c and c + 8, z = c = L//2, x in
    [1, L-2]), clock monomers touching them at (a, c+1, c) and (b, c+7, c), and the source monomer face-adjacent
    to clock A ('A'), to clock B ('B') or absent (None, the no-source control)."""
    c = L // 2
    pl = [_x_fibre("F1", L, c, c), _x_fibre("F2", L, c + 8, c),
          _site("clockA", (a, c + 1, c), clock), _site("clockB", (b, c + 7, c), clock)]
    if source_at == "A":
        pl.append(_site("source", (a, c + 2, c), source))
    elif source_at == "B":
        pl.append(_site("source", (b, c + 6, c), source))
    elif source_at is not None:
        raise ValueError("source_at must be 'A', 'B' or None")
    return _r23(f"clockrates_source_{source_at}", L, pl, steps,
                {"monitors": {"A_light_at_B": [b, c, c, 0], "B_own_at_B": [b + 2, c + 8, c, 0]}, "window": [70, 149]})


def r08_clockrates_cases():
    return {"clockrates_source_at_A": r08_clockrates_spec("A"), "clockrates_source_at_B_swapped": r08_clockrates_spec("B"),
            "clockrates_no_source_control": r08_clockrates_spec(None)}


# ---------------------------------------------------------------------------- r15 wave 3/4 cards
def r15_w3_selector_spec(signs=PPP, L=256, X0=1, XJ=120, nA=130, nB=120, K=21, XQ=99, DA=10, YLO=None, YHI=None,
                         seeds=True, cores=True, side=True, steps=200):
    """r15 W3 seeded selector (w3_board.Board G0): r13's resting device (input line, degree-3 junction, arms A /
    B), halo-core registers (1,0,4) in the -y slot of arm A's node and the -z slot of arm B's node at path
    length K, dump.open_line@1 = the ch-18 side fibre along y at x = M + 1 (y in [YLO, YHI]), and two
    seed.emitter_core@1 channels (-1,0,0): Q in the -y halo of input node XQ, A in the -x halo of the side
    fibre node at y = c - 1 - DA. ``signs`` (-1,1,1) places the same composition by gauge transport."""
    from universe24 import Coupling
    from .guides import channel_path
    c, M = L // 2, XJ + K
    YLO = max(1, c - 1 - DA - 100) if YLO is None else YLO
    YHI = min(L - 2, c + 100) if YHI is None else YHI
    sp = r13_device_spec(None, None, None, L=L, X0=X0, XJ=XJ, nA=nA, nB=nB, k=K, steps=steps, name="r15_w3_selector")
    pl = sp["placements"]
    cp = Coupling((1, 1, 1))
    if side:
        pl.append({"name": "dump", "block": "guide_net@1",
                   "params": {"paths": [{"name": "S", "g0": 18, "dirs": [[2, YHI - YLO]]}]}, "at": [M + 1, YLO, c]})
    if cores:
        branch = channel_path(cp, (XJ, c + 1, c), cp.ports[2][0], [2] * (K - 1))
        pl.append(_core("XA", (M, c, c), 3))
        pl.append(_core("XB", branch[K - 1][0], 5, node_label=branch[K - 1][1]))
    if seeds:
        pl.append({"name": "SQ", "block": "single_channel@1", "params": {"channel": cp.ports[3][0], "triple": [-1, 0, 0]},
                   "at": [XQ, c - 1, c]})
        pl.append({"name": "SA", "block": "single_channel@1",
                   "params": {"channel": cp.ports[1][18], "triple": [-1, 0, 0]}, "at": [M, c - 1 - DA, c]})
    sp["assertions"] = {}
    sp["id"] = f"r15_w3_selector_G0_{'ppp' if tuple(signs) == tuple(PPP) else 'mpp'}"
    if tuple(signs) != tuple(PPP):
        sp["board"]["coupling"]["signs"] = list(signs)
        for p in pl:
            p["native_signs"], p["gauge"] = list(PPP), "auto"
    return sp


def r15_w3_cases():
    return {"w3_seeded_selector_G0_ppp": r15_w3_selector_spec(),
            "w3_seeded_selector_G0_signs-++": r15_w3_selector_spec(signs=(-1, 1, 1))}


def r08_spectro_spec(d=6, arrivals=(), cores=True, packet=True, phases=(0, 0), L=420, X0=2, Y0=210, I1=200, D=400,
                     lead_off=5, steps=None):
    """atom.two_core_trap@1 / store.two_core_trap_store@1 instances (r08 spectro.build + add_train): a +++
    channel-0 fibre of D nodes from (X0, Y0, Y0), r04 cores (orbit of (0,-1,4), ``phases``) in the +z halo of
    nodes I1 and I1 + d, the bound packet (``packet``: head at node I1 + lead_off; packet=False = empty trap)
    and unit pulses moving +x whose heads reach core 1's node at the times ``arrivals``."""
    pk = ([{"path": "P", "f": F, "lead": I1 + lead_off}] if packet else []) + \
         [{"path": "P", "f": F, "lead": I1 - int(ta)} for ta in arrivals]
    pl = [{"name": "F", "block": "guide_net@1",
           "params": {"paths": [{"name": "P", "g0": 0, "dirs": [[0, D - 1]]}], "packets": pk}, "at": [X0, Y0, Y0]}]
    if cores:
        for nm, i, ph in (("c1", I1, phases[0]), ("c2", I1 + d, phases[1])):
            pl.append({"name": nm, "block": "slot_clock@1",
                       "params": {"state": R23_ORBIT[ph % 4], "node_label": 0, "slot_direction": 4},
                       "at": [X0 + i, Y0, Y0]})
    lev = 2 * d + 4
    return {"format": FORMAT, "id": f"r08_spectro_d{d}_{'atom' if packet else 'empty'}_{'_'.join(map(str, arrivals))}",
            "board": _board(L, PPP), "placements": pl, "steps": steps or 43 + 2 * d + 3 * lev + 60,
            "timing": {"t0": 0, "declared": {"core1_arrivals": list(arrivals), "level": lev}}}


def r08_spectro_cases():
    """r08 spectro.write_census_preps files as compositions; the K_reversed files are recipes (see verifier)."""
    out = {}
    for d in (6, 10, 14):
        def trap(arr, **kw):
            return r08_spectro_spec(d, arr, **kw)
        out[f"spectro_d{d}_empty_trap_pair_t43_P{2 * d}_capture"] = trap([43, 43 + 2 * d], packet=False)
        out[f"spectro_d{d}_empty_trap_pair_t43_P{2 * d - 1}_control"] = trap([43, 42 + 2 * d], packet=False)
        out[f"spectro_d{d}_empty_trap_pair_t43_P{2 * d + 1}_control"] = trap([43, 44 + 2 * d], packet=False)
        out[f"spectro_d{d}_empty_trap_pair_t41_P{2 * d}_control"] = trap([41, 41 + 2 * d], packet=False)
        out[f"spectro_d{d}_empty_trap_single_t43_control"] = trap([43], packet=False)
        out[f"spectro_d{d}_atom_alone_control"] = trap([])
        out[f"spectro_d{d}_fibre_pair_t43_P{2 * d}_atom_absent_control"] = trap([43, 43 + 2 * d], cores=False,
                                                                                  packet=False)
    for ta, tag in ((49, "elastic"), (51, "shift12"), (48, "altered"), (43, "two_out_shift4"), (45, "multiplication")):
        out[f"spectro_d10_atom_pulse_t{ta}_{tag}"] = r08_spectro_spec(10, [ta])
    return out


# ---------------------------------------------------------------------------- r19 shared-record gate
def r19_sr_gate_placements(prefix, m, yc, zc=64, side=400, phase=0, arrivals=(), delay2=2):
    """gate.shared_rotor_two_readers@2 = r19 sr_gate (V14): ONE all-48 dark clock (orbit phase ``phase`` with its
    history halo) at C = (m, yc, zc), read through its channel 6 by F1 = channel 0 at C - 2y and F2 = channel 14
    at C + 2y, both +++ fibres with sigma +1 (rest (0,0,4)) over x in [1, side - 2]; each approval = a pulse on
    F1 whose head reaches node m at t and one on F2 reaching it at t + delay2 (r19 srgate.station)."""
    return [plus_fibre(prefix + "F1", 1, side - 2, yc - 2, zc, [(m, t) for t in arrivals]),
            plus_fibre(prefix + "F2", 1, side - 2, yc + 2, zc, [(m, t + delay2) for t in arrivals], g0=14, sigma0=1),
            {"name": prefix + "R", "block": "phase_gate@2", "params": {"phase": phase, "offset": [0, 2, 0]},
             "at": [m, yc - 2, zc]}]


def r19_sr_gate_spec(arrivals=(), m=220, yc=60, side=400, phase=0, steps=70, name=None):
    pl = r19_sr_gate_placements("", m, yc, side=side, phase=phase, arrivals=arrivals)
    return {"format": FORMAT, "id": name or "r19_sr_gate", "board": _board(side, PPP), "placements": pl,
            "assertions": {"beside_fibre": [["R", "F1.F_nodes"]]}, "steps": steps,
            "timing": {"t0": 0, "declared": {"approvals_F1": list(arrivals), "F2_delay": 2,
                                             "rule": "F1 fires iff (t + 2s) mod 4 in {1,2}, F2 iff (t + 2 + 2s) mod 4 "
                                                     "in {1,2}; s = record parity (CLOCKS s1, T7)"}}}


def r19_angle_pair_spec(alpha=0, beta=0, P=20, t0=41, n=12, m=360, ys=(60, 180), side=800):
    """exp.angle_pair_Z4@1 (r19 E2b): two separated sr_gate stations (clock phases alpha, beta = settings on the
    Z_4 grid) on one +++ board, the same approval stream (n approvals, spacing P from t0) on both."""
    arr = [t0 + k * P for k in range(n)]
    pl = r19_sr_gate_placements("A_", m, ys[0], side=side, phase=alpha, arrivals=arr) + \
        r19_sr_gate_placements("B_", m, ys[1], side=side, phase=beta, arrivals=arr)
    return {"format": FORMAT, "id": f"r19_angle_Z4_P{P}_t{t0}_a{alpha}_b{beta}", "board": _board(side, PPP),
            "placements": pl, "assertions": {"beside_fibre": [["A_R", "A_F1.F_nodes"], ["B_R", "B_F1.F_nodes"]]},
            "steps": arr[-1] + 4 * n + 30,
            "timing": {"t0": 0, "declared": {"law": "cos(90 deg * (alpha - beta)) on the Z_4 grid (r19 E2b)"}}}


def r19_cases():
    out = {f"w1_srgate_V14_single_t{t}": r19_sr_gate_spec([t]) for t in (40, 41)}
    out["w1_srgate_V14_control_no_approval"] = r19_sr_gate_spec([])
    for P, t0 in ((20, 41), (17, 41), (17, 43)):
        arr = [t0 + k * P for k in range(12)]
        out[f"w1_srgate_V14_stream_P{P}_t{t0}_n12"] = r19_sr_gate_spec(arr, m=360, side=800, steps=arr[-1] + 78)
    for al, be in ((0, 0), (0, 1), (0, 2)):
        out[f"w1_angle_Z4_P20_t41_a{al}_b{be}"] = r19_angle_pair_spec(al, be)
    return out


# ---------------------------------------------------------------------------- r18 planar sector and the Wu seed
R18_OBJ = {"G-": [[0, -1, 4], [-1, 0, 0]], "JG-": [[0, 1, 0], [1, 0, 4]], "G+": [[-1, 0, 0], [0, -1, 4]],
           "JG+": [[1, 0, 4], [0, 1, 0]], "S+": [[0, 0, 4]], "S-": [[0, 0, 0]], "S2+": [[0, 0, 4], [0, 0, 4]],
           "S2-": [[0, 0, 0], [0, 0, 0]], "Dpm": [[0, 0, 4], [0, 0, 0]], "Dmp": [[0, 0, 0], [0, 0, 4]]}


def r18_planar_spec(items, L=12, steps=26, name="r18_planar"):
    """r18 planar compositions (planar.place + decode_runs.cells_of, phase 0): items = [(object, lowest plane)],
    objects from R18_OBJ (matter.planar_glider@1 G-+, JG-+; medium.mark_plane@1 sheets S+-, S2+-, dipoles Dpm /
    Dmp), each as all48_planes@1 over the whole board (+++, vacuum (0,0,2))."""
    pl = [{"name": f"{obj}_{x0}", "block": "all48_planes@1", "params": {"planes": R18_OBJ[obj], "size": L},
           "at": [x0, 0, 0], "wrap": True} for obj, x0 in items]
    return {"format": FORMAT, "id": name, "board": _board(L, PPP), "placements": pl, "steps": steps,
            "timing": {"t0": 0, "declared": {"law": "G- passes iff every prefix sum of p_i <= 0 (block moves +2), "
                                                    "else reflects as JG+ (r18 PR-3/PR-4, exact ring)"}}}


def r18_planar_cases():
    """r18 decode_runs.cli_cases init files (runs/matter_light_v1/r18/decoder)."""
    return {"i_Gminus_vs_Splus_L12": r18_planar_spec([("S+", 2), ("G-", 6)], name="planar_mirror"),
            "ii_Gminus_vs_Sminus_L12": r18_planar_spec([("S-", 2), ("G-", 6)], name="planar_pass_through"),
            "iii_free_Gminus_L12": r18_planar_spec([("G-", 6)], name="planar_free_glider"),
            "iv_Splus_alone_L12": r18_planar_spec([("S+", 2)], name="planar_sheet_alone")}


R18_WU = {(0, 1, 14, 23): [0, 20, 2], (2, 22, 24, 40): [0, -7, 2]}


def r18_wu_seed_spec(signs=PPP, L=19, site=(9, 9, 0), steps=8):
    """parity.wu_seed@1 (r18): eight channels of one site (channels 0, 1, 14, 23 at (0,20,2); 2, 22, 24, 40 at
    (0,-7,2)), the same data under every coupling; it is mirror-symmetric and emits asymmetrically only in
    class F (r18: A = +74 / -74 / 0 for ++-, +-+, +++; decoder)."""
    cells = [[0, 0, 0, g, *tr] for chans, tr in R18_WU.items() for g in chans]
    return {"format": FORMAT, "id": f"wu_seed_{''.join('+' if s > 0 else '-' for s in signs)}_L{L}",
            "board": _board(L, list(signs)),
            "placements": [{"name": "wu", "block": "literal_patch@1", "params": {"kind": "wu-seed", "cells": cells},
                            "at": list(site)}], "steps": steps}


def r18_wu_cases():
    return {f"wu_seed_{t}_L19": r18_wu_seed_spec(s) for t, s in (("+++", (1, 1, 1)), ("++-", (1, 1, -1)),
                                                                 ("+-+", (1, -1, 1)))}


# ---------------------------------------------------------------------------- r14 co-moving Einstein module
# r06 catalog species (natively verified s = -1 classes, by medium string), profile computed with r06
# crystal.G.halo_and_passage (r21 WAVE 4); class '0' is the r08 / r14 ladder glider (v = 1/3, T = 3).
R06_CATALOG = {"0": {"W": 3, "s": -1, "a": [-1, -1, 0], "b": [-1, 1, 0], "c": [1, 0, 1], "T": 3, "v": 1,
                     "medium": [0], "halo": {"1": -1}},
               "0002": {"W": 3, "s": -1, "a": [1, 1, 0], "b": [0, -1, -1], "c": [2, 0, 2], "T": 8, "v": 4,
                        "medium": [0, 0, 0, 2], "halo": {"1": 1}}}


def r14_e2_sync_spec(D=64, h=12, A=True, B=True, L=640, X0=40, YJ=420, GAP=8, hit=None, steps=None):
    """exp.co_moving_einstein@1 (r14 W2 E2, e2_sync.cells_for): rail = matter_line@1 at x = X0 (class-0 medium),
    collector = light_line@1 along y on label 41 at x = X0 + h (light phase 1), three rungs = light_line@1 along
    x at y = YJ, YJ - u, YJ - s_f (r08 ladder conventions, phase 1), two class-0 slow gliders (v = 1/3) D apart
    (A at YJ + GAP, B at YJ + GAP - D; ``A`` / ``B`` = the single-glider controls)."""
    from fractions import Fraction
    R0 = 2 * h - 5
    s_f, s_b = (R0 + 5 + 3 * D) // 2, (3 * D - R0 - 5) // 4
    u = s_f - s_b
    startA = YJ + GAP
    starts = [s for on, s in ((A, startA), (B, startA - D)) if on]
    socks = sorted({(s - k) % L for s in starts for k in range(3)})
    pl = [{"name": "rail", "block": "matter_line@1", "params": {"length": L, "sockets": socks}, "at": [X0, 0, 3],
           "wrap": True},
          {"name": "collector", "block": "light_line@1", "params": {"length": L, "label": 41, "axis": "y",
                                                                    "gauge_phase": 1}, "at": [X0 + h, 0, 3]}]
    for j, yj in enumerate((YJ, YJ - u, YJ - s_f)):
        pl.append({"name": f"rung{j}", "block": "light_line@1", "params": {"length": L, "gauge_phase": 1},
                   "at": [0, yj, 4]})
    for nm, s in zip(("GA", "GB") if A else ("GB",), starts):
        pl.append({"name": nm, "block": "slow_glider@2", "params": {"start": s, "hit": hit or R06_CATALOG["0"]},
                   "at": [X0, 0, 3], "wrap": True})
    De = D + R0 + 5
    tau_f, tau_b = Fraction(3, 2) * De, Fraction(3, 4) * De
    return {"format": FORMAT, "id": f"r14_e2_sync_D{D}_{'both' if A and B else ('A_alone' if A else 'B_alone')}",
            "board": _board(L, MPP), "placements": pl, "steps": steps or int(26 + float(tau_f + tau_b)) + 40,
            "timing": {"t0": 0, "declared": {"tau_f": str(tau_f), "tau_b": str(tau_b), "delta": str(Fraction(3, 8) * De),
                                             "reply_delay": 4, "observer": "peak_arrival (r14, read-only)"}}}


def r14_e2_cases():
    out = {f"w2_e2_sync_D{D}_both_L640": r14_e2_sync_spec(D) for D in (40, 48, 64, 80)}
    out["w2_e2_sync_D64_A_alone_L640"] = r14_e2_sync_spec(64, B=False)
    out["w2_e2_sync_D64_B_alone_L640"] = r14_e2_sync_spec(64, A=False)
    return out


# ---------------------------------------------------------------------------- r12 SCE (registry proposal, verbatim)
# r12/registry_proposal/sce_compositions.py (02:26:56), merged by r21 WAVE 4: helper names prefixed _sce_ / SCE_
# to keep this module's namespace; otherwise unchanged. Every placement is a registered block.
SCE_GATES = ("DA", "DB", "DA2", "DB2")
SCE_BESIDE = {"DA": "dev.main_nodes", "DB": "dev.armB_nodes", "DA2": "dev.main_nodes", "DB2": "dev.armB_nodes"}


def sce_e07_spec(L=100, X0=6, XJ=22, nA=44, nB=44, k=20, k2=28, q_arrival=28, eid="E07_sce_collapse_entanglement"):
    """SCE (b) collapse by the approval router and (c) common-past Z4 Bell test on r13's beam-splitter device.
    Base: quantum (1,0,-1) reaching the gates at q_arrival, four phase gates at phase 1, a light clock at z = 70.
    Controls: b_cal_phi0..3, b_none, b_appA, b_appB, b_appA_only, b_device_only, b_none_clock, b_appA_clock, and
    c_tA{a}_tB{b}_lam{l} (a, b, l in 0..3)."""
    iJ = XJ - X0
    t_meet = iJ - (iJ + k - q_arrival)                     # quantum head at the junction

    def quantum(lam=0):
        return {"path": "main", "f": F, "lead": iJ + k - (q_arrival + lam)}
    approval = {"A": {"path": "~main", "f": F, "lead": nA - t_meet},
                "B": {"path": ["~armB", f"main[{iJ}:{iJ + 1}]", f"~main[:{iJ}]"], "f": F, "lead": nB - t_meet}}
    spec = r13_device_spec(q_arrival, None, {"A": 1, "B": 1, "A2": 1, "B2": 1}, L=L, X0=X0, XJ=XJ, nA=nA, nB=nB,
                           k=k, k2=k2, steps=60, name=eid)
    spec["placements"].append(plus_fibre("CLK", 1, L - 3, L // 2, 70, [(50, 4), (50, 44)]))
    spec["note"] = ("r12 SCE parts (b) and (c): r13 beam-splitter device (r04 junction + r08 phase gates), r12 approval "
                    "router packets (inward, merge at the junction), r08 light clock (pulse_train@1 at z = 70)")

    def ctl(name, packets, phases=None, keep_clock=False, gates=SCE_GATES):
        c = {"name": name, "override": {"dev": {"packets": packets}}}
        remove = [g for g in SCE_GATES if g not in gates] + ([] if keep_clock else ["CLK"])
        if remove:
            c["remove"] = remove
        for g, ph in (phases or {}).items():
            c["override"][g] = {"phase": ph}
        c["assertions"] = {"beside_fibre": [[g, SCE_BESIDE[g]] for g in gates]}
        return c
    q = quantum()
    ctls = [ctl(f"b_cal_phi{phi}", [q], {g: phi for g in SCE_GATES}) for phi in range(4)]
    ctls += [ctl("b_none", [q]), ctl("b_appA", [q, approval["A"]]), ctl("b_appB", [q, approval["B"]]),
             ctl("b_appA_only", [approval["A"]]), ctl("b_device_only", []),
             ctl("b_none_clock", [q], keep_clock=True), ctl("b_appA_clock", [q, approval["A"]], keep_clock=True)]
    for a, b, lam in product(range(4), repeat=3):
        ctls.append(ctl(f"c_tA{a}_tB{b}_lam{lam}", [quantum(lam)], {"DA": a, "DB": b}, gates=("DA", "DB")))
    spec["controls"] = ctls
    return spec


def _sce_front_sites(L, M, width, n0, zsign, amp):
    """Site triples of a right-moving exact (111)-type C0 front along n = x + y + zsign*z (r03 pulse111_cells)."""
    f = [0] * L
    for j in range(width):
        f[(n0 + j) % L] = amp * M
    out = {}
    for x, y, z in product(range(L), repeat=3):
        n = (x + y + zsign * z) % L
        a, b = f[(n + 1) % L], f[n]
        if a or b:
            out[(x, y, z)] = (a, b, 2)
    return out


def _sce_sum(*maps):
    out = {}
    for m in maps:
        for s, (a, b, r) in m.items():
            a0, b0, r0 = out.get(s, (0, 0, 2))
            out[s] = (a0 + a, b0 + b, r0 + r - 2)
    return {s: v for s, v in out.items() if v != (0, 0, 2)}


def sce_e07b_spec(L=6, M=1000, clock_site=(3, 3, 3), eid="E07b_sce_superposition_interference"):
    """SCE (a) two exact C0 fronts on one screen and (d) a C0 front through a dark clock, as all48_site@1
    placements. Controls: a_A, a_B, a_AB, a_ABplus, d_both, d_clock."""
    A, B = _sce_front_sites(L, M, 2, 1, +1, +1), _sce_front_sites(L, M, 2, 1, -1, -1)
    Bp = {s: (-a, -b, r) for s, (a, b, r) in B.items()}
    AB = _sce_sum(A, B)
    sites = sorted(set(A) | set(B))
    base = {s: AB.get(s, (0, 0, 2)) for s in sites}
    pl = [{"name": f"s{x}{y}{z}", "block": "all48_site@1", "params": {"triple": list(base[(x, y, z)])},
           "at": [x, y, z]} for (x, y, z) in sites]
    pl.append({"name": "clock", "block": "all48_site@1", "params": {"triple": [-1, -1, 0]}, "at": list(clock_site)})
    spec = {"format": "u24-composition-v1", "id": eid,
            "board": {"side": L, "background": [0, 0, 2], "coupling": {"signs": [1, 1, 1], "variant": None}},
            "placements": pl, "assertions": {}, "steps": 6,
            "note": ("r12 SCE parts (a) and (d): exact (111)-type C0 fronts as all48_site@1 placements; A along x+y+z "
                     "(= block exact_front_111_box), B along x+y-z with amplitude -M; the dark clock (-1,-1,0) at (3,3,3)")}

    def to(target, keep_clock):
        c = {"remove": sorted(f"s{x}{y}{z}" for (x, y, z) in set(A) | set(B) if (x, y, z) not in target), "override": {}}
        for s, v in target.items():
            if base[s] != v:
                c["override"][f"s{s[0]}{s[1]}{s[2]}"] = {"triple": list(v)}
        if not keep_clock:
            c["remove"].append("clock")
        return c
    spec["controls"] = [{"name": "a_A", **to(A, False)}, {"name": "a_B", **to(B, False)},
                        {"name": "a_AB", **to(AB, False)}, {"name": "a_ABplus", **to(_sce_sum(A, Bp), False)},
                        {"name": "d_both", **to(A, True)}, {"name": "d_clock", **to({}, True)}]
    return spec



# ---------------------------------------------------------------------------- r27 wave 2: entangled-pair detectors
BB27V2_DET_A = {0: ([0, -1, 4], 20), 1: ([1, 0, 4], 18), 2: ([0, -1, 4], 18), 3: ([1, 0, 4], 20)}
BB27V2_DET_B = {0: ([0, -1, 4], -18), 1: ([1, 0, 4], -20), 2: ([0, -1, 4], -20), 3: ([1, 0, 4], -18)}


def bb27v2_target_spec(psiA=0, psiB=0, control=None, L=160):
    """exp.bigbang_entangled_pair@1 (r27 bb27v2.ent): the rings2 hardware at T = 12 (data/compositions/
    bb27v2_base_target_T12_L160: movers ahead of every device) + two detector slot clocks on B0 set by the
    wing settings psi (r27 DET_A / DET_B: psi -> (state, x)); control 'noP' = detectors (0, 0) without the two
    light packets, 'nodet' = no detectors (the base itself)."""
    import json
    spec = json.loads(json.dumps(_registry_data("compositions/bb27v2_base_target_T12_L160.composition.json")))
    if L != 160:
        raise ValueError("the bb27v2 base is registered for L = 160")
    if control == "nodet":
        spec["id"] = "bb27v2_ent_ctrl_nodet_target_T12_L160"
        return spec
    if control == "noP":
        psiA, psiB = 0, 0
        spec["placements"] = [p for p in spec["placements"] if p["name"] not in ("Pp", "Pm")]
        for p in spec["placements"]:
            if p["name"] == "B0":
                p["params"]["sockets"] = []
    elif control is not None:
        raise ValueError(control)
    for name, table, psi in (("detA", BB27V2_DET_A, psiA), ("detB", BB27V2_DET_B, psiB)):
        st, x = table[psi]
        spec["placements"].append({"name": name, "block": "slot_clock@1", "params": {"state": list(st)},
                                   "at": [x % L, 0, 4]})
    spec["id"] = f"bb27v2_ent_{'ctrl_' + control if control else f'pA{psiA}_pB{psiB}'}_target_T12_L160"
    spec["observables"] = {**spec.get("observables", {}), "detectors": {"A": {"site": [BB27V2_DET_A[psiA][1] % L, 0, 5],
                                                                        "channel": 4},
                                                                  "B": {"site": [BB27V2_DET_B[psiB][1] % L, 0, 5],
                                                                        "channel": 4},
                                                                  "window": [16, 25]}}
    return spec


def bb27v2_seedstar_spec(psiA=0, psiB=0, control=None, L=160):
    """The seed* of a bb27v2 universe: its dark network + seed.bb27_point@1 at O (T + 4 = 16 updates before the
    target). Not defined for control 'noP' (its seed is the gliders' part only; use the recipe)."""
    if control == "noP":
        raise ValueError("the noP control has no bb27_point seed (use S0 = JR(F^16(JR(T))))")
    t = bb27v2_target_spec(psiA, psiB, control, L)
    return _bb27_seed_from(t, 12, L, True, (0, 0, 3), t["id"].replace("_target_T12", "_seedstar"))


def bb27v2_cases():
    """r27's bb27v2 seed* init files that are compositions (16 settings + the no-detector control)."""
    out = {f"bb27v2_ent_pA{a}_pB{b}_seedstar_L160": bb27v2_seedstar_spec(a, b) for a in range(4) for b in range(4)}
    out["bb27v2_ent_ctrl_nodet_seedstar_L160"] = bb27v2_seedstar_spec(control="nodet")
    return out



def r14_w3_created_spec(L=1280, xA1=220, Y=-24, rungs=(60, 106, 132), h=10, seed=True, line2=True, seed_start=8,
                        steps=720):
    """exp.created_co_moving_einstein@1 (r14 W3, w3_module.build): seed line A0 (matter_line@2, catalog medium '0002') with
    the 1/2-speed class-0002 seed glider at seed_start; creation lines B0 (y = 0) and B1 (y = Y), phase 0;
    the created gliders' line A1 at x = xA1 (class 0); rungs (phase 1) and the collector (label 41 along y at
    xA1 + h, phase 1). Controls: seed=False (no seed), line2=False (one creation junction)."""
    med = R06_CATALOG["0002"]
    pl = [{"name": "A0", "block": "matter_line@2",
           "params": {"length": L, "medium": med["medium"], "medium_origin": seed_start,
                      "sockets": [(seed_start - k) % L for k in range(3)] if seed else []},
           "at": [0, 0, 3], "wrap": True},
          {"name": "A1", "block": "matter_line@1", "params": {"length": L}, "at": [xA1, 0, 3]}]
    for nm, yb in (("B0", 0), ("B1", Y % L))[: 2 if line2 else 1]:
        pl.append({"name": nm, "block": "light_line@1", "params": {"length": L, "gauge_phase": 0}, "at": [0, yb, 4]})
    for j, yr in enumerate(rungs):
        pl.append({"name": f"rung{j}", "block": "light_line@1", "params": {"length": L, "gauge_phase": 1},
                   "at": [0, yr % L, 4]})
    pl.append({"name": "collector", "block": "light_line@1",
               "params": {"length": L, "label": 41, "axis": "y", "gauge_phase": 1}, "at": [xA1 + h, 0, 3]})
    if seed:
        pl.append({"name": "seed", "block": "slow_glider@2", "params": {"start": seed_start, "hit": med},
                   "at": [0, 0, 3], "wrap": True})
    tag = "joint" if seed and line2 else ("noseed" if line2 else "onejunction")
    return {"format": FORMAT, "id": f"r14_w3_created_einstein_{tag}_L{L}", "board": _board(L, MPP),
            "placements": pl, "steps": steps,
            "timing": {"t0": 0, "declared": {"passage_laws": ["232 + 3y", "356 + 3y"], "delta": 23}}}


def r14_w3_cases():
    return {"w3_created_einstein_joint_L1280": r14_w3_created_spec(),
            "w3_created_einstein_noseed_L1280": r14_w3_created_spec(seed=False),
            "w3_created_einstein_onejunction_L1280": r14_w3_created_spec(line2=False)}


# ---------------------------------------------------------------------------- appended published blocks (dff39dc)
def published_appended_specs():
    """The eight blocks appended to the published package after the 338 (R10E-41..48) as compositions of
    registered blocks: r11's twin atoms (exp.twin_atoms@1 instances and controls) and the D1 skeleton's 2L
    extension and no-seed control (exp.bigbang_network)."""
    def tw(L, tiles, q2):
        return twins_spec(L, tiles, q2, 3, s1=(-1, 0, 4) if q2 == 8 else (-1, 0, 0), s2=(-1, 0, 0))
    from .compose import apply_control
    t = tw(160, 1, 12)
    lower = [p["name"] for p in t["placements"] if p["name"].startswith("lcore")]
    return {"twin_atoms_q212_L160": t, "twin_atoms_q212_L320": tw(320, 2, 12),
            "twin_atoms_q28_L160": tw(160, 1, 8), "twin_atoms_q28_L320": tw(320, 2, 8),
            "twin_atoms_q212_L160_control_no_lower_cores": apply_control(t, {"name": "no_lower_cores",
                                                                             "remove": lower}),
            "twin_atoms_q212_L160_control_no_seed": apply_control(t, {"name": "no_seed", "remove": ["seed"],
                                                                      "unfill_sockets": True}),
            "d1_skeleton_atom_spin_clocks_L320": d1_skeleton_spec(320, 2),
            "d1_skeleton_atom_spin_clocks_L160_control_no_seed": apply_control(
                d1_skeleton_spec(160), {"name": "no_seed", "remove": ["seed"], "unfill_sockets": True})}


# ===================================================================== WAVE 5 (r21; r16b ARCHITECT_REPORT2 s3 fixes)
# ---------------------------------------------------------------------------- r28 split-pair reader / r27b ring tap
W6_DIRS = {"z": [[0, 3], [4, 4], [1, 3], [5, 4]], "h1": [[0, 4], [4, 3], [1, 4], [5, 3]]}   # one lap from K = J + x
H1_BACK_DIRS = [[4, 3], [0, 4], [5, 3], [1, 3]]     # the h1 loop traversed backwards from K (closed)


def w6_node(J, kind, i, signs=MPP):
    """(site, channel, sigma) of node i of r04's W6 ring at junction J (first lap; sigma0 = +1 at K = J + x);
    kind 'z' (= 'hz', spin_ring_z@1) or 'h1' (spin.holonomy_ring_h1@1)."""
    c = Coupling(tuple(signs))
    K = (J[0] + 1, J[1], J[2])
    return G.channel_path(c, K, c.ports[0][41], G.expand_dirs(W6_DIRS["z" if kind == "hz" else kind]), None,
                          sigma0=1)[i]


def ring_tap_placement(name, J, kind="h1", node=9, exit_dir=4, length=200, holes=(), signs=MPP, path_name="T"):
    """clock.ring_emitter@2 (update-of clock.ring_emitter@1; r27b ring_tap@1): the r04 B13 tap on a W6 ring at
    junction J -- a straight exit fibre leaving ring node ``node`` through port ``exit_dir``, its gauge continued
    from the ring (sigma = sigma_node * w); ``holes`` = leading fibre nodes left out (the emitter-masked control).
    The ring is the host's block."""
    c = Coupling(tuple(signs))
    s, g, sig = w6_node(J, kind, node, signs)
    fib = G.channel_path(c, G.add(s, exit_dir), c.ports[exit_dir][g], [exit_dir] * (length - 1), None,
                         sigma0=sig * c.weights[exit_dir][g])
    k = len(holes)
    if tuple(holes) != tuple(range(k)):
        raise ValueError("only leading holes (0, 1, ...) are supported")
    s0, g0, sg0 = fib[k]
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": path_name, "start": list(s0), "g0": g0, "sigma0": sg0,
                                  "dirs": [[exit_dir, length - 1 - k]]}]},
            "at": [0, 0, 0], "wrap": True}


def split_pair_reader_placement(name, J, kind, length=100, direction=4, signs=MPP):
    """gate.split_pair_reader@1 (r28 I4): the ring tap at node 7 -- the antipode of K = J + x -- of a W6 ring
    leaving through ``direction`` (+z; r28 falls back to +x where the network halo is not clean)."""
    return ring_tap_placement(name, J, kind, 7, direction, length, (), signs, path_name="X")


def r28_reg9b_spec(config="Zr", L=128, J=(0, 40, 5), start=52, length=60, direction=4):
    """r28 REG-9b isolated boards (wave2.w6_parts + reader_fibre): a label-41 matter line through J with a SLOW
    glider (start 52) feeding the W6 ring at J (Z*: spin_ring_z@1, H*: the holonomy-1 ring), plus the reader
    (Zr, Hr). Zrot is the C-image of Z0 plus the reader (a recipe)."""
    kind = "z" if config[0] == "Z" else "h1"
    pl = [{"name": "A0", "block": "matter_line@1", "params": {"length": L, "sockets": [(start - k) % L for k in (2, 1, 0)]},
           "at": [0, 0, J[2]], "wrap": True},
          ({"name": "ring", "block": "spin_ring_z@1", "params": {}, "at": list(J), "wrap": True} if kind == "z"
           else h1_ring_placement("ring", J)),
          {"name": "G", "block": "slow_glider@1", "params": {"start": start, "hit": "SLOW"}, "at": [0, 0, J[2]],
           "wrap": True}]
    if config in ("Zr", "Hr"):
        pl.append(split_pair_reader_placement("reader", J, kind, length, direction))
    return {"format": FORMAT, "id": f"r28_reg9b_{config}_L{L}", "board": _board(L, MPP), "placements": pl,
            "steps": 150, "timing": {"t0": 0, "declared": {"reader_site": "exit node 3",
                                                           "z_ring": "one passage per lap (18)",
                                                           "h1_ring": "one merged passage per lighting"}}}


def r28_module_readers(L, length=100, direction=4):
    """The created split-pair module (r28 module.r27_split_pair_module): readers on r27's lower z-ring
    (J_lo = (0, -16, 3)) and upper h1 ring (J_up = (0, 16, 3)); placed on an r27 bb27v3_h1 board."""
    return [split_pair_reader_placement("Rlo", (0, (-16) % L, 3), "z", length, direction),
            split_pair_reader_placement("Rup", (0, 16, 3), "h1", length, direction)]


def ring_clock_h1_placement(name, J, leads=(3,), back_leads=(), f=(1, -1), signs=MPP):
    """clock.ring_clock_h1@1 (r27b ring_clock_h1@1; variant-of light.fibre_ring@1): the spin.holonomy_ring_h1@1
    path (closed, 14 nodes from K = J + x) carrying prepared packets of shape f; back_leads on the same loop
    traversed backwards. One packet: the free ring clock (period 14); leads (3,) + back_leads (3,): period 22."""
    g0 = _ports(signs)[0][41]
    paths = [{"name": "R", "start": [1, 0, 0], "g0": g0, "dirs": H1_RING_DIRS, "sigma0": 1}]
    closed = ["R"]
    pk = [{"path": "R", "f": list(f), "lead": int(v)} for v in leads]
    if back_leads:
        paths.append({"name": "Q", "start": [1, 0, 0], "g0": g0, "dirs": H1_BACK_DIRS, "sigma0": 1})
        closed.append("Q")
        pk += [{"path": "Q", "f": list(f), "lead": int(v)} for v in back_leads]
    return {"name": name, "block": "guide_net@1", "params": {"paths": paths, "packets": pk, "closed": closed},
            "at": list(J), "wrap": True}


def ring_clock_h1_spec(L=64, back_leads=(), steps=100):
    """r27b's ring-clock calibration boards: matter line A0 + the ring clock at J = (0, L/2, 3)."""
    return {"format": FORMAT, "id": f"bb27v4_ringclock_{'two' if back_leads else 'one'}_L{L}", "board": _board(L, MPP),
            "placements": [{"name": "A0", "block": "matter_line@1", "params": {"length": L, "sockets": []},
                            "at": [0, 0, 3], "wrap": True},
                           ring_clock_h1_placement("clock", (0, L // 2, 3), (3,), back_leads)],
            "steps": steps}


def mirror_bridge_placement(name, node_at, node_r, runs=((4, 4), (3, 24)), label=1, signs=MPP, wrap=False):
    """medium.mirror_bridge@1 (r27b bridge@1; variant-of medium.guide_bridge@1): a gauged light path leaving the
    light-line node at ``node_at`` (rest remainder node_r) through the run-length directions ``runs``, the node
    itself excluded and its gauge continued; it ends open (a mirror) instead of descending to the other line."""
    c = Coupling(tuple(signs))
    if node_r not in (0, 4):
        raise ValueError("a light-line node rests at r = 0 or 4")
    nodes = G.channel_path(c, (0, 0, 0), label, G.expand_dirs(runs), None, sigma0=1 if node_r == 4 else -1)
    s1, g1, sg1 = nodes[1]
    rest = [[int(d), int(n)] for d, n in runs]
    rest[0][1] -= 1
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "B", "start": list(s1), "g0": g1, "sigma0": sg1,
                                  "dirs": [r for r in rest if r[1] > 0]}]},
            "at": list(node_at), "wrap": wrap}


# ---------------------------------------------------------------------------- r30 wu_half_cross
def wu_half_cross_spec(signs, b=1, variant="V2", side=24, parent=True, steps=20):
    """parity.wu_half_cross@1 (r30 wucross.spec3): +x arm = light_line@1 label 3, +y arm = light_line@1 label 37
    (gauge phase 1), parent = single_channel@1 label 11 at o = (c, c, c) with (0, b, 2). V2: half arms from o;
    V1: full lines (they cross at (c-1, c-1, c); decoder v1.0 mis-assigns tracks there)."""
    c = side // 2
    if variant == "V1":
        lx = {"length": side, "label": 3, "axis": "x", "gauge_phase": 1}, [0, c - 1, c]
        ly = {"length": side, "label": 37, "axis": "y", "gauge_phase": 1}, [c - 1, 0, c]
    else:
        lx = {"length": side - c, "label": 3, "axis": "x", "gauge_phase": 1}, [c, c - 1, c]
        ly = {"length": side - c, "label": 37, "axis": "y", "gauge_phase": 1}, [c - 1, c, c]
    pl = [{"name": "light_x", "block": "light_line@1", "params": lx[0], "at": lx[1]},
          {"name": "light_y", "block": "light_line@1", "params": ly[0], "at": ly[1]}]
    if parent:
        pl.append({"name": "parent", "block": "single_channel@1", "params": {"channel": 11, "triple": [0, b, 2]},
                   "at": [c, c, c]})
    tag = "".join("+" if s > 0 else "-" for s in signs)
    return {"format": FORMAT, "id": f"wu_{variant}_{tag}_b{b:+d}_L{side}", "placements": pl, "assertions": {},
            "board": {"side": side, "background": [0, 0, 2], "coupling": {"signs": list(signs), "variant": None}},
            "steps": steps}


def r30_cases():
    out = {}
    for tag, signs in (("-+-", (-1, 1, -1)), ("--+", (-1, -1, 1)), ("-++", (-1, 1, 1)), ("---", (-1, -1, -1))):
        for b in (1, -1):
            out[f"wu_V2_{tag}_b{b:+d}_L24"] = wu_half_cross_spec(signs, b, "V2")
    for tag, signs in (("-++", (-1, 1, 1)), ("-+-", (-1, 1, -1))):
        out[f"wu_V1_{tag}_b+1_L24"] = wu_half_cross_spec(signs, 1, "V1")
    return out


# ---------------------------------------------------------------------------- r19 race comparator / heralded Z6
def _race_fibre(name, y, z, xlen, approval_head, threshold_head):
    """One race (r19 W2-A): channel-0 fibre x in [1, xlen] (+++), approval = unit pulse moving +x with head at x,
    threshold = its mirror image moving -x with head at x (on '~P': index counted from x = xlen)."""
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "P", "g0": 0, "dirs": [[0, xlen - 1]]}],
                       "packets": [{"path": "P", "f": F, "lead": approval_head - 1},
                                   {"path": "~P", "f": F, "lead": xlen - threshold_head}]},
            "at": [1, y, z]}


def r19_race_spec(Hh=10, spacing=3):
    """detect.race_comparator@1 board (r19 W2-A, race.main): races (proj, t in -H..H), one fibre each on a
    (2H+1)^2 transverse grid; they meet at x = M + proj + t at update D + t - proj (decision click kind 2, q = +1)."""
    D = 2 * Hh + 6
    M = D + 2 * Hh + 6
    xlen, n = 2 * M, 2 * Hh + 1
    side = max(xlen + 2, spacing * n + 4)
    races = [(p, t) for p in range(-Hh, Hh + 1) for t in range(-Hh, Hh + 1)]
    pl = [_race_fibre(f"r{k}", 2 + spacing * (k % n), 2 + spacing * (k // n), xlen, M - D + 2 * p, M + D + 2 * t)
          for k, (p, t) in enumerate(races)]
    return {"format": FORMAT, "id": f"r19_race_H{Hh}", "board": _board(side, PPP), "placements": pl,
            "steps": D + 2 * Hh + 8,
            "timing": {"t0": 0, "declared": {"outcome": "sgn(proj + t)", "E(proj)": "2 proj / (2H + 1)"}}}


TWO_COS = [2, 1, -1, -2, -1, 1]


def r19_heralded_z6_spec(D=10, M=20, spacing=3, trials=None):
    """detect.heralded_projection_z6@1 board (r19 W3, heralded_z6.main): 432 trials (alpha, beta, phi in Z6,
    t in {0,1}), three races each (A: proj_A, threshold 0; B1 / B2: proj_B, thresholds -t / +t) = 1,296 races on
    one board; heralded on Bob's detections (a declared post-selection). ``trials`` = a subset (default: all)."""
    trials = trials if trials is not None else [(al, be, phi, t) for al in range(6) for be in range(6)
                                               for phi in range(6) for t in (0, 1)]
    races = []
    for al, be, phi, t in trials:
        pa, pb = TWO_COS[(al - phi) % 6], TWO_COS[(be - phi) % 6]
        races += [(pa, 0), (pb, -t), (pb, t)]
    n = math.ceil(math.sqrt(len(races)))
    side = max(2 * M + 4, spacing * n + 4)
    pl = [_race_fibre(f"r{j}", 2 + spacing * (j % n), 2 + spacing * (j // n), 2 * M, M - D + 2 * p, M + D + 2 * th)
          for j, (p, th) in enumerate(races)]
    return {"format": FORMAT, "id": "r19_heralded_z6", "board": _board(side, PPP), "placements": pl, "steps": D + 8,
            "timing": {"t0": 0, "declared": {"heralded_E": "-cos(60 deg (alpha - beta))", "heralded_fraction": "2/3"}}}


# ---------------------------------------------------------------------------- r25 E11 light clocks
FAMILIES = {"d1": (1, 1, 1), "d2": (1, 1, -1), "d3": (1, -1, 1), "d4": (-1, 1, 1)}
E11_CLOCKS = {"d1": (2, 1), "d2": (1, 1), "d3": (1, 2), "d4": (2, 2)}


def _profile(j, L):
    vals = [2 * math.cos(2 * math.pi * j * n / L) for n in range(L)]
    out = [round(v) for v in vals]
    if any(abs(v - o) > 1e-12 for v, o in zip(vals, out)):
        raise ValueError("profile is not an exact integer cosine on this side")
    return out


def _a1_sites(name, L, scalar, steps):
    pl = [_site(f"s{x}_{y}_{z}", (x, y, z), (a, b, r)) for (x, y, z), (a, b, r) in sorted(scalar.items())
          if (a, b, r) != (0, 0, 2)]
    return {"format": FORMAT, "id": name, "board": _board(L, PPP), "placements": pl, "steps": steps}


def e11_main_diagonal_spec(side=6, clocks=None, steps=24):
    """E11 main (r25 preparations_e11.main_diagonal; clock.diagonal_light_clock@1): four exact diagonal light
    clocks, a forward f(n - t) and a backward g(n + t) wave per body-diagonal family n = s.x, f, g = 2 cos(2 pi j n
    / 6), all 48 channels of every site in one triple (A1 light; all48_site@1 placements)."""
    clocks = clocks or E11_CLOCKS
    L = side
    scalar = {}
    for x in range(L):
        for y in range(L):
            for z in range(L):
                a = b = 0
                for nm, (jf, jb) in clocks.items():
                    s = FAMILIES[nm]
                    n = (s[0] * x + s[1] * y + s[2] * z) % L
                    f, g = _profile(jf, L), _profile(jb, L)
                    b += f[n] + g[n]
                    a += f[(n + 1) % L] + g[(n - 1) % L]
                scalar[(x, y, z)] = (a, b, 2)
    return _a1_sites("e11_main_diagonal", L, scalar, steps)


def e11_control_generic_spec(side=5, n1=1, n2=2, M=1000, steps=24):
    """E11 control (preparations_e11.generic_clock): a y-uniform light clock along z under a transverse standing
    wave cos(2 pi x / 5) (lattice-scale k, rounding active: not an exact family)."""
    L = side
    kap = 2 * math.pi / L
    k1, k2 = n1 * kap, n2 * kap
    w = [math.acos((2 * math.cos(kap) + 2 + 2 * math.cos(k)) / 6) for k in (k1, k2)]
    scalar = {}
    for x in range(L):
        for y in range(L):
            for z in range(L):
                b = round(M * math.cos(kap * x) * (math.cos(k1 * z) + math.cos(k2 * z)))
                a = round(M * math.cos(kap * x) * (math.cos(k1 * z + w[0]) + math.cos(k2 * z + w[1])))
                scalar[(x, y, z)] = (a, b, 2)
    return _a1_sites("e11_control_generic", L, scalar, steps)


def r25_e11_cases():
    return {"main_diagonal_L6": e11_main_diagonal_spec(), "control_generic_L5": e11_control_generic_spec()}


# ---------------------------------------------------------------------------- r23 E09 Einstein 1911
def e09_line_spec(L=160, k=0, P=8, x_first=60, probe=None, steps=150):
    """E09 Shapiro / river board (r23 e09_build.line_board): gravity.counter_flux_link@1 with an inbound ('in',
    head x, moving +x) or co-moving ('co', head x, moving -x) probe."""
    y0 = L // 2
    bwd = [(L - 2) - (x_first + j * P) for j in range(k)]
    fwd = []
    if probe is not None:
        kind, x = probe
        if kind == "in":
            fwd = [x - 1]
        else:
            bwd = bwd + [(L - 2) - x]
    return {"format": FORMAT, "id": f"e09_line_k{k}", "board": _board(L, PPP),
            "placements": [_x_fibre("F", L, y0, y0, fwd=fwd, bwd=bwd)], "steps": steps}


def e09_y_spec(L=160, J=18, lenA=106, lenB=118, k=0, P=8, s_first=60, probe=True, start=(2, 32, 32), steps=170):
    """E09 bending board (e09_build.y_board): main fibre along +x (input + arm A), r04 degree-3 junction at main
    node J with the branch (arm B) along +y; k flux packets on arm A moving toward the junction."""
    n_main = J + lenA
    pk = [{"path": "main", "f": F, "lead": 4}] if probe else []
    pk += [{"path": "~main", "f": F, "lead": (n_main - 1) - (J + s_first + j * P)} for j in range(k)]
    return {"format": FORMAT, "id": f"e09_y_k{k}", "board": _board(L, PPP), "steps": steps,
            "placements": [{"name": "Y", "block": "guide_net@1",
                            "params": {"paths": [{"name": "main", "g0": 0, "dirs": [[0, n_main - 1]]},
                                                 {"name": "armB", "branch_of": "main", "at_node": J, "dir": 2,
                                                  "length": lenB}],
                                       "packets": pk}, "at": list(start)}]}


def e09_emitter_spec(L=200, M=160, counter=False, clock=True, start=(10, 10, 70), jnode=6, exit_dir=5, steps=220,
                     counter_lead=4):
    """E09 redshift board (r23 e09_make.emitter, the runs' builder): clock.ring_emitter@1 (4 x 4 ring, tap at node 6,
    exit fibre of M nodes along -z) with its clock packet (lead 3) and optionally one counter-circulating packet at
    reversed-ring lead 4 (two pulses per 24 at the exit)."""
    ring = _ring("E", start, 4, 4, leads=(3,) if clock else (), counter_leads=[counter_lead] if counter else [],
                 tap=(jnode, exit_dir, M))
    return {"format": FORMAT, "id": f"e09_emitter_c{int(counter)}_k{int(clock)}", "board": _board(L, PPP),
            "placements": [ring], "steps": steps}


def r23_e09_cases():
    """E09's runs (r23 e09_make.runs_spec) as compositions; redshift_flux_check_16 is dropped (it equals
    redshift_clock_in_flux: same init, final-state and log hashes; r16b)."""
    out = {}
    for k in range(7):
        out[f"shapiro_k{k}"] = e09_line_spec(k=k, probe=("in", 5))
    out["shapiro_flux_only"] = e09_line_spec(k=6)
    out["river_comoving"] = e09_line_spec(k=6, probe=("co", 150))
    out["river_comoving_no_flux"] = e09_line_spec(k=0, probe=("co", 150))
    for k in range(6):
        out[f"bending_k{k}"] = e09_y_spec(k=k)
    out["bending_flux_only"] = e09_y_spec(k=5, probe=False)
    out["redshift_far_clock"] = e09_emitter_spec(counter=False)
    out["redshift_clock_in_flux"] = e09_emitter_spec(counter=True)
    out["redshift_no_packets"] = e09_emitter_spec(counter=False, clock=False)
    return out


# ---------------------------------------------------------------------------- r22 E10 prescribed relay lattice
E10_L, E10_STEPS, E10_B = 256, 200, 16
E10_KT = {"far": Fraction(1), "near": Fraction(3, 2)}
E10_RECT = {16: (4, 4), 24: (6, 6), 36: (8, 10)}         # rings that close after one lap (+++)
E10_EXIT_LEN = 200
E10_OFFSET = {"E": 0, "T": 85, "F": 170}                 # lattice offsets in y on the one board
E10_ZST = 220                                            # station plane
E10_RAYS = (8, 16, 24, 40)


def e10_kappa(v, shell, radial):
    t = E10_KT[shell]
    return Fraction(1) if v == "F" else (t if v == "T" else (t * t if radial else t))


def _e10_link_dirs(n, w=4):
    e = n - E10_B
    if e < 0 or e % 2:
        raise ValueError(f"link node count {n} must be {E10_B} + an even number")
    if e == 0:
        return [[0, E10_B]]
    a = (E10_B - w) // 2
    return [[0, a], [4, e // 2], [0, w], [5, e // 2], [0, E10_B - w - a]]


def _e10_meander(counts, tail):
    out = []
    for n in counts:
        out += _e10_link_dirs(int(n))
    return out + [[0, tail]]


def e10_ray_counts(v, b):
    out = []
    for k in range(8):
        xm = -64 + 16 * k + 8
        r = math.hypot(xm, b)
        shell = "near" if r < 32 else "far"
        radial = abs(xm) / r > 1 / math.sqrt(2)
        out.append(int(E10_B * e10_kappa(v, shell, radial)))
    return out


def e10_route_counts(v):
    return [int(E10_B * e10_kappa(v, s, True)) for s in ("far", "near", "near", "far")], [E10_B] * 6


def _e10_guide(name, at, paths, packets=(), closed=()):
    return {"name": name, "block": "guide_net@1", "at": list(at),
            "params": {"paths": paths, "packets": list(packets), "closed": list(closed)}}


def e10_lattice(v):
    """One lattice of r22's E10 (variant 'E': kappa_r = kappa_t^2, 'T': the 1911 twin kappa_r = kappa_t, 'F': flat)
    at its y offset (r22 e10_build.lattice, ported): ring clocks with taps, cavities, a radial probe, four rays and
    two routes, every fibre a guide_net@1 path whose coarse links carry 16 kappa nodes (z-bump meanders)."""
    pl, y0, zst = [], E10_OFFSET[v], E10_ZST
    for i, (key, shell, radial) in enumerate((("ring_t_far", "far", False), ("ring_t_near", "near", False),
                                             ("ring_r_far", "far", True), ("ring_r_near", "near", True))):
        N = int(16 * e10_kappa(v, shell, radial))
        pl.append(_e10_guide(f"{v}_{key}", (10 + 20 * i, y0 + 50, zst),
                             [{"name": "R", "g0": 0, "dirs": _rect(*E10_RECT[N])},
                              {"name": "X", "branch_of": "R", "at_node": 6, "dir": 5, "length": E10_EXIT_LEN}],
                             [{"path": "R", "f": F, "lead": 3}], ["R"]))
    for key, shell, radial, x, dy in (("cav_t_far", "far", False, 90, 52), ("cav_r_far", "far", True, 90, 60),
                                      ("cav_t_near", "near", False, 110, 52), ("cav_r_near", "near", True, 110, 60)):
        D = int(8 * e10_kappa(v, shell, radial))
        pl.append(_e10_guide(f"{v}_{key}", (x, y0 + dy, zst), [{"name": "C", "g0": 0, "dirs": [[0, D - 1]]}],
                             [{"path": "C", "f": F, "lead": 3}]))
    pl.append(_e10_guide(f"{v}_radial_probe", (10, y0 + 16, 80),
                         [{"name": "P", "g0": 0, "dirs": _e10_meander([int(E10_B * e10_kappa(v, "near", True)),
                                                                     int(E10_B * e10_kappa(v, "far", True))], 40)}],
                         [{"path": "P", "f": F, "lead": 3}]))
    for b in E10_RAYS:
        pl.append(_e10_guide(f"{v}_ray_b{b}", (10, y0 + b, 20),
                             [{"name": "P", "g0": 0, "dirs": _e10_meander(e10_ray_counts(v, b), 10)}],
                             [{"path": "P", "f": F, "lead": 3}]))
    ra, rb = e10_route_counts(v)
    pl.append(_e10_guide(f"{v}_route_A", (10, y0 + 8, 50), [{"name": "P", "g0": 0, "dirs": _e10_meander(ra, 20)}],
                         [{"path": "P", "f": F, "lead": 3}]))
    pl.append(_e10_guide(f"{v}_route_B", (10, y0 + 24, 50), [{"name": "P", "g0": 0, "dirs": _e10_meander(rb, 20)}],
                         [{"path": "P", "f": F, "lead": 3}]))
    return pl


def e10_spec_all():
    """E10 (r22 e10_build.spec_all, ported): ONE board holding three lattices side by side (E at y 0, T at y 85, F at
    y 170); control 'dark' = all packets removed. A PRESCRIBED, non-dynamical geometry, not sourced gravity. Equals
    E10's composition.json exactly."""
    pl = e10_lattice("E") + e10_lattice("T") + e10_lattice("F")
    guides = [p["name"] for p in pl]
    return {"format": FORMAT, "id": "e10_schwarzschild_ETF",
            "board": {"side": E10_L, "background": [0, 0, 2], "coupling": {"signs": [1, 1, 1], "variant": None}},
            "placements": pl, "assertions": {},
            "timing": {"t0": 0, "declared": {"label": "PRESCRIBED non-dynamical geometry, not sourced gravity",
                                              "lattices": {"E": "kappa_r = kappa_t^2 (y offset 0)",
                                                           "T": "1911 twin, kappa_r = kappa_t (y 85)",
                                                           "F": "flat (y 170)"},
                                              "base_link": E10_B, "kappa_t": {"far": "1", "near": "3/2"}}},
            "controls": [{"name": "dark", "override": {g: {"packets": []} for g in guides}}],
            "steps": E10_STEPS}


def e10_lamp_spec():
    """E10 lamp control (r22 e10_build.lamp_spec): an all-48 (-1,-1,0) lamp touching its fibre (on-site clock,
    blind to the prescribed geometry)."""
    return {"format": FORMAT, "id": "e10_lamp", "board": _board(128, PPP),
            "placements": [{"name": "lamp_fibre", "block": "guide_net@1",
                            "params": {"paths": [{"name": "P", "g0": 0, "dirs": [[0, 100]]}]}, "at": [14, 40, 40]},
                           {"name": "lamp", "block": "all48_site@1", "params": {"triple": [-1, -1, 0], "halo": True},
                            "at": [64, 41, 40]}],
            "assertions": {}, "timing": {"t0": 0, "declared": {"note": "on-site clock: blind to the prescribed geometry"}},
            "steps": 90}


# ===================================================================== WAVE 6 (r21b)
# ---------------------------------------------------------------------------- r36 cyclic universes, r27b bounce
#: seed.cyclic_point@1 (r36): the JR-invariant bang seed, literal cells [dx, dy, dz, g, a, b, r] relative to the bang
#: node O, a node of a (-,+,+) light_line@2 (label 1 along x, gauge phase 0).  'head_on' (C1): the midpoint of two
#: fibre_packet@1 meeting head-on at a class-0 node; 'wall' (C2): the reflection midpoint at a bare line end (O = node
#: 0).  O and its line neighbours are written (two of them back to the vacuum), so they are sockets of the line.
CYCLIC_POINT = {
    "head_on": [[-1, 0, 0, 1, 0, 0, 2], [0, -1, 0, 35, 0, 0, 4], [0, 0, -1, 41, 0, 0, 4], [0, 0, 0, 1, 1, -1, 0],
                [0, 0, 1, 4, 0, 0, 4], [0, 1, 0, 22, 0, 0, 4], [1, 0, 0, 1, 0, 0, 2]],
    "wall": [[-1, 0, 0, 1, 0, 0, 0], [0, -1, 0, 35, 0, 0, 4], [0, 0, -1, 41, 0, 0, 4], [0, 0, 0, 1, 1, -1, 0],
             [0, 0, 1, 4, 0, 0, 4], [0, 1, 0, 22, 0, 0, 4], [1, 0, 0, 1, 0, 0, 2]]}
#: Literal t = 0 states of r36's two C1 controls relative to the same O (exact data, not seeds): one packet
#: (F^11 of the incoming pair without P-) and asymmetric arms (F^12 with P- at front 30; its moment is at node O + 1).
C1_CONTROL_CELLS = {
    "one_packet": [[1, 0, 0, 1, -1, 0, 0], [2, -1, 0, 35, 0, 0, 0], [2, 0, -1, 41, 0, 0, 0], [2, 0, 0, 1, -1, 1, 0],
                   [2, 0, 1, 4, 0, 0, 0], [2, 1, 0, 22, 0, 0, 0], [3, 0, 0, 1, 0, 1, 0]],
    "asymmetric": [[0, 0, 0, 1, 0, 0, 2], [1, -1, 0, 35, 0, 0, 0], [1, 0, -1, 41, 0, 0, 0], [1, 0, 0, 1, -1, 1, 4],
                   [1, 0, 1, 4, 0, 0, 0], [1, 1, 0, 22, 0, 0, 0], [2, 0, 0, 1, 0, 0, 2]]}
C1_AT, C1_N, C1_O = (4, 8, 8), 41, 20                       # C1 segment: 41 nodes from (4, 8, 8), bang node 20
C2_AT, C2_N, C2_A = (4, 40, 4), 74, ((40, 27, 3), 27)       # C2: light segment (wall = node 0), matter segment A
C3A_RING_AT = (100, 100, 60)


def cyclic_point_placement(form, O, name="seed", cells=None):
    """seed.cyclic_point@1 in socket form at the bang node O (form 'head_on' or 'wall'); ``cells`` overrides the data
    (the C1 controls)."""
    return {"name": name, "block": "literal_patch@1",
            "params": {"kind": "fibre-packet", "cells": [list(c) for c in (cells or CYCLIC_POINT[form])]},
            "at": list(O), "wrap": True}


def _socket_nodes(cells, axis=0):
    return sorted({c[axis] for c in cells if c[3] == 1 and all(c[i] == 0 for i in range(3) if i != axis)})


def cyclic_light_spec(L=64, steps=288):
    """exp.cyclic_light@1 (r36 C1): one 41-node (-,+,+) light segment whose bare ends are mirrors, with the head-on
    seed.cyclic_point@1 at node 20.  Period 48, moments 24Z (two-moment theorem).  Controls (r36's): 'dark' (no seed),
    'one_packet' (period 88) and 'asymmetric' (arms 20 / 21, period 96)."""
    O = (C1_AT[0] + C1_O, C1_AT[1], C1_AT[2])

    def line(cells):
        return [C1_O + n for n in _socket_nodes(cells)]
    pl = [{"name": "F0", "block": "light_line_s@1",
           "params": {"length": C1_N, "gauge_phase": 0, "sockets": line(CYCLIC_POINT["head_on"])},
           "at": list(C1_AT), "wrap": False},
          cyclic_point_placement("head_on", O)]
    controls = [{"name": "dark", "remove": ["seed"], "override": {"F0": {"sockets": []}}}]
    for name, cells in C1_CONTROL_CELLS.items():
        controls.append({"name": name, "override": {"F0": {"sockets": line(cells)}, "seed": {"cells": cells}}})
    return {"format": FORMAT, "id": f"cyclic_light_L{L}", "board": _board(L, MPP), "placements": pl,
            "timing": {"t0": "integer moment (JR S = S)", "declared": {"period": 48, "moments": "24Z"}},
            "controls": controls, "steps": steps}


def cyclic_matter_spec(L=256, steps=656):
    """exp.cyclic_matter@1 (r36 C2): a 74-node (-,+,+) light segment B with the wall form of seed.cyclic_point@1 at its
    bare end (node 0), and a 27-node matter segment A crossing it at the class-0 junction J = (40, 40) (B node 36):
    the seed's packet creates a glider pair at J; at T = 82 every product is at its mirror.  Period 164, moments 82Z.
    Controls: 'dark' (no seed) and 'no_matter' (A removed: a light-only cycle of period 154)."""
    (ax, ay, az), na = C2_A
    pl = [{"name": "B", "block": "light_line_s@1",
           "params": {"length": C2_N, "gauge_phase": 0,
                      "sockets": [n for n in _socket_nodes(CYCLIC_POINT["wall"]) if 0 <= n < C2_N]},
           "at": list(C2_AT), "wrap": False},
          {"name": "A", "block": "matter_line@1", "params": {"length": na, "sockets": []}, "at": [ax, ay, az],
           "wrap": False},
          cyclic_point_placement("wall", C2_AT)]
    return {"format": FORMAT, "id": f"cyclic_matter_L{L}", "board": _board(L, MPP), "placements": pl,
            "assertions": {"junction_classes": {f"{ax},{C2_AT[1]}": 0}},
            "timing": {"t0": "integer moment (JR S = S)", "declared": {"period": 164, "moments": "82Z",
                                                                        "creation_at_J": 43}},
            "controls": [{"name": "dark", "remove": ["seed"], "override": {"B": {"sockets": []}}},
                         {"name": "no_matter", "remove": ["A"], "assertions": {"junction_classes": None}}],
            "steps": steps}


def holonomy_ring_counterpair_placement(name, at, leads, n1=3, n2=36, g0=4, f=(1, -1), signs=MPP):
    """spin.holonomy_ring@2 (r36; update-of spin.holonomy_ring@1): an n1 x n2 rectangle in the x-y plane traversed twice
    as ONE closed guide_net@1 path 'main' (N = 2 (n1 + n2) sites per lap; one lap maps g0 to z.g0, so the two-lap loop
    closes on g0), carrying a counter-circulating pair of unit packets: leads[0] on 'main' and leads[1] on '~main' (the
    same packet as on the loop's backward closed path with lead + 1).  The pair meets head-on every N + 4 updates and
    X(t + N + 4) = C X(t) (C: g -> z.g).  Checked here: one lap returns to its site on z.g0, two laps close on g0."""
    lap = [[0, n1], [2, n2], [1, n1], [3, n2]]
    c = Coupling(tuple(signs))
    one = G.channel_path(c, (0, 0, 0), g0, G.expand_dirs(lap), None)
    if one[-1][0] != (0, 0, 0) or one[-1][1] != _group().multiplication[_group().central][g0]:
        raise ValueError(f"the {n1} x {n2} loop from channel {g0} is not a holonomy-z ring under {tuple(signs)}")
    if one[-1][2] != 1:
        raise ValueError("the two-lap loop needs one lap of gauge sign +1")
    return {"name": name, "block": "guide_net@1",
            "params": {"paths": [{"name": "main", "g0": g0, "dirs": lap + lap[:3] + [[3, n2 - 1]]}], "closed": ["main"],
                       "packets": [{"path": "main", "f": list(f), "lead": int(leads[0])},
                                   {"path": "~main", "f": list(f), "lead": int(leads[1])}]},
            "at": list(at), "wrap": True}


C3A_LEADS = {"incoming": (12, 127), "outgoing": (30, 145)}     # ring pair 11 updates before / after the bang
C3A_PACKET = {"incoming": (8, -1), "outgoing": (10, 1)}        # C2's packet (front, direction) on B


def cyclic_spin_spec(L=256, form="outgoing", steps=656):
    """exp.cyclic_spin@1 (r36 C3a): C2 plus spin.holonomy_ring@2 (3 x 36, N = 78, N + 4 = 82 = C2's T) at (100,100,60).
    At the bang the ring's pair is meeting (its own JR moment), which no registered generator writes, so the seed is
    prepared from a composition of registered blocks by an exact recipe:
    * form 'incoming' (r36's): the board 11 updates before the bang; seed = F^11(composition);
    * form 'outgoing': its JR image, the board 11 updates after the bang; seed = 11 exact rewinds of it.
    Both give the same seed because it is JR-fixed (JR F JR = F^-1, r36 Lemma 1).  Period 164; ring C-image every 82."""
    if form not in C3A_LEADS:
        raise ValueError("form is 'incoming' or 'outgoing'")
    front, direction = C3A_PACKET[form]
    (ax, ay, az), na = C2_A
    socks = [front, front + 1, front + 2] if direction == -1 else [front - 2, front - 1, front]
    pl = [{"name": "B", "block": "light_line_s@1", "params": {"length": C2_N, "gauge_phase": 0, "sockets": socks},
           "at": list(C2_AT), "wrap": False},
          {"name": "P", "block": "fibre_packet@1", "params": {"front": front, "direction": direction, "gauge_phase": 0},
           "at": list(C2_AT), "wrap": False},
          {"name": "A", "block": "matter_line@1", "params": {"length": na, "sockets": []}, "at": [ax, ay, az],
           "wrap": False},
          holonomy_ring_counterpair_placement("R", C3A_RING_AT, C3A_LEADS[form])]
    prep = {"advance": 11} if form == "incoming" else {"rewind": 11}
    return {"format": FORMAT, "id": f"cyclic_spin_{form}_L{L}", "board": _board(L, MPP), "placements": pl,
            "assertions": {"junction_classes": {f"{ax},{C2_AT[1]}": 0}},
            "timing": {"t0": f"{11 if form == 'incoming' else -11} updates from the bang", "declared": {
                "preparation": prep, "period": 164, "moments": "82Z", "ring": "X(t + 82) = C X(t)"}},
            "steps": steps}


#: exp.bigbang_bounce_v6@1 (r27b): the 20-cell literal of the exact bounce s*, [dx, dy, z, g, a, b, r] with x and y
#: relative to the bang site (0, 0) of the matter line A0 (z = 3) and the light line B0 (z = 4).
BOUNCE_V6_CELLS = [
    [0, 0, 3, 41, 0, 0, 2], [0, 0, 4, 1, 0, 0, 2], [0, 1, 2, 31, 0, 0, 0], [0, 1, 3, 41, -1, 1, 0],
    [0, 1, 4, 1, 0, 0, 0], [0, 2, 3, 41, 0, 0, 2], [0, -2, 3, 41, 0, 0, 2], [0, -1, 2, 31, 0, 0, 0],
    [0, -1, 3, 41, -1, 1, 0], [0, -1, 4, 1, 0, 0, 0], [1, 0, 3, 41, 0, 0, 4], [1, 0, 4, 1, 1, -1, 0],
    [1, 0, 5, 4, 0, 0, 4], [1, 1, 3, 13, 0, 0, 0], [1, 1, 4, 22, 0, 0, 4], [1, -1, 3, 13, 0, 0, 0],
    [1, -1, 4, 35, 0, 0, 4], [2, 0, 4, 1, 0, 0, 2], [-1, 1, 3, 27, 0, 0, 0], [-1, -1, 3, 27, 0, 0, 0]]


def bigbang_bounce_v6_spec(L=640):
    """exp.bigbang_bounce_v6@1 (r27b bb27v6): the exact bounce s* with JR(s*) = s* on the whole board -- r27's dark
    network reduced to zero-counter hardware (matter lines A0 / AH, light lines B0 / B+-12, the spin_ring_z@1 and h1
    rings, the ring tap, the A -> B bridge) plus the two all-48 gates at their JR-fixed phases 3 and 1 and one 20-cell
    literal at the bang site.  Runs: forward from s*; the bounce = s* rewound 240 exact steps, then 480 updates."""
    cells = sorted([[c[0] % L, c[1] % L, *c[2:]] for c in BOUNCE_V6_CELLS])
    pl = [{"name": "A0", "block": "matter_line@1", "params": {"length": L, "sockets": [0, 1, 2, L - 2, L - 1]},
           "at": [0, 0, 3], "wrap": True},
          {"name": "AH", "block": "matter_line@1", "params": {"length": L, "sockets": []}, "at": [61, 0, 3],
           "wrap": True},
          {"name": "B0", "block": "light_line_s@1", "params": {"length": L, "gauge_phase": 1, "sockets": [0, 1, 2]},
           "at": [0, 0, 4], "wrap": True},
          {"name": "Bup", "block": "light_line_s@1", "params": {"length": 148, "gauge_phase": 1, "sockets": []},
           "at": [3, 12, 4], "wrap": False},
          {"name": "Blo", "block": "light_line_s@1", "params": {"length": 148, "gauge_phase": 1, "sockets": []},
           "at": [3, L - 12, 4], "wrap": False},
          {"name": "ringA0", "block": "spin_ring_z@1", "params": {}, "at": [0, L - 16, 3], "wrap": True},
          {"name": "ringUp", "block": "guide_net@1",
           "params": {"paths": [{"name": "R", "start": [1, 0, 0], "g0": _ports(MPP)[0][41], "dirs": H1_RING_DIRS,
                                 "sigma0": 1}], "closed": ["R"]}, "at": [0, 16, 3], "wrap": True},
          {"name": "gateUp", "block": "phase_gate@2", "params": {"phase": 3, "offset": [0, 0, 2]}, "at": [107, 12, 4]},
          {"name": "gateLo", "block": "phase_gate@2", "params": {"phase": 1, "offset": [0, 0, 2]},
           "at": [107, L - 12, 4]},
          {"name": "tapLo", "block": "guide_net@1",
           "params": {"paths": [{"name": "T", "start": [4, 0, 5], "g0": 1, "sigma0": 1, "dirs": [[4, 79]]}]},
           "at": [0, L - 16, 3], "wrap": True},
          {"name": "bridgeAB", "block": "guide_net@1",
           "params": {"paths": [{"name": "B", "start": [0, 0, 1], "g0": 4, "sigma0": 1, "dirs": [[4, 3], [3, 24]]}]},
           "at": [69, 12, 4], "wrap": True},
          {"name": "bounce_seed", "block": "literal_patch@1", "params": {"kind": "glider-seed", "cells": cells},
           "at": [0, 0, 0], "wrap": True}]
    return {"format": FORMAT, "id": f"bb27v6_sstar_L{L}", "board": _board(L, MPP), "placements": pl, "steps": 240,
            "timing": {"t0": "the symmetric moment (JR s* = s*)",
                       "bounce_log": "exact rewind 240 then 480 updates (bounce at 240)"}}


# ---------------------------------------------------------------------------- r33 E13 field-line bundle
def _run_length(dirs):
    out = []
    for d in dirs:
        if out and out[-1][0] == d:
            out[-1][1] += 1
        else:
            out.append([d, 1])
    return out


def field_line_bundle_placement(name, at, rho=4, x_root=16, x_end=100, g0=0, flux=None, probe=None, packets=(),
                                root_sources=None, signs=PPP):
    """medium.field_line_bundle@1 (r33): ONE field_line_bundle@1 placement of the (2 rho)^2 open gauged staircases from
    the source point ``at`` (no junction), with parametric packets (the generator's ``flux``, ``probe``, ``packets``,
    ``root_sources``).  The halo condition is checked here and again by the generator."""
    if not bundle_halo_ok(Coupling(tuple(signs)), field_line_bundle_lines(rho, x_root, x_end), g0):
        raise ValueError("field lines share halo channels or touch: raise x_root or lower rho")
    params = {"rho": rho, "x_root": x_root, "x_end": x_end, "g0": g0}
    for k, v in (("flux", flux), ("probe", probe), ("root_sources", root_sources)):
        if v:
            params[k] = v
    if packets:
        params["packets"] = list(packets)
    return {"name": name, "block": "field_line_bundle@1", "at": list(at), "params": params}


E13 = {"rho": 4, "half": 24, "x_root": 16, "x_end": 100, "radii": (24, 32, 48, 96), "side": 200, "O": (0, 100, 100),
       "station": 1, "shape": [1, 0, -1], "flux_heads": {1: [5], 2: [5, 13]}, "delay": 4, "margin": 8}
#: E13's runs: name -> (flux quanta per line m, probe radius r or None); the first is the base composition
E13_RUNS = {"flux_only": (1, None), "probe_r24": (1, 24), "probe_r24_noflux": (0, 24), "probe_r32": (1, 32),
            "probe_r32_noflux": (0, 32), "probe_r48": (1, 48), "probe_r48_noflux": (0, 48), "probe_r96": (1, 96),
            "probe_r96_noflux": (0, 96), "probe_r48_flux2": (2, 48), "dark": (0, None)}


def e13_geometry():
    """Per probe radius r: the lines whose entry node into the plane x = r lies in |y|, |z| <= h, each with its entry
    index p (n(r) = (2 h rho / r)^2 = 36864 / r^2 for these parameters); per line its node count."""
    B = field_line_bundle_lines(E13["rho"], E13["x_root"], E13["x_end"])
    radii = {}
    for r in E13["radii"]:
        rows = {}
        for n, ln in B.items():
            p = next((i for i, s in enumerate(ln["sites"]) if s[0] == r), None)
            if p is not None and max(abs(ln["sites"][p][1]), abs(ln["sites"][p][2])) <= E13["half"]:
                rows[n] = p
        radii[r] = rows
    return {"nodes": {n: len(ln["sites"]) for n, ln in B.items()}, "radii": radii}


def _e13_packets(m, r):
    """The bundle's parametric packets of one E13 run: m outward flux quanta per line, a probe surface at x = r."""
    out = {"flux": {"f": list(E13["shape"]), "heads": list(E13["flux_heads"][m])} if m else None,
           "probe": {"f": list(E13["shape"]), "x": r, "half": E13["half"]} if r is not None else None}
    return out


def e13_horizon(geo, m, r):
    """Updates of one E13 run: the last free station arrival plus the contact delays plus a margin."""
    if r is None:
        return max(e13_horizon(geo, 2 if rr == 48 else 1, rr) for rr in E13["radii"])
    return max(p - E13["station"] for p in geo["radii"][r].values()) + E13["delay"] * max(m, 1) + E13["margin"]


def e13_spec():
    """exp.exchange_inverse_square@1 (r33 E13): medium.field_line_bundle@1 (64 lines, side 200, source at (0,100,100))
    with one outward (1,0,-1) flux quantum per line; the controls are packet masks (probes of fixed area at r = 24, 32,
    48, 96 with and without flux, a double flux, dark).  PRESCRIBED lines: the 1/r^2 is geometric exchange, not a
    field at a distance.  Equals E13's composition.json exactly (r33 e13_build.spec, ported)."""
    geo = e13_geometry()
    rho, half = E13["rho"], E13["half"]
    base = {"format": FORMAT, "id": "e13_exchange_inverse_square",
            "board": {"side": E13["side"], "background": [0, 0, 2], "coupling": {"signs": PPP, "variant": None}},
            "placements": [field_line_bundle_placement("field", E13["O"], rho, E13["x_root"], E13["x_end"], 0,
                                                       **{k: v for k, v in _e13_packets(1, None).items() if v})],
            "assertions": {},
            "timing": {"t0": 0, "declared": {
                "label": "PRESCRIBED field lines; the 1/r^2 is geometric exchange, not a field at a distance",
                "lines": f"64 open gauged staircases from O toward (2rho, 2j+1, 2k+1), rho = {rho}, from x = "
                         f"{E13['x_root']} to x = {E13['x_end']} (the +x bundle of a 384-line cube-gnomonic source)",
                "probe_surface": f"|y|, |z| <= {half} on the plane x = r (fixed area {(2 * half) ** 2})",
                "radii": list(E13["radii"]), "flux": "m outward (1,0,-1) quanta per line, heads at local nodes 5 (,13)",
                "probe": "one inward (1,0,-1) quantum on each line crossing the surface, head at its entry node",
                "station": f"local node {E13['station']} of every line"}},
            "controls": [], "steps": e13_horizon(geo, 1, None)}
    for name, (m, r) in E13_RUNS.items():
        if name != "flux_only":
            base["controls"].append({"name": name, "override": {"field": _e13_packets(m, r)}})
    return base


#: E13b's runs (r33 W2): name -> (root sources on, probe radius r or None); the first is the base composition
E13B_RUNS = {"cores_only": (True, None), "probe_r24": (True, 24), "probe_r24_nocores": (False, 24),
             "probe_r32": (True, 32), "probe_r32_nocores": (False, 32), "probe_r48": (True, 48),
             "probe_r48_nocores": (False, 48), "probe_r96": (True, 96), "probe_r96_nocores": (False, 96),
             "dark": (False, None)}
E13B = {"delay": 2, "margin": 8, "station_window_from": 8, "root_source": [-1, 0, 0]}


def e13b_spec():
    """exp.created_flux_inverse_square@1 (r33 E13b): E13's bundle with CREATED flux: no flux prepared in flight; one
    root source (single channel (-1,0,0) in the -x halo slot of every root, r33's seed.emitter_core@1) fires its root
    once after t = 0 and starts a front.  Controls are masks: the probe surfaces at r = 24 .. 96, with and without
    the root sources, and dark.  PRESCRIBED lines: the 1/r^2 is geometric exchange, not a field at a distance."""
    geo = e13_geometry()
    base = e13_spec()
    base["id"] = "e13b_created_flux_inverse_square"
    base["placements"] = [field_line_bundle_placement("field", E13["O"], E13["rho"], E13["x_root"], E13["x_end"], 0,
                                                      root_sources={"triple": list(E13B["root_source"])})]
    base["timing"]["declared"].update({
        "label": "PRESCRIBED field lines, CREATED flux: the 1/r^2 is geometric exchange, not a field at a distance",
        "flux": "none prepared: one root source per line (-x halo slot of the root) fires its root once after t = 0 "
                "and starts a front (copy-free)", "station_window_from": E13B["station_window_from"]})
    base["steps"] = max(p - E13["station"] for p in geo["radii"][96].values()) + E13B["delay"] + E13B["margin"]
    base["controls"] = []
    for name, (cores, r) in E13B_RUNS.items():
        if name != "cores_only":
            base["controls"].append({"name": name, "override": {"field": {
                "probe": _e13_packets(0, r)["probe"], "root_sources": {"triple": list(E13B["root_source"])}
                if cores else None}}})
    return base


# ---------------------------------------------------------------------------- r29 fused movers, towed / leapfrog pairs
def _mover_on_line(name, line_at, n, front, direction=1, phase=0):
    """A fused_mover@1 placement on the matter line placed at ``line_at`` (label 41 along y), wrapped on side L."""
    return {"name": name, "block": "fused_mover@1",
            "params": {"n": n, "front": front, "direction": direction, "phase": phase}, "at": list(line_at),
            "wrap": True}


def _mover_sockets(n, front, direction=1, phase=0, L=None):
    from .generators import fused_mover_window
    return sorted({i % L for i in fused_mover_window(n, front, direction, phase)})


def fused_mover_line_spec(n=1, L=30, x=4, z=4, front=10, direction=1, steps=None):
    """matter.fused_mover@1 (r29): one beta_n on a bare class-0 matter line (label 41 along y at (x, ., z), a ring of
    side L), front node ``front`` activated at t = 0.  beta_1 is r06's SLOW_LEFT glider one update after its registered
    phase (direction +1)."""
    pl = [{"name": "A", "block": "matter_line@1",
           "params": {"length": L, "sockets": _mover_sockets(n, front, direction, 0, L)}, "at": [x, 0, z],
           "wrap": True},
          _mover_on_line("beta", [x, 0, z], n, front, direction, 0)]
    out = {"format": FORMAT, "id": f"beta{n}_matter_line_L{L}", "board": _board(L, MPP), "placements": pl,
           "timing": {"t0": 0, "declared": {"speed": "1/3 (exact translator, S(t+3) = shift S(t))"}}}
    if steps is not None:
        out["steps"] = steps
    return out


R29_XA = 20


def _rail_pair_spec(sid, L, h, rungs, marks_a, marks_b, movers):
    """Two matter rails (label 41 along y) at x = 20 and 20 + h with class-2 marks, class-2 rungs (light_line@1 of label
    1 along x at y = rungs, z = 4, gauge phase 1) and fused movers: movers = [(rail, n, front, phase)]."""
    sock = {"A": set(), "B": set()}
    for rail, n, front, phase in movers:
        sock[rail].update(_mover_sockets(n, front, 1, phase, L))
    pl = []
    for rail, x, marks in (("A", R29_XA, marks_a), ("B", R29_XA + h, marks_b)):
        pl.append({"name": f"rail{rail}", "block": "matter_line@3",
                   "params": {"length": L, "sockets": sorted(sock[rail]), "marks": [[int(m) % L, 2] for m in marks]},
                   "at": [x, 0, 3], "wrap": True})
    ph = (R29_XA + 1) % 2
    for k, y in enumerate(rungs):
        pl.append({"name": f"rung{k}", "block": "light_line@1", "params": {"length": L, "gauge_phase": ph},
                   "at": [0, int(y) % L, 4], "wrap": True})
    for rail, n, front, phase in movers:
        pl.append(_mover_on_line(f"mover{rail}", [R29_XA + (h if rail == "B" else 0), 0, 3], n, front, 1, phase))
    want = {f"{x},{int(y) % L}": 2 for x in (R29_XA, R29_XA + h) for y in rungs}
    return {"format": FORMAT, "id": sid, "board": _board(L, MPP), "placements": pl,
            "assertions": {"junction_classes": want}}


def towed_pair_spec(p=12, K=8, h=8, a=6, L=480, Y0=120, yA0=80, master=True, slave=True):
    """atom.towed_pair@1 (r29 L2): master rail A (plain) and slave rail B (one class-2 advancer at y_k + a after every
    rung), K class-2 rungs at y_k = Y0 + k p; master SLOW (beta_1) from yA0, slave SLOW started ceil((h + 4) / 3) sites
    behind and phased so that it reaches rung 0 exactly h + 4 updates after the master (the braking rule)."""
    lag = -(-(h + 4) // 3)
    movers = ([("A", 1, yA0, 0)] if master else []) + ([("B", 1, yA0 - lag, 3 * lag - (h + 4))] if slave else [])
    rungs = [Y0 + k * p for k in range(K)]
    tag = "pair" if master and slave else "master_alone" if master else "slave_alone"
    return _rail_pair_spec(f"tow_{tag}_p{p}_h{h}_K{K}_L{L}", L, h, rungs, [], [y + a for y in rungs], movers)


def leapfrog_pair_spec(h=4, p=30, K=8, L=960, Y0=120, yA0=80, gap=3, A=True, B=True):
    """atom.leapfrog_pair@1 (r29 L4): rails A and B (h apart), class-2 rungs at y_k = Y0 + k p; (2h + 12) / 4
    advancers (gap 3, from 6 sites after the rung) after every even rung on rail B and after every odd rung on rail A;
    gliders on both rails phased as in the towed pair.  The bound pair moves at 15/41 (UPDATE 17), slower than either
    glider alone (3/8)."""
    n_adv = (2 * h + 12) // 4
    if 4 * n_adv != 2 * h + 12:
        raise ValueError("h must make (2h + 12) / 4 an integer")
    marks = {"A": [], "B": []}
    for k in range(K):
        sites = [Y0 + k * p + 6 + gap * i for i in range(n_adv)]
        if sites[-1] > Y0 + (k + 1) * p - 6:
            raise ValueError("pitch too short for the advancers")
        marks["B" if k % 2 == 0 else "A"] += sites
    lag = -(-(h + 4) // 3)
    movers = ([("A", 1, yA0, 0)] if A else []) + ([("B", 1, yA0 - lag, 3 * lag - (h + 4))] if B else [])
    tag = "pair" if A and B else "A_alone" if A else "B_alone"
    return _rail_pair_spec(f"leapfrog_{tag}_p{p}_h{h}_K{K}_L{L}", L, h, [Y0 + k * p for k in range(K)], marks["A"],
                           marks["B"], movers)


# ---------------------------------------------------------------------------- r20 X-gates, cavity, escorted junction
def split_guide_path(c, name, start, g0, dirs, gaps=(), sigma0=1):
    """A guide path cut at its ``gaps`` (node indices left at the vacuum: r20's X-gate, a vacuum node shared by two
    fibres).  Returns (pieces, where): the pieces as guide_net@1 path specs, each carrying the gauge continued through
    the gaps, and node index -> (piece name, index in the piece).  An interior gap needs the cut because guide_net@1
    writes every node of a path at rest."""
    dirs = [int(d) for d in dirs]
    nodes = G.channel_path(c, tuple(start), int(g0), dirs, None, sigma0=int(sigma0))
    gaps, runs, cur = set(gaps), [], []
    for i in range(len(nodes)):
        if i in gaps:
            if cur:
                runs.append(cur)
            cur = []
        else:
            cur.append(i)
    if cur:
        runs.append(cur)
    pieces, where = [], {}
    for k, idx in enumerate(runs):
        pname = f"{name}{k}" if len(runs) > 1 else name
        s, g, sg = nodes[idx[0]]
        pieces.append({"name": pname, "start": list(s), "g0": g, "sigma0": sg,
                       "dirs": _run_length(dirs[idx[0]:idx[-1]]) or [[0, 0]]})
        where.update({i: (pname, j) for j, i in enumerate(idx)})
    return pieces, where


def path_through(name, site, g, d, n_before, n_after, sigma=1, signs=PPP):
    """The path spec {name, start, g0, sigma0, dirs} of the r04 channel path that passes channel g at ``site`` with
    gauge ``sigma`` while moving along direction d, n_before nodes before the site and n_after after it."""
    c = Coupling(tuple(signs))
    back = G.channel_path(c, tuple(site), int(g), [int(d) ^ 1] * int(n_before), None, sigma0=int(sigma))
    s0, g0, sg0 = back[-1]
    nodes = G.channel_path(c, s0, g0, [int(d)] * (int(n_before) + int(n_after)), None, sigma0=sg0)
    if nodes[int(n_before)] != (tuple(site), int(g), int(sigma)) or nodes[:int(n_before)] != list(reversed(back[1:])):
        raise ValueError("the channel path is not reciprocal through the site")
    return {"name": name, "start": list(s0), "g0": g0, "sigma0": sg0, "dirs": [[int(d), int(n_before) + int(n_after)]]}


def gapped_guide_placement(name, at, paths, gaps=(), packets=(), signs=PPP, wrap=False):
    """gate.x_gate@1 hardware in guide_net@1 form: guide ``paths`` ({name, start, g0, sigma0?, dirs}, run-length, local
    coordinates) whose nodes on the ``gaps`` (local sites [x, y, z]: every path node there; or addresses
    [x, y, z, g]: that channel only) are left at the vacuum (0,0,2), every path being cut there with its gauge
    continued.  ``packets`` [{path, f, lead}] move forward on the FULL paths (lead = the head's node index on the full
    path at t = 0) and are written on the piece that holds them; a packet must not reach a gap by t = 0."""
    c = Coupling(tuple(signs))
    gap_sites = {tuple(int(v) for v in g) for g in gaps if len(g) == 3}
    gap_addr = {tuple(int(v) for v in g) for g in gaps if len(g) == 4}
    out, where = [], {}
    for p in paths:
        dirs = G.expand_dirs(p["dirs"])
        nodes = G.channel_path(c, tuple(p.get("start", (0, 0, 0))), int(p["g0"]), dirs, None,
                               sigma0=int(p.get("sigma0", 1)))
        gi = [i for i, n in enumerate(nodes) if n[0] in gap_sites or (*n[0], n[1]) in gap_addr]
        pieces, wh = split_guide_path(c, p["name"], p.get("start", (0, 0, 0)), p["g0"], dirs, gi, p.get("sigma0", 1))
        out += pieces
        where[p["name"]] = (wh, len(nodes))
    pk = []
    for q in packets:
        wh, n = where[q["path"]]
        head, f = int(q["lead"]), list(q["f"])
        span = [i for i in range(head - len(f) - 1, head + 1) if 0 <= i < n]
        if head not in wh or len({wh.get(i, (None,))[0] for i in span}) != 1:
            raise ValueError(f"packet on {q['path']} at node {head} touches a gap at t = 0")
        piece, j = wh[head]
        pk.append({"path": piece, "f": f, "lead": j})
    return {"name": name, "block": "guide_net@1", "params": {"paths": out, "packets": pk}, "at": list(at),
            "wrap": bool(wrap)}


def x_gate_spec(data=True, delta=None, L=64, n=30, t_D=20, f=(1, 0, -1)):
    """gate.x_gate@1 (r20): the vacuum gap X at (L/2, L/2, L/2) shared by a channel-0 x-line and the r04 y-path through
    X (n nodes before X on each, n - 1 after; +++).  A lone head is mirrored; two heads reaching X in the same update
    (Delta = 0) both pass.  data: the x-line head reaches X at t_D; delta: the y-line head at t_D + delta."""
    C = L // 2
    paths = [{"name": "X", "start": [-n, 0, 0], "g0": 0, "dirs": [[0, 2 * n - 1]]},
             path_through("Y", (0, 0, 0), 0, 2, n, n - 1)]
    pk = ([{"path": "X", "f": list(f), "lead": n - t_D}] if data else []) + \
         ([{"path": "Y", "f": list(f), "lead": n - (t_D + delta)}] if delta is not None else [])
    return {"format": FORMAT, "id": f"xgate_d{int(data)}_delta{delta}", "board": _board(L, PPP),
            "placements": [gapped_guide_placement("xg", (C, C, C), paths, [[0, 0, 0]], pk)],
            "timing": {"t0": 0, "declared": {"t_data_at_X": t_D if data else None,
                                              "t_control_at_X": None if delta is None else t_D + delta}}}


def x_cavity_spec(data=True, escorts_1=(), escort_2=None, L=200, gates=(94, 106), t_D=20, f=(1, 0, -1)):
    """store.x_cavity@1 (r20): two X-gates ``gates`` (x positions) on one channel-0 x-line (x = 2 .. L - 3, +++), each
    with its own y-line (98 nodes below, 97 above); the cavity between them stores a quantum that arrives with an
    escort (Delta = 0 at gate 1) and releases it on a later escort at gate 2.  data: head at gate 1 at t_D; escorts_1:
    escort heads at gate 1; escort_2: an escort head at gate 2 (the release)."""
    C = L // 2
    paths = [{"name": "X", "start": [2, C, C], "g0": 0, "dirs": [[0, L - 5]]}]
    for k, x in enumerate(gates):
        paths.append(path_through(f"Y{k + 1}", (x, C, C), 0, 2, 98, 97))
    i1 = gates[0] - 2
    pk = [{"path": "X", "f": list(f), "lead": i1 - t_D}] if data else []
    pk += [{"path": "Y1", "f": list(f), "lead": 98 - int(t)} for t in escorts_1]
    if escort_2 is not None:
        pk.append({"path": "Y2", "f": list(f), "lead": 98 - int(escort_2)})
    return {"format": FORMAT, "id": "x_cavity", "board": _board(L, PPP),
            "placements": [gapped_guide_placement("cav", (0, 0, 0), paths, [[x, C, C] for x in gates], pk)],
            "timing": {"t0": 0, "declared": {"t_data_at_gate1": t_D if data else None, "escorts_gate1": list(escorts_1),
                                              "escort_gate2": escort_2}}}


def escort_pair_router_placement(name, at, M=48, half=45, t_X=None, escort_B=None, escort_C=None, f=(1, 0, -1),
                                 signs=PPP):
    """select.escorted_junction@1 (r20) / select.escort_pair_router@1 (r15b), the junction node X at ``at`` (+++):
    input A along +x (M - 1 nodes ending at X); output B along +x and output C along +y; the doors B1 = X + x and
    C1 = X + y are X-gates, each an interior node of a private escort line along z (half + 1 nodes below, half above).
    Packets of shape f: the data head reaches X at ``t_X``; escort heads reach doors B1 / C1 at ``escort_B`` /
    ``escort_C`` (None = absent).  One escort with Delta = 0 at its door routes the quantum into that output; the pair
    from one clock, staggered by 2, lets the data phase pick the door (r15b)."""
    c = Coupling(tuple(signs))
    ab = G.channel_path(c, (2 - M, 0, 0), 0, [0] * (2 * M - 5), None)
    cy = G.channel_path(c, (0, 0, 0), ab[M - 2][1], [2] * half, None)
    paths = [{"name": "A", "start": [2 - M, 0, 0], "g0": 0, "dirs": [[0, 2 * M - 5]]},
             {"name": "C", "start": [0, 1, 0], "g0": cy[1][1], "sigma0": cy[1][2], "dirs": [[2, half - 1]]}]
    for nm, (s, g, sg) in (("B", ab[M - 1]), ("C", cy[1])):
        paths.append(path_through("e" + nm, s, g, 4, half + 1, half, sg, signs))
    pk = [{"path": "A", "f": list(f), "lead": M - 2 - int(t_X)}] if t_X is not None else []
    for nm, t in (("B", escort_B), ("C", escort_C)):
        if t is not None:
            pk.append({"path": "e" + nm, "f": list(f), "lead": half + 1 - int(t)})
    return gapped_guide_placement(name, at, paths, [list(ab[M - 1][0]), list(cy[1][0])], pk, signs)


def escort_pair_router_spec(stagger="S0", lam=0, L=96, M=48, half=45, t_X0=24, t_e0=25, steps=80):
    """r15b XR1 boards: the escort pair from one clock, staggered by 2 (S0: B at t_e0, C at t_e0 + 2; S1 swapped);
    the data head reaches X at t_X0 + 2 lam (its phase class lam picks the door with Delta = 0)."""
    eB, eC = (t_e0, t_e0 + 2) if stagger == "S0" else (t_e0 + 2, t_e0)
    return {"format": FORMAT, "id": f"xr1_{stagger}_lam{lam}", "board": _board(L, PPP),
            "placements": [escort_pair_router_placement("xr", (M, M, M), M, half, t_X0 + 2 * lam, eB, eC)],
            "timing": {"t0": 0, "declared": {"t_X": t_X0 + 2 * lam, "escort_B": eB, "escort_C": eC}}, "steps": steps}


def escorted_junction_spec(door="B", L=96, M=48, t_X=24, steps=70):
    """r20's escorted junction (xrouter I1 / I2): one escort, head at its door one update after the data head reaches
    X (Delta = 0 at the door), routes the quantum into that output."""
    kw = {"escort_B": t_X + 1} if door == "B" else {"escort_C": t_X + 1}
    return {"format": FORMAT, "id": f"xrouter_escort_{door}", "board": _board(L, PPP),
            "placements": [escort_pair_router_placement("xr", (M, M, M), M, 45, t_X, **kw)],
            "timing": {"t0": 0, "declared": {"t_X": t_X, "escort_at_door": t_X + 1, "door": door}}, "steps": steps}


# ---------------------------------------------------------------------------- r15b conserving router (gated halo cores)
#: r15's halo-core register: orbit phase s holds ORB[s] (the (1,0,4) core run s updates); at phases 2, 3 the nodes it
#: shares sit at r = 2, the vacuum value (history-consistent gating), i.e. they are gap nodes of their guides.
CORE_ORBIT = ([1, 0, 4], [0, -1, 4], [-1, 0, 4], [0, 1, 4])


def conserving_router_spec(lam=0, variant="R1", quantum=True, approval=True, pre=True, partner=True, store=True,
                           selectors=True, L=300, X0=10, XJ=110, nA=180, nB=140, KE=13, d=8, TJ0=24, T_A=29,
                           side_half=140, sb_half=110, dt_pre=-6, dt_partner=6, steps=180):
    """router.conserving@1 (r15b R1 / R2; store.set_entrance@1 + selectors), +++, plane z = L/2: r13's device (input
    channel-0 line to the junction XJ, arm A along +x, arm B the r04 branch along +y); side-port entrance registers
    E_A (+z halo of arm-A path KE, shared with side line S_A, channel 35 along z) and E_B (+x halo of arm-B path KE,
    shared with S_B, channel 12 along x); selector registers D_A (+z halo of arm-A path KD = KE + d, shared with the
    approval line AP) and D_B (-z halo of arm-B path KD).  Pulses (unit packets (1,0,-1)): the quantum at the junction
    at t_J = TJ0 + 2 lam, the approval at D_A's side node at T_A, a SET pulse at t_c - 6 and (R1) a partner at t_c + 6
    on each side line (t_c = t_J + KE).  R2: side lines end 4 sites beyond their side node, E_B phase-shifted by 2, no
    partner.  Registers are halo cores at orbit phases (E: -(t_c0 + dt_pre), D: -(TJ0 + KD), mod 4); at phases 2, 3
    their nodes are gap nodes (gapped_guide_placement)."""
    if variant not in ("R1", "R2"):
        raise ValueError("variant is 'R1' or 'R2'")
    stub, e_off = (None, 0) if variant == "R1" else (4, 2)
    partner = partner and variant == "R1"
    c = Coupling(PPP)
    cz, iJ, KD = L // 2, XJ - X0, KE + d
    main = G.channel_path(c, (X0, cz, cz), 0, [0] * (iJ + nA), None)
    sJ, gJ, sJg = main[iJ]
    arm_b = G.channel_path(c, G.add(sJ, 2), c.ports[2][gJ], [2] * (nB - 1), None, sigma0=sJg * c.weights[2][gJ])
    arm_a = main[iJ + 1:]
    zlo = cz + 1 - side_half
    lens = (2 * side_half if stub is None else side_half + stub, 2 * sb_half if stub is None else sb_half + stub)
    paths = [{"name": "main", "start": [X0, cz, cz], "g0": 0, "dirs": [[0, iJ + nA]]},
             {"name": "armB", "start": list(arm_b[0][0]), "g0": arm_b[0][1], "sigma0": arm_b[0][2],
              "dirs": [[2, nB - 1]]},
             {"name": "SA", "start": [XJ + KE + 1, cz, zlo], "g0": 35, "dirs": [[4, lens[0]]]},
             {"name": "AP", "start": [XJ + KD + 1, cz, zlo], "g0": 35, "dirs": [[4, 2 * side_half]]},
             {"name": "SB", "start": [XJ + 1 - sb_half, cz + KE, cz - 1], "g0": 12, "dirs": [[0, lens[1]]]}]
    nodes = {p["name"]: G.channel_path(c, tuple(p["start"]), p["g0"], G.expand_dirs(p["dirs"]), None,
                                       sigma0=p.get("sigma0", 1)) for p in paths}
    S_E, S_D = (-(TJ0 + KE + dt_pre)) % 4, (-(TJ0 + KD)) % 4
    if (T_A + S_D) % 4:
        raise ValueError("the approval must reach D_A at a transmit time")
    regs = []                         # (name, arm node, halo direction, side node or None, side feed direction, phase)
    if store:
        regs += [("EA", arm_a[KE - 1], 4, nodes["SA"][side_half], 1, S_E),
                 ("EB", arm_b[KE - 1], 0, nodes["SB"][sb_half], 4, S_E + e_off)]
    if selectors:
        regs += [("DA", arm_a[KD - 1], 4, nodes["AP"][side_half], 1, S_D), ("DB", arm_b[KD - 1], 5, None, None, S_D)]
    gaps, cores = [], []
    for nm, (s, g, sg), dd, side, ds, ph in regs:
        core = (*G.add(s, dd), c.ports[dd][g])
        if sg != 1 or c.weights[dd][g] != 1:
            raise ValueError("a halo core needs a node of gauge +1 and a port of weight +1")
        if side is not None and (*G.add(side[0], ds), c.ports[ds][side[1]]) != core:
            raise ValueError(f"{nm}: the side node does not feed the core")
        if ph % 4 in (2, 3):
            gaps += [[*s, g]] + ([[*side[0], side[1]]] if side is not None else [])
        cores.append({"name": nm, "block": "slot_clock@1", "params": {"state": CORE_ORBIT[ph % 4], "node_label": g,
                                                                       "slot_direction": dd}, "at": list(s)})
    tJ = TJ0 + 2 * lam
    tc = tJ + KE
    pk = [{"path": "main", "f": list(F), "lead": iJ - tJ}] if quantum else []
    if approval:
        pk.append({"path": "AP", "f": list(F), "lead": side_half - T_A})
    for nm, j in (("SA", side_half), ("SB", sb_half)):
        if pre:
            pk.append({"path": nm, "f": list(F), "lead": j - (tc + dt_pre)})
        if partner:
            pk.append({"path": nm, "f": list(F), "lead": j - (tc + dt_partner)})
    pl = [gapped_guide_placement("dev", (0, 0, 0), paths, gaps, pk)] + cores
    return {"format": FORMAT, "id": f"r15b_{variant}_lam{lam}", "board": _board(L, PPP), "placements": pl,
            "timing": {"t0": 0, "declared": {"t_J": tJ, "t_c": tc, "t_A": T_A, "E_phase": S_E, "D_phase": S_D}},
            "steps": steps}


def side_port(c, node, d, d2):
    """The side port of a guide node (s, g, sigma): its halo channel h in direction d, shared with the node of a
    straight side line at site s + e_d + e_d2 that feeds h back through the direction opposite to d2.  Returns
    (h address, side node (site, channel))."""
    s, g, _ = node
    sh, h = G.add(s, d), c.ports[d][g]
    inv = [x for x in range(48) if c.ports[int(d2) ^ 1][x] == h]
    if len(inv) != 1:
        raise ValueError("no unique side channel")
    return (*sh, h), (G.add(sh, d2), inv[0])


def conserving_pair_router_spec(lam=0, q1=True, approval=True, side=True, release=True, q2=True, store=True, L=300,
                                X0=10, XJ=160, nA=130, nB=130, KE=12, d=8, TJ0=24, T_A=28, half=140, stub=4, hold=4,
                                dt_pre=-6, cross=4, pair2=None, steps=220):
    """router.conserving_pair@1 (r15b R3): the R2 router with both entrances on +z side ports (E_B's side line is the
    z-line through the +x neighbour of its halo site), KE + d even; the unselected copy is held between E_X and D_X
    for ``hold`` rounds of 2 d + 4, released by one more lambda-locked side pulse per side line at t_f = t_rel - 6
    (``cross`` updates earlier when the SET pulse is also there), and merged at the junction with a second quantum Q2
    arriving at t_m = t_rel + KE (the K-merge sends one packet into the selected arm).  ``pair2`` = (lam3, gap): a
    second pair through the same router (r15b R3-2), its pulses shifted by gap + 2 (lam3 - lam), no approval, its side
    pulses launched 8 (SET) and 12 (release) updates early (each crosses returning pulses, 4 per crossing)."""
    if (KE + d) % 2 or d % 2:
        raise ValueError("KE + d and d must be even")
    c = Coupling(PPP)
    cz, iJ, KD = L // 2, XJ - X0, KE + d
    main = G.channel_path(c, (X0, cz, cz), 0, [0] * (iJ + nA), None)
    sJ, gJ, sJg = main[iJ]
    arm_b = G.channel_path(c, G.add(sJ, 2), c.ports[2][gJ], [2] * (nB - 1), None, sigma0=sJg * c.weights[2][gJ])
    arm_a = main[iJ + 1:]
    z0 = cz + 1 - half
    _, (bs, bg) = side_port(c, arm_b[KE - 1], 4, 0)
    paths = [{"name": "main", "start": [X0, cz, cz], "g0": 0, "dirs": [[0, iJ + nA]]},
             {"name": "armB", "start": list(arm_b[0][0]), "g0": arm_b[0][1], "sigma0": arm_b[0][2],
              "dirs": [[2, nB - 1]]},
             {"name": "SA", "start": [XJ + KE + 1, cz, z0], "g0": 35, "dirs": [[4, half + stub]]},
             {"name": "AP", "start": [XJ + KD + 1, cz, z0], "g0": 35, "dirs": [[4, 2 * half]]},
             {"name": "SB", "start": [bs[0], bs[1], bs[2] - half], "g0": bg, "dirs": [[4, half + stub]]}]
    nodes = {p["name"]: G.channel_path(c, tuple(p["start"]), p["g0"], G.expand_dirs(p["dirs"]), None,
                                       sigma0=p.get("sigma0", 1)) for p in paths}
    if nodes["SB"][half][:2] != (bs, bg):
        raise ValueError("the side line of E_B is not straight along z")
    S_E, S_D = (-(TJ0 + KE + dt_pre)) % 4, (-(TJ0 + KD)) % 4
    if (T_A + S_D) % 4:
        raise ValueError("the approval must reach D_A at a transmit time")
    regs = ([("EA", arm_a[KE - 1], nodes["SA"][half], S_E), ("EB", arm_b[KE - 1], nodes["SB"][half], S_E + 2)]
            if store else []) + [("DA", arm_a[KD - 1], nodes["AP"][half], S_D)]
    gaps, cores = [], []
    for nm, (s, g, sg), side_node, ph in regs:
        core = (*G.add(s, 4), c.ports[4][g])
        if (*G.add(side_node[0], 1), c.ports[1][side_node[1]]) != core or sg != 1 or c.weights[4][g] != 1:
            raise ValueError(f"{nm}: not a shared +z halo core")
        if ph % 4 in (2, 3):
            gaps += [[*s, g], [*side_node[0], side_node[1]]]
        cores.append({"name": nm, "block": "slot_clock@1", "params": {"state": CORE_ORBIT[ph % 4], "node_label": g,
                                                                       "slot_direction": 4}, "at": list(s)})
    s, g, _ = arm_b[KD - 1]
    if S_D % 4 in (2, 3):
        gaps.append([*s, g])
    cores.append({"name": "DB", "block": "slot_clock@1", "params": {"state": CORE_ORBIT[S_D % 4], "node_label": g,
                                                                     "slot_direction": 5}, "at": list(s)})
    tJ = TJ0 + 2 * lam
    tc = tJ + KE
    t_rel = tc + 2 * d + 2 + (2 * d + 4) * hold
    t_f, t_m = t_rel - 6, t_rel + KE
    pk = ([{"path": "main", "f": list(F), "lead": iJ - tJ}] if q1 else []) + \
         ([{"path": "main", "f": list(F), "lead": iJ - t_m}] if q2 else []) + \
         ([{"path": "AP", "f": list(F), "lead": half - T_A}] if approval else [])
    for nm in ("SA", "SB"):
        if side:
            pk.append({"path": nm, "f": list(F), "lead": half - (tc + dt_pre)})
        if release:
            pk.append({"path": nm, "f": list(F), "lead": half - (t_f - (cross if side else 0))})
    if pair2 is not None:
        shift = int(pair2[1]) + 2 * (int(pair2[0]) - lam)
        pk += [{"path": "main", "f": list(F), "lead": iJ - (tJ + shift)},
               {"path": "main", "f": list(F), "lead": iJ - (t_m + shift)}]
        for nm in ("SA", "SB"):
            pk += [{"path": nm, "f": list(F), "lead": half - (tc + dt_pre + shift - 8)},
                   {"path": nm, "f": list(F), "lead": half - (t_f + shift - 12)}]
    pl = [gapped_guide_placement("dev", (0, 0, 0), paths, gaps, pk)] + cores
    return {"format": FORMAT, "id": f"r15b_R3_lam{lam}" + (f"_pair2_lam{pair2[0]}" if pair2 else ""),
            "board": _board(L, PPP), "placements": pl,
            "timing": {"t0": 0, "declared": {"t_J1": tJ, "t_c1": tc, "t_rel": t_rel, "t_f": t_f, "t_m": t_m,
                                              "t_A": T_A, "E_phase": S_E, "D_phase": S_D}}, "steps": steps}


# ---------------------------------------------------------------------------- r36b C3b / G1: gravity inside the cycle
#: r36b's parts: a lap ({"lap": runs} or a rectangle in the x-y plane), its start channel and laps per closed path
R36B_RINGS = {"lamp": {"n1": 4, "n2": 8, "g0": 0, "turns": 1}, "clock": {"n1": 2, "n2": 4, "g0": 2, "turns": 1},
              "spin": {"lap": [[0, 2], [2, 2], [4, 10], [1, 2], [3, 2], [5, 10]], "g0": 0, "turns": 2}}
R36B_AT = {"lamp": (40, 150, 40), "clock": (24, 150, 70), "free": (50, 150, 42), "spin": (200, 200, 100)}
R36B_LEADS = {"lamp": (3, 14), "clock": (3, 6), "spin": (3, 46)}        # packets on 'R' and '~R'
#: each part's moment patch at its own symmetric moment (its composition advanced t_m updates; JR-fixed), cells
#: [dx, dy, dz, g, a, b, r] relative to the counter node O: the head-on meeting of the counter pair on a ring (lamp,
#: clock, spin) or the reflection midpoint at a bare line end (free; c2p = seed.cyclic_point's wall form at gauge phase 1)
R36B_MOMENTS = {
    "lamp": {"t_m": 6, "O": (44, 152, 40), "cells": [
        [-1, 0, 0, 6, 0, 0, 4], [0, -1, 0, 2, 0, 0, 2], [0, 0, -1, 30, 0, 0, 0], [0, 0, 0, 6, -1, 1, 4],
        [0, 0, 1, 44, 0, 0, 0], [0, 1, 0, 13, 0, 0, 2], [1, 0, 0, 6, 0, 0, 4]]},
    "clock": {"t_m": 4, "O": (26, 152, 70), "cells": [
        [-1, 0, 0, 18, 0, 0, 0], [0, -1, 0, 33, 0, 0, 2], [0, 0, -1, 27, 0, 0, 4], [0, 0, 0, 27, -1, 1, 4],
        [0, 0, 1, 27, 0, 0, 4], [0, 1, 0, 17, 0, 0, 2], [1, 0, 0, 41, 0, 0, 0]]},
    "free": {"t_m": 11, "O": (50, 150, 198), "cells": [
        [-1, 0, 0, 34, 0, 0, 4], [0, -1, 0, 0, 0, 0, 4], [0, 0, -1, 2, 0, 0, 2], [0, 0, 0, 2, 1, -1, 0],
        [0, 0, 1, 2, 0, 0, 0], [0, 1, 0, 6, 0, 0, 4], [1, 0, 0, 15, 0, 0, 4]]},
    "spin": {"t_m": 6, "O": (202, 202, 102), "cells": [
        [-1, 0, 0, 3, 0, 0, 4], [0, -1, 0, 8, 0, 0, 0], [0, 0, -1, 44, 0, 0, 2], [0, 0, 0, 3, -1, 1, 4],
        [0, 0, 1, 29, 0, 0, 2], [0, 1, 0, 11, 0, 0, 0], [1, 0, 0, 3, 0, 0, 4]]},
    "c2p": {"t_m": 12, "O": (4, 40, 4), "cells": [
        [-1, 0, 0, 1, 0, 0, 4], [0, -1, 0, 35, 0, 0, 0], [0, 0, -1, 41, 0, 0, 0], [0, 0, 0, 1, -1, 1, 4],
        [0, 0, 1, 4, 0, 0, 0], [0, 1, 0, 22, 0, 0, 0], [1, 0, 0, 1, 0, 0, 2]]}}
R36B_FREE_N = 157


def _closed_runs(ring):
    lap = ring.get("lap") or [[0, ring["n1"]], [2, ring["n2"]], [1, ring["n1"]], [3, ring["n2"]]]
    runs = [list(r) for _ in range(int(ring.get("turns", 1))) for r in lap]
    runs[-1][1] -= 1
    return [r for r in runs if r[1] > 0]


def counter_ring_placement(name, at, ring, leads=(), back_leads=(), tap=None, gaps=None, signs=MPP):
    """clock.counter_ring@1 / clock.counter_lamp@1 / spin.box_loop_z@1 (r36b): one closed guide_net@1 path 'R' (the
    ring's laps) carrying packets (1,-1) on 'R' (leads) and '~R' (back_leads), with an optional bare-ended tap
    {node, exit, length} (r04 B13, degree 3).  ``gaps`` (local addresses) instead writes the dark ring (no packets) with
    those nodes left for a moment patch (gapped_guide_placement)."""
    if gaps is None:
        paths = [{"name": "R", "g0": ring["g0"], "dirs": _closed_runs(ring)}]
        if tap:
            paths.append({"name": "T", "branch_of": "R", "at_node": tap["node"], "dir": tap["exit"],
                          "length": tap["length"]})
        pk = [{"path": "R", "f": [1, -1], "lead": int(v)} for v in leads]
        pk += [{"path": "~R", "f": [1, -1], "lead": int(v)} for v in back_leads]
        return {"name": name, "block": "guide_net@1", "params": {"paths": paths, "packets": pk, "closed": ["R"]},
                "at": list(at), "wrap": True}
    c = Coupling(tuple(signs))
    paths = [{"name": "R", "start": [0, 0, 0], "g0": ring["g0"], "dirs": _closed_runs(ring)}]
    if tap:
        s, g, sg = G.channel_path(c, (0, 0, 0), ring["g0"], G.expand_dirs(_closed_runs(ring)), None)[tap["node"]]
        d = int(tap["exit"])
        paths.append({"name": "T", "start": list(G.add(s, d)), "g0": c.ports[d][g], "sigma0": sg * c.weights[d][g],
                      "dirs": [[d, int(tap["length"]) - 1]]})
    return {**gapped_guide_placement(name, at, paths, [[*(int(v) for v in k)] for k in gaps], (), signs), "wrap": True}


def _moment_patch(part, name=None):
    m = R36B_MOMENTS[part]
    return {"name": name or f"moment_{part}", "block": "literal_patch@1",
            "params": {"kind": "fibre-packet", "cells": [list(c) for c in m["cells"]]}, "at": list(m["O"]), "wrap": True}


def _gaps_rel(part):
    """The moment patch's cells that sit on the part's own guide nodes, relative to the part's placement."""
    m, at = R36B_MOMENTS[part], R36B_AT[part]
    return [(m["O"][0] + c[0] - at[0], m["O"][1] + c[1] - at[1], m["O"][2] + c[2] - at[2], c[3]) for c in m["cells"]
            if c[6] == 2 or (c[4], c[5]) != (0, 0)]


def cyclic_gravity_spec(L=256, universe="g1", dark=False, oneway=False, D=60, steps=960):
    """exp.cyclic_gravity@1 (r36b G1: lamp + clock + free light) and exp.cyclic_universe_c3b@1 (r36b C3b: C2' + spin
    box loop + G1), period 320 (T = 160), coupling (-,+,+).  The seed is ONE composition: the dark parts (rings with
    the nodes of their moment patch left open, light lines with sockets there) plus each part's moment patch.
    ``dark``: hardware only (K1); ``oneway``: the lamp's back packet removed (K2: one packet at lead 3 + 6, not a
    moment); ``D``: the lamp's tap length (240 on L = 512: the probe-removed K3)."""
    parts = {"g1": ("lamp", "clock", "free"), "c3b": ("c2p", "spin", "lamp", "clock", "free")}[universe]
    pl = []
    for part in parts:
        if part == "c2p":
            pl.append({"name": "B", "block": "light_line_s@1",
                       "params": {"length": 152, "gauge_phase": 1, "sockets": [] if dark else [0, 1]},
                       "at": [4, 40, 4], "wrap": False})
            pl.append({"name": "A", "block": "matter_line@1", "params": {"length": 53, "sockets": []}, "at": [79, 14, 3],
                       "wrap": False})
        elif part == "free":
            pl.append({"name": "free", "block": "light_line_s@1",
                       "params": {"length": R36B_FREE_N, "label": 2, "axis": "z", "gauge_phase": 0,
                                  "sockets": [] if dark else [R36B_FREE_N - 2, R36B_FREE_N - 1]},
                       "at": list(R36B_AT["free"]), "wrap": False})
        else:
            tap = {"node": 0, "exit": 4, "length": D} if part == "lamp" else None
            if dark:
                pl.append(counter_ring_placement(part, R36B_AT[part], R36B_RINGS[part], tap=tap))
            elif part == "lamp" and oneway:
                pl.append(counter_ring_placement(part, R36B_AT[part], R36B_RINGS[part], (R36B_LEADS[part][0] + 6,),
                                                 tap=tap))
            else:
                pl.append(counter_ring_placement(part, R36B_AT[part], R36B_RINGS[part], tap=tap, gaps=_gaps_rel(part)))
        if not dark and not (part == "lamp" and oneway):
            pl.append(_moment_patch(part))
    tag = "dark" if dark else "oneway" if oneway else f"D{D}" if D != 60 else "seed"
    return {"format": FORMAT, "id": f"{universe}_{tag}_L{L}", "board": _board(L, MPP), "placements": pl,
            "timing": {"t0": "integer moment (JR S = S)" if not (dark or oneway) else 0,
                       "declared": {"period": 320, "moments": "160Z", "parts_t_m": {p: R36B_MOMENTS[p]["t_m"]
                                                                                    for p in parts}}},
            "steps": steps}


def r36b_part_spec(part, L=256, D=60, back=True, at=None):
    """One r36b part as its own incoming composition (r36b compositions/r36b_*.json); its moment is t_m updates later
    (R36B_MOMENTS).  The calibration clocks are part 'clock' at (20, L/2, 20) with back=False (one packet) or True."""
    if part == "free":
        n = R36B_FREE_N
        front = n - 1 - 8
        pl = [{"name": "free", "block": "light_line_s@1",
               "params": {"length": n, "label": 2, "axis": "z", "gauge_phase": 0, "sockets": [front - 2, front - 1, front]},
               "at": list(R36B_AT["free"]), "wrap": False},
              {"name": "free_packet", "block": "fibre_packet@1",
               "params": {"front": front, "direction": 1, "label": 2, "axis": "z", "gauge_phase": 0},
               "at": list(R36B_AT["free"]), "wrap": False}]
        return {"format": FORMAT, "id": "r36b_free", "board": _board(L, MPP), "placements": pl}
    leads = R36B_LEADS[part]
    tap = {"node": 0, "exit": 4, "length": D} if part == "lamp" else None
    pl = [counter_ring_placement(part, at or R36B_AT[part], R36B_RINGS[part], leads[:1], leads[1:] if back else (),
                                 tap=tap)]
    return {"format": FORMAT, "id": f"r36b_{part}" + (f"_D{D}" if part == "lamp" else ""), "board": _board(L, MPP),
            "placements": pl}
