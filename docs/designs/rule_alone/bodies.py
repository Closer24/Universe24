"""Bodies for the rule-alone runs (records 2134, 2130; ALGEBRA.md 9.98 (3), 9.91 (11)): a body
is a record with a well (its lowered pair on the Nodes of its support, the kind elsewhere), a
count s written by the hold at its Nodes into the gravity record's time part, and the one seam:
the well hops with the record's envelope centroid. The initial record is the well's bound mode,
a HOST computation of the shipped massive generator's own operator (its `seed_on_the_mode`),
taken here as a start value and nothing else. The gravity time part is its own record, stepped
by the same rule with the pair [1, 1] and no content (its pace Gamma), the hold writing s at the
bodies' Nodes each interval; its start is the static level by relaxation (HOST floats rounded
to integers)."""

from __future__ import annotations

import copy
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_alone as R  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


massive = load(ROOT / "examples" / "events" / "massive_record" / "make_worlds.py", "rule_alone_massive")

KIND = (800, 850)  # the species that binds a well of side 5 in three dimensions (9.98 (9) (a))
WELL = (800, 801)
SIDE = 5
SEED = 1 << 17  # the record's amplitude (the rule's total stays within int64 up to about 2^19)


@dataclass
class Body:
    centre: list[int]
    amount: int
    side: int = SIDE
    kind: tuple[int, int] = KIND
    well: tuple[int, int] = WELL

    def corner(self) -> list[int]:
        return [c - self.side // 2 for c in self.centre]

    def mask(self, shape: tuple[int, int, int]) -> np.ndarray:
        out = np.zeros(shape, dtype=bool)
        corner = self.corner()
        index = np.ix_(*[[(corner[a] + i) % shape[a] for i in range(self.side)] for a in range(3)])
        out[index] = True
        return out

    def pairs(self, shape: tuple[int, int, int]) -> tuple[np.ndarray, np.ndarray]:
        num = np.full(shape, self.kind[0], dtype=R.INT)
        den = np.full(shape, self.kind[1], dtype=R.INT)
        mask = self.mask(shape)
        num[mask] = self.well[0]
        den[mask] = self.well[1]
        return num, den


def pair_cosine(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    """cos omega of the pair at each Node, num / den: the engine's own norm reads the record's
    envelope with it (9.19); the moving record rotates within a percent of it."""
    return num.astype(np.float64) / den.astype(np.float64)


def boundary_of(wrap: tuple[bool, bool, bool]) -> dict[str, str]:
    return {name: "periodic" if w else "open" for name, w in zip("xyz", wrap, strict=True)}


def bound_mode(
    shape: tuple[int, int, int], wrap: tuple[bool, bool, bool], body: Body
) -> tuple[np.ndarray, list[int]]:
    """The body's bound mode over the whole board at the amplitude SEED, alone on its board (9.96
    (4)), by the shipped generator's operator (HOST); returns the profile and the mode's clock
    [a, b] (2 cos omega_b = a / b)."""
    block = {
        "position": body.corner(),
        "extents": [body.side] * 3,
        "amount": body.amount,
        "pair": list(body.well),
        "kind": list(body.kind),
        "seed": SEED,
        "charge": 0,
    }
    document = massive.world(
        "rule-alone",
        "CHECK",
        list(shape),
        boundary_of(wrap),
        list(body.kind),
        [block],
        10,
        seed_profile=False,
    )
    if not all(wrap):
        document["face_depth"] = 1
    alone = copy.deepcopy(document)
    massive.seed_on_the_mode(alone)
    entry = alone["measured"][0]
    return np.array(entry["seed"], dtype=R.INT).reshape(shape), [int(v) for v in entry["clock"]]


def moving_record(
    profile: np.ndarray,
    body: Body,
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
    axis: int,
    speed: float,
    clock: list[int],
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    """The mode times the character of K along `axis` at the group pace `speed`, the two levels
    split about the standing start with the later sample as now (ALGEBRA.md 9.98 (9) (b)):
    now = round(p cos(K dx - omega_K / 2)), before = round(p cos(K dx + omega_K / 2)). K and
    omega_K from the mode's own dispersion (the generator's HOST reading of its integers)."""
    import math

    document = {
        "measured": [
            {
                "position": body.corner(),
                "extents": [body.side] * 3,
                "pair": list(body.well),
                "kind": list(body.kind),
                "seed": profile.ravel().tolist(),
                "clock": clock,
                "family": "matter",
            }
        ],
        "shape": list(shape),
        "boundary": boundary_of(wrap),
        "families": [{"name": "matter", "pair": "body"}],
    }
    two_cos_rest, quotient = massive.mode_dispersion(document, 0, axis)
    wavenumber, rotation = massive.moving_rotation(float(two_cos_rest), float(quotient), abs(speed))
    omega = math.acos((float(two_cos_rest) - (1.0 - math.cos(wavenumber)) * float(quotient)) / 2.0)
    coordinate = np.arange(shape[axis], dtype=np.int64) - body.centre[axis]
    if wrap[axis]:
        coordinate = (coordinate + shape[axis] // 2) % shape[axis] - shape[axis] // 2
    phase = math.copysign(1.0, speed) * wavenumber * coordinate.astype(np.float64)
    form = [1, 1, 1]
    form[axis] = shape[axis]
    now = np.rint(profile * np.cos(phase - omega / 2.0).reshape(form)).astype(R.INT)
    before = np.rint(profile * np.cos(phase + omega / 2.0).reshape(form)).astype(R.INT)
    return (
        now,
        before,
        {
            "K": wavenumber,
            "omega_K": omega,
            "rotation_at_centre": rotation,
            "omega_rest": math.acos(float(two_cos_rest) / 2.0),
        },
    )


def static_content(
    shape: tuple[int, int, int], wrap: tuple[bool, bool, bool], bodies: list[Body], sweeps: int = 3000
) -> np.ndarray:
    """The gravity time part's static level: the lattice Laplace equation with the level s on
    each body's Nodes and 0 beyond an open face, by Jacobi relaxation (HOST floats), rounded."""
    field = np.zeros(shape, dtype=np.float64)
    fixed = np.zeros(shape, dtype=bool)
    for body in bodies:
        mask = body.mask(shape)
        field[mask] = body.amount
        fixed |= mask
    values = field.copy()
    for _ in range(sweeps):
        total = np.zeros_like(field)
        for axis in range(3):
            for shift in (1, -1):
                rolled = np.roll(field, shift, axis=axis)
                if not wrap[axis]:
                    edge = [slice(None)] * 3
                    edge[axis] = slice(0, 1) if shift == 1 else slice(shape[axis] - 1, shape[axis])
                    rolled[tuple(edge)] = 0.0
                total += rolled
        field = total / 6.0
        field[fixed] = values[fixed]
    return np.rint(field).astype(R.INT)


def hold(
    gravity_now: np.ndarray, gravity_before: np.ndarray, bodies: list[Body], shape: tuple[int, int, int]
) -> None:
    """The bodies' counts written at their Nodes into the gravity time part, both levels."""
    for body in bodies:
        mask = body.mask(shape)
        gravity_now[mask] = body.amount
        gravity_before[mask] = body.amount


def window_centroid(
    weight: np.ndarray,
    centre: list[int],
    half: int,
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> tuple[float, float, float]:
    """The record's centroid over its support (9.98 (8)): the box of half-width `half` about
    the well's centre, wrapped on a periodic axis; a per-body tally, the seam's."""
    total = 0.0
    moments = [0.0, 0.0, 0.0]
    offsets = [np.arange(-half, half + 1) for _ in range(3)]
    index = np.ix_(
        *[
            (centre[a] + offsets[a]) % shape[a]
            if wrap[a]
            else np.clip(centre[a] + offsets[a], 0, shape[a] - 1)
            for a in range(3)
        ]
    )
    box = weight[index]
    total = float(box.sum())
    if total <= 0.0:
        return (float(centre[0]), float(centre[1]), float(centre[2]))
    for a in range(3):
        form = [1, 1, 1]
        form[a] = 2 * half + 1
        moments[a] = float((box * offsets[a].astype(np.float64).reshape(form)).sum()) / total
    return (centre[0] + moments[0], centre[1] + moments[1], centre[2] + moments[2])


def lone_static_field(
    shape: tuple[int, int, int], wrap: tuple[bool, bool, bool], body: Body
) -> np.ndarray:
    """The static content of one body at the board's middle (relaxation, HOST), to be shifted to
    each well: the gravity time part's steady level without the runner's reflecting faces."""
    middle = Body(
        [shape[0] // 2, shape[1] // 2, shape[2] // 2], body.amount, body.side, body.kind, body.well
    )
    return static_content(shape, wrap, [middle])


def shifted_content(field: np.ndarray, bodies: list[Body], shape: tuple[int, int, int]) -> np.ndarray:
    """The bodies' static levels, each rolled from the board's middle to its well, summed."""
    total = np.zeros(shape, dtype=R.INT)
    for body in bodies:
        shift = [body.centre[a] - shape[a] // 2 for a in range(3)]
        total += np.roll(field, shift, axis=(0, 1, 2))
    return total


def current_pace(
    now: np.ndarray,
    before: np.ndarray,
    num: np.ndarray,
    den: np.ndarray,
    cos_omega: np.ndarray,
    centre: list[int],
    half: int,
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> tuple[float, float, float]:
    """THE SECOND SEAM TRIED (a per-body tally of the rule's own integers, 9.98 (4)'s current):
    the record's pace over its support, v_a = SUM (num / den) J_a / (3 SUM F), J_a(i) = now_(i+a)
    before_i - before_(i+a) now_i the current through the Port along +a, F the form at the Node;
    on the moving mode at v = 0.05, 0.1, 0.2 this reads 0.9995, 1.017, 1.083 of v (HOST, the
    probe of 2026-09-26). The well hops by one Node when the accumulated pace passes one Link."""
    n = now.astype(np.float64)
    b = before.astype(np.float64)
    ratio = num.astype(np.float64) / den.astype(np.float64)
    form = n * n + b * b - 2.0 * n * b * cos_omega
    offsets = [np.arange(-half, half + 1) for _ in range(3)]
    index = np.ix_(
        *[
            (centre[a] + offsets[a]) % shape[a]
            if wrap[a]
            else np.clip(centre[a] + offsets[a], 0, shape[a] - 1)
            for a in range(3)
        ]
    )
    total_form = float(form[index].sum())
    if total_form <= 0.0:
        return (0.0, 0.0, 0.0)
    out = []
    for axis in range(3):
        current = np.roll(n, -1, axis=axis) * b - np.roll(b, -1, axis=axis) * n
        out.append(float((ratio * current)[index].sum()) / (3.0 * total_form))
    return (out[0], out[1], out[2])


def hop_by_pace(
    body: Body,
    carried: list[float],
    pace: tuple[float, float, float],
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> bool:
    """The well moves one Node along an axis when the carried displacement passes one Link."""
    moved = False
    for axis in range(3):
        carried[axis] += pace[axis]
        while abs(carried[axis]) >= 1.0:
            step = 1 if carried[axis] > 0 else -1
            carried[axis] -= step
            body.centre[axis] += step
            if wrap[axis]:
                body.centre[axis] %= shape[axis]
            moved = True
    return moved


def hop(
    body: Body,
    centroid: tuple[float, float, float],
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> bool:
    """THE ONE SEAM: the well moves to the Node nearest the record's envelope centroid."""
    moved = False
    for axis in range(3):
        target = int(round(centroid[axis]))
        if wrap[axis]:
            target %= shape[axis]
        if target != body.centre[axis]:
            body.centre[axis] = target
            moved = True
    return moved
