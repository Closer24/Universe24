"""The engine's records: the Node-clocks' state, the layout read once at load, and what a round puts out."""

from typing import NamedTuple

from tensor24.algebra.carry import Z


class State(NamedTuple):
    """Per gear its now and before slots, fine tooth and going; per Node-clock its dial, count and slots' times."""

    a: Z
    b: Z
    r: Z
    go: Z
    ph: Z
    c: Z
    tb: Z
    tn: Z


class Layout(NamedTuple):
    """The board read once: the six neighbours, each Mesh's grip, the teeth, the rates and the full rate."""

    nb: Z
    grip: Z
    w: Z
    rate: Z
    gamma: Z


class Out(NamedTuple):
    """What a round puts out: where it fired, where it ticked, and the before slot's time it replaced."""

    fire: Z
    k: Z
    tb: Z
