"""STOP1 probe: the stop laid as one more block of J's potential, on an extracted tree's own loader, act, runner,
rewind and decoder (the tree read only; the block added in this process alone, nothing written into the tree).

The block (form=each, CONF1 section 7's candidate): for every tied train T and every two pairs (y, z), (w, v) of T's
rows through its kinds' table with itself onto A1 (plans.pairs_of, the tie's own pairs), the monomial
(hold f C_yz C_wv; x_y, x_z, x_w, x_v), f = rest div Gamma by Rule3's carry, hold the file's, as plans.holding's line
68 reads the tie: the factor hold x f x entry x tied[T]. Summed, the block is hold f c_T^2, c_T = SUM C_yz x_y x_z.
A monomial at the factor 0 pushes nothing and enters no passing; they are left out (the tables' zero entries).
Other readings of "the same rule", measured beside it to show what the reading decides (STOP1 section 2):
  form=pairs: every unordered pair of squares of the coupled trains (tied and held) once at hold f, the tie excepted
              (laid already): each c_T^2, the held hand's own c_H^2 (HAT1's quartic without its n), each c_T c_T'.
  form=sum:   each tied square times the tied trains' summed square, hold f c_T SUM_T' c_T' = hold f (SUM_T c_T)^2.
  form=half:  (hold f / 2) (c_H + SUM_T c_T)^2 less the tie: each own square at hold f / 2 (the held hand's too), each
              c_T c_T' at hold f; the half by Rule3's carry (f = 6 den Gamma is even here, the carry's remainder read).
Steps: step=built, the tree's step.act; step=dg, HAT2's linearly implicit discrete gradient, both of a round's dials
gaining kappa(a) = SUM over the monomials and over each pair (legs 1-2, legs 3-4) holding a row twice of 2 f times
the other pair at the now slot. A row held four times (x^4, the stop's (x x)(x x)) is held twice in each of its two
pairs, so it gains 4 f x^2: the polarization V_d = f [P1(z+) P2(z) + P1(z) P2(z+)] = 2 f x+^2 x^2, whose difference
over the window factors as (a+ - b) 2 f a^2 (a+ + b), linear in the row's own next count (STOP1 section 3).
Per run: the record and the ledger the tree's run.run would write (its own functions: promised, clicked, header,
counts, stated, digest; for dg the tooth's promise is read beside, not stopped on), the widest count per round, the
first round past 8/16/32/64/128 bits, the run back from the end state alone with nothing saved (rewind by the tree's
untick), the farthest round it holds back to (the forward states' digests compared, read after it), the decoder's
books, the clicks per train, the 24 (turns=N rounds: every turned lay run against the turned plain run, every field),
and seed=1, the owner's seed test (ii): the lay with one click tooth one unit up runs to the same board.
lam=unit (stopped_lam.py alone): the factor hold x the entries, f left out (the bare entry, Big Pic's "entry at 1").
Usage: python -I stopped_lam.py <tree> <files dir> <record .jsonl> <built|dg> [stop=0|1] [form=each|pairs|sum|half]
       [rounds=N] [turns=N] [seed=1] [every=E]
Whole numbers only; Rule3's carry the one division; no float, root, search or table.
"""

import hashlib
import itertools
import json
import sys
from pathlib import Path

TREE, FILES, RECORD, STEP = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
opts = dict(x.split("=", 1) for x in sys.argv[5:] if "=" in x)
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.decoder import clicks as dclicks  # noqa: E402
from tensor24.decoder import records as drecords  # noqa: E402
from tensor24.decoder import shadow as dshadow  # noqa: E402
from tensor24.engine import kinds as kindsmod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner import plans  # noqa: E402
from tensor24.runner import run as runmod  # noqa: E402
from tensor24.runner.files import departures, held_departures, sites_of, star, vocabulary  # noqa: E402

