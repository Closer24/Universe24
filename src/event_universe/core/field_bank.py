"""One sparse, unit-edge scheduler for a fixed tuple of injected field definitions."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import NamedTuple, Protocol, cast

from .lattice import PeriodicLattice
from .state import Address, Vector, checked, checked_work

Record = tuple[int, ...]
Packets = tuple[Record, Record, Record, Record, Record, Record]
Magnitude = tuple[int, int]
Faces = tuple[Magnitude, Magnitude, Magnitude, Magnitude, Magnitude, Magnitude]
ZERO_RESPONSE: Faces = ((1, 1),) * 6


class Definition(Protocol):
    """Pure local callbacks; zero inputs must be quiescent at every phase."""

    @property
    def name(self) -> str: ...
    @property
    def zero_state(self) -> Record: ...
    @property
    def zero_packet(self) -> Record: ...
    @property
    def response_unit(self) -> str: ...
    def publish(self, old: Record, sources: int, phase: int) -> Packets: ...
    def absorb(
        self, old: Record, incoming: Packets, sources: int, phase: int
    ) -> tuple[Record, Faces]: ...
    def response(self, faces: Faces) -> Vector: ...
    def validate_state(self, state: Record) -> None: ...
    def validate_outgoing(self, packets: Packets) -> None: ...
    def validate_incoming(self, packets: Packets) -> None: ...
    def validate_faces(self, faces: Faces) -> None: ...


class FieldCell(NamedTuple):
    state: Record
    response_faces: Faces


class FieldBank:
    """All fields publish old state, route one edge, then absorb atomically.

    F and every schema width are fixed at construction. Dictionary iteration is
    host work; each local operation has six ports per definition. No field name
    selects an engine branch. Longer links require an explicit buffering law and
    are deliberately unsupported here. Stored records contain positive codes.
    """

    def __init__(
        self, lattice: PeriodicLattice, definitions: tuple[Definition, ...], *, link_length: int = 1
    ) -> None:
        checked(link_length)
        if link_length < 1:
            raise ValueError("link length must be positive")
        if link_length != 1:
            raise NotImplementedError("the generic field bank currently supports unit links only")
        if not isinstance(definitions, tuple) or not definitions:
            raise ValueError("a fixed nonempty tuple of field definitions is required")
        if len({d.name for d in definitions}) != len(definitions):
            raise ValueError("field definition names must be unique")
        if len({d.response_unit for d in definitions}) != 1:
            raise ValueError("combined fields must declare the same response unit")
        self._lattice = lattice
        self._definitions = definitions
        self._zero = tuple(FieldCell(d.zero_state, ZERO_RESPONSE) for d in definitions)
        self._cells: dict[Address, tuple[FieldCell, ...]] = {}
        for definition, zero in zip(definitions, self._zero, strict=True):
            definition.validate_state(zero.state)
            emitted = definition.publish(zero.state, 0, 0)
            definition.validate_outgoing(emitted)
            state, faces = definition.absorb(zero.state, (definition.zero_packet,) * 6, 0, 0)
            definition.validate_state(state)
            definition.validate_faces(faces)
            if emitted != (definition.zero_packet,) * 6 or state != zero.state or faces != ZERO_RESPONSE:
                raise ValueError("sparse field definitions must preserve their quiescent zero")
            if definition.response(faces) != (0, 0, 0):
                raise ValueError("a zero field cannot produce a response")

    @property
    def definitions(self) -> tuple[Definition, ...]:
        return self._definitions

    @property
    def cells(self) -> Mapping[Address, tuple[FieldCell, ...]]:
        """Read-only snapshot view of the last committed field records."""
        return MappingProxyType(self._cells)

    def at(self, address: Address, index: int = 0) -> FieldCell:
        return self._cells.get(self._lattice.wrap(address), self._zero)[index]

    def response_at(self, address: Address) -> Vector:
        total = (0, 0, 0)
        for index, definition in enumerate(self._definitions):
            vector = definition.response(self.at(address, index).response_faces)
            if not isinstance(vector, tuple) or len(vector) != 3:
                raise ValueError("a definition response must return three working integers")
            total = cast(
                Vector,
                tuple(checked_work(a + checked_work(b)) for a, b in zip(total, vector, strict=True)),
            )
        return total

    @property
    def registers_per_cell(self) -> int:
        return sum(len(record.state) + 12 for record in self._zero)

    def validate(self) -> None:
        """Host audit of actual persisted records, outside the physical update."""
        for address, records in self._cells.items():
            if self._lattice.wrap(address) != address or len(records) != len(self._definitions):
                raise ValueError("invalid field-bank address or fixed definition count")
            for definition, record in zip(self._definitions, records, strict=True):
                definition.validate_state(record.state)
                definition.validate_faces(record.response_faces)

    def advance(self, sources: Mapping[Address, int], phase: int) -> None:
        checked(phase)
        if phase < 0:
            raise ValueError("phase must be non-negative")
        for address, count in sources.items():
            checked(count)
            if count < 0 or self._lattice.wrap(address) != address:
                raise ValueError("sources require canonical addresses and non-negative counts")
        work = set(self._cells) | set(sources)
        arrivals: dict[Address, list[list[Record]]] = {}
        for address in tuple(work):
            for index, definition in enumerate(self._definitions):
                outgoing = definition.publish(
                    self.at(address, index).state, sources.get(address, 0), phase
                )
                definition.validate_outgoing(outgoing)
                for direction, packet in enumerate(outgoing):
                    if packet == definition.zero_packet:
                        continue
                    target = self._lattice.neighbor(address, direction)
                    if target not in arrivals:
                        arrivals[target] = [[d.zero_packet] * 6 for d in self._definitions]
                    arrivals[target][index][direction ^ 1] = packet
                    work.add(target)
        proposals: dict[Address, tuple[FieldCell, ...]] = {}
        for address in work:
            records = []
            for index, definition in enumerate(self._definitions):
                incoming = (
                    cast(Packets, tuple(arrivals[address][index]))
                    if address in arrivals
                    else (definition.zero_packet,) * 6
                )
                definition.validate_incoming(incoming)
                state, faces = definition.absorb(
                    self.at(address, index).state, incoming, sources.get(address, 0), phase
                )
                definition.validate_state(state)
                definition.validate_faces(faces)
                vector = definition.response(faces)
                if not isinstance(vector, tuple) or len(vector) != 3:
                    raise ValueError("a definition response must return three working integers")
                for value in vector:
                    checked_work(value)
                records.append(FieldCell(state, faces))
            committed = tuple(records)
            if committed != self._zero:
                proposals[address] = committed
        self._cells = proposals
