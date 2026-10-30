# Notes 05: what P1 measured (probe_p1_lockin.txt), and the coefficient of v^2 on paper

## A. Free from v0 = 1 (W0 = 10^4 and 10^5), 10^6 rounds; stride every round, dA over the 10^4 rounds before each mark
- symmetric: W = W0 + t exactly to 10^6 rounds (dA = 10000 in every window): the lock-in holds for 100 W0. Against
  nature's course (4 W^3 / (W0 (2 W0 + 3 t)^2)): 1280, 2115, 5199, 14078, 45186 permille at t = 10^4, 3x10^4, 10^5,
  3x10^5, 10^6: W is 1.09, 1.28, 1.73, 2.41, 3.56 times nature's, growing as t^(1/3) without bound. The ORDER (the act
  as built) gives the same W at every mark: at v = 1 the root form is the as-built clock.
- carried: v = 1 until t = W0 (the tooth reaches the bottom), then the quotient alternates 1, 0, 1, 0 for ever (9999
  changes in every window of 10^4): v = 1/2 exactly, locked; the register E = t - W0 + 1 grows one count a round without
  bound (E = 990,001 at 10^6 against the edge's dial 2 W = 1,030,000: the dial on alternate rounds is 2t and 40,000).
  W = 514,999: 1.81 times nature's. The text's "pumped for ever" confirmed to 10^6 rounds.
- twin: A frozen at 2 W0 - 1 for ever; B = W0 + t: the parting grows as t (A - B = -990,001). The halves' mean, 515,000,
  is the carried dial's course.
- At W0 = 10^5 the same picture scaled by 10.

## B. Free from v0 = 3 and 2 (W0 = 10^6), 3 x 10^6 and 2 x 10^6 rounds
- symmetric: v falls 3 -> 2 -> 1 at about the right times: W within 962 .. 1204 permille of nature's W^3 (within 7
  percent in W) to 3 x 10^6 rounds; at v = 1 (from about 1.6 x 10^6) locked, running linearly, so it will overtake
  nature's t^(2/3) later. By windows of 10^4 rounds the velocity is exactly an integer (dA = 20000 or 10000, no
  jitter): v^2 W by windows swings 963, 1407, 1852 (v = 2), 537, 648 (v = 1) permille of v0^2 W0: the invariant
  sqrt(W) v is not kept by windows at |v| <= 3; only the integrated course is, to 7 percent.
- carried and twin: W v kept to within 8 percent (Wv 916 .. 1081); v = 1 held from 5 x 10^5 on with E = +-2 and
  A - B = -7: no pump, no parting yet (the half count is not reached within the run). Order: v = 3 for ever.

## C. One kick from rest (W0 = 10^4; 4 push = 2 W0 at round 0, nature's v = 1/2)
- symmetric: q = 1 at every one of rounds 0..11 and for ever: v = 1 from a kick nature reads as 1/2; W = 1,010,000 at
  10^6 rounds, W^3 178 times nature's (W 5.6 times). The order: identical at every mark.
- carried: q = 1, 0, 1, 0 from round 0 (v = 1/2 in the mean, nature's at first), E = t exactly; W = 510,000 at 10^6.

## D. A constant small push, one count every k rounds (F = 1/k), from rest at W0 = 10^4, 10^6 rounds
- On paper the symmetric form's v = n is stable iff n(n-1) <= 2F <= n(n+1): the integer nearest sqrt(2F) with a floor at
  1. Measured: F = 1/4 (nature's v = 0.707): symmetric v = 1 locked from 3 x 10^5 on (v^2 / 2F = 2000 permille);
  F = 1/16 (0.354): v = 1 (8000); F = 1/64 (0.177): v = 0 until the tooth fills (3.2 x 10^5 rounds), then v = 1 (32000).
  The order identical at every mark. So below F = 1/8 a round the root form's clock runs at one count a round where
  nature's runs at sqrt(2F): 1.4, 2.8, 5.7 times too fast at these three pushes, bounded.
- carried: once at the half count the register's alternation makes the velocity's weight alternate between a frozen
  small dial and a growing one, and a push then amplifies the velocity: v^2 / 2F = 720 -> 19220 -> 95221 -> 283221
  permille at F = 1/4 (v = 11.9 counts a round at 10^6 rounds, 17 times nature's); 80 -> 72000 at F = 1/16; the twin
  about twice that (v = 23.8 at F = 1/4). A runaway, unbounded, where the symmetric form's error is a bounded factor.
  CONTROL (P4): the pushes above have even periods, which could resonate with the register's period 2; odd periods and
  an aperiodic push are measured in probe_p4_push_control.txt before this is stated as generic.

## The coefficient of v^2 is a choice (notes_02 D10, sharpened)
With W = rest + a and a lapse-only metric ds^2 = -(rest / W) dt^2 + dx^2, four "derivations" give four laws for the
00 row's own uniform motion, W a'' + c a'^2 = F:
  c = 0: the act as built / the order (a flat d'Alembertian: v kept);
  c = 1/4: the covariant scalar action in that metric, L = (1/2) sqrt(W/rest) a_t^2 - (1/2) sqrt(rest/W) (grad a)^2,
       whose Euler-Lagrange time part is W a'' + a'^2 / 4 (W^(1/4) v kept);
  c = 1/2: the test-field equation of mc_phys item 1 applied to the lapse itself, the symmetric form (sqrt(W) v kept);
  c = 1: the edge (W v kept).
GR gives the lapse no equation of its own (a uniform lapse is a time coordinate; with flat slices and no shift the
Hamiltonian constraint leaves N no dynamics), so nature picks none of the four; the text's "nature's form" is the
c = 1/2 choice, dressed as a reading of nature and attributed to "the physicist", whose derivation was for a test
field under a lapse, not for the lapse. The one honest sense of the text's choice: the 00 gear's own clock beats as
every other clock at its site does.
