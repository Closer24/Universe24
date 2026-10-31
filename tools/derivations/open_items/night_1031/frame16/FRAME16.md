# FRAME16: light's cone at the Node-clock, from the quaternion

Status: DRAFTED, read by no hostile reader. Probes in this folder, whole numbers only, the one division Rule3's
carry, the engine's own `gear()` and `carry()` imported read-only from scanZ: p_frame16.py, p_slots.py,
p_gauge.py, p_gauge2.py, each with its .txt. C = diag(1, -1, -1, -1). For quaternions Re(p q) = p0 q0 - p.q =
p^T C q and Re(p conj q) = p^T q.

## 0. First, the cone with no added gear (the owner's word: "check from the quaternion how it comes out")

0.1 READ: yes, with no gear. The board's four-vector V = t + x i + y j + z k (the stride real, the three axes pure)
    is a quaternion. On the flat slots (00 = 1, ii = -1, the rest 0) the interval is Hamilton's own Re(V V) =
    t^2 - r^2, signature (1, 3) by itself, against Re(V conj V) = N(V) at (4, 0). DERIVED. On any slots G (G00 = W,
    Gii = -grip, G0i, Gjk), the cone of a displacement is -V^T adj(G) V >= 0: cubic in the slots, whole, no root, no
    division (det G < 0 at (1, 3)). On diagonal slots it is grip^2 (grip t^2 - W r^2), i.e. Re(V Vg) >= 0 with
    Vg = grip t + W (x i + y j + z k): the owner's quadric W r^2 <= grip t^2. MEASURED: 0 misses on 3 x 2401
    displacements (p_slots.txt, first line).
0.2 HELD: no. The ten slots as built are ten gears moved linearly; nothing keeps G at (1, 3). MEASURED, each slot
    stepped by the generic act (p_slots.txt): small start (base 16, spread 4): (1, 3) in 1107 of 1107 Node-clock-
    rounds; large start (base 4, spread 6): (1, 3) 198, (2, 2) 848, (3, 1) 55, degenerate (1, 2, 1) 6. The cone
    closes and turns over on the act's own steps. Also short: "Sym^2 V" holds as kinds, not as values (one
    quaternion's square has rank one, 624 of 624; Hamilton's words of one hand reach five slots, ONE_ALGEBRA
    finding 5); and the density sqrt(-g) of the covariant act is a root of the slots.
