# The single reversible load-scattering coupling

`universe24/model.py` defines one fixed tensor with 48 live Boolean occupation
channels per node. The channels are grouped into six directional face views,
eight per face. The model transports, blocks and turns occupation without
particle-species labels, external queues or an extra clock bank. Its operational
load interpretation is described in [LOAD_DISTRIBUTION.md](LOAD_DISTRIBUTION.md).
A positive reversible simulation does not establish Einstein dynamics.

## A finite-capacity gate shared by two nodes

Write the retained current value as b_g(x)=1+z_g(x), where z is Boolean. Let
n_g=R_g e_x. An order-four group element h reverses this direction and has
h squared equal to the central element of 2O. Each edge quartet contains

\[
 (g,x),\quad(gh,x+n_g),\quad(gh^2,x),\quad(gh^3,x+n_g).
\]

The even positions are at one endpoint and the odd positions at its neighbor.
The implementation uses group label h=6. These quartets partition all
channel/site positions. Starting from another
member gives the same cyclic quartet and does not create another stored link.

For a quartet word w=(w_0,w_1,w_2,w_3), the edge gate E is:

- If exactly three positions are occupied, keep the word in place during the
  edge stage.
- Otherwise rotate the four values by one position. Every occupied value then
  crosses to the other endpoint; empty/full words are unchanged as arrays.

This is a conservative permutation of all 16 words. Its inverse rotates the
other way and holds the same three-occupation words. The first component and
its inverse are the integer cubics

\[
 E_0(w)=w_3+w_1w_2(w_0-w_3),\qquad
 E^{-1}_0(w)=w_1+w_2w_3(w_0-w_1).
\]

The other components follow by cyclic index shifts. Thus a conditional
finite-capacity rule is implemented by a fixed polynomial, not by a runtime
branch, threshold callback or hidden scheduler. Every monomial reads only one
physical edge and its target.

If q_L=w_0+w_2 and q_R=w_1+w_3, the signed net transfer toward the right is

\[
 J(w)=\begin{cases}
 0,&q_L+q_R=3,\\
 q_L-q_R,&\text{otherwise}.
 \end{cases}
\]

Equivalently, with local bits a,c and neighboring bits b,d,

\[
 J=a+c-b-d-ac(b+d)+bd(a+c).
\]

Endpoint reversal changes its sign. An endpoint therefore responds to its
neighbor's retained occupation. A 2|1
quartet is blocked for this edge stage, while 2|0 can cross. This local current
is not a proof of optimal routing or global equalization. The link has no
additional scalar length or stored tooth-count variable: holding and turning
are changes in the counted occupation state. An effective passage delay must
be measured from actual events, rather than assigned to an extra edge bank.

## Internal gear turning and the complete map

After the edge stage, a fixed onsite right permutation turns the channel
frame. Let T rotate the body axes e_x to e_y, e_y to e_z and e_z to e_x, and
let q=T inverse times h (implemented labels T=4 and q=5). Define the indexing convention

\[
 (O z)_g(x)=z_{gq}(x),\qquad F=O E,\qquad F^{-1}=E^{-1}O^{-1}.
\]

The onsite permutation changes which face carries an occupied channel next;
it neither moves occupation between nodes nor changes a node's total. The
edge stage carries the load-dependent inter-node transfer. Both F and its
inverse remain cubic and satisfy target-plus-one-face support. Right group
multiplication commutes with the joint left channel/cube action, giving exact
`2O-left-regular-cube/1` covariance.

The polynomial tensor is the affine positive encoding

\[
 u(b)=6+3F(b-1)+3F^{-1}(b-1).
\]

Its canonical expansion has 672 monomials of degree at most three. For any
complete Boolean occupation z, prepare

\[
 b=1+z,\qquad a=1+F^{-1}(z),\qquad r\in\{1,2,3,4,5\}.
\]

The unchanged Rule3 update

