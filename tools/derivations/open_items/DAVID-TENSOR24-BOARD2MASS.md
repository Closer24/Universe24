# Board to mass: how a mass enters on the board, how it comes out in the clicks, and what the 24 say of three generations

David, 2026-10-30, 04:1x UTC, on the owner's words to David (in Hebrew; in translation):

- 03:0x UTC: "Prepare a page on this that everyone will agree on... board2mass. It has to explain why nature also shows three generations... On the board a mass is a spring with a coupling: what is the formula has to be understood. First you, then a hostile mathematician agent and a hostile physicist agent go over it after you finish. From the clocks, understand what the transformation from the board to the clicks is. And why those ratios are seen in the clicks, and why there are 3 generations, with all their ratios and properties."
- Before it: "How a mass enters the board, in the four dimensions of the events' spacetime, and how it comes out of the click, whose spacetime is three dimensions, has to be understood, no?" (Sofer's 8.2: both are 3 + 1, and what differs is which 1.)

Animate's reading of the mass and the clock (#2187 6514375401, on the owner's word to her: "Pass to David what you think about the mass and the clock, because he centres it") stands here whole as the clicks' side (section 3).

Probes, in whole numbers alone (the owner's word through Sofer, 6514488548: "Only whole numbers are allowed"), each with its output beside it in derive/david_open/mass/, on tensor24-review 2a6203a4a:

- m1_kinds.py: which subgroups of the 24 a held count of each kind keeps, and how many masses a spring that keeps the subgroup can give a three-component gear;
- m2_spring.py: the spring each held kind gives a three-component gear, read from the act's own tables;
- m3_beat.py: the beat on the head's own gear and tick: what is a mass and what is not, the held count's drift, two runaways.

Only the Boss writes engine code (decision 40). This page is a derivation and its checks, nothing more. Two hostile readers, a mathematician and a physicist (the owner's ask), read it beside the next stage, and their findings fold at the next push (decision 43). The status words are the protocol's: DERIVED (follows from the law and the act as built), CHECKED (a probe shows it), OPEN (neither), REFUSED (nature or the law refuses it).

## 0. The answer in short

- **On the board, a mass is a gear held by a spring inside its own Node-clock.** Light's gear is meshed only sideways, to its six neighbours. A massive gear is also meshed inward, through a three-leg vertex, to a held count at its own Node-clock. Because the held count stands still, the vertex pulls the gear back toward 0 in proportion to its own value: a spring, D = g C n (the coupling's strength, the 24's table entry, the held count).
- **The formula** is the step itself: W (a+ - 2a + a-) = grip sum over the six Spokes (a_s - a) - D a. A wave of wave number k beats omega a round with W (2 - 2 cos omega) = grip sum_i (2 - 2 cos k_i) + D. At long waves omega^2 = c0^2 k^2 + D / W, with c0^2 = grip / W = 1/6: the rest beat is omega0^2 = D / W, and that rest beat is the mass.
- **In the clicks, a mass is a ratio of counts:** a clock's rest beat in its own ticks, read side by side with another clock. The round never reaches the clicks, and motion cancels (a moving clock beats slower per round and the same per its own tick). Two masses compare by squares, m_A^2 / m_B^2 = D_A / D_B, a ratio of whole numbers.
- **Why three:** a family of species alike in every way but mass is the components of one kind of the 24. The 24's kinds have 1, 1, 2, 3 and 3 components, so the largest family is three, the number of the board's axes, and never four. That holds under one condition: no coupling reads the family's components against a direction of the board.
- **Why their masses differ:** a held count of kind A1 or A2, the plan's two candidates, gives the three components one mass. Three different masses need a held count of kind E, with both of its components, or, on a hand of two parts, a T1 count along one line.
- **What does not follow:** the ratios' numbers. Three masses take three numbers, and the split's form (a + B cos (phi + 2 pi k / 3)) has three parameters, so the form alone predicts nothing. Koide's 2/3 is a test, and on whole counts in its own reading it can be approached but never met exactly (section 6.2). Mixing, spin, and the step that a mass joining two hands needs are open.

## 1. What nature shows

The facts the page has to meet (PDG 2024 unless named):

- **Three generations, no fourth light one:** the Z's width counts the light neutrinos, N = 2.9963 +- 0.0074 (LEP, with the 2020 luminosity correction of Janot and Jadach; 2.9840 +- 0.0082 in the 2006 combination). A fourth family's heavy quarks would raise the Higgs boson's production by gluons about ninefold, which the LHC refuses.
- **The generations are alike but for mass:** the same charges and the same spin one half in each; lepton universality holds to a few parts in a thousand.
- **The masses are far apart:** charged leptons 0.51099895 MeV, 105.6583755 MeV, 1776.93 +- 0.09 MeV; up quarks about 2.2 MeV, 1.27 GeV, 172.6 GeV; down quarks about 4.7 MeV, 93 MeV, 4.18 GeV; neutrinos below 1 eV, with squared differences 7.4 x 10^-5 eV^2 and 2.5 x 10^-3 eV^2.
- **The generations mix:** the quarks' mixing has the Cabibbo angle, |V_us| = 0.2243; the neutrinos' has large angles, theta12 about 33.7 degrees, theta23 about 42 to 49 degrees, and theta13 about 8.6 degrees (Daya Bay and RENO, 2012).
- **Koide's relation** (Koide, 1982): K = (m_e + m_mu + m_tau) / (sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 0.6666645 +- 0.0000051 from the masses above, against 2/3, within half its error. In Brannen's form (2006), sqrt m_k = mu (1 + sqrt 2 cos (delta + 2 pi k / 3)) with delta = 0.222225, against 2/9 = 0.222222.
- **The masses hold still:** atomic clocks bound the drift of the proton-to-electron mass ratio at -8 +- 36 parts in 10^18 a year, and of the fine-structure constant at 1.0 +- 1.1 (Lange et al., 2021).
- **A short life is a broad mass:** width times life is hbar; the Z's width 2.4952 GeV is a life of 2.6 x 10^-25 s.
- **Inertial mass is gravitational mass:** MICROSCOPE (2022) bounds any difference at about 10^-15.

The Standard Model holds all of it with three copies put in by hand and the masses and mixings from couplings to the Higgs field's held value (246 GeV): thirteen free numbers for the charged fermions' masses and mixings alone, and no reason for three.

## 2. Mass on the board: a gear held by a spring

### 2.1 At the clocks' level

- **Light** is a gear meshed sideways only, through its Node-clock's six Meshes to the six neighbours' gears. A light wave that is the same at every Node-clock is pulled by nothing, so it does not beat. On the head (CHECKED, m3 (a)): the uniform wave laid at rest stands at 1 for 60 rounds, and laid moving it drifts 2, 3, 4, and so on, with no beat.
- **A mass** is a gear meshed inward as well, to a held count in its own Node-clock, through a three-leg vertex C[X; K, X] whose legs are the held count K and the gear X twice.
  - The held count is the coupling family's gear standing at its steady count, one quantum per Node-clock (decision 40 (g)). It is the same at every Node-clock, so the Meshes pull it by nothing, and it has no rate, so it does not move by itself.
  - Since it stands, the vertex's push on X is linear in X and points back toward 0: a spring. D = g C n, the coupling's strength g, the 24's table entry C and the held count n.
  - Everything is inside one Node-clock, so the spring keeps the Node-clock's law (line 92): it reads its own state and its six neighbours alone.

### 2.2 The formula

- **The step** (the head's gear, engine/step.py): W (a+ - 2a + a-) = push, the carry keeping the remainder in the fine tooth. With the Meshes' pull and the spring:
  - W (a+ - 2a + a-) = grip sum over the six Spokes (a_s - a) - D a.
  - On the head 6 grip = W exactly (grip 3881691330332771584000000, W 23290147981996629504000000; the loader's teeth at rest 6 den Gamma^2 G^2 and its grip den Gamma^2 G^2 per Mesh). CHECKED, m3 (a).
- **The band** (DERIVED, the step's identity on a wave of wave number k): W (2 - 2 cos omega) = grip sum_i (2 - 2 cos k_i) + D.
- **At long waves:** W omega^2 = grip k^2 + D, so omega^2 = c0^2 k^2 + omega0^2 with c0^2 = grip / W = 1/6 (light's 1 / sqrt 6 Mesh a round) and omega0^2 = D / W. That is the relativistic form E^2 = (p c)^2 + (m c^2)^2 with hbar one round: **the rest beat omega0 is the mass, and its square is the spring over the teeth.**
- **Checked by counting, with no cosine** (m3 (b)): at D = W div k^2 the uniform wave's sign changes over 20,000 rounds, times k, read 6368 at k = 8, 16 and 32, and 6336 and 6400 at k = 64 and 128, where the count is 99 and 50: one number, about 20,000 / pi. So the beat goes as the root of the spring, and the mass's square as the spring.
- **Exact periods** where the step allows them (m3 (b)): 6, 4 and 3 rounds at D = W, 2W and 3W.
- **The heaviest mass the board holds** (DERIVED, CHECKED): the top mode, every neighbour opposite, is pulled by 12 grip = 2W, so its step reads a+ = (-D / W) a - a-, which holds only while D <= 2W. At D = 2W it grows by two starts a round (49 times its start at round 24), and at D = 3W it runs away (17,393,796,001 times its start in 24 rounds). So every mass beats below a quarter turn a round. The size of D / W is the board's, unmeasured: if a round were the Planck time, the electron would need D / W of about 2 x 10^-45. Only ratios reach the clicks (section 3).

### 2.3 What is not a mass

- **The lone gear's 6-round beat** (the example's gear, Animate's item 4): with its six neighbours at 0, the pull is -6 grip a = -W a, so the step reads a+ = a - a-: 1, 0, -1, -1, 0, 1, period 6 exactly (CHECKED, m3 (a)).
- **Its neighbours never carry:** each is pushed by grip a = W a / 6, so its fine tooth climbs to W / 3 over the beat and comes back. None moved in 60 rounds.
- **So it is the board's own lone-site mode**, a gear pinned by still neighbours, not a mass: the uniform wave, which is the mass's test, does not beat on the head. A mass is the beat that stays when the neighbours move with the gear, the k = 0 end of the band.

### 2.4 The held count needs a law that holds it

- **The vertex pushes all its legs** (the plan's G3 line: "only three-leg vertices, each pushing all its legs"). From the potential (g/2) K X C X, the held count is pushed by -(g/2) X C X. For an A1 count that is -(g/2) X X, whose mean over a beat is below 0 and not 0.
- **On the gear rule it drifts** (CHECKED, m3 (c)): K laid at 10^6 with X at 10^5 and D = g K = W div 400 falls to 800,187 by round 250 and to 142,793 by round 500. It passes below 0 at round 537, the spring turns over, and X runs past 10^60 by round 686. With a spring of its own (W div 16) the count stays between 999,559 and 1,000,243 over 2,000 rounds.
- **Three-leg vertices alone hold no count** (DERIVED): a potential of three-leg vertices is a cubic form V, with V(t phi) = t^3 V(phi). At any stationary phi* that is not 0, Euler's identity gives 3 V(phi*) = phi* . grad V(phi*) = 0, and grad V(t phi*) = t^2 grad V(phi*) = 0 for every t. So the whole ray through phi* is stationary and flat, and nothing pulls the count back along it.
- **So G3's held count needs a term that holds it:** a spring of its own (a two-leg term) or a one-leg term, or the law's "one quantum per Node-clock" as an act. Nature's held value, the Higgs field's 246 GeV, is held by its potential, whose curvature is the Higgs boson's mass of 125 GeV: a two-leg term and a four-leg one, not three-leg vertices. That is G3's toy, bounded at lambda = 1/Gamma (OPEN), and the drift above is what the toy must refuse.

## 3. From the board to the clicks: what the clocks do

- **The two spacetimes** (8.2): the board is 3 + the tick, and the clicks are the same 3 + each clock's own count. The mass enters on the board as the uniform wave's beat in the tick, made at every Node-clock by its own spring. It comes out in the clicks as a clock whose rate is its mass. The tick cancels, as it cancels in the click's shadow.
- **The transformation, through the clocks** (DERIVED at long waves, the Boss's D7, 8.1 item 10):
  - a packet of the massive gear moving at v beats, at its own place, omega - k v = omega0^2 / omega = omega0 sqrt (1 - v^2 / c^2) a round: slower per round, which is time dilation;
  - its own ticks run slower by the same factor, so per its own tick it beats omega0, whatever its motion. That is Animate's reading: **the mass is the rest beat counted in the clock's own ticks, invariant, with no formula** (decision 37).
- **What the clicks can read is a ratio** (DERIVED): a clock's own beat counted against itself is 1. A mass is read as one clock's beats against another's, side by side at rest, as an atomic clock is read against a caesium clock, or as an atom's Compton frequency was read against a clock (Lan et al., 2013).
  - The round's unit cancels in the ratio: no one measures the board.
  - On the board the ratio is omega0_A / omega0_B, so the clicks compare masses by squares with no root: m_A^2 / m_B^2 = D_A / D_B = (g C n)_A / (g C n)_B, a ratio of whole numbers. Every row has the same teeth W, so W cancels too.
- **The width is the clock's life** (Animate's reading; agreed): a beat counted over few of its own ticks is spread, over many sharp. Nature's width times life is hbar. On the board a spring with no way out beats sharp. A three-leg vertex to lighter trains drains the beat, and its life sets the width. OPEN on the act (G5, G6).
- **The least a clock needs** (Animate, 6514643547, on the owner's word to her: "Pass it to David, it will help him"):
  - to tick, a Node-clock with its six neighbours, never one alone (2.3);
  - to click, two clocks, a giver and a taker with parts;
  - to show a sharp mass, many of its own ticks (its life) and enough Node-clocks to stay together (its span).
  So the least mass the clicks can see is set by the simplest clock that can both take and live long, not by the watcher.
- **Gravity reads the same beat** (DERIVED from decision 40 (a), read under the owner's law of 04:1x, line 102: no books in the engine, a push read by the tensor operation itself from every gear's state): what the tensor operation reads from a beating gear, its rate, its differences and its spring's part, pushes the metric's 00 slot by rho + 3p, as for every train. So the inertial mass, the beat, and the gravitational mass, what the metric reads, are one count, which is the equivalence MICROSCOPE tests.

## 4. Three components, three species: what the 24 give

### 4.1 The kinds

The 24's turns, made from the Node-clock's six Spokes, have five kinds of 1, 1, 2, 3 and 3 components (CHECKED, m1 line 1: A1 and A2, E, then T1 and T2). A train of kind T1 has three components, turned among themselves by the 24 as the three axes are.

### 4.2 Why a T1 train is three species alike in the clicks

- **The step is blind to the component** (CHECKED on the head): every row of every train steps at the same teeth W, and the loader lays one grip, den Gamma^2 G^2, on every Mesh for every row (load.geared). So the three components of a T1 train each step as the same wave, at the same light speed.
- **The vertices at one Node-clock read components, not places.** A turn of the 24 applied to the components alone, with the places left where they are, keeps the pull, which is blind to the component, and keeps every vertex whose legs are all read at the Node-clock itself, since the tables are the 24's own. So the family's components can be turned among themselves apart from the board's places.
- **In the clicks the three components are then three species**, alike in everything the 24 keep alike: the same speed, the same spin and the same couplings through A1. Their pair to A1, T1 x T1 -> A1, is the dot product, x with x, y with y and z with z, so an A1 train such as light couples to the three alike: universality.
- **The condition** (OPEN, G3's to keep): no coupling row reads the family's components against a direction of the board, whether the gradient (a T1 reading of an A1 train, made from the Spokes) or a train whose components are the board's own directions (the metric's 0i slots, T1; its jk slots, T2; its E part). If one does, the components turn with the places, and the clicks would see a turn of the laboratory change one species into another. Nature refuses that, to the precision of the clock comparisons. The stress the tensor operation reads from a T1 train is a sum over its components, so decision 40 (a) keeps the condition.

### 4.3 Why three, and never four

DERIVED under the condition: a family alike in all but mass is one kind's components, and the 24 hold no kind of more than three. So a family is one, two or three species, and three is the number of the board's axes. Nature's N = 2.9963 +- 0.0074 agrees. What does not follow (OPEN): why every one of nature's fermion families is a triplet and none is a single or the E pair, and how spin one half rides on a T1 train (the twin kinds wait on OPEN 3). A hand of three parts loads at 5176be5e0 (the part's check is out), but that three is the files' choice, an internal one, and explains nothing; the 24's T1 is the three the page derives.

## 5. Three masses: what splits the triplet

### 5.1 The plan's two candidates give one mass

- **Schur's lemma, CHECKED** (m1): a held count that keeps the whole 24 is of kind A1 alone, and any spring it gives a T1 gear has one value. A count of kind A2 keeps the even half A4, under which T1 stays one irreducible triplet, so it too leaves one value, on a real gear and on a hand of two parts alike.
- **On the act's tables** (CHECKED, m2): C[A1, T1 -> T1] is the identity, so an A1 count gives the three components one spring. C[A2, T1 -> T1] is zero (A2 x T1 is T2), so an A2 count gives T1 no spring at all. It only mixes a T1 train with a T2 train (C[A2, T2 -> T1] is the identity), and the pair's masses solve (lambda - a)(lambda - a') = b^2: two values, each three alike.
- **So the plan's A1 or A2** (decision 40 (h), "its kind, A1 or A2, is David's") gives three generations of one mass. Nature refuses it.

### 5.2 An E count gives three

- **On the act's tables** (CHECKED, m2): E's two components give the diagonal springs diag(1, -1, 0) and diag(0, 1, -1), each with trace 0. An A1 + E count (n0; e1, e2) gives the three springs n0 + e1, n0 - e1 + e2 and n0 - e2, times g.
  - They sum to 3 n0, and their spread about the mean is 2 (e1^2 - e1 e2 + e2^2) (checked at every |e1|, |e2| <= 9).
  - Two of them meet only on three lines, e1 = -e2, e2 = 2 e1 and e1 = 2 e2. Of the 48 whole (e1, e2) in [-3, 3]^2 other than (0, 0), 38 give three masses.
- **By the subgroups** (CHECKED, m1): an E count with both components off those lines keeps only the three half turns D2, under which T1 splits into three different one-dimensional kinds, so three masses. On one of the lines it keeps D4, and T1 splits as one plus two.
- **What it costs on the act:** the files' checker refuses a train of kind E on its own (runner/files.py at 5176be5e0: "a kind with no whole basis the 24 permute stands only in the four-vector's square, whose basis is whole"). E loads inside the metric's square and nowhere else, so an E held count is a kind the act cannot hold as built.

### 5.3 On a hand of two parts

- **A T1 count along one line splits the triplet on a hand** (CHECKED, m1: Z3 and C4 give three values on a hand and two on a real gear). Its table is the cross product (m2: antisymmetric), which on a hand reads as the hermitian i M, with values 0 and plus and minus |v| (m2: lambda^3 - 3 lambda for v = (1, 1, 1)).
- **With A1 and T2 along the same body diagonal** it is the complex circulant a + b P + b* P^T, with three values (m2: lambda^3 - 15 lambda^2 + 60 lambda - 54, discriminant 13068). Its mass basis is the Z3 Fourier basis. A T2 count alone along that diagonal is the real circulant, with a pair alike (m2: lambda^3 - 3 lambda - 2, discriminant 0).
- **On a real gear the same count is no spring:** its push is antisymmetric, x M x = 0, and the gear runs away (CHECKED, m3 (e): -1,602,744, then 41,579,439, then -1,481,206,931 at rounds 100, 200 and 400). How a hand reads i M depends on how the coupling plan joins its two parts (OPEN, G3).

### 5.4 The form, and why it predicts nothing alone

Any three springs that sum to 3a can be written a + B cos (phi + 2 pi k / 3), k = 0, 1, 2, with B from the spread and phi from the direction of (e1, e2) in E's plane. That is Brannen's form, here for whichever reading the springs give (section 6.1). But three masses are three numbers, and the form has three parameters, so it says nothing alone. A prediction needs the law to fix B / a and phi, that is, the held counts n0, e1 and e2 and the vertex strengths. That is G3's vertex law, and it is OPEN.

## 6. The ratios: what the form says and what it does not

### 6.1 Nature's numbers in three readings

The charged leptons in the form a + B cos (phi + 2 pi k / 3), read on three quantities:

| reading | B / a | lightest / a | where the board's step gives it |
| --- | --- | --- | --- |
| the squares, m^2 | 1.98944 | 2.47 x 10^-7 | the second-order gear as built: D / W = omega0^2 |
| the masses, m | 1.83341 | 8.14 x 10^-4 | a first-order step (OPEN, N2's form) |
| the roots, sqrt m | 1.41421 (sqrt 2 = 1.414214) | 0.0404 | none named |

- **On the squares**, the reading the board's gear gives, the electron is a remainder: the A1 count and the E count must cancel to 2.5 parts in 10^7 at the electron. A law of whole counts would have to explain that cancellation, so it stands against the squares' reading unless one does (OPEN).
- **On the roots** the cancellation is to 4 parts in 100, and B / a is sqrt 2 to five digits. That is Koide's relation (6.2). The board names no step whose spring is the root of a mass.

### 6.2 Koide's 2/3 on whole counts

- **The reading:** if the three values n0 + mu_k (section 5.2) were the roots of the masses, Koide's ratio would be sum d^2 / (sum d)^2 = 1/3 + spread / (9 n0^2), and Koide's 2/3 would read spread = 3 n0^2, that is 2 (e1^2 - e1 e2 + e2^2) = 3 n0^2.
- **No whole counts meet it** (DERIVED; CHECKED, m2: none with 1 <= n0 <= 60 and |e1|, |e2| <= 60):
  - e1^2 - e1 e2 + e2^2 is the norm of e1 + e2 w in the Eisenstein integers, w a cube root of 1.
  - 2 stays prime there, since x^2 + x + 1 has no root mod 2. So a nonzero norm is 4^j times an odd number, and its power of 2 is even.
  - Then the left side's power of 2 is odd and the right side's, 3 n0^2, is even, unless both sides are 0.
  - The same holds for rational vertex strengths, by clearing the denominators.
- **So on whole counts Koide's 2/3 is approached, never met.** The nearest in m2's range is off by 1/27225, and larger counts come closer, since the norms near (3/2) n0^2 lie ever more densely in proportion. Nature's K = 0.6666645 +- 0.0000051 cannot tell 2/3 from such a near value. Koide's 2/3 stays a test, not a claim.

### 6.3 Mixing

- **Aligned counts give no mixing** (DERIVED, m2): an E count makes every T1 train's spring diagonal in the axes' basis, so every family's mass basis is the same and the mixing is the identity. Nature refuses it (the Cabibbo angle; the neutrinos' large angles).
- **Mixing needs a count off the diagonal** (T2, or T1 on a hand) acting on one family and not the other. Which counts the law lays is G3's (OPEN).
- **The A4 route in the literature:** A4 as a family symmetry (Ma and Rajasekaran, 2001; Altarelli and Feruglio, 2005) is the board's even half. In its tri-bimaximal form it predicted theta13 = 0, which Daya Bay and RENO refuted in 2012. The board's families meet the same test.

### 6.4 A mass that joins two hands

- **Nature's charged fermion masses join two trains,** the left hand and the right hand, through the held value: a spring off the diagonal.
- **On the second-order gear a spring off the diagonal alone runs away** (DERIVED, CHECKED, m3 (d)): with push_X = -D Y and push_Y = -D X, the mode X + Y takes the spring D and beats, while the mode X - Y takes -D and grows. Laid as X = -Y = 10^5 with D = W div 400, X reaches 24,812,700,041,447 at round 400; laid as X = Y it beats within its start (38,325 at round 400).
- **So such a mass needs** diagonal springs at least as large, or the first-order step, each rate in its own slot (N2's form). A first-order step on the board also meets the doublers at the board's corner wave numbers (Nielsen and Ninomiya, 1981): 1 + 3 + 3 + 1 under the 24, a second place where a three stands. OPEN.

## 7. What follows, and what does not

| claim | status | where |
| --- | --- | --- |
| a mass is the k = 0 beat of a gear held by a spring, D = g C n | DERIVED; CHECKED | 2.1, 2.2; m3 (a), (b) |
| the band W (2 - 2 cos omega) = grip sum (2 - 2 cos k_i) + D, omega0^2 = D / W at long waves | DERIVED; CHECKED by counts | 2.2; m3 (b) |
| the board holds every mode only while D <= 2W | DERIVED; CHECKED | 2.2; m3 (b) |
| the lone gear's 6-round beat is no mass | CHECKED | 2.3; m3 (a) |
| the held count drifts under the vertex's push; three-leg vertices alone hold no count | DERIVED; CHECKED | 2.4; m3 (c) |
| in the clicks a mass is a ratio of rest beats, invariant; m_A^2 / m_B^2 = D_A / D_B | DERIVED at long waves | 3 |
| the width is the clock's life | Animate's reading, agreed; OPEN on the act | 3 |
| inertial and gravitational mass are one count | DERIVED from decision 40 (a); OPEN on the act | 3 |
| a T1 train is three species alike, coupled alike through A1 | DERIVED under the condition of 4.2; the condition OPEN (G3) | 4.2 |
| a family has at most three species, the board's axes | DERIVED under the same condition; nature agrees | 4.3 |
| why every fermion family is a triplet; spin one half on a T1 train | OPEN | 4.3 |
| an A1 or A2 held count gives a triplet one mass | DERIVED; CHECKED; nature REFUSES it as the generations' law | 5.1; m1, m2 |
| three masses need an E count with both components, or a T1 count on a hand | DERIVED; CHECKED | 5.2, 5.3; m1, m2 |
| the files' checker refuses a train of kind E on its own | the act as built (5176be5e0) | 5.2 |
| the form a + B cos (phi + 2 pi k / 3) | DERIVED; it predicts nothing alone | 5.4 |
| the ratios' numbers | OPEN (G3's vertex law and held counts) | 5.4, 6.1 |
| the squares' reading needs a cancellation to 2.5 x 10^-7 at the electron | DERIVED from nature's numbers; stands against that reading unless a law explains it | 6.1 |
| Koide's 2/3 on whole counts in the roots' reading | DERIVED: never exactly, as close as wanted | 6.2; m2 |
| mixing | none from aligned counts (DERIVED); the rest OPEN; tri-bimaximal REFUSED by nature | 6.3 |
| a mass that joins two hands on the second-order gear | runs away (DERIVED; CHECKED); needs N2's first-order form (OPEN) | 6.4; m3 (d) |

## 8. For the team

- **Boss, for G3:**
  1. The held count's kind: A1 or A2 gives a triplet one mass (5.1). Three masses need an E count with both components, or a T1 count on a hand (5.2, 5.3). The files' checker refuses an E train on its own (5176be5e0).
  2. Three-leg vertices alone hold no count (Euler, 2.4). Under the vertex's push the count drifts and the gear it holds runs away (m3 (c)). G3's toy has to hold it, by a term of its own or by the law's act for "one quantum per Node-clock".
  3. The family's components must not be read against a direction of the board (4.2), or the clicks would see a turn change a species.
  4. A mass that joins two trains is a spring off the diagonal and runs away on the second-order gear (6.4): N2's first-order form.
- **Sofer:** line 35's "whose kind is to derive" has its derivation here: A1 and A2 give no split and E does. No line of the law changes without the owner's word. The row for 8.2: the mass, on the board a gear's spring to a held count (G3), in the clicks a clock's rest beat in its own ticks, ratios by squares.
- **Animate:** your reading is section 3. The ratio is read side by side at rest, by squares, so it needs no root.

## 9. The probes

Each runs as `python3 -I <probe> <src of tensor24-review at 2a6203a4a>` from derive/david_open/mass/, in whole numbers alone (integers and quotients of two, no float, no root, no cosine), its output beside it as <probe>.txt:

- **m1_kinds.py:** the 24 from kinds.turns and kinds.kinds on the head's star; for nine subgroups the invariant vectors of each kind and the number of distinct values of a generic spring that keeps the subgroup, by the characteristic polynomial's gcd with its derivative; the kinds on A4 by characters.
- **m2_spring.py:** the act's tables C[K, T1 -> T1] for every kind and component; the A1 + E spring, its spread and the lines where two values meet; the Koide search; the circulants by their characteristic polynomials and discriminants; the A2 mixing.
- **m3_beat.py:** the head's tick on the example's files (the lone gear, the uniform wave); the head's gear() under a spring (periods, the top mode, the count of sign changes); the held count under the vertex's push, with and without a spring of its own; a spring off the diagonal; the antisymmetric push.
