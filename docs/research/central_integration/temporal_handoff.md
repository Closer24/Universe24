# Temporal integration handoff

This review pins the completion source to
`8c53e69f4b466dcbd2da7dab7e3c365bd9731766` (PR #52), inspected in integration
commit `90bd7c59d4ec4aa3f934f4b66f1be554861e4a2e`. It changes no physical law
and supplies no accepted Einstein model.

## The specific obstruction

`validation/completion/constraint_closure.py` constructs the rational target
for the homogeneous four-vector `z=(k,p,phi,dust)` with

\[
C(z)=z^T Jz,\qquad J=\operatorname{diag}(6,-1,-\mu,-2).
\]

The continuous equations obey `Cdot=6*k*C`. The Cayley target preserves the
zero constraint exactly on its stated denominator domain. The actual Rule3
compiler, however, implements `b_next=M*N(b)-a`, rather than overwriting `b`
with that target. The projective denominator does not remove this subtraction.

There is a restricted obstruction stronger than the single saved counterexample.
For any independently null numerator `N`, old physical vector `a`, and nonzero multiplier `M`,

\[
C(MN-a)=M^2 C(N)+C(a)-2M N^TJa=-2M N^TJa.
\]

For positive mass squared `mu>0`, nonzero real null vectors of this Lorentzian
form are orthogonal only when they are collinear. To see this, rescale their
coordinates to `(sqrt(6)*k,p,sqrt(mu)*phi,sqrt(2)*dust)`; nullness gives
`|spatial|=|time|`, and orthogonality saturates the Euclidean Cauchy–Schwarz
inequality. Thus this **specific independently-null-target-minus-null-history
ansatz** can stay on `C=0` only when the target and old physical slice are
collinear (or one is zero). Generic changing scalar phase violates that
condition. Replacing Euler with another independently constraint-preserving
one-step target does not by itself repair this lift.

This is not a no-go theorem for Rule3, for complete-state observables, for
multi-tick encodings, for signed/zero mass squared, or for general Einstein
discretizations. The theorem is conditional on both numerator and old slice
being null and on the displayed subtraction ansatz. It does not assume every
possible physical constraint must be a function of `b` alone.

## Independently rerun evidence

On the pinned completion source, the review ran `algebra_audit()`,
`history_audit()` and `native_compiler.joint_nonlinear_audit()` locally.

| Check | Result |
|---|---|
| Continuous identity, Cayley identity, first-order consistency | Passed symbolically |
| Five-channel history lift, all six remainders, oracle and full rewind | Passed mechanically |
| History lift first tick constraint | Exactly zero |
| History lift second tick constraint | Nonzero, about `-3.185966042080138e-38` |
| History lift peak retained bits, ticks 1/2/3 | `34 / 124 / 397` |
| Seven-channel nonlinear compiler | Ten signed-coupling/workspace cases passed |
| Compiler scope | 54 microticks per case, 216 nodes, exact inverse and restored workspace/scheduler |
| Compiler maximum peak bits across cases | 194 |

The five-channel tensor fingerprint is
`e33be737ff30660efc4293c73e2ef4c715fdc08f22f73f288d4adbe2eecabb4c`.
The unit-coupling seven-channel fingerprint is
`e35d2691856235e6124dfc21172498c75a454a9b049cc70f75f54563f00dc2af`.
The latter implements the finite macro map
`S*=S+floor(P/18); P'=P+2*F(S*); S'=S*` on prepared workspace residues,
with `S=a+b`, `P=6*a+r`. It is not an Einstein or arbitrary-refinement compiler.

An additional independent SymPy check expanded the generic cross-history
identity above. For the strong seed `(-1,0,2,1)`, `mu=1`, `h=1/16`, two rational
Cayley target applications each had exactly zero constraint, but the inner
product of the second target with the initial seed was exactly

```
24657391696697648610081152 / 600327258027381476283936025
```

All six pairwise collinearity minors were nonzero. This is an exact witness
for the restricted obstruction, separate from the actual Engine counterexample.
No new full-repository test run is claimed by this review.

The exact witness is reproducible with only Python's standard library:

```python
from fractions import Fraction as F

def C(z):
    k, p, f, d = z
    return 6*k*k-p*p-f*f-2*d*d

def target(z):
    k, p, f, d = z
    h = F(1, 16)
    generator = [[0, 0, -f/2, -d/2], [0, 0, -1, 0],
                 [-3*f, 1, 0, 0], [-3*d/2, 0, 0, 0]]
    rhs = [z[i]+h/2*sum(generator[i][j]*z[j] for j in range(4))
           for i in range(4)]
    rows = [[F(i == j)-h/2*generator[i][j] for j in range(4)]
            + [rhs[i]] for i in range(4)]
    for col in range(4):
        pivot = next(i for i in range(col, 4) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v/scale for v in rows[col]]
        for i in range(4):
            if i != col:
                scale = rows[i][col]
                rows[i] = [v-scale*w for v, w in zip(rows[i], rows[col])]
    return tuple(row[-1]/(1-3*h*k) for row in rows)

old = tuple(map(F, (-1, 0, 2, 1)))
first = target(old)
second = target(first)
inner = sum(F(w)*x*y for w, x, y in zip((6, -1, -1, -2), second, old))
assert C(old) == C(first) == C(second) == 0
assert inner == F(24657391696697648610081152, 600327258027381476283936025)
assert C(tuple(x-y for x, y in zip(second, old))) == -2*inner != 0
print(inner)
```

This solver is only a standard-library certificate for the mathematical
target, never a runtime callback or proposed Engine implementation. The
displayed difference uses multiplier one to expose the bilinear identity;
it does not claim to reproduce the actual lifted tensor's integer scaling.
The actual tensor's counterexample is independently rerun with
`python -m validation.completion.constraint_closure`.

## Concrete next implementation boundary

Use the independently verified homogeneous reduction as the small physics
fixture, and develop a **complete-state macro map** against it. Do not append
the independent seven-channel compiler to the 45-channel tensor: that counts
52 channels and does not create a coupling. Extending its current two-data,
two-work, three-scheduler layout naively to 44 data channels counts 91.

The next candidate must specify its decoded geometry, scalar phase, momentum
and dust from the retained `(a,b,r)`, its static microtick schedule, and the
full state inverse before a physical success claim. The native compiler is a
useful exact arithmetic primitive; its potential force and floor drift are not
the reduced Einstein equations. In particular, variable-denominator arithmetic,
degree-three forces gated by a clock, and arbitrary temporal refinement remain
unimplemented interfaces.

Acceptance for a candidate handoff:

1. Publish one immutable tensor, exact seed, passive decode and source hash;
   count all physical, work and scheduler channels together, at most 48.
2. Prove or check the macro oracle on complete states, including negative data
   and all allowed remainder classes. Check each microtick against the scalar
   oracle and inverse, then rewind the whole run. A selected workspace residue
   is an explicit preparation condition, not a discarded integer.
3. Reproduce the existing Euler and tick-two history failures unchanged as
   negative controls. A tiny nonzero rational is not exact constraint closure.
4. For a claimed exact closure, derive the actual decoded macro constraint
   identity and check at least three consecutive nontrivial macro updates.
   For an approximation claim, preregister a fixed-time refinement envelope
   instead; do not replace it afterward with a favorable residual threshold.
5. Compare the same decoded field trajectory against the reduced continuous
   equations at three temporal resolutions with a strictly tighter independent
   reference. Report denominator-domain failures and retained-bit cost.
6. Only after this reduced test passes, provide the spatial/full-frame lift
   and its complete allocation. The reduced result alone does not certify
   general Einstein evolution, operational apparatus, Born probabilities or
   stable complexity growth.

The actionable change in direction is to include mandatory memory and residue
semantics when designing the physical update, before compiling its numerator.
The missing artifact is that complete-state physical macro map; another
first-order constrained rational formula alone does not supply it.
