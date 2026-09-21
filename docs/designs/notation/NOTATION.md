# The one symbol table of the law without clashes with physics' letters: the proposal (read-only, the derivation mathematician, 2026-09-21)

The owner's order (record 362, through the Visualiser, translated: "the
names must be chosen so that there are no clashes, and so that they look
good like all the formulas in the world"), put by the Boss as one page
for his decision: TERMINOLOGY's symbol table (the Boss's), the paper,
HIGHLIGHTS 5.7 and FORM.md follow it, one writer per document. Nothing
here changes a rule or a world key.

**The rule of record 184, applied.** Every symbol is named in English
at its first use; a scalar plain (E, p, c), a vector bold lowercase
(**p**, **s**), a matrix, a tensor or an operator bold uppercase (**C**,
**G**), a component plain with its index (`p_x`); inside a code span
every letter is plain. Two rules added by this proposal: (i) a world
key or a code identifier is written in code font and is not a formula
symbol (`K`, `width`, `release`, `action`, `direction_bound`), so a
letter that names a key never clashes with a letter in a formula; (ii)
physics' letters keep physics' meanings wherever they appear in a
formula: E energy, `E_0` the rest energy, **p** momentum, c the limit
speed, gamma the Lorentz factor, m mass, h Planck's quantum, f
frequency, v speed, G Newton's constant, F force, W work, S action or
entropy, Q charge. The law's own letters that clash with these appear
today as: Q the label's scale (64), S the width, N the circle, P the
direction bound, K the clock's pair and the budget, G the fan's grain
and the strong column, W four times (the exact square of the energy,
17.6; the click's weight `f^T G f`; the drive's wall; the birth wheel
in TERMINOLOGY), F the interval's map (**F**), and beside them D the
direction against the diffusion tensor **D** of section 25, T the
ladder's total against `T_D` the resolution, k the presence against the
wave vector **k**, **V** the label flow against a potential, c both the
limit `1 / sqrt 3` and the heading's `32 / 55`.

## (a) The main formula in physics' letters

    E^2 = E_0^2 + p^2 c^2,        c^2 = 1 / 3  (Links per interval)^2,   the pace  v = p c^2 / E,
    E_0 = m c^2,   m = Q S M       (the definition line: Q the label's scale, S the width, M the content, the law's grains and count; nowhere else in the formula)

The integer form, marked once beneath it: the law keeps `(E / c^2)^2 =
m^2 + 3 p . p` as an integer and never roots it (17.6 M3: the exact
square, the comparisons only); in code `energy_square`. The prime of
17.6 (`E'`, `E'_0`) goes: `E'` was E in mass units, `E / c^2`, and the
paper writes E with `c^2` explicit. So the formula reads as every
physicist reads it, and the law's constants stand in one definition
line where a footnote names them as grains, not as charge and action.

## (b) The clashes, a letter each: the recommendation, the alternatives, the cost

