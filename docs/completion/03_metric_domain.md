# Full-frame metric domain: an explicit cubic candidate

Status: source-only research. The original corrected massive45 tensor and this
cubic metric candidate are different immutable laws. Neither is an accepted
Einstein model. Run `python -m validation.completion.metric_domain`; fresh evidence
is written to `runs/completion/03_metric_domain.json`.

## 1. What must be preserved

The nine frame entries form a real matrix B; the inverse spatial metric is
`gamma_inverse = B^T B`. It is positive definite exactly when `det(B) != 0`.
Positive individual diagonal entries are insufficient: the matrix
`[[1,1,0],[1,1,0],[0,0,1]]` is singular despite having positive diagonal entries.
The previous protected diagonal-pair construction only proves the determinant
claim for a genuinely triangular frame. Retaining the full frame is necessary
for the presently proved all-direction principal-symbol result.

The six independent K entries form a symmetric matrix by construction; this is
an algebraic identity of the readout, not a constraint assumed approximately.
The original continuum frame equation is `B_dot = K B`, and hence
`det(B)(t) = det(B)(0) exp(integral tr(K) dt)` while the solution is regular.
This continuum identity does not automatically survive the retained integer step.

## 2. Exact failure of the original corrected45 tensor

Let h be the prepared step. Initialize all old numerators and the old denominator
to zero, current B=I, K=diag(-1/h,0,0), and connection and matter to zero, uniformly
on the periodic 3-cube. Every returned vacuum constraint is zero. In particular
`(tr K)^2 - tr(K^2) = 0`, and spatial/torsion derivatives vanish. The continuum
constraint additions therefore vanish too.

The first decoded projective step is exactly Euler:

`B_next = (I + h K) B = diag(0,1,1)`.

Thus the original full45 law destroys nondegeneracy even from vacuum constraint
initial data. The exact continuum solution in this sector is
`K00(t) = -1/(h+t)`, `B00(t) = h/(h+t)` with the other diagonal entries equal to
one. At t=h, the continuum value is 1/2, not zero; this is not a continuum
singularity. The audit uses the actual massive (`mass_squared=1`) compiled tensor,
all six carry values, an independent scalar integer oracle, and exact inversion.
Exact reversibility persists despite the failed metric readout.

## 3. A local cubic repair without extra channels

Replace only the prepared frame RHS by

`F_B^h = K B + h K^2 B`.

All K, connection, scalar, dust, Maxwell and potential RHS expressions are the
same as the massive corrected full-frame source. Compile the whole law at degree
three using the existing projective compiler. This adds onsite monomials of the
form `K_ab K_bc B_ci`; it adds no channel, no old-a read, no edge, no inverse and
no runtime branch. The degree is three, total retained channels remain 45, and
there are 135 retained integers per node. The ordinary Engine still uses exactly
`ell,r_next=divmod(2*u+r,6); a_next=b; b_next=ell-a` from one complete old snapshot.

Write the numerator matrix as P, and the shared denominator as D. The actual
compiled recurrence is

`D_next = C D^3 - D_old`,

`P_next = C (D^2 P + h D K_P P + h^2 K_P^2 P) - P_old`,

where C is the static positive coefficient-clearing integer, at least two, and
`K_P/D = K`. Every tensor contribution to u has a factor three, so every legal
carry in {0,...,5} stays unchanged. The displayed recurrence is exact, including
nonzero carries.

For current B=P/D, define

`R(K) = I + h K + h^2 K^2 = (hK + I/2)^2 + 3I/4`.

Since K is symmetric, `R >= 3I/4` for every real K, with no small-K assumption.
For positive D and D_old, the decoded frame recurrence is

`B_next = (1+epsilon) R B - epsilon B_old`,

`epsilon = D_old/(C D^3-D_old)`.

The first step has epsilon=0 and P_old=0, so its readout is `R B`; no physical
previous time slice is inferred from the zero memory boundary.

## 4. All-finite-tick determinant theorem

Assume the standard prepared memory boundary `P_old=0, D_old=0`, uniform integer
`D_0 >= 2`, `C >= 2`, arbitrary invertible B_0 at every node, and the stored
symmetric K representation. The other fields and their subsequent dynamics may
be arbitrary. The theorem does not require homogeneous geometry or vacuum.

First, `D_next = C D^3-D_old > D >= 2` follows inductively from `0 <= D_old < D`.
Therefore

`0 <= epsilon < 1/(C D^2-1) <= 1/7`.

Set X_0=0 for the memory-boundary step. For subsequent steps set
`X_n=B_(n-1) B_n^{-1}`. Suppose `||X_n||_2 <= 2`, and write

`A_n = (1+epsilon_n) R(K_n) - epsilon_n X_n`,

so `B_(n+1)=A_n B_n`. The singular-value perturbation inequality gives

`sigma_min(A_n) >= 3(1+epsilon_n)/4 - 2 epsilon_n`

`= 3/4 - 5 epsilon_n/4 >= 4/7 > 1/2`.

Thus A_n is invertible and
`||X_(n+1)||_2 = ||A_n^{-1}||_2 <= 7/4 < 2`, closing the induction. At the
initial step the stronger bound `sigma_min(A_0)>=3/4` holds. Moreover the path
`(1+epsilon_n) R(K_n) - s epsilon_n X_n`, 0<=s<=1, stays invertible by the same
bound. It starts positive definite, so `det(A_n)>0`. Consequently every finite
tick preserves the sign of det(B) and positive definiteness of `B^T B`.

