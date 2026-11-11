# From amplitudes to clicks: what is implemented and what is assumed

> Historical research/reference document. The current supported interface and acceptance status are defined in [ONE_SYSTEM.md](ONE_SYSTEM.md). Commands and default-model descriptions below refer to the earlier construction; see [the 0.6 migration](MIGRATION_0_6.md). No general ≤48-channel physical model is accepted.


The local wave really delays the detector until arrival. That fact does not
yet supply a Born probability law or a Bell violation. This audit separates
the actual Engine events from an explicit quantum reference.

```bash
python -m experiments.quantum.bell_cone_audit --out runs/bell-born-cone
python -m unittest universe24.tests.test_bell_born_reference -v
```

The [declared protocol](../experiments/quantum/BELL_CONE_PROTOCOL.md) records
the settings, source controls, readers and reference assumptions. Results are
in [the evidence file](evidence/bell_born_cone.json). No production tensor,
seed API, runtime or click classifier changes in this follow-up.

## What produces a square on the board?

Represent a local complex amplitude by two retained integers, `psi=a+i*b`.
Its phase-invariant squared norm is `a*a+b*b`, a degree-two integer polynomial
allowed by the engine. For two indistinguishable paths, add their amplitudes
**before** taking the norm:

```text
|psi1 + psi2|^2 = |psi1|^2 + |psi2|^2 + 2 Re(conj(psi1)*psi2).
```

The cross term carries interference. Counting paths, counting clocks, or
adding their separate intensities cannot replace it. Such a coupling remains
local if both path amplitudes have arrived at the same detector. A click is
a recorded outcome; amplitudes and relative phases are inferred from
repeated measurements and interference, not read directly from one click.

The repository already contains this polynomial in `build_born_router` and
its locally gated counterpart `build_gated_pair`. The experiment composes
the latter with four real/imaginary `build_fibre` channels and a retained
detector marker: seven gears on L=9. Each arm starts two edges from the
central detector. The complete initial histories prepare directed transport;
the amplitudes arrive at update two and the detector reads that old snapshot
at update three. There is no earlier detector click, arrival callback or
time-dependent gate. Relative phase is retained during transport. This is
a declared experimental tensor, not an addition to the default runtime.

The missing step is that an intensity input is not automatically a probability
of a binary click. An exact calibration exhausts 36 pairs of detector
remainders, with initially zero detector a,b and the transported amplitudes:

| Arms | Squared output inputs | Born probabilities | Actual binary clicks (36 emissions) |
| --- | --- | --- | --- |
| 1, 1 | 4, 0 | 1, 0 | 36, 0 |
| 1, i | 2, 2 | 1/2, 1/2 | 24, 24 |
| 1, -1 | 0, 4 | 0, 1 | 0, 36 |
| 2, 1 | 9, 1 | 9/10, 1/10 | 36, 12 |

The last row yields a 3/4:1/4 share of clicks, **not** 9/10:1/10; it also has
12 double-click emissions. The `1,i` row has 16 double-click and 4 zero-click
emissions, even though normalizing the click counts hides this problem.
All 144 complete preparations rewind exactly through all three updates.
The reported amplitude traces show zero field at update one, the prepared
complex pair at update two, and zero field again at update three. The input
intensities and click counts match the earlier static calibration; what is
new is the verified local transport and delayed readout. These are calibration
controls, not a claim about every possible detector preparation. Counting a
larger quotient as multiple independent detector events would change the
readout definition and is not used to claim success.

## Cone restriction and Bell sampling

On L=13, the source emits toward two detectors three edges away. Every
nonempty trial first clicks at update three. The detector separation is six,
so neither setting can reach the other detector before the measurement ends.
Source packet triples are identical across all four independent setting
combinations. All complete-state cones, remote-choice controls and rewinds
pass. Trial identifiers and deadlines are fixed before examining outcomes.

The default detector has no physical analyzer angle. The literal unit-packet
case is therefore explicitly a settings-inert control, not a complete Bell
experiment. Additional controls use the same fixed tensor with declared
local marker values 1 or 2; these values are not claimed to represent spin
measurements.

For the deliberately constructed selection-stress source:

| Reader of the same Engine transitions | Included per setting | CHSH S |
| --- | --- | --- |
| Every arrival click, binary sign of quotient | 8/8 emissions | 1 |
| C2-only detection; local nondetection assigned +1 | 8/8 emissions | 3/2 |
| Keep only emissions with C2 at both detectors | 2/8 emissions | 4 |

The last row changes the hidden-source ensemble with the settings. It even
has unbiased, apparently nonsignalling selected marginals. It is a deliberate
detection/sampling-loophole control, **not** an engine Bell result. All its
clicks obey the same cone. A second shared-sign control has no accepted
coincidences for two settings; its conditional CHSH is undefined, not zero.

## Randomness only when choosing

Bell locality does not require physically predetermined outcomes. Let lambda
describe the shared past, including retained structure and past messages. If
the settings are independent of lambda and the two local stochastic choices
factor conditionally, their mean outputs a_x and b_y lie in [-1,1]. Then

```text
|a0*(b0+b1) + a1*(b0-b1)|
  <= |b0+b1| + |b0-b1| = 2*max(|b0|,|b1|) <= 2.
```

Averaging over lambda preserves the bound. It applies to any local mapping
from complexity to outcome probabilities, including fresh randomness drawn
only at measurement. The audit checks all 16 binary local response tables
and a separate exact grid of 625 stochastic models. Neither is claimed to
be a substitute for the analytical statement for continuous probabilities.

No operational complexity measure or derivation of its weights has been
provided here. To identify complexity weights with squared amplitudes would
be an additional hypothesis. Selecting the more complex option alone does
not establish the coherent cross term, Born normalization or Bell statistics.

## Explicit quantum reference: amplitudes first, randomness at measurement

The separate reference starts with singlet amplitudes [[0,1],[-1,0]], applies
the specified local basis matrices, squares the resulting **joint** amplitudes
and normalizes exactly. The correlations are computed, not entered as a
lookup table. It yields

```text
E00 = E01 = -4/5; E10 = -3/5; E11 = 3/5;
S = 14/5 = 2.8.
```

All exact local marginals are unbiased and independent of the remote setting.
Only after both actual Engine arrival times are reached does the reference
consume random numbers. There are 20,000 draws per setting, all retained;
the specified seed produced sample S=2.8037. The full sample log stores the
setting, measurement microtick, random ticket and outcome. Together with
the four retained amplitude arrays in the report, every sampled choice can
be reconstructed. This is a reference sampling check, not an experimental
significance claim or a new inverse law for a stochastic Engine.

**Born's rule is assumed in this reference.** Its joint sampler uses both
settings; it does not implement a Bell-local response factorization, does not
feed Rule3 and does not convert reference draws into engine clicks. The
reported 2.8 is consequently **not** a claim that the local board has derived
quantum collapse or reproduced nature's Bell experiments. The gap remains:
derive an adequate detector probability law and joint-state structure from
the proposed board dynamics, with every changed assumption stated explicitly.

References: [Feynman, Probability Amplitudes](https://www.feynmanlectures.caltech.edu/III_03.html);
[Brunner et al., Bell nonlocality](https://arxiv.org/abs/1303.2849);
[Larsson and Gill, coincidence-time loophole](https://arxiv.org/abs/quant-ph/0312035).
