# Load, internal face transmissions and distribution

A node applies the same fixed polynomial at every update. Its six internal
face mechanisms carry the state that can block or redirect information.
Nothing in the evolution rule asks whether a pattern is called light, matter
or dark matter. Those names require observable physical properties; display
labels never enter the tensor.

The purpose of the load diagnostics is to test whether retained information
actually leaves a concentrated region and how traffic changes its passage.
They are passive measurements. A measured load, a chart or the observer must
not become an uncounted controller that changes the Engine.

## What counts as heavy computation

Three quantities answer different questions and are reported separately in
`universe24/load.py`:

| Quantity | What is counted | What a larger value establishes |
| --- | --- | --- |
| Fixed logical work | Monomial evaluations, factor reads, arithmetic operations and Rule3 calls per node | The symbolic work schedule of this tensor; it does not vary with particle labels |
| Integer representation cost | Magnitude bit lengths of retained a,b,r | Larger stored operands in this encoding; not measured CPU duration, physical energy or mass |
| Dynamical load | Conserved occupation, blocked edge capacity, traffic and response delay | More activity or occupied transmission capacity under the declared model |

The Engine can represent arbitrarily large integers in general. In the current
proved positive Boolean domain, a and b are only 1 or 2 and carries stay in
1..5. There is therefore no growing integer-width bottleneck in that domain.
A busy face is a dynamical transmission condition, not evidence that its host
CPU evaluates more polynomial terms than another node.

