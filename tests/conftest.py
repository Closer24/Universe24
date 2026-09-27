"""Test session options: the explicit visualization opt-in and the result-file leases; every test file is collected and a living test is never skipped."""

from pathlib import Path

import pytest


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
