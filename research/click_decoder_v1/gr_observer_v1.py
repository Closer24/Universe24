"""r64 GR-O: the geometry an inhabitant measures, read from the official click log only.

A declared, read-only observer (AGENTS rule 10).  ``observe(log, declaration)`` is a pure function of

* the official click log (``python -m universe24 --events`` JSONL, or the same records as an iterable):
  only ``step``, ``address`` = (x, y, z, g), ``kind`` and ``quotient`` are kept; ``before``/``after`` are state
  values, dropped while loading and never read;
* a declaration fixed before decoding: the observer's own stations (clock sites, light ports) and the list of
  measurements to make.

Nothing here imports ``universe24``, sees a board state, or writes a file.  Same inputs give the same report.

Time.  The update index of a click is used only as the event board's coordinate label of that click (R4: it is
recoverable from the causal order of the clicks).  Every physical number is also expressed in a station's PROPER
time: the laps of that station's own ring clock, one lap = ``lap`` proper units (a standard ring of 16 coarse
sites has lap 16, so a flat standard ring's proper time equals the update count).  Exact rationals throughout
(``Fraction``); "exact" means equality of click records, never a fit.

Measurements (``declaration["measurements"]``, each a dict with ``"type"`` and a ``"name"``):

``clock``        proper time at a station: the exact period P of its clock record (smallest p for which the record
                 is p-periodic on a run that ends at the horizon and covers >= 3 periods, silent updates included),
                 the tick times, and the rate dtau/dt = lap/P (= N relative to the board's coordinate time).
``received``     a pulse train received at a port: arrival times (filtered head clicks) and the exact period of the
                 port record inside a declared window.
``redshift``     emitter clock E received at port R of station S: one emitter lap (lap_E proper units of E) is
                 received as one exact period P_received of the port record, i.e. rate_S * P_received proper units
                 of S, so f_received/f_emitted = lap_E / (rate_S * P_received); rate_S is the receiving station's
                 own clock rate (or a declared calibration from a reference board, named in the report).
``one_way``      first arrival at port A (emission) and first arrival at port B after it: coordinate delay and the
                 delay in B's proper time.
``radar``        emission at port A (a passage in the declared direction inside the declared emission window),
                 reflection at port B (first click after), return at A (first passage in the opposite direction
                 after the reflection):
                 d = rate_A * (t3 - t1)/2 in A's proper time; Einstein's time of the reflection
                 tau_A((t1 + t3)/2); the Einstein offset t2 - (t1 + t3)/2 (coordinate) [R1 criterion].
``ring_radar``   the closed light path of a ring clock read as a radar loop: a tick at the dial site (t1), the next
                 head click at the antipode site (t2), the next tick (t3).
``metric``       N(x), H(x), v(x) and alpha from earlier measurements of this report (see ``metric``).
``regge``        discrete curvature of a station network from radar lengths (the Regge functions below, also in
                 ``regge.py``): 2D vertex deficits
                 (``triangles``) or 3D edge-hinge deficits and the Regge scalar (``tetrahedra``).
``shells``       Schwarzschild relations of a shell family: N * H_r; the areal radius r = C / 2 pi only from a
                 tangential ruler that is not the station's own clock ring (otherwise: "no areal-radius
                 measurement declared"); the mass function m(r) = (r/2)(1 - 1/H_r^2) and the (r, theta) curvature.
``schwarzschild`` vacuum test of a static spherical station family: m_i = (r_i/2)(1 - N_i^2) from clocks and
                 tangential radar must be one constant, and the radial radar light times must follow
                 r*(r) = r + 2m ln(r/2m - 1) with that m (no free parameter); the 1911 twin is the control.

Generic detector readouts (shared with the QM team):

``detector``     the clicks at one declared detector in a window: count, first/last update, distinct times, the
                 kind histogram and the observed (kind, quotient) signature; optional ``bin`` gives counts per bin.
``outcome``      several detectors over one window: which fired, the first to fire (ties listed), and whether
                 exactly one fired (an exclusive outcome).

Cross-run quantities (Shapiro excess, river, route switch) are differences of the same declared measurement in two
reports: ``compare(reports, measurement, key)``.

DECLARATION FORMAT ``r64-observer-declaration-1`` (the binding observer contract, BRIEF UPDATE 44; ``validate``)::

    {"format": "r64-observer-declaration-1",
     "name": "...", "horizon": 220,                       # horizon optional (else the last click's update)
     "medium": {"profile": "A", "what": "..."},           # optional, informational (the prepared medium)
     "stations": {                                        # the observer's instruments = the ONLY sites it reads
        "<name>": {"sites": [[x, y, z], ...],             # required
                   "channels": [g, ...] | null,           # click filters (null = any)
                   "kinds": [0, 1, 2] | null, "quotients": [q, ...] | null,
                   "role": "clock" | "port" | "mirror" | "antipode" | "detector",
                   "profile": "A" | "B" | "C",            # packet profile of the instrument's packet:
                                                          #   A = (1,0,-1), B = (0,1,-1), C = (1,-1,0)
                                                          # ("species" = deprecated alias, UPDATE 46 item 4)
                   "lap": 16, "mode": "period" | "ticks", "direction": 1}},   # clocks only
     "readouts": [ {"type": "<one of TYPES>", "name": "...", ...}, ... ]}       # alias "measurements"

Inside a readout, the instrument fields may name a station instead of repeating its sites: ``clock`` (clock),
``port`` (received, redshift), ``from.port`` / ``to.port`` (one_way), ``station.port`` / ``mirror.port`` (radar),
``antipode`` (ring_radar), ``detector`` (detector) and the list ``detectors`` (outcome).  Elsewhere a string names an
earlier readout (e.g. ``clock`` of ring_radar, metric and shells).
Every readout output echoes the profile of the instruments it used (``profile``, ``probe_profile``,
``emitter_profile``).  A, B and C are packet PROFILES, not species (BRIEF UPDATE 46 item 4); the old declaration key
``species`` is read as a deprecated alias of ``profile``.  The older inline style (sites written into each
measurement) stays valid.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Mapping, Sequence

VERSION = "r64-observer-gr-1.2"         # 1.2: species -> profile (referee r10zb fix 8); numbers unchanged
KEEP = ("step", "address", "kind", "quotient")
FORMAT = "r64-observer-declaration-1"
PROFILES = {"A": (1, 0, -1), "B": (0, 1, -1), "C": (1, -1, 0)}
SPECIES = PROFILES                       # deprecated alias (UPDATE 46 item 4: A, B, C are profiles)


def profile_of(decl) -> str | None:
    """The declared packet profile of an instrument (key ``profile``; ``species`` is a deprecated alias)."""
    if not isinstance(decl, Mapping):
        return None
    return decl.get("profile", decl.get("species"))
TYPES = ("clock", "received", "redshift", "one_way", "radar", "ring_radar", "metric", "regge", "shells",
         "schwarzschild", "detector", "outcome")


# ------------------------------------------------------------------------------------------------------ the log
class ClickLog:
    """Clicks indexed by site: {(x, y, z): [(t, g, kind, quotient), ...]} in log order; nothing else is kept."""

    def __init__(self, records: Iterable[Mapping], horizon: int | None = None, source: str | None = None,
                 sha256: str | None = None):
        sites: dict[tuple, list] = {}
        ignored: set[str] = set()
        n, last = 0, 0
        for rec in records:
            ignored.update(k for k in rec if k not in KEEP)
            x, y, z, g = rec["address"]
            t = int(rec["step"])
            sites.setdefault((x, y, z), []).append((t, int(g), int(rec["kind"]), int(rec["quotient"])))
            n += 1
            last = max(last, t)
        self.sites = sites
        self.events = n
        self.horizon = horizon if horizon is not None else last
        self.fields_ignored = sorted(ignored)
        self.source = source
        self.sha256 = sha256

    def info(self) -> dict:
        return {"source": self.source, "sha256": self.sha256, "events": self.events, "horizon": self.horizon,
                "fields_kept": list(KEEP), "fields_ignored": self.fields_ignored}


def read_log(path, horizon: int | None = None) -> ClickLog:
    """Load an official click log (JSONL); ``before``/``after`` are dropped record by record."""
    path = Path(path)
    blob = path.read_bytes()

    def records():
        for line in blob.decode("utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                yield {k: rec[k] for k in rec}           # all keys seen (to list the ignored ones); only KEEP used
    return ClickLog(records(), horizon=horizon, source=path.name, sha256=hashlib.sha256(blob).hexdigest())


# --------------------------------------------------------------------------------------------- records and ports
def _sites(decl) -> list[tuple]:
    return [tuple(s) for s in decl["sites"]]


def _accept(decl, g, kind, q) -> bool:
    ch, kinds, qs = decl.get("channels"), decl.get("kinds"), decl.get("quotients")
    return (ch is None or g in ch) and (kinds is None or kind in kinds) and (qs is None or q in qs)


def record(log: ClickLog, decl) -> dict[int, tuple]:
    """{t: sorted tuple of (site index, g, kind, quotient)} of the declared sites and filters."""
    out: dict[int, list] = {}
    for i, site in enumerate(_sites(decl)):
        for t, g, kind, q in log.sites.get(site, ()):
            if _accept(decl, g, kind, q):
                out.setdefault(t, []).append((i, g, kind, q))
    return {t: tuple(sorted(v)) for t, v in out.items()}


def clicks_at(log: ClickLog, decl, lo: int = 1, hi: int | None = None) -> list[int]:
    """Sorted distinct update indices at which a declared site has an accepted click, inside [lo, hi]."""
    hi = log.horizon if hi is None else hi
    return sorted(t for t in record(log, decl) if lo <= t <= hi)


def exact_period(rec: Mapping[int, tuple], lo: int, hi: int, min_reps: int = 3,
                 max_period: int | None = None) -> dict | None:
    """Smallest p such that rec[t] == rec[t + p] for every t of a run [s, hi - p] (silent updates count), the run
    [s, hi] covering >= min_reps periods and holding at least one click; s is the earliest such start (the run is
    anchored at hi, the steady end of the window).  None if no p qualifies."""
    span = hi - lo + 1
    top = span // min_reps if max_period is None else min(max_period, span // min_reps)
    for p in range(1, top + 1):
        t = hi - p
        while t >= lo and rec.get(t, ()) == rec.get(t + p, ()):
            t -= 1
        s = t + 1
        if hi - s + 1 >= min_reps * p and any(lo <= u <= hi and u >= s for u in rec):
            return {"period": p, "run": [s, hi], "periods_covered": Fraction(hi - s + 1, p)}
    return None


def passages(log: ClickLog, port, lo: int = 1, hi: int | None = None) -> list[dict]:
    """Head passages at a port.  A port declares ``sites`` (one site, or an ordered line of three fibre nodes
    [previous, centre, next]) and click filters.  For a three-node line the direction of each passage at the centre
    is +1 if the previous node had an accepted click one update earlier, -1 if the next node had, else 0."""
    hi = log.horizon if hi is None else hi
    sites = _sites(port)
    rec_of = [record(log, {**port, "sites": [s]}) for s in sites]
    centre = rec_of[len(sites) // 2] if len(sites) == 3 else rec_of[0]
    out = []
    for t in sorted(centre):
        if not lo <= t <= hi:
            continue
        d = 0
        if len(sites) == 3:
            before, after = (t - 1) in rec_of[0], (t - 1) in rec_of[2]
            d = 1 if before and not after else -1 if after and not before else 0
        out.append({"t": t, "direction": d})
    return out


# ------------------------------------------------------------------------------------------------- measurements
def signature(log: ClickLog, decl, lo: int = 1, hi: int | None = None) -> list:
    """The observed (kind, quotient) pairs of every click at the instrument's sites (channel filter only)."""
    hi = log.horizon if hi is None else hi
    ch = decl.get("channels")
    out = set()
    for site in _sites(decl):
        for t, g, kind, q in log.sites.get(site, ()):
            if lo <= t <= hi and (ch is None or g in ch):
                out.add((kind, q))
    return sorted(out)