Useful quantitative bounds, for n>=1, are

`sigma_min(B_n) >= (3/4)(4/7)^(n-1) sigma_min(B_0)`

and the simpler

`lambda_min(B_n^T B_n) >= 4^(-n) lambda_min(B_0^T B_0)`.

These are finite-step domain bounds, not uniform infinite-time conditioning.
No matrix inverse, singular-value computation or projection is used in Engine.
The code's exact rational matrix inverse and Sylvester minors are passive
certificates of the tested recurrence, never feedback.

The memory hypothesis matters. The audit constructs a legal retained state with
positive current B but an adversarial old numerator that cancels the next frame.
Its next determinant is zero and it still rewinds. The theorem deliberately does
not claim positivity for arbitrary old retained histories.

## 5. Finite-h provenance and continuum limits

The new term is algebraic and contains no derivative. Thus its exact principal
symbol contribution is zero at arbitrary fields and direction; the original
full-frame principal-symbol theorem remains the principal-symbol theorem of the
modified PDE as well. The coefficient is h, so the generating RHS tends to the
original source as h tends to zero on bounded fields. This establishes formal
first-order consistency only. It is not a convergence proof for the complete
retained map.

The correction is NOT a multiple of the Einstein/torsion constraints. The
original constraint-propagation equations cannot be copied onto the modified
finite-h tensor. For example, a spatially varying K produces an added frame
velocity `h K^2 B`, with an added derivative of that expression in the torsion
time derivative. This requires a separate discrete-constraint test, and the
original projective Euler scheme already has its own discrete defect.

There is an exact negative control, not merely an untested concern. At the
sourced homogeneous background B=I, K=-I, Pi_phi=2, dust_amplitude=1, choose a
transverse-traceless perturbation deltaK00=1, deltaK11=-1 with Fourier direction
(0,0,q). All 33 linear constraints and their original continuum time derivatives
vanish for this mode. The added velocity is deltaB_dot=-2h deltaK, while the
connection velocity is unchanged. The corrected constraint velocities are
`deltaC020_dot=2 i h q` and `deltaC121_dot=-2 i h q`. The audit checks these
identities exactly and includes the changed background contribution to C_dot.
Thus finite-h continuum constraint invariance for this cubic candidate fails;
the defect tends to zero with h on bounded smooth modes. This negative result
must accompany the positive metric-domain theorem.

The lower bound `4^(-n)` degenerates when n=T/h tends to infinity. A uniform
physical-time lower bound needs extra bounded-solution information. For
instance, if `||K||_2<=M`, h=1/m<=1 and C>=m^2 (true when the uncombined h^2
coefficient must be cleared), then `epsilon<=h^2/3`, and

`||A-I||_2 <= (1+epsilon)(hM+h^2 M^2)+3epsilon <= c h`,

with `c=4(M+M^2)/3+1`. If c h<=1/2 and n h<=T, then
`sigma_min(B_n)>=exp(-2cT) sigma_min(B_0)` follows from the product bound.
The required uniform K bound is not proved by this audit. The all-finite-tick
nondegeneracy theorem itself does not need that additional assumption.

## 6. Actual Engine controls and remaining gates

The executable test uses 27 nodes, four ticks, inhomogeneous rational full frames
with off-diagonal entries and nonzero matter. At every node/tick it checks the
exact decoded matrix recurrence, positive determinant, and positive leading
principal minors of `4I-X^T X`, which certify `||X||_2<2`. Every step is compared
to the independent scalar monomial/divmod oracle and inverted. All six remainders
are exercised; the complete final state rewinds to its seed. The JSON records the
exact tensor fingerprint, C, monomial count and actual integer bit sizes.

These fixtures are not claimed to solve the Einstein constraints. No retained
clock/probe is added; three slots remain unused. Time stability, discrete
Einstein/Noether closure, convergence, operational geodesic motion and efficient
integer storage remain separate gates. Degree-three projective denominator
bits grow at least as fast as a constant times 3^n; this repair worsens that cost
relative to degree two. The production runtime and accepted-model status are
unchanged.

## 7. Primary reading and alternatives

- [Iserles, Munthe-Kaas, Norsett and Zanna, Lie-group methods, Acta Numerica 9
  (2000)](https://sites.math.rutgers.edu/courses/549/Lie_methods.pdf), §§2.5 and 8:
  matrix flows and preserving group structure during discretization.
- [Drumetz et al., arXiv:2210.08842v5](https://arxiv.org/pdf/2210.08842), §4.1:
  invertible-matrix congruence preserves symmetric positive definiteness, with
  infinitesimal action `MP+PM^T`.

These papers motivate preserving the matrix domain rather than testing diagonal
entries. They do not supply the polynomial/history invariant above; that is the
explicit derivation in this report. Exact exponential or Cayley updates would
require additional compilation work under the degree-three, old-snapshot and
state restrictions. We make no impossibility claim against such alternatives.
The polynomial construction already fits the current 45-channel allocation.

Coordination and initial derivation:
[issue #40 comment](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810759402).
