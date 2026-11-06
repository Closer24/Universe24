# Experiments, seeds and reproducibility

Experiments configure initial data for the **same** generic engine; they never supply new physics or per-experiment node logic.

## JSON schema in practice

```json
{
  "side": 9,
  "coupling_signs": [1, -1, 1],
  "background": [0, 0, 2],
  "seed_changes": [
    {"position": [4, 4, 4], "channel": 0, "state": [0, 2, 2]}
  ],
  "steps": 12
}
```

| Field | Required? | Rules |
| --- | --- | --- |
| `side` | Yes | Integer `L >= 3`; cube geometry is always `L × L × L` |
| `coupling_signs` | No | Exactly three integers from `[-1,+1]`, in body-axis order `x,y,z`; default `[1,1,1]` |
| `background` | No | Triple `[a,b,r]` with `a=b=0`, `r` one of `0..5`; default `[0,0,2]` |
| `seed_changes` | No | Unique channel-address overrides, each with a position, channel and state; default empty |
| `steps` | No | Nonnegative integer count of reference updates; default 0 |

A `seed_changes` record has `position: [x,y,z]` (three integer coordinates from 0 through `L-1`), `channel` (integer 0 through 47), and `state: [a,b,r]` (two exact integers and `r` from 0 through 5). Duplicate addresses, invalid coordinates and unknown configuration keys are rejected.

All 48 channels at each unlisted spatial site remain in the chosen background. A random seed number alone does **not** define a complete state unless a deterministic generation algorithm is also supplied and documented.

## What is allowed to change?

Before running: the side, fixed coupling-sign choice, prepared states and reference step count. The coupling can have three signs because it is a **structural variant**, not a dynamic toggle.

After starting: no state injection, coupling adjustment, detector decision, replacement of another state, or post hoc erasure. Using `--resume` continues Rule3 from an existing complete state.

## Included examples

- [`impulse.json`](../examples/impulse.json): reference positive coupling and a channel-0 impulse at the center.
- [`signed_impulse.json`](../examples/signed_impulse.json): the same type of impulse using the fixed `[1,-1,1]` signed tensor.
- [`clock.json`](../examples/clock.json): a prepared motif in channels 0 and 14. This tests a possible local recurrence, **not** a physical particle, atom, or operational clock.

A useful comparison holds the side and seed fixed and varies only `coupling_signs`, then compares recorded full-state trajectories or diagnostics. A different coupling choice means a **different fixed candidate model**, not a change within one run.

## Saving and resuming

The full-state checkpoint includes: format version, completed reference steps, coupling fingerprint, cube size, signs, background and all deviations from background. Its content is sufficient to continue the same deterministic trajectory provided the same engine/coupling algorithm is used.

An event log includes **only selected arithmetic observations**. It is not a state checkpoint and cannot reconstruct the full trajectory.

The CLI uses exclusive file creation. Choose new filenames for each output; output paths must differ from input paths.

## Audits and reproducibility

`--audit` checks three mathematical properties on each step: exact one-step inversion, local Rule3 balance, and the expected global change of the signed algebraic account. For frustrated signed coupling, the signed account is **not necessarily conserved**; that is not a failed audit if its calculated change matches.

For reproducible publications, include: commit SHA, `side`, all body signs, complete seed or checkpoint, background, number of updates, output/readout definition, precise comparison method, and whether the audit was enabled. Report negative controls and cases that fail as well as successes.

## Performance

The state is sparse around a fixed background, but spatial influence can spread to new channels over time. Memory cost can therefore grow toward the entire cube (`48 L³` channels, each with three stored numbers), with additional overhead from Python's arbitrary-precision integers. The engine is an exact reference implementation, not a high-performance solver optimized for very large universes.
