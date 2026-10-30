# ANIMATE-LINKS: Meshes that lengthen, read by clicks alone

The owner's word to Animate (2026-10-30, 04:2x UTC, in Hebrew; in translation, his first person plural rendered
without a person): "Make sure that in the plan the coordinates fit, and that the links lengthen at the Node-clocks,
right? So it is not always a fixed space in time, in the spacetime. Check that everything converges in sound
mathematics: conversions from space to space, and in the imagined space of events in time, with the two directions
of time, the links lengthen, right? Just check that everything converges."

Run: `python -I tools/derivations/open_items/ANIMATE-LINKS/links.py` (well under a second; the output is links.txt).
Whole numbers only: no root, no float, no table.

## What it is

A stand-in for G2's moving Meshes, which the engine holds at rest until G2. A line of 40 Node-clocks keeps its labels
for ever; what lengthens is the Mesh, as the rounds light needs to cross it. Light gains one unit a round and crosses
a Mesh when its gain reaches the Mesh's length then, the rest kept by the carry, so it never crosses more than one
Mesh a round. Every clock stands at its Node-clock and ticks once a round, so what changes is the Mesh and not the
clock. Four laws of lengthening: still, growing (a unit every 50 rounds), doubling (every 400 rounds) and a swing (up
to a top at round 1,500, then down).

## What it shows (links.txt)

1. **A difference of sites is no length:** the echo between Node-clocks 0 and 5, in Node-clock 0's own count, is 40
   at every lay when nothing lengthens; 40, 152, 263, 375 and 485 when the Meshes grow; 40, 80, 160, 608 and then
   none when they double. The label distance is 5 every time.
2. **The horizon closes in:** under doubling, a quantum laid at round 1,600 is taken at Node-clock 0 from Node-clocks
   up to 11 only; laid at round 2,400, up to 2; laid at round 3,200, from none.
3. **The redshift:** quanta laid every 10 rounds from Node-clock 20 arrive 10 apart when nothing lengthens, and more
   than 10 apart, all 99 of them, when the Meshes grow.
4. **After the top, the clicks still see the expansion:** the gaps from Node-clock 2 drop below 10 at round 1,555
   with no red gap after the top; from Node-clock 10 at round 1,668, after 9 red gaps; from Node-clock 30 at round
   1,908, after 24 red gaps. The nearest turns blue first, as docs/BIG_PICTURE.md section 7 says.
5. **The cone:** never more than one Mesh a round, under every law.

## What does not follow

- The engine's own light and Meshes: they move from G2 on (the Boss's travelling-wave file comes with G2's first
  test), and the readings are owed on its records.
- A clock's rate changing with the load: here every clock ticks once a round; on the engine the tick's weight is a
  slot too, and a clock's own count already reads it.
