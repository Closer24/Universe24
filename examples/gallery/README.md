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
`summary.json`, five GIF files and five stills.

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

## Configured lepton reactions: annihilation, muon pair and beta decay

Source: [lepton_reactions.json](lepton_reactions.json), the
`configured-lepton-reactions-v1` candidate. It uses only the generic
[two-record conversion](../../docs/LOCAL_CONVERSIONS.md): each rule replaces
exactly two co-resident records with two others, and the engine checks that
every conserved inventory keeps its pair sum. The inventories are energy and
momentum in units of 0.1 MeV, charge, electron and muon lepton numbers and
baryon number. A unit `direction` field drives transport at one Node per
tick. A held `vacuum_slot` record is the second input of every decay; it is
the configured decay location, not a physical particle. The gallery runs
three scenarios in an open 15 x 15 x 3 world:

| Scenario | Recorded reactions | Recorded numbers |
| --- | --- | --- |
| `annihilation` | tick 5 at (7, 7, 1): e- + e+ -> gamma + gamma | inputs E = 1.3 MeV, p = (+/-1.2, 0, 0); photons E = 1.3 MeV, p = (+/-1.3, 0, 0); totals unchanged |
| `muon_pair` | tick 5: e- + e+ -> mu- + mu+ (E = 110 MeV each, p = (0, +/-30.6, 0)); tick 8 at (7, 10, 1) and (7, 4, 1): mu -> nu_mu + W; tick 9: W -> e + nu_e | the W boson is a held record for exactly one tick; final six leptons carry 220 MeV, lepton numbers 0 and charge 0 |
| `beta_decay` | tick 4 at (7, 7, 1): n -> p + W-; tick 5: W- -> e- + anti-nu_e | n E = 939.6 MeV, p E = 938.2 MeV, e- and anti-nu_e 0.7 MeV each; baryon number 1 and charge 0 throughout |

The muon-pair rule applies when the pair's energy exceeds twice the muon mass
(211.4 MeV) and the two-photon rule otherwise. Muon decay conserves both
lepton numbers through the intermediate W. Rest masses are consistent with the
recorded energies and momenta to the integer unit for the muons (E = 110,
|p| = 30.6, m = 105.66 MeV) and the photons and neutrinos (E = |p|), but the
engine does not enforce a mass shell: the 0.7 MeV beta electron and the
110 MeV incoming electrons are treated as massless in these integer values.
Product directions are configured by the rule, not derived from a matrix
element; the two-body kinematics are the model's own hypothesis.

The recorded summary now includes `charged_lepton_mass_shell`, a passive screen
of resident, held-output and in-flight charged leptons in saved frames. It
requires `E > 0` and reports the beta electron's zero `E^2 - |p|^2` as `failed`,
independently of balanced accounting. A positive shell value is only a necessary condition and is
reported `not_established`, never a validated species mass. Missing samples also
remain `not_established`. No masses, tolerances or corrected physical products
are silently invented. The remaining weak and bound-electron work has explicit
[acceptance requirements and owners](../../docs/NUCLEAR_ELECTRON_ACCEPTANCE.md).

## What the gallery does not show

The backscatter is a configured elastic rule, not a derived interaction. The
reactions are configured conversions with conserved integer inventories, not
a derived weak or electromagnetic interaction: there are no cross sections,
lifetimes, spins or angular distributions, and a decay happens where a vacuum
slot was placed. The contact profile is
the [causal source candidate](../../docs/CAUSAL_QUANTUM_SOURCES.md) with its
documented retarded-source approximation; the two domains share the ordinary
field but no mutual force. `tests/test_particle_gallery.py` checks the derived
inputs and the recorded facts in the fast gate and the rendering only with
`--visualize-runs`.
