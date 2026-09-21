<!-- The physics-rule reviewer's read-only review of 2026-09-20 of the fraction-free counts (records 147 and 148), copied verbatim from the reviewer's scratchpad; its scripts `crowd_replay.py` and `pair_by_ordinal.py` are described in its scope paragraph and not shipped. -->
<!-- Built as BEAM_LAW note 41 and MIGRATION "The fraction-free law"; nothing here is edited. -->

# The fraction-free counts under a changing rate: which count is the law's (the physics-rule reviewer, read-only, 2026-09-20)

**Scope.** The Boss's four questions on the implementer's finding (branch
`fraction-free` at a2120413 plus the held patch `ff_stage1_counts.patch`,
applied cleanly in my own scratch worktree, removed at the end): FORM.md's
"constant-rate counts are bit-identical" fails on the register because a
paid lamp's content falls at every birth and a crowd changes at every
interval, so every lamp world and every crowd world moves under the
accumulator. About 40 minutes; no repository file edited, nothing committed.
My own replays (each at most 200 intervals): `bell/a0_b0` (160), the four
CHSH pair worlds of series L3 and `mz_equal` (80 + 12), `weak/j3_deuteron`
(200, twice: through the runner and in-process recording the crowd per
interval), on the base a2120413 and on the patched tree. The implementer's
full 700-interval replays of the deuteron (`scratchpad/fraction_free/runs/
gate_base`, `gate_head1`) are cited where a 700-tick fact is needed. Scripts
and outputs beside this file (`crowd_replay.py`, `pair_by_ordinal.py`,
`runs/`, `bell_only/`).

## 1. The physical count for a rate that changes: the accumulator

