# Compatible identities under the single-face contract

Base: PR #47, `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
This is a source-only identity audit, not a proposed replacement physical law.

```bash
python -m validation.synthesis.compatible_geometry --out runs/synthesis/compatible_geometry.json
```

## What the literature supplies

Desbrun, Hirani, Leok and Marsden, *Discrete Exterior Calculus* (2005),
[primary paper](https://arxiv.org/abs/math/0508341), sections 5 and 8,
construct the coboundary derivative and a discrete wedge product with a
Leibniz identity. The wedge is not ordinary collocated pointwise multiplication.
This supports testing a compatible calculus, not assuming the continuum
product rule for the existing centered point samples.

Braune, Tong, Gay-Balmaz and Desbrun, *A Discrete Exterior Calculus of
Bundle-valued Forms* (2025 version),
[primary paper](https://arxiv.org/abs/2406.05383), Proposition 5.3,
establish an exact discrete differential Bianchi identity for their transported
bundle-valued operators. Their simplicial connection/transport data and
averaging are additional construction requirements. The theorem does not
certify Universe24's current frame update or its channel/locality budget.

## Exact identity that fits

Let `delta_i = T_i - 1` on a periodic Cartesian node array. The translations
commute, so `delta_i delta_j = delta_j delta_i` and `div_delta curl_delta A=0`.
The audit checks these identities with rational spatially varying data, including
all periodic seams. This is the Cartesian incidence identity behind
boundary-of-boundary cancellation. It is independent of a metric.

A six-channel mechanical fixture demonstrates that the identity can survive
the actual mandatory update. Store three node components each of A and B:

```text
u_Ai = 6 b_Ai
u_Bi = 6 b_Bi + 3 (curl_delta b_A)_i
```

Prepare `a_A=b_A` and both B slices divergence free. For every carry `0<=r<6`,
the fixed-six quotient gives

```text
A_next = 2 A_current - A_previous
B_next = 2 B_current - B_previous + curl_delta A_current
r_next = r
```

Thus A is stationary in this prepared fixture and B's divergence obeys a
homogeneous two-slice recurrence. Zero divergence on both initial slices stays
zero. Every term is linear and on one face; there are 18 monomials, six channels
and 18 retained integers per node. No extra history or carry state is omitted.
The fields are **node components**, not geometrically extended edge/face gears;
the experiment therefore does not claim a complete DEC geometric allocation.

The actual Engine ran eight updates on 64 nodes, agreed at every retained
entry with the independent scalar oracle and rewound exactly. All six carries
were present. Divergence remained zero; maximum current-field integer length
was 12 bits. Flipping one curl orientation produced divergence 54 on the first
step. This is a six-channel independent control, not six channels appended to
the existing 44 (which would violate the cap).

## Product defects and an admissible algebraic correction

For centered difference `D_i=(T_i-T_i^-1)/(2h)`, the exact defect is

```text
D_i(fg) - f D_i g - g D_i f
 = [(f_+-f)(g_+-g) - (f_--f)(g_--g)] / (2h).
```

Each expanded numerator term uses only the target and one face neighbor.
The canonical numerator has six quadratic terms; multiplying it by a target
field still has degree at most three. Its integer-scale numerator passes the
strict Tensor support check. A rational coefficient `1/(2h)` is a passive
identity here: an evolving implementation still needs a proved integer
encoding, such as an admissible projective construction, rather than a new
runtime divisor.

The forward alternative is exactly
`delta_i(fg) = (T_i f) delta_i g + g delta_i f`.
Both identities were independently evaluated at all 125 nodes on all three
axes. Ordinary centered point-product defect reached `341/5`; subtracting the
displayed correction gave exactly zero. The 2,250 forward/centered derivative
commutator comparisons were all zero. The wrong-orientation rational curl
control gave nonzero divergence `1024/3`.

This connects to #47's already diagnosed momentum tangent defect. It gives
an implementable local polynomial *building block*, not permission to cancel
one residual by editing an equation without checking the other constraints.
A next candidate must derive a common discrete product/connection calculus,
recheck every H/M/torsion/gradient identity and conservation balance, and then
test full trajectories at fixed physical endpoints on held-out data.

## Where direct compilation fails

The Tensor validator rejects `f(x+e_i) g(x+e_j)` for distinct axes: the
complete monomial touches two different faces. It also rejects a diagonal
`f(x+e_i+e_j)` read. Direct plaquette transport/holonomy products therefore
cannot be inserted as same-step monomials under the current contract. The
commuting-derivative identity above may inspect a composed stencil as a
passive diagnostic; each Engine transition still uses only single-face terms.

Multi-step communication could assemble information causally, but every
retained intermediary and schedule would count toward the same 48 channels.
Neither the paper nor this audit supplies that compiler or a coupled nonlinear
Einstein replacement. General Einstein acceptance, matter/metric coupling,
operational apparatus and convergence remain unestablished.

The JSON result records executable/dependency hashes, exact rational outcomes,
the reproduction command and limitations. No production code was changed.
