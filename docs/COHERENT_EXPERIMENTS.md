# Local coherent mode experiments

## Implemented boundary

`local-coherent-modes-v1` is an explicit initialization schema and controller
using the existing `DeferredQuantum` event-network owner. It adds finite moving
mode supports, local coherent collisions, additive-sector guards, fixed neighbor
transit, local cost, terminal escape, conditional records and read-only reports.
There is no second wave owner or independent classical copy of a quantum branch.
The shared `CausalEventSpace` owns all event identities and causal metadata;
the quantum backend owns only its payloads. This preserves the namespace used by
[native event programs](NATIVE_QUANTUM_EVENTS.md).

The six examples in `examples/quantum/` are supplied finite candidates. Scattering
matrices and timed routing are input laws, not inferred electromagnetic physics
or emergent classical equations. The ordinary disturbance schema and spatial
computation field retain their own contracts; this quantum schema reuses cost
arithmetic but does not couple amplitudes to that ordinary spatial field.

## State, configuration and conservation

Required JSON keys are `schema`, `model_id`, `shape`, `boundary`, `link_ticks`,
`normal_budget`, `ticks`, `quantities`, `modes`, `state`, `rules`, `actions` and
`groups`. Optional `budgets` sets existing node/evaluation/term/record limits.
Unknown and duplicate keys, unresolved references and booleans as integers fail.
Configuration never imports executable code. Model, quantity, rule and mode names
are labels, not dispatch on physical identity.

A mode is a binary degree of freedom with a name, initial 3D position and one to
eight integer additive quantities. There are at most 30 modes in the quantum
owner and eight at a cell. `state` supplies occupied mode names and complex
Gaussian-integer amplitudes for each nonzero term of the initial joint state.
Alternatives are not additional copies of a target's mass. `groups` selects at
most sixteen read-only reductions, each containing up to eight mode references.

Every nonzero matrix entry must preserve each declared additive total between
its input and output occupation masks, including currently unused basis states.
Checking only the expected value is insufficient. Instruments obey those guards
and common-scale completeness. Conditioning can reweight initially different
sectors, but cannot introduce a new one; reports retain the sector distribution.

These quantities are diagonal observables of the finite model. A mode address
is its support/packet label, not a simultaneous sharp position and canonical
momentum eigenvalue. In the polarization/path probes, momentum labels are channel
inventories; target Fourier momentum and recoil broadening are unresolved. The
separate recoil benchmark supplies explicit energy-momentum channels. Neither
case derives a free-particle Hamiltonian or a continuum classical limit.

## Local actions and causal ownership

| Kind | Contract |
| --- | --- |
| `local` | One to four co-located modes; a supplied 2/4/8/16-dimensional unitary acts without sampling |
| `link` | One mode, one cardinal port; its entire degree of freedom moves one neighbor after fixed transit |
| `escape` | One mode crossing an open terminal port; full transit precedes permanent removal from further simulated interactions |
| `observe` | One local mode, a complete one-mode instrument and an explicit integer ticket; creates a persistent conditional record |

Moving a mode changes its address, not its amplitude, occupation, polarization
or identity. It is a directed quantum wire, not an exchange that could move an
occupied destination backward. Scattering changes occupation among co-located
outgoing modes. A returning wire therefore carries its original correlations.
Unoccupied alternatives can have declared routes without selecting a hidden path;
no occupancy query decides whether a coherent collision occurs.

Each action has an explicit positive model cost. Simultaneous disjoint actions
from a cell sum their costs before the shared `cycle_timing` calculation:
`extra = (max(1, ceil(cost / normal_budget)) - 1) * link_ticks`. The cell has a
common extra wait and no debt in later cycles. A local operation then takes one
tick; a link departs after that extra wait and arrives `link_ticks` later. A
destination's cost never sets the source wait. Reservations freeze involved
cells/modes through completion. An observation's cost includes its unit modeled
quantum query; graph evaluation and diagnostics are separate host work.

The immutable finite schedule is initial data. Setup checks local positions,
reservations and causal timing without reading amplitudes. It may reject an
impossible program; it never dynamically routes around remote congestion.
Runtime supplies bounded local operations at their reserved completions. A mode
cannot interact and cross a link in the same tick. Distant motion requires
successive completed links. Host setup/tick scans are not claimed O(1); fixed
local matrix/support work is bounded. There is no diagnostic feedback or
nonlocal ordinary force, field or movement input.

Periodic mapping reuses the existing lattice on all three axes. Open escape is
neither reflection nor measurement. Escaped modes remain only in the bounded
quantum environment so correlations are not erased; exterior motion is not
simulated and the mode budget is not recycled. Retained and escaped reports count
each occupation once. After observations they are conditional quantum reports,
not remotely available classical registers or an exterior signal.

