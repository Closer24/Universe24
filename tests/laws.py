"""The helpers of the law's tests: a module loaded by its path (a tool; the generator, the back-in-time gate and the runner loaded once for every test), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`); the chain is the shortest that holds the body of 50 quanta (about eleven Nodes about its centre) and the end node_readers with their regions apart, since the lay's cost is the start's relaxation over the chain's length squared, and every bound the tests put on the chain is per Node, the same on any length."""

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe import credit, growth, node, share
from event_universe.core import paces
from event_universe.game_board import GameBoard
from event_universe.loader.derived import Row, quanta_records

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the law's rows
CHAIN, QUANTA = (
    24,
    6,
)  # the shortest chain (x open) holding the body apart from the end node_readers; the
# smallest body the generator lays on it in seconds (a test runs under 30 seconds, the owner's word)
CHARGED = {"name": "charged", "pair": [4000, 6000], "dimension": 2}  # matter's pair as a plane
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


def refused(match: str, call, *args, **keys):
    with pytest.raises(ValueError, match=match) as refusal:
        call(*args, **keys)
    return refusal.value


def design_beside(folder: Path, stem: str, **keys: object) -> Path:
    """The folder's design file with the generator's keys for one world (`worlds[stem]`: `quanta`, `senses`, `pixels`, the inputs the generator reads from the design file beside the world and never from the command line; the owner's decision C2, #1793 comment 5982379080), the other worlds' entries kept."""
    path = folder / "design.json"
    design = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"worlds": {}}
    design["worlds"][stem] = {**design["worlds"].get(stem, {}), **keys}
    path.write_text(json.dumps(design), encoding="utf-8")
    return path


TOOLS = ("pixel_mode", "back_in_time", "run_inputs")  # the generator, the back-in-time gate, the runner
TOOL, BACK, RUN = (load_file(name, ROOT / "tools" / f"{name}.py") for name in TOOLS)
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")  # the look's reader


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, of every family's reads too, a family's pair replaced where `pairs` names it, the charged matter row, matter's pair as a plane, added where `charged`) with the engine's start file as e.json."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [json.loads(json.dumps(CHARGED))] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
        family["reads"] = {name: w for name, w in family["reads"].items() if name not in drop}
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())


