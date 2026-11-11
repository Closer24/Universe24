# Universe24 — Could a Simple Automaton Be the Logic Behind Nature?

Research Grant Opportunity for a Mathematician or Theoretical Physicist

## 1. Project overview

Universe24 asks whether one elementary local mechanism can generate the diversity of nature. The final objective is to derive quantitative laws of physics in observable events, called clicks, rather than merely produce familiar-looking internal patterns. The project seeks a dedicated researcher, supported through a research grant, to develop the mathematical construction and confront it with physical requirements.

The public repository implements one scalar Rule3 update with the fixed divisor six, a local integer polynomial coupling tensor, and a complete initial state. The current default is a 48-channel cube-group reference construction. The former larger field assembly and its adjustable divisor have been retired. These implementation choices are examples to investigate, not necessary consequences of the foundational postulates.

The research proceeds in both directions: infer constraints on the underlying board from desired click-level observations, and calculate click predictions from a precisely specified board. The algebra in Section 7 describes the fixed-six implementation contract. Mathematical identities, numerical results, proposed mechanisms and unproved physical interpretations are distinguished throughout.

## 2. Conceptual picture and basic terms

An automaton is a system with a stored state and an explicit update rule. A reversible cellular automaton uses local updates from which the complete previous state can be recovered. The model need not be a manufactured computer.

A node is one site of the spatial network. Its board is the collection of internal gear states stored there. A gear, also called a channel, stores three exact integers (a,b,r): two time-level registers and a division remainder. The registers a and b are not two independent boards. This implementation uses one board per node and a periodic cubic network: opposite faces connect, so the finite simulation has no external boundary.

Coupling means that another gear's stored values enter a gear's update input. A matrix describes linear coupling. The supported tensor format also includes products of input values, so its general coupling is a polynomial tensor: a fixed collection of integer coefficients with indices specifying the output gear, input gears, spatial offsets and time registers. The tensor is fixed during a run; its input values evolve. “Rank at most four” here counts one output index and up to three input factors. It is not matrix rank.

A seed is the complete initial state of the whole board, including zero or background values outside any localized disturbance. The law, geometry and seed jointly determine a unique trajectory. An experiment that changes the seed is a different preparation, not a runtime intervention.

A click is a declared local readout of a transition. The current code detects nonzero quotient events for which the stored triple actually changes, and classifies their remainder turn. Readout alone does not modify the board. A measurement apparatus with backreaction must itself be encoded in the evolving gears and fixed couplings.

A representation specifies how a quantity transforms under a symmetry. A scalar is invariant under rotation; a vector transforms by the rotation matrix; a rank-two spatial tensor has two vector indices; a spinor transforms under a double cover of the rotation group. These transformation laws do not by themselves establish a particle, a physical spin measurement, or a gravitational field.

A local rule uses only allowed nearby inputs. A causal relationship specifies which events can influence other events. A reversible rule recovers the full prior state; this differs from a physical time-reversal symmetry and from a signal traveling into the past.

A computational step labels the synchronous evaluation used by the simulator. A physical clock is a local observable process calibrated against other processes. This implementation has computational steps and candidate clock patterns; it has not derived observer-independent physical time without a universal update schedule.

The clock metaphor describes recurring local patterns, gearing describes coupling and frequency relationships, and a clutch describes state-dependent transmission. A fixed coupling coefficient can multiply a changing gear value, creating a varying effective interaction without changing the tensor. A demonstrated clutch still requires a measured transmission contrast, retained information and repeatable operation. The metaphor is not itself a proof.

## 3. Foundational postulates

P1–P10 state the research program's commitments. They are assumptions and target requirements, not claims that the default implementation has already met all of them. P1 is the primary postulate. The remaining sections distinguish the chosen implementation from what must still be derived.

### P1. One universal law at an elementary local level

The central working premise of Universe24 is that the same fundamental law, with the same fundamental parameters, applies everywhere. By resolving physical systems into progressively smaller local constituents, the research postulates an elementary level at which each unit follows that common law. This elementary local mechanism is what the project calls an automaton. Differences between observed phenomena arise from states, interactions, arrangements and histories, rather than separate fundamental laws for each location, particle species or experiment.

