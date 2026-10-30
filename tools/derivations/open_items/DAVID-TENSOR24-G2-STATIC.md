# G2, the static field on the slot form: what the clocks and light read, and why gamma = 1 brings beta = 1

David, 2026-10-30, on the owner's word of 11:1x UTC (derive what the Node-clock needs to close; everything to stand with
a hostile mathematician and a hostile physicist), for the architecture document's terms 2, 3, 5 and 13. It reads the act
as built on main (0df0e8385) and N2's source for term 5 (the Boss's draft, derive/boss/n2). The probe is
derive/david_open/node/g2_static.py, its output g2_static.txt beside it, whole numbers alone, about 6 s.

**The finding in one line:** on the slot form the act gives the post-Newtonian beta = 2 - gamma exactly at second order,
because every grip reads the ii slots at both ends of its Mesh. So if term 5 pushes each slot in the unit its own
reading uses, gamma = 1 and then beta = 1, which is general relativity's static field to the order the solar system
tests.

## 1. In clocks

- **The teeth are time.** A Node-clock's teeth are the rest plus its clock family's 00 slot. Every gear there turns by
  those teeth, so a deeper 00 slot slows every clock at that Node-clock alike. A clock's beat goes as the root of its
  spring over its teeth.
- **The grips are length.** A Mesh's grip is the rest grip plus the ii slot of its axis at both of its ends. Light's
  beat goes as the root of the grip over the teeth, so light crosses a slack Mesh more slowly.
- **Near a mass** the 00 slot rises and the ii slots fall, each by the mass's push in its own unit: the clocks there run
  slow and the Meshes slacken, and light passing by is slowed by both.
- **The field's own weight.** The 00 slot is itself pulled through those grips. Where the Meshes slacken, the 00 slot's
  pull weakens, so it rises a little more. That extra rise is second order, and it is exactly what general relativity
  asks of it.

## 2. On the board

**The readings** (CHECKED on the act, probe (a) and (b)).

- A gear on a spring s at teeth W beats at 4 sin^2 (omega / 2) = s / W. So a clock's rate against a clock at the rest
  teeth is N with N^2 = rest / W at a small beat. Probe (a): 64, 32 and 21 sign changes at W = rest, 4 rest and 9 rest,
  as 1, 1/2 and 1/3.
- Light on the lattice beats at 4 sin^2 (omega / 2) = (grip / W) 4 sin^2 (k / 2); on the ring's mode (1, 0, -1, 0),
  2 grip / W. Probe (b): 746, 369, 1,568 and 746 at (W, grip) = (rest, g), (4 rest, g), (rest, 4 g) and (4 rest, 4 g):
  only grip / W counts.
- Write u = c00 / rest for the 00 slot and v for the ii slot over the grip g at each end, so a Mesh's grip is
  g (1 + v_i + v_j), g (1 + 2 v) where the field is smooth. The clocks read N^2 = 1 / (1 + u); light reads the
  coordinate speed N / A with A^2 = (rest / g) / (1 + 2 v).
- So in the post-Newtonian form, -g00 = 1 + 2 Phi + 2 beta Phi^2 and g_ii = 1 - 2 gamma Phi, with Phi the Newtonian
  potential (below 0 near a mass): u = -2 Phi at first order (the Newtonian limit), and v = gamma Phi at first order.
  That last line is what gamma is, read in the slots.

**The second order, exact on the lattice** (DERIVED; probe (c) and (d)).

- Outside the matter, the 00 slot stands still where the pull on it is 0: the sum over the six Meshes of
  (1 + v_i + v_j)(u_j - u_i) = 0, the grips read at both ends.
- Split u = u1 + u2, with u1 the first-order field (the lattice Laplacian of u1 is minus the source) and v1 = -(gamma /
  2) u1. Then the sum of (u2_j - u2_i) equals minus the sum of (v1_i + v1_j)(u1_j - u1_i), which is (gamma / 2) times
  the sum of (u1_j^2 - u1_i^2). That is an identity on the lattice, not a limit: (u1_i + u1_j)(u1_j - u1_i) = u1_j^2 -
  u1_i^2.
- So u2 = (gamma / 2) u1^2 = 2 gamma Phi^2, with no harmonic remainder where the field vanishes far away.
- Then N^2 = 1 / (1 + u1 + u2) = 1 + 2 Phi + (4 - 2 gamma) Phi^2 to third order, so **beta = 2 - gamma.**

**gamma, from term 5's source** (DERIVED, given N2's source).

- N2 pushes the ten slots by 2 T-bar, the trace-reversed stress: J00 = rho + 3 p and Jii = rho - p. For matter at rest
  (p = 0) J00 = Jii = rho: the 00 slot and each ii slot get the same push.
- In the metric's own terms that push is h_00 = h_ii, which is gamma = 1. In counts, each slot carries its metric
  component in the unit its reading uses:
  - the 00 slot in teeth, c00 = rest h00;
  - each ii slot in grips, inverted and counted at both ends of a Mesh, c_ii = -(g / 2) h_ii.
- So the ii slots' push is -g / (2 rest) = -1 / 12 of the 00 slot's (rest = 6 g). That is N2's "strengths per slot",
  OPEN there, fixed here by the readings. Other values give gamma = -12 c_ii / c00.
