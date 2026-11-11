# Reassembly through bounded local memory-controlled rotors

## Declaration before execution

New optional toy model, on unchanged fixed-six Engine; reviewed production
baseline `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.

Fixed grid: L=3 and L=5; routing connected/disconnected; one-site initial
memory intervention present/absent. Run all eight combinations for 160
updates, plus a no-message L=5 control. No search or threshold adjustment.
The intended sector is algebraically bounded to bits and density values
0,1,2; arbitrary retained remainders remain in 0..5. Verify every full step,
first-order invariant, conservation, full inverse, and official click class.
The standard 3/4 compact, <1/2 dispersed hysteresis and structural score are
unchanged. Density is a retained record of message occupancy, not the
independent 48-channel reference physics, so this toy cannot pass that full
research goal by changing labels.

The hypothesis tested is that **bounded retained local memory can alter
future communication and subsequent concentration without growing integer
amplitudes**. It is not yet a stagnation detector or a complexity selector.

## Exact local map and lift

For each of three spatial axes, each bank contains message occupancies
`p,n in {0,1}`, retained memory `m in {0,1}`, and density `R=p+n`.
The local collision is

```text
p' = p + m(n-p)
n' = n + m(p-n)
m' = m + p+n-2pn -2mp-2mn+4mpn
R' = R.
```

Thus messages exchange directions when memory is one, and memory toggles
exactly on odd occupancy. This is receipt-parity memory, not an archive of
all distinct motifs. A second equal visit can erase its visible bit.

The inverse message selector is `1-m'`; the inverse memory is the same
parity polynomial evaluated on the output pair. Proof: if `p=n`, swapping
does nothing and memory stays fixed. If `p!=n`, memory toggles; swapping
according to `1-m'` reverses the original swap. All eight Boolean input
triples are independently enumerated, have distinct outputs and recover
their originals. On unrestricted integers this collision inverse is not
claimed; the common Engine still retains its own general inverse.

Streaming S translates p one edge forward and n one edge backward, keeps
memory at its site and updates density by exact continuity:

```text
R_next = R + p(x-e)+n(x+e)-p(x)-n(x).
```

S is invertible; reversing both shifts reverses this density update. Both
collision and streaming preserve `R=p+n` and total message occupancy. The
two-bank first-order map and inverse are

```text
F(X,Y) = (C(Y), S(X))
F^-1(X,Y) = (S^-1(Y), C^-1(X)).
```

Compile `u=3*(F(b)+F^-1(b))` into the fixed tensor and prepare
`a=F^-1(b)`. Every term is cubic or lower. Collision terms are entirely
on-site; every streaming term reads one face neighbor. There are no old-a
dependencies in this standalone tensor. For arbitrary retained `r in 0..5`,

```text
divmod(2u+r,6) = (F(b)+F^-1(b), r)
b_next = F(b)+F^-1(b)-a = F(b)
a_next = b = F^-1(b_next).
```

The preparation relation is therefore invariant. All r entries stay fixed;
all actual official events are C0. Reversibility is proved on the stated
Boolean map, and also checked through the actual common Engine at every
step. Neither a hidden normalization nor a different denominator appears.
The density stays in `{0,1,2}`, and message/memory values remain Boolean.
The complete orbit is finite for fixed L and r; no unlimited accumulation
is possible within this bit sector.

## Executed fixed-grid results

All nine declared cases completed 160 updates and exact full rewind. No
128-bit guard was reached; retained a/b counters never exceeded magnitude
2. Eight additional nonuniform preparations on L=3/5, routing on/off,
passed eight exact first-order/Engine steps and inverse checks each.

| L | Routing | One-site memory change | Density episodes | Full-state returns in horizon |
|---|---|---|---:|---|
| 3 | disconnected | absent | 0 | Every 6 updates |
| 3 | disconnected | present | 0 | Every 6 updates |
| 3 | connected | absent | 0 | Every 12 updates |
| 3 | connected | present | 0 | Update 84 |
| 5 | disconnected | absent | 16 | Every 10 updates |
| 5 | disconnected | present | 16 | Every 10 updates |
| 5 | connected | absent | 16 | Every 20 updates |
| 5 | connected | present | 15 | None within 160 |
| 5 | connected, no messages | absent | 0 | Every update |

