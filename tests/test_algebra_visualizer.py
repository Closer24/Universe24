"""The algebra visualizer (`tools/algebra_visualizer/`, the design
docs/designs/algebra_visualizer/DESIGN.md section 9): the tool's contract
against the record it read, never a pin of a world's number.

The fixture runs are made once per session by the runner's API from two
registered worlds cheap enough for a test (series Q's `c_measured`, 100
intervals, and series L1's `mz_equal`, 80 intervals: births, splits,
records and gathers at two one-Node sets). The tests:

(1) headless, the tool writes nothing; (2) every panel is present and every
number is labelled with one of the seven kinds and a source; (3) the
readings equal the record's own totals (the tool against the file it read);
(4) the light rule's worked example satisfies the two lines, the integers
written in the design before the tool; (5) no engine and no render import
in the four modules (by `ast`) and none loaded by importing the tool; (6)
the page, under `--visualize-runs` alone: one file, parsed, the three
layers, the legend, both fingerprints, the light rule's label, the
diagnostic's title, no run of digits outside a labelled element, under 4 MB;
(7) the refusals: a missing run folder names the line that makes it; a
record without gathers fills Layer 3 with "not recorded" and does not fail.
"""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import re
import sys
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path
from types import ModuleType

import pytest

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "algebra_visualizer"
LIGHT_WORLD = ROOT / "examples" / "events" / "c_measured" / "c_measured.json"
DETECTOR_WORLD = ROOT / "examples" / "events" / "amplitude" / "mz_equal.json"
MODULES = ("record.py", "panels.py", "svg.py", "render.py")
FORBIDDEN = ("event_universe", "numpy", "matplotlib", "PIL", "playwright")


def load(name: str, path: Path) -> ModuleType:
    if str(TOOL) not in sys.path:
        sys.path.insert(0, str(TOOL))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def runs(tmp_path_factory: pytest.TempPathFactory) -> Path:
    folder = tmp_path_factory.mktemp("visualizer_runs")
    run_initialization(LIGHT_WORLD, folder / "c_measured" / "run")
    run_initialization(DETECTOR_WORLD, folder / "mz_equal" / "run")
    return folder


@pytest.fixture(scope="session")
def render() -> ModuleType:
    return load("algebra_visualizer_render", TOOL / "render.py")


@pytest.fixture(scope="session")
def panels(render: ModuleType, runs: Path) -> list:
    light, detector = render.load_pair(runs, "c_measured", "mz_equal")
    return render.build_panels(light, detector)


def test_headless_prints_and_writes_nothing(render: ModuleType, runs: Path) -> None:
    before = {p for p in runs.rglob("*")}
    out = io.StringIO()
    with redirect_stdout(out):
        assert render.main([str(runs), "--detector", "mz_equal"]) == 0
    assert {p for p in runs.rglob("*")} == before
    lines = out.getvalue().splitlines()
    assert lines and all(line.split()[0] in render.KINDS or line.startswith("(none)") for line in lines)


def test_every_panel_present_and_every_number_labelled(render: ModuleType, panels: list) -> None:
    keys = [p.key for p in panels]
    assert keys == [
        "torus",
        "node",
        "state",
        "verb_t",
        "verb_b",
        "verb_g",
        "verb_p",
        "verb_e",
        "verb_d",
        "light_rule",
        "fan",
        "pace",
        "block",
        "objects",
        "gameboard",
        "life",
        "screen",
        "clock",
        "intervals",
    ]
    assert {p.layer for p in panels} == {1, 2, 3}
    for panel in panels:
        if panel.missing:
            assert not panel.numbers
            continue
        for number in panel.numbers:
            assert number.kind in render.KINDS
            assert number.source
    rows = render.as_rows(panels)
    assert rows and all(row[3] in render.KINDS for row in rows)


