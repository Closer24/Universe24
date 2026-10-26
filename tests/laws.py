"""The helpers of the law's tests: the test worlds under tests/worlds (the toy's universe at den 15,162,856,759,112,389 and its seeds: the 3-cube at 20 intervals, the 5-cube hole seed at 60, the chiral seed at 60), a Node built from one (`node_of`), a module loaded by its path (`load_file`), the refusal by name (`refused`), the first form of Rule3 written by hand (`arrivals_rule3`, in no file of src/), the state's integers for the run back (`state_of`, `run_back_exact`)."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe.core.rule3 import carried_division
from event_universe.features import volume
from event_universe.links import cross
from event_universe.loader.world import load_world
from event_universe.node import Node

WORLDS = (ROOT := Path(__file__).resolve().parents[1]) / "tests" / "worlds"


def world_of(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    return load_world(WORLDS / name)


def node_of(name: str, **changes: Any) -> Node:
    """A Node from a test world, the world's keys changed as given (a shape, a seed, an intervals count)."""
    universe, world = world_of(name)
    return Node(universe, {**world, **changes})


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
    reads: Any, arrivals: Any, self_coefficient: Any, wall: Any, now: Any, before: Any, remainder: Any
) -> tuple[Any, Any]:
    """Rule3's first form by hand: w a_next + r' = SUM_j R_j m_j + S a_now - w a_before + r, the one carried division."""
    total = sum(read * arrival for read, arrival in zip(reads, arrivals, strict=True))
    return carried_division(total + self_coefficient * now - wall * before, wall, remainder, 1)


def state_of(node: Node) -> str:
    """Every level and remainder of the Node's state as one text, the run back's comparison bit for bit."""
    return node.state_bytes().decode() + f" {node.interval}"


def run_back_exact(node: Node, n: int) -> int:
    """The count of the n states returned exactly by n intervals forward and n back."""
    kept = []
    for _ in range(n):
        kept.append(state_of(node))
        node.step()
    return sum(state_of(node) == kept[n - 1 - k] for k in range(n) if not node.step(-1))


def level_at(node: Node, content: int) -> int:
    """The carrier's level at a content."""
    return int(
        np.asarray(
            volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )


def wronskian(re: Any, im: Any) -> Any:
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the former links.wronskian, read by the tests alone)."""
    return cross(re.now, im.now, re.before, im.before)
