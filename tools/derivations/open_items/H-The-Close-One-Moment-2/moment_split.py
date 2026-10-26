"""At every plane credit: whether the stepped levels equal the levels now, the levels before, or neither,
split by whether the Node turned. From the log alone."""
import json
import sys

for path in sys.argv[1:]:
    with open(path) as handle:
        log = json.load(handle)["log"]
    out = {}
    for e in log:
        if e.get("event") != "credit" or "re_now" not in e.get("frame", {}):
            continue
        f = e["frame"]
        s = (f["re_stepped"], f["im_stepped"])
        kind = "now" if s == (f["re_now"], f["im_now"]) else (
            "before" if s == (f["re_before"], f["im_before"]) else "neither")
        key = ("turned" if e["turned"] else "still") + " / " + kind
        out[key] = out.get(key, 0) + 1
    print(json.dumps({"record": path.split("/")[-1], "counts": out}))
