# Named-particle gallery

Two experiments with catalog particle names, rendered as three-dimensional
animations from recorded runs of the canonical runner. The harness derives
both inputs from checked-in files, runs them, reads the outputs back and draws
one frame per recorded tick. Nothing is interpolated and no trajectory is
invented. The animations are outputs and stay outside source commits.

```sh
pip install -e ".[render]"
PYTHONPATH=src python examples/gallery/particle_gallery.py --output artifacts/particle-gallery
```

`--no-render` runs and summarizes without matplotlib. The output directory
receives each derived initialization file, each run directory,
`summary.json`, two GIF files and two stills.

## Electron and positron: bounded rational elastic contact

Source: [electron-positron.json](../particle-contracts/electron-positron.json),
the `bounded-rational-elastic-electron-positron-v1` contract from
[rational particle candidates](../../docs/RATIONAL_PARTICLES.md). The gallery
changes only the seeds, to x = 5 and x = 11 on the line y = z = 8, and the run
length, to 96 ticks, so that the approach is recorded. Both bodies carry
`m = 1000`, `|p| = 1000` and unit charges of opposite sign, and move one Node
per twelve ticks.

Recorded: receptions at ticks 12, 24, 36, ..., 96. At tick 36 both bodies share
Node (8, 8, 8); the configured elastic backscatter exchanges their momenta,
`(1000, 0, 0)` and `(-1000, 0, 0)`, and they recede to x = 3 and x = 13 by tick
96. Total momentum is zero, total charge zero and total mass 2000 at every
completed tick. The frame shows each body's name, symbol, momentum, mass and
charge, and the momentum arrows; the contact frame is held.

## Catalog electron and positron in the causal contact profile

Source: [catalog-contact/prepare.py](../catalog-contact/prepare.py) with
`--entity electron --entity positron`, which reuses the
[causal charge template](../quantum/causal_charge.json) and the shared
[entity catalog](../known-entities/catalog.json). Each occurrence has its own
three-Node domain: the electron at y = 1 and the positron at y = 3, sources at
x = 1 and capture probes at x = 3, in an open 7 x 5 x 3 world for 16 ticks.
Charges are catalog values in thirds of the elementary charge and masses are
511 keV/c2; the frame labels show them.

Recorded: at tick 0 each source meets its held probe and becomes a unit wave
whose Node emits `electric_signal` with the catalog charge, so the two field
halos have opposite signs. At tick 3 the far probe of each domain decides with
weights `[9, 16]`, the fixed ticket 9 selects capture, and one
`localized_charge` record appears at x = 3 in each domain. The recorded field
per Node is drawn as a glow, blue for negative and red for positive, with the
one-half decay per hop of the outward transport. Final totals are charge 0 and
mass 1022 keV/c2.

## What the gallery does not show

The backscatter is a configured elastic rule, not a derived interaction, and
no annihilation, pair creation or radiation is modeled. The contact profile is
the [causal source candidate](../../docs/CAUSAL_QUANTUM_SOURCES.md) with its
documented retarded-source approximation; the two domains share the ordinary
field but no mutual force. `tests/test_particle_gallery.py` checks the derived
inputs and the recorded facts in the fast gate and the rendering only with
`--visualize-runs`.
