"""The engine's records: the Node-clocks' state, the layout read once at load, and what a round puts out."""

from typing import NamedTuple

from tensor24.algebra.carry import Z


class State(NamedTuple):
    """Per gear its now and before slots, fine tooth and going; per Node-clock its dial, count and now slot's time."""

    a: Z
    b: Z
    r: Z
    go: Z
    ph: Z
    c: Z
    tn: Z


class Layout(NamedTuple):
    """The board read once: the six neighbours, each Spoke's Mesh, each Mesh's grip once, the teeth, the rates and the full rate."""

    nb: Z  # (6, N): +x, -x, +y, -y, +z, -z, each the other's opposite (the load makes the relation symmetric)
    meshes: Z  # (6, N): the Mesh each Spoke holds, its two ends paired by runner/board.py; a grip its own conjugate
    grip: Z  # one grip per Mesh
    w: Z
    rate: Z  # from 0 to the full rate, so the beat's k is a bit (the load refuses a rate above it)
    gamma: Z


class Out(NamedTuple):
    """What a round puts out: where it fired, where it ticked, and the now slot's time before the round."""

    fire: Z
    k: Z
    tn: Z
