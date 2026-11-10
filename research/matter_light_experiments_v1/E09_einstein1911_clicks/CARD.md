# E09 — Einstein-1911 signatures in a prepared light-flux medium: redshift, Shapiro delay, least-click-time route, river (α = 1, γ = 0)

## On the event board
- board: sides 160 (Shapiro, river, bending) and 200 (redshift), coupling +++ (reference), quiet vacuum (0,0,2)
- prepared at t = 0 (compositions/*.json, guide_net@1 only: r04 fibre packets, ring16 emitter, degree-3 junction):
  - Shapiro/river: one x fibre; a "flux" of k = 0..6 unit packets (1,0,−1), spacing 8, moving −x; one probe moving
    +x (counter-moving) or −x behind the flux (co-moving)
  - bending: a Y junction; arm A (106 nodes) straight through a flux of k = 0..5 packets moving toward the junction,
    arm B (118 nodes) flux-free; one probe enters the junction and is copied into both arms
  - redshift: a ring16 emitter (tap, exit fibre 160 nodes) with or without one counter-circulating packet on the ring
- controls: no flux (k = 0; far clock), flux only (no probe), emitter without packets; 150–220 updates
- after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- stations (detectors.json): single fibre nodes; each window is one in which only the probe can click
- Shapiro: first click at x = 100 = 95, 99, 103, 107, 111, 115, 119 for k = 0..6 (exactly +4 per packet met);
  flux only: 0 clicks
- river: co-moving probe at x = 60: 90 with the flux and 90 without (delay 0); counter-moving: +24 for k = 6
- bending: arm A 116, 120, 124, 128, 132, 136 (k = 0..5), arm B 129: the first arrival switches from the route
  through the flux (k ≤ 3) to the route around it (k ≥ 4); flux only: both stations silent
- redshift: far clock received at 120, 136, 152, 168 (period 16); clock in the flux at 128, 152, 176, 200
  (exact period 24, not 16-periodic); decoder ring-source periods [16] and [24]; empty emitter silent

## Claim
- [SIMULATION] (declared 2026-11-09 02:43 UTC; bending v2 02:46 UTC): in a light-flux medium every head-on
  crossing delays a packet by exactly 4, so light is slower against the flux (Shapiro: Δt = 4 × packets met),
  not slowed with it (river), first arrivals avoid dense flux (least click-time route), and the received pattern
  of a light-ring clock carrying the flux repeats every 24 instead of 16 (N = 2/3; its pulse rate rises, 2 per 24
  against 1 per 16, so only the exact period lengthens).
- These are Einstein-1911 signatures only: α = d ln v_null / d ln N = 1 (γ = 0), from r23's matched pair (wave 1,
  α = 1.000, R10F-16; r14 G3; r22). Half of Einstein's light bending is inferred from α = 1, not measured. α = 2 is
  impossible for light instruments on the same links (r22 no-go): links and light clocks are slowed by the same
  rule, so H = 1.
- referee: r10f R10F-8 CONFIRMED
- limits: prepared fibres, junction and emitter; the flux sits on the probe's or clock's own fibre (junctions
  copy); the clock in the flux emits two pulses per period (the flux packet is emitted too), so only the exact
  period, not the click rate, is the redshift; no 1/r profile; bending design v2 (v1's flux-only control failed:
  junction copies reached arm B inside its window; v2 declared 02:46 UTC)

Reproduce: python -m research.matter_light_experiments_v1.verify E09_einstein1911_clicks
