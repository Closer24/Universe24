"""Light's redshift on the lattice (hand V2, 2026-10-25; the brief's items (b) and (c)): a standing wave of the massless line at the wavelength 4 Links along x on the torus [12, 3, 3] of the tests' small universe (den 1,021, Gamma 1,000, T 36,000), the volume's write off and the content imposed by hand at every interval (common.impose_volume), raised RAMP units of content per interval between plateaus held for SPAN intervals (the adiabatic raise; the brief's lay guard stands at load alone), the interval's acts without the close. Read at every plateau, integers: the Node's upward zero crossings n over the span s at the antinode (the decoder's beat), the proper count P_s = SUM over the span of p_0 (the credit line's proper, in the unit Gamma one vacuum interval), the amplitude A (the largest level over the span), the three-level cosine as a pair of sums (SUM a_t (a_(t+1) + a_(t-1)), 2 SUM a_t^2) against the derived (3 Gamma^2 - p_a^2) / (3 Gamma^2), the invariant's square J2 = (A^4 p_a^2 (6 Gamma^2 - p_a^2)) div (9 Gamma^4), that is A^4 sin^2 omega at the lattice's exact cos omega = 1 - p_a^2 / (3 Gamma^2), the engine's share summed over the board in W_c and the two decoder readings: the board frequency against e^(2 U), K_board = (n Gamma^2 SCALE) div (s p_0^2), and the proper frequency against e^U, K_proper = (n Gamma^2 SCALE) div (P_s p_0) (E(U) e^U, nature's redshift at a conserved number); floats named as checks beside. Command: PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/v2/redshift.py [adiabatic|sudden]"""

from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

import numpy as np

from common import ACTION, DEN, GAMMA, SCALE, dump, impose_volume, lattice_of, paces_at, quotient, volume_at, write_off

from event_universe import records
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features import volume

SHAPE = (12, 3, 3)
WAVES = 3  # the wave number k = 2 pi WAVES / 12 = pi / 2, the wavelength 4 Links, cos k = 0
AMPLITUDE = 400
PLATEAUS = (0, 500, 1000, 1500, 2000)
SPAN = 240  # intervals held at each plateau
RAMP = 2  # units of content per interval on a ramp between plateaus (the adiabatic raise)


def wave_board(folder: Path):  # type: ignore[no-untyped-def]
    """The torus with the massless line's record replaced by the standing wave A cos(k x) at the vacuum's rotation, the levels now and before one half rotation apart, the remainder as laid."""
    board = lattice_of(folder, SHAPE)
    light = board.world.seed
    write_off(board)
    k = 2 * math.pi * WAVES / SHAPE[0]
    cosine = 1 - paces_at(0)["p_a"] ** 2 / (3 * GAMMA**2)  # the vacuum's cos omega at cos k = 0 (the lay alone)
    omega = math.acos(cosine)
    x = np.arange(SHAPE[0]).reshape(SHAPE[0], 1, 1)
    profile = AMPLITUDE * np.cos(k * x)
    now = np.rint(profile * math.cos(omega / 2)) * np.ones(SHAPE)
    before = np.rint(profile * math.cos(-omega / 2)) * np.ones(SHAPE)
    line = board.states[light].lines[0]
    board.states[light].lines[0] = records.Record(
        now.astype(board.kind), before.astype(board.kind), line.remainder
    )
    return board, light


def schedule() -> list[int]:
    """The content at every interval: the plateaus held SPAN intervals, the ramps one unit per interval (the sudden variant jumps between plateaus)."""
    found: list[int] = []
    sudden = len(sys.argv) > 1 and sys.argv[1] == "sudden"
    for number, level in enumerate(PLATEAUS):
        if number:
            previous = PLATEAUS[number - 1]
            if not sudden:
                found += list(range(previous + RAMP, level + 1, RAMP))
        found += [level] * SPAN
    return found


