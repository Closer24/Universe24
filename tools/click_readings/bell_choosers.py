"""The CHSH reading of the Bell run with the choosers on the GameBoard
(issue #363; the entry "A2 with the choosers on the GameBoard (2026-09-20)"
in docs/EXPERIMENTS.md; the worlds of `examples/events/bell/make_chooser_worlds.py`).

Reads one run folder (the runner's `run.json`, `initialization.json` and
`events.jsonl`) of a world of that design: a pair lamp of `light` at the
centre of a bar, four counters `alice_plus`, `alice_minus`, `bob_plus` and
`bob_minus` (each its own detector), and two setting streams whose phase
the counters read for their windows (`phase_window` `{"reads": ...}`), or,
in a control, windows written in the file. Every number printed is
labelled DETECTOR (a record of a detector's set: the clicks, the passes,
the windows carried on them) or GAMEBOARD (the host's view: the world
replayed for the rows at the counters' Nodes), the experimenter's rule.
Every criterion is exact, on integers and `fractions.Fraction`.

The reading, per pair (the two rows of one record of the lamp, one
birth: the record's identity, the lamp's number x 2^32 + the birth's
ordinal, is carried on every click and pass line): A = +1 for a click at
`alice_plus`, -1 at `alice_minus`, B likewise; the AGE of a pair is its
birth ordinal less one, read off the record on the line, and its phase is
that age mod N (u, the birth phase), as in `tools/click_readings/bell.py`. Since the
fraction-free law (2026-09-20, BEAM_LAW note 41) a paid lamp's exact clock
stalls where its content has fallen below K, so the tick of a birth is
not the age of the lamp's clock and a pair is read by its record, never
by its tick; the tick offsets (the smallest tick - age at each counter,
the flight's) are reported. The setting of a side at a pair is the
centre of the plus counter's window at that pair, carried on the plus
counter's `click` or `pass` line (`window`; the declared number in a
control); the minus counter's window must be its exact complement
(`window` + N / 2 on the minus click). The pairs analysed are the ages
from the first at which every counter had a setting (the warm-up, the
pairs that passed a plus counter with `window` None, is excluded and
counted) to the last whose minus clicks the run holds. The pairs are
binned by (a, b); per bin the four coincidence counts, E = (same -
different) / n and the triangle 1 - 4 k / N (d = (a - b) mod N, k =
min(d, N - d)); then S over the declared quadruple (`--chsh a,a2,b,b2`;
the design's by default), the largest S over every quadruple of settings
that occurred (over the four placements of the minus sign), against the
triangle's own value on the same quadruple, and no-signalling: each
side's marginal of +1 per bin, equal across the other side's settings.

    python tools/click_readings/bell_choosers.py artifacts/bell363/read
    python tools/click_readings/bell_choosers.py artifacts/bell363/written_a0_b8 artifacts/bell363/written_a0_b29 \
        artifacts/bell363/written_a25_b8 artifacts/bell363/written_a25_b29
    python tools/click_readings/bell_choosers.py artifacts/bell363/fixed --replay 40
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world  # noqa: E402
from event_universe.trimmed_record import refuse_trimmed_record  # noqa: E402
from event_universe.world_loading import world_of_run  # noqa: E402

LIGHT = "light"
SIDES = (("alice", "alice_plus", "alice_minus"), ("bob", "bob_plus", "bob_minus"))
PLUS = {plus for _, plus, _ in SIDES}
MINUS = {minus for _, _, minus in SIDES}
NODES = PLUS | MINUS
ALLOWED_RECORDS = {"click", "pass", "record"}
# The design's quadruple (make_chooser_worlds.chsh_quadruple): Alice's 0 and
# 25 with Bob's 8 and 29, ordered within a half circle.
CHSH: tuple[tuple[int, int], tuple[int, int]] = ((0, 25), (8, 29))
Setting = tuple[int, int]
Counts = dict[tuple[int, int], int]


def in_window(phase: int, setting: int, modulus: int) -> bool:
    """The centred half circle of the engine (`nature_beam_tables.window`)."""
    d = (phase - setting) % modulus
    return 4 * d < modulus or 4 * d >= 3 * modulus


def expected_correlation(a: int, b: int, modulus: int) -> Fraction:
    d = (a - b) % modulus
    k = min(d, modulus - d)
    return 1 - Fraction(4 * k, modulus)


@dataclass
class Checks:
    """The criteria, each with its verdict and what was found."""

    rows: list[tuple[str, bool, str]] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str) -> None:
        self.rows.append((name, ok, detail))

    def equal(self, name: str, found: object, expected: object) -> None:
        self.add(name, found == expected, f"found {found}, expected {expected}")

    @property
    def failed(self) -> int:
        return sum(1 for _, ok, _ in self.rows if not ok)


@dataclass(frozen=True)
class CounterEntry:
    """A counter as the world declares it: its Node, whether it is a plus
    counter, its declared window (a number) or the family it reads its
    window from with the offset."""

    name: str
    node: tuple[int, int, int]
    declared: int | None
    reads: str | None
    offset: int


@dataclass
class Bin:
    """One (a, b) bin: the coincidence counts and each side's +1 counts."""

    counts: Counts = field(default_factory=lambda: {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0})

    @property
    def n(self) -> int:
        return sum(self.counts.values())

    @property
    def same(self) -> int:
        return self.counts[(1, 1)] + self.counts[(-1, -1)]

    @property
    def different(self) -> int:
        return self.counts[(1, -1)] + self.counts[(-1, 1)]

    @property
    def correlation(self) -> Fraction:
        return Fraction(self.same - self.different, self.n)

    def marginal(self, side: int) -> Fraction:
        """The fraction of +1 on one side (0 Alice, 1 Bob)."""
        plus = sum(count for outcome, count in self.counts.items() if outcome[side] == 1)
        return Fraction(plus, self.n)


