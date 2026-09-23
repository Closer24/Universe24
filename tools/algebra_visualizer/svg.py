"""The pictures of the algebra visualizer as inline SVG text.

Each function takes a panel's figure data (`panels.py`) and returns one
`<svg>` element. Floats appear in drawing coordinates alone; every number
printed as text sits under an element carrying `data-kind` (the root `<svg>`
carries the figure's dominant kind, a text element its own where it
differs). Colours are the page's CSS classes, so a picture follows the
viewer's theme.
"""

from __future__ import annotations

import math
from html import escape
from typing import Any

CLASS_MARK = {"axes": "m-axes", "face_diagonals": "m-face", "body_diagonals": "m-body", "rest": "m-rest"}
CLASS_WORD = {
    "axes": "the axes",
    "face_diagonals": "the face diagonals",
    "body_diagonals": "the body diagonals",
    "rest": "the rest of the fan",
}


def _svg(width: int, height: int, body: str, kind: str, label: str) -> str:
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}" data-kind="{kind}" '
        f'class="figure">{body}</svg>'
    )


def _text(
    x: float, y: float, text: str, cls: str = "t", anchor: str = "start", kind: str | None = None
) -> str:
    extra = f' data-kind="{kind}"' if kind else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(text)}</text>'


# --- layer 1 ----------------------------------------------------------------


def boards(fig: dict[str, Any]) -> str:
    parts = []
    y = 24
    for board in fig["boards"]:
        shape = board["shape"]
        boundary = board["boundary"]
        parts.append(_text(8, y, str(board["name"]), "t-label"))
        x = 150
        for axis, extent in zip(("x", "y", "z"), shape, strict=True):
            periodic = isinstance(boundary, dict) and boundary.get(axis) == "periodic"
            if periodic:
                parts.append(f'<circle cx="{x + 40}" cy="{y - 4}" r="14" class="line"/>')
                parts.append(_text(x + 40, y + 26, f"{axis}: a circle of {extent}", "t-small", "middle"))
            else:
                parts.append(f'<line x1="{x}" y1="{y - 4}" x2="{x + 80}" y2="{y - 4}" class="line"/>')
                parts.append(f'<line x1="{x}" y1="{y - 12}" x2="{x}" y2="{y + 4}" class="line-strong"/>')
                parts.append(
                    f'<line x1="{x + 80}" y1="{y - 12}" x2="{x + 80}" y2="{y + 4}" class="line-strong"/>'
                )
                parts.append(
                    _text(
                        x + 40,
                        y + 26,
                        f"{axis}: a segment of {extent}, faces face:-{axis}, face:+{axis}",
                        "t-small",
                        "middle",
                    )
                )
            x += 200
        y += 64
    return _svg(
        760, y - 16, "".join(parts), "DECLARATION", "the GameBoard's axes, a circle or a segment each"
    )


def node_ports(fig: dict[str, Any]) -> str:
    cx, cy = 200, 120
    spokes = {
        "+x": (110, 0),
        "-x": (-110, 0),
        "+y": (55, -75),
        "-y": (-55, 75),
        "+z": (0, -100),
        "-z": (0, 100),
    }
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="16" class="node"/>',
        _text(cx, cy + 34, "a Node", "t-small", "middle"),
    ]
    for port in fig["ports"]:
        dx, dy = spokes[port]
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + dx}" y2="{cy + dy}" class="line"/>')
        parts.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="9" class="node-far"/>')
        ox = 18 if dx >= 0 else -18
        parts.append(
            _text(cx + dx + ox, cy + dy + 4, f"Port {port}", "t-small", "start" if dx >= 0 else "end")
        )
    parts.append(
        _text(
            cx,
            232,
            "the seven Nodes of the causal front, one message per Link per interval",
            "t-small",
            "middle",
        )
    )
    return _svg(400, 244, "".join(parts), "DECLARATION", "a Node with its six Ports")


def state_vector(fig: dict[str, Any]) -> str:
    parts = []
    x = 8
    for name in fig["components"]:
        w = 22 + 8 * len(name)
        parts.append(f'<rect x="{x}" y="14" width="{w}" height="34" rx="4" class="box"/>')
        parts.append(_text(x + w / 2, 36, name, "t-mono", "middle"))
        x += w + 8
    parts.append(
        _text(
            8,
            70,
            "s, the state vector of one record: each component a bounded integer accumulator",
            "t-small",
        )
    )
    return _svg(
        max(x + 8, 560), 80, "".join(parts), "GAMEBOARD", "the components of a record's state vector"
    )


