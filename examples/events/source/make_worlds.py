"""THE RUN FILES OF THE SOURCE VERB (the ledger's primitive "source", unassigned until the
Boss's record 2217 of 2026-09-26 gave it to Nature24; ALGEBRA.md 9.108 items 11 and 13, 9.110
items 2, 3 and 7, 9.112 row 6, 9.116 item 4b): one record of matter at rest and one moving, each
sourcing two scalar field families that nothing reads back, one by the plain count and one by
the saturating table, with an unsourced family beside.
The source verb alone is under test: a sourced family's level at the record's Nodes gains the
record's local count D_i div E_s each interval and nowhere else, its stationary level is the
static response of the family's own pair, the unsourced family beside stays exactly zero, the
inverse subtracts the same integers. No well: no record reads the sourced family (the well is
closed, beyond the rule, record 2199).

THE WORDS are the check-mode generator's (record 2128: `universe` a path, `q`, `stocks`; no
momentum or spin on a body, a moving body its record with its tail), and the two declarations
the loader lacks today, written as the ledger's table names them: `sourced` {of, weight, scale,
cap} on the sourced family's entry of the universe file, and `readings` on the world file. THE
ONE UNIVERSE (record 2075): every world names the shipped `examples/events/universe.json`; the
three families of these runs (`field`, sourced by the plain count; `field_table`, sourced by the
table; `control`, not sourced) are written here as `universe_entries.json`, the entries to append
to the shipped file the day the loader reads `sourced`, never a second universe file;
`tests/test_source_worlds.py` checks the fragment and the worlds' structure. Every number in
the README is labelled: GAMEBOARD (a diagnostic the run writes), COMPUTATION (the declaration's
arithmetic), HOST (the machine's cost).

    PYTHONPATH=src python examples/events/source/make_worlds.py [name ...]
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import scipy.sparse
import scipy.sparse.linalg

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent
ROOT = EVENTS.parent.parent


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


check_mode = load(EVENTS / "check_mode" / "make_worlds.py", "source_check_mode")
massive = check_mode.massive

UNIVERSE = "examples/events/universe.json"
ENTRIES = HERE / "universe_entries.json"

# THE SOURCED FAMILY AND ITS CONTROL: scalar (parts [1]), a pair of levels (phase 2, the rule
# 9.57 (1) is of second order), the pair [1000, 1019] (kappa^2 = 6 den / num - 6 = 0.114, the
# range 1 / kappa = 2.96 Links, the gap omega_0 = arccos(num / den) = 0.193 per interval; the
# numbers of ALGEBRA.md 9.108 item 11, used here for the short range alone: a level that falls
# by e every three Links shows the source's locality on a small GameBoard), no read, no self
# source, no click; `field` sourced by every matter record with the weight 1 and the scale
# E_s, `field_table` the same under the saturating table with the cap s_cap, `control` the same
# family with no source (the leak test, record 2075 (3)).
FAMILY_PAIR = [1000, 1019]
SOURCED_BY = "matter"
SOURCE_WEIGHT = 1
SIGMA_PEAK = 100  # the count added per interval at the record's peak Node, sets E_s (COMPUTATION)
# E_s, THE UNIVERSE'S INTEGER (COMPUTATION, the generator's reading of the rest world's record):
# D_peak = 4096^2 (2 b - a) div b = 1,891,072 at the mode's clock [a, b] on the 32^3 board, and
# E_s = D_peak div 100 = 18,910, so the peak Node adds 100 per interval; the same E_s serves the
# moving world (its mode's D_peak 1,895,312 on the 48 x 32 x 32 board gives 100 there too)
SCALE = 18910
TABLE_CAP = 60  # s_cap of the table form: the count saturates below the peak's 100 (COMPUTATION)

# THE BODY: the check-mode body (a well of side 5, 2000 quanta, the kind [800, 850], the record
# seeded on its bound mode at the amplitude 2^12); the GameBoard open on six faces
BODY_SIDE = check_mode.BODY_SIDE
BODY_QUANTA = check_mode.BODY_QUANTA
REST_SHAPE = [32, 32, 32]
REST_CENTRE = [16, 16, 16]
MOVING_SHAPE = [48, 32, 32]
MOVING_CENTRE = [10, 16, 16]
MOVING_SPEED = 0.1  # Links per interval along +x (COMPUTATION), 30 Links in the run
TICKS = 300
FAR_OFFSET = 12  # the far Node: 12 Links from the record's centre along +x, 10 beyond its well
EVERY = 1


def sourced_family(name: str, scale: int, cap: int | None, sourced: bool) -> dict:
    entry: dict = {
        "name": name,
        "parts": [1],
        "phase": 2,
        "pair": list(FAMILY_PAIR),
        "reads": [],
        "self_source": {"unit": 0},
    }
    if sourced:
        entry["sourced"] = {"of": SOURCED_BY, "weight": SOURCE_WEIGHT, "scale": scale}
        if cap is not None:
            entry["sourced"]["cap"] = cap
    return entry


def universe_entries(scale: int, cap: int) -> dict:
    """The fragment: the three families to append to the shipped universe file."""
    return {
        "families": [
            sourced_family("field", scale, None, sourced=True),
            sourced_family("field_table", scale, cap, sourced=True),
            sourced_family("control", scale, None, sourced=False),
        ]
    }


def universe_document(scale: int, cap: int) -> dict:
    """The shipped universe file with the fragment's families appended, nothing of the shipped
    part changed: the universe of the day the source lands (in memory; the test reads it)."""
    shipped = json.loads((ROOT / UNIVERSE).read_text(encoding="utf-8"))
    document = copy.deepcopy(shipped)
    document["families"].extend(universe_entries(scale, cap)["families"])
    return document


def record_count(profile: np.ndarray, clock: list[int]) -> np.ndarray:
    """D_i at the start (COMPUTATION, ALGEBRA.md 9.108 item 13): the seed writes both levels
    the profile p_i, the rotation's symmetric point, so D_i = now^2 - next x before = p_i^2 (2 -
    2 cos omega) = p_i^2 (2 b - a) div b with the mode's clock [a, b] (2 cos omega = a / b)."""
    a, b = int(clock[0]), int(clock[1])
    squared = profile.astype(object) ** 2
    return np.array([int(v) * (2 * b - a) // b for v in squared.ravel()], dtype=object).reshape(
        profile.shape
    )


def counts(record: np.ndarray, scale: int, cap: int | None) -> np.ndarray:
    """s_i = D_i div E_s, or with the table s_cap D_i div (s_cap E_s + D_i) (9.108 item 3)."""
    flat = record.ravel()
    if cap is None:
        values = [int(d) // scale for d in flat]
    else:
        values = [(cap * int(d)) // (cap * scale + int(d)) for d in flat]
    return np.array(values, dtype=np.int64).reshape(record.shape)


def static_response(source: np.ndarray, pair: list[int]) -> np.ndarray:
    """The stationary level of the sourced family (COMPUTATION, HOST floats): the rule at rest
    with the count added after every step, SUM over the six neighbours of (a_j - a_i) -
    kappa^2 a_i = -(3 den / num) s_i, kappa^2 = 6 den / num - 6 (ALGEBRA.md 9.108 item 11, the
    combine line of 9.112 item 2 with w = 2 num Gamma^2 and W = 6 den Gamma^2), the level zero
    beyond the open faces; solved exactly on the GameBoard by a sparse direct solve."""
    num, den = pair
    kappa2 = 6.0 * den / num - 6.0
    shape = source.shape
    n = int(np.prod(shape))
    index = np.arange(n).reshape(shape)
    diagonal = np.full(n, -(6.0 + kappa2))
    rows = [np.arange(n)]
    cols = [np.arange(n)]
    data = [diagonal]
    for axis in range(3):
        for sign in (1, -1):
            here = np.take(
                index, np.arange(0 if sign > 0 else 1, shape[axis] - (1 if sign > 0 else 0)), axis=axis
            )
            there = np.take(
                index, np.arange(1 if sign > 0 else 0, shape[axis] - (0 if sign > 0 else 1)), axis=axis
            )
            rows.append(here.ravel())
            cols.append(there.ravel())
            data.append(np.ones(here.size))
    matrix = scipy.sparse.csc_matrix(
        (np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)
    )
    right = -(3.0 * den / num) * source.astype(np.float64).ravel()
    return scipy.sparse.linalg.spsolve(matrix, right).reshape(shape)


def readings(centre: list[int], far: list[int], moving: bool) -> list[dict]:
    """The readings the run writes, each a GameBoard reading (the ledger's run declarations;
    the kinds by the ledger's words, bent to Main Loop's interface when it lands): a family's
    level at a Node over intervals, a family's sum of absolute levels (the leak), the count of
    Nodes with a nonzero level (the locality), a family's and a body's centre."""
    lines: list[dict] = []
    for family in ("field", "field_table"):
        lines.append({"kind": "level", "family": family, "node": list(centre), "every": EVERY})
        lines.append({"kind": "level", "family": family, "node": list(far), "every": EVERY})
        lines.append({"kind": "support", "family": family, "every": EVERY})
    lines.append({"kind": "total", "family": "control", "every": EVERY})
    if moving:
        lines.append({"kind": "centre", "family": "field", "every": 10})
        lines.append({"kind": "centre", "body": 0, "every": 10})
    return lines


def build(name: str, shape: list[int], centre: list[int], moving: bool):
    """One world (in the loader's words of today, translated at the write) and its numbers: the
    plain form's and the table's, both families in the one universe."""
    block = check_mode.body(check_mode.corner(centre, BODY_SIDE), [BODY_SIDE] * 3, BODY_QUANTA)
    document = check_mode.build(name, shape, check_mode.OPEN, [block], TICKS)
    entry = document["measured"][0]
    profile = np.array(entry["seed"], dtype=np.int64).reshape(shape)
    record = record_count(profile, entry["clock"])
    peak = int(max(record.ravel()))
    numbers: dict[str, float] = {
        "profile_peak": int(profile.max()),
        "count_peak": peak,
        "scale_from_this_peak": peak // SIGMA_PEAK,
    }
    far = [centre[0] + FAR_OFFSET, centre[1], centre[2]]
    for word, cap in (("plain", None), ("table", TABLE_CAP)):
        source = counts(record, SCALE, cap)
        level = static_response(source, FAMILY_PAIR)
        numbers[f"{word}_sigma_peak"] = int(source[tuple(centre)])
        numbers[f"{word}_source_nodes"] = int((source != 0).sum())
        numbers[f"{word}_source_total"] = int(source.sum())
        numbers[f"{word}_static_centre"] = float(level[tuple(centre)])
        numbers[f"{word}_static_far"] = float(level[tuple(far)])
        numbers[f"{word}_static_total"] = float(level.sum())
    if moving:
        numbers.update(check_mode.move(document, 0, [MOVING_SPEED, 0.0, 0.0]))
    return document, far, numbers


WORLDS = {
    "source_rest": (REST_SHAPE, REST_CENTRE, False),
    "source_moving": (MOVING_SHAPE, MOVING_CENTRE, True),
}


def main() -> None:
    from event_universe.world_files import input_stamp

    names = sys.argv[1:] or list(WORLDS)
    ENTRIES.write_text(check_mode.dumps(universe_entries(SCALE, TABLE_CAP)), encoding="utf-8")
    for name in names:
        shape, centre, moving = WORLDS[name]
        document, far, numbers = build(name.replace("_", "-"), shape, centre, moving)
        written = check_mode.translate(document)
        written["universe"] = UNIVERSE
        # the universe's integers are the universe file's alone (record 2128 (3)); a body
        # moves by the rule or stands by its own symmetry, never by a `fixed` word (the ledger's
        # run files table: a record without `fixed` moves by the rule)
        for key in ("momentum_unit", "twist_table"):
            written.pop(key, None)
        for entry in written["measured"]:
            entry.pop("fixed", None)
        written["readings"] = readings(centre, far, moving)
        written.pop("stamp", None)
        written["stamp"] = input_stamp(written)
        path = HERE / f"{name}.json"
        path.write_text(check_mode.dumps(written), encoding="utf-8")
        print(
            path.name,
            "shape",
            shape,
            json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in numbers.items()}),
        )


if __name__ == "__main__":
    main()
