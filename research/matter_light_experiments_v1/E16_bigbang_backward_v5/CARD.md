# E16 — Big Bang candidate v5, built backwards: created light, two created ring clocks, one gate decision, a matched α_in = 1 instrument pair and a radar echo, from a 14-cell seed

## On the event board
- board: L = 640 and 2L = 1280, 240 updates (ring clock: L = 64, 100); coupling (−,+,+) (reference); vacuum (0,0,2)
- prepared at t = 0 (compositions/*.json, registered blocks only): a zero-counter network (matter lines A0 and AH, light
  line B0, the hz spinor ring and the h1 ring, a tap fibre, the A→B bridge and its mirror), prepared counter-carrying
  devices (two all-48 gates, analysers, twin trap cores, recorders) and the 14-cell seed* at O
- [THEOREM + check] seed* is the exact 16-step rewind of a composed T = 12 target holding only 4 movers at O (two light
  packets, two gliders); the prepared network alone gives 0 clicks in 240 updates (R10H-1); nothing acts after t = 0
- runs: main on L and 2L; controls probe removed, no bridge, no bridge with the emitter masked; variants mirror B→A,
  farther mirror, gate setting ψ = (2,0), a second reader on the h1 ring (M5h1); ring clock with one and two packets

## In the clicks (decoder 1.0, from the official click log only)
- M1: two created periodic sources born at 44, periods 36 (hz ring) and 22 (h1 ring); M2: exactly one gate fires
  (GU 8 clicks from 147, GL 0), with ψ = (2,0) neither fires
- M3: lamp tracks at exact +1 born at 56 + 18k; probe tracks at exact −7/11 against the stream (T43 born 150, T62);
  ring clock: period 22, one free packet 14 (N = 7/11); probe removed: no −7/11 track; emitter masked: 0 fibre clicks
- M4: A's radar echo over the bridge: node 0 out 109 / back 167, node 14 123 / 153, A's line 106 / 170, mirror 136,
  midpoint 138 (farther mirror: 144); B's region as without the bridge to 192; B→A swaps A, B; ψ = (2,0): bridge silent
- M5: z-ring reader at 54 + 18k; with the h1 reader: 54 + 18k to 234, h1 reader 54, 188, 224, no period 22, −7/11 kept
- decoder `created` (first clicks after t = 0, away from the seed): rings 44, lamp 56 + 18k, probe 150; the prepared
  dark traps light at 100; L and 2L: every declared readout identical, 22,124 records each (full records: R10H-2)
- the decoder also reports four single-site sources that no claim uses: (35,0,4) period 36 from 92; (30,0,4) 36 from
  123; (0,12,3) 16 from 174; (33,0,4) 20 from 192

## Claim
- [SIMULATION] From a 14-cell seed in a prepared network (zero-counter lines; gates, analysers, trap cores, recorders
  with counters at t = 0) decoder 1.0 reads created light, two created ring clocks (36, 22), one gate decision, a
  matched α_in = 1 instrument pair whose moving parts are all created, and a radar echo, identically on L and 2L.
- referee: r10h R10H-1, 3, 4, 7 CONFIRMED; R10H-2, 5, 6, 8 PARTLY, with these caveats:
  - α_in = 1 is a matched instrument pair (r23 Lemma 2, s − 4 = R): the clock (h1 ring slowed by its own counter packet,
    14 → 22) and the probe (tap fibre slowed by the lamp stream, 7/11) are separate devices equal by design, not N(x)
    and v(x) of one medium, and not created gravity
  - M4 is A's radar echo from a mirror beside B; B is not in the loop (no A–B synchronisation); the back windows were
    widened after the 03:33 registration ([150,175] → [150,190]); the farther-mirror 179 and 182 lie only inside them
  - the twin atoms are prepared dark traps lit at about t = 100: cores, analysers, recorders and gates carry counters
    at t = 0; on L = 320 (not shipped) the records diverge from update 159, where B0 wraps (readouts unchanged)
- limits: prepared network; backward construction; one moment, no turnaround (see E17, E15); v1.0: one run per site

Reproduce: python -m research.matter_light_experiments_v1.verify E16_bigbang_backward_v5
