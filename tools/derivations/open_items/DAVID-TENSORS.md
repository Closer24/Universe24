# The regulator as one symmetric tensor: the law's side

David, 2026-10-27, 15:4x UTC, for the Boss, on the owner's words of 14:32 UTC ("check how tensors help you simplify everything"). Read on the head 608d97134 (regulation.py, tick.py, meshes.py); the scans are in DAVID-TENSORS_CHECKS.txt.

## The ten gears as h_mu_nu

| gears | the part | the source (regulation.py) | under the 48 |
|---|---|---|---|
| 0, time | h_00 with the spatial trace | the hands' forms less the stress's trace | A_1g: fixed |
| 1 to 3, tensions | the traceless diagonal, h_aa - tr / 3 | 3 T_aa - tr | E_g: permuted |
| 4 to 6, fluxes | h_0a | the records' count flux (momentum density) | T_1u: signed permutations |
| 7 to 9, shears | h_ab, a < b | num d_a . d_b | T_2g: the two axes' signs multiplied |

**Ten gears, the trace twice.** The three tensions are sourced traceless, and the spatial trace rides on the time gear. But each tension's write is its own carry, so their sum drifts by the floors: up to 61 at one clock of the hole by tick 60, against tensions of at most 45. So the trace is carried twice, once on the time gear by its source and once on the tensions by their floors. One traceless write would hold the sum at 0: two carries, with the third gear their negated sum. That is a new act, and it moves the charts.

**The 48** act on all of them as h -> P h P^T, with P the cube's signed permutation matrices.

## What Rule3 reads of it

1. **The time gear:** the clock's rate p_0, through the content. This sets the spring and the reaches.
2. **The tensions:** each spoke's factor Q = (Gamma - t_a)^2 / Gamma^2 (meshes.factors). So the spoke sum SUM_j R_j (m_j - a) is the trace g^ab d_a d_b over the diagonal of the inverse metric.
3. **The fluxes:** the mesh's fold turn (meshes.skewed). h_0a is a rotation of the hand across the mesh, the frame's drag, as a Gaussian factor (w2 + i m).
4. **The shears: nothing.** They are written every tick, and no other gear's act reads them (a scan of every read of the regulator's gears; only the rows' report reads them, DAVID-CLOSE-LAW.md item 7). An axis lattice has no diagonal mesh for them to act on. **A finding:** the off-diagonal metric is booked and never felt.

## The hand's stress

Every source above is one bilinear of the Gaussian hand over its gradients, T_mu_nu = Re(conj(d_mu z) d_nu z):

| part of T_mu_nu | what regulation.py computes |
|---|---|
| T_00 | the forms of the kick |
| T_0a | the flux, a hand's velocity against its gradient |
| T_aa | the tensions' diagonal |
| T_ab | the shears |

As one tensor act this is one source per index pair, and no separate spelling of a tension, a flux and a shear.

## What it simplifies, in whole numbers

1. **One act for the nine axis gears:** the source is T_mu_nu, the write the same carry. The 48 are P h P^T, so their four kinds of test (time, tension, flux, shear) are one.
2. **The trace is the spoke sum.** Rule3 reads only the diagonal and the time part; the fluxes enter through the turn.
3. **The shears are inert.** They are struck, or they need a diagonal reach, the owner's word: on an axis lattice, h_ab can act only through a two-spoke product (a step along a and then along b). That is a new read and changes every chart where the shears stand.

No formula is added. A tensor here is only the index pairs of acts that already stand.
