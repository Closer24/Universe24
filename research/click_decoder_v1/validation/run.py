"""Validation of the click decoder on the pre-registered sets (validation/PREREGISTRATION.md, v1.0: 01:00 UTC).

    nice -n 10 python -m research.click_decoder_v1.validation.run logs     # official CLI logs, set A; layers, set C
    nice -n 10 python -m research.click_decoder_v1.validation.run score    # decode and score A, B, C
    ... run score --version 1.1 / run extra --version 1.1                   # the same with decoder v1.1
    ... run logs --sets A / run score --sets A [--version 1.1]              # set A only, from tracked data

Set A: catalog blocks of research/matter_light_blocks_v1 (declared signatures).
Set B: r08's wave-6 test set with r08's reference truth (validation/r08_reference.json).
Set C: the l = 0 layer (change observer minus native) of r08's wave-7 logs.
Logs, per-case reports and scores go to runs/click_decoder_v1/ (not versioned); nothing is written into the
package. score and extra compare their scores with the recorded files next to this file (results_v<version>.json,
results_v<version>_extra.json) and stop with an error if a recorded value is not reproduced.
The truth is used only here, never by the decoder.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

from research.click_decoder_v1 import decoder as D10, decoder_v11 as D11

D = D11 if "--version" in sys.argv and sys.argv[sys.argv.index("--version") + 1] == "1.1" else D10
FROZEN_FILE = {"1.0": "FROZEN.json", "1.1": "FROZEN_v1.1.json"}

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUNS = ROOT / "runs/click_decoder_v1"
CATALOG = ROOT / "research/matter_light_blocks_v1/catalog.json"
CATALOG_SHA = "465c080634253134cd027018560430eca4c2211f6699d68795abdb319a508263"     # registered file (8301320)
# The catalog's prose fields keep being edited (commit 17c7588 and later working-tree edits change only
# 'what' and 'status'). The pre-registered truth is fixed through a fingerprint of exactly the fields used
# here, computed from the registered file (validation/PREREGISTRATION.md, 01:31); the scorer refuses any catalog whose truth differs.
# Release 1.0.1: the published catalog grows by appending (commit dff39dc: 338 -> 346 entries). Set A is the
# registered first 338 entries; the fingerprint covers exactly that prefix, and appended entries are not scored.
REGISTERED_ENTRIES = 338
TRUTH_FIELDS = ("name", "group", "file", "file_sha256", "side", "steps", "heavy", "signature", "box_checks",
                "final_state_sha256")
TRUTH_SHA = "c3123352043c26124d10e9522d4666faa7948fc00819dae904151bba6c641c79"     # first 338 entries
OBS = ROOT / "runs/matter_light_v1/r08/observers"
DEV = {"I6_impulse", "D5_dimer", "mover_v2of6_sp_guide02", "fiber_x_packet", "atom_trap_d6", "ring16",
       "lamp_pmm_bg4_core10", "bigbang_C3_seed_pmm_bg4", "crystal_light_matter_L8", "crystal_light_and_matter",
       "diag_sheet"}
SET_C = ["chamber_L26", "trap_d6", "pair45", "HL22_dimer_monomer", "HL22_like_pair", "C3_lamp_L81",
         "flagship_v2", "dark_M4_far", "crystal_g17_36"]
RSS_LIMIT = 1.4e9


def _watchdog():
    def loop():
        while True:
            try:
                rss = int(next(l for l in open("/proc/self/status") if l.startswith("VmRSS")).split()[1]) * 1024
            except (OSError, StopIteration, ValueError):
                return
            if rss > RSS_LIMIT:
                print(f"watchdog: RSS {rss / 1e9:.2f} GB > 1.4 GB, stopping", flush=True)
                os._exit(3)
            time.sleep(0.5)
    threading.Thread(target=loop, daemon=True).start()


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------------ set A: selection and horizon (pre-registered)
def horizon(e):
    s, st = e["signature"], e["steps"]
    if e.get("box_checks"):
        return st
    if s.get("silent"):
        return max(st, 24) if "period" in s else st
    if "period" in s:
        return min(max(st, 4 * s["period"], 24), 480)
    return max(st, 4 * s["translation"]["period"], 24)


def catalog_cases():
    entries = json.loads(CATALOG.read_text())["entries"]
    registered = entries[:REGISTERED_ENTRIES]
    if len(registered) != REGISTERED_ENTRIES or _truth_sha(registered) != TRUTH_SHA:
        raise SystemExit(f"catalog.json: its first {REGISTERED_ENTRIES} entries differ from the pre-registered catalog "
                         f"(truth fingerprint {_truth_sha(registered)}, registered {TRUTH_SHA}); set A is not scored")
    if len(entries) > REGISTERED_ENTRIES:
        print(f"catalog.json: {len(entries)} entries; set A uses the registered first {REGISTERED_ENTRIES} "
              "(appended entries are not in set A)", file=sys.stderr, flush=True)
    out = []
    for e in registered:
        s = e["signature"]
        if e["heavy"] or not ("period" in s or "translation" in s or s.get("silent") or e.get("box_checks")):
            continue
        out.append({"name": e["name"], "group": e["group"], "file": "research/matter_light_blocks_v1/" + e["file"],
                    "side": e["side"], "H": horizon(e), "signature": s, "boxes": e.get("box_checks") or [],
                    "dev": e["name"] in DEV})
    return out


def _truth_sha(entries):
    blob = json.dumps([[e.get(k) for k in TRUTH_FIELDS] for e in entries], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


def logs(sets="ABC"):
    """Set-A logs with the official CLI; unless sets == "A", also set C's l = 0 layers (needs local observer logs)."""
    (RUNS / "setA").mkdir(parents=True, exist_ok=True)
    index = {}
    for c in catalog_cases():
        log = RUNS / "setA" / f"{c['name']}.jsonl"
        if not log.exists():
            t = time.time()
            r = subprocess.run(["nice", "-n", "10", sys.executable, "-m", "universe24", "--config", c["file"],
                                "--steps", str(c["H"]), "--events", str(log)], cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"{c['name']}: CLI failed: {r.stderr}")
            print(f"{c['name']:48s} H={c['H']:4d} {time.time() - t:6.1f}s", flush=True)
        index[c["name"]] = {"log": str(log.relative_to(ROOT)), "sha256": _sha(log), "H": c["H"],
                            "command": f"python -m universe24 --config {c['file']} --steps {c['H']} --events LOG"}
    (RUNS / "setA" / "index.json").write_text(json.dumps(index, indent=1) + "\n")
    if sets == "A":
        return
    (RUNS / "setC").mkdir(parents=True, exist_ok=True)
    for name in SET_C:
        out = RUNS / "setC" / f"{name}.L0.jsonl"
        if not out.exists():
            subprocess.run([sys.executable, "-m", "research.click_decoder_v1", "diff", str(OBS / f"{name}.C.jsonl"),
                            str(OBS / f"{name}.N.jsonl"), "--out", str(out)], cwd=ROOT, check=True)


