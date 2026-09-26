# The comb against the fan's density: a held mass's crowd on the lattice at five fan bounds (the chief physicist, host algebra, no run)

The Bending Algebraist's step algebra
([STEP_ALGEBRA.md](STEP_ALGEBRA.md), section 8) found the reason the
bending's coefficient is not 4 and grows with the impact distance b on
series K's in-plane beam: the fan's comb. The transverse flow a light row
sums along its path, in the mass's plane at the fan of 290 directions,
is 2.1 to 8.3 times the continuum's value that the coefficient
`alpha = 2 c_f (n S / d) G M / (c^2 b)` was taken in. The model owner's
word of 2026-09-22 ("continue with the checks to close the atom and the
light bending") asked what the comb does as the fan grows. This note
answers by the same map (`step_algebra_map.py`'s `Crowd`, one row per
direction per interval, the flight rule's dwell at every Node, the flow
the label per arriving row), re-run at five fan bounds by
`comb_map.py` (`docs/designs/light_bending/comb_map.py`, deleted 2026-09-26) (its output [`comb_map.out`](comb_map.out)).
Every number is GAMEBOARD by formula, a host arithmetic of the lines;
nothing here is a detector's reading and nothing is pinned.

## The table

The fan: every primitive direction with `|a| + |b| + |c| <= bound`
(series K's 290 at bound 6). The path sum: the flow's transverse
component `V_y` at the Nodes `(x, b, 0)` of the heading from x = -26 to
25, times the row's dwell there, against the continuum's
`2 q Q b / (4 pi) x L / (b sqrt(L^2 + b^2)) x sqrt 3` (section 8's ratio;
the bound 6 row reproduces section 8 and its `F_L1` exactly). `F_L1`: the
shell mean of `|V| r^2 / Q` over r = 4 .. 14 against `q / (4 pi)`. `A r / q`:
the age moment's shell mean times r over the fan's count, at r = 4, 8, 12,
14 (a constant is Newton's 1 / r). The crossed fraction: the share of a
shell's Nodes that any line of the fan passes, at r = 6 and 12. The spread:
the coefficient of variation of the age moment over the shell's Nodes,
at r = 6 and 12.

| bound | q | path sum / continuum at b = 3, 6, 8, 10, 14 | `F_L1` | `A r / q` at r = 4, 8, 12, 14 | crossed fraction, r = 6, 12 | spread of A, r = 6, 12 |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 290 | 2.08, 3.34, 4.09, 5.83, 7.25 | 1.421 | 0.239, 0.267, 0.255, 0.234 | 0.63, 0.20 | 0.98, 2.17 |
| 8 | 674 | 2.11, 2.80, 2.93, 4.44, 5.76 | 1.408 | 0.247, 0.265, 0.267, 0.224 | 1.00, 0.45 | 0.66, 1.42 |
| 10 | 1250 | 1.95, 2.12, 2.38, 3.26, 4.14 | 1.420 | 0.244, 0.250, 0.254, 0.255 | 1.00, 0.66 | 0.46, 1.03 |
| 12 | 2114 | 1.87, 1.88, 2.09, 2.78, 3.39 | 1.425 | 0.243, 0.240, 0.257, 0.239 | 1.00, 0.87 | 0.38, 0.72 |
| 16 | 4898 | 1.81, 1.69, 1.72, 2.11, 2.51 | 1.426 | 0.241, 0.244, 0.230, 0.232 | 1.00, 1.00 | 0.44, 0.45 |

## The reading

The potential is Newtonian on the shell average at any fan (`A r / q`
constant in r to within its grain at 290 directions already, `F_L1` the
same 1.41 to 1.43 at every bound), while the field at a Node is a comb
whose teeth close only with a fan of thousands (the crossed fraction at
r = 12 from 0.20 to 1.00, the spread from 2.2 to 0.45); a single beam in
the mass's plane sums the teeth and converges slowly (the ratio still 1.7
to 2.5 at 4898 directions, and still growing with b), whereas the ring of
starts of STEP_ALGEBRA.md section 9, the orientation average, converges at
once. So the ring is the right instrument for the bending's row and no
denser fan is needed for it; the coefficient the ring reads, 5.1 to 5.9
tending to 6 = 4 x 3 / 2, is the label-per-Node factor `F_L1` on top of
the declared 4, which the push's label per Euclidean Link
(`flow-link-v1`) removes and a denser fan does not.

## What this note does not say

Nothing about the atom: the hydrogen world's fan is 2616 directions
(bound 12 here, the comb mild), and its loop's widening is the pulsed
crowd's kicks and the fan's grain (docs/designs/atoms/PINS.md items 3 and
4), not the comb of this table; the bound the atom needs is a separate
algebra. Nothing is run; no pin moves; the Algebraist's files are
untouched.

> The scripts of this folder (`comb_map.py`, `step_algebra_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/light_bending/<script>`).
