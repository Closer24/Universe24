"""``log_symmetry_v1``: time-mirror, period and C-image symmetries of a click log (a declared, read-only layer).

Pre-registered in validation/PREREGISTRATION_log_symmetry_v1.md (04:20 UTC) and frozen on
its own (FROZEN_log_symmetry_v1.json), outside the frozen decoder cores. It supersedes click_mirror_v1 (same mirror
and cycle logic) and takes in the behaviour of r36's read-only observers cycle_compare_v1, phase_split_v1,
mirror_check_v1 and spin_image_v1. A record is (t, x, y, z, g, k, q), read from ``step``, ``address``, ``kind`` and
``quotient`` only; ``period(..., full_records=True)`` compares complete records.

* mirror(log, tau): the partner of (t, x, y, z, g, k, q) is (2 tau + 1 - t, x, y, z, g, -k mod 3, -q).
* best_tau(log): the tau that pairs the most records.
* period(log, P): cycles of P updates compared after shifting; the records that differ.
* c_image(log, T): the record set at n + T against the C image (channel g -> z.g) or K image of the set at n.
* split(log, t_split), record_diff(a, b), shift(records, dt).

    python -m research.click_decoder_v1.log_symmetry_v1 LOG [--tau TAU | --best]
           [--period P [--t0 T0] [--horizon H] [--full]] [--c-image T [--region x0 x1 y0 y1 z0 z1] [--kind C|K]]
           [--diff OTHER_LOG]
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

NAME = "log_symmetry_v1"
# channel of z.g for g = 0..47 in 2O (z = 14), as the decoder config's c_image_table; checked by the tests
Z_TABLE = (14, 23, 24, 33, 34, 35, 36, 43, 32, 44, 31, 27, 26, 45, 0, 39, 42, 21, 37, 41, 38, 17, 40, 1, 2, 47, 12, 11,
           46, 30, 29, 10, 8, 3, 4, 5, 6, 18, 20, 15, 22, 19, 16, 7, 9, 13, 28, 25)


def _lines(log):
    with open(log, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def records(log):
    """The records (t, x, y, z, g, k, q) of a log (a path), or the given list of records unchanged."""
    if isinstance(log, (str, Path)):
        return [(int(r["step"]), *(int(v) for v in r["address"]), int(r["kind"]), int(r["quotient"]))
                for r in _lines(log)]
    return list(log)


def _two(tau):
    s = 2 * tau
    if s != int(s):
        raise ValueError("tau must be an integer or a half-integer")
    return int(s)


def partner(rec, tau):
    t, x, y, z, g, k, q = rec
    return (_two(tau) + 1 - t, x, y, z, g, (-k) % 3, -q)


def mirror(log, tau, lo=None, hi=None, first=5):
    """Pairing about tau (records as a multiset), and mirrored updates n in [lo, hi] (default 1 .. 2 tau): the record
    set at n equals the mirror image of the set at 2 tau + 1 - n (r36's mirror_check_v1)."""
    recs, s = records(log), _two(tau)
    have = Counter(recs)
    paired = sum(min(c, have[partner(r, tau)]) for r, c in have.items())
    unpaired = sorted(r for r, c in have.items() for _ in range(c - min(c, have[partner(r, tau)])))
    per_t = Counter(r[0] for r in unpaired)
    by = defaultdict(set)
    for r in recs:
        by[r[0]].add(r[1:])
    lo, hi = (1 if lo is None else lo), (s if hi is None else hi)
    img = lambda n: {(x, y, z, g, (-k) % 3, -q) for x, y, z, g, k, q in by.get(s + 1 - n, ())}
    ok = sum(1 for n in range(lo, hi + 1) if by.get(n, set()) == img(n))
    silent = [n for n in range(lo, hi + 1) if not by.get(n)]
    return {"tau": tau, "map": "t -> 2 tau + 1 - t, k -> -k mod 3, q -> -q", "records": len(recs), "paired": paired,
            "unpaired": len(unpaired), "unpaired_updates": len(per_t), "unpaired_per_update": dict(sorted(per_t.items())[:50]),
            "first_unpaired": [list(r) for r in unpaired[:first]], "steps": [lo, hi],
            "steps_mirrored": f"{ok}/{hi - lo + 1}", "steps_mirrored_n": ok, "silent_steps": silent[:60]}


def best_tau(log):
    """The tau that pairs the most records; unique if no other tau pairs as many; the runner-up."""
    recs = records(log)
    if not recs:
        return {"tau": None, "unique": None, "unpaired": 0, "runner_up": None, "records": 0}
    by_key = defaultdict(Counter)
    for r in recs:
        by_key[r[1:]][r[0]] += 1
    pairs = Counter()
    for (x, y, z, g, k, q), ts in by_key.items():
        other = by_key.get((x, y, z, g, (-k) % 3, -q))
        if other:
            for t, c in ts.items():
                for t2, c2 in other.items():
                    pairs[t + t2 - 1] += min(c, c2)
    if not pairs:
        return {"tau": None, "unique": None, "unpaired": len(recs), "runner_up": None, "records": len(recs)}
    tau = lambda s: s // 2 if s % 2 == 0 else s / 2
    ranked = sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))
    (s, n), rest = ranked[0], ranked[1:]
    return {"tau": tau(s), "unique": not rest or rest[0][1] < n, "paired": n, "unpaired": len(recs) - n,
            "runner_up": {"tau": tau(rest[0][0]), "unpaired": len(recs) - rest[0][1]} if rest else None,
            "records": len(recs), "taus_tried": len(pairs)}


