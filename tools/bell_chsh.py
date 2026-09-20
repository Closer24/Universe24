"""The CHSH reading of the Bell run A2 under the Beam Law.

Reads the run folders of the ten worlds of `examples/events/bell/` (the
runner's `run.json`, `initialization.json` and `events.jsonl`) and prints,
per run, the four coincidence counts, the correlation E and its expected
value, and, over the runs, the CHSH sum S of the settings (0, 8), (0, 24),
(16, 8), (16, 24) and the sum S' of the non-saturating quadruple (0, 8),
(0, 12), (4, 8), (4, 12); every criterion of the entry "A2, under the Beam
Law (2026-09-19)" in docs/EXPERIMENTS.md is checked and a failed
criterion exits nonzero. Every expectation is exact: the arithmetic is on
integers and `fractions.Fraction`, no float anywhere in a criterion.

The reading: a pair is the two releases of one age a of the lamp (the ray
on -X toward Alice and the ray on +X toward Bob, both stamped with the
phase a mod N); A = +1 for a click at `alice_plus`, -1 at `alice_minus`,
B likewise; the age of a click is its tick less the offset of its Node,
read off the record itself (the earliest click at a Node is the smallest
age its window admits, whose phase is that age, so the offset is that
click's tick less its phase; under the Beam Law a ray flies at 1 / sqrt 3,
so a minus Node's offset exceeds its plus Node's by the flight table's
ninth Link, two intervals); the first `PAIRS` ages are analysed and the
later ones, still in flight when the run ends, are excluded. E is
(same - different) / PAIRS, expected 1 - 4 k / N with d = (a - b) mod N and
k = min(d, N - d): the triangle of a deterministic local window.

    python tools/bell_chsh.py artifacts/bell
    python tools/bell_chsh.py artifacts/bell/a0_b8 artifacts/bell/a0_b24 ...
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

N = 64
PAIRS = 128
LIGHT = "light"
SIDES = (("alice_plus", "alice_minus"), ("bob_plus", "bob_minus"))
PLUS = {plus for plus, _ in SIDES}
MINUS = {minus for _, minus in SIDES}
NODES = PLUS | MINUS
ALLOWED_RECORDS = {"click", "pass", "record"}
CHSH = ((0, 8), (0, 24), (16, 8), (16, 24))
PRIME = ((0, 8), (0, 12), (4, 8), (4, 12))
CONTROLS = {(0, 0): Fraction(1), (0, 32): Fraction(-1), (0, 16): Fraction(0)}
Setting = tuple[int, int]


def in_window(phase: int, setting: int) -> bool:
    """The centred half circle of the engine (`engine.in_window`) at N."""
    d = (phase - setting) % N
    return d < N // 4 or d >= 3 * N // 4


def expected_correlation(a: int, b: int) -> Fraction:
    d = (a - b) % N
    k = min(d, N - d)
    return 1 - Fraction(4 * k, N)


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


@dataclass
class Run:
    folder: Path
    setting: Setting
    counts: dict[tuple[int, int], int]
    correlation: Fraction
    offsets: dict[str, int]
    plus_ages: dict[str, frozenset[int]]
    fingerprint: str

    @property
    def same(self) -> int:
        return self.counts[(1, 1)] + self.counts[(-1, -1)]

    @property
    def different(self) -> int:
        return self.counts[(1, -1)] + self.counts[(-1, 1)]


def load(folder: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    return record, world, events


def windows(world: dict[str, Any]) -> dict[str, int]:
    """The phase window of each detector's one Node, read from the world."""
    tables = {tuple(entry["position"]): entry.get("table", {}) for entry in world["measured"]}
    found: dict[str, int] = {}
    for detector in world["detectors"]:
        (position,) = detector["positions"]
        found[detector["name"]] = int(tables[tuple(position)][LIGHT]["phase_window"])
    return found


