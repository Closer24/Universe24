# A restricted integer pp-wave sector with local Palatini constraints

This experiment puts a prepared, nonflat vacuum plane-wave sector through the
unchanged Rule3 engine. It stores tetrad and scaled Lorentz-connection
components as integer gears, transports them through actual face-neighbor
terms, and checks the first-order gravitational constraints on the interior of
an explicitly declared coordinate chart. It is not a derivation of general
Einstein evolution, a global solution on the periodic transverse board, or an
operational proper-clock model.

Run the isolated experiment from the repository root:

```sh
python experiments/geometry/ppwave_palatini_local.py
```

The runner is
[ppwave_palatini_local.py](../experiments/geometry/ppwave_palatini_local.py).
The checked result is
[ppwave_palatini_local.json](evidence/ppwave_palatini_local.json).
It constructs a separate fixed tensor before the run and uses the shared
fixed-six engine. It does not mutate the default tensor or preparation.

## Exact continuum geometry used by the decoder

Use coordinates `(t,x,y,z)`, internal metric
`eta=diag(-1,1,1,1)`, and the constant null covector

    l = dt-dz,       l_mu = (1,0,0,-1),
    l^a = (-1,0,0,-1),
    L^a_mu = l^a l_mu,       L^2 = 0.

Let `P` be a fixed positive integer and choose

    s = z-t,
    F = A(s)(x^2-y^2) + 2 B(s) x y,
    E = P I + F L.

Here `E` is the coframe matrix, whose rows are the one-forms

    e^0 = P dt - F(dt-dz),
    e^1 = P dx,
    e^2 = P dy,
    e^3 = P dz - F(dt-dz).

Nilpotence gives identities valid for every value of `F`:

    det E = P^4,
    J = P I - F L,
    E J = J E = P^2 I,
    E^-1 = J/P^2,
    g = E^T eta E = P^2 eta + 2 P F l l^T.

The inverse is a passive exact rational readout with a fixed denominator. No
inverse, division by a state variable, determinant solve, or branch selection
appears in the fundamental update. Nondegeneracy and Lorentzian signature
hold independently of the profile amplitude.

The connection is stored with one fixed integer scaling. Write
`W_ab=P omega_ab`, with both internal indices lowered, and let each listed
coefficient multiply `l`:

    W_01 = F_x l,       W_13 = F_x l,
    W_02 = F_y l,       W_23 = F_y l,
    W_03 = W_12 = 0,
    W_ba = -W_ab.

Thus the six stored independent coefficients are integers when `A`, `B`, `x`,
and `y` are integers. Raising the first index uses `eta`; it is not an ordinary
Euclidean antisymmetric matrix. In mixed-index notation, the nonzero entries
of the actual connection are

    omega^0_i = omega^3_i = omega^i_0 = -(F_i/P) l,
    omega^i_3 = +(F_i/P) l,              i in {1,2}.

Since `(partial_t+partial_z)F=0`, the longitudinal derivative of `F` drops out
of `dF wedge l`. Direct substitution then gives

    T^a = de^a + omega^a_b wedge e^b = 0,
    omega wedge omega = 0,
    R^0_i = R^3_i = (F_ij/P) l wedge dx^j.

The corresponding other mixed curvature entries follow from metric
compatibility. The only possible Ricci contribution is

    Ric = -(F_xx+F_yy)/P * l tensor l = 0.

The transverse Hessian is

    [[F_xx,F_xy],[F_yx,F_yy]] = [[2A,2B],[2B,-2A]].

Consequently, a profile with nonzero `A` or `B` has nonzero curvature despite
its zero Ricci tensor. The metric is not merely flat spacetime written with a
changing diagonal scale factor. Curvature scalar contractions are not a
suitable nonflatness test here: vacuum plane waves can have nonzero Riemann
curvature while their polynomial scalar curvature invariants vanish.

