# Term 11's count (CLICK25.md sections 0, 2, 3 and 6): the hostile mathematician's report

New to the project, 2026-10-30. Probes in this folder, all in whole numbers with the engine's own carry as the one
division, wrapping the engine's own act (t24b src untouched): `t11lib.py` (the harness), `probe_a.py` (the identity,
the evenness, the count and its misses, the four rounding rules), `probe_b.py` and `probe_b2.py` (cases built to pass
the stated rule and break; the long run; many windings a round; three hands; the click's sign backward), `probe_c.py`
(the exact exchanged wind and the hold that survives the run back), `probe_d.py` (the key's parity on the grid),
`probe_e.py` (a train over five Node-clocks, emulated), `probe_f.py` (the search for a whole-number quadratic
invariant). Each with its `.txt`. The text's own probes rerun byte for byte (`rerun/`). Notes as I went: `00_plan.md`
to `04_law_lines.md`.

## VERDICT on term 11's count: NOT PASSED

### Items, most serious first

**1. BLOCKING. The books are not a law of this count; they fail at a steady rate set by the wobble over the exchange per
round, and totally where the swing is small.** Place: section 3 Board "The books" ("the books miss in 2 rounds of
6,000 ... Rule3's turn ... named, not hidden"), section 3 Physics ("the two runs part only where the wind moves"),
section 6 item 1, and the owner's "energy and momentum are conserved in the clicks" which the text rests on.
Measured (probe_a, probe_b): on the text's own world the 2 misses are one event: at round 216 the giver clicks -1 with
x_L = -0.500432 key while the taker stands at x_M = +0.499655 key (the wobble delta = x_L + x_M = -776 millionths of
a key), the taker clicks +1 a round later; the books are open for 1 round. That is the whole mechanism: each hand's
D is rounded separately against a fixed offset, and the two D's do not sum to a constant (the act's rounded drift
breaks even the leapfrog's 2 E_shadow = SUM (W q v - a J) by 32 millionths of itself; D's remainder term adds more).
Cases that pass the stated rule and break it: the vertex weakened to g = f div 100: 5 click rounds, 4 misses, the
books open 2 rounds; the swing shrunk to A = 10^5 (the key a seventh of D_L as the text sets it): 60 click rounds, 44
misses, open 24 rounds (the wobble 1.9 per cent of a key); A = 10^4: 433 click rounds, 388 misses; A = 10^3: the FREE
hand clicks 4,731 times (its count -2..1) and the pair's books miss in 3,727 rounds. Over 60,000 rounds at the text's
swing: 40 misses of 355 click rounds (11 per cent), open 20 rounds, a steady rate (the wobble itself stays bounded,
about +-2,100 millionths in every block of 6,000; no diffusion seen). The key shrunk (g = f, D_L div 700): 625 misses
of 5,815 click rounds; D_L div 7000: 4,137 of 5,992. Three hands (a giver and two takers): every click round misses
(89 of 89), the counts' sum within [-1, 1]. Answer to the Boss's question: the miss is the count's, not Rule3's: Rule3
supplies a wobble of order A x W per gear per round, which is exactly what the text says; the count turns a wobble of
a thousandth of a key into whole windings because it rounds two quantities whose sum the act does not keep. No
whole-number quadratic form of the act's energy with the teeth is kept exactly either (probe_f: in (a, b, r) and in
(a, b, r, a+, r+), on four lays with W = 800, 10^6 and 7 and swings 300 to 10^6, 0 true invariants beyond the constant
and the identically-zero forms; the control a+ = 3 a - b finds its a^2 - 3 a b + b^2), so the OPEN question of
section 7 is answered: no form of the state closes these books. Fix: count the exchanged wind, not the held wind's
difference. In exact arithmetic the hand's wind moves per round by exactly X_M = g (M_before . L_now - M_now . L_before)
= g SUM (b_M a_L - a_M b_L), X_L = -X_M by construction (the same g, the dot symmetric): whole, read from now and
before alone, antisymmetric in the pair as an identity, the meeting of the two hands' futures and pasts at the
meshing. Measured (probe_c): |W dD_M - X_M| <= 2,607 millionths of key_w a round (Rule3's turn, as the text's work tau_D
at 2,696); carried by a tooth per train at the odd key_w born at (key_w - 1) div 2: giver -6, taker +6, 0..7, 34 click
rounds, 0 misses of 6,000, k_L + k_M = key_w - 1 at 6,001 of 6,001, the taker's X-count equal to the text's D-count
at every round of the text's run and within 1 at A = 10^4 where the D-count misses 388 times; the free hand's X is 0
by construction at every swing. The miss is then a theorem's absence, not a remainder's size.

**2. BLOCKING. "No hold survives the run back" is false as stated and is the one reason given for the count's form.**
Place: section 3 Algebra "No hold survives the run back", Board "no hold is kept (Algebra: a hold would break the run
back)", NOTES.md. The argument shows only that a held COUNT n(t-1) cannot be restored (true: D(t-1) needs a_{t-2}). A
held TOOTH of a round-computable increment runs back exactly (TERM11's lemma, probe2's 6,000 of 6,000), and the
exchanged wind X is such an increment. Measured (probe_c C3): the mirrored round's X is -X; with the tooth KEPT the
tooth returns in 6,000 of 6,000 rounds with the quotient -q; with the tooth FLIPPED as the law's (iii) says, 0 of
6,000. So a hold survives, the "third dial" is not needed for exact books (X splits the vertex's wind into the two
hands by construction), and the law's (iii) must be read by the increment's parity under the reversal: the tooth of an
odd increment is kept, of an even one (the area's tau) flipped. Fix: strike the sentence, state the lemma for an odd
increment (-X + k+ = -q key + k), and derive the count as a carried tooth of X, which also lets the act write the click
as its own quotient instead of the runner differencing two rounds.

**3. BLOCKING. A train that keeps its beat clicks at every Node-clock it reaches under this count, and the proposed law
line drops the law's "and its six neighbours" without a word.** Place: section 6 item 1 ("summed over its gears"),
section 3 Board "The hand's wind, read ... from the train's own rows", section 7 OPEN "a train across its Node-clocks".
Measured (probe_e, five hands tied in a chain by the vertex g = f div 10, one train over five Node-clocks emulated;
hand 0 turning, the rest at rest, D_lay = 0 for hands 1 to 4): hands 1 to 4 click in 12, 12, 13 and 15 rounds, counts
up to 4, 3, 4 and 7, first clicks at rounds 218, 632, 1,056 and 1,416; the five counts' sum within [-1, 1], 66 rounds
where the clicks do not sum to 0; the whole train's wind kept within 2,072 millionths of a key. A per-Node-clock D with
a per-Node-clock D_lay cannot tell a train's travel from a take, whatever the lay's held wind. The text names the
OPEN but proposes the law line anyway, and the same line says "a clock that keeps its beat does not click". Fix: no
law line until the count is of the exchange at the vertex (X, or the area, both of which read the plan's coupling
and not the Meshes' pull); keep "its six neighbours" or ask the owner's word for dropping them.

**4. MINOR. Identities and theorems cited as measurements; numbers cited from another count.** Place: section 2 "With
the mirror" and section 3 Physics ("D reads the same backward: 6,000 of 6,000"): D on the mirrored state equals D
forward because untick is exact and next x before is symmetric; a check of the code (probe_a A2 agrees, 6,000 of
6,000). "the taker holds at least one winding in about 4,920 rounds of 6,000, the clocks connecting 3 times
(probe_wind.txt)" are the tooth-carry click's numbers (probe_wind, 46 misses), not this count's; this count gives
4,919 and 3 (probe_a). "term 11's click under the 24, 24 of 24 (TERM11 Measured 4)" is the area click on the draft
act; the wind count's 48-invariance is an identity (D is a sum of each gear's products with itself). Fix: mark each as
a check or an identity; cite probe_count's numbers.

**5. MINOR. The law line's words against the derivation.** Place: section 6 item 1. (a) "read alike in both runs": the
count n is alike, the click is reversed, a take read as a give (probe_b2 c: the backward click is minus the forward's
at 5,999 of 5,999 rounds); the record's click line on the run back is -q, which the line and the schema must say.
(b) "coming apart by one winding": |q| reaches 10 at the key D_L div 700 and 95 at D_L div 7000 with g = f
(probe_b2 a). (c) "plus the half key": k_0 = (key - 1) div 2 is not the law's (i) birth key div 2 at an even key
(equal at odd ones); name (i). (d) "the one quantum per Node-clock of decision 40 (g)": 40 (g) is the coupling
family's steady count, one per Node-clock; D_lay is one per train per Node-clock. Fix each word.

**6. MINOR. The per-gear identity is written for one world.** Place: section 3 Algebra "Per gear, W D_i = W q_i v_i -
a_i J_i - a_i (r_i - r_i+)". Exact as written (probe_a A1: 0 misses of 72,000 gear-rounds) because Animate's world has
s = T_k = T_d = 1 and no Mesh, so the push is J. The act's identity is W D = W q v - a push - a (r - r+) with push =
s (F + T_k q_d); Euler's "-SUM a J = 2 V" needs the push linear in the counts, which T_d > 1 breaks by its own floor,
and the Mesh pull F puts the Meshes' energy into the Node-clock's D. Fix: write push, and name the two conditions.

**7. MINOR. "D_L + D_M is the act's invariant up to Rule3's turn" counts one Rule3 term where there are two.** Place:
section 3 Board "The books", Algebra. SUM (W q v - a J) is the exact leapfrog's 2 E, kept only where the drift is whole;
the act rounds the drift, so 2 E_shadow itself moves (32 millionths of itself over 6,000 rounds, probe_a) beside the
remainders' term a (r - r+). Fix: say both, with the number.

**8. MINOR. Words that name a dial where there is none.** Place: section 2 "What it acts on: ... the train's click tooth
k", section 3 Board "the remainder its tooth". The count's remainder is recomputed every round from the state and
kept nowhere; the meshing's click as defined acts on nothing and writes nothing: it is a reading of two rounds by the
runner. Fix: say "reading", or give it the tooth of item 1.

**9. MINOR (for the physicist). "a key of wind is a key of energy at every beat" against the text's own identity.**
Place: section 3 Physics. W D = 2 E per the identity, so a key of D at teeth W is W/2 x key in the gears' energy;
"the wind's key does not scale with W" (section 5) then means the energy per winding scales with the clock. Fix: say
which is meant, since the key is one for the board and W is not.

### The key's parity, settled by measurement (probe_d)

Both texts are right about their own rule and wrong about the other's. A function count on an exact pair (x, -x),
keys 1 to 40, x within 3 keys, 4,960 cases: CLICK25's floor with the shared offset (key - 1) div 2 and the law's (i)
offset key div 2 miss 0 times at odd keys and 120 at even ones (once per key of area, exactly where 2 x + key is a
multiple of 2 key: the half-tooth prediction of section 3 agrees in 4,960 of 4,960 cases); EDGE's centred split with
the tie taken even, read as a function, and the law's own (iv) half away from zero miss 0 times at every key, odd or
even. EDGE's split as a tooth-carry born at 0 on areas (A, -A) over three rounds: 0 misses of 44,640 carries (the
plain carry born at (key - 1) div 2 on the same data: 1,598 misses, all at even keys). On the text's run the four
rules agree at the odd key and at the two even keys beside it (no tie fell in 6,000 rounds; the 2 misses are the
wobble's, item 1, not parity's). So: the pair's books need an ODD ROUNDING (n(-x) = -n(x)), not an odd key; the floor
carry with one shared birth is odd only at odd keys, which is the whole content of "the births must sum to 2 key - 1".
The odd key is CHOSEN only as long as the rounding is the plain floor; with EDGE's split, or with the law's (iv), the
key has no parity condition, as line 100 says of every teeth count. The text should say which rounding it chooses and
why, and drop "its reason exact". (Whether a tie rule is an "if" under Postulate 5 is the owner's; EDGE builds it from
lit() and carries.)

