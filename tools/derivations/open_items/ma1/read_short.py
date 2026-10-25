import json, sys, subprocess
sys.set_int_max_str_digits(0)
for f in sys.argv[1:]:
    out = subprocess.run([sys.executable, "read_diag.py", f], capture_output=True, text=True).stdout
    d = json.loads(out)
    keep = ["laid", "mean at the marks", "mean's peak (i, X)", "tops with every Node turning (i, X)", "turns of fewer than every Node (i, count), first 6", "returns to Gamma (i)", "e at every 40th", "first interval with e > 0", "gap0 share peak (i, units, rem)", "nodes at one unit of light, max", "F max peak (i, F)", "twist max peak (i, h)", "W total values", "mergers summed", "last interval with a whole massive Link", "counts", "run back", "integers", "max bits", "transient bits", "48 at the end", "invariance at the end"]
    print("=====", f)
    for k in keep:
        v = d[k]
        if k == "laid":
            v = [{kk: vv for kk, vv in l.items() if kk in ("pattern", "row", "sense", "amplitude", "flip")} for l in v]
        if k == "counts":
            v = {kk: vv for kk, vv in v.items() if vv != "0"}
        print(k, ":", json.dumps(v))
