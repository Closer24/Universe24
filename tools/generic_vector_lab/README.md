# Generic vector lab

An independent executable prototype, outside Universe24's simulator. It tests
mechanisms and exact conservation on finite examples. It does not implement the
Standard Model, replace the current engine, or prove numerical stability over
arbitrary trajectories.

## Run

Python 3.14.7 was used. The runtime and demo use only the standard library.

```powershell
python -m tools.generic_vector_lab.run_demo
python -m pip install pytest
python -m pytest tools/generic_vector_lab -q
```

Run these commands from the repository root. The demo writes `artifacts/generic-vector-lab/report.json`, including every product and exact before/after
energy, momentum and charge totals. Use pytest `--junitxml=artifacts/generic-vector-lab/tests.xml` to record test results.
`definitions.json` is the runtime input. Edit it directly to change formulas,
types, reactions, balances, coefficients or schedule weights, then rerun.
There is no compilation step. `build_examples.py` is an optional authoring helper;
running it overwrites the example JSON, so do not run it after editing that JSON.

## Files and generic contract

* `algebra.py`: bounded rational scalars and 3-vectors, addition, subtraction,
  scalar multiplication/division, dot product, cross product, dimensional checks
  and a bounded expression interpreter. No Python `eval` or callbacks.
* `runtime.py`: typed immutable records; generic atomic N-to-M transactions;
  configured balance checks; adjacent-cell transport with ownership in links;
  reproducible weighted event scheduling; local complex amplitudes, unitary
  evolution and measurement coupled to physical transactions.
* `definitions.json`: external entity fields, derived quantities, mass-shell
  constraints, reaction outputs, elastic impulse, field mixing, quantum rotation
  and discrete decay weights. Entity names have no special engine meaning.
* `test_lab.py`: independent expected outcomes, invariants, failure/rollback cases,
  bounds, schema extensions, transport ownership and reproducibility.

Expressions use `{"ref":"a.p"}`, `{"value":[1,0,0],"unit":"energy"}` or
`{"op":"dot","args":[...]}`. Intermediate quantities use the reaction's `let`
mapping. Rational literals use `{"value":{"n":3,"d":5}}`. A new balance is a
JSON entry containing its zero quantity and per-record expression; no runtime
branch needs to know the quantity's name. Tests rename particle and momentum
labels and add a new conservation rule without changing runtime code.

## Node participation and compatibility configuration

The `limits` object in `definitions.json` specifies `cell_capacity`,
`max_participants`, `max_products`, `link_capacity` and `match_attempts`.
There is no hard-coded 16-participant limit. The current demo chooses six;
a separate test changes only configuration and executes a 17-input transaction.
Invalid/nonpositive limits and oversized rule declarations are rejected.
Formula and numeric representation budgets remain separate implementation limits.

Each reaction's `inputs` list defines its exact participant count and allowed
type(s) for each named role. For example `six_node_exchange` requires two A,
two B and two C disturbances, all in the same node. Six arbitrary records do
not qualify. Missing rules and incompatible compositions cannot interact.
Optional `when` expressions add property conditions, such as charge or energy
thresholds. `outputs` and `let` define the actual shared transformation.
There is no default all-to-all interaction or implicit contact normal.

Binding is independent of the caller's ID order, with deterministic ascending-ID
backtracking for overlapping type sets, limited by `match_attempts`. The first
type-compatible binding is used; `when` then validates that binding. The engine
does not search other bindings to satisfy `when`, automatically select among
competing reaction rules, or scan all subsets of a node. The caller chooses a
named rule and participants. A rule failure leaves the node and ID allocator
unchanged. Same-type roles can have different formulas; role ordering is explicit.

Run `python -m pip install pillow` and `python -m tools.generic_vector_lab.node_movie` for the new demo.
It writes `node-states.json`, `six-node.gif` and hash-based provenance. The GIF
shows the six recorded momentum vectors before and after one simultaneous node
reaction; camera motion emphasizes depth. These are two physical states, not 64
simulated ticks or fabricated approach/departure trajectories. No field is drawn
because this demo defines no field. Its orthogonal momentum mapping is a toy
configured law, checked for conservation on the actual input; it is not a derived
universal scattering law. The older `elastic` rule remains only as a separately
named algebra test and is not used by this node demonstration.

## Energy and momentum

These examples use normalized natural units, c=1. Mass, energy and momentum
therefore share a dimension. The two dimension exponents represent square-root
energy and charge, allowing the example quadratic field energy to be checked.
This is deliberately not a complete SI dimensional registry.

* Classical records derive E = dot(p,p)/(2m); this E is kinetic energy only.
* Relativistic records store E, p and m and validate E squared = dot(p,p) + m
  squared, with positive E and m. Rest energy is m; kinetic energy is E-m.
