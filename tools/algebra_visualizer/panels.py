"""The panel models of the algebra visualizer: one model per panel of the
design (docs/designs/algebra_visualizer/DESIGN.md sections 2 to 4), built
from two run records and nothing else.

A panel carries its title, the algebra's lines it quotes (each with its
source section), its numbers (each a `Number`: a value, its kind and the
file and line it was read from) and the data of its picture. Every number
is one of the seven kinds: DETECTOR (a click or a count of a detector's
record), GAMEBOARD (the host's view of the board, a diagnostic), COMPUTATION
(a closed form or a worked example, no run), HOST (a cost or a fingerprint
of the machine), CONVERSION (an exact difference or ratio of two recorded
integers), DECLARATION (an input of the world file) and PIN (a register's
number written before the run, printed beside and never as a verdict). A
panel a run cannot fill says so in `missing` and carries no number.

Nothing of the law is computed here: the worked example of the light rule
(`LIGHT_RULE_EXAMPLE`) and the block's table (`BLOCK_TABLE`) are constants
declared in the design and labelled as such on the page.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

from record import (
    RunRecord,
    chosen_of,
    face_node,
    fraction,
    label_class,
    manhattan,
    squared_distance,
)

KINDS = ("DETECTOR", "GAMEBOARD", "COMPUTATION", "HOST", "CONVERSION", "DECLARATION", "PIN")

KIND_WORDS = {
    "DETECTOR": "a detector's reading: a click, a gather, a count of a detector's own record",
    "GAMEBOARD": "the host's view of the board, a diagnostic; compared with nothing",
    "COMPUTATION": "a closed form or a worked example; no run",
    "HOST": "a cost, a time or a fingerprint of the machine",
    "CONVERSION": "an exact difference or ratio of two recorded integers",
    "DECLARATION": "an input of the world file",
    "PIN": "the register's number, written before the run; printed beside, never a verdict",
}

# The worked example of the light rule (DESIGN.md section 2.5): the integers
# were written in the design before this tool existed and the test checks
# them against the two lines; the page labels them COMPUTATION, "not from a
# run". The rule itself is docs/designs/detector_law/DESIGN.md section 2 on
# the branch detector-law-design (not in the engine on main).
LIGHT_RULE_EXAMPLE: dict[str, Any] = {
    "neighbours": {"a_E": 7, "a_W": 5, "a_N": 4, "a_S": 2, "a_U": 3, "a_D": 1},
    "S_6": 22,
    "a_before": 4,
    "r": 1,
    "light": {"pair": (1, 1), "a_next": 3, "r_next": 2},
    "massive": {"pair": (2, 3), "a_next": 1, "r_next": 0},
}

# The block's declared pairs and their rest periods, from MASSIVE_RECORD.md
# section 2 on detector-law-design at b6131c64 (DECLARATION; not built).
BLOCK_TABLE: list[dict[str, Any]] = [
    {
        "self_pair": "[1, 64]",
        "pair": "[128, 129]",
        "omega_0": "0.1246",
        "period": "50.4",
        "pace": "0.9961",
    },
    {
        "self_pair": "[1, 16]",
        "pair": "[32, 33]",
        "omega_0": "0.2468",
        "period": "25.5",
        "pace": "0.9847",
    },
    {"self_pair": "[1, 4]", "pair": "[8, 9]", "omega_0": "0.4759", "period": "13.2", "pace": "0.9428"},
    {"self_pair": "[1, 1]", "pair": "[2, 3]", "omega_0": "0.8411", "period": "7.5", "pace": "0.8165"},
]
BLOCK_SOURCE = "docs/designs/detector_law/MASSIVE_RECORD.md section 2, detector-law-design at b6131c64"

PORT_ORDER = ("+x", "-x", "+y", "-y", "+z", "-z")


@dataclass(frozen=True)
class Number:
    """One number on the page: its label, its value as text, its kind and the
    file and line kind (or field) it was read from."""

    label: str
    value: str
    kind: str
    source: str

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError(f"unknown kind {self.kind!r} for {self.label!r}")
        if not self.source:
            raise ValueError(f"a number without a source: {self.label!r}")


@dataclass
class Panel:
    """One panel of the page."""

    key: str
    layer: int
    title: str
    algebra: list[tuple[str, str]] = field(default_factory=list)
    numbers: list[Number] = field(default_factory=list)
    figure: dict[str, Any] = field(default_factory=dict)
    note: str = ""
    missing: str | None = None


def vec(values: Any) -> str:
    return "(" + ", ".join(str(int(v)) for v in values) + ")"


def _boundary_text(boundary: Any) -> str:
    if boundary == "open":
        return "open on every axis"
    if isinstance(boundary, dict):
        return ", ".join(f"{axis} {kind}" for axis, kind in boundary.items()) + ", the other axes open"
    return str(boundary)


# --- the head ---------------------------------------------------------------


def head_numbers(run: RunRecord) -> list[Number]:
    meta = run.meta
    return [
        Number("the model identity", str(meta.get("model")), "DECLARATION", "run.json: model"),
        Number(
            "the world file's sha256",
            str(meta.get("initialization_sha256")),
            "HOST",
            "run.json: initialization_sha256",
        ),
        Number(
            "the engine's fingerprint", str(meta.get("source_sha256")), "HOST", "run.json: source_sha256"
        ),
        Number(
            "the intervals", str(meta.get("completed_ticks")), "GAMEBOARD", "run.json: completed_ticks"
        ),
        Number("the status", str(meta.get("status")), "HOST", "run.json: status"),
        Number(
            "the books balanced at every completed tick",
            str(meta.get("conserved_at_every_completed_tick")),
            "GAMEBOARD",
            "run.json: conserved_at_every_completed_tick",
        ),
        Number(
            "the runner's seconds",
            f"{float(meta.get('elapsed_seconds', 0.0)):.2f}",
            "HOST",
            "run.json: elapsed_seconds",
        ),
        Number(
            "per-row click lines left out",
            str(meta.get("omit_row_clicks")),
            "HOST",
            "run.json: omit_row_clicks",
        ),
    ]


# --- the record's helpers ---------------------------------------------------


def followed_record(run: RunRecord) -> dict[str, Any] | None:
    """The first `gather` line whose chosen set is a declared detector set
    (not a wall body, `measured:<n>`, and not a face): the record Layer 3
    follows and Layer 1 takes its instances from."""
    for gather in run.of_kind("gather"):
        chosen = gather.get("chosen")
        if not isinstance(chosen, list) or not chosen:
            continue
        name = str(chosen[0][0])
        if name.startswith("measured:") or name.startswith("face:"):
            continue
        return gather
    return None


def chosen_name(gather: dict[str, Any]) -> str:
    chosen = gather.get("chosen")
    if isinstance(chosen, list) and chosen:
        return str(chosen[0][0])
    return "none"


def chosen_kind(name: str) -> str:
    if name.startswith("measured:"):
        return "wall"
    if name.startswith("face:"):
        return "faces"
    return "screen"


def body_at(run: RunRecord, position: list[int]) -> dict[str, Any] | None:
    for body in run.bodies():
        if [int(v) for v in body.get("position", [])] == [int(v) for v in position]:
            return body
    return None


def object_role(entry: dict[str, Any], detector_positions: set[tuple[int, ...]]) -> str:
    if "lamp" in entry:
        return "an emitter (a lamp)"
    if "table" in entry:
        return "a re-emitter (an opening or a splitter)"
    if tuple(int(v) for v in entry.get("position", [])) in detector_positions:
        return "a detector's body (a set of one Node)"
    return "a wall's body (an absorber)"


# --- layer 1 ----------------------------------------------------------------


def panel_torus(light: RunRecord, detector: RunRecord) -> Panel:
    boards = []
    numbers = []
    for run in (light, detector):
        shape = [int(v) for v in run.meta["shape"]]
        boundary = run.meta.get("boundary")
        boards.append({"name": run.name, "shape": shape, "boundary": boundary})
        numbers.append(Number(f"{run.name}: the shape", vec(shape), "DECLARATION", "run.json: shape"))
        numbers.append(
            Number(
                f"{run.name}: the boundary",
                _boundary_text(boundary),
                "DECLARATION",
                "run.json: boundary",
            )
        )
    return Panel(
        key="torus",
        layer=1,
        title="The GameBoard as the torus",
        algebra=[
            (
                "The translation group Z_X x Z_Y x Z_Z per world: the GameBoard's extents per axis, each factor a circle (a periodic axis) or a segment (an open axis whose faces are the border, a click at the face detector).",
                "ALGEBRA.md 1.6",
            ),
            (
                "An open face of the GameBoard is a detector, named face:+x .. face:-z; a periodic axis has no faces.",
                "TERMINOLOGY.md, the location",
            ),
        ],
        numbers=numbers,
        figure={"kind": "boards", "boards": boards},
    )


def panel_node_ports() -> Panel:
    return Panel(
        key="node",
        layer=1,
        title="A Node and its six Ports",
        algebra=[
            (
                "The one choice of the model is the six Ports of a Node, +X, -X, +Y, -Y, +Z, -Z, with the opposite involution: a Node and its six neighbours, the seven Nodes of the causal front, one message per Link per interval.",
                "ALGEBRA.md 7 (i)",
            ),
            (
                "The 48 maps of the six Ports that send opposite Ports to opposite Ports are the symmetry; the determinant splits them into the 24 rotations, the group of order 24, and the 24 reflections, told apart by the hand.",
                "ALGEBRA.md 1.1, 1.4, 4.5",
            ),
        ],
        note="No number of a run is here: the Port order is the constant of TERMINOLOGY.md, carried as text.",
        figure={"kind": "node_ports", "ports": list(PORT_ORDER)},
    )


def panel_state_vector(light: RunRecord, detector: RunRecord) -> Panel:
    numbers: list[Number] = []
    rows = detector.nodes_with_rows()
    row_run = detector
    if not rows:
        rows = light.nodes_with_rows()
        row_run = light
    if rows:
        node = rows[0]
        family = node["families"][0]
        ray = family["rays"][0]
        src = "state.json: nodes[].families[].rays[]"
        numbers += [
            Number(f"{row_run.name}: a row's Node x", vec(node["position"]), "GAMEBOARD", src),
            Number("its family", str(family["family"]), "GAMEBOARD", src),
            Number("its direction D", vec(ray["direction"]), "GAMEBOARD", src),
            Number("its age tau", str(ray["age"]), "GAMEBOARD", src),
            Number("its phase", str(ray["phase"]), "GAMEBOARD", src),
            Number("its amount", str(ray["amount"]), "GAMEBOARD", src),
            Number("its content per unit", str(ray["content"]), "GAMEBOARD", src),
            Number("its number", str(ray["number"]), "GAMEBOARD", src),
            Number("its record's identity", str(ray.get("record")), "GAMEBOARD", src),
            Number("its birth wheel u", str(ray.get("u")), "GAMEBOARD", src),
        ]
    bodies = detector.bodies() or light.bodies()
    if bodies:
        body = bodies[0]
        src = "state.json: measured[]"
        acc = body.get("acc", {})
        numbers += [
            Number("a body's Node", vec(body["position"]), "GAMEBOARD", src),
            Number("its momentum p", vec(body["momentum"]), "GAMEBOARD", src),
            Number("its content M", str(body["content"]), "GAMEBOARD", src),
            Number("its phase", str(body["phase"]), "GAMEBOARD", src),
            Number("its clock (age, its own count)", str(body["age"]), "GAMEBOARD", src),
            Number("its owed count", str(body["owed"]), "GAMEBOARD", src),
            Number("its steps", str(body["steps"]), "GAMEBOARD", src),
            Number(
                "its accumulator acc.owed",
                str(acc.get("owed")),
                "GAMEBOARD",
                "state.json: measured[].acc",
            ),
            Number(
                "its accumulator acc.turn",
                str(acc.get("turn")),
                "GAMEBOARD",
                "state.json: measured[].acc",
            ),
            Number(
                "its accumulator acc.lamp",
                str(acc.get("lamp")),
                "GAMEBOARD",
                "state.json: measured[].acc",
            ),
        ]
    return Panel(
        key="state",
        layer=1,
        title="A record's state vector",
        algebra=[
            (
                "On a record's state vector (x, D, p, tau, f, acc_drive, acc_push, acc_owed) the lines of one interval are the hop, the phase, the push, the crowd, the split, the sum, the click and the age, each one of the six verbs on bounded integers.",
                "ALGEBRA.md 2.11",
            ),
            (
                "Each component of the state is a bounded integer accumulator with a declared rate and a declared wall; every wall counted is an event and nothing else happens.",
                "ALGEBRA.md 2",
            ),
        ],
        note="The store's view at the last interval, a diagnostic: one row of the snapshot and one body of the snapshot.",
        numbers=numbers,
        figure={
            "kind": "state_vector",
            "components": ["x", "D", "p", "tau", "f", "acc_drive", "acc_push", "acc_owed"],
        },
        missing=None if numbers else "no row and no body in either snapshot",
    )


def panel_verb_t(light: RunRecord) -> Panel:
    births = light.of_kind("birth", "giving")
    clicks = [c for c in light.of_kind("click") if str(c.get("detector", "")).startswith("face:")]
    if not births or not clicks:
        return Panel(
            "verb_t",
            1,
            "(T) The translation of an accumulator by its rate",
            missing="no birth and face click in the light run; the line that would show it is a birth line and a face click line of one row",
        )
    birth = births[0]
    click = next((c for c in clicks if c.get("record") == birth.get("record")), clicks[0])
    age = int(click["tick"]) - int(birth["tick"])
    links = manhattan(click["node"], birth["node"]) + 1
    numbers = [
        Number("the birth's tick", str(birth["tick"]), "DETECTOR", "events.jsonl: birth.tick"),
        Number("the birth's Node", vec(birth["node"]), "DETECTOR", "events.jsonl: birth.node"),
        Number("the birth wheel u", str(birth["u"]), "DETECTOR", "events.jsonl: birth.u"),
        Number("the click's tick", str(click["tick"]), "DETECTOR", "events.jsonl: click.tick"),
        Number("the click's Node", vec(click["node"]), "DETECTOR", "events.jsonl: click.node"),
        Number("the face", str(click["detector"]), "DETECTOR", "events.jsonl: click.detector"),
        Number("the phase at the click", str(click["phase"]), "DETECTOR", "events.jsonl: click.phase"),
        Number(
            "the label (the direction's unit vector at the scale Q)",
            vec(click["momentum"]),
            "DETECTOR",
            "events.jsonl: click.momentum",
        ),
        Number(
            "the age at the click, tick less tick", str(age), "CONVERSION", "click.tick - birth.tick"
        ),
        Number(
            "the Links crossed, the Manhattan difference plus the face's step",
            str(links),
            "CONVERSION",
            "|click.node - birth.node|_1 + 1",
        ),
    ]
    return Panel(
        key="verb_t",
        layer=1,
        title="(T) The translation of an accumulator by its rate",
        algebra=[
            (
                "x -> x + r on Z^k or on a torus; every count of the law is this: the flight on the digital line, the phase's turn, the age, the drive, the owed count.",
                "ALGEBRA.md 2.1",
            ),
            (
                "On a row the flight's accumulator gains 2 S_1 Q per interval against the wall 2 T_D (the flight's pair, the engine's table, not loaded here); the Links a row has crossed by the age tau are its count.",
                "ALGEBRA.md 2.1, 4.1",
            ),
        ],
        numbers=numbers,
        figure={
            "kind": "translation",
            "age": age,
            "links": links,
            "birth": birth["node"],
            "node": click["node"],
            "face": click["detector"],
        },
    )


def panel_verb_b(detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    offers = [
        line
        for line in detector.of_kind("record")
        if line.get("reading") == "sum" and (gather is None or line.get("of") == gather.get("record"))
    ]
    if not offers:
        return Panel(
            "verb_b",
            1,
            "(B) The bilinear form with a declared matrix",
            missing="no record line under the reading sum in the detector run; the line that would show it is a set's record line with its pointer and its square",
        )
    line = offers[0]
    x, y = (int(v) for v in line["pointer"])
    numbers = [
        Number("the set", str(line["detector"]), "DETECTOR", "events.jsonl: record.detector"),
        Number("the record's identity", str(line["of"]), "DETECTOR", "events.jsonl: record.of"),
        Number("the pointer X", str(x), "DETECTOR", "events.jsonl: record.pointer"),
        Number("the pointer Y", str(y), "DETECTOR", "events.jsonl: record.pointer"),
        Number(
            "the square X^2 + Y^2, as recorded",
            str(line["record"]),
            "DETECTOR",
            "events.jsonl: record.record",
        ),
        Number(
            "the multiplicity",
            str(line["multiplicity"]),
            "DETECTOR",
            "events.jsonl: record.multiplicity",
        ),
        Number("the label", str(line.get("label")), "DETECTOR", "events.jsonl: record.label"),
    ]
    return Panel(
        key="verb_b",
        layer=1,
        title="(B) The bilinear form with a declared matrix",
        algebra=[
            (
                "The click's weight is this form on the record's element: f^T G f with G = E^T E, nothing squared as a step of its own; the push on a body is this form too, the reader's content times the flow.",
                "ALGEBRA.md 2.2",
            ),
        ],
        note="The page draws the recorded pointer and prints the recorded square; it squares nothing. No body is pushed in either run; the line that would show the push is a step line's momentum beside the body's pushed.",
        numbers=numbers,
        figure={"kind": "phase_plane", "pointers": [{"name": str(line["detector"]), "x": x, "y": y}]},
    )


def panel_verb_g(detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    if gather is None:
        return Panel(
            "verb_g",
            1,
            "(G) The group-ring addition: the merge and the cancel",
            missing="no gather in the detector run; the lines that would show it are one record's offers and its gather's weight and total",
        )
    identity = gather["record"]
    offers = [line for line in detector.of_kind("record") if line.get("of") == identity]
    cancels = detector.of_kind("cancel")
    numbers = [
        Number("the record's identity", str(identity), "DETECTOR", "events.jsonl: gather.record"),
        Number(
            "its offers (record lines) at the sets",
            str(len(offers)),
            "DETECTOR",
            "events.jsonl: record.of",
        ),
        Number(
            "the gather's weight (the chosen cell's, a pair)",
            str(gather["weight"]),
            "DETECTOR",
            "events.jsonl: gather.weight",
        ),
        Number(
            "the gather's total (the sum the layer made, a pair)",
            str(gather["total"]),
            "DETECTOR",
            "events.jsonl: gather.total",
        ),
        Number(
            "cancel lines in the run (an antiphase pair leaving nothing)",
            str(len(cancels)),
            "DETECTOR",
            "events.jsonl: cancel",
        ),
    ]
    pointers = [
        {"name": str(line["detector"]), "x": int(line["pointer"][0]), "y": int(line["pointer"][1])}
        for line in offers[:12]
    ]
    return Panel(
        key="verb_g",
        layer=1,
        title="(G) The group-ring addition: the merge and the cancel",
        algebra=[
            (
                "A record's rows at one Node and label are one element f of Z[Z_N]; the merge of identical rows is the ring's addition, f <- f + g, with the cancel [p + N/2] = -[p] (an antiphase row subtracts; an equal antipodal pair leaves nothing).",
                "ALGEBRA.md 2.3",
            ),
        ],
        note="The offers of one record, each a pointer at a set, and the total the layer summed, recorded on the gather line; the page adds nothing. The first twelve offers are drawn.",
        numbers=numbers,
        figure={"kind": "phase_plane", "pointers": pointers},
    )


def panel_verb_p(detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    splits = detector.of_kind("split")
    if gather is not None:
        own = [s for s in splits if s.get("record") == gather.get("record")]
        splits = own or splits
    if not splits:
        return Panel(
            "verb_p",
            1,
            "(P) The permutation of the joint state",
            missing="no split line in the detector run; the collision writes no line (a store operation between rows of one number)",
        )
    split = splits[0]
    numbers = [
        Number("the tick", str(split["tick"]), "DETECTOR", "events.jsonl: split.tick"),
        Number("the Node (the re-emitter)", vec(split["node"]), "DETECTOR", "events.jsonl: split.node"),
        Number(
            "the row in (absorbed)", str(split["absorbed"]), "DETECTOR", "events.jsonl: split.absorbed"
        ),
        Number("the rows out (born)", str(split["born"]), "DETECTOR", "events.jsonl: split.born"),
        Number(
            "the multiplicity after",
            str(split["multiplicity"]),
            "DETECTOR",
            "events.jsonl: split.multiplicity",
        ),
        Number("the birth wheel u, carried", str(split["u"]), "DETECTOR", "events.jsonl: split.u"),
    ]
    return Panel(
        key="verb_p",
        layer=1,
        title="(P) The permutation of the joint state",
        algebra=[
            (
                "The collision: per class the single units in the eight slots are permuted, the forward map the cyclic shift; the gate; the apportioning's tie. A permutation of directions, labels or Nodes, never of contents.",
                "ALGEBRA.md 2.4",
            ),
            (
                "The split: P, B, D, T (one row in, the fan out with the declared weights and turns).",
                "COUPLINGS.md, the split's row (ALGEBRA.md 2.9)",
            ),
        ],
        note="The collision writes no line in either run (a store operation between rows of one number); the split line at an opening is the permutation these runs record.",
        numbers=numbers,
        figure={"kind": "split", "born": int(split["born"]), "absorbed": int(split["absorbed"])},
    )


def panel_verb_e(detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    if gather is None:
        return Panel(
            "verb_e",
            1,
            "(E) The evaluation at the roots of unity: the click's pointer",
            missing="no gather in the detector run",
        )
    name = chosen_name(gather)
    offer = next(
        (
            line
            for line in detector.of_kind("record")
            if line.get("of") == gather["record"] and line.get("detector") == name
        ),
        None,
    )
    numbers = [
        Number("the wheel's value u", str(gather["u"]), "DETECTOR", "events.jsonl: gather.u"),
        Number(
            "the detectors (the rungs of the ladder)",
            str(len(gather.get("detectors", gather.get("cells", [])))),
            "DETECTOR",
            "events.jsonl: gather.detectors",
        ),
        Number("the chosen set", name, "DETECTOR", "events.jsonl: gather.chosen"),
        Number("the chosen Node", vec(gather["node"][0]), "DETECTOR", "events.jsonl: gather.node"),
        Number("the weight (a pair)", str(gather["weight"]), "DETECTOR", "events.jsonl: gather.weight"),
        Number("the total (a pair)", str(gather["total"]), "DETECTOR", "events.jsonl: gather.total"),
        Number("T, the norm", str(gather["T"]), "DETECTOR", "events.jsonl: gather.T"),
    ]
    pointers = []
    if offer is not None:
        x, y = (int(v) for v in offer["pointer"])
        numbers.append(
            Number(
                "the chosen set's pointer (X, Y)",
                f"({x}, {y})",
                "DETECTOR",
                "events.jsonl: record.pointer",
            )
        )
        pointers.append({"name": name, "x": x, "y": y})
    return Panel(
        key="verb_e",
        layer=1,
        title="(E) The evaluation at the roots of unity: the click's pointer",
        algebra=[
            (
                "The exact evaluation ev: Z[Z_N] -> Z[zeta_N] is a surjective ring homomorphism whose kernel is the merge's cancel; the built evaluation is the tables C and S at the scale 256, the pointer (X, Y) = E f, and the weight X^2 + Y^2 = f^T G f, then the ladder on the wheel.",
                "ALGEBRA.md 2.5",
            ),
        ],
        numbers=numbers,
        figure={"kind": "phase_plane", "pointers": pointers},
    )


def panel_verb_d(light: RunRecord, detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    numbers: list[Number] = []
    exact_click = next(
        (
            c
            for run in (light, detector)
            for c in run.of_kind("click")
            if "exact" in c and "remainder" in c
        ),
        None,
    )
    if exact_click is not None:
        numbers += [
            Number(
                "a face click's phase",
                str(exact_click["phase"]),
                "DETECTOR",
                "events.jsonl: click.phase",
            ),
            Number(
                "its exact phase at the last Link (the whole part)",
                str(exact_click["exact"]),
                "DETECTOR",
                "events.jsonl: click.exact",
            ),
            Number(
                "its remainder, kept (a pair)",
                str(exact_click["remainder"]),
                "DETECTOR",
                "events.jsonl: click.remainder",
            ),
        ]
    ladder: list[tuple[str, int]] = []
    if gather is not None:
        ladder = [
            (str(rung[0][0][0]), int(rung[1]))
            for rung in gather.get("detectors", gather.get("cells", []))
        ]
        numbers += [
            Number("the wheel's value u", str(gather["u"]), "DETECTOR", "events.jsonl: gather.u"),
            Number(
                "the first rung of the ladder",
                str(ladder[0][1]) if ladder else "none",
                "DETECTOR",
                "events.jsonl: gather.cells",
            ),
            Number(
                "the last rung of the ladder",
                str(ladder[-1][1]) if ladder else "none",
                "DETECTOR",
                "events.jsonl: gather.cells",
            ),
            Number(
                "the cell the comparison chose",
                chosen_name(gather),
                "DETECTOR",
                "events.jsonl: gather.chosen",
            ),
        ]
    if not numbers:
        return Panel(
            "verb_d",
            1,
            "(D) The division with the remainder kept, and the comparison",
            missing="no click with an exact phase and no gather in these runs",
        )
    return Panel(
        key="verb_d",
        layer=1,
        title="(D) The division with the remainder kept, and the comparison",
        algebra=[
            (
                "The count is the whole part the accumulator holds in units of the wall, that much is subtracted and the remainder stays, bounded below the wall; the comparison is part of this verb: the ladder's cell 2 T u + T <= 2 N C_k, an age against a key, a phase against a window.",
                "ALGEBRA.md 2.6",
            ),
        ],
        note="The ladder of one gather: the rungs in order and the wheel's value u; the first rung above u is the detector chosen, as recorded on the gather line.",
        numbers=numbers,
        figure={
            "kind": "ladder",
            "cells": ladder,
            "u": int(gather["u"]) if gather is not None else None,
            "N": int(detector.meta.get("N", 0)),
            "chosen": chosen_name(gather) if gather is not None else None,
        },
    )


def panel_light_rule() -> Panel:
    ex = LIGHT_RULE_EXAMPLE
    src = "constant: DESIGN.md section 2.5 (a worked example, not from a run)"
    numbers = [
        Number(f"the neighbour {name}", str(value), "COMPUTATION", src)
        for name, value in ex["neighbours"].items()
    ]
    numbers += [
        Number("S_6, the six-neighbour sum", str(ex["S_6"]), "COMPUTATION", src),
        Number("a_before", str(ex["a_before"]), "COMPUTATION", src),
        Number("r, the remainder before", str(ex["r"]), "COMPUTATION", src),
        Number("light, the pair [1, 1]: a_next", str(ex["light"]["a_next"]), "COMPUTATION", src),
        Number(
            "light, the pair [1, 1]: r', the remainder after",
            str(ex["light"]["r_next"]),
            "COMPUTATION",
            src,
        ),
        Number(
            "a massive kind, the pair [2, 3]: a_next", str(ex["massive"]["a_next"]), "COMPUTATION", src
        ),
        Number("a massive kind, the pair [2, 3]: r'", str(ex["massive"]["r_next"]), "COMPUTATION", src),
    ]
    return Panel(
        key="light_rule",
        layer=1,
        title="The light rule as one picture",
        algebra=[
            (
                "3 a_next + r' = S_6 - 3 a_before + r, 0 <= r' < 3: the six-neighbour sum the group-ring addition (G) over the six Ports, the division by 3 with the remainder kept the verb (D), the accumulator carrying r the translation (T).",
                "ALGEBRA_MASSIVE_RECORD.md 0.1; the rule of docs/designs/detector_law/DESIGN.md section 2 on detector-law-design",
            ),
            (
                "3 den a_next + r' = num S_6 - 3 den a_before + r, 0 <= r' < 3 den: the pair [num, den] on the six-neighbour term, [1, 1] the light rule bit for bit, den > num a massive record kind; the six-neighbour term one entry of verb (B)'s declared matrix.",
                "MASSIVE_RECORD.md section 1 on detector-law-design at b6131c64",
            ),
        ],
        note=(
            "A worked example, COMPUTATION; not from a run. The rule is docs/designs/detector_law on detector-law-design, "
            "not in the engine on main, and no run on main records a_now, a_before or r at a Node; when one does, this "
            "panel reads the record's row at a Node and its six neighbours and the example goes."
        ),
        numbers=numbers,
        figure={"kind": "light_rule", "example": ex},
    )


# --- layer 2 ----------------------------------------------------------------


def panel_fan_faces(light: RunRecord) -> Panel:
    births = light.of_kind("birth", "giving")
    clicks = [c for c in light.of_kind("click") if str(c.get("detector", "")).startswith("face:")]
    if not births or not clicks:
        return Panel(
            "fan",
            2,
            "A record propagating, read where it is read: at the faces",
            missing="no birth and no face click in the light run",
        )
    birth = births[0]
    marks = [
        {
            "face": str(c["detector"]),
            "node": [int(v) for v in c["node"]],
            "tick": int(c["tick"]),
            "cls": label_class(c["momentum"]),
        }
        for c in clicks
    ]
    ticks = sorted({m["tick"] for m in marks})
    by_class = Counter(m["cls"] for m in marks)
    first_tick_by_class = {cls: min(m["tick"] for m in marks if m["cls"] == cls) for cls in by_class}
    numbers = [
        Number("the birth's tick", str(birth["tick"]), "DETECTOR", "events.jsonl: birth.tick"),
        Number("the birth's Node", vec(birth["node"]), "DETECTOR", "events.jsonl: birth.node"),
        Number("the rows born (units)", str(birth["units"]), "DETECTOR", "events.jsonl: birth.units"),
        Number("the face clicks", str(len(marks)), "DETECTOR", "events.jsonl: click (detector face:*)"),
        Number("the first click's tick", str(ticks[0]), "DETECTOR", "events.jsonl: click.tick"),
        Number("the last click's tick", str(ticks[-1]), "DETECTOR", "events.jsonl: click.tick"),
    ]
    for cls in ("axes", "face_diagonals", "body_diagonals", "rest"):
        if cls in by_class:
            numbers.append(
                Number(
                    f"clicks of the {cls.replace('_', ' ')}",
                    str(by_class[cls]),
                    "DETECTOR",
                    "events.jsonl: click.momentum (the label's class)",
                )
            )
            numbers.append(
                Number(
                    f"first click of the {cls.replace('_', ' ')} at tick",
                    str(first_tick_by_class[cls]),
                    "DETECTOR",
                    "events.jsonl: click.tick",
                )
            )
    if light.register and isinstance(light.register.get("classes"), dict):
        for cls, entry in light.register["classes"].items():
            ages = entry.get("ages")
            if ages:
                numbers.append(
                    Number(
                        f"the register's ages of the {cls.replace('_', ' ')}",
                        ", ".join(str(a) for a in ages),
                        "PIN",
                        "expectations.json: classes.*.ages",
                    )
                )
    return Panel(
        key="fan",
        layer=2,
        title="A record propagating, read where it is read: at the faces",
        algebra=[
            (
                "A row advances c_D = Q |D|_2 / T_D Links per interval on its direction; S_1 Q <= T_D (the Manhattan bound, at most one Link per interval, equality on the body diagonals); an isotropic pace under it is at most the slowest line's, 1 / sqrt 3.",
                "ALGEBRA.md 4.2",
            ),
            (
                "The line from the emitter to the detector is the reader's inference after the click.",
                "HIGHLIGHTS.md 5.4, the line of record 1336",
            ),
        ],
        note=(
            "The runner writes the snapshot once, at the end, so the board's interior per interval is not recorded; the record "
            "is seen where it is read. The slider fills the faces in the order the clicks came; the faint lines from the birth "
            "Node are the reader's inference, not a recorded path."
        ),
        numbers=numbers,
        figure={
            "kind": "cube_net",
            "shape": [int(v) for v in light.meta["shape"]],
            "birth": [int(v) for v in birth["node"]],
            "clicks": marks,
            "ticks": ticks,
        },
    )


def panel_pace(light: RunRecord) -> Panel:
    births = light.of_kind("birth", "giving")
    clicks = [c for c in light.of_kind("click") if str(c.get("detector", "")).startswith("face:")]
    if not births or not clicks:
        return Panel(
            "pace",
            2,
            "The pace c from the three inputs",
            missing="no birth and no face click in the light run",
        )
    birth = births[0]
    origin = [int(v) for v in birth["node"]]
    points = []
    for c in clicks:
        outside = face_node(c)
        age = int(c["tick"]) - int(birth["tick"])
        points.append(
            {
                "age": age,
                "distance2": squared_distance(outside, origin),
                "links": manhattan(outside, origin),
                "cls": label_class(c["momentum"]),
            }
        )
    numbers: list[Number] = []
    for cls in ("axes", "face_diagonals", "body_diagonals", "rest"):
        own = [p for p in points if p["cls"] == cls]
        if not own:
            continue
        ages = sorted({p["age"] for p in own})
        links = sorted({p["links"] for p in own})
        ratios = sorted({Fraction(p["links"], p["age"]) for p in own})
        label = cls.replace("_", " ")
        numbers.append(
            Number(
                f"{label}: the ages at the click",
                ", ".join(str(a) for a in ages),
                "DETECTOR",
                "events.jsonl: click.tick - birth.tick",
            )
        )
        numbers.append(
            Number(
                f"{label}: the Links to the face's outside Node",
                ", ".join(str(a) for a in links),
                "CONVERSION",
                "|face_node - birth.node|_1",
            )
        )
        numbers.append(
            Number(
                f"{label}: Manhattan Links per interval, exact",
                ", ".join(str(r) for r in ratios[:6]) + (" ..." if len(ratios) > 6 else ""),
                "CONVERSION",
                "links / age",
            )
        )
        if (
            light.register
            and isinstance(light.register.get("classes"), dict)
            and cls in light.register["classes"]
        ):
            pace = light.register["classes"][cls].get("pace", {})
            if isinstance(pace, dict) and "mean" in pace:
                numbers.append(
                    Number(
                        f"{label}: the register's Euclidean pace, mean",
                        str(pace["mean"]),
                        "PIN",
                        "expectations.json: classes.*.pace.mean",
                    )
                )
    if light.register and "c" in light.register:
        numbers.append(
            Number("the register's c", str(light.register["c"]), "PIN", "expectations.json: c")
        )
    numbers.append(
        Number("c = 1 / sqrt 3, the flight operator's norm", "0.57735", "COMPUTATION", "ALGEBRA.md 4.2")
    )
    return Panel(
        key="pace",
        layer=2,
        title="The pace c from the three inputs",
        algebra=[
            (
                "The three inputs, and no more: locality with the 48 (the six neighbours enter with one weight, so near k = 0 the pace is one number in every direction); the zero mode (a uniform record is a solution); the absent self term (s = 0 picks w = 1 / 3). So c^2 = 1 / 3, c = 1 / sqrt 3 Links per interval: a consequence, not a free constant.",
                "MASSIVE_RECORD.md 1.1 on detector-law-design (derived, not declared)",
            ),
            (
                "c was not chosen: it is the norm of the flight operator, 1 / sqrt 3, from locality and straightness.",
                "ALGEBRA.md 1.3 (5), 4.2",
            ),
            (
                "A negative result: the constancy of c is not a theorem of the six verbs; on the engine as built it is the declared postulate P9 (the flight table indexed by direction and age).",
                "ALGEBRA.md 4.14",
            ),
        ],
        note=(
            "Every click of the light run as a point: the Euclidean distance from the birth Node to the Node outside the face "
            "(a drawing coordinate) against the age; the pace is the slope by eye; the line c = 1 / sqrt 3 is the algebra's, "
            "COMPUTATION. No verdict is printed."
        ),
        numbers=numbers,
        figure={"kind": "pace", "points": points, "c": 0.5773502691896258},
    )


def panel_block() -> Panel:
    numbers: list[Number] = []
    for row in BLOCK_TABLE:
        numbers.append(
            Number(
                f"the pair {row['pair']} (the self pair {row['self_pair']}): the rest frequency omega_0",
                row["omega_0"],
                "DECLARATION",
                BLOCK_SOURCE,
            )
        )
        numbers.append(
            Number(
                f"the pair {row['pair']}: the rest period N_0 in intervals",
                row["period"],
                "DECLARATION",
                BLOCK_SOURCE,
            )
        )
        numbers.append(
            Number(f"the pair {row['pair']}: the pace c_m / c", row["pace"], "DECLARATION", BLOCK_SOURCE)
        )
    return Panel(
        key="block",
        layer=2,
        title="A foreign object as a declared block with its own pair",
        algebra=[
            (
                "The object is a block R of side s (a square on a layer, a cube on the board), declared as world data like a wall's placement, every cell of R carrying a lowered pair [num', den'] with num' / den' > num / den, a well of the pair in that medium; the object's record is the bound mode of the map in that well; its clock is the mode; its extent is the mode's, never a declaration in motion.",
                "MASSIVE_RECORD.md section 4 on detector-law-design",
            ),
            (
                "One integer per axis for the whole block, P, with its remainder; the block's cells and its pair region step one Link together by verb T; its click the evaluation E across R.",
                "MASSIVE_RECORD.md sections 5 and 6",
            ),
        ],
        note="Not built and not on main: the vocabulary of MASSIVE_RECORD.md only, its own table's numbers as DECLARATION; no run, no pin. The block differs from the light rule (Layer 1) by the pair on the six-neighbour term alone.",
        numbers=numbers,
        figure={
            "kind": "block",
            "side": 3,
            "medium": "[num, den]",
            "well": "[num', den']",
            "rows": BLOCK_TABLE,
        },
    )


def panel_declared_objects(detector: RunRecord) -> Panel:
    world = detector.world
    sets = world.get("detectors", []) if isinstance(world.get("detectors"), list) else []
    positions = {tuple(int(v) for v in p) for s in sets for p in s.get("positions", [])}
    objects = []
    roles: Counter[str] = Counter()
    for entry in world.get("measured", []):
        role = object_role(entry, positions)
        roles[role] += 1
        objects.append(
            {
                "role": role,
                "position": [int(v) for v in entry["position"]],
                "family": str(entry.get("family")),
            }
        )
    numbers = [
        Number(f"{role}s", str(count), "DECLARATION", "initialization.json: measured[]")
        for role, count in roles.items()
    ]
    numbers.append(
        Number("detector sets", str(len(sets)), "DECLARATION", "initialization.json: detectors[]")
    )
    for kind, label in (
        ("birth", "birth lines (the emitter's records)"),
        ("split", "split lines (the re-emitters')"),
        ("record", "record lines (the sets' offers)"),
        ("gather", "gather lines (the records' clicks)"),
    ):
        numbers.append(
            Number(label, str(detector.counts.get(kind, 0)), "DETECTOR", f"events.jsonl: {kind}")
        )
    return Panel(
        key="objects",
        layer=2,
        title="A detector-emitter as a declared object",
        algebra=[
            (
                "Every external entity is one generic detector-emitter, a receiver-inserter declared Outside; only a detector's reading is a measurement.",
                "HIGHLIGHTS.md 5.4, the line of record 1327",
            ),
            (
                "A detector's clock is its own count of intervals stretched by the age wall: the detector receives the Node's time; it has no other.",
                "HIGHLIGHTS.md 5.4, the line of record 709",
            ),
        ],
        note="The plane as the world file declares it (DECLARATION), each object by its declared role, and beside it what the objects wrote to the record in this run.",
        numbers=numbers,
        figure={"kind": "plane", "shape": [int(v) for v in detector.meta["shape"]], "objects": objects},
    )


def panel_gameboard_view(detector: RunRecord) -> Panel:
    nodes = detector.nodes_with_rows()
    marks = []
    for node in nodes:
        amount = sum(
            int(ray.get("amount", 0))
            for family in node.get("families", [])
            for ray in family.get("rays", [])
        )
        marks.append({"position": [int(v) for v in node["position"]], "amount": amount})
    numbers = [
        Number(
            "Nodes still holding rows at the last interval",
            str(len(nodes)),
            "GAMEBOARD",
            "state.json: nodes",
        )
    ]
    audit = detector.last_audit()
    if audit is not None:
        numbers.append(
            Number("the books' tick", str(audit.get("tick")), "GAMEBOARD", "run.json: audit[-1].tick")
        )
        for family, lines in audit.get("families", {}).items():
            transit = lines.get("transit", {})
            for key in ("released", "current", "absorbed", "escaped", "cancelled"):
                if key in transit:
                    numbers.append(
                        Number(
                            f"{family}: {key} (the transit line)",
                            str(transit[key]),
                            "GAMEBOARD",
                            "run.json: audit[-1].families.*.transit",
                        )
                    )
            numbers.append(
                Number(
                    f"{family}: the transit line balanced",
                    str(transit.get("balanced")),
                    "GAMEBOARD",
                    "run.json: audit[-1].families.*.transit.balanced",
                )
            )
        numbers.append(
            Number(
                "the books balanced",
                str(audit.get("balanced")),
                "GAMEBOARD",
                "run.json: audit[-1].balanced",
            )
        )
    return Panel(
        key="gameboard",
        layer=2,
        title="The GameBoard view, a diagnostic",
        algebra=[
            (
                "Every message released is on exactly one line of the books at every interval: released = in transit + absorbed + escaped (+ cancelled) per family, in amount and in content, exact at every tick (the engine's ledger).",
                "ALGEBRA.md 4.3",
            ),
            (
                "A reading of the board itself is a diagnostic; nothing measured inside the board is compared.",
                "ALGEBRA.md 3.2; record 281",
            ),
        ],
        note="GAMEBOARD: the store at the last interval (the Nodes still holding rows, with their amounts) and the books at the last completed tick. Compared with nothing.",
        numbers=numbers,
        figure={"kind": "store", "shape": [int(v) for v in detector.meta["shape"]], "nodes": marks},
    )


# --- layer 3 ----------------------------------------------------------------


def panel_record_life(detector: RunRecord, gather: dict[str, Any] | None) -> Panel:
    if gather is None:
        return Panel(
            "life",
            3,
            "How a click is born on the board: one record",
            missing="no gather at a declared detector set in the detector run",
        )
    identity = gather["record"]
    lines = detector.of_record(identity)
    birth = next((line for line in lines if line["event"] == "birth"), None)
    splits = [line for line in lines if line["event"] == "split"]
    face_clicks = [
        line
        for line in lines
        if line["event"] == "click" and str(line.get("detector", "")).startswith("face:")
    ]
    offers = [line for line in lines if line["event"] == "record"]
    after = [
        line for line in lines if line["event"] == "record" and int(line["tick"]) > int(gather["tick"])
    ]
    name = chosen_name(gather)
    body = body_at(detector, [int(v) for v in gather["node"][0]])
    stages: list[dict[str, Any]] = []
    if birth is not None:
        stages.append(
            {
                "title": "the birth",
                "tick": int(birth["tick"]),
                "lines": [
                    f"tick {birth['tick']}, at the Node {vec(birth['node'])}, the wheel u = {birth['u']}, {birth['units']} units on {birth['arms']} arm(s), the multiplicity {birth['multiplicity']}"
                ],
                "kind": "DETECTOR",
                "source": "events.jsonl: birth",
            }
        )
    for split in splits:
        stages.append(
            {
                "title": "a split at a re-emitter",
                "tick": int(split["tick"]),
                "lines": [
                    f"tick {split['tick']}, at {vec(split['node'])}: {split['absorbed']} row in, {split['born']} rows out, the multiplicity {split['multiplicity']}, u = {split['u']} carried"
                ],
                "kind": "DETECTOR",
                "source": "events.jsonl: split",
            }
        )
    if face_clicks:
        by_face = Counter(str(c["detector"]) for c in face_clicks)
        stages.append(
            {
                "title": "its rows that left through the faces",
                "tick": int(face_clicks[0]["tick"]),
                "lines": [
                    f"{len(face_clicks)} face clicks from tick {face_clicks[0]['tick']} to {face_clicks[-1]['tick']}: "
                    + ", ".join(f"{face} {n}" for face, n in sorted(by_face.items()))
                ],
                "kind": "DETECTOR",
                "source": "events.jsonl: click (face)",
            }
        )
    if offers:
        stages.append(
            {
                "title": "its offers in the detectors' own records",
                "tick": int(offers[0]["tick"]),
                "lines": [
                    f"{len(offers)} record lines at tick {offers[0]['tick']}, one per set the record reached; the chosen set's pointer "
                    + next(
                        (
                            f"({o['pointer'][0]}, {o['pointer'][1]}), the square {o['record']}"
                            for o in offers
                            if o.get("detector") == name
                        ),
                        "not among them",
                    )
                ],
                "kind": "DETECTOR",
                "source": "events.jsonl: record (reading sum)",
            }
        )
    stages.append(
        {
            "title": "the gather: the evaluation in the detector's own record, the comparison, the click",
            "tick": int(gather["tick"]),
            "lines": [
                f"tick {gather['tick']}, arrived {gather['arrived']}: u = {gather['u']}, {len(gather['cells'])} cells, the chosen {name} at {vec(gather['node'][0])}, the weight {gather['weight']}, the total {gather['total']}, T = {gather['T']}, before {gather['before']}, after {gather['after']}"
            ],
            "kind": "DETECTOR",
            "source": "events.jsonl: gather",
        }
    )
    stages.append(
        {
            "title": "the deletion",
            "tick": int(gather["tick"]),
            "lines": [
                f"record lines of this identity after the gather: {len(after)} (of {len(offers)} before); the record's rows are gone from the store: the one deletion"
            ],
            "kind": "DETECTOR",
            "source": "events.jsonl: record.of after gather.tick",
        }
    )
    stamp_line = "no clock field on any line: the world does not declare clock_stamp"
    if "clock" in gather:
        stamp_line = f"the detector's own count on the gather line: clock = {gather['clock']}"
    if body is not None:
        stamp_line += f"; the chosen set's body in state.json: age {body['age']}, owed {body['owed']}, waited {body['waited']}"
    stages.append(
        {
            "title": "the stamp with the detector's own count",
            "tick": int(gather["tick"]),
            "lines": [stamp_line],
            "kind": "DETECTOR" if "clock" in gather else "GAMEBOARD",
            "source": "events.jsonl: gather.clock; state.json: measured[]",
        }
    )
    numbers = [
        Number("the record's identity", str(identity), "DETECTOR", "events.jsonl: gather.record"),
        Number("its birth wheel u", str(gather["u"]), "DETECTOR", "events.jsonl: gather.u"),
        Number("its lines in the record", str(len(lines)), "DETECTOR", "events.jsonl: record identity"),
        Number("its offers before the gather", str(len(offers)), "DETECTOR", "events.jsonl: record.of"),
        Number(
            "its record lines after the gather",
            str(len(after)),
            "DETECTOR",
            "events.jsonl: record.of after gather.tick",
        ),
        Number("the chosen set", name, "DETECTOR", "events.jsonl: gather.chosen"),
        Number("the gather's tick", str(gather["tick"]), "GAMEBOARD", "events.jsonl: gather.tick"),
    ]
    if "clock" in gather:
        numbers.append(
            Number(
                "the detector's own count at the click",
                str(gather["clock"]),
                "DETECTOR",
                "events.jsonl: gather.clock",
            )
        )
    if body is not None:
        numbers.append(
            Number(
                "the chosen set's body: its age (its own count)",
                str(body["age"]),
                "GAMEBOARD",
                "state.json: measured[].age",
            )
        )
        numbers.append(
            Number(
                "the chosen set's body: its owed count",
                str(body["owed"]),
                "GAMEBOARD",
                "state.json: measured[].owed",
            )
        )
    return Panel(
        key="life",
        layer=3,
        title="How a click is born on the board: one record",
        algebra=[
            (
                "A click is an action, not a passive read: the record ends at the detector, its content enters the detector's own record, and the detector's count advances; a record is read once by one comparison and deleted: the only read-out, the one deletion.",
                "ALGEBRA.md 3.1; the owner's word of record 1139",
            ),
            (
                "The interval is injective between clicks: no rule of the interval deletes a weight, a multiplicity or a phase; the click is the one deletion.",
                "ALGEBRA.md 4.7, Theorem 3",
            ),
        ],
        note=(
            "One record followed from its birth to its gather, from the record alone (no replay). Without clock_stamp no line carries "
            "the detector's own count; the body's age and owed in the snapshot are the store's view (GAMEBOARD): with owed 0 its count "
            "advanced at every interval, so its count at the click is the tick. The DETECTOR stamp proper is the clock field a world under "
            "clock_stamp writes."
        ),
        numbers=numbers,
        figure={"kind": "stages", "stages": stages},
    )


def panel_screen(detector: RunRecord) -> Panel:
    gathers = detector.of_kind("gather")
    if not gathers:
        return Panel(
            "screen",
            3,
            "The pattern on the screen, as the experimenter sees it",
            missing="no gather line in the detector run",
        )
    sets = (
        detector.world.get("detectors", []) if isinstance(detector.world.get("detectors"), list) else []
    )
    names = [str(s["name"]) for s in sets]
    counts = Counter(chosen_name(g) for g in gathers)
    kinds = Counter(chosen_kind(chosen_name(g)) for g in gathers)
    bars = [{"name": name, "count": counts.get(name, 0)} for name in names]
    numbers = [
        Number("gathers (the records' clicks)", str(len(gathers)), "DETECTOR", "events.jsonl: gather")
    ]
    for kind in ("screen", "wall", "faces"):
        numbers.append(
            Number(
                f"chosen at the {kind}" if kind != "screen" else "chosen at a declared set (the screen)",
                str(kinds.get(kind, 0)),
                "DETECTOR",
                "events.jsonl: gather.chosen",
            )
        )
    lit = [b for b in bars if b["count"]]
    numbers.append(
        Number("sets with at least one click", str(len(lit)), "DETECTOR", "events.jsonl: gather.chosen")
    )
    reg = detector.register
    if isinstance(reg, dict) and isinstance(reg.get("clicks_by_kind"), dict):
        for kind, value in reg["clicks_by_kind"].items():
            numbers.append(
                Number(
                    f"the register's clicks by kind, {kind}, over the register's births",
                    str(value),
                    "PIN",
                    "expectations.json: clicks_by_kind (the world's block)",
                )
            )
    return Panel(
        key="screen",
        layer=3,
        title="The pattern on the screen, as the experimenter sees it",
        algebra=[
            (
                "A click at a detector, a count between clicks on the detector's own record, and a ratio of such counts are what is compared with nature; nothing measured inside the board is compared; a reading of the board itself is a diagnostic.",
                "ALGEBRA.md 3.2, the reading rule",
            ),
        ],
        note="One bar per declared set: the count of gathers whose chosen set it is, over every record gathered in the run; the wall's and the faces' gathers beside. The register's numbers, where the series has them, are printed as PIN; nothing is called matched.",
        numbers=numbers,
        figure={
            "kind": "bars",
            "bars": bars,
            "others": [
                {"name": "the wall", "count": kinds.get("wall", 0)},
                {"name": "the faces", "count": kinds.get("faces", 0)},
            ],
        },
    )


def panel_counts_clock(detector: RunRecord) -> Panel:
    gathers = detector.of_kind("gather")
    if not gathers:
        return Panel(
            "clock",
            3,
            "The detector's counts against its own clock",
            missing="no gather line in the detector run",
        )
    stamped = all("clock" in g for g in gathers)
    axis_key = "clock" if stamped else "tick"
    series = [
        {
            "name": "every declared set together",
            "ticks": sorted(
                int(g[axis_key]) for g in gathers if chosen_kind(chosen_name(g)) == "screen"
            ),
        }
    ]
    per_set: dict[str, list[int]] = {}
    for g in gathers:
        name = chosen_name(g)
        if chosen_kind(name) == "screen":
            per_set.setdefault(name, []).append(int(g[axis_key]))
    for name, ticks in sorted(per_set.items()):
        series.append({"name": name, "ticks": sorted(ticks)})
    body_owed = None
    first = next((g for g in gathers if chosen_kind(chosen_name(g)) == "screen"), None)
    if first is not None:
        body = body_at(detector, [int(v) for v in first["node"][0]])
        if body is not None:
            body_owed = int(body["owed"])
    numbers = [
        Number(
            "clicks at the declared sets",
            str(len(series[0]["ticks"])),
            "DETECTOR",
            "events.jsonl: gather.chosen",
        ),
        Number(
            "the first such click's " + ("own count" if stamped else "tick"),
            str(series[0]["ticks"][0]) if series[0]["ticks"] else "none",
            "DETECTOR" if stamped else "GAMEBOARD",
            f"events.jsonl: gather.{axis_key}",
        ),
        Number(
            "the last such click's " + ("own count" if stamped else "tick"),
            str(series[0]["ticks"][-1]) if series[0]["ticks"] else "none",
            "DETECTOR" if stamped else "GAMEBOARD",
            f"events.jsonl: gather.{axis_key}",
        ),
    ]
    if body_owed is not None:
        numbers.append(
            Number(
                "the first chosen set's body: its owed count",
                str(body_owed),
                "GAMEBOARD",
                "state.json: measured[].owed",
            )
        )
    axis_label = (
        "the detector's own count (DETECTOR, the clock field)"
        if stamped
        else "the tick (GAMEBOARD); equal to the set's own count in this run, its owed 0"
    )
    return Panel(
        key="clock",
        layer=3,
        title="The detector's counts against its own clock",
        algebra=[
            (
                "A detector D at a Node has its own count n_D, its count of intervals stretched by what arrives at it; it never reads the tick, only n_D; the click is the event of receiving a packet, stamped with n_D.",
                "ALGEBRA.md 3.1",
            ),
        ],
        note="A staircase: the count of clicks against the clock, for every declared set together and for one set chosen by the reader. The axis is "
        + axis_label
        + ".",
        numbers=numbers,
        figure={
            "kind": "staircase",
            "series": series,
            "axis": axis_label,
            "axis_kind": "DETECTOR" if stamped else "GAMEBOARD",
        },
    )


def panel_intervals(detector: RunRecord) -> Panel:
    gathers = detector.of_kind("gather")
    screen = [g for g in gathers if chosen_kind(chosen_name(g)) == "screen"]
    if len(screen) < 2:
        return Panel(
            "intervals",
            3,
            "The interval between clicks",
            missing="fewer than two clicks at the declared sets",
        )
    stamped = all("clock" in g for g in screen)
    key = "clock" if stamped else "tick"
    ticks = sorted(int(g[key]) for g in screen)
    diffs = [b - a for a, b in zip(ticks[:-1], ticks[1:], strict=True)]
    us = [int(g["u"]) for g in screen]
    kind = "DETECTOR" if stamped else "GAMEBOARD"
    numbers = [
        Number(
            "the intervals between consecutive clicks at the declared sets",
            ", ".join(str(d) for d in diffs[:24]) + (" ..." if len(diffs) > 24 else ""),
            "CONVERSION",
            f"gather.{key} differences ({kind} axis)",
        ),
        Number("the least interval", str(min(diffs)), "CONVERSION", f"gather.{key} differences"),
        Number("the greatest interval", str(max(diffs)), "CONVERSION", f"gather.{key} differences"),
        Number(
            "the wheel's value u of each click, in order",
            ", ".join(str(u) for u in us[:24]) + (" ..." if len(us) > 24 else ""),
            "DETECTOR",
            "events.jsonl: gather.u",
        ),
        Number("distinct u among them", str(len(set(us))), "DETECTOR", "events.jsonl: gather.u"),
    ]
    return Panel(
        key="intervals",
        layer=3,
        title="The interval between clicks",
        algebra=[
            (
                "The least time a detector times by itself is a pulse to its neighbour and its return, two intervals Inside, two of its counts at r_D = 1; the tick itself is GAMEBOARD and never read.",
                "ALGEBRA.md 3.4, discreteness Outside",
            ),
        ],
        note="The differences of consecutive clicks at the declared sets, as a histogram of exact integers, and the wheel's value of every click, so the eye sees the wheel turn once per birth.",
        numbers=numbers,
        figure={"kind": "histogram", "values": diffs, "axis_kind": kind},
    )


def build_panels(light: RunRecord, detector: RunRecord) -> list[Panel]:
    gather = followed_record(detector)
    return [
        panel_torus(light, detector),
        panel_node_ports(),
        panel_state_vector(light, detector),
        panel_verb_t(light),
        panel_verb_b(detector, gather),
        panel_verb_g(detector, gather),
        panel_verb_p(detector, gather),
        panel_verb_e(detector, gather),
        panel_verb_d(light, detector, gather),
        panel_light_rule(),
        panel_fan_faces(light),
        panel_pace(light),
        panel_block(),
        panel_declared_objects(detector),
        panel_gameboard_view(detector),
        panel_record_life(detector, gather),
        panel_screen(detector),
        panel_counts_clock(detector),
        panel_intervals(detector),
    ]


def as_rows(panels: list[Panel]) -> list[tuple[str, str, str, str, str]]:
    """Every number of every panel as (panel, label, value, kind, source): the
    headless printout and what the test checks."""
    rows = []
    for panel in panels:
        for number in panel.numbers:
            rows.append((panel.key, number.label, number.value, number.kind, number.source))
    return rows


def register_fraction(value: Any) -> Fraction:
    """A register's number as a fraction (kept for the readers' callers)."""
    return fraction(value)


# --- one run of either engine: the algebra layer (DESIGN_3D.md section 2) ----


def _pair_text(value: Any) -> str:
    if isinstance(value, list) and len(value) == 2:
        return f"[{int(value[0])}, {int(value[1])}]"
    return str(value)


def _vec_text(value: Any) -> str:
    if isinstance(value, list):
        return "(" + ", ".join(str(int(v)) for v in value) + ")"
    return str(value)


def panel_algebra_board(run: RunRecord) -> Panel:
    shape = run.shape
    numbers = [
        Number("the extents (x, y, z)", vec(shape), "DECLARATION", "run.json: shape"),
        Number(
            "the faces per axis",
            _boundary_text(run.meta.get("boundary")),
            "DECLARATION",
            "run.json: boundary",
        ),
    ]
    ones = sum(1 for v in shape if v == 1)
    form = "a chain" if ones >= 2 else ("a layer" if ones == 1 else "a 3-D box")
    numbers.append(Number("the GameBoard's form", form, "DECLARATION", "run.json: shape"))
    families = run.meta.get("families") if isinstance(run.meta.get("families"), list) else []
    if run.massive:
        for family in families:
            faces = family.get("faces")
            if isinstance(faces, dict):
                numbers.append(
                    Number(
                        f"the family {family.get('name')}'s own faces",
                        ", ".join(f"{a} {faces.get(a, 'periodic')}" for a in ("x", "y", "z")),
                        "DECLARATION",
                        "run.json: families[].faces",
                    )
                )
    return Panel(
        key="alg_board",
        layer=1,
        title="The board: the translation group of the torus",
        algebra=[
            (
                "Z_X x Z_Y x Z_Z per world: the GameBoard's extents per axis, each factor a circle (a periodic axis) or a segment (an open axis whose faces are the border, a click at the face detector). Chosen per world by shape and boundary.",
                "ALGEBRA.md 1.6",
            ),
            (
                "An open face of the GameBoard is a detector, named face:+x .. face:-z; a periodic axis has no faces.",
                "TERMINOLOGY.md, Face, face detector",
            ),
        ],
        note="A 3-D box when every extent exceeds 1, a layer when one extent is 1 (the layer worlds of the new engine's schedule), a chain when two are. On a massive world each family's own faces are a second declaration beside light's.",
        numbers=numbers,
    )


def panel_algebra_families(run: RunRecord) -> Panel:
    families = run.meta.get("families") if isinstance(run.meta.get("families"), list) else []
    if not families:
        return Panel(
            "alg_families", 1, "The families and their pairs", missing="no families in run.json"
        )
    numbers: list[Number] = []
    for family in families:
        name = str(family.get("name"))
        numbers.append(
            Number(
                f"{name}: quantum h",
                str(family.get("quantum")),
                "DECLARATION",
                "run.json: families[].quantum",
            )
        )
        if "charge" in family:
            numbers.append(
                Number(
                    f"{name}: charge per unit of content",
                    _pair_text(family.get("charge")),
                    "DECLARATION",
                    "run.json: families[].charge",
                )
            )
        if "phase" in family:
            numbers.append(
                Number(
                    f"{name}: a phase circle",
                    str(family.get("phase")),
                    "DECLARATION",
                    "run.json: families[].phase",
                )
            )
        if "phase_per_link" in family:
            numbers.append(
                Number(
                    f"{name}: phase per Link (the family's clock)",
                    _pair_text(family.get("phase_per_link")),
                    "DECLARATION",
                    "run.json: families[].phase_per_link",
                )
            )
        if family.get("lifetime") is not None:
            numbers.append(
                Number(
                    f"{name}: lifetime",
                    str(family.get("lifetime")),
                    "DECLARATION",
                    "run.json: families[].lifetime",
                )
            )
        if "pair" in family:
            pair = family["pair"]
            kind_word = (
                "light's kind bit for bit"
                if pair == [1, 1]
                else "a massive kind (den > num), its clock its gap, no lamp"
            )
            numbers.append(
                Number(
                    f"{name}: the pair [num, den] on the six-neighbour term ({kind_word})",
                    _pair_text(pair),
                    "DECLARATION",
                    "run.json: families[].pair",
                )
            )
        elif run.is_new:
            numbers.append(
                Number(
                    f"{name}: the pair",
                    "[1, 1] (light's kind; no pair key under the world without massive_record)",
                    "DECLARATION",
                    "run.json: families[] (absent pair reads as [1, 1], BUILD.md section 3)",
                )
            )
    note = (
        "The rule with the pair: 3 den a_next + r' = num S_6 - 3 den a_before + r, 0 <= r' < 3 den; [1, 1] the light rule bit for bit, den > num a massive kind whose gap is cos omega_0 = num / den."
        if run.is_new
        else "No pair is declared: the engine on main runs the Beam Law, whose record form is amplitude-v1; the six-neighbour rule with the pair is not in it, and nothing is invented here."
    )
    return Panel(
        key="alg_families",
        layer=1,
        title="The families and their pairs",
        algebra=[
            (
                "A row turns phi(tau) = floor((tau + 1) n / d) - floor(tau n / d) steps per interval of age, the pair [n, d] its family's declaration, read modulo N.",
                "ALGEBRA.md 2.1",
            ),
            (
                "A record kind's pair [num, den] on the six-neighbour term: [1, 1] light's, den > num a massive kind.",
                "MASSIVE_RECORD.md sections 1 and 2 (detector-law-build)",
            ),
        ],
        note=note,
        numbers=numbers,
    )


BLOCK_KEYS = (
    "side",
    "pair",
    "amount",
    "momentum",
    "held",
    "coupling",
    "wheel",
    "seed",
    "absorbing",
    "cavity",
    "ramp",
    "margin",
    "emits",
)
BODY_KEYS = ("amount", "momentum", "fixed", "held", "phase", "directions")


def panel_algebra_blocks(run: RunRecord) -> Panel:
    numbers: list[Number] = []
    measured = run.declared_measured()
    numbers_meta = run.meta.get("numbers") if isinstance(run.meta.get("numbers"), dict) else {}
    if run.is_new:
        blocks = [(i, e) for i, e in enumerate(measured) if "side" in e]
        if not blocks:
            return Panel(
                "alg_blocks",
                1,
                "The blocks with their pairs and sides",
                missing="no block declared (no measured event with side)",
            )
        for index, entry in blocks:
            label = f"block measured:{index} ({entry.get('family')})"
            numbers.append(
                Number(
                    f"{label}: the corner",
                    _vec_text(entry.get("position")),
                    "DECLARATION",
                    "initialization.json: measured[].position",
                )
            )
            for key in BLOCK_KEYS:
                if key in entry:
                    value = entry[key]
                    if key == "coupling" and isinstance(value, dict):
                        text = "G " + _pair_text(value.get("G")) + ", g " + _pair_text(value.get("g"))
                    elif isinstance(value, dict):
                        text = ", ".join(f"{k} {v}" for k, v in value.items())
                    elif isinstance(value, list):
                        text = _pair_text(value) if key == "pair" else _vec_text(value)
                    else:
                        text = str(value)
                    numbers.append(
                        Number(
                            f"{label}: {key}",
                            text,
                            "DECLARATION",
                            f"initialization.json: measured[].{key}",
                        )
                    )
        note = "A block is a measured event that declares side: a cube of that side at its corner, its cells carrying its own pair [num', den'] (a well when num' / den' > num / den), its momentum P one integer per axis. run.json's numbers echoes its position and family and no block key (the branch at 2f44797c)."
    else:
        if not numbers_meta:
            return Panel(
                "alg_blocks",
                1,
                "The blocks with their pairs and sides",
                missing="no body declared (run.json numbers is empty)",
            )
        for key, entry in numbers_meta.items():
            label = f"body {key} ({entry.get('family')})"
            numbers.append(
                Number(
                    f"{label}: position",
                    _vec_text(entry.get("position")),
                    "DECLARATION",
                    "run.json: numbers[].position",
                )
            )
            numbers.append(
                Number(
                    f"{label}: span (its extent)",
                    _vec_text(entry.get("span")),
                    "DECLARATION",
                    "run.json: numbers[].span",
                )
            )
            if entry.get("become") is not None:
                numbers.append(
                    Number(
                        f"{label}: become",
                        str(entry.get("become")),
                        "DECLARATION",
                        "run.json: numbers[].become",
                    )
                )
            declared = measured[int(key) - 1] if 0 < int(key) <= len(measured) else {}
            for dkey in BODY_KEYS:
                if dkey in declared:
                    value = declared[dkey]
                    text = (
                        _vec_text(value)
                        if isinstance(value, list) and value and not isinstance(value[0], list)
                        else str(value)
                    )
                    numbers.append(
                        Number(
                            f"{label}: {dkey}",
                            text,
                            "DECLARATION",
                            f"initialization.json: measured[].{dkey}",
                        )
                    )
            table = declared.get("table")
            if isinstance(table, dict):
                rules = ", ".join(
                    f"{fam} {rule.get('rule') if isinstance(rule, dict) else rule}"
                    for fam, rule in table.items()
                )
                numbers.append(
                    Number(
                        f"{label}: its rule per family (the table)",
                        rules,
                        "DECLARATION",
                        "initialization.json: measured[].table",
                    )
                )
        note = "A body of the Beam Law: its extent span, a box of Nodes centred on its position, its rule per family; not a cube of the massive kind, whose pair and side no run on main declares."
    return Panel(
        key="alg_blocks",
        layer=1,
        title="The blocks with their pairs and sides",
        algebra=[
            (
                "A foreign object as a declared cube of side s at a corner, its cells carrying the lowered pair [num', den'], a well; its momentum one integer per axis with its remainder; its click the evaluation (E) across its cells.",
                "MASSIVE_RECORD.md sections 4 to 7 (detector-law-build)",
            )
        ],
        note=note,
        numbers=numbers,
    )


def panel_algebra_instruments(run: RunRecord) -> Panel:
    numbers: list[Number] = []
    for entry in run.declared_detectors():
        name = str(entry.get("name"))
        positions = entry.get("positions") if isinstance(entry.get("positions"), list) else []
        numbers.append(
            Number(
                f"detector {name}: Nodes",
                str(len(positions)),
                "DECLARATION",
                "initialization.json: detectors[].positions",
            )
        )
        if positions:
            numbers.append(
                Number(
                    f"detector {name}: first Node",
                    _vec_text(positions[0]),
                    "DECLARATION",
                    "initialization.json: detectors[].positions",
                )
            )
        for key in ("threshold", "reading"):
            if key in entry:
                numbers.append(
                    Number(
                        f"detector {name}: {key}",
                        str(entry[key]),
                        "DECLARATION",
                        f"initialization.json: detectors[].{key}",
                    )
                )
    faces = []
    for axis in ("x", "y", "z"):
        if not run.periodic(axis):
            faces.extend([f"face:+{axis}", f"face:-{axis}"])
    numbers.append(
        Number(
            "the face detectors (the open faces)",
            ", ".join(faces) or "none",
            "DECLARATION",
            "run.json: boundary",
        )
    )
    base = 0 if run.is_new else 1
    for index, entry in enumerate(run.declared_measured()):
        label = f"measured:{index + base} ({entry.get('family')}) at {_vec_text(entry.get('position'))}"
        lamp = entry.get("lamp")
        if isinstance(lamp, dict):
            numbers.append(
                Number(
                    f"emitter {label}: rate",
                    _pair_text(lamp.get("rate")),
                    "DECLARATION",
                    "initialization.json: measured[].lamp.rate",
                )
            )
            numbers.append(
                Number(
                    f"emitter {label}: wheel [r, W]",
                    _pair_text(lamp.get("wheel")),
                    "DECLARATION",
                    "initialization.json: measured[].lamp.wheel",
                )
            )
            directions = lamp.get("directions") if isinstance(lamp.get("directions"), list) else []
            numbers.append(
                Number(
                    f"emitter {label}: directions",
                    str(len(directions)),
                    "DECLARATION",
                    "initialization.json: measured[].lamp.directions",
                )
            )
            if "train" in lamp:
                numbers.append(
                    Number(
                        f"emitter {label}: train (in periods)",
                        str(lamp["train"]),
                        "DECLARATION",
                        "initialization.json: measured[].lamp.train",
                    )
                )
        if "emits" in entry:
            numbers.append(
                Number(
                    f"emitter {label}: emits",
                    str(entry["emits"]),
                    "DECLARATION",
                    "initialization.json: measured[].emits",
                )
            )
        if "lamp" not in entry and "emits" not in entry:
            numbers.append(
                Number(
                    f"receiver {label}",
                    "a measured event: its Nodes receive"
                    if run.is_new
                    else "a measured event, a detector of one Node where outside every set",
                    "DECLARATION",
                    "initialization.json: measured[]",
                )
            )
    probes = run.world.get("probes")
    if isinstance(probes, list):
        numbers.append(
            Number(
                "probes (light's amplitude read per interval, a diagnostic)",
                str(len(probes)),
                "DECLARATION",
                "initialization.json: probes",
            )
        )
    return Panel(
        key="alg_instruments",
        layer=1,
        title="The detectors and the emitters",
        algebra=[
            (
                "A detector D at a Node has its own count n_D; it never reads the tick, only n_D.",
                "ALGEBRA.md 3.1",
            ),
            (
                "A detector, a lamp and an external body are declarations of the world file, not records that hop.",
                "ALGEBRA.md 3.4",
            ),
            (
                "Every external entity is one generic detector-emitter, a receiver-inserter declared Outside.",
                "HIGHLIGHTS.md 5.4, the line of record 1327",
            ),
        ],
        note="Every declared set with its Nodes, the face detectors the open faces make, every emitter (a measured event with a lamp: its rate, its wheel, its directions; on the new engine its train; a block with emits), every receiver."
        + (
            " Under the detector law every declared set's Nodes and every measured event's Nodes receive (BUILD.md section 3)."
            if run.is_new
            else ""
        ),
        numbers=numbers,
    )


VERB_LINES = [
    (
        "(T) the translation of an accumulator by its rate: x -> x + r on Z^k or on a torus; every count of the law is this.",
        "ALGEBRA.md 2.1",
    ),
    (
        "(B) the bilinear form with a declared matrix: a signed inner product over declared columns times the moment.",
        "ALGEBRA.md 2.2",
    ),
    (
        "(G) the group-ring addition: the merge of identical rows is the ring's addition, f <- f + g, with the cancel [p + N/2] = -[p].",
        "ALGEBRA.md 2.3",
    ),
    (
        "(P) the permutation of the joint state: of directions, labels or Nodes, never of contents.",
        "ALGEBRA.md 2.4",
    ),
    (
        "(E) the evaluation at the roots of unity: ev(f) = sum over p of f_p zeta_N^p, the click's pointer.",
        "ALGEBRA.md 2.5",
    ),
    (
        "(D) the division with the remainder kept, and the comparison: the count is the whole part in units of the wall, that much is subtracted and the remainder stays.",
        "ALGEBRA.md 2.6",
    ),
]


def panel_algebra_verbs(run: RunRecord) -> Panel:
    if run.is_new:
        acting = [
            (
                "One line per record per interval: 3 den a_next + r' = num S_6 - 3 den a_before + r, 0 <= r' < 3 den: (G) the sum over the six Ports, (D) the division by 3 den with the remainder kept, (T) the carry of r; the pair one entry of (B)'s declared matrix; (E) the click across the cells.",
                "MASSIVE_RECORD.md section 1; ALGEBRA_MASSIVE_RECORD.md 0.1",
            )
        ]
        note = "No run records the row's three integers a_now, a_before and r (DESIGN_3D.md, Finding 1); the rule's instance is the first page's worked example, COMPUTATION, in DESIGN.md section 2.5."
    else:
        acting = [
            (
                "One interval of a record applies, in order, (T) on every accumulator, (D) whose whole part is the event, (B) at the push and at the click, (G) and (E) where rows are summed at one Node and where they end, and (P) at a collision; the lines are the hop, the phase, the push, the crowd, the split, the sum, the click and the age.",
                "ALGEBRA.md 2.11",
            )
        ]
        note = "The verbs as the Beam Law applies them per interval, quoted; the record's lines of this run (the events) are the marks of the GameBoard layer."
    return Panel(
        key="alg_verbs",
        layer=1,
        title="The verbs that act per interval",
        algebra=VERB_LINES + acting,
        note=note,
    )


# --- one run of either engine: the Outside layer (DESIGN_3D.md section 4) ----


def _cell_group(name: str) -> str:
    if name.startswith("face:"):
        return "the faces"
    if name.startswith("measured:"):
        return "the measured events"
    return "the declared sets"


def _axis_of(run: RunRecord, gathers: list[dict[str, Any]]) -> tuple[str, str, str]:
    """The key of a click's count on a gather line, its kind and its label."""
    if gathers and all("clock" in g for g in gathers):
        return "clock", "DETECTOR", "the detector's own count (DETECTOR, the clock field)"
    if run.is_new and gathers and all("click" in g for g in gathers):
        return (
            "click",
            "GAMEBOARD",
            "the interval of the first rung's crossing (GAMEBOARD, the record's ordering; the detector's own count is not stamped in this run)",
        )
    return (
        "tick",
        "GAMEBOARD",
        "the tick (GAMEBOARD, the record's ordering; the detector's own count is not stamped in this run)",
    )


