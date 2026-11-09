# log_symmetry_v1: pre-registration (r17)

Written 2026-11-09 04:20 UTC, before any code of this layer. Name and scope follow r16b (ARCHITECT_REPORT4 section
3) and the coordinator (04:20): ONE frozen layer `log_symmetry_v1` of click_decoder_v1, declared and read-only,
frozen on its own (`FROZEN_log_symmetry_v1.json`), developed in `research/matter_light_v1/r17/layers_dev/`
outside the released package, released only through a new package release with r16b's review.

It supersedes `click_mirror_v1` (pre-registered 04:14, frozen 04:17:00Z, validated 04:18, all cases passed;
it stays in layers_dev as a record and is not released). log_symmetry_v1 reuses its frozen logic and adds the
behaviour of r36's four read-only observers (r36/c1.py `cycle_compare_v1`, `phase_split_v1`, `mirror_check_v1`;
r36/c3.py `spin_image_v1`), which per UPDATE 8 move from experiment code into this decoder layer.

## Definitions
Input: a click log (path) or its records. A record is (t, x, y, z, g, k, q), read from `step`, `address`, `kind`,
`quotient` only, except in `period(..., full_records=True)`, which compares complete records.
* **mirror(log, tau)**: the partner of (t, x, y, z, g, k, q) is (2 tau + 1 - t, x, y, z, g, -k mod 3, -q); tau is
  an integer or a half-integer. Reported: records, paired, unpaired (count, per update, first records); and, as
  r36's `mirror_check_v1`, the number of updates n in a declared range whose record set equals the mirror image of
  the set at 2 tau + 1 - n (`steps_mirrored`), with the silent updates.
* **best_tau(log)**: the tau that pairs the most records; whether it is unique; the runner-up.
* **period(log, P, t0=0, horizon=None, full_records=False)**: cycle j = updates t0 + jP + 1 .. t0 + (j + 1)P, times
  shifted to 1..P. Per complete cycle: record count, SHA-256 of its canonical form, and the records that differ
  from cycle 0 (only in cycle 0, only in cycle j). Reported: whether every cycle is identical, the first differing
  cycle, records outside complete cycles. With full_records=True the complete JSON records are compared (step
  shifted), as r36's `cycle_compare_v1` compares lines.
* **c_image(log, T, region=None, kind="C")**: decision: the C-image test belongs in this layer, as a map on records
  like the mirror. For each update n in [lo, hi - T]: the record set at n + T against the image of the set at n,
  C: channel g -> z.g (z = 14; the 48-entry table of the decoder config, checked against universe24 by a test),
  kind and quotient kept; K: channel z.g, k -> -k mod 3, q -> -q. region: an optional declared box of sites
  (r36's ring box). Reported: image steps, plain-repeat steps (set at n + T equal to the set at n, non-empty),
  steps with clicks, and unmatched records.
* **split(log, t_split)**: records with t <= t_split, and records with t > t_split shifted by -t_split (r36's
  `phase_split_v1` for t_split = P / 2 on one cycle).
* **record_diff(a, b)**: records only in A, only in B, and their sum.

## Validation (pre-registered expected results; logs read before: see "seen")
Positive:
* P1 bounce `runs/matter_light_v1/r27b/bb27v6_bounce_L640.events.jsonl` and `_L1280` (seen by click_mirror_v1):
  mirror tau = 240: 49,830 records, 0 unpaired, steps_mirrored 480/480 on [1, 480]; best_tau 240, unique.
* P2 r36 C1 `c1/c1_seed_L64.jsonl`, `_L128` (seen): period P = 48: 6 identical cycles of 316 records, also with
  full_records; mirror tau = 24 inside each cycle (split by period): 0 unpaired, 48/48 steps mirrored; best_tau of
  the whole log 144, unique, 0 unpaired.
* P3 r36 C2 `c2/c2_seed_L256.jsonl`, `_L512` (seen): P = 164: 4 identical cycles of 1372, also full_records;
  inside each cycle tau = 82: 0 unpaired, 164/164; best_tau 328, unique, 0 unpaired.
* P4 r36 C3a `c3/c3_seed_L256.jsonl`, `_L512` (BLIND; truth r36/REPORT_WAVE2.md): P = 164: 4 identical cycles of
  2612 records, also full_records; inside each cycle tau = 82: 164/164 steps mirrored, 0 unpaired; c_image on the
  ring box ((99, 105), (99, 138), (58, 62)) with T = 82 on updates 1..82 of each cycle: 82/82 image steps, 0 plain
  repeats; best_tau of the whole log 328, unique.
* P5 reference behaviour: on every C1, C2 and C3a cycle file r36 wrote (`*_cycle<k>.jsonl`), this layer's
  steps_mirrored equals r36's `mirror_check_v1` (recomputed with r36's own function on the same file), and its
  c_image steps on C3a equal r36's `spin_image_v1`; the cycle files written by period(full_records=True) are
  byte-identical to r36's cycle files.
Negative:
* N1 unsymmetrized bounce: the symmetrized and unsymmetrized L = 320 forward logs (runs/matter_light_v1/r17/
  click_mirror/, seen) differ in 17,407 records; the unsymmetrized bounce (L = 640, 480 updates, seen) is not a
  mirror about tau = 240 (78,572 unpaired) and its best tau leaves records unpaired.
* N2 C1's asymmetric seed `c1/c1_ctrl_asym_L64.jsonl` (seen): P = 48 not identical (first differing cycle 1);
  P = 96 identical (3 cycles).
* N3 c_image on r36 C2 (no ring) with T = 82 and the C3a ring box: no image steps with clicks (the box is silent).
Synthetic (tests): mirror and best_tau on a random mirrored log, one flipped quotient -> 2 unpaired, a half-integer
tau, periodic cycles and one moved record, c_image of a synthetic C-ring and K-ring and of a plain repeat, split,
record_diff, the z table against universe24.

Failures are recorded; the layer is frozen before P1-P5 and N1-N3 are run with it.
