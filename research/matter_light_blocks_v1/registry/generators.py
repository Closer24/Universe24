"""Registered parametric blocks: data generators only (they return ``research.components`` Patches).

Ported from the program registrar's ``compose_v1`` (r21) so that compositions can be regenerated
from tracked code. Each generator writes initial triples once and checks its structural
precondition against the fixed reference coupling; nothing here evolves a state. A generator
id carries a version (``matter_line@1``); a changed generator gets a new version.

The two pieces of researcher data the generators need are embedded below or in ``data/``:
* the slow-glider profile of r06 (``demo.SLOW``/``SLOW_LEFT``, and the history halo S0 that r06's
  ``glider.halo_and_passage`` gives for both: the single value S0 = 1 one site behind the window);
* r04's wave-6 holonomy-z ring fragment (28 cells relative to the junction node J).
"""
from __future__ import annotations

import json
from pathlib import Path

from universe24 import Channel, Coupling
from universe24.core.group_2o import DIRECTIONS, group
from research.components import Patch, Socket, TensorSpec

DATA = Path(__file__).resolve().parent / "data"
AXES = {"x": 0, "y": 1, "z": 2}
#: The eight silent states of a slot clock, by the class of its node (r06 recomb.SILENT; r04 dark clock).
SILENT = {0: [(-1, 0, 4), (0, 1, 4), (0, 1, 0), (-1, 0, 0)],
          2: [(0, -1, 4), (1, 0, 4), (1, 0, 0), (0, -1, 0)]}
#: r06 slow gliders: 3-site window (a, b, c with r = 2c) and the history halo {chain offset: S0}.
GLIDERS = {"SLOW": {"W": 3, "s": -1, "a": (1, 1, 0), "b": (0, -1, -1), "c": (2, 0, 2), "halo": {1: 1}},
           "SLOW_LEFT": {"W": 3, "s": -1, "a": (0, 1, 1), "b": (-1, -1, 0), "c": (2, 0, 2), "halo": {1: 1}}}
LINEAGE = {
    "matter_line@1": "r11 net.py MNet.rest_cells (A-lines; r06 network convention), via r21 compose_v1",
    "light_line@1": "r11 net.py MNet.rest_cells/classB (B-lines; r04 gauge, own phase), via r21 compose_v1",
    "slot_clock@1": "r11 net.py MNet.core_key + SILENT (r06 recomb.SILENT; r04 dark clock), via r21 compose_v1",
    "slow_glider@1": "r06 crystal.glider_delta with demo.SLOW/SLOW_LEFT (profile embedded), via r21 compose_v1",
    "spin_ring_z@1": "r04 preparations/wave6_spin_module_fragment.json (data/spin_ring_z.json), via r21 compose_v1",
}


def _tensor(signs):
    return TensorSpec.from_signs(tuple(signs))


def _straight(coupling, label, axis):
    d = 2 * axis
    if coupling.ports[d][label] != label or coupling.ports[d + 1][label] != label:
        raise ValueError(f"label {label} is not self-ported along axis {axis} under {coupling.body_signs}")
    return coupling.weights[d][label]


def _node(axis, i, label):
    p = [0, 0, 0]
    p[axis] = i
    return (*p, label)


def matter_line(board, *, length, label=41, axis="y", sockets=()):
    """Straight class-0 matter fibre: ``length`` nodes of one self-ported label at rest (0,0,0).
    ``sockets``: local node indices left unassigned for a filler block of kind 'glider-seed'."""
    c = Coupling(tuple(board["signs"]))
    ax = AXES[axis]
    _straight(c, label, ax)
    cells = {_node(ax, i, label): (0, 0, 0) for i in range(length) if i not in set(sockets)}
    sk = (Socket("seed-window", tuple(_node(ax, i, label) for i in sockets), ("glider-seed",)),) if sockets else ()
    return Patch("matter-line", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"start": (_node(ax, 0, label),), "end": (_node(ax, length - 1, label),)}, sockets=sk,
                 evidence_domains=("r06/r11 A-line: uniform r = 0; guide of the SLOW glider (speed 1/3).",))


def light_line(board, *, length, label=1, axis="x", gauge_phase=0):
    """Gauged straight light fibre (r04 guide lemma): node i rests at r = 0 if (i + phase) is even, else
    r = 4. Requires chain weight -1 (alternating gauge) and an even length on a closed loop."""
    c = Coupling(tuple(board["signs"]))
    ax = AXES[axis]
    if _straight(c, label, ax) != -1:
        raise ValueError("this light-line generator covers chain weight -1 (alternating r04 gauge) only")
    if length == board["side"] and length % 2:
        raise ValueError("a closed gauged loop needs prod w = +1, i.e. even length")
    cells = {_node(ax, i, label): (0, 0, 0 if (i + gauge_phase) % 2 == 0 else 4) for i in range(length)}
    return Patch("light-line", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"start": (_node(ax, 0, label),), "end": (_node(ax, length - 1, label),)},
                 evidence_domains=("r04 gauged fibre; class 0 (r=0) where i+phase even, class 2 (r=4) where odd.",))


