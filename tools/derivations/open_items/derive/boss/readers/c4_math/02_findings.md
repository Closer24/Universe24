# c4_math findings (saved as I go; numbers from my probes in this folder and the reruns)

## Reruns
probe_canon, probe_flux, probe_x, probe_xring: byte for byte (rerun_*.txt, empty .err).

## F1 (c4_canon_mesh.py) The canonical identity is unscoped and false with Meshes and on a moving clock
- Sea of bobs (light row with Meshes, value vertex): 2 dE_i = X_i + v-(r- - r+) MISSES on light's row 18,694 of 19,152
  gear-rounds, 0 on the bobs' row. The gap is exactly v- (F(a) + F(b)), the pull's work (0 misses).
- With 2 E' = W v+ v- - a (J + F) and the pull's Wronskian a F(b) - b F(a) beside X: 0 misses both rows. That
  Wronskian sums to 0 over the ring 400 of 400 (a flux; = div Psi_pull, the text's own Psi form with G the grip).
- The pull's flux is up to 134 times the exchange on light's row: "a hand's X_h is its own energy change" is false by
  two orders where a hand has Meshes.
- Moving clock (Animate's world + a clock row rising 1/round read into the teeth): misses 11,996 of 35,988; with the
  term (W_t - W_{t-1}) v-^2 added: 0 of 35,988.
- Exact general form (derived, measured): 2 dE' = X + (a F(b) - b F(a)) + v-(r- - r+) + (W_t - W_{t-1}) v-^2.
- The text uses the unscoped reading in The Mesh flux ("two beating hands ... there each hand's X_h is its own energy
  change"): false where both have Meshes (the both-beats world: both rows carry grips G).

## F2 (c4_pairing.py, c4_sameact.py) The run back of the tooth is not the same act on the mirrored state
- Pairing I (tooth with S+ absorbed X(S+)): the probes' run back returns 6,000 of 6,000. Pairing II (absorbed X(S)):
  tooth returns 0 of 6,000 (the quotient "negated" 6,000 trivially: |q| <= 1 and X slow).
- But the probes' backward step carries on the READ state while the forward carries on the PRODUCED state: two acts.
  MEASURED (c4_sameact.txt), the same act on the mirrored state (mirror, act, mirror), the tooth kept, 6,000 rounds:
  act B (carry on read): gears return 6,000, the teeth 0, quotients negated 5,960 (trivially, |q| <= 1 mostly 0);
  act I (carry on produced, the probes' forward): gears 6,000, teeth 0, quotients 5,960;
  act S (carry X(S) + X(S+), key 2K even, births K-1 and K): gears 6,000, TEETH 6,000, quotients 6,000; forward
  books 0 misses, the taker 0..7, k_L + k_M = 2K - 1 kept 6,001 of 6,001.
- So the text's X (one state, "no next") has no act that is its own inverse under the mirror; the fix is the two-round
  increment (the physicist's form the text calls "one form" with X), three contractions a round (J(b), J(a), J(a+))
  or a kept J, an even key and the two births (the parity trade the text lists), or an asymmetric act declared
  (against Postulate 2's "the same acts in the reverse order").
- Derivation: forward reads S=(a,b), produces S+=(a+,a). Backward reads M=mirror(S+)=(a,a+), produces mirror(S)=(b,a).
  X(M) = -X(S+), X(mirror(S)) = -X(S). F(read, produced) must satisfy F(M, mirror S) = -F(S, S+): X(read) fails,
  X(produced) fails, X(read) + X(produced) works. Only the symmetric increment is one act both ways.

## F3 (c4_torus.py) The flux on two axes and the force-leg cross vertex: SOUND, extends the text
- Torus 12x8, the engine's own gradient reading, g M (dL/dx + dL/dy) with its reaction: X_L + X_M = div_x Phi_x +
  div_y Phi_y at 19,200 of 19,200 (the x flux alone 64); torus sum 0 in 200 of 200; both fluxes odd 200 of 200;
  booked to light 618/618, 0 off (unbooked 648/618, 1,182 off).
- Force-leg cross vertex g M F_L with its reaction (both rows with grips): X_L + X_M = div Xi at 14,400 of 14,400,
  Xi(s,s+1) = -g G [a_M b_L+ - b_M a_L+ + a_L b_M+ - b_L a_M+].
- Locality: a monomial with TWO Mesh legs (grad x grad, grad x force, force x force) has a reaction reading s +- 2:
  not layable at a Node-clock. "a term with several Mesh legs sums theirs" holds for several AXES of one gradient
  leg; one Mesh leg per monomial beside value legs is forced by locality.

## F6 (c4_planck_w.py) Planck's key names W: one key per train is Planck's at one teeth count
- Animate's world, the same action 6,999 thousandths of 7 K_a laid on a circle at teeth W, 2W, 4W (beat periods 123.1,
  172.6, 240.9 rounds): at the card's key (cut at W) the taker's course 0..7, 0..5, 0..4; at the key cut at the local
  teeth 0..7, 0..7, 0..7 (misses 0 everywhere). Planck's key at 2W is 707 thousandths of the card's, at 4W 500.
- So "one odd whole number on the train card" is Planck's at the rest teeth alone; where the 00 slot differs the
  relation names another key. Scope it (the rest teeth), or OPEN with G2.

## F4 (c4_keys.py) The pair's invariant: SOUND and sharper than the text
- Closing sums C for keys 2..13: only C = key - 1 (every key, odd or even). No parity enters the pair's books.
- Animate's increments at the even key: one shared birth key/2 -> 0 misses in this run but k_L + k_M = key (the
  invariant lost; a miss needs a boundary hit); the two births key/2 - 1, key/2 -> 0 misses, invariant kept.
- Three hands: shared count in [-1, 1], 3 k0 - (shared) key = teeth's sum at 6,000 of 6,000 (a bound by the births).

## F5 (c4_td.py) T_d > 1: X on J is off in SCALE by T_d / (s T_k), not by "the floor's remainder"
- (1,1,5): X^J / X^kick = 5.000; the pair's books on X^J: the taker runs 0..35 (5 keys per real key); on X^kick 0..7.
- 2 dE = X^kick + v-(r- - r+) exact (0 of 71,988) at every gearing; with X^J 23,996 misses at T_d = 5.
- Last round's kick is recoverable from the state by the drive's own run back (carry(J(b), T_d, T_d - 1 - rd)): 0 misses.
- |X^kick_L + X^kick_M| = 0 at T_d = 5 because 5 divides f and g (no remainder). At T_d = 7 (a remainder): up to
  4,672,419 at (1,1,7) and 14,530,020 at (3,2,7), against keys of 4 x 10^28 and 6.6 x 10^28 (0 trillionths);
  X^J / X^kick = 7.000 and 1.166; the taker on X^J 0..49 (7 keys per real key) and 0..8, on X^kick 0..7 and 0..7;
  books 0 misses on both; 2 dE = X^kick + Rule3 exact 0 of 71,988 at every gearing, X^J 23,996 misses at T_d > 1.
- Road to close the OPEN: read X on the kick (two drive carries, last round's kick recovered by the drive's own run
  back, 0 misses), exact energy, antisymmetry off by the floor only (SUM |a| s T_k per round at most).
