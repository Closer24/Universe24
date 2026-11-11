# Tetrad/Palatini gravity: a precise next target, not a completed Rule3 derivation

The isolated checks are reproducible from the repository root:

```sh
python experiments/geometry/palatini_constraint_checks.py
```

The default output is under ignored `runs/geometry/`. The checked result is
[palatini_constraint_checks.json](evidence/palatini_constraint_checks.json).
The runner is [palatini_constraint_checks.py](../experiments/geometry/palatini_constraint_checks.py).
No default tensor or core update is changed by this experiment.

A separate [local pp-wave construction](PPWAVE_PALATINI_LOCAL.md) now provides
an exact prepared-sector embedding of a known nonflat vacuum family through
integer Rule3 steps. Its centered interior residuals vanish, but transverse
periodic seams and operational clock response fail. It addresses a restricted
example of the embedding criterion below; it does not resolve the general
Palatini evolution, gauge, or matter-coupling problem.

In every Rule3 recurrence below, `D` denotes the fixed constant six.
It is not an adjustable coefficient.

## What the polynomial action actually gives

Let e^a be a nondegenerate coframe and omega^ab an antisymmetric Lorentz connection. The metric is defined algebraically by

    g_mu_nu=eta_ab e^a_mu e^b_nu.

This identity can be evaluated exactly on integer/rational coframe data. By Sylvester's law, invertible e gives Lorentzian signature. The identity alone does not show that the chosen time coordinate is timelike, that link propagation follows this metric, that a retained coframe stays invertible, or that Einstein's equations hold.

The first-order gravitational action has the form

    S[e,omega] proportional to integral epsilon_abcd e^a wedge e^b wedge
        (d omega^cd+omega^c_f wedge omega^fd)
        -Lambda/6 integral epsilon_abcd e^a wedge e^b wedge e^c wedge e^d.

Its algebraic terms have degree at most four. For nondegenerate coframes and the appropriate matter hypotheses, its variations impose the torsion/connection equation and Einstein equation. Derek K. Wise, *MacDowell-Mansouri Gravity and Cartan Geometry*, https://arxiv.org/pdf/gr-qc/0611154, section5.1, equations10–12, gives this classical relationship. This is the useful polynomial target, not yet an explicit validated Rule3 input tensor.

## Why degree counting is insufficient

Palatini's time derivative terms are first order and degenerate. The connection momentum is constrained by coframe products; time components enforce gauge and geometric constraints. There are primary and secondary relations rather than independent unrestricted inertial data for every component.

In contrast, a b-only reciprocal Rule3 map with positive field signs, with remainders temporarily removed for this structural comparison, obeys

    D(q_next-2q+q_previous)=2 grad Phi(q)-2Dq.

A corresponding regular discrete Lagrangian is

    L_d(q,q_next)=D/2|q_next-q|^2+2Phi(q)-D|q|^2.

Its mixed kinetic Hessian is -D I, nonsingular. For reciprocal fields with signs s_i=±1, the corresponding sign-weighted kinetic form also has a nonsingular mixed Hessian. With allowed old-a reads, the chosen topological order makes partial b_next/partial a triangular with diagonal -1 in the smooth remainder-free map; it does not create Palatini's multiplier degeneracy. This comparison rules out a naive equality of the full unrestricted systems. It does not rule out a constrained invariant subset or a retimed encoding.

The exact control in the experiment makes the issue explicit. The reciprocal local potential

    Phi=D/2(q^2+lambda^2)-kappa lambda(q^2-1)

has degree three. With D=6,kappa=1,a=b=(1,1),r=0, the constraint q^2=1 is initially true but the next q is 0. The complete state still rewinds exactly. If q were one diagonal coframe component, a nondegenerate metric would have become degenerate. Giving the multiplier ordinary Rule3 inertia converts its role into another force equation, not algebraic constraint enforcement.

## Geometric locality is a separate condition

