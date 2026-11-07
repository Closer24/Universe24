# Algorithmic analogues for signal-controlled records

**Date:** 7 November 2026. **Base:** `b86e97f0a45f9857021ba7dd8b035acba8ecd932`. **Status:** literature and proposals; no new implementation or simulation.

The target is a transported board signal that causes an encounter, leaves a waiting state, and later receives an ordinary approval signal that permits one committed output direction. The most useful combination is **reversible controlled routing, a waiting store, and finite acknowledgment accounting**. Exact constraint solving is a candidate discovery tool. The reviewed literature supplies constructions in other models; it does not establish their realizability under Rule3.

This targeted review is not exhaustive. The model remains one board, 48 channels, six neighbors, one fixed tensor and synchronous Rule3 with `num=den=1`. Search chooses initial data. Runtime gates, injections, deleted branches and inverse-executor calls remain excluded.

## What branching would mean

A complete Rule3 state has one future and one past. Its dependencies can spread across many nodes, and several candidate patterns may coexist. Neither fact means that all alternative histories are evaluated. Classical fanout, explicitly encoded alternatives and quantum probability amplitudes are different claims.

“Board carrier” names a mathematical transported pattern. “Observed photon” would require an operational correspondence between preparations, propagation, detectors and click statistics. Quantum walks explicitly use amplitudes and unitary evolution in a Hilbert space [9]; decoherence analysis concerns quantum systems and their environmental records [10]. Those structures cannot be inferred from reversibility or a quiet outlet alone. A click counter may pause while the board evolves; this does not by itself derive a physical arrow of time.

## Comparison of useful precedents

| Precedent | Relevant result in its own model | Transfer to Universe24 and missing work |
|---|---|---|
| Fredkin–Toffoli conservative logic [1] | Conditional routing preserves the control; circuits also provide classical fanout and storage using specified inputs and auxiliary lines. | Best architectural starting point: make one arriving pattern route another while retaining the control and remaining information. No Fredkin gate is known to be compiled into this Rule3 lattice. |
| Margolus soft-sphere automata [2] | Collision-based lattice models support universal computation, including momentum-conserving arrangements without fixed mirrors. | A precedent for computation through local collisions. Its collision law, timing and signal resources cannot be imported as extra Rule3 operations. |
| Sutherland micropipelines [3] | A rendezvous element waits for the required events; SELECT separately routes an event according to data. | Separate waiting from direction choice. A handshake specification does not supply a reversible Rule3 memory or router. The electronic primitives are not new engine primitives. |
| Dijkstra–Scholten termination detection [4] | Deficits and returned signals account for completion of a terminating diffusing computation on a finite graph. | Useful for a finite set of routes: account for every issued branch before approval. Completion detection does not choose a winner or compare complexity. Its bookkeeping must acquire a board representation. |
| Bennett reversible computation [5] | Retained history permits reversible computation and controlled restoration of workspace while keeping the output. | Preserve rejected-route information and acknowledgment history. Any later history recycling must itself be realized by forward Rule3 dynamics, not by switching the simulator into rewind mode. |
| Coherent virtual absorption [6] | A matched, growing incident waveform can store energy temporarily in a lossless resonator; interrupting the drive releases it. | A waveform-design analogy for capture and release. It is not an idle persistent memory, and an externally controlled optical drive is not an allowed runtime controller here. |
| SMT and bounded reachability [7] | Exact integer constraints and unrolled transition relations can describe finite reachable-state questions. | Search for one shared initial apparatus satisfying all controls. A satisfying assignment still needs full-engine replay; timeout is not impossibility. |
| Compositional cellular-automaton synthesis [8] | SAT completes arrangements of existing Game-of-Life patterns into larger objects. | Reuse a verified carrier and search its interface. Game of Life is a different automaton; the transferable idea is constrained composition, not its objects or transition rules. |

## Recommended architecture, still unimplemented