0.3 HELD WITH NO ADDED GEAR: re-read the same ten gears as a symmetric (gradient) frame S (rows s_m, S = S^T, the
    slots' own kinds A1, T1, A1 + E, T2) and the slots as S C S, slot_mn = Re(s_m s_n). Then S C S = E C E^T with
    E = S C, so by Sylvester the slots are (1, 3) wherever det S /= 0, with no law and no gear added. DERIVED. It
    is section 3's symmetric gauge (E C = (E C)^T): the 16-gear frame with its six local turns tied, which the act
    holds (3.3). MEASURED (p_gauge2.txt, each of the 16 components the generic act, the tie seeded, base 4,
    spread 1 and 3, so not the same start as 0.2's): (1, 3) at
    1100 and 1101 invertible Node-clock-rounds of 1107, singular (1, 2, 1) at 7 and 6, never (2, 2) or (3, 1): the
    cone can close for a round at det S = 0, it cannot turn over. The cone of a displacement: Re(Z Z), Z = adj(S) V.
    Flat: S = I. Diagonal: S = diag(L, l, l, l) gives W = L^2, grip = l^2 (section 4). The price: the act reads
    its slots quadratically (W = S00^2 - S01^2 - S02^2 - S03^2, not rest + k0 c00), a law change of the same kind
    the escapement's W = L^2 already is. Not closed by it: singular S, the tip against the board's clock (2.3), the
    window (5.3). This is the candidate this text puts first; the 16-gear frame below is its parent and its price.

## 1. The 16-gear frame as a clock fix

1.1 The act: the generic act as built on each of the 16 components e_m^a (m the leg: 0 the clock, 1..3 the axes;
    a the quaternion's component), each a gear (now a, before b, tooth s) with its own spring pull and the same
    teeth. Nothing else is needed for the reading or for the run back. The parity: the reading's own is g_0i odd,
    g_00, g_ii, g_jk even; the mirror E -> T E (T = diag(-1, 1, 1, 1), e_0's four rows odd) gives it, and so does
    E -> T E T (odd exactly where one index is time: e_0^k, e_k^0), which section 3's tie needs. DERIVED (both
    give g -> T g T, as T C T = C; they differ by an internal flip, a local turn the reading cannot see).
1.2 The run back: the tick on the mirrored state, mirrored, row by row as for any gear. MEASURED (T E parity):
    40 rounds back on a periodic 3 x 3 x 3 board, 0 entries missed of 1296, three runs. T E T parity on the tied
    frame: 0 missed of 1296, two runs (p_gauge2.txt). The engine's hypotheses hold: each push reads its own row.
1.3 The 24 and the 48: by conjugation, with the legs turned. A board turn R acts on the legs (e_m -> R_mn e_n) and
    on each quaternion by w e conj(w) carried at N(w) (w a whole lift: 24 Hurwitz units doubled, N = 4; 24 of norm 2
    for the quarter turns, N = 2). MEASURED (1500 whole invertible frames x 48 lifts): carry remainders 0;
    conjugation alone changes g in 0 cases; legs turned plus conjugation gives g -> R g R^T with 0 misses; the flat
    frame (1, i, j, k) is fixed in 48 of 48. One side (w e) changes g in 33000 of 33000 non-real cases (still (1, 3),
    0 misses: a different metric, since p -> w p is an invertible map) and for the quarter turns is not whole
    without the root of 2. Why: if b a = +-1, Re(a p b a q b) = +-Re(a p q b) = +-Re(p q b a) = Re(p q); conversely
    a map keeping both N up to scale and C commutes with C, fixes the real line, so a b is real. Only conjugation
    (and parity, a conj(p) a^-1) keeps the reading. DERIVED. The frame is whole-speed (a vector in both
    indices, w and -w alike); one side is the half-speed hand's action (g psi), left to the families.
1.4 Singular: det E = 0, a nonzero displacement mapped to the quaternion 0. The generic act does nothing against
    it. MEASURED (p_frame16.txt B): singular Node-clock-rounds 1 (small, at rest), 1 (small, moving), 16 (large);
    there the reading has a zero root. And det E changes sign between rounds with no zero between, by whole jumps:
    25, 154, 339 (the frame's orientation flips; g's signature cannot see it).

## 2. The metric as a reading

2.1 Which slot: g_00 = Re(e_0 e_0) = (e_0^0)^2 - |vec e_0|^2; g_0i = Re(e_0 e_i); g_ii = Re(e_i e_i);
    g_jk = Re(e_j e_k).
    The index: the act reads W on the count's second difference and the grips on the gradients, so light runs at
    c^2 = grip / W: the slots are the wave operator's coefficients, the inverse metric. So the frame that reads the
    board's slots is the gradient frame F: slot^mn = Re(f^m f^n), and a displacement's interval is Re(Z Z) with
    Z = adj(F) V, whole, no division (det(F)^2 times the true interval). MEASURED: 0 misses of 12005 (C). Read as
    g_mn = Re(e_m e_n) with 00 = W and -ii = grip, light would run at c^2 = W / grip, the inverse. DERIVED.
2.2 Signature on the act's own steps: (1, 3) at every invertible Node-clock-round, by Sylvester (g = E C E^T), no
    law needed. DERIVED. MEASURED: 1106 of 1106, 1106 of 1106, 1091 of 1091; the no, Re(e_m conj e_n), gives
    (4, 0) on the same. The density comes free: det g = -det(E)^2, sqrt(-g) = |det E|, no root. DERIVED. Its
    converse: a whole G with -det G no square (diag(2, -1, -1, -1): 1 < 2 < 4) is no whole frame's reading.
2.3 Correction to "cannot close or turn over": the signature cannot change, but the cone can tip against the
    board's clock with the frame invertible: the 00 reading <= 0 (as g_00 the clock leg is not timelike, as the
    slot W the slice t = const is not spacelike: the board's clock is no time for that cone) in 81, 871, 1004
    invertible Node-clock-rounds of the act; in 1361 of 1500 whole frames; the spatial block not negative definite
    in 1251. MEASURED. Example:
    E = (i, 1, j, k) reads diag(-1, 1, -1, -1). To be the board's clock, two whole inequalities more are owed:
    g_00 > 0 (in slot form W > 0) and the spatial block definite (its three leading minors). Neither is held.

## 3. The six local turns

3.1 What they are: 16 = 10 + 6. E -> E Lambda with Lambda C Lambda^T = C keeps g: so(1, 3). DERIVED. Three are
    rotations: one conjugation u e_m conj(u) for all four legs (whole, g kept, 0 changes measured in 1.3). Three
    are boosts: no quaternion product from either side gives them (1.3). Whole boosts exist only as the integral
    Lorentz group, e.g. p -> p + Re(p v) v with v = 1 + i + j + k, Re(v v) = -2: 1 -> 2 + i + j + k, whose square's
    real part is 4 - 3 = 1. DERIVED.
3.2 What the act does to them: it commutes with constant whole internal signed permutations that keep C (the pull
    is the same on every component), but not with site-dependent turns: pull(E Lambda(x)) /= pull(E) Lambda(x).
    So the generic act is not locally Lorentz-blind: the six are not gauge for it; left free, they wander with
    the rest. DERIVED.
3.3 The tie that holds: the symmetric gauge E C = (E C)^T, six whole linear ties (e_k^0 = -e_0^k, e_j^k = e_k^j),
    transversal to the six turns (so(1, 3) meets {X : X C symmetric} only in 0; "E symmetric" is not a gauge, the
    boosts lie in it). DERIVED. It is kept by the 24 (R S R^T stays symmetric) and by the mirror E -> T E T. The
    act holds it: MEASURED, 0 broken rounds of 60, two seeds (p_gauge.txt); 0 broken Node-clock-rounds of 1107,
    two seeds, with the T E T mirror's run back exact (p_gauge2.txt). Why exactly: on the probe's dial
    (D = 18) a tooth started at 0 stays a multiple of 4, so the half-open edge s = -18 where -n would not split
    to -q, -s is never reached. On a dial whose edge is reachable the opposite ties can break by one: OPEN.
    With the tie the frame is ten gears: section 0.3.

## 4. W = L^2 as the diagonal case

    Gradient frame f^0 = L (real), f^k = l_k u_k (u_k = i, j, k). Re(f^0 f^0) = L^2 = W; -Re(f^k f^k) = l_k^2 =
    grip_k; Re(f^0 f^k) = L l_k Re(u_k) = 0; Re(f^j f^k) = l_j l_k Re(u_j u_k) = 0 (u_j u_k = +-u_i, pure). So the
    diagonal frame reads the diagonal slots exactly, 0i = jk = 0. DERIVED. With l_k = L0 it is the escapement:
    c^2 = grip / W = (L0 / L)^2 = N^2, the rate N = L0 / L. ONE_ALGEBRA's single Phi = L + l_x i + l_y j + l_z k is
    this frame's sum of legs; its square read along the Spokes is rank one, the frame's reading is not.

## 5. Light's cone in the click world

5.1 The order: click B is in A's future iff -dV^T adj(G) dV >= 0 and dt > 0; in its past iff >= 0 and dt < 0;
    otherwise neither can touch the other. Flat: Re(dV dV) >= 0, the sign of Re(dV) choosing the nappe. Diagonal:
    W r^2 <= grip t^2. A quadric with no root. The owner's question: yes, a cone forward and backward from each
    Node-clock, one quadric with two nappes; the mirror swaps them (t -> -t), so the backward cone is the forward
    cone of the mirrored state, and the run back needs no second cone. DERIVED.
5.2 What a click must carry: its round t and its site (x, y, z), whole; the order reads the slots (or S) at the
    Node-clock. Uniform slots: one quadric orders any two clicks. Curved: the order is the chain of local cones
    (B after A iff a chain of neighbour steps runs from A to B, each inside its own Node-clock's forward cone), so
    the comparison reads the slots along the way, not at the ends. DERIVED as a definition; its use OPEN.
5.3 The six Spokes' bound: the board reaches one Spoke per round, |x| + |y| + |z| <= |t|; the quadric lies inside
    iff 3 grip <= W (the octahedron's least reach is along (1, 1, 1)). MEASURED: 144 of 144 (W, grip) pairs, the
    witness (k, k, k) at t = 3k - 1. It is the same whole inequality as the act's linear window in 3-D (von
    Neumann: 12 grip / W <= 4), a law to hold, not a gift of Sylvester. DERIVED for the diagonal case.
5.4 Read twice (owed, not run): (i) special: a source switched on at A changes no click rate at B outside A's
    forward cone, the front read at W r^2 = grip t^2; (ii) general: where the 00 slot deepens the cone narrows,
    and the first click across a deep region comes later than across a flat one (the delay at c = L0 / L). A
    board reading proves no physics.

## 6. OPEN

- That the act as built reaches every frame (or S) reading's 0i and jk: it reads them nowhere (ONE_ALGEBRA finding 5).
- The law that keeps det S (det E) from 0 on the act's own steps.
- The law that keeps g_00 > 0 and the slice spacelike (the cone's place against the board's clock).
- The law that keeps 3 grip <= W, the six Spokes' bound, at every Node-clock.
- The symmetric tie on a dial whose half-open edge is reachable (one-off breaks).
- The act's plan reading g = S C S quadratically, and its books (term 5) against FWDBACK3.
- The density sqrt(-g) = |det E| in the act: the covariant wave law, the escapement's N div(N grad a), checked.
- Lorentz boosts in the act: the interval keeps the integral Lorentz group, the board (a lattice) only long waves.
- Time orientation: det E's sign jumps by whole steps (1.4); what fixes the future nappe across Node-clocks.
- The two click-world readings of 5.4, measured.