def chain_body_world(folder, tool, quanta=QUANTA, at=(), senses=(), taker=False, mode=True, chain=CHAIN):  # type: ignore[no-untyped-def]
    """A chain of `chain` Nodes (x open) with a body of matter declared with `quanta` on each Node of `at` (the chain's centre where empty; the last read by the node_reader `taker` where asked), or, where `senses` gives the body a sense, a body of the charged family (matter's pair as a plane) rotating in that sense, one quantum of count 1 (the law's count per charged record, the loader's gate; ALGEBRA.md, No record reads its own write of the sign), laid by the generator as the one-Node record of its quantum (the design file's `pixels` and `senses` beside the chain, `design_beside`) where the matter body is laid at its fixed point: the bodies' Nodes with their counts and the mode file beside them; the node_readers `left` and `right`, two Nodes each at the chain's two ends (never one Node), report the light's inflow there."""
    at = at or (chain // 2,)  # the chain's centre where no Node is named
    families = [CHARGED["name"] if i < len(senses) and senses[i] else "matter" for i in range(len(at))]
    universe_beside(folder, charged=CHARGED["name"] in families)
    charged = [f == CHARGED["name"] for f in families]  # one quantum per charged record, the law's count
    nodes = [[dict(node=[x, 0, 0], count=1 if c else quanta)] for x, c in zip(at, charged, strict=True)]
    bodies = [dict(family=f, nodes=n) for f, n in zip(families, nodes, strict=True)]
    ends = [{"name": "left", "positions": [[0, 0, 0], [1, 0, 0]]}]
    ends += [{"name": "right", "positions": [[chain - 2, 0, 0], [chain - 1, 0, 0]]}]
    node_readers = ends + ([{"name": "taker", "block": len(at) - 1}] if taker else [])
    world = dict(shape=[chain, 1, 1], node_readers=node_readers, bodies=bodies, ticks=400, face_depth=1)
    world.update(boundary=dict(x="open", y="periodic", z="periodic"), universe="u.json", engine="e.json")
    (path := folder / "chain.json").write_text(json.dumps(world), encoding="utf-8")
    pixels = [n for n, c in enumerate(charged) if c]  # the charged body a one-Node record
    design_beside(folder, path.stem, senses=list(senses), pixels=pixels)  # the design's keys beside
    if mode:  # the charged body laid by the design's `pixels` in its sense, matter at its fixed point
        tool.main(["--input", str(path)])
    return path


SLIT = dict(shape=[24, 9, 1], boundary=dict(x="open", y="open", z="periodic"), face_depth=1, ticks=24)
SLIT.update(universe="u.json", engine="e.json", bodies=[], node_readers=[])
SLIT["faces"] = [{"axis": "x", "at": 12, "gaps": [{"y": [4, 4], "z": [0, 0]}]}]
PACKET = {"family": "charge", "along": "x", "wave": [1, 4], "phase": [0, 1], "amplitude": 1328}
PACKET.update(top={"x": [5, 5], "y": [0, 8], "z": [0, 0]}, edge={"x": 4, "y": 0, "z": 0})


def packet_world(folder: Path, tool, lifetime: int = 8, width: int = 3, ticks: int = 60) -> Path:  # type: ignore[no-untyped-def]
    """The open board's packet world cut small: the shipped packet giving's giver over two Nodes of a 160 by 5 by 5 board with one giving at `lifetime` and `width`, its window 2, no reader and no draw, its mode file written by the generator."""
    world = json.loads((EVENTS / "packet_giving" / "packet_giving.json").read_text(encoding="utf-8"))
    giver = world["bodies"][0]
    rate = {**giver["rates"][0], "width": width, "lifetime": lifetime}
    nodes = [{"node": [80, 2, 2], "weight": 1}, {"node": [81, 2, 2], "weight": 1}]
    small = {**world, "shape": [160, 5, 5], "ticks": ticks, "node_readers": []}
    reader = {**giver["node_reader"], "window": 2}
    small["bodies"] = [{**giver, "nodes": nodes, "rates": [rate], "node_reader": reader}]
    del small["draw"]
    (path := folder / "small.json").write_text(json.dumps(small) + "\n", encoding="utf-8")
    tool.main(["--input", str(path)])
    return path


def ion_universe_beside(folder: Path) -> None:
    """The shelved ion's universe copied beside a world as u.json with the engine file as e.json: four families, no holder of the content, so a periodic box needs no sink."""
    (folder / "u.json").write_bytes((EVENTS / "shelved_ion" / "mercury_ion.json").read_bytes())
    (folder / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())


def ion_world(folder: Path, tool, ticks: int = 23, amplitude: int = 600, body: bool = True) -> Path:  # type: ignore[no-untyped-def]
    """The ion-like world on a periodic box of 8 by 6 by 5 (one odd extent, so that the staggered mode (-1)^(x + y + z + t), the band's top, is no exact mode of the board): the three-part ion over two Nodes with its transition at [2, 3] from the strong drive and its giving to the fluorescence at the lifetime 8, the drive a plane wave along x at `amplitude`, the counter the plane x = 0 with the world's draw at the window 18; the telegraph's shape, its mode file written by the generator; without the ion (`body` False) the drive and the counter alone as beam_alone.json, the twin of the undepleted beam."""
    ion_universe_beside(folder)
    shape = (8, 6, 5)
    at, beside = [3, 3, 2], [4, 3, 2]
    parts = [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {"window": 1, "seed": 25, "multiplier": 6364136223846793005, "increment": 1}
    nodes = [{"node": at, "weight": 1}, {"node": beside, "weight": 1}]
    record = {"family": "ion", "nodes": nodes, "parts": parts, "node_reader": draw}
    record["transitions"] = [
        {"from": "S", "to": "P", "drive": "strong_drive", "weight": 1, "resonance": [2, 3]}
    ]
    record["rates"] = [{"from": "P", "to": "S", "lifetime": 8, "gives_to": "fluorescence"}]
    drive = {
        "family": "strong_drive",
        "along": "x",
        "wave": [1, 2],
        "phase": [0, 1],
        "amplitude": amplitude,
    }
    top = {axis: [0, extent - 1] for axis, extent in zip("xyz", shape, strict=True)}
    drive.update(top=top, edge={"x": 0, "y": 0, "z": 0})
    plane = [[0, y, z] for y in range(shape[1]) for z in range(shape[2])]
    world = dict(shape=list(shape), boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=ticks)
    world.update(universe="u.json", engine="e.json", bodies=[record] if body else [], messages=[drive])
    world.update(
        node_readers=[{"name": "counter", "positions": plane}], draw={**draw, "window": 18, "seed": 24}
    )
    (path := folder / ("ion_like.json" if body else "beam_alone.json")).write_text(json.dumps(world))
    tool.main(["--input", str(path)])
    return path


def slit_world(folder: Path, tool, name: str = "slit", **changes: object) -> Path:  # type: ignore[no-untyped-def]
    universe_beside(folder)
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "messages": [PACKET], **changes}), encoding="utf-8")
    tool.main(["--input", str(path)])
    return path


def own_lines(board: GameBoard, index: int) -> list[node.Record]:
    """A family's record lines as the engine reads them: every record's lines, light the sum of its rows."""
    return [line for r in quanta_records(board.families, index) for line in board.lines_of(index, r)]


