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
`tools/bell_gate.py`), NODEREADER:

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
window inflows NODEREADER, the lay's count LATTICE; #1827 comment 5975991093):

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

## The gate's table

Every row is a reading of the experimenter's run on the current tree (main d00aa9e, 2026-10-04), re-run and
compared bit for bit by `tools/reading_gate.py`: the label the reading's own (NODEREADER for the credit
lines' clicks and the trials' coincidences, LATTICE for the verdict, the intervals, the line counts, the
end's books and the back-in-time pass), the world the folder's file, `by` the tool that re-runs it, the
reading in the gate's words and the value as its report prints it.

| label | world | by | reading | value |
| --- | --- | --- | --- | --- |
| LATTICE | ghz_x_y_y.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_x_y_y.json | run_inputs | intervals | 60 |
| NODEREADER | ghz_x_y_y.json | run_inputs | clicks | 3 |
| NODEREADER | ghz_x_y_y.json | run_inputs | clicks left | 1 |
| NODEREADER | ghz_x_y_y.json | run_inputs | clicks right | 1 |
| NODEREADER | ghz_x_y_y.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines click | 156 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines parts | 156 |
| LATTICE | ghz_x_y_y.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_y_x_y.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_y_x_y.json | run_inputs | intervals | 60 |
| NODEREADER | ghz_y_x_y.json | run_inputs | clicks | 3 |
| NODEREADER | ghz_y_x_y.json | run_inputs | clicks left | 1 |
| NODEREADER | ghz_y_x_y.json | run_inputs | clicks right | 1 |
| NODEREADER | ghz_y_x_y.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines click | 156 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines parts | 156 |
| LATTICE | ghz_y_x_y.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_y_y_x.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_y_y_x.json | run_inputs | intervals | 60 |
| NODEREADER | ghz_y_y_x.json | run_inputs | clicks | 3 |
| NODEREADER | ghz_y_y_x.json | run_inputs | clicks left | 1 |
| NODEREADER | ghz_y_y_x.json | run_inputs | clicks right | 1 |
| NODEREADER | ghz_y_y_x.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines click | 156 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines parts | 156 |
| LATTICE | ghz_y_y_x.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_x_x_x.json | run_inputs | verdict | LAWFUL |
| LATTICE | ghz_x_x_x.json | run_inputs | intervals | 60 |
| NODEREADER | ghz_x_x_x.json | run_inputs | clicks | 3 |
| NODEREADER | ghz_x_x_x.json | run_inputs | clicks left | 1 |
| NODEREADER | ghz_x_x_x.json | run_inputs | clicks right | 1 |
| NODEREADER | ghz_x_x_x.json | run_inputs | clicks top | 1 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines click | 156 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines parts | 156 |
| LATTICE | ghz_x_x_x.json | run_inputs | lines credit | 3 |
| LATTICE | ghz_x_y_y.json | back_in_time | intervals 60 | MATCH |
