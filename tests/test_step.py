"""THE STEP FILE (the model owner's decision through the Boss, record 2251): the interval's
order lives in one data file shared by every world, law/step.json, the places (i) to (v) and
"any" with the ordered names of the register's primitives; the loop reads it at the start
through the host (world_files) and the register refuses a file naming an unknown primitive,
listing one at a place it does not declare, or leaving out a built one; the writers of one
value at one place follow the file's order (ALGEBRA.md 9.117 item 3 transcribed: the hold
before the source, the clicks before the giving before the clicks list, the giving's bulk
share before the recoil, the feed before the induction, the receive before the internal
representation, the clicks before the lifetime); a folder's card carries no order; every run
writes the file's digest; today's step is transcribed, every shipped world bit for bit (the
digests' gate). HOST; no physics, no pin."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from event_universe.core.register import Declaration, Register, discover
from event_universe.core.step import PLACES, STEP_FILE, Step, read_step
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, parse_nature_beam_world, world_files
from tests.test_emitter import emitter_world
from tests.test_register import ORDERS

ROOT = Path(__file__).resolve().parents[1]


def shipped() -> dict:
    return json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8"))


def test_the_file_names_every_built_primitive_at_its_declared_place_and_the_writers_follow_it():
    register = discover()
    step = read_step(shipped(), "d")
    register.check_step(step)
    listed = [name for names in step.places.values() for name in names]
    assert set(register.built_names()) <= set(listed) and len(listed) == len(set(listed))
    for place, names in step.places.items():
        for name in names:
            assert register.declarations[name].place == place, name
    assert step.places["(iii)"] == () and step.places["any"] == ("the trace",)
    for (place, value), expected in ORDERS.items():
        assert register.writers(value, place, step) == expected, (place, value)
    register.check_writers(step)
    assert not any(field.name == "order" for field in dataclasses.fields(Declaration))


def test_the_host_reads_the_file_the_loader_carries_it_and_the_run_writes_its_digest(tmp_path):
    document = emitter_world(stock=1, ticks=3)
    files = world_files(document)
    step = files[STEP_FILE]
    assert isinstance(step, Step) and step.digest == input_digest(shipped())
    world = parse_nature_beam_world(document)
    assert world.step == step
    simulation = DetectorLawSimulation(world)
    assert simulation.register.step == step
    for _ in range(3):
        simulation.step()
    # the loop's calls through the register stand at the file's places; another place is refused
    assert simulation.register.at("the hold", "(iv)") is not None
    with pytest.raises(
        ValueError,
        match=r"the loop calls the primitive 'the hold' at the place \(ii\), but it declares",
    ):
        simulation.register.at("the hold", "(ii)")
    listed_elsewhere = Register()
    listed_elsewhere.add(
        Declaration("the hold", "(iv)", (), ("a family's level at a Node",), lambda: 0, "")
    )
    listed_elsewhere.add(
        Declaration("the source", "(iv)", (), ("a family's level at a Node",), lambda: 0, "")
    )
    listed_elsewhere.check_step(Step({"(iv)": ("the hold", "the source")}, "d"))
    assert listed_elsewhere.at("the source", "(iv)")() == 0
    partial = Register()
    partial.add(Declaration("the hold", "(iv)", (), (), lambda: 0, ""))
    partial.add(Declaration("the source", "(iv)", (), (), None, ""))
    partial.check_step(Step({"(iv)": ("the hold",)}, "d"))
    with pytest.raises(
        ValueError,
        match=r"calls the primitive 'the source' at \(iv\), which the step file does not list there",
    ):
        partial.at("the source", "(iv)")
    # the one command writes the digest beside the stamp
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("run_inputs_step", ROOT / "tools" / "run_inputs.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["run_inputs_step"] = module
    spec.loader.exec_module(module)
    source = tmp_path / "world.json"
    source.write_text(json.dumps(document), encoding="utf-8")
    module.run_input(str(source), str(tmp_path), [])
    output = (
        json.loads((tmp_path / "world.json").read_text(encoding="utf-8"))
        if (tmp_path / "world.json").exists()
        else None
    )
    written = next(p for p in tmp_path.glob("*.json") if p.name != "world.json")
    output = json.loads(written.read_text(encoding="utf-8"))
    assert output["verdict"] == "LAWFUL" and output["step"] == {"hash": input_digest(shipped())}


def test_each_defect_of_the_file_is_refused_by_name():
    good = shipped()
    register = discover()

    def refused(change, match):
        broken = json.loads(json.dumps(good))
        change(broken)
        with pytest.raises(ValueError, match=match):
            register.check_step(read_step(broken, "d"))

    with pytest.raises(ValueError, match="law/step.json must be a JSON object with the places"):
        read_step([], "d")
    refused(lambda d: d.__setitem__("(vi)", []), r"law/step.json has unknown keys: \(vi\)")
    refused(lambda d: d.pop("(iii)"), r"law/step.json lacks the places: \(iii\)")
    refused(
        lambda d: d.__setitem__("(iii)", "the hold"),
        r"law/step.json.\(iii\) must be a list of primitive names",
    )
    refused(lambda d: d["(iii)"].append("the hold"), r"lists 'the hold' twice, at \(iii\) and \(iv\)")
    refused(
        lambda d: d["(iv)"].append("the well"), r"lists 'the well' at \(iv\), which the register lacks"
    )
    refused(
        lambda d: (d["(iv)"].remove("the hold"), d["(ii)"].append("the hold")),
        r"lists 'the hold' at \(ii\), but it declares \(iv\)",
    )
    refused(lambda d: d["(iv)"].remove("the hold"), "leaves out the built primitive 'the hold'")
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any") and tuple(good) == PLACES


def test_a_world_without_the_step_file_is_refused_at_load():
    from event_universe.events.world import parse_world_document

    document = emitter_world(stock=1, ticks=2)
    files = {key: value for key, value in world_files(document).items() if key != STEP_FILE}
    with pytest.raises(
        ValueError, match="the step file 'law/step.json' is missing at the repository's root"
    ):
        parse_world_document(document, files, input_digest(document))
