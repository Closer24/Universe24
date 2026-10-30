# Notes 03: provenance of the text's numbers

- Every probe_tg*.err says the interpreter was scratchpad/t24b/.venv, not scratchpad/live/.venv (node-live, the code the
  Boss names). live/src and t24b/src differ in engine/step.py, state.py, mesh.py, contract.py, main.py and the runner.
- edge_lib.UNIVERSE points at t24b/examples/tensor24/universe.json.
- Under live's venv: probe_tg9 (one gear, carry only) reruns IDENTICAL (rerun_tg9_live.txt). probe_tg7 parts A and B
  (one gear) identical; parts C and D (the line of 6, the cube) FAIL: E.board -> live's load.load wants
  universe["chosen"]["key"], absent from t24b's example universe (rerun_tg7_live.err: KeyError 'chosen'). The same
  E.board call feeds tg2, tg3, tg4, tg5 (A-C), tg8: none of the text's board numbers (the cone 1008/1006, the run back
  40 of 40, the books, the 24) were or can be measured on node-live as it stands.
- The engine's structure on the line of 6 (t24b, read through the text's own harness): rows 12, the 00 row r00 = 2;
  rest = 6 GRIP on every row; the clock read lands the 00 count with factor 1 on every row (the 00 row included: W =
  rest + a_00); stretch = kick = drive = 1; the push = GRIP x (a[z+1] + a[z-1] - 2 a[z]) with periodic neighbours along
  z (nb rows 4, 5 are the shifts); GRIP = 15162856759112389000000 (74 bits; den x full_rate^2).
  So a two-row periodic line (light, 00) with push = GRIP x Lap and W = 6 GRIP + a_00 reproduces the engine's board for
  the cone lays exactly; I build it in whole numbers and check it against the text's light period (275 over 5965).
- My one-gear probes use the text's own nearest_root (probe_tg7_squared) for the root, as allowed, and carry for all else.
