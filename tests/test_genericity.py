"""The genericity test: a seeded generator draws one to twenty families with random English names and admitted attributes; every draw loads and runs, and five properties hold on each (a failing seed is kept)."""

from __future__ import annotations

import copy
import json
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import AMPLITUDE, INTERVALS, SEEDS, TEMPLATE, WORDS, draw, reads_of
from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
# draws kept as fixed tests with their seeds: seed -> the finding (empty until one fails)
KEPT: dict[int, str] = {}


def recorder():  # type: ignore[no-untyped-def]
    return load_file("state_digest", ROOT / "tools" / "state_digest.py")


SHIPPED = json.loads((ROOT / "examples/events/universe.json").read_text(encoding="utf-8"))
INTEGERS = {**SHIPPED["integers"], "node_clock": TEMPLATE["node_clock"], "amplitude_bound": AMPLITUDE}


def world_of(drawn: dict[str, Any]) -> dict[str, Any]:
    """The world on the drawn universe: the emitter test world's chain of 80 with its body of the drawn body family (the shipped kind and well, the seed on the mode as the template carries it), its emitter giving the drawn given family to the screen of three receivers, or the body alone where the draw has one family."""
    roles = drawn["roles"]
    document = copy.deepcopy(TEMPLATE)
    for key in ("node_clock", "amplitude_bound", "momentum_unit"):
        document.pop(key, None)
    document["universe"] = "universe.json"
    document["engine"] = "start.json"
    body = document["measured"][0]
    body["family"] = roles["body"]
    body["kind"] = [2, 3]
    if "given" in roles:
        body["stocks"] = {roles["given"]: 1}
        body["emitter"]["family"] = roles["given"]
        body["moment"] = [0, 0, 1]
        for receiver in document["measured"][1:]:
            receiver["family"] = roles["given"]
    else:
        body["stocks"] = {}
        body.pop("emitter")
        body.pop("moment", None)
        document["measured"] = [body]
        document["detectors"] = []
    document.pop("stamp", None)
    return document


def alone(drawn: dict[str, Any], families: list[dict[str, Any]]) -> tuple[list, dict]:
    """The world and the universe of property (d): the body alone on the GameBoard, no emitter, no stock, no detector, no moment (no click and no load acts on its record); the body's reads kept where they are at the plain pace (an integer weight, by 1, the twist "own")."""
    document = world_of(drawn)
    body = document["measured"][0]
    body["stocks"] = {}
    body.pop("emitter", None)
    body["moment"] = [0, 0, 0]
    document["measured"] = [body]
    document["detectors"] = []
    plain = copy.deepcopy(families)
    for family in plain:
        if family["name"] == drawn["roles"]["body"]:
            family["reads"] = [
                read
                for read in family["reads"]
                if isinstance(read["weight"], int) and read["by"] == 1 and read["twist"] == "own"
            ]
    return plain, document


def place(
    tmp_path: Path, monkeypatch, families: list[dict[str, Any]], document: dict[str, Any]
) -> dict[str, Any]:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "universe.json").write_text(
        json.dumps({"integers": INTEGERS, "families": families}), encoding="utf-8"
    )
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    placed = copy.deepcopy(document)
    placed["stamp"] = input_stamp(placed)
    return placed


def run(document: dict[str, Any], intervals: int = INTERVALS) -> tuple[DetectorLawSimulation, list]:
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    lines: list[dict[str, object]] = []
    simulation.record = lines.append
    for _ in range(intervals):
        simulation.step()
        assert simulation.leaks() == [], "a family with no source moved (record 2075 (3))"
    return simulation, lines


def renamed(value: Any, mapping: dict[str, str]) -> Any:
    """Every family name in a reading replaced by its new name (keys and string values)."""
    if isinstance(value, dict):
        return {renamed(k, mapping): renamed(v, mapping) for k, v in value.items()}
    if isinstance(value, list):
        return [renamed(v, mapping) for v in value]
    if isinstance(value, str):
        for old, new in mapping.items():
            value = value.replace(old, new) if value == old else value
        return value
    return value


