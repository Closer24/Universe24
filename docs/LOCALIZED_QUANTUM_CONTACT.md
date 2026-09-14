# Localized quantum contact candidate

`localized-contact-quantum-v1` is an explicit finite hybrid model. Ordinary
fields are sourced only by localized disturbances. A delocalized excitation
does not source a probability-weighted classical field. Existing field packets
continue under their configured local laws. This is not quantum electromagnetism.

The separately selected [causal source extension](CAUSAL_QUANTUM_SOURCES.md),
`causal-contact-fields-v1`, adds locally evolved weighted field sources and
Link-delivered cancellation. The localized-only contract on this page remains
the behavior of `localized-contact-quantum-v1`.

The [recurrent extension](RECURRENT_QUANTUM_CONTACT.md) separately selects
complete outcome instruments and fresh local continuations after interactions.

| Part | Contract |
| --- | --- |
| Law | A local contact with an explicit unknown-momentum marker transfers one configured disturbance into a vacuum quantum domain. Configured number-preserving neighbor gates propagate it. A complete local absorption instrument transfers it back into one localized disturbance. |
| Inputs | Only resident contact participants, a configured validity scalar, fixed output templates and local quantum registers. No physical rule reads a remote origin's carrier values or a diagnostic probability. |
| Evolving state | Ordinary records retain ownership during a delayed cycle. A bounded integer token reserves a local conversion. Each finite domain is activated once; local banks retain at most six origin IDs. The quantum owner retains exact conditional amplitudes. |
| Parameters | Finite disjoint binary mode domains, source and detector types, unknown marker, localized output template, integer unitary matrices and a repeating disjoint local gate schedule. No species name selects a law. |
| Derived values | A domain owns one configured inventory vector between conversion and capture, regardless of the number of references. Conservation totals include this sector exactly once. |
| Outputs | Source removal and quantum preparation commit together. Capture uses K0=\|0><0\| and K1=\|0><1\|, leaving vacuum after a click and installing one local output. Zero momentum with a valid marker does not trigger preparation. |
| Consistency | Preflight every local output alternative before drawing. Capture attempts depend on resident detectors, with equal cycle cost for vacuum and occupied outcomes. Local propagation respects Link transit; shared origin retirement never rewrites remote classical fields. |
| Tests | Delayed ownership transfer; valid zero versus unknown; no-contact vacuum; exact split and recombination; capture ticket weights and single charge; output/capacity rejection before drawing; causal nonzero classical emission; finite source allowance; generic renaming. |

The initial candidate uses finite one-shot domains and declared capture templates.
It does not infer momentum, a Hamiltonian, spin, exchange statistics or a
measurement apparatus from missing information. Fixed-template conversion requires
matching conserved quantities at the source. Classical emission allowances are
finite per localized source event and their injection remains in source accounting;
they are not an unmodelled promise of total field/matter energy conservation.
No reciprocal field action during coherent propagation is claimed.

The existing `local-quantum-events-v1/v2/v3` contracts remain separate. Passive
classical-only conservation audits and shared Node clock profiles need their own
quantum inventory composition before they can select this candidate.

## Configuration and execution

Use [localized_charge.json](../examples/quantum/localized_charge.json) through
the ordinary runner:

```sh
python -m event_universe --init examples/quantum/localized_charge.json --output artifacts/localized-charge
```

`event_program.model` selects the candidate. `addresses` declares at most thirty
distinct binary-mode locations. Each `domains` entry owns disjoint
`register_indices`, a deferred named source, a capture definition and repeating
`phases`. Every mode belongs to exactly one domain. The source defines its local
register, source/partner type, owned validity scalar, unknown value and vacuum to
occupied preparation matrix. Capture defines local detector registers, detector
type, a held output template and the complete null/absorption instrument.
The output retains the unknown marker; later motion needs an explicit local law.

Each phase is a disjoint list of one-mode or neighboring two-mode integer
unitaries. Phase `(tick-1) modulo phase_count` repeats automatically. A neighbor
operation waits until both endpoints satisfy the configured Link time. Unarrived
support cannot relay through a second Link in that tick. Periodic seams use the
ordinary six-Port topology in every axis. This finite quantum circuit has no
implicit extra modes or exterior quantum escape; open-world ordinary carriers and
classical fields retain their existing exit accounting.

An actual source contact replaces one ordinary record only at commit. It reserves
the occupied local slots because pre-contact field coupling may also change a
third resident; capture additionally reserves one empty output slot. Unused empty
slots remain available for arrivals during the wait. All alternatives preserve
the common field reaction and every coupled resident. Source and output conserved
values must match, including runtime seed overrides; mismatches fail before a draw.
Contact conversion takes one local cycle instead of the ordinary carrier planner
at that Node. Source and capture templates therefore do not inherit unspecified
simultaneous ordinary update or collision laws.

Resident detectors attempt capture on their ordinary cycle clock, including
vacuum, until a localized output is present. This models a continuously active
detector, whose no-click instrument can alter subsequent coherent evolution.
Every alternative has cost `2*read + 2*update + commit + 1`, plus any common
classical field work. The final unit is the quantum request under Q-ORACLE-1.
Normal budget delay applies before the request executes; there is no ownership
escrow. Gate/read tariffs and cancellation certification are separate quantum
audit work, never a remotely observable change in carrier delay.

Public event-backed steps and state snapshots share the event transaction lock.
Concurrent readers cannot observe a quantum transfer before its ordinary
installation. This does not enable parallel Node planning, which remains rejected
for event programs. An origin bank is polled once per tick. A resolution after
that poll is retired on the next poll; ordinary fields are never swept or reset.

`run.json` records `computation.resolver.contact_transfers`, exact quantum records,
costs and the quantum inventory sector. `state.json` and optional playback expose
`event_support` separately from ordinary disturbances and spatial fields. These
are conservative origin references, possibly with zero amplitude; they are not
sampled positions, charge copies or probabilities. Rendering only reads them.
Headless runs load no renderer. Field emission requires finite budgets; schema 2
also declares decay and localized/dissipated residue under the existing field law.

## Numerical acceptance

The [local moment-response candidate](../examples/quantum/local_moment_exchange.md)
uses a later ordinary pair conversion after capture, preserving this profile's
initial held/unknown output. Its supplied mean and variance are not derived from
the spatial wave. Converted emitters remain unsupported. A separate regression
checks arrival into an unused slot during delayed capture: an empty reserved
output slot stays locked, while an unlocked spare receives the incoming record.

[The focused tests](../tests/test_localized_quantum_contact.py) check source
conversion at tick 0, capture at tick 2 two Links away, charge -1 and mass 1 at
every tick. Finite ordinary sources inject -6 before conversion and -12 after
capture, recorded separately from charge. A delayed C=6, B=1 example transfers
ownership at ticks 5 and 11. A 3:4 mixing operation gives probabilities 9/25 and
16/25; its inverse recombines to probability one. Exhaustive tickets give sixteen
local clicks out of twenty-five with and without the remote detector, at equal
local cost. These are finite candidate checks, not a general no-signalling theorem.
