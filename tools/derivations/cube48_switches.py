"""The cube 48 on the board (cube48, 2026-10-24; a test-local script in the worktree cube48_wt at origin/main, no key of any
file, nothing of the engine changed): the law's seed (the hole at the origin), the plus-one seed or the faces seed on a bare torus
at a toy den, run interval by interval with
  (a) the invariance test: the state compared with its image under every element of the 48 (the signed permutations of the axes
      about the origin), the levels, the remainders, the write remainders and the phase lines apart, per interval; the first
      interval and orbit that is not uniform; and the commutation test: at an interval the state is copied, transformed by a
      generator of the 48 (or by the conjugation C), both stepped once, and the stepped image compared with the image of the
      stepped: the first act that does not commute, by the line and the Node;
  (b) the orbit quotient: per interval and orbit the seed's levels, the share q, the digits' sum;
  (c) the read as a switch: ordered (the shipped Port order), sorted (the six Ports' digits sorted by value), sum (the digits'
      plain sum), link (a digit per Link: the neighbour's remainder on the LINK'S lattice F_ij = gcd(w, R_ji, R^c_ji, R^s_ji),
      the Node's own on its own lattice, the sorted multiset in the mixed radix), link_sum (the Link digits and the Node's, the
      digits at the lay's origin left out, the plain sum, the draw the sum modulo the total, no moduli); the selector: main (the
      heaviest whose walls fit, the shipped child_of) or aprime (the primes' lifts that fit, drawn at equal weights by the read);
      the hole: zero (main's, the met Node's seed lines to (0, 0)), mean (the frame's uniform part by Rule3's division at the wall,
      the ruling of 13:33, which fails: it keeps the drift), before_mean ((b_u, b_u), b_u the six Ports' before over PORTS by the
      division act, the remainder kept whole), own_before ((b_i, b_i), the Node's own before twice);
  (d) the mirror lay: W per record at every born Node right after the lay;
  (e) the mirror run: the whole run from the image of the start under one element, compared interval by interval;
  (f) the two-tiles test: the torus cut in two x-tiles with one-Link halos, each a lattice of its own, each stepped from its own
      state and its halos at the tick before, the halos exchanged after, the interiors compared with the board bit for bit
      (tests/test_two_tiles_with_skewed_clocks_run_the_board.py's form): the first interval and array at which they part.
Usage: cube48.py --den D --cube L --intervals N --seed {hole,plus1,faces} --read {ordered,sorted,sum,link,link_sum}
       --select {main,aprime} --hole {zero,mean,before_mean,own_before} --prefix PATH [--commute N] [--commute-every K]
       [--mirror ELEMENT] [--tiles] [--no-all48] [--digits-table]"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections import Counter
from itertools import permutations, product
from math import gcd
from pathlib import Path

import numpy as np

from event_universe import conversion, credit, flux, meeting_board, records, share
from event_universe.act import born_items, click
from event_universe.core.ports import AXES, PORTS
from event_universe.core.rule3 import division_forward, largest_below, wall_of
from event_universe.digits import at_origin, digits_of, frame_of, lattice_of, picked, ruled
from event_universe.digits import read_of as read_ordered
from event_universe.emission import emitted_lines
from event_universe.features import phase
from event_universe.features.click import drawn_from, read_number
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.circle import angled
from event_universe.loader.derived import count_wall, quanta_records
from event_universe.meeting_board import child_of, meetings, readings_at
from event_universe.readings import ports
from event_universe.reports import birth_line
from event_universe.reports import credit as credit_line
from event_universe.seed import drift_of
from event_universe.world_files import load_world

# ----------------------------------------------------------------------------------------------------------------------
# the 48
# ----------------------------------------------------------------------------------------------------------------------
AXIS_NAMES = "xyz"


def elements():
    """The 48 signed permutations (perm, signs): (P x)_i = signs[i] x[perm[i]]."""
    return [(perm, signs) for perm in permutations(range(3)) for signs in product((1, -1), repeat=3)]


def name_of(element):
    perm, signs = element
    return "".join(AXIS_NAMES[p] for p in perm) + "," + "".join("+" if s > 0 else "-" for s in signs)


GENERATORS = [
    ((0, 1, 2), (-1, 1, 1)),  # the reflection of x
    ((0, 1, 2), (1, -1, 1)),  # the reflection of y
    ((0, 1, 2), (1, 1, -1)),  # the reflection of z
    ((1, 2, 0), (1, 1, 1)),  # the cyclic turn of the axes (a rotation about the diagonal)
    ((1, 0, 2), (1, 1, 1)),  # the transposition of x and y (a reflection in the diagonal plane)
]


class Transform:
    """One element's action on the arrays of a board of shape (L, L, L) about the origin: `scalar` moves A to A' with
    A'[P x] = A[x]; `owned(axis)` moves a +axis Link's line to its image Link's owner (P x - e_axis where that axis is flipped);
    `axis_of(i)` the old axis the new axis i is the image of, with its sign."""

    def __init__(self, element, shape):
        self.perm, self.signs = element
        L = shape[0]
        assert shape == (L, L, L)
        grid = np.indices(shape).reshape(3, -1)
        image = np.stack([(self.signs[i] * grid[self.perm[i]]) % L for i in range(3)])
        self.source = tuple(grid)
        self.target = tuple(image)
        self.shifted = {}
        for i in range(3):
            moved = image.copy()
            if self.signs[i] < 0:
                moved[i] = (moved[i] - 1) % L
            self.shifted[i] = tuple(moved)

    def scalar(self, a):
        a = np.asarray(a)
        found = np.empty_like(a)
        found[self.target] = a[self.source]
        return found

    def owned(self, a, axis):
        a = np.asarray(a)
        found = np.empty_like(a)
        found[self.shifted[axis]] = a[self.source]
        return found

    def axis_of(self, new_axis):
        return self.perm[new_axis], self.signs[new_axis]


def complement(remainder, wall):
    return np.asarray(wall, dtype=object) - 1 - np.asarray(remainder, dtype=object)


def line_kinds(board):
    """Per family the kind of every line: 'scalar', ('even', axis) for the volume holder's tension lines, ('odd', axis) for the
    sign holder's odd lines."""
    kinds = {}
    for index, family in enumerate(board.families):
        found = []
        for number in range(family.lines):
            if family.held:
                within = number % family.width
                if within == 0:
                    found.append("scalar")
                elif family.wronskian:
                    found.append(("odd", within - 1))
                else:
                    found.append(("even", within - 1))
            else:
                found.append("scalar")
        kinds[index] = found
    return kinds


def held_walls(board, index):
    """The walls the held family's write remainders are kept under, one per line (as Lattice.start keeps them)."""
    return records.divided_walls(board.families[index], board.fixed_walls[index], board.world.node_clock)


def in_kind(array, like):
    return np.asarray(array, dtype=np.asarray(like).dtype)


