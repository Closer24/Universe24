"""The assembly of the engine's state from the parsed world, out of the loop's module: the bodies' held counts, the detectors and their map, the universe's values, the arrays and caches of the interval, the bodies' blocks with their own records, and the held families' records; each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and the parsed world, sets the same attributes the loop's `__init__` set, in the same order, and is called from it once before the first interval."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.features.polariser import read_term
from event_universe.features.receive import ReceiveTerm
from event_universe.loader.world import NatureBeamWorld

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def held_table(world: NatureBeamWorld) -> list[list[int]]:
    """Every body's held quanta per family: its declared counts, padded with zeros to the families' number."""
    count = len(world.families)
    return [list(entry.held) + [0] * (count - len(entry.held)) for entry in world.measured]


def detectors(loop: DetectorLawSimulation, world: NatureBeamWorld) -> None:
    """The detectors, index 0 .. K - 1: each measured event's, the sets' (a set bound to a body a receiver), the face receiver's slab on every open axis, and the map of the Node to its detector."""
    # The detectors: index 0 .. K - 1 with a name, the Nodes of each, and the
    # measured event (if any) that receives the content of a click there.
    # A detector set is ONE detector over its whole cube: the flux into the
    # cube through its Ports from outside is its increment, the click is the
    # detector's, reported by its name, never by a Node.
    loop.detector_names = []
    loop.detector_measured = []
    loop.detector_face = []
    # The gather's detector triple [set, channel, label]: a detector's set name
    # (its own name but for a table body's two detectors, which carry their
    # set's name) and its channel (0, the + channel; 1 the - channel of
    # a table body); every detector as built is [name, 0, "0"].
    loop.detector_set = []
    loop.detector_channel = []
    loop.detector_at_node = np.full(loop.shape, -1, dtype=np.int64)
    # the Port pairs per family for the detectors' inflow, listed once on first use
    loop._inflow_port_pairs = {}
    # the Ports' faces beside the pairs (axis, side), item 56
    loop._inflow_port_faces = {}
    for number, entry in enumerate(world.measured):
        nodes = loop._span_nodes(entry.position, entry.span)
        own = loop._detector(f"measured:{number}", number, False)
        for node in nodes:
            loop.detector_at_node[node] = own
    # The sets bound to a block are receivers (DECLARATIONS.md section 10 item 9, section 13 item 1): their
    # Nodes take (the one-way Port take, the row held at 0, the offer booked to the set's detector, the click
    # at the first rung stamped with the block's own count); a set with one declared position is the Node
    # beside the block, one without positions takes at the block's current Nodes (`set_block`, `set_nodes`).
    loop.set_block = {}
    # the detector sets in their declared order: the ladder of a
    # record that names no receiver (ALGEBRA.md #rule3)
    loop.set_detectors = []
    loop.set_nodes = {}
    # THE TABLES ARE RETIRED (the cleanup order's step 3; ALGEBRA.md #the-postulates):
    # a measured event with a table entry (a polariser's window, a
    # splitter's rows) is refused here; the polariser returns as a body
    # with an axis and two receivers named, a splitter as a region of the
    # one operator
    for number, entry in enumerate(world.measured):
        if any(window is not None for window in entry.windows) or any(
            split is not None for split in entry.splits
        ):
            raise ValueError(
                f"measured[{number}].table is refused: the "
                "tables (the polariser's two detectors at one Node, the splitter's linear form) "
                "retired with the flux reading (the given pair on the circle; BUILD.md section 26 item 17); a polariser is "
                "a body with an axis and two receivers named, a splitter a region of the one "
                "operator (ALGEBRA.md #the-postulates)"
            )
    for detector in world.detectors:
        set_detector: int | None = None
        if detector.block is not None:
            set_detector = loop._detector(detector.name, detector.block, False)
            loop.set_block[set_detector] = detector.block
            loop.set_detectors.append(set_detector)
            if detector.positions:
                nodes_mask = np.zeros(loop.shape, dtype=bool)
                for position in detector.positions:
                    node = (int(position[0]), int(position[1]), int(position[2]))
                    nodes_mask[node] = True
                    loop.detector_at_node[node] = set_detector
                loop.set_nodes[set_detector] = nodes_mask
            else:
                loop.set_nodes[set_detector] = None
            continue
        for position in detector.positions:
            node = (int(position[0]), int(position[1]), int(position[2]))
            existing = int(loop.detector_at_node[node])
            measured = loop.detector_measured[existing] if existing >= 0 else None
            if set_detector is None:
                set_detector = loop._detector(detector.name, measured, False)
                loop.set_detectors.append(set_detector)
            elif measured is not None and loop.detector_measured[set_detector] is None:
                loop.detector_measured[set_detector] = measured
            loop.detector_at_node[node] = set_detector
    # THE FACE RECEIVER (ALGEBRA.md #rule3): an open axis carries the receiver `face` at its border,
    # last on every ladder, so what leaves the board clicks there; a periodic axis has none; a `closed` face
    # is a zero row with no receiver. THE FACE SLAB (ALGEBRA.md #the-ladder): the receiver is the slab of `face_depth`
    # free Nodes nearest every open border, one detector, its Ports toward the interior alone.
    loop.face_detector = None
    for axis in range(3):
        if world.periodic[axis] or world.closed[axis] or loop.shape[axis] < 2:
            continue
        if loop.face_detector is None:
            loop.face_detector = loop._detector("face", None, True)
        depth = min(world.face_depth, loop.shape[axis])
        for index in [*range(depth), *range(loop.shape[axis] - depth, loop.shape[axis])]:
            view = np.moveaxis(loop.detector_at_node, axis, 0)[index]
            free = view < 0
            view[free] = loop.face_detector


