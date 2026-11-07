# Computation review: prepared signals and click approval

Base: `5894510ada12d22f17a70f93a41ec311aef13265`. All sources, settings and readouts
were fixed before the corresponding trajectories. No engine, tensor construction,
generic component, runner or Presenter source was changed.

## Primary finite correlation audit

The [frozen protocol](protocol.json) has SHA-256
`3c95321cce84de5bec0da1942f27a32d7d25250b68410c3da979203bad2c3e9d`.
One L97 board contains two source–guide–receiver preparations. Receiver positions
are `(32,24,48)` and `(32,72,48)`; their toroidal Manhattan distance 48 exceeds
twice the 16-step observation horizon. Each source starts 8 sites left of its
receiver. The +++ tensor is identical throughout all trials. Settings alter only
the two initial receiver remainders, `(4,0)` or `(0,4)`.

The four source phases are `(a,b)=(0,1),(1,0),(0,-1),(-1,0)`. There are 16
shared-phase trials, 64 independent-phase trials and 4 source-absent controls.
Phase weights are uniform and independent of both settings. These are designed
initial common causes, not a dynamically derived entangled photon source.
Receiver settings are local preparations, not calibrated polarization analyzers.

The fixed outcome is the sign of the first guarded arithmetic quotient at
receiver channel 0 in updates 1..16, or 0 if none. This is a passive trajectory
statistic, not a proved internally persistent signed result. Every trial and
all 48 receiver channels remain in the evidence.

| Ensemble | Full-trial CHSH | Both-click-conditioned CHSH | Joint detection per setting pair |
|---|---:|---:|---:|
| Shared phase | 1 | 2 | 1/2 |
| Independent phases | 1/2 | 2 | 1/4 |
| Both sources absent | 0 | Undefined | 0 |

Conditioning is reported as a selection diagnostic, never as the primary Bell
test. The finite response table is consistent with
`A(x,p)=(-1)^x d(p)`, where `d(p)=1` for phases 0 and 3 and 0 otherwise; B has the
same form. Thus the common phase correlates detection availability. A detected
sign is fixed by its local setting.

All 84 runs completed: 1,428 complete states and 1,344 forward transitions, each with
an exact inverse check, followed by complete-run rewind. Duplicate preparations
reproduced exactly. All 84 grouped comparisons of full local detector trajectories
across the remote setting agreed. All null controls are quiet; none of the
80 detected source-on receiver instances clicked before source distance 8.

All80 detected receiver instances had later C events. None retained constant
`I=a^2+b^2` or constant remainder pair **from its first C through update16**.
This does not deny later finite memory plateaus: the `shared-0-00` receiver has
I=0 through 7, I=1 at 8–9 and I=4 at 10–16; its remainder pair returns to `(4,0)` at 10.
Strict first-click retention is therefore not established by this preparation.

The complete result is [primary_v1/result.json](evidence/primary_v1/result.json).
Every compressed record includes its full assembly/specification, native
Presenter states, complete detector states and actual six-neighbor input sums.

## Secondary autonomous pending/confirmation probe

The separately frozen [protocol](approval_protocol.json) has SHA-256
`395b6fd14ec252330234b2db4f1c843c9453c547b43e3cfa0a4b40a003229063`.
The board is L101, H32, receiver `(50,50,50)` with remainders `(2,4)`, source
offsets −8 and +16. The left source is initially `(0,1)`; the two prospective right
phase controls are `(0,1)` and `(0,-1)`. Every 00/10/01/11 source mask is included:
8 runs, 264 complete states, 256 exact forward/inverse transitions.

Both phase families fail their registered strict approval predicate (0/2
accepted). The actual left-only waveform is a precise counterexample to the
required quiet waiting interval:

| Update | Actual paired input | Channel 0 after update | Channel 14 after update |
|---|---|---|---|
| 8 | `(1,-1)` | `(0,0,4)` | `(0,0,2)` |
| 9 | `(0,0)` | `(0,0,4)` | `(0,0,2)` |
| 10 | `(-2,2)` | `(0,0,0)` | `(0,1,0)` |

The desired pending state is reached, but only for two complete states.
Channel 14 then clicks without the right source. The positive right source alone
also creates repeated clicks; the negative right source alone stays quiet.
Both joint preparations have early/repeated clicks and fail the specified
eight-state confirmed-record retention. Null controls remain stationary and
all full-state rewinds pass.

This rejects these two registered autonomous preparations. It does not refute
the scalar conditional two-kick calculation, which assumes an input sequence
that these full-board waveforms do not supply. It also does not construct an
internal route-computed approval mechanism.

See [approval_v1/result.json](evidence/approval_v1/result.json) for every acceptance
predicate and retained failure.

## Reproduction and actual presentation

From this research checkout:

```bash
python -m research.light_approval.compute --output runs/light-primary
python -m research.light_approval.approval_probe --output runs/light-approval
```

Each output contains a standalone `The_Presenter.html`. The primary includes
eight cases selected before the data; the secondary includes all eight controls.
Both use the existing generic Presenter and complete original states.

The [primary rotating full-cube GIF](evidence/primary_v1/render/sequence-01/recorded-clocks.gif)
shows 17 consecutive recorded states. Its existing renderer verified all eight
cases, every fixed readout and the 48-channel inspector, unchanged retained
state/tensor/readout data, and all eight cube corners inside every frame.
The [render report](evidence/primary_v1/render/report.json) is scoped to jsdom
with native Canvas2D and explicit geometry; it is not Safari/native browser CSS
validation. The uniform stationary background is omitted visually only.

The 92 engine runs took about 8.6 CPU seconds; rendering took 24.24 CPU seconds.
The complete two-study evidence and rendered views occupied 5,107,813 bytes at
completion. No physical entanglement, wavefunction collapse, all-alternatives
exploration, permanent approval latch or physical-light interpretation was
established. The next concrete preparation question is whether an autonomous
guide can supply the required first kick and suppress its premature second kick
while an independent later signal supplies confirmation, under the same rule.
