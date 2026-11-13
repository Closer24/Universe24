"""Passive node and internal-face views of the regular 48-channel state.

A node has six ports, each grouping eight existing directional channels. This
grouping is by propagation-frame label, not by exclusive input ownership: a
channel's polynomial may read either neighboring face when locality permits.
An edge is a shared *topological reference* between two ports, not a new state
bank, stored travel time, metric or geometric length. Only the Engine evolves
``State``. These accessors do not implement an additional update mechanism.

Views retain a reference to the supplied State, not copies of its arrays. A
new Engine output needs a new view; a view does not silently follow evolution.
Returned values are immutable Python-integer tuples for passive inspection.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .algebra.group_2o import group
from .core import State
from .core.lattice import DIRECTIONS, DIRECTION_NAMES, lattice


def _integer_in_range(value, upper, name):
    if type(value) is not int or not 0 <= value < upper:
        raise ValueError(f"{name} must be an integer in 0..{upper - 1}")


def _check_state(state):
    if not isinstance(state, State):
        raise TypeError("node views require a complete State")
    if state.G != 48:
        raise ValueError("the regular node view requires exactly 48 channels")


def _bank(state, name):
    if name not in ("a", "b", "r"):
        raise ValueError("bank must be 'a', 'b' or 'r'")
    return getattr(state, name)


@lru_cache(maxsize=1)
def face_channels():
    """Six immutable channel groups in +x,-x,+y,-y,+z,-z order.

    This uses only the regular representation's frame, not a selected tensor
    or a claim that every admitted tensor transports an optical signal.
    """
    directions = tuple(tuple(rotation[i][0] for i in range(3))
                       for rotation in group().rotations)
    return tuple(tuple(g for g, n in enumerate(directions) if n == direction)
                 for direction in DIRECTIONS)


@dataclass(frozen=True, slots=True)
class EdgeRef:
    """One periodic undirected adjacency, named by its positive-axis base.

    Equality identifies the same edge from either endpoint, including across
    a periodic boundary. ``base`` is a naming convention, not state ownership.
    No edge variable or dynamical history is stored here.
    """

    L: int
    base: int
    axis: int

    def __post_init__(self):
        lat = lattice(self.L)
        _integer_in_range(self.base, lat.N, "base")
        _integer_in_range(self.axis, 3, "axis")

    @property
    def key(self):
        return (self.L, self.base, self.axis)

    @property
    def endpoints(self):
        return (self.base, lattice(self.L).neighbour(self.base, 2 * self.axis))

    def ports(self, state):
        """Return the two facing ports of this reference on one snapshot."""
        _check_state(state)
        if state.L != self.L:
            raise ValueError("edge and state must use the same periodic cube")
        left, right = self.endpoints
        return (FacePort(state, left, 2 * self.axis),
                FacePort(state, right, 2 * self.axis + 1))


@dataclass(frozen=True, slots=True, eq=False)
class FacePort:
    """Eight channels inside a node, associated with one neighboring face.

    ``opposite`` is the neighbor's facing port. The two ports share adjacency
    identity but read their respective node's retained state. Their values
    need not agree; this interface does not impose an unproved common length.
    A channel's face label does not restrict its tensor to reading this edge
    alone or imply interaction with every other face group.
    """

    state: State
    node_index: int
    direction: int

    def __post_init__(self):
        _check_state(self.state)
        _integer_in_range(self.node_index, self.state.N, "node index")
        _integer_in_range(self.direction, 6, "direction")

    @property
    def name(self):
        return DIRECTION_NAMES[self.direction]

    @property
    def offset(self):
        return DIRECTIONS[self.direction]

    @property
    def channels(self):
        return face_channels()[self.direction]

    @property
    def central_pairs(self):
        partner = group().multiplication[group().central]
        return tuple((g, partner[g]) for g in self.channels if g < partner[g])

    @property
    def neighbour_index(self):
        return self.state.lattice.neighbour(self.node_index, self.direction)

    @property
    def edge(self):
        base = self.neighbour_index if self.direction % 2 else self.node_index
        return EdgeRef(self.state.L, base, self.direction // 2)

    @property
    def opposite(self):
        return FacePort(self.state, self.neighbour_index, self.direction ^ 1)

    @property
    def node(self):
        return NodeView(self.state, self.node_index)

    def values(self, bank="b"):
        values = _bank(self.state, bank)
        return tuple(int(values[g, self.node_index]) for g in self.channels)

    def triples(self):
        return tuple(self.state.gear(g, self.node_index) for g in self.channels)

    def central_contrasts(self, bank="b"):
        """Signed passive differences; not additional clock or metric state."""
        values = _bank(self.state, bank)
        return tuple(int(values[g, self.node_index]) - int(values[h, self.node_index])
                     for g, h in self.central_pairs)

    def pair_sums(self, bank="b"):
        values = _bank(self.state, bank)
        return tuple(int(values[g, self.node_index]) + int(values[h, self.node_index])
                     for g, h in self.central_pairs)


@dataclass(frozen=True, slots=True, eq=False)
class NodeView:
    """Six internal ports partitioning one node's 144 retained integers.

    This is a diagnostic view of retained state, not the observer's click
    stream. It adds no public claim of matter, light or spacetime reconstruction.
    """

    state: State
    index: int

    def __post_init__(self):
        _check_state(self.state)
        _integer_in_range(self.index, self.state.N, "node index")

    @property
    def coordinates(self):
        return self.state.lattice.coords(self.index)

    @property
    def faces(self):
        return tuple(self.face(direction) for direction in range(6))

    def face(self, direction):
        return FacePort(self.state, self.index, direction)

    def values(self, bank="b"):
        values = _bank(self.state, bank)
        return tuple(int(values[g, self.index]) for g in range(48))

    def triples(self):
        return tuple(self.state.gear(g, self.index) for g in range(48))
