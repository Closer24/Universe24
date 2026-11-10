"""Compositions of registered blocks (format ``u24-composition-v1``) to one initial state.

A composition names one board (side, background, one coupling) and placements of registered
blocks (id@version, parameters, translation ``at``, proper 2O lift ``orientation``, explicit
``wrap``). ``compose`` uses the repository's strict one-time assembler (``research.components``:
no overwrite, no addition, sockets filled only by the declared filler kind, one tensor and one
background). The composition's ``assertions`` are then checked on the initial data. Nothing is
evolved here and nothing acts after t = 0. Controls are masks of one composition
(``apply_control``), never hand edits. Ported from the registrar's ``compose_v1`` (r21).

Added by r21 (WAVE 2), backwards compatible:
* ``gauge`` on a placement ({"character": bool, "staggered": bool} or "auto"), with ``native_signs``:
  the block is generated for its own triple and moved into the board's triple as data (``symmetry``;
  THEORY S7). Only inside one gauge class (B or F), with a J-fixed background, and on even L when
  staggered. Click addresses are unchanged; C1 <-> C2 and q -> -q on the flipped channels.
* ``include`` placements: a sub-composition (a spec) placed by translation ``at``, optionally gauged;
  its placements get ``prefix`` and its assertions are carried along.
* assertions ``beside_fibre`` and ``clearance``.

Added by r21 (WAVE 4), backwards compatible:
* assertion ``guide_halo_clear``: [{"port": "<placement>.<path>_nodes", "closed": bool, "allow": [[x,y,z,g]]}]
  -- every halo channel of that guide (receivers off the guide, from the board's coupling) is vacuum in the
  initial state, except the listed junction channels (r04's insertion rule for rings beside a line);
* ``apply_control`` on a spec without ``assertions`` no longer raises (r12) and adds none.
"""
from __future__ import annotations

import hashlib
import json

from universe24 import Channel
from universe24.core.group_2o import DIRECTIONS, group, rotate
from universe24.experiments import checkpoint_data
from research.components import BoardSpec, Patch, Socket, TensorSpec, finalize, place

from . import symmetry as SY
from . import guides as G
from .generators import BLOCKS, SILENT, _tensor

FORMAT = "u24-composition-v1"
_GR = group()


def expand(spec):
    """Inline ``include`` placements (recursively); returns a new spec without includes."""
    out = json.loads(json.dumps(spec))
    placements, extra = [], {}
    for p in out["placements"]:
        if "include" not in p:
            placements.append(p)
            continue
        sub = expand(p["include"])
        pre = p.get("prefix", p["name"] + "_")
        at = p.get("at", [0, 0, 0])
        gauge = p.get("gauge")
        for q in sub["placements"]:
            q = json.loads(json.dumps(q))
            q["name"] = pre + q["name"]
            q["at"] = [q["at"][i] + at[i] for i in range(3)]
            if gauge is not None:
                if "gauge" in q:
                    raise ValueError("nested gauges are not supported")
                q["gauge"] = gauge
                q["native_signs"] = list(sub["board"]["coupling"]["signs"])
            placements.append(q)
        for k, v in sub.get("assertions", {}).items():
            if k == "slot_clocks_silent":
                extra.setdefault(k, []).extend(pre + n for n in v)
            elif k == "beside_fibre":
                extra.setdefault(k, []).extend([pre + a, pre + b] for a, b in v)
            elif k == "junction_classes":
                d = extra.setdefault(k, {})
                for key, cls in v.items():
                    x, y = (int(s) for s in key.split(","))
                    d[f"{x + at[0]},{y + at[1]}"] = cls
    out["placements"] = placements
    for k, v in extra.items():
        if isinstance(v, dict):
            out.setdefault("assertions", {}).setdefault(k, {}).update(v)
        else:
            out.setdefault("assertions", {}).setdefault(k, []).extend(v)
    return out


