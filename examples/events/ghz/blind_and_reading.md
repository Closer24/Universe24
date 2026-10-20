# The GHZ gate: the blind and the reading

The four worlds of the gate (ALGEBRA.md, The click is the meeting; `design.json`, `build_world.py`,
the blind `expectation.json` M = -4 written before any run, `tools/bell_gate.py` the reader over the
four output files with the gate's expectation). A reading that misses the blind is a finding,
written as such.

## The reading (branch click-share-fix, fb2c14c, 2026-10-04, the lay without the uniform mode)

The packet lay's uniform mode taken out at the lay (ALGEBRA.md, The packet lay, the sentence of
2026-10-04; the experimenter's bug report, #1827 comment 5975131359): each packet's two levels sum to
0 over the board (the sums were 13,502 and 12,182 before), the lay's count 1,702 per packet against
1,787 at the design's amplitude kept. The four worlds re-run (`tools/run_inputs.py`,
`tools/bell_gate.py`), NODEDETECTOR:

| setting | E |
| --- | --- |
| x y y | -1 |
| y x y | -1 |
| y y x | -1 |
| x x x | 1 |
| M | -4 |

M by the parts' shares -1, by the local sums -1, by the sign -1: every number bit for bit the
blind's and the reading before the fix.

## The three readers' reports and the lay's backward component, 2026-10-04 (main d00aa9e)

