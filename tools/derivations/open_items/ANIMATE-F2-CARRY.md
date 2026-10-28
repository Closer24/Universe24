# F2's carry through the clocks and the tensor: a toy check for the plan (Animate)

The owner's words to Animate, 2026-10-28, 14:3x UTC (Hebrew, translated): "When you say carry, is it a clock's carry?" and "Think through the clocks and the tensor what its carry is." F2 is the bound the A1 course stands on (ANIMATE-MANY-BANGS.md, part 4: struck, the course is refused at tick 15). The toys are in ANIMATE-PROBES-3. Every claim is marked CHECKED or OPEN.

## 1. What F2 is on the head

- **The reading:** the tension t of a Spoke is the mean of its two ends' axis gears (meshes.factors). The Mesh's factor is Q = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 (rule3.mesh_factor), the square of the Mesh rate (Gamma - t) / Gamma.
- **F2 reads t into [0, Gamma]:** below 0 at 0 (no Mesh faster than the full rate) and above Gamma at Gamma (the Mesh at a standstill).
- **On the A1 course, F2 acts on every Mesh at every tick** (a1_tension_scale_60.txt). CHECKED.
  - The axis gears are traceless (their sum is 0 to 3) and run in the millions: -833,333 to 1,666,667 at tick 1, and -18,784,058 to 37,568,115 at the top.
  - So the tension falls inside [0, Gamma] at 0 of the 384 Mesh readings, at every tick.
  - F2 makes every Mesh binary: the full coupling along the two compressed axes, and a standstill along the stretched one.
- **The tension over the stretch is small:** t / X runs from -0.042 to 0.083 at tick 1, and from -0.0046 to 0.0091 at the top. The light's anisotropy is a few percent.

## 2. In the clocks

- **The tension is a carry of one gear on another's dial.** The axis gears and the time gear are gears of one regulator: the axis gear counts the Link's stretch along its axis in notches, and the time gear counts the whole stretch X. What the Mesh's rate reads is the axis gear in the time gear's teeth, Rule3's carry: Gamma a = t X + r, so t = (Gamma a) div X, and the remainder r stays.
- **The tension's whole turn** (t = Gamma) is the Link stretched by the whole stretch along its axis: the horizon along that axis, Rule3's own zero of the Mesh rate.
- **The upper side goes.** Read this way, the tension on the course stays between -42 and 83 against Gamma = 1,000, so it never nears the horizon and no act holds it there. CHECKED.
- **The lower side is the light cone.** A compressed axis (t below 0) asks for a Mesh faster than the full rate, up to 1.042 of it. Its carry is the Node-clock's own tick: a clock's time is the carry of its own dial (DAVID-TENSOR24-THE-LOCAL-TICK.md, toys-5 ac22caa8).
  - Where light would cross more than one Mesh in a tick of the great clock, the clock's dial completes more than one turn, and the clock ticks again. Each local tick crosses at most one Mesh.
  - Where the rate is 0 there is no tick: the horizon.
  - Past it the dial runs back, a negative carry: the turnover, as at the time gear's top.

  One dial and one carry on both sides, with no clamp. OPEN: the toy is synchronous and does not test the local tick itself.

## 3. In the tensor

- **The metric's spatial part** is X (delta_ab + h_ab). Its A1 part X is the time gear, its E part h_aa the axis gears (traceless), and its T2 part the shears. The axis gears hold X h_aa in notches, which is why they grow with the stretch.
- **The Mesh rate along an axis** reads the light cone's slope along it, a function of h_aa alone: the E part over the A1 part, the carry above. Its weight (h or h / 2 at first order, against the square in Q) is David's to set (OPEN).
- **The cone** is g(v, v) >= 0 for v = (one tick, one Mesh). The clamp holds the tick fixed and cuts g. The local tick keeps the cone exact and lets the tick follow.
- **The 24** permute the axes, the E part's components and the cone's two sides together, so the reading and its carry are covariant. It is one formula for every Node-clock and every family.

## 4. The toy (A1 calibre, 5,000,000 quanta, 250 ticks, the dial read at the tick's start, BH-S1 struck)

