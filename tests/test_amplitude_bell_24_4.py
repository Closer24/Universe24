"""Bell at N = 512, 2048, 4096, 8192 and 16384 under the one click and the
wheel: the pin of docs/DERIVATIONS_BEAM.md section 24.4 (the run the law owes
before the pin is final; the Boss's order of 2026-09-21 under the model
owner's record 337, and the plateau's run of 2026-09-22 on the owner's word
through the paper's writer), on the worlds `bell_n<N>_<a>_<b>` of series L
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`bell_24_4` and `pair_n`; the register's L6 entry). The expected integers of
docs/TEST_EXPECTATIONS.md ("The amplitude law: Bell at N = 512 to 16384, the
pin of 24.4"), written before the runs; the test holds no literal of a world's
number, it derives the pin from the worlds and reads the register:

(a) the pin derived from each world file and the ladder: the world's N, its
    lamp's wheel [1, W] with W = N, the settings read off the counters'
    windows (Alice's counters on the lamp's -x side, Bob's on its +x side)
    and the labels off the lamp's `branches`; the design's joint weights on
    the half-angle tables of 2N (the generator's `joint`) and the ladder's
    rungs b_k = (2 W C_k + T) // (2 T) on the wheel W give the register's
    counts per cell (`pair_n`), widths and rungs (`bell_24_4`); every count
    within one of W x its cell's weight over the total; both marginals
    W / 2 exactly; E x W the register's;
(b) S over the CHSH quadruple of each N, from the derived counts: the
    register's S x N (1448 at N = 512, 5792 at 2048, 11584 at 4096, 23168 at
    8192, 46344 at 16384), the closed form of 24.4, S x N = 8 (c_1 + c_1') -
    4 N with c_1 the ++ count at (0, N / 8) and c_1' the ++ count at (N / 4,
    N / 8), and, as a fraction, the register's S per N: 181 / 64 exactly on
    the plateau 512 to 8192 and 5793 / 2048 at 16384, where the plateau ends;
(c) the replay of each shipped world file in-process, loaded as the runner
    loads it, bit-exact against the registered
    readings of the run (DETECTOR): one gather per record over the first W
    records by ordinal, the counts per cell, E x W and both marginals the
    register's, every gather's rungs the pinned rungs and its windows the
    world's settings; the GameBoard reading of the run (GAMEBOARD, the
    books) registered as conserved at every completed tick;
(d) S from the registered readings' E: the derived S of (b), so the run's
    S is the pinned fraction at every N.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "amplitude"
ORDER = ("++", "+-", "-+", "--")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load("amplitude_make_worlds_bell_24_4", WORLDS / "make_worlds.py")
EXPECTATIONS = json.loads((WORLDS / "expectations.json").read_text("utf-8"))
PIN = EXPECTATIONS["bell_24_4"]
NAMES = tuple(PIN["worlds"])
CIRCLES = tuple(sorted({int(PIN["worlds"][name]["N"]) for name in NAMES}))


def world_file(name: str) -> dict[str, object]:
    return json.loads((WORLDS / f"{name}.json").read_text("utf-8"))


def run_block(name: str) -> dict[str, object]:
    """The run block of the register that holds the world's readings: the
    run of 2026-09-21 (`run`, N = 512 and 4096) or the plateau's run of
    2026-09-22 (`run_2048_8192_16384`); one block per run, each with its
    own date, tree and source digest."""
    blocks = [PIN[key] for key in PIN if key.startswith("run") and name in PIN[key]["worlds"]]
    assert len(blocks) == 1, (name, len(blocks))
    return blocks[0]


def registered(path: str) -> object:
    """An entry of the register by its dotted path (`counts_under`)."""
    found: object = EXPECTATIONS
    for key in path.split("."):
        assert isinstance(found, dict)
        found = found[key]
    return found


def apparatus(world: dict[str, object]) -> tuple[int, int, tuple[int, int], list[tuple[int, int]]]:
    """N, the wheel W, the settings (a, b) and the labels, read off the
    world file: the lamp's wheel and branches, the windows of the counters
    on either side of the lamp."""
    measured = world["measured"]
    assert isinstance(measured, list)
    lamp = next(entry for entry in measured if "lamp" in entry)
    rate, wheel = lamp["lamp"]["wheel"]
    assert rate == 1
    lamp_x = lamp["position"][0]
    windows = {
        entry["position"][0] < lamp_x: entry["table"]["light"]["phase_window"]
        for entry in measured
        if entry["family"] == "counter"
    }
    labels = [(int(label), int(weight)) for label, weight in lamp["lamp"]["branches"]]
    return int(world["N"]), int(wheel), (int(windows[True]), int(windows[False])), labels  # type: ignore[call-overload]


def derived_counts(world: dict[str, object]) -> tuple[dict[str, int], dict[str, Fraction], list[int]]:
    """The design's counts per cell over the W births, the cells' widths
    W x w_k / T and the rungs, from the world's own apparatus."""
    n, wheel, (a, b), labels = apparatus(world)
    weights = GENERATOR.joint([(a, 0), (b, 0)], labels, n)
    order = GENERATOR.outcomes(2)
    counts = GENERATOR.counts_of(weights, order, wheel)
    total = sum(weights.values())
    cumulative = 0
    rungs: list[int] = []
    widths: dict[str, Fraction] = {}
    for key in order:
        cumulative += weights[key]
        rungs.append((2 * wheel * cumulative + total) // (2 * total))
        widths["".join(key)] = Fraction(wheel * weights[key], total)
    return {cell: counts.get(cell, 0) for cell in ORDER}, widths, rungs


def correlation(counts: dict[str, int]) -> int:
    return sum(value if cell[0] == cell[1] else -value for cell, value in counts.items())


def quadruple(correlations: list[int]) -> int:
    """S x N over the CHSH quadruple in the order of `chsh_labels`:
    E(a1, b1) - E(a1, b2) + E(a2, b1) + E(a2, b2)."""
    assert len(correlations) == 4
    return correlations[0] - correlations[1] + correlations[2] + correlations[3]


def names_of(n: int) -> list[str]:
    return [name for name in NAMES if int(PIN["worlds"][name]["N"]) == n]


@pytest.mark.parametrize("name", NAMES)
def test_the_pin_is_derived_from_the_world_and_the_ladder(name: str) -> None:
    """(a)."""
    world = world_file(name)
    n, wheel, (a, b), _ = apparatus(world)
    pinned = PIN["worlds"][name]
    assert (pinned["N"], pinned["W"], pinned["settings"], pinned["wheel"]) == (n, wheel, [a, b], [1, n])
    assert (pinned["births"], pinned["ticks"]) == (wheel, world["ticks"])
    counts, widths, rungs = derived_counts(world)
    assert counts == registered(pinned["counts_under"])
    assert rungs == pinned["rungs"]
    assert rungs[-1] == wheel
    for cell in ORDER:
        assert pinned["widths"][cell] == [widths[cell].numerator, widths[cell].denominator]
        assert abs(counts[cell] - widths[cell]) <= PIN["tolerance"]
    assert counts["++"] + counts["+-"] == pinned["marginal"] == wheel // 2
    assert counts["++"] + counts["-+"] == wheel // 2
    assert correlation(counts) == pinned["E"]
    fraction = Fraction(pinned["E"], wheel)
    assert pinned["E_over_W"] == [fraction.numerator, fraction.denominator]


@pytest.mark.parametrize("n", CIRCLES)
def test_s_over_the_quadruple_is_the_registered_fraction(n: int) -> None:
    """(b)."""
    names = names_of(n)
    assert [PIN["worlds"][name]["settings"] for name in names] == [
        list(pair) for pair in GENERATOR.chsh_labels(n)
    ]
    counts = [derived_counts(world_file(name))[0] for name in names]
    s = quadruple([correlation(c) for c in counts])
    assert s == PIN["S_times_N"][str(n)] == EXPECTATIONS["pair_n"][str(n)]["S"]
    # The closed form of 24.4: S x N = 8 (c_1 + c_1') - 4 N.
    assert s == 8 * (counts[0]["++"] + counts[2]["++"]) - 4 * n == PIN["S_times_N_closed_form"][str(n)]
    assert Fraction(s, n) == Fraction(*PIN["S"][str(n)])


def replay(name: str) -> NatureBeamSimulation:
    """The shipped world file as the runner reads it (its families resolved
    through `load_world`), stepped for its own intervals."""
    path = WORLDS / f"{name}.json"
    world = load_world(path.read_bytes(), base_dir=path.parent).world
    simulation = NatureBeamSimulation(world)
    for _ in range(world.ticks):
        simulation.step()
    return simulation


def ordinal(gather: dict[str, object]) -> int:
    return int(gather["record"]) & 0xFFFFFFFF  # type: ignore[call-overload]


def outcome(gather: dict[str, object]) -> str:
    return "".join(str(factor[2]) for factor in gather["chosen"])  # type: ignore[union-attr]


@pytest.mark.parametrize("name", NAMES)
def test_the_replay_is_bit_exact_against_the_registered_readings(name: str) -> None:
    """(c)."""
    world = world_file(name)
    _, wheel, (a, b), _ = apparatus(world)
    pinned = PIN["worlds"][name]
    run = run_block(name)["worlds"][name]
    detector = run["readings"]["DETECTOR"]
    assert run["readings"]["GAMEBOARD"]["conserved_at_every_completed_tick"] is True
    simulation = replay(name)
    assert simulation.layer is not None
    # The first W records by ordinal, the low 32 bits of the record's identity
    # (the lamp's number x 2^32 + the birth's ordinal, BEAM_LAW note 37); the
    # lamp's clock stalls as the births spend its content, so a birth is not
    # one per tick and `born`, the birth tick, is not the ordinal.
    gathers = [g for g in simulation.layer.gathers if ordinal(g) <= wheel]
    assert len(gathers) == wheel == detector["gathered_of_W"]
    assert len({g["record"] for g in gathers}) == wheel
    counts = Counter(outcome(g) for g in gathers)
    assert {cell: counts.get(cell, 0) for cell in ORDER} == detector["counts"]
    assert detector["counts"] == registered(pinned["counts_under"])
    assert correlation(dict(counts)) == detector["E"] == pinned["E"]
    plus = [sum(1 for g in gathers if g["chosen"][arm][2] == "+") for arm in (0, 1)]  # type: ignore[index]
    assert plus == [detector["alice_plus"], detector["bob_plus"]] == [wheel // 2, wheel // 2]
    assert {tuple(cell[1] for cell in g["cells"]) for g in gathers} == {tuple(pinned["rungs"])}  # type: ignore[union-attr]
    windows = {tuple((w[0], w[1], w[2]) for w in g["windows"]) for g in gathers}  # type: ignore[union-attr]
    (alice, bob) = next(iter(windows))
    assert len(windows) == 1 and (alice[1], bob[1]) == (a, b) and (alice[2], bob[2]) == (0, 0)


@pytest.mark.parametrize("n", CIRCLES)
def test_the_runs_s_is_the_derived_s(n: int) -> None:
    """(d)."""
    names = names_of(n)
    measured = quadruple(
        [run_block(name)["worlds"][name]["readings"]["DETECTOR"]["E"] for name in names]
    )
    derived = quadruple([correlation(derived_counts(world_file(name))[0]) for name in names])
    assert measured == derived == PIN["S_times_N"][str(n)]
    assert Fraction(measured, n) == Fraction(*PIN["S"][str(n)])
