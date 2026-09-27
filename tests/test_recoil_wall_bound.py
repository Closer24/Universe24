"""The recoil's wall L, the least common multiple of a world's declared wavelengths, stays below 2^63 in every shipped world and divides their product; a world whose L reaches the width is refused by name."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from event_universe.core.integer import MAX_WORK_INT
from event_universe.world_files import input_digest, parse_world_document, world_files

EVENTS = Path(__file__).resolve().parents[1] / "examples" / "events"
NOT_WORLDS = {"universe.json", "expectations.json", "pins.json", "engine_start.json"}


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


def clocks_of(world) -> list[tuple[int, int]]:
    """The clocks [p, q] that enter L: the given families' rows and the emitters' own (the recoil's row; #1295)."""
    givers = [e.block.emitter for e in world.measured if e.block and e.block.emitter]
    found = [(int(g.clock[0]), int(g.clock[1])) for g in givers]
    for index, family in enumerate(world.families):
        if family.phase_per_age is not None and any(g.family == index for g in givers):
            found.append((int(family.phase_per_age[0]), int(family.phase_per_age[1])))
    return found


def shipped_worlds():
    for path in sorted(EVENTS.rglob("*.json")):
        if path.name in NOT_WORLDS:
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        try:
            yield path, parse_world_document(document, world_files(document), input_digest(document))
        except ValueError:
            continue  # a file that is no world of the engine (a reading, an older format)


def test_every_shipped_world_keeps_the_wall_below_the_width():
    """Twenty worlds keep the wall; the two point-emitter worlds at N = 64 give the charge row's clock [512, 1] with no whole wavelength (lambda_q = 1/4), the law's load refusal (the recoil's row: L over the given families' clocks; measured once)."""
    seen, refused = 0, 0
    for path, world in shipped_worlds():
        if any((2 * int(world.phase_steps) * q) % p for p, q in clocks_of(world)):
            refused += 1  # no whole wavelength: the law's load refusal
            continue
        wavelengths = declared_wavelengths(int(world.phase_steps), clocks_of(world))
        wall = recoil_wall(wavelengths)
        assert 1 <= wall <= MAX_WORK_INT, path
        assert wall <= math.prod(wavelengths or [1])
        seen += 1
    assert seen == 20 and refused == 2


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
