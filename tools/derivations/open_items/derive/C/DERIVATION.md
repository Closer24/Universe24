# Draft C: the course's closure (J's metric half on the regulator's time gear)

Tensor24's owed list, section 19 ("the course's closure", Animate's condition (b), 6465411419); section 16's E10, E11 and F1; section 24, item 2; section 28's `trace` row. Drafted under derive/PROTOCOL.md: steps 1 to 4 and a self-check of step 6 are here; step 5 (the second hand) and David's sign-off are not mine.

Every claim is marked **PROVED** (with its proof), **CHECKED** (with its probe and count) or **OPEN**.

## 0. The answer

- **A brake from the stress that overtakes the push after every rise: cannot be derived.** It is impossible for any matter whose pressure stays at or below its energy (every train of the calibre), on the piece's torus, in the one formula's A1 course. The theorems are C1 to C4 (section 5), checked on the engine.
- **What does derive** is the push: GR's A1 equation in the head's own gauge. It replaces held_numerator's typed form (E10), needs no clamp (F1), and never brakes (section 4).
- **The missing piece is named exactly:** a brake that does not dilute with the stretch.
  - Either a **positive spatial curvature k**: a closed 3-sphere, which the cube's torus is not.
  - Or a **negative vacuum energy, Lambda < 0**: in the one formula this is exactly the time gear's own spring D_R (theorem C5).
  - Each is a declaration. Each contradicts nature: the torus is flat, and nature's Lambda is positive.
  - The seed's own Friedmann residual, held as k, is not a way out. It makes the plan's seed static (C6).
- **What does close the course with no typed number is not a brake.** It is a threshold: the rate chain's zero.
  - At the stretch X_c = 4,268,834,097 the mesh rate rounds to 0 (load 3,793, rate 22). There the head's frozen Node-clock (BH-S1, the fake R10) makes law 4's weak maximum, and the whole board turns over.
  - With the derived push this gives recurring, longer bangs whose length follows Friedmann's rule: 5 bangs in 250 ticks at 5,000,000 quanta, 2 at 500,000, 1 at 50,000.
  - The rewind is 20 of 20 through the turnovers, and the books close 250 of 250.
  - It stands only on R10's restore. With the restore struck there is no top, and the head's rewind of the stopped Node-clocks fails (0 of 20).
  - So it is David's (R10 as "the rate 0 gives nothing") or the owner's (a ceiling trigger in law 4) to decide.

## 1. The A1 course of the one formula, exactly (PROVED)

On a piece alike at every Node-clock, the regulator's time gear steps by clock.act: Rule3's turn (clock.turn), then the drive (clock.drive). The turn's total is

    hold X - w X- + SUM_j R_j X_j + r,   hold = 2 w - D_R - SUM_j R_j,

and the grips cancel exactly, because every X_j = X. So, with the drive's carry:

    X+ = 2 X - X- + floor((r - D_R X) / w) + floor((N + r_d) / T_d)
    r' = (r - D_R X) mod w,   r_d' = (N + r_d) mod T_d

