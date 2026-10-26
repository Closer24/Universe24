"""pr2: the premise of the merger read from a record's log alone (no engine import, the code-shape gate).
For every birth at interval i on the Link (minus, plus) of the row s, the premise event logged at
i + 1 on that same Link and row: the current and twist the close governed by (the interval's start,
the pair as the birth laid it) against the alternative read (the same pair one Rule3 step on), and
the fate of that meeting (the refusals by name at that Link, the merger paid). The counts by fate.
Usage: python premise_read.py <record.json> [<out.json>]"""
import json
import sys

sys.set_int_max_str_digits(0)


def key(a, b):
    a, b = tuple(a), tuple(b)
    return (a, b) if a < b else (b, a)


def main(path, out_path=None):
    rec = json.load(open(path))
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth" and not e.get("merger")]
    premises = {}
    for e in log:
        if e["event"] == "premise":
            premises.setdefault((e["i"], e["row"], key(e["node"], e["link"])), e)
    refusals = {}
    for e in log:
        if e["event"] == "refused" and "link" in e and "row" in e:
            refusals.setdefault((e["i"], e["row"], key(e["node"], e["link"])), e["cause"])
    stops = {}
    lays = {}
    for e in log:
        if e["event"] == "refused" and e["cause"] == "stop":
            stops.setdefault(e["i"], []).append(tuple(e["node"]))
        if e["event"] == "refused" and e["cause"] == "lay" and "row" in e:
            lays.setdefault((e["i"], e["row"]), []).append(tuple(e["node"]))
    paid = {}
    for e in log:
        if e["event"] == "birth" and e.get("merger"):
            paid[(e["i"], e.get("taken_row"), key(e["minus"], e["plus"]))] = e
    rows = []
    for b in births:
        i, s = b["i"], b["line_pair"]
        kk = key(b["minus"], b["plus"])
        at = (i + 1, s, kk)
        p = premises.get(at)
        fate = "no meeting"
        if p is not None:
            fate = refusals.get(at, "met")
            if fate == "met":
                if any(n in kk for n in stops.get(i + 1, [])):
                    fate = "stop"
                elif any(n in kk for n in lays.get((i + 1, s), [])):
                    fate = "lay"
                elif any(k[0] == i + 1 and k[2] == kk for k in paid):
                    fate = "paid"
        rows.append(
            dict(
                i=i,
                row=s,
                born_row=b.get("taken_row"),
                link=[list(kk[0]), list(kk[1])],
                met=p is not None,
                flow=None if p is None else p["flow"],
                twist=None if p is None else p["twist"],
                charges=None if p is None else p["charges"],
                flow_other=None if p is None else p["flow_other"],
                twist_other=None if p is None else p["twist_other"],
                charges_other=None if p is None else p["charges_other"],
                fate=fate,
            )
        )
    met = [r for r in rows if r["met"]]
    zero = [r for r in met if r["flow"] == 0]
    zero_other = [r for r in met if r["flow_other"] == 0]
    opposite = [r for r in met if r["charges"][0] * r["charges"][1] < 0]
    rest = [r for r in met if r["flow"] == 0 and r["charges"][0] * r["charges"][1] < 0]
    rest_other = [
        r for r in met if r["flow_other"] == 0 and r["charges_other"][0] * r["charges_other"][1] < 0
    ]
    fates = {}
    for r in rows:
        fates[r["fate"]] = fates.get(r["fate"], 0) + 1
    summary = dict(
        births=len(births),
        met_at_next_close=len(met),
        flow_zero_at_next_close=len(zero),
        flow_zero_stepped=len(zero_other),
        charges_opposite=len(opposite),
        rest_premise_as_laid=len(rest),
        rest_premise_stepped=len(rest_other),
        fates=fates,
        premise_lines=len(premises),
        all_premise_flow_zero=sum(1 for p in premises.values() if p["flow"] == 0),
        all_premise_flow_zero_stepped=sum(1 for p in premises.values() if p["flow_other"] == 0),
        all_premise_rest=sum(
            1
            for p in premises.values()
            if p["flow"] == 0 and p["charges"][0] * p["charges"][1] < 0
        ),
        all_premise_rest_stepped=sum(
            1
            for p in premises.values()
            if p["flow_other"] == 0 and p["charges_other"][0] * p["charges_other"][1] < 0
        ),
        mergers_paid=len(paid),
    )
    print(json.dumps(summary))
    for r in rows:
        print(json.dumps(r))
    if out_path is not None:
        json.dump(dict(summary=summary, pairs=rows), open(out_path, "w"))


if __name__ == "__main__":
    main(*sys.argv[1:])
