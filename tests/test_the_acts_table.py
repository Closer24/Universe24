"""Part D, Task 3, gate (3): the acts table as a test (the owner, issue #1793, comment 6077234684: "every act on a level is Rule3's one carried division; integers only; no shears, no rotation act, no sine or cosine, no tables, no declared acts on levels, no root anywhere; only the numbers at the Node"). Every .py of src/event_universe is parsed with `ast`; every call of `division_forward`, `division_back`, `rule3`, `rounded` (or `paces.rounded`), `link_factor`, `phase.act` or `act`, `phase.iterate` or `iterate`, `largest_below`, and every raw `//` or `%` (which tests/test_integer_algebra.py confines to core/rule3.py and the named index wraps) is a call site, keyed by (the file, the qualified name of the function holding it, the callee as written). INVENTORY is the table written by hand from what the code holds, each entry with its kind and a six-word reason: "R", a carried division on levels whose remainder is kept and returned into a record (Rule3's own step, the division act where the carry is a record's remainder); "D", a coefficient's division once, the remainder discarded (the coefficients, the Link factor, the roundings, the rooms, the bounds, the seeds, the index wraps); "S", a search by comparisons (`largest_below` and the bisections' probes); the volume form's level reading (features/volume, `searched_levels` under `level_of`) is a search by comparisons with its halving listed as S, as `largest_below` is, and the volume of a level at the start one division D. `phase.iterate` is one carried act on a pair and is listed under the one kind R at every site (Part H, the hands' SHOULD): the bisections around it (`paces.rotation_unit`, `meeting.quarter_turn`, their halving of the span) are S and D, and the fold's coefficient (`meeting.folded_lines`, `phase.fold`'s one rounding) is D; `math.gcd`, Euclid's remainders on coefficients (`credit.Books.unabsorbed_in`, `derived.held_write_of`, `digits.lattice_of`, `digits.read_of`, `features/click.bias_bound`), is a coefficient's division, D. A new division anywhere in src fails this test until it is listed with its kind."""

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
    ("seed.py", "drift_of", "largest_below"): "S",  # the seed's drift v^2 <= T by the search
    ("meeting_board.py", "meetings", "division_forward"): "D",  # the Node's own count, once
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
        "records.py",
        "pressure_term",
        "paces.rounded",
    ): "D",  # the stress's trace in the energy's units, once
    ("records.py", "write_sources", "paces.rounded"): "D",  # the fixed wall's ratio, rounded once
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
    # act.py, the born pair
    (
        "act.py",
        "born_pair",
        "division_forward",
    ): "D",  # the whole quanta standing at the Node, the floor once
    # conversion.py
    ("conversion.py", "sine_of", "largest_below"): "S",  # the pair's integer sine by the search
    # emission.py
    ("emission.py", "laid_by_count", "division_forward"): "D",  # the count's lay, one division
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
    (
        "features/currents/__init__.py",
        "level_term",
        "division_forward",
    ): "D",  # the Link's level term's half, the floor once, discarded (The booking is the frame's, 2026-10-23)
    ("features/click/__init__.py", "face_value", "division_forward"): "D",  # the face's value, once
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
        "Orbit.carried_to",
        "act",
    ): "R",  # the orbit's step from the seed, remainders carried
    (
        "features/phase/__init__.py",
        "Orbit.carried_to",
        "division_forward",
    ): "D",  # the checkpoint's place by the spacing, an index
    (
        "features/phase/__init__.py",
        "Orbit.pairs_at",
        "division_forward",
    ): "D",  # the checkpoint below a count, an index
    (
        "features/phase/__init__.py",
        "Orbit.pairs_at",
        "iterate",
    ): "R",  # the Links carried by the rest, remainders carried
    (
        "features/phase/__init__.py",
        "amplitude",
        "division_forward",
    ): "D",  # the width's amplitude, a bound
    # features/volume, the volume form's level reading and the start's conversion
    (
        "features/volume/__init__.py",
        "clock_zero",
        "division_forward",
    ): "D",  # halving the search, discarded
    ("features/volume/__init__.py", "volume_of", "division_forward"): "D",  # the level's volume, once
    (
        "features/volume/__init__.py",
        "searched_levels",
        "division_forward",
    ): "S",  # the reading's halving, by search
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
    (
        "features/start/rests.py",
        "damped",
        "division_forward",
    ): "D",  # the damped pass's mean, carry dropped at the stop
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
    # lattice.py, lay.py
    ("lattice.py", "Lattice.half_wall", "division_forward"): "D",  # the half wall, once
    # board_readings.py
    ("board_readings.py", "uniform_mode", "division_forward"): "D",  # the uniform level read, once
    ("lay.py", "shares_of", "division_forward"): "D",  # the shares' floors, once each
    # loader
    ("loader/derived.py", "FamilyRule.width", "//"): "D",  # exact, a row's lines, named
    ("loader/derived.py", "FamilyRule.planes", "//"): "D",  # exact, a part's planes, named
    (
        "loader/charge.py",
        "pythagorean_readers",
        "largest_below",
    ): "D",  # the integer sine of a sign reader's pair, the search on the share reading, once (the sign's reader is Pythagorean, 2026-10-24)
    (
        "loader/charge.py",
        "charge_factors",
        "division_forward",
    ): "D",  # the readers' count units to one wall and the factors reduced, exact, no remainder (The constants, 2026-10-24)
    (
        "loader/charge.py",
        "charge_factors",
        "gcd",
    ): "D",  # Euclid's remainders on the count units and the factors, once each
    # the lightest point of the circle (2026-10-24): the loader's number theory on den, every division the act
    ("loader/charge.py", "primes_below", "division_forward"): "D",  # trial division's remainders
    ("loader/charge.py", "is_prime", "division_forward"): "D",  # n - 1 = d 2^s, the remainders by 2
    ("loader/charge.py", "split", "gcd"): "D",  # Pollard's rho, Euclid on |x - y| and n
    ("loader/charge.py", "factors", "division_forward"): "D",  # 2 divided out, the cofactor of a split
    (
        "loader/charge.py",
        "two_squares",
        "division_forward",
    ): "D",  # (p - 1) div 4 and Euclid's remainders
    ("loader/charge.py", "two_squares", "largest_below"): "D",  # the root of p, the remainders' floor
    ("loader/charge.py", "lightest_point", "division_forward"): "D",  # a prime's class modulo 4
    (
        "loader/rooms.py",
        "held_room",
        "largest_below",
    ): "D",  # a held write's level bound inside the width, the search on the share reading
    (
        "loader/rooms.py",
        "held_room",
        "division_forward",
    ): "D",  # (largest - wall) div room, once per line
    (
        "loader/rooms.py",
        "width_of",
        "division_forward",
    ): "D",  # halving the width's search, discarded (the width derived, 2026-10-24)
    ("loader/derived.py", "held_write_of", "division_forward"): "D",  # the held write's wall, once
    ("loader/derived.py", "held_write_of", "gcd"): "D",  # Euclid's remainders on coefficients, once
    (
        "loader/derived.py",
        "alpha_of",
        "division_forward",
    ): "D",  # the pairs and the law's alpha reduced by the division act, once each
    (
        "loader/derived.py",
        "alpha_of",
        "gcd",
    ): "D",  # Euclid's remainders on the pair's and the ratio's integers, once each
    ("loader/rooms.py", "hill_scale", "division_forward"): "D",  # the hill's room, once
    ("loader/rooms.py", "tension_room", "largest_below"): "S",  # the room's factor by search
    ("loader/rooms.py", "tension_room", "division_forward"): "D",  # the room's ceiling, once
    (
        "loader/derived.py",
        "bound_under_rooms",
        "division_forward",
    ): "D",  # the bound's quotients, once each
    ("loader/derived.py", "bound_under_rooms", "largest_below"): "S",  # the largest level by search
    ("loader/world.py", "even_box_refused", "division_forward"): "D",  # the extents' parity, once
    # node.py
    (
        "node.py",
        "phase_carried",
        "phase.iterate",
    ): "R",  # the record's phase line carried to the count the state stands at (2026-10-23)
    (
        "node.py",
        "phase_rows",
        "act",
    ): "R",  # the Node's phase row at the wall 2 with the write 2 c, division_forward or division_back by direction, its remainder the record's frame (the frame clause, 2026-10-23)
    # flux.py, the step
    (
        "flux.py",
        "step_line",
        "rule3",
    ): "R",  # Rule3's flux line at every Node of a plain line, the law's step
    ("flux.py", "step_plane", "rule3"): "R",  # the same on each part of a turned or folded plane
    ("flux.py", "step_traceless", "rule3"): "R",  # the tension lines' traceless step, wall 3 w
    (
        "flux.py",
        "step_momentum",
        "division_forward",
    ): "R",  # the shear's momentum at the volume's wall, remainder kept
    # plane.py, records.py
    ("plane.py", "sign_pairs", "paces.rounded"): "D",  # the sign's pair, rounded once
    ("records.py", "write_origins", "division_forward"): "D",  # the write's origin, once
    # share.py
    ("share.py", "over_pace", "division_forward"): "D",  # the share over the pace
    ("share.py", "quanta_of", "division_forward"): "D",  # the quanta's rounding, once
    ("share.py", "half_action", "division_forward"): "D",  # T div 2, the count's unit of a plane record
}

