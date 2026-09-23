"""The pins of the event split before any run (the chief physicist,
2026-09-23; DESIGN.md section 7, CORRECTIONS.md section 2). COMPUTATION
only: an offline coin walk of one record on a world's GameBoard, no
engine run, nothing registered.

(A) The copy rule against the coin in one dimension: the growth factor of
    the copy rule (a diffusion with phases) and the coin's front (a wave);
    the norm of each.
(B) The coin walk's front on an empty two-dimensional GameBoard from one
    birth on the in-plane fans (the primitive directions of Manhattan
    length at most 3 and at most 6, and the four headings): the front's
    radius by direction and the norm's conservation (the fan's isotropy).
(C) The single opening (row 10, `docs/designs/fail_rows/opening_w27.json`
    and `opening_w9.json`) and the two slits (row 2a,
    `examples/events/amplitude/slits_huygens.json`) under the coin: the
    world's lamp births its declared fan with its turns (the one-input
    rule at the birth), the coin acts at every free Node the record
    enters, the wall's Nodes and the screen's pixels absorb (cells of the
    ladder), the open faces take the escapes (cells); the screen's cell
    weights, their full width at half maximum in sin theta, the product
    w x FWHM / lambda against the pins, the shares of the screen, the
    walls and the faces, and the clicks of 4096 births under the golden
    wheel by `cell_of`.
(D) The registered bars of the pair and Malus worlds (`bell/read.json`,
    `amplitude/malus_a.json`) under the coin with the six headings: the
    shares reaching each set and each face, the record that those
    arrangements cannot be read under the split (Reviewer 3's D3).

The walk (DESIGN.md section 3.2): every row of one record has the
record's age; a row on the direction D steps when the flight table's
count m_D(tau) = (2 tau S_1 Q + T_D) // (2 T_D) increases, along D's
digital line (the Bresenham order of nature_beam), so every row on D at
one age is at the same point of its line (`reseed_flight`); the arrivals
at a Node in one interval are multiplied by Grover's coin (2 / K) J - I
over the fan; the outputs are placed at the Node and merge with the
rows dwelling there on the same direction; the phase of every row is the
record's, floor(tau n / d) mod N at the age tau, so a set's pointer is
the sum over its arrivals of the amplitude times (cos, sin) of the phase
at the arrival. Amplitudes are floats here (the engine's exact integers
scale them by sqrt of the multiplicity); every ratio below is the
ladder's.

Run from the repository root:

    PYTHONPATH=src python docs/designs/event_split/split_pins.py > docs/designs/event_split/split_pins.out
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "docs" / "designs" / "fail_rows"))

from run_10_pins import (  # noqa: E402
    FAR_FIELD,
    NEAR_FIELD_W27,
    PIN_W9,
    PIN_W27,
    REFUTES_BELOW,
    fwhm_in_s,
)

from event_universe.events.amplitude import cell_of  # noqa: E402

Q = 64
WHEEL = (2531, 4096)
RECORDS = 4096
NEAR_FIELD_W9 = 0.891  # 22.2's exact Euclidean sum at w = 9 (run_10_pins.out P4)


def primitive_fan_2d(bound: int) -> list[tuple[int, int]]:
    """The primitive in-plane directions (a, b) with 0 < |a| + |b| <= bound."""
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            if (a or b) and abs(a) + abs(b) <= bound and math.gcd(abs(a), abs(b)) == 1:
                found.append((a, b))
    found.sort()
    return found


def bresenham(vector: tuple[int, int]) -> list[tuple[int, int]]:
    """The S_1 unit steps of one period of the digital line (nature_beam._bresenham)."""
    s1 = sum(abs(c) for c in vector)
    steps = []
    position = [0, 0]
    for j in range(s1):
        best = max(range(2), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        steps.append((step[0], step[1]))
    return steps


class Line:
    def __init__(self, vector: tuple[int, int], uniform: bool = False):
        self.uniform = uniform
        self.vector = vector
        self.s1 = sum(abs(c) for c in vector)
        self.t_d = math.isqrt(3 * (vector[0] ** 2 + vector[1] ** 2) * Q * Q)
        self.steps = bresenham(vector)

    def made(self, tau: int) -> int:
        if self.uniform:
            return tau
        return (2 * tau * self.s1 * Q + self.t_d) // (2 * self.t_d)


class Board:
    """One record's coin walk on a rectangle X x Y with open faces: the
    amplitude per direction and Node, the absorbing Nodes (each its own
    set unless named in a detector set), the faces' sets."""

    def __init__(
        self,
        width: int,
        height: int,
        fan: list[tuple[int, int]],
        absorbing: dict,
        phase_rate: tuple[int, int],
        modulus: int,
        mode: str = "coin",
        openings: list | None = None,
        coin_turn: float = math.pi,
        uniform: bool = False,
    ):
        self.mode = mode
        self.coin_turn = coin_turn
        self.uniform = uniform
        self.openings = set(openings or [])
        self.width, self.height = width, height
        self.fan = fan
        self.lines = [Line(v, uniform) for v in fan]
        self.index = {v: k for k, v in enumerate(fan)}
        self.amp = np.zeros((len(fan), width, height), dtype=complex)
        self.absorbing = absorbing  # (x, y) -> set name
        self.mask = np.zeros((width, height), dtype=bool)
        for x, y in absorbing:
            self.mask[x, y] = True
        self.n, self.d = phase_rate
        self.modulus = modulus
        self.pointer: dict[str, complex] = {}
        self.absorbed_norm = 0.0
        self.tau = 0

    def phase_at(self, tau: int) -> int:
        return (tau * self.n // self.d) % self.modulus

    def deposit(self, name: str, value: complex, tau: int, k: int) -> None:
        """A row arriving at a cell on the direction k at the age tau: its
        phase is the record's rate n / d times the EXACT flight time of the
        Links it made on its line, made T_D / (S_1 Q) intervals (BEAM_LAW
        note 45, the click's one floor; the integer age would round the
        phase by up to half an interval, a quarter turn at the registered
        rate), on top of the phase the row carries (the lamp's turn)."""
        line = self.lines[k]
        t_exact = tau if self.uniform else line.made(tau) * line.t_d / (line.s1 * Q)
        angle = 2 * math.pi * (self.n / self.d) * t_exact / self.modulus
        self.pointer[name] = self.pointer.get(name, 0j) + value * complex(
            math.cos(angle), math.sin(angle)
        )
        self.absorbed_norm += abs(value) ** 2

    def step(self) -> None:
        """One interval: the coin at every Node on every row there (the
        arrivals and the dwellers alike, the one unitary form: a coin that
        acted on the arrivals alone and merged its outputs with the
        dwellers would not conserve the norm), C = I - (2 / K) J, so that a
        lone row continues on its direction with 1 - 2 / K and sends
        -2 / K to each other direction (Grover's coin with the moving
        shift; the sign is the flip-flop convention's); then the rows on
        the directions whose flight table steps at this age move one Link
        along their lines, the arrivals at absorbing Nodes and off the
        board deposited into their cells."""
        self.tau += 1
        tau = self.tau
        K = len(self.fan)
        if self.mode == "coin":
            # the general unitary coin symmetric in the outputs, exp(i eps P) with
            # P = J / K the projector on the symmetric vector: C = I + (e^{i eps} - 1) P;
            # eps = pi is Grover's coin, eps -> 0 the straight rays
            total = self.amp.sum(axis=0)
            factor = (complex(math.cos(self.coin_turn), math.sin(self.coin_turn)) - 1.0) / K
            self.amp = self.amp + factor * total[None, :, :]
        opening_in: dict = {}
        for k, line in enumerate(self.lines):
            if line.made(tau) == line.made(tau - 1):
                continue
            sx, sy = line.steps[(line.made(tau) - 1) % line.s1]
            moving = self.amp[k].copy()
            self.amp[k] = 0.0
            shifted = np.zeros_like(moving)
            xs = slice(max(0, sx), self.width + min(0, sx))
            ys = slice(max(0, sy), self.height + min(0, sy))
            xs_from = slice(max(0, -sx), self.width + min(0, -sx))
            ys_from = slice(max(0, -sy), self.height + min(0, -sy))
            shifted[xs, ys] = moving[xs_from, ys_from]
            if sx > 0:
                for y in np.nonzero(moving[self.width - 1, :])[0]:
                    self.deposit("face:+x", complex(moving[self.width - 1, y]), tau, k)
            elif sx < 0:
                for y in np.nonzero(moving[0, :])[0]:
                    self.deposit("face:-x", complex(moving[0, y]), tau, k)
            if sy > 0:
                for x in np.nonzero(moving[:, self.height - 1])[0]:
                    self.deposit("face:+y", complex(moving[x, self.height - 1]), tau, k)
            elif sy < 0:
                for x in np.nonzero(moving[:, 0])[0]:
                    self.deposit("face:-y", complex(moving[x, 0]), tau, k)
            hit = shifted * self.mask
            if np.abs(hit).any():
                for x, y in zip(*np.nonzero(hit), strict=True):
                    self.deposit(self.absorbing[(int(x), int(y))], complex(hit[x, y]), tau, k)
                shifted = shifted * ~self.mask
            if self.mode == "apparatus" and self.openings and sx != 0:
                # a row stepping in y between two opening Nodes is not split again
                # (the registered multiplicity 27 x 601, one split per row)
                # the law as built: the row arriving at an opening's Node is split
                # once over the forward fan (a > 0), equal weights (the registered
                # rerelease with its fan); the outputs are not split again there
                for ox, oy in self.openings:
                    a = shifted[ox, oy]
                    if abs(a):
                        opening_in[(ox, oy)] = opening_in.get((ox, oy), 0j) + complex(a)
                        shifted[ox, oy] = 0.0
            self.amp[k] = shifted
        if opening_in:
            forward = [k for k, v in enumerate(self.fan) if v[0] > 0]
            for (ox, oy), a in opening_in.items():
                self.amp[forward, ox, oy] += a / math.sqrt(len(forward))

    def norm(self) -> float:
        return float((np.abs(self.amp) ** 2).sum())


def load_world(path: Path):
    world = json.loads(path.read_text())
    fams = world.get("families")
    if fams is None:
        fams = json.loads((ROOT / "examples" / "events" / "entities" / "families.json").read_text())
        light = None
        for e in fams["entities"]:
            for f in e["families"]:
                if f["name"] == "light":
                    light = f
    else:
        light = next(f for f in fams if f["name"] == "light")
    n, d = light["phase_per_link"]
    width, height, _ = world["shape"]
    lamp = next(m for m in world["measured"] if "lamp" in m)
    absorbing = {}
    openings = []
    for m in world["measured"]:
        if "lamp" in m:
            continue
        x, y = m["position"][0], m["position"][1]
        if "table" in m and "rerelease" in json.dumps(m["table"]):
            openings.append((x, y))  # free under the split
            continue
        absorbing[(x, y)] = f"wall_{x}_{y}"
    for det in world["detectors"]:
        for pos in det["positions"]:
            absorbing[(pos[0], pos[1])] = det["name"]
    return world, (n, d), width, height, lamp, absorbing, openings


def run_world(
    path: Path,
    fan_bound: int,
    max_intervals: int = 400,
    quiet: bool = False,
    phase_rate: tuple[int, int] | None = None,
    mode: str = "coin",
    world_fan: bool = False,
    coin_turn: float = math.pi,
    uniform: bool = False,
):
    world, (n, d), width, height, lamp, absorbing, openings = load_world(path)
    if phase_rate is not None:
        n, d = phase_rate
    modulus = world["N"]
    fan = [(v[0], v[1]) for v in world["directions"]] if world_fan else primitive_fan_2d(fan_bound)
    lamp_dirs = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
    for v in lamp_dirs:
        if v not in fan:
            fan.append(v)
    turns = lamp["lamp"].get("turns", [0] * len(lamp_dirs))
    board = Board(
        width,
        height,
        fan,
        absorbing,
        (n, d),
        modulus,
        mode=mode,
        openings=openings,
        coin_turn=coin_turn,
        uniform=uniform,
    )
    # the birth: the lamp's one-input fan, equal weights, the turns as phase offsets
    amplitude = 1.0 / math.sqrt(len(lamp_dirs))
    for v, t in zip(lamp_dirs, turns, strict=True):
        angle = 2 * math.pi * t / modulus
        board.amp[board.index[v], lamp["position"][0], lamp["position"][1]] += amplitude * complex(
            math.cos(angle), math.sin(angle)
        )
    live_norm = []
    for _ in range(max_intervals):
        board.step()
        live_norm.append(board.norm())
        if board.norm() < 1e-6:
            break
    screen_x = max(x for (x, _y) in absorbing if absorbing[(x, _y)].startswith("screen"))
    pixels = [absorbing.get((screen_x, y), None) for y in range(height)]
    weights = [abs(board.pointer.get(name, 0j)) ** 2 if name else 0.0 for name in pixels]
    walls = sum(abs(v) ** 2 for k, v in board.pointer.items() if k.startswith("wall"))
    faces = {k: abs(v) ** 2 for k, v in board.pointer.items() if k.startswith("face")}
    screen = sum(weights)
    total = screen + walls + sum(faces.values())
    return {
        "world": path.stem,
        "fan": len(fan),
        "intervals": board.tau,
        "live_norm_end": board.norm(),
        "absorbed_norm": board.absorbed_norm,
        "screen_x": screen_x,
        "weights": weights,
        "screen": screen,
        "walls": walls,
        "faces": faces,
        "total": total,
        "openings": openings,
        "lamp": lamp,
        "n_d": (n, d),
        "modulus": modulus,
        "pointer": board.pointer,
        "pixels": pixels,
        "width": width,
        "height": height,
    }


def clicks(weights: list[float], records: int = RECORDS) -> list[int]:
    scale = 2**40
    pairs = [(int(w * scale), 1) for w in weights]
    counts = [0] * len(weights)
    r, w = WHEEL
    for ordinal in range(1, records + 1):
        u = (ordinal * r) % w
        k = cell_of(pairs, w, u)
        if k is not None:
            counts[k] += 1
    return counts


def section_a() -> None:
    print(
        "A. THE COPY RULE AGAINST THE COIN IN ONE DIMENSION (K = 2), from one birth of amplitude 1 at x = 0"
    )
    print(
        "   the copy rule: a(x, t + 1) = (a(x - 1, t) + a(x + 1, t)) / sqrt 2, the growth factor sqrt 2 cos k per interval;"
    )
    print(
        "   the coin: out_right = a_left_arrival - ... : the Grover coin over two outputs is [[0, 1], [1, 0]]: a swap, and"
    )
    print(
        "   the wave in one dimension needs the two-output coin with a sign, the Hadamard [[1, 1], [1, -1]] / sqrt 2 (K = 2 is"
    )
    print(
        "   the one K where Grover's (2 / K) J - I is a permutation); shown with Hadamard here, the two-dimensional walks use Grover's."
    )
    L = 401
    c = L // 2
    a = np.zeros(L)
    a[c] = 1.0
    hr = np.zeros(L)
    hl = np.zeros(L)
    hr[c] = hl[c] = 1 / math.sqrt(2)
    for t in (16, 64, 128):
        while True:
            # copy rule
            a = (np.roll(a, 1) + np.roll(a, -1)) / math.sqrt(2)
            # Hadamard walk
            r_in = np.roll(hr, 1)
            l_in = np.roll(hl, -1)
            hr, hl = (r_in + l_in) / math.sqrt(2), (r_in - l_in) / math.sqrt(2)
            globals()["_t"] = globals().get("_t", 0) + 1
            if globals()["_t"] == t:
                break
        x = np.arange(L) - c
        norm_a = float((a**2).sum())
        rms_a = math.sqrt(float((x * x * a * a).sum()) / norm_a)
        p = hr**2 + hl**2
        norm_h = float(p.sum())
        rms_h = math.sqrt(float((x * x * p).sum()) / norm_h)
        front_h = int(np.max(np.abs(x[p > 1e-3 * p.max()])))
        print(
            f"   t = {t:3d}: the copy rule's norm {norm_a:.4g} (grows), its rms spread {rms_a:.2f} = {rms_a / math.sqrt(t):.3f} sqrt t (diffusive);"
            f" the coin's norm {norm_h:.6f} (conserved), its rms spread {rms_h:.2f} = {rms_h / t:.3f} t (ballistic), its front at |x| = {front_h}"
        )
    print()


def section_b() -> None:
    print(
        "B. THE COIN WALK'S FRONT ON AN EMPTY BOARD, one birth at the centre on every direction of the fan, equal amplitudes"
    )
    for bound in (1, 3, 6):
        fan = primitive_fan_2d(bound)
        size = 161
        board = Board(size, size, fan, {}, (8591334592, 1073741824), 64)
        amp = 1 / math.sqrt(len(fan))
        for v in fan:
            board.amp[board.index[v], size // 2, size // 2] = amp
        radii = {}
        for tau in range(1, 65):
            board.step()
            if tau in (32, 64):
                p = (np.abs(board.amp) ** 2).sum(axis=0)
                xs, ys = np.nonzero(p > 1e-4 * p.max())
                c = size // 2
                by_angle = {}
                for x, y in zip(xs, ys, strict=True):
                    ang = int(round(math.degrees(math.atan2(y - c, x - c)) / 15.0)) * 15
                    r = math.hypot(x - c, y - c)
                    by_angle[ang] = max(by_angle.get(ang, 0.0), r)
                radii[tau] = by_angle
        norm = board.norm() + board.absorbed_norm
        for tau, by_angle in radii.items():
            rs = [by_angle[a] for a in sorted(by_angle)]
            print(
                f"   fan Manhattan <= {bound} (K = {len(fan)}): age {tau}: the front's radius by 15-degree sector, min {min(rs):.1f}, max {max(rs):.1f},"
                f" mean {sum(rs) / len(rs):.1f} Links; the flight table's c tau = {tau / math.sqrt(3):.1f}; the anisotropy (max - min) / mean {(max(rs) - min(rs)) / (sum(rs) / len(rs)):.3f}"
            )
        print(
            f"   fan Manhattan <= {bound}: the norm after 64 intervals {norm:.9f} (1 under the coin; the escapes counted)"
        )
    print()


def section_c(fan_bound: int) -> None:
    print(
        f"C. THE SINGLE OPENING AND THE TWO SLITS UNDER THE COIN, the in-plane fan of Manhattan <= {fan_bound} plus the lamp's directions"
    )
    for rel, w_nodes, pin, near in (
        ("docs/designs/fail_rows/opening_w27.json", 27, PIN_W27, NEAR_FIELD_W27),
        ("docs/designs/fail_rows/opening_w9.json", 9, PIN_W9, NEAR_FIELD_W9),
    ):
        out = run_world(ROOT / rel, fan_bound)
        n, d = out["n_d"]
        modulus = out["modulus"]
        period = modulus * d / n
        wavelength = period * Q / math.isqrt(3 * Q * Q)
        centre = out["lamp"]["position"][1]
        openings = out["openings"]
        wall_x = min(x for x, _ in openings)
        distance = out["screen_x"] - wall_x
        weights = out["weights"]
        width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
        product = w_nodes * width_s / wavelength
        pixels = out["pixels"]
        others = [k for k in out["pointer"] if not k.startswith("screen")]
        cell_weights = weights + [abs(out["pointer"][k]) ** 2 for k in others]
        all_counts = clicks(cell_weights)
        counts = all_counts[: len(pixels)]
        width_c, peak_c, left_c, right_c = fwhm_in_s([float(c) for c in counts], centre, distance)
        product_c = w_nodes * width_c / wavelength
        print(
            f"   {out['world']}: w = {w_nodes}, L = {distance}, lambda = {wavelength:.4f}, the fan K = {out['fan']}; the walk ended after {out['intervals']} intervals,"
            f" the live norm {out['live_norm_end']:.2e}, the absorbed norm {out['absorbed_norm']:.6f} (1 under the coin)"
        )
        print(
            f"      the shares (COMPUTATION, the cells' weights over their sum): the screen {out['screen'] / out['total']:.4f}, the wall {out['walls'] / out['total']:.4f},"
            f" the faces {sum(out['faces'].values()) / out['total']:.4f} ({', '.join(f'{k} {v / out["total"]:.4f}' for k, v in sorted(out['faces'].items()))})"
        )
        print(
            f"      the screen's exact sum: the peak at y = {peak}, the half-maximum crossings s = {left:.4f} and {right:.4f}, FWHM(sin theta) = {width_s:.4f},"
            f" w x FWHM / lambda = {product:.3f}; the pin at the pixel grain and the Fresnel number {near} (22.2's band {pin[0]} +- {pin[1]}: {'inside' if abs(product - pin[0]) <= pin[1] else 'OUTSIDE'});"
            f" the far field {FAR_FIELD}; the refuting bound {REFUTES_BELOW}: {'above' if product >= REFUTES_BELOW else 'BELOW'}"
        )
        print(
            f"      the clicks of {RECORDS} births under the golden wheel over every cell (the pixels, the wall's Nodes, the faces): the screen {sum(counts)} of {RECORDS},"
            f" the peak at y = {peak_c} ({counts[peak_c]}), FWHM {width_c:.4f}, w x FWHM / lambda = {product_c:.3f}"
        )
        print(
            f"      the screen weights y = {centre - 20} .. {centre + 20} (per mille of the screen's sum): "
            + " ".join(
                f"{1000 * weights[y] / max(out['screen'], 1e-300):.1f}"
                for y in range(centre - 20, centre + 21)
            )
        )
    out = run_world(ROOT / "examples/events/amplitude/slits_huygens.json", fan_bound)
    n, d = out["n_d"]
    modulus = out["modulus"]
    period = modulus * d / n
    wavelength = period * Q / math.isqrt(3 * Q * Q)
    weights = out["weights"]
    centre = out["lamp"]["position"][1]
    openings = sorted(set(y for _, y in out["openings"]))
    separation = openings[-1] - openings[0]
    distance = out["screen_x"] - max(x for x, _ in out["openings"])
    # the visibility within the central envelope: the max and the min over the central fringes
    central = [weights[y] for y in range(centre - 15, centre + 16)]
    peaks = [
        i
        for i in range(1, len(central) - 1)
        if central[i] >= central[i - 1] and central[i] >= central[i + 1]
    ]
    troughs = [
        i
        for i in range(1, len(central) - 1)
        if central[i] <= central[i - 1] and central[i] <= central[i + 1]
    ]
    i_max = max(central)
    i_min = min(central[i] for i in troughs) if troughs else 0.0
    visibility = (i_max - i_min) / (i_max + i_min) if i_max + i_min else 0.0
    fringe = wavelength * distance / separation
    print(
        f"   {out['world']}: the openings at y = {openings}, the separation {separation}, L = {distance}, lambda = {wavelength:.4f}, the fringe period lambda L / d = {fringe:.2f} pixels;"
        f" the fan K = {out['fan']}; the walk ended after {out['intervals']} intervals, the absorbed norm {out['absorbed_norm']:.6f}"
    )
    print(
        f"      the shares: the screen {out['screen'] / out['total']:.4f}, the wall {out['walls'] / out['total']:.4f}, the faces {sum(out['faces'].values()) / out['total']:.4f}"
    )
    print(
        f"      the screen weights y = {centre - 15} .. {centre + 15} (per mille of the screen's sum): "
        + " ".join(f"{1000 * w / max(out['screen'], 1e-300):.1f}" for w in central)
    )
    print(
        f"      the visibility over the central fringes (I_max - I_min) / (I_max + I_min) = {visibility:.4f} (the fan's registered 0.9659, history); the peaks at {[centre - 15 + i for i in peaks]}"
    )
    print()


def section_d() -> None:
    print(
        "D. THE REGISTERED BARS UNDER THE COIN WITH THE SIX HEADINGS (K = 6, the coin on the arrivals at each Node, the outputs on +-y and +-z escaping at the next step, y and z open)"
    )
    for rel, _lamp_x, sets in (
        (
            "examples/events/bell/read.json",
            10,
            {7: "alice_plus", 4: "alice_minus", 17: "bob_plus", 18: "bob_minus"},
        ),
        (
            "examples/events/amplitude/malus_a.json",
            0,
            {4: "first (read, non-absorbing: counted here as absorbing for the share)", 6: "second"},
        ),
    ):
        world = json.loads((ROOT / rel).read_text())
        width = world["shape"][0]
        n, d = 8591334592, 1073741824
        absorbing = {(x, 0): name for x, name in sets.items()}
        fan = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]  # the two z headings escape as the y ones do: counted with y
        board = Board(width, 1, fan, absorbing, (n, d), world["N"])
        lamp = next(m for m in world["measured"] if "lamp" in m)
        dirs = [(v[0], v[1]) for v in lamp["lamp"]["directions"]]
        amp = 1 / math.sqrt(len(dirs))
        for v in dirs:
            board.amp[board.index[v], lamp["position"][0], 0] += amp
        # K = 6 in the coin although only four directions are on the plane: the z outputs are escapes too
        K6 = 6
        for _ in range(200):
            board.tau += 1
            tau = board.tau
            arrivals = np.zeros_like(board.amp)
            stepped = False
            for k, line in enumerate(board.lines):
                if line.made(tau) == line.made(tau - 1):
                    continue
                stepped = True
                sx, sy = line.steps[0]
                moving = board.amp[k].copy()
                board.amp[k] = 0
                if sy != 0:
                    for x in range(width):
                        if abs(moving[x, 0]):
                            board.deposit("escape:y,z", complex(moving[x, 0]), tau, k)
                    continue
                shifted = np.zeros_like(moving)
                if sx > 0:
                    shifted[1:, 0] = moving[:-1, 0]
                    if abs(moving[-1, 0]):
                        board.deposit("face:+x", complex(moving[-1, 0]), tau, k)
                else:
                    shifted[:-1, 0] = moving[1:, 0]
                    if abs(moving[0, 0]):
                        board.deposit("face:-x", complex(moving[0, 0]), tau, k)
                for x in range(width):
                    if abs(shifted[x, 0]) and (x, 0) in absorbing:
                        board.deposit(absorbing[(x, 0)], complex(shifted[x, 0]), tau, k)
                        shifted[x, 0] = 0
                arrivals[k] = shifted
            if not stepped:
                continue
            total = arrivals.sum(axis=0)
            out = arrivals - np.broadcast_to((2.0 / K6) * total, board.amp.shape)
            # the two z outputs, -(2 / K6) total each, escape at their next step
            z_out = -(2.0 / K6) * total
            board.amp += out
            for x in range(width):
                if abs(z_out[x, 0]):
                    board.deposit("escape:y,z", complex(z_out[x, 0]), tau + 1, 2)
                    board.deposit("escape:y,z", complex(z_out[x, 0]), tau + 1, 2)
            if board.norm() < 1e-9:
                break
        total = sum(abs(v) ** 2 for v in board.pointer.values())
        shares = {k: abs(v) ** 2 / total for k, v in board.pointer.items()}
        print(
            f"   {rel}: the lamp at x = {lamp['position'][0]} on {dirs}; the walk ended after {board.tau} intervals; the shares of the cells (COMPUTATION):"
        )
        for k in sorted(shares, key=lambda s: -shares[s]):
            print(f"      {k}: {shares[k]:.5f}")
        named = {k: v for k, v in shares.items() if not k.startswith(("escape", "face"))}
        if len(named) >= 2:
            ks = list(named)
            print(
                f"      the ratio of the sets' shares {ks[0]} : {ks[1]} = {named[ks[0]] / max(named[ks[1]], 1e-300):.3f}; the registered arrangement reads the two outcomes at different depths,"
                " so this ratio, not the rotation's, would set the cells: NOT READABLE under the split (Reviewer 3's D3); the re-arranged bar of DESIGN.md section 7 puts both outcomes at one depth"
            )
    print()


def section_v() -> None:
    print(
        "V. THE READING MACHINERY CHECKED ON THE LAW AS BUILT: straight lines, the one-time equal split over the world's forward fan at the opening's Nodes"
    )
    print(
        "   (the registered rerelease, its 601 forward directions), the screen read as above: against RUN_10's exact sums 0.916 (w = 27) and 0.891 (w = 9)"
    )
    for rel, w_nodes, near in (
        ("docs/designs/fail_rows/opening_w27.json", 27, NEAR_FIELD_W27),
        ("docs/designs/fail_rows/opening_w9.json", 9, NEAR_FIELD_W9),
    ):
        out = run_world(ROOT / rel, 0, max_intervals=320, mode="apparatus", world_fan=True)
        n, d = out["n_d"]
        modulus = out["modulus"]
        wavelength = (modulus * d / n) * Q / math.isqrt(3 * Q * Q)
        centre = out["lamp"]["position"][1]
        wall_x = min(x for x, _ in out["openings"])
        distance = out["screen_x"] - wall_x
        weights = out["weights"]
        width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
        product = w_nodes * width_s / wavelength
        smooth = sum(
            abs(weights[y] - (weights[y - 1] + weights[y + 1]) / 2) for y in range(1, len(weights) - 1)
        ) / max(sum(weights), 1e-300)
        print(
            f"   {out['world']}: the fan K = {out['fan']}; the walk ended after {out['intervals']} intervals, the absorbed norm {out['absorbed_norm']:.4f} (the one-time split is not unitary over re-met paths, amplitude-v1 2.5);"
            f" the screen's share {out['screen'] / out['total']:.4f}; the peak at y = {peak}, FWHM(sin theta) = {width_s:.4f}, w x FWHM / lambda = {product:.3f} against {near}; the roughness {smooth:.3f}"
        )
        print(
            "      the screen weights y = 60 .. 100 (per mille): "
            + " ".join(
                f"{1000 * weights[y] / max(out['screen'], 1e-300):.1f}"
                for y in range(centre - 20, centre + 21)
            )
        )
    print()


def section_e(fan_bound: int) -> None:
    print(
        f"E. THE COIN WALK'S OWN WAVELENGTH: the single opening w = 27 at slower clocks (the phase rate n / d in turns of N = 64 per interval), the fan Manhattan <= {fan_bound}"
    )
    print(
        "   the ray law's lambda = c N d / n is exact at every rate; the coin walk is a lattice wave with its own dispersion, isotropic only where lambda is many Links:"
    )
    print(
        "   at each rate the screen's exact sum, its FWHM in sin theta, w x FWHM / lambda against the far field's 0.886 lambda / w (the Fresnel number w^2 / (lambda L) beside)"
    )
    for n, d in ((8591334592, 1073741824), (4, 1), (2, 1), (1, 1), (1, 2)):
        out = run_world(
            ROOT / "docs/designs/fail_rows/opening_w27.json",
            fan_bound,
            max_intervals=600,
            phase_rate=(n, d),
        )
        modulus = out["modulus"]
        period = modulus * d / n
        wavelength = period * Q / math.isqrt(3 * Q * Q)
        centre = out["lamp"]["position"][1]
        wall_x = min(x for x, _ in out["openings"])
        distance = out["screen_x"] - wall_x
        weights = out["weights"]
        width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
        product = 27 * width_s / wavelength
        fresnel = 27 * 27 / (wavelength * distance)
        smooth = sum(
            abs(weights[y] - (weights[y - 1] + weights[y + 1]) / 2) for y in range(1, len(weights) - 1)
        ) / max(sum(weights), 1e-300)
        print(
            f"   n / d = {n} / {d}: the period {period:.2f} intervals, lambda = {wavelength:.2f} Links, the Fresnel number {fresnel:.3f}; the screen's share {out['screen'] / out['total']:.4f};"
            f" the peak at y = {peak}, FWHM(sin theta) = {width_s:.4f}, w x FWHM / lambda = {product:.3f} (the far field 0.886); the pixel-to-pixel roughness {smooth:.3f}"
        )
        print(
            "      the screen weights y = 60 .. 100 (per mille): "
            + " ".join(
                f"{1000 * weights[y] / max(out['screen'], 1e-300):.1f}"
                for y in range(centre - 20, centre + 21)
            )
        )
    print()


def section_f(fan_bound: int) -> None:
    print(
        "F. THE COIN'S ONE PARAMETER: the unitary coin symmetric in the outputs is exp(i eps P), P the projector on the symmetric vector;"
    )
    print(
        "   eps = pi is Grover's, eps -> 0 the straight rays; the single opening w = 27 at the registered clock (lambda = 4.65) and at n / d = 2 (lambda = 18.6),"
    )
    print(
        f"   the fan Manhattan <= {fan_bound}: the screen's share, w x FWHM / lambda (the pins 0.916 at lambda = 4.65, Fresnel 1.45; the far field 0.886 at lambda = 18.6, Fresnel 0.36), the roughness"
    )
    for (n, d), pin in (((8591334592, 1073741824), 0.916), ((2, 1), 0.886)):
        for turn_steps in (1, 2, 4, 8, 16, 32):
            eps = 2 * math.pi * turn_steps / 64
            out = run_world(
                ROOT / "docs/designs/fail_rows/opening_w27.json",
                fan_bound,
                max_intervals=500,
                phase_rate=(n, d),
                coin_turn=eps,
            )
            modulus = out["modulus"]
            wavelength = (modulus * d / n) * Q / math.isqrt(3 * Q * Q)
            centre = out["lamp"]["position"][1]
            wall_x = min(x for x, _ in out["openings"])
            distance = out["screen_x"] - wall_x
            weights = out["weights"]
            width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
            product = 27 * width_s / wavelength
            smooth = sum(
                abs(weights[y] - (weights[y - 1] + weights[y + 1]) / 2)
                for y in range(1, len(weights) - 1)
            ) / max(sum(weights), 1e-300)
            print(
                f"   lambda = {wavelength:5.2f}, eps = {turn_steps:2d} / 64 turn: the screen's share {out['screen'] / out['total']:.3f}, the peak at y = {peak}, w x FWHM / lambda = {product:.3f} (the pin {pin}), the roughness {smooth:.3f};"
                f" the absorbed norm {out['absorbed_norm']:.4f} after {out['intervals']} intervals"
            )
            print(
                "      y = 60 .. 100 (per mille): "
                + " ".join(
                    f"{1000 * weights[y] / max(out['screen'], 1e-300):.1f}"
                    for y in range(centre - 20, centre + 21)
                )
            )
    print()


def section_g() -> None:
    print(
        "G. THE HOP (pace B) FOR COMPARISON: the four headings, every row one Link per interval (the pace 1, not the flight table's), Grover's coin (eps = pi),"
    )
    print(
        "   the single opening w = 27 at slow clocks (lambda = the period in Links at pace 1): the pattern, its width against the far field and the Fresnel sum"
    )
    for n, d in ((4, 1), (2, 1), (1, 1)):
        out = run_world(
            ROOT / "docs/designs/fail_rows/opening_w27.json",
            1,
            max_intervals=500,
            phase_rate=(n, d),
            uniform=True,
        )
        modulus = out["modulus"]
        wavelength = (modulus * d / n) * 1.0
        centre = out["lamp"]["position"][1]
        wall_x = min(x for x, _ in out["openings"])
        distance = out["screen_x"] - wall_x
        weights = out["weights"]
        width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
        product = 27 * width_s / wavelength
        fresnel = 27 * 27 / (wavelength * distance)
        smooth = sum(
            abs(weights[y] - (weights[y - 1] + weights[y + 1]) / 2) for y in range(1, len(weights) - 1)
        ) / max(sum(weights), 1e-300)
        print(
            f"   n / d = {n} / {d}: lambda = {wavelength:.1f} Links, the Fresnel number {fresnel:.3f}; the screen's share {out['screen'] / out['total']:.3f}; the peak at y = {peak}, w x FWHM / lambda = {product:.3f} (the far field 0.886); the roughness {smooth:.3f}; the absorbed norm {out['absorbed_norm']:.4f}"
        )
        print(
            "      y = 60 .. 100 (per mille): "
            + " ".join(
                f"{1000 * weights[y] / max(out['screen'], 1e-300):.1f}"
                for y in range(centre - 20, centre + 21)
            )
        )
    print()


def section_h() -> None:
    print(
        "H. THE SCALAR LATTICE WAVE FOR COMPARISON (the field form, build (i), with two time levels): psi(t + 1) = c^2 sum over the four in-plane"
    )
    print(
        "   neighbours of psi(t) + (2 - 4 c^2) psi(t) - psi(t - 1), c^2 = 1 / 3 (the flight table's pace is the lattice wave's stability limit in three"
    )
    print(
        "   dimensions); the source the aperture itself, psi = 1 on the opening's 27 Nodes at t = 0 (the plane wave the registered lamp's turns make);"
    )
    print(
        "   the field at an absorbing Node is deposited into its cell with the record's phase at the age and zeroed (the click); the far edges damped;"
    )
    print(
        "   the single opening w = 27 at the registered clock and slower ones, the same reading: the pattern, its width against the pins"
    )
    world, (n0, d0), width, height, lamp, absorbing, openings = load_world(
        ROOT / "docs/designs/fail_rows/opening_w27.json"
    )
    modulus = world["N"]
    mask = np.zeros((width, height), dtype=bool)
    for x, y in absorbing:
        mask[x, y] = True
    c2 = 1.0 / 3.0
    centre = lamp["position"][1]
    wall_x = min(x for x, _ in openings)
    screen_x = max(x for (x, _y) in absorbing if absorbing[(x, _y)].startswith("screen"))
    distance = screen_x - wall_x
    damp = np.ones((width, height))
    for i in range(8):
        f = (i + 1) / 9.0
        damp[width - 1 - i, :] *= f
        damp[:, i] *= f
        damp[:, height - 1 - i] *= f
    for i in range(2):
        damp[i, :] *= (i + 1) / 3.0
    for (n, d), pin_text in (
        (
            (8591334592, 1073741824),
            "the pin at the pixel grain and Fresnel 1.45: 0.916; 22.2's band 0.92 +- 0.03",
        ),
        ((4, 1), "the far field 0.886 (Fresnel 0.73)"),
        ((2, 1), "the far field 0.886 (Fresnel 0.37)"),
    ):
        period = modulus * d / n
        wavelength = period * math.sqrt(c2)
        prev = np.zeros((width, height))
        cur = np.zeros((width, height))
        for x, y in openings:
            cur[x, y] = 1.0
        pointer: dict[str, complex] = {}
        for tau in range(1, 1200):
            lap = np.zeros_like(cur)
            lap[1:, :] += cur[:-1, :]
            lap[:-1, :] += cur[1:, :]
            lap[:, 1:] += cur[:, :-1]
            lap[:, :-1] += cur[:, 1:]
            nxt = c2 * lap + (2 - 4 * c2) * cur - prev
            angle = 2 * math.pi * (n / d) * tau / modulus
            rot = complex(math.cos(angle), math.sin(angle))
            hit = nxt * mask
            for x, y in zip(*np.nonzero(hit), strict=True):
                name = absorbing[(int(x), int(y))]
                pointer[name] = pointer.get(name, 0j) + float(hit[x, y]) * rot
            nxt = nxt * ~mask * damp
            prev, cur = cur, nxt
            if tau > 400 and float(np.abs(cur).max()) < 1e-6:
                break
        weights = [abs(pointer.get(absorbing.get((screen_x, y), ""), 0j)) ** 2 for y in range(height)]
        total_screen = sum(weights)
        width_s, peak, left, right = fwhm_in_s(weights, centre, distance)
        product = 27 * width_s / wavelength
        fresnel = 27 * 27 / (wavelength * distance)
        smooth = sum(
            abs(weights[y] - (weights[y - 1] + weights[y + 1]) / 2) for y in range(1, len(weights) - 1)
        ) / max(total_screen, 1e-300)
        print(
            f"   n / d = {n} / {d}: lambda = {wavelength:.2f} Links, the Fresnel number {fresnel:.3f}; the peak at y = {peak}, the crossings s = {left:.4f} and {right:.4f}, FWHM(sin theta) = {width_s:.4f},"
            f" w x FWHM / lambda = {product:.3f} ({pin_text}); the roughness {smooth:.3f}; {tau} intervals"
        )
        print(
            "      y = 60 .. 100 (per mille): "
            + " ".join(
                f"{1000 * weights[y] / max(total_screen, 1e-300):.1f}"
                for y in range(centre - 20, centre + 21)
            )
        )
    print()


def main() -> None:
    print(
        "THE PINS OF THE EVENT SPLIT BEFORE ANY RUN (COMPUTATION; the coin walk offline, no engine run, nothing registered)\n"
    )
    section_v()
    section_a()
    section_b()
    section_c(3)
    section_d()
    section_e(3)
    section_f(3)
    section_g()
    section_h()


if __name__ == "__main__":
    main()
