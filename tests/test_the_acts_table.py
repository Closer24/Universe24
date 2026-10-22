"""Part D, Task 3, gate (3): the acts table as a test (the owner, issue #1793, comment 6077234684: "every act on a level is Rule3's one carried division; integers only; no shears, no rotation act, no sine or cosine, no tables, no declared acts on levels, no root anywhere; only the numbers at the Node"). Every .py of src/event_universe is parsed with `ast`; every call of `division_forward`, `division_back`, `rule3`, `rounded` (or `paces.rounded`), `link_factor`, `phase.act` or `act`, `phase.iterate` or `iterate`, `largest_below`, and every raw `//` or `%` (which tests/test_integer_algebra.py confines to core/rule3.py and the named index wraps) is a call site, keyed by (the file, the qualified name of the function holding it, the callee as written). INVENTORY is the table written by hand from what the code holds, each entry with its kind and a six-word reason: "R", a carried division on levels whose remainder is kept and returned into a record (Rule3's own step, the division act where the carry is a record's remainder); "D", a coefficient's division once, the remainder discarded (the coefficients, the Link factor, the roundings, the rooms, the bounds, the seeds, the index wraps); "S", a search by comparisons (`largest_below` and the bisections' probes). `phase.iterate` is one carried act on a pair and is listed under the one kind R at every site (Part H, the hands' SHOULD): the bisections around it (`paces.rotation_unit`, `meeting.quarter_turn`, their halving of the span) are S and D, and the fold's coefficient (`meeting.folded_lines`, `phase.fold`'s one rounding) is D; `math.gcd`, Euclid's remainders on coefficients (`credit.Books.unabsorbed_in`, `derived.held_write_of`, `digits.lattice_of`, `digits.read_of`, `features/click.bias_bound`), is a coefficient's division, D. A new division anywhere in src fails this test until it is listed with its kind."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "event_universe"
CALLEES = frozenset(
    {
        "division_forward",
        "division_back",
        "rule3",
        "carried_division",
        "rounded",
        "link_factor",
        "act",
        "iterate",
        "largest_below",
        "gcd",
    }
)
KINDS = frozenset({"R", "D", "S"})
STEP = (
    "core/rule3.py",
    "core/paces.py",
    "flux.py",
    "node.py",
    "plane.py",
    "lattice.py",
    "features/phase/__init__.py",
)

INVENTORY: dict[tuple[str, str, str], str] = {
    # core/rule3.py
    ("core/rule3.py", "carried_division", "//"): "R",  # the one carried division, remainder kept
    ("core/rule3.py", "rule3", "carried_division"): "R",  # the flux line's division, the law's step
    ("core/rule3.py", "division_forward", "carried_division"): "R",  # the division act forward
    ("core/rule3.py", "division_back", "carried_division"): "R",  # the division act back
    ("core/rule3.py", "link_factor", "division_forward"): "D",  # the Link's factor, once, discarded
    (
        "core/rule3.py",
        "largest_below",
        "division_forward",
    ): "D",  # halving the candidates' span, discarded
    # core/paces.py
    ("core/paces.py", "rounded", "division_forward"): "D",  # the rounding half up, once
    ("core/paces.py", "sine_den", "largest_below"): "S",  # the integer sine by the search
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
    (
        "features/phase/__init__.py",
        "rotation_unit",
        "division_forward",
    ): "D",  # the seed's multiple and the halving
    (
        "features/phase/__init__.py",
        "rotation_unit",
        "iterate",
    ): "R",  # the one carried act on a pair (the bisection around it S)
    (
        "features/phase/__init__.py",
        "quarter_turn",
        "division_forward",
    ): "D",  # halving the quarter turn's span
    ("features/phase/__init__.py", "quarter_turn", "iterate"): "R",  # the pair carried along the probe
    ("core/paces.py", "turn_factor", "rounded"): "D",  # the turn per interval, once
    # core/ports.py
    ("core/ports.py", "shifted", "%"): "D",  # the periodic index wrap, named exception
    # credit.py
    ("conversion.py", "sine_of", "largest_below"): "S",  # the pair's integer sine by the search
    ("credit.py", "Books.unabsorbed_in", "division_forward"): "D",  # the units' lcm and the share
    ("credit.py", "Books.unabsorbed_in", "gcd"): "D",  # Euclid's remainders on coefficients, once
    ("credit.py", "quanta_rounded", "paces.rounded"): "D",  # the side's gate, the count's rounding
    (
        "credit.py",
        "quanta_through",
        "division_forward",
    ): "R",  # the inflow over the unit, its remainder carried
    ("credit.py", "clocked_regions", "paces.rounded"): "D",  # the region's mean clock, rounded once
    (
        "credit.py",
        "clocked_regions",
        "division_forward",
    ): "R",  # the region's clock remainder kept in books
    # emission.py
    (
        "emission.py",
        "emitted_quantum",
        "division_forward",
    ): "D",  # the quantum's share over the parts laid alike, once
    ("emission.py", "radiated_total", "division_forward"): "D",  # the total's coefficients, once each
    ("emission.py", "radiated_total", "largest_below"): "S",  # the search on the total's square
    ("emission.py", "born_unit", "largest_below"): "S",  # the search on the unit's square
    ("emission.py", "born_unit", "division_forward"): "D",  # the unit over den squared, once
    ("emission.py", "packet_unit", "division_forward"): "D",  # den cos omega of the packet's wave, once
    ("emission.py", "laid_by_count", "division_forward"): "D",  # the count's lay, one division
    ("emission.py", "laid_packet", "division_forward"): "D",  # the envelope's part and the half cosine
    ("emission.py", "laid_packet", "rounded"): "D",  # the packet's levels, rounded once
    ("emission.py", "_offsets", "division_forward"): "D",  # the half width, an index
    ("emission.py", "start_of", "largest_below"): "S",  # the parts' sizes by the search
    ("emission.py", "start_of", "rounded"): "D",  # the start's two levels, rounded
    ("emission.py", "increments_of", "division_forward"): "D",  # the aimed share, once
    ("emission.py", "increments_of", "rounded"): "D",  # the increment, rounded once
    ("emission.py", "increments_of", "largest_below"): "S",  # the amplitude by the search
    ("emission.py", "holds_period", "division_forward"): "D",  # the doubled cosine, once
    ("emission.py", "advanced", "rounded"): "D",  # the recurrence's one rounding half up
    # guide.py, the guide clause of the emission
    ("guide.py", "half_angle", "division_forward"): "D",  # den (den + den cos) over two, once
    ("guide.py", "half_angle", "largest_below"): "S",  # the half angle's cosine by the search
    ("guide.py", "multiples", "division_forward"): "D",  # Chebyshev's recurrence, one division per step
    (
        "guide.py",
        "sine_of",
        "largest_below",
    ): "S",  # the sine by the search on den squared less cos squared
    ("guide.py", "modes_of", "//"): "D",  # the periodic width's half, an index
    ("guide.py", "modes_of", "%"): "D",  # the periodic width's parity, named
    ("guide.py", "travelling", "division_forward"): "D",  # den cos k of the guide's wave, once
    (
        "guide.py",
        "guide_total",
        "division_forward",
    ): "D",  # the total over the travelling share, one division
    # digits.py, the click's read of the board
    ("digits.py", "lattice_of", "gcd"): "D",  # the digits' lattice, Euclid on the rule's integers
    ("digits.py", "read_of", "division_forward"): "D",  # each digit its index on the lattice, r div F
    ("digits.py", "read_of", "gcd"): "D",  # the bases less one, the plain sum's modulus, once
    # features/click
    (
        "features/click/__init__.py",
        "drawn_from",
        "division_forward",
    ): "D",  # the click's read over the total, once per draw
    ("features/click/__init__.py", "bias_bound", "gcd"): "D",  # the total's shared factors, F
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
    (
        "features/click/__init__.py",
        "two_squares",
        "largest_below",
    ): "S",  # a plane's (re, im) by the search
    ("features/click/__init__.py", "plane_squares", "division_forward"): "D",  # the planes' target, once
    ("features/click/__init__.py", "direction", "largest_below"): "S",  # the pair's norm by the search
    (
        "features/click/__init__.py",
        "direction",
        "division_forward",
    ): "D",  # the direction's two levels, once
    (
        "features/click/__init__.py",
        "standing",
        "division_forward",
    ): "D",  # the before level, rounded once
    (
        "features/click/__init__.py",
        "invariant",
        "division_forward",
    ): "D",  # the invariant's quotient, once
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
        "wave_cosine",
        "division_forward",
    ): "D",  # the cosine's bisection, discarded
    ("features/click/__init__.py", "along_cosine", "division_forward"): "D",  # the along cosine, once
    ("features/click/__init__.py", "envelope", "division_forward"): "D",  # the slice's energy, once
    ("features/click/__init__.py", "envelope", "largest_below"): "S",  # the slice's amplitude by search
    # features/held_write
    ("features/held_write/__init__.py", "held_write", "act"): "R",  # the held write's remainder returned
    # features/phase
    ("features/phase/__init__.py", "half_wall", "division_forward"): "D",  # the half wall, once
    ("features/phase/__init__.py", "seed", "division_forward"): "D",  # the seed X div Gamma, once
    ("features/phase/__init__.py", "seed", "rounded"): "D",  # the seed's rounding, once
    ("features/phase/__init__.py", "act", "rule3"): "R",  # the phase line's carried step
    ("features/phase/__init__.py", "iterate", "act"): "R",  # the step repeated, remainders carried
    ("features/phase/__init__.py", "signed_rounded", "rounded"): "D",  # a signed rounding, once
    (
        "features/phase/__init__.py",
        "amplitude",
        "division_forward",
    ): "D",  # the width's amplitude, a bound
    # features/read
    ("features/read/__init__.py", "link_tension", "division_forward"): "D",  # the Link's tension, once
    ("features/read/__init__.py", "link_factors", "link_factor"): "D",  # the six Link factors, once
    ("features/read/__init__.py", "edge_squared", "division_forward"): "D",  # the edge's square, once
    ("features/read/__init__.py", "edge_of", "largest_below"): "S",  # the edge's pace by search
    # features/start
    (
        "features/start/__init__.py",
        "division",
        "division_forward",
    ): "D",  # the start's division, discarded
    (
        "features/start/__init__.py",
        "settled.act",
        "division_forward",
    ): "D",  # the lay's iteration, remainder discarded
    ("features/start/__init__.py", "settled", "act"): "D",  # the iteration to the fixed point
    ("features/start/__init__.py", "rest", "division_forward"): "D",  # the rest's rounding, once
    (
        "features/start/__init__.py",
        "without_uniform",
        "division_forward",
    ): "D",  # the carried torus's source less its read-weighted mean, discarded
    (
        "features/start/__init__.py",
        "recentred",
        "division_forward",
    ): "D",  # the carried torus's gauge, the levels' mean, discarded
    (
        "features/start/__init__.py",
        "settled_free",
        "division_forward",
    ): "D",  # the carried torus's iteration, remainder discarded
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
    # board_readings.py
    ("board_readings.py", "uniform_mode", "division_forward"): "D",  # the uniform level read, once
    ("lay.py", "shares_of", "division_forward"): "D",  # the shares' floors, once each
    # loader
    ("loader/faces.py", "connected", "%"): "D",  # a walked coordinate's wrap, named
    ("loader/derived.py", "FamilyRule.width", "//"): "D",  # exact, a row's lines, named
    ("loader/derived.py", "FamilyRule.planes", "//"): "D",  # exact, a part's planes, named
    ("loader/derived.py", "held_write_of", "division_forward"): "D",  # the held write's wall, once
    ("loader/derived.py", "held_write_of", "gcd"): "D",  # Euclid's remainders on coefficients, once
    ("loader/draw.py", "reduced_write", "gcd"): "D",  # the write's coefficients over their gcd, once
    ("loader/draw.py", "reduced_write", "division_forward"): "D",  # the reduction, exact, no remainder
    ("loader/rooms.py", "hill_scale", "division_forward"): "D",  # the hill's room, once
    ("loader/rooms.py", "tension_room", "largest_below"): "S",  # the room's factor by search
    ("loader/rooms.py", "tension_room", "division_forward"): "D",  # the room's ceiling, once
    (
        "loader/rooms.py",
        "write_rooms",
        "largest_below",
    ): "S",  # the covector's Link room, X 2^(1/2) by search
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
    ("loader/world.py", "even_box_refused", "division_forward"): "D",  # the extents' parity, once
    (
        "loader/instrument.py",
        "near_zone",
        "division_forward",
    ): "D",  # den div den sin k, the shell's radius
    ("loader/instrument.py", "near_zone", "largest_below"): "S",  # den sin k by the search, the radius
    ("loader/window.py", "passage", "division_forward"): "D",  # den cos omega and the passage's ceiling
    ("loader/window.py", "rate_passage", "division_forward"): "D",  # half the doubled cosine, once
    # lists.py
    ("lists.py", "hazard_weights", "rounded"): "D",  # the hazard's weight, rounded once
    ("lists.py", "absorption", "division_forward"): "D",  # the unit over the norm
    # take.py
    (
        "take.py",
        "recoil_phases",
        "largest_below",
    ): "S",  # den cos k_a from den sin k_a by search (2026-10-21)
    # node.py
    ("node.py", "phased", "phase.iterate"): "R",  # the record's phase line carried
    # flux.py, the step
    (
        "flux.py",
        "step_line",
        "rule3",
    ): "R",  # Rule3's flux line at every Node of a plain line, the law's step
    ("flux.py", "step_plane", "rule3"): "R",  # the same on each part of a turned or folded plane
    # node_detector.py
    ("node_detector.py", "books_of", "largest_below"): "S",  # the record's norm by search
    ("node_detector.py", "own_clock", "paces.rounded"): "D",  # the mean clock, rounded once
    ("node_detector.py", "clock_advanced", "division_forward"): "R",  # the reader's clock remainder kept
    ("node_detector.py", "drawn_weights", "division_forward"): "D",  # the inflow over the unit
    # plane.py, records.py
    ("plane.py", "sign_pairs", "paces.rounded"): "D",  # the sign's pair, rounded once
    ("records.py", "write_origins", "division_forward"): "D",  # the write's origin, once
    # resonance.py
    ("resonance.py", "references_of", "paces.rounded"): "D",  # the cosine record's level, rounded once
    ("resonance.py", "references_of", "division_forward"): "D",  # the sine record's level, the floor
    ("resonance.py", "turned_direction", "largest_below"): "S",  # the arriving size by search
    ("resonance.py", "turned_direction", "division_forward"): "D",  # the turned direction, floors
    ("resonance.py", "window_turn", "largest_below"): "S",  # the plane's size by search
    ("resonance.py", "window_turn", "division_forward"): "D",  # the turn over the scale
    ("resonance.py", "unit_weight", "largest_below"): "S",  # the sine and S_1 by search
    ("resonance.py", "unit_weight", "division_forward"): "D",  # (A_1 W)^2 over sin k, and the half
    ("resonance.py", "window_pair", "phase.iterate"): "R",  # the window's pair, remainders carried
    ("resonance.py", "hopped", "division_forward"): "R",  # the labels' hop, carries returned
    # covector.py
    ("covector.py", "link_fluxes", "division_forward"): "D",  # the pace squared off the pair, exact
    # readings.py
    (
        "readings.py",
        "turned_currents_of",
        "division_forward",
    ): "D",  # the pace squared off the pair, exact
    # share.py
    ("share.py", "over_pace", "division_forward"): "D",  # the share over the pace
    ("share.py", "quanta_of", "division_forward"): "D",  # the quanta's rounding, once
    ("share.py", "half_action", "division_forward"): "D",  # T div 2, the count's unit of a plane record
    (
        "resonance.py",
        "projected",
        "division_forward",
    ): "D",  # the gradient's half on the dipole, the carry kept
}

# the carried divisions outside the step, named and reported, not moved (Part D, Task 3):
R_OUTSIDE_THE_STEP = frozenset(
    {
        (
            "credit.py",
            "clocked_regions",
            "division_forward",
        ),  # a region's clock, its remainder in the books
        ("credit.py", "quanta_through", "division_forward"),  # the credit's remainder carried per record
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
