"""Conservative scalar and octant definitions for one positive-record field bank.

These are explicit equal-bundle redistribution laws with retained remainders.
Historical potential and rotating-leftover rules remain separate. No gravity,
isotropy or complete causal/self-force proof follows from flux conservation.
"""

from dataclasses import dataclass
from typing import cast

from event_universe.core.state import Neighbors, Vector, checked, checked_work
from event_universe.fields.conservation import split_ratio
from event_universe.fields.definition import (
    FacePackets,
    FieldDefinition,
    FieldRecord,
    PublishResult,
    ResponseFaces,
    validate_response_faces,
)
from event_universe.fields.encoding import (
    EncodedMagnitude,
    decode_signed,
    decode_values,
    encode_signed,
    encode_values,
)
from event_universe.fields.faces import face_imbalance
from event_universe.fields.streaming import OCTANT_SIGNS, _direction

ALL_FACES = (1, 2, 3, 4, 5, 6)
PAIR_ENCODING = "positive-magnitude/sign-code-v1"


def _values(record: FieldRecord, width: int) -> tuple[int, ...]:
    if not isinstance(record, tuple) or len(record) != width:
        raise ValueError("field input does not match its fixed schema")
    return decode_values(record)


def _local_inputs(sources: int, phase: int) -> None:
    checked(sources)
    checked(phase)
    if sources < 0 or phase < 0:
        raise ValueError("local source count and phase must be non-negative")


def _six_packets(incoming: FacePackets) -> None:
    if not isinstance(incoming, tuple) or len(incoming) != 6:
        raise ValueError("exactly six delivered packets are required")


def decode_response_faces(faces: ResponseFaces) -> Neighbors:
    """Read-only signed projection of the positive-coded face record."""
    validate_response_faces(faces)
    return cast(Neighbors, tuple(decode_signed(value) for value in faces))


def encoded_face_response(faces: ResponseFaces) -> Vector:
    """Decode only for transient shared opposite-face working arithmetic."""
    validate_response_faces(faces)
    return face_imbalance(cast(Neighbors, tuple(decode_signed(value) for value in faces)))


def _validate_nonnegative_pairs(record: FieldRecord) -> None:
    if any(value < 0 for value in decode_values(record)):
        raise ValueError("conserved flux records encode non-negative magnitudes only")


@dataclass(frozen=True, slots=True)
class _ScalarRules:
    strength: EncodedMagnitude

    def source_amount(self, sources: int, phase: int) -> tuple[int, ...]:
        _local_inputs(sources, phase)
        return (checked_work(sources * decode_signed(self.strength)),)

    def sink_amount(self, old: FieldRecord, sources: int, phase: int) -> tuple[int, ...]:
        _local_inputs(sources, phase)
        self.inventory_state(old)
        return (0,)

    def inventory_state(self, state: FieldRecord) -> tuple[int, ...]:
        value, remainder = _values(state, 4)
        if value < 0 or not 0 <= remainder < 6:
            raise ValueError("non-negative scalar flux and remainder below six required")
        return (checked_work(value + remainder),)

    def inventory_packet(self, packet: FieldRecord) -> tuple[int, ...]:
        value = _values(packet, 2)[0]
        if value < 0:
            raise ValueError("scalar flux packets must be non-negative")
        return (value,)

    def publish(self, old: FieldRecord, sources: int, phase: int) -> PublishResult:
        self.inventory_state(old)
        value, remainder = _values(old, 4)
        amount = checked_work(value + self.source_amount(sources, phase)[0])
        portions, retained = split_ratio(amount, (1, 1, 1, 1, 1, 1), remainder)
        outgoing = cast(FacePackets, tuple(encode_signed(portion) for portion in portions))
        return outgoing, encode_values((0, retained))

    def absorb(
        self, retained: FieldRecord, incoming: FacePackets, sources: int, phase: int
    ) -> tuple[FieldRecord, ResponseFaces]:
        _local_inputs(sources, phase)
        _six_packets(incoming)
        self.inventory_state(retained)
        value, remainder = _values(retained, 4)
        faces = []
        for packet in incoming:
            amount = self.inventory_packet(packet)[0]
            value = checked(checked_work(value + amount))
            faces.append(encode_signed(amount))
        return encode_values((value, remainder)), cast(ResponseFaces, tuple(faces))


