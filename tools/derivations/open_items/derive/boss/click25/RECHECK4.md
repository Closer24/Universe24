# RECHECK4: the final mathematician's two blocking items on COUNT4, checked by the deriver (notes, saved as I go)

Source: scratchpad/c4_math/03_report.md with c4_sameact, c4_canon_mesh (and c4_td, c4_torus, c4_keys, c4_planck_w).
Order: the law of findings: break each item down, think it over again, then measure (reruns, my own probe, a case
built to break his reading). No fifth text until the final physicist's report and Big Pic's word.

## Item 1: the click tooth's run back is not the same act on the mirrored state

**His finding, broken down.** probe_x's forward carry used X of the state the round PRODUCES (xs[t-1] = X(states[t]),
states[t] the output of round t); its run back used X of the state the backward round READS (the mirror of states[t]).
Those are two rules, hence two acts. One act must take its increment by one rule from what the round has: the read
state S = (a, b) and the produced state S+ = (a+, a).

**On paper.** The forward round t reads S = (a_t, a_t-1), produces S+ = (a_t+1, a_t). The backward round undoing it
reads mirror(S+) = (a_t, a_t+1) and produces mirror(S) = (a_t-1, a_t). The lemma -X + k+ = -q key + k inverts the
tooth (kept) only if the backward increment is minus the forward one.
- Act B (the read state): forward X(S); backward X(mirror(S+)) = -X(S+). Not -X(S). Fails.
- Act I (the produced state): forward X(S+); backward X(mirror(S)) = -X(S). Not -X(S+). Fails.
- Act S (both): forward X(S) + X(S+); backward -X(S+) - X(S). Holds.
He is right. The reversal of the round maps the window (a_t-1, a_t, a_t+1) to (a_t+1, a_t, a_t-1); an increment
runs back under one act iff it is odd under that reversal of the window. X(S) and X(S+) are exchanged (and negated)
by it; only their sum is odd.

**The case built to test his "only".** His "only" is among increments linear in X(S) and X(S+). The reversal of the
window has another odd form with the Wronskian's shape: G = a_t+1 J(a_t-1) - a_t-1 J(a_t+1), the next against the
before, the mirror's own pair (as D = now^2 - next x before is built on the same window). Under the reversal
G -> -G exactly; for a quadratic one-potential vertex G_L = -G_M exactly (the same symmetric bilinear argument);
the own spring's G is 0 (a+ (-2 f b) - b (-2 f a+) = 0). It needs two contractions, J(b) and J(a+), not three; for a
vertex whose legs are at the Node-clock J(a+) is the Node-clock's own (a+ is the round's output); for a Mesh leg
J(a+) would need the neighbours' a+, which one pass does not have (OPEN with the Mesh flux road, as before). Its
size is about X(S) + X(S+), two rounds' passing: the key is about doubled.

**The key's parity.** His "the key doubles and is EVEN" holds if the key is set to exactly 2 K. The key is the train
card's one odd whole number, CHOSEN, fixed by Planck's relation only to the nearest whole (for G: K_G^2 W^2 = 16 f
(2 W - f) K_a^2 to the nearest whole, where an odd choice is at hand). So the odd key and the shared birth are not
lost by the symmetric form; the owner's choice stands as it was, if he wants it. To measure: acts B, I, S, G on
Animate's world: teeth returned by ONE act (mirror, act, mirror), quotients negated, the pair's books, the free hand,
SUM G / SUM X.

## Item 2: the canonical identity holds on one board only

**His finding, broken down.** 2 dE_i = X_i + v- (r- - r+) with 2 E_i = W v+ v- - a J was measured on Animate's world
(no Mesh, standing clock, s = T_k = T_d = 1) and stated for every board. On the sea of bobs (light carries Meshes)
it misses on light's row; on a rising clock too.

**On paper, the general form.** The act's identity per gear at round t: W_t q + r+ = W_t v + P(a) + r, P = J + F the
whole push (s = T_k = T_d = 1); at round t-1: W_t-1 v + r = W_t-1 v-- + P(b) + r-. With 2 E'(t) = W_t v+ v- - a P(a)
and 2 E'(t-1) = W_t-1 v- v-- - b P(b):
  2 E'(t) - 2 E'(t-1) = v [W_t q - W_t-1 v--] - a P(a) + b P(b)
  W_t q - W_t-1 v-- = P(a) + P(b) + r- - r+ + (W_t - W_t-1) v
  => 2 dE' = a P(b) - b P(a) + v (r- - r+) + (W_t - W_t-1) v^2
           = [a J(b) - b J(a)] + [a F(b) - b F(a)] + v (r- - r+) + (W_t - W_t-1) v^2.