Start with a one-shot receiver and one data carrier. The receiver must distinguish ready, waiting and committed states through fixed passive predicates. A later approval is another counter/remainder disturbance. A control-dependent collision routes the stored information toward one declared output, while the complete state retains the control, unused information and cancellation witnesses.

A first router may use a declared control bit. Internal comparison comes later: candidate data and comparison must be encoded on the board; an observer's complexity score cannot send approval.

If the initial state, dynamics and readout respect an exchange of the outlets, deterministic unique choice requires declared symmetry breaking; an undisclosed tie rule is insufficient.

Test a splitter using **one input producing two outgoing arms**. Two preloaded packets do not demonstrate fanout. Disclose auxiliary preparations and retain them in source-off controls. A two-route acknowledgment test requires both arms' completion information, not observer-inferred silence. Specify causal bounds, missing-message behavior, duplicates and a priority or tie rule.

The original arithmetic event classes `C0/C1/C2` remain unchanged and visible. A prospective “committed direction” predicate would be an additional passive observable, not a replacement definition of a click. Every encounter, waiting-phase and later arithmetic C remains in the trace. No after-the-fact filtering may turn a multi-event trajectory into a claimed single-event mechanism.

## Existing boundary and a separate waiting candidate

The [published message study](../../docs/MESSAGE_MECHANISM.md) retains 0/9 baseline quiet-pending successes, 0/891 stationary-converter successes, no accepted cancellation/quiet record in 15 interaction groups, and 0/54 admissible reverse preparations. The reverse-prepared receivers already contained their target. These results remain failures of their registered criteria.

The quiet zero-counter contract also has an exact input-area constraint. A confined finite-support row front with stationary far fields, zero transverse input and one-site advance per internal period cannot leave a changed far-field remainder. These bounded findings motivate transverse interactions and different memory representations; they do not prove global impossibility or authorize a new evolution law.

A separately proposed waiting representation is a localized periodic orbit. There is a simple algebraic preparation: put counters `(A,B)` in one center channel and keep neighbor quotients zero. All other board counters are zero; nonhalo remainders are fixed initially. Thus the center input is zero. A signed receiving halo channel has successive remainders

```text
r_h + 2*w*{0, B, B-A, -A, 0},  where w is its fixed sign.
```

Valid halo remainders exist exactly when `|A|+|B| <= 2`. For `L >= 3`, the unit preparation `(A,B)=(1,0)`, all other board counters zero, halo and background remainders 2, and any valid center remainder gives an exact four-cycle. The six receiving addresses are distinct signed-permutation recipients; their zero counters prevent feedback. This is a prepared oscillator, not a demonstrated incoming-signal memory. Capture, approval-dependent release and composition remain unproved. A future orbit contract must include the complete 48-channel center and halo phases and be registered separately from the failed zero-counter predicate.

Invertibility forbids an incoming whole-board state outside a periodic orbit from entering that orbit. Any capture proposal must retain external dynamics or radiation and specify a finite waiting interval; a local periodic readout does not make the complete board periodic.

## An exact, bounded synthesis pilot

The proposed encoding introduces integer variables for every retained channel and time:

```text
u = sum_of_the_six_fixed_signed_neighbor_b_values
6*ell + r_next = 2*u + r,    0 <= r_next < 6
a_next = b,                b_next = ell - a
```

With fixed integer weights these are quantifier-free linear integer constraints. The positive denominator gives the required signed Euclidean division. Use arbitrary-precision integer semantics; do not silently replace the model by overflowing bit vectors. All runs share the same unknown apparatus preparation, while declared source-presence inputs differ. Terminal information outside the readout may remain unconstrained, but must be saved and reversed during audit.

**Pilot A preserves the old quiet criterion.** Search 22 initial even remainders: three row pairs plus two row positions times four transverse faces times two mapped channels. Initial apparatus counters are zero; the ready receiver is fixed and cannot contain the target. Freeze geometry with first arrival at update 4, horizon 12, and exact quiet target states `4..12`. Solve source-present and source-absent cases together. The tensor, source recipe, address set, all other initial data and predicates are fixed before solving.

