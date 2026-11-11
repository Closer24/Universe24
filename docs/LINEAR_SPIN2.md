# Exact constrained integer curl waves

This isolated construction supplies a nontrivial, bounded travelling sector of the unchanged scalar Rule3 engine. Its prepared fields obey exact symmetry, trace and divergence constraints. It is a linear tensor-wave example, not a nonlinear Einstein metric, a universal matter coupling or a calibrated detector.

Reproduce it from the repository root:

```sh
python experiments/geometry/linear_spin2_check.py
```

The default output is under ignored `runs/geometry/`. The checked evidence is
[linear_spin2.json](evidence/linear_spin2.json), produced by
[linear_spin2_check.py](../experiments/geometry/linear_spin2_check.py).
No default layer or core update is changed.

## 1. State, operator and the one update

At each node store two full 3×3 integer arrays E and B, hence 18 gear types. Every gear retains the usual a,b,r triple. The arrays are stored in full so that off-diagonal equality is an explicit prepared constraint, not a hidden overwrite.

On a periodic cubic grid define commuting central differences

    delta_i=T_(+e_i)-T_(-e_i).

The chosen single-index curl is

    (A T)_ij=epsilon_i k l delta_k T_lj.

It is ordinary vector curl applied to each column. This full-nine-component extension is deliberate. Let D=6Q and use only the fixed inputs

    u_E=(D/2) A b_B,   u_B=(D/2) A b_E.

Because D is even, all tensor coefficients are integers. The input is linear: tensor order two, below the maximum four. Each monomial reads one face neighbor. With all gears declared as node fields, its physical support is one edge. The construction has 72 nonzero monomials.

Every 2u is divisible by D. Therefore, for every allowed remainder phase, the actual scalar Rule3 gives exactly

    a_E'=b_E,   b_E'=A b_B-a_E,   r_E'=r_E,
    a_B'=b_B,   b_B'=A b_E-a_B,   r_B'=r_B.

No remainder approximation, rounding omission or extra update instruction is used. The operator A appears only through the fixed tensor coefficients.

## 2. Exact constrained sector

Call a tensor TT here if it is symmetric, tracefree and divergence-free under the declared central differences:

    T_ij=T_ji,   sum_i T_ii=0,   sum_i delta_i T_ij=0.

These are discrete linear constraints; their name does not by itself identify T as measured curvature.

The operator A preserves this sector. Its trace vanishes on symmetric T because an antisymmetric epsilon contracts a symmetric pair. Its divergence vanishes by commutation of central differences. The antisymmetric part of A T is dual to div T-grad(tr T), which vanishes on TT tensors. Thus A T is again symmetric, tracefree and divergence-free.

If both a and b tensors satisfy these constraints initially, the exact Rule3 recurrence preserves them at every update. Constraints need not hold for arbitrary seeds; no projection or attracting correction is applied.

On a periodic grid, delta_i is skew-adjoint and the epsilon component matrix is antisymmetric. Their product makes A self-adjoint in the full Frobenius inner product, including off-sector full-nine-component arrays. The inputs are reciprocal derivatives of

    Phi=(D/2) <E,A B>.

The full-state inverse is explicit: old b=new a, old r=new r, and

    old a_E=A new a_B-new b_E,
    old a_B=A new a_E-new b_B.

The test also verifies covariance under all 24 proper cube rotations on a generic off-sector state. E and B transform as R T(R^-1 x) R^T; signed component changes are accompanied by an allowed complementary remainder phase. A local perturbation has no effect beyond its face-distance causal prefix in the checked steps. These are finite lattice symmetries/locality statements, not continuous Lorentz invariance.

## 3. A prepared first-order interpretation without a phase callback

Define two algebraic involutions on the current E,B arrays:

    P(E,B)=(E,-B+A E),
    J(E,B)=(-E+A B,B).

Both square to the identity, and P+J=(A B,A E). If the initial retained state is prepared with a=P(b), Rule3 alternates the two phase graphs: the first current-state update is J, the next P. This is a consequence of the existing a,b memory, not a runtime schedule.

Two updates give

    W^2 b=-F(b),
    F: E_new=E-A B,  B_new=B+A E_new.

Removing the fixed sign carrier at even updates is a passive algebraic description of F. It is not an extra board operation and does not identify the global update counter as physical proper time. F is a symplectic-Euler discretization of opposite-sign curl equations.

Roy Maartens and Bruce Bassett, *Gravito-electromagnetism*,
https://arxiv.org/pdf/gr-qc/9704059, define the conventional symmetric tensor curl and explain the Maxwell-like Weyl equations. Their introduction also explicitly distinguishes the Bianchi equations from the additional geometric information needed for an Einstein solution. Here A equals the conventional symmetric curl on the TT sector when the same differences are used. Since delta_i approximates 2dx partial_i, the formal macro time unit for unit propagation speed is 2dx. This scaling statement does not prove a general stable continuum limit.

