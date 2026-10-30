# rd_phys notes 03: probe results (probes 1-5)

## Probe 1 (the push floor), one gear, L = 100, W = 10^4
- A constant push p < 50 (= L/2) moves NOTHING in 2000 rounds (as built: a = p x 200); p in [50, 149] acts as 100:
  F_eff = L round_odd(p/L), a staircase; at p = 50 the force is doubled (2000 permille). Bias, same sign every round.
- Hairspring g = 1: a0 < 50 frozen for ever (0 crossings; as built 10 beats in 6000 rounds); a0 = 50, 51: 15 crossings
  against 10 (the beat 1.5x too fast); a0 = 75: 12; a0 >= 100: 10 = 10.
- The kick K = T_k s q_d = 1 a round (as BUILT): as built one notch after W = 10^4 rounds; root dial 0 for ever.
  The smallest kick that passes is L/2, and it passes as L.
- Calibre (den = 6 k^2, k = 5e7, Gamma 1000: L_rest = 3e11, grip 1.5e22): the floor is 1e-11 of one count's pull
  (the deriver's number holds for the PULL); the kick at 1 and a spring below |a| = L/(2g) are lost.

## Probe 2 (windows), standing L = 100, g = 37, 300,000 rounds, ten windows
- No secular drift in any window at any amplitude (the windows agree to the permille).
- a0 = 1 (g a0/L = 0.37): frozen for ever. As built at a0 = 1: 55 crossings per 30,000 (T 545 against nature's 103):
  both acts are wrong at one count; the root freezes, the as-built staircases its velocity.
- a0 = 2: a limit cycle, 144 crossings per 30,000 (T 208 against 103), 32 E breathes 2368..43984 (mean 7.05 E0).
- a0 = 3: T 213, E mean 3.8 E0; a0 = 5: T 120, 2.1 E0; a0 = 10: T 90, 1.3 E0; a0 = 30: T 100, 1.025 E0 (E breathes 7%);
  a0 = 100: T 103.4, E 1.026 (the leapfrog's offset, the same breathing as built); a0 >= 1000: E 999-1001, A 1000-1004.
- So: no leak, no drift; a staircase anharmonicity and a dead zone for g A below about 10 L; clean above 30 L.

## Probe 3 (two clocks, half-open), rising 100 -> 200 and falling 200 -> 100
- Free gears: P = 2 D v + s conserved to the BIT (1000 permille at every mark, rising and falling), v = 10^6 x 100/L
  exactly (800000 at L 125, 666667 at 150, 571429 at 175): L v kept exactly, better than the deriver's "8 permille"
  (that was the dial's granularity read as v^2 W at a step).
- A sub-notch momentum (v0 = 0, s0 = 150 of a notch's 400): a = 0 for 30,000 rounds, P kept; nature moves 7825
  counts. The tooth holds a sub-notch momentum for ever with no notch: below half a notch a round nothing moves
  (as built too: r stays). A floor on the velocity, the act's, not the root dial's.
- Hairspring g = 100, a0 = 1e7: A/A0 999-1000, T^2/W 998-1003 rising AND falling; v_max T 63.8e6, 63.1e6, 62.7e6
  (1.7% fall over L x 1.75: the measured v_max is the quotient's integer at the turning round); L v_max 1.009e8,
  1.0076e8, 1.0064e8; g A^2 within 0.5%. Tie-even identical to the digit (711, 854, 997).
- a0 = 5 (v_max 0.5): A kept (6), T^2/W 1000, 1230, 1823 rising, 1000, 563, 520 falling: the beat does not follow L.
- g = 37, a0 = 3 (floor bites): A 3 kept, T 2434/10 = 243 against nature's 2 pi sqrt(15625/37) = 129 at L 125.
- g = 37, a0 = 300: A/A0 1000, 1013, 1052 rising: the amplitude GROWS 5% over L x 1.75 at g a0/L = 1.1 x 100.

## Probe 4 (ring of 32, grip 36)
- Standing: T 544.7 at L 102 (nature 544 + 1.6 permille dispersion), 1088.8 at 204, 272.3 at 51: c^2 = grip/L^2.
- Peak amplitude 80 and 8 at L 102: the wave degrades (6 and 4 crossings in 6528 rounds against 12): a curvature of
  one count pushes 36 < 51: dropped. Frozen band: at L 150, grip 36, amp 8: 0 of 32 sites move in 3000 rounds;
  at grip = L^2/6 = 3750: 32 of 32 move.
- Rising clock (102 -> 204): the proper energy 996-1005 permille in ten windows (nature constant); the as-built
  amplitude grows to 2901 permille.
- The 00 row's cone: periods 783 (L 6) against 1568 (L 12): c^2 ratio 4.01 = W/W_rest. Unchanged by the root dial.

## Probe 5 (seed)
- The example's den, the hand's den, cheap runs, K1's, the 3-cube's: none is 6 k^2 (none divisible by 3 but... none).
- Lifts of den = 6 k^2 exist iff k has a prime 1 mod 4 (k = 5, 10, 13, 15, 17, 20, 25, 26, 29, 30 of 1..30).
- L_rest = 6 k Gamma, W_rest = L_rest^2 = 6 den Gamma^2, grip = den Gamma^2, c^2 = 1/6: the floor 3/L_rest of a count's pull.
