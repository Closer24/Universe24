# Draft K: the detector's click under way 2, against law 10

For Tensor24's owed list (TENSOR24.md, section 30, item 11 (f), with (o) way 2 and (s); law 10 in section 19). The owner's word of 14:37 UTC, in translation: "The missing part: try to solve it through the detector's click", or else solve it once the engine is built in tensors; "The solution is in the detector's click." Drafted under derive/PROTOCOL.md. Research stopped at 15:00 UTC by the owner's word through the coordinator: no probe was run, so this draft holds proofs and OPEN items only, and no CHECKED mark. Every claim is marked PROVED (with its proof) or OPEN (with what blocks it).

## 0. The answer in short

- The act: at a detector's Node-clock the click of a split (law 6) divides the meeting into two parts, the detector's own axis phi and its turned-over axis T phi; the draw's quotient t leaves as the event, its remainder r stays, and the measured hand is written along the part's axis. Under way 2 the reversed run leaves that write in place.
- K1, PROVED: the write is many to one, so after a turnover the board retraces the mirror of its past only back to the last click and departs there. This is the only place way 2 breaks the palindrome, as the second reviewers found.
- K2, PROVED: on a finite board every reading taken per bang is eventually periodic, whatever the acts, the detector's click included. So row 46, read as counts rising at every bang, cannot hold for ever on a finite board. It can hold only through a transient that the clicks open, and that transient has no length in the exact rewind.
- K3, PROVED (cited): the click kinds read in the 24 are at most eight (MB_verify, Burnside). So the number of distinct kinds per bang, 0 to 8, rises strictly for at most eight bangs in a row.
- K4, PROVED: the record, the Outside, grows at every bang by that bang's clicks. It rises strictly at every bang if and only if every bang clicks at least once. This is the one count that can rise for ever, and the board never reads it.
- OPEN: whether a kept carry (law 11) lets the detector's click grow the gears themselves bang after bang; the toy counts per bang; row 1c on the toy.
- It replaces nothing yet. It narrows item (f): the detector's click carries the arrow (Postulate 7 of the old seven: "the clicks carrying the arrow"), but "more at every bang" from it needs either the record's reading of row 46 or an unbounded board.

## 1. In the clocks

- A twin hand psi, carried by the step, comes to a detector's Node-clock, where the detector's own twin hand phi stands.
- The click of a whole fires (law 5), and the meeting splits into two parts, sized by the two clock readings N(<phi, psi>) and N(det[phi, psi]). Their sum is the product of the two counts (Lagrange).
- The draw reads the vernier, the board's own invariant digits, and Rule3 divides it: c (sigma_up + sigma_down) = t room + r.
- The quotient t names the part and leaves as an event into the record. The remainder r stays in the vernier's digits.
- The measured hand is rewritten along the part's axis: the detector's hand for up, the detector's turned-over hand for down.
- Many hands are rewritten to one, so the click cannot be run back without its log.
- At the top the whole board turns over by T, each gear by its kind's phase reversal. The reversed run is the forward law again (way 2). Between clicks it retraces the mirror of the past. At each click it finds what the click wrote, not what was there before, and runs on with it into the next bang.

## 2. The formula, in the three operations

For twin hands phi = (phi_u, phi_d) and psi = (psi_u, psi_d) of Gaussian integers, with the bar the conjugate:

- <phi, psi> = bar(phi_u) psi_u + bar(phi_d) psi_d; det[phi, psi] = phi_u psi_d - phi_d psi_u.
- sigma_up = N(<phi, psi>), sigma_down = N(det[phi, psi]), sigma_up + sigma_down = rho_phi rho_psi.
- The draw: c (sigma_up + sigma_down) = t room + r, with 0 <= r < room (Rule3). The part is up where t < sigma_up, that is, where c (sigma_up + sigma_down) < room sigma_up. This is law 6's line "c (rho + rho) rho_d < room (rho rho_d + S . m)", since 2 sigma_up = rho rho_d + S . m.
- The write, up: psi <- <phi, psi> phi. Down: psi <- det[phi, psi] phi_perp, with phi_perp = (-bar(phi_d), bar(phi_u)) = -T phi.
- The event: (t, the part) into the record. The vernier keeps r.
- Only multiplication, addition and Rule3 appear. The comparison t < sigma_up is itself a Rule3 quotient, the part's index being the quotient of t by the first part's size, read 0 or at least 1. Writing that select without an if, as one Rule3 quotient times the two writes, is OPEN for the engine's code and belongs to Sofer's check.

