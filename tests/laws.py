"""The helpers of the law's tests: a module loaded by its path (a tool; the generator, the back-in-time gate and the runner loaded once for every test), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`); the chain is the shortest that holds the body of 50 quanta (about eleven Nodes about its centre) and the end node_detectors with their regions apart, since the lay's cost is the start's relaxation over the chain's length squared, and every bound the tests put on the chain is per Node, the same on any length."""

import importlib.util
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import readings
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients
from event_universe.lattice import Lattice
from event_universe.loader.derived import FamilyRule, Row
from event_universe.loader.universe import universe_of
from event_universe.loader.world import World
from event_universe.records import Record

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the law's rows
CHAIN, QUANTA = (
    24,
    6,
)  # the shortest chain (x open) holding the body apart from the end node_detectors; the
# smallest body the generator lays on it in seconds (a test runs under 30 seconds, the owner's word)
CHARGED = {"name": "charged", "pair": [4000, 6000], "dimension": 2}  # matter's pair as a plane
LIGHT_ROW = {
    "name": "light",
    "pair": [6000, 6000],
    "dimension": 1,
    "reads": {},
}  # the one massless family of quanta, the seed every world is laid with (ALGEBRA.md, The uniform seed is a lay)
# the band's top as a resonance pair, cos Omega = 0; a region declares no quantum of its own
TOP = [0, 6000]
CHARGED["reads"] = {"gravity": 1, "binding": 1, "charge": 1}  # every holder, the sign's among them


def real_rows(*rows: tuple[str, tuple[int, int], int, int | None]) -> list[Row]:
    """Rows of real lines as the loader reads them (loader.derived.Row), each (name, pair, lines, level weight): one part, no plane, sourced by the form where it is held at the write weight 1, acting on the pace, and every row reading every held row among them at the weight 1 (the tests' declaration)."""
    held = tuple((name, 1) for name, _pair, _lines, weight in rows if weight is not None)
    return [Row(n, p, k, 1, False, False, False, w, w and 1, 0, held) for n, p, k, w in rows]


def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def vacuum_content(world: World, family: FamilyRule) -> int:
    """The content a record of `family` reads where nothing is laid: the declared rests of the holders its declaration names, each at its read weight (ALGEBRA.md, The vacuum content, item 22), 60 on the shipped universes with a gravity row."""
    return sum(world.families[read.family].rest * read.weight for read in family.reads)