def panel_outside_records(run: RunRecord) -> Panel:
    gathers = run.of_kind("gather")
    numbers: list[Number] = []
    chosen = Counter(chosen_of(g) or "none" for g in gathers)
    for entry in run.meta_detectors():
        name = str(entry.get("name"))
        if run.is_new:
            positions = entry.get("positions") if isinstance(entry.get("positions"), list) else []
            numbers.append(
                Number(
                    f"{name}: Nodes",
                    str(len(positions)),
                    "DECLARATION",
                    "run.json: detectors[].positions",
                )
            )
            numbers.append(
                Number(
                    f"{name}: clicks (the gathers whose chosen cell it is)",
                    str(entry.get("clicks")),
                    "DETECTOR",
                    "run.json: detectors[].clicks",
                )
            )
        else:
            for key in ("nodes", "threshold", "reading"):
                if key in entry:
                    numbers.append(
                        Number(
                            f"{name}: {key}",
                            str(entry[key]),
                            "DECLARATION",
                            f"run.json: detectors[].{key}",
                        )
                    )
            families = entry.get("families") if isinstance(entry.get("families"), dict) else {}
            for family, values in families.items():
                if not isinstance(values, dict):
                    continue
                for key in ("measured", "clicks", "record", "content", "phase"):
                    if key in values:
                        text = (
                            _vec_text(values[key]) if isinstance(values[key], list) else str(values[key])
                        )
                        numbers.append(
                            Number(
                                f"{name}, {family}: {key}"
                                + (" (the detector's own record)" if key == "record" else ""),
                                text,
                                "DETECTOR",
                                f"run.json: detectors[].families.{key}",
                            )
                        )
        numbers.append(
            Number(
                f"{name}: gather lines chosen here",
                str(chosen.get(name, 0)),
                "DETECTOR",
                "events.jsonl: gather.chosen",
            )
        )
    if not run.is_new:
        faces = Counter(
            str(line.get("detector"))
            for line in run.of_kind("click")
            if str(line.get("detector", "")).startswith("face:")
        )
        for name, count in sorted(faces.items()):
            numbers.append(
                Number(
                    f"{name}: face click lines", str(count), "DETECTOR", "events.jsonl: click.detector"
                )
            )
    for name, count in sorted(chosen.items()):
        if not any(str(e.get("name")) == name for e in run.meta_detectors()):
            numbers.append(
                Number(
                    f"{name} ({_cell_group(name)}): gather lines chosen here",
                    str(count),
                    "DETECTOR",
                    "events.jsonl: gather.chosen",
                )
            )
    if run.is_new:
        cycles = [line for line in run.of_kind("click")]
        by_block = Counter(int(line.get("measured", -1)) for line in cycles)
        for index, count in sorted(by_block.items()):
            numbers.append(
                Number(
                    f"block measured:{index}: its own cycles (its self-clicks)",
                    str(count),
                    "DETECTOR",
                    "events.jsonl: click.cycle",
                )
            )
            last = [line for line in cycles if line.get("measured") == index][-1]
            if "clock" in last:
                numbers.append(
                    Number(
                        f"block measured:{index}: its count at its last self-click",
                        str(last["clock"]),
                        "DETECTOR",
                        "events.jsonl: click.clock",
                    )
                )
    numbers.append(
        Number(
            "gather lines (the records' clicks)", str(len(gathers)), "DETECTOR", "events.jsonl: gather"
        )
    )
    layer = run.meta.get("layer")
    if isinstance(layer, dict):
        for key in ("born", "gathered", "open"):
            if key in layer:
                numbers.append(
                    Number(f"the layer's {key}", str(layer[key]), "DETECTOR", f"run.json: layer.{key}")
                )
    if not numbers:
        return Panel(
            "out_records",
            3,
            "The detectors' own records in their own counts",
            missing="no detector table and no gather line in this run",
        )
    return Panel(
        key="out_records",
        layer=3,
        title="The detectors' own records in their own counts",
        algebra=[
            (
                "A click is an action, not a passive read: the record ends at the detector, its content enters the detector's own record, and the detector's count advances.",
                "ALGEBRA.md 3.1",
            )
        ],
        note="One card per detector from the run's own table (run.json detectors), beside the count of gather lines chosen at it, which the test holds equal to the record's own totals; on the new engine a block's self-clicks are the click of a body (MASSIVE_RECORD.md section 1).",
        numbers=numbers,
    )


