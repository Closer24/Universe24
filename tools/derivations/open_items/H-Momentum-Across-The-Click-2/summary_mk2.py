"""mk2: the out/*.json records summed: the flag, the hashes, the counts, the run back, the bits, the gates, and the per-click identity along the click's axis (dP_take + dP_recoil = r, |2r| <= |wall|) with the transverse recoil named."""
import glob, json, os, sys
sys.set_int_max_str_digits(0)
AXES = 3
for path in sorted(glob.glob(sys.argv[1] + "/*_world_*.log")):
    try:
        d = json.load(open(path))
    except Exception as exc:
        print(os.path.basename(path), "NO SUMMARY:", open(path).read()[-300:].replace("\n", " ")); continue
    if not os.path.exists(path[:-4] + ".json"):
        print(os.path.basename(path), {k: d[k] for k in ("flag", "final state hash", "log hash", "run_back")}); continue
    rec = json.load(open(path[:-4] + ".json"))
    log = rec["log"]
    clicks = [e for e in log if e["event"] in ("birth", "credit")]
    booked = [e for e in clicks if "recoil" in e]
    moved = [e for e in booked if e["recoil"] != 0]
    along_r = sum(abs(e["dP_take"][e["recoil_axis"]] + e["dP_recoil"][e["recoil_axis"]]) for e in booked if e["recoil_axis"] >= 0)
    along_t = sum(abs(e["dP_take"][e["recoil_axis"]]) for e in booked if e["recoil_axis"] >= 0)
    within = sum(1 for e in booked if e["recoil_axis"] >= 0 and 2 * abs(e["dP_take"][e["recoil_axis"]] + e["dP_recoil"][e["recoil_axis"]]) <= abs(e["recoil_wall"]))
    exact_axis = sum(1 for e in booked if e["recoil_axis"] >= 0 and e["dP_take"][e["recoil_axis"]] + e["dP_recoil"][e["recoil_axis"]] == 0)
    exact3 = sum(1 for e in booked if all(e["dP_take"][a] + e["dP_recoil"][a] == 0 for a in range(AXES)))
    transverse_recoil = sum(abs(e["dP_recoil"][b]) for e in booked for b in range(AXES) if b != e["recoil_axis"])
    transverse_take = sum(abs(e["dP_take"][b]) for e in booked for b in range(AXES) if b != e["recoil_axis"])
    transverse_zero = sum(1 for e in booked if all(e["dP_recoil"][b] == 0 for b in range(AXES) if b != e["recoil_axis"]))
    c = d["counts"]
    print(json.dumps({
        "file": os.path.basename(path), "flag": d["flag"], "state hash": d["final state hash"][:12], "log hash": d["log hash"][:12],
        "births": c["births"], "credits": c["body_clicks"], "laid_back": c["laid_back"], "turns": c["turns"], "recoil moved": c.get("recoil"), "recoil flat": c.get("recoil_flat"),
        "run_back": d["run_back"], "integers": d["integers per Node"], "state bits": d["max state bits"], "transient bits": d["max transient bits"],
        "SHOWN": d["gates SHOWN"], "gate 23": d["gate 23"]["verdict"], "gate 54": d["gate 54"][:9],
        "clicks": len(clicks), "booked": len(booked), "moved": len(moved), "largest p": max((abs(e["recoil"]) for e in booked), default=0),
        "along axis: remainder abs / take abs": [along_r, along_t], "remainder within the wall's half": within, "exact on the axis": exact_axis, "exact on three axes": exact3,
        "transverse: recoil abs / take abs": [transverse_recoil, transverse_take], "transverse recoil 0": transverse_zero,
        "axes of the booked clicks": [sum(1 for e in booked if e["recoil_axis"] == a) for a in range(AXES)],
    }))
