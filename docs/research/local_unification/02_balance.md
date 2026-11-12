# A positive kinetic account for the same carrier–record collision

This report concerns `validation/local_unification/native.py` and its single
eight-channel paired-bank tensor. It is not a balance imported from a separate
successful model. `balance.py` implements a literal independent collision
table, complete-state oracle, node/region ledgers and wrong-state controls.

## Collision, information and physical recoil

In one four-rail bank let `(a,b,c,d)` mean record+, record−, carrier+, carrier−.
Each occupied rail is assigned one unit of massless lattice-ray energy and
directional momentum `+1` or `−1`. These are an explicit discrete kinetic
interpretation, not derived SI units or a proof of continuous Lorentz symmetry.

Define

\[
\delta=ad(1-b-c)-bc(1-a-d),\qquad
G(a,b,c,d)=(a-\delta,b+\delta,c+\delta,d-\delta).
\]

The difference between the two exclusive quartic event indicators cancels
their equal quartic term. The resulting polynomial is cubic. Enumerating the
16 Boolean inputs proves that `G` exchanges `1001` and `0110` and fixes every
other state. It is therefore an involution on the full Boolean domain.

Direct substitution gives four invariant counts, three linearly independent:

\[
a+c,\quad b+d,\quad a+b,\quad c+d.
\]

Thus positive total energy `E=a+b+c+d` and signed momentum `P=a+c-b-d` are
preserved, with `E >= |P|`. Record and carrier particle numbers are individually
preserved. The species momenta exchange

\[
\Delta P_{\rm carrier}=2\delta,\qquad
\Delta P_{\rm record}=-2\delta.
\]

A right-moving ready record and left-moving carrier (`1001`) produce a
left-moving used record and right-moving carrier (`0110`). The record supplies
the actual equal-opposite recoil. It is not a zero-momentum bit reset or an
unbounded signed compensation counter. An absent or double carrier is not
converted to a single apparent detection. Used records can return and undo a
later sorting event; finite supply and periodic recurrence remain explicit.

The two distinct single-carrier inputs with a ready record produce the same
preferred outgoing carrier, but different outgoing records. This is the
recoverable provenance required by injectivity. No energy-per-bit theorem is
claimed; here the chosen directional record particles have equal energies and
different momenta.

## Both banks, full histories and physical timing

The native lift is

\[
F(A,B)=(G(B),S(A)),\qquad F^{-1}(A,B)=(S^{-1}(B),G(A)).
\]

The same Rule3 tensor uses `u=3(F+F^-1)`. On the declared sector
`a_history=F^-1(b_current)`, its next current state is `F(b_current)` and every
legal carry is unchanged. The full previous/current/carry state remains
recoverable. The old history is not counted as an independent population;
it is fixed by the current state on this prepared sector. Carries are retained
degenerate tags under this kinetic interpretation. Both current four-rail banks
ARE counted: ignoring either bank makes the per-tick account wrong.

At each native tick, old B collides into new A while old A streams into new B.
Consequently

\[
F^2(A,B)=(G(S(A)),S(G(B))).
\]

Both staggered populations move one cell per **two** Engine ticks. We define
one physical lattice macro-unit as two native ticks, and one cell per macro as
unit speed. There is no claim that a carrier travels one cell at every native
tick, nor that these stage labels constitute an operational proper-time clock.

## Exact local and regional source/flux balance

Let `A_+=A_record+ + A_carrier+` and similarly `A_-`; let `n_+=A_+ + B_+` and
`n_-=A_- + B_-`. The node accounts are `E=n_++n_-`, `P=n_+-n_-`.
For the oriented face `(x,x+e)` the per-native-tick currents are

\[
J_E(x)=A_+(x)-A_-(x+e),\qquad
J_P(x)=A_+(x)+A_-(x+e).
\]

The exact current-state identities are

\[
E'(x)-E(x)=J_E(x-e)-J_E(x),\qquad
P'(x)-P(x)=J_P(x-e)-J_P(x).
\]

The same energy identity holds independently for the record and carrier
species. Their momentum equations include the local collision sources
`−2 delta_B(x)` and `+2 delta_B(x)`. The total source cancels at the same node;
dropping record momentum fails already for `1001`.

For any node set R, multiply the identity by its membership indicator and
sum. Each internal face cancels. The remaining oriented boundary term is
`sum_faces (1_R(x)-1_R(x+e)) J(x)`. Regions wrapping around the periodic seam,
checkerboard regions, singleton regions and the full board use this same
formula. Internal communication has not disappeared when its regional net
exchange cancels.

## Positive stress and its exact limitation

At macro times each bank's directional total translates freely:

\[
n_+^{t+2}(x)=n_+^t(x-e),\qquad
n_-^{t+2}(x)=n_-^t(x+e).
\]

In flat continuum-target units, `k_±=(1,±e)` are null and

\[
T^{\mu\nu}=n_+k_+^\mu k_+^\nu+n_-k_-^\mu k_-^\nu.
\]

This is symmetric and tracefree, and its positive populations give the usual
causal energy bound. Smooth advected profiles satisfy the flat continuity
equations; the exact finite-lattice statement is the staggered face balance
above. A pointwise tensor readout must not be silently substituted for that
face flux in a discrete divergence.

**The total stress is species-blind.** The collision changes carrier paths
and retained record correlations but preserves both directional total
populations pointwise. This predicts an unchanged total source contribution
at the collision, not a vanishing source everywhere. No compulsory metric
response to a memory-only label exchange follows. A gravitational completion
must source the generally nonzero two-stream stress and separately prove its
curvature, covariant balance and metric-domain obligations.

`source_transition_ledgers` can verify the same packet account inside the
explicit twelve-channel source tensor. It first requires that the first eight
rows and channel names are exactly the selected native packet law, with no
feedback from the extra coordinates into those rows. It then checks their
complete history and transition against the independent literal oracle. The
four additional geometry/integration coordinates have no additive packet-energy
assignment. Their equations and physical metric interpretation must pass the
separate geometry audit on the same full twelve-channel state. Packet counts
are not silently identified with coordinate or tetrad energy density.
The audit also runs the actual twelve-channel planar source preparation at
L19 for six microticks and checks these packet identities throughout the full
retained board. Its result carries the full tensor and complete-seed hashes.
The physical metric is asserted only on the geometry audit's finite causal
chart, even though the packet ledger itself remains valid across every seam.

On the periodic board the global `E` and vector `P` are constant, hence
`M²=E²-|P|²` is a nonnegative kinematic invariant. A pair of opposite rays has
positive COM rest energy. This does not establish a localized bound massive
body, an operational massive clock, general relativistic covariance, or an
Einstein field equation. A flat metric with this nonzero stress would fail
Einstein's sourced equation; charge conservation cannot repair that failure.

## Reproduction and falsifiers

```sh
python -m validation.local_unification.balance --out runs/local-unification/balance.json
python -m unittest universe24.tests.test_local_unification_balance -v
```

Fresh audits check the actual same native tensor along all six directions on
L3 and L5, all six carry classes, every step's full oracle and inverse, full
rewind, six node/region balances, actual species recoil, macro timing and
positive tracefree stress. Tests reject corrupted transitions, unprepared old
histories and non-Boolean populations. The one-tick speed assertion and the
carrier-only momentum account have explicit counterexamples.