## 3. In the tensors

- phi and psi are E1/2 of 2O. det[phi, psi] is the A1 invariant of E1/2 x E1/2. <phi, psi> = -det[phi_perp, psi] is the same invariant taken against the turned-over detector.
- So both parts are A1 readings, and the click's two axes are phi and T phi. The 24 allows the split because both sizes are invariant under every signed rotation of 2O, which commutes with T = i sigma_y K (draft E).
- The composite (candidate (c)): measured quantum and detector read as one dial, E1/2 x E1/2 = A1 + T1 (item (t)). The kinds reachable stop at the eight of 2O (K3).

## 4. The proofs

- **The split (PROVED).** rho_phi psi = <phi, psi> phi + det[phi, psi] phi_perp.
  - First component: (bar(phi_u) psi_u + bar(phi_d) psi_d) phi_u - (phi_u psi_d - phi_d psi_u) bar(phi_d) = (N(phi_u) + N(phi_d)) psi_u.
  - The second component the same way.
  - Taking the norm with <phi, phi_perp> = 0 and N(phi_perp) = rho_phi gives Lagrange: rho_phi rho_psi = sigma_up + sigma_down.
- **phi_perp = -T phi (PROVED).** T phi = i sigma_y bar(phi) = (bar(phi_d), -bar(phi_u)).
- **K1, the click is many to one and breaks the mirror only at itself (PROVED).**
  - For rho_phi > 0 the up write maps every psi with one value of <phi, psi> to one hand; det[phi, psi] is erased, and only the log keeps it (law 3's line, "a click is undone only from its log").
  - Let the forward run be x_i = C_i(S x_(i-1)), with C_i the click map at tick i (the identity where nothing clicks).
  - Because T^-1 S T = S^-1 on every gear (T T = -1 on twin hands commutes with the linear step), S T x = T S^-1 x for every state.
  - So the reversed run from T x_K gives T x_(K-1), T x_(K-2), ..., as long as no click acts in either direction.
  - The retrace departs at the first tick, counted back from the top, where a click acts. Either the forward run's click at tick i wrote something, so that S^-1 x_i differs from x_(i-1), or the reversed run's own click fires on T x_i. The board after the turnover is the mirror of its past plus what the clicks wrote; with no click acting, the retrace is whole.
  - With the clicks undone from the log, every C_i is inverted, and the reviewers' palindrome returns: two distinct bang states, four with T T = -1.
- **K2, finite board (PROVED).**
  - Every act under way 2 is deterministic: the step, the clicks with a draw that reads the board's own digits, the turnover at the time gear's top. So one swing from bang to bang is a map H of the finite set X of gear states into itself.
  - Among b_0, ..., b_|X| two bang states coincide, and from there H repeats everything. So the bang states, and every reading f(b_k), are eventually periodic, with transient plus period at most |X|.
  - A reading that rises strictly at every bang is never periodic, so it fails by bang |X| at the latest. The record is written but never read by the gears, so it does not change H.
  - Under the exact rewind H is a bijection, so the transient has no length: the orbit is periodic from the first bang (the palindrome). A many-to-one click is what makes a transient possible.
  - Draft F's closing step is the periodic part of this.
- **K3 (PROVED, cited).** The kinds are irreducible kinds of 2O: eight (MB_verify; Burnside and Brauer).
- **K4 (PROVED).** Let n_j be the number of clicks at bang j. The record after bang k has n_1 + ... + n_k events, which rises strictly at bang k if and only if n_k >= 1. On the eventual cycle of a finite board the n_j are periodic, so the record grows linearly if and only if some bang of the cycle clicks; it grows at every bang if and only if every bang of the cycle clicks.

## 5. The probes

None was run (the 15:00 UTC stop). The probe designed, kept here as OPEN:

- **The toy.** A ring of 3 Node-clocks, gears mod 7 with symmetric residues so that the conjugate keeps every norm.
  - Light ell_j and twin hands psi_j; a detector hand phi at one Node-clock; a free time gear with velocity +-1.
  - The step: every gear second order, now' = F(now) - before. F is the neighbours' sum on light and quaternion-form coefficients on the twins, so F commutes with T.
  - T: (now, before) -> (T before, T now). The turnover fires at the time gear's carry, at 0 and K.
  - The fitting: q = ell^2 div 9 at the fitting's Node-clock; the take leaves ell = 0; it lays q pairs (a, T a) along the hand there.
  - The detector: law 5's q = rho_psi div w, then the split of section 2, with c the light digits in radix 7 and room = 7^3, r written back to those digits.
- **The counts per bang:** distinct states, births, detector clicks up and down, distinct axes written, record length, bang states repeated.
- **The mutants:** (i) the clicks undone from the log, which must give the palindrome; (ii) the detector removed; (iii) the draw replaced by the fixed part up, the vernier untouched; (iv) no clicks at all.
- **The pass criteria:** (i) and (iv) give exactly the palindrome's two (or four) bang states; the way-2 run departs from the mirror at the last click of each swing (K1); the bang states become eventually periodic (K2).

## 6. The law's lines

From origin/scribe-5:docs/ALGEBRA.md as held locally at 3d6cd8a35 (13:23 UTC; the remote has since moved to f07832061, which was not fetched, since a fetch changes state):

- Line 76: "7. The Inside is the lattice, where no one measures, deterministic and bit-reversible between clicks, holding the future with no arrow; the Outside is the detectors and their clicks, realised events, the detectors bobs of the great clock with two sides and the clicks carrying the arrow, the only thing claimed to represent nature."
- Lines 73 to 74: "6. A measurement is a detector's click ... the realised click written at the one Node-clock from which the quantum reached the detector, the instrument's act and the one drive outside the reversal".
- TENSOR24 section 19:
  - law 3: "The click is many to one, so a click is undone only from its log";
  - law 4 with (s): the turnover is T on every gear, and T T = -1 on twin hands;
  - law 6 (the split);
  - law 9 (the draw);
  - law 10.

## 7. What it replaces and what moves

- No fake is removed, and no row moves on a run.
- **Row 46 per bang:** on a finite board under any deterministic acts it fails by K2. The detector's click cannot change that.
- **Row 46 on the record:** read cumulatively on the Outside, it holds at every bang that clicks (K4). That reading is the owner's to rule, with item (d).
- **Row 1c:** under way 2 it is possible only through the clicks (K1, K2). On the toy it is OPEN.
- This agrees with BC_verify: the next cycle's S gains only where the settings repeat. The detector's write runs on, but on a finite board it runs on into a cycle.

## 8. OPEN

- **The toy's counts and the four mutants** (section 5). Blocked by the 15:00 UTC stop; drafter K or the verifier.
- **An unbounded board (law 11, the carry kept).** Only that escapes K2. Does the detector's click supply a kept carry at every bang? For example, the draw's remainder kept as a new vernier digit, so that room and the possible click outcomes grow bang after bang. Blocked by an engine in tensors with kept carries; the owner's "or once the engine is built in tensors".
- **The select without an if** (section 2): Sofer's.
- **Whether every bang of the eventual cycle clicks at least once**, so that K4 gives growth at every bang. Blocked by the toy, then the engine.
- **The reading of "more":** per bang on the gears (impossible for ever on a finite board, K2), or on the record (K4). The owner's, with item (d).