```python
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

then gives b_next=1+F(z) and leaves r unchanged. All a,b remain in {1,2},
and all carries remain positive, under both forward and inverse evolution.
Exactly 48 channels retain `(a,b,r)`, or 144 integers per node. There are no
static marker rows or separately retained clock/counter variables.

Preparation supplies every channel and carry before execution. The Engine
alone evolves them. A truth-table `sector_map` is an independent oracle and
never feeds an Engine update. Outside the prepared Boolean domain, the Engine
still has its exact integer inverse, but Boolean transport and positivity are
not asserted.

## What is conserved and what the controls show

The node load and total occupation are

\[
 Q(x)=\sum_{g=0}^{47}(b_g(x)-1),\qquad Q_{\rm total}=\sum_xQ(x).
\]

Each edge gate conserves its quartet occupation; onsite turning conserves
Q(x). Therefore Q_total is conserved and the change of Q(x) is exactly the sum
of its signed edge currents. There is a finite counted capacity of 48 occupied
channels per node. This is a logical account, not calibrated physical energy,
rest mass or gravitational stress.

A four-run intervention separates the nonlinear interaction from unconditional
turning: compare empty, probe-only, downstream-occupation-only, and combined
preparations. The interaction contrast is initially zero in both retained
histories. With one probe at the source and two opposing downstream occupants,
the aggregate node-load contrast becomes nonzero after one update. A matched
unconditional edge-flow/turning control has zero interaction contrast. This
establishes local congestion feedback and actual changes in transported load,
not merely different internal phases.

Spreading and improved balancing are separate claims. Two finite comparisons
with the same unconditional-flow/turning control give different outcomes:

| Preparation and observation | Lower concentration | Higher concentration |
| --- | --- | --- |
| Sixteen sparse Bernoulli-1/4 cubes of side 3 in a 7-cube, measured at update 8 | 13 | 3 |
| Sixteen Bernoulli-1/2 cubes of side 2 in a 5-cube, summed over updates 1..30 | 5 | 11 |

All cases are retained, including the unfavorable outcomes. The second
comparison uses fixed seeds 9200..9215. These samples establish some finite
improvements and failures, not an improved global load-balancing theorem.
Concentration can increase again, and the finite closed reversible sector
recurs. Failure cases must remain visible in measurements.

For the sparse comparison, initialize NumPy `default_rng(73613)`, consume four
`integers(0,2,(48,125))` draws used by the continuity checks, then draw sixteen
`random((48,343)) < 0.25` fields. Keep only coordinates `[2:5,2:5,2:5]` in
each 7-cube, using C-order flattened coordinates. Compare sum_x Q(x)^2 after
eight updates. For the dense comparison, initialize a fresh generator for each
seed 9200..9215 and assign `integers(0,2,(48,8))` to all 48 rows over the eight
coordinates whose components are 1 or 2 in a 5-cube, zero elsewhere. Compare
the sum of sum_x Q(x)^2 over updates 1 through 30. Both controls use the same
initial occupation and onsite turn, with the capacity hold removed.

A perfectly full 48-channel single-node burst is a useful negative control:
its central-pair symmetry permits only even quartet occupation, so the
three-occupation capacity gate never fires. Its outward spreading is identical
to unconditional transport. An asymmetric occupied halo can be prepared to
exercise the capacity mechanism; that asymmetry is part of the seed, not a
spontaneously generated physical species.

The default `prepare-model` burst uses size 7, radius 0, the cube center and
root frame 0: its full 48-slot core plus six boundary occupants gives total Q
of 54. A radius-1 core has seven full nodes and 30 halo occupants, total Q=366.
`--no-halo` supplies the symmetric control; `--pattern pulse` and
`--pattern vacuum` prepare one occupied slot and no occupied slots respectively.
All use the same tensor. Arbitrary complete Boolean fields are accepted by
`prepare_occupation`; preparation is finished before the first update.

## Vacuum transport and physical boundary

For one isolated occupied channel g at x, each update advances one face along
n_g and changes the channel to gT. The microscopic path visits the three body
axes in sequence. After three updates its displacement is

\[
 \Delta x=R_g(1,1,1).
\]

In lattice units it travels one graph edge per update. Its unwrapped Euclidean
speed over a three-update block is 1/sqrt(3), not one. The one-edge causal bound
and the isolated-carrier trajectory are different statements. The channel's
binary-octahedral lift returns after six turns.

Even the natural free-carrier coarse momentum
P=sum_(x,g) R_g(1,1,1) z_g(x) is not a conserved collision account. A quartet
word (1,1,1,0) gives P=(1,3,1) before an Engine update and P=(-1,3,-1) after it,
while total Q stays 3. This rejects that momentum interpretation, not every
possible alternative account. Scalar occupation conservation is insufficient
for a physical stress-energy tensor; see [PHYSICS.md](PHYSICS.md).

This construction replaces the previous straight-axis signal/clock tensor.
Its old transverse E/B and residence-time results are not transferred to the
new law. The rotating carrier is not yet a Maxwell photon, a Lorentz-invariant
light cone or a geodesic in a derived Einstein metric. No massive or dark-matter
species, proper clock, gravitational wave or Big-Bang dynamics is established.

All coefficients are divisible by three, so the prepared model has constant
carries and emits only C0 arithmetic clicks. These records can be reconstructed
with explicit initial calibration; they are not photon counts or quantum
measurement probabilities. See [OBSERVATION.md](OBSERVATION.md) and
[PHYSICS.md](PHYSICS.md) for the observation and physical boundaries.