def plateau_reading(level: int, trace: list[int], proper: int, board, light: int) -> dict:  # type: ignore[no-untyped-def]
    """One plateau's integer readings from the antinode's trace over the span."""
    found = paces_at(level)
    p_0, p_a = found["p_0"], found["p_a"]
    span = len(trace) - 1
    crossings = sum(1 for t in range(1, len(trace)) if trace[t - 1] < 0 <= trace[t])
    first = next((t for t in range(1, len(trace)) if trace[t - 1] < 0 <= trace[t]), None)
    last = next((t for t in range(len(trace) - 1, 0, -1) if trace[t - 1] < 0 <= trace[t]), None)
    amplitude = max(abs(a) for a in trace)
    c_num = sum(trace[t] * (trace[t + 1] + trace[t - 1]) for t in range(1, len(trace) - 1))
    c_den = 2 * sum(trace[t] * trace[t] for t in range(1, len(trace) - 1))
    j2 = quotient(amplitude**4 * p_a * p_a * (6 * GAMMA * GAMMA - p_a * p_a), 9 * GAMMA**4)
    shares, _ = board.share_of(light)
    total = int(sum(int(s) for s in np.asarray(shares, dtype=object).ravel()))
    unit = int(board.credit.units[light])
    row = {
        **found,
        "span": span,
        "crossings": crossings,
        "first_crossing": first,
        "last_crossing": last,
        "proper_count": proper,  # SUM over the span of p_0, in the unit Gamma one vacuum interval
        "amplitude": amplitude,
        "cosine_sums": (c_num, c_den),
        "cosine_derived": (3 * GAMMA * GAMMA - p_a * p_a, 3 * GAMMA * GAMMA),
        "cosine_residual_scaled": int(
            division_forward(
                (c_num * 3 * GAMMA * GAMMA - c_den * (3 * GAMMA * GAMMA - p_a * p_a)) * SCALE, c_den * 3 * GAMMA * GAMMA, 0
            )[0]
        ),
        "J2": j2,
        "J": largest_below(j2["quotient"]),
        "share_total": total,
        "share_total_over_W_c_scaled": int(division_forward(total * SCALE, unit, 0)[0]),
        "share_corrected_over_W_c_scaled": int(
            division_forward(total * p_a * p_a * SCALE, unit * GAMMA * GAMMA, 0)[0]
        ),
    }
    if crossings >= 2 and first is not None and last is not None:
        between = last - first
        row["period_board"] = quotient(between, crossings - 1)  # intervals per period, a quotient with remainder
        row["K_board"] = int(division_forward((crossings - 1) * GAMMA * GAMMA * SCALE, between * p_0 * p_0, 0)[0])
    row["check_omega_float"] = (
        2 * math.pi * (crossings - 1) / (last - first) if crossings >= 2 and first is not None else None
    )
    row["check_cos_derived_float"] = 1 - p_a * p_a / (3 * GAMMA * GAMMA)
    row["check_omega_derived_float"] = math.acos(row["check_cos_derived_float"])
    return row


def main() -> None:
    board, light = wave_board(Path(tempfile.mkdtemp(prefix="v2_redshift_")))
    print(f"amplitude bound {board.world.amplitude_bound}, kind {board.kind}, W_c {board.credit.units[light]}")
    contents = schedule()
    traces: dict[int, list[int]] = {}
    propers: dict[int, list[int]] = {}
    plateau_at = {}
    for t, level in enumerate(contents):
        x = volume_at(level)
        impose_volume(board, x, x - x // 2)
        board.advanced_to_the_close()
        assert not board.turned.any(), "a top fired under the imposed volume"
        if t % 200 == 0:
            print(f"interval {t} of {len(contents)} at the level {level}", flush=True)
        if level in PLATEAUS:
            if level not in traces:
                traces[level] = []
                propers[level] = []
                plateau_at[level] = board.interval
            traces[level].append(int(np.asarray(board.states[light].lines[0].now, dtype=object)[0, 0, 0]))
            propers[level].append(paces_at(level)["p_0"])
    rows = []
    for level in PLATEAUS:
        trace, proper = traces[level], propers[level]
        row = plateau_reading(level, trace, sum(proper), board, light)
        if "period_board" in row:
            first, last = row["first_crossing"], row["last_crossing"]
            proper_between = sum(proper[first:last])  # the proper count between the first and the last crossing
            row["proper_between"] = proper_between
            row["period_proper_scaled"] = int(division_forward(proper_between * SCALE, (row["crossings"] - 1) * GAMMA, 0)[0])
            row["K_proper"] = int(
                division_forward((row["crossings"] - 1) * GAMMA * GAMMA * SCALE, proper_between * row["p_0"], 0)[0]
            )
        rows.append(row)
        print(
            f"plateau level {level:5d} p_0 {row['p_0']:4d} p_a {row['p_a']:4d} e^U x1e6 {row['e_U_scaled']:8d} span {row['span']} "
            f"crossings {row['crossings']} period {row.get('period_board', {}).get('quotient', '-')}+"
            f"{row.get('period_board', {}).get('remainder', '-')}/{row['crossings'] - 1 if row['crossings'] > 1 else '-'} "
            f"A {row['amplitude']} J {row['J']} cos residual x1e6 {row['cosine_residual_scaled']} "
            f"share/W_c x1e6 {row['share_total_over_W_c_scaled']} corrected x1e6 {row['share_corrected_over_W_c_scaled']} "
            f"K_board {row.get('K_board', '-')} K_proper {row.get('K_proper', '-')} "
            f"check omega {row['check_omega_float']} derived {row['check_omega_derived_float']:.6f}"
        )
    name = "redshift_sudden.json" if len(sys.argv) > 1 and sys.argv[1] == "sudden" else "redshift.json"
    print(dump(name, {"shape": SHAPE, "waves": WAVES, "amplitude": AMPLITUDE, "plateaus": rows, "den": DEN, "gamma": GAMMA, "T": ACTION}))


if __name__ == "__main__":
    main()
