# Working on this simulator

1. Read `POSTULATES_HE.md` and `SIMULATOR_DEFINITIONS.md` before changing a
   physical module. A postulate change must update both documents and its tests.
2. Keep scheduling, generic field/dynamics calculations, model choices and output
   code in their documented modules. Reuse the generic arithmetic; choose and
   connect it in `models/current_field.py` rather than copying it into a model.
3. Use named immutable physical records, typed public interfaces and short local
   functions. Do not add growing per-source structures or render imports to core.
4. For a defect, add a focused test of the failed behavior before the correction.
   Tests should assert a contract or observed result, not mirror implementation.
5. For refactors, retain exact differential equivalence to the frozen baseline.
   A change to a physical hypothesis needs a separate model identity and review;
   do not change baseline expectations merely to make a test pass.
6. Run `python tools/check.py`. Inspect the HTML for affected run scenarios.
   Test reusable calculations in `test_scalar_field.py` and `test_turning.py`,
   current choices in `test_current_field.py`, and public component replacement
   in `test_field_composition.py`.
   Specify input, expected output and a boundary case for each calculation;
   maintain `docs/TEST_EXPECTATIONS_HE.md`. Movement, lattice geometry, field
   policies and diagnostic projections have their own focused test modules.
   Assembly modules must contain no independent arithmetic; the architecture
   gate also checks absolute and relative dependencies.
7. Commit code and documentation together. Keep generated outputs outside source
   commits; attach them to reviews or saved experiment packages.

Formatting is managed by Ruff. The development dependencies are declared in
`pyproject.toml`; exact tool versions used for the delivered validation are
recorded in `docs/VALIDATION.md`. No coverage percentage substitutes for tests of
integer bounds, causality, occupancy, momentum and known historical regressions.
