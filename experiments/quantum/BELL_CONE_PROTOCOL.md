# Bell / cone audit protocol

Declared before executing this audit. This tests the existing PR #33 wave
tensor; it does not add an entangled source or a physical spin analyzer.
No tensor, runtime, detector callback, or click definition is changed.

## Geometry and trials

Use distance d=3, periodic side L=4d+1=13. Emit `nx` and `px` packets from
the center toward Alice and Bob at x=center-d and center+d. Their separation
is 2d=6. Both measurements end after d=3 updates, before either setting can
influence the opposite detector. All packet `a,b,r` history is prepared;
the initial source footprint includes the previous packet positions.

Every source emission has a fixed trial identifier. Pair records by that
identifier, never by searching for a convenient coincidence window. End each
trial at the declared arrival time, including trials with no C2. Verify that
there are no detector clicks before arrival, all full-state differences from
a no-packet control stay within the complete-seed cone, and full rewind is
exact. Compare Alice across Bob's choices and Bob across Alice's choices.

Enumerate every combination of source label lambda and x,y in {0,1}, equally
weighted. Thus the source distribution is exactly identical in all four
settings. Hash all packet-lane initial triples to verify this independently
of the scalar outcome summary. This is finite exact enumeration, not an
experimental p-value or a random-settings hardware implementation.

## Declared local settings and outputs

The default detector has no analyzer angle. First run it literally with gain
one for both nominal settings, unit packets, and label this a settings-inert
control. It cannot establish a physical Bell prediction.

For two additional **audit controls only**, encode a local setting in the
existing static marker: `a_detector=b_detector=1+x` for Alice and `1+y` for
Bob. The unchanged `u_detector=6*b_detector` retains it. This is a new declared
preparation, not a quantum measurement model. A binary outcome is the sign of
the actual arrival quotient, not the C2 label. Memory starts with r=2 as in
the PR. Select outcomes only after `Engine.step`.

Report three readers on the same records:

1. Every emission, any arrival click; assign +1 locally if there is no click.
2. Every emission, C2-only detection; assign +1 locally to a non-C2/no-click.
3. A deliberately conditional sample keeping only trials with C2 at both
   detectors. Report all acceptance denominators; if any setting has no
   accepted trials, CHSH is undefined, not zero and not a successful test.

Compute exact rational E_xy and `S=abs(E00+E01+E10-E11)`. Also report local
marginals, per-setting efficiency and direct counterfactual locality. The
16 possible local binary response tables provide an independent algebraic
bound S<=2 for every-emission readers; timing and memory can be included in
lambda without changing this bound.

## Source controls (no fitted search)

- `literal_unit`: one unit packet to each side; both nominal settings use
  the unchanged gain-one preparation.
- `shared_sign`: equally weighted source signs sigma=-1,+1; both packet
  payloads equal sigma. This checks that missing conditional settings are
  retained and reported.
- `selection_stress`: deliberately constructed detection-loophole control,
  **not a candidate explanation of nature**. Enumerate lambda=(i,j,sigma),
  i,j in {0,1}, sigma in {-1,+1}. Set local desired signs to sigma and
  sigma*(-1)^(i*j). Encode a sign and accepted setting into a payload using
  (setting 0, sign +)→1, (0,-)→-2, (1,+)→2, (1,-)→-1. These payloads are fixed
  before and independent of the actual x,y choices. The local C2 predicate
  selects one setting on each side. This intentionally tests whether a
  conditional score can look nonlocal while the full data remain local.

No result is called a Bell violation of the physical model merely because
the conditional reader exceeds two. In particular a cone condition and
apparently nonsignalling selected marginals do not by themselves remove
the detection/sampling loophole.

Reference: J.-A. Larsson and R. Gill, *Bell's inequality and the coincidence-time
loophole*, EPL 67 (2004), 707–713, https://arxiv.org/abs/quant-ph/0312035.
Our fixed-trial C2 selection control concerns detection/sample selection;
we deliberately do not introduce a setting-dependent coincidence-time window.

## Extension: randomness at measurement and squared amplitudes

Added after the initial cone audit, before running the new reference controls.
Check local stochastic response probabilities on the fixed grid
{0,1/4,1/2,3/4,1}; distinguish this finite check from the analytical bound for
all probabilities. No particular structural complexity measure is supplied
by the model. Any local complexity-to-probability map remains subject to the
same conditional-locality assumptions.

Calibrate the existing `build_born_router(kappa=1, form='mirror')` on arm
pairs (1,1), (1,i), (1,-1), (2,1), with the two real/imaginary components
retained explicitly. Exhaust all 36 pairs of initial detector remainders.
Compare both squared input intensities and actual binary click counts to
the normalized Born ratios; retain zero- and double-click trials. Do not
identify quotient magnitude with the number of detector events.

Add a separately labelled external Born-rule reference. Represent a singlet
by integer amplitudes [[0,1],[-1,0]]. Use A0=identity, A1=[[1,1],[-1,1]],
B0=[[3,1],[-1,3]], B1=[[3,-1],[1,3]], with their common scale removed by exact
probability normalization. Multiply amplitudes before squaring; do not enter
the desired correlations as a table. Compute exact CHSH and all marginals.
Draw 20,000 outcomes per setting with seed 20261111, only when both actual
arrival times from the unit-packet Engine control have been reached. No
random numbers are consumed before measurement. Retain all trials.

This quantum reference ASSUMES Born's rule and uses a joint distribution
depending on both settings. It is not implemented by the local Rule3 tensor,
does not feed it, and is not a proof of emergent collapse or information
preservation of a new stochastic Engine. Amplitudes and sampled tickets are
retained as reference data. The Engine retains its own exact inverse.

## Connecting the amplitude calibration to arrival

After the initial static calibration, repeat the same four states with the
existing `build_fibre` and `build_gated_pair` constructors. On L=9 each arm
starts two edges from the central detector. Prepare both complete histories
for directed transport. The real and imaginary components arrive at update
two; the detector reads that old snapshot at update three. Verify no earlier
detector clicks, retain the local amplitude trace, and rewind all seven
gears exactly for all 144 preparations. A retained static marker specifies
the detector site; it supplies neither a time nor an arrival callback.

This declared experimental tensor is not the default UniverseProgram and
does not supply a Born sampler to the Engine. Compare its results with the
initial static calibration without rewriting that historical run.
