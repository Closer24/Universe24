"""Usable scalar and octant definitions for the same positive-record field bank.

These adapters retain the existing local equations. A bank's delivery schedule
is a separate candidate contract; no gravity or complete causal proof follows.
"""

from dataclasses import dataclass
from typing import cast

from event_universe.core.state import Neighbors, Vector, checked, checked_work
from event_universe.fields.definition import (
    FacePackets,
    FieldDefinition,
    FieldRecord,
    ResponseFaces,
    validate_magnitude_pairs,
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
from event_universe.fields.policies import nonnegative_sample, uniform_source
from event_universe.fields.scalar import ScalarField, ScalarSample
from event_universe.fields.streaming import CausalOctantStream, Octants

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
        raise ValueError("octant records encode non-negative populations only")


@dataclass(frozen=True, slots=True)
class _ScalarRules:
    strength: EncodedMagnitude
    denominator: int

    def publish(self, old: FieldRecord, sources: int, phase: int) -> FacePackets:
        _local_inputs(sources, phase)
        phi, _ = _values(old, 4)
        packet = encode_signed(phi)
        return packet, packet, packet, packet, packet, packet

    def absorb(
        self, old: FieldRecord, incoming: FacePackets, sources: int, phase: int
    ) -> tuple[FieldRecord, ResponseFaces]:
        _local_inputs(sources, phase)
        _six_packets(incoming)
        phi, remainder = _values(old, 4)
        neighbors = cast(Neighbors, tuple(_values(packet, 2)[0] for packet in incoming))
        law = ScalarField(neighbor_weights=(1, 1, 1, 1, 1, 1), self_weight=0)
        sample = law.advance(
            ScalarSample(phi, remainder),
            neighbors,
            source=uniform_source(sources, decode_signed(self.strength)),
            denominator=self.denominator,
        )
        result = nonnegative_sample(sample)
        faces = cast(ResponseFaces, tuple(encode_signed(value) for value in neighbors))
        return encode_values((result.value, result.remainder)), faces


def scalar_definition(
    name: str = "scalar-relaxation", *, source_strength: int = 64, denominator: int = 7
) -> FieldDefinition:
    """Existing six-neighbor scalar relaxation with an explicit integer residue."""
    checked(source_strength)
    checked(denominator)
    if source_strength < 0 or denominator < 1:
        raise ValueError("non-negative source strength and positive denominator required")
    rules = _ScalarRules(encode_signed(source_strength), denominator)
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
        encoding_validator=validate_magnitude_pairs,
        source_rule="Occupancy times source strength enters absorption once per field update.",
        combination_rule="Six scalar inputs plus source and old division remainder.",
        decay_rule="Division by the explicit denominator; no additional decay operation.",
        propagation_rule="Publish the old scalar equally on all six outgoing faces.",
        response_rule="Full source-facing imbalance; momentum exchange belongs to dynamics.",
    )


@dataclass(frozen=True, slots=True)
class _OctantRules:
    strength: EncodedMagnitude

    def publish(self, old: FieldRecord, sources: int, phase: int) -> FacePackets:
        _local_inputs(sources, phase)
        populations = cast(Octants, _values(old, 16))
        outgoing = CausalOctantStream().emit(populations, sources, decode_signed(self.strength), phase)
        return cast(FacePackets, tuple(encode_values(packet) for packet in outgoing))

    def absorb(
        self, old: FieldRecord, incoming: FacePackets, sources: int, phase: int
    ) -> tuple[FieldRecord, ResponseFaces]:
        _local_inputs(sources, phase)
        _six_packets(incoming)
        if any(value < 0 for value in _values(old, 16)):
            raise ValueError("old octant populations must be non-negative")
        populations = [0] * 8
        faces = []
        for packet in incoming:
            values = _values(packet, 16)
            if any(value < 0 for value in values):
                raise ValueError("incoming octant populations must be non-negative")
            amount = 0
            for index, value in enumerate(values):
                populations[index] = checked(checked_work(populations[index] + value))
                amount = checked(checked_work(amount + value))
            faces.append(encode_signed(amount))
        return encode_values(tuple(populations)), cast(ResponseFaces, tuple(faces))


def octant_definition(name: str = "outward-octants", *, source_per_octant: int = 64) -> FieldDefinition:
    """Existing conservative sign-sector branching, with no per-source identity."""
    checked(source_per_octant)
    if source_per_octant < 0:
        raise ValueError("source strength per octant must be non-negative")
    rules = _OctantRules(encode_signed(source_per_octant))
    empty = encode_values((0, 0, 0, 0, 0, 0, 0, 0))
    return FieldDefinition(
        name=name,
        state_width=16,
        packet_width=16,
        zero_state=empty,
        zero_packet=empty,
        allowed_faces=ALL_FACES,
        allowed_directions=ALL_FACES,
        publish=rules.publish,
        absorb=rules.absorb,
        response=encoded_face_response,
        magnitude_encoding=PAIR_ENCODING,
        encoding_validator=_validate_nonnegative_pairs,
        source_rule="Occupancy emits the configured amount into each octant at publication.",
        combination_rule="Checked addition per octant; each face records its total arrival.",
        decay_rule="No decay; every integer population is transferred conservatively.",
        propagation_rule="Three permitted cardinal directions per fixed sign sector; phase modulo three.",
        response_rule="Full imbalance of six source-facing arrival totals.",
    )