def translation(fig: dict[str, Any]) -> str:
    age, links = int(fig["age"]), int(fig["links"])
    parts = [
        '<line x1="30" y1="60" x2="370" y2="60" class="line"/>',
        '<circle cx="30" cy="60" r="7" class="node"/>',
        '<circle cx="370" cy="60" r="7" class="mark-detector"/>',
        _text(30, 88, "the birth", "t-small", "middle"),
        _text(370, 88, f"the click at {fig['face']}", "t-small", "middle"),
        _text(200, 44, f"{links} Links crossed in {age} intervals of age", "t-small", "middle"),
    ]
    steps = min(links, 40)
    for i in range(1, steps):
        x = 30 + 340 * i / steps
        parts.append(f'<line x1="{x:.1f}" y1="56" x2="{x:.1f}" y2="64" class="line"/>')
    return _svg(400, 100, "".join(parts), "CONVERSION", "one row from its birth to its click")


def phase_plane(fig: dict[str, Any]) -> str:
    pointers = fig["pointers"]
    size = 240
    c = size / 2
    scale = max([abs(int(p["x"])) for p in pointers] + [abs(int(p["y"])) for p in pointers] + [1])
    parts = [
        f'<line x1="8" y1="{c}" x2="{size - 8}" y2="{c}" class="grid"/>',
        f'<line x1="{c}" y1="8" x2="{c}" y2="{size - 8}" class="grid"/>',
        f'<circle cx="{c}" cy="{c}" r="{c - 12}" class="grid"/>',
        _text(size - 10, c - 6, "X", "t-small", "end"),
        _text(c + 6, 16, "Y", "t-small"),
    ]
    for p in pointers:
        x = c + (int(p["x"]) / scale) * (c - 14)
        y = c - (int(p["y"]) / scale) * (c - 14)
        parts.append(
            f'<line x1="{c}" y1="{c}" x2="{x:.1f}" y2="{y:.1f}" class="arrow"><title>{escape(str(p["name"]))}: ({int(p["x"])}, {int(p["y"])})</title></line>'
        )
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" class="mark-detector"><title>{escape(str(p["name"]))}: ({int(p["x"])}, {int(p["y"])})</title></circle>'
        )
    parts.append(_text(8, size - 4, f"the phase plane; the circle's radius {scale}", "t-small"))
    return _svg(size, size, "".join(parts), "DETECTOR", "pointers on the phase plane")


def split(fig: dict[str, Any]) -> str:
    born = int(fig["born"])
    parts = [
        '<line x1="20" y1="80" x2="150" y2="80" class="arrow"/>',
        _text(20, 66, f"{fig['absorbed']} row in", "t-small"),
    ]
    shown = min(born, 25)
    for i in range(shown):
        angle = -60 + 120 * i / max(shown - 1, 1)
        x2 = 150 + 150 * math.cos(math.radians(angle))
        y2 = 80 + 70 * math.sin(math.radians(angle))
        parts.append(f'<line x1="150" y1="80" x2="{x2:.1f}" y2="{y2:.1f}" class="line-faint"/>')
    parts.append(_text(310, 30, f"{born} rows out (the declared fan)", "t-small", "end"))
    return _svg(320, 160, "".join(parts), "DETECTOR", "a split at a re-emitter")


def ladder(fig: dict[str, Any]) -> str:
    cells = fig["cells"]
    n = int(fig["N"]) or 1
    u = fig["u"]
    width, top, bottom = 520, 20, 70
    parts = [f'<line x1="20" y1="{bottom}" x2="{width - 20}" y2="{bottom}" class="line"/>']
    for name, rung in cells:
        x = 20 + (width - 40) * min(rung, n) / n
        chosen = name == fig["chosen"]
        parts.append(
            f'<line x1="{x:.1f}" y1="{top + (0 if chosen else 20)}" x2="{x:.1f}" y2="{bottom}" class="{"rung-chosen" if chosen else "rung"}"><title>{escape(name)}: the rung {rung}</title></line>'
        )
    if u is not None:
        x = 20 + (width - 40) * min(int(u), n) / n
        parts.append(
            f'<polygon points="{x - 6:.1f},{bottom + 14} {x + 6:.1f},{bottom + 14} {x:.1f},{bottom + 3}" class="mark-detector"/>'
        )
        parts.append(_text(x, bottom + 30, f"u = {u}", "t-small", "middle"))
    parts.append(_text(20, bottom + 30, "0", "t-small"))
    parts.append(_text(width - 20, bottom + 30, f"N = {n}", "t-small", "end"))
    parts.append(
        _text(
            20,
            14,
            f"the ladder of one gather: {len(cells)} rungs; the tallest is the chosen cell",
            "t-small",
        )
    )
    return _svg(
        width, 110, "".join(parts), "DETECTOR", "the ladder of a gather against the wheel's value"
    )


