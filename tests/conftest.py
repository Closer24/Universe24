"""Test session options: the cancelled suites never collected, explicit visualization opt-in
and result-file leases."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _cancelled_tests() -> list[str]:
    """The ray law's test files (docs/CANCELLED_WORLDS.md section 3, read by
    tools/cancelled_paths.py): the gate never collects them; a living test is never skipped
    (the Boss's records 2102 and 2133)."""
    spec = importlib.util.spec_from_file_location("cancelled_paths", ROOT / "tools/cancelled_paths.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return [path.removeprefix("tests/") for path in module.cancelled_paths("tests")]


collect_ignore = _cancelled_tests()


def pytest_addoption(parser):
    parser.addoption(
        "--visualize-runs",
        action="store_true",
        default=False,
        help="Execute visualization tests that render run reports",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "visualization: requires explicit --visualize-runs")


def pytest_sessionstart(session):
    # Under pytest-xdist only the controller writes the JUnit file; a worker
    # (config.workerinput is set) must not take the lease a second time.
    if hasattr(session.config, "workerinput"):
        return
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


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    lease = getattr(session.config, "_result_lease", None)
    if lease is not None:
        lease.finish()