* Massless pulses validate E squared = dot(p,p), with positive E.
* Toy field records derive E = dot(amplitude,amplitude)/2.
* The bound-state example converts two rest-energy units into a bound record
  with one rest-energy unit and two opposite photons, each carrying half a unit.
  Binding is represented by the configured mass defect. Do not additionally add
  a separate negative binding term, which would double count it.

Classical and relativistic energy conventions should not be mixed in a physical
experiment without explicitly reconciling their reference energies. Examples
are separate experiments, not a common physical material model. Electron and
positron labels use normalized mass 1; they are not fitted experimental data.

Every transaction checks all configured scalar/vector sums before committing.
Residents and in-flight link records both appear in the read-only total ledger.
No global correction force or rescaling repairs failed balances. Charge sign
does not imply negative mass. Reactions must explicitly authorize input types.

## What is actually exercised

| Capability | Example or test | Scope |
|---|---|---|
| N-to-M changes | 1-to-2 decay, 2-to-1 absorption, 2-to-2 annihilation/creation, 2-to-3 capture, 3-to-2 breakup | Atomic outputs, no partial deletion |
| Energy accounting | Rest/kinetic decomposition, photons, binding mass defect, field amplitudes | Exact configured balances; no full electromagnetic field energy |
| Kinematics | Massive and massless on-shell records, recoil, threshold rejection | Supplied rational output kinematics; no arbitrary scattering solver |
| General contact | Elastic impulses along arbitrary nonzero 3-D normals, unequal masses | Normal supplied by caller; no geometry/contact detector |
| Coupled fields | Local 3/5 and 4/5 orthogonal amplitude mixing | Energy-preserving toy coupling, not Maxwell equations |
| Stochastic events | Seeded discrete survival/decay and weighted tickets | Discrete hazard; no measured lifetimes or cross sections |
| Quantum coupling | Complex phases, interference, 9/25 and 16/25 Born weights, collapse plus physical decay | At most four local basis states; no nonlocal entanglement or QFT |
| Bound/internal states | Capture, breakup, absorption and emission with recoil | Configured levels; no spectrum solver |
| Vector diagnostics | Dot/cross identities, angular momentum, q(E+v cross B) expression | Algebra checks only; no integrated EM evolution |
| Local transport | One-hop handoff, blocked destination, conserved ownership | Abstract 1-D cell graph; no world geometry renderer |

For the equal-mass oblique contact with p1=(1,0,0), p2=(0,0,0), normal=(1,1,1),
the tested outputs are p1=(2/3,-1/3,-1/3) and p2=(1/3,1/3,1/3).
Total p remains (1,0,0); kinetic energy remains exactly 1/2.
Absorption combines a mass-2 resting record and an energy-3 photon into an
excited mass-4 record with E=5 and p=(3,0,0), including recoil.

## Numerical and scheduling limits

Retained signed numerators use positive integer codes; denominators are positive
and reduced. Payload magnitude is bounded by 2^30-1, with explicitly checked
signed 64-bit working arithmetic. Values are never silently rounded. Irrational
outcomes, denominator growth or overflow require another numeric representation
or an explicitly designed approximation policy; this prototype rejects them.
Python storage itself is not a hardware proof of fixed-size memory.

Cell and link capacities and participant/product limits come from configuration. Expressions are
bounded to 128 nodes and depth 16. Local quantum dimension is at most 4. The host
owns the number of cells and invokes ticks; this is not a benchmark of Universe24.
The RNG is xorshift32, for reproducibility rather than cryptographic use. One
bounded rejection attempt avoids modulo bias; rejected tickets defer the event.
A failed reaction returns no advanced stream and changes no physical state.
Scheduling order is caller-defined. Measurement returns a new immutable collapsed
state only after its physical transaction succeeds.

## Still required for physical completeness

A complete local field propagator with energy and momentum, boundary reservoirs,
generic geometry and continuous collision detection, arbitrary relativistic
outcome generation, measured reaction laws and cross sections, quantum spin and
statistics, multi-body bound-state dynamics and validation against experiment
remain outside this prototype. Passing these tests demonstrates the listed
software mechanisms on their cases, not support for every real particle.

## Saved visual evidence

[Six-node GIF](https://drive.google.com/file/d/1K6lCENFGADLUPaSvPzXDaZVrZ7juvdHl/view)
shows the recorded before/after vectors.
[Original code and evidence package](https://drive.google.com/file/d/1M1jW_KUasWM4wgefz5OP86MYh7PXIXh4/view)
retains the standalone delivery. Git source uses module imports and writes generated
outputs below artifacts instead of beside its source. No active simulator imports
this opt-in lab. No durable Skill update is needed: the existing workflow applies.