| the tension | F2 | result |
|---|---|---|
| the head's, in absolute notches | held | draft C bit for bit: tops every 47 ticks; F2 acts at 91,776 values |
| the head's | struck | refused at tick 15 (X = 27,218,198,742,186 at tick 2) |
| in the time gear's teeth | struck | the tension -42 to 83; tops at 20, 59 and 83; refused at tick 87; the rewind 20 of 20 |
| in the time gear's teeth | the lower side read at 0, a diagnosis only | 6 tops every 39 ticks; births 96; books 250 of 250; carries 0 and 1; the rewind 20 of 20; the end teeth's fallback 0 |

CHECKED (a1_tension_ratio_nof2_5M_250.txt, a1_tension_ratio_cone_5M_250.txt). F2's upper side goes by the derived reading, and what stands is the light cone alone, whose carry is the local tick. The Meshes now couple along every axis, so the course is not draft C's: its tops come every 39 ticks.

## 5. For the plan

- **F2** (section 30, item 10 (1)):
  - Its upper side is no bound: read in the time gear's teeth, the tension never reaches the horizon on the course.
  - Its lower side is the light cone. Its carry is the local tick, David's asynchronous board.
- **The same carry is what the twin calibre lacks** (ANIMATE-TWIN-TOY.md, part 3). A clock at rate 0 does not tick, so its stretch cannot run past the horizon. A fast region ticks finer, so no step carries more than one turn of the dial.
- **A big law above both, for the owner's list:** every clock's time is the carry of its own dial, and light crosses one Mesh per local tick.
- **How it was solved before:**
  - in numerical relativity, the cone is held by local time steps: refined regions take more steps per coarse step (Berger and Oliger's subcycling, 1984);
  - the asynchronous variational integrators (Lew, Marsden, Ortiz and West, 2003) give each element its own time step and keep the step variational.
- **OPEN:**
  - the weight of the reading;
  - a toy of the local tick on the course;
  - the twin calibre on this reading.

## 6. For the engine, the law and what it leaves (the owner's word of 2026-10-28, 14:5x UTC)

The owner's word (Hebrew, translated): "OK, pass it on for implementation in the engine, with an explanation of which law changes are needed, and maybe the generic solution, by the same way, for what it does not solve." The Boss builds the engine and Animate writes no engine code (the owner's words of 13:31 and 14:4x UTC). The turnover stays as the owner approved it at 14:37 UTC: T on every gear at the time gear's top, and the clicks carrying the arrow (section 30, item 11 (o) and (s)).

**For the engine (the Boss's, after the plan's approval):**
1. **The tension's reading** (meshes.factors): t = (Gamma t_ij) div X_ij, where t_ij is the two ends' axis gears' mean and X_ij the two ends' mean stretch at the tick's start. With no min and no max.
2. **The light cone as the Node-clock's own tick** (David's asynchronous board, one dial per Node-clock):
   - a clock ticks when its dial carries;
   - a Mesh rate above the full rate gives more local ticks, and each local tick moves light at most one Mesh;
   - F2's lower clamp goes with it.
3. **One operation, written once** (Sofer, 6471863755, item 4): BH-S1's Mesh mask, the local tick's rate 0, QR4's held Meshes, H's cone lapse, F5's rate dial and F2's lower side are the Node-clock's one dial.
4. **The twin calibre on it** needs no end teeth's fallback if every step moves the stretch at most one dial turn. That is to check by a toy on the asynchronous runner.

**The law's changes** (Sofer's to enter, on the owner's word):
1. **The Mesh's tension** (The rates, "the tension is the Mesh's"): the axis gear read in the time gear's teeth (the E part over the A1 part), Rule3's carry of Gamma a by X, and not the absolute notch.
2. **Law 11's list of departures:** F2 struck, its upper side by change 1 and its lower side by change 3.
3. **The tick and the light cone** (The tick; Postulate 3, lines 29 and 33):
   - each Node-clock's tick is the carry of its own dial, and light crosses one Mesh per local tick;
   - line 557's "the value last sent" reads the neighbour where it stands at the reading moment (David's correction).
4. **The horizon** (line 1610) **and BH-S1** (line 132): a rate of 0 is no tick, the local tick's arithmetic, and the mask and the restore are struck.
5. **The big law above them, for the owner's list:** every clock's time is the carry of its own dial, and light crosses one Mesh per local tick.

**What it leaves, and a generic candidate for each by the same way** (clocks first, then the tensor, then the 24):
1. **The local tick itself:**
   - the check is a toy, the A1 course and the twin calibre on David's asynchronous runner, with the tension's reading and no F2;
   - Animate's to run if the Boss asks.