# ------------------------------------------------------------------ helpers
def _by_step(events):
    g = defaultdict(list)
    for e in events:
        g[e[0]].append(e[1:])
    return {t: tuple(v) for t, v in g.items()}


def ref_click_period(events, P, H):
    """Smallest divisor d of P with events(t + d) == events(t) for all t in [1, H - d] (definitional)."""
    g = _by_step(events)
    for d in sorted(x for x in range(1, P + 1) if P % x == 0):
        if all(g.get(t) == g.get(t + d) for t in range(1, H - d + 1)):
            return d
    return None


def shift_holds(events, T, v, L, H):
    g = _by_step(events)
    for t in range(1, H - T + 1):
        a = sorted(((x + v[0]) % L, (y + v[1]) % L, (z + v[2]) % L, *r) for x, y, z, *r in g.get(t, ()))
        if tuple(a) != tuple(sorted(g.get(t + T, ()))):
            return False
    return True


def _velocities(rep):
    vs = [t["motion"]["velocity"] for t in rep["tracks"] if t["motion"]["exact"]]
    for s in rep["sources"]:
        vs += [m["velocity"] for m in s["internal_motion"].get("exact_velocities", [])]
    return [tuple(Fraction(x) for x in v) for v in vs]


def _decode(log, side, H, layer="native"):
    events, info = D.read_log(log)
    t = time.time()
    rep = D.decode(events, side=side, horizon=H, layer=layer, log_info=info)
    rep["input"]["decode_seconds"] = round(time.time() - t, 2)
    return events, rep


