# Local scattering and a vacuum Maxwell limit

This experiment selects a new microscopic field hypothesis through ordinary
initialization data. Its conditional long-wavelength vacuum Maxwell generator
and measured axial/oblique frequencies agree. Exact centered Gauss conservation
and instantaneous macroscopic electromagnetic energy conservation fail.
This is not a complete electromagnetic model.

Six transverse vector populations form one configured field group. E and B
are moments of those populations, not additional duplicated stock. The engine
and existing entity catalog defaults are unchanged; names select no engine law.

## Local hypothesis

At each node, form two sums of the six resident populations: their vector sum
and their direction-cross-vector sum. Reflect the populations about the
subspace represented by those moments. Transfer each population through its
own directional link. These are bounded sums, cross products, sign changes,
subtraction and exact halving. No time derivative, spatial derivative, Maxwell
equation or continuum force law supplies a physical update.

Choosing the moment map and reflection is additional microscopic structure.
Conservation and locality alone do not force this choice. The independent
[derivation and forecasts](DERIVATION.md) were prepared before engine execution.
The formal low-frequency generator has wave speed one half link per tick;
the causal link speed stays one link per tick. Units are never rescaled to
hide that distinction.

| Contract | Selection |
| --- | --- |
| Identity | `transverse-six-port-reflection-v1` |
| Inputs | Six resident transverse vectors; every remote input crosses a completed neighbor link |
| State | Six signed vector fields, zero baseline; one reachable outgoing channel per population |
| Parameters | Fixed amplitude scale `2**20`, one-tick transit; same scattering for all sizes |
| Outputs | Atomic reflected stock, then ownership transfer to six links |
| Local invariants | Both vector moments, population squared amplitude, each population's transversality |
| Precision | Initial projection spends two binary factors; 18 generic halving steps remain, subject to runtime bounds |
| Diagnostics | Fourier frequency, divergence and quadratic norms; read-only and never fed back |

## Run and inspect

