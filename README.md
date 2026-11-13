# Universe24

[Repository](https://github.com/Closer24/Universe24)

Universe24 asks whether the whole universe can follow one local integer law.
Each node receives information only from its immediate face neighbors and
updates its own retained integers. There is no direct communication across
distant nodes. This is the research postulate; deriving quantum observations
and gravity from it remains a task to test, not an assumed consequence.

Universe24 implements one execution path:

**complete integer seed + immutable local tensor → reversible Engine → passive records → independent verification**.

The same Rule3 updates every retained channel. Geometry, matter, clocks, apparatus, scheduling and workspace share **exactly 48 explicitly supplied node channels**, obeying the mandatory joint 2O channel/cube action. Each channel retains all three integers `(a,b,r)`:

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

All inputs read the complete old snapshot. The fixed integer polynomial has degree at most three, target-plus-one-physical-face support and an acyclic old-`a` dependency graph. No projection, reset, external solver or click callback advances the state. Arbitrary integer bit growth is reported; a channel limit is not a memory bound.

The software execution system is implemented and reviewed. Restricted sourced Einstein sectors are reproducible. **A single physical construction combining spatial gravity, operational detectors, repeated cosmological bursts and sustained complexity growth has not been established.** The research controls below keep their distinct tensors and domains; their successes cannot be pooled into that claim.

## Run and verify

From the repository checkout, install the package and run the supported mechanical smoke into a new directory:

```bash
python -m pip install .
python -m universe24 status
python -m validation.system_smoke --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
```

New preparations use bundle schema 3. Every model must supply 48 channels and
pass exact polynomial covariance under `2O-left-regular-cube/1`, for all 48
group elements. `research`, an omitted role, or an omitted symmetry declaration
does not disable the check. Explicit null or alternate symmetry values fail.
Preparation does not add padding or change the law to make it symmetric.
See [the action and representation limits](docs/COUPLING_ALGEBRA.md).

Read `runs/system-smoke/smoke.json` and `run/validation.json` under that
directory. The smoke compares complete states with an independent scalar
oracle and verifies exact rewind and canonical clicks. Success does not
establish physical acceptance.

The installed interface is always `python -m universe24`. To execute your own complete prepared input:

```bash
python -m universe24 prepare   --tensor tensor.json --seed seed.json --channels channels.json   --protocol protocol.json --model model.json --out runs/input
python -m universe24 run --bundle runs/input --steps 12 --out runs/output
python -m universe24 verify --run runs/output
```

Use new output directories. Preparation validates and seals the inputs; it cannot invent a physical model or certify an equation. `verify --require-physics` deliberately rejects a general physical acceptance claim while its gates remain unresolved.

A bundle binds tensor, full seed, ownership, protocol and interpretation by hashes. A run saves its input bundle, full transitions, canonical records and validation. Replay checks every transition, inverse and emitted record. Stored traces are evidence, never extra evolving state.

## What is integrated

The research results and reproduction commands below are historical records
from the [pre-schema-3 snapshot](https://github.com/Closer24/Universe24/tree/e281f7e7b251641a741d185116656fedaa5396f8).
Their source remains inspectable. Incompatible smaller or non-equivariant laws
are rejected by the current runtime, including the old system acceptance
collector; reproducing those old experiments requires their pinned source.

| Construction | Verified result | Boundary |
| --- | --- | --- |
| Native massless scalar + dust, six channels | Exact sourced expanding homogeneous FLRW flow, complete-history constraint, positive declared chart and independent Einstein-component checks | No mass term, spatial modes, detector or cosmological bounce |
| Native anisotropic massless scalar + dust, eight channels | Exact diagonal Bianchi I source, shear charges and source-based comoving proper-time invariant; independent metric and passive geodesic checks | Homogeneous only; passive moving probes; no retained detector or spatial momentum closure |
| Massive scalar + dust spinor coordinates, six channels | Exact decoded constraint, correct source pushforward and finite-time first-order convergence on a stated preparation family | Exponential integer cost; nonzero finite-step dust drift; no spatial detector |
| Generic interaction compiler | One local potential produces all declared reciprocal forces; counted native composition executes through the same Engine | Separate compiler controls do not implement the full gravity model |
| Full45 to six-channel symmetry restriction | Exact guarded reconstruction of both histories and all carries | Only the declared homogeneous neutral sector; the old massive45 constraint defect remains |
| Retained selection and record feedback | Local memory can change future carrier trajectories and phase | Record stress, bounded interaction energy and general spatial source closure remain incomplete |
| Repeated activity and structural growth | Exhaustive finite-sector recurrence and a fixed growth criterion are checked independently | Recurring activity is not a cosmological bang; sustained growth is not established |
| Quantum controls | Complete-trial, non-detection, preparation-measure and locality countercontrols | No derived universal Born rule or physical Bell instrument |
| Local carrier–record source, twelve channels | Repeated scattering, retained records, exact packet balances and a finite positive two-null-stream Einstein chart on the same saved history | Finite prepared supply; no globally periodic positive-source chart, massive bound body or operational clock |
| Finite gauge links, seven and ten channels | Static Z4 loop interference and separate dynamic Z2 record/link feedback | Static wave is unstable; dynamic sector has period three and no successive-edge propagation; no combined Maxwell/gravity law |
| Installed light component, 48 dynamical channels | Exact 2O covariance and unit-speed transverse plane streams through main prepare/run/verify | Six axis directions and flat background; no general Maxwell/Einstein coupling or photon detector |

The anisotropic extension retains two shear charges in eight channels; its exact metric and source share the complete state. A 4,096-update check passed independent scalar comparisons, inverse and full rewind with 26-bit peak integers. Its moving-probe paths and proper-time integrals are passive diagnostics, with no retained transported body. A same-tensor spatial negative preserves pointwise Hamiltonian constraints but fails the momentum constraint.

The native massless experiment has also passed 16,384 actual updates and full rewind with 30-bit peak integers. This efficient result belongs to its linear native volume law. It does not transfer to the massive projective spinor law, whose three-resolution checks reach 207, 649 and 6101 bits.

For the expanding native massless scalar/dust source, density decreases and the scale factor decelerates. Repeated homogeneous density bursts are incompatible with that declared source. The finite Boolean selector instead has recurrent activity, but its closed cycles exclude indefinite strict increase of a state-defined complexity score. These are two explicit limits, not a joint burst-growth solution.

## Inspect the saved geodesic board

```bash
python -m validation.geodesic_board --out runs/geodesic-board
python -m universe24 verify --run runs/geodesic-board/runtime
```

Open `runs/geodesic-board/board.html`. This retained **massive45 negative-control board** shows passive null/timelike paths, source diagnostics and the signed Einstein residual from one saved run. It visibly retains the first-step defect `-7*dt**2`; it is not the newly constrained six-channel solution, a transported material probe or a default accepted universe. Playback never evolves a second system.

## Architecture and source map

| Path | Responsibility |
| --- | --- |
| `universe24/core/` | Fixed tensor, lattice, exact state and Rule3 Engine |
| `universe24/light.py` | Installed 48-channel 2O light tensor and complete plane-wave preparation |
| `universe24/system/bundle.py` | Complete inputs, budget, strict locality and integrity |
| `universe24/system/runtime.py` | The sole run/replay/verify implementation |
| `universe24/system/decoder.py` | Canonical passive arithmetic records |
| `universe24/runtime.py` | Installed prepare/run/verify/status commands |
| `validation/system_acceptance/` | Source-only integrated evidence checks; no model selector |
| `validation/` | Independent research constructions and falsification controls, excluded from installation |

The architecture review is `docs/research/system_acceptance/architecture_review.md`. The complete idea decisions are in `docs/research/system_acceptance/idea_ledger.md`; the physical and massive-encoding boundaries are beside it. Current algebra is `docs/MODEL.md`, the execution contract is `docs/ONE_SYSTEM.md`, and source provenance is in `docs/research/central_integration/README.md`. Historical evidence retains its original source pin and is not relabeled as current validation.

## Run the installed light component

`universe24/light.py` is part of the installed main package. Its 48 dynamical
channels obey the exact `2O-left-regular-cube/1` polynomial contract, with no
idle padding. The same Engine advances its sealed bundle:

```bash
python -m universe24 prepare-light --out runs/light-bundle
python -m universe24 run --bundle runs/light-bundle --steps 6 --out runs/light-main
python -m universe24 verify --run runs/light-main
```

Use `prepare-light --axis y --polarization x` for a different transverse mode,
or `--sign -1` for the reverse direction. The prepared state translates one
face per tick exactly, indefinitely, without a precision scale. This provides
axis-aligned transverse plane light in flat spacetime; arbitrary-direction
Maxwell convergence, a dynamic Einstein source and photon detection remain
unestablished. The [component contract and archived experiment](docs/research/light_packet/README.md)
keep those boundaries explicit. The older 18-channel optical experiment is
preserved as historical evidence; it is a different tensor.

## What we need to research

The research backlog is maintained in `docs/RESEARCH_AGENDA.md`, together with
the disposition of the former PRs and issues. Closing those discussions means
their work has been integrated, retained as a reference, or moved to this agenda.
It does not mean the remaining physics is solved.

1. Construct one spatial coupling that joins geometry, source flow, reusable
   records and matter in the same complete state. Recover the validated
   restricted limits and check all independent Einstein constraints.
2. Build retained moving bodies and material clocks. Compare their actual
   trajectories and records with the same metric, including backreaction.
3. Demonstrate repeated bursts under that same fixed local law, without
   injecting or resetting state. Specify what counts as a burst before running.
4. Test whether structure persists and grows from burst to burst. Keep all
   trials, finite-memory exhaustion, insufficient histories and failed cases.
   Repeating a pattern or increasing amplitude is not structural growth.
5. Derive a stable propagating field, its source/energy accounts and the
   quantum preparation and detection statistics. Finite gauge symmetry and
   arithmetic clicks alone do not establish them.
6. Measure precision cost and convergence. Preserve exact rewind and the
   total 48-channel limit for matter, geometry, records and all workspace.

The current result is one software system with one execution path and one
central acceptance command. It still contains separately identified research
constructions. No single physical law has passed all six targets together.

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-smoke
python -m universe24 verify --run runs/new-smoke/run
```

A regression test may pass by reproducing a failed physical hypothesis. The corresponding physical result stays failed. No research label, channel name or successful replay can promote it.

The automated suite covers engine, tensor algebra, 48 channels, mandatory 2O
symmetry and bundle/replay integrity. Research unit tests and research CI jobs
are removed; source research programs and historical evidence remain. A green
CI run certifies software checks, not those physical results.

## Local carrier–record interaction with a spatial source chart

The [local unification package](docs/research/local_unification/README.md)
constructs bounded, conservative record–carrier scattering and a twelve-channel
source-dependent extension through the same saved-bundle runtime:

```bash
python -m validation.local_unification.run_all --out runs/local-unification
python -m universe24 verify --run runs/local-unification/geometry/runtime
```

The declared preparation supports repeated encounters without resetting records.
Independent current, recoil, complete-history and source tests inspect the same
run. A cubic-spline readout gives an exact two-null-stream Einstein solution on
a proved finite causal interior. Nonphysical periodic-seam defects are retained
and exposed; the whole periodic board is not certified as an Einstein universe.

This construction does not establish localized massive bodies, operational
proper clocks, sustained complexity growth or a new production default.
The central acceptance command also executes this collection and the gauge
controls, binds their summaries to independently replayed saved runs, and
rejects attempts to combine different laws or flux preparations as one result.
