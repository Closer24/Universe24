# G5, the split click's draw: what stands where decision 29's c stood

David, 2026-10-30, on Sofer's ask (#2187 6518975579, item 3: "the build has held no beat count since G1b ... so the
draw needs a source for c on the act. Which gear's tooth or sum is c is yours and David's to name") and the owner's
word of 11:1x UTC (derive what the Node-clock needs to close; everything to stand with a hostile mathematician and a
hostile physicist). Animate's measurement on the act as built (ANIMATE-CLICK/draw.py) is the starting point. The probe
is derive/david_open/node/g5_draw.py, its output g5_draw.txt beside it, whole numbers alone, about 16 s.

**The finding in one line:** no tooth is needed where c stood. The Node-clock's own fine teeth already move more than
any dial wherever a click can happen. Read them as a fraction of one turn of the Node-clock's own teeth, and rank that
fraction against the sizes by cross products. Then Born's rule holds for any total of sizes, to within one pitch of the
teeth.

## 1. In clocks

- **The dust.** Every gear's turn leaves the part of a tooth that did not make a whole one: its fine tooth, kept for the
  next turn. Every round the pushes move it: the Meshes' pull by whole sixths of a turn (the teeth are six grips),
  the coupling by finer steps. So round after round it lands somewhere new in the turn, at large swings and at
  swings of 10 counts alike.
- **The split.** Two twins share a winding that completes in a round, and neither holds it whole. The Node-clock must
  say which twin takes it.
- **The pointer.** The Node-clock sums the fine teeth of the scalar gears at itself and its six neighbours, and reads
  where that sum stands within one turn of its own teeth: a pointer on its own face that no round winds. The twins share
  the face in proportion to their sizes, and the twin under the pointer takes the whole winding.
