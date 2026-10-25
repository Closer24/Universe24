"""ag2's reader of the records (items 5 and 7 of the brief): the decoder's own counts against the log's (births, credits, taken, booked, laid back), the births' charge (the senses' sum), the exact take (taken against booked per birth), SL-S2's mergers (the taken row gapped, two ends' takes), EQ-S1 (credits laid back where the net current is 0, taken = laid back), the light no body (credits of the gap-0 row), the energy in the clicks (the beat unchanged between a body's consecutive credits), the state's and the transients' bits, the integers' count, the run back, and the decoder's species solve against the credited row's pair. Integers only; a reader, no act. Usage: python read_records.py <record.json> ..."""

from __future__ import annotations

import json
import sys
from collections import defaultdict

from event_universe.core.paces import sine_den
from event_universe.clicks import decoded_credits
from event_universe.decoder import Record, solve

sys.set_int_max_str_digits(0)


def read(path: str) -> dict:
    run = json.load(open(path, encoding="utf-8"))
    record = Record(run)
    log = run["log"]
    counts = {k: int(v) for k, v in run["counts"].items()}
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    rec0 = record.line_num.index(record.den)
    out = {"file": path.split("/")[-1], "intervals": run["intervals"], "cube": run["cube"], "den_bits": record.den.bit_length()}
    out["counts_vs_log"] = {
        "births": [counts["births"], len(births)],
        "body_clicks": [counts["body_clicks"], len(credits)],
        "laid_back": [counts["laid_back"], sum(1 for c in credits if "laid_back" in c)],
        "taken (births)": [counts["taken"], sum(int(b["taken"]) for b in births) if births else 0],
        "booked (births)": [counts["booked"], sum(int(b["booked"]) for b in births) if births else 0],
    }
    # the births' charge and the exact take
    senses = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    out["births_charge_sum"] = sum(senses)
    out["births_W_children_abs"] = sorted({abs(w) for b in births for w in b["W_children"]})[:4]
    exact = sum(1 for b in births if b["taken"] == b["booked"])
    excess = [int(b["taken"]) - int(b["booked"]) for b in births]
    out["exact_take"] = {"births": len(births), "taken == booked": exact, "taken >= booked": sum(1 for x in excess if x >= 0), "excess least/largest": [min(excess), max(excess)] if excess else None}
    # the stop and the merger (SL-S2)
    mergers = [b for b in births if "takes" in b]
    out["mergers (SL-S2)"] = {"count": len(mergers), "each end's taken >= its wall": sum(1 for b in mergers for t in b["takes"] if t["taken"] >= t["booked"]), "ends": 2 * len(mergers), "children W": sorted({tuple(b["W_children"]) for b in mergers})[:3]}
    out["refused"] = {k: v for k, v in counts.items() if k.startswith("refused")}
    # EQ-S1 and the light no body
    laid = [c for c in credits if "laid_back" in c]
    out["eq_s1"] = {"credits": len(credits), "laid back": len(laid), "levels taken == laid back on every laid-back credit": all(c["levels"] == c["laid_back"] for c in laid), "dP 0 on laid back": all(c["dP_take"] == [0, 0, 0] for c in laid)}
    out["light_no_body (credits of the gap-0 row)"] = sum(1 for c in credits if c["line"] == rec0)
    # the energy in the clicks: the beat between consecutive credits of one body
    beats: dict = defaultdict(list)
    for c in credits:
        beats[(tuple(c["node"]), c["line"])].append((c["i"], c["beat"]))
    pairs = [(a[1], b[1]) for cs in beats.values() for a, b in zip(sorted(cs), sorted(cs)[1:]) if a[1] > 0 and b[1] > 0]
    out["energy_beats"] = {"pairs": len(pairs), "unchanged": sum(1 for a, b in pairs if a == b), "changed": sum(1 for a, b in pairs if a != b), "beats seen": sorted({b for cs in beats.values() for _i, b in cs})[:8]}
    # the width and the count
    rows = run["rows"]
    out["width"] = {"integers": sorted({r["integers"] for r in rows}), "state bits max": max(r["max bits"] for r in rows), "transient bits max": max(r["max transient bits"] for r in rows), "run_back": run["run_back"]}
    # the decoder's solve against the credited row's pair: the name nearest the solved rational (clicks.decoded_credits), and the count within the one-click floor
    decoded, right, within, _floors = decoded_credits(record)
    out["decoder_solve"] = {"credits": len(credits), "decoded": len(decoded), "name right (nearest)": right, "within the one-click floor": within}
    return out


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(json.dumps(read(path)))
