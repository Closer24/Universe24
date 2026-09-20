# The label rotation per Link: the admissible integer form and bounds (read-only, the mathematician, 2026-09-20)

On the Boss's assignment under [record 119](../../LOG_2026-09-20.md)
(item 5: a record's label rotated at every Link of flight by a declared
setting, the neutrino's three family labels as the qubit's, the click
reading the family). The physicist's design is written in parallel; this
file gives the integer form that keeps the click's integers exact, its
bound against the register's ceiling over L Links, and the three-label
case with the expected counts at three distances at N = 64 from a
standalone map before any run. Every integer is from `rotation_map.py`
beside this file (`rotation_map.out`; the tables of 2N from the engine's
own `phase_cosines`). Nothing is built; no run.

## 1. The fact, and why a rotation applied per Link cannot be

The design's rotation of a label bit (amplitude-v1 section 2.2) applies
`U_s = [[C'[s], S'[s]], [-S'[s], C'[s]]]` on the half-angle tables of 2N at
scale 256: `U_s^T U_s = n_s I` exactly with `n_s = C'^2 + S'^2`, which over
the 128 settings at N = 64 runs from 65 242 to 65 824 and is 65 536 only
where an entry is 0 or 256 (`rotation_map.out` A; record 105 settled the
norm for one rotation). A rotation applied at every Link multiplies the
amplitudes by n_s per Link and the row's multiplicity by 65 536 per Link:
`65536^L` passes 2^62 at L = 4 (2^64), and a path of 64 Links would need
2^1024. **Applying the tables per Link is not admissible** on the register,
whatever the setting; the norm's drift (n_s / 65536 within 0.44 %) is the
smaller problem.

## 2. The admissible form: an angle index added per Link, the tables once at the click

A rotation by the setting s per Link is a rotation by the angle pi s / N
per Link about the same label bit, and rotations about one bit compose by
the addition of their angles exactly. So the record carries, per rotating
label bit, **an angle index** sigma in [0, 2N) on the row (one int16
column beside `phase`, which is the same kind of register: `phase` is an
index added per Link mod N by `phase_per_link`), advanced by the family's
declared `label_turn_per_link` s at every Link crossed, mod 2N, and never
applied on the lattice. At the click a set that reads the bit applies the
tables ONCE at the composed index, `U_{(sigma + a) mod 2N}` with a the
set's own setting (the analyser), and takes its channels' residual
amplitudes from that one matrix: the multiplicity is multiplied by 65 536
once per click, whatever L, and the only rounding is the one lookup, the
same rounding the design's window already makes (within 0.36 % in the
norm). Exact composition, one rounding, no growth.

Bounds: sigma < 2N <= 8192 (int16); the addition per Link is the phase's;
the click's product as the design's rotation (the birth's norm times
65 536, within the ceiling for every path length; three such lookups per
path fit, as the design's ceiling says, and a per-Link angle costs none of
them). Refusals: `label_turn_per_link` outside 0 .. 2N - 1; the key on a
family without a phase circle; the key without the world key `amplitude`.
Locality: the angle is on the row, advanced where the row is, read where
it clicks. Identity: under `amplitude-v1` as a further key, no third
identity; absent, no row carries an angle and every world is byte-identical.

