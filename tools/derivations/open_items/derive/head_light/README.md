# The head's light act in Tensor24's terms

The question (the ruling's stage 4, "equal to the head on the light alone, act by act"; the Boss's #2187 comments
6479126486, and Sofer's reading of it, 6479294042): what the head (src/event_universe at 67b765312) computes for its
light, tick by tick, written in the terms of Tensor24's gear.

**The act:** at a Node-clock, for each of the light's two gears (three and twelve, the unsprung hand, ratio (rim, rim)):
- a+ = a + q, b+ = a, with (q, r+) = carry(W (a - b) + (r - home(W, 0)) + s F + home(W+, 0), W+);
- F = sum_j R_ij (a_j - a), a_j the neighbour's now slot as it is;
- that is Tensor24's gear(a, b, r, 0, W, W+, push), the pull's grips s R_ij.

Its integers, each as the head writes it: T = 6 rim Gamma^2 G^2 (core/rule3.py:29-31); W = (T div 2)(X_b + X_n), X
the regulator's time gear (tick.py:209); home(W, 0) = W div 2, the head's mid (core/acts.py:20-22), its gears
holding no going (its going is the tick's direction, +1 forward); s = X_n (tick.py:116); R_ij = 2 rim p_i^2 Q_ij per
Spoke (rule3.py:52), p_i the Node-clock's own mesh rate at its load, Q_ij from the tension gears, 0 at a stopped end;
the spring D = 0 on the light, U_j = 1 (its coupling 0), J = 0, K = 0; W+ = (T div 2)(X_n + X_n'), X_n' after the
regulator's act (tick.py:258-261).

**CHECKED** (probe.py, `python -I probe.py <a worktree at 67b765312> <tensor24-review's src> [records dir]`; its
output probe_out.txt): six worlds of the toy calibre, matter laid at 0 (the head's smallest test piece at sides 3
and 4, its sea, a packet over the sea, the packet alone, the vacuum), 20 to 40 ticks: 5,970 site-ticks per gear.
- The act equals the formula, and Tensor24's own gear(), at 5,970 of 5,970 on each gear.
- Every input recomputed from the head's raw state equals the head's own at every site.
- The end of tick equals the act at 4,123 of 4,123 site-ticks where no turnover hit.

**Sofer's five conditions on the test** (6479294042): (a) the differences named, with counts and stage; (b) mutants
that part it: the push's sign, the pull reading the before slot, the grip from the neighbour's Mesh, b+ = b; (c) the
probe's six worlds, not the smallest piece alone; (d) the per-end table inside the test alone, a test of the board's
own Meshes beside it; (e) the probe and this README committed here.

**The light's spring:** D = 0 on the light, so stage 4 holds no spring term; the term enters with matter at stage 7.

**The differences, named** (condition (a)):
- the turnover replaces the act at 1,847 of 5,970 site-ticks: the head mirrors the tooth as (2 mid W - r) mod W with
  no going, where the tie rule flips it to w - 1 - r and advances go (stage 8);
- the regulator moves W, W+ and the stretch s at every site and tick: W+ = W at 45 of 5,970 (stage 7);
- a head grip belongs to one end of a Mesh: R_ij = R_ji on 8,763 of 17,910 Meshes, since p_i^2 is each end's own
  mesh rate (law 2, "every Mesh couples its two ends alike"; one grip per Mesh in Tensor24; David's formula at
  stage 7);
- the head cannot run the light alone: a calibre with no matter row is refused, and the regulator is always built
  and always acts. David's M1 for stage 4 (W+ = W, every grip W/3, no regulator) parts from the head at tick 1.

**In code:** tests/test_the_tensor24_light.py runs the six worlds and compares Tensor24's pull and gear at the head's
inputs at every site and tick, the end of tick where no turnover hit, with six mutants each parting it; the head's
per-end grips enter through a table of the test alone, and tests/test_the_tensor24_board.py holds the board's own
Meshes, one grip per Mesh.

**Words:** Sofer's on the reading, yes with five conditions (6479294042); David's on the law-2 point, asked.