def light_rule(fig: dict[str, Any]) -> str:
    ex = fig["example"]
    nb = ex["neighbours"]
    cx, cy = 260, 150
    places = {
        "a_E": (110, 0),
        "a_W": (-110, 0),
        "a_N": (60, -70),
        "a_S": (-60, 70),
        "a_U": (0, -105),
        "a_D": (0, 105),
    }
    parts = []
    for name, (dx, dy) in places.items():
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + dx}" y2="{cy + dy}" class="line"/>')
        parts.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="16" class="node-far"/>')
        parts.append(_text(cx + dx, cy + dy + 4, str(nb[name]), "t-mono", "middle"))
        parts.append(
            _text(
                cx + dx,
                cy + dy + 30 if dy > 0 else (cy + dy - 22 if dy < 0 else cy + dy + 30),
                name,
                "t-small",
                "middle",
            )
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="20" class="node"/>')
    parts.append(_text(cx, cy + 4, "a_now", "t-on-node", "middle"))
    x0 = 470
    parts.append(_text(x0, 40, "the Node's row", "t-label"))
    parts.append(_text(x0, 66, f"a_before = {ex['a_before']}", "t-mono"))
    parts.append(_text(x0, 90, f"r = {ex['r']}", "t-mono"))
    parts.append(_text(x0, 120, f"S_6 = {ex['S_6']}", "t-mono"))
    parts.append(
        _text(
            x0,
            154,
            f"light, [1, 1]: a_next = {ex['light']['a_next']}, r' = {ex['light']['r_next']}",
            "t-mono",
        )
    )
    parts.append(
        _text(
            x0,
            178,
            f"3 x {ex['light']['a_next']} + {ex['light']['r_next']} = {ex['S_6']} - 3 x {ex['a_before']} + {ex['r']}",
            "t-small",
        )
    )
    parts.append(
        _text(
            x0,
            212,
            f"a massive kind, [2, 3]: a_next = {ex['massive']['a_next']}, r' = {ex['massive']['r_next']}",
            "t-mono",
        )
    )
    parts.append(
        _text(
            x0,
            236,
            f"9 x {ex['massive']['a_next']} + {ex['massive']['r_next']} = 2 x {ex['S_6']} - 9 x {ex['a_before']} + {ex['r']}",
            "t-small",
        )
    )
    parts.append(_text(x0, 276, "a worked example, COMPUTATION; not from a run", "t-small"))
    parts.append(
        _text(cx, 318, "3 a_next + r' = S_6 - 3 a_before + r,  0 <= r' < 3", "t-mono", "middle")
    )
    return _svg(
        820, 330, "".join(parts), "COMPUTATION", "the light rule on one Node and its six neighbours"
    )


# --- layer 2 ----------------------------------------------------------------


FACE_AXES = {
    "+x": ("y", "z"),
    "-x": ("y", "z"),
    "+y": ("x", "z"),
    "-y": ("x", "z"),
    "+z": ("x", "y"),
    "-z": ("x", "y"),
}
NET_PLACES = {"+z": (1, 0), "-y": (0, 1), "+x": (1, 1), "+y": (2, 1), "-x": (3, 1), "-z": (1, 2)}
AXIS_INDEX = {"x": 0, "y": 1, "z": 2}


def cube_net(fig: dict[str, Any]) -> str:
    shape = fig["shape"]
    size = 150
    gap = 10
    parts = []
    origins = {}
    for face, (col, row) in NET_PLACES.items():
        ox, oy = 10 + col * (size + gap), 10 + row * (size + gap)
        origins[face] = (ox, oy)
        parts.append(f'<rect x="{ox}" y="{oy}" width="{size}" height="{size}" class="face"/>')
        a, b = FACE_AXES[face]
        parts.append(_text(ox + 4, oy + 12, f"face:{face}  ({a}, {b})", "t-small"))

    def place(face: str, node: list[int]) -> tuple[float, float]:
        a, b = FACE_AXES[face]
        ox, oy = origins[face]
        ea, eb = max(shape[AXIS_INDEX[a]] - 1, 1), max(shape[AXIS_INDEX[b]] - 1, 1)
        return ox + 8 + (size - 16) * node[AXIS_INDEX[a]] / ea, oy + size - 8 - (size - 16) * node[
            AXIS_INDEX[b]
        ] / eb

    birth = fig["birth"]
    bx, by = place("+x", birth)
    for mark in fig["clicks"]:
        face = mark["face"].split(":")[1]
        x, y = place(face, mark["node"])
        parts.append(
            f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{x:.1f}" y2="{y:.1f}" class="line-inference" data-tick="{mark["tick"]}"/>'
        )
    for mark in fig["clicks"]:
        face = mark["face"].split(":")[1]
        x, y = place(face, mark["node"])
        cls = CLASS_MARK.get(mark["cls"], "m-rest")
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" class="mark {cls}" data-tick="{mark["tick"]}">'
            f"<title>tick {mark['tick']}, the Node ({mark['node'][0]}, {mark['node'][1]}, {mark['node'][2]}), {escape(mark['face'])}, {CLASS_WORD.get(mark['cls'], mark['cls'])}</title></circle>"
        )
    parts.append(
        f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="5" class="node"><title>the birth Node ({birth[0]}, {birth[1]}, {birth[2]}), inside the board, drawn on face:+x by its (y, z)</title></circle>'
    )
    legend_y = 10 + 3 * (size + gap) + 6
    x = 10
    for cls, word in CLASS_WORD.items():
        parts.append(f'<circle cx="{x + 5}" cy="{legend_y - 4}" r="4" class="mark {CLASS_MARK[cls]}"/>')
        parts.append(_text(x + 14, legend_y, word, "t-small"))
        x += 150
    parts.append(f'<circle cx="{x + 5}" cy="{legend_y - 4}" r="4" class="node"/>')
    parts.append(_text(x + 14, legend_y, "the birth Node", "t-small"))
    width = 10 + 4 * (size + gap)
    return _svg(
        width,
        legend_y + 10,
        "".join(parts),
        "DETECTOR",
        "the six faces unfolded, every face click a mark",
    )