def measure_detector(log: ClickLog, m: Mapping) -> dict:
    """Clicks at one declared detector in a window (the QM/GR shared readout)."""
    det = m["detector"]
    lo, hi = m.get("window", [1, log.horizon])
    rec = {t: v for t, v in record(log, det).items() if lo <= t <= hi}
    times = sorted(rec)
    kinds: dict = {}
    for v in rec.values():
        for _, g, kind, q in v:
            kinds[kind] = kinds.get(kind, 0) + 1
    out = {"profile": profile_of(det), "window": [lo, hi], "clicks": sum(len(v) for v in rec.values()),
           "first": times[0] if times else None, "last": times[-1] if times else None,
           "times": times[:1000], "kinds": {str(k): n for k, n in sorted(kinds.items())},
           "signature": sorted({(kind, q) for v in rec.values() for _, g, kind, q in v})}
    if m.get("bin"):
        b = int(m["bin"])
        bins = [0] * ((hi - lo) // b + 1)
        for t, v in rec.items():
            bins[(t - lo) // b] += len(v)
        out["bins"] = bins
    return out


def measure_outcome(log: ClickLog, m: Mapping) -> dict:
    """Which of several declared detectors fire in one window, and which fires first."""
    lo, hi = m["window"]
    first = {}
    for name, det in zip(m["detector_names"], m["detectors"]):
        ts = clicks_at(log, det, lo, hi)
        first[name] = ts[0] if ts else None
    fired = [n for n, t in first.items() if t is not None]
    t0 = min((first[n] for n in fired), default=None)
    return {"window": [lo, hi], "first_click": first, "fired": fired,
            "first_to_fire": [n for n in fired if first[n] == t0], "exclusive": len(fired) == 1}


INSTRUMENTS = {"clock": [("clock",)], "received": [("port",)], "redshift": [("port",)],
               "one_way": [("from", "port"), ("to", "port")], "radar": [("station", "port"), ("mirror", "port")],
               "ring_radar": [("antipode",)], "detector": [("detector",)]}


def resolve(declaration: Mapping) -> dict:
    """The declaration with every station reference replaced by the station's definition (a new dict).  Only the
    instrument fields of each readout type (``INSTRUMENTS``; ``detectors`` of an outcome) may name a station; a
    string elsewhere (e.g. ``clock`` in ring_radar / metric / shells) names an earlier readout."""
    import copy
    stations = declaration.get("stations", {})

    def station(name):
        if name not in stations:
            raise ValueError(f"unknown station {name!r}")
        return copy.deepcopy(dict(stations[name]))
    out = []
    for m in declaration.get("readouts", declaration.get("measurements", [])):
        r = copy.deepcopy(dict(m))
        for path in INSTRUMENTS.get(r.get("type"), ()):
            holder = r
            for k in path[:-1]:
                holder = holder.get(k) if isinstance(holder, Mapping) else None
            if isinstance(holder, dict) and isinstance(holder.get(path[-1]), str):
                holder[path[-1]] = station(holder[path[-1]])
        if r.get("type") == "outcome":
            names = list(m["detectors"])
            r["detector_names"] = [n if isinstance(n, str) else f"detector_{i}" for i, n in enumerate(names)]
            r["detectors"] = [station(n) if isinstance(n, str) else n for n in names]
        out.append(r)
    return {**{k: v for k, v in declaration.items() if k not in ("readouts", "measurements")}, "measurements": out}


def validate(declaration: Mapping) -> list[str]:
    """Problems of a declaration against ``r64-observer-declaration-1`` (empty list = valid)."""
    bad = []
    stations = declaration.get("stations", {})
    if not isinstance(stations, Mapping):
        return ["stations must be a mapping"]
    for name, st in stations.items():
        sites = st.get("sites") if isinstance(st, Mapping) else None
        if not sites or not all(isinstance(x, (list, tuple)) and len(x) == 3 and all(type(c) is int for c in x)
                                for x in sites):
            bad.append(f"station {name}: sites must be a non-empty list of [x, y, z] integers")
        for f in ("channels", "kinds", "quotients"):
            if st.get(f) is not None and not (isinstance(st[f], list) and all(type(v) is int for v in st[f])):
                bad.append(f"station {name}: {f} must be a list of integers or null")
        if "profile" in st and "species" in st and st["profile"] != st["species"]:
            bad.append(f"station {name}: profile and its deprecated alias species disagree")
        if profile_of(st) is not None and profile_of(st) not in PROFILES:
            bad.append(f"station {name}: profile must be one of {sorted(PROFILES)}")
    readouts = declaration.get("readouts", declaration.get("measurements"))
    if not isinstance(readouts, list) or not readouts:
        return bad + ["readouts (or measurements) must be a non-empty list"]
    names = [m.get("name") for m in readouts]
    if len(set(names)) != len(names) or None in names:
        bad.append("every readout needs a unique name")
    for m in readouts:
        if m.get("type") not in TYPES:
            bad.append(f"readout {m.get('name')}: unknown type {m.get('type')!r}")
        w = m.get("window")
        if w is not None and not (isinstance(w, list) and len(w) == 2 and all(type(v) is int for v in w)
                                  and w[0] <= w[1]):
            bad.append(f"readout {m.get('name')}: window must be [lo, hi] integers, lo <= hi")
    try:
        resolve(declaration)
    except (ValueError, KeyError) as exc:
        bad.append(f"reference: {exc}")
    return bad


def measure_ticks(log: ClickLog, m: Mapping) -> dict:
    """Tick mode (for clocks that need not be exactly periodic, e.g. in a sourced, irregular medium): the dial is a
    3-node port on the ring, [previous, dial, next] along the clock packet's own direction of circulation; every
    passage in that direction (+1) is one tick, so counter-circulating traffic is not counted.  Mean rate
    = lap * (ticks - 1) / (last tick - first tick) (exact rational); the tick intervals are reported, and
    'exactly_periodic' says whether they are all equal."""
    decl = m["clock"]
    lap = Fraction(decl.get("lap", 16))
    lo, hi = m.get("lo", 1), m.get("hi", log.horizon)
    ticks = [p["t"] for p in passages(log, decl, lo, hi) if p["direction"] == decl.get("direction", 1)]
    if len(ticks) < 2:
        return {"status": "fewer than two ticks", "ticks": ticks, "lap": lap}
    gaps = [b - a for a, b in zip(ticks, ticks[1:])]
    mean = Fraction(ticks[-1] - ticks[0], len(ticks) - 1)
    return {"status": "ok", "mode": "ticks", "profile": profile_of(decl), "ticks": ticks, "intervals": gaps,
            "mean_period": mean, "exactly_periodic": len(set(gaps)) == 1,
            "period": gaps[0] if len(set(gaps)) == 1 else None, "lap": lap, "rate": lap / mean}


def measure_clock(log: ClickLog, m: Mapping) -> dict:
    """Proper time at a station from its own ring clock's clicks."""
    decl = m["clock"]
    if decl.get("mode") == "ticks":
        return measure_ticks(log, m)
    lap = Fraction(decl.get("lap", 16))
    hi = m.get("hi", log.horizon)
    rec = record(log, decl)
    per = exact_period(rec, m.get("lo", 1), hi)
    if per is None:
        return {"status": "no exact period", "clicks": len(rec)}
    P, s = per["period"], per["run"][0]
    first = min(t for t in rec if t >= s)
    ticks = list(range(first, hi + 1, P))
    return {"status": "ok", "profile": profile_of(decl), "period": P, "run": per["run"],
            "periods_covered": per["periods_covered"], "lap": lap, "ticks": ticks,
            "tick_signature": list(rec[first]), "dial_signature": signature(log, decl),
            "rate": lap / P, "proper_time_at_horizon": lap * Fraction(hi - first, P)}


def proper_time(clock: Mapping, t) -> Fraction:
    """tau(t) of a clock measurement: lap units per lap, zero at its first steady tick, linear between ticks."""
    return clock["lap"] * (Fraction(t) - clock["ticks"][0]) / clock["period"]


def measure_received(log: ClickLog, m: Mapping) -> dict:
    lo, hi = m["window"]
    port = m["port"]
    rec = {t: v for t, v in record(log, port).items() if lo <= t <= hi}
    times = sorted(rec)
    per = exact_period(rec, lo, hi) if times else None
    return {"profile": profile_of(port), "arrivals": times, "first": times[0] if times else None,
            "period": None if per is None else per["period"],
            "run": None if per is None else per["run"],
            "clicks_per_period": None if per is None else sum(
                1 for t in times if per["run"][0] <= t < per["run"][0] + per["period"])}


def _rate(report: Mapping, ref) -> tuple[Fraction | None, str]:
    """A station rate: a clock measurement of this report (by name) or a declared calibration
    {"value": "p/q", "from": text}."""
    if isinstance(ref, str):
        c = report["measurements"].get(ref, {})
        return (c.get("rate"), f"clock {ref} of this log") if c.get("status") == "ok" else (None, f"clock {ref} absent")
    return Fraction(ref["value"]), "calibration: " + ref.get("from", "declared")


def measure_redshift(log: ClickLog, m: Mapping, report: Mapping) -> dict:
    rec = measure_received(log, m)
    emitter_lap = Fraction(m.get("emitter_lap", 16))
    rate_r, how = _rate(report, m["receiver_rate"])
    emitter = m.get("emitter_clock")
    out = {"received": rec, "receiver_rate": rate_r, "receiver_rate_source": how, "emitter_lap": emitter_lap,
           "emitter_profile": report["measurements"].get(emitter, {}).get("profile") if emitter else None}
    if rec["period"] and rate_r:
        received_proper = rate_r * rec["period"]              # received period in the receiver's proper time
        out["received_period_proper"] = received_proper
        out["f_received_over_f_emitted"] = emitter_lap / received_proper
        emitter = m.get("emitter_clock")
        if emitter and report["measurements"].get(emitter, {}).get("status") == "ok":
            e = report["measurements"][emitter]
            out["emitter_own_period"] = e["period"]
            out["static_check_received_equals_emitted_period"] = rec["period"] == e["period"]
    return out


def measure_one_way(log: ClickLog, m: Mapping, report: Mapping) -> dict:
    a = passages(log, m["from"]["port"], *m["from"]["window"])
    if m["from"].get("direction"):
        a = [p for p in a if p["direction"] == m["from"]["direction"]]
    if not a:
        return {"status": "no emission click"}
    t1 = a[0]["t"]
    lo, hi = m["to"]["window"]
    b = passages(log, m["to"]["port"], max(lo, t1 + 1), hi)
    if m["to"].get("direction"):
        b = [p for p in b if p["direction"] == m["to"]["direction"]]
    if not b:
        return {"status": "no arrival", "t_emit": t1}
    t2 = b[0]["t"]
    out = {"status": "ok", "probe_profile": profile_of(m["from"]["port"]), "t_emit": t1, "t_arrive": t2,
           "delay": t2 - t1}
    if m.get("receiver_rate") is not None:
        rate, how = _rate(report, m["receiver_rate"])
        if rate is not None:
            out["delay_receiver_proper"] = rate * (t2 - t1)
            out["receiver_rate_source"] = how
    return out


def measure_radar(log: ClickLog, m: Mapping, report: Mapping) -> dict:
    lo, hi = m.get("window", [1, log.horizon])
    elo, ehi = m.get("emit_window", [lo, hi])
    out_dir = m.get("direction", 1)
    sent = [p["t"] for p in passages(log, m["station"]["port"], elo, ehi) if p["direction"] == out_dir]
    if not sent:
        return {"status": "no emission"}
    t1 = sent[0]
    refl = passages(log, m["mirror"]["port"], t1 + 1, hi)
    if not refl:
        return {"status": "no reflection", "t1": t1}
    t2 = refl[0]["t"]
    back = [p["t"] for p in passages(log, m["station"]["port"], t2 + 1, hi) if p["direction"] == -out_dir]
    if not back:
        return {"status": "no return", "t1": t1, "t2": t2}
    t3 = back[0]
    rate, how = _rate(report, m["station_rate"])
    mid = Fraction(t1 + t3, 2)
    out = {"status": "ok", "probe_profile": profile_of(m["station"]["port"]), "t1": t1, "t2": t2, "t3": t3,
           "round_trip": t3 - t1, "einstein_offset": t2 - mid, "station_rate": rate, "station_rate_source": how}
    if rate is not None:
        out["radar_distance_proper"] = rate * Fraction(t3 - t1, 2)
        out["round_trip_proper"] = rate * (t3 - t1)
    if m.get("mirror_dwell") is not None:
        # a bare fibre end holds the pulse for `dwell` updates (a device constant, calibrated on a flat control):
        # the reflection lasts [t2, t2 + dwell]; Einstein's midpoint refers to the middle of the dwell
        dw = Fraction(m["mirror_dwell"])
        out["mirror_dwell"] = dw
        out["round_trip_corrected"] = t3 - t1 - dw
        out["einstein_offset_corrected"] = t2 + dw / 2 - mid
        if rate is not None:
            out["radar_distance_proper_corrected"] = rate * (t3 - t1 - dw) / 2
    return out


def measure_ring_radar(log: ClickLog, m: Mapping, report: Mapping) -> dict:
    """A ring clock's lap read as a radar loop: dial (emit, return) and antipode (reflection) of one ring."""
    clock = report["measurements"].get(m["clock"], {})
    if clock.get("status") != "ok":
        return {"status": "clock absent"}
    t1, t3 = clock["ticks"][0], clock["ticks"][0] + clock["period"]
    t2 = offset = None
    if m.get("antipode"):
        b = clicks_at(log, m["antipode"], t1 + 1, t3)
        if not b:
            return {"status": "no antipode click"}
        t2 = b[0]
        offset = t2 - Fraction(t1 + t3, 2)
    rate, how = _rate(report, m.get("station_rate", m["clock"]))
    out = {"status": "ok", "clock": m["clock"], "t1": t1, "t2": t2, "t3": t3, "round_trip": t3 - t1,
           "einstein_offset": offset, "station_rate": rate, "station_rate_source": how}
    if rate is not None:
        out["radar_distance_proper"] = rate * Fraction(t3 - t1, 2)
        out["round_trip_proper"] = rate * (t3 - t1)
    return out


# ------------------------------------------------------------------------------------------------------- metric
def _log_ratio(a: Fraction, b: Fraction) -> float | None:
    return None if a <= 0 or b <= 0 or b == 1 else math.log(a) / math.log(b)


def alpha_exact(v_ratio: Fraction, n_ratio: Fraction) -> str | None:
    """'2' if v_ratio == n_ratio**2 exactly, '1' if v_ratio == n_ratio exactly, else None."""
    if n_ratio == 1:
        return None
    if v_ratio == n_ratio ** 2:
        return "2"
    if v_ratio == n_ratio:
        return "1"
    return None


def metric(report: Mapping, m: Mapping) -> dict:
    """N(x), H(x), v(x) and alpha at declared places, from this report's measurements only.

    ``places``: {name: {"clock": clock measurement, "ruler": ring_radar or radar measurement (optional),
    "ruler_length": coordinate length the ruler's round trip covers, in lattice units (e.g. 16 sites)}}
    ``reference``: the far place (N = 1, H = 1, v = 1 by definition of the units).

    N(x)   = rate(x) / rate(ref)                          (clock rate: lapse; equals the redshift factor)
    H(x)   = proper round trip of the ruler / its coordinate length, relative to the reference
             (radar length per lattice link in the station's own proper time)
    v(x)   = coordinate light speed along the ruler = coordinate length / coordinate round trip, relative to ref
    alpha  = ln v / ln N  (two-point slope, reference N = v = 1);  identity: alpha = 1 - ln H / ln N.
    """
    meas = report["measurements"]
    places = {name: (meas[p["clock"]], meas.get(p["ruler"]) if p.get("ruler") else None, p.get("ruler_length"))
              for name, p in m["places"].items()}
    return metric_rows(places, m["reference"])


def metric_rows(places: Mapping[str, tuple], reference: str) -> dict:
    """``metric`` from (clock measurement, ruler measurement or None, ruler coarse length) per place; the places may
    come from different logs (e.g. a far-clock run and a clock-in-medium run of one experiment)."""
    rows = {}
    for name, (c, ruler, length) in places.items():
        row = {"rate": c.get("rate")}
        if ruler and ruler.get("status") == "ok" and c.get("rate") is not None:
            L = Fraction(length)
            row["ruler_round_trip"] = ruler["round_trip"]
            row["H_raw"] = c["rate"] * ruler["round_trip"] / L
            row["v_raw"] = L / ruler["round_trip"]
        rows[name] = row
    m = {"reference": reference}
    ref = rows[m["reference"]]
    if ref["rate"] is None or any(row["rate"] is None for row in rows.values()):
        return {"status": "a clock has no exact period", "reference": m["reference"], "places": rows}
    for name, row in rows.items():
        row["N"] = row["rate"] / ref["rate"]
        if "H_raw" in row and "H_raw" in ref:
            row["H"] = row["H_raw"] / ref["H_raw"]
            row["v"] = row["v_raw"] / ref["v_raw"]
            row["alpha"] = _log_ratio(row["v"], row["N"])
            row["alpha_from_H"] = None if row["N"] == 1 else 1 - math.log(row["H"]) / math.log(row["N"])
            row["alpha_exact"] = alpha_exact(row["v"], row["N"])
    return {"reference": m["reference"], "places": rows}


# ----------------------------------------------- curvature from lengths (verbatim from r64/regge.py; this file is
# self-contained so that it can be pinned as ONE frozen file, packager r67's request; regge.py keeps the same code for
# the synthetic tests, and a test checks that both copies agree)
# ------------------------------------------------------------------------------------------------- triangles
def triangle_angles(a: float, b: float, c: float) -> tuple[float, float, float]:
    """Angles opposite to the sides a, b, c of a Euclidean triangle (radians)."""
    def ang(x, y, z):                       # angle opposite x
        v = (y * y + z * z - x * x) / (2 * y * z)
        if v < -1 - 1e-12 or v > 1 + 1e-12:
            raise ValueError(f"lengths {a}, {b}, {c} violate the triangle inequality")
        return math.acos(max(-1.0, min(1.0, v)))
    return ang(a, b, c), ang(b, c, a), ang(c, a, b)


def _key(u, v):
    return (u, v) if str(u) <= str(v) else (v, u)


def deficits_2d(lengths: Mapping[tuple, float], triangles: Iterable[Sequence], interior: Iterable = None) -> dict:
    """{vertex: 2 pi - sum of its triangle angles} for the interior vertices (default: every vertex whose triangles
    close around it, i.e. each of its edges is shared by exactly two of its triangles)."""
    L = {_key(*k): float(v) for k, v in lengths.items()}
    angle_sum: dict = {}
    edge_count: dict = {}
    for tri in triangles:
        p, q, r = tri
        a, b, c = L[_key(q, r)], L[_key(r, p)], L[_key(p, q)]
        A, B, C = triangle_angles(a, b, c)
        for v, x in ((p, A), (q, B), (r, C)):
            angle_sum[v] = angle_sum.get(v, 0.0) + x
        for e in (_key(p, q), _key(q, r), _key(r, p)):
            edge_count[e] = edge_count.get(e, 0) + 1
    if interior is None:
        interior = [v for v in angle_sum
                    if all(n == 2 for e, n in edge_count.items() if v in e)]
    return {v: 2 * math.pi - angle_sum[v] for v in interior}


# ----------------------------------------------------------------------------------------------- tetrahedra
def _embed(l01, l02, l03, l12, l13, l23):
    """Coordinates of a tetrahedron with the given edge lengths (vertex 0 at the origin)."""
    x1 = l01
    x2 = (l02 ** 2 + l01 ** 2 - l12 ** 2) / (2 * l01)
    y2 = math.sqrt(max(0.0, l02 ** 2 - x2 ** 2))
    x3 = (l03 ** 2 + l01 ** 2 - l13 ** 2) / (2 * l01)
    y3 = (l03 ** 2 + x2 ** 2 + y2 ** 2 - l23 ** 2 - 2 * x2 * x3) / (2 * y2)
    z3sq = l03 ** 2 - x3 ** 2 - y3 ** 2
    if z3sq < -1e-9 * max(l01, l02, l03) ** 2:
        raise ValueError("edge lengths do not form a Euclidean tetrahedron")
    return [(0.0, 0.0, 0.0), (x1, 0.0, 0.0), (x2, y2, 0.0), (x3, y3, math.sqrt(max(0.0, z3sq)))]


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def dihedral_angles(tet: Sequence, lengths: Mapping[tuple, float]) -> dict:
    """{edge: interior dihedral angle} of the tetrahedron ``tet`` = (p, q, r, s) from its six edge lengths."""
    p = list(tet)
    L = {_key(*k): float(v) for k, v in lengths.items()}
    g = lambda i, j: L[_key(p[i], p[j])]
    X = _embed(g(0, 1), g(0, 2), g(0, 3), g(1, 2), g(1, 3), g(2, 3))
    out = {}
    for i in range(4):
        for j in range(i + 1, 4):
            k, l = [m for m in range(4) if m not in (i, j)]
            e = _sub(X[j], X[i])
            # components of (X[k] - X[i]) and (X[l] - X[i]) orthogonal to the edge
            def perp(v):
                w = _sub(v, X[i])
                t = _dot(w, e) / _dot(e, e)
                return tuple(w[m] - t * e[m] for m in range(3))
            u, w = perp(X[k]), perp(X[l])
            c = _dot(u, w) / math.sqrt(_dot(u, u) * _dot(w, w))
            out[_key(p[i], p[j])] = math.acos(max(-1.0, min(1.0, c)))
    return out


def deficits_3d(lengths: Mapping[tuple, float], tetrahedra: Iterable[Sequence], interior_edges=None) -> dict:
    """{edge: 2 pi - sum of the dihedral angles at that edge} for the interior edges (default: edges whose
    tetrahedra close around them, judged by each incident face being shared by exactly two tetrahedra)."""
    dsum: dict = {}
    faces: dict = {}
    for tet in tetrahedra:
        for e, a in dihedral_angles(tet, lengths).items():
            dsum[e] = dsum.get(e, 0.0) + a
        for skip in range(4):
            f = tuple(sorted((v for m, v in enumerate(tet) if m != skip), key=str))
            faces[f] = faces.get(f, 0) + 1
    if interior_edges is None:
        interior_edges = [e for e in dsum
                          if all(n == 2 for f, n in faces.items() if e[0] in f and e[1] in f)]
    return {e: 2 * math.pi - dsum[e] for e in interior_edges}


def regge_scalar(deficits: Mapping[tuple, float], lengths: Mapping[tuple, float]) -> dict:
    """sum eps_h l_h (= half the integrated scalar curvature) and sum |eps_h| l_h (its scale) over the hinges."""
    L = {_key(*k): float(v) for k, v in lengths.items()}
    s = sum(eps * L[_key(*e)] for e, eps in deficits.items())
    a = sum(abs(eps) * L[_key(*e)] for e, eps in deficits.items())
    return {"sum_eps_l": s, "sum_abs_eps_l": a, "relative": s / a if a else 0.0, "hinges": len(deficits)}


# -------------------------------------------------------------------------------------- orthogonal shells
def shell_curvature(r: Sequence[float], A: Sequence[float], B: Sequence[float]) -> list:
    """Gaussian curvature of the (r, theta) surface dl^2 = A(r)^2 dr^2 + B(r)^2 dtheta^2 at the interior shells,
    by centred differences: K = -(1/(A B)) d/dr( B' / A ).  ``A``: radial proper length per unit r at the shells,
    ``B``: tangential proper length per unit angle at the shells."""
    out = []
    for i in range(1, len(r) - 1):
        # B'/A at the half points
        q_minus = (B[i] - B[i - 1]) / (r[i] - r[i - 1]) / ((A[i] + A[i - 1]) / 2)
        q_plus = (B[i + 1] - B[i]) / (r[i + 1] - r[i]) / ((A[i + 1] + A[i]) / 2)
        dq = (q_plus - q_minus) / ((r[i + 1] - r[i - 1]) / 2)
        out.append(-dq / (A[i] * B[i]))
    return out


def schwarzschild_relations(shells: Sequence[Mapping]) -> list:
    """Per shell (ordered outward): N (clock rate, far = 1), C (proper circumference from tangential radar) and
    ell (proper radial distance from the innermost shell, from radial radar).  Returns per interval the areal radius
    r = C / 2 pi at its midpoint, H_r = d ell / d r, N * H_r (Schwarzschild: 1) and the mass function
    m = (r/2)(1 - 1/H_r^2) (Schwarzschild: constant), plus 1 - N^2 against 2m/r."""
    out = []
    for a, b in zip(shells, shells[1:]):
        ra, rb = a["C"] / (2 * math.pi), b["C"] / (2 * math.pi)
        H = (b["ell"] - a["ell"]) / (rb - ra)
        r = (ra + rb) / 2
        N = (a["N"] + b["N"]) / 2
        m = r / 2 * (1 - 1 / H ** 2)
        out.append({"r": r, "H_r": H, "N": N, "N_times_H_r": N * H, "m": m,
                    "one_minus_N2": 1 - N * N, "two_m_over_r": 2 * m / r})
    return out


# ------------------------------------------------------------------- static vacuum equations (acceptance test)
def _d1d2(s, f, i):
    """First and second derivative of f at s[i] from its two neighbours (non-uniform centred differences)."""
    h1, h2 = s[i] - s[i - 1], s[i + 1] - s[i]
    d1 = (-h2 / (h1 * (h1 + h2))) * f[i - 1] + ((h2 - h1) / (h1 * h2)) * f[i] + (h1 / (h2 * (h1 + h2))) * f[i + 1]
    d2 = 2 * (f[i - 1] / (h1 * (h1 + h2)) - f[i] / (h1 * h2) + f[i + 1] / (h2 * (h1 + h2)))
    return d1, d2


def static_vacuum_spherical(N: Sequence[float], r: Sequence[float], s: Sequence[float], m: float | None = None):
    """The static vacuum Einstein equations in lapse/space form for a spherical station family (overseer r66's
    acceptance test): with s the proper radial distance (radar), r(s) the areal radius (tangential radar) and N(s)
    the lapse (clocks), the space metric is ds^2 + r(s)^2 dOmega^2 and

        K_t = (1 - r'^2) / r^2      (sectional curvature of the tangential planes; Schwarzschild +2m/r^3)
        K_r = -r'' / r              (radial planes; Schwarzschild -m/r^3)
        R[h] = 2 (2 K_r + K_t)      (spatial Ricci scalar; vacuum 0)
        Delta N = N'' + 2 (r'/r) N'                                   (vacuum 0)
        R_ss = 2 K_r = N''/N,  R_tt = K_r + K_t = r' N' / (r N)       (R_ij[h] = nabla_i nabla_j N / N)

    evaluated at every interior station by centred differences.  Residuals are divided by the curvature scale
    3m/r^3 (Schwarzschild's |K_t| + |K_r|; without m: the measured |K_t| + |K_r|) at that station.  ``m`` (e.g. from the clocks) gives the Schwarzschild ratios; the Misner-Sharp mass
    r (1 - r'^2)/2 is reported too."""
    rows = []
    for i in range(1, len(s) - 1):
        r1, r2 = _d1d2(s, r, i)
        N1, N2 = _d1d2(s, N, i)
        Kt, Kr = (1 - r1 ** 2) / r[i] ** 2, -r2 / r[i]
        lap = N2 + 2 * (r1 / r[i]) * N1
        scale = 3 * m / r[i] ** 3 if m else abs(Kt) + abs(Kr)     # Schwarzschild's |K_t| + |K_r| when m is given
        row = {"s": s[i], "r": r[i], "N": N[i], "K_tangential": Kt, "K_radial": Kr,
               "misner_sharp_mass": r[i] * (1 - r1 ** 2) / 2, "laplacian_N": lap,
               "res_laplacian_N": (lap / N[i]) / scale if scale else None,
               "res_ricci_scalar": 2 * (2 * Kr + Kt) / scale if scale else None,
               "res_R_radial": (2 * Kr - N2 / N[i]) / scale if scale else None,
               "res_R_tangential": (Kr + Kt - r1 * N1 / (r[i] * N[i])) / scale if scale else None}
        if m:
            row["K_tangential_over_2m_r3"] = Kt / (2 * m / r[i] ** 3)
            row["K_radial_over_minus_m_r3"] = Kr / (-m / r[i] ** 3)
        rows.append(row)
    return rows


def static_vacuum_planar(N: Sequence[float], s: Sequence[float]):
    """A planar station family (the tangential radar lengths do not change outward): space is flat, every sectional
    curvature 0, so the vacuum equations R_ij = nabla_i nabla_j N / N reduce to N'' = 0 (N linear in the proper
    distance: Rindler).  Reports N', N'' and the dimensionless N'' (s_next - s_prev) / |N'| at interior stations."""
    rows = []
    for i in range(1, len(s) - 1):
        N1, N2 = _d1d2(s, N, i)
        rows.append({"s": s[i], "N": N[i], "N_first": N1, "N_second": N2,
                     "res_N_second": N2 * (s[i + 1] - s[i - 1]) / abs(N1) if N1 else None})
    return rows


# ------------------------------------------------------------------------------------- curvature (Regge) and shells
def _length(report: Mapping, spec) -> float | None:
    """An edge length in proper units: {"measurement": name, "key": key, "scale": factor} (default key
    "radar_distance_proper") or {"value": number} (a declared length, e.g. in a synthetic test)."""
    if "value" in spec:
        return float(Fraction(spec["value"]))
    r = report["measurements"].get(spec["measurement"], {})
    v = r.get(spec.get("key", "radar_distance_proper"))
    return None if v is None else float(Fraction(v) * Fraction(spec.get("scale", 1)))


def _edges(report: Mapping, m: Mapping) -> tuple[dict, list]:
    lengths, missing = {}, []
    for name, spec in m["edges"].items():
        u, v = name.split("|")
        x = _length(report, spec)
        if x is None:
            missing.append(name)
        else:
            lengths[(u, v)] = x
    return lengths, missing


def measure_regge(report: Mapping, m: Mapping) -> dict:
    """2D (``triangles``): vertex deficit angles; 3D (``tetrahedra``): edge-hinge deficits and the Regge scalar
    sum eps_h l_h (= half the integrated scalar curvature) against its scale sum |eps_h| l_h."""
    lengths, missing = _edges(report, m)
    if missing:
        return {"status": "edges without a radar length", "missing": missing}
    if "triangles" in m:
        d = deficits_2d(lengths, [tuple(t) for t in m["triangles"]], m.get("interior"))
        return {"status": "ok", "dimension": 2, "deficits": {str(k): v for k, v in d.items()},
                "sum_deficits": sum(d.values()), "max_abs_deficit": max((abs(v) for v in d.values()), default=0.0)}
    d = deficits_3d(lengths, [tuple(t) for t in m["tetrahedra"]])
    return {"status": "ok", "dimension": 3, "hinges": len(d), "regge_scalar": regge_scalar(d, lengths),
            "max_abs_deficit": max((abs(v) for v in d.values()), default=0.0)}


def measure_shells(report: Mapping, m: Mapping) -> dict:
    """Schwarzschild relations from a shell family, ordered outward.  Per shell: ``clock`` (a clock measurement:
    N = rate / rate of the ``reference`` shell), optional ``ruler`` + ``ruler_length`` (a ring_radar of radial links:
    radial radar length per coordinate step H_r = rate x round trip / length), optional ``circumference`` (an edge
    spec: the shell's proper circumference from tangential radar) and ``ell`` (an edge spec: proper radial distance
    from the innermost shell, from radial radar).  Reports N * H_r per shell (Schwarzschild: 1).

    The areal radius r = C / 2 pi is MEASURED only by a tangential ruler that is not a standard clock.  If a shell's
    "circumference" is the round trip of that station's own clock ring (a ring_radar read on the shell's clock), it
    has the same proper size at every station by definition and cannot see the areal radius: the readout then says
    "no areal-radius measurement declared" and reads nothing about flatness or m(r) (referee r10zb / r68 D14,
    10:03 UTC; the earlier 'planar' reading of E10 and E-II is withdrawn).  With true tangential rulers and C and
    ell at every shell it gives the mass function m(r) = (r/2)(1 - 1/H_r^2) (constant in vacuum, then
    N^2 = 1 - 2m/r) and the (r, theta) curvature K (Schwarzschild: -m/r^3)."""
    meas = report["measurements"]
    rows = []
    clock_ruler = []
    for sh in m["shells"]:
        c = meas.get(sh["clock"], {})
        row = {"name": sh["name"], "rate": c.get("rate")}
        if sh.get("ruler"):
            rr = meas.get(sh["ruler"], {})
            if rr.get("status") == "ok" and c.get("rate") is not None:
                row["H_r_raw"] = c["rate"] * rr["round_trip"] / Fraction(sh["ruler_length"])
        circ = sh.get("circumference")
        if circ:
            src = meas.get(circ.get("measurement"), {}) if "measurement" in circ else {}
            if src.get("clock") == sh["clock"]:
                clock_ruler.append(sh["name"])          # the station's own clock ring: not an areal-radius ruler
            else:
                row["C"] = _length(report, circ)
        if sh.get("ell"):
            row["ell"] = _length(report, sh["ell"])
        rows.append(row)
    ref = next(r for r in rows if r["name"] == m["reference"])
    if ref["rate"] is None:
        return {"status": "reference clock absent", "shells": rows}
    for r in rows:
        if r["rate"] is not None:
            r["N"] = r["rate"] / ref["rate"]
        if "H_r_raw" in r and "H_r_raw" in ref:
            r["H_r"] = r["H_r_raw"] / ref["H_r_raw"]
            r["N_times_H_r"] = r["N"] * r["H_r"]
    out = {"status": "ok", "shells": rows}
    Cs = [r.get("C") for r in rows]
    if clock_ruler or not all(c is not None for c in Cs):
        out["areal_radius_measured"] = False
        out["geometry"] = ("no areal-radius measurement declared" + (
            f": the only tangential ruler at shells {clock_ruler} is the station's own clock ring, a standard clock "
            "of the same proper size at every station by definition" if clock_ruler else "") +
            "; neither flatness nor m(r) = const can be read; N * H_r = 1 alone does not certify Schwarzschild")
        return out
    out["areal_radius_measured"] = True
    if len(Cs) >= 2:
        out["areal_radius"] = [c / (2 * math.pi) for c in Cs]
        out["areal_radius_changes"] = any(abs(a - b) > 1e-12 for a, b in zip(Cs, Cs[1:]))
        if out["areal_radius_changes"] and all(r.get("ell") is not None and r.get("N") is not None for r in rows):
            sh = [{"N": float(r["N"]), "C": r["C"], "ell": r["ell"]} for r in rows]
            out["relations"] = schwarzschild_relations(sh)
            rad = out["areal_radius"]
            if len(rows) >= 3:
                A = [None] * len(rows)
                for i in range(len(rows)):
                    j, k = max(0, i - 1), min(len(rows) - 1, i + 1)
                    A[i] = (rows[k]["ell"] - rows[j]["ell"]) / (rad[k] - rad[j])
                out["curvature_r_theta"] = shell_curvature(rad, A, rad)
        elif not out["areal_radius_changes"]:
            # measured by true tangential rulers (not clocks): equal circumferences at every shell
            out["geometry"] = ("the measured tangential circumference is the same at every shell: no areal-radius "
                               "change; the (r, theta) surface dl^2 = H_r^2 dr^2 + C^2 dtheta^2 / 4 pi^2 has K = 0")
            out["curvature_r_theta"] = [0.0] * max(0, len(rows) - 2)
            pos = [sh.get("position") for sh in m["shells"]]
            if all(p_ is not None for p_ in pos) and all("H_r" in r for r in rows):
                order = sorted(range(len(rows)), key=lambda i: pos[i])
                link = float(m.get("link_length", 1))
                s_prop = [0.0]
                for a, b in zip(order, order[1:]):
                    s_prop.append(s_prop[-1] + link * (pos[b] - pos[a]) * (float(rows[a]["H_r"]) +
                                                                            float(rows[b]["H_r"])) / 2)
                Ns = [float(rows[i]["N"]) for i in order]
                out["static_vacuum_acceptance"] = {
                    "reading": "measured equal circumferences: flat space, so vacuum needs N'' = 0",
                    "order": [rows[i]["name"] for i in order], "s_proper": s_prop, "N": Ns,
                    "interior_stations": static_vacuum_planar(Ns, s_prop), "testable": len(rows) >= 3}
    return out


def measure_schwarzschild(report: Mapping, m: Mapping) -> dict:
    """Vacuum test of a static spherical station family, from clocks and radar only.

    Per shell i (ordered outward): N_i = clock rate / far-clock rate; the tangential radar arm over 1/k of the
    shell gives the proper circumference C_i = k * (dwell-corrected radar length in the shell's proper time) and the
    areal radius r_i = C_i / 2 pi; the mass parameter m_i = (r_i / 2)(1 - N_i^2) (constant in vacuum, Birkhoff).
    The radial radar arm from shell i to i+1 gives the coordinate light time T_i = (t3 - t1 - dwell)/2, compared
    with Schwarzschild's T = r*(r_i+1) - r*(r_i), r* = r + 2m ln(r/2m - 1) (radial light speed N^2, alpha = 2) and
    with the 1911 twin T = int dr / N (radial light speed N, alpha = 1), both with m = mean m_i: no free parameter.
    The radial radar length per areal-radius step is H_r ~ N_mid T_i / (r_i+1 - r_i); Schwarzschild: N H_r -> 1."""
    meas = report["measurements"]
    far = meas.get(m["far_clock"], {})
    if far.get("status") != "ok":
        return {"status": "far clock absent"}
    k = m.get("arc_fraction", 1)
    rows = []
    for sh in m["shells"]:
        c, a = meas.get(sh["clock"], {}), meas.get(sh["arc"], {})
        if c.get("status") != "ok" or a.get("status") != "ok":
            return {"status": f"shell {sh['clock']} incomplete"}
        N = c["rate"] / far["rate"]
        C = k * a["radar_distance_proper_corrected"]
        r = float(C) / (2 * math.pi)
        row = {"N": N, "C": C, "r": r, "m": r / 2 * (1 - float(N) ** 2)}
        if sh.get("radial"):
            rad = meas.get(sh["radial"], {})
            if rad.get("status") == "ok":
                row["T_radial"] = Fraction(rad["round_trip_corrected"], 2)
        rows.append(row)
    ms = [row["m"] for row in rows]
    mh = sum(ms) / len(ms)

    def rstar(r):
        return r + 2 * mh * math.log(r / (2 * mh) - 1)

    def twin(r1, r2, n=4000):
        h = (r2 - r1) / n
        f = lambda r: 1 / math.sqrt(1 - 2 * mh / r)
        return h / 3 * (f(r1) + f(r2) + sum((4 if i % 2 else 2) * f(r1 + i * h) for i in range(1, n)))
    for a, b in zip(rows, rows[1:]):
        if "T_radial" not in a:
            continue
        T = float(a["T_radial"])
        a["T_schwarzschild"] = rstar(b["r"]) - rstar(a["r"])
        a["T_twin"] = twin(a["r"], b["r"])
        a["residual_schwarzschild"] = (T - a["T_schwarzschild"]) / T
        a["residual_twin"] = (T - a["T_twin"]) / T
        nmid = (float(a["N"]) + float(b["N"])) / 2
        a["N_mid_times_H_r"] = nmid * nmid * T / (b["r"] - a["r"])
    have = [r for r in rows if "T_radial" in r]
    shapiro = None
    if have and len(have) == len(rows) - 1:
        # radar Shapiro delay over the whole radial chain: coordinate light time minus the areal-radius difference,
        # against Schwarzschild's logarithm 2m ln((r_out - 2m)/(r_in - 2m)) (one way)
        excess = float(sum(r["T_radial"] for r in have)) - (rows[-1]["r"] - rows[0]["r"])
        shapiro = {"one_way_excess": excess,
                   "schwarzschild_log": 2 * mh * math.log((rows[-1]["r"] - 2 * mh) / (rows[0]["r"] - 2 * mh)),
                   "twin_excess": sum(twin(a["r"], b["r"]) for a, b in zip(rows, rows[1:]))
                   - (rows[-1]["r"] - rows[0]["r"])}
    acceptance = None
    if have and len(have) == len(rows) - 1 and len(rows) >= 3:
        s_prop = [0.0]
        for a, b in zip(rows, rows[1:]):                 # proper radial distance from two-sided radar (midpoint N)
            s_prop.append(s_prop[-1] + (float(a["N"]) + float(b["N"])) / 2 * float(a["T_radial"]))
        acc = static_vacuum_spherical([float(r["N"]) for r in rows], [r["r"] for r in rows], s_prop, mh)
        keys = ("res_laplacian_N", "res_ricci_scalar", "res_R_radial", "res_R_tangential")
        acceptance = {"interior_stations": acc,
                      "max_abs_residual": {k: max(abs(x[k]) for x in acc) for k in keys},
                      "K_tangential_over_2m_r3": [x["K_tangential_over_2m_r3"] for x in acc],
                      "K_radial_over_minus_m_r3": [x["K_radial_over_minus_m_r3"] for x in acc],
                      "misner_sharp_mass": [x["misner_sharp_mass"] for x in acc]}
    return {"status": "ok", "shells": rows, "m_mean": mh, "m_relative_spread": (max(ms) - min(ms)) / mh,
            "shapiro_radial_chain": shapiro, "static_vacuum_acceptance": acceptance,
            "max_abs_residual_schwarzschild": max(abs(r["residual_schwarzschild"]) for r in rows
                                                  if "residual_schwarzschild" in r),
            "max_abs_residual_twin": max(abs(r["residual_twin"]) for r in rows if "residual_twin" in r)}


# ------------------------------------------------------------------------------------------------------ observe
def observe(log: ClickLog | str | Path, declaration: Mapping) -> dict:
    """The observer's report: a pure function of the click log and the declaration."""
    if not isinstance(log, ClickLog):
        log = read_log(log, horizon=declaration.get("horizon"))
    elif declaration.get("horizon") is not None and declaration["horizon"] != log.horizon:
        raise ValueError(f"declared horizon {declaration['horizon']} != log horizon {log.horizon}")
    problems = validate(declaration)
    if problems:
        raise ValueError("invalid declaration: " + "; ".join(problems))
    declaration = resolve(declaration)
    report = {"observer": VERSION, "input": log.info(), "declaration_name": declaration.get("name"),
              "medium": declaration.get("medium"), "measurements": {}}
    for m in declaration["measurements"]:
        kind = m["type"]
        if kind == "clock":
            out = measure_clock(log, m)
        elif kind == "received":
            out = measure_received(log, m)
        elif kind == "redshift":
            out = measure_redshift(log, m, report)
        elif kind == "one_way":
            out = measure_one_way(log, m, report)
        elif kind == "radar":
            out = measure_radar(log, m, report)
        elif kind == "ring_radar":
            out = measure_ring_radar(log, m, report)
        elif kind == "metric":
            out = metric(report, m)
        elif kind == "regge":
            out = measure_regge(report, m)
        elif kind == "shells":
            out = measure_shells(report, m)
        elif kind == "schwarzschild":
            out = measure_schwarzschild(report, m)
        elif kind == "detector":
            out = measure_detector(log, m)
        elif kind == "outcome":
            out = measure_outcome(log, m)
        else:
            raise ValueError(f"unknown measurement type {kind!r}")
        report["measurements"][m["name"]] = out
    return report


def station_sites(declaration: Mapping) -> set[tuple]:
    """Every site the declaration's stations read (clock dials, antipodes, ports): the observer's whole world."""
    out: set[tuple] = set()
    declaration = resolve(declaration)

    def walk(obj):
        if isinstance(obj, Mapping):
            if "sites" in obj:
                out.update(tuple(s) for s in obj["sites"])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(declaration.get("measurements", []))
    return out


def run_declared(log, declaration: Mapping) -> dict:
    """The observer as a decoder layer (packager r67): ``jsonable(observe(log, declaration))`` — JSON-ready (fractions
    as "p/q" strings, tuples as lists), like click_decoder_v1's ``beat_clock_v1.run_declared``.  ``log`` is a path
    to an official click log or a ``ClickLog``."""
    return jsonable(observe(log, declaration))


def compare(reports: Mapping[str, Mapping], measurement: str, key: str, baseline: str) -> dict:
    """{run: value - baseline value} of one measurement key across reports (e.g. Shapiro excess of a delay)."""
    base = reports[baseline]["measurements"][measurement][key]
    return {name: (r["measurements"][measurement].get(key) - base
                   if r["measurements"][measurement].get(key) is not None else None)
            for name, r in reports.items()}


def jsonable(obj):
    """Fractions as 'p/q' strings (integers stay integers) for writing a report."""
    if isinstance(obj, Fraction):
        return obj.numerator if obj.denominator == 1 else f"{obj.numerator}/{obj.denominator}"
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    return obj


__all__ = ["ClickLog", "read_log", "record", "clicks_at", "exact_period", "passages", "proper_time", "observe",
           "metric", "metric_rows", "station_sites", "compare", "alpha_exact", "jsonable", "validate", "resolve",
           "signature", "profile_of", "run_declared", "deficits_2d", "deficits_3d", "regge_scalar",
           "shell_curvature", "schwarzschild_relations", "static_vacuum_spherical", "static_vacuum_planar",
           "VERSION", "FORMAT", "PROFILES", "SPECIES", "TYPES"]


def main(argv=None) -> int:
    """python -m research.matter_light_v1.r64.observer_gr LOG.jsonl DECLARATION.json [KEY] [--horizon N]

    DECLARATION is a single declaration ({"measurements": [...]}) or a stations file with "declarations"; KEY picks
    one of them.  Prints the report (JSON, fractions as "p/q") to stdout; writes nothing."""
    import argparse
    ap = argparse.ArgumentParser(description="r64 GR observer: read-only report from a click log")
    ap.add_argument("log")
    ap.add_argument("declaration")
    ap.add_argument("key", nargs="?")
    ap.add_argument("--horizon", type=int)
    a = ap.parse_args(argv)
    decl = json.loads(Path(a.declaration).read_text(encoding="utf-8"))
    if "declarations" in decl:
        decl = decl["declarations"][a.key]
    if a.horizon is not None:
        decl = {**decl, "horizon": a.horizon}
    print(json.dumps(jsonable(observe(a.log, decl)), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
