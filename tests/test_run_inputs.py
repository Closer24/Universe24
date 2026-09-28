"""The one command (tools/run_inputs.py): input files in, one output file per experiment out, each in its own process; each input LAWFUL or REFUSED at load, a lawful one run and its clicks written per detector with the pin's verdict. COMPUTATION on small worlds; no pin of nature."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from run_inputs import OUTPUT_FORMAT, main, run_input  # noqa: E402

from event_universe.world_files import input_stamp  # noqa: E402
from tests.worlds import chain_world, emitter_world  # noqa: E402


def write(directory: Path, name: str, document: dict) -> Path:
    (path := directory / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", "utf-8")
    return path


def test_two_inputs_together_give_the_files_of_each_alone(tmp_path: Path):
    """Two small worlds (the emitter world with a stock of 2 over 250 intervals, the chain world with a stock of 2) run together in two processes and each alone: the output files are byte for byte the same; each output carries the format, the input's stamp, the verdict LAWFUL, the ticks, the click lines (detector and interval) and the counts per detector, with at least one click at `screen` in each."""
    emitter = emitter_world(stock=2, ticks=250)
    chain = chain_world(stock=2)
    chain["ticks"] = 250
    chain["stamp"] = input_stamp(chain)  # the stamp over the whole file (item 28)
    (inputs := tmp_path / "inputs").mkdir()
    a = write(inputs, "emitter_small", emitter)
    b = write(inputs, "chain_small", chain)
    together = tmp_path / "together"
    assert main(["--out", str(together), "--jobs", "2", str(a), str(b)]) == 0
    alone_a, alone_b = tmp_path / "alone_a", tmp_path / "alone_b"
    assert main(["--out", str(alone_a), "--jobs", "1", str(a)]) == 0
    assert main(["--out", str(alone_b), "--jobs", "1", str(b)]) == 0
    for name, alone in (("emitter_small", alone_a), ("chain_small", alone_b)):
        joint = (together / f"{name}.output.json").read_bytes()
        assert joint == (alone / f"{name}.output.json").read_bytes()
        output = json.loads(joint)
        assert output["format"] == OUTPUT_FORMAT and output["verdict"] == "LAWFUL"
        assert output["ticks"] == 250 and output["stamp"]["hash"]
        assert output["counts"]["screen"] >= 1 and output["pins"] == []
        keys = {"detector", "interval", "giving", "record", "giver", "taker", "norm", "tally"}
        keys |= {"giver_clock", "clock"}  # the body's language on every click
        assert all(set(click) == keys for click in output["clicks"])
        clicked = [c for c in output["clicks"] if c["detector"] is not None]
        assert sum(output["counts"].values()) == len(clicked)


def test_a_refused_input_writes_its_reason_and_the_pins_verdict_is_read(tmp_path: Path):
    """An input whose body lacks a key of the frame (its momentum) is REFUSED by name, its output carrying the reason and no clicks, and the command's exit is 1; a lawful input with pins registered before the run reads MATCH within the band and MISS outside it, the value read written beside each: a pin on the count of clicks, a pin on the detector's first click (the least interval since the record's giving among its clicks) and a pin on the mean interval since the giving over its clicks (ALGEBRA.md #the-ladder; a detector with no click reads None and MISS); the GAMEBOARD row `reversible` runs 60 intervals forward and back across the first giving's open and reads MATCH (HIGHLIGHTS line 33; across a window's close with stock left, and from interval 160 on, the same world reads MISS today: the engine's findings, named in the row)."""
    (inputs := tmp_path / "inputs").mkdir()
    # THE MODE PIN (item 57): the pins are compared under the mode "pin" alone; a start file of that mode, named by its path relative to the repository's root
    (start := tmp_path / "start_pin.json").write_text(json.dumps({"mode": "pin"}), encoding="utf-8")
    relative = os.path.relpath(start, Path(__file__).resolve().parents[1])
    bad = {**emitter_world(stock=2, ticks=200), "engine": relative}
    del bad["measured"][0]["momentum"]  # refused by name at the frame (the old residual check is gone)
    bad["stamp"] = input_stamp(bad)
    bad_path = write(inputs, "bad", bad)
    good = {**emitter_world(stock=2, ticks=250), "engine": relative}
    good["readings"] = [{"name": "n", "kind": "momentum", "body": 0, "every": 50}]
    good["stamp"] = input_stamp(good)
    good_path, twin_path = write(inputs, "good", good), write(inputs, "twin", good)
    # the expectation file beside the world, two sections: DETECTOR pins join the pins file's, GAMEBOARD pins read the declared readings at the named interval (a diagnostic) and the one-Node equivalence against a twin
    ratio = {"detector": "screen", "twin": "twin", "ratio": [1, 1], "band": [0, 1]}
    nowhere = {"detector": "screen", "twin": "nowhere", "ratio": [1, 1], "band": [1, 1]}
    expectation = {"DETECTOR": [{"detector": "screen", "count": 2, "band": 1}, ratio, nowhere]}
    expectation["GAMEBOARD"] = [{"body": 0, "interval": 50, "momentum": [0, 0, 0], "band": 0}]
    expectation["GAMEBOARD"].append({"equivalent": "twin", "within": 0})
    expectation["GAMEBOARD"].append({"equivalent": "nowhere", "within": 1})
    expectation["GAMEBOARD"].append(
        {"reversible": 60}
    )  # forward and back across the first giving's open
    good_path.with_suffix(".expectation.json").write_text(json.dumps(expectation), encoding="utf-8")
    good_pins = [
        {"detector": "screen", "count": 2, "band": 1},
        {"detector": "screen", "count": 40, "band": 1},
        {"detector": "screen", "first_click": 1, "band": 0},
        {"detector": "nowhere", "first_click": 1, "band": 1000},
        {"detector": "screen", "mean_interval": 100, "band": 60},
        {"detector": "nowhere", "mean_interval": 100, "band": 1000},
    ]
    (pins := tmp_path / "pins.json").write_text(json.dumps({"good": good_pins}), encoding="utf-8")
    inputs = ["--pins", str(pins), str(bad_path), str(good_path), str(twin_path)]
    assert main(["--out", str(out := tmp_path / "out"), "--jobs", "2", *inputs]) == 1
    refused = json.loads((out / "bad.output.json").read_text(encoding="utf-8"))
    assert refused["verdict"] == "REFUSED" and "clicks" not in refused
    assert "lacks keys: momentum" in refused["reason"]
    good = json.loads((out / "good.output.json").read_text(encoding="utf-8"))
    assert good["verdict"] == "LAWFUL" and (read := good["counts"]["screen"]) >= 0
    waits = [c["interval"] - c["giving"] for c in good["clicks"] if c["detector"] == "screen"]
    first, mean = min(waits), (2 * sum(waits) + len(waits)) // (2 * len(waits))
    assert good["pins"][6]["verdict"] == good["pins"][0]["verdict"] and len(good["pins"]) == 13
    assert [pin["verdict"] for pin in good["pins"][9:]] == ["MATCH", "MISS"] * 2
    assert (good["pins"][11]["read"], good["pins"][12]["read"]) == ([0, 0], None)
    assert good["clicks"][0]["giver"] == 0 and good["clicks"][0]["taker"] == 1  # the screen's entry
    assert (good["pins"][9]["read"], good["pins"][10]["read"]) == ([1, 1], None)
    assert (good["pins"][8]["kind"], good["pins"][8]["verdict"]) == ("reversible", "MATCH")
    momentum = [line for line in good["readings"] if line["name"] == "n"][0]["lines"][1]["momentum"]
    assert good["pins"][7]["read"] == momentum and good["pins"][7]["kind"] == "momentum"
    assert good["pins"][7]["verdict"] == ("MATCH" if momentum == [0, 0, 0] else "MISS")
    hits = [abs(read - 2) <= 1, first == 1, abs(mean - 100) <= 60]
    expected = [verdict for hit in hits for verdict in ("MATCH" if hit else "MISS", "MISS")]
    assert [pin["verdict"] for pin in good["pins"][:6]] == expected
    assert [pin["read"] for pin in good["pins"][:6]] == [read, read, first, None, mean, None]
    kinds = ["count", "first_click", "mean_interval"]
    assert [pin["kind"] for pin in good["pins"][:6]] == [kind for kind in kinds for _ in range(2)]