def slot_clock(board, *, state, node_label=1, slot_direction=4):
    """One silent period-4 channel in a slot of a light-line node (trap core or recorder).
    Local origin = the node; the clock sits at node + e(slot) on label ports[slot][node_label]."""
    c = Coupling(tuple(board["signs"]))
    lab = c.ports[slot_direction][node_label]
    off = DIRECTIONS[slot_direction]
    if tuple(state) not in SILENT[0] + SILENT[2]:
        raise ValueError(f"{state} is not one of the 8 silent slot-clock states")
    return Patch("slot-clock", {(*off, lab): tuple(state)}, tensor=_tensor(board["signs"]),
                 background=Channel(*board["background"]), ports={"clock": ((*off, lab),)},
                 evidence_domains=("silent only if state in SILENT[class of its node] (checked by assertion).",))


def glider_cells(side, signs, label, point, start, hit):
    """Window plus history halo of one r06 slow glider on the matter fibre of ``label`` through
    ``point`` (port of r06 ``crystal.glider_delta``); the halo assumes the vacuum (0,0,2)."""
    c = Coupling(tuple(signs))
    if c.weights[0][0] != hit["s"]:
        raise ValueError("glider chain sign must equal sx")
    rotation = group().rotations[label]
    chain = tuple(rotation[i][0] for i in range(3))
    ax = next(i for i in range(3) if chain[i])
    sense = chain[ax]

    def site(k):
        p = list(point)
        p[ax] = (start + sense * k) % side
        return tuple(p)

    out = {}
    for j in range(hit["W"]):
        out[(*site(j), label)] = (hit["a"][j], hit["b"][j], 2 * hit["c"][j])
    for j, s in sorted(hit["halo"].items()):
        p = site(j)
        for d in range(6):
            if DIRECTIONS[d][ax]:
                continue
            q = tuple((p[i] + DIRECTIONS[d][i]) % side for i in range(3))
            out[(*q, c.ports[d][label])] = (0, 0, 2 * (1 + c.weights[d][label] * s))
    return out


