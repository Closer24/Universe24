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
GameBoard, one integer per Node per level, with a remainder per Node; a
family with two levels per Node holds a **pair** (re, im) at each Node.
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
the action of one quantum of any family, a unit as Gamma is; the momentum unit Q_unit; the twist table ([the transport](#the-transport));
`least_residues`, the fewest remainder values the pair of a giving family must give at its giving Node, so that the ladder's residue u is spread over them (a pair with fewer is refused by name: the number is the file's, the rule the law's).

THE FAMILIES FROM THE RULE (the owner's question, 2026-09-28, 09:13 Israel: how are the families derived from Rule3): a family is a band of the one rule and not a declaration, and its row holds nothing the rule and the geometry fix. Its pair [num, den], cos omega_0 = num / den: the vacuum's band [1, 1] (the rule's own massless line) and the exact band [1, 2] (2 cos omega_0 = 1, the period 6, one of the three exact rotations the rule allows, which never click) are the rule's; the matter pair (the word "body", every body its own) is the one free physical pair. THE MASS IS ONE INTEGER (the owner, 2026-09-28, 10:46 Israel): every pair is written over the GameBoard's one denominator Gamma, cos omega_0 = m / Gamma, the file holding the numerator m alone: light m = Gamma, the exact band m = Gamma div 2 (Gamma even), matter its one integer, 6,667 in the universe of record (the nearest to 2 / 3: cos omega_0 0.666667 -> 0.6667, omega_0 0.841069 -> 0.841024, the reach cosh kappa 2.5 -> 2.49978, every number written before a run within 5 x 10^-5 of itself, the carried division the same act at the finer wall); THE WALL IS ONE (Cheshbon's correction, 2026-09-28, 14:12 Israel, on the de Broglie Experimenter's finding that a pair reduced to lowest terms shrinks the wall 4,000-fold, lifts A to 1.3 x 10^9 and drives the count's line past the width): the wall is w = 6 Gamma^3 for every family, the pair enters the coefficients as the file writes it, m over Gamma (R_a = 2 m p_a^2, the rest term 12 (Gamma - m) p_0^2), and a reduction to lowest terms is a reading and never the loader's act, so every family's remainder has the one resolution and the exact bands leave none in any form (S + 6 R = 6 Gamma^3 exactly); so the width's amplitude unit falls (A = 512,409 in the universe of record against 4,270,079 at [800, 1200], the pair (level, remainder) carrying the same bits) and T is set so that every record at c T stays under A (T at most 9 x 10^11 for the givers of record; 5 x 10^11 proposed). THE FINAL UNIFICATION (the owner, 2026-09-28, 10:53 Israel): the three of Rule3 is the three axes; the three axes give the three tensor ranks, 1, 3 and 6, the symmetric parts under the 48, and no fourth; every family is one rank and carries two keys, its pair and its divisor, of which the rule fixes at least one: a field that every family reads into its pace is on the pace's own band [1, 1] and its divisor is free (the vector's alpha, the tensor's G), a quantized scalar holds nothing, has no divisor, and its pair is free (the mass m), and an exact band ([1, 2], the period 6) has both fixed, the pair by the rule and the divisor 1 by the well being the count, so it carries none; thus each rank carries one free number and no more, the scalar the mass, the vector alpha, the tensor G: the count three is derived from the three axes, the values free as nature's. The crack, named: a second massive scalar family, a second mass at rank 1, the rule does not forbid; the universe of record declares one, and nature's spectrum of masses is the open row under this line. Its parts are the tensor rank of what writes it (1 the count; [1, 3] the count and the current; [1, 3, 6] the count, the current and the current's tensor), its phase is 2 where it carries quanta (a current, [the count's line](#the-counts-line), the clicks) and 1 where it never clicks: the highest rank, which every family writes and which reads none, and the exact band, whose rotation leaves no remainder (no remainder, no click), so two real fields; its clicks are that same bit. Its reads are the graph of the ranks (each family reads the ranks above it) with the one weight 1 (reciprocity, [a family's write](#the-primitives)), the reader's own twist and by its own count with the sign of the body that holds it, the same word as the read family's held count. Its held writer writes the count with the body's sign and the dipole of the body's spin with the divisor equal to its phase (1 for the real field, 2 for a pair: Dirac's 2); the row's divisor E_s is one of the two free numbers of [the constants](#the-constants) (gravity's, G; the charge's, alpha). The action of one quantum is T, the universe's one integer for every family: Rule3 is linear and its form's scale is free, so no line of Rule3 fixes T; it is a unit, declared once, and no family, no body and no emitter declares its own (the owner, 2026-09-28). So the files hold Gamma, T, the matter pair and the two divisors, and nothing else of physics: `quantum` (1, the unit T), `sign` (0), `self_source` (0: the source is D_i div T), `clock` (the mode's `wavelength`), `Lambda` (1), every `weight` (1), `twist` ("own") and the held `factors` (the linearised field's 4 and 2, nature's numbers written by hand and no rule's) leave the files, and `spins_step` leaves with the spin's step below.

THE EXACT BANDS (the owner's word, 2026-09-28, 11:44 Israel: the quarks are there for a reason and are almost never seen; the algebra on one Node, 12:03 Israel): the line of one Node at rest, a_next = 2 cos omega_0 a_now - a_before, is exact in integers only where 2 cos omega_0 is an integer, so the rule carries exactly three exact rotations, 2 cos omega_0 = 1, 0 and -1, the periods 6, 4 and 3, the pairs [1, 2], [0, 1] and [-1, 2]; a record on an exact band at rest at the vacuum's pace leaves no remainder in its rest rotation, so its quanta stand exactly at every Node, it gives nothing and never decays alone, and stable matter is built on an exact band; everything else of it clicks as every family's does, its packets (a wave number is no integer rotation), its Nodes in a well (2 cos omega = 2 - (p_0 / Gamma)^2 there) and its reads, so an exact band is seen exactly when it is moved or probed and only then (the owner's word, 2026-09-28, 12:25 Israel: it does click). THE EXACT BANDS ARE EXACT ONLY IN THE VACUUM (Cheshbon's correction, 2026-09-28, 13:09 Israel): at a Node of pace p_0 the band's rest rotation is 2 cos omega = 2 - 2 (den - num) (p_0 / Gamma)^2, an integer at p_0 = Gamma alone, so a record on an exact band inside a well, its own or another's, leaves a remainder and clicks like every family's: the third's three phases sum not to 0 but to a share of a record's level that grows with the well, 0.015 at a level 30 of 12,000, 0.148 at 300, 1.2 at the self-binding edge, and white matter stands only where the well at its Nodes is small against Gamma: under the divisor 1 (the well is the count) no white pixel exists and the third and the polarisation are messages of the vacuum, while under a divisor E_s of the universe of record a white body of thousands of quanta is white to 10^-5; so white matter requires a divisor far above 1, and the smallness of the charge's coupling is a condition of the quarks' whiteness before it is a distance of nature from the rule (the first line under THE THREE DISTANCES ARE THE RULE'S, below). The first is the bound charge, the polarisation, never seen free. THE THIRD (a hypothesis under its own name: the quarks and the strong force): a record on [-1, 2] turns a third per interval; three thirds in the phases 0, 2 pi / 3 and 4 pi / 3 (three consecutive states of one record) sum to zero in their linear write at every interval while their quanta add and stand constant (the white body), and the whiteness is read at every Node from its own three levels, the click's local language; when a third moves off its body every Node between the two carries the three levels' sum uncancelled, a record of the third's own count per Node, so the tube between them costs the third's count per Link and its cost is linear in the length (the tension is the count, no number: the strong force's line), its remainders cross T and click, each click a quantum moved whole along the tally's axis sigma_a, which lies along the tube (the click's vector converges to the direction of the missing third: the string pulls), and when the tube's quanta reach a third's worth the click converts them (THE CONVERSION below) into a new pair of thirds, the string breaks into mesons and a third is never free: confinement is that theorem, and the width's refusal of a lone third is only the engine's shadow of it; the three colours are the three phases, a probe shorter than the body clicks at one Node and reads one phase, a third's charge reads a third, the sense of a third is the sign q of its read, and a meson is two thirds of opposite sign. THE CONVERSION (a hypothesis under its own name: the weak force): a click that takes a quantum of one family and gives it as quanta of others, the rotations adding as the crystal's row has it, is the whole weak interaction, one Node's act, no field and no massive vector, and no family's row declares anything for it. The band [0, 1], the charges 2 / 3 and 1 / 3 of the two thirds, and the three generations are open rows under this line ([what is open](#what-is-open)).
THE RULE'S OWN UNIVERSE, a hypothesis under its own name (the owner's word, 2026-09-28, 12:08 Israel: the hypothesis enters the finish line now): a universe whose every number is the rule's. Its pairs are the integers 1, 2 and 3 of the three exact rotations and the three axes: [1, 1] the vacuum's band, on which the two real fields stand, [1, 2] the exact band, [2, 3] the matter pair, cos omega_0 = 2 / 3, the first pair past the exact bands, which the universe of record approximates by 6,667 over 10^4, and [-1, 2] the third; its divisors are 1 (the well is the count: every held level is the count itself, so a count near Gamma div 2 is a horizon, the pace 0, and no body's Node exceeds it, the maximal coupling); Gamma is a multiple of 6 so that every pair is exact over it (12,000: m = 12,000, 6,000, 8,000 and -6,000); T is the one unit and cancels in every reading. So it carries zero free numbers, no G, no alpha and no m, against the universe of record's three, and it is the same rule and the same engine on another file, the sixth first look beside the five, a universe file of its own beside the universe of record and not in its place. A PAIR'S NUMERATOR MAY BE NEGATIVE: the third's R_a = 2 num p_a^2 is negative, S is what the line makes it, the band is the mirror of [1, 2] (2 cos omega inside [-1, 1] at every wave number and every pace at or below Gamma, the edge P = isqrt(2 den Gamma^2 div (den + num)) = 2 Gamma, the rest term 12 (den - num) p_0^2 = 36 p_0^2), and the loader admits a pair with den > |num| as a massive kind and refuses den <= |num| and den = 0 by name; nothing of Rule3 changes. THE THREE COLOURS ARE THREE INTERVAL STATES: a third's record at rest steps (now, before) -> (-now - before, now) with the period 3, so its three phases are three bodies whose two levels are three consecutive states of one record (7, -10, 3 on one Node: each interval's three levels sum to 0 exactly, the quanta 7^2 + 10^2 + 3^2 - 7 (-10) - (-10) 3 - 3 x 7 constant), the generator writes two levels and no new key; the first look of the white body is on the rule's own universe file, its blind expectation there the three phases' sum 1.2 of a level at the edge and not 0 (a finding and not whiteness: THE EXACT BANDS ARE EXACT ONLY IN THE VACUUM), and no look is on the universe of record; in the rule's own universe the matter is the pixels of [2, 3] and the light, and the third and the polarisation are messages, exact in the vacuum and clicking in every well. A THIRD DOES NOT BIND ITSELF: its read is negative, so its own well pushes its rest rotation up into the vacuum's band (2 cos omega = 0.31 at a count 3,000 of 12,000, inside [-1, 1]) and the record leaks; a record of the third at one Node is a packet of every wave number and disperses in every universe, its uniform mode alone exact; so one family on [-1, 2] holds no standing body, no white body and no tube, and THE THIRD's white body, tube and tension stand only with the colours as three families of one pair under one constraint of whiteness, THE COLOURS ARE THE THREE AXES (the Closer's line, 2026-09-28, 13:42 Israel, on the owner's word that the quarks close today; Cheshbon's derivation 13:46): the white body is a pixel of [2, 3]; the count's line carries a tally per axis, so the three colours are the three tallies sigma_x, sigma_y, sigma_z, and whiteness is their balance at rest (an isotropic tail carries no net current through any Port); under a pull the clicks are biased along one axis at the rate omega_b e^(-kappa d) per interval, which falls with the distance and gives no linear potential: the force between two pixels is short-ranged, its range 1 / kappa (2.2 Links at 3,000 of 12,000; the click's reach 18 Links at T = 1), the nuclear force between nucleons and no confinement inside a pixel, which has no inside; the smallest bound fraction of a horizon pixel is 0.2255 / (1 / 2) = 0.451, so a third of a pixel never binds and disperses (confinement is the edge, no line of its own) while two thirds bind, and a meson is two fractions above 0.451 of opposite q within the tail's reach; the charges 2 / 3 and 1 / 3 as numbers stay open. THE COLOURS ARE THREE FAMILIES UNDER ONE CONSTRAINT stays named as the alternative with no first look. THE BOUND BODY IS ONE NODE (the owner's word, 2026-09-28, 12:30 Israel: every bound body fits in one Node, and that is what pixelates everything): under the divisor 1 a body that binds itself at rest is one Node, its count c in [0.2255 Gamma, Gamma div 2), the lower edge where the one-Node well first holds a rotation below the vacuum's band (the three-dimensional Green's function of the six Ports, a pure number of the rule; below it the record disperses), the upper the horizon (the pace 0, the Node reads nothing and freezes); its record is the one-Node line at its bound rotation omega_b(c) (0.841 at the edge, 0.464 at 5,412 of 12,000) and its tail outside is the well, evanescent by kappa = acosh((9 / 2) cos omega_b - 2) per Link (0.45 at 3,000, 1.27 at 5,000: the tail ends within three Links); its mode carries the count through the form, D = now^2 - next x before = b^2 (2 - 2 cos omega_b) at rest with both levels b, so a pixel of c quanta loads with b = isqrt(c T den div (2 den - a)) for the clock pair [a, den] of 2 cos omega_b (69 at 3,000, 97 at 4,000, 139 at 5,000 of 12,000 at T = 1; isqrt(c) alone loads 1,812 quanta for 3,000, under every edge) and its tail as b t^(|dx| + |dy| + |dz|) rounded with t = e^(-kappa) (0.640 at 3,000, 0.362 at 4,000, 0.281 at 5,000); on an engine where the level enters the Link once (before the conformal term) the same Green's function puts the edge at 0.345 Gamma (4,136 of 12,000) with kappa 0.63 at 5,000 and 0.98 at 6,000, the number of that engine's first looks; a body of more quanta than Gamma div 2 is a cluster of such Nodes, each a bound body, clicking to one another. So between bound bodies there is nothing but the click and the band [1, 1]: the record does not leave its Node (kappa > 0), a quantum crosses a Link whole at a click and nothing else does ([the count's line](#the-counts-line)), the overlap of two tails within reach is read by the count's line and clicks (the exchange), and light and the two real fields carry the rest; a Node is a bound body or vacuum; the bound body keeps its record on the GameBoard and Rule3 steps it at its Node and along its tail as it steps every record (the one-Node line is the reading of its rotation, not a step of its own: with the six reads returning the Node's own level the line gives the Node's rest rotation, 1.05 at 3,000 of 12,000 by the pre-conformal coefficients and 0.62 by the conformal, and not the bound omega_b = 0.81 that the tail fixes; the tail is 0.64 of the level one Link away at 3,000 and carries the exchange and the fall), so the engine of the rule's universe is the engine of record on another file, and a step of the pixel alone is an optimisation for the day the tail is derived in integers. In the universe of record no body binds itself (the well is M div E_s, the edge M >= 0.2255 Gamma E_s), so its bodies are declared modes and the theorem does not reach them. THE UNIVERSE IS BOUND, the unification's assumption and no theorem (the owner's word, 2026-09-28, 12:37 Israel): every body is bound, no body is free, and a record that is in no bound body is a message between two clicks, the one that gave it and the one that will take it (a matter record below the edge cannot be a body and disperses; light never binds, its band's bottom is 0); a fall is the bias of a bound body's clicks, its tail longer toward the well (the local band lower there, kappa smaller), so the remainder crosses T first on that side; a click on a record with a partner label is entanglement and a click on a record with none is a measurement, and Bell's S reads that and nothing else; the assumption removes no number, it names the universe that has none, and where it fails (the universe of record, nature) the two distances stay. THE CLICK JOINS AND PARTS (the owner's word, 2026-09-28, 12:43 Israel: bound bodies join or part, and that is by clicks; the join is the non-local act): two clusters whose tails overlap (within 1 / kappa, three Links) read each other by the count's line and click, the tail biased toward the deeper (omega_b falls with c), so the smaller gives quantum by quantum to the larger until its count falls under the edge and it dissolves into messages the larger takes, the join a run of clicks whose last ends the smaller's record, one Node where c_1 + c_2 < Gamma div 2 and a cluster of two at the horizon otherwise, one record for the joined cluster; a cluster parts where a Node's count falls under the edge (it dissolves) or where two tails cease to overlap: the tail's e-fold is 1 / kappa (about two Links at 3,000 of 12,000) but the click's reach is where the Link's current a_1 a_2 e^(-kappa d) falls under T, d = ln(a_1 a_2 / T) / kappa, about 18 Links at T = 1 for two pixels of 3,000, and the transfer between two pixels runs at about omega_b e^(-kappa d) per interval (0.33 at two Links, 0.09 at five): beyond the reach no click, parted, and a taker at the horizon overflows into a neighbour inside its own well (the real field 0.34 of the count one Link away) so the cluster grows a Node per click (a body never splits into three equal pixels: 2 x 0.2255 < 1 / 2 < 3 x 0.2255); the one record opening for the joined cluster and closing everywhere for the parted one is THE HALF QUANTUM's one non-local act and there is no other; the conversion changes the family. THE OBSERVER IS A CLUSTER: a Node reads six Ports and a cluster's record is what its Nodes carry, so inside a cluster everything is seen (a GameBoard reading is the local language of its own record) and beyond its tail only a whole quantum arrives, a click. THE TREE, the closure: the root is THE LAW IN ONE LINE; from it alone the exact bands, the colours, the tube's linear cost, the edge P, entanglement as the click and the observer as a cluster are derived; with the named assumption the pairs from 1, 2 and 3 (den the three axes) the matter pair [2, 3] and the crack [1, 3]; with the named assumption the divisors 1 (the rule's universe) the bound body as one Node with the edge 0.2255, the horizon, the tail, the cluster, and the click that remakes, joins and parts; THE UNIVERSE IS BOUND is an assumption and THE CONVERSION a hypothesis; so the algebra is closed on one root, two named assumptions, one assumption of the universe and one hypothesis, with zero numbers, and is not closed toward nature by name: the three distances alpha = 1 / 137.036, m_e / m_P and m_p / m_e (the rule's universe has one pixel mass scale, its counts within [0.2255, 1 / 2] Gamma), the charges 2 / 3 and 1 / 3, the generations and the band [0, 1]; THE THREE DISTANCES ARE THE RULE'S is the hypothesis under its own name that the three are derived, and its first two lines stand: a divisor far above 1 is what white matter needs; and ONE QUANTUM PER WINDOW bounds the charge's divisor from below: a giver's window closes when the outward flux reaches T, the flux of the written wave is a_light^2 sin omega sin k per outer Link per interval (0.745 a_light^2 at lambda = 4) and the window is one interval at least, so a given record carries more quanta than the stock loses unless 0.745 a_light^2 <= T, that is E_s >= g M a_body sqrt(0.745 / T) with the write g q M a_body div E_s; under the divisor 1 a pixel of 4,000 at T = 1 gives 4.7 x 10^10 quanta per interval for one of its stock, so the rule's own universe carries E_s(charge) = 0.86 (Gamma div 2)^(3 / 2), the bound at the horizon pixel (4.0 x 10^5 at Gamma = 12,000), derived from Gamma and no free number, while E_s(gravity) = 1 stands (the real field gives nothing); in the universe of record the same bound reads 32,300 against the file's 40,000. THE ALGEBRA OF CLUSTERS (the owner's word, 2026-09-28, 14:40 Israel: the algebra is closed, so the five looks must close, and the rule's universe is a universe of clusters alone, whose algebra may differ a little because nothing else is there; Cheshbon's section, 14:55, one closed derivation from the root on the one assumption "only clusters", with the Nature24 session's lines of 14:44): (1) THE NODE HOLDS ITS COUNT: a Node holds one integer, its count c, and nothing else; THE COUNT IS THE RECORD'S FORM: in a universe of clusters the count is no level beside the record, c = D div T at the Node with the remainder D mod T, D = now^2 - next x before the record's form there, the click is that integer division (the pixelation), and no hold of a declared count stands beside the record, so a declared count that is not D div T of its mode is refused by name, a count below zero (the Bell Experimenter's -4,566, 14:27) is the count parted from its record, a defect of the engine and never a reading, and the count's line moves at most what the Node holds. (2) THE COUNT IS READ ONCE: a count enters a family's pace once, through the held content of the family that holds it at the divisor 1, read down the graph of the ranks at the weight 1 (THE FINAL UNIFICATION), so every family's pace at a Node is p_0 = Gamma - c and on its Link p_a = p_0 - c - c_a, a pixel's horizon is Gamma div 2, and 2c (the count read as the hold and again as the record's source, or again as a spin's step at the divisor 1) is a reading of the engine that differs from the algebra, a defect and never a finding: the content 12,157 at a pixel of 3,034 is four such readings. (3) THE EDGE: a pixel binds itself where the GameBoard's Green's function of its own well closes, at 0.2255 Gamma (2,706 of 12,000) on the law and at 0.3444 Gamma (4,133) on an engine where the level enters the Link once; below the edge a pixel is a cloud and disperses. (4) THE TAIL: the bound rotation omega_b, kappa = acosh((9 / 2) cos omega_b - 2), t = e^(-kappa), the level b t^d and the well c t^(2 d) at d Links; on the law 3,000: omega_b 0.8105, t 0.640, the wells 1,229 / 503 / 206 at 1 / 2 / 3 Links; 4,000: 0.6578, 0.362, 524 / 69 / 9; 5,000: 0.5137, 0.281, 395 / 31 / 2; with the level once 4,400: 0.8290, 0.754, 2,501 / 1,422 / 809; 4,700: 0.8055, 0.619, 1,801 / 690 / 264; 5,000: 0.7779, 0.532, 1,415 / 401 / 113; 6,000: 0.6741, 0.377, 853 / 121 / 17; two pixels bind together while each count with its partner's well at their distance stays within the horizon. (5) THE TRANSFER between clusters is omega_b e^(-kappa d) per interval at d Links, and the click's reach ln(a_1 a_2 / T) / kappa (THE CLICK JOINS AND PARTS). (6) THE LIGHT is written by clicks alone: g q M(n) times the body's rotation over E_s at the giver's Nodes, one quantum per window, E_s(charge) = 0.86 (Gamma div 2)^(3 / 2), the giver's count at most (A^2 / T)^(1 / 3). (7) THE ONE INTEGER: the universe of clusters carries Gamma and nothing else, the pixel's size in quanta; alpha / G goes as Gamma^(3 / 2) through the charge's divisor. THE FIVE LOOKS ON THIS SECTION: on an engine that reads the count once with the level once the bound window is 4,133 <= c < Gamma div 2 less the partner's well, so (a), (b) and (c) stand at 5,000, (d) at 4,400 and 4,700, (e) the giver 4,400 and the taker 5,000 (the clocks' ratio 1.066); on an engine that reads the count twice or more no pair binds under Gamma (the de Broglie Experimenter's 12,825 at 5,000 / 5,000, 14:22) and the fix is the reading, never the pair; with the conformal term (the level twice) the looks stand at 3,000 and 4,000 on the edge 2,706. THE SCREEN IS A CLUSTER (the owner's question, 2026-09-28, 14:51 Israel: does what the look runs on the screen also have to be a bound body, since the universe holds bound bodies alone; Cheshbon's line, 14:55): everything that stands on the GameBoard of a look is a bound body or a cluster of them, the source, the screen, the slit's walls, the mirror, the polariser and the detector alike, each pixel at or above the edge; a face of the GameBoard is no body, a click on a face is no click, and a look with a declared element that is no bound body is not a look in the rule's universe; a solid wall of adjacent bound pixels does not exist, two adjacent pixels at the edge pass the horizon on their Link in every case, so a screen is a sieve of pixels at a period s with the Links between them under the horizon: on the law 4,000 at s = 2 and 3,000 at s = 3 (a chain of 3,000 at s = 2), with the level once 5,000 or 6,000 at s = 2 and 4,400 at s = 4; a sieve at s = 2 reflects the light of lambda = 4 (Bragg's condition, 2 s = lambda) and is the wall and the mirror of the rule's universe, and a row of taker pixels at s = 2 is its screen, so the five looks are rewritten on sieves and clicks alone before their next run. THE HIERARCHY IS RECURSIVE (the owner's word, 2026-09-28, 14:57 and 14:58 Israel; Cheshbon's line, 15:05): a cluster of clusters is the same structure one level up, Nodes each a bound body clicking at one another, with no number that bounds the depth; THE CLICK IS THE POINTER: the click is the only thing that passes between a cluster and its neighbour and between a level and the next, so from inside a cluster everything is seen and beyond the tail only a whole quantum arrives (THE OBSERVER IS A CLUSTER); THE LEVELS AT A NODE ARE THE NESTING: the three held levels of a Node, the matter's tail, the charge's well and gravity's well, are the three kinds of binding by rank, and the size of a level is the depth in its kind, gravity's well at a Node being the sum of the tails of every body above it (each c_i t_i^(2 d_i), the count its record lays there), so a GameBoard reading names the clusters a Node belongs to; a level n + 1 is bound by the same inequality as the level 1 with the cluster's total count over its members' spacing in place of a pixel's count over one Link, and the one bound on the depth is the horizon at a Node, the content read there under Gamma, at which a cluster's centre is the horizon pixel. THE COUPLINGS ARE AT THE EDGE (the Nature24 session's line, 14:44, corrected by the width): every coupling is the edge the rule allows and no number: a pixel's count is at most (A^2 / T)^(1 / 3) = 4,447 and its well at least 0.2255 Gamma = 2,706, so E_s(gravity) <= 1.64 and is 1, and E_s(charge) is the bound of one quantum per window; THE STABLE PIXEL IS ONE: the small gives to the large until it melts, so the bound universe has one stable count, the horizon pixel, and its second body, the electron, is the open distance m_p / m_e. THE WAVELENGTH IS THE GIVER'S (Cheshbon's line, 15:05, on the Light Experimenter's question of 14:52): the given light carries the giver's bound rotation, and on the band [1, 1] cos omega = (2 + cos k) / 3 along an axis, so cos k = 3 cos omega_b - 2 and lambda = 2 pi / k: a pixel at the edge (omega_b = acos(2 / 3)) gives k = pi / 2 and lambda = 4 exactly, the law's wavelength derived; 4.18 at 3,000 and 5.29 at 4,000 on the law, 4.07 at 4,400 and 4.38 at 5,000 with the level once; a deeper pixel gives a longer wave, and a mode file's wavelength is this number rounded to the Link, 4 for every pair of the five looks. THE CLOSED GAMEBOARD HAS NO REST (on the Light Experimenter's refusal of 14:59): the sum's rest on a GameBoard closed on every axis exists only under a net count 0, so a bound universe closed on itself carries a mean of the held field that drifts by the net count over the Nodes each interval, the hypothesis THE UNIVERSE EXPANDS under its own name and no look of today; a look keeps one axis open with its pixels far from the faces, and there is no sink, a count being never negative. THE WIDTH BOUNDS A BY THE LEAST OF THE THREE (Cheshbon's line, 15:27, on the Nature24 session's finding at Gamma = 24): the amplitude unit A is the largest amplitude at which every total of an interval stays inside the width, Rule3's 2 w A with w = 6 Gamma^3, the count's line's 6 A^2 and the transport's 3 d_1 d_0 (A + 1) with the largest d of the file's twist table, the least of the three and never Rule3's alone; at Gamma = 24 the three give 3.7 x 10^13, 1.2 x 10^9 and about 3,000, so A is about 3,000 against record levels of 3 to 9, and the universe of 24 runs inside the width; a pixel's twist is 0, its rotation living in its clock pair, the twist being the transport's. THE ELECTRON IS THE LIGHTEST BAND, a hypothesis under its own name (the Nature24 session's line, 15:27, on the owner's question what the electron does; Cheshbon's check, 15:32): the lightest massive band the rule holds is m = Gamma - 1, cos omega_e = 1 - 1 / Gamma, omega_e = sqrt(2 / Gamma), and the electron is one quantum on it with q = -1, no pixel (a pixel's ratio is at most 2.22), stable by the integer (one quantum does not disperse into fractions and no massive band lies below), its charge the proton's exactly since q is the click's integer, the positron the same band with q = +1 and pair creation THE CONVERSION; THE MASS IS THE COUNT: the rule reads inertia as the count, the momentum n = M v in the unit Q with the wall W = 3 Q M, so m_p / m_e = c_p / 1, the proton a pixel of 1,836 quanta, bound and within the horizon when 0.2255 Gamma <= 1,836 <= Gamma div 2, so Gamma lies between 3,672 (the horizon pixel) and 8,142 (the edge pixel) and the world's one number is measured; what this carries by name: one quantum is one energy and its rotation is its frequency, nature's E = h nu being the record's click rate, and the spin 1 / 2 is open. THE GENERATOR IS RULE3 (the owner's word, 2026-09-28, 15:28 Israel: no floating point in the generator; Cheshbon's integer run at Gamma = 24, 15:41 and 15:43): a body's bound record is what Rule3 makes of its count at its Node in the engine's own integers, seeded at the Node with the count's well held, run on its GameBoard over many periods until the record stands (its levels repeating over a whole period), and the record itself is the mode file; its period P, its amplitude b, its clock pair [next + before, now], its tail level(d + 1) / level(d) and its wavelength are readings of the standing record and never inputs, a clock pair, a tail or a twist computed in floating point being a tool's defect; at Gamma = 24 Rule3 in integers gives the periods 9.6, 11, 12 and 14 at the counts 8 to 11 on the law (the Green's function: 9.55, 10.8, 12.2, 13.8), and the pixels the integers hold are b = 5 carrying 8 to 10 quanta and b = 8 carrying 12 to 15; THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD: an integer record's form D at a Node moves between 0 and 2 c within one period at Gamma = 24, so the count is (SUM over the period of D) div (P T), read once per period on the record's own clock, never the form of one interval, which kills a pixel of the law and drives a pixel of the level once to the horizon within ten intervals; until a file declares the record itself, a declared count is a reading checked against the loaded record's form at the gate |c - D div T| <= 2 isqrt(c) + 1 (the rounding of an integer amplitude moves D by about 2 b (2 - 2 cos omega_b), 1.5 sqrt(c)), refused by name beyond it; a count moves only whole and never below zero, a Node at 0 gives nothing, and a clamp that sets a negative result to 0 creates quanta and is no rule: the deficit stays as the Node's remainder or the line refuses by name. GAMMA IS NOT CONSTANT, a hypothesis under its own name (the owner's word, 2026-09-28, 15:44 Israel: every tick the universe grows by 6, which explains the expansion and how with the size more and more creatures became possible; Cheshbon's line, 15:50): Gamma_(t + 1) = Gamma_t + 6, the step the six Ports of a Node and no free number; the rule's physics depends on the ratios c / Gamma and m / Gamma alone, so every pair steps with Gamma ([m_0 Gamma_t div Gamma_0, Gamma_t], the matter +4 and light and the charge +6 per interval) and the wall, A and the twist's unit are derived from Gamma_t each interval, the file holding node_clock as [Gamma_0, 6] and the engine no number; a count is the integer its Node holds and stays, so a pixel that does not gather falls under the rising edge 0.2255 Gamma_t and dissolves after (c / 0.2255 - Gamma_0) / 6 intervals, the small giving to the large being the way a body keeps its c / Gamma; the distinct bound counts between the edge and the horizon number 0.2745 Gamma, one and two thirds more kinds each interval (7 at 24, 1,647 at 6,000, 2,235 at 8,142); light on [Gamma, Gamma] does not drift, the clocks of pixels do, a pixel of a fixed count slowing as c / Gamma falls with the rate H = (6 / Gamma) |d ln omega_b / d ln (c / Gamma)|, 5 x 10^-4 to 1.3 x 10^-3 per interval at 6,000, the rule's Hubble rate, and Gamma = 6 t reads the universe's age in intervals (1,000 at 6,000); a look reads it as the takers' clock ratio growing by (6 / Gamma)(s_taker - s_giver) per interval, about 2.6 x 10^-4 at 6,000; at Gamma = 24 every pixel dissolves within three intervals of stepping, so the five looks keep Gamma fixed and a stepping Gamma is a look of its own. THE CLOSE'S WEIGHTS UNDER THE TERM (Cheshbon's line, 16:06, on the Newton Experimenter's reading of 15:56): the weighted current SUM q_n (now_n - before_n) is conserved where the Link coefficients are reciprocal in the weights, q_n R_(n to a) = q_a R_(a to n); without the conformal term R is symmetric and q_n = 2^16 Gamma^2 div p_n^2 at the clock's pace p_n = Gamma - c_n is exact, while under the term R_(n to a) = 2 m (Gamma - 2 c_n - c_a)^2 is not symmetric and no weight per Node is reciprocal on an uneven well, so B at the clock's pace leaves a current that the zero mode grows without bound; under the term the weight's pace is the Node's mean Link pace, p_n = Gamma - 2 c_n - (SUM over the six Ports of c_a) div 6, exact where the neighbours' counts are equal (a chain: Gamma - 2 c - t_x) and within the neighbours' spread otherwise, and only a current weighted on the Links is exact everywhere. A FIXTURE'S T IS ONE WINDOW AT ITS OWN ROTOR (Cheshbon's line, 16:23 and 16:35, on the Newton Experimenter's table of 16:29): one quantum per window is one window's flux at the giver's own rotation, T = floor(a_light^2 N_face sin omega_b sin k) with cos k = 3 cos omega_b - 2 and a_light = (g M a + r) div E_s the light as written, in integers from the giver's clock pair [a, den] of 2 cos omega_b as T = isqrt((a_light^2 N_face)^2 (4 den^2 - a^2) (4 den^2 - (3 a - 4 den)^2)) div (4 den^2), of which sqrt(5) / 3 is the value at the edge alone; a giver whose E_s exceeds g M a writes 0 and is refused by name. THE TWO READINGS OF GAMMA ARE TWO LEVELS (the owner's question, 16:27; Cheshbon's line, 16:35): under THE HIERARCHY IS RECURSIVE every level has its own Gamma and its own interval, a level's interval being the period of the record one level below it, so the proton to electron ratio reads the atomic level's Gamma (3,672 to 8,142, its interval the proton's period over about eight ticks) while the universe's age reads the top level's Gamma = 6 t, one tick for both being impossible; 1,836 is the local count of a cluster within a cluster; the tick ratio of one level is the cluster's period over the pixel's, P_2 / P_1 = e^(kappa d), 7.6 for two pixels of 2,000 at two Links at Gamma = 6,000 (the band 5 to 11, a number the join look reads as the breathing period of the pair's total count), and about 66 such levels lie between the atomic Gamma and the cosmic one. THE LADDER OF THE BOUND STATES (Cheshbon's table, 16:45): the bound states of a Node at a given Gamma are one rung per integer amplitude b from the edge to the horizon, each carrying the count c = b^2 (2 - 2 cos omega_b(c)) at its self-consistent rotation, so at Gamma = 24 there are two rungs (b = 5 and b = 8) and at Gamma = 6,000 about 67 on the law (b = 46 to 112, c = 1,396 to 2,700, the period 7.5 to 13.4) and 27 with the level once, the ratio of neighbouring rungs 1 + 2 / b (1.04 at the edge, 1.02 at the horizon) and the whole ladder spanning 2.22, a near continuum that singles out no ratio: neither 1,836 (between the rungs b = 61 and 62 at 6,000) nor the hadrons' 1.31 is predicted, the mass ratio to the electron fixing Gamma and nothing more; with THE STABLE PIXEL IS ONE the proton is the horizon pixel, so m_p / m_e = Gamma div 2 and the atomic level's Gamma is 3,672 = 6 x 612, one number and no range, a derivation from the law and no prediction of 1,836, which is its input; the chain from the universe's age to that count is not closed: the age gives the top level's Gamma in the top level's own ticks, the step per level e^(kappa d) is a law's number only if the law fixes the stable cluster (horizon pixels in a sieve at the period 2 would give about 13 to 15), the count of levels and the law tying a level's Gamma to its parent's are open by name, and the join look with two horizon pixels at two Links reads the step as the pair's breathing period over the pixel's, about 13.5 in the band 9 to 20; THREE KINDS OF BINDING, NOT THREE LEVELS (the owner's reading, 16:47; Cheshbon's line, 16:51): the three ranks give three kinds of binding, quanta into a pixel by the matter's tail (the step in count the pixel's c, in ticks its period), pixels into a white cluster by the charge's well (the step E_s over q M, 37 at Gamma = 3,672, the same number as the coupling's gap to alpha), and white clusters into a gravitational cluster by gravity's well (e^(kappa d) for tail-touching pixels, the sum's well beyond), and the third kind nests without bound, so the count of gravitational levels is the universe's history and no number of the law. THE WELL IS THE COUNT AND NO FIELD: NO COMPUTATION AT THE THRESHOLD (the owner's word, 2026-09-28, 17:58 Israel, on the Bell Experimenter's finding of 17:45; Cheshbon's line, 18:05): the threshold is kappa = 0, the bottom of the vacuum's band [1, 1] at k = 0 and the self-binding edge alike, where a tail is infinite and a static field on [1, 1] is Laplace's, no decay and no rest on a closed GameBoard; no computation of the law and none of the generator stands there: every bound body sits inside its band at kappa > 0 and light inside [1, 1] at k > 0. So in the rule's own universe (every held divisor 1) a held family has no record of its own that steps and no rest that is solved: its level at a Node is the count laid there and nothing else, every interval (THE COUNT IS READ ONCE), the well at d Links is the matter record's own count there, c t^(2 d) laid from its form over its period (THE TAIL), and gravity's well at a Node is the sum of those tails; a held record stepped by Rule3 on [Gamma, Gamma] at the divisor 1 (the Bell Experimenter's [2, 5, 7, 10, 10, 11, 8, 8, 7, 6, 5, 4, 3, 2, 1] along the white world's pipe from one pixel of 10, two pixels of 10 two Links apart reading 26 and 27; the Clock's 1,466 / 2,444 / 2,553 at the neighbours of 4,400) and a START's rest solved on [1, 1] (the Clock's 9,952 = 2.26 c at the charge over 400,000, where c div E_s = 0) are the field at the threshold, readings of the engine that differ from the algebra, the defects (d) and (e) and never findings; the files change in nothing, the divisor 1 being the word. The blind numbers under the line at Gamma = 24 with the level once: a pixel of 10 lays 2 / 0 / 0 at 1 / 2 / 3 Links (the wells 2.8 / 0.8 / 0.2), two pixels two Links apart read 10 to 11 each, a sieve's Node 8 to 11, the pipe [0, 0, 0, 2, 10, 2, 0, ...]. Under a divisor above 1 the held field on [1, 1] is the universe of record's (THE FINAL UNIFICATION, THE FALL, DARK MATTER), and the word's reach there is the owner's to say. THE GATE READS THE FORM AT ANY PHASE: a standing record's D = now^2 - next x before at its Node is B^2 sin^2 omega_b at every interval, B its peak, and equals b^2 (2 den - a) div den with b the level where now = before alone (b = B cos(omega_b / 2)), so the gate compares the declared count with D of the loaded record after one interval of Rule3 and with no formula of a phase (the Clock's 5,310 against 4,379 is B read as b). THE GENERATOR HAS NO SINK: Rule3 is reversible and nothing leaves a GameBoard but a quantum by a click at a face; a fill of 0 beyond an open face and a slab zeroed each interval are walls (the Node beside reads 0: the reflection with the sign flipped), so the unbound part of a seed never leaves; a seed of one Node carries the mode's share 1 / (1 + 6 t^2 + 18 t^4 + 38 t^6 + 66 t^8) (0.18 at Gamma = 24 with the level once, 0.62 on the law) and the rest is debris spread over the GameBoard's V Nodes, so the record is read at the Node over many periods on a GameBoard whose V dilutes the debris and purified by re-seeding from the record within three Links of the Node at its peak's phase, 0 elsewhere, integers alone, each pass leaving the debris its share within reach (about 180 / V); a record whose pair lies inside the vacuum's band (the Clock's [8, 8], the period 6, against the bound periods 8 to 14 at 24) is a mode of the walls and no pixel, and every reading is at the Node, never the GameBoard's sum. THE GENERATOR OF THE RULE'S UNIVERSE WRITES BOUND BODIES ALONE (the owner's word, 14:32): a body is its count at its Node; its record is the bound state of that count and nothing else, b through the form and the tail from kappa (THE WALL IS ONE), no free record and no declared mode; a world file holds counts, their bound records and the band [1, 1], and nothing more.

### The interval

The engine steps every family from the state at the interval's start to
the state at its end. Every read is of the start's values: the six
neighbours' levels, the Node's own pace, the arrivals, never a value
written in the same interval; one Link per interval and nothing in zero
time. The interval has five places, in order:

(i) the clicking families' step, every component, with the transport through
the Ports and the self-source; (ii) the bookings at the Ports (the current),
the ladder, the takings and the givings, the count's line; (iii) the held
families' step; (iv) the holds written (a body's values into its family's
levels), the clicks' changes of a body's content, charge and momentum
included; (v) the bodies on one Node: the feed, the induction, the spin's
step, each a reading of the body's record and no write (a body has no law of its own).

The order within a place, where two primitives write one value, is the
step file's (`law/step.json`), one data file shared by every world,
read at the start, its digest in every run's output. A click's writes
enter at the next interval. Backward, the places run in reverse order
and each primitive runs its own inverse.

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

THE LAW IN ONE LINE: at every Node, each interval, the division act below with its coefficients from the family's pair and the Node's paces; every level on the GameBoard is written by that same act ([a family's write](#the-primitives)), a quantum moves whole when a remainder crosses T ([the count's line](#the-counts-line)), and everything else is a number in a file. Every family, at every Node, with the wall w, the read coefficient R_a on
each axis a, the self coefficient S, the level a_now at the interval's
start, a_before one interval earlier, and the remainder r kept at the Node:

  w a_next + r' = SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now - w a_before + r,
  0 <= r' < w,

arr_(±a) the **arrival** through the Port ±a: the neighbour's level, or
its rotation by the Link's angle ([the transport](#the-transport)); 0 beyond an open face;
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
THE PACE IS CONFORMAL: below the vacuum's pace every family's rotation at every wave number obeys sin^2 (omega / 2) = (p / Gamma)^2 sin^2 (omega_vac(k) / 2), the pace multiplying the clock of every wave and every bound mode alike (the isotropic S is 12 den (Gamma^2 - p^2); the light's line was so already, the matter's mass term stood half at the vacuum's pace), so two clocks at one level shift alike, d ln omega / d c = 2 tan (omega / 2) / (omega p), and a packet's fall in a pace gradient, Delta x 2 tan (omega_0 / 2) x (c_+ - c_-) / (p D), does not depend on its family or its shape beyond the band's own (the owner's word, 2026-09-28, 09:01 Israel: the line enters the engine now, as one term of the self coefficient, not after a run; the light experiment's redshift reading, a light record against a matter clock at one level, the ratio 1.0, is the engine's check of the line).

### The direction

Let sigma be the direction, +1 forward and -1 backward, and let div and
mod be the floor division and its remainder in [0, w), and rho the
remainder carried in. With

  u = sigma (SUM_a R_a arr_a + S x - w y) + rho,
  z = sigma (u div w),  rho' = u mod w,

forward (x, y, rho) = (a_now, a_before, r) gives (z, rho') = (a_next, r');
backward (x, y, rho) = (a_now, a_next, r') gives (z, rho') = (a_before, r).

PROOF. Forward, sigma = 1, the line is the definition of div and mod.
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

(a) THE READ, the line above over the GameBoard (the six arrivals); (b) THE
ONE-NODE STEP, the line with the neighbours' reads declared 0: a_next +
a_before = (a / b) a_now, the rotation by the angle whose doubled cosine is
a / b (Chebyshev's recurrence); with a / b = 1 and the coefficient on
a_before declared 0 it KEEPS a level; with a / b = 2 from (0, 1) it COUNTS,
a_t = t; (c) THE DIVISION, the line with R = S = 0: w a_next + r' = the
numerator + r, Euclid's division with the remainder kept; (d) THE LOAD, a
declared integer in the numerator, how a count enters a level.

A COMPOSITION of Rule3's acts with declared coefficients is a finite
sequence of these acts, each with its coefficients (a pair, a weight, a
wall, a load) declared in the files, applied to declared levels.

THEOREM (what the acts can form). Every composition of the four acts is
a piecewise-linear function of the levels with integer slopes: a sum of
linear forms and of floors of linear forms, composed. No such function
is quadratic in the levels.

PROOF. Each act is a linear form of the levels or the floor of one; a
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

THE THREE TESTS OF EVERY RULE. A line enters the law only if it is
generic (one primitive with declared integers, no family's name and no
kind), vector (one of the acts on the state, no root and no float) and
local (its own record and the six neighbours, nothing kept at a Node
beyond the law's numbers). A hypothesis that needs more is stated under
its own name, outside the law.

### The paces

The **pace** of a Node for a family is what its reads make of the Node
clock:

  p_0 = Gamma - SUM over the reads of (weight x by x the read family's time level at the Node),
  p_a = p_0 - SUM over the reads of (weight x by x the read family's time level at the Node) - SUM over the reads of (weight x by x the read family's aa component div 2),  a = x, y, z,

one division per read per axis, rounded at the read: the pace is a coefficient of the interval and no level, so no remainder is kept for it (nothing at a Node but the law's numbers). A positive weight is a hollow (the read family's level
slows the clock, an attraction); a negative weight is a hill. By "q" the
weight is multiplied by the reading record's charge sign. A family with
no reads steps at p_0 = p_a = Gamma, the plain rule. The clock's slowing
is this pace: a record at a Node of pace p rotates and moves as a record
at Gamma does, with its intervals p / Gamma as long. THE LEVEL ENTERS THE LINK TWICE AND THE CLOCK ONCE: the time level lowers the clock's pace p_0 once and each axis's pace p_a once more, so a wave's speed along a Link falls by the level twice (the Link as well as the clock, as nature's light past a body bends by twice the clock's share) while a mode's rest rotation, from S alone, falls by the level once (the owner's word, 2026-09-28, 08:40 Israel: the light experiment settles the symmetries inside the engine, with Nature24's line of 08:55 Israel; the bending's centroid against the twin reads it, twice the clock's share).

THE GUARD, two-sided: 0 < p <= P at every Node, with the edge

  P = isqrt(2 den Gamma^2 div (den + num)),

Gamma for light and above Gamma where num < den (the conformal line, 2026-09-28: the old edge isqrt(Gamma^2 (18 den + 6 num) div (18 num + 6 den)) was the half-fixed mass term's). Below 0 the pace is no clock; beyond P the step
is unstable: the mode at wave number pi has the factor (S - 6 R) / w = 2 - 2 (1 + num / den) (p / Gamma)^2, which
is -2 num / den at p = Gamma and falls below -2 once p^2 (den + num) exceeds
2 den Gamma^2, so the record grows without bound; P is
the largest pace at which p^2 (den + num) <= 2 den Gamma^2
holds exactly, and every pace at or below Gamma is inside it. A hill lessens a hollow and never exceeds it; a pace outside
the guard refuses the run naming the Node.

THE BAND AT A PACE, a reading of the line and no new rule: at a Node of pace p on every axis a record's rotation at wave number k along an axis is cos omega = 1 - (p / Gamma)^2 (1 - (num / (3 den)) (2 + cos k)), with cos k_x + cos k_y + cos k_z in place of 2 + cos k off an axis, so the band of rotations a body's Nodes carry narrows with p^2: a record whose rotation lies outside the band there is evanescent inside (for [1, 1], cosh kappa = (Gamma / p)^2 (1 - cos k) - 1 per Node) and is reflected whole, and one whose rotation lies inside is slowed to the band's group velocity (num / (3 den)) (p / Gamma)^2 sin k_in / sin omega with 1 - cos k_in = (Gamma / p)^2 (1 - cos k) for [1, 1]; light ([1, 1]) meets a total mirror exactly where p < Gamma sin(k / 2), that is where the count c exceeds Gamma (1 - sin(k / 2)) (2,929 at lambda = 4 Links, 3,891 at 4.78), and a window otherwise, with the step's partial share at each face.

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

### The transport

A family with a pair (re, im) at each Node and a read with a twist turns
its arrivals by the Link's angle. On the Port along axis a in the sense
sigma, for each such read with the factor f (the weight times the
record's own rotation for the twist "own", else the declared twist; by q
the charge sign):

  k = sigma x f x (V_a at this Node + V_a arrived through the Port),

V_a the read family's vector component along the axis; both ends form the
same number with opposite signs, so the transport back is the inverse
rotation. The **twist table** of the universe gives, for the angle k in
units of theta_unit = 1 / unit radians (unit the file's, 4 Gamma 2^16 in the
shipped files), a Pythagorean triple (c, s, d) with c^2 + s^2 = d^2 exactly:
|k| = k_1 F + k_0 with F the fine table's length (2^10 in the shipped files),
the fine triple of k_0 and the coarse triple of k_1 composed, (c_1 c_0 - s_1 s_0, s_1 c_0 + c_1
s_0, d_1 d_0), with (c, -s, d) for k < 0 and (1, 0, 1) at k = 0; a k beyond
the coarse table, or any k on a world without a table, refuses the run
naming the Port. The arriving pair is rotated to the nearest unit:

  R_re = (2 c re - 2 s im + d) div 2 d,   R_im = (2 s re + 2 c im + d) div 2 d,

two read acts of Rule3 with the coefficients (2c, -2s) and (2s, 2c) on the
two arrivals, the load d, the wall 2 d, the remainder not kept: a remainder
carried across intervals is one to one only while d stands, and d changes
with the angle every interval; the rounding is unbiased in the mean and the
inverse recomputes the same triple from the start's levels, exact. The
record's own rotation "own" is round(unit omega_0 / (4 Gamma)), written once
by the loader from the record's pair (matter) or from its wavelength on light's
dispersion (light), so no per-world number is declared. The charge's twist
on a charged record is Lambda times "own", by q: no separate number exists.

### The second level

A phase-2 family runs [the line](#the-line) on each of its two levels with the
transported arrivals; with no twist the second level stays exactly zero
when it starts zero. The **self-source** of a family with the unit P_2
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

PROOF at constant paces. Without the rounding the line is a_next +
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

the pair's second level added (im_now_i im_before_j - im_before_i
im_now_j), the weight the family's common wall in the form's units (its
num where one pair stands); positive inward, as the ladder reads it: a
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

THE REMAINDER'S ORIGIN. The remainder at a Node starts at the ladder's
origin, (2 u + 1) T div 2 with u the record's residue ([the ladder](#the-ladder)):
started at 0, a Node with no quantum reads the count -1 at its first
outward swing (T c + r below 0), a hole the line conserves and nature
does not show. A body's count is laid with its record: at every Node
T c + r is the Node's share of the record's form plus the origin, so
the count follows the norm with the margin T / 2 against the rounding's
walk.

THE INVERSE is the same line with the current reversed: T c_now + r =
T c_next + r' - SUM_j F_ij, exact, the currents read from the
interval's levels as the forward step read them.

THEOREM (the count is conserved). Over any region of Nodes, SUM (T c_i +
r_i) changes in one interval only by the currents through the region's
boundary Links.

PROOF. Summing the line over the region, each interior Link's current
enters one Node's right side as +F and its neighbour's as -F and
cancels; what remains is the sum over the boundary Links, a telescoping
sum, exact in integers. On a periodic GameBoard with no face the sum is
constant to the bit.

THE VELOCITY. The record's wave number is conserved by the record's line,
and the count's line is the continuity equation of the current in integers,
so the count's centroid moves at the current's velocity, with no leak beyond
the ladder's remainder; a body at rest has zero net current at every Node in
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

THE BOUND. The total at a Node is at most 6 x weight x 4 A^2 + T (c + 1)
+ T: one current per Port, each the weight times the two products of two
levels at A on each of the two level pairs, the count's wall T (c + 1)
and the remainder below T. The shipped universe (A = 2^20, the weight
800) is within int64; a world declaring A beyond 2^24 at the weight
10^3 is refused by name; the generator's A ([the generator](#the-generator) (f)) is
admitted.

### The ladder

Until the count's line is bound in the loop, the click is read by the
**ladder**, the same division act on a record's inward flux. The data:
the record's residue u (its remainder at its giving Node), its norm T,
its wheel V, hence its threshold theta = (2 u + 1) T / (2 V), fixed at
the giving; the named detectors in their declared order with the face
last. At every interval each Node i of a detector receives the one-way
inward flux f_i(t) >= 0 of the record through its Ports (a Link between
two Nodes of one detector is not a Port and carries no offer); the
record's running total is C(t) = C(t - 1) + SUM_i f_i(t). The click is
at the first interval t* with C(t*) >= theta, at the Node whose segment
of that interval's increment, laid in the ladder's order, contains theta
- C(t* - 1); there the record ends, whole. The rungs are the division
act: b_k = (2 V C_k + Total) div (2 Total).

THEOREM (one quantum, one click). theta is crossed exactly once.

PROOF. C is non-decreasing, theta < T, and the total offered with the
face last is at least T (what leaves offers everything at the face), so
C crosses theta once; the deletion of the record at once leaves nothing
to cross it again.

THEOREM (Born's rule). Let u be spread evenly over {0, ..., V - 1}; then
the probability that the click lands at Node i is C_i(infinity) / T, the
detector's share of the record's total inward flux, whatever the time
profile.

PROOF. theta is then spread evenly over V points in [0, T).
The segments [C(t - 1) + SUM_{j < i} f_j(t), C(t - 1) + SUM_{j <= i}
f_j(t)), one per (interval, Node), partition [0, C(infinity)) and have
the lengths f_i(t); so P(the click at interval t at Node i) = f_i(t) / T
to the grain 1 / V, and summing over t gives the share. The counts over
many records are binomial about the shares, since the residues are
equidistributed and not a permutation.

A detector is one connected region of Nodes with one name; separate places
are separate names. A detector set is one Node of the count's line with its
Ports the set's outer Ports, the sum of its Nodes' lines with one remainder;
Born's rule is the shares of the current among the set's Nodes.

THE PAIR RECORD, rank 2 (the decisions, "Where a tensor enters"): one record with two labels, its level at a Node the 2 x 2 matrix **M** over the labels' two directions, written as the identity by the crystal's giving click (the two labels identical), stepped by Rule3 alone at every Node it reaches (the step, the transport and the paces as any record's, component by component, Rule3 linear), spreading from the crystal's Node through the Ports to both sides; a polariser turns the labels at its own Nodes by its angle through the transport's exact triple, the rows on the one side and the columns on the other, reading nothing beyond them. THE LABELS' CLICKS: each label clicks alone at its own detector, by its own ladder (its own residue, the two spread by `least_residues` at the crystal's Node) at the interval the label reaches the detector's Nodes, reading nothing but the level at those Nodes; the detector of the first label at the setting a offers its two sets the rows of **R**(-a) **M**, each row's booking one half, and the taking click of the row i ends that label and not the pair: the record goes on as rank 1, its level at every Node the row i of the turned matrix there (the click, the law's one non-local act, ends one label at once everywhere and leaves the other on the GameBoard), so the second label at the setting b offers **R**(-b) applied to that row, cos^2 (a - b) to the set of the same index and sin^2 (a - b) to the other, whichever label clicks first.
THE HALF QUANTUM, the count in integers: the crystal's taking click takes the arriving quantum whole into its count (the universe's T), and its giving click lowers its count by one and gives the pair record at T div 2 by the division act, each label one quantum of the record's own unit, the half; the count's line and the ladder run per label at that norm in integers alone, so the theorem "one quantum, one click" holds per label in the label's unit and the pair's two clicks are the arriving quantum, a half and a half, as nature's down-conversion (each photon at half the energy and half the rotation, the crystal's row); a detector's content counts the labels it took, in the label's unit. THE COINCIDENCE READING is the host's, not law: the pairs are counted after the run from the clicks' intervals within a window the expectations file declares, as Aspect's, one label's click at each side; the law has no coincidence set and no joint click (the owner's word: no uniform time of events exists on the GameBoard, the delays and the bounds rule, and the correlation travels in the record alone, by Rule3).

## The primitives
A FAMILY'S WRITE IS ONE ACT: every write into a family's level on the GameBoard is (w x q(Node) + r) div E at a Node each interval, at both levels of the writer's rotation (the second the read act once more, halved), the division act with the remainder r carried at that Node: q(Node) the writer's own quantity THERE (a body: the count declared there times its tensor (1, n_a / W, n_a n_b / W^2), the source sigma u_a u_b; a record: its quanta there, D_i div T, times its rotation over the rest rotation of the matter quantum, omega_r / omega_m (the energy sources, as a photon weighs h omega / c^2); the giving: the body's record's two levels at the shell times its bound charge M_pol(Node), the polarisation it holds there; the recoil: the click's tally), w the one weight of the pair of families (the weight with which the writer's family reads the written family: whoever reads with w sources with w, action and reaction one key), E the written row's divisor (E_s; the recoil's wall L); the hold, the source, the giving, THE START (the rest of the hold's line, its fixed point) and the recoil (the same act into the record's phase at the Port, the recoil's accumulator) are its five instances, and no number is the act's own; generic (the rows' keys), vector (one carried division), local (the Node).


Every primitive of the engine is one folder under
`src/event_universe/features/` with its declaration (its name, its
place, what it reads, what it writes, its line here) and its function
`apply(term, start, own)`, which calls Rule3 and nothing else; the loop binds
the folders through the register and the step file. No folder holds a
number, a family's name or a default. Every write of a primitive is a
whole integer into a declared level; every division's remainder lives
on the record of the primitive that divided.

| Primitive | Place | Reads | Writes | The line |
| --- | --- | --- | --- | --- |
| the pair | (i) | the pair [num, den] | the record's levels | Rule3's coefficients from the declared pair ([the line](#the-line)) |
| the degree | (i) | the parts | the record's levels | the same line on 1, 3 or 6 components |
| the phase | (i) | the phase | the record's levels | phase 2 is Rule3 on the pair; phase 1 is Rule3 with the coefficient on a_before declared 0 |
| the signed read | (i), first on the right side | the read families' levels at the start, the signed weights, by, the tensor's parts | the paces | [the paces](#the-paces); the guard two-sided |
| the send | (i) | the record's level | the Link's value | the value on the Link is the level times the read's weight, R's factor |
| the receive | (i) | the Link's value, the twist reads, the twist table | the arrivals | [the transport](#the-transport): the angle per Port a read act over the wall 1, the triple the tables' composed reading, the rotation two read acts over the wall 2 d with the load d, the six arrivals summed per axis |
| the internal representation | (i) | the generators' tables | the record's pairs | n pairs, each rotated at the Port by the generators' exact tables in sequence, the one-Node step at the tables' pairs |
| the self-source | (i) | the family's own levels, P_2 | the family's level | [the second level](#the-second-level) |
| the operation | (i) | the coefficients | the record's levels | Rule3's line itself |
| the wait | (i) | the record's age | the record's age | the count (b) at a / b = 2: one interval |
| the clicks | (ii) | the current at the detectors' Ports, u, V, T | the record's tally; a body's content M_k at t + 1 | the ladder of [the ladder](#the-ladder) until the count's line is bound in the loop |
| the count's line | (ii) | the body's own record's levels at the Node and across its six Ports as the step produced them (a given record is another record; a loaded level carries no current), T, the weight | the count at a Node, its remainder | [the count's line](#the-counts-line) |
| the lifetime | (ii) | the record's age, L (the key `lifetime` of the record's family's row, an integer from 1; absent, for ever) | the record's end, a click at the face | the age is the count (b) on the record; at age L, wherever the record stands, it clicks at the face, the ladder's last detector, its whole content to the border the key names, after the ladder's click of that interval (the clicks first), so that every record clicks once |
| the clicks list | (ii) | the record's remainders, the wheels | the taken momentum's shares | the products' shares are the click's draw; the sum is the taken momentum exactly |
| the hand | (ii) | **S** and **n** of the taking body at their levels now, the declared hand (the key `hand` of the clicking record's family's row, -1 or +1; absent, no check) | admits or refuses the click | **S** . **n** is a booking of the spin's and the momentum's levels, the three products summed; its sign in {-1, 0, 1} against the declared hand refuses the click where their product is -1 and admits it otherwise, a set with no body and the face admitting with no check; a refused record stays whole with its running total and clicks at the next admitting set in the ladder's order, the face last |
| the polariser | (ii) | the record's pair at a polariser body's Nodes, the body's moment D (its axis and its angle a, [the transport](#the-transport)) | the record's pair; the two sets' shares | a hypothesis under its own name: at the body's Nodes the record's pair is turned back by the angle a through the transport once, at its passage, the turn read in the click's booking and never written into the levels (a turn written at the Nodes every interval the record stands on them is the angle applied many times, a scatterer, not a polariser), and its second level is taken by the body's second set, the first level passing to its first set, so the shares of the click are cos^2 and sin^2 of the angle between the record's pair and the axis, the ladder then as written; a body with no moment polarises nothing; THE SWITCHING (the decision, as Aspect's of 1982): a polariser whose card declares two angles (`angles`, two exact pairs) and a period (`every`, an integer of intervals from 1) turns by the first angle for `every` intervals and by the second for the next `every`, by its own clock (the count act (b) on the body, periodic and local), the angle read at the interval the record's level passes its Nodes and never at the giving; a card with one angle stands as today |
| the giving | (ii) | the body's own levels, its bound charge M_pol at each shell Node (the polarisation it holds there), the given row's divisor E_s, the outward current through its outer Ports, T, M, **n** | the given family's level at the body's outer Ports; at the open M_k -= 1 and **n** at t + 1 | the three acts of one window in this order: the open (M_k -= 1 of the given family and the bulk share n_a -= sgn(n_a) (|n_a| div M), the division act with the wall M, both written at t + 1), the write (the given level at the body's outer shell += (M_pol x a_body) div E_s each interval at both levels, the family's write by the body's record, the division act with the remainder carried, a load, before the bookings: the bound charge radiates (a neutral atom shines; the net charge is Coulomb's alone), the flux grows as M_pol^2, and the given row's divisor is the one coupling of light to charge, as e in nature; the outer shell is the body's Nodes with a Port to a Node outside the body, and no inner Node is written), the close (at outward >= T, the universe's quantum action, the record named, its direction the tally's sign per axis); the open is the click's count move with the opposite sign, and a close is never an open: the count moves once per window; THE TRAIN: one quantum is the train the window writes, N_q periods of the giver's rotation until the outward flux reaches T, its band 2 pi / (N_q u) in k (u the group velocity), so T, the unit, is chosen once so that N_q of every giver of record is tens of periods (the tail beyond a mirror's wavelength falls as 1 / N_q) and the generator writes N_q as a reading |
| the crystal | (ii) | the record arriving at a crystal body's one Node (an ordinary body of matter with the key `crystal`, which declares nothing else), the click's residue u, the family's norm T | the arriving record's click at the Node; the giving click of one pair record of rank 2 from the Node's Ports | a hypothesis under its own name (the decisions, "Where a tensor enters"): the arriving record's taking click at the crystal's Node by the ladder as at any set, its quantum into the crystal's count, and in the same interval the crystal's giving click of one record of rank 2 from that count (its count down by one; the record at T div 2 by the division act, two labels of a half quantum each, the quantum conserved as a half and a half, THE HALF QUANTUM under the ladder), its rotation the crystal's own from its count in the file (the giving's row, the body's mode rotation; the decision, as nature's phase matching in a crystal: the conservation fixes the sum of the labels' rotations to the arriving record's, the crystal fixes the division, and in the symmetric case each label rotates at half the arriving rotation) and its wave number the dispersion's at that rotation, no key for the wavelength; the record's two labels are identical on its two sides (the decision, as Aspect's pairs), so its channel is the identity and nothing is declared; Rule3 spreads its events from the crystal's Node through the Ports as any record's, the record created only during the run and never written at interval 0; the crystal is one Node by default (the decisions, "A detector as nature's instrument"), a cube only where the one-Node equivalence fails, stated with its test (the same world with the body as one Node and as the cube gives the same click intervals within one and the same books; the generator's share inside the one Node at least a half); generic (a body's one key, no integer, no family's name), vector (the two clicks' division acts, the giving's load), local (the one Node and its Ports) |
| the hold | (iv) | a body's content M_k, the quantum's weight w_k of each family's row (its key `quantum`, an integer from 1, required), the row's divisor E_s (its key `divisor`, an integer from 1, required), the count's line's net current j_a at the Node (a reading of the record, as the momentum **n** is), the dipole (the body's spin **S**, the curl of that current about its centre, a reading) | the held family's levels at the body's Nodes; the body's remainders | the count s = SUM_k w_k M_k enters the field's line as a source: the time part at the body's Nodes gains (s + r) div E_s each interval, the division act as a load with the remainder r carried on the body, and at a body in the law's form ([what a body is](#what-a-body-is), its Nodes with their counts) each Node gains (w_k M_k(Node) + r) div E_s of the count declared THERE with a remainder of its own, never the whole s at every Node, a signed source the body's charge q times the Node's count (THE SIGN IS THE BODY'S, 2026-09-28: a family carries no sign and `sign` leaves its files, a body's key q signs its count, so one matter family holds bodies of both signs and the third exact band's sense is sign q); so that two bodies' wells add, a body stands in another's well, and the field's rest is Poisson's with the sources (nature's form: potentials add; a level clamped to the count would make a body's Nodes carry its own count alone); THE WELL OF A BODY WITH A RECORD IS ITS RECORD'S FORM (the owner's word 2026-09-28: the well is the count, and the count is the record's quanta, D_i div T): at every Node of such a body the count written is its own record's quanta there, D_i div T with the form's remainder carried, the source's instance on its own record each interval ([the count's line](#the-counts-line) is its integral, the same in the mean), so the well moves with the record to the form's resolution and the self-force vanishes (the well is the record's own, action and reaction), and a bound body falls in a pace gradient at the free packet's rate (Newton's reading, 2026-09-28: the engine equals the algebra for a free packet to a second order of the gradient); a well written from an integer count alone moves only when a quantum's current crosses T, lags the record's shift a / Omega^2 below one quantum and pins it (the engine's zero of a bound body alone in the tent), a defect and not a finding; the vector part (j_a + r) div (E_s T), j_a the count's line's net current of the Node through its two Ports of the axis ([the count's line](#the-counts-line); the momentum n_a = j_a div T its reading), and the tensor part (n_a n_b + r) div (E_s M(Node)), each with its remainder carried and per Node as the time part: the three parts are one source, the count and its current's tensor at one scale with no factor of the files (the linearised field's 4 and 2 were nature's numbers by hand; the rule's own reading against the moving body decides them), so the row's divisor divides each; the dipole sigma (D x e_j)_i div its divisor at the six neighbours |
| the source | (iv) | the record's quanta at its Nodes, D_i div T with D_i = now^2 - next x before (the form's Node term), the weight w with which the record's family reads the sourced family, the sourced row's divisor E_s | the sourced family's level at the record's Nodes; the record's remainder | a record writes as a body does (the family's write): the level gains w x ((D_i div T) x (omega_r / omega_m) + r_i) div E_s each interval (omega_r the record's rotation, omega_m the rest rotation of the matter quantum, cos omega_m = num / den of the matter row, the ratio by the host's arc cosine as the twist's: the energy is the source, a light quantum weighs its rotation), the division act as a load, with the same w the record's family reads the sourced family by (no weight, divisor or table of its own: the key `sourced` names the family alone, or the read implies it); so light sources gravity and the bound charge as its quanta do (E = m c^2) and every pair of families that read each other is reciprocal; the field's shape is the static limit of Rule3, (Delta - kappa^2) a = -sigma / q with kappa^2 = 6 den / num - 6 (kappa the inverse reach, sigma the source, q the charge's weight) |
| the recoil | (iv) | the click's tally sigma_a, k_q (the quantum's wave number, 2 pi / lambda_q at the giver's rotation on the given family's band, cos k = 3 cos omega_b x den / num - 2, the generator's reading `wavelength` of the mode, no key), M (the body's count), the twist table | the body's own record's two levels at its Nodes, its phase along the tally's axis (the fifth instance of the one write, into the record's phase, [a family's write](#the-primitives)); the momentum **n** a reading | at the close the body's record turns by delta k = sigma_a x (k_q div M) per Link along each axis with a tally, the rotation act by the table's triple nearest delta k at the twist's unit, the angle's remainder carried at the body, the taker and the giver with opposite signs, so the record's envelope carries the phase k per Link of a moving body ([the generator](#the-generator) (e)) and the velocity moves by (num / (3 den sin omega_b)) x k_q / M, the quantum's momentum over the body's quanta ((o) of [the rows against nature](#the-rows-against-nature)), a heavy body's recoil small by its quanta; **n** is read from the record's current ([the count's line](#the-counts-line)) and is no level; a taker with no record of its own takes no recoil; a turn that would carry the phase per Link to pi or beyond is refused naming the body (no speed at the wall, [the paces](#the-paces)); no wall, no store, nothing declared |
| the feed | (v) | DERIVED, no primitive: the body's record in the pace gradient | the body's momentum **n** as a reading | a body has no law of motion of its own: its record moves by Rule3 alone, and in a pace gradient its packet accelerates at a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D (Delta the mode's top velocity, the second derivative of its band in k; d omega_0 / d c the mode's redshift per level; c_+ and c_- the read level at its two faces D Links apart), the count follows the record by the count's line, and its momentum **n** is the reading of its record's current (SUM over its Links of F_ij at the norm T: the count's line's velocity times 3 Q_unit M); no coefficient is declared; bodies with the same Delta x d omega_0 / d c fall alike, and two light bodies in one tent read it |
| the induction | (v) | DERIVED, no primitive: the record's drift in the vector part | the body's momentum **n** as a reading | the reader's pace carries the read family's vector part, - (n_b V_b) div W ((f) THE CHARGE of [the rows against nature](#the-rows-against-nature)), so the record's packet turns and drifts in a vector part's gradient by Rule3 alone: the Lorentz force and its gravitational twin with no line of their own; **n** the reading as the feed's |
| the spin's step | (v) | **S**, a reading of the body's record (the curl of its current about its centre, as **n** is its current) | nothing: no write | a body has no law of its own ([what a body is](#what-a-body-is)): the spin turns with the record by Rule3 alone, and the step's two weights (the curl's 1 / 4 and the tidal term's 3 / 4, nature's geodetic 3 / 2 against the frame's 1 / 2 written by hand) leave with it; the precession of a spinning body is a reading of its record against the row |
| the trace | any | every act's integers | nothing | a reading of every act, it writes nothing |

The hop is retired: the count's line moves the count with its record's
current, and no accumulator of a body's position remains. The rows whose own
code the count's line retires when bound: the ladder's rungs, the giving's
open and close, the clicks list's count move, the lifetime's tally.

A body's writes into its family's levels (the hold): a body of quanta
M_k of the family k, each family's quantum weighing w_k (the key
`quantum` of its row, an integer from 1, required; every shipped family
declares 1), has the count s = SUM_k w_k M_k, the charge Q, the
momentum **n** = **j** div T with **j** the count's line's current through
its Ports (a reading of its record; its velocity **n** / M in Links per interval), the spin **S** the curl of that current about its centre and the moment
**mu** the same with the charge's sign; at every Node of its support it writes gravity's time part s, its
vector j_a div T, its tensor (n_a n_b) div M, the charge's time
part Q and vector the same current with the charge's sign, no factor of the files (the 4 and 2 of the
linearised field were nature's numbers by hand); and the dipoles at its Node's six neighbours, gravity's vector i at the Node + sigma e_j gaining sigma (S x e_j)_i, the charge's (sigma (mu x e_j)_i) div 2.
## The stable body

### What a body is

A body is its count and its record over its Nodes, and never one Node: every body is many Nodes, and nothing gathers it (the owner's word of 2026-09-28). The count c_i is the family of clicks' level at the body's Nodes, in quanta; it enters Rule3 through the pace alone, p_i = Gamma - the held level at the Node (the source's rest: the body's own count and its neighbours' over the divisor), and it never splits: a quantum moves whole, by the count's line. The record (now, before) of the body's family splits by the send and is bound by the wells its counts source. THE FOUR LINES OF THE BODY (the owner's word, in the law's words): (a) THE BODY IS THE FIXED POINT OF ITS BINDING ROW: a body is its quanta over its Nodes; its counts source every held row at the row's divisor; its record is the standing record Rule3 makes in those paces; its counts are that record's form, D div T, with the remainder carried; it stands where the counts return themselves; refused by name as a cloud (the rotation not above the band's top) or a collapse (a pace reaching 0). (b) THE FORM SOURCES THE FIELDS: a held row's level is the rest THE START solves from the counts at the row's divisor and Rule3 steps; no row holds at the divisor 1; a well is a field with a reach, the gapped pair's 1 / kappa. (c) THE COUNT MOVES BY THE COUNT'S LINE ALONE: no count is laid from the form; the count at a Node changes only by the line's flux, and the total is conserved. (d) THE FALL: a = Delta |d omega_b / dc| grad c, Delta the band's curvature at k = 0, d omega_b / dc from Rule3's coefficients at the body's pace and rotation, grad c the other body's content, one line for every held row the body sources. Which fixed point stands is [the stable body theorem](#the-functional-and-the-dilation). The world file names the body's family, its Nodes, its count per Node, its momentum **n** at its two levels (now and before, both declared, a resting body's equal) and its spin's two levels where it has one, and on a body that gives its stocks and its emitter (the given family and the ladder by name), and nothing else: no lowered pair on its Nodes, no seed, no stop, no profile, no closed Port, no period (P_body is its mode's rotation).

### The well

At a Node whose held level is c Rule3's one-Node rotation rises from cos omega_0 = num / den by (1 - p^2 / Gamma^2)(den - num) / den, and its bonds fall from num / (3 den) to num p_i p_j / (3 den Gamma^2): the symmetric form of the line with the weights 1 / p_i. The depth is bounded by the family's own 1 - cos omega_0, so a family whose pair lies close to 1 binds nothing: on [800, 809] (1 - cos omega_0 = 0.011) no cube of any side at any count is bound; on [800, 1200] (1 / 3) at Gamma = 10^4 a cube of side 12 is bound from the level 500 at its Nodes (the mode's share inside 0.79, 0.92 at 1000, 0.997 at 5000), of side 6 from 1000, of side 3 at 3000, one Node at 5000; omega_b / omega_0 for side 12 is 0.832 at 500 and 0.771 at 2000. A body's clock is set by the level at its Nodes and its side, from the rule: a body's mass is its count. THE REACH OF A HELD FAMILY IS ITS PAIR: under the hold as a sum a held family's rest solves num Delta^2 a - 6 (den - num) a = -3 den sigma (its line a_next = num S_6(a_now) div (3 den) - a_before with the source once an interval, Delta^2 the six-neighbour second difference), so outside a body its rest falls by e^(-kappa) per Link with cosh kappa = 3 den / num - 2, the family's own band at zero rotation (cos omega = (num / (3 den)) (2 + cos k) at omega = 0, the evanescent k; kappa^2 = 6 den / num - 6 to the second order, the static limit of the source's row), the same pair that sets the band of its records and de Broglie's k for them ((j)): the gap is the mass of the records and the inverse reach of the field, one number; [1, 1] has no gap (2 cos omega = 2 at k = 0) and its rest is Poisson's over the whole GameBoard, the pull between bodies (Newton's tent, (i)); a pair with den > num has the gap 2 cos omega = 2 num / den at k = 0 and inside a thick body its rest stands at 3 den sigma / (num kappa^2) (Delta^2 the six-neighbour second difference, kappa^2 its value on e^(-kappa r)), so at [1, 2] with the divisor 1 the level inside a body is its count and falls by e^(-kappa) = 0.127 per Link outside (cosh kappa = 4): a body's well is the static field of every family it holds, read at its Nodes by the paces, so a body's binding, a mirror's line c > Gamma (1 - sin(k / 2)) and a window are the short-reach family's and the pull between bodies the massless one's, two held rows of the universe file, one pair each; generic (a row's pair and divisor, no name), vector (the line's own static limit, no root), local (the six reads and the source at the Node).

### The functional and the dilation

THE FUNCTIONAL. Let a body of M quanta have the record phi over its region, SUM phi_i^2 = 1, its counts the form c_i = M phi_i^2, and let every held row r it sources be a hollow (sigma_r = +1) or a hill (sigma_r = -1) with the static kernel G_r of its line ((Delta^2 - kappa_r^2) a = -3 den sigma / num, [the well](#the-well); kappa = 0 for the massless row) and the divisor E_r, so the well at a Node is Phi_i = SUM_r sigma_r (M / E_r) SUM_j G_r,ij phi_j^2. To first order in Phi / Gamma the well line raises the one-Node rotation 2 cos omega by 4 g Phi / Gamma (cos omega by g (1 - p^2 / Gamma^2)), g = (den - num) / den, and the bonds' fall under the pace is of the pressure's own order and drops out at a width beyond the Link; there the fixed point of the binding row is a critical point on the sphere SUM phi_i^2 = 1 of

  F[phi] = (num / (3 den)) SUM over Links (phi_i - phi_j)^2 - (2 g / Gamma) SUM_r sigma_r (M / E_r) SUM_ij phi_i^2 G_r,ij phi_j^2,

the band's pressure less the wells' energy, each well counted once for the record being its own source (Hartree's form). PROOF. The record is the top mode of Rule3's symmetric form at the paces, at first order **M**(Phi) = **M**_0 + (4 g / Gamma) diag(Phi), so it solves **M**(Phi[phi^2]) phi = 2 cos omega_b phi. The derivative of the wells' term at phi_j is 2 (4 g / Gamma) Phi_j phi_j, phi_j entering twice with G_r symmetric; the pressure's is 2 (2 cos omega_0 - **M**_0 phi)_j; so dF / dphi = -2 (**M**(Phi) phi - 2 cos omega_0 phi), and dF / dphi = 2 lambda phi on the sphere is the fixed point's own equation with 2 cos omega_b = 2 cos omega_0 - lambda, and conversely.

THE DILATION. Let phi_R(x) = R^(-d / 2) phi(x / R) be the body dilated, d the GameBoard's dimension and R beyond the Link. The pressure is K / R^2 and each row's well energy W_r / R^(s_r), with s_r the row's scaling power at the body's size: s_r = d beyond the row's reach (the kernel a contact of weight 3 den_r / (6 (den_r - num_r)) per unit source, the rest inside a thick body), s_r = d - 2 within the reach or for the massless row (Poisson's 3 / (4 pi r) in a box; on a plane the logarithm, s = 0 in the sense of the limit, whose energy grows as 2 W per unit of ln R; on a chain the linear well, s = -1).

THEOREM (the stable body). At a fixed point of the binding row of width R the virial 2 K = SUM_r sigma_r s_r W_r holds, and the second variation of F along the dilation is R^2 F''(R) = SUM_r sigma_r s_r (2 - s_r) W_r. A body is stable only where this sum is positive; it is a minimum of F where further the Hessian on the modes orthogonal to the dilation and the translations is positive.

PROOF. F(R) = K / R^2 - SUM_r sigma_r W_r R^(-s_r); F'(1) = 0 is -2 K + SUM_r sigma_r s_r W_r = 0; F''(1) = 6 K - SUM_r sigma_r s_r (s_r + 1) W_r = SUM_r sigma_r (3 s_r - s_r^2 - s_r) W_r. Derrick's scaling, Pohozaev's identity on the GameBoard; at another R the same with W_r read there.

THE SIGNS. s (2 - s) is +1 at s = 1, 0 at s = 2, -3 at s = 3: a hollow holds the body where its well falls slower than the pressure (s < 2) and breaks it where it falls faster (s > 2), and a hill does the opposite. From them, on the rows the law holds:

(a) THE HOLLOW'S DIMENSION. One hollow beyond its reach: on a chain (s = 1) every mass binds, at the width R = 2 K / W, falling as 1 / M; on a plane (s = 2) the dilation is flat and the well within the reach (the logarithm, +2 W) decides: above the mass at which the well's coefficient passes the pressure's the body stands at the reach's size, a window; in a box (s = 3) the one critical point is a maximum along the dilation, a saddle for every mass: the body disperses beyond it and collapses within it. The three GameBoards of the generator read so: on a chain of 60 Nodes 200 to 1,000 quanta stand, on a plane of 40 x 40 x 1 3,000 to 8,000, on a box of 48 x 24 x 24 29,500 to 30,000 alone, at the band's edge.

(b) THE MASSLESS ROW HOLDS THE BODY. Gravity's Poisson well in a box has s = 1: with the pressure alone F = a / R^2 - c / R has the one critical point R = 2 a / c, a minimum for every mass (Pekar's body), its width falling as E_g / M. Beside it a hollow beyond its reach (s = 3) adds a barrier: on a Gaussian body F = a / R^2 - b / R^3 - c / R with a = num / (2 den), b = (2 g / Gamma) (M / E_b) (3 den_b / (6 (den_b - num_b))) / (2 pi)^(3 / 2) and c = (2 g / Gamma) (M / E_g) (3 / (4 pi)) sqrt(2 / pi); the critical points R = (a +- sqrt(a^2 - 3 b c)) / c, the wide one the minimum and the narrow one the saddle, the barrier to the collapse; none where 3 b c > a^2, the collapse. The minimum is a minimum exactly where W_g > 3 W_b there, R^2 > 3 (den_b / num_b) (E_g / E_b) / kappa_b^2, and the largest mass with a minimum is M_max = a sqrt(E_b E_g) / sqrt(3 b_1 c_1), b_1 and c_1 the coefficients at M / E = 1. COMPUTED (the script beside the paper): on the matter pair [4000, 6000] with the binding row [5760, 6000] (reach 2.02 Links) and gravity [1, 1] at Gamma = 6,000, M_max = 4,450 sqrt(E_b E_g); at the divisors 2 and 10 M_max is 19,900, 20,000 quanta stand at the edge (a^2 = 3 b c, the minimum and the barrier meeting at 8 Links) and 30,000 have no critical point at first order: the fixed point the generator reaches at 29,500 to 30,000 is the saturated saddle of the scaling's check (the width one Link, the well at the horizon's edge, (c)), and 32,000 and above collapse; at the binding's divisor 50, M_max is 99,600, the minimum for 30,000 lies at 10.3 Links and its barrier at 0.24, under the Link: gravity's body alone (10.5 Links at 30,000, 5.2 at 60,000), the widths the scaling's scan with the saturation reads as 11 and 4.8, and its collapse from 100,000. On the GameBoard the two kernels' constants at the widths 3 to 6 are 0.51 to 0.78 of the contact's and 0.92 to 0.84 of Poisson's, the reach's crossover and the box; the exponents are the theorem's.

(c) THE HORIZON ENDS A COLLAPSE. Beyond first order the well line saturates (the rotation's gain 2 g (1 - (1 - Phi / Gamma)^2) is bounded by 2 g) and the Link's pace weakens the pressure by (1 - 2 Phi / Gamma)^2; neither makes a minimum, since both vanish together at the pace's floor: the collapse ends where a Link's pace reaches 0, Phi = Gamma / 2 on the Link, a frozen cluster of horizon Nodes, the guard's floor and no body of ordinary matter.

(d) THE HILL. A hill beyond its own reach adds +3 W_h in a box: a hill whose reach is shorter than the body turns the saddle into a minimum where 3 W_h > 3 W_b - W_g; within its reach a hill is Coulomb-like and adds -W_h, so a hill longer than the body disperses it. HYPOTHESIS (the hill holds the body): a body stands as a stable extended fixed point where a held row read with the opposite sign (by q, like signs), of reach shorter than the hollow's, is held beside the hollow: below the hill's reach both are Coulomb-like and the hill, with the smaller divisor, forbids the collapse; between the two reaches the hollow binds; the body's size lies between the reaches. The rows the law holds for it: the polarisation [1, 2] read by q (1 / kappa = 0.49 Links, a hard core of one Link), the binding row (the hollow of reach two Links), gravity (the pull). A run of the generator with the third row decides it; it enters the universe's files by the owner's word alone.

WHAT IS MISSING for the theorem to close (DERIVED): (i) the Hessian on the modes orthogonal to the dilation and the translations: for the massless row alone it is positive at the ground state (the non-degeneracy of Choquard's ground state, a theorem of the continuum), for a set of rows it is read from the run; (ii) the functional beyond first order: the fixed point sources its wells from the form phi^2 while the bonds' weakening under the pace would need the sourcing from the Link's own form, so beyond first order there is no exact functional and the stability is the count's line's own dynamics; (iii) the finite GameBoard: Poisson's rest measured from the faces' zero sets a cloud threshold (30,000 on a box of 64^3 at the divisor 10), and a minimum wider than the GameBoard is no body of that GameBoard.

### The generator

The generator builds every world from zero; it declares nothing and
holds no float.

(a) THE INPUT AND THE REGION. The input is a world file in the law's
form: the GameBoard, the Node clock, the universe file it names and one
body by its Nodes with their counts; nothing on the command line. The
iteration runs on the body's Nodes and their surroundings, out to where
the mode's tail falls below one unit; the count stays on the body's Nodes.

(b) THE ITERATION. Rule3's read act with the before-coefficient 0, a <-
(SUM_a R_a arr_a + S a) div w on the region, then the division act to
the amplitude unit A (the level times A over its largest size): the
power iteration of the symmetric form's top mode (the bound mode, above
the band, the eigenvalue largest in size), at cos omega_0 / cos omega_b per step.

(c) THE STOP FROM THE INTEGERS. The profile is an integer vector bounded by
A, so the iteration is a map on a finite set and enters a cycle; the stop is
the first repeat, exact, no tolerance and no declared count, the profile
there the mode within one unit of A.

(d) THE TWO LEVELS AND THE AMPLITUDE FROM THE COUNT. The mode's second
level is the read act once more, halved (**M** phi = 2 cos omega_b
phi); the two levels are scaled together
so that the record's conserved form equals c T, c the body's count and
T the universe's quantum action: the body's record carries exactly its
quanta's action, its amplitude follows, and no bound on a level is
written (a level beyond the integer width is the engine's refusal). THE UNITS: the ladder reads a record's norm with the weights 1 / R_i and
the family's common wall L, the form of [the conserved form](#the-conserved-form)
times L / (2 num), so the ladder's T is the form's T times L / (2 num).

(e) THE MOVING BODY. The momentum **n** is a reading of the record's current, **v** =
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

(f) THE AMPLITUDE UNIT A IS DERIVED, NEVER WRITTEN: the largest amplitude at
which Rule3's total stays inside the integer width at every content of the
region, the bound of [the bound](#the-bound) solved for the amplitude, A =
(2^63 - 1 - w) div (6 R + |S| + w) at the content whose coefficients are
largest (between 2^22 and 2^23 in the cases of (c)). The fixed point does
not depend on A beyond its resolution: at A / 2 the profile agrees with the
one at A, rescaled, within 12 units of the coarser, and the rotation to
10^-6; the final scale comes from c T.

(g) THE FIELD AT REST, THE START OF A WORLD. The generator iterates the held family's own
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

THE START. The loop writes every held family at the load at its rest, by
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
count and never by less: the quantum of gravity is the click. THE THREE FREE NUMBERS AND THEIR BOUNDS (the owner's question, 2026-09-28, 09:30 Israel): the rule's own universe ([the families from the rule](#the-line), the hypothesis under its own name) carries none of the three; the universe of record carries all three, and its three are these. E_s of gravity is fixed by no line of the law, as nature's G is fixed by none (Rule3 is linear and its form's scale is free: one count writes one level over E_s at any E_s; "the well is the count", the polarisation's divisor 1, is the bound charge's own family writing itself and no relation for gravity); it is free, and its bound is the law's and no person's: at every Node of every body the pace stays positive, count x (1 + K / E_s) < Gamma with K the hold's kernel summed over the body (about 51 for a body wider than the reach), so E_s > K x count / (Gamma - count) at the world's heaviest Node (the loader's guard is this line), and the reading's resolution bounds it above (a fall of one Link within the run, the bending's centroid above its draw); a relation that would fix it (E_s = K Gamma, a body at the pace's edge writing one level per count) is a hypothesis under its own name. The charge's E_s is free as alpha is, bounded below by the same pace at the bound charge's Nodes and by the train (one quantum at least one period, de Broglie's reading 4 x 10^4) and read by the train's N_q. The matter pair is free as the mass is, bounded by the band: den > num, and the reach cosh kappa = 3 den / num - 2 fitting the body's width.

### The rows against nature

Each row is a detector's click on a declared world, read blind, with
U_b = c_b / Gamma the potential at the point named (the clock's shift per level, the conformal pace); the bands are
the rounding's, one Node of centroid or one interval, and the draw's
where counts are read.

(a) THE REDSHIFT: two clocks of one family at the levels c_1 and c_2; the ratio of their tick intervals is the root of (1 - 2 U_1 + 2 U_1^2) / (1 - 2 U_2 + 2 U_2^2), 1 - (U_1 - U_2) to first order.
(b) THE BENDING: a beam past a body at closest distance b, the centroid at a receiver L Links beyond shifted by 4 U_b L toward the body.
(c) THE DELAY: a round trip past the body, delayed by 4 U_b times the path's length within the well's reach.
(d) THE PERIHELION: an orbiting emitter at semi-axis a and eccentricity e advances 6 pi U_p per orbit with U_p the potential at a (1 - e^2).
(e) THE MOVING CLOCK: a body at velocity v = n / W (its phase k per Link an exact pair of the file) has its tick lengthened by the dispersion of its own bound band: the tick's factor f = Omega(k) / omega_0 with Omega(k) = omega(k) - k omega'(k) the rotation at the moving centre (the phase rate less k times the group velocity) and omega(k) = omega_0 + Delta (1 - cos k) the body's bound band, omega_0 its rest rotation and Delta its packet's top velocity (at a quarter turn per Link), both the generator's from the file's counts and pair, no key; to the second order f = sqrt(1 - v^2 / c_b^2) with c_b^2 = Delta omega_0, Lorentz's factor at the body's own light speed; read as the mean of the front and back click periods P_v (1 -/+ v / u) at two resting detectors (u the light's group velocity), P_rest / P_v = f, the GameBoard's own term inside the rows' bands.
(f) THE CHARGE: like signs a hill, unlike a hollow; a reader of charge q reads + q Lambda d in its pace and - q Lambda (**n** . **A**) div W on its vector part, so like charges moving together repel less.
(g) THE TWO SLITS: a giving body, a wall body with two openings d Links apart (its count above the mirror's of [the paces](#the-paces)) and a screen body L Links beyond carrying the sets in strips: the strips' shares of the clicks are the openings' interference at lambda_q, cos^2 (pi d y / (lambda_q L)) at the height y under one opening's envelope, the bright strips lambda_q L / d apart, to the first order in the GameBoard's anisotropy; the exact shares are the two arms' phases **k** . **r** with the wavevector set by cos k_x + cos k_y + cos k_z = 3 cos omega den / num at the record's rotation, a term that at lambda_q = 4 Links on d = 16 and L = 97 moves the second bright pair from 6 to 8.5 strips of 4 Nodes and falls below one strip at lambda_q = 16; the record's rows show it splitting at the openings and its parts meeting on the screen (GAMEBOARD).
(h) BELL: an emitter firing at a crystal body of one Node (its taking click, then its giving click of the pair record, rank 2, two identical labels of a half quantum each), a polariser at each end set to a and b and two detectors, one per end, each clicking its own label alone by its own ladder at its own interval (the labels' clicks): the first click takes a row of **R**(-a) at one half each and leaves the other label as that row on the GameBoard, the second's shares are cos^2 (a - b) to the set of the same index and sin^2 (a - b) to the other, so over all pairs E(a, b) = cos 2(a - b), each side's marginal one half at every setting (no signalling), and S at the settings 0, pi / 4, pi / 8, 3 pi / 8 is 2 sqrt 2 = 2.83, nature's number, derived from the local law with the click's one non-local act alone; the pairs are the host's coincidence reading (the two clicks' intervals within the file's window, as Aspect's), and within the window the number is the same where the window holds every pair's two clicks and no other pair's (the giving's period above the window, the two paths' delays within it), else the pairs lost or crossed read as random pairings at E = 0 in their share; with switching polarisers (the polariser's row) each side's angle is the one at its passage; the run says, and no cell is tuned.
(i) THE FALL: a light body of D Links across, L Links from a heavy body of count c per Node on an open chain, under the hold as a sum ((g)): the held field's rest is the tent Delta^2 a = -3 sigma at the heavy body's Nodes (sigma = w c / E_s per Node per interval on [1, 1]), linear outside with the slope half the body's total source, 0 beyond the open faces; the light body's acceleration a = Delta x |d omega_0 / d c| x |c_+ - c_-| / D toward the heavy body (the feed's row, derived: Delta its mode's top velocity, d omega_0 / d c its redshift per level, c_+ and c_- the level at its two faces), its record's current growing by a x 3 Q M per interval, the fall of L Links in t = sqrt(2 L / a) intervals at the speed a t at the touch; the detector on the falling body reads the heavy body's records given at its mode's period, their number before the touch the givings whose flight at the group velocity ends before t; two light bodies of different shape in one tent read the equivalence principle, alike within the unit or a finding by name.
(j) DE BROGLIE'S FRINGES: (g) with a matter record given by a body of a lighter family: a giver of rotation omega_b radiates only a family whose free band holds it, num / (3 den) <= cos omega_b <= num / den (a bound mode's rotation lies above its own family's band, so no body radiates its own family); the record's wave number is the band's, cos omega_b = (num / (3 den)) (2 + cos k), its group velocity v = (num / (3 den)) sin k / sin omega_b, and to the second order k = omega_b v / c_m^2 with c_m^2 = omega_0 / (3 tan omega_0) the family's own light speed (0.2508 on [800, 1200]): de Broglie's law with the rest rotation as the mass; the strips' shares are (g)'s at lambda = 2 pi / k.
(k) THE TWO-QUBIT COMPUTER: one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate (the phase (k_in - k) l over a depth l, [the paces](#the-paces)) and the polariser; two qubits are the crystal's pair record, whose two labels' clicks paired by the host's window are (h)'s E; a controlled gate needs one record to turn another's phase, which the acts alone cannot (the theorem of the four acts) and a read can only through the pace: a target family reading the control family with the weight g_c has its pace wobble with the control's level, the first order averaging out over the control's rotation and the second order a hill of g_c^2 A^2 / (4 Gamma) over the overlap (A the control's amplitude), so the blind expectation is (h)'s E with that small phase, and a controlled phase of order one is a hypothesis under its own name, not in the law.
(l) MACH-ZEHNDER: a giving body, a splitter (a body of a count inside the record's band, one Node deep along the beam, its reflected share s the slab's from [the paces](#the-paces), one half at the count found by bisection), a mirror on each arm (a count above the mirror's), a second splitter and two sets: the shares of the clicks are 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = k (L_1 - L_2) the arms' phase difference, so at equal arms and s = 1 / 2 every click is at the cross exit; the record's rows show the two arms (GAMEBOARD).
(m) THE ROUND TRIP: a giver receding at v from a mirror at rest, its set on itself, giving every P intervals: the forward record's wave number solves Omega(k) + k v = omega_b (the giver's rotation seen from the GameBoard), the returned record has the same rotation and wave number, and the returned clicks come every P (u + v) / (u - v) intervals with u the group velocity at that k: the two-way Doppler ratio with the light's group velocity in place of c.
(n) SAGNAC: a giver with its set on itself moving at v along a ring of N Links (a periodic chain): one record's two arms return after N / (u + v) and N / (u - v) intervals, u the light's group velocity, so the set's clicks fall in two groups whose means differ by 2 N v / (u^2 - v^2), which is 4 A omega / u^2 for the ring's area A and angular speed omega to the first order in v / u (each arm's Doppler shift of k the second), and coincide at rest; a giver at rest on the ring reads one group at N / u.
(o) THE MOVING MASS: a body giving a lighter matter family (a row whose band holds the giver's rotation, (j)) toward a set L Links away: the record's quanta move at the count's line's velocity v = (num / (3 den)) sin k / sin omega_b, the set's clicks come L / v intervals after each giving, and the giver's momentum moves by 3 Q_unit P_body (L div lambda_q) div L per quantum given (the recoil); the record's rows show one packet at v (GAMEBOARD).
(p) THE MEDIUM'S DELAY: a light record through a window body of depth l (a count below the mirror's of [the paces](#the-paces)) is slowed inside to v_in = (p / Gamma)^2 sin k_in / (3 sin omega) with 1 - cos k_in = (Gamma / p)^2 (1 - cos k), the index v_g / v_in, and a set beyond reads the passage longer by l (1 / v_in - 1 / v_g), a round trip by twice that; through a window moving at w along the beam the record's wave number inside is matched at the moving face, omega - k w = omega_in - k_in w, and its speed inside is the band's group velocity at that k_in, not v_in + w; Fresnel's drag w (1 - v_in^2 / v_g^2) is nature's number beside it.
(q) DARK MATTER: a heavy body in a box and a light test body at the distance r on a circular orbit (v^2 = r a): the held field's rest outside the body is Laplace's ([1, 1]), c(r) = s x the reference flux / r falling to the faces' 0 (the open faces' images steepen it near a face), so a = Delta x |d omega_0 / d c| x (c_+ - c_-) / D falls as 1 / r^2 and v^2 as 1 / r, Kepler's fall-off, under the hold's write as a load and as a sum alike (the source inside, Laplace outside); the DETECTOR reads the orbit's period in the waits' phase as in (d); a flat v(r) is the finding that names a missing law.
(r) DARK ENERGY: a giver and two far sets on a long periodic chain over 10^5 intervals: Rule3 is translation-invariant, so a free record keeps its wave number and rotation exactly and the sets' mean click interval stays the giving's period P at every distance, the record's rows widening by the dispersion as the root of t while its count does not move (GAMEBOARD), the rounding's walk at most one unit of level per Node per interval; a mean interval growing with the distance is the finding.

A row outside its band is a finding: it names the missing law or the
defect, and no body's numbers are patched to meet it.

## What is open

1. Whether a body at rest jitters when its current's swing reaches T / 2: on sixteen Nodes the swing over 400 intervals is one percent of T / 2.
2. The self-source's cubic term: not in the engine, the line is the squares' sum alone.
3. The twist table's small angles: a triple with d at most 10^9 reaches no angle below 6.3 x 10^-5 radians.
4. The equivalence principle holds to the band's own shape: Delta x 2 tan (omega_0 / 2) differs by a tenth across the bound bodies of the clock's table; the fall with two light bodies reads the rest.
5. The two thirds' charges: a third with the sign q reads a third, and the composite read modulo a turn identifies -1 / 3 with +2 / 3, but no line gives the up third 2 / 3 and the down third 1 / 3.
6. The three generations: a hypothesis under its own name, the three ranks of the exact band [-1, 2]; no line gives a rank a mass.
7. The exact band [0, 1] of the period 4: a family that never clicks and carries no colour, unnamed in nature here.
8. The stable body theorem's Hessian beyond the dilation for a set of held rows, and the functional beyond first order in the well over Gamma ([the functional and the dilation](#the-functional-and-the-dilation)); whether the hill holds the body is a run's finding.