@dataclass
class Run:
    folder: Path
    modulus: int
    offsets: dict[str, int]
    first: int
    last: int
    warm_up: int
    bins: dict[Setting, Bin]
    fingerprint: str
    settings: tuple[list[int], list[int]]

    @property
    def pairs(self) -> int:
        return sum(item.n for item in self.bins.values())


def load(folder: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = world_of_run(folder)
    refuse_trimmed_record(folder)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    return record, world, events


def counters_of(world: dict[str, Any]) -> dict[str, CounterEntry]:
    """The four counters from the world: the detector of one Node each and
    its `light` entry's window, declared or read."""
    tables = {tuple(entry["position"]): entry.get("table", {}) for entry in world["measured"]}
    found: dict[str, CounterEntry] = {}
    for detector in world["detectors"]:
        if detector["name"] not in NODES:
            continue
        (position,) = detector["positions"]
        entry = tables[tuple(position)][LIGHT]
        window = entry["phase_window"] if isinstance(entry, dict) else None
        node = (int(position[0]), int(position[1]), int(position[2]))
        if isinstance(window, dict):
            found[detector["name"]] = CounterEntry(
                detector["name"], node, None, str(window["reads"]), int(window.get("offset", 0))
            )
        else:
            found[detector["name"]] = CounterEntry(
                detector["name"], node, None if window is None else int(window), None, 0
            )
    return found


def offsets_of(lines: list[dict[str, Any]], base: int, checks: Checks, label: str) -> dict[str, int]:
    """The tick offset of every counter's Node, a report: the smallest
    tick - age over its clicks and passes, the flight's (a stall of the
    lamp's clock puts every later birth a tick on); every line must carry
    the lamp's record (`base` the lamp's number x 2^32), the age's owner."""
    offsets: dict[str, int] = {}
    for name in sorted(NODES):
        at_node = [e for e in lines if e["detector"] == name]
        checks.equal(
            f"{label}: every line at {name} carries the lamp's record",
            all("record" in e and int(e["record"]) > base for e in at_node),
            True,
        )
        offsets[name] = min((int(e["tick"]) - (int(e["record"]) - base - 1) for e in at_node), default=0)
    return offsets


def analyse(folder: Path, checks: Checks, pairs: int | None = None) -> Run:
    record, world, events = load(folder)
    label = folder.name
    modulus = int(world.get("N", 64))
    half = modulus // 2
    counters = counters_of(world)
    checks.equal(f"{label}: the four counters", set(counters), NODES)
    ticks = int(world["ticks"])
    checks.equal(f"{label}: status", record["status"], "completed")
    checks.equal(f"{label}: completed ticks", record["completed_ticks"], ticks)
    checks.equal(f"{label}: the books at every tick", record["conserved_at_every_completed_tick"], True)
    checks.equal(f"{label}: record kinds", {e["event"] for e in events} - ALLOWED_RECORDS, set())
    (lamp,) = [entry for entry in world["measured"] if "lamp" in entry]
    (lamp_state,) = [entry for entry in record["measured"] if entry["position"] == lamp["position"]]
    lamp_number = int(lamp_state["number"])
    checks.equal(f"{label}: the pair lamp's momentum at the end", lamp_state["momentum"], [0, 0, 0])
    lines = [
        e
        for e in events
        if e["event"] in ("click", "pass") and e["family"] == LIGHT and e["detector"] in NODES
    ]
    clicks = [e for e in lines if e["event"] == "click"]
    passes = [e for e in lines if e["event"] == "pass"]
    checks.equal(
        f"{label}: every click one unit of the lamp's light",
        all(e["number"] == lamp_number and e["amount"] == 1 for e in clicks),
        True,
    )
    base = lamp_number << 32
    offsets = offsets_of(lines, base, checks, label)
    for side, plus, minus in SIDES:
        checks.add(
            f"{label}: {side}'s minus counter later than its plus",
            offsets[minus] > offsets[plus],
            f"plus {offsets[plus]}, minus {offsets[minus]}",
        )

    # The window a line carries: the reading's centre on a read entry (None
    # in the warm-up), the declared number otherwise.
    def window_of(line: dict[str, Any]) -> int | None:
        counter = counters[str(line["detector"])]
        if counter.reads is not None:
            value = line.get("window")
            return None if value is None else int(value)
        return counter.declared

    def age_of(line: dict[str, Any]) -> int:
        return int(line.get("record", base + 1)) - base - 1

    # The warm-up: the ages at which a plus counter had no setting.
    unset = [age_of(e) for e in passes if e["detector"] in PLUS and window_of(e) is None]
    first = 1 + max(unset) if unset else 0
    # The last analysed pair: the last age at which both sides are on the
    # record (a pair still in flight when the run ends has one side or none).
    complete = [
        age
        for age in {age_of(e) for e in clicks}
        if all(
            any(age_of(e) == age and e["detector"].startswith(side) for e in clicks)
            for side in ("alice", "bob")
        )
    ]
    last = max(complete, default=-1)
    checks.add(f"{label}: the run holds analysed pairs", last >= first, f"first {first}, last {last}")
    if pairs is not None:
        last = min(last, first + pairs - 1)
    # Per side and age: the setting (the plus counter's window) and the outcome.
    setting_at: dict[str, dict[int, int]] = {side: {} for side, _, _ in SIDES}
    outcome_at: dict[str, dict[int, list[int]]] = {side: {} for side, _, _ in SIDES}
    phase_at: dict[int, set[int]] = {}
    phase_rule = True
    window_rule = True
    complement_rule = True
    for e in lines:
        age = age_of(e)
        phase = int(e["phase"])
        phase_rule = phase_rule and age >= 0 and phase == age % modulus
        phase_at.setdefault(age, set()).add(phase)
        name = str(e["detector"])
        side = "alice" if name.startswith("alice") else "bob"
        window = window_of(e)
        if name in PLUS:
            if window is not None:
                setting_at[side].setdefault(age, window)
                setting_at[side][age] = window
            if e["event"] == "click":
                window_rule = window_rule and window is not None and in_window(phase, window, modulus)
                outcome_at[side].setdefault(age, []).append(1)
            else:
                window_rule = window_rule and (window is None or not in_window(phase, window, modulus))
        else:
            # A minus counter's window is the plus counter's complement.
            plus_window = setting_at[side].get(age)
            if plus_window is not None:
                complement_rule = complement_rule and window == (plus_window + half) % modulus
            if e["event"] == "click":
                window_rule = window_rule and window is not None and in_window(phase, window, modulus)
                outcome_at[side].setdefault(age, []).append(-1)
            else:
                window_rule = window_rule and (window is None or not in_window(phase, window, modulus))
    checks.equal(f"{label}: every click's and pass's phase is its age mod N", phase_rule, True)
    checks.equal(f"{label}: every click inside its window, every pass outside", window_rule, True)
    checks.equal(f"{label}: every minus window the plus window's complement", complement_rule, True)
    checks.equal(
        f"{label}: one phase per age on the record", all(len(p) == 1 for p in phase_at.values()), True
    )
    bins: dict[Setting, Bin] = {}
    missing: list[int] = []
    for age in range(first, last + 1):
        alice = outcome_at["alice"].get(age, [])
        bob = outcome_at["bob"].get(age, [])
        if (
            len(alice) != 1
            or len(bob) != 1
            or age not in setting_at["alice"]
            or age not in setting_at["bob"]
        ):
            missing.append(age)
            continue
        key = (setting_at["alice"][age], setting_at["bob"][age])
        bins.setdefault(key, Bin()).counts[(alice[0], bob[0])] += 1
    checks.equal(
        f"{label}: exactly one outcome per side and a setting at every analysed age", missing[:10], []
    )
    warm_up = first
    escaped = {entry["family"]: int(entry["amount"]) for entry in record["escaped"]}
    lost = sum(
        1
        for age in range(0, first)
        if len(outcome_at["alice"].get(age, [])) + len(outcome_at["bob"].get(age, [])) < 2
    )
    checks.equal(f"{label}: light escaped only from the warm-up pairs", escaped.get(LIGHT, 0), lost)
    for key, item in sorted(bins.items()):
        a, b = key
        checks.equal(
            f"{label}: E{key} on the triangle", item.correlation, expected_correlation(a, b, modulus)
        )
    settings = (
        sorted({a for a, _ in bins}),
        sorted({b for _, b in bins}),
    )
    return Run(
        folder, modulus, offsets, first, last, warm_up, bins, str(record["source_sha256"]), settings
    )


def chsh_sum(
    bins: dict[Setting, Bin], quadruple: tuple[tuple[int, int], tuple[int, int]]
) -> Fraction | None:
    """S = E(a, b) - E(a, b') + E(a', b) + E(a', b') over the bins, if all four are present."""
    (a, a2), (b, b2) = quadruple
    keys = ((a, b), (a, b2), (a2, b), (a2, b2))
    if any(key not in bins for key in keys):
        return None
    e = [bins[key].correlation for key in keys]
    return e[0] - e[1] + e[2] + e[3]


def signed_sums(e: list[Fraction]) -> list[Fraction]:
    """The four CHSH sums of one quadruple, the minus sign on each term in turn."""
    total = sum(e, Fraction(0))
    return [total - 2 * item for item in e]


def best_quadruple(
    bins: dict[Setting, Bin], modulus: int
) -> tuple[Fraction, tuple[tuple[int, int], tuple[int, int]], Fraction] | None:
    """The largest S over every quadruple of settings that occurred (a < a',
    b < b', all four bins present, the four placements of the minus sign),
    with the triangle's own S on that quadruple; None without a quadruple."""
    alice = sorted({a for a, _ in bins})
    bob = sorted({b for _, b in bins})
    best: tuple[Fraction, tuple[tuple[int, int], tuple[int, int]], Fraction] | None = None
    for a, a2 in combinations(alice, 2):
        for b, b2 in combinations(bob, 2):
            keys = ((a, b), (a, b2), (a2, b), (a2, b2))
            if any(key not in bins for key in keys):
                continue
            measured = signed_sums([bins[key].correlation for key in keys])
            expected = signed_sums([expected_correlation(x, y, modulus) for x, y in keys])
            for value, triangle in zip(measured, expected, strict=True):
                if best is None or value > best[0]:
                    best = (value, ((a, a2), (b, b2)), triangle)
    return best


def replay(world: dict[str, Any], intervals: int) -> list[dict[str, object]]:
    """GAMEBOARD: the world replayed through the engine; per interval, at
    each counter's Node, the rows of the setting families present (their
    amount and phase per row), the host's view of what the window read."""
    parsed = parse_nature_beam_world(world)
    simulation = NatureBeamSimulation(parsed)
    counters = counters_of(world)
    families = [family.name for family in parsed.families]
    found: list[dict[str, object]] = []
    for _ in range(intervals):
        simulation.step()
        entry: dict[str, object] = {"tick": simulation.tick}
        for name, counter in sorted(counters.items()):
            if counter.reads is None:
                continue
            store = simulation.stores[families.index(counter.reads)]
            lo, hi = store.slice(store.flat(counter.node))
            entry[name] = [
                (int(row.amount), int(row.phase))
                for row in store.rows(lo, hi)
                if row.number != simulation.occupant(counter.node)
            ]
        found.append(entry)
    return found


def table(run: Run) -> str:
    head = "a | b | n | ++ | +- | -+ | -- | E | triangle | P(A=+) | P(B=+)"
    rows = [head, " | ".join("---" for _ in head.split(" | "))]
    for (a, b), item in sorted(run.bins.items()):
        cells = [
            a,
            b,
            item.n,
            item.counts[(1, 1)],
            item.counts[(1, -1)],
            item.counts[(-1, 1)],
            item.counts[(-1, -1)],
            item.correlation,
            expected_correlation(a, b, run.modulus),
            item.marginal(0),
            item.marginal(1),
        ]
        rows.append(" | ".join(str(cell) for cell in cells))
    return "\n".join(rows)


def parse_quadruple(text: str) -> tuple[tuple[int, int], tuple[int, int]]:
    a, a2, b, b2 = (int(part) for part in text.split(","))
    return (a, a2), (b, b2)


def merged(runs: list[Run]) -> dict[Setting, Bin]:
    """The bins of several runs merged by setting (a control of one setting
    per run gives its quadruple over four runs, as `tools/click_readings/bell.py`
    reads A2's ten)."""
    found: dict[Setting, Bin] = {}
    for run in runs:
        for key, item in run.bins.items():
            target = found.setdefault(key, Bin())
            for outcome, count in item.counts.items():
                target.counts[outcome] += count
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folders", nargs="+", type=Path, help="run folders (each with run.json)")
    parser.add_argument(
        "--chsh",
        type=parse_quadruple,
        default=CHSH,
        help="the quadruple a,a',b,b' (the design's by default)",
    )
    parser.add_argument("--pairs", type=int, default=None, help="analyse at most this many pairs")
    parser.add_argument("--replay", type=int, default=0, help="GAMEBOARD: replay this many intervals")
    args = parser.parse_args(argv)
    checks = Checks()
    runs = [analyse(folder, checks, args.pairs) for folder in args.folders]
    modulus = runs[0].modulus
    for run in runs:
        print(f"DETECTOR  {run.folder.name}: source_sha256 {run.fingerprint}")
        print(
            "DETECTOR  tick offsets (the smallest tick - age at each counter, the flight's): "
            + ", ".join(f"{k} {v}" for k, v in sorted(run.offsets.items()))
        )
        print(
            f"DETECTOR  warm-up {run.warm_up} pairs excluded (no setting at a plus counter); "
            f"analysed the ages {run.first}..{run.last}, {run.pairs} pairs in {len(run.bins)} bins"
        )
        print(f"DETECTOR  Alice's settings {run.settings[0]}, Bob's settings {run.settings[1]}")
        print("DETECTOR  per bin (a, b): the counts, E, the triangle and the marginals")
        print(table(run))
    fingerprints = {run.fingerprint for run in runs}
    checks.equal("one source fingerprint over the runs", len(fingerprints), 1)
    bins = merged(runs)
    alice = sorted({a for a, _ in bins})
    bob = sorted({b for _, b in bins})
    varied = len(alice) >= 2 and len(bob) >= 2
    value = chsh_sum(bins, args.chsh)
    (a, a2), (b, b2) = args.chsh
    triangle = sum(
        (
            expected_correlation(a, b, modulus),
            -expected_correlation(a, b2, modulus),
            expected_correlation(a2, b, modulus),
            expected_correlation(a2, b2, modulus),
        ),
        Fraction(0),
    )
    if value is not None or varied:
        checks.add(
            f"S over ({a},{b}) ({a},{b2}) ({a2},{b}) ({a2},{b2})",
            value == triangle,
            f"found {value}, the triangle {triangle}",
        )
    print(
        f"DETECTOR  S = E({a},{b}) - E({a},{b2}) + E({a2},{b}) + E({a2},{b2}) = {value} "
        f"(the triangle {triangle})"
    )
    best = best_quadruple(bins, modulus)
    if best is None:
        if varied:
            # Two settings per side and still no quadruple: the settings
            # never varied independently of each other (a locked clock).
            checks.add(
                "a quadruple of settings occurred",
                False,
                f"none over Alice's {len(alice)} and Bob's {len(bob)} settings: they never varied "
                "independently",
            )
        print(
            "DETECTOR  max S over quadruples: none occurred (no two settings of each side meet all "
            "four ways)"
        )
    else:
        largest, quadruple, expected = best
        checks.add(
            f"max S over quadruples, on {quadruple}",
            largest == expected,
            f"found {largest}, the triangle {expected}",
        )
        print(
            f"DETECTOR  max S over all {len(alice)} x {len(bob)} settings' quadruples = {largest} "
            f"on {quadruple} (the triangle {expected})"
        )
    # No-signalling: each side's marginal per own setting, equal across the other side's settings.
    for side in (0, 1):
        name = SIDES[side][0]
        by_own: dict[int, dict[int, Fraction]] = {}
        for (a_s, b_s), item in bins.items():
            own, other = (a_s, b_s) if side == 0 else (b_s, a_s)
            by_own.setdefault(own, {})[other] = item.marginal(side)
        for own, marginals in sorted(by_own.items()):
            values = sorted(set(marginals.values()))
            checks.add(
                f"no-signalling: {name}'s marginal at {own} over the other side's {sorted(marginals)}",
                len(values) == 1,
                f"{len(values)} distinct value(s) {[str(v) for v in values]}",
            )
            print(
                f"DETECTOR  no-signalling: P({name} = +1 | {own}) = {[str(v) for v in values]} "
                f"over {sorted(marginals)}"
            )
    if args.replay:
        for run in runs:
            _, world, _ = load(run.folder)
            for entry in replay(world, args.replay):
                print(f"GAMEBOARD  {run.folder.name} {entry}")
    print()
    for name, ok, detail in checks.rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    print()
    print(f"{len(checks.rows) - checks.failed} criteria passed, {checks.failed} failed")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
