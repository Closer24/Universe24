"""Terminal private-register contacts using the declared one-number pair law.

Contract: docs/PRIVATE_REGISTER_CONTACTS.md at df1de27c67dbe94cc1ac020ad4ea812bf49a78c1.
Ordinary local preparation has no access to the shared quantum owner. Only
this integration adapter resolves requests, at the actual input's due tick.
"""

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType

from ..core.disturbance_state import bounded, pack, unpack
from ..core.private_register import PrivateKey, PrivateResult, PrivateState, RegisterDatum
from ..core.private_worklist import PrivateInput
from ..fields.bonds import MAX_OPEN_BONDS, BondRegistry


@dataclass(frozen=True, slots=True)
class DetectorDefinition:
    end: int
    setting: int

    def __post_init__(self) -> None:
        if type(self.end) is not int or self.end not in (1, 2):
            raise ValueError("detector end must be one or two")
        if type(self.setting) is not int or not 0 <= self.setting < 64:
            raise ValueError("detector setting must be an integer phase from zero to 63")


@dataclass(frozen=True, slots=True)
class PairRequest:
    pair_id: int
    end: int
    setting: int

    def __post_init__(self) -> None:
        if bounded(self.pair_id) <= 0:
            raise ValueError("pair identity must be positive")
        DetectorDefinition(self.end, self.setting)


def prepare_capture(
    state: PrivateState, received: RegisterDatum, detector: DetectorDefinition
) -> PairRequest:
    """Read exactly one private state, actual datum and immutable local setting."""
    if type(state) is not PrivateState or type(received) is not RegisterDatum:
        raise ValueError("capture requires private state and one actual datum")
    if type(detector) is not DetectorDefinition:
        raise ValueError("capture requires an immutable detector definition")
    if state.codes:
        raise ValueError("a terminal detector already owns a captured token")
    values = unpack(received.codes)
    if len(values) != 2 or values[1] != detector.end:
        raise ValueError("capture token must contain pair identity and the local detector end")
    return PairRequest(values[0], values[1], detector.setting)


def captured_result(request: PairRequest, outcome: int) -> PrivateResult:
    """Retain one input token and its answer; no beam leaves a terminal capture."""
    if type(outcome) is not int or outcome not in (-1, 1):
        raise ValueError("a captured outcome must be minus one or plus one")
    return PrivateResult(PrivateState(pack((request.pair_id, request.end, outcome))), None)


@dataclass(frozen=True, slots=True)
class PairSlot:
    settings: tuple[int | None, int | None] = (None, None)
    answers: tuple[int | None, int | None] = (None, None)


class PrivatePairOwner:
    """A finite shared quantum bank; retained answers make completed replay inert."""

    def __init__(self, pair_ids: tuple[int, ...], seed: int, stream: tuple[int, ...] = ()) -> None:
        if type(pair_ids) is not tuple or not 1 <= len(pair_ids) <= MAX_OPEN_BONDS:
            raise ValueError("declare one to 4096 pair identities")
        if any(bounded(pair) <= 0 for pair in pair_ids) or len(set(pair_ids)) != len(pair_ids):
            raise ValueError("pair identities must be distinct positive bounded integers")
        if type(stream) is not tuple or len(stream) > len(pair_ids):
            raise ValueError("the finite number stream may contain at most one number per pair")
        self.registry = BondRegistry(seed, 64, stream)
        self.slots = {pair: PairSlot() for pair in pair_ids}

    def answer(self, request: PairRequest) -> int:
        if type(request) is not PairRequest or request.pair_id not in self.slots:
            raise ValueError("contact requests an undeclared pair identity")
        slot = self.slots[request.pair_id]
        index = request.end - 1
        answer = slot.answers[index]
        if answer is not None:
            if slot.settings[index] != request.setting:
                raise ValueError("a completed endpoint cannot change its detector setting")
            return answer
        if (
            slot.answers == (None, None)
            and self.registry.stream
            and self.registry.consumed >= len(self.registry.stream)
        ):
            raise OverflowError("the external bond stream is exhausted")
        answer = self.registry.draw(request.pair_id, request.setting, request.end)
        settings = list(slot.settings)
        answers = list(slot.answers)
        settings[index], answers[index] = request.setting, answer
        self.slots[request.pair_id] = PairSlot((settings[0], settings[1]), (answers[0], answers[1]))
        return answer

    def canonical_state(self) -> tuple[object, ...]:
        registry = self.registry
        return (
            registry.seed,
            registry.phase_steps,
            registry.stream,
            registry.consumed,
            registry.questions,
            registry.numbers,
            registry.released,
            tuple(sorted(registry.open.items())),
            tuple(sorted(self.slots.items())),
        )