The law is assumed to have a short finite description. The existence of an elementary level and its exact discrete representation are research assumptions, not a deduction from the uniformity of physical laws alone. Effective descriptions can differ between scales; the postulate does not require a large system to behave identically to a small one. It fixes neither a lattice spacing nor a literal zero-size point. The possible implementation, its cubic grid, internal gear types and fixed polynomial tensor in Section 7 are an illustrative realization to test, not compulsory consequences of this postulate.

### P2. Local dependence

An elementary interaction depends only on the participating local state and inputs received through the network's permitted causal connections. No update or observation condition may consult an inaccessible distant state or an external description of the whole network. This specifies which information an interaction may use; causal scheduling and the physical propagation bound are specified separately in P6 and P9.

### P3. One discrete event network

Nature's underlying substrate is postulated to be one discrete network of events and local causal relations, with a (3+1)-dimensional spacetime interpretation. Discreteness is a hypothesis about nature, not merely a numerical approximation. An event is a transition or interaction; its causal relations provide the temporal organization. Each node contains one board of internal channel states, not an additional physical spacetime. The exact topology and physical scale remain model choices; H2 and H10 address them, while H3 states the adopted single-board architecture.

### P4. Reversibility of the complete state

Every permitted elementary transition is a bijection on its complete participating state, with a unique inverse. The participating state includes carriers, interaction controls, apparatus and any ordering information needed for inversion. A finite composition is inverted by reversing its operation order and inverting each transition. Retention of all information needed for recovery is a consequence of this postulate, not an additional postulate. A many-to-one description of a partial observation does not contradict full-state reversibility. Mathematical inversion is not, by itself, physical time-reversal symmetry or a physical signal to the past.

### P5. Discrete state representation and exact arithmetic

Each elementary unit’s stored state is exactly representable by a finite tuple of natural numbers N₀={0,1,2,...}; signed integers are equivalent notation through the injective representation in A1. Fundamental transitions and inverses use exact discrete operations, including integer arithmetic, finite permutations and quotient-with-remainder operations, rather than hidden continuous variables or finite-precision rounding. This local representation does not require a finite network, a finite total configuration space or bounded integers. Real-valued quantities may be used in analysis and physical calibration without becoming fundamental stored variables. H1a, H13 and H14 impose stricter restrictions on the permitted dynamics.

### P6. Autonomous causal ordering and local time

Event readiness and the resolution of competing interactions must be determined from locally available state and causal inputs, without an external controller or a universal synchronized physical clock. Different orderings of causally independent events must describe the same physical history and observable results. Any ordering choice that changes an outcome belongs to the retained state required by P4. Physical elapsed time must be calibrated from local observable processes and their causal relationships, not identified with a reference update counter. A synchronous reference calculation alone does not establish this autonomous realization.

### P7. Local observable events and records

Observable clicks arise from local interactions through a declared readout O=Θ(local event state), where O denotes the observed output and Θ the readout function. Each candidate must specify the emission condition, recorded outcome and physical measurement interaction using only the inputs allowed by P2. The readout is fixed for that candidate and may be many-to-one; a physically stored record and its effects remain part of the complete dynamics under P4. This postulate does not prescribe a particular internal clock encounter, a fixed number of click channels or a separate stored click history. Causal ordering of clicks does not by itself establish a thermodynamic arrow of time.

### P8. Local balance of physical quantities

The dynamics must admit local storage-and-transfer accounts that can be quantitatively identified with the physical conserved quantities claimed by the model. Where a conserved account admits a regional total, its change equals net exchange with the surroundings; otherwise the appropriate local balance law must be stated. Count carriers, interactions, apparatus and shared quantities once. Physical energy, momentum, charge and angular momentum require their own identification and calibration; reversibility does not establish them. H15 specifies the balance tests, including the appropriate curved-spacetime formulation and the conditions under which a global conserved total exists.

### P9. Causal speed bound and operational light calibration

In a declared local observer calibration, physical influence is bounded by the common speed c, and an identified freely propagating vacuum light mode attains that bound. For distance d along such a free light path, the observer's elapsed time is d/c; other modes, storage and interactions may take longer. This is not the proper time along a light ray. The same physical calibration must account for different directions and observers in the regime being claimed. An internal gear rate, a fastest lattice route or an uncalibrated reference step does not establish this requirement. H9 and Section 6 specify the tests.

