"""The helpers of the law's tests: the test pieces under tests/worlds (the toy's calibre at rim 15,162,856,759,112,389 and its settings: the 3-cube at 20 ticks, the 5-cube hole setting at 60, the chiral setting at 60), a clock built from one (`node_of`), a module loaded by its path (`load_file`), the refusal by name (`refused`), the first form of Rule3 written by hand (`arrivals_rule3`, in no file of src/), the state's integers for the rewind (`state_of`, `run_back_exact`)."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import run as record
from event_universe.assembly.piece import read_piece
from event_universe.clock import Clock
from event_universe.core.acts import carry
from event_universe.features import stretch
from event_universe.meshes import cross

WORLDS = (ROOT := Path(__file__).resolve().parents[1]) / "tests" / "worlds"


def world_of(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    return read_piece(WORLDS / name)


def node_of(name: str, **changes: Any) -> Clock:
    """A clock from a test piece, the piece's keys changed as given (a size, a setting, a count of ticks)."""
    calibre, piece = world_of(name)
    return Clock(calibre, {**piece, **changes})


def load_file(name: str, path: Path) -> Any:
    """A module loaded by its path, for a tool run as a test."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refused(match: str, call: Callable[..., Any], *args: Any, **keys: Any) -> None:
    """The call refused by name: a ValueError whose message holds the words."""
    with pytest.raises(ValueError, match=match):
        call(*args, **keys)


def arrivals_rule3(
    grips: Any, pulls: Any, hold: Any, teeth: Any, now: Any, before: Any, fine: Any
) -> tuple[Any, Any]:
    """Rule3's first form by hand: w a_next + r' = SUM_j R_j m_j + S a_now - w a_before + r, the one carry."""
    total = sum(grip * pull for grip, pull in zip(grips, pulls, strict=True))
    return carry(total + hold * now - teeth * before, teeth, fine, 1)


def state_of(clock: Clock) -> str:
    """Every notch and fine tooth of the clock's state as one text, the rewind's comparison bit for bit."""
    return record.state_text(clock) + f" {clock.ticks}"


def run_back_exact(clock: Clock, n: int) -> int:
    """The count of the n states returned exactly by n ticks forward and n back."""
    kept = []
    for _ in range(n):
        kept.append(state_of(clock))
        clock.tick()
    return sum(state_of(clock) == kept[n - 1 - k] for k in range(n) if not clock.tick(-1))


def level_at(clock: Clock, load: int) -> int:
    """The regulator's notch at a load."""
    return int(
        np.asarray(
            stretch.stretch_of(clock.full_rate, np.array([load], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )


def wronskian(three: Any, twelve: Any) -> Any:
    """The hand's bilinear W = three_now twelve_before - twelve_now three_before at every clock (the former links.wronskian, read by the tests alone)."""
    return cross(three.now, twelve.now, three.before, twelve.before)
