# The hand as one Gaussian integer: what folds, what it explains, what it costs

David, 2026-10-27, 15:1x UTC, for the Boss (his eighth consultation, the task of 12:3x UTC), with his folds 1 to 4 on the head (edaf5b35c, then 608d97134 with the spin merged).

## The words

The owner's words of 12:3x UTC to the Boss, recorded by the Boss, in translation:

> "The engine must of course run in integers, but check whether representing the hand or the clock with a complex number, that is two coefficients, helps [the project]: whether it simplifies things even more into clocks, hands and pendulums; whether it shortens the functions or Rule3 somehow, when [one looks] at complex numbers; but still everything runs in integers. Do these complex numbers save [the project] tables? It is still integers, they only represent a complex number. Not mandatory, I only ask whether it simplifies, unifies and explains many things for clocks, for gears."

(The translation's first person plural is rendered in brackets.)

**The marks:**

- **measured:** by the scripts in DAVID-GAUSSIAN-HAND_CHECKS.txt, on the head edaf5b35c, and the verification and the circuit's spot check again on 608d97134;
- **checked:** whole-number algebra;
- **read:** read in the code.

**The names.** A hand at one notch is z = three + i twelve, two whole numbers. A hand's ratio is rho = pinion + i s, with |rho| = rim exactly (MS-S2). The sweep is W = Im(conj(z_now) z_before). Twin hands are (z_up, z_down).

## The answer

**Yes: it simplifies, unifies and explains, and every integer stays.**

1. **The Boss's four folds stand bit for bit.** The three charts were regenerated on edaf5b35c (folds 1 to 3) and on 608d97134 (fold 4, with the spin merged). Against the committed charts, all of these are the same: the Node lines, the rows, the counts, the turns, the run back 20 of 20, the whole log, and the reading line for line. [measured]
2. **The carry on a complex gear changes no integer.** Rule3 is real-linear and its coefficients are the same for a hand's two gears, so the Gaussian carry is the two gears' carries. The mirror w - 1 - r is per gear, and so is each drive's fine wheel. [checked]
3. **Tables:**

   | table | under the Gaussian hand |
   |---|---|
   | the cycle lay's four quarter digits | go: they are the powers of i, a fold |
   | the circuit | can go, as the exact Gaussian power of a Pythagorean step: every state integer, event and reading of the three charts stands (measured) |
   | the clock's rates | stay: a real power, with no turn in it |
   | the rim | is already Gaussian (rim.py) |

4. **What it explains:**
   - the mass is the squared chord between the rest turn and no turn;
   - the light is the hand with no chord;
   - the wind is the mean of two norms, and the sweep is the count;
   - twin hands are one quaternion, and the half turns' lifts are the units of Q8 on the right;
   - the 4 pi is the unit -1 of that group.
5. **What does not fold:** one division per hand in the wind. Every event and every reading stands, but the books move by one tooth (section 3).

## 1. The Boss's folds, verified the same way

**Folds 1 to 4:**

| fold | the act | lines |
|---|---|---|
| 1 | every bilinear of a hand is one product conj(a) b, its imaginary part meshes.cross: the sweep, the lead and the frame's read; the conjugation as signs in acts.reverse | 23 fewer |
| 2 | the mesh's turn is one Gaussian square, g^2 / \|g\|^2, with g = (W + i n)(w2 + i m) | 6 fewer |
| 3 | a lay's notches are read as each gear's two shadows | 8 fewer |
| 4 | the push of a lay is one act over the hand's gears, Re conj(a) b (unspring.push_per_gear struck) | 19 fewer |

**Measured** (verify_head.py, the head's own src on the path; each chart regenerated from its world and compared key by key), the same on edaf5b35c and on 608d97134:

| chart | Node lines | rows | counts | turns | run back | log | the reading |
|---|---|---|---|---|---|---|---|
| hole | same | same | same | same | 20 of 20 | same | same, line for line |
| chiral | same | same | same | same | 20 of 20 | same | same, line for line |
| bodies | same | same | same | same | 20 of 20 | same | same, line for line |

## 2. The carry on a complex gear

Rule3 on one gear reads w a' + r' = w (2 a - b) - D a + SUM R (m - a) + r. Here w, D and the grips R belong to the clock and are the same for a hand's two gears.

So on a hand z the same line reads:

```
w z' + rho' = w (2 z - z_before) - D z + SUM R (mu - z) + rho
```

with rho = r_three + i r_twelve. The Gaussian carry takes the floor and the remainder in [0, w) part by part, so it is exactly the two gears' carries.

**Consequences:**

- the direction's mirror w - 1 - r and the negation's mirror (w - r) mod w (F48-S1) are per part;
- the exchange is the conjugate with each part's mirror (fold 1's signs);
- the unsprung hand's drive is on its three gear alone (W-S1's lay), so its write is along the real axis and stays per gear. [checked; read]

