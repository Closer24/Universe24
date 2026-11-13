"""Seven-channel static Z4 background and two-path interference control.

This is a source-only research construction, not a Maxwell or quantum model.
Two matter registers evolve by ``b_next = H_U b - a``. Four retained link
registers remain stationary on the explicitly prepared ``a == b`` domain.
A neutral, one-way reader records the previous matter intensity as its Rule3
quotient. No link field dynamics, conserved matter norm or physical detector
is inferred from those identities.

``U_k(x)`` transports a field at ``x + e_k`` back to ``x``. A local,
time-independent Z4 transformation is ``psi_x -> i**q_x psi_x`` and
``U_k(x) -> i**(q_x-q_(x+e_k)) U_k(x)``. Signed permutations act on complete
registers: a negative component sends ``(a,b,r) -> (-a,-b,5-r)``.
Arbitrary time-dependent local phase changes are outside this control.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from validation.padding import sector_state
from universe24.core import State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO, lattice
from universe24.core.tensor import TensorBuilder


NAMES = (
    "gauge_loop.matter_re", "gauge_loop.matter_im",
    "gauge_loop.link_x_re", "gauge_loop.link_x_im",
    "gauge_loop.link_y_re", "gauge_loop.link_y_im",
    "gauge_loop.intensity_reader",
)
G = len(NAMES)
PHI, CHI = 0, 1
LINK_ROWS = {0: (2, 3), 1: (4, 5)}
RECEIVER = 6
UNITS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def build_tensor() -> Tensor:
    """One fixed, b-only, integer tensor with strict single-edge support.

    All coefficients are multiples of three. Thus every legal carry is
    stationary, including nonzero carries, and the quotient is ``u // 3``.
    The complete Engine inverse still recovers both histories and carries.
    """
    builder = TensorBuilder()
    for row, name in enumerate(NAMES):
        axis = 0 if row in LINK_ROWS[0] else 1 if row in LINK_ROWS[1] else None
        builder.gear(name, label="audit" if row == RECEIVER else "official", link=axis)

    def term(target: int, coefficient: int, *factors: tuple[int, tuple[int, int, int]]) -> None:
        builder.term(NAMES[target], coefficient,
                     *((NAMES[row], offset, "b") for row, offset in factors))

    for axis, (real, imag) in LINK_ROWS.items():
        forward, backward = DIRECTIONS[2 * axis:2 * axis + 2]
        # U(x) psi(x+e): the stored link transports the neighbor to x.
        term(PHI, 3, (real, ZERO), (PHI, forward))
        term(PHI, -3, (imag, ZERO), (CHI, forward))
        term(CHI, 3, (real, ZERO), (CHI, forward))
        term(CHI, 3, (imag, ZERO), (PHI, forward))
        # U(x-e)^* psi(x-e): reverse orientation uses the conjugate.
        term(PHI, 3, (real, backward), (PHI, backward))
        term(PHI, 3, (imag, backward), (CHI, backward))
        term(CHI, 3, (real, backward), (CHI, backward))
        term(CHI, -3, (imag, backward), (PHI, backward))
        term(real, 6, (real, ZERO))
        term(imag, 6, (imag, ZERO))
    for matter in (PHI, CHI):
        term(RECEIVER, 3, (matter, ZERO), (matter, ZERO))
    return builder.build(strict_support=True)


def _integer(value: object, name: str) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    return int(value)


def _check_state(state: State) -> None:
    if not isinstance(state, State):
        raise ValueError(f"expected a complete {G}-channel State")
    state = sector_state(state, G)
    count = lattice(state.L).N
    # State's constructor checks exact integers, but its arrays are mutable.
    # Validate again before any int conversion can conceal caller corruption.
    for name in ("a", "b", "r"):
        bank = getattr(state, name)
        if not isinstance(bank, np.ndarray) or bank.shape != (G, count):
            raise ValueError(f"{name} must have shape ({G}, {count})")
        if bank.dtype.kind in "iu":
            if name == "r" and (int(bank.min()) < 0 or int(bank.max()) >= 6):
                raise ValueError("every carry must lie in 0..5")
            continue
        for value in bank.flat:
            integer = _integer(value, f"{name} register")
            if name == "r" and not 0 <= integer < 6:
                raise ValueError("every carry must lie in 0..5")


def _node(state: State, node: int) -> int:
    node = _integer(node, "node")
    if not 0 <= node < state.N:
        raise ValueError("node index outside the cube")
    return node


def validate_static_domain(state: State) -> None:
    """Reject nonunit or moving links; matter/reader histories are arbitrary.

    This invariant preparation domain has integer Gaussian-unit links, both
    histories equal, and legal carries. It is not a claim about generic seeds.
    """
    _check_state(state)
    for real, imag in LINK_ROWS.values():
        for node in range(state.N):
            if any(int(state.a[row, node]) != int(state.b[row, node]) for row in (real, imag)):
                raise ValueError("static links require equal a and b histories")
            pair = (int(state.b[real, node]), int(state.b[imag, node]))
            if pair not in UNITS:
                raise ValueError("every link must be a Gaussian unit")


def prepare_two_path(flux: int = 1, L: int = 5, amplitude: int = 1,
                     carry_offset: int = 0) -> State:
    """Origin impulse and one changed y link, giving W(0)=flux.

    For L>=5 and flux=+/-1, two updates give matter amplitude
    ``amplitude * (1 + flux)`` at (1,1,0), hence intensities 4*amplitude**2
    and zero. The reader records that intensity on the third update.
    On a periodic board the changed edge also changes an adjacent plaquette;
    this preparation does not claim a single isolated nonzero flux.
    """
    flux, L = _integer(flux, "flux"), _integer(L, "L")
    amplitude = _integer(amplitude, "amplitude")
    carry_offset = _integer(carry_offset, "carry_offset")
    if flux not in (-1, 1):
        raise ValueError("two-path flux must be +1 or -1")
    if L < 5:
        raise ValueError("the two-path fixture requires L >= 5")
    lat = lattice(L)
    a = np.zeros((G, lat.N), dtype=object)
    b = np.zeros((G, lat.N), dtype=object)
    for real, _imag in LINK_ROWS.values():
        a[real, :] = 1
        b[real, :] = 1
    changed = lat.index(1, 0, 0)
    a[LINK_ROWS[1][0], changed] = flux
    b[LINK_ROWS[1][0], changed] = flux
    b[PHI, lat.index(0, 0, 0)] = amplitude
    r = np.array([[(row * lat.N + node + carry_offset) % 6 for node in range(lat.N)]
                  for row in range(G)], dtype=object)
    state = State(L, a, b, r)
    validate_static_domain(state)
    return state


def _phase_exponents(phases: Sequence[int], count: int) -> tuple[int, ...]:
    if len(phases) != count:
        raise ValueError(f"expected {count} local phase exponents")
    result = tuple(_integer(value, "phase exponent") for value in phases)
    if any(not 0 <= value < 4 for value in result):
        raise ValueError("local phase exponents must lie in 0..3")
    return result


def gauge_transform(state: State, phases: Sequence[int]) -> State:
    """Apply a time-independent local Z4 action to every complete register.

    This is a bijection, including signed components with nonzero carries.
    The neutral reader is unchanged. It transforms arbitrary complete states;
    unit and stationary links additionally remain in the static domain.
    """
    _check_state(state)
    phases = _phase_exponents(phases, state.N)
    a, b, r = (bank.astype(object, copy=True) for bank in (state.a, state.b, state.r))
    # Destination (real, imag) gets these signed source components.
    rotations = (((0, 1), (1, 1)), ((1, -1), (0, 1)),
                 ((0, -1), (1, -1)), ((1, 1), (0, -1)))

    def rotate(rows: tuple[int, int], node: int, exponent: int) -> None:
        for destination, (source, sign) in enumerate(rotations[exponent % 4]):
            target, original = rows[destination], rows[source]
            a[target, node] = sign * int(state.a[original, node])
            b[target, node] = sign * int(state.b[original, node])
            carry = int(state.r[original, node])
            r[target, node] = carry if sign == 1 else 5 - carry

    for node, phase in enumerate(phases):
        rotate((PHI, CHI), node, phase)
        for axis, rows in LINK_ROWS.items():
            endpoint = state.lattice.neighbour(node, 2 * axis)
            rotate(rows, node, phase - phases[endpoint])
    return State(state.L, a, b, r)


def inverse_gauge_transform(state: State, phases: Sequence[int]) -> State:
    """Exact inverse of ``gauge_transform`` for the same supplied exponents."""
    exponents = _phase_exponents(phases, state.N)
    return gauge_transform(state, tuple((-phase) % 4 for phase in exponents))


def multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Exact multiplication of integer complex pairs."""
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def _link(state: State, node: int, axis: int) -> tuple[int, int]:
    real, imag = LINK_ROWS[axis]
    return int(state.b[real, node]), int(state.b[imag, node])


