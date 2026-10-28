# Sofer's gate: the owner's rules as a script that refuses a push

The owner's direct words of 2026-10-28, 05:0x UTC, to Sofer (in Hebrew, verbatim in translation): "From the twins' state! Sync. Everything you found here that cannot be at all, also for David: if he tries to bring in circles, or numbers in the code, or cosines or formulas, it is better that it shouts at him right there, that he need not go through you. Let your laws be simply in scripts, that cannot push at all things that break our lawfulness. Do you understand what I say? But do it logical and smart."

This file says what the gate does, how it decides, where it runs, what it cannot do and what the Boss adopts. The script is tools/derivations/open_items/scribe_scan.py (the law's **No circularity that makes a phenomenon happen** names it); it needs nothing but the standard library and Python 3.14 (venv314/bin/python; an older interpreter runs it again under the repository's own).

## What it refuses

A rule is a count of hits per file under src: every package there, the current engine's (src/event_universe) and any new engine written beside it, so that a new file starts at 0 hits and a hit in it is refused; the rule PIN alone reads the tests. A refusal (tier BLOCK) stops the push; a note (tier WARN) is printed and the push goes.

| rule | tier | what a hit is | the law it keeps |
| --- | --- | --- | --- |
| NUMBER | BLOCK | a number beyond 0 and 1 | No number in the code |
| FLOAT | BLOCK | a float literal, a true division, round(), pow(), float, a numpy float function (np.floor, ceil, trunc, rint, around, round and fix among them) | No float anywhere in the system |
| IMPORT | BLOCK | math, cmath, random, fractions, decimal, statistics, scipy, sympy, mpmath | No float anywhere in the system |
| DTYPE | BLOCK | a numpy constructor with no dtype (its default is a float) | No float anywhere in the system |
| CIRCLE | BLOCK | a cosine, sine, tangent, pi or another circular function, by name or through numpy | No circularity that makes a phenomenon happen |
| ROOT | BLOCK | a call of an integer root (largest_below, sine_rim, isqrt, sqrt): the integer sine is a circle by search | the same |
| WORD | BLOCK | a circular word in a name: cosine, sine, angle, theta, circle, quaternion, Tsirelson, Lorentz ... | the same |
| TABLE | BLOCK | a typed table of three or more integers (a quarter turn, a singlet, a neighbour list) | No number in the code (a world's data stands in its files) |
| MIX | BLOCK | a tuple of three or more bilinear sums: a rotation or a hypercomplex product by a setting outside Rule3 | the same |
| STATE | BLOCK | a module-level container, a `global`, an `id()` key: state outside a Node-clock | Locality is never broken |
| LOGREAD | BLOCK | an act reads the great clock's log (the readers of a finished chart may) | Locality is never broken |
| TEXT | WARN | a circular word in a string, a docstring or a comment | read it: a rotation or a closed form may be described there |
| MEMO | WARN | a module-level cache (functools.cache): state beyond the Node-clock, allowed only for a pure function of integers | Locality is never broken |
| LOOP | BLOCK | a for, a while or a comprehension in an engine module (the readers may loop): the machine is one tensor operation | the owner's words of 2026-10-28, 06:5x and 09:0x: no loop that makes a formula; the count per file and kind may not rise |
| OPERATION | BLOCK | a power, a shift, an exclusive or, or a floor division or a remainder outside the carry's home (core/acts.py, core/rule3.py), and the same under a function's name (divmod, np.mod, np.remainder, np.floor_divide, np.left_shift, np.right_shift, np.bitwise_xor, operator.xor and the like) | the owner's word of 2026-10-28, 09:0x: three operations only, multiplication, addition and Rule3 |
| REFUSE | BLOCK | a raise in an engine module: a refusal by name; the count per file may not rise | the owner's word of 2026-10-28, 09:0x: no declarations (the exclusion's refusals were such) |
| CLAMP | BLOCK | min, max, abs, clip, where, sign, select, piecewise, choose, heaviside or copysign (a call) in an engine module (the readers may use them): a bound or a branch written as a clamp | the owner's word of 2026-10-28, 08:0x, through David: the step does multiplication, addition and Rule3 alone; approved for Sofer's check |
| COMPARE | WARN | an ordering comparison (less, at most, greater, at least) in an engine module: a threshold read by order and not as the quotient of a carry | the same word; the count may not rise |
| PIN | WARN | in a test (the tests folder), an assert that holds a number beyond 0 and 1: a pinned value is a verdict the code wrote, and not a law the test derives; the count per file may not rise | the owner's word of 2026-10-28, 08:5x: no result fitted to what is wanted, as the exclusion is today |

