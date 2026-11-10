"""``sign_split_v1``: the quotient-sign layers of a click log (r20's declared observer, read-only).

Layer P holds the records with quotient > 0 and layer M the records with quotient < 0; each record
is kept verbatim (same line), records with quotient 0 go to neither. Each layer is a click log in the
official record form and is decoded on its own, never merged. Definition: r20,
research/matter_light_v1/r20/phase_element.py (``sign_split``). This file is outside the frozen cores
of decoder v1.0 and v1.1 and is frozen on its own (``FROZEN_sign_split_v1.json``).
"""
from __future__ import annotations

import json
from pathlib import Path

NAME = "sign_split_v1"


def sign_split(log, out_prefix):
    """Write ``<out_prefix>.P.jsonl`` and ``<out_prefix>.M.jsonl``; returns their paths and record counts."""
    lines = Path(log).read_text(encoding="utf-8").splitlines()
    out = {}
    for tag, keep in (("P", lambda q: q > 0), ("M", lambda q: q < 0)):
        path = Path(f"{out_prefix}.{tag}.jsonl")
        n = 0
        with path.open("x", encoding="utf-8") as fh:
            for line in lines:
                if line.strip() and keep(json.loads(line)["quotient"]):
                    fh.write(line + "\n")
                    n += 1
        out[tag] = {"path": str(path), "records": n}
    return out
