# What the clocks lack: the open problems by their causes, the law that removes them, and small toys (Animate)

The owner's word to Animate, 2026-10-28, 15:2x UTC (Hebrew, translated): "Try to understand, at the level of the clocks, where the problem is now in each of them, and whether it is one law or several that are needed, and solve it at the logical level of the clocks, simply, and after that translate it into an algebraic solution. Analyze all the problems there are now, the open things with the clocks, and think; do a small simulation; what is really needed at the level of the clocks: the laws that are lacking and that solve everything, couplings, families."

This page is a toy check for the plan. Nothing here is engine code. The toys are in ANIMATE-PROBES-4, and every claim is marked CHECKED or OPEN.

## 1. The open problems, each where it breaks in the clocks

| # | the problem | where it breaks, in the clocks | the cause |
|---|---|---|---|
| 1 | F2's lower side: light faster than one Mesh a tick along a compressed axis | one tick of the great clock for clocks that run at different rates | A, time |
| 2 | the horizon and BH-S1: a clock at rate 0 is held by a mask | the same: every clock is moved at every tick, so a stopped one must be held | A |
| 3 | the twin calibre breaks: a step past one turn of the dial, the end teeth's fallback | the same: a fast clock is stepped once where it needs several ticks | A |
| 4 | the detector's click never fires (0 splits in every run) | a hand holds one direction, so every born child is definite and nothing is left to decide | B, state |
| 5 | no composite clock forms on the board | two clocks that meet are never read as one dial | B |
| 6 | the fitting's lay breaks the 24 (12 of 72 cases) | the lay must give each child a direction (cause B) and gives the twins' own one | C, selection |
| 7 | law 10 on the A1 calibre: births stop after the third bang | A1 x A1 = A1; no click writes a new direction (B, C); the light's own kind is A1 | B, C and the light's family |
| 8 | Pauli's exchange sign is a premise | which part of two equal clocks' joint dial they take | B (open: draft J) |
| 9 | Bell at a distance | a joint dial lives where its clocks meet, and no local clock carries it apart | Bell's theorem: no local law gives it |
| 10 | the fusion's books: the wind does not add | the joint dial's whole turn is a carry whose remainder must be booked | law 11, which stands |
| 11 | the density step's locality (Sofer's finding) | the three sub-acts of the step, not the state | the step; the state stays local under B |
| 12 | the draw's fairness | the vernier's composition, not a clock's act | item 6 |

## 2. Three causes, three letters of one law

**A, time: a clock's time is the carry of its own dial.**
- Each clock's dial advances by its own rate, and each whole turn is one of its ticks.
- Light crosses one Mesh per local tick.
- A fast clock ticks more often, a clock at rate 0 does not tick, and a clock past it runs back (the turnover).
- This removes problems 1 to 3 and is Sofer's one operation under six names.

