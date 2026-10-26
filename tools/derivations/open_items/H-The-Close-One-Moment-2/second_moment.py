"""The credit's frame second moment measured on a record's log alone: the stepped levels against the
levels now at every plane credit, and the merger takes' per-end bookings. Imports nothing of the engine."""

import json
import sys


def read(path):
    with open(path) as handle:
        return json.load(handle)


def main():
    for path in sys.argv[1:]:
        rec = read(path)
        log = rec.get("log", rec)
        credits = [e for e in log if e.get("event") == "credit"]
        plane = [e for e in credits if "re_now" in e.get("frame", {})]
        same = [e for e in plane if (e["frame"]["re_stepped"], e["frame"]["im_stepped"])
                == (e["frame"]["re_now"], e["frame"]["im_now"])]
        apart = [e for e in plane if e not in same]
        births = [e for e in log if e.get("event") == "birth"]
        mergers = [e for e in births if "takes" in e]
        rows = []
        for e in mergers:
            rows.append({
                "i": e["i"], "node": e["node"],
                "ends": [t["node"] for t in e["takes"]],
                "dP_take": [t["dP_take"] for t in e["takes"]],
                "sum": [sum(t["dP_take"][a] for t in e["takes"]) for a in range(3)],
                "taken": [t["taken"] for t in e["takes"]],
                "booked": [t["booked"] for t in e["takes"]],
                "dP_lay_ends": e.get("dP_lay_ends"),
            })
        print(json.dumps({
            "record": path.split("/")[-1],
            "credits": len(credits), "plane credits": len(plane),
            "stepped equal to now": len(same), "apart": len(apart),
            "first apart": (apart[0]["i"], apart[0]["node"]) if apart else None,
            "births": len(births), "merger takes": len(mergers),
            "senses": sorted({e["sense"] for e in credits}),
            "merger rows": rows,
        }))


main()
