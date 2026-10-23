"""A bound record declared an instrument body by the host's frame tool (2026-10-21; the reader's design of the conserving click, (b): the parts, the transition and the resonance written into the mode file by the tool as a derived declaration, "declaring what the law derives until the body runs"; ALGEBRA.md, The click writes on the lattice (3) and (4); The emission of a bound record is the click's act of the taker): the mode entry's key `instrument` (loader/mode.instrument_of, typed by tools/frame_of.py) read into the declaration the engine holds for every detector body (`instrument_body`, loader/node_detector_declaration.node_detector_of), the body's levels the mode file's as laid into the part carrying its count (`laid_parts`, `Lattice.lay`), its Links uncut and the step untouched (`meeting.cut`), its standing region the Nodes its click writes over (`BodyRow.region`, `BodyRow.shares`, node_detector.books_of); so that the engine's instrument-body click runs on the bound record with no new act and no body-wide re-lay."""

from __future__ import annotations

import itertools
from dataclasses import replace
from typing import TYPE_CHECKING

from event_universe.core.rule3 import division_forward, largest_below
from event_universe.loader.derived import FamilyRule
from event_universe.loader.faces import connected
from event_universe.loader.keys import Node, integer, keyed, node_of
from event_universe.loader.mode import (
    MOVING_KEYS,
    PROFILE_KEYS,
    PROFILE_REQUIRED,
    Profile,
    instrument_of,
    levels_of,
)
from event_universe.loader.node_detector_declaration import (
    NodeDetectorDeclaration,
    node_detector_of,
    packet_form,
)

if TYPE_CHECKING:
    from event_universe.loader.packets import PacketRow
    from event_universe.loader.world import BodyRow

REGION_NODE_KEYS = ("node", "weight")  # a standing region's Node with the lay's weight (1 where absent)


def declared_body(
    row: BodyRow,
    written: object,
    label: str,
    families: tuple[FamilyRule, ...],
    quanta: dict[str, int],
    shape: Node,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool],
    bound: int,
) -> BodyRow:
    """A laid body's row with its declaration where its mode entry `written` carries the key `instrument` (`instrument_of`, `instrument_body`), the row otherwise unchanged."""
    instrument = instrument_of(written, label)
    if instrument is None:
        return row
    return instrument_body(
        row, instrument, f"{label}.instrument", families, quanta, shape, beyond, action, periodic, bound
    )


