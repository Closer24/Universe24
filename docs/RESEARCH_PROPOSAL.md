# Universe24 — Could a Simple Automaton Be the Logic Behind Nature?

Research Grant Opportunity for a Mathematician or Theoretical Physicist

## 1. Project overview

Universe24 asks whether one elementary local mechanism can generate the diversity of nature. The final objective is to derive quantitative laws of physics in observable events, called clicks, rather than merely produce familiar-looking internal patterns. The project seeks a dedicated researcher, supported through a research grant, to develop the mathematical construction and confront it with physical requirements.

ONE is the current executable example and the sole active implementation in the public repository. It combines one scalar Rule3 update, one shared integer divisor, a fixed local polynomial coupling tensor, and a complete initial state. The current default has 382 gear types per node; its 48-channel cube-symmetry block is only one part of that state. These choices are an implementation to investigate, not necessary consequences of the foundational postulates.

The research proceeds in both directions: infer constraints on the underlying board from desired click-level observations, and calculate click predictions from a precisely specified board. The algebra in Section 7 describes the implemented ONE construction. Mathematical identities, numerical results, proposed mechanisms and unproved physical interpretations are distinguished throughout.

## 2. Conceptual picture and basic terms

An automaton is a system with a stored state and an explicit update rule. A reversible cellular automaton uses local updates from which the complete previous state can be recovered. The model need not be a manufactured computer.

A node is one site of the spatial network. Its board is the collection of internal gear states stored there. A gear, also called a channel, stores three exact integers (a,b,r): two time-level registers and a division remainder. The registers a and b are not two independent boards. ONE uses one board per node and a periodic cubic network: opposite faces connect, so the finite simulation has no external boundary.

Coupling means that another gear's stored values enter a gear's update input. A matrix describes linear coupling. ONE also includes products of input values, so its general coupling is a polynomial tensor: a fixed collection of integer coefficients with indices specifying the output gear, input gears, spatial offsets and time registers. The tensor is fixed during a run; its input values evolve. “Rank at most four” here counts one output index and up to three input factors. It is not matrix rank.

A seed is the complete initial state of the whole board, including zero or background values outside any localized disturbance. The law, geometry and seed jointly determine a unique trajectory. An experiment that changes the seed is a different preparation, not a runtime intervention.

A click is a declared local readout of a transition. The current code detects nonzero quotient events for which the stored triple actually changes, and classifies their remainder turn. Readout alone does not modify the board. A measurement apparatus with backreaction must itself be encoded in the evolving gears and fixed couplings.

A representation specifies how a quantity transforms under a symmetry. A scalar is invariant under rotation; a vector transforms by the rotation matrix; a rank-two spatial tensor has two vector indices; a spinor transforms under a double cover of the rotation group. These transformation laws do not by themselves establish a particle, a physical spin measurement, or a gravitational field.

A local rule uses only allowed nearby inputs. A causal relationship specifies which events can influence other events. A reversible rule recovers the full prior state; this differs from a physical time-reversal symmetry and from a signal traveling into the past.

A computational step labels the synchronous evaluation used by the simulator. A physical clock is a local observable process calibrated against other processes. ONE has computational steps and candidate clock patterns; it has not derived observer-independent physical time without a universal update schedule.

The clock metaphor describes recurring local patterns, gearing describes coupling and frequency relationships, and a clutch describes state-dependent transmission. A fixed coupling coefficient can multiply a changing gear value, creating a varying effective interaction without changing the tensor. A demonstrated clutch still requires a measured transmission contrast, retained information and repeatable operation. The metaphor is not itself a proof.

## 3. Foundational postulates

P1–P10 state the research program's commitments. They are assumptions and target requirements, not claims that default ONE has already met all of them. P1 is the primary postulate. The remaining sections distinguish the chosen implementation from what must still be derived.

### P1. One universal law at an elementary local level

The central working premise of Universe24 is that the same fundamental law, with the same fundamental parameters, applies everywhere. By resolving physical systems into progressively smaller local constituents, the research postulates an elementary level at which each unit follows that common law. This elementary local mechanism is what the project calls an automaton. Differences between observed phenomena arise from states, interactions, arrangements and histories, rather than separate fundamental laws for each location, particle species or experiment.

The law is assumed to have a short finite description. The existence of an elementary level and its exact discrete representation are research assumptions, not a deduction from the uniformity of physical laws alone. Effective descriptions can differ between scales; the postulate does not require a large system to behave identically to a small one. It fixes neither a lattice spacing nor a literal zero-size point. The ONE construction, its cubic grid, internal gear types and fixed polynomial tensor in Section 7 are an illustrative realization to test, not compulsory consequences of this postulate.

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

The postulates do not fix the number of gears, the cubic lattice, its physical spacing, a tensor coefficient or a particular clock mechanism. ONE supplies explicit choices for testing. Retained division remainders make exact inversion possible; they do not establish thermodynamic energy, a physical arrow of time, or a selection principle. Spatial reflection, reversal of a trajectory and the central sign of a spinor are different operations.

## 4. Working hypotheses

### H1. A simple common mechanism can generate diverse phenomena

The motivating intuition is that one basic property or operation could generate the complexity of nature through repeated local interactions. This makes a compact automaton worth investigating. It is a reason to search, not a calibrated probability that Rule3 is the correct physical law. Success must explain which observed features are consequences of the law and which were specified in the tensor or seed.

### H1a. One elementary update, with explicit construction choices

Every ONE gear uses the same quotient-and-remainder recurrence and the same divisor D=6Q. The default Q is 2³³+1. This is not the earlier restriction to a complete 48-channel system with divisor six. The scalar update form is preserved, while the enlarged state and polynomial tensor contain additional mathematical content. Using one function does not derive that content automatically.

### H2. Local cubic geometry as a test platform

The current simulation uses six face neighbors, plus local factors at the target node. Every monomial involves at most one of those neighbors. Finite propagation and cubic symmetry are useful starting constraints, but neither establishes continuous rotational symmetry, Lorentz invariance or curved spacetime. Continuum and large-volume limits must be tested.

### H3. One board with different internal roles

