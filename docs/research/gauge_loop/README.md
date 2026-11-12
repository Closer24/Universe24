# Finite gauge loops and retained connection exchange

This implements the experiments tracked in [issue 66](https://github.com/Closer24/Universe24/issues/66)
against main `b8a064a9b0cccb1218445578d8765642572b40a7`.
The existing six-channel transported-overlap control proved a static algebraic
identity. This work adds an actual square-loop intervention and a separate
group-valued dynamical connection construction. Both execute through the
unchanged fixed-six Engine and the supported saved-run runtime.

| Construction | Counted channels | Established scope | Explicit boundary |
| --- | ---: | --- | --- |
| Static local Z4 transport | 7 | Two-path interference, independent plaquette flux, complete-state gauge covariance, neutral retained intensity readout | Prepared stationary links; one-way reader; unstable homogeneous matter mode |
| Dynamic local Z2 exchange | 10 | Unit sign links, evolving invariant plaquettes, complete-history charged-register/link feedback, exact invariant preparation | Period divides three; no propagating matter, electric field or Gauss law |
| Historical countercontrols | Separately hashed tensors | Reproduce link-norm, bare-charge, locality and raw-click interpretation failures | Do not transfer those failures indiscriminately to other encodings |

These are **two different immutable laws**. Their successful rows do not
establish one combined dynamical wave/field system. Neither is QED, a Maxwell
solver, an Einstein source, an operational clock or a Born detector. No
production model selector, default, Engine callback or new decoder is added.

## Static square-loop construction

The seven registers are complex matter `(phi,chi)`, complex links on the
positive x/y faces (four registers), and a neutral reader. Each register has
its full `(a,b,r)`, so the allocation is 21 integers per node. Links include
their physical endpoints in the strict-support check.

Let `U_k(x)` transport from `x+e_k` to `x`. The integer covariant adjacency is

\[
(H_U\psi)_x=\sum_{k=x,y}
 [U_k(x)\psi_{x+e_k}+U_k(x-e_k)^*\psi_{x-e_k}].
\]

The matter input is `u=3 H_U b`, the link input is `u=6b`, and the neutral
reader input is `u=3(phi^2+chi^2)`. Thus the exact recurrences are

\[
\psi_{n+1}=H_U\psi_n-\psi_{n-1},\qquad
U_{n+1}=2U_n-U_{n-1},\qquad
\ell_{reader}=|\psi_n|^2.
\]

All coefficients are multiples of three, so every legal carry remains
unchanged. The prepared link domain has `a=b` and each complex link in
`{1,i,-1,-i}`; it is invariant for all updates. Matter and reader histories
may be arbitrary exact integers. Domain validation rejects malformed or
nonstationary links; it never repairs them during a run. There are 22
monomials, degree at most two, with no strict physical-support violations.

For independent node phases `g_x in Z4`, transform matter by `g_x`, and links
by `g_x U_xy g_y^-1`. Apply the signed permutation to **both** histories.
A negative component also sends `r -> 5-r`. The neutral reader is unchanged.
The tensor source is equivariant under this action. Since

\[
-2u+5-r=6(-\ell)+(5-r'),
\]

the same transformation commutes with the complete Engine update, including
nonzero carries. Only time-independent residual local transformations are
claimed; arbitrary time-dependent gauges require temporal transport or a
separately justified gauge-fixed constraint treatment.

The passive xy plaquette is

\[
W(x)=U_x(x)U_y(x+e_x)U_x(x+e_y)^*U_y(x)^*.
\]

Its gauge factors cancel. This multi-edge expression is an offline readout,
never an input monomial. A pure endpoint connection `U_xy=g_x g_y^-1` has
`W=1`; independently prepared flux cannot be removed by node rephasing.

On a periodic cube with side at least five, put a matter impulse at the
origin, zero previous matter history, and change the y link based at `(1,0,0)`
from `1` to `w=+1` or `-1`. At `(1,1,0)`, exactly two length-two paths arrive.
The amplitude at update two is `1+w`, so its intensity is four or zero.
The retained neutral reader reports that value as its quotient on update
three. This is an algebraic intensity, not a binary detection probability.
Changing one edge on a periodic board also changes an adjacent plaquette;
no isolated flux or monopole claim is made.

The collector saves both flux preparations and their complete local gauge
copies. It checks the actual saved histories, all neutral intensities,
all reader quotients, fixed plaquettes, scalar replay and inverse. Raw event
identities are run-specific and are not equated across different bundles.

### Stability countercontrol

The uniform matter mode obeys `q_next=4q-q_previous`. Starting with both
histories one gives `1,3,11,41`; its characteristic roots are `2 +/- sqrt(3)`.
The growing root exceeds one. The four-step interference control therefore
does **not** establish a stable wave equation or a conserved probability
norm. The growth witness is executable and reported as a failed stability
claim. Integer growth is reported, not normalized away.

## Dynamic group-valued connection construction

The ten channels are one stationary charged reference `y` and, on each
positive x/y/z edge, two charged registers `chi,eta` at its base and one
link sign `U`. All current values lie in `{-1,+1}`. This counts 30 retained
integers per node, with no external link bank.

Writing `Y=y(x+e_k)`, define the first-order map

\[
F(\chi,\eta,U)=(\eta,UY,\chi Y),\quad
F^{-1}(\chi,\eta,U)=(UY,\chi,\eta Y),\quad y'=y.
\]

The tuple `(chi,eta,U*Y)` undergoes a literal three-cycle, so `F^3=id`.
Prepare the **complete** history `a=F^-1(b)` and any legal carries. Compile
the polynomial input `u=3(F(b)+F^-1(b))`. Rule3 then yields

\[
b'=F(b)+F^{-1}(b)-a=F(b),\quad a'=b=F^{-1}(b'),\quad r'=r.
\]

This proves the preparation domain invariant for all updates, with exact
group-valued links and a complete period dividing three. The source has
degree two and strict single-edge support. The stationary neighbor reference
is retained and counted; it is not an externally supplied clock or field.

The local Z2 action multiplies `y,chi,eta` by `g_x`, and `U_xy` by `g_x g_y`.
Its complete-history/carry lift commutes with the tensor. Covariance also
holds on arbitrary integer complete states; unit-link preservation and the
period-three claim require the explicitly checked preparation domain.

The feedback experiment changes only complete charged-register histories,
while matching every initial link `(a,b,r)` and reference register. A link
and invariant plaquette change at update one; a different charged register
responds at update two. A separately identified frozen-link tensor removes
that delayed response. A direct link-only intervention additionally checks
the Engine dependency but lies outside the prepared first-order sector; it
is not used to claim domain preservation.

Evolving information stays within each base/axis triplet. There is no
transport of evolving signals across successive edges. Changing Wilson
plaquettes is consequently insufficient evidence of Maxwell propagation.
There is no retained electric conjugate, derived Gauss charge, energy-stress
law, shared metric or material clock. Period-three recurrence also excludes
indefinite strict growth of any state-defined complexity on this domain.

## Preserved falsifiers

`obstructions.py` runs the historical builders directly:

- Two normalized complex-link histories `1,i` can evolve to `-1+2i`, with
  norm squared five. Exact inversion does not preserve the unit manifold.
- The historical displayed Gauss charge changes `0 -> -6` while its
  carry-aware balance has zero residual. No replacement conserved physical
  charge is silently introduced.
- The existing integer actions contain 4 Gaussian units, 8 quaternion units,
  and 96 determinant-one monomial matrices. These are finite groups. This
  is not a universal obstruction to rational or emergent encodings.
- The historical 20-channel two-path tensor has 120 strict physical-support
  violations. The strict constructor rejects it. Several legal steps may
  still transport loop information; no general locality no-go is inferred.
- An actual locally gauge-related Engine pair exchanges raw C1 and C2
  labels while preserving gauge-invariant diagnostics and full covariance.
  A neutral or apparatus-relative outcome remains possible. Charged-channel
  C2 alone is not a gauge-invariant physical selection criterion.

The audits mark these physical claims **failed**, even when reproducing the
counterexample makes the software test pass.

## Reproduction and acceptance

```sh
python -m unittest universe24.tests.test_gauge_loop -v
python -m validation.gauge_loop.audit --out runs/gauge-loop
python -m universe24 verify --run runs/gauge-loop/static/positive
python -m universe24 verify --run runs/gauge-loop/dynamic
```

Use a fresh output directory. `report.json` binds source hashes, separate
tensor/bundle/run identities, exact saved-trace hashes, bit growth and scope.
The collector compares all saved transitions against the independent scalar
Rule3 evaluator and keeps both constructions distinct. The regression suite
adds a separately expanded complex-adjacency oracle, signed large integers,
all carry classes, malformed-domain rejection and rehashed trace corruption.
CI exports complete bundles, histories and canonical clicks on Python 3.11
and 3.12. Its success does not pass the generic physical acceptance gates.

### Executed focused evidence

The 19 focused regression tests pass. The collector independently compares
46,860 saved register outputs (42,000 static and 4,860 dynamic) with scalar
Rule3 calculations. The dynamic audit additionally checks 108 prepared
transitions and 120 covariance cases, including those same 108 cases; these
counts overlap and are not independent samples. Its local truth table covers
all 16 sign assignments. All six carry classes and signed large-integer
controls are included.

The committed [evidence snapshot](evidence.json) records the exact source
hashes and every scoped result. Fresh complete histories are produced under
`runs/` and exported by CI. The largest retained values in the four-step
static fixtures use six bits; the prepared dynamic sector uses at most
three bits including carries. Arbitrary-state covariance stress tests use
much larger integers and are outside the normalized dynamic domain.

Next physical obligations are a **single** bounded, propagating, reciprocal
wave/link law; its electric/Gauss and energy accounts; controlled U(1)/Maxwell
limits; and coupling to the same metric and operational apparatus. These
remain unestablished rather than being inferred by combining this table's
different laws.

## Physics references and boundary

- [Wilson, Confinement of quarks](https://doi.org/10.1103/PhysRevD.10.2445):
  link variables and gauge-invariant lattice loops.
- [Kogut and Susskind, Hamiltonian formulation of Wilson's lattice gauge theories](https://doi.org/10.1103/PhysRevD.11.395):
  additional electric and Hamiltonian structure absent from the finite cycle.
- [Tong, Lattice Gauge Theory, section 4.2](https://davidtong.org/pdfs/teaching/gauge-theory/gauge4.pdf):
  transporters, plaquettes and the Wilson action.

These references motivate the comparison/loop tests. None proves the
project-specific integer tensor implements their physical theory.
