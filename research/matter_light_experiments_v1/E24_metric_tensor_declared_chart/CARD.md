# E24 — A PRESCRIBED metric tensor read back from clicks in a DECLARED chart: staircase fibre radars read their node counts exactly (aniso, Manhattan control); two prescribed rings tick 24 and 16

## On the event board
- coupling +++, vacuum (0,0,2); r71's builders (registry wave 16; = his init files); nothing acts after t = 0. A
  station: a 16-node ring clock and 26 radar arms of fibre light (13 lattice lines n, both ways), staircases with an
  A-pulse (1,0,−1) probe (two elementary quanta), a 3-node port (nodes 4–6) and a bare far end as mirror (dwell 4)
- aniso (L = 966, T = 1526): "arm n is assigned coordinate B n by the designer" (B = 400) and gets the node count D(n) =
  round(400 √(nᵀgn)), g = [[1, 3/20, 1/20], [3/20, 6/5, −1/10], [1/20, −1/10, 9/10]]; manhattan (L = 310, T = 640), the
  negative control: D(n) = Σ|n_i| A_i, A = (100, 110, 95), B = 100 (a Finsler length)
- time_v2 (L = 674, T = 568): S (24-node ring, N = 2/3; 13 arms, D = round(96 √(nᵀgn) / N)) above F (16-node ring, N =
  1; 13 arms), rings tapped into exit fibres past the other's 3-node receiver; g, N only in node counts

## In the clicks (gr_observer_v1 run_declared with r71's declarations; official click logs)
- "a clicks-only observer GIVEN A DECLARATION (port and mirror addresses, directions n, scale B, dwell 4, standard lap
  16)": t1, t3 at the MIDDLE port node, t2 at the mirror; distance = rate · (t3 − t1 − 4) / 2, rate = 16 / ring period
- aniso, manhattan: all 26 arms read their node counts D(n) exactly (time_v2: 13 + 13); dwell-corrected offsets 0
- time_v2: rings 24 (S), 16 (F): rates 2/3, 1 (lap 16); the receivers' 3-node records (r71's declaration, channel filter
  only) repeat exactly with periods 24 at F and 16 at S (6 clicks per period): f_r/f_e = 2/3 at F, 3/2 at S

## Claim
- [SIMULATION] "the only simulated content: a staircase fibre radar reads its node count exactly, with dwell 4"; "the
  quadratic form, the covariance and N = 2/3 follow from the written integers [THEOREM given that; verified]"
- [THEOREM (d), r71 §9; R10ZG-7 and R10ZG-10; reproduced on aniso by GR-F9; not computed by this package's checks] in
  the clicks' own addresses the staircase boards give Manhattan lengths (d = |Δx|₁ on every arm of all three boards), so
  the tensor exists only in the declared chart; only the three lat_* boards carry it in lattice coordinates, and there
  the metric is hand-placed meander length (still prescribed) (reported, not run here; R10ZG-7)
- [by construction, R10ZG-8] time part: "N = 2/3 is the prescribed ring ratio 16/24; received periods are the emitters'
  periods carried unchanged by static fibres; no redshift was measured"; 2/3, 3/2: period ratios of prescribed rings
- reported, not computed by this package's checks: aniso's least-squares tensor matches g to rounding, 7 check residuals
  −0.0041 to 0.0090 in bounds 0.017–0.028 (R10ZG-3); manhattan: "r71's tensor analysis reports 'not a metric tensor'"
  (parallelogram defects 4.4, 3.8, 4.18 vs rounding about 0.02 (check residuals 3.8–8.58 against bounds 0.08–0.14,
  R10ZG-6); the test's power against small non-quadratic defects is untested); time_v2 per node with the (kind 1, q 1)
  filter: click gaps exactly 24 and 16, unfiltered 4 + 20 and 4 + 12, two clicks per A-pulse (GR-F9); covariance
  (R10ZG-4); 2O image (R10ZG-5); flat, iso, lat_* (R10ZG-7); spinor 720° (R10ZG-9, r71's logs only)
- not claimed: a metric produced by matter; curvature; gravity; a tensor in the lattice's own coordinates
- referee: r10zg R10ZG-1..11 CONFIRMED (3 given the reads and the design; 5 every record; 6 coarse; 8 by construction; 9
  on r71's logs, not re-run; 11 with a remark), R10ZG-12 PARTLY (fixes 1–9 applied); fresh machine 2 GR-F9: 4 boards
  audited, (1)–(5) and the addendum CONFIRMED (fixes 1–3 applied)

Reproduce: python -m research.matter_light_experiments_v1.verify E24_metric_tensor_declared_chart
