# The derivations

This folder holds the derivations of the law's numbers in Python, each from
Rule3's line as `docs/ALGEBRA.md` states it and leaning on no run of the
engine (the owner's order of 2026-10-04, 04:20 UTC: every derived mark's
script, everything from Rule3, nothing from the simulator). A module is pure
Python, integers and fractions where the law is exact and floats where a
cosine is asked for; it imports nothing of `event_universe` and reads no file of
`runs/`; no number of nature enters a derivation, and nature's numbers enter the
comparison columns alone, named as such at the module's head. Its root is `rule3.py`, the line and
its invariants transcribed sentence by sentence (the coefficients, the step
and its backward act, the band at the vacuum's paces and at a Node's paces,
the group velocity, the conserved form with the remainders' walk, the paces'
closed formulas, the guard's edge and the bound); every other module imports
it and derives its numbers from it. The law's sentence beside the method of
derivation, step 6, is the folder's rule: no line of the law is derived from
the engine.

## The two gates

- Documents gate (3), `tools/documents_gates.py` `derived()`, run by
  `tests/test_documents.py`: every number of `tools/numbers.json` that carries
  a `derivation` rule (`module`, `function`, `expected`, `digits`, and
  `arguments` where the function takes the table's own inputs, a run's reading
  among them, which no module holds) is that function's output to the digits
  named, compared positionally, so a number of the documents is its script's.
- `tests/test_derivations_lean_on_rule3_alone.py`: (a) every module here
  imports nothing of the engine and names no run's file, a hard rule, and the
  paper-side scripts of `paper/general_formula/` that lean on the engine or
  read a run are a ratchet that only falls (`PAPER_SCRIPTS_LEANING_ON_THE_ENGINE`,
  2 at the paper's head d75c42a9); (b) the modules here that do not import
  `rule3` are a ratchet that only falls (`MODULES_WITHOUT_RULE3_ROOT`, at most
  4, the four modules below that receive no mark; an `import rule3` anywhere in
  the module counts), so a new module roots in `rule3.py`; (c) `rule3.py`'s own
  checks: a
  plane wave at the derived omega satisfies the line to rounding on a chain,
  the conserved form is exact over 50 intervals on a periodic chain of 24
  Nodes with integer levels and the integer step's walk of it is the law's
  term exactly; (d) the inventory below loads with every field, each entry's
  status one of `scriptless` (no script here yet), `scripted` (its `script`,
  `function`, `expected` and `digits` named) or `differs` (its `computed` and
  `reason` named, a finding for the hands), and the scriptless count is a
  ratchet that only falls (`SCRIPTLESS_MARKS`, at most 18); (e) every scripted
  entry's function returns its printed numbers in order, a `num/den` string as
  an exact Fraction, an int as it stands and a float to `digits` decimal places;
  the comparer matches the printed numbers as an in-order subsequence of the
  function's output, so a function returns its mark's numbers first and names
  every output in its docstring.

## The inventory

`paper_marks.json` lists every `\claimmark{derived}` and `\claimmark{computed}`
of the paper's `main.tex` (the branch `paper`, its head in the file's header)
whose enclosing parenthesis names no `\texttt{<name>.py}`, by the rule of
`paper_gates.gate_scripts`: the line, the mark, the section of `main.tex`, the
sentence, its printed numbers, the supplement derivation or section it cites,
the existing script that already gives its numbers where one exists under
`paper/general_formula/` or here, the proposed module here, and the status
`scriptless`. A computed mark, a reading of the implementation's run, names
its reader (the run's reader or its test, never a derivation) and, since the
owner's word of 2026-10-04, 04:39 UTC, two more fields: `derived_counterpart`,
the formula or the script and function that gives the derived value, or "none
in closed form" for the three the advisor names (the integer step's exact
remainders, the draw's outcomes at a seed, the body's fixed point by
iteration), and `bound`, the integer budget's bound where it applies. The run
is the check of the derivation and never the claim: beside the run's number
the derived value and the bound print, the two slits' N = 270 beside the law's
real line at the same lay, 269.3, within sigma sqrt(n) = 0.236 x sqrt(130) = 2.7
levels, about 1.1 unit of N; Bell's S = 478 / 169 and the GHZ's M = -4 beside
their exact derivations, the run a bit-for-bit check; the gates' readings
beside their blinds' formulas. The header also lists the paper-side scripts
that lean on the engine, each engine name they import with the law's line that
replaces it.

## How a later worker closes a mark

1. Take the mark's entry: its proposed module, its numbers and its source.
2. Write the function in that module, importing `rule3` and deriving the
   numbers from the line's functions and the law's sentences; the docstring
   names the sentence it transcribes and the formula, one line per step. Run
   the module: its `__main__` prints the numbers.
3. Where the number also stands in the documents, add a `derivation` rule to
   the number's row of `tools/numbers.json` (`module`, `function`, `expected`,
   `digits`); documents gate (3) then holds the number to the script.
