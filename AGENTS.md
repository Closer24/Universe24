# Universe24 one-system development contract

The repository has one installed CLI, one built-in signal/clock law and one
Engine. The owner's cleanup instruction removes historical experiments from
the current tree; their source remains in the Git revision linked in README.
Do not restore an experiment menu or present separate laws as one universe.

1. Preserve exactly `ell,r_next=divmod(2*u+r,6); a_next=b; b_next=ell-a`.
2. All outputs read one complete old snapshot. Never clip, project, veto,
   reset or discard state. Rewind all `(a,b,r)`, including nonzero carries.
3. Exactly 48 explicitly supplied TOTAL channels per node: 144 integers,
   including clocks, geometry, matter, apparatus and workspace. No padding,
   extra link state, hidden history or uncounted runtime queue. Report bit growth.
4. The fixed integer polynomial has degree <=3. Each monomial's physical
   support is target plus at most one face edge. Old-a dependencies are acyclic.
5. Preparation completes all inputs before evolution. Only Engine advances
   state. Observers and independent oracles never feed the evolution.
6. Immutable schema-3 bundles bind tensor, full seed, ownership, protocol and
   metadata. Reject corruption, unknown schemas, inexact integers and missing rows.
7. Every supported bundle must satisfy `2O-left-regular-cube/1` exactly. No
   role, research label or missing metadata bypasses the symmetry contract.
8. Mechanical correctness, positive preparation and a conserved logical
   account do not prove Einstein geometry, matter, dark matter, quantum theory
   or a Big Bang. State domains and limitations precisely in docs/PHYSICS.md.
9. The current proved Boolean sector selects one orientation at a time.
   Six passive face views do not establish simultaneous six-face closure.
10. Keep generated evidence in ignored runs/. Update README and current docs
    for model/interface changes; do not commit experiment archives or run outputs.

For structural changes run full unittest discovery and the independent scalar
forward/replay smoke in README. Keep tests for the Engine, algebra, supported
model and I/O contracts. Review the diff and installed package. Green CI never
changes the physical acceptance gate by itself.
