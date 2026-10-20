"""The engine's repository root around every test: a test, or a helper of tests/laws.py (`world_beside`, `one_photon_board`), that points `world_files`' repository root at its own copy leaves it where it found it, so the shipped worlds load by their repository paths in the tests that follow in the same process."""

import pytest

from event_universe import world_files


@pytest.fixture(autouse=True)
def repository_root_kept():  # type: ignore[no-untyped-def]
    kept = world_files.REPOSITORY_ROOT
    yield
    world_files.REPOSITORY_ROOT = kept
