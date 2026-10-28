# The Scribe's gate: the owner's rules as a script that refuses a push

The owner's direct words of 2026-10-28, 05:0x UTC, to the Scribe (in Hebrew, verbatim in translation): "From the twins' state! Sync. Everything you found here that cannot be at all, also for David: if he tries to bring in circles, or numbers in the code, or cosines or formulas, it is better that it shouts at him right there, that he need not go through you. Let your laws be simply in scripts, that cannot push at all things that break our lawfulness. Do you understand what I say? But do it logical and smart."

This file says what the gate does, how it decides, where it runs, what it cannot do and what the Boss adopts. The script is tools/derivations/open_items/scribe_scan.py (the law's **No circularity that makes a phenomenon happen** names it); it needs nothing but the standard library and Python 3.14 (venv314/bin/python; an older interpreter runs it again under the repository's own).

## What it refuses

A rule is a count of hits per file in src/event_universe. A refusal (tier BLOCK) stops the push; a note (tier WARN) is printed and the push goes.

| rule | tier | what a hit is | the law it keeps |
| --- | --- | --- | --- |
| NUMBER | BLOCK | a number beyond 0 and 1 | No number in the code |
| FLOAT | BLOCK | a float literal, a true division, round(), pow(), float, a numpy float function | No float anywhere in the system |
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

`scribe_scan.py --rules` prints the same table. The words are the ones the owner named; the script cannot read a formula that spells no such word (a closed form with plain names), so the Scribe still reads every push whole against the five rules, and the gate only takes from that reading what a script can see.

## How it decides: a ratchet, and no list to keep

A push may not raise the count of any hit above the same file's at its merge base (the revision named by CHECK_BASE, else origin/engine-5.0-test): what stands at the base stands, and the code departs from the law at the register's R5 until the Boss removes it. A hit is keyed by its rule, its file and its detail (the number, the name, the container), never by its line, so a moved or reformatted line is no new hit; a module git reads as renamed carries its counts; a new file has none. Replacing one hit by another of a different name is a new hit. A hit leaves the list by being removed and enters it only by the owner's word: tools/derivations/open_items/scribe_scan_allowed.json holds the entries the owner allowed (rule, file, detail, count, his word, the ledger's row), is written by the Scribe alone and is read from origin/scribe-5, so that a push cannot allow itself by editing its own copy. It stands empty.

`scribe_scan_baseline.json` is the other list: the hits that stand now (209 at the engine head 42d5448b7), for the Scribe's audit of the whole tree (`scribe_scan.py --baseline`), and it can only shrink.

## Where it runs

1. **At the push, by git.** `python tools/derivations/open_items/scribe_scan.py --install` writes .git/hooks/pre-push in the clone (a hook of another make is never overwritten); every `git push` then reads the commits it sends and is refused with the hits named, by file and line, and the law each breaks. `git push --no-verify` goes round it, which is a breach to report.
2. **At the push, by Claude Code.** tools/derivations/open_items/scribe_gate_claude_settings.json is the project settings file for .claude/settings.json: a PreToolUse hook on Bash that reads every command holding `git push` and refuses it (exit 2, the message shown to the session) before it runs, and a SessionStart hook that installs the git hook above in every new session's clone. It shouts at the session at the moment it types the push, which is the owner's "right there".
3. **At the merge, by the Boss's checks.** tools/derivations/open_items/scribe_gate_check_py.patch adds one line to the RATCHETS of tools/check.py, so that `tools/check.py` (every selection and `--full`) and the CI's lint shard run the gate against CHECK_BASE like the four ratchets before it.

The three are the Boss's to adopt (the Scribe writes no tools/*.py and no .claude/ file): `git apply tools/derivations/open_items/scribe_gate_check_py.patch`, and copy scribe_gate_claude_settings.json to .claude/settings.json. A refusal at the server, so that even a push that goes round the hooks cannot land, is one setting of the repository (a required status check on engine-5.0-test), the owner's.

## Tested

- The engine head 42d5448b7 against its merge base: no refusal, no note; the Boss's push of 04:39 against 97e5b3fd6: no refusal and one note (the module-level cache draw.kept_mid).
- David's DAVID-THE-BELL-LOCAL.patch on 97e5b3fd6: ten refusals (the module-level containers _BELL and BELL_DETECTORS, two id() keys, four reads of the log, the typed twins (1, 0, 1, 0), the four bilinear sums of bell_turn) and three notes (quaternion and Born in docstrings).
- Replayed over the last 40 pushes to engine-5.0-test that touched src (each against its parent): 30 pass (five of them with a note) and 10 are refused, nine with one to a dozen hits each, every one a real hit under today's rules (an id() key at tick.py:293 in 97e5b3fd6 and at tick.py:252 in ce40d8d63, a log read in undo, a number 4 in merger_end, a number 2 in core/acts.py, sine_rim in phenomena.py, the angles of the setting), and the restructure of 67a7633d5 (modules and functions moved) is refused whole with 134 hits.
- A synthetic module holding every kind (import math, a container, a global, a division, round, np.cos, np.zeros with no dtype, an id, a table, a bilinear tuple, a root, a log read): refused for each. A moved line, a container made non-empty, a violation removed: no new hit. A number replaced by another: refused. An allowed entry (a test only, removed): the one hit stands.
- The installed git hook in a throwaway repository: a clean push goes through, a violating push is refused and the remote does not hold it, `--no-verify` goes round. The Claude command: a violating `git push` exits 2 with the message, an `ls` and a clean push exit 0, a clone with no script lets every push go.
- The patched RATCHETS run as tools/check.py runs them: the engine gates, the code's and the tests' shapes and the new gate hold at the head; the documents' gates now read the script itself (a run of three capitals is refused in a script too).

## What it cannot do

- It sees words and shapes, not meaning: a rotation or a probability law written in plain names passes (the Scribe's reading, and the owner's rule "report at once", stay).
- A push through the GitHub API (a tool writing files straight to a branch) passes no git hook and no Bash command; a command that commits and pushes in one line is read by the Claude hook at the commit before it (the git hook reads the right one).
- It stands in the clone of whoever runs it: a session that edits or removes the script or its hooks is a breach, and the Scribe reads every push for it (a change of the gate's own files is printed as a note).

## If a rule or a law must be broken

Stop, and tell the owner, the Boss and David in the thread at once (his order of 2026-10-28, 04:5x UTC). Only his word lets a hit stand: the Scribe writes it into scribe_scan_allowed.json with the word and the row, and then the push goes. A restructure that moves code (the rename of 67a7633d5 is the example) is refused whole and goes with his word.
