# The law of the GameBoard

The one document of the law: what the engine computes, in whole numbers,
and why. Every symbol is named in English where it first appears. A
scalar is written plain, a vector in bold lowercase (**n**), a matrix or
an operator in bold uppercase (**C**). A line that no longer holds is
not in this document.

## The GameBoard and the families

### The objects

A **Node** is a physical location. The **GameBoard** is all the Nodes
together, a box of `shape` = (N_x, N_y, N_z) Nodes; each axis is periodic
(the box a torus on that axis) or open (a face beyond which no Node
lies), as the world declares. Two Nodes that differ by one step along
one axis are joined by a **Link**; each Node has six Links, one through
each of its six **Ports**, named by their outward direction +x, -x, +y,
-y, +z, -z. An axis of one layer folds: its two Ports return the Node
itself. The local information of a Node is its **NodeState**: the
levels and remainders of the families at that Node, and nothing else.
A change of a NodeState is an **Event**; the rule that makes it is a
**LocalRule**, and there is one LocalRule, Rule3 ([Rule3](#rule3)).

A **family** is one kind of physical value with its own declarations
([a family's declaration](#a-familys-declaration)). A family's **record** is a set of levels over the
GameBoard, two levels per Node (now and before) with a remainder per Node;
the family's level at a Node is one number.
A **body** is a set of Nodes on which a family's **count** stands, with
the values the body's writer declares (its content, its momentum, its
spin, its moment); a body is one connected region.

### A family's declaration

Every physical number comes from the world's files: the universe file
(the families and the universe's integers) and the world file (the
bodies, the detectors, the readings). The engine holds no number of its
own; a scale that is no physics (the amplitude unit A of [the generator](#the-generator) (f), a
product bound) is derived from the integer width, never written.

The universe's integers: the Node clock Gamma (the pace of an empty
Node, every family's clock unit); the quantum's action T (`quantum_action`),
the action of one quantum of any family, a unit as Gamma is; the momentum unit Q_unit.

**The families from the rule** (the owner's question, 2026-09-28, 09:13 Israel: how are the families derived from Rule3): a family is a band of the one rule and not a declaration, and its row holds nothing the rule and the geometry fix. Its pair [num, den], cos omega_0 = num / den: the vacuum's band [1, 1] (the rule's own massless line) and the exact band [1, 2] (2 cos omega_0 = 1, the period 6, one of the three exact rotations the rule allows, which never click) are the rule's; the matter pair (the word "body", every body its own) is the one free physical pair.

The families as the rule derives them from the two keys of a row, its pair and what it holds, with the reads on the held row's pair (**The families from the rule** above; the rows of the rule's own universe, `examples/events/rule.json`, and the third a band the rule allows and the universe does not use, **The third and the colours, closed as absent**):

| Family, its rank | Pair | Holds, at the divisor | Parts | Clicks | Reads | Its free number |
| --- | --- | --- | --- | --- | --- | --- |
| gravity, the time part and the three tensions | [1, 1] | the content, E_s = 1 | 1, 3 | never: a field and no click | none | none |
| charge (its quanta light), a scalar holding the sign | [1, 1] | the sign, E_s = 1 | 1 | its count moves by its own count's line from 0, quanta and holes together; light is born by the write into its record | gravity, the bound charge | none |
| the bound charge (polarisation), the exact band | [1, 2] | the content, E_s = 1 | 1 | never | none | none, both keys fixed |
| matter, the scalar | [m, Gamma] | nothing | 1 | its count moves by the count's line and stays its family; a quantum that leaves a body is a message of matter | gravity, the bound charge; charge by its own q | m, the mass |
| the third (a band the rule allows, unused), the mirror band | [-1, 2] | nothing | 1 | as matter | as matter | none |

**The mass is one integer** (the owner, 2026-09-28, 10:46 Israel): every pair is written over the GameBoard's one denominator Gamma, cos omega_0 = m / Gamma, the file holding the numerator m alone: light m = Gamma, the exact band m = Gamma div 2 (Gamma even), matter its one integer, 4,000 over 6,000 in the rule's own universe (2 / 3 exactly);

**The wall is one** (Cheshbon's correction, 2026-09-28, 14:12 Israel, on the de Broglie Experimenter's finding that a pair reduced to lowest terms shrinks the wall 4,000-fold, lifts A to 1.3 x 10^9 and drives the count's line past the width): the wall is w = 6 Gamma^3 for every family, the pair enters the coefficients as the file writes it, m over Gamma (R_a = 2 m p_a^2, the rest term 12 (Gamma - m) p_0^2), and a reduction to lowest terms is a reading and never the loader's act, so every family's remainder has the one resolution and the exact bands leave none in any form (S + 6 R = 6 Gamma^3 exactly); so the width's amplitude unit falls (A = 512,409 in the universe of record against 4,270,079 at [800, 1200], the pair (level, remainder) carrying the same bits) and T is set so that every record at c T stays under A (T at most 9 x 10^11 for the givers of record; 5 x 10^11 proposed).

**The final unification** (the owner, 2026-09-28, 10:53 Israel; the divisors, the reads, the sign and the parts as the owner's words of 2026-09-30 have them): the three of Rule3 is the three axes; the three axes give the three tensions a held row carries beside its time part, the axis contents Rule3 reads into the Link's paces, and no other part: the parts Rule3 never reads (a vector part, the off-diagonal parts of a tensor) are not in the law (the owner, 2026-09-30, "the parts Rule3 never reads leave"); every family carries two keys, its pair and its divisor: the field on the pace's own band [1, 1] holding the content carries the time part and the three tensions (gravity, 1 + 3), the holder of the sign on [1, 1] its time part alone (the charge, a scalar whose quanta are light), a quantized scalar holds nothing and has no divisor (matter, its pair the mass m), and the exact band [1, 2] holding the content is the bound charge; in the rule's own universe every divisor is 1 (**The rule's own universe**), so the parts carry no free number and the mass is the one. The crack, named: a second massive scalar family, a second mass, the rule does not forbid, and nature's spectrum of masses is the open row under this line. A family carries quanta (a count and its current, [the count's line](#the-counts-line)) unless it holds the content, and never clicks where it does: the massless row and the exact band that hold the content, whose rest rotation at the vacuum's pace leaves no remainder (no remainder, no click), so two real fields; a family that carries quanta and holds the sign is one record, its time part its real level pair (**Light is born by the write**); an exact band that carries quanta (the third on [-1, 2]) clicks as every family's does, exactly only in the vacuum (**The exact bands** below). Its reads ([the paces](#the-paces)): every family of quanta reads every holder of the content at the weight 1, a row without a gap as its stepped field and a row with a gap as the well it laid (**The vacuum's row steps at the divisor 1**), and every other holder of the sign by its own q (the sign of its own sense, **The sign is the rotation sense**); a family sources what it reads at the weight it reads with. The action of one quantum is T, the universe's one integer for every family: Rule3 is linear and its form's scale is free, so no line of Rule3 fixes T; it is a unit, declared once, and no family, no body and no emitter declares its own (the owner, 2026-09-28). So the files hold Gamma, T and the matter pair, every divisor 1, and nothing else of physics.

**The exact bands** (the owner's word, 2026-09-28, 11:44 Israel: the quarks are there for a reason and are almost never seen; the algebra on one Node, 12:03 Israel): the line of one Node at rest, a_next = 2 cos omega_0 a_now - a_before, is exact in integers only where 2 cos omega_0 is an integer, so the rule carries exactly three exact rotations, 2 cos omega_0 = 1, 0 and -1, the periods 6, 4 and 3, the pairs [1, 2], [0, 1] and [-1, 2]; a record on an exact band at rest at the vacuum's pace leaves no remainder in its rest rotation, so its quanta stand exactly at every Node, it gives nothing and never decays alone, and stable matter is built on an exact band; everything else of it clicks as every family's does, its packets (a wave number is no integer rotation), its Nodes in a well (2 cos omega = 2 - (p_0 / Gamma)^2 there) and its reads, so an exact band is seen exactly when it is moved or probed and only then (the owner's word, 2026-09-28, 12:25 Israel: it does click).

**The exact bands are exact only in the vacuum** (Cheshbon's correction, 2026-09-28, 13:09 Israel): at a Node of pace p_0 the band's rest rotation is 2 cos omega = 2 - 2 (den - num) (p_0 / Gamma)^2, an integer at p_0 = Gamma alone, so a record on an exact band inside a well, its own or another's, leaves a remainder and clicks like every family's: the third's three phases sum not to 0 but to a share of a record's level that grows with the well, 1 + 2 cos omega' of a record's level with 2 cos omega' = 2 - 3 (p_0 / Gamma)^2 at [-1, 2] and k = 0: 0.015 at a level 30 of 12,000, 0.146 at 300, 1.05 at the self-binding edge and 1.5 at the horizon, and white matter stands only where the well at its Nodes is small against Gamma: under the divisor 1 no white pixel exists and the third and the polarisation are messages of the vacuum; a white body would need a divisor far above 1, which the universe does not have (a finding). The first is the bound charge, the polarisation, never seen free.

**The third and the colours, closed as absent** (the advisor on the owner's word of 2026-09-30, #1519 comment 5903952622; the standing line **The colours are the three axes** of 2026-09-28 kept): the third [-1, 2] is a band the rule allows and the universe does not use, the mirror of [1, 2] (**A pair's numerator may be negative** below), and one family on it holds no standing body: its read is negative, so its own well pushes its rest rotation up into the vacuum's band (2 cos omega = 0.31 at a count 3,000 of 12,000, inside [-1, 1]) and the record leaks, a record of the third at one Node being a packet of every wave number that disperses in every universe, its uniform mode alone exact (**A third does not bind itself**). The three colours are the count's line's three tallies sigma_x, sigma_y, sigma_z, a detector's reading of the click's axis, no charge of the body and no force of their own; whiteness is their balance at rest (an isotropic tail carries no net current through any Port). The law has no strong force but the tail's reach: under a pull the clicks are biased along one axis at the rate omega_b e^(-kappa d) per interval, which falls with the distance and gives no linear potential, so the force between two pixels is short-ranged, its range 1 / kappa (2.2 Links at 3,000 of 12,000; the click's reach 18 Links at T = 1), the nuclear force between nucleons, and a nucleus is horizon pixels within tail reach; a pixel has no inside, and the smallest bound fraction of a horizon pixel is 0.2255 / (1 / 2) = 0.451, so a third of a pixel never binds and disperses (confinement is the edge, no line of its own). So the quarks are not in the law: the white body, the tube, the string, the charges 2 / 3 and 1 / 3, the generations and up and down leave with the third, no line and no look, and the band [0, 1] of the period 4 is the same, a band the rule allows and the universe does not use. In the rule's own universe the matter is the pixels of [2, 3] and the light, and the third and the polarisation are messages, exact in the vacuum and clicking in every well (**The exact bands are exact only in the vacuum**).

**The conversion** (a hypothesis under its own name: the weak force): a click that takes a quantum of one family and gives it as quanta of others, the rotations adding, is the whole weak interaction, one Node's act, no field and no massive vector, and no family's row declares anything for it. The charges 2 / 3 and 1 / 3, the generations and the band [0, 1] are no rows under it: they left with the third (**The third and the colours, closed as absent**).
**The rule's own universe** (the owner's word of 2026-09-29: the universe, no longer a hypothesis; the name kept as the decision's, from the owner's word of 2026-09-28, 12:08 Israel): the universe is the one whose every number is the rule's, the exact bands and the vacuum's pair, every divisor 1, matter's m the one integer of nature beside Gamma and T (`examples/events/rule.json`). Its pairs are the integers 1, 2 and 3 of the three exact rotations and the three axes: [1, 1] the vacuum's band, on which the two real fields stand, [1, 2] the exact band, [2, 3] the matter pair, cos omega_0 = 2 / 3, the first pair past the exact bands, which the universe of record approximates by 6,667 over 10^4, and [-1, 2] the third; its divisors are 1 (the well is the count: every held level is the count itself, so a count near Gamma div 2 is a horizon, the pace 0, and no body's Node exceeds it, the maximal coupling); Gamma is a multiple of 6 so that every pair is exact over it (the file's 6,000: m = 6,000, 3,000, 4,000 and -3,000); T is the one unit and cancels in every reading. So it carries zero free numbers, no G, no alpha and no m, and it is the universe: the universe of record and the Planck files are not the law's, and the tests run on this file (the owner's word of 2026-09-30).

**A pair's numerator may be negative**: the third's R_a = 2 num p_a^2 is negative, S is what the line makes it, the band is the mirror of [1, 2] (2 cos omega inside [-1, 1] at every wave number and every pace at or below Gamma, the edge's square P^2 = 2 den Gamma^2 div (den + num) = 4 Gamma^2, the rest term 12 (den - num) p_0^2 = 36 p_0^2), and the loader admits a pair with den > |num| as a massive kind and refuses den <= |num| and den = 0 by name; nothing of Rule3 changes.

**The bound body is one Node** (the owner's word, 2026-09-28, 12:30 Israel: every bound body fits in one Node, and that is what pixelates everything): under the divisor 1 a body that binds itself at rest is one Node, its count c in [0.2255 Gamma, Gamma div 2), the lower edge where the one-Node well first holds a rotation below the vacuum's band (the three-dimensional Green's function of the six Ports, a pure number of the rule; below it the record disperses), the upper the horizon (the pace 0, the Node reads nothing and freezes); its record is the one-Node line at its bound rotation omega_b(c) (0.841 at the edge, 0.464 at 5,412 of 12,000) and its tail outside is the well, evanescent by kappa = acosh((9 / 2) cos omega_b - 2) per Link (0.45 at 3,000, 1.27 at 5,000: the tail ends within three Links); its mode carries the count through the form, D = now^2 - next x before = b^2 (2 - 2 cos omega_b) at rest with both levels b, so a pixel of c quanta loads with the largest b whose square is at most c T den div (2 den - a), the fixed point of the division act, for the clock pair [a, den] of 2 cos omega_b (69 at 3,000, 97 at 4,000, 139 at 5,000 of 12,000 at T = 1; the root of c alone loads 1,812 quanta for 3,000, under every edge) and its tail as b t^(|dx| + |dy| + |dz|) rounded with t = e^(-kappa) (0.640 at 3,000, 0.362 at 4,000, 0.281 at 5,000); on an engine where the level enters the Link once (before the conformal term) the same Green's function puts the edge at 0.345 Gamma (4,136 of 12,000) with kappa 0.63 at 5,000 and 0.98 at 6,000, the number of that engine's first looks; a body of more quanta than Gamma div 2 is a cluster of such Nodes, each a bound body, clicking to one another. So between bound bodies there is nothing but the click and the band [1, 1]: the record does not leave its Node (kappa > 0), a quantum crosses a Link whole at a click and nothing else does ([the count's line](#the-counts-line)), the overlap of two tails within reach is read by the count's line and clicks (the exchange), and light and the two real fields carry the rest; a Node is a bound body or vacuum; the bound body keeps its record on the GameBoard and Rule3 steps it at its Node and along its tail as it steps every record (the one-Node line is the reading of its rotation, not a step of its own: with the six reads returning the Node's own level the line gives the Node's rest rotation, 1.05 at 3,000 of 12,000 by the pre-conformal coefficients and 0.62 by the conformal, and not the bound omega_b = 0.81 that the tail fixes; the tail is 0.64 of the level one Link away at 3,000 and carries the exchange and the fall), so the engine of the rule's universe is the engine of record on another file, and a step of the pixel alone is an optimisation for the day the tail is derived in integers. In the universe of record no body binds itself (the well is M div E_s, the edge M >= 0.2255 Gamma E_s), so its bodies are declared modes and the theorem does not reach them.

**The universe is bound**, the unification's assumption and no theorem (the owner's word, 2026-09-28, 12:37 Israel): every body is bound, no body is free, and a record that is in no bound body is a message between two clicks, the one that gave it and the one that will take it (a matter record below the edge cannot be a body and disperses; light never binds, its band's bottom is 0); a fall is the bias of a bound body's clicks, its tail longer toward the well (the local band lower there, kappa smaller), so the remainder crosses T first on that side; a click on a record with a partner label is entanglement and a click on a record with none is a measurement, and Bell's S reads that and nothing else; the assumption removes no number, it names the universe that has none, and where it fails (the universe of record, nature) the two distances stay.

**The click joins and parts** (the owner's word, 2026-09-28, 12:43 Israel: bound bodies join or part, and that is by clicks; every click local, **The click ends nothing** of 2026-09-30): two clusters whose tails overlap (within 1 / kappa, three Links) read each other by the count's line, and the interference current of two standing records at the rotations omega_1 and omega_2, a_i b'_j + b_i a'_j - a'_i b_j - b'_i a_j, is a sum of cosines of (omega_1 - omega_2) t and (omega_1 + omega_2) t with no constant term: its mean over the beat is 0 at every Link, so at fixed paces no quantum passes at first order and the counts swing at the beat about their laid values; a transfer is second order (the well moving with the count) or radiative (the messages), a run's finding, and where the smaller does give to the larger until its count falls under the edge it dissolves into messages the larger takes, the join a run of local clicks after which the smaller's levels go on as messages and nothing ends, one Node where c_1 + c_2 < Gamma div 2 and a cluster of two at the horizon otherwise, one record for the joined cluster; a cluster parts where a Node's count falls under the edge (it dissolves) or where two tails cease to overlap: the tail's e-fold is 1 / kappa (about two Links at 3,000 of 12,000) but the click's reach is where the Link's current a_1 a_2 e^(-kappa d) falls under T, d = ln(a_1 a_2 / T) / kappa, about 18 Links at T = 1 for two pixels of 3,000, and the beat's swing of the counts between two pixels is about omega_b e^(-kappa d) per interval (0.33 at two Links, 0.09 at five), no net transfer at first order: beyond the reach no click, parted, and a taker at the horizon overflows into a neighbour inside its own well (the real field 0.34 of the count one Link away) so the cluster grows a Node per click (a body never splits into three equal pixels: 2 x 0.2255 < 1 / 2 < 3 x 0.2255); the join and the parting are runs of local clicks, no record opens or closes anywhere, and there is no non-local act (**The click ends nothing**).

**The observer is a cluster**: a Node reads six Ports and a cluster's record is what its Nodes carry, so inside a cluster everything is seen (a GameBoard reading is the local language of its own record) and beyond its tail only a whole quantum arrives, a click.

**The tree**, the closure: the root is **The law in one line**; from it alone the exact bands, the colours as the click's three tallies, the edge P, entanglement as the click and the observer as a cluster are derived; with the named assumption the pairs from 1, 2 and 3 (den the three axes) the matter pair [2, 3] and the crack [1, 3]; with the named assumption the divisors 1 (the rule's universe) the bound body as one Node with the edge 0.2255, the horizon, the tail, the cluster, and the click that remakes, joins and parts;

**The universe is bound** is an assumption and **The conversion** a hypothesis; so the algebra is closed on one root, two named assumptions, one assumption of the universe and one hypothesis, with zero numbers, and is not closed toward nature by name: the three distances alpha = 1 / 137.036 (the fine-structure constant), m_e / m_P and m_p / m_e (the rule's universe has one pixel mass scale, its counts within [0.2255, 1 / 2] Gamma), each a computation of [the rows against nature](#the-rows-against-nature) (t) and (v);

**The three distances are the rule's** is the hypothesis under its own name that the three are derived. **No quantum changes family at a crossing** (the owner, 2026-09-30): a body's quanta that leave it stay its family and light is born by the write alone (**Light is born by the write**); every divisor is 1.

**The algebra of clusters** (the owner's word, 2026-09-28, 14:40 Israel: the algebra is closed, so the five looks must close, and the rule's universe is a universe of clusters alone, whose algebra may differ a little because nothing else is there; Cheshbon's section, 14:55, one closed derivation from the root on the one assumption "only clusters", with the Nature24 session's lines of 14:44): (1) **The Node holds its count**: a Node holds one integer, its count c, and nothing else;

**The count is the record's form**: in a universe of clusters the count is laid from the record and no declared level stands beside it, the body's count SUM_i D_i div T over its Nodes with D = now^2 - next x before the form's Node term, the well at a Node D_i div T each interval with the remainder D mod T the fields' source, the click that integer division (the pixelation), so a declared count that is not the record's **Sum D** div T within the gate is refused by name; a count far below zero (the Bell Experimenter's -4,566, 14:27) is the count parted from its record, a defect of the lay and never a reading, while the hole of -1 at an edge Link is the line's own, conserved and filled: the count's line is the plain division act with no clamp, no block and no guard ([the count's line](#the-counts-line), **The inverse**).

(2) **The count is read through both holders** (the owner's line of 2026-09-30, **The vacuum's row steps at the divisor 1**, the open item closed; the reading computed by the advisor, #1495 comment 5902351186): a pixel's pace reads its count through both holders of the content, the contact well of the bound charge [1, 2] and the field of the vacuum's row [1, 1]: the well laid each interval is D_i div T, 0.63 of the count at the Node for the standing mode and never the count; the field at the Node is the rest's sum over the whole body's wells (884 for 2,000 at the Node on rule.json, of which 480 the Node's own well); the window of a pixel on rule.json is the narrow branch from about 1,650 at the Node (2,460 in all) to the horizon at about 4,900 at the Node (5,270 in all), where the guard ends the run by name; below 2,460 in all a cloud; one quantum is a message; one row read twice (as the hold and again as the record's source) is a reading of the engine that differs from the algebra, a defect and never a finding; the tree's numbers (the edge 0.2255, the bound states, the sieve's periods) are recomputed under this before any blind number.

(3) **The edge**: a pixel binds itself where the GameBoard's Green's function of its own well closes, at 0.2255 Gamma (2,706 of 12,000) on the law and at 0.3444 Gamma (4,133) on an engine where the level enters the Link once; below the edge a pixel is a cloud and disperses.

(4) **The tail**: the bound rotation omega_b, kappa = acosh((9 / 2) cos omega_b - 2), t = e^(-kappa), the level b t^d and the well c t^(2 d) at d Links; on the law 3,000: omega_b 0.8105, t 0.640, the wells 1,229 / 503 / 206 at 1 / 2 / 3 Links; 4,000: 0.6578, 0.362, 524 / 69 / 9; 5,000: 0.5137, 0.281, 395 / 31 / 2; with the level once 4,400: 0.8290, 0.754, 2,501 / 1,422 / 809; 4,700: 0.8055, 0.619, 1,801 / 690 / 264; 5,000: 0.7779, 0.532, 1,415 / 401 / 113; 6,000: 0.6741, 0.377, 853 / 121 / 17; two pixels bind together while each count with its partner's well at their distance stays within the horizon.

(5) **The transfer** between clusters is no first-order act: the counts swing at the beat with about omega_b e^(-kappa d) per interval at d Links and return, and a net transfer is second order or radiative, a run's finding; the click's reach is ln(a_1 a_2 / T) / kappa (**The click joins and parts**).

(6) **The light** is the sign holder's own record, born by the write (**Light is born by the write**): a rotating body writes its Wronskian's quanta into the holder of the sign at its Nodes each interval; a static body writes a static level and radiates nothing, a breathing or moving body a varying source that the row carries away at one Link per interval as a wave, and that wave is the light, its count moved by its own count's line from 0, a quantum born with its hole; a real record, so neutral (**The sign is the rotation sense**); a rotating body reads the sign holder by its own sense at its own Nodes, so a breathing body reads the light it writes and its pace answers, the radiation reaction, and whether it cools is a run's finding.

(7) **The one integer**: the universe of clusters carries Gamma and nothing else, the pixel's size in quanta, every divisor 1.

**The five looks on this section**: on an engine that reads the count once with the level once the bound window is 4,133 <= c < Gamma div 2 less the partner's well, so (a), (b) and (c) stand at 5,000, (d) at 4,400 and 4,700, (e) the giver 4,400 and the taker 5,000 (the clocks' ratio 1.066); on an engine that reads the count twice or more no pair binds under Gamma (the de Broglie Experimenter's 12,825 at 5,000 / 5,000, 14:22) and the fix is the reading, never the pair; with the conformal term (the level twice) the looks stand at 3,000 and 4,000 on the edge 2,706.

**The screen is a cluster** (the owner's question, 2026-09-28, 14:51 Israel: does what the look runs on the screen also have to be a bound body, since the universe holds bound bodies alone; Cheshbon's line, 14:55): everything that stands on the GameBoard of a look is a bound body or a cluster of them, the source, the screen, the slit's walls, the mirror and the detector alike, each pixel at or above the edge; a face of the GameBoard is no body, a click on a face is no click, and a look with a declared element that is no bound body is not a look in the rule's universe; a solid wall of adjacent bound pixels does not exist, two adjacent pixels at the edge pass the horizon on their Link in every case, so a screen is a sieve of pixels at a period s with the Links between them under the horizon: on the law 4,000 at s = 2 and 3,000 at s = 3 (a chain of 3,000 at s = 2), with the level once 5,000 or 6,000 at s = 2 and 4,400 at s = 4; a sieve at s = 2 reflects the light of lambda = 4 (Bragg's condition, 2 s = lambda) and is the wall and the mirror of the rule's universe, and a row of taker pixels at s = 2 is its screen, so the five looks are rewritten on sieves and clicks alone before their next run.

**The hierarchy is recursive** (the owner's word, 2026-09-28, 14:57 and 14:58 Israel; Cheshbon's line, 15:05): a cluster of clusters is the same structure one level up, Nodes each a bound body clicking at one another, with no number that bounds the depth;

**The click is the pointer**: the click is the only thing that passes between a cluster and its neighbour and between a level and the next, so from inside a cluster everything is seen and beyond the tail only a whole quantum arrives (**The observer is a cluster**);

**The levels at a Node are the nesting**: the three held levels of a Node, the matter's tail, the charge's well and gravity's well, are the three kinds of binding by rank, and the size of a level is the depth in its kind, gravity's well at a Node being Rule3's wave on [1, 1] sourced by every body's form, 1 / r at rest (**The fork, decided**), so a GameBoard reading names the clusters a Node belongs to; a level n + 1 is bound by the same inequality as the level 1 with the cluster's total count over its members' spacing in place of a pixel's count over one Link, and the one bound on the depth is the horizon at a Node, the content read there under Gamma, at which a cluster's centre is the horizon pixel.

**The couplings are at the edge** (the Nature24 session's line, 14:44, and the owner's word of 2026-09-30): every coupling is the edge the rule allows and no number: every divisor is 1, a pixel's count at most (A^2 / T)^(1 / 3) and its well at least 0.2255 Gamma;

**The stable pixel is one**: where the small gives to the large until it melts (at second order or by the messages, **The click joins and parts**), the bound universe has one stable count, the horizon pixel, the endpoint of accretion (**The proton is the horizon body**, [the hypotheses under their own names](#the-hypotheses-under-their-own-names)), and its second body, the electron, one free quantum; the distance m_p / m_e is the road to Gamma through the well ([the rows against nature](#the-rows-against-nature) (t)).

**The wavelength is the giver's** (Cheshbon's line, 15:05, on the Light Experimenter's question of 14:52): the given light carries the giver's bound rotation, and on the band [1, 1] cos omega = (2 + cos k) / 3 along an axis, so cos k = 3 cos omega_b - 2 and lambda = 2 pi / k: a pixel at the edge (omega_b = acos(2 / 3)) gives k = pi / 2 and lambda = 4 exactly, the law's wavelength derived; 4.18 at 3,000 and 5.29 at 4,000 on the law, 4.07 at 4,400 and 4.38 at 5,000 with the level once; a deeper pixel gives a longer wave, and a mode file's wavelength is this number rounded to the Link, 4 for every pair of the five looks.

**The closed GameBoard has no rest** (on the Light Experimenter's refusal of 14:59): the sum's rest on a GameBoard closed on every axis exists only under a net count 0, so a bound universe closed on itself carries a mean of the held field that drifts by the net count over the Nodes each interval, the finite board's word and no physics of the universe (the advisor's closure of 2026-09-30, no look resting on it); a look keeps one axis open with its pixels far from the faces, and there is no sink, a count being never negative.

**The width bounds A by the least of the two** (Cheshbon's line, 15:27, on the Nature24 session's finding at Gamma = 24): the amplitude unit A is the largest amplitude at which every total of an interval stays inside the width, Rule3's 2 w A with w = 6 Gamma^3 and the count's line's 6 A^2, the least of the two and never Rule3's alone; at Gamma = 24 the two give 3.7 x 10^13 and 1.2 x 10^9, and the universe of 24 runs inside the width; a pixel's rotation lives in its clock pair.

**The electron needs no band of its own** (the advisor's closure of 2026-09-30, #1519 comment 5903952622, on the owner's question of 2026-09-28 what the electron does): the electron is one quantum of the matter family with the sense -1, a message and no pixel, stable by the integer (one quantum does not disperse into fractions), its charge the proton's exactly since the sense is a sign, the positron the same quantum in the sense +1, and pair creation the conversion between the two senses (**The electron is one quantum**, [the hypotheses under their own names](#the-hypotheses-under-their-own-names));

**The mass is the well, the count the baryon number** (the owner's word of 2026-09-30, #1519 comment 5904035389, "go with it and put a caveat", on the advisor's closure 5903952622; replacing **The mass is the count**): what sources gravity, a body's mass, is its well, the sum over its Nodes of D_i div T; the count is conserved by the count's line and is the baryon number, not a mass. A free quantum of matter at rest has a well equal to its count, and a bound body's well is under its count, 0.70 of the count at the edge, 0.62 at 2,000, the minimum 1,636 at about 2,500 at the Node and 0.39 near the horizon ([the rows against nature](#the-rows-against-nature) (u)): the binding lightens. The caveat, as decided: the reading stands while the inertia agrees with it; the momentum reading n = 3 Q j_a div T takes the count as the inertia's unit, and the advisor computes the body's inertia along the branch; if the inertia of a bound body is its well, the momentum reading is re-read with the well and the Eotvos balance holds (a bound body and a free quantum fall alike and weigh alike); if it differs, the line is reopened and the difference is a finding against nature. Which body is the proton is computed, not chosen: the body where the well and the inertia agree; Gamma follows from m_p / m_e = 1,836 through that body's well fraction, about 5,150 with the horizon body and about 6,200 with the edge body ((t)), and the count ratios (3,672 to 8,142, 1,950, 4,300 and 6,500) are withdrawn. What stays by name: one quantum is one energy and its rotation is its frequency, nature's E = h nu being the record's click rate, and the spin 1 / 2 is open.

**The generator is Rule3** (the owner's word, 2026-09-28, 15:28 Israel: no floating point in the generator; Cheshbon's integer run at Gamma = 24, 15:41 and 15:43): a body's bound record is what Rule3 makes of its count at its Node in the engine's own integers, seeded at the Node with the count's well held, run on its GameBoard over many periods until the record stands (its levels repeating over a whole period), and the record itself is the mode file; its period P, its amplitude b, its clock pair [next + before, now], its tail level(d + 1) / level(d) and its wavelength are readings of the standing record and never inputs, a clock pair or a tail computed in floating point being a tool's defect; at Gamma = 24 Rule3 in integers gives the periods 9.6, 11, 12 and 14 at the counts 8 to 11 on the law (the Green's function: 9.55, 10.8, 12.2, 13.8), and the pixels the integers hold are b = 5 carrying 8 to 10 quanta and b = 8 carrying 12 to 15;

**The count is the record's form over its period**: an integer record's form D at a Node moves between 0 and 2 c within one period at Gamma = 24, so the count is (SUM over the period of D) div (P T), read once per period on the record's own clock, never the form of one interval as the count (the form of one interval is the well, that interval's source of the fields, the hold's row of [the primitives](#the-primitives)), which as a count kills a pixel of the law and drives a pixel of the level once to the horizon within ten intervals; a declared count is checked against the count the lay makes from the loaded record (the weighted share, **The lay and the wall**) at the gate ((|c - laid| - 1) div 2)^2 <= c, the rounding's inequality written as a square and never as a root (the rounding of an integer amplitude moves the form by about one and a half times the root of c), refused by name beyond it; a count moves only whole, and a clamp that sets a negative result to 0 creates quanta and is no rule: the deficit is the hole of [the count's line](#the-counts-line), the count -1 with its remainder in range, which the line conserves and fills.

**Gamma is not constant**, a hypothesis under its own name (the owner's word, 2026-09-28, 15:44 Israel: every tick the universe grows by 6, which explains the expansion and how with the size more and more creatures became possible; Cheshbon's line, 15:50): Gamma_(t + 1) = Gamma_t + 6, the step the six Ports of a Node and no free number; the rule's physics depends on the ratios c / Gamma and m / Gamma alone, so every pair steps with Gamma ([m_0 Gamma_t div Gamma_0, Gamma_t], the matter +4 and light and the charge +6 per interval) and the wall and A are derived from Gamma_t each interval, the file holding node_clock as [Gamma_0, 6] and the engine no number; a count is the integer its Node holds and stays, so a pixel that does not gather falls under the rising edge 0.2255 Gamma_t and dissolves after (c / 0.2255 - Gamma_0) / 6 intervals, the small giving to the large being the way a body keeps its c / Gamma; the distinct bound counts between the edge and the horizon number 0.2745 Gamma, one and two thirds more kinds each interval (7 at 24, 1,647 at 6,000); light on [Gamma, Gamma] does not drift, the clocks of pixels do, a pixel of a fixed count slowing as c / Gamma falls with the rate H = (6 / Gamma) |d ln omega_b / d ln (c / Gamma)|, 5 x 10^-4 to 1.3 x 10^-3 per interval at 6,000, the rule's Hubble rate, and Gamma = 6 t reads the universe's age in intervals (1,000 at 6,000); a look reads it as the takers' clock ratio growing by (6 / Gamma)(s_taker - s_giver) per interval, about 2.6 x 10^-4 at 6,000; at Gamma = 24 every pixel dissolves within three intervals of stepping, so the five looks keep Gamma fixed and a stepping Gamma is a look of its own.

**The close's weights under the term** (Cheshbon's line, 16:06, on the Newton Experimenter's reading of 15:56): the weighted current SUM q_n (now_n - before_n) is conserved where the Link coefficients are reciprocal in the weights, q_n R_(n to a) = q_a R_(a to n); without the conformal term R is symmetric and q_n = 2^16 Gamma^2 div p_n^2 at the clock's pace p_n = Gamma - c_n is exact, while under the term R_(n to a) = 2 m (Gamma - 2 c_n - c_a)^2 is not symmetric and no weight per Node is reciprocal on an uneven well, so B at the clock's pace leaves a current that the zero mode grows without bound; under the term the weight's pace is the Node's mean Link pace, p_n = Gamma - 2 c_n - (SUM over the six Ports of c_a) div 6, exact where the neighbours' counts are equal (a chain: Gamma - 2 c - t_x) and within the neighbours' spread otherwise, and only a current weighted on the Links is exact everywhere.

**The two readings of Gamma are two levels** (the owner's question, 16:27; Cheshbon's line, 16:35): under **The hierarchy is recursive** every level has its own Gamma and its own interval, a level's interval being the period of the record one level below it, so the proton to electron ratio reads the atomic level's Gamma (about 5,150 through the well, [the rows against nature](#the-rows-against-nature) (t), its interval the proton's period over about eight ticks) while the universe's age reads the top level's Gamma = 6 t, one tick for both being impossible; 1,836 is a local ratio of a cluster within a cluster; the tick ratio of one level is the cluster's period over the pixel's, P_2 / P_1 = e^(kappa d), 7.6 for two pixels of 2,000 at two Links at Gamma = 6,000 (the band 5 to 11, a number the join look reads as the breathing period of the pair's total count), and about 66 such levels lie between the atomic Gamma and the cosmic one.

**The bound states of a Node** (Cheshbon's table, 16:45; a reading for the pixel's first look): the bound states of a Node at a given Gamma are one per integer amplitude b from the edge to the horizon, each carrying the count c = b^2 (2 - 2 cos omega_b(c)) at its self-consistent rotation: two at Gamma = 24 (b = 5 and b = 8) and about 67 at Gamma = 6,000 on the law (b = 46 to 112, c = 1,396 to 2,700, the period 7.5 to 13.4), the ratio of neighbouring states 1 + 2 / b, a near continuum that singles out no ratio.

**Three kinds of binding, not three levels** (the owner's reading, 16:47; Cheshbon's line, 16:51): the three ranks give three kinds of binding, quanta into a pixel by the matter's tail (the step in count the pixel's c, in ticks its period), pixels into a white cluster by the holder of the sign's field (at the divisor 1), and white clusters into a gravitational cluster by gravity's 1 / r well (the vacuum's row stepped as Rule3's wave), and the third kind nests without bound, so the count of gravitational levels is the universe's history and no number of the law.

**The vacuum's row steps at the divisor 1** (the owner's line of 2026-09-30, replacing **The well is the count and no field** of 2026-09-28): in the rule's own universe the massless held row [1, 1] (gravity, the tensor, the one field that is not a click) is a record at every Node that steps by Rule3 at the pace 1 with the wall 3 den, a_next = (S_6(a_now) - 3 a_before + r) div 3, sourced each interval by the hold's division act with the wells of the families that read it, (w (D div T) + r) div E_s, and started at its rest, the fixed point of the division act with its remainder (the start's iteration), which around a static source is the six Ports' Green's function: 1 / r and no chosen number. The lattice's values per quantum at the divisor 1 are **The lattice constants** of [the paces](#the-paces), 3 G(0) = 0.7582 s at the Node and 3 s / (4 pi r) far away, s the source's quanta per interval. A static pixel gives a static field (the fixed point is a pair, level and remainder, so nothing rings); a moving pixel a field that follows it one Link per interval, causal and retarded; the inverse is Rule3's direction -1 and the division back. Every family of quanta reads the row's level into its pace: a pixel its own field (the self-binding, **The count is read through both holders**), another's (the pull, orbits, the fall); light reads it too and is bent by twice the clock's share. A held row with a gap (num < den; the bound charge [1, 2]) is not stepped: its level is the well laid each interval, the sum over the sourcing families of w (D div T) through its divisor, the count itself and no field, for every reader, since its rest is 0 beyond the reach. Light can read the massless row wherever its rest is at least one unit (the whole laboratory at the divisor 1); it keeps away from open faces, where the rest is 0, or the board is closed, where the row has no rest and its level drifts upward uniformly and never below zero. The line of 2026-09-28 rested on the Bell finding at Gamma 24 with a pixel of 10, where the rest at two Links is 1.2 units, under the resolution: a finding of the small universe and not of the stepping.

**The gate reads the form at any phase**: a standing record's D = now^2 - next x before at its Node is B^2 sin^2 omega_b at every interval, B its peak, and equals b^2 (2 den - a) div den with b the level where now = before alone (b = B cos(omega_b / 2)), so the lay reads the record after one interval of Rule3 with no formula of a phase (the Clock's 5,310 against 4,379 is B read as b).

**The generator has no sink**: Rule3 is reversible and nothing leaves a GameBoard but a quantum by a click at a face; a fill of 0 beyond an open face and a slab zeroed each interval are walls (the Node beside reads 0: the reflection with the sign flipped), so the unbound part of a seed never leaves; a seed of one Node carries the mode's share 1 / (1 + 6 t^2 + 18 t^4 + 38 t^6 + 66 t^8) (0.18 at Gamma = 24 with the level once, 0.62 on the law) and the rest is debris spread over the GameBoard's V Nodes, so the record is read at the Node over many periods on a GameBoard whose V dilutes the debris and purified by re-seeding from the record within three Links of the Node at its peak's phase, 0 elsewhere, integers alone, each pass leaving the debris its share within reach (about 180 / V); a record whose pair lies inside the vacuum's band (the Clock's [8, 8], the period 6, against the bound periods 8 to 14 at 24) is a mode of the walls and no pixel, and every reading is at the Node, never the GameBoard's sum.

**The generator of the rule's universe writes bound bodies alone** (the owner's word, 14:32): a body is its count at its Node; its record is the bound state of that count and nothing else, b through the form and the tail from kappa (**The wall is one**), no free record and no declared mode; a world file holds counts, their bound records and the band [1, 1], and nothing more.

### The interval

The engine steps every family from the state at the interval's start to
the state at its end. Every read is of the start's values: the six
neighbours' levels, the Node's own pace, the arrivals, never a value
written in the same interval; one Link per interval and nothing in zero
time. Before the first interval the whole initial state is checked once
against the guard ([the paces](#the-paces), **The guard**), and no act of
the interval reads a Node to refuse. The interval has four acts, in order:

(i) the signed read: every family's paces from the held families' levels
at the start; (ii) Rule3 on every record: each family of quanta's two
level pairs by its pair and its paces (the holder of the sign's time part
is its real pair and steps so, bent by the content it reads), each
holder of the content's parts without a gap at the pace 1; (iii) the
count's line and the sense's line on every family's count and sense (the
current through the Ports), the tension on each axis booked beside them,
and the clicks at the Nodes declared to report, the rise of a family's
count there; (iv) the hold: each held family's time part gains its
source over its divisor (a row with a gap is laid, the well itself), its
tensions the sources' stresses; light is born here, by the write of a
rotating body's varying Wronskian into the sign holder's record.

Backward, the acts run by Rule3's direction -1: a held row's hold back
once every family that sources it is booked back, a family of quanta
booked back (its lines back from the levels as the step left them, its
records and its wells back) once its own hold is off, so the holder of
the sign goes before the rows it sources; every interval returns bit for
bit, and only the lay is not taken back. The back-in-time gate (the
owner's word of 2026-09-30) is the whole run: N intervals forward and N
back, every array of every family compared bit for bit at every interval
on the way back, MATCH or MISS by name; a held row with a gap keeps one
interval of its past, so over more than one interval it returns only
where its level stands still (the row "the hold").

### Readings and measurements

A **measurement** is a detector's click: the rise of a family's count
across the Nodes the file declares as the detector, the count's line's
own quantum arriving there ([the count's line](#the-counts-line));
nothing ends and nothing is handed over. Only a measurement is compared with nature. A
**GameBoard reading** (a level, a support, a total, a body's centre) is
a diagnostic and is labelled so wherever it appears; a number whose kind
is not named is not a result. Displays read state and write nothing.
Every run is headless; the readings are declared in the world file and
written in one format, each labelled DETECTOR, GAMEBOARD or HOST.

## Rule3

### The line

**The law in one line**: at every Node, each interval, the division act below with its coefficients from the family's pair and the Node's paces; every level on the GameBoard is written by that same act ([a family's write](#the-primitives)), a quantum moves whole when a remainder crosses T ([the count's line](#the-counts-line)), and everything else is a number in a file. Every family, at every Node, with the wall w, the read coefficient R_a on
each axis a, the self coefficient S, the level a_now at the interval's
start, a_before one interval earlier, and the remainder r kept at the Node:

  w a_next + r' = SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now - w a_before + r,
  0 <= r' < w,

arr_(±a) the **arrival** through the Port ±a: the neighbour's level; 0 beyond an open face;
the Node's own level on a folded axis. The remainder r is the Node's own
and never travels.

The coefficients at a Node, from its paces ([the paces](#the-paces)) and its
family's pair [num, den]:

  w   = 6 den Gamma^2,
  R_a = 2 num p_a^2,
  S   = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num (p_x^2 + p_y^2 + p_z^2).

At the vacuum's pace p_0 = p_a = Gamma the line is the plain second-order
wave rule of the pair: a_next + a_before = 2 cos omega a_now with the
six-neighbour coupling, the rotation omega_0 with cos omega_0 = num /
den at wave number zero. A held family's field steps at its row's pair with the pace 1 and the wall 3 den, at first order.
**The clock once and the Link twice**, the two paces in one line: from the coefficients above, the rotation at a Node of the clock's pace p_0 and the Link's paces p_a is cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) SUM_a (p_a / Gamma)^2 (1 - cos k_a), the mass term scaling with the clock's square and the band term with the Link's pace. Two readings follow and no third.

(i) **The clocks shift alike**: at k = 0 every massive band's rest rotation obeys 1 - cos omega_b = (p_0 / Gamma)^2 (1 - cos omega_0), one factor for every family, so two bound bodies at one Node shift their clocks alike (the redshift Phi = c / Gamma to the first order) and a packet's fall in a pace gradient, Delta x |d omega_b / d c| x (c_+ - c_-) / D, does not depend on its family beyond the band's own Delta and d omega_b / d c (item 3 of [what is open](#what-is-open)).

(ii) **The Link is twice**: along a Link every wave's speed falls with p_a = Gamma - 2 c - t_a, the level entering the Link twice and the clock once, so light, which reads the vacuum's row as every family does, is delayed and bent into a mass by twice the clock's share (the bending 4 U_1 / b, [the rows against nature](#the-rows-against-nature) (b)). The line is not conformal: a light wave at a fixed wave number scales with (p_a / Gamma)^2 and a bound mode at rest with (p_0 / Gamma)^2, and the two differ already at the first order in c / Gamma (0.625 against 0.411 at c = 3,000 of 12,000 on [8000, 12000], k = 0 against pi); a light record's rotation is conserved along its path, the paces being static, so a light record read against a matter clock at one level reads the clock's shift, (i), and the bending reads (ii).

### The direction

Let sigma be the direction, +1 forward and -1 backward, and let div and
mod be the floor division and its remainder in [0, w), and rho the
remainder carried in. With

  u = sigma (SUM_a R_a arr_a + S x - w y) + rho,
  z = sigma (u div w),  rho' = u mod w,

forward (x, y, rho) = (a_now, a_before, r) gives (z, rho') = (a_next, r');
backward (x, y, rho) = (a_now, a_next, r') gives (z, rho') = (a_before, r).

**Proof**. Forward, sigma = 1, the line is the definition of div and mod.
Backward, sigma = -1: write Y for the right side's first two terms, SUM_a
R_a arr_a + S a_now. Then u = w a_next - Y + r', and z = -floor(u / w) =
ceil((Y - w a_next - r') / w). From the forward line, Y - w a_next - r' = w
a_before - r with 0 <= r < w, whose ceiling divided by w is a_before
exactly; and rho' = u - w floor(u / w) = w a_before - (Y - w a_next - r') =
r. So the backward call returns (a_before, r) bit for bit; the reversibility
of every run needs no second function. Checked bit for bit on 20,000 random
cases against a forward and a backward function written separately.

### The four acts

Rule3's line is one act; declared coefficients make it four:

(a) **The read**, the line above over the GameBoard (the six arrivals); (b) **The one-Node step**, the line with the neighbours' reads declared 0: a_next +
a_before = (a / b) a_now, the rotation by the angle whose doubled cosine is
a / b (Chebyshev's recurrence); with a / b = 1 and the coefficient on
a_before declared 0 it keeps a level; with a / b = 2 from (0, 1) it counts,
a_t = t; (c) **The division**, the line with R = S = 0: w a_next + r' = the
numerator + r, Euclid's division with the remainder kept; (d) **The load**, a
declared integer in the numerator, how a count enters a level.

**A composition** of Rule3's acts with declared coefficients is a finite
sequence of these acts, each with its coefficients (a pair, a weight, a
wall, a load) declared in the files, applied to declared levels.

**Theorem** (what the acts can form). Every composition of the four acts is
a piecewise-linear function of the levels with integer slopes: a sum of
linear forms and of floors of linear forms, composed. No such function
is quadratic in the levels.

**Proof**. Each act is a linear form of the levels or the floor of one; a
floor of a linear form is piecewise linear with integer slopes; sums and
compositions of piecewise-linear functions with integer slopes are of
the same kind. The second difference of such a function in any one
level is 0 almost everywhere, while the second difference of a product
now_i before_j in the pair (now_i, before_j) is 1. So nothing bilinear
comes from the acts alone.

What the theorem separates: every product of two levels in the engine
is a **booking**, a reading of a bilinear form with declared
coefficients and no write ([the booking](#the-booking)); the one thing written from a
product is the count, by the count's line ([the count's line](#the-counts-line)), and that
product is Rule3's own conserved current.

**The three tests of every rule**. A line enters the law only if it is
generic (one primitive with declared integers, no family's name and no
kind), vector (one of the acts on the state, no root and no float) and
local (its own record and the six neighbours, nothing kept at a Node
beyond the law's numbers). A hypothesis that needs more is stated under
its own name, outside the law.

### The paces

The **pace** of a Node for a family is what its reads make of the Node
clock:

  p_0 x p_0 = (Gamma - c)^2 + c^2,  c = SUM over the reads of (weight x by x the read family's time level at the Node),
  p_a x p_a = (Gamma - 2 c - SUM over the reads of (weight x by x the read family's aa component div 2))^2,  a = x, y, z,

one division per read per axis, rounded at the read: the pace is a coefficient of the interval and no level, so no remainder is kept for it (nothing at a Node but the law's numbers). A positive weight is a hollow (the read family's level
slows the clock, an attraction); a negative weight is a hill. By sign the
weight is multiplied by the reader's q at the Node, the sign of its own
sense there (**The sign is the rotation sense**). A family with
no reads steps at p_0 = p_a = Gamma, the plain rule. The clock's slowing
is this pace: a record at a Node of pace p rotates and moves as a record
at Gamma does, with its intervals p / Gamma as long.

**The reads are the held row's pair's** (the owner's line of 2026-09-30, **The vacuum's row steps at the divisor 1**): every family reads a held row without a gap (num = den) as its stepped field and a held row with a gap (num below den) as the well laid each interval, the rule on the row's pair alone through its divisor, no name and no number; the guard stands two-sided at load: the vacuum's row is non-negative where light travels (its rest at least one unit over the whole laboratory at the divisor 1), and a trough below zero where light reads it in the initial state (beside an open face) is refused by name, since on the vacuum's pair the edge P = Gamma is a theorem (at wave number pi on every axis the multiplier is 2 - 4 (p_a / Gamma)^2, exactly -2 at p_a = Gamma) and light tolerates no hill; in the run the arithmetic carries it (**The guard**).

**The sign is the rotation sense** (the owner's word of 2026-09-30): a family of quanta carries its record as two level pairs, (re, im), two solutions of the same line stepped by one call of Rule3 with one set of coefficients, each with its own remainder (a held family's parts stay real); the charge density at a Node is the booking W_i = re_now x im_before - im_now x re_before, the Wronskian of the two pairs, which Rule3 conserves exactly with the conserved form's weights 1 / p_i^2 (**D M** symmetric), its local change the Link current G_ij = num (im_i re_j - re_i im_j) at the levels the step started from; the sense is laid once at the first act from w W_i div (2 p_i^2) at the count's wall W_c and moved by the count's line on that current, SUM (W_c k + r) conserved to the bit; a real record (im = 0) has W = 0, so light, the sign holder's own real record, is neutral, and a rotating record has W of either sign by its sense (-A^2 sin omega for e^(+i omega t), +A^2 sin omega for e^(-i omega t)). The sign is the rotation sense and no key: the reader's q at a Node is the sign of its own sense there, the read by sign multiplying the holder's level by it, and the holder of the sign is sourced by the Wronskian's quanta, (W_i + r) div T each interval, over its divisor (the hold's row); the count of (re, im) is laid from the sum of the two pairs' forms, so a rotating record's count is its |A|^2; pair creation is the conversion between the two senses, and the hole stays the matter count's debt.

**The level enters the Link twice and the clock once**: the time level lowers the clock's pace p_0 once and each axis's pace p_a once more, so a wave's speed along a Link falls by the level twice (the Link as well as the clock, as nature's light past a body bends by twice the clock's share) while a mode's rest rotation, from S alone, falls by the level once (the owner's word, 2026-09-28, 08:40 Israel: the light experiment settles the symmetries inside the engine, with Nature24's line of 08:55 Israel; the bending's centroid against the twin reads it, twice the clock's share).

**The clock's second order is the composition** (the owner's word, 2026-09-29: simplify the clock): each unit of the level slows the clock as it already stands, p_0 = Gamma (1 - 1 / Gamma)^c, whose square to the second order is (Gamma - c)^2 + c^2 = Gamma^2 (1 - 2 Phi + 2 Phi^2) in the level's share Phi = c / Gamma; Rule3's coefficients take the paces' squares as written, no division act and no rounding, and no act takes the pace's root: the guard at load compares the squares, and p_0 = Gamma - c + c^2 div 2 Gamma to the unit is a reading of the algebra; the Link's pace stays Gamma - 2 c - (the tensions div 2), the level entering it twice.

**Computed** by the geometric optics of the band beside the paper (einstein_check.py, both forms of S): the light's bending 4 U_1 / b (2.02 x Newton's) with the clock to the first order or the second, the periapsis advance of the matter pair 7 pi U_1 / (a (1 - e^2)) (1.17 x Einstein's) with the clock to the first order and 6 pi U_1 / (a (1 - e^2)) (1.00 x Einstein's) with the second order; the second order of the clock is the line and the engine follows it (the owner's word, 2026-09-29, with the Link twice).

**The guard**, two-sided and on squares, once at load (the owner, 2026-09-30: the root leaves the run, and everywhere): 0 < p_a and p^2 (den + num) <= 2 den Gamma^2 at every Node, with the edge's square

  P^2 = 2 den Gamma^2 div (den + num),

Gamma^2 for light and above it where num < den, read on the clock's square p_0^2 = (Gamma - c)^2 + c^2 (never 0) and on each Link's pace p_a = Gamma - 2 c - t_a alike, over the whole initial state and never in the interval. Below 0 a pace is no clock; beyond P the step
is unstable: the mode at wave number pi on every axis has the factor (S - 2 SUM_a R_a) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 - 4 (num / den) (p_a / Gamma)^2, which
is -2 num / den in the vacuum and stays at or above -2 wherever p_0 and p_a are both at or below P,
since (P / Gamma)^2 (2 - 2 num / den + 4 num / den) <= 4 exactly when P^2 (den + num) <= 2 den Gamma^2;
a pace beyond P lets the record grow without bound,
and every pace at or below Gamma is inside it. A hill lessens a hollow and never exceeds it; an initial state outside
the guard refuses the run naming the Node. In the run no act reads a Node to refuse: every coefficient of Rule3 is a square, R_a = 2 num p_a^2 passes through 0 as the content reaches Gamma div 2 (the Link closes: the horizon) and reopens mirrored beyond it, and beyond P the mode at wave number pi grows until the host's trap on the arithmetic's width ends the run (the amplitude bound A is derived from the width for this reason); the report gives the pace's minimum from the final state as a GameBoard diagnostic, and the interval at which a run crossed 0 is found by the inverse when wanted. No act of the law takes a square root: the loader's amplitude bound and the generator's scales are the fixed point of the division act iterated, x <- (x + n div x) div 2 from above until it repeats (Newton's integer iteration, the start's own act), the largest x whose square fits.

**The band at a pace**, a reading of the line and no new rule: at a Node of the clock's pace p_0 and the Link's pace p_a on every axis a record's rotation at wave number k along an axis is cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) (p_a / Gamma)^2 (1 - cos k), with SUM_a (1 - cos k_a) in place of 1 - cos k off an axis, so the band of rotations a body's Nodes carry narrows with the paces: a record whose rotation lies outside the band there is evanescent inside (for [1, 1], cosh kappa = (Gamma / p_a)^2 (1 - cos k) - 1 per Node) and is reflected whole, and one whose rotation lies inside is slowed to the band's group velocity (num / (3 den)) (p_a / Gamma)^2 sin k_in / sin omega with 1 - cos k_in = (Gamma / p_a)^2 (1 - cos k) for [1, 1]; light ([1, 1]) meets a total mirror exactly where p_a < Gamma sin(k / 2), that is where the count c exceeds Gamma (1 - sin(k / 2)) div 2 (1,464 at lambda = 4 Links, 1,946 at 4.78), and a window otherwise, with the step's partial share at each face.

**The lattice constants**, the six Ports' own, exact and no number of nature, stated here once: the massless row's rest around one static source of s quanta per interval at the divisor 1, by the start's iteration on an open box with its faces' constant image removed, is 3 G(r) s with 3 G(0) = 0.7582 at the Node and 0.2582, 0.1286, 0.0826, 0.0608 and 0.0483 at 1 to 5 Links (r x level 0.258, 0.257, 0.248, 0.243, 0.242, toward 3 / (4 pi) = 0.2387 far away; on the box of 61 Nodes the levels read 0.0067 lower, on the box of 41 0.0099 lower), of which 0.76 s at the Node and 0.24 s / r beyond are the continuum's; light's speed at long wavelength is 1 / sqrt(3) Links per interval (on [1, 1] cos omega = (2 + cos k) / 3 along an axis, so omega = |k| / sqrt(3) as k goes to 0, and (1 - 2 x) |k| / sqrt(3) at the content x = c / Gamma, [the rows against nature](#the-rows-against-nature) (b)), under the causal bound of one Link per interval, the arrival's own speed; the two differ, and what in nature is one Link and one interval rests on the two units Gamma and T ([the constants](#the-constants)).

A body is a balance of a hollow and a hill of different ranges: a
hollow alone in three dimensions binds no record (it collapses into its
own well or disperses); gravity is the one-signed exception. This is
[the stable body theorem](#the-functional-and-the-dilation): each held row
adds sigma s (2 - s) times its well energy to the second variation along
the dilation, s the row's scaling power at the body's size.

### The bound

The rule's total at a Node whose levels and arrivals stand at the
amplitude A is at most 6 A |R| + A |S| + w (A + 1). Every world declares
integers under which this total sits below 2^63 - 1, the width of the
engine's integers, or the loader refuses it naming the total; the
generator's amplitude unit is the largest A that keeps it inside
([the generator](#the-generator) (f)). With Gamma = 10^4 and A = 2^20 the total is near 3 x
10^18, one third of the room.

### The self-source

The **self-source** of a family with the unit P_2
above 0, at every Node from the start's levels,

  Sigma_self = (SUM over the six Links, the family's records and their levels of (a_j - a_i)^2) div P_2,

is subtracted from the step's right side as w Sigma_self: each
difference is a read act, its square a booking of the family's own
levels, the division Rule3's with the remainder not kept; P_2 = 0 turns
the line off, and a nonzero P_2 stands at or above 24 A (the generator's unit).

### The conserved form

The read matrix 2 num p_i^2 is not symmetric where the paces differ, so
the form carries the weight 1 / p_i^2 on the Node terms and the plain
current on the Links:

  E = SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - 2 num SUM_i now_i S_6(before)_i,

S_6 the sum over the six neighbours. E is exact where the paces stand and
changes by the work term where they move; it is a GameBoard reading.
Its Link term, the plain current num (now_i before_j - before_i now_j)
through the Link ij, is the current of Rule3's own conservation law and
the one product the click reads ([the count's line](#the-counts-line)).

**Proof** at constant paces. Without the rounding the line is a_next +
a_before = **M** a_now with **M** the matrix whose diagonal is S_i / w
and whose entries on the six Links are R / w. Let **D** be the diagonal
matrix of the weights 1 / p_i^2; then **D M** is symmetric, since R_a =
2 num p_a^2 at the reading Node and the weight 1 / p_i^2 cancels it on
both sides of every Link. For a symmetric **K** = **D M** the quantity
Q(x, y) = x . **D** x + y . **D** y - x . **K** y satisfies Q(a_next,
a_now) = Q(a_now, a_before): with a_next = **M** a_now - a_before,
a_next . **D** a_next - a_next . **K** a_now = (**M** a_now - a_before)
. **D** (**M** a_now - a_before) - (**M** a_now - a_before) . **D M**
a_now = a_before . **D** a_before - a_before . **D M** a_now, which
is the other side. Multiplied by w this is E up to the Link term's
sign convention. With the rounding, each Node's remainder adds at most
one unit of the level per interval to the walk of E.
## The click

### The booking

The **current** of a record into Node i from its neighbour j through
their Link over an interval is the bilinear form of its two levels at
the two ends,

  F_ij = weight x (now_i before_j - before_i now_j),

the weight the family's num; positive inward: a
record of wave number k travelling from i to j has F_ij = -2 weight x
|psi|^2 sin omega sin k, below 0. It is antisymmetric, F_ji = -F_ij, and
it is the Link term of the conserved form of [the conserved form](#the-conserved-form): the current of
Rule3's own conservation law. The booking reads it at a Port and writes
nothing.

### The count's line

Every family of quanta carries a **count** c, the number of its quanta
at a Node, one count per family over the GameBoard; its wall is
W_c = 3 den T, T the quantum's action; its read is the current. At every Node,

  W_c c_next + r' = W_c c_now + SUM_j F_ij + r,   0 <= r' < W_c,

the sum over the six Ports of the current into the Node from its
neighbour over the interval, r the remainder kept at the Node: Rule3
with the coefficient 1 on each axis's inflow through its two Ports, W_c on
the count and the wall W_c. The **click** is the division: a quantum moves
whole from one Node to the next exactly when the remainder crosses W_c,
and never a fraction of one. **The click ends nothing** (the owner's
word of 2026-09-30): the click is the count's line's move of one whole
quantum where the remainder crosses the wall, at one Link, local; the
record goes on after it and nothing ends anywhere; the count that
arrives at a detector's Node is the detector's click, a detector's
count is a family's count at its Nodes, and a detector reports and
takes nothing: the ending of a record at a click (the absorption, a
detector that takes the quantum into its own count) is decided against
and is no hypothesis of the law; under it feeble light and a lone
quantum spread over many Nodes move no remainder over W_c and never
click, the law's claim against nature, tested by the two slits'
dilution series ([what is open](#what-is-open), item 4); a body's
quanta that leave it stay its family, messages of matter (**Light is
born by the write** below). The same line carries a body: the
count follows its record's current at every Node, one quantum at a
time, so a body moves without any accumulator of its position. A click
has a family and an axis: the family whose count moved and the Port the
quantum crossed, the axis and the side of the count's line's tally.

**Light is born by the write; no quantum changes family at a crossing** (the owner's word of 2026-09-30 on the advisor's line, #1509 comment 5902657899, replacing the giving of 2026-09-29): a body's quanta that leave it stay its family (a free quantum of matter is a message of matter) and the matter count is conserved by this line to the bit; the body's Nodes are where its family's count stands about its declared Nodes and its shell the Nodes among them with a Port to a count 0, derived when a report needs them and never kept; no ledger of bodies, no conversion at an outer Port and no scaled write. Light is the sign holder's own record: the holder of the sign is one record whose time part is its real level pair, stepped by Rule3 at the paces of its reads (the content, so light is bent) and written by the hold from the Wronskian's quanta of the families that read it by sign; a static rotating body writes a static level (its well in the sign holder) and radiates nothing; a breathing or moving body writes a varying source at its Nodes, the row carries it away at one Link per interval in the vacuum, and that wave is the light. Its count needs no lay and no conversion: every family runs the count's line on its own record, a held family's count starting at 0 everywhere where its record is 0 and moved by its currents, so its total stays 0 within the remainders' walk, quanta and holes -1 together, the line's own pair creation (a photon born with its hole). A detector is a Node declared in the file: it reports the rise of a family's count across its Nodes, the click, the one measurement; nothing is handed over, and a detector is one connected region of Nodes with one name. The three channels are the read, the write and the click as the measurement alone. The sign holder starts at its rest under the bodies' Wronskian's quanta at the written moment (the start, sources of either sign), so a static rotating body's row stands still from the first interval within the rounding.

**The remainder's origin**. The remainder at a Node starts at the
origin W_c div 2: started at 0, a Node with no quantum reads the count -1 at its first
outward swing (W_c c + r below 0), a hole the line conserves and nature
does not show at an empty Node (a body of holes is the anti-body,
[the hypotheses under their own names](#the-hypotheses-under-their-own-names)). A body's count is laid with its record: at every Node
W_c c + r is the Node's share of the record's form plus the origin, so
the count follows the norm with the margin W_c / 2 against the rounding's
walk. **The lay and the wall**: the count is laid from the weighted share, the conserved form's Node term over the Link's pace squared less the plain Link term, e_i = [w (now_i^2 + before_i^2) - S_i now_i before_i] div (2 p_i^2) - num x now_i x S_6(before)_i with p_i the Link's pace at the Node ([the conserved form](#the-conserved-form)), in the current's units: its change over one interval of Rule3 is exactly SUM_j F_ij at every Node, in the vacuum and in a well alike (the Node term changes by (next - before) R S_6(now) and R = 2 num p_i^2), so the count's line is the continuity of Rule3's conserved form everywhere. In the vacuum it is the plain share E_i / 2 = 3 den (now^2 + before^2) - num now S_6(before), whose sum over a closed GameBoard is 3 den SUM_i D_i; in a well the plain share is the local form D that sources the fields and no count, so a body in its well is lighter in every field it sources than in quanta by Gamma^2 / p_i^2 at its Nodes (714 quanta against 599 on the chain body of Gamma 6,000; **The mass defect is the form's fall at a kept count**). So the count's wall at every Node is 3 den T, T the universe's quantum action and 3 den the family's plain wall, the body's count is the sum of the counts laid at its Nodes, and a declared count is checked against the laid sum at the gate ((|c - laid| - 1) div 2)^2 <= c, as squares, refused by name beyond it. The count is laid once, at the first act, and then moves by the line's flux alone.

**The inverse** is the same line with the current reversed: W_c c_now + r =
W_c c_next + r' - SUM_j F_ij, exact, the currents read from the
interval's levels as the forward step read them. The line has no other act: a total below zero gives the count -1 with the remainder in range, the hole above, which the line conserves and fills (a lawful body's edge Links read such holes, so a guard that refused them would end every lawful run); a clamp at 0 would create quanta, and a block of a Node's currents is a branch on a Node's value that reads two Links away and loses the inverse, so neither is a rule.

**Theorem** (the count is conserved). Over any region of Nodes, SUM (W_c c_i +
r_i) changes in one interval only by the currents through the region's
boundary Links.

**Proof**. Summing the line over the region, each interior Link's current
enters one Node's right side as +F and its neighbour's as -F and
cancels; what remains is the sum over the boundary Links, a telescoping
sum, exact in integers. On a periodic GameBoard with no face the sum is
constant to the bit.

**The velocity**. The record's wave number is conserved by the record's line,
and the count's line is the continuity equation of the current in integers,
so the count's centroid moves at the current's velocity, with no leak beyond
the remainder; a body at rest has zero net current at every Node in
the mean and its count stays in place (the open point, [what is
open](#what-is-open)). On the shipped worlds: the resting Lorentz world's
body keeps its count in place under its own standing record stepped by the
loop, two hundred intervals, the swing 2 x 10^-9 of T / 2; a record of two
levels with the phase k per Link, stepped by the loop on the moving Lorentz
world's GameBoard, carries its count at Rule3's group velocity R 2 sin k /
(2 w sin omega), the count's centroid within one Node of the record's over
six hundred intervals, and the integrated inflow of a slab is the change of
the form's share there within the rounding's re-allocation of the Link
terms. Under the count's line a moving body is the moving mode of
[the generator](#the-generator) (e), its count moved by its record's current.

**The bound**. The total at a Node is at most 6 x weight x 4 A^2 + W_c (c + 1)
+ W_c: one current per Port, each the weight times the two products of two
levels at A on each of the two level pairs, the count's wall W_c (c + 1)
and the remainder below W_c. The shipped universe (A = 2^20, the weight
800) is within int64; a world declaring A beyond 2^24 at the weight
10^3 is refused by name; the generator's A ([the generator](#the-generator) (f)) is
admitted.

## The primitives
**A family's write is one act**: every write into a family's level on the GameBoard is (w x q(Node) + r) div E at a Node each interval, the division act with the remainder r carried at that Node: q(Node) the writer's own quantity there (a family of quanta's form D_i div T, its Wronskian's quanta, or its tension T_aa), w the one weight of the pair of families (whoever reads with w sources with w), E the written row's divisor (E_s, times W_c for the tension, (w x T_aa + r_aa) div (E_s W_c), one act per axis); the hold, the well and **The start** (the rest of the hold's line, its fixed point) are its instances; no number is the act's own; generic (the rows' keys), vector (one carried division), local (the Node).


Every act of the engine is a pure function of the whole GameBoard's
arrays that calls Rule3 and nothing else, in `src/event_universe/node.py`
and the modules split from it (`flow.py`, `reports.py`) and in the folders of
`src/event_universe/features/` (the count's line, the
hold, the write, the signed read, the start); the GameBoard calls them in
the interval's order ([the interval](#the-interval)). No act holds a
number, a family's name or a default. Every write is a whole integer
into a family's level; every division's remainder lives at the Node
where it divided.

| Primitive | Place | Reads | Writes | The line |
| --- | --- | --- | --- | --- |
| the signed read | (i) | the read families' time parts at the start (a row with a gap: the well it laid), the weights, by, the tensions; the reader's own sense (its q) | the paces | [the paces](#the-paces); the content as it is, no floor and no guard in the interval (the guard reads the initial state at load) |
| the operation | (ii) | the coefficients from the pair and the paces; a holder of the content's parts at the pace 1 | every family of quanta's two level pairs (the holder of the sign's time part among them), every held family's parts | Rule3's line itself |
| the count's line | (iii) | the family's two level pairs at the Node and across its six Ports as the step produced them, the neighbours' differences through the Ports, W_c, the weight num, the Nodes declared to report | the family's count at a Node, its remainder; its sense and the sense's remainder (the sense's line, the Wronskian's current); the tension T_aa booked per axis for the hold | [the count's line](#the-counts-line): the count is the family's, one count per family over the GameBoard, laid once at the first act from the weighted share of the family's two level pairs and moved by the line alone; a held family's count starts at 0 where its record is 0 and moves by its line, quanta and holes together (**Light is born by the write**); a body's quanta of another family are that family's count at its Nodes; a detector, a Node declared in the file, reports the rise of the count summed over its Nodes, the net inflow across its boundary, the click, and nothing is handed over |
| the hold | (iv) | every family of quanta that reads the row: its well D_i div T at the Node this interval (by sign its Wronskian's quanta W_i div T), its tension T_aa on each axis; the weight it sources with; the row's divisor E_s; W_c | the held family's parts at every Node; their carries per part, axis and sourcing family at the Node (four per sourcing family at most) | in the count's words, at every Node each interval: the time part gains (w x n_i + r) div E_s, n_i the well of the sourcing family; the tension on the axis a gains (w x T_aa + r_aa) div (E_s W_c) in one act, **The tension** below, at the one wall for every part, no count in the divisor and no branch, so the inverse is exact; every family of quanta sources the rows it reads at the weight it reads with (whoever reads with w sources with w); a row with a gap is not stepped: its time part is the well laid each interval, (w x n_i + r) div E_s with its own remainder, the level before kept beside it (so its inverse is exact over one interval, and over more where its level stands still); so that two bodies' wells add, the field's rest is Poisson's with the sources, and the well moves with the record (**The well of a body with a record is its record's form**: the self-force vanishes, action and reaction); the parts are one source at one scale with no factor of the files |
| the feed | none | **Derived**, no primitive: the body's record in the pace gradient | the body's momentum **n** as a reading | a body has no law of motion of its own: its record moves by Rule3 alone, and in a pace gradient its packet accelerates at a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D (Delta the mode's top velocity, the second derivative of its band in k; d omega_0 / d c the mode's redshift per level; c_+ and c_- the read level at its two faces D Links apart), the count follows the record by the count's line, and its momentum **n** is the reading of its record's current (SUM over its Links of F_ij at the norm T: the count's line's velocity times 3 Q_unit M); no coefficient is declared; bodies with the same Delta x d omega_0 / d c fall alike, and two light bodies in one tent read it |

**The tension** (the advisor's derivation, #1509 comment 5903245927, the owner's word of 2026-09-30 on its diagonal): the momentum density along the axis a at the Node i is the count's line's current per axis, P_a(i) = (F_(i,i+a) - F_(i,i-a)) / num, and Rule3's line gives exactly, at constant paces,

  w [P_a(t + 1) - P_a(t)] = SUM_b R_b [G_ab(i - b) - G_ab(i)],  G_ab(i) = now_i (now_(i+a+b) - now_(i-a+b)) - now_(i+b) (now_(i+a) - now_(i-a)),

G_ab(i) the flux of the a-momentum through the b-Link (i, i + b) at one time, the levels now alone (**Proof**: substitute w now' = SUM_b R_b (now_(i+b) + now_(i-b)) + S now_i - w before_i into w P_a(t + 1); the S term cancels, the w term is w P_a(t), and the R term is the difference of the fluxes); so the stress on the Link is num G_ab, the second booking of the conserved form (its Link term shifted by one Link), and the tension on the axis a at the Node, the part Rule3 reads into the Link's pace, is the mean over its two a-Links, T_aa(i) = num (G_aa(i) + G_aa(i - a)) div 2 with G_aa(i) = now_i (now_(i+2a) - now_i) - now_(i+a) (now_(i+a) - now_(i-a)), the neighbour's own difference brought through the Port and no other shift: the tension on a Link is the booking of its two ends' own readings, a level and a difference each, and a Node sources its tensions with half of each of its Links, as F combines the two ends' (now, before) and the reach of two Links is two one-Link reads composed (the advisor, #1509 comment 5903471455); with the rounding the identity holds up to the remainders' term, - r'_i D_a now_i + now_i (r'_(i+a) - r'_(i-a)), exactly. It is read and never written, quadratic in the amplitude as the count is: a plane wave of the amplitude b at the wave number k has G_ab = -2 b^2 sin k_a sin k_b, a uniform record 0, and a standing body's tail a tension that does not vanish in the mean; for a packet of count c and velocity v it is c v_a v_b within the rounding, the dust's stress with no count in the divisor and nothing undefined at 0; the off-diagonal parts and the vector part, which Rule3 never reads, are not written (**The final unification**).

The hop is retired: the count's line moves the count with its record's
current, and no accumulator of a body's position remains. The click is one mechanism: the count's line carries every family's quanta, and a Node declared to report reads each quantum that arrives whole.

A body's writes into the held rows are its family's (the hold's row): at every Node its family's well sources the time part and its tension the tension, at the weight its family sources the row with, and its Wronskian the holder of the sign's time part; the momentum n = 3 Q j div T and the wall W = 3 Q M are readings of that current and count, and the dipoles of a spin and a moment are no write of the engine.
## The stable body

### What a body is

A body is its count and its record over its Nodes, and never one Node: every body is many Nodes, and nothing gathers it (the owner's word of 2026-09-28). The count c_i is its family's count at the body's Nodes, in quanta; it enters Rule3 through the pace alone, p_i = Gamma - the held level at the Node (the source's rest: the body's own count and its neighbours' over the divisor), and it never splits: a quantum moves whole, by the count's line. The record (now, before) of the body's family splits by the send and is bound by the wells its counts source.

**A pixel** (the advisor's sentence, accepted by the owner, 2026-09-30): A pixel is a bound body: a standing record above the top of its family's band in the wells its own form lays, its count the sum over its Nodes, at one Node near the horizon and over its tail below it; a cluster is pixels within tail reach that click at one another; the generator lays a pixel as its standing mode, the Node and its tail, at a count.

**The four lines of the body** (the owner's word, in the law's words): (a) **The body is the fixed point of its binding row**: a body is its quanta over its Nodes; its form (the vacuum's share of its levels at the written moment, the form that sources the fields) sources every held row its family sources, at the row's divisor; its record is the standing record Rule3 makes in those paces; its count is the weighted share that record lays (**The lay and the wall**); it stands where the sources return themselves; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace reaching 0).

(b) **The form sources the fields**: a held row's level is the rest **The start** solves from the bodies' forms at the row's divisor, then Rule3 steps it; every divisor is 1 (**The rule's own universe**); a well has the reach of its pair, the gapped pair's 1 / kappa and the vacuum's none.

(c) **The count moves by the count's line alone**: the count is laid once, at the first act, from the record's form ([the count's line](#the-counts-line), **The lay and the wall**), and after it no count is laid from the form: the count at a Node changes only by the line's flux, and the total is conserved; the well, D_i div T each interval, is the record's quanta as the fields' source and no count. A body's Nodes are the Nodes where its family's count stands about its declared Nodes, and its shell the Nodes among them with a Port to a count 0, both derived when a report needs them and never kept; its quanta that leave it stay its family, messages of matter, and no ledger follows them (**Light is born by the write**).

(d) **The fall**: a = Delta |d omega_b / dc| grad c, Delta the band's curvature at k = 0, d omega_b / dc from Rule3's coefficients at the body's pace and rotation, grad c the other body's content, one line for every held row the body sources. Which fixed point stands is [the stable body theorem](#the-functional-and-the-dilation). The world file names the body's family, its Nodes with their counts and the quanta of other families it holds, and nothing else: no momentum, no spin, no emitter (a body radiates by its write), no sign (a body's sense is its record's), no lowered pair on its Nodes, no seed, no stop, no closed Port, no period (P_body is its mode's rotation); its two levels are the generator's mode file beside the world.

### The well

At a Node whose held level is c Rule3's one-Node rotation rises from cos omega_0 = num / den by (1 - p^2 / Gamma^2)(den - num) / den, and its bonds fall from num / (3 den) to num p_i p_j / (3 den Gamma^2): the symmetric form of the line with the weights 1 / p_i. The depth is bounded by the family's own 1 - cos omega_0, so a family whose pair lies close to 1 binds nothing: on [800, 809] (1 - cos omega_0 = 0.011) no cube of any side at any count is bound; on [800, 1200] (1 / 3) at Gamma = 10^4 a cube of side 12 is bound from the level 500 at its Nodes (the mode's share inside 0.79, 0.92 at 1000, 0.997 at 5000), of side 6 from 1000, of side 3 at 3000, one Node at 5000; omega_b / omega_0 for side 12 is 0.832 at 500 and 0.771 at 2000. A body's clock is set by the level at its Nodes and its side, from the rule: a body's mass is its count.

**The reach of a held family is its pair**: under the hold as a sum a held family's rest solves num Delta^2 a - 6 (den - num) a = -3 den sigma (its line a_next = num S_6(a_now) div (3 den) - a_before with the source once an interval, Delta^2 the six-neighbour second difference), so outside a body its rest falls by e^(-kappa) per Link with cosh kappa = 3 den / num - 2, the family's own band at zero rotation (cos omega = (num / (3 den)) (2 + cos k) at omega = 0, the evanescent k; kappa^2 = 6 den / num - 6 to the second order, the static limit of the source's row), the same pair that sets the band of its records and de Broglie's k for them ((j)): the gap is the mass of the records and the inverse reach of the field, one number; [1, 1] has no gap (2 cos omega = 2 at k = 0) and its rest is Poisson's over the whole GameBoard, the pull between bodies (Newton's tent, (i)); a pair with den > num has the gap 2 cos omega = 2 num / den at k = 0 and inside a thick body its rest stands at 3 den sigma / (num kappa^2) (Delta^2 the six-neighbour second difference, kappa^2 its value on e^(-kappa r)), so at [1, 2] with the divisor 1 the level inside a body is its count and falls by e^(-kappa) = 0.127 per Link outside (cosh kappa = 4): a body's well is the static field of every family it holds, read at its Nodes by the paces, and a body's binding is the contact well of the bound charge [1, 2] (the well laid, the count itself, **The vacuum's row steps at the divisor 1**) and the 1 / r field of the vacuum's row together, the pull between bodies the vacuum's row's, and a mirror's line c > Gamma (1 - sin(k / 2)) and a window are read by light from both; generic (a row's pair and divisor, no name), vector (the line's own static limit, no root), local (the six reads and the source at the Node).

### The functional and the dilation

**The functional**. Let a body of M quanta have the record phi over its region, SUM phi_i^2 = 1, its counts the form c_i = M phi_i^2, and let every held row r it sources be a hollow (sigma_r = +1) or a hill (sigma_r = -1) with the static kernel G_r of its line ((Delta^2 - kappa_r^2) a = -3 den sigma / num, [the well](#the-well); kappa = 0 for the massless row) and the divisor E_r, so the well at a Node is Phi_i = SUM_r sigma_r (M / E_r) SUM_j G_r,ij phi_j^2. To first order in Phi / Gamma the well line raises the one-Node rotation 2 cos omega by 4 g Phi / Gamma (cos omega by g (1 - p^2 / Gamma^2)), g = (den - num) / den, and the bonds' fall under the pace is of the pressure's own order and drops out at a width beyond the Link; there the fixed point of the binding row is a critical point on the sphere SUM phi_i^2 = 1 of

  F[phi] = (num / (3 den)) SUM over Links (phi_i - phi_j)^2 - (2 g / Gamma) SUM_r sigma_r (M / E_r) SUM_ij phi_i^2 G_r,ij phi_j^2,

the band's pressure less the wells' energy, each well counted once for the record being its own source (Hartree's form). **Proof**. The record is the top mode of Rule3's symmetric form at the paces, at first order **M**(Phi) = **M**_0 + (4 g / Gamma) diag(Phi), so it solves **M**(Phi[phi^2]) phi = 2 cos omega_b phi. The derivative of the wells' term at phi_j is 2 (4 g / Gamma) Phi_j phi_j, phi_j entering twice with G_r symmetric; the pressure's is 2 (2 cos omega_0 - **M**_0 phi)_j; so dF / dphi = -2 (**M**(Phi) phi - 2 cos omega_0 phi), and dF / dphi = 2 lambda phi on the sphere is the fixed point's own equation with 2 cos omega_b = 2 cos omega_0 - lambda, and conversely. **The dilation**. Let phi_R(x) = R^(-d / 2) phi(x / R) be the body dilated, d the GameBoard's dimension and R beyond the Link. The pressure is K / R^2 and each row's well energy W_r / R^(s_r), with s_r the row's scaling power at the body's size: s_r = d beyond the row's reach (the kernel a contact of weight 3 den_r / (6 (den_r - num_r)) per unit source, the rest inside a thick body), s_r = d - 2 within the reach or for the massless row (Poisson's 3 / (4 pi r) in a box; on a plane the logarithm, s = 0 in the sense of the limit, whose energy grows as 2 W per unit of ln R; on a chain the linear well, s = -1).

**Theorem** (the stable body). At a fixed point of the binding row of width R the virial 2 K = SUM_r sigma_r s_r W_r holds, and the second variation of F along the dilation is R^2 F''(R) = SUM_r sigma_r s_r (2 - s_r) W_r. A body is stable only where this sum is positive; it is a minimum of F where further the Hessian on the modes orthogonal to the dilation and the translations is positive.

**Proof**. F(R) = K / R^2 - SUM_r sigma_r W_r R^(-s_r); F'(1) = 0 is -2 K + SUM_r sigma_r s_r W_r = 0; F''(1) = 6 K - SUM_r sigma_r s_r (s_r + 1) W_r = SUM_r sigma_r (3 s_r - s_r^2 - s_r) W_r. Derrick's scaling, Pohozaev's identity on the GameBoard; at another R the same with W_r read there. **The signs**. s (2 - s) is +1 at s = 1, 0 at s = 2, -3 at s = 3: a hollow holds the body where its well falls slower than the pressure (s < 2) and breaks it where it falls faster (s > 2), and a hill does the opposite. From them, on the rows the law holds:

(a) **The hollow's dimension**. One hollow beyond its reach: on a chain (s = 1) every mass binds, at the width R = 2 K / W, falling as 1 / M; on a plane (s = 2) the dilation is flat and the well within the reach (the logarithm, +2 W) decides: above the mass at which the well's coefficient passes the pressure's the body stands at the reach's size, a window; in a box (s = 3) the one critical point is a maximum along the dilation, a saddle for every mass: the body disperses beyond it and collapses within it. The three GameBoards of the generator read so: on a chain of 60 Nodes 200 to 1,000 quanta stand, on a plane of 40 x 40 x 1 3,000 to 8,000, on a box of 48 x 24 x 24 29,500 to 30,000 alone, at the band's edge.

(b) **The massless row holds the body**. Gravity's Poisson well in a box has s = 1: with the pressure alone F = a / R^2 - c / R has the one critical point R = 2 a / c, a minimum for every mass (Pekar's body), its width falling as E_g / M. Beside it a hollow beyond its reach (s = 3) adds a barrier: on a Gaussian body F = a / R^2 - b / R^3 - c / R with a = num / (2 den), b = (2 g / Gamma) (M / E_b) (3 den_b / (6 (den_b - num_b))) / (2 pi)^(3 / 2) and c = (2 g / Gamma) (M / E_g) (3 / (4 pi)) sqrt(2 / pi); the critical points R = (a +- sqrt(a^2 - 3 b c)) / c, the wide one the minimum and the narrow one the saddle, the barrier to the collapse; none where 3 b c > a^2, the collapse. The minimum is a minimum exactly where W_g > 3 W_b there, R^2 > 3 (den_b / num_b) (E_g / E_b) / kappa_b^2, and the largest mass with a minimum is M_max = a sqrt(E_b E_g) / sqrt(3 b_1 c_1), b_1 and c_1 the coefficients at M / E = 1.

**Computed** (the script beside the paper): on the matter pair [4000, 6000] with the binding row [5760, 6000] (reach 2.02 Links) and gravity [1, 1] at Gamma = 6,000, M_max = 4,450 sqrt(E_b E_g); at the divisors 2 and 10 M_max is 19,900, 20,000 quanta stand at the edge (a^2 = 3 b c, the minimum and the barrier meeting at 8 Links) and 30,000 have no critical point at first order: the fixed point the generator reaches at 29,500 to 30,000 is the saturated saddle of the scaling's check (the width one Link, the well at the horizon's edge, (c)), and 32,000 and above collapse; at the binding's divisor 50, M_max is 99,600, the minimum for 30,000 lies at 10.3 Links and its barrier at 0.24, under the Link: gravity's body alone (10.5 Links at 30,000, 5.2 at 60,000), the widths the scaling's scan with the saturation reads as 11 and 4.8, and its collapse from 100,000. On the GameBoard the two kernels' constants at the widths 3 to 6 are 0.51 to 0.78 of the contact's and 0.92 to 0.84 of Poisson's, the reach's crossover and the box; the exponents are the theorem's.

(c) **The horizon ends a collapse**. Beyond first order the well line saturates (the rotation's gain 2 g (1 - (1 - Phi / Gamma)^2) is bounded by 2 g) and the Link's pace weakens the pressure by (1 - 2 Phi / Gamma)^2; neither makes a minimum, since both vanish together at the pace's floor: the collapse ends where a Link's pace reaches 0, Phi = Gamma / 2 on the Link, a frozen cluster of horizon Nodes, the guard's floor and no body of ordinary matter. (d) **The hill**. A hill beyond its own reach adds +3 W_h in a box: a hill whose reach is shorter than the body turns the saddle into a minimum where 3 W_h > 3 W_b - W_g; within its reach a hill is Coulomb-like and adds -W_h, so a hill longer than the body disperses it. **The hill holds the body**, a hypothesis under its own name: a body stands as a stable extended fixed point where a held row read with the opposite sign (by q, like signs), of reach shorter than the hollow's, is held beside the hollow: below the hill's reach both are Coulomb-like and the hill, with the smaller divisor, forbids the collapse; between the two reaches the hollow binds; the body's size lies between the reaches. The rows the law holds for it: the polarisation [1, 2] read by q (1 / kappa = 0.49 Links, a hard core of one Link), the binding row (the hollow of reach two Links), gravity (the pull). A run of the generator with the third row decides it; it enters the universe's files by the owner's word alone.

(e) **The cooling**, a hypothesis under its own name (the owner's word of 2026-09-29, 04:40 Israel, under the write of 2026-09-30): a body above its minimum sheds its excess as quanta of its own family, messages of matter moved by the count's line at the universe's one T, its count falling by one per quantum shed, and radiates light by its write while it breathes (**The photon channel is the write**); the shedding lasts while the body's rotation lies above the rotation of the stable body theorem's minimum for its count and stops there, so a cold body is a body that has finished shedding and sits at the minimum, and matter stays matter: no quantum is made or lost, the total over the families changes only by the flux through the faces, and the quantum moves whole. The engine sheds by the count's line alone: a body laid off its minimum sheds while its current crosses its outer Ports; whether it settles at the minimum is a run's finding.

**The photon channel is the write** (the owner's word of 2026-09-30, replacing the giving of 2026-09-29): a body radiates by its write into the holder of the sign its family reads, the Wronskian's quanta of its rotating record, varying as it breathes or moves; a real body (no sense) writes nothing into it and radiates no light, and every body's own quanta leave it by the line as messages of its family.

**What is missing** for the theorem to close (**Derived**): (i) the Hessian on the modes orthogonal to the dilation and the translations: for the massless row alone it is positive at the ground state (the non-degeneracy of Choquard's ground state, a theorem of the continuum), for a set of rows it is read from the run; (ii) the functional beyond first order: the fixed point sources its wells from the form phi^2 while the bonds' weakening under the pace would need the sourcing from the Link's own form, so beyond first order there is no exact functional and the stability is the count's line's own dynamics; (iii) the finite GameBoard: Poisson's rest measured from the faces' zero sets a cloud threshold (30,000 on a box of 64^3 at the divisor 10), and a minimum wider than the GameBoard is no body of that GameBoard.

### The surplus leaves

**The free part**. At a Node of a body's record the local rotation is read from its three levels by the read act, 2 cos omega_i = (next_i + before_i) / now_i, and the local band from the Node's paces, its top (S_i + 2 SUM_a R_a,i) / w; in integers the Node is bound where now_i (next_i + before_i) w > now_i^2 (S_i + 2 SUM_a R_a,i) and free otherwise, from the Node and its six neighbours alone, no division. At a fixed point of the binding row every Node is bound (2 cos omega_b above the band's top at every Node, the mode's own relation); a cloud not at its fixed point has a free part, the Nodes whose rotation lies in the band, and the free part is a free record: it leaves at its band's group velocity by Rule3 as it stands, the count's line carries its quanta with it, and they end at a face or in another body (a cloud evaporates). A family sheds at its own band's group velocity, so a family whose pair lies near the exact band (m near 1: the bonds 2 m p^2 near 0) sheds nothing.

**The bound surplus does not leave by itself**: the part of a cloud's surplus held in its bound modes stays, since a bound mode is stationary and Rule3 reversible; a cloud twice too wide in a static well breathes about its minimum for 6,000 intervals with no settling, on a chain with open faces as on a closed one (**Computed**, the script beside the paper: the width swinging between 2.1 and 3.4 Links about the mode's 2.4, the form inside the body kept), so evaporation sheds the free part alone, and a body settles by the cooling of [the functional and the dilation](#the-functional-and-the-dilation) (e) alone.

**The held rows radiate**: a body whose form changes in time changes the source of every held row it sources, the row's record steps by Rule3 from that source, and the massless row's waves leave through the open faces at one Link per interval; a settled body sources a rest and radiates nothing.

**The mass defect is the form's fall at a kept count**. The line a_next = **M**(t) a_now - a_before with the paces changing in time changes the total form D = |a_now|^2 - <a_next, a_before> by exactly D(t + 1) - D(t) = <a_next, (**M**(t) - **M**(t + 1)) a_now> (**Theorem**, from the line by substitution; the identity holds to 10^-15 in the check), 0 at fixed paces (the conserved form) and negative where a well deepens, while the count's line, moved by the flux alone, keeps T c + r (**Computed**: a standing mode in a well deepening from 300 to 600 at Gamma = 6,000 loses 4.0 percent of its form with its count kept and the adiabatic invariant A^2 sin omega_b kept to 10^-5): the count is the quanta and the form sources the fields, so a body that binds is lighter in every field it sources by its binding and no lighter in quanta: gravity's source is the well and the count is the baryon number, with the inertia's caveat (**The mass is the well, the count the baryon number**).

**The cooling's local trigger is the count's line's own current**: the form's flux through a body's edge Port, the current the count's line reads, is 0 at every interval for a standing mode and swings for a cloud at the beat of its bound modes, the difference of their rotations (**Computed**: at the edge Node the form's standard deviation over 3,000 intervals is 0 for the mode and 0.0065 against its mean 0.011 for the cloud twice too wide), so a cloud's quanta leave across the edge at the beat as messages of its family and none leave at the fixed point without any knowledge of the minimum: "the shedding stops there" is the current's own zero, local.

**The number of quanta a cloud gives to settle** (**Derived**, a blind expectation for the run of (e)): the law keeps the count and not an energy, so the quanta shed are the part of the cloud outside the ground mode of the well its final count makes, the rest staying as the body; for a Gaussian cloud twice too wide in its own massless well (the final width falling as 1 / M') the fraction f that stays solves f = (4 f / (1 + 4 f^2))^d: 13 percent leave on a chain, 20 on a plane, 23 in a box, each quantum carrying the body's rotation; the brackets: at most 1 - (4 / 5)^d for a fixed well (20, 36 and 49 percent), at least the energy's account M c^2 / (4 a) / (2 sin omega_b omega_b) of (b), 76 quanta of 30,000 under gravity at the divisor 10, a quarter of a percent; the far detector's clicks of the body's family count them and the body's count falls by the same; a family that sheds nothing (a flat band) stays a cloud, dark.

### The generator

The generator builds every world from zero; it declares nothing and
holds no float.

(a) **The input and the region**. The input is a world file in the law's
form: the GameBoard, the Node clock, the universe file it names and one
body by its Nodes with their counts; nothing on the command line. The
iteration runs on the body's Nodes and their surroundings, out to where
the mode's tail falls below one unit; the count stays on the body's Nodes.

(b) **The iteration**. Rule3's read act with the before-coefficient 0, a <-
(SUM_a R_a arr_a + S a) div w on the region, run at the amplitude 2^16 and
scaled to the amplitude unit A by the division act at the end alone (the
level times A over its largest size): the power iteration of the symmetric
form's top mode (the bound mode, above the band, the eigenvalue largest in size), at cos omega_0 / cos omega_b per step; the read act at a small amplitude zeroes the tail's levels of 1 and 2 and stops on a mode half as wide (**Computed**, 600 quanta on a chain: [106, 91, 63, 35, 14, 2, 0] against the mode's [106, 105, 85, 62, 44, 30, 20, 13, 9, 6, 4, 2.5, 1.6]), so the region grows until its outer envelope is 0 and nothing inside it is purged.

(c) **The stop from the integers, the standing read**. The profile is an integer vector bounded by A, so the iteration is a map on a finite set and enters a cycle; the stop is the first repeat, exact, no tolerance and no declared count, the profile there the mode within one unit of A. A record stands when between two whole cycles of its rotation (P_body intervals) the form D_i = now_i^2 - next_i before_i returns to itself at every Node of its region within one quantum, |D_i(t + P_body) - D_i(t)| < T (the form is the count's shadow: a form that drifts by T over a cycle moves a quantum, and a standing record moves none); the region is every Node whose form is at least a hundredth of a quantum, T div 100, the mode's tail falling by e^(-2 kappa) per Link in the form with cosh kappa = (3 den / num) cos omega_b - 2 on a chain and by the support function of [the shape] in a box, and nothing inside the region is purged; a reading of the centre alone is a reading and no stop, and a record whose form drifts by T or more at any Node of its region is a packet and no mode.

**The quantum's action sets the resolution**: one rounding of a level at the amplitude A moves 2 A / T of a quantum of form, so at T = 64 no record of 600 quanta stands at any amplitude (the rounding a third of a quantum in the tail per interval; the reader refuses and the engine spreads the count from the width 4 to 26), while from T = 4,096 the same record stands (599 of 600 quanta carried on 19 Nodes, held 1,000 intervals by the engine, the count's width 2.7 to 3.2 as laid, 0 to 6 quanta beyond the set): the universe's T for worlds of bodies is the owner's, the shipped worlds keep 64 bit for bit.

(d) **The two levels and the amplitude from the count**. The mode's second
level is the read act once more, halved (**M** phi = 2 cos omega_b
phi); the two levels are scaled together
so that the weighted share the record lays over its region carries c,
the body's count (**The lay and the wall**), its sources the vacuum's
share at the written moment: its amplitude follows, and no bound on a
level is written (a level beyond the integer width is the engine's
refusal); a body laid with a sense carries its second level pair, the
sense times the record a quarter period on, the two scaled by one factor
so their plain form is the record's own (**The sign is the rotation sense**).

(e) **The moving body**. The momentum **n** is a reading of the record's current, **v** =
**n** / W the packet's velocity. The moving body is the resting envelope with the phase k per
Link along the axis of motion, the rotation act on its two levels by the
triple of the pair (m, j), cos k = (m^2 - j^2) / (m^2 + j^2), exact; k is
the pair at which the packet's own current along the axis, SUM over its
Links of F_ij = now_i before_j - before_i now_j at the norm T (M quanta),
equals T n / (3 Q_unit), the count's line's velocity of the packet, M
cancelling: by bisection on j at the declared m (the body's `momentum` n and its `phase_denominator` m are its numbers in the world file, k is derived).
The read with the arrivals along the axis turned by +k and -k on a fixed
well is a gauge of the plain read: its fixed point is the rest mode, its
current 0 and its rotation the rest's at every k; the packet is stationary
in the body's frame only where the count's line moves the well at **v**; the
loader's proper pair of a moving body is the packet's rotation at its centre.
Generic: one primitive, the family's pair and the body's two numbers; vector: the rotation act, a booking, the division act, no root; local: each Node's six Links.

(f) **The amplitude unit A is derived, never written**: the largest amplitude at
which Rule3's total stays inside the integer width at every content of the
region, the bound of [the bound](#the-bound) solved for the amplitude, A =
(2^63 - 1 - w) div (6 R + |S| + w) at the content whose coefficients are
largest (between 2^22 and 2^23 in the cases of (c)). The fixed point does
not depend on A beyond its resolution: at A / 2 the profile agrees with the
one at A, rescaled, within 12 units of the coarser, and the rotation to
10^-6; the final scale comes from the count.

(g) **The field at rest, the start of a world**. The generator iterates the held family's own
line to rest first, at the pair of the family's row, as the hold's source makes it: the
body's form (the vacuum's share of its levels) over the divisor E_s added at the body's Nodes each pass, the homogeneous line
outside. From nothing the level at every Node is num S_6(a) div (6 den), plus half the
source at the body's Nodes (6 den a = num S_6(a) + 3 den sigma, sigma = w M div E_s: the
source enters once an interval at one level), by the division act on a fine unit derived
from the width; the levels go to a fixed point, its first repeat, for sources of either sign or both wherever the board has a sink (the owner and the advisor, 2026-09-30: the tension's source is of both signs about a body, and so are the senses');
the levels are Poisson's rest with the sources within one unit, and the mode is solved on
that content: generic (one primitive, the row's pair and divisor, no family name), vector
(the division act alone, no root, no float) and local (the six reads and the source's load).
A world starts from the field at rest, never from zeros, whose transient rings. Under [1, 1]
between periodic faces the sources have no rest (the periodic Poisson problem at kappa = 0),
and the world is refused by name; between open faces the harmonic well of the sources.

**The start**. The loop writes every held family at the load at its rest, by
one folder found by its name, once before the first interval and never in
it, the level and its remainder together (the fixed point of the division act is a pair: with the rounded rest a and its line's residual rho = num SUM_6 a - 6 den a, the remainder r_0 is one from which the first step returns a, any r_0 with 0 <= rho + r_0 < w, the half wall the division's unbiased origin for every Node whose |rho| is below it, and the hold's carries E_s div 2 at the sources' Nodes so the source's current is even from the first interval; a remainder 0 by fiat is no rest, the first step kicks every Node whose rho is negative, Newton's reading of 2026-09-28). The rest is (g)'s iteration and nothing else, on a chain and a box alike and in the generator as in the engine: the division act from nothing until the levels repeat, the levels the fine levels' nearest integers by the division act. Generic (the row's pair and divisor), vector (the division act alone), local (the six reads and the source); the cost is the iteration's, about the square of the board's extent for the massless row.

### The velocity

Rule3 is translation-invariant, so the record's wave number k is conserved
where no pace gradient stands: the record's centre moves at its group
velocity v_g(k) exactly, bound or spreading. The count follows the record by
the count's line: with the record's norm c T the current across the body's
face is c T v_g per interval, so c v_g quanta cross per interval and the
count's centroid moves at v_g, exact up to the remainder. The well moves
with the count one quantum at a time, 1 / c_i of a Link, so the record is
never kicked by a whole Link; the leak of a hop of the whole well by one
Link, delta = 1 - <phi | X phi>^2 with X the shift by one Link, is 0.031 at
side 12 and 1000 per Node (0.021 at 500, 0.040 at 2000; 0.099 at side 6 and
2000; 0.38 at side 3 and 5000; 0.999 at one Node and 9000), and per Link of
travel delta / c = 3 x 10^-5 at side 12 and 1000: the bound norm, and with
it the velocity, falls by 3 x 10^-5 per Link there. A one-Node body of one
quantum binds nothing and is a free record: its velocity is v_g(k) with no
count to follow it.

The run beside these numbers (the cube of side 12 on [800, 1200] at 1000 per
Node at v = 1 / 3 on a periodic box, 10^4 intervals): the count's centroid
against v t, the slope v within the remainder; the share inside the cube
0.92 at the start, falling by at most 3 x 10^-5 per Link; the clock's period
2 pi / omega_b(k), 7.74 intervals at k = 0. A larger fall, or a slope that
drifts, names a missing law; the body's own numbers are never patched.

## What the law says of nature

### The reading

**One sentence** (the owner's word, 2026-09-29): the universe is counts of clicks at Nodes, moved by Rule3 through the records' currents, and a body is a place where the record's form lowers the pace until its clicks cannot leave.

**One thing, two faces.** Outside, the count; inside, the form. The count at a Node is the number of clicks that came to rest there, and it is all the Outside sees. The form D div T of the record is what slows the clock inside, and nobody measures it. The count's line ties the two: its sum is the flux of the form, so the two agree on average and differ by a remainder. Matter and light are one thing in two states: matter is clicks at rest, light is clicks on their way; the band with a gap (m under Gamma) is where rest is allowed, and [1, 1] without a gap is not, and that is all the families say. A body, an atom, a star are readings: a world file holds counts and records, and who is bound to whom is read from the nesting of the levels at the Nodes, never declared.

**What a body does, in the words of the clicks.** Under the edge the wave does not hold its clicks and they scatter as messages. In the window it holds them: a discrete breathing of Rule3's focusing non-linearity. In the lower half the body is a blot of a few Links moving as a soliton and the count follows it; "the fall is the bias of the clicks" describes it exactly. Near the horizon the hop to the neighbours vanishes as (1 - 2 c / Gamma)^2: the clicks are locked and the Node indifferent. Two bodies within tail range: the smaller's wave is nearer the band, more coupled to the messages, and its clicks migrate to the larger at second order or by the messages (**The click joins and parts**); the universe flows toward frozen bodies at the horizon. All of it consequences of the rule, with no correction in them.

**The fork, decided** (the owner's word of 2026-09-29, the advisor's advice): gravity is one field that is not a click, the row [1, 1] holding the content, stepped as Rule3's wave at the pace 1 at the divisor 1, the universe's own (**The rule's own universe**, no free number): it gives 1 / r, orbits and retardation at one Link per interval and keeps the exact inverse. Le Sage's shadow, gravity as clicks of an isotropic bath of light that opaque bodies absorb, is refused: a moving body meets more of the bath ahead (the drag, orbits decaying in about 1 / v orbits) and the absorbers grow. A third way, the massless row's level as a count of resting clicks laid from the bodies' counts by the start's own act each interval, is named as a hypothesis under its own name and not the law: a relaxation has no exact inverse and relaxing to the fixed point within an interval is action at a distance, so it trades the inverse or the causality for a level never below zero.

**What is checked first.** Two looks already named: a body in a tent (the fall, (i)) and two bodies within tail range (the join of clusters); before them one computation, the edge 0.2255 recomputed for a smeared well, since the tail's Nodes have a well of their own. If both looks come out, the algebra of clusters is a right reading of Rule3, and its one line that does not click is gravity's (**The fork, decided**).

### The hypotheses under their own names

Every hypothesis stands outside the law under its own name until it passes the three tests or the owner admits it; each line says what would decide it.

**The anti-body is the count's sign reversed** (a hypothesis, the advisor's line of 2026-09-30): the anti-body of any body is the same record with its count's sign reversed, a body of holes, which the count's line makes and conserves (pair creation the line's own act at an empty Node); a neutron and an antineutron are both real records (W = 0) and differ by the sign of their count, an antiproton holes with the opposite sense, and the baryon number is the count's sign. Decided by a lay of a body of holes and its clicks, a detector reading the fall of its family's count, against nature's antineutron, distinct from the neutron.

**The electron is one quantum** (a hypothesis): the electron is one quantum of the matter family with the sense -1, a message and no pixel, with no band of its own (**The electron needs no band of its own**); its well equals its count, a plane wave at k = 0 carrying per Node the count b^2 (1 - (num / den) cos omega_0) / T and the well b^2 sin^2 omega_0 / T, equal at cos omega_0 = num / den; the positron is the same quantum in the sense +1. Decided by the mass ratio's road to Gamma ([the rows against nature](#the-rows-against-nature) (t)) and, against nature, by the lone quantum's detection under the two slits' dilution series ([what is open](#what-is-open), item 4).

**The proton is the horizon body** (a hypothesis, the advisor's line): the pixel whose count stands at the horizon of its window, the endpoint of accretion: a body takes the quanta that fall into its well and grows until the horizon closes its Links (R_a = 0 at the Node, the currents through its Ports averaging to 0), so every count between the edge and the horizon is a body still growing or still dying, and the horizon body's well is about 0.36 Gamma ((u)). Which body is the proton is computed, not chosen (the owner's word of 2026-09-30): the body where the well and the inertia agree, the advisor's inertia along the branch deciding it, with a run of bodies inside the window drifting to one count and the selection line, which fixed point stands ([what is open](#what-is-open), item 2), beside it; the number it gives is Gamma about 5,150 with the horizon body against about 6,200 with the edge body ((t)).

The hypotheses the law keeps by name elsewhere in this document: **The conversion** (the weak force), **Gamma is not constant**, **The three distances are the rule's**, **The hill holds the body**, **The cooling**, the third way of gravity (**The fork, decided**), a controlled phase of order one ((k)) and **A cross-axis read or a current's read** ([what is open](#what-is-open), item 15).

### The postulates

1. The world is Nodes and Events. Space is the GameBoard; an Event is a wall
crossed by a remainder at a Node: a level stepped, a count moved, a click;
nothing else happens. 2. A Node holds bounded local information: its
NodeState, fixed in size, read from itself and its six neighbours; no read
beyond them, no list that grows with the world, nothing of the past kept.
Every physical update uses its own record and the six causally available
neighbours with fixed work and storage for a fixed set of families
(LOCALITY-1); a self-field estimated or subtracted from anything global is
forbidden, whatever the size of its final answer. 3. Consistency is local
and causal: an Event first changes its own Node and travels Link by Link,
one Link per interval, each Node updating on receipt under the same rule;
there is no exception, and no quantum changes family at a crossing.
4. The causal speed is one Link per interval, built in; every
other speed is a rational, a count of Links over a count of intervals. 5.
Every physical calculation is on bounded integers; there is no float, no
root and no draw in the law; a Node keeps only the law's own numbers: each
record's level pairs and their remainders (a family of quanta's real pair
and its second, the rotation sense), the counts and their remainders, the
family's pair and the Node clock from the content there. 6. A measurement is a detector's click, an action of
the law on the state: a count arrives at the detector's Node and the
detector's count changes. Only a click is compared with nature or pinned as an
expectation; displays and the host's readings read state and write nothing.
7. The Inside is the GameBoard, where no one measures; the Outside is the
detectors and their clicks, the only thing claimed to represent nature.

### The constants

The causal bound is one Link per interval, and light's own speed at
long wavelength is 1 / sqrt(3) Links per interval (**The lattice
constants**, [the paces](#the-paces)). The quantum of action is one
click, its energy the quantum's norm T of its family. Newton's constant
is not declared: a body whose wells are s quanta per interval makes the
massless row's rest 3 G(r) s at r Links (the hold's row at the divisor
1, the well entering the field's line), 0.7582 s at the Node and 3 s /
(4 pi r) far away, and the level slows the clock by the potential Phi =
-c / Gamma, so

  G = 3 / (4 pi Gamma) per quantum of well, in Links and intervals,

a reading of Gamma and the lattice and no number of the law.
A world at a smaller Gamma has stronger gravity per unit of content; the
ratios between rows carry G once and cancel it. The quantum of distance is
the Link, of time the interval; nothing between two Nodes or two intervals
is observed. The row's source moves by whole quanta of well and never by
less, and the field itself is no click (**The fork, decided**).

**No free number but the mass** (the owner's words of 2026-09-29 and 2026-09-30): every divisor of the rule's own universe is 1, so G and alpha are no numbers of the law but readings of Gamma and the GameBoard's geometry; the matter pair's m is the one integer of nature beside Gamma and T, bounded by the band (den > num) and the reach cosh kappa = 3 den / num - 2 fitting the body's width. The constants the law derives with no free number are [the rows against nature](#the-rows-against-nature) (v).

### The rows against nature

Each row is a detector's click on a declared world, read blind, with
U_b = c_b / Gamma the potential at the point named (the clock's shift per level, the clock's pace); the bands are
the rounding's, one Node of centroid or one interval, and the draw's
where counts are read.

(a) **The redshift** (derived, blind, the advisor's derivation of 2026-09-30, #1509 comment 5903866751): two clocks of one family at the levels c_1 and c_2; the ratio of their tick intervals is the root of (1 - 2 U_1 + 2 U_1^2) / (1 - 2 U_2 + 2 U_2^2), 1 - (U_1 - U_2) to first order, for a band whose rotation follows the clock's pace; the band's own slope: at the content x = c / Gamma a record of the pair [num, den] at rest rotates at 2 cos omega = 2 - 2 ((den - num) / den) ((1 - x)^2 + x^2), so for matter [4000, 6000] cos omega = 2 / 3 + (2 x - 2 x^2) / 3 and d omega / omega = -1.06 x to the first order (**The clocks shift alike**): the gravitational redshift is the clock's share, z = 1.06 x, a matter clock five Links from the 2,000 pixel (x = 0.013) running 1.4 percent slow against a far one; light born by a breathing body in the well leaves with the body's rotation and keeps it in flight (a static content changes no frequency), so a far detector reads the emitter's slow clock; the run that reads it is a breathing pixel's light at a far detector, its period against a far clock's.
(b) **The bending** (derived, blind, the same derivation): at a Node of content x = L / Gamma light's line has S / w = 2 - 2 (1 - 2 x)^2 and R_a / w = (1 - 2 x)^2 / 3, so at long wavelength omega = (1 - 2 x) |k| / sqrt(3): light's speed is c(x) = c_0 (1 - 2 x), the index n = 1 / (1 - 2 x), n - 1 = 2 x, the Link's pace reading the content twice (**The Link is twice**); far from a body its field is the massless row's rest, L(r) = 3 sigma_tot / (4 pi r) beyond a few Links (sigma_tot the body's wells per interval, 1,637 for the 2,000 pixel), so n - 1 = 3 sigma_tot / (2 pi Gamma r), and a beam past the body at the closest distance b turns by 3 sigma_tot / (pi Gamma b) radians, 4 U_b, the centroid at a receiver L Links beyond shifted by 4 U_b L toward the body: for the 2,000 pixel at Gamma = 6,000, 0.26 / b radians, 3.0 degrees at b = 5 Links and 1.5 at b = 10; a lambda = 8 packet passing at b = 6 turns by 0.043 radians, a transverse shift of 1.3 Links over 30 Links of path, readable in the wave's front. The ratio that is nature's: the bending is 2 x and the redshift 1.06 x, so light is bent by 1.9 times a matter clock's share (exactly 2 against the clock's own share x, the 1.06 the band's slope at [4000, 6000]), against nature's 2, with no chosen number in it; the lattice computation of it to three digits, a pixel of 2,000 and a packet passing at five Links, the count's line's deflection against the clock's share at the same Node, is the first proof-grade number ((v), the first candidate): 2.00 within the rounding is the direction confirmed, 1.9 sharp a lattice correction to state.
(c) **The delay**: a round trip past the body, delayed by 4 U_b times the path's length within the well's reach.
(d) **The perihelion**: an orbiting emitter at semi-axis a and eccentricity e advances 6 pi U_p per orbit with U_p the potential at a (1 - e^2).
(e) **The moving clock**: a body at velocity v = n / W (its phase k per Link an exact pair of the file) has its tick lengthened by the dispersion of its own bound band: the tick's factor f = Omega(k) / omega_0 with Omega(k) = omega(k) - k omega'(k) the rotation at the moving centre (the phase rate less k times the group velocity) and omega(k) = omega_0 + Delta (1 - cos k) the body's bound band, omega_0 its rest rotation and Delta its packet's top velocity (at a quarter turn per Link), both the generator's from the file's counts and pair, no key; to the second order f = sqrt(1 - v^2 / c_b^2) with c_b^2 = Delta omega_0, Lorentz's factor at the body's own light speed; read as the mean of the front and back click periods P_v (1 -/+ v / u) at two resting detectors (u the light's group velocity), P_rest / P_v = f, the GameBoard's own term inside the rows' bands.
(f) **The charge**: like senses a hill, unlike a hollow; a reader of the sense q (the sign of its own sense at the Node, **The sign is the rotation sense**) reads - q times the holder's level in its pace; a current's read (like charges moving together repelling less, a vector part read as - q Lambda (**n** . **A**) div W) is a hypothesis under its own name and no line of the law ([what is open](#what-is-open)). **The coupling goes as the sign** (a finding): the read by sign enters the pace as q times a level, never as Q / M, so an electron and a proton accelerate alike in one field; the law has no Q / M line, and the response in a gradient is the mode's own and not the coupling's ([what is open](#what-is-open), item 3).
(g) **The two slits**: a radiating body, a wall body with two openings d Links apart (its count above the mirror's of [the paces](#the-paces)) and a screen body L Links beyond carrying the sets in strips: the strips' shares of the clicks are the openings' interference at lambda_q, cos^2 (pi d y / (lambda_q L)) at the height y under one opening's envelope, the bright strips lambda_q L / d apart, to the first order in the GameBoard's anisotropy; the exact shares are the two arms' phases **k** . **r** with the wavevector set by cos k_x + cos k_y + cos k_z = 3 cos omega den / num at the record's rotation, a term that at lambda_q = 4 Links on d = 16 and L = 97 moves the second bright pair from 6 to 8.5 strips of 4 Nodes and falls below one strip at lambda_q = 16; the record's rows show it splitting at the openings and its parts meeting on the screen (GAMEBOARD).
(h) **Bell**: two labels of one written wave, each clicking alone at its own end; the pair's birth, the turn at each end and the labels' clicks are open under the count's line (the old click and its rows are deleted, the model owner's word of 2026-09-29 on #1495, finding 10); the blind expectation stands: E(a, b) = cos 2(a - b), each side's marginal one half at every setting (no signalling), and S at the settings 0, pi / 4, pi / 8, 3 pi / 8 is 2 sqrt 2 = 2.83, nature's number; the pairs are the host's coincidence reading.
(i) **The fall**: a light body of D Links across, L Links from a heavy body of count c per Node on an open chain, under the hold as a sum ((g)): the held field's rest is the tent Delta^2 a = -3 sigma at the heavy body's Nodes (sigma = w c / E_s per Node per interval on [1, 1]), linear outside with the slope half the body's total source, 0 beyond the open faces; the light body's acceleration a = Delta x |d omega_0 / d c| x |c_+ - c_-| / D toward the heavy body (the feed's row, derived: Delta its mode's top velocity, d omega_0 / d c its redshift per level, c_+ and c_- the level at its two faces), its record's current growing by a x 3 Q M per interval, the fall of L Links in t = sqrt(2 L / a) intervals at the speed a t at the touch; the detector on the falling body reads the light the heavy body writes at its mode's period, the count of its clicks before the touch the waves whose flight at the group velocity ends before t; two light bodies of different shape in one tent read the equivalence principle, alike within the unit or a finding by name.
(j) **De Broglie's fringes**: (g) with a matter record shed by a body of that family (its own quanta leaving by the line, messages of matter, at the rotation omega_b of the body): a free record travels only where its family's band holds its rotation, num / (3 den) <= cos omega_b <= num / den; the record's wave number is the band's, cos omega_b = (num / (3 den)) (2 + cos k), its group velocity v = (num / (3 den)) sin k / sin omega_b, and to the second order k = omega_b v / c_m^2 with c_m^2 = omega_0 / (3 tan omega_0) the family's own light speed (0.2508 on [800, 1200]): de Broglie's law with the rest rotation as the mass; the strips' shares are (g)'s at lambda = 2 pi / k.
(k) **The two-qubit computer**: one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate (the phase (k_in - k) l over a depth l, [the paces](#the-paces)); two qubits are the two labels of one written wave, whose clicks paired by the host's window are (h)'s E; a controlled gate needs one record to turn another's phase, which the acts alone cannot (the theorem of the four acts) and a read can only through the pace: a target family reading the control family with the weight g_c has its pace wobble with the control's level, the first order averaging out over the control's rotation and the second order a hill of g_c^2 A^2 / (4 Gamma) over the overlap (A the control's amplitude), so the blind expectation is (h)'s E with that small phase, and a controlled phase of order one is a hypothesis under its own name, not in the law.
(l) **Mach-Zehnder**: a radiating body, a splitter (a body of a count inside the record's band, one Node deep along the beam, its reflected share s the slab's from [the paces](#the-paces), one half at the count found by bisection), a mirror on each arm (a count above the mirror's), a second splitter and two sets: the shares of the clicks are 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = k (L_1 - L_2) the arms' phase difference, so at equal arms and s = 1 / 2 every click is at the cross exit; the record's rows show the two arms (GAMEBOARD).
(m) **The round trip**: a radiating body receding at v from a mirror at rest, its set on itself, writing its wave every P intervals: the forward record's wave number solves Omega(k) + k v = omega_b (the body's rotation seen from the GameBoard), the returned record has the same rotation and wave number, and the returned clicks come every P (u + v) / (u - v) intervals with u the group velocity at that k: the two-way Doppler ratio with the light's group velocity in place of c.
(n) **Sagnac**: a radiating body with its set on itself moving at v along a ring of N Links (a periodic chain): one record's two arms return after N / (u + v) and N / (u - v) intervals, u the light's group velocity, so the set's clicks fall in two groups whose means differ by 2 N v / (u^2 - v^2), which is 4 A omega / u^2 for the ring's area A and angular speed omega to the first order in v / u (each arm's Doppler shift of k the second), and coincide at rest; a radiating body at rest on the ring reads one group at N / u.
(o) **The moving mass**: a body of a matter family shedding its quanta ((j)) toward a set L Links away: the record's quanta move at the count's line's velocity v = (num / (3 den)) sin k / sin omega_b, the set's clicks come L / v intervals after each quantum leaves, and the body's momentum moves by 3 Q_unit P_body (L div lambda_q) div L per quantum shed (the recoil); the record's rows show one packet at v (GAMEBOARD).
(p) **The medium's delay**: a light record through a window body of depth l (a count below the mirror's of [the paces](#the-paces)) is slowed inside to v_in = (p / Gamma)^2 sin k_in / (3 sin omega) with 1 - cos k_in = (Gamma / p)^2 (1 - cos k), the index v_g / v_in, and a set beyond reads the passage longer by l (1 / v_in - 1 / v_g), a round trip by twice that; through a window moving at w along the beam the record's wave number inside is matched at the moving face, omega - k w = omega_in - k_in w, and its speed inside is the band's group velocity at that k_in, not v_in + w; Fresnel's drag w (1 - v_in^2 / v_g^2) is nature's number beside it.
(q) **Dark matter**: a heavy body in a box and a light test body at the distance r on a circular orbit (v^2 = r a): the held field's rest outside the body is Laplace's ([1, 1]), c(r) = 3 s / (4 pi r) falling to the faces' 0 (the open faces' images steepen it near a face), so a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D falls as 1 / r^2 and v^2 as 1 / r, Kepler's fall-off, under the hold's write as a load and as a sum alike (the source inside, Laplace outside); the DETECTOR reads the orbit's period in the waits' phase as in (d); a flat v(r) is the finding that names a missing law.
(r) **Dark energy**: a radiating body and two far sets on a long periodic chain over 10^5 intervals: Rule3 is translation-invariant, so a free record keeps its wave number and rotation exactly and the sets' mean click interval stays the write's period P at every distance, the record's rows widening by the dispersion as the root of t while its count does not move (GAMEBOARD), the rounding's walk at most one unit of level per Node per interval; a mean interval growing with the distance is the finding.
(s) **The pixel's first look** (a GameBoard reading, a diagnostic and no click): one pixel of 2,000 at the Node on rule.json, on a board with at least one open axis (a board periodic on every axis has no rest), the generator laying the standing mode with its tail, the start sourced by the wells the lay writes; the blind expectation with the tension read (the advisor, #1509 comment 5903471455, both holders and the tension, the window's edge about 1,700 at the Node and 2,540 in all, its horizon p_a = Gamma - 2 L_0 - t_a = 0 at about 5,200 at the Node and 5,640 in all): 2 cos omega_b = 1.478, the period 8.50 intervals, the well 1,027 and the field 903 at the Node, the axis parts at rest -262 at the Node and their read t_a = -131, the mode's level at the Node b_0 = 8,608 with the tail 0.235 per Link, 2,640 quanta in all over 81 Nodes; over a run of at least three periods the form returns within b_0, the field within one unit after the transient, the count within its rounding walk of 0.058 quanta per unit; the back-in-time gate runs on the look's world before the look. Not yet run: the look is its own round after the round of the write (the generator's lay of the mode with its tail from the narrow branch, the start sourced by the wells, the search's memory bounded for 25^3; [what is open](#what-is-open), item 13).
(t) **The mass ratio's road to Gamma** (derived, blind, waiting on the advisor's inertia; the proton computed, not chosen, and the electron one quantum, [the hypotheses under their own names](#the-hypotheses-under-their-own-names)): the mass nature weighs is the well (**The mass is the well, the count the baryon number**), so m_p / m_e = 1,836 is the ratio of the proton's body's total well to one free quantum's, whose well is its count; the proton's body is the one where the well and the inertia agree, and its well fraction reads Gamma = 1,836 / (the well fraction): the horizon body's well is 0.352 Gamma at 5,000 at the Node and about 0.36 Gamma at the horizon itself ((u)), so Gamma about 5,150 with the horizon body and about 6,200 with the edge body, both beside the file's 6,000 by a road that is not the count's (the count ratios, 1,950 for the horizon body, 4,300 for the edge body and the earlier 6,500, are withdrawn); the inertia along the branch, the bound body's effective mass in a pace gradient against a free quantum's, is the computation that remains ([what is open](#what-is-open), item 1): if it agrees with the well, the momentum reading with the well is the law's line and the fall stays universal, and if it differs the line is reopened; until it is computed no number of Gamma is the law's, and the constants of (v) are predictions at the Gamma it fixes.
(u) **The well along the branch** (derived from the fixed point with the tension, #1519 comment 5903978440; a reading of the algebra and no click): the standing pixel's total well, the sum over its Nodes of D_i div T, gravity's source, against its total count along the narrow branch on rule.json:

| Count at the Node | Total count | Total well | Well over count | Total well over Gamma | Total count over Gamma |
| --- | --- | --- | --- | --- | --- |
| 1,650 (the edge) | 2,541 | 1,769 | 0.70 | 0.295 | 0.424 |
| 2,000 | 2,640 | 1,637 | 0.62 | 0.273 | 0.440 |
| 2,500 | 3,005 | 1,636 | 0.54 | 0.273 | 0.501 |
| 3,000 | 3,449 | 1,692 | 0.49 | 0.282 | 0.575 |
| 4,000 | 4,413 | 1,860 | 0.42 | 0.310 | 0.736 |
| 5,000 (near the horizon) | 5,440 | 2,114 | 0.39 | 0.352 | 0.907 |

A free quantum of matter at rest has a well equal to its count (**The electron is one quantum**), and a bound body's well is under its count everywhere in the window, 0.70 at the edge to 0.39 at the horizon: the binding lightens, the more so the deeper. The well has a minimum along the branch, 1,636 at about 2,500 at the Node (3,000 in all), and rises toward the horizon; the well's total is the record's conserved form over T, the body's energy against its count, so from the edge to 3,000 in all a quantum joining lowers the energy and beyond it raises it by 0.28 of a free quantum's, still 0.72 of binding: accretion pays all the way to the horizon, where it ends (the Links close), and the minimum at 3,000 is a distinguished count of the branch, noted and not read.
(v) **The constants the law derives with no free number** (#1521; each derived and never fitted, a blind number written before its run): the rule's own universe holds Gamma and T, two units as c and hbar are in nature, and the matter pair's m, the one free number, and every coupling is derived (the weights 1, the divisors 1, **The lattice constants**), so a constant of nature is derived as a dimensionless number, or as a dimensional one once the three units are fixed from nature; five candidates, in the order of their computation: (1) the bending factor of light, the bending over the clock's share, Einstein's 2 against Newton's 1: 1.9 on the lattice in the first approximation ((b)), the lattice computation to three digits the first proof-grade number, 2.00 within the rounding the direction confirmed; (2) the strength of gravity against the quantum, G m^2 / (hbar c), with Gamma and T as c and hbar and the matter quantum's mass from nature: the coupling of one quantum to another through the content holder at the divisor 1 (the pace's shift per level 1 / Gamma, the well per quantum 0.7582 at the Node and 3 / (4 pi r) beyond, [the constants](#the-constants)), to compute as a function of Gamma against nature's 1.75 x 10^-45 for the electron and 5.9 x 10^-39 for the proton, and whether a Gamma of the window reaches nature's size or the law says gravity between two quanta is of order one, a finding against nature to state; (3) alpha, the fine-structure constant: the sign holder's well of one quantum with the sense (its Wronskian's quanta, W div T) against the content holder's well of one quantum, both at the divisor 1, the electric against the gravitational pull between two electrons, nature's 4.2 x 10^42, and alpha itself as light's coupling to the charge (the bending of light's phase by one charge's well against one wavelength), to compute, with its distance from 1 / 137.036; (4) the mass ratio m_p / m_e = 1,836, read the other way, fixes Gamma ((t)), and then (1), (2) and (3) are predictions at that Gamma with no number left free, the strongest form of the proof; (5) the lattice constants 3 G(0) = 0.7582, 3 / (4 pi) far away and light's 1 / sqrt(3) Links per interval, the six Ports' own, exact and not nature's, entering every derivation above. A number that comes out against nature is written as such.

A row outside its band is a finding: it names the missing law or the
defect, and no body's numbers are patched to meet it.

## What is open

As of the owner's word of 2026-09-30 (#1519): an item sharpened to a computation stays as that computation, a decided line stands against nature until tested, an item the law's own words closed stays as one line saying why, and the rest is open.

1. **The proton and the electron**, one computation: the electron is one matter quantum with the sense -1 and no band of its own, and which body is the proton is computed, not chosen, the body where the well and the inertia agree (the horizon body, the endpoint of accretion, the advisor's candidate); Gamma follows from m_p / m_e = 1,836 through that body's well, about 5,150 with the horizon body and about 6,200 with the edge body ([the rows against nature](#the-rows-against-nature) (t)), once the advisor's inertia along the branch is computed; the count ratios 1,950, 4,300 and the earlier 6,500 are withdrawn, and until it is computed no number of Gamma is the law's.
2. **Which fixed point stands**, one computation: along the narrow branch the total count grows with the binding, dC / d lambda > 0 with lambda = 2 cos omega_b, and along the wide branch it falls, so by the Vakhitov and Kolokolov criterion the narrow branch is the stable body and the wide the saddle; a theorem of the continuum's equation, here a reading until a run of each.
3. **Q / M and the equivalence principle**, one computation: the coupling through the pace is universal (the read by sign enters as q, never as Q / M, (f)) and the response is not, a body's acceleration in a content gradient being its own mode's Delta d omega / dc, and a pixel near the horizon has a hopping that goes to 0 as (1 - 2 x_0)^2, so it barely moves where a free quantum moves fully, the electron light and the proton heavy in one field by the mode and not by a coupling; what it costs: the fall (d) of [what a body is](#what-a-body-is) takes the band's Delta for every body while the mode's own Delta is smaller (Delta x 2 tan (omega_0 / 2) differs by a tenth across the bound bodies), so a pixel would fall slower than a free quantum unless the fall's line is the mode's; the 2,000 pixel's drift in a content gradient against a free wave's decides between the law's sentence and the mode, and two light bodies in one tent read the rest ((i)).
4. **The lone quantum's detection**, decided, and against nature until tested: the click ends nothing (**The click ends nothing**), so feeble light and a lone quantum spread over many Nodes move no remainder over W_c and never click, and a free electron is never detected as one, where nature counts single photons and single electrons; the two slits' dilution series tests it, and its result is the law's answer, not a line to add. The owner's ask of 2026-09-30, the law's own line for the taking of light by a body (the body's re-write, the count's line's -1 at the taker, the light's quantum becoming the body's well), is with the advisor (#1509 comment 5904261873); its answer is written here as a line or a finding.
5. **The colours and the third**, closed as absent: a colour is a detector's reading of the click's axis, no charge of the body and no force of its own; the law has no strong force but the tail's reach, and a nucleus is horizon pixels within tail reach; the third [-1, 2] and the band [0, 1] are bands the rule allows and the universe does not use, and the charges 2 / 3 and 1 / 3, the generations and up and down leave with them, no line and no look (**The third and the colours, closed as absent**).
6. **The universe expands**, closed as a statement about boards: a look's board has an open face and the massless row its rest, a board closed on every axis has no rest and its level drifts, the finite board's word and no physics of the universe; no look rests on it (**The closed GameBoard has no rest**).
7. **The unread parts**, closed as out: nothing in the law reads a cross-axis part or a current (the owner's "they leave"); what would read them is item 15.
8. **The builds**, closed as decisions: the sense as the second level pair, light born by the write with no conversion and no ledger, the detector a declared Node, the board's shape a declaration, the start's rest for every part, the generator laying the pixel as the fixed point and the whole board back in time as a gate, a build each and no physics open.
9. **Gamma and T**, closed as a unit and a resolution: every prediction is written in counts and fractions of Gamma and does not depend on T, which only the rounding one accepts sets (2^19 for a hundredth of a quantum per unit at the pixel); Gamma is the one scale of the law, as the Planck length is nature's, fixed by one measured ratio once item 1 is computed.
10. **Radiation reaction**, closed by the sense's build: a family of quanta reads the sign holder by its own sense, so a breathing body reads the light it writes at its own Nodes and its pace answers; whether it cools is a run's finding.
11. **The mass defect**, closed as the law's reading with its caveat: gravity's source is the well, D_i div T, a bound body's wells under its count (1,637 against 2,640 at 2,000), the count conserved and the baryon number, not a mass; the caveat is the inertia, the fixed point's momentum against its well along the branch, the advisor's computation (**The mass is the well, the count the baryon number**).
12. **The neutron and the antineutron**, closed by the hole: the anti-body is the same record with its count's sign reversed, a body of holes the count's line makes and conserves, and the baryon number is the count's sign (**The anti-body is the count's sign reversed**).
13. **The generator's branch and the start's sources**: the generator lays a one-Node body from a spread over its neighbours with the declared counts as the first sources and finds the wide fixed point, a cloud; the pixel of the window is the narrow branch (**The count is read through both holders**), which a first lay sourced by the form the lay writes would reach, and the generator does not lay it yet; the engine's start sources the held rows by the vacuum's share of the record (about the count) while the run sources them by the well of each interval, D_i div T, so the field starts above the run's rest and the row with a gap jumps at the first interval: the start sourced by the wells, the fixed point of the wells under the rest they make, is the next round's line ([the rows against nature](#the-rows-against-nature) (s)).
14. **The tensions' start**: the start sources the time parts alone, so the massless row's tensions start at 0 and ring up to their rest under a standing body's stress over the first intervals, a transient that is no wave of the body; their start at the rest of the stress at the written moment (sources of both signs, the start's iteration converging wherever the board has a sink) is the next round's line.
15. **A cross-axis read or a current's read**, a hypothesis under its own name: a read of an off-diagonal part of the stress (a cross-axis term in Rule3's reads) or of the count's line's current per axis (a vector part, frame dragging, the induction of (f)); Rule3's line reads neither, so the parts that would carry them are not in the law (the owner, 2026-09-30).
16. Whether a body at rest jitters when its current's swing reaches T / 2: on sixteen Nodes the swing over 400 intervals is one percent of T / 2.
17. The self-source's cubic term: not in the engine, the line is the squares' sum alone.
18. The stable body theorem's Hessian beyond the dilation for a set of held rows, and the functional beyond first order in the well over Gamma ([the functional and the dilation](#the-functional-and-the-dilation)); whether the hill holds the body and whether the cooling brings a body to it ((e)) are a run's findings.