def test_readings_equal_the_records_own_totals(render: ModuleType, runs: Path, panels: list) -> None:
    by_key = {p.key: p for p in panels}
    detector = runs / "mz_equal" / "run"
    light = runs / "c_measured" / "run"
    with (detector / "events.jsonl").open(encoding="utf-8") as handle:
        detector_lines = [json.loads(line) for line in handle if line.strip()]
    with (light / "events.jsonl").open(encoding="utf-8") as handle:
        light_lines = [json.loads(line) for line in handle if line.strip()]
    gathers = [line for line in detector_lines if line["event"] == "gather"]
    screen = by_key["screen"]
    assert screen.missing is None
    total = next(n for n in screen.numbers if n.label == "gathers (the records' clicks)")
    assert int(total.value) == len(gathers)
    assert sum(b["count"] for b in screen.figure["bars"]) + sum(
        b["count"] for b in screen.figure["others"]
    ) == len(gathers)
    fan = by_key["fan"]
    face_clicks = [
        line
        for line in light_lines
        if line["event"] == "click" and str(line["detector"]).startswith("face:")
    ]
    assert len(fan.figure["clicks"]) == len(face_clicks)
    assert next(n for n in fan.numbers if n.label == "the face clicks").value == str(len(face_clicks))
    meta = json.loads((detector / "run.json").read_text(encoding="utf-8"))
    audit = meta["audit"][-1]
    books = by_key["gameboard"]
    balanced = next(n for n in books.numbers if n.label == "the books balanced")
    assert balanced.value == str(audit["balanced"]) and balanced.kind == "GAMEBOARD"


def test_the_light_rules_worked_example(render: ModuleType) -> None:
    panels_module = sys.modules["panels"]
    example = panels_module.LIGHT_RULE_EXAMPLE
    s6 = sum(example["neighbours"].values())
    assert s6 == example["S_6"]
    a_before, r = example["a_before"], example["r"]
    light = example["light"]
    assert 3 * light["a_next"] + light["r_next"] == s6 - 3 * a_before + r
    assert 0 <= light["r_next"] < 3
    num, den = example["massive"]["pair"]
    massive = example["massive"]
    assert 3 * den * massive["a_next"] + massive["r_next"] == num * s6 - 3 * den * a_before + r
    assert 0 <= massive["r_next"] < 3 * den