`scribe_scan.py --rules` prints the same table. The words are the ones the owner named; the script cannot read a formula that spells no such word (a closed form with plain names), so Sofer still reads every push whole against the five rules, and the gate only takes from that reading what a script can see.

## How it decides: a ratchet, and no list to keep

A push may not raise the count of any hit above the same file's at its merge base (the revision named by CHECK_BASE, else origin/engine-5.0-test): what stands at the base stands, and the code departs from the law at the register's R5 until the Boss removes it. A hit is keyed by its rule, its file and its detail (the number, the name, the container), never by its line, so a moved or reformatted line is no new hit; a module git reads as renamed carries its counts; a new file has none. Replacing one hit by another of a different name is a new hit. A hit leaves the list by being removed and enters it only by the owner's word: tools/derivations/open_items/scribe_scan_allowed.json holds the entries the owner allowed (rule, file, detail, count, his word, the ledger's row), is written by Sofer alone and is read from origin/scribe-5, so that a push cannot allow itself by editing its own copy. It stands empty.

A patch (`--patch FILE --base REV`) and a push also print one line of counts by rule from the base to the push (`counts from the base: LOOP 372 to 360, CLAMP 76 to 70`), so that the plan's end check, every count falling or equal and 0 at the end, is read at each push.

`scribe_scan_baseline.json` is the other list: the hits that stand now (932 at the engine head 526a5666d: 647 refusing, of which 372 loops, 76 clamps, 75 circular names, 31 raises, 27 roots, 24 numbers, 22 state, 13 operations, 3 tables, 3 log reads and 1 float, and 285 notes: 126 pinned numbers in the tests' asserts, 102 ordering comparisons, 51 circular words in text and 6 caches), for Sofer's audit of the whole tree (`scribe_scan.py --baseline`), and it can only shrink.

## Where it runs

1. **At the push, by git.** `python tools/derivations/open_items/scribe_scan.py --install` writes .git/hooks/pre-push in the clone (a hook of another make is never overwritten); every `git push` then reads the commits it sends and is refused with the hits named, by file and line, and the law each breaks. `git push --no-verify` goes round it, which is a breach to report.
2. **At the push, by Claude Code.** tools/derivations/open_items/scribe_gate_claude_settings.json is the project settings file for .claude/settings.json: a PreToolUse hook on Bash that reads every command holding `git push` and refuses it (exit 2, the message shown to the session) before it runs, and a SessionStart hook that installs the git hook above in every new session's clone. It shouts at the session at the moment it types the push, which is the owner's "right there".
3. **At the merge, by the Boss's checks.** tools/derivations/open_items/scribe_gate_check_py.patch adds one line to the RATCHETS of tools/check.py, so that `tools/check.py` (every selection and `--full`) and the CI's lint shard run the gate against CHECK_BASE like the four ratchets before it.

The three are the Boss's to adopt (Sofer writes no tools/*.py and no .claude/ file): `git apply tools/derivations/open_items/scribe_gate_check_py.patch`, and copy scribe_gate_claude_settings.json to .claude/settings.json. A refusal at the server, so that even a push that goes round the hooks cannot land, is one setting of the repository (a required status check on engine-5.0-test), the owner's.

## Tested

- The engine head 42d5448b7 against its merge base: no refusal, no note; the Boss's push of 04:39 against 97e5b3fd6: no refusal and one note (the module-level cache draw.kept_mid).
- David's DAVID-THE-BELL-LOCAL.patch on 97e5b3fd6: ten refusals (the module-level containers _BELL and BELL_DETECTORS, two id() keys, four reads of the log, the typed twins (1, 0, 1, 0), the four bilinear sums of bell_turn) and three notes (quaternion and Born in docstrings).
- Replayed over the last 40 pushes to engine-5.0-test that touched src (each against its parent): 31 pass (five of them with a note) and 9 are refused, eight with one to a dozen hits each, every one a real hit under today's rules (an id() key at tick.py:293 in 97e5b3fd6 and at tick.py:252 in ce40d8d63, a log read in undo, a number 4 in merger_end, a number 2 in core/acts.py, sine_rim in phenomena.py, the angles of the setting), and the restructure of 67a7633d5 (modules and functions moved) is refused with 40 hits. The Boss's three pushes of 05:04, 05:12 and 05:21 (the shears, rows 76 and 56, the click's rename) pass clean, the rename carried.
- Counting corrected (2026-10-28, 09:0x): the earlier lists merged hits of one kind on one line (a comprehension twice on one line counted once), so the exact counts at 526a5666d are 372 loops (not 367), 76 clamps (not 71), 27 roots (not 25) and 22 state hits (not 21). A snippet holding a loop, two comprehensions on one line, a power, a floor division, a remainder, a shift, a raise, an ordering comparison, a minimum, a complex dtype, the complex type and divmod: every one found in an engine module, and in core/acts.py the division, the remainder and divmod pass. A patch that adds a raise and a power to core/spokes.py: two refusals and one note. 834cfd72e and the engine head c18414a43 against the list that stands: no refusal, no note.
- The gate tested on itself (2026-10-28, 09:3x): `venv314/bin/python tools/derivations/open_items/scribe_scan_selftest.py` runs 50 cases, a snippet for each rule that must trip it (the loops and comprehensions, the foreign operations under their operators and their numpy and operator names, the raise, the clamps, the comparison, the float and complex forms, the number, the circular names, the state, the pinned number in a test) and one that must not (a reader, the carry's home, the engine's own remainder function, 0 and 1), and the ratchet (two loops against one that stands give one new; a new package's every hit is new); a rule switched off in a trial parts seven of them. A change of the gate runs it first.
- The scope widened (2026-10-28, 09:2x), for the new engine of section 10 beside the current one: a scratch tree holding a new package (src/new_engine/core/step.py with a loop, a minimum, a number, a power, an ordering comparison and a raise) and a test file with a pinned number gives one refusal for each of the six code rules, one note for the comparison and one for the pin, the file named by its path under src; a new package has no counts, so every hit in it is a rise; the head 834cfd72e and the Boss's head 24a8806c2 against the list that stands (932 hits): no refusal, no note.
- Replayed with the loop rule (2026-10-28, 06:5x): the Boss's order-free click (42d5448b7 against 97e5b3fd6): no refusal and 31 notes (the loops of the new phase.py and of the modules it touched, one cache); the pushes after it: no note.
- A synthetic module holding every kind (import math, a container, a global, a division, round, np.cos, np.zeros with no dtype, an id, a table, a bilinear tuple, a root, a log read): refused for each. A moved line, a container made non-empty, a violation removed: no new hit. A number replaced by another: refused. An allowed entry (a test only, removed): the one hit stands.
- The installed git hook in a throwaway repository: a clean push goes through, a violating push is refused and the remote does not hold it, `--no-verify` goes round. The Claude command: a violating `git push` exits 2 with the message, an `ls` and a clean push exit 0, a clone with no script lets every push go.
- The patched RATCHETS run as tools/check.py runs them: the engine gates, the code's and the tests' shapes and the new gate hold at the head; the documents' gates now read the script itself (a run of three capitals is refused in a script too).

## What the gate enforces on every Tensor24 push (the owner's direct words of 2026-10-28, 08:5x to 09:0x UTC)

The owner to Sofer: Sofer is in effect the gate of every push of the Tensor24 plan, enforces that there are no numbers in the code, that everything is generic, that no loop makes a formula, that the engine knows no family but acts generically on one (the families' definitions, with their numbers, stand in the universe and world files), that there are no declarations and no statements, everything following from the laws and the mathematics and no result fitted to what is wanted, as the exclusion is today; that only three operations enter the code, multiplication, addition and Rule3; that the complex numbers are whole numbers in the coefficients; and approves, after the code is in, that all the fakes were fixed. The plan is the Boss's file; he decides what advances it. This section is Sofer's list for his section 21.

**What the scan refuses, by rule** (each a count per file that may not rise above the merge base; the scan reads every package under src, and the tests for PIN):
1. **No numbers:** NUMBER (beyond 0 and 1); TABLE (a typed table of three or more integers); the typed axes count AXES = 3 leaves with the lattice read from the piece's shape.
2. **Whole numbers only:** FLOAT (a float, a true division, round, pow, the complex type or literal, a numpy float or complex dtype); IMPORT; DTYPE.
3. **No circle and no root:** CIRCLE, ROOT, WORD (a circular word in a name).
4. **Three operations only:** OPERATION (a power, a shift, an exclusive or, a floor division or remainder outside core/acts.py and core/rule3.py, where the carry is written); CLAMP (min, max, abs, clip, where); COMPARE (an ordering comparison, a note until the gate is one act of carries, then a refusal).
5. **No loop that makes a formula:** LOOP, a refusal per file and kind; the end state is 0.
6. **No declaration:** REFUSE (a raise by name in an engine module); with TABLE above.
7. **Generic, and state only in the Node-clock:** STATE, MEMO, LOGREAD, and the engine gates' counts of family names and of the unsprung hand's identity.

**What Sofer reads on every push, because no script can** (the diff against every law and postulate, within 15 minutes of the post):
- **Every new line is a term of a formula of the plan** (section 19 and the cut's own formula, David's): a condition, a sign, a constant, a branch or a refusal that the formula does not hold is a declaration and the push stops. This is the check that the result is not fitted to what is wanted.
- **The engine knows no family:** no name, no identity read, no branch on a train; dispatch by kind and the calibre's integers; the numbers of a family only in the universe and world files (the rename test: rename every family of a universe file and the run's gears are the same bits).
- **The complex numbers:** a hand is a Gaussian integer, two integer coefficients (three and twelve); the functions are the sum, the complex product ((a c - b d) + i (a d + b c): products and a sum), the conjugate (the imaginary coefficient's sign), the norm (a product and a sum), the multiplication by i (an exchange and a sign), and the real and imaginary coefficients of conj(z) w (the dot and the cross); Rule3's carry acts on each coefficient as its own gear with its own remainder. Refused: the complex type or literal, a complex dtype, a complex division, the absolute value, argument, exponential or root of a complex number, any polar form. A ring for the twin hands (Z[zeta8] or the double cover over the Gaussian integers) is David's derivation: integer coefficients and the same three operations, checked when it is posted.
- **The two clicks:** the click of a whole is one carry of the wind at the winding (q = E div w, the remainder booked) and nothing else; the click of a split is the one comparison c (rho + rho) rho_d < room (rho rho_d + S . m), the draw by the parts' sizes, the one place a choice enters; any other branch that chooses is refused.
- **The tests of the plan can fail:** the stencil, purity and rename tests, the formula's probe and the images test on every chart pass at the push; a pinned number a test asserts is a verdict the code wrote, and the scan notes each one (PIN, 126 at the head, 0 in a new test file).

**After the code is in** Sofer approves, in one line in the thread, that all the fakes were fixed: every count above is 0 at the head and the baseline file empty; the five tests pass; every item of the fakes lists (SOFER-FAKES-1.md A1 to A13 and G1 to G9; David's R1 to R14 and bounds; Animate's F1 to F5 and the readers' rows) has its closing commit named; the law's lines on Pauli, the bounds, the closure, the shears, the turnover's triggers and the typed exponential entered only on the owner's word; the rewind exact 20 of 20 and the images alike on every chart; the readers' rows each read two independent readings (Animate).

## What it cannot do

- It sees words and shapes, not meaning: a rotation or a probability law written in plain names passes (Sofer's reading, and the owner's rule "report at once", stay).
- It counts loops and does not weigh them: a loop over the six spokes and a search loop count alike, and the owner's end state is 0 in the machine.
- It counts a raise in the loader like a raise in an act, and it counts boolean masks (and, or, not, &, |, ~) nowhere: they are the glue of the comparisons, which stay a note.
- A push through the GitHub API (a tool writing files straight to a branch) passes no git hook and no Bash command; a command that commits and pushes in one line is read by the Claude hook at the commit before it (the git hook reads the right one).
- It stands in the clone of whoever runs it: a session that edits or removes the script or its hooks is a breach, and Sofer reads every push for it (a change of the gate's own files is printed as a note).

## If a rule or a law must be broken

Stop, and tell the owner, the Boss and David in the thread at once (his order of 2026-10-28, 04:5x UTC). Only his word lets a hit stand: Sofer writes it into scribe_scan_allowed.json with the word and the row, and then the push goes. A restructure that moves code (the rename of 67a7633d5 is the example) is refused whole and goes with his word.
