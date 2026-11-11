# ONE algebra

This is the current implementation specification. The broader motivations and postulates are in [the research proposal](RESEARCH_PROPOSAL.md).

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
