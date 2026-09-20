# The masses and the charges in the Beam Law: is the ladder derivable? (read-only, the mathematician, 2026-09-20)

Base: `05b49279` (the branch `claude/universe24-new-3ytqde` at the start
of this session, the day's records 1 to 99 read). Nothing under `src/` was
edited and nothing is registered: this design answers the model owner's
question of 2026-09-20, "what about completing the families: predicting the
masses and charges in nature, the particles?" and "what about the
mathematician on the masses?", on the law as it stands. Its evidence is
beside it: `ladder.py` with its output `ladder.out` (standalone integer
arithmetic; the one thing imported from the engine is the collision
table's own class function), `cavity_read.py` with `cavity.out` (the
readings of two engine runs, the worlds in
[`examples/events/masses/`](../../../examples/events/masses/README.md)).
Every integer below is from those outputs unless marked "stated". The law
read is [BEAM_LAW](../../BEAM_LAW.md) with its notes 30 to 36, the engine's
`nature_beam.py`, `engine.py`, `measured.py`, `world.py` and
`core/integer.py`, the [catalog](../../ENTITY_CATALOG.md), [hypothesis 12](../../HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding),
the record "the constants: what is derived and what is an input"
([Highlights 5.5](../../HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)),
[DERIVATIONS section 12](../../DERIVATIONS.md#12-the-ladder-of-masses) (the
ladder under the superseded loop law), series I, H and J of the register
and the log of the day.

The verdict in one line: **not derivable in this law.** Content and charge
are declared keys and no rule of the Beam Law reads a content back into
itself in a way that selects it; the ladder of hypothesis 12 belonged to a
law (rays circulating on a ring under a binding table) that the Beam Law
superseded on 2026-09-19, and the sentence "mass ratios are derivable" in
Highlights 5.5 is a statement about that law, not this one. Section 6 names
the smallest rule that would make a ladder and shows, with the numbers,
that the ladder it makes disagrees with nature.

---

## 1. What "a loop closes" means in the Beam Law

Hypothesis 12 defined a bound thing as a periodic orbit of the meeting rule
on a ring of Nodes (Highlights 3.4, 2026-09-17), the ladder as the set of
contents whose orbit closes, and A10 as the count of them. Under the Beam
Law there is no meeting table, no binding table and no ray that circulates:
a bound thing is a measured event (a body) with a declared `amount`, held
in place by pushes and the contact, and a ray is an event in transit on a
digital line. "A loop closes" therefore has exactly three readings in the
law as it stands, each a named rule with named integers:

| Reading | The rule | The integers it reads | What returns to itself |
| --- | --- | --- | --- |
| (a) a cycle of the collision table at one Node of free space | BEAM_LAW section 4: the class of a slot state (crowd mask, number of singles, their headings' sum) is invariant, the forward map the cyclic shift inside the class | the eight slot codes (0 empty, 1 single, 2 crowd) and nothing else | the slot pattern, with period 1, 2, 3, 4 or 6 (`ladder.out` A: 4429 fixed states, 933 classes of period 2, 52 of 3, 23 of 4, 3 of 6 over the 6561 states); the amount enters only as "single or crowd", the content never |
| (b) a ray that comes home | section 3 step 4: an arrival of the reader's own number is home, created again on the reader's `directions` at its next self-creation; what came home is the same in and out (note 18); a paid ray's label joins the momentum at the home and leaves at the re-creation | the ray's number against the reader's; the amount and content apportioned whole over the directions | the ray's amount, content per unit and phase, exactly, for every amount and every content: a bijection with no condition on the content |
| (c) the closure of a body's phase on its orbit (`bohr-v1`) | note 30 (ii): at every Link stepped the body's phase turns by `by_clock(k0, \|p\| N, h)`; over a closed orbit of the GameBoard the turn is (N / h) x the sum of \|p_axis\| over the Links, 4 p r on a circle | the momentum label p, the world's `action` h, the Links stepped k | the phase, when 4 p r = j h: a condition on the momentum and the radius of a body of GIVEN content, never on the content |

The pushes, the columns, the lifetime and the contact (notes 31 and 34) bind
bodies at one Link and hold them there (series I: the deuteron at one Link
never steps in 3000 intervals); none of them reads a content into a
condition. A body of content 1836 and one of content 1837 are held the
same way, the push proportional to the reader's content (the equivalence
principle, step 5) and the contact handing a momentum component whatever
the content. The contents of series I (1836, 1839, the unit of `nuclear`)
are declared.

## 2. A fixed point of content, defined

Let the state of a measured event A be (M_A, age_A, phase_A, p_A, the
`held` vector), and let F be the interval map of the law on the whole
GameBoard. A **fixed point of content** is a configuration whose contents
and clocks reproduce themselves: a period T at which every measured
event's `held` is what it was, its clock has advanced T self-creations,
and what is in transit is what was in transit (the phases modulo N and the
momenta apart, which are the orbit's, not the mass's). The ladder of
hypothesis 12 is the set of contents at which such a fixed point exists
and off which the configuration does not reproduce itself (disperses,
drains or grows).

What can change a measured event's content in the Beam Law, the whole
list (BEAM_LAW steps 4 and 5, note 36 (iii)):

1. a click of a paid ray: `held[family] += amount x content` of the row
   (the content joins; a free ray carries no content and joins nothing);
2. a lamp's release: at a self-creation whose turn is s = `by_clock(age,
   M, K)` (the clock's rate [1, K], note 33), each direction releases
   `min(by_clock(age, rate_n, rate_d), held // (h s))` units of content
   h x s, so the cost per self-creation is the rate times h s per
   direction, that is h x rate x M / K per direction on average;
3. a transformation `become`: the declared products' content leaves, the
   remainder moves to the new family; the total is exact and the amounts
   are declared;
4. a home or a re-release: in and out the same.

Nothing else touches `held`. The pushes, the columns, the contact, the
meeting, the collision and the flight never read or write a content into a
content; the lifetime removes rays, not held content. A free family's
measured event (matter: the electron, the proton, the neutron of the
catalog) has no lamp and clicks only paid rays: its content is its
declared `amount` plus whatever light it absorbs, and nothing ever leaves
it but a `become`. So a free body of ANY content is a fixed point of
content at every period, trivially: the map is the identity on it.

The one non-trivial dynamics is 1 with 2, the exchange of light, and it is
**linear in the content**: the cost per unit is the turn, M / K per
self-creation to the floor, and the click returns exactly what was paid.
`ladder.out` C iterates the exact integer map for two lamps of one paid
family facing each other seven Links apart (K 4096, N 64, the flight age
12 intervals), and the engine's run of the same world reproduces it
integer by integer at 600 intervals ((29634, 11209) both):

| Start | After 6000 intervals (the map; the engine at 6000 the same, `cavity.out`) | Read |
| --- | --- | --- |
| (32768, 8192) | (20806, 20035), on the lamps 40841 + 119 in transit = 40960, the books balanced at every tick | the difference relaxes as (1 - 2 / K) per interval, time constant K / 2 = 2048 |
| (20480, 20480) | (20420, 20420) from the flight time on (the engine at 600: the same) | a fixed point: 120 units of content in transit, twelve intervals x five each way |
| every total T tried (2, 64, 4096, 8192, 40960, 65536, 2^18, 2^20 + 6) | the equal split of T is fixed (less the transit) | one fixed point per total, every integer total within the bounds |

So the set of fixed points of the exchange is a **continuum**: one per
total, and the total is a declared number. There is no rung. The detector
reading of the same fact (`cavity.out`): the content per click at each
reader is the partner's turn at the unit's birth (E = h f read at the
receiver), 8 and 2 at the start of the unequal world, 5 and 5 at its end,
5 throughout the equal one; nothing in the record singles out 5, or any
other turn.

## 3. Does the law select contents? The bounds, and what is not a rung

The only constraints the law puts on a content M are bounds (`ladder.out`
B): M is an integer from 1; the frame refuses a turn of half the circle or
more, so M <= K (N / 2 - 1) (32 505 856 at the register's K = 2^20, N = 64);
the label's product Q x M x amount must fit 2^62 - 1; and a lamp's cost
h x s must be covered. Every integer between the bounds is admitted and
behaves as its neighbour does. The floor of `by_clock` makes the turn of
M and of M + 1 differ at some ages and not at others, a grain of 1 / K,
never a rung: two contents differing by one release the same units at
almost every self-creation and one more at one age in K.

Three things that look like selection and are not:

- **The window's stride** (note 36 (i)). A reader's window admits the
  fraction w / N of a source's rays when the source's stride s over the
  circle is coprime to N, and g x (the residues inside the arc) / N when
  gcd(s, N) = g; a source whose turn is exactly N / 2 puts its phase on
  two values and is admitted wholly or not at all by a narrow window. That
  is arithmetic of the circle, present for any content whose turn shares
  a factor with N, a comb of admittance in s = M / K and not a stable
  point of M: a content off the comb is not moved toward it, its rays
  are admitted or pass, and its held content is untouched by a pass. The
  window's setting is a declared constant of the entry (or, under note
  34, a reading of another set), never the reader's own clock phase; so
  no reader ever compares an arriving phase with its own present.
- **The wave threshold** (note 32) reads the pointer's square of one
  interval's arrivals and admits or passes a set; it reads amplitudes
  and phases, never a content.
- **The click's ladder of `amplitude-v1`** (record 86: "the ladder read at
  the record's completion, normalised by the sum of its offers, the rungs
  at the nearest integer") is a ladder of offers of one record at a click,
  the choice of one row; it does not touch any measured event's content.

Therefore: **content is free in the Beam Law.** The answer to "does the
law as it stands have a mechanism that selects contents, so that a ladder
exists" is no, and the answer is exact, not numerical: the map is the
identity on a free body's content and linear on a paid exchange, and a
linear conserving map has no isolated fixed point.

## 4. Charge: what quantises it, and what fixes 1, -1 and the thirds

The rules that touch a charge, the whole list:

| Rule | What it says | What it quantises |
| --- | --- | --- |
| the family key `charge` on a free family (note 28) | rho, an integer or a pair [n, d], d >= 1; refused only for d = 0 or a part that is not an integer | nothing: every rational is a lawful rho, 2/3 and -1/3 as much as 1 and -15 |
| the charge of a measured event (D-1, note 31 (i)) | the exact rational sum over the families it holds of rho x content | nothing: a rational times an integer |
| the push (note 31) | one product per column, sign(V E n) x by_clock(age, \|V E n\|, D d), floored on its own | nothing: rho enters as a product with the partner's rho; no feedback on rho |
| a paid family's `charge` (D-1, note 36 (ii)) | a whole integer c per unit of amount, read on the books' charge line only; a fraction refused | **the one quantisation in the law**: a unit of amount is whole, so its charge is whole; it follows from the wholeness of the amount, not from a rule about charge |
| `become` (note 36 (iii)) | the parser refuses a transformation whose charges do not balance | conservation, not quantisation: the charge line is the same pair before and after |
| the columns beyond `charge` | the same pair form with a sign | nothing |

So nothing in the law fixes 1, -1 or the thirds: they are declared values
of the pair form, and the pair form admits every rational. Three facts of
nature that a referee will name at once, and what the law says of each:

1. **|q_e| = |q_p| to one part in 10^21** (the neutrality of matter). In the
   law the electron's charge is rho_e x M_e and the proton's rho_p x M_p;
   with M_p / M_e = 1836 the equality needs rho_e = -1836 rho_p exactly (the
   catalog's electron declares -15 against the proton's [1, 1] with both
   contents 1836 in series H, a scale chosen for the run). Two declared
   rationals; no rule ties them. The muon and the tau of the catalog
   declare [n_e, 207 d_e] and [n_e, 3477 d_e]: the same equality declared
   twice more, to the grain of the pair.
2. **Every charge a multiple of e / 3, and every free particle's a multiple
   of e.** Not in the law: nothing forbids a family of rho = 1/7. What the
   law has, exactly as nature has, is that a composite's charge is the sum
   over what it holds (2/3 + 2/3 - 1/3 = 1, catalog): conservation and
   addition, present in every theory with a charge.
3. **The neutron's charge 0 after beta decay** (series J): the products'
   charges balance because the parser refuses a `become` that does not
   balance. A conservation law, declared.

The smallest rule that would quantise charge (not asked for; named as the
catalog's gap list names keys): rho a whole number (the pair form dropped
on free families) with the unit of charge e / 3, so that the down quark is
-1, the up 2, the electron -3 and the proton, as three quarks held, 2 + 2
- 1 = 3. That rule forbids non-multiples; it derives no value, and it
leaves fact 1 exactly where it is (the electron's -3 and the proton's 3
are still two declarations; in physics the equality is not derived either
below a grand unification). The catalog's leptons of a fractional rho per
unit of content (the muon at [n_e, 207 d_e]) would then have to be held
composites: one charged unit held with 206 neutral ones, which the law's
`held` key already expresses.

## 5. The computation against nature: what comes out, what does not

Since no mechanism exists, "compute the ladder in integers" has no ladder
to compute; what `ladder.py` computes instead is (i) the proof by
enumeration and iteration above (A to C), (ii) what the law does say about
the masses it holds, against nature (F), (iii) A10's representability test
as the register wrote it (D), and (iv) the ladder the smallest rule would
give, against nature's spectrum (E, section 6). The numbers (CODATA 2018,
PDG 2022, the uncertainties as published):