- X is the stretch (the time gear's notch); X- is the notch before.
- w = T = 6 rim Gamma^2 G^2 is the regulator's teeth count.
- D_R = 12 (rim - pinion_R) p_0^2 G^2 is its spring (rule3.spring).
- N is the drive's numerator and T_d its drive teeth (t rim Gamma^4 key, rule3.held_teeth).
- r and r_d are the fine teeth.

Proof: clock.turn, clock.act and clock.drive (S/t24/src/event_universe/clock.py:146-203), rule3.gearing and rule3.spring. Animate's reading, (X+ - X) - (X - X-) = q - (D_R / w) X, is this up to the fine tooth. There is no constant term: the flat torus gives the course no curvature.

## 2. The gauge, and the matter's half is GR's (PROVED; CHECKED)

**The gauge.** The rate is the lapse, N = p_0 / Gamma. The scale is a = Gamma / p_0. The stretch is X = Gamma a^4, because features/stretch sets X = ceil(Gamma^5 / p_0^4), so X p_0^4 = Gamma^5 to the ceiling.

**The driven gear.** It obeys W+ (a+ - a) - W (a - a-) = X F, with W = (T / 2)(X- + X), the time gear's mean teeth (readings.mean_teeth). Its coefficients:
- R_j / T = (1/3) (p_m / Gamma)^2 = (1/3) N^4 at no tension, from p_m = p_0^2 / Gamma (rates.mesh_rate);
- D / T = 2 (s / rim) N^2, with s = rim - pinion the train's spring.

So, with N = 1 / a, d/dt (a^4 da/dt) = (1/3) LAPLACIAN a - m^2 a^2 a, with m^2 = 2 s / rim. This is GR's scalar field on the Friedmann metric with lapse 1 / a: d/dt (a^3 phi' / N) = N a LAPLACIAN phi - N a^3 m^2 phi. The 1/3 is the stencil's light speed squared. PROVED by the coefficients.

**The forms.** tick.impulse's forms are the sum over every driven gear of u_in u_out + (-a pull) div T. They split exactly into three parts:
- K, the kinetic products;
- G = (-a pull - D a a) div T, the Meshes' wind;
- V = D a a div T, the springs' wind (the head's `masses`).

In GR's terms F = K + G + V = 2 rho / a^2, with rho = (1/2)(phi'/N)^2 + (1/2)|grad phi|^2 / a^2 + (1/2) m^2 phi^2.

CHECKED: forms = K + G + V within 7 units at every tick of 30 at 500 quanta (trace_head_500_parts.txt; the per-gear carries). At the seed the forms are 18,000,000 = 500 key, with K = 0 and G = 18,000,000.

## 3. GR's A1 equations in this gauge (PROVED)

Notation: kappa is the coupling; k is the spatial curvature; S = 2 (3 p) / a^2 is the stress's whole trace in the forms' units.

For a scalar train:
- 3 p = 3K' - G' - 3V' in proper units, so S = 3K - G - 3V;
- F - S/3 = (4/3) G + 2 V;
- F + S = 4 K - 2 V.

The three equations:

    (C)  Friedmann's constraint, G_00 = kappa T_00:   X'^2 = (8 kappa / 3) X^2 F - 16 Gamma k X
    (V)  the volume equation, R^i_i:                   X'' = kappa X (F - S/3) - 8 Gamma k
    (R)  the 00 equation, R_00 (Raychaudhuri):         X'' - X'^2 / (2 X) = -(kappa / 3) X (F + S)
         in the area Y = a^2 = (X / Gamma)^(1/2):      Y'' = -(kappa / 3)(rho + 3 p)

