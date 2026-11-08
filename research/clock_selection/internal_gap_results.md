# Exact finite internal modes in the unchanged baseline

The native engine completed all 20 registered runs: 220 complete states and 200 transitions, with 20 complete rewinds. Every recorded triple agrees exactly with the integer oracle, and every native click address, class and quotient agrees with the registered prediction. Signed modes, a stationary uniform counter offset, and the inert remainder-parity control all pass their separate comparisons. [Independent replay](evidence/independent_audit/internal_gap_v1.json) confirms all native transitions, complete states, inverse checks and registered readouts.

The [protocol](internal_gap_protocol.json), SHA-256 `ff58a9cae8b106975a662c719af46496260ff8b807d6435f83554f4e3d50a449`, and executed producer, SHA-256 `a415e0346f523f121eda4edec1cc0f35e75e7b64d077632c15f948bfefdcc07b`, were frozen before capture. [Native evidence](evidence/internal_gap_v1/result.json) includes every preparation, full frame, raw C event and exact executed source. The [independent mathematical preflight](evidence/independent_audit/internal_gap_preflight_v2.json) preceded all trajectories.

## What was proved and what was tested

The [algebraic derivation](internal_gap_algebra.md) identifies an integer 48-channel vector v with `F0*v=2*v`, whereas the uniform channel vector has eigenvalue six. For spatially uniform preparation, the first gives `cos(omega)=1/3`; the stationary uniform branch has `omega=0`. These are two internal response families under the same +++ tensor and unchanged Rule3, with num=den=1.

For a chosen finite H, the entire board starts with

`a_g(0)=sign*3^(H-1)*v_g+M`,

`b_g(0)=sign*3^H*v_g+M`,

and remainder R, either two or three. Define the integer coefficients `C_0=C_1=1` and `C_(t+1)=2*C_t-9*C_(t-1)`. Then, through the declared H,

`b_g(t)=sign*3^(H-t)*C_t*v_g+M`,

with `a_g(t)=b_g(t-1)` and the remainder exactly R. This oracle was derived and checked before running; no frequency was fitted to an observed series. Its C_t coefficients are unrelated to the native C0/C1/C2 event labels.

The numerical runs test H=8 and H=12 on cube sides three and five, with five preparations for each pair:

| Preparation | Counter sign | Stationary uniform offset M | Remainder R | Observed finite behavior |
| --- | ---: | ---: | ---: | --- |
| gap_plus | +1 | 0 | 2 | Exact internal mode |
| gap_minus | -1 | 0 | 2 | Exact counter-negative mode |
| uniform_only | 0 | 1 | 2 | Unchanged state |
| gap_plus_offset | +1 | 1 | 2 | Exact internal mode plus stationary counter offset |
| gap_plus_parity | +1 | 0 | 3 | Same counters and events as gap_plus; every remainder greater by one |

Adding M to both counters throughout the board changes native inputs and quotients; it is **not inert**. The parity label R=2 versus R=3 is inert in this comparison. The offset identity concerns counters in an explicitly prepared state; remainders or complete physical states are never added by the engine.

## Native clicks and limits

Each gapped case has exactly `18*L^3` C0 events per update and no C1 or C2 events. The 20 recordings contain 218,880 C0 events altogether. The stationary uniform preparation has no clicks, despite a nonzero quotient, because its complete triples do not change. The R=2 and R=3 runs have identical event addresses, classes, times and quotients while retaining distinct full reversible states.

These C0 events occur throughout a prepared global internal oscillation. They do not demonstrate routing approval, unique path selection or an externally arriving photon. Native click counts do not define mass or a measured time scale here.

The preparation fills the entire periodic cube and its initial amplitude grows exponentially as `3^H`. The exact assertion ends at the registered H; these runs do not test later updates. This is not an eternal oscillator at fixed amplitude, a localized clock with a composable interface, a moving object, a dispersion measurement, or a derivation of physical mass. Establishing any of those properties requires a separately registered family.

## Reproduction and viewing

Capture used 28.57 CPU seconds and 28.79 wall seconds, within the 120 CPU-second, 240 wall-second and 32 MiB budgets. Four regression tests cover the finite oracle boundary, the unchanged-triple click guard, negative Euclidean division and parity retention on zero-vector channels.

From the repository root, select a fresh output directory:

```sh
python -m research.clock_selection.internal_gap_demo --output /tmp/universe24-internal-gap-new
python -m unittest tests.test_clock_selection_internal_gap
```

The [generic Presenter bundle](evidence/internal_gap_v1/experiments.json) contains all five L=3, H=8 preparations. It displays actual native states and uses the existing Presenter without engine or display changes.
