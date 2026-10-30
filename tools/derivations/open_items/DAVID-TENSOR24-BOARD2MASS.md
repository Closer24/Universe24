# Board to mass: how a mass enters on the board, how it comes out in the clicks, and what the 24 say of three generations

David, 2026-10-30, 05:5x UTC, on the owner's words to David (in Hebrew; in translation):

- 03:0x UTC: "Prepare a page on this that everyone will agree on... board2mass. It has to explain why nature also shows three generations... On the board a mass is a spring with a coupling: what is the formula has to be understood. First you, then a hostile mathematician agent and a hostile physicist agent go over it after you finish. From the clocks, understand what the transformation from the board to the clicks is. And why those ratios are seen in the clicks, and why there are 3 generations, with all their ratios and properties."
- Before it: "How a mass enters the board, in the four dimensions of the events' spacetime, and how it comes out of the click, whose spacetime is three dimensions, has to be understood, no?" (Sofer's 8.2: both are 3 + 1, and what differs is which 1.)
- 04:3x UTC: "Think in clock terms, not gears. What does the page say? Check whether trains are allowed at all, because everything must be generic and tensor, and a Node-clock is local: only in the definition of the families and the couplings, the coupling family, right?" (Section 2: yes.)
- 05:0x UTC: "Finish only as far as the hostile ones agree with you. Remember that nature is in the clicks, not in the board. Let the writer also confirm that there are no breaches of the laws in the page."

Animate's reading of the mass and the clock (#2187 6514375401 and 6514643547) stands here as the clicks' side (section 4).

Probes, in whole numbers alone (the owner's word through Sofer, 6514488548), each with its output beside it in derive/david_open/mass/, on tensor24-review 2a6203a4a:

- m1_kinds.py: the 24's kinds, and for all eleven classes of subgroups which held kinds keep them and how many masses a spring that keeps them can give a three-hand family; the turns that fix a given held count;
- m2_spring.py: the spring each held kind gives a three-hand family, read from the act's own tables; the T2 split; Koide's 2/3 on whole counts;
- m3_beat.py: the beat on the head's own step and tick; the floor at small swings; the held hand's drift; three runaways.

Only the Boss writes engine code (decision 40). This page is a derivation and its checks, nothing more. Its first draft went to two hostile readers, a mathematician and a physicist (the owner's ask). Both found errors, and section 10 lists what changed. The status words are the protocol's: DERIVED (follows from the law and the act as built, or from the band the step obeys), CHECKED (a probe shows it), OPEN (neither), REFUSED (nature or the law refuses it).

**Nature is in the clicks, not in the board** (the owner's word of 05:0x; line 695, the great clock's tick is no observable; 8.2). Every number from nature on this page is a reading of records: counts of clicks, their rates and their ratios. The board's own numbers, its teeth W, its springs D, its grips and its round, are never measured directly: at first order they cancel from every reading of the clicks, and at order omega0^2 they show only as small departures (4.3, 4.4), for swings above the floor (3.3), which nature's null results bound. The page sets against nature only what the board's clicks would read, and the board's sections (2 and 3) are the mechanism behind them, no claim about nature on their own.

**Words.** In clock terms (the owner's ask): a Node-clock is a clock at one place. A **hand** is the law's gear, a dial with its carried remainder (line 90). A **family** is the law's train, a tensor of one kind defined in the universe file alone (line 96). A family of kind T1 puts three hands in every Node-clock, one for each axis.

## 0. The answer in short

- **Nature is in the clicks, not in the board.** Every comparison with nature below is what the board's clicks would read; the board itself is never measured directly.
- **Families stand only in the files** (section 2). The Node-clock knows none of them. Every hand steps by the one act, and the coupling family is one family among the others.
- **On the board, a mass is a hand held by a spring inside its own Node-clock** (section 3).
  - Light's hand is pulled only sideways, by its six neighbours' hands. A massive hand is also tied, through a three-leg vertex, to a held hand at its own Node-clock: the coupling family's hand standing at its steady count.
  - Because the held hand stands, the vertex pulls the hand back toward 0: a spring, D = g C n (the coupling's strength, the 24's table entry, the held count).
  - The hand then swings by itself even when its neighbours swing with it. That rest beat is the mass: exactly 4 sin^2 (omega0 / 2) = D / W, and omega0^2 = D / W while D is far below W.
  - Two conditions hold it. The swing must be at least about one count a round, or the carry's floor sets a different beat. And the held hand needs a law of its own, or it drifts and the hand runs away.
- **In the clicks, a mass is read through differences of energy and through motion** (section 4): reaction and photon energies read the rest beat, and recoils and orbits read the band's curve. The two agree at first order, and there the round cancels. At order omega0^2 they part, and the round shows as small departures that nature bounds.
  - Masses compare by squares, m_A^2 / m_B^2 = D_A / D_B, at leading order.
  - Inertial and gravitational mass agree at first order, because every hand reads the same teeth W. They part at order omega0^2, and MICROSCOPE bounds that.
- **Three** (section 5): the 24's kinds have 1, 1, 2, 3 and 3 hands, and the largest is three, the number of the board's axes. That three of a T1 family are three species alike in the clicks needs four assumptions and one condition.
  - The condition: no coupling reads the family's hands, the held hands that split them or the grips against a direction of the board.
  - The condition pulls against the plan's one plan, since the kinds that split a triplet are the metric's own (OPEN, G3).
  - So the 24 give a natural three, not a derived one.
- **Three masses** (section 6): a held count of kind A1 or A2, the plan's two candidates, gives a triplet one mass.
  - Three masses need held counts that cut the 24 to a group under which the three hands fall into one-dimensional pieces: E off its three lines, T2 off the body diagonals, or a mix, each with an A1 part large enough.
  - A T2 family loads on the act as built.
- **What does not follow** (section 7): the ratios' numbers, what tells the electron, the quarks and the neutrino families apart, mixing, CP violation, the neutrinos' masses and the left-right mass's step. Koide's 2/3 is a test; on the diagonal spring alone no whole counts meet it, and with a T2 part many do.

## 1. What nature shows, in the clicks

The facts the page has to meet, each a reading of records (PDG 2024 unless named):

- **Three generations, no fourth light one:** the Z's width counts the light active neutrinos.
  - The 2006 LEP combination gave N = 2.9840 +- 0.0082. The beam-beam correction (Voutsinas et al., 2019) moved it to 2.9918 +- 0.0081, and the luminosity correction (Janot and Jadach, 2020) to 2.9963 +- 0.0074.
  - A sequential (chiral) fourth family's heavy quarks would raise the Higgs boson's production by gluons about ninefold, which the LHC refuses.
- **The generations are alike but for mass:** the same charges and the same spin one half in each.
  - Lepton universality holds to a few parts in a thousand, with a tension of about 3 sigma in the B mesons' R(D) and R(D*).
- **The masses are far apart.**
  - Charged leptons: 0.51099895 MeV, 105.6583755 MeV, 1776.93 +- 0.09 MeV.
  - Up quarks: 2.16 MeV, 1.27 GeV, 172.57 GeV. Down quarks: 4.70 MeV, 93.5 MeV, 4.18 GeV. All but the top are in the MS-bar scheme, the top near its pole mass.
  - Neutrinos: KATRIN bounds the mass below 0.45 eV. The squared differences are 7.53 x 10^-5 eV^2 and about 2.5 x 10^-3 eV^2.
- **The generations mix.**
  - The quarks' mixing has |V_us| = 0.2243 and a CP-violating phase, with Jarlskog's invariant about 3.1 x 10^-5. Kobayashi and Maskawa (1973) showed that three generations are the least that can carry such a phase.
  - The neutrinos' mixing has theta12 about 33.7 degrees, theta23 about 42 to 49 degrees, and theta13 about 8.6 degrees (Daya Bay and RENO, 2012).
- **Koide's relation** (Koide, 1982): K = (m_e + m_mu + m_tau) / (sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 0.6666645 +- 0.0000051, against 2/3, within half its error. In Brannen's form (2006), sqrt m_k = mu (1 + sqrt 2 cos (delta + 2 pi k / 3)), with delta = 0.222225 +- 0.000006 against 2/9 = 0.222222.
- **The masses hold still:** atomic clocks bound the drift of the proton-to-electron mass ratio at -8 +- 36 parts in 10^18 a year (Lange et al., 2021), and of the fine-structure constant at 1.8 +- 2.5 parts in 10^19 a year (Filzinger et al., 2023).
- **A short life is a broad mass:** width times life is hbar. The Z's width, 2.4955 +- 0.0023 GeV, is a life of 2.64 x 10^-25 s.
- **Free fall is universal:** MICROSCOPE (2022) bounds the Eotvos parameter at (-1.5 +- 2.3 +- 1.5) x 10^-15.
- **Space is the same in every direction:** cavity comparisons bound a difference in light's speed by direction at 9.2 +- 10.7 parts in 10^19 (Nagel et al., 2015).
- **Charged-lepton flavour holds:** mu -> e gamma is below 1.5 x 10^-13 (MEG II, 2025).
- **The Standard Model:**
  - It holds the charged fermions with three copies put in by hand. Their masses and mixings come from couplings to the Higgs field's held value of 246 GeV, held by a potential whose curvature is the Higgs boson's mass of 125 GeV: thirteen free numbers, and no reason for exactly three.
  - In its minimal form the neutrinos are massless.

## 2. Families stand only in the files

The owner's question of 04:3x, answered yes from the law and the act:

- **Line 90:** a train (a family) is a tensor whose kind is one of the 24's five. What differs between families is the kind and the file's pair, never a branch of the code; no coupling is declared in any file (decision 35), and line 90's older words "the pair, the couplings" read so. As built, the universe file still holds coupling rows with their strengths, a breach G3 removes (7.3). The Node-clock's step is one act, the same for every family.
- **Line 96:** a Node-clock and a Mesh do not know what they run. No act and no reading of a Node-clock names a family; the shape and the pair decide everything.
- **The coupling family** (decision 40 (d), (g) and (h)): an ordinary family of the one hand type, with its leg in every source by the one plan, only three-leg vertices, and a steady count of one quantum per Node-clock from the law.
- **On the act** (tensor24-review 5176be5e0):
  - the files are read against the engine's kinds, and the families become one record of arrays;
  - the step reads every hand alike, from its Node-clock and its six neighbours alone;
  - Sofer's gate refuses a family named or found by its place (its FAMILY and POSITION rules).
- So everything below is about what a family's definition in the file yields under the one act. Nothing in it asks the Node-clock to know a family.

## 3. Mass on the board, in clock terms

### 3.1 Light's hand and a massive hand

- **Light's hand** is pulled only through its Node-clock's six Meshes, by the neighbours' hands. If every neighbour swings with it, nothing pulls it, and it does not beat. On the head (CHECKED, m3 (a)): the uniform wave laid at rest stands at 1 for 60 rounds, and laid moving it drifts 2, 3, 4 and on.
- **A massive hand** is also tied, through the three-leg vertex C[X; K, X], to the held hand K at its own Node-clock, K standing at its steady count n (decision 40 (g)).
  - Because K stands, the vertex's push on X is linear in X and points back toward 0: a spring, D = g C n.
  - Everything is inside one Node-clock, so the spring keeps line 92: the Node-clock reads its own state and its six neighbours alone.

### 3.2 The formula

- **The step** (the head's gear in engine/step.py): W (a+ - 2a + a-) = push + r - r+, the carry keeping the remainder r below one tooth. With the Meshes' pull and the spring, the push is grip sum over the six Spokes (a_s - a) - D a.
  - On the head 6 grip = W exactly: grip 3881691330332771584000000 and W 23290147981996629504000000, the loader's teeth 6 den Gamma^2 G^2 and grip den Gamma^2 G^2 per Mesh (CHECKED, m3 (a)).
- **The band** (DERIVED, the identity of the linear step, the remainder dropped): a wave of wave number k beats omega a round with W (2 - 2 cos omega) = grip sum_i (2 - 2 cos k_i) + D.
- **The rest beat, exactly:** at k = 0, 4 sin^2 (omega0 / 2) = D / W.
- **At long waves, with D far below W:** omega^2 = c0^2 k^2 + omega0^2, with c0^2 = grip / W = 1/6 (light's 1 / sqrt 6 Mesh a round) and omega0^2 = D / W. This is the relativistic form. If a quantum is a fixed action (line 332 at scribe-5 7880f9ec7: "The action of one quantum is T"), so that its energy is hbar times its beat, the mass is m = hbar omega0 / c0^2.
- **Checked by counting, with no cosine** (m3 (b)): at D = W div k^2 the uniform wave's sign changes over 20,000 rounds, times k, read 6368 at k = 8, 16 and 32, about 20,000 / pi. So the beat goes as the root of the spring.
- **Exact periods of the uniform wave alone** (m3 (b)): 6, 4 and 3 rounds at D = W, 2W and 3W. The board holds only D < 2W, and at 2W its top mode is already at the edge (3.4).

### 3.3 The floor: the formula needs a swing of about a count a round

- **Below it, the carry's floor sets the beat** (CHECKED, m3 (h)): under the spring D = W div 400, whose band period is about 126 rounds, the uniform wave laid at 1 beats with period 804, at 2 with 408, at 5 with 180 and at 10 with 120, each the exact first return of the hand's whole state. Only at 30 and at 1000 does it beat with the band's 126.
  - Below the floor the period is exactly 2W / (A D) + 4A at those four amplitudes (the hostile mathematician's formula, m3 (h)): slower than the band's at the smallest swings and a little faster near A omega0 of 1, reaching the band near A omega0 of 1.5.
- **So the beat is the mass only once A omega0 is at least about 1.** At the smallest spring the head holds (D = 1, omega0 about 2 x 10^-13 a round), that is about 5 x 10^12 counts of swing. The held count stands still and is not limited by the floor; what falls under it is a small swing of the massive hand, and whether one quantum's swing lies above it depends on how many counts a quantum's swing holds (line 332; OPEN).

### 3.4 The board's limits

- **The heaviest mass** (DERIVED, CHECKED, m3 (b)): the top mode, every neighbour opposite, is pulled by 12 grip = 2W, so its step reads a+ = (-D / W) a - a-. It holds only while D < 2W.
  - At D = 2W it grows by two starts a round (49 times its start at round 24). At D = 3W it runs away (17,393,796,001 times its start in 24 rounds).
  - So every mass beats below a quarter turn a round.
- **The lightest, and the range:** a spring is a whole number, D >= 1, so D / W >= 1 / W, about 4.3 x 10^-26 at the head's W.
  - A second-order (scalar) hand type then holds masses spanning at most about sqrt W in the kinetic reading (4.8 x 10^12 at the head's W), or (pi / 2) sqrt W in the rest beat's, so it needs W of at least R^2 for a range R.
  - The range R the clicks read in nature, the top quark over the lightest mass not 0, is at least the top over the second neutrino. That neutrino is at least 8.7 meV, which bounds that ratio from above, not R (R grows without bound if the lightest neutrino is tiny but not 0). So a lower bound on R needs a bound on the neutrinos' scale from above:
    - KATRIN's 0.45 eV gives R of at least 3.8 x 10^11 (W of at least 1.5 x 10^23);
    - Planck's sum below 0.12 eV, at least 4.3 x 10^12 (W of at least 1.9 x 10^25);
    - DESI's sum below 0.064 eV (2025), with the normal ordering it favours, at least 1.9 x 10^13 (W of at least 3.6 x 10^26, above the head's 2.3 x 10^25).
    - These are for scalar springs.
  - But they are fermions, and a fermion's mass on a first-order step (7.8) is linear in its counts: its rest beat goes as M / T, so the range one hand type holds is about its teeth T. The head's teeth of about 10^25 would hold 2 x 10^13, and an electron at a Planck round would need T of about 2.4 x 10^22 (OPEN, N2's form).
  - If a round were the Planck time, a scalar of the electron's mass would need D / W of about 1.75 x 10^-45, and W of at least about 5.7 x 10^44. The board's numbers reach the clicks only as ratios at first order, and as departures of order omega0^2 beyond (4.3, 4.4).

### 3.5 What is not a mass

- **The lone hand's 6-round beat** (the example's hand, Animate's item 4): with its six neighbours at 0 the pull is -6 grip a = -W a, so the step reads a+ = a - a-: 1, 0, -1, -1, 0, 1, period 6 (CHECKED, m3 (a)).
- **It is the carry's floor, not a mode of the board** (CHECKED, m3 (f)): it stands only while every neighbour's push stays below one tooth. Laid at 1 or 2 no neighbour moves. Laid at 3, a neighbour carries at round 2 and the period is lost, and laid at 10^6 the hand spreads at once (1000000, 166666, -500001, ...).
- A mass is the beat that stays when the neighbours swing with the hand: the k = 0 end of the band, with the spring.

### 3.6 The held hand needs a law that holds it

- **The vertex pushes all its legs** (the plan's G3 line: "only three-leg vertices, each pushing all its legs"). From the potential (g/2) K X C X, the held hand is pushed by -(g/2) X C X. For an A1 count that is -(g/2) X X, whose mean over a beat is below 0.
- **On the step it drifts** (CHECKED, m3 (c)). K is laid at 10^6 and X at 10^5, with g K just under W div 400 (by 760,000 out of about 5.8 x 10^22).
  - K falls to 800,187 by round 250 and to 142,793 by round 500. It passes below 0 at round 537, the spring turns over, and X runs past 10^60 by round 686.
  - With a spring of its own (W div 16), K stays between 999,559 and 1,000,243 over 2,000 rounds.
- **Three-leg vertices alone hold no count** (DERIVED):
  - A potential of three-leg vertices is a cubic form V, odd in its counts, so it is unbounded below, and it has no strict minimum: its stationary points lie on flat lines, neutrally stable along them.
  - At any stationary phi* that is not 0, Euler's identity gives V(phi*) = 0. Since grad V(t phi*) = t^2 grad V(phi*), the whole line through phi* is stationary, and nothing pulls the count back along it.
  - A one-leg term alone, with only the vertex K X X, does not make (n, 0) stationary.
- **So G3's held hand needs a term that holds it:** a one-leg term with a spring of its own, or a one-leg term with the vertex of three held legs, or the law's "one quantum per Node-clock" as an act.
  - h K + c K^3 has only a local minimum, where K^2 = -h / 3c and c K > 0, behind a barrier of (4/3) |h| K. The vertex's push adds (g/2) <X X> to h, and once that reaches |h| the minimum is gone and the count runs away, as in m3 (c).
  - A spring of its own keeps a minimum for a push of any size, but the push moves it down by (g/2) X X / kappa. As that shift nears n the count reaches 0, and then the hand it holds, a second-order hand as in m3, runs away (CHECKED, m3 (i); both readers' finding at the fourth reading). With the spring W div 16 the shift at the swing's top is 199 for X laid at 10^5, which holds; n / 2 at 5 x 10^6, where K, laid at n, swings to -3,786 and X still stays; 2 n at 10^7 and 8 n at 2 x 10^7, where X runs past 10^60 by rounds 49 and 29.
  - So no term of one, two or three legs bounds the whole potential: with K at its spring's minimum, the potential left for X is (g/2) n X X - g^2 X^4 / (8 kappa), unbounded below. Only a four-leg term bounds it, as the quartic does in nature's held value, which is held by a quadratic and a quartic term. That is G3's toy, bounded at lambda = 1/Gamma (OPEN), beside the plan's G3 line, which lays only three-leg vertices.
- **The held hand's own potential gravitates** (OPEN): a uniform potential is a vacuum energy, with rho + 3p = -2V. Its value at the held count is what gravitates, and that value depends on where the tensor operation sets the potential's zero. The depth of the well that holds it does not: kappa n^2 / 2 for a spring kappa, the change in vacuum energy as the count settles. For a held value like the Higgs field's, that depth is about m_H^2 v^2 / 8, 1.2 x 10^8 GeV^4, against the measured rho_Lambda of about 2.5 x 10^-47 GeV^4. That is the cosmological constant's problem, met here too.

## 4. From the board to the clicks: what the clocks do

### 4.1 The two spacetimes

The board is 3 + the tick, and the clicks are the same 3 + each clock's own count (8.2). The mass enters on the board as a hand's rest beat, made at every Node-clock by its own spring. It comes out in the clicks as a clock whose energy differences and motion show its mass. The tick cancels, as it cancels in the click's shadow.

### 4.2 Motion cancels (DERIVED at long waves, the Boss's D7, 8.1 item 10)

- A packet of the massive hand moving at v beats, at its own place, omega - k v = omega0^2 / omega = omega0 sqrt (1 - v^2 / c^2) a round: slower per round, which is time dilation.
- Two clocks moving together share the factor, so the ratio of their rest beats is the same at every speed, provided every species that interacts has the same limiting speed; lattice interactions generically spoil that at some order (Collins et al., 2004), so it is a condition on the board. That is Animate's reading on the board: the mass is the rest beat counted in the clock's own ticks, invariant, with no formula (decision 37).

### 4.3 What the clicks read

- **A rest beat alone is no click's reading:** a quantum's rest phase is common to all its states (Wolf et al., 2011, on the 2010 redshift claim). The clicks read masses in two ways:
  - **through differences of energy** (reaction energies, photon energies, mass defects), which read the rest beat, omega0;
  - **through motion** (Penning traps, recoils, orbits), which reads the band's curve at k = 0, the kinetic mass, going as sin omega0.
  - They agree at first order and part at order omega0^2 / 6. Rainville et al. (2005) compared exactly these two readings, a Penning trap's mass difference against a capture's photon energy: 1 - Delta m c^2 / E = (-1.4 +- 4.4) x 10^-7. That is a click-level bound on the parting, beside MICROSCOPE's (4.4).
- **Ratios:**
  - exactly, sin^2 (omega0A / 2) / sin^2 (omega0B / 2) = D_A / D_B;
  - m_A^2 / m_B^2 = D_A / D_B holds at leading order. Its corrections are of relative size (D_A - D_B) / W: -(D_A - D_B) / 4W in the kinetic reading and +(D_A - D_B) / 12W in the rest beat's. It also shifts with W, and so with the gravitational potential; atomic clocks bound that shift for the proton-to-electron ratio at (c^2 / mu)(d mu / d Phi) = 7 +- 45 parts in 10^8 (Lange et al., 2021);
  - on a second-order step a spring's values are the masses' squares, so the ratios D_A / D_B are rational when the spring's values are (A1 5 and T2 (0, 0, 2) give 3, 5 and 7), and in general not off the diagonal (the complex circulant of 6.2 gives 9 and 3 +- sqrt 3).
  - The round's unit cancels from every ratio at first order. At order omega0^2 the ratios carry D / W itself, the corrections above, so the round reaches the clicks there, as a condition the board's rest beats must meet.
- **The width is the clock's life** (Animate's reading; agreed): a beat counted over few of its own ticks is spread, over many sharp. On the board a spring with no way out beats sharp. A three-leg vertex to lighter families drains the beat, and its life sets the width. OPEN on the act (G5, G6).
- **The least a clock needs** (Animate, 6514643547, on the owner's word to her: "Pass it to David, it will help him"):
  - to tick, a Node-clock with its six neighbours, never one alone (3.5);
  - to click, two clocks, a giver and a taker with parts;
  - to show a sharp mass, many of its own ticks (its life) and enough Node-clocks to stay together (its span).

### 4.4 Gravity reads the beat, at first order

- **Every hand reads the same teeth W.** So at first order a mass's inertia and its weight are one count: every hand's step reads the metric through W alike (the clocks' read at the now slot), and the tensor operation reads every hand's state alike (decision 40 (a) under the owner's law of 04:1x, line 102: no books in the engine).
- **At order omega0^2 they part** (DERIVED from the band, the hostile physicist's finding):
  - the rest mass goes as omega0;
  - the kinetic mass, the band's curve at k = 0, goes as sin omega0;
  - the passive gravitational mass, the beat's response to W, goes as 2 tan (omega0 / 2), since W d omega0 / dW = -tan (omega0 / 2).
- **So a hand falls in a gradient of W with an acceleration proportional to sec^2 (omega0 / 2)**, and heavier hands fall faster by about omega0^2 / 4.
  - The hostile physicist's float run of the step's linear rule on a chain, outside the repository, agrees: 1.0398 against 1.0411 at omega0 = 0.4, and 1.4635 against 1.4680 at 1.2.
  - So MICROSCOPE's 10^-15 bounds the rest beats a round, and with them the round's length. It reaches them only through the composition of its titanium and platinum masses, which differ in electron share by about 3.3 x 10^-5 and in binding share by about 9 x 10^-4, and for composite masses only through a model of how their parts beat.
- **The active side:** the tensor operation reads a beating hand's rho + 3p = 2W (stride)^2 - D a^2 per Node-clock. That swings at twice the beat between +2D A^2 and -D A^2, and only its mean, D A^2 / 2, is rho.
- **The law's "the clock's read at the factor 1"** is a placeholder until (e)'s exact read at G2. Both sides are OPEN on the act.

## 5. Three hands, three species: what the 24 give

### 5.1 The kinds

The 24's turns, made from the Node-clock's six Spokes, have five kinds of 1, 1, 2, 3 and 3 hands (A1, A2 and E, then T1 and T2). They are irreducible, unlike one another and complete: their characters' sums over the 24 give 24 on the diagonal and 0 off it, and their squared sizes sum to 24 (CHECKED, m1). A family of kind T1 has three hands in every Node-clock, turned among themselves by the 24 as the three axes are.

### 5.2 When a T1 family's three hands are three species alike in the clicks

- **The step is blind to the hand** (CHECKED on the head): every hand of every family steps at the same teeth W, and the loader lays one grip, den Gamma^2 G^2, on every Mesh for every hand. So the three hands step as the same wave at light's speed.
- **The vertices at one Node-clock read hands, not places.** A turn of the 24 applied to the hands alone, the places left where they are, keeps the pull and every vertex whose legs are all read at the Node-clock. So the three hands can be turned among themselves apart from the places.
- **In the clicks they are then three species alike** in speed and in their couplings through A1. Their pair to A1, T1 x T1 -> A1, is the dot product: x with x, y with y, z with z. As built they are spin 0 (5.3).
- **The condition** (OPEN, G3): no coupling may read against a direction of the board any of these:
  - the family's hands;
  - the held hands that split them;
  - the grips (the 24 allow a grip that differs by hand).

  If one does, the three hands are the polarizations of one spin-1 species. Once they are split, a turn of the laboratory changes one into another, which clock comparisons refuse.
- **The condition pulls against the one plan** (OPEN, G3; the hostile physicist's finding):
  - The kinds that split a triplet (E, T2, and T1 on a hand) are the metric's own spatial kinds, and on the act E stands only inside the metric's square.
  - The plan lays the coupling family's "leg in every source by the one plan". A vertex that pairs a held E count with the metric's E slots, or a held T2 count with its T2 slots, would carry the split into the metric's shear, and light's speed would differ by axis, which the cavities bound at parts in 10^18.
  - So a split of the 24's triplet and the one plan's genericity pull against each other. G3 has to say which vertices the one plan lays and why.

### 5.3 Spin and the family

- If spin rode on the T1 hands, a first-order step would contract them with the gradient (gamma^i d_i), which the condition forbids.
- As built, a T1 family's hands are three spin-0 species.
- So spin and family must be separate kinds: a twin kind for the spin, times T1 for the family (the twin kinds wait on OPEN 3).

### 5.4 Three, under four assumptions

The page derives "at most three" only under these:

1. a family alike in all but mass is one kind's hands (a definition);
2. the family's index holds no twin kind (the 24's double cover, 48 turns, holds kinds of 2, 2 and 4 hands beside the five);
3. no doublers are counted (a first-order step has 8 copies on the board's corners, and 16 with a first-order tick, unless a term lifts them);
4. one family per type of charge (two T1 families, or a T1 and a T2 family mixed by an A2 count, give six alike).

- **Under them, a family holds at most three species, the number of the board's axes.**
- **Nature's reason is different:** its generations are alike because gauge invariance couples any number of copies alike. The strong force's asymptotic freedom allows up to sixteen quark flavours.
- **N cannot test a cap:** it counts light active neutrinos, so it agrees with any model that has three.
- **So the 24's three is natural, not derived.** A hand of three parts loads at 5176be5e0 too, but that three is the files' choice.

## 6. Three masses: what splits the triplet

### 6.1 The plan's two candidates give one mass

- **Schur, CHECKED** (m1): a held count that keeps the whole 24 is of kind A1 alone, and any spring it gives a T1 family has one value. A count of kind A2 keeps the even half A4, under which T1 stays one triplet, so it too leaves one value, on a real hand and on a hand of two parts alike.
- **On the act's tables** (CHECKED, m2):
  - C[A1, T1 -> T1] is the identity.
  - C[A2, T1 -> T1] is zero (A2 x T1 is T2), so an A2 count gives T1 no spring at all.
  - It only mixes a T1 family with a T2 family (C[A2, T2 -> T1] is the identity), with two values, each three alike.
- **So the plan's A1 or A2** (decision 40 (h)) gives three generations of one mass. Nature refuses it.

### 6.2 What gives three

- **The rule** (DERIVED; CHECKED, m1 over all eleven classes of subgroups): the held counts must cut the 24 to a group under which T1 has only one-dimensional pieces, real ones on a real hand.
  - **Where the three pieces all differ,** the group fixes the mass basis: D2 (the three half turns about the axes) and the Klein group of the half turns about z, (1, 1, 0) and (1, -1, 0), on a real hand; also Z3 and C4 on a hand of two parts.
  - **Where some pieces repeat,** the masses still differ for generic counts, but the counts set the basis: a single half turn about an axis or a face diagonal, or nothing kept. Only these leave room for a mixing angle set by the counts; two families cut to different fixed-basis groups mix at a fixed angle (E on one, D2, and T2 (0, 0, 1) on the other, the Klein group, mix at 45 degrees; 7.4).
- **It is met by:**
  - **E off its three lines** (m2): an A1 + E count (n0; e1, e2) gives n0 + e1, n0 - e1 + e2 and n0 - e2. They sum to 3 n0, with spread 2 (e1^2 - e1 e2 + e2^2), a polynomial identity. Two meet only on the lines e1 = -e2, e2 = 2 e1 and e1 = 2 e2. E (1, 0) gives three values, and it is fixed by D2 alone; E (1, 2), on a line, is fixed by D4 and gives two (m1).
  - **T2 off the body diagonals** (m2): the spring [[0, t3, t2], [t3, 0, t1], [t2, t1, 0]] has the polynomial lambda^3 - |t|^2 lambda - 2 t1 t2 t3 and the discriminant 4 ((t1^2 + t2^2 + t3^2)^3 - 27 t1^2 t2^2 t3^2), which is 0 only where t1^2 = t2^2 = t3^2. T2 (0, 0, 1) gives three values and is fixed by the Klein group above (m1).
  - **Any mix:** with one strength, A1 + E + T2 hold every whole symmetric spring whose trace is a multiple of 3 (1 + 2 + 3 numbers; the trace is 3 n0). With whole strengths of their own, the trace stays a multiple of 3 g_A1, so they hold every rational symmetric spring only up to a common factor.
  - **On a hand, A1 + T1,** if the plan joins the two parts as the hermitian i M (OPEN). T1 alone gives 0 and plus and minus |v|, and with A1 and T2 along a body diagonal it is the complex circulant a + b P + b* P^T (m2: lambda^3 - 15 lambda^2 + 60 lambda - 54). A T2 count alone along that diagonal leaves a pair alike (m2: lambda^3 - 3 lambda - 2).
- **On the act:** the probes read the act at 2a6203a4a, where a family of kind E is refused outright. At 5176be5e0 a T2 family loads, and E loads only inside a family whose kinds' characters are the four-vector's square (runner/files.py), which the act reads as a metric family, its 00 slot the clock.

### 6.3 An A1 part large enough

- **Every traceless count needs an A1 part above minus its least value,** or a hand runs away. E (1, 0) and T2 (0, 0, 1) each need n0 > 1, and T1 on a hand needs n0 > |v|.
- **On a real hand, a T1 count's push is antisymmetric, with values plus and minus i |v|, and the hand runs away** (CHECKED, m3 (e): -1,602,744, then 41,579,439, then -1,481,206,931 at rounds 100, 200 and 400).
- **On a hand of two parts, read as i M on the mode (1, -i, 0):** x reaches 24,812,700,041,447 at round 400 with no A1 part, and with an A1 part of 2 |v| it beats (38,332 at round 400) (CHECKED, m3 (g)).

### 6.4 E's own form

The act's E basis (e1 - e2, e2 - e3) is not orthogonal: its Gram matrix is G = [[2, -1], [-1, 2]]. The table that pushes E from X X is 3 G^-1 times the one that pushes X from E (exactly, on the act's tables), so the vertex comes from one potential only if an E count's own spring and stress use G.

### 6.5 The form predicts nothing alone

Any three springs that sum to 3a can be written a + B cos (phi + 2 pi k / 3), k = 0, 1, 2: Brannen's form, for whichever reading the springs give. But three masses are three numbers and the form has three parameters, so it says nothing alone. A prediction needs the law to fix the held counts and the vertex strengths: G3's vertex law, OPEN.

## 7. The ratios and the properties: what follows and what does not

### 7.1 Nature's numbers in three readings

The charged leptons in the form a + B cos (phi + 2 pi k / 3):

| reading | B / a | lightest / a | where the step gives it |
| --- | --- | --- | --- |
| the squares, m^2 | 1.98944 | 2.47 x 10^-7 | a scalar's second-order spring, D linear in the counts; a charged lepton's M^dagger M is quadratic in them, so no step gives its m^2 linear |
| the masses, m | 1.83341 | 8.14 x 10^-4 | a first-order step's singular values (7.8) |
| the roots, sqrt m | 1.41421 (sqrt 2 = 1.414214) | 0.0404 | none named |

In every reading the electron is a remainder of the other two. The page draws no verdict from that: on whole counts a near-0 value is no rarer than any other, so this is a remark on naturalness, not a derivation.

### 7.2 Koide's 2/3 on whole counts

- **On the diagonal A1 + E spring, none** (DERIVED; CHECKED, m2: none with 1 <= n0 <= 60 and |e1|, |e2| <= 60):
  - read as the roots of the masses, Koide's ratio is 1/3 + spread / (9 n0^2), so 2/3 reads 2 (e1^2 - e1 e2 + e2^2) = 3 n0^2;
  - e1^2 - e1 e2 + e2^2 is the norm of e1 + e2 w in the Eisenstein integers, w a cube root of 1;
  - 2 stays prime there (x^2 + x + 1 has no root mod 2), so a nonzero norm is 4^j times an odd number, and its power of 2 is even;
  - so the left side's power of 2 is odd and the right side's is even, unless both are 0. The same holds for rational strengths, by clearing the denominators.
- **The nearest approaches come from below,** by the least step 1 / (9 n0^2): for example n0 = 389 and E (-361, 179), with values 28, 929 and 210 (m2). A step from above by 1 / (9 n0^2) is impossible: for an odd n0 it would need a norm that is 2 mod 4, and for an even n0 an odd 2N.
- **With a T2 part, many meet it exactly** (CHECKED, m2):
  - the ratio is tr S^2 / (tr S)^2, and 2/3 reads 2 (e1^2 - e1 e2 + e2^2 + |t|^2) = 3 n0^2;
  - at n0 = 4 alone, 336 whole counts give three distinct values above 0 with Koide's ratio 2/3 exactly, one of them E (-3, -5) and T2 (-2, 0, 1), the spring [[1, 1, 0], [1, 2, -2], [0, -2, 9]].
- **So Koide's 2/3 is a test, not a claim:** nature's K = 0.6666645 +- 0.0000051 can tell neither case.

### 7.3 What tells the families apart

Under the law no file declares a coupling (decision 35, line 35) and no act names a family, and the plan gives the coupling family one strength from its vertex law (decision 40; G3, not built). Then every family of one kind and part meets the same held counts through the same vertex law, and has the same spring. As built, the act's coupling rows still carry a strength each (runner/files.py's row fields, load.plan), a breach the plan removes at G3; until then families of one kind can differ through their rows' strengths.

- The electron's, the up quarks', the down quarks' and the neutrinos' families would then share one set of ratios and one mass basis, so there would be no mixing.
- Nature refuses that: m_mu / m_e = 207, m_c / m_u about 590, m_s / m_d about 20.
- What differs between families under the law is their kind, their part and the file's pair (line 90 as decision 35 reads it). Whether those set four different spectra is OPEN.

### 7.4 Mixing

- **Commuting springs give no mixing** (DERIVED, m2): an E count makes every T1 family's spring diagonal in the axes' basis. The mixing is then a permutation, ordering two families' masses along different axes, never a mixing angle.
- **Mixing needs two families' springs that do not commute,** which needs counts off the diagonal (T2, or T1 on a hand) acting on them differently (OPEN, 7.3).
- **The A4 route in the literature:** A4 as a family symmetry (Ma and Rajasekaran, 2001; Altarelli and Feruglio, 2005) is the board's even half. In its tri-bimaximal form it predicted theta13 = 0, which Daya Bay and RENO refuted in 2012.

### 7.5 CP violation

Three generations are the least that carry a CP phase in the quarks' mixing (Kobayashi and Maskawa, 1973). That is the one established role of "three" in nature, with Jarlskog's invariant about 3.1 x 10^-5. A real hand gives a real spring, with no phase; only counts on a hand of two parts can carry one. OPEN.

### 7.6 The neutrinos' masses

Their origin, and their ratio to the electron's below 10^-6, are not treated here. OPEN.

### 7.7 The held counts' own ripples

- **Flavour changes** (OPEN): the ripples of an E or T2 held count couple to the three hands unequally. Once there is mixing they change flavour at tree level, which K-meson mixing and mu -> e gamma bound hard.
- **An E count alone is safe but empty:** it leaves the parities of the three half turns, which forbid charged flavour change and forbid mixing too.
- **Domain walls** (OPEN): if the 24 break by the state, unlike regions break them differently and walls stand between them (Zel'dovich, Kobzarev and Okun, 1974).

### 7.8 A mass that joins two hands

- **Nature's charged fermion masses join the left hand and the right hand** in the first-order equation. Squared to second order, such a mass is M^dagger M on the diagonal, never below 0, so it never runs away (the hostile readers' finding; the first draft was wrong here). The masses are then M's singular values, so the counts' signs do no harm.
- **Only a spring off the diagonal alone runs away** (DERIVED, CHECKED, m3 (d)): with push_X = -D Y and push_Y = -D X, the mode X - Y takes -D. Laid as X = -Y = 10^5 with D = W div 400, X reaches 24,812,700,041,447 at round 400; laid as X = Y it beats within its start (38,325 at round 400).
- **A first-order step is needed for spinor structure and chirality, not for stability** (N2's form; OPEN). Fermi statistics is quantum and is not settled by an integer step (OPEN).
- **Such a step meets the doublers** at the board's corner wave numbers (Nielsen and Ninomiya, 1981):
  - the corners fall 1 + 3 + 3 + 1 under the 24, with chiralities alternating and summing to 0;
  - the two triplets have opposite chirality, so they cannot be chiral generations, and as orbits of wave numbers each is A1 + E, not T1;
  - a first-order tick doubles the count to 16.

## 8. What follows, and what does not

| claim | status | where |
| --- | --- | --- |
| families stand only in the files; the Node-clock knows none | the law (lines 90, 96) and the act (5176be5e0) | 2 |
| a mass is a held hand's rest beat, D = g C n, 4 sin^2 (omega0 / 2) = D / W | DERIVED (linear step); CHECKED by counts | 3.1, 3.2; m3 (b) |
| the beat is the mass only for swings of about a count a round or more | CHECKED | 3.3; m3 (h) |
| the board holds every mode only while D < 2W | DERIVED; CHECKED | 3.4; m3 (b) |
| a scalar hand type's range of masses is at most about sqrt W (kinetic), a first-order one's about its teeth; nature's range needs a premise on the neutrinos' scale | DERIVED | 3.4 |
| the lone hand's 6-round beat is the carry's floor | CHECKED | 3.5; m3 (a), (f) |
| the held hand drifts under the vertex; three-leg vertices alone hold no count; a spring of its own holds it only while the push's shift stays below about n; only a four-leg term bounds the potential | DERIVED; CHECKED | 3.6; m3 (c), (i) |
| the held hand's potential at its count gravitates as a vacuum energy; its well's depth kappa n^2 / 2 is the change as the count settles | DERIVED (the zero OPEN); OPEN on the act | 3.6 |
| motion cancels from the ratio of two rest beats | DERIVED at long waves | 4.2 |
| the clicks read the rest beat through energy differences and the kinetic mass, going as sin omega0, through motion; they part at order omega0^2 | DERIVED | 4.3 |
| m_A^2 / m_B^2 = D_A / D_B at leading order, corrections of relative size (D_A - D_B) / W; whole when the spring's values are rational | DERIVED | 4.3 |
| the width is the clock's life | Animate's reading, agreed; OPEN on the act | 4.3 |
| inertia and weight agree at first order and part at order omega0^2 (fall as sec^2 (omega0 / 2)) | DERIVED from the band; OPEN on the act | 4.4 |
| a T1 family is three species alike, coupled alike through A1 | DERIVED under 5.2's condition; the condition OPEN and in tension with the one plan | 5.2 |
| spin rides on another kind than the family | DERIVED from 5.2; OPEN 3 | 5.3 |
| at most three alike | DERIVED under 5.4's four assumptions; nature's alikeness has another reason | 5.4 |
| A1 or A2 held counts give a triplet one mass | DERIVED; CHECKED; nature REFUSES it as the generations' law | 6.1; m1, m2 |
| three masses need counts under which T1 has only one-dimensional pieces: D2 or the Klein group (basis fixed), a half turn or nothing (basis set by the counts); Z3 and C4 on a hand | DERIVED; CHECKED | 6.2; m1, m2 |
| T2 families load on the act; E only inside the metric's square | the act at 5176be5e0 (E refused outright at 2a6203a4a, the probes' baseline) | 6.2 |
| traceless counts need an A1 part large enough | DERIVED; CHECKED | 6.3; m3 (e), (g) |
| the form a + B cos (phi + 2 pi k / 3) predicts nothing alone | DERIVED | 6.5 |
| the ratios' numbers | OPEN (G3's vertex law and held counts) | 6.5, 7.1 |
| Koide's 2/3 on whole counts: never on the diagonal spring; often with T2 | DERIVED; CHECKED | 7.2; m2 |
| families of one kind and part come out alike under the law and G3's single strength; as built, rows' strengths can differ | DERIVED (the law); the act as built | 7.3 |
| what tells the families apart | OPEN | 7.3 |
| mixing | none from commuting springs (DERIVED); the rest OPEN; tri-bimaximal REFUSED by nature | 7.4 |
| CP violation, the neutrinos' masses, flavour changes, domain walls | OPEN | 7.5 to 7.7 |
| a left-right mass is M^dagger M on the diagonal; a spring off the diagonal alone runs away | DERIVED; CHECKED | 7.8; m3 (d) |

## 9. For the team

- **Boss, for G3:**
  1. **The held count's kind:** A1 or A2 gives a triplet one mass (6.1). Three masses need counts that cut the 24 further, E off its lines or T2 off the body diagonals, each with an A1 part large enough (6.2, 6.3). A T2 family loads as built.
  2. **The held hand needs a term that holds it:** three-leg vertices alone hold no count, and under the vertex's push it drifts below 0 and the second-order hand it holds runs away (3.6, m3 (c)). A spring of its own holds it only while the push's shift (g/2) X X / kappa stays below about n (m3 (i)). Only a four-leg term bounds the whole potential, and the plan's G3 line lays only three-leg vertices. G3's toy must hold it: say which term the one plan lays.
  3. **The one plan against the split:** the kinds that split a triplet are the metric's own. If the one plan pairs a held E or T2 count with the metric's slots of the same kind, a held split shears space, and the cavities refuse that at parts in 10^18 (5.2). Say which vertices the one plan lays.
  4. **The integers:** a mass's beat is its band's only for swings of about a count a round or more (3.3). A scalar hand type spans masses of at most about sqrt W, so a range R asks W of at least R^2; if nature's range were held by scalar springs, DESI's neutrino sum would ask about 3.6 x 10^26, above the head's. Nature's wide range is the fermions', and a first-order (fermion) hand type spans about its teeth (3.4; OPEN).
  5. **Families of one kind and part come out alike** under the law and G3's single strength (7.3); as built they can differ only through their rows' strengths, the breach G3 removes. What tells them apart is OPEN.
  6. **The equivalence:** inertia and weight part at order omega0^2 on the step (4.4).
- **Sofer:** line 35's "whose kind is to derive" has its answer here: A1 and A2 give no split, and E or T2 counts do. No line of the law changes without the owner's word. The row for 8.2: the mass, on the board a hand's rest beat held by a spring to a held hand (G3); in the clicks, read through energy differences (the rest beat) and through motion (the kinetic mass), by squares at leading order.
- **Animate:** your rest beat in the clock's own ticks is the board's side (4.2). The clicks read it through energy differences, and the kinetic mass through motion; the two equal each other at first order and part at order omega0^2 (4.3). Your width and your least stand (4.3).

## 10. The two hostile readers: what changed

The first readings (04:4x and 04:5x UTC) read the first draft: the physicist toys-5 825ef7496, the mathematician the working copy that became a90f256c4. The second readings (05:1x and 05:2x UTC) read e9143fd41 with the clicks' framing at its top. The third (05:3x UTC) read 0b3b180af and agreed with minor fixes. The fourth (05:4x UTC) read 8b3454cf4 and agreed but for one sentence of 3.6, the same sentence for both. Each reader reran the three probes every time, and each output matched its saved text.

| finding | by | changed |
| --- | --- | --- |
| three masses need only E: false, since T2 off the body diagonals splits the triplet; m1 missed two classes of subgroups | both | 6.2; m1 holds all eleven classes, m2 the T2 discriminant |
| "E with both components": false (E (1, 0) splits) | both | 6.2 |
| Koide never met exactly on whole counts: only for the diagonal spring | both | 7.2; m2 finds the T2 solutions |
| m_A^2 / m_B^2 = D_A / D_B exactly and whole: first order only, whole only when diagonal | both | 3.2, 4.3 |
| a left-right mass runs away: wrong, M^dagger M is diagonal | both | 7.8 |
| inertial and gravitational mass one count: they part at order omega0^2 | both | 4.4 |
| the lone hand's beat a mode of the board: the carry's floor | both | 3.5; m3 (f) |
| the beat is the mass at every swing: only above the floor | physicist | 3.3; m3 (h) |
| traceless counts need an A1 part; T1 on a hand is one free and one runaway mode alone | both | 6.3; m3 (g) |
| "never four" an overclaim (twin kinds, doublers, gauge alikeness, two families) | both | 5.4 |
| the condition too narrow; the split's kinds are the metric's | physicist | 5.2 |
| spin on the T1 hands contradicts the condition | physicist | 5.3 |
| the range of masses one hand type holds; the floor of the spring | both | 3.4 |
| families of one kind come out alike | physicist | 7.3 |
| the clicks read masses through motion, not by a rest phase | physicist | 4.3 |
| the squares' cancellation is a remark, not a derivation | physicist | 7.1 |
| CP violation, the neutrinos' masses, flavour changes, domain walls left out | physicist | 7.5 to 7.7 |
| the doublers' chiralities | physicist | 7.8 |
| D <= 2W should be D < 2W; mixing a permutation; E's form uses G; numbers (the Z's width, N's chain, the alpha drift, Brannen's error, KATRIN, the neutrinos' splitting) | both | 3.4, 7.4, 6.4, 1 |
| round 1, minor: the band is the linear step's identity, not the integer step's; the Euler line runs both ways; the approach to 2/3 from below; the characters and stabilisers cited from m1; the T1 runaway read from its eigenvalues; the Planck figures; the baselines; g K, the polynomial identity, co-moving clocks | mathematician | 3.2, 3.6, 7.2, 5.1, 6.3, 3.4, 6.2 |
| round 1: unsplit hands tied to space are one spin-1 species' polarizations; motion cancels only with one limiting speed for every species (Collins et al., 2004); MICROSCOPE tests the passive side | physicist | 5.2, 4.2, 4.4 |
| round 2: the round reaches the clicks at order omega0^2 | physicist | top, 0, 3.4, 4.3 |
| round 2: the rule needs only one-dimensional pieces, repeats allowed (both readers' round-1 wording had "different") | both | 0, 6.2, 8 |
| round 2: the sqrt (2W) range is a scalar's; a fermion's is its first-order teeth | physicist | 3.4, 9 |
| round 2: the range's bound pointed the wrong way; it needs a premise on the neutrinos' scale; W of at least R^2 in the kinetic reading | mathematician | 3.4, 9 |
| round 2: the clicks read the rest beat through energy differences (Rainville et al., 2005) beside motion | physicist | 0, 4.3 |
| round 2: the act's coupling rows carry their own strengths as built | mathematician | 7.3, 9 |
| round 2, minor: the floor's period 2W / (A D) + 4A; no strict minimum; a one-leg term with the vertex of three held legs; whole when the values are whole; the trace a multiple of 3; 3 G^-1; statistics OPEN; the vacuum energy's zero; section 1's wordings; the table's scalar label; the uniform wave's periods; the baselines; a second-order spring's values are squares; Lange et al.'s bound on the potential; MICROSCOPE's reach through composition | both | 3.3, 3.6, 4.3, 6.2, 6.4, 7.8, 1, 7.1, 3.2, 4.4 |
| round 3, minor: for swings above the floor; the floor's periods as exact first returns; the range's direction and the premise's ordering; the cubic spring's barrier; what gravitates; MICROSCOPE through composition; the ratios rational where the spring's values are; the rest beat through energy differences and the kinetic mass through motion; an angle set by the counts; up to a common factor | both | 0, 2, 3.3, 3.4, 3.6, 4.1, 4.3, 6.2, 9; m3 (h) |
| round 4: a spring of its own keeps a minimum but holds the count only while the push's shift stays below about n; only a four-leg term bounds the whole potential | both | 3.6, 8, 9; m3 (i) |

## 11. The probes

Each runs as `python3 -I <probe> <src of tensor24-review at 2a6203a4a>` from derive/david_open/mass/, in whole numbers alone (integers and quotients of two, no float, no root, no cosine), with its output beside it as <probe>.txt:

- **m1_kinds.py:** the 24 from kinds.turns and kinds.kinds on the head's star; the kinds' characters (irreducible, unlike, complete); for all eleven classes of subgroups, the invariant counts of each kind and the number of distinct values of a generic spring that keeps the subgroup, read from the characteristic polynomial's gcd with its derivative; the kinds on A4; the turns that fix eight held counts.
- **m2_spring.py:** the act's tables C[K, T1 -> T1] for every kind and component; the A1 + E spring, its spread and the lines where two values meet; the diagonal Koide search and the nearest approach; the T2 discriminant; the A1 + E + T2 Koide solutions; the circulants by their polynomials and discriminants; the A2 mixing.
- **m3_beat.py:** the head's tick on the example's files (the lone hand at 1, 2, 3 and 10^6; the uniform wave); the head's gear under a spring (periods, the top mode, the count of sign changes, the floor at small swings); the held hand under the vertex's push, with and without a spring of its own, and with it under larger swings; a spring off the diagonal; the antisymmetric push on a real hand and on a hand of two parts.
