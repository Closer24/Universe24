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
| 1 | **Causal cone.** No information at distance more than one Link per interval: `d_1(x, y) <= t` (the L1 distance in Links). | proved (the transfer rule) | `c = a / tau`, the light cone; nothing travels faster | The front is an octahedron: the Euclidean speed of the front is `1 / (\|cos\| + \|sin\|)` off an axis, `1 / sqrt 3` on the body diagonal, 42 percent slower than along an axis. Isotropy of `c` is tested to `10^-17` (Michelson-Morley type tests). **Open**: the model owes the real world the isotropy of its front, and no run in the register has an oblique free ray. |
| 2 | **Wavelength.** A row's phase counts `n / d` steps of the N-circle per interval of its age (or an integer per Link crossed), so its wavelength is `lambda = N d / n` Links; the shortest is 2 Links; the phase resolution is `2 pi / N` whatever the rate. | proved (the phase rule; `by_clock`) | de Broglie: `k = 2 pi / lambda`, `omega = c k`, no dispersion, no mass in the worlds of this paper | The Link is at most half the shortest wavelength ever seen: `a <= 4.4 x 10^-22 m` from the 1.4 PeV photon of LHAASO (2021). No lower bound on `a`. The energy `h nu` is not in the model (no energy is defined on a row): the reading `E = h c / lambda` is **assumed**. |
| 3 | **The click's precision.** `P(o) = b_o / N` with the rungs `b_k = (2 N C_k + T) // (2 T)`: `\|P(o) - W_o / T\| <= 1 / (2 N)`. | proved (Definition 3) | the Born rule to precision `1 / (2 N)`; probabilities are multiples of `1 / N` | A squared-sum law confirmed to `delta` bounds `N >= 1 / (2 delta)`: `N >= 500` at `10^-3`, `5000` at `10^-4`. The pair's `S(N)` against Poh et al. 2015 is sharper (`N >= 184`, `checks/s_of_n.txt`). The Born rule itself is **assumed** (the click reads the squared sum by definition, as the paper says). |
| 4 | **No amplification.** The split `(w, m) -> (w a_i, m A)`, `A = sum a_i^2`, keeps `sum w_i^2 / m_i = w^2 / m` (Theorem 2). | proved | no-cloning: two rows of the full norm would need the sum 2; an amplifier cannot copy one quantum | None that a run tests; the (3, 4) split's 63/1 is the registered instance of the identity (L1). |
| 5 | **Bits per click.** A click reports one cell of a record: at most `log2 (cells)` bits leave the rows per record, whatever the rows carried. | proved (Definition 3) | the Holevo bound: at most `log2 d` classical bits from one measurement of a `d`-level system | The register's GHZ XXX: 4 of 8 triples, 2 bits, the product the law's. Not a test, an identity of the model with quantum mechanics. |
| 6 | **The joint law of a pair.** `P(o_A, o_B \| a, b) = #{u : cell_A(u, a) = o_A, cell_B(u, b) = o_B} / N`, `u = t mod N` the birth phase carried on the record (eq. joint in the paper). | proved; marginals `N / 2` (Theorem 3); `E` within `2 / N + 0.011` of the cosine (Theorem 4) | Bell correlations; no-signalling; the shared variable is the birth interval modulo `N` | `S(N)` computed for every `N`; measured at 64, 1024, 4096. Two records born at the same `u` in identical apparatus click alike: real sources spread births over many intervals, so `u` is uniform in practice (**assumed**, as the paper says). |
| 7 | **Distance.** The joint law does not depend on the Links between the parties. | measured (`bell_16_24_far`: Bob 116 Links farther, cells 27, 5, 5, 27, `E = 11/16` as at 116 Links nearer) | Bell correlations independent of distance (Hensen 2015 at 1.3 km; Yin 2017 at 1200 km) | None; the click adds nothing that travels. |
| 8 | **Reversibility between clicks.** The maps between clicks are injective given the record (Theorem 1); the only deletion is the click. | proved | unitarity between measurements; the arrow of time is the record of clicks, nothing else | Landauer's reading (**open**, a conjecture): a click erases at least the rows' bits less the cell's, `Q >= k T ln 2 x (bits erased)`: 16 to 56 bits for the register's records, 0.3 to 1.0 eV at 300 K, 1 to 3 meV at 1 K, a lower bound far below any real detector. |
| 9 | **Two slits.** If the phase counts Links on a staircase path, the path difference of two slits at distance `s` is the L1 one, `\|y - s/2\| - \|y + s/2\|`, constant beyond `\|y\| >= s / 2`: no periodic fringes. With Euclidean length it is `~ y s / D`, fringes spaced `lambda D / s`. | computed from the rule (the table in `checks/information_transfer.txt`) | Young's fringes, spaced `lambda D / s` | The registered two-slit run correlates 0.368 with the cosine pattern and 0.744 with the incoherent sum (L2): the register's pattern is not Young's. **Open, the sharpest question for the Boss**: which length the phase counts, and how the L1 count becomes the Euclidean one at scale. |

## 3. What does not follow, and is not claimed

- **Isotropy.** Rows 1 and 9 are the same fact twice: the model's distances
  are counted in Links, and the count is L1. Every real interference
  experiment reads Euclidean lengths. Nothing in the click rules gives
  isotropy; it cannot be assumed silently. Candidates the Boss may weigh:
  (a) the step rule with a momentum whose label scale `Q S M` is large
  against `|p|` moves a row at the velocity `p / (Q S M)` on every axis at
  once, so the *time* to a Node is Euclidean to first order, and a phase
  counted per interval of age (the pair form) would then count Euclidean
  length; (b) lattice-gas results (a cubic lattice's second-rank tensors are
  isotropic, its fourth-rank ones are not; FHP and FCHC lattices restore
  isotropy) say what a six-direction lattice can and cannot do. Either is a
  computation the paper does not have; the paper states the L1 count and
  the two-slit Pearson as a computed departure and nothing more.
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

1. Which length does a row's phase count in `amplitude-v1` on an oblique
   momentum: the Links of the staircase (L1) or the intervals of its age,
   and does the step rule make the time to a Node Euclidean when
   `Q S M >> |p|`? A one-world run (a free ray at 45 degrees, a counter on
   each of an axis Node and a diagonal Node at the same Euclidean distance)
   would decide the cone's shape and the phase's metric together.
2. Is the proposition of section 1 acceptable as the paper's statement of
   the principle, with the layer named as the apparatus's?
3. Does the Boss want the Landauer conjecture in Part II, or kept out?
4. Should the isotropy question become an item in the day's log for the
   physicist, since it is the first thing the model owes the real world
   after the Bell value?
