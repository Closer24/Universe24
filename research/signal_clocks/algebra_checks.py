"""Finite exact checks of signal-clock algebra; no forward-engine modification.

The prescribed-input examples are scalar truth tables, not closed-board devices.
Use the full-board experiment suite for any realizability or routing claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from universe24.core.rule3 import forward, inverse
from universe24.core.state import Channel


def phase_oracle(state: Channel, u: int) -> Channel:
    """Independent three-phase quotient form of the unchanged scalar rule."""
    theta, parity = state.r // 2, state.r % 2
    carry = (u + theta) // 3
    next_theta = u + theta - 3 * carry
    return Channel(state.b, carry - state.a, 2 * next_theta + parity)


def local_two_arrivals(wait: int = 6, tail: int = 8, amplitude: int = 1) -> list[dict]:
    """A declared externally prescribed scalar input sequence, never an engine run.

    Two (+amplitude,-amplitude) pair inputs separated by `wait` zero-input updates. This is
    useful as a component requirement; it supplies no spatial sources.
    """
    if type(wait) is not int or wait < 0 or type(tail) is not int or tail < 0:
        raise ValueError("wait and tail must be nonnegative integers")
    if type(amplitude) is not int or amplitude <= 0:
        raise ValueError("amplitude must be a positive integer")
    pair = (Channel(0, 0, 2), Channel(0, 0, 2))
    history = [{"step": 0, "pair": [list(x) for x in pair], "input": None,
                "guarded_C": [None, None]}]
    arrival = (amplitude, -amplitude)
    inputs = [arrival] + [(0, 0)] * wait + [arrival] + [(0, 0)] * tail
    for step, sums in enumerate(inputs, 1):
        old = pair
        pair = tuple(phase_oracle(s, u) for s, u in zip(pair, sums))
        events = [((new.r - before.r) // 2) % 3
                  if new.b + before.a != 0 and new != before else None
                  for before, new in zip(old, pair)]
        history.append({"step": step, "pair": [list(x) for x in pair],
                        "input": list(sums), "guarded_C": events})
    return history


def check_algebra() -> dict:
    start = time.process_time()
    checked = 0
    huge = 10 ** 5000 + 17
    pairs = [(a, b) for a in range(-3, 4) for b in range(-3, 4)]
    pairs += [(huge, -huge), (-huge, huge), (0, huge), (huge, 0)]
    inputs = list(range(-12, 13))
    for a, b in pairs:
        for r in range(6):
            old = Channel(a, b, r)
            for u in inputs:
                new = forward(old, u)
                expected = phase_oracle(old, u)
                assert new == expected, (a, b, r, u)
                assert inverse(new, u) == old
                assert new.r % 2 == r % 2
                assert ((new.r != r) == (u % 3 != 0))
                carry = new.b + old.a
                assert 2 * u + r == 6 * carry + new.r
                checked += 1
    zero_inputs = 0
    for a, b in pairs:
        for r in range(6):
            initial = Channel(a, b, r)
            state = initial
            seen = []
            for _ in range(4):
                state = phase_oracle(state, 0)
                seen.append(state)
            assert state == initial
            if a or b:
                assert all(s != initial for s in seen[:3])
            else:
                assert all(s == initial for s in seen)
            zero_inputs += 1
    waiting_cases = 0
    for wait in (0, 1, 4, 6, 12):
        trajectory = local_two_arrivals(wait, 12)
        remainders = [tuple(s[2] for s in sample["pair"]) for sample in trajectory]
        edges = [i for i in range(1, len(trajectory)) if remainders[i] != remainders[i-1]]
        assert edges == [1, wait + 2]
        assert remainders[0] == (2, 2)
        assert all(x == (4, 0) for x in remainders[1:wait+2])
        assert all(x == (0, 4) for x in remainders[wait+2:])
        assert all(all(s[0] == s[1] == 0 for s in sample["pair"])
                   for sample in trajectory[:wait+2])
        waiting_cases += 1
    guarded_waiting_cases = 0
    for wait in (4, 6, 8, 10, 12):
        trajectory = local_two_arrivals(wait, 12, amplitude=4)
        memory = [tuple(s[2] for s in sample["pair"]) for sample in trajectory]
        event_steps = [sample["step"] for sample in trajectory
                       if any(c is not None for c in sample["guarded_C"])]
        assert event_steps == [1, wait + 2]
        assert all(trajectory[t]["guarded_C"] == [1, 2] for t in event_steps)
        assert memory[0] == (2, 2)
        assert all(m == (4, 0) for m in memory[1:wait+2])
        assert all(m == (0, 4) for m in memory[wait+2:])
        guarded_waiting_cases += 1
    off = (phase_oracle(Channel(0, 0, 2), 1),
           phase_oracle(Channel(0, 0, 2), -1))
    on = (phase_oracle(Channel(0, 0, 4), 1),
          phase_oracle(Channel(0, 0, 0), -1))
    assert tuple(s.b for s in off) == (0, 0)
    assert tuple(s.b for s in on) == (1, -1)
    return {
        "format": "universe24-signal-clock-algebra-v1",
        "passed": True,
        "scope": "Finite scalar oracle checks and prescribed-input truth tables; no closed-board realization claim",
        "scalar_cases": checked,
        "scalar_domain": {"a_b": "[-3,3]^2 plus four 5001-digit pairs", "r": [0, 5], "u": [-12, 12]},
        "zero_input_cycle_cases": zero_inputs,
        "two_arrival_wait_cases": waiting_cases,
        "guarded_C_two_arrival_wait_cases": guarded_waiting_cases,
        "prescribed_silent_priming_example": local_two_arrivals(),
        "prescribed_guarded_C_example": local_two_arrivals(amplitude=4),
        "state_conditioned_output": {"identical_input": [1, -1],
             "memory_2_2_output_b": [s.b for s in off],
             "memory_4_0_output_b": [s.b for s in on],
             "closed_board_routing_proven": False},
        "cpu_seconds": time.process_time() - start,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output exists; choose a new evidence path")
    result = check_algebra()
    root = Path(__file__).resolve().parents[2]
    sources = [Path(__file__).resolve(), root / "universe24/core/rule3.py",
               root / "universe24/core/state.py"]
    result["source_sha256"] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sources}
    if result["cpu_seconds"] > 180:
        raise RuntimeError("scalar verification exceeded the 180 CPU-second budget")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"passed": result["passed"], "scalar_cases": result["scalar_cases"],
                      "zero_input_cycle_cases": result["zero_input_cycle_cases"],
                      "cpu_seconds": result["cpu_seconds"]}))


if __name__ == "__main__":
    main()