def universe_values(loop: DetectorLawSimulation, world: NatureBeamWorld) -> None:
    """The universe's integers on the engine: the momentum's unit Q, the twist table as arrays with the receive's term, the self-source cache and the Node clock Gamma; a world without a unit or a clock is refused by name."""
    # THE NODE CLOCK (ALGEBRA.md #the-paces): the world's Gamma and the content M at every Node (the
    # held quanta of every family at every measured event's Nodes, 0 in the vacuum), the clock pair
    # (Gamma, Gamma + M) in every family's rule at the Node; M changes only at the law's events, so the
    # array is rebuilt from the held books as each interval begins (`_hold`) and after a giving.
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md #the-primitives): the universe's integer; every body's wall is W = 3 Q M.
    loop.momentum_unit = int(world.momentum_unit)
    if loop.momentum_unit < 1:
        raise ValueError(
            "the world declares no momentum unit (`momentum_unit`, Q from 1; ALGEBRA.md #the-primitives)"
        )
    # THE TWIST TABLE (ALGEBRA.md #the-transport, #the-primitives; commit 4): the universe's
    # triples as arrays, (c, s, d) by k_0 (fine) and by k_1 (coarse); None on a world
    # without one, where a nonzero twist is refused naming the Port
    loop.twist_table = world.twist_table
    loop._receive_term = ReceiveTerm(None, None, 0)
    if loop.twist_table is not None:
        loop._fine = np.array(loop.twist_table.fine, dtype=np.int64).T
        loop._coarse = np.array(loop.twist_table.coarse, dtype=np.int64).T
        loop._receive_term = ReceiveTerm(loop._fine, loop._coarse, loop.twist_table.fine_bits)
    # HOST: the self-source per family per interval (ALGEBRA.md #the-interval), None at P_2 = 0
    loop._sources = {}
    loop.node_clock = int(world.node_clock)
    if loop.node_clock < 1:
        raise ValueError(
            "the world declares no Node clock (`node_clock`, Gamma from 1; "
            "ALGEBRA.md #the-paces; BUILD.md section 26 item 31)"
        )


