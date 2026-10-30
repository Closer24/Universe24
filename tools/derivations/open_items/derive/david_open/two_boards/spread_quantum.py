"""One quantum spread over many absorbers, on the doubled Node-clock: what the backward half brings to the source.

David's probe for the Boss's ask under decision 31 (comment 6493855395: "what the backward half brings to a spread
quantum's source (the absorbers' takes), and what it brings to a pair's birth (the frames)"), on the owner's word to
the Boss of 10:0x UTC ("Better to see it as one board with doubled Node-clocks, which simulates a double board, no?
Let the clicks be derived exactly from the full picture").

usage: python3 -I spread_quantum.py

The backward dial holds a fixed count per Node-clock, so the takes of many absorbers cannot ride back to the source each
on its own: they would need a count that grows with the absorbers. So they ride back merged:
  pass 1, forward: the quantum spreads; each Node-clock learns its tick of arrival, and each absorber its share, the
          forward size sigma_f (here a whole number given per absorber);
  pass 2, backward, one Mesh a sweep from the farthest to the source: each Node-clock adds its own take (sigma_f
          sigma_b where an absorber stands) to the totals of the branches that reach it from one Mesh farther, draws
          one branch by the rank count over those totals, d = (c + V) mod total, keeps the branch drawn, and passes the
          total on to its parent, the neighbour one Mesh nearer the source;
  pass 3, forward: from the source, the word follows the branches drawn, out to one absorber, which clicks.
Each Node-clock keeps two integers more in its backward dial (the total and the branch drawn) and reads only its six
neighbours. The parts that need the word are named in pass 3 alone, so no click is written before pass 2 ends.
Checked, in exact fractions and by enumeration:
  1. each absorber wins with odds exactly its take over the sum of the takes (the telescoping product of the branch
     draws), on two different trees (two Spoke orders for the parent), so the law does not depend on the tree;
  2. a silent future (sigma_b alike) gives Born over sigma_f; an absorber with no free slot (sigma_b = 0) never wins;
  3. on a small board, every combination of the merges' digits over their full turns is enumerated: each absorber is
     drawn exactly its take's share of the joint turn, and exactly one absorber clicks at every combination (g2 = 0).
"""

from fractions import Fraction
from itertools import product
from math import prod

SPOKES = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def nonneg(n: int) -> int:
    """The one whether: 1 where n is at least 0 and 0 below."""
    return n // (n * n + 1) + 1


def drawn(n: int, sizes: list[int]) -> int:
    """The rank count: the part whose cumulative interval holds d = n mod L, with no sort and no if."""
    total = sum(sizes)
    d = n % total
    part, run = 0, 0
    for s in sizes[:-1]:
        run += s
        part += nonneg(d - run)
    return part


def board(side: int):
    """A cube of side `side`, wrapped on no axis, the source at its centre; the tick of arrival is the Mesh distance."""
    sites = [(x, y, z) for x in range(side) for y in range(side) for z in range(side)]
    c = side // 2
    source = (c, c, c)
    arrival = {s: sum(abs(a - b) for a, b in zip(s, source, strict=True)) for s in sites}
    return sites, source, arrival


def parents(sites, arrival, order):
    """Each Node-clock's parent: its first neighbour, in the given Spoke order, one Mesh nearer the source."""
    up = {}
    for s in sites:
        if arrival[s] == 0:
            continue
        for k in order:
            n = tuple(a + b for a, b in zip(s, SPOKES[k], strict=True))
            if n in arrival and arrival[n] == arrival[s] - 1:
                up[s] = n
                break
    return up


def branches(sites, up):
    """For each Node-clock, its children: the Node-clocks whose parent it is, in a fixed order."""
    kids = {s: [] for s in sites}
    for s, p in sorted(up.items()):
        kids[p].append(s)
    return kids


def totals(sites, arrival, kids, takes):
    """Pass 2's totals, from the farthest Node-clocks to the source: a Node-clock's own take plus its children's."""
    tot = {}
    for s in sorted(sites, key=lambda q: -arrival[q]):
        tot[s] = takes.get(s, 0) + sum(tot[k] for k in kids[s])
    return tot


def odds(sites, source, arrival, kids, takes) -> dict:
    """Each absorber's odds of winning: the product of the branch draws' odds along its path from the source."""
    tot = totals(sites, arrival, kids, takes)
    out = {}
    for a in takes:
        p = Fraction(1)
        s = a
        chain = []
        while s != source:
            chain.append(s)
            s = next(q for q in sites if s in kids[q])
        chain.append(source)
        # at the absorber itself the part is its own take; at every Node-clock above, the branch it lies in
        p = Fraction(takes[a], tot[a]) if tot[a] else Fraction(0)
        for child, node in zip(chain[:-1], chain[1:], strict=True):
            p *= Fraction(tot[child], tot[node]) if tot[node] else Fraction(0)
        out[a] = p
    return out