def plaquette(state: State, node: int = 0) -> tuple[int, int]:
    """Passive xy-loop product Ux(x) Uy(x+ex) Ux(x+ey)^* Uy(x)^*.

    Reading a loop is an offline observable. The tensor never reads this
    multi-edge expression and it never feeds the evolution.
    """
    _check_state(state)
    node = _node(state, node)
    x, y = state.lattice.neighbour(node, 0), state.lattice.neighbour(node, 2)
    product = (1, 0)
    for pair, adjoint in ((_link(state, node, 0), False), (_link(state, x, 1), False),
                          (_link(state, y, 0), True), (_link(state, node, 1), True)):
        product = multiply(product, (pair[0], -pair[1]) if adjoint else pair)
    return product


def intensity(state: State, node: int) -> int:
    """Passive integer norm of the current matter amplitude, not a probability."""
    _check_state(state)
    node = _node(state, node)
    return int(state.b[PHI, node]) ** 2 + int(state.b[CHI, node]) ** 2


def receiver_quotient(before: State, after: State, node: int) -> int:
    """Read the neutral receiver quotient from a declared transition pair.

    Its equality to ``intensity(before,node)`` is an independent check; this
    helper does not certify that its arguments form an Engine transition.
    """
    _check_state(before)
    _check_state(after)
    if before.L != after.L:
        raise ValueError("receiver snapshots must have the same lattice")
    node = _node(before, node)
    return int(after.b[RECEIVER, node]) + int(before.a[RECEIVER, node])
