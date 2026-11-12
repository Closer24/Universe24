# A cubic constraint-preserving target and its reversible-history obstruction

Run `python -m validation.completion.constraint_closure`. Evidence is written to
`runs/completion/07_constraint_closure.json`. This report separates an exact
rational target from the actual five-channel Rule3 tensor that attempts to lift
it. The latter passes mechanical checks and **fails** its constraint gate at the
second tick. Neither is an accepted full45 Einstein integrator.

## Homogeneous reduction and exact Euler defect

Take a homogeneous isotropic frame, K_ab=k delta_ab, real scalar phi with momentum
p, signed normal dust amplitude d, mass squared mu, zero connection, and zero
other fields. In the repository's synchronous convention the four source
equations are

```
k_dot   = 3 k^2 - (mu phi^2+d^2)/2
p_dot   = 3 k p - mu phi
phi_dot = p
d_dot   = 3 k d/2.
```

Write z=(k,p,phi,d), J=diag(6,-1,-mu,-2), F(z) for this vector field, and
C=z^T J z. Direct differentiation gives C_dot=6kC. This is preservation of the
zero constraint surface, not conservation of C at every off-constraint point.
The exact polynomial identity for the Euler map is

`C(z+hF) = (1+6hk) C(z) + h^2 F(z)^T J F(z)`.

On C=0, its last coefficient can be reduced to

```
R = -3 d^2 (mu phi^2+p^2)/4 - 3 mu phi^2 p^2/2
    - mu^2 phi^2 - mu p^2 + 6 k mu phi p.
```

This is generally nonzero. At the strong massive initial data
(k,p,phi,d,mu)=(-1,0,2,1,1), it is -7. At the massless data (-1,2,0,1,0), it is -3.
The symbolic test checks the entire polynomial identity, not merely these points.
An addition to F which vanishes on C=0 cannot alter this first-step defect there.

The shared full45 weak seed has (k,p,phi,d)=(-1/10,0,1/5,1/10), mu=1 and h=1/64.
Its actual Engine first step gives

`H_after = -403/40960000`,

exactly matching the general formula. The independently reduced C readout also
equals the full equation builder's Hamiltonian constraint. Its shared tensor is
`6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0`, and complete
seed hash is `b53909631f3e14e3c09905275fe7b50a0dad2ecdec9ac431db2306127abd3b7c`.

## An explicit reduced target with cubic numerator and denominator

The following decomposition avoids guessing a constraint projection:

```
F(z) = 3 k z + A(z) z,

A = [[0,       0, -mu phi/2, -d/2],
     [0,       0, -mu,        0  ],
     [-3 phi,  1,  0,         0  ],
     [-3 d/2,  0,  0,         0  ]].
```

The exact algebraic identity A^T J+J A=0 holds, including for mu=0. Let

```
L = I-h A/2,       R = I+h A/2,
delta = det(L),    N = adj(L) R z,
W = delta (1-3hk).
```

On the domain `delta!=0` and `1-3hk!=0`, define the rational target z_next=N/W.
The frozen Cayley matrix L^-1 R preserves J, so

`C(z_next) = C(z)/(1-3hk)^2`.

Thus it preserves C=0 exactly and its first derivative at h=0 is F(z). The
reciprocal dilation is deliberate: multiplying the numerator directly by
(1+3hk) would produce fourth-degree terms. Here all four entries of N and W have
degree at most three in the dynamical variables. This cancellation is checked
symbolically, as is

`N^T J N = delta^2 z^T J z`.

The determinant used for a concrete denominator audit is

`delta = 1 + mu h^2/4 - 3 d^2 h^2/16 - 3 mu phi^2 h^2/8 - 3 mu d^2 h^4/64`.

No global nonzero-denominator, global invertibility, stability or convergence
claim is made. This first-order-consistent rational target has no spatial
gradients, frame B, Maxwell fields or operational clock. It supplies an explicit
reduced source map for a future counted compiler, not a solution of the whole
Einstein system.