**B, state: clocks that meet share one dial.**
- Two clocks at one Node-clock, or the two children of a fitting at the two ends of one Mesh, are read as one joint dial, held where they meet and never wider (line 98's count stays fixed).
- A clock's own state is how its winding is shared among its directions, and it may have none.
- This removes problems 4 and 5, and it keeps the state local (11).

**C, selection: every carry keeps the kind.**
- A click lays the part of the joint dial whose kind is the kind of what feeds it.
- Still light lays the A1 part (the singlet). A light with a lead along a Mesh lays the T1 part along it.
- This removes problem 6 and, with B, gives the detector's click and the composite.

**The one law** (for the owner's list): **the board is dials and their carries. Each clock's time is the carry of its own dial; clocks that meet share one dial; and every carry keeps the kind of what feeds it.** Law 11 ("every bound is a clock's carry") and the tension read in the time gear's teeth (ANIMATE-F2-CARRY.md) are its earlier letters.

**Law 10 then needs no law of its own.** Each click writes a direction that the reversed run leaves standing (item 11 (o), way 2) and breaks the board's sameness, so the next bang fits more pairs (B, C). The local tick keeps the course whole while it does (A).

## 3. In the algebra

- **A:**
  - each Node-clock holds one more integer, its dial tau (David's local tick);
  - its tick is Rule3's carry of tau plus its rate by the full rate;
  - an event steps its gears by the one formula with the coupling c d^2 (d its own tick), reading each neighbour at the event's moment: the neighbour's now, its before, or the point between them, by one carry;
  - the events run in the order of their moments, and the rewind undoes them in the reverse order.
- **B:**
  - the joint dial of two clocks u and v is u x v, for two twins a 2 x 2 Gaussian matrix;
  - its kind parts are C_K (u x v) (DAVID-TENSOR24-THE-COMPOSITE.md);
  - a clock's own state is its two-point reading, for the twins (rho, S);
  - it is held at one Node-clock, or on the one Mesh of a fitting.
- **C:**
  - the lay is the source kind's projection of E1/2 x E1/2: eps from A1 light, sigma_a eps from a lead along the axis a;
  - every click is the 24's kind projection, with shares the projections' traces (Schur).

## 4. The toys (ANIMATE-PROBES-4), each one that can fail

1. **local_tick.py, law A** (a ring of 60 clocks in exact rationals; a patch of 20 at c = 27/25, the rest at c = 1, the light cone). CHECKED.
   - **One tick for all:** grows past 10^6 by tick 48, so the cone breaks.
   - **The clamp:** holds (largest 2.0), but the patch's light is held to the full rate.
   - **The local tick:** the patch's clocks tick twice per great tick, and every clock reads its neighbours where they stand at its own moment. It holds (largest 2.135), its front reaches the probe a tick sooner (the patch's faster light), and the rewind is exact over 9,600 events.
   - A first try that read a neighbour at the wrong moment blew up even with the clamp. The read at the reader's own moment is what holds it: David's correction of line 557.
2. **kind_kept.py, law C.** The 24's lifts are closed from three generators (24 classes up to a scalar). CHECKED.
   - **The head's lay** (the up twin at one end, the down at the other) keeps the 24 at 12 of 72 (turn, axis) cases. The singlet and the vector lay keep it at 72 of 72.
   - **A child's own state:** S = (0, 0, 1) under the head's lay, definite, so no detector has anything to decide. It is S = 0 under the singlet and under the vector lay: the winding is split half and half along every axis, so the detector's click fires.
3. **kind_kept.py, the families' ladder,** with Pauli's rule and the fitting's pair unequal. CHECKED.
   - Light A1 alone stays at A1.
   - A vector light (T1) alone reaches the 24's five kinds, A1, A2, E, T1 and T2, by bang 3, and never the spinor kinds.
   - A1 light with twin hands reaches all eight at bang 4, and T1 light with twin hands at bang 3.
4. **Earlier** (ANIMATE-F2-CARRY.md, part 7): with F2's carry and the twin hands, the clicks rise 64, 96, 256 and 1,152 per bang, until tick 157 is refused where law A is missing.

## 5. The families and the couplings

**The families:**
- The twin hands in the calibre are the detectors (decided, item 11 (e)).
- **A candidate:** the light as a vector, T1, three Gaussian gears, as nature's photon is spin one. With it the ladder climbs from the light alone to the 24's five kinds, and with the twins one bang sooner. Under C, a vector light also lays vector composites directly.
- Composites are derived from their parts, never declared.

**The couplings:**
- The fitting is the light's coupling to the pair's joint dial, its kind kept by C. It adds no integer (Wigner and Eckart's rule on the 24).
- The spin's coupling to the current (S . J, the A1 contraction, decided as item 5) carries each written direction into the next bang's light. It is what passes the arrow from bang to bang.
- With a vector light, its A1 contraction with the twins' current (T1 x T1 holds A1), its strength one integer of the file.

## 6. The choice carried into the next bang (the owner's word of 2026-10-28, 15:4x UTC)

The owner's word (Hebrew, translated): "And try to reach the part where the draw, if it chooses one direction, then in the next bang perhaps the other direction is chosen. Do you understand what I am trying to achieve? That the detector's choice influences its choice in the next bang, for some reason."

- **In clocks, the reason is the turnover.**
  - The turnover is T on every gear, the clock's film run backward, and a spinning top in a backward film spins the other way: T sends S to -S.
  - What a click wrote stands through the reversed run (item 11 (o), way 2), so a direction chosen in one bang comes into the next bang reversed: chosen up, it reads down there, and up again in the bang after.
- **On the board** (twin_flip.py, the twin calibre at 5,000,000 quanta, T = J K):
  - at each clock the two twins hold almost equal wind, and which twin holds more, the sign of the spin's z part, flips at every bang: up, down, up, down at clock (0, 0, 0) through the 7th to the 10th bangs, and the opposite at its three neighbours (the pair's other ends);
  - at the 11th bang the new births of down twins write over the flip, and it stays down. CHECKED.
- **So the choice is remembered, reversed, from bang to bang.** By itself it is a period of two, the palindrome both reviewers found, and the new clicks of each bang are what break it (way 2).
- **What the owner asks for further,** a fresh draw whose odds the last choice moves, needs the last choice to reach the next draw's frame. In clocks, the reversed spin bends the light's lead through the spin's coupling to the current (S . J, item 5). The next fitting then lays its vector pair along that lead (law C), and the next detector draws in the frame the last choice left. OPEN: the next toy reads it.
- In this toy no detector's click wrote the spins (the split chime fires 0 times here): the births and the twins' own motion wrote them. The turnover's flip acts on any record alike.

**The chosen path, in the owner's next word** (15:4x UTC, translated): "A detector's click chooses one path for the future. In the next bang I want it to influence it: the path it chose for the future should not disappear; it should influence it."

- **In clocks, the chosen path becomes the next bang's detector.**
  - A click writes its chosen path as a twin pair with a definite direction: the record.
  - The reversed run leaves it standing (way 2), and the turnover only reverses it (T).
  - Law 6's detector is "a second twin pair at the Node-clock", so in the next bang the record is the detector at its clock. The next child there is clicked along the axis the last choice left, with the shares (rho + S . m) / 2 and (rho - S . m) / 2.
  - The spin's coupling to the current (S . J, item 5) bends the light's lead along the record, so the next fitting lays its child along it (law C), and the last choice moves the next draw's odds.
  - The coupling's strength is the twin train's integer in the universe file.
- **The toy** (chosen_path.py; one Node-clock over 4,096 bangs, the 24's axis directions in integers, the board's draw by a fixed stream of fair digits). CHECKED.

  | what crosses into the next bang | next choice on the last choice's line | last choice reversed | fresh draws |
  |---|---|---|---|
  | nothing: the exact rewind undoes every click | 1,343 of 4,095 (a third) | 686 (a sixth) | 4,096 |
  | the record, as the next detector (way 2) | 4,095 | 2,033 (a half) | 4,096 |
  | the record, also bending the next child along it | 4,095 | 4,095 | 1 |
  | the record, bending the next child half along it | 4,095 | 3,085 (three quarters) | 4,096 |

- **So the chosen path never disappears under way 2.** It carries the next click's axis always. Through S . J it also moves the next choice's odds, from a half to certainty as the coupling grows, while each click stays a draw below that.
- **Bell through the circle reads the same way:** each bang's pairs are clicked in the frames the last bang's records left, in their common past.

## 7. What stays open

- Pauli's exchange sign: law 7's premise, draft J.
- Bell at a distance: Bell's theorem leaves no local law that gives it; the cone route stands within the common past.
- The composite's binding and the density step's form (David).
- The draw's fairness (item 6).
- **The next toy:** A, B and C together on the one big bang, which needs the joint dial as a state. It is to read per bang the detector's clicks, the composites, the births, and whether the light is spent in a burst.

---
Animate, reader-5.
