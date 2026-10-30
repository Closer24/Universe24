# Findings from probes B2 and F

## B2 (probe_b2.txt)
- (a) g = f: key D_L/70 -> max |q| 1; key D_L/700 -> max |q| 10, 5,371 rounds with |q_M| >= 2, misses 625 of 5,815
  click rounds; key D_L/7000 -> max |q| 95, misses 4,137 of 5,992. The law line's "coming apart by one winding"
  is wrong where |q| >= 2 (and the misses grow as the key shrinks against the wobble).
- (b) a giver and two takers (D-count): the three counts' sum in [-1, 1] (bound 1 holds); EVERY click round misses
  (89 of 89); counts at the end (-6, 3, 3).
- (c) the backward run's click is minus the forward's at 5,999 of 5,999 rounds: "read alike in both runs" is true of
  the count n, not of the click (a take read as a give).

## F (probe_f.txt): the mathematician's question (CLICK25 section 7 OPEN) answered
No whole-number quadratic form in (a, b, r) nor in (a, b, r, a+, r+) is kept by the act's gear on any of four lays
(W = 800, 10^6, 7; swings 300 to 10^6): true invariants 0 after removing the constant and the forms that vanish
identically by the one-round identity. The control (a+ = 3a - b, exact) finds its invariant a^2 - 3ab + b^2.
So "a whole-number form of the act's energy with the teeth" that closes the wind's books exactly does not exist
among quadratic forms; exact books need an exactly antisymmetric increment (the area's tau, or X), not a state form.