def _world_patch(patch, at, orientation, wrap, L, gauge, board_signs, board_bg):
    """The patch in world coordinates (lifted, translated, wrapped), gauge-transported into the board."""
    R = _GR.rotations[orientation]

    def tr(a):
        xyz = rotate(R, a[:3])
        xyz = tuple(xyz[i] + at[i] for i in range(3))
        if wrap:
            xyz = tuple(v % L for v in xyz)
        return (*xyz, _GR.multiplication[orientation][a[3]])

    character, staggered = gauge
    if staggered and L % 2:
        raise ValueError("the staggered gauge needs an even board side")
    cells = SY.gauge_cells({tr(k): (v.a, v.b, v.r) for k, v in patch.cells}, character, staggered, board_bg)
    return Patch(patch.kind, cells, tensor=TensorSpec.from_signs(board_signs), background=Channel(*board_bg),
                 ports={k: tuple(tr(a) for a in v) for k, v in patch.ports.items()},
                 sources={k: tuple(tr(a) for a in v) for k, v in patch.sources.items()},
                 sockets=tuple(Socket(s.name, tuple(tr(a) for a in s.addresses), s.allowed_kinds)
                               for s in patch.sockets),
                 evidence_domains=patch.evidence_domains)


def compose(spec, blocks=None):
    """``(PreparedBoard, assertion report)`` for one composition (reference couplings only)."""
    spec = expand(spec)
    if spec.get("format") != FORMAT:
        raise ValueError("unknown composition format")
    coupling = spec["board"]["coupling"]
    if coupling.get("variant") is not None:
        raise ValueError("variant boards are not composed by registry v1; write a variant init file")
    signs = tuple(coupling["signs"])
    board = {"side": spec["board"]["side"], "signs": signs, "background": tuple(spec["board"]["background"])}
    blocks = BLOCKS if blocks is None else blocks
    placements = []
    for p in spec["placements"]:
        if p["block"] not in blocks:
            raise ValueError(f"unregistered block {p['block']}")
        native = tuple(p.get("native_signs", signs))
        gauge = p.get("gauge")
        if gauge == "auto":
            g = SY.gauge_for(native, signs)
            if g is None:
                raise ValueError(f"{p['name']}: {native} and {signs} are not in one gauge class")
            gauge = {"character": g[0], "staggered": g[1]}
        if gauge is None and native != signs:
            raise ValueError(f"{p['name']} needs {native}; the board has {signs} (one tensor per board)")
        patch = blocks[p["block"]]({**board, "signs": native}, **p.get("params", {}))
        if gauge is None:
            placements.append(place(patch, at=tuple(p["at"]), name=p["name"], orientation=p.get("orientation", 0),
                                    wrap=p.get("wrap", False)))
            continue
        g = (bool(gauge.get("character")), bool(gauge.get("staggered")))
        if SY.gauged_signs(native, *g) != signs:
            raise ValueError(f"{p['name']}: gauge {g} maps {native} to {SY.gauged_signs(native, *g)}, not {signs}")
        wp = _world_patch(patch, tuple(p["at"]), p.get("orientation", 0), p.get("wrap", False), board["side"], g,
                          signs, board["background"])
        placements.append(place(wp, at=(0, 0, 0), name=p["name"]))
    prepared = finalize(BoardSpec(board["side"], background=Channel(*board["background"]),
                                  tensor=_tensor(board["signs"])), placements)
    return prepared, check_assertions(spec, prepared)


def junctions(prepared, line_label_a=41, line_label_b=1):
    """(A-node, B-node, weight) for every pair of the two line labels linked by the fixed coupling."""
    st, eng = prepared.initial, prepared.engine
    L = st.cube.side
    out = []
    for k, v in st.cells.items():
        if k[3] != line_label_b:
            continue
        for d in range(6):
            q = tuple((k[i] + DIRECTIONS[d][i]) % L for i in range(3)) + (eng.coupling.ports[d][k[3]],)
            if q[3] == line_label_a and q in st.cells and st.cells[q].r == 0 and st.cells[q].a == st.cells[q].b == 0:
                out.append((q, k, eng.coupling.weights[d][k[3]]))
    return out


def _manhattan(a, b, L):
    return sum(min((a[i] - b[i]) % L, (b[i] - a[i]) % L) for i in range(3))