def state_arrays(loop: DetectorLawSimulation, world: NatureBeamWorld) -> None:
    """The arrays and caches of the interval: the held families' levels and charges, the paces' carries, the leak marks, the spans, the records' table, the bodies' lists and the pair arrays by (family, pair) with each family's wrap."""
    # THE FAMILY GENERICITY (ALGEBRA.md #the-counts-line, #the-paces): the engine knows no family's name or role. A family
    # with a declared `held` source has one record over the board (`held_records`), its level at every
    # body's Nodes the body's declared source (both levels, the remainder 0), written at the load and at
    # every click, elsewhere its own plain step after the other families'; never booked, no click of its
    # own. `node_level` is each held family's level as every reading family's step reads it
    # (`_effective_content`: SUM weight x level, or - q x weight x level by the reader's charge sign q).
    loop.held_families = list(world.held_families)
    loop.family_charge = [int(family.charge[0]) for family in world.families]
    loop.node_level = {family: np.zeros(loop.shape, dtype=np.int64) for family in loop.held_families}
    loop._effective = {}  # HOST: per interval, cleared by the hold
    # THE FOUR PACES (ALGEBRA.md #the-interval; commit 3): per reading family the
    # three axis contents t_a (the reads' aa components halved, the division's
    # remainder carried per Node, `_pace_carry` keyed (family, read, axis)),
    # computed once per interval (HOST cache by tick); None where every read's
    # tensor part is silent (the isotropic rule, bit for bit)
    loop._pace_carry = {}
    loop._axis_effective = {}
    # THE LEAK TEST (BUILD.md section 26 item 55): a held family no body has ever
    # sourced must be exactly zero everywhere; the hold marks the first nonzero
    # source (HOST, a flag per held family, read by `leaks`)
    # per part (ALGEBRA.md #the-interval): (family, part), the time part 0
    loop._sourced_ever = {
        (family, part): False
        for family in loop.held_families
        for part in range(loop.families[family].components)
    }
    loop.span_masks, loop.span_hold = {}, {}
    for number, entry in enumerate(world.measured):
        if entry.block is None:
            span = np.zeros(loop.shape, dtype=bool)
            for node in loop._span_nodes(entry.position, entry.span):
                span[node] = True
            loop.span_masks[number] = span
    loop.records = {}
    # HOST: `kind_wall` per (family, pair), cleared by `_write_pair`
    loop._kind_walls = {}
    # the records clicked this interval, deleted whole after the advances
    loop.dead = []
    loop.blocks = []
    loop.block_by_number = {}
    # The block's count at a light record's first rung at its detector
    # (the click's `clock`, the body's event in the body's own clock).
    loop.rung_counts = {}
    # THE PAIR ARRAYS BY (FAMILY, PAIR) (ALGEBRA.md #the-primitives, #the-interval): per family the pair on the
    # six-neighbour term as two dense int64 arrays over the board, a record's rows stepping with their own
    # rest pair everywhere but at the bodies of the family, whose wells (the lowered pair) are written into
    # every array of the family; made once per (family, pair) on first use (`pair_arrays`); one border for
    # every family (the world's `boundary`).
    loop._pairs = {}
    loop.kind_wrap = [world.kind_periodic(index) for index in range(len(world.families))]


def bodies(loop: DetectorLawSimulation, world: NatureBeamWorld) -> None:
    """The bodies' blocks: every measured event with a block, its Nodes written into its family's pair arrays, its own record seeded on its Nodes, the blocks' Nodes on the detector map and the receiver by name."""
    # The blocks (massive-record-v1): every measured event with a block,
    # its Nodes written into its kind's pair arrays, its own record
    # seeded on its Nodes and its momentum on its wall W = 3 Q M (`wall_of`).
    for number, entry in enumerate(world.measured):
        if entry.block is None:
            continue
        definition = entry.block
        corner = [int(entry.position[axis]) for axis in range(3)]
        mask = loop._box(corner, definition.extents, entry.family)
        if definition.nodes is not None:
            mask = np.zeros(loop.shape, dtype=bool)
            mask[tuple(np.array(definition.nodes).T)] = True
        block = loop._block(number, entry, definition, corner, mask)
        loop._write_pair(block)
        identity = -1 - number
        if definition.seed > 0:
            own_record = loop._massive_record(
                identity, number, entry.family, definition.kind, definition.twist
            )
            if definition.profile is not None:
                # the declared integer profile over the whole board at both
                # levels (a standing start on the bound mode: MASSIVE_RECORD.md
                # section 11 item 7), the world file's integers and nothing else
                profile = np.array(definition.profile, dtype=np.int64).reshape(loop.shape)
                own_record.now[:] = profile
                own_record.before[:] = profile
            else:
                own_record.now[mask] = definition.seed
                own_record.before[mask] = definition.seed
            own_record.standing = True  # a body's own record, read by no detector (item 51)
            block.own = own_record
            loop.records[own_record.identity] = own_record
            block.previous_sum = int(np.sum(own_record.now[mask]))
            if definition.emitter is not None:
                # the first excited record (ALGEBRA.md #the-click): the
                # seed at both levels, its residue the first of the wheel,
                # its norm the seed's squares over the body's Nodes
                loop._excite(block, own_record)
        loop.blocks.append(block)
        loop.block_by_number[number] = block
    loop.polarisers = {
        b.number: t for b in loop.blocks if (t := read_term(dict(b.definition.declared))) is not None
    }
    # The blocks' Nodes: a block's Nodes carry its detector's index (the flux
    # into them booked to it, never chosen: the detector is on no ladder); a
    # set bound to a block without positions owns the block's Nodes
    # instead (the flux into them booked to the set; a set bound to a block is a receiver). Nothing
    # takes (ALGEBRA.md #rule3): the rows evolve at every detector.
    if loop.blocks:
        for block in loop.blocks:
            for node in zip(*np.nonzero(block.mask), strict=True):
                address = (int(node[0]), int(node[1]), int(node[2]))
                loop.detector_at_node[address] = block.detector
        for set_detector, number in loop.set_block.items():
            if loop.set_nodes[set_detector] is None:
                block = loop.block_by_number[number]
                loop.detector_at_node[block.mask] = set_detector
    # The receiver by name (DECLARATIONS.md section 13 item 7): an
    # emitting block's `receiver` names the detector set whose one detector
    # is the ladder of every record it emits (the click line at that
    # detector's first rung after the train; the faces and every other set
    # sinks for it, their take into `absorbed` alone and onto no pointer).
    # A block without the key keeps the ladder of every detector and the line
    # at the close, as before the key (the registered worlds byte for byte).
    loop.receiver_detector = {}
    for block in loop.blocks:
        name = block.definition.receiver
        if name is None:
            continue
        if name not in loop.detector_names:
            raise ValueError(
                f"measured[{block.number}].receiver {name!r} names no detector of the "
                f"simulation (the detectors: {loop.detector_names})"
            )
        loop.receiver_detector[block.number] = loop.detector_names.index(name)
    loop.has_receiver = bool(loop.receiver_detector)