# the carried divisions outside the step, named and reported, not moved (Part D, Task 3):
R_OUTSIDE_THE_STEP = frozenset(
    {
        ("features/held_write/__init__.py", "held_write", "act"),  # the held write's remainder
        ("features/write/__init__.py", "carried", "division_forward"),  # the write's remainder forward
        ("features/write/__init__.py", "carried", "division_back"),  # the write's remainder back
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


def test_the_fifth_act_the_swap_at_the_top_divides_nothing_and_is_its_own_inverse():
    """The acts table's fifth row (ALGEBRA.md, The swap at the top; swap.py): the swap at the top is a bijection and an involution on the Node's state, no division of any kind: every line's two levels exchanged and every remainder complemented at its wall by `records.complement` (wall - 1 - r, the ones' complement, whose square is the identity), so the module holds no call site of the acts table (no `//`, no division act) and its one arithmetic is the complement; the trigger reads three levels by comparisons alone."""
    source = (ROOT / "src" / "event_universe" / "swap.py").read_text(encoding="utf-8")
    assert "records.complement(" in source and "//" not in source.replace('"""', "")
    assert (
        "division_forward" not in source
        and "division_back" not in source
        and "carried_division" not in source
    )
    assert all(f"{path}" != "swap.py" for path, _function, _act in INVENTORY)