def panel_outside_clock(run: RunRecord) -> Panel:
    gathers = run.of_kind("gather")
    if not gathers:
        return Panel(
            "out_clock",
            3,
            "The counts against the detector's own count",
            missing="no gather line in this run",
        )
    key, kind, label = _axis_of(run, gathers)
    per_cell: dict[str, list[int]] = {}
    for g in gathers:
        name = chosen_of(g)
        if name is not None:
            per_cell.setdefault(name, []).append(int(g[key]))
    series = [
        {
            "name": "every cell together",
            "ticks": sorted(int(g[key]) for g in gathers if chosen_of(g) is not None),
        }
    ]
    for name, ticks in sorted(per_cell.items()):
        series.append({"name": name, "ticks": sorted(ticks)})
    numbers = [
        Number(
            "clicks with a chosen cell",
            str(len(series[0]["ticks"])),
            "DETECTOR",
            "events.jsonl: gather.chosen",
        ),
        Number(
            "the first click's " + ("own count" if kind == "DETECTOR" else "ordering"),
            str(series[0]["ticks"][0]),
            kind,
            f"events.jsonl: gather.{key}",
        ),
        Number(
            "the last click's " + ("own count" if kind == "DETECTOR" else "ordering"),
            str(series[0]["ticks"][-1]),
            kind,
            f"events.jsonl: gather.{key}",
        ),
    ]
    if run.is_new:
        cycles = run.of_kind("click")
        if cycles and all("clock" in c for c in cycles):
            series.append(
                {
                    "name": "a block's own cycles (click.cycle against click.clock)",
                    "ticks": sorted(int(c["clock"]) for c in cycles),
                }
            )
            numbers.append(
                Number(
                    "a block's self-clicks", str(len(cycles)), "DETECTOR", "events.jsonl: click.clock"
                )
            )
    return Panel(
        key="out_clock",
        layer=3,
        title="The counts against the detector's own count",
        algebra=[
            (
                "A detector D at a Node has its own count n_D, its count of intervals stretched by what arrives at it; it never reads the tick, only n_D; the click is the event of receiving a packet, stamped with n_D.",
                "ALGEBRA.md 3.1",
            )
        ],
        note="A staircase: the count of clicks against "
        + label
        + ", for every cell together and for one cell chosen by the reader.",
        numbers=numbers,
        figure={"kind": "staircase", "series": series, "axis": label, "axis_kind": kind},
    )