def rename_everything(
    families: list[dict[str, Any]], document: dict[str, Any], mapping: dict[str, str]
) -> tuple[list, dict]:
    return renamed(copy.deepcopy(families), mapping), renamed(copy.deepcopy(document), mapping)


def state_reading(module, simulation: DetectorLawSimulation) -> dict[str, Any]:  # type: ignore[no-untyped-def]
    reading = module.run_reading(simulation, [])
    return {k: v for k, v in reading.items() if k in ("records", "held families", "read remainders")}


@pytest.mark.parametrize("seed", SEEDS)
def test_a_drawn_universe_loads_runs_and_keeps_the_five_properties(seed: int, tmp_path, monkeypatch):
    if seed in KEPT:
        pytest.xfail(KEPT[seed])
    module = recorder()
    drawn = draw(seed)
    families, document = drawn["families"], world_of(drawn)
    # the draw loads and runs (every family of the universe on, record 2075)
    placed = place(tmp_path, monkeypatch, families, document)
    simulation, lines = run(placed)
    assert [f.name for f in simulation.families] == [f["name"] for f in families]
    base = module.run_reading(simulation, lines)
    digest = module.digest_of(base)
    # (c) no source, exactly zero: the run's leak test held at every interval (in `run`); and
    # every clicking family without a record or a hold has no level anywhere
    roles, holders = drawn["roles"], drawn["holders"]
    quiet = {f["name"] for f in families} - {roles["body"], roles.get("given")} - set(holders)
    for index, family in enumerate(simulation.families):
        if family.name in quiet:
            assert all(live.family != index for live in simulation.records.values())
    # (a) renaming the families leaves the run bit for bit
    rng = random.Random(seed + 1000)
    fresh = rng.sample([w for w in WORDS if w not in {f["name"] for f in families}], len(families))
    mapping = {f["name"]: new for f, new in zip(families, fresh, strict=True)}
    families_a, document_a = rename_everything(families, document, mapping)
    placed_a = place(tmp_path, monkeypatch, families_a, document_a)
    simulation_a, lines_a = run(placed_a)
    back = {new: old for old, new in mapping.items()}
    assert module.digest_of(renamed(module.run_reading(simulation_a, lines_a), back)) == digest
    # (b) reordering the families in the universe file leaves it bit for bit
    families_b = list(families)
    rng.shuffle(families_b)
    if families_b == families and len(families) > 1:
        families_b = families[::-1]
    placed_b = place(tmp_path, monkeypatch, families_b, document)
    simulation_b, lines_b = run(placed_b)
    assert module.digest_of(module.run_reading(simulation_b, lines_b)) == digest
    # (d) Rule3's conserved form where no click and no load acts: the body alone, its own
    # record's step the exact identity value - previous = the remainders' drift (ALGEBRA.md
    # ALGEBRA.md #the-line; item 44), the record's own pair (ALGEBRA.md #the-primitives), the level in force the body's plain
    # reads summed (weight x the read family's level as the interval began)
    plain, document_d = alone(drawn, families)
    placed_d = place(tmp_path, monkeypatch, plain, document_d)
    simulation_d = DetectorLawSimulation(parse_nature_beam_world(placed_d))
    (live,) = simulation_d.records.values()
    body_family = live.family
    num, den = simulation_d.pair_arrays(body_family, live.pair)
    counts = {f["name"]: f["held"]["count"] for f in plain if "held" in f}
    weights = {
        counts[read["family"]]: read["weight"]
        for f in plain
        if f["name"] == roles["body"]
        for read in f["reads"]
    }

    def level_in_force() -> np.ndarray:
        level = np.zeros(simulation_d.shape, dtype=np.int64)
        for count, weight in weights.items():
            level += weight * simulation_d.level_of(count)
        return level

    def form(now: np.ndarray, before: np.ndarray, level: np.ndarray) -> Fraction:
        (read_coefficient, _, _), self_coefficient, wall = coefficients(
            num.astype(object), den.astype(object), simulation_d.node_clock, level.astype(object)
        )
        read = reads_of(simulation_d, body_family)(before).astype(object)
        total = Fraction(0)
        for node in zip(*np.nonzero(now.astype(object) | before.astype(object) | read), strict=True):
            a, b = int(now[node]), int(before[node])
            total += Fraction(
                int(wall[node]) * (a * a + b * b) - int(self_coefficient[node]) * a * b,
                3 * int(read_coefficient[node]),
            )
            total -= Fraction(1, 3) * a * int(read[node])
        return total

    states = [(live.now.copy(), live.before.copy(), live.remainder.copy())]
    levels = [level_in_force()]
    for _ in range(INTERVALS):
        simulation_d.step()
        (live,) = simulation_d.records.values()
        states.append((live.now.copy(), live.before.copy(), live.remainder.copy()))
        levels.append(level_in_force())
    assert len(simulation_d.layer.gathers) == 0, "the body alone clicks"
    assert np.count_nonzero(states[-1][0]) > 0, "the body's record is empty"
    for t in range(1, INTERVALS + 1):
        now, before, remainder = states[t]
        prev_now, prev_before, prev_remainder = states[t - 1]
        (read_coefficient, _, _), _self, _wall = coefficients(
            num.astype(object), den.astype(object), simulation_d.node_clock, levels[t - 1].astype(object)
        )
        drift = Fraction(0)
        for node in zip(*np.nonzero((now != prev_before) | (remainder != prev_remainder)), strict=True):
            drift += Fraction(
                (int(now[node]) - int(prev_before[node]))
                * (int(prev_remainder[node]) - int(remainder[node])),
                3 * int(read_coefficient[node]),
            )
        value = form(now, before, levels[t - 1])
        previous = form(prev_now, prev_before, levels[t - 1])
        assert value - previous == drift, (seed, t)
    # (e) running backward returns the start in the world of the Nodes, bit for bit
    simulation_e = DetectorLawSimulation(parse_nature_beam_world(placed))
    start = state_reading(module, simulation_e)
    start_digest = module.digest_of(start)
    for _ in range(INTERVALS):
        simulation_e.step()
    assert module.digest_of(state_reading(module, simulation_e)) != start_digest
    for _ in range(INTERVALS):
        simulation_e.step_inverse()
    assert module.digest_of(state_reading(module, simulation_e)) == start_digest


