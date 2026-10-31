# Koide's 2/3 on whole counts: never on the diagonal spring, often with a T2 part

David, 2026-10-30, 15:xx UTC, for the architecture document's families (the Algebra line: "Koide's 2/3 is a test,
David's (board2mass 7.2; OPEN ...)"), on Sofer's statuses (6523641446, item 3: its probe m2 left the tree on the owner's
word, so the line stands as OPEN until a whole-number probe and a new pair of readers stand) and the owner's word of
11:1x UTC (everything to stand with a hostile mathematician and a hostile physicist). It rebuilds board2mass 7.2's
checks in whole numbers alone, in the law's four layers (Postulate 4, item (10)). The probe was
derive/david_open/node/koide_whole.py, its output koide_whole.txt beside it, about 1 s.

**Its probe left the tree** (2026-10-31, 02:1x UTC; its record stays in git at toys-5 c8c8adbba). The owner's law
bars a root in the code and a root by search, and Sofer's gate now reads a search over a range for a value of a form:
the probe took whole square roots by Newton's steps (its root(), in (d) and (f)) and counted whole solutions of forms
by running over ranges ((b), (d) and (e)). The page's numbers below are that record's, read once, until a probe with no
root and no search stands; the parity argument of (c), the Eisenstein norm's even power of 2, needs neither. The
page is paused with its line (OPEN).

**The finding in one line:** read as the roots of three masses, a held spring's three values on the diagonal (an A1
part and an E part) never give Koide's ratio 2/3 with whole counts, since 2 / 3 asks an Eisenstein norm to carry an odd
power of 2, which no norm does; they approach it from below by steps of 1 / (9 n0^2) and never from above; with a T2
part the ratio meets 2/3 exactly often. Nature's charged leptons give 0.6666645 +- 0.0000051, which tells neither case
apart: the ratio is a test of the spring's form, not a result.

## 1. In clocks

- **Three masses from one spring.** A family of three rows hung on a held count with parts beats in three ways, one
  for each of the spring's own values; the three beats are the three masses (board2mass, section 7). Reading the
  spring's values as the roots of the masses makes Koide's ratio a statement about the spring's three values alone.
- **On the diagonal** (an A1 part n0 and an E part, no shears) the three values sum to three times n0, and how far they
  spread is the E part's size: the ratio is 1/3 plus that spread over 9 n0^2. Koide's 2/3 asks the spread to be exactly
  three halves of n0 squared, and whole counts never give that.
- **With shears** (a T2 part) the spread gains the shears' size, and whole counts meet 2/3 often.

## 2. In the algebra

- **The identity** (DERIVED; CHECKED, probe (a)). With s = (n0 + e1, n0 - e1 + e2, n0 - e2), sum s = 3 n0 and
  sum s^2 = 3 n0^2 + 2 N, N = e1^2 - e1 e2 + e2^2. So Q = sum s^2 / (sum s)^2 = 1/3 + 2 N / (9 n0^2), and Q = 2/3
  reads 2 N = 3 n0^2.
- **No whole solution on the diagonal** (DERIVED; CHECKED, probes (b), (c)). N is the norm of e1 + e2 w in the
  Eisenstein integers, w a cube root of 1. The prime 2 stays prime there (x^2 + x + 1 has no root mod 2), so a nonzero
  norm is 4^j times an odd number: its power of 2 is even. 2 N = 3 n0^2 needs n0 even, and then N = 6 (n0 / 2)^2,
  whose power of 2 is odd. So both sides are 0: no three values above 0. The same holds for rational strengths, by
  clearing the denominators.
- **The nearest approaches** (DERIVED; CHECKED, probe (d)). The least step is 1 / (9 n0^2). From below,
  3 n0^2 - 2 N = 1 needs n0 odd and N = (3 n0^2 - 1) / 2, which norms meet. From above, 2 N - 3 n0^2 = 1 is impossible:
  for an odd n0 it needs N = 2 mod 4, a power of 2 that is odd; for an even n0 an odd 2 N.
- **With a T2 part** (DERIVED; CHECKED, probe (e)). The spring is the symmetric matrix S with that diagonal and the
  shears t off it, its eigenvalues the roots; tr S = 3 n0 and tr S^2 = 3 n0^2 + 2 N + 2 |t|^2, so 2/3 reads
  2 (N + |t|^2) = 3 n0^2, which whole counts meet often: the shears' size carries the odd power of 2 that the norm
  cannot.
- **What the test can tell.** Any three positive values fit a + B cos(phi + 2 pi k / 3) (board2mass 6.5), so the form
  alone predicts nothing; Koide's exact 2/3 asks for a spring with shears, or for a spring off whole counts.

## 3. On the board (koide_whole.txt)

- **The identity** (probe (a)): holds on all 111,630 whole (n0, e1, e2) with 1 <= n0 <= 30 and |e1|, |e2| <= 30.
- **No solution** (probe (b)): no whole (n0, e1, e2) with 1 <= n0 <= 60 and |e1|, |e2| <= 60 has 2 N = 3 n0^2.
- **The norms' parity** (probe (c)): of the 361,200 nonzero norms with |e1|, |e2| <= 300, none has an odd power of 2.
- **The approaches** (probe (d)): for n0 up to 400, 3 n0^2 - 2 N = 1 with three values above 0 at 72 values of n0, 492
  triples in all; at n0 = 389, E (-361, 179) gives the values 28, 929 and 210; none from above.
- **With a T2 part** (probe (e)): at n0 = 4, 336 whole (e1, e2, t) give a positive spring with three distinct values
  and Q = 2/3 exactly; one is E (-3, -5) with T2 (-2, 0, 1), the spring [[1, 1, 0], [1, 2, -2], [0, -2, 9]].

## 4. In the clicks

- **Nature's ratio** (probe (f)): the charged leptons' masses (PDG 2024, S. Navas and others, Phys. Rev. D 110,
  030001 (2024): m_e = 0.51099895000 MeV, m_mu = 105.6583755 MeV, m_tau = 1776.93 +- 0.09 MeV) give
  Q = 0.666664463, and 0.666659382 to 0.666669544 across m_tau's spread: 2/3 lies within it.
- **What it tells.** A diagonal spring of whole counts reads Q below 2/3 by at least 1 / (9 n0^2), which falls inside
  nature's spread of 5.1 x 10^-6 once n0 passes 148; so nature's figure cannot tell the diagonal spring of a large n0
  from an exact 2/3, nor either from a spring with shears. The test is a test of the spring's form, read once the
  spring's values are derived; the masses are read in the clicks only as beats (term 6, G3), and the roots-as-values
  reading is board2mass's assumption, named.
- **Departures, named:** none claimed; the line is a test, not a prediction.

## 5. What stands (for the families' Algebra line, when its readers agree)

- "Koide's 2/3 is a test, David's (DAVID-TENSOR24-KOIDE-WHOLE.md, with board2mass 7.2): never met on the diagonal A1 + E
  spring with whole counts (an Eisenstein norm's power of 2 is even), approached only from below by 1 / (9 n0^2), met
  often with a T2 part; nature's 0.6666645 +- 0.0000051 tells neither apart." **Status:** DERIVED and CHECKED in whole
  numbers; DRAFTED until its two readers pass it.

## 6. OPEN

- **The spring's values themselves**, derived and not chosen: the held count's own potential (G3, OPEN (2)).
- **The reading of the masses' roots as the spring's values** against the beats the clicks read (board2mass 7.2's
  assumption).
- **The quarks' sectors**, with their running masses.
