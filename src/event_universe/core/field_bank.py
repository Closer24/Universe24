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
    @property
    def conserved_width(self) -> int: ...
    def inventory_state(self, state: Record) -> tuple[int, ...]: ...
    def inventory_packet(self, packet: Record) -> tuple[int, ...]: ...
    def source_amount(self, sources: int, phase: int) -> tuple[int, ...]: ...
    def sink_amount(self, old: Record, sources: int, phase: int) -> tuple[int, ...]: ...
    def publish(self, old: Record, sources: int, phase: int) -> tuple[Packets, Record]: ...
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
            checked(definition.conserved_width)
            if definition.conserved_width < 1:
                raise ValueError("a field requires fixed conserved channels")
            neutral = (0,) * definition.conserved_width
            if (
                self._quantities(definition, definition.inventory_state(zero.state)) != neutral
                or self._quantities(definition, definition.inventory_packet(definition.zero_packet))
                != neutral
            ):
                raise ValueError("neutral sparse records must have zero conserved inventory")
            emitted, retained = self._publish(definition, zero.state, 0, 0)
            state, faces = self._absorb(definition, retained, (definition.zero_packet,) * 6, 0, 0)
            definition.validate_state(state)
            definition.validate_faces(faces)
            if (
                emitted != (definition.zero_packet,) * 6
                or retained != zero.state
                or state != zero.state
                or faces != ZERO_RESPONSE
            ):
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

    def inventory_at(self, address: Address, index: int = 0) -> tuple[int, ...]:
        """Measured conserved channels, including retained division remainders."""
        definition = self._definitions[index]
        return self._quantities(definition, definition.inventory_state(self.at(address, index).state))

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
                self._quantities(definition, definition.inventory_state(record.state))

    @staticmethod
    def _quantities(definition: Definition, values: tuple[int, ...]) -> tuple[int, ...]:
        if not isinstance(values, tuple) or len(values) != definition.conserved_width:
            raise ValueError("inventory must match the fixed conserved channel count")
        for value in values:
            checked_work(value)
            if value < 0:
                raise ValueError("conserved inventory must be non-negative")
        return values

    @staticmethod
    def _add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(checked_work(a + b) for a, b in zip(left, right, strict=True))

    def _packet_total(self, definition: Definition, packets: Packets) -> tuple[int, ...]:
        total = (0,) * definition.conserved_width
        for packet in packets:
            total = self._add(total, self._quantities(definition, definition.inventory_packet(packet)))
        return total

    def _publish(
        self, definition: Definition, old: Record, sources: int, phase: int
    ) -> tuple[Packets, Record]:
        outgoing, retained = definition.publish(old, sources, phase)
        definition.validate_outgoing(outgoing)
        definition.validate_state(retained)
        available = self._add(
            self._quantities(definition, definition.inventory_state(old)),
            self._quantities(definition, definition.source_amount(sources, phase)),
        )
        accounted = self._add(
            self._packet_total(definition, outgoing),
            self._quantities(definition, definition.inventory_state(retained)),
        )
        accounted = self._add(
            accounted, self._quantities(definition, definition.sink_amount(old, sources, phase))
        )
        if available != accounted:
            raise ValueError("field publication violates channel flux conservation")
        return outgoing, retained

    def _absorb(
        self, definition: Definition, retained: Record, incoming: Packets, sources: int, phase: int
    ) -> tuple[Record, Faces]:
        definition.validate_incoming(incoming)
        state, faces = definition.absorb(retained, incoming, sources, phase)
        definition.validate_state(state)
        definition.validate_faces(faces)
        available = self._add(
            self._quantities(definition, definition.inventory_state(retained)),
            self._packet_total(definition, incoming),
        )
        if available != self._quantities(definition, definition.inventory_state(state)):
            raise ValueError("field absorption violates channel flux conservation")
        return state, faces

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
        retained_states: dict[Address, list[Record]] = {}
        for address in tuple(work):
            retained_states[address] = []
            for index, definition in enumerate(self._definitions):
                outgoing, retained = self._publish(
                    definition, self.at(address, index).state, sources.get(address, 0), phase
                )
                retained_states[address].append(retained)
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
                retained = (
                    retained_states[address][index]
                    if address in retained_states
                    else definition.zero_state
                )
                state, faces = self._absorb(
                    definition, retained, incoming, sources.get(address, 0), phase
                )
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
