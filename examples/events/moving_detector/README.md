# The moving detector, a cart with a click

The model owner's word of 2026-09-22 (record 816 of
[docs/LOG_2026-09-20.md](../../../docs/LOG_2026-09-20.md): "we no longer
need a wall; we need a cart with a click"; record 824: "make sure we know
how to run in the code Outside with a moving detector, consecutive
clicks"). The design, with every pin written from the Inside step and the
conversion before any run, is
[docs/designs/moving_detector/DESIGN.md](../../../docs/designs/moving_detector/DESIGN.md);
this folder holds the six worlds it declares, written by `make_worlds.py`,
and `expectations.json`, the pins. The physics-rule reviewer read the design
ADMISSIBLE (his four lines folded). Nothing is registered as a measurement of
nature yet.

## The worlds

A bar of 240 x 3 x 3 Nodes (320 for the quantum world), open, no crowd, no
key of a hypothesis, series O's numbers (N = 64, K = 2^22 + 2^13, Q = 64, the
width 2^20). Three measured events on the axis: the post R (fixed at x = 1,
the transponder: the cart's pulses re-emitted on +x by the rule `rerelease`,
stamped with its number), the lamp A (the family `source`, fixed at x = 3, one row per
self-creation on +x), and the cart D (the moving body detector: from x = 20
at the pace v = 1 / k Nodes per self-creation exactly, a lamp of its own on
-x, its table measuring the lamp's rows and its own returned pulses). Every
world declares the key `clock_stamp`, so every line a measured event writes
carries `clock`, its own count of self-creations; the reading tool reads
nothing of the tick.

| World | k | the pace v | beta = v / c | the bar | intervals | model id |
| --- | --- | --- | --- | --- | --- | --- |
| `cart_k3.json` | 3 | 1/3 | 55/96 | 240 | 600 | `beam-moving-detector-cart-k3-v1` |
| `cart_k5.json` | 5 | 1/5 | 11/32 | 240 | 600 | `beam-moving-detector-cart-k5-v1` |
| `cart_k9.json` | 9 | 1/9 | 55/288 | 240 | 600 | `beam-moving-detector-cart-k9-v1` |
| `cart_k17.json` | 17 | 1/17 | 55/544 | 240 | 600 | `beam-moving-detector-cart-k17-v1` |
| `cart_quantum.json` | 7/3 | 3/7 (the hops at gaps 2, 2, 3) | 165/224 | 320 | 600 | `beam-moving-detector-cart-quantum-v1` |
| `capability_k5.json` | 5 | 1/5 | 11/32 | 120, no post | 300 | `beam-moving-detector-capability-k5-v1` |

c = 32 / 55 Nodes per interval on a heading (the flight table's pace). The
cart's momentum is `Q S M / (k - 1)` (`3 Q S M / 4` for the pace 3 / 7), M
the content the drive's wall reads (the held mass 2^22 plus the light 2^13),
whole in every world. `capability_k5` is the smallest world of the design's
step 4 (the lamp and the cart only). Every world declares `per_axis_drive`
since the merge of 2026-09-22 with the law's line drive (the model owner's
record 972, [DEFAULT.md](../../../docs/designs/drive_b/DEFAULT.md)): its
momenta and pins are the per-axis drive's (`v = p / (Q S M + p)` exactly),
the drive of history under which they were derived and read; the key is
transient and goes when this series is re-pinned under the law.

## The pins, before any run (the design's section 5)

**Superseded on the radar velocity's sign (issue #937, 2026-09-22): the
coordinate `x_D = c (n_r - n_e) / 2` gives `+ v`; the versioned
preregistration is
[docs/designs/moving_detector/PREREGISTRATION_V2.md](../../../docs/designs/moving_detector/PREREGISTRATION_V2.md),
and `expectations.json`'s `radar_velocity` pins below are version 1's,
kept as written until the build commit before the rerun (the owner's
word). The five-world run of batch 933 on `main` at 4376712e read the
radar velocity `+ 0.3323`, `+ 0.2008`, `+ 0.1105`, `+ 0.0584`, `+ 0.4279`
against `- 1/3`, `- 1/5`, `- 1/9`, `- 1/17`, `- 3/7`: five FAILs, recorded
as such in version 2's section 4.**

At the law's rate r = 1, beta = 55 / (32 k): `k_AB` = 1 / (1 - beta) (the
cart's counts apart over the lamp's ordinals apart; the missing direction of
the click frame), `k_BA` = 1 + beta (the post's counts apart over the cart's
ordinals apart), the ratio `k_BA / k_AB` = 1 - beta^2 (the law's number,
stated so that it fails against the comparison 1, Lorentz's one symmetric
factor; it carries r_R / r_D^2), the round trip (1 + beta) / (1 - beta) (a
ratio of the cart's own counts, r cancels), the radar velocity -v, the least
step (the Node's change at most one per count between any two clicks; 0 or
1 between consecutive clicks of the lamp's rows in the k worlds, 1 or 2 in
the quantum world), the pace over the window v. The windows: the one-way
factors from the cart's 60th count; the round trip and the radar from the
first return (153, 100, 81, 73 and 248 counts). Tolerance 2 / W over a window
of W counts. Every number is in `expectations.json` as a fraction.

## Run and read

```bash
PYTHONPATH=src python examples/events/moving_detector/make_worlds.py
PYTHONPATH=src python tools/run_series.py --out artifacts/moving_detector examples/events/moving_detector/capability_k5.json
PYTHONPATH=src python tools/moving_detector_readings.py artifacts/moving_detector --capability
```

The run is the model owner's word (step 4, the capability check on
`capability_k5`: the consecutive clicks printed as DETECTOR, the pins as
"read / not read" only; the transponder worlds after the reviewer's read of
the build). `tests/test_moving_detector.py` pins the shipped worlds to the
generator, the pins to the closed forms, and the key's field.

