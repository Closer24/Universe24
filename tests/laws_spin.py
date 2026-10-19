"""The spin family's worlds and readers for the law's tests (the spin branch, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route), beside tests/laws.py, whose size the tests' shape caps: the two-plane family's world with its regions' axes and patterns and, optionally, its declared sign under exchange (`spin_world`), the exclusion world of a body of several parts with its drives (`exclusion_world`, the capacity's and the shell's), one run at a seed (`trial`), the reader's own arithmetic of the joint credit beside the engine's (`joint_shares`, the terms by the family's sign), the engine's own accumulation run again (`rebooked`), and the singlet's correlation from the half-angle pairs (`correlation`)."""

import itertools
import json
from fractions import Fraction
from pathlib import Path

from event_universe import credit, world_files
from event_universe.lattice import Lattice
from event_universe.loader.draw import ports_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, load_file

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
    meeting=None,
    reach=None,
    regions=None,
    erasure=None,
):  # type: ignore[no-untyped-def]
    """The spin branch's world beside `folder` (the pair's universe with the massless two-plane family `spin` added, the shape [2, 2]: two parts of a plane each, one quantum one count; as u.json with the engine file as e.json and the repository root turned to `folder`): a chain of `length` Nodes open on x with receding faces, one packet of the family at k = pi / 4 laid at the centre toward the lower side (and one toward the upper side with `both`), one quantum by the share at the amplitude 90 (the generator's lay 75; the laid share 0.9994 of the record's unit `credit.record_unit`, the books' count 1), its parts laid alike by the generator (the equal-parts state, the planes' sense lines at 0); with `both` the two packets at the amplitude 64 each (the lay 54), half a quantum each, the pair one quantum of the record (the share 1.0134 of the unit, the count 1), the regions of four Nodes at the ends with their `axis` and `pattern` from `sides` ({"left": (axis, pattern), "right": ...}), the draw over one window of `intervals`; with `exchange` the family's declared sign under exchange on its row, `antisymmetric` or `symmetric` (the key `exchange`, read by the joint credit as the determinant or the permanent of the two sides' parts, 2026-10-19), none otherwise; with `meeting` the draw's reading of the meeting, `root` or `back` (the key `meeting`, the click that runs back, `meeting_back`), and with `reach` the run back's reach beside it, `board`, `cone` or `books` (the key `reach`), each key absent otherwise, with `regions` the regions' x positions by name in place of the ends' four Nodes ({name: [x, ...]}: a third region, or regions of one Node), and with `erasure` the front's taper on the world (the key `erasure`), absent otherwise; the mode file by tools/pixel_mode.py; the world's path."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((EVENTS / "pair.json").read_text(encoding="utf-8"))
    universe["families"].append(json.loads(json.dumps(SPIN)))
    if exchange is not None:
        universe["families"][-1]["exchange"] = exchange
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (folder / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
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
            "axis": list(axis),
            "pattern": pattern,
        }
        for name, (axis, pattern) in sides.items()
    ]
    world = {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": intervals,
        **({"erasure": erasure} if erasure is not None else {}),
        "universe": "u.json",
        "engine": "e.json",
        "bodies": [],
        "packets": packets,
        "node_detectors": detectors,
        "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
        "draw": {
            "window": intervals,
            "seed": 24,
            "multiplier": 6364136223846793005,
            "increment": 1442695040888963407,
            **({"meeting": meeting} if meeting is not None else {}),
            **({"reach": reach} if reach is not None else {}),
        },
    }
    (path := folder / "spin.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


TRIALS = load_file(
    "meeting_trials", ROOT / "tools" / "meeting_trials.py"
)  # the trials tool: its hashed states
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
    seed,
    length=112,
    intervals=125,
    grounds=(("g", 2),),
    excited=("e", "f"),
    exchange=None,
):  # type: ignore[no-untyped-def]
    """The exclusion's world beside `folder` (the spin branch, item (e)): the two atoms' universe with the atom's family at the parts `grounds` (each a name with its count at the start; one part g of two quanta) and `excited` (the names, each at the count 0 and at the declared `capacity`, none where it is None), one plane each, one body at the chain's centre with a transition from every ground part to every excited part by `photon` at one weight and one resonance, its window at `seed`; with `exchange` the family's declared sign under exchange on its row (`antisymmetric` or `symmetric`, the key `exchange`), so that the start splits its counts over several ground parts (the shell's world, one quantum in gu and one in gd), none otherwise; two photons of one quantum each from the two ends toward the body, the second arriving after the first window closes (the lower from 24, the upper from 96, the chain of `length` Nodes open on x with receding faces); the mode file by tools/pixel_mode.py; the world's path."""
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((EVENTS / "anticoincidence" / "two_atoms.json").read_text(encoding="utf-8"))
    universe["families"][0]["dimension"] = [len(grounds) + len(excited), 2]
    if exchange is not None:
        universe["families"][0]["exchange"] = exchange
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (folder / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
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
    draw = {"multiplier": 6364136223846793005, "increment": 1442695040888963407, "seed": seed}
    body = {"family": "atom", "nodes": [{"node": [x, 0, 0], "weight": 1} for x in (at, at + 1)]}
    body.update(parts=parts, transitions=turns, rates=[], node_detector=draw)
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
        "engine": "e.json",
        "bodies": [body],
        "packets": photons,
        "node_detectors": [],
        "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
    }
    (path := folder / "exclusion.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def trial(path: Path, seed: int, intervals: int) -> tuple[Lattice, list[dict]]:  # type: ignore[type-arg]
    """One run from the lay with the regions' draw at the trial's seed (`hashed_state`, the trials tool's), the board and its lines."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    board.credit.state = TRIALS.hashed_state(seed, board.world.width)
    for _ in range(intervals):
        board.step()
    return board, lines


def joint_shares(
    lines: list[dict], sides: dict[str, tuple[tuple[int, int], list[list[int]]]], exchange: int = 0
) -> dict[tuple[int, ...], int]:  # type: ignore[type-arg]
    """The joint credit's shares per combination of the sides' ports (0 the plus port, 1 the minus) from the `parts` lines of the regions in `sides` ({name: (axis, pattern)}), the reader's own arithmetic beside the engine's (`credit.joined`): per interval and member of the level pair the amplitude's terms, each the product over the sides of e^s_k(port) psi^s_k with psi^s_k the part's (re, im) sums at side s, SUM_k over the same part at every side for a family declaring no sign or the symmetric one (`exchange` 0 or 1, the form as it stood) and SUM_{k != l} sign(l - k) over the ordered pairs of parts across two sides for the antisymmetric (`exchange` -1, the determinant of the two sides' parts), its norm squared summed over the window; one side gives the two shares of Stern and Gerlach."""
    names = list(sides)
    ports = {
        n: ports_of(axis, tuple(tuple(pair) for pair in pattern)) for n, (axis, pattern) in sides.items()
    }
    parts = len(ports[names[0]][0])
    terms = (
        [(1, (k,) * len(names)) for k in range(parts)]
        if exchange >= 0
        else [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]
    )
    intervals: dict[int, dict[str, list[list[int]]]] = {}
    for row in lines:
        if row["event"] == "parts" and row["node_detector"] in sides:
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
                        sums = levels.get(
                            name, [[0, 0]] * (2 * parts)
                        )  # per line [now, before]: re_k, im_k
                        e = ports[name][port][k]
                        re, im = e * sums[2 * k][member], e * sums[2 * k + 1][member]
                        product = (product[0] * re - product[1] * im, product[0] * im + product[1] * re)
                    re_sum, im_sum = re_sum + product[0], im_sum + product[1]
                total += re_sum * re_sum + im_sum * im_sum
        found[key] = total
    return found


def conditional_shares(
    lines: list[dict],  # type: ignore[type-arg]
    sides: dict[str, tuple[tuple[int, int], list[list[int]]]],
    exchange: int,
    first: int,
    port: int,
) -> tuple[list[int], list[int], list[int]]:
    """The two readings of the meeting that runs back from the `parts` lines, the reader's own arithmetic beside the engine's books (`credit.marginal_of`, `credit.conditioned`, `credit.reweighted_share`; the identity P(A) P(B | A) = P(A, B) of tests/test_the_meeting_back.py): the first side's marginal per port, the sum of the joint shares over the partner's ports (`joint_shares`); the re-weighting of the partner's parts at the first side's realised `port`, per term of the amplitude (the symmetric form's SUM_k over the same part, the antisymmetric's determinant over the ordered pairs) the sign times the first side's coefficient on its part, added on the partner's part, so lambda_k = e_k(port) and lambda_l = SUM_k sign(l - k) e_k(port); and the partner's share per port q, SUM over the window's intervals and both members of |SUM_k e_k(q) lambda_k psi_k|^2 with psi_k the part's (re, im) sums; returns (marginal, lambdas, conditional)."""
    names, partner = list(sides), 1 - first
    ports = {
        n: ports_of(axis, tuple(tuple(pair) for pair in pattern)) for n, (axis, pattern) in sides.items()
    }
    parts, joint = len(ports[names[0]][0]), joint_shares(lines, sides, exchange)
    marginal = [sum(share for key, share in joint.items() if key[first] == p) for p in range(2)]
    terms = (
        [(1, (k, k)) for k in range(parts)]
        if exchange >= 0
        else [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]
    )
    lambdas = [0] * parts
    for sign, which in terms:
        lambdas[which[partner]] += sign * ports[names[first]][port][which[first]]
    conditional = []
    for q in range(2):
        total = 0
        for row in lines:
            if row["event"] == "parts" and row["node_detector"] == names[partner]:
                for member in range(2):
                    re_sum, im_sum = 0, 0
                    for k in range(parts):
                        e = ports[names[partner]][q][k] * lambdas[k]
                        re_sum += e * row["levels"][2 * k][member]
                        im_sum += e * row["levels"][2 * k + 1][member]
                    total += re_sum * re_sum + im_sum * im_sum
        conditional.append(total)
    return marginal, lambdas, conditional


def rebooked(board: Lattice, lines: list[dict], family: str = "spin") -> dict[tuple[int, ...], int]:  # type: ignore[type-arg]
    """The engine's own joint credit run again over the run's `parts` lines (the joints are cleared at the window's close): the joints emptied, and the window's sums per interval with them where the meeting runs back, and `credit.joined` fed each interval's sums per region as the meeting feeds it, the shares per combination returned to be compared with the reader's exactly, no statistics."""
    index = [f.name for f in board.families].index(family)
    board.credit.joints.clear()
    board.credit.levels.clear()
    sums: dict[int, dict[str, list[list[int]]]] = {}
    for row in lines:
        if row["event"] == "parts" and row["family"] == family:
            sums.setdefault(row["interval"], {})[row["node_detector"]] = row["levels"]
    for interval in sorted(sums):
        credit.joined(board, index, sums[interval])
    return dict(board.credit.joints[index])


def correlation(a: tuple[int, int], b: tuple[int, int]) -> Fraction:
    """The singlet's E(a, b) = -cos(theta_a - theta_b) from the half-angle pairs, exact: -((c_a c_b + s_a s_b)^2 - (c_a s_b - s_a c_b)^2) / ((c_a^2 + s_a^2) (c_b^2 + s_b^2))."""
    (ca, sa), (cb, sb) = a, b
    same, different = (ca * sb - sa * cb) ** 2, (ca * cb + sa * sb) ** 2
    return Fraction(same - different, (ca * ca + sa * sa) * (cb * cb + sb * sb))