## Actual cubic Rule3 compilation and the exact second-tick failure

The audit expands N and W once in preparation, homogenizes them to degree three
in five retained coordinates (D,P_k,P_p,P_phi,P_d), clears fixed rational
coefficients with an integer multiplier, and builds one immutable onsite tensor.
There is no runtime inverse, dynamic division, projection, reset, callback or
external ODE solver. Only the ordinary Engine advances state.

Every tensor input u is a multiple of three; hence all six legal fixed-six
remainders remain retained unchanged. If x=(D,P), the actual update is

`x_next = multiplier * T_hom(x) - x_old`.

It contains the mandatory history subtraction. It is therefore **different**
from the rational target, despite sharing its polynomial numerator coefficients.
With D_old=P_old=0, its first decoded step equals the target and has C=0. On the
second step, both the target numerator and previous numerator individually lie
on the null cone, but their difference need not. More generally, writing
delta_hom=D^2 delta(P/D), the exact retained-numerator identity is

```
C(P_next) = multiplier^2 delta_hom^2 C(P)
            + C(P_old) - 2 multiplier N_hom^T J P_old.
```

The cross-history term remains when both individual constraints vanish. This is
the missing discrete identity a reversible lift must address.

For h=1/16, mu=1, D0=4 and strong constrained data (-1,0,2,1), the actual tensor
has 5 channels / 15 integers per node, 28 monomials, degree three and multiplier
67108864. Its fingerprint is
`e33be737ff30660efc4293c73e2ef4c715fdc08f22f73f288d4adbe2eecabb4c`.
All 27 nodes and all six carries are checked for three updates against an
independent scalar monomial/divmod oracle, each inverse, and complete rewind.
Peak retained bits are 34, 124 and 397. These are observed costs; there is no
general storage or denominator-positivity theorem for this new target lift.

The first constraint is exactly zero. At the second tick it is exactly

`-211805381883956703960796807492009984 / 6648074056234057895988554997906461158237804299242833919931086162572083201`,

approximately -3.185966e-38. An ordinary floating-point tolerance could hide
this failure; the audit compares exact rational integers and verifies the
cross-history identity. The third tick also fails. Complete rewind still passes.

## Compiler connection and remaining work

The native three-tick potential construction preserves its position coordinate
while kicking momentum. That is not a realization of the rational target above.
Its quadratic-force gate fits degree three; multiplying this cubic target by an
additional pulse would generically reach degree four. A fixed-six quotient
primitive likewise does not yet compute an arbitrary state-dependent W with
counted workspace and uncomputation. These are concrete interface obligations,
not a general impossibility theorem for reversible arithmetic.

Deleting/resetting the old slice would implement a different, noncompliant law.
Adding a numerical projection would also fail the stated contract. A successful
next construction must preserve an appropriate discrete gravity/matter identity
while retaining every old-state contribution, and must document all clocks,
workspace, spatial support and bit cost. The source problem is now given by
explicit cubic polynomials and an exact cross-history counterexample.

## Primary reading and issue coordination

Tapley, [On the preservation of second integrals by Runge-Kutta methods,
arXiv:2105.10929](https://arxiv.org/abs/2105.10929), §1 equations (2)-(3), §2:
the correct discrete target is a nonsingular cofactor identity for an invariant
zero set. A generic Runge-Kutta method does not universally inherit irreducible
quadratic Darboux invariants; the paper explicitly discusses special exceptions.
That general limitation is motivation, not a proof about this particular tensor.
The F, A, cubic-degree and cross-history identities above are derived directly
for this source and checked by the accompanying code.

[Research coordination](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810909516)
responds to the independent strong-source Euler defect, native compiler work and
cubic metric repair. All positive and negative results retain their separate
law fingerprints. General discrete Einstein constraints remain failed/open.
