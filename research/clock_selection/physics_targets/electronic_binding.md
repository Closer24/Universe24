# Electronic and chemical binding: physical targets and board requirements

Status: sourced physical requirements and a proposed model test, not a derivation
of electrons, atoms or chemistry from Rule3. Sources checked on 2026-11-08.

## What chemical binding means

Electronic structure is governed primarily by electron–nucleus and
electron–electron electromagnetic interactions, together with quantum dynamics
and the statistics of identical electrons. NIST describes the dominant Coulomb
contributions and the additional direct/exchange and relativistic terms in
atomic structure [1]. Precision molecular calculations also need effects beyond
a purely electrostatic approximation: a primary hydrogen-molecule study
computes a quantum-electrodynamic correction and compares its dissociation
energy with experiment [2]. This does not make a classical exchanged pulse a
complete model of chemical binding.

IUPAC defines covalent bonding through shared electron density between nuclei
and a characteristic internuclear separation [3]. Ionic bonding involves
electrostatic attraction between oppositely charged ions; actual bonds can have
mixed ionic and covalent character [4]. Electron transfer is useful for some
preparations and reactions, but literal repeated transfer of individually
labeled electrons is not a universal definition of a bond. Quantum exchange
concerns permutation symmetry of indistinguishable electrons; it is not simply
a small ball repeatedly handed between two atoms. The antisymmetry/occupation
requirements are additional tests, not consequences of naming board channels
“electrons” [5].

## What detector records would have to show

The following are proposed operational targets. They are not existing Universe24
results. Detector calibration, trial boundaries and no-click outcomes must be
fixed before fitting any model.

| Physical target | Required record-level comparison | Required internal board behavior |
|---|---|---|
| Persistent composite | Repeated calibrated probes identify the same composite over a stated interval | A complete, robust interacting structure, including retained state outside its visible core |
| Formation and dissociation | Preparation-dependent creation of a composite or identifiable separated products, with controls | Ordinary Rule3 interactions change structure; no bond-creation callback or deletion of rejected products |
| Electronic spectra | Several transition frequencies, relative line responses and ionization thresholds under one calibration | Distinct stable internal states and an emergent energy/frequency relation; a single fitted period is insufficient |
| Scattering and charge response | Angular/energy-resolved detector counts and their response to calibrated probes | Mobile identifiable structures and a derived interaction law, not movement of an unconserved activity centroid |
| Occupation and exclusion | State-dependent loading and correlation records under repeated equivalent preparations | Emergent indistinguishability, occupation constraints and antisymmetry-compatible predictions; no external occupancy veto |

NIST's Atomic Spectra Database supplies evaluated levels, transition wavelengths
and probabilities and ionization energies [6]. These are examples of measurable
targets, not numbers that may be inserted into Rule3. Molecular dissociation
spectroscopy provides a separate quantitative benchmark [2]. A physical-energy
assignment and a predictive detector model are still missing from Universe24.

## Simplest current falsifiable step

The existing structure study found prepared recurrent clusters and explicitly
did not demonstrate physical binding, moving constituents joining, or
source-created assembly. Its 128-case confirmation included both passing and
failed radius-one criteria; see [the retained report](../../../docs/STRUCTURE_STUDY.md).

The new [structure protocol](../structure_protocol_v1.json) asks a narrower
question: can an incoming carrier create or reconfigure a complete paired-clock
cluster in a prepared remainder environment? It compares identical preparations
with source and cluster counters present/absent, retains every remainder, and
checks incoming-carrier validity before interpreting a response. Complete-region
recurrence and isolated product templates are specified before execution.

A source-dependent period or state change would establish a computational
interaction. A quiet control followed by a persistent recurrent region would
support signal-created structure within that preparation. Two independently
identified spatially separated products would be a stronger structural result. None
alone establishes electrons, electromagnetic force, Pauli exclusion, molecular
binding energy or chemistry. This experiment starts with a stationary composite,
so attraction/repulsion of two mobile objects is outside its scope.

No additional force, occupancy rule, measurement update or dynamic coupling is
proposed. The scientific gap is to obtain the required effective behavior and
record statistics from unchanged Rule3, with errors and validity domains.

## Sources and evidence scope

1. NIST, [Atomic Spectroscopy: Helium-like Ions; LS Coupling](https://www.nist.gov/pml/atomic-spectroscopy-compendium-basic-ideas-notation-data-and-formulas/atomic-spectroscopy-helium).
   Official reference: Coulomb, direct/exchange and smaller relativistic
   contributions to atomic levels. Retrieved 2026-11-08.
2. Puchalski, Komasa, Czachorowski and Pachucki, [Nonadiabatic QED Correction to
   the Dissociation Energy of the Hydrogen Molecule](https://doi.org/10.1103/PhysRevLett.122.103003),
   Physical Review Letters 122, 103003, published 2019-03-15. Primary paper's
   accessible abstract: QED correction to molecular energy and comparison with
   a parallel dissociation-energy measurement. No claim of reading paywalled text.
3. IUPAC Gold Book, [covalent bond](https://goldbook.iupac.org/terms/view/C01384),
   5th edition, version5.0.0 (2025), DOI10.1351/goldbook.C01384. Official term
   retrieved through indexed definition on 2026-11-08; direct page returned403.
4. IUPAC Gold Book, [ionic bond](https://goldbook.iupac.org/terms/view/IT07058),
   version5.0.0 (2025), DOI10.1351/goldbook.IT07058. Official definition distinguishes
   electrostatic ionic attraction and mixed bond character; retrieved2026-11-08.
5. IUPAC Gold Book, [Pauli exclusion principle](https://goldbook.iupac.org/terms/view/PT07089),
   version5.0.0 (2025), DOI10.1351/goldbook.PT07089. Official term states paired-spin
   orbital occupancy and many-electron permutation antisymmetry. Indexed
   definition retrieved2026-11-08; direct page returned403.
6. NIST, [Atomic Spectra Database](https://www.nist.gov/pml/atomic-spectra-database),
   SRD78, version5.12, data update November2024 as displayed when checked2026-11-08;
   DOI10.18434/T4W30F. Official evaluated-data resource for levels, lines,
   transition probabilities and ionization energies.
