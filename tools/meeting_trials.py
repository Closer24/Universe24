"""The trials of a world of records declared NodeReaders (examples/events/zeno, examples/events/anticoincidence; ALGEBRA.md, The click writes on the lattice (j); the paper's S.57 and S.59): one world file run as many times as the design names seeds, each run from the same lay with every reader's generator at a state of its own from the trial's seed, the hash of the trial's label (the seed times the records' number plus the record's number; `hashed_state`: the generator is affine, so labels in arithmetic progression would stay one progression at every draw's depth and the trials' variates one Weyl sequence and not independent draws, the mathematician's finding of 2026-10-04 on #1827 at the advisor's second) (the design's list of seeds, `seeds`, the host's declaration standing where one world file holds one seed; the counter's generator untouched), over the design's intervals, and at the end the part each record stands in (its books, the reader's own), its windows closed (its books' count, the pulsed gate's n) and its `credit` lines labelled NODEREADER naming `taken` or `given`, the clicks (the null window's LATTICE-labelled lines left out); the readings over the trials: per record the fraction of trials ending in each part and the windows closed per trial, the clicks per kind, the trials the run refused inside (the guard's refusal with its interval, by seed, read and not hidden), and over the records the coincidence rows derived from the records' count (`coincidence_rows`): the fractions of trials with a taking at every record alone and at every pair and no other, at neither, and per pair the anticoincidence parameter P(both) / (P(A) P(B)) where defined (A_only, B_only, both, neither and alpha for two records). Every number a click (the clicks, the parts the writes left) and no array is read; the tool holds no number of the law and compares nothing, the blind printed beside the readings where an expectation file is given.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/meeting_trials.py --world <world>.json --design <design>.json [--expectation <expectation>.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from string import ascii_uppercase

from event_universe.lattice import Lattice
from event_universe.world_files import load_world


def hashed_state(label: int, width: int) -> int:
    """The generator's state for one record in one trial from the trial's label (the seed times the records' number plus the record's number): SHA-256 of the label's decimal text read as one little-endian integer and reduced to the generator's modulus (`width` the universe's largest integer, 2^bits - 1, the modulus 2^bits). The generator is affine, x <- (multiplier x + increment) mod modulus, so states in arithmetic progression stay one progression at every depth of the draw and the trials' variates at a fixed depth are one Weyl sequence, not independent draws (the control's second draw fell in the even tenths alone across its 200 trials); a hash of the label breaks the progression, and the seeds' list of the design stands as written."""
    digest = hashlib.sha256(str(int(label)).encode("ascii")).digest()
    return int.from_bytes(digest, "little") % (1 << int(width).bit_length())


def one_trial(
    path: Path, seed: int, intervals: int
) -> tuple[list[str], list[int], list[dict[str, object]], str | None]:
    """One run from the lay with every record's generator at `seed`: the parts the records stand in at the end, by their declared names, their windows closed, the click lines, and the guard's refusal where the run was refused inside (its message, naming the interval; None otherwise)."""
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(path), lines.append)
    for books in board.credit.bodies:  # every record its own state, distinct per record and per trial
        books.state = hashed_state(seed * len(board.credit.bodies) + books.number, board.world.width)
    refused = None
    try:
        for _ in range(intervals):
            board.step()
            if board.ended is not None:
                break
    except (
        RuntimeError
    ) as refusal:  # the guard: a level above the bound, the run refused at its interval
        refused = str(refusal)
    parts = [books.declared.names[books.part] for books in board.credit.bodies]
    windows = [books.windows for books in board.credit.bodies]
    clicks = [
        line
        for line in lines
        if line["event"] == "credit"
        and line["label"] == "NODEREADER"
        and (line["taken"] or line["given"])
    ]
    return parts, windows, clicks, refused


def coincidence_rows(took: Counter[tuple[int, ...]], bodies: int, trials: int) -> dict[str, object]:
    """The coincidence rows over the records, derived from their count and from no fixed key (the advisor's breaker and the mathematician's audit, #1793 comments 5981736108 K6, 5982140872 B3; the Boss's 5981734131 item 6; two hands): every record alone and every pair (`itertools.combinations` over the records), each row the trials with a taking at those records and at no other (`took`, the trials by the set of records that took), a record named by its letter in the world's order (A, B, C, ...), a row `<letters>_only` and `both` where the pair is every record, so that two records' rows read A_only, B_only, both, neither and alpha as the shipped two-body worlds' reports do; `neither` the trials with no taking; and per pair the anticoincidence parameter P(both) / (P(A) P(B)) where defined, P(A) over the trials with a taking at A whatever the others took, `alpha` for two records and `alpha_<letters>` beside; no row under two records (a coincidence is between records); a world of three records gets its three singles, its three pairs and `all`, the trials where every record took (the mathematician's note, #1793 comment 5982776069), so that every trial with a taking stands in exactly one row."""
    if bodies < 2:
        return {}
    letters = [ascii_uppercase[number] for number in range(bodies)]
    rows: dict[str, object] = {}
    for size in range(1, bodies + 1):  # every subset of the records, the all-took trials their own row
        for subset in combinations(range(bodies), size):
            whole = "both" if bodies == 2 else "all"
            name = whole if size == bodies else "_".join(letters[n] for n in subset) + "_only"
            rows[name] = [took[subset], trials]
    rows["neither"] = [took[()], trials]
    for first, second in combinations(range(bodies), 2):
        a = sum(count for subset, count in took.items() if first in subset)
        b = sum(count for subset, count in took.items() if second in subset)
        both = sum(count for subset, count in took.items() if first in subset and second in subset)
        alpha = Fraction(both * trials, a * b) if a and b else None
        name = "alpha" if bodies == 2 else f"alpha_{letters[first]}_{letters[second]}"
        rows[name] = [alpha.numerator, alpha.denominator] if alpha is not None else None
    return rows


def reading(path: Path, design: Path, expectation: Path | None) -> dict[str, object]:
    """The trials' readings against the design's seeds and intervals (its keys `seeds` and `intervals`, or the world's `ticks`), the blind beside them where given."""
    declared = json.loads(design.read_text(encoding="utf-8"))
    world = json.loads(path.read_text(encoding="utf-8"))
    seeds = [int(seed) for seed in declared["seeds"]]
    intervals = int(declared.get("intervals", world["ticks"]))
    ends: list[Counter[str]] = []
    closed: list[Counter[int]] = []
    kinds: Counter[str] = Counter()
    took: Counter[tuple[int, ...]] = Counter()
    refusals: dict[int, str] = {}
    for seed in seeds:
        parts, windows, clicks, refused = one_trial(path, seed, intervals)
        if refused is not None:
            refusals[seed] = refused
            continue
        for number, (part, count) in enumerate(zip(parts, windows, strict=True)):
            while len(ends) <= number:
                ends.append(Counter())
                closed.append(Counter())
            ends[number][part] += 1
            closed[number][count] += 1
        kinds.update(f"{j['node_reader']} {j['realised']} by {j['taken'] or j['given']}" for j in clicks)
        took[tuple(sorted({int(str(j["node_reader"]).split()[-1]) for j in clicks if j["taken"]}))] += 1
    trials = len(seeds) - len(refusals)
    fractions = {
        f"body {n}": {part: [c, trials] for part, c in sorted(found.items())}
        for n, found in enumerate(ends)
    }
    windows_closed = {
        f"body {n}": {str(count): c for count, c in sorted(found.items())}
        for n, found in enumerate(closed)
    }
    coincidence = coincidence_rows(took, len(ends), trials)
    found: dict[str, object] = {
        "world": path.name,
        "trials": trials,
        "intervals": intervals,
        "ends_in_part": fractions,
        "windows_closed": windows_closed,
        "refused": {str(seed): message for seed, message in sorted(refusals.items())},
        "clicks": dict(sorted(kinds.items())),
        "coincidence": coincidence,
        "label": "NODEREADER",
    }
    if expectation is not None:
        found["blind"] = json.loads(expectation.read_text(encoding="utf-8")).get("blind")
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--world", type=Path, required=True, help="the world file, its mode file beside it"
    )
    parser.add_argument("--design", type=Path, required=True, help="the design file naming the seeds")
    parser.add_argument("--expectation", type=Path, help="the blind expectation file, printed beside")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.design, args.expectation), indent=1))


if __name__ == "__main__":
    main()
