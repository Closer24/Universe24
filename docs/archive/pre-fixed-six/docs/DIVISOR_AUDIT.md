# When the common divisor scale can be removed

The scalar law is `ell,r_next=divmod(2*u+r,6*Q)`, followed by
`a_next=b` and `b_next=ell-a`. `Q` is a positive integer construction
parameter, not a derived physical constant or a fractional register.

Changing `Q` alone changes this law. For the same input `u=4`, the same
two-time values `a=b=0`, and the same remainder `r=0`:

| Q | Divisor | New b | New remainder |
| ---: | ---: | ---: | ---: |
| 1 | 6 | 1 | 2 |
| 2 | 12 | 0 | 8 |

The engine test `test_changing_Q_alone_changes_the_law` executes both cases
and checks their inverse. Replacing the name `Q` by `D` would keep the same
choice of divisor; it would not remove that mathematical input.

## Exact reduction when there is a common factor

Suppose every integer coefficient of the input tensor is divisible by `Q`,
so `u=Q*v`. Write each retained remainder uniquely as

    r = Q*rho + kappa,       0 <= rho < 6,       0 <= kappa < Q.

Then the exact Euclidean-division identity is

    divmod(2*Q*v + Q*rho + kappa, 6*Q)
      = (ell, Q*rho_next + kappa),
    (ell, rho_next) = divmod(2*v + rho, 6).

Thus a divisor-six model with divided tensor coefficients has the same
`a,b` history. The low remainder digit `kappa` stays fixed. To reconstruct
the complete original state, it must be retained as part of the preparation,
or one fixed sector must be declared. Simply dropping it identifies distinct
complete states. The official quotients and click classes also agree under
this encoding, since the remainder increments scale with the divisor and
the complete-triple change condition is preserved.

This termwise divisibility condition is sufficient for that direct integer
tensor reduction. Special invariant-state encodings may allow other
reductions, but they require their own proof. No such reduction of the full
default model is established by this audit.

## Result for the current constructions

| Construction | Q | Live monomials | Coefficients not divisible by Q |
| --- | ---: | ---: | ---: |
| Default `one_system()` | 8,589,934,593 | 18,592 | 18,568 |
| Local Palatini pp-wave experiment | 1 | 93 | 0 |
| Prepared geodesic/clock experiment | 1 | 98 | 0 |

The greatest common divisor of all default coefficients is one. Consequently
there is no shared integer factor to cancel between its complete coefficient
template and `Q`. For example, one coefficient is `Q-1=8,589,934,592`.
Dividing it by `Q` would require a noninteger coefficient, contrary to the
model contract. Rounding that division or simply changing the divisor would
define a different law.

The two new experiments already fix `Q=1` in their tensor definitions. Their
run functions expose no adjustable `Q` argument. The redundant explicit
second argument in `Engine(tensor,1)` was removed; they now use
`Engine(tensor)`, whose existing default is one. The tensor's `Q=1` declaration
is retained as validation/provenance, and the complete recorded histories
remain identical. The common engine and default model are unchanged.

The arithmetic checks, including nonlinear terms, staged old-history reads,
nonzero low remainder digits, official events and exact rewind, are
reproducible with:

```sh
python -m unittest universe24.tests.test_resolution -v
```

This audit establishes a role for the divisor in the current arithmetic.
It supplies no evidence that its default numerical value is physically
necessary or that a future model cannot be constructed entirely at `Q=1`.
