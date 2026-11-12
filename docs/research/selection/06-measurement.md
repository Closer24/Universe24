# Measurement, retained records and relational time

Lane 6, 2026-11-12. Source-only research; no supported runtime, tensor or default changed.

The new construction is a finite, exactly reversible relational-clock reference with two explicitly modeled memory registers and a complete-trial instrument reader. It separates three questions: when a record appears, whether it persists and agrees with a fresh probe, and why a particular outcome has its probability. It also reads the actual native pointer lane's traces, so the reference does not substitute for board evidence.

## What the primary papers supply

| Primary source | Specific useful result | Limit for this project |
|---|---|---|
| Page and Wootters, *Evolution without evolution* (1983), [DOI](https://doi.org/10.1103/PhysRevD.27.2885) | The abstract proposes relational evolution through correlations in a stationary global state. | This work is motivation; the original full text was not accessible in this audit. |
| Giovannetti, Lloyd and Maccone, *Quantum Time* (2015), [paper](https://arxiv.org/pdf/1504.04215), [DOI](https://doi.org/10.1103/PhysRevD.92.045033) | Equations 28–31 introduce a unitary system-memory interaction, normalized Kraus operators and squared-norm outcome probabilities. Equations 35–40 include clock-conditioned memories and a distinct second memory for sequential measurements. | The probability rule is present before the relational-clock calculation; this is not its derivation from Rule3. Memory persistence is an explicit modeling choice. |
| Ozawa, *Uncertainty principle for quantum instruments and computing* (2003, revised 2004), [paper](https://arxiv.org/html/quant-ph/0310071v2) | Section II characterizes instruments using complete positivity, affine mixing and realizable indirect measurement models. | These quantum assumptions and an initial apparatus state must be declared when using the representation. |
| Schlosshauer, *Decoherence, the measurement problem, and interpretations of quantum mechanics* (2004/2005), [paper](https://arxiv.org/pdf/quant-ph/0312059) | Sections II and III distinguish premeasurement entanglement, a reduced density operator and the definite-outcome problem; environmental records can stabilize a preferred record basis. | A diagonal local density operator does not by itself prove that one global branch was dynamically selected. |

These are construction guides and assumption checks. None establishes a native degree-three, 48-channel realization or a physical preparation measure for this board.

## Exact construction that now runs

`validation/selection/measurement.py` uses exact rational amplitudes as a quantum-circuit reference. It is deliberately not passed to the Engine. The retained reference basis is a four-state clock, a source bit, a ternary pointer and a separate ternary fresh probe: dimension `4*2*3*3 = 72`. Pointer state zero is ready; states one and two are distinct recorded outcomes. A binary pointer would conflate ready with one outcome unless additional retained structure distinguished them.

Let `W` swap ready with the label controlled by the source bit, leaving the other label unchanged. The four clock-controlled operations are

\[
U_0=W_M,\quad U_1=W_{M'},\quad U_2=I,\quad U_3=W_MW_{M'}.
\]

Their product is the identity. The global update

\[
V=\sum_{t=0}^{3}|t+1\bmod4\rangle\langle t|\otimes U_t
\]

is a permutation on all 72 basis states. Starting with source amplitudes `3/5, 4/5` and both memories ready, form the normalized history

\[
|\Psi\rangle=\tfrac12\sum_{t=0}^{3}|t\rangle|\psi_t\rangle,
\qquad |\psi_{t+1}\rangle=U_t|\psi_t\rangle.
\]

The script verifies `V|Psi> = |Psi>` exactly, exact inverse replay and recovery of each slice by conditioning on its clock reading. Basis preparations give one persistent pointer label at ticks 1–3 and a matching fresh probe at tick 2. At tick 4 both memories uncompute: the longer persistence gate correctly fails. The finite clock therefore supplies a declared record window, not permanent memory at no resource cost.

For the superposed source the reduced pointer matrix at tick 2 is `diag(0,9/25,16/25)`, while the full state retains cross-branch matrix element `12/25`. Both branches remain. Interpreting the diagonal as outcome probabilities uses the usual quantum squared-norm rule; this program never samples it and never calls a random generator. Relational conditioning organizes observations but does not select one branch.

## Native pointer integration and the complete-trial contract

The reusable `assess_trials` requires unique declared trial IDs, a fixed decision index, a fixed persistence window, all active labels per tick and, if desired, an explicit exact preparation measure. Missing, duplicated, malformed and truncated streams are rejected. No-outcome and multiple-outcome trials remain in the denominator. Uniform counting is visibly a diagnostic convention rather than a claimed physical measure. Observation of an empty first frame does not certify a physical ready sector.

Run the linked audit:

```sh
python -m validation.selection.measurement \
  --pointer-trials runs/selection/pointer/instrument_trials.json \
  --out runs/selection/measurement
```

The native pointer controls use decision index 2 and seven observed persistence ticks. All six controls are retained: four stable single records, one no-source/no-record control and one double-source/double-record control. The deliberately prefilled `matched_history` control makes the pooled ready-window check false. These are different engineering preparations, so their pooled counting proportions are not physical outcome frequencies. The primitive establishes useful arrival memory; it does not yet supply exclusive selection for a two-port excitation. The report hashes both its own source and the imported trace file.

The reader cannot certify locality, ownership, full-state rewind, feedback or fresh-apparatus repeatability from visible labels alone. Those remain separate native construction gates. Its embedded controls also demonstrate that an initially single record can fail persistence later.

## Complexity before the click versus biasing its count

A fixed complexity-dependent interaction could change amplitudes before measurement, provided its actual retained dynamics, clock, workspace and locality are accounted for. The subsequent quantum prediction would then use those new amplitudes. This is a concrete place to seek the user's mechanism without silently changing the probability rule.

The exact control rotates amplitudes `(3/5,4/5)` with the orthogonal matrix `[[3,-4],[4,3]]/5`, producing `(-7/25,24/25)` and squared weights `(49/625,576/625)`. By contrast, multiplying the original outcome counts by factors `(2,1)` and renormalizing gives `(9/17,8/17)`. The latter is a changed counting/selection law for the original preparation, not an amplitude evolution. These controls do not prove that either operation is generated by structural complexity.

Even exclusive deterministic records leave a measure missing: exactly the same two outcome traces admit explicit preparation weights `(1/2,1/2)` or `(9/10,1/10)`. Neither clock order nor repeatability chooses between them. A deterministic retained register that routes a prepared seed is useful circuitry, but its seed distribution must be declared and independently justified before claiming Born statistics.

## Next concrete gates

1. Realize ready, local source interaction, and mutually exclusive retained outcome sectors in one admissible tensor. Preserve the failed double-source control.
2. Probe the retained record with a distinct, budgeted apparatus and test a predeclared persistence horizon including clock recurrence.
3. Make the record affect later retained structure. Compare the same complete preparation with feedback disconnected; an external decoder changing the next seed is not this mechanism.
4. Specify the complete preparation ensemble and its measure before looking at outcomes. Keep losses, doubles and all trials in reported statistics.
5. Compare amplitude predictions and click frequencies on held-out preparations and measurement settings. Keep a conventional quantum reference labeled as such.
6. Measure structural change between internally defined bursts with preregistered complexity quantities and matched feedback controls. Growth in a stored integer or overwritten display alone does not establish growing organization.

Status: rational clock/reference checks passed; native pointer trace contract exercised and correctly exposes its negative controls. The separate native gate proves conditional single-occupancy routing in its declared ready sector; the two-port pulse pointer still fails unconditional exclusive measurement. Born derivation and preference for increasing structural complexity remain unproved. Full source-only output is `runs/selection/measurement/measurement.json`.