4. The writer names the script beside the mark in `main.tex`,
   `\texttt{<module>.py}` inside the mark's parenthesis, and `gate_scripts`'s
   count falls by one; lower `SCRIPTLESS_MARKS` and the entry's status in
   `paper_marks.json` accordingly, with the paper's new head in the header.
5. A computed mark is closed by its reader and its derived counterpart, never
   by a derivation of the run's number.

## The proposed modules

| Module | Marks | Subject |
| --- | --- | --- |
| `weak_field.py` | 16 | the redshift, the bending, Shapiro's delay, the perihelion, the fall, Newton, the lens, the shadow, the gravity of light |
| `constants.py` | 15 | G_clock and Kepler's G, charge universality, alpha_law, the energy line, the Link's bound, the lattice's properties, the calibration series, the masses |
| `clicks.py` | 12 | the click's formulas: the frozen Node, the declarations' costs, the one draw, the arrival window, the write's form, decay statistics |
| `body_clicks.py` | 9 | a body's clicks: the resonance, Rabi's rate, the invariant and the drift, E = hbar omega, Millikan's slope |
| `bands.py` | 8 | the bands along an axis and the diagonal, the slow limit, de Broglie, the folded axis, light's speed |
| `bell.py` | 8 | the root's sum, the four lines of Bell, unequal parts, 478 / 169, the GHZ correlation, the bound |
| `paces.py` | 8 | the clock's composition, the acts' factors, the index, the mirror, the horizon, the two clocks |
| `families.py` | 6 | the universe table's columns, the holder's rest, the gap as the inverse reach, the two speeds, the gapped kernel |
| `frame.py` | 6 | the lattice's frame: alpha_1, the polarisations, no g_0a, the five forms, Gravity Probe B |
| `bodies.py` | 5 | the four statements, the functional's barrier, the kinds of binding, the binding bound |
| `moving_clock.py` | 4 | the tick's factor from the band, the Lorentz form, Michelson-Morley |
| `atom.py` | 3 | Bohr's levels, the orbital Zeeman g = 1, the nuclear holder's exclusion |
| `nuclear.py` | 3 | confinement, the nuclear findings, the explicit finding |
| `rule3.py` | 3 | the band at a pace, the form's walk with the rounding, the backward reading |
| `cosmology.py` | 2 | the ball of dust's deceleration, the Doppler period times the moving clock |
| `sign.py` | 2 | the Wronskian's walk witness, the odd lines' source |
| `two_slits.py` | 2 | the near-field minima, the opaque NodeReader's envelope |
| `tension.py` | 1 | the stress of dust |
| `zeno.py` | 1 | nature's n = 1 against the body's own period |
| (computed, no module) | 9 | the back-in-time gate, the two branches' solution, the two slits' run, the Bell efficiency, the atom's readings: readers named |

The existing modules `units.py`, `wells.py`, `two_body.py` and
`greens_function.py` receive no new mark and stand as existing scripts for
several. Forty-four marks already have a script whose output gives their
numbers (`paper/general_formula/einstein_check.py`, `stable_body_check.py`,
`moving_clock.py`, `bands.py`, `invariant_check.py`, `band_and_channels.py`,
`click_body.py`, `two_slits_real_line.py` and the modules here); the field
`existing_script` names it. `two_slits_real_line.py` imports the engine's
coefficients, count wall and loader and stands under the paper-side ratchet;
the header lists the law's line that replaces each import (w = 6 den Gamma^2,
R = 2 num Gamma^2, S = 0 at the vacuum's paces; W_c = 3 den T; the files are
JSON), so the import can drop when the writer re-pins the paper. A module of
this folder never imports the engine: `units.py` held the engine's
`count_wall` and `click.squared` as a second method until this gate, and the
engine's agreement with the formulas is the test's.