### P10. Branching of causal influence

The common dynamics must permit at least some local interactions whose influence reaches more than one successor event along distinct causal paths. Not every event is required to branch. The event itself remains a located transition; its effects propagate. Branching must satisfy the reversibility, balance and speed requirements of P4, P8 and P9, rather than duplicating a carrier together with its full conserved account. This capability is distinct from merely routing an existing carrier, and from selecting between mutually exclusive complete histories as investigated in H16.

### Motivation and scope

The postulates do not fix the number of gears, the cubic lattice, its physical spacing, a tensor coefficient or a particular clock mechanism. The implementation supplies explicit choices for testing. Retained division remainders make exact inversion possible; they do not establish thermodynamic energy, a physical arrow of time, or a selection principle. Spatial reflection, reversal of a trajectory and the central sign of a spinor are different operations.

## 4. Working hypotheses

### H1. A simple common mechanism can generate diverse phenomena

The motivating intuition is that one basic property or operation could generate the complexity of nature through repeated local interactions. This makes a compact automaton worth investigating. It is a reason to search, not a calibrated probability that Rule3 is the correct physical law. Success must explain which observed features are consequences of the law and which were specified in the tensor or seed.

### H1a. One elementary update, with explicit construction choices

Every gear uses the same exact operation `divmod(2*u+r,6)` with two retained
integer histories and a six-state remainder. There is no adjustable divisor
scale or per-channel numerator/denominator. The fixed tensor, state space and
seed still contain mathematical choices; using one function does not derive
those choices automatically.

### H2. Local cubic geometry as a test platform

The current simulation uses six face neighbors, plus local factors at the target node. Every monomial involves at most one of those neighbors. Finite propagation and cubic symmetry are useful starting constraints, but neither establishes continuous rotational symmetry, Lorentz invariance or curved spacetime. Continuum and large-volume limits must be tested.

### H3. One board with different internal roles

The default board contains 48 group-labelled channels carrying the regular representation of the binary octahedral group. Its current coupling has 288 linear terms, so its actual tensor order is two. Optional examples use other channel counts and polynomial inputs up to order four. The count, coupling and interpretation are construction choices; the group does not determine an inventory of physical species.

### H4. Complete seed and reversible history

A complete seed and fixed law specify one history. Apparently irreversible observations may discard distinctions that remain in the full state. A model of alternative outcomes must specify the initial ensemble or the internal apparatus state. It cannot erase unwanted complete histories while claiming a bijective full-state update.

### H5. Clocks, cooperation and assembly

Recurring patterns may synchronize, exchange signals and form larger persistent structures. Test cooperation by measuring persistence, relative phase, transfer of influence and resilience under perturbation. Compare with controls having the relevant initial structure or coupling removed before the run. Formation, motion and breakup must be demonstrated in the dynamics, not inferred from a clock-shaped visualization.

### H6. Clicks as the observable layer

Physical predictions must be expressed in click positions, ordering, correlations, spectra, rates and responses of local apparatus. The current arithmetic click taxonomy is a candidate observation convention. Calling a quotient event a measurement does not derive the probabilities or causal structure of quantum experiments.

### H7. Effective families and num/den

Different collective modes may exhibit different effective frequencies or recurrence coefficients, despite sharing one elementary update. Ratios such as 1/2 or 2/3 remain hypotheses about effective families. For an exact claim, specify an injective encoding E, a time grouping m and an effective map Wα satisfying W^m E = E Wα on a declared invariant domain, including remainders. A single matching frequency or event fraction is weaker evidence.

### H8. Persistence and stability

Investigate exact periodic states, bounded oscillatory regions, traveling patterns and their perturbations. Reversibility alone permits unbounded growth. A finite recurrence observed on one board is not a proof of stability in larger systems or for arbitrarily long times.

### H9. Emergent isotropy and observer agreement

The 24 proper cube rotations provide a finite symmetry. Continuous isotropy and Lorentz symmetry require additional evidence in a specified scale limit. Check angular dispersion, speed calibration, polarization and moving-observer measurements, rather than equating cubic symmetry with relativity.

### H10. Physical scale and calibration

