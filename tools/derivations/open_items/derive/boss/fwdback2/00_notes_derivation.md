# Notes 00: the Mesh's tooth on a moving clock (the second text's deriver, 2026-10-30)

Read: the first text (fwdback/), Big Pic's 6532006298 item 2 with p12 and p13 (reader-5 b49d1b4a8, 43fcd2fe2), the
hostile physicist (fb_phys/REPORT.md, P1..P6) and the hostile mathematician (fb_math/REPORT.md, m0..m9).

## The state in (x, P) form

A gear (a, b, r) is a position a and a momentum P = rest (a - b) + r, r in [0, rest): b = a - (P div rest). The act as
built at rest is kick-then-drift: P += push(a) (at the now slot), a += P div rest. The slot mirror (a, b, r) ->
(b, a, rest - 1 - r) is S = Dr o M with M: P -> rest - 1 - P (at fixed a) and Dr the drift; M K M = K^-1 for every
kick K (P += f(a)), M Dr M = Dr^-1, so S (Dr K) S = (Dr K)^-1. Every kick commutes with every kick.

## Why the Mesh's payment forces two changes in the first text

1. A Mesh that pays both ends at one event pays the end whose Node-clock stood: its P moves with a fixed, so its
   before slot b = a - (P div rest) moves on a stood round. The mirror must then reverse that gear's momentum (M),
   not leave it (the first text's mirror leaves a stood Node-clock's gears): without M the backward round pays the
   same pull again with the same sign.
2. The first text's dial D = L(a) + L(b) reads the 00 gear's before slot, which now moves on a stood round (item 1),
   and M moves it again (b -> 2a - b). Theorem 2 (b) ("after a stood round D is unchanged") fails. The dial must read
   only what a stood round leaves: the now slot. D = L(a) + L(a). The mirror's flag is the carry of the tooth flipped
   at the now dial; the tooth is flipped at the pivot's dial, which is the dial of the carry that made it (rule (iii)
   literally), and the backward round reads the forward round's own dial (its pivot is the same count).

## The Mesh's tooth: why its dial must be a count of the structure

The mathematician's three properties that free the escapement: a first-order carry, a push that never exceeds its
dial, a dial that stands still on a stood round. Big Pic's tooth (dial L(i) + L(j), push 2 L_0) has the first two; its
dial moves whenever an END releases while the Mesh stands (the end's 00 slot moves), so on a falling clock its tooth
can stand above its dial: inside Theorem 1's hypothesis (H) again (a remainder at a dial that moves). On a still clock
it is exact (Big Pic's p13).

A dial that stands still in every stood round of the Mesh, whatever its ends do, reads no clock: a count of the
structure. The clock must then come in through the push, per round, whole, local and with no remainder: the only such
reading of the two ends' clocks is their own releases, g_i and g_j (each 0 or 1 by Theorem 2). The dial is fixed by
the uniform clock: where both ends release together the Mesh must release with them, so push 2 fills the dial: 1 + 1.

    h, mu+ = carry(g_i + g_j, 1 + 1, mu)

mu in {0, 1}; push <= 2 = the dial; h in {0, 1} on every state, no domain. Rate (N_i + N_j) / 2, the edge's lapse
(the arithmetic mean; Big Pic's is the harmonic 2 / (1/N_i + 1/N_j); equal at first order in the contrast).

## The round

    g, tau+ = carry(L_0 + L_0, L(a) + L(a), tau)                      per Node-clock
    h, mu+  = carry(g_i + g_j, 1 + 1, mu)                              per Mesh (i, j)
    q_d, r_d+ = carry(g J, T_d, r_d)                                    per gear (J at the now slot)
    q, r+ = carry(rest (a - b) + s (SUM_e h_e G_e (a_e - a) + T_k q_d), rest, r)
    a+ = a + g q;  b+ = a+ - q

At g = 0 and h = 0 the carry returns (a - b, r): the gear stands. Where every h equals its ends' g (the uniform clock
with its teeth in phase) it is the first text's act; at c = 0 the act as built state for state.

## The mirror

    f = carry(L_0 + L_0, D, D - 1 - tau)'s quotient, D = L(a) + L(a)  (did the round that made this state release)
    a -> a - f (a - b);  b -> a_m + (a - b);  r -> rest - 1 - r;  r_d -> T_d - 1 - r_d   (every gear: M; the drift back where f)
    tau -> D_m - 1 - tau with D_m = L(a_m) + L(a_m) (the pivot's dial);  mu -> 1 - mu (flipped at 1 + 1)

untick = mirror o tick o mirror.

## To measure

- The five probes again with the Mesh tooth (fb1 at one Node-clock: the new dial only).
- Big Pic's step (his lay, the engine's floor act), the physicist's P6 steps, the mathematician's 2:1 step.
- The long runs on the hostile lays: P5c A (the board, 1 x 1 x 16, uniform 2 L_0, teeth staggered, 2e4 rounds), P5 B
  (e = 1 .. 1/1000, 2e4 .. 4e5 rounds), P5 C, the smooth well (4e4), m5 A and B (4e4); the non-uniform moving 00 lays
  (P5c B, probe_fb2's own, m6) with the clocks' course and the books every round.
- Mutants: the first text's mirror on the Mesh tooth (stood gears left); the first text's dial (both slots) with the
  Mesh tooth; Big Pic's own-dial tooth on a non-uniform moving clock.
