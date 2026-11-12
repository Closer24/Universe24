# Cube/clock research: evidence checkpoint after environment loss

This is an **evidence recovery checkpoint, not the complete implementation PR**.

The managed execution environment became unavailable during final integration validation. The new Python modules, tests, source reports and normal bundle metadata remained in the local checkout when access was lost. Only the already uploaded, hash-verified compressed blobs are included here. Do not describe this branch as a runnable publication of the new implementation or as a passing final integration check.

Tracking: https://github.com/Closer24/Universe24/issues/62

## What was completed and observed before the interruption

Seven delegated research lanes completed: cube algebra; native spatial evolution; clock relations; complexity/epochs; spatial Einstein constraints; chirality; independent review.

- Full local discovery on the PR59 source baseline: **447 tests passed in 220.192 seconds**, including 42 new tests.
- Eight research/runtime audits passed. The compressed reports below retain the actual measured states and scoped claims.
- All recorded source maps were rechecked after rebasing onto central integration `e2d29499df418f498f7d81ec1a8cf1dd9e4db6a6`; they still matched.
- Fresh generic smoke/replay on that integration source passed.
- Discovery found 459 tests on that source. **The outcome of that final full run was not received** before the environment disappeared.
- A newer central head `bf6c2944267fdf4223eb0893ce8f496223fd0aa1` was observed subsequently. Its anisotropic source additions were inspected through GitHub but are not claimed as locally integrated/tested here.
- Original local implementation commit before the integration rebase: `474d4ec`. Checkout: `/workspace/scratch/d01c5ea2900a/universe24-cube`, local branch `research/cube-clock-cycles`. The rebased local commit ID was not captured. Neither local implementation commit was published.

## The exact algebraic connection

There are three distinct objects:

| Object | Cardinality | Meaning |
|---|---:|---|
| Proper cube rotations | 24 | Spatial rotations preserving orientation |
| Full cube spatial group | 48 | Rotations plus orientation-reversing mirrors |
| Binary octahedral spin lift | 48 | A double cover of the 24 proper rotations |

The two groups of order 48 are different. The spin lift has order-eight elements; the full spatial group does not. Internal quaternion actions, spatial spin actions and coordinate parametrizations called “spinor” are not automatically the same physical representation.

Every transformation must act on the complete retained state. For an odd input law, the already-existing negation
`J(a,b,r)=(-a,-b,5-r)`
commutes exactly with Rule3 because
`divmod(-2u+5-r,6)=(-ell,5-r_next)`.
Negating a,b while leaving r unchanged generally fails. The existing parity-preserving Jp is another valid convention.

A reusable construction is an integer symmetry-orbit sum of a node/one-face potential of degree at most four. Its gradient is a covariant force of degree at most three. The representation must preserve ownership and support; a signed-gradient signature must commute with the representation. A b-only construction preserves the acyclic old-history contract. Symmetry alone does not prove Einstein equations, energy conservation, stability or physical chirality. Including mirrors in the averaging enforces parity, so it cannot silently describe parity-violating couplings.

## One actual spatial control

The shared candidate uses two scalar carrier channels, six retained integers per node, twelve linear face terms, and no hidden workspace:

`u_g(x) = sum of b_g(y) over the six face neighbors y`.

The unchanged update is
`ell,r_next=divmod(2*u+r,6); a_next=b; b_next=ell-a`.

Tensor SHA-256:
`3bc4972b821458041ed521160146ef3bc7a59a75c60938e900aaa920701c0981`.

The native audit made 59,976 independent scalar-register comparisons, checked inverse/rewind, all six carry classes, all 48 cube actions and eight internal signed actions. Exact shift charges are sums of `6(b-a)+r`. Removing one face or discarding carries breaks relevant checks.

Two saved runtime histories use this tensor:
- 27-node structured preparation, 48 steps, exact complete period 12.
- 125-node irregular mixed-carry preparation, 36 steps.

The two passive observers consume the same saved complete history, bound by tensor/seed/model/run/trace receipts. Both runs peak at five magnitude bits. A separate arbitrary-precision fixture reaches 75 bits.