def panel_outside_intervals(run: RunRecord) -> Panel:
    gathers = [g for g in run.of_kind("gather") if chosen_of(g) is not None]
    if len(gathers) < 2:
        return Panel(
            "out_intervals",
            3,
            "The intervals between clicks",
            missing="fewer than two clicks with a chosen cell",
        )
    key, kind, _label = _axis_of(run, gathers)
    ticks = sorted(int(g[key]) for g in gathers)
    diffs = [b - a for a, b in zip(ticks[:-1], ticks[1:], strict=True)]
    us = [int(g["u"]) for g in gathers if "u" in g]
    numbers = [
        Number(
            "the intervals between consecutive clicks",
            ", ".join(str(d) for d in diffs[:24]) + (" ..." if len(diffs) > 24 else ""),
            "CONVERSION",
            f"gather.{key} differences ({kind} axis)",
        ),
        Number("the least interval", str(min(diffs)), "CONVERSION", f"gather.{key} differences"),
        Number("the greatest interval", str(max(diffs)), "CONVERSION", f"gather.{key} differences"),
    ]
    if us:
        numbers.append(
            Number(
                "the wheel's value u of each click, in order",
                ", ".join(str(u) for u in us[:24]) + (" ..." if len(us) > 24 else ""),
                "DETECTOR",
                "events.jsonl: gather.u",
            )
        )
        numbers.append(
            Number("distinct u among them", str(len(set(us))), "DETECTOR", "events.jsonl: gather.u")
        )
    if run.is_new and all("birth" in g and "click" in g for g in gathers):
        ages = [int(g["click"]) - int(g["birth"]) for g in gathers]
        numbers.append(
            Number(
                "each record's age at its click, in the record's ordering (click - birth)",
                ", ".join(str(a) for a in ages[:24]) + (" ..." if len(ages) > 24 else ""),
                "CONVERSION",
                "gather.click - gather.birth (GAMEBOARD integers)",
            )
        )
    return Panel(
        key="out_intervals",
        layer=3,
        title="The intervals between clicks",
        algebra=[
            (
                "The least time a detector times by itself is a pulse to its neighbour and its return, two intervals Inside, two of its counts at r_D = 1; the tick itself is GAMEBOARD and never read.",
                "ALGEBRA.md 3.4, discreteness Outside",
            )
        ],
        note="The differences of consecutive clicks' counts over every cell, as a histogram of exact integers, and the wheel's value of every click.",
        numbers=numbers,
        figure={"kind": "histogram", "values": diffs, "axis_kind": kind},
    )


