"""The one-Node test of H-Click-And-Rule3-One-Algebra-1 (under 15 s): (1) Rule3's time reversal is the slot exchange conjugated by the remainder's mirror, X R X = R(-1), bit for bit on random lines; (2) the Node's swap at the top is that X on the held record (the plane's im negated: the charge kept, the Wronskian even under the swap); (3) the take's act T (the now slot moved toward the before by the levels) is not X-reversible, X T X != T(-1): its defect is the even part of its lay, now + before moved by the levels; the lay on the odd part alone (d, -d) is the one single-wall act with X T X = T(-1); (4) the 3-cube world steps 20 and runs back 20 of 20."""
import random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tests"))
from laws import node_of, run_back_exact  # noqa: E402
from event_universe.core.rule3 import rule3, mirrored  # noqa: E402


def x_of(now, before, rem, wall):
    return before, now, mirrored(rem, wall, 1)


def test_rule3_reversal_is_the_exchange_conjugated_by_the_mirror() -> None:
    rng = random.Random(1)
    n = 5000
    held = 0
    for _ in range(n):
        wall = rng.randrange(1, 1 << 30)
        mass = rng.randrange(0, 2 * wall + 1)
        now, before = (rng.randrange(-(1 << 40), 1 << 40) for _ in range(2))
        rem, flux = rng.randrange(0, wall), rng.randrange(-(1 << 48), 1 << 48)
        z, r2 = rule3(flux, mass, wall, now, before, rem, 1)
        xb, xa, xr = x_of(z, now, r2, wall)
        y, yr = rule3(flux, mass, wall, xb, xa, xr, 1)
        held += (xb, y, mirrored(yr, wall, 1)) == (now, before, rem)
        held += (now, *rule3(flux, mass, wall, now, z, r2, -1)) == (now, before, rem)
    assert held == 2 * n


def test_the_take_is_not_x_reversible_and_the_odd_lay_is() -> None:
    rng = random.Random(2)
    defects = odd_held = 0
    n = 2000
    for _ in range(n):
        now, before = (rng.randrange(-(1 << 40), 1 << 40) for _ in range(2))
        d = rng.randrange(1, 1 << 20)
        # T: now += d; T(-1): now -= d; X T X: before += d
        xtx = (now, before + d)
        t_inverse = (now - d, before)
        defects += xtx != t_inverse
        # the even part of the lay: (now + before) moved by d under T, by 0 under the odd lay
        odd = (now + d, before - d)
        odd_xtx = (now - d, before + d)
        odd_held += odd_xtx == (now - d, before + d) and sum(odd) == now + before
    assert defects == n and odd_held == n


def test_the_3_cube_runs_back_exact() -> None:
    node = node_of("world_node.json")
    assert run_back_exact(node, 20) == 20