## Failure and observation contract

One completed tick and its explicit records are staged and installed atomically
inside the same quantum owner. Invalid tickets, capacity, graph or record
arithmetic leave that tick uncommitted. Staging copies host graph containers
under Q-ORACLE-1, not another physical world used to calculate forces. There is
no coupled classical transaction and thus no cross-owner partial update.
Staged metadata publishes a suffix into the original shared ledger only after
success; intervening appends reject a stale stage. Transfers record destination
addresses and completed physical links. Host checkpoints compact quantum payloads,
retain causal provenance and do not restart an in-flight link's physical clock.

Signed 32-bit amplitudes and checked 64-bit intermediates remain mandatory.
Setup caps actions at 512, rules at 64 and duration at 10,000 ticks. Deferred
insertion can still reach a term/arithmetic budget during a later query; the run
fails with its last committed tick and trace, never a guessed outcome.

Exact checkpoints preserve the full correlated component and unresolved phases.
They do not replace a returning environment by a local density matrix. Read-only
partial traces report exact rational complex entries, purity and the sum of
squared off-diagonal magnitudes. Those reports never drive scheduling. One
Kraus operator per distinguished outcome is supported; an unresolved multi-Kraus
sum still needs a mixed-state extension.

## Runs and independent expectations

Use the prepared Python environment with this checkout on `PYTHONPATH`; editing
JSON requires no compilation, package build or installation:

```sh
python -m event_universe --init examples/quantum/three-photon-decoherence.json --output artifacts/three-photon-run
python -m event_universe --init examples/quantum/photon-return-erasure.json --output artifacts/coherent-return-run
python -m event_universe.integration.quantum_experiment --init examples/quantum/photon-return-erasure.json --output artifacts/checkpoint-return-run --checkpoint-every 3
```

Use fresh output paths. Initialization, completion/failure metadata, action and
causal-event JSONL, and observation JSONL use the existing 24-hour leases. Runs are headless, with
no renderer imports. The quantum schema rejects ordinary movie/duration
overrides; it does not present a classical sharp-particle movie as a quantum view.

| Input | Independent expectation |
| --- | --- |
| `photon-return.json` | A local polarization mark removes target interference. The same probe returns around four periodic cells at one cell per link tick. Return alone leaves zero target off-diagonal coherence |
| `photon-return-erasure.json` | A second local encounter inverts the mark and restores off-diagonal element 1/2. A phase applied while away can produce -1/2 instead. A full checkpoint leaves the result unchanged |
| `three-photon-decoherence.json` | Three distinct probes have conditional overlap 3/5 per encounter. Relative coherence is 3/5, 9/25, 27/125; final off-diagonal element 27/250 and purity 8177/15625, without outcome sampling |
| `conditioned-target-path.json` | An explicit outgoing-probe observation gives two equal-weight records. Each conditions a target alternative following a local configured route; averaging both preserves the unread marginal. This is supplied kinematics, not derived Newtonian motion |
| `photon-recoil.json` | Reversible local channel exchange maps target (E,p)=(12,0), radiation (6,6) to target (15,9), radiation (3,-3). Energy 18 and momentum 6 are exact; 15^2-9^2=12^2. Radiation then travels in -X. The supplied benchmark is not a Compton cross section or an emergent collision law |
| `photon-open-escape.json` | Escape occurs only after terminal transit. Exited radiation number is 1 and energy 6; retained energy is 12. Removing the environment from the simulated domain does not restore target coherence |

`tests/test_quantum_experiment.py` also tests axis/orientation changes, cost waits,
immutable arrivals, renamed modes, reordered declarations, forbidden remote
gates, invariant violations, resources and atomic failure. Physical return
preserves a possibility of recoherence, not automatic recovery. Decoherence and
a unique conditioned trajectory are distinct tests; see
[Zurek's review](https://arxiv.org/abs/quant-ph/0105127).

## Code owners and remaining physical questions

`quantum/event_network.py` owns the joint state, optional local modes, moving
addresses and atomic tick/record installation. `event_rules.py` and
`mode_rules.py` own bounded arithmetic and generic sector guards.
`integration/quantum_initialization.py` resolves data and static reservations
using shared geometry/timing. `quantum_experiment.py` supplies the clock and
headless outputs; `quantum_observations.py` only reads. `runner.py` selects the
schema lazily, leaving ordinary disturbance runs on their existing owner.

The finite representation gaps now compose in a runnable experiment: moving
modes, local coherent scattering, coherent return, exact declared balances,
configuration, records and result diagnostics. Arbitrary photon production,
indistinguishable bosonic Fock dynamics, a quantum electromagnetic field,
physical decoherence rates, autonomous collision dispatch and universal
quantum-to-classical dynamics still require additional model laws or experiments.
