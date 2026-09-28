"""The main loop's guards (core/main_loop.py, core/ports.py): a cheating primitive is refused by name (a write its card does not name, a place not its own, a write into the interval's start, two writers out of the file's order), an honest one passes and its write lands, the six arrivals are one exchange per array per interval on the neighbours' addresses, and the walk is the file's. HOST; no physics, no pin."""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe import world_files as host
from event_universe.core.game_board import adjacent_node
from event_universe.core.main_loop import MainLoop, Stage
from event_universe.core.ports import Ports, arrival, port_of
from event_universe.core.primitive import Write
from event_universe.core.register import Declaration, Register, discover
from event_universe.core.step import INTERVAL, STEP_FILE, Step
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.records import StampedMap
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world, shipped

SPIN, MOMENTUM, CONTENT = "a body's spin S", "a body's momentum n", "a body's content M_k"
LAW_ROOT = host.LAW_ROOT


def cheated(tmp_path, monkeypatch, declaration, place, after, terms=(), acts_change=None):
    """The emitter world's engine with one more card and its act in the file after the act named."""
    monkeypatch.setattr(host, "LAW_ROOT", LAW_ROOT)
    document = emitter_world(stock=1, ticks=4)
    monkeypatch.setattr(host, "LAW_ROOT", tmp_path)
    (tmp_path / "law").mkdir(exist_ok=True)
    acts = list(shipped()[INTERVAL])
    index = next(i for i, act in enumerate(acts) if act[1] == after)
    acts.insert(index + 1, [place, declaration.name])
    if acts_change is not None:
        acts_change(acts)
    (tmp_path / STEP_FILE).write_text(json.dumps({INTERVAL: acts}), encoding="utf-8")

    class Cheated(DetectorLawSimulation):
        def _engine_register(self):
            register = discover()
            register.add(declaration)
            register.bind(self)
            return register

        def family_terms(self):
            return super().family_terms() + list(terms)

    return Cheated(parse_nature_beam_world(document))


def card(name, place, writes, function, word="after the step"):
    return Declaration(name, place, (), writes, function, "test", word=word)


def test_a_a_write_its_card_does_not_name_is_refused_by_name(tmp_path, monkeypatch):
    """A generic act writing a value outside its card, and a bound act changing a ledger word outside its card, are refused."""
    plain = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=4)))

    def apply(term, start, own):
        return [Write(MOMENTUM, 0, None, (1, 0, 0))]

    simulation = cheated(
        tmp_path,
        monkeypatch,
        card("the cheat", "(v)", (SPIN,), apply),
        "(v)",
        "the spin's step",
        [("test", "the cheat")],
    )
    with pytest.raises(
        ValueError,
        match="the primitive 'the cheat' wrote \"a body's momentum n\", which its card does not name",
    ):
        simulation.step()
    original = plain._hold

    def hold_and_cheat(*args, **kwargs):
        original(*args, **kwargs)
        plain.held[0][0] += 1

    plain._hold = hold_and_cheat  # type: ignore[method-assign]
    with pytest.raises(
        ValueError,
        match=r"the act 'the hold' at \(iv\) changed \"a body's content M_k\" of \['0'\]; its card names",
    ):
        plain.step()


def test_b_a_place_not_its_own_is_refused_and_a_bodys_value_at_ii_is_deferred_to_iv(
    tmp_path, monkeypatch
):
    """The register refuses a card listed at another place; a (ii) write of a body's value must be deferred and is applied before the (iv) hold, ahead of the feed's write at (v) by the places' order (its leapfrog then carries the written level as the level before)."""

    def apply(term, start, own):
        return [Write(MOMENTUM, 0, None, (1, 0, 0))]

    with pytest.raises(ValueError, match=r"lists 'the cheat' at \(v\), but it declares \(i\)"):
        cheated(tmp_path, monkeypatch, card("the cheat", "(i)", (SPIN), apply), "(v)", "the spin's step")
    simulation = cheated(
        tmp_path,
        monkeypatch,
        card("the cheat", "(ii)", (MOMENTUM,), apply),
        "(ii)",
        "the giving",
        [("test", "the cheat")],
    )
    with pytest.raises(
        ValueError,
        match="wrote \"a body's momentum n\" now; a body's value written at \\(ii\\) enters at \\(iv\\) and must be deferred",
    ):
        simulation.step()

    def deferred(term, start, own):
        return [Write(MOMENTUM, 0, None, (1, 0, 0), deferred=True)]

    simulation = cheated(
        tmp_path,
        monkeypatch,
        card("the cheat", "(ii)", (MOMENTUM,), deferred),
        "(ii)",
        "the giving",
        [("test", "the cheat")],
    )
    seen: list[list[int]] = []
    original_windows, original_fields = simulation._point_windows, simulation._advance_fields
    simulation._point_windows = lambda: (
        seen.append(list(simulation.blocks[0].momentum)),
        original_windows(),
    )[1]  # type: ignore[method-assign]
    simulation._advance_fields = lambda hold: (
        seen.append(list(simulation.blocks[0].momentum)),
        original_fields(hold),
    )[1]  # type: ignore[method-assign]
    simulation.step()
    body = simulation.blocks[0]  # the write landed at (iv); nothing at (v) steps the pair on
    assert seen == [[0, 0, 0], [1, 0, 0]] and body.momentum == [1, 0, 0]
    assert body.momentum_before == [0, 0, 0]


