# One big clock: spin, Bell, the click, and the names

David, 2026-10-27, 10:5x UTC, for the Boss (his fifth consultation, his task of 10:2x UTC).

## The word

The owner's words of 2026-10-27, 10:1x UTC, relayed in the Boss's task, in translation:

- "Can spin, Bell and the click be solved when one looks at everything as one big clock made of small clocks?"
- "everything with names tied to clocks, right?"

The ground is DAVID-CLOCKS.md. Each claim is derived before it is measured, and each carries one of four marks:

- **checked**: the scripts in DAVID-ONE-CLOCK_CHECKS.txt beside this file;
- **read**: read from the code;
- **earlier**: measured or derived in an earlier document;
- **unknown**: neither settles it.

## The big clock

- **Its state:** every line of every row at every Node, with the counts.
- **Its tick:** the interval.
- **Its small clocks:** the lines, each a coarse and a fine hand on a dial of w ticks; and the planes, each a family's hand at its rest rate.
- **Its reach:** a small clock's next state is a function of its Node and the six neighbours, so influence travels one Link per tick.
- **Its direction:** the run back is exact.
- **Its bang:** every Node's volume clock reversed at its top.

So every state at every tick is a function of the seed: one clock, deterministic and local. [read; earlier]

## 1. Spin

**In one line.** Not on the engine's head. Every family is a plane, and a plane's hand cannot turn with space. The least a hand needs for spin's half turn is a second plane (about one axis), or four planes (all three axes, which is the struck shape-8 row). The full turn's sign shows only as an interference of two parts of one family, one part turned by 2 pi in a held field relative to the other, and no act of the engine makes that turn.

### (a) The full turn's sign

- **Space never turns in the engine.** The 48 are relabelings of the Ports that the kit compares, not acts. A plane's two lines name no Port, so every plane is a scalar under every relabeling. A full turn of space is therefore the identity on every hand, and no act ever meets a declared sign. [read]
- **A global sign cannot be seen.** The wind (the share), the charge W and the current are all even in the hand. The textbook observable is relative: split one family's wave in two, turn one part's hand by 2 pi with space relative to the other (a precession in a held field), and recombine at a click. The chime count against the field's strength then has period 4 pi for spin one half and 2 pi for a scalar. [derived]
- **The smallest world that would show it:**
  - one family laid as two packets with a fixed relative phase, on the two arms of the board;
  - on one arm, a held uniform curl of the shape-4 row's odd lines (the field);
  - a detector body at the Node where the arms meet;
  - the reading: the credits there against the field's strength.

  The engine cannot show it. No hand turns with space, and the one coupling that turned a hand in a field (the curl term, SR-S3) was struck with the spinor row. [derived; read]
- **The big clock's own full turn is two reversals of time:** the bang's top and its floor, each an exchange. On a plane this turn is +1 by force. A time reversal must send the Link's phase turn R(theta) to R(-theta), so its map on (re, im) anticommutes with the quarter turn J; every such map is a reflection, and every reflection squares to the identity. (Checked: every integer 2 x 2 matrix with det +-1 that anticommutes with J squares to I.) The sign -1 here is Kramers' T^2 = -1, which nature ties to half-integer spin. It needs a doublet: T = (i sigma_y) K on two planes. [derived; checked]

### (b) The half turn with space

- **What it needs.** A quarter turn of space must act as 45 degrees on the hand, so that four quarter turns give 180 degrees, which is -1. On integer levels a 45-degree turn is a matrix of order 8 on the hand's lattice.
- **One plane cannot carry it.** This is the crystallographic restriction: an integer 2 x 2 matrix of finite order has order 1, 2, 3, 4 or 6. It holds in general because its characteristic polynomial has degree 2, while the eighth roots' minimal polynomial x^4 + 1 has degree 4. Checked by exhaustion on entries in [-6, 6]: the finite orders found are 1, 2, 3, 4 and 6. [checked; derived]
- **The big clock's state adds no rank.** One bit beside the two lines could hold the hand in Z[i] or in (1 + i) Z[i]: the 45-degree step maps (a, b) to (a - b, a + b) and comes back by halves. But the halves are exact only while both lines keep equal parity, and Rule3 rounds each line on its own and does not keep it. [derived]
- **Two planes suffice for one axis.** On four integer lines, the companion matrix of x^4 + 1 has order 8 and its fourth power is -I: the hand of Z[zeta_8]. [checked]
- **All three axes need eight lines.** The double cover of the cube's 24 rotations (the binary octahedral group) has no faithful rational representation below dimension 8: its spinorial characters either carry sqrt 2 (the two of dimension 2) or are quaternionic (the one of dimension 4). That is the struck shape-8 row exactly. [derived from the group's character table]
- **So** a second plane per family is the least for the half turn about one axis, and four planes for the full double cover. Row 41's two beats in a held field also need the field's coupling back. [derived]

### One level up: a proposal for the owner's word

