# Fourth hostile review: the gate adoption 3b606a606 and stage 5 4b39f234b

Verdict: approve with changes (agent a7024f84da6517f75, returned 19:1x UTC 2026-10-28).

## Required (the Boss)

R1. tests/test_the_tensor24_ring.py does not pin overlap, reverse, axis or add: 14 of 41 source mutants of
ring.py pass (probes/ring_mutants.py, ring_mutants.out). Survivors: overlap crosswise; S's components swapped
or one sign flipped (D_verify's axis_y_sign among them); add as the difference; overlap as <psi, phi>, without
conj, or with the down pair subtracted; reverse times -1, i or -i; axis from pair(down, up).
Fix: three laws, each with its own mutant: the split's share in (rho, S), 2 N<phi, psi> = rho rho' + S . S';
the joint dial, <T phi, psi> = phi_up psi_down - phi_down psi_up; S's orientation as derive/D reads it.
Written and run: probes/test_ring_strengthened.py, 41 of 41 killed (ring_mutants_strengthened.out).

Done in the third and fourth reviews' commit: the test adopted, its comparisons through tests.frame.same
(Python integers only: the minor point 6), 41 of 41 killed again on the adopted file.

## Follow-ups (not blocking)

1. (Sofer) The self-test misses three weakened scans: FLOOR set to HEAD, FLOOR moved later, merge_base
   returning the tree itself (probes/gate_weakened.sh). Fix: pin FLOOR to 526a5666d... in the self-test and
   run merge_base on its scratch repo.
2. (Sofer) floored() floors a merge base on a side line too (probes/gate_floor_sideways.py).
3. (Sofer) The root wall reads import statements only: importlib.import_module and __import__ pass outside
   algebra/, engine/ and readings/ (probes/gate_closed_list.py, gate_dynamic_assign.py).
4. (Sofer, text) a banned phrase in scribe_scan_selftest.py:1245 and a dated phrase in SCRIBE-GATE-1.md:94;
   three all-caps names in a row at SCRIBE-GATE-1.md:42 and 119 (his files stay byte-identical: his to change).
5. (Convention) The plan, derive/D and ring.reverse write T as (-conj z2, conj z1); DAVID-GAUSSIAN-HAND.md's
   (i sigma_y) K is its negative. N, rho and S do not see the sign; det does. R1's joint dial pins the plan's.
6. (Minor) The ring test never checked result types; an int64 array wraps silently.

## What holds

- 3b606a606: the four files byte for byte origin/scribe-5's; check.py its parent plus the patch; the floor
  (CHECK_BASE=origin/main: floored at 526a5666d, 0 refusals); 19 of 19 static plants; the self-test a ratchet,
  720 cases, 6 of 9 weakenings caught; the plan's two lines match SOFER-ARCHITECTURE-1.md; the rate promise
  reproduced (twice the full rate: k reaches 2, the rewind not exact).
- 4b39f234b: ring.py exact against a model on the real parts in 20,000 runs up to 2**400; conventions match
  derive/D, D_verify and the plan; each of the seven laws fails on its own mutant; 27 of 41 source mutants
  killed; fast checks pass; text rules hold; fullcheck_s5.log 200 passed.
