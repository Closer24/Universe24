# Why the orbit's inward legs read 1.5 shell means: the crossing rule on the fan, derived (the mathematician, read-only, 2026-09-21)

The auditor's round 9 on series D (the Boss's order of 2026-09-21, about
13:58Z; the shipped `s32_r12` and `s32_r24` and the generator's `s32_r16`,
`s32_r20`): per full turn the inward push the probe reads (DETECTOR, its
`read` lines, in units of the label's scale) over the sum of the shell law
`m q L / N(r_t)` at the radii it visits, pinned 1.00 +- 0.15, read 1.39,
1.20, 1.31 and 1.16 (FAIL on three of four); split by the probe's radial
motion, the inward legs read 1.52 against the crossing rule's Doppler
1.18 (`1 + v_r / c_h`, c_h = 32 / 55 the heading's pace) over 1536
intervals and the outward legs 1.08 against 0.73 over 2310. The question:
why does a reader stepping toward the source read more than its Doppler,
and stepping away the shell law and not the Doppler-reduced value; is the
excess the rule's (a double count on the fan) or nature's? Answered
read-only from [orbit_read_map.py](orbit_read_map.py) and its
[output](orbit_read_map.out): the crossing rule transcribed as
[crossing_2d.py](../crossing/crossing_2d.py) transcribes it (C1 the swap,
C2 the entered Node's residents against the step, C2' with it, C3 the
arrivals, C3' came with the body, C3'' the leapfrog), on series D's own
geometry (the plane, the fan of 120 in-plane directions, one shell of 120
rows every 10 intervals, the rows on the engine's own digital lines), with
readers on prescribed paths. Host arithmetic; no run; nothing registered
or decided.

## 1. The answer in one paragraph

The excess is neither a double count of the rule nor nature's: it is the
normalisation. The shell law `q L / N(r)` divides the rows by the ring's
Node count, but a digital line crosses the unit-wide ring at `S_1 / |D|`
Nodes (its Manhattan length per unit of Euclidean length), the fan's mean
1.287 (a fan uniform in angle gives 4 / pi = 1.273), so the mean reading
of a body at rest on the ring is 1.13 to 1.43 shell means at r = 8 to 28
(section 3). Series C's registered `C = 1.00 +- 0.10` was read on the six
headings, where `S_1 / |D|` is exactly 1, and does not carry to a fan. On
top of that constant the crossing rule reads the Doppler: exactly on the
axis (1.326, 1.204, 1.163 against 1.329, 1.205, 1.164 inward at k = 5, 8,
10; 0.674, 0.796, 0.837 against 0.671, 0.795, 0.836 outward; no row twice)
and within the grain on the fan's oblique lines and on an orbit-like path
(1.12 to 1.14 of the rest reading inward against the Doppler's 1.15 to
1.20; 0.87 to 0.89 outward against 0.81 to 0.85). The auditor's legs are
the product: 1.287 x 1.18 = 1.52 inward (read 1.52); outward 1.287 x 0.88
(the rule's outward reading on the fan) = 1.13 against the read 1.08, and
1.287 x 0.73 = 0.94 with the bare Doppler. One second meeting exists on the
fan, the plaquette leapfrog (section 2), 1 row in about 120 reads on the
orbit-like path and none on a radial path: named, not the 1.5.

## 2. The rule on the fan: the Doppler, and the one second meeting

| Reader (the map's sections B to D) | v_r / c_h | read / rest at the same Nodes | the Doppler `1 - v_r / c_h` | rows read twice |
| --- | --- | --- | --- | --- |
| on the axis, inward, k = 5, 8, 10 | -0.33, -0.21, -0.16 | 1.326, 1.204, 1.163 | 1.329, 1.205, 1.164 | 0 |
| on the axis, outward, k = 5, 8, 10 | +0.33, +0.21, +0.16 | 0.674, 0.796, 0.837 | 0.671, 0.795, 0.836 | 0 |
| on the lines (-1, -1), (-2, -1), (-5, -2), (-3, -7), inward, k = 8 | -0.15 to -0.16 | 1.129, 1.118, 1.136, 1.122 | 1.147 to 1.159 | 0 |
| the same lines outward | +0.15 to +0.16 | 0.879, 0.886, 0.870, 0.888 | 0.841 to 0.853 | 0 |
| orbit-like (the S = 32 pace 0.220 tangential, 0.11 radial), inward from r = 24 | -0.20 | 1.135 | 1.195 | 0 |
| orbit-like, outward from r = 14 | +0.19 | 0.880 | 0.813 | 1 of 120 |
| a circle at r = 19, no drift | 0.00 | 1.055 | 0.997 | 0 |

The rest reading is the same Nodes read by a body at rest (every line
through the Node delivers one row per 10 intervals, read once at its
arrival). On the axis the rule is the Doppler to the third digit, the
proof of the crossing design (section 2, "why each row is read once"). On
an oblique line the rule reads 0.03 to 0.06 less than the Doppler in
magnitude either way, the grain of the digital lines (the crossing
design's own numbers beyond the axis: 36 in 32 against the step on the
face diagonal and 24 in 32 with it); no row is read twice on any radial
path, so there is no double count on the fan.

**The one second meeting**, on the orbit-like path (the map's trace): a
row of the line (7, 2) arrives at (75, 64) at the tick 226 while the
reader is there (C3, read); at 227 the row rests and the reader steps +y
to (75, 65); at 228 the row steps +x to (76, 64) and the reader +x to
(76, 65); at 229 the row steps +y to (76, 65), the reader's Node, with the
reader at rest: an arrival with e = 0, e' = +x and s_1 = +y, so C3'' (s_1
= e') does not apply and the row is read again. The two went round the
two sides of one plaquette and met at its opposite corner: two meetings
of world lines that touch and do not cross, which the two one-Link marks
cannot see. It is the plane's, not the axis's; 1 read in about 120 on the
orbit-like path, 0.8 percent, of one sign (a re-read), and not the source
of a 30 percent excess. Named for the crossing design's proof (which
covers the heading stream): a fan case for its test list, not a bug of
the implementation (`nature_beam.py` :3110-3142 is the design as written).

## 3. The normalisation: the Manhattan factor of the ring

| r | N(r) | the lines' Node-visits on the ring | per line | ring Nodes on no line | the ring mean of the rest reading over `q L / N(r)` |
| --- | --- | --- | --- | --- | --- |
| 8 | 48 | 136 | 1.133 | 0 | 1.132 |
| 12 | 68 | 144 | 1.200 | 8 | 1.199 |
| 16 | 112 | 164 | 1.367 | 12 | 1.366 |
| 20 | 112 | 136 | 1.133 | 16 | 1.134 |
| 24 | 144 | 160 | 1.333 | 24 | 1.333 |
| 28 | 184 | 172 | 1.433 | 40 | 1.433 |

The shell law counts one Node per line per ring (Gauss on the ring, the
form DERIVATIONS_BEAM 3.2 reaches in the shell mean); a digital line of
direction D crosses the unit-wide ring `abs(dist - r) < 1 / 2` at
`S_1 / |D|` of its Nodes on average, `(abs(a) + abs(b)) / sqrt(a^2 +
b^2)`, the fan's mean 1.287, so the rows' arrivals per ring are `q x
1.287`, the ring mean of what a body reads is 1.29 shell means, and the
ring's ripple (1.13 to 1.43) is which lines hit which ring. A body
reading at a Node reads every row once; the sum over the ring's Nodes
counts a row at each ring Node it visits, and the orbiting probe, which
visits many ring Nodes, reads the per-Node rate: its time mean is the
ring mean of the per-Node reading, `1.29 q L / N(r)`, not the flux `q L /
N(r)`. Series C's `C = 1.00 +- 0.10` is exact on its six headings
(`S_1 / |D| = 1`) and is the registered evidence for the derivation's
`C = 1` (the orbit README (`examples/events/orbit/README.md`, deleted 2026-09-26),
"C = 1 (taken; series C: 1.00 +- 0.10)"); on the 120-direction fan the
constant is the Manhattan mean, and the auditor's C_naive (1.87, 1.33,
1.29) and C_shell (1.39, 1.20, 1.31, 1.16) are this constant times the
legs' Doppler times Jensen's `<1 / r_t> <r_t>`, as the auditor
decomposed them.

## 4. What it says of the register's D pin, and of nature's orbit

- **The crossing rule as written: MET.** The Doppler exactly on the axis
  and within the grain on the fan; the plaquette leapfrog the one second
  meeting, small and named. No bug report.
- **The pin `C = 1.00 +- 0.10` on the fan, as a hypothesis: REFUTED by the
  lattice's own lines**, not by the run: on a fan the flow constant a
  body reads is the fan's Manhattan mean `<S_1 / |D|>` = 1.287 (4 / pi in
  the limit of every direction), which the six headings hid. The ring
  count is not the cause (the auditor's `C_cont` within 0.02 of
  `C_shell`): `N(r)` and `2 pi r` both count Nodes once.
- **Nature's orbit: DIFFERENT LAW in the constant, the same form.** Gauss's
  flux through a ring is 1 in nature; on the GameBoard an isotropic fan
  delivers 4 / pi of it to a body (the digital ring's Manhattan perimeter
  8 r over 2 pi r), the `1 / r` form on the plane and the `1 / r^2` form
  in space unchanged. What it moves: the circular-orbit momentum of the
  S = 32 worlds with `C = 1.287` is 10.18 label units (the whole 10) in
  place of 8.83 (the register's 9), the pace 0.238 in place of 0.220, the
  period at r = 12 317 intervals in place of 343 and at r = 24 633 in
  place of 687 (the map's G); the registered orbits, launched at n = 9
  from `C = 1`, read a push 1.29 times the one they were derived for, and
  their radial legs are that under-speed's. A NATURE row (the Boss named
  24.3) only on the Boss's word, after this answer.

**What this note does not decide.** No run; the auditor's numbers are the
register's. The map's orbit-like path is synthetic (one axis per interval,
x before y, an ideal circle with a drift); the registered orbits' Nodes may
sample the lines differently, and the replicator can read the register's
runs directly: the mean over the probe's visited Nodes of the lines' count
against `q L / N(r_t)` is the rest factor, and the legs' `read / rest` the
rule's Doppler on the fan, the two numbers this note predicts as 1.2 to
1.34 and 1.13 / 0.88.

## 5. Links

[The crossing rule](../crossing/DESIGN.md) (section 2, the criterion and
the proof on the axis; section 5 (c) beyond the axis) and its
[independent count](../crossing/crossing_2d.py);
[DERIVATIONS_BEAM 3.2](../../DERIVATIONS_BEAM.md#32-the-far-field-a-beam-does-not-dilute-a-shell-does)
(the shell mean and the ring counts);
series D (`examples/events/orbit/README.md`, deleted 2026-09-26) and
its generator (`examples/events/orbit/make_worlds.py`, deleted 2026-09-26);
[BEAM_LAW section 3](../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
step 4 and note 48.