## 4. Exact integer travelling profiles, bounded for all time

Consider a profile depending only on z. Write its two TT polarizations as

    E=[[p,q,0],[q,-p,0],[0,0,0]].

Let S f(z)=f(z+1), and let R_perp(p,q)=(-q,p). On these tensors,

    A=R_perp(S-S^-1),   R_perp^2=-I.

Choose any two periodic integer profiles p,q and prepare

    B=R_perp S E,
    a_E=E,   a_B=-R_perp S^-1 E.

This is exactly a=P(b). Direct substitution yields

    E-A B=S^2 E,
    B+A S^2 E=S^2 B.

Therefore every two updates give

    b_(2n)=(-1)^n S^(2n) b_0.

The odd update also consists only of shifts and signs on these prepared profiles. Hence their amplitudes are bounded for all time, not merely over the tested horizon. S shifts the profile argument positively; its peak moves toward the negative coordinate direction. The same construction works along each coordinate axis and linear superpositions of those axis sectors remain exact. Such a superposition is not a single oblique wave or a claim of full directional stability.

The checked L=7 profiles have zero mean:

    p=(3,-2,-1,0,0,0,0),
    q=(2,0,0,-1,-1,0,0).

Zero mean avoids the simplest periodic zero-mode obstruction to later metric reconstruction, but no metric reconstruction is claimed here. The complete a,b,r state has minimal period 28 for these preparations. That exact return plus the explicit shift formula proves the observed amplitude bound for all future repeats. The remainder background stays fixed; it is not translated with the counter pattern.

| Preparation | Steps checked | Peak counter | Full-state period | Official records |
|---|---:|---:|---:|---:|
|z profiles, Q=1|56|3|28|120736|
|z profiles, Q=7|56|3|28|120736|
|Three axis sectors, Q=7|56|5|28|258720|

Every symmetry, trace and divergence residual on both a and b remained exactly zero. Every remainder was constant and every full state rewound exactly. A separate Q=1 versus Q=2^70 comparison gives identical counter histories and official quotient records despite different allowed initial remainder phases.

All official events in this sector are arithmetic kind C0 because the remainder does not move. Their signed quotients still carry a nontrivial travelling pattern. Counting these events or naming them C0 does not make them physical graviton detections.

## 5. The essential negative control: general three-dimensional instability

On a generic nonzero Fourier mode, let v_i=2sin(k_i). On the TT subspace the single curl has eigenvalues

    c=+/-|v|=+/-2sqrt(sum_i sin^2 k_i).

The macro map satisfies cos(omega)=1-c^2/2. Its exact conserved quadratic is

    H=||E||^2+||B||^2-<E,A B>.

It is positive definite only on spectral sectors with |c|<2. Generic three-dimensional modes violate that condition. At |c|=2, generic Jordan directions can also grow, although the exact travelling preparation selects bounded combinations.

The experiment supplies an integer TT seed combining f(x+y) and f(x+y+z) on L=5. The single-curl run reaches 103-bit counters by update 64. All TT constraints, constant remainders, the macro quadratic identity and exact rewind still hold. Thus exact constraint preservation, reciprocity and reversibility do not establish stability.

Central differences also vanish at Nyquist components on even grids. There the divergence constraint rank changes and extra static/doubler sectors exist. Two propagating polarizations describe generic nonzero-symbol TT modes, not every lattice mode or arbitrary full 18-gear seed.

Dividing A by a chosen integer generally reintroduces componentwise carries and may spoil the exact constraint identities. A global resolution lift scales numerator and divisor together and does not change this spectral ratio. Any proposed smaller-step remedy needs a separate arithmetic or retiming proof.

## 6. Why the original doubled curl was replaced

The earlier full-nine extension

    (C T)_ij=epsilon_i k l delta_k T_lj+epsilon_j k l delta_k T_il

is self-adjoint and preserves TT constraints; on TT tensors it equals 2A. Its trace vanishes even on a general full tensor because epsilon contracts T_li+T_il. Its indices must not be confused with a different off-sector symmetrization.

Using C doubles the problematic spectrum. The matching L=5 control reaches 175-bit counters after 64 updates while still preserving constraints and rewinding exactly. Replacing it by A does not divide a rounded result by two: it selects a different, wholly integer, full-nine tensor that agrees with the desired half-curl on the invariant TT sector.

There is a stronger obstruction for that doubled scheme alone. On a finite periodic integer board any bounded complete orbit is periodic, so supported macro eigenvalues lambda are roots of unity. For a doubled TT Fourier mode,

    c^2=4alpha,   alpha=sum_i(2-zeta_i^2-zeta_i^-2),
    c^2=2-lambda-lambda^-1.