def transformed(board, element, conjugate=False):
    """The image of the board's state under an element of the 48 (and, with `conjugate`, under the conjugation C: every plane's
    im line negated, the sign holder's lines negated, the counts K and the phase rows negated, every negated line's remainder
    complemented at its wall), a new Lattice (a deep copy) whose arrays are the images; the phase states registered on their orbit."""
    image = copy.deepcopy(board)
    image.output = None
    image.observers = []
    T = Transform(element, board.shape)
    kinds = line_kinds(board)
    gamma = board.world.node_clock
    for index, family in enumerate(board.families):
        state, source = image.states[index], board.states[index]
        wall = wall_of(family.pair[1], gamma, board.unit)
        lines = list(source.lines)
        new_lines = [None] * len(lines)
        for number, line in enumerate(lines):
            kind = kinds[index][number]
            if kind == "scalar":
                now, before, rem = T.scalar(line.now), T.scalar(line.before), T.scalar(line.remainder)
                if conjugate and (family.wronskian or (family.plane and number % 2 == 1)):
                    now, before, rem = -now, -before, in_kind(complement(rem, wall), rem)
                new_lines[number] = records.Record(now, before, rem)
            else:
                tag, new_axis = kind
                old_axis, sign = T.axis_of(new_axis)
                old = lines[number - new_axis + old_axis]
                now, before, rem = T.scalar(old.now), T.scalar(old.before), T.scalar(old.remainder)
                if tag == "odd" and ((sign < 0) != conjugate):
                    now, before, rem = -now, -before, in_kind(complement(rem, wall), rem)
                new_lines[number] = records.Record(now, before, rem)
        state.lines = new_lines
        if source.write_remainders:
            walls = held_walls(board, index)
            new_writes = [None] * len(source.write_remainders)
            for number, rem in enumerate(source.write_remainders):
                kind = kinds[index][number]
                if kind == "scalar":
                    moved = T.scalar(np.asarray(rem, dtype=object))
                    if conjugate and family.wronskian:
                        moved = complement(
                            moved,
                            T.scalar(
                                np.asarray(walls[number], dtype=object)
                                + 0 * np.asarray(rem, dtype=object)
                            ),
                        )
                    new_writes[number] = moved
                else:
                    tag, new_axis = kind
                    old_axis, sign = T.axis_of(new_axis)
                    base = number - new_axis + old_axis
                    moved = T.scalar(np.asarray(source.write_remainders[base], dtype=object))
                    if tag == "odd" and ((sign < 0) != conjugate):
                        moved = complement(
                            moved, T.scalar(np.asarray(walls[base], dtype=object) + 0 * moved)
                        )
                    new_writes[number] = moved
            state.write_remainders = new_writes
        if source.phases:
            new_phases = []
            for row in source.phases:
                if not row:
                    new_phases.append([])
                    continue
                phi = row[-1]
                new_row = [None] * len(row)
                for new_axis in range(AXES):
                    old_axis, sign = T.axis_of(new_axis)
                    cos_line, sin_line, count = (
                        row[2 * old_axis],
                        row[2 * old_axis + 1],
                        row[2 * AXES + old_axis],
                    )
                    mover = (lambda a, i=new_axis: T.owned(a, i)) if sign < 0 else T.scalar
                    new_row[2 * new_axis] = records.Record(
                        mover(cos_line.now), mover(cos_line.before), mover(cos_line.remainder)
                    )
                    new_row[2 * new_axis + 1] = records.Record(
                        mover(sin_line.now), mover(sin_line.before), mover(sin_line.remainder)
                    )
                    k_now = mover(count.now)
                    if (sign < 0) != conjugate:
                        k_now = -k_now
                    new_row[2 * AXES + new_axis] = records.Record(
                        k_now, mover(count.before), mover(count.remainder)
                    )
                phi_now, phi_before, phi_rem = (
                    T.scalar(phi.now),
                    T.scalar(phi.before),
                    T.scalar(phi.remainder),
                )
                if conjugate:  # the phase row stepped at the wall 2 with the write 2 c: the remainder stands under c -> -c
                    phi_now, phi_before = -phi_now, -phi_before
                new_row[-1] = records.Record(phi_now, phi_before, phi_rem)
                new_phases.append(new_row)
            state.phases = new_phases
            if family.rotation:
                phase.seeded(state, phase.unit(gamma), image.amplitude)
    image.proper_count = T.scalar(np.asarray(board.proper_count, dtype=object))
    image.closes = T.scalar(board.closes)
    return image


def differences(a, b, limit=6):
    """The lines where two boards differ: the levels and the remainders apart, then the write remainders and the phase lines."""
    found = []
    for index, family in enumerate(a.families):
        for number, (x, y) in enumerate(zip(a.states[index].lines, b.states[index].lines, strict=True)):
            for part, (u, v) in (
                ("now", (x.now, y.now)),
                ("before", (x.before, y.before)),
                ("remainder", (x.remainder, y.remainder)),
            ):
                differ = np.asarray(np.asarray(u, dtype=object) != np.asarray(v, dtype=object))
                if differ.any():
                    where = np.argwhere(differ)[:limit]
                    sample = [
                        [
                            list(map(int, n)),
                            str(np.asarray(u, dtype=object)[tuple(n)]),
                            str(np.asarray(v, dtype=object)[tuple(n)]),
                        ]
                        for n in where[:2]
                    ]
                    found.append(
                        {
                            "family": family.name,
                            "line": number,
                            "part": part,
                            "nodes": int(differ.sum()),
                            "where": [list(map(int, n)) for n in where],
                            "sample": sample,
                        }
                    )
        for number, (u, v) in enumerate(
            zip(a.states[index].write_remainders, b.states[index].write_remainders, strict=True)
        ):
            differ = np.asarray(np.asarray(u, dtype=object) != np.asarray(v, dtype=object))
            if differ.any():
                found.append(
                    {
                        "family": family.name,
                        "write_remainder": number,
                        "nodes": int(differ.sum()),
                        "where": [list(map(int, n)) for n in np.argwhere(differ)[:limit]],
                    }
                )
        for row, (ra, rb) in enumerate(zip(a.states[index].phases, b.states[index].phases, strict=True)):
            for number, (x, y) in enumerate(zip(ra, rb, strict=True)):
                for part, (u, v) in (
                    ("now", (x.now, y.now)),
                    ("before", (x.before, y.before)),
                    ("remainder", (x.remainder, y.remainder)),
                ):
                    differ = np.asarray(np.asarray(u, dtype=object) != np.asarray(v, dtype=object))
                    if differ.any():
                        found.append(
                            {
                                "family": family.name,
                                "phase_row": row,
                                "line": number,
                                "part": part,
                                "nodes": int(differ.sum()),
                                "where": [list(map(int, n)) for n in np.argwhere(differ)[:limit]],
                            }
                        )
    return found


def summarised(found):
    counts = {"levels": 0, "remainders": 0, "write_remainders": 0, "phases": 0}
    for d in found:
        if "phase_row" in d:
            counts["phases"] += d["nodes"]
        elif "write_remainder" in d:
            counts["write_remainders"] += d["nodes"]
        elif d["part"] == "remainder":
            counts["remainders"] += d["nodes"]
        else:
            counts["levels"] += d["nodes"]
    return counts


