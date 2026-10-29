"""Q2, the composition: which carry turns jointly uniform digits into a c uniform on [0, room) exactly, with no sort,
no if and no bound; the head's sorted composition and its capped room as the mutants. Exact enumeration, Python ints.
Every carry is tensor24.algebra.carry.carry (Rule3: n + r = q d + r', 0 <= r' < d)."""
import itertools
from collections import Counter
from fractions import Fraction

from tensor24.algebra.carry import carry


def pick(c, sizes, room):
    """The split's second carry: c (sum sizes) = t room + r_t; the part whose bracket holds t (the plan's rule)."""
    t, _ = carry(c * sum(sizes), room, 0)
    edge = 0
    for k, s in enumerate(sizes):  # a probe's loop to read which bracket holds t; not the engine's form
        if edge <= t < edge + s:
            return k
        edge += s


def horner(digits):
    """The mixed radix through the carry, no sort and no cap: c = c b + d at each digit, room = room b."""
    c, room = 0, 1
    for d, b in digits:
        c, room = c * b + d, room * b
    return c, room


def summed(digits, room):
    """The sum through the carry: d_1 + ... + d_m = q room + c; q leaves, c stays. Symmetric in the digits."""
    q, c = carry(sum(d for d, _ in digits), room, 0)
    return c, room


def sorted_head(digits, modulus):
    """The head's vernier (src/event_universe/draw.py:83-87): sorted by value, Horner mod M, room capped at M."""
    c, room = 0, 1
    for d, b in sorted(digits):
        _, c = carry(c * b + d, modulus, 0)
        room = min(room * b, modulus)
    return c, room


def capped(digits, modulus):
    """The head's composition with the sort removed but the cap kept: Horner mod M, room = min(prod b, M)."""
    c, room = 0, 1
    for d, b in digits:
        _, c = carry(c * b + d, modulus, 0)
        room = min(room * b, modulus)
    return c, room


def census(compose, bases):
    cnt, room = Counter(), None
    for ds in itertools.product(*[range(b) for b in bases]):
        c, room = compose(list(zip(ds, bases)))
        cnt[c] += 1
    return cnt, room


def report(name, cnt, room):
    tot = sum(cnt.values())
    up = sum(v for c, v in cnt.items() if pick(c, [1, 1], room) == 0)
    flat = len(cnt) == room and len(set(cnt.values())) == 1
    print(f"  {name:34s} room {room:5d}  values hit {len(cnt):5d}  counts min/max "
          f"{min(cnt.values()) if len(cnt) == room else 0}/{max(cnt.values())}  uniform {flat}  "
          f"P(up | 1,1) = {Fraction(up, tot)} = {float(Fraction(up, tot)):.4f}")
    return flat


print("(1) Jointly uniform digits, every tuple enumerated once")
cases = [((5, 7, 9), 100), ((10, 10, 10), 1000), ((6, 6, 6, 6), 1296), ((8, 8, 8), 64), ((2, 3, 4, 5), 120)]
results = {}
for bases, M in cases:
    print(f" bases {bases}, the head's modulus M {M}")
    results[(bases, "horner")] = report("mixed radix by carry (no sort/cap)", *census(horner, bases))
    results[(bases, "summed")] = report(f"sum by carry, room {bases[0]}",
                                        *census(lambda ds: summed(ds, bases[0]), bases))
    results[(bases, "sorted")] = report("MUTANT head: sorted, capped at M", *census(lambda ds: sorted_head(ds, M), bases))
    results[(bases, "capped")] = report("MUTANT unsorted, capped at M", *census(lambda ds: capped(ds, M), bases))
print(" mixed radix uniform at every case:", all(results[(b, "horner")] for b, _ in cases))
print(" sum by carry uniform at every case:", all(results[(b, "summed")] for b, _ in cases))
print(" sorted mutant uniform at any case:", [b for b, _ in cases if results[(b, "sorted")]])
print(" capped mutant uniform exactly where M divides prod b:",
      [(b, M, results[(b, "capped")]) for b, M in cases])

print("\n(2) The one-digit lemma: one digit uniform on [0, room) and independent; the others ANY law (here the sorted")
print("    mutant's own biased c, and a constant): the sum by carry is still uniform on [0, room)")
room = 10
biased, _ = census(lambda ds: sorted_head(ds, 1000), (10, 10, 10))  # 220 values of 1000, max count 6
for name, other in [("others = sorted mutant's c (biased)", biased), ("others = constant 7", Counter({7: 1}))]:
    cnt = Counter()
    for d in range(room):
        for y, wgt in other.items():
            _, c = carry(d + y, room, 0)
            cnt[c] += wgt
    print(f"  {name:40s} counts per residue {sorted(set(cnt.values()))}  uniform {len(set(cnt.values())) == 1 and len(cnt) == room}")
print("  and with NO uniform digit (both from the sorted mutant): ", end="")
cnt = Counter()
for y1, w1 in biased.items():
    for y2, w2 in biased.items():
        _, c = carry(y1 + y2, room, 0)
        cnt[c] += w1 * w2
print(f"counts min/max {min(cnt.values())}/{max(cnt.values())}, uniform {len(set(cnt.values())) == 1}")

print("\n(3) The 24 on the six Meshes' digits: the cube's rotations permute the faces +x,-x,+y,-y,+z,-z")
gens = [(2, 3, 1, 0, 4, 5), (0, 1, 4, 5, 3, 2)]  # 90 deg about z, 90 deg about x, as face permutations
group = {tuple(range(6))}
while True:
    new = {tuple(g[p[i]] for i in range(6)) for p in group for g in gens} | group
    if new == group:
        break
    group = new
print("  rotations generated:", len(group))
b = 3
moved_h = moved_s = 0
tuples = list(itertools.product(range(b), repeat=6))
for ds in tuples:
    h0, _ = horner([(d, b) for d in ds])
    s0, _ = summed([(d, b) for d in ds], b)
    for g in group:
        dg = [ds[g[i]] for i in range(6)]
        moved_h += horner([(d, b) for d in dg])[0] != h0
        moved_s += summed([(d, b) for d in dg], b)[0] != s0
print(f"  over {len(tuples)} tuples x 24 turns at base {b}: mixed radix changed {moved_h} times, sum by carry {moved_s} times")
cnt = Counter(summed([(d, b) for d in ds], b)[0] for ds in tuples)
print(f"  the sum by carry over the six Meshes: counts {dict(sorted(cnt.items()))} (uniform on [0, {b}))")

print("\n(4) Born's pick on a uniform c: part k's count is ceil(sig_<=k room/S) - ceil(sig_<k room/S),")
print("    exactly sig_k room / S where S divides room, within one count otherwise (every room < 80, sizes < 6)")
exact = within = total = 0
for room in range(1, 80):
    for sizes in itertools.product(range(6), repeat=3):
        S = sum(sizes)
        if S == 0:
            continue
        cnt = Counter(pick(c, list(sizes), room) for c in range(room))
        for k, s in enumerate(sizes):
            err = abs(Fraction(cnt.get(k, 0)) - Fraction(s * room, S))
            total += 1
            within += err < 1
            if room % S == 0:
                exact += err == 0
print(f"  {total} part-cases: within one count {within}; at S | room exact in every case: "
      f"{exact == sum(1 for room in range(1, 80) for sizes in itertools.product(range(6), repeat=3) if sum(sizes) and room % sum(sizes) == 0) * 3}")