The pages on main (the experimenter's #1827 comment 5975980838, item 2) name one number beside the
gate's: the top reader's window inflow is 803.239 quanta against the left's 923.186 and the right's
922.756, the same in all four worlds, where the design lays the three beams alike (two along x from
the column 16, one along y from the row 16, the top 7 Nodes across, the edges 6 along and 4 across,
the readers 28 Nodes each). Read with each beam laid alone (copies of `ghz_x_y_y.json` with one, two
or three of its packets, laid by `tools/pixel_mode.py --input` and run over the 60 intervals; the
window inflows NODEDETECTOR, the lay's count LATTICE; #1827 comment 5975991093):

| the lay | left | right | top | the lay's count |
| --- | --- | --- | --- | --- |
| the beam toward -x alone | 800.701 | 32.703 | 0.514 | 1,703 |
| the beam toward +x alone | 32.692 | 800.269 | 0.519 | 1,703 |
| the beam toward +y alone | 0.514 | 0.511 | 800.582 | 1,704 |
| the two x beams | 919.917 | 920.322 | 0.955 | 3,574 |
| all three, the shipped world | 923.186 | 922.756 | 803.239 | 5,257 |

Each beam alone delivers 800 quanta to its reader, x and y alike within 0.4, so the lattice is
isotropic to the reading and the y lay is the x lay's; a beam carries a backward component, 32.7
quanta of 800 arriving at the opposite reader (4.1 percent); the two x beams are laid at the same
Nodes, so each beam's backward component rides with the other's forward wave and adds coherently:
the sides read 920 each in place of 800 + 32.7, and the pair's lay counts 3,574 in place of 2 x
1,703 (the cross term 168 quanta at the lay, the two readers' excess 2 x 87); the y beam has no
partner laid on it and reads 800. The gate's numbers are untouched (M and every marginal are
normalised per world), and nothing of the engine moved: the number is the design's lay of two
counter-propagating packets on one place.

The backward component is the lay's own, derived by the advisor (#1827 comment 5976031061, the first
hand; the mathematician's second asked): a packet laid as now_i = b e_i cos(k x_i) and before_i =
b e_i cos(k x_i + omega_0) with the one phase omega_0 under the same envelope is not a forward wave
of every component, a component at the wave number k + delta advancing by omega(k + delta) and not
omega_0, so the backward share is v_g^2 <delta^2> / (4 sin^2 omega) with <delta^2> the envelope's own
bandwidth: at k = pi / 4 on light's row (omega_0 = 0.4456, sin omega_0 = 0.431, v_g = 0.547) 3.4
percent by the exact decomposition over the band at the top 1 and the edge 6 (3.6 by the first-order
formula) against the 4.1 read, the integers' rounding and the cross-section's spread the rest; 2.0
percent at the edge 8, 1.2 at the top 7, 0.5 at the edge 16; the two slits' `elsewhere` holds the same
number. The edge rule of the division act zeros the uniform component and not the dispersion across
the band; the law's own words, the record one interval earlier, with the envelope moved back by v_g
in the before level, bring the backward share to 6 x 10^-5 at the same envelope: the change's line
when the owner reopens the engine, nothing of the engine or the worlds tonight. The design's other
road, the x beams laid apart by the packet's 13 Nodes, is a world file's change and also waits.

## The reading at the clean engine (main 1fe3790a, 2026-10-05; the engine of main 39cc3851)

The control run (the advisor's division, #1827 comments 5986693793 at 39cc3851 and 5987050362 at
1fe3790a; the folder's own tools, `tools/run_inputs.py` and `tools/bell_gate.py`, the same command at
both hashes; 60 intervals per world), NODEDETECTOR: E_3 = -1, -1, -1, +1 for x y y, y x y, y y x and
x x x, M = -4, the blind's; every marginal 1 / 2 and every pairwise correlation 0 at both hashes.
`tools/back_in_time.py` on ghz_x_y_y.json MATCH over 40 (LATTICE). The packet lay at the declared
vacuum content 60 (the tool row F8 of 1fe3790a) moves the lines' counts (the gate's table below: 170
`click` and 160 `parts` lines per world against 156 and 156 at the lay of 2026-10-04) and no number
of the gate.

## The gate's table

Every row is a reading of the control run at the clean engine (the engine of main 39cc3851; the lays and the
tools of main 1fe3790a, 2026-10-05; the clicks the control's, the line counts and the books the gate's own
re-run on the committed files), re-run and compared bit for bit by `tools/reading_gate.py`: the label the reading's own (NODEDETECTOR for the credit
lines' clicks and the trials' coincidences, LATTICE for the verdict, the intervals, the line counts, the
end's books and the back-in-time pass), the world the folder's file, `by` the tool that re-runs it, the
reading in the gate's words and the value as its report prints it.

| label | world | by | reading | value |
| --- | --- | --- | --- | --- |
| LATTICE | ghz_x_y_y.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_x_y_y.json | run_inputs | intervals | 60 |
| NODEDETECTOR | ghz_x_y_y.json | run_inputs | clicks | 3 |
| NODEDETECTOR | ghz_x_y_y.json | run_inputs | clicks left | 1 |
| NODEDETECTOR | ghz_x_y_y.json | run_inputs | clicks right | 1 |
| NODEDETECTOR | ghz_x_y_y.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines click | 170 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines parts | 160 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_y_x_y.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_y_x_y.json | run_inputs | intervals | 60 |
| NODEDETECTOR | ghz_y_x_y.json | run_inputs | clicks | 3 |
| NODEDETECTOR | ghz_y_x_y.json | run_inputs | clicks left | 1 |
| NODEDETECTOR | ghz_y_x_y.json | run_inputs | clicks right | 1 |
| NODEDETECTOR | ghz_y_x_y.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines click | 170 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines parts | 160 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_y_y_x.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_y_y_x.json | run_inputs | intervals | 60 |
| NODEDETECTOR | ghz_y_y_x.json | run_inputs | clicks | 3 |
| NODEDETECTOR | ghz_y_y_x.json | run_inputs | clicks left | 1 |
| NODEDETECTOR | ghz_y_y_x.json | run_inputs | clicks right | 1 |
| NODEDETECTOR | ghz_y_y_x.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines click | 170 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines parts | 160 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_x_x_x.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_x_x_x.json | run_inputs | intervals | 60 |
| NODEDETECTOR | ghz_x_x_x.json | run_inputs | clicks | 3 |
| NODEDETECTOR | ghz_x_x_x.json | run_inputs | clicks left | 1 |
| NODEDETECTOR | ghz_x_x_x.json | run_inputs | clicks right | 1 |
| NODEDETECTOR | ghz_x_x_x.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines click | 170 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines parts | 160 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_x_y_y.json | back_in_time | intervals 60 | MATCH |

## The counts under the click's plan (2026-10-19, branch claude/click-one-act)

The light's unit is the record's own, W_c sin omega at k = pi / 4 (C1), so the lay's count moved with
the unit and the mode files were written again at it (a5c8f0b): 4,243 per packet, where main carried
1,829 per packet before C1 and the reading above 1,702 per packet (3,574 for the record); the record
counts 12,298 by the record's own unit at the lay. The readings' tables above were taken before C1 and
are not re-run (the owner's word); their M and the gate's verdict are the readers' from the output
files of their own run.

## The click that runs back over three sides: the back world (2026-10-19)

The (x, x, x) world once more with one added word on its draw, `meeting: back`, and nothing more
(ALGEBRA.md, The meeting's reading, root or back, the owner's words of 2026-10-19, the N sides and
the run back's reach; ENGINE.md section 3, act 6, and section 10, item 11), written by
`build_back.py` beside the four as `ghz_back_x_x_x.json` with its mode file: the same square, the
same three beams, the same regions with their bases and patterns, the same seed 24. The run back's
reach is the cone, the default where the key is absent: the record's own light cone runs back, the
rest of the board untouched (neither read nor written; one ring beyond the cone read from the board
and asserted equal to the lay's frame 0 by the engine at every step). The law's words it reads: the
click is the meeting of the future with the past; backward, to the past, the click is a reading and
never a write.

### The design

At the window's close (the interval 60; the one window closes the three regions at one interval, so
the declared order, `left`, `right`, `top`) the sides draw one after another, each alone at its own
place with its own generator state: the first on its marginal from the booked joint shares, the sum
over the other sides' ports; each next side on its conditional from the same shares with the realised
ports fixed, the chain rule, exact in the books' integers; between the draws the record runs back to
its birth, the lay's interval 0, by the engine's own inverse inside its own light cone, and forward
again to the close, bit for bit, a reading and never a write; two runs back and forward for three
sides, five passes in the look: the run to the first close (pass 1, the intervals 0 to 60), the run
back (pass 2, 59 down to 0), the run forward to the second side's close (pass 3, 1 to 60), the run
back (pass 4) and the run forward to the third side's close (pass 5).

### The blind

In `expectation_back.json`, the folder's blind with the back world in the (x, x, x) run's place and
the key `back`, derived from the folder's blind before the run by `build_back.py`: the first side's
marginal 1 / 2 at either port; the second side's conditional 1 / 2 at either port whatever the first
realised; the third side's conditional 1 and 0 exactly, the port determined by the two before it
(plus after plus plus and after minus minus, minus after plus minus and after minus plus: an even
number of minus ports, the joint 0 at an odd); the sequential shares the joint shares exactly, 1 / 4
at the four even triples and 0 at the four odd; the same E_3 = +1 and, with the three root-mode
worlds, the same M = -4; three credit lines, `left` with `meeting: back` and `order` 1, `right` with
`order` 2 and `top` with `order` 3, the count 1 each.

### The reading (the branch atom-arranged, 2026-10-19)

Run by `tools/run_inputs.py` (LAWFUL, 60 intervals, the cone's assertion holding at every step back
and forward, no refusal), read by `tools/bell_gate.py` over the four output files with the back
world's in the (x, x, x) run's place against `expectation_back.json`: E_3(x, x, x) = +1, the
blind's; the eight shares 1 / 4 at the even triples and 0 at the odd, the root mode's; the marginals
1 / 2; M = -4 with the three root-mode worlds, the blind's; 60 intervals reported, 170 click lines
and 160 parts lines as in the root mode. The three credit lines at the interval 60: `left` realised
minus, `meeting: back`, `order` 1; `right` realised minus, `order` 2; `top` realised plus, `order`
3, the count 1 each and the record's count left 12,297 as in the root mode's lines: the triple (-,
-, +), one of the four the shares allow, the third port the one the two before it determine (minus
minus: plus, the blind's). The look (`ghz_back_x_x_x.look.json`, the stride 6: frame 0, every sixth
interval and each pass's last, 51 frames in the five passes, 11 and four times 10, the arrays by
their nonzero Nodes): the header `reach` cone, `cone_support` the lay's 569 Nodes (the three beams,
x 4 to 28 and y 2 to 30) and `cone_volume` per interval, 655 at the birth, 1,927 at the interval 12,
from which the cone holds the declared square of 33 x 33 whole (its farthest Node 13 Links from the
lay's Nodes), 2,059 at 13, and 8,865 of the grown board's 9,409 Nodes (97 x 97) at the close, inside
it; every frame carrying the board's tick, 60 through the two readings, and the frames of the passes
2 to 5 their `cone_radius`, t + 1 at the interval t; the frames' arrays the engine's as they stand,
outside the cone the board as the engine left it, the lay's frame 0 here. The cone stepped alone
(2026-10-20, the owner's word): the two runs back and forward step the record's cone and nothing
else, the ball's box with one ring read beyond it and asserted at the lay's frame 0, the rest of the
board neither read nor written, each close equal to the board run's bit for bit; the header's
`cone_stepped` sums to 1,320,928 Node-steps against the board run's 1,357,680 (the declared square
whole in the cone from the interval 12 and the box about twice the diamond's Nodes, so the saving is
modest and the principle the point). The page `ghz_back_x_x_x.html` (the blind, the gate's reading
and the run's output): the slider over the five passes with the bounds marked, the frame's label
with the tick, the interval the record is read at, the pass, the direction and the cone's radius and
support, the cone shaded on the board and on the view from above, the legend line and the radius
graph, the records' clicks table with the three draws in their passes; the page's count of the
cone's Nodes equals the look's |G| at every frame shown. The screenshots
`ghz_back_x_x_x.pass2.screenshot.png` (the run back at the interval 6, the cone 7 Links about the
beams, the square's corners outside it) and `ghz_back_x_x_x.pass3.screenshot.png` (the run forward
to the second side's close at the interval 6).