def slow_glider(board, *, start, hit="SLOW", label=41, axis="y"):
    """r06 SLOW (moves along the label's body x-axis; -y for label 41) or SLOW_LEFT glider: 3-site window
    + history halo. The window cells are written into a matter-line socket (kind 'glider-seed')."""
    if tuple(board["background"]) != (0, 0, 2):
        raise ValueError("the slow-glider halo is defined for the vacuum (0,0,2)")
    L = board["side"]
    raw = glider_cells(L, board["signs"], label, (0, 0, 0), start % L, GLIDERS[hit])

    def local(k):
        return tuple(((k[i] + L // 2) % L) - L // 2 for i in range(3)) + (k[3],)

    cells = {local(k): v for k, v in raw.items()}
    window = tuple(sorted(k for k in cells if k[3] == label and k[0] == 0 and k[2] == 0))
    return Patch("glider-seed", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"window": window}, sources={"window": window},
                 evidence_domains=("r06 SLOW glider, speed 1/3 on a class-0 matter line (exact laps, native).",))


def spin_ring_z(board):
    """r04 wave-6 holonomy-z light ring (14 nodes, 28 cells) joined to a matter-line node J (local origin)."""
    if tuple(board["signs"]) != (-1, 1, 1):
        raise ValueError("the recorded fragment is for (-,+,+)")
    fragment = json.loads((DATA / "spin_ring_z.json").read_text(encoding="utf-8"))
    cells = {(*c["offset"], c["channel"]): tuple(c["state"]) for c in fragment["cells"]}
    return Patch("spin-ring", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"ring": tuple(sorted(cells))},
                 evidence_domains=("r04 W6: R(t0+18) = C R(t0), R(t0+36) = R(t0) after a feeder glider passes J.",))


BLOCKS = {"matter_line@1": matter_line, "light_line@1": light_line, "slot_clock@1": slot_clock,
          "slow_glider@1": slow_glider, "spin_ring_z@1": spin_ring_z}


# ===================================================================== WAVE 2 (r21) additions
# Registered by the registrar r21 (REGISTRY_SPEC s4 decisions in research/matter_light_v1/r21/).
# guide_net@1 is the general gauged guide generator (r04 guides port, ``guides.py``); all48_site@1,
# phase_gate@2, single_channel@1, k_core@1 and pulse_train@1 complete the set. BLOCKS keeps the five
# blocks above unchanged.
from . import guides as G

ORBIT = ((-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0))     # all-48 dark clock (r08/r13), period 4
S_HIST = (0, -1, 0, 1)                                       # cumulative clock output before phase p
LINEAGE_WAVE2 = {
    "guide_net@1": "r04 guides.py (channel_path, guide_cells, halo_map, packet_state, superpose), pure port; "
                   "reproduces r04 junction_Y_fanout, r08 guided.guide/pulse, r12 e7 routers, r13 E1 devices",
    "all48_site@1": "r08 lmi.all48; r13 device ORBIT/S_HIST history halo; einstein_clock_bricks_v1 all-48 sites",
    "phase_gate@2": "r08 clicktime.gate (phases 0/2, +y side) and r13 Device._place (phases 0..3, z_off -2)",
    "single_channel@1": "r05 star lemma seeds; staged_blocks ShieldedOrbit (single channel, vacuum halo)",
    "k_core@1": "research/components CompactFiveClock, LocalizedSixClock (tracked factories)",
}


def _patch(kind, board, cells, ports=None, sources=None, evidence=()):
    bg = tuple(board["background"])
    return Patch(kind, {k: tuple(v) for k, v in cells.items() if tuple(v) != bg}, tensor=_tensor(board["signs"]),
                 background=Channel(*bg), ports=ports or {}, sources=sources or {}, evidence_domains=evidence)


def _path_nodes(c, spec, built):
    if "branch_of" in spec:
        parent = built[spec["branch_of"]]
        s, g, sig = parent[int(spec["at_node"])]
        d = int(spec["dir"])
        h, w = c.ports[d][g], c.weights[d][g]
        start = G.add(s, d)
        dirs = [d] * (int(spec["length"]) - 1) if "dirs" not in spec else G.expand_dirs(spec["dirs"])
        return G.channel_path(c, start, h, dirs, None, sigma0=sig * w)
    return G.channel_path(c, tuple(spec.get("start", (0, 0, 0))), int(spec["g0"]), G.expand_dirs(spec["dirs"]),
                          None, sigma0=int(spec.get("sigma0", 1)))


def _expr_nodes(expr, built):
    """'name' | '~name' | 'name[a:b]' | '~name[a:b]' | list of these (concatenated)."""
    if isinstance(expr, list):
        out = []
        for e in expr:
            out += _expr_nodes(e, built)
        return out
    rev = expr.startswith("~")
    e = expr[1:] if rev else expr
    if "[" in e:
        name, sl = e[:-1].split("[")
        a, b = sl.split(":")
        nodes = built[name][int(a) if a else None:int(b) if b else None]
    else:
        nodes = built[e]
    return list(reversed(nodes)) if rev else list(nodes)


def guide_net(board, *, paths, packets=(), closed=()):
    """Gauged guide paths with in-flight packets, in local coordinates (the composer wraps explicitly).

    paths:   [{"name", "g0", "dirs": [[d, n], ...], "start"?: [x,y,z], "sigma0"?: +-1}
              | {"name", "branch_of", "at_node", "dir", "length"}]   (a branch = a junction at at_node)
    packets: [{"path": expr, "f": [..], "lead": int, "keep"?: "halo"}]  expr: 'main', '~armA' (inward), lists
             concatenate; keep="halo" writes only the packet's halo remainders (the node cells stay at rest):
             r12's halo-retaining control mask, which is NOT a true-absence control
    closed:  names of closed paths (rings: the last step returns to the start; packets are periodic)
    """
    c = Coupling(tuple(board["signs"]))
    built = {}
    for spec in paths:
        built[spec["name"]] = _path_nodes(c, spec, built)
    rest = {}
    for name, nodes in built.items():
        for k, v in G.guide_cells(nodes).items():
            if k in rest and rest[k] != v:
                raise ValueError(f"guide paths disagree at {k}")
            rest[k] = v
    closed = set(closed)
    pk = []
    for p in packets:
        nodes = _expr_nodes(p["path"], built)
        is_closed = isinstance(p["path"], str) and p["path"] in closed
        cells_p = G.packet_state(c, nodes, tuple(p["f"]), int(p["lead"]), None, closed=is_closed)
        if p.get("keep") == "halo":
            on_path = {(*s_, g_) for nodes_ in built.values() for s_, g_, _ in nodes_}
            cells_p = {k: v for k, v in cells_p.items() if k not in on_path}
        elif p.get("keep") not in (None, "all"):
            raise ValueError("packet keep must be 'all' or 'halo'")
        pk.append(cells_p)
    cells = G.superpose(rest, *pk)
    ports = {}
    for name, nodes in built.items():
        ports[name + "_nodes"] = tuple((*s, g) for s, g, _ in nodes)
    return _patch("guide-net", board, cells, ports=ports,
                  evidence=("r04 guide propagation lemma (THEOREM); fan-out at degree 3/4 exact (r04 30/30); "
                            "merge = JR time reverse of the copy (r12 E7, r13 T1).",))


def _all48_cells(c, site, triple=None, phase=None, halo=True):
    cells = {}
    if phase is not None:
        triple = ORBIT[phase % 4]
    for g in range(48):
        cells[(*site, g)] = tuple(triple)
    if phase is not None and halo and S_HIST[phase % 4]:
        hist = {}
        for g in range(48):
            for d in range(6):
                rec = (*G.add(site, d), c.ports[d][g])
                hist[rec] = hist.get(rec, 0) + c.weights[d][g] * S_HIST[phase % 4]
        for rec, hs in hist.items():
            th = 1 + hs
            if not 0 <= th <= 2:
                raise ValueError("inconsistent clock history")
            if th != 1:
                cells[rec] = (0, 0, 2 * th)
    return cells


def all48_site(board, *, triple=None, phase=None, halo=True):
    """All 48 channels of the local origin site at ``triple``, or at orbit phase ``phase`` of (-1,-1,0)
    with its history-consistent halo (assumes vacuum (0,0,2) under the halo)."""
    if (triple is None) == (phase is None):
        raise ValueError("give exactly one of triple / phase")
    c = Coupling(tuple(board["signs"]))
    cells = _all48_cells(c, (0, 0, 0), triple, phase, halo)
    return _patch("all48-site", board, cells, ports={"site": tuple((0, 0, 0, g) for g in range(48))},
                  evidence=("T4 silent rotor when the halo window holds; period 4 (P2).",))


def phase_gate(board, *, phase=0, offset=(0, 2, 0), halo=True):
    """Dark-clock gate: an all48 clock at orbit phase ``phase`` placed at ``offset`` (two sites, transverse)
    from the fibre node at the local origin. Gate law (CLOCKS s1): X(phase) overflows its shared halo iff
    (t_arr + phase) mod 4 in {1, 2} (r13 sign-corrected form; r08 GATE[0] = phase 0, GATE[2] = phase 2)."""
    off = tuple(int(v) for v in offset)
    if sorted(abs(v) for v in off) != [0, 0, 2]:
        raise ValueError("a phase gate sits two sites from its fibre node along one transverse axis")
    c = Coupling(tuple(board["signs"]))
    cells = _all48_cells(c, off, None, phase, halo)
    return _patch("phase-gate", board, cells,
                  ports={"clock": tuple((*off, g) for g in range(48)), "node_site": ((0, 0, 0, 0),)},
                  evidence=("gate law THEOREM (r08 CLOCKS s1); 1-bit record SIMULATION (R08-2, R08-3).",))


def single_channel(board, *, channel, triple):
    return _patch("single-channel", board, {(0, 0, 0, int(channel)): tuple(triple)},
                  ports={"clock": ((0, 0, 0, int(channel)),)},
                  evidence=("star lemma (periods 5-48) / T4 silent orbit; vacuum halo.",))


def k_core(board, *, shape="dimer", phase=0, conjugated=False, core_remainder=None, halo_parity=0):
    """T6 k-cores from the tracked research.components factories (signs +++ only, as those factories)."""
    from research.components import CompactFiveClock, LocalizedSixClock
    tensor = _tensor(board["signs"])
    if shape == "cube":
        return LocalizedSixClock(phase=phase, core_remainder=2 if core_remainder is None else core_remainder,
                                 halo_parity=halo_parity, tensor=tensor)
    return CompactFiveClock(shape=shape, phase=phase, conjugated=conjugated, tensor=tensor)


BLOCKS_EXT = {"guide_net@1": guide_net, "all48_site@1": all48_site, "phase_gate@2": phase_gate,
              "single_channel@1": single_channel, "k_core@1": k_core}


def pulse_train(board, *, length, arrivals=(), node=None, first=None, period=None, count=0, g0=0, sigma0=1,
                f=(1, 0, -1)):
    """A straight fibre of ``length`` nodes (label ``g0`` self-ported along x; rest (0,0,4) for sigma +1,
    (0,0,0) for sigma -1) carrying unit pulses: each arrival (m, t) is a pulse whose head reaches local
    node m at update t (r08 guided.pulse == r04 packet_state, lead = m - t); or ``count`` pulses every
    ``period`` updates from ``first`` at ``node`` (an approval stream; separate pulses need period >= 4)."""
    c = Coupling(tuple(board["signs"]))
    if c.ports[0][g0] != g0 or c.ports[1][g0] != g0:
        raise ValueError(f"label {g0} is not self-ported along x under {c.body_signs}")
    arr = [tuple(int(v) for v in a) for a in arrivals]
    if count:
        if period is None or (count > 1 and period < 4):
            raise ValueError("a train of separate pulses needs period >= 4 (r08)")
        arr += [(int(node), int(first) + k * int(period)) for k in range(int(count))]
    packets = [{"path": "F", "f": list(f), "lead": m - t} for m, t in arr]
    return guide_net(board, paths=[{"name": "F", "g0": int(g0), "sigma0": int(sigma0), "dirs": [[0, int(length) - 1]]}],
                     packets=packets)


BLOCKS_EXT["pulse_train@1"] = pulse_train
LINEAGE_WAVE2["pulse_train@1"] = "r08 guided.guide + guided.pulse (straight +++ channel-0 fibre), via guide_net@1"
LINEAGE.update(LINEAGE_WAVE2)
BLOCKS.update(BLOCKS_EXT)


# ===================================================================== WAVE 3 (r21) additions
def light_line_v2(board, *, length, label=1, axis="x", gauge_phase=0, sockets=()):
    """light_line@2 = light_line@1 plus optional sockets that accept a 'fibre-packet' or a 'glider-seed' filler
    (e.g. seed.bb27_point@1); with no sockets the output is exactly light_line@1's (update-of light_line@1,
    relation 'generalizes'; r27's light_line_s@1)."""
    base = light_line(board, length=length, label=label, axis=axis, gauge_phase=gauge_phase)
    if not sockets:
        return base
    holes = {int(i) % length for i in sockets}
    ax = AXES[axis]
    keep = {k: (v.a, v.b, v.r) for k, v in base.cells if not (k[ax] in holes and k[3] == label)}
    sk = (Socket("packet-window", tuple(_node(ax, i, label) for i in sorted(holes)), ("fibre-packet", "glider-seed")),)
    return Patch("light-line", keep, tensor=base.tensor, background=base.background, ports=dict(base.ports), sockets=sk,
                 evidence_domains=base.evidence_domains + ("light_line@2: socket nodes are filled by fibre_packet@1",))


def fibre_packet(board, *, front, direction, label=1, axis="x", gauge_phase=0, f=(1, -1)):
    """light.fibre_packet in socket form: the deviation cells of an in-flight r04 packet of admissible shape f
    (default (1,-1), the r27 / D1-B0 packet) on a gauged light line, local origin = the line's node 0.
    Computed with guides.packet_state on a window of the line (sigma = -1 where node + gauge_phase is even);
    the front must sit on a class-0 node (front + gauge_phase even), as registered by r27."""
    c = Coupling(tuple(board["signs"]))
    ax = AXES[axis]
    _straight(c, label, ax)
    if direction not in (1, -1):
        raise ValueError("direction must be +1 or -1")
    if (front + gauge_phase) % 2:
        raise ValueError("packet front must sit on a class-0 node (front + gauge_phase even)")
    pad = len(f) + 3
    start = front - direction * pad
    sigma0 = -1 if (start + gauge_phase) % 2 == 0 else 1
    d = 2 * ax + (0 if direction == 1 else 1)
    site0 = [0, 0, 0]
    site0[ax] = start
    nodes = G.channel_path(c, tuple(site0), label, [d] * (2 * pad), None, sigma0=sigma0)
    rest = G.guide_cells(nodes)
    cells = {k: v for k, v in G.packet_state(c, nodes, tuple(f), pad, None).items() if rest.get(k, (0, 0, 2)) != v}
    line_cells = tuple(sorted(k for k in cells if k[3] == label and all(k[i] == 0 for i in range(3) if i != ax)))
    return Patch("fibre-packet", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"window": line_cells}, sources={"packet": tuple(sorted(cells))},
                 evidence_domains=("light.fibre_packet (r04 alphabet shape f) in socket form; speed 1 node/update.",))