2. **The exchange sign of two equal quanta** (law 7's premise; draft J):
   - in clocks, two equal clocks are one joint dial (item (t)), and the approved T acts on it;
   - the candidate is that the exchange of two equal clocks is the full turn of one, T T, the kind's square (Schwinger's route, J's turnover route). The toy holds T T = J J on the board, -1 on the twins, with the rewind exact;
   - it stays a premise until J derives it.
3. **The composite's books** (the wind does not add at a fusion; David's correction):
   - in clocks, the fusion is the joint dial's whole turn, a carry: the composite takes the quotient, and the shortfall s1 (den - p2) + s2 (den - p1) is the carry's remainder, the binding;
   - by law 11 the remainder stays on the dial or leaves as a click of a whole on the light's train (the mass defect radiated, E = mc^2 at the fusion);
   - so the books close as quotient plus remainder, as every carry's do (law 8). David's to derive.
4. **Law 10's missing part** (the owner's direction of 14:37 UTC: "the solution is in the detector's click"; draft K):
   - data for K: the twin hands are the one big bang's detectors' train;
   - on the twin calibre at 5,000,000 quanta, the clicks of the run after the turnover bring births at the 7th and 11th bangs, and the eleven bottoms' states are all distinct (ANIMATE-TWIN-TOY.md, 65d9c2ec).

## 7. Law 10 with F2's carry: the clicks per bang (the owner's word of 2026-10-28, 15:0x UTC)

The owner's word (Hebrew, translated): "So the missing part is solved for law 10? Think in clocks and the tensor." The toy events_per_bang.py counts the log's events in each bang, the refusals by their cause, at 5,000,000 quanta.

| the calibre | the tension | clicks per bang (births and chimes), bang 2 on | the fittings' refusals | the detector's click (split) |
|---|---|---|---|---|
| A1 | the head's (F2 held) | 64, 32, then 0 | "disengaged" 8,576 to 11,456 a bang | 0 |
| A1 | in the time gear's teeth (lower side held) | 0, 0, 64, 0, 32, then 0 | "disengaged" 0 | 0 |
| twins, T = J K | the head's (F2 held) | 64, 32, 0, 64, 0, 96, 0, 64, 0, 160 | "disengaged" 8,256 to 16,512 a bang | 0 |
| twins, T = J K | in the time gear's teeth (lower side held) | **64, 96, 256, 1,152**, then refused at tick 157 | "disengaged" 0; "orientation" 22,592, 8,448, 3,040 | 0 |

CHECKED (the events_*.txt outputs).

- **In clocks:**
  - A fitting needs both ends of a Mesh engaged and a lead across it that names which end is which.
  - F2's standstill disengages every Mesh along the stretched axis, a third of all engagements (the "disengaged" refusals). Read in the time gear's teeth, those Meshes couple again.
  - The light's alike pattern gives no lead along some axes, so the fittings there have no orientation (the "orientation" refusals): that is the alike board's tie.
  - With twin hands and every Mesh coupled, each bang's clicks break the board's sameness. The orientation ties fall, the next bang fits more, and the clicks rise at every bang: 64, 96, 256, 1,152. That is "every bang shows more" for four bangs in a row.
- **In the tensor:**
  - The alike board is A1, and A1 x A1 = A1, so on the A1 calibre no click can make a new kind and the births stop.
  - The twin hands' clicks write non-A1 parts (the leads and the spins, T1), and the ladder's product table climbs from there (part 7 of ANIMATE-MANY-BANGS.md).
- **What stops it:** at tick 157 a step carries the stretch past one turn of its dial, and the run is refused. That is the missing local tick, the light cone's carry, the same piece as in part 2.
- **What is not seen:** the detector's click itself, the split chime, fires 0 times in every run.
  - The fitting writes each twin pair definite along its Mesh (the head reads the light's lead there), so no pair holds its winding split between its twins, and there is nothing for a detector to decide.
  - The singlet laid at the fitting would be axis-blind (E_verify v6: the fitting's spin write commuting with 2O), the A1 part of E1/2 x E1/2. Under it each child's winding is split between its twins, so every born pair's children would click at their detectors and write their axes.
  - That is the owner's "detector's click", for draft K.
- **So, for the plan:**
  - Law 10's missing part has its clocks: F2's carry and the twin hands make the clicks rise at every bang, measured for four bangs.
  - Two pieces are owed: the local tick, so that the course holds; and the singlet lay, so that the detector's click fires.

---
Animate, reader-5.