| Today | Recommended | Alternatives (one line each) | The cost (documents; code) |
| --- | --- | --- | --- |
| W, the exact square of the energy | written `E^2` as above; the integer kept called "the exact square", code `energy_square` | `Omega` (a scalar Greek); `E2` | DERIVATIONS 17.6, 21.2 rows 38 and 44, 23, 24.1; no code (not built) |
| W, the click's weight `f^T G f` | R(f), the reading of 6.5 (already the theorem's letter) | `w(f)`; "the weight" in words | DERIVATIONS 6.5 to 6.7, TERMINOLOGY's **G** row; the code's `gram_form` keeps its name |
| W, the drive's wall | d, the wall of the counts table (the state's own symbol, **s**, **r**, d), subscripted `d_p` | `Delta_p`; "the wall" in words | FORM.md 3, 3.1, BEAM_LAW note 49, ENGINE; the code's `wall` keeps its name |
| W, the birth wheel [r, W] | `N_u`, the wheel's circle (the grain family below) | keep W with a footnote (the wheel is a count, not work) | TERMINOLOGY, BEAM_LAW note 46, DERIVATIONS 6.2, 24.4; the key `wheel` keeps its name |
| **F**, the interval's map | **Phi**, bold uppercase (the Boss's suggestion; the map of one interval) | a script F; **M** (clashes with M the content) | DERIVATIONS 0, 11, 24.1; TERMINOLOGY; LAW.md; no code |
| G, the strong column | `sigma_s`, the strong coupling per unit (19.1's own word "sigma") | `g_s` | BEAM_LAW note 40, the quarks design, DERIVATIONS 18.3, 19; the column key keeps its name |
| G, the fan's angular grain | `N_theta`, the grain family | `N_a` | TERMINOLOGY, TWO_SLITS.md, LAW.md, HIGHLIGHTS 5.7; the code's constant keeps its name |
| Q, the label's scale (64) | keep Q in the law's documents and the definition line; in the paper's formulas it appears only through m = Q S M | `N_l` (the grain family: the label's steps per unit) at the cost of 641 lines in docs, 340 in designs, 83 in src | none if kept; large if renamed |
| S, the width | keep S in the law's documents and the definition line, as Q | `N_w`; `w` (clashes with the window's width) | none if kept; 958 / 287 / 38 lines if renamed |
| N, the circle | keep N (physics' N is a count too) | `N_phi` when the family is adopted | none |
| P, the direction bound | `N_D`, the grain family | keep P (rarely in a formula) | TERMINOLOGY, BEAM_LAW section 2, note 49; the key `direction_bound` keeps its name |
| K, the clock's pair; K the budget (13) | the key in code font, `K`; in prose "the clock's rate `[n, d]`"; the budget of section 13 `K_node` | `r_phi` for the rate | DERIVATIONS 13 (already `K_clock` there), ENGINE; the key keeps its name |
| **D**, the diffusion tensor (25.6) against D the direction | `D_diff` in words "the diffusion tensor", as 25's notation line already wrote it | bold **B** | DERIVATIONS 25.6, 25.10, the symbol table (mine) |
| T, the ladder's total | `C_K`, the last cumulative weight (the cells' own letter) | `T_tot` | BEAM_LAW notes 37 and 46, TERMINOLOGY; the code's `total` keeps its name |
| k, the presence a body read | `a_r`, the amount read (the reading's own letter **a**) | `n_r` | BEAM_LAW step 2, ENGINE, DERIVATIONS 12c; the code's `counted` keeps its name |
| **V**, the label flow at a Node | **a**, the label flow vector of the derivation (section 0's row) | keep **V** in code font as the code writes it | BEAM_LAW step 2, TERMINOLOGY; the code's `V` keeps its name |
| c, two paces | c the limit `1 / sqrt 3`; a direction's Manhattan pace `c_1 = S_1 Q / T_D` (section 0's row), `64 / 110` on a heading written `c_1` | `c_h` for the heading (18.6's), to be replaced by `c_1` | DERIVATIONS 2, 12, 17.6, 18.6 (mine); TERMINOLOGY's c row |
| A, the norm of a split; **A** the axis | the norm written out, `sum a_i^2`; the axis `e_A` (a unit vector, bold lowercase **e**) | `nu` for the norm | BEAM_LAW notes 37 (ii) and 39; the keys keep their names |
| L, the lifetime | keep L (physics' tau is the age here) | `T_L` | none |
| h, f, E, p, v, gamma, beta, rho, m, M | keep: physics' meanings (M the content as a count of units, m = Q S M the mass in label units; both named) | | none |

The grain family, if adopted as one rule: every grain is N with a
subscript naming what it grains (`N_phi` the circle, `N_l` the label,
`N_w` the width, `N_D` the direction bound, `N_theta` the angle, `N_u`
the wheel), the paper's formulas carrying m, c, h alone; the cost is
the rename of Q and S across the law's documents (about 1900 lines),
which is why the recommendation keeps Q and S in the definition line and
renames the cheap ones (the four W's, **F**, the two G's, P, T, k, **V**,
the second c, the diffusion tensor).

## (c) The table of the law, under the rule

| Symbol | Kind | Name | Physics' reading |
| --- | --- | --- | --- |
| E, `E_0`, m, **p**, c, v, gamma, beta | scalars, one vector | the energy, the rest energy, the mass `Q S M`, the momentum, the limit speed, the speed, the Lorentz factor, `v / c` | the same |
| h, f, s | scalars | the quantum of action (`E = h f`), the frequency `s / N` per self-creation, the turn | the same (s the turn, not the action) |
| M, Q, S, N, `N_D`, `N_theta`, `N_u` | scalars | the content (units), the label's scale, the width, the circle, the direction bound, the angle grain, the wheel | counts of the lattice (the definition lines) |
| **Phi**; **s**, **r**, d | operator; vector, vector, scalar | the interval's map; the state on the torus, its rate, its wall (`d_p` the drive's) | none (the map), the accumulator |
| **C**, **a**, `sigma_s` | matrix, vector, scalar | the coupling matrix, the label flow read at a Node, the strong coupling per unit | the same as a coupling |
| **G**, **E**, **U**_s, R(f) | matrices, a form | the click's Gram matrix, the tables' matrix, the label rotation, the click's reading (weight) | none |
| D, `u_D`, `T_D`, `S_1`, `c_1` | vector, vector, scalars | a direction, its unit vector at the scale Q, its resolution, its Manhattan length, its Manhattan pace | none |
| u, tau, `b_k`, `C_k` | scalars | the birth wheel's value, the age, a rung, a cumulative weight (`C_K` the total) | none |
| `a_r`, `[n, d]` pairs | scalar, pairs | the amount read (the presence), the declared rates (suspension, clock, release) as keys | none |
| **k**, lambda, psi, theta, omega | vector, scalars, a field | the wave vector, the wavelength, the wave function of the limit, an angle, the angular frequency | the same |
| Theta, `D_diff`, `c_s`, `nu_L`, g | scalar, tensor, scalars | the temperature reading, the diffusion tensor, the sound speed, the longitudinal viscosity, the Galilean factor (section 25) | the same |
| z, H, q | scalars | the redshift, the growing wall's rate, the deceleration parameter (section 15, 20) | the same |

## (d) The recommendation in one paragraph

Adopt (a) for the paper and for HIGHLIGHTS 5.7: physics' letters in
every formula, the law's Q, S, M in one definition line under m. Rename
the cheap clashes now, in prose only, the code identifiers keeping their
names (`gram_form`, `wall`, `wheel`, `total`, `counted`, `V`,
`direction_bound`): the four W's to `E^2`, R(f), `d_p` and `N_u`; **F**
to **Phi**; the strong column's G to `sigma_s` and the fan's G to
`N_theta`; P to `N_D`; the ladder's T to `C_K`; the presence's k to
`a_r`; **V** to **a**; the heading's pace to `c_1`; the diffusion tensor
to `D_diff`; the prime of `E'` dropped with `c^2` explicit. Keep Q, S, N
as they are in the law's documents (the rename would touch about 1900
lines and every world file's reader), or adopt the grain family `N_x`
in one later pass if the owner wants no Q and no S anywhere. The
alternatives stand in the table, one line each.