def period(log, P, t0=0, horizon=None, full_records=False, write_prefix=None):
    """Cycles j = updates t0 + jP + 1 .. t0 + (j + 1)P, with times shifted to 1..P, compared after shifting.
    full_records=True compares the complete JSON records in log order (step shifted, r36's cycle_compare_v1) and
    can write each cycle to ``<write_prefix>_cycle<j+1>.jsonl``."""
    P = int(P)
    if full_records:
        rows = _lines(log)
        times = [int(r["step"]) for r in rows]
    else:
        rows = records(log)
        times = [r[0] for r in rows]
    H = horizon if horizon is not None else max(times, default=t0)
    n_cyc = max(0, (H - t0) // P)
    cyc, before, after = [[] for _ in range(n_cyc)], 0, 0
    for r, t in zip(rows, times):
        j = (t - t0 - 1) // P
        if j < 0:
            before += 1
        elif j >= n_cyc:
            after += 1
        elif full_records:
            r = dict(r)
            r["step"] = t - t0 - j * P
            cyc[j].append(json.dumps(r, separators=(",", ":")))
        else:
            cyc[j].append((t - t0 - j * P, *r[1:]))
    if full_records:
        text = ["".join(x + "\n" for x in c) for c in cyc]
        if write_prefix:
            for j, tx in enumerate(text):
                Path(f"{write_prefix}_cycle{j + 1}.jsonl").write_text(tx, encoding="utf-8")
    else:
        text = ["".join(json.dumps(list(x), separators=(",", ":")) + "\n" for x in sorted(c)) for c in cyc]
    sha = [hashlib.sha256(tx.encode()).hexdigest() for tx in text]
    diffs = []
    for j in range(1, n_cyc):
        a, b = Counter(cyc[0]), Counter(cyc[j])
        diffs.append({"cycle": j, "only_cycle_0": sum((a - b).values()), "only_this_cycle": sum((b - a).values())})
    first = next((d["cycle"] for d in diffs if d["only_cycle_0"] or d["only_this_cycle"] or sha[d["cycle"]] != sha[0]),
                 None)
    return {"period": P, "t0": t0, "horizon": H, "full_records": full_records, "cycles": n_cyc,
            "records_per_cycle": [len(c) for c in cyc], "cycle_sha256": sha,
            "identical": n_cyc > 0 and len(set(sha)) == 1, "first_differing_cycle": first,
            "differences": [d for d in diffs if d["only_cycle_0"] or d["only_this_cycle"]],
            "records_before_t0": before, "records_after_last_cycle": after}


def _in(box, r):
    return box is None or all(lo <= r[1 + i] <= hi for i, (lo, hi) in enumerate(box))


def c_image(log, T, region=None, kind="C", lo=None, hi=None):
    """For n in [lo, hi] (default 1 .. last update - T): the record set at n + T against the image of the set at n;
    C: channel g -> z.g (kind and quotient kept, r36's spin_image_v1); K: channel z.g, k -> -k mod 3, q -> -q.
    region: an optional box ((x0, x1), (y0, y1), (z0, z1)) of sites, bounds included."""
    recs = [r for r in records(log) if _in(region, r)]
    by = defaultdict(set)
    for r in recs:
        by[r[0]].add(r[1:])
    if kind == "C":
        img = lambda v: (v[0], v[1], v[2], Z_TABLE[v[3]], v[4], v[5])
    elif kind == "K":
        img = lambda v: (v[0], v[1], v[2], Z_TABLE[v[3]], (-v[4]) % 3, -v[5])
    else:
        raise ValueError("kind must be C or K")
    last = max(by, default=0)
    lo, hi = (1 if lo is None else lo), (last - T if hi is None else hi)
    ok = plain = clicks = unmatched = 0
    for n in range(lo, hi + 1):
        a, b = by.get(n, set()), by.get(n + T, set())
        ia = {img(v) for v in a}
        ok += b == ia
        plain += b == a and bool(a)
        clicks += bool(a)
        unmatched += len(b ^ ia)
    steps = max(0, hi - lo + 1)
    return {"T": T, "kind": kind, "region": region, "steps": [lo, hi], "image_steps": f"{ok}/{steps}",
            "image_steps_n": ok, "plain_repeat_steps": plain, "steps_with_clicks": clicks,
            "unmatched_records": unmatched, "records_in_region": len(recs)}


def split(log, t_split):
    """(records with t <= t_split, records with t > t_split moved by -t_split): r36's phase_split_v1."""
    recs = records(log)
    return [r for r in recs if r[0] <= t_split], [(r[0] - t_split, *r[1:]) for r in recs if r[0] > t_split]


def shift(log, dt, lo=None, hi=None):
    """The records with lo <= t <= hi (if given), moved by dt updates."""
    return [(r[0] + dt, *r[1:]) for r in records(log) if (lo is None or r[0] >= lo) and (hi is None or r[0] <= hi)]


def record_diff(a, b):
    """Records only in A, only in B (multisets), and the size of the symmetric difference."""
    A, B = Counter(records(a)), Counter(records(b))
    only_a, only_b = sum((A - B).values()), sum((B - A).values())
    return {"records_a": sum(A.values()), "records_b": sum(B.values()), "only_a": only_a, "only_b": only_b,
            "differ": only_a + only_b}


def log_info(log):
    p = Path(log)
    return {"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=NAME)
    ap.add_argument("log")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--best", action="store_true")
    ap.add_argument("--period", type=int)
    ap.add_argument("--t0", type=int, default=0)
    ap.add_argument("--horizon", type=int)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--c-image", type=int, dest="c_image")
    ap.add_argument("--region", type=int, nargs=6)
    ap.add_argument("--kind", default="C")
    ap.add_argument("--diff")
    a = ap.parse_args()
    rep = {"layer": NAME, "log": log_info(a.log)}
    if a.tau is not None:
        rep["mirror"] = mirror(a.log, a.tau if a.tau != int(a.tau) else int(a.tau))
    if a.best:
        rep["best_tau"] = best_tau(a.log)
    if a.period:
        rep["period"] = period(a.log, a.period, a.t0, a.horizon, a.full)
    if a.c_image:
        box = tuple(zip(a.region[0::2], a.region[1::2])) if a.region else None
        rep["c_image"] = c_image(a.log, a.c_image, box, a.kind)
    if a.diff:
        rep["record_diff"] = {"other": log_info(a.diff), **record_diff(a.log, a.diff)}
    print(json.dumps(rep, indent=1))