def literal_patch(board, *, cells, kind="literal", ports=None):
    """A literal data block: [[x, y, z, g, a, b, r], ...] in local coordinates (e.g. a seed found by rewind).
    ``kind`` names the socket kind it may fill ('glider-seed' on matter lines, 'fibre-packet' on light lines)."""
    data = {(int(c[0]), int(c[1]), int(c[2]), int(c[3])): (int(c[4]), int(c[5]), int(c[6])) for c in cells}
    if len(data) != len(cells):
        raise ValueError("duplicate address in a literal patch")
    return Patch(kind, data, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={k: tuple(tuple(a) for a in v) for k, v in (ports or {}).items()} or
                 {"cells": tuple(sorted(data))},
                 evidence_domains=("literal initial data; its behaviour is the card's (b), checked by the verifier.",))


BLOCKS.update({"light_line@2": light_line_v2, "light_line_s@1": light_line_v2, "fibre_packet@1": fibre_packet,
               "literal_patch@1": literal_patch})
LINEAGE.update({"light_line@2": "update-of light_line@1 (adds packet sockets; r27 light_line_s@1 is this id's alias)",
                "light_line_s@1": "alias of light_line@2 (r27)",
                "fibre_packet@1": "light.fibre_packet in socket form via guides.packet_state; equals r27 design.fibre_packet "
                                  "(D1 B0 packet, shape (1,-1)) exactly in both directions and gauge phases",
                "literal_patch@1": "literal initial data (seeds found by rewind, r27 bb27_point)"})