def scalar_definition(
    name: str = "scalar-conserved-redistribution", *, source_strength: int = 64, denominator: int = 6
) -> FieldDefinition:
    """Conservative six-way local redistribution, replacing generic potential copying.

    This explicitly changes direction locally. The historical scalar relaxation
    model remains separate; its denominator-seven potential stencil is not flux.
    """
    checked(source_strength)
    checked(denominator)
    if source_strength < 0 or denominator != 6:
        raise ValueError("conservative scalar redistribution requires six-way denominator 6")
    rules = _ScalarRules(encode_signed(source_strength))
    return FieldDefinition(
        name=name,
        state_width=4,
        packet_width=2,
        zero_state=encode_values((0, 0)),
        zero_packet=encode_signed(0),
        allowed_faces=ALL_FACES,
        allowed_directions=ALL_FACES,
        publish=rules.publish,
        absorb=rules.absorb,
        response=encoded_face_response,
        magnitude_encoding=PAIR_ENCODING,
        encoding_validator=_validate_nonnegative_pairs,
        source_rule="Occupancy times source strength is added once at publication.",
        combination_rule="Add received non-negative flux; retain the previous division remainder.",
        decay_rule="No sink or loss; apparent dilution comes only from conservative local spreading.",
        propagation_rule="Whole equal six-way bundles; leftover units remain local for future ticks.",
        response_rule="Full source-facing imbalance; momentum exchange belongs to dynamics.",
        conserved_width=1,
        inventory_state=rules.inventory_state,
        inventory_packet=rules.inventory_packet,
        source_amount=rules.source_amount,
        sink_amount=rules.sink_amount,
        direction_change_rule="Explicit local isotropic redistribution with fixed weights (1,1,1,1,1,1).",
    )


@dataclass(frozen=True, slots=True)
class _OctantRules:
    strength: EncodedMagnitude

    def source_amount(self, sources: int, phase: int) -> tuple[int, ...]:
        _local_inputs(sources, phase)
        amount = checked_work(sources * decode_signed(self.strength))
        return (amount,) * 8

    def sink_amount(self, old: FieldRecord, sources: int, phase: int) -> tuple[int, ...]:
        _local_inputs(sources, phase)
        self.inventory_state(old)
        return (0,) * 8

    def inventory_state(self, state: FieldRecord) -> tuple[int, ...]:
        values = _values(state, 32)
        populations, remainders = values[:8], values[8:]
        if any(value < 0 for value in populations) or any(not 0 <= r < 3 for r in remainders):
            raise ValueError("non-negative octant populations and remainders below three required")
        return tuple(checked_work(p + r) for p, r in zip(populations, remainders, strict=True))

    def inventory_packet(self, packet: FieldRecord) -> tuple[int, ...]:
        values = _values(packet, 16)
        if any(value < 0 for value in values):
            raise ValueError("octant packets must be non-negative")
        return values

    def publish(self, old: FieldRecord, sources: int, phase: int) -> PublishResult:
        self.inventory_state(old)
        values = _values(old, 32)
        populations, remainders = values[:8], values[8:]
        source = self.source_amount(sources, phase)
        buckets = [[0] * 8 for _ in range(6)]
        retained = []
        for octant, (population, remainder) in enumerate(zip(populations, remainders, strict=True)):
            amount = checked_work(population + source[octant])
            portions, new_remainder = split_ratio(amount, (1, 1, 1), remainder)
            for axis, portion in enumerate(portions):
                buckets[_direction(axis, OCTANT_SIGNS[octant][axis])][octant] = portion
            retained.append(new_remainder)
        outgoing = cast(FacePackets, tuple(encode_values(tuple(bucket)) for bucket in buckets))
        return outgoing, encode_values((0,) * 8 + tuple(retained))

    def absorb(
        self, retained: FieldRecord, incoming: FacePackets, sources: int, phase: int
    ) -> tuple[FieldRecord, ResponseFaces]:
        _local_inputs(sources, phase)
        _six_packets(incoming)
        self.inventory_state(retained)
        values = _values(retained, 32)
        populations, remainders = list(values[:8]), values[8:]
        faces = []
        for packet in incoming:
            amount = 0
            for index, value in enumerate(self.inventory_packet(packet)):
                populations[index] = checked(checked_work(populations[index] + value))
                amount = checked(checked_work(amount + value))
            faces.append(encode_signed(amount))
        return encode_values(tuple(populations) + remainders), cast(ResponseFaces, tuple(faces))


def octant_definition(
    name: str = "octant-conserved-redistribution", *, source_per_octant: int = 64
) -> FieldDefinition:
    """Conserve each sign sector and emit equal three-way bundles with local carry."""
    checked(source_per_octant)
    if source_per_octant < 0:
        raise ValueError("source strength per octant must be non-negative")
    rules = _OctantRules(encode_signed(source_per_octant))
    return FieldDefinition(
        name=name,
        state_width=32,
        packet_width=16,
        zero_state=encode_values((0,) * 16),
        zero_packet=encode_values((0,) * 8),
        allowed_faces=ALL_FACES,
        allowed_directions=ALL_FACES,
        publish=rules.publish,
        absorb=rules.absorb,
        response=encoded_face_response,
        magnitude_encoding=PAIR_ENCODING,
        encoding_validator=_validate_nonnegative_pairs,
        source_rule="Occupancy adds the configured amount to each sector once at publication.",
        combination_rule="Checked independent sector sums; each face records total arrival.",
        decay_rule="No sink; every sector's outgoing plus retained amount equals its available flux.",
        propagation_rule="Whole equal three-way bundles inside each fixed octant, with eight carries.",
        response_rule="Full imbalance of six source-facing arrival totals.",
        conserved_width=8,
        inventory_state=rules.inventory_state,
        inventory_packet=rules.inventory_packet,
        source_amount=rules.source_amount,
        sink_amount=rules.sink_amount,
        direction_change_rule="Local redistribution to three fixed sign-compatible axes with weights (1,1,1).",
    )