The default board contains 382 gear types. Some carry matter-like amplitudes, others link fields, relays, metric candidates, clocks or records. The 48-gear L0 block carries the regular representation of the binary octahedral group. This count is a construction choice; the group does not force the total number of gears or the inventory of physical species.

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

Test how locally constructed clocks respond to fields, motion and signals. The current forward engine has no external freeze, trigger or restart of a clock. Any such effect must be implemented through the same gears and tensor. A cosmic-hand zero crossing does not inject a new seed or remove the existing state.

### H13. Retained division information

The remainder r records the Euclidean division exactly, also for negative input. Its parity is invariant because the input is even and D is even. In ONE it has D possible values, with D/2 values in a fixed-parity sector. Calling these values teeth does not imply a uniform physical ticking rate.

### H14. Algebra organizes the model but does not uniquely choose it

Cube rotations, quaternions, representations and algebraic ideals describe exact relations and transformation laws. Fixed matrices construct linear parts of the coupling; polynomial coefficients construct the nonlinear parts. The chosen coefficients, field inventory and seed remain explicit inputs until a derivation selects them.

### H15. Exact balances and physical conservation

Check identities that follow from the integer recurrence and distinguish them from physical energy, momentum, charge and angular momentum. A reciprocal subset of the tensor can admit a common potential; declared one-way and two-time terms require separate analysis. A global potential, bounded energy or exact physical conservation law must not be assumed for the complete default model.

### H16. Complexity-oriented cooperation and route selection

The proposed explanatory hypothesis is that observable outcomes can stabilize cooperation among local structures and favor persistent, organized configurations against dispersive tendencies. This is a possible organizing interpretation of superposition, entanglement and measurement collapse, not an identification already established by ONE.

A test must define a complexity or organization measure, candidate routes, accessible local information and the information retained when one observed route is realized. Demonstrate that the preference is produced autonomously by the declared tensor and seed ensemble. The current engine does not search future histories, maximize a complexity score, or delete alternatives at C2 clicks. A literal global look-ahead optimizer would be an extra law unless realized locally within the stated dynamics.

“Anti-entropy” is shorthand for formation of local order, not an assumed fundamental force. The opposing effect must be identified through measured spreading, heating or disorder in declared variables. Algebraic amplitude growth is not automatically temperature.

On a finite invariant set, reversible evolution consists of cycles. A scalar organization score cannot increase strictly around a closed cycle. A proposed ordering preference must therefore specify the observed subsystem, preparation ensemble and regime; it cannot be assumed to improve every complete state at every update forever.

### H17. Quantum structure as a research target

Determine why a successful model would have quantum-like observable probabilities, superposition and correlations. Conditional carry statistics and spinor transformation rules are useful ingredients, but general Born probabilities, interference, Bell correlations, measurement independence and no-signalling must be assessed together. A classically local deterministic model with independently chosen settings cannot claim an ordinary Bell-inequality violation without identifying which assumption changes.

## 5. Current construction and evidence

### The ONE default

ONE v1 has 382 gear types, 18,592 live input monomials and 736 terms explicitly designated one-way. Its common scale is Q=2³³+1. Every forward step evaluates the fixed polynomial on the same previous snapshot, then applies Rule3 componentwise. The exact construction is selected by one_system(); Section 7 gives its definitions.

The fixed coupling graph divides the gear types into fifteen weak dependency components, or six groups when named modules are considered as whole units. A weak component groups gear types connected by input dependencies, ignoring the direction of influence. A module is a named set of related gears. Its seven-gear cosmic block is disconnected from the package. Under its documented preparation with a shared detector remainder, the detector difference has a recurrence independent of the shared detector token; changing that token therefore does not change the future hand or reader trajectory. A common engine does not by itself create communication.

### What the code and checks establish

The implementation provides exact integer state evolution, validated local polynomial support, an acyclic old-a dependency order and a staged inverse. Tests exercise complete-state recovery, arbitrary-precision fallback, fixed tensor fingerprints, remainder identities, read-only observations and specific prepared experiments. Passing these checks establishes the stated properties and tested cases, not the laws of physics.

Controlled quotient-and-remainder constructions produce exclusive events and conditional frequency identities for specified loads and remainder ensembles. Clock and field studies demonstrate particular oscillations, responses and failure regimes. Their initialization, parameter choices, observation rules and tested horizons are part of each result.

### Optional clock experiments

A new optional fixed tensor adds seven local clock types and reciprocal detector-sum feedback, for 389 types in total. Controlled initial perturbations produce downstream official-record differences; bridge-off and reverse-direction controls distinguish interaction from coincident oscillations. The same scalar Rule3 advances every register. These are chosen experimental interactions, not gravity or a complexity optimizer. The individual detector ledger changes, so its former probability interpretation cannot be copied unchanged. Detailed preparations and outcomes are in [the clock research record](CLOCK_RESEARCH.md).

A separate three-channel circuit has an exact all-time boundedness proof on its prepared Boolean sector. Two chosen local involutions are compiled into one fixed polynomial input, producing transmission, reflection and periodic clocks through Rule3 alone. All official clicks in this example are C0. It is an explicit building block, not the complete physical model or the binary-octahedral representation. [Equations, proof and actual traces](BOUNDED_CIRCUITS.md).

### Stability evidence

The original default preparation, called jpure in the code, on L=3 exceeds the declared growth limit at update 2192, while the entire computed history remains exactly reversible. Lowering only the initial matter amplitudes by a factor of sixteen gives longer quiet tested windows; slow metric drift remains. Separate even-lattice and sector-level checks are needed because a large background clock can hide growth in another field. Hand crossings are computational clock markers, not established cosmological bangs.