def shares_of(board: GameBoard, index: int, read, pairs) -> np.ndarray:  # type: ignore[no-untyped-def]
    """The share form per Node of a family's lines at the paces of its `read`, in Python's integers."""
    gamma, unit = board.world.node_clock, board.unit
    found = share.family_share(board.families[index], pairs, board.wrap, gamma, *read, unit)
    return found.astype(object)


def booked(board: GameBoard, monkeypatch, *indexes: int) -> list[tuple[int, Fraction]]:  # type: ignore[no-untyped-def]
    """One step of the GameBoard with the booking identity per act on the families `indexes` (ALGEBRA.md S.6; the advisor's lines, #1563 comments 5954101082 and 5963391333): the share's change over the step is the currents at the pair the step started from with the paces' anisotropy term and Rule3's remainder term, within the division act's floors, plus the face term per face presented at the step, (next - before) R_face (value - arrival) over 2 p_i^2 G^2 (the hole over its two intervals, each shell of the front), the identity on the stepped levels before the lays; the lays (the taking's and the giving's parts, the given quantum, the null window's re-lay) change the share form at the written Nodes and their six neighbours alone, exact; per family the paces' own change of the books' total and the slack."""
    growth.grow(board)  # the receding faces read first, as the step reads them
    gamma, unit, begun, shape = board.world.node_clock, board.unit, {}, board.shape
    for index in indexes:
        read = board.read(index)
        pace = np.asarray(paces.link_pace_of(gamma, read[0])).astype(object)
        flow = [np.asarray(current, dtype=object) for current in board.currents()[index]]
        factors = [np.asarray(q).astype(object) - unit * unit for q in read[1]]
        skew = [q * c for q, c in zip(factors, flow, strict=True)]
        terms = sum(Fraction(int(n), unit * unit) for found in skew for n in found.ravel())
        reads = node.rule_of(board.families[index], gamma, *read, unit)[0]
        squares, net = np.broadcast_to(pace * pace, shape), int(sum(c.sum() for c in flow))
        begun[index] = (read, own_lines(board, index), net, terms, squares, reads)
    stepped, counted = {}, credit.counted_windows

    def kept(b: GameBoard) -> None:  # the lines after the hold, before the NodeReaders' acts
        stepped.update({i: own_lines(b, i) for i in indexes}), counted(b)

    with monkeypatch.context() as swap:
        swap.setattr(credit, "counted_windows", kept), board.step()
    found = []
    for index in indexes:
        read, records, net, terms, squares, reads = begun[index]
        moved, fixed = own_lines(board, index), int(shares_of(board, index, read, stepped[index]).sum())
        for was, now in zip(records, stepped[index], strict=True):  # Rule3's remainder term per line
            step = (now.now.astype(object) - was.before.astype(object)).ravel()  # next - before
            carried = (now.remainder.astype(object) - was.remainder.astype(object)).ravel()  # r' - r
            pairs = zip(step * carried, squares.ravel(), strict=True)
            terms += sum(Fraction(-int(n), 2 * int(d) * unit * unit) for n, d in pairs)
        for face in [f for f in board.credit.faces.get(board.tick, []) if f.family == index]:
            here, read_at = tuple(np.add(face.at, board.offset)), reads[face.port]  # the face term
            read_at = int(np.asarray(read_at)[here]) if np.ndim(read_at) else int(read_at)
            fill = board.families[index].rest if face.line == 0 else 0
            arrived = int(node.ports(records[face.line].now, board.wrap, fill)[face.port][here])
            step = int(stepped[index][face.line].now[here]) - int(records[face.line].before[here])
            wall = 2 * int(squares[here]) * unit * unit
            terms += Fraction(step * read_at * (face.value - arrived), wall)
        floors = len(records) * records[0].now.size  # the division act's floor, under one unit per Node
        start = int(shares_of(board, index, read, records).sum())
        assert abs(Fraction(fixed - start - net) - terms) < floors, (index, fixed - start - net, terms)
        delta = shares_of(board, index, read, moved) - shares_of(board, index, read, stepped[index])
        laid = np.zeros(shape, dtype=bool)
        for a, b in zip(stepped[index], moved, strict=True):  # the Nodes a lay wrote
            laid |= (a.now != b.now) | (a.before != b.before) | (a.remainder != b.remainder)
        ports = node.ports(laid.astype(np.int64), board.wrap)
        near = laid | np.logical_or.reduce([p != 0 for p in ports])
        assert not delta[~near].any() and fixed + int(delta[near].sum()) == int(delta.sum()) + fixed
        found.append((board.total_share(index)[0] - fixed - int(delta.sum()), abs(terms) + floors))  # type: ignore[operator]
    return found