Derivation:
- (C) is (a' / (N a))^2 = (kappa/3) rho - k / a^2 with N a = 1, written in X = Gamma a^4 and rho a^6 = (X / Gamma)^2 F / 2.
- (V) is d(X'^2)/dt of (C), using the continuity equation rho' = -3 (a'/a)(rho + p).
- (R) is the proper-time a''/a = -(kappa/6)(rho + 3p), with d/dtau = a d/dt.
- (V) and (R) agree on (C): the right side of (R) less that of (V) is (C)'s residual, X'^2 - (8 kappa / 3) X^2 F + 16 Gamma k X, divided by 2X.
- Along (V), E = X'^2 / 16 - (kappa / 6) X^2 F + Gamma k X is a first integral. With continuity, dE/dt = 0. GR asks E = 0.

The head's course is (V) with k = 0 and no constraint. Its seed at rest has E = -(kappa/6) X_0^2 F_0 < 0, which acts as a negative stiff energy: a bounce at the seed, then an expansion for ever.

## 4. The derived push (replaces E10's typed form) (PROVED; CHECKED)

**The formula, in the three operations:**

    q = carry( X ((d + 1) G + 2 d V),  Gamma key,  r_d )
    G = carry( SUM over every driven train and gear of (- a pull - D a a),  T )
    V = carry( SUM over every driven train and gear of D a a,  T )

**Its terms, in clock words:**
- X: the stretch at the tick's start;
- a: a gear's start notch, and pull its pull;
- D: the train's spring;
- T: the teeth count;
- Gamma: the full rate; key: the quantum of action;
- d + 1 = 4: the axes plus one; 2 d = 6: the Spokes;
- r_d: the time gear's drive fine tooth.

It is (V) with kappa = d / (Gamma key). That normalization makes it equal to the head's own push term at the vacuum. The coupling's reading as Newton's constant is still owed (David, section 28).

The trace weight t drops out. In the probe and in work/ the numerator carries M = t rim Gamma^3 over the head's drive teeth M Gamma key. The quotients are those of the plain form: carry(M n, M T, M r) = (carry(n, T, r)'s quotient, M times its remainder) forward. The fine tooth is born at mid(M T) = M mid(T), the teeth T = Gamma key being even, and the turnover's mirror keeps the factor M. Every probe and every rewind here ran the scaled form; the plain form's own rewind is law 3's (any carry that keeps its remainder).

**Its properties:**
- **Never below 0 on the A1 course** (PROVED).
  - V >= 0 for every spring D >= 0.
  - On the A1 course every Node-clock reads the same G (the plan's light has its wind alike at every Node-clock). So G is the board's mean: (1/2) SUM over the Meshes of R |U a_j - a|^2, divided by the number of Node-clocks, which is >= 0. The grips are read the same from both ends and U is unitary.
  - Off the A1 course G can be below 0 at a Node-clock (a local brake). OPEN; but CHECKED that it never turned a first difference down at 500 quanta (0 falls of 16,000), where the fittings leave the board only nearly alike.
- **The rewind** (PROVED; CHECKED). N reads only the tick's start (the start notches, their pulls, the stretch), and these are the same forward and backward, so the drive's carry is undone exactly.
  - 500 quanta: 20 of 20.
  - 5,000,000 quanta: 20 of 20 from tick 15, through the turnover at 24.
  - 500,000 quanta: 20 of 20 from tick 64, through the turnover at 74.
- **The first step from rest is X1 = X0 (1 + 4 n / Gamma)** for the plan's light (G0 = F0 = n key) (PROVED; CHECKED: 3,000 at 500 quanta; 20,001,000 at 5,000,000). The head's own step is X0 (1 + (4/3) n / Gamma).
- **On the head's setting at its first tick, it is the head's push term without its brake** (PROVED; CHECKED: q = 2,000 at 500 quanta against the head's push 2,000 less its brake 1,333).
- **The quanta kept:** it moves no quanta (the regulator holds no hand). The books are in section 6.
- **The 24:** G and V are the head's per-gear form products, split in two. They inherit the forms' symmetry. OPEN: not checked separately; the second hand should.
- **Built into the scratch copy** (CHECKED): work/src/event_universe/core/rule3.py `time_drive`, and work/src/event_universe/tick.py (the impulse books G and V; the carry drives the time gear by `time_drive`; the regulator's spring is set to 0, item (c)). The diff is work_drive.diff.txt. It is bit for bit with the probe's installed drive: state hashes cd82a7acc76d2f87 (500 quanta, 60 ticks), 8351891de2026407 (5M, 30), 8cffcddb562c345c (500, 250), 77e8684641d42469 (5M, 250).

## 5. Why no brake closes the course

**C1. The flat torus never turns** (PROVED: GR).
- With (C) and k = 0: X'^2 = (8 kappa / 3) X^2 F > 0 for every state with energy, so X' never vanishes: no top and no recollapse.
- A top needs F = 0 there, that is a negative-energy part (Lambda < 0), or k > 0.
- A seed at rest with energy is not a state of GR on the torus: it breaks (C) by (8 kappa / 3) X0^2 F0.
- So **"a discrete closed Friedmann universe" cannot be the torus's A1 course.** The torus is closed in topology but flat in geometry, and a flat Friedmann universe with positive energy expands for ever.

**C2. Push only means no second top, exactly** (PROVED; CHECKED).
- If D_R = 0 and N >= 0 at every tick, then section 1 gives floor(r / w) = 0 for 0 <= r < w, and floor((N + r_d) / T_d) >= 0. So X+ - X >= X - X- at every Node-clock of an A1 board.
- After a rise, no weak maximum can come. The floor X_f = 19 is never met on a rise.
- CHECKED on the head's acts.carry (monotone.py, 200,000 random states):
  - with D = 0 and N >= 0: 200,000 of 200,000 held;
  - with the regulator's spring alone: 5 held;
  - with N of either sign: 100,041 held.
- CHECKED on the engine with the derived push: the first difference fell at 0 of 16,000 Node-clock ticks at 500 quanta, 0 of 16,000 at 5,000, and 0 of 15,680 at 5,000,000.

**C3. The pressure never overtakes the energy** (PROVED).
- For every train with D >= 0 (pinion <= rim), F - S/3 = (4/3) G + 2 V >= 0 on the A1 course (section 4). So (V)'s numerator is >= 0, and C2 applies.
- A brake by the pressure would need p > rho: the dominant energy condition broken, a sound faster than light.
- This is the question "the sign of the matter's pressure". In (V) the pressure does brake (rho - p), but it never wins.

**C4. No brake from the trace can stop dust** (PROVED; CHECKED).
- On an A1 board, a sprung hand at rest has every centred gradient 0. So the head's trace sigma = SUM_a Re(conj(d_a z) d_a z) is 0, while its forms are > 0.
- Any drive of the form X (alpha F - beta sigma), with any weights, pushes it and never brakes it.
- The head's typed brake tops the first rise at 500 quanta and never again (CHECKED, trace_head_500.txt):
  - q < 0 at (0, 0, 0) from tick 4 to 20;
  - sigma / (rim F) is 31.8 at X 10,442 on the first rise (tick 11), and 8.2 at X 10,912 on the second (tick 31), after the fittings; the springs' part is at most 2.4 percent of the forms over the first 30 ticks (trace_head_500_parts.txt), so dust is not what escapes the brake there;
  - so its brake rests on the light's mode, a lattice reading, not a law.
- Head, 500 quanta: 1 bang in 800 ticks (run_head_500_800.txt).

**C5. The time gear's spring is a negative Lambda** (PROVED; CHECKED).
- (D_R X / w)^2 = 4 (s_R / rim)^2 Gamma X (X p_0^4 / Gamma^5), from rule3.spring, teeth_of and stretch_of.
- So -(D_R / w) X = -2 (s_R / rim) (Gamma X)^(1/2) to the stretch's ceiling.
- A Lambda adds 4 Lambda (Gamma X)^(1/2) to (V). So Lambda = -(1/2)(s_R / rim), which is about -1 / (2 Gamma) at the head's pair s_R = rim div Gamma.
- In the continuum it closes every course: it grows as X^(1/2), while every push dilutes.
- At the head's value it is too weak before the rate chain's zero. CHECKED (volL, 500 quanta, 800 ticks): 0 bangs; the board reaches the stopped load (X up to 5,095,062,125) with 108 local turnovers there; books 800 of 800.

**C6. The seed's own residual is static** (PROVED; CHECKED).
- Holding the seed's constraint residual as the curvature, 8 Gamma k = (4 kappa / 3) X0 F0 - X0'^2 / (2 X0), is (V) made equal to (R).
- At the plan's seed it gives X'' = -(kappa / 3) X0 (4 K0 - 2 V0) = 0. The quarter-turn light has its whole wind in the Meshes' part (K = u_in u_out = 0 at the quarter turn), so rho + 3p = 0 in the lattice's measure: a static Einstein point.
- CHECKED (volR, 500 quanta, 250 ticks):
  - X = 1,000 at all 64 Node-clocks at every tick;
  - 0 fittings;
  - the drive's quotient alternates between 0 and -1 (the held residual against the per-tick carry of G), so law 4 reads 83 one-notch tops, every 3 ticks, which move no notch;
  - rewind 20 of 20; books 250 of 250.

## 6. What closes the course, and what each costs

| route | probe | bangs (whole-board turnovers) | rewind | books | status |
| --- | --- | --- | --- | --- | --- |
| the head: typed form and F1, 5,000,000 quanta | probe_head_5M | 50 in 250 (3, 8, ..., 248), stretch at most 4,992 | 20 of 20 | 250 of 250 | E10, F1 |
| the head, 500 quanta | probe_head_500, run_head_500_800 | 1 in 800 (tick 12), then a runaway to the rate chain's zero | 20 of 20 | 250 of 250; 800 of 800 | E10 |
| F1 struck, 5,000,000 quanta | probe_nocap_5M | 10 in 30 (every 3 ticks), a spike to 6,667,665 | 20 of 20 | 30 of 30 | Animate's spike |
| derived push, 500 / 5,000 quanta | probe_vol0_500, probe_vol0_5k | 0 in 250 | 20 of 20 (500) | 250 of 250 | C2 |
| derived push, 50,000 quanta | probe_vol0_50k | 1 (tick 250) | | 250 of 250 | the rate chain's zero |
| derived push, 500,000 quanta | probe_vol0_500k_250 | 2 (74, 221) | 20 of 20 from 64 | 250 of 250 | the rate chain's zero |
| derived push, 5,000,000 quanta | probe_vol0_5M_250, work_probe_5M_250 | 5 (24, 71, 118, 165, 212), all 5 with every Node-clock stopped | 20 of 20 from 15 | 250 of 250 | the rate chain's zero, through R10 |
| derived push, BH-S1's restore struck | probe_vol0_free_5M | 0 in 40: X coasts past the zero | 0 of 20 from 15 | 40 of 40 | R10 is load-bearing |
| plus the head's spring (Lambda < 0) | run_volL_500_800 | 0 in 800 | | 800 of 800 | C5, too weak |
| plus the seed's residual (k) | probe_volR_500 | static | 20 of 20 | 250 of 250 | C6 |
| plus half the residual (a declared k) | probe_volK2_500 | 2 (5, 15), then 328 local turnovers | 20 of 20 | 247 of 250 | declared |

**(a) The threshold: the rate chain's zero** (CHECKED; its standing OPEN).
- The mesh rate rounds to 0 where 2 p_0^2 < Gamma, which is load 3,793 (rate 22), the stopped load. There X_c = ceil(Gamma^5 / 22^4) = 4,268,834,097, about (2 Gamma)^2 Gamma = 4 Gamma^3: the lattice's last readable ruler, a_c^2 about 2 Gamma (PROVED: rates.stopped_load, rounded).
- There BH-S1 restores the stopped Node-clock's gears, and law 4 reads the frozen time gear (X0 < X1 = X2) as a weak maximum (FR-S1).
- With the derived push:
  - the bangs recur, and their length follows Friedmann's rule. The turnovers come at 24, 74 and 250 at 5,000,000, 500,000 and 50,000 quanta: each tenth of the energy multiplies the rise by 3.1 to 3.4, against the square root of 10, 3.16;
  - each bang differs while the fittings go on. The tops are 4,638,548,302, 4,639,582,178, 4,641,211,062 and 4,641,121,200. The fifth repeats the third (4,641,211,062; first steps 20,001,018 at ticks 95 and 189) once no fitting comes: the exact return of a time-symmetric course, period two bangs;
  - every bottom returns to X = 1,000 at rest; 96 births (fittings and unspringings) at 5,000,000 quanta, 32 at 500,000.
- It is **not a brake**: the first difference never falls (0 of 15,680).
- It needs R10's restore. Without it the stopped time gear coasts (its first difference constant at 517,114,983 from tick 23), and the head's rewind of the stopped Node-clocks breaks (0 of 20).
- A derived form would be R10's "the rate 0 gives nothing" holding the time gear's own step at the lapse's zero (David), or a third trigger of law 4, the ceiling beside the floor X_f (the owner's). Neither is derived here: OPEN.

**(b) A declared curvature k > 0** (CHECKED with half the seed's residual, volK2).
- 2 whole-board bangs (5, 15). The sameness breaks at tick 25 (32 and 32), and then come 328 local turnovers in 250 ticks, the stretch spreading to 3,343,235..20,921,688. It is no longer an A1 course.
- Rewind 20 of 20 through both bangs.
- Books 247 of 250. The 3 open phases (ticks 50, 54 and 67, by 4, 8 and 4) are all at unspringings, one unit per unspringing (books_open.py; books_open_volK2.txt).
- The head's own click opens alike: on its hole world 119 of 120 (tick 79, by -1, at one unspringing), and on the bang at 2,000 quanta 249 of 250 (tick 51, by -4, at 8 unspringings) (books_world.py, CHECKED). So the open books are the head's unspringing books (E18, group A), not the drive's.
- k's value is fitted: excluded by Sofer's law.

**(c) A declared Lambda < 0**, the time gear's spring (C5). At the head's pair it is too weak. Any value that closes the course in 250 ticks is fitted. It also contradicts nature's positive Lambda, and item (c) for the nine other gears.

## 7. The aim, a discrete closed Friedmann universe: what can and cannot be shown

- **Cannot** (C1): on the torus the A1 course is a discrete flat Friedmann universe, with k = 0 by section 1. With positive energy it never turns.
- **Shown** (CHECKED): the derived push is (V) in the head's own integers.
  - X1 = X0 (1 + 4 n / Gamma).
  - The first difference is monotone (C2).
  - The rise to a fixed stretch scales as n^(-1/2), Friedmann's rule.
- The only turn on the torus is the lattice's own last rate (section 6 (a)): a horizon of the ruler, not a curvature.

## 8. What it replaces and what it changes

- **E10** (held_numerator's typed form: the trace weight t, the trailing p_0, the brake -sigma p_0^2) is replaced by the derived push (section 4). t keeps no role in the course; section 28's `trace` row loses its course meaning.
- **E11 / F1** (the clamp at plus and minus the hold) is replaced by nothing: the push needs no clamp.
  - One remark: above n = Gamma / 4 quanta per Node-clock, the first step more than doubles the stretch (at 5,000,000 quanta it is 20,001 times the seed). The owner's sentence of 2026-10-27, 18:5x UTC, "no clock's stretch moves by more than itself in one tick", then binds. Below it, the course to the rate chain's zero is thousands of ticks long (OPEN, the owner's).
- **R13 / item (c):** the regulator's spring is set to 0 in work/. C5 shows its A1 meaning: a negative Lambda.
- **Other worlds move** (CHECKED, world_course.py on the hole world, 30 ticks):
  - with the derived push, no turnover after tick 1 and no fitting by tick 30;
  - the head has local turnovers at every tick and 21 births;
  - so the head's test test_the_books_close_at_every_click_mergers_and_lays_alike fails on work/. Its books close at every click, but no unspringing comes in 30 ticks (work_books_test.txt).
  - The hole's local turnovers on the head rest on E10's typed brake too.
- **Rows** (Animate's to bench, not read here):
  - 1 and 1c (the bangs recur and differ) would read the threshold route's 5 bangs;
  - 46 (each later bang shows more) needs the fittings to go on: at 5,000,000 quanta they stop by tick 120 (96 births in 120 ticks, 96 in 250);
  - 58 to 60 (the expansion per bang) read (V)'s course;
  - the hole's rows move with its course.
- **Contradictions with nature it leaves:**
  - GR's flat universe never recollapses; the turn at the rate chain's zero is the lattice's resolution (a_c of about 45 at Gamma = 1,000).
  - A declared k > 0 contradicts the torus.
  - A declared Lambda < 0 contradicts the observed acceleration (row 5).
  - The plan's seed at rest breaks Friedmann's constraint.

## 9. Sofer's law check (self-check; Sofer's own owed) and what the second hand should attack

**The push:**
- no number beyond 0, 1 and the counts d + 1 and 2 d;
- no float, root, clamp, branch on a train, or table;
- one sum over every driven train alike;
- it is the Einstein equation's A1 part, not a formula of the bang;
- kappa's normalization is chosen to meet the head's push at the vacuum: a convention to be read as G (owed).

**Not proposed:** volK2's half-residual (fitted) and any Lambda (fitted).

**To attack:**
- the gauge identification (section 2) on a non-uniform board;
- C3's sign of G off an A1 board;
- the 24 of G and V;
- the claim that the open books are the head's;
- whether any train (twin hands, a negative spring) can make F - S/3 < 0;
- the rate chain's zero at another Gamma.

## 10. OPEN

1. The course's closure as a brake needs one declaration (k or Lambda), or the constraint violation read as curvature (static at the plan's seed). The owner chooses, or rules that there is one bang.
2. The threshold route's standing: R10 (BH-S1's restore) is load-bearing. David derives "the rate 0 gives nothing" for the time gear's own step, or the owner rules on a ceiling trigger for law 4 beside the floor.
3. The 24 of the split forms. The 00 equation's exact integer rewind in X (its velocity term), or the time gear on the area Y = a^2 (where (R) is a pure brake). The lattice's kinetic measure at the quarter turn (u_in u_out = 0).
4. A setting that lays the light with a moving time gear. run_volRv_500_60.txt is not evidence: setting X- by hand breaks the hands' momenta, which are read at the mean teeth.
5. The unspringing's books opening by one unit (the head's: hole tick 79; bang at 2,000 quanta tick 51).
6. Newton's constant from kappa = d / (Gamma key), and the owner's 18:5x sentence against the derived push's first step.

## 11. The probes (run with /home/user/Universe24/venv314/bin/python -I; ROOT is S/t24 or S/derive/C/work)

| file | what it does | outputs |
| --- | --- | --- |
| course.py ROOT DRIVE QUANTA TICKS [REWIND [TRACE or - [FROM]]] | the one big bang world with a drive (pure: the tree's own). Reads the stretch per tick, the whole-board turnovers (and whether every Node-clock is stopped then), the local turnovers, the falls of the first difference, the births, the books per click phase (test_the_record's form) and the rewind (tests.laws.run_back_exact from tick FROM) | probe_*.txt, run_*.txt, work_probe_*.txt, work_pure_*.txt, t24_vol0_5M_30.txt |
| drives.py | the head's impulse and carry copied line for line (bit for bit: state hash 03e86dd8c8abf664 at 500 quanta and 40 ticks, alike for the tree's own and the copy), the forms split into K, G, V, and the drives: head, nocap, vol0 (derived push), vol0_free (BH-S1's restore struck), volL, volR, volK2 | trace_*.txt: tick, going, X, forms, trace, rate, N, hold[, K, G (over T), V (over T)] at (0, 0, 0) |
| monotone.py ROOT DRAWS | C2 on the head's acts.carry, with random states | monotone.txt |
| books_open.py, books_world.py | the open books' phases under a drive, and the head's own click on any world | books_open_volK2.txt, books_*.txt, work_books_*.txt |
| world_course.py ROOT WORLD TICKS | the stretch's range, the turnovers and the births on any world | head_hole_course.txt, work_hole_course.txt |
| work/ | S/t24 copied (cp -r), with the derived push built in (work_drive.diff.txt) | work_*.txt |

Animate's readings as read: ref/ANIMATE-TENSOR24-READINGS.md (reader-5 7435272d, through the GitHub API, read-only).