def profiles_of(
    instrument: dict[str, object],
    label: str,
    family: FamilyRule,
    declaration: NodeDetectorDeclaration,
    nodes: tuple[Node, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[Profile, ...]:
    """The transition's two levels' profiles under the instrument's key `profiles`, typed by the frame tool from Rule3's standing line (tools/frame_of.py, 2026-10-22; ALGEBRA.md, The click writes on the lattice (5): the frame's run of the body's full beat lays the two levels each at one quantum in the body's own well, and the upper level's share is read against them): one entry per part, {`part`, `now`, `before`, optionally `im_now` and `im_before`}, each level at one quantum's charge in the mode file's `moving` form, read as a body's levels are (`levels_of`: the nonzero Nodes, within the amplitude bound, none beyond the board), in the parts' order; refused by name: the key on a body with no transition, a profile of a part in no transition of the body, two profiles for one part or a part without one, and a profile standing at none of the body's declared Nodes (a level of another well); () where the key is absent, a bound body whose own-light row falls due with no frame run refused by name at that close (frame_run.hazard), the instrument of the file with its rate needing none."""
    rows, names = instrument.get("profiles"), declaration.names
    if rows is None:
        return ()
    if not declaration.transitions:
        raise ValueError(
            f"{label}.profiles stands on a body with no transition: the profiles are a transition's two levels"
        )
    if not isinstance(rows, list) or len(rows) != len(names):
        raise ValueError(
            f"{label}.profiles lists one profile per part, {len(names)} here, in the parts' order"
        )
    declared = {(x * shape[1] + y) * shape[2] + z for x, y, z in nodes}
    found: dict[int, Profile] = {}
    for index, line in enumerate(rows):
        where = f"{label}.profiles[{index}]"
        entry = keyed(line, where, PROFILE_KEYS, PROFILE_REQUIRED)
        part = integer(entry["part"], f"{where}.part", 0, len(names) - 1)
        if part in found:
            raise ValueError(
                f"{where} is a second profile of the part {names[part]!r}: one profile per part"
            )
        if not any(part in (t.leaves, t.enters) for t in declaration.transitions):
            raise ValueError(
                f"{where} is the profile of {names[part]!r}, a part in no transition of the body"
            )
        moving = {key: entry[key] for key in MOVING_KEYS if key in entry}
        entry = {"family": family.name, "pair": list(family.pair), "moving": moving}
        levels = levels_of(entry, where, family, shape, bound, beyond)
        if not any(at in declared for laid in levels[:2] for at, _level in laid):
            raise ValueError(
                f"{where} stands at none of the body's declared Nodes {[list(n) for n in nodes]}: a level of "
                "the body's own well stands at its Node"
            )
        found[part] = levels
    return tuple(found[part] for part in range(len(names)))


def instrument_body(
    row: BodyRow,
    instrument: dict[str, object],
    label: str,
    families: tuple[FamilyRule, ...],
    quanta: dict[str, int],
    shape: Node,
    beyond: tuple[Node, ...],
    action: int,
    periodic: tuple[bool, bool, bool],
    bound: int,
) -> BodyRow:
    """A bound body declared an instrument body by the host's frame tool (the mode entry's `instrument`): the declaration read in the form the loader reads for every detector body (`node_detector_of`: its `parts` with the count in the level it stands in, its `transitions`, its `rates`, its `node_detector`, the emissions' lay decided by the board's shape from every Node of its region, `packet_form`), its `nodes` the standing region with the lay's weights (one connected region of distinct Nodes through the six Ports holding one of the body's declared Nodes and every Node where a level of the laid part stands other than 0, the laid part's whole support, so that the exchange's write moves the whole quantum and leaves no tail of the part standing outside the region, charge the write would create; none beyond the board; refused by name otherwise, 2026-10-21, the cold reader's first finding on the half region), the body's levels the mode file's as laid (its record standing in its well, its Links uncut, the step untouched); the count the body's declared count, read by the gate at its declared Node as for every laid body; its light front the near zone's shell of its first transition's resonance whichever part it stands in (`near_zone`; since 2026-10-22, the transition into the standing part alone before), so that a body climbing into its upper part has its front and its frame run (`profiles_of`, frame_run.py)."""
    nodes = instrument["nodes"]
    if not isinstance(nodes, list) or not nodes:
        raise ValueError(f"{label}.nodes must list the standing region's Nodes with their weights")
    region, shares = [], []
    for index, line in enumerate(nodes):
        keyed(line, f"{label}.nodes[{index}]", REGION_NODE_KEYS, ("node",))
        region.append(node_of(line["node"], f"{label}.nodes[{index}].node", shape, beyond))
        shares.append(integer(line.get("weight", 1), f"{label}.nodes[{index}].weight", 1))
    if not any(node in region for node in row.nodes):
        raise ValueError(
            f"{label}.nodes holds none of the body's declared Nodes {[list(n) for n in row.nodes]}: the standing "
            "region stands about the Node the body is declared at"
        )
    if len(set(region)) != len(region) or not connected(tuple(region), shape, periodic):
        raise ValueError(
            f"{label}.nodes is one connected region of distinct Nodes through the six Ports, the body's standing "
            "region (ALGEBRA.md, The NodeDetector is one declaration kind for every world)"
        )
    inside = {(int(x) * shape[1] + int(y)) * shape[2] + int(z) for x, y, z in region}
    levels = (row.now, row.before, row.second_now, row.second_before)
    outside = sorted({at for laid in levels for at, level in laid if level and at not in inside})
    if outside:  # the reader's line of 2026-10-21: a tail outside the region is charge the write creates
        first = next(
            at
            for at in itertools.product(*(range(n) for n in shape))
            if (at[0] * shape[1] + at[1]) * shape[2] + at[2] == outside[0]
        )
        raise ValueError(
            f"{label}.nodes leaves the laid part's level standing outside the region at {len(outside)} Nodes, "
            f"{list(first)} the first: the standing region is the laid part's whole support, the exchange "
            "moving the whole quantum (ALGEBRA.md, The click writes on the lattice (3))"
        )
    holder = next((read for read in families[row.family].reads if families[read.family].held), None)
    rows = instrument.get("transitions", []) if isinstance(instrument, dict) else []
    for index, line in enumerate(rows if isinstance(rows, list) else []):
        if not isinstance(line, dict):
            continue  # the declaration's own check of the row follows (node_detector_of)
        if (
            "weight" in line
        ):  # (5), 2026-10-22: a bound body's coupling is its record's read weight, by reciprocity
            raise ValueError(
                f"{label}.transitions[{index}] declares the weight {line['weight']!r}: a bound body couples to its "
                "drive at its record's read weight of its holder, by reciprocity, and declares none (ALGEBRA.md, "
                "The click writes on the lattice (5), 2026-10-22)"
            )
        if holder is None:
            raise ValueError(
                f"{label}.transitions[{index}]: the family {families[row.family].name!r} reads no held family, so "
                "no read weight stands for a bound body's coupling"
            )
        line["weight"] = holder.weight
    declaration = node_detector_of(instrument, label, families, row.family, quanta, sum(row.counts))
    declaration = packet_form(declaration, label, families, tuple(region), shape, periodic, action)
    profiles = profiles_of(
        instrument, label, families[row.family], declaration, row.nodes, shape, bound, beyond
    )
    part = next((p for p, c in enumerate(declaration.counts) if c), None)  # the declared count's part
    due = part is not None and any(t.enters == part for t in declaration.transitions)
    if (
        part is not None
        and due
        and not profiles
        and not any(r.leaves == part for r in declaration.rates)
    ):
        raise ValueError(
            f"{label}: the body stands in the part {declaration.names[part]!r} with a transition into it and no "
            "rate out of it, so its own-light row falls due at its window's close, and it declares no `profiles`: "
            "the two levels the frame tool types are the A the row is weighed by (run tools/frame_of.py on the world)"
        )
    front = declaration.transitions[:1]  # the light's front of the body's transition, whichever part
    radius, shell, missing = (
        near_zone(front[0].resonance, row.nodes[0], shape, periodic) if front else (0, (), 0)
    )
    return replace(
        row,
        detector=declaration,
        region=tuple(region),
        shares=tuple(shares),
        shell=shell,
        radius=radius,
        missing=missing,
        profiles=profiles,
    )


def near_zone(
    resonance: tuple[int, int], centre: Node, shape: Node, periodic: tuple[bool, bool, bool]
) -> tuple[int, tuple[Node, ...], int]:
    """The light's front of a bound body, the near zone's edge (ALGEBRA.md, The click writes on the lattice (5), the reader's ruling of 2026-10-22): a Chebyshev shell about the body's declared Node at the radius r = 1 / k Links, k from the resonance pair [num, den] by the massless holder's own dispersion, den cos k = 3 num - 2 den exactly, den sin k by the one search (`rule3.largest_below` on den^2 - den^2 cos^2 k), the radius den div (den sin k) + 1 by the division act (4 on [5889, 6000], 3 on [5879, 6000]; 1 where no wave travels at the resonance, cos k at or beyond 1), no declared radius; the shell's Nodes on the board at that distance (the shorter way round on a periodic axis) and the count of its outward Ports that leave the board, named and not refused (a body nearer a face than the radius)."""
    num, den = resonance
    cosine = 3 * num - 2 * den  # den cos k, the massless line cos k = 3 cos Omega - 2
    sine = (
        largest_below(den * den - cosine * cosine) if -den < cosine < den else 0
    )  # den sin k, the search
    radius = int(division_forward(den, sine, 0)[0]) + 1 if sine > 0 else 1
    shell: list[Node] = []
    missing = 0
    for x, y, z in itertools.product(*(range(n) for n in shape)):
        at: Node = (x, y, z)
        distances = [
            min(abs(a - c), n - abs(a - c)) if wraps else abs(a - c)
            for a, c, n, wraps in zip(at, centre, shape, periodic, strict=True)
        ]
        if max(distances) != radius:
            continue
        shell.append(at)
        for a, c, n, wraps, d in zip(at, centre, shape, periodic, distances, strict=True):
            if d == radius and not wraps:
                missing += not (0 <= a + (1 if a > c else -1) < n)  # the outward Port off the board
    return radius, tuple(shell), missing


def laid_parts(row: BodyRow | PacketRow, family: FamilyRule) -> list[int]:
    """The parts of a record the mode file's levels are laid on (`Lattice.lay`): every part alike for a packet and for a body without a declaration (the pair family's two parts laid equal, ALGEBRA.md #the-click-is-the-meeting), and for a bound body declared an instrument body the part carrying its declared count alone, the level it stands in (the other parts empty, a lay in one mode having no amplitude in any other, The click writes on the lattice (j))."""
    detector = getattr(row, "detector", None)
    if detector is None:
        return list(range(family.parts))
    return [part for part, count in enumerate(detector.counts) if count]
