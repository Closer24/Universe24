# Compact null-covector geometry

The optional compact experiment retains one integer profile in two transport
banks and reconstructs the prepared pp-wave coframe exactly. It replaces the
**32 coframe channels** of the older construction with **2 profile channels**
on this restricted sector. The old experiment's 12 connection channels and
four signal/clock channels are absent, not compressed into hidden state.
This is a new model, not a full-state refactor of the 48-channel experiment.
The default ADM metric, component assembly and scalar Engine are unchanged.

## Fixed null algebra

Use `eta=diag(-1,1,1,1)`, fixed positive integer `P`, and a fixed nonzero
integer covector `ell` with `ell^T eta ell=0`. Raising the index means
`ell_sharp=eta ell`. Define

    L = ell_sharp ell^T,       L^2 = 0,
    E = P I + F L,             J = P I - F L.

For every integer profile value, including negative and arbitrarily large F,

    E J = J E = P^2 I,         det E = P^4,
    g = E^T eta E = P^2 eta + 2 P F ell ell^T,
    H = P eta - 2 F ell_sharp ell_sharp^T,
    g H = H g = P^3 I,         det g = -P^8.

Thus `E^-1=J/P^2` and `g^-1=H/P^3`. These are passive exact rational
readouts with fixed denominators, not extra Engine divisors, retained
rational gears or feedback into a future state. Invertible E preserves
Lorentzian signature by congruence. It does not guarantee that the chosen
coordinate time is timelike or that constant-t slices are spacelike.

`universe24.algebra.null_covector.NullCoframe` validates these hypotheses
without rounding, normalizing or mutating the caller's inputs. It supports
general integer null covectors, but supplies no propagation or connection
law for them. The compact transport experiment fixes `ell=(1,0,0,-1)`;
generic null directions are algebra tests only.

The shortcut does **not** extend automatically to sums of two null
deformations: for `ell=(1,0,0,-1)`, `m=(1,0,0,1)`, let
`L=ell_sharp ell^T`, `M=m_sharp m^T`. Although `L^2=M^2=0`,
`(L+M)^2` is nonzero. In fact `2I+L+M` is singular. Combining wave
directions requires a separate inverse and nondegeneracy argument.

## Exact fixed-six transport and inverse

Let `(S F)(x,y,z)=F(x,y,z-1)` on the storage cube and

    R(X,Y) = (Y,S X),          R^-1(X,Y) = (S^-1 Y,X).
    u_X = 3(Y+S^-1 Y),         u_Y = 3(X+S X).

These four linear monomials obey strict single-edge support. They read only
the complete old b snapshot. The tensor is fixed before the run; it contains
no clocks, step counter, precomputed future profile or finite computation
horizon. The runner's stop time is an observation choice, not tensor data.

Prepare `b=(F,F)`, `a=R^-1 b=(S^-1 F,F)` and any retained remainder
array `r` in `[0,6)`. Because `u=3(R+R^-1)b`, exact Euclidean division gives

    divmod(2u+r,6) = ((R+R^-1)b,r).

On `a=R^-1 b`, Rule3 therefore yields `b_next=R b`, `a_next=b`,
`r_next=r`. The relation is preserved forward and backward. Two updates
give the full-state identity

    EngineStep^2 Enc_r(F) = Enc_r(S F).

The subscript matters: **remainders remain at their storage nodes**. They
do not translate with a and b, and the geometric decoder cannot recover
them. Every `(a,b,r)` value is preserved in the complete exported trace.
On a periodic L-cube the prepared state returns after `2L` updates (its
minimal period may divide that number), so the prepared run can continue
without increasing its channel allocation. This periodicity supplies no
accumulated structure. All click classes are C0 because the remainders are
fixed; this is not a new C2 production mechanism. Off this sector,
`a=1,b=0` uniformly gives exact
unbounded drift `b_n=-n`; rewind still succeeds.

## Readout and comparison scope

The passive observer accepts coherent macro snapshots and rejects generic
odd staggered or off-preparation states. The audit separately compares the
decoded coframe in **both banks and both retained histories at every
microstep** against the original
[pp-wave experiment](PPWAVE_PALATINI_LOCAL.md). At even steps it also compares
the metric and checks both left and right inverse certificates.

The prepared profile is the original
`F=A(z-t)(x^2-y^2)+2B(z-t)xy`, with
`A(z)=z%5-2`, `B(z)=(2z+1)%3-1`. Equality of the coframe on this
family does not reconstruct independently perturbable connection gears,
clock phases, signals or the older experiment's remainders. No vacuum
equations are asserted for arbitrary input profiles. The transverse chart's
periodic seam failures remain; no new boundary treatment is supplied.

The runner uses the existing channel allocator with owner
`null_wave_experiment`, labels both channels `audit`, and writes its complete
channel manifest, fixed tensor, decoder constants and all snapshots into
`full_trace.jsonl`. It is standalone and does not supply the event board's
physical metric or stress tensor.

## Reproduction and evidence

```bash
python experiments/geometry/compact_null_wave.py --out runs/compact-null-wave
python -m unittest universe24.tests.test_null_covector -v
```

The [source-hashed report](evidence/compact_null_wave.json), at `L=5,P=256`,
compares against the unchanged original experiment from base commit
`ebe4b97e953845390a97ad284bfc0525ccc008d8`:

| Check | Result |
| --- | ---: |
| Compact channels / monomials | 2 / 4 |
| Complete snapshots / updates | 11 / 10 |
| Coframe bank/history/node comparisons | 5,500 |
| Metric/node comparisons | 750 |
| Two-sided inverse/node checks | 750 |
| Coframe or metric mismatches | 0 |
| Full-state cycle and every-step inverse | Exact |
| Nonzero remainders retained in place | Exact |
| Audit click classes C0 / C1 / C2 | 2,080 / 0 / 0 |

Tests independently invert matrices with SymPy, exercise non-axis integer
null covectors and integers beyond int64, replay the entire trace through
the Engine, reject inexact inputs, and retain the two-direction singularity
and off-preparation drift as negative controls. The checked evidence is new;
the original experiment and its historical hashes are not rewritten.

This delivers a compact representation and a reusable inverse identity.
It adds no matter backreaction, physical clock response, general Einstein
evolution or mechanism for recurrent bursts with growing complexity.