Any association between the lattice spacing, computational step and physical units is an additional calibration hypothesis. Planck's constant has units of action and does not alone determine a lattice spacing. No physical scale is established by the present exact arithmetic.

### H11. Entropy and the arrow of time

Define the coarse variables and ensemble before discussing entropy. A bijective update does not erase complete-state information; coarse-grained entropy may change. Local organization can increase while an environment becomes more disordered, but this requires an explicit accounting of the relevant degrees of freedom. Complexity, order and low entropy are not interchangeable quantities.

### H12. Local clock comparison and measurement

Test how locally constructed clocks respond to fields, motion and signals. The current forward engine has no external freeze, trigger or restart of a clock. Any such effect must be implemented through the same gears and tensor. A clock crossing does not inject a new seed or remove the existing state.

### H13. Retained division information

The remainder r records the Euclidean division exactly, also for negative input. Its parity is invariant because the numerator contribution is even and the divisor is six. It has six possible values, with three values in a fixed-parity sector. Calling these values teeth does not imply a uniform physical ticking rate.

### H14. Algebra organizes the model but does not uniquely choose it

Cube rotations, quaternions, representations and algebraic ideals describe exact relations and transformation laws. Fixed matrices construct linear parts of the coupling; polynomial coefficients construct the nonlinear parts. The chosen coefficients, field inventory and seed remain explicit inputs until a derivation selects them.

### H15. Exact balances and physical conservation

Check identities that follow from the integer recurrence and distinguish them from physical energy, momentum, charge and angular momentum. A reciprocal subset of the tensor can admit a common potential; declared one-way and two-time terms require separate analysis. A global potential, bounded energy or exact physical conservation law must not be assumed for the complete default model.

### H16. Complexity-oriented cooperation and route selection

The proposed explanatory hypothesis is that observable outcomes can stabilize cooperation among local structures and favor persistent, organized configurations against dispersive tendencies. This is a possible organizing interpretation of superposition, entanglement and measurement collapse, not an identification already established by the implementation.

A test must define a complexity or organization measure, candidate routes, accessible local information and the information retained when one observed route is realized. Demonstrate that the preference is produced autonomously by the declared tensor and seed ensemble. The current engine does not search future histories, maximize a complexity score, or delete alternatives at C2 clicks. A literal global look-ahead optimizer would be an extra law unless realized locally within the stated dynamics.

“Anti-entropy” is shorthand for formation of local order, not an assumed fundamental force. The opposing effect must be identified through measured spreading, heating or disorder in declared variables. Algebraic amplitude growth is not automatically temperature.

On a finite invariant set, reversible evolution consists of cycles. A scalar organization score cannot increase strictly around a closed cycle. A proposed ordering preference must therefore specify the observed subsystem, preparation ensemble and regime; it cannot be assumed to improve every complete state at every update forever.

### H17. Quantum structure as a research target

Determine why a successful model would have quantum-like observable probabilities, superposition and correlations. Conditional carry statistics and spinor transformation rules are useful ingredients, but general Born probabilities, interference, Bell correlations, measurement independence and no-signalling must be assessed together. A classically local deterministic model with independently chosen settings cannot claim an ordinary Bell-inequality violation without identifying which assumption changes.

## 5. Current construction and evidence

### The default and the model migration

The current default is the 48-channel group-reference tensor selected by
`one_system()`. All channels use the fixed divisor six. The previous
382-channel variable-divisor assembly is retired, so its physical
calibrations and state histories are not evidence about this new default.
The [current algebra](MODEL.md) defines the supported law.

### What is established mathematically

The implementation has exact integer states, fixed local polynomial inputs,
acyclic old-history dependencies where used, and a staged inverse. Checks
exercise complete-state recovery, arbitrary-precision arithmetic, local
support, passive observations and explicitly prepared examples. Passing them
does not establish the laws of physics.

The [bounded-circuit construction](BOUNDED_CIRCUITS.md) proves routing and
periodic clocks on a prepared Boolean sector. The [integer reciprocal
examples](INTEGER_RECIPROCAL_GEOMETRY.md) show particular coupled cycles and
explicit unbounded controls. The [integer curl-wave example](LINEAR_SPIN2.md)
has exact constrained travelling sectors, while generic three-dimensional
preparations can be unstable.

### Restricted geometry and clock examples

