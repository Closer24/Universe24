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
    """light_line@2 = light_line@1 plus optional packet sockets (kind 'fibre-packet'); with no sockets the output
    is exactly light_line@1's (update-of light_line@1, relation 'generalizes'; r27's light_line_s@1)."""
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
