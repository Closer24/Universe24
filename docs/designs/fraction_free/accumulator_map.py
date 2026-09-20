"""The fraction-free law: the accumulator against the whole part off the
clock (the mathematician, 2026-09-20, read-only; standalone exact integers,
no import). Output beside this file: `accumulator_map.out`.

by_clock(age, n, d) = floor((age + 1) n / d) - floor(age n / d): the count
gained at one self-creation at the rate n / d read off the clock, no
remainder kept. The accumulator: acc += n; while acc >= d: count += 1,
acc -= d; the remainder owned in acc, 0 <= acc < d.
"""

from __future__ import annotations

import random


def by_clock(age: int, n: int, d: int) -> int:
    return ((age + 1) * n) // d - (age * n) // d


def drive(acc: int, n: int, d: int) -> tuple[int, int]:
    """One self-creation: the count gained and the new accumulator (n < d
    gives 0 or 1; a larger n gives n // d or one more)."""
    acc += n
    count = acc // d
    return count, acc - count * d


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# --------------------------------------------------------------------------
section("1. A constant rate from age 0: the accumulator and by_clock are identical")
rates = [
    (1, 3),
    (32, 55),
    (4198400, 4198400),
    (1836, 1048576),
    (7, 1),
    (1023, 1024),
    (9715512228193, 291465366845793),
]
for n, d in rates:
    acc = 0
    same = True
    for age in range(20000):
        c, acc = drive(acc, n, d)
        if c != by_clock(age, n, d):
            same = False
            break
    print(
        f"   rate {n} / {d}: identical over 20000 self-creations: {same}; the accumulator is (age + 1) n mod d, checked: {acc == (20000 * n) % d}"
    )
print(
    "   proof: after k self-creations acc = k n - count x d with 0 <= acc < d, so count = floor(k n / d): the same whole part, the remainder kept instead of recomputed."
)

section("2. A start at a nonzero age, or a changed rate: where they differ")
n, d = 32, 55
for a0 in (1, 7, 30):
    acc = 0
    differences = []
    for k in range(200):
        c, acc = drive(acc, n, d)
        differences.append(c - by_clock(a0 + k, n, d))
    acc2 = (a0 * n) % d
    same = True
    for k in range(200):
        c, acc2 = drive(acc2, n, d)
        if c != by_clock(a0 + k, n, d):
            same = False
    print(
        f"   start age {a0:2d}, acc 0: per-step differences in {sorted(set(differences))}, the sum {sum(differences)}; with acc initialised to a0 n mod d = {(a0 * n) % d}: identical {same}"
    )
print(
    "   a changed rate: by_clock at the CURRENT rate reads floor(age n' / d) - floor((age - 1) n' / d), a count that forgets the old rate's whole part"
)
acc = 0
clock_counts, drive_counts = [], []
for age in range(120):
    n_t = 32 if age < 60 else 8
    clock_counts.append(by_clock(age, n_t, 55))
    c, acc = drive(acc, n_t, 55)
    drive_counts.append(c)
print(
    f"   rate 32/55 for 60 steps then 8/55: by_clock's Links {sum(clock_counts)} (the first 60: {sum(clock_counts[:60])}, the next 60: {sum(clock_counts[60:])}, longest burst of consecutive 1s after the change {max(len(s) for s in ''.join(map(str, clock_counts[60:])).split('0'))}),"
)
print(
    f"   the accumulator's {sum(drive_counts)} = floor((60 x 32 + 60 x 8) / 55) = {(60 * 32 + 60 * 8) // 55}: the distance the rate drove, exactly, no burst."
)

section("3. A varying numerator (the push): per interval within 1 of each other, the sums")
random.seed(7)
D = 1000
X = [random.randint(0, 5 * D) for _ in range(5000)]
acc = 0
clock_sum = drive_sum = 0
max_diff = 0
for age, x in enumerate(X):
    c1 = by_clock(age, x, D)
    c2, acc = drive(acc, x, D)
    clock_sum += c1
    drive_sum += c2
    max_diff = max(max_diff, abs(c1 - c2))
exact = sum(X) / D
print(
    f"   5000 intervals, X_t uniform in [0, 5 D], D = {D}: the largest per-interval difference {max_diff} (each is floor(X_t / D) or one more);"
)
print(
    f"   the accumulator's sum {drive_sum} = floor(sum X_t / D) = {sum(X) // D} exactly, the remainder {acc} in the accumulator;"
)
print(
    f"   by_clock's sum {clock_sum}: off the exact {exact:.1f} by {clock_sum - exact:+.1f} (a drift with no owner; over T intervals it can reach T in the worst case)."
)
# The worst case: X_t chosen so that by_clock rounds up at every age.
worst = []
for age in range(2000):
    x = next((x for x in range(D - 1, 0, -1) if by_clock(age, x, D) == 1), D - 1)
    worst.append(x)
acc = 0
s_clock = sum(by_clock(a, x, D) for a, x in enumerate(worst))
s_drive = 0
for x in worst:
    c, acc = drive(acc, x, D)
    s_drive += c
print(
    f"   an adversarial X_t below D chosen to round up at every age (2000 intervals): by_clock counts {s_clock}, the exact sum X_t / D = {sum(worst) / D:.1f}, the accumulator {s_drive}."
)

section("4. Additivity: one accumulator takes the directions in any order, exactly")
random.seed(3)
D = 4096
for trial in range(3):
    parts = [random.randint(0, 3 * D) for _ in range(290)]
    acc_a = acc_b = 0
    count_a = count_b = 0
    for x in parts:
        c, acc_a = drive(acc_a, x, D)
        count_a += c
    shuffled = parts[:]
    random.shuffle(shuffled)
    for x in shuffled:
        c, acc_b = drive(acc_b, x, D)
        count_b += c
    c, acc_c = drive(0, sum(parts), D)
    floors = sum(x // D for x in parts)
    print(
        f"   trial {trial}: 290 directions summed one by one {count_a} (acc {acc_a}), shuffled {count_b} (acc {acc_b}), all at once {c} (acc {acc_c}): equal {count_a == count_b == c and acc_a == acc_b == acc_c};"
        f" the per-direction floors sum to {floors}, short by {c - floors} units (at most 289)"
    )