His general form, exactly. My probe_canon's P was J alone (F = 0 there, W fixed), so it held there and nowhere else.
The pull's Wronskian a F(b) - b F(a) is the pull's flux (Psi with the grip as its G), summing to 0 over a closed
region; the clock's term (W_t - W_t-1) v^2 is the moving clock's. He is right; the identity is scoped and the general
form is the one to give. To measure: rerun c4_canon_mesh; then my own check of the general form on the sea and on a
rising clock, and the one case where the clock's term alone is present (a rising clock with no Mesh).

## Measured so far
- His c4_sameact and c4_canon_mesh rerun byte for byte (rerun_c4/).
- probe_canon2 (mine): a rising clock with NO Mesh (Animate's world, the teeth at rest raised by one a round from
  outside, 3,000 rounds, 35,988 gear-rounds): the text's form misses 11,996 (his number on his rising clock, which
  had the clock as a row); with the clock's term (W_t - W_t-1) v-^2 added, 0 misses; the term up to 2.5 x 10^9.
  So item 2 stands in each of its three parts: the pull's Wronskian (his A), the clock's term (his B and mine), and
  the gearing (his c4_td). The identity is Animate's world's; the general form is the one to write.
- probe_sameact (mine, probe_sameact.txt; one act both ways, mirror / act / mirror, the tooth kept, Animate's world,
  6,000 rounds): B (the read state's X) teeth return 0 of 6,000, quotients negated 5,960; I (the produced state's X)
  0 and 5,960; S (X(S) + X(S+), at the nearest odd whole to twice the key) 6,000 and 6,000, books 0 misses, the
  taker 0..7; G (a+ J(b) - b J(a+), the same odd key) 6,000 and 6,000, books 0 misses, the taker 0..7. Summed
  passing to the taker over the run against the one-round X's: G 1.996, S 1.999. G_L + G_M = 0 in every round; G on
  the backward round is -G in every round; the free hand's SUM |G| = 0. His B, I, S numbers reproduced exactly.

## Conclusions, by the law of findings

**Item 1 stands.** The lemma was exact; "by the act alone" was not: probe_x carried forward on the produced state
and back on the read state, two acts. A same-act run back needs an increment odd under the reversal of the round's
window (before, now, next). His fix, act S, works (6,000 of 6,000). His "only" holds within the class he named
(combinations of X(S) and X(S+)); outside it the window has a second odd form, G = next . J(before) - before . J(next),
which also runs back by one act (6,000 of 6,000), with TWO more contractions (J(b), J(a+)) rather than three, the
same exact pair antisymmetry, the free hand's 0, and the books closed at an ODD key: the nearest odd whole to twice
the one-round key. So what the item forces is: the passing is read on the window's two outer slots (or on both
one-round halves), "with no next" is struck, and the record's -q on the run back stands; what it does not force is
the key's evenness: the key is the card's CHOSEN odd whole, fixed by Planck's doubled relation to the nearest whole,
and the shared birth stands. The owner's half-open decision is touched only if he sets the key to exactly 2 K (act
S's literal double): then even, the births K - 1 and K told apart, or EDGE's split. I would propose G at an odd key.
Two readings of G beside it: it is the mirror's own pair (the mirror swaps before and next), and it sits on the same
window as the wind D = now^2 - next x before, D even and G odd under the mirror as they should be. For a vertex whose
legs are at the Node-clock, J(a+) is the Node-clock's own (a+ the round's output), one pass; for a Mesh leg, J(a+)
needs the neighbours' a+, which one pass does not have: OPEN with the Mesh flux road (G3), as before. Postulate 2 is
not bent; the fourth text's claim is withdrawn and replaced.

