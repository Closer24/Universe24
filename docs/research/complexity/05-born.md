# Complexity, phase-resolved clocks and Born weights

## Protocol fixed before the run

Base production main: `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
Worktree snapshot: `1e22b18`. No production code is changed. This is a declared
experimental clock/detector tensor plus an analytical probability reference.

We use all 83 multisets of one, two or three initial phases from Z6. A branch
contains unit clocks with phases p_h(t)=p_h(0)+t mod 6. Candidate measures are
declared in advance:

1. Number of histories N.
2. Number of distinct six-step phase histories D.
3. Number of ordered pairs with a persistent phase difference L (including
   self-pairs); for these locked clocks L=N².
4. Signed pair contrast C=(1/2) sum_hk K(p_h-p_k), with the fixed kernel
   K=(2,1,-1,-2,-1,1). This counts equal phase positively, antiphase negatively
   and intermediate phase with smaller signed weights. It is not an unsigned
   count of complexity.

Compare the last measure to an independent exact amplitude calculation in the
triangular basis z=x+y*w, w=exp(i*pi/3), |z|²=x²+xy+y². The phase vectors are
(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1). No floating-point trigonometry is used.

For every ordered pair of the 83 branches, excluding only pairs whose total
reference intensity is zero, compare normalized candidate weights to the
reference q_j/sum q. For postweighting fixed q, evaluate
p_j=q_j*(1+lambda*C_j)/sum q*(1+lambda*C), with lambda in {0,1/4,1}, separately
for the three unsigned measures. Report exact total variation distance,
counterexamples and acceptance denominators. Zero-probability branches are
retained. No C2 postselection, selected settings or Bell experiment occurs.

Controls: common phase rotations; duplicating every clock 2 or 3 times;
adding an antiphase pair to one branch; a three-clock cancelling triad; and a
six-update scan with different local frequencies to distinguish coherent
intensity from time-averaged intensity and persistent unsigned structure.

Engine prototype: every retained clock has two ordinary integer gears with
u=3b. Prepare a=R^-1 b where R(x,y)=(-y,x+y). Six updates implement one local
cycle. Remainders are zero and are NOT identified with phase. A local observer
gear reads the fixed quadratic pair-contrast polynomial; it supplies no
runtime callback. Enumerate six initial detector remainders for every branch,
compare its first-update input and actual event against an independent scalar
oracle, and rewind the complete state. All clocks are already at the local
detector; this prototype makes no new propagation claim.

Run command:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.complexity_born --out runs/complexity-research/05-born
```

The hypotheses being tested are phase-pair intensity, unsigned complexity as
branch weight, and complexity postweighting of an already fixed quantum
state. None assumes that a successful intensity identity derives Born
sampling. A new state produced by a physical complexity-dependent interaction
must instead be compared with the Born probabilities of that new state.

## Results

All 83 signed pair contrasts equal the independently computed amplitude norm.
All 498 common-phase rotations and 166 uniform-history duplication controls
pass. The 6,889 ordered branch pairs contain 25 with both amplitudes zero;
those do not define a normalized reference state. All other 6,864 pairs are
included, including dark individual branches. No detector event is filtered.

| Candidate used directly as branch weight | Mismatches / 6,864 | Maximum total variation |
| --- | --- | --- |
| History count N | 5,892 | 3/4 |
| Distinct phase histories D | 5,964 | 3/4 |
| Persistent unsigned pairs L | 5,820 | 9/10 |
| Signed pair contrast | 0 | 0 |

The last row is a proved intensity identity, not a discovered statistical
law: its physical assumptions are explicit below. Normalizing that intensity
as a probability is still the reference Born rule. The Engine test makes the
distinction concrete: all 498 preparations pass the input identity, the
six-update phase trajectory, and exact inverse after both one and six steps.
Actual detector event frequency remains `min(1,q/3)` under the declared
uniform-remainder ensemble. A working local intensity is not yet exclusive
Born-distributed selection. The detector is an observer; no absorption,
conditional post-measurement state or Bell-locality exception is supplied.

The fixed polynomial has two gears per retained clock and one observer:
3/5/7 total gears for 1/2/3 clocks, respectively. Its degree is at most two,
every factor is at the same node, and it has no old-a input dependencies.
Clock phase evolves autonomously under the ordinary Engine recurrence.
Its sixfold phase is encoded in (a,b); the private remainder r is unchanged
for those clock gears. The prototype does not require or claim C2 events in
the clock sector. Complete information is retained in all clock registers,
not reconstructed from their possibly cancelling aggregate.

### Why the pair construction works

Let `v_p=(x_p,y_p)` be the declared triangular phase vectors and let
`G=[[1,1/2],[1/2,1]]`. The kernel satisfies
`K(p-q)=2*v_p^T*G*v_q`. Therefore summing ordered pair contrasts gives

```text
C_pair = (1/2) sum_hk K(p_h-p_k)
       = (sum_h v_h)^T G (sum_k v_k)
       = x_total² + x_total*y_total + y_total².
```

This is a constructive bilinear mechanism: the local observer polynomial is
the expanded pair interaction. The independent contrast routine counts
phase differences with the six-entry kernel rather than evaluating the
norm formula. Positive total contrast follows even though some pair
contributions are negative.

