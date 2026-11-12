# Reciprocal matter–apparatus control

Base: PR #47, `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
This is an isolated exact algebra/Engine control, not a new installed universe,
not a modification of the 44-channel geometry, and not an accepted detector.

## Question and result

Can a source and receiver exchange information reciprocally through one face,
with exact charge-like accounting, while preserving Rule3 and the channel cap?
Yes for the restricted construction below. Can exact reversal or reciprocity
then establish physical stress-energy conservation? No: explicit energy
counterexamples remain even in this small control.

The concurrent four-slot intensity readout in issue #45 is a declared one-way
test apparatus. It preserves the source's projection by design. That is useful
for observation, but cannot establish a closed source-plus-apparatus physical
balance. The present control supplies a concrete reciprocal alternative to
study, not a silent change to that team's interface.

## Primary source and inference boundary

Marsden and West, *Discrete mechanics and variational integrators*, Acta
Numerica 10 (2001), 357–514, [author-hosted full text](https://lagrange.mechse.illinois.edu/pubs/MaWe2001/MaWe2001.pdf),
Theorem 1.3.3 and sections 3.2.3 and 4.3.6, connect a discrete action's symmetry
to its discrete momentum map, including the effect of forces. Their extended
energy discussion requires the appropriate time equations; it does not grant
exact continuous energy conservation to every fixed-step variational map.
These portions were inspected. The source motivates checking the correct
two-time invariant and accounting for reciprocal forces. The formulas and
integer tests below are our separately derived restricted construction, not
a published theorem about Universe24 or Einstein gravity.

## Law, allocation and exact identities

Let two real carrier components form `z(x)` and two receiver components form
`w(x)`. Pair `z(x)` with `w(x+e1)` and let

\[
d_x=z_x-w_{x+e_1},\qquad
V=\sum_x\left(\frac{|d_x|^2}{2}+\frac{\lambda|d_x|^4}{4}\right),
\quad \lambda\in\{0,1\}.
\]

For the complete vector of both species choose

\[
u=3(2b-\nabla V(b)),\qquad c=2b-a-\nabla V(b).
\]

The unchanged fixed-six engine gives `(a,b,r)->(b,c,r)` for **every**
`r=0,...,5`; inverse recovery is `a=2b-grad V(b)-c`. The source force is
`-(1+lambda |d|²)d`, and its paired receiver force is its negative.
The linear tensor has 8 monomials of degree 1; the nonlinear tensor has
48 monomials of degree at most 3. Every complete monomial support lies on one
physical face. There are four audit channels, 12 retained integers per node,
no scheduler, no hidden state, no old-a reads and no normalization.

The discrete action `Ld(a,b)=|b-a|²/2−V(b)` gives the same recurrence.
Define the passive two-time quantities

\[
P=\sum_x[(b_z-a_z)+(b_w-a_w)],\qquad
J=\sum_x[a_z\mathbin\times b_z+a_w\mathbin\times b_w].
\]

Pairwise force cancellation proves `Delta P=0`. Also
`Delta J=sum b cross force`; each edge contributes
`-(1+lambda |d|²)(z-w) cross d=0`. Thus `J` is exactly conserved even for
the cubic force. This is a global internal rotation/phase invariant of the
real polynomial extension and its integer trajectories, not a proof of
local gauge symmetry. `P` is an internal configuration-translation invariant,
**not established physical spacetime momentum**.

For `lambda=0` there is an additional exact polarized invariant

\[
E_{pol}=\|b-a\|^2+\sum_x(a_z-a_{w+})\cdot(b_z-b_{w+}).
\]

Writing the quadratic form as `L=L^T` gives
`c+a=(2I-L)b`. Factoring `E_pol(b,c)-E_pol(a,b)` then gives zero.
This does not identify `E_pol` with the energy density that sources Einstein
equations. In particular the naive point expression
`E_point=|b-a|²/2+V(b)` is not conserved. Cubic reciprocity does not preserve
the quadratic polarized formula either.

## Executed evidence

Run from the source root:

```bash
python -m validation.synthesis.matter_backreaction --out runs/synthesis/matter_backreaction.json
```

The JSON contains the source revision, source SHA-256 values, raw defects,
small counterexamples, command and scope. Results:

| Control | Exact result |
| --- | --- |
| Signed old/current pair values in `{-1,0,1}`, both potentials, all six carries | 78,732 scalar cases passed |
| Actual Engine on 27 nodes, both potentials, reciprocal/one-way controls, six carry preparations, 3 updates | 72 complete transitions matched independent scalar oracle and exact inverse |
| Full rewind including nonzero remainders | Passed |
| Reciprocal linear and cubic tensors | Reciprocity checker passed; `Delta J=Delta P=0` |
| One-way controls with source force removed | Reciprocity checker failed; nonzero charge and internal momentum defects |
| Linear reciprocal `E_pol` | Exact zero defect |
| Naive point energy | Nonzero defect in every variant |
| Largest stored integer | Linear reciprocal 123 bits; cubic reciprocal 3,280 bits after 3 updates from a 121-bit preparation |

For a transparent single-pair negative control, prepare both old and current
`z=(1,0), w=(0,1)`. The reciprocal linear step swaps them: `J:0->0` and
`E_pol:2->2`, while `E_point:1->3`. Removing the source force gives
`z_next=(1,0), w_next=(1,0)` and `J:0->-1`. With the reciprocal cubic force,
`J:0->0` but `E_point:2->668` and `E_pol:2->26`. These are retained failures,
not checks to be weakened or relabelled physical success.

## Integration handoff and falsifying gate

Potential ledger: reuse the two carrier components and allocate two receiver
components, giving **44+2=46** channels. This is a proposed alternative to the
other team's four-slot intensity allocation, not an additional appendage.
The remaining two slots are not automatically sufficient for calibration,
gauge links or scheduling. All such state must still be counted.

The carrier in PR #47 is projectively decoded. Its existing first-order
geometry/matter recurrence is not this raw second-order oscillator. Therefore
adding the tested monomials directly to its numerators has **not** been shown
to realize the same physical interaction. A valid next change must derive the
common-denominator compilation, reciprocal matter/apparatus stress, and the
same metric's clock response; preserve the existing constraints/counterexamples;
then demonstrate full-state oracle/replay and refined physical balances.
Single fixed-face pairing also does not constitute a three-dimensional
transport network. No detector, proper-time, Born, Bell, Einstein or
complexity-growth gate is closed by this control.
