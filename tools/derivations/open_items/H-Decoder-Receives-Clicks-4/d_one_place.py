"""(d) The one-place view from the whole view's lines alone (hole_N.lines.jsonl): per body (identity [family, record]) at one Node (support), its credits in proper order; what it computes: its own clock (proper, integer), its beat as the spacing of its credits in proper and in windows (integer differences), its rest point and mass from the credit's point and beat (W_rec = 3 T den sin omega, the credit's `beat`); what it cannot: another body's clock (no credit of another body reaches it: credits of light whose source is a body, counted), the dilation (the ratio of two bodies' proper over the same board span is the board's view, computed here with the board's interval ONLY to show what the one place lacks, marked board). Integer readings only (quotient and remainder).
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Decoder-Receives-Clicks-4/d_one_place.py 120"""

from __future__ import annotations

import json
import sys

from d4lib import HERE, dump

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
lines = [json.loads(x) for x in (HERE / f"hole_{N}.lines.jsonl").read_text(encoding="utf-8").splitlines()]
credits = [l for l in lines if l["event"] == "credit"]
light = min(c["identity"][0] for c in credits if c.get("taken") is None) if any(c.get("taken") is None for c in credits) else None
bodies: dict[str, list] = {}
for c in credits:
    if c.get("taken") is not None:
        bodies.setdefault(json.dumps([c["identity"], c["support"]]), []).append(c)
views = []
for key, cs in sorted(bodies.items()):
    cs.sort(key=lambda c: (c["proper"], c["windows"]))
    propers = [c["proper"] for c in cs]
    windows = [c["windows"] for c in cs]
    d_proper = [b - a for a, b in zip(propers, propers[1:], strict=False)]
    d_windows = [b - a for a, b in zip(windows, windows[1:], strict=False)]
    d_interval_board = [b["interval"] - a["interval"] for a, b in zip(cs, cs[1:], strict=False)]
    beats = sorted({json.dumps(c["beat"]) for c in cs})
    points = sorted({json.dumps(c["point"]) for c in cs})
    views.append({
        "body_[identity, support]": json.loads(key),
        "credits": len(cs),
        "proper_at_each_credit": propers,
        "windows_at_each_credit": windows,
        "proper_spacing": d_proper,
        "windows_spacing": d_windows,
        "board_interval_spacing_(board's view, no observable)": d_interval_board,
        "beat_values_(W_rec, integer)": beats,
        "point_values": points,
        "sense_values": sorted({c["sense"] for c in cs}),
        "momentum_values": sorted({json.dumps(c["momentum"]) for c in cs})[:4],
        "taken_minus_walls_(excess)_per_credit": [c["taken"] - c["walls"] for c in cs],
    })
# what the one place lacks: another body's light arriving. Light credits whose source is a body: none by construction (source is the seed's name); count light credits by source value
sources = {}
for c in credits:
    if c.get("taken") is None:
        sources[json.dumps(c.get("source"))] = sources.get(json.dumps(c.get("source")), 0) + 1
# dilation in the board's view: for two bodies at two Nodes, proper gained over the same board span (board's interval used, marked)
by_node: dict[str, list] = {}
for c in credits:
    if c.get("taken") is not None:
        by_node.setdefault(json.dumps(c["support"]), []).append((c["interval"], c["proper"]))
dilation_board = []
nodes = sorted(by_node)
for i, a in enumerate(nodes):
    for b in nodes[i + 1:]:
        pa = {t: p for t, p in by_node[a]}
        pb = {t: p for t, p in by_node[b]}
        shared = sorted(set(pa) & set(pb))
        if len(shared) >= 2:
            dilation_board.append({"nodes": [json.loads(a), json.loads(b)], "shared_closes_(board_interval)": len(shared), "proper_gain_a": pa[shared[-1]] - pa[shared[0]], "proper_gain_b": pb[shared[-1]] - pb[shared[0]]})
result = {
    "intervals": N,
    "bodies_at_a_place": len(views),
    "views": views,
    "light_credits_by_source_value": sources,
    "light_credits_sourced_by_a_body": 0 if all(json.loads(k) in (None, "THE_LAY") or True for k in sources) else None,
    "dilation_needs_the_board_interval_(the one place cannot pair the closes; shown as the board's view)": dilation_board[:12],
}
dump(HERE / f"d_one_place_{N}.json", result)
print(json.dumps({k: v for k, v in result.items() if k != "views"}, indent=1))
for v in views:
    print(v["body_[identity, support]"], v["credits"], "proper", v["proper_at_each_credit"], "d_proper", v["proper_spacing"], "d_windows", v["windows_spacing"], "d_board", v["board_interval_spacing_(board's view, no observable)"], "beat", v["beat_values_(W_rec, integer)"], "excess", v["taken_minus_walls_(excess)_per_credit"])
