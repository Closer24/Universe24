"""THE STEP FILE: the interval's order lives in one data file shared by every world, law/step.json,
an ordered list of acts, each a primitive's name at its place with the words of its call; the
host reads it, the loader carries it, the loop walks it act by act through the register and
holds only the interval's frame (the clock, the bodies' clocks, the deletion, the readings) and
the record's fused chain; the register refuses a file naming an unknown primitive, listing one at
a place it does not declare, or leaving out a built one, and the loop refuses an act with words
its stage does not take or a file ordering the record's chain otherwise; the writers of one value
at one place follow the file's order (ALGEBRA.md 9.117 item 3 transcribed); a folder's card
carries no order; every run writes the file's digest; two independent acts exchanged in a
temporary file exchange the loop's calls; today's step is transcribed, every shipped world bit
for bit (the digests' gate). HOST; no physics, no pin."""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe import world_files as host
from event_universe.core.register import Declaration, Register, discover
from event_universe.core.step import INTERVAL, PLACES, STEP_FILE, Step, read_step
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_digest, parse_nature_beam_world, world_files
from tests.running import ORDERS
from tests.worlds import emitter_world, shipped

ROOT = Path(__file__).resolve().parents[1]


def tool(name: str):
    """A tool of tools/ loaded by its file (the tools are not a package)."""
    spec = importlib.util.spec_from_file_location(f"{name}_step", ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"{name}_step"] = module
    spec.loader.exec_module(module)
    return module


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
    assert step.acts[0][:2] == ("(iv)", "the hold")
    holds = [act for act in step.acts if act[1] == "the hold"]
    assert holds == [
        ("(iv)", "the hold", (("advance", False),)),
        ("(iv)", "the hold", (("advance", True),)),
    ]
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
    module = tool("run_inputs")
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


def test_each_defect_of_the_file_is_refused_by_name(tmp_path, monkeypatch):
    good = shipped()
    register = discover()

    def refused(change, match):
        broken = json.loads(json.dumps(good))
        change(broken)
        with pytest.raises(ValueError, match=match):
            register.check_step(read_step(broken, "d"))

    with pytest.raises(ValueError, match="law/step.json must be a JSON object with the key 'interval'"):
        read_step([], "d")
    with pytest.raises(ValueError, match=r"has unknown keys: \(i\), \(ii\) \(the one key: 'interval'\)"):
        read_step({"(i)": [], "(ii)": []}, "d")
    refused(lambda d: d.__setitem__("(vi)", []), r"law/step.json has unknown keys: \(vi\) \(the one key")
    refused(lambda d: d.pop(INTERVAL), "law/step.json lacks the key 'interval'")
    refused(lambda d: d.__setitem__(INTERVAL, {}), "law/step.json.interval must be a list of acts")
    refused(
        lambda d: d[INTERVAL].__setitem__(3, "the hold"),
        r"law/step.json.interval\[3\] must be \[place, name\]",
    )
    refused(
        lambda d: d[INTERVAL].__setitem__(3, ["(i)", "the hold", {"advance": 1.5}]),
        r"interval\[3\] must be",
    )
    refused(
        lambda d: d[INTERVAL].__setitem__(0, ["(vi)", "the hold"]),
        r"interval\[0\] names the place '\(vi\)', which is none of",
    )
    refused(
        lambda d: d[INTERVAL].append(["(iii)", "the hold"]),
        r"lists 'the hold' at \(iv\) and \(iii\): one place per primitive",
    )
    refused(
        lambda d: d[INTERVAL].append(["(iv)", "the hold", {"advance": True}]),
        r"lists the act 'the hold' at \(iv\) with the words \{'advance': True\} twice: one act, one call",
    )
    refused(
        lambda d: d[INTERVAL].append(["(iv)", "the well"]),
        r"lists 'the well' at \(iv\), which the register lacks",
    )
    refused(
        lambda d: d[INTERVAL].__setitem__(14, ["(v)", "the giving"]),
        r"lists 'the giving' at \(v\), but it declares \(ii\)",
    )
    refused(lambda d: d[INTERVAL].pop(12), "leaves out the built primitive .the count's line.")
    # the loop's refusals at construction, the file redirected: the record's chain reordered, an act
    # with other words, a whole-board act inside the chain
    monkeypatch.setattr(host, "LAW_ROOT", tmp_path)
    (tmp_path / "law").mkdir()

    def constructed(acts):
        (tmp_path / STEP_FILE).write_text(json.dumps({INTERVAL: acts}), encoding="utf-8")
        return DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))

    acts = good[INTERVAL]
    assert constructed(acts).register.step.acts == read_step(good, "d").acts
    with pytest.raises(
        ValueError,
        match="the record's step is one chain today: the pair, .*; the file orders them as the clicks, the operation, the phase",
    ):
        constructed(list(reversed(acts)))
    moved = [act for act in acts if act[1] != "the giving"]
    moved.insert(moved.index(["(ii)", "the clicks"]), ["(ii)", "the giving"])
    with pytest.raises(
        ValueError, match="the file orders them as the pair, .*the clicks, with the giving between them"
    ):
        constructed(moved)
    with pytest.raises(
        ValueError,
        match=r"the step file's act 'the hold' at \(iv\) carries the words \[\]; the loop's stage of 'the hold' takes \['advance'\]",
    ):
        constructed(
            [
                ["(iv)", "the hold"] if act[1] == "the hold" and not act[2]["advance"] else act
                for act in acts
            ]
        )
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any") and tuple(good) == (INTERVAL,)
    assert tuple(read_step(good, "d").places) == PLACES


def test_a_world_without_the_step_file_is_refused_at_load():
    from event_universe.loader.world import parse_world_document

    document = emitter_world(stock=1, ticks=2)
    files = {key: value for key, value in world_files(document).items() if key != STEP_FILE}
    with pytest.raises(
        ValueError, match="the step file 'law/step.json' is missing at the repository's root"
    ):
        parse_world_document(document, files, input_digest(document))
