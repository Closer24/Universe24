"""Quantum continuation identities; all history remains in the event spacetime.

Local banks contain at most six integer origin IDs. These are conservative
causal-support references, not occupation samples or copies of quantum state.
Only the quantum owner may use shared resolution status to select an instrument.
"""

from dataclasses import dataclass

from event_universe.core.disturbance_state import Address3, bounded
from event_universe.core.event_links import EventReferences
from event_universe.core.event_space import CausalEventSpace


@dataclass(frozen=True, slots=True)
class WaveDefinition:
    name: str
    register_index: int

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name or len(self.name) > 128:
            raise ValueError("bounded nonempty wave name required")
        if bounded(self.register_index) < 0:
            raise ValueError("nonnegative wave source register required")


@dataclass(frozen=True, slots=True)
class WaveStatus:
    origin_event: int
    resolution_event: int | None = None


WaveUpdate = tuple[EventReferences, tuple[int, ...], int]


class WaveOrigins:
    """Fixed configured origins and their write-once continuation resolutions.

    The enclosing EventNetwork holds the shared event-space transaction during
    changes. Lookup reads one status; it never follows an ancestor or successor.
    Resolved cells remain as spacetime bookkeeping, while local banks prune them
    independently at their next tick. A checkpoint never changes these identities.
    """

    def __init__(
        self,
        events: CausalEventSpace,
        addresses: tuple[Address3, ...],
        heads: tuple[int, ...],
        definitions: tuple[WaveDefinition, ...],
    ) -> None:
        self.events = events
        self.addresses = addresses
        unique = tuple(dict.fromkeys(addresses))
        banks = events.bind_references(unique)
        self.banks = dict(zip(unique, banks, strict=True))
        self.names: dict[str, int] = {}
        for definition in definitions:
            address = addresses[definition.register_index]
            origin = events.append(
                tick=0,
                addresses=(address,),
                owner="quantum",
                kind="wave-origin",
                parents=(heads[definition.register_index],),
            )
            self.names[definition.name] = origin.id
            bank = self.banks[address]
            bank.replace((*bank.origins, origin.id), origin.id)
        self._origin_ids = frozenset(self.names.values())

    @property
    def states(self) -> tuple[WaveStatus, ...]:
        return tuple(self.status(origin) for origin in self.names.values())

    def status(self, origin: int) -> WaveStatus:
        if type(origin) is not int or origin not in self._origin_ids:
            raise ValueError("unknown quantum wave origin")
        event = self.events.event(origin)
        if event.owner != "quantum" or event.kind != "wave-origin":
            raise ValueError("unknown quantum wave origin")
        return WaveStatus(origin, self.events.resolution(origin))

    def relevant(self, origin: int) -> bool:
        return self.status(origin).resolution_event is None

    def tick_node(self, address: Address3) -> None:
        """One Node checks its own six slots; no remote bank is updated."""
        bank = self.banks[address]
        retained = tuple(origin for origin in bank.origins if self.relevant(origin))
        if retained != bank.origins:
            bank.replace(retained, bank.event_id)

    def local(self, address: Address3, origins: tuple[int, ...]) -> bool:
        bank = self.banks[address]
        return all(origin in bank.origins and self.relevant(origin) for origin in origins)

    def operation_live(self, origins: tuple[int, ...], indices: tuple[int, ...]) -> bool:
        return all(
            self.relevant(origin)
            and any(origin in self.banks[self.addresses[q]].origins for q in indices)
            for origin in origins
        )

    def plan(self, operations: tuple[tuple[int, tuple[int, ...]], ...]) -> tuple[WaveUpdate, ...]:
        """Validate a whole simultaneous layer against its old local banks.

        Each configured gate delivers the union of its one or two local banks.
        Separate gates never relay a new arrival through two Links in one tick.
        Zero amplitudes remain possible: these references do not measure presence.
        """
        planned: dict[Address3, tuple[tuple[int, ...], int]] = {}
        for event_id, indices in operations:
            addresses = tuple(dict.fromkeys(self.addresses[q] for q in indices))
            incoming = tuple(
                dict.fromkeys(
                    origin
                    for address in addresses
                    for origin in self.banks[address].origins
                    if self.relevant(origin)
                )
            )
            for address in addresses:
                prior = planned.get(address, ((), event_id))[0]
                combined = tuple(dict.fromkeys((*prior, *incoming)))
                if len(combined) > 6:
                    raise OverflowError("local quantum wave capacity exceeds six")
                planned[address] = (combined, event_id)
        return tuple((self.banks[a], ids, event) for a, (ids, event) in planned.items())

    def publish(self, updates: tuple[WaveUpdate, ...]) -> None:
        for bank, origins, event_id in updates:
            bank.replace(origins, event_id)

    def resolve(self, origins: tuple[int, ...], event_id: int) -> None:
        # The caller already checked every origin and committed the conditional
        # instrument under the same transaction. No Node bank is visited here.
        self.events.resolve(origins, event_id)
