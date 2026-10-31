# The hostile mathematician (THIRD pair) on LIGHT1 (the wave's clicks with a clock), 2026-10-31

(Written by the Boss from the reader's hand-back, 04:5x UTC, the reader's harness refusing the write; the text is the
reader's, shortened in layout. Evidence in light1_math/: kprobe/p_light1_k.py (the teeth at a probe key),
kprobe/p_chain.py (2.3's chain rule), runA/ and runB/ (two reruns, byte-identical to the frozen run1, digest
0e24f4d25cdc29d8). All finished before 04:55.)

VERDICT on LIGHT1: NOT PASSED

The edge split, its pairing and its pair of teeth are sound. Two items are BLOCKING: reading 7's echo rule cannot fail
as written, and the measured claims about the teeth cannot fail at key 1.

## BLOCKING

B1. Reading 7's rule (2.3) cannot fail as written, and the "no echo" verdict uses a criterion the rule does not state
(sections 2.3, 4 "ECHO: not in this record", 5.1).
- As written, an echo between A and B is a chain out from A's give to B's take, then back from B's give to A's take,
  each link to a neighbouring place at a later round.
- Measured on the shipped record (p_chain.py; each line a relay from its giving end to its taking end, at strictly later
  rounds): chains out and back exist for 3,456 of 11,344 ordered pairs of places at 2 Meshes or more. The rule as
  written finds thousands of echoes in a record the text says has none.
- The verdict rests instead on "no place falls quiet and clicks again", which is not in the rule; and that clashes
  with the text's own probe, which counts 135 quiet gaps (up to 7 rounds) after which lines resume, dismissed by their
  length ("no place has a gap over 20"), while 2.3 says the rule "picks no threshold".
- With A's quiet written in (no line at A strictly between its give and the return's take), the rule needs no
  threshold and can fail; here it reads 0 of 11,344, agreeing with the verdict.
- Fix: state the rule with A's quiet and the relay linkage (each link a give at one end of an edge and the take at its
  other end, the next link given from that place at a later round); run it in the probe and report 0 on this record;
  say what record would pass it.

B2. The teeth's MEASURED claims cannot fail at key 1, and the probe's run back is built so that it fails at any other
key (1.4 "MEASURED: 0 missed"; 3.1 "0 of 45,000"; 3.2 edge by edge; section 6; p_light1.py line 98).
- At the file's key, K = 1, every carry is carry(S, 1, 0) = (S, 0): no edge's tooth ever leaves its birth (measured: 0
  of 360). So the complement, the teeth's run back and the teeth's turn are all identities on zeros.
- p_light1.py starts every run with the teeth at birth, the backward run included, while the text's 3.1 keeps the
  tooth.
- Measured at a probe-only key K = 1,000,003 (an identity test, not a claim about the world): as built, the run back
  misses 4,026 of 45,000 quotients, and only 148 of 360 teeth return to birth (212 had moved); started from the
  forward's end teeth, it misses 0 of 45,000 and all 360 teeth return; the complement misses 0.
- So the teeth are correctly DERIVED (Rule3's complement and the carry's sign law), not MEASURED.
- Fix: start the backward run from the forward's end teeth and compare the final teeth with their birth; label the
  teeth DERIVED, the K = 1 measurement called vacuous; exercise them at a probe key above 1, named as such.

## MINOR

1. The split is exact and unique as the matrix of the Mesh contraction (a linear map's entries are unique; 0 entries
   missed). The per-Spoke wording of 1.2 matches it only where an axis's two Spokes reach distinct sites (sides of 3 or
   more); on sides of 1 or 2 they cancel, and the probe measured the summed entries. Fix: define the edge as the matrix
   entry, summed over the Spokes that reach the same partner.
2. Why the two ends hold the same c: the plan's two halves are adjoint (J_l = F C D m, J_m = -F C D l, D antisymmetric),
   so the coupling matrix is symmetric; that is what makes P_wave = -P_tied an identity, since P_wave + P_tied =
   (c_w - c_t)(x_w y_t - y_w x_t). Say so in 1.2.
