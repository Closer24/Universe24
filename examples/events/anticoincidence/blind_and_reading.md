# One photon on two bodies, the anticoincidence: the blind and the reading

The paper's S.57 (the mathematician's 144 and 145, two hands by the law as it stands; the owner's
word of 2026-10-03, 03:25): a chain of 24 Nodes open on x with both faces receding, y and z folded;
two records of two parts (g, e) of the pair [1, 1299] declared NodeReaders at one Node each, the
Nodes 6 and 17, equidistant from the centre, their six Link factors 0 so that they stay; one light
record of the family `photon` (light's pair, one real line) laid at the centre as two packets toward
both at k = pi / 4, its laid share one whole quantum (the books' count 1 read from the loaded
world), the control's two; each record reads the light into e at the transition's weight 6 over one
window, the run of 40 intervals, and the credit draws once over both records' outcomes into the
light (the taking the exchange at the record's Node). The blind is `expectation.json`, written by
`build_world.py` before any run and never edited after; the reading is appended here after the
night's run, every number a click (the `jump` lines over the trials, `tools/meeting_trials.py`); a
reading that misses the blind is a finding, written as such and never adjusted.

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

## What is not built, by name

The record's own NodeReader region around its Node (the mathematician's 180); the one draw's
generator the first closing record's (the world has no draw of its own); the face form of the
hole (the mathematician's 193, 195 and 197, the advisor's second in #1572 comment 5963391333), the
morning's unless the gate worlds read MATCH across the click with it tonight.

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

## On the lay without the uniform mode, 2026-10-04 (branch click-share-fix, 84f151f)

The experimenter's bug report (#1827 comment 5975131359; the hands' lines 5975317261, 5975334043 and
5975371441; the Boss's 5975430859): the message lay wrote the packets with a uniform-mode content, the
sum of now -563 and of before -406 over the chain, and Rule3 carries their difference exactly on the
massless row (the double root at wave number 0), so the mean level fell by 157 every interval, the
records read that standing level in place of the passing packet (the finding named above), and the
click act's hole, written to 0 into it, left two kinks worth a quantum of share that the front carried
outward (the photon's share 1 quantum to 2 after the one taking, 2 to 5 in the control). The fix: the
generator takes the uniform mode's content out of a massless packet's two levels (each sums to 0 over
the board, the sum divided among the packet's Nodes in proportion to the envelope by the division act)
and the loader refuses a massless message whose sums are not 0; nothing of Rule3, the hole, the front or
the books moves. This folder's design changes by its own rule and no more: the amplitudes 160 and 226
become 238 and 333 so that the books read one and two quanta (the lump at top 1 and edge 3 was more than
half uniform mode), and the declared seed 25 becomes 5 so that the shipped run takes (body 0 at 40) and
the reader test's window of 10 takes at 10; the blind is untouched. Re-run by `tools/meeting_trials.py`
over the 200 seeds and by `tools/run_inputs.py` on the shipped world, every number labelled:

| world | A only | B only | both | neither | alpha |
| --- | --- | --- | --- | --- | --- |
| one_photon | 7 of 200 | 47 of 200 | 0 of 200 | 146 of 200 | 0 |
| two_photons | 8 of 200 | 80 of 200 | 11 of 200 | 101 of 200 | 2200 / 1729 = 1.27 |

One photon: P(both) = 0 exactly and alpha = 0, the blind's (PASS, by the count); P(A only) = 0.035 and
P(B only) = 0.235, each at most 1 / 2 (PASS on the bound) and in the shares' proportion of this lay
(the draw's shares at the window's end A 0.034, B 0.253, none 0.714, NODEREADER), not equal: the two
packets after the correction differ (the hands' line on the blind's "equal", 5975092300 and 5975225429,
reads it as the shares' proportion), and most windows close with no taking, since the lump's passage at
the weight 6 transfers a few percent where the standing level had transferred nearly all. Two photons:
P(both) = 0.055 above 0 (PASS); alpha = 1.27, neither form of the blind exactly (the second draw over
the atom left and the rest of its unit). The shipped run (GAMEBOARD, the books per interval): the share
1.02 quanta at the lay and 1.05 through the window, 1.05 at the hole's two faces (the hole at a Node the
packets left 26 intervals before removes about nothing and adds nothing: every Node outside the hole's
first shell bit for bit a no-taking run's, the dedicated test), then falling as the light leaves through
the receding faces, 0.66 at 72; the 32 erasure lines take 5 to 136 units per shell, the residual wave;
`tools/back_in_time.py --intervals 72` MATCH. What the folder still owes, the hands' design item: a
packet long against its wavelength on a longer chain with the window closing at the passage's end (the
chain 96, the packets at 47 and 48 with top 1 and edge 8, the atoms at 23 to 24 and 71 to 72, the window
48, the run 170), read on the experimenter's scratch branch at 50 seeds as A only 25, B only 25, both 0,
neither 0 and the control both 50 of 50, the front sweeping the near packet within 15 intervals and the
far one from about 120, the board dark at 170; its pull request follows this one.
