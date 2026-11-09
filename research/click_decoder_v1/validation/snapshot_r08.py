"""One-off: snapshot r08's post-hoc reference truth for the wave-6 test set (validation set B).

Imports r08's ``clicks_truth.reference`` and its dark rule read-only and writes plain JSON, so
that scoring does not depend on r08's research folder. Records the hashes of r08's files and of
the logs. Run once; the output is versioned with the decoder.

    python -m research.click_decoder_v1.validation.snapshot_r08
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "r08_reference.json"
LOGS = ROOT / "runs/matter_light_v1/r08/clicklogs"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    from research.matter_light_v1.r08 import clicks_only_v2 as V2, clicks_truth as CT
    cases = []
    for name in CT.REF_CASES + CT.EXTRA_CASES:
        log = LOGS / f"{name}.jsonl"
        summ = json.loads((LOGS / f"{name}.summary.json").read_text())
        events = V2.load(log)
        clicks, site_steps = defaultdict(set), defaultdict(list)
        for e in events:
            clicks[e[0]].add((e[1], e[2], e[3]))
            site_steps[(e[1], e[2], e[3])].append(e[0])
        L = summ["side"]
        objs = []
        for o in CT.reference(name):
            dark = CT.is_dark(o, clicks, site_steps, L)
            own = CT.own_clicks(o, site_steps, L) if CT._rest(o) else None
            objs.append({k: o[k] for k in ("family", "start", "end", "birth_centroid", "velocity", "bound",
                                           "created", "lamp", "period", "own_radius", "what")}
                        | {"dark": dark, "own_clicks": own, "at_rest": CT._rest(o)})
        cases.append({"case": name, "declared": name in CT.REF_CASES, "log": str(log.relative_to(ROOT)),
                      "log_sha256": _sha(log), "side": L, "horizon": summ["completed_steps"], "objects": objs})
    prov = {f: _sha(ROOT / "research/matter_light_v1/r08" / f) for f in ("clicks_truth.py", "clicks_only_v2.py")}
    out = {"what": "r08 post-hoc reference truth for the wave-6 clicks-only test set (r08/REPORT_WAVE6.md 2.2), "
                   "with r08's dark rule; snapshot taken by r17 before any decoding",
           "matching": "same family, time overlap >= 50% of the shorter life, Chebyshev <= 4 at the middle common "
                       "update; one-to-one, visible objects first, nearest pairs first",
           "r08_sources_sha256": prov, "cases": cases}
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print({c["case"]: (len(c["objects"]), sum(o["dark"] for o in c["objects"])) for c in cases})


if __name__ == "__main__":
    main()
