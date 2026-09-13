# Many local quantum captures

This configuration runs six independent charged disturbances alongside eighteen
massive target disturbances and six massless preparation partners in one periodic
11 x 11 x 8 world. It uses all thirty mode addresses supported by
`causal-contact-fields-v1`. The simulator source and physical laws are unchanged.
The trials test delocalization followed by one localized capture per disturbance;
they do not demonstrate repeated hopping between targets or mutually interacting
quantum particles.

## Input and expected observation

[many_contacts.json](many_contacts.json) is the complete initialization file.
Every domain has a source S, an adjacent transit Node H and three targets A/B/C
neighboring H. Each target is two physical Links from S. The four configured
phases are S-to-H SWAP, a 3:4 H/A mixer, a 3:4 H/B mixer and H-to-C SWAP.
Twelve empty phases prevent a second gate cycle within the 24-tick recording.

The independent capture probabilities are A = 16/25, B = 144/625 and C = 81/625.
Local capture event ticks are 3, 5 and 7, respectively. Ordinary source envelopes
and field propagation retain their causal delays. Field attenuation explicitly
uses `residue: "dissipate"`; injection and loss must balance, while charge -6
and mass 24 stay constant. Raw field stock is not a conserved closed amount.

The first seed, 20260913, was fixed before inspecting the outcomes. Repetitions
use consecutive seeds, without selecting a run for a preferred result. The
representative runs 24 ticks; subsequent independent trials run 12 ticks, through
capture and causal cancellation. Statistical repetitions are separate worlds,
not 1,200 particles simultaneously inside one world.

## Reproduce

Use the existing project Python environment, with `PYTHONPATH=src`; no simulator
build is required. Supply a new output directory.

```sh
python -m event_universe.configuration_validation examples/quantum/many_contacts.json
python examples/quantum/many_contacts.py --output artifacts/many-contacts-result --trials 200 --visualize
python examples/quantum/many_contacts_view.py artifacts/many-contacts-result
```

Omit `--visualize` and the last command for headless execution. The primary runner
records the representative `run.json`, causal events and optional `run.html`.
The experiment additionally records every trial's seed, actual capture events,
inventory and field accounting in `trials.jsonl`, plus the combined `summary.json`.
Its read-only representative trace is checked against the primary runner's
capture records and final state. The optional renderer reads these saved records;
it never advances a world or interpolates a particle trajectory.

The six animation panels use actual XYZ coordinates in an oblique projection.
Gray marks configured Nodes; blue rings show local source-envelope weights;
orange marks the combined ordinary field; purple stars show actual localized
outputs. Blue weights are the retarded local source approximation, not the
globally conditioned quantum probability after measurement. Frame 4 first shows
the events committed at tick 3; frames are completed world snapshots. The GIF
stops at its last frame. Generated outputs are enrolled in 24-hour retention;
these source inputs and scripts remain reproducible in Git.

## Observed result, 2026-09-13

On source SHA-256
`1ac603cc9fb6bc34967dcd1b9c4dc6c6e08680229e6e6ed7527f8d4dbf432aaa`,
input SHA-256
`9871bfb99fae8eec96cd85655ee7cf7f13861bac9af5e9d57e57826419cb1512`,
all 200 trials completed: 1,200 captures, exactly one per domain per trial.
Total experiment time including the primary recorded run was 124.21 seconds;
the primary 24-tick run took 1.076 seconds. Python 3.14.7 was used.

| Target | Captures | Observed | Configured expectation |
| --- | ---: | ---: | ---: |
| A | 756 | 63.00% | 64.00% |
| B | 283 | 23.58% | 23.04% |
| C | 161 | 13.42% | 12.96% |

Every trial preserved charge -6 and mass 24 at every tick; every field accounting
check passed. All final envelopes retired, final field stock was zero and escape
was zero. The representative field stays zero from frame 11 through frame 24.
Its injected -864 units are all accounted for as dissipation. The primary runner's
raw-stock conservation flag is therefore false, and its source/loss accounting
flag is true. These values are compatible with the selected finite field law.

The representative has three A captures at event tick 3, two B captures at tick 5
and one C capture at tick 7. Six localized outputs remain at frame 24 alongside
the original twenty-four probe records. No extra carrier copies or later hops
appear. Independent review checked all trial records against the summary and
the actual representative frames. The visual inspection covers initial state,
ordinary field, first capture, final state and decoded GIF frames.

Repeated hopping requires a supported next local preparation after capture,
including a new origin lifecycle and physical encounter rule. Current domains
are disjoint and one-shot, and capture outputs are held. This experiment reports
that limitation; it does not bypass it by relabeling a chain of independent runs.
The existing configuration Skill was corrected to route spatial-field quantum
experiments to their explicit supported profiles. Other orchestration and
execution Skills already cover this workflow and required no changes.

Affected validation from base `2fb5b57`: 209 tests passed and two optional
visualization tests skipped in 32.63 seconds. Ruff and formatting checks passed
for all five affected Python files. The experiment animation was separately
rendered and visually inspected. No simulator build or full-suite run was used.