- With gamma = 1, beta = 1 follows with no choice left. With any other gamma, beta = 2 - gamma, so:
  - Nordtvedt's eta = 4 beta - gamma - 3 = 5 (1 - gamma);
  - the perihelion's factor (2 + 2 gamma - beta) / 3 = gamma.

## 3. In the clicks

The physics is read after the clicks, never on the board. These are the readings of the decoder's light (owed), each a
ratio of counts and arrival rounds between clocks that exchange light; no slot ever reaches the record.

- **Clocks.** Two clocks at different 00 depths click at rates in the ratio root (W_B / W_A): the gravitational
  redshift. Pound and Rebka 1960; Gravity Probe A (Vessot and others 1980) to 7 x 10^-5; the eccentric Galileo
  satellites (Delva and others 2018; Herrmann and others 2018) to about 2.5 x 10^-5.
- **Light.** A quantum sent past a mass arrives late and bends, by (1 + gamma) / 2 of general relativity's. Cassini
  (Bertotti, Iess and Tortora 2003): gamma - 1 = (2.1 +- 2.3) x 10^-5.
- **Orbits.** A perihelion advances by gamma times general relativity's when beta = 2 - gamma. Mercury's ephemeris holds
  beta - 1 near 10^-4 or below (Park and others 2017, with MESSENGER's ranging).
- **The strong equivalence principle, in its static part.** Lunar laser ranging bounds Nordtvedt's eta at about 10^-4;
  here eta = 5 (1 - gamma), 0 at gamma = 1. So the standing field's binding falls as nature's does at this order. That
  answers, at second order, the item I left OPEN on N2 (6521577088, item 2). The waves' own energy as a source stays
  OPEN there.
- **Departures, named:** none in the static weak field at gamma = 1. The shift (the 0i slots: frame dragging, the
  preferred-frame parameters) and the time-dependent field are not read here (section 5).

## 4. Term 13, the frozen clock: what this gives and what stays open

- A clock freezes where its teeth grow without bound: N^2 = 1 / (1 + u) goes to 0 only as u does to infinity. In the
  weak field u is small, and to second order it is general relativity's.
- **Where the grips vanish**, 1 + 2 v = 0, light's speed is 0. With v = gamma Phi, first order in v, that is at
  Phi = -1 / 2: for one mass r = 2 gamma G M / c^2, Schwarzschild's radius at gamma = 1.
- **Whether the clocks freeze there too**, so that the clocks stop where light stops (a horizon), is the strong field's
  question. It turns on the ii slots' own equation past first order and on N2's metric self-push onto them. One reading
  shows it is not given for free. Let v obey the same pull with no self-push: (1 + 2 v) v' r^2 is constant outside one
  mass, so 1 + 2 v = root (1 - 4 gamma G M / (c^2 r)). That vanishes at r = 4 gamma G M / c^2, as a root, and there
  u' = D / (r^2 (1 + 2 v)) is integrable, so u stays finite and no clock freezes. OPEN, on the act.
- No hold and no restore: whatever freezes is the act's own result, as the architecture document's term 13 says.
  Postulate 4 (no Node-clock frozen for ever) is a condition the strong field must meet.

## 5. Measured (g2_static.txt)

| Check | Result |
|---|---|
| (a) a clock on a spring at W = rest, 4 rest, 9 rest | 64, 32, 21 sign changes in 4,000 rounds (times 1, 2, 3: 64, 64, 63); the run back bit for bit |
| (b) light on the ring's mode, (W, grip) = (rest, g), (4 rest, g), (rest, 4 g), (4 rest, 4 g) | 746, 369, 1,568, 746: the same grip / W, the same count |
| (c) the sum of (v_i + v_j)(u_j - u_i) against minus the sum of (u_j^2 - u_i^2) where v = -u | equal at all 216 Node-clocks of a whole field |
| (d) ((1 + u) G - 1) q^4 at Phi = -1 / q, q = 10^3, 10^4, 10^5, G = 1 + 2 Phi + (4 - 2 gamma) Phi^2 | of order q for gamma 0 and 2 (8,000 to 800,000 and their negatives), 4 for gamma 1: third order or less |

## 6. What stands (rows for the architecture document)

- **Term 2, the teeth:** clocks read N^2 = rest / W (CHECKED on the act).
- **Term 3, the grips:** light reads grip / W, the grip at both ends of a Mesh (CHECKED on the act).
- **Term 5's strengths per slot:** each slot pushed in the unit its reading uses, the ii slots at -1 / 12 of the 00
  slot's, which gives gamma = 1 (DERIVED from N2's source and the readings). Then beta = 1 (DERIVED, exact at second
  order on the lattice).
- **Term 13:** where the grips vanish, light stops; whether the clocks freeze there is OPEN, on the act.

## 7. OPEN

- **The sign in code:** N2's probes push the ii slots with the 00 slot's sign. The change is a strength, not a new rule:
  -1 / 12 of the 00 slot's.
- **The strong field and the horizon** (term 13), as in section 4.
- **The shift and the shears** (the 0i and jk slots, term 10, G4): frame dragging, and the preferred-frame parameters
  alpha_1 and alpha_2.
- **The time-dependent field:** gravitational waves ride the same grips and teeth as light, the 00 row's own teeth at
  rest, so their speed is light's in the weak field (GW170817: within about 10^-15); to be read on the act with N2.
- **The volume's notch** (term 9) and its swing: not read here.