### What is SOUND, with numbers

- The text's probes rerun byte for byte (probe_count.txt, probe_wind.txt).
- The per-gear identity W D_i = W q_i v_i - a_i J_i - a_i (r_i - r_i+): exact, 0 misses of 72,000 gear-rounds in the
  text's world (with push = J there).
- The count as computed: giver -6, taker +6, the taker 0..7, 35 click rounds, 2 misses, n_L + n_M in {-1, 0}; the
  wobble within [-1,855, +1,712] millionths of a key and 3,351 in a round; W (D_L + D_M) within 264 millionths; the
  free hand 0 clicks and within 1,855 millionths at A = 10^6; the giver on a line, the taker 0..7, 4 misses (two
  events); the line hand has a wind (the TERM11 math reader's blocking item answered).
- The miss located and explained exactly (round 216, delta = -776 millionths against an offset of 431 from the edge).
- D even under the mirror (as a theorem; measured 6,000 of 6,000) and the count the same in both runs; the click's sign
  reversed (5,999 of 5,999).
- The nearest-whole-number reading at an odd key (no ties), so the hand holds n -/+ 1/2 keys at the n-th click.
- The bound (n - 1) div 2 on the counts' sum: three hands within [-1, 1], five within [-1, 1].
- The half-tooth parity claim of section 3 (both born at u = key miss iff 2 A + key = 0 mod 2 key): 4,960 of 4,960.
- The wobble bounded over 60,000 rounds at the text's swing (no diffusion seen).
- The exchanged wind X as a whole, antisymmetric, round-local form: X_L + X_M = 0 in 6,000 of 6,000 rounds by
  construction; |W dD_M - X_M| <= 2,607 millionths of key_w; and the X tooth-carry's books 0 misses, its count equal
  to the D-count at the text's swing: the count's physics (the seven windings passing and returning, the clocks
  connecting three times) stands; its bookkeeping does not.

### Solution24

One line: a count's books are a law only where the counted increment is exactly antisymmetric by an identity of the
act, and every claim of a count is measured on the lay built to strain it (the weak vertex, the small swing, the small
key, the travelling train) before a law line is proposed; the method's step 6 was run on one lay and a law line was
written over a named OPEN.