The two-label counts at three distances (`rotation_map.out` B; a row born
on label 0, s = 3 per Link, the analyser at a = 0, the counts over the 64
births by the design's ladder):

| L | sigma = 3 L mod 128 | (C', S') | weights (+, -) | counts (+, -) | cos^2, a report |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | (256, 0) | (65536, 0) | (64, 0) | 1.000 |
| 5 | 15 | (190, 172) | (36100, 29584) | (35, 29) | 0.549 |
| 10 | 30 | (25, 255) | (625, 65025) | (1, 63) | 0.010 |
| 16 | 48 | (-181, 181) | (32761, 32761) | (32, 32) | 0.500 |
| 32 | 96 | (0, -256) | (0, 65536) | (0, 64) | 0.000 |
| 64 | 64 | (-256, 0) | (65536, 0) | (64, 0) | 1.000 |

The period of the reading is 2N / gcd(s, 2N) Links in the index and N / s
Links in the counts (the sign of the amplitude is not read): an
oscillation of the click's channel along the path, exact.

The alternatives asked about: a rotation every k Links applies the tables
L / k times and multiplies the multiplicity by 65 536 each time, so k must
exceed L / 3 on every path: not a per-Link rule, and it rounds L / k times;
a renormalisation per Link would divide the amplitudes by 256 and the
multiplicity by 65 536 after each application, which the normal form does
only when every amount divides exactly (the design's 2.2) and which
otherwise discards a remainder with no owner: not admissible. The angle
index is the one form that is exact, bounded and local.

## 3. Three labels: the neutrino's families

A rotation on three labels from two settings is a product of two plane
rotations (Givens), `U = R_23(s23) R_12(s12)` with theta_13 = 0, its
entries products of two table entries at scale 65 536 (`rotation_map.out`
C: for s12 = 11 and s23 = 16 of 2N = 128, the angles 30.9 and 45 degrees,
`U = [[56320, 33792, 0], [-23892, 39820, 46336], [23892, -39820, 46336]]`,
the rows' norms within 0.44 % of 65536^2). Two plane rotations on
different pairs do NOT commute, so a three-label "rotation per Link" has
no angle index: `(R_23 R_12)^L` is not `R_23(L s23) R_12(L s12)`, and the
per-Link application is refused by section 1 anyway. The form that is
exact, bounded, and the physics of oscillation, is the one the design
already has the pieces for:

1. **the mixing at the birth**: the lamp's `branches` declare the flavour's
   row of U as the labels' amplitudes (flavour 0: `[56320, 33792, 0]` at
   scale 256 of one table entry, the norm 2^16);
2. **a phase per Link per label**: `phase_per_link` declared PER LABEL of
   the family (three rates, the mass differences; today one rate per
   family), an addition mod N per Link on each label's rows: exact, no
   table, no growth;
3. **the analyser at the click**: the set reads the flavour beta as the
   row beta of U applied once to the three labels' amplitudes at their
   phases, `a_beta = sum_j U[beta][j] U[0][j] (C[phi_j], S[phi_j])`, the
   weights `|a_beta|^2` per channel, the ladder over the three channels.

The multiplicity: the birth's norm 2^16 times the click's 2^32 = 2^48 per
path, within 2^62; a mixing applied per Link would multiply by 2^32 per
Link and pass the ceiling at the second Link. The exactness: the phases
are exact; the two matrices are each one lookup's rounding; the weights
are Python integers of the layer's report (never refused).

The expected counts at N = 64 for that one declared mixing and the phase
rates (0, 5, 9) steps per Link on the three labels, a record born as
flavour 0 read at an analyser of the three flavours, over 64 births
(`rotation_map.out` C; the probabilities beside them are a report):

| L | phases (0, 1, 2) | counts (0, 1, 2) | P (report) |
| --- | --- | --- | --- |
| 0 | (0, 0, 0) | (64, 0, 0) | 1.000, 0, 0 |
| 8 | (0, 40, 8) | (21, 22, 21) | 0.336, 0.332, 0.332 |
| 16 | (0, 16, 16) | (39, 13, 12) | 0.611, 0.195, 0.195 |
| 24 | (0, 56, 24) | (57, 3, 4) | 0.886, 0.057, 0.057 |
| 32 | (0, 32, 32) | (14, 25, 25) | 0.221, 0.389, 0.389 |
| 64 | (0, 0, 0) | (64, 0, 0) | 1.000, 0, 0 |

Three distances for the run, L = 8, 16, 32 (the flavour-0 counts 21, 39,
14 of 64, the other two flavours equal at this mixing since theta_23 = 45
degrees puts them symmetric): the survival of the born flavour oscillates
along the path and the two others appear, which is what the design's
click "reading the family" must show, at these integers, before any run.
The period on this table is N / gcd of the rates (64 Links for the rates
5 and 9); a different mixing or rate is one declaration and the same map.

## 4. The verdict in one line

Admissible: the label's angle index added per Link mod 2N with the tables
applied once at the click (exact composition, one rounding, the multiplicity
65 536 once, bounded for every L, local); a rotation applied per Link is
not (the ceiling at the fourth Link); for three labels the mixing at the
ends with a phase per Link per label, 2^48 per path, and the counts above
as the pinned expectation of the first run.