def _save(rep, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rep, sort_keys=True) + "\n")


def _track_counts(rep):
    """v1.0 writes "tracks": 0 (not {}) in the summary of an empty log; read both forms."""
    t = rep["summary"].get("tracks")
    return dict(t) if isinstance(t, dict) else {}


def _rate(num, den):
    return {"n": num, "of": den, "rate": round(num / den, 3) if den else None}


# ------------------------------------------------------------------ set A scoring
def score_a(tag):
    rows = []
    for c in catalog_cases():
        log = RUNS / "setA" / f"{c['name']}.jsonl"
        events, rep = _decode(log, c["side"], c["H"])
        _save(rep, RUNS / tag / "setA" / f"{c['name']}.json")
        s, H, L = c["signature"], c["H"], c["side"]
        row = {"name": c["name"], "group": c["group"], "dev": c["dev"], "H": H, "events": len(events),
               "log_sha256": rep["input"]["log"]["sha256"], "seconds": rep["input"]["decode_seconds"],
               "sources": [[x["period"], x["n_sites"], x["composite"], x["lamp"]] for x in rep["sources"]],
               "tracks": _track_counts(rep), "created": len(rep["summary"].get("created", [])),
               "explained": rep["summary"].get("explained_fraction")}
        periods = [x["period"] for x in rep["sources"]]
        if "period" in s and not s.get("silent"):
            P = s["period"]
            row["P"] = P
            row["identifiable"] = H >= 3 * P
            row["p_ref"] = ref_click_period(events, P, H)
            row["decoded_lcm"] = D._lcm(periods) if periods else None
            row["period_exact"] = row["decoded_lcm"] == row["p_ref"]
            row["periods_divide_P"] = [P % p == 0 for p in periods]
            if "clicks_per_period" in s:
                row["cpp_declared"] = s["clicks_per_period"]
                row["cpp_decoded"] = sum(x["clicks_per_period"] * P // x["period"] for x in rep["sources"]
                                         if P % x["period"] == 0)
            if "kinds_per_period" in s:
                k = Counter()
                for x in rep["sources"]:
                    if P % x["period"] == 0:
                        k.update({kk: v * P // x["period"] for kk, v in x["kinds_per_period"].items()})
                row["kpp_declared"] = {kk: v for kk, v in s["kinds_per_period"].items() if v}
                row["kpp_decoded"] = {kk: v for kk, v in k.items() if v}
        if "translation" in s:
            T, v = s["translation"]["period"], s["translation"]["shift"]
            truth = tuple(Fraction(x, T) for x in v)
            vs = _velocities(rep)
            row["v_truth"] = [str(x) for x in truth]
            row["shift_holds_in_log"] = shift_holds(events, T, v, L, H)
            row["v_found"] = truth in vs
            row["v_exact_reported"] = [[str(x) for x in w] for w in vs]
            row["v_exact_correct"] = sum(1 for w in vs if w == truth)
            l1 = sum(abs(x) for x in truth)
            row["lm_truth"] = "light" if l1 == 1 else "matter"
            cls = [t["class"] for t in rep["tracks"] if t["motion"]["exact"]
                   and tuple(Fraction(x) for x in t["motion"]["velocity"]) == truth]
            cls += [m["class"] for x in rep["sources"] for m in x["internal_motion"].get("exact_velocities", [])
                    if tuple(Fraction(y) for y in m["velocity"]) == truth]
            row["lm_decoded"] = cls[0] if cls else None
        if s.get("silent"):
            row["silent_ok"] = not rep["sources"] and not rep["tracks"]
        for b in c["boxes"]:
            cen = D.Torus(L).centroid([tuple(x) for x in b["sites"]])
            near = [x for x in rep["sources"] if D.Torus(L).cheb(x["centroid"], cen) <= 4]
            if b["type"] == "periodic":
                ok = any(x["period"] == b["period"] and x["birth"]["created"] for x in near)
                per = any(x["period"] == b["period"] for x in near)
            else:
                ok = any(x["channel_period_ratio"] == 2 for x in near)      # the registered v1.0 criterion
                per = any((x.get("c_image") or {}).get("lap") == b["lap"] for x in near)   # v1.1: C-image lap
            row.setdefault("boxes", []).append({"label": b["label"], "type": b["type"], "ok": ok,
                                                "period_found": per,
                                                "near": [[x["period"], x["period_channels_ignored"],
                                                          x["birth"]["created"], x["birth"]["t"]] for x in near]})
        rows.append(row)
        print(f"A {c['name']:48s} {rep['input']['decode_seconds']:6.1f}s", flush=True)
    m = {}
    per = [r for r in rows if "P" in r]
    ident = [r for r in per if r["identifiable"]]
    m["A-P recall (lcm == p_ref, identifiable)"] = _rate(sum(r["period_exact"] for r in ident), len(ident))
    m["A-P recall (lcm == P, identifiable)"] = _rate(sum(r["decoded_lcm"] == r["P"] for r in ident), len(ident))
    m["A-P p_ref == P (clicks show the full state period)"] = _rate(sum(r["p_ref"] == r["P"] for r in ident), len(ident))
    m["A-P not identifiable (H < 3P), counted as misses"] = _rate(
        sum(r["period_exact"] for r in per if not r["identifiable"]), len(per) - len(ident))
    m["A-P recall over all period blocks"] = _rate(sum(r["period_exact"] for r in per), len(per))
    pd = [x for r in ident for x in r["periods_divide_P"]]
    m["A-P precision (source periods dividing P)"] = _rate(sum(pd), len(pd))
    m["A-P coverage (mean explained fraction)"] = round(sum(r["explained"] or 0 for r in ident) / len(ident), 4) if ident else None
    tr = [r for r in rows if "v_truth" in r]
    m["A-T recall (exact velocity == shift/T)"] = _rate(sum(r["v_found"] for r in tr), len(tr))
    m["A-T precision (exact velocities equal to shift/T)"] = _rate(sum(r["v_exact_correct"] for r in tr),
                                                                   sum(len(r["v_exact_reported"]) for r in tr))
    m["A-T log obeys the declared shift"] = _rate(sum(r["shift_holds_in_log"] for r in tr), len(tr))
    m["A-LM light/matter class correct"] = _rate(sum(r["lm_decoded"] == r["lm_truth"] for r in tr), len(tr))
    sil = [r for r in rows if "silent_ok" in r]
    m["A-S silent blocks with zero objects"] = _rate(sum(r["silent_ok"] for r in sil), len(sil))
    k1 = [r for r in rows if "cpp_declared" in r and r.get("identifiable")]
    m["A-K clicks per period reproduced"] = _rate(sum(r["cpp_declared"] == r["cpp_decoded"] for r in k1), len(k1))
    k2 = [r for r in rows if "kpp_declared" in r and r.get("identifiable")]
    m["A-K kinds per period reproduced"] = _rate(sum(r["kpp_declared"] == r["kpp_decoded"] for r in k2), len(k2))
    bx = [b for r in rows for b in r.get("boxes", [])]
    for typ in ("periodic", "c_image"):
        sel = [b for b in bx if b["type"] == typ]
        m[f"A-B box {typ}: found as declared"] = _rate(sum(b["ok"] for b in sel), len(sel))
    m["A-B box c_image: C-image lap == declared lap (v1.1 test)"] = _rate(
        sum(b["period_found"] for b in bx if b["type"] == "c_image"), sum(1 for b in bx if b["type"] == "c_image"))
    m["A-B box periodic: period found (created or not)"] = _rate(
        sum(b["period_found"] for b in bx if b["type"] == "periodic"), sum(1 for b in bx if b["type"] == "periodic"))
    for sub, f in (("dev (seen)", lambda r: r["dev"]), ("held-out", lambda r: not r["dev"])):
        ii = [r for r in ident if f(r)]
        tt = [r for r in tr if f(r)]
        m[f"A-P recall, {sub}"] = _rate(sum(r["period_exact"] for r in ii), len(ii))
        m[f"A-T recall, {sub}"] = _rate(sum(r["v_found"] for r in tt), len(tt))
    # post-hoc view (the catalog README notes 10 groups of repeated preparations): distinct logs only
    seen, distinct = set(), []
    for r in rows:
        if r["log_sha256"] not in seen:
            seen.add(r["log_sha256"])
            distinct.append(r)
    di = [r for r in distinct if "P" in r and r["identifiable"]]
    dt = [r for r in distinct if "v_truth" in r]
    m["post-hoc: distinct logs"] = len(distinct)
    m["post-hoc: A-P recall over distinct logs (identifiable)"] = _rate(sum(r["period_exact"] for r in di), len(di))
    m["post-hoc: A-T recall over distinct logs"] = _rate(sum(r["v_found"] for r in dt), len(dt))
    groups = defaultdict(lambda: Counter())
    for r in rows:
        g = groups[r["group"]]
        g["blocks"] += 1
        g["with sources"] += bool(r["sources"])
        g["composite sources"] += sum(1 for x in r["sources"] if x[2])
        g["lamps"] += sum(1 for x in r["sources"] if x[3])
        g["light tracks"] += r["tracks"].get("light", 0) + r["tracks"].get("front", 0)
        g["matter tracks"] += r["tracks"].get("matter", 0)
        g["created objects"] += r["created"]
    return {"metrics": m, "by_group": {k: dict(v) for k, v in sorted(groups.items())}, "cases": rows}


# ------------------------------------------------------------------ sets B and C: object-level matching (r08's rule)
def _cheb(p, q, L):
    return max(min(abs(p[i] - q[i]) % L, L - abs(p[i] - q[i]) % L) for i in range(3))


def _tpos(o, t):
    return [o["birth_centroid"][i] + o["velocity"][i] * (t - o["start"]) for i in range(3)]


def _dpos(a, t):
    if a["path"] is None:
        return a["at"]
    return min(a["path"], key=lambda p: abs(p[0] - t))[1:]


def _match(T, A, L):
    cand = []
    for i, o in enumerate(T):
        for j, a in enumerate(A):
            lo, hi = max(o["start"], a["t0"]), min(o["end"], a["t1"])
            short = min(o["end"] - o["start"] + 1, a["t1"] - a["t0"] + 1)
            if short <= 0 or hi - lo + 1 < 0.5 * short:
                continue
            d = _cheb(_tpos(o, (lo + hi) // 2), _dpos(a, (lo + hi) // 2), L)
            if d <= 4:
                cand.append((o["dark"], d, i, j))
    cand.sort()
    ti, aj, pairs = set(), set(), []
    for _, d, i, j in cand:
        if i not in ti and j not in aj:
            ti.add(i)
            aj.add(j)
            pairs.append((i, j))
    return pairs


def _objects(rep):
    out = []
    for t in rep["tracks"]:
        fam = {"light": "light", "front": "light", "matter": "matter"}.get(t["class"])
        out.append({"id": t["id"], "family": fam, "t0": t["t_start"], "t1": t["t_end"], "path": t["path"],
                    "at": None, "bound": False, "created": t["birth"]["created"]})
    for s in rep["sources"]:
        out.append({"id": s["id"], "family": "source", "t0": s["window"][0], "t1": s["window"][1], "path": None,
                    "at": s["centroid"], "bound": s["composite"], "created": s["birth"]["created"],
                    "period": s["period"]})
    return out


FAMS = ("light", "matter", "source", "bound", "created")


def _score_case(truth, rep, L, fams=FAMS):
    A = _objects(rep)
    per = {}
    for fam in fams:
        if fam == "bound":
            T, AA = [o for o in truth if o["bound"]], [a for a in A if a["bound"]]
        elif fam == "created":
            T, AA = [o for o in truth if o["created"]], [a for a in A if a["created"]]
        else:
            T, AA = [o for o in truth if o["family"] == fam], [a for a in A if a["family"] == fam]
        pairs = _match(T, AA, L)
        nd = sum(o["dark"] for o in T)
        tpd = sum(1 for i, _ in pairs if T[i]["dark"])
        per[fam] = {"truth": len(T), "truth_dark": nd, "found": len(AA), "tp": len(pairs), "tp_dark": tpd,
                    "fp": len(AA) - len(pairs), "fn": len(T) - len(pairs)}
        if fam == "source":
            per[fam]["periods"] = [[T[i]["what"], T[i]["period"], AA[j]["period"]] for i, j in pairs if T[i]["period"]]
    return per


def _totals(rows, fams=FAMS):
    tot = {}
    for fam in fams:
        d = Counter()
        for r in rows:
            d.update({k: v for k, v in r["per_family"][fam].items() if isinstance(v, int)})
        vis = d["truth"] - d["truth_dark"]
        tot[fam] = dict(d) | {"precision": round(d["tp"] / (d["tp"] + d["fp"]), 3) if d["tp"] + d["fp"] else None,
                              "recall_all": round(d["tp"] / d["truth"], 3) if d["truth"] else None,
                              "recall_visible": round((d["tp"] - d["tp_dark"]) / vis, 3) if vis else None}
    return tot


def score_b(tag):
    ref = json.loads((HERE / "r08_reference.json").read_text())
    rows, extra = [], []
    for c in ref["cases"]:
        log = ROOT / c["log"]
        if _sha(log) != c["log_sha256"]:
            raise SystemExit(f"{c['case']}: log differs from the snapshot")
        events, rep = _decode(log, c["side"], c["horizon"])
        _save(rep, RUNS / tag / "setB" / f"{c['case']}.json")
        row = {"case": c["case"], "events": len(events), "per_family": _score_case(c["objects"], rep, c["side"]),
               "decoded": {"sources": [[s["id"], s["period"], s["centroid"], s["composite"], s["lamp"],
                                        s["birth"]["created"]] for s in rep["sources"]],
                           "tracks": _track_counts(rep), "created": rep["summary"].get("created", [])},
               "seconds": rep["input"]["decode_seconds"]}
        (rows if c["declared"] else extra).append(row)
        print(f"B {c['case']:24s} {rep['input']['decode_seconds']:6.1f}s", flush=True)
    return {"totals": _totals(rows), "cases": rows, "extra_cases": extra}


def score_c(tag):
    ref = {c["case"]: c for c in json.loads((HERE / "r08_reference.json").read_text())["cases"]}
    rows = []
    for name in SET_C:
        c = ref[name]
        log = RUNS / "setC" / f"{name}.L0.jsonl"
        events, rep = _decode(log, c["side"], c["horizon"], layer="change_l0")
        _save(rep, RUNS / tag / "setC" / f"{name}.json")
        rest = [o for o in c["objects"] if o["at_rest"]]
        per = _score_case(rest, rep, c["side"], fams=("source",))
        A = [a for a in _objects(rep) if a["family"] == "source"]
        pairs = _match(rest, A, c["side"])
        dark = [o for o in rest if o["dark"]]
        rows.append({"case": name, "events": len(events), "per_family": per,
                     "dark_found": sum(1 for i, _ in pairs if rest[i]["dark"]), "dark_total": len(dark),
                     "sources": [[s["id"], s["period"], s["centroid"]] for s in rep["sources"]],
                     "seconds": rep["input"]["decode_seconds"]})
        print(f"C {name:24s} {rep['input']['decode_seconds']:6.1f}s", flush=True)
    tot = _totals(rows, fams=("source",))
    tot["dark_recall"] = _rate(sum(r["dark_found"] for r in rows), sum(r["dark_total"] for r in rows))
    return {"totals": tot, "cases": rows}


def score(sets="ABC"):
    _watchdog()
    tag = f"v{D.VERSION}"
    ff = HERE.parent / FROZEN_FILE[D.VERSION]
    frozen = json.loads(ff.read_text()) if ff.exists() else None
    now = D.code_fingerprint()
    if frozen and frozen.get("version") == D.VERSION and frozen.get("code_sha256") != now:
        raise SystemExit("decoder files differ from FROZEN.json for this version")
    t = time.time()
    out = {"decoder": {"name": D.NAME, "version": D.VERSION, "code_sha256": now},
           "frozen": frozen, "catalog_registered_sha256": CATALOG_SHA, "catalog_file_sha256": _sha(CATALOG),
           "catalog_truth_sha256": TRUTH_SHA,
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    out["set_A"] = score_a(tag)
    if sets != "A":
        out["set_B"] = score_b(tag)
        out["set_C"] = score_c(tag)
    print(json.dumps({k[4:]: out[k]["metrics" if k == "set_A" else "totals"] for k in out if k.startswith("set_")},
                     indent=1))
    _record(out, f"results_v{D.VERSION}.json", "results_setA.json" if sets == "A" else f"results_v{D.VERSION}.json", t)


def _no_timing(x):
    if isinstance(x, dict):
        return {k: _no_timing(v) for k, v in x.items() if k != "seconds"}
    if isinstance(x, list):
        return [_no_timing(v) for v in x]
    return x


def _reproduces(cur, rec):
    """True if every recorded value is reproduced: dicts on the recorded keys, lists element by element, timing
    ignored (the scorer gained fields after v1.0's results were recorded)."""
    if isinstance(rec, dict):
        return isinstance(cur, dict) and all(k == "seconds" or (k in cur and _reproduces(cur[k], v))
                                             for k, v in rec.items())
    if isinstance(rec, list):
        return isinstance(cur, list) and len(cur) == len(rec) and all(_reproduces(c, r) for c, r in zip(cur, rec))
    return cur == rec


def _record(out, recorded, written, t):
    """Write the scores under runs/click_decoder_v1/v<version>/ (never into the package) and compare each set with
    the recorded file validation/<recorded>; stop with an error if a recorded value is not reproduced."""
    ref = json.loads((HERE / recorded).read_text())
    check = {k: {"equal": _no_timing(out[k]) == _no_timing(ref.get(k)),
                 "reproduces_recorded": _reproduces(out[k], ref.get(k))} for k in sorted(out) if k.startswith("set_")}
    if "set_A" in out:
        check["set_A"]["metrics_not_recorded"] = sorted(set(out["set_A"]["metrics"]) - set(ref["set_A"]["metrics"]))
    out["recorded_check"] = {"recorded": f"validation/{recorded}", "sets": check}
    out["seconds"] = round(time.time() - t, 1)
    path = RUNS / f"v{D.VERSION}" / written
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"recorded_check": out["recorded_check"], "written": str(path.relative_to(ROOT))}, indent=1))
    if not all(c["reproduces_recorded"] for c in check.values()):
        raise SystemExit(f"scores differ from validation/{recorded}")


SET_D = {6: "8ec29c6cea7485ff4fa08056296bd85aebc23b05357a3ecee92487dbeb239392",
         10: "dba3e1d5c61e42d563f2c18f1ac9956d1b1bbd395aba0060c509bad248747c64",
         14: "dcc43ca7e99d9755169bace304e8b03e5eb2dda23e7d34e4203ded6e0988c588"}


def extra():
    """Held-out set D (pre-registered 01:40) and a post-hoc coverage diagnostic for set C."""
    _watchdog()
    t = time.time()
    tag, out = f"v{D.VERSION}", {"decoder": {"version": D.VERSION, "code_sha256": D.code_fingerprint()}}
    rows = []
    for d, sha in SET_D.items():
        log = ROOT / f"runs/matter_light_v1/r08/clicklogs/spectro_d{d}_atom_alone.jsonl"
        summ = json.loads(log.with_name(log.name.replace(".jsonl", ".summary.json")).read_text())
        if _sha(log) != sha:
            raise SystemExit(f"set D log d={d} differs from the registered hash")
        events, rep = _decode(log, summ["side"], summ["completed_steps"])
        _save(rep, RUNS / tag / "setD" / f"spectro_d{d}.json")
        hit = [s for s in rep["sources"] if s["period"] == 2 * d + 4]
        rows.append({"d": d, "truth_period": 2 * d + 4, "found_period": bool(hit),
                     "found_composite": any(s["composite"] for s in hit),
                     "sources": [[s["id"], s["period"], s["n_sites"], s["composite"], s["composite_reason"],
                                  s["internal_motion"]["kind"], s["extent"]] for s in rep["sources"]],
                     "tracks": _track_counts(rep)})
    out["set_D"] = {"pre_registered": "validation/PREREGISTRATION.md (set D, 01:40)", "cases": rows,
                    "period": _rate(sum(r["found_period"] for r in rows), len(rows)),
                    "period_and_composite": _rate(sum(r["found_composite"] for r in rows), len(rows))}
    # post hoc: a dark object at rest counts as covered if some l = 0 source has a site within 1 of it
    ref = {c["case"]: c for c in json.loads((HERE / "r08_reference.json").read_text())["cases"]}
    cov = []
    for name in SET_C:
        rep = json.loads((RUNS / tag / "setC" / f"{name}.json").read_text())
        L = ref[name]["side"]
        sites = [tuple(x) for s in rep["sources"] for x in s["sites"]]
        for o in ref[name]["objects"]:
            if o["at_rest"] and o["dark"]:
                c = [int(round(x)) % L for x in o["birth_centroid"]]
                cov.append({"case": name, "what": o["what"],
                            "covered": any(_cheb(c, q, L) <= max(1, o["own_radius"]) for q in sites)})
    out["set_C_coverage_posthoc"] = {"rule": "dark object at rest covered by some l = 0 source site within "
                                             "Chebyshev max(1, own radius) (many-to-one)",
                                     "covered": _rate(sum(c["covered"] for c in cov), len(cov)),
                                     "not_covered": [c for c in cov if not c["covered"]]}
    print(json.dumps({"D": out["set_D"], "C_cov": out["set_C_coverage_posthoc"]["covered"]}, indent=1))
    _record(out, f"results_v{D.VERSION}_extra.json", f"results_v{D.VERSION}_extra.json", t)


if __name__ == "__main__":
    SETS = sys.argv[sys.argv.index("--sets") + 1] if "--sets" in sys.argv else "ABC"
    if SETS not in ("A", "ABC") or (SETS == "A" and sys.argv[1] == "extra"):
        raise SystemExit("--sets: use --sets A with logs or score (sets B, C and D need the program's local logs)")
    {"logs": lambda: logs(SETS), "score": lambda: score(SETS), "extra": extra}[sys.argv[1]]()   # also: --version 1.1
