"""THE ONE COMMAND (the model owner's record 1887 of 2026-09-25; tools/run_inputs.py):
input files in, one output file per experiment out, each in its own process, in
parallel; each input first LAWFUL or REFUSED at load, the lawful one run under the law
and its clicks written per detector with the registered pin's verdict. Every reading
here is the engine's on the line's small test worlds (COMPUTATION); no pin of nature.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from run_inputs import OUTPUT_FORMAT, main  # noqa: E402

from event_universe.events.world import input_stamp  # noqa: E402
from tests.test_detector_law import chain_world  # noqa: E402
from tests.test_emitter import emitter_world  # noqa: E402


def write(directory: Path, name: str, document: dict) -> Path:
    path = directory / f"{name}.json"
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path


def test_two_inputs_together_give_the_files_of_each_alone(tmp_path: Path):
    """Two small worlds (the emitter world with a stock of 2 over 250 intervals, the chain
    world with a stock of 2) run together in two processes and each alone: the output files
    are byte for byte the same; each output carries the format, the input's stamp, the
    verdict LAWFUL, the ticks, the click lines (detector and interval) and the counts per
    detector, with at least one click at `screen` in each."""
    emitter = emitter_world(stock=2, ticks=250)
    chain = chain_world(stock=2)
    chain["ticks"] = 250
    chain["input"] = input_stamp(chain)  # the stamp over the whole file (item 28)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    a = write(inputs, "emitter_small", emitter)
    b = write(inputs, "chain_small", chain)
    together = tmp_path / "together"
    assert main(["--out", str(together), "--jobs", "2", str(a), str(b)]) == 0
    alone_a = tmp_path / "alone_a"
    alone_b = tmp_path / "alone_b"
    assert main(["--out", str(alone_a), str(a)]) == 0
    assert main(["--out", str(alone_b), str(b)]) == 0
    for name, alone in (("emitter_small", alone_a), ("chain_small", alone_b)):
        joint = (together / f"{name}.output.json").read_bytes()
        assert joint == (alone / f"{name}.output.json").read_bytes()
        output = json.loads(joint)
        assert output["format"] == OUTPUT_FORMAT and output["verdict"] == "LAWFUL"
        assert output["ticks"] == 250 and output["stamp"]["law"]
        assert output["counts"]["screen"] >= 1 and output["pins"] == []
        assert all(
            set(click) == {"detector", "interval", "birth", "record"} for click in output["clicks"]
        )
        assert sum(output["counts"].values()) == len(
            [click for click in output["clicks"] if click["detector"] is not None]
        )


def test_a_refused_input_writes_its_reason_and_the_pins_verdict_is_read(tmp_path: Path):
    """An input whose profile is off the mode (the peak doubled, the stamp rewritten so that
    the residual speaks) is REFUSED, its output carrying the reason and no clicks, and the
    command's exit is 1; a lawful input with pins registered before the run reads MATCH
    within the band and MISS outside it, the value read written beside each: a pin on the
    count of clicks, a pin on the detector's first click (the least interval since the
    record's birth among its clicks) and a pin on the mean interval since the birth over
    its clicks (ALGEBRA.md 9.25 (11) (d); a detector with no click reads None and MISS)."""
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    bad = emitter_world(stock=2, ticks=200)
    profile = bad["measured"][0]["seed"]
    peak = max(range(len(profile)), key=lambda index: abs(profile[index]))
    profile[peak] *= 2
    bad["input"] = input_stamp(bad)
    bad_path = write(inputs, "bad", bad)
    good_path = write(inputs, "good", emitter_world(stock=2, ticks=250))
    pins = tmp_path / "pins.json"
    pins.write_text(
        json.dumps(
            {
                "good": [
                    {"detector": "screen", "count": 2, "band": 1},
                    {"detector": "screen", "count": 40, "band": 1},
                    {"detector": "screen", "first_click": 1, "band": 0},
                    {"detector": "nowhere", "first_click": 1, "band": 1000},
                    {"detector": "screen", "mean_interval": 100, "band": 60},
                    {"detector": "nowhere", "mean_interval": 100, "band": 1000},
                ]
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    assert (
        main(["--out", str(out), "--jobs", "2", "--pins", str(pins), str(bad_path), str(good_path)]) == 1
    )
    refused = json.loads((out / "bad.output.json").read_text(encoding="utf-8"))
    assert (
        refused["verdict"] == "REFUSED"
        and "is not the mode of its family's operator" in refused["reason"]
    )
    assert "clicks" not in refused
    good = json.loads((out / "good.output.json").read_text(encoding="utf-8"))
    assert good["verdict"] == "LAWFUL"
    read = good["counts"]["screen"]
    waits = [
        click["interval"] - click["birth"] for click in good["clicks"] if click["detector"] == "screen"
    ]
    first = min(waits)
    mean = (2 * sum(waits) + len(waits)) // (2 * len(waits))
    assert [pin["verdict"] for pin in good["pins"]] == [
        "MATCH" if abs(read - 2) <= 1 else "MISS",
        "MISS",
        "MATCH" if first == 1 else "MISS",
        "MISS",
        "MATCH" if abs(mean - 100) <= 60 else "MISS",
        "MISS",
    ]
    assert [pin["read"] for pin in good["pins"]] == [read, read, first, None, mean, None]
    assert [pin["kind"] for pin in good["pins"]] == [
        "count",
        "count",
        "first_click",
        "first_click",
        "mean_interval",
        "mean_interval",
    ]