Alpha is an algebraic integer. Every conjugate lies in [0,1], because the conjugates of lambda are also roots of unity. If alpha is nonzero, its algebraic norm is a positive integer no greater than one; equality forces every conjugate to equal one. Thus alpha is 0 or 1. Bounded modes can only have c^2=0 or4, with growing Jordan directions excluded. This prevents generic bounded oscillatory integer travelling modes in that doubled discretization. It is not a no-go theorem for A, for other Rule3 tensors or for differently encoded systems.

## 7. Scope of the result

The positive result is an exact, local, reciprocal constrained tensor sector with arbitrary integer travelling profiles and a passive arithmetic event stream. This tensor is unstable for generic three-dimensional preparations; a stable general replacement remains to be constructed. No coframe or metric is reconstructed, no matter reads this field as a common geometry, no full Einstein constraints are imposed, and no calibrated detector is built. The construction is a building block for those questions, not their completion.

## 8. Separate exact retiming control

The original curl example propagates its prepared axis profile at one coarse
site per update. A separate, simpler tensor shows that this speed is not a
universal restriction of Rule3. It does not modify the curl experiment or its
instability control.

For one chosen axis let S shift the profile argument by one coarse site. Store
two banks X,Y for each of the two planar polarizations p,q: four scalar gears.
Define the integer permutation

    R(X,Y)=(Y,S X),   R^-1(X,Y)=(S^-1 Y,X).

Use the fixed inputs

    u_X=(D/2)(Y+S^-1 Y),
    u_Y=(D/2)(X+S X).

These eight linear monomials are rank two and each uses either one node or one
physical edge. R is orthogonal as a permutation, so R^-1=R^T. Consequently the
input matrix is symmetric and comes from the reciprocal potential

    Phi=(D/2)<X,(I+S^-1)Y>.

Prepare a=R^-1 b, with any allowed fixed remainder phases. The actual Rule3
quotient is exactly (R+R^-1)b, because its numerator is divisible by D. Hence

    b'=R b,   a'=b=R^-1 b',   r'=r.

The prepared graph is invariant; no phase callback or runtime projection is
needed. R^2(X,Y)=(S X,S Y), so both banks shift one coarse site every two
updates. Every prepared counter is a permutation of an initial counter and is
therefore bounded for all time.

An exact every-update interpretation is available by choosing a periodic
integer profile on a ring of length 2L and preparing

    X_z=f(2z),   Y_z=f(2z+1).

Then R shifts this interleaved profile by one fine sample per update. If the
coarse spacing is one, the fine spacing is one half and the pattern speed is
one half. This is a staggered interpretation of two internal banks along one
axis. It does not refine the other spatial coordinates, change the board
graph, or prove that those internal offsets are physical positions. Preparing
X=Y instead gives a staircase when only one bank is read.

[retimed_tensor_wave.py](../experiments/geometry/retimed_tensor_wave.py) checks
the actual Engine against an independent fine-ring oracle. The
[checked evidence](evidence/retimed_tensor_wave.json) covers all three separate
axis choices at Q=4 and Q=2^72: six histories of 56 updates, each with peak
counter 3, complete state period 14, constant remainders and exact reversal.
The reconstructed planar tensors obey symmetry, trace and divergence
constraints on both retained states in each bank. Counter histories and
official C0 records agree across the two divisors. Rotating the chosen axis
selects a different fixed tensor; this is not a proof of one isotropic
three-dimensional propagation law.

The negative control starts all banks with a=1,b=0 instead of the required
phase graph. It gives the exact unbounded solution a_t=1-t,b_t=-t while still
rewinding. Thus the all-time bound applies to the prepared sector, not to all
states of the reversible recurrence.

This supplies a precise next candidate for the characteristic-speed mismatch
in the separate metric-shaped probe. A scalar stencil

    u_chi=D chi+w Delta chi,   w=D/8

has long-wave speed sqrt(2w/D)=1/2; w is integral when Q is divisible by four.
Its complete linear dispersion is

    cos(omega)=1-(1/2) sum_i sin(k_i/2)^2,

which lies in [-1/2,1], with spectral headroom in three dimensions. Along an
axis its frequency is 2 asin[(1/2)sin(k/2)], whereas the smooth interleaved
retiming branch has frequency k/2. They agree to leading order only; their
difference is order k^3. This scalar stencil is an algebraic comparison, not
an executed matter-coupling experiment here. Retiming therefore offers an
exact bounded building block and a matching long-wave speed candidate. It
does not establish matching finite-lattice dispersion, a shared microscopic
cone, reciprocal gravitational backreaction or Einstein dynamics.
