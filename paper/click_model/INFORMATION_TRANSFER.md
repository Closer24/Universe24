# Everything is information transfer: the formulas it gives the paper, and how each reads in the real world

A report for the Boss (the owner's request of 2026-09-20: "think which
formulas can be derived for the paper from information transfer on the
GameBoard, and how it translates to the real world"). The principle is
[POSTULATES.md section 24](../../POSTULATES.md) and Highlights 5.4 ("Everything
is information on rays", read under the law of events). The rules are those
of `amplitude-v1` as the paper states them (Definitions 1 to 3 of
`main.tex`). The numbers are in [`checks/information_transfer.txt`](checks/information_transfer.txt)
(`checks/information_transfer.py`, formulas evaluated from the rules, not an
engine run), and every registered number they are compared with is in
[`NUMBERS.md`](NUMBERS.md). Each formula carries one of the paper's four
labels: **measured** (a registered run), **proved** (from the definitions),
**assumed** (put in) or **open** (a conjecture, or a question for the Boss).

## 1. The principle as it holds in the model

The state of the GameBoard at an interval is the multiset of rows
(amount, phase, multiplicity, record, branch) on its Nodes, and nothing
else: a Node holds no register, remainder or draw (the engine's contract,
[ARCHITECTURE](../../docs/ARCHITECTURE.md)). Every rule (transfer, collision,
split, rotation, merge, birth) maps the rows at a Node and its six
neighbours to rows, one Link per interval. The click is the only read: it
takes one record's rows, reports one cell, and deletes the record. So in the
model "everything is information transfer" is not a slogan but a
proposition: *information exists only on rows, moves only on Links, one per
interval, and leaves the rows only at a click.* The one exception is the
apparatus's layer (the pointers X, Y per Node), which is host bookkeeping
for the click and is read once and deleted; the paper already places it
with the apparatus, and the proposition must say so.

## 2. The formulas that follow

| # | Formula | Status in the model | Real-world reading | Departure or test |
| --- | --- | --- | --- | --- |
| 1 | **Causal cone.** No information at more than one Link per interval, and the flight table (BEAM_LAW section 3) moves every direction at `1 / sqrt 3` Links per interval on its digital line: the front is a sphere to the line's rounding (1.5 percent over 600 intervals). | proved (the flight table); measured (L7: the axis row 17 Links and the diagonal row 24 Links both click at the age 29) | `c = a / (tau sqrt 3)`, the light cone, isotropic | None from the front. The lattice's anisotropy sits in the phase, row 9: the *time* to a Node is Euclidean, the *Links stepped* are L1. (The first version of this row claimed an octahedral front; L7 refuted it.) |
| 2 | **Wavelength.** Two declared forms of `phase_per_link`: the integer form turns `p` steps per Link stepped, wavelength `N / p` Links along the staircase (L1); the pair form turns `n / d` steps per interval of age, wavelength `N d / n` intervals = `N d / (n sqrt 3)` Links of Euclidean length in every direction. The shortest is 2 Links or 2 intervals; the resolution is `2 pi / N`. | proved (the phase rule; `by_clock`); measured (L7) | de Broglie: `k = 2 pi / lambda`, `omega = c k`, no dispersion, no mass in the worlds of this paper | The Link is at most half the shortest wavelength ever seen: `a <= 4.4 x 10^-22 m` from the 1.4 PeV photon of LHAASO (2021). No lower bound on `a`. The energy `h nu` is not in the model (no energy is defined on a row): the reading `E = h c / lambda` is **assumed**. |
| 3 | **The click's precision.** `P(o) = b_o / N` with the rungs `b_k = (2 N C_k + T) // (2 T)`: `\|P(o) - W_o / T\| <= 1 / (2 N)`. | proved (Definition 3) | the Born rule to precision `1 / (2 N)`; probabilities are multiples of `1 / N` | A squared-sum law confirmed to `delta` bounds `N >= 1 / (2 delta)`: `N >= 500` at `10^-3`, `5000` at `10^-4`. The pair's `S(N)` against Poh et al. 2015 is sharper (`N >= 184`, `checks/s_of_n.txt`). The Born rule itself is **assumed** (the click reads the squared sum by definition, as the paper says). |
| 4 | **No amplification.** The split `(w, m) -> (w a_i, m A)`, `A = sum a_i^2`, keeps `sum w_i^2 / m_i = w^2 / m` (Theorem 2). | proved | no-cloning: two rows of the full norm would need the sum 2; an amplifier cannot copy one quantum | None that a run tests; the (3, 4) split's 63/1 is the registered instance of the identity (L1). |
| 5 | **Bits per click.** A click reports one cell of a record: at most `log2 (cells)` bits leave the rows per record, whatever the rows carried. | proved (Definition 3) | the Holevo bound: at most `log2 d` classical bits from one measurement of a `d`-level system | The register's GHZ XXX: 4 of 8 triples, 2 bits, the product the law's. Not a test, an identity of the model with quantum mechanics. |
| 6 | **The joint law of a pair.** `P(o_A, o_B \| a, b) = #{u : cell_A(u, a) = o_A, cell_B(u, b) = o_B} / N`, `u = t mod N` the birth phase carried on the record (eq. joint in the paper). | proved; marginals `N / 2` (Theorem 3); `E` within `2 / N + 0.011` of the cosine (Theorem 4) | Bell correlations; no-signalling; the shared variable is the birth interval modulo `N` | `S(N)` computed for every `N`; measured at 64, 1024, 4096. Two records born at the same `u` in identical apparatus click alike: real sources spread births over many intervals, so `u` is uniform in practice (**assumed**, as the paper says). |
| 7 | **Distance.** The joint law does not depend on the Links between the parties. | measured (`bell_16_24_far`: Bob 116 Links farther, cells 27, 5, 5, 27, `E = 11/16` as at 116 Links nearer) | Bell correlations independent of distance (Hensen 2015 at 1.3 km; Yin 2017 at 1200 km) | None; the click adds nothing that travels. |
| 8 | **Reversibility between clicks.** The maps between clicks are injective given the record (Theorem 1); the only deletion is the click. | proved | unitarity between measurements; the arrow of time is the record of clicks, nothing else | Landauer's reading (**open**, a conjecture): a click erases at least the rows' bits less the cell's, `Q >= k T ln 2 x (bits erased)`: 16 to 56 bits for the register's records, 0.3 to 1.0 eV at 300 K, 1 to 3 meV at 1 K, a lower bound far below any real detector. |
| 9 | **Two slits.** Under the integer form the path difference of two slits at distance `s` is the L1 one, `\|y - s/2\| - \|y + s/2\|`, constant beyond `\|y\| >= s / 2`: no periodic fringes. Under the pair form the phase counts intervals, the flight is Euclidean, so the path difference is the Euclidean `~ y s / D` to the rounding and the fringes are spaced `lambda D / s`. | computed from the rule (the table in `checks/information_transfer.txt`); the two forms measured in L7 | Young's fringes, spaced `lambda D / s` | The registered two-slit world declares the pair form, so its Pearson 0.368 with the cosine (L2) is not the L1 effect; the gathers of that run land five `u` alone on the screen (PR #395's reading), and the pattern's visibility is not formed there. **Open**: which form nature's light is, the model does not say; a two-slit world with enough gathers per pixel under each form. |

## 3. What does not follow, and is not claimed

- **Isotropy, settled by L7 as far as the engine goes.** The flight table
  moves every direction at `1 / sqrt 3` Links per interval (Euclidean, to
  the digital line's rounding), so the cone is isotropic. What the lattice
  counts is the phase: the integer form of `phase_per_link` counts the
  Links stepped (L1 on a staircase, 24 for the diagonal row against 17 for
  the axis row at the same Euclidean distance), the pair form counts the
  intervals (Euclidean, 29 for both). The registered worlds with a phase
  per Link (the unequal-arm Mach-Zehnder, the two slits) declare the pair
  form. What the model does not say is which form nature's light is: the
  paper states both forms, the L7 readings, and that the Euclidean one is
  the pair form.
- **Energy, mass, gravity.** No row carries energy or mass; the worlds of
  this paper have no mass. The readings `E = h nu`, the rest clock
  `content / K` per interval, and gravity as a delay are Highlights
  hypotheses, not formulas of the click model; Part II lists them as
  conjectures with the model identity that would carry them.
- **The tick and the Link.** `a` and `tau` are free; only `c = a / tau`
  and the bound `a <= lambda_min / 2` follow. `N` is bounded below by the
  Bell data (`N >= 184`) and above by nothing.
- **Which-path with a window, HOM, the rung tie, unequal weights**: open
  as the paper lists them (PLAN.md, referee round 1).

## 4. What is proposed for the paper

Half a page in Part I after Lemma 1: the proposition of section 1 with its
one-paragraph proof (the state is the rows; each rule is local and
one-Link; the click is the only read and deletes what it reads; the layer is
the apparatus's). Rows 1 to 8 of the table as the consequences already in
the paper, gathered under that proposition (the cone and the wavelength are
new sentences; 3 to 8 are Theorems 1 to 4 and the far worlds restated as
information statements). Row 9 and the isotropy paragraph go to "not
claimed" and to the computed departures, with the two-slit Pearson as the
evidence. The Landauer reading goes to Part II as a conjecture with its
number. No number of the paper changes and no physical law is touched.

## 5. Questions for the Boss

1. Which length does a row's phase count on an oblique momentum?
   Answered by the Boss (issue #376, the integer form counts the Links
   stepped) and by the run L7 (section 6): the time to a Node is
   Euclidean by the flight table, the phase's metric is the declared
   form's.
2. Is the proposition of section 1 acceptable as the paper's statement of
   the principle, with the layer named as the apparatus's?
3. Does the Boss want the Landauer conjecture in Part II, or kept out?
4. Should the isotropy question become an item in the day's log for the
   physicist, since it is the first thing the model owes the real world
   after the Bell value?

## 6. The cone test, series L7 (2026-09-20)

Approved by the Boss on issue #376, run on the one click's head 725d811f
(the fingerprint `4bf55a62e6fd`; the run on main follows PR #395's
landing). Two worlds of one geometry, `cone_links` (the integer form, 3
steps per Link stepped) and `cone_intervals` (the pair form [3, 1], 3 steps
per interval of age): a lamp at (0, 0) on +x to a counter 17 Links away, a
lamp at (0, 3) on the plane diagonal (1, 1, 0) to a counter at (12, 15),
24 Links along the staircase (the Euclidean distances 17 and 16.97), N =
64, 96 intervals. Pinned before the run from the flight table (BEAM_LAW
section 3; `expectations.json` under `cone`): both rows click at the age
29; the path phase phase - u at the click 51 and 8 under the integer form,
23 and 23 under the pair form.

| Reading | Pin | `cone_links` | `cone_intervals` |
| --- | --- | --- | --- |
| Age at the axis click / the diagonal click | 29 / 29 | 29 / 29 | 29 / 29 |
| Path phase at the axis click | 51 (links), 23 (intervals) | 51 | 23 |
| Path phase at the diagonal click | 8 (links), 23 (intervals) | 8 | 23 |
| Records per lamp, all alike | 67 | 67 | 67 |
| Gathers, one per record | 134 | 134 | 134 |

So: the cone is Euclidean; the phase's metric is the form's. Rows 1, 2 and
9 above were corrected on this evidence, and the check's sections 1 and 7
recomputed.
