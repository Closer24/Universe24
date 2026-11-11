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

The quarter-turn lifts qₓ=(1+i)/√2 and qᵧ=(1+j)/√2 generate the binary octahedral group H=2O of order 48. The map H→O sends q and −q to the same one of the 24 proper cube rotations. The central element −1 acts trivially on vectors but can change the sign of a spinor.

These 48 elements are not the 24 rotations plus 24 spatial reflections. The full spatial cube group including reflections is a different group. If a model needs reflection symmetry, specify and test the action on every relevant gear and link orientation.

The implementation represents each quaternion component exactly as (m+n√2)/2 using an integer pair (m,n). Multiplication and conjugation use exact integer operations and checked divisibility. The resulting cube rotation matrices are integral. No floating-point rotation is inserted into Rule3.

### A3. The 48-gear L0 block and its matrices

The 48 L0 gear labels correspond to g∈H. Write Rg for its spatial rotation. For a world face direction d, compute the body-frame direction Rg⁻¹d. Set body actions

h₊ₓ=h₋ₓ=1;    h₊ᵧ=qᵧ;    h₋ᵧ=qᵧ⁻¹;    h₊𝓏=q𝓏³;    h₋𝓏=q𝓏⁻³.

Define πd(g)=g h(Rg⁻¹d). A chosen sign s for each body axis supplies the weight wd(g). The directional matrix is

[Pd]g,h = wd(g) if h=πd(g), and 0 otherwise.

Each Pd is a signed 48×48 permutation matrix. Opposite directions satisfy P−d=Pdᵀ, so three matrices determine all six. For the isolated L0 block,

uₓ = Q Σd Pd bₓ₊d.

This is the matrix form of the fixed L0 coupling actually used by the builder. The complete ONE tensor adds other gears and terms, so this equation alone is not the complete ONE input. Its helper functions retain the name “reference” for this L0 block; that name does not invoke another engine.

Matrix entries are generated from the exact group construction before a run. Cached group products and permutation indices are representations of those fixed matrices, not additional dynamical laws or tunable routing instructions.

### A4. Representations and the role of an ideal

An L0 state can be written Bₓ=Σg bₓg[g] in the group ring ℤ[H], where [g][h]=[gh]. Equivalently,

ℤ[H] ≅ ℤ⟨Xg : g∈H⟩ / ⟨Xe−1, XgXh−Xgh⟩.

The angle brackets in the denominator denote a two-sided ideal: the imposed relations and all their algebraic consequences. This identifies equivalent expressions for composed group elements. It does not merge distinct stored states or discard remainders.

Under the regular action, representative projections are s=Σg bg, v=Σg bg Rg e, A=Σg bg Rg A* Rgᵀ, and ψ=Σg bg g. Their transformation laws are scalar, vector, rank-two tensor and quaternionic spinor, respectively. The seed vector e and tensor A* define the projection. These projections may overlap in information and need not have closed independent dynamics.

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

The degrees of freedom to investigate are the tensor construction, its coefficient choices, geometry, initial state and declared observation map. Changing the tensor changes the model; changing only the seed changes the preparation. The current number of gears, masses, gauge content and coupling constants are not uniquely derived from Rule3 or from 24 cube rotations.

### A9. What a click is in the implemented code

For two consecutive snapshots define ℓ=b′+a. An official-stream event requires ℓ≠0 and (a′,b′,r′)≠(a,b,r). A raw carry stream drops the second condition and must be labeled separately.

Let δ=(r′−r) mod D. Its arithmetic class is C0 for δ=0 or δ=D/2; C1 for 0<δ<D/2; and C2 for D/2<δ<D. At D=6 this agrees with the original three-class remainder convention. Gear metadata additionally labels observables as official or audit; select the declared observable sector explicitly.

This classification is calculated after a transition. It does not choose the transition, erase alternatives, or impose an entropy gradient. A physical record and its backreaction must come from gears already present in T. A C2 event is not, by definition, collapse of a wavefunction.

For the current matched cosmic preparation, ell_dp−ell_dm=I and Delta_b_next=I−Delta_a, where I=b_M1²+b_M2². Together with the hand's dependence on the recording pair only through Delta, this makes its future reader/hand history independent of the load split and token under the declared conditions. The [explicit proof](SYSTEM_MAP.md#a-precise-obstruction-to-the-current-choice-interpretation) rules out describing these records as selecting different future hand/reader trajectories in this preparation.

### A10. Exact identities and conditional statistics

Since 2u and D are even, r′≡r (mod 2). The exact quotient ledger for a fixed gear over N steps is

D Σₙ₌₀ᴺ⁻¹ ℓₙ = 2 Σₙ₌₀ᴺ⁻¹ uₙ + r₀−rN.

This identity is not an assertion of positive physical energy. Physical balances require identifying the relevant stored quantity, spatial flux and source terms in the selected tensor, including the remainder contribution.

If K=2u is fixed with 0≤K<D and r is sampled uniformly from 0,…,D−1, precisely K choices of r produce a carry, giving P(ℓ=1)=K/D. On a fixed-parity sector the analogous count must respect that sector and the even input. Inputs proportional to squared amplitudes can therefore yield Born-like conditional counts in constructed preparations. Independence, renewed uniformity, arbitrary sequential measurements and general quantum statistics do not follow from this counting identity.

A reciprocal b-only subset may satisfy uᵢ=sᵢ∂Φ/∂bᵢ for a common polynomial potential Φ and fixed field signs sᵢ. ONE checks the stated reciprocity conditions and explicitly lists one-way exceptions. The complete default includes 736 designations. Do not identify the whole tensor with a conservative Hamiltonian or omit the exact remainder term when comparing with a continuous equation.

### A11. Clock spectra, families and physical limits

For a linear b-only input u=Bb, ignoring the bounded remainder correction gives bₙ₊₁+bₙ₋₁≈(2/D)Bbₙ. A mode with B-eigenvalue β has cos ω≈β/D. Oscillatory modes require |β|<D; the endpoints can have marginal or drifting solutions, and values outside this interval allow growth. Nonlinear couplings and remainder forcing require additional stability analysis.

A mode gap, a recurrence period or a velocity is not a complete effective Rule3 law and is not yet physical mass or light. A traveling packet must be distinguished from a sequence of similar readouts at fixed sites. Demonstrating synchronized or assembled clocks requires reproducible observables and perturbation tests.

### A12. Gravity candidates and the cosmic block

ONE includes ten metric-labeled gears, but the default coupling uses a much narrower gravitational mechanism. Lapse denotes a candidate factor relating local clock rates to the computational coordinate; it is not physical proper time until calibrated. The L0 sector participates in a coupled lapse construction. The visible doublet still lacks the universal rest-clock response required by the equivalence principle.

Weak-field response and inverse-distance source studies are evidence within specified constructions. Chosen site and link coefficients can reproduce desired leading-order factors, so those factors must not be presented as uniquely derived from Rule3. Optional Einstein-layer calculations are not a derivation of full general relativity for default ONE.

The cosmic block contains a hand Θ, two readers M1,M2, two loads Lp,Lm and two record gears dp,dm. Its tensor defines their interactions. A hand crossing zero can organize a diagnostic time interval, but it does not reset or reseed the board. Exact forward and inverse histories retain the whole state through the crossing.

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