The [local pp-wave construction](PPWAVE_PALATINI_LOCAL.md) embeds a known
vacuum metric family and preserves its declared centered interior residuals.
It fails at periodic transverse seams. The [geodesic extension](PPWAVE_OPERATIONAL_ROUTE.md)
uses four additional worldline registers inside a carrier node; its exact
prepared trajectory has a proved calibrated coordinate/proper-time relation.
It does not yet implement a packet moving between board nodes, a universal
clock, or matter backreaction.

These are selected tensors and seeds within the common engine. They show
possible mathematical building blocks, not a unique emergence of physical
law from the scalar recurrence.

### What remains unresolved

Stable local structures, effective coefficient families, a common operational
metric, sourced Einstein evolution, observable quantum statistics and a
reversible complexity-oriented selection mechanism remain research targets.
Historical successes and failures are preserved in the
[archive](archive/pre-fixed-six/README.md), with their original assumptions.
Retired conformal, field-clock and detector presets require a new integer
construction before their claims can transfer to the fixed-six model.

## 6. Research objectives, method and people

### 6.1 Ultimate objective: physics in the clicks

Derive the quantitative laws of physics from the underlying local dynamics and show them in observable clicks: their spacetime relationships, probabilities, spectra and apparatus responses. An internal field resembling a known equation is an intermediate result. The final test is agreement with measured phenomena under a declared physical calibration.

### 6.2 Explanatory objective: why these mechanisms?

Explain the structural reason particular realizations occur, not only that a simulation resembles them. “What was the thought behind it?” is a metaphor for an organizing rationale, not conscious intention in nature. Intuition can suggest a solution; explicit constraints, alternative constructions and falsifiable predictions must evaluate it.

