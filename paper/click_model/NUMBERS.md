# Every number of the paper, and where it comes from

Three kinds, named on every row: **register** (a run recorded in
[docs/EXPERIMENTS.md](../../docs/EXPERIMENTS.md), series L, with its source
fingerprint), **design** (the check outputs of
[docs/designs/amplitude-v1/](../../docs/designs/amplitude-v1/)), and
**computation** (this directory's `checks/`, from the design's formulas with
the repository's tables, not an engine run). The paper cites a run only from
the register. The runs were reproduced for the figures on the merged tree of
`d2064195` (source fingerprint `731d0f56c9f9`, every integer equal to the
register's at `ff5c382d672f`; `figures/summary.json`).

| Number in the paper | Value | Kind | Where |
| --- | --- | --- | --- |
| Mach-Zehnder equal arms, half turn, quarter turn | D1/D2 64/0, 0/64, 32/32 | register | L1, `mz_equal`, `mz_half`, `mz_quarter` |
| (1, 1) split; (3, 4) split | 64/0; 63/1 | register | L1, `mz_balanced`, `mz_345` |
| Unequal arms at the phase per age 0, 8, 16 | 64/0, 32/32, 0/64 | register | L1, `mz_unequal_f0`, `_f8`, `_f16` |
| Elitzur-Vaidman (20, 21); (119, 120) | absorber 32, D1 17, D2 15; 32, 16, 16 | register | L1, `ev_29`, `ev_169` |
| The record's total over u: eight values | 65448/65536 to 65773/65536 | register | L1 (the departure); `summary.json` `totals` |
| Two slits at a low rate: clicks by kind | wall 34, screen 15, faces 15 of 64 | register | L2, `slits_low` |
| Two slits: Pearson of the weights with the incoherent sum, the cosine, the screen-alone histogram | 0.744, 0.368, 0.931 | register (the generator's reading, `expectations.json`) | L2 |
| The pair at N = 64: the CHSH cells | 27, 5, 5, 27 (E x 64 = 44, -44, 44, 44) | register | L3, `bell_0_8`, `bell_0_24`, `bell_16_8`, `bell_16_24` |
| S(64) | 176/64 = 2.75 | register | L3 |
| Every marginal 32/64 in all 4096 setting pairs at N = 64 | 32/64 | register (re-read from `bell_0_8`'s rows by the reviewer, record 105) and computation | L3; record 105; `checks/s_of_n.txt` |
| The choosers' 15 bins, E x 64 | 44, -60, 20, 60, -8, -48, -8, 60, -52, -64, 40, 20, -28, -36, 64 | register | L3, `bell_choosers`; `summary.json` `choosers` |
| The registered quadruple (0, 25) x (8, 29) | S = 156/64 | register | L3 |
| Which-path on Alice's arm | E x 64 = 44, -44, 0, 0; S = 88/64 | register | L3, `path_*` |
| No maintenance: Bob 116 Links farther | E x 64 = 44 (0 with the read) | register | L3, `bell_16_24_far`, `path_16_24_far` |
| GHZ: the allowed triples, 16 each, the products | XXX +1; XYY, YXY, YYX -1; YYY all eight, 8 each | register | L4, `ghz_*` |
| CNOT then the pair; CNOT twice; GHZ by one gate; the register's ceiling | S = 176/64; the identity; the same triples; three rotations fit, four refused | register | L5, `cnot_*`, `rotations_3` |
| S(1024) | 2896/1024 = 181/64; E x 1024 = 724, -724, 724, 724 | register | L6, `bell_n1024_*` |
| S(4096) | 11584/4096 = 181/64; E x 4096 = 2900, -2900, 2892, 2892 | register | L6, `bell_n4096_*` |
| S(N) for every N with 8 \| N up to 4096; 252 of 512 above 2 sqrt 2; the powers of two from 512 exactly 181/64 | the table | computation | `checks/s_of_n.txt` |
| The per-E deviation over all setting pairs: 2.27/N at N = 64, 5.9/N at N = 512 | 0.0355, 0.0115 | computation | `checks/s_of_n.txt` |
| No rung tie at N = 8 .. 512 over every setting pair; at 64, 256, 1024 (all pairs) and 4096 (a = 0, 1024) | none | computation; the reviewer's re-read | `checks/s_of_n.txt`; record 105 |
| The tables' norm, -351 to +361 about 65536 for the powers of two through 65536; 65897 at N = 4096, p = 503 | | computation | the draft's section 1 (recomputed 2026-09-20) |
| The rotation's norm factor at N = 64, s = 1 | 65705/65536 | computation | the draft's Theorem 2 |
| Poh et al. 2015 | S = 2.82759 +- 0.00051 | literature | Phys. Rev. Lett. 115, 180408 |
| Hensen et al. 2015 | S = 2.42 +- 0.20 (2.38 +- 0.14 over both runs) | literature | Nature 526, 682; Sci. Rep. 6, 30289 |
| Paper 1's local candidates and the choosers' run | S = 2 exactly; the registry 2.83 | register (A2, A2 with the choosers) and paper 1 | the "before" |