def part_one_two() -> list[str]:
    sites, source, arrival = board(7)
    c = 3
    # seven absorbers at several distances and directions, the escape at a far corner; sigma_f given, sigma_b their takes
    forward = {
        (c + 3, c, c): 5,
        (c, c - 3, c): 3,
        (c, c, c + 2): 4,
        (c - 2, c + 2, c): 2,
        (c + 1, c + 1, c - 3): 6,
        (c - 3, c - 3, c - 3): 1,
        (c + 2, c - 2, c + 2): 7,
        (0, 6, 6): 2,  # the escape: the share that reaches no absorber, taken at the board's edge
    }
    backward = dict.fromkeys(forward, 1)
    backward[(c - 2, c + 2, c)] = 0  # an absorber with no free slot
    backward[(c, c, c + 2)] = 2  # an absorber with two slots
    out = []
    trees_agree = True
    exact = True
    for order in ([0, 1, 2, 3, 4, 5], [5, 3, 1, 4, 2, 0]):
        kids = branches(sites, parents(sites, arrival, order))
        takes = {a: forward[a] * backward[a] for a in forward}
        law = odds(sites, source, arrival, kids, takes)
        total = sum(takes.values())
        exact &= all(law[a] == Fraction(takes[a], total) for a in takes)
        trees_agree &= law == odds(
            sites, source, arrival, branches(sites, parents(sites, arrival, [0, 1, 2, 3, 4, 5])), takes
        )
    out.append(
        f"  each absorber wins with odds its take over the sum of the takes, on two trees: {exact}; the two trees' "
        f"laws equal: {trees_agree}"
    )
    kids = branches(sites, parents(sites, arrival, [0, 1, 2, 3, 4, 5]))
    silent = odds(sites, source, arrival, kids, dict(forward))
    born = all(silent[a] == Fraction(forward[a], sum(forward.values())) for a in forward)
    full = odds(sites, source, arrival, kids, {a: forward[a] * backward[a] for a in forward})
    out.append(
        f"  a silent future (sigma_b alike) gives Born over sigma_f: {born}; the absorber with no free slot wins with "
        f"odds {full[(c - 2, c + 2, c)]}; the absorber with two slots: {full[(c, c, c + 2)]} "
        f"(4 x 2 over {sum(forward[a] * backward[a] for a in forward)})"
    )
    return out


def part_three() -> list[str]:
    """A board of side 5 with five absorbers, three on one path: every combination of the merges' digits, enumerated."""
    sites, source, arrival = board(5)
    c = 2
    # (c + 2, c + 1, c), (c + 1, c + 1, c) and (c, c + 1, c) lie on one path to the source, so the merges nest
    takes = {
        (c + 2, c + 1, c): 2,
        (c + 1, c + 1, c): 1,
        (c, c + 1, c): 2,
        (c, c + 1, c + 1): 3,
        (c, c, c - 2): 1,
    }
    kids = branches(sites, parents(sites, arrival, [0, 1, 2, 3, 4, 5]))
    tot = totals(sites, arrival, kids, takes)

    # the merges that draw: Node-clocks with two or more parts that are not 0 (its own take and its children's totals)
    def parts_of(s):
        return [takes.get(s, 0)] + [tot[k] for k in kids[s]]

    drawing = [s for s in sites if sum(1 for v in parts_of(s) if v) >= 2]
    turns = [tot[s] for s in drawing]
    wins = dict.fromkeys(takes, 0)
    one_click = 0
    combos = 0
    for digits in product(*[range(t) for t in turns]):
        pick = dict(zip(drawing, digits, strict=True))
        # pass 3: from the source, follow the branches drawn
        s = source
        while True:
            ps = parts_of(s)
            if s in pick:
                k = drawn(pick[s], ps)
            else:
                k = next(i for i, v in enumerate(ps) if v)
            if k == 0:
                break
            s = kids[s][k - 1]
        clicked = [a for a in takes if a == s]
        one_click += len(clicked) == 1
        wins[s] += 1
        combos += 1
    total = sum(takes.values())
    exact = all(wins[a] * total == takes[a] * combos for a in takes)
    return [
        f"  merges that draw: {len(drawing)}, their turns {turns}, the joint turn {prod(turns)} combinations",
        f"  each absorber drawn exactly its take's share of the joint turn: {exact} "
        f"(wins {[wins[a] for a in takes]} for takes {[takes[a] for a in takes]})",
        f"  exactly one absorber clicks at every combination (g2 = 0): {one_click} of {combos}",
    ]


def main() -> None:
    lines = [
        "One quantum spread over many absorbers, on the doubled Node-clock (David, 2026-10-29): exact",
        "",
    ]
    lines.append(
        "1 and 2. The takes merged back along the backward half, on a board of side 7 with eight parts"
    )
    lines.extend(part_one_two())
    lines.append("")
    lines.append(
        "3. Every digit of every merge, on a board of side 5 with five absorbers, the merges nested"
    )
    lines.extend(part_three())
    print("\n".join(lines))


if __name__ == "__main__":
    main()