Integer width is not an intrinsic gravitational source. For example, the
reversible recoding a'=a+K, b'=b+K and u'(b')=u(b'-K)+6K preserves the fixed-six
Rule3 trajectories after subtracting K. It can make the stored integers much
wider without changing the decoded trajectory. A physical theory based on
integer width would need an additional encoding postulate and operational
calibration. Lloyd's physical computation bounds concern a device's energy
and available degrees of freedom, not an arbitrary choice of numeral code [4].

## The implemented mechanism

The built-in law uses all 48 channels as live occupation bits, eight per face,
with positive encoding b=1+bit. There are no separate light/matter labels,
static marker rows or extra clock variables. A quartet shared by two neighboring
nodes has two channels at each endpoint. Its values cross cyclically unless
exactly three are occupied, in which case that edge-stage transfer is held.
A fixed onsite permutation then turns the channel frames toward other faces.
The same rule applies at every node and both endpoints affect its current.

This gives species-blind, occupation-dependent scattering and blocking within
the exact reversible Engine. The conserved node account is
Q(x)=sum_g(b_g(x)-1), with total Q conserved. The edge current is q_L-q_R except
when the four-slot occupation is three, where it is zero. All conditional
behavior comes from fixed cubic coefficients. There is no separate queue
controller that makes the decision after observing the state. The equations,
inverse and complete positive domain are in [MODEL.md](MODEL.md).

The measured local feedback is stronger than a visual spreading pattern. In
four matched runs (empty, probe, downstream occupancy, combined), the initial
interaction contrast is zero in both histories and becomes nonzero in the
aggregate node load at causal contact. Unconditional turning/edge flow has
zero interaction contrast. The downstream occupation therefore changes actual
transported load, not only channel phase.

This result does not establish that congestion improves global balancing.
A sparse 16-case localized sample had lower concentration than unconditional
transport in 13 cases and higher in 3 at update 8. A different, denser 16-case
sample on a 5-cube, compared over the entire update window 1..30, had lower
time-summed concentration in only 5 cases and higher in 11. The global
improvement claim fails for that second sample; neither the initial states nor
the measurement time may be selected after seeing favorable outcomes. Exact
preparation domains are listed in [MODEL.md](MODEL.md).

A full 48-channel single-node burst never activates the three-occupation gate:
its central-pair symmetry is preserved and every quartet occupancy remains
even. Its visible expansion is therefore a free-transport control. A prepared
asymmetric halo exercises the congestion gate; the board must expose its
actual blocked activity and distinguish this preparation from the symmetric
control. Finite spreading alone is not an optimization or gravity claim.

## Delay, backpressure and spreading are different tests

An occupied mechanism may retain information longer. This does not by itself
show that the load is redistributed or that a remote congested region sends
feedback upstream. In queueing networks, backpressure couples routing/service
decisions to differences between connected queue states and to capacity
constraints [1]. Merely lowering the service rate of a busy queue can make its
backlog worse. Throughput stability also does not guarantee delivery of each
individual item: Neely gives a stable one-packet example in which routing can
wander indefinitely [7]. Service/fairness and release-time claims need their
own tests. The finite-buffer result of Supittayapornpong and Neely explicitly trades
reliability for packet drops [8]; it cannot be imported into this model's
no-discard dynamics.

The reversible model must keep all information, including any internal routing
or phase state, within the 48 retained channels. Importing a conventional
scheduler, dropping packets, resetting a queue or consulting a global load
map would change that contract. Conservative reversible gates demonstrate
that state-dependent routing and information preservation can coexist [2];
they do not supply a general guarantee that every initial distribution becomes
uniform.

The relevant checks are operational:

- **Residence:** compare a stored unit's occupancy before and after additional
  traffic. Distinguish this from a claim about identifiable particles.
- **Causal information delay:** compare two complete preparations differing
  in a declared input perturbation, with the same later traffic. Measure the
  first outgoing difference and the first difference at the next node.
- **Reverse feedback:** change a downstream region while keeping the upstream
  preparation fixed. A response upstream must occur only after causal contact;
  detect the actual transported influence rather than renaming a local pause.
- **Cross-face transfer:** begin with a directional preparation and verify
  transfer into other directions under the same tensor, with an exact account
  of what moves. Populating six outgoing directions initially is not that test.
- **Distribution:** compare concentration, occupied support and peak load at
  the same conserved total, with a rigid-translation control and all failures
  retained. A moving bright region need not become less concentrated.

For nonnegative node weights q_i, let Q=sum_i q_i and S2=sum_i q_i^2. The
passive profile reports participation Q^2/S2 and normalized concentration
N*S2/Q^2 as exact rational numbers. Participation equals the occupied-node
count for equal nonzero weights; normalized concentration is 1 for a uniform
nonempty distribution and N for a single occupied node. An empty distribution
is explicitly flagged and uses zero as a reporting convention. Neither
quantity changes when a configuration is merely permuted or translated.

At fixed Q, a decrease in S2 establishes finite-time spreading for that
comparison. It does not establish permanent equilibration. A closed finite
reversible state space is a permutation of its states and eventually returns.
A scalar concentration cannot strictly decrease on every step of every cycle.
Coarse-grained relaxation and useful finite-time redistribution remain
possible, but require their own measured domain and timescale. An exact
reversible lattice model can exhibit ballistic, diffusive or insulating
transport in different regimes [9]; reversibility alone selects none of them.

## From signal timing to an Einstein comparison

The nearest established comparison is effective optical or causal geometry:
a signal can see a nonuniform propagation medium without that medium obeying
Einstein's equations [5]. A calibrated communication length c times a measured
transit time is useful for observations, but it is not a unique spacetime
metric.

For any positive n(x), the static line elements

\[
 ds_A^2=-c^2dt^2+n(x)^2dx^2,\qquad
 ds_B^2=-c^2dt^2/n(x)^2+dx^2
\]

have identical coordinate null travel times dt=n(x)|dx|/c. Stationary material
clocks instead read dτ_A=dt and dτ_B=dt/n(x). Timing the same light trajectories
does not determine the missing clock calibration. Six axial delays also do
not determine all mixed components of a general four-dimensional metric.

General relativity couples geometry to stress-energy, including energy,
momentum flow and stress, with covariant conservation. A scalar traffic count
and global occupancy conservation are not yet that tensor. The natural
free-carrier momentum proxy sum_(x,g) R_g(1,1,1) z_g(x) already fails at a
three-occupation capacity collision: (1,3,1) becomes (-1,3,-1) with Q_total=3.
That counterexample rejects this proxy, not all possible physical accounts.
Species-independent software is useful, but the physical equivalence principle
additionally requires the same operational geometry for distinct probes and
material clocks.

Two precise research routes illustrate what is still needed. Regge calculus
specifies a simplicial geometry, computes curvature from shared edge data and
varies a discrete action [6]. Jacobson's derivation assumes local causal
horizons, horizon entropy proportional to area, Unruh temperature and an
energy/entropy relation for every local null direction; geometric focusing
then constrains curvature [3]. Neither result identifies Einstein gravity
with an optimizer for CPU or queue load.

Acceptance therefore requires one retained construction with calibrated
material clocks, a common Lorentzian metric, a source stress tensor and
independent constraint/evolution residuals under refinement. Separate timing,
transport and homogeneous-gravity examples cannot be pooled as that result.

## Initial preparations and the board

A localized preparation supplies complete state before evolution. A compact
source spreading after that preparation is a simulated release of activity;
it is not by itself a cosmological Big Bang or creation of new information.
The tensor and retained state, rather than a display animation, must produce
all subsequent frames.

The board replays canonical clicks with explicit public initial calibration
from the sealed input bundle. It checks that calibration against the selected
positive forward sector; subsequent frames are reconstructed from clicks,
without opening the full transition trace or advancing Engine. The initial
occupation history is supplied, not discovered from silent channels.
Recorded host update numbers order events; they are not inferred proper time.
A full-state field diagnostic and an unaided click-only observation are distinct
operations and must be labelled accordingly.

The implemented display shows occupation, transferable and held capacity,
empty capacity, arithmetic clicks, all six faces, concentration and integer
representation cost. Its held-capacity count includes three-slot blocked and
four-slot saturated quartets, which are separately reported. Those snapshot
counts are not individual residence-time measurements. A stationary
pattern is not automatically a massive particle. A pattern absent from one
optical readout is not automatically dark matter: gravitational sourcing and
its interaction with optical probes must be demonstrated under the same law.
The physical statuses remain those in [PHYSICS.md](PHYSICS.md), regardless of
the colors or names chosen for the board.

## Sources and their scope

1. L. Tassiulas and A. Ephremides (1992), [Stability properties of constrained
   queueing systems and scheduling policies for maximum throughput in multihop
   radio networks](https://www.di.ens.fr/~busic/mar/projets/TE92.pdf).
   Queueing stability and scheduling provide an engineering comparison, not
   an Einstein or reversible-universe theorem.
2. E. Fredkin and T. Toffoli, [Conservative Logic, MIT technical report
   (1981)](https://dspace.mit.edu/entities/publication/19826ace-4422-4f48-b134-5be130d5bcf5),
   published in *International Journal of Theoretical Physics* (1982).
3. T. Jacobson (1995), [Thermodynamics of Spacetime: The Einstein Equation of
   State](https://arxiv.org/html/gr-qc/9504004v2).
4. S. Lloyd (2000), [Ultimate physical limits to
   computation](https://arxiv.org/abs/quant-ph/9908043).
5. C. Barceló, S. Liberati, S. Sonego and M. Visser (2004), [Causal structure of
   acoustic spacetimes](https://arxiv.org/abs/gr-qc/0408022).
6. T. Regge and R. M. Williams (2000), [Discrete structures in
   gravity](https://arxiv.org/html/gr-qc/0012035v1).
7. M. J. Neely, [Notes on Backpressure Routing](https://ee.usc.edu/stochastic-nets/docs/backpressure.pdf),
   especially the separation between network stability and individual delivery.
8. S. Supittayapornpong and M. J. Neely (2015), [Achieving
   Utility-Delay-Reliability Tradeoff in Stochastic Network Optimization with
   Finite Buffers](https://arxiv.org/abs/1501.03457).
9. M. Medenjak, K. Klobas and T. Prosen (2017), [Diffusion in deterministic
   interacting lattice systems](https://arxiv.org/abs/1705.04636).

These papers motivate comparisons and tests. They do not validate this
repository's tensor or identify its occupied states with physical species.
