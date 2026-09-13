# Known entity configurations

The physical inventory is [catalog.json](catalog.json). It describes fields,
particles and antiparticles with separate representation, dynamics and emergence
status; compile selected profiles with `python -m event_universe.entities` as
described in [the executable catalog](../../docs/ENTITY_CATALOG.md). The
[conversion probe](conversion.json) exercises generic two-record type replacement.
The catalog itself is not a raw initialization file. See
[physical entities and discrete support](../../docs/PHYSICAL_ENTITIES.md) for
the sourced audit, the elementary-rule restriction and the two new executable
probes: [discrete-pair.json](discrete-pair.json) and
[field-channel.json](field-channel.json). The original five-run wrapper below
does not include these probes. The existing collision formula is a reference
benchmark, not evidence of emergence from elementary vector operations.

From a repository checkout with the project Python environment already available:

```powershell
./examples/known-entities/run_reference_checks.ps1 -Python python
```

Pass the existing environment's Python executable with `-Python` when needed.
On other shells, set `PYTHONPATH=src` and run
`python -B examples/known-entities/run_reference_checks.py` from the repository root.
No build, installation, simulator edits, or visualization is performed.
All entity definitions and laws are in the five JSON inputs. The collision input
is [the canonical workspace example](../04-unequal-mass-collision.json), also used
by this runner; no local duplicate is maintained. The normal-budget three-mass
case reuses [three_mass_finite.json](../three_mass_finite.json) with an explicit
120-tick override through the existing runner. The original input remains 100
ticks and is preserved byte-for-byte in output; the actual completed count is
recorded separately. Low-budget and boundary controls retain their distinct
physical configurations. The diagnostic
runner reads them without overwriting them. Its numerical acceptance checks
are specific to these configurations; update expectations when editing a model.

Results go to a fresh `artifacts/known-entities-*` directory. Generated runs
and summary files are registered for the standard 24-hour artifact retention;
idle removal requires the existing retention watcher. See
[retention](../../docs/RETENTION.md). Original configurations remain in Git.

Historical local validation on 2026-09-12 using Python 3.14.7 (source hash below):

| Configuration | Ticks | Simulator seconds | Observation |
|---|---:|---:|---|
| collision | 360 | 0.093 | Mass 5 and momentum (5,0,0) preserved; final momenta (-4,0,0), (9,0,0), expected final positions, unchanged kinetic diagnostic 35/2 in raw configured units. |
| three-masses | 120 | 0.915 | Three carriers, mass 10, one nonzero field exchange. Finite computation emission 2160 fully dissipated, background retained. |
| three-masses-low-budget | 120 | 0.915 | 19 delayed cycles, 29 moves versus 36 at normal budget. No nonzero field exchange in this timing. |
| boundary-periodic | 14 | 0.012 | Six carriers wrap correctly across all positive/negative X/Y/Z faces, including repeated wraps. |
| boundary-open | 3 | 0.002 | Six carriers leave; escaped mass 6 recorded, no records remain. |

The standard runner checked quantity accounting at every tick, including spatial sources, decay, and escape. Additional acceptance checks verify exact collision results, movement timing, delay arithmetic, all six boundary positions, original input preservation, and unchanged simulator source fingerprint.

The decaying momentum field does not preserve physical momentum indefinitely: normal-budget final momentum (-1,7,0) plus recorded dissipation (-1,3,0) equals initial (-2,10,0). This is balanced accounting with dissipation, not a claim of conserved physical momentum. Those figures were recorded under the earlier dissipative default; with the current localizing default the same removed fractions are reported as `localized_totals` deposits and remain inside `final_totals`. The computation background is 1 per node, so its aggregate baseline is 274625; excess field returned to zero.

An initial diagnostic incorrectly required a nonzero field exchange in both budget settings. The low-budget run completed successfully but that assertion failed. The corrected checks require a nonzero exchange in the normal-budget case and observed computation delays in the low-budget case; they report both reaction counts without assuming identical trajectories.

These are configured classical examples, not validation of real particle physics. Simulator source SHA-256: cf684492a86605a68c29aba0a169a6e992478b2f7f7b3d70804e8fce7f2d4f4a.