def pace(fig: dict[str, Any]) -> str:
    points = fig["points"]
    width, height, left, bottom, top, right = 640, 360, 56, 320, 20, 20
    max_age = max([int(p["age"]) for p in points] + [1])
    max_dist = max([math.sqrt(int(p["distance2"])) for p in points] + [1.0])
    x_of = lambda age: left + (width - left - right) * age / max_age  # noqa: E731
    y_of = lambda d: bottom - (bottom - top) * d / max_dist  # noqa: E731
    parts = [
        f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" class="line"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" class="line"/>',
    ]
    for k in range(0, 5):
        age = max_age * k / 4
        parts.append(_text(x_of(age), bottom + 18, f"{age:.0f}", "t-small", "middle"))
        d = max_dist * k / 4
        parts.append(_text(left - 6, y_of(d) + 4, f"{d:.0f}", "t-small", "end"))
        parts.append(
            f'<line x1="{left}" y1="{y_of(d):.1f}" x2="{width - right}" y2="{y_of(d):.1f}" class="grid"/>'
        )
    parts.append(
        _text(
            (left + width - right) / 2,
            bottom + 34,
            "the age at the click (intervals)",
            "t-small",
            "middle",
        )
    )
    parts.append(
        f'<text x="14" y="{(top + bottom) / 2:.1f}" class="t-small" text-anchor="middle" transform="rotate(-90 14 {(top + bottom) / 2:.1f})">the distance to the face (Links)</text>'
    )
    c = float(fig["c"])
    age_end = min(max_age, max_dist / c)
    parts.append(
        f'<line x1="{x_of(0):.1f}" y1="{y_of(0):.1f}" x2="{x_of(age_end):.1f}" y2="{y_of(c * age_end):.1f}" class="line-c"/>'
    )
    parts.append(
        _text(
            x_of(age_end * 0.42),
            y_of(c * age_end * 0.42) - 12,
            "c = 1 / sqrt 3, the algebra's line (COMPUTATION)",
            "t-small",
            "middle",
            "COMPUTATION",
        )
    )
    shapes = {"axes": "circle", "face_diagonals": "rect", "body_diagonals": "diamond", "rest": "dot"}
    for p in points:
        x, y = x_of(int(p["age"])), y_of(math.sqrt(int(p["distance2"])))
        cls = CLASS_MARK.get(p["cls"], "m-rest")
        title = f"<title>{CLASS_WORD.get(p['cls'], p['cls'])}: the age {p['age']}, {p['links']} Manhattan Links, the squared distance {p['distance2']}</title>"
        kind = shapes[p["cls"]]
        if kind == "circle":
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" class="mark {cls}">{title}</circle>')
        elif kind == "rect":
            parts.append(
                f'<rect x="{x - 4.5:.1f}" y="{y - 4.5:.1f}" width="9" height="9" class="mark {cls}">{title}</rect>'
            )
        elif kind == "diamond":
            parts.append(
                f'<polygon points="{x:.1f},{y - 6:.1f} {x + 6:.1f},{y:.1f} {x:.1f},{y + 6:.1f} {x - 6:.1f},{y:.1f}" class="mark {cls}">{title}</polygon>'
            )
        else:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" class="mark {cls}">{title}</circle>'
            )
    lx = left + 8
    for cls, word in CLASS_WORD.items():
        parts.append(f'<circle cx="{lx + 5}" cy="{top + 10}" r="4" class="mark {CLASS_MARK[cls]}"/>')
        parts.append(_text(lx + 14, top + 14, word, "t-small"))
        lx += 140
    return _svg(
        width,
        height,
        "".join(parts),
        "DETECTOR",
        "the distance to the face against the age, every click a point",
    )