**Nothing moves.** A "one carry per hand with two fine wheels" is a spelling, not an act.

## 3. One division per hand in the wind (does not fold)

hands.wind divides each gear's own form once: "one division per line". Summing the two gears' numerators before one division gives a wind at most one tooth higher, since floor(x) + floor(y) <= floor(x + y) <= floor(x) + floor(y) + 1.

At the vacuum, for a uniform hand, the division is exact (DAVID-AMPLITUDES.md section 1), so nothing changes there. Off the vacuum, the books move.

**Measured, the hole chart under one division per hand:**

- **stand:** the Node lines, the rows, the turns, the run back, the births, the chimes and every reading row;
- **move by one tooth:** the logged falls, walls, owed and remainders of 14 births, 273 chimes and 7,105 refusals;
- **the count `booked` moves by 14:** 99,589,590,320,968,651,927,074 to ...088;
- **the take's remainder (the slack, a state integer) moves by one.**

The chiral and the bodies charts move the same way: every event and every reading stands, and the first log entry off is the 24th on the chiral and the 855th on the bodies.

**Verdict:** keep one division per gear. The per-hand division changes integers for no event, and "a division per line stays one per line" is the law's own rule.

## 4. The circuit as an exact Gaussian power

**The walked orbit.** The standard's pair at a count is the orbit X e^(i n theta_0), with cos theta_0 = 1 - 1 / (2 Gamma^2) [read: features/standard]. It is walked by Rule3's rotation act, one act per count per line. It is stored in a table to the half turn H (3,142 at Gamma 1,000) and read beyond it by the mirror. Its magnitude drifts by the walk's rounding (features/standard: within (Gamma + 1) / 2 of X and at most 1.42 N + 2.3 Gamma levels over N acts).

**The Gaussian step.** sin theta_0 is no rational, so theta_0 has no Gaussian point on the circle. The nearest Gaussian step is the half-angle tangent 1 / (2 Gamma):

```
zeta = (2 Gamma + i)^2 = (4 Gamma^2 - 1) + i 4 Gamma,   |zeta| = 4 Gamma^2 + 1
```

This is a Pythagorean triple, so the point zeta / (4 Gamma^2 + 1) lies exactly on the circle.

**Its read:**

```
pair(n) = X zeta^n div (4 Gamma^2 + 1)^n
```

That is one exact Gaussian power and one rounding per gear at the read:

- no walk and no drift, because the norm is multiplicative and |zeta^n| = (4 Gamma^2 + 1)^n exactly;
- beyond the half turn the mirror read is kept, since a far count would be a vast number (a count of 12 million, which one world reached, would be 264 million bits);
- the half turn is the same, 3,142 counts.

**Measured against the walked orbit:** the angles part by 1 / (8 Gamma^3) per count, about 3.93 x 10^-7 of X at the half turn: 113,214 notches at the declared X, and 5,955,983,441,205 at X = Gamma rim.

**Measured on the three charts, the circuit replaced by the power:**

| chart | the state hash at the end | the reading | what moves |
|---|---|---|---|
| hole, 60 ticks | 478aeb245a987204, the walked circuit's | same, line for line | the phase pairs of 2,135 chime frames; the rows' `orbit table` size at 14 rows |
| chiral, 60 ticks | 5f34155e2c2e1d6d, the walked circuit's | same, line for line | 2,781 frames' phase pairs; 14 rows' `orbit table` |
| bodies, 120 ticks | 32a4218e47ee05c2, the walked circuit's | same, line for line | 14,771 frames' phase pairs; 15 rows' `orbit table` |