# ----------------------------------------------------------------------------------------------------------------------
# the orbits
# ----------------------------------------------------------------------------------------------------------------------
def orbit_key(node, L):
    folded = [x if x <= L // 2 else x - L for x in node]
    return tuple(sorted(abs(x) for x in folded))


def orbits_of(shape):
    L = max(shape)
    found = {}
    for node in np.ndindex(*shape):
        found.setdefault(orbit_key(node, L), []).append(tuple(int(x) for x in node))
    return dict(sorted(found.items(), key=lambda kv: (sum(kv[0]), kv[0])))


# ----------------------------------------------------------------------------------------------------------------------
# the read as a switch
# ----------------------------------------------------------------------------------------------------------------------
READ = {"mode": "ordered"}
CURRENT = {}
DRAWS = []


def link_digits(board, index, at):
    """One family's digits at the frame `at` with ONE-LINK lattices (DERIVATION.md section 7): the Node's own digit on its own
    lattice F_i (digits.lattice_of at the Node: w, D_i, its six reaches and pairs, every one one Link from it); each Port's digit
    the neighbour's remainder on the LINK'S lattice F_ij = gcd(w, R_ji, R^c_ji, R^s_ji), the neighbour's reach and pairs across
    this Link read from the neighbour's end (the opposite Port), a multiple of the neighbour's own F_j, so the Link digit is the
    coarse index, the floor of the fine one over the two lattices' ratio; otherwise as digits.digits_of (every record of quanta,
    every line, the remainder with its lattice, the wall and the place)."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    wall = wall_of(family.pair[1], gamma, unit)
    node = at[0]
    for record in quanta_records(board.families, index):
        content, factors = board.read(index, 1, record)
        rule = ruled(board, index, record, content, factors)
        pairs = flux.pairs_of(
            index,
            board.families,
            board.states,
            1,
            board.wrap,
            gamma,
            content,
            factors,
            record,
            board.amplitude,
        )
        lattice = [lattice_of(rule, [node], pairs)[0]]
        for place in range(1, len(at)):
            opposite = (place - 1) ^ 1  # the Port of the neighbour that looks back at the Node
            j = at[place]
            terms = [picked(rule.reaches[opposite], [j])[0]]
            if pairs is not None:
                terms += [picked(pairs[0][opposite], [j])[0], picked(pairs[1][opposite], [j])[0]]
            lattice.append(gcd(int(rule.wall), *(int(t) for t in terms)))
        for line in board.lines_of(index, record):
            kept = picked(line.remainder, at)
            for place, (remainder, found) in enumerate(zip(kept, lattice, strict=True)):
                yield remainder, found, int(wall), (record, place)


def digits_by_line(board, reads, source):
    """The frame's digits grouped per (family, record, line): [(place, digit, base, at_origin)], the copies dropped as read_of
    drops them (the reader's D2); the flags every digit at the origin and every digit coarse (on the vacuum lattice)."""
    groups, origin, coarse = [], True, True
    for index, at in reads:
        half, earlier, line_counter, group = board.half_wall(index), {}, {}, None
        for remainder, found, wall, place in source(board, index, at):
            values = int(division_forward(wall, found, 0)[0])
            origin = origin and remainder == half
            coarse = coarse and values <= AXES
            standing = earlier.setdefault(place, [])
            copied = any(remainder in (kept, wall - kept) for kept in standing)
            standing.append(remainder)
            record, position = place
            if position == 0:
                n = line_counter.get(record, 0)
                line_counter[record] = n + 1
                group = []
                groups.append(((index, record, n), group))
            if copied:
                continue
            digit = int(division_forward(remainder, found, 0)[0])
            group.append((position, digit, values + 1, remainder == half, digit * int(found)))
    return groups, origin, coarse


def read_switch(board, reads, label):
    """The read of the board by the switch (the module's sentence): ordered (the shipped read_of, bit for bit); sorted (per
    line the Node's own digit first, then the six Ports' (digit, base) pairs sorted ascending, the mixed radix); sum (the plain
    sum, the moduli (1, 1)); link (the Link digits sorted, the mixed radix; link_q the same number, the pick from the quotient by
    the unit in child_aprime); link_sum (the Link digits and the Node's, the digits at the lay's origin left out, the plain sum, no
    moduli); rem_sum_q (the plain SUM of the kept remainders projected on their lattices, each neighbour's (r_j div F_ij) x F_ij and
    the Node's own (r_i div F_i) x F_i, the origin's and the copies left out, no moduli: the whether that sum modulo the unit, the pick
    from the quotient by the unit)."""
    at = reads[0][1][0]
    CURRENT.update(node=list(map(int, at)), label=label)
    mode = READ["mode"]
    if mode == "ordered":
        number, moduli = read_ordered(board, reads, label)
        CURRENT.update(number=int(number), moduli=[int(m) for m in moduli])
        return number, moduli
    source = (
        link_digits if mode in ("link", "link_sum", "link_q", "rem_sum_q", "link_q_all") else digits_of
    )
    groups, origin, coarse = digits_by_line(board, reads, source)
    if origin:
        raise RuntimeError(
            f"the read at {label} finds every digit at the lay's origin w div 2: refused ({mode} read)"
        )
    if coarse:
        raise RuntimeError(
            f"the read at {label} finds every digit on the lattice of the exact vacuum paces: refused ({mode} read)"
        )
    digits, bases, projected = [], [], []
    if (
        mode == "link_q_all"
    ):  # every kept digit of the Node and its six Links, of every line and record, one multiset sorted
        pairs = sorted((g[1], g[2]) for _key, group in groups for g in group)
        digits, bases = [d for d, _b in pairs], [b for _d, b in pairs]
        number = read_number(digits, bases)
        summed = gcd(*(base - 1 for base in bases[1:])) if len(bases) > 1 else 1
        moduli = (summed, bases[-1])
        CURRENT.update(number=int(number), moduli=[int(m) for m in moduli], digits=len(digits))
        return number, moduli
    for _key, group in groups:
        own = [g for g in group if g[0] == 0]
        rest = sorted((g[1], g[2], g[3], g[4]) for g in group if g[0] != 0)
        if mode in ("link_sum", "rem_sum_q"):
            own = [g for g in own if not g[3]]
            rest = [g for g in rest if not g[2]]
        for g in own:
            digits.append(g[1])
            bases.append(g[2])
            projected.append(g[4])
        for g in rest:
            digits.append(g[0])
            bases.append(g[1])
            projected.append(g[3])
    if mode in ("sum", "link_sum", "rem_sum_q"):
        if not digits:
            raise RuntimeError(
                f"the read at {label} finds no digit off the lay's origin: nothing to read ({mode} read)"
            )
        number = sum(projected) if mode == "rem_sum_q" else sum(digits)
        moduli = (1, 1) if mode == "sum" else None
    else:
        number = read_number(digits, bases)
        summed = gcd(*(base - 1 for base in bases[1:])) if len(bases) > 1 else 1
        moduli = (summed, bases[-1])
    CURRENT.update(
        number=int(number),
        moduli=None if moduli is None else [int(m) for m in moduli],
        digits=len(digits),
    )
    return number, moduli


def drawn_logged(number, weights, label, moduli=None):
    """drawn_from with its log: the whether (the two weights rest and unit less rest) or a pick."""
    total = sum(int(w) for w in weights)
    line = {
        "event": "draw",
        "interval": CURRENT.get("interval"),
        "node": CURRENT.get("node"),
        "read": READ["mode"],
        "board": CURRENT.get("board", "main"),
        "weights": [str(w) for w in weights],
        "total": str(total),
        "number_bits": int(number).bit_length(),
        "residue": str(int(number) % total) if total else None,
        "moduli": [str(m) for m in moduli] if moduli else None,
        "digits": CURRENT.get("digits"),
        "kind": "whether" if len(weights) == 2 and total != 2 else "pick",
    }
    try:
        found = drawn_from(number, weights, label, moduli)
    except RuntimeError as refusal:
        line.update(refused=str(refusal)[:200])
        DRAWS.append(line)
        raise
    line.update(drawn=int(found[0]), met=found[0] == 0)
    DRAWS.append(line)
    return found


# ----------------------------------------------------------------------------------------------------------------------
# the selector as a switch: A-prime, the primes' lifts that fit, drawn at equal weights by the read
# ----------------------------------------------------------------------------------------------------------------------
SELECT = {"mode": "main", "lifts": None}
PICKS = []


def lift_families(board):
    """The families whose point is a lift of one of den's primes: the label's exponent vector with the one entry 2 e at the
    prime's place and 0 elsewhere (loader/circle.circle_points: the prime's Gaussian factor to the power 2 e, the others real)."""
    den = board.families[board.world.seed].pair[1]
    primes, _scale = angled(den)
    found = []
    for index, family in enumerate(board.families):
        if not family.plane or not family.name.startswith("point "):
            continue
        vector = [int(w) for w in family.name.split()[1:]]
        hot = [k for k, step in enumerate(vector) if step != 0]
        if len(hot) == 1 and vector[hot[0]] == 2 * primes[hot[0]][1]:
            found.append(index)
    return found


def child_aprime(board, index, share, whole, at):
    """A-prime: among the lifts the tables ((k, -1), (k, 1)) whose two walls fit, 2 x count_wall x max(whole, 2) <= 2 x share;
    one is certain; several are drawn at equal weights by the switch's read on the Node's frame; a refusal births nothing."""
    over, energy, action = max(whole, 2), 2 * share, board.world.quantum_action
    candidates = [
        t
        for t in conversion.birth_of(board.families, index)
        if t[0][0] in SELECT["lifts"]
        and 2 * count_wall(board.families[t[0][0]], action) * over <= energy
    ]
    line = {
        "event": "pick",
        "interval": board.interval,
        "node": list(at),
        "board": CURRENT.get("board", "main"),
        "share": str(share),
        "whole": whole,
        "q": share / board.credit.units[index],
        "candidates": [board.families[t[0][0]].name for t in candidates],
    }
    if not candidates:
        line.update(how="none")
        PICKS.append(line)
        return None
    if len(candidates) == 1:
        line.update(how="certain", picked=board.families[candidates[0][0][0]].name)
        PICKS.append(line)
        return candidates[0]
    label = f"the Node {list(at)}'s read for the pick among the lifts at the interval {board.interval}"
    region = frame_of(at, board.shape, board.world.periodic)
    reads = [(family, region) for family in board.order]
    if at_origin(board, reads):
        line.update(how="no_draw_origin")
        PICKS.append(line)
        return None
    try:
        number, moduli = read_switch(board, reads, label)
        if (
            READ["mode"] in ("link_q", "rem_sum_q", "link_q_all")
        ):  # the one division act at every close: the number divided by the unit, the quotient the pick's
            quotient = int(division_forward(int(number), board.credit.units[index], 0)[0])
            k, _left = drawn_from(quotient, [1] * len(candidates), label, None)
            line.update(
                how_number="quotient",
                quotient_bits=quotient.bit_length(),
                quotient_residue=quotient % len(candidates),
            )
        else:
            k, _left = drawn_from(number, [1] * len(candidates), label, moduli)
    except RuntimeError as refusal:
        line.update(how="refused", refused=str(refusal)[:200])
        PICKS.append(line)
        return None
    line.update(
        how="read",
        drawn=k,
        picked=board.families[candidates[k][0][0]].name,
        number_bits=int(number).bit_length(),
        residue=int(number) % len(candidates),
    )
    PICKS.append(line)
    return candidates[k]


def child_switch(board, index, share, whole, at):
    if SELECT["mode"] == "aprime":
        return child_aprime(board, index, share, whole, at)
    return child_of(board, index, share, whole)


# ----------------------------------------------------------------------------------------------------------------------
# the board's own close, main's line by line, with the read, the selector and the hole as switches
# ----------------------------------------------------------------------------------------------------------------------
HOLE = {"mode": "zero"}


def hole_changes(board, index, number, at_nodes, amounts=None):
    """Per born Node the change the hole writes on the seed's line `number`, read on the state the step left before ANY write
    (every face before any write): zero: the line to (0, 0) at the Node (main's); mean: the six Ports' mean of now and of before by
    Rule3's division act at the wall, (w div 6) SUM_j m_j divided at w with the line's remainder as the carry, the remainder kept
    (the ruling of 13:33; it keeps the drift and fails); before_mean: (b_u, b_u), b_u = SUM_j before_j div PORTS by the division
    act, the remainder kept whole; own_before: (b_i, b_i), the Node's own level before twice, the remainder kept whole."""
    line = board.states[index].lines[number]
    found = {}
    mode = HOLE["mode"]
    if mode == "exact_take":
        return exact_take(board, index, number, at_nodes, amounts)
    if mode == "zero":
        for at in at_nodes:
            found[at] = (-int(line.now[at]), -int(line.before[at]), None)
        return found
    if mode == "own_before":
        for at in at_nodes:
            b = int(line.before[at])
            found[at] = (b - int(line.now[at]), 0, None)
        return found
    now_sum = sum(np.asarray(a, dtype=object) for a in ports(line.now, board.wrap))
    before_sum = sum(np.asarray(a, dtype=object) for a in ports(line.before, board.wrap))
    if mode == "before_mean":
        for at in at_nodes:
            b_u = int(division_forward(int(before_sum[at]), PORTS, 0)[0])
            found[at] = (b_u - int(line.now[at]), b_u - int(line.before[at]), None)
        return found
    wall = wall_of(board.families[index].pair[1], board.world.node_clock, board.unit)
    sixth = int(division_forward(wall, PORTS, 0)[0])
    for at in at_nodes:
        r = int(line.remainder[at])
        q_now, r1 = division_forward(sixth * int(now_sum[at]), wall, r)
        q_before, r2 = division_forward(sixth * int(before_sum[at]), wall, int(r1))
        found[at] = (int(q_now) - int(line.now[at]), int(q_before) - int(line.before[at]), int(r2))
    return found


TAKES = []


def frame_share(board, index, record, lines, mask):
    """The light's share summed over the Nodes of `mask` for the trial `lines` of the record, by the engine's own share
    (share.family_share at the record's read: the content and the Links' factors of the state the write acts on)."""
    family, gamma = board.families[index], board.world.node_clock
    content, factors = board.read(index, 1, record)
    found = share.family_share(family, lines, board.wrap, gamma, content, factors, board.unit, mask)
    return int(np.asarray(found, dtype=object)[mask].sum())


def exact_take(board, index, number, at_nodes, amounts):
    """The exact take (DERIVATION.md section 10): at every born Node the Node's before is kept and its now is moved from n toward b
    one level at a time until the frame's seven shares (the Node's and its six neighbours', read on the state the write acts on,
    every face before any write) have dropped by the booked amount, the children's walls summed; the last step's overshoot is named
    as the take's remainder; where the full stop's take is below the amount the hole refuses by name (None: nothing born)."""
    line = board.states[index].lines[number]
    found = {}
    for at in at_nodes:
        amount = amounts[at]
        n, b = int(line.now[at]), int(line.before[at])
        frame = frame_of(at, board.shape, board.world.periodic)
        mask = board.mask(tuple(frame))
        start = frame_share(board, index, 0, [line], mask)
        step = -1 if n > b else 1
        taken, chosen, previous = 0, None, 0
        for k in range(1, abs(n - b) + 1):
            trial_level = n + k * step
            trial_now = np.asarray(line.now).copy()
            trial_now[at] = trial_level
            trial = records.Record(trial_now, line.before, line.remainder)
            taken = start - frame_share(board, index, 0, [trial], mask)
            if taken >= amount:
                chosen = trial_level
                break
            previous = taken
        record = {
            "node": list(at),
            "now": n,
            "before": b,
            "amount": str(amount),
            "full_stop_take": None,
            "q_frame_start": start,
        }
        if chosen is None:
            record.update(
                refused=True,
                taken_at_full_stop=str(taken),
                reason="the full stop's take is below the booked amount",
            )
            TAKES.append(record)
            found[at] = None
            continue
        record.update(
            level_after=chosen,
            moved=chosen - n,
            taken=str(taken),
            overshoot=str(taken - amount),
            overshoot_over_unit=(taken - amount) / board.credit.units[index],
            step_share=str(taken - previous),
        )
        TAKES.append(record)
        found[at] = (chosen - n, 0, None)
    return found


def closed_switch(board, begun):
    """meeting_board.closed of origin/main line by line (the read on the interval's start, every face read before any write,
    the hole, the pair laid by act.click, the credit and birth lines, the count read back), the child's selection by the
    selector switch, the read by the read switch, the hole by the hole switch."""
    index = board.world.seed
    if index is None:
        return
    books = board.credit
    unit, family = books.units[index], board.families[index]
    span = records.record_slice(family, 0)
    stepped = [(state.lines, state.phases) for state in board.states]
    for state, lines, phases in zip(board.states, begun[0], begun[2], strict=True):
        state.lines, state.phases = lines, phases
    try:
        shares, frozen = board.share_of(index)
        born = []
        for at, whole, rest in meetings(board, index, shares, frozen):
            table = child_switch(board, index, int(shares[at]), whole, at)
            if table is None:
                continue
            meet = whole >= 2
            if not meet and rest > 0:
                label = f"the Node {list(at)}'s read of itself and its Links at the interval {board.interval}"
                region = frame_of(at, board.shape, board.world.periodic)
                reads = [(fam, region) for fam in board.order]
                if not at_origin(board, reads):
                    try:
                        number, moduli = read_switch(board, reads, label)
                        meet = drawn_logged(number, [rest, unit - rest], label, moduli)[0] == 0
                    except RuntimeError as refusal:
                        if READ["mode"] == "ordered":
                            raise
                        DRAWS.append(
                            {
                                "event": "draw",
                                "interval": CURRENT.get("interval"),
                                "node": list(at),
                                "read": READ["mode"],
                                "board": CURRENT.get("board", "main"),
                                "kind": "whether",
                                "refused": str(refusal)[:200],
                                "weights": [str(rest), str(unit - rest)],
                                "total": str(unit),
                            }
                        )
                        meet = False
            if meet:
                born.append((at, table))
    finally:
        for state, (lines, phases) in zip(board.states, stepped, strict=True):
            state.lines, state.phases = lines, phases
    action = board.world.quantum_action
    amounts = {
        at: sum(count_wall(board.families[out], action) for out, _sense in table) for at, table in born
    }
    total_before = int(np.asarray(board.share_of(index)[0], dtype=object).sum()) if born else None
    changes = {
        number: hole_changes(board, index, number, [at for at, _t in born], amounts)
        for number in range(span.start, span.stop)
    }
    refused = [
        at
        for at, _t in born
        if any(changes[number][at] is None for number in range(span.start, span.stop))
    ]
    born = [(at, table) for at, table in born if at not in refused]
    for at, _table in born:
        board.closes[at] += 1
    readings = {at: readings_at(board, begun, index, 0, at) for at, _table in born}
    items = []
    for at, table in born:
        here = board.mask((at,))
        for number in range(span.start, span.stop):
            d_now, d_before, remainder = changes[number][at]
            change = (np.where(here, d_now, 0), np.where(here, d_before, 0))
            origin = (
                None
                if remainder is None
                else np.where(here, remainder, board.states[index].lines[number].remainder)
            )
            laid(board, index, number, change, None, origin, here)
        items.extend(born_items(board.families, table, (at,)))
    click(board, items)
    if born or refused:
        total_after = int(np.asarray(board.share_of(index)[0], dtype=object).sum())
        booked = sum(amounts[at] for at, _t in born)
        TAKES.append(
            {
                "event": "close",
                "interval": board.interval,
                "board": CURRENT.get("board", "main"),
                "hole": HOLE["mode"],
                "born": [list(at) for at, _t in born],
                "refused": [list(at) for at in refused],
                "light_before": str(total_before),
                "light_after": str(total_after),
                "booked": str(booked),
                "taken": str(total_before - total_after),
                "made": str(booked - (total_before - total_after)),
                "taken_over_unit": (total_before - total_after) / unit,
                "booked_over_unit": booked / unit,
                "made_over_unit": (booked - (total_before - total_after)) / unit,
            }
        )
    for at, table in born:
        if board.output is not None:
            names = [board.families[out].name for out, _sense in table]
            seed = board.families[index].name
            place = int(np.ravel_multi_index(at, board.shape))
            found, clock = readings[at]
            board.output(
                credit_line(
                    board.interval,
                    seed,
                    place,
                    [board.interval, board.interval],
                    clock.proper,
                    clock.windows,
                    names[0],
                    None,
                    1,
                    None,
                    None,
                    seed,
                    names[0],
                    momentum=clock.momentum,
                    fan=clock.fan,
                    recoil=clock.recoil,
                    readings=found,
                )
            )
            children = born_items(board.families, table, (at,))
            board.output(
                birth_line(
                    board.interval,
                    seed,
                    names,
                    [sense for _out, sense in table],
                    (at,),
                    [child.record for child in children],
                    [list(board.families[child.family].pair) for child in children],
                )
            )
    counted = credit.count_of(board, index)
    if counted is not None:
        books.counts[index] = counted


# ----------------------------------------------------------------------------------------------------------------------
# the world and the seeds
# ----------------------------------------------------------------------------------------------------------------------
def build_world(folder, den, shape, intervals, gamma, action, name):
    folder.mkdir(parents=True, exist_ok=True)
    universe = folder / f"u_{den}.json"
    universe.write_text(
        json.dumps({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}}),
        encoding="utf-8",
    )
    world = folder / f"{name}.json"
    world.write_text(
        json.dumps({"universe": str(universe), "shape": list(shape), "intervals": intervals}),
        encoding="utf-8",
    )
    return world


def faces_seed(board, level):
    """The faces seed: the uniform sea restored at the origin (the drift v laid back, the former seed that births nothing) and the
    six face Nodes raised to `level` (now; before 0), a seed symmetric about the origin whose first one-quantum meetings fall on
    the 6-orbit, by the one lay act; the count read back."""
    index = board.world.seed
    family = board.families[index]
    drift = drift_of(board.world.quantum_action)
    first = records.record_slice(family, 0).start
    origin = board.mask(((0, 0, 0),))
    faces = board.mask(
        tuple(
            tuple((side if i == axis else 0) % board.shape[0] for i in range(3))
            for axis in range(3)
            for side in (1, -1)
        )
    )
    for line in emitted_lines(family):
        laid(
            board,
            index,
            first + line,
            (np.where(origin, drift, 0), np.where(origin, 0, 0)),
            None,
            None,
            origin,
        )
        laid(
            board,
            index,
            first + line,
            (np.where(faces, level - drift, 0), np.where(faces, 0, 0)),
            None,
            None,
            faces,
        )
    counted = credit.count_of(board, index)
    if counted is not None:
        board.credit.counts[index] = counted
    return level


def plus_one(board):
    """The plus-one seed: the sea's quantum laid back at the origin and one more, now = largest_below(2 T) (268 at T 36000),
    the share of two quanta less the rounding, before 0 (the previous hands' form), by the one lay act; the count read back."""
    index = board.world.seed
    family = board.families[index]
    level = largest_below(2 * board.world.quantum_action)
    at = board.mask(((0, 0, 0),))
    first = records.record_slice(family, 0).start
    for line in emitted_lines(family):
        laid(board, index, first + line, (np.where(at, level, 0), np.where(at, 0, 0)), None, None, at)
    counted = credit.count_of(board, index)
    if counted is not None:
        board.credit.counts[index] = counted
    return level


# ----------------------------------------------------------------------------------------------------------------------
# the two-tiles test (tests/test_two_tiles_with_skewed_clocks_run_the_board.py's form)
# ----------------------------------------------------------------------------------------------------------------------
def layers_of(interior, side):
    return [(interior[0] - 1) % side, *interior, (interior[-1] + 1) % side]


def taken(array, layers):
    return np.asarray(array)[layers]


def imposed(tile, whole, layers):
    for state, (lines, remainders, phases) in zip(tile.states, whole, strict=True):
        state.lines = [records.Record(*(taken(a, layers) for a in line)) for line in lines]
        state.write_remainders = [taken(r, layers) for r in remainders]
        state.phases = [
            [records.Record(*(taken(a, layers) for a in line)) for line in row] for row in phases
        ]


def arrays_of(board):
    return [
        (
            [(line.now, line.before, line.remainder) for line in state.lines],
            list(state.write_remainders),
            [[(line.now, line.before, line.remainder) for line in row] for row in state.phases],
        )
        for state in board.states
    ]


def merged(tiles, interiors, shape):
    found = []
    for index in range(len(tiles[0].states)):
        parts = [arrays_of(tile)[index] for tile in tiles]

        def put(part, *path, parts=parts):
            pieces = []
            for tile_part, interior in zip(parts, interiors, strict=True):
                a = tile_part[part]
                for step in path:
                    a = a[step]
                pieces.append((interior, np.asarray(a)[1 : 1 + len(interior)]))
            whole = np.zeros(shape, dtype=pieces[0][1].dtype)
            for interior, piece in pieces:
                whole[interior] = piece
            return whole

        lines = [tuple(put(0, k, j) for j in range(3)) for k in range(len(parts[0][0]))]
        remainders = [put(1, k) for k in range(len(parts[0][1]))]
        phases = [
            [tuple(put(2, r, k, j) for j in range(3)) for k in range(len(parts[0][2][r]))]
            for r in range(len(parts[0][2]))
        ]
        found.append((lines, remainders, phases))
    return found


def tile_differences(whole, board, limit=6):
    """Every array of the tiles' merged state that differs from the board's, named by family, line and part, with the Nodes."""
    found = []
    parts = ("now", "before", "remainder")
    for family, ((lines, remainders, phases), state) in zip(
        board.families, zip(whole, board.states, strict=True), strict=True
    ):
        for k, (line, kept) in enumerate(zip(lines, state.lines, strict=True)):
            for part, (u, v) in enumerate(
                zip(line, (kept.now, kept.before, kept.remainder), strict=True)
            ):
                differ = np.asarray(np.asarray(u, dtype=object) != np.asarray(v, dtype=object))
                if differ.any():
                    found.append(
                        {
                            "family": family.name,
                            "line": k,
                            "part": parts[part],
                            "nodes": int(differ.sum()),
                            "where": [list(map(int, n)) for n in np.argwhere(differ)[:limit]],
                        }
                    )
        for k, (a, b) in enumerate(zip(remainders, state.write_remainders, strict=True)):
            differ = np.asarray(np.asarray(a, dtype=object) != np.asarray(b, dtype=object))
            if differ.any():
                found.append(
                    {
                        "family": family.name,
                        "write_remainder": k,
                        "nodes": int(differ.sum()),
                        "where": [list(map(int, n)) for n in np.argwhere(differ)[:limit]],
                    }
                )
        for r, (row, kept_row) in enumerate(zip(phases, state.phases, strict=True)):
            for k, (line, kept) in enumerate(zip(row, kept_row, strict=True)):
                for part, (u, v) in enumerate(
                    zip(line, (kept.now, kept.before, kept.remainder), strict=True)
                ):
                    differ = np.asarray(np.asarray(u, dtype=object) != np.asarray(v, dtype=object))
                    if differ.any():
                        found.append(
                            {
                                "family": family.name,
                                "phase_row": r,
                                "line": k,
                                "part": parts[part],
                                "nodes": int(differ.sum()),
                                "where": [list(map(int, n)) for n in np.argwhere(differ)[:limit]],
                            }
                        )
    return found


class Tiles:
    """The two x-tiles with one-Link halos beside the board: each a Lattice over its layers, imposed from the board at the start;
    `tick` steps them in alternating order from their own state and their halos at the tick before, exchanges the halos and
    compares the merged interiors with the board."""

    def __init__(self, board, folder, den, gamma, action, intervals):
        side = board.shape[0]
        half = side // 2 + 1
        self.interiors = [list(range(0, half)), list(range(half, side))]
        self.layers = [layers_of(interior, side) for interior in self.interiors]
        self.tiles = []
        for rows in self.layers:
            path = build_world(
                folder,
                den,
                (len(rows), board.shape[1], board.shape[2]),
                intervals,
                gamma,
                action,
                f"tile_{den}_{side}x{board.shape[1]}x{board.shape[2]}_{len(rows)}",
            )
            self.tiles.append(Lattice(load_world(path), output=None))
        whole = arrays_of(board)
        for tile, rows in zip(self.tiles, self.layers, strict=True):
            imposed(tile, whole, rows)
        self.parted = None

    def tick(self, board, interval):
        first, second = self.tiles if interval % 2 else self.tiles[::-1]
        CURRENT["board"] = "tile_a"
        first.step()
        CURRENT["board"] = "tile_b"
        second.step()
        whole = merged(self.tiles, self.interiors, board.shape)
        for tile, rows in zip(self.tiles, self.layers, strict=True):
            imposed(tile, whole, rows)
        found = tile_differences(whole, board)
        if found and self.parted is None:
            self.parted = interval
        return found


# ----------------------------------------------------------------------------------------------------------------------
# the readings per interval
# ----------------------------------------------------------------------------------------------------------------------
def invariance(board, all48):
    """Under which elements of the 48 the state is its own image: the levels, the remainders, the write remainders and the
    phases apart; the counts of elements and the first failing names."""
    found = {"levels": [], "remainders": [], "write_remainders": [], "phases": []}
    names = [name_of(e) for e in all48]
    for element in all48:
        image = transformed(board, element)
        diff = summarised(differences(board, image, limit=1))
        for key in found:
            if diff[key] == 0:
                found[key].append(name_of(element))
    return {k: len(v) for k, v in found.items()}, {
        k: [n for n in names if n not in v][:6] for k, v in found.items()
    }


def orbit_table(board, orbits, with_digits):
    """Per orbit: the seed's levels (now, before) distinct values, the share q distinct values, the digits' sum distinct values
    (the digits as the next close would read them by the switch's lattices, on the state the step left)."""
    index = board.world.seed
    unit = board.credit.units[index]
    first = records.record_slice(board.families[index], 0).start
    line = board.states[index].lines[first]
    shares, _frozen = board.share_of(index)
    source = (
        link_digits
        if READ["mode"] in ("link", "link_sum", "link_q", "rem_sum_q", "link_q_all")
        else digits_of
    )
    rows = []
    for key, nodes in orbits.items():
        nows = sorted({int(line.now[n]) for n in nodes})
        befores = sorted({int(line.before[n]) for n in nodes})
        qs = sorted({round(int(shares[n]) / unit, 6) for n in nodes})
        row = {
            "orbit": list(key),
            "size": len(nodes),
            "now": nows[:8],
            "before": befores[:8],
            "q": qs[:8],
            "uniform": len(nows) == 1 and len(befores) == 1 and len(qs) == 1,
        }
        if with_digits:
            sums = set()
            for n in nodes:
                region = frame_of(n, board.shape, board.world.periodic)
                groups, _origin, _coarse = digits_by_line(
                    board, [(fam, region) for fam in board.order], source
                )
                sums.add(int(sum(g[1] for _k, gr in groups for g in gr)))
            row["digit_sum"] = sorted(sums)[:8]
            row["digit_sum_uniform"] = len(sums) == 1
        rows.append(row)
    return rows


def wronskians_at(board, nodes):
    """W per plane family and record at the Nodes, read right after the lay; the family's total at the Node beside."""
    found = []
    for index, family in enumerate(board.families):
        if not family.plane:
            continue
        per_record = [
            np.asarray(records.wronskian(board.lines_of(index, record), True), dtype=object)
            for record in range(family.records)
        ]
        for n in nodes:
            values = [int(w[tuple(n)]) for w in per_record]
            if any(values):
                found.append(
                    {
                        "family": family.name,
                        "node": list(n),
                        "W_per_record": values,
                        "W_total": sum(values),
                    }
                )
    return found


def commutation(board, element, conjugate=False):
    """The commutation test at the board's interval: g S stepped once against g (S stepped once); the differences."""
    image = transformed(board, element, conjugate)
    original = copy.deepcopy(board)
    original.output = None
    original.observers = []
    saved = len(DRAWS), len(PICKS), len(TAKES)
    CURRENT["board"] = "commute"
    original.step()
    image.step()
    del DRAWS[saved[0] :]
    del PICKS[saved[1] :]
    del TAKES[saved[2] :]
    expected = transformed(original, element, conjugate)
    found = differences(expected, image)
    return found, summarised(found), int((image.closes != expected.closes).sum())


# ----------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--den", type=int, required=True)
    ap.add_argument("--cube", type=int, default=3)
    ap.add_argument("--intervals", type=int, default=60)
    ap.add_argument("--seed", choices=("hole", "plus1", "faces"), default="hole")
    ap.add_argument("--faces-level", type=int, default=219)
    ap.add_argument(
        "--read",
        choices=("ordered", "sorted", "sum", "link", "link_sum", "link_q", "rem_sum_q", "link_q_all"),
        default="ordered",
    )
    ap.add_argument("--select", choices=("main", "aprime"), default="main")
    ap.add_argument(
        "--hole", choices=("zero", "mean", "before_mean", "own_before", "exact_take"), default="zero"
    )
    ap.add_argument("--shape", type=str, default=None, help="X,Y,Z in place of --cube")
    ap.add_argument("--prefix", type=Path, required=True)
    ap.add_argument(
        "--commute",
        type=int,
        default=0,
        help="the commutation test from the states of the intervals below this",
    )
    ap.add_argument("--commute-every", type=int, default=1)
    ap.add_argument(
        "--mirror",
        type=str,
        default=None,
        help="an element's name, e.g. 'xyz,-++': the run from the image of the start",
    )
    ap.add_argument("--tiles", action="store_true", help="the two-tiles test beside the board")
    ap.add_argument("--no-all48", action="store_true")
    ap.add_argument("--digits-table", action="store_true")
    ap.add_argument("--seconds", type=float, default=3000.0)
    ap.add_argument("--gamma", type=int, default=1000)
    ap.add_argument("--action", type=int, default=36000)
    args = ap.parse_args()
    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    READ["mode"], SELECT["mode"], HOLE["mode"] = args.read, args.select, args.hole
    meeting_board.closed = (
        closed_switch  # the switch: main's close line by line with the read, the selector and the hole
    )

    folder = args.prefix.parent / "worlds"
    shape = tuple(int(x) for x in args.shape.split(",")) if args.shape else (args.cube,) * 3
    world_path = build_world(
        folder,
        args.den,
        shape,
        args.intervals,
        args.gamma,
        args.action,
        f"bare_{args.den}_{'x'.join(str(x) for x in shape)}",
    )
    world = load_world(world_path)
    lines = []
    out_lines = open(str(args.prefix) + ".births.jsonl", "w")
    sym_out = open(str(args.prefix) + ".sym.jsonl", "w")
    draws_out = open(str(args.prefix) + ".draws.jsonl", "w")
    commute_out = open(str(args.prefix) + ".commute.jsonl", "w") if args.commute else None
    mirror_out = open(str(args.prefix) + ".mirror.jsonl", "w") if args.mirror else None
    tiles_out = open(str(args.prefix) + ".tiles.jsonl", "w") if args.tiles else None

    def keep(line):
        if line.get("event") in ("birth", "credit", "lay", "click"):
            lines.append(line)

    t0 = time.time()
    board = Lattice(world, output=keep)
    SELECT["lifts"] = lift_families(board) if args.select == "aprime" else []
    families = [
        {
            "index": i,
            "name": f.name,
            "pair": [str(f.pair[0]), str(f.pair[1])],
            "plane": f.plane,
            "held": f.held,
            "wronskian": f.wronskian,
            "rotation": f.rotation,
            "records": f.records,
            "lines": f.lines,
            "rung": (2 * largest_below(f.pair[1] ** 2 - f.pair[0] ** 2) / f.pair[1])
            if f.plane
            else None,
            "lift": (i in SELECT["lifts"]) if f.plane else None,
        }
        for i, f in enumerate(board.families)
    ]
    unit = board.credit.units[world.seed]
    head = {
        "event": "head",
        "den": args.den,
        "cube": args.cube,
        "intervals": args.intervals,
        "seed": args.seed,
        "read": args.read,
        "select": args.select,
        "hole": args.hole,
        "tiles": args.tiles,
        "gamma": args.gamma,
        "action": args.action,
        "drift": drift_of(args.action),
        "W_c": str(unit),
        "wall_seed": str(wall_of(args.den, args.gamma, board.unit)),
        "kind": str(board.kind),
        "width": world.width.bit_length(),
        "families": families,
        "amplitude_A": largest_below(args.action // 2),
        "load_seconds": round(time.time() - t0, 2),
    }
    if args.seed == "plus1":
        head["plus_one_level"] = plus_one(board)
    if args.seed == "faces":
        head["faces_level"] = faces_seed(board, args.faces_level)
    print(json.dumps({k: v for k, v in head.items() if k != "families"}))
    print(
        json.dumps(
            {"families": [(f["index"], f["name"], f["pair"], f["rung"], f["lift"]) for f in families]}
        )
    )
    sym_out.write(json.dumps(head) + "\n")
    all48 = elements()
    orbits = orbits_of(board.shape)

    mirror = mirror_element = None
    if args.mirror:
        mirror_element = next(e for e in all48 if name_of(e) == args.mirror)
        mirror = transformed(board, mirror_element)
        found = differences(board, mirror)
        mirror_out.write(
            json.dumps(
                {
                    "event": "mirror_start",
                    "element": args.mirror,
                    "start_differs": summarised(found),
                    "first": found[:8],
                }
            )
            + "\n"
        )
    tiles = (
        Tiles(board, folder, args.den, args.gamma, args.action, args.intervals) if args.tiles else None
    )

    inv_counts, inv_fail = invariance(board, all48) if not args.no_all48 else (None, None)
    sym_out.write(
        json.dumps(
            {
                "event": "interval",
                "interval": 0,
                "invariant": inv_counts,
                "failing": inv_fail,
                "orbits": orbit_table(board, orbits, args.digits_table),
                "births": 0,
            }
        )
        + "\n"
    )
    first_split = first_level_split = None
    reached = 0
    for _ in range(args.intervals):
        if time.time() - t0 > args.seconds:
            break
        CURRENT["interval"] = board.interval + 1
        if args.commute and board.interval < args.commute and board.interval % args.commute_every == 0:
            for element in GENERATORS:
                found, counts, closes = commutation(board, element)
                commute_out.write(
                    json.dumps(
                        {
                            "event": "commute",
                            "interval_from": board.interval,
                            "element": name_of(element),
                            "differs": counts,
                            "closes_differ": closes,
                            "first": found[:6],
                        }
                    )
                    + "\n"
                )
            found, counts, closes = commutation(board, ((0, 1, 2), (1, 1, 1)), conjugate=True)
            commute_out.write(
                json.dumps(
                    {
                        "event": "commute",
                        "interval_from": board.interval,
                        "element": "C",
                        "differs": counts,
                        "closes_differ": closes,
                        "first": found[:6],
                    }
                )
                + "\n"
            )
            commute_out.flush()
        CURRENT["board"] = "main"
        board.step()
        reached = board.interval
        births = [row for row in lines if row["event"] == "birth" and row["interval"] == board.interval]
        born_nodes = [tuple(n) for b in births for n in b["nodes"]]
        for b in births:
            out_lines.write(json.dumps(b) + "\n")
        if born_nodes:
            out_lines.write(
                json.dumps(
                    {
                        "event": "W_after_lay",
                        "interval": board.interval,
                        "W": wronskians_at(board, born_nodes),
                    }
                )
                + "\n"
            )
        for t in TAKES:
            if t.get("event") == "close" or "node" in t:
                t.setdefault("interval", board.interval)
                out_lines.write(json.dumps(t) + "\n")
        TAKES.clear()
        if tiles is not None:
            found = tiles.tick(board, board.interval)
            tiles_out.write(
                json.dumps(
                    {
                        "event": "tiles",
                        "interval": board.interval,
                        "differs": len(found),
                        "nodes": sum(d["nodes"] for d in found),
                        "first": found[:6],
                    }
                )
                + "\n"
            )
            tiles_out.flush()
        if mirror is not None:
            CURRENT["board"] = "mirror"
            mirror.step()
            found = differences(transformed(board, mirror_element), mirror)
            mirror_out.write(
                json.dumps(
                    {
                        "event": "mirror",
                        "interval": board.interval,
                        "differs": summarised(found),
                        "first": found[:6],
                    }
                )
                + "\n"
            )
            mirror_out.flush()
        for d in DRAWS:
            draws_out.write(json.dumps(d) + "\n")
        DRAWS.clear()
        for p in PICKS:
            draws_out.write(json.dumps(p) + "\n")
        PICKS.clear()
        inv_counts, inv_fail = invariance(board, all48) if not args.no_all48 else (None, None)
        table = orbit_table(board, orbits, args.digits_table)
        split = [r["orbit"] for r in table if not r["uniform"]]
        if inv_counts is not None and first_level_split is None and inv_counts["levels"] < 48:
            first_level_split = board.interval
        if split and first_split is None:
            first_split = (board.interval, split)
        row = {
            "event": "interval",
            "interval": board.interval,
            "seconds": round(time.time() - t0, 2),
            "invariant": inv_counts,
            "failing": inv_fail,
            "orbits": table,
            "births": len(births),
            "born": [list(n) for n in born_nodes],
            "children": sorted({c for b in births for c in b["children"]}),
            "light_count": board.credit.counts.get(world.seed),
            "tiles_parted": None if tiles is None else tiles.parted,
        }
        sym_out.write(json.dumps(row) + "\n")
        for f in (sym_out, out_lines, draws_out):
            f.flush()
        if board.interval % 10 == 0 or births:
            print(
                json.dumps(
                    {
                        "interval": board.interval,
                        "s": round(time.time() - t0, 1),
                        "invariant": inv_counts,
                        "births": len(births),
                        "born": [list(n) for n in born_nodes],
                        "children": row["children"],
                        "split": split,
                        "light": row["light_count"],
                        "tiles_parted": row["tiles_parted"],
                    }
                )
            )
            sys.stdout.flush()
    summary = {
        "event": "end",
        "reached": reached,
        "seconds": round(time.time() - t0, 1),
        "first_split_orbit": first_split,
        "first_level_asymmetry_interval": first_level_split,
        "tiles_parted": None if tiles is None else tiles.parted,
        "births_total": sum(1 for row in lines if row["event"] == "birth"),
        "births_by_child": dict(
            sorted(
                Counter(c for row in lines if row["event"] == "birth" for c in row["children"]).items()
            )
        ),
        "births_by_interval": dict(
            sorted(Counter(row["interval"] for row in lines if row["event"] == "birth").items())
        ),
        "light_count_end": board.credit.counts.get(world.seed),
    }
    print(json.dumps(summary))
    sym_out.write(json.dumps(summary) + "\n")
    for f in (out_lines, sym_out, draws_out, commute_out, mirror_out, tiles_out):
        if f:
            f.close()


if __name__ == "__main__":
    main()