# ===================================================================== WAVE 4 (r21) additions
def all48_planes(board, *, planes, size, axis="x"):
    """A stack of consecutive whole planes normal to ``axis`` (local index 0, 1, ...): every site of plane k
    (``size`` x ``size`` sites, the board's transverse extent) holds all 48 channels in ``planes[k]``. The planar
    sector of r05 / r18: planar gliders G-+ (two planes), static mark planes '+' (0,0,4) / '-' (0,0,0), sheets
    and dipole blocks. A vacuum entry (the background) leaves that plane empty (a gap)."""
    ax = AXES[axis]
    others = [i for i in range(3) if i != ax]
    bg = tuple(board["background"])
    cells = {}
    for k, tr in enumerate(planes):
        tr = tuple(int(v) for v in tr)
        if tr == bg:
            continue
        for u in range(int(size)):
            for v in range(int(size)):
                pos = [0, 0, 0]
                pos[ax], pos[others[0]], pos[others[1]] = k, u, v
                for g in range(48):
                    cells[(*pos, g)] = tr
    return Patch("planes", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"origin": (min(cells),)} if cells else {},
                 evidence_domains=("r18 planar translation law (exact ring, 452 cases; native + decoder).",))


BLOCKS.update({"all48_planes@1": all48_planes})
LINEAGE.update({"all48_planes@1": "r05 W5 / r18 planar.OBJ + decode_runs.cells_of (whole all-48 planes)"})


