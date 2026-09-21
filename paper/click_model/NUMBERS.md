# Every number of the paper, and where it comes from

Four kinds, named on every row: **register** (a run recorded in
[docs/EXPERIMENTS.md](../../docs/EXPERIMENTS.md), series L, with its source
fingerprint), **design** (the check outputs of
[docs/designs/amplitude-v1/](../../docs/designs/amplitude-v1/)), and
**computation** (this directory's `checks/`, from the design's formulas with
the repository's tables, not an engine run), and **map** (the mathematician's
`two_slits_map.py` of `docs/designs/fraction_free/` on the merged tree, records
156 and 160; record 160's width sweep is a scratch map not in the repository,
labelled so). For the pace and the Lorentz section the design kind also names
`docs/designs/light_speed/` (FORM.md and `light_speed_map.out`) and the
derivation `docs/DERIVATIONS_BEAM.md` with its host scripts (sections 4, 12,
12b, 13), all on main at 88d843ef; the register kind there is series G2.
Literature values are their own kind, cited by the paper. The paper cites a run only from
the register. The runs were reproduced for the figures on the paper's tree, the merge
`4ccf65c7` of main's `d2064195` (source fingerprint `731d0f56c9f9`; main's
own is `48a9d1c91661`, the two trees differing by one docstring), every
integer equal to the register's at `ff5c382d672f` (the gate worlds were
re-run in the register after the gate's fix with the same integers;
`figures/summary.json` covers the 45 keyed worlds; `slits_one` is read by the generator).

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
| The maximum of S over every setting quadruple at N = 64 and 256; quadruples within 3 sigma of Poh at N = 256 | 11/4; 91/32 = 2.84375; 181,152 | computation | `checks/s_of_n.txt` |
| Rung ties at the CHSH labels for every 8 divides N up to 4096, and over every pair at N = 1024 | 0; 0 | computation | `checks/s_of_n.txt`; record 105 for 64, 256, 1024 and 4096 at a = 0, 1024 |
| The bound of Theorem 4 with rho = 256 - sqrt 2 / 2: 4 delta and 16 delta | 0.01108 < 0.0111; 0.04432 < 0.0444 | computation | the proof |
| Every marginal 32/64 in all 4096 setting pairs at N = 64 | 32/64 | register (re-read from `bell_0_8`'s rows by the reviewer, record 105) and computation | L3; record 105; `checks/s_of_n.txt` |
| The choosers' 15 bins, E x 64 | 44, -60, 20, 60, -8, -48, -8, 60, -52, -64, 40, 20, -28, -36, 64 | register | L3, `bell_choosers`; `summary.json` `choosers` |
| The registered quadruple (0, 25) x (8, 29) | S = 156/64 | register | L3 |
| Which-path on Alice's arm | E x 64 = 44, -44, 0, 0; S = 88/64 | register | L3, `path_*` |
| No maintenance: Bob 116 Links farther | E x 64 = 44 (0 with the read) | register | L3, `bell_16_24_far`, `path_16_24_far`; `summary.json` `far` |
| GHZ: the allowed triples, 16 each, the products | XXX +1; XYY, YXY, YYX -1; YYY all eight, 8 each | register | L4, `ghz_*` |
| CNOT then the pair; CNOT twice; GHZ by one gate; the register's ceiling | S = 176/64; the identity; the same triples; three rotations fit, four refused | register (re-run after the gate's fix, record 109) | L5, `cnot_*`, `rotations_3`; `summary.json` `gate` |
| S(1024) | 2896/1024 = 181/64; E x 1024 = 724, -724, 724, 724 | register | L6, `bell_n1024_*` |
| S(4096) | 11584/4096 = 181/64; E x 4096 = 2900, -2900, 2892, 2892 | register | L6, `bell_n4096_*` |
| S(N) for every N with 8 \| N up to 4096; 252 of 512 above 2 sqrt 2; the powers of two from 512 exactly 181/64 | the table | computation | `checks/s_of_n.txt` |
| The per-E deviation over all setting pairs: 2.27/N at N = 64, 5.9/N at N = 512 | 0.0355, 0.0115 | computation | `checks/s_of_n.txt` |
| No rung tie at N = 8 .. 512 over every setting pair; at 64, 256, 1024 (all pairs) and 4096 (a = 0, 1024) | none | computation; the reviewer's re-read | `checks/s_of_n.txt`; record 105 |
| The tables' norm, -351 to +361 about 65536 for the powers of two through 65536; 65897 at N = 4096, p = 503; 65185 at N = 32768, p = 3995 | | computation | `checks/tables_norm.txt` |
| The rotation's norm factor at N = 64, s = 1 | 65705/65536 | computation | `checks/tables_norm.txt` |
| E at the CHSH labels before the cells' rounding, at every N | 46565/65773 and 46452/65773 | computation (the half-angle entries 237, 98 and 181, 181) | the draft after Theorem 4; record 105 |
| The two-slit expectation re-pinned once after a first run | 31/14/19 to 34/15/15 | register | L2, "dated history of the same day"; record 96 |
| Poh et al. 2015 | S = 2.82759 +- 0.00051 | literature | Phys. Rev. Lett. 115, 180408 |
| Hensen et al. 2015 | S = 2.42 +- 0.20 (2.38 +- 0.14 over both runs) | literature | Nature 526, 682; Sci. Rep. 6, 30289 |
| Paper 1's local candidates and the choosers' run | S = 2 exactly; the registry 2.83 | register (A2, A2 with the choosers) and paper 1 | the "before" |
| S(N, Q) at N = 64, 256, 1024 for Q = 256 .. 2^20; the bound 8/N + 16 arcsin(sqrt 2 / 2Q) | 2.75, 2.8125, 2.828125; the bound 0.125, 0.031, 0.0078 at Q = 2^20 (0.169, 0.076, 0.052 at Q = 256 with rho = Q - sqrt 2 / 2; limits.txt prints 0.075 at the nominal Q) | computation | `checks/limits.txt` section 1 |
| The choosers' bin (51, 8) against the step curve E(d, 0) | E = -28/64; E(43, 0) = -32/64; 18 of 19 registered E on the curve | register and computation | `summary.json` choosers; `checks/s_of_n.py` |
| The flight speed per direction at the flight scale Q_f = 64 | 0.8 percent above 1 / sqrt 3 on an axis, 0.5 on the plane diagonal, exact on (1, 1, 1) | computation | `checks/information_transfer.txt` section 1; BEAM_LAW section 3 |
| The two-slit record's offered total against its birth norm | 847181/745472 = 1.136 | register (the generator's reading) | `expectations.json` two_slits.total |
| Young under the fan's discreteness: Pearson(W, cosine) at K = 91, 361, 721 directions; pixels with both openings | 0.45, 0.84, 0.90; all 121 from K = 721 | computation | `checks/limits.txt` section 2b |
| Young under the flight's rounding alone at lambda = 8 intervals | Pearson 0.93 | computation | `checks/limits.txt` section 2 |
| The plane wave: omega / k = 1 / sqrt 3 for every rate n / d | withdrawn (referee round 3: k was defined as omega / c) | computation | `checks/limits.txt` section 3, kept as history |
| A record's interference wavelength under the pair form n / d | c N d / n Links along the flight | computation (the definition of the phase and the flight; no script) | the limits section |
| The abstract's bound | 8/N + 0.045 (16 delta = 0.04432 rounded up) | computation | the proof of Theorem 4 |
| The two paths of one record at a pixel of the two-slit world | up to 18 intervals apart | the mathematician's map | record 156 (main) |
| The two-slit run's clicks: pixels and cells | 14 pixels; 19 cells landed by the first 64 births, the same for every birth after | register and the mathematician's map | `summary.json`; record 156 |
| The lattice's primitive fan with equal weights at the width 64; with the angular weights | Pearson 0.65; 0.90 | the mathematician's map | record 160 (main) |
| The exact phase's effect on the two-slit Pearson | 0.02 (0.390 to 0.407) | the mathematician's map | record 156 |
| The prediction for the wheel W = 2^12, the screen's fan (one direction per pixel from each opening, equal multiplicity) and the exact phase | fringes at the Euclidean spacing, Pearson 0.963, visibility 0.96 over 4096 births | map, pinned before any run | record 156 |
| The angular fan alone (P = 48): the pin of `slits_huygens` | fringes in the weights (Pearson about 0.9, visibility 0.95 to 0.97), none in the clicks until the wheel | map (a scratch map), pinned before the run | record 160 |
| L7, the cone: the age at both counters; the path phase under the integer and the pair form | 29 and 29; 51 and 8; 23 and 23 | register | L7, `cone_links`, `cone_intervals`; record 144 |
| The sigma distances of S(N) from Poh: N = 64, 256, the powers of two from 512; the first admitted N; excluded at five sigma; the largest excluded | 152, 30, +1.0; 184; 136 of 512; 3016 | computation | `checks/s_of_n.txt` |
| The second party's strict count 33/64 in 3944 of 4096 setting pairs at N = 64 (the crossing that the nearest rung removes) | 3944; 33/64 | design | `docs/designs/amplitude-v1/DESIGN.md` section 4.3 |
| The two-slit clicks' Pearson with the weights | 0.655 | register (the generator's reading) | `summary.json` two_slits.pearson.histogram_weight |
| The tables' norm range at N = 64 | -88 to +237 | computation | `checks/tables_norm.txt` |
| The Mach-Zehnder offers at the equal arms | 1681/1682 and 1/1682 | design | L1; `expectations.json` |
| The two-slit fan: directions per opening; pixels reached; pixels reached by both openings | 91; 75; 27 | register (the generator's reading) | `expectations.json` two_slits (pixels_with_rows, two_path_pixels); record 156 |
| The register's ceiling: balanced (1, 1) splits, (3, 4, 5) splits, (20, 21, 29) splits and label rotations that fit below 2^62 | 62; 13; 6; 3 (the fourth refused) | design and register | the design's section 10; L5 |
| The choosers' periods and the births that cover their common period with N | 3 and 5; 960 = lcm(3, 5, 64) | register (the world file) | `bell_choosers.json`; `make_worlds.py` |
| The two-slit sets | 80 | register (the generator's reading) | `expectations.json` two_slits.sets |
| The primitive directions with components within 64; the integer equality S_1 Q_f = T_d; the cube diagonals among them; the near ones; the shortest near one | 1,780,418; 2072; 8; 2064; (22, 21, 21) with S_1 = 64 and sqrt 3 |d| = 64.016 | computation (the map's 1,780,418 and 2072 agree; FORM.md's "all cube diagonals" does not, reported) | `checks/light_speed.txt` section 1; `light_speed_map.out` A |
| The pace on a heading, the plane diagonal, the cube diagonal at Q_f = 64 | 64/110 = 0.5818 (0.77 percent above 1/sqrt 3); 0.49 percent above; exact | computation | `checks/light_speed.txt` section 2 |
| The anisotropy's scale; the bound on Q_f from an isotropy of c to 1e-18 | 1/(sqrt 3 Q_f); Q_f >= 5.8e17 | computation (the 1e-18 is literature, Nagel et al. 2015) | `checks/light_speed.txt` section 2 |
| The supremum of isotropic paces under one Link per interval in n = 1, 2, 3 | 1, 1/sqrt 2, 1/sqrt 3 | computation (Cauchy-Schwarz; the proof in the paper) | `checks/light_speed.txt` section 3 |
| The group of the octahedron: signed axis permutations; rotations; reflections | 48 = 3! x 2^3; 24; 24 | computation (main's `core.game_board.cube_symmetries` names the same 48) | `checks/light_speed.txt` section 4; record 226 |
| The digital line under the 48 over two periods: positions differing on (1, 1, 0) and (5, 2, 1); on (1, 0, 0) and (2, 1, 0); at whole periods | 48 of 192 and 48 of 768; 0; 0 | computation (the line rule of LAW.md 4.1) | `checks/light_speed.txt` section 4 |
| The Courant bound in n dimensions; the lattice Boltzmann sound speed | 1/sqrt n; c_s^2 = 1/3 | literature (Courant, Friedrichs and Lewy 1928; Qian, d'Humieres and Lallemand 1992) | `checks/light_speed.txt` section 5 |
| Lorentz: the thrown orbit at 0.21 c, contraction and slowing, against Lorentz's | 0.87 to 0.96 and 1.31 to 1.43; 0.977 and 1.024 | design (the derivation's host integration, section 12b.2) | DERIVATIONS_BEAM.md 12b.2; record 228 |
| Lorentz: the muon's 64th turn at every speed (series J4, defined and not run); under lorentz-v1 at 0.43 c and 0.86 c | 64; 71 and 126 | design (FORM.md section 4; the map's section E; HYPOTHESES entry 21) | `light_speed_map.out` E; record 186 |
| Lorentz: the fastest coasting star's z, the classical value, gamma's | 0.2636; 0.2674; 0.315 | register (series G2, `coasting_none`) and design (the derivation's 4.3) | DERIVATIONS_BEAM.md 4.3 |
| Lorentz: the dispersion under form B against relativity at p = m in the map's units (Newton's pace one Link per interval; c = 32/55 on a heading) | 0.632 c; 0.864 c | design (the map's table B) | `light_speed_map.out` B; FORM.md section 2 |
| Lorentz: the classical identity behind Heaviside's ellipsoids checked; the bond clock's factors in the limit | 1e-15; gamma^2 along and gamma across | design (the derivation's 12.1, 12.3) | record 213 |
| Lorentz, route C: the sphere mean of the crossing rule's count of a mover through an isotropic crowd at rest; the mean of the relative speed \|n - beta\| (the sweep, not the rule); the mover's rate over the rest rate never below | 1 exactly; 1 + beta^2/3; 1/2 | design (the derivation's 12c.1, 12c.2, 12c.7, `mover_counter.out`) | DERIVATIONS_BEAM.md 12c; records 230, 245 |
| Lorentz: nature's measurements | gamma = 29.3 (Bailey 1977); 0.34 c to 2e-9 (Botermann 2014); isotropy 1e-18 (Nagel 2015); Bertozzi 1964 | literature | the paper's bibliography |
| Lorentz: the classical ether's two-way anisotropy for a laboratory at the Earth's orbital speed | of order beta^2/2 = 1e-8 at 1e-4 c | computation (from (vi), the derivation's 12.3) | referee round 7, M1 |
