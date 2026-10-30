# Reading notes (sources read: CLICK25.md, NOTES.md, probe_wind/count.py+txt, probe2.py, click.py,
# carry.py, step.py, state.py, mesh.py, TERM11.md + 2 readers, EDGE.md, ALGEBRA.md lines 35/122/1021, ARCH term 11)

## Facts about the world (Animate's): one Node-clock, no Mesh (nb = itself -> pull = 0), W = 10^20, f = W div 800,
A = 10^6, g = f div 10, s = T_k = T_d = 1 so push = J exactly. A1 table = identity (entries 1 on the diagonal):
"through the A1 table" is the plain sum over the three components. D_L(lay) = 5 x 10^9, key = 714,285,715 (odd).

## EDGE.md's rule (section Algebra "The split", "The click's books", Measured 8)
Dial m = 2 key; n + key = q0 m + r0 (Rule3), s0 = r0 - key in [-key, key); at r0 = 0 (a tie) the count is taken
even: q = q0 - tie*odd(q0), s = s0 + tie*odd(q0)*m. So |s| <= key, |s| = key only at even q, and split(-n) = (-q, -s)
exactly. Tooth born at 0, mirrored by negation. Claim: q(A) + q(-A) = 0 at every key (4,960 cases, 0 misses), a
giver and a taker born at 0 opposite in 6,000 of 6,000 at keys 12 and 13.
=> This is round-half-to-even: an ODD function of its argument at every key. CLICK25's plain floor carry with the
shared offset (key-1) div 2 is odd only at odd keys. Both texts are right about THEIR OWN rule; the sentence
"the pair's books need the two teeth to sum to 2 key - 1 ... so the key stays odd" is a fact about the floor carry,
not about the count. To measure: both rules on the same grid and the same run.

## Decision 40 (g) (ALGEBRA.md line 35): "the coupling family's steady count is one quantum per Node-clock, from
the law and not from a file". It is about the COUPLING FAMILY's steady count. CLICK25 uses it for D_h,lay, one
held wind PER TRAIN per Node-clock (n trains -> n held winds). The identification is loose.

## Law line 35 (4) as written: "a sum of products of its gears now and before over the Node-clock and its six
neighbours". CLICK25's new line: "D = now^2 - next x before summed over its gears" -- the six neighbours are
dropped without a word, and "next" enters (it was "now and before").

## Law line 122 (i): the remainder is born at w div 2. CLICK25's k_0 = (key - 1) div 2: equal at odd keys only.

## TERM11 readers' items still relevant: MATH_2 item 6 (identities cited as measures) applies again here:
"D even under the mirror, 6,000 of 6,000" is a consequence of the exact run back (untick exact), and
"tau_D,L + tau_D,M = -(S - S)" is pure algebra (CLICK25 does label that one as an identity).
