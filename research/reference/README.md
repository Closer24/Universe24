# Independent exact reference

This research-only oracle imports no `universe24` code. It is an independent
implementation of the **same specification**, not an alternative physical law.
`algebra.py` uses generic 4x4 matrix products over rational polynomials modulo
x²−2, with `fractions.Fraction`. A closed-form set of 48 unit-quaternion matrices
(8 units, 16 half-coordinate vectors and 24 paired √2/2-coordinate vectors)
is checked against generator closure. BFS order Cx then Cy establishes the
specified labels independently. Rotations follow by matrix conjugation and
couplings by the stated body actions. No production table is used as an oracle.

`evolution.py` uses complete dense tuples and gather updates, unlike the
production sparse scatter executor. Matrix arithmetic is construction-time only.
Exact scalar updates and inverse reconstruction are independently written.
The same specification and Python integer arithmetic are shared assumptions;
agreement cannot prove the specification physically correct or rule out every
shared conceptual error.

API from `research.reference`:

- `algebra()`: immutable `matrices`, `multiplication`, `inverses`, `rotations`,
  `central` fields.
- `coupling(signs)`: independently constructed immutable `ports` and `weights`.
- `addresses(L)`, `index(address,L)`, `flatten(mapping,L,background=(0,0,2))`.
- `forward((a,b,r),u)` and `inverse((a,b,r),u)` for valid integer states.
- `advance(dense,L,signs=(1,1,1))`, `rewind(dense,L,signs=(1,1,1))`.

Dense data is a tuple of all 48L³ triples; its flat index is
`(((x*L+y)*L+z)*48+g)`. Inputs must contain valid integer triples with r in 0..5;
this trusted research API is not a replacement for production input validation.
Optional `order=` is a permutation of all flat indices used only to test
old-snapshot independence. There is no state mutation or runtime coupling change.