Use the project Python 3.14 environment with `render` dependencies from the
[main instructions](../../README.md#install-and-run):

```bash
PYTHONPATH=src python examples/maxwell/run_experiments.py --output artifacts/maxwell-new
```

The harness saves eleven JSON initialization files and invokes the canonical
runner and HTML generator for each run. Its standalone `report.html` embeds
compressed complete original players; no frame is removed and no GIF is made.
A modern browser is required for the compressed player. Node playback shows
the six populations; report plots show their measured E/B moments.

Edit a saved initialization and execute it without rebuilding:

```bash
PYTHONPATH=src python -m event_universe.runner \
  --init artifacts/maxwell-new/inputs/axial-15.json \
  --output artifacts/maxwell-edited --visualize
```

`--resume` reuses only successful recordings whose exact input bytes and
runtime fingerprint match. It permits read-only diagnostic updates without
rerunning physical evolution. Changed or failed runs are not silently reused.
Generated output follows the [retention contract](../../docs/RETENTION.md).
The reproducible generators and acceptance criteria remain in source control.

## Completed measurements

Eleven experiments completed 138 field steps and 149 recorded frames on
Python 3.14.7, runtime source fingerprint
`b380a79428e0fcdb103ba92c16ae3df903da1229197c586e932a6e583256b299`.
Independent review reconstructed every frame's moments, population norm and
transversality, and matched 145,520 sent packets to causal one-hop arrivals.
The eleven runs were repeated after the shared-vector refactor in main
`2fe9c43b9ffe6033e428d83861ca4c3461651347`; all frames and entire event traces
were identical to the earlier runs. Integration then included main
`99b9f5f0034ea288f7de0a2a8d7645220c45d8aa`. Its only added source module is
the unreferenced read-only `diagnostics/node_contract.py`; the executed source
files and candidate inputs are unchanged, so the recorded physical evidence
is reused without relabeling its source fingerprint.

No source injected new stock. Both summed vector moments and full population
norm were exact, separately from the per-field transformation accounting.

| Experiment | Space | Measured result |
| --- | --- | --- |
| Electric-only axial mode, period 9 | `9 x 3 x 3`, periodic | Phase speed 0.5000000000000001 |
| Same axial mode, period 15 | `15 x 3 x 3`, periodic | Phase speed 0.5000000000000001 |
| Second polarization and cyclic axis rotation | `9 x 3 x 3`, `3 x 9 x 3` | Same frequency and speed |
| Asymmetric oblique `(1,2,0)`, period 9 | `9 x 9 x 3`, periodic | Speed 0.4914676951; error from 0.5 is 1.70646% |
| Same oblique mode, period 15 | `15 x 15 x 3`, periodic | Speed 0.4970237415; error 0.595252% |
| Same initial state, scattering disabled | `15 x 3 x 3`, periodic | Oscillatory branch speed 1, not 0.5 |
| Axial longitudinal control | `15 x 3 x 3`, periodic | Static electric pattern; magnetic moment stays zero |
| Initially centered-divergence-free oblique field | `9 x 9 x 3`, periodic | Exact initial zero; nonzero divergence after one step |
| Compact electric seed | `9 x 9 x 9`, `15 x 15 x 15` | Identical translated populations through three steps, inside causal cone |

The standing waves begin with B exactly zero and develop magnetic response.
Even streaming without reflection does that: magnetic appearance alone does
not establish Maxwell. Frequency, polarization and scale controls are needed.
All wave recurrence residuals are below `3e-14`; the candidate was not adjusted
after measuring them. Axial E and B Fourier moments at even ticks agree with
the standing vacuum target within `1.9e-15` relative error. Odd microscopic
steps still contain kinetic deviations, visible in the energy plot.

Period 15 tests a longer wavelength with unchanged elementary units and rules.
Thin periodic axes represent plane waves uniform in those directions, not
localized 3D radiation. The compact point seed tests locality and domain size;
its initial Gauss divergence is nonzero at adjacent empty nodes. The diagnostic
includes those nodes. The longitudinal control also violates the charge-free
initial constraint and is used only to inspect the stationary sector.

## Blockers and proposed directions

1. **Exact centered Gauss fails.** The stronger control initializes E as an
   integer centered curl, making initial divergence exactly zero. Its raw
   maximum becomes 12,582,912 after one step and 27,525,120 after four. These
   are amplitude-code differences at scale `2**20`, not SI charge. There is
   no charge source accounting for them. Magnetic divergence stays zero in
   this planar symmetry; general magnetic Gauss remains unproved.
2. **Population norm is not macro energy.** The minimum macro energy fraction
   is 0.733305 for oblique period 9 and 0.890807 for period 15. The remaining
   norm is in additional kinetic modes. Only the full norm is exact.
3. **Integer lifetime is finite.** A raw transverse amplitude of one needs an
   inexact half and is rejected atomically. The high-amplitude experiments do
   not prove unrestricted integer closure for unlimited time. Adding generic
   remainders alone would not prove quadratic conservation.
4. **Wave and causal speeds differ.** The low-frequency wave speed is 0.5;
   a compact precursor can cross one link per tick. Physical light speed has
   not been derived.

A possible next hypothesis gives oriented-link flux explicit ownership and
permits only signed closed-loop transfers, so divergence cancellation follows
from the transfer structure. It needs causal arrival/current continuity and
integer conservation proofs. It is not implemented here. Changing a divergence
readout after failure would not repair this model. A nonlinear reversible
integer scattering law is a separate direction for removing finite halving.
Writing a finite-difference Maxwell update into JSON would insert the target
dynamics and would not answer this emergence question.

Charges, currents, Lorentz force, matter coupling, material response, photons
and full Lorentz symmetry remain outside this experiment. The evidence supports
a conditional leading vacuum generator and finite mode agreement, not complete
electromagnetism or a complete continuum convergence theorem.

## Validation and handoff

[configuration.py](configuration.py) builds candidate JSON;
[cases.py](cases.py) prepares integer seeds;
[measurements.py](measurements.py) reads recordings;
[run_experiments.py](run_experiments.py) executes and saves evidence. The
[focused tests](../../tests/test_maxwell_configuration.py) cover local
reflection/involution, inexact-division rejection, one-link ownership,
independent frequency recovery and empty-node divergence. Use
`python tools/check.py` for affected checks only.

Highlights was reread at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Boss, field-development, simulation-runner and physics-rule-validation were
reviewed. Their current locality, ownership, hypothesis and independent-test
requirements cover these lessons; no skill or postulate change is needed.
