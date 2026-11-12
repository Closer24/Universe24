# From clock relations to a measurement law

The four retained receiver channels produce coherent intensity records on the
same carrier board. They do not yet produce a normalized single measurement
outcome. This distinction survives exact replay and every allowed detector
remainder. The next construction must change apparatus dynamics and its
preparation contract; changing the displayed count or drawing a new outcome
from normalized weights would assume the missing law.

## Preregistered experiment and scope

The implementation is `validation/clock_links/born_bell_audit.py`, based on
main `4c494c1188f70eb8a677bf59765cc6e8571c6b88`. The integration run imports the
pinned 44-field bundle and appends the same four channels used by the phase
and observer audits. There is one 48-channel tensor and the unchanged Engine.
No external randomness, acceptance selection or probability feedback is used.

Two carrier amplitudes are prepared at separate nodes on an arrival snapshot.
All current and previous carrier components are cleared before inserting the
declared current amplitudes; the other base fields remain unchanged. This is
a calibration of the apparatus response to a supplied snapshot, not a
constraint-satisfying Einstein preparation or a transported emission experiment.
Both initial detector remainders independently take every value in 0..5, giving
36 equally weighted preparations per case. Equal weighting is an explicit
experimental measure, not a distribution derived from the board.

Every trial uses one predeclared update. All C0/C1/C2 classes are retained, with
none/single/multiple outcomes kept separately. The seven cases give 252 complete
trials. Four coherent phase controls and two indistinguishability controls bring
the saved total to **258 complete transitions**. Each saved record contains the
full initial and final state and the canonical click stream. The CLI rereads
every record, checks the exact complete trial set, recomputes every output with
the independent coordinate/monomial scalar oracle, checks inverse recovery and
canonical stream equality, and verifies saved state hashes where supplied.

## Exact result: weight is not count

For a receiver driven by `u=3I`, the fixed-six law gives

\[
\ell,r'=\operatorname{divmod}(6I+r,6)=(I,r),\qquad
(a',b')=(b,I-a).
\]

Thus the retained quotient is exactly the intensity, independently of the
initial remainder. Every receiver record is C0. For a ready receiver with
`a=b=0`, positive intensity gives a record with quotient `I`; zero intensity
gives none. Two positive branches therefore both produce a record, regardless
of their relative intensities.

| Prepared intensities | Trials | Binary counts | Quotient weights | Trial outcome |
| --- | ---: | --- | --- | --- |
| 9:1 | 36 | 36:36 | 324:36 | All 36 are multiple |
| 36:4 | 36 | 36:36 | 1296:144 | All 36 are multiple |
| 1:1 | 36 | 36:36 | 36:36 | All 36 are multiple |
| 4:0 | 36 | 36:0 | 144:0 | All 36 are single |
| 0:0 | 36 | 0:0 | 0:0 | All 36 are none |

A common quarter turn preserves the 9:1 result. The face receiver correctly
distinguishes constructive, destructive and quadrature amplitudes, producing
4, 0 and 2. These are exact interference records. Normalizing their quotient
weights can reproduce an intensity ratio, but that is not an exclusive outcome
frequency. In particular the 9:1 preparation has a binary-event share 1/2:1/2,
not 9/10:1/10.

## A stronger receiver-only obstruction

If `I` is even and `a=b=I/2`, the receiver triple is unchanged. The official
arithmetic record rule therefore emits no event even though `ell=I>0`.

This is tested on the full 48-channel tensor with two source preparations:

- `z0=(3,1), z1=(1,1)` gives local intensities 10:2.
- The exchanged amplitudes give 2:10.

Every local and face intensity in these preparations is even. Preparing each
of the four receiver channels at `a=b=I/2` produces **the same empty receiver
stream everywhere** during the one-update observation window. Their normalized
positive intensities differ: 5/6:1/6 versus 1/6:5/6.

Consequently no decoder restricted to those four receiver streams can recover
the Born ratios for every admitted apparatus seed in this window. This is a
protocol-specific impossibility result. It does not exclude a restricted
preparation sector, longer observations, access to other records, or a different
interacting detector. The old and new full states remain distinct and exactly
reversible; the loss occurs at the observation boundary.

## What a constructive next stage must add

1. **A declared ready-state domain.** Specify which apparatus histories are
   allowed, how a fresh apparatus is physically prepared, and how preparation is
   included in the retained budget. A runtime reset is not permitted. Restricting
   the initial domain removes the stationary counterexample only if that
   restriction is justified; it does not remove the ready-state double clicks.