A separate prescribed-background clock test compares dimensionless ratios of raw official-click cycle rates. For a prescribed dimensionless field amplitude U=1/64 controlling the clock factor, a pair including a faster clock differs from common dilation by about 0.000989, exceeding the declared 0.00001 tolerance; the two slow clocks differ by about 0.000000652 and pass that restricted test. This identifies a finite-frequency limitation and a possible low-frequency regime. It does not construct a propagation metric or derive the Einstein equations. [Exact protocol and results](CLOCK_RESEARCH.md#8-gravity-means-a-shared-metric-measured-by-clocks-and-signals).

Further isolated geometric experiments provide limited constructive results. A new four-gear conformal scalar tensor gives converging common clock scaling, including an interacting clock pair, with sixteen exactly reversed histories. The optional Einstein tensor also has a prepared planar wave sector whose linear trace and divergence constraints are preserved exactly; its activity remains in the audit stream rather than official detector records. These are explicit building blocks, not general Einstein dynamics. [Geometric derivations and tests](GEOMETRY_RESEARCH.md).

A separate 18-gear [integer tensor-wave example](LINEAR_SPIN2.md) supplies an exact bounded travelling sector with two polarizations and a moving official arithmetic event pattern. The same scalar Rule3 preserves its prepared symmetry, trace and divergence constraints for all time. General three-dimensional preparations remain unstable, and no matter detector yet reads this field as a common metric.

### What remains unresolved

The visible matter doublet is not yet coupled to the rest-lapse in the way needed for universal gravitational response. Additional gauge sectors are present without a complete interacting Standard Model. Uniform and checkerboard metric modes, and runaway in the original default preparation as well as rejected couplings, limit stability claims. A general fresh-remainder mechanism, unrestricted Born statistics, Bell-consistent quantum predictions and autonomous physical time are not established.

The coupled-doublet experiment is rejected and off by default because it exhibited runaway. Additional variants, such as the Einstein extension and the CG2 gauge experiment, are also off by default and have separate configurations and tested limits. The enabled default already contains gravitational candidates and gauge layers; the system map lists them explicitly. Results from additional variants must not be attributed to that default. Retained research records include failed hypotheses and superseded choices. The current source and default fingerprint govern what is actually implemented.

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

The event-space target includes the Einstein energy and momentum constraints, their preservation by the evolution, and a consistently identified stress source. Six directed axis measurements and a local clock do not determine all ten metric components; the off-diagonal spatial components require independent observations. Section A12a defines the reconstruction and constraint obligations. A continuum interpretation must specify its refinement, physical calibration and error bounds.

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

### A0. Overview: what the algebra does

The construction has three fixed ingredients: a local state space, a coupling tensor T, and a positive scale Q. A complete seed S₀ supplies initial data. Its evolution and readout are

D = 6Q;    uₙ = T(vₙ,vₙ,vₙ);    Sₙ₊₁ = W(T,Q)(Sₙ);    Oₙ = Θ(Sₙ,Sₙ₊₁).

Here v packages the constant 1 and the local old-a and old-b inputs. Padding lower-degree terms with 1 allows the cubic notation T(v,v,v); it does not require each term to have three nonconstant factors. W is the componentwise Rule3 update, and Θ is the declared passive observation map. A separate global history chooser is not present.

The cube and quaternions provide exact symmetry data. Matrices construct linear field actions; the polynomial tensor combines these with local interactions. Retained remainders make the division invertible when the stated dependency condition holds. These ingredients explain how ONE is built, not why nature must select this particular construction.

### A1. Space, registers and degrees of freedom

Let Λ=(ℤ/Lℤ)³ with L≥3. Each site x has G gear types i=1,…,G. A link gear is stored at the base of its positively oriented spatial link; it is still one ordinary gear in the engine.

S = ((aₓᵢ,bₓᵢ,rₓᵢ))ₓ,ᵢ,    aₓᵢ,bₓᵢ∈ℤ,    0≤rₓᵢ<D,    D=6Q.

For default ONE, G=382 and Q=2³³+1. Each node therefore stores 764 unbounded signed integers and 382 finite remainders. This is not 382 continuous physical fields. A fixed remainder-parity sector has D/2 possible values per remainder.

Signed integers can be encoded by natural numbers without loss: encode(z)=2z for z≥0 and encode(z)=−2z−1 otherwise. This establishes the finite-tuple representation required by P5; it is not an extra update.

The root simulation state contains a, b and r arrays of shape (G,L³). There is no separately evolved click log, second board, hidden local time register or external control state in this representation. A diagnostic can keep a history for analysis without feeding it back.

The history of these local transitions is the proposed underlying event network (P3). Clicks are observations of that network (P7), not a second physical spacetime. The intended relativistic geometry must follow from signal and clock dynamics on the board and be confirmed by click measurements. The coordinate pair (n,x) is a computational label; it has not been shown to be an Einstein-spacetime coordinate system with an operational Lorentzian metric.

### A2. The cube, its rotations and quaternions

The orientation-preserving rotations of the cube are 24 signed 3×3 permutation matrices R with determinant +1. Quaternion units obey i²=j²=k²=ijk=−1. Unit quaternions act on a spatial vector, written as a pure imaginary quaternion, by v↦qvq⁻¹.

Define the quarter-turn lifts qₓ=(1+i)/√2, qᵧ=(1+j)/√2 and q𝓏=(1+k)/√2. The first two generate the binary octahedral group H=2O of order 48. The map H→O sends q and −q to the same one of the 24 proper cube rotations. The central element −1 acts trivially on vectors but can change the sign of a spinor.

These 48 elements are not the 24 rotations plus 24 spatial reflections. The full spatial cube group including reflections is a different group. If a model needs reflection symmetry, specify and test the action on every relevant gear and link orientation.

The implementation represents each quaternion component exactly as (m+n√2)/2 using an integer pair (m,n). Multiplication and conjugation use exact integer operations and checked divisibility. The resulting cube rotation matrices are integral. No floating-point rotation is inserted into Rule3.

### A3. The 48-gear L0 block and its matrices

The 48 L0 gear labels correspond to g∈H. Write Rg for its spatial rotation. For a world face direction d, compute the body-frame direction Rg⁻¹d. Set body actions

h₊ₓ=h₋ₓ=1;    h₊ᵧ=qᵧ;    h₋ᵧ=qᵧ⁻¹;    h₊𝓏=q𝓏³;    h₋𝓏=q𝓏⁻³.

Define πd(g)=g h(Rg⁻¹d). Choose body-axis signs s=(sₓ,sᵧ,s𝓏)∈{−1,+1}³ and set wd(g)=s_axis(Rg⁻¹d), with the same sign for both orientations of an axis. The complete default selects (1,−1,1); the standalone reference builder also supports other sign choices. The directional matrix is

[Pd]g,h = wd(g) if h=πd(g), and 0 otherwise.

Each Pd is a signed 48×48 permutation matrix. Opposite directions satisfy P−d=Pdᵀ, so three matrices determine all six. The standalone reference builder uses

uₓ = Q Σd Pd bₓ₊d.

The complete default instead selects the free L0 block built by gravity_l0c.py, with input

uₓ = 6bₓ + (Q−1)Σd Pd bₓ₊d.

Its reduced neighbor weight and on-site term move the lowest possible free-input eigenvalue from −D to −D+12. This small margin does not guarantee stability after adding interactions. The full tensor then adds lapse and source couplings, as well as other gears and interactions; neither free-block equation alone is the complete input. The helper functions retain the name “reference” for L0; that name does not invoke another engine.

Matrix entries are generated from the exact group construction before a run. Cached group products and permutation indices are representations of those fixed matrices, not additional dynamical laws or tunable routing instructions.

### A4. Representations and the role of an ideal

An L0 state can be written Bₓ=Σg bₓg[g] in the group ring ℤ[H], where [g][h]=[gh]. Equivalently,

ℤ[H] ≅ ℤ⟨Xg : g∈H⟩ / ⟨Xe−1, XgXh−Xgh⟩.

The angle brackets in the denominator denote a two-sided ideal: the imposed relations and all their algebraic consequences. This identifies equivalent expressions for composed group elements. It does not merge distinct stored states or discard remainders.

The regular action permutes group labels by left multiplication: (ρ(h)b)g=b_h⁻¹g. For a spatial field the combined rotation is (ρ(h)b)ₓ,g=b_Rh⁻¹x,h⁻¹g. Representative projections are s=Σg bg, v=Σg bg Rg e, A=Σg bg Rg A* Rgᵀ, and ψ=Σg bg g. Their transformation laws are scalar, vector, rank-two tensor and quaternionic spinor, respectively. The seed vector e and tensor A* define the projection. These projections may overlap in information and need not have closed independent dynamics.

ONE also explicitly builds field modules, rather than obtaining every field by observing L0. Its matter matrices use left and right multiplication by i,j,k and integer Kronecker products. They encode proposed Dirac-like transport and internal actions; other blocks contain link and metric candidates. These are additional representation and coupling choices within T. An abstract representation does not prove that the interacting full tensor has the desired physical symmetry.

The group ring and ideal give a precise description of the algebra. The runtime evaluates the compiled integer polynomial; it does not run an ideal-reduction algorithm or update a continuous quaternion field.

### A5. One fixed polynomial coupling tensor

For each output gear i and site x, the exact input is

uₓᵢ(a,b) = Σm:target(m)=i cm ∏f∈m z(x+δf,jf,σf).

Here cm is a fixed integer coefficient; σf is either a or b; jf is an input gear; δf is zero or a face-neighbor offset; and z(x,j,a)=aₓⱼ, z(x,j,b)=bₓⱼ. A term has at most three factors. A constant term has an empty product equal to one.

Each term reads stored registers at the output site and at most one face neighbor. Different terms may read different neighbors. Local on-site factors are allowed. This is more general than exactly one linear input per face. This storage-locality condition is distinct from geometric support: including both endpoints of link gears, 3,300 default monomials span more than one link, with maximum Manhattan diameter two. They remain finite-range local, but the stronger single-physical-link condition does not hold.

A purely matrix notation is possible after lifting the inputs: form Z(v), the vector of the required monomial products, and write u=M Z(v), where M is a fixed integer matrix. This notation does not turn the dynamics into a linear map of a and b. Omitting Z would omit the nonlinear interactions.

For example, a fixed term c·bₓ,j·bₓ+d,k has a changing effective coefficient c·bₓ,j for the second factor. It permits modulation through the state while c and the tensor remain fixed. Whether it realizes a useful gate or clutch must be tested.

The implementation validates locality, merges equal monomials and records the order needed for inversion. Its sparse coefficient representation is an implementation of this algebra, not a second changing table. Default ONE has 18,592 live monomials of degree at most three.

The optional [single-edge construction](SINGLE_EDGE_IMPLEMENTATION.md) introduces node mediators while retaining all physical link types. It has 472 gear types and zero strict support violations. Its equations, inverse proof and passive source-coordinate observation map are explicit. The map restores the Lorenz diagnostic, but the new dynamics includes extra forces and is not proved physically equivalent. It is an experiment, not the default algebra or an established physical correction.

### A6. The scalar update and the common divisor

At every gear and node, using the same old snapshot:

ℓₓᵢ, r′ₓᵢ = divmod(2uₓᵢ+rₓᵢ, D);
a′ₓᵢ = bₓᵢ;    b′ₓᵢ = ℓₓᵢ−aₓᵢ.

Euclidean division means 2u+r=Dℓ+r′ with 0≤r′<D, also for negative u. The exact recurrence is

D(b′+a) = 2u+r−r′.

Q is itself a positive integer. All tensor coefficients, seed registers and evolving registers are integers; division returns an integer quotient and an integer remainder, never a fractional register value. For example, with Q=1 and 2u+r=8, divmod(8,6) returns (1,2). Fractions used in a dispersion calculation or physical calibration are analysis of the integer history, not extra state or runtime arithmetic. A larger Q changes the allowed remainder range; it is an optional construction parameter, not a derived physical constant. Only the simultaneous scaling in A11c gives the stated equivalence between different Q values; changing Q alone changes the dynamics.

There is one shared Q and D for the complete construction, not a freely selected num/den for each gear. On the isolated L0 subspace, multiplying its coefficients and remainders by Q reproduces the divisor-six recurrence. This scaling does not make all nonlinear ONE terms equivalent to the earlier 1/1 model. Any claimed effective num/den family needs its own derivation under H7.

### A6a. Exact inverse and the distinction from a mirror

From the new state recover old b=a′ everywhere. To recover old a, process gear types in the validated dependency order. If a target input contains an old-a factor of gear j, j must have been recovered in an earlier stage. Self-dependencies and cycles in this graph are rejected.

At each stage compute the exact old input u and set

r = (r′−2u) mod D;
a = (2u+r−r′)/D − b′.

The numerator is exactly divisible by D. Induction over the dependency stages proves unique reconstruction of every register. Substitution into the forward equation proves W⁻¹W=WW⁻¹=id on valid states. For b-only tensors all targets can be inverted in one stage.

A time mirror is a separate state map X satisfying XWX=W⁻¹ when X is an involution. For b-only inputs, M(a,b,r)=(b,a,D−1−r) is such a reversor. General old-a couplings need additional conditions and possibly a more elaborate map. The full inverse proof does not automatically prove any proposed mirror, spatial reflection or physical CPT interpretation. ONE includes separate reversor checks for the stated constructions.

### A7. The node code and how nodes connect

The following scalar function is the exact arithmetic performed per gear. The production engine evaluates many gears at once and uses checked int64 bounds with arbitrary-precision fallback; the mathematical operation is the same.

```python
def rule3(a: int, b: int, r: int, u: int, D: int):
    quotient, r_next = divmod(2 * u + r, D)
    return b, quotient - a, r_next
```

For a node x, first evaluate its G inputs uₓ from the fixed tensor and the old snapshot of that node and its six neighbors. Apply rule3 to each local triple. Store all resulting triples in a new snapshot. The full network step commits that snapshot only after all nodes have read the old one. This prevents the evaluation order from becoming an unintended extra law.

The repository's core/tensor.py constructs and validates the inputs; core/engine.py implements the shared step and inverse; layers/one.py selects the default tensor; prepare/one.py constructs the seed; observe/ computes diagnostics. The run loop repeatedly calls Engine.step. There is no separate update for a spinor, vector, clock or click.

The [system map](SYSTEM_MAP.md) identifies the actual dependency graph and gives the inverse/locality argument with its scope. The default has six independent namespace groups; the common engine does not couple them merely by evaluating them in one array. Field names, observer labels and link metadata do not change the numerical update for a fixed indexed polynomial.

### A8. The seed, vacuum and what remains free

Choose the fixed tensor and its parameters, L, and every initial a,b,r value before the run. Default ONE's background construction uses r*=3Q−1 where its complete system preparation specifies that vacuum. The standalone L0 builder also supports the Q-scaled r=2Q vacuum for its isolated arithmetic tests. Use the declared preparation for the selected construction.

The seed can contain localized packets, static loads and correlated remainders. These are inputs, not derived physical facts. A seed ensemble specifies how different preparations are sampled. The engine performs no new random draw during evolution.

The default jpure preparation uses floating-point projection and norm matching to choose an integer seed. Forward evolution then uses exact arithmetic only. Exporting the complete integer seed gives reproducible input; a random-seed number alone does not guarantee identical preparation across numerical-library versions.

The degrees of freedom to investigate are the tensor construction, its coefficient choices, geometry, initial state and declared observation map. Changing the tensor changes the model; changing only the seed changes the preparation. The current number of gears, masses, gauge content and coupling constants are not uniquely derived from Rule3 or from 24 cube rotations.

### A9. What a click is in the implemented code

For two consecutive snapshots define ℓ=b′+a. An official-stream event requires ℓ≠0 and (a′,b′,r′)≠(a,b,r). A raw carry stream drops the second condition and must be labeled separately.

Let δ=(r′−r) mod D. Its arithmetic class is C0 for δ=0 or δ=D/2; C1 for 0<δ<D/2; and C2 for D/2<δ<D. At D=6 this agrees with the original three-class remainder convention. Gear metadata additionally labels observables as official or audit; select the declared observable sector explicitly.

This classification is calculated after a transition. It does not choose the transition, erase alternatives, or impose an entropy gradient. A physical record and its backreaction must come from gears already present in T. A C2 event is not, by definition, collapse of a wavefunction.

For the default matched cosmic preparation, without the optional sum bridge, ell_dp−ell_dm=I and Delta_b_next=I−Delta_a, where I=b_M1²+b_M2². Together with the hand's dependence on the recording pair only through Delta, this makes its future reader/hand history independent of the load split and token under the declared conditions. The [explicit proof](SYSTEM_MAP.md#a-precise-obstruction-to-the-current-choice-interpretation) rules out describing these records as selecting different future hand/reader trajectories in this preparation.

### A10. Exact identities and conditional statistics

Since 2u and D are even, r′≡r (mod 2). The exact quotient ledger for a fixed gear over N steps is

D Σₙ₌₀ᴺ⁻¹ ℓₙ = 2 Σₙ₌₀ᴺ⁻¹ uₙ + r₀−rN.

This identity is not an assertion of positive physical energy. Physical balances require identifying the relevant stored quantity, spatial flux and source terms in the selected tensor, including the remainder contribution.

If K=2u is fixed with 0≤K<D and r is sampled uniformly from 0,…,D−1, precisely K choices of r produce a carry, giving P(ℓ=1)=K/D. On a fixed-parity sector the analogous count must respect that sector and the even input. Inputs proportional to squared amplitudes can therefore yield Born-like conditional counts in constructed preparations. Independence, renewed uniformity, arbitrary sequential measurements and general quantum statistics do not follow from this counting identity.

A reciprocal b-only subset may satisfy uᵢ=sᵢ∂Φ/∂bᵢ for a common polynomial potential Φ and fixed field signs sᵢ. ONE checks the stated reciprocity conditions and explicitly lists one-way exceptions. The complete default includes 736 designations. Do not identify the whole tensor with a conservative Hamiltonian or omit the exact remainder term when comparing with a continuous equation.

### A11. Clock spectra, families and physical limits

For a linear b-only input u=Bb, ignoring the bounded remainder correction gives bₙ₊₁+bₙ₋₁≈(2/D)Bbₙ. A mode with B-eigenvalue β has cos ω≈β/D. Oscillatory modes require |β|<D; the endpoints can have marginal or drifting solutions, and values outside this interval allow growth. Nonlinear couplings and remainder forcing require additional stability analysis.

A mode gap, a recurrence period or a velocity is not a complete effective Rule3 law and is not yet physical mass or light. A traveling packet must be distinguished from a sequence of similar readouts at fixed sites. Demonstrating synchronized or assembled clocks requires reproducible observables and perturbation tests.

### A11a. Optional connected clocks: fixed tensor data

The optional clock network adds one master-clock gear and one clock gear per selected sector **at every node**. A master gear is a local register, not a global variable read by every node. Quadratic springs couple these clocks; optional face-neighbor springs transmit clock disturbances locally. The clock-only input is

u_C = (D/2)C + Σ_j k_j(C_j−C).

Here C and C_j denote the current b values of clock gears, and k_j are fixed nonnegative integer spring coefficients. The spring language describes these polynomial couplings, not a separately applied mechanical force law.

An isolated clock with this coefficient obeys b′=b−a exactly and keeps its remainder unchanged, hence has a period dividing six. Connecting clocks changes their normal modes; it does not prove an attracting synchronized state. All new clocks require explicit initial a,b,r values.

Field ports use complete declared multiplets. For a diagonal integer quadratic form E=Σ_i w_i(b_i+v_i)², define the chosen interaction

Φ_port = −λ C²(E−E₀)/2,
Δu_C = −λ C(E−E₀),
Δu_i = −s_i λ C²w_i(b_i+v_i).

Here λ is a fixed integer coupling, E₀ is a fixed reference value, v_i are fixed affine shifts from stored deviations to full fields, and s_i∈{−1,+1} is the field sign. These are integer input polynomials of degree at most three. Subtracting E₀ can cancel the clock's vacuum input; it does not generally cancel the reciprocal force on a shifted field. A physical-link multiplet couples symmetrically to the clocks at its two endpoints. Every added term has single-edge physical support. This does not remove existing wider-support terms in the source tensor.

The quadratic form must be invariant under the representation being claimed. The catalogue uses complete reference, matter, Higgs and gauge-matter multiplets and the spatial metric Frobenius form. It does not use an electromagnetic-potential norm, which is not gauge invariant. Covariance of an added polynomial is not a proof of continuous gauge covariance of the full rounded dynamics or Lorentz invariance. The resulting dependency graph is connected, but a homogeneous zero field can remain unexcited: a graph path alone is not a signal experiment.

### A11b. Record backreaction without a click callback

The default matched pair is read only through its difference, which is blind to the shared initial detector token under the conditions in A9. A new optional scalar bridge reads the sum as well:

Φ_bridge = −κ C(d_p+d_m),
Δu_C = −κ(d_p+d_m),
Δu_dp = Δu_dm = −κ C.

The three gears are on-site scalar gears with sign +1. This reciprocal, degree-one addition changes the fixed tensor before the run; it adds no rule after an observed click. A token-dependent record can now affect a future clock state. The matched-pair difference and shared remainder lock survive because the same force enters both detectors. Their individual quotient ledgers change, however:

Write the original positive detector input as c I L_p, where c is its fixed integer coefficient, I=M1²+M2² is the reader intensity and L_p is its stored positive load. The sum below is over the observed updates:

D Σℓ_p = 2c ΣI L_p − 2κ ΣC + r_p,0−r_p,N.

The previous individual probability interpretation cannot be copied without this term. A controlled isolated example changes the shared initial detector remainder while keeping loads fixed; the records change at step one and the clock at step two. Removing the bridge removes that clock response. This proves a route for record backreaction, not an optimizer, wavefunction collapse, quantum entanglement or a preference for complexity.

### A11c. Resolution, stability and the scope of the clock metaphor

For any positive integer M, an exact change of integer resolution is

T_M=MT,  Q_M=MQ,  E_M(a,b,r)=(a,b,Mr),
W(T_M,Q_M) E_M = E_M W(T,Q).

This follows from divmod(M(2u+r),MD)=(ℓ,Mr′). It preserves baseline a,b histories, quotients and click classes exactly. It embeds them in a subset of the larger remainder space. Adding small integer interactions afterwards defines a new model; the identity applies to its zero-added-coupling control. A newly computed vacuum 3MQ−1 generally differs from the required lifted remainder M(3Q−1). Specialized mirror or seed-symmetry statements require new checks.

Resolution lifting does not cure an unstable source history. The isolated metric row has u=6b+(Q−1)Σ_neighbors b, giving the even-lattice checkerboard eigenvalue β=−D+12. Negative on-site stiffness can push this mode out of the oscillatory band. Odd periodic grids omit the exact checkerboard mode, so even-grid controls are required. A continuous confining quartic potential also does not imply bounded discrete Rule3 motion: a cubic restoring force can overshoot and produce an escaping recurrence at sufficiently large amplitudes.

The retained remainders matter even inside that linear band. On an even cube, a prepared free metric mode has bₓ(n)=(−1)^(x+y+z+n)(B+vn) over an explicitly proved finite interval while its remainders remain within range. For v=0 the complete state has period two; for B=512, v=1 and the default Q, the interval exceeds two billion updates. One million updates and their inverses were checked in the exact two-sublattice reduction, with a separate full-engine prefix check. This is a high-frequency counterexample to an unrestricted stability claim, not a rejection of every smooth continuum limit. The [metric-source audit](METRIC_SOURCE_AUDIT.md) gives the seed, proof and executable checks.

The [clock research record](CLOCK_RESEARCH.md) separates algebraic identities, finite-horizon controls, rejected integrations and physical targets. Hand zero crossings, reader-state echoes and full-state recurrence are separate diagnostics. None is by itself a cosmological bang. A deterministic local clock network with independent measurement settings and all trials counted obeys the Bell–CHSH bound; connecting its clocks does not evade that theorem.

### A11d. An exactly bounded routing and clock example

A separate small experiment gives an all-time invariant-sector proof, rather than extrapolating a finite run. Choose two local polynomial maps 𝒫 and 𝒥 that are involutions on a finite domain: applying either twice returns the input. Compile the fixed input

u=(D/2)[𝒫(b)+𝒥(b)],    a₀=𝒫(b₀).

Ordinary Rule3 gives (a′,b′,r′)=(b,𝒥(b),r). Because 𝒥²=id, the next state lies on a=𝒥(b), and the following step gives b′=𝒫(b). The two prepared phase graphs alternate automatically through the two-time registers. There is no extra gate call or runtime phase switch. If both maps preserve Boolean states, a and b remain Boolean and r remains fixed at every time. On a finite board, reversibility then proves periodicity.

With E(b,r)=(𝒫(b),b,r), this is the exact embedding identity W²E(b,r)=E(𝒫𝒥(b),r). It recovers a complete two-step circuit transition, not just one matching frequency. It does not yet produce an effective Rule3 family with a different num/den ratio.

The concrete example has three node channels: a retained control c and two data channels L,R. The local controlled swap is 𝒫(c,L,R)=(c,L+c(R−L),R+c(L−R)), with c∈{0,1}. The wire map swaps R(x) with L(x+e) for one chosen axis e. Both are involutions on the prepared Boolean sector; the compiled input is quadratic and strictly single-edge local. Four control-dependent terms are explicitly nonreciprocal. Arbitrary mismatched two-time seeds are outside the boundedness proof.

The [bounded-circuit example](BOUNDED_CIRCUITS.md) shows exact transmission, reflection and periodic clocks using the same fixed tensor and different complete seeds. Its controls are retained static data, not a complexity optimizer. Its clicks all have class C0, so routing does not require or establish C2 collapse. This is a selected circuit within the common Rule3 engine, not the default field model, a full cube-symmetric construction, or a derivation of light, mass, gravity or quantum entanglement.

### A12. Gravity candidates and the cosmic block

ONE includes ten metric-labeled gears, but the default coupling uses a much narrower gravitational mechanism. Lapse denotes a candidate factor relating local clock rates to the computational coordinate; it is not physical proper time until calibrated. The L0 sector participates in a coupled lapse construction. The visible doublet still lacks the universal rest-clock response required by the equivalence principle.

Weak-field response and inverse-distance source studies are evidence within specified constructions. Chosen site and link coefficients can reproduce desired leading-order factors, so those factors must not be presented as uniquely derived from Rule3. Optional Einstein-layer calculations are not a derivation of full general relativity for default ONE.

The gravitational target is geometry, not an additional attraction between clocks. Infer a common metric g from local clock intervals and signal travel through links, then require it to predict free fall and the observations of other species without separate fits. In a continuum limit, massive test bodies should follow its timelike geodesics and light its null cones; the metric must itself obey the appropriate source and constraint equations. A causal graph or ten metric-labeled gears alone does not establish this.

The rank-four coupling tensor T is not the spacetime metric. Its indices describe polynomial inputs. A physical spacetime metric g is a rank-two object inferred from clock and signal measurements. Its state-dependent values and curvature would have to emerge under the fixed update law.

Even common rest coefficients need a calibration check. Write F=metric.h00 and U=F/(2P), where P is the fixed integer normalization of this field. The current second-order reference clock coupling has the remainder-free relation sin(ω(U)/2)/sin(ω₀/2)=√(1−2U). In that approximation, its raw frequency ratio is 1−[2tan(ω₀/2)/ω₀]U+O(U²), which depends on the clock's rest frequency. A universal low-frequency limit, all-species transport, metric sources and the Einstein equations remain requirements. The optional clock springs and norm ports above are experimental interactions and are not identified as gravity.

The cosmic block contains a hand Θ_c (the gear cosmic.Th), two readers M1,M2, two loads Lp,Lm and two record gears dp,dm. This hand is distinct from the observation map Θ in A0. Its tensor defines their interactions. A hand crossing zero can organize a diagnostic time interval, but it does not reset or reseed the board. Exact forward and inverse histories retain the whole state through the crossing.

### A12a. Reconstructing geometry and preserving Einstein constraints

A general metric relates locally measured times and spatial separations. In units where the calibrated speed of light is one, write

ds² = −N²dt² + γᵢⱼ(dxⁱ+βⁱdt)(dxʲ+βʲdt).

Here γ is the positive spatial metric, N is the lapse relating coordinate time to clocks moving normally to a spatial slice, and β is the shift between successive spatial coordinate labels. A clock fixed at a board coordinate measures dτ/dt=√(N²−γᵢⱼβⁱβʲ), which equals N only when the shift is zero. The coordinates are descriptive labels, not an assumed universal physical clock.

The local reconstruction can be written explicitly. Let α=dτ_fixed/dt be the calibrated rate of a clock fixed in these coordinates, and t₊,t₋ the forward and reverse signal travel times over coordinate displacements ±ℓn. For constant metric coefficients in the measured patch, the null-interval equation gives

B(n)=g₀ᵢnⁱ=α²(t₊−t₋)/(2ℓ),
Γ(n)=γᵢⱼnⁱnʲ=α²t₊t₋/ℓ².

Once the full positive matrix γ and the components Bᵢ are determined, β=γ⁻¹B and N²=α²+Bᵀγ⁻¹B. These are reconstruction identities conditional on physical clock and signal measurements; they do not assume that the present gears already provide those measurements.

Clock rates together with independent directional signal travel times can reconstruct these coefficients under a declared synchronization and scale convention. In a locally approximately stationary, constant patch, or an appropriate local refinement limit, the six directed axis measurements determine the time-space components and spatial diagonal, but leave three spatial off-diagonal entries undetermined. Travel times through a varying field instead depend on the whole path. Independent oblique propagation or other calibrated observations are required. The [geometry research](GEOMETRY_RESEARCH.md) derives the inverse formulas and an exact axis-data ambiguity.

The current scalar lapse construction has a restricted slow-wave interpretation. For U=F/(2P), its rest coefficient is N²=1−2U and transport coefficient is C=1−4U. In the uniform weak-field, low-frequency limit they fit a spatial scale A²=N²/C and ds²=−N²c₀²dt²+A²d𝐱², where c₀ is the flat low-frequency propagation speed. This is an inferred kinematic candidate from selected coefficients. Finite-frequency effects, spatial variation, remainders and other species require additional checks. A separate [conformal scalar experiment](CONFORMAL_METRIC_EXPERIMENT.md) gives a controlled common clock limit for another chosen tensor; it does not supply general Einstein geometry.

Einstein dynamics requires more than reconstruction. Let Kᵢⱼ measure the change of the spatial geometry normal to a slice, K=γⁱʲKᵢⱼ its trace, and ³R the curvature scalar of that spatial metric. Let ρ and jⁱ be independently identified physical energy and momentum densities. Initial data must satisfy the energy constraint and three momentum constraints:

³R + K² − KᵢⱼKⁱʲ = 16πG_eff ρ + 2Λ,
∇ⱼ(Kⁱʲ−γⁱʲK) = 8πG_eff jⁱ.

The derivative ∇ is defined by γ; indices are raised with its inverse. G_eff is the effective gravitational coupling to be inferred and calibrated, and Λ is a possible cosmological term. These are target physical parameters, not additional runtime update functions. The remaining metric evolution equations and local stress conservation must also follow from the same construction. The physical stress tensor is distinct from the fixed polynomial coupling tensor T.

An exact encoded constraint sector requires that both Rule3 and its inverse preserve all its defining constraints, with the retained remainders included. A continuum claim instead needs a specified refinement and bounds showing the physical constraint residuals vanish. A prepared planar tensor-wave sector in the optional Einstein example preserves its linear trace and divergence constraints exactly, but its activity is audit-only and the general nonlinear constraints have not been obtained. Stored off-diagonal fields currently can be invisible to the other sectors, and the implemented source has a conservation defect.

A separate [integer tensor-wave construction](LINEAR_SPIN2.md) gives an exact propagating building block. Two 3×3 arrays E and B use 18 ordinary gears and fixed inputs u_E=(D/2) curl B, u_B=(D/2) curl E, where curl acts on each tensor column through face-neighbor differences. The scalar Rule3 preserves prepared symmetry, zero trace and zero divergence without dropping remainders. A particular preparation makes every two updates translate arbitrary integer profiles two cells with a fixed sign; amplitudes are bounded for all time. Its official arithmetic clicks carry the travelling pattern. General three-dimensional preparations can still grow, and these fields are not yet a metric measured by matter or detectors. This example does not change the default construction or establish nonlinear Einstein dynamics.

A subsequent [local metric experiment](PHASE_METRIC_EXPERIMENT.md) adds two internal phase registers, themselves updated by Rule3. A fixed quadratic expression in the registers reconstructs a travelling metric perturbation at every update. Its linearized Ricci tensor and linear energy/momentum constraints vanish exactly for the explicitly declared central-difference operator. A separate one-way, rank-four probe coupling changes actual official detector records. This is still a restricted test-body construction: the phase registers themselves emit no official clicks, the wave and probe speeds differ, and reciprocal backreaction and nonlinear Einstein constraints are absent. In the chosen transverse wave gauge, fixed-coordinate rest clocks have no first-order slowing; the tested response is spatial propagation.

The [Palatini target](PALATINI_TARGET.md) expresses a possible geometric starting point using a local coframe e and metric g=eᵀηe, where η is the Minkowski signature matrix. Its quartic gravitational action makes low polynomial degree plausible, but its first-order constraints, physical link support and matter coupling require a separate reversible construction. The current work does not derive a complete Einstein event spacetime.

### A12b. Integer reciprocal examples and their limits

Separate integer reciprocal examples use Q=1 and D=6, including explicitly integer seeds. A two-gear, order-four spatial potential Phi=sum_x(3e_x^2+7chi_x^2)-sum_edges(1+e_x^2+e_y^2)(chi_y-chi_x)^2 has a prepared complete-state period-five orbit. Its positive integer link coefficients change between one and three, and same-tensor initial-only controls change the opposite field's official records. This is a standing periodic interaction, not an operational metric; the same tensor also has a proved unbounded preparation.

A separate node-flux construction produces diagonal and off-diagonal official detector responses with strict single-edge support. All fields use the same scalar Rule3 and complete flat transport block, but their response on curved backgrounds is not universal. The reciprocal sources fail the required constraints, and finite response runs grow rapidly. Reciprocal coupling, exact reversal and a nonzero detector response do not establish Einstein dynamics.

The source-constraint analysis also proves an independent compatibility condition: every spatially periodic flat linearized Einstein field has zero spatial sum of G00. It therefore cannot have nonzero nonnegative total matter density as its source. A consistent homogeneous dynamical background or boundary contribution and a conserved discrete stress source are needed. These are precise limitations of the stated target, not a no-go theorem for all integer Rule3 constructions.

See [the complete integer constructions and proofs](INTEGER_RECIPROCAL_GEOMETRY.md) and [the source-constraint analysis](DYNAMICAL_GEOMETRY_CONSTRAINTS.md). These are optional experiments; the default tensor is unchanged.

### A13. Validation and source of truth

The executable source of truth is the public repository's default one_system() construction and its tests. The default dynamics fingerprint is 77f6d251a8adfb2e4727bd2bd5ffeaa0e2ae3538aac393fe95c497fce754acf6. This identifies the indexed polynomial dynamics; it is not a physical validation certificate.

The compatibility field name dynamics_fingerprint excludes Q. A complete law identifier is (dynamics_fingerprint, Q), or the full tensor fingerprint when Q is recorded. Rank four, exact arithmetic and a fixed tensor specify an executable construction; they do not establish all of its proposed physical interpretations.

The repository migration preserves the default complete-state traces and keeps the exact cube algebra inside ONE. The old independent runtime is available only through Git history. Its results are not silently reclassified as ONE results. Current validation commands and actual outcomes are recorded in docs/VALIDATION.md.

[Public code and run instructions](https://github.com/Closer24/Universe24)
[Current algebra](https://github.com/Closer24/Universe24/blob/main/docs/MODEL.md)
[Default construction](https://github.com/Closer24/Universe24/blob/main/universe24/layers/one.py)
[Exact engine](https://github.com/Closer24/Universe24/blob/main/universe24/core/engine.py)
[Validation record](https://github.com/Closer24/Universe24/blob/main/docs/VALIDATION.md)
[Research status and limitations](https://github.com/Closer24/Universe24/blob/main/docs/RESEARCH_STATUS.md)

The remaining research obligations are to establish stable, interacting structures, operational physical time, the required click-level laws and a tested mechanism for H16 if that hypothesis is retained. ONE provides a precise starting construction; it does not settle these obligations by naming its gears after physical quantities.
