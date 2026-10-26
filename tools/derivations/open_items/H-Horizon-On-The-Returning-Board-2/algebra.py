"""The algebra of the frozen mark on a board alike at every Node: the frozen content at Gamma, the volume at that content, and the quanta the lay needs for it (the law's own tables, event_universe.core.paces and features.volume; no Node and no interval imported)."""

import sys

from event_universe.core import paces
from event_universe.features import volume

GAMMA = 1000
EXPONENT = 4  # the level's clause: Gamma^(d + 2) <= X p_0(a)^(d + 1) on three axes


def volume_at(gamma: int, content: int) -> int:
    """The least volume X whose level is at or above the content: Gamma^5 <= X p_0(content)^4."""
    p = paces.clock(gamma, content)
    target = gamma ** (EXPONENT + 1)
    return -(-target // p**EXPONENT)


def main() -> None:
    frozen = paces.frozen_content(GAMMA)
    x_frozen = volume_at(GAMMA, frozen)
    print(f"Gamma {GAMMA}")
    print(f"the frozen content (the Link pace rounds to 0): {frozen}")
    print(f"the clock at the frozen content: {paces.clock(GAMMA, frozen)}")
    print(f"the least volume at the frozen content: {x_frozen} ({x_frozen.bit_length()} bits)")
    print(f"the level of that volume (the reader's own): {volume.level_of(GAMMA, x_frozen)}")
    print(f"four times Gamma cubed: {4 * GAMMA**3} (the derived mark 4 Gamma^3)")
    print(f"the level of 4 Gamma^3: {volume.level_of(GAMMA, 4 * GAMMA**3)}")
    for x in (2070, 17800, 21888, 5600000):
        print(f"the level of the volume {x}: {volume.level_of(GAMMA, x)}")
    for content in (1047, 2157, 3025, 3700, frozen):
        print(f"the least volume at the content {content}: {volume_at(GAMMA, content)}")
    print(f"the ratio of the frozen volume to the volume at the content 2157: {x_frozen // volume_at(GAMMA, 2157)}")


if __name__ == "__main__":
    sys.exit(main())