The Node lines, the counts, the turns and the run back (20 of 20) are the same on all three (gauss_run.py), and the same again on the hole on 608d97134.

**What moves:**

- the frames' phase pairs, which record the points read, so the points differ by the angle;
- the rows' `orbit table` field, which reports the walked table's size, because that table is gone.

**The cost:** the power at count n is a number of about 22 n bits (69,000 at the half turn), so a read is one large division. Cached, it is a table again, but a table of exact points.

## 5. Which clauses become one

| clause | before | as a Gaussian hand | moves |
|---|---|---|---|
| the quarter turn J, the conjugation K | matrices on a train's lines | i and the conjugate (fold 1) | nothing |
| the sweep, the lead, the frame's read | bilinear forms | Im(conj(a) b) by meshes.cross (fold 1) | nothing |
| the mesh's turn | two tangent triples multiplied out | one square g^2 / \|g\|^2 (fold 2) | nothing |
| the rest and moving lays | (base C, sense base S) over rim, per line | z_before = z_now (pinion + i sense s) / rim, one product, a signed carry per gear | nothing |
| the axis pairs | the point composed one mesh at a time | the point's powers, one odd rounding per part per mesh | nothing (it is so already) |
| the cycle lay's quarter digits | a table of four pairs | i^q | nothing |
| the wind | per gear | (3 / 2 rim)(\|rim z_before - rho z_now\|^2 + \|rim z_before - conj(rho) z_now\|^2) at the vacuum, uniform | nothing (it is an identity, DAVID-AMPLITUDES.md) |

**Rule3 itself does not shorten:** it is one real line, the same on each part. What shortens is everything around it that reads a hand.

## 6. What it explains

- **The mass in gears.** rim - pinion = |rho - rim|^2 / (2 rim): the squared chord between the rest turn rho and no turn rim. The spring is D = SPOKES p_0^2 G^2 |rho - rim|^2 / rim.
- **The light.** pinion = rim and s = 0: no chord, so no spring, and a hand at rest sweeps nothing. Its quantum is the one-clock bound SPOKES rim e (DAVID-AMPLITUDES.md section 5).
- **The wind.** It is the mean of two norms, at least SPOKES s |W| uniform and SPOKES rim |W| at one clock. The sweep is the count (DAVID-AMPLITUDES.md).
- **The twin hands are one quaternion.** On the four gears (three_up, twelve_up, three_down, twelve_down), q = z_up + z_down j. The twin build's Pauli gearing gives the half turns' lifts U_a = -i sigma_a as right multiplications by units of Q8, in whole numbers [measured on every gear set in [-2, 2]^4]:

  | lift | right multiplication by |
  |---|---|
  | U_x | -k |
  | U_y | j |
  | U_z | -i |

  - The hand's own rest turn is the left multiplication by a complex ratio, the same on each twin, so the spin and the phase commute.
  - Kramers' T = (i sigma_y) K is the conjugation of both twins followed by the right multiplication by -j, and T T = -1.
- **The 4 pi.** A full turn of the twins' axis is the right multiplication by -1, and two full turns by +1. On the great clock this is the measured overlap cos(theta / 2) (DAVID-SPIN-IN-CLOCKS.md section 3).

## 7. The cost, and the order

1. **Folds 1 to 4:** built and verified. The source is 56 lines shorter (64 added, 120 struck) and every chart is bit for bit.
2. **The cycle lay's quarter digits as i^q:** a fold of four lines.
3. **The circuit as the exact Gaussian power.** features/standard reads the pair at a count as X zeta^n div (4 Gamma^2 + 1)^n:
   - the half turn is the first count where its cosine stops falling (3,142), and the mirror beyond it is kept;
   - the walk, the table and the orbit's drift are struck;
   - the frames' phase pairs and the rows' `orbit table` field are regenerated.

   **For the owner's word:** the law's one angle per count becomes the gear's, 2 atan(1 / (2 Gamma)), in place of the walk's arccos(1 - 1 / (2 Gamma^2)). They part by 1 / (8 Gamma^3) per count, and no state integer, event or reading of the three charts moves. The power of a Gaussian gear is the gear meshed n times, an act and not a typed cosine.
4. **Not built:** one division per hand in the wind (section 3).

A document and its checks; no engine file changed.
