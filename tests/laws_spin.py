"""The spin family's worlds and readers for the law's tests (the spin branch, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route), beside tests/laws.py, whose size the tests' shape caps: the two-plane family's world with its regions' axes and patterns and, optionally, its declared sign under exchange (`spin_world`), the exclusion world of a body of several parts with its drives (`exclusion_world`, the capacity's and the shell's), one run at a seed (`trial`), the reader's own arithmetic of the joint credit beside the engine's (`joint_shares`, the terms by the family's sign), the chain rule's weights from them (`marginal_of`) and the engine's weights at every side's draw against them (`sided`), and the singlet's correlation from the half-angle pairs (`correlation`)."""

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe import meeting_back, world_files
from event_universe.lattice import Lattice
from event_universe.loader.draw import ports_of, times
from event_universe.world_files import load_world
from tests.laws import EVENTS, TOOL
from tests.laws_content import with_content

SPIN = {"name": "spin", "pair": [6000, 6000], "reads": {"gravity": 1, "binding": 1}, "dimension": [2, 2]}


def spin_world(
    folder,
    monkeypatch,
    sides,
    both=False,
    length=33,
    intervals=40,
    amplitude=90,
    exchange=None,
    regions=None,
):  # type: ignore[no-untyped-def]
    """The spin branch's world beside `folder` (the pair's universe with the massless two-plane family `spin` added, the shape [2, 2]: two parts of a plane each, one quantum one count; as u.json with the engine file as e.json and the repository root turned to `folder`): a chain of `length` Nodes open on x with receding faces, one packet of the family at k = pi / 4 laid at the centre toward the lower side (and one toward the upper side with `both`), one quantum by the share at the amplitude 90 (the generator's lay 75; the laid share 0.9994 of the record's unit `credit.record_unit`, the books' count 1), its parts laid alike by the generator (the equal-parts state, the planes' sense lines at 0); with `both` the two packets at the amplitude 64 each (the lay 54), half a quantum each, the pair one quantum of the record (the share 1.0134 of the unit, the count 1), the regions of four Nodes at the ends with their `axis` and `pattern` from `sides` ({"left": (axis, pattern), "right": ...}), the draw over one window of `intervals`; with `exchange` the family's declared sign under exchange on its row, `antisymmetric` or `symmetric` (the key `exchange`, read by the joint credit as the determinant or the permanent of the two sides' parts, 2026-10-19), none otherwise, with `regions` the regions' x positions by name in place of the ends' four Nodes ({name: [x, ...]}: a third region, or regions of one Node); the mode file by tools/pixel_mode.py; the world's path."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((EVENTS / "pair.json").read_text(encoding="utf-8"))
    universe["families"].append(json.loads(json.dumps(SPIN)))
    if exchange is not None:
        universe["families"][-1]["exchange"] = exchange
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
    source, depth = length // 2, 4
    packets = [
        {
            "family": "spin",
            "along": "x",
            "wave": [sign, 4],
            "phase": [0, 1],
            "amplitude": amplitude,
            "top": {"x": [source, source], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 6, "y": 0, "z": 0},
        }
        for sign in ((-1, 1) if both else (-1,))
    ]
    ends = {"left": list(range(depth)), "right": list(range(length - depth, length))}
    ends.update(regions or {})
    detectors = [
        {
            "name": name,
            "positions": [[x, 0, 0] for x in ends[name]],
            "basis": list(axis),
            "pattern": pattern,
        }
        for name, (axis, pattern) in sides.items()
    ]
    world = {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": intervals,
        "universe": "u.json",
        "bodies": [],
        "packets": packets,
        "node_detectors": detectors,
        "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
        "draw": {},  # the window derived (2026-10-23)
    }
    (path := folder / "spin.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


IDENTITY = [[1, 0], [0, 1]]  # the parts the spinor's two components: the + port reads (c, s)
SINGLET = [
    [0, 1],
    [-1, 0],
]  # the partner's pattern in the singlet: its + port reads (s, -c), its - port (c, s)
BELL = (
    (1, 0),
    (1, 1),
    (12, 5),
    (5, 12),
)  # a, a', b, b' as half-angle pairs: 0 and 90 degrees, and cos = 119 / 169
PORT = {"plus": 0, "minus": 1}


def exclusion_world(
    folder,
    monkeypatch,
    capacity,
    length=112,
    intervals=125,
    grounds=(("g", 2),),
    excited=("e", "f"),
    exchange=None,
):  # type: ignore[no-untyped-def]
    """The exclusion's world beside `folder` (the spin branch, item (e)): the two atoms' universe with the atom's family at the parts `grounds` (each a name with its count at the start; one part g of two quanta) and `excited` (the names, each at the count 0 and at the declared `capacity`, none where it is None), one plane each, one body at the chain's centre with a transition from every ground part to every excited part by `photon` at one weight and one resonance, its window at `seed`; with `exchange` the family's declared sign under exchange on its row (`antisymmetric` or `symmetric`, the key `exchange`), so that the start splits its counts over several ground parts (the shell's world, one quantum in gu and one in gd), none otherwise; two photons of one quantum each from the two ends toward the body, the second arriving after the first window closes (the lower from 24, the upper from 96, the chain of `length` Nodes open on x with receding faces); the mode file by tools/pixel_mode.py; the world's path."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((EVENTS / "anticoincidence" / "two_atoms.json").read_text(encoding="utf-8"))
    universe = with_content(universe)  # the content of the born universe, 2026-10-20
    universe["families"][2]["dimension"] = [len(grounds) + len(excited), 2]
    if exchange is not None:
        universe["families"][2]["exchange"] = exchange
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", folder)
    at, held = length // 2 - 9, {} if capacity is None else {"capacity": capacity}
    parts = [{"part": k, "name": n, "count": c} for k, (n, c) in enumerate(grounds)] + [
        {"part": len(grounds) + k, "name": n, "count": 0, **held} for k, n in enumerate(excited)
    ]
    turns = [
        {"from": g, "to": e, "drive": "photon", "weight": 6, "resonance": [5414, 6000]}
        for g, _count in grounds
        for e in excited
    ]
    body = {"family": "atom", "nodes": [{"node": [x, 0, 0], "weight": 1} for x in (at, at + 1)]}
    body.update(parts=parts, transitions=turns, rates=[], node_detector={})  # the window derived
    photons = [
        {
            "family": "photon",
            "along": "x",
            "wave": [sign, 4],
            "phase": [0, 1],
            "amplitude": 110,
            "top": {"x": [x, x], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        }
        for sign, x in ((1, 24), (-1, 96))
    ]
    world = {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": intervals,
        "universe": "u.json",
        "bodies": [body],
        "packets": photons,
        "node_detectors": [],
        "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
    }
    (path := folder / "exclusion.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def trial(path: Path, intervals: int) -> tuple[Lattice, list[dict]]:  # type: ignore[type-arg]
    """One run from the lay over `intervals`, every draw the click's read of the board: the board and its lines."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    for _ in range(intervals):
        board.step()
    return board, lines


def joint_shares(
    lines: list[dict],  # type: ignore[type-arg]
    sides: dict[str, tuple],  # type: ignore[type-arg]
    exchange: int = 0,
    width: int = 2,
    close: int | None = None,
) -> dict[tuple[int, ...], int]:
    """The joint credit's shares per combination of the sides' ports (0 the plus port, 1 the minus) from the `parts` lines of the regions in `sides` ({name: (axis, pattern)}), the reader's own arithmetic beside the engine's sides' books (`credit.moments_booked`, the second moments per side; the joint is the test's reading alone, nothing joint in the books): per interval and member of the level pair the amplitude's terms, each the product over the sides of e^s_k(port) psi^s_k with psi^s_k the part's (re, im) sums at side s (`width` 2, a plane's two lines; 1 a real line, im 0), SUM_k over the same part at every side for a family declaring no sign or the symmetric one (`exchange` 0 or 1, the form as it stood) and SUM_{k != l} sign(l - k) over the ordered pairs of parts across two sides for the antisymmetric (`exchange` -1, the determinant of the two sides' parts), its norm squared summed over the window; one side gives the two shares of Stern and Gerlach."""
    names = list(sides)
    ports = {  # a side (axis, pattern) or (axis, pattern, turn), the quarter turn of a plane side
        n: ports_of(side[0], tuple(tuple(pair) for pair in side[1]), *side[2:])
        for n, side in sides.items()
    }
    parts = len(ports[names[0]][0])
    terms = (
        [(1, (k,) * len(names)) for k in range(parts)]
        if exchange >= 0
        else [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]
    )
    if (
        close is None
    ):  # the sides' own close, the interval of their credit lines (the window derived, 2026-10-23: the close before the run's end, where the declared window was the run)
        closes = [
            int(row["interval"])
            for row in lines
            if row["event"] == "credit" and row["node_detector"] in sides
        ]
        close = min(closes) if closes else None
    intervals: dict[int, dict[str, list[list[int]]]] = {}
    for row in lines:  # the window's parts lines: to the sides' close
        if row["event"] == "parts" and row["node_detector"] in sides:
            if close is None or row["interval"] <= close:
                intervals.setdefault(row["interval"], {})[row["node_detector"]] = row["levels"]
    found = {}
    for key in itertools.product(range(2), repeat=len(names)):
        total = 0
        for levels in intervals.values():
            for member in range(2):
                re_sum, im_sum = 0, 0
                for sign, which in terms:
                    product = (sign, 0)
                    for name, port, k in zip(names, key, which, strict=True):
                        sums = levels.get(name, [[0, 0]] * (width * parts))  # per line [now, before]
                        e = ports[name][port][k]  # a Gaussian integer, (e, 0) on a real-port side
                        psi = (sums[width * k][member], sums[width * k + 1][member] if width == 2 else 0)
                        product = times(product, times((e[0], -e[1]), psi))  # <e(port)|psi>: conj(e) psi
                    re_sum, im_sum = re_sum + product[0], im_sum + product[1]
                total += re_sum * re_sum + im_sum * im_sum
        found[key] = total
    return found


def marginal_of(
    joint: dict[tuple[int, ...], int], side: int, fixed: dict[int, int] | None = None
) -> list[int]:
    """The chain rule's weights from the joint shares (`joint_shares`), the reader's own arithmetic beside the engine's Gram read: per port of `side` the sum of the shares over the keys agreeing with the realised ports `fixed`; the marginal where none is fixed."""
    realised = fixed or {}
    return [
        sum(
            share
            for key, share in joint.items()
            if key[side] == port and all(key[s] == p for s, p in realised.items())
        )
        for port in range(2)
    ]


def sided(board: Lattice, index: int, joint: dict[tuple[int, ...], int], realised: list[int]) -> None:
    """The engine's weights at every side's draw (`credit.Books.weights`, the Gram read of the side's own moments of the record as written) against the chain rule from the joint shares of the `parts` lines, exact in the rationals: the first side's the marginal, each later side's the conditional at the ports realised before it (the Gram theorem, ALGEBRA.md, The meeting's identity); exact in the integers where every coefficient written before the side takes one magnitude on the surviving parts, which is the case the caller asserts here."""
    fixed: dict[int, int] = {}
    for side, (name, _ports) in enumerate(board.credit.sides):
        weights, chain = board.credit.weights[(index, name)], marginal_of(joint, side, fixed)
        assert sum(weights) > 0 and sum(chain) > 0, (name, weights, chain)
        assert [Fraction(w, sum(weights)) for w in weights] == [
            Fraction(c, sum(chain)) for c in chain
        ], name
        fixed[side] = realised[side]


def correlation(a: tuple[int, int], b: tuple[int, int]) -> Fraction:
    """The singlet's E(a, b) = -cos(theta_a - theta_b) from the half-angle pairs, exact: -((c_a c_b + s_a s_b)^2 - (c_a s_b - s_a c_b)^2) / ((c_a^2 + s_a^2) (c_b^2 + s_b^2))."""
    (ca, sa), (cb, sb) = a, b
    same, different = (ca * sb - sa * cb) ** 2, (ca * cb + sa * sb) ** 2
    return Fraction(same - different, (ca * ca + sa * sa) * (cb * cb + sb * sb))


def digest(board: Lattice) -> str:
    """One hash of every array of the board at a frame (`meeting_back.snapshot`, the arrays' bytes in the families' and the lines' order, the levels' list where the kind is Python's integers): the state of one frame, compared frame by frame between two reaches or two seeds."""
    found = hashlib.sha256()
    for arrays in meeting_back.snapshot(board):
        for _label, array in arrays:
            a = np.asarray(array)
            found.update(a.tobytes() if a.dtype != object else repr(a.ravel().tolist()).encode())
    return found.hexdigest()


def reduced_write(
    written: list[tuple[int, int]], coefficients: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """The test's own reading of the click's write (the Boss's amendment of 2026-10-20; `credit.reduced`): the port's coefficients over their greatest common divisor on the surviving parts (the cumulative coefficient other than 0), 1 everywhere when they are one value there (a scaling alone writes nothing) and on a part written 0; the cumulative coefficients after the write. On Gaussian integers (pairs): the common factor the gcd of every component of the surviving coefficients, the identity (1, 0) where one pair stands on every surviving part."""
    surviving = [k for k, w in enumerate(written) if w != (0, 0)]
    common = 0
    for k in surviving:
        common = math.gcd(math.gcd(common, abs(coefficients[k][0])), abs(coefficients[k][1]))
    found = [
        (coefficients[k][0] // common, coefficients[k][1] // common)
        if common and k in surviving
        else (1, 0)
        for k in range(len(written))
    ]
    if len({found[k] for k in surviving}) <= 1:
        found = [(1, 0)] * len(written)
    return [times(w, c) for w, c in zip(written, found, strict=True)]
