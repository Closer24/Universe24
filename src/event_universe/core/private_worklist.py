"""Sparse and dense scheduling of one shared private Register transport law."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Literal, Protocol

from .private_reference import DenseSelector
from .private_register import (
    PRIVATE_PORT_PAIRS,
    PrivateKey,
    PrivateNode,
    PrivateResult,
    PrivateState,
    RegisterDatum,
    private_transition,
    validate_private_pairs,
)
from .private_transport import CausalTransport, PeriodicWiring


@dataclass(frozen=True, slots=True)
class PrivateInput:
    """Immutable own state and actually due datum at a host-owned contact address."""

    key: PrivateKey
    state: PrivateState
    datum: RegisterDatum

    def __post_init__(self) -> None:
        if (
            type(self.key) is not PrivateKey
            or type(self.state) is not PrivateState
            or type(self.datum) is not RegisterDatum
        ):
            raise ValueError("a private contact input requires immutable local records")


class PreparedPrivateContacts(Protocol):
    """Validated quantum-owner proposals; commit must publish one prepared stage."""

    @property
    def results(self) -> Mapping[PrivateKey, PrivateResult]: ...

    def commit(self) -> None: ...


class PrivateContacts(Protocol):
    """External contact owner; preparation never mutates its committed state."""

    def prepare(self, tick: int, inputs: tuple[PrivateInput, ...]) -> PreparedPrivateContacts: ...

    def canonical_state(self) -> tuple[object, ...]: ...


class Selector(Protocol):
    checks: int

    def select(self, due: frozenset[PrivateKey]) -> tuple[PrivateKey, ...]: ...


class SparseSelector:
    """Visit only actual received-input handles; no dormant Register scan."""

    def __init__(
        self,
        keys: Iterable[PrivateKey] | None = None,
        *,
        pairs: tuple[tuple[int, int], ...] = PRIVATE_PORT_PAIRS,
    ) -> None:
        validate_private_pairs(pairs)
        self.pairs = frozenset(pairs)
        self._known = None if keys is None else frozenset(keys)
        if self._known is not None and any(
            (key.from_port, key.to_port) not in self.pairs for key in self._known
        ):
            raise ValueError("a sparse key is not in the configured Port pairs")
        self.checks = 0

    def select(self, due: frozenset[PrivateKey]) -> tuple[PrivateKey, ...]:
        if any((key.from_port, key.to_port) not in self.pairs for key in due) or (
            self._known is not None and not due.issubset(self._known)
        ):
            raise ValueError("a due input targets an undeclared private Register")
        self.checks += len(due)
        return tuple(sorted(due))


@dataclass(frozen=True)
class TransferEvent:
    tick: int
    kind: Literal["receive", "send", "capture"]
    source: PrivateKey
    target: PrivateKey
    codes: tuple[int, ...]
    due_tick: int


class PrivateSimulation:
    """Private transport with optional prepared terminal contacts.

    Nodes only contain private units. Routing, due handles, history and global
    time belong to this host adapter and are never arguments of the local law.
    """

    def __init__(
        self,
        wiring: PeriodicWiring,
        seeds: tuple[tuple[PrivateKey, RegisterDatum], ...],
        *,
        strategy: Literal["dense", "sparse"] = "sparse",
        contacts: PrivateContacts | None = None,
    ) -> None:
        if strategy not in ("dense", "sparse"):
            raise ValueError("private execution strategy must be dense or sparse")
        self.wiring = wiring
        self.nodes = {address: PrivateNode(pairs=wiring.pairs) for address in wiring.nodes}
        self.transport = CausalTransport(wiring, seeds)
        self.selector: Selector = (
            DenseSelector(wiring.nodes, pairs=wiring.pairs)
            if strategy == "dense"
            else SparseSelector(wiring.channels, pairs=wiring.pairs)
        )
        self.contacts = contacts
        self.tick = 0
        self.transitions = 0
        self.events: list[TransferEvent] = []

    def step(self) -> None:
        preview = self.transport.preview_inputs(self.tick)
        due = frozenset(preview)
        old_checks = self.selector.checks
        try:
            selected = self.selector.select(due)
            new_checks = self.selector.checks
        finally:
            self.selector.checks = old_checks
        if len(selected) != len(due) or frozenset(selected) != due:
            raise ValueError("scheduler must dispatch exactly the actual due Register cohort")
        records = tuple(
            PrivateInput(key, self.nodes[key.node].unit(key.from_port, key.to_port).state, preview[key])
            for key in selected
        )
        proposals = {
            item.key: private_transition(
                item.state,
                item.datum,
                self.nodes[item.key.node].unit(item.key.from_port, item.key.to_port).law,
            )
            for item in records
        }
        prepared = None if self.contacts is None else self.contacts.prepare(self.tick, records)
        if self.contacts is not None and prepared is None:
            raise ValueError("contacts must supply a prepared result mapping and commit")
        if prepared is not None:
            if not isinstance(prepared.results, Mapping) or not callable(prepared.commit):
                raise ValueError("contacts must supply a prepared result mapping and commit")
            overrides = dict(prepared.results)
            if any(type(key) is not PrivateKey for key in overrides) or not overrides.keys() <= due:
                raise ValueError("contact overrides must belong to the selected own Registers")
            proposals.update(overrides)
        for item in records:
            self._validate_result(item, proposals[item.key])
        if prepared is not None:
            prepared.commit()
        receipts = self.transport.receive(self.tick)
        for source, packet in receipts:
            self.events.append(
                TransferEvent(
                    self.tick, "receive", source, packet.target, packet.datum.codes, packet.due_tick
                )
            )
        for item in records:
            key = item.key
            result = proposals[key]
            self.nodes[key.node].unit(key.from_port, key.to_port).state = result.state
            if result.output is None:
                self.transport.retain(key, item.datum)
                self.events.append(
                    TransferEvent(self.tick, "capture", key, key, result.state.codes, self.tick)
                )
            else:
                packet = self.transport.emit(key, result.output, self.tick)
                self.events.append(
                    TransferEvent(
                        self.tick, "send", key, packet.target, result.output.codes, packet.due_tick
                    )
                )
            self.transitions += 1
        self.selector.checks = new_checks
        self.tick += 1

    @staticmethod
    def _validate_result(item: PrivateInput, result: PrivateResult) -> None:
        if type(result) is not PrivateResult:
            raise ValueError("a contact result must be an immutable PrivateResult")
        if result.output is not None:
            if result.output is not item.datum:
                raise ValueError("identity transport requires the actual received datum owner")
            if result.state != item.state:
                raise ValueError("identity transport must preserve its private state")
        elif (
            item.state.codes
            or len(result.state.codes) != len(item.datum.codes) + 1
            or result.state.codes[:-1] != item.datum.codes
        ):
            raise ValueError("capture must retain its actual input and one outcome in empty own state")

    def work_report(self) -> dict[str, int]:
        return {
            "register_checks": self.selector.checks,
            "nonempty_transitions": self.transitions,
            **self.transport.queue_report(),
        }

    def canonical_state(self) -> tuple[object, ...]:
        """Read all private owners, causal deadlines and events for comparison.

        This complete observation may scan the world. It never runs within the
        measured step or supplies input to a private physical calculation.
        """
        private_states = tuple(
            (PrivateKey(address, *pair), unit.state.codes)
            for address, node in sorted(self.nodes.items())
            for pair, unit in zip(node.pairs, node.units, strict=True)
        )
        inputs = tuple((key, datum.codes) for key, datum in sorted(self.transport.inputs.items()))
        channels = tuple(
            (source, packet.target, packet.datum.codes, packet.due_tick)
            for source, packet in sorted(self.transport.channels.items())
        )
        physical = self.tick, private_states, inputs, channels, tuple(self.events)
        if self.contacts is None:
            return physical
        return (*physical, self.contacts.canonical_state())
