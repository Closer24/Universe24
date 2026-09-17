# Entity audit: catalog, validators, consumers and headless runs

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, headless). Read-only: the audit runs the repository's own
validators, tests, tools and CLI on the shipped
[entity catalog](../../../docs/ENTITY_CATALOG.md) and its consumers and records
what they report. Nothing was changed.

## Files and commands

| file | role |
| --- | --- |
| `dump_catalog.py` | tabulates every catalog record with status, value, uncertainty and sources (`results/catalog_dump.txt`) |
| `cross_checks.py` | cross-file checks: channel balances, antiparticle reciprocity, mass consistency with `particle-contracts`, keV rounding, property coverage (`results/cross_checks.txt`) |
| `run_headless.py` | runs `LABEL=init.json` pairs through `python -m event_universe` and tabulates `run.json` (`results/runs_summary.json`, trimmed of stdout tails and key lists) |
| `inputs/*.json` | the hand-written probe initializations of the `rp-*` runs (all validate as initializations); the three quantum probes `e-quantum`, `e-p-quantum` and `photon-quantum` and their rows in `results/runs_summary.json` were deleted on 2026-09-17 with the quantum layer, leaving seven |
| `results/validate_*.json` | `python -m event_universe.configuration_validation --json` reports |
| `results/pytest_entity_suites.txt` | the entity test suites: 287 passed |
| `results/audit_particle_contracts_summary.json` | `tools/audit_particle_contracts.py --output` with the configuration copies removed; 24 result rows verbatim |

```sh
export PYTHONPATH=src
python examples/research/entity-audit/dump_catalog.py --output artifacts/research/entity-audit/catalog_dump.txt
python examples/research/entity-audit/cross_checks.py --output artifacts/research/entity-audit/cross_checks.txt
python -m event_universe.configuration_validation --json examples/known-entities/catalog.json
python -m event_universe.configuration_validation --json --catalog examples/known-entities/catalog.json examples/known-entities/representation-probes.json
python examples/research/entity-audit/run_headless.py --output artifacts/research/entity-audit \
    discrete-pair=examples/known-entities/discrete-pair.json rp-e-positron=examples/research/entity-audit/inputs/e-positron.json
# examples/catalog-contact/prepare.py --all was part of the recorded audit; it was deleted on 2026-09-17
python tools/audit_particle_contracts.py --output artifacts/research/entity-audit/audit_particle_contracts.json
```

The 56 recorded runs were: the 11 shipped initializations under
`examples/known-entities`, `examples/particle-contracts` and
`examples/quantum/causal_charge.json` (deleted on 2026-09-17); the catalog-contact
demo and one bounded world per catalog particle from `prepare.py --all`
(35 `cc-*` runs, deleted on 2026-09-17); and the ten `rp-*` probes in `inputs/`,
of which the three quantum probes were deleted on 2026-09-17. Re-run at packaging: `dump_catalog.py`
and `cross_checks.py` (outputs byte-identical to the recorded ones) and
`run_headless.py` on two inputs (completed, balanced).

## Results

| item | recorded |
| --- | --- |
| catalog counts | 35 particle entities, 11 field entities, 14 disturbance families, 17 interaction families, 33 representative channels, 27 sources |
| validators | catalog valid; `representation-probes.json` valid (46 profiles, 46 classical, 46 quantum); `property-coupling-probes.json` valid (3 profiles); 15 shipped initializations valid; `entities.json`, `experiment.json` and `physical-units.json` are reported unsupported by the auto-router (they are not initializations, catalogs or profiles), as designed |
| entity test suites | 287 passed in 5.25 s |
| channel balance | all 33 channels balance electric charge, baryon number and lepton sector |
| antiparticle reciprocity, conjugate charge, equal spin | holds for all 35 records |
| mass consistency with `particle-contracts/entities.json` | proton 1,836,153 against the catalog-derived 1,836,152.67 (electron-mass thousandths), neutron 1,838,684 against 1,838,683.66, muon 206,768 against 206,768.28 |
| keV rounding of catalog masses | electron 510.99895069 -> 511 (loss 0.001 keV); proton loss 0.089 keV; neutron 0.42 keV; muon 0.38 keV; tau, quarks and Higgs exact at their published precision |
| property coverage (35 particles) | `magnetic_moment` absent 29, measured 3, reference 3; `lifetime` reference 12, unknown 9, not applicable 6, not supplied 4, measured 3, established 1; `decay_width` absent 29, measured 4, reference 2; `mass` measured 14, reference 12, not applicable 6, theoretical 2, hypothetical 1 |
| status fields | interaction families: `claim_level` `descriptive_only` 17 of 17; particles: `dynamics_status` `not_implemented_as_physical_law` 33, `restricted_classical_proxy_only` 2; `representation_status` `catalog_only` 33, `classical_attributes_available` 2; fields: `not_implemented_as_physical_law` 11 of 11 |
| nucleus, atom, meson | no record: `alpha` exists only in `particle-contracts/entities.json` (mass 7,294,300, charge 2), not in the catalog; no helium-nucleus disturbance family |
| headless runs | 56 of 56 exit 0, status `completed`, `accounting_balanced_at_every_completed_tick` true; `conserved_at_every_completed_tick` true in 35, false in 21 (the catalog-contact demo; the `rp-*` worlds `e-p-n-photon`, `e-positron`, `e-emfield`, `e-p-emfield`; and the 16 `cc-*` worlds of the up-type quarks, the charged leptons, the proton and antiproton and the two W bosons; the down-type quark, neutrino, photon, gluon, Z and Higgs worlds report true) |
| contract audit (`tools/audit_particle_contracts.py`) | 24 cases: mass and charge conserved 24 of 24; maximum decoded momentum error 0 and maximum total-energy error 0 in every case; delayed cycles 0 except `free-electron-delayed` (15, by configuration) |

Every one of the 56 runs is a labeled configuration probe (`model_id` such as
`restricted-classical-conjugate-pair-v1` or
`bounded-rational-elastic-electron-positron-v1`) whose catalog records carry
`dynamics_status: not_implemented_as_physical_law` or
`restricted_classical_proxy_only`; the runs measure that the configured worlds
complete and balance, not that a physical law holds.

## Gaps recorded in the outputs

1. No decay or interaction dynamics: all 17 interaction families are
   `descriptive_only`; lifetimes and widths are catalog values with no rule
   that uses them.
2. No composite matter: no nucleus, atom or meson record.
3. No magnetic-moment representation for 29 of 35 particles (all quarks,
   the muon and tau, the neutrinos, the bosons).
4. Two particles have classical attributes available; 33 are catalog-only.
5. A world with a sourced field can report `conserved = false` while its
   accounting is balanced (the [electron-photon run](../electron-photon-scatter/README.md)
   shows it explicitly: source total -3456, escaped -1952, final -1504), so
   the conservation flag alone does not separate a balanced sourced world
   from a broken one; the accounting flag does.

## Values against the cited tables

The catalog cites PDG 2026 tables (URLs under `pdg.lbl.gov/2026/...`). The
audit transcript reports that ten catalog values differ from the PDG 2024
tables within one to two sigma; the packaged outputs carry the catalog values
with their sources (`catalog_dump.txt`) but no saved comparison table, and the
cited PDG 2026 pages were not fetched, so the catalog values are **unverified
against their cited source** at this revision.

## Limits and what is not established

- Read-only: the audit reports the repository's own checks; it adds no
  validator and proves no physical property.
- The muon g-2 and the neutron lifetime have no representation to measure
  (no magnetic-moment dynamics, no decay law).
- The 56 runs are short (6 to 180 ticks) and exercise configuration and
  accounting, not physics.