In nature, the exchange's sign (Pauli) and spin one half's two marks (the full turn's sign and T^2 = -1) are one fact: spin-statistics. In the engine they could be one declaration:

- an antisymmetric family is carried as a doublet (two planes), with its exchange T = (i sigma_y) K and its hand turning 45 degrees per quarter turn of space;
- a symmetric family stays a plane.

The price:

- each matter row doubles its lines, two more per matter family at every Node;
- every record moves;
- the curl coupling comes back.

Unknown until built; this is the owner's word to give.

## 2. Bell

- **The bound.** The big clock is local (one Link per tick) and deterministic. For two clicks outside each other's light cone, with settings independent of the pair's fine hands, |S| <= 2: Bell's theorem. [derived]
- **The door is built in.** The settings (the detector Node's proper parity, in bell2.py) belong to the big clock's state. They are functions of the detector's past cone, which overlaps the birth's past cone, because the seed is common to both. So measurement independence fails in form. [derived]
- **The engine's pairs never leave the light cone.** On the head's three records, every pair the reader finds clicks at the birth's two ends: one Link apart, 1 to 7 intervals after the birth, the two clicks 0 to 7 intervals apart. The two ends exchange levels every interval through their Link, so no pair of these records tests anything about the door. [checked]

  | record | pairs | S |
  |---|---|---|
  | chiral | 14 | 4/3 |
  | hole | 18 | 27/20 |
  | bodies | 8 | not read (three cells only) |

- **The world that would measure it.** The act it lacks is the moving child lay, the owner's word:
  - the children laid moving apart at the birth (MV-S1's wave lay at opposite wave numbers, the momentum booked as it is booked now);
  - detector bodies standing L Links from the birth on each side, with L above the number of intervals between the two clicks;
  - bell2's pairing kept to the spacelike pairs (the clicks' Link distance above the intervals between them);
  - at least 32 pairs and 8 per cell, from varied seeds. [derived]
- **What the algebra says.** The door carries S past 2 only if the parity of the detector's proper count correlates with the pair's fine hands in the sign pattern the four cells need. The proper count sums the clock's rates over the Node's whole history, so its parity is a hash of the content there, and nothing in Rule3 ties it to hands born at a meeting L Links away. The expectation is therefore |S| <= 2 within the ensemble's noise; the measurement decides. [derived; unknown]

## 3. The click

- **What the code does.** Read from bodies.py, a click takes four things at one Node:
  - a record other than the light, standing at a whole quantum of its own unit (its wind at least one unit);
  - standing so for at least one beat of its own hand (the beat is the ticks between two zero crossings of its re line: half a turn);
  - the light at that Node paying one quantum of the body's unit (the take from the gap-0 row), laid back where nothing arrives (the current across the six Links summing to 0);
  - the credit logged with its frame. [read]
- **So the owner's sentence is the trigger, with two corrections.** "A small clock completing one turn while it holds a whole quantum" is right except that the turn is half a turn (one beat), and the light's hand pays. The click is a transaction between two clocks at one Node. [read]
- **What the big clock adds.**
  - The tick that counts the beat and the standing: a deep body's beat is longer in ticks, which is what gate 10's dilation and gate 2's spacing read.
  - The ledger: the account at the Node.
  - Nothing about which Node clicks: that is decided by the Node's own two counters. [read]
- **The detector is no cluster in the engine.** A body laid over many Nodes clicks Node by Node, each on its own counters. "A cluster of small clocks with one beat" would need a coupling of the counters across Nodes, and no act makes one. The coincidences the engine has are two: of two counters at one Node (standing at least the beat), and, at a meeting, of two neighbouring clocks each holding a whole quantum. [read]

## 4. Clock names

The two levels are kept apart: the first four names are the line's own clock (the carried division); the rest are the family's hand and the acts on it.

| the law's name | clock name | what the code does |
|---|---|---|
| line | dial | one number w a + r: a coarse hand a and a fine hand r on w ticks. Rule3 is the carry: V = w (a_now - a_before) + r, V' = V + F |
| level | coarse hand | the count a; a_now and a_before are its last two readings, their order the direction |
| remainder | fine hand | r in [0, w), the fraction of the velocity; born at the half wall, at rest |
| wall | the dial's ticks | w, the ticks per coarse step |
| row | clockwork | every Node's dials of one family, stepped by one rule (its pair) |
| plane | hand | a family's two dials at a Node, (re, im): one hand's two shadows, turning at the rest rate cos omega_0 = num / den |
| pace | rate | p_0, the Node's clock rate per tick; the Link's pace is the rate twice, the ruler |
| content | slowing | the count of 1 / Gamma slowings compounded on the Node's rate |
| carrier | regulator | the row whose time line X counts the Node's own ticks and rulers per board cell, and so sets every rate at the Node |
| emitter | the free hand (the light) | the plane with no rest rate (D = 0) |
| share | wind | the hand's stored energy: its length squared in the rule's form, counted in quanta |
| take | unwind | the hand shortened by the least count whose wind falls by the quanta booked |
| lay | set | levels set on a dial: the seed, a child, a lay-back |
| draw | fine read | the fine hands at the Node and its six neighbours, read as digits and composed modulo the unit times the count of planes |
| credit | chime | a hand that held a whole quantum through one beat chimes; the light pays one quantum; logged with its frame |

**My judgment on the rename.** As a glossary the dictionary costs nothing. As a rename it costs much:

- The record's keys ("credit", "birth", "taken", "booked", "laid" and the counts) are the format that every reader, every gate and the Reader's folders read. They stay, or every record and every reader moves.
- The law's text names every clause in these words, and the code's docstrings cite the law. A rename in src alone would make the code and the law speak two languages.

My advice:

- put the clock names beside the law's names as one table, in ENGINE.md or in the law;
- keep the identifiers;
- rename only with the owner's word on the law's text;
- never rename the record's keys.

A document and its checks alone: no code and no test change.
