# Problem solving: how the project advanced

One line per problem: what was wrong, how it was solved, who solved it. The
model owner is Alon Gonen; Boss is the orchestrating agent; a specialist is
an agent dispatched by Boss for one bounded task. Model decisions are the
owner's; formulations marked "Boss" are the orchestrator's wording or
elaboration of the owner's decision, and a specialist's entry names the
feature, run or fix it delivered. Dates are 2026-09-17 and 2026-09-18 unless
stated. The register of runs is [EXPERIMENTS.md](EXPERIMENTS.md); the
decisions themselves are in [HIGHLIGHTS.md](HIGHLIGHTS.md).

## The field

| Problem | Solution | Who |
| --- | --- | --- |
| The spreading field's sub-quantum shares were placed by phase, so the remainder wandered between headings and the screen's counts depended on the phase rule. | The Node owns the remainder per family and heading, and a whole quantum leaves when a heading reaches one (`field-remainder-v1`, feature 12b). | Decision: owner. Feature: specialist. |
| Nobody knew whether the engine's integers reproduce the mean field of the split table, or what law the field follows. | The mean field was solved as a fixed point (Gauss exact on the GameBoard, J = 11/8 Φ, 1/r² on the axis from r ≈ 21, t90 ≈ 1.5 r²); A5s Run 2 in dense mode measured the engine equal to it to a part in a thousand at r = 12, 16 and 20. | Question: owner. Derivation and runs: specialists. Reading and registration: Boss. |
| The field reaches distance r only after t ∝ r² ticks: it diffuses, it does not propagate like light. | Recorded as an open item of Highlights 3.5 (a phase-steered split would be needed for a wave equation); not solved. | Finding: specialist (mean-field research). Open: owner. |
| Is the force 1/r or 1/r², and are the books between release and meeting closed? | E11 read the field shell by shell without assuming a power law: content per Node ≈ 1/r near the source, radial momentum per Node exactly 1/r², flux constant through every shell; the books balance at every tick only with a source line (the emitter pays nothing, a push creates −3·a·h). | Question and the shell-by-shell method: owner. Run: specialist. |
| Large GameBoards ran out of time and memory (r = 20 needed 3 hours and 11 GB; r = 24 impossible). | The dense field mode (pure-field Nodes as vectorized integer arrays, state and ledger identical to the engine's), 94–145× faster on filled GameBoards; r = 20's final snapshot was still killed by the memory cgroup, and its result was read from the events. | Mode: specialist. r = 20 reading: Boss. |

## Matter and its motion

| Problem | Solution | Who |
| --- | --- | --- |
| A bound group was a ray held at one Node by a rule with no outputs, so any content bound and there was no ladder. | Binding is a periodic orbit of the meeting table on a ring of four Nodes (`loop-binding-v1`, feature 14); the electron at rest, absorption, emission and photofission all run as loops with exact books. | Decision: owner. Feature and runs: specialists. |
| A free ray at the speed of light could not orbit a nucleus (E8: an arc, then escape, on 15³ and 21³). | Recorded as a finding; the momentum turn was fixed to keep the ray's walk (`ray-momentum-turn-v2`) and the run repeated; the escape stands. | Runs and fix: specialists. Reading: Boss. |
| Two electrons' fields had to push each other by a rule that did not exist. | The momentum register (feature 8b) and the momentum table; A5 measured Δp = 3 at b = 4 and attraction of opposite charges. | Decision: owner. Feature and run: specialists. |
| Light passing a mass: does it bend, by what law, and does G_eff N² hold? | A6 measured the momentum form bending within 1.4 % of the mean field, linear in M, mirrored; the pre-registered delay table bends nothing; the exponent is the GameBoard's; light and a slow ray bend alike (ratio 1, not 2); G_eff is constant over N and G_eff N² is not. | Question: owner. Series: specialist. Analysis, docs and PR after the specialist stopped: Boss. |

## The Detector

| Problem | Solution | Who |
| --- | --- | --- |
| A screen beside a ring at rest stopped clicking at tick 72: the clicked quantum spread on with its bit and the bit reached the other marks (E9). | A click is an absorption: the realized quantum ends in the mark's counter with its momentum on the marks' line (`detector-absorb-v1`, feature 2c); E9 repeated counted 265 with no pass. | Finding: specialist. Decision: owner. Feature: specialist. |
| Is the Detector's draw needed at all? | E12: a counter without a draw reproduces the whole screen; the draw only partitions the same arrivals by efficiency; the record is the same under another seed; two sources in phase and antiphase give identical counts. | Question: owner. Run: specialist. |
| The Bell price: could a transmission (bit 0) ever be drawn again? | Left open; then superseded by the law of the bit (a mark meets a 0 or a 1, nothing is drawn). | Owner. |

## The law of the bit (2026-09-18)

| Problem | Solution | Who |
| --- | --- | --- |
| The emitter pays nothing and a meeting creates momentum: the world conserves only in the books, with a source line. | The recoil is the field ray itself turned back with the opposite momentum (Newton's third law at every push). | Diagnosis: E11 (specialist). Proposal: Boss. Decision: owner. |
| Should the emitter pay for its field? A body radiating its mass away is not physics: a static field is free, radiation costs. | The distinction is not the family but the bit: 0 the shadow (free, pushes, returns), 1 the thing (real, counted, paid). | Objection: owner (an emitting electron would lose its mass). Reframing: Boss. Decision: owner. |
| A screen counts a static field forever: free energy. | A mark absorbs only a thing; a shadow is returned; an electron is seen through real light scattered from it, not through its field. | Owner. |
| What is radiation, what is matter, what is a field? | There is no light and no matter: one kind of content, the ray, with declared properties and one bit; a shadow is the same family with bit 0. | Owner. |
| What of the field that never meets anything, streaming out forever? | A thing does not emit; its shadows are given with the GameBoard (a declared profile or the mean field's steady state) and circulate: a shadow that comes home leaves again from where the thing now is. | Standing-field proposal: Boss. Decision and "a thing does not emit": owner. |
| The return arrives at the release Node and the thing has moved. | Each Node remembers the heading the last thing left by; the return follows the trace; a thing at the causal speed is never caught. | Question: Boss. "It chases it": owner. Local rule: Boss. |
| A thing pushed by its own shadow: self-force. | A shadow meeting its owner is home, absorbed back, never a push; shadows carry their owner's identity. | Owner. |
| Does a pushed electron become a possibility (bit 0), since we no longer know where it is? | No: a thing has one path and only one, decided at every meeting by the coupling; the bit never changes at a meeting; what the observer does not know is the observer's. | Proposal: owner. Objection (mass, field, dissolution): Boss. Decision: owner. |
| What has mass, what costs computation? | A thing's content is mass, advances a clock and delays a Node; a shadow has none and moves at the causal speed; the world's computation is the things' content, constant between absorptions. | Owner. |
| Where do events happen? | Only at Nodes holding a 1; the GameBoard has two layers, thing Nodes cycled in full and shadow Nodes as one step or a formula; the dense mode is the shadow layer. | Owner. |
| Is the lottery real? | No: a mark meets a 0 or a 1, decided at birth and along the path; an imperfect mark is a declared table; no RNG in the engine. | Owner. |
| One general statement of all of it. | "Every action is a message that returns": 1 is what there is, 0 is what is said; what is said returns, what there is stays. | Formulation: Boss, at the owner's request. |
| Does one meeting in the field cancel the other branches ("the universe chooses one path")? | No: locality; each share is realized where it meets or never; the books close per share; stopping the spread after a meeting would break Gauss. | Question: owner. Answer: Boss. Locality reaffirmed: owner. |

## Process and tooling

| Problem | Solution | Who |
| --- | --- | --- |
| The viewer's camera fit left loops tiny; the owner could not see the runs on the phone. | The events fit (`camera_fit: "events"`) and a run document's own box; shorter labels. | Complaint: owner. Fix: specialist. |
| The phone GIFs came out white and grey and too large. | The palette was a median cut by population on a dark scene, dropping the few saturated pixels; maximum coverage keeps every colour; 480 px, 12 frames: 65–137 KB each; GIFs are delivered inside an HTML page. | Complaint: owner. Diagnosis and fix (PR #261): Boss. |
| Google Drive uploads through the connector take inline content only. | Pages and GIFs are published as artifacts and sent as files; a links page sits in the Drive folder. | Boss. |
| Long runs died when the container was reclaimed after idle. | A monitor heartbeat keeps the session alive; detached runs relaunch skipping completed cases. | Boss. |
| Feature specialists were told to run the whole suite locally, against the skill's rule (affected tests only; the suite in CI). | Briefs corrected to the skill; the owner's rule recorded: no experiments inside a feature, the feature proves itself with its own test. | Correction: owner. Skill: existing. |
| Boss attached proposals and offers to every answer. | Recorded in the boss skill: answer the question and stop; propose only when asked or when genuinely important, in one sentence. | Owner. |
| Old-law experiments (E12's viewer extraction) kept running after the law changed. | Stopped; every run from here on is under the law of the bit, one by one after feature 15. | Owner. |

## What is open (as of 2026-09-18)

- Feature 15 (`bit-law-v1`): the law as the engine's only behaviour; the
  returns aggregated in the shadow layer (the performance review's design).
- The owner's declarations the law does not fix: the size of the shadow set
  X (the force constant), the rounding of a prefilled field to whole quanta,
  and what becomes of a thing's shadows when a mark absorbs it.
- The repeats on the final law, one by one: E9, E11 (a), A5, E8, E10, A6;
  then A1 (two slits), E13 (annihilation), A13 (Bell as a function of
  efficiency and geometry).
- The diffusive spread (t ∝ r²) against light's straight propagation.
- Derivations from the Node operator (Newton, Gauss, diffusion, E = m,
  bending, the moving clock, G, gravity on a quantum) in `DERIVATIONS.md`.
