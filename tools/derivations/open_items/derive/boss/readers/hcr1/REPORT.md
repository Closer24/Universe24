# The first hostile code reader on origin/main..f72067cdf (node-live), 2026-10-30

Filed by the Boss from the reader's hand-back.

HOSTILE CODE READING: origin/main 2bcf315b6 .. f72067cdf (node-live), at the head

Summary: one BLOCKING finding, and the known well-world window is confirmed with the cause you gave. The run back is broken under term 5's push in the books' form. The fault is in writer A's act, not only in the plan B2b will lay, so B2b as planned will not close the window. There are thirteen MINOR findings.

What I ran:
- The gate: 0 refusals, 5 notes (INDICATOR at load.py:110 and :112; PIN at test_the_tensor24_load.py:76, :77, :80).
- The full check: exit 0, 27 passed.
- tensor24: 10 rounds, exact 1. tensor24-live: 100 rounds, exact 1. tensor24-well: exit 1 at round 2, no record written.
- Every probe is whole numbers. They are in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hcr1/probes/ and the numbers are in /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hcr1/RESULTS.txt.
- The worktree is removed.

=== BLOCKING ===

B1. The run back is not exact under the metric's push in the books' form. Writer A.
- Where: src/tensor24/engine/step.py:51-64 (stress) and :128-129 (act); the docstrings at :52 and :170; tests/test_the_tensor24_engine.py:145-158, :240-255, :258-267 and :270-299.
- Law broken: every act undone bit for bit. Claims broken: stress says "the mirror swaps and negates the two momenta"; untick says it is "tick's inverse wherever ... every tooth stands within its edge's dial, the clock standing or moving".
- Mechanism:
  - stress reads M_out = M_in + 4 (s F + K1). K1 is the drive's quotient on J1 alone (`first, _ = drive(j1, ...)`, with the remainder dropped).
  - The round's true outgoing momentum is N = M_in + 4 (s F + K), with K taken from J1 + J5.
  - The backward round reads its sigma_in from -N - 1, not from -M_out - 1.
  - The books' form pushes the ii rows and also reads their momenta for the 00 slot. Where the push lands on a row, K differs from K1, so the backward momenta are not the forward ones mirrored, J5 changes and the round does not return.
  - The old form read matter momenta alone, which is why term5_edge ran back.
- Evidence on the engine test's own pushed() layout, from the 24 test's drawn states:
  - One-round run back exact at 0 of 6 states at T_d 7, 2 and 1. With the push plan emptied: 6 of 6.
  - At small counts in [-3, 4): off at 768 of 875 gears. The backward momenta are off at 500 gears, and sigma(M_out at K1) differs from sigma(N at K) at 500.
- Evidence on the well world, with the plan laid as PLAN B2b states it (k0 = 12; minus the stretches squared on the ii slots; k0 sigma_in sigma_out of every row but the 00 on the 00 slot; T_d 2 on the 00 and ii rows; push 1):
  - One-round run back exact at 0 of 19 rounds.
  - At round 1, sigma(M_out) differs from sigma(N) at 2520 gears, all on rows 2, 6, 7 and 8 (the 00 and ii rows). The backward momenta are off at the same 2520. The run back misses at 710 of 8424 gears (814 with T_d 1 on every row).
- The tests do not reach it. pushed() is used only for stress at push 0, where M_out = M_in, and for the forward 24. It is never run back.
- Fix:
  - Make the momenta the push reads the round's own. The loader lays the push as two plans: the terms on the stretches, and the terms on the momenta.
  - The act carries every row at J1 plus the stretch terms and reads sigma_out from that N. It then adds the momentum terms, which land on the 00 row alone, a row whose momentum no term reads. No mask is needed in the act.
  - Add the run back under pushed() to the engine test, with the K1 read as its no.
  - A probe of this direction: pushed() 6 of 6 at T_d 7 and 1; the well world under the books' form 12 of 12 rounds.
  - The deriver's "run back 12 of 12" (probe_f) should be rerun on the act as built.

=== THE KNOWN WINDOW: confirmed, cause as stated (writer B, B2b) ===

- Where: src/tensor24/runner/plans.py:126-187. pushing still lays the old planes. At :132-135, `unit = (d + senses^2) rows` is plane 7*rows. On A1b's planes that is row 0's sigma_out. The "sigma_in" leg reads the -z stretch and the "sigma_out" leg reads sigma_in.
- The run tool at the head: "round 2: row 0, site 0: ... the teeth 6334123 and -40268301", 5148 departures. Round 1's one-round run back is already off (b differs at 7072 entries).
- With step.stress swapped back to ac3085db4's (the plan contracted on the readings, then sigma_in, sigma_out and the unit) at this head: 128 rounds, every promise held, 128 of 128 one-round run backs exact, rewound bit for bit.
- examples/README.md's well section still says "the run back returns the lay bit for bit". That is false at the head.
- Per B1, B2b alone will not restore the run back.

=== MINOR ===

M1. The square train's passing form is not kept by the 24. Writer B.
- Where: plans.py:12-38. passing applies pairs_of to every train, the square included. pairs_of takes the square's slot-basis rows by kind blocks: xx is treated as A1, and (yy, zz) as E with (2, -1; -1, 2).
- The form is kept by 8 of 24 turns. The (T1, T2) train's form is kept by 24 of 24.
- It is latent: X_square is 0 under the notch, which is isotropic, so no click shows it. No test reaches it.
- Fix: give the square the factor 0 by its flag, as pushing does, or lay its form from the square's own representation.

