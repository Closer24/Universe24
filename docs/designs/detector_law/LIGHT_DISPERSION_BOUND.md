# Light against itself: the GameBoard's own dispersion of light, its anisotropy on the sky, and the bound it puts on the one scale (row A2; the chief physicist, 2026-09-23, on the model owner's word "now, not in the morning"; docs and one computation, no run)

The model owner's question of 2026-09-23, about 23:40Z (Hebrew, in
substance): "c itself as a ratio to another speed?" This page is the second
such ratio. The first is row A: the massive kind's cone against light's,
a function of the mass, a BOUND on the one scale from nature's bound on a
subluminal electron. This one is light against light: on the GameBoard a
short wave of light runs slower than a long one, by an amount the rule
fixes with no declaration, and nature has measured that ratio in the
photons of gamma-ray bursts. Every number is labelled; the published bound
was RECALLED until the Source Verifier confirmed it (SOURCES_VERIFIED.md,
2026-09-24: E_QG2 = 1.3 x 10^11 GeV VERIFIED, Vasileiou and others 2013;
the parametrisation's factor 3 / 2 in section 3 NOT FOUND by him, so it is
this page's own reading of the published form: without it the Link and
the interval below are smaller by sqrt(2 / 3) = 0.82, the same order).

## 1. The derivation (COMPUTATION, `light_dispersion_bound.py`)

Light's kind is the pair [1, 1], so a plane wave obeys 2 cos omega = S_6 / 3
with S_6 = 2 SUM_i cos k_i. Along a unit direction **n** with |**k**| = k:

    cos omega = (1 / 3) SUM_i cos(k n_i)
    omega = (k / sqrt 3) (1 - (3 SUM_i n_i^4 - 1) k^2 / 72 + O(k^4))
    v_g / c = 1 - (3 SUM_i n_i^4 - 1) k^2 / 24 + O(k^4),   c = 1 / sqrt 3 Link per interval.

The script checks the series against the exact group pace: on an axis at
k = 0.3 the exact 0.992472 against the series' 0.992500; on the body
diagonal the quadratic term is exactly zero (the exact pace 1.000000 to six
places at k = 0.6). The coefficient 3 SUM n_i^4 - 1 runs from 0 on a body
diagonal, through 1 / 2 on a face diagonal, to 2 on an axis, and averages
4 / 5 over the sphere (the script's sample 0.7992). Nothing is declared:
the pair [1, 1], the six reads and the three axes give the number.

## 2. The prediction of the form (P, said before any measurement is read)

The quadratic dispersion of light is ANISOTROPIC on the sky with a cubic
pattern: zero along the GameBoard's body diagonals, largest along its axes,
the coefficient (3 SUM n_i^4 - 1) in [0, 2]. Direction-dependent
coefficients exist elsewhere (the standard-model extension's photon
sector at mass dimension 6 carries them up to j = 4, with FREE
coefficients); what is the GameBoard's own is the FIXED shape with no
free coefficient: 2 on an axis, 1 / 2 on a face diagonal, 0 on a body
diagonal, the average 4 / 5. Its falsifier: a set of bursts in
different directions whose dispersion coefficients, once nature's
sensitivity reaches the effect, do not fit one cubic pattern on the sky.
Nature today has bounds, not a measured coefficient, so this is a
prediction of the form with no number to compare yet.

## 3. The bound on the one scale (BOUND; the published number RECALLED)

Nature parametrises a quadratic photon dispersion as v / c = 1 - s (3 / 2)
(E / E_QG2)^2, s = +1 for the subluminal side, which is the GameBoard's
sign (a short wave is slower). With k = E a / (hbar c), a the Link:

    a <= (hbar c / E_QG2) sqrt(36 / (3 SUM n^4 - 1)),   tau = a / (sqrt 3 c_nature),

the interval from the Link through the GameBoard's own c = 1 / sqrt 3 Link
per interval (light covers one Link in sqrt 3 intervals; Reviewer 3's line
of 23:32Z: row A's number is a time from a time and carries no such
factor). hbar c = 1.973 x 10^-16 GeV m, c_nature and the Planck length and
time are CONVERSION, as in the script.

VERIFIED by the Source Verifier (Vasileiou and others 2013; RECALLED when
first written): the Fermi gamma-ray-burst bound on the subluminal quadratic term,
E_QG2 of order 1.3 x 10^11 GeV (GRB 090510, the Fermi LAT analysis of
2013). With that input the script prints: on an axis the Link a <= 6.4 x
10^-27 m and one interval tau <= 1.2 x 10^-35 s (2.3 x 10^8 Planck
times); for the sphere average 1.0 x 10^-26 m and 2.0 x 10^-35 s; on a
face diagonal 1.3 x 10^-26 m and 2.5 x 10^-35 s. Along a body diagonal the quadratic term vanishes and the
bound does not apply; several bursts in different directions close that
gap. The bound is a factor of about 1.8 x 10^7 tighter than row A's two-pace
bound (3.6 x 10^-28 s) and about 2 x 10^8 above the Planck time (5.4 x
10^-44 s), which it does not reach. The published number, its side and its
burst are the Source Verifier's to confirm; the script takes E_QG2 as its
input so the bound follows the confirmed value without a change of text.

## 4. What this is and is not

- It is a derived, dimensionless ratio (a pace over a pace) with no
  declared input, read against a published bound: row A2, a BOUND row
  beside row A, no run needed (the dispersion is the rule's own
  COMPUTATION, its band; row 5a's pace by wavelength is the reading that
  checks it). Row 5a's 0.8, 0.4 and 0.2 percent at 12, 16 and 24 Links
  are the same coefficient on the PHASE pace (k^2 / 72 along an axis),
  consistent with the group pace's k^2 / 24 at the same k; the two are not
  one number.
- It is not a derivation of c, hbar or G: those are the three unit
  conversions and no theory computes them. The one scale (the Link, the
  interval) is bounded here, not fixed.
- The isotropic part is what nature's bounds constrain today; the
  anisotropy is the prediction, and it is the same cubic pattern as row
  5a's anisotropy of c by direction, seen at short wavelength.
