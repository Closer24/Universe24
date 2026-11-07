# Light approval and entanglement: physics review

**Question:** Does a locally evolving board that delays a click until a signal approves it produce quantum entanglement in the clicks?

**Status:** Primary-source review and conditional physical analysis, 7 November 2026. No engine change or experimental entanglement claim. The reference candidate is the published commit `5894510ada12d22f17a70f93a41ec311aef13265`.

## Finding

Signal-dependent approval can be a mechanism for generating correlated records. It is not sufficient evidence of quantum entanglement. Three distinct cases must be separated: a common cause preparing correlated devices; communication that coordinates later records; and a selection rule that changes which trials enter the displayed statistics. All three can create striking click correlations without establishing quantum entanglement.

Bell and CHSH provide a test of a specified local explanation under explicit assumptions [1,2]. Quantum entanglement is a different property: within quantum theory a bipartite state is entangled when it cannot be represented as a mixture of product states. Werner constructed entangled states admitting a local hidden-variable model for the measurements in his construction [3]. Therefore a result at or below a CHSH bound does not, by itself, exclude every entangled quantum state. Conversely, correlation or a unique click alone does not establish an entangled-state interpretation of a classical automaton.

## What a Bell comparison requires

For settings `a,b`, outcomes `A,B` and a complete shared variable `lambda`, the relevant local form is

`P(A,B|a,b) = integral rho(lambda) P(A|a,lambda) P(B|b,lambda) dlambda`.

The distribution `rho` must not change with the chosen settings. A finite deterministic implementation is the special case `A=A(a,lambda)` and `B=B(b,lambda)`. Including a local no-click outcome as zero keeps each outcome bounded by one and preserves the all-trial CHSH bound of two under these conditions. This is a conditional mathematical restriction, not an assertion that determinism alone is inconsistent with quantum predictions.

The Universe24 settings used in the current bounded audit are local initial preparations, not derived physical analyzer orientations. A prepared shared source phase is an explicitly supplied common cause. Testing all four setting pairs with the same fixed weights is useful for auditing locality and selection; it is not yet an optical Bell experiment.

## Approval: heralding, communication or postselection

| Meaning of approval | Required accounting | Physical conclusion available |
| --- | --- | --- |
| A preparation herald selects an ensemble independently of the settings | Verify `rho(lambda|a,b,H)=rho(lambda|H)` and retain every accepted trial's outcome, including failures | Heralding can define valid Bell trials; it does not itself create Bell-nonlocal statistics |
| An approval signal carries information from both settings before a click | Include the communication paths and full delays in the causal diagram | Outcomes may cease to factor locally; the result is not a spacelike Bell test on that board |
| Keep only trials where both detectors eventually click | Publish the original trials, acceptance probabilities and conditional hidden-variable distribution | Selected correlations can exceed a naively applied bound through a detection or selection loophole |
| Pair separately recorded clicks by a timing window | Fix pairing and timing rules prospectively and account for unpaired events | Setting-dependent timing can produce the coincidence-time loophole [5] |

A herald fixed before fresh, independent settings is a simple sufficient design. It is not the only valid chronology. In Hensen's event-ready experiment the herald event is spacelike separated from the setting-generation events, and the local bases are selected independently of the herald [4, pp. 2–3]. The essential issue is the justified causal and statistical independence of acceptance from the settings, not the word “approval.”

Larsson and Gill explicitly construct local timing models whose coincidence-selected correlations require a different bound [5]. Equal observed acceptance rates across settings are not enough to establish fair sampling: the accepted *composition* can still differ. Equal local marginals in the selected data also do not cure this problem.

## Board time and click time

The proposal that many board updates correspond to no increment of an observer's click clock is coherent as a proposed observation map. It does not change the board's causal paths. If those updates allow a setting to reach the other apparatus before its record is fixed, the two outcomes are causally connected in board time.

This does not by itself prove that every effective physical interpretation is impossible. It means the research must derive an operational spacetime map: how clocks measure durations, how rulers and signal speeds are calibrated, when settings become fixed, when outcomes become records, and which events are spacelike for the observed physics. A model with hidden board communication could be nonlocal relative to that effective spacetime. It must then explain the observed absence of controllable faster-than-light signalling and reproduce the full experimental timing constraints, rather than obtaining them by redefining time after seeing the outcomes.

## A click is not a derivation of collapse

An interaction may establish a stable apparatus record while the complete dynamics retain information. Zurek's quantum measurement model shows how an apparatus–environment interaction selects a robust record basis within an already specified quantum theory [7]. It does not establish that any reversible integer record implements that theory.

For Universe24, an effective-collapse claim requires an independently defined mapping to states, preparation procedures, measurement settings and conditional probabilities. It must reproduce interference and the relevant quantum probability law over a declared family. A physical deletion of alternatives would contradict the fixed complete-state reversibility contract. An observer conditioning on a record is permitted as analysis but is not an extra state-changing engine operation.

