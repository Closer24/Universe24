# Notes 01: the physicist's paper derivation before probing (FWDBACK, the escapement), 2026-10-30

Reruns: probe_fb1..fb5 on t24b (9067de20d) byte-identical (rerun_text/). Under node-live (939fa65a7) probe_fb1 is
identical; probe_fb3 and probe_fb5 stop at the board (load: KeyError 'chosen'), as tg_phys item 6 found.

## 1. One site (or a uniform clock): the proper-time sequence is the standing act's, exactly

At a release every gear does carry(rest (a - b) + push, rest, r): the standing act. Between releases nothing moves.
So the sequence of a site's gear states sampled at its releases IS the standing act's run, state for state, whatever
the clock does, if the pushes read only the site's own gears. Consequences: nature's test for a uniform lapse change
(nothing two clocks at one site show each other changes) holds EXACTLY at every velocity, the count level included;
no pump at any swing (a uniform lapse swing is a change of time coordinate); two clocks at one site keep every ratio
in proper steps. The count-level physics is the standing act's own (displacement per step = floor(P / rest): a
sub-notch momentum never moves the position; as built the same), independent of the clock. Expect: no lock-in of the
escapement's own. To measure: the release-sampled states against a standing run, 0 misses, on rising, falling,
swinging clocks, test gear at v_p = 0 (sub-notch), 1, 2 and a hairspring of a few counts.

## 2. The 00 row's own law (the lapse's): a choice, which one

The 00 gear rides its own escapement: in proper time the standing act, so a free clock keeps its proper velocity
u = dc/dtau. In rounds: dc/dt = (L_0 / L) u, so L dc/dt = L_0 u is kept: L v kept, L = L_0 + c, i.e. sqrt(W_eff) v
kept with W_eff = rest (L / L_0)^2. In the time gear's family (W^k v kept): k = 1/2, the TIMEGEAR text's own choice
(tg_phys item 2: k = 0 as built, 1/4 the covariant scalar action of a lapse-sourcing field, 1/2, 1 the edge; GR gives
a uniform lapse no equation). Check of 1/4 here: L_lag = (1/2) N^(-1) cdot^2, N^(-1) = 1 + c / L_0: E-L gives
L c'' + (1/2) c'^2 = 0, sqrt(L) c' kept, not L c'. Free course of the escapement: L^2 - L_0^2 = 2 L_0 u t, W_eff
LINEAR in t (k = 1/4: L^(3/2) ~ t; k = 0: L ~ t; k = 1: L^3 ~ t). The text's own fb1 A: c00 = 20,000 after 30,000
rounds from u = 1, L_0 = 20,000: L^2 - L_0^2 = 1.2e9 = 2 L_0 t exactly. So: k = 1/2, chosen by the structure (one act
for every gear), not argued from nature. The text's "CHOSEN nowhere" (s.7 step 3) and "the 00 row's own law ... retire"
(step 10) are over-claims. At the count level the free clock at u = 1 follows its own class's course exactly (the
time gear locked at 1 a round); a sub-notch proper momentum of the clock freezes (the standing act's).

## 3. Neighbours at different depths: the board's equation is NOT nature's

Nature, a massless field on a static lapse N(x), flat slices (the covariant scalar; Maxwell with eps = mu = 1/N alike):
  d_t (N^-1 d_t phi) = div (N grad phi)        lattice: sum over links of kappa N_xy (phi_y - phi_x).
Its pi = N^-1 d_t phi; d_t SUM pi = SUM div(...) = 0: the row's momentum is EXACT in nature on any static lapse
(the shift charge). Impedance sqrt(N^-1 N) = 1: no reflection at a lapse step, in 1D at any sharpness.
The escapement: site x releases at the rate N_x = L_0 / L_x (the dial's), each release P_x += F_x with F_x the
standing grip's pull, so d_t P_x = N_x F_x and P_x / rest = d phi / dtau_x = N^-1 d_t phi = pi. Hence
  d_t (N^-1 d_t phi) = N kappa Lap phi = nature's - kappa grad N . grad phi.
d_t SUM P = SUM N_x F_x = - grip SUM_links (N_y - N_x)(a_y - a_x) != 0. So the text's "the lapse gradient's force,
nature's d_t SUM pi = SUM N Lap a" is wrong: nature's is 0; the drift is the escapement's departure (size first order
in dN and in da; sign: minus the product of the two gradients).
For a static N the escapement's equation is N^-2 d_t^2 phi = kappa Lap phi: the ACT AS BUILT's static equation
(W phi'' = grip Lap phi with W = rest / N^2). So on a static non-uniform clock the escapement is the act as built's
physics, and its conserved row momentum (on average) is SUM (L_x / L_0) P_x = SUM W v_coord / rest-scaled, the act
as built's exact book; the text's "which the act as built does not have" is backward.
Consequences to measure: (a) SUM P drifts, SUM L P bounded by windows, the as-built SUM (W v + r) exact, nature's
SUM (W_n v + r) exact; (b) reflection at a sharp step N 1 -> 1/2: escapement and as built R = (Z1 - Z2)/(Z1 + Z2)
with Z ~ N^-1: -1/3; nature 0; (c) WKB: the escapement's conserved energy is SUM of proper (local) energies
(H = SUM (rest/2) v_p^2 + (grip/2) SUM da^2), so a packet entering a well keeps its local energy while its local
frequency rises by 1/N: the quanta fall as N (nature keeps them: Killing energy N E_local kept); amplitude ~ N^(1/2)
(nature constant). (d) Shapiro: the coordinate light speed N c in all lapse-only forms: excess delay
INT (L / L_0 - 1) dz / c, half of GR's weak-field (gamma = 1: the spatial metric, the ii slots, G2's).
Structural: nature's push per proper step of x is kappa (N_xy / N_x)(phi_y - phi_x), the weight N_xy / N_x =
2 L_x / (L_x + L_y): the push divided at a dial that moves with the clocks, the hypothesis (H) of Theorem 1 back for
the Mesh's part. The escapement escapes (H) only where the lapse is uniform across every Mesh.

## 4. The half-step phase

After release n the dial is D_n = L_n + L_(n-1) and the next release is about D_n / (2 L_0) rounds later: the
interval [n, n+1] is timed by L at n - 1/2, while the 00 gear moves from c_n to c_(n+1) during it. Against the
now-slot reference (L_n over the interval) the lag per step is (L_n - L_(n-1)) / (2 L_0) rounds, summed in proper
steps (1/2) ln(L_end / L_start) (the text's number); against L at n + 1/2 it is twice that. Bounded by the clock's
range in rounds: (L_end - L_start) / L_0 at most. To measure on rising, falling, swinging and a long rise.

## 5. The domain and the lever

D >= 2 L_0: no clock faster than the rest. Lost: a clock above the reference (a void against the mean, a hill), a 00
wave about a mean at rest (half its swing below), a clock that speeds up over cosmic time. The lever: push 4 rest m,
L_0 = 2 rest m^2 (the text's "2 rest m" must be per slot): rate at rest 1/m, q <= 1 down to L = 2 rest m, i.e.
c >= -2 rest m (m - 1); W_eff at rest = (L_0 / 2) = m^2 rest. Cost: the rest clock stands m - 1 rounds of m, so every
coordinate reading is a staircase m deep and light per round is m times slower; neighbours whose clocks differ by a
count release on different rounds everywhere.

## 6. Two clocks at one site

Exact by section 1 (both gears step at the same releases at their own standing teeth): ratios kept to the step in
proper steps. The text's 2012..2016 are periods in rounds over spans of different lengths on a rising clock.