DNA, the molecule carrying hereditary information, provides an analogy: a shared generative basis can produce diverse structures through interactions. It is not evidence for Rule3. Einstein expressed the role of intuition: “There is no logical path to these laws; only intuition, resting on sympathetic understanding of experience, can reach them.” The quotation motivates proposing mechanisms, not accepting them without tests. [Source and translation context](https://plato.stanford.edu/entries/einstein-philscience/).

### 6.3 Immediate mathematical objectives

Establish long-time and size-dependent stability of the default; distinguish bounded regimes from growth. Make the common-law assumptions, parameter choices and retained information explicit. Prove local inverse and balance identities under their actual hypotheses, and test how these identities compose across layers. Identify which construction choices can be reduced without changing the complete state trace or the claimed observable behavior.

### 6.4 Relativity targets at the click level

Show operational local clocks and causal cones; consistent calibration of a common light speed; observer agreement and an appropriate Lorentz limit; universal free fall and clock redshift; a metric interpretation with local conservation and constrained gravitational degrees of freedom; and quantitative weak-field and radiative predictions. Recovering general relativity requires an appropriate continuum theory and empirical limits, not merely storing ten metric components.

The target is gravitational geometry: infer one operational metric from local clock intervals and signal travel through links, then test its predictions for other species and for free fall without separate fits. A separate attraction between oscillator amplitudes does not establish gravity. The rank-four coupling tensor is not itself the rank-two spacetime metric.

The event-space target includes the Einstein energy and momentum constraints, their preservation by the evolution, and a consistently identified stress source. Six directed axis measurements and a local clock do not determine all ten metric components; the off-diagonal spatial components require independent observations. Section A12 states the acceptance requirements, and the geometry research notes detail the reconstruction and constraint obligations. A continuum interpretation must specify its refinement, physical calibration and error bounds.

The equivalence principle requires different physical clock and matter constructions to respond consistently. Test gravitational redshift, free fall, light bending, propagation delay and gravitational waves with independently defined apparatus and sources. General covariance concerns physical predictions under coordinate descriptions; it is not proved by relabeling lattice indices. State the regime and approximation for each target.

### 6.5 Quantum, light and matter targets

Derive stable propagating and localized families, dispersion, polarization, spin behavior, interference and quantitative detector statistics. Distinguish a frequency gap from physical mass. Determine whether the family structure and parameters follow from the law, or were inserted through tensor coefficients.

Test Bell correlations with settings, detections and sampling rules declared in advance. Check no-signalling, contextuality and measurement backreaction. Reject explanations that rely on discarded events or hidden setting correlations unless those mechanisms are explicitly the model's stated hypothesis and face their own experimental tests.

### 6.6 Cooperative clocks, route choice and entropy

Demonstrate local patterns that connect, cooperate, move, persist and break apart, using the clock-and-gear analogy as an operational guide. Show which interaction transmits influence and which state stores a record. Under H16, test whether a selected observed route stabilizes greater persistent organization, compared with declared alternatives and controls, while accounting for dispersive behavior and coarse-grained entropy elsewhere.

The route choice must occur in the underlying dynamics. Clicks should reveal its observable record. Reversibility requires the full information to remain recoverable; a readout can hide alternatives without physically deleting information. Identify a measurable benefit of the proposed cooperation rather than assuming that every click increases complexity.

### 6.7 Method: inference in both directions

From clicks to boards: specify desired observable phenomena and derive necessary causal, algebraic, balance and apparatus constraints. From boards to clicks: define one tensor and seed family, run the exact dynamics, and calculate the registered observables. Iterate between these directions. Neither direction may silently fit the observation by changing the rule during a run.

Use recurring patterns in nature—local organization maintained by exchanges, propagation, synchronization and dispersal—as sources of candidate mechanisms. Do not assume that a single node already possesses a macroscopic temperature, entropy or gravitational field. Define the microscopic variable and show how the larger phenomenon follows.

Separate exact theorems, finite computations and physical hypotheses. Register controls, failure criteria, observable definitions and resource limits before a run where practical. Keep all state needed for inversion. Report negative results, size dependence and uncertainty. Mathematical incompatibilities should lead to a named change in assumptions, not a change of terminology.

### 6.8 People needed for the project

Mathematician: A specialist in reversible cellular automata and computational algebra, with knowledge of finite groups and their representations. Able to define the node operations, prove reversibility, analyze stability and implement exact-arithmetic tests.

Theoretical physicist: A researcher with expertise in quantum foundations, quantum field theory and relativity. Able to connect click predictions to measurable phenomena, assess Bell-test consistency and investigate the emergence of particles and gravity.

The public repository is an executable starting example for this research grant. It is intended to make the assumptions and unresolved tasks concrete for a dedicated researcher; it is not a completed physical theory.

## 7. Algebra of a possible implementation

This is the current mathematical contract for the executable model. A node's
state, a fixed integer coupling tensor, and the complete seed specify a run.
The scalar divisor is the constant six. There is no adjustable divisor scale,
per-channel numerator/denominator, hidden arithmetic rescaling, or second
state-update rule.

### A0. Overview: what the algebra does

Write the full state as `S_n=(a_n,b_n,r_n)` and augment the old register vector
with a constant component, `v_n=(1,b_n,a_n)`. The fixed tensor supplies a local
integer polynomial `u_n=T(v_n,v_n,v_n)`, with unused input slots represented
by the constant component. The one evolution map and passive observation are

    S_(n+1) = W_T(S_n),       O_n = Theta(S_n,S_(n+1)).

The tensor and seed are construction choices. They are not derived from the
scalar recurrence alone. The reference cube block and the geometric examples
are possible constructions, not necessary models of nature.

### A1. Space, registers and degrees of freedom

The implemented storage lattice is a periodic cubic graph with six face
neighbors. At each node `x` and gear type `i`, retain

    S_(x,i) = (a_(x,i), b_(x,i), r_(x,i)),
    a,b in Z,       r in {0,1,2,3,4,5}.

For `G` gear types, a node has `2G` unbounded signed integer registers and `G`
six-state remainders. Signed integers can be stored as natural numbers via
`z -> 2*z` for `z>=0` and `z -> -2*z-1` otherwise; this is an injective
encoding, not an extra update. The old and current histories `a,b` are not independent
physical boards by definition. Interpreting them as two interacting boards
requires a separate construction and observation map.

Since the incoming numerator is even, each remainder's parity is invariant.
After choosing that parity, its accessible remainder alphabet has three
values. This is a sector restriction, not an additional coordinate.

The graph is closed by periodic boundaries. That does not imply that every
continuum coordinate chart assigned to its samples is globally periodic or
satisfies physical field equations across the seams.

### A2. Cube rotations, quaternions and reflections

The proper rotations of the cube form a group of order 24. Unit quaternions
act on spatial vectors by `v -> q v q^-1`; opposite quaternions give the same
spatial rotation. Lifting the cube rotations gives the binary octahedral
group `2O`, with 48 elements. Quarter-turn generators may be written

    q_x=(1+i)/sqrt(2), q_y=(1+j)/sqrt(2), q_z=(1+k)/sqrt(2),
    i^2=j^2=k^2=ijk=-1.

These formulas construct fixed algebraic matrices. The runtime register
values remain integers; it does not update floating quaternion components.
The 48-element double cover is not the 48-element cube group obtained by
adding spatial reflections. A reflection convention and its action on the
state must be specified separately.

### A3. The 48-channel reference block and its matrices

The reference block labels one channel by each element of `2O`. Multiplying
a group label gives a fixed permutation of the 48 coordinates. Neighbor
transport is represented by six fixed integer matrices `P_d`, each 48 by 48,
with the selected signs and direction conventions supplied by the builder.
The current default uses `body_signs=(1,-1,1)`, 288 nonzero linear terms
and actual tensor order two; the format also permits order-four examples:

    u_x = sum_(six directions d) P_d b_(x+d).

The matrices specify which channel at a face neighbor contributes to a local
channel. Opposite directions, sign choices, reciprocity and rotation
covariance are properties to verify for the chosen matrices. Merely naming
the group does not prove them for every coupled tensor.

The same coupling may be stored sparsely as nonzero matrix/tensor entries.
That storage choice does not add a lookup-dependent update law. The global
operator is assembled from these local blocks and the six spatial shifts;
a node never evaluates a dense global matrix.

### A4. Representations and the role of an ideal

The complex regular representation decomposes into irreducible group
representations. Appropriate linear readouts can therefore transform as
scalars, vectors, tensor components or spinorial representations of this
finite group. These are transformations of a shared integer state, not four
different scalar update rules. They do not by themselves establish photons,
fermions, continuous Lorentz symmetry or quantum statistics.

The group ring can be described by generators `[g]` with `[g][h]=[gh]`.
Equivalently, a two-sided ideal imposes the relations

    X_e-1=0,       X_g X_h-X_(gh)=0.

An ideal identifies algebraic expressions representing the same group
operation. It does not authorize deleting distinct dynamic states or division
remainders. A prepared invariant sector may also be expressed by polynomial
relations; its preservation must be proved under the full update and inverse.

### A5. One fixed polynomial coupling tensor

For each output gear, the input is

    u_(x,i) = sum_m c_m product_(f in m) v_(x+offset_f, gear_f),
    c_m in Z,       number of input factors <= 3.

This is an order-at-most-four tensor when the output index is counted. It is
not the rank-four Riemann curvature tensor. Its entries remain fixed during
the run. An effective link strength may depend on evolving registers because
the polynomial contains products; that is different from replacing tensor
entries at runtime.

Every monomial reads only its target node and at most one face neighbor.
For physical link gears, both geometric endpoints must be counted when
checking strict single-edge support. Storage-local reads alone are not a
proof of that stronger condition.

Old-`a` reads are permitted only when their gear dependency graph is acyclic.
All forward inputs still read one complete old snapshot; the ordering is
used by the inverse, not by the forward loop.

### A6. The single scalar operation

At every node and gear, use the same Euclidean division:

    ell, r_next = divmod(2*u+r, 6)
    a_next = b
    b_next = ell-a

Equivalently,

    2*u+r = 6*(b_next+a)+r_next,       0 <= r_next < 6.

The convention also applies to negative input. All intermediate values,
quotients and remainders are exact integers. There is no adjustable divisor
argument in the engine or tensor. The previous variable-divisor models are
superseded; their calibrated predictions do not automatically transfer to
this law. See the [migration note](DIVISOR_AUDIT.md).

### A6a. Exact inverse and the distinction from a mirror

Recover old `b=a_next`. In the validated dependency order, evaluate each old
input using the recovered old `b` and any earlier recovered old `a`, then set

    r = (r_next-2*u) mod 6,
    a = (2*u+r-r_next)//6 - b_next.

The division is exact. This recovers the full retained state. Invertibility
is not boundedness, physical energy conservation or a proof of a preferred
arrow of time. For b-only inputs, `M(a,b,r)=(b,a,5-r)` is a reversor; that
particular mirror need not apply to general old-history couplings.

### A7. Node code and connection to the rest of the board

The elementary operation is

```python
def rule3(a, b, r, u):
    quotient, remainder = divmod(2 * u + r, 6)
    return b, quotient - a, remainder
```

The shared engine first evaluates the fixed local tensor from the old
snapshot, then applies this operation componentwise. Preparation constructs
the graph, tensor and complete integer seed before the first update.
Observers read histories and never inject state, choose branches, reset
clocks or alter links between updates.

### A8. What remains free

The model designer chooses the number and interpretation of gear types,
the allowed graph and boundary conditions, fixed integer tensor entries,
and the initial `a,b,r` arrays. A decoder and any physical-unit calibration
must also be declared. They are not hidden dynamic variables.

There is no independently chosen `num/den` for a channel. Effective families
with other coefficients are hypotheses about collective or retimed dynamics.
An exact claim needs an injective encoding `E` and a fixed number of steps
`m` satisfying `W_T^m E = E F` on a declared invariant sector, including all
retained information required for reversal. Matching one frequency is weaker.

### A9. What a click means in the code

An official click is a passive record with nonzero quotient when the complete
local triple changes, subject to its declared observation label. For the
remainder increment modulo six, classes distinguish zero, positive and
negative turns. They do not select the next state.

An absent record does not always mean the quotient was zero: a nonzero
stationary triple can have a nonzero quotient and no click. Reconstructing a
state from clicks therefore needs a proved decoder and its declared initial
information. The [geodesic example](PPWAVE_OPERATIONAL_ROUTE.md) makes this
restriction explicit.

### A10. Balances, clocks and stability

The quotient-remainder ledger is exact by construction. A physical charge,
energy or stress balance needs its own definition and proof for the selected
tensor. Reciprocity can be checked as the existence of a polynomial potential,
but it is not sufficient to establish Einstein constraints or physical energy.

Periodic registers, transported patterns and prepared interacting cycles can
serve as clock candidates. A finite return of the complete state proves
repetition of that orbit, not stability for all seeds. Unbounded integer
orbits remain possible even under an invertible rule.

A score on a closed periodic orbit cannot increase strictly at every step.
A proposed complexity-oriented selection mechanism must retain the information
needed for reversal and define how observable outcomes follow from the state.
No such physical collapse or global optimization law is supplied by Rule3 alone.

### A11. Retained constructive examples

The [bounded circuit](BOUNDED_CIRCUITS.md) realizes routing and periodic clocks
on a proved Boolean sector. The [integer reciprocal examples](INTEGER_RECIPROCAL_GEOMETRY.md)
show prepared coupled cycles and explicit instability controls.

The [local pp-wave example](PPWAVE_PALATINI_LOCAL.md) transports a chosen
nonflat vacuum metric sector and checks exact interior geometric residuals.
Its periodic chart seams fail those equations. The [geodesic extension](PPWAVE_OPERATIONAL_ROUTE.md)
encodes selected one-axis worldlines at a carrier node, with exact calibrated
readouts. It does not yet produce a packet moving on board links, universal
clocks or matter backreaction.

Each construction must be validated under the fixed-six engine. Historical
large-divisor run records are not evidence for the migrated construction.

### A12. Physical acceptance requirements

A common spacetime metric must be inferred consistently from local clock
comparisons and signal propagation, and predict other test bodies without
species-specific fits. Geodesic motion is not enough: the metric must obey
a stated source equation and preserve its constraints. A coordinate chart,
local graph or set of tensor-named counters does not establish Einstein space.

Quantum claims separately require observable probabilities, interference,
contextuality or Bell-test consistency under stated assumptions, and appropriate
scaling of the state space. No reference to a finite group, complex readout,
reversible branch or click alone proves those properties.

### A13. Validation and source of truth

The executable tensor, complete seed, scalar engine and declared decoder are
the reproducible specification. Compare complete states, inverse results,
local support and event records. Keep exact theorems, finite run evidence and
physical hypotheses separate. See [validation](VALIDATION.md) for commands and
current scope; superseded record files must not be promoted by wording alone.
