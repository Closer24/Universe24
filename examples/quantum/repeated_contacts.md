# Repeated local quantum contact outcomes

[repeated_contacts.json](repeated_contacts.json) is a self-contained input for
`recurrent-contact-fields-v1`. It uses the existing runner and a periodic
7 x 3 x 3 world, three held contact probes and one unit-inventory disturbance.
Physical labels are initialization data. No simulator build or visualization
is required.

The source instrument transfers the initial ordinary disturbance into a vacuum
domain. Each capture instrument defines null, localized, new-wave and continued
outcomes with integer coefficients 13, 3, 4 and 12. In an occupied local mode the
relative weights are 9, 16 and 144 out of 169. Vacuum produces a certain null.
The prescribed tickets exercise a chosen acceptance sequence; this file is not
an unbiased statistical trial or a derived particle-interaction law.

```sh
python -m event_universe.configuration_validation examples/quantum/repeated_contacts.json
python -m event_universe --init examples/quantum/repeated_contacts.json --output artifacts/repeated-contacts-result
```

Use the project Python with `PYTHONPATH=src` and a fresh output directory. The
headless runner saves input identity, run metadata, event records and final state.
Generated artifacts follow the runner's 24-hour retention policy; the input and
acceptance results remain versioned.

| Event tick | Position | Local result | Current generation |
| --- | --- | --- | --- |
| 0 | (1,1,1) | Transfer ordinary inventory into wave | 1 |
| 3 | (2,1,1) | New wave | 2 |
| 6 | (2,1,1) | Continue | 2 |
| 9 | (3,1,1) | New wave | 3 |
| 12, 15, 18 | (3,1,1) | Continue | 3 |
| 21 | (2,1,1) | New wave | 4 |
| 24 | (2,1,1) | Localize | 4 |

Every new-wave result resolves its old origin and creates a fresh local origin.
No duplicate ordinary carrier is created, and localized output retains the
explicit unknown-momentum marker. Origin count is not particle count.

Link transit is three ticks. Six preallocated ordinary envelope generations
emit on fixed round-robin turns, independently of remote quantum outcomes. Old
cancellation packets stay within the old generation; earlier field stock keeps
propagating and attenuating. At the end of 48 ticks, charge remains -1, mass 1,
ordinary field injection totals -36, dissipation totals -36 and field stock is
zero. Carrier and field accounting balance at every completed tick.

The local envelopes are retarded source approximations after measurement, not
globally conditioned probabilities. This experiment tests finite outcome and
ownership mechanics; it does not establish reciprocal field action, a physical
Hamiltonian, momentum/energy closure or unlimited many-body collisions. See the
[contract](../../docs/RECURRENT_QUANTUM_CONTACT.md) and
[actual validation evidence](../../docs/VALIDATION.md).
