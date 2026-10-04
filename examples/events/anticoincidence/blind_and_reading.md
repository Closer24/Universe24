# One photon on two bodies, the anticoincidence: the blind and the reading

The paper's S.57 (the mathematician's 144 and 145, two hands by the law as it stands; the owner's
word of 2026-10-03, 03:25; the redesign of 2026-10-04 at the lay without the uniform mode, two
hands, #1827 comments 5975470305 and 5975568700): a chain of 96 Nodes open on x with both faces
receding, y and z folded; two records of two parts (g, e) of the pair [1, 1299] declared NodeReaders
at two Nodes each, the Nodes 23 to 24 and 71 to 72, 24 Links from the centre each, their six Link
factors 0 so that they stay; one light record of the family `photon` (light's pair, one real line)
laid at the centre as two packets toward both, from 48 toward +x and from 47 toward -x, at k = pi / 4
with the raised cosine of one wavelength beyond the top (so that the packet carries no uniform mode),
its laid share one whole quantum (the books' count 1 read from the loaded world), the control's two;
each record reads the light into e at the transition's weight 6 over one window of 48 intervals, the
passage's end, the run going on to 170 so that the erasing front reaches both packets, and the credit
draws once over both records' outcomes into the light (the taking the exchange at the record's
Node). The blind is `expectation.json`, written by `build_world.py` before any run and never edited
after; the reading is appended here after each run, every number a click (the credit lines over the
trials, `tools/meeting_trials.py`); a reading that misses the blind is a finding, written as such and
never adjusted. The sections below carry the folder's history at their commits: the chain of 24 with
the atoms at the Nodes 6 and 17 and the window of 40, laid at top 1 and edge 3, until the redesign of
2026-10-04 (the last section).

## The blind (expectation.json)

1. One photon: P(A only) = P(B only) = s with s at most 1 / 2, P(both) = 0 exactly, alpha =
   P(both) / (P(A) P(B)) = 0, where independent draws, classical light, give 1.
2. Two photons, the control: P(both) above 0; S.57 (c) gives alpha = 1 / 2 over the ordered pairs,
   two independent sequential takings at one share give 1.

## The reading (branch ion-world, the night of 2026-10-03, 200 trials per world, the seeds 1 to 200)

| world | A only | B only | both | neither | alpha |
| --- | --- | --- | --- | --- | --- |
| one_photon | 101 of 200 | 99 of 200 | 0 of 200 | 0 of 200 | 0 |
| two_photons | 24 of 200 | 47 of 200 | 28 of 200 | 101 of 200 | 56 / 39 = 1.44 |

One photon: P(both) = 0 exactly and alpha = 0, the blind's (PASS, by the count: the credit's one
draw over the two records' outcomes and the light's count at 0 after the first taking, so that the
second record's outcome into it has no share); P(A only) = 0.505 and P(B only) = 0.495, equal within
the standard error (PASS on the symmetry); the share s reads 1 / 2 each with no "neither", above
the blind's "s at most 1 / 2" bound's meaning: both records' shares were near 1 at the window's end
(FINDING, below), so the one draw split the quantum between them. Two photons: P(both) = 0.14
above 0 (PASS), one taking per record at most in a window, alpha = 1.44, neither S.57 (c)'s 1 / 2
nor the sequential 1 (the two records' shares at the window's end differ, 0.26 and 0.375, and the
draw's "neither" outcome, 0.505, carries the rest of the unit, a form S.57 does not have).

**The finding, by name: the light's one-Node lays and holes pump the massless row's marginal uniform
mode, so the records read a standing level and not a passing packet.** The two packets are laid by
the mode file with their Rule3 remainders at 0, and the row's remainders rising to their mean give
the uniform mode (a double root of Rule3 at wave number 0, a level of zero share) a velocity, so the
photon's level at both records drifts to about -145 by the interval 8 and stays there while the
packets have passed (a GameBoard reading of one trial: the level at A and at B -98 and -157 at 8,
-146 and -149 at 28, -141 and -141 at 32); the records' turn therefore keeps accumulating, about
0.15 per interval at the weight 6, and the two-mode line's share at the window's end is the Rabi
oscillation's phase at that interval (in the one-photon world near 1 for both, in the two-photon
world 0.26 and 0.375), not the transfer over a passage; the same mechanism that ends the
telegraph's run (examples/events/shelved_ion/blind_and_reading.md). The structure the blind tests,
one quantum one click, holds whatever the shares: P(both) = 0 is the count's, read in 200 trials.

**With the erasing front in the tree** (`front.py`, the round's last act): the same 200 trials per
world read the same table, number for number (one photon: 101, 99, 0, 0, alpha 0; two photons: 24,
47, 28, 101, alpha 56 / 39). In the one-photon world the light's count reaches 0 at the one taking
and its front begins from the taker's Node, one shell per interval along the chain, its erasure lines
in the output; the window has closed by then and the second record's outcome has no share whatever
the levels show, so the clicks do not move; in the two-photon world the count reaches 0 at the
second taking, at the window's end, with the same effect.

**Through the one click act with the face** (the tree at 84f0352d and after, 200 trials per world): the
same table number for number (one photon: 101, 99, 0, 0, alpha 0, PASS; two photons: 24, 47, 28,
101, alpha 56 / 39), the photon's quantum taken by the face at the taker's Node over two intervals and
the record's parts laid; the front's faces on the chain after the count reaches 0.

## What is open, by name (2026-10-04)

The front's taper (the shell at a distance within the last L written at a fraction of Rule3's own
level, 0 behind, so that the hole's and the front's transients, 5 and 12 percent of a quantum for
about eight intervals, leave the picture; a law line at the owner's word, the hands' counsel #1827
comments 5975438107 and 5975470305); the giving's packet and the source in time without a uniform
mode (the mathematician's first and the advisor's second, the second pull request); the erasure
line's `taken` printed as the faces' booked take in quanta in place of the levels' sizes. The one
draw's generator is the first closing record's (the world has no draw of its own); the record's own
NodeReader region and the face form of the hole are built.

## On the own quantum, 2026-10-03 (branch own-quantum, 8382b8b9)

The round of the NodeReader's own quantum (the mathematician's 213, 214, 220, 221 and 223 and the
advisor's seconds, the ids in `examples/events/resonance/blind_and_reading.md`) declares the atoms'
transition at the resonance [5414, 6000] (the photon's rotation at k = pi / 4, cos omega =
(cos(pi / 4) + 2) / 3) and lays no light here (the atoms have no rates); the two worlds declare no
region NodeReader. Re-run by `tools/meeting_trials.py` on 8382b8b9 over the 200 seeds: one photon A only
101, B only 99, both 0, neither 0, alpha 0; two photons 24, 47, 28, 101, alpha 56 / 39; bit for bit the
readings above. PASS and unchanged.

## The readings' sources (the owner's word of 2026-10-03, 10:08 Israel)

The table's numbers (A only, B only, both, neither, alpha) are the NodeReader's: the `jump` lines'
`taken` per trial, read by `tools/meeting_trials.py`. The finding's levels at the two records' Nodes
(-98 and -157 at 8, -146 and -149 at 28, -141 and -141 at 32) are a GameBoard reading of one trial,
labelled so, and no number of the blind. The lines carry the board's `tick` and the `window` in board
intervals and nothing of the records' own clocks.

## On the resonant act, 2026-10-03 (branch resonant-act, on main's dark grain)

The resonant two-mode act (the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and
5966081562; the advisor's seconds, 5965918924 and 5966129376 with #1563 comment 5966129628; the hands'
precisions of the morning, #1572 comments 5966338551 and 5966387795; the form in
`examples/events/resonance/blind_and_reading.md`, the window's turn applied as W sub-turns with the
carry) changes the records' turn here: the window's turn is k isqrt(X^2 + Y'^2) div R with X and Y' the
arriving level summed over the window against the records' reference records at [5414, 6000], so a
standing level (the uniform mode's drift of about -145 named above) sums to a bounded residue and the
records read the passing packet alone, the transfer over a passage the design intended. Re-run by
`tools/meeting_trials.py` over the 200 seeds on the tree holding main's dark grain (no giving here, so
the grain changes nothing), the blind untouched, every number changed by name:

| world | A only | B only | both | neither | alpha |
| --- | --- | --- | --- | --- | --- |
| one_photon | 99 of 200 | 97 of 200 | 0 of 200 | 4 of 200 | 0 |
| two_photons | 21 of 200 | 17 of 200 | 162 of 200 | 0 of 200 | 10800 / 10919 = 0.99 |

One photon: P(both) = 0 exactly and alpha = 0, the blind's (PASS, by the count as before); P(A only) =
0.495 and P(B only) = 0.485, equal within the standard error (PASS on the symmetry), each at most 1 / 2
with a "neither" of 0.02 (PASS on the bound's meaning: the records' shares at the window's end read
about 0.49 each from the packet's passage, and the draw's complement carries the rest). Two photons:
P(both) = 0.81 above 0 (PASS); alpha = 0.99, the value of two independent sequential takings at one
share (the records' shares at the window's end about 0.9 each under the control's larger amplitude)
and not S.57 (c)'s 1 / 2 (a FINDING by name, as before in kind: the one draw with the complement
outcome is not S.57 (c)'s form). The finding named above, the standing level read as a turn, is lifted
by the resonant form. The first build of the act (one shear of the window's sum) read 92, 89, 0 and
19 with alpha 0 and 19, 19, 162 and 0 with alpha 0.99; its numbers are replaced by this table's.

## On the lay without the uniform mode and the redesign, 2026-10-04 (branch click-share-fix)

The experimenter's bug report (#1827 comment 5975131359; the hands' lines 5975317261, 5975334043 and
5975371441; the Boss's 5975430859 and 5975547149): the message lay wrote the packets with a uniform-mode
content, the sum of now -563 and of before -406 over the chain of 24, and Rule3 carries their difference
exactly on the massless row (the double root at wave number 0), so the mean level fell by 157 every
interval, the records read that standing level in place of the passing packet (the finding named
above), and the click act's hole, written to 0 into it, left two kinks worth a quantum of share that the
front carried outward (the photon's share 1 quantum to 2 after the one taking, 2 to 5 in the control).
The fix: the generator takes the uniform mode's content out of a massless packet's two levels (each sums
to 0 over the board, the sum divided among the packet's Nodes in proportion to the envelope by the
division act) and the loader refuses a massless message whose sums are not 0; nothing of Rule3, the
hole, the front or the books moves (ALGEBRA.md, The message lay, the sentence of 2026-10-04). The old
lay at top 1 and edge 3 on the chain of 24 was mostly uniform mode: what the correction leaves is a
three-Node wiggle of no wave number near pi / 4, off the atoms' resonance, whose reading contradicts
this folder's blind (the advisor's finding, 5975512075: at the amplitudes that keep the count, 36 of 50
seeds close with no taking), so it is replaced and not kept. The redesign (the advisor's and the
mathematician's approval, 5975470305 and 5975568700): the chain 96 open on x with both faces receding,
the atoms at the Nodes 23 to 24 and 71 to 72 (24 Links from the centre each, the lay symmetric), the
packets toward +x from 48 and toward -x from 47 at k = pi / 4 with top one Node and edge 8 (one
wavelength, the envelope's transform 0 at the carrier, so the correction is a no-op), the amplitudes by
the design's own rule so that the books read one whole quantum (116: 585,066,000, 0.99 W_rec) and two
(165: 1,188,630,000, 2.02), the window 48 at the passage's end (the packets reach the atoms' rings by
about 27, their tops at 42), the run 170 so that the front reaches both packets; the blind rebuilt by
the builder from the design with one line added at the hands' word, P(A only) = P(B only) exact by the
lay's symmetry and the seeds' draw alone, its exact claims unchanged. Re-run by `tools/meeting_trials.py`
over the 200 seeds and by `tools/run_inputs.py` on the shipped world, every number labelled:

| world | A only | B only | both | neither | alpha |
| --- | --- | --- | --- | --- | --- |
| one_photon | 99 of 200 | 101 of 200 | 0 of 200 | 0 of 200 | 0 |
| two_photons | 5 of 200 | 0 of 200 | 195 of 200 | 0 of 200 | 1 |

One photon: P(both) = 0 exactly and alpha = 0, the blind's (PASS, by the count); P(A only) = 0.495 and
P(B only) = 0.505, equal within the standard error and the symmetry's (PASS), each at most 1 / 2 with no
"neither" (PASS on the bound: the draw's shares at the window's end A 0.487, B 0.513, none 0.000,
NODEREADER, the passage's transfer complete at the weight 6). Two photons: P(both) = 0.975 above 0
(PASS); alpha = 1, the blind's second form (two sequential takings at one share). The shipped run
(GAMEBOARD, the books per interval; the page from the output file): the share 1.00 quanta at the lay and
1.01 at 48; body 0 takes at 48 (NODEREADER, the count 1 to 0, the hole at its Node); 1.05 at 49 (the
hole's transient) and 1.12 at 56 (the front's sweep through the near packet, the most, the known
transient of the hole to 0 inside a smooth wave), 0.59 at 60 and 0.49 from 80 to 150 (the near packet
erased, the far one the empty wave in the grown layers), 0.10 at 170 as the front sweeps the far packet
(it meets its top at about 159), 0.02 at 180 and 0 exactly from 190, the board dark; the erasure one
shell per interval on both sides until the left shell leaves the declared board; `tools/back_in_time.py
--intervals 170` MATCH; the control both atoms at 48. The two transients are the hands' known one, named
by their numbers until the front's taper at the owner's word.

## The gate's table

Every row is a reading of the experimenter's run on the current tree (main d00aa9e, 2026-10-04), re-run and
compared bit for bit by `tools/reading_gate.py`: the label the reading's own (NODEREADER for the credit
lines' clicks and the trials' coincidences, GAMEBOARD for the verdict, the ticks, the line counts, the
end's books and the back-in-time pass), the world the folder's file, `by` the tool that re-runs it, the
reading in the gate's words and the value as its report prints it.

| label | world | by | reading | value |
| --- | --- | --- | --- | --- |
| GAMEBOARD | one_photon.json | run_inputs | verdict | LAWFUL |
| GAMEBOARD | one_photon.json | run_inputs | ticks | 170 |
| NODEREADER | one_photon.json | run_inputs | clicks | 1 |
| NODEREADER | one_photon.json | run_inputs | clicks body 0 | 1 |
| NODEREADER | one_photon.json | run_inputs | clicks body 1 | 0 |
| NODEREADER | one_photon.json | run_inputs | takings body 0 | 1 |
| NODEREADER | one_photon.json | run_inputs | takings body 1 | 0 |
| GAMEBOARD | one_photon.json | run_inputs | lines lay | 8 |
| GAMEBOARD | one_photon.json | run_inputs | lines face | 323 |
| GAMEBOARD | one_photon.json | run_inputs | lines erasure | 122 |
| GAMEBOARD | one_photon.json | run_inputs | lines credit | 1 |
| GAMEBOARD | one_photon.json | run_inputs | books photon quanta | 0 |
| GAMEBOARD | one_photon.json | run_inputs | books photon share | 61284000 |
| GAMEBOARD | one_photon.json | run_inputs | books atom quanta | 2 |
| GAMEBOARD | one_photon.json | meeting_trials | trials | 200 |
| GAMEBOARD | one_photon.json | meeting_trials | refused | 0 |
| NODEREADER | one_photon.json | meeting_trials | A only | 99 |
| NODEREADER | one_photon.json | meeting_trials | B only | 101 |
| NODEREADER | one_photon.json | meeting_trials | both | 0 |
| NODEREADER | one_photon.json | meeting_trials | neither | 0 |
| NODEREADER | one_photon.json | meeting_trials | alpha | 0 |
| NODEREADER | one_photon.json | meeting_trials | ends in e body 0 | 99 |
| NODEREADER | one_photon.json | meeting_trials | ends in g body 0 | 101 |
| NODEREADER | one_photon.json | meeting_trials | ends in e body 1 | 101 |
| NODEREADER | one_photon.json | meeting_trials | ends in g body 1 | 99 |
| NODEREADER | one_photon.json | meeting_trials | clicks body 0 e by photon | 99 |
| NODEREADER | one_photon.json | meeting_trials | clicks body 1 e by photon | 101 |
| GAMEBOARD | two_photons.json | run_inputs | verdict | LAWFUL |
| GAMEBOARD | two_photons.json | run_inputs | ticks | 170 |
| NODEREADER | two_photons.json | run_inputs | clicks | 2 |
| NODEREADER | two_photons.json | run_inputs | clicks body 0 | 1 |
| NODEREADER | two_photons.json | run_inputs | clicks body 1 | 1 |
| NODEREADER | two_photons.json | run_inputs | takings body 0 | 1 |
| NODEREADER | two_photons.json | run_inputs | takings body 1 | 1 |
| GAMEBOARD | two_photons.json | run_inputs | lines lay | 16 |
| GAMEBOARD | two_photons.json | run_inputs | lines face | 325 |
| GAMEBOARD | two_photons.json | run_inputs | lines erasure | 122 |
| GAMEBOARD | two_photons.json | run_inputs | lines credit | 2 |
| GAMEBOARD | two_photons.json | run_inputs | books photon quanta | 0 |
| GAMEBOARD | two_photons.json | run_inputs | books photon share | 36954000 |
| GAMEBOARD | two_photons.json | run_inputs | books atom quanta | 2 |
| GAMEBOARD | two_photons.json | meeting_trials | trials | 200 |
| GAMEBOARD | two_photons.json | meeting_trials | refused | 0 |
| NODEREADER | two_photons.json | meeting_trials | A only | 5 |
| NODEREADER | two_photons.json | meeting_trials | B only | 0 |
| NODEREADER | two_photons.json | meeting_trials | both | 195 |
| NODEREADER | two_photons.json | meeting_trials | neither | 0 |
| NODEREADER | two_photons.json | meeting_trials | alpha | 1 |
| NODEREADER | two_photons.json | meeting_trials | ends in e body 0 | 200 |
| NODEREADER | two_photons.json | meeting_trials | ends in g body 0 | 0 |
| NODEREADER | two_photons.json | meeting_trials | ends in e body 1 | 195 |
| NODEREADER | two_photons.json | meeting_trials | ends in g body 1 | 5 |
| NODEREADER | two_photons.json | meeting_trials | clicks body 0 e by photon | 200 |
| NODEREADER | two_photons.json | meeting_trials | clicks body 1 e by photon | 195 |
| GAMEBOARD | one_photon.json | back_in_time | intervals 170 | MATCH |
| GAMEBOARD | one_photon.json | back_in_time | intervals 72 | MATCH |
| GAMEBOARD | two_photons.json | back_in_time | intervals 170 | MATCH |
