# Exact global sectors cannot be entered from outside

This is a scope corollary of **M11**, not an additional native experiment or a
new claim-register entry. The [frozen invariant-family proof](invariant_families_algebra.md),
the [48-case evidence](../invariant_families_v1/results.md) and all original
protocols remain unchanged. The fundamental rule is still `num=den=1`.

## The reduced recurrence is bijective

Let `S = Z × Z × {0,1,2,3,4,5}`. For an integer eigenvalue `lambda`, the reduced
map is

```text
ell, R = divmod(2*lambda*b + r, 6)
Phi_lambda(a,b,r) = (b, ell-a, R).
```

For any proposed output `(A,B,R)` in `S`, its unique predecessor is

```text
r = (R - 2*lambda*A) mod 6
ell = (2*lambda*A + r - R) / 6
(a,b) = (ell-B, A).
```

Here `mod 6` selects the unique remainder in `0..5`. The numerator defining
`ell` is divisible by six, and `2*lambda*A+r = 6*ell+R` with `R` in `0..5` is
exactly the required Euclidean division. Substitution recovers the output.
Thus `Phi_lambda` is a bijection on the entire declared scalar state space.

## Consequence for the complete board

Fix one nonzero ternary eigenpattern `v` with `Fv=lambda*v`. Let `E_beta` be the
M11 signed encoding, with a fixed valid remainder assignment `beta` at every
zero-pattern address. The registered examples use remainder 2 there; any fixed
valid zero-address remainder remains unchanged when its counters and total
input are zero. Write `M_beta = E_beta(S)` for this exact **full-board** sector,
including every counter and remainder. The encoding is injective because `v`
has a nonzero entry.

The proved intertwining identity is

```text
W E_beta = E_beta Phi_lambda.
```

Surjectivity of `Phi_lambda` gives `W(M_beta)=M_beta`. Since the native full-state
map `W` is bijective, a state in `M_beta` cannot also have a predecessor outside
it. Therefore

```text
W(M_beta) = M_beta = W^(-1)(M_beta).
```

For every finite number of updates, a full state initially outside this exact
global sector cannot enter it. The same statement holds for the union over
all valid fixed zero-address assignments `beta`, because each constituent
sector is invariant in both directions.

## What this does and does not exclude

These exact globally encoded families cannot first form from an outside full
state under this autonomous reversible evolution. Their native demonstrations
start inside the family and establish its closure and reduced behavior.

This does **not** exclude a local pattern forming within a larger evolving
board, an approximate pattern, or a coarse observation becoming regular while
distinguishing information remains elsewhere. Such a condition is not equality
to the full-board sector `M_beta`. It requires its own preparation, observation
and persistence tests; the present corollary supplies no formation mechanism.
