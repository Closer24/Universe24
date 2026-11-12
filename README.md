# Universe24

Universe24 has one supported execution path:

**complete integer seed + immutable local tensor → reversible Engine → passive click decoder → validation**.

Every input bundle is rejected unless it has at most **48 total retained channels per node**, including all geometry, matter, clocks, apparatus, scheduling and workspace. Each channel retains `(a,b,r)`. All evolution uses exact integers and the same fixed rule:

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

The tensor has degree at most three, strict physical face-edge support and acyclic old-`a` dependencies. The full retained state is reversible. Recorded clicks are a passive, potentially information-losing observation.

**The execution architecture is implemented; a general Einstein model with matter and physical clocks/detectors within this budget is not yet established.** No default model is silently substituted. A successful run/replay establishes mechanical evidence, not Einstein convergence or Born statistics. `python -m universe24 status` reports the blockers, and `verify --require-physics` fails until independent physical acceptance exists.

## One command

```bash
python -m pip install .
python -m universe24 status

# Supply the complete declared inputs; no future-state callback is allowed.
python -m universe24 prepare \
  --tensor tensor.json --seed seed.json --channels channels.json \
  --protocol protocol.json --model model.json --out runs/input

python -m universe24 run --bundle runs/input --steps 12 --out runs/output
python -m universe24 verify --run runs/output
# Deliberately fails while the physical research gates remain unresolved:
python -m universe24 verify --run runs/output --require-physics
```

`prepare` seals the supplied tensor and initial state; it does not solve Einstein initial constraints or invent a physical model. Model metadata identifies the equations, version and domain. It cannot grant physical certification. The Python preparation API is `universe24.system.bundle.create_bundle` and `save_bundle`; see [the input and output contract](docs/ONE_SYSTEM.md).

The bundle contains `bundle.json`, `tensor.json`, `seed.json.gz`, `channels.json`, `protocol.json` and `model.json`. Ownership lists every channel. The manifest binds all components by hashes and records lattice, budget, law and inverse stages. The runtime saves its exact input bundle, complete transition trace, canonical clicks and a validation report. Verification reexecutes each transition, checks the inverse, and reproduces the click stream.

Integers have arbitrary bit length; 48 channels does not imply bounded memory. Run reports record integer growth. Output histories are never read as extra evolution state.

## Modules

| Module | Contract |
| --- | --- |
| `universe24/system/bundle.py` | Complete inputs, exact schema, integrity, channel budget and locality |
| `universe24/core/` | Immutable tensor and unchanged fixed-six Engine |
| `universe24/system/decoder.py` | One canonical arithmetic click decoder, passive and deterministic |
| `universe24/system/runtime.py` | One run/replay/verify path and scoped evidence |
| `universe24/runtime.py` | Public CLI: prepare, run, verify, status |
| `validation/` | Source-only independent oracles and historical audit harnesses; excluded from installation |

The previous ADM driver, demonstration commands and `experiments/` entry points have moved to `validation/`. The public CLI has no ADM/reference/FLRW/probe selector and no override for the 48-channel limit. Historical construction helpers retained in `layers/`, `prepare/` and `observe/` are research dependencies; they are not accepted alternate physical systems. Historical evidence keeps its source revision and does not become current evidence by renaming files.

## Verification and research

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
```

The smoke input is explicitly a mechanical test fixture, not a supplied Einstein universe. The source-only `validation.team48_contract` adapter also passes the pinned 44-channel sourced proposal through this same runtime and compares every retained state to its independent scalar oracle. CI supplies the exact external source pin; this compatibility result does not promote the proposal to a physical default.

The same saved 44-channel run can be inspected without changing its dynamics:

```bash
python -m validation.team48_observables --audit runs/team48-contract --source validation-reference
python -m validation.team48_board --observables runs/team48-contract/observables.json --out runs/one-system-board.html
```

The board shows exact metric/link diagnostics, scalar/dust/Maxwell energy,
momentum, stress and signed classical charge. It also exposes Hamiltonian,
momentum and torsion defects. These are retained-state readouts, not physical
measurements decoded from detector clicks. Opposite U(1) charge is not a claim
of quantum antiparticle counts or annihilation. Complexity growth/selection
remains the explicit open task in [issue #45](https://github.com/Closer24/Universe24/issues/45).

Tests retain independent Einstein equation checks and known counterexamples. A regression test can pass by confirming that a proposed physical construction fails; the corresponding physics gate remains failed.

## Same-run geodesic board

From this repository checkout, generate a complete saved run and an interactive,
self-contained event board with one command:

```bash
python -m validation.geodesic_board --out runs/geodesic-board
python -m universe24 verify --run runs/geodesic-board/runtime
# Open runs/geodesic-board/board.html in a browser.
```

This prepares one explicitly massive corrected full-frame tensor with **45
channels**, then executes it through the same bundle/runtime above. The saved
metric supplies null and timelike geodesics, proper-time integrals, scalar/dust
energy and the visible Einstein constraint residual. The HTML works offline;
its time slider and playback inspect the saved run without evolving a second
system. Exact inputs, transitions, arithmetic clicks, provenance and independent
constraint/clock/quantum audit reports accompany it.

The current fixture is a finite homogeneous scalar/dust preparation. Its
geodesics are **passive test paths in the reconstructed metric**, not retained
probe dynamics or evidence of general Einstein convergence. The initially zero
Hamiltonian constraint becomes exactly `-7*dt**2` after the first update; this
failure is displayed and tested. Quantum audits validate complete-trial and
selection controls, not an Engine realization of Born or Bell physics. See the
[integrated report](docs/research/geodesic_board/README.md) for the eight-agent
results, domains and remaining work.

[The standard model report](docs/ONE_SYSTEM.md) defines the research question, equations, module boundaries, methods, results and gates A–F. [The proposal index](docs/proposals/INDEX.md) records the inherited ADM, Frame48, null and FLRW work. [Issue #40](https://github.com/Closer24/Universe24/issues/40) coordinates the missing coupled encoding, refinement, shared-metric apparatus and detector physics.
