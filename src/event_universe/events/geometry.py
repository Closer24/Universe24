"""The GameBoard's geometry under the engine: the Node sets, boxes, masks and Ports of a body or a detector from the GameBoard's shape and the families' borders, and the pair arrays' cache; no physics, no number."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, cast

import numpy as np

from event_universe.core.game_board import Address3, adjacent_node, box_centre
from event_universe.core.main_loop import MainLoop
from event_universe.core.ports import Ports, port_of
from event_universe.features.spins_step import Neighbours
from event_universe.loader.world import BlockDefinition, FamilyDefinition, body_node_indices


class Body(Protocol):
    """What the geometry reads of a body: its number and family, its declaration, its lower corner and its Nodes."""

    number: int
    family: int
    definition: BlockDefinition
    corner: list[int]
    mask: np.ndarray


class GameBoardGeometry[B: Body]:
    """The engine's geometry, the methods of the simulation that compute Node sets, boxes, masks and Ports from the GameBoard's shape and cache the pair arrays; the engine supplies the state the annotations name, its momentum reading included."""

    shape: tuple[int, ...]
    ports: Ports
    families: tuple[FamilyDefinition, ...]
    kind_wrap: list[tuple[bool, bool, bool]]
    blocks: list[B]
    block_by_number: dict[int, B]
    set_block: dict[int, int]
    main_loop: MainLoop
    _pairs: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]]
    _kind_walls: dict[tuple[int, int, int], int]
    _momentum_now: Callable[[B], list[int]]

    def _span_nodes(
        self, position: tuple[int, int, int], span: tuple[int, int, int]
    ) -> list[tuple[int, int, int]]:
        found: list[tuple[int, int, int]] = []
        for dx in range(int(span[0])):
            for dy in range(int(span[1])):
                for dz in range(int(span[2])):
                    node = (int(position[0]) + dx, int(position[1]) + dy, int(position[2]) + dz)
                    if all(0 <= node[a] < self.shape[a] for a in range(3)):
                        found.append(node)
        return found

    def _box(self, corner: list[int], extents: tuple[int, int, int], family: int) -> np.ndarray:
        """The Nodes R of a block: the box of `extents` per axis (a cube's side three times; the slabs of ALGEBRA.md #a-familys-declaration) from its lower corner, wrapped on an axis the world's border makes periodic, cut on an open one (a G_48-set of Nodes, world data)."""
        mask = np.zeros(self.shape, dtype=bool)
        position = (int(corner[0]), int(corner[1]), int(corner[2]))
        nodes = body_node_indices(self._extents(), position, extents, self.kind_wrap[family])
        mask.ravel()[nodes] = True
        return mask

    def _extents(self) -> Address3:
        """The GameBoard's shape as the core's address, three integers."""
        return int(self.shape[0]), int(self.shape[1]), int(self.shape[2])

    def _faces(self, wrap: tuple[bool, bool, bool], folded: bool) -> tuple[bool, bool, bool]:
        """The faces a read wraps on: the periodic axes and, where `folded`, an axis of extent 1 (the Node itself read again)."""
        x, y, z = (bool(wrap[axis] or (folded and self.shape[axis] == 1)) for axis in range(3))
        return x, y, z

    def declared_counts(self, block: B) -> np.ndarray:
        """The count at every Node as the world file declares it for a body in the law's form (ALGEBRA.md #what-a-body-is), 0 elsewhere and everywhere for a body by its position."""
        counts = np.zeros(self.shape, dtype=np.int64)
        if block.definition.nodes is not None and block.definition.counts is not None:
            for node, count in zip(block.definition.nodes, block.definition.counts, strict=True):
                counts[node] = count
        return counts

    def body_quanta(self, block: B, amount: int) -> int:
        """A body's quanta: the world file's counts per Node summed for a body in the law's form (ALGEBRA.md #what-a-body-is), else the declared amount over its Nodes."""
        return sum(block.definition.counts or ()) or int(block.mask.sum()) * amount

    def mask_box(self, mask: np.ndarray) -> tuple[tuple[int, int], ...]:
        """The box of a body's Nodes, [low, high) per axis (HOST)."""
        axes = np.nonzero(mask)
        return tuple((int(axis.min()), int(axis.max()) + 1) for axis in axes)

    @staticmethod
    def support_box(*arrays: np.ndarray) -> tuple[tuple[int, int], ...] | None:
        """HOST: the bounding box [lo, hi) per axis of the Nodes where any of the arrays is not zero; None when every array is zero everywhere (the whole board then, the safe default)."""
        nonzero = np.zeros(arrays[0].shape, dtype=bool)
        for array in arrays:
            nonzero |= array != 0
        if not nonzero.any():
            return None
        box = []
        for axis in range(nonzero.ndim):
            along = np.any(nonzero, axis=tuple(other for other in range(nonzero.ndim) if other != axis))
            where = np.nonzero(along)[0]
            box.append((int(where[0]), int(where[-1]) + 1))
        return tuple(box)

    def centre_mask(self, block: B) -> np.ndarray:
        """The excited record's named set (ALGEBRA.md #rule3): the body's centre Node, the lower corner plus the extent // 2 on each axis, one Node (the Node itself for a body of side 1); it follows the body's steps."""
        centre = box_centre(block.corner, block.definition.extents, self.shape)
        return self._box(list(centre), (1, 1, 1), block.family)

    def _centre_node(self, block: B) -> list[int]:
        """The body's Node, the centre of its named set."""
        return [int(axis[0]) for axis in np.nonzero(self.centre_mask(block))]

    def _dipole_node(
        self, centre: list[int], family: int, j: int, sigma: int
    ) -> tuple[int, int, int] | None:
        """The Node + sigma e_j of a body's Node on the family's faces, None beyond an open face."""
        position = (int(centre[0]), int(centre[1]), int(centre[2]))
        faces = self._faces(self.kind_wrap[family], True)
        return adjacent_node(position, port_of(j, sigma), self._extents(), faces)

    def _neighbour_nodes(
        self, node: tuple[int, ...], wrap: tuple[bool, bool, bool]
    ) -> list[tuple[int, int, int]]:
        """The six reads of a Node as the send makes them: the wrap on a periodic axis, the Node itself twice on a folded axis of extent 1, none beyond an open face."""
        position = (int(node[0]), int(node[1]), int(node[2]))
        shape, faces = self._extents(), self._faces(wrap, True)
        reads = [
            adjacent_node(position, port_of(axis, side), shape, faces)
            for axis in range(3)
            for side in (1, -1)
        ]
        return [read for read in reads if read is not None]

    def _ports_of(
        self,
        level_now: np.ndarray,
        silent: bool,
        centre: tuple[int, int, int],
        wrap: tuple[bool, bool, bool],
    ) -> Neighbours:
        """A level at the six neighbours of a Node in the Ports' order, the spin's step's read (HOST): None where the loop has no read there, a silent part, an axis of extent 1 or a Node beyond an open face; the wrap on a periodic axis."""
        found: list[int | None] = []
        shape, faces = self._extents(), self._faces(wrap, False)
        for axis in range(3):
            for sigma in (1, -1):
                if silent or self.shape[axis] == 1:
                    found.append(None)
                    continue
                node = adjacent_node(centre, port_of(axis, sigma), shape, faces)
                found.append(None if node is None else int(level_now[node]))
        return cast(Neighbours, tuple(found))

    def shell_mask(self, block: B) -> np.ndarray:
        """The shell of a body: its Nodes with a Port, a Link to a Node outside the body (the wrap on a periodic axis; no Port beyond an open face; a folded axis carries none)."""
        outward = self.ports.outward(block.mask, self.kind_wrap[block.family])
        shell = np.zeros(self.shape, dtype=bool)
        for port in outward:
            shell |= port
        return shell

    def first_shell_node(self, block: B) -> tuple[int, int, int]:
        """THE FIRST SHELL NODE IN THE DECLARED ORDER (ALGEBRA.md #the-ladder, #the-postulates: which Node is read is a convention): the first Node of the body in the engine's x-major order (`body_node_indices`, the loader's and the generator's one convention) that has a Port; it follows the body's steps. A body with no shell (every Link inside it) is refused: nothing reads its residue."""
        where = np.nonzero(self.shell_mask(block))
        if len(where[0]) == 0:
            raise ValueError(
                f"measured[{block.number}] has no shell (no Node of it has a Port to "
                "a Node outside it), so no Node reads its residue (ALGEBRA.md #the-ladder)"
            )
        return int(where[0][0]), int(where[1][0]), int(where[2][0])

    def _moving_sets(self) -> dict[int, tuple[B, list[int]]]:
        """The detectors bound to a block whose momentum is not zero at this interval, each with its block and the momentum (ALGEBRA.md #the-ladder): the faces of these sets book in the body's frame; empty on a board at rest, where the rule is the Port booking alone."""
        moving: dict[int, tuple[B, list[int]]] = {}
        for detector, number in self.set_block.items():
            block = self.block_by_number[number]
            momentum = self._momentum_now(block)
            if any(momentum):
                moving[detector] = (block, momentum)
        return moving

    def _window_centre(self, block: B) -> tuple[int, int, int]:
        """The body's Node of a block with a window (its centre Node)."""
        axes = np.nonzero(self.centre_mask(block))
        return (int(axes[0][0]), int(axes[1][0]), int(axes[2][0]))

    def pair_arrays(
        self, family: int, pair: tuple[int, int] | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """THE PAIR ARRAYS of a record of `family` at its rest pair (ALGEBRA.md #the-primitives, #the-interval): num and den over the board, the pair everywhere but at the family's bodies, whose declared pairs are written at their Nodes; made once per (family, pair) by the pair folder's function through the register and kept up with the bodies' steps (`_write_pair`); `pair` None reads the family's own declared pair (refused on a family whose pair is the body's)."""
        if pair is None:
            definition = self.families[family]
            if definition.pair_on_body:
                raise ValueError(
                    f"the family {definition.name!r} declares no pair of its own; a "
                    "record's pair is read from the record (ALGEBRA.md #the-primitives, #the-interval)"
                )
            pair = definition.pair
        key = (family, int(pair[0]), int(pair[1]))
        found = self._pairs.get(key)
        if found is None:
            arrays = self.main_loop.function_of("the pair", "(i)")
            wells = [
                (block.mask, block.definition.pair) for block in self.blocks if block.family == family
            ]
            found = cast(tuple[np.ndarray, np.ndarray], arrays(self.shape, key[1:], wells))
            self._pairs[key] = found
        return found

    def _write_pair(self, block: B) -> None:
        """The block's pair written on its Nodes into every pair array of its family; the array's own pair elsewhere on the Nodes the block left."""
        self.ports.begin()
        for key in [key for key in self._kind_walls if key[0] == block.family]:
            del self._kind_walls[key]  # the family's walls read anew (`kind_wall`)
        for (family, rest_num, rest_den), (num, den) in self._pairs.items():
            if family != block.family:
                continue
            num[~block.mask] = rest_num
            den[~block.mask] = rest_den
            num[block.mask] = block.definition.pair[0]
            den[block.mask] = block.definition.pair[1]
            for other in self.blocks:
                if other is not block and other.family == block.family:
                    num[other.mask & ~block.mask] = other.definition.pair[0]
                    den[other.mask & ~block.mask] = other.definition.pair[1]


class PairView:
    """The tests' view of a family's pair arrays by its own declared pair (`kind_num[family]`, `kind_den[family]`; item 51's form): one array of the two, from `pair_arrays`."""

    def __init__(self, simulation: GameBoardGeometry[Any], index: int) -> None:
        self.simulation = simulation
        self.index = index

    def __getitem__(self, family: int) -> np.ndarray:
        return self.simulation.pair_arrays(family)[self.index]