2. **A coupled, persistent pointer.** Replace the independent intensity readers
   with an interaction that changes future retained apparatus and carrier
   states. Demonstrate exactly one stable pointer outcome per complete trial,
   including finite response time and no/double controls. Lost alternatives
   must remain in reversible degrees of freedom; an external winner selector
   is not the mechanism. The proposed oscillator/pointer allocation in the
   algebra report is a candidate interface, not an implemented instrument.
3. **A measure over prepared clock phases.** For a deterministic reversible
   map, an outcome frequency requires a preparation measure `mu_psi`. The law
   alone does not select one: different distributions over complete initial
   states can give different frequencies. Derive and test a preserved or
   transported measure and outcome basins satisfying
   `mu_psi(outcome i)=|psi_i|^2/sum_j|psi_j|^2`. Merely choosing this basin measure
   is the Born assumption. A local phase rotor with six equally weighted states
   by itself only supplies fractions with denominator six; the retained
   apparatus must explain any finer measure used.
4. **Predeclared instrument tests.** After selecting an explicit mechanism,
   test held-out amplitude ratios, common phase, interference cancellation,
   amplitude scaling, apparatus-history sensitivity, repeatability, and full
   trial completeness. Coupling, stress and clock calibration must use the
   same metric before a physical apparatus claim is made.

No minimal number of required channels is proved here. All four free slots
are currently occupied, so a future pointer mechanism must replace or share
their functions with an explicit reversible encoding; it cannot append a
second apparatus bank.

## Complexity and Bell remain separate gates

For positive intensities and positive complexity factors, direct algebra gives

\[
\frac{I_0c_0}{I_0c_0+I_1c_1}=\frac{I_0}{I_0+I_1}
\quad\Longleftrightarrow\quad c_0=c_1.
\]

The audit checks 1,296 integer cases. For example, intensity 9:1 multiplied by
complexity factors 2:1 becomes 18/19:1/19. A common factor cancels. Complexity
may still change amplitudes, preparations or the apparatus interaction before
measurement; unequal postweighting of already fixed intensities generally
changes Born ratios.

Treating the entire board as one clock expands the common-past state; it does
not by itself remove the Bell assumptions. If complete trials share a
setting-independent distribution and conditional responses factor locally,
their response means obey `a0,a1,b0,b1 in [-1,1]`. Pointwise,

\[
|a_0(b_0+b_1)+a_1(b_0-b_1)|
\le |b_0+b_1|+|b_0-b_1|
=2\max(|b_0|,|b_1|)\le2.
\]

Averaging preserves the bound. The exact rational grid checks 6,561 response
tables, including local stochastic rules and zero outcomes. A probability
draw performed only at detection remains subject to the same conditional
factorization. The apparatus in this iteration supplies neither an entangled
source nor two physical analyzer settings, so an Engine Bell experiment is
**not tested**, not passed. Any proposal to change a Bell assumption must state
which assumption changes and test its consequences, rather than infer a
violation from C2 filtering or a shared clock.

Primary references for this theoretical boundary are Bell,
[Physics Physique Fizika 1, 195 (1964)](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195),
and Clauser, Horne, Shimony and Holt,
[Physical Review Letters 23, 880 (1969)](https://doi.org/10.1103/PhysRevLett.23.880).
The code-specific statements above are proved by the displayed fixed-six
algebra and the stored complete-state experiments, not inferred from those
papers.

## Reproduction and gate status

Run the combined audit from a fresh output directory:

```bash
python -m validation.clock_links.run_audits \
  --base-bundle runs/team48-contract/run/bundle \
  --out runs/clock-links-final
python -m unittest universe24.tests.test_clock_link_born_bell -v
```

The base path must identify the pinned 44-channel import produced by
`validation.team48_contract`, not a hand-written substitute. The tests use a
small mechanical carrier fixture to isolate the observation regression; the
CLI evidence uses the full 44+4 integration and stores the input bundle.

| Gate | Result |
| --- | --- |
| Same-board coherent intensity record | Passed in these preparations |
| Complete trial retention and exact saved replay | Passed for the declared 258 transitions |
| One outcome per measurement trial | Failed |
| Binary Born frequencies | Failed |
| Universal intensity recovery from four receiver streams | Refuted for the declared one-update/all-apparatus domain |
| General physical detector or proper clock | Not established |
| Engine Bell violation | Not tested |
