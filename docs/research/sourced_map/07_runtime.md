# Saved-run integration of the sourced volume encoding

Researcher 7 of the owner's eight-agent task, tracked in issue #58. The
implementation is `validation/sourced_map/runtime.py`; run it with

```bash
python -m validation.sourced_map.runtime
```

The module is a source-only client of the existing `create_bundle`,
`run_bundle` and `verify_run` interfaces. It introduces no alternate public
runner, update callback, production model selector or decoder authority.

## One declared bundle

`make_bundle(program, seed)` requires the exact native law and the declared
constraint/physical chart before creating a research bundle. It never adjusts
the state. The complete native tensor, both histories, every remainder and an
exhaustive six-channel ownership manifest are saved by the existing runtime.
The allocation is six channels, eighteen retained integers per node, without
additional work or scheduling banks.

The immutable model metadata binds:

- The integer resolution `N` and proper-time step `h=1/N`.
- Unit lapse, the massless assumption and the expanding mixed-source domain.
- `V=b_volume/(4N²)` and
  `U=(b_volume-a_volume+3b_dust_charge)/(4N)`.
- Every retained scalar/dust charge and scalar-phase reference.
- The metric `ds²=-d_tau²+V^(2/3)(dx²+dy²+dz²)`, positive real root branches,
  and the logarithmic scalar coordinate interpretation.
- The distinction between full-state physical diagnostics and canonical
  arithmetic clicks.

`N` is static interpretation data, not another evolution register. Source
values and scalar integration constants are actual retained channels. The
canonical protocol remains exactly `default_protocol()`; physical calibration
is not smuggled into that arithmetic protocol.

## Executed saved-state checks

Three genuine runtime executions use `N=24,48,96` for respectively 3, 6 and
12 Engine steps. They reach the same proper time `tau=1/8`, with the same
physical preparation. The native tensor is identical across all resolutions;
complete raw seeds and bundle identities differ because the integer scales
differ.

`inspect_run(path)` first calls the existing full saved-run verifier, then:

1. Reconstructs the declared native program from saved model metadata and
   checks the actual tensor, ownership and interpretation against it.
2. Reads each complete saved before/after state and compares the after state
   against a separate scalar implementation of the Rule3 recurrence.
3. Verifies each complete inverse and final rewind independently.
4. Decodes `V,U` from the actual current and previous volume registers, then
   evaluates the exact rational source/constraint readouts and passive root/log
   physical fields. No state comes from a precomputed time trajectory.
5. Re-decodes the complete trace using the canonical arithmetic decoder and
   compares every saved click without filtering.
6. Checks exact zero physical constraint and the declared proper-time counter
   at every saved physical step.

The final exact coordinates are `V=355/256` and `U=51/16`. The rational fields
and equally evaluated high-precision root/log fields coincide across the three
resolutions. This is exact sampling of the stated restricted solution. It is
not a numerical convergence-order fit or evidence for general spatial physics.

A fourth actual three-step run changes one retained carry while preserving
all physical preparation values. Its physical readouts agree because carries
are transparent for this tensor, but its complete seed, bundle and run hashes
differ. The same-run comparison rejects that join. Equal physical fields do
not establish equal complete state.

A fifth three-step run shifts both retained time-counter histories by ten.
Its saved coordinate time starts at `10/24` and ends at `13/24`; the physical
fields agree with the zero-origin run. The physical reader checks each time as
`initial_tau+step/N`, so a legal coordinate-origin shift is handled consistently
by both bundle construction and saved-state inspection.

## Comparison contracts and negative controls

`require_same_run` checks locally produced receipts for the same complete run,
seed, tensor, time interpretation, trace and window. `compare_resolution` is a
separate, explicit comparison: it requires identical physical preparation,
retained scalar anchors and final proper time before comparing the exact
physical endpoint. It never labels different resolutions as one run.

Nine negative controls are retained:

- Same tensor at different resolutions cannot be joined as the same run.
- Equal resolutions cannot be labelled a cross-resolution comparison.
- A changed physical final time is rejected.
- A changed physical preparation is rejected.
- Identical physical fields with a changed complete carry seed fail same-run
  identity.
- Relabelling the bundle as a massive scalar is rejected.
- Changing the proper-time calibration independently of `N` is rejected.
- Calling a full-state diagnostic a click-only observation is rejected.
- An off-constraint seed is rejected by the physical research constructor,
  with no projection or alteration of its retained integers.

The receipts are compatibility records created by this module, not
authenticated certificates for arbitrary externally forged data. Hashes bind
the actual inputs; mathematical validity comes from the separate proofs and
checked domain, not from the hash itself.

## Reproduction and evidence

`runs/sourced-map/runtime.json` records all five saved-run directories, the
per-step rational and physical diagnostics, complete comparison counts,
source hashes and rejected controls. Saved bundles, complete traces, canonical
clicks and ordinary verification reports live under
`runs/sourced-map/runtime/runtime-*/`.

Every invocation uses a fresh output directory, so the runtime's refusal to
overwrite historical evidence remains effective. The public `run_audit(out)`
function also accepts an explicitly new directory. The standard command

```bash
python -m universe24 verify --run <one-recorded-run-directory>
```

replays any of the retained runs using the existing public interface.

The generic runtime keeps gates C, D, E and F as `not_tested` in every run.
This package's exact homogeneous massless-sector certificate is reported
separately. It does not establish a spatial detector, an independent material
clock, general Einstein evolution, massive-scalar dynamics or quantum measure.