M2. A1 struck the planned no on a false identity. Writer A.
- Where: d6ec46ff0's message, "-n + (d - 1 - r') = -q d + (d - 1 - r)".
- The identity holds in 288 of 1148 small cases. The kept-tooth law holds in 1148 of 1148.
- On pair(), a mirror that flips the click tooth returns the teeth in 2 of 40 rounds; the kept tooth returns 40 of 40.
- So FRAMES 4's no ("the tooth flipped breaks the run back") stands, and no test now holds it. The existing yes still catches the flipping mutant.
- Fix: restore the one-line no and correct the note.

M3. The run test's pair world is a transient. Writer B.
- Where: tests/test_the_tensor24_run.py:275-297.
- q is (0, 1, -1) every round to round 56. The giver's 32^2 plus the gliding taker's count^2 passes Gamma div 4 = 2500 at round 39.
- At round 57 the held hand bends (|k|^2 = 2) and q is (-177, 1601, 4986): the books are off by 6410 and the held hand clicks.
- Over 300 rounds the sum of q is not 0 at 149 of 294 places.
- The test's 30 rounds sit inside this window, and its comment says "within the room".
- Fix: lay the pair within the room for ten beats, with the taker at rest, or state the window.

M4. Pins spelt as sums, under the PIN note. Writers B and C.
- Where: run test :293-296 (`(1 + 1) * ticks`, `== 1 + 1`, `[1, 1 + 1]`, which are verdicts on the run's output); decoder test :545 and :560-565.
- The habit stands at main, but the PIN count per file "may not rise".
- Fix: let the notes show, or read the 2 from the structure.

M5. "mesh" is required and documented but inert. Writer B.
- Where: files.py:70-78. Nothing reads it: load.py:176-181; laid_out lays no Mesh plan.
- A world with mesh above 0 runs as if mesh were 0, with no word.
- Fix: refuse it by name until B5, or drop the key until then.

M6. The key's oddness is claimed but not enforced. Writer B.
- Where: plans.py:36 says "CHOSEN odd"; files.py:72 has key ONE.
- With an even key on pair(): the books miss in 8 of 400 rounds at 2^17 and 90 of 400 at 2^12, and k_L + k_M is off key - 1 in 400 of 400. With odd keys, 0 and 0.
- Fix: refuse an even key by name.

M7. Docstrings, comments and messages that claim what the code does not do.
- step.py:4, "gamma = 1 by the slots' own units": k0 = 1 at the head (load.py:220-224), and MAP.md strikes gamma = 1 from every status line. Writer A.
- step.py:52, "a hand at rest sources nothing": the engine test's own resting tent pushes zz. Writer A.
- state.py:3 and :74 still describe the old push readings. Writer A.
- plans.py:127, "so gamma = 1". Writer B.
- The README states the window as SUM grip / W <= 1; run.window checks against senses W. Writer B.
- run.py:46 and :56 print a dial below 0 as "[--33934178, -33934178)", naming teeth below 1 as a tooth off its dial. Writer B.

M8. tests_shape ROOM raised against origin/main. Writers A and B.
- Raised: frame 230 to 237, engine 202 to 299, load 113 to 140, run 285 to 297. Lowered: decoder 600 to 572.
- ARCHITECTURE section 4 forbids raising these with a code change. It is named under the Boss's ceilings, so it is not hidden, but it needs the writer's or Sofer's word before main.

M9. Code the document does not name, and plan drift.
- scribe_law_check --arch reports 1 departure: runner/plans.py.
- NOT_CLOSED 25 and PLAN A2 say frame.turned would carry the twisted action. A2 put the twist in the engine test's own twisted(), and frame.turned still permutes sites only.

M10. The decoder accepts click lines the schema rules out. Writer C.
- Where: decoder/records.py.
- Read without refusal: a train with no header card, q 0, the same (round, site, train) twice, a tooth past the key, a tooth below 0.
- Fix: refuse each by name.

M11. MINOR = len(ADDED) grew to 3 (schema.py:25). Writer C.
- ARCHITECTURE section 6 tied reading this count from the schema to schema 1.3.
- No frame names it.

M12. J5 enters no train's X, since the passing reads only layout.plan. Writer A's docstring and the architect's FRAMES.md.
- The matter-metric exchange is booked by no click.
- FRAMES 5 names only the Mesh plan.

=== SOUND ===

- Law scans:
  - No literal beyond 0 or 1, and no 1 + 1, in src or in tools/tensor24_*.py (checked on the syntax tree).
  - No //, %, divmod, power or shift outside carry.py.
  - No if, loop, mask, comparison or clamp in engine/.
  - ASCII only. docs/, .github, uv.lock and the gate files are untouched. Imports stay within section 5.
- Locality: by reading, and by probe with the push and a click, 14 of 14 sites read nothing past their six Meshes.
- The 24:
  - A2's test: 24 of 24 under the push with k0 12, T_d 7 and the clock moving; 3 of 24 without the flip.
  - My probe on B2's frame through the real loader (light, square, held hand, two tied hands; hold 1, tie 1200): 24 of 24, clicks included.
- The run back without the push holds:
  - The engine test, the pair world, tensor24 and live are exact.
  - B2's frame rewinds bit for bit over 6 rounds, even in a runaway outside the room.
- The click tooth kept under the mirror is correct.
- B1: the two-square refusal by name; pairs_of checked against a naive model of the tables.
- B2: the flags by exact character tests (the INDICATOR notes are the square flag's form, not a bound); the held rows' grips are 0; the plans are generic.
- B4: the 1.3 header and the click lines in the schema's order.
- C1 and C2: the schema; clicks.py counts with no verdict and no numbers.
- C3: whole numbers, and it measures the act.
- The frames are named in FRAMES.md and NOT_CLOSED.md, apart from M5, M6, M12 and B1's price.
