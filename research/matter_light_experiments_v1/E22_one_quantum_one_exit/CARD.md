# E22 — One quantum token, one exit per cycle: builder D's CC8 router with two prepared escort packets; exit frequency a counting-fraction sawtooth, not cos², not Born

## On the event board
- coupling +++ (reference), vacuum (0,0,2), L = 256 (the representative pair also on 2L = 512, X at the same site);
  builder D's CC8 as ONE registered guide_net@1 placement (registry wave 11): E20's hardware with a 60-node input line
  and both escort lines trapped below their doors (65 nodes; 110-node arms above), so every encounter falls on an
  8-update lattice: the quantum is back at X every 128 updates, each escort at its door every 136
- three separately prepared unit (1,−1) fibre packets (profile C; fibre light, r04 guide packets, speed 1), all lit at
  t = 0: the quantum, a token, on the input line at its hidden phase τ (14 lattice phases); escort B at a fixed
  phase and escort C at the device phase D′ (13 realisable values) are prepared hardware; nothing acts after t = 0
- replayed here: all 182 members (14 τ × 13 D′), each to t* + 200 (t* = its first exit click), and the representative
  pair D′ = 8, τ = 6 and 70 to update 2,100 on L and 2L; the composed boards equal builder D's; |a|, |b| ≤ 1 throughout
- predicted exit: the earlier exact coincidence of the quantum at X with an escort at its door (builder D's arithmetic)

## In the clicks (decoder 1.0 and log_symmetry_v1, official click logs; declared exits B and C)
- every run: the input line and both escort segments click from update 1 (all three prepared packets are lit), every
  click is on the guides, and exactly one exit clicks in [1, t* + 200], first at the predicted coincidence + 2
- the law, over all 182: exit B first in N_B = 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13 of the 14 runs for D′ = 1, 2,
  3, 6–12, 14–16, exit C in the others: P(exit B) = N_B / 14, a counting fraction over the prepared hidden phase
- representative D′ = 8: τ = 6 → exit C first at 776, exit B silent in [1, 976]; τ = 70 → exit B first at 712, exit C
  silent in [1, 912]; L = 2L (the same click records)
- exclusive per cycle, not forever: in the τ = 6 run exit B clicks 594 times after t* + 200, up to update 2,100 (the
  transmitted escort's return); in the τ = 70 run exit C stays silent to 2,100
- No C0 click occurs in any of the 186 runs (0 repaid, 0 unrepaid; unit-quantum regime, max |a|, |b| = 1); the exit
  is fixed by the prepared hidden phase (R10G-280, R10G-284). C0 is a meeting product (R10G-286).

## Claim
- in plain words: the quantum is a token that reaches one exit only, until the transmitted escort returns; the escorts
  are prepared hardware. The run's exit is unpredictable for the detector-only observer; the deciding datum (the
  quantum's phase) is in the full official log from the input line's clicks. Over a uniform hidden phase, exit B's
  frequency is a counting-fraction sawtooth (rising 1/14 per device phase step, up to ties from sampling 14 of 17
  phases: D′ = 12 and 14 both give 11/14), not cos², not Born
- [SIMULATION, exact per run; EXHAUSTIVE over the 182] the exit is fixed by the initial data; its law is that sawtooth
- reported by builder D and QM-F4 (f), not replayed here: the other exit lights after t* + 200 (to 2,100) in 50 of 182
- not claimed: cos² or Born (that needs a prepared amplitude threshold); a selection law (C2 is an arithmetic class);
  that the quantum or the device makes the outcome; other lattices or hidden-datum measures; TT-1 / TT-2 (not in E22)
- referee: r10g (REVIEW_R10G_W9 item 1): R10G-276..281, 283, 284 CONFIRMED; R10G-282, 286 PARTLY (wording, applied);
  R10G-285 NOT CHECKED (QM-1, not in E22); nothing refuted; fresh machine 2 QM-F4 ALL PASS

Reproduce: python -m research.matter_light_experiments_v1.verify E22_one_quantum_one_exit
