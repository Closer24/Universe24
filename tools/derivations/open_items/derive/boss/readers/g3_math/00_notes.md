# g3_math: the hostile mathematician's notes on G3 (the coupling family, whole-speed part)

Read: G3.md, G3_MEASURES.md, NOTES.md, lab.py, p0..p7 (.py and .out); engine/contract.py, kinds.py, step.py,
state.py, mesh.py, algebra/carry.py, runner/load.py, files.py, main.py; docs/ARCHITECTURE.md whole; ALGEBRA.md
line 35 (decisions 35, 37, 38, 40 (a), (d), (g), (h); the time gear's spring; the principle's item (4)), lines 84,
88, 90, 92, 94, 96, 100, 102, 104, 106, 330; tests/frame.py (turns, turned, stored), the engine test's cube() and
turned(); FAMILIES4.md, families/NOTES.md, FAMILIES3.md (the contraction's group passage).

## The act, exactly (for every derivation below)
- v_t := W (a_t - b_t) + r_t (the "velocity in teeth", with the remainder). Then u = v_t + J_t, q = floor(u/W),
  r+ = u mod W, a+ = a + q, b+ = a, so v_{t+1} = W q + r+ = u = v_t + J_t EXACTLY, and a_{t+1} = a_t + floor(v_{t+1}/W).
  The act is the exact integer leapfrog: v += J(a); a += floor(v / W). (T_d = 1 makes q_d = J, r_d = 0 always.)
- contract.pushes: a monomial f x_a x_b x_c x_d pushes each leg by -f times the other three = -dV/dx exactly, so J = -grad V
  for V = sum of the monomials, and a leg standing twice is pushed twice (the factor 2 of the derivative).

## 1. The theorem of the turn (G3 section 2.1), re-derived
- Own spring K on a row: a+ = 2a - b + floor((r - K a)/W). Independent of r for all r in [0, W) iff K = c W. OK.
- With K = c W: a+ = (2 - c) a - b, r untouched. Characteristic lambda^2 - (2-c) lambda + 1.
  * |2 - c| < 2: on the unit circle, bounded. |2 - c| = 2 (c = 0 or c = 4): a double root +-1 with a Jordan block:
    LINEAR GROWTH, unbounded. The text's "bounded iff |2 - c| <= 2" is FALSE at equality; its own p6 (i) shows it
    (2W: "marginal linear growth"; 0: "drift"). And 2.4 says "bounded for K/W in [0, 4], the edge 4 marginal with a
    linear growth": a contradiction in terms. The window is the OPEN interval 0 < K/W < 4.
  * periodic with whole coefficients iff 2 - c in {-1, 0, 1}: periods 3, 4, 6. OK.
- THE KEY FACT THE TEXT MISSES: at K = 2W every row ALONE is (a, b) -> (-b, a), period 4, with now^2 + before^2 held
  per row. The two rows re, im are INDEPENDENT (no monomial couples them). The "Gaussian unit" (re, im) -> (-im, re)
  is a reading of the SEED (lab.lay_turn puts im into re's before slot), not an act of the engine. Consequences:
  * re^2 + im^2 at the now slots is constant ONLY for the quadrature seed. Seed a = (1, 1), b = (0, 0): |k|^2 goes
    2, 0, 2, 0 (period 2): the "square" is no invariant of the act. (probe q1)
  * the invariant of the act is now^2 + before^2 PER ROW (D of line 35 (4) per row); a plan's leg cannot read a
    before slot, so the text reads re^2 + im^2 as a stand-in, valid on the seed alone.
  * the "sense of the turn" is which row the seed delayed; the act has no sense.

## 2. The tie is the unit in disguise within the room
- J_x = -2 g f |k|^2 (C x) with |k|^2 = re^2 + im^2 at the now slot. While the turn is exact, |k|^2 is the seed's
  constant, so the tied hand's trajectory is BIT FOR BIT the one of the monomial (g f |k|^2 C_yz; y, z, 1, 1), the
  very "mass laid by hand on the unit" the text says the law refuses (its section 0). The held hand adds nothing but
  its back-reaction, which the room REQUIRES to be invisible (absorbed in r_k). (probe q2)
- So: within the room, a declared mass whose strength is g f times a SETTING-file integer (|k|^2); past the room, a
  medium with a frame and a sense (G5's physicist). No third regime.

## 3. Decision 40 (g) is not met: no law fixes |k|^2
- Every (re, im) is a fixed point of the turn (p1, p2 D, p7). No restoring force on |k|^2: the magnitude, the
  quadrature, the phase and the fine tooth of the held hand are all the setting file's. "one quantum per Node-clock,
  from the law and not from a file" (40 (g)) is not derived; the text's Open 3 half-says it, its Clock layer states
  "D ... is one: one quantum per Node-clock" as a result.
- The room needs the held hand's tooth born at W/2 (lab.blank): the loader's default is 0 (load.lay). With r_k = 0
  the room is 0: the first push bends the turn. (probe q3) So the setting file must lay 2 x sites teeth of 3 den Gamma^2.

## 4. The room holds half a quantum, not one -- CORRECTED BY MEASUREMENT (q4)
- My harmonic analysis (D_x = A^2 sin^2 omega, = 1 at A^2 = 500) was the wrong model at these amplitudes: the swing is a
  relaxation, and the integer per-round wind x^2 - x_next x_before averages 0.944 at A 15 and 1.000 at A 16 (g A^2 = 256),
  right at the room's edge. So the text's NUMBER stands ("about one quantum") while its ROUTE (the harmonic D_x with the
  mean x.x) does not: by that route the quantum is at twice the room. Downgraded to MINOR (M5 in 01_findings.md).
- Likewise the text's formula values at A_q (134 = 3/pi of 140.5) and the minimum 126.5 hold with the unit spring; the held
  hand bends at round 1 at A_q, so the exact turn never reaches the quantum's amplitude at k (1, 0).

## 4b. Later measurements that changed my reading
- q3 c: the tooth's walk is bounded and does not drift over 20,000 rounds at Gamma 1000 (A 10, 14, 15): the room is a steady
  state there; the text's slow walk is at larger Gamma near the edge (its p2 B). I make no leak claim.
- q11: the ring's dispersion holds to 0.1 per cent in the mode (light 156.94 / 156.8; tied 104.70 / 104.6), so M10 is "unmeasured
  by the text, true"; beside it light's wave heats fifty-fold in size by the act's rounding: a side finding for the Boss.
- q9 a: the held hand at (44, 0), K/W 3.872, runs away where the unit spring (q10) is bounded: the window's top is softer for
  the held hand than for the unit.
- q6: on the full act the 24 hold bit for bit only with the tooth flipped on negated rows (24/24 against 3/24).

## 5. The 00 slot window (section 3, "exact for |00 slot| below rest/2")
- With W = rest + c and the spring fixed at 2 rest, r at rest/2, the cycle (1,0),(0,1),(-1,0),(0,-1) is exact iff
  -rest/4 <= c < rest/2 (derivation: u = c - rest/2 at (1,0) needs q = -1, so c >= -rest/4; r walks to rest/2 + 2c
  and back). The text sampled c/rest in {-0.5, -0.1, 0.25, 0.5, ...} and stated |c| < rest/2: FALSE for
  -rest/2 < c < -rest/4. (probe q5)
- Deeper: the own spring is "rest", a loader constant, not "W" the teeth: "its own spring is its teeth" holds at
  c = 0 only; in a deeper clock the turn is held by the floor's slack, not by the theorem. To track W the spring
  would need a leg on the 00 slot, which the text refuses ("nothing on the square").

## 6. The 24 on the full act (the text: "the act commutes with all 24, bit for bit")
- p4/p4b check step.sources (J, F) only. On the carry, a negated gear's image needs its tooth flipped:
  carry(-n, W, W-1-r) = (-q, W-1-r'). Without the flip the teeth of negated T1 rows drift by 2 J per round and the
  counts part where a quotient differs. (probe q6) The law's own frame.turned permutes sites only.

## 7. Where the half-speed part touches the whole-speed part
- Both ties share k. The linear/rocking tie pushes k NOT along k (J_k_re = -g f (L.R), J_k_im = -g f (L x R)): it
  breaks the quadrature, |k|^2 wanders (the text's own p5 (b), (c)), and every whole-speed spring 2 g f |k|^2 wanders
  with it: no fixed beat. The whole-speed part cannot be certified with one k shared. (probe q7)
- The pair rule (K with A2 x K) is of the held hand's own shape (A1, A2): under its own rule the held hand ties to
  its own square (V = g f |k|^4); the plan exempts it by hand.

## 8. Genericity (the owner's law: only generic laws)
- Three selections are laid by hand in every probe: which train is held (own_turn(0)), which tie (square_tie(1, 0)),
  which are light (untied). The text's Open 1 admits the second. No loader rule is derived for any; the act ties
  whatever is laid (p6 (ii)). FAMILIES4: the norm tells no kind; here every tied kind beats alike (p6 (ii), (iii)),
  and V = g f |k|^2 sum_i x_i^2 over all tied rows is kept by every signed permutation of the tied rows ACROSS trains.
  (probe q8)
- g is CHOSEN 1 and the same for every train, so ONE mass for all tied matter (the time gear's own beat at |k|^2 = 1);
  "the spectrum of one plan is wide" needs g per train in a file: decision 35.

## 9. The relaxation period P = Gamma/(g |k|^2 A) + 4 A: derivable
- Steady cycle: stand at +A while v falls from ~W to 0 by K A per round (W/(K A) rounds), fall one count a round
  (2A rounds, v in [-W, 0)), stand at -A (W/(K A) rounds), rise (2A rounds). P = 2W/(K A) + 4A = Gamma/(g|k|^2 A) + 4A.
  Holds while K A < W (one count a round), i.e. A < Gamma/(2 g |k|^2); the "+4A" branch is wrong past A ~ sqrt(Gamma/4g)
  where the fall is more than a count a round. The text's "3/pi at A_q" extrapolates the formula to A_q = 22, outside
  its verified range (1..15) and outside the room. (probe q4 measures P at A_q with the unit spring)

## 10. Smaller
- The drive at T_d = 1 is the identity (q_d = J, r_d = 0): "the one drive serves every row" is a name on a no-op.
- lab.ratio and lab.blank use // and % outside carry (the probes' own rule), and lab.py declares the trains in code.
- "f is an exact whole number": yes, 6 den Gamma, no division needed (len(spokes) den Gamma).
