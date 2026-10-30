# Final reading of term 5 (fourth text), hostile mathematician

Code read: step.py, contract.py, mesh.py, state.py, kinds.py, carry.py, load.py, run.py, rewind.py, main.py, files.py.
Text read: TERM5_FOURTH.md. Probes read: t5_lib, probe_e/g/m/r/w.

## First observations from the code (before any run)

1. split(n, d, senses): q, r = carry(n + d, senses*d, 0); return q, r - d.
   So n + d = q (2d) + r, r in [0, 2d) -> n = q 2d + (r - d), s = r - d in [-d, d). OK.
   Mirror of n -> -1 - n: (-1 - n) + d = -(n + d) + 2d - 1 = -(q 2d + r) + 2d - 1 = (-q) 2d + (2d - 1 - r),
   with 2d - 1 - r in [0, 2d). So q -> -q, r -> 2d - 1 - r, s -> d - 1 - r = -1 - (r - d) = -1 - s. OK exact.

2. gear(): n = senses*(d_in*(a-b) + senses*push) + s; q, kept = split(n, d_out, senses); return a+q, a, kept.
   D_in = wa + wb at the state (a, b). D_out = wa + W(first) where first = the 00 row's own next count.
   NOTE: in act(), D_out = wa + weight(gearing, clock, first) where first is the FULL state's "first" (all rows),
   computed with d_out = d_in. weight reads the 00 slot of `first` into every row. Hmm: first = gear(a, b, tooth,
   wa+wb, wa+wb, push, senses)[0] for ALL rows; then weight(gearing, clock, first) = rest + read(clock, first): only
   the 00 row's component of `first` is read (clock reads first row of square train, into every row but itself).
   For the 00 row itself D_out = wa + rest... wait: weight for 00 row = rest + 0 = rest, and wa for the 00 row = rest.
   So the 00 row's dial is always 2 rest at both ends: D_in = 2 rest, D_out = 2 rest. OK consistent with the text.
   For another row: D_out = W(a) + W(a+) where a+ is the 00 row's next count. Since the 00 row's own next count is
   computed with its own dial (2 rest, unchanged), `first` for the 00 row equals a1 for the 00 row. OK.

3. mirror(): tau = 2*even - 1 (+1 even, -1 odd). State(tau*b, tau*a, tooth - even*(2*tooth + 1), rd + even*(flip(rd,T)-rd), flip(k,key)).
   Even: (b, a, -1 - s, T-1-rd, key-1-k). Odd: (-b, -a, s, rd, key-1-k).

4. THE CRUCIAL QUESTION for the run back under the push: the stress() at the mirrored state must reproduce
   the push with the right sign. In stress(): m_in = 2 (wa + wb)(a - b) + tooth; m_out = m_in + 4 push, where
   push = driven(gearing, force, kick(first)) with first = drive(j1, teeth, rd)[0] -- this is J1's drive quotient
   WITHOUT J5. Then sigma_in = split(m_in, 2 rest, 2)[0], sigma_out = split(m_out, 2 rest, 2)[0].
   Then the FULL j = j1 + stress; q = drive(j, teeth, rd); push_full = driven(force, kick(q)).
   But the matter rows: j5 lands only on the square's rows (target rows are the metric's). So for matter rows
   j = j1 and push = s F + K1 exactly as used in stress's m_out. Good: for the matter rows M_out as read in stress
   IS the actual M_out. For the metric's rows, stress reads them only through... hmm, does the push read the metric
   rows' strides? f = entry * matter[train] * strength * square[target]: only pairs (one, two) of matter trains.
   So sigma of metric rows is never read (factor 0). OK.