def slow_glider_v2(board, *, start, hit="SLOW", label=41, axis="y"):
    """slow_glider@2 = slow_glider@1 plus explicit r06 catalog species: ``hit`` is 'SLOW' / 'SLOW_LEFT' (then the
    cells equal slow_glider@1's) or a profile {"W", "s", "a", "b", "c", "halo": {j: S}} of a natively verified
    r06 catalog species (e.g. compositions.R06_CATALOG['0'], the class-0 species used by r08 / r14 ladders)."""
    if isinstance(hit, str):
        return slow_glider(board, start=start, hit=hit, label=label, axis=axis)
    if tuple(board["background"]) != (0, 0, 2):
        raise ValueError("the slow-glider halo is defined for the vacuum (0,0,2)")
    prof = {"W": int(hit["W"]), "s": int(hit["s"]), "a": [int(v) for v in hit["a"]], "b": [int(v) for v in hit["b"]],
            "c": [int(v) for v in hit["c"]], "halo": {int(k): int(v) for k, v in hit["halo"].items()}}
    if not (len(prof["a"]) == len(prof["b"]) == len(prof["c"]) == prof["W"]):
        raise ValueError("profile window arrays must have length W")
    L = board["side"]
    raw = glider_cells(L, board["signs"], label, (0, 0, 0), start % L, prof)

    def local(k):
        return tuple(((k[i] + L // 2) % L) - L // 2 for i in range(3)) + (k[3],)

    cells = {local(k): v for k, v in raw.items()}
    window = tuple(sorted(k for k in cells if k[3] == label and k[0] == 0 and k[2] == 0))
    return Patch("glider-seed", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"window": window}, sources={"window": window},
                 evidence_domains=("r06 catalog species (window + history halo), exact translator (r06 catalog).",))


BLOCKS.update({"slow_glider@2": slow_glider_v2})
LINEAGE.update({"slow_glider@2": "update-of slow_glider@1 (generalizes: explicit r06 catalog species profiles; "
                                 "'SLOW'/'SLOW_LEFT' unchanged)"})


def matter_line_v2(board, *, length, label=41, axis="y", sockets=(), medium=(0,), medium_origin=0):
    """matter_line@2 = matter_line@1 plus a periodic catalog medium: node i rests at
    r = 2 * medium[((medium_origin - i) mod length) mod len(medium)] (r06 catalog medium strings read along the
    glider's direction, e.g. '0002' for the 1/2-speed species); medium (0,) is exactly matter_line@1."""
    med = [int(v) for v in medium]
    if tuple(med) == (0,):
        return matter_line(board, length=length, label=label, axis=axis, sockets=sockets)
    if any(v not in (0, 1, 2) for v in med):
        raise ValueError("medium classes are remainders / 2 in {0, 1, 2}")
    c = Coupling(tuple(board["signs"]))
    ax = AXES[axis]
    _straight(c, label, ax)
    holes = set(int(i) for i in sockets)
    P = len(med)
    cells = {_node(ax, i, label): (0, 0, 2 * med[((int(medium_origin) - i) % length) % P])
             for i in range(length) if i not in holes}
    cells = {k: v for k, v in cells.items() if v != tuple(board["background"])}
    sk = (Socket("seed-window", tuple(_node(ax, i, label) for i in sorted(holes)), ("glider-seed",)),) if holes else ()
    return Patch("matter-line", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"start": (_node(ax, 0, label),), "end": (_node(ax, length - 1, label),)}, sockets=sk,
                 evidence_domains=("r06 catalog medium line (natively verified species media, r06 / r08 / r14).",))


BLOCKS.update({"matter_line@2": matter_line_v2})
LINEAGE.update({"matter_line@2": "update-of matter_line@1 (generalizes: periodic r06 catalog medium; medium (0,) "
                                 "unchanged); r14 w3_module A0 seed line"})


# ===================================================================== WAVE 6 (r21b) additions
from . import bform as BF


def fused_mover_window(n, front, direction=1, phase=0):
    """Local chain indices (ascending) that ``fused_mover@1`` writes: every node where beta_n differs from the rest
    at t = 0, padded by one node on each side (a matter-line socket window)."""
    lo, hi = -(4 * n + phase + 6) // 3 - 2, (phase + 1) // 3 + 3
    offs = list(range(lo, hi + 1))
    act = [o for o, a, b, c in zip(offs, *(BF.beta_field(n, offs, t) for t in (phase - 1, phase, phase + 1)))
           if a or b or c]
    dys = range(min(act) - 2, max(act) + 3)
    return sorted(front + direction * dy for dy in dys)


def fused_mover(board, *, n, front, direction=1, phase=0, label=41, axis="y"):
    """r29's fused mover beta_n (matter.fused_mover@1; beta_1 = r06's SLOW family) on a straight class-0 chain of
    ``label`` along ``axis`` (chain weight -1), its front node ``front`` activated at t = -phase, moving ``direction``
    (+1 / -1 along the axis): the cumulative-hand embedding (bform) of the free translator B(t), with the history
    halo on the private vacuum partners.  Writes the whole ``fused_mover_window`` (rest values included), so it fills
    a matter-line socket of exactly those nodes; the chain must be at rest class 0 there, with no coupled partner."""
    if tuple(board["background"]) != (0, 0, 2):
        raise ValueError("the fused-mover halo is defined for the vacuum (0,0,2)")
    if int(n) < 1 or direction not in (1, -1) or int(phase) < 0:
        raise ValueError("n >= 1, direction +-1, phase >= 0")
    c = Coupling(tuple(board["signs"]))
    ax = AXES[axis]
    if _straight(c, label, ax) != -1:
        raise ValueError("fused movers live on chains of weight -1 (the r06 matter-line convention)")
    idx = fused_mover_window(int(n), int(front), direction, int(phase))
    dys = [(i - front) * direction for i in idx]
    nodes = [_node(ax, i, label) for i in idx]
    cells = BF.bform_cells(c, nodes, [0] * len(nodes), BF.beta_field(int(n), dys, int(phase) - 1),
                           BF.beta_field(int(n), dys, int(phase)))
    return Patch("glider-seed", cells, tensor=_tensor(board["signs"]), background=Channel(*board["background"]),
                 ports={"window": tuple(nodes)}, sources={"window": tuple(nodes)},
                 evidence_domains=("r29 Theorem C: beta_n is an exact translator, one node per 3 updates (EXHAUSTIVE, "
                                   "periods <= 18); cumulative-hand embedding (Theorem B0).",))


def matter_line_v3(board, *, length, label=41, axis="y", sockets=(), medium=(0,), medium_origin=0, marks=()):
    """matter_line@3 = matter_line@2 plus sparse rest-class marks: ``marks`` = [[node, class], ...] (class in {0, 1, 2};
    a class-2 mark is r06's phase advancer, a SLOW passing it gains 4 updates); no marks = matter_line@2 exactly."""
    base = matter_line_v2(board, length=length, label=label, axis=axis, sockets=sockets, medium=medium,
                          medium_origin=medium_origin)
    if not marks:
        return base
    ax = AXES[axis]
    holes = {int(i) for i in sockets}
    cells = {k: (v.a, v.b, v.r) for k, v in base.cells}
    for node, cls in marks:
        node, cls = int(node) % length, int(cls)
        if cls not in (0, 1, 2) or node in holes:
            raise ValueError("a mark is a class in {0, 1, 2} on a node that is not a socket")
        cells[_node(ax, node, label)] = (0, 0, 2 * cls)
    cells = {k: v for k, v in cells.items() if v != tuple(board["background"])}
    return Patch("matter-line", cells, tensor=base.tensor, background=base.background, ports=dict(base.ports),
                 sockets=base.sockets, evidence_domains=base.evidence_domains + (
                     "matter_line@3: class-2 marks are r06 phase advancers (r29 braking rule, B-form model).",))


BLOCKS.update({"fused_mover@1": fused_mover, "matter_line@3": matter_line_v3})
LINEAGE.update({"fused_mover@1": "r29 blocks_r29.fused_mover_cells / bnet.beta_field (numpy BGraph), ported to the "
                                 "standard library (bform.py); r29 Theorems B0 and C",
                "matter_line@3": "update-of matter_line@2 (generalizes: sparse rest-class marks); r29 tow / leapfrog "
                                 "rails with class-2 advancers"})


# ---------------------------------------------------------------------------- WAVE 6 fix (r21c; r16c ARCHITECT_REPORT1 s5.2)
_AX_DIR = {(0, 1): 0, (0, -1): 1, (1, 1): 2, (1, -1): 3, (2, 1): 4, (2, -1): 5}       # (axis, sign) -> direction


def staircase_dirs(D, n):
    """The first n unit steps of the monotone lattice staircase from the origin toward the integer direction D
    (deficit rule: step along the axis whose count lags most behind n |D_k| / |D|_1; ties go x, y, z)."""
    S = sum(abs(v) for v in D)
    cnt, out = [0, 0, 0], []
    for step in range(n):
        best, arg = None, None
        for k in range(3):
            if D[k]:
                deficit = (step + 1) * abs(D[k]) - S * cnt[k]
                if best is None or deficit > best:
                    best, arg = deficit, k
        cnt[arg] += 1
        out.append(_AX_DIR[(arg, 1 if D[arg] > 0 else -1)])
    return out


def field_line(D, x_root, x_end):
    """One field line: the part of the staircase toward D (D[0] > 0) from its first node on the plane x = x_root to its
    first node on x = x_end, as {D, start, dirs, sites} (sites in the source's local frame, the source at 0)."""
    S = sum(abs(v) for v in D)
    steps = staircase_dirs(D, (x_end + 2) * S // D[0] + 2 * S)
    pos = [(0, 0, 0)]
    for d in steps:
        pos.append(G.add(pos[-1], d))
    i0 = next(i for i, p in enumerate(pos) if p[0] == x_root)
    i1 = next(i for i, p in enumerate(pos) if p[0] == x_end)
    return {"D": tuple(D), "start": pos[i0], "dirs": steps[i0:i1], "sites": pos[i0:i1 + 1]}


def field_line_bundle_lines(rho=4, x_root=16, x_end=100):
    """medium.field_line_bundle@1 geometry (r33): the (2 rho)^2 lines L<j><k> toward D = (2 rho, 2j+1, 2k+1),
    j, k = -rho .. rho-1 (the +x bundle of a cube-gnomonic source: the line through the grid point
    ((j + 1/2)/rho, (k + 1/2)/rho) of the plane x = 1)."""
    return {f"L{j + rho}{k + rho}": field_line((2 * rho, 2 * j + 1, 2 * k + 1), x_root, x_end)
            for j in range(-rho, rho) for k in range(-rho, rho)}


def bundle_halo_ok(coupling, lines, g0):
    """r04's halo condition over the whole bundle at the channel level: no guide-to-guide shortcut and no halo channel
    fed by two guide nodes (then each line propagates independently: no copy, no coincidence node)."""
    owner, donors = {}, {}
    for name, ln in lines.items():
        for i, (s, g, _) in enumerate(G.channel_path(coupling, ln["start"], g0, ln["dirs"], None)):
            owner[(*s, g)] = (name, i)
    for (x, y, z, g), (name, i) in owner.items():
        for d in range(6):
            rec = (*G.add((x, y, z), d), coupling.ports[d][g])
            if rec in owner:
                on, j = owner[rec]
                if on != name or abs(j - i) != 1:
                    return False
            elif donors.setdefault(rec, (name, i)) != (name, i):
                return False
    return True


def field_line_bundle(board, *, rho=4, x_root=16, x_end=100, g0=0, flux=None, probe=None, packets=(),
                      root_sources=None):
    """medium.field_line_bundle@1 (r33 E13/E13b): the (2 rho)^2 open gauged staircases of ``field_line_bundle_lines``
    from the local origin (the source point), written as guide_net@1 paths L<j><k> (no junction; r04's halo condition
    over the whole bundle is checked here), with in-flight packets given parametrically:
    * ``flux`` {"f", "heads"}: outward packets on every line, heads at the given local node indices;
    * ``probe`` {"f", "x", "half"}: one inward packet on every line whose entry node into the plane x lies in
      |y|, |z| <= half, its head at that entry node (r33's fixed-area probe surface);
    * ``packets``: explicit guide_net@1 packets on the line paths;
    * ``root_sources`` {"triple"}: one single channel per line in the -x halo slot of its root (r33's
      seed.emitter_core@1, the created-flux source of E13b).
    Equals guide_net@1 with the 64 explicit paths and the same packet list (r21b's field_line_bundle_placement)."""
    c = Coupling(tuple(board["signs"]))
    lines = field_line_bundle_lines(int(rho), int(x_root), int(x_end))
    if not bundle_halo_ok(c, lines, int(g0)):
        raise ValueError("field lines share halo channels or touch: raise x_root or lower rho")
    names = sorted(lines)
    pk = []
    if flux:
        pk += [{"path": n, "f": list(flux["f"]), "lead": int(h)} for n in names for h in flux["heads"]]
    if probe:
        r, half = int(probe["x"]), int(probe["half"])
        for n in names:
            sites = lines[n]["sites"]
            p = next((i for i, s in enumerate(sites) if s[0] == r), None)
            if p is not None and max(abs(sites[p][1]), abs(sites[p][2])) <= half:
                pk.append({"path": "~" + n, "f": list(probe["f"]), "lead": len(sites) - 1 - p})
    pk += [dict(q) for q in packets]
    paths = [{"name": n, "g0": int(g0), "start": list(lines[n]["start"]), "dirs": [[d, 1] for d in lines[n]["dirs"]]}
             for n in names]
    net = guide_net(board, paths=paths, packets=pk)
    cells = {k: (v.a, v.b, v.r) for k, v in net.cells}
    ports = dict(net.ports)
    if root_sources:
        for n in names:
            s0 = tuple(lines[n]["start"])
            g_root = G.channel_path(c, s0, int(g0), lines[n]["dirs"][:1], None)[0][1]
            addr = (*G.add(s0, 1), c.ports[1][g_root])
            if addr in cells:
                raise ValueError(f"the root source of {n} would overwrite a guide or packet cell")
            cells[addr] = tuple(root_sources["triple"])
            ports[f"{n}_root_source"] = (addr,)
    return _patch("field-line-bundle", board, cells, ports=ports,
                  evidence=net.evidence_domains + ("r33: the bundle's lines are independent guides (halo condition "
                                                   "checked); counts at fixed area are geometric (R10G-46..50).",))


BLOCKS.update({"field_line_bundle@1": field_line_bundle})
LINEAGE.update({"field_line_bundle@1": "r33 field_lines.bundle / e13_build.spec and e13b_build.cores, via r21b's "
                                       "field_line_bundle_placement (guide_net@1); r04 guide algebra and halo rule"})


# ===================================================================== WAVE 8 (r21c) additions
def plane_light(board, *, beams):
    """light.plane_light@1 (r26 blocks.plane111): exact A1 plane light on the whole board, a sum of travelling
    profiles along the eight body diagonals.  ``beams`` = [{"sigma": [s1, s2, s3] (each +-1, the
    direction of motion), "profile": [f_0, ..., f_{p-1}] (integers, p dividing the side), "shift": k (default 0)}];
    every channel of every site x gets a = sum f((sigma.x + 1 + k) mod p), b = sum f((sigma.x + k) mod p), r = 2, and
    a site with a = b = 0 stays vacuum.  The patch is the whole board in local coordinates 0..L-1 (place it at the
    origin).  One beam (1,1,1) with a delta profile is the published diag_sheet (light.front_111@1).  Needs the
    coupling +++ and the quiet vacuum (0, 0, 2), the scope of r26's theorem."""
    L = int(board["side"])
    if tuple(board["signs"]) != (1, 1, 1) or tuple(board["background"]) != (0, 0, 2):
        raise ValueError("plane_light@1 needs the coupling +++ and the vacuum (0, 0, 2)")
    parsed = []
    for bm in beams:
        s = tuple(int(v) for v in bm["sigma"])
        f = [int(v) for v in bm["profile"]]
        if len(s) != 3 or any(v not in (1, -1) for v in s):
            raise ValueError("sigma must be a body diagonal (+-1, +-1, +-1)")
        if not f or L % len(f):
            raise ValueError("the profile period must divide the side")
        parsed.append((s, f, int(bm.get("shift", 0))))
    cells = {}
    for x in range(L):
        for y in range(L):
            for z in range(L):
                a = b = 0
                for s, f, k in parsed:
                    n = s[0] * x + s[1] * y + s[2] * z + k
                    b += f[n % len(f)]
                    a += f[(n + 1) % len(f)]
                if a or b:
                    for g in range(48):
                        cells[(x, y, z, g)] = (a, b, 2)
    return _patch("plane-light", board, cells,
                  evidence=("r26 [THEOREM] (coherent_wave_algebra.md, extended to sums): the input of every channel is "
                            "3 sum (f(s + 1) + f(s - 1)), a multiple of 3, so r stays 2 and b_t(x) = sum f(sigma.x + k - t) "
                            "exactly, at every amplitude.",))


BLOCKS.update({"plane_light@1": plane_light})
LINEAGE.update({"plane_light@1": "r26 blocks.plane111 (proposed light.plane111@1), r25 preparations_e11.main_diagonal "
                                 "and r01 blocks.diag_sheet; update-of the global preparation of light.front_111@1"})