3. The probe types a literal 2 for the birth (line 43) and in turned (line 198); the loader reads it as senses
   (load.py:176, carry(key - 1, senses, 0)). Fix: read it with step.halves(layout).
4. For an even key the birth (K - 1) div senses differs from its complement by 1, so which end holds the lower tooth
   is a convention; at odd keys, K = 1 included, the birth is its own complement. Name it.
5. 3.2 contradicts itself ("complement exactly where a turn negates its passing ... never", then "a turn that negates
   a row complements the edge's teeth"); the half turn about z negates T1_x but complements nothing, the Spoke
   reversing too. Fix: the edge's teeth follow the passing's parity, never a row's alone; the row rule is the gear's
   tooth's.
6. The half turn about z keeps every passing: derived for every edge of a cubic board (on x and y edges the row's sign
   and the Spoke's sense flip together; on z edges neither flips); measured only on the x edges, the y and z edges
   vanishing on sides of 1.
7. The probe's reported windows are typed: 40 rounds (line 135), a gap over 20 (line 148), the places 16 to 23 and
   round 60 (lines 149, 150), quoted by the text. Fix: read the lay's places from setting.json.
8. The engine is imported from scratchpad/scanZ/src (line 14), outside the frozen folder; the reruns reproduce only
   while scanZ stands at 49e97c992. Fix: freeze the engine with the text.
9. The shipped world's universe.json names its cards "light", "held" and "matter", board labels the owner's 03:2x line
   forbids (LIGHT1 reads by kinds and is unaffected). Name it in the text for the world's owner.
10. Roads 5.1 and 5.3 are one: at K = 1 every unit of passing is a line, and the lay's places keep clicking long after
    the front (941 lines after round 60; 5,888 lines more than 40 rounds after their place's first). So in 5.1's echo
    world A would not fall quiet while any tail remains; B1's quiet rule then needs a tail exactly zero or a key set by
    the structure (5.3). Say so in 5.1.

## SOUND

- The pairing an identity once the ends hold the same c (MINOR 2); equal ends measured 360 of 360.
- The split matching the engine's Mesh contraction with 0 entries missed, both slots, 125 rounds; a check that can
  fail.
- Rule3's complement correct algebra, measured non-trivially at K = 1,000,003 (0 missed, 212 teeth moving).
- The run back's oddness right: P(y, x) = -P(x, y), so S becomes -S and the kept tooth returns; measured at
  K = 1,000,003 with the teeth kept, 0 of 45,000 missed.
- The 24: why 8 turns (16 signed permutations send x to +-x, 8 proper); the passing the A1 product; 0 of 8 turns
  differ, 0 quotients missed edge by edge.
- No sign test or INDICATOR in the edge's act (one kept-tooth carry per edge per round, plus its complement); the
  selector in 2.2 belongs to the decoder and reads kinds.
- No number picked (F and K from the file, the birth from the loader's rule).
- Reproduced: two reruns byte-identical to the frozen run1, digest 0e24f4d25cdc29d8.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED: the split, the equal ends, the pairing, the complement, one tooth per component, the run back's oddness, the
  8 turns and the A1 product.
- MEASURED: the text's (equal ends 360 of 360; the split 0 missed; 25,312 lines summing to 0; the passing's run back;
  the 8 turns); the reader's (the teeth at K = 1,000,003 miss 4,026 as built, 0 when kept; the chain rule reads 3,456
  echoes without quiet, 0 with it).
- OVERCLAIMED: the teeth reported MEASURED at K = 1 (B2); "picks no threshold", while the verdict uses one (B1).

## The reader's questions for the Boss

1. Is A's quiet the intended echo criterion for reading 7?
2. With the shipped file fixing K = 1, can any echo be read before the structure sets a key (5.3)?

## Solution24 (the reader's line)

The edge is an exact, lawful split of the engine's own vertex, with a lawful pair of teeth. Before reading 7 stands on
it, its echo rule must be stated so that it can fail, and its teeth checked at a key other than 1.
