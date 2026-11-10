"""Generic click decoder v1: objects, periods, speeds and births read only from a click log.

Input: the official ``python -m universe24 --events`` JSONL, or a read-only observer log
in the same record form. From each record only ``step``, ``address``, ``kind`` and
``quotient`` are kept; ``before``/``after`` are state values and are dropped at load
time. The board side and the horizon are declared by the caller. Every threshold is in
``config_v1.json``; nothing is tuned per experiment. Standard library only.

Pipeline (each stage uses only the events and the earlier stages):
  1. per-update clusters of clicked sites (Chebyshev gap ``cluster_gap``);
  2. tracks: clusters linked over updates (causal distance, predicted position);
  3. periodic sites: the longest exact run of a site's click pattern with period p;
  4. sources: connected periodic sites minus the "arms" that only escaping tracks use;
  5. free tracks: co-moving tracks merged, exact co-moving symmetry (T, v) or a fit;
  6. births: seed / emitted (earlier clicks in the causal neighbourhood) / isolated,
     and ``created`` (born after the seed updates, away from the seed footprint);
  7. spectra, kind statistics, optional detector correlations.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from itertools import product
import hashlib
import json
import math
from pathlib import Path

NAME = "click_decoder_v1"
VERSION = "1.0"
HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config_v1.json"
READ = ("step", "address", "kind", "quotient")
SOURCES = ("decoder.py", "correlate.py", "config_v1.json")


# ------------------------------------------------------------------ input
def read_log(path):
    """(events, info). events: sorted tuples (t, x, y, z, g, kind, quotient); nothing else is kept."""
    raw = Path(path).read_bytes()
    events, ignored = [], set()
    for line in raw.decode("utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            x, y, z, g = d["address"]
            events.append((int(d["step"]), int(x), int(y), int(z), int(g), int(d["kind"]), int(d["quotient"])))
            ignored.update(k for k in d if k not in READ)
    events.sort()
    return events, {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "events": len(events),
                    "fields_read": list(READ), "fields_ignored": sorted(ignored)}


def load_config(path=None) -> dict:
    return json.loads(Path(path or CONFIG).read_text(encoding="utf-8"))


def code_fingerprint() -> dict:
    return {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in SOURCES}


# ------------------------------------------------------------------ torus geometry
class Torus:
    def __init__(self, side: int):
        self.L = side

    def d(self, a, b):
        """Signed minimal image of b - a (works for floats)."""
        L = self.L
        return (b - a + L / 2) % L - L / 2

    def cheb(self, p, q):
        return max(abs(self.d(p[i], q[i])) for i in range(3))

    def wrap(self, p):
        return tuple(int(round(c)) % self.L for c in p)

    def shift(self, s, v):
        L = self.L
        return ((s[0] + v[0]) % L, (s[1] + v[1]) % L, (s[2] + v[2]) % L)

    def centroid(self, sites):
        ref = sites[0]
        return tuple(ref[i] + sum(self.d(ref[i], s[i]) for s in sites) / len(sites) for i in range(3))

    def unwrap(self, prev, c):
        return tuple(prev[i] + self.d(prev[i], c[i]) for i in range(3))


def _offsets(gap):
    r = range(-gap, gap + 1)
    return [o for o in product(r, r, r) if o != (0, 0, 0)]


def _components(sites, torus, gap):
    """Connected components (Chebyshev <= gap, periodic) of a set of sites; sorted."""
    present, seen, out, offs, L = set(sites), set(), [], _offsets(gap), torus.L
    for s in sorted(present):
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for dx, dy, dz in offs:
                v = ((u[0] + dx) % L, (u[1] + dy) % L, (u[2] + dz) % L)
                if v in present and v not in seen:
                    seen.add(v)
                    stack.append(v)
        out.append(sorted(comp))
    return out


def _dilate(sites, torus, r=1):
    offs = _offsets(r) + [(0, 0, 0)]
    return {torus.shift(s, o) for s in sites for o in offs}


# ------------------------------------------------------------------ exact periodic runs
def _longest_run(times, same, lo, hi, p):
    """Longest run [a, b] of consecutive t in [lo, hi - p] with same(t); same(t) may fail only
    when t or t + p is in ``times``. The periodic segment is then [a, b + p]."""
    bad = sorted({u for s in times for u in (s, s - p) if lo <= u <= hi - p and not same(u)})
    best, prev = None, lo - 1
    for b in bad + [hi - p + 1]:
        if b - 1 >= prev + 1 and (best is None or b - 1 - (prev + 1) > best[1] - best[0]):
            best = (prev + 1, b - 1)
        prev = b
    return best


def _accept(run, p, times, reps):
    if run is None:
        return None
    a, e = run[0], run[1] + p
    if e - a + 1 < reps * p or sum(1 for t in times if a <= t <= e) < reps:
        return None
    return a, e


def _period(pat, lo, hi, cfg, pmax=None):
    """Smallest p with an exact p-periodic segment covering >= period_min_reps periods."""
    reps = cfg["period_min_reps"]
    times = sorted(pat)
    if len(times) < reps:
        return None
    for p in range(1, min(pmax or cfg["period_max"], (hi - lo + 1) // reps) + 1):
        seg = _accept(_longest_run(times, lambda t: pat.get(t) == pat.get(t + p), lo, hi, p), p, times, reps)
        if seg:
            return p, seg
    return None


def _lcm(values):
    return reduce(lambda a, b: a * b // math.gcd(a, b), values, 1)


# ------------------------------------------------------------------ stage 1-2: clusters and tracks
class Cluster:
    __slots__ = ("t", "sites", "c", "r", "ev")

    def __init__(self, t, sites, torus, ev):
        self.t, self.sites, self.ev = t, sites, ev
        self.c = torus.centroid(sites)
        ref = torus.wrap(self.c)
        self.r = max(torus.cheb(s, ref) for s in sites)


class Track:
    __slots__ = ("id", "obs", "path", "parent")

    def __init__(self, i, cl, parent):
        self.id, self.obs, self.path, self.parent = i, [cl], [cl.c], parent


def _dmin(a, b, torus, limit):
    """Smallest Chebyshev distance between two site lists if <= limit, else None."""
    best = None
    for s in a:
        for q in b:
            d = torus.cheb(s, q)
            if d <= limit and (best is None or d < best):
                best = d
                if d == 0:
                    return 0
    return best


def _slow(tr, cfg):
    if len(tr.obs) < cfg["slow_min_obs"]:
        return False
    dt = tr.obs[-1].t - tr.obs[0].t
    disp = max(abs(tr.path[-1][i] - tr.path[0][i]) for i in range(3))
    return dt > 0 and disp / dt < cfg["slow_max_speed"]


def _predict(tr, t):
    pts, ts = tr.path[-6:], [o.t for o in tr.obs[-6:]]
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
            pred = _predict(tr, t)
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


# ------------------------------------------------------------------ kinematics
def _fit(ts, path):
    if len(ts) < 2 or ts[-1] == ts[0]:
        return (0.0, 0.0, 0.0)
    mt = sum(ts) / len(ts)
    den = sum((t - mt) ** 2 for t in ts)
    return tuple(sum((ts[k] - mt) * path[k][i] for k in range(len(ts))) / den for i in range(3))


def _kinematics(steps, torus, cfg):
    """steps: sorted list of (t, sites, events). Path of unwrapped centroids, fitted velocity, front test."""
    ts = [s[0] for s in steps]
    cents = [torus.centroid(s[1]) for s in steps]
    path = [cents[0]]
    for c in cents[1:]:
        path.append(torus.unwrap(path[-1], c))
    vel = _fit(ts, path)
    disp = max(abs(path[-1][i] - path[0][i]) for i in range(3))
    ext = max(max(abs(p[i] - path[0][i]) for i in range(3)) for p in path)
    # spread of each observation about its own centroid: a front is a footprint that keeps growing
    rad = [max(torus.cheb(q, c) for q in s[1]) for s, c in zip(steps, cents)]
    m = min(len(ts), cfg["front_window"])
    slope = _fit(ts[:m], [(r, 0, 0) for r in rad[:m]])[0] if m >= 4 else 0.0
    return {"ts": ts, "path": path, "vel": vel, "disp": disp, "extent": ext, "radius": rad, "slope": slope}


def _pattern(steps, events):
    """t -> sorted tuple of (x, y, z, kind, quotient): the channel index g is left out because
    prepared guides relabel channels along a path (the 2O gauge), which a translation cannot follow."""
    return {t: tuple(sorted(events[i][1:4] + events[i][5:] for i in ev)) for t, _, ev in steps}


def _exact_motion(pat, t0, t1, vel, torus, cfg):
    """Smallest (T, v), |v|_1 <= T, with pattern(t + T) == pattern(t) shifted by v on >= reps periods."""
    if not pat or max(len(p) for p in pat.values()) > cfg["exact_max_events_per_step"]:
        return None
    reps = cfg["period_min_reps"]
    times = sorted(pat)
    lab = {t: tuple(sorted(Counter(e[3:] for e in p).items())) for t, p in pat.items()}
    for T in range(1, min(cfg["track_period_max"], (t1 - t0 + 1) // reps) + 1):
        if not _accept(_longest_run(times, lambda t: lab.get(t) == lab.get(t + T), t0, t1, T), T, times, reps):
            continue
        base = [round(vel[i] * T) for i in range(3)]
        cands = {(base[0] + a, base[1] + b, base[2] + c) for a, b, c in product((-1, 0, 1), repeat=3)}
        cands = sorted((v for v in cands if sum(map(abs, v)) <= T),
                       key=lambda v: (sum((v[i] - vel[i] * T) ** 2 for i in range(3)), v))
        for v in cands:
            def same(t, v=v):
                a, b = pat.get(t, ()), pat.get(t + T, ())
                return len(a) == len(b) and tuple(sorted(torus.shift(e[:3], v) + e[3:] for e in a)) == b
            seg = _accept(_longest_run(times, same, t0, t1, T), T, times, reps)
            if seg:
                return T, v, seg
    return None


def _velocity_out(exact, vel):
    if exact:
        T, v, seg = exact
        fr = [Fraction(v[i], T) for i in range(3)]
        return {"exact": True, "T": T, "shift": list(v), "velocity": [str(f) for f in fr],
                "l1_speed": str(sum(abs(f) for f in fr)), "max_speed": str(max(abs(f) for f in fr)),
                "euclid_speed": round(math.sqrt(sum(float(f) ** 2 for f in fr)), 4), "window": list(seg)}
    return {"exact": False, "velocity": [round(x, 4) for x in vel], "l1_speed": round(sum(map(abs, vel)), 4),
            "max_speed": round(max(map(abs, vel)), 4), "euclid_speed": round(math.sqrt(sum(x * x for x in vel)), 4)}


def _l1(motion):
    return float(Fraction(motion["l1_speed"])) if motion["exact"] else motion["l1_speed"]


def _direction(vel):
    n = math.sqrt(sum(x * x for x in vel))
    if n == 0:
        return None
    k = max(range(3), key=lambda i: abs(vel[i]))
    return {"unit": [round(x / n, 4) for x in vel], "main_axis": ("+" if vel[k] > 0 else "-") + "xyz"[k]}


def _kinds(events, idx):
    c = Counter(events[i][5] for i in idx)
    return {f"C{k}": c.get(k, 0) for k in range(3)}


# ------------------------------------------------------------------ the decoder
def decode(events, side=None, horizon=None, config=None, detectors=None, layer="native", log_info=None):
    """Decode a list of click events (as from ``read_log``) into a deterministic report dict."""
    cfg = load_config() if config is None else config
    side_src = "declared"
    if side is None:
        side = 1 + max((max(e[1:4]) for e in events), default=0)
        side_src = "inferred lower bound (1 + largest clicked coordinate)"
    t_last = max((e[0] for e in events), default=0)
    hor_src = "declared"
    if horizon is None:
        horizon, hor_src = t_last, "last click update"
    head = {"decoder": {"name": NAME, "version": VERSION, "code_sha256": code_fingerprint(),
                        "config_version": cfg.get("version")},
            "input": {"layer": layer, "log": log_info, "side": {"value": side, "source": side_src},
                      "horizon": {"value": horizon, "source": hor_src}, "events": len(events)}}
    if not events:
        head["summary"] = {"note": "no clicks: everything on this board is dark to this layer",
                           "sources": 0, "tracks": 0}
        head.update(sources=[], tracks=[], events=[], spectra={}, kinds={"C0": 0, "C1": 0, "C2": 0})
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

    # 1-2. clusters and tracks
    clusters = {}
    for t in steps:
        sites = defaultdict(list)
        for i in by_t[t]:
            sites[events[i][1:4]].append(i)
        clusters[t] = [Cluster(t, comp, torus, [i for s in comp for i in sites[s]])
                       for comp in _components(sites, torus, cfg["cluster_gap"])]
    tracks = _tracks(clusters, torus, cfg)
    ev_track = [0] * n
    for tr in tracks:
        for o in tr.obs:
            for i in o.ev:
                ev_track[i] = tr.id
    kin = [_kinematics([(o.t, o.sites, o.ev) for o in tr.obs], torus, cfg) for tr in tracks]

    def is_mover(k):
        return k["disp"] >= cfg["mover_min_disp"] and len(k["ts"]) >= cfg["mover_min_obs"]

    # 3. periodic sites (full labels, and without channel index)
    pat_cache = {}

    def site_pat(s, chan=True):
        if (s, chan) not in pat_cache:
            p = defaultdict(list)
            for i in by_site[s]:
                e = events[i]
                p[e[0]].append(e[4:] if chan else e[5:])
            pat_cache[s, chan] = {t: tuple(sorted(v)) for t, v in p.items()}
        return pat_cache[s, chan]

    periodic = {}
    for s in sorted(by_site):
        if len({events[i][0] for i in by_site[s]}) >= cfg["period_min_reps"]:
            r = _period(site_pat(s), lo, hi, cfg)
            if r:
                periodic[s] = r
    reps = cfg["period_min_reps"]

    def linked(a, b):
        (pa, sa), (pb, sb) = periodic[a], periodic[b]
        return min(sa[1], sb[1]) - max(sa[0], sb[0]) + 1 >= reps * max(pa, pb)

    # regions: periodic sites within region_gap whose periodic segments overlap by >= reps periods
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

    # 4. arms. A periodic site is "fed" by a periodic neighbour when its channel-free pattern on its
    # periodic segment is that neighbour's pattern delayed by tau (|offset|_1 <= tau < period): a
    # train passing through. An arm is a feeding chain whose last site touches clicked sites that are
    # not periodic (the train leaves the periodic region); walking back from that end to the first
    # unfed site gives the arm. Chains that close inside the region (circulation) stay in the core.
    # Sites whose every click belongs to tracks that leave the region are arms as well.
    feeder = {s: _feeder(s, periodic, site_pat, torus) for s in periodic}
    feeds = {f for f in feeder.values() if f is not None}
    nonperiodic = set(by_site) - set(periodic)
    arm_sites = set()
    for s in sorted(periodic):
        if feeder[s] is None or s in feeds or not any(torus.shift(s, o) in nonperiodic for o in _offsets(1)):
            continue
        u = s
        while u is not None and feeder[u] is not None and u not in arm_sites:
            arm_sites.add(u)
            u = feeder[u]

    sources = []
    for reg in regions:
        R = set(reg)
        D = _dilate(reg, torus)
        escaping = set()
        for tid in {ev_track[i] for s in reg for i in by_site[s]}:
            tr = tracks[tid]
            outside = sum(1 for o in tr.obs if not any(q in D for q in o.sites))
            if outside >= cfg["escape_min_obs"] and is_mover(kin[tid]):
                escaping.add(tid)
        core = [s for s in reg if s not in arm_sites and any(ev_track[i] not in escaping for i in by_site[s])]
        for comp in _components(core, torus, cfg["region_gap"]):
            sources.append(_source(comp, periodic, by_site, events, torus, cfg, lo, hi, site_pat,
                                   arms=len(R) - len(core)))
    sources = [s for s in sources if s is not None]
    sources.sort(key=lambda s: (s["birth"]["t"], s["sites"][0]))

    # internal tracks: every observation inside a source core (dilated by one site)
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
            for i in by_site[tuple(site)]:
                if a <= events[i][0] <= e:
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
                moves.append(m)
        s["internal_motion"]["exact_velocities"] = [json.loads(m) for m in
                                                    sorted({json.dumps(m, sort_keys=True) for m in moves})]
        if moves:      # a mover that wraps the torus inside its periodic region: not an oscillation
            s["internal_motion"]["kind"] = "translating"
            s["composite_reason"] = [r for r in s["composite_reason"] if r != "internal motion"]
            s["composite"] = bool(s["composite_reason"])

    # 5. free tracks, co-moving groups
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
            if max(abs(ka["vel"][i] - kb["vel"][i]) for i in range(3)) > cfg["comove_max_dvel"]:
                continue
            ta, tb = dict(zip(ka["ts"], ka["path"])), dict(zip(kb["ts"], kb["path"]))
            common = sorted(set(ta) & set(tb))
            short = min(len(ta), len(tb))
            if len(common) < cfg["comove_min_overlap"] * short:
                continue
            if all(torus.cheb(ta[t], tb[t]) <= cfg["comove_max_dist"] for t in common):
                parent_of[find(b)] = find(a)
    groups = defaultdict(list)
    for t in free:
        groups[find(t)].append(t)
    objects = []
    for root in sorted(groups, key=lambda r: (min(tracks[t].obs[0].t for t in groups[r]), r)):
        members = sorted(groups[root])
        per_t = defaultdict(lambda: ([], []))
        for tid in members:
            for o in tracks[tid].obs:
                per_t[o.t][0].extend(o.sites)
                per_t[o.t][1].extend(o.ev)
        st = [(t, sorted(set(v[0])), sorted(v[1])) for t, v in sorted(per_t.items())]
        k = _kinematics(st, torus, cfg)
        objects.append({"members": members, "steps": st, "kin": k})
    for j, ob in enumerate(objects):
        for t, _, ev in ob["steps"]:
            for i in ev:
                if ev_owner[i] is None:
                    ev_owner[i] = ("track", j)
    out_tracks = []
    for j, ob in enumerate(objects):
        k, st = ob["kin"], ob["steps"]
        mover = k["disp"] >= cfg["mover_min_disp"] and len(k["ts"]) >= cfg["mover_min_obs"]
        ex = _exact_motion(_pattern(st, events), st[0][0], st[-1][0], k["vel"], torus, cfg) if mover else None
        motion = _velocity_out(ex if ex and any(ex[1]) else None, k["vel"])
        front = k["slope"] >= cfg["front_slope"]
        if front:
            cls = "front"
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
                           "path": [[t] + [round(c, 2) for c in p] for t, p in zip(k["ts"], k["path"])],
                           "_members": ob["members"], "_birth_sites": st[0][1]})

    # 6. births: seed / emitted / isolated; created (UPDATE 6, positional)
    seed_steps = steps[:cfg["seed_steps"]]
    # causal wrap bound: no click signal can have crossed half the torus before this update
    wrap_bound = steps[0] + side // 2
    seed_sites = {events[i][1:4] for t in seed_steps for i in by_t[t]}
    track_obj = {}
    for j, ob in enumerate(objects):
        for tid in ob["members"]:
            track_obj[tid] = j

    def label(owner):
        if owner is None:
            return None
        return (f"S{owner[1]}" if owner[0] == "source" else f"T{owner[1]}")

    def birth(t_b, sites, own_test, split_parent=None):
        out = {"t": t_b, "sites": [list(s) for s in sites[:8]], "centroid": [round(c, 2) for c in torus.centroid(sites)]}
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
        dseed = _capped_distance(sites, seed_sites, torus, cfg["create_radius"] + 1)
        out["seed_distance"] = dseed
        out["created"] = bool(t_b not in seed_steps and t_b > seed_steps[-1] and dseed is not None
                              and dseed > cfg["create_radius"])
        return out

    for j, s in enumerate(sources):
        s["id"] = f"S{j}"
        b = s["birth"]
        s["birth"] = birth(b["t"], [tuple(x) for x in b["sites"]], lambda i, j=j: ev_owner[i] == ("source", j))
    for j, tr in enumerate(out_tracks):
        first = tracks[min(tr["_members"], key=lambda t: (tracks[t].obs[0].t, t))]
        sp = None
        if first.parent is not None and first.parent not in tr["_members"]:
            p = first.parent
            sp = f"S{internal[p]}" if p in internal else f"T{track_obj[p]}"
        tr["birth"] = birth(tr["t_start"], tr.pop("_birth_sites"), lambda i, j=j: ev_owner[i] == ("track", j), sp)
        tr["members"] = len(tr.pop("_members"))
    for s in sources:      # emitted: a mover born after the source, next to its core
        core = [tuple(x) for x in s["sites"]]
        em = [t["id"] for t in out_tracks if t["class"] in ("light", "matter", "front")
              and t["birth"]["origin"] != "seed" and t["t_start"] >= s["birth"]["t"]
              and min(torus.cheb(tuple(q), c) for q in t["birth"]["sites"] for c in core) <= cfg["lamp_birth_radius"]]
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

    # 7. spectra and statistics
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
    report = dict(head)
    report["summary"] = {
        "sources": len(sources), "periods": [s["period"] for s in sources],
        "composites": [s["id"] for s in sources if s["composite"]], "lamps": [s["id"] for s in sources if s["lamp"]],
        "tracks": Counter(t["class"] for t in out_tracks),
        "exact_speeds": sorted({t["motion"]["l1_speed"] for t in out_tracks if t["motion"]["exact"]}),
        "created": [e["object"] for e in ev_list if e["type"] == "creation"],
        "wrap_bound": wrap_bound,
        "explained_fraction": round(explained / n, 4)}
    report["sources"] = sources
    report["tracks"] = out_tracks
    report["events"] = ev_list
    report["spectra"] = {"source_periods": dict(sorted(Counter(s["period"] for s in sources).items())),
                         "site_intervals": dict(sorted(intervals.items())),
                         "global_period": ({"period": gp[0], "window": list(gp[1])} if gp else None)}
    report["kinds"] = _kinds(events, range(n))
    if detectors:
        from .correlate import correlations
        report["correlations"] = correlations(events, detectors, horizon, side)
    return report


def _capped_distance(sites, others, torus, cap):
    """min(cap, smallest Chebyshev distance between two site collections); cap means 'at least cap'."""
    if len(others) <= (2 * cap + 1) ** 3:
        return min([cap] + [torus.cheb(s, q) for s in sites for q in others])
    ring = sorted(product(range(-cap + 1, cap), repeat=3), key=lambda o: max(map(abs, o)))
    return min([cap] + [next((max(map(abs, o)) for o in ring if torus.shift(s, o) in others), cap) for s in sites])


def _feeder(s, periodic, site_pat, torus):
    """The neighbour whose channel-free pattern, delayed by the smallest tau, equals this site's
    pattern on its periodic segment (None if there is none)."""
    p, (a, e) = periodic[s]
    mine = {t: v for t, v in site_pat(s, chan=False).items() if a <= t <= e}
    t0 = min(mine)
    best = None
    for o in _offsets(1):
        n = torus.shift(s, o)
        if n not in periodic or periodic[n][0] != p:
            continue
        other = site_pat(n, chan=False)
        # a delay tau must map one of the neighbour's clicks onto this site's first click
        taus = sorted(t0 - t for t in other if max(1, sum(map(abs, o))) <= t0 - t < p)
        for tau in taus:
            if best is not None and tau >= best[0]:
                break
            if other.get(t0 - tau) == mine[t0] and len(mine) == sum(1 for t in other if a <= t + tau <= e) \
                    and all(other.get(t - tau) == v for t, v in mine.items()):
                best = (tau, n)
                break
    return best[1] if best else None


def _source(comp, periodic, by_site, events, torus, cfg, lo, hi, site_pat, arms):
    """Periodic source from a connected set of periodic core sites."""
    sites = sorted(comp)
    p = _lcm(periodic[s][0] for s in sites)
    joint = defaultdict(list)
    for s in sites:
        for i in by_site[s]:
            e = events[i]
            joint[e[0]].append((s, *e[4:]))
    jp = {t: tuple(sorted(v)) for t, v in joint.items()}
    jointly = True
    if p > cfg["period_max"]:
        return None
    times = sorted(jp)
    seg = _accept(_longest_run(times, lambda t: jp.get(t) == jp.get(t + p), lo, hi, p), p, times,
                  cfg["period_min_reps"])
    if seg is None:
        jointly = False
        seg = (max(periodic[s][1][0] for s in sites), min(periodic[s][1][1] for s in sites))
        if seg[1] - seg[0] + 1 < p:
            return None
    a, e = seg
    # channel-free period (site, kind, quotient): a 360-degree image differs only in the channel index g
    p0s = []
    for s in sites:
        r = _period(site_pat(s, chan=False), lo, hi, cfg, pmax=p)
        p0s.append(r[0] if r else p)
    p0 = _lcm(p0s)
    win = [i for s in sites for i in by_site[s] if a <= events[i][0] < a + p]
    first = min(events[i][0] for s in sites for i in by_site[s]
                if periodic[s][1][0] <= events[i][0] <= periodic[s][1][1])
    bsites = sorted({events[i][1:4] for s in sites for i in by_site[s] if events[i][0] == first})
    phases = sorted({(events[i][0] - a) % p for i in win})
    # internal structure over one period
    ref = sites[0]
    cen = []
    for t in range(a, a + p):
        st = [events[i][1:4] for i in win if events[i][0] == t]
        if st:
            cen.append(tuple(ref[k] + sum(torus.d(ref[k], q[k]) for q in st) / len(st) for k in range(3)))
    axis = max(range(3), key=lambda k: max(c[k] for c in cen) - min(c[k] for c in cen))
    seq = [c[axis] for c in cen]
    # reversals: the centroid retreats >= 1 site from its running extreme (counted over two cycles, halved)
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
    rng = max(c[axis] for c in cen) - min(c[axis] for c in cen)
    zig = rng >= cfg["zigzag_min_extent"] and rev >= cfg["zigzag_min_reversals"]
    parts = []
    for c in _components(sites, torus, cfg["centre_gap"]):
        cs = set(c)
        ph = sorted({(events[i][0] - a) % p for i in win if events[i][1:4] in cs})
        parts.append({"sites": len(c), "centroid": [round(x, 2) for x in torus.centroid(c)], "phases": ph})
    distinct = len({tuple(x["phases"]) for x in parts})
    composite = (len(parts) >= 2 and distinct >= 2) or zig
    reason = [r for r, ok in (("parts", len(parts) >= 2 and distinct >= 2), ("internal motion", zig)) if ok]
    box = [[min(torus.d(ref[k], s[k]) for s in sites) + ref[k], max(torus.d(ref[k], s[k]) for s in sites) + ref[k]]
           for k in range(3)]
    return {"sites": [list(s) for s in sites], "n_sites": len(sites), "arm_sites_removed": arms,
            "centroid": [round(c, 2) for c in torus.centroid(sites)], "box": box,
            "extent": max(b[1] - b[0] for b in box),
            "period": p, "period_channels_ignored": p0, "channel_period_ratio": p // p0 if p % p0 == 0 else None,
            "jointly_periodic": jointly, "window": [a, e], "periods_observed": (e - a + 1) // p,
            "clicks_per_period": len(win), "kinds_per_period": _kinds(events, win), "phases": phases,
            "site_periods": dict(sorted(Counter(periodic[s][0] for s in sites).items())),
            "parts": parts, "composite": composite, "composite_reason": reason,
            "internal_motion": {"kind": "oscillating" if zig else "none", "axis": "xyz"[axis],
                                "centroid_range": round(rng, 2), "reversals_per_period": rev,
                                "turning_points": [round(min(seq), 2), round(max(seq), 2)]},
            "birth": {"t": first, "sites": [list(s) for s in bsites]}}
