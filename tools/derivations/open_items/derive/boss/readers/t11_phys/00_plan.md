# t11_phys: hostile physicist's reading of CLICK25.md sections 0, 2, 3, 4 (term 11's count)

Folder: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t11_phys/
Draft: scratchpad/click25/CLICK25.md (2026-10-30 15:37), probes probe_wind.py, probe_count.py.

## Questions to answer (the task)
1. Is the wind given or taken a quantum of energy per mode (E = n hbar omega, key = hbar) for light and for a bound hand?
2. Does a line train (standing wave) click correctly against nature (absorption/emission by a linearly polarized mode)?
3. Does the held quantum's exemption match a vacuum?
4. Are energy and momentum conserved at a click in the clicks' spacetime?
5. What do the books' 2 misses in 6,000 mean physically?
6. Does the count respect causality and the run back?
7. What do three trains sharing a click do?
Plus: rerun the probes; build my own whole-number checks on the real act (carry only).

## First impressions from reading (to test)
- D = a^2 - a+ b summed over the hand. For a harmonic gear a_t = A cos(omega t + phi): a_t^2 - a_{t+1} a_{t-1}
  = A^2 sin^2(omega) exactly (a trig identity), INDEPENDENT of phase. So D = A^2 sin^2 omega per gear, constant on a
  free hand. Good: D is an energy-like invariant for a free oscillator. But E = (1/2) m omega^2 A^2; D = A^2 sin^2 omega
  ~ A^2 omega^2 for small omega. So D ~ 2 E / (m) ... D is proportional to E at FIXED omega. Across modes of different
  omega, D/E = 2 sin^2(omega)/(m omega^2)... D is E times a frequency-dependent factor. A key in counts^2 is NOT
  hbar: E = n key would make every mode's quantum the same ENERGY, not E = n hbar omega. CHECK THIS CAREFULLY.
  Actually: D per gear = A^2 sin^2 omega. E_phys = (1/2) m omega^2 A^2 (with m the gear's mass, which in the engine is
  W/W^2?...). So D = E * 2 sin^2(omega)/(m omega^2). For the engine, the energy per the leapfrog: W^2 D = ... The draft
  says D is "the leapfrog's energy over W^2". With key constant across trains: a quantum of D is NOT a quantum of
  E proportional to omega. E = n key corresponds to hbar omega = key for all omega => hbar ~ 1/omega. NOT Planck.
  Unless the key depends on frequency per train... the draft says "one key for the board".
- "The decoder's h-bar is the key over the beat it reads": key / omega = hbar? That makes hbar frequency-dependent.
  Planck's constant is universal; this is a BLOCKING physical mismatch unless the wind is normalised by omega.
- The taker's count goes 0..7 and back over 6000 rounds — that's a beat (Rabi-like exchange between two coupled
  oscillators), classical energy sloshing. The "clicks" are just integer thresholds crossed by a smoothly varying
  classical energy. In nature, a photon absorption is one quantum, not a slow sloshing through 7 levels. But the owner's
  frame says this is fine ("clocks connecting"). Hmm, must check what the clicks show: the count climbing 0->7 over
  ~1000 rounds means 7 clicks spaced out in time; the reverse gives -7. Each click "fires" at a threshold crossing.
- Causality: n(t) is defined from D(t) which uses a_{t+1} (the "next"). The runner writes the click comparing n(t)
  with n(t-1). D(t) needs a_{t+1}: computed in the round. Fine for the forward run. For the run back: mirror state
  (a_t, a_{t+1}) ticks to a_{t-1}; D read as a_t^2 - a_{t-1} a_{t+1} = D(t). Same. OK, even under mirror. But the
  click is n(t) - n(t-1): in the run back the sign flips (give <-> take). Fine.
- Three trains: "(n-1) div 2" bound — must test.
- 2 misses in 6000: the sum D_L + D_M drifts by Rule3's remainders (round-off of the integer leapfrog). The misses are
  where the drift crosses a key boundary. Physically: energy non-conservation of the integer scheme shows up as a
  spurious click (a quantum created or destroyed from nothing). In nature that's forbidden. Also note the drift
  relative to the key is 1854 millionths... the key is 1/7 of D_L. So the drift is ~ 1.3e-4 of the energy. The
  misses are where the pair's clicks don't sum to 0 in a round: a click in one hand with no matching click in the
  other in the SAME round. Could be a one-round delay (the other clicks the next round) — then it's not a loss, just
  a timing offset. Need to check whether misses are balanced over time (n_L + n_M in {-1, 0} says they are bounded).
- The key value is chosen as D_L(lay)/7 made odd: a 1/7 of the giver's energy. Arbitrary. CHOSEN.
- Line train: the giver on a line (im = 0): D nonzero (A^2 sin^2 omega), the area 0. Energy passes, charge doesn't.
  Physically a linearly polarized mode has energy n hbar omega, zero angular momentum on average. The exchange with
  the taker at rest: the taker is a 2-part hand (re, im) at rest; the giver (re only) drives the taker's re only
  through the vertex (if the vertex couples re to re and im to im). Then the taker becomes a line hand too. OK.
- "Absorption and emission by a linearly polarized mode": in nature, the photon number of a linearly polarized mode
  changes by 1 at absorption; angular momentum is +-hbar per photon of circular polarization, 0 average for linear.
  So wind clicks with no area clicks is consistent-ish. But the atom's angular momentum changes by +-1 even for
  linear light (superposition). Classical picture can't show it. Not a BLOCKING item per se.
- Vacuum: the held quantum D_lay is the lay's wind. The exemption: D_lay is "never counted". For a vacuum, the zero
  point energy hbar omega / 2 is not extractable. Here D_lay is the hand's INITIAL energy — for the giver, that's
  5e9 counts^2 = 7 keys of energy! The giver's lay wind is 7 keys, all "held", "never counted"? Then the taker's lay
  wind is 0 (at rest). The giver's count runs 0..-7 as it gives. So the "held quantum" is actually ALL the energy
  the hand was laid with, not one quantum. Decision 40 (g) says "one held quantum per Node-clock". The draft's D_lay
  is per train per Node-clock and equals whatever the lay gave it — 7 keys for the giver. That's not "one quantum".
  This is a physical mismatch: a hand laid with 7 quanta should read 7, not 0. The count is RELATIVE to the lay, so
  an observer cannot tell a hand with 7 quanta from one with 0 — until it gives. Hmm, but the owner's words: "the
  click counts where the two runs part (D given or taken), never D held". So the count being relative is the owner's
  word. But the "one held quantum" of 40 (g) vs D_lay = 7 keys: the draft conflates. CHECK decision 40 (g) text.
- Momentum: on one Node-clock, no Mesh, no momentum to speak of. The momentum conservation "in the clicks' spacetime"
  is untested by these probes. The draft claims nothing about momentum. Item: momentum untested.
