"""NC29 probe: the split at the rest (David's sixth text, 2.4) built in a COPY of step.act's passing, run by the
engine's own runner on node-live 36fbfbbde (worktree wt/, read only). Nothing in wt/ is edited: step.act is replaced
in this process only.

The passing, per train and Node-clock, on the window (b, a, a+), from J's potential's live monomials (the loader's):
- a train's own monomial: nothing;
- a two-leg monomial between trains A and B: S_A = (kappa / two) (W_A - W_B), S_B = -S_A (the act's own, times 3);
- a tie group c P |k|^2 (held legs a row squared over every held row, tied legs P): the value at the rest c n P is
  the tied train's own (nothing); the excursion c P (|k|^2 - n) with the excursion as one leg:
  S_held = (kappa / legs) (tied W_held - W_tied_exc), S_tied = -S_held, legs = tied + 1;
- W_A = SUM over A's positions of J_i(a) (a+ - b), J_i(a) = -f PROD over the other positions at a.
kappa = two * legs, every count read off the monomials' legs (two = a two-leg monomial's value legs, tied = a tie
group's tied legs), none typed; the key read at kappa / two times the loader's key, the tooth born at its half.
n: mode "rest0", the held rows' own spring's rest, k = 0 (the laid potential's held-own part is spring |k|^2), so
n = 0 and the whole tie is the excursion; mode "seed", the laid state's |k|^2 at each Node-clock (David's frame-6
reading, a board reading with no law behind it, OPEN).

Usage: python -I split_run.py <mode rest0|seed> <universe> <piece> <setting> <record .jsonl> [<ticks>]
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("wt", "src")))

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import plans  # noqa: E402
from tensor24.runner import run as runmod  # noqa: E402
from tensor24.runner.files import star  # noqa: E402

MODE = sys.argv[1]
WORLD = {}


def prod_rows(v, legs):
    out = None
    for leg in legs:
        out = v[leg] if out is None else out * v[leg]
    return out


def built(loaded):
    """The live monomials classified by the trains their value legs lie in, as index arrays."""
    factor, legs = loaded.potential
    legs = np.stack(legs, axis=1)  # (M, 4), -1 the unit
    _, of, _, _, _ = plans.rows_of(loaded.trains)
    of = np.asarray(of, dtype=np.intp)
    rows = len(of)
    held_t = [t for t in range(len(loaded.trains)) if int(loaded.trains.held[t])]
    assert len(held_t) == 1, held_t
    held_t = held_t[0]
    held_rows = [r for r in range(rows) if of[r] == held_t]
    own, two, ties, kinds = [], [], {}, {"own": 0, "two": 0, "tie": 0}
    for m in range(len(factor)):
        f = int(factor[m])
        if f == 0:
            continue
        vals = [int(h) for h in legs[m] if h >= 0]
        owners = {int(of[h]) for h in vals}
        if len(owners) == 1:
            kinds["own"] += 1
            continue
        if len(vals) == len(owners) == 2:
            kinds["two"] += 1
            two.append((f, [int(h) for h in legs[m]]))
            continue
        hl = [h for h in vals if of[h] == held_t]
        tl = tuple(sorted(h for h in vals if of[h] != held_t))
        assert len(owners) == 2 and held_t in owners and len(hl) == 2 and hl[0] == hl[1], (f, legs[m])
        kinds["tie"] += 1
        ties.setdefault((f, tl), set()).add(hl[0])
    for k, rs in ties.items():
        assert rs == set(held_rows), (k, rs)
    # counts off the monomials: a two-leg monomial's value legs, a tie group's tied legs, the excursion one leg more
    twos = {len([h for h in lg if h >= 0]) for _, lg in two}
    tieds = {len(tl) for _, tl in ties}
    assert len(twos) <= 1 and len(tieds) == 1, (twos, tieds)
    two_n = twos.pop() if twos else len(next(iter(ties))[1])
    tied_n = tieds.pop()
    legs_n = tied_n + 1
    kappa = two_n * legs_n
    WORLD.update(
        of=of, held_t=held_t, held_rows=held_rows, kinds=kinds, groups=sorted(ties), two_n=two_n, tied_n=tied_n,
        legs_n=legs_n, kappa=kappa, half=carry(kappa, two_n, 0)[0], third=carry(kappa, legs_n, 0)[0],
        trains=len(loaded.trains),
    )
    if two:
        f2 = np.array([f for f, _ in two], dtype=object)
        l2 = np.array([lg for _, lg in two], dtype=np.intp)  # unit -1 reads the valued last row
        trs, others = [], []
        for i in range(l2.shape[1]):
            tr = [int(of[lg[i]]) if lg[i] >= 0 else 0 for lg in l2]
            ot = [next(iter({int(of[h]) for h in lg if h >= 0} - {int(of[lg[i]])})) if lg[i] >= 0 else 0 for lg in l2]
            trs.append(np.array(tr, dtype=np.intp)); others.append(np.array(ot, dtype=np.intp))
        WORLD.update(f2=f2, l2=l2, trs=trs, others=others)
    g = WORLD["groups"]
    WORLD.update(
        gc=np.array([c for c, _ in g], dtype=object)[:, None],
        gt=np.array([list(tl) for _, tl in g], dtype=np.intp),
        gtt=np.array([int(of[tl[0]]) for _, tl in g], dtype=np.intp),
    )


def ksq(x):
    return sum(x[r] * x[r] for r in WORLD["held_rows"])


def split_moved(b, a, a1, n):
    """S per train and Node-clock under the split at the rest (the module's docstring)."""
    w = WORLD
    out = np.zeros((w["trains"], a.shape[-1]), dtype=object) * 0
    vb, va, va1 = step.valued(b), step.valued(a), step.valued(a1)
    if "f2" in w:
        f2, l2 = w["f2"], w["l2"]
        m, p = l2.shape
        for i in range(p):
            others = [l2[:, j] for j in range(p) if j != i]
            j_i = -f2[:, None] * prod_rows(va, others)  # (M, sites)
            work = j_i * (va1[l2[:, i]] - vb[l2[:, i]])
            # S_A = half (W_A - W_B): each position's work enters its own train at +half, the other at -half
            # (the unit's work is 0, a+ - b = 0 on it)
            np.add.at(out, w["trs"][i], w["half"] * work)
            np.add.at(out, w["others"][i], -w["half"] * work)
    gc, gt, gtt = w["gc"], w["gt"], w["gtt"]
    held_rows = w["held_rows"]
    # W_held: the tie's own pushes on the held rows, -2 c P(a) k_r, summed over the monomials' held positions
    p_a = prod_rows(va, [gt[:, j] for j in range(gt.shape[1])])
    w_held = 0 * p_a
    for r in held_rows:
        # the leg k_r stands twice in c P k_r k_r, each position's push -c P k_r: the two positions' work
        w_held = w_held + (-gc * p_a * va[r]) * (va1[r] - vb[r]) + (-gc * p_a * va[r]) * (va1[r] - vb[r])
    e = ksq(va) - n  # the excursion's |k|^2 - n at the now slot
    w_tied = 0 * p_a
    for i in range(gt.shape[1]):
        other = prod_rows(va, [gt[:, j] for j in range(gt.shape[1]) if j != i])
        w_tied = w_tied + (-gc * other * e) * (va1[gt[:, i]] - vb[gt[:, i]])
    s_held = w["third"] * (w["tied_n"] * w_held - w_tied)
    np.add.at(out, np.full(len(gtt), w["held_t"]), s_held)
    np.add.at(out, gtt, -s_held)
    return out


def act_x(x, y):
    """The act's X per train from the monomials (for the check against the engine's own passing)."""
    w = WORLD
    factor, legs = WORLD["potential"]
    out = np.zeros((w["trains"], x.shape[-1]), dtype=object) * 0
    vx, vy = step.valued(x), step.valued(y)
    for m in WORLD["live"]:
        lg = legs[m]
        for i in range(4):
            if lg[i] < 0:
                continue
            oth = [lg[j] for j in range(4) if j != i]
            oy, ox = prod_rows(vy, oth), prod_rows(vx, oth)
            out[w["of"][lg[i]]] += -factor[m] * (vx[lg[i]] * oy - vy[lg[i]] * ox)
    return out


CHECK = {"rounds": 0, "equal": 0}


def act(layout, s):
    """A copy of step.act with the passing replaced by the split at the rest; every other line as the engine's."""
    _, _, _, _, gearing, plan, clock, _, click, _, _ = layout
    a, b, tooth, rd, k = s
    force, j1 = step.sources(layout, a)
    _, _, _, teeth, _ = gearing
    first_, second_, factor_, target_, key = click
    first, _ = step.drive(j1, teeth, rd)
    j = j1 + step.stress(layout, s, step.driven(gearing, force, step.kick(gearing, first)))
    q, kept = step.drive(j, teeth, rd)
    kicks = step.kick(gearing, q)
    senses, push = step.halves(layout), step.driven(gearing, force, kicks)
    wa, wb = step.dials(layout, s)
    first, _, _ = step.gear(a, b, tooth, wa + wb, wa + wb, push, senses)
    a1, b1, s1 = step.gear(a, b, tooth, wa + wb, wa + step.weight(gearing, clock, first), push, senses)
    if CHECK["rounds"] < 3:
        jb, ja, ja1 = (contract(plan, step.valued(v), v) for v in (b, a, a1))
        engine = step.passing(click, a, b, ja, jb) + step.passing(click, a1, a, ja1, ja)
        mine = act_x(a, b) + act_x(a1, a)
        CHECK["rounds"] += 1
        CHECK["equal"] += int(np.array_equal(engine, mine))
    moved = split_moved(b, a, a1, WORLD["n"])
    clicks, k1 = carry(moved, key, k)
    return State(a1, b1, s1, kept, k1), clicks


ORIG_LOAD = runmod.load


def load(universe, setting, sites, kinds, c, square):
    loaded, found = ORIG_LOAD(universe, setting, sites, kinds, c, square)
    if found:
        return loaded, found
    built(loaded)
    factor, legs = loaded.potential
    WORLD["potential"] = (factor, np.stack(legs, axis=1))
    WORLD["live"] = [m for m in range(len(factor)) if int(factor[m]) != 0]
    first, second, fac, target, key = loaded.click
    scale = WORLD["half"]  # kappa / two: the act's two-leg passing at kappa two read at kappa
    key3 = key * scale
    a0 = loaded.state[0]
    # the tooth born at (key3 - 1) div senses, the loader's own birth rule and senses
    side = c.shape[-1]
    senses, _ = carry(len(star(side)), side, 0)
    birth, _ = carry(key3 - 1, senses, 0)
    k0 = 0 * loaded.state[4] + birth
    state = (*loaded.state[:4], k0)
    WORLD["n"] = 0 * ksq(a0) if MODE == "rest0" else ksq(a0)
    WORLD["senses"] = senses
    return loaded._replace(click=(first, second, fac, target, key3), state=state), found


runmod.load = load
step.act = act  # tick and untick read step's act: the run back is the same act on the mirrored state


def main():
    universe, piece, setting, record = (Path(p) for p in sys.argv[2:6])
    if len(sys.argv) > 6:
        held = json.loads(setting.read_text(encoding="utf-8"))
        held["ticks"] = int(sys.argv[6])
        cut = record.parent.joinpath(record.stem + "_files")
        cut.mkdir(exist_ok=True)
        setting = cut.joinpath("setting.json")
        setting.write_text(json.dumps(held), encoding="utf-8")
    engine = runmod.Engine(tmain.made, tmain.layout, act, step.untick, State, step.dials, step.grips)
    found = runmod.run(engine, [universe, piece, setting], record)
    w = WORLD
    print(
        json.dumps(
            {
                "mode": MODE, "kinds": w.get("kinds"), "groups": len(w.get("groups", [])), "kappa": w.get("kappa"),
                "half": w.get("half"), "third": w.get("third"), "tied_n": w.get("tied_n"), "senses": w.get("senses"),
                "held_t": w.get("held_t"), "n": [int(v) for v in np.atleast_1d(w.get("n", 0))][:3],
                "act_check_equal": f"{CHECK['equal']} of {CHECK['rounds']}", "found": found,
            }
        )
    )


if __name__ == "__main__":
    main()