**Item 2 stands.** The canonical identity is Animate's world's (no Mesh, a standing clock, s = T_k = T_d = 1). The
general form, derived here from the two consecutive act identities with the whole push P = J + F and the two teeth
W_t, W_t-1, is his: 2 dE' = X + (a F(b) - b F(a)) + v- (r- - r+) + (W_t - W_t-1) v-^2, 2 E' = W v+ v- - a (J + F);
measured by him on the sea (0 misses with the terms, 18,694 without on light's row) and on his rising clock (11,996 /
0), and by me on a rising clock with no Mesh (11,996 / 0: the clock's term alone). The fifth text scopes the identity,
gives the general form, says in Clicks "summed over a closed region, or at a Node-clock without Meshes", and rewrites
the two-beating-hands sentence as "each hand's X_h plus the pull's flux through its Meshes is its own energy change".

**Minors, to fold when the fifth text is written:** 3 (X on J off in scale by T_d / (s T_k); the kick's X, with last
round's kick recovered by the drive's own run back, is the road: accept, with his numbers); 4 (one Mesh leg beside
value legs, its flux summed over the axes it reads; the force-leg cross vertex's flux Xi: accept); 5 (Planck's key
at the rest teeth, or OPEN with G2 beside the moving clock; the checker's half-step tolerance by two carries; load.py
has no key, card or checker today: accept); 6 (the 24 on a moving clock measured under the half-tooth act: say it in
the claim); 7 (folded into item 1 above: the round reads three slots).

**Solution24:** his line taken: a new dial's run back is checked as the same act on the mirrored state, and an
identity measured on one world is scoped to that world's push until the act's general form is written.

**Waiting on:** the final physicist's report and Big Pic's word (the lead's order). No fifth text yet.

# The final physicist's three blocking items (c4_phys/REPORT.md), checked

## P-item 1: Planck's key at the rest teeth only

**His finding, broken down.** With W = rest + the 00 slot and the beat cos theta = 1 - f / W, every eigenmode has
E = sin theta(W) x I exactly, so one action quantum K_a is 2 sin theta(W) K_a of wind; the card's one key counts the
same 7.00 K_a as 0..7 at rest, 0..4 at 4 x rest, 0..2 at 16 x rest. A local key needs sin theta(W), a root.

**On paper.** The act's 2E = W v+ v- - a J for the sprung gear (J = -2 f a, a+ = 2 cos theta a - b with cos theta =
1 - f / W): v+ v- = ((2 cos theta - 1) a - b)(a - b), so 2E / W = a^2 + b^2 - 2 cos theta a b, which on the eigenmode
a_t = A cos(theta t + phi) is A^2 sin^2 theta; the action (the (a, p) area over 2 pi, p = W v) is W A^2 sin theta / 2.
So E = sin theta x I: his theorem holds. The forms the act holds whole are the wind D = A^2 sin^2 theta, cos theta =
1 - f / W (a ratio) and, for a two-part hand, the area Omega = W A^2 sin theta (the action itself, whole, no root). For
a one-part hand sin theta enters only by its square, f (2W - f) / W^2: no whole form of (a, b) gives I; I^2 = W^4 D^2
/ (4 f (2W - f)) is a whole ratio. He is right. To check: his pa_deep rerun; my own course at 4 x rest.

**The owner's lead, weighed.** "The action of a hand from its now and before slots together": in the (now, before)
plane a one-part hand runs on an ellipse of area pi A^2 sin theta (the action is W times it over 2 pi); the wind D is
the double area of the chord-triangle swept in one round (D = a.a - a+ b is the cross product of (a, b) and (a+, a));
summed over one turn of the hand the triangles make the inscribed polygon, pi A^2 sin theta x (sin theta / theta): the
action to order theta^2, the lattice's own order, with no root, when the turn is closed by the hand's own beat. So
the action is reachable from the two slots either (i) as the area of a two-part hand, exactly, or (ii) for a
one-part hand as the wind summed over its own turn, to theta^2, the turn being the clock's own count. Neither is a
per-round key: (i) is the first text's count (Planck at every depth, the books exact under the common turn); (ii)
needs the hand's turn as the dial that closes it. The wind's per-round key at a deep clock is 2 sin theta(W) K_a,
and the decoder can read it from the record's passed wind and 00 slot by squares (n^2 4 f (2W - f) K_a^2 <= X^2 W^2,
whole numbers, no root). No price chosen: the fifth text states the theorem, the measurement, and the two forms.

## P-item 2: the test world is tachyonic

**His finding, broken down.** A value vertex g L M between beatless light (no spring) and a beating bob has the
pair's stiffness [[2 G (1 - cos k), g], [g, 2 f]] with determinant -g^2 at k = 0: light's uniform mode grows by
about 1 + sqrt(g^2 / (2 f W)) a round, x100 in 400 rounds on my sea. The derivative vertex g SUM M_s (L_s+1 - L_s-1)
has 4 G f (1 - cos k) - 4 g^2 sin^2 k = 4 (1 - cos k) [G f - g^2 (1 + cos k)] > 0 at every k for g^2 < G f / 2.