## Minimum prospective tests

1. **Local record test:** fix the approval signal, receiver region, click predicate, latency and retention horizon. Compare source-present, source-absent, delayed-source and irrelevant-source preparations. Retain all counters and remainders; verify full rewind. A record that reverts before the declared horizon fails that criterion.
2. **Complete trial accounting:** fix a finite outcome deadline, trial identifiers and no-click outcome. Keep every attempted trial. Report `P(A,B|a,b)` including zeros, local marginals, both-click acceptance rates, and separately labelled conditional statistics. First-click pairing must not silently replace fixed trials.
3. **Independence and locality audit:** show exactly which initial data encode settings and shared variables; keep their ensemble weights independent. Verify that remote settings cannot reach each local record by the declared board horizon. If they can, classify the run as a communication experiment.
4. **Quantum target:** specify the observable family and a predicted correlation curve before the run. For a Bell-nonlocal target, compare with an inequality appropriate to the complete detection model and settings distribution. For an entangled-state claim without Bell violation, provide an independently justified quantum subsystem/measurement representation and a valid entanglement witness or tomography procedure.
5. **Finite statistics:** complete enumeration of a declared finite ensemble gives exact results for that ensemble. Randomly sampled trials require a prespecified stopping and statistical method. Do not use an independent-trial Gaussian error bar when retained apparatus memory violates that assumption. Hensen's analysis allows device memory; Shalm's trial accounting includes trials without detected photons and uses specified statistical stopping [4,6].

The immediate experiment can establish source-sensitive, correlated click records and expose a selection bias. To establish the user's stronger claim, an operational quantum interpretation and a loophole-accounted statistical target remain necessary.

## Primary sources

1. J. S. Bell, “On the Einstein Podolsky Rosen paradox,” *Physics Physique Fizika* **1**, 195–200 (1964). [Publisher](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195). Locality and quantum-correlation obstruction; not a theorem against determinism by itself.
2. J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt, “Proposed Experiment to Test Local Hidden-Variable Theories,” *Physical Review Letters* **23**, 880–884 (1969), with the 1970 erratum. [Publisher](https://doi.org/10.1103/PhysRevLett.23.880). Experimental Bell comparison.
3. R. F. Werner, “Quantum states with Einstein-Podolsky-Rosen correlations admitting a hidden-variable model,” *Physical Review A* **40**, 4277–4281 (1989). [Publisher](https://doi.org/10.1103/PhysRevA.40.4277). Entanglement and Bell nonlocality are not identical properties; claims here rely on the publisher's abstract, not an uninspected full-text derivation.
4. B. Hensen et al., “Experimental loophole-free violation of a Bell inequality using entangled electron spins separated by 1.3 km,” *Nature* **526**, 682–686 (2015). [Author manuscript](https://arxiv.org/abs/1508.05949), [full text](https://arxiv.org/pdf/1508.05949). Event-ready timing on pp. 2–3, memory-aware inference on pp. 5–6. The paper reports `S=2.42±0.20` from 245 trials, with its specified hypothesis test.
5. J.-Å. Larsson and R. D. Gill, “Bell's inequality and the coincidence-time loophole,” *Europhysics Letters* **67**, 707–713 (2004). [Author manuscript](https://arxiv.org/abs/quant-ph/0312035), [full text](https://arxiv.org/pdf/quant-ph/0312035). Setting-dependent timing can change the selected subensemble even for local dynamics.
6. L. K. Shalm et al., “A strong loophole-free test of local realism,” *Physical Review Letters* **115**, 250402 (2015). [NIST publication record](https://www.nist.gov/publications/strong-loophole-free-test-local-realism), [author manuscript](https://arxiv.org/pdf/1511.03189). Locality, detection accounting and statistical stopping; the full text's table notes include undetected trials.
7. W. H. Zurek, “Pointer basis of quantum apparatus: Into what mixture does the wave packet collapse?” *Physical Review D* **24**, 1516–1525 (1981). [Publisher](https://doi.org/10.1103/PhysRevD.24.1516). Dynamical selection of an apparatus record basis within quantum theory; not an integer-automaton derivation.

## Research access log

Primary-source web review used Bell's publisher record/original-paper reproduction, CHSH's publisher record, Werner's publisher abstract, Hensen/Larsson–Gill/Shalm author full-text PDFs, and Zurek's publisher abstract/full-text opening. No direct quotations are used. Tool retrieval references supplied to the project manager include `turn6search1`, `turn6search5`, `turn8view1`, `turn8view2`, `turn8view3`, `turn8view4`, `turn8view5`, `turn7search6` and `turn9view0`. The failed arXiv HTML fetch for Hensen was replaced by the complete PDF; it is not evidence of a missing paper.