| Quantity | Nature | The law | Verdict |
| --- | --- | --- | --- |
| m_p / m_e | 1836.15267343(11) | an input: the catalog's 1836 (and 1 for the electron); series H declares both 1836 | not derived |
| m_n / m_p | 1.00137841931(49) | an input: the register's 1839 / 1836 = 1.0016340, off by 2.6 x 10^-4 even as an input (rounded) | not derived |
| m_mu / m_e | 206.7682830(46) | an input: the catalog's 207 | not derived |
| m_tau / m_e | 3477.23(23) | an input: the catalog's 3477 | not derived |
| m_pi+ / m_e, m_pi0 / m_e | 273.1324(4), 264.1430(10) | nothing: no meson, no quark, no bound loop of a quark and an antiquark exists in the law (the "loop closes" of hypothesis 13 and E7 is the superseded law's) | absent |
| m_d / m_e (the deuteron) | 3670.48296788(13) | m_p + m_n exactly = 3674.83634 (a free ray carries no content: no mass defect, series I) | **the law predicts, and is off by 4.353 m_e = 2.225 MeV, 0.119 %** |
| m_alpha / m_e | 7294.29954142(24) | 2 m_p + 2 m_n = 7349.67267 | **predicts, off by 55.373 m_e = 28.296 MeV, 0.759 %** |
| the ratios of electric to gravity (ee : ep : pp) | 1836^2 : 1836 : 1 (with equal and opposite charges) | the same, from the form M_A (rho_A rho_B - 1) V_B (record 11) | an identity of the form, as the orchestrator said: Coulomb and Newton give it too |

Two lines come out of the law, and both are wrong in nature's direction:
the binding energy is absent, so every composite is heavier than nature's
by its mass defect (0.12 % for the deuteron, 0.76 % for the alpha, the
whole of nuclear binding). The catalog's gap list says so ("mass defect,
binding energy: not in design"); this design puts the numbers beside it.
The one reading of a binding energy the law has, the clock's count under a
suspension (series I's I7, cut), is a rate, not a content: it would show a
bound clock slower, not a bound pair lighter.

**A10's representability** (`ladder.out` D): the smallest electron rung k
at which k x (m_mu / m_e) and k x (m_p / m_e) are both within their
published uncertainties of an integer is k = 13 840 (the muon at 2 861 673,
the proton at 25 412 353); with the neutron added k = 18 104, the tau
adds nothing (its uncertainty exceeds a rung from k = 3 on), the two pions
fit at 13 840 as well; and 989 567 of the k below 3 000 000 fit the muon
and the proton together. That is the arithmetic of a fine grid: it carries
any set of ratios once the grid is finer than their uncertainties, and it
predicts nothing unless a rule fixes k. The law fixes no k. A10 therefore
stays what the register says, planned under a law that no longer exists;
this design recommends that it be marked so, when the owner decides.

## 6. The smallest rule that would make a ladder, and what that ladder says

A ladder needs a rule that reads a content back into the survival of that
content, non-linearly. The physicist's report on hydrogen named it on
2026-09-20 ("Bohr's radii would need ... a closure reading against its own
past, for which the law has no place, a law change"), and the smallest
form of it in the law's vocabulary is one key value: **a window whose
setting is the reader's own clock phase** (say `phase_window: "clock"` on
a table entry, in place of a declared step; every other rule untouched).
Under it a body of content M whose own light returns to it after tau
intervals (a mirror's `rerelease` around it, the returning row carrying
the mirror's number so that the body reads it) re-absorbs the unit iff the
phase the unit carries, its birth phase plus 2 l x `phase_per_link`, is
within w of the body's present phase, that is iff

    (2 l x phase_per_link - tau x M / K) mod N is inside the window (to the floor of by_clock),

so the contents that keep their light are bands of width w K / tau spaced
**K N / tau** apart (8 388 608 / 3 at the register's K = 2^20, N = 64 and a
round trip of 24 intervals; `ladder.out` E). A content off a band pays
h x s per unit and gets nothing back: it drains at M / K per self-creation
until it enters a band from above, so the upper edges of the bands are
attractors. That is a ladder, and it is the clock's resonance with the
cavity, E = h f closing on the round trip: exactly hypothesis 12's
"loop-closing content" in the Beam Law's vocabulary.

What that ladder says against nature (`ladder.out` E): it is **harmonic**,
equally spaced in M, m_j = a (j + c) for two constants a and c (the
spacing and the window's offset). Three masses then fix the ratio
(m_p - m_e) / (m_mu - m_e) = 8.918540052(20) as a ratio of two whole numbers
of rungs, p / q, within the published uncertainty; the smallest is
27 371 / 3 069. So the electron, the muon and the proton on one harmonic
ladder put the muon 3 069 rungs above the electron, with **3 068 charged
leptons between them that nature does not show** (the next after the muon
is the tau, at 3477). A ladder of one cavity per particle (tau chosen per
family) fits anything and predicts nothing. Either way the rule does not
give nature's spectrum; it gives a spectrum, which is more than the law has,
and the wrong one.

What a rule with a chance would have to do, stated so that it is not read
as a proposal: make the spacing grow with the rung (a geometric or
power-law ladder, as the three charged leptons roughly are: 1 : 207 :
3477), which no resonance of one clock with one flight time does; the
content would have to enter the flight time or the rate itself. The law
has no such term, and this design does not invent one.

## 7. The verdict, as a referee would state it

1. **The mass ratios are not derivable in the Beam Law.** Every content is a
   declared `amount`; the only content dynamics (the exchange of light) is
   linear and conserving, with one fixed point per total; the collision
   table is content-blind; the phase closure of `bohr-v1` selects radii,
   not contents. The claim in Highlights 5.5 that "mass ratios are
   derivable" refers to the loop law of 2026-09-17 and should be read as
   superseded with it; DERIVATIONS section 12 had already found, under that
   law's Port form, "no ladder, mass free", and under its Born form every
   even content. The two contents the law does predict (the deuteron's, the
   alpha's) are the sums, above nature by the missing binding energy.
2. **The charges are not derivable either, and not quantised.** rho is any
   rational; the one whole charge in the law (a paid unit's) is whole
   because the amount is; the equality of the electron's and the proton's
   charge is two declarations. The thirds are ordinary values, allowed and
   not explained.
3. **"Derivable with one named rule" does not hold for the smallest rule.**
   A self-referential window makes a harmonic ladder, and a harmonic ladder
   that carries e, mu and p has 3 068 unseen leptons. No single key of the
   law's kind gives a geometric spectrum.
4. What a referee would add: a model whose masses and charges are all
   inputs is not thereby wrong; it is where the Standard Model is on the
   same questions (nineteen parameters, the Yukawa couplings among them,
   charge quantisation assumed). The claim to avoid is the one Highlights
   5.5 still carries. The catalog's gap list already says "the Higgs and
   mass generation: not in design"; this design agrees and adds that no
   rule of the present kind (a key on a family, a table entry, a column)
   can close the gap, because every such rule acts per unit of content and
   is therefore linear in it.

Nothing here is registered; the owner decides whether the sentence in
Highlights 5.5 is amended, whether A10 is marked as belonging to the
superseded law, and whether the numbers of section 5 (the mass defects as
the law's own predictions against nature) go to PREDICTIONS.md.

## 8. How to reproduce

```bash
PYTHONPATH=src python docs/designs/masses/ladder.py            # < 1 s; the output is ladder.out
PYTHONPATH=src python -m event_universe --init examples/events/masses/cavity_unequal.json --output runs/masses/cavity_unequal
PYTHONPATH=src python -m event_universe --init examples/events/masses/cavity_equal.json --output runs/masses/cavity_equal
PYTHONPATH=src python docs/designs/masses/cavity_read.py runs/masses      # the output is cavity.out
```

Environment of 2026-09-20: Python 3.14.7, numpy 2.5.3, headless; the two
runs took 6 s and 1 s; source fingerprint `b4d074f2b762e58d...` (the
branch at `05b49279`).