STOP = opts.get("stop", "0") == "1"
FORM = opts.get("form", "each")
assert STEP in ("built", "dg"), STEP
assert FORM in ("each", "pairs", "sum", "half"), FORM
PATHS = [FILES.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
TREE_LOAD = loadmod.load


def squares(trains, c, traces, which):
    """Per train in `which`, its square's nonzero pairs: (row one, row two, entry) through its form onto A1. The tied
    trains' pairs are plans.pairs_of's; the held hand's square is its rows each once at 1, as plans.holding reads it
    (held[None, :] at the factor 1, its rows its own: A1 x A1 and A2 x A2 onto A1 are 1)."""
    out = {}
    if which == "tied":
        one, two, entry, train = plans.pairs_of(trains, c, traces)
        for i in range(len(entry)):
            t = int(train[i])
            if int(trains.tied[t]) and int(entry[i]):
                out.setdefault(t, []).append((int(one[i]), int(two[i]), int(entry[i])))
    else:
        row, of, _, _, _ = plans.rows_of(trains)
        for r, t in zip(row, of):
            if int(trains.held[int(t)]):
                out.setdefault(int(t), []).append((int(r), int(r), 1))
    return out


def product(p, q, factor):
    """c_P c_Q's monomials at the factor, every pair of P with every pair of Q once in order."""
    return [(factor * e1 * e2, (y, z, w, v)) for (y, z, e1) in p for (w, v, e2) in q]


def stop_block(universe, shape, trains, c, traces):
    """The stop's monomials by the form read (module docstring); every factor hold x f x the entries."""
    _, rest = loadmod.teeth(universe, star(len(shape)))
    f, _ = carry(rest, universe["integers"]["full_rate"], 0)  # plans.holding's line 63
    hf = universe["chosen"]["hold"] * f  # line 68's hold x f
    if opts.get("lam") == "unit":
        hf = universe["chosen"]["hold"]  # the bare entry: the least whole factor with V bounded below (lam > 0)
    tied, held = squares(trains, c, traces, "tied"), squares(trains, c, traces, "held")
    T, H = sorted(tied), sorted(held)
    mono = []
    if FORM == "each":
        for t in T:
            mono += product(tied[t], tied[t], hf)
    elif FORM == "pairs":
        for t in T:
            mono += product(tied[t], tied[t], hf)
        for h in H:
            mono += product(held[h], held[h], hf)
        for x, y in itertools.combinations(T, 2):
            mono += product(tied[x], tied[y], hf)
    elif FORM == "sum":
        for x in T:
            for y in T:
                mono += product(tied[x], tied[y], hf)
    else:
        half, left = carry(hf, 2, 0)
        assert left == 0, "hold f is odd: the half is no whole number"
        for t in T:
            mono += product(tied[t], tied[t], half)
        for h in H:
            mono += product(held[h], held[h], half)
        for x, y in itertools.combinations(T, 2):
            mono += product(tied[x], tied[y], hf)
    return hf, mono


INFO = {}


def stopped_load(universe, setting, sites, kinds, c, square):
    loaded, found = TREE_LOAD(universe, setting, sites, kinds, c, square)
    if found or not STOP:
        return loaded, found
    traces = loadmod.vocabulary(kinds, square)[2][0]
    shape = json.loads(PATHS[1].read_text(encoding="utf-8"))["shape"]
    hf, mono = stop_block(universe, shape, loaded.trains, c, traces)
    INFO["hold f"], INFO["stop monomials"] = hf, len(mono)
    if not mono:
        return loaded, found
    f_old, l_old = loaded.potential
    newf = np.concatenate((np.asarray(f_old, dtype=object), np.array([m[0] for m in mono], dtype=object)))
    newl = tuple(
        np.concatenate((np.asarray(l_old[q]), np.array([m[1][q] for m in mono], dtype=np.intp))) for q in range(4)
    )
    return loaded._replace(potential=(newf, newl)), found


runmod.load = stopped_load  # the runner's own name for the loader: the block enters J's potential, the plan and the passing

# ---- the files, loaded as the runner loads them
found = departures(*PATHS)
assert not found, found
files = [(p, p.read_text(encoding="utf-8")) for p in PATHS]
universe, piece, setting = (json.loads(t) for _, t in files)
shape = piece["shape"]
kinds, tables, square = tmain.made(star(len(shape)))
found = held_departures(universe, setting, vocabulary(kinds, square))
assert not found, found
loaded, found = runmod.load(universe, setting, sites_of(shape), kinds, tables, square)
assert not found, found
if "seed" in opts:
    # the owner's seed test (ii): the same lay, one hidden unit up in one click tooth (the first tied train's, site 0)
    a0, b0, r0, rd0, k0 = loaded.state
    k0 = k0.copy()
    tt = [t for t in range(len(loaded.trains)) if int(loaded.trains.tied[t])][0]
    k0[tt, 0] = k0[tt, 0] + 1
    loaded = loaded._replace(state=(a0, b0, r0, rd0, k0))
layout = tmain.layout(universe, shape, loaded)
start = State(*loaded.state)
ROUNDS = int(opts.get("rounds", setting["ticks"]))
WIDTH = universe["integers"]["width"]
EVERY = int(opts.get("every", 0)) or max(1, ROUNDS)

# ---- dg: HAT2's form, every pair of a monomial's legs holding a row twice adds 2 f times the other pair to its dials
factor, legs = loaded.potential
LIVE = [(int(f), [int(x) for x in lg]) for f, lg in zip(factor, np.stack(legs, axis=1)) if int(f) != 0]
RA, CA, O1, O2 = [], [], [], []
for f, lg in LIVE:
    pairs = ((lg[0], lg[1], lg[2], lg[3]), (lg[2], lg[3], lg[0], lg[1]))
    for p0, p1, q0, q1 in pairs:
        if p0 == p1 and p0 >= 0:
            RA.append(p0)
            CA.append(2 * f)
            O1.append(q0)
            O2.append(q1)
    for r in set(x for x in lg if x >= 0):
        # every row held twice stands twice in one pair (the legs as the plans lay them, a pair's two legs one row);
        # a row held once is a two-leg pair with the unit (the hands' tie) and gains nothing
        m = lg.count(r)
        assert m in (1, 2, 4), lg
        assert m == 1 or (m == 2 and (lg[0] == lg[1] == r or lg[2] == lg[3] == r)) or (m == 4), lg
RA, O1, O2 = (np.array(x, dtype=np.intp) for x in (RA, O1, O2))
CA = np.array(CA, dtype=object)[:, None]


def kappa(a):
    v = step.valued(a)
    k = 0 * a
    if len(RA):
        np.add.at(k, RA, CA * v[O1] * v[O2])
    return k


def act_dg(lay, s):
    _, _, _, _, gearing, plan, clock, _, click, _, _ = lay
    a, b, tooth, rd, k = s
    force, j1 = step.sources(lay, a)
    _, _, _, teeth, _ = gearing
    _, _, _, _, key = click
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(lay, s, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    sns, push = step.halves(lay), step.driven(gearing, force, kicks)
    wa, wb = step.dials(lay, s)
    kap = kappa(a)
    first, _, _ = step.gear(a, b, tooth, wa + wb + kap, wa + wb + kap, push, sns)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb + kap, wa + step.weight(gearing, clock, first) + kap, push, sns)
    jb, ja, ja1 = (step.contract(plan, step.valued(v), v) for v in (b, a, a1))
    moved = step.passing(click, a, b, ja, jb) + step.passing(click, a1, a, ja1, ja)
    clk, k1 = carry(moved, key, k)
    return State(a1, b1, s1, kept, k1), clk


BUILT_ACT = step.act
if STEP == "dg":
    step.act = act_dg  # step.tick, and so step.untick, read the module's act: the run back is the same act mirrored
ACT = step.act


def stated(s):
    return runmod.stated(s)


def bits(s):
    return max(int(abs(int(x))).bit_length() for x in np.concatenate((s.a.ravel(), s.b.ravel())))


def board_digest(s):
    return hashlib.sha256(json.dumps([s.a.tolist(), s.b.tolist(), s.r.tolist(), s.rd.tolist()]).encode()).hexdigest()


def dg_off(s):
    """dg's own promise, read beside: the tooth within the dial the round reads it on, D + kappa(a)."""
    wa, wb = step.dials(layout, s)
    d = wa + wb + kappa(s.a)
    return int(((s.r < -d) | (s.r >= d)).sum())


# ---- the run, as run.run runs it (its own functions), the readings beside
print(f"tree {TREE.name}; files {FILES.name}; step {STEP}; stop {int(STOP)} form {FORM}; "
      f"{INFO if STOP else 'no block'}; rounds {ROUNDS}; sites {start.a.shape[-1]}; rows {start.a.shape[0]}; "
      f"live monomials {len(LIVE)}", flush=True)
found = runmod.promised(tmain.ENGINE, layout, start, WIDTH) if ROUNDS else []
if STEP == "dg":
    found = runmod.wide(start, WIDTH)
assert not found, found
events, s, read_ = [], start, start
digests = [hashlib.sha256(stated(start).encode()).hexdigest()]
first_wide, widest, named, dg_first_off = {}, [], None, None
chain = board_digest(start)
per100 = {}
ledger = runmod.ledger_of(RECORD)
with ledger.open("w", encoding="utf-8") as counted:
    for at in range(1, ROUNDS + 1):
        s, clk = ACT(layout, s)
        counted.writelines(json.dumps(line) + "\n" for line in runmod.counts(at, s, loaded.trains))
        events += runmod.clicked(at, read_, s, clk)
        read_ = s
        w = bits(s)
        widest.append(w)
        for mark in (8, 16, 32, 64, 128):
            if w > mark and mark not in first_wide:
                first_wide[mark] = at
        chain = hashlib.sha256((chain + board_digest(s)).encode()).hexdigest()
        digests.append(hashlib.sha256(stated(s).encode()).hexdigest())
        if STEP == "dg" and dg_first_off is None and at < ROUNDS and dg_off(s):
            dg_first_off = at + 1
        bucket, _ = carry(at - 1, 100, 0)
        for t in range(clk.shape[0]):
            per100.setdefault(t, {}).setdefault(int(bucket), 0)
            per100[t][int(bucket)] += int(abs(clk[t]).sum())
        if STEP == "built":
            found = runmod.promised(tmain.ENGINE, layout, s, WIDTH) if at < ROUNDS else runmod.wide(s, WIDTH)
        else:
            found = runmod.wide(s, WIDTH)
        if carry(at, EVERY, 0)[1] == 0:
            print(f"round {at}: widest {w} bits; chain {chain[:16]}", flush=True)
        if found:
            named = [f"round {at + 1}: {line}" for line in found][:3]
            break
ran = len(widest)
print("ran:", ran, "of", ROUNDS, "rounds; named:", named, flush=True)
print("first round past 8/16/32/64/128 bits:", json.dumps(first_wide), flush=True)
if ran:
    blocks = []
    for lo in range(0, ran, 100):
        blocks.append(f"{lo + 1}-{min(ran, lo + 100)}: {min(widest[lo:lo + 100])}..{max(widest[lo:lo + 100])}")
    print("the counts' width, bits, per 100 rounds:", "; ".join(blocks), flush=True)
    print("widest over the run:", max(widest), "bits; least:", min(widest), flush=True)
if STEP == "dg":
    print("dg's tooth promise (within D + kappa(a), the dial it is read on): first broken at round", dg_first_off, flush=True)
print("board chain digest:", chain, flush=True)
end = s
print("end board digest:", board_digest(end), flush=True)
# the run back from the end state alone, nothing saved: the tree's untick (the act mirrored), round by round as the
# tree's rewind runs it; each backward state's digest read beside against the forward run's (a reading, after)
held_back, b_, broke = 0, end, False
for n in range(1, ran + 1):
    b_ = step.untick(layout, b_)
    if not broke and hashlib.sha256(stated(b_).encode()).hexdigest() == digests[ran - n]:
        held_back = n
    else:
        broke = True
exact = int(stated(b_) == stated(start))
print(f"run back from the end state alone over {ran} rounds: start seed reached, board and every tooth: {bool(exact)}", flush=True)
print(f"run back holds for the last {held_back} of {ran} rounds (back to round {ran - held_back})", flush=True)
first_return = None
d0 = digests[0]
for at in range(1, ran + 1):
    if digests[at] == d0:
        first_return = at
        break
print("first round whose whole state (board and every tooth) is the start seed again:", first_return, flush=True)
if named is None:
    lines = [
        runmod.header(RECORD, files, universe, shape, kinds, loaded, layout),
        *events,
        {"kind": "end", "rounds": ran, "digest": runmod.digest(stated(end)), "undone": ran, "exact": exact},
    ]
    RECORD.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    rec_digest = hashlib.sha256(RECORD.read_bytes()).hexdigest()
    led_digest = hashlib.sha256(ledger.read_bytes()).hexdigest()
    print("record sha256:", rec_digest, "; ledger sha256:", led_digest, flush=True)
    record, cause = drecords.read(str(RECORD))
    if record is None:
        print("decoder: not read:", cause, flush=True)
    else:
        held = dclicks.counted(record)
        labels = {t.get("index"): t.get("label") for t in record.header.get("trains", [])}
        print("click lines:", len(held.lines), flush=True)
        for t, tally in held.trains.items():
            print(f"  train {t} ({labels.get(t)}): {tally.lines} lines, given {tally.given}, taken {tally.taken}, net {tally.net}", flush=True)
        b = dshadow.books(record)
        print("books:", b["kind"], "|", str(b["cause"])[:400], flush=True)
        summed = dclicks.summed(held.lines)
        open_places = sum(1 for v in summed.values() if v != 0)
        print(f"places whose q sum to other than 0: {open_places} of {len(summed)}", flush=True)
else:
    ledger.unlink()
    print("nothing written past the named round (the runner's rule)", flush=True)
nb = max(per100) + 1 if per100 else 0
for t in range(nb):
    print(f"clicks |q| per 100 rounds, train {t}:", [per100[t].get(i, 0) for i in range(len(per100[t]))], flush=True)

# ---- the 24: every turned lay run against the turned plain run, every field, over N rounds
NT = int(opts.get("turns", 0))
if NT:
    rows = start.a.shape[0]
    xyz = np.indices(shape).reshape(3, -1).astype(object)
    sides = np.array(shape, dtype=object)[:, None]

    def turned(m, s):
        _, wrapped = carry(np.array(m, dtype=object) @ xyz, sides, 0)
        site = np.array([int(x) for x in (wrapped[0] * sides[1, 0] + wrapped[1]) * sides[2, 0] + wrapped[2]], dtype=np.intp)
        acting = kindsmod.kinds(np.array(m)[None, :, :])
        turn = np.eye(rows, dtype=object)
        for t in range(len(loaded.trains)):
            train = loaded.trains[t]
            blocks = [kindsmod.square(acting)[0]] if train.square else [acting[k][0] for k in train.kinds]
            before = 0
            for matrix in blocks:
                at = train.first + (before + np.arange(len(matrix))) * train.part
                before += len(matrix)
                for part in range(train.part):
                    turn[np.ix_(at + part, at + part)] = matrix
        out = [np.empty_like(x) for x in s]
        for x, y in zip(out, s):
            x[:, site] = y
        out[0][:, site], out[1][:, site] = turn @ s.a, turn @ s.b
        half, _ = carry(turn @ (s.r + s.r + 1) - 1, 2, 0)
        out[2][:, site] = half
        return State(*out)

    TURNS = []
    for order, signs in itertools.product(itertools.permutations(range(3)), itertools.product((1, -1), repeat=3)):
        m = np.zeros((3, 3), dtype=int)
        m[range(3), order] = signs
        if int(np.dot(m[0], np.cross(m[1], m[2]))) == 1:
            TURNS.append(m)
    assert len(TURNS) == 24
    plain = [start]
    for _ in range(min(NT, ran)):
        plain.append(ACT(layout, plain[-1])[0])
    alike = 0
    for m in TURNS:
        x, ok = turned(m, start), True
        for r in range(1, len(plain)):
            x = ACT(layout, x)[0]
            if stated(x) != stated(turned(m, plain[r])):
                ok = False
                break
        alike += int(ok)
    print(f"the 24: alike in {alike} of 24 turns over {len(plain) - 1} rounds, every field", flush=True)
