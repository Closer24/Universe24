"""Command line of the generic click decoder (versions 1.0 and 1.1, both frozen).

    python -m research.click_decoder_v1 decode LOG.jsonl --side L [--horizon H] [--version 1.0|1.1]
                                         [--c C] [--detectors DET.json] [--layer NAME] [--out REPORT.json]
    python -m research.click_decoder_v1 diff A.jsonl B.jsonl --out A_MINUS_B.jsonl
    python -m research.click_decoder_v1 peak LOG.jsonl --out PEAK.jsonl [--window T0 T1]
    python -m research.click_decoder_v1 field LOG.jsonl --side L --out FIELD.json [--window T0 T1] [--centre X Y Z]
    python -m research.click_decoder_v1 sign LOG.jsonl --out-prefix PREFIX     # sign_split_v1 (r20)

``decode`` writes the deterministic JSON report and prints a short summary. The default version is
1.0, so every command used for a v1.0 claim reproduces unchanged; pass ``--version 1.1`` for v1.1
(``--c`` declares a light speed for its "c-light" class). ``diff`` keeps the records of A whose
(step, address) is absent from B (with A the change observer and B the native log: the l = 0
layer; with B a declared control run: the difference layer). ``peak`` writes r14's
peak_arrival_click_v1 layer. Layers are decoded separately and never merged.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import decoder as V10, decoder_v11 as V11, layers


def _decode(a) -> int:
    mod = V11 if a.version == "1.1" else V10
    events, info = mod.read_log(a.log)
    det = json.loads(Path(a.detectors).read_text(encoding="utf-8")) if a.detectors else None
    kw = {}
    if a.version == "1.1":
        kw["c"] = a.c
        if a.field_window:
            kw["field"] = {"window": a.field_window, "centre": a.centre, "r_range": a.r_range}
    elif a.c is not None or a.field_window:
        raise SystemExit("--c and --field-window need --version 1.1")
    rep = mod.decode(events, side=a.side, horizon=a.horizon, detectors=det, layer=a.layer, log_info=info, **kw)
    if a.out:
        with Path(a.out).open("x", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=1, sort_keys=True)
            fh.write("\n")
    s = rep["summary"]
    short = {"decoder": rep["decoder"]["version"], "events": rep["input"]["events"],
             "side": rep["input"]["side"], "horizon": rep["input"]["horizon"]}
    if rep["sources"] or rep["tracks"]:
        short.update(sources=[[x["id"], x["period"], x["centroid"], "composite" if x["composite"] else "clock",
                               "lamp" if x["lamp"] else "", "c-image" if x.get("c_image") else ""]
                              for x in rep["sources"]],
                     tracks=s["tracks"], exact_speeds=s["exact_speeds"], created=s["created"],
                     explained_fraction=s["explained_fraction"])
    else:
        short["note"] = s.get("note")
    print(json.dumps(short, indent=1))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m research.click_decoder_v1", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decode", help="decode one click log")
    d.add_argument("log")
    d.add_argument("--side", type=int, help="board side L (declared by the experiment)")
    d.add_argument("--horizon", type=int, help="number of updates run (default: last click update)")
    d.add_argument("--version", choices=("1.0", "1.1"), default="1.0", help="frozen decoder version (default 1.0)")
    d.add_argument("--c", type=float, help="v1.1: declared light speed (Euclidean sites/update) for class c-light")
    d.add_argument("--detectors", help="JSON detector declaration for correlations (and v1.1 passages)")
    d.add_argument("--field-window", type=int, nargs=2, metavar=("T0", "T1"),
                   help="v1.1: window of the quotient field (r24's quotient_field_v1)")
    d.add_argument("--centre", type=int, nargs=3, help="v1.1: declared centre for the field's radial profile")
    d.add_argument("--r-range", type=int, nargs=2, help="v1.1: r range of the a/r + c fit (default 1..L/2)")
    d.add_argument("--layer", default="native", help="name of the observer layer (label only)")
    d.add_argument("--out", help="report path (refuses to overwrite)")
    f = sub.add_parser("diff", help="records of A whose (step, address) is not in B")
    f.add_argument("a")
    f.add_argument("b")
    f.add_argument("--out", required=True)
    qf = sub.add_parser("field", help="r24's quotient_field_v1: per-site signed quotient sums (a field file)")
    qf.add_argument("log")
    qf.add_argument("--side", type=int, required=True)
    qf.add_argument("--out", required=True)
    qf.add_argument("--window", type=int, nargs=2)
    qf.add_argument("--centre", type=int, nargs=3)
    qf.add_argument("--r-range", type=int, nargs=2)
    sg = sub.add_parser("sign", help="sign_split_v1 (r20): quotient-sign layers PREFIX.P.jsonl (q > 0), PREFIX.M.jsonl")
    sg.add_argument("log")
    sg.add_argument("--out-prefix", required=True)
    pk = sub.add_parser("peak", help="r14's peak_arrival_click_v1 layer of a click log")
    pk.add_argument("log")
    pk.add_argument("--out", required=True)
    pk.add_argument("--window", type=int, nargs=2)
    pk.add_argument("--w", type=int, default=V11.load_config()["peak_half_window"])
    a = ap.parse_args(argv)
    if a.cmd == "decode":
        return _decode(a)
    if a.cmd == "diff":
        print(json.dumps({"kept": layers.diff(a.a, a.b, a.out), "out": a.out}))
        return 0
    if a.cmd == "sign":
        from .sign_layer import sign_split
        print(json.dumps(sign_split(a.log, a.out_prefix)))
        return 0
    events, info = V11.read_log(a.log)
    if a.cmd == "field":
        res = layers.quotient_field(events, a.side, a.window, a.centre, a.r_range)
        res["log"] = {"name": info["name"], "sha256": info["sha256"]}
        with Path(a.out).open("x", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(json.dumps({k: res[k] for k in ("observer", "window", "sites", "total")}))
        return 0
    print(json.dumps({"records": layers.write_peak_arrival(events, a.out, a.w, a.window), "out": a.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