@dataclass(frozen=True, slots=True)
class CaptureRecord:
    tick: int
    key: PrivateKey
    pair_id: int
    end: int
    setting: int
    outcome: int


@dataclass(frozen=True, slots=True)
class PreparedCaptures:
    results: Mapping[PrivateKey, PrivateResult]
    owner: PrivateContacts
    previous: tuple[object, ...]
    staged: PrivatePairOwner
    records: tuple[CaptureRecord, ...]

    def commit(self) -> None:
        if self.owner.canonical_state() != self.previous:
            raise ValueError("the contact owner changed after preparation")
        self.owner.quantum = self.staged
        self.owner.records.extend(self.records)


class PrivateContacts:
    """Host receipt adapter; the ordinary private rule never receives this owner."""

    def __init__(
        self,
        bindings: tuple[tuple[PrivateKey, DetectorDefinition], ...],
        pair_ids: tuple[int, ...],
        *,
        seed: int,
        stream: tuple[int, ...] = (),
    ) -> None:
        if type(bindings) is not tuple or not 1 <= len(bindings) <= 2 * MAX_OPEN_BONDS:
            raise ValueError("declare a bounded nonempty set of detector bindings")
        if any(
            type(key) is not PrivateKey or type(rule) is not DetectorDefinition for key, rule in bindings
        ):
            raise ValueError("each detector binds a private key and immutable local definition")
        if len({key for key, _ in bindings}) != len(bindings):
            raise ValueError("detector Register bindings must be unique")
        self.bindings: Mapping[PrivateKey, DetectorDefinition] = MappingProxyType(dict(bindings))
        self.quantum = PrivatePairOwner(pair_ids, seed, stream)
        self.records: list[CaptureRecord] = []

    def prepare(self, tick: int, inputs: tuple[PrivateInput, ...]) -> PreparedCaptures:
        bounded(tick)
        if tick < 0:
            raise ValueError("contact tick must be nonnegative")
        pending = []
        for local in inputs:
            detector = self.bindings.get(local.key)
            if detector is not None:
                pending.append((local.key, prepare_capture(local.state, local.datum, detector)))
        # All private requests validate before any shared draw; all shared changes
        # remain staged until the scheduler has validated every physical result.
        previous = self.canonical_state()
        staged = deepcopy(self.quantum) if pending else self.quantum
        results = {}
        records = []
        seen = set()
        for key, request in pending:
            identity = (request.pair_id, request.end)
            if (
                identity in seen
                or staged.slots.get(request.pair_id, PairSlot()).answers[request.end - 1] is not None
            ):
                raise ValueError("a pair endpoint already has a terminal capture owner")
            seen.add(identity)
            outcome = staged.answer(request)
            results[key] = captured_result(request, outcome)
            records.append(
                CaptureRecord(tick, key, request.pair_id, request.end, request.setting, outcome)
            )
        return PreparedCaptures(MappingProxyType(results), self, previous, staged, tuple(records))

    def canonical_state(self) -> tuple[object, ...]:
        return self.quantum.canonical_state(), tuple(self.records)

    def report(self) -> dict[str, int]:
        registry = self.quantum.registry
        return {
            "oracle_calls": len(self.records),
            "model_oracle_operations": len(self.records),
            "additional_model_ticks": 0,
            "numbers": registry.numbers,
            "answered_endpoints": len(self.records),
            "completed_pairs": registry.released,
            "open_pairs": len(registry.open),
            "declared_pair_slots": len(self.quantum.slots),
        }
