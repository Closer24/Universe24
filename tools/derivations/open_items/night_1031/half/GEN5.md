# GEN5: Big Pic's turning frame for the parting term, on HALF2's train in the engine's terms

The Boss's deriver of the half-speed gear, 2026-10-31, 03:1x UTC, for a pair. Big Pic's own words:
#2187 6538128481 item 5, fetched by gh api into bigpic_6538128481.txt in this folder. They say: "Turn the 2' and 2''
pair in its own plane by theta each round, now and before slots alike". "The plane is the axes' x + y + z = 0 ...
where omega's turn W is a whole matrix and J = 2 W + I generates its turns (J^2 = -3)". The turn "factors into three
shears ... each one Rule3 carry with its tooth kept". "theta is the held hand's charge sigma times a strength". "The
plane's turn is A2 too (a quarter turn reverses it), so their product lands on A1 and the 24 keep it". "So it is
lawful in form, and OPEN until a deriver shows it with its 24, its run back and its books".

GEN4 is kept frozen. The probe is probe_gen5.py, with probe_gen5.txt and probe_gen5_run2.txt, byte-identical. It
runs with scratchpad/live/.venv/bin/python -I and reuses probe_half2, probe_gen3 and probe_gen4. It keeps the same
rules: whole numbers, Rule3's carry the one division, no root, Z[w] as exact pairs. The turn is Cayley's at t = 1/4:
c = 13/19, s = 8/19, c^2 + 3 s^2 = 1. In board words, the held hand's winding sigma (Big Pic's "charge") and the
class difference Q.

## 1. The act on HALF2's 24-gear train: where 2' and 2'' are, and the plane (DERIVED, MEASURED)

- **No gear carries 2' or 2''.** 2' + 2'' is the image of the whole projector Pi_c, rank 16, inside the train's 24
  gears. 2 is the image of Pi_2, rank 8 (GEN3 part 4). The act as built moves every gear by the per-gear leapfrog and
  carry. A spring kept by the 24 keeps both parts (GEN4 1.5).
- **The 24's own plane is the class difference Q, not the axes' plane.** Q is antisymmetric, a sum of the L(g), and
  Q Q = -Pi_c, so J_t = Q / 2 has J_t^2 = -3 on 2' + 2''. That is Big Pic's J, and it is 0 on 2.
  - The turn there is T = Pi_2 / 12 + c Pi_c / 12 + s J_t, whole over 456 (part C). It is orthogonal, kept by all 24,
    the identity on 2, and each r2 lift turns it back (T -> T^-1). That is "a quarter turn reverses it", in whole
    numbers.
- **Big Pic's plane is one hand's toy, and the 24 do not keep it on the train (MEASURED, part B).** His x + y + z = 0
  of the three axis rows is a whole lattice, W is w's turn, and J J = -3 there (part A).
  - Laid on the 8-gear train on the three axes as R_axes x I_8, the plane's turn is orthogonal and commutes with W.
  - But it is kept by only 6 of the 24 whole units: the lifts of w's three turns.
  - The half turns about the axes send the plane x + y + z = 0 to x - y - z = 0 and its kin, so the 24 do not keep the
    plane. "The 24 keep it" holds only for the 24's own plane, Q.

## 2. theta varies with sigma: the power road and the Cayley road (DERIVED)

- **The power road, R(s)^sigma, is refused on three counts.**
  - Its numerators grow as sigma log2 19 bits: 5, 44, 425 and 4,248 bits at sigma = 1, 10, 100 and 1,000 (part E).
    The width of 128 bits is passed by sigma near 30.
  - It is a loop over sigma, or over sigma's bits, in the act: refused (no loop in the act, line 35).
  - It is de Moivre: R^sigma makes cos(sigma theta0) and sin(sigma theta0) by construction, so it is refused by line
    102, which bans any construction that finds a cosine.
- **The Cayley road, with t = kappa sigma, finds no cosine.** The shear factors are -3 t and 2 t / (1 + 3 t^2),
  rational in sigma, one triple of carries a round, with no power and no angle taken in.
  - The parted rates are w0 + theta and w0 - theta with tan(theta / 2) = r3 kappa sigma. That is nonlinear in sigma,
    and about r3 kappa sigma twice for small kappa sigma.
  - The middle shear's divisor, the denominator of 1 + 3 t^2, is read from the state, as the split's dial 4 W is.
- **Is R(s) the K = 2 W kind of fake? No, on the Cayley road.**
  - K = 2 W aimed one angle, the quarter, by its choice of strength.
  - Here every rational kappa gives an exact turn, since each carried shear is a bijection by its tooth for every
    factor (part A). Exactness is needed for the run back, and no angle is aimed.
  - kappa is a CHOSEN strength like hold, tie and mesh.
- **Tonight's rule (a value is lawful only when it comes out of the families and their coupling) still refuses it.**
  - Q is a table of the 48: the half x half -> A2 antisymmetric channel, from the class sums.
  - But sigma pairs the held hand's now slot with its before slot. The families' coupling as laid reads value legs
    (the now slot) for every push, and the before slot only in the passing (term 11), which pushes nothing.
  - The frame turn is a new step of the act, with three new carries and three new teeth per plane pair. That is a law
    change, not a term of the act as built.

