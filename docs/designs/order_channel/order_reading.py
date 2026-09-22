"""The order channel's reading: Bob's outcome ORDER after a detector
(docs/designs/order_channel/PINS.md; RUN.md). Standard library only,
integers and `fractions.Fraction`, no float anywhere.

    python docs/designs/order_channel/order_reading.py <run dir> [<run dir> ...]

A run dir is the shipped runner's output for one of the two worlds of
PINS.md. The tool reads `run.json` (the model, the source and world sha256)
and `events.jsonl`: under the pair form the record's one click is its
`gather` line (`chosen`: the channel + or - per arm in the arms' order,
Alice first, at the counter named; `u` the wheel value; `record` the
identity, the lamp's number x 2^32 + the birth ordinal), and the arm's
arrival at its counter is a `click` line carrying `window` (the setting
read there). Every number printed from those lines is DETECTOR; the pins
(PINS.md section 5, declared before the run) are COMPUTATION; nature's 0
is the thing compared with. The analysed births are the first L = 192
consecutive ordinals from the first ordinal whose record clicked at
`alice_plus` with a window read there (the chooser world's warm-up births
meet no setting and click at `alice_minus`). The serial correlation at
lag 1 is the cyclic mean (1 / L) sum_t x_t x_{(t + 1) mod L}; the open
mean over the L - 1 adjacent pairs is printed beside it, unpinned. Exit
status 1 when a pinned reading does not match its pin or the run is
incomplete.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

LAMP = 1 << 32
BIRTHS = 192
N = 64
FIRST_COUNTER = "alice_plus"
SECOND_COUNTER = "bob_plus"
# The pins of PINS.md section 5, by the world's model id: Bob's serial
# correlation at lag 1 (cyclic over 192 births), the marginals, Alice's
# serial correlation, the same-sign pairs, the settings of the protocol.
PINS: dict[str, dict[str, object]] = {
    "beam-order-a0_b0-v1": {
        "bob_serial": Fraction(15, 16),
        "marginal": (96, 96),
        "alice_serial": Fraction(15, 16),
        "same": 192,
        "settings": [0],
    },
    "beam-order-a0_21_42_b0-v1": {
        "bob_serial": Fraction(-1, 16),
        "marginal": (96, 96),
        "alice_serial": Fraction(15, 16),
        "same": 94,
        "settings": [0, 21, 42],
    },
}
NATURE_SERIAL = Fraction(0)


def sign(channel: str) -> int:
    if channel not in "+-":
        raise ValueError(f"a channel is + or -, not {channel!r}")
    return 1 if channel == "+" else -1


def serial(xs: list[int]) -> tuple[Fraction, Fraction]:
    L = len(xs)
    return (
        Fraction(sum(xs[t] * xs[(t + 1) % L] for t in range(L)), L),
        Fraction(sum(xs[t] * xs[t + 1] for t in range(L - 1)), L - 1),
    )


def read_events(folder: Path) -> tuple[dict[int, dict[str, object]], dict[int, set[int]]]:
    """The gathers by birth ordinal and the windows read at the first
    counter per ordinal (a set: every arrival line of the record there)."""
    gathers: dict[int, dict[str, object]] = {}
    windows: dict[int, set[int]] = {}
    with (folder / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            event = json.loads(line)
            if event.get("family") != "light":
                continue
            ordinal = int(event["record"]) - LAMP
            if event["event"] == "gather":
                if ordinal in gathers:
                    raise ValueError(f"two gathers of the record {ordinal}")
                gathers[ordinal] = event
            elif (
                event["event"] == "click"
                and event.get("detector") == FIRST_COUNTER
                and "window" in event
            ):
                windows.setdefault(ordinal, set()).add(int(event["window"]))
    return gathers, windows


def analyse(folder: Path) -> bool:
    run = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(run["model"])
    print(
        f"== {folder.name}: model {model}, source sha256 {run['source_sha256']}, world sha256 {run['initialization_sha256']}, {run['completed_ticks']} of {run['requested_ticks']} intervals, status {run['status']}"
    )
    gathers, windows = read_events(folder)
    first = min(
        (o for o, g in gathers.items() if g["chosen"][0][0] == FIRST_COUNTER and o in windows),
        default=None,
    )
    if first is None:
        print("   no record clicked at the first counter with a window: incomplete")
        return False
    ordinals = list(range(first, first + BIRTHS))
    missing = [o for o in ordinals if o not in gathers or o not in windows]
    if missing:
        print(
            f"   incomplete: the ordinals {missing[:5]}... lack a gather or a window ({len(missing)} of {BIRTHS})"
        )
        return False
    A: list[int] = []
    B: list[int] = []
    settings: list[int] = []
    us: list[int] = []
    ok = True
    for o in ordinals:
        g = gathers[o]
        chosen = g["chosen"]
        if chosen[0][0] != FIRST_COUNTER or chosen[1][0] != SECOND_COUNTER:
            print(
                f"   ordinal {o}: the click at {chosen[0][0]}, {chosen[1][0]}, not the two plus counters"
            )
            ok = False
        if len(windows[o]) != 1:
            print(
                f"   ordinal {o}: the arrival lines at {FIRST_COUNTER} carry {sorted(windows[o])}, not one window"
            )
            ok = False
        A.append(sign(chosen[0][2]))
        B.append(sign(chosen[1][2]))
        settings.append(min(windows[o]))
        us.append(int(g["u"]))
    print(
        f"   DETECTOR: births analysed {BIRTHS}, the ordinals {first} .. {first + BIRTHS - 1}, the first wheel value u = {us[0]}"
    )
    wheel_ok = all(u == (o - 1) % N for o, u in zip(ordinals, us, strict=True))
    print(
        f"   DETECTOR: u = (ordinal - 1) mod {N} on every analysed record: {'yes' if wheel_ok else 'NO'}"
    )
    theorem5 = all((a == 1) == (u < N // 2) for a, u in zip(A, us, strict=True))
    print(f"   DETECTOR: Alice + exactly for u < {N // 2} (Theorem 5): {'yes' if theorem5 else 'NO'}")
    distinct = sorted(set(settings))
    period = next(
        (
            p
            for p in range(1, BIRTHS + 1)
            if all(settings[t] == settings[(t + p) % BIRTHS] for t in range(BIRTHS))
        ),
        None,
    )
    print(
        f"   DETECTOR: Alice's settings read at {FIRST_COUNTER}: the values {distinct}, the period {period}, the first three {settings[:3]}; Bob's window the world's integer 0"
    )
    bob_cyclic, bob_open = serial(B)
    alice_cyclic, alice_open = serial(A)
    same = sum(1 for a, b in zip(A, B, strict=True) if a == b)
    print(
        f"   DETECTOR: Bob's sequence, the first turn of the wheel: {''.join('+' if b == 1 else '-' for b in B[:N])}"
    )
    print(
        f"   DETECTOR: Bob's marginal {B.count(1)} / {B.count(-1)}; Alice's marginal {A.count(1)} / {A.count(-1)}; same-sign pairs {same} of {BIRTHS}"
    )
    print(
        f"   DETECTOR: Bob's serial correlation at lag 1 = {bob_cyclic} cyclic ({bob_open} open, unpinned); Alice's {alice_cyclic} cyclic ({alice_open} open)"
    )
    pins = PINS.get(model)
    if pins is None:
        print(f"   no pin declared for the model {model}")
        return False
    checks = [
        ("Bob's serial correlation at lag 1", bob_cyclic, pins["bob_serial"]),
        ("Bob's marginal", (B.count(1), B.count(-1)), pins["marginal"]),
        ("Alice's marginal", (A.count(1), A.count(-1)), pins["marginal"]),
        ("Alice's serial correlation at lag 1", alice_cyclic, pins["alice_serial"]),
        ("same-sign pairs", same, pins["same"]),
        ("Alice's settings, the cycle", sorted(set(settings)), sorted(set(pins["settings"]))),
        ("Alice's settings, the period", period, len(pins["settings"])),
        ("the wheel and Theorem 5", (wheel_ok, theorem5), (True, True)),
    ]
    for name, reading, pin in checks:
        match = reading == pin
        ok = ok and match
        print(
            f"   {'MATCH' if match else 'NO MATCH'} against the algebra: {name}: read {reading}, pinned {pin}"
        )
    verdict = "FAIL" if bob_cyclic != NATURE_SERIAL else "PASS"
    print(
        f"   {verdict} against nature: Bob's serial correlation at lag 1 read {bob_cyclic}, nature {NATURE_SERIAL} (no signalling in the order)"
    )
    return ok


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    results = [analyse(Path(arg)) for arg in argv]
    print(f"== {sum(results)} of {len(results)} runs match every pin")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
