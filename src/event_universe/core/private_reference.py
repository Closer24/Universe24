"""Dense host reference for the same private units used by sparse execution."""

from collections.abc import Collection, Iterable

from .disturbance_state import Address3
from .private_register import PRIVATE_PORT_PAIRS, PrivateKey


class DenseSelector:
    """Visit all 24 units of every configured Node on every model tick.

    The due input set is frozen before selection. Checking an absent input is a
    certified identity no-op, so it need not invoke the physical kernel. Selected
    units use the same transition and channel transfer owner as sparse execution.
    Checks count host work and never change private physical state or model time.
    """

    def __init__(self, node_addresses: Iterable[Address3]) -> None:
        addresses = tuple(node_addresses)
        if len(set(addresses)) != len(addresses):
            raise ValueError("dense reference Node addresses must be unique")
        self.keys = tuple(
            PrivateKey(node, source, target)
            for node in sorted(addresses)
            for source, target in PRIVATE_PORT_PAIRS
        )
        self._known = frozenset(self.keys)
        self.checks = 0

    def select(self, due: Collection[PrivateKey]) -> tuple[PrivateKey, ...]:
        """Select existing due inputs in canonical Node/Register order."""
        ready = frozenset(due)
        if len(ready) != len(due):
            raise ValueError("a private Register has at most one due input")
        if not ready.issubset(self._known):
            raise ValueError("a due input targets an undeclared private Register")
        self.checks += len(self.keys)
        return tuple(key for key in self.keys if key in ready)
