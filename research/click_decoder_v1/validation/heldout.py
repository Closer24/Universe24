"""Held-out targets of decoder v1.1 (pre-registered 01:53-02:03 UTC, before v1.1 existed or ran on them).

    nice -n 10 python -m research.click_decoder_v1.validation.heldout

H1 r06b flagship v3 (glider split, spin ring as a C-image source), H2 r15 D2J (2-click detector
events, light turning back), H3 r14 peak-arrival light (layer equality, c-light), H4 set A's c-image
box, H5/H7 planar Big Bang and planar glider (E05), H6 E01, H8 E06, H9 r24's quotient field.
Every target is decoded with v1.0 and v1.1. Logs that are not already in the program record are made
with the official CLI; their SHA-256 are checked against the manifests where these record them. The
truth comes from the owners' reports and manifests and is used only here. Writes heldout_v1.1.json.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

from research.click_decoder_v1 import decoder as D10, decoder_v11 as D11, layers
from research.click_decoder_v1.validation.run import _watchdog

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "runs/click_decoder_v1/heldout"
DEC = {"1.0": D10, "1.1": D11}
EXP = ROOT / "research/matter_light_experiments_v1"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cli(init, steps, name):
    log = OUT / "logs" / f"{name}.jsonl"
    if not log.exists():
        log.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["nice", "-n", "10", sys.executable, "-m", "universe24", "--config", str(init), "--steps",
                        str(steps), "--events", str(log)], cwd=ROOT, check=True, capture_output=True)
    return log


def both(log, side, horizon, **kw):
    out = {}
    for v, M in DEC.items():
        ev, info = M.read_log(log)
        extra = {k: x for k, x in kw.items() if v == "1.1" or k == "detectors"}
        t = time.time()
        out[v] = M.decode(ev, side=side, horizon=horizon, log_info=info, **extra)
        out[v]["input"]["decode_seconds"] = round(time.time() - t, 2)
    return out


def cheb(p, q, L):
    return max(min(abs(p[i] - q[i]) % L, L - abs(p[i] - q[i]) % L) for i in range(3))


def exact_tracks(rep, v):
    v = tuple(Fraction(x) for x in v)
    return [t for t in rep["tracks"] if t["motion"]["exact"] and tuple(Fraction(x) for x in t["motion"]["velocity"]) == v]


def exact_set(rep):
    vs = {tuple(t["motion"]["velocity"]) for t in rep["tracks"] if t["motion"]["exact"]}
    for s in rep["sources"]:
        vs |= {tuple(m["velocity"]) for m in s["internal_motion"].get("exact_velocities", [])}
    return vs


# ------------------------------------------------------------------ H1 r06b
def h1():
    logs, prep = ROOT / "runs/matter_light_v1/r06b/logs", ROOT / "research/matter_light_v1/r06b/preparations"
    laps_truth = {160: 6, 320: 7, 256: 8, 512: 8}
    rows = []
    for b in ("skeleton_main_L160", "skeleton_main_L256", "skeleton_main_L320", "skeleton_main_L512",
              "twins_far_main_L256", "twins_far_main_L512", "skeleton_no_ring_L160"):
        init = json.loads((prep / f"flagship_v3_{b}.json").read_text())
        L, T = init["side"], init["steps"]
        reps = both(logs / f"{b}.jsonl", L, T)
        ring = (15.5, -20 % L, 5)
        row = {"board": b, "side": L, "horizon": T, "log_sha256": sha(logs / f"{b}.jsonl")}
        for v, rep in reps.items():
            r = {}
            if b.startswith("skeleton_main"):
                for sgn, key in ((1, "plus_y"), (-1, "minus_y")):
                    hits = [t for t in exact_tracks(rep, (0, Fraction(sgn, 3), 0))
                            if t["birth"]["t"] <= 45 and cheb(t["birth"]["centroid"], (13, 0, 3), L) <= 4]
                    r[key] = [[t["id"], t["t_start"], t["t_end"], t["birth"]["origin"], t["birth"]["parent"]] for t in hits]
                    first = sorted((t for t in rep["tracks"] if t["motion"]["exact"] and t["motion"]["velocity"] ==
                                    ["0", str(Fraction(sgn, 3)), "0"]), key=lambda t: t["t_start"])
                    r[key + "_first_exact_track"] = [first[0]["t_start"], first[0]["birth"]["centroid"]] if first else None
                r["Q1_pass"] = bool(r["plus_y"] and r["minus_y"])
            near = [s for s in rep["sources"] if cheb(s["centroid"], ring, L) <= 6]
            r["ring_sources"] = [[s["id"], s["period"], s.get("period_channels_ignored"), s.get("c_image"),
                                  s["birth"]["t"], s["birth"]["created"]] for s in near]
            ci = [s["c_image"] for s in near if s.get("c_image") and s["c_image"]["lap"] == 18]
            r["Q2_c_image_lap18"] = bool(ci)
            r["laps_verified"] = max((c["laps_verified"] for c in ci), default=None)
            r["v1_0_style_period36_ratio2"] = any(s["period"] == 36 and s.get("channel_period_ratio") == 2 for s in near)
            row[v] = r
        row["laps_truth"] = None if "no_ring" in b else laps_truth[L] if b.startswith("skeleton") else ">= 8 (T = 300)"
        rows.append(row)
        print("H1", b, {v: (row[v].get("Q1_pass"), row[v]["Q2_c_image_lap18"], row[v]["laps_verified"]) for v in DEC},
              flush=True)
    return rows


# ------------------------------------------------------------------ H2 r15
def h2():
    from research.matter_light_v1.r15 import d2j as R15
    res = json.loads((ROOT / "research/matter_light_v1/r15/d2j_result.json").read_text())
    dev = R15.device()
    rows = []
    for row in res["rows"]:
        log, tq, steps = ROOT / row["log"], row["t_q"], row["steps"]
        wins = {"approval": [15, 28], "quantum": [tq - 1, tq + 12], "afterpulse": [tq + 13, tq + 60]}
        out = {"log": row["log"], "log_sha256": sha(log), "approval": row["approval"], "lambda": row["lambda"],
               "cores": row["cores"], "windows": {}}
        for w, win in wins.items():
            spec = R15.det_spec(dev, win)
            p = OUT / "r15" / f"{Path(row['log']).stem}.{w}.detectors.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(spec, sort_keys=True) + "\n")
            reps = both(log, dev.L, steps, detectors=spec)
            got = {}
            for v, rep in reps.items():
                c = rep["correlations"]["detectors"]
                got[v] = {arm: {"clicks": sum(d["clicks"] for k, d in c.items() if k.startswith(arm + "_")),
                                "kinds": {k: sum(d["kinds"].get(k, 0) for kk, d in c.items() if kk.startswith(arm + "_"))
                                          for k in ("C0", "C1", "C2")},
                                "first_click": min([d["first_click"] for k, d in c.items() if k.startswith(arm + "_")
                                                    and d["first_click"] is not None], default=None)}
                          for arm in ("A", "B")}
            truth = row[f"{w}_window"]
            out["windows"][w] = {"truth": truth, "v1.0": got["1.0"], "v1.1": got["1.1"],
                                 "equal_v1.0": got["1.0"] == truth, "equal_v1.1": got["1.1"] == truth}
        if row["approval"] and row["lambda"] == 0 and row["cores"]:
            reps = both(log, dev.L, steps)
            for v, rep in reps.items():
                back = [t for t in exact_tracks(rep, (-1, 0, 0)) if 45 <= t["birth"]["t"] <= 49
                        and cheb(t["birth"]["centroid"], (90, 100, 99), dev.L) <= 3]
                down = [t for t in exact_tracks(rep, (0, -1, 0)) if 89 <= t["birth"]["t"] <= 93
                        and cheb(t["birth"]["centroid"], (70, 120, 99), dev.L) <= 3]
                out[f"turning_back_{v}"] = {
                    "minus_x": [[t["id"], t["birth"]["t"], t["birth"]["centroid"], t["birth"]["origin"], t["t_end"],
                                 t["end"]] for t in back],
                    "minus_y": [[t["id"], t["birth"]["t"], t["birth"]["centroid"], t["birth"]["origin"]] for t in down],
                    "pass": bool([t for t in back if t["birth"]["origin"] == "emitted"]) and bool(down)}
        rows.append(out)
        print("H2", Path(row["log"]).stem, {w: (x["equal_v1.0"], x["equal_v1.1"]) for w, x in out["windows"].items()},
              out.get("turning_back_1.1", {}).get("pass"), flush=True)
    return rows


# ------------------------------------------------------------------ H3 r14
def h3():
    r14 = ROOT / "runs/matter_light_v1/r14"
    c = 1 / math.sqrt(3)
    rows = []
    for kind, names in (("staircase", [f"w2_v2_chain_{d}_amp1e+06_staircase" for d in ("100", "110", "111")]),
                        ("line", [f"w2_v2_chain_{d}_amp1e+06_line" for d in ("100", "110", "111")]),
                        ("native_line", [f"w2_v1_native_{d}_L16_line" for d in ("100", "110", "111")])):
        for name in names:
            src = r14 / f"{name}.clicks.jsonl"
            ev, _ = D11.read_log(src)
            peak = OUT / "r14" / f"{name}.peak.jsonl"
            if not peak.exists():
                peak.parent.mkdir(parents=True, exist_ok=True)
                layers.write_peak_arrival(ev, peak, w=D11.load_config()["peak_half_window"])
            row = {"name": name, "kind": kind, "source_sha256": sha(src), "peak_sha256": sha(peak)}
            ref = r14 / f"{name}.peak_arrival_v1.jsonl"
            if ref.exists():
                mine = [json.loads(x) for x in peak.read_text().splitlines()]
                theirs = [json.loads(x) for x in ref.read_text().splitlines() if x.strip()]
                row["equal_to_r14_layer"] = mine == theirs
                row["records"] = [len(mine), len(theirs)]
            side = 16 if kind == "native_line" else 1600
            H = max(e[0] for e in ev)
            reps = both(peak, side, H, c=c)
            for v, rep in reps.items():
                main = max(rep["tracks"], key=lambda t: (t["clicks"], -t["t_start"]), default=None)
                row[v] = {"main_class": main and main["class"], "main_euclid": main and main["motion"]["euclid_speed"],
                          "main_exact": main and main["motion"]["exact"], "tracks": rep["summary"]["tracks"],
                          "c_light": rep["summary"].get("c_light"),
                          "plane_wave": (rep.get("arrival_map") or {}).get("plane_wave")}
            rows.append(row)
            print("H3", name, row.get("equal_to_r14_layer"), {v: (row[v]["main_class"], row[v]["main_euclid"]) for v in DEC},
                  flush=True)
    truth = {"staircase": [0.57602, 0.57669, 0.57735], "line": [0.57602, 0.57669 / math.sqrt(0.5), 1.0]}
    summary = {}
    for kind, tv in truth.items():
        sel = [r for r in rows if r["kind"] == kind]
        for v in DEC:
            sp = [r[v]["main_euclid"] for r in sel]
            within = [abs(s - t) <= 0.01 * t if s else False for s, t in zip(sp, tv)]
            summary[f"{kind} {v}"] = {"speeds": sp, "truth": tv, "within_1pct": within,
                                       "c_light_class": [r[v]["main_class"] == "c-light" for r in sel],
                                       "spread": (max(sp) / min(sp) - 1) if all(sp) else None}
    return {"rows": rows, "summary": summary,
            "layer_equal_3of3": all(r.get("equal_to_r14_layer") for r in rows if r["kind"] == "staircase")}


# ------------------------------------------------------------------ H5/H7 planar, H6 E01, H8 E06
def manifest(eid):
    return json.loads((EXP / eid / "experiment.json").read_text())


def run_path(eid, r):
    if r.get("block_file"):
        return ROOT / r["block_file"]
    if r.get("init"):
        return EXP / eid / r["init"]
    return ROOT / r["source"].split(" ")[0]


def manifest_reps(eid):
    m = manifest(eid)
    out = {}
    for r in m["runs"]:
        init = run_path(eid, r)
        log = cli(init, r["steps"], f"{eid}.{r['name']}")
        side = json.loads(init.read_text())["side"]
        out[r["name"]] = {"log_sha256": sha(log), "manifest_log_sha256": r.get("log_sha256"),
                          "log_matches_manifest": sha(log) == r.get("log_sha256"), "side": side, "steps": r["steps"],
                          "reps": both(log, side, r["steps"])}
        print("  ", eid, r["name"], out[r["name"]]["log_matches_manifest"], flush=True)
    return out


def periods(rep):
    return sorted(s["period"] for s in rep["sources"])


def h_planar():
    rows = {}
    init = ROOT / "research/matter_light_blocks_v1/blocks/seeds_big_bang/planar_bigbang_L16.json"
    for steps in (14, 18):
        log = cli(init, steps, f"planar_bigbang_L16_h{steps}")
        reps = both(log, 16, steps)
        rows[f"planar_bigbang_L16_h{steps}"] = {
            "log_sha256": sha(log),
            **{v: {"plus": [t["id"] for t in exact_tracks(rep, (Fraction(1, 2), 0, 0))],
                   "minus": [t["id"] for t in exact_tracks(rep, (Fraction(-1, 2), 0, 0))],
                   "tracks": rep["summary"]["tracks"], "exact_speeds": rep["summary"]["exact_speeds"],
                   "classes": [[t["class"], t["motion"]["velocity"], t["motion"]["exact"], t["t_start"]] for t in rep["tracks"]],
                   "seconds": rep["input"]["decode_seconds"]} for v, rep in reps.items()}}
        for v in DEC:
            rr = rows[f"planar_bigbang_L16_h{steps}"][v]
            rr["pass"] = bool(rr["plus"] and rr["minus"])
        print("H5", steps, {v: rows[f"planar_bigbang_L16_h{steps}"][v]["pass"] for v in DEC}, flush=True)
    return rows


def h_e05():
    runs = manifest_reps("E05_planar_bigbang")
    res = {}
    for v in DEC:
        bb, pg = runs["planar_bigbang_L16"]["reps"][v], runs["planar_glider_L12"]["reps"][v]
        res[v] = {"E05-1": bool(exact_tracks(bb, (Fraction(1, 2), 0, 0)) and exact_tracks(bb, (Fraction(-1, 2), 0, 0))),
                  "E05-2": bool(exact_tracks(pg, (Fraction(-1, 2), 0, 0))) or ("-1/2", "0", "0") in exact_set(pg),
                  "E05-3": [pg["kinds"]["C0"], pg["kinds"]["C1"]] == [0, 0]}
    return {"logs": {k: {x: r[x] for x in ("log_sha256", "log_matches_manifest")} for k, r in runs.items()}, "checks": res}


def h_e01():
    runs = manifest_reps("E01_local_atom_twins")
    res = {}
    for v in DEC:
        R = {k: r["reps"][v] for k, r in runs.items()}
        a100, a200 = R["d1_atom_L100"], R["d1_atom_L200"]
        s100 = [s for s in a100["sources"] if s["period"] == 20]
        s200 = [s for s in a200["sources"] if s["period"] == 20]
        ts, q28 = R["twins_sync_L160"], R["twins_q28_L160"]
        ts2 = R["twins_sync_L320"]
        tw = sorted((s for s in ts["sources"] if s["period"] == 20), key=lambda s: s["birth"]["t"])
        tw2 = sorted((s for s in ts2["sources"] if s["period"] == 20), key=lambda s: s["birth"]["t"])
        qw = sorted((s for s in q28["sources"] if s["period"] == 20), key=lambda s: s["birth"]["t"])
        res[v] = {
            "E01-1": periods(a100) == [20],
            "E01-2": sorted(a100["summary"]["exact_speeds"]) == ["1", "1/3"],
            "E01-3": bool(s100) and s100[0]["birth"]["created"],
            "E01-4": bool(s100 and s200) and s100[0]["birth"]["t"] == s200[0]["birth"]["t"],
            "E01-5": bool(s100 and s200) and s100[0]["birth"]["sites"] == s200[0]["birth"]["sites"],
            "E01-6": R["d1_control_no_seed_L100"]["input"]["events"] == 0,
            "E01-7": len(R["d1_control_no_cores_L100"]["sources"]) == 0,
            "E01-8": len(R["d1_control_B0_phase0_L100"]["sources"]) == 0,
            "E01-9": periods(ts) == [20, 20],
            "E01-10": len(tw) == 2 and tw[0]["phases"] == tw[1]["phases"],
            "E01-11": len(tw) == 2 and tw[0]["birth"]["t"] == tw[1]["birth"]["t"],
            "E01-12": len(tw) == 2 and len(tw2) == 2 and [s["birth"]["t"] for s in tw] == [s["birth"]["t"] for s in tw2],
            "E01-13": len(qw) == 2 and qw[1]["birth"]["t"] - qw[0]["birth"]["t"] == 12,
            "E01-14": R["twins_sync_control_no_seed_L160"]["input"]["events"] == 0,
            "E01-15": periods(R["twins_sync_control_no_lower_cores_L160"]) == [20],
            "_details": {"d1_L100": [[s["period"], s["birth"]["t"], s["composite"], s["lamp"]] for s in a100["sources"]],
                         "exact_speeds_L100": a100["summary"]["exact_speeds"],
                         "twins_sync": [[s["period"], s["birth"]["t"], s["phases"][:6]] for s in ts["sources"]],
                         "twins_q28": [[s["period"], s["birth"]["t"]] for s in q28["sources"]],
                         "no_cores": periods(R["d1_control_no_cores_L100"]),
                         "B0_phase0": periods(R["d1_control_B0_phase0_L100"]),
                         "no_lower_cores": periods(R["twins_sync_control_no_lower_cores_L160"])}}
    return {"logs": {k: {x: r[x] for x in ("log_sha256", "log_matches_manifest")} for k, r in runs.items()}, "checks": res}


def h_e06():
    runs = manifest_reps("E06_moving_light_clock")
    res = {}
    for v in DEC:
        R = {k: r["reps"][v] for k, r in runs.items()}
        e2, e3 = exact_set(R["coincidence_v1of2_h12_L640"]), exact_set(R["coincidence_v1of3_h22_L640"])
        sp2 = {str(sum(abs(Fraction(x)) for x in w)) for w in e2}
        sp3 = {str(sum(abs(Fraction(x)) for x in w)) for w in e3}
        res[v] = {"E06-4 (v=1/2)": {"1", "1/2"} <= sp2, "E06-4b (v=1/3)": {"1", "1/3"} <= sp3,
                  "E06-5": R["control_no_glider_L640"]["input"]["events"] == 0,
                  "_exact_v1of2": sorted(sp2), "_exact_v1of3": sorted(sp3),
                  "_matter_v1of2": [[t["motion"]["velocity"], t["motion"]["exact"], t["t_start"], t["t_end"]]
                                    for t in R["coincidence_v1of2_h12_L640"]["tracks"] if t["class"] == "matter"][:6]}
    return {"logs": {k: {x: r[x] for x in ("log_sha256", "log_matches_manifest")} for k, r in runs.items()}, "checks": res}


# ------------------------------------------------------------------ H4 and H9
def h4():
    out = {}
    for v in DEC:
        p = ROOT / f"runs/click_decoder_v1/v{v}/setA/d1_skeleton_atom_spin_clocks_L160.json"
        if not p.exists():
            out[v] = "report missing (run validation.run score first)"
            continue
        rep = json.loads(p.read_text())
        near = [s for s in rep["sources"] if cheb(s["centroid"], (15.5, 140, 5), 160) <= 4]
        out[v] = {"near": [[s["period"], s.get("period_channels_ignored"), s.get("c_image")] for s in near],
                  "pass": any((s.get("c_image") or {}).get("lap") == 18 for s in near)}
    return out


def h9():
    from research.matter_light_v1.r24 import observer as R24
    rows = []
    for p in sorted((ROOT / "runs/matter_light_v1/r24/events").glob("*.jsonl")):
        L = int(p.stem.split("_L")[-1])
        centre = (L // 2,) * 3
        theirs = R24.quotient_field(p, L, centre)
        ev, _ = D11.read_log(p)
        mine = layers.quotient_field(ev, L, None, centre)
        sums_equal = mine["sum"] == {k: v for k, v in sorted(theirs["qsum_sites"].items()) if True} or \
            {k: v for k, v in mine["sum"].items() if v} == {k: v for k, v in theirs["qsum_sites"].items() if v}
        prof_ok = all(abs(mine["profile_Qbar"][str(r)] - v) <= 1e-12 * max(1.0, abs(v))
                      for r, v in theirs["profile_Qbar"].items())
        rows.append({"log": p.name, "sha256": sha(p), "side": L, "sums_equal": sums_equal, "profile_equal": prof_ok,
                     "fit": mine.get("fit_a_over_r_plus_c")})
        print("H9", p.name, sums_equal, prof_ok, flush=True)
    return rows


def main():
    _watchdog()
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    res = {"decoders": {v: M.code_fingerprint() for v, M in DEC.items()},
           "frozen_v1.1": json.loads((HERE.parent / "FROZEN_v1.1.json").read_text()),
           "pre_registered": "validation/PREREGISTRATION.md (v1.1: 01:53, 01:59, 02:03)"}
    for key, fn in (("H9_quotient_field", h9), ("H2_r15_d2j", h2), ("H3_r14_peak_light", h3), ("H4_set_A_c_image_box", h4),
                    ("H1_r06b_flagship_v3", h1), ("H5_planar_bigbang", h_planar), ("H7_E05", h_e05), ("H6_E01", h_e01),
                    ("H8_E06", h_e06)):
        res[key] = fn()
        (HERE / "heldout_v1.1.json").write_text(json.dumps(res, indent=1, sort_keys=True, default=str) + "\n")
    res["seconds"] = round(time.time() - t, 1)
    (HERE / "heldout_v1.1.json").write_text(json.dumps(res, indent=1, sort_keys=True, default=str) + "\n")
    print("done", res["seconds"], "s")


if __name__ == "__main__":
    main()