The input geometry and the pair coupling are assumptions. They have not
been derived from arbitrary information complexity. The phase representation
is natural for an actual six-state clock: with `R(x,y)=(-y,x+y)`,
`R+R^-1=I` and `R^6=I`; prepared `a=R^-1 b` makes fixed-six `u=3b` give
`b_next=R b` exactly. A positive symmetric quadratic form invariant under R
is a positive multiple of G. This motivates the invariant intensity within
the declared phase encoding, but still does not fix a sample space, detector
ensemble or choice probability.

For a quantum-history interpretation the coupling also assumes which
histories are coherent. If different histories leave orthogonal physical
which-path records, the corresponding cross terms need not survive. The
present simultaneously retained classical clock labels do not themselves
derive a quantum environment overlap or decoherence law. Quantum state,
environment and measurement definitions remain necessary [1,2].

### Why unsigned persistent organization is insufficient

Two locked equal-phase clocks have four persistent ordered pairs and q=4.
Two locked antiphase clocks have the same four persistent pairs and q=0.
The locked triad at phases (0,2,4) has nine persistent pairs and q=0. More
histories, diversity or stable relations therefore does not monotonically
increase coherent intensity. The signed contrast is useful physics-facing
correlation data, not a monotonic complexity ranking.

For two clocks with relative drift, the six instantaneous intensities are
4,3,1,0,1,3 and their time average is 2. The persistent unsigned pair count is
also 2, but a fixed-time initial intensity is 4. Averaging requires a
physical integration-time or ensemble assumption; it is not the probability
at every instant. All clocks advancing by one common phase leaves their
contrast invariant. Thus a global common phase alone selects no branch;
relative phases and interactions are the operational quantities.

### Postweighting a fixed state changes its probabilities

| Extra unsigned factor `1+lambda*C` | Mismatches at lambda=1/4 | Maximum TV | Mismatches at lambda=1 | Maximum TV |
| --- | --- | --- | --- | --- |
| C=N | 2,808 | 1/12 | 2,808 | 1/6 |
| C=D | 3,672 | 1/12 | 3,672 | 1/6 |
| C=L | 2,808 | 2/9 | 2,808 | 1/3 |

All counts are over the same 6,864 pairs. All lambda=0 controls match.
For fixed q_j>=0 with nonzero sum and positive factors f_j,

```text
q_j*f_j / sum_k(q_k*f_k) = q_j / sum_k(q_k)
```

holds on every active branch iff f_j is common on all q_j>0 branches.
Zero-amplitude branches impose no restriction on their factor. This exact
ratio statement does not forbid complexity from changing the physical
state first. If a specified interaction changes Psi, use the Born reference
of that changed state and account for the apparatus as part of the model.

A controlled counterexample adds the cancelling phase pair (1,4) to the
history (0). The aggregate amplitude and q=1 are unchanged, while N goes
from 1 to 3, D from 1 to 3 and L from 1 to 9. Against another q=1 branch,
postweighting by 1+N changes (1/2,1/2) to (2/3,1/3). This is a same-state
test only if the extra histories are representational under the proposed
physical decoder; if they are an independently measurable source/apparatus
change, the physical state and its measurement must be specified afresh.

## Handoff and next falsifiable gates

1. Clock/transport: send complete relative-phase data to the interaction
   site, with matched arrival/cone tests. Retain the prepared phase sector
   or prove its stability. Equal unsigned packets at equal and opposite
   phases must remain distinguishable by the signed coupling.
2. Memory: distinguish a record that changes subsequent physical evolution
   or coherence from a post hoc weighting of fixed amplitudes. Test matched
   record/no-record interventions and preserve the full history on rewind.
   Orthogonal path records versus an erased record are a prospective test;
   no quantum overlap rule has yet been built by this prototype.
3. Selection: derive an apparatus ensemble and exclusive outcome mechanism
   whose all-emission frequencies match the intensity ratios. The current
   threshold reader fails that gate even though the pair identity succeeds.
   Do not redefine quotients as event multiplicities or hide double clicks.
4. Bell: a common phase history can be part of the shared source lambda.
   With independent settings and conditionally local outcome distributions,
   it remains within the Bell bound. A proposed exception must identify the
   changed structural premise and preserve operational no-signalling; this
   intensity construction makes no such exception or Bell claim.

The issue handoff is recorded at
https://github.com/Closer24/Universe24/issues/17#issuecomment-6802149413.
It responds to the six-agent coordination and keeps the original physical
G0–G5 and recurrent-burst gates open.

## Sources

[1] Feynman, *Probability Amplitudes*: coherent alternatives add before the
absolute square, https://www.feynmanlectures.caltech.edu/III_03.html.

[2] Preskill, *Foundations I: States and Ensembles* and *Measurement and
Evolution*: quantum rays, composite systems, environment and measurements,
https://www.preskill.caltech.edu/ph219/chap2_15.pdf and
https://www.preskill.caltech.edu/ph219/chap3_15.pdf.

[3] Brunner et al., *Bell nonlocality*, conditional-locality framework,
https://arxiv.org/abs/1303.2849. The phase-kernel identity and postweighting
criterion above are elementary derivations supplied by this experiment.
