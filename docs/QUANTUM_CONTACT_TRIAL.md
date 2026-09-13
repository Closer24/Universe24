# Quantum-selected local contact trial

This document preserves the earlier bounded contact fixture. The newer
[native event-program interface](NATIVE_QUANTUM_EVENTS.md) supports optional
composition through the ordinary engine and repeated local triggers. The limits
below belong to this historical fixture, not that newer interface.

## Selected experiment, not a default engine rule

`quantum-selected-elastic-contact-demo-v1` composes the existing
`DisturbanceEngine`, `DisturbanceLaw` and the selected
[deferred quantum event network](QUANTUM_EVENTS.md). The user requested an actual
combined run after integrating the quantum backend. No production core, field
law, default Simulation or existing read-only QuantumBridge is modified.

Two unit-mass bodies start at (2,2,1) and (10,2,1), with momenta (+1,0,0)
and (-1,0,0). One neighbor transit takes one tick. At tick 4 both reach (6,2,1).
Only their local co-residence invokes the explicit position instrument on a
three-site quantum sidecar. No distant particle search triggers the decision.

The source begins at quantum site 0. An explicitly supplied 3:4 local mixing
matrix at tick 1 gives weights 16 for empty and 9 for occupied at site 0.
One supplied ticket in [0,25) selects transmission (0..15) or momentum exchange
(16..24). Tickets are reproducible test inputs, not a verified random source.
Enumeration of all tickets tests this exact distribution without RNG claims.

The integration planner writes the selected code into the two local proposal
records. The generic initialization-defined interaction either does nothing or
exchanges their momentum vectors. The existing engine commits that mechanical
pair and routes the actual outgoing packets. Thus the outcome changes native
`sent` events and subsequent trajectories; this is not two unrelated simulations.

## Boundaries and timing

The fixture binder restricts shape, occupancy, initial records, link time and
run length. Its positional roles are field 0 mass, field 1 momentum, field 2
outcome code, and types 0/1 the two bodies. This is an eight-tick, one-contact
experiment, not a general dispatcher for arbitrary nodes or repeated encounters.
Names are labels; the ordinary engine has no quantum or particle-name branch.

The classical local planner receives exactly two local slots. Its quantum call
belongs to the explicitly selected integration controller under Q-ORACLE-1,
not an exception allowing ordinary forces to read distant physical state.
All candidate mechanical plans validate before the quantum record commits.
One extra modeled operation is counted; the fixed normal budget makes the local
wait zero. Host preparation evaluates both alternatives; its work is not
reported as CPU-constant quantum computation.

The quantum record is followed by the mechanical commit. These are sequential
local events within tick 4, not a cross-owner transaction. An error in the later
engine event aborts the run and retains the earlier quantum record; it never
substitutes no-event or publishes a passing trial. The CLI preserves an event
trace and failure report. The unchanged engine retains its own failure contract.

World and quantum recipe clocks are synchronized. Preparing and committing the
instrument advances neither clock. The tick-4 outcome is visible in completed
frame 5, when the first post-contact packets have their arrival time. Later
nearest-neighbor SWAP recipes at ticks 5 and 6 retain and propagate the selected
quantum continuation. No second measurement or rerandomization is introduced.

## Checks and interpretation

The read-only balance check counts node-owned and in-flight bodies exactly once:
mass 2, total momentum (0,0,0), and twice unit-mass classical kinetic energy 2.
Failure rejects the run without repairing any state. These balances concern the
two classical bodies; quantum/environment energy and recoil are not modeled.
This does not establish a closed quantum-plus-matter conservation law.

Identity and equal-mass momentum exchange each preserve those classical balances.
The occupation-preserving mixing and SWAP matrices preserve one excitation.
The complete position instrument preserves total outcome probability. These are
explicitly supplied toy laws, not derived particle scattering or a classical limit.

The tests enumerate all 25 tickets, verify native outgoing directions and causal
arrival times, retain quantum continuation, compare unmeasured classical routing,
reject invalid tickets/capacities/geometry, and compare visual with headless results.
No oracle query occurs before the contact. Full-state final diagnostics are host
work and are not included in the single modeled oracle-call count.

## Reproduce from the repository

```sh
python -m event_universe.integration.quantum_contact_trial --init examples/quantum/contact.json --output artifacts/contact-reflection --ticket 24 --visualize
python -m event_universe.integration.quantum_contact_trial --init examples/quantum/contact.json --output artifacts/contact-transmission --ticket 0 --visualize
python tools/check.py --base origin/main --tests tests/test_quantum_contact_trial.py
```

Use a new output directory. Omit `--visualize` for ordinary headless output.
The HTML uses the existing recorded-state generator and never directs motion.
Source, configuration, tests and this contract remain in Git. Generated results
follow the existing finite retention policy. Python identity and source
fingerprints are recorded by every successful trial; CI also saves the Git head.
