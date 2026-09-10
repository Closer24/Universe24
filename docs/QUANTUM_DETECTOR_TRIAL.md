# Detector integration prototype

GitHub base: e74f2fdf390b5dc8036b707eefcfc53bc8a82c17.
Exact cached src tree verified: 18253dfaca7208b9f5f8d4e4f4bf7cc48fd579d7.
Development branch: `feat/quantum-detector-trial` in `Closer24/Universe24`.
The connector verifies the base and publishes this focused change; it does not
replace main from an archive. Merge requires successful CI and explicit approval.
Previous quantum sidecar was absent from main; only its quantum/integration
modules and focused tests are ported. No existing physical source is replaced.

Run python -m pytest tests/test_quantum_detector_trial.py -q.
Every actual Engine run uses the existing pytest HTML visualization path.
Full gate: python tools/check.py. Missing dependencies must not be marked PASS.

This is a prescribed finite 3D interferometer circuit and a terminal single-
excitation detector mock, not spontaneous detector physics. The main test harness
stores a single physical-side record but Engine has no detector commit API.
No coupled quantum field dynamics, general post-measurement evolution, energy or
momentum proof, no-signalling or Bell test. Fixed graph nodes and bounded ints
remain mandatory; total host DAG work is not constant.