def band_of(pair, gamma: int, content: int, unit: int, *cosines):  # type: ignore[no-untyped-def]
    """cos omega(q) in the test's floats from the line's own read at `content` (the law's (h), **L** the line's own read: 2 w cos omega(q) = S + SUM over the six Ports of R_ij cos q_a), Rule3's coefficients at the composed paces of the content with no tension; `cosines` the cos q_a of the three axes, numbers or arrays; (num / den) SUM_a cos q_a / 3 at the content 0."""
    reads, self_coefficient, wall = coefficients(
        *pair, gamma, *paces.node_paces(gamma, content), None, unit
    )
    arrived = sum(int(read) * cosines[port // 2] for port, read in enumerate(reads))
    return (int(self_coefficient) + arrived) / (2 * int(wall))


def refused(match: str, call, *args, **keys):
    with pytest.raises(ValueError, match=match) as refusal:
        call(*args, **keys)
    return refusal.value


BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")  # the back-in-time gate


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, of every family's reads too, a family's pair replaced where `pairs` names it, the charged matter row, matter's pair as a plane, added where `charged`)."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [json.loads(json.dumps(CHARGED))] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
        family["reads"] = {name: w for name, w in family["reads"].items() if name not in drop}
    if not any(  # the seed family where the universe holds no massless family of quanta, 2026-10-24
        "held" not in f and f["pair"][0] == f["pair"][1] for f in universe["families"]
    ):
        universe["families"] += [json.loads(json.dumps(LIGHT_ROW))]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")


# the builders the parts' tests share (tests/test_part_*.py; the shape of tests/: a helper imported by two files
# lives here): the turning universe's charged record by hand, the Coulomb chain, the one photon's board, a shipped
# world edited beside tmp_path, the emit-and-take world and the fold's floor
TURNING_FILE = EVENTS / "turning.json"
TURNING_INTEGERS, TURNING = universe_of(json.loads(TURNING_FILE.read_text(encoding="utf-8")))
TURNING_T, TURNING_PAIR = TURNING_INTEGERS["quantum_action"], (4000, 6000)
CHARGE = [family.name for family in TURNING].index("charge")
RULE_WALL = coefficients(*TURNING[CHARGE].pair, 6000, 6000, 6000, None, 16)[2]  # w = 6 den Gamma^2 G^2
SINE = 4472  # isqrt(6000^2 - 4000^2): the matter pair's sin omega_0 times den
COULOMB_CHAIN, COULOMB_AT, EMIT_RUN = 400, 280, 200
COULOMB_UNIVERSE = {
    "integers": {"node_clock": 6000, "quantum_action": 36000, "width": 63, "link_unit": 16},
    "families": [
        {
            "name": "charge",
            "pair": [6000, 6000],
            "reads": {},
            "held": {"sources": ["wronskian"], "level_weight": 100},
        },
        {"name": "charged", "pair": list(TURNING_PAIR), "reads": {"charge": 1}, "dimension": 2},
    ],
}  # the energy line: E_h T num = 100 x 36,000 x 4,000 = k_w Gamma den = 400 x 6,000 x 6,000
GRAVITY = {
    "name": "gravity",
    "pair": [6000, 6000],
    "reads": {"gravity": 1},
    "held": {"sources": ["form"], "level_weight": 1000, "write_weight": 1, "rest": 60},
}


ORACLE = load_file(
    "step_oracle", ROOT / "tools" / "step_oracle.py"
)  # the step's oracle: the law's first form with the one Node's interval around it
arrivals_rule3 = (
    ORACLE.arrivals_rule3
)  # the first form of Rule3, written in the tool and in no file of src/


def flux_world(tmp_path, shape, intervals=4, level_weight=1):  # type: ignore[no-untyped-def]
    """The rule's universe with the charged plane and gravity carrying the flux's odd lines, on a board."""
    universe_beside(tmp_path, charged=True)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    gravity = next(row for row in rows["families"] if row["name"] == "gravity")["held"]
    gravity["sources"], gravity["level_weight"] = ["form", "tensions", "flux"], level_weight
    (tmp_path / "u.json").write_text(json.dumps(rows), encoding="utf-8")
    world = dict(shape=list(shape), intervals=intervals)
    world.update(universe="u.json")
    (path := tmp_path / "flux.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def packet(board: Lattice, axis: int, wave: tuple[int, int], size: int, at: int) -> None:
    """A plane-wave packet of the charged family laid by hand, moving along `axis` with the wave number 2 pi wave[0] / wave[1] per Link under a raised-cosine envelope over `size` Nodes from `at`, its level before the wave advanced by the band's own rotation at the vacuum's content, z_before = z_now e^(i omega), the record of positive Wronskian moving toward +a."""
    index = [f.name for f in board.families].index(CHARGED["name"])
    family, gamma = board.families[index], board.world.node_clock
    k = 2 * np.pi * wave[0] / wave[1]
    content = vacuum_content(board.world, family)
    omega = np.arccos(band_of(family.pair, gamma, content, board.unit, np.cos(k), 1.0, 1.0))
    x = np.indices(board.shape)[axis]
    inside = (x >= at) & (x < at + size)  # a raised-cosine window: a locally plane wave
    envelope = 600 * inside * np.sin(np.pi * (x - at + 1) / (size + 1)) ** 2
    phase = k * x
    lines = [
        Record(
            np.rint(envelope * np.cos(phase)).astype(board.kind),
            np.rint(envelope * np.cos(phase + omega)).astype(board.kind),
            board.states[index].lines[0].remainder,
        ),
        Record(
            np.rint(envelope * np.sin(phase)).astype(board.kind),
            np.rint(envelope * np.sin(phase + omega)).astype(board.kind),
            board.states[index].lines[1].remainder,
        ),
    ]
    board.states[index].lines = lines


LINE_KEYS = ("now", "before", "remainder")  # a record's three arrays


def family(board: Lattice, name: str) -> int:
    return [f.name for f in board.families].index(name)


def arrays(board: Lattice) -> list[np.ndarray]:
    """Every array of the state: the lines, the write remainders and the phase pairs."""
    found = [getattr(r, k).copy() for s in board.states for r in s.lines for k in LINE_KEYS]
    found += [r.copy() for s in board.states for r in s.write_remainders]
    found += [
        getattr(r, k).copy() for s in board.states for rows in s.phases for r in rows for k in LINE_KEYS
    ]
    return found


def linear_sum(wall: int, line: Record) -> int:
    """The linear sum of one line over the board, L = SUM over the Nodes of [w (now - before) + r], w the family's wall 6 den Gamma^2 G^2 (the flux form of Rule3: w (next - 2 now + before) + r' - r = SUM over the Ports of R_ij (arrival - now) - D now, so the Link terms pair off on a closed board read at one rate and L moves by the mass term alone, zero for light); a lattice reading, no level written."""
    now, before = line.now.astype(object), line.before.astype(object)
    return int((wall * (now - before) + line.remainder.astype(object)).sum())


def linear_exchange(reads: Sequence[Any], line: Record, wrap: Wrap) -> int:
    """The change of a line's linear sum over one interval by its exchange with the board's faces, a family of light (num = den, so D = 0, at any content): -SUM over the Ports of R_ij times the Node's number over every Node whose Port arrives from beyond a face (the fill 0 there), 0 on a periodic axis; with the step's own six reads R_ij, the expected change of L where no other act writes the line, so that a jump beyond it names a level written outside Rule3's line."""
    beyond = readings.ports(np.zeros_like(line.now), wrap, 1)
    now = line.now.astype(object)
    found = 0
    for read, mask in zip(reads, beyond, strict=True):
        where = np.asarray(mask, dtype=bool)
        found += int(
            (np.broadcast_to(np.asarray(read, dtype=object), now.shape)[where] * now[where]).sum()
        )
    return -found


def weighted_linear_sum(wall: int, line: Record, weights: Any) -> int:
    """The linear sum weighted by the Node's rate, L'' = SUM over the Nodes of weight_i x [w (now - before) + r] with weight_i = scale div p_i^2, scale the least common multiple of the distinct p_i^2 on the board, so that every weight is a whole number (the caller's, no division here): R_ij / p_i^2 = 2 num Q_ij G^2 is the same at a Link's two ends whatever their rates, so the weighted Link terms of the flux form pair off on a closed board at any fixed content profile and L'' of light is kept exactly where L moves by the pairing term; a lattice reading."""
    now, before = line.now.astype(object), line.before.astype(object)
    scaled = np.broadcast_to(np.asarray(weights, dtype=object), now.shape)
    return int(((wall * (now - before) + line.remainder.astype(object)) * scaled).sum())