def test_c_a_write_into_the_intervals_start_is_refused(tmp_path, monkeypatch):
    """A primitive writing into a level of the start meets numpy's refusal, re-raised under its name."""

    def apply(term, start, own):
        start.levels_now[0][...] = 1
        return []

    simulation = cheated(
        tmp_path,
        monkeypatch,
        card("the cheat", "(v)", (SPIN,), apply),
        "(v)",
        "the spin's step",
        [("test", "the cheat")],
    )
    with pytest.raises(
        ValueError,
        match="the primitive 'the cheat' at \\(v\\) wrote into an array of the interval's start",
    ):
        simulation.step()


def fake_loop(state):
    """A loop object of the main loop's duck type over one integer state, no arrays."""

    class Loop:
        tick = 0
        ports = Ports((False, False, False))

        def start_arrays(self):
            return ()

        def grants(self, name):
            return ()

        def fingerprints(self):
            return {SPIN: {0: state["spin"]}}

        def close_interval(self):
            pass

    return Loop()


def test_d_two_writers_of_one_value_follow_the_files_order_or_are_refused():
    """Two cards writing one value in one interval pass in the file's order and are refused out of it; a file leaving one out is refused at load."""
    state = {"spin": 0}

    def writer(function):
        state["spin"] += 1

    register = Register()
    for name in ("the other cheat", "the cheat"):
        register.add(card(name, "(v)", (SPIN,), lambda *a: []))
    step = Step(
        {"(v)": ("the other cheat", "the cheat")},
        "d",
        (("(v)", "the other cheat", ()), ("(v)", "the cheat", ())),
    )
    register.check_step(step)
    stages = {name: Stage(writer, (), (name,)) for name in ("the other cheat", "the cheat")}
    loop = MainLoop.plan(register, step, stages, (), ())
    loop.run(fake_loop(state))
    assert loop.walked == ["the other cheat", "the cheat"] and state["spin"] == 2
    loop.written.clear()
    loop.note("the cheat", "(v)", SPIN, 0)
    with pytest.raises(
        ValueError,
        match="was written by \\['the cheat'\\] and then by 'the other cheat' in one interval; the step file orders no such pair",
    ):
        loop.note("the other cheat", "(v)", SPIN, 0)
    with pytest.raises(ValueError, match="leaves out the built primitive 'the cheat'"):
        register.check_step(Step({"(v)": ("the other cheat",)}, "d", (("(v)", "the other cheat", ()),)))


def test_e_an_honest_primitive_passes_and_its_write_lands(tmp_path, monkeypatch):
    """A generic act writing what its card names runs through the register and its write is applied by the loop."""

    def apply(term, start, own):
        return [Write(SPIN, 0, None, (0, 0, 1))]

    simulation = cheated(
        tmp_path,
        monkeypatch,
        card("the cheat", "(v)", (SPIN,), apply),
        "(v)",
        "the spin's step",
        [("test", "the cheat")],
    )
    simulation.step()
    assert simulation.blocks[0].spin == [0, 0, 1]
    assert simulation.register.at("the cheat", "(v)") is apply
    assert "the cheat" in simulation.main_loop.walked