These are the Brinkmann plane-wave identities. A primary reference is Abraham
I. Harte, [*Tails of plane wave spacetimes: Wave-wave scattering in general
relativity*](https://arxiv.org/pdf/1309.5020), section II, equations 5–8 and 14.
The convention above has `g/P^2` in Brinkmann form with wave profile `2F/P`.
The direct coframe and connection calculation fixes the signs and scaling used
by this experiment.

## What the integer time evolution actually does

The common engine divisor is the fixed constant `D=6`. The separate
constant `P=256` scales the geometric representation. It is not a second
engine divisor, a floating state variable, or a change to Rule3.

The unit cell has 48 gears:

| Gears | Count | Role |
| --- | ---: | --- |
| Two banks of 16 tetrad coefficients | 32 | Retained coframe components |
| Two banks of six lowered connection coefficients | 12 | Retained coefficients of `W=P omega` |
| Two signal banks | 2 | A transported pulse in the same fixed null direction |
| Two local clock controls | 2 | Period-four and period-six uncoupled oscillators |

This count of 48 follows from those explicit storage roles. It is not a
derived binary-octahedral (`2O`) representation or an identification with the
default group-reference block.

No field component is overwritten after an engine update. Every component,
including zero or constant tetrad entries, follows the scalar recurrence.
The coordinate-dependent initial values are constructed once by preparation.

Let `S` denote the negative index shift,

    (S f)(x,y,z) = f(x,y,z-1).

A profile `f(z-n)` therefore moves in the positive `z` direction as the coarse
time `n` increases. For each transported bank pair `(X,Y)`, the fixed tensor is

    u_X = 3 (Y + S^-1 Y),
    u_Y = 3 (X + S X).

Each monomial has integer coefficient, input degree one, and support on the
target node or one face neighbor. No monomial touches both face neighbors.
There are no old-`a` reads or inverse-stage cycles.

Define `R(X,Y)=(Y,SX)`. On the prepared subset

    a = R^-1 b,       r = 0,

the exact Rule3 update is `b_next=R b`. Indeed, its polynomial input is
`u=3(R+R^-1)b`, so `divmod(2u,6)` has zero remainder and the old `a` cancels
the `R^-1 b` contribution. A single geometric profile `f` has the injective
encoding

    b = (f,f),
    a = (S^-1 f,f),
    r = 0.

If this encoding is denoted by `Enc`, then the complete transported-bank
state identity is

    EngineStep^2 Enc(f) = Enc(S f).

The identity includes `a`, `b`, and `r` for these banks; it is not just
equality after discarding an auxiliary bank. The full 48-gear target also
retains the evolving clock states. Two updates advance their phases rather
than resetting them, so `Enc(f)` here denotes the transported-bank part only.
Odd microsteps have staggered banks. The geometric observation times are the
even microsteps, one coarse unit apart.

The target map is therefore an exact reversible translation within this
prepared wave sector. The continuum vacuum equations allow arbitrary smooth
functions `A(s)` and `B(s)`; they do not select the chosen initial waveform.
Choosing that waveform and preserving its null translation is a restricted
solution construction, not solving the generic Einstein initial-value
problem.

## Constraint preservation and exact difference checks

On the declared chart, the prepared fields obey the coframe profile relations,
the transverse gradient relations for `W`, and the trace-free Hessian
condition. Translation in `z` preserves these relations because `x` and `y`
are unchanged. Both `S` and `S^-1` preserve them. The determinant is the
constant `P^4` throughout the evolution.

The residual calculation uses commuting centered coordinate differences.
For a component `q`, define its integer numerator

    delta_mu q = q(event+mu) - q(event-mu).

The centered derivative is `delta_mu/2`. Coarse time neighbors are the
neighboring geometric observation times, rather than single microsteps.
For `F_n(x,y,z)=F_0(x,y,z-n)`, the longitudinal identity is exact even for
arbitrary integer profile samples:

    delta_t F + delta_z F = 0.

Centered transverse differences differentiate a quadratic profile and its
linear gradient exactly wherever the stencil remains inside the chart.
Treating `delta` as the corresponding exterior-difference numerator, the
runner evaluates only integer-scaled residuals:

    Tor2   = P delta E + 2 W wedge E,
    Curv2  = P delta W + 2 W wedge W,
    Pal_a  = epsilon_abcd E^b wedge Curv2^cd.

Mixed-index matrix products raise the first Lorentz index with `eta`. These
quantities represent `2P T`, `2P^2 R`, and the corresponding scaled vacuum
Palatini equation. Because all connection one-forms are proportional to the
same `l`, `W wedge W=0` in this sector. No fractional intermediate is needed
to check the residuals.

The finite-difference result is a direct identity for this ansatz. Centered
differences do not obey the ordinary product rule on general fields. Thus the
result does not establish a general discrete exterior calculus, local Lorentz
gauge covariance, a discrete Palatini action, or preservation of all Einstein
constraints for unrestricted data.

The runner retains an explicit product-rule control. Under the different
shifted product `dx_mu f=(S_mu f) dx_mu`, two connection one-forms proportional
to `dt-dz` need not have zero wedge product. For the recorded integer sample,
the relevant coefficient is `6*(8-4)=24`. Thus the pointwise-product zeros
cannot simply be reused in that lattice exterior calculus. This arithmetic
control is separate from the engine trajectory.

The runner also constructs a coordinate Ricci numerator using the polynomial
inverse certificate and checks the normal-normal and normal-spatial
projections of the decoded Einstein tensor. Their vanishing follows from the
vanishing full Ricci tensor in this sector. These are consistency checks of
the corresponding ADM projections, not an independently derived discrete ADM
Hamiltonian, lapse/shift evolution law, or constraint solver.

The longitudinal profile can be interpolated by smooth periodic functions;
every such interpolation remains transversely harmonic and gives a continuum
vacuum metric. This interpolation is an interpretation of the samples. The
integer difference residuals are checked separately and do not depend on
choosing one interpolant.

## The chart boundary is part of the result

The runtime storage lattice is periodic in all three spatial directions.
The functions `x^2-y^2` and `xy` are not periodic transverse coordinate
functions. A stencil that wraps across an `x` or `y` seam therefore does not
differentiate the declared quadratic chart profile.

Bulk constraints are checked only where their transverse stencils remain
inside that chart. The runner also evaluates the seam stencils as a negative
control. Their failures are not dropped from the report or interpreted as
vacuum points. No atlas transitions are stored, and no claim is made that the
entire transverse torus supports this nonconstant harmonic profile.

## Signals and clocks: what is and is not supplied

For the geometric scale above,

    g_tt = P(2F-P),
    g^tt = -(P+2F)/P^3.

The bound `|2F|<P` makes fixed-coordinate time lines timelike and the
constant-`t` slices spacelike on the declared patch. It is a condition on the
chosen seed and fixed scale, not a consequence of Lorentzian signature
alone. Translation preserves the profile range, so a verified bound remains
true over the full orbit.

The signal banks use the same shift as the geometry. Their coarse trajectory
has tangent `v=partial_t+partial_z`, for which `l(v)=0` and `g(v,v)=0`
identically. This checks one fixed copropagating null direction. The signal
law does not respond to the profile. It supplies no bending, no independent
test of the opposite null direction or complete light cone, and no matter
backreaction.

The two local controls use `u=0` and `u=3b`, giving periods four and six at
the fixed divisor six and `r=0`. They do not couple to the metric fields. In particular, their
ticks do not change when the local coordinate-clock proper interval changes.
That missing response is an explicit negative operational result: these
gears have not become proper clocks merely because a geometric decoder
exists.

For the default longitudinal period of seven cells, the transported banks
return after 14 microsteps. Including both clock controls gives a
complete-state cycle of 84 microsteps. Checking that cycle and exact inversion tests the prepared
integer orbit; it does not establish gravitational energy conservation or
general stability.

## Recorded default check

The checked run uses `L=7`, `P=256`, and the integer profiles

    A = [-2,-1,0,1,2,-2,-1],
    B = [0,-1,1,0,-1,1,0].

Its tensor has 48 gears and 93 monomials, input degree one (tensor rank two),
passes strict single-edge support, and is reciprocal. The complete wave and
flat-control states each return exactly after 84 updates, and each recorded
step rewinds exactly. State and trace hashes are retained in the checked JSON.

One seven-macrostep longitudinal cycle gives the following results:

| Check | Recorded result |
| --- | ---: |
| Interior spacetime samples | 1,225 |
| Interior torsion, Palatini, Ricci, and normal/momentum projection residuals | All exactly zero |
| Largest absolute interior curvature numerator `Curv2` | 2,048 |
| Transverse seam events with nonzero torsion | 1,092 |
| Transverse seam events with nonzero Palatini residual | 840 |
| Minimum and maximum `-g_tt` | 54,272 and 76,800 |
| Minimum slice factor `P+2F` | 212 |
| Largest absolute retained counter during the cycle | 278 |

The nonzero curvature numerator distinguishes the vacuum wave from the flat
control. The positive coordinate-clock norm and slice factor verify the
timelike-coordinate and spacelike-slice conditions for this seed. They do not
make the uncoupled clock controls respond: the official clock and signal
records are identical in the flat and wave runs.

Two independent negative controls test the equations themselves. Replacing
the harmonic profile by one with equal `x^2` and `y^2` coefficients leaves
torsion zero but gives a nonzero Palatini numerator, with peak 2,097,152.
Setting the connection to zero for the nonconstant wave gives nonzero
torsion, with peak 6,144, even though its curvature-based Palatini expression
is zero. Both controls still rewind exactly.

A separate off-preparation history has `b_t=-t` uniformly in the selected
tetrad banks. This is exact unbounded drift under the same update law.
Boundedness of the prepared periodic orbit therefore does not extend to
arbitrary retained histories.

The milestone is therefore narrow but constructive: actual fixed integer
Rule3 terms transport a nonflat, constrained coframe/connection sector, with
an exact inverse and exact local vacuum residuals. The unresolved step is an
operational and less restricted gravity model whose matter, clocks, transport,
boundary treatment, and constraint evolution agree with the decoded metric.

A separate [prepared geodesic experiment](PPWAVE_OPERATIONAL_ROUTE.md) adds
geometry-dependent worldline registers and an exact calibrated clock readout.
It covers a static one-axis family. Its coordinates are stored at one carrier
node, so it does not repair the board-propagation or boundary limitations of
this experiment.