**Pilot B requires a new registration after a positive A result.** Extend to horizon 21 with a second arrival at update 13 and the four data/approval controls `00/10/01/11`. The first-only case must wait; the approval-only case must not commit; only the joint case may produce the specified retained record. A periodic-store search is a separate candidate, with its own full-state phase predicate, not a relaxation silently applied to Pilot A.

Proposed pilot budget: 600 CPU seconds, 4 GiB memory and at most 250,000 channel updates in the complete causal encoding. Preflight the dependency count. A proven locality reduction is allowed; dropping dependencies or imposing an artificial absorbing boundary is not. Exceeding the cap or receiving `unknown`/timeout is inconclusive. `UNSAT` excludes only the completely encoded bounded family. No solver experiment has yet been executed.

## Ranked decisions and acceptance

1. **Search the carrier-to-waiting interface with exact shared-apparatus constraints.** Keep the existing quiet target first; report a model, bounded exclusion or resource limit. Independently reconstruct every candidate and replay it under unchanged forward Rule3.
2. **Investigate periodic capture/release under a separate protocol.** Require complete center/halo retention, all four arrival phases, all arithmetic events logged, and source-dependent behavior. Apparatus alone must not manufacture the claimed record. One prepared oscillator is insufficient.
3. **Compose a reversible router with finite acknowledgment accounting.** Require a single input's fanout, returned branch obligations and one committed direction; preserve the losing-route information. A supplied control signal tests routing before an internal comparison is claimed.

After discovery, freeze 24 validation runs: four controls, two board sizes and three delays. Require complete records, response windows, no boundary return, exact rewind and joined-component compatibility. Amplitude and sign robustness need a separate frozen study. Earlier events remain visible after any later retraction. These tests are proposed, not completed. Select one exact pilot registration before implementation.

## Primary sources

1. Fredkin and Toffoli, *Conservative Logic* (1982; 2002 reprint), especially Figures 3.6, 3.8 and 3.16: [MIT-hosted paper](https://fab.cba.mit.edu/classes/862.22/notes/computation/Fredkin-2002.pdf).
2. Margolus, *Universal Cellular Automata Based on the Collisions of Soft Spheres*: [arXiv:0806.0127](https://arxiv.org/abs/0806.0127).
3. Sutherland, *Micropipelines* (1989): [paper](https://arc.cecs.pdx.edu/wp-content/uploads/2023/04/Sutherland_Micropipelines_TuringAward_ACM_1989.pdf).
4. Dijkstra and Scholten, *Termination Detection for Diffusing Computations*: [EWD684](https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD684.html).
5. Bennett, *Logical Reversibility of Computation* (1973): [original paper](https://worrydream.com/refs/Bennett_1973_-_Logical_Reversibility_of_Computation.pdf).
6. Baranov, Krasnok and Alù, *Coherent Virtual Absorption Based on Complex Zero Excitation for Ideal Light Capturing*: [arXiv:1710.09345](https://arxiv.org/abs/1710.09345).
7. [SMT-LIB integer theory](https://smt-lib.org/theories-Ints.shtml); Bjørner et al., [*Programming Z3*, bounded model checking](https://z3prover.github.io/papers/programmingz3).
8. Nishimura and Hasebe, *Compositional Object Synthesis in Game of Life Cellular Automata Using SAT Solver* (2021): [paper](https://www.cs.tsukuba.ac.jp/~hasebe/downloads/icsi2021_nishimura.pdf).
9. Aharonov et al., *Quantum Walks on Graphs*: [paper](https://arxiv.org/pdf/quant-ph/0012090).
10. Zurek, *Decoherence, Einselection, and the Quantum Origins of the Classical*: [paper](https://arxiv.org/html/quant-ph/0105127v3).