5. Mirrored round, on an even matter row: state (b, a, -1 - s). D_in'' = W(b) + W(a) = D_in (teeth read 00 slot
   of the mirrored state's now slot = the forward state's... wait. W is read at `a` and `b` of the mirrored state.
   Mirrored now = b_fwd_next = a_fwd (the forward's now). Hmm, let me be careful. The forward round takes
   (a, b, s) -> (a1, b1=a, s1). The mirrored state of the result is (b1, a1, -1 - s1) = (a, a1, -1 - s1).
   Its M_in'' = 2 (W(a) + W(a1)) (a - a1) + (-1 - s1) = -(2 D_out (a1 - a) + s1) - 1 = -(2 D_out q + s1) - 1
   = -n - 1 where n = 2 D_out q + s1 is the forward's split dividend... the forward's n = 2 (D_in (a-b) + 2 push) + s
   = M_in + 4 push = M_out. So M_in'' = -M_out - 1. Hmm! Not -M_out. And the text says
   (sigma_in'', sigma_out'') = (-sigma_out, -sigma_in). With the centred half-open split, split(-1 - n) = -split(n)
   exactly, so sigma_in'' = -sigma_out exactly. And M_out'' = M_in'' + 4 push'' = -M_out - 1 + 4 push''.
   For the mirrored round to run back we need push'' = push (even target), so M_out'' = -M_in - 1 and
   sigma_out'' = -sigma_in exactly. This is consistent IF push'' = push on the matter rows: push on the matter rows
   = s F + K1, F = pull at the now slot (same now slot a, same grips since grips read the now slot's ii slots... but
   WAIT: the grips read the ii slots of the metric at the now slot. In the mirrored state the now slot is a_fwd (the
   forward's now), so the ii slots at a are the forward's ii at `a`. Same. OK.) and K1 = kick(drive(j1, T, rd'')) with
   rd'' = T-1-rd on even rows... for T_d = 1 nothing. For T_d > 1: j1 (the notch's potential; 0 as strength 0).
   Fine.

   BUT: the pull F on the matter rows reads the matter's neighbours at `a`  -  same. OK, push'' = push on matter rows.
   And the metric's 00 row: push on the 00 row = s F00 + K(J5 + J1). The mirrored round's J5'' must equal J5
   for the 00 row to run back: J5'' is the plan on the mirrored readings: (a same, D_i a same, F same,
   sigma_in'' = -sigma_out, sigma_out'' = -sigma_in). Plan invariant under that -> J5'' = J5. That's (e).

6. HOLD ON. There is a subtlety: stress() computes m_out with push = driven(force, kick(first)) where first =
   drive(j1, teeth, rd). In the mirrored round, rd'' = T - 1 - rd (even) and the drive's carry is
   carry(j1, T, rd''). For T_d = 1, rd = 0 always and the quotient is j1. Fine at T_d = 1. At T_d > 1 the
   quotient of (j1 + T - 1 - rd) div T vs (j1 + rd) div T differ in general! For the run back the drive's
   quotient must be ... hmm, the drive's "run back" on an even row: forward: j + rd = q T + rd'. Backward with
   flipped tooth: j + (T - 1 - rd') = ? We need the backward quotient to be q (the same, since the backward
   gear's dividend is -M_out - 1 + 4 push'' and needs push'' = push) and the backward remainder to be T-1-rd.
   j + T - 1 - rd' = j + T - 1 - (j + rd - qT) = qT + T - 1 - rd = q T + (T - 1 - rd). Since T-1-rd in [0,T),
   quotient q, remainder T-1-rd. 

   So with the same J the flipped tooth returns the same q and the flipped original tooth. This is the
   "flip" law. Note it needs the SAME J, i.e. J'' = J. And `first` (the J1-only drive) in stress() is computed with
   rd'' and j1'' = j1 (j1 reads the now slot only; even rows). Fine: first'' = first. But WAIT: that holds for the
   carry with the FINAL remainder rd' flipped. In stress(), `first` is the quotient of carry(j1, T, rd)  -  using the
   state's rd  -  and the mirrored state's rd is flip(rd', T) where rd' is the forward's post-round remainder of the
   FULL j = j1 + j5, not of j1 alone. So first'' = carry(j1, T, T-1-rd')[0] where rd' = (j1 + j5 + rd) mod T.
   Forward first = carry(j1, T, rd)[0]. These are NOT equal in general when j5 != 0 mod T! But at T_d = 1 both
   are j1. So at T_d > 1 on a pushed row (the metric's rows), the `first` used inside stress differs between the
   forward and backward rounds... but does `first` matter for the metric's rows? stress reads sigma only of the
   MATTER rows (factor 0 otherwise), and on the matter rows j5 = 0, so rd' = (j1 + rd) mod T and first'' = first.
   OK so it's fine, because the matter rows take no J5. Unless a matter row is pushed  -  hypothesis (d) forbids.
   Fine.

7. What about the odd rows (0i slots) at the mirrored state: (-b, -a, s). Their M_in'' = 2 (W(-b)+W(-a)) (-b + a)
   + s. Hmm: W(-b): the teeth of a 0i row = rest + c00 read at the now slot of... the clock read reads the 00 slot
   (an even row) which in the mirrored state is the forward's `a` in the 00 row (swapped). Wait: the metric's 00
   row is even so the mirrored state's 00 row is (b00, a00, ...) -- I mean mirrored now = forward's a1? Let me
   redo: forward (a, b) -> (a1, a). Mirror: even rows (a, a1, -1 - s1), odd rows (-a, -a1, s1).
   For an odd row: M_in'' = 2 (W_now'' + W_before'') (-a_odd + a1_odd) + s1 where W_now'' = rest + c00 at the
   mirrored now = rest + a_00 = W(a) in the fwd; W_before'' = rest + a1_00 = W(a1). So D_in'' = D_out (fwd). And
   M_in'' = -(2 D_out (a1 - a)) + s1 = -(n - s1) + s1 = -n + 2 s1 ... hmm, that's not right. Let me recompute:
   n = 2 D_out q + s1, q = a1 - a. So 2 D_out (a1 - a) = n - s1. M_in'' = -(n - s1) + s1 = -n + 2 s1.
   Hmm, that's wrong. Let me recheck with the formula M_in = 2 D_in (a - b) + s: for the mirrored odd state,
   a'' = -a (the forward now negated), b'' = -a1 (the forward next negated), s'' = s1.
   M_in'' = 2 D_in'' (a'' - b'') + s'' = 2 D_out (-a + a1) + s1 = 2 D_out q + s1 = n. So M_in'' = n = M_out (fwd).
   And then the backward round: n'' = M_in'' + 4 push'' = n + 4 push''. For run back we need the backward split to
   give q'' = -q... wait. Backward: a1'' = a'' + q'' = -a + q''. After mirroring back (negate and swap): the
   recovered "before" = -(a1'') ... let me think. Backward state after the round: (a1'', b1'', s1'') = (-a + q'',
   -a, s1''). Mirror (odd): (-b1'', -a1'', s1'') = (a, a - q'', s1''). We need this = (a, b, s): so q'' = a - b
   and s1'' = s. So the backward dividend n'' must satisfy n'' = 2 D_in (a - b) + s = M_in, with D_out'' = D_in
   (the dial of the backward split = W(a'') + W(a1'') = W at 00 of... the backward's a1'' for the 00 row is the 00
   row's own backward next count = b_00 (if the 00 row runs back), so W(a1'') = W(b); D_out'' = W(a) + W(b) = D_in.
   OK). So we need n'' = M_in: n + 4 push'' = M_in = n - 4 push, so push'' = -push. The odd row's push must be
   NEGATED: push = s F + K. F'' on the odd row: the pull reads neighbours' counts of the odd row at now'' = -a
   -> F'' = -F (grips the same since they read the even ii slots at the now slot a... wait, the grips read the ii
   slots of the mirrored now, which for the even ii rows is a_ii (fwd now). Same. Good, F'' = -F.) And K'' = kick
   of the drive quotient of J'' at the kept tooth rd' (odd rows keep the tooth): we need J'' = -J to give
   q'' = -q: j + rd = q T + rd'; -j + rd' = -qT + rd. Yes, so with J'' = -J exactly and the tooth kept the drive
   gives q'' = -q and remainder rd. 

   So the odd row needs J5'' = -J5 on the 0i target: that is the "target's parity sign" in (e). The 0i terms:
   -2 (si + so) D_i a. Mirrored: (-so - si) D_i a = -(si + so) D_i a -> J'' = -J. Good.
   And a term reading an odd row's count: the count is negated in the mirror. Fine, consistent with the text.

8. Now the subtle point about the dividend: the text's proof says "M -> -1 - M" on even rows  -  I verified
   M_in'' = -M_out - 1 and that requires sigma_in'' = -sigma_out via split(-1-n) = -split(n). On the odd row
   M_in'' = +M_out exactly (no -1), since the tooth is kept and the counts are negated. Does the stress read odd
   rows' strides? No (factor 0). Fine.

9. The T_d > 1 case with an odd row: the drive on an odd row keeps the tooth and needs J'' = -J. But the drive's
   quotient feeds the kick K = s T_k q_d. The dividend n'' = M_in'' + 4 (s F'' + K'') = n + 4(-sF - K) = M_in. OK.
   BUT what about `first` inside stress() for... not relevant (matter rows only).

10. A possible gap: the 00 row's teeth and the 0i rows. The 0i row's dial D = W(a) + W(b) reads the 00 slot, fine.

11. Now the things to BUILD to break: 
   (i) T_d > 1 with J1 != 0 (the notch) and T_d > 1 on matter rows: `first` in stress is carry(j1, T, rd)[0]; in the
   backward round rd'' = T-1-rd' with rd' = (j1 + rd) mod T (matter rows take no j5). first'' = (j1 + T-1-rd') div T
   = (j1 + T - 1 - (j1 + rd - q1 T)) div T = (q1 T + T - 1 - rd) div T = q1. OK equal. Fine.
   But j1 on matter rows: the notch pushes only the square's rows. So j1 = 0 on matter anyway. Fine.
   (ii) Is there an issue when the push plan reads the FORCE of a matter row (plane 4)? The force F at the now slot
   is the same in the mirrored round (even row). Fine. 
   (iii) The grips read the ii slots at the NOW slot only: held(layout, a). In the forward round the pull on a matter
   gear uses grips at a (now). Backward: grips at a'' = a (fwd now). Same. But the DIAL D_out = W(a) + W(a1) uses the
   00 slot at both; the grips use only the now slot. The pull F enters the momentum as 4 s F: forward F(a), backward
   F(a)  -  same. OK.
   (iv) The window promise (grips within [0, W])? Not a run-back issue.
   (v) THE 24: a turn that negates a row flips its tooth... the commit says the tests' turn written for T_d=1.
   
12. What about the 00 row's own next count `first` computed via gear(a, b, tooth, wa+wb, wa+wb, push, senses)  -  it
   is computed for ALL rows with d_out = d_in, but only the 00 row's component is used (through the clock read,
   which reads the square's first row). For the 00 row d_in = d_out = 2 rest always. So `first[00]` = a1[00]. OK.
   But hmm, what if there are TWO square trains? Then the clock read reads both 00 slots into every row but each's
   own... each 00 row reads the OTHER square train's 00 slot! Then the 00 row's teeth are NOT at rest: the cut is
   only of its own row. With two square trains, row 00 of train A has W = rest + c00(B), and row 00 of B has
   W = rest + c00(A). Then `first` for A's 00 row is computed with d_out = d_in = W_A(a) + W_A(b), but the true
   a1 for A's 00 row is computed with d_out = W_A(a) + W_A(first) where W_A(first) = rest + first_B00, and
   first_B00 is itself computed at the wrong dial... This is a "two square trains" case. The shipped world has one.
   The text says "the 00 row's own teeth at rest (the acyclic cut)". With two squares the cut is not acyclic
   (A reads B, B reads A). Is it a legit case? The loader allows any trains. Note it as a MINOR gap of the theorem
   statement: "the clock's reads acyclic" is a hypothesis, listed. Two squares break acyclicity  -  but the text lists
   acyclic reads as a hypothesis, so it's covered. Would the run back break? Let's test: that would be a case
   where the hypothesis is stated and load-bearing. Not a finding against the theorem, though it IS a finding
   against the loader+act if the run back then fails silently. Test it maybe.

13. MORE IMPORTANT: ties at the edge. s in [-D, D) with D = W(b) + W(a)  -  the promise is checked from outside
   before each round (run.promised). After a round, s1 in [-D_out, D_out) by construction, where D_out = W(a)+W(a1).
   Next round D_in = W(a1) + W(a) = D_out. Same. OK so the promise always holds after the first round. Good.
   But for the MIRRORED state's promise: s'' = -1 - s1 in [-D_out, D_out) iff s1 in (-D_out - 1, D_out - 1] i.e.
   s1 in [-D_out, D_out - 1]: yes since s1 in [-D_out, D_out). Fine.

14. The ii-slot/grip: the grips in the pull are held(layout, a) = grip_rest + ii(a_here) + ii(a_neighbour).
   The text says "grip = grip_rest + 2 ii" for uniform. OK.

15. -1/12 = -c^2/2 "derived": the claim is delta W / rest = 12 J/(6 grip) = 2J/grip and delta grip/grip = -2J/grip.
   But the 12 is `scale = n * senses = 6 * 2 = 12` in load.pushing: whole = scale^2 f on 00 from sigma^2 terms,
   less = -scale f on ii. The ratio of the 00 push to the ii push for dust is scale^2 f S... wait: T00 = S (si^2 +
   so^2) with S = 12 and the 00 slot takes +S J00 = 144 (si^2 + so^2) f; each ii takes -J_ii = -12 (si^2+so^2) f.
   So ratio 12 : -1 in counts. The "derivation": one count of c00 is 1/rest of a dial (W = rest + c00); one count
   of ii is 2/grip_rest of a grip (grip = grip_rest + ii_here + ii_there = grip_rest + 2 ii for uniform).
   delta W / rest = 144 X / (6 grip) = 24 X / grip; delta grip / grip = -2 * 12 X / grip = -24 X / grip. Equal and
   opposite: gamma = 1. OK so the 12 : -1 gives gamma = 1 since rest = 6 grip and the Mesh has 2 ends:
   rest/2 = 3 grip... hmm: for gamma = 1 we need (delta W / W) = -(delta grip / grip), i.e. P00 / rest = 2 P_ii /
   grip => P00 / P_ii = 2 rest / grip = 12. Yes. So -1/12 = -(grip/rest)/2 = -c^2/2 with c^2 = grip/rest = 1/6.
   This is DERIVED given (i) the slots' units (W = rest + c00, grip = grip_rest + ii both ends), (ii) rest = 6 grip
   (the loader: rest = len(spokes) * grip), (iii) the requirement gamma = 1. But WAIT: is gamma = 1 required by
   the push's form J = 2T - eta T, or is it the CHOICE of the slot ratio? The text says: "One coupling pushes the
   00 slot's momentum by 12 J and each ii slot's by -J (load.pushing: whole = scale^2 f, less = -scale f)". The
   factor S = 12 on T00 = S(si^2 + so^2) and then the 00 slot takes +S J00: that's S^2 on the 00 slot and S on ii
   for dust. Where does "the 00 slot takes +S J00" come from? The text: "the 00 slot pushed by +S J00 (its unit the
   teeth), each ii, jk and 0i slot by -J (its unit the grips)". The S in "+S J00" is a CHOSEN relative factor
   justified by the units: 1 count of c00 = 1/rest of the dial, 1 count of ii = 2/grip of the grip. To push both by
   equal relative amounts needs the count ratio rest/(grip/2) = 12. So the S on the 00 slot is "derived" from
   gamma = 1 being the target. Is gamma = 1 derived or imposed? In GR, gamma = 1 follows from the field equations.
   Here the push law J = 2T - eta T is chosen (the linearized Einstein equations' trace-reversed source), and
   the relative unit conversion is... the claim "equal in each slot's own relative unit"  -  this is the statement
   that h_00 and h_ii are pushed by J00 and J_ii in the same units. In linearized GR, box h-bar_{mu nu} = -16 pi G
   T_{mu nu}; with h-bar = h - eta h/2, so box h_{mu nu} = -16 pi G (T - eta T/2). The text's J = 2T - eta T =
   2(T - eta T/2). So J IS the trace-reversed source. Then gamma = 1 follows IF the 00 and ii slots are pushed by J00
   and J_ii in the same unit (h_00 and h_ii in the same metric units). And the unit conversion count-to-metric is
   what the "12" encodes: c00 counts -> h_00 = c00/rest ... and ii counts -> h_ii = 2 ii / grip. The lowering of
   the index (teeth are -g^00, grips are g^ii) handles signs. So: the 12 is the count unit conversion, which is
   derived from the loader's W and grip definitions, and the claim is then a derivation. But there's a hidden
   conversion: is h_00 = -c00/rest exactly the right normalization vs h_ii = 2 ii/grip? g^00 = -1/N^2... With
   N^2 = rest/W = 1/(1+u): g_00 = -N^2 = -1/(1+u) ~ -(1 - u), so h_00 = u = c00/rest. g^ii = grip/grip_rest ...
   hmm, c^2 = grip/W: light's speed squared = grip/W. The spatial metric g_ii = 1/(grip/grip_rest)? If light's
   speed c^2 = grip/W in lattice units, with both g_00 = -rest/W... Let me define: ds^2 = -N^2 dt^2 + A^2 dx^2,
   light: A^2 dx^2 = N^2 dt^2 -> c^2 = N^2/A^2 = (rest/W)/A^2. The measured c^2 = grip/W => A^2 = rest/grip (xconst).
   With grip = grip_rest(1 - 2 ii/grip_rest)... A^2 = rest/grip = (rest/grip_rest)/(1 - v) ~ 6(1 + v) with
   v = 2 ii_count... wait sign: ii is negative, grip = grip_rest + 2 ii < grip_rest. So A^2  proportional to  1/(1 - |v|) ~ 1 + |v|,
   h_ii = |v| = -2 ii/grip_rest. And h_00 = u = c00/rest. gamma = h_ii/h_00 = (-2 ii/grip_rest)/(c00/rest) =
   -2 ii rest/(grip_rest c00) = -12 ii/c00 (with rest = 6 grip_rest). gamma = 1 <=> ii/c00 = -1/12. OK consistent,
   the probe's gamma_slot = (grip_rest - grip)(rest + c00)/(grip c00)  -  this is (2|ii|/grip)(W/c00)  -  hmm, that uses
   grip (pushed) and W (pushed) rather than rest values; at first order the same. Fine.
   BUT: is the "clock's rate N^2 = rest/W" right, given the act? The clock's period^2 ratio was measured = W/rest
   exactly. And light's speed^2 = grip/W measured. So c^2 = grip/W and N^2 = rest/W; the spatial metric A^2 = N^2/c^2
   = rest/grip. So g_ii  proportional to  rest/grip, g_00  proportional to  -rest/W. h_ii = -delta grip/grip_rest (first order) = -2 ii/grip_rest,
   h_00 = c00/rest... wait g_00 = -rest/W = -1/(1+u) ~ -(1-u) so h_00 = +u (h_00 = g_00 + 1 = u). And g_ii = rest/grip
   normalized to 1 at rest: grip_rest/grip = 1/(1 - 2|ii|/grip_rest) ~ 1 + 2|ii|/grip_rest, h_ii = 2|ii|/grip_rest.
   gamma = h_ii/h_00 (isotropic, Newtonian gauge h_00 = 2 Phi, h_ii = 2 gamma Phi) = 2|ii| rest/(grip_rest c00) =
   12 |ii|/c00. OK matches.
   
   So the derivation of -1/12: DERIVED from (W, grip definitions; rest = 6 grip; J the trace-reversed source with
   equal units on slots). The "equal units" is the content; it's the statement that the metric slots are pushed by
   J_{mu nu} in the same metric unit for 00 and ii. Fine, I'd accept it as derived GIVEN the identification of the
   slots' metric units. The "two-ended Mesh" is the factor 2 in grip = grip_rest + ii_here + ii_there.

16. Now the probe_w Green's function: (-Delta) G = N delta_0 - 1, sum G = 0. The static equation: grip Delta c00 = -P
   (per the text "grip Delta c00 = -P"). Hmm, let me re-derive. The 00 row's gear: n = 2(D (a-b) + 2 (sF + K)) + s;
   with D = 2 rest, the velocity v = a - b; momentum M = 2 D v + s = 4 rest v + s; M+ = M + 4 (F + P) where P = K =
   the drive's push (T_d=1: K = J). Static: M = const -> F + P = 0 -> grip Delta c00 + P = 0 -> grip Delta c00 = -P.
   Wait F = sum grip (nb - own) = grip Delta c00 (lattice Laplacian, grips at rest-ish). So Delta c00 = -P/grip,
   c00 = G * P / grip where (-Delta) G = delta. On the torus with mean subtracted: (-Delta) G = N delta - 1 (scaled
   by N, i.e. (-Delta)(G/N) = delta - 1/N). The probe: pred = sum_y P(y) nums[class(x-y)] / (N grip d0). G_true(x) =
   nums/d0 / N. OK so c00(x) = sum_y P(y) G_true(x-y)/grip. Consistent. I'll re-derive G independently (fraction-free,
   e.g. by solving with exact rationals via integers / or by a different method: e.g. Fourier over Z_5^3 in exact
   arithmetic isn't integer... I can solve the 125x125 system with integer Gaussian elimination (Bareiss) on the full
   lattice, no class reduction, and compare to the class numbers. Or verify the class solution satisfies the full
   125-site equation exactly: (-Delta) G = N delta - 1 at every site with sum G = 0. That's a direct exact check.

17. "9402 against 9400": the measured window-mean well vs the Green's prediction with the measured push. This is
   a self-consistency check of the lattice Poisson equation in the mean, it's MEASURED, not derived. Fine.

18. The pass-2 plan invariance: the shipped plan's 76 terms: verify rule_e independently.

## Potential cracks to probe
A. T_d > 1 on the push with the 0i rows (odd)  -  text claims measured 12 of 12 at T_d = 7. Reproduce it myself,
   and ALSO T_d > 1 with the notch (J1 != 0) and the push together (J1 on the 00 and ii slots, J5 too).
B. A moving clock with the 0i slots moving (not standing): the 0i rows' dial D = W(a) + W(b)  -  fine.
C. Two square trains (the clock read then not acyclic): the run back may fail. The theorem lists acyclicity, but
   the LOADER allows two squares and the act has no guard -> a silent failure of "information does not vanish".
D. Ties at the edge: s = -D exactly and s = D - 1 exactly; mirrored -1 - s = D - 1 and -D. Fine by construction.
   But a tooth laid by the setting at s = D - 1 with a then-changing W: the dial at the next round is D_out, the
   split is at the new dial. The tooth is "kept" as a number; the promise is checked at D_in = W(a) + W(b) of the
   state as the round reads it. Fine.
E. The 24 under the push: a turn of the cube acting on the state should commute with the act. The push plan's
   covariance: T_0i -> under a turn that negates axis i, D_i a -> -D_i a and the 0i slot (T1) -> -; jk slots (T2)
   -> sign*...; ii -> permuted. The text claims "the 24 at every round". I can test: apply a turn g to the state
   (permute sites and rows by the kinds' matrices), act, compare with act then turn. Need the row action: 00: 1;
   0i: T1 matrix; ii: the axes' permutation (t1*t1); jk: T2. And the tooth: "a turn that negates a row flips its
   fine tooth in its teeth by the same sign law"  -  hmm, for the edge tooth s, negating the row's counts: n -> -n
   means s -> -1 - s? For the edge split: -n at dial 2D: -n + D = -(n + D) + 2D = -(q 2D + r) + 2D = (-q) 2D + (2D - r)
    -  r' = 2D - r, which is in (0, 2D]  -  NOT in [0, 2D) when r = 0. So a negated row's tooth is -s... let me see:
   s = r - D; -n = (-q) 2D + (2D - r) = (-q) 2D + (D - s) and D - s = -s + D so s' = -s when -s in [-D, D), i.e. s in
   (-D, D]. At s = -D: -s = D not in range; -n = (-q)2D + 2D = (-q+1) 2D + 0 -> s' = -D, q' = -q + 1. So the tooth
   ties at s = -D break the exact negation symmetry of the split. Since the mirror uses -1 - s (the half-open law
   matched to the mirror), the sign-flip symmetry (the 24's turns that negate a row) is NOT exactly compatible with
   the half-open split when s = -D, OR when... hmm, actually let me recompute: n = q 2D + s, s in [-D, D). -n =
   -q 2D - s. For -n to split as (-q) 2D + (-s) we need -s in [-D, D) i.e. s in (-D, D]. s = -D fails, s = D is not
   possible. So at s = -D, split(-n) = (-q + 1, -D)... hmm wait: -n = -q 2D + D = (-q) 2D + D, and D is not in [-D, D)
   so = (-q + 1) 2D + (D - 2D) = (-q+1) 2D - D. So q' = -q + 1, s' = -D. So "24 of 24 for rounds 1 to 6" with the
   turns "once a turn that negates a row flips its fine tooth in its teeth by the same sign law"  -  what does "flips
   its fine tooth" mean for the edge tooth under a turn? If the turn maps s -> -1 - s (the mirror's flip), then
   -n - 1 = (-q) 2D + (-1 - s), which is exact. But the state negated with s -> -1 - s is not the "negation" of the
   state: the momentum M = 2 D v + s -> -2 D v - 1 - s = -M - 1, not -M. The act is then NOT exactly covariant under
   the 24 with plain negation; it's covariant under "negate and flip" which is an off-by-one. Under the turn the
   dividend n = 2(D v + 2 push) + s; turned: -2(Dv + 2 push) - 1 - s = -n - 1 -> q' = -q, s' = -1 - s. So with the
   tooth flipped the turned act is exact. This is a consistent twisted action. Hmm, OK: the 24's action on a state
   includes the tooth flip for negated rows. That is an odd but consistent definition; whether it is "the 24 hold" is
   a matter of definition. For the odd rows and the mirror they use "kept", for the turns they use "flipped"  -  the
   mirror composes (negate counts, swap, keep tooth) and the turn (negate counts, flip tooth). Composition of a turn
   and the mirror on an odd row: negate twice = identity on counts, swap, flip tooth: = the even mirror. Consistent!
   Good: so the group action is consistent. I'd note this as sound but a definitional subtlety.

F. The dust probe G1: are all sites alike (uniform)? Yes ("spread 0").

G. probe_r: the recurrence is "the act's own": is it? For the 00 gear: n00 = m00 + 4 p00 split at 2 REST dial
   (split(n, 2 REST) -> dial 4 rest). p00 = 144*2*900*strength = PUSH_PER_STRENGTH * strength: assumes si = so = 30
   exactly at every round: si = split(m_in, 2 rest)[0] where m_in = 2 (W(a)+W(b)) (a-b) + s for the matter: a - b =
   30 at the start with s = 0 and W = rest: m_in = 4 rest * 30 -> si = 30 exactly. Then m_out = m_in + 4 push
   (push = 0 on the matter: uniform -> F = 0). so = 30. Next round: the matter gear's n = m_in = M_out (push 0) -> 
   n = 4 rest * 30 split at the new dial 2 D_out = 2 (W(a) + W(a1)) = 2(2 rest + c00 + c00+) -> q = (4 rest 30 + D_out)
   div (2 D_out) ... a - b = q < 30 as W grows; but m_in next round = 2 D_out q + s1 = n = 4 rest * 30 exactly (the
   momentum is kept). So si = split(4 rest 30, 2 rest) = 30 always. Yes P00 constant. OK the recurrence is right.
   But that is the dust: the velocity drops as the clock deepens but the momentum stays. Fine.

H. Check -12 ii/c00 = 999 at u = 1 permille  -  the departure from 1000 is a notch effect? -12 ii / c00 where c00 is
   the sum of q00's; ii is the sum of qii's with the ii dial growing. At u small the ratio should be ~1000 - 12u/... 
   whatever. Fine, measured.

I. The claim "gamma -> 1 on pushed slots": gamma_slot = 1001, 1015, 1030... at u = 1, 10, 20 permille. The deviation
   1015 at u = 10 permille is 1.5% at 1% depth: the second-order coefficient is ~1.5 (gamma ~ 1 + 1.5 u). Compared to
   (1+u)/(1-u) ~ 1 + 2u. Is the departure a lattice/dial artifact (claimed: the ii gear's moving dial)? The recurrence
   reproduces the act so the act's own arithmetic gives 1 + 1.5u. Whether "gamma = 1 at first order" is right: 
   gamma(u) - 1 = 1.5 u -> at first order in u the deviation vanishes as u -> 0. OK. But hmm, actually is gamma = 1
   exactly "derived" or is it a first-order statement of a non-covariant lattice dynamics? It's the latter: the second
   order is admitted OPEN. Fine.

J. The G3 1 + gamma measurement: 2050 at u = 20 permille vs 2040 expected (2/(1-u) = 2.0408): +0.5% off; at u = 50:
   2100 vs 2105; at 200: 2370 vs 2500. The claim "1 + gamma = 2 at first order" within 0.5-1%: with light's period^2
   ratio 1041 vs the clock's 1020: 1 + gamma = 41/20 = 2.05. The numbers are permille-rounded: 1041 could be
   1040.5-1041.5, 1020 could be 1019.5-1020.5 => ratio in [40.5/20.5, 41.5/19.5] = [1.976, 2.128]. So the measured
   1 + gamma at u = 0.02 is 2.05 +- 0.08 from rounding alone. The claim "2050 against 2040" is within the rounding
   noise; the resolution does not support a 3-digit statement. MINOR: the reported digits exceed the measure's
   resolution (permille of a ratio near 1, differenced). The 20-period measurement of 311878 permille rounds vs
   305645: the ratio^2 = (311878/305645)^2 = 1.04125 -> 1041; the clock's (634311/628057)^2 = 1.02003 -> 1020.
   So 1 + gamma = 0.04125/0.02003 = 2.059. The interpolation of zero crossings in permille rounds is itself an
   approximation (linear interpolation of a sinusoid: error ~ (step)^3...). With period 15.28 rounds and 20 periods
   the interpolation error per crossing ~ O(0.01 round)? So the period is known to ~1e-4 relative, the ratio^2 to
   ~2e-4, so 0.0412 +- 0.0002 and 0.0200 +- 0.0002 -> 1 + gamma = 2.06 +- 0.02. So "2050 vs 2040" is consistent
   with 2 at the 3% level, not better. At u = 0.05: 1105 vs 1050 -> 0.105/0.050 = 2.10 vs 2/(0.95) = 2.105. 

K. The dispersion: the standing wave's period on a 6-site ring is NOT the continuum's: omega^2 = 4 c^2 sin^2(k/2)
   with k = 2pi/6: the lattice's; the ratio under the metric change: both light and clock measured at the SAME mode
   so the ratio of periods^2 is grip_rest/grip x W/rest for light (speed^2 = grip/W)  -  the dispersion cancels in
   the ratio. OK.

L. "the clock's period^2 ratio = W/rest exactly": 1020, 1050, 1200  -  the spring's omega^2 = g/W: the clock gear's
   n = 2(D v + 2 J1) + s with J1 = -g a... the dial D = 2 W (uniform) -> the equation: W (a+ - 2a + a-) ~ -g a
   (with momentum kept). So omega^2 ~ g/W. Period^2  proportional to  W. Yes = W/rest. OK derived & measured.

## Things to actually run
1. Rerun all five probes (reproduce outputs).
2. My own T_d > 1 test with the push on all slots AND with the notch strength nonzero AND the hand moving AND the
   0i slots moving (not standing), at several T_d, several rounds. Also with a laid rd != 0 on the odd rows.
3. Two square trains -> run back? (acyclicity hypothesis load-bearing; the loader permits it).
4. Verify the Green's function exactly on the 125-site system.
5. Verify rule (e) on the shipped plan by my own independent code (e.g. by symbolic evaluation: evaluate the plan
   on random readings with the swap applied and compare J'' vs sign * J numerically on integers).
6. The ii-slot/jk/0i push signs  -  check the plan's terms against the formula in the text: J_ii = -12(si^2+so^2) -
   (D_i a)^2 + sum_{j != i} (D_j a)^2 ... wait: J = 2T - eta T. T = trace: eta^{mu nu} T_{mu nu} = -T00 + sum T_ii
   (signature -+++). J_ii = 2 T_ii - T = 2 T_ii + T00 - sum_j T_jj = 2 (D_i a)^2 + S(si^2+so^2) - sum_j (D_j a)^2 =
   S (si^2 + so^2) + (D_i a)^2 - sum_{j!=i} (D_j a)^2. And the text says each ii takes -J_ii = -12(si^2+so^2) -
   (D_i a)^2 + sum_{j!=i} (D_j a)^2. OK consistent. J00 = 2 T00 - eta_00 T = 2 T00 + T = 2 T00 - T00 + sum T_jj =
   T00 + |Da|^2 = S(si^2+so^2) + |Da|^2. The 00 slot takes +S J00 = 144 (si^2 + so^2) + 12 |Da|^2. Matches text.
   Check the code's blocks: 00: whole = S^2 f on (so,sw) and (to,tw) [si*si, so*so], half = S f on (go, gw) [D_i a
   D_i a summed over i] -> +S J00. ii: less = -S f on si^2, so^2; back = -f on (go,gw) [-(D_i a)^2 for the SAME i]
   -- spread(go, gw, back, qii): go has shape (pairs, d), gw (pairs, d), qii (pairs, d): for each i: -f (D_i a)(D_i a)
   onto ii_i. Good. other: f * [axes differ] on (goo, gww, qii[:,:,None]): goo (pairs,1,d)... goo = grad[:, None, :]
   * rows + o[:, None, None] -> shape (pairs, 1, d); gww same; other shape (1, d, d) [axis i != j]; qii[:, :, None]
   (pairs, d, 1). Broadcast: (pairs, d, d): index [p, i, j]: first = goo[p, 0, j] = D_j, second = gww[p, 0, j] = D_j,
   factor = f lit(i - j), target = qii[p, i]. So + f (D_j a)^2 onto ii_i for j != i. Good.
   jk: back on (ao, bw) and (bo, aw) onto qjk: qjk[p, i] = the shear slot named by its third axis i; after[i] = (i+1)
   mod 3, before[i] = (i+2) mod 3: -f D_after D_before (twice, from the two orderings: ao*bw + bo*aw = 2 D_a D_b for
   the SAME pair one, two... wait o and w are the pair's two rows (the matter's part rows). Hmm: pairs_of gives
   (one, two) = each pair of rows of a train through the A1 form; for the light train with kinds A1 and part 2, the
   form is 1x1 so one = two = ... let me check: dim = 1 for A1, entry runs over the 1 entry (x=i=0), parts: each
   entry once per part: one = first + 0 + offset, two = first + 0 + offset, offset 0..1. So pairs (r0, r0) and
   (r1, r1) with entry form[A1,0,0] = c. Then so = sigma_in of r0 and sw = sigma_in of r0 (same row). So si*si of
   each part separately; and T_ij = D_i a D_j a per part. The jk slot: -f (D_after a)(D_before a) x 2 (two
   orderings). -J_jk = -2 T_jk = -2 D_j a D_k a. Good. 0i: back on (so, gw), (go, sw), (to, gw), (go, tw) onto q0i:
   -f (si D_i + D_i si + so D_i + D_i so) = -2 f (si + so) D_i a = -J_0i with J_0i = 2 T_0i = 2(si+so) D_i. Good.
   
   So the plan matches the text's formulas. Note what "T_0i = (sigma_in + sigma_out) D_i a" is: a product of the
   stride (velocity in rest-dial turns) and the gradient; in the continuum T_0i = -rho v_i ... with T00 = S(si^2 + 
   so^2) ~ 2 S v^2 and T_0i ~ 2 v D_i a: the relative normalization of T00 to T_0i is S : 1 /(... ) hmm. For a scalar
   field T_{mu nu} = d_mu phi d_nu phi - ...: T00 = (phi_dot)^2 + ..., T_0i = phi_dot d_i phi, T_ij = d_i phi d_j phi.
   Here phi_dot ~ sigma (velocity per round in rest-dial units: sigma = (a - b) x (D_in/(2 rest))... roughly
   sigma ~ v W/rest... For T00 = S sigma^2 (x2 for in and out) vs T_ij = D_i D_j: in the canonical form T00 =
   phi_dot^2 + |grad|^2)/2 ... they said "twice the canonical massless scalar's stress", J = 2T - eta T with T = v(x)v,
   v = (sqrt(S) sigma, D_i a)? Then T_0i = sqrt(S) sigma D_i, not sigma D_i. The text's T_0i = (si + so) D_i a lacks
   the sqrt(12)... that's the "36 : 6 : 1 candidate against the second text's root"  -  the 0i unit is OPEN (P-7).
   The physicist flagged that. The unit of the 0i slot is admitted OPEN. OK, but what about the consistency of the
   four-vector v = (sigma, D_i a) if T00 = S sigma^2 means v_0 = sqrt(S) sigma  -  then T_0i = sqrt(S) sigma D_i and
   T_ii = D_i D_j: the "S" is the conversion of a stride in rest-dial turns to a gradient in counts per site:
   c^2 = 1/6 = grip/rest: a velocity of 1 turn/round in dial units... c = 1/sqrt(6) sites per round in lattice
   units? Light's speed^2 = grip/W = 1/6 at rest in (sites/round)^2. So d_t phi in units of c dx: (d_t phi)/c = 
   sqrt(6) sigma... but sigma itself is (a-b) x 2D/(2 rest).(1/2)... let me compute: m_in = 2 D_in (a - b) + s,
   sigma_in = m_in / (4 rest) rounded = (a - b) D_in / (2 rest) at rest = (a - b) (2 rest)/(2 rest) = a - b. So
   sigma = a - b = d_t phi per round. d_t phi / c = sqrt(6) (a - b) -> (d_t phi/c)^2 = 6 sigma^2. The text has
   T00 = S (si^2 + so^2) = 12 (si^2 + so^2) ~ 24 sigma^2 (for si = so) and T_ij = D_i a D_j a where D_i is the
   centred difference over 2 sites: D_i a = a(x+1) - a(x-1) = 2 d_i phi. So T_ij = 4 d_i d_j phi. T00 = 24 sigma^2 =
   4 x 6 sigma^2 = 4 (d_t phi / c)^2. OK so T00 : T_ij = 4 (d_t/c)^2 : 4 d_i d_j  -  consistent with v = 2 (d_t/c,
   d_i) and T = v v (times 1, both "2"s). Then T_0i should be 4 (d_t phi/c) d_i phi = 4 sqrt(6) sigma d_i = 
   2 sqrt(6) sigma D_i. The text has (si + so) D_i = 2 sigma D_i: short by sqrt(6) = sqrt(S/2)... They said the
   0i unit is OPEN. OK so T is NOT v(x)v for one four-vector v: T00 and T_ij are, but T_0i is not (off by sqrt 6).
   Hmm, wait. Let me redo: S = 12 and T00 = S(si^2 + so^2). With si = so = sigma: T00 = 24 sigma^2. And 
   (d_t phi/c)^2 = 6 sigma^2 so T00 = 4 (d_t phi/c)^2. T_ij = D_i D_j = 4 d_i d_j. So T = 4 (d phi)(d phi) with
   d = (d_t/c, d_i). T_0i = 4 (d_t/c) d_i = 4 sqrt(6) sigma d_i = 2 sqrt(6) sigma D_i. Text: T_0i = 2 sigma D_i.
   Ratio sqrt 6. So the text's "With T = v (x) v this J is twice the canonical massless scalar's" is FALSE for the
   0i components as built: a T with T00 = 24 sigma^2, T_ij = D_i D_j and T_0i = 2 sigma D_i is not of the form
   v (x) v for any v (v(x)v requires T_0i^2 = T00 T_ii: (2 sigma D_i)^2 = 4 sigma^2 D_i^2 vs T00 T_ii = 24 sigma^2
   D_i^2 (dust-like...). So T_0i^2 = T00 T_ii / 6. Not rank one. That's the "36 : 6 : 1" story: the physicist's
   P3/P-7  -  with sqrt 6 irrational, no whole-number v exists; the 0i slot's unit is OPEN. The text admits the unit is
   OPEN but ALSO claims "With T = v (x) v this J is twice the canonical massless scalar's stress tensor"  -  an
   overclaim as to the 0i slots. I should flag: the built T is not rank-one; it is v(x)v on the 00 and ij blocks, and
   on the 0i block it is off by the factor sqrt(S/2) = sqrt 6, which can't be whole: the 0i slot's push is NOT the
   stress tensor's T_0i in the same unit as the others. This is a MINOR (admitted OPEN as to "unit") but the
   sentence "this J is twice the canonical massless scalar's stress tensor" is overclaimed. Also S/2 = 6: and
   their "36 : 6 : 1 candidate": pushing 00 by 36?, 0i by 6, ii by 1  -  i.e. squaring everything to avoid the root. 

   ALSO the trace: T = -T00 + sum T_ii: this uses the 0i blocks not at all; so J00, J_ii, J_jk are self-consistent
   as 2T - eta T for the (00, ij) blocks; only J_0i = 2 T_0i is in question. OK.

M. Check "the 0i slots' largest count 45" in probe_w vs expectation: sigma_out = A/6 = 5? The neighbour's pull: F at
   a neighbour of the centre = grip x (A - 0) = grip A (only the centre differs) -> 4 push = 4 s F = 4 grip A;
   m_out = m_in + 4 grip A = 0 + 4 grip A -> sigma_out = split(4 grip A, 2 rest = 12 grip) = (4 grip A + 2 rest)
   div (4 rest) = (4 A grip + 12 grip) div (24 grip) = (4A + 12) div 24 = (120 + 12) div 24 = 5. OK A/6 = 5. Fine.

N. "the books exact by windows": 4(grip_rest Delta sum_w w + sum_w P) = the 00 momentum's change: M+ = M + 4 (F + P);
   F = sum grip (nb - own) with grip = grip_rest + ii_here + ii_there: they use grip_rest only and claim "the ii
   slots' part of the grips is below a permille here" but then they report 0 permille in all windows  -  the books
   with grip_rest alone can't be EXACTLY 0 unless the ii part contributes less than the rounding... they compute
   permille(|books|.sum(), 4 * denom) with denom = sum |P - mean P| ~ 6.5e26 x ... the ii-part: ii ~ -749 counts,
   Delta w ~ 1e4 counts, product ~ 1e7 counts vs P ~ 1e26: negligible. So "0 permille" is trivially true because
   the push P is 1e26 and the residual's deviation is 1e7: the books test is 20 orders of magnitude too coarse to
   see anything but the P-term. Hmm, but what are the books testing? grip Delta w + P - mean P = dM/4 (mean subtracted):
   this is the act's own identity M+ = M + 4(F + P) with F = grip_rest Delta w + (the ii part). The check is the
   identity up to the ii part, measured at permille of P. Since |dM/4| ~ |P| ~ 1e26 and F ~ grip x 1e4 ~ 1.5e26
    -  comparable. So the check does verify that F + P - dM/4 = ii-part ~ 1e7 << 1e26 x 1e-3. Fine, it's a sanity
   check of the identity at permille level; "exact" is an overstatement: it is exact to the permille of P, not bit
   for bit. MINOR wording: "the act's books exact"  -  it's an identity of the act (M+ = M + 4(F+P)) which holds bit
   for bit by construction; the probe checks it only to permille with grip_rest in place of the grips. I can check
   it bit for bit myself including the ii part of the grips.

O. The theorem's statement: "exact at every W of at least 1 from every such s and r_d, the clock rising or
   falling." Potential crack: W(a+) must be >= 1 for the split's dial: D_out = W(a) + W(a1) >= 1 -> fine if each
   W >= 1... The promise is checked outside. If the 00 slot goes below -rest + 1 at any site (W <= 0) the carry
   divides by <= 0: the runner's promise catches that before the round. The mirrored state's dial = D_out of the
   forward; fine.

P. ANOTHER potential crack  -  the `first` computation in act() for the 00 row: `first, _, _ = gear(a, b, tooth,
   wa + wb, wa + wb, push, senses)` then `weight(gearing, clock, first)`: the clock read reads row `first[00]` into
   every row but 00. For the mirrored round the 00 row's next count must be the forward's b00  -  it is if the 00
   row runs back, which it does (its dial is fixed at 2 rest both ways, needs push'' = push on the 00 row: J5'' =
   J5 (hyp e) and F'' = F (same now slot)). Yes.

Q. The ii slots and the GRIPS in the dial? The dial D = W(a) + W(b) reads the 00 slot only. Fine.

R. The wave window: grips within [0, W] per sense: with the push lowering the grips and raising W: fine.

S. What about the odd rows' momentum read "sigma" (never read, factor 0)? Fine.

T. What if the matter train is itself odd-parity? The parity array `even` is 1 for all rows except the square's 0i
   rows. A matter train with kinds T1 (a vector) is even under time reversal as built -- fine, time reversal of a
   vector field: depends on physics; whatever.

U. probe_e's run_back: `moved = int(abs(states[-1].a[2:] - s0.a[2:]).sum())` assumes the metric's rows are 2..11
   (the light's are 0, 1). OK for this universe.

V. The dust G1 at u = 200 permille: -12 ii/c00 = 911: the ratio falls 9% at u = 0.2; gamma_slot 1337 vs
   (1+u)/(1-u) = 1500. The text says "the second order is the ii gears' own, not the sign's". Fine  -  admitted OPEN.

W. The claim "a hand at rest sources nothing": si = so = 0 when a = b, s = 0 and F = 0 (uniform)? With a gradient
   (tent) at rest: T_ij = D_i D_j nonzero -> J00 = |Da|^2 pushes the 00 slot even for a static field. "a hand at rest
   sources nothing" means uniform at rest. The tent at rest DOES source (M-7). OK consistent.

X. Hmm, the 00 row's teeth: the text (sec 0) says "W = rest + the 00 slot, into every row but the 00 row (acyclic
   cut; its teeth stand at rest)". And M-8 finds the 00 wave superluminal by sqrt(W/rest). OK admitted.

Y. The "moving clock" case in (A) of probe_e: W moves from ...111376 to ...337363762: by 3.2e6 counts over 12
   rounds out of 9e22: u ~ 3.6e-17. The clock "moves" by 1 part in 10^17. The run-back test under a moving clock is
   thus trivially at the "notch" level: the dial D changes by ~3e6 out of 1.8e23: the momentum's re-split changes
   q only when the tooth crosses a boundary... The strides are ~30 so n ~ 4 rest 30 ~ 1e25; a change of dial by
   3e6/1.8e23 relative ~ 2e-17 changes the quotient only if the tooth is within 1e-17 x n ~ 2e8 of a boundary;
   with s uniformly spread in [-D, D) (D ~ 1.8e23) the chance per gear per round is 1e-15. So the "moving clock"
   in probe_e NEVER actually changes any quotient: the run back under a moving clock is not exercised by probe_e
   in any meaningful way! To really test the run back under a moving dial you need the dial to change by O(1)
   relative per round, or the strides to be huge (as in G1 where c00 moves 1e18 counts a round: u up to 0.2). The
   G1/G3 dust runs do move the clock substantially  -  do they test the run back? probe_g does NOT test run back.
   The shipped probe "the moving hand under the push runs back 40 of 40"  -  at what strength? STRENGTH = GRIP/1000
   -> same 1e-17 regime. So: the theorem's "the clock rising or falling" is proved algebraically (and I verified
   the algebra), but the MEASUREMENT of the run back under a substantially moving clock is absent in these probes.
   I should run my own: run back of the G1 dust at u = 0.2 (30 rounds, c00 moving 1e18+ a round), and of a lump
   at high strength where the dial changes by percent per round. If the algebra is right it will hold; if there's
   a hidden flaw (e.g. in `first`/D_out), it would show there. Let me test that: this is the most valuable test.

Z. One more potential crack in the algebra for D_out: a1 = a + q where q = split(n, D_out)... and D_out = W(a) +
   W(a1[00]): for the 00 row itself a1[00] = first[00] computed with the dial 2 rest = D_in = D_out: fine. For the
   other rows, the dial D_out depends on a1[00] which is computed before. In the backward round, D_out'' = W(a'') +
   W(a1''[00]) = W(a) + W(b[00]) = D_in (fwd). Requires the 00 row's backward next = b00, i.e. the 00 row runs back
    -  which requires push''[00] = push[00]  -  which needs J5''[00] = J5[00] (hyp e) and F''[00] = F[00]. F[00] = sum
   grip (nb00 - own00) at the now slot: the grips read the ii slots of the NOW slot: same in both. OK.
   And q''[00] = -q[00] by the split law at the same dial 2 rest... wait for the 00 row the dial is 2 rest at both
   ends ALWAYS, and the mirrored dividend n'' = M_in'' + 4 push'' = -M_out - 1 + 4 push = -(M_in + 4 push) - 1 + 4
   push = -M_in - 1. Hmm, that is not -n - 1 where n = M_out = M_in + 4 push... wait. We need q'' = -q where q =
   split(n = M_out, D_out). The backward split is of n'' = -M_in - 1 at the dial D_in. But q = split(M_out, D_out)
   and we need q'' = split(-M_in - 1, D_in) = -split(M_in, D_in). Is split(M_in, D_in) = q? M_in = 2 D_in (a - b) +
   s with s in [-D_in, D_in): so split(M_in, D_in) = (a - b, s). And we need a1'' = a'' + q'' = a - (a - b) = b.
   YES: q'' = -(a - b), so a1'' = b, and s1'' = -1 - s, and mirrored back: (b1'', a1'', -1 - s1'') = (a, b, s). 
   So the backward round does not need to "invert the split of M_out"; it re-splits M_in at D_in, which by the
   promise gives back (a - b, s). Clean. The algebra is exact. The theorem holds given: (1) push'' = push on even
   rows, (2) push'' = -push on odd rows, (3) the dials: D_in'' = D_out and D_out'' = D_in (needs the 00 row to run
   back first, and the dial reads of 00 at both slots), (4) teeth >= 1.

   WAIT. One more check of (3): D_in'' = W(a'') + W(b'') = W(a) + W(a1) where "W(x)" means rest + x[00]. = D_out. (ok).
   D_out'' = W(a'') + W(a1''[00]) where a1''[00] = the 00 row's own backward next count = b[00] (ok) (shown above for
   the 00 row since its dial is 2 rest fixed... but hold on, for the 00 row is D_in = D_out = 2 rest ALWAYS? W(00 row)
   = rest + read(clock, a)[00] and the clock read's factor for (first = 00, landed = 00) is lit(0) = 0, so yes
   W[00 row] = rest always, D = 2 rest.) (ok).

   So the theorem is right for the act as built with one square train. With two square trains the 00 rows read each
   other and the dial of each 00 row depends on the other's next count, which `first` computes at the WRONG dial
   (d_out = d_in)  -  then weight(first) is not the true W(a1) and the state's tooth might not even be in the dial
   that the next round reads. That would break the run back AND the promise. That's the "acyclic" hypothesis, which
   the loader does not enforce. Test it: a universe with two metric trains.

AA. ANOTHER crack: the metric's 0i rows are odd, but what about the clock read landing on the 0i rows (M-2 says
   it holds). The 0i rows' W = rest + c00: the dial reads an even row's count into an odd row's teeth. In the mirror
   the odd row (-b, -a, s): D_in'' = W(mirrored now) + W(mirrored before) = (rest + a00) + (rest + a1_00) = D_out (ok).

AB. The theorem's claim about T_d > 1: "the drive's negated source carries at the kept tooth by the carry's sign
   law": -j + rd' = -q T + rd: from j + rd = qT + rd' (ok). But in act(), there are TWO drive calls: first = drive(j1, T,
   rd) used for `first` inside stress's m_out (matter rows: j5 = 0 so fine), and q = drive(j, T, rd). On an odd
   target row, J'' = -J where J = j1 + j5. j1 on the 0i rows: the notch pushes the 00 and ii slots only ("the E part
   and the shears get none")  -  0i gets none. So j1[0i] = 0 and J'' = -J needs j5'' = -j5 (ok).
   On an EVEN row with T_d > 1 the notch's j1 (00 and ii slots) + j5: J'' = J (ok) (j1 reads the now slot, even rows).

AC. What about the matter's `first` at T_d > 1 when the MATTER has j1 != 0? The notch has strength 0 or acts on
   squares only. There's no plan on matter (G3). So j1[matter] = 0 and first = 0, m_out = m_in + 4 s F. Fine.

AD. The 24 at every round under the push: let me test it myself (the row action on the metric's slots and the
    tooth flip under negation). Lower priority.

AE. The G3 "light" measurement: the light replaced on the metric's state with the strides r = 0 and b = a: a
    standing wave with zero initial velocity; the metric frozen (strength 0). Does the metric move during the light
    run? Strength 0 -> no push; the metric's own act: the 00 slot uniform -> F = 0 -> the metric stands. (ok).

AF. The dust push: the 00 slot's push at stride 30 at each site, with F = 0 (uniform), W rises uniformly: c00 =
    a R(R+1)/2  -  c00 after R rounds given constant push p00: M grows by 4 p00 each round: M_R = 4 p00 R; q_R =
    M_R/(4 rest) ~ p00 R/rest; c00 = sum q ~ p00 R(R+1)/(2 rest). OK.

Let me now run things. Priority:
 1. Rerun the probes as given (reproduce).
 2. My probe A: run back under a strongly moving clock (dust at u = 0.2, 30 rounds; a lump at high strength) with
    T_d = 1 and T_d = 7, with the 0i slots moving (laid non-zero velocity), with the notch on.
 3. My probe B: two square trains.
 4. My probe C: the Green's function verified exactly at 125 sites; and the window numbers reproduced.
 5. My probe D: the plan's (e) checked numerically; the T_0i non-rank-one observation documented.
 6. My probe E: the 24 under the push.
 7. The books bit for bit with the full grips.