## 3. The shears' carries, each checked

- **The INDICATOR rule (BRIEF_PAIRS line 49): passed by form (DERIVED).** Each shear is
  alpha += carry(f_num beta, f_den, tooth), with f_den the strength's denominator or 1 + 3 t^2's. There is no
  carry(x, x x + 1, 0), no 1 div x, no 1 minus a quotient, and no bound carried by a bound.
- **The run back: exact as the act's own mirror (MEASURED on the toy plane).**
  - Three carried shears, teeth kept, are undone by the same three at -t: 20,000 of 20,000 whole points. The teeth go
    back by the carry's sign law, carry(-n, d, r') = (-q, r).
  - Under the act's mirror the slots swap, both get the same turn, and sigma flips (sigma = a_A1 b_A2 - a_A2 b_A1
    changes sign when a and b swap). So mirror o turn(sigma) o mirror = turn(-sigma) = turn(sigma)^-1 exactly.
  - The round must be a palindrome, turn o step o turn (DERIVED), because the step's per-gear rounding does not commute
    with a turn that is not a signed permutation.
  - sigma must be read where the mirror reads it. The held hand's winding is kept exactly while it turns at its
    quarter mode, so reading it before or after the step agrees there. Elsewhere this is OPEN.
- **The 24: no carried form keeps them for the uniform turn (DERIVED, MEASURED, part D).**
  - A shear kept by the 24 commutes with every L(g), so with Q: it is complex-linear under J_t / r3.
  - On 2' + 2'', which is 4 copies of one complex-type piece, the operators kept by the 24 form M_4(C). Their products
    of shears (unipotents) have complex determinant 1: they lie in SL_4(C).
  - The uniform turn T is the scalar c + r(-3) s on the copies, with determinant (c + r(-3) s)^4. Measured:
    (-129263 - 9568 r(-3)) / 130321, not 1.
  - So no product of carried shears kept by the 24 is T. Only theta in (pi / 2) Z escapes, and no rational turn there
    parts anything: theta = pi gives -1 on both 2' and 2''.
  - The 24's orbit of a vector of 2' + 2'' spans a Q-invariant space (rank 8, and 8 with Q). This is a sanity check;
    it follows from Q being a sum of L(g).
  - A turn of determinant 1, for example +theta on three copies and -3 theta on one, is reachable. But it needs a
    frame of the four copies, which no family gives: a declaration.
- **What the click world would read: nothing tonight (OPEN).** A half-speed train has no click (HALF2's gate). The
  toy's turn, if laid, would break the half turns about the axes on the half-speed quanta alone: a world turned by a
  half turn would click otherwise. It would not move light, which the turn does not touch.

## 4. The probe (MEASURED, twice; probe_gen5.txt)

- **The parted rates.** The exact turn T parts 2' from 2'': tr((456 T)^k B) = 0, -36,864, -23,003,136, ... for
  k = 0 to 8. The round spring-then-turn, (R(h) + R(h^-1)) a - b and then T on both slots, parts them at k = 4
  (-1,218,982,182,912). The same round without the turn reads 0 at every k, as GEN4 1.4 says.
- **The run back.** 20,000 of 20,000 on the toy plane's carried shears.
- **The 24.**
  - T is kept by all 24 and reversed by the r2 lifts.
  - The toy plane's turn on the train is kept by 6 of 24.
  - No carried shear form keeps the 24 for T (the determinant).
- **The controls that must fail, and do.**
  - The toy plane's turn fails the 24: 6 of 24.
  - The round with no turn fails to part: 0 at every k.
  - The uniform turn's determinant fails to be 1.

## 5. Status, one word each

| question | status |
| --- | --- |
| where 2' and 2'' are on the train, and the 24's plane (Q / 2, J_t^2 = -3) | DERIVED |
| Big Pic's axes' plane kept by the 24 on the train: no, 6 of 24 | MEASURED |
| the turn T: exact, orthogonal, kept by the 24, reversed by the r2 lifts, parting 2' from 2'' | MEASURED |
| the power road R(s)^sigma: refused (width, a loop, line 102) | DERIVED |
| the Cayley road: no cosine, no aimed angle, a CHOSEN strength | DERIVED |
| the INDICATOR rule for the shears | DERIVED |
| the run back of carried shears by the same shears at -t | MEASURED |
| the round as a palindrome, and sigma read where the mirror reads it | OPEN |
| carried shears kept by the 24 forming the uniform turn: impossible (complex determinant) | DERIVED |
| the parting term on HALF2's train, lawful in the engine's terms | OPEN |
| its source in the families' coupling (sigma pairs now and before; a new step of the act) | OPEN |
| what the click world reads | OPEN |

On the engine's terms the turning frame gives either the run back, by carried shears in a plane the 24 do not keep,
or the 24, by the exact turn T, which has no carried form. It does not give both. The parting term stays OPEN, and
the obstruction is the complex determinant of the uniform turn.
