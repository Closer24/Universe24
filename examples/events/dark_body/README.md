# The dark body: content without clicks

Two worlds of one base, written by `make_worlds.py` (ALGEBRA.md 9.54 (4);
the model owner's word of 2026-09-25 through the Boss, record 2015; BUILD.md
section 26 item 39). Built now; RUN ONLY WHEN THE MODEL OWNER SAYS THE
ENGINE IS STABLE. The pins in `expectations.json` are declared here from the
algebra, blind, before any run; a reading outside its band is reported with
its numbers and never moved.

## The GameBoard

One layer of 400 x 200 x 1 Nodes, x closed (mirrors), y open (a zero face
with the receiver slab one Node deep), the Node clock 10^4 (the weak-field rule's
integers, ALGEBRA.md 9.57 (2) and 9.61 (3), BUILD.md section 26 item 44; 10^6
HISTORY), the rule with the Node's own pace entering twice (item 44; item 36's
first-order rule HISTORY), five families: light on the given clock
[512, 1], the matter kind [800, 809], the family `dark` of the same kind, the
family of clicks and the family of charge; every family's charge 0.

- **The emitter**: a body of the matter kind in the well [800, 801], the
  train's 32 Nodes along x and 5 across at [5, 37) x [98, 103), seeded on its
  mode at 2^18, the stock 30 held as light beside its one own quantum (BUILD.md section 26 item 47); its emitter gives light along +x with a train
  of 8 periods; its records' ladder the screen's cubes (the bright world's
  body first).
- **The body**: 32 x 5 Nodes at [184, 216) x [143, 148), its centre (200, 145),
  45 Links beside the beam's line y = 100, holding M = 4812 quanta at every
  Node (below Gamma = 10^4, the load's guard; the static level on the beam's
  line under it 2000, U_b = 0.1; 100000 at Gamma 10^6 HISTORY; the family of
  clicks held at M there, its field the discrete Coulomb
  potential around it, ALGEBRA.md 9.41 (3)).
  - `dark.json`: the family `dark`, charge 0, no emitter, on no detector set:
    it gives nothing and takes nothing (ALGEBRA.md 9.54 (2)).
  - `bright.json`: the family `matter` with an emitter of light (its own
    giving clicks toward the screen) and the detector set `at_body` bound to
    its Nodes (its taking clicks, the shadow it casts on the beam).
- **The screen**: 40 detector cubes of side 3 (`screen_<y>`, record 1899) in
  the column x = 380 from y = 40 to 160, receiver bodies of light.

## The pins (declared blind, `expectations.json`)

| Pin | Kind | Value |
| --- | --- | --- |
| dark: the emitter's records' clicks at the screen | DETECTOR | 30, the stock: every record arrives, no shadow |
| dark: clicks at the body, light from the body | DETECTOR | none: no set on it, no giving line of its number |
| bright: the emitter's records' clicks at the screen | DETECTOR | below 30 by the body's taking clicks (the shadow); the body's own giving lines present |
| the bend | DETECTOR | the centroid of the emitter's records' clicks over the screen's cubes, in y, less the beam's line: 76.3 Links toward the body (the ray's COMPUTATION at the regenerated content; 13.7 at Gamma 10^6 and M = 100000 HISTORY), the band 30 percent; the same in both worlds within one cube. The pre-change controls of 2026-09-25 (BUILD.md section 26 item 41, `../toward_nature/README.md`) read +5.7 +- 7.4 and +4.0 +- 7.6 Links at the old numbers: the beam at k = pi / 2 is not a ray, it spreads to 35 Links rms at the screen |

The bend's number: the family of clicks' static level on this board with the
body's Nodes held at M and the faces at 0 (the plain step's fixed point,
solved), and the ray of the given clock traced through it by 9.29's equations
under the Node's own pace (9.50 (13)); the packet averages the gradient and
falls short of the ray (9.29's table), inside the band. Both worlds are read
in both worlds (ALGEBRA.md 9.51 (7)): the counts and the centroid are clicks;
the family of clicks' level beside the two bodies (equal) and the family of
charge (flat) are GAMEBOARD diagnostics, read by `tests/test_dark_body.py`
over 80 intervals without the pins.
