"""Part A, gravity's odd lines in the fold form (ALGEBRA.md, The clock family on the Ports; the two hands' joint line of 2026-10-09): a holder of the content declaring the source `flux` carries three odd lines after its tension lines, written by the count's flux through the axis's two Links summed unhalved over twice the count's wall, and every plane reading it has each Link's read folded into the pair (X^c, X^s) with X^s_ji = -X^s_ij; without the key the engine is bit for bit the frozen one."""

import json
import lzma
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe import node, world_files
from event_universe.core import paces
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.loader.derived import folds
from event_universe.plane import link_pairs, odd_links
from event_universe.world_files import load_world
from tests import laws
from tests.laws import CHARGED, EVENTS, universe_beside

ORACLE = Path(__file__).resolve().parent / "oracle" / "two_slits.look.json.xz"
KEYS = ("now", "before", "remainder")


def flux_world(tmp_path, shape, boundary, intervals=4, level_weight=1):  # type: ignore[no-untyped-def]
    """The rule's universe with the charged plane and gravity carrying the flux's odd lines, on a board."""
    universe_beside(tmp_path, charged=True)
    rows = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    gravity = next(row for row in rows["families"] if row["name"] == "gravity")["held"]
    gravity["sources"], gravity["level_weight"] = ["form", "tensions", "flux"], level_weight
    (tmp_path / "u.json").write_text(json.dumps(rows), encoding="utf-8")
    world = dict(shape=list(shape), boundary=boundary, face_depth=1, intervals=intervals)
    world.update(universe="u.json", engine="e.json", bodies=[], node_detectors=[])
    (path := tmp_path / "flux.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def packet(board: Lattice, axis: int, wave: tuple[int, int], size: int, at: int) -> None:
    """A plane-wave packet of the charged family laid by hand, moving along `axis` with the wave number 2 pi wave[0] / wave[1] per Link under a raised-cosine envelope over `size` Nodes from `at`, its level before the wave advanced by the band's own rotation at the vacuum's content, z_before = z_now e^(i omega), the record of positive Wronskian moving toward +a."""
    index = [f.name for f in board.families].index(CHARGED["name"])
    family, gamma = board.families[index], board.world.node_clock
    k = 2 * np.pi * wave[0] / wave[1]
    content = laws.vacuum_content(board.world, family)
    omega = np.arccos(laws.band_of(family.pair, gamma, content, board.unit, np.cos(k), 1.0, 1.0))
    x = np.indices(board.shape)[axis]
    inside = (x >= at) & (x < at + size)  # a raised-cosine window: a locally plane wave
    envelope = 600 * inside * np.sin(np.pi * (x - at + 1) / (size + 1)) ** 2
    phase = k * x
    lines = [
        node.Record(
            np.rint(envelope * np.cos(phase)).astype(board.kind),
            np.rint(envelope * np.cos(phase + omega)).astype(board.kind),
            board.states[index].lines[0].remainder,
        ),
        node.Record(
            np.rint(envelope * np.sin(phase)).astype(board.kind),
            np.rint(envelope * np.sin(phase + omega)).astype(board.kind),
            board.states[index].lines[1].remainder,
        ),
    ]
    board.states[index].lines = lines


def arrays(board: Lattice) -> list[np.ndarray]:
    return [getattr(r, k).copy() for s in board.states for r in s.lines for k in KEYS] + [
        r.copy() for s in board.states for r in s.write_remainders
    ]


def test_without_flux_the_step_is_bit_identical(monkeypatch):
    """(a) The two slits world of light.json, no `flux` declared, stepped for 20 intervals: every family's level now equals the frozen engine's look file frame by frame (the oracle recorded before Part A), so the code path without a flux holder is the engine of 441b2399 bit for bit; and no family of the shipped universes is folded."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    look = json.loads(lzma.open(ORACLE).read())
    board = Lattice(load_world(EVENTS / "two_slits" / "two_slits.json"))
    assert not any(folds(board.families, i) for i in range(len(board.families)))
    for interval in range(21):
        frame = look["frames"][interval]
        assert frame["interval"] == interval and tuple(frame["shape"]) == board.shape
        for index, family in enumerate(board.families):
            recorded = frame["families"][family.name]["now" if family.quanta else "level"]
            flat = np.zeros(board.shape, dtype=object).reshape(-1)
            if isinstance(recorded, dict):
                flat[recorded["at"]] = recorded["values"]
            else:
                flat = np.array(recorded, dtype=object).reshape(-1)
            assert np.array_equal(flat.reshape(board.shape), board.states[index].lines[0].now), (
                interval,
                family.name,
            )
        board.step()


def test_the_odd_line_is_odd(tmp_path, monkeypatch):
    """(b) On a periodic cube of 7^3 with a packet moving along +x: after eight intervals the x odd line is written and nonzero, V_ji = -V_ij on every Link (the +a Port's read at i equals minus the -a Port's read at i + a) and X^s_ji = -X^s_ij exactly, the Link quantity read the same size from both ends with the opposite sign; the vector test: the same packet laid along +y gives the same state transposed bit for bit, every line of every family, the odd lines as a vector (the three axes alike, the step knowing no axis and no name)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (7, 7, 7), dict(x="periodic", y="periodic", z="periodic"))
    boards = []
    for axis in (0, 1):
        board = Lattice(load_world(world))
        packet(board, axis, (1, 4), 3, 2)
        for _ in range(8):
            board.step()
        boards.append(board)
    board = boards[0]
    index = [f.name for f in board.families].index(CHARGED["name"])
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert (
        gravity.lines[4].now.any() and not gravity.lines[5].now.any() and not gravity.lines[6].now.any()
    )
    links = odd_links(index, board.families, board.states, 1, board.wrap)
    content, factors = board.read(index)
    pairs = link_pairs(board.families[index].pair, board.world.node_clock, content, factors, links, None)
    assert pairs is not None
    odd = pairs[1]
    pace = paces.link_pace_of(board.world.node_clock, content)
    assert links is not None and any(np.asarray(link).any() for link in links)
    for axis in range(3):
        ahead, behind = links[2 * axis], np.roll(links[2 * axis + 1], -1, axis)
        assert np.array_equal(ahead, -behind)
        sizes = [odd[2 * axis] // (pace * pace), np.roll(odd[2 * axis + 1] // (pace * pace), -1, axis)]
        assert np.array_equal(sizes[0], -sizes[1]) and (axis > 0 or np.asarray(sizes[0]).any())
    axes = (1, 0, 2)
    for state, other in zip(boards[0].states, boards[1].states, strict=True):
        lines = list(state.lines)
        if len(lines) == 7:  # the odd lines and the tension lines as vectors: x and y exchanged
            lines = [lines[0], lines[2], lines[1], lines[3], lines[5], lines[4], lines[6]]
        for line, image in zip(lines, other.lines, strict=True):
            for key in KEYS:
                assert np.array_equal(np.transpose(getattr(line, key), axes), getattr(image, key))


def test_the_back_step_is_exact_with_the_fold(tmp_path, monkeypatch):
    """(c) A chain of 25 with a flux holder and a moving packet: 30 intervals forward and 30 back by `step_inverse`, every line's two levels and remainder and every write remainder bit for bit, the fold's pair recomputed from the held rows' levels at each interval's start."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (25, 1, 1), dict(x="periodic", y="periodic", z="periodic"))
    board = Lattice(load_world(world))
    packet(board, 0, (1, 4), 7, 3)
    begun = arrays(board)
    for _ in range(30):
        board.step()
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    assert gravity.lines[4].now.any()  # the odd line was written along the packet's way
    for _ in range(30):
        board.step_inverse()
    assert all(np.array_equal(a, b) for a, b in zip(begun, arrays(board), strict=True))


def test_the_one_link_reach_with_the_fold(tmp_path, monkeypatch):
    """(d) The dependency radius under the fold: on a chain of 9 with a flux holder and every line at random levels (the odd lines among them), a difference two Links from the centre leaves the centre's NodeState bit for bit after one interval and a difference one Link away reaches it."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (9, 1, 1), dict(x="open", y="periodic", z="periodic"))

    def state(far: int) -> Lattice:
        board, draw = Lattice(load_world(world)), np.random.default_rng(3)
        for index, (family, kept) in enumerate(zip(board.families, board.states, strict=True)):
            low = 0 if family.held and not family.wronskian else -60
            picks = [draw.integers(low, 60, (3, *board.shape)) for _ in kept.lines]
            kept.lines = [node.Record(now, before, np.abs(r)) for now, before, r in picks]
            if family.axes:  # the tension lines at 0, the odd lines at their random levels
                kept.lines[1:4] = [node.empty_record(board.shape, board.kind) for _ in range(3)]
            kept.write_remainders = [draw.integers(0, wall, board.shape) for wall in board.walls(index)]
            for array in [*(getattr(r, k) for r in kept.lines for k in KEYS), *kept.write_remainders]:
                array[4 + far, 0, 0] += 7 * bool(far)
        return board

    def centre(board: Lattice) -> list[int]:
        return [int(a[4, 0, 0]) for a in arrays(board)]

    (same := state(0)).step()
    assert any(np.asarray(v).any() for v in odd_links(4, same.families, same.states, 1, same.wrap))
    for far, reaches in ((1, True), (2, False)):
        (other := state(far)).step()
        assert (centre(other) != centre(same)) is reaches, far


def test_the_static_source_gives_v_proportional_to_u_times_v(tmp_path, monkeypatch):
    """(e) V = U v_g to first order (ALGEBRA.md, The clock family on the Ports): a plane-wave packet of the charged family moving along +x on a periodic chain under a flux holder of level weight 1; the time line and the odd line are the same massless line of one holder stepped with one rule, so their sums over the chain follow one recurrence from their writes, the form D = 2 L^2 sin^2 omega and the flux 4 num L^2 sin omega sin k over the walls E_s T and 2 E_s 3 den T: SUM V_x against SUM (U - rest) times v_g = (num / (3 den)) sin k / sin omega within the rounding over 20 intervals, and the odd line's sign is the flux's."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = flux_world(tmp_path, (61, 1, 1), dict(x="periodic", y="periodic", z="periodic"), 1, 1)
    board = Lattice(load_world(world))
    index = [f.name for f in board.families].index(CHARGED["name"])
    family, gamma = board.families[index], board.world.node_clock
    packet(board, 0, (1, 8), 21, 10)
    k = 2 * np.pi / 8
    content = laws.vacuum_content(board.world, family)
    omega = np.arccos(laws.band_of(family.pair, gamma, content, board.unit, np.cos(k), 1.0, 1.0))
    num, den = family.pair
    speed = num / (3 * den) * np.sin(k) / np.sin(omega)
    gravity = board.states[[f.name for f in board.families].index("gravity")]
    rest = board.families[[f.name for f in board.families].index("gravity")].rest
    for _ in range(20):
        board.step()
    well = int((gravity.lines[0].now - rest).sum(dtype=object))
    odd = int(gravity.lines[4].now.sum(dtype=object))
    assert odd > 0 and well > 0 and 0 < speed < 1
    assert abs(odd - speed * well) <= 0.03 * speed * well + board.shape[0], (odd, well, speed)


def test_the_rotation_unit_by_the_rotation_act():
    """The family's rest rotation to the unit, K = omega_0 Gamma, found by a bisection on the rotation act and no root (the two hands' (d) of 2026-10-09; features/phase at the fixed angle theta_0 = 1 / Gamma): 5,046 at [4000, 6000] and Gamma 6,000 (arccos(2 / 3) x 6,000 = 5,046.4), 0 at the massless pair [1, 1], and at [2, 3] within one unit of Gamma arccos(2 / 3); the value checked against the phase line itself in Python's fractions at an independent amplitude, the cosine line's level over X above 2 / 3 one act before K and below it one act after, the crossing within one unit of K; and the root is gone from core/paces.py."""
    gamma = 6000
    assert phase.rotation_unit(4000, 6000, gamma) == 5046
    assert phase.rotation_unit(1, 1, gamma) == 0
    found = phase.rotation_unit(2, 3, gamma)
    assert abs(found - gamma * np.arccos(2 / 3)) <= 1
    amplitude = (2**36 // gamma) * gamma  # an amplitude of the test's own, a multiple of Gamma
    pair = phase.iterate(phase.seed(amplitude, gamma), found - 1, gamma)
    before = Fraction(int(phase.read(pair)[0]), amplitude)
    after = Fraction(int(phase.read(phase.iterate(pair, 2, gamma))[0]), amplitude)
    assert before > Fraction(2, 3) > after, (before, after)
    source = Path(paces.__file__).read_text(encoding="utf-8")
    assert "division_fixed_point" not in source