def test_no_engine_and_no_render_import(render: ModuleType) -> None:
    for name in MODULES:
        tree = ast.parse((TOOL / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for imported in names:
                assert imported.split(".")[0] not in FORBIDDEN, f"{name} imports {imported}"
    # The test module itself imports the runner; the tool's own modules must not.
    for module_name in ("algebra_visualizer_render", "panels", "svg", "record"):
        module = sys.modules[module_name]
        for attr in vars(module).values():
            if isinstance(attr, ModuleType):
                assert attr.__name__.split(".")[0] not in FORBIDDEN, (
                    f"{module_name} loaded {attr.__name__}"
                )


class _Digits(HTMLParser):
    """Every run of digits in the page's text must sit under an element that
    carries `data-kind` (a number with its kind) or `data-ref` (a section, a
    file or a SHA referenced); style, script and title text are not numbers."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, bool]] = []
        self.unlabelled: list[str] = []
        self.labelled = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        if tag in ("br", "input", "img", "meta", "link", "hr"):
            return
        self.stack.append((tag, "data-kind" in found or "data-ref" in found))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if any(tag in ("style", "script", "title") for tag, _ in self.stack):
            return
        if re.search(r"\d", data):
            if any(ok for _, ok in self.stack):
                self.labelled += 1
            else:
                self.unlabelled.append(data.strip()[:60])


@pytest.mark.visualization
def test_the_page(render: ModuleType, runs: Path, tmp_path: Path) -> None:
    out = tmp_path / "page.html"
    assert render.main([str(runs), "--detector", "mz_equal", "--render", str(out)]) == 0
    assert [p.name for p in tmp_path.iterdir()] == ["page.html"]
    text = out.read_text(encoding="utf-8")
    assert out.stat().st_size < 4 * 1024 * 1024
    for needle in (
        "The geometry that is the algebra",
        "How it produces the physics",
        "The clicks",
        "not from a run",
        "GAMEBOARD, a diagnostic",
    ):
        assert needle in text
    for kind in render.KINDS:
        assert f'class="badge k-{kind}"' in text
    for name in ("c_measured", "mz_equal"):
        meta = json.loads((runs / name / "run" / "run.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] in text and meta["initialization_sha256"] in text
    parser = _Digits()
    parser.feed(text)
    assert parser.labelled > 100
    assert parser.unlabelled == []


def test_a_missing_run_is_refused_with_the_line_that_makes_it(
    render: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert render.main([str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "tools/run_series.py" in err and "no run record" in err


def test_a_record_without_gathers_fills_layer_3_with_not_recorded(
    render: ModuleType, runs: Path, tmp_path: Path
) -> None:
    source = runs / "mz_equal" / "run"
    trimmed = tmp_path / "trimmed" / "run"
    trimmed.mkdir(parents=True)
    for name in ("run.json", "state.json", "initialization.json"):
        (trimmed / name).write_bytes((source / name).read_bytes())
    with (source / "events.jsonl").open(encoding="utf-8") as handle:
        kept = [
            line
            for line in handle
            if '"event": "gather"' not in line and '"event": "record"' not in line
        ]
    (trimmed / "events.jsonl").write_text("".join(kept), encoding="utf-8")
    light, detector = render.load_pair(runs, "c_measured", "c_measured")
    detector = render.load_run(trimmed)
    panels = render.build_panels(light, detector)
    by_key = {p.key: p for p in panels}
    for key in ("life", "screen", "clock", "intervals", "verb_b", "verb_g", "verb_e"):
        assert by_key[key].missing, key
        assert not by_key[key].numbers


# --- the 3-D page of one run (DESIGN_3D.md section 7) -------------------------

MODULES_3D = MODULES + ("board3d.py",)
RUN_KEYS = [
    "alg_board",
    "alg_families",
    "alg_blocks",
    "alg_instruments",
    "alg_verbs",
    "board",
    "board_objects",
    "board_cells",
    "board_snapshot",
    "out_records",
    "out_clock",
    "out_intervals",
    "out_pattern",
]


def write_new_engine_record(folder: Path) -> None:
    """The new engine's record built by hand from the keys its engine writes on
    the branch detector-law-build at 2f44797c (DESIGN_3D.md section 5.3 and
    Finding 3): a chain of 40 Nodes, a lamp of light at 2, a screen at 36, one
    block of the massive kind of side 3 at the corner 12 stepping at the
    intervals 3, 6 and 9, its self-click at 35, two gathers at the screen, a
    probe per interval, the snapshot with the block's rows and one live record.
    The integers are a fixture of the tool's contract, not a number of a world."""
    folder.mkdir(parents=True)
    world = {
        "law": "beam",
        "model_id": "beam-massive-record-fixture-v1",
        "shape": [40, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 12,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "probes": [[20, 0, 0], [30, 0, 0]],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "matter", "quantum": 1, "pair": [800, 809], "faces": {"x": "open"}},
        ],
        "measured": [
            {
                "position": [2, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[1, 0, 0]],
                "lamp": {"rate": [1, 1], "wheel": [2531, 4096], "directions": [[1, 0, 0]], "train": 4},
            },
            {
                "position": [12, 0, 0],
                "family": "matter",
                "amount": 1,
                "phase": 0,
                "momentum": [64, 0, 0],
                "fixed": True,
                "side": 3,
                "charge": 0,
                "spin": [0, 0, 0],
                "moment": [0, 0, 0],
                "pair": [800, 800],
                "coupling": {"G": [1, 1], "g": [1, 500]},
                "seed": 5,
            },
            {
                "position": [36, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[-1, 0, 0]],
            },
        ],
        "detectors": [{"name": "screen", "positions": [[36, 0, 0]], "threshold": 1}],
    }
    (folder / "initialization.json").write_text(json.dumps(world), encoding="utf-8")
    families_meta = [
        {
            "name": "light",
            "quantum": 1,
            "charge": [0, 1],
            "phase": True,
            "phase_per_link": [77, 25],
            "lifetime": None,
            "pair": [1, 1],
            "faces": {"x": "open", "y": "periodic", "z": "periodic"},
        },
        {
            "name": "matter",
            "quantum": 1,
            "charge": [0, 1],
            "phase": True,
            "phase_per_link": 0,
            "lifetime": None,
            "pair": [800, 809],
            "faces": {"x": "open", "y": "periodic", "z": "periodic"},
        },
    ]
    corners = [[12, 0, 0]] * 2 + [[13, 0, 0]] * 3 + [[14, 0, 0]] * 3 + [[15, 0, 0]] * 4
    audit = []
    transit, measured_content = [], []
    for tick in range(1, 13):
        audit.append(
            {
                "tick": tick,
                "families": {
                    "light": {
                        "measured": {
                            "initial": 2,
                            "measured": 0,
                            "became": 0,
                            "current": 1,
                            "spent": 1,
                            "escaped": 0,
                            "balanced": True,
                        },
                        "transit": {
                            "initial": 0,
                            "released": 1,
                            "current": 1,
                            "absorbed": 0,
                            "escaped": 0,
                            "balanced": True,
                        },
                        "form": 1000 + tick,
                    },
                    "matter": {
                        "measured": {
                            "initial": 1,
                            "measured": 0,
                            "became": 0,
                            "current": 1,
                            "spent": 0,
                            "escaped": 0,
                            "balanced": True,
                        },
                        "transit": {
                            "initial": 0,
                            "released": 0,
                            "current": 0,
                            "absorbed": 0,
                            "escaped": 0,
                            "balanced": True,
                        },
                        "form": 302442,
                    },
                },
                "momentum": {"held": [64, 0, 0], "transit": [0, 0, 0], "escaped": [0, 0, 0]},
                "records": 2,
                "balanced": True,
            }
        )
        transit.append([1, 0])
        measured_content.append([1, 1])
    meta = {
        "package_version": "0.3.1",
        "source_sha256": "f" * 64,
        "initialization_sha256": "e" * 64,
        "law": "beam-v1",
        "model": "beam-massive-record-fixture-v1",
        "shape": [40, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": [0, 1],
        "width": 1,
        "clock_stamp": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "omit_row_clicks": True,
        "hypotheses": ["amplitude-v1", "detector-law-v1", "massive-record-v1"],
        "families": families_meta,
        "numbers": {
            "1": {
                "position": [2, 0, 0],
                "family": "light",
                "span": [1, 1, 1],
                "phase_by_momentum": False,
                "become": None,
            },
            "2": {
                "position": [12, 0, 0],
                "family": "matter",
                "span": [1, 1, 1],
                "phase_by_momentum": False,
                "become": None,
            },
            "3": {
                "position": [36, 0, 0],
                "family": "light",
                "span": [1, 1, 1],
                "phase_by_momentum": False,
                "become": None,
            },
        },
        "status": "completed",
        "error": None,
        "requested_ticks": 12,
        "completed_ticks": 12,
        "tick": 12,
        "elapsed_seconds": 0.01,
        "conserved_at_every_completed_tick": True,
        "audit": audit,
        "measured_content": measured_content,
        "transit_content": transit,
        "momentum": [{"held": [64, 0, 0], "transit": [0, 0, 0], "escaped": [0, 0, 0]}] * 12,
        "measured": [
            {"number": 0, "position": [2, 0, 0], "family": "light", "held": [0, 0]},
            {"number": 1, "position": [12, 0, 0], "family": "matter", "held": [0, 1]},
            {"number": 2, "position": [36, 0, 0], "family": "light", "held": [1, 0]},
        ],
        "detectors": [{"name": "screen", "positions": [[36, 0, 0]], "clicks": 2}],
        "escaped": [
            {"family": "light", "amount": 0, "content": 0, "momentum": [0, 0, 0]},
            {"family": "matter", "amount": 0, "content": 0, "momentum": [0, 0, 0]},
        ],
        "display": "none",
        "world": [],
        "open": [],
        "layer": {"law": "detector-law-v1", "born": 2, "gathered": 2, "open": 0},
    }
    (folder / "run.json").write_text(json.dumps(meta), encoding="utf-8")
    lines: list[dict] = [
        {
            "event": "birth",
            "tick": 1,
            "node": [2, 0, 0],
            "measured": 0,
            "family": "light",
            "record": 1,
            "u": 0,
            "labels": [[0, 1]],
            "arms": 1,
            "units": 1,
            "multiplicity": 1,
            "train": 104,
            "clock": 1,
        },
        {
            "event": "birth",
            "tick": 2,
            "node": [2, 0, 0],
            "measured": 0,
            "family": "light",
            "record": 2,
            "u": 1,
            "labels": [[0, 1]],
            "arms": 1,
            "units": 1,
            "multiplicity": 1,
            "train": 104,
            "clock": 2,
        },
    ]
    for tick in range(1, 13):
        lines.append(
            {
                "event": "block",
                "tick": tick,
                "measured": 1,
                "corner": corners[tick - 1],
                "sum": 10 + tick,
                "clock": 0 if tick < 11 else 1,
                "steps": [12, 13, 14, 15].index(corners[tick - 1][0]),
            }
        )
        lines.append({"event": "probe", "tick": tick, "values": [tick, -tick]})
    lines.append(
        {
            "event": "gather",
            "tick": 8,
            "arrived": 8,
            "family": "light",
            "record": 1,
            "u": 0,
            "born": 1,
            "chosen": [["screen", 0, "0"]],
            "node": [[36, 0, 0]],
            "windows": [],
            "content": 1,
            "momentum": [64, 0, 0],
            "weight": [1, 1],
            "total": [1, 1],
            "unit": 1,
            "T": 1,
            "before": 1,
            "after": 1,
            "cells": [[[["screen", 0, "0"]], 64]],
            "birth": 1,
            "click": 7,
            "clock": 7,
        }
    )
    lines.append(
        {
            "event": "click",
            "tick": 11,
            "node": [15, 0, 0],
            "measured": 1,
            "family": "matter",
            "record": 4294967296,
            "cycle": 1,
            "clock": 1,
        }
    )
    lines.append(
        {
            "event": "gather",
            "tick": 12,
            "arrived": 12,
            "family": "light",
            "record": 2,
            "u": 1,
            "born": 2,
            "chosen": [["screen", 0, "0"]],
            "node": [[36, 0, 0]],
            "windows": [],
            "content": 1,
            "momentum": [64, 0, 0],
            "weight": [1, 1],
            "total": [1, 1],
            "unit": 1,
            "T": 1,
            "before": 1,
            "after": 1,
            "cells": [[[["screen", 0, "0"]], 64]],
            "birth": 2,
            "click": 11,
            "clock": 11,
        }
    )
    (folder / "events.jsonl").write_text(
        "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
    )
    rows = [0] * 40
    for x in range(15, 18):
        rows[x] = 3 - (x - 15)
    state = {
        "law": "detector-law-v1",
        "tick": 12,
        "measured": meta["measured"],
        "blocks": [
            {
                "measured": 1,
                "family": "matter",
                "corner": [15, 0, 0],
                "side": 3,
                "charge": 0,
                "spin": [0, 0, 0],
                "moment": [0, 0, 0],
                "clock": 1,
                "steps": 3,
                "drive": [8, 0, 0],
                "momentum": [64, 0, 0],
                "responses": 0,
                "emitted": [],
                "rows": rows,
                "form": 302442,
            }
        ],
        "records": [
            {
                "record": 4294967296,
                "lamp": 1,
                "family": "matter",
                "u": 0,
                "born": 0,
                "birth": 0,
                "age": 12,
                "train": 0,
                "norm": 0,
                "absorbed": 0,
                "pointers": {
                    "measured:0": 0,
                    "measured:1": 0,
                    "measured:2": 0,
                    "screen": 0,
                    "face:-x": 0,
                    "face:+x": 0,
                },
                "form": 302442,
            }
        ],
    }
    (folder / "state.json").write_text(json.dumps(state), encoding="utf-8")


@pytest.fixture(scope="session")
def new_run(tmp_path_factory: pytest.TempPathFactory) -> Path:
    folder = tmp_path_factory.mktemp("new_engine") / "fixture_chain" / "run"
    write_new_engine_record(folder)
    return folder


@pytest.fixture(scope="session")
def old_run(runs: Path) -> Path:
    return runs / "mz_equal" / "run"


def _load_lines(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _ints_of(value: object, found: set[int]) -> None:
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        found.add(value)
    elif isinstance(value, list):
        for item in value:
            _ints_of(item, found)
    elif isinstance(value, dict):
        for item in value.values():
            _ints_of(item, found)


def _printed_ints(panels: list) -> set[int]:
    found: set[int] = set()
    for panel in panels:
        for number in panel.numbers:
            found.update(int(v) for v in re.findall(r"-?\d+", number.value))
        rows = panel.figure.get("rows") if panel.figure.get("kind") == "table" else None
        for row in rows or []:
            for value, _kind, _source in row:
                found.update(int(v) for v in re.findall(r"-?\d+", value))
    return found


def test_the_engine_is_told_from_hypotheses(
    render: ModuleType, old_run: Path, new_run: Path, tmp_path: Path
) -> None:
    record = sys.modules["record"]
    assert render.load_one(old_run).engine == record.ENGINE_OLD
    new = render.load_one(new_run)
    assert new.engine == record.ENGINE_NEW and new.is_new and new.massive
    assert not render.load_one(old_run).massive
    bare = tmp_path / "bare"
    bare.mkdir()
    for name in ("events.jsonl", "state.json", "initialization.json"):
        (bare / name).write_bytes((new_run / name).read_bytes())
    meta = json.loads((new_run / "run.json").read_text(encoding="utf-8"))
    del meta["hypotheses"]
    (bare / "run.json").write_text(json.dumps(meta), encoding="utf-8")
    with pytest.raises(SystemExit, match="hypotheses"):
        _engine = render.load_one(bare).engine


def test_one_run_headless_writes_nothing(render: ModuleType, old_run: Path, new_run: Path) -> None:
    for folder in (old_run, new_run):
        before = {p for p in folder.rglob("*")}
        out = io.StringIO()
        with redirect_stdout(out):
            assert render.main([str(folder)]) == 0
        assert {p for p in folder.rglob("*")} == before
        lines = out.getvalue().splitlines()
        assert lines and lines[0].startswith("(engine)")
        assert all(
            line.split()[0] in render.KINDS or line.startswith(("(none)", "(table)", "(engine)"))
            for line in lines
        )


def test_one_run_every_panel_present_and_every_number_labelled(
    render: ModuleType, old_run: Path, new_run: Path
) -> None:
    for folder in (old_run, new_run):
        run = render.load_one(folder)
        board, board_panels = render.build_layer(run)
        panels = render.build_run_panels(run, board_panels)
        assert [p.key for p in panels] == RUN_KEYS
        assert {p.layer for p in panels} == {1, 2, 3}
        for panel in panels:
            if panel.missing:
                assert not panel.numbers
                continue
            for number in panel.numbers:
                assert number.kind in render.KINDS and number.source
            for row in panel.figure.get("rows", []) if panel.figure.get("kind") == "table" else []:
                for _value, kind, source in row:
                    assert kind in render.KINDS and source
        by_key = {p.key: p for p in panels}
        assert by_key["board"].figure["kind"] == "board3d"
        assert board["ticks"] == run.ticks
        in_json: set[int] = set()
        _ints_of(board, in_json)
        printed = _printed_ints(panels)
        # every integer of the board's data is printed once with its kind (DESIGN_3D.md 6.3);
        # the cap and the interval count are HOST and GAMEBOARD numbers of the board panel
        missing = sorted(v for v in in_json if v not in printed)
        assert missing == [], (
            f"{run.name}: integers of the board's JSON not printed with a kind: {missing[:20]}"
        )


def test_one_run_readings_equal_the_records_own_totals(
    render: ModuleType, old_run: Path, new_run: Path
) -> None:
    for folder in (old_run, new_run):
        run = render.load_one(folder)
        board, board_panels = render.build_layer(run)
        panels = render.build_run_panels(run, board_panels)
        by_key = {p.key: p for p in panels}
        lines = _load_lines(folder / "events.jsonl")
        gathers = [line for line in lines if line["event"] == "gather"]
        chosen: dict[str, int] = {}
        for g in gathers:
            chosen[g["chosen"][0][0]] = chosen.get(g["chosen"][0][0], 0) + 1
        pattern = by_key["out_pattern"]
        total = next(n for n in pattern.numbers if n.label == "gathers (the records' clicks)")
        assert int(total.value) == len(gathers)
        assert sum(b["count"] for b in pattern.figure["bars"]) + sum(
            o["count"] for o in pattern.figure["others"]
        ) == len(gathers)
        for name, count in chosen.items():
            assert board["counts"][name][-1][1] == count
        meta = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        state = json.loads((folder / "state.json").read_text(encoding="utf-8"))
        if run.is_new:
            for entry in meta["detectors"]:
                printed = next(
                    n
                    for n in by_key["out_records"].numbers
                    if n.label == f"{entry['name']}: clicks (the gathers whose chosen cell it is)"
                )
                assert int(printed.value) == entry["clicks"] == chosen.get(entry["name"], 0)
            for block in state["blocks"]:
                obj = next(
                    o for o in board["objects"] if o["name"] == f"block measured:{block['measured']}"
                )
                assert obj["positions"][-1][1] == block["corner"]
                assert (
                    obj["steps"]
                    == [
                        line
                        for line in lines
                        if line["event"] == "block" and line["measured"] == block["measured"]
                    ][-1]["steps"]
                )
            assert sum(c[3] for c in board["snapshot"]["cells"]) == sum(state["blocks"][0]["rows"])
        else:
            for body in state["measured"]:
                obj = next(o for o in board["objects"] if o["name"] == f"body {body['number']}")
                assert obj["positions"][-1][1] == body["position"]
            rows_total = sum(
                int(ray["amount"])
                for node in state["nodes"]
                for fam in node["families"]
                for ray in fam["rays"]
            )
            assert sum(c[3] for c in board["snapshot"]["cells"]) == rows_total
        assert board["books"]["transit"][-1] == meta["transit_content"][-1]
        assert board["books"]["measured"][-1] == meta["measured_content"][-1]
        key = "clock" if all("clock" in g for g in gathers) else ("click" if run.is_new else "tick")
        ticks = sorted(int(g[key]) for g in gathers)
        diffs = [b - a for a, b in zip(ticks[:-1], ticks[1:], strict=True)]
        assert by_key["out_intervals"].figure["values"] == diffs


def test_one_run_a_body_moves_by_its_step_lines(
    render: ModuleType, old_run: Path, tmp_path: Path
) -> None:
    """A `step` line built by hand from cart_k5's recorded form (DESIGN_3D.md
    section 7): body 1 of the fixture moves at tick 5 from its position to the
    next Node; the object stands there from tick 5 and nowhere between."""
    copy = tmp_path / "stepping" / "run"
    copy.mkdir(parents=True)
    for name in ("run.json", "state.json", "initialization.json"):
        (copy / name).write_bytes((old_run / name).read_bytes())
    meta = json.loads((old_run / "run.json").read_text(encoding="utf-8"))
    origin = meta["numbers"]["1"]["position"]
    to = [origin[0] + 1, origin[1], origin[2]]
    step = {
        "event": "step",
        "tick": 5,
        "number": 1,
        "node": origin,
        "to": to,
        "momentum": [70506183131328, 0, 0],
        "phase": 3,
        "drive": [201326848, 0, 0],
        "step_port": 0,
        "last_step_port": -1,
    }
    (copy / "events.jsonl").write_text(
        (old_run / "events.jsonl").read_text(encoding="utf-8") + json.dumps(step) + "\n",
        encoding="utf-8",
    )
    run = render.load_one(copy)
    board, _panels = render.build_layer(run)
    obj = next(o for o in board["objects"] if o["name"] == "body 1")
    assert obj["positions"] == [[0, origin], [5, to]]
    assert any(m[0] == 5 and m[1] == "step" and [m[2], m[3], m[4]] == to for m in board["marks"])


def test_one_run_refusals(render: ModuleType, old_run: Path, new_run: Path, tmp_path: Path) -> None:
    # a record without gathers fills the Outside with "not recorded" and does not fail
    trimmed = tmp_path / "trimmed" / "run"
    trimmed.mkdir(parents=True)
    for name in ("run.json", "state.json", "initialization.json"):
        (trimmed / name).write_bytes((new_run / name).read_bytes())
    kept = [
        line
        for line in (new_run / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if '"gather"' not in line
    ]
    (trimmed / "events.jsonl").write_text("\n".join(kept) + "\n", encoding="utf-8")
    run = render.load_one(trimmed)
    panels = render.build_run(run)
    by_key = {p.key: p for p in panels}
    for key in ("out_clock", "out_intervals", "out_pattern"):
        assert by_key[key].missing and not by_key[key].numbers, key
    # a run of the new engine without blocks in its snapshot draws no cube and does not fail
    bare = tmp_path / "no_blocks" / "run"
    bare.mkdir(parents=True)
    for name in ("run.json", "events.jsonl"):
        (bare / name).write_bytes((new_run / name).read_bytes())
    world = json.loads((new_run / "initialization.json").read_text(encoding="utf-8"))
    world["measured"] = [e for e in world["measured"] if "side" not in e]
    (bare / "initialization.json").write_text(json.dumps(world), encoding="utf-8")
    state = json.loads((new_run / "state.json").read_text(encoding="utf-8"))
    del state["blocks"]
    (bare / "state.json").write_text(json.dumps(state), encoding="utf-8")
    run = render.load_one(bare)
    board, board_panels = render.build_layer(run)
    assert board["objects"] == [] and board["snapshot"]["count"] == 0
    panels = render.build_run_panels(run, board_panels)
    by_key = {p.key: p for p in panels}
    assert by_key["board_objects"].missing and by_key["alg_blocks"].missing
    # a folder without the four files names the runner's line
    assert render.main([str(tmp_path / "nothing")]) == 2


def test_no_engine_import_in_the_3d_module(render: ModuleType) -> None:
    tree = ast.parse((TOOL / "board3d.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        for imported in names:
            assert imported.split(".")[0] not in FORBIDDEN, f"board3d.py imports {imported}"
    module = sys.modules["board3d"]
    for attr in vars(module).values():
        if isinstance(attr, ModuleType):
            assert attr.__name__.split(".")[0] not in FORBIDDEN


@pytest.mark.visualization
def test_the_3d_page(render: ModuleType, old_run: Path, new_run: Path, tmp_path: Path) -> None:
    explor = tmp_path / "EXPLORATORY_chain" / "run"
    explor.mkdir(parents=True)
    for name in ("run.json", "events.jsonl", "state.json", "initialization.json"):
        (explor / name).write_bytes((new_run / name).read_bytes())
    for index, folder in enumerate((old_run, new_run, explor)):
        out = tmp_path / f"page_{index}.html"
        assert render.main([str(folder), "--render", str(out)]) == 0
        text = out.read_text(encoding="utf-8")
        assert out.stat().st_size < 8 * 1024 * 1024
        for needle in (
            "The algebra",
            "The GameBoard, the Inside: a diagnostic, never a measurement",
            "The Outside: the clicks",
            "GAMEBOARD, a diagnostic",
            "keeps no",
            "data-board-json",
        ):
            assert needle in text, needle
        assert (
            "<script src" not in text
            and "<link" not in text
            and "http" not in text.split("<title>")[1].split("</title>")[0]
        )
        meta = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        assert meta["source_sha256"] in text and meta["initialization_sha256"] in text
        blob = re.search(r'<script type="application/json" data-board-json>(.*?)</script>', text, re.S)
        assert blob is not None
        board = json.loads(blob.group(1).replace("<\\/", "</"))
        assert board["ticks"] == meta["completed_ticks"]
        parser = _Digits()
        parser.feed(text)
        assert parser.labelled > 50
        assert parser.unlabelled == []
        if folder is explor:
            assert text.count("EXPLORATORY") >= len(RUN_KEYS) + 1 and "<title>EXPLORATORY:" in text
        else:
            assert "EXPLORATORY" not in text
    assert sorted(p.name for p in tmp_path.iterdir() if p.is_file()) == [
        "page_0.html",
        "page_1.html",
        "page_2.html",
    ]
