"""Generic click decoder v1.1 (frozen separately; v1.0 in ``decoder.py`` stays unchanged).

Same input contract as v1.0: only ``step``, ``address``, ``kind`` and ``quotient`` of each record;
side, horizon and (optionally) a light speed ``c`` are declared by the caller. The unchanged
primitives (torus geometry, clusters, exact runs, kinematics) are imported from v1.0. Changes
against v1.0 (README, "v1.1"):

(i) C-image laps: lap(n+1) = C(lap n), C: g -> z.g (z = 14, a fixed 48-entry table in the config);
(g) tracks split at velocity changes and split-born tracks take back their share of the shared
    clusters down to the real split; (h) arm walks stop at feeding cycles, and non-periodic sites
    get a second test with passing movers' clicks removed; (j) arrival map, and class "c-light"
    for a declared c; (a) the period that explains most click updates; (b) "translating" only over
    a full source period; (c) co-moving merge only for tracks born together; (d) fragments whose
    union is an exact co-mover become one track; (e) sheet co-movers (all shifts |v|_1 <= T for
    small T, sampled pre-check, larger cap); (f) one summary schema; reports carry the log's file
    name and SHA-256, not its path; the prediction window and velocity search box are config values.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import hashlib
import json
import math
from pathlib import Path

from . import decoder as V0
from .decoder import (Cluster, Track, Torus, _accept, _capped_distance, _components, _dilate, _direction,
                      _dmin, _feeder, _fit, _kinds, _kinematics, _l1, _lcm, _longest_run, _offsets, _pattern,
                      _slow, _velocity_out)

NAME = "click_decoder_v1"
VERSION = "1.1"
HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config_v1.1.json"
SOURCES = ("decoder.py", "decoder_v11.py", "layers.py", "correlate.py", "config_v1.1.json")


def read_log(path):
    """(events, info) as in v1.0, but the info carries the file name and SHA-256, not the path."""
    events, info = V0.read_log(path)
    info = {"name": Path(path).name, **{k: v for k, v in info.items() if k != "path"}}
    return events, info


def load_config(path=None) -> dict:
    return json.loads(Path(path or CONFIG).read_text(encoding="utf-8"))


def code_fingerprint() -> dict:
    return {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in SOURCES}


# ------------------------------------------------------------------ periods (a) and C-image laps (i)
def _period(pat, lo, hi, cfg, pmax=None):
    """The period whose exact run (>= period_min_reps periods) covers the most click updates; ties go to
    the smallest period. Silent updates never count, so multiples of the true period gain nothing."""
    reps = cfg["period_min_reps"]
    times = sorted(pat)
    if len(times) < reps:
        return None
    best = None
    for p in range(1, min(pmax or cfg["period_max"], (hi - lo + 1) // reps) + 1):
        seg = _accept(_longest_run(times, lambda t: pat.get(t) == pat.get(t + p), lo, hi, p), p, times, reps)
        if seg:
            covered = sum(1 for t in times if seg[0] <= t <= seg[1])
            if best is None or covered > best[2]:
                best = (p, seg, covered)
                if covered == len(times):
                    break
    return (best[0], best[1]) if best else None


def _c_run(rec, T, table, gi, lo, hi):
    """Longest run [a, b] with C(rec(t)) == rec(t + T); rec maps t -> sorted tuple with the channel at gi."""
    def img(v):
        return tuple(sorted(x[:gi] + (table[x[gi]],) + x[gi + 1:] for x in v))
    times = sorted(rec)
    return _longest_run(times, lambda t: (img(rec[t]) if t in rec else ()) == rec.get(t + T, ()), lo, hi, T), times


def _c_image(rec, T, table, gi, lo, hi, cfg):
    """C-image relation with lap T on >= c_image_min_laps lap-to-lap steps, and not a plain T-period."""
    run, times = _c_run(rec, T, table, gi, lo, hi)
    if run is None:
        return None
    a, b = run
    laps = (b - a + 1) // T
    clicks = sum(1 for t in times if a <= t <= b + T)
    if laps < cfg["c_image_min_laps"] or clicks < cfg["period_min_reps"]:
        return None
    if all(rec.get(t) == rec.get(t + T) for t in range(a, b + 1)):
        return None                       # C-invariant records: no 360-degree signature
    return {"z": cfg["c_image_z"], "lap": T, "laps_verified": laps, "window": [a, b + T], "return_after": 2 * T}


# ------------------------------------------------------------------ tracks (P6: prediction window from config)
def _predict(tr, t, window):
    pts, ts = tr.path[-window:], [o.t for o in tr.obs[-window:]]
    if len(pts) < 2 or ts[-1] == ts[0]:
        return pts[-1]
    v = [(pts[-1][i] - pts[0][i]) / (ts[-1] - ts[0]) for i in range(3)]
    return tuple(pts[-1][i] + v[i] * (t - ts[-1]) for i in range(3))


def _tracks(clusters, torus, cfg):
    tracks, open_ = [], []
    slack = cfg["link_slack"]
    for t in sorted(clusters):
        cand, props = clusters[t], []
        for tr in open_:
            last = tr.obs[-1]
            dt = t - last.t
            slow = _slow(tr, cfg)
            if dt > (cfg["rest_link_gap"] if slow else cfg["link_gap"]):
                continue
            pred = _predict(tr, t, cfg["predict_window"])
            for ci, c in enumerate(cand):
                if torus.cheb(last.c, c.c) > dt + slack + last.r + c.r + 1:
                    continue
                dm = _dmin(last.sites, c.sites, torus, dt + slack)
                if dm is None:
                    continue
                dp = torus.cheb(pred, c.c)
                if slow and dp > cfg["slow_max_deviation"]:
                    continue
                props.append((round(dp, 6), dm, tr.id, ci))
        props.sort()
        used, owner = set(), {}
        for _, _, ti, ci in props:
            if ti not in used and ci not in owner:
                used.add(ti)
                owner[ci] = ti
        for ci, c in enumerate(cand):
            if ci in owner:
                tr = tracks[owner[ci]]
                tr.path.append(torus.unwrap(tr.path[-1], c.c))
                tr.obs.append(c)
            else:
                parent = next((ti for _, _, ti, cj in props if cj == ci), None)
                tracks.append(Track(len(tracks), c, parent))
        open_ = [tr for tr in tracks if t - tr.obs[-1].t <= cfg["rest_link_gap"]]
    return tracks


def _repath(tr, torus):
    tr.path = [tr.obs[0].c]
    for o in tr.obs[1:]:
        tr.path.append(torus.unwrap(tr.path[-1], o.c))


def _vel(obs, path):
    return _fit([o.t for o in obs], path)


def _sub(o, keep, events, torus):
    ks = set(keep)
    return Cluster(o.t, sorted(ks), torus, [i for i in o.ev if events[i][1:4] in ks])


def _backdate(tracks, events, torus, cfg):
    """(g) A split-born track takes back, update by update, the parent's sites that lie on its own
    back-extrapolated path (nearer to it than to the parent's), down to where the two separate."""
    m, r = cfg["split_min_obs"], cfg["split_radius"]
    for tr in tracks:
        if tr.parent is None or len(tr.obs) < m:
            continue
        par = tracks[tr.parent]
        tc = tr.obs[0].t
        after = [k for k, o in enumerate(par.obs) if o.t >= tc]
        before = [k for k, o in enumerate(par.obs) if o.t < tc]
        if len(after) < 2 or not before:
            continue
        vc = _vel(tr.obs[:12], tr.path[:12])
        pa = [par.path[k] for k in after[:12]]
        vp = _vel([par.obs[k] for k in after[:12]], pa)
        if max(abs(vc[i] - vp[i]) for i in range(3)) < cfg["split_min_dvel"]:
            continue
        t_pa = par.obs[after[0]].t
        taken = []
        for k in reversed(before):
            o = par.obs[k]
            pc = tuple(tr.path[0][i] - vc[i] * (tc - o.t) for i in range(3))
            pp = tuple(pa[0][i] - vp[i] * (t_pa - o.t) for i in range(3))
            if torus.cheb(pc, pp) < 1:
                break
            mine = [q for q in o.sites if torus.cheb(q, pc) <= r and torus.cheb(q, pc) < torus.cheb(q, pp)]
            rest = [q for q in o.sites if q not in set(mine)]
            if not mine or not rest:
                break
            par.obs[k] = _sub(o, rest, events, torus)
            taken.append(_sub(o, mine, events, torus))
        if taken:
            tr.obs = taken[::-1] + tr.obs
            _repath(tr, torus)
            _repath(par, torus)
    return tracks


def _segments(ts, path, cfg):
    """Breakpoints splitting a path into pieces of constant velocity (recursive best two-piece fit)."""
    m = cfg["split_min_obs"]
    n = len(ts)
    if n < 2 * m:
        return []

    def fit(lo, hi):
        t, p = ts[lo:hi], path[lo:hi]
        v = _fit(t, p)
        mt = sum(t) / len(t)
        mp = [sum(q[i] for q in p) / len(p) for i in range(3)]
        sse = sum((q[i] - mp[i] - v[i] * (tt - mt)) ** 2 for tt, q in zip(t, p) for i in range(3))
        return v, math.sqrt(sse / len(t))

    v_all, rms_all = fit(0, n)
    if rms_all <= cfg["split_max_rms"]:
        return []
    best = None
    for k in range(m, n - m + 1):
        (va, ra), (vb, rb) = fit(0, k), fit(k, n)
        if ra <= cfg["split_max_rms"] and rb <= cfg["split_max_rms"] and \
                max(abs(va[i] - vb[i]) for i in range(3)) >= cfg["split_min_dvel"]:
            if best is None or ra + rb < best[0]:
                best = (ra + rb, k)
    if best is None:
        return []
    k = best[1]
    return _segments(ts[:k], path[:k], cfg) + [k] + [k + j for j in _segments(ts[k:], path[k:], cfg)]


def _split_velocity(tracks, cfg):
    """(g) A track whose path has pieces of different constant velocity becomes one track per piece;
    each later piece is born from the earlier one at the change."""
    out = []
    for tr in tracks:
        cuts = _segments([o.t for o in tr.obs], tr.path, cfg)
        if not cuts:
            out.append(tr)
            continue
        bounds = [0] + cuts + [len(tr.obs)]
        prev = None
        for a, b in zip(bounds, bounds[1:]):
            piece = Track(tr.id, tr.obs[a], tr.parent if prev is None else prev)
            piece.obs, piece.path = tr.obs[a:b], tr.path[a:b]
            out.append(piece)
            prev = piece
    # renumber; parents refer to objects until here
    idx = {}
    for k, tr in enumerate(out):
        idx[id(tr)] = k
    first_of = {}
    for tr in out:
        first_of.setdefault(tr.id, tr)
    for k, tr in enumerate(out):
        p = tr.parent
        if isinstance(p, Track):
            tr.parent = idx[id(p)]
        elif p is not None:
            tr.parent = idx[id(first_of[p])] if p in first_of else None
    for k, tr in enumerate(out):
        tr.id = k
    return out


# ------------------------------------------------------------------ exact co-moving symmetry (e)
def _exact_motion(pat, t0, t1, vel, torus, cfg, min_coverage=None):
    """Smallest (T, v), |v|_1 <= T, with pattern(t + T) == pattern(t) shifted by v on >= reps periods and
    on >= exact_min_coverage of the click updates. Candidates: the rounded fitted displacement +- velocity_search_box, and for T <= ball_search_max_T
    every shift with |v|_1 <= T (a sheet has no meaningful centroid). A sampled pre-check rejects most."""
    if not pat or max(len(p) for p in pat.values()) > cfg["exact_max_events_per_step"]:
        return None
    reps, box = cfg["period_min_reps"], cfg["velocity_search_box"]
    times = sorted(pat)
    lab = {t: tuple(sorted(Counter(e[3:] for e in p).items())) for t, p in pat.items()}
    sets = {}
    for T in range(1, min(cfg["track_period_max"], (t1 - t0 + 1) // reps) + 1):
        if not _accept(_longest_run(times, lambda t: lab.get(t) == lab.get(t + T), t0, t1, T), T, times, reps):
            continue
        base = [round(vel[i] * T) for i in range(3)]
        cands = {(base[0] + a, base[1] + b, base[2] + c) for a, b, c in product(range(-box, box + 1), repeat=3)}
        if T <= cfg["ball_search_max_T"]:
            cands |= {v for v in product(range(-T, T + 1), repeat=3)}
        cands = sorted((v for v in cands if 0 < sum(map(abs, v)) <= T),
                       key=lambda v: (sum((v[i] - vel[i] * T) ** 2 for i in range(3)), v))
        probe = [t for t in times if t + T in pat]
        probe = probe[::max(1, len(probe) // cfg["exact_sample_steps"])][:cfg["exact_sample_steps"]]
        for t in probe:
            sets.setdefault(t + T, set(pat[t + T]))
        for v in cands:
            if probe and not any(all(torus.shift(e[:3], v) + e[3:] in sets[t + T]
                                     for e in pat[t][:cfg["exact_sample_events"]]) for t in probe):
                continue

            def same(t, v=v):
                a, b = pat.get(t, ()), pat.get(t + T, ())
                return len(a) == len(b) and tuple(sorted(torus.shift(e[:3], v) + e[3:] for e in a)) == b
            seg = _accept(_longest_run(times, same, t0, t1, T), T, times, reps)
            # the exact run must explain most of the track, not only 3 periods somewhere inside it
            cover = cfg["exact_min_coverage"] if min_coverage is None else min_coverage
            if seg and sum(1 for t in times if seg[0] <= t <= seg[1]) >= cover * len(times):
                return T, v, seg
    return None


# ------------------------------------------------------------------ arrival map and c-light (j)
def _solve(A, b):
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def _line_fit(xs, ts):
    if len(xs) < 2:
        return None
    mx, mt = sum(xs) / len(xs), sum(ts) / len(ts)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    b = sum((x - mx) * (t - mt) for x, t in zip(xs, ts)) / den
    rms = math.sqrt(sum((t - mt - b * (x - mx)) ** 2 for x, t in zip(xs, ts)) / len(xs))
    return {"speed": round(1 / b, 6) if b > 0 else None, "rms": round(rms, 4), "sites": len(xs)}


def _arrival_map(events, torus, cfg, wrap_bound):
    first = {}
    for e in events:
        first.setdefault(e[1:4], e[0])
    t0 = min(first.values())
    o = torus.centroid([s for s, t in first.items() if t == t0])
    pts = []
    for s, t in first.items():
        d = [torus.d(o[i], s[i]) for i in range(3)]
        if max(map(abs, d)) >= cfg["arrival_min_distance"] and t < wrap_bound:
            pts.append((t, d))
    out = {"origin": [round(c, 2) for c in o], "first_update": t0, "sites": len(pts), "radial": {}, "directions": {}}
    if len(pts) < cfg["arrival_min_sites"]:
        return out
    ts = [p[0] for p in pts]
    for name, f in (("euclid", lambda d: math.sqrt(sum(x * x for x in d))), ("l1", lambda d: sum(map(abs, d))),
                    ("max", lambda d: max(map(abs, d)))):
        out["radial"][name] = _line_fit([f(p[1]) for p in pts], ts)
    A = [[0.0] * 4 for _ in range(4)]
    b = [0.0] * 4
    for t, d in pts:
        row = [1.0, *d]
        for i in range(4):
            b[i] += row[i] * t
            for j in range(4):
                A[i][j] += row[i] * row[j]
    sol = _solve(A, b)
    if sol:
        k = sol[1:]
        nk = math.sqrt(sum(x * x for x in k))
        res = math.sqrt(sum((t - sol[0] - sum(k[i] * d[i] for i in range(3))) ** 2 for t, d in pts) / len(pts))
        out["plane_wave"] = {"speed": round(1 / nk, 6) if nk else None,
                             "direction": [round(x / nk, 4) for x in k] if nk else None, "rms": round(res, 4)}

    def cls(d):
        a = sorted(abs(x) for x in d)
        if a[1] < 0.5:
            return "axis"
        if a[0] < 0.5 and abs(a[1] - a[2]) < 0.5:
            return "face_diagonal"
        if abs(a[0] - a[2]) < 0.5:
            return "body_diagonal"
        return None
    groups = defaultdict(list)
    for t, d in pts:
        c = cls(d)
        if c:
            groups[c].append((math.sqrt(sum(x * x for x in d)), t))
    for c, v in sorted(groups.items()):
        if len(v) >= cfg["arrival_min_sites"]:
            out["directions"][c] = _line_fit([x for x, _ in v], [t for _, t in v])
    return out


# ------------------------------------------------------------------ sources
def _source(comp, periodic, basis, site_pat, by_site, excluded, events, torus, cfg, lo, hi, arms):
    sites = sorted(comp)
    p = _lcm(periodic[s][0] for s in sites)
    if p > cfg["period_max"]:
        return None
    table = cfg["c_image_table"]
    joint = defaultdict(list)
    for s in sites:
        for i in by_site[s]:
            if i not in excluded.get(s, ()):
                e = events[i]
                joint[e[0]].append((s, *e[4:]))
    jp = {t: tuple(sorted(v)) for t, v in joint.items()}
    times = sorted(jp)
    reps = cfg["period_min_reps"]
    seg = _accept(_longest_run(times, lambda t: jp.get(t) == jp.get(t + p), lo, hi, p), p, times, reps)
    src_basis = "exact"
    if seg is None and p % 2 == 0:
        ci = _c_image(jp, p // 2, table, 1, lo, hi, cfg)
        if ci:
            seg, src_basis = tuple(ci["window"]), "c_image"
    jointly = seg is not None
    if seg is None:
        seg = (max(periodic[s][1][0] for s in sites), min(periodic[s][1][1] for s in sites))
        if seg[1] - seg[0] + 1 < p:
            return None
    a, e = seg
    p0s = []
    for s in sites:
        r = _period(site_pat(s, chan=False), lo, hi, cfg, pmax=p)
        p0s.append(r[0] if r else p)
    p0 = _lcm(p0s)
    cimg = None
    if p % 2 == 0 and (p // 2) % p0 == 0:
        cimg = _c_image(jp, p // 2, table, 1, lo, hi, cfg)
    own = lambda i, s: i not in excluded.get(s, ())
    win = [i for s in sites for i in by_site[s] if a <= events[i][0] < a + p and own(i, s)]
    first = min(events[i][0] for s in sites for i in by_site[s]
                if periodic[s][1][0] <= events[i][0] <= periodic[s][1][1] and own(i, s))
    bsites = sorted({events[i][1:4] for s in sites for i in by_site[s] if events[i][0] == first and own(i, s)})
    phases = sorted({(events[i][0] - a) % p for i in win})
    ref = sites[0]
    cen = []
    for t in range(a, a + p):
        st = [events[i][1:4] for i in win if events[i][0] == t]
        if st:
            cen.append(tuple(ref[k] + sum(torus.d(ref[k], q[k]) for q in st) / len(st) for k in range(3)))
    axis = max(range(3), key=lambda k: max(c[k] for c in cen) - min(c[k] for c in cen))
    seq = [c[axis] for c in cen]
    rev2, ext, sgn = 0, seq[0], 0
    for v in seq + seq:
        if sgn == 0:
            if abs(v - seq[0]) >= 1:
                sgn, ext = (1 if v > seq[0] else -1), v
        elif (v - ext) * sgn > 0:
            ext = v
        elif abs(v - ext) >= 1:
            rev2, sgn, ext = rev2 + 1, -sgn, v
    rev = rev2 // 2
    rng = max(seq) - min(seq)
    zig = rng >= cfg["zigzag_min_extent"] and rev >= cfg["zigzag_min_reversals"]
    parts = []
    for c in _components(sites, torus, cfg["centre_gap"]):
        cs = set(c)
        ph = sorted({(events[i][0] - a) % p for i in win if events[i][1:4] in cs})
        parts.append({"sites": len(c), "centroid": [round(x, 2) for x in torus.centroid(c)], "phases": ph})
    distinct = len({tuple(x["phases"]) for x in parts})
    reason = [r for r, ok in (("parts", len(parts) >= 2 and distinct >= 2), ("internal motion", zig)) if ok]
    box = [[min(torus.d(ref[k], s[k]) for s in sites) + ref[k], max(torus.d(ref[k], s[k]) for s in sites) + ref[k]]
           for k in range(3)]
    return {"sites": [list(s) for s in sites], "n_sites": len(sites), "arm_sites_removed": arms,
            "centroid": [round(c, 2) for c in torus.centroid(sites)], "box": box,
            "extent": max(b[1] - b[0] for b in box),
            "period": p, "period_basis": src_basis, "period_channels_ignored": p0,
            "channel_period_ratio": p // p0 if p % p0 == 0 else None, "c_image": cimg,
            "jointly_periodic": jointly, "window": [a, e], "periods_observed": (e - a + 1) // p,
            "clicks_per_period": len(win), "kinds_per_period": _kinds(events, win), "phases": phases,
            "site_periods": dict(sorted(Counter(periodic[s][0] for s in sites).items())),
            "site_bases": dict(sorted(Counter(basis.get(s, "exact") for s in sites).items())),
            "traffic_clicks_removed": sum(len(excluded.get(s, ())) for s in sites),
            "parts": parts, "composite": bool(reason), "composite_reason": reason,
            "internal_motion": {"kind": "oscillating" if zig else "none", "axis": "xyz"[axis],
                                "centroid_range": round(rng, 2), "reversals_per_period": rev,
                                "turning_points": [round(min(seq), 2), round(max(seq), 2)]},
            "birth": {"t": first, "sites": [list(s) for s in bsites]}}


# ------------------------------------------------------------------ the decoder
def _summary_empty(note):
    return {"note": note, "sources": 0, "periods": [], "composites": [], "lamps": [], "tracks": {},
            "exact_speeds": [], "created": [], "c_light": None, "wrap_bound": None, "explained_fraction": None}


def decode(events, side=None, horizon=None, config=None, detectors=None, layer="native", log_info=None, c=None,
           field=None):
    """Decode click events (as from ``read_log``) into a deterministic report dict (decoder v1.1).
    ``c``: optional declared light speed (Euclidean sites/update) for the class "c-light".
    ``field``: optional declaration {"window": [t0, t1], "centre": [x, y, z], "r_range": [r0, r1]} for the
    quotient field (r24's quotient_field_v1); its summary (not the per-site sums) enters the report."""
    cfg = load_config() if config is None else config
    side_src = "declared"
    if side is None:
        side = 1 + max((max(e[1:4]) for e in events), default=0)
        side_src = "inferred lower bound (1 + largest clicked coordinate)"
    hor_src = "declared"
    if horizon is None:
        horizon, hor_src = max((e[0] for e in events), default=0), "last click update"
    if log_info and "path" in log_info:
        log_info = {"name": Path(log_info["path"]).name, **{k: v for k, v in log_info.items() if k != "path"}}
    head = {"decoder": {"name": NAME, "version": VERSION, "code_sha256": code_fingerprint(),
                        "config_version": cfg.get("version")},
            "input": {"layer": layer, "log": log_info, "side": {"value": side, "source": side_src},
                      "horizon": {"value": horizon, "source": hor_src}, "events": len(events),
                      "declared_c": c}}
    if not events:
        head.update(summary=_summary_empty("no clicks: everything on this board is dark to this layer"),
                    sources=[], tracks=[], events=[], spectra={}, kinds={"C0": 0, "C1": 0, "C2": 0},
                    arrival_map=None)
        if detectors:
            from .correlate import correlations
            head["correlations"] = correlations(events, detectors, horizon, side)
        return head
    torus, n = Torus(side), len(events)
    lo, hi = 1, horizon
    by_t, by_site = defaultdict(list), defaultdict(list)
    for i, e in enumerate(events):
        by_t[e[0]].append(i)
        by_site[e[1:4]].append(i)
    steps = sorted(by_t)
    reps = cfg["period_min_reps"]
    wrap_bound = steps[0] + side // 2

    # 1-2. clusters and tracks; (g) backdating of split-born tracks, split at velocity changes
    clusters = {}
    for t in steps:
        sites = defaultdict(list)
        for i in by_t[t]:
            sites[events[i][1:4]].append(i)
        clusters[t] = [Cluster(t, comp, torus, [i for s in comp for i in sites[s]])
                       for comp in _components(sites, torus, cfg["cluster_gap"])]
    tracks = _split_velocity(_backdate(_tracks(clusters, torus, cfg), events, torus, cfg), cfg)
    ev_track = [0] * n
    for tr in tracks:
        for o in tr.obs:
            for i in o.ev:
                ev_track[i] = tr.id
    kin = [_kinematics([(o.t, o.sites, o.ev) for o in tr.obs], torus, cfg) for tr in tracks]

    def is_mover(k):
        return k["disp"] >= cfg["mover_min_disp"] and len(k["ts"]) >= cfg["mover_min_obs"]

    # 3. periodic sites: exact (a); C-image laps (i); second test without passing traffic (h2)
    excluded, cache = {}, {}

    def site_pat(s, chan=True):
        if (s, chan) not in cache:
            p = defaultdict(list)
            ex = excluded.get(s, ())
            for i in by_site[s]:
                if i not in ex:
                    e = events[i]
                    p[e[0]].append(e[4:] if chan else e[5:])
            cache[s, chan] = {t: tuple(sorted(v)) for t, v in p.items()}
        return cache[s, chan]

    periodic, basis = {}, {}
    enough = [s for s in sorted(by_site) if len({events[i][0] for i in by_site[s]}) >= reps]
    for s in enough:
        r = _period(site_pat(s), lo, hi, cfg)
        if r:
            periodic[s] = r
    table = cfg["c_image_table"]
    for s in enough:
        if s in periodic:
            continue
        r0 = _period(site_pat(s, chan=False), lo, hi, cfg)
        if r0:
            ci = _c_image(site_pat(s), r0[0], table, 0, lo, hi, cfg)
            if ci:
                periodic[s], basis[s] = (2 * r0[0], tuple(ci["window"])), "c_image"
    traffic = {tr.id for tr in tracks if kin[tr.id]["disp"] >= cfg["traffic_min_disp"]
               and len(kin[tr.id]["ts"]) >= cfg["mover_min_obs"]}
    for s in enough:
        if s in periodic:
            continue
        rm = {i for i in by_site[s] if ev_track[i] in traffic}
        if rm and len({events[i][0] for i in by_site[s] if i not in rm}) >= reps:
            excluded[s] = rm
            cache.pop((s, True), None)
            cache.pop((s, False), None)
            r = _period(site_pat(s), lo, hi, cfg)
            if r:
                periodic[s], basis[s] = r, "traffic_removed"
            else:
                del excluded[s]
                cache.pop((s, True), None)
                cache.pop((s, False), None)

    def linked(a, b):
        (pa, sa), (pb, sb) = periodic[a], periodic[b]
        return min(sa[1], sb[1]) - max(sa[0], sb[0]) + 1 >= reps * max(pa, pb)

    regions, left, offs = [], set(periodic), _offsets(cfg["region_gap"])
    for s0 in sorted(periodic):
        if s0 not in left:
            continue
        group, stack = [s0], [s0]
        left.discard(s0)
        while stack:
            u = stack.pop()
            for o in offs:
                v = torus.shift(u, o)
                if v in left and linked(u, v):
                    left.discard(v)
                    group.append(v)
                    stack.append(v)
        regions.append(sorted(group))

    # 4. arms (v1.0 rule), the walk now stops at feeding cycles (h1)
    feeder = {s: _feeder(s, periodic, site_pat, torus) for s in periodic}
    cycle = set()
    for s in sorted(periodic):
        path, u = [], s
        seen = {}
        while u is not None and u not in seen and u not in cycle:
            seen[u] = len(path)
            path.append(u)
            u = feeder[u]
        if u is not None and u in seen:
            cycle.update(path[seen[u]:])
    feeds = {f for f in feeder.values() if f is not None}
    nonperiodic = set(by_site) - set(periodic)
    arm_sites = set()
    for s in sorted(periodic):
        if feeder[s] is None or s in feeds or s in cycle or \
                not any(torus.shift(s, o) in nonperiodic for o in _offsets(1)):
            continue
        u = s
        while u is not None and feeder[u] is not None and u not in arm_sites and u not in cycle:
            arm_sites.add(u)
            u = feeder[u]
    sources = []
    for reg in regions:
        D = _dilate(reg, torus)
        escaping = set()
        for tid in {ev_track[i] for s in reg for i in by_site[s]}:
            tr = tracks[tid]
            outside = sum(1 for o in tr.obs if not any(q in D for q in o.sites))
            if outside >= cfg["escape_min_obs"] and is_mover(kin[tid]):
                escaping.add(tid)
        core = [s for s in reg if s not in arm_sites
                and any(ev_track[i] not in escaping for i in by_site[s] if i not in excluded.get(s, ()))]
        for comp in _components(core, torus, cfg["region_gap"]):
            sources.append(_source(comp, periodic, basis, site_pat, by_site, excluded, events, torus, cfg, lo, hi,
                                   arms=len(reg) - len(core)))
    sources = [s for s in sources if s is not None]
    sources.sort(key=lambda s: (s["birth"]["t"], s["sites"][0]))

    core_d = [_dilate([tuple(x) for x in s["sites"]], torus) for s in sources]
    internal = {}
    for tr in tracks:
        for j, D in enumerate(core_d):
            if all(q in D for o in tr.obs for q in o.sites):
                internal[tr.id] = j
                break
    ev_owner = [None] * n
    for j, s in enumerate(sources):
        a, e = s["window"]
        for site in s["sites"]:
            st = tuple(site)
            for i in by_site[st]:
                if a <= events[i][0] <= e and i not in excluded.get(st, ()):
                    ev_owner[i] = ("source", j)
    for j, s in enumerate(sources):
        moves = []
        inner = sorted((t for t, k in internal.items() if k == j and kin[t]["extent"] >= cfg["mover_min_disp"]
                        and len(kin[t]["ts"]) >= cfg["mover_min_obs"]), key=lambda t: (-len(kin[t]["ts"]), t))
        for tid in inner[:cfg["internal_exact_max_tracks"]]:
            k, obs = kin[tid], tracks[tid].obs
            ex = _exact_motion(_pattern([(o.t, o.sites, o.ev) for o in obs], events), obs[0].t, obs[-1].t,
                               k["vel"], torus, cfg)
            if ex and any(ex[1]):
                m = _velocity_out(ex, k["vel"])
                m["class"] = "light" if _l1(m) >= cfg["light_min_l1_speed"] else "matter"
                m["covers_period"] = ex[2][1] - ex[2][0] + 1 >= s["period"]
                moves.append(m)
        s["internal_motion"]["exact_velocities"] = [json.loads(x) for x in
                                                    sorted({json.dumps(m, sort_keys=True) for m in moves})]
        if any(m["covers_period"] for m in moves):     # (b) a translation through a full period
            s["internal_motion"]["kind"] = "translating"
            s["composite_reason"] = [r for r in s["composite_reason"] if r != "internal motion"]
            s["composite"] = bool(s["composite_reason"])

    # 5. free tracks: co-moving merge of tracks born together (c), then exact chains of fragments (d)
    free = [tr.id for tr in tracks if tr.id not in internal]
    movers = [t for t in free if is_mover(kin[t])]
    parent_of = {t: t for t in free}

    def find(t):
        while parent_of[t] != t:
            parent_of[t] = parent_of[parent_of[t]]
            t = parent_of[t]
        return t

    for a_i, a in enumerate(movers):
        for b in movers[a_i + 1:]:
            ka, kb = kin[a], kin[b]
            if abs(tracks[a].obs[0].t - tracks[b].obs[0].t) > cfg["link_gap"]:
                continue
            if max(abs(ka["vel"][i] - kb["vel"][i]) for i in range(3)) > cfg["comove_max_dvel"]:
                continue
            ta, tb = dict(zip(ka["ts"], ka["path"])), dict(zip(kb["ts"], kb["path"]))
            common = sorted(set(ta) & set(tb))
            if len(common) < cfg["comove_min_overlap"] * min(len(ta), len(tb)):
                continue
            if all(torus.cheb(ta[t], tb[t]) <= cfg["comove_max_dist"] for t in common):
                parent_of[find(b)] = find(a)

    def build(members):
        per_t = defaultdict(lambda: ([], []))
        for tid in members:
            for o in tracks[tid].obs:
                per_t[o.t][0].extend(o.sites)
                per_t[o.t][1].extend(o.ev)
        st = [(t, sorted(set(v[0])), sorted(v[1])) for t, v in sorted(per_t.items())]
        return {"members": sorted(members), "steps": st, "kin": _kinematics(st, torus, cfg)}

    groups = defaultdict(list)
    for t in free:
        groups[find(t)].append(t)
    objects = [build(groups[r]) for r in sorted(groups, key=lambda r: (min(tracks[t].obs[0].t for t in groups[r]), r))]
    # (d) objects that touch in space-time (one starts <= link_gap + 1 updates after the other ends, close
    # by, or both overlap and stay close) and whose union is an exact co-mover over >= 80 % of its span
    link = {j: j for j in range(len(objects))}

    def root(j):
        while link[j] != j:
            link[j] = link[link[j]]
            j = link[j]
        return j

    ends = [(ob["steps"][0], ob["steps"][-1]) for ob in objects]
    at = [{t: sts for t, sts, _ in ob["steps"]} for ob in objects]
    for i in range(len(objects)):
        for j in range(len(objects)):
            if i == j:
                continue
            (fi, li), (fj, lj) = ends[i], ends[j]
            dt = fj[0] - li[0]
            if 0 < dt <= cfg["link_gap"] + 1:          # j starts just after i ends, close by
                d = _dmin(li[1], fj[1], torus, dt + cfg["cluster_gap"] + cfg["link_slack"])
                if d is not None:
                    link[root(j)] = root(i)
            elif i < j and fj[0] <= li[0] and fi[0] <= lj[0]:   # overlapping in time: close at a common update
                for t in sorted(set(at[i]) & set(at[j])):
                    if _dmin(at[i][t], at[j][t], torus, cfg["comove_max_dist"]) is not None:
                        link[root(j)] = root(i)
                        break
    chains = defaultdict(list)
    for j in range(len(objects)):
        chains[root(j)].append(j)
    merged = []
    for r in sorted(chains):
        js = chains[r]
        if len(js) > 1:
            ob = build([t for j in js for t in objects[j]["members"]])
            st, k = ob["steps"], ob["kin"]
            ex = _exact_motion(_pattern(st, events), st[0][0], st[-1][0], k["vel"], torus, cfg)
            if ex and any(ex[1]) and ex[2][1] - ex[2][0] + 1 >= cfg["chain_min_exact_fraction"] * (st[-1][0] - st[0][0] + 1):
                ob["exact"] = ex
                merged.append(ob)
                continue
        merged.extend(objects[j] for j in js)
    # (g+) a mover with no exact velocity over exact_min_coverage of its clicks, but with an exact run of
    # >= split_min_obs updates, is cut at the ends of that run (each exact segment is its own track)
    pieces = []
    for ob in merged:
        st, k = ob["steps"], ob["kin"]
        if ob.get("exact") or k["disp"] < cfg["mover_min_disp"] or len(k["ts"]) < cfg["mover_min_obs"]:
            pieces.append(ob)
            continue
        pat = _pattern(st, events)
        full = _exact_motion(pat, st[0][0], st[-1][0], k["vel"], torus, cfg)
        if full:
            ob["exact"] = full
            pieces.append(ob)
            continue
        sub = _exact_motion(pat, st[0][0], st[-1][0], k["vel"], torus, cfg, min_coverage=0.0)
        if not sub or sum(1 for x in st if sub[2][0] <= x[0] <= sub[2][1]) < cfg["split_min_obs"]:
            pieces.append(ob)
            continue
        prev = None
        for part, exact in (([x for x in st if x[0] < sub[2][0]], None),
                            ([x for x in st if sub[2][0] <= x[0] <= sub[2][1]], sub),
                            ([x for x in st if x[0] > sub[2][1]], None)):
            if part:
                new = {"members": ob["members"], "steps": part, "kin": _kinematics(part, torus, cfg), "prev": prev}
                if exact:
                    new["exact"] = exact
                pieces.append(new)
                prev = new
    objects = sorted(pieces, key=lambda ob: (ob["steps"][0][0], ob["members"][0], ob["steps"][-1][0]))
    pos = {id(ob): j for j, ob in enumerate(objects)}
    for j, ob in enumerate(objects):
        for t, _, ev in ob["steps"]:
            for i in ev:
                if ev_owner[i] is None:
                    ev_owner[i] = ("track", j)
    out_tracks = []
    tol = cfg["c_light_rel_tol"]
    for j, ob in enumerate(objects):
        k, st = ob["kin"], ob["steps"]
        mover = k["disp"] >= cfg["mover_min_disp"] and len(k["ts"]) >= cfg["mover_min_obs"]
        ex = ob.get("exact") or (_exact_motion(_pattern(st, events), st[0][0], st[-1][0], k["vel"], torus, cfg)
                                 if mover and "prev" not in ob else None)
        motion = _velocity_out(ex if ex and any(ex[1]) else None, k["vel"])
        if k["slope"] >= cfg["front_slope"]:
            cls = "front"
        elif mover and c and abs(motion["euclid_speed"] - c) <= tol * c:
            cls = "c-light"
        elif mover:
            cls = "light" if _l1(motion) >= cfg["light_min_l1_speed"] else "matter"
        elif st[-1][0] - st[0][0] >= cfg["local_min_duration"]:
            cls = "local"
        else:
            cls = "transient"
        own = [i for _, _, ev in st for i in ev if ev_owner[i] == ("track", j)]
        out_tracks.append({"id": f"T{j}", "class": cls, "t_start": st[0][0], "t_end": st[-1][0],
                           "observations": len(st), "start": list(torus.wrap(k["path"][0])),
                           "end": list(torus.wrap(k["path"][-1])), "motion": motion,
                           "direction": _direction(k["vel"]), "net_displacement": round(k["disp"], 2),
                           "extent": round(k["extent"], 2),
                           "front": {"radius_slope": round(k["slope"], 4), "radius_first": k["radius"][:12]},
                           "clicks": len(own), "kinds": _kinds(events, own),
                           "path": [[t] + [round(x, 2) for x in p] for t, p in zip(k["ts"], k["path"])],
                           "_members": ob["members"], "_birth_sites": st[0][1],
                           "_prev": pos[id(ob["prev"])] if ob.get("prev") is not None else None})

    # 6. births (as v1.0)
    seed_steps = steps[:cfg["seed_steps"]]
    seed_sites = {events[i][1:4] for t in seed_steps for i in by_t[t]}
    track_obj = {tid: j for j, ob in enumerate(objects) for tid in ob["members"]}

    def label(owner):
        return None if owner is None else (f"S{owner[1]}" if owner[0] == "source" else f"T{owner[1]}")

    def birth(t_b, sites, own_test, split_parent=None):
        out = {"t": t_b, "sites": [list(s) for s in sites[:8]], "centroid": [round(x, 2) for x in torus.centroid(sites)]}
        if t_b in seed_steps:
            out.update(origin="seed", parent=None)
        else:
            best, sset = None, set(sites)
            for dt in range(1, cfg["emit_lookback"] + 1):
                r = cfg["emit_radius"] + dt
                ring = sorted(product(range(-r, r + 1), repeat=3), key=lambda o: max(map(abs, o)))
                for i in by_t.get(t_b - dt, ()):
                    if own_test(i):
                        continue
                    q = events[i][1:4]
                    if len(sites) <= len(ring):
                        d = min(torus.cheb(q, s) for s in sites)
                    else:
                        d = next((max(map(abs, o)) for o in ring if torus.shift(q, o) in sset), r + 1)
                    if d <= r and (best is None or (d, dt) < best[:2]):
                        best = (d, dt, i)
            if split_parent is not None:
                out.update(origin="emitted", parent=split_parent, rule="split from a linked track")
            elif best:
                own = ev_owner[best[2]]
                if own is None:
                    tid = ev_track[best[2]]
                    own = ("source", internal[tid]) if tid in internal else ("track", track_obj.get(tid))
                out.update(origin="emitted", parent=label(own),
                           rule=f"earlier click at distance {best[0]}, {best[1]} update(s) before")
            else:
                out.update(origin="isolated", parent=None, rule="no earlier click in the causal neighbourhood")
        out["after_wrap_bound"] = t_b >= wrap_bound
        out["seed_distance"] = _capped_distance(sites, seed_sites, torus, cfg["create_radius"] + 1)
        out["created"] = bool(t_b not in seed_steps and t_b > seed_steps[-1]
                              and out["seed_distance"] > cfg["create_radius"])
        return out

    for j, s in enumerate(sources):
        s["id"] = f"S{j}"
        b = s["birth"]
        s["birth"] = birth(b["t"], [tuple(x) for x in b["sites"]], lambda i, j=j: ev_owner[i] == ("source", j))
    for j, tr in enumerate(out_tracks):
        first = tracks[min(tr["_members"], key=lambda t: (tracks[t].obs[0].t, t))]
        sp = None
        prev = tr.pop("_prev")
        if prev is not None:
            sp = f"T{prev}"
        elif first.parent is not None and first.parent not in tr["_members"]:
            p = first.parent
            sp = f"S{internal[p]}" if p in internal else (f"T{track_obj[p]}" if p in track_obj else None)
        tr["birth"] = birth(tr["t_start"], tr.pop("_birth_sites"), lambda i, j=j: ev_owner[i] == ("track", j), sp)
        tr["members"] = len(tr.pop("_members"))
    for s in sources:      # (k) emitted: born next to the core after the source's birth, and it leaves
        core = [tuple(x) for x in s["sites"]]
        em = [t["id"] for t in out_tracks if t["class"] in ("light", "matter", "front", "c-light")
              and t["birth"]["origin"] != "seed" and t["t_start"] >= s["birth"]["t"]
              and min(torus.cheb(tuple(q), x) for q in t["birth"]["sites"] for x in core) <= cfg["lamp_birth_radius"]
              and min(torus.cheb(tuple(t["end"]), x) for x in core) >= cfg["lamp_min_travel"]]
        s["emitted_tracks"] = em
        s["lamp"] = len(em) >= cfg["lamp_min_emitted"]
    ev_list = []
    for o in sources + out_tracks:
        b = o["birth"]
        if b["origin"] == "emitted":
            ev_list.append({"type": "emission", "t": b["t"], "object": o["id"], "parent": b["parent"],
                            "at": b["centroid"]})
        if b["created"]:
            ev_list.append({"type": "creation", "t": b["t"], "object": o["id"], "origin": b["origin"],
                            "at": b["centroid"], "seed_distance": b["seed_distance"],
                            "after_wrap_bound": b["after_wrap_bound"]})
    ev_list.sort(key=lambda e: (e["t"], e["type"], e["object"]))

    # 7. spectra, kinds, arrival map, c-light consistency
    intervals = Counter()
    for s, idx in by_site.items():
        ts = sorted({events[i][0] for i in idx})
        intervals.update(b - a for a, b in zip(ts, ts[1:]))
    glob = defaultdict(list)
    for e in events:
        glob[e[0]].append(e[1:])
    gp = _period({t: tuple(v) for t, v in glob.items()}, lo, hi, cfg)
    explained = sum(1 for i in range(n) if ev_owner[i] is not None and
                    (ev_owner[i][0] == "source" or out_tracks[ev_owner[i][1]]["class"] != "transient"))
    amap = _arrival_map(events, torus, cfg, wrap_bound)
    c_light = None
    if c:
        cl = [t for t in out_tracks if t["class"] == "c-light"]
        dirs = []
        for t in cl:
            u = (t["direction"] or {}).get("unit")
            if u and all(max(abs(u[i] - w[i]) for i in range(3)) > 0.1 for w in dirs):
                dirs.append(u)
        arr = {k: v["speed"] for k, v in amap.get("directions", {}).items() if v and v.get("speed")}
        ok = [abs(v - c) <= tol * c for v in arr.values()]
        c_light = {"c": c, "tolerance": tol, "tracks": [t["id"] for t in cl],
                   "track_speeds": [t["motion"]["euclid_speed"] for t in cl], "track_directions": dirs,
                   "arrival_direction_speeds": arr,
                   "consistent_across_directions": (all(ok) and bool(cl)) if len(dirs) + len(arr) >= 2 else None}
    report = dict(head)
    report["summary"] = {
        "sources": len(sources), "periods": [s["period"] for s in sources],
        "composites": [s["id"] for s in sources if s["composite"]], "lamps": [s["id"] for s in sources if s["lamp"]],
        "c_image_sources": [s["id"] for s in sources if s["c_image"]],
        "tracks": dict(sorted(Counter(t["class"] for t in out_tracks).items())),
        "exact_speeds": sorted({t["motion"]["l1_speed"] for t in out_tracks if t["motion"]["exact"]}),
        "created": [e["object"] for e in ev_list if e["type"] == "creation"],
        "c_light": c_light, "wrap_bound": wrap_bound, "explained_fraction": round(explained / n, 4)}
    report["sources"] = sources
    report["tracks"] = out_tracks
    report["events"] = ev_list
    report["spectra"] = {"source_periods": dict(sorted(Counter(s["period"] for s in sources).items())),
                         "site_intervals": dict(sorted(intervals.items())),
                         "global_period": ({"period": gp[0], "window": list(gp[1])} if gp else None)}
    report["kinds"] = _kinds(events, range(n))
    report["arrival_map"] = amap
    if field:
        from .layers import quotient_field
        qf = quotient_field(events, side, field.get("window"), field.get("centre"), field.get("r_range"))
        qf.pop("sum")
        report["quotient_field"] = qf
    if detectors:
        from .correlate import _member, correlations
        report["correlations"] = correlations(events, detectors, horizon, side)
        # (l) passages: each free track's first and last click inside each declared detector region
        pas = {}
        for name, det in sorted(detectors["detectors"].items()):
            inside = _member(det, side)
            rows = []
            for j, ob in enumerate(objects):
                ts = [events[i][0] for _, _, ev in ob["steps"] for i in ev if inside(events[i])]
                if ts:
                    rows.append({"track": f"T{j}", "class": out_tracks[j]["class"], "first": min(ts), "last": max(ts),
                                 "clicks": len(ts)})
            pas[name] = rows
        report["passages"] = pas
    return report
