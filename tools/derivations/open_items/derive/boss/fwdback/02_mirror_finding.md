# Notes 02: the mirror of a clock that skips rounds (the finding that fixed the form)

## What probe_fb1's first run showed

The physics of the escapement form was nature's to the permille (A, B, D), but the run back missed on EVERY round the
Node-clock stood (10000 of 30000 rising, 9909 of 28000 falling). Reason: the gears' slots shift only when the
Node-clock steps, so after a stood round the output state's before slot is NOT the round's pivot; the mirror (the
swap) then puts the backward pivot at b, and the escapement's tooth, carried at L(now), was flipped at L(before).

## The dead ends (each checked on paper)

1. A flag "did the last round step" in the state: the backward round regenerates only ITS OWN quotient, never the
   previous round's; the flag is not recovered. Reading the flag off tau (tau < L_0 after a step) needs a compare,
   or lit(tau div L_0): two carries read as a flag, the thing the owner's half-open decision removed from the split.
2. The slots shifting every round (b+ = a) with the velocity as a register u: the as-built backward step rebuilds
   b = a - u, wrong after a stood round (b = a).
3. The stood round folding the momentum into the tooth (a, b, r) -> (a, a, rest v + r): the same act cannot unfold it.
4. A third slot kappa = the position one round ago: an involutive mirror (kappa, kappa + a - b, a), but kappa is the
   flag in another dress and is not recovered backward.
5. Any dial function f(input) = g(output) for both cases forces g constant (f(a, b) = h(a) from the stepped case,
   h(b) = h(a) from the stood case).

## The way out: the escapement's dial symmetric in the two slots (the edge's dial of the clock)

   q_tau, tau+ = carry(2 L_0, L(now) + L(before), tau),  L(x) = L_0 + x00,  the mirror flipping tau at the same
   D = L(now) + L(before) (symmetric: the same number before and after the swap; the mirror an involution).

- Stood round: tau+ = tau + 2 L_0 < D; the swap puts the pivot at b, but on a stood round nothing acts except the
  escapement, whose dial D(b, a) = D(a, b) does not care which end is the pivot: the backward carry gives
  (0, D - 1 - tau), and the final flip at D gives tau. Exact always.
- Stepped round: tau+ = tau + 2 L_0 - D_in in [0, 2 L_0); the swap puts the pivot at a (right); the mirror flips
  tau+ at D_out = L(a+) + L(a); the backward carry at D_out of D_out + D_in - 1 - tau gives q = 1 iff
  0 <= D_in - 1 - tau < D_out, which holds whenever D_out >= 2 L_0 (since the step needs tau >= D_in - 2 L_0); the
  gears un-step at rest (the standing act's lemma); the final flip at D(b, a) = D_in gives tau. Exact in the domain
  L >= L_0 at every slot (D >= 2 L_0: the clock at or below its rest rate).
- q_tau <= 1 in the domain (tau + 2 L_0 < 2 D_in); tau+ < D_out always (2 L_0 <= D_out after a step; D unchanged
  after a stood round).

The clock is read at both slots, forward and backward: time forward and backward is what makes the stood round's
mirror harmless. Steps per round 2 L_0 / (L(a) + L(b)) = L_0 / L at the half step: the same physics, read
time-symmetrically.
