"""The recoil's wall L, the least common multiple of a world's declared wavelengths, stays below 2^63 and divides their product; a world whose L reaches the width is refused by name."""

from __future__ import annotations

import math

import pytest

from event_universe.core.integer import MAX_WORK_INT


def declared_wavelengths(steps: int, clocks: list[tuple[int, int]]) -> list[int]:
    """Each family's wavelength 2 N q / p in Links, whole or refused by name."""
    found = []
    for p, q in clocks:
        if p < 1 or q < 1 or (2 * steps * q) % p:
            raise ValueError(f"the clock [{p}, {q}] on N = {steps} gives no whole wavelength 2 N q / p")
        found.append(2 * steps * q // p)
    return found


def recoil_wall(wavelengths: list[int]) -> int:
    """L, the least common multiple of the declared wavelengths (1 where none is declared), refused by name at or beyond the width."""
    wall = math.lcm(*wavelengths) if wavelengths else 1
    if wall > MAX_WORK_INT:
        raise ValueError(
            f"the recoil's wall L = {wall}, the least common multiple of the wavelengths {wavelengths}, "
            f"reaches the width {MAX_WORK_INT}: the world is refused"
        )
    return wall


def test_the_wall_divides_the_product_and_the_width_refuses_by_name():
    waves = declared_wavelengths(1024, [(512, 1), (256, 3), (128, 5)])
    assert waves == [4, 24, 80]
    assert recoil_wall(waves) == 240 and math.prod(waves) % recoil_wall(waves) == 0
    assert recoil_wall([]) == 1
    with pytest.raises(ValueError, match="no whole wavelength"):
        declared_wavelengths(1024, [(3, 1)])
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    with pytest.raises(ValueError, match="reaches the width"):
        recoil_wall(primes)
    assert recoil_wall(primes[:12]) < MAX_WORK_INT
