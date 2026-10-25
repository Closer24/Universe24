"""Hand r4 (2026-10-25): the riding massless line on the chain with the volume set by hand (ALGEBRA.md, The line; The paces
compose; The band at a pace; The write per proper volume; the brief's (c)): a standalone integer stepper of one plain line
on the torus [N, 1, 1] at the tests' small universe (den 1,021, Gamma 1,000, T 36,000, G 16), the paces and the volume
from the engine's own functions (core/paces, features/volume), the content a raised by hand 2 units per interval between
plateaus (0, 500, 1000, 1500, 2000, each held `HOLD` intervals; the sudden variant jumps), the line stepped as the branch
steps it (plain) and as the riding line (ride): w [X_now (a_next - a_now) - X_before (a_now - a_before)] + r' - r =
X_now SUM_j R (m_j - a_now), one division at the wall w X_now, X_now = volume_of(a(t)), X_before = volume_of(a(t - 1)).
Read at every plateau (integers): n the upward zero crossings at Node 0, the span s' and the proper count P = SUM p_0
between the first and the last crossing, the largest level A over the plateau, J2 = (A^4 p_a^2 (6 Gamma^2 - p_a^2)) div
(9 Gamma^4) and J its integer root (A^2 sin omega), J_X = J X div Gamma (the riding invariant), the share e at the
plateau's end (the conserved form's Node term over the chain, in W_c), e e^(2U) read as e X div Gamma... each a quotient;
K_proper = (n - 1) Gamma^2 10^6 div (P p_0) and K_board = (n - 1) Gamma^2 10^6 div (s' p_0^2). The uniform drift v = 189
beside the wave: v at every plateau under both lines and v X div Gamma. Outputs ride_chain.json and ride_chain.log."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below, rule_integers  # noqa: E402
from event_universe.features import volume  # noqa: E402

HERE = Path(__file__).resolve().parent
DEN, GAMMA, T, G = 1021, 1000, 36000, 16
N, A0, HOLD, RAISE = 28, 1500, 1200, 2
PLATEAUS = (0, 500, 1000, 1500, 2000)


def rule_at(content):
    p0, pa = paces.clock(GAMMA, content), paces.link_pace(GAMMA, content)
    rule = rule_integers(DEN, DEN, GAMMA, p0, pa, None, G)
    return p0, pa, rule.reaches[0], rule.wall, rule.self_coefficient


def volume_at(content):
    return int(volume.volume_of(GAMMA, [content])[0])


def step(now, before, rem, content_now, content_before, ride):
    """One interval of the line on the chain: plain (the branch's Rule3) or riding."""
    p0, pa, reach, w, _s = rule_at(content_now)
    x_now, x_before = volume_at(content_now), volume_at(content_before)
    nxt, rem2 = [0] * N, [0] * N
    for i in range(N):
        flux = reach * (now[(i + 1) % N] - now[i]) + reach * (now[(i - 1) % N] - now[i])
        if ride:
            numerator = x_now * flux + w * x_now * now[i] + w * x_before * (now[i] - before[i]) + rem[i]
            if ride == 2:  # the half wall's move: the remainder born at half the old wall stands at half the new (step_momentum's clause)
                numerator += (w * (x_now - x_before)) // 2
            wall = w * x_now
        else:
            numerator = flux + w * (now[i] + now[i] - before[i]) + rem[i]
            wall = w
        q = numerator // wall
        nxt[i], rem2[i] = q, numerator - wall * q
    return nxt, now, rem2


def share_total(now, before, content):
    """SUM over the chain of the conserved form's Node term over 2 p_a^2 G^2 (share.py's reading), in quanta of W_c beside."""
    p0, pa, reach, w, s = rule_at(content)
    total = 0
    for i in range(N):
        links = reach * (before[(i + 1) % N] + before[(i - 1) % N])
        total += w * (now[i] * now[i] + before[i] * before[i]) - s * now[i] * before[i] - now[i] * links
    return total // (2 * pa * pa * G * G)


def lay_wave():
    """The travelling wave at k = pi / 2 (V1's lay): now = A cos(k x), before = A cos(k x + omega) at the vacuum, cos omega = 2 / 3."""
    a_c = (A0 * 2) // 3
    a_s = largest_below(A0 * A0 * 5 // 9)
    now = [(A0, 0, -A0, 0)[x % 4] for x in range(N)]
    before = [(a_c, -a_s, -a_c, a_s)[x % 4] for x in range(N)]
    return now, before


def schedule(sudden):
    found = []
    for number, plateau in enumerate(PLATEAUS):
        if number:
            previous = PLATEAUS[number - 1]
            if not sudden:
                found.extend(range(previous + RAISE, plateau, RAISE))
        found.extend([plateau] * HOLD)
    return found


def run(ride, sudden, drift):
    log = []
    if drift:
        now, before = [189] * N, [0] * N
    else:
        now, before = lay_wave()
    _p0, _pa, _reach, w, _s = rule_at(0)
    rem = [(w * volume_at(0)) // 2 if ride else w // 2] * N
    start_level = None
    contents = schedule(sudden)
    previous, readings, plateau_rows = 0, [], []
    t = 0
    crossings, proper, largest, first, last, proper_at = [], 0, 0, None, None, 0
    current = None
    for content in contents:
        if content != current and content in PLATEAUS and contents.count(content) >= HOLD and (current is None or content != current):
            # a plateau begins: the readings reset
            crossings, largest, first, last, proper_at = [], 0, None, None, 0
            current, start_level, start_t = content, now[0], t
        now2, before2, rem = step(now, before, rem, content, previous, ride)
        p0 = paces.clock(GAMMA, content)
        if content in PLATEAUS and current == content:
            if now[0] <= 0 < now2[0]:
                crossings.append(t)
                if first is None:
                    first, proper_at = t, 0
                last = t
            if first is not None:
                proper_at += p0 if t > first else 0
            largest = max(largest, max(abs(v) for v in now2))
        now, before, previous = now2, before2, content
        t += 1
        if (content in PLATEAUS) and (t < len(contents)) and contents[t] != content and current == content:
            plateau_rows.append(read_plateau(content, crossings, first, last, proper_at, largest, now, before, drift, now[0] - start_level, t - start_t))
        elif t == len(contents):
            plateau_rows.append(read_plateau(content, crossings, first, last, proper_at, largest, now, before, drift, now[0] - start_level, t - start_t))
    return plateau_rows


def read_plateau(content, crossings, first, last, proper_at, largest, now, before, drift, moved, held):
    p0, pa, reach, w, s = rule_at(content)
    x = volume_at(content)
    n = len(crossings)
    row = {"content": content, "p_0": p0, "p_a": pa, "X": x, "eU_x10^6": GAMMA * 10 ** 6 // p0, "crossings": n, "largest_level": largest}
    row["mean_level_x_N"] = sum(now)  # the k = 0 mode's level times N (an integer), the remainders' walk and its bias
    row["mean_velocity_x_N"] = sum(now) - sum(before)
    if drift:
        v = now[0] - before[0]
        row.update({"velocity": v, "velocity_x_X_div_Gamma": v * x // GAMMA, "velocity_all_equal": len(set(now[i] - before[i] for i in range(N))) == 1,
                    "level_moved_over_plateau": moved, "plateau_intervals": held, "mean_velocity_x_X_div_Gamma_x_10^3": moved * x * 1000 // (held * GAMMA)})
    else:
        j2 = (largest ** 4 * pa * pa * (6 * GAMMA * GAMMA - pa * pa)) // (9 * GAMMA ** 4)
        j = largest_below(j2)
        row.update({"J": j, "J_X_div_Gamma": j * x // GAMMA, "largest_x_eU_div_10^3": largest * GAMMA // p0 * 1000 // 1000, "largest_div_eU_x10^3": largest * p0 * 1000 // GAMMA})
        if n >= 2:
            span = last - first
            row.update({
                "span_between_crossings": span,
                "proper_between_crossings": proper_at,
                "period_board_quotient_remainder": [span // (n - 1), span % (n - 1)],
                "K_board": (n - 1) * GAMMA * GAMMA * 10 ** 6 // (span * p0 * p0),
                "K_proper": (n - 1) * GAMMA * GAMMA * 10 ** 6 // (proper_at * p0),
            })
    e = share_total(now, before, content)
    row.update({"share_total": e, "share_quanta_W_c": e // (3 * DEN * T), "share_x_Gamma_div_X": e * GAMMA // x})
    return row


if __name__ == "__main__":
    found = {}
    for name, ride, sudden, drift in (
        ("plain_adiabatic", 0, False, False),
        ("ride_nomove_adiabatic", 1, False, False),
        ("ride_adiabatic", 2, False, False),
        ("ride_sudden", 2, True, False),
        ("plain_drift", 0, False, True),
        ("ride_nomove_drift", 1, False, True),
        ("ride_drift", 2, False, True),
    ):
        found[name] = run(ride, sudden, drift)
    (HERE / "ride_chain.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    lines = []
    for name, rows in found.items():
        lines.append(f"== {name}")
        for row in rows:
            lines.append(json.dumps(row))
    (HERE / "ride_chain.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