def test_the_draw_is_fixed_by_its_seed_and_spans_the_admitted_attributes():
    """The same seed draws the same universe; over the seeds the draw reaches one to twenty families, every parts form, both phases, several pairs, holds of both counts, reads by plain and by sign with an integer or the universe's word for the weight, a self-source on and off, quanta above one."""
    assert draw(3) == draw(3)
    seen: dict[str, set] = {
        k: set() for k in ("count", "parts", "phase", "pair", "held", "by", "weight", "self", "quantum")
    }
    for seed in range(200):
        drawn = draw(seed)
        seen["count"].add(len(drawn["families"]))
        for f in drawn["families"]:
            seen["parts"].add(tuple(f["parts"]))
            seen["phase"].add(f["phase"])
            seen["pair"].add(str(f["pair"]))
            if "held" in f:
                seen["held"].add(f["held"]["count"])
            for r in f["reads"]:
                seen["by"].add(r["by"])
                seen["weight"].add(str(r["weight"]))
            seen["self"].add(f["self_source"]["unit"] > 0)
            if "clicks" in f:
                seen["quantum"].add(f["clicks"]["quantum"])
    assert seen["count"] >= {1, 2, 20} and min(seen["count"]) == 1 and max(seen["count"]) == 20
    assert seen["parts"] == {(1,), (1, 3), (1, 3, 6)} and seen["phase"] == {1, 2}
    assert len(seen["pair"]) >= 5 and seen["held"] == {"content", "sign"}
    assert seen["by"] == {1, "q"} and "Lambda" in seen["weight"] and "1" in seen["weight"]
    assert seen["self"] == {True, False} and seen["quantum"] >= {1, 2, 3, 4}
