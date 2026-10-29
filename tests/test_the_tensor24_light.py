"""Tensor24's light against the head: its pull the head's push at every site and tick, and its gear the head's act
wherever the head's W stands at its W+, at the head's inputs."""

# The named differences (derive/head_light): the turnover replaces the act at turned-over clocks (stage 8); the regulator
# moves W, W+ and the stretch at every tick (stage 7), the gear's W = W+; the head's grips are one end's of a Mesh (law 2).

from types import SimpleNamespace

import numpy as np
import pytest

from event_universe import readings
from event_universe import tick as head
from event_universe.clock import Clock
from event_universe.trains import REGULATOR
from tensor24.engine import mesh, step
from tensor24.engine.state import Layout
from tensor24.runner.board import board
from tests.frame import same
from tests.laws import world_of


def worlds():
    """The probe's six: the head's smallest test piece, its sea, a packet over the sea, the packet alone, side 4, the vacuum."""
    node, piece = world_of("world_node.json")
    sea, sea_piece = world_of("world_sea_3.json")
    wave = [node["integers"]["den"] // 2, 0, 0]
    packet = {
        "lay": "at",
        "row": 0,
        "centre": [1, 1, 1],
        "width": 2,
        "quanta": 1,
        "sense": 1,
        "wave": wave,
    }
    return [
        (node, piece, 40),
        (sea, sea_piece, 30),
        (node, {**piece, "seed": [{"lay": "sea", "row": 0}, packet]}, 30),
        (node, {**piece, "seed": [packet]}, 30),
        (node, {**piece, "shape": [4, 4, 4]}, 30),
        (node, {**piece, "seed": []}, 20),
    ]


def run(calibre, piece, ticks):
    """One world of the head: per tick the light at the start, after its act and at the end, W, W+, s R, the turnovers."""
    clock = Clock(calibre, piece)
    # the trains stand, and each carry makes their gears anew
    light, regulator, seen = clock.unsprung(), clock.train(REGULATOR), []
    impulse, advances, click = head.Tick.impulse, head.Tick.advances, head.Tick.click

    def gears():
        return [
            [np.asarray(x, dtype=object).reshape(1, -1) for x in (g.now, g.before, g.fine)]
            for g in light.gears
        ]

    def started(tick):
        grips = readings.gearing_of(clock, light, tick.load, tick.factors).grips
        w = readings.mean_teeth(clock, regulator.gears[0])
        seen.append({"start": gears(), "w": w, "grip": [tick.stretch_now * grip for grip in grips]})
        impulse(tick)

    def acted(tick):
        seen[-1] |= {"wp": tick.end_teeth(regulator.gears[0]), "act": gears()}
        advances(tick)

    def ended(tick):
        click(tick)
        seen[-1] |= {"end": gears(), "top": np.asarray(tick.top, dtype=bool).reshape(1, -1)}

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(head.Tick, "impulse", started)
        patch.setattr(head.Tick, "advances", acted)
        patch.setattr(head.Tick, "click", ended)
        for _ in range(ticks):
            clock.tick()
    return tuple(clock.size), seen


@pytest.fixture(scope="module")
def heads():
    """The six worlds, run once for every law and mutant."""
    return [run(*world) for world in worlds()]


def pushed(a, b, r, done, w, wp):
    """The head's push from its act: its stride read at W, carried at W+, each tooth about its home, the going 0."""
    after, _, kept = done
    return (after - a) * wp + kept - wp // (1 + 1) - w * (a - b) - r + w // (1 + 1)


def alike(m, heads):
    """At the head's inputs the pull is its push everywhere; where its W stands at W+ the gear is its act and its end."""
    for shape, seen in heads:
        nb, _ = board(shape)
        # each Spoke its own grip: the grips fed, s R, depart from law 2 at 9,713 of the six worlds' 17,910 Meshes
        spokes = np.arange(6 * nb.shape[1]).reshape(6, -1)
        for act in seen:
            grip = np.concatenate([np.asarray(g, dtype=object).reshape(-1) for g in act["grip"]])
            layout = Layout(nb, spokes, grip.reshape(1, -1), None, None, None)
            w, wp = (np.asarray(act[key], dtype=object).reshape(1, -1) for key in ("w", "wp"))
            held = w == wp
            for (a, b, r), done, end in zip(act["start"], act["act"], act["end"], strict=True):
                pull = m.pull(layout, a)
                ticked = m.gear(a, b, r, w, pull)
                at = [held, held & ~act["top"]]
                if not (
                    same([pull], [pushed(a, b, r, done, w, wp)])
                    and all((x[at[0]] == y[at[0]]).all() for x, y in zip(ticked, done, strict=True))
                    and all((x[at[1]] == y[at[1]]).all() for x, y in zip(end, ticked, strict=True))
                ):
                    return False
    return True


def mutants():
    """Broken copies of the act, each with what it replaces: the comparison must part on every one."""
    pull, gear = mesh.pull, step.gear
    first = lambda grip: grip * (np.arange(grip.shape[-1]) >= grip.shape[-1] // 6)  # noqa: E731
    return {
        "the push's sign": {"gear": lambda a, b, r, w, push: gear(a, b, r, w, -push)},
        "the fine tooth dropped": {"gear": lambda a, b, r, w, push: gear(a, b, 0 * r, w, push)},
        "b+ = b in place of b+ = a": {
            "gear": lambda a, b, r, w, push: (lambda x, _, z: (x, b, z))(*gear(a, b, r, w, push))
        },
        "the grip taken from the neighbour's Mesh": {
            "pull": lambda layout, a: pull(layout._replace(meshes=layout.meshes[:, layout.nb[0]]), a)
        },
        "the +x Spoke's pull dropped": {
            "pull": lambda layout, a: pull(layout._replace(grip=first(layout.grip)), a)
        },
    }


@pytest.mark.parametrize("mutant", list(mutants()))
def test_the_light_acts_as_the_head_does_at_its_inputs_and_fails_on_each_mutant(mutant, heads):
    engine = SimpleNamespace(pull=mesh.pull, gear=step.gear)
    assert alike(engine, heads)
    assert not alike(SimpleNamespace(**{**vars(engine), **mutants()[mutant]}), heads)


def test_the_named_differences_are_met_in_the_worlds(heads):
    seen = [act for _, acts in heads for act in acts]
    assert any(act["top"].any() for act in seen)
    assert any((act["wp"] != act["w"]).any() for act in seen) and any(
        (act["wp"] == act["w"]).any() for act in seen
    )