**The two forms.** `by_clock(age, n, d) = floor((age + 1) n / d) - floor(age
n / d)` with `n` the CURRENT rate (`src/event_universe/core/integer.py:58-70`
on main; the turn `engine.py:419-473` `_frame_all`, the owed count
`engine.py:119-129` `count_owed` and `:476-486` `_suspend`, the release and
the lamp `nature_beam.py` at the self-creation). The accumulator: `acc +=
n_k` at each self-creation, one unit each time `acc` crosses `d`, `acc -=
d` (`by_drive`, `integer.py:73-102`; the patch lines 141-176, 196-250,
379-413). At a constant rate from age 0 they are the same integers (FORM.md
section 1, proved; the patch's test (a)). At a changing rate they are not,
and the difference has a sign and a size:

- **E = h f.** The turn is the lamp's frequency: `s` phase steps per
  self-creation at `content x n / d` (the free release's own form, BEAM_LAW
  note 33; step 5, `docs/BEAM_LAW.md:489-536`). A lamp PAYS at every birth,
  `cost = quantum x turn` per unit (`nature_beam.py:3780`, `:3862-3863`), so
  its frequency falls at every birth: on `bell/a0_b0` from `K + 2` by 2 per
  birth (the lamp's content at tick 160: 1048258 on main = 1048578 - 2 x
  160). The number of turns a clock of frequency f has made is the whole
  part of the integral of f over its history; that is the accumulator's
  count and nothing else: `sum_k M_k / K` on `a0_b0` is 3 exactly after
  three births and `4 - 4/K` after four, so the fourth step is not complete
  at tick 4 and the exact clock births at ticks 1, 2, 3, 5, ... (the
  implementer's "stall at tick 4" is the clock's truth, not a defect); 159
  births in 160 intervals and the phase 31 (`gate_head1/a0_b0`: phase 31,
  `acc.turn` 1023768 = 2^20 - 24808, the integral 159.976 turns). `by_clock`
  credits 160: at age a it reads `floor((a + 1) M_a / K) - floor(a M_a /
  K)`, the whole part of a history that ran at TODAY's content, which never
  happened; its sum over the history telescopes only at a constant rate
  and otherwise has no invariant. Measured on the same lamp (K + 2, paying
  2 per birth, my drift script): by_clock births minus the integral's whole
  part = +1 over 160 self-creations, +3 over 2000, +9 over 20 000, +1089
  over 200 000 (0.66 % of the lamp's births credited to no frequency). The
  books balance either way (each birth is paid); what drifts is the
  relation of the phase to the energy, E = h f itself.
- **The crowd.** The owed count is the clock's slowing by the presence,
  `k n / d` per self-creation (note 25, `docs/BEAM_LAW.md:1399-1470`; step
  5): the waits of a clock are the integral of the potential along its
  history, not `age x k_now / d`. On `j3_deuteron` the crowd a nucleon's
  clock reads changes at every interval (the fan's rows dwell 1 or 2
  intervals: 128 800 and 104 880 at the proton, 128 590 and 104 709 at the
  neutron; `crowd_replay.py`). Over 200 intervals (my in-process replay on
  both trees): the proton's clock read `sum k n / d` = 19.294 over 177
  self-creations and `by_clock` wrote 23 waits; the neutron's 18.963 and 22
  waits; under the accumulator 19.953 -> 19 waits and 19.921 -> 19 waits,
  the whole part of the integral EXACTLY on both bodies, `acc_owed` 999 696
  and 965 583 below d = 2^20. `by_clock`'s four extra waits per body (+21 %)
  are the "burst" at the lower crowd: `floor((a + 1) k' / d) - floor(a k' /
  d)` at k' = 104 880 fires whenever the phase of `a k' / d` happens to
  cross, crediting the whole age with a crowd it did not have (the log:
  ticks 22 and 12 fire at the lower crowd on main, none on the patch). Over
  700 intervals (the implementer's replays): 80 waits against 69, the same
  excess.
- **The local integer operation contract.** "A rule that permits division
  with remainder must declare the existing bounded remainder owner, update
  and lifetime; do not silently discard a remainder"
  (`docs/ARCHITECTURE.md:80-82`). `by_clock` keeps no remainder; note 17's
  exemption (`docs/BEAM_LAW.md:1048-1123`, its last sentence: "'No remainder
  is kept' above stands for the clock, the release, the lamp and the owed
  count, which read a rate against an age no push changes") is sound only
  because at a constant rate the remainder is `(age n) mod d`, a function of
  the age, so the age is its owner. When the rate changes the remainder of
  the history is a function of the rates that were, which the record does
  not hold: it is discarded, undeclared. On the register that premise fails
  for every lamp (every lamp is paid: the kind follows from the quantum,
  and a paid lamp spends at every birth: the chooser worlds' own generator
  says so, `examples/events/bell/make_chooser_worlds.py:55-56`, "a paid lamp
  spends its content and its turn drifts") and for every crowd on a fan.
  The accumulator is the remainder owner the contract asks for: one bounded
  integer below d on the reader's record, updated at each self-creation,
  nothing at a Node (the patch's `Measured.acc_*`, lines 269-320; test (e)).
- **LOCALITY-1** (`SIMULATOR_DEFINITIONS.md:353-362`). Both forms are local
  in space: the age and the current rate are on the record, as is the
  accumulator. `by_clock`'s re-evaluation is therefore not a non-local
  reading of the past; it is worse in kind: the past is not read at all, it
  is overwritten, every earlier self-creation re-priced at the present rate.
  The count at a change of rate then depends on the phase of the age
  against the new rate, that is on when the body started, not on what
  happened to it (the "stall and burst" of RULES.md section 1). This is the
  same primitive and the same defect the owner already rejected for the
  step (note 17 as amended: "stalled a body for tens of intervals under a
  falling momentum and then stepped it at every interval ... the Links made
  equal to age x v_now"; record 108, "a generic solution if he can"), and
  FORM.md section 1 (ii) (`docs/designs/fraction_free/FORM.md:43-56`) named
  the owed count, the release and the turn as the same case; what FORM.md
  under-counted (its section 7 line 1 and reason (iv)) is that on the
  register there is no constant-rate lamp and no constant crowd on a fan,
  so its "bit-identical" theorem describes the primitive and not the
  register's worlds. The implementer's finding is that correction, not a
  contradiction of the law.

**Answer (1):** the accumulator (the exact whole part of the running sum) is
the physical count under E = h f, under note 25's clock, and under the
contract; `by_clock` at a changed rate is a count of a clock whose history
was rewritten, local but a-historical, with a drift that has no bound.

## 2. The Bell worlds: an artifact of the worlds' timing, not of the correlations

**What fails and why.** The Bell design fixed the pair lamp's content at
`K + 2` "so that the release of age a is stamped with the phase a mod 64
exactly for every age of the run" (`examples/events/bell/README.md:28-30`)
and reads "the age of a click as its tick less its Node's offset, read off
the record itself" (`README.md:47-50`; `tools/bell_chsh.py:16-20`,
`:166-175`). Both are true only under `by_clock`, whose credit of one turn
per self-creation for 160 intervals is the drift of section 1 in the
lamp's favour; `K + 2` is the smallest content that hides the stall from
`by_clock` for the run's length. Under the exact clock the birth of tick 4
is missing and every later birth is one tick later, so the tool's `tick -
phase` gives two offsets per Node and the tool's ages, pairs and windows
are misread: on my `a0_b0` replay (`bell_only/ff_review`) 18 criteria fail
against 11 on the base (the base's 11 are the one-click re-run's, pinned):
"every click's phase is its age mod N: False", "exactly one outcome per age
on alice's side: [3]", "every analysed pair counted: 127 of 128", E(0, 0) =
127/128 (`tools/bell_chsh.py:205`, `:228`, `:246`). The implementer's
"E(20, 44) found 1 expected -1/2" of `test_bell_choosers` is the same
misreading with fixed streams: the tool pairs Alice's and Bob's clicks by
`tick - offset`, and one offset per Node no longer exists.

**The correlations themselves are unchanged, bit for bit.** The click of a
record is a function of its birth phase u and the settings alone (the
ladder, note 37 (iv); `u = (births - 1) mod N` is the record's own field:
on the patched `a0_b0` the births at ticks 1, 2, 3, 5, 6 ... carry u = 0,
1, 2, 3, 4 ..., `gate_head1/a0_b0/run/events.jsonl`). Read by BIRTH
ORDINAL (the first 64 records of the lamp, `pair_by_ordinal.py`, both
trees): `bell_0_8` cells 27, 5, 5, 27 (E x 64 = 44), `bell_0_24` 5, 27, 27,
5 (-44), `bell_16_8` and `bell_16_24` 27, 5, 5, 27 (44), every u once,
**S = 176/64 exactly on the base and on the patch**; `mz_equal` 64 gathers
on D1 and 0 on D2 on both, the last gather at tick 76 (the test's bound).
Read by the tests' TICK window (born in ticks 1..64: `tests/
test_amplitude_pair.py:90-101` `gathers_of`, `tests/test_amplitude_layer.py:
179-181`) the patch gives 63 records (the birth of tick 3 is missing in
these worlds, K = 15 x 2^20), the cells 27, 5, 5, 26 and the Mach-Zehnder's
63: the implementer's failures, all of them a window of ticks reading a
lamp whose ticks moved.

**The re-alignment, of the readers or of the worlds, never of the law.**
Either of two, both restoring S = 176/64 and the 11 base criteria:
(a) the tools and tests read a pair by the record's identity (the birth
ordinal), not by `tick - offset` or a tick window: `bell_chsh.py` and
`bell_choosers.py` pair Alice's and Bob's clicks by the `record` column the
click line carries under the one click, and the L tests take the first 64
records; the world files stay byte-identical and the runs re-register by
their dated lines (every birth tick after the stall moves by one); or
(b) the worlds' lamps get the content the exact clock needs for one birth
per interval over T intervals, `K + 2 (T - 1)` (a lamp paying 2 per birth
must start at least 2 (T - 1) above K: `K + 320` on `a0_b0`; the
accumulator then stays at `a (2T - 1 - a) < K`), which aligns phase = age
under BOTH counts (checked: with `K + 160` over 160 intervals by_clock and
the integral both give 160 births, the first exact stall at tick 162) and
makes the alignment a statement about the lamp instead of a by_clock
artifact. I prefer (a): the register's claim is then read from the record
and not from a tick, and (b) can be added to the Bell README as the rule
it always was. The chooser worlds (`read`, `one_clock`): the setting a
pair meets is the stream's phase at the click's tick, so the one-tick
shift re-pairs births with settings; but every bin's E is a function of
the 64 u's of the bin (each bin holds every u once over a full period of
960 shifted births, the periods 5, 3 and 64 coprime), so the design's E
list and S = 156/64 hold by ordinal once the window starts after the stall
(born from tick 9, or the records from the 8th); not run here (1000
intervals), stated as the argument for the re-registration to check.

**To record:** S = 176/64 does NOT depend on the alignment; it is a
function of the births' u over one circle and the settings, and my replays
show it invariant under the change of count. What depends on the alignment
is every reading that takes `tick - 1` for the lamp's age or a tick window
for a set of births; the register should say "the age of a pair is its
birth ordinal (the record's identity); the tick of a birth is not the age
of a lamp's clock once the lamp pays", and the bell/ README's `K + 2`
sentence should be replaced by the rule of (b).

## 3. The deuteron: the accumulator's 69 is the law's count; the verdict stands

The law's count is the integral of the crowd (section 1: 19 waits of 19.95
at 200 intervals exactly on both bodies under the accumulator; 23 and 22
under `by_clock` for 19.29 and 18.96). Over 700 (the implementer's
replays): 69 waits in place of 80 on both bodies, 11 waits `by_clock`
charged to a crowd the clock never read. The registered verdict
(`examples/events/weak/README.md:252-259`, "the deuteron holds again: 0
steps of 33 and 29 attempted, the neutron fires at 577 and its beta clicks
the shell at 590 with the content 3"): under the accumulator the pair holds
on the same two Nodes for 700 intervals (`gate_head1/j3_deuteron`: (10, 10,
10) and (11, 10, 10), `axis_steps` 33 and 31, every attempt a refused
contact, 64 contacts against 62), the neutron fires at 568 with the same
`counted` 128 590 and the same products and recoil, its beta clicks the
shell at 581 with the content 3 at the same Node (13, 16, 6); at 200 the
contacts fall on the same first tick (17) and thereafter in pairs one tick
apart (17, 18, 35, 36 ...) in place of the base's (17, 21, 38, 44 ...): the
two clocks now wait at the same intervals, which they should, reading the
same crowd. So: BOUND stands; `p = 0` in the sense of record 139 (no Link
made, no self-propulsion) stands; the trigger tick moves from 577 to 568,
outside the "574 or up to 3 before" window (`README.md:244-246`), which is
the pinned tick of a wait-count that was `by_clock`'s and re-registers by a
dated line; the beta's click 590 -> 581 likewise. One observation for the
physicist's re-reading, not a claim: the pair's measured momentum at 700 is
[-19, -58, 19] under the accumulator against [1.62 x 10^11, -58, 19] under
`by_clock` (the base's x is one contact's hand not yet returned at the last
tick; at 200 the base holds [+3.1 x 10^11 on the neutron, 0 on the proton]
and the patch [+3.1 x 10^11, -3.1 x 10^11], the pair's sum 0). The
`j3_deuteron_crowd` gate world reads the same way (69 for 80, 36 and 33
attempted, no transformation, `gate_head1`).

## 4. Recommendation

**(i), the full unification**, with the Bell readers re-aligned by the
record (section 2 (a)) and every lamp and crowd world re-registered in one
batch with dated lines, the Bell pins re-read by ordinal. What it costs:
the register's replay is most of the 109 worlds and not the pushed ones
only (every lamp world, every world with a crowd on a fan, every cavity
world: the gate set's 14 of 16 moved in the implementer's replay; a batch
of hours under `--full`, made once), the two Bell tools and the L tests'
windows rewritten to read by record, the deuteron's and every "first
difference" tick re-pinned (577 -> 568, 590 -> 581), note 41 stating the
one discarded count that remains (a lamp's count at a self-creation of
turn 0 or outside the window is taken out of the accumulator and lost, as
the clock's was, not banked: the patch lines 379-392, a declared choice to
write down) and the Bell README's `K + 2` sentence replaced by `K + 2 (T -
1)`. What it means for the claims: one primitive, the remainder owned on
the record as the contract asks, E = h f exact in the integral, the
clock's dilation the integral of the potential, and the register's
correlations proved invariant (S = 176/64, the cells, the Mach-Zehnder
ports, bit for bit by ordinal). **(ii)** costs less today (the pushed
worlds only, once more) but keeps `by_clock` for exactly the four counts
whose constant-rate premise is false on every registered lamp and every
crowd, with a docstring ("a rate no push changes") that is true of the push
and false of the birth's cost, a phase-frequency drift with no bound (+1089
turns in 200 000), a contract exemption (note 17's last sentence) that no
longer holds, and a Bell alignment that is a by_clock artifact hidden by
`K + 2`; the law would then carry two count forms, one of them the form the
owner already retired for the step for this very reason, and the next paid
lamp or fan crowd would reopen the question. The evidence for (i) is
complete on the small worlds; the Bell chooser worlds and the crowd worlds
of series G2, K and the cavities are to be read in the batch, by record,
before their lines are dated.

**RECOMMEND (i):** under E = h f the count of a clock whose rate changes is
the whole part of the integral of its rate, which the accumulator holds
and `by_clock` overwrites, and every count on the register changes its
rate.