def held_records(loop: DetectorLawSimulation) -> None:
    """The held families' records (the time part and the silent further parts), the sourced families' records after them, and the source's argument and remainders per Node."""
    # the held families' records (item 51): the load's write, each family's
    # declared source held at every body's Nodes and 0 elsewhere (ALGEBRA.md
    # ALGEBRA.md #the-counts-line, #the-paces); the identities below 0, one per held family
    loop.held_records = {
        family: loop._held_part(position, family, 0)
        for position, family in enumerate(loop.held_families)
    }
    # THE OTHER PARTS of a held family (ALGEBRA.md #the-primitives, #the-interval; commit
    # 1): one record per component beyond the time part (gravity's nine,
    # the charge's three), zero and silent until a hold writes them (the
    # vector and tensor holds, commit 2); stepped with the time part
    loop.held_parts = {
        family: [
            loop._held_part(position, family, part)
            for part in range(1, loop.families[family].components)
        ]
        for position, family in enumerate(loop.held_families)
    }
    for parts in loop.held_parts.values():
        for record in parts:
            record.silent = True
    # THE SOURCED FAMILIES (ALGEBRA.md #the-primitives row "the source"): a field written from a
    # record family's count has one record over the board, stepped as a held family's
    # is, its identity after the held families'; the counts D_i summed per record family
    # at the step and the remainder per Node are the source's own, read at its act
    loop.sourced_records = {
        family: loop._held_part(len(loop.held_families) + position, family, 0)
        for position, family in enumerate(
            index
            for index, definition in enumerate(loop.families)
            if definition.sourced is not None and definition.held is None
        )
    }
    loop._source_argument = {
        definition.sourced[0]: np.zeros(loop.shape, dtype=np.int64)
        for definition in loop.families
        if definition.sourced is not None
    }
    loop._source_remainders = {
        family: np.zeros(loop.shape, dtype=np.int64)
        for family, definition in enumerate(loop.families)
        if definition.sourced is not None
    }


def start_at_rest(loop: DetectorLawSimulation) -> None:
    """THE START (ALGEBRA.md #the-generator, THE START): every held family's time part at the load at its rest, the fixed point of the family's line under the hold's rewrite, by the folder found by its name, once before the first interval and never in it; the rest on the counts the load's hold wrote at the bodies' Nodes (0 elsewhere), its levels written at both levels with the remainder 0, `node_level` the same array; a family no body holds stays at 0, and the folder's refusal names the family."""
    start = loop.register.at("the start", "any")
    for family, record in loop.held_records.items():
        if not record.now.any():
            continue
        try:
            field: Any = start(record.now, loop.families[family].pair, loop.kind_wrap[family])
            levels = field.levels
        except ValueError as refusal:
            raise ValueError(
                f"the start of the held family {loop.families[family].name!r}: {refusal}"
            ) from refusal
        record.now[...] = levels
        record.before[...] = levels
        record.remainder[...] = 0
        loop.node_level[family] = record.now
