"""The step file drives the step: in one tick of a shipped world every built act of law/step.json is looked up once, in the file's order, and no built primitive runs outside an act (the gate of #1198, gate 2)."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from event_universe.core.rule3 import THE_REWRITE
from event_universe.core.step import STEP_FILE, read_step
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hold import HoldOwn, HoldStart, HoldTerm
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ("massive_record/light_clock.json", "dark_body/dark.json")


def spied(world: str) -> tuple[DetectorLawSimulation, list[tuple[str, str]], list[str]]:
    """A shipped world's loop with a spy on the register: the lookups in order, and every built primitive called outside an act."""
    document = json.loads((ROOT / "examples" / "events" / world).read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    register = simulation.register
    lookups: list[tuple[str, str]] = []
    outside: list[str] = []
    acting: list[str] = []
    lookup = register.at

    def at(name: str, place: str):  # type: ignore[no-untyped-def]
        lookups.append((place, name))
        return lookup(name, place)

    def counted(name: str, function):  # type: ignore[no-untyped-def]
        def call(*args, **words):  # type: ignore[no-untyped-def]
            if not acting:
                outside.append(name)
            return function(*args, **words)

        return call

    def within(name: str, stage):  # type: ignore[no-untyped-def]
        def run(function, **words):  # type: ignore[no-untyped-def]
            acting.append(name)
            try:
                return stage(function, **words)
            finally:
                acting.pop()

        return run

    for name in register.built_names():
        declaration = register.declarations[name]
        if declaration.function is not None:
            register.declarations[name] = dataclasses.replace(
                declaration, function=counted(name, declaration.function)
            )
    register.at = at  # type: ignore[method-assign]
    simulation.main_loop.acts = tuple(
        dataclasses.replace(
            act, stage=dataclasses.replace(act.stage, function=within(act.name, act.stage.function))
        )
        if act.stage is not None
        else act
        for act in simulation.main_loop.acts
    )
    return simulation, lookups, outside


def the_files_built_acts(simulation: DetectorLawSimulation) -> list[tuple[str, str]]:
    step = read_step(json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8")), "d")
    built = set(simulation.register.built_names())
    return [(place, name) for place, name, _words in step.acts if name in built]


def test_one_tick_looks_up_every_built_act_once_in_the_files_order_and_nothing_outside():
    for world in WORLDS:
        simulation, lookups, outside = spied(world)
        simulation.step()
        assert lookups == the_files_built_acts(simulation), world
        assert outside == [], world


def test_a_loop_out_of_the_files_order_or_calling_a_primitive_outside_an_act_fails():
    """A loop whose acts are out of the file's order is seen by the lookups; a primitive called outside an act is seen by the spy (the hold's line writes nothing on the GameBoard itself, so the main loop's guard has nothing to refuse there)."""
    simulation, lookups, outside = spied(WORLDS[0])
    acts = list(simulation.main_loop.acts)
    acts[2], acts[3] = acts[3], acts[2]
    simulation.main_loop.acts = tuple(acts)
    close = simulation.close_interval

    def close_and_cheat() -> None:
        term, own = HoldTerm("content", (1,), (1,), None, 1, 1), HoldOwn({}, {})
        start = HoldStart(THE_REWRITE, 0, (0, 0, 0), 1, None)
        simulation.register.declarations["the hold"].function(term, start, own)
        close()

    simulation.close_interval = close_and_cheat  # type: ignore[method-assign]
    simulation.step()
    assert lookups != the_files_built_acts(simulation)
    assert outside == ["the hold"]