def block(fig: dict[str, Any]) -> str:
    n, cell, side = 9, 26, int(fig["side"])
    ox, oy = 10, 10
    parts = []
    start = (n - side) // 2
    for i in range(n):
        for j in range(n):
            inside = start <= i < start + side and start <= j < start + side
            parts.append(
                f'<rect x="{ox + i * cell}" y="{oy + j * cell}" width="{cell - 2}" height="{cell - 2}" class="{"cell-well" if inside else "cell-medium"}"/>'
            )
    x0 = ox + n * cell + 24
    parts.append(_text(x0, 30, "the medium: every Node carries the pair " + fig["medium"], "t-small"))
    parts.append(
        _text(
            x0,
            52,
            f"the block R, side s = {side}: its cells carry the lowered pair " + fig["well"],
            "t-small",
        )
    )
    parts.append(
        _text(x0, 74, "the object's record: the bound mode in the well; its clock the mode", "t-small")
    )
    parts.append(
        _text(
            x0,
            96,
            "its momentum P: one integer per axis for the whole block, with its remainder",
            "t-small",
        )
    )
    parts.append(_text(x0, 118, "its click: the evaluation E across R, in its own clock", "t-small"))
    parts.append(_text(x0, 150, "DECLARATION; not built, not on main", "t-small"))
    return _svg(
        x0 + 470,
        oy + n * cell + 10,
        "".join(parts),
        "DECLARATION",
        "a foreign object as a block of cells with a lowered pair in a medium",
    )


ROLE_CLASS = {
    "an emitter (a lamp)": "obj-lamp",
    "a re-emitter (an opening or a splitter)": "obj-reemit",
    "a detector's body (a set of one Node)": "obj-detector",
    "a wall's body (an absorber)": "obj-wall",
}


def plane(fig: dict[str, Any]) -> str:
    shape = fig["shape"]
    w, h = 600, 300
    ex, ey = max(shape[0] - 1, 1), max(shape[1] - 1, 1)
    parts = [f'<rect x="10" y="10" width="{w - 20}" height="{h - 60}" class="face"/>']
    cw = max((w - 20) / (ex + 1), 2)
    ch = max((h - 60) / (ey + 1), 2)
    for obj in fig["objects"]:
        px, py = obj["position"][0], obj["position"][1]
        x = 10 + (w - 20) * px / (ex + 1)
        y = 10 + (h - 60) - (h - 60) * (py + 1) / (ey + 1)
        cls = ROLE_CLASS.get(obj["role"], "obj-wall")
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(cw, 3):.1f}" height="{max(ch, 3):.1f}" class="{cls}"><title>{escape(obj["role"])}, {escape(obj["family"])} at ({obj["position"][0]}, {obj["position"][1]}, {obj["position"][2]})</title></rect>'
        )
    lx = 10
    for role, cls in ROLE_CLASS.items():
        parts.append(f'<rect x="{lx}" y="{h - 36}" width="10" height="10" class="{cls}"/>')
        parts.append(_text(lx + 14, h - 27, role, "t-small"))
        lx += 150
    parts.append(
        _text(
            10,
            h - 6,
            f"the plane x from 0 to {shape[0] - 1}, y from 0 to {shape[1] - 1}, as the world file declares it",
            "t-small",
        )
    )
    return _svg(w, h, "".join(parts), "DECLARATION", "the declared objects on the plane")


def store(fig: dict[str, Any]) -> str:
    shape = fig["shape"]
    nodes = fig["nodes"]
    w, h = 600, 300
    ex, ey = max(shape[0] - 1, 1), max(shape[1] - 1, 1)
    top = max([n["amount"] for n in nodes] + [1])
    parts = [f'<rect x="10" y="10" width="{w - 20}" height="{h - 40}" class="face"/>']
    cw = max((w - 20) / (ex + 1), 2)
    ch = max((h - 40) / (ey + 1), 2)
    for n in nodes:
        px, py = n["position"][0], n["position"][1]
        x = 10 + (w - 20) * px / (ex + 1)
        y = 10 + (h - 40) - (h - 40) * (py + 1) / (ey + 1)
        opacity = 0.25 + 0.75 * n["amount"] / top
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(cw, 3):.1f}" height="{max(ch, 3):.1f}" class="store-node" style="opacity:{opacity:.2f}"><title>the Node ({n["position"][0]}, {n["position"][1]}, {n["position"][2]}): amount {n["amount"]}</title></rect>'
        )
    parts.append(
        _text(
            10,
            h - 8,
            f"GAMEBOARD, a diagnostic: {len(nodes)} Nodes holding rows at the last interval; the darkest holds {top} units",
            "t-small",
        )
    )
    return _svg(w, h, "".join(parts), "GAMEBOARD", "the store at the last interval")


