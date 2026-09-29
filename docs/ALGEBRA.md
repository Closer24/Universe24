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

The families as the rule derives them from the two keys of a row, its pair and what it holds, with the graph of the reads down the ranks (**The families from the rule** above; the universe of record's rows, the bound charge beside them, and the third as a hypothesis under its own name):

| Family, its rank | Pair | Holds, at the divisor | Parts | Clicks | Reads | Its free number |
| --- | --- | --- | --- | --- | --- | --- |
| gravity, the tensor | [1, 1] | the content, E_s = G | 1, 3, 6 | never | none | G |
| charge, the vector | [1, 1] | the sign, E_s = alpha | 1, 3 | gives and takes one quantum | gravity, the bound charge | alpha |
| the bound charge (polarisation), the exact band | [1, 2] | the content, E_s = 1 | 1 | never | none | none, both keys fixed |
| matter, the scalar | [m, Gamma] | nothing | 1 | gives and takes one quantum | gravity, the bound charge; charge by q | m, the mass |
| the third (a hypothesis), the mirror band | [-1, 2] | nothing | 1 | gives and takes one quantum | as matter | none |

**The mass is one integer** (the owner, 2026-09-28, 10:46 Israel): every pair is written over the GameBoard's one denominator Gamma, cos omega_0 = m / Gamma, the file holding the numerator m alone: light m = Gamma, the exact band m = Gamma div 2 (Gamma even), matter its one integer, 6,667 in the universe of record (the nearest to 2 / 3: cos omega_0 0.666667 -> 0.6667, omega_0 0.841069 -> 0.841024, the reach cosh kappa 2.5 -> 2.49978, every number written before a run within 5 x 10^-5 of itself, the carried division the same act at the finer wall);

**The wall is one** (Cheshbon's correction, 2026-09-28, 14:12 Israel, on the de Broglie Experimenter's finding that a pair reduced to lowest terms shrinks the wall 4,000-fold, lifts A to 1.3 x 10^9 and drives the count's line past the width): the wall is w = 6 Gamma^3 for every family, the pair enters the coefficients as the file writes it, m over Gamma (R_a = 2 m p_a^2, the rest term 12 (Gamma - m) p_0^2), and a reduction to lowest terms is a reading and never the loader's act, so every family's remainder has the one resolution and the exact bands leave none in any form (S + 6 R = 6 Gamma^3 exactly); so the width's amplitude unit falls (A = 512,409 in the universe of record against 4,270,079 at [800, 1200], the pair (level, remainder) carrying the same bits) and T is set so that every record at c T stays under A (T at most 9 x 10^11 for the givers of record; 5 x 10^11 proposed).

**The final unification** (the owner, 2026-09-28, 10:53 Israel): the three of Rule3 is the three axes; the three axes give the three tensor ranks, 1, 3 and 6, the symmetric parts under the 48, and no fourth; every family is one rank and carries two keys, its pair and its divisor, of which the rule fixes at least one: a field that every family reads into its pace is on the pace's own band [1, 1] and its divisor is free (the vector's alpha, the tensor's G), a quantized scalar holds nothing, has no divisor, and its pair is free (the mass m), and an exact band ([1, 2], the period 6) has both fixed, the pair by the rule and the divisor 1 by the well being the count, so it carries none; thus each rank carries one free number and no more, the scalar the mass, the vector alpha, the tensor G: the count three is derived from the three axes, the values free as nature's. The crack, named: a second massive scalar family, a second mass at rank 1, the rule does not forbid; the universe of record declares one, and nature's spectrum of masses is the open row under this line. Its parts are the tensor rank of what writes it (1 the count; [1, 3] the count and the current; [1, 3, 6] the count, the current and the current's tensor), it carries quanta (a count and its current, [the count's line](#the-counts-line), the clicks) unless it holds the content, and never clicks where it does: the highest rank, which every family writes and which reads none, and the exact band that holds the content (the bound charge on [1, 2]), whose rest rotation at the vacuum's pace leaves no remainder (no remainder, no click), so two real fields; an exact band that carries quanta (the third on [-1, 2]) clicks as every family's does, exactly only in the vacuum (**The exact bands** below); its clicks are that same bit. Its reads are the graph of the ranks (each family reads the ranks above it) with the one weight 1 (reciprocity, [a family's write](#the-primitives)), and by its own count with the sign of the body that holds it, the same word as the read family's held count. Its held writer writes the count with the body's sign and the dipole of the body's spin with the divisor 1 for the real field and 2 for a family of quanta (Dirac's 2); the row's divisor E_s is one of the two free numbers of [the constants](#the-constants) (gravity's, G; the charge's, alpha). The action of one quantum is T, the universe's one integer for every family: Rule3 is linear and its form's scale is free, so no line of Rule3 fixes T; it is a unit, declared once, and no family, no body and no emitter declares its own (the owner, 2026-09-28). So the files hold Gamma, T, the matter pair and the two divisors, and nothing else of physics: `quantum` (1, the unit T), `sign` (0), `self_source` (0: the source is D_i div T), `clock` (the mode's `wavelength`), `Lambda` (1), every `weight` (1) and the held `factors` (the linearised field's 4 and 2, nature's numbers written by hand and no rule's) leave the files, and `spins_step` leaves with the spin's step below.

**The exact bands** (the owner's word, 2026-09-28, 11:44 Israel: the quarks are there for a reason and are almost never seen; the algebra on one Node, 12:03 Israel): the line of one Node at rest, a_next = 2 cos omega_0 a_now - a_before, is exact in integers only where 2 cos omega_0 is an integer, so the rule carries exactly three exact rotations, 2 cos omega_0 = 1, 0 and -1, the periods 6, 4 and 3, the pairs [1, 2], [0, 1] and [-1, 2]; a record on an exact band at rest at the vacuum's pace leaves no remainder in its rest rotation, so its quanta stand exactly at every Node, it gives nothing and never decays alone, and stable matter is built on an exact band; everything else of it clicks as every family's does, its packets (a wave number is no integer rotation), its Nodes in a well (2 cos omega = 2 - (p_0 / Gamma)^2 there) and its reads, so an exact band is seen exactly when it is moved or probed and only then (the owner's word, 2026-09-28, 12:25 Israel: it does click).

**The exact bands are exact only in the vacuum** (Cheshbon's correction, 2026-09-28, 13:09 Israel): at a Node of pace p_0 the band's rest rotation is 2 cos omega = 2 - 2 (den - num) (p_0 / Gamma)^2, an integer at p_0 = Gamma alone, so a record on an exact band inside a well, its own or another's, leaves a remainder and clicks like every family's: the third's three phases sum not to 0 but to a share of a record's level that grows with the well, 0.015 at a level 30 of 12,000, 0.148 at 300, 1.2 at the self-binding edge, and white matter stands only where the well at its Nodes is small against Gamma: under the divisor 1 (the well is the count) no white pixel exists and the third and the polarisation are messages of the vacuum, while under a divisor E_s of the universe of record a white body of thousands of quanta is white to 10^-5; so white matter requires a divisor far above 1, and the smallness of the charge's coupling is a condition of the quarks' whiteness before it is a distance of nature from the rule (the first line under **The three distances are the rule's**, below). The first is the bound charge, the polarisation, never seen free.

**The third** (the alternative named **The colours are three families under one constraint** below, with no first look; the standing line is **The colours are the three axes**, under which one family on [-1, 2] holds no white body and no tube, **A third does not bind itself**): a record on [-1, 2] turns a third per interval; three thirds in the phases 0, 2 pi / 3 and 4 pi / 3 (three consecutive states of one record) sum to zero in their linear write at every interval while their quanta add and stand constant (the white body), and the whiteness is read at every Node from its own three levels, the click's local language; when a third moves off its body every Node between the two carries the three levels' sum uncancelled, a record of the third's own count per Node, so the tube between them costs the third's count per Link and its cost is linear in the length (the tension is the count, no number: the strong force's line), its remainders cross T and click, each click a quantum moved whole along the tally's axis sigma_a, which lies along the tube (the click's vector converges to the direction of the missing third: the string pulls), and when the tube's quanta reach a third's worth the click converts them (**The conversion** below) into a new pair of thirds, the string breaks into mesons and a third is never free: confinement would be that theorem, and the width's refusal of a lone third is only the engine's shadow of it; the three colours are the three phases, a probe shorter than the body clicks at one Node and reads one phase, a third's charge reads a third, the sense of a third is the sign q of its read, and a meson is two thirds of opposite sign.

**The conversion** (a hypothesis under its own name: the weak force): a click that takes a quantum of one family and gives it as quanta of others, the rotations adding, is the whole weak interaction, one Node's act, no field and no massive vector, and no family's row declares anything for it. The band [0, 1], the charges 2 / 3 and 1 / 3 of the two thirds, and the three generations are open rows under this line ([what is open](#what-is-open)).
**The rule's own universe**, a hypothesis under its own name (the owner's word, 2026-09-28, 12:08 Israel: the hypothesis enters the finish line now): a universe whose every number is the rule's. Its pairs are the integers 1, 2 and 3 of the three exact rotations and the three axes: [1, 1] the vacuum's band, on which the two real fields stand, [1, 2] the exact band, [2, 3] the matter pair, cos omega_0 = 2 / 3, the first pair past the exact bands, which the universe of record approximates by 6,667 over 10^4, and [-1, 2] the third; its divisors are 1 (the well is the count: every held level is the count itself, so a count near Gamma div 2 is a horizon, the pace 0, and no body's Node exceeds it, the maximal coupling); Gamma is a multiple of 6 so that every pair is exact over it (12,000: m = 12,000, 6,000, 8,000 and -6,000); T is the one unit and cancels in every reading. So it carries zero free numbers, no G, no alpha and no m, against the universe of record's three, and it is the same rule and the same engine on another file, the sixth first look beside the five, a universe file of its own beside the universe of record and not in its place.

**A pair's numerator may be negative**: the third's R_a = 2 num p_a^2 is negative, S is what the line makes it, the band is the mirror of [1, 2] (2 cos omega inside [-1, 1] at every wave number and every pace at or below Gamma, the edge P = isqrt(2 den Gamma^2 div (den + num)) = 2 Gamma, the rest term 12 (den - num) p_0^2 = 36 p_0^2), and the loader admits a pair with den > |num| as a massive kind and refuses den <= |num| and den = 0 by name; nothing of Rule3 changes.

**The three colours are three interval states**: a third's record at rest steps (now, before) -> (-now - before, now) with the period 3, so its three phases are three bodies whose two levels are three consecutive states of one record (7, -10, 3 on one Node: each interval's three levels sum to 0 exactly, the quanta 7^2 + 10^2 + 3^2 - 7 (-10) - (-10) 3 - 3 x 7 constant), the generator writes two levels and no new key; the first look of the white body is on the rule's own universe file, its blind expectation there the three phases' sum 1.2 of a level at the edge and not 0 (a finding and not whiteness: **The exact bands are exact only in the vacuum**), and no look is on the universe of record; in the rule's own universe the matter is the pixels of [2, 3] and the light, and the third and the polarisation are messages, exact in the vacuum and clicking in every well.

**A third does not bind itself**: its read is negative, so its own well pushes its rest rotation up into the vacuum's band (2 cos omega = 0.31 at a count 3,000 of 12,000, inside [-1, 1]) and the record leaks; a record of the third at one Node is a packet of every wave number and disperses in every universe, its uniform mode alone exact; so one family on [-1, 2] holds no standing body, no white body and no tube, and **The third's** white body, tube and tension stand only with the colours as three families of one pair under one constraint of whiteness, **The colours are the three axes** (the Closer's line, 2026-09-28, 13:42 Israel, on the owner's word that the quarks close today; Cheshbon's derivation 13:46): the white body is a pixel of [2, 3]; the count's line carries a tally per axis, so the three colours are the three tallies sigma_x, sigma_y, sigma_z, and whiteness is their balance at rest (an isotropic tail carries no net current through any Port); under a pull the clicks are biased along one axis at the rate omega_b e^(-kappa d) per interval, which falls with the distance and gives no linear potential: the force between two pixels is short-ranged, its range 1 / kappa (2.2 Links at 3,000 of 12,000; the click's reach 18 Links at T = 1), the nuclear force between nucleons and no confinement inside a pixel, which has no inside; the smallest bound fraction of a horizon pixel is 0.2255 / (1 / 2) = 0.451, so a third of a pixel never binds and disperses (confinement is the edge, no line of its own) while two thirds bind, and a meson is two fractions above 0.451 of opposite q within the tail's reach; the charges 2 / 3 and 1 / 3 as numbers stay open.

**The colours are three families under one constraint** stays named as the alternative with no first look.

**The bound body is one Node** (the owner's word, 2026-09-28, 12:30 Israel: every bound body fits in one Node, and that is what pixelates everything): under the divisor 1 a body that binds itself at rest is one Node, its count c in [0.2255 Gamma, Gamma div 2), the lower edge where the one-Node well first holds a rotation below the vacuum's band (the three-dimensional Green's function of the six Ports, a pure number of the rule; below it the record disperses), the upper the horizon (the pace 0, the Node reads nothing and freezes); its record is the one-Node line at its bound rotation omega_b(c) (0.841 at the edge, 0.464 at 5,412 of 12,000) and its tail outside is the well, evanescent by kappa = acosh((9 / 2) cos omega_b - 2) per Link (0.45 at 3,000, 1.27 at 5,000: the tail ends within three Links); its mode carries the count through the form, D = now^2 - next x before = b^2 (2 - 2 cos omega_b) at rest with both levels b, so a pixel of c quanta loads with b = isqrt(c T den div (2 den - a)) for the clock pair [a, den] of 2 cos omega_b (69 at 3,000, 97 at 4,000, 139 at 5,000 of 12,000 at T = 1; isqrt(c) alone loads 1,812 quanta for 3,000, under every edge) and its tail as b t^(|dx| + |dy| + |dz|) rounded with t = e^(-kappa) (0.640 at 3,000, 0.362 at 4,000, 0.281 at 5,000); on an engine where the level enters the Link once (before the conformal term) the same Green's function puts the edge at 0.345 Gamma (4,136 of 12,000) with kappa 0.63 at 5,000 and 0.98 at 6,000, the number of that engine's first looks; a body of more quanta than Gamma div 2 is a cluster of such Nodes, each a bound body, clicking to one another. So between bound bodies there is nothing but the click and the band [1, 1]: the record does not leave its Node (kappa > 0), a quantum crosses a Link whole at a click and nothing else does ([the count's line](#the-counts-line)), the overlap of two tails within reach is read by the count's line and clicks (the exchange), and light and the two real fields carry the rest; a Node is a bound body or vacuum; the bound body keeps its record on the GameBoard and Rule3 steps it at its Node and along its tail as it steps every record (the one-Node line is the reading of its rotation, not a step of its own: with the six reads returning the Node's own level the line gives the Node's rest rotation, 1.05 at 3,000 of 12,000 by the pre-conformal coefficients and 0.62 by the conformal, and not the bound omega_b = 0.81 that the tail fixes; the tail is 0.64 of the level one Link away at 3,000 and carries the exchange and the fall), so the engine of the rule's universe is the engine of record on another file, and a step of the pixel alone is an optimisation for the day the tail is derived in integers. In the universe of record no body binds itself (the well is M div E_s, the edge M >= 0.2255 Gamma E_s), so its bodies are declared modes and the theorem does not reach them.

**The universe is bound**, the unification's assumption and no theorem (the owner's word, 2026-09-28, 12:37 Israel): every body is bound, no body is free, and a record that is in no bound body is a message between two clicks, the one that gave it and the one that will take it (a matter record below the edge cannot be a body and disperses; light never binds, its band's bottom is 0); a fall is the bias of a bound body's clicks, its tail longer toward the well (the local band lower there, kappa smaller), so the remainder crosses T first on that side; a click on a record with a partner label is entanglement and a click on a record with none is a measurement, and Bell's S reads that and nothing else; the assumption removes no number, it names the universe that has none, and where it fails (the universe of record, nature) the two distances stay.

**The click joins and parts** (the owner's word, 2026-09-28, 12:43 Israel: bound bodies join or part, and that is by clicks; the join is the non-local act): two clusters whose tails overlap (within 1 / kappa, three Links) read each other by the count's line and click, the tail biased toward the deeper (omega_b falls with c), so the smaller gives quantum by quantum to the larger until its count falls under the edge and it dissolves into messages the larger takes, the join a run of clicks whose last ends the smaller's record, one Node where c_1 + c_2 < Gamma div 2 and a cluster of two at the horizon otherwise, one record for the joined cluster; a cluster parts where a Node's count falls under the edge (it dissolves) or where two tails cease to overlap: the tail's e-fold is 1 / kappa (about two Links at 3,000 of 12,000) but the click's reach is where the Link's current a_1 a_2 e^(-kappa d) falls under T, d = ln(a_1 a_2 / T) / kappa, about 18 Links at T = 1 for two pixels of 3,000, and the transfer between two pixels runs at about omega_b e^(-kappa d) per interval (0.33 at two Links, 0.09 at five): beyond the reach no click, parted, and a taker at the horizon overflows into a neighbour inside its own well (the real field 0.34 of the count one Link away) so the cluster grows a Node per click (a body never splits into three equal pixels: 2 x 0.2255 < 1 / 2 < 3 x 0.2255); the one record opening for the joined cluster and closing everywhere for the parted one is **The half quantum's** one non-local act and there is no other; the conversion changes the family.

**The observer is a cluster**: a Node reads six Ports and a cluster's record is what its Nodes carry, so inside a cluster everything is seen (a GameBoard reading is the local language of its own record) and beyond its tail only a whole quantum arrives, a click.

**The tree**, the closure: the root is **The law in one line**; from it alone the exact bands, the colours, the tube's linear cost, the edge P, entanglement as the click and the observer as a cluster are derived; with the named assumption the pairs from 1, 2 and 3 (den the three axes) the matter pair [2, 3] and the crack [1, 3]; with the named assumption the divisors 1 (the rule's universe) the bound body as one Node with the edge 0.2255, the horizon, the tail, the cluster, and the click that remakes, joins and parts;

**The universe is bound** is an assumption and **The conversion** a hypothesis; so the algebra is closed on one root, two named assumptions, one assumption of the universe and one hypothesis, with zero numbers, and is not closed toward nature by name: the three distances alpha = 1 / 137.036, m_e / m_P and m_p / m_e (the rule's universe has one pixel mass scale, its counts within [0.2255, 1 / 2] Gamma), the charges 2 / 3 and 1 / 3, the generations and the band [0, 1];

**The three distances are the rule's** is the hypothesis under its own name that the three are derived, and its first two lines stand: a divisor far above 1 is what white matter needs; and **One quantum per giving** holds at the birth (the model owner's word of 2026-09-29 on #1495, finding 10): the given record is written once at the giver's click, g q M a_body div E_s at its Nodes, and scaled so its form lays exactly one quantum, its count then moved by the line, so a given record carries the one quantum the stock loses at any write and no longer bounds the charge's divisor from below; the flux of the written wave, a_light^2 sin omega sin k per outer Link per interval (0.745 a_light^2 at lambda = 4), sets the scale and not the quanta; the bound the window gave, E_s(charge) = 0.86 (Gamma div 2)^(3 / 2) at the horizon pixel (4.0 x 10^5 at Gamma = 12,000; 32,300 in the universe of record against the file's 40,000), stands as a reading of the written amplitude, derived from Gamma and no free number, while E_s(gravity) = 1 stands (the real field gives nothing).

**The algebra of clusters** (the owner's word, 2026-09-28, 14:40 Israel: the algebra is closed, so the five looks must close, and the rule's universe is a universe of clusters alone, whose algebra may differ a little because nothing else is there; Cheshbon's section, 14:55, one closed derivation from the root on the one assumption "only clusters", with the Nature24 session's lines of 14:44): (1) **The Node holds its count**: a Node holds one integer, its count c, and nothing else;

**The count is the record's form**: in a universe of clusters the count is laid from the record and no declared level stands beside it, the body's count SUM_i D_i div T over its Nodes with D = now^2 - next x before the form's Node term, the well at a Node D_i div T each interval with the remainder D mod T the fields' source, the click that integer division (the pixelation), so a declared count that is not the record's **Sum D** div T within the gate is refused by name; a count far below zero (the Bell Experimenter's -4,566, 14:27) is the count parted from its record, a defect of the lay and never a reading, while the hole of -1 at an edge Link is the line's own, conserved and filled: the count's line is the plain division act with no clamp, no block and no guard ([the count's line](#the-counts-line), **The inverse**).

(2) **The count is read once**: a count enters a family's pace once, through the held content of the family that holds it at the divisor 1, read down the graph of the ranks at the weight 1 (**The final unification**), so every family's pace at a Node is p_0 = Gamma - c and on its Link p_a = p_0 - c - c_a, a pixel's horizon is Gamma div 2 (with two held rows of content at the divisor 1, gravity's [1, 1] and the bound charge's [1, 2], the pace reads the count twice and the horizon falls to Gamma div 4: which row is the count's one reader in the rule's own universe is item 8 of [what is open](#what-is-open)), and 2c (the count read as the hold and again as the record's source, or again as a spin's step at the divisor 1) is a reading of the engine that differs from the algebra, a defect and never a finding: the content 12,157 at a pixel of 3,034 is four such readings.

(3) **The edge**: a pixel binds itself where the GameBoard's Green's function of its own well closes, at 0.2255 Gamma (2,706 of 12,000) on the law and at 0.3444 Gamma (4,133) on an engine where the level enters the Link once; below the edge a pixel is a cloud and disperses.

(4) **The tail**: the bound rotation omega_b, kappa = acosh((9 / 2) cos omega_b - 2), t = e^(-kappa), the level b t^d and the well c t^(2 d) at d Links; on the law 3,000: omega_b 0.8105, t 0.640, the wells 1,229 / 503 / 206 at 1 / 2 / 3 Links; 4,000: 0.6578, 0.362, 524 / 69 / 9; 5,000: 0.5137, 0.281, 395 / 31 / 2; with the level once 4,400: 0.8290, 0.754, 2,501 / 1,422 / 809; 4,700: 0.8055, 0.619, 1,801 / 690 / 264; 5,000: 0.7779, 0.532, 1,415 / 401 / 113; 6,000: 0.6741, 0.377, 853 / 121 / 17; two pixels bind together while each count with its partner's well at their distance stays within the horizon.

(5) **The transfer** between clusters is omega_b e^(-kappa d) per interval at d Links, and the click's reach ln(a_1 a_2 / T) / kappa (**The click joins and parts**).

(6) **The light** is written by clicks alone: g q M(n) times the body's rotation over E_s at the giver's Nodes, once at the giver's click and scaled so its form lays one quantum, its count then moved by the line; E_s(charge) = 0.86 (Gamma div 2)^(3 / 2), the giver's count at most (A^2 / T)^(1 / 3).

(7) **The one integer**: the universe of clusters carries Gamma and nothing else, the pixel's size in quanta; alpha / G goes as Gamma^(3 / 2) through the charge's divisor.

**The five looks on this section**: on an engine that reads the count once with the level once the bound window is 4,133 <= c < Gamma div 2 less the partner's well, so (a), (b) and (c) stand at 5,000, (d) at 4,400 and 4,700, (e) the giver 4,400 and the taker 5,000 (the clocks' ratio 1.066); on an engine that reads the count twice or more no pair binds under Gamma (the de Broglie Experimenter's 12,825 at 5,000 / 5,000, 14:22) and the fix is the reading, never the pair; with the conformal term (the level twice) the looks stand at 3,000 and 4,000 on the edge 2,706.

**The screen is a cluster** (the owner's question, 2026-09-28, 14:51 Israel: does what the look runs on the screen also have to be a bound body, since the universe holds bound bodies alone; Cheshbon's line, 14:55): everything that stands on the GameBoard of a look is a bound body or a cluster of them, the source, the screen, the slit's walls, the mirror and the detector alike, each pixel at or above the edge; a face of the GameBoard is no body, a click on a face is no click, and a look with a declared element that is no bound body is not a look in the rule's universe; a solid wall of adjacent bound pixels does not exist, two adjacent pixels at the edge pass the horizon on their Link in every case, so a screen is a sieve of pixels at a period s with the Links between them under the horizon: on the law 4,000 at s = 2 and 3,000 at s = 3 (a chain of 3,000 at s = 2), with the level once 5,000 or 6,000 at s = 2 and 4,400 at s = 4; a sieve at s = 2 reflects the light of lambda = 4 (Bragg's condition, 2 s = lambda) and is the wall and the mirror of the rule's universe, and a row of taker pixels at s = 2 is its screen, so the five looks are rewritten on sieves and clicks alone before their next run.

**The hierarchy is recursive** (the owner's word, 2026-09-28, 14:57 and 14:58 Israel; Cheshbon's line, 15:05): a cluster of clusters is the same structure one level up, Nodes each a bound body clicking at one another, with no number that bounds the depth;

**The click is the pointer**: the click is the only thing that passes between a cluster and its neighbour and between a level and the next, so from inside a cluster everything is seen and beyond the tail only a whole quantum arrives (**The observer is a cluster**);

**The levels at a Node are the nesting**: the three held levels of a Node, the matter's tail, the charge's well and gravity's well, are the three kinds of binding by rank, and the size of a level is the depth in its kind, gravity's well at a Node being the sum of the tails of every body above it (each c_i t_i^(2 d_i), the count its record lays there), so a GameBoard reading names the clusters a Node belongs to; a level n + 1 is bound by the same inequality as the level 1 with the cluster's total count over its members' spacing in place of a pixel's count over one Link, and the one bound on the depth is the horizon at a Node, the content read there under Gamma, at which a cluster's centre is the horizon pixel.

**The couplings are at the edge** (the Nature24 session's line, 14:44, corrected by the width): every coupling is the edge the rule allows and no number: a pixel's count is at most (A^2 / T)^(1 / 3) = 4,447 and its well at least 0.2255 Gamma = 2,706, so E_s(gravity) <= 1.64 and is 1, and E_s(charge) is the bound of the written amplitude, one quantum per giving holding at the birth at any E_s;

**The stable pixel is one**: the small gives to the large until it melts, so the bound universe has one stable count, the horizon pixel, and its second body, the electron, is the open distance m_p / m_e.

**The wavelength is the giver's** (Cheshbon's line, 15:05, on the Light Experimenter's question of 14:52): the given light carries the giver's bound rotation, and on the band [1, 1] cos omega = (2 + cos k) / 3 along an axis, so cos k = 3 cos omega_b - 2 and lambda = 2 pi / k: a pixel at the edge (omega_b = acos(2 / 3)) gives k = pi / 2 and lambda = 4 exactly, the law's wavelength derived; 4.18 at 3,000 and 5.29 at 4,000 on the law, 4.07 at 4,400 and 4.38 at 5,000 with the level once; a deeper pixel gives a longer wave, and a mode file's wavelength is this number rounded to the Link, 4 for every pair of the five looks.

**The closed GameBoard has no rest** (on the Light Experimenter's refusal of 14:59): the sum's rest on a GameBoard closed on every axis exists only under a net count 0, so a bound universe closed on itself carries a mean of the held field that drifts by the net count over the Nodes each interval, the hypothesis **The universe expands** under its own name and no look of today; a look keeps one axis open with its pixels far from the faces, and there is no sink, a count being never negative.

**The width bounds A by the least of the two** (Cheshbon's line, 15:27, on the Nature24 session's finding at Gamma = 24): the amplitude unit A is the largest amplitude at which every total of an interval stays inside the width, Rule3's 2 w A with w = 6 Gamma^3 and the count's line's 6 A^2, the least of the two and never Rule3's alone; at Gamma = 24 the two give 3.7 x 10^13 and 1.2 x 10^9, and the universe of 24 runs inside the width; a pixel's rotation lives in its clock pair.

**The electron is the lightest band**, a hypothesis under its own name (the Nature24 session's line, 15:27, on the owner's question what the electron does; Cheshbon's check, 15:32): the lightest massive band the rule holds is m = Gamma - 1, cos omega_e = 1 - 1 / Gamma, omega_e = sqrt(2 / Gamma), and the electron is one quantum on it with q = -1, no pixel (a pixel's ratio is at most 2.22), stable by the integer (one quantum does not disperse into fractions and no massive band lies below), its charge the proton's exactly since q is the click's integer, the positron the same band with q = +1 and pair creation **The conversion**;

**The mass is the count**: the rule reads inertia as the count, the momentum n = M v in the unit Q with the wall W = 3 Q M, so m_p / m_e = c_p / 1, the proton a pixel of 1,836 quanta, bound and within the horizon when 0.2255 Gamma <= 1,836 <= Gamma div 2, so Gamma lies between 3,672 (the horizon pixel) and 8,142 (the edge pixel) and the world's one number is measured; what this carries by name: one quantum is one energy and its rotation is its frequency, nature's E = h nu being the record's click rate, and the spin 1 / 2 is open. Two masses stand in this paragraph and are not one: the inertia of a body is its count (the momentum's wall W = 3 Q M), while the energy of a body is its quanta times their rotation (a quantum weighs its rotation, the source's row), so the inertial ratio c_p / 1 and the energy ratio c_p omega_b / omega_e differ by omega_b / omega_e, about 65 at Gamma = 12,000; which of the two nature's m_p / m_e reads is item 9 of [what is open](#what-is-open).

**The generator is Rule3** (the owner's word, 2026-09-28, 15:28 Israel: no floating point in the generator; Cheshbon's integer run at Gamma = 24, 15:41 and 15:43): a body's bound record is what Rule3 makes of its count at its Node in the engine's own integers, seeded at the Node with the count's well held, run on its GameBoard over many periods until the record stands (its levels repeating over a whole period), and the record itself is the mode file; its period P, its amplitude b, its clock pair [next + before, now], its tail level(d + 1) / level(d) and its wavelength are readings of the standing record and never inputs, a clock pair or a tail computed in floating point being a tool's defect; at Gamma = 24 Rule3 in integers gives the periods 9.6, 11, 12 and 14 at the counts 8 to 11 on the law (the Green's function: 9.55, 10.8, 12.2, 13.8), and the pixels the integers hold are b = 5 carrying 8 to 10 quanta and b = 8 carrying 12 to 15;

**The count is the record's form over its period**: an integer record's form D at a Node moves between 0 and 2 c within one period at Gamma = 24, so the count is (SUM over the period of D) div (P T), read once per period on the record's own clock, never the form of one interval as the count (the form of one interval is the well, that interval's source of the fields, the hold's row of [the primitives](#the-primitives)), which as a count kills a pixel of the law and drives a pixel of the level once to the horizon within ten intervals; until a file declares the record itself, a declared count is a reading checked against the loaded record's form at the gate |c - D div T| <= 2 isqrt(c) + 1 (the rounding of an integer amplitude moves D by about 2 b (2 - 2 cos omega_b), 1.5 sqrt(c)), refused by name beyond it; a count moves only whole, and a clamp that sets a negative result to 0 creates quanta and is no rule: the deficit is the hole of [the count's line](#the-counts-line), the count -1 with its remainder in range, which the line conserves and fills.

**Gamma is not constant**, a hypothesis under its own name (the owner's word, 2026-09-28, 15:44 Israel: every tick the universe grows by 6, which explains the expansion and how with the size more and more creatures became possible; Cheshbon's line, 15:50): Gamma_(t + 1) = Gamma_t + 6, the step the six Ports of a Node and no free number; the rule's physics depends on the ratios c / Gamma and m / Gamma alone, so every pair steps with Gamma ([m_0 Gamma_t div Gamma_0, Gamma_t], the matter +4 and light and the charge +6 per interval) and the wall and A are derived from Gamma_t each interval, the file holding node_clock as [Gamma_0, 6] and the engine no number; a count is the integer its Node holds and stays, so a pixel that does not gather falls under the rising edge 0.2255 Gamma_t and dissolves after (c / 0.2255 - Gamma_0) / 6 intervals, the small giving to the large being the way a body keeps its c / Gamma; the distinct bound counts between the edge and the horizon number 0.2745 Gamma, one and two thirds more kinds each interval (7 at 24, 1,647 at 6,000, 2,235 at 8,142); light on [Gamma, Gamma] does not drift, the clocks of pixels do, a pixel of a fixed count slowing as c / Gamma falls with the rate H = (6 / Gamma) |d ln omega_b / d ln (c / Gamma)|, 5 x 10^-4 to 1.3 x 10^-3 per interval at 6,000, the rule's Hubble rate, and Gamma = 6 t reads the universe's age in intervals (1,000 at 6,000); a look reads it as the takers' clock ratio growing by (6 / Gamma)(s_taker - s_giver) per interval, about 2.6 x 10^-4 at 6,000; at Gamma = 24 every pixel dissolves within three intervals of stepping, so the five looks keep Gamma fixed and a stepping Gamma is a look of its own.

**The close's weights under the term** (Cheshbon's line, 16:06, on the Newton Experimenter's reading of 15:56): the weighted current SUM q_n (now_n - before_n) is conserved where the Link coefficients are reciprocal in the weights, q_n R_(n to a) = q_a R_(a to n); without the conformal term R is symmetric and q_n = 2^16 Gamma^2 div p_n^2 at the clock's pace p_n = Gamma - c_n is exact, while under the term R_(n to a) = 2 m (Gamma - 2 c_n - c_a)^2 is not symmetric and no weight per Node is reciprocal on an uneven well, so B at the clock's pace leaves a current that the zero mode grows without bound; under the term the weight's pace is the Node's mean Link pace, p_n = Gamma - 2 c_n - (SUM over the six Ports of c_a) div 6, exact where the neighbours' counts are equal (a chain: Gamma - 2 c - t_x) and within the neighbours' spread otherwise, and only a current weighted on the Links is exact everywhere.

**A fixture's T is one quantum at its own rotor** (Cheshbon's line, 16:23 and 16:35, on the Newton Experimenter's table of 16:29): one quantum per giving is the record written once at the giver's click and scaled so its form lays one quantum, its count then moved by the line; the written light's flux per interval at the giver's own rotation, the scale's reading, is T = floor(a_light^2 N_face sin omega_b sin k) with cos k = 3 cos omega_b - 2 and a_light = (g M a + r) div E_s the light as written, in integers from the giver's clock pair [a, den] of 2 cos omega_b as T = isqrt((a_light^2 N_face)^2 (4 den^2 - a^2) (4 den^2 - (3 a - 4 den)^2)) div (4 den^2), of which sqrt(5) / 3 is the value at the edge alone; a giver whose E_s exceeds g M a writes 0 and is refused by name.

**The two readings of Gamma are two levels** (the owner's question, 16:27; Cheshbon's line, 16:35): under **The hierarchy is recursive** every level has its own Gamma and its own interval, a level's interval being the period of the record one level below it, so the proton to electron ratio reads the atomic level's Gamma (3,672 to 8,142, its interval the proton's period over about eight ticks) while the universe's age reads the top level's Gamma = 6 t, one tick for both being impossible; 1,836 is the local count of a cluster within a cluster; the tick ratio of one level is the cluster's period over the pixel's, P_2 / P_1 = e^(kappa d), 7.6 for two pixels of 2,000 at two Links at Gamma = 6,000 (the band 5 to 11, a number the join look reads as the breathing period of the pair's total count), and about 66 such levels lie between the atomic Gamma and the cosmic one.

**The ladder of the bound states** (Cheshbon's table, 16:45): the bound states of a Node at a given Gamma are one rung per integer amplitude b from the edge to the horizon, each carrying the count c = b^2 (2 - 2 cos omega_b(c)) at its self-consistent rotation, so at Gamma = 24 there are two rungs (b = 5 and b = 8) and at Gamma = 6,000 about 67 on the law (b = 46 to 112, c = 1,396 to 2,700, the period 7.5 to 13.4) and 27 with the level once, the ratio of neighbouring rungs 1 + 2 / b (1.04 at the edge, 1.02 at the horizon) and the whole ladder spanning 2.22, a near continuum that singles out no ratio: neither 1,836 (between the rungs b = 61 and 62 at 6,000) nor the hadrons' 1.31 is predicted, the mass ratio to the electron fixing Gamma and nothing more; with **The stable pixel is one** the proton is the horizon pixel, so m_p / m_e = Gamma div 2 and the atomic level's Gamma is 3,672 = 6 x 612, one number and no range, a derivation from the law and no prediction of 1,836, which is its input; the chain from the universe's age to that count is not closed: the age gives the top level's Gamma in the top level's own ticks, the step per level e^(kappa d) is a law's number only if the law fixes the stable cluster (horizon pixels in a sieve at the period 2 would give about 13 to 15), the count of levels and the law tying a level's Gamma to its parent's are open by name, and the join look with two horizon pixels at two Links reads the step as the pair's breathing period over the pixel's, about 13.5 in the band 9 to 20;

**Three kinds of binding, not three levels** (the owner's reading, 16:47; Cheshbon's line, 16:51): the three ranks give three kinds of binding, quanta into a pixel by the matter's tail (the step in count the pixel's c, in ticks its period), pixels into a white cluster by the charge's well (the step E_s over q M, 37 at Gamma = 3,672, the same number as the coupling's gap to alpha), and white clusters into a gravitational cluster by gravity's well (e^(kappa d) for tail-touching pixels, the sum's well beyond), and the third kind nests without bound, so the count of gravitational levels is the universe's history and no number of the law.

**The well is the count and no field: no computation at the threshold** (the owner's word, 2026-09-28, 17:58 Israel, on the Bell Experimenter's finding of 17:45; Cheshbon's line, 18:05): the threshold is kappa = 0, the bottom of the vacuum's band [1, 1] at k = 0 and the self-binding edge alike, where a tail is infinite and a static field on [1, 1] is Laplace's, no decay and no rest on a closed GameBoard; no computation of the law and none of the generator stands there: every bound body sits inside its band at kappa > 0 and light inside [1, 1] at k > 0. So in the rule's own universe (every held divisor 1) a held family has no record of its own that steps and no rest that is solved: its level at a Node is the count laid there and nothing else, every interval (**The count is read once**), the well at d Links is the matter record's own count there, c t^(2 d) laid from its form over its period (**The tail**), and gravity's well at a Node is the sum of those tails; a held record stepped by Rule3 on [Gamma, Gamma] at the divisor 1 (the Bell Experimenter's [2, 5, 7, 10, 10, 11, 8, 8, 7, 6, 5, 4, 3, 2, 1] along the white world's pipe from one pixel of 10, two pixels of 10 two Links apart reading 26 and 27; the Clock's 1,466 / 2,444 / 2,553 at the neighbours of 4,400) and a START's rest solved on [1, 1] (the Clock's 9,952 = 2.26 c at the charge over 400,000, where c div E_s = 0) are the field at the threshold, readings of the engine that differ from the algebra, the defects (d) and (e) and never findings; the files change in nothing, the divisor 1 being the word. The blind numbers under the line at Gamma = 24 with the level once: a pixel of 10 lays 2 / 0 / 0 at 1 / 2 / 3 Links (the wells 2.8 / 0.8 / 0.2), two pixels two Links apart read 10 to 11 each, a sieve's Node 8 to 11, the pipe [0, 0, 0, 2, 10, 2, 0, ...]. Under a divisor above 1 the held field on [1, 1] is the universe of record's (**The final unification, the fall, dark matter**), and the word's reach there is the owner's to say.

**The gate reads the form at any phase**: a standing record's D = now^2 - next x before at its Node is B^2 sin^2 omega_b at every interval, B its peak, and equals b^2 (2 den - a) div den with b the level where now = before alone (b = B cos(omega_b / 2)), so the gate compares the declared count with D of the loaded record after one interval of Rule3 and with no formula of a phase (the Clock's 5,310 against 4,379 is B read as b).

**The generator has no sink**: Rule3 is reversible and nothing leaves a GameBoard but a quantum by a click at a face; a fill of 0 beyond an open face and a slab zeroed each interval are walls (the Node beside reads 0: the reflection with the sign flipped), so the unbound part of a seed never leaves; a seed of one Node carries the mode's share 1 / (1 + 6 t^2 + 18 t^4 + 38 t^6 + 66 t^8) (0.18 at Gamma = 24 with the level once, 0.62 on the law) and the rest is debris spread over the GameBoard's V Nodes, so the record is read at the Node over many periods on a GameBoard whose V dilutes the debris and purified by re-seeding from the record within three Links of the Node at its peak's phase, 0 elsewhere, integers alone, each pass leaving the debris its share within reach (about 180 / V); a record whose pair lies inside the vacuum's band (the Clock's [8, 8], the period 6, against the bound periods 8 to 14 at 24) is a mode of the walls and no pixel, and every reading is at the Node, never the GameBoard's sum.

**The generator of the rule's universe writes bound bodies alone** (the owner's word, 14:32): a body is its count at its Node; its record is the bound state of that count and nothing else, b through the form and the tail from kappa (**The wall is one**), no free record and no declared mode; a world file holds counts, their bound records and the band [1, 1], and nothing more.

### The interval

The engine steps every family from the state at the interval's start to
the state at its end. Every read is of the start's values: the six
neighbours' levels, the Node's own pace, the arrivals, never a value
written in the same interval; one Link per interval and nothing in zero
time. The interval has five acts, in order:

(i) the signed read: every family's paces from the held families' levels
at the start, the guard two-sided; (ii) Rule3 on every level: each family
of quanta by its pair and its paces, each held family's parts at the pace
1; (iii) the count's line on every family's count (the current through the
Ports), the reports at the Nodes told to report its reading; (iv) the
hold: each held family's time part gains its source over its divisor; (v)
the bodies' clocks and the givings at their clicks, each a reading of the
count's line and the one act a click writes (a body has no law of its own).

A giving's writes are read from the next interval. Backward, the acts
run in reverse order, each by Rule3's direction -1, and the givings are
not taken back.

### Readings and measurements

A **measurement** is a detector's click: the one act of the law on the
state that ends a record at the detector and changes the detector's own
record ([the count's line](#the-counts-line)). Only a measurement is compared with nature. A
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

(ii) **The Link is twice**: along a Link every wave's speed falls with p_a = Gamma - 2 c - t_a, the level entering the Link twice and the clock once, so light is delayed and bent into a mass by twice the clock's share (the bending 4 U_1 / b, [the rows against nature](#the-rows-against-nature) (b)). The line is not conformal: a light wave at a fixed wave number scales with (p_a / Gamma)^2 and a bound mode at rest with (p_0 / Gamma)^2, and the two differ already at the first order in c / Gamma (0.625 against 0.411 at c = 3,000 of 12,000 on [8000, 12000], k = 0 against pi); a light record's rotation is conserved along its path, the paces being static, so a light record read against a matter clock at one level reads the clock's shift, (i), and the bending reads (ii).

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
a_before declared 0 it KEEPS a level; with a / b = 2 from (0, 1) it COUNTS,
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
slows the clock, an attraction); a negative weight is a hill. By "q" the
weight is multiplied by the reading record's charge sign. A family with
no reads steps at p_0 = p_a = Gamma, the plain rule. The clock's slowing
is this pace: a record at a Node of pace p rotates and moves as a record
at Gamma does, with its intervals p / Gamma as long.

**The level enters the Link twice and the clock once**: the time level lowers the clock's pace p_0 once and each axis's pace p_a once more, so a wave's speed along a Link falls by the level twice (the Link as well as the clock, as nature's light past a body bends by twice the clock's share) while a mode's rest rotation, from S alone, falls by the level once (the owner's word, 2026-09-28, 08:40 Israel: the light experiment settles the symmetries inside the engine, with Nature24's line of 08:55 Israel; the bending's centroid against the twin reads it, twice the clock's share).

**The clock's second order is the composition** (the owner's word, 2026-09-29: simplify the clock): each unit of the level slows the clock as it already stands, p_0 = Gamma (1 - 1 / Gamma)^c, whose square to the second order is (Gamma - c)^2 + c^2 = Gamma^2 (1 - 2 Phi + 2 Phi^2) in the level's share Phi = c / Gamma; Rule3's coefficients take the paces' squares as written, no division act and no rounding, and the pace itself, where a guard reads it, is the integer square root of its square (p_0 = Gamma - c + c^2 div 2 Gamma to the unit); the Link's pace stays Gamma - 2 c - (the aa components div 2), the level entering it twice.

**Computed** by the geometric optics of the band beside the paper (einstein_check.py, both forms of S): the light's bending 4 U_1 / b (2.02 x Newton's) with the clock to the first order or the second, the periapsis advance of the matter pair 7 pi U_1 / (a (1 - e^2)) (1.17 x Einstein's) with the clock to the first order and 6 pi U_1 / (a (1 - e^2)) (1.00 x Einstein's) with the second order; the second order of the clock is the line and the engine follows it (the owner's word, 2026-09-29, with the Link twice).

**The guard**, two-sided: 0 < p <= P at every Node, with the edge

  P = isqrt(2 den Gamma^2 div (den + num)),

Gamma for light and above Gamma where num < den, read on the clock's pace p_0 = isqrt((Gamma - c)^2 + c^2) and on each Link's pace p_a alike. Below 0 a pace is no clock; beyond P the step
is unstable: the mode at wave number pi on every axis has the factor (S - 2 SUM_a R_a) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 - 4 (num / den) (p_a / Gamma)^2, which
is -2 num / den in the vacuum and stays at or above -2 wherever p_0 and p_a are both at or below P,
since (P / Gamma)^2 (2 - 2 num / den + 4 num / den) <= 4 exactly when P^2 (den + num) <= 2 den Gamma^2;
a pace beyond P lets the record grow without bound,
and every pace at or below Gamma is inside it. A hill lessens a hollow and never exceeds it; a pace outside
the guard refuses the run naming the Node.

**The band at a pace**, a reading of the line and no new rule: at a Node of the clock's pace p_0 and the Link's pace p_a on every axis a record's rotation at wave number k along an axis is cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) (p_a / Gamma)^2 (1 - cos k), with SUM_a (1 - cos k_a) in place of 1 - cos k off an axis, so the band of rotations a body's Nodes carry narrows with the paces: a record whose rotation lies outside the band there is evanescent inside (for [1, 1], cosh kappa = (Gamma / p_a)^2 (1 - cos k) - 1 per Node) and is reflected whole, and one whose rotation lies inside is slowed to the band's group velocity (num / (3 den)) (p_a / Gamma)^2 sin k_in / sin omega with 1 - cos k_in = (Gamma / p_a)^2 (1 - cos k) for [1, 1]; light ([1, 1]) meets a total mirror exactly where p_a < Gamma sin(k / 2), that is where the count c exceeds Gamma (1 - sin(k / 2)) div 2 (1,464 at lambda = 4 Links, 1,946 at 4.78), and a window otherwise, with the step's partial share at each face.

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

The **family of clicks** is one family like every other: its level at a
Node is the **count** c, the number of quanta there; its wall is T, the
quantum's norm; its read is the current. At every Node,

  T c_next + r' = T c_now + SUM_j F_ij + r,   0 <= r' < T,

the sum over the six Ports of the current into the Node from its
neighbour over the interval, r the remainder kept at the Node: Rule3
with the coefficient 1 on each axis's inflow through its two Ports, T on
the count and the wall T. The **click** is the division: a quantum moves
whole from one Node to the next exactly when the remainder crosses T,
and never a fraction of one. The record ends where its last quantum
leaves it; the count that arrives at a detector's Node is the
detector's click, and a detector's count is the family of clicks' level
at its Nodes; an emitter's giving is the count leaving through its
outer Ports into the born record. The same line carries a body: the
count follows its record's current at every Node, one quantum at a
time, so a body moves without any accumulator of its position.

**The free record** (the model owner's word of 2026-09-29 on #1495, finding 10: every bound body gives at its click, a detector is a Node told to report the count arriving, and the old click is deleted, not kept beside the new): a given record is laid with one quantum from its form at its birth, at the giving body's click, its two levels written once at the body's Nodes and scaled so the count its form lays is exactly one quantum (the generator's act; no scale that lays exactly one is refused by name); its count moves by this line, as a body's does; a Node told to report (a detector's Node, an open face's layer) reports each quantum standing on it and hands it to its body; and the record ends where its last quantum left it. A detector is one connected region of Nodes with one name; separate places are separate names. There is one click: this line's.

**The remainder's origin**. The remainder at a Node starts at the
origin T div 2: started at 0, a Node with no quantum reads the count -1 at its first
outward swing (T c + r below 0), a hole the line conserves and nature
does not show. A body's count is laid with its record: at every Node
T c + r is the Node's share of the record's form plus the origin, so
the count follows the norm with the margin T / 2 against the rounding's
walk. **The lay and the wall**: the share is the form in the current's units, E_i / 2 = 3 den (now_i^2 + before_i^2) - num x now_i x S_6(before)_i, whose change over one interval of Rule3 is exactly SUM_j F_ij at every Node in the vacuum, where every pace is Gamma and S = 0 (the line is the continuity of Rule3's conserved form there; in a well the conserved form carries the weight Gamma^2 / p_i^2 on the Node term, [the conserved form](#the-conserved-form), so the plain share's change parts from the currents at the well's Nodes: on the chain body of Gamma 6,000 at rest by up to 20 quanta at its centre Node in one interval, oscillating and bounded, the body standing; on the same body moving, accumulating at its rear into a count of -32 within 200 intervals, the Paper Writer's measurement of 2026-09-29) and whose sum over a closed GameBoard is exactly 3 den SUM_i D_i with D_i = now^2 - next x before in the vacuum alike; so the count's wall at every Node is 3 den T, T the universe's quantum action and 3 den the family's plain wall, the body's count is the sum of the counts laid at its Nodes (SUM_i D_i div T in the vacuum), and a declared count is checked against the laid sum at the gate |c - laid| <= 2 isqrt(c) + 1, refused by name beyond it. The count is laid once, at the first act, and then moves by the line's flux alone.

**The inverse** is the same line with the current reversed: T c_now + r =
T c_next + r' - SUM_j F_ij, exact, the currents read from the
interval's levels as the forward step read them. The line has no other act: a total below zero gives the count -1 with the remainder in range, the hole above, which the line conserves and fills (a lawful body's edge Links read such holes, so a guard that refused them would end every lawful run); a clamp at 0 would create quanta, and a block of a Node's currents is a branch on a Node's value that reads two Links away and loses the inverse, so neither is a rule.

**Theorem** (the count is conserved). Over any region of Nodes, SUM (T c_i +
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

**The bound**. The total at a Node is at most 6 x weight x 4 A^2 + T (c + 1)
+ T: one current per Port, each the weight times the two products of two
levels at A on each of the two level pairs, the count's wall T (c + 1)
and the remainder below T. The shipped universe (A = 2^20, the weight
800) is within int64; a world declaring A beyond 2^24 at the weight
10^3 is refused by name; the generator's A ([the generator](#the-generator) (f)) is
admitted.

## The primitives
**A family's write is one act**: every write into a family's level on the GameBoard is (w x q(Node) + r) div E at a Node each interval, at both levels of the writer's rotation (the second the read act once more, halved), the division act with the remainder r carried at that Node: q(Node) the writer's own quantity THERE (a body: the count declared there times its tensor (1, n_a / W, n_a n_b / W^2), the source sigma u_a u_b; a record: its quanta there, D_i div T, times its rotation over the rest rotation of the matter quantum, omega_r / omega_m (the energy sources, as a photon weighs h omega / c^2); the giving: the body's record's two levels at the shell times its bound charge M_pol(Node), the polarisation it holds there; the recoil: the click's tally), w the one weight of the pair of families (the weight with which the writer's family reads the written family: whoever reads with w sources with w, action and reaction one key), E the written row's divisor (E_s; the recoil's wall L); the hold, the source, the giving, **The start** (the rest of the hold's line, its fixed point) and the recoil (the same act into the record's phase at the Port, the recoil's accumulator) are its five instances, and no number is the act's own; generic (the rows' keys), vector (one carried division), local (the Node).


Every act of the engine is a pure function of the whole GameBoard's
arrays that calls Rule3 and nothing else, in `src/event_universe/node.py`
and in the folders of `src/event_universe/features/` (the count's line, the
hold, the write, the signed read, the start); the GameBoard calls them in
the interval's order ([the interval](#the-interval)). No act holds a
number, a family's name or a default. Every write is a whole integer
into a family's level; every division's remainder lives at the Node
where it divided.

| Primitive | Place | Reads | Writes | The line |
| --- | --- | --- | --- | --- |
| the signed read | (i) | the read families' time parts at the start, the weights, by, the tensor's parts | the paces | [the paces](#the-paces); the content as it is, no floor, the guard two-sided |
| the operation | (ii) | the coefficients from the pair and the paces; a held family's parts at the pace 1 | every family's levels | Rule3's line itself |
| the count's line | (iii) | the family's levels at the Node and across its six Ports as the step produced them, T, the weight num, the Nodes told to report | the family's count at a Node, its remainder | [the count's line](#the-counts-line): the count is the family's, one count per family over the GameBoard, laid once at the first act from the family's levels and moved by the line alone; a body's quanta of another family are that family's count at its Nodes; a detector reports the rise of the count summed over its Nodes, the net inflow across its boundary, a reading, and nothing is handed over (the model owner's word of 2026-09-29 on #1495, (c)) |
| the hold | (iv) | a body's content M_k, the quantum's weight w_k of each family (one for every family, no key: the count's quantum), the row's divisor E_s (its key `divisor`, an integer from 1, required), the count's line's net current j_a at the Node (a reading of the record, as the momentum **n** is), the dipole (the body's spin **S**, the curl of that current about its centre, a reading) | the held family's levels at the body's Nodes; the body's remainders | the count s = SUM_k w_k M_k enters the field's line as a source: the time part at the body's Nodes gains (s + r) div E_s each interval, the division act as a load with the remainder r carried on the body, and at a body in the law's form ([what a body is](#what-a-body-is), its Nodes with their counts) each Node gains (w_k M_k(Node) + r) div E_s of the count declared THERE with a remainder of its own, never the whole s at every Node, a signed source the body's charge q times the Node's count (**The sign is the body's**, 2026-09-28: a family carries no sign and `sign` leaves its files, a body's key q signs its count, so one matter family holds bodies of both signs and the third exact band's sense is sign q); so that two bodies' wells add, a body stands in another's well, and the field's rest is Poisson's with the sources (nature's form: potentials add; a level clamped to the count would make a body's Nodes carry its own count alone); **The well of a body with a record is its record's form** (the owner's word 2026-09-28: the well is the count, and the count is the record's quanta, D_i div T): at every Node of such a body the count written is its own record's quanta there, D_i div T with the form's remainder carried, the source's instance on its own record each interval ([the count's line](#the-counts-line) is its integral, the same in the mean), so the well moves with the record to the form's resolution and the self-force vanishes (the well is the record's own, action and reaction), and a bound body falls in a pace gradient at the free packet's rate (Newton's reading, 2026-09-28: the engine equals the algebra for a free packet to a second order of the gradient); a well written from an integer count alone moves only when a quantum's current crosses T, lags the record's shift a / Omega^2 below one quantum and pins it (the engine's zero of a bound body alone in the tent), a defect and not a finding; the vector part (j_a + r) div (E_s T), j_a the count's line's net current of the Node through its two Ports of the axis ([the count's line](#the-counts-line); the momentum n_a = 3 Q j_a div T its reading, W = 3 Q M its wall), and the tensor part (n_a n_b + r) div (E_s M(Node)), each with its remainder carried and per Node as the time part: the three parts are one source, the count and its current's tensor at one scale with no factor of the files (the linearised field's 4 and 2 were nature's numbers by hand; the rule's own reading against the moving body decides them), so the row's divisor divides each; the dipole sigma (D x e_j)_i div its divisor at the six neighbours |
| the giving | (v) | the body's click (its clock's crossing), its family's count at its shell, its family's two levels at the Node that gives | the count at that Node, the given family's two levels there | at every click of every body, no key (the model owner's word of 2026-09-29 on #1495, (c)): one quantum leaves through an outer Port from the shell Node where its family's count stands highest, where it is at least 1, into the given family, the one holder of the sign its family reads (the count there -1 of its own family and +1 of the given; the conversion changes the family), and the given family's two levels there gain the body's family's two levels scaled so that the form the write adds lays exactly one count ([the count's line](#the-counts-line), the lay and the wall), refused by name where no scale does |
| the feed | none | **Derived**, no primitive: the body's record in the pace gradient | the body's momentum **n** as a reading | a body has no law of motion of its own: its record moves by Rule3 alone, and in a pace gradient its packet accelerates at a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D (Delta the mode's top velocity, the second derivative of its band in k; d omega_0 / d c the mode's redshift per level; c_+ and c_- the read level at its two faces D Links apart), the count follows the record by the count's line, and its momentum **n** is the reading of its record's current (SUM over its Links of F_ij at the norm T: the count's line's velocity times 3 Q_unit M); no coefficient is declared; bodies with the same Delta x d omega_0 / d c fall alike, and two light bodies in one tent read it |
| the induction | none | **Derived**, no primitive: the record's drift in the vector part | the body's momentum **n** as a reading | the reader's pace carries the read family's vector part, - (n_b V_b) div W ((f) **The charge** of [the rows against nature](#the-rows-against-nature)), so the record's packet turns and drifts in a vector part's gradient by Rule3 alone: the Lorentz force and its gravitational twin with no line of their own; **n** the reading as the feed's |

The hop is retired: the count's line moves the count with its record's
current, and no accumulator of a body's position remains. The click is one mechanism: the count's line carries every family's quanta, and a Node told to report reads each quantum that arrives whole.

A body's writes into its family's levels (the hold): a body of quanta
M_k of the family k, each family's quantum weighing w_k (one for every
family, no key: the count's quantum), has the count s = SUM_k w_k M_k, the charge Q, the
momentum **n** = 3 Q **j** div T with **j** the count's line's current through
its Ports (a reading of its record: **j** / T its quanta crossing per interval, **n** / W its velocity in Links per interval with the wall W = 3 Q M, and **Sum F** = T n / (3 Q) as [the generator](#the-generator) (e) reads it), the spin **S** the curl of that current about its centre and the moment
**mu** the same with the charge's sign; at every Node of its support it writes gravity's time part s, its
vector j_a div T, its tensor (n_a n_b) div M, the charge's time
part Q and vector the same current with the charge's sign, no factor of the files (the 4 and 2 of the
linearised field were nature's numbers by hand); and the dipoles at its Node's six neighbours, gravity's vector i at the Node + sigma e_j gaining sigma (S x e_j)_i, the charge's (sigma (mu x e_j)_i) div 2.
## The stable body

### What a body is

A body is its count and its record over its Nodes, and never one Node: every body is many Nodes, and nothing gathers it (the owner's word of 2026-09-28). The count c_i is the family of clicks' level at the body's Nodes, in quanta; it enters Rule3 through the pace alone, p_i = Gamma - the held level at the Node (the source's rest: the body's own count and its neighbours' over the divisor), and it never splits: a quantum moves whole, by the count's line. The record (now, before) of the body's family splits by the send and is bound by the wells its counts source.

**The four lines of the body** (the owner's word, in the law's words): (a) **The body is the fixed point of its binding row**: a body is its quanta over its Nodes; its counts source every held row at the row's divisor; its record is the standing record Rule3 makes in those paces; its counts are that record's form, D div T, with the remainder carried; it stands where the counts return themselves; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace reaching 0).

(b) **The form sources the fields**: a held row's level is the rest **The start** solves from the counts at the row's divisor and Rule3 steps; no row holds at the divisor 1; a well is a field with a reach, the gapped pair's 1 / kappa.

(c) **The count moves by the count's line alone**: the count is laid once, at the first act, from the record's form ([the count's line](#the-counts-line), **The lay and the wall**), and after it no count is laid from the form: the count at a Node changes only by the line's flux, and the total is conserved; the well, D_i div T each interval, is the record's quanta as the fields' source and no count. A body's Nodes are the Nodes where its count stands, each interval: the set follows the quanta by the line alone, nothing else moves it, and its shell, the Nodes among them with a Port to a Node beyond, is where its clicks are read (the surface rule), so a moving body's clicks are read at its moving shell.

(d) **The fall**: a = Delta |d omega_b / dc| grad c, Delta the band's curvature at k = 0, d omega_b / dc from Rule3's coefficients at the body's pace and rotation, grad c the other body's content, one line for every held row the body sources. Which fixed point stands is [the stable body theorem](#the-functional-and-the-dilation). The world file names the body's family, its Nodes with their counts and the quanta of other families it holds, and nothing else: no momentum, no spin, no emitter (every body gives at its click), no lowered pair on its Nodes, no seed, no stop, no closed Port, no period (P_body is its mode's rotation); its two levels are the generator's mode file beside the world.

### The well

At a Node whose held level is c Rule3's one-Node rotation rises from cos omega_0 = num / den by (1 - p^2 / Gamma^2)(den - num) / den, and its bonds fall from num / (3 den) to num p_i p_j / (3 den Gamma^2): the symmetric form of the line with the weights 1 / p_i. The depth is bounded by the family's own 1 - cos omega_0, so a family whose pair lies close to 1 binds nothing: on [800, 809] (1 - cos omega_0 = 0.011) no cube of any side at any count is bound; on [800, 1200] (1 / 3) at Gamma = 10^4 a cube of side 12 is bound from the level 500 at its Nodes (the mode's share inside 0.79, 0.92 at 1000, 0.997 at 5000), of side 6 from 1000, of side 3 at 3000, one Node at 5000; omega_b / omega_0 for side 12 is 0.832 at 500 and 0.771 at 2000. A body's clock is set by the level at its Nodes and its side, from the rule: a body's mass is its count.

**The reach of a held family is its pair**: under the hold as a sum a held family's rest solves num Delta^2 a - 6 (den - num) a = -3 den sigma (its line a_next = num S_6(a_now) div (3 den) - a_before with the source once an interval, Delta^2 the six-neighbour second difference), so outside a body its rest falls by e^(-kappa) per Link with cosh kappa = 3 den / num - 2, the family's own band at zero rotation (cos omega = (num / (3 den)) (2 + cos k) at omega = 0, the evanescent k; kappa^2 = 6 den / num - 6 to the second order, the static limit of the source's row), the same pair that sets the band of its records and de Broglie's k for them ((j)): the gap is the mass of the records and the inverse reach of the field, one number; [1, 1] has no gap (2 cos omega = 2 at k = 0) and its rest is Poisson's over the whole GameBoard, the pull between bodies (Newton's tent, (i)); a pair with den > num has the gap 2 cos omega = 2 num / den at k = 0 and inside a thick body its rest stands at 3 den sigma / (num kappa^2) (Delta^2 the six-neighbour second difference, kappa^2 its value on e^(-kappa r)), so at [1, 2] with the divisor 1 the level inside a body is its count and falls by e^(-kappa) = 0.127 per Link outside (cosh kappa = 4): a body's well is the static field of every family it holds, read at its Nodes by the paces, so a body's binding, a mirror's line c > Gamma (1 - sin(k / 2)) and a window are the short-reach family's and the pull between bodies the massless one's, two held rows of the universe file, one pair each; generic (a row's pair and divisor, no name), vector (the line's own static limit, no root), local (the six reads and the source at the Node).

### The functional and the dilation

**The functional**. Let a body of M quanta have the record phi over its region, SUM phi_i^2 = 1, its counts the form c_i = M phi_i^2, and let every held row r it sources be a hollow (sigma_r = +1) or a hill (sigma_r = -1) with the static kernel G_r of its line ((Delta^2 - kappa_r^2) a = -3 den sigma / num, [the well](#the-well); kappa = 0 for the massless row) and the divisor E_r, so the well at a Node is Phi_i = SUM_r sigma_r (M / E_r) SUM_j G_r,ij phi_j^2. To first order in Phi / Gamma the well line raises the one-Node rotation 2 cos omega by 4 g Phi / Gamma (cos omega by g (1 - p^2 / Gamma^2)), g = (den - num) / den, and the bonds' fall under the pace is of the pressure's own order and drops out at a width beyond the Link; there the fixed point of the binding row is a critical point on the sphere SUM phi_i^2 = 1 of

  F[phi] = (num / (3 den)) SUM over Links (phi_i - phi_j)^2 - (2 g / Gamma) SUM_r sigma_r (M / E_r) SUM_ij phi_i^2 G_r,ij phi_j^2,

the band's pressure less the wells' energy, each well counted once for the record being its own source (Hartree's form). **Proof**. The record is the top mode of Rule3's symmetric form at the paces, at first order **M**(Phi) = **M**_0 + (4 g / Gamma) diag(Phi), so it solves **M**(Phi[phi^2]) phi = 2 cos omega_b phi. The derivative of the wells' term at phi_j is 2 (4 g / Gamma) Phi_j phi_j, phi_j entering twice with G_r symmetric; the pressure's is 2 (2 cos omega_0 - **M**_0 phi)_j; so dF / dphi = -2 (**M**(Phi) phi - 2 cos omega_0 phi), and dF / dphi = 2 lambda phi on the sphere is the fixed point's own equation with 2 cos omega_b = 2 cos omega_0 - lambda, and conversely. **The dilation**. Let phi_R(x) = R^(-d / 2) phi(x / R) be the body dilated, d the GameBoard's dimension and R beyond the Link. The pressure is K / R^2 and each row's well energy W_r / R^(s_r), with s_r the row's scaling power at the body's size: s_r = d beyond the row's reach (the kernel a contact of weight 3 den_r / (6 (den_r - num_r)) per unit source, the rest inside a thick body), s_r = d - 2 within the reach or for the massless row (Poisson's 3 / (4 pi r) in a box; on a plane the logarithm, s = 0 in the sense of the limit, whose energy grows as 2 W per unit of ln R; on a chain the linear well, s = -1).

**Theorem** (the stable body). At a fixed point of the binding row of width R the virial 2 K = SUM_r sigma_r s_r W_r holds, and the second variation of F along the dilation is R^2 F''(R) = SUM_r sigma_r s_r (2 - s_r) W_r. A body is stable only where this sum is positive; it is a minimum of F where further the Hessian on the modes orthogonal to the dilation and the translations is positive.

**Proof**. F(R) = K / R^2 - SUM_r sigma_r W_r R^(-s_r); F'(1) = 0 is -2 K + SUM_r sigma_r s_r W_r = 0; F''(1) = 6 K - SUM_r sigma_r s_r (s_r + 1) W_r = SUM_r sigma_r (3 s_r - s_r^2 - s_r) W_r. Derrick's scaling, Pohozaev's identity on the GameBoard; at another R the same with W_r read there. **The signs**. s (2 - s) is +1 at s = 1, 0 at s = 2, -3 at s = 3: a hollow holds the body where its well falls slower than the pressure (s < 2) and breaks it where it falls faster (s > 2), and a hill does the opposite. From them, on the rows the law holds:

(a) **The hollow's dimension**. One hollow beyond its reach: on a chain (s = 1) every mass binds, at the width R = 2 K / W, falling as 1 / M; on a plane (s = 2) the dilation is flat and the well within the reach (the logarithm, +2 W) decides: above the mass at which the well's coefficient passes the pressure's the body stands at the reach's size, a window; in a box (s = 3) the one critical point is a maximum along the dilation, a saddle for every mass: the body disperses beyond it and collapses within it. The three GameBoards of the generator read so: on a chain of 60 Nodes 200 to 1,000 quanta stand, on a plane of 40 x 40 x 1 3,000 to 8,000, on a box of 48 x 24 x 24 29,500 to 30,000 alone, at the band's edge.

(b) **The massless row holds the body**. Gravity's Poisson well in a box has s = 1: with the pressure alone F = a / R^2 - c / R has the one critical point R = 2 a / c, a minimum for every mass (Pekar's body), its width falling as E_g / M. Beside it a hollow beyond its reach (s = 3) adds a barrier: on a Gaussian body F = a / R^2 - b / R^3 - c / R with a = num / (2 den), b = (2 g / Gamma) (M / E_b) (3 den_b / (6 (den_b - num_b))) / (2 pi)^(3 / 2) and c = (2 g / Gamma) (M / E_g) (3 / (4 pi)) sqrt(2 / pi); the critical points R = (a +- sqrt(a^2 - 3 b c)) / c, the wide one the minimum and the narrow one the saddle, the barrier to the collapse; none where 3 b c > a^2, the collapse. The minimum is a minimum exactly where W_g > 3 W_b there, R^2 > 3 (den_b / num_b) (E_g / E_b) / kappa_b^2, and the largest mass with a minimum is M_max = a sqrt(E_b E_g) / sqrt(3 b_1 c_1), b_1 and c_1 the coefficients at M / E = 1.

**Computed** (the script beside the paper): on the matter pair [4000, 6000] with the binding row [5760, 6000] (reach 2.02 Links) and gravity [1, 1] at Gamma = 6,000, M_max = 4,450 sqrt(E_b E_g); at the divisors 2 and 10 M_max is 19,900, 20,000 quanta stand at the edge (a^2 = 3 b c, the minimum and the barrier meeting at 8 Links) and 30,000 have no critical point at first order: the fixed point the generator reaches at 29,500 to 30,000 is the saturated saddle of the scaling's check (the width one Link, the well at the horizon's edge, (c)), and 32,000 and above collapse; at the binding's divisor 50, M_max is 99,600, the minimum for 30,000 lies at 10.3 Links and its barrier at 0.24, under the Link: gravity's body alone (10.5 Links at 30,000, 5.2 at 60,000), the widths the scaling's scan with the saturation reads as 11 and 4.8, and its collapse from 100,000. On the GameBoard the two kernels' constants at the widths 3 to 6 are 0.51 to 0.78 of the contact's and 0.92 to 0.84 of Poisson's, the reach's crossover and the box; the exponents are the theorem's.

(c) **The horizon ends a collapse**. Beyond first order the well line saturates (the rotation's gain 2 g (1 - (1 - Phi / Gamma)^2) is bounded by 2 g) and the Link's pace weakens the pressure by (1 - 2 Phi / Gamma)^2; neither makes a minimum, since both vanish together at the pace's floor: the collapse ends where a Link's pace reaches 0, Phi = Gamma / 2 on the Link, a frozen cluster of horizon Nodes, the guard's floor and no body of ordinary matter. (d) **The hill**. A hill beyond its own reach adds +3 W_h in a box: a hill whose reach is shorter than the body turns the saddle into a minimum where 3 W_h > 3 W_b - W_g; within its reach a hill is Coulomb-like and adds -W_h, so a hill longer than the body disperses it. HYPOTHESIS (the hill holds the body): a body stands as a stable extended fixed point where a held row read with the opposite sign (by q, like signs), of reach shorter than the hollow's, is held beside the hollow: below the hill's reach both are Coulomb-like and the hill, with the smaller divisor, forbids the collapse; between the two reaches the hollow binds; the body's size lies between the reaches. The rows the law holds for it: the polarisation [1, 2] read by q (1 / kappa = 0.49 Links, a hard core of one Link), the binding row (the hollow of reach two Links), gravity (the pull). A run of the generator with the third row decides it; it enters the universe's files by the owner's word alone.

(e) **The cooling**, a HYPOTHESIS under its own name (the owner's word of 2026-09-29, 04:40 Israel): a body above its minimum gives its excess away as quanta of the family it gives, one quantum per click of the giving at the universe's one T, each quantum carrying the body's rotation at the giving (the given record's clock the body's clock pair), and the body's count falls by one per quantum given; the giving lasts while the body's rotation lies above the rotation of the stable body theorem's minimum for its count and stops there, so a cold body is a body that has finished giving and sits at the minimum with nothing left to give, and matter stays matter: no quantum is made or lost, the total over the families changes only by the flux through the faces, and the quantum moves whole. The engine holds no such line: a body gives only from a declared stock, in its mode's cycle, never from its own excess, so a body laid off its minimum stays off it (wider disperses, narrower collapses), which is what the generator's runs read.

**The photon channel** is its local form, decided by the owner (2026-09-29, 04:45 Israel) and not yet built: a body that carries an emitter gives the quanta the count's line pushes out of it, across its edge, as quanta of the given family instead of quanta of its own, one for one at its clock, by the giving's own line at the edge Node; a body without an emitter sheds matter as before.

**The birth is a pair of clicks** (the owner's word, 2026-09-29, 07:2x Israel: if one leaves, one enters; Nature24's agreement 07:36): a Node beyond the body's set holding two quanta of the count's line gives one: one quantum is born as light through the outward Port with levels worth one quantum of form (the click's division act, the remainder kept at the Node) and one steps back into the body through the inward Port with its levels, in one act; a Node holding one quantum beyond the set gives nothing, and the count's line moves it as it moves any quantum, its remainder signed as [the count's line](#the-counts-line) has it (a hole where the current leaves a Node with no quantum, never a floor at 0).

**Computed** (the quanta model on the chain, 600 quanta, 30,000 intervals): a cloud twice too wide gives 9 percent and ends at the mode's width, where a birth at one quantum gives 57 percent and a body that keeps trimming; on the integer chain with the count's line as written a standing body gives nothing under the pair and the mode's two tail quanta under the one-quantum birth. Generic (any family with an emitter, the rows' pairs), vector (no root), local (the edge Node's outward flux of the count's line). A run decides it: a body laid wider or narrower than the theorem's width gives quanta of light while its width returns to the theorem's and its rotation to the minimum's, then gives no more; the clicks of the given light at a far detector count the quanta the body lost, and the total over the families is constant to the bit. It enters the universe's files and the engine by the owner's word alone.

**What is missing** for the theorem to close (**Derived**): (i) the Hessian on the modes orthogonal to the dilation and the translations: for the massless row alone it is positive at the ground state (the non-degeneracy of Choquard's ground state, a theorem of the continuum), for a set of rows it is read from the run; (ii) the functional beyond first order: the fixed point sources its wells from the form phi^2 while the bonds' weakening under the pace would need the sourcing from the Link's own form, so beyond first order there is no exact functional and the stability is the count's line's own dynamics; (iii) the finite GameBoard: Poisson's rest measured from the faces' zero sets a cloud threshold (30,000 on a box of 64^3 at the divisor 10), and a minimum wider than the GameBoard is no body of that GameBoard.

### The surplus leaves

**The free part**. At a Node of a body's record the local rotation is read from its three levels by the read act, 2 cos omega_i = (next_i + before_i) / now_i, and the local band from the Node's paces, its top (S_i + 2 SUM_a R_a,i) / w; in integers the Node is bound where now_i (next_i + before_i) w > now_i^2 (S_i + 2 SUM_a R_a,i) and free otherwise, from the Node and its six neighbours alone, no division. At a fixed point of the binding row every Node is bound (2 cos omega_b above the band's top at every Node, the mode's own relation); a cloud not at its fixed point has a free part, the Nodes whose rotation lies in the band, and the free part is a free record: it leaves at its band's group velocity by Rule3 as it stands, the count's line carries its quanta with it, and they end at a face or in another body (a cloud evaporates). A family sheds at its own band's group velocity, so a family whose pair lies near the exact band (m near 1: the bonds 2 m p^2 near 0) sheds nothing.

**The bound surplus does not leave by itself**: the part of a cloud's surplus held in its bound modes stays, since a bound mode is stationary and Rule3 reversible; a cloud twice too wide in a static well breathes about its minimum for 6,000 intervals with no settling, on a chain with open faces as on a closed one (**Computed**, the script beside the paper: the width swinging between 2.1 and 3.4 Links about the mode's 2.4, the form inside the body kept), so evaporation sheds the free part alone, and a body settles by the cooling of [the functional and the dilation](#the-functional-and-the-dilation) (e) alone.

**The held rows radiate**: a body whose form changes in time changes the source of every held row it sources, the row's record steps by Rule3 from that source, and the massless row's waves leave through the open faces at one Link per interval; a settled body sources a rest and radiates nothing.

**The mass defect is the form's fall at a kept count**. The line a_next = **M**(t) a_now - a_before with the paces changing in time changes the total form D = |a_now|^2 - <a_next, a_before> by exactly D(t + 1) - D(t) = <a_next, (**M**(t) - **M**(t + 1)) a_now> (**Theorem**, from the line by substitution; the identity holds to 10^-15 in the check), 0 at fixed paces (the conserved form) and negative where a well deepens, while the count's line, moved by the flux alone, keeps T c + r (**Computed**: a standing mode in a well deepening from 300 to 600 at Gamma = 6,000 loses 4.0 percent of its form with its count kept and the adiabatic invariant A^2 sin omega_b kept to 10^-5): the count is the quanta and the form sources the fields, so a body that binds is lighter in every field it sources by its binding and no lighter in quanta.

**The cooling's local trigger is the count's line's own current**: the form's flux through a body's edge Port, the current the count's line reads, is 0 at every interval for a standing mode and swings for a cloud at the beat of its bound modes, the difference of their rotations (**Computed**: at the edge Node the form's standard deviation over 3,000 intervals is 0 for the mode and 0.0065 against its mean 0.011 for the cloud twice too wide), so the photon channel of (e), the quanta the count's line pushes out across the edge given as the given family, gives at the beat and gives nothing at the fixed point without any knowledge of the minimum: "the giving stops there" is the current's own zero, local.

**The number of quanta a cloud gives to settle** (**Derived**, a blind expectation for the run of (e)): the law keeps the count and not an energy, so the quanta given are the part of the cloud outside the ground mode of the well its final count makes, the rest staying as the body; for a Gaussian cloud twice too wide in its own massless well (the final width falling as 1 / M') the fraction f that stays solves f = (4 f / (1 + 4 f^2))^d: 13 percent leave on a chain, 20 on a plane, 23 in a box, each quantum carrying the body's rotation; the brackets: at most 1 - (4 / 5)^d for a fixed well (20, 36 and 49 percent), at least the energy's account M c^2 / (4 a) / (2 sin omega_b omega_b) of (b), 76 quanta of 30,000 under gravity at the divisor 10, a quarter of a percent; the far detector's clicks count them and the body's count falls by the same; a family that gives nothing (no emitter) and sheds nothing (a flat band) stays a cloud, dark.

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
so that the record's conserved form equals c T, c the body's count and
T the universe's quantum action: the body's record carries exactly its
quanta's action, its amplitude follows, and no bound on a level is
written (a level beyond the integer width is the engine's refusal).

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
10^-6; the final scale comes from c T.

(g) **The field at rest, the start of a world**. The generator iterates the held family's own
line to rest first, at the pair of the family's row, as the hold's source makes it: the
count over the divisor E_s added at the body's Nodes each pass, the homogeneous line
outside. From nothing the level at every Node is num S_6(a) div (6 den), plus half the
source at the body's Nodes (6 den a = num S_6(a) + 3 den sigma, sigma = w M div E_s: the
source enters once an interval at one level), by the division act on a fine unit derived
from the width; the map is monotone, so the levels rise to a fixed point, its first repeat;
the levels are Poisson's rest with the sources within one unit, and the mode is solved on
that content: generic (one primitive, the row's pair and divisor, no family name), vector
(the division act alone, no root, no float) and local (the six reads and the source's load).
A world starts from the field at rest, never from zeros, whose transient rings. Under [1, 1]
between periodic faces the sources have no rest (the periodic Poisson problem at kappa = 0),
and the world is refused by name; between open faces the harmonic well of the sources.

**The start**. The loop writes every held family at the load at its rest, by
one folder found by its name, once before the first interval and never in
it, the level and its remainder together (the fixed point of the division act is a pair: with the rounded rest a and its line's residual rho = num SUM_6 a - 6 den a, the remainder r_0 is one from which the first step returns a, any r_0 with 0 <= rho + r_0 < w, the half wall the division's unbiased origin for every Node whose |rho| is below it, and the hold's carries stand spread over the body's Nodes so the source's current is even from the first interval; a remainder 0 by fiat is no rest, the first step kicks every Node whose rho is negative, Newton's reading of 2026-09-28): on a chain (one layer on two axes) in one pass in integers, the
tridiagonal line with the sources on its right side; on a box a guess of the line's solver refined on the exact
residual R and certified in whole integers: the exit-time field T of the
same line, with its own exact residual rho, bounds the inverse, ||A^-1|| <=
||T|| / (6 den x scale - ||rho||), so the field stands within ||A^-1|| ||R||
of the exact rest, and where every free Node is farther than that from a
half the levels are the rest's nearest integers; a Node nearer takes a
finer unit once, then rounds up, the half's own side. Generic (the
row's pair and divisor), vector (the levels by the division act, the certificate in
integers; the guess is no value of the law), local (the six reads and the
source); the cost is the load's.

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
one Link per interval, each Node updating on receipt under the same rule.
The one exception is the click: a record ends at once, whole, at the
detector. 4. The causal speed is one Link per interval, built in; every
other speed is a rational, a count of Links over a count of intervals. 5.
Every physical calculation is on bounded integers; there is no float, no
root and no draw in the law; a Node keeps only the law's own numbers: each
record's two levels and its remainder, the family's pair and the Node clock
from the content there. 6. A measurement is a detector's click, an action of
the law on the state: the record ends at the detector and the detector's own
record changes. Only a click is compared with nature or pinned as an
expectation; displays and the host's readings read state and write nothing.
7. The Inside is the GameBoard, where no one measures; the Outside is the
detectors and their clicks, the only thing claimed to represent nature.

### The constants

The speed of light is one Link per interval. The quantum of action is
one click, its energy the quantum's norm T of its family. Newton's
constant is not declared: a body of energy count s makes the level c(r)
= s times the reference flux over E_s over the distance r in Links (the
hold's row: the count enters the field's line over the row's divisor E_s),
and the level slows the clock by the potential Phi = -c / Gamma, so

  G = (the reference flux) / (Gamma E_s) per unit of energy count,

with the reference flux a number of the GameBoard's geometry (about 1.4 for
a cube of side 3) and the divisor E_s the energy unit setting the mass of one unit of level.
A world at a smaller Gamma has stronger gravity per unit of content; the
ratios between rows carry G once and cancel it. The quantum of distance is
the Link, of time the interval; nothing between two Nodes or two intervals
is observed. The potential at a body's Nodes changes by G per unit of energy
count and never by less: the quantum of gravity is the click.

**The three free numbers and their bounds** (the owner's question, 2026-09-28, 09:30 Israel): the rule's own universe ([the families from the rule](#the-line), the hypothesis under its own name) carries none of the three; the universe of record carries all three, and its three are these. E_s of gravity is fixed by no line of the law, as nature's G is fixed by none (Rule3 is linear and its form's scale is free: one count writes one level over E_s at any E_s; "the well is the count", the polarisation's divisor 1, is the bound charge's own family writing itself and no relation for gravity); it is free, and its bound is the law's and no person's: at every Node of every body the pace stays positive, count x (1 + K / E_s) < Gamma with K the hold's kernel summed over the body (about 51 for a body wider than the reach), so E_s > K x count / (Gamma - count) at the world's heaviest Node (the loader's guard is this line), and the reading's resolution bounds it above (a fall of one Link within the run, the bending's centroid above its draw); a relation that would fix it (E_s = K Gamma, a body at the pace's edge writing one level per count) is a hypothesis under its own name. The charge's E_s is free as alpha is, bounded below by the same pace at the bound charge's Nodes and by the train (one quantum at least one period, de Broglie's reading 4 x 10^4) and read by the train's N_q. The matter pair is free as the mass is, bounded by the band: den > num, and the reach cosh kappa = 3 den / num - 2 fitting the body's width.

### The rows against nature

Each row is a detector's click on a declared world, read blind, with
U_b = c_b / Gamma the potential at the point named (the clock's shift per level, the clock's pace); the bands are
the rounding's, one Node of centroid or one interval, and the draw's
where counts are read.

(a) **The redshift**: two clocks of one family at the levels c_1 and c_2; the ratio of their tick intervals is the root of (1 - 2 U_1 + 2 U_1^2) / (1 - 2 U_2 + 2 U_2^2), 1 - (U_1 - U_2) to first order.
(b) **The bending**: a beam past a body at closest distance b, the centroid at a receiver L Links beyond shifted by 4 U_b L toward the body.
(c) **The delay**: a round trip past the body, delayed by 4 U_b times the path's length within the well's reach.
(d) **The perihelion**: an orbiting emitter at semi-axis a and eccentricity e advances 6 pi U_p per orbit with U_p the potential at a (1 - e^2).
(e) **The moving clock**: a body at velocity v = n / W (its phase k per Link an exact pair of the file) has its tick lengthened by the dispersion of its own bound band: the tick's factor f = Omega(k) / omega_0 with Omega(k) = omega(k) - k omega'(k) the rotation at the moving centre (the phase rate less k times the group velocity) and omega(k) = omega_0 + Delta (1 - cos k) the body's bound band, omega_0 its rest rotation and Delta its packet's top velocity (at a quarter turn per Link), both the generator's from the file's counts and pair, no key; to the second order f = sqrt(1 - v^2 / c_b^2) with c_b^2 = Delta omega_0, Lorentz's factor at the body's own light speed; read as the mean of the front and back click periods P_v (1 -/+ v / u) at two resting detectors (u the light's group velocity), P_rest / P_v = f, the GameBoard's own term inside the rows' bands.
(f) **The charge**: like signs a hill, unlike a hollow; a reader of charge q reads + q Lambda d in its pace and - q Lambda (**n** . **A**) div W on its vector part, so like charges moving together repel less.
(g) **The two slits**: a giving body, a wall body with two openings d Links apart (its count above the mirror's of [the paces](#the-paces)) and a screen body L Links beyond carrying the sets in strips: the strips' shares of the clicks are the openings' interference at lambda_q, cos^2 (pi d y / (lambda_q L)) at the height y under one opening's envelope, the bright strips lambda_q L / d apart, to the first order in the GameBoard's anisotropy; the exact shares are the two arms' phases **k** . **r** with the wavevector set by cos k_x + cos k_y + cos k_z = 3 cos omega den / num at the record's rotation, a term that at lambda_q = 4 Links on d = 16 and L = 97 moves the second bright pair from 6 to 8.5 strips of 4 Nodes and falls below one strip at lambda_q = 16; the record's rows show it splitting at the openings and its parts meeting on the screen (GAMEBOARD).
(h) BELL: two labels of one giving, each clicking alone at its own end; the pair's giving, the turn at each end and the labels' clicks are open under the count's line (the old click and its rows are deleted, the model owner's word of 2026-09-29 on #1495, finding 10); the blind expectation stands: E(a, b) = cos 2(a - b), each side's marginal one half at every setting (no signalling), and S at the settings 0, pi / 4, pi / 8, 3 pi / 8 is 2 sqrt 2 = 2.83, nature's number; the pairs are the host's coincidence reading.
(i) **The fall**: a light body of D Links across, L Links from a heavy body of count c per Node on an open chain, under the hold as a sum ((g)): the held field's rest is the tent Delta^2 a = -3 sigma at the heavy body's Nodes (sigma = w c / E_s per Node per interval on [1, 1]), linear outside with the slope half the body's total source, 0 beyond the open faces; the light body's acceleration a = Delta x |d omega_0 / d c| x |c_+ - c_-| / D toward the heavy body (the feed's row, derived: Delta its mode's top velocity, d omega_0 / d c its redshift per level, c_+ and c_- the level at its two faces), its record's current growing by a x 3 Q M per interval, the fall of L Links in t = sqrt(2 L / a) intervals at the speed a t at the touch; the detector on the falling body reads the heavy body's records given at its mode's period, their number before the touch the givings whose flight at the group velocity ends before t; two light bodies of different shape in one tent read the equivalence principle, alike within the unit or a finding by name.
(j) **De Broglie's fringes**: (g) with a matter record given by a body of a lighter family: a giver of rotation omega_b radiates only a family whose free band holds it, num / (3 den) <= cos omega_b <= num / den (a bound mode's rotation lies above its own family's band, so no body radiates its own family); the record's wave number is the band's, cos omega_b = (num / (3 den)) (2 + cos k), its group velocity v = (num / (3 den)) sin k / sin omega_b, and to the second order k = omega_b v / c_m^2 with c_m^2 = omega_0 / (3 tan omega_0) the family's own light speed (0.2508 on [800, 1200]): de Broglie's law with the rest rotation as the mass; the strips' shares are (g)'s at lambda = 2 pi / k.
(k) **The two-qubit computer**: one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate (the phase (k_in - k) l over a depth l, [the paces](#the-paces)); two qubits are the two labels of one giving, whose clicks paired by the host's window are (h)'s E; a controlled gate needs one record to turn another's phase, which the acts alone cannot (the theorem of the four acts) and a read can only through the pace: a target family reading the control family with the weight g_c has its pace wobble with the control's level, the first order averaging out over the control's rotation and the second order a hill of g_c^2 A^2 / (4 Gamma) over the overlap (A the control's amplitude), so the blind expectation is (h)'s E with that small phase, and a controlled phase of order one is a hypothesis under its own name, not in the law.
(l) MACH-ZEHNDER: a giving body, a splitter (a body of a count inside the record's band, one Node deep along the beam, its reflected share s the slab's from [the paces](#the-paces), one half at the count found by bisection), a mirror on each arm (a count above the mirror's), a second splitter and two sets: the shares of the clicks are 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = k (L_1 - L_2) the arms' phase difference, so at equal arms and s = 1 / 2 every click is at the cross exit; the record's rows show the two arms (GAMEBOARD).
(m) **The round trip**: a giver receding at v from a mirror at rest, its set on itself, giving every P intervals: the forward record's wave number solves Omega(k) + k v = omega_b (the giver's rotation seen from the GameBoard), the returned record has the same rotation and wave number, and the returned clicks come every P (u + v) / (u - v) intervals with u the group velocity at that k: the two-way Doppler ratio with the light's group velocity in place of c.
(n) SAGNAC: a giver with its set on itself moving at v along a ring of N Links (a periodic chain): one record's two arms return after N / (u + v) and N / (u - v) intervals, u the light's group velocity, so the set's clicks fall in two groups whose means differ by 2 N v / (u^2 - v^2), which is 4 A omega / u^2 for the ring's area A and angular speed omega to the first order in v / u (each arm's Doppler shift of k the second), and coincide at rest; a giver at rest on the ring reads one group at N / u.
(o) **The moving mass**: a body giving a lighter matter family (a row whose band holds the giver's rotation, (j)) toward a set L Links away: the record's quanta move at the count's line's velocity v = (num / (3 den)) sin k / sin omega_b, the set's clicks come L / v intervals after each giving, and the giver's momentum moves by 3 Q_unit P_body (L div lambda_q) div L per quantum given (the recoil); the record's rows show one packet at v (GAMEBOARD).
(p) **The medium's delay**: a light record through a window body of depth l (a count below the mirror's of [the paces](#the-paces)) is slowed inside to v_in = (p / Gamma)^2 sin k_in / (3 sin omega) with 1 - cos k_in = (Gamma / p)^2 (1 - cos k), the index v_g / v_in, and a set beyond reads the passage longer by l (1 / v_in - 1 / v_g), a round trip by twice that; through a window moving at w along the beam the record's wave number inside is matched at the moving face, omega - k w = omega_in - k_in w, and its speed inside is the band's group velocity at that k_in, not v_in + w; Fresnel's drag w (1 - v_in^2 / v_g^2) is nature's number beside it.
(q) **Dark matter**: a heavy body in a box and a light test body at the distance r on a circular orbit (v^2 = r a): the held field's rest outside the body is Laplace's ([1, 1]), c(r) = s x the reference flux / r falling to the faces' 0 (the open faces' images steepen it near a face), so a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D falls as 1 / r^2 and v^2 as 1 / r, Kepler's fall-off, under the hold's write as a load and as a sum alike (the source inside, Laplace outside); the DETECTOR reads the orbit's period in the waits' phase as in (d); a flat v(r) is the finding that names a missing law.
(r) **Dark energy**: a giver and two far sets on a long periodic chain over 10^5 intervals: Rule3 is translation-invariant, so a free record keeps its wave number and rotation exactly and the sets' mean click interval stays the giving's period P at every distance, the record's rows widening by the dispersion as the root of t while its count does not move (GAMEBOARD), the rounding's walk at most one unit of level per Node per interval; a mean interval growing with the distance is the finding.

A row outside its band is a finding: it names the missing law or the
defect, and no body's numbers are patched to meet it.

## What is open

1. Whether a body at rest jitters when its current's swing reaches T / 2: on sixteen Nodes the swing over 400 intervals is one percent of T / 2.
2. The self-source's cubic term: not in the engine, the line is the squares' sum alone.
3. The equivalence principle holds to the band's own shape: Delta x 2 tan (omega_0 / 2) differs by a tenth across the bound bodies of the clock's table; the fall with two light bodies reads the rest.
4. The two thirds' charges: a third with the sign q reads a third, and the composite read modulo a turn identifies -1 / 3 with +2 / 3, but no line gives the up third 2 / 3 and the down third 1 / 3.
5. The three generations: a hypothesis under its own name, the three ranks of the exact band [-1, 2]; no line gives a rank a mass.
6. The exact band [0, 1] of the period 4: a family that never clicks and carries no colour, unnamed in nature here.
7. The stable body theorem's Hessian beyond the dilation for a set of held rows, and the functional beyond first order in the well over Gamma ([the functional and the dilation](#the-functional-and-the-dilation)); whether the hill holds the body and whether the cooling brings a body to it ((e)) are a run's findings.
8. **The count is read once** against the graph of the reads: with gravity's [1, 1] and the bound charge's [1, 2] both holding the content at the divisor 1, a matter record's pace reads the count twice and the horizon falls to Gamma div 4; which row is the count's one reader in the rule's own universe.
9. **The mass is the count** against a quantum weighing its rotation: whether nature's m_p / m_e is the counts' ratio c_p / 1 or the energies' ratio c_p omega_b / omega_e.