The L=3 concentration never passes the required dispersal threshold. This
does not get reclassified as a failure of transport or as a success of
recurrence. The L=5 disconnected episodes occur at `8,18,28,...,158`;
connected baseline episodes occur at `10,14,30,34,...,150,154`. The memory
intervention shifts later episodes again (for example `74→75` and a later
episode at `116`). None of these schedules is supplied to the law.

The connected baseline's repeated score is `(3,3,0)`. The memory-intervened
case initially has scores `(3,6,1),(3,6,1),(3,4,1),(3,3,0),...`; it loses
persistence and is not componentwise growing. **Every declared case fails
the original cumulative-structure gate.** The complete original goal also
requires an independent reference board and a demonstrated stagnation
trigger; neither is present here.

### Causal attribution

The connected and disconnected versions start from identical complete
seeds in these fixtures, including both histories and all remainders.
The memory intervention changes only one site's retained memory histories.
For both L values:

- With routing connected, message histories first differ at update 2 and
  retained density first differs at update 3.
- With routing disconnected, message and density histories never differ
  over the 160-update observation, although the changed memory is retained.
- Two separately checked 12-update complete-state intervention cones have
  zero changes outside their one-edge-per-update bound and exact rewinds.

This establishes a bounded **memory→communication→density** subgoal and a
change in subsequent concentration. It does not establish novel structure,
physical collapse, a Born probability, or a new physical cosmology. R is a
retained density record of messages; it cannot be used to bypass the
registered exclusion of carrier echoes from independent reference-board
success. No metrics or counter increments were fed back from the host.

## Sensor interface for the separately declared joint experiment

Following the peer review, an algebraically compatible interface is supplied
to the integration owner, without changing the original nine runs. This
section is a specification; the integrated run must be checked separately.

For an independent Boolean alarm s, replace the collision's swap selector
by `h=m XOR s=m+s-2ms`, retain the same occupancy-parity memory update, and
use inverse selector `1-(m XOR s)`. Let `D=n-p`. Relative to the standalone
tensor, the expanded additions are

```text
target comm.plus.axis.X, source bank Y: +3*b_alarm*D -6*b_alarm*m*D
target comm.minus.axis.X:             -3*b_alarm*D +6*b_alarm*m*D
target comm.plus.axis.Y, source bank X: -3*a_alarm*D +6*a_alarm*m*D
target comm.minus.axis.Y:              +3*a_alarm*D -6*a_alarm*m*D.
```

These remain degree 2/3 and on-site. Keep streaming, memory and density
terms unchanged. For an evolving alarm, the exact retained-history lift is

```text
u_rotor = 3*[F_(b_alarm)(b_rotor) + F^-1_(a_alarm)(b_rotor)]
initial a_rotor = F^-1_(initial a_alarm)(initial b_rotor).
```

Cancellation gives `b_rotor_next=F_(b_alarm)(b_rotor)`. The sensor's next a
is its old b, so the preparation relation propagates. Both retained alarm
histories must remain Boolean. A current-only signal, the signed memory
values `-1,+1`, or an unrestricted archive counter is not a valid substitute.
The source→alarm→rotor old-a dependency chain is acyclic. No unproved
backreaction into the source or sensor is included in this interface.

The joint experiment still has to verify the actual expanded tensor,
retimed complete preparation, source independence, domains, local cones,
memory interventions, disconnect controls and exact inverse. A one-update
no-change sensor also remains insufficient to recognize a repeating
period-two source as structurally stagnant.

## Reproduction and records

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/complexity/reassembly_feedback.py --out runs/complexity-research/03-reassembly/verified
```

The final standalone evidence is
`runs/complexity-research/03-reassembly/verified/summary.json`; per-case
directories retain `tensor.json`, full `initial.json.gz`/`final.json.gz`,
all passive samples and message hashes. Source/dependency hashes and every
negative gate are included. The original nine-case run remains under the
parent run directory; later validation added local truth-table and random
sector checks without changing its declared cases or outcomes. The
complete-seed/intervention-cone check is retained separately in
`runs/complexity-research/03-reassembly/local_intervention_cone.json`.

Public coordination, with the user-authorized peer discussion:

- Initial result: https://github.com/Closer24/Universe24/issues/17#issuecomment-6802157441.
- Sensor interface discussion: https://github.com/Closer24/Universe24/issues/17#issuecomment-6802232260.
- Exact expanded-law handoff: https://github.com/Closer24/Universe24/issues/17#issuecomment-6802277905.