def check_assertions(spec, prepared):
    """Composition-level checks on the initial data (junction classes, silent slot clocks, gates beside
    fibres, clearances)."""
    rep = {}
    a = spec.get("assertions", {})
    st = prepared.initial
    if "junction_classes" in a:
        found = {}
        for qa, kb, w in junctions(prepared):
            found[f"{qa[0]},{qa[1]}"] = {"class": st.cells[kb].r // 2, "weight": w}
        want = a["junction_classes"]
        rep["junctions_found"] = found
        rep["junction_classes_ok"] = (all(found.get(k, {}).get("class") == v for k, v in want.items())
                                      and set(found) == set(want))
    if "slot_clocks_silent" in a:
        ok = True
        for name in a["slot_clocks_silent"]:
            (addr,) = prepared.ports[name + ".clock"]
            node = (addr[0], addr[1], addr[2] - 1, 1)
            cls = st.cells[node].r // 2 if node in st.cells else None
            val = st.cells[addr]
            ok &= cls in SILENT and (val.a, val.b, val.r) in SILENT[cls]
        rep["slot_clocks_silent_ok"] = bool(ok)
    L = st.cube.side
    if "beside_fibre" in a:
        ok = True
        for gate, fibre in a["beside_fibre"]:
            node = prepared.ports[gate + ".node_site"][0][:3]
            nodes = {k[:3] for k in prepared.ports[fibre]} if fibre in prepared.ports else set()
            clock = prepared.ports[gate + ".clock"][0][:3]
            ok &= node in nodes and _manhattan(node, clock, L) == 2 and clock not in nodes
        rep["beside_fibre_ok"] = bool(ok)
    if "clearance" in a:
        res = []
        for c in a["clearance"]:
            sup = []
            for names in (c["a"], c["b"]):
                s = set()
                for rec in prepared.manifest["components"]:
                    if rec["name"] in names:
                        s.update(tuple(r[:3]) for r in rec["raw_assignments"])
                sup.append(s)
            d = min(_manhattan(x, y, L) for x in sup[0] for y in sup[1]) if sup[0] and sup[1] else None
            res.append({"a": list(c["a"])[:3], "b": list(c["b"])[:3], "min_manhattan": d, "required": c["min"],
                        "ok": d is not None and d >= c["min"]})
        rep["clearance"] = res
        rep["clearance_ok"] = all(r["ok"] for r in res)
    if "guide_halo_clear" in a:          # WAVE 4: r04 insertion rule (a guide's halo channels stay vacuum)
        coupling = prepared.engine.coupling
        res = []
        for item in a["guide_halo_clear"]:
            nodes = [(tuple(k[:3]), k[3], 1) for k in prepared.ports[item["port"]]]
            allow = {(int(v[0]) % L, int(v[1]) % L, int(v[2]) % L, int(v[3])) for v in item.get("allow", [])}
            recs = {rec for hm in G.halo_map(coupling, nodes, L, bool(item.get("closed", False))) for rec, _, _ in hm}
            bad = sorted(r for r in recs if r in st.cells and r not in allow)
            res.append({"port": item["port"], "halo": len(recs), "prepared_in_halo": len(bad), "examples": bad[:3]})
        rep["guide_halo_clear"] = res
        rep["guide_halo_clear_ok"] = all(r["prepared_in_halo"] == 0 for r in res)
    return rep


def apply_control(spec, control):
    """A control is a mask of the same composition: remove placements and/or override parameters.
    With ``unfill_sockets`` the sockets that a removed seed filled return to the line's rest state."""
    out = json.loads(json.dumps(spec))
    out["id"] = spec["id"] + "__" + control["name"]
    removed = set(control.get("remove", []))
    out["placements"] = [p for p in out["placements"] if p["name"] not in removed]
    for p in out["placements"]:
        if p["name"] in control.get("override", {}):
            p["params"].update(control["override"][p["name"]])
        if control.get("unfill_sockets") and p["block"] == "matter_line@1":
            p["params"]["sockets"] = []
    if "assertions" in out or control.get("assertions"):     # a spec without assertions stays without them
        a = out.setdefault("assertions", {})
        for k, v in control.get("assertions", {}).items():
            if v is None:
                a.pop(k, None)
            else:
                a[k] = v
        a["slot_clocks_silent"] = [n for n in a.get("slot_clocks_silent", []) if n not in removed]
    out.pop("controls", None)
    return out


def init_data(prepared, steps: int = 0) -> dict:
    """The official init dictionary (``python -m universe24 --config``) of a composed board."""
    data = checkpoint_data(prepared.initial, prepared.engine, 0)["experiment"]
    data["steps"] = steps
    return data


def state_digest(state, signs) -> str:
    blob = json.dumps([list(signs), state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())], separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()
