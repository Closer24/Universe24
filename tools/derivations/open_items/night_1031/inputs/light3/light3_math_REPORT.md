<!-- Boss note, 2026-10-31 ~09:4x UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of LIGHT3 (frozen e111cfcd), the hostile mathematician (LIGHT2's mathematician). -->

# The hostile mathematician on LIGHT3, 2026-10-31, 09:01 to 09:30 UTC

The whole report is below; it is meant for S/light3_math/REPORT.md (S = S).

**What I read:**
- LIGHT3.md (367 lines; its sha256 matches e111cfcd...);
- every probe and queue in the frozen folder;
- my LIGHT2 report as written;
- the brief's rulings: 07:5x (second part), 08:4x and 08:5x.

**How I ran:**
- My copy of the frozen folder is S/light3_math/copy/. All 1,324 of 1,324 sums in FROZEN.sha256 match, and every file is listed there.
- Python 3.14.6 with -I, under nice -n 19, one process at a time, each after the load wait. Whole numbers only.
- My own files, all under S/light3_math/:
  - m_turned.py;
  - worlds/mesh250 and worlds/mesh250h: the shipped mesh world, and the same with the held hand at site 40, each with ticks 250 (a test's cut), laid by the text's own lay tool;
  - runs/mesh250.jsonl and runs/mesh250h.jsonl, written by the runner's own tool from copy/all;
  - every output, in out/.

VERDICT on LIGHT3: NOT PASSED

LIGHT3 meets every item of my LIGHT2 report in form. It is honest that the echo's yes is OPEN. One item blocks: the rule's no, which the build recommendation leans on, belongs to the shipped 125-round window, not to the file's key.

## BLOCKING

**B1. The echo rule's NOT SHOWN "at the file's key" is the 125-round window's. On a longer cut of the same world, at the same key, it reads SHOWN with no reflector.** (Text 0.4, 0.5, section 4, 5.3, 7, 8, and question 1.)
- MEASURED, with the text's own probe (p_light3.py) on the shipped mesh world at the file's key, run to 250 rounds (a test's cut, laid by lay_light3.py `ticks=250`):
  - With no reflector laid, it reads SHOWN: 14 echoes, 10 pairs, B among (1, 2), (6, 2), (14, 2), (26, 2), (34, 2), (39, 2) ... There are 16,620 windows, all of them after round 125. The first echo: A (1, 2) gives at 172; B (177, 2) takes from site 178 at 176 and gives back there at 177; A takes at 182.
  - With the held hand laid 2 at site 40 (mesh250h), it reads SHOWN: 7 echoes, 5 pairs, and none of them has B at site 40.
- The board check beside it, two records compared (never the reading):
  - The lay's turned part does reach light's lines on the lay's side, from round 143: the first medium lines that differ are at sites 39 and 41 together.
  - By round 250, 2,319 medium lines differ below B and 2,527 above it.
  - p_diff3b counts 10,131 lines whose across field differs.
  - Within 250 rounds the second front cannot reach site 40 (it gets there at about round 320). So the part on the lay's side can only come from B.
- So, at the file's key as well as the test key:
  - the rule's SHOWN is the uniform relay's;
  - the rule never reads the laid B, even once B's turn is in the light lines;
  - its NOT SHOWN on the shipped records says only that A's quiet does not yet hold within 125 rounds.
- Two statements fall:
  - 0.4's "the test key's SHOWN readings are the uniform relay's" understates it: the same is true at the file's key.
  - Section 7's picture of the file's key as a readout with no quiet does not survive 250 rounds: 16,620 windows, and 68 echoes without the turn.
- Fix:
  - Name the no as "NOT SHOWN within the shipped 125 rounds".
  - Add the 250-round readings.
  - If the rule is built, its yes must print as "turns read: OPEN, no echo reading", never as SHOWN. Otherwise the decoder prints SHOWN on longer records of a shipped world where no echo exists.

## MINOR

1. **"The lay is the reflector" (5.4, 0.5).** On the text's own evidence the turn was not separated:
   - on ring60h the second front mixes the turned part with the passed part, and the text's own caveat says so;
   - on the shipped ring within 125 rounds, no light line differs.
   - My 250-round board check now separates it: the medium is turned back from round 143, as B1 gives.
   - Fix: cite that check, name it a board check, and say the turn begins after the shipped run.
2. **0.6, "A's count is 0 in every echo found anywhere".** The built L1 reads A's count 2 (3.4). Say "on every world's record".
3. **The three queues hard-code the writer's folder.** drive.sh, probe.sh and probe2.sh name scratchpad/light3, so run from the frozen folder they read and write outside it. The probes themselves take their paths from their own folder.
4. **The turn reduces to one edge changing direction** (3.5; the text's question 2). In these worlds, B's light partner at site P is one medium clock. So the turn is one edge's quanta changing direction, and any edge whose passing changes sign twice turns: 110 of 122 matter clocks do (DERIVED from 2.3, MEASURED). A laid B can differ only in how many quanta turn and when. Any condition that separates it must read the sizes of q, against a cut that comes from the structure; any other cut is a pick.
5. **Per train against per clock, at the test key** (1.4; question 4). At the file's key the split vanishes: on 250 rounds train 2 is matter at 178 of 178 clocks. The false echoes of B1 remain there, so the per-train choice does not cause them.
6. **The cone's 120 against the ruling's 114** (2.4). 120 includes the 6 starting clocks; 114 / 62 / 187 counts the later clocks only. Say which. This rests on the 08:5x ruling, made after the freeze.
7. **The guard's reach** (header, 3.3, 9). The 08:5x ruling says texts must name that "admitted" means the mates close, not that the record is faithful to the act. Say so where the text cites the guard. This also rests on a ruling made after the freeze.

## My LIGHT2 items

- **B1 (a turn at B): met as fixed.**
  - The turn is built (3.1). H1, H1b and R4 read NOT SHOWN; H2 reads B = (4, 2) alone with the hold (4, 5); the cases order alone cannot tell are named.
  - The substance, a yes that means an echo, is OPEN in the text's own words, and is now shown false at the file's key too (B1).
- **B2 (chains through meetings): met.**
  - Three components, of 187, 91 and 91 clocks. This is my measurement, now reproduced by a third code.
  - 0 of 122 sites have all their clocks in one component.
  - The cone per clock reads 120 / 62 / 187, and the 187 are one whole component.
  - H3 reads no echo through the hop.
- **B3 (lay a reflector and run it): met.** It was laid and run at both keys; its conclusion is now supported by my board check (MINOR 1).
- **The minors:**
  - M1 (the medium as a named set, on prefixes): met. The record cut at round 20 reads {0, 2}, and from round 21 {0}.
  - M2 (lawful built records): met. The mirror lines are written, the guard passes, and no event repeats.
  - M3 (file names): met, case01 to case13.
  - M4 (probes inside their folder): met for the probes; the queues still are not (MINOR 3).
  - M5 (the least quiet for every record): met. t >= g + 3 holds for every record, and I checked its proof.
  - M6 (whose quiet): met. A's quiet is A's own; the site quiet is named a board check.
  - M7 (the earliest take): met. It is replaced by the last take.
  - M8 (click200 frozen): met.
- **My four questions:** all ruled at 07:5x and built.

## SOUND

- All 17 outputs, rerun from my copy, are byte for byte the frozen: the tests, the 8 records, both diffs, diff3b and the 4 turn counts.
- Rule L on the shipped mesh world:
  - the medium is {0}, with 125 medium clocks and 122 + 122 matter clocks;
  - 18,096 meetings, 4,442 of them own and 13,654 across a Mesh;
  - the click world's no stands: 27 components of 3 clocks.
- 3.1 as coded matches its words:
  - t is A's next light meeting, and it must be a take;
  - the turn reads B's last take round, and every take in it comes from site P;
  - chains run through meetings, both ends, at strictly later rounds.
- The least quiet is DERIVED for every record.
- The turn removes the laps and the pass-throughs.
- 5.2's numbers hold: 110 lines differ, all at site 40 (shipped ring, 125 rounds); on ring60h, 1,095 lines at 24 sites.
- The face is out: A's count and B's hold are read from their own meetings.
- No key is picked, no site index is read as a coordinate, and the yes is named OPEN.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, and sound:**
  - rule L, its set and its prefixes;
  - the least quiet;
  - the turn against a front that never turns;
  - why the medium never meets its site's matter;
  - measure.past as a board check.
- **MEASURED, the text's, reproduced:** sections 1.3 to 1.5, 2.2, 2.4, 2.5, 3.3 to 3.5, 4, 5.2, 5.3 and 6.2.
- **MEASURED, mine:**
  - at the file's key, on 250 rounds: 14 echoes with no reflector, and 7 with B laid at site 40, none of them off B;
  - the board's turn from round 143, as B1 gives.
- **OVERCLAIMED:**
  - "at the file's key it reads NOT SHOWN on every shipped world", read as the rule's no;
  - "the lay is the reflector", on the text's own evidence;
  - "A's count 0 ... anywhere".

## Questions for the Boss

1. Shall the echo rule be built only as NOT SHOWN, or as "turns read: OPEN", never printing SHOWN?
2. The text's question 2: is a one-record comparison of B's turned quanta (the sizes of q) lawful when its cut comes from the structure, and a pick otherwise?
3. A's quiet occurs at the file's key after about round 170. Does LIGHT2's batch item "A's quiet" then leave the owner's batch?

## Solution24

Rule L and the per-clock cone can be built now. The echo rule reads a turn, not an echo: its NOT SHOWN is the shipped window's, and its SHOWN comes from the uniform relay at both keys. The held hand at one site does turn the medium on the board from round 143. The click world still needs a reading that tells that turn from the relay.