**On paper.** V = (G / 2) SUM (L_s+1 - L_s)^2 + f SUM M^2 + g SUM L M at wavenumber k: the form above; det at k = 0 is
-g^2 < 0: one negative direction (L uniform, M = -g L / 2 f): no ground state, a growing mode. The derivative form's
determinant as he writes it, positive for g^2 < G f / 2. He is right: the value-vertex sea has no ground state, and
"if G3's plan reads values alone, nothing is needed" does not hold for a beatless train; light on matter lives in the
Mesh-leg branch, where the per-Node-clock books close only with the booking declared (N5). The identities measured on
the sea are algebra and stand; the physics sentences on it fall. To check: his pt_tachyon rerun; my own: light's
uniform mode on my sea against the derivative sea.

## P-item 3: the clicks' books stay open under emission and absorption

**His finding, broken down.** One excited bob (7 quanta) in the stable derivative sea gives 6 keys (6 lines) while the
191 other bobs hold 5.4 quanta and write 2 lines (no site above one key): the take is spread below a key per site;
at smaller keys 94 to 100 percent of the lines are to-and-fro (a driven hand's reactive exchange); the board
conserves and the clicks lose it.

**On paper.** TERM11's bound stands: a winding spread over n Node-clocks in shares each below half a key clicks
nowhere (P5), and a reactive exchange below the quanta moves a tooth to and fro. A per-Node-clock tooth reads what
passes at its Node-clock; it cannot read a take spread over many. The law's own answer is the backward run: the click
is the meeting of the forward run from the emitter with the backward run from the realised click (line 1021; decision
34, the backward board carrying the split click's which back to the birth), which makes the spread take whole at
one Node-clock: term 12's draw and the backward board, not term 11. He is right that term 11 alone cannot close
these books; the fifth text says so as a theorem (the bound) and names the term. The to-and-fro: "never flickers" is
for a steady hand; a driven hand's reactive wind passes and returns, and the record's net over a window is the
decoder's; the click line stands as written (the passing that round). To check: his pg_emission rerun; what a break
would be: a take made whole at one Node-clock by the backward run, which no probe here can build.

## Measured (probe_phys5.txt, mine; his pa_deep, pt_tachyon, pg_emission rerun byte for byte, rerun_c4/phys.log)
- P-item 1: the same action 7.000 K_a at W and at 4 W (the swing 707,107, the im slot at the halved sin theta): the
  card's key counts the taker 0..7 at W and 0..4 at 4 W (totals -1 / +1), the odd local key 0..7 (totals -2 / +2),
  0 misses everywhere; the card's key by squares at 4 W: 3,998 thousandths of Planck's 1,000. His numbers.
- P-item 2: light's uniform mode on my value sea, window means of 50: 1,065 -> 105,650 thousandths of the lay's
  (x100 in 400 rounds), the squares rising in the last window; on the derivative sea within +-63 thousandths and the
  squares flat (1,719..1,732). det at k = 0 for the value vertex -g^2 = -2.5 x 10^9; g^2 < G f / 2 (2.5 x 10^9 against
  5 x 10^11) for the derivative vertex. His reading stands; my sea has no ground state.
- P-item 3 (reduced: 48 Node-clocks, 800 rounds, one bob of 7 keys): the emitter 7,000 -> 5,768 thousandths, 1 line
  (net -1); the other bobs together took 1,045 thousandths of a key net and wrote 0 lines (the largest |net| at one
  site 0): the spread take below a key per site, the board's books closed, the clicks' open. His structure.

## Where the five items stand after the check
1 (the same act): stands; the fix is a window-odd increment: his S (three contractions) or G (two); the key stays
  CHOSEN odd under either unless set to exactly 2 K. 2 (the identity): stands; the general form is his and mine.
P1 (Planck at depth): stands as a theorem (E = sin theta(W) I); the per-round key at depth is irrational; the forms
  that carry Planck at every depth are the two-part hand's area (exact) and the squares (the decoder); the one-part
  hand's action over its own turn to theta^2. P2 (the tachyon): stands; light on matter is the Mesh-leg branch; my
  sea's physics sentences fall, its identities stand. P3 (the open books): stands as a theorem of the per-Node-clock
  tooth; closed only by the backward run's meeting (term 12 / the backward board), named OPEN for term 11.
