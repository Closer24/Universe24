"""THE EIGHTH HARD QUESTION (record 2140; ALGEBRA.md 9.103 (4)), THE ALGEBRA'S NUMBER, second
computation: a Lanczos iteration from one starting vector cannot show a multiplicity (its
Krylov space meets each eigenspace in one direction), so the levels' counts are read here from
the full symmetric eigendecomposition of the margin operator A = D^-1/2 (S_6 / 3) D^-1/2 on a
small periodic board (HOST floats, dense), and checked with the shift-invert eigensolver of
scipy on a larger board. A level is a cluster of eigenvalues within 1e-6; the multiplicity is
the cluster's size. The cube group's irreducible dimensions are 1, 1, 2, 3, 3, so a count of 3
is the p-like triplet of 9.103 (4).

    PYTHONPATH=src python docs/designs/rule_alone/item8_dense.py [side] [board] [dense|sparse]
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402


def operator(side: int, board: int) -> tuple[sp.csr_matrix, float]:
    shape = (board, board, board)
    body = B.Body([board // 2] * 3, 2000, side=side)
    num, den = body.pairs(shape)
    inv_sqrt = (1.0 / np.sqrt(den / num)).ravel()
    size = board**3
    index = np.arange(size).reshape(shape)
    rows, cols = [], []
    for axis in range(3):
        for step in (1, -1):
            rows.append(index.ravel())
            cols.append(np.roll(index, step, axis=axis).ravel())
    rows_all = np.concatenate(rows)
    cols_all = np.concatenate(cols)
    data = inv_sqrt[rows_all] * inv_sqrt[cols_all] / 3.0
    matrix = sp.csr_matrix((data, (rows_all, cols_all)), shape=(size, size))
    top = 2.0 * float(B.KIND[0]) / float(B.KIND[1])
    return matrix, top


def cluster(values: np.ndarray, top: float, tolerance: float = 1e-6) -> list[dict]:
    bound = sorted((float(v) for v in values if v > top + 1e-9), reverse=True)
    levels: list[dict] = []
    for v in bound:
        if levels and abs(levels[-1]["members"][-1] - v) < tolerance:
            levels[-1]["members"].append(v)
        else:
            levels.append({"members": [v]})
    for level in levels:
        level["count"] = len(level["members"])
        level["mean"] = float(np.mean(level["members"]))
        level["omega"] = math.acos(level["mean"] / 2.0)
    return levels


def spectrum(side: int, board: int, method: str) -> dict:
    matrix, top = operator(side, board)
    if method == "dense":
        values = np.linalg.eigvalsh(matrix.toarray())
    else:
        # the eigenvalues nearest 2.0 (above the band top), shift-invert; ARPACK with a
        # random start finds a degenerate level's copies through the restarts
        values = spl.eigsh(matrix, k=12, sigma=2.0, which="LM", return_eigenvectors=False, tol=1e-10)
    levels = cluster(np.asarray(values), top)
    return {"side": side, "board": board, "method": method, "band_top": top, "levels": levels}


def main() -> None:
    side = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    board = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    method = sys.argv[3] if len(sys.argv) > 3 else "dense"
    result = spectrum(side, board, method)
    print(
        f"the well of side {side} at {B.KIND} on {B.WELL}, the board {board}^3 periodic, {method}; the band top 2 cos = {result['band_top']:.6f}"
    )
    for index, level in enumerate(result["levels"]):
        print(
            f"  level {index}: 2 cos omega = {level['mean']:.7f} (omega {level['omega']:.5f}), multiplicity {level['count']}"
        )
    name = f"item8_dense_side{side}_board{board}_{method}.json"
    (Path(__file__).resolve().parent / name).write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
