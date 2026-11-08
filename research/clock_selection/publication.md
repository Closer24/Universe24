# Evidence transport and reproduction

The live research tree retains every completed trajectory, failed target,
aborted attempt, corrected observer, exact executed source and independent
certificate. Publication transports that same evidence through a checksum-locked
archive. The scientific protocols and code remain ordinary repository files;
the archive is restricted to `research/clock_selection/evidence/`.

From a fresh checkout:

```sh
python -m pip install -r research/clock_selection/requirements.txt -r research/clock_selection/requirements-solver.txt
python -m research.experiments.materialize_evidence
python -m research.experiments.materialize_evidence --check-only
python -m research.clock_selection.archive materialize
python -m research.clock_selection.archive materialize --check-only
python -m unittest discover -s tests -v
```

The historical archive and this research archive have separate pins and target
namespaces. Neither materializer writes engine, tests, source code or docs.
Existing identical evidence is left unchanged; a differing existing file causes
failure before restoration writes begin. Archive member paths, sizes, hashes,
duplicates and symlinks are checked. Restoration is not forward computation and
does not alter the recorded outcomes.

The baseline symbolic-synthesis checks additionally need the optional pinned
`requirements-solver.txt`. Without it, their skips are explicit. The core engine
keeps an empty dependency list. The coherent-wave critical observer test uses
the pinned `mpmath==1.3.0` research dependency. CI installs both pinned research
packages so the full solver checks execute too. CI restores
both evidence collections and runs regression/reproducibility checks rather
than repeating all large studies. A workflow definition is not proof that a
remote CI run has succeeded.

## Lossless large-certificate representation

Two large independent certificates are already retained as verified gzip
files. The explicit [representation manifest](evidence_transport_representations.json)
records both original JSON paths, their exact byte counts and SHA-256 hashes,
and the corresponding gzip paths/hashes. The archive carries each compressed
member once. Its complete inventory still includes the original JSON paths;
restoration bounded-decompresses and verifies the original bytes before writing
them back at those paths. Reports, links and audit commands therefore continue
to use the original certificates without modification. No JSON field or
scientific record is discarded.

An additional partial wave-certificate copy has unverified origin. It is an
exact prefix of the complete certificate and is retained with its own
[provenance diagnostic](evidence/independent_audit/wave_partial_copy_provenance.json).
It supplies no separate verdict and is not counted as another experiment.

## Frozen publication receipt

The evidence was frozen at2026-11-08 03:37:51UTC. The
[parts manifest](artifacts/evidence_v1.parts/manifest.json) pins259 parts totaling
270,911,247 archive bytes and2,422 original files totaling1,652,601,476 decoded
bytes. Its SHA-256 is
`8cb2881871ffc969ded5c0d0c7cd5408f84d97b99c50b1d189466f3a9a8becb1`.

The final archive inventory and source-tree receipt are recorded after all
authorized studies, independent audits and Presenter packages close. The
materializer rejects an archive whose parts manifest does not match its pinned
SHA-256. Subsequent restoration/test receipts belong under `publication/`,
outside the frozen evidence payload. This avoids changing the archived file
inventory while verifying it.

The expanded local recordings remain available throughout packaging. The
archive builder never deletes them. A fresh checkout verification must restore
only declared repository files and pinned evidence, excluding unrelated local
temporary directories. Scientific success, failed acceptance criteria,
resource overruns, incomplete timing coverage and browser limitations remain
separate fields in the linked reports.
