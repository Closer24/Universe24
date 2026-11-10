"""Synchronous executor for a fixed ``VariantCoupling``.

The per-channel law is not re-implemented: ``forward`` and ``inverse`` are the
reference primitives imported from ``universe24/core/rule3.py``. This module
only routes the six signed inputs through the variant table, from one complete
old snapshot, exactly as ``universe24.core.engine.Engine`` does with the
reference table. There are no observers, callbacks, gates or runtime changes:
the coupling is immutable and chosen before ``advance`` is first called.
``rewind`` is the exact inverse, for audit and recovery only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from universe24.core.rule3 import forward, inverse
from universe24.core.state import Address, State

from .coupling import VariantCoupling


@dataclass(frozen=True, slots=True)
class VariantEngine:
    coupling: VariantCoupling

    def __post_init__(self):
        if not isinstance(self.coupling, VariantCoupling):
            raise TypeError("Expected a validated VariantCoupling")

    @property
    def label(self) -> str:
        return self.coupling.label

    def input_sums(self, state: State, component: int = 1) -> dict[Address, int]:
        """Signed six-port sums of component b (forward) or a (inverse) of one snapshot."""
        if component not in (0, 1):
            raise ValueError("component must be a or b")
        ports, weights = self.coupling.ports, self.coupling.weights
        totals = {}
        for address, triple in state.cells.items():
            value = triple[component]
            if value == 0:
                continue
            g = address[3]
            for d in range(6):
                receiver = state.cube.adjacent(address, d, ports[d][g])
                totals[receiver] = totals.get(receiver, 0) + weights[d][g] * value
        return totals

    def advance(self, state: State) -> State:
        sums = self.input_sums(state)
        cells = {}
        for address in state.cells.keys() | sums.keys():
            new = forward(state.cells.get(address, state.background), sums.get(address, 0))
            if new != state.background:
                cells[address] = new
        return State(state.cube, state.background, cells)

    def rewind(self, state: State) -> State:
        """Exact inverse for audit/reconstruction; never a forward stage."""
        sums = self.input_sums(state, component=0)
        cells = {}
        for address in state.cells.keys() | sums.keys():
            old = inverse(state.cells.get(address, state.background), sums.get(address, 0))
            if old != state.background:
                cells[address] = old
        return State(state.cube, state.background, cells)

    def evolve(self, initial: State, steps: int) -> Iterator[State]:
        if type(steps) is not int or steps < 0:
            raise ValueError("steps must be nonnegative")
        state = initial
        yield state
        for _ in range(steps):
            state = self.advance(state)
            yield state
