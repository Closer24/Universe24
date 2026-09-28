"""Test session options: the explicit visualization opt-in; every test file is collected and a living test is never skipped; the fixture of the load's hold alone for the tests of the mechanics on a chosen GameBoard state."""

import pytest

from event_universe.events import assembly


@pytest.fixture
def the_loads_hold_alone(monkeypatch):
    """A GameBoard state set by the test, diagnostic: the load's hold alone, THE START not applied (ALGEBRA.md #the-generator, THE START), so a held family is its bodies' counts at their Nodes and 0 elsewhere, the slab these tests of the mechanics (a signed read, the inverse step, the clock under content, the click's tallies) read; under the law's start that slab is at its rest before the first interval, the uniform level on a periodic chain at [1, 1]."""
    monkeypatch.setattr(assembly, "start_at_rest", lambda loop: None)


def pytest_addoption(parser):
    parser.addoption(
        "--visualize-runs",
        action="store_true",
        default=False,
        help="Execute visualization tests that render run reports",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "visualization: requires explicit --visualize-runs")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--visualize-runs"):
        skip = pytest.mark.skip(reason="visualization requires --visualize-runs")
        for item in items:
            if "visualization" in item.keywords:
                item.add_marker(skip)
