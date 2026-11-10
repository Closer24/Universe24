"""beat_clock_v1: a declared read-only observer of official click logs (proposal for the experiments package, r25).

Purpose.  Decoder v1.0 reports click timing, periods, tracks and kinds, but no phase of the click quotient, so it
cannot read the rate of a beat clock in the linear regime (r14 N6).  This observer does exactly that and nothing
else.  It is an OBSERVER-LAYER claim, not a decoder claim.

Input contract (the same as the decoder's): from each record of the official ``--events`` JSONL only ``step``,
``address`` = (x, y, z, g) and ``quotient`` are used (``click_decoder_v1.read_log``).  Declared before decoding:
the board side, the horizon, one channel, a detector (a list of sites; default: every site), and per clock two
wavevectors K1, K2 (radians per site, 3-vectors), the clock axis e (unit 3-vector, motion is read along e) and the
light speed c along e that the special-relativity prediction uses.  An absent record means q = 0 at that address.

Algorithm (pure function, no state, no tuning):
  F_i(t) = sum over detector sites x of q_t(x) exp(-i K_i . x)              (one Fourier projection per wave)
  omega_i: if F_i rotates (|mean Im(F(t+1) conj F(t))| > 1e-9 |F|^2) the signed phasor rate
           -arg(sum F(t+1) conj F(t)); else (a standing wave, F real up to a constant phase) the Prony rate
           arccos( sum s_t (s_{t+1} + s_{t-1}) / (2 sum s_t^2) ) of s_t = Re(F_i(t) exp(-i arg F_i(t*))), t* = argmax |F|.
  k_i = K_i . e (axis wavenumbers); chord speed u = (omega_2 - omega_1)/(k_2 - k_1);
  clock rate at the in-phase point Omega = (k_2 omega_1 - k_1 omega_2)/(k_2 - k_1);
  rest frequency w' = sqrt(wbar^2 - c^2 kbar^2) (wbar, kbar the means: invariant of the pair);
  SR prediction Omega_SR = w' sqrt(1 - u^2/c^2);  ratio = Omega / Omega_SR.
For an exactly relativistic dispersion omega = sqrt(m^2 + c^2 k^2) the ratio is exactly 1 (the beat pattern is the
boost of a standing wave of frequency w').  A standing clock (K2 = -K1) has u = 0 and Omega = omega.
"""
from __future__ import annotations

import cmath
import json
import math

VERSION = "beat_clock_v1 1.0"


def quotient_field(events, steps, channel, sites):
    """q[t-1][j] for t = 1..steps at detector site j (absent record = 0).  ``events`` as from the decoder's
    ``read_log``: tuples (step, x, y, z, g, kind, quotient) or dicts with step/address/quotient."""
    index = {tuple(s): j for j, s in enumerate(sites)}
    q = [[0] * len(sites) for _ in range(steps)]
    for e in events:
        if isinstance(e, dict):
            t, (x, y, z, g), quot = e["step"], e["address"], e["quotient"]
        else:
            t, x, y, z, g, quot = e[0], e[1], e[2], e[3], e[4], e[6]
        if g != channel or not 1 <= t <= steps:
            continue
        j = index.get((x, y, z))
        if j is not None:
            q[t - 1][j] = quot
    return q


def project(q, sites, K):
    return [sum(row[j] * cmath.exp(-1j * (K[0] * s[0] + K[1] * s[1] + K[2] * s[2])) for j, s in enumerate(sites))
            for row in q]


def frequency(F):
    """Signed rate of a rotating projection, or the Prony rate of a standing one (see module docstring)."""
    norm = sum(abs(f) ** 2 for f in F) / len(F)
    if norm == 0:
        return None, "empty"
    cross = sum(F[t + 1] * F[t].conjugate() for t in range(len(F) - 1))
    if abs(cross.imag) / (len(F) - 1) > 1e-9 * norm:
        return -cmath.phase(cross), "rotating"
    tstar = max(range(len(F)), key=lambda t: abs(F[t]))
    rot = cmath.exp(-1j * cmath.phase(F[tstar]))
    s = [(f * rot).real for f in F]
    num = sum(s[t] * (s[t + 1] + s[t - 1]) for t in range(1, len(s) - 1))
    den = 2 * sum(s[t] ** 2 for t in range(1, len(s) - 1))
    return math.acos(max(-1.0, min(1.0, num / den))), "standing"


def beat_clock(events, side, steps, channel, clock, sites=None):
    """One declared clock: {'name', 'K1', 'K2', 'axis', 'c'} -> measured rates, u, Omega, w', SR ratio."""
    if sites is None:
        sites = [(x, y, z) for x in range(side) for y in range(side) for z in range(side)]
    q = quotient_field(events, steps, channel, sites)
    e = clock["axis"]
    norm_e = math.sqrt(sum(c * c for c in e))
    e = [c / norm_e for c in e]
    out = {"observer": VERSION, "name": clock.get("name"), "steps": steps, "channel": channel,
           "detector_sites": len(sites)}
    w, kinds = [], []
    for K in (clock["K1"], clock["K2"]):
        om, kind = frequency(project(q, sites, K))
        w.append(om)
        kinds.append(kind)
    out["omega"], out["projection"] = w, kinds
    if None in w:
        out["verdict"] = "no clock (an empty projection)"
        return out
    k1, k2 = (sum(K[i] * e[i] for i in range(3)) for K in (clock["K1"], clock["K2"]))
    c = clock["c"]
    u = (w[1] - w[0]) / (k2 - k1)
    Om = (k2 * w[0] - k1 * w[1]) / (k2 - k1)
    wbar, kbar = (w[0] + w[1]) / 2, (k1 + k2) / 2
    rest2 = wbar ** 2 - c ** 2 * kbar ** 2
    out.update({"axis_wavenumbers": [k1, k2], "u": u, "u_over_c": u / c, "Omega": Om,
                "rest_frequency": math.sqrt(rest2) if rest2 > 0 else None})
    if rest2 > 0 and abs(u) < c:
        sr = math.sqrt(rest2) * math.sqrt(1 - u * u / (c * c))
        out.update({"Omega_SR": sr, "ratio": Om / sr, "gamma": 1 / math.sqrt(1 - u * u / (c * c))})
    else:
        out["Omega_SR"] = None
        out["verdict"] = "pair is not timelike for this c (no SR rest frame)"
    return out


def run_declared(log_path, declaration):
    """Apply every clock of a declaration {'side','steps','channel','clocks':[...] , 'sites'?} to one official log."""
    from research.click_decoder_v1 import read_log
    events, _ = read_log(log_path)
    sites = declaration.get("sites")
    return {"observer": VERSION, "log": str(log_path),
            "clocks": [beat_clock(events, declaration["side"], declaration["steps"], declaration["channel"], ck,
                                  [tuple(s) for s in sites] if sites else None)
                       for ck in declaration["clocks"]]}


if __name__ == "__main__":
    import sys
    print(json.dumps(run_declared(sys.argv[1], json.loads(open(sys.argv[2]).read())), indent=1))
