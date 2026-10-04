"""The pixel's tail and the wells between two pixels (ALGEBRA.md, The tail, L205; R187 and R193): at the count c with the tail t = e^(-kappa) the level d Links away is b t^d and the well c t^(2 d); two pixels s Links apart put at the Node between them, one Link from each, the wells' sum 2 c t^2, which the Link's pace Gamma less that sum must keep open.

Usage: `python tools/derivations/wells.py` prints the wells of the table's 6,000 (level once, t = 0.377) and the sum at the Node between.
"""

from __future__ import annotations


def wells(count: int = 6000, tail: float = 0.377, reach: int = 3) -> list[float]:
    """The well c t^(2 d) at d = 1 to `reach` Links."""
    return [count * tail ** (2 * d) for d in range(1, reach + 1)]


def node_between(count: int = 6000, tail: float = 0.377, gamma: int = 6000) -> list[float]:
    """[the two wells' sum at the Node between two pixels at s = 2, the pace Gamma less it] (R193: 2 x 853 = 1,706, open)."""
    total = 2 * round(wells(count, tail)[0])
    return [total, gamma - total]


if __name__ == "__main__":
    print("wells at 1, 2, 3 Links:", [round(w) for w in wells()])
    print("the Node between at s = 2, the pace left:", node_between())