def analyse(folder: Path, checks: Checks) -> Run:
    record, world, events = load(folder)
    label = folder.name
    setting_of = windows(world)
    a, b = setting_of["alice_plus"], setting_of["bob_plus"]
    checks.equal(f"{label}: the detectors", set(setting_of), NODES)
    checks.equal(f"{label}: Alice's complement", setting_of["alice_minus"], (a + N // 2) % N)
    checks.equal(f"{label}: Bob's complement", setting_of["bob_minus"], (b + N // 2) % N)
    ticks = int(world["ticks"])
    checks.equal(f"{label}: status", record["status"], "completed")
    checks.equal(f"{label}: completed ticks", record["completed_ticks"], ticks)
    checks.equal(
        f"{label}: the books at every completed tick", record["conserved_at_every_completed_tick"], True
    )
    checks.equal(
        f"{label}: every audit entry balanced", all(entry["balanced"] for entry in record["audit"]), True
    )
    checks.equal(f"{label}: audit entries", len(record["audit"]), ticks)
    checks.equal(
        f"{label}: nothing escaped",
        [(entry["family"], entry["amount"], entry["momentum"]) for entry in record["escaped"]],
        [(family["name"], 0, [0, 0, 0]) for family in world["families"]],
    )
    (lamp,) = [entry for entry in world["measured"] if "lamp" in entry]
    (lamp_state,) = [entry for entry in record["measured"] if entry["position"] == lamp["position"]]
    checks.equal(f"{label}: the lamp's momentum at the end", lamp_state["momentum"], [0, 0, 0])
    lamp_number = int(lamp_state["number"])
    checks.equal(f"{label}: record kinds", {event["event"] for event in events} - ALLOWED_RECORDS, set())
    clicks = [event for event in events if event["event"] == "click"]
    passes = [event for event in events if event["event"] == "pass"]
    checks.equal(
        f"{label}: every click one unit of the lamp's light at a detector",
        all(
            event["detector"] in NODES
            and event["family"] == LIGHT
            and event["number"] == lamp_number
            and event["amount"] == 1
            for event in clicks
        ),
        True,
    )
    # The offsets: the earliest click at a Node is the smallest age its
    # window admits, and that age is its phase.
    offsets: dict[str, int] = {}
    for node in sorted(NODES):
        at_node = [event for event in clicks if event["detector"] == node]
        checks.add(f"{label}: clicks at {node}", bool(at_node), f"{len(at_node)} clicks")
        if not at_node:
            # A Node without a click (the record form of the lamp, stage
            # (vii) step 4): no offset to read, the check above fails.
            offsets[node] = 0
            continue
        first = min(at_node, key=lambda e: int(e["tick"]))
        offsets[node] = int(first["tick"]) - int(first["phase"])
    checks.equal(f"{label}: the plus offsets agree", offsets["alice_plus"], offsets["bob_plus"])
    checks.equal(f"{label}: the minus offsets agree", offsets["alice_minus"], offsets["bob_minus"])
    checks.add(
        f"{label}: a minus Node one Link on (a later offset)",
        offsets["alice_minus"] > offsets["alice_plus"],
        f"plus {offsets['alice_plus']}, minus {offsets['alice_minus']}",
    )
    checks.equal(
        f"{label}: the run lets the last analysed pair complete",
        ticks >= PAIRS - 1 + max(offsets.values()),
        True,
    )
    phase_rule = True
    window_rule = True
    outcomes: dict[str, dict[int, list[int]]] = {"alice": {}, "bob": {}}
    node_ages: dict[str, set[int]] = {node: set() for node in NODES}
    for event in clicks:
        node = str(event["detector"])
        age = int(event["tick"]) - offsets[node]
        phase = int(event["phase"])
        phase_rule = phase_rule and age >= 0 and phase == age % N
        window_rule = window_rule and in_window(phase, setting_of[node])
        if age < PAIRS:
            side = "alice" if node.startswith("alice") else "bob"
            outcomes[side].setdefault(age, []).append(1 if node in PLUS else -1)
            node_ages[node].add(age)
    checks.equal(f"{label}: every click's phase is its age mod N", phase_rule, True)
    checks.equal(f"{label}: every click inside its window", window_rule, True)
    pass_rule = all(
        event["detector"] in PLUS
        and event["number"] == lamp_number
        and event["amount"] == 1
        and int(event["phase"]) == (int(event["tick"]) - offsets[str(event["detector"])]) % N
        and int(event["window"]) == setting_of[str(event["detector"])]
        and not in_window(int(event["phase"]), int(event["window"]))
        for event in passes
    )
    checks.equal(
        f"{label}: every pass at a plus Node, outside its window, phase its age mod N", pass_rule, True
    )
    for plus, minus in SIDES:
        passed = {
            int(e["tick"]) - offsets[plus]
            for e in passes
            if e["detector"] == plus and int(e["tick"]) - offsets[plus] < PAIRS
        }
        checks.equal(f"{label}: what passes {plus} clicks at {minus}", passed, node_ages[minus])
    for side in ("alice", "bob"):
        checks.equal(
            f"{label}: exactly one outcome per age on {side}'s side",
            [age for age in range(PAIRS) if len(outcomes[side].get(age, [])) != 1],
            [],
        )
    for node in sorted(NODES):
        checks.equal(
            f"{label}: {node} clicks on exactly half of the analysed pairs",
            len(node_ages[node]),
            PAIRS // 2,
        )
    counts: dict[tuple[int, int], int] = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    for age in range(PAIRS):
        alice = outcomes["alice"].get(age, [0])[0]
        bob = outcomes["bob"].get(age, [0])[0]
        if (alice, bob) in counts:
            counts[(alice, bob)] += 1
    same = counts[(1, 1)] + counts[(-1, -1)]
    different = counts[(1, -1)] + counts[(-1, 1)]
    checks.equal(f"{label}: every analysed pair counted", same + different, PAIRS)
    correlation = Fraction(same - different, PAIRS)
    expected = expected_correlation(a, b)
    checks.equal(
        f"{label}: same / different",
        (same, different),
        (PAIRS * (1 + expected) // 2, PAIRS * (1 - expected) // 2),
    )
    checks.equal(f"{label}: E({a}, {b})", correlation, expected)
    return Run(
        folder,
        (a, b),
        counts,
        correlation,
        offsets,
        {node: frozenset(node_ages[node]) for node in PLUS},
        str(record["source_sha256"]),
    )


def chsh(runs: dict[Setting, Run], quadruple: tuple[Setting, ...]) -> Fraction | None:
    """E(a, b) - E(a, b') + E(a', b) + E(a', b') over the four runs, if all are present."""
    if any(setting not in runs for setting in quadruple):
        return None
    first, second, third, fourth = (runs[setting].correlation for setting in quadruple)
    return first - second + third + fourth


def table(runs: list[Run]) -> str:
    head = "run | a | b | ++ | +- | -+ | -- | same | different | E | expected E"
    rows = [head, " | ".join("---" for _ in head.split(" | "))]
    for run in runs:
        a, b = run.setting
        cells = [
            run.folder.name,
            a,
            b,
            run.counts[(1, 1)],
            run.counts[(1, -1)],
            run.counts[(-1, 1)],
            run.counts[(-1, -1)],
            run.same,
            run.different,
            run.correlation,
            expected_correlation(a, b),
        ]
        rows.append(" | ".join(str(cell) for cell in cells))
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", type=Path, help="run folders, or one folder holding them")
    args = parser.parse_args(argv)
    folders = sorted(
        path
        for root in args.paths
        for path in ([root] if (root / "run.json").exists() else root.iterdir())
        if (path / "run.json").exists()
    )
    if not folders:
        parser.error("no run folder (a folder with run.json) under the given paths")
    checks = Checks()
    runs: list[Run] = []
    by_setting: dict[Setting, Run] = {}
    for folder in folders:
        run = analyse(folder, checks)
        checks.add(
            f"{folder.name}: one run per setting",
            run.setting not in by_setting,
            f"setting {run.setting}",
        )
        runs.append(run)
        by_setting[run.setting] = run
    print(table(runs))
    print()
    fingerprints = {run.fingerprint for run in runs}
    checks.equal("one source fingerprint over the runs", len(fingerprints), 1)
    print("source_sha256:", ", ".join(sorted(fingerprints)))
    offsets = {tuple(sorted(run.offsets.items())) for run in runs}
    checks.equal("the same tick offsets in every run", len(offsets), 1)
    print(
        "tick offsets (tick = age + offset):",
        ", ".join(f"{k} {v}" for k, v in sorted(runs[0].offsets.items())),
    )
    for name, quadruple, expected in (("S", CHSH, Fraction(2)), ("S'", PRIME, Fraction(3, 2))):
        value = chsh(by_setting, quadruple)
        settings = " ".join(f"({a},{b})" for a, b in quadruple)
        checks.add(f"{name} over {settings}", value == expected, f"found {value}, expected {expected}")
        print(
            f"{name} = E{quadruple[0]} - E{quadruple[1]} + E{quadruple[2]} + E{quadruple[3]} = {value}"
        )
    for setting, expected in CONTROLS.items():
        if setting in by_setting:
            checks.equal(f"control E{setting}", by_setting[setting].correlation, expected)
    # No-signalling, exact: Alice's clicks depend on a alone, Bob's on b alone.
    for index, (plus, _) in enumerate(SIDES):
        groups: dict[int, set[frozenset[int]]] = {}
        for run in runs:
            groups.setdefault(run.setting[index], set()).add(run.plus_ages[plus])
        for own, sets in sorted(groups.items()):
            others = sorted({run.setting[1 - index] for run in runs if run.setting[index] == own})
            checks.add(
                f"no-signalling: the ages {plus} clicks at setting {own} over the other side's {others}",
                len(sets) == 1,
                f"{len(sets)} distinct set(s) of ages",
            )
    print()
    for name, ok, detail in checks.rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    print()
    print(f"{len(checks.rows) - checks.failed} criteria passed, {checks.failed} failed")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
