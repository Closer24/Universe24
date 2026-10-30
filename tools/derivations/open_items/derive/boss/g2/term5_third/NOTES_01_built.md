# Working notes 01: what is built on node-live (2b8a81bb3), and the mirror's swap on the edge

## The state and the act (src/tensor24/engine/step.py)
- State (a, b, s, r_d, k): now count, before count, the edge's tooth s within [-D, D) with D = W(a) + W(b),
  the drive's tooth, the click tooth. Momentum on the edge: M_in = 2 D_in (a - b) + s; the gear carries
  n = M_in + 4 push to the next edge and splits it there: n = q (2 D_out) + s+, s+ within [-D_out, D_out)
  by ONE carry from the dial's half (split: q, r = carry(n + D, 2 D, 0); s+ = r - D). a+ = a + q, b+ = a.
  So M_out := M_in + 4 push = M_in of the next round, exactly.
- push = s F + K, F the Meshes' pull (grip x (neighbour - own) summed over six Spokes), K = T_k s q_d,
  q_d the drive's quotient of J = J1 + J5 at T_d (T_d = T_k = s = 1 on the loader's lay: q_d = J, r_d = 0).
- J5 = stress(): the push's plan contracted on the readings (value, D_x, D_y, D_z, force, sigma_in, sigma_out,
  unit), sigma_in = split(M_in, 2 rest, 2) = the momentum in whole turns of the REST dial 4 rest (the centred
  split: the nearest whole, ties up), sigma_out the same of M_out = M_in + 4 (s F + K(J1)). For the matter rows
  J1 = 0 and J5 lands on no matter row, so the stress's M_out is the matter's exact next M_in.
- Teeth W = rest + (clock's read of a): every row reads the square's 00 slot except the 00 row itself (acyclic
  cut; the 00 row's teeth stand at rest). Grips: grip_rest + the ii slot of the Mesh's axis at BOTH ends.
  rest = 6 grip_rest (six Spokes): c^2 = grip_rest / rest = 1/6.

## The push's plan (runner/load.py pushing())
For each matter pair (rows o, w through the A1 form; light = A1 x 2 parts: pairs (0,0) and (1,1), entry 1):
T00 = S (si si + so so), S = Spokes x senses = 12; T_ij = D_i a D_j a; T_0i = (si + so) D_i a; J = 2T - eta T.
Slot pushes, per unit strength: 00 by +S J00 = 144 (si^2 + so^2) + 12 |Da|^2; ii by -J_ii = -12 (si^2 + so^2)
- (D_i a)^2 + sum_{j != i} (D_j a)^2; jk by -J_jk = -2 D_j a D_k a; 0i by -J_0i = -2 (si + so) D_i a.
Factor f = entry x matter[train] x strength x square[target]: the strength is the file's "chosen": {"push"}.
NOTE: with T = v (x) v, J = 2T - eta T = 2 x the canonical massless scalar's stress tensor (T^can = v v -
eta (v.v)/2), so J00 = kinetic + gradient energy (x2), J_ii = 2 T^can_ii: the continuum's.

## The mirror and the swap (derived here, measured in probe_e)
Even row: (a, b, s) -> (b, a, -1 - s). Then M_in' = 2 D_in (b - a) + (-1 - s) = -M_in - 1, and the centred
half-open split gives sigma' = -sigma EXACTLY (n -> -1 - n maps q -> -q and s -> -1 - s, since -1 - s stays in
[-D, D)). Checking untick(tick s) = s: the mirrored round's now slot is a (the same), its M_in'' = -M_out - 1
and M_out'' = M_in'' + 4 F(a) = -M_in - 1. Hence the mirrored round reads
    (sigma_in'', sigma_out'') = (-sigma_out, -sigma_in):
the push's plan must be invariant under the SWAP of the two stride planes with both negated, up to the target's
parity sign (00, ii, jk even: the same push; 0i odd: negated push, its count negated by the mirror). That is
hypothesis (e). Rule (b) (an even count of odd legs counting the target) is NOT sufficient: sigma_in^2 alone passes
(b) and maps to sigma_out^2.
On an even row the run back needs push'' = push (then n'' = -M_out - 1 + 4 push = -M_in - 1 -> q'' = -q).

## Measures in the shipped probe (tools/derivations/open_items/derive/boss/term5_edge/probe.txt)
hand at rest: 0 of 10,800 slot-rounds moved; dust: 00 : ii momenta 12 : -1 remainder 0; moving hand under the
push 40 rounds: untick(tick) 40 of 40, the 24 at 24 for rounds 1-6; light rows' board sums of P kept 41 of 41;
the 0i parity taken even breaks the run back 0 of 12.
