"""The (3, 4) split at N = 32 and N = 128 under the one click and the wheel:
the power window of docs/DERIVATIONS_BEAM.md section 6.5 pinned from above
(the Boss's order of 2026-09-21 on the auditor's round 4), on the worlds
`mz_345_n32` and `mz_345_n128` of series L
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`mz_345_n`; the register's L1 entry). The expected integers of
docs/TEST_EXPECTATIONS.md ("The amplitude law: the (3, 4) split at N = 32
and 128"), written before the run; the test holds no literal of a world's
number, it derives the pin from the worlds and the engine and reads the
register:

(a) the pin derived from each world file and the engine's own tables and
    ladder: N and the lamp's wheel [1, W] with W = N; the rows at the two
    ports off the lamp's turns and the splitter's weights and turns (the
    generator's `mach_zehnder_ports`: a + b in phase at the quarter turn
    toward D1, the cancel's remainder b - a at the half turn toward D2,
    the multiplicity the birth's rows times a^2 + b^2); per u the ports'
    pointers on `phase_cosines` and `phase_sines` of N, the rungs by
    `amplitude.rungs` on the wheel and the cell of u by
    `amplitude.cell_of` give the register's counts per port, the u of
    every click at D2 (every u from the first rung up), the rungs (one
    list at every u) and the totals' spread; the first rung is the rung of
    the design's exact offers (a + b)^2 / T and (b - a)^2 / T, unmoved by
    the tables' rounding; the generator's `mach_zehnder_pin` agrees; the
    same derivation on the registered `mz_345` at N = 64 gives L1's
    registered clicks, its u to D2 and its first rungs;
(b) the power window per N from the rung (6.5: with the ports' single rows
    r = (a + b) / (b - a) against 1, a power k reads r^k against 1 and the
    cells b / (N - b) hold iff r^k / (r^k + 1) lies in [(2 b - 1) / (2 N),
    (2 b + 1) / (2 N)); the bounds of r^k exact, k's to three decimals)
    equals the register's at N = 32, 64 and 128; the intersection of the
    three with the pair's registered window is the register's, its lower
    bound N = 64's and its upper bound N = 128's; it contains 2 and
    excludes 1 and 3;
(c) the replay of each shipped world file in-process, loaded as the runner
    loads it, bit-exact against the registered readings of the run
    (DETECTOR): one gather per record over the first W records by ordinal,
    the counts per port, the u of every click at D2, every gather's rungs
    and the totals' spread the register's, and the counts over every
    gather; the GameBoard reading of the run (GAMEBOARD) registered as
    conserved at every completed tick, the replay's births, gathers and
    open records the register's and its books balanced at the end.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import NatureBeamSimulation
from event_universe.events.amplitude import cell_of, rungs
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "amplitude"
PORTS = ("D1", "D2")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load("amplitude_make_worlds_mz_345_n", WORLDS / "make_worlds.py")
EXPECTATIONS = json.loads((WORLDS / "expectations.json").read_text("utf-8"))
PIN = EXPECTATIONS["mz_345_n"]
NAMES = tuple(PIN["worlds"])


def world_file(name: str) -> dict[str, object]:
    return json.loads((WORLDS / f"{name}.json").read_text("utf-8"))


def splitter() -> tuple[int, int]:
    a, b = PIN["splitter"]
    return int(a), int(b)


def exact_rung(n: int) -> int:
    """The first rung of the design's exact offers (a + b)^2 / T and
    (b - a)^2 / T on the wheel N (DERIVATIONS_BEAM 6.5's b_1)."""
    a, b = splitter()
    total = (a + b) ** 2 + (b - a) ** 2
    return (2 * n * (a + b) ** 2 + total) // (2 * total)


def derived_pin(world: dict[str, object]) -> dict[str, object]:
    """The counts per port, the u of every click at D2, the rungs and the
    totals' spread over the W births, from the ports' rows on the engine's
    tables and the engine's ladder."""
    n, wheel, ports, multiplicity = GENERATOR.mach_zehnder_ports(world)
    cosines, sines = phase_cosines(n), phase_sines(n)
    counts = dict.fromkeys(PORTS, 0)
    to_d2: list[int] = []
    ladders: set[tuple[int, ...]] = set()
    totals: set[Fraction] = set()
    for u in range(wheel):
        weights: list[tuple[int, int]] = []
        for port in PORTS:
            x = sum(32 * amount * cosines[(phase + u) % n] for amount, phase in ports[port])
            y = sum(32 * amount * sines[(phase + u) % n] for amount, phase in ports[port])
            weights.append((x * x + y * y, multiplicity))
        ladder, total = rungs(weights, wheel)
        ladders.add(tuple(ladder))
        totals.add(Fraction(*total))
        cell = cell_of(weights, wheel, u)
        assert cell is not None
        counts[PORTS[cell]] += 1
        if PORTS[cell] == "D2":
            to_d2.append(u)
    (ladder_found,) = ladders
    return {
        "counts": counts,
        "u_to_D2": to_d2,
        "rungs": list(ladder_found),
        "distinct_totals": len(totals),
    }


@pytest.mark.parametrize("name", NAMES)
def test_the_pin_is_derived_from_the_world_and_the_engines_tables_and_ladder(name: str) -> None:
    """(a)."""
    world = world_file(name)
    pinned = PIN["worlds"][name]
    a, b = splitter()
    n, wheel, ports, multiplicity = GENERATOR.mach_zehnder_ports(world)
    assert (pinned["N"], pinned["W"], pinned["wheel"], pinned["births"]) == (n, wheel, [1, n], n)
    assert pinned["ticks"] == world["ticks"]
    # The ports' rows of a record born at u = 0: a + b in phase at the
    # quarter turn toward D1, a at the birth phase and b at the half turn
    # toward D2 (the cancel's remainder b - a), the multiplicity 2 x A.
    assert {phase for _, phase in ports["D1"]} == {n // 4}
    assert sum(amount for amount, _ in ports["D1"]) == a + b
    assert {phase: amount for amount, phase in ports["D2"]} == {0: a, n // 2: b}
    assert multiplicity == pinned["multiplicity"] == 2 * (a * a + b * b)
    assert {port: [list(row) for row in rows] for port, rows in ports.items()} == pinned["ports"]
    derived = derived_pin(world)
    for key, value in derived.items():
        assert value == pinned[key], (name, key)
    assert derived == {key: GENERATOR.mach_zehnder_pin(world)[key] for key in derived}
    assert pinned["rungs"] == [exact_rung(n), n] and pinned["rung_of_the_exact_offers"] == exact_rung(n)
    assert pinned["u_to_D2"] == list(range(exact_rung(n), n))
    assert sum(pinned["counts"].values()) == n and pinned["counts"]["D2"] == n - exact_rung(n)
    total = (a + b) ** 2 + (b - a) ** 2
    assert Fraction(PIN["offers"]["D1"]) == Fraction((a + b) ** 2, total)
    assert Fraction(PIN["offers"]["D2"]) == Fraction((b - a) ** 2, total)


def test_the_same_derivation_gives_the_registered_split_at_n_64() -> None:
    """(a), the registered `mz_345`."""
    registered = EXPECTATIONS["mach_zehnder"]["mz_345"]
    world = GENERATOR.mach_zehnder("mz_345", splitter=splitter())
    derived = derived_pin(world)
    assert derived["counts"] == registered["clicks"]
    assert derived["u_to_D2"] == [registered["pythagorean_5"]["u_to_D2"]]
    assert derived["rungs"] == registered["pythagorean_5"]["first_rungs"]
    assert derived["distinct_totals"] == EXPECTATIONS["mach_zehnder"]["totals"]["distinct"]
    assert derived == {key: GENERATOR.mach_zehnder_pin(world)[key] for key in derived}
    window = PIN["power_windows"][str(world["N"])]
    assert (window["world"], window["rung"]) == ("mz_345", derived["rungs"][0])


def window_of(n: int, rung: int) -> tuple[Fraction, Fraction]:
    """The bounds of r^k, r = (a + b) / (b - a), for the cells rung /
    (N - rung) (6.5): the first rung is b iff r^k / (r^k + 1) lies in
    [(2 b - 1) / (2 N), (2 b + 1) / (2 N))."""
    return Fraction(2 * rung - 1, 2 * n - 2 * rung + 1), Fraction(2 * rung + 1, 2 * n - 2 * rung - 1)


def test_the_power_window_per_n_and_its_intersection_are_the_registered() -> None:
    """(b)."""
    a, b = splitter()
    ratio = Fraction(PIN["ratio"])
    assert ratio == Fraction(a + b, b - a)
    lows: list[tuple[float, str]] = [(PIN["pair_power_window"][0], "the pair")]
    highs: list[tuple[float, str]] = [(PIN["pair_power_window"][1], "the pair")]
    for key, window in PIN["power_windows"].items():
        n = int(key)
        rung = exact_rung(n)
        assert window["rung"] == rung and window["cells"] == f"{rung} / {n - rung}"
        low, high = window_of(n, rung)
        assert [Fraction(bound) for bound in window["ratio_power_k_in"]] == [low, high]
        k_low, k_high = round(_log(low, ratio), 3), round(_log(high, ratio), 3)
        assert window["k_in"] == [k_low, k_high]
        assert window == {**window, **GENERATOR.power_window(n, rung, ratio)}
        lows.append((k_low, f"N = {n}"))
        highs.append((k_high, f"N = {n}"))
    low, low_from = max(lows)
    high, high_from = min(highs)
    intersection = PIN["intersection"]
    assert intersection["k_in"] == [round(low, 3), round(high, 3)]
    assert (intersection["lower_bound_from"], intersection["upper_bound_from"]) == (low_from, high_from)
    assert low < high
    for k in intersection["contains"]:
        assert low <= k < high
    for k in intersection["excludes"]:
        assert not low <= k < high
    assert intersection["contains"] == [2] and intersection["excludes"] == [1, 3]


def _log(value: Fraction, base: Fraction) -> float:
    """log_base(value) as a host reading (the window's bounds in k)."""
    return math.log(value) / math.log(base)


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


def port(gather: dict[str, object]) -> str:
    return str(gather["chosen"][0][0])  # type: ignore[index]


@pytest.mark.parametrize("name", NAMES)
def test_the_replay_is_bit_exact_against_the_registered_readings(name: str) -> None:
    """(c)."""
    pinned = PIN["worlds"][name]
    wheel = int(pinned["W"])
    run = PIN["run"]["worlds"][name]
    detector, game_board = run["readings"]["DETECTOR"], run["readings"]["GAMEBOARD"]
    assert game_board["conserved_at_every_completed_tick"] is True
    assert game_board["books_balanced_every_tick"] is True
    assert run["completed_ticks"] == pinned["ticks"]
    simulation = replay(name)
    assert simulation.layer is not None
    # The first W records by ordinal, the low 32 bits of the record's
    # identity (the lamp's number x 2^32 + the birth's ordinal, BEAM_LAW
    # note 37); the lamp's clock stalls as the births spend its content,
    # so a birth is not one per tick.
    gathers = [g for g in simulation.layer.gathers if ordinal(g) <= wheel]
    assert len(gathers) == wheel == detector["gathered_of_W"]
    assert len({g["record"] for g in gathers}) == wheel
    counts = Counter(port(g) for g in gathers)
    assert {cell: counts.get(cell, 0) for cell in PORTS} == detector["counts"] == pinned["counts"]
    assert sorted(int(g["u"]) for g in gathers if port(g) == "D2") == detector["u_to_D2"]  # type: ignore[call-overload]
    assert detector["u_to_D2"] == pinned["u_to_D2"]
    assert {tuple(cell[1] for cell in g["cells"]) for g in gathers} == {tuple(pinned["rungs"])}  # type: ignore[union-attr]
    assert detector["rungs_on_every_gather"] == pinned["rungs"]
    totals = {Fraction(int(g["total"][0]), int(g["total"][1])) for g in gathers}  # type: ignore[index]
    assert len(totals) == detector["distinct_totals"] == pinned["distinct_totals"]
    assert max(int(g["tick"]) for g in gathers) == detector["last_gather_tick"]  # type: ignore[call-overload]
    every = Counter(port(g) for g in simulation.layer.gathers)
    assert {cell: every.get(cell, 0) for cell in PORTS} == detector["counts_over_every_gather"]
    lamp = next(entry for entry in simulation.measured.values() if entry.lamp_rate is not None)
    assert lamp.births == game_board["born"]
    assert len(simulation.layer.gathers) == game_board["gathered"]
    assert lamp.births - len(simulation.layer.gathers) == game_board["open"]
    assert simulation.books(recount=True)["balanced"]