- **No dial.** The old c stepped once a beat. The Node-clock counts nothing: no round, no beat, no time. Wherever a
  coupling pushes, the dust already moves more than a dial would. Where no coupling pushes, no area moves, so nothing
  clicks and nothing is drawn (Animate's "no vertex, no click").
- **The run back.** The click writes into no gear's teeth, so the run back reads the same pointer and undoes the same
  click.

## 2. On the board

**The rule.** At the Node-clock that draws, with W the teeth its round's carry used:

    V = the sum, over the Node-clock and its six neighbours, of every A1 row's fine tooth
    d, from carry(V, W, 0): d = V - W (V div W), the remainder
    the part = SUM_i nonneg(d L - S_i W), over the cumulative sizes S_1 < ... < S_(m-1), L their total

One carry; the rank count compares two products, as fractions are compared everywhere in the law; no count, no dial, no
gcd, nothing held. Each size is decision 29's product of the part's size on the forward board and on the backward board.

**Why A1 rows alone.** An A1 row's fine tooth is the same under all 24 turns. A T1 or A2 row's tooth flips to W - 1 - r
under some turns, so a sum over it would draw differently on the turned board.

**The lemma.** Let X be one A1 fine tooth of the drawing Node-clock itself, and p the pitch of its row: the gcd of W
with every move its fine tooth makes, so X stands on a progression of step p in [0, W), W / p points. Write Y = V - X.
Suppose that, given Y, X is spread evenly over its progression. Then for every part, however large L is,

    | P(part i) - sigma_i / L | < p / W.

Proof. Fix Y = y. Then d = (X + y) mod W is spread evenly over a progression of step p in [0, W), since a shift on
the cycle keeps the even spread. Part i is drawn when S_i W <= d L < S_(i+1) W, an interval of d of length
sigma_i W / L. A progression of step p holds within 1 of (the length) / p of its points in any half-open interval,
so P(part i | y) is within p / W of sigma_i / L. Averaging over y keeps the bound. Nothing asks the rest of V to
stand on X's lattice.

**Why the law's form fails, d = (c + V) mod L, part = SUM_i nonneg(d - S_i):**

- **(i) The pitch.** Every fine tooth stands on its row's lattice (born at W div 2, moved by multiples of its pitch).
  When every A1 row's pitch shares a factor q with L, V mod q never moves, so d mod q never moves, the part's chances
  are multiples of q / L, and they miss the sizes. On the probe's board every pitch is even (the grip, 4 and 2), so V is
  always even: at L = 2, part 0 is drawn every time.
- **(ii) The span.** V stays below 35 W at most (five rows, seven Node-clocks). When L is past V's top, d = V and every
  draw falls in the first parts. A size as a norm of counts, squared on two boards, reaches 10^28 at swings of 10^7.
- The fold at W meets both: the pitch enters only as the bound p / W, and L enters only through the products.

**c struck.** The node holds no count (TENSOR24_NODE.md section 0; G1b). The dial's own property, each part drawn
exactly its size times over L consecutive beats, gives a partition noise below the binomial, which nature does not show.
Where V moves, the dial changes no measured number; where V does not move, nothing clicks. Animate's two candidates:
(a) a time gear stepping one count a beat is a dial with a train of its own, struck on the same ground; (b) the sizes
read within V's span is what the fold does, at the teeth's resolution p / W.

**The pitch is the strengths'.** With the plan empty, every push is a multiple of the grip and every fine tooth takes 6
values, so d takes 6. Term 6's strengths make the pitch small: on G3's probe numbers, 4 on matter and 2 on the held
count. So G3's strengths, still OPEN, owe one condition to the draw: their gcd with the grip is small against W.

## 3. In the clicks

The physics is read after the clicks, on the record, never on the board. The draw reaches the record only as which part
took the quantum.

- **Born's rule.** Over many splits, part i takes the quantum with frequency sigma_i / L. With a silent future
  (the backward sizes alike) that is the forward sizes' share, as decision 29 has it.
- **Independent trials.** The count of one detector's clicks over N splits spreads as the binomial, N p (1 - p): no
  runs, no alternation. Nature's beam splitter does this. Random number generators built on single photons at a beam
  splitter pass the standard randomness tests (Jennewein and others 2000; Stefanov and others 2000).
- **No signal.** d is read within one Mesh. No setting farther away moves it.
- **Departures, named:**
  - Born holds to within p / W, about 4 x 10^-23 on the probe.
  - The outcome is fixed by the dust, a hidden variable at the Node-clock. That gives the statistics of one particle's
    splits. Bell's correlations between distant clicks are not reachable by this draw alone; they stand on the two
    boards (decision 28), outside this page.
  - A split where no A1 row near the click is pushed has a frozen pointer. That is a click among T1 trains alone with no
    held count. Term 5 pushes the clock family's 00 and trace slots (N2), and they are A1 rows, so once term 5 is built
    every motion moves the pointer. Until then that case is OPEN by name.

## 4. Measured (g5_draw.txt)

The board: 6 by 6 by 6 Node-clocks; light, matter (two parts each) and the held count, all A1; W = 6 grip. Term 6 at
G3's probe strengths: g = 227442851386684, kappa = W div 16, lam = 4548860, the least whole multiple of 4 with
2 kappa lam >= g^2. 400 rounds read from round 20, 86,400 draws.

| Check | The plan empty | Term 6 |
|---|---|---|
| Pitch: light, matter, held count | the grip, three times (6 values) | the grip, 4, 2 |
| d = V mod W: distinct values in 86,400 | 6 | 86,400 |
| chi-square of the tenths, on 9 | 57,605 | 2.30 |
| one half, two rounds in a row / one Mesh apart (500 if independent) | 499 / 499 | 500 / 500 |

Born with term 6, part 0 of sizes S1 and S2 (z^2 near 1 or below is chance):

| S1 : S2 | the law's d = V mod L | the fold at W, cross products | partition noise of the fold (1000 = binomial) |
|---|---|---|---|
| 1 : 1 | 86,400 of 86,400, z^2 86,400 | 43,209, z^2 0.003 | 959 |
| 1 : 2 | 28,657, z^2 1.07 | 28,787, z^2 0.008 | 1013 |
| 3 : 7 | 34,391 for 25,920, z^2 3,955 | 25,955, z^2 0.067 | 1007 |
| 10^6 : 3 x 10^6 | 21,611, z^2 0.007 | 21,611, z^2 0.007 | 1025 |
| 10^30 : 3 x 10^30 | 86,400 of 86,400, z^2 259,200 | 21,611, z^2 0.007 | 1025 |

- **Sizes read from the same state as V** (S1 = m_re^2 + 1, S2 = m_im^2 + 1 at the drawing Node-clock): 42,837 against
  42,802 expected, z^2 0.108.
- **Only at the rounds where a Node-clock's swept area crosses a key** (Omega = m_re p_im - m_im p_re, the key 10^10 W,
  about seven times the area's median): 14,333 crossings; chi-square of the tenths of d 9.73 on 9; Born on the state's
  sizes, 7,040 against 7,034, z^2 0.016.
- **The dial**, c one count a round: with term 6 it moves nothing (one half 500 to 501 per mille, partition noise
  940 to 1032, against 968 to 1034 with c struck). With the plan empty at L = 1,000, both degenerate: V is a multiple of
  the grip, so V mod 1,000 never moves; the dial gives the same half in 1,000 of 1,000 pairs, and the partition noise is
  0 either way.
- **The run back:** 300 rounds out and back by the act's own untick; the draw recomputed equal at 300 of 300 rounds
  back; the lay returns bit for bit.
- **The 24:** with the state turned by each turn and both ticked, V at the image Node-clock equals V at the original at
  every Node-clock, 24 of 24.
- **The two hardest lays** (the held count laid at n, so only matter moves it), with a part of 1 in 100, whose
  interval needs the fine digits and not only the halves:

  | Lay | distinct d | chi-square on 9 | one half, two rounds in a row | the 1-in-100 part | in two rounds running |
  |---|---|---|---|---|---|
  | matter laid to 10 counts, every Node-clock | 86,400 of 86,400 | 9.51 | 499 | 862 for 864 | 13 for 8 |
  | a cold board, one packet near 100 counts, read on its 27 Node-clocks | 10,800 of 10,800 | 12.24 | 502 | 127 for 108 | 1 for 1 |

  At 10 counts the part fell in two rounds running 13 times for 8: the dust moves less than a turn a round there, a
  hint that draws one round apart are not quite independent at a resolution of 1 in 100. A click is many rounds
  from the last, so this bounds the worst case.

## 5. What stands (term 12's entry for the architecture document)

- **Clock:** the Node-clock reads where its scalar gears' dust stands within one turn of its own teeth, and the twin
  whose share holds that point takes the whole winding. No count, no dial.
- **Board:** d = V mod W, one carry, V the seven Node-clocks' A1 fine teeth; the part by the rank count over d L against
  S_i W; nothing written, so the run back reads the same d.
- **Clicks:** Born's frequencies by the sizes, to within p / W; binomial partition noise; no signal past one Mesh.
- Algebra: the lemma above. Home: owed in code at G5, beside term 11's click tooth. Status: DERIVED; CHECKED on the
  node's act with term 6 at G3's probe strengths.

## 6. OPEN

- **The owner's word:** decision 29's d = (c + V) mod L, c the beat count, becomes d = V mod W with the rank by cross
  products, c struck. The law's wording follows his word (Sofer's 6518975579).
- **G3's strengths** set the pitch p; the draw asks only that p be small against W.
- **The case with no A1 row pushed near the click,** until term 5 is built (section 3).
- **The sizes** (G5): the forward norm and the backward share, decision 28's form on the act.
- **The spread of the dust** is a property of the act, CHECKED on one board (216 Node-clocks, 400 rounds, one set of
  strengths, four lays) and OPEN in general; with no coupling there is no click.