The curvature contains different connection directions. If omega_x and omega_y are honest link gears, a product involving both generally touches the base vertex and two different neighboring vertices. Such a term violates the repository's strict one-physical-edge monomial condition despite having low polynomial degree. The executable control constructs a rank-four term of this form and the strict validator rejects it.

A Wilson-loop curvature uses an entire plaquette. A finite-difference Lie-algebra connection has lower apparent degree, but its exact discrete gauge covariance is a further theorem; replacing derivatives by ordinary differences does not preserve all continuum product identities. Storing directional coefficients as node values may change support accounting, but then one must prove that their operational link transport is the intended connection rather than quietly treating physical links as pointlike.

Relays or a sequence of local reversible gates can communicate around a plaquette while each microstep remains local. The resulting curvature then belongs to a retimed encoding. Its consistency, inverse and constraint propagation must be shown over a complete macrostep; it is not an instantaneous local plaquette product.

The pure gravity degree count also does not settle matter: a direct tetrad Dirac term contains e^3 times a spinor bilinear and derivative/connection, while a direct mass term contains e^4 times the bilinear. Densitized fields or auxiliary formulations might reduce this cost, but their exact definitions and evolution must be supplied. A quartic pure-gravity action is not already a quartic universal matter-gravity tensor.

## A constructive embedding criterion

Choose a definite discrete geometric system first. Let C be its allowed, gauge-fixed integer state set, including nondegeneracy/orientation conditions and every discrete constraint. A usable target is a single-valued reversible map F:C->C. To represent it by the present automaton, require an injective encoding E and a fixed finite number m of local updates such that

    W^m E(z)=E(F(z)) for every z in C.

The encoding must retain all information needed for reversal, including remainders and arithmetic work registers. The decoded metric and link transport must agree at the specified observation times. If constraints are represented polynomially, exact ideal preservation F*I(C) subset I(C), together with the inverse condition and the nonalgebraic inequalities, is one possible route to proving invariance. Checking a few residuals numerically is not equivalent to this identity.

There is a general algebraic mechanism showing why a first-order target is not categorically excluded. If F and F^-1 are explicitly available, define involutions on two copies by

    P(x,y)=(y,x),
    J(x,y)=(F(y),F^-1(x)).

Then P^2=J^2=id. The prepared Rule3 construction u=(D/2)(P+J),a=P(b) alternates J and P; a two-step macro update gives (F^-1(x),F(y)). One copy therefore follows the target forward while the other retains reversible information. This exactly embeds the doubled map F^-1 x F. For the original single-copy F it is a simulation through projection, not by itself an encoding with a reset auxiliary state. A fixed auxiliary point, another invariant auxiliary preparation, or an explicitly extended target state is needed for that stronger conjugacy claim. Constraints are preserved if F and F^-1 preserve C. This is only admissible directly when both maps meet the polynomial-degree and physical-support bounds; otherwise a proven local reversible circuit compilation is needed.

For Palatini gravity, the prerequisite F is precisely what is missing. Its constraints, gauge choices, branch selection and implicit solves must be resolved consistently. Rational inverses, determinants and nonlocal constraint solves cannot be hidden inside a tensor coefficient or a state overwrite. If a finite arithmetic realization is built instead, its precision and retiming must be part of the stated model.

## Constraint preservation cannot be assumed from the continuum

Bahr and Dittrich, *Breaking and restoring of diffeomorphism symmetry in discrete gravity*, https://arxiv.org/pdf/0909.5688, show why ordinary discretization can remove continuum gauge degeneracies and discuss symmetry-preserving alternatives. This is not a no-go theorem for every discrete action. It establishes that action resemblance and polynomial degree do not suffice: the discrete equations and their constraint propagation need an independent derivation.

The next defensible milestone is therefore a small explicitly specified constrained geometric map, a valid seed, a proof of its inverse and constraint preservation, and an operational clock/link decoder consistent with g=eta e e. The previous variable-divisor conformal toy is retired. The active local pp-wave example is a narrower exact construction; it does not establish generic matter coupling or preservation of the full Einstein constraint system.
