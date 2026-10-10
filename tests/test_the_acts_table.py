"""Part D, Task 3, gate (3): the acts table as a test (the owner, issue #1793, comment 6077234684: "every act on a level is Rule3's one carried division; integers only; no shears, no rotation act, no sine or cosine, no tables, no declared acts on levels, no root anywhere; only the numbers at the Node"). Every .py of src/event_universe is parsed with `ast`; every call of `division_forward`, `division_back`, `rule3`, `rounded` (or `paces.rounded`), `link_factor`, `phase.act` or `act`, `phase.iterate` or `iterate`, `largest_below`, and every raw `//` or `%` (which tests/test_integer_algebra.py confines to core/rule3.py and the named index wraps) is a call site, keyed by (the file, the qualified name of the function holding it, the callee as written). INVENTORY is the table written by hand from what the code holds, each entry with its kind and a six-word reason: "R", a carried division on levels whose remainder is kept and returned into a record (Rule3's own step, the division act where the carry is a record's remainder); "D", a coefficient's division once, the remainder discarded (the coefficients, the Link factor, the roundings, the rooms, the bounds, the seeds, the index wraps); "S", a search by comparisons (`largest_below` and the bisections' probes). A new division anywhere in src fails this test until it is listed with its kind."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "event_universe"
CALLEES = frozenset(
    {
        "division_forward",
        "division_back",
        "rule3",
        "rounded",
        "link_factor",
        "act",
        "iterate",
        "largest_below",
    }
)
KINDS = frozenset({"R", "D", "S"})
STEP = (
    "core/rule3.py",
    "core/paces.py",
    "node.py",
    "plane.py",
    "lattice.py",
    "features/phase/__init__.py",
)

INVENTORY: dict[tuple[str, str, str], str] = {
    # core/rule3.py
    ("core/rule3.py", "rule3", "//"): "R",  # the one carried division, remainder kept
    ("core/rule3.py", "division_forward", "rule3"): "R",  # the division act forward, carry given
    ("core/rule3.py", "division_back", "rule3"): "R",  # the division act back, carry given
    ("core/rule3.py", "link_factor", "division_forward"): "D",  # the Link's factor, once, discarded
    (
        "core/rule3.py",
        "largest_below",
        "division_forward",
    ): "D",  # halving the candidates' span, discarded
    # core/paces.py
    ("core/paces.py", "rounded", "division_forward"): "D",  # the rounding half up, once
    ("core/paces.py", "clock_alone", "rounded"): "D",  # the clock from the content, once
    ("core/paces.py", "Side.reach", "rounded"): "D",  # the side's table of clocks, once
    ("core/paces.py", "frozen_content", "rounded"): "D",  # the bisection's probe, a clock reading
    (
        "core/paces.py",
        "frozen_content",
        "division_forward",
    ): "D",  # halving the bisection's span, discarded
    ("core/paces.py", "axis_pace", "rounded"): "D",  # the axis pace, one rounding
    ("core/paces.py", "write_factor", "rounded"): "D",  # the write's factor, one rounding
    ("core/paces.py", "rotation_unit", "division_forward"): "D",  # the seed's multiple and the halving
    ("core/paces.py", "rotation_unit", "phase.iterate"): "S",  # the bisection's probe on the line
    ("core/paces.py", "turn_factor", "rounded"): "D",  # the turn per interval, once
    # core/ports.py
    ("core/ports.py", "shifted", "%"): "D",  # the periodic index wrap, named exception
    ("core/ports.py", "run_offsets", "%"): "D",  # the run's offsets around the ring
    # credit.py
    ("credit.py", "Books.unabsorbed_in", "division_forward"): "D",  # the units' lcm and the share
    ("credit.py", "record_unit", "division_forward"): "D",  # the mean unit rounded half up
    ("credit.py", "quanta_through", "division_forward"): "D",  # the inflow over the unit, rounded
    (
        "credit.py",
        "clocked_regions",
        "division_forward",
    ): "R",  # the region's clock remainder kept in books
    # emission.py
    ("emission.py", "radiated_total", "division_forward"): "D",  # the total's coefficients, once each
    ("emission.py", "radiated_total", "largest_below"): "S",  # the search on the total's square
    ("emission.py", "born_unit", "largest_below"): "S",  # the search on the unit's square
    ("emission.py", "born_unit", "division_forward"): "D",  # the unit over den squared, once
    ("emission.py", "laid_by_count", "division_forward"): "D",  # the count's lay, one division
    ("emission.py", "laid_packet", "largest_below"): "S",  # the sine and the transverse size
    ("emission.py", "laid_packet", "division_forward"): "D",  # the packet's levels, rounded once
    ("emission.py", "_offsets", "division_forward"): "D",  # the half width, an index
    ("emission.py", "start_of", "largest_below"): "S",  # the parts' sizes by the search
    ("emission.py", "start_of", "division_forward"): "D",  # the start's two levels, rounded
    ("emission.py", "increments_of", "division_forward"): "D",  # the aimed share and the increment
    ("emission.py", "increments_of", "largest_below"): "S",  # the amplitude by the search
    ("emission.py", "holds_period", "division_forward"): "D",  # the doubled cosine, once
    ("emission.py", "advanced", "division_forward"): "D",  # the recurrence's one rounding half up
    # features/click
    ("features/click/__init__.py", "drawn", "division_forward"): "D",  # the draw's shares, once each
    ("features/click/__init__.py", "face_value", "division_forward"): "D",  # the face's value, once
    ("features/click/__init__.py", "presented", "division_forward"): "D",  # the presented share, once
    ("features/click/__init__.py", "squared", "largest_below"): "S",  # the search on the lay's square
    (
        "features/click/__init__.py",
        "squared",
        "division_forward",
    ): "D",  # the lay's quotient before the search
    ("features/click/__init__.py", "spread", "largest_below"): "S",  # the search on the spread square
    ("features/click/__init__.py", "spread", "division_forward"): "D",  # the Node's share of the square
    ("features/click/__init__.py", "amplitude", "largest_below"): "S",  # the amplitude by the search
    ("features/click/__init__.py", "direction", "largest_below"): "S",  # the pair's norm by the search
    (
        "features/click/__init__.py",
        "direction",
        "division_forward",
    ): "D",  # the direction's two levels, once
    ("features/click/__init__.py", "standing", "largest_below"): "S",  # the sine den by the search
    (
        "features/click/__init__.py",
        "standing",
        "division_forward",
    ): "D",  # the before level, rounded once
    ("features/click/__init__.py", "invariant", "largest_below"): "S",  # the sine den by the search
    (
        "features/click/__init__.py",
        "invariant",
        "division_forward",
    ): "D",  # the invariant's quotient, once
    ("features/click/__init__.py", "laid_pairs", "largest_below"): "S",  # the sine den by the search
    (
        "features/click/__init__.py",
        "laid_pairs",
        "division_forward",
    ): "D",  # the pairs' levels, once each
    (
        "features/click/__init__.py",
        "exact_total",
        "division_forward",
    ): "D",  # the total's quotient before search
    ("features/click/__init__.py", "exact_total", "largest_below"): "S",  # the search on the total
    ("features/click/__init__.py", "line_total", "largest_below"): "S",  # the search on the line's total
    (
        "features/click/__init__.py",
        "line_total",
        "division_forward",
    ): "D",  # the line's quotient before search
    (
        "features/click/__init__.py",
        "rotated",
        "rule3",
    ): "R",  # the lay's recurrence carrying its remainder
    (
        "features/click/__init__.py",
        "transverse_cosine",
        "division_forward",
    ): "D",  # the cosine's bisection, discarded
    ("features/click/__init__.py", "along_cosine", "division_forward"): "D",  # the along cosine, once
    ("features/click/__init__.py", "envelope", "division_forward"): "D",  # the slice's energy, once
    ("features/click/__init__.py", "envelope", "largest_below"): "S",  # the slice's amplitude by search
    # features/held_write
    ("features/held_write/__init__.py", "held_write", "act"): "R",  # the held write's remainder returned
    # features/phase
    ("features/phase/__init__.py", "half_wall", "rule3"): "D",  # the half wall, once
    ("features/phase/__init__.py", "seed", "rule3"): "D",  # the seed X div Gamma, once
    ("features/phase/__init__.py", "seed", "rounded"): "D",  # the seed's rounding, once
    ("features/phase/__init__.py", "act", "rule3"): "R",  # the phase line's carried step
    ("features/phase/__init__.py", "iterate", "act"): "R",  # the step repeated, remainders carried
    ("features/phase/__init__.py", "signed_rounded", "rounded"): "D",  # a signed rounding, once
    ("features/phase/__init__.py", "amplitude", "rule3"): "D",  # the width's amplitude, a bound
    # features/read
    ("features/read/__init__.py", "link_tension", "division_forward"): "D",  # the Link's tension, once
    ("features/read/__init__.py", "link_factors", "link_factor"): "D",  # the six Link factors, once
    ("features/read/__init__.py", "edge_squared", "division_forward"): "D",  # the edge's square, once
    ("features/read/__init__.py", "edge_of", "largest_below"): "S",  # the edge's pace by search
    # features/start
    ("features/start/__init__.py", "division", "rule3"): "D",  # the start's division, discarded
    (
        "features/start/__init__.py",
        "settled.act",
        "rule3",
    ): "D",  # the lay's iteration, remainder discarded
    ("features/start/__init__.py", "settled", "act"): "D",  # the iteration to the fixed point
    ("features/start/__init__.py", "refined", "rule3"): "D",  # the numerator at wall 1
    ("features/start/__init__.py", "rest", "rule3"): "D",  # the rest's rounding, once
    # features/write
    (
        "features/write/__init__.py",
        "carried",
        "division_forward",
    ): "R",  # the write's remainder returned forward
    (
        "features/write/__init__.py",
        "carried",
        "division_back",
    ): "R",  # the write's remainder returned back
    # growth.py
    ("growth.py", "reached", "%"): "D",  # a line's index wrap, named
    ("growth.py", "resized", "%"): "D",  # a line's index wrap, named
    # lattice.py, lay.py
    ("lattice.py", "Lattice.half_wall", "division_forward"): "D",  # the half wall, once
    ("lay.py", "shares_of", "division_forward"): "D",  # the shares' floors, once each
    # loader
    ("loader/faces.py", "connected", "%"): "D",  # a walked coordinate's wrap, named
    ("loader/derived.py", "FamilyRule.width", "//"): "D",  # exact, a row's lines, named
    ("loader/derived.py", "FamilyRule.planes", "//"): "D",  # exact, a part's planes, named
    ("loader/derived.py", "count_wall", "largest_below"): "S",  # the quantum's wall by search
    ("loader/derived.py", "held_write_of", "division_forward"): "D",  # the held write's wall, once
    ("loader/derived.py", "hill_scale", "division_forward"): "D",  # the hill's room, once
    ("loader/derived.py", "tension_room", "largest_below"): "S",  # the room's factor by search
    ("loader/derived.py", "tension_room", "division_forward"): "D",  # the room's ceiling, once
    (
        "loader/derived.py",
        "bound_under_rooms",
        "division_forward",
    ): "D",  # the bound's quotients, once each
    ("loader/derived.py", "bound_under_rooms", "largest_below"): "S",  # the largest level by search
    ("loader/lay.py", "least_action", "division_forward"): "D",  # the budget's quotient, once
    (
        "loader/node_detector_declaration.py",
        "packet_form",
        "division_forward",
    ): "D",  # the half width, an index
    (
        "loader/universe.py",
        "composed_pair",
        "division_forward",
    ): "D",  # the composed pair's quotients, once
    ("loader/universe.py", "composed_pair", "largest_below"): "S",  # the sines and the norm
    ("loader/world.py", "even_box_refused", "division_forward"): "D",  # the extents' parity, once
    # meeting.py
    ("meeting.py", "hazard_weights", "division_forward"): "D",  # the hazard's weight, rounded once
    ("meeting.py", "absorbed", "division_forward"): "D",  # the unit over the norm
    ("meeting.py", "scaled", "division_forward"): "D",  # a P over num, once per axis
    ("meeting.py", "quarter_turn", "division_forward"): "D",  # halving the quarter turn's span
    ("meeting.py", "quarter_turn", "phase.iterate"): "S",  # the bisection's probe on the cosine
    ("meeting.py", "folded_lines", "phase.iterate"): "D",  # the fold's pair, once per offset
    ("meeting.py", "twisted", "division_forward"): "D",  # halving the twist's span, discarded
    # node.py
    ("node.py", "phased", "phase.iterate"): "R",  # the record's phase line carried
    ("node.py", "step", "rule3"): "R",  # Rule3's step at every Node
    # node_detector.py
    ("node_detector.py", "books_of", "largest_below"): "S",  # the record's norm by search
    ("node_detector.py", "arriving", "division_forward"): "D",  # the projected level, rounded once
    ("node_detector.py", "own_clock", "division_forward"): "D",  # the mean clock, rounded once
    ("node_detector.py", "clock_advanced", "division_forward"): "R",  # the reader's clock remainder kept
    ("node_detector.py", "drawn_weights", "division_forward"): "D",  # the inflow over the unit
    ("node_detector.py", "piece_momentum", "division_forward"): "D",  # one count's P over the share
    # plane.py, records.py
    ("plane.py", "sign_pairs", "paces.rounded"): "D",  # the sign's pair, rounded once
    ("plane.py", "step_plane", "rule3"): "R",  # Rule3's step on the plane
    ("records.py", "write_origins", "rule3"): "D",  # the write's origin, once
    # resonance.py
    ("resonance.py", "references_of", "division_forward"): "D",  # the references' levels, rounded once
    ("resonance.py", "references_of", "largest_below"): "S",  # the sine's level by search
    ("resonance.py", "turned_direction", "largest_below"): "S",  # the arriving size by search
    ("resonance.py", "turned_direction", "division_forward"): "D",  # the turned direction, floors
    ("resonance.py", "window_turn", "largest_below"): "S",  # the plane's size by search
    ("resonance.py", "window_turn", "division_forward"): "D",  # the turn over the scale
    ("resonance.py", "window_pair", "phase.iterate"): "R",  # the window's pair, remainders carried
    ("resonance.py", "hopped", "division_forward"): "R",  # the labels' hop, carries returned
    # share.py
    ("share.py", "over_pace", "rule3"): "D",  # the share over the pace
    ("share.py", "share", "rule3"): "D",  # the Link's reading, wall 1
    ("share.py", "quanta_of", "rule3"): "D",  # the quanta's rounding, once
}

# the carried divisions outside the step, named and reported, not moved (Part D, Task 3):
R_OUTSIDE_THE_STEP = frozenset(
    {
        (
            "credit.py",
            "clocked_regions",
            "division_forward",
        ),  # a region's clock, its remainder in the books
        ("features/click/__init__.py", "rotated", "rule3"),  # the lay's recurrence with its carry
        ("features/held_write/__init__.py", "held_write", "act"),  # the held write's remainder
        ("features/write/__init__.py", "carried", "division_forward"),  # the write's remainder forward
        ("features/write/__init__.py", "carried", "division_back"),  # the write's remainder back
        ("node_detector.py", "clock_advanced", "division_forward"),  # the reader's clock remainder
        ("resonance.py", "window_pair", "phase.iterate"),  # the window's pair in the memo
        ("resonance.py", "hopped", "division_forward"),  # the labels' hop with its carries
    }
)


def call_sites() -> dict[tuple[str, str, str], list[int]]:
    """Every call site of the acts in src, keyed as INVENTORY is, with its lines."""
    found: dict[tuple[str, str, str], list[int]] = {}

    def visit(node: ast.AST, name: str, quals: list[str]) -> None:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            quals = [*quals, node.name]
        where = ".".join(quals) or "<module>"
        if isinstance(node, ast.Call):
            callee = node.func
            short = callee.id if isinstance(callee, ast.Name) else getattr(callee, "attr", None)
            if short in CALLEES:
                found.setdefault((name, where, ast.unparse(callee)), []).append(node.lineno)
        if isinstance(node, ast.BinOp | ast.AugAssign) and isinstance(node.op, ast.FloorDiv | ast.Mod):
            sign = "//" if isinstance(node.op, ast.FloorDiv) else "%"
            found.setdefault((name, where, sign), []).append(node.lineno)
        for child in ast.iter_child_nodes(node):
            visit(child, name, quals)

    for path in sorted(SOURCE.rglob("*.py")):
        visit(ast.parse(path.read_text(encoding="utf-8")), path.relative_to(SOURCE).as_posix(), [])
    return found


def test_the_acts_table_lists_every_division_of_src_with_its_kind():
    """The set of call sites found equals the set of INVENTORY's keys (an unlisted division fails; a listed one gone fails), every kind is R, D or S, and every R stands inside the step (STEP: core/rule3.py, core/paces.py, node.py, plane.py, lattice.py, features/phase) except the named R_OUTSIDE_THE_STEP, each a remainder returned into a record by the write, the clocks, the lay's recurrence or the window's labels; the counts by kind are printed for the Boss."""
    found = call_sites()
    unlisted = {f"{k[0]}:{k[1]} {k[2]} L{found[k]}" for k in found if k not in INVENTORY}
    gone = {f"{k[0]}:{k[1]} {k[2]}" for k in INVENTORY if k not in found}
    assert not unlisted and not gone, {"unlisted": sorted(unlisted), "gone": sorted(gone)}
    assert set(INVENTORY.values()) <= KINDS
    carried = {key for key, kind in INVENTORY.items() if kind == "R"}
    outside = {key for key in carried if key[0] not in STEP}
    assert outside == R_OUTSIDE_THE_STEP, sorted(outside ^ R_OUTSIDE_THE_STEP)
    counts = {kind: sum(1 for k in INVENTORY.values() if k == kind) for kind in sorted(KINDS)}
    print("the acts table by kind", counts, "sites", sum(len(lines) for lines in found.values()))
    assert counts["R"] + counts["D"] + counts["S"] == len(INVENTORY)