def test_a_leak_refuses_the_run_naming_the_family(tmp_path: Path, monkeypatch):
    """THE LEAK TEST IN EVERY RUN (the model owner's record 2075 (3); BUILD.md section 26 item 55): the runner reads the engine's leaks after every interval; a family carrying rows without a source ends the run with the verdict LEAK, the reason naming the family and the interval, the output written. The engine's own reading is tested in tests/test_charge.py (v); here its report is stood in for on the first interval. The edge case: with no leak the run is LAWFUL."""
    from event_universe.events.detector_law import DetectorLawSimulation

    document = emitter_world(stock=1, ticks=20)
    path = write(tmp_path, "leaky", document)
    calls: list[int] = []

    def ghost(self: DetectorLawSimulation) -> list[str]:
        calls.append(self.tick)
        return ["ghost"] if len(calls) == 1 else []

    monkeypatch.setattr(DetectorLawSimulation, "leaks", ghost)
    row = run_input(str(path), str(tmp_path), [])
    assert row["verdict"] == "LEAK"
    output = json.loads((tmp_path / "leaky.output.json").read_text(encoding="utf-8"))
    reason = output["reason"]
    assert output["verdict"] == "LEAK" and "['ghost']" in reason and "interval 1" in reason
    assert "clicks" not in output
    monkeypatch.setattr(DetectorLawSimulation, "leaks", lambda self: [])
    assert run_input(str(path), str(tmp_path), [])["verdict"] == "LAWFUL"


def test_a_refusal_inside_the_run_is_written_with_its_interval(tmp_path: Path, monkeypatch):
    """A guard's refusal inside the run (the amplitude bound, the twist table, the wall: an exception raised by the engine's step) ends the run with the verdict REFUSED, the reason naming the error and the interval, the output written as at a refusal at the load and no exception escaping; the edge case: a run without a refusal is LAWFUL."""
    from event_universe.events.detector_law import DetectorLawSimulation

    path = write(tmp_path, "guarded", emitter_world(stock=1, ticks=20))
    step = DetectorLawSimulation.step

    def guarded(self: DetectorLawSimulation) -> None:
        if self.tick == 2:
            raise ValueError("the twist on the Port toward +x reaches beyond the twist table")
        step(self)

    monkeypatch.setattr(DetectorLawSimulation, "step", guarded)
    assert run_input(str(path), str(tmp_path), [])["verdict"] == "REFUSED"
    output = json.loads((tmp_path / "guarded.output.json").read_text(encoding="utf-8"))
    assert output["verdict"] == "REFUSED" and "ValueError at interval 2" in output["reason"]
    assert "twist table" in output["reason"] and "clicks" not in output
    monkeypatch.setattr(DetectorLawSimulation, "step", step)
    assert run_input(str(path), str(tmp_path), [])["verdict"] == "LAWFUL"
