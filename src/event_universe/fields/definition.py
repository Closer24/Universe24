"""Immutable, schema-sized field definitions for a common six-port runtime."""

from collections.abc import Callable
from dataclasses import dataclass

from event_universe.core.state import Vector, checked
from event_universe.fields.encoding import EncodedMagnitude, decode_signed, decode_values

FieldRecord = tuple[int, ...]
FacePackets = tuple[FieldRecord, FieldRecord, FieldRecord, FieldRecord, FieldRecord, FieldRecord]
ResponseFaces = tuple[
    EncodedMagnitude,
    EncodedMagnitude,
    EncodedMagnitude,
    EncodedMagnitude,
    EncodedMagnitude,
    EncodedMagnitude,
]
PublishResult = tuple[FacePackets, FieldRecord]
PublishRule = Callable[[FieldRecord, int, int], PublishResult]
AbsorbRule = Callable[[FieldRecord, FacePackets, int, int], tuple[FieldRecord, ResponseFaces]]
ResponseRule = Callable[[ResponseFaces], Vector]
EncodingValidator = Callable[[FieldRecord], None]
Inventory = tuple[int, ...]
InventoryRule = Callable[[FieldRecord], Inventory]
SourceAmountRule = Callable[[int, int], Inventory]
SinkAmountRule = Callable[[FieldRecord, int, int], Inventory]


def validate_magnitude_pairs(record: FieldRecord) -> None:
    """The supplied definitions store canonical magnitude/sign-code pairs."""
    decode_values(record)


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    """All local policies and fixed schemas; no engine, world or evolving state.

    Publish consumes an OLD record and returns outgoing packets plus retained
    state. After transport, absorb consumes that retained state and six newly
    delivered packets. Explicit source and sink budgets apply at publication;
    absorption only combines retained inventory with delivered packets. The bank
    does not branch on field names. Response returns transient signed working arithmetic for
    the existing dynamics adapter, not a stored negative field register.
    """

    name: str
    state_width: int
    packet_width: int
    zero_state: FieldRecord
    zero_packet: FieldRecord
    allowed_faces: tuple[int, ...]
    allowed_directions: tuple[int, ...]
    publish: PublishRule
    absorb: AbsorbRule
    response: ResponseRule
    magnitude_encoding: str
    encoding_validator: EncodingValidator
    source_rule: str
    combination_rule: str
    decay_rule: str
    propagation_rule: str
    response_rule: str
    conserved_width: int
    inventory_state: InventoryRule
    inventory_packet: InventoryRule
    source_amount: SourceAmountRule
    sink_amount: SinkAmountRule
    response_unit: str = "candidate-integer-response-v1"
    direction_change_rule: str = "No direction-changing local interaction."

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("a field definition requires a name")
        for width in (self.state_width, self.packet_width, self.conserved_width):
            checked(width)
            if width < 1:
                raise ValueError("field state and packet widths must be positive")
        for codes in (self.allowed_faces, self.allowed_directions):
            if not isinstance(codes, tuple) or len(set(codes)) != len(codes):
                raise ValueError("face and direction codes require an immutable unique tuple")
            for code in codes:
                checked(code)
                if not 1 <= code <= 6:
                    raise ValueError("face and direction codes must lie in one through six")
        if not set(self.allowed_directions) <= set(self.allowed_faces):
            raise ValueError("propagation directions must be carried by allowed faces")
        for description in (
            self.magnitude_encoding,
            self.source_rule,
            self.combination_rule,
            self.decay_rule,
            self.propagation_rule,
            self.response_rule,
            self.response_unit,
            self.direction_change_rule,
        ):
            if not isinstance(description, str) or not description:
                raise ValueError("every field policy must have an explicit description")
        for rule in (
            self.publish,
            self.absorb,
            self.response,
            self.encoding_validator,
            self.inventory_state,
            self.inventory_packet,
            self.source_amount,
            self.sink_amount,
        ):
            if not callable(rule):
                raise TypeError("field rules and encoding validation must be callable")
        self.validate_state(self.zero_state)
        self.validate_packet(self.zero_packet)

    def _validate_record(self, record: FieldRecord, width: int) -> None:
        if not isinstance(record, tuple) or len(record) != width:
            raise ValueError("field record does not match its fixed schema width")
        for value in record:
            checked(value)
            if value < 1:
                raise ValueError("stored field registers must be strictly positive")
        self.encoding_validator(record)

    def validate_state(self, state: FieldRecord) -> None:
        self._validate_record(state, self.state_width)

    def validate_packet(self, packet: FieldRecord) -> None:
        self._validate_record(packet, self.packet_width)

    def validate_outgoing(self, packets: FacePackets) -> None:
        if not isinstance(packets, tuple) or len(packets) != 6:
            raise ValueError("exactly six fixed outgoing packets are required")
        for face, packet in enumerate(packets, start=1):
            self.validate_packet(packet)
            if face not in self.allowed_directions and packet != self.zero_packet:
                raise ValueError("field output uses a forbidden propagation direction")

    def validate_incoming(self, packets: FacePackets) -> None:
        if not isinstance(packets, tuple) or len(packets) != 6:
            raise ValueError("exactly six fixed incoming packets are required")
        for face, packet in enumerate(packets, start=1):
            self.validate_packet(packet)
            if face not in self.allowed_faces and packet != self.zero_packet:
                raise ValueError("field input uses a forbidden face")

    def validate_faces(self, faces: ResponseFaces) -> None:
        """Validate local response values against this definition's face support."""
        validate_response_faces(faces)
        for face, value in enumerate(faces, start=1):
            if face not in self.allowed_faces and decode_signed(value) != 0:
                raise ValueError("field response uses a forbidden face")


def validate_response_faces(faces: ResponseFaces) -> None:
    if not isinstance(faces, tuple) or len(faces) != 6:
        raise ValueError("exactly six encoded response faces are required")
    for value in faces:
        decode_signed(value)
