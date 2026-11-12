# Integer coordinates for the joined sourced massless map

Baseline: `f4f64e062f07b3ca119eccf655df746be206908b` (current PR56).
This lane supplies an exact coordinate/scaling certificate for the single
six-channel model implemented by `validation.sourced_map.native`. It does
not add a projective numerator recurrence or a separate physical tensor.

## Physical sector and exact map

Take the homogeneous, isotropic, neutral **massless** scalar plus normal dust
subcase of the existing reduced equations. Write volume `V=B^-3>0`,
`U=Vdot=-3kV`, scalar charge `P=pV` and dust coefficient `D=d²V`. Both P and D
are conserved. The Einstein constraint and evolution become

\[
U^2=\frac32P^2+3DV,\qquad \dot V=U,\qquad \dot U=\frac32D.
\]

The exact time-h map, rather than an Euler approximation, is

\[
V'=V+hU+\frac34Dh^2,\qquad U'=U+\frac32Dh.
\]

Substitution proves preservation of `U²-3P²/2-3DV` and inverse time-h recovery.
The decoded fields `k=-U/(3V)`, `p=P/V`, `d²=D/V`, `B=V^-1/3` obey the
massless reduced equations. Symbolic checks independently verify
`kdot=3k²-d²/2`, `pdot=3kp`, `(d²)dot=3k d²`, and the positive-branch
identities `ddot=3kd/2`, `Bdot=kB`. The scalar field must still be reconstructed
with its retained integration reference as described in the joined decoder.
No numerical reference trajectory drives these equations.

This is a restriction to mass squared zero. For the massive source the
constraint also contains `-mu*phi²` and its dynamics change. The selected
map is not a solution of that massive system. Spatial gradients, charge,
Maxwell and anisotropic geometry are absent.

## Exact integer scaling and use of both histories

Fix `h=1/N` before execution and use

\[
q=4N^2V,\qquad J=4NU.
\]

At the implemented unit convention, D and P are retained integers. The
integer coordinate map and inverse are

\[
R(q,J)=(q+J+3D,J+6D),\qquad
R^{-1}(q,J)=(q-J+3D,J-6D).
\]

Its exact quadratic invariant is

\[
I=J^2-12Dq-24N^2P^2.
\]

The joined native model does **not** allocate a J channel. Instead the
volume's two retained histories encode it bijectively:

\[
J=b_q-a_q+3D,\qquad a_q=b_q-J+3D.
\]

The actual fixed-six input `u_q=6b_q+18D` therefore gives

\[
b_q'=2b_q+6D-a_q=b_q+J+3D,\quad a_q'=b_q,\quad J'=J+6D.
\]

All coefficients are divisible by three, so for every legal carry
`divmod(2u+r,6)=(u/3,r)`. Carries remain retained rather than being reset or
discarded. Constant-source/reference channels require both histories equal;
the proper-tick channel instead has its declared unit history difference.
The scalar offset and reference velocity are retained by the joined
six-channel model, not supplied later from an external initial-condition log.

The physical constraint is exactly

\[
H=6k^2-p^2-2d^2=\frac{2N^2}{3b_q^2}I.
\]

This differs from the failed current-slice Cayley lift. Here physical
velocity depends on both retained histories and the source terms. There is
no independently null target minus an independently null old physical
four-vector. Consequently the previous null-vector obstruction does not
apply. Nothing in this argument relaxes Rule3 or deletes mandatory memory.

## Exact representability and legitimate restrictions

`encode_initial(V,U,D,P,N)` requires rational V,U; positive V; integer D,P
with D nonnegative; integer `4N²V` and `4NU`; and the exact constraint.
It rejects rounding. Every constrained rational V,U with integer D,P is
representable at sufficiently divisible N. A simple mixed-source family is
to choose positive integer D, integer P and rational U with
`U²>3P²/2`, then set `V=(U²-3P²/2)/(3D)` and choose N to clear denominators.

The implemented rational coordinate domain excludes nontrivial pure
massless-scalar data D=0, P!=0: its constraint would require
`(U/P)²=3/2`, impossible for rational U/P. It does not follow that such a
physical solution is impossible; an algebraic coordinate extension would
be required. Pure dust P=0 can be represented, as can mixed sources with
either sign of P and either expansion sign of U.

Positive real B and dust-amplitude branches are selected. B and d are
generally algebraic rather than rational physical values; the scalar field
uses a logarithmic antiderivative. Exact integer evolution does not imply
that those displayed physical fields are rational. Negative dust-amplitude
signs, alternative frame orientation and massive/inhomogeneous modes are
not silently reconstructed from information that was never retained.

The integer map is reversible globally, but a physical trajectory must stay
in a connected V>0 branch. A large step that passes through V=0 and returns
to positive V is not a valid continuation of this spacetime patch. Physical
domain enforcement belongs in the passive audit/readout and must not veto
or repair Engine updates.

## Executed independent checks

`validation.sourced_map.projective` verifies the polynomial invariant,
inverse, history-coordinate bijection, exact physical scaling and source
ODE identities symbolically. It checks24 constrained rational source
families (D=1,2,5; P=-3,-1,0,2; expanding/contracting) through five integer
coordinate steps and inverse recovery. These are independent coordinate
oracles; the joined native audit supplies the actual Engine evidence.

For V0=1,U0=3,D=1,P=2, the N=24,48,96 families make3,6,12 steps to the
same physical time T=1/8. Every exact endpoint is

\[
V(T)=355/256,\qquad U(T)=51/16.
\]

Negative controls reject an unrepresentable resolution, nonzero initial
constraint and nonpositive initial volume. A separate exact control changes
only the old source history: with `a_D!=b_D`, the source evolves and the
decoded next velocity differs from the assumed constant-source map by3.
This keeps the full-history preparation condition visible.

```bash
python -m validation.sourced_map.projective
```

Output: `runs/sourced-map/projective.json`, including the source hash,
symbolic certificates,24 family records, three fixed-endpoint checks and
negative controls. Helpers available to the joined audit are
`history_to_phase`, `phase_to_history`, `affine_step`, `invariant_jet`,
`constraint_numerator` and `encode_initial`.
