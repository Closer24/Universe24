"""THE EIGHTH HARD QUESTION (record 2140; ALGEBRA.md 9.103 (4)), THE ALGEBRA'S NUMBER: the
multiplicities of a well's bound levels under the cube group, from the margin operator's
spectrum (docs/designs/detector_law/MASSIVE_RECORD.md section 11 item 4: the characters 2 cos
omega D a = (S_6 / 3) a, D = den / num per Node, the symmetric operator A = D^-1/2 (S_6 / 3)
D^-1/2, the bound levels its eigenvalues above the kind's band top 2 num / den). A Lanczos
iteration with full reorthogonalisation on the well's own board (HOST floats), the top
eigenvalues clustered into levels, each level's count. A well of side 5 (and of side 9) at the
kind [800, 850] on the pair [800, 801], the board 32^3 periodic.

    PYTHONPATH=src python docs/designs/rule_alone/item8_spectrum.py [side] [board]
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodies as B  # noqa: E402


def six_sum(a: np.ndarray) -> np.ndarray:
    total = np.zeros_like(a)
    for axis in range(3):
        total += np.roll(a, 1, axis=axis) + np.roll(a, -1, axis=axis)
    return total


def lanczos(apply, size: int, steps: int, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(size)
    q /= np.linalg.norm(q)
    basis = [q]
    alphas, betas = [], []
    for _ in range(steps):
        w = apply(basis[-1])
        alpha = float(basis[-1] @ w)
        w = w - alpha * basis[-1] - (betas[-1] * basis[-2] if betas else 0.0)
        # full reorthogonalisation (the degenerate levels need it)
        for vector in basis:
            w -= (vector @ w) * vector
        beta = float(np.linalg.norm(w))
        alphas.append(alpha)
        if beta < 1e-12:
            break
        betas.append(beta)
        basis.append(w / beta)
    matrix = (
        np.diag(alphas) + np.diag(betas[: len(alphas) - 1], 1) + np.diag(betas[: len(alphas) - 1], -1)
    )
    return np.sort(np.linalg.eigvalsh(matrix))[::-1]


def spectrum(side: int, board: int, steps: int = 160) -> dict:
    shape = (board, board, board)
    body = B.Body([board // 2] * 3, 2000, side=side)
    num, den = body.pairs(shape)
    ratio = (den / num).astype(np.float64)  # D
    inv_sqrt = 1.0 / np.sqrt(ratio)

    def apply(v: np.ndarray) -> np.ndarray:
        a = v.reshape(shape) * inv_sqrt
        return (inv_sqrt * six_sum(a) / 3.0).ravel()

    values = lanczos(apply, board**3, steps)
    top = 2.0 * float(B.KIND[0]) / float(B.KIND[1])
    bound = [float(v) for v in values if v > top + 1e-9]
    # cluster into levels: gaps above 1e-6 of the value separate levels
    levels = []
    for v in bound:
        if levels and abs(levels[-1]["value"] - v) < 1e-6:
            levels[-1]["count"] += 1
            levels[-1]["members"].append(v)
        else:
            levels.append({"value": v, "count": 1, "members": [v]})
    for level in levels:
        level["omega"] = math.acos(level["value"] / 2.0)
        level["mean"] = float(np.mean(level["members"]))
    return {"side": side, "board": board, "band_top": top, "levels": levels, "lanczos_steps": steps}


def main() -> None:
    side = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    board = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    result = spectrum(side, board)
    print(
        f"the well of side {side} at [800, 850] on [800, 801], the board {board}^3 periodic; the kind's band top 2 cos = {result['band_top']:.6f}"
    )
    for index, level in enumerate(result["levels"]):
        print(
            f"  level {index}: 2 cos omega = {level['mean']:.7f} (omega {level['omega']:.5f}), multiplicity {level['count']}"
        )
    (Path(__file__).resolve().parent / f"item8_spectrum_side{side}.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
