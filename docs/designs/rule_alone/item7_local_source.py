"""ITEM 7 of record 2134: a LOCAL source from the record's current and stress (ALGEBRA.md 9.98
(4) as redesigned in 9.102 (3): the vector part 4 s J_a(i) div F_i at the Node alone, the tensor
2 s J_a J_b div F_i div F_i, zero at rest where the current is zero). The check, a HOST reading
of the moving record's own integers (no run): at each Node of the support, the pace the local
source implies, v_i = (num / den) J_a(i) / (3 F_i), against the record's pace v; its spread; and
the local source's total over the support, SUM 4 s J_a(i) / F_i x (F_i / SUM F), against 4 s v
(the sum 9.91 (3) writes). Nothing exists with the Node and its six neighbours alone if the
per-Node ratio is not v.

    PYTHONPATH=src python docs/designs/rule_alone/item7_local_source.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402

SHAPE = (240, 32, 32)
WRAP = (True, True, True)
AMOUNT = 2000


def main() -> None:
    body = B.Body([60, 16, 16], AMOUNT)
    profile, clock = B.bound_mode(SHAPE, WRAP, body)
    cos_b = clock[0] / (2.0 * clock[1])
    out = {"clock": clock, "rows": []}
    for v in (0.05, 0.1, 0.2):
        now, before, numbers = B.moving_record(profile, body, SHAPE, WRAP, 0, v, clock)
        n = now.astype(np.float64)
        b = before.astype(np.float64)
        num, den = body.pairs(SHAPE)
        ratio = num.astype(np.float64) / den.astype(np.float64)
        current = np.roll(n, -1, axis=0) * b - np.roll(b, -1, axis=0) * n
        form = n * n + b * b - 2.0 * n * b * cos_b
        mask = body.mask(SHAPE)
        # the support: the well's Nodes and the shell of the record around it (form above 1/1000 of the peak)
        support = form > form.max() / 1000.0
        local = np.where(form > 0, ratio * current / (3.0 * np.maximum(form, 1e-9)), 0.0)
        on_well = local[mask]
        on_support = local[support]
        total_local = float((4 * AMOUNT * ratio * current / 3.0)[support].sum() / form[support].sum())
        row = {
            "v": v,
            "K": numbers["K"],
            "support_nodes": int(support.sum()),
            "well_nodes_pace_median": float(np.median(on_well)),
            "well_nodes_pace_min_max": [float(on_well.min()), float(on_well.max())],
            "support_pace_median": float(np.median(on_support)),
            "support_pace_quartiles": [
                float(np.percentile(on_support, 25)),
                float(np.percentile(on_support, 75)),
            ],
            "sum_local_source_over_4s": total_local / (4 * AMOUNT),
            "at_rest_current_max": None,
        }
        out["rows"].append(row)
        print(
            f"v {v}: K {numbers['K']:.4f}; the local pace on the well's 125 Nodes: median {row['well_nodes_pace_median']:.4f}, "
            f"min {row['well_nodes_pace_min_max'][0]:.4f}, max {row['well_nodes_pace_min_max'][1]:.4f}; on the support "
            f"({row['support_nodes']} Nodes): median {row['support_pace_median']:.4f}, quartiles {row['support_pace_quartiles'][0]:.4f} "
            f"to {row['support_pace_quartiles'][1]:.4f}; the local source's total / (4 s) = {row['sum_local_source_over_4s']:.4f} against v"
        )
    # at rest: the current is zero at every Node
    n = profile.astype(np.float64)
    current_rest = np.roll(n, -1, axis=0) * n - np.roll(n, -1, axis=0) * n
    print(
        "at rest (both levels the profile): the current's largest magnitude",
        float(np.abs(current_rest).max()),
    )
    out["at_rest_current_max"] = float(np.abs(current_rest).max())
    (Path(__file__).resolve().parent / "item7_local_source.json").write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