## The capability run (step 4, 2026-09-22)

The model owner's word of record 824 ("make sure we know how to run in the
code Outside with a moving detector, consecutive clicks"), as the Boss gave
it: one run of `capability_k5` through `tools/run_series.py` (300
intervals, completed, the books balanced at every interval, the source
9a189f6b8f53, the record's digests under `runs` of
`expectations.json`), read by `tools/moving_detector_readings.py
--capability`: the cart's consecutive clicks of the source's rows printed
as DETECTOR (its own count `clock`, its Node, the ordinal the packet
brought; the differences, the Outside step of record 803: the first
clicks at the counts 44, 47, 48, 49, 52, 53, 54, 57 at the Nodes 28, 29,
29, 29, 30, 30, 30, 31, the ordinals 1 to 8), 168
clicks in all. Nothing is pinned as nature's; the design's pins for that
world are said read or not read only: `k_AB` read, 1.5159 over
238 counts (the closed form 32 / 21 = 1.5238 stands beside it, not
compared); the least step read, the Node's change between consecutive
clicks {'0': 116, '1': 51} and at most one per count; the pace over the
window read, 0.1975 Nodes per count (the closed form 1 / 5).
GAMEBOARD, labelled: 60 step lines, the intervals between hops
{'5': 59}; the cart's final age 300 against 300 intervals;
every line's tick, read by nothing above. The transponder worlds wait on
the physics-rule reviewer's read of the build and on the owner's word.

## The register entry, drafted (not registered until the model owner says so)

- **Confronts.** The missing direction of the click frame, `k_AB`, a lamp at
  rest counted on a moving detector's own count; with `k_BA` the ratio that
  decides between the law's `1 - beta^2` and Lorentz's 1; the radar velocity;
  the quantum of the Outside step.
- **Reads.** DETECTOR: the cart's clicks (its own count, its Node, the
  ordinal read); the post's re-release lines (its own count, the cart's
  ordinals). GAMEBOARD, labelled: the tick of every line, the step lines.
- **Predicts.** The pins above, the law's own numbers; the ratio fails
  against nature's 1 at second order, as NATURE row 4b already reads.