Clock relation: both endpoint carrier vectors nonzero, dot product positive, and `4*cross^2 <= dot^2`; persistence requires two snapshots. Connected components are correlation proxies, not proved bound states. On the structured trajectory the largest component grows **6 → 23 → 6**, returning at tick 12. All aggregate diagnostics were invariant under all 48 spatial actions across 49 checkpoints.

Complexity protocol: undirected dot/cross-sign edge labels, sorted six-face motifs, and currently repeated nonuniform motifs persisting for two checkpoints. Activity peaks are strict interior maxima of changed edge labels. At least four peaks are required; the score must strictly increase at every successive peak. The declared growth criterion failed on both recurrent and irregular preparations. These peaks are not identified as cosmological bangs.

## What increasing complexity between bangs would require

Repeated macroappearance may coexist with different complete microstates. Exact complete recurrence cannot have a different deterministic future, so a current-state complexity cannot strictly increase around the same complete cycle. Fixed-window observations also repeat after their window fills.

For N nodes, G channels and histories satisfying |a|,|b| < 2^B, the complete-state capacity is at most:

`6^(G*N) * (2^(B+1)-1)^(2*G*N)`.

Indefinitely distinct epochs on a fixed board therefore require unbounded retained bit capacity or new degrees of freedom. A new epoch must retain distinctions from its predecessors; a reset erasing the old complete state is incompatible with the retained reversible law.

This does not forbid finite complexity growth from a special initial condition or growth in an unbounded state space. It does not prove that bits are physical complexity. The motif proxy can score random patterns positively and is bounded by N/2. A nonzero uniform native fixed point remains on a plateau without any subsequent peak.

The independent reviewer also found an even-side solution of the same tensor with amplitude `(-1)^t*(t+1)` times a spatial checkerboard. It reaches amplitude 65 after 64 ticks and grows without bound, while relational activity and motif organization remain zero. Thus arithmetic cost and structural organization are distinct.

## Einstein, mass and spatial dependence

The massive homogeneous model already present in PR60 is a separate physical sector. Mass changes local matter dynamics; spatial dependence introduces gradients, curvature and momentum transport.

For the repository sign convention K^i_j = k delta^i_j:
`D_j K^j_i - D_i K = -2 partial_i k`.

A flat slice with k = -(2+sin x), scalar velocity p=2, phi=0, and dust density `3(2+sin x)^2-2` obeys the onsite Hamiltonian constraint but violates the momentum constraint by `(2 cos x,0,0)`. A real 27-node nonuniform PR59 negative control preserves every onsite invariant and rewinds, while its spatial momentum constraint fails. The homogeneous decoder correctly rejects it.

Einstein's construction links rods/clocks, geodesic motion, the metric and matter conservation; clock phase alone does not select the field equation. Primary reference: https://www.gutenberg.org/files/66944/66944-h/66944-h.htm (1916 paper, sections 2, 9, 16–18, 22).

A global Engine tick can order events; material clocks must measure proper time from the same metric that governs matter and geometry. CPU wall time or bit cost does not supply that metric.

## Handedness boundary

The audited Clifford volume/chirality changes under parity; the mass operator exchanges the audited complementary sectors. Internal quaternion generators commute with the spatial Clifford action. These are exact algebraic facts, not a physical chiral spectrum in the running scalar control.

The historical chiral family requires 72 channels with its two-path auxiliaries. Matter32 + Higgs4 + weak links12 already exhaust 48 without geometry/apparatus. Its old calibration-dependent builder is disabled. The “spinor” coordinates used to parametrize the homogeneous scalar/dust constraint in PR60 do not establish spin-1/2 matter.

## Recovery and acceptance boundary

The independent reviewer corrected duplicate carrier indices, collector failure handling, and plural source-hash verification. The original full source patch must be recovered, checked against its source maps, and exported before a complete implementation PR is claimed. The final integration test must be rerun or its actual outcome recovered.

The archives on this branch preserve measured evidence. Some normal bundle metadata and source files are absent, so the ordinary runtime verification command is not advertised as executable from this checkpoint alone.

Still open: coupled spatial Einstein dynamics, material clocks/binding/detectors, physical chirality within the total budget, a justified physical complexity/entropy measure, and a dynamical cosmological bounce.
