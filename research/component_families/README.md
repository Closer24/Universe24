# Reusable family components: compact evidence

Use the exported factories in [`research.components`](../components/__init__.py),
the existing generic [JSON experiment runner](../experiments/run.py), and the
[API and algebra guide](../../docs/LOCAL_BUILDING_BLOCKS.md).
This package contains reproduction tools and evidence, not another engine.

## Quick runs

```sh
python -m research.experiments.run --spec research/component_families/examples/three_clocks.json --output runs/three-clocks
python -m research.component_families.verify --output runs/family-check
python -m research.component_families.verify --case holdout-L233-D28-w0p1 --case holdout-L233-D28-w1p1 --presenter --output runs/register-view
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/runs/three-clocks/The_Presenter.html` or
`http://localhost:8000/runs/register-view/index.html`. Each linked Presenter is
complete and offline-capable. The HTML requires JavaScript in an actual browser;
an attachment preview may display only its static shell. Rotate the cube by
dragging. The renderer, classifier and engine are unchanged.

The verifier refuses existing output directories. `--case` accepts any exact
ID in [`evidence/index.json`](evidence/index.json), repeatable for controls.
Omit it to replay the entire published subset. `--presenter` records and exports
each selected complete run through the existing recorder and renderer. The
scientific states are regenerated, not simulated by the HTML.

## What is shipped

| Cohort | Original recordings | States | Purpose |
| --- | ---: | ---: | --- |
| Cube, dimer and plaquette clocks | 5 | 109 | Representative full cycles and both J signs for period-five bodies |
| Cooperative pair | 4 | 100 | Both cores, each alone and neither, same prepared hardware |
| Complete even packet | 2 | 98 | Whole-state translation at two sizes |
| Guided scatterer | 4 | 196 | Source with/without downstream target at both sizes |
| Single-read holdouts | 8 | 456 | All four source masks at two new geometries |
| Repeated-read test | 8 | 712 | Six passing controls and two scientifically failing dual-probe cases |
| **Total** | **31** | **1,671** | **1,640 native transitions** |

These exact trajectories were independently audited locally before promotion.
The original records remain local; this repository stores a lossless
**reproduction specification**, not their large rendered/full-record copies.
Each compressed fixture contains the complete sparse initial state plus explicit
background (therefore the entire board), fixed tensor and fingerprint, exact
case parameters, `seed: null` for deterministic preparation, horizon, every
full-state SHA-256, selected fixed original observations and original record
hash. The index is pinned in the verifier. Original executed source hashes and
frozen audit hashes are in [`provenance.json`](evidence/provenance.json).

Selection was for this documented API contract, after the original study; it is
not a new preregistered discovery cohort or an unbiased emergence sample. All
single-read holdout masks and all repeated-read masks are included. Historical
source-off scatter controls used counter masks; the public true-absence controls
are instead exact all-counter-zero stationary configurations checked by tests.
No claim is made that all 553 local study recordings are included here.

## Checks performed on replay

1. Validate inventory, source provenance, fixture hashes, unique IDs and complete
   initial triples. Reconstruct the public API preparation and compare it exactly.
2. Derive all coupling ports/weights independently from `research.reference`
   matrices. Its new sparse **gather** oracle imports no production engine,
   state, Rule3 or click classifier. Stationary background closes every omitted
   address; every possible recipient is included before gathering six donors.
3. Compare every full native state to both the independent update and original
   digest; check both inverses at every step and rewind the entire native run.
4. Recompute all native C classifications, exact algebraic q, clock recurrence,
   packet translation, three-packet full-state factorization, fixed read input,
   outgoing full templates, full576-triple restoration and reference clocks.
5. Preserve scientific failure separately from arithmetic validity. Both
   dual-probe runs must reproduce their failed second input, with `u=0` at57.

The checks and their finite domains are defined in
[`observations.py`](observations.py), separate from preparation and evolution.
The report records source hashes and CPU time after imports. No exact historical
resource total or physical significance is inferred from that measurement.

## Scope

The strongest new readout result is **source-overlap register clearing followed
by one controlled remote orthogonal read**. The four memory addresses are part
of the writer's initial remainder halo. They are not a disjoint remote detector.
The stored r0/r2 difference gives C2 for **unwritten**, no selected C for written.
Template rejection does not erase information. Two-read composition fails
despite local restoration. The guided target resets and produces three packets;
it does not retain remote memory.

No physical photons, massive particles, electric charge, quantum spin,
complexity-based path selection, Born rule, gravity or physical elapsed time are
derived by these API examples. Exact mathematics, bounded native computations
and remaining hypotheses stay separate.
