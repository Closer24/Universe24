"""Capture test simulations only when --visualize-runs is requested."""

import html
import re
from contextlib import ExitStack
from pathlib import Path
from uuid import uuid4

import pytest

RUNS = []


def pytest_addoption(parser):
    parser.addoption(
        "--visualize-runs",
        action="store_true",
        default=False,
        help="Capture simulation frames, render run reports and execute visualization tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "visualization: requires explicit --visualize-runs")


def pytest_sessionstart(session):
    xml = getattr(session.config.option, "xmlpath", None)
    if xml:
        from event_universe.retention import ArtifactLease, validate_output_path

        output = Path(xml).absolute()
        validate_output_path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.touch(exist_ok=True)
        session.config._result_lease = ArtifactLease(output.parent, [output.resolve()])


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--visualize-runs"):
        skip = pytest.mark.skip(reason="visualization requires --visualize-runs")
        for item in items:
            if "visualization" in item.keywords:
                item.add_marker(skip)


@pytest.fixture(autouse=True)
def capture_test_runs(monkeypatch, request):
    """Keep at most a few sampled frames per actual engine, without changing its inputs."""
    if not request.config.getoption("--visualize-runs"):
        yield
        return

    from event_universe.core.engine import Engine
    from event_universe.diagnostics.frames import capture_volume

    runs = {}

    def instrument(original):
        def step(world):
            key = id(world)
            if key not in runs:
                runs[key] = {
                    "world": world,
                    "frames": [],
                    "stride": 1,
                    "label": request.node.nodeid,
                }
                runs[key]["frames"].append(capture_volume(world))
            result = original(world)
            record = runs[key]
            if world.tick % record["stride"] == 0:
                record["frames"].append(capture_volume(world))
            if len(record["frames"]) > 6:
                record["frames"] = record["frames"][::2]
                record["stride"] *= 2
            return result

        return step

    monkeypatch.setattr(Engine, "step", instrument(Engine.step))
    yield
    for record in runs.values():
        final = capture_volume(record["world"])
        if record["frames"][-1].tick != final.tick:
            record["frames"].append(final)
        record.pop("world")
        RUNS.append(record)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        if session.config.getoption("--visualize-runs"):
            _write_test_runs(session, exitstatus)
    finally:
        lease = getattr(session.config, "_result_lease", None)
        if lease is not None:
            lease.finish()


def _write_test_runs(session, exitstatus):
    from event_universe.retention import ArtifactLease, validate_output_path

    root = Path("artifacts")
    output = root / "test-runs" / uuid4().hex
    validate_output_path(output)
    validate_output_path(root / "test-runs.html")
    output.mkdir(parents=True)
    summary = root / "test-runs.html"
    summary.touch(exist_ok=True)
    with ExitStack() as stack:
        stack.enter_context(ArtifactLease(output.parent, [output.absolute()]))
        stack.enter_context(ArtifactLease(root, [summary.absolute()]))
        _render_test_runs(session, exitstatus, output, summary)


def _render_test_runs(session, exitstatus, output, summary_path):
    if not session.config.getoption("--visualize-runs"):
        return

    from event_universe.diagnostics.render import render_volume

    sections = []
    for index, run in enumerate(RUNS):
        label = run["label"]
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", label)[:85]
        path = render_volume(
            run["frames"],
            output / f"{index:03d}-{slug}.html",
            title=label,
            metadata={"suite_exit_status": int(exitstatus)},
        )
        contents = path.read_text(encoding="utf-8")
        image = re.search(r"<img [^>]+>", contents).group(0)
        sections.append(f"<section><h2>{html.escape(label)}</h2>{image}</section>")
    summary = (
        f"<!doctype html><html><head><meta charset=utf-8><title>Simulation test runs</title>"
        "<style>body{font-family:system-ui;background:#111827;color:#eee;padding:24px}"
        "main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}"
        "h2{font-size:14px;overflow-wrap:anywhere}img{max-width:100%}section{background:#1f2937;padding:12px}"
        "</style></head><body><h1>Simulation test runs</h1>"
        f"<p>Exit status: {int(exitstatus)} · {len(RUNS)} runs · sampled frames; full physics in 3D</p>"
        f"<main>{''.join(sections)}</main></body></html>"
    )
    summary_path.write_text(summary, encoding="utf-8")