def panel_outside_pattern(run: RunRecord) -> Panel:
    gathers = run.of_kind("gather")
    if not gathers:
        return Panel(
            "out_pattern", 3, "The pattern an experimenter sees", missing="no gather line in this run"
        )
    chosen = Counter(chosen_of(g) or "none" for g in gathers)
    names = [str(e.get("name")) for e in run.declared_detectors()]
    bars = [{"name": name, "count": chosen.get(name, 0)} for name in names]
    others = []
    for name, count in sorted(chosen.items()):
        if name not in names:
            others.append({"name": name, "count": count})
    numbers = [
        Number("gathers (the records' clicks)", str(len(gathers)), "DETECTOR", "events.jsonl: gather"),
        Number(
            "at the declared sets",
            str(sum(b["count"] for b in bars)),
            "DETECTOR",
            "events.jsonl: gather.chosen",
        ),
        Number(
            "elsewhere (the measured events, the faces)",
            str(sum(o["count"] for o in others)),
            "DETECTOR",
            "events.jsonl: gather.chosen",
        ),
        Number(
            "cells with at least one click",
            str(sum(1 for c in chosen.values() if c)),
            "DETECTOR",
            "events.jsonl: gather.chosen",
        ),
    ]
    reg = run.register
    if isinstance(reg, dict):
        for key, value in reg.items():
            if isinstance(value, (int, str)) and not isinstance(value, bool):
                numbers.append(
                    Number(
                        f"the register's {key}",
                        str(value),
                        "PIN",
                        "expectations.json (the world's block)",
                    )
                )
    if not bars:
        bars = others
        others = []
    return Panel(
        key="out_pattern",
        layer=3,
        title="The pattern an experimenter sees",
        algebra=[
            (
                "A click at a detector, a count between clicks on the detector's own record, and a ratio of such counts are what is compared with nature; nothing measured inside the board is compared; a reading of the board itself is a diagnostic.",
                "ALGEBRA.md 3.2, the reading rule",
            )
        ],
        note="One bar per declared set in the world file's order, the count of gathers whose chosen cell it is; the measured events' and the faces' beside. On a chain or a world of one detector the pattern is one bar. A register's number, where the series has one, is PIN; nothing is called matched; this page compares nothing.",
        numbers=numbers,
        figure={"kind": "bars", "bars": bars, "others": others},
    )


