"""Reference compositions: r11's D1 module written as placements of registered blocks (r21).

``d1_main_spec(100)`` regenerates the published block ``d1_local_atom_L100``,
``d1_main_spec(200, tiles=2)`` regenerates ``d1_local_atom_L200``, its ``no_seed`` control
regenerates ``d1_control_no_seed_L100``, and ``d1_skeleton_spec(160)`` regenerates
``d1_skeleton_atom_spin_clocks_L160`` (same complete initial state and coupling).
"""
from __future__ import annotations

from .compose import FORMAT


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
    data = _registry_data("bb27_point.json")
    rel = data["cells_relative_to_O"] if star else data["seed_28_relative_to_O"]
    cells = [[(O[0] + c[0]) % L, (O[1] + c[1]) % L, O[2] + c[2], c[3], c[4], c[5], c[6]] for c in rel]
    spec = bb27_dark_spec(bb27_target_spec(variant, L))
    spec["id"] = f"{variant}_{'seedstar' if star else 'seed'}_L{L}"
    for p in spec["placements"]:
        if p["name"] == "A0":
            p["params"]["sockets"] = sorted({c[1] for c in cells if c[0] == O[0] and c[2] == O[2] and c[3] == 41})
        if p["name"] == "B0":
            p["params"]["sockets"] = sorted({c[0] for c in cells if c[1] == O[1] and c[2] == O[2] + 1 and c[3] == 1})
    spec["placements"].append({"name": "seed", "block": "literal_patch@1", "params": {"kind": "glider-seed",
                                                                                   "cells": cells},
                               "at": [0, 0, 0], "wrap": True})
    spec["timing"] = {"t0": 0, "declared": {"target_at": _BB27_T[variant] + (4 if star else 0)}}
    return spec
