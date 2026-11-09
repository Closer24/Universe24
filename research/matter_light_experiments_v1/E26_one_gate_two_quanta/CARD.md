# E26 — One gate, two quanta: two separately prepared quanta add exactly until they meet, the gate records the meeting at the update it begins, and the mirror run retraces every click

## On the event board
- coupling (−,+,+) (reference), vacuum (0,0,2), L = 128, T = 80; builder B's single X-gate router as ONE guide_net@1
  placement (registry wave 14): the x- and y-lines through one vacuum gap node X = (40, 40, 20); quantum Q on the x-line
  12 nodes before X, quantum K on the y-line 12 + D nodes before X (D = −8..8), the y-line in gauge s = ±1: 34 members
  (D, s); both unit (1,−1) fibre packets (profile C; fibre light, r04 guide packets, speed 1), separately prepared; for
  D = 8 (2 of the 34 members) the y-line begins at K's lead, so only K's leading cell (0, ∓1) is placed: there K is a
  truncated packet, not a full (1,−1) quantum; nothing acts after t = 0
- runs: 34 members on the board and with K alone; Q alone and the hardware alone per gauge (72 forward runs); 8 mirror
  runs from JR(x_T) (official init files; second forward runs, not rewinds): the 6 meeting members, (5, +), (−6, −)

## In the clicks (decoder 1.0 and log_symmetry_v1; declared: the gate channel (40, 40, 20, 1), exits at distance 3)
- 28 of 34 members: the gate stays silent up to T = 80 and the board log is the union of the branch logs (every record
  of Q alone and of K alone, which share none, and nothing else): the two quanta add exactly
- 6 members meet: the gate's first click records the meeting at (−4, +) 12, (0, +) 12, (4, +) 16, (−2, −) 12 (kind C1),
  (2, −) 14 (C2); (8, −) (K truncated) is a meeting of returning light at t = 58, its first gate record a C0. Exits lit
  in (t_g, t_g + 8]: {x+, y+, y−} for (−4, +), (−2, −), (8, −); {x+, x−, y+} for (4, +), (2, −); {x+, y+} for (0, +)
- C0 on the board: 35 in (−2, −), 37 in (2, −), 1 in (8, −), 0 in the other 31; not decoded: 17 repaid (q, −q) pairs + 1
  unrepaid, 18 + 1, 1 unrepaid; max |a|, |b|: 3 in (−2, −), (2, −), 2 in (8, ±) (additive overlap), 1 elsewhere
- hardware alone: no click; 8 mirror runs: C0 equal, C1 ↔ C2, totals equal, last gate click at 81 − t_g, kind mirrored

## Claim
- owner sentence (r10zh; UPDATE 46 item 33): "One gate, two quanta, 34 prepared arrival offsets. The two quanta add
  exactly, cell by cell, until they meet: linearity below overflow, as for classical waves. 28 of the 34 never meet
  within 80 updates. Where they do meet, the gate records the meeting at the exact update it begins. It records the
  meeting; it does not decide anything. Light then leaves by two or three exits, fixed by the prepared offset and sign.
  Running the board from the mirror image of its final state retraces every click backwards. Every reading reveals
  prepared data: classical hidden-variable behaviour." (its "two quanta" holds for 32 of the 34 offsets; at D = 8 K is
  truncated)
- [SIMULATION] the decoded facts; [THEOREM] additivity below overflow (builder B's T1; its proof confirmed in R10X-1)
  and the mirror (Theorem M, R10ZC-9); reported, not decoded (R10ZH-27): the state is additive cell by cell before t_o
  (34/34) and t_q = t_o in 6/6 (the other 28 members have neither); t_g = t_o in 6/6 (R10ZH-28); the meeting is the only
  source of non-additivity; non-additivity begins at t_o, the first quotient defect; by T = 200 one more meets, at 196
- not claimed: "one quantum takes all paths" (two separately prepared quanta, not a sum over paths); "the click chooses
  a path" (every meeting lights 2–3 exits); a Born rule; anything specifically quantum
- referee: r10zh R10ZH-27..32 CONFIRMED (27 with a wording fix, 28 with scope, 31 on a rerun member); R10ZH-33 PARTLY
  (wording fixes 1–4 applied); fresh machine 2 QM-F15: builder rerun and (a)–(d) CONFIRMED, its fixes 1–4 applied

Reproduce: python -m research.matter_light_experiments_v1.verify E26_one_gate_two_quanta