def test_f_the_six_arrivals_are_the_neighbours_addresses_once_per_array_per_interval():
    """`arrival` agrees with `adjacent_node` on every Node and Port of a small board; the six arrivals of one array are taken once per interval and again after `begin`."""
    shape = (3, 2, 1)
    a = np.arange(6, dtype=np.int64).reshape(shape)
    for wrap in ((False, False, False), (True, False, True), (True, True, True)):
        for port in range(6):
            axis, side = port // 2, 1 if port % 2 == 0 else -1
            got = arrival(a, axis, side, wrap[axis], -1)
            if shape[axis] == 1:
                assert got is a
                continue
            for node in np.ndindex(shape):
                neighbour = adjacent_node(node, port, shape, wrap)
                assert got[node] == (-1 if neighbour is None else a[neighbour]), (wrap, port, node)
    ports = Ports((True, False, False))
    first = ports.arrivals(a)
    assert ports.arrivals(a) is first and ports.exchanged == 1
    assert first[port_of(0, 1)][0, 0, 0] == a[1, 0, 0] and first[port_of(0, -1)][0, 0, 0] == a[2, 0, 0]
    ports.begin()
    assert ports.arrivals(a) is not first and ports.exchanged == 2
    mask = np.zeros(shape, dtype=bool)
    mask[1, 0, 0] = True
    outward = ports.outward(mask, (False, False, False))
    assert outward[port_of(0, 1)][1, 0, 0] and outward[port_of(0, -1)][1, 0, 0]
    assert outward[port_of(1, 1)][1, 0, 0] and not outward[port_of(1, -1)].any()
    assert not outward[port_of(2, 1)].any() and not outward[port_of(2, -1)].any()


def test_g_the_walk_is_the_files_and_the_plan_refuses_by_name(tmp_path, monkeypatch):
    """One interval walks every built act of the file once in its order; a built card with no stage, no chain and no function is refused at load; a (ii) writer of a body's value with no (iv) act after (ii) is refused."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=4)))
    simulation.step()
    built = set(simulation.register.built_names())
    assert simulation.main_loop.walked == [
        name for _place, name, _words in simulation.world.step.acts if name in built
    ]
    with pytest.raises(
        ValueError, match="the loop has no stage for the built primitives \\['the cheat'\\]"
    ):
        cheated(
            tmp_path,
            monkeypatch,
            Declaration(
                "the cheat",
                "(v)",
                (),
                (SPIN,),
                None,
                "test",
                word="after the step",
                binder=lambda loop: lambda *a: None,
            ),
            "(v)",
            "the spin's step",
        )
    register = Register()
    register.add(card("the cheat", "(ii)", (CONTENT,), lambda *a: []))
    step = Step({"(ii)": ("the cheat",)}, "d", (("(ii)", "the cheat", ()),))
    register.check_step(step)
    with pytest.raises(
        ValueError,
        match="whose writes of a body's value enter at \\(iv\\), and no \\(iv\\) act after \\(ii\\)",
    ):
        MainLoop.plan(register, step, {}, (), ())


def test_a_bodys_remainders_are_stamped_by_identity_and_version_and_every_write_moves_the_stamp():
    """THE STAMP OF A BODY'S REMAINDERS (ENGINE.md, the main loop's guards): the audit takes each body's hold remainders by the map's identity and write counter, never by walking its entries (one per Node and part, stamped before and after every act), the counter rises at every kind of write and at no read, and an act writing a remainder outside its card is refused by name as before."""
    remainders = StampedMap({("g", 0): 1})
    seen = [remainders.version]
    for write in (
        lambda: remainders.__setitem__(("g", 1), 2),
        lambda: remainders.update({("g", 2): 3}),
        lambda: remainders.pop(("g", 2)),
        lambda: remainders.__delitem__(("g", 1)),
        remainders.clear,
    ):
        write()
        seen.append(remainders.version)
    assert seen == sorted(set(seen)) and len(seen) == 6
    remainders[("g", 0)] = 1
    version = remainders.version
    assert remainders.get(("g", 0)) == 1 and list(remainders.items()) and remainders.version == version
    loop = MainLoop.plan(Register(), Step({}, "d", ()), {}, (), ())
    stamp = (id(remainders), version, id(remainders), version)
    moved = {"a body's remainders": {0: stamp[:1] + (version + 1,) + stamp[2:]}}
    with pytest.raises(ValueError, match="changed \"a body's remainders\" of \['0'\]"):
        loop.audit("the cheat", "(v)", frozenset(), {"a body's remainders": {0: stamp}}, moved, set())
