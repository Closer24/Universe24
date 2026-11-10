"""The 48 reference channels (+++) as a layer block, Q-scaled into the common divisor D = 6Q."""
from __future__ import annotations

from ..core.tensor import Block, reference_block


def build_reference(*, Q: int = 1, body_signs=(1, 1, 1), name: str | None = "ref", label: str = "official") -> Block:
    """The 48-gear L0 block inside ONE.

    Parameters
    ----------
    Q : divisor scale; D = 6Q is the ONE divisor of the composed system. Entries are x Q (Q-scaling theorem).
    body_signs : the three body-axis signs of universe24.algebra.coupling.Coupling (default +++).
    name : namespace; gear names become "<name>.R00" ... "<name>.R47" (gear Rg carries the 2O label g).
    label : readout label of these gears (official by default).
    Vacuum: every channel at (0, 0, 2Q), the Q-scaled L0 vacuum.
    """
    core = reference_block(Q, body_signs, prefix="R", label=label)
    return Block(core.gears, core.terms, name=name, vacuum={g.name: 2 * Q for g in core.gears},
                 params={"Q": Q, "body_signs": tuple(body_signs), "label": label},
                 doc="48 reference channels, ports/weights from universe24.algebra.coupling, entries x Q", Q=Q)
