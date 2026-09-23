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
