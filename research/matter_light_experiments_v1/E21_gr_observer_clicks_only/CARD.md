# E21 — A clicks-only observer reads E09 and E10: exact clock periods, redshift, Shapiro delays, routes, the lapse N, the radial stretch H_r and α, and a radar echo, from declared stations only

## On the event board
- no new board: E09's prepared light-flux boards (20 runs) and E10's PRESCRIBED relay lattice (main and packet-free
  control), +++, composition files byte for byte, published run hashes (E10's lamp not read); E10: declared node counts
- every ring, flux and probe is fibre light (r04 guide packets, speed 1) carried by A = (1,0,−1) pulses (two elementary
  (1,−1) quanta at adjacent phases, R10Y-17); on E09 the probe is delayed +4 per A-pulse met
- the observer is the released layer gr_observer_v1 = r64's observer_gr.py 1.2 byte for byte: a pure function of (step,
  address, kind, quotient) at the stations declared in detectors.json (r64's declarations, fixed before it read any log);
  it never imports universe24 and writes nothing; its numbers survive deleting every off-site record (R10ZB-1)
- proper time = a declared W0 ring of A-pulses: a station counts laps of its own declared ring; an unslowed ring's
  period equals its lap, so the update label is the far clock's proper time

## In the clicks (layer gr_observer_v1 on each official log; decoder 1.0 pinned)
- E09 proper time: the far ring clock has exact period 16, the clock whose ring carries a counter-circulating pulse 24
- E09 redshift from exact periods: x = 100 receives period 16 and 24 from update 104, so f_received/f_emitted = 1 and
  2/3 (received period = the emitter's own); the click RATE there rises ×4/3 (2/16 → 4/24): never read rates (R10ZB-7)
- E09 Shapiro: first arrival at x = 100 at 95 + 4k for k = 0..6 A-pulses met; river: 90 with and without the flux; route:
  arm A 116 + 4k, arm B 129, so B clicks first from k = 4; the controls stay silent
- E10 clocks: E tangential 16 / 24, radial 16 / 36; T 16 / 24 and 16 / 24; F 16 everywhere; O receives every pattern
  from update 24 with the emitter's own period; the packet-free control has no click at all
- E10 near the centre: E has N = 2/3, H_r = 3/2, v = 4/9, α = 2 exactly (N_r = N_t²); T has N = 2/3, H_r = 1, α = 1
- E10 light: radial probe 84 / 72 / 64 (E / T / F: +20, +8); rays E 186, 186, 146, 130, T 162, 162, 146, 130, F 130;
  route: E's B first (108 vs 116), T and F: A first
- E10 radar on its official log: t1/t2/t3 = 2/89/180 (E), 2/77/156 (T), 2/69/140 (F); the return leg exceeds the
  outgoing leg by exactly 4 (the bare end's delay, one device constant; raw offset −2): not an independent sync test

## Claim
- in plain words: an observer who owns only declared stations (ring clocks, light ports, a mirror) and reads nothing but
  their clicks recovers E09's and E10's refereed numbers: proper times, redshift, Shapiro delays, routes, and on E10 the
  lapse N, the radial stretch H_r and α = 2 (E) or 1 (T)
- [SIMULATION, exact: equality of click records, exact rationals] the numbers above, from the declared stations only
- not claimed: spatial curvature (E10's clicks contain no areal-radius measurement, so the observer cannot read the
  spatial curvature from them; N·H_r = 1 alone does not certify Schwarzschild); E10's step layout is curved on its shell
  boundaries (not vacuum); gravity sourced by matter; α from E09 alone (its α = 1 is r23's matched pair); the E09
  probe–flux relative phase (r10zb fix 8, not stated); the shells and fan boards; E09's radar; the 44 ring-loop offsets
- referee: r10zb R10ZB-1, 3, 4, 5, 7, 16, 17 CONFIRMED (R10ZB-6 PARTLY, fix-6 frame; R10ZB-19's profile wording applied);
  fresh machine 1 GRF2 and GRF5 (E21 reproduced); the boards: E09 r10f R10F-8, E10 r10f R10F-7

Reproduce: python -m research.matter_light_experiments_v1.verify E21_gr_observer_clicks_only