def head_numbers_run(run: RunRecord) -> list[Number]:
    """The head of a one-run page: the first page's head plus the engine."""
    found = head_numbers(run)
    found.insert(
        0,
        Number(
            "the engine, told from run.json's hypotheses",
            run.engine,
            "DECLARATION",
            "run.json: hypotheses",
        ),
    )
    found.insert(
        1,
        Number(
            "the identities",
            ", ".join(str(v) for v in run.meta.get("hypotheses", [])),
            "DECLARATION",
            "run.json: hypotheses",
        ),
    )
    if run.massive:
        found.insert(
            2,
            Number(
                "the massive record kind's key",
                str(run.meta.get("massive_record")),
                "DECLARATION",
                "run.json: massive_record",
            ),
        )
    found.append(
        Number(
            "the intervals requested",
            str(run.meta.get("requested_ticks")),
            "DECLARATION",
            "run.json: requested_ticks",
        )
    )
    if run.meta.get("error"):
        found.append(Number("the error", str(run.meta.get("error")), "HOST", "run.json: error"))
    return found


def build_run_panels(run: RunRecord, board_panels: list[Panel]) -> list[Panel]:
    """The thirteen panels of one run in the owner's three layers
    (DESIGN_3D.md sections 2 to 4): the algebra, the GameBoard (built by
    `board3d.build_layer`), the Outside."""
    return [
        panel_algebra_board(run),
        panel_algebra_families(run),
        panel_algebra_blocks(run),
        panel_algebra_instruments(run),
        panel_algebra_verbs(run),
        *board_panels,
        panel_outside_records(run),
        panel_outside_clock(run),
        panel_outside_intervals(run),
        panel_outside_pattern(run),
    ]