# --- layer 3 ----------------------------------------------------------------


def bars(fig: dict[str, Any]) -> str:
    items = list(fig["bars"])
    top = max([b["count"] for b in items] + [1])
    n = max(len(items), 1)
    width, height, left, bottom, up = max(640, 6 * n + 80), 220, 40, 170, 20
    slot = (width - left - 20) / n
    parts = [f'<line x1="{left}" y1="{bottom}" x2="{width - 20}" y2="{bottom}" class="line"/>']
    for k in range(0, top + 1, max(1, top // 4)):
        y = bottom - (bottom - up) * k / top
        parts.append(_text(left - 6, y + 4, str(k), "t-small", "end"))
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - 20}" y2="{y:.1f}" class="grid"/>')
    step = max(1, len(items) // 12)
    for i, b in enumerate(items):
        x = left + slot * i + slot * 0.2
        hgt = (bottom - up) * b["count"] / top
        parts.append(
            f'<rect x="{x:.1f}" y="{bottom - hgt:.1f}" width="{max(slot * 0.6, 2):.1f}" height="{hgt:.1f}" '
            f'rx="2" class="bar"><title>{escape(str(b["name"]))}: {b["count"]}</title></rect>'
        )
        if i % step == 0:
            parts.append(_text(x + slot * 0.3, bottom + 14, str(b["name"]), "t-tiny", "middle"))
    others = ", ".join(f"{o['name']} {o['count']}" for o in fig.get("others", []))
    parts.append(
        _text(
            left,
            height - 6,
            "one bar per declared set, the count of gathers whose chosen set it is; beside the sets: "
            + others,
            "t-small",
        )
    )
    return _svg(width, height, "".join(parts), "DETECTOR", "the clicks per declared set")


def _stair(series: dict[str, Any], axis: str, axis_kind: str) -> str:
    ticks = series["ticks"]
    width, height, left, bottom, up = 640, 220, 48, 180, 16
    span = max(ticks[-1] if ticks else 1, 1)
    total = max(len(ticks), 1)

    def x_of(t: float) -> float:
        return left + (width - left - 20) * t / span

    def y_of(c: float) -> float:
        return bottom - (bottom - up) * c / total

    body = [
        f'<line x1="{left}" y1="{bottom}" x2="{width - 20}" y2="{bottom}" class="line"/>',
        f'<line x1="{left}" y1="{up}" x2="{left}" y2="{bottom}" class="line"/>',
    ]
    path = [f"M {x_of(0):.1f} {y_of(0):.1f}"]
    for count, t in enumerate(ticks, start=1):
        path.append(f"L {x_of(t):.1f} {y_of(count - 1):.1f} L {x_of(t):.1f} {y_of(count):.1f}")
    body.append(f'<path d="{" ".join(path)}" class="stair"/>')
    for count, t in enumerate(ticks, start=1):
        body.append(
            f'<circle cx="{x_of(t):.1f}" cy="{y_of(count):.1f}" r="3" class="mark-detector">'
            f"<title>the click {count} at {t}</title></circle>"
        )
    for k in range(5):
        t = span * k / 4
        body.append(_text(x_of(t), bottom + 16, f"{t:.0f}", "t-small", "middle", axis_kind))
    for k in range(0, total + 1, max(1, total // 4)):
        body.append(_text(left - 6, y_of(k) + 4, str(k), "t-small", "end"))
    body.append(
        _text(
            left,
            height - 6,
            series["name"] + ": the count of clicks (DETECTOR) against " + axis.split(";")[0],
            "t-small",
        )
    )
    return _svg(width, height, "".join(body), "DETECTOR", "the count of clicks against the clock")


def staircase(fig: dict[str, Any]) -> str:
    parts = []
    for index, series in enumerate(fig["series"]):
        hidden = "" if index == 0 else " hidden"
        parts.append(
            f'<div class="stair-series" data-series="{escape(series["name"])}"{hidden}>'
            + _stair(series, fig["axis"], fig["axis_kind"])
            + "</div>"
        )
    return "".join(parts)


def histogram(fig: dict[str, Any]) -> str:
    values = list(fig["values"])
    counts: dict[int, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    keys = sorted(counts)
    top = max(counts.values()) if counts else 1
    width, height, left, bottom, up = 640, 200, 40, 150, 16
    n = max(len(keys), 1)
    slot = (width - left - 20) / n
    parts = [f'<line x1="{left}" y1="{bottom}" x2="{width - 20}" y2="{bottom}" class="line"/>']
    for i, k in enumerate(keys):
        x = left + slot * i + slot * 0.2
        hgt = (bottom - up) * counts[k] / top
        parts.append(
            f'<rect x="{x:.1f}" y="{bottom - hgt:.1f}" width="{max(slot * 0.6, 2):.1f}" height="{hgt:.1f}" rx="2" class="bar"><title>the interval {k}: {counts[k]} times</title></rect>'
        )
        parts.append(_text(x + slot * 0.3, bottom + 14, str(k), "t-small", "middle"))
        parts.append(_text(x + slot * 0.3, bottom - hgt - 4, str(counts[k]), "t-tiny", "middle"))
    parts.append(
        _text(
            left,
            height - 6,
            f"the interval between consecutive clicks, in units of the {fig['axis_kind']} axis; how many times each",
            "t-small",
        )
    )
    return _svg(width, height, "".join(parts), "CONVERSION", "the intervals between clicks")


FIGURES = {
    "boards": boards,
    "node_ports": node_ports,
    "state_vector": state_vector,
    "translation": translation,
    "phase_plane": phase_plane,
    "split": split,
    "ladder": ladder,
    "light_rule": light_rule,
    "cube_net": cube_net,
    "pace": pace,
    "block": block,
    "plane": plane,
    "store": store,
    "bars": bars,
    "staircase": staircase,
    "histogram": histogram,
}


def figure(fig: dict[str, Any]) -> str:
    """The picture of one panel's figure data, or an empty string for a
    figure this module does not draw (the stages, drawn as HTML by the page)."""
    kind = fig.get("kind")
    drawer = FIGURES.get(str(kind))
    return drawer(fig) if drawer is not None else ""


# --- the GameBoard in 3-D (DESIGN_3D.md section 3) ---------------------------


def _project(x: float, y: float, z: float, yaw: float, pitch: float) -> tuple[float, float, float]:
    """The same orthographic projection as `board3d.project` and the page's
    script: yaw about z, then a tilt; (u, v, depth), v downwards."""
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    x1 = x * cy - y * sy
    y1 = x * sy + y * cy
    return (x1, -(y1 * sp + z * cp), y1 * cp - z * sp)


def board3d(fig: dict[str, Any]) -> str:
    """The pre-rendered board at the last interval in the default view: the
    box, the open faces, the cells, the objects as cubes, the marks (every
    tick, each carrying `data-tick` so the script can show and hide), the
    snapshot's cells shaded by their value. Floats in drawing coordinates."""
    board = fig["board"]
    x_n, y_n, z_n = (max(int(v), 1) for v in board["shape"])
    yaw, pitch = 0.62, 0.42
    corners = [(x, y, z) for x in (0, x_n) for y in (0, y_n) for z in (0, z_n)]
    projected = [_project(*c, yaw, pitch) for c in corners]
    u_min = min(p[0] for p in projected)
    u_max = max(p[0] for p in projected)
    v_min = min(p[1] for p in projected)
    v_max = max(p[1] for p in projected)
    width, height, pad = 760, 460, 36
    scale = min(
        (width - 2 * pad) / max(u_max - u_min, 1e-9), (height - 2 * pad) / max(v_max - v_min, 1e-9)
    )

    def at(x: float, y: float, z: float) -> tuple[float, float, float]:
        u, v, d = _project(x, y, z, yaw, pitch)
        return (pad + (u - u_min) * scale, pad + (v - v_min) * scale, d)

    items: list[tuple[float, str]] = []
    # the open faces, translucent
    for face in board["faces"]:
        axis = "xyz".index(face["axis"])
        fixed = [x_n, y_n, z_n][axis] if face["positive"] else 0
        others = [i for i in range(3) if i != axis]
        ext = [x_n, y_n, z_n]
        quad = []
        for a, b in ((0, 0), (ext[others[0]], 0), (ext[others[0]], ext[others[1]]), (0, ext[others[1]])):
            point = [0.0, 0.0, 0.0]
            point[axis] = fixed
            point[others[0]] = a
            point[others[1]] = b
            quad.append(at(*point))
        depth = sum(q[2] for q in quad) / 4
        points = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in quad)
        items.append(
            (
                depth - 0.5,
                f'<polygon points="{points}" class="b-face"><title>{escape(face["name"])}, an open face, a detector</title></polygon>',
            )
        )
    # the box's edges
    edges = [
        ((0, 0, 0), (x_n, 0, 0)),
        ((0, y_n, 0), (x_n, y_n, 0)),
        ((0, 0, z_n), (x_n, 0, z_n)),
        ((0, y_n, z_n), (x_n, y_n, z_n)),
        ((0, 0, 0), (0, y_n, 0)),
        ((x_n, 0, 0), (x_n, y_n, 0)),
        ((0, 0, z_n), (0, y_n, z_n)),
        ((x_n, 0, z_n), (x_n, y_n, z_n)),
        ((0, 0, 0), (0, 0, z_n)),
        ((x_n, 0, 0), (x_n, 0, z_n)),
        ((0, y_n, 0), (0, y_n, z_n)),
        ((x_n, y_n, 0), (x_n, y_n, z_n)),
    ]
    for a, b in edges:
        pa, pb = at(*a), at(*b)
        axis = next(i for i in range(3) if a[i] != b[i])
        cls = "b-edge-periodic" if board["axes"][axis]["periodic"] else "b-edge"
        items.append(
            (
                (pa[2] + pb[2]) / 2 - 1.0,
                f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" class="{cls}"/>',
            )
        )
    # the snapshot's cells, shaded by value
    cells = board["snapshot"]["cells"]
    if cells:
        top = max(abs(c[3]) for c in cells) or 1
        for x, y, z, value in cells:
            p = at(x + 0.5, y + 0.5, z + 0.5)
            r = 1.2 + 2.2 * min(abs(value) / top, 1.0) * scale / max(scale, 1)
            items.append(
                (
                    p[2],
                    f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{max(r, 1.2):.1f}" class="{"b-cell-neg" if value < 0 else "b-cell"}" opacity="{0.25 + 0.7 * min(abs(value) / top, 1.0):.2f}"><title>({x}, {y}, {z}): {value}, GAMEBOARD</title></circle>',
                )
            )
    # the detectors' cells
    for cell in board["cells"]:
        for node in cell["nodes"]:
            p = at(node[0] + 0.5, node[1] + 0.5, node[2] + 0.5)
            cls = {
                "detector": "b-det",
                "emitter": "b-lamp",
                "block": "b-blockcell",
                "body": "b-body",
            }.get(cell["role"], "b-body")
            items.append(
                (
                    p[2],
                    f'<rect x="{p[0] - 3:.1f}" y="{p[1] - 3:.1f}" width="6" height="6" class="{cls}"><title>{escape(cell["name"])}, {escape(cell["role"])} at ({node[0]}, {node[1]}, {node[2]}), DECLARATION</title></rect>',
                )
            )
    # the objects as cubes at their last recorded position
    for obj in board["objects"]:
        tick, node = obj["positions"][-1]
        size = [obj["side"]] * 3 if obj["side"] else obj["span"]
        origin = list(node) if obj["side"] else [node[i] - (size[i] - 1) // 2 for i in range(3)]
        c = [
            (origin[0] + dx, origin[1] + dy, origin[2] + dz)
            for dx in (0, size[0])
            for dy in (0, size[1])
            for dz in (0, size[2])
        ]
        faces_idx = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
        for f in faces_idx:
            quad = [at(*c[i]) for i in f]
            depth = sum(q[2] for q in quad) / 4
            points = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in quad)
            items.append(
                (
                    depth,
                    f'<polygon points="{points}" class="b-cube"><title>{escape(obj["name"])} at ({node[0]}, {node[1]}, {node[2]}) from its line at t = {tick}, GAMEBOARD</title></polygon>',
                )
            )
    # the marks, every tick, with data-tick for the script
    last = board["ticks"]
    for tick, event, x, y, z, kind in board["marks"]:
        p = at(x + 0.5, y + 0.5, z + 0.5)
        age = max(0, min(last - tick, 40))
        opacity = 0.9 - 0.02 * age
        cls = "b-mark-det" if kind == "DETECTOR" else "b-mark"
        items.append(
            (
                p[2] + 0.01,
                f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.6" class="{cls}" opacity="{opacity:.2f}" data-tick="{tick}"><title>{escape(event)} at ({x}, {y}, {z}), t = {tick}, {kind}</title></circle>',
            )
        )
    items.sort(key=lambda item: item[0], reverse=True)
    body = "".join(html for _depth, html in items)
    # the axes' names at the box's far corners
    labels = []
    for axis, (name, extent) in enumerate(zip(("x", "y", "z"), (x_n, y_n, z_n), strict=True)):
        end = [0.0, 0.0, 0.0]
        end[axis] = extent + 0.5
        p = at(*end)
        labels.append(_text(p[0], p[1], f"{name} = {extent}", "t-small", "middle", "DECLARATION"))
    origin = at(-0.3, -0.3, -0.3)
    labels.append(_text(origin[0], origin[1], "(0, 0, 0)", "t-tiny", "middle", "DECLARATION"))
    label = f"the GameBoard in 3-D at the last interval, {board['form']}, GAMEBOARD, a diagnostic"
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}" data-kind="GAMEBOARD" class="figure" data-board-svg>'
        f"<g data-board-drawn>{body}</g>{''.join(labels)}</svg>"
    )


FIGURES["board3d"] = board3d
