# Rerun of the seven probes, and the plan of my own checks

## Rerun (fam_phys/rerun/, with t24b/.venv/bin/python -I, from the families/ sources)
probe_kinds 0 s, probe_48 2 s, probe_spinor 2 s, probe_act 15 s, probe_pair 3 s, probe_induced 98 s, probe_pauli2 4 s:
all seven outputs byte-identical to the text's (cmp), stderr empty. (probe_pauli2's docstring says "about two minutes";
it took 4 s here.)

## What the probes lay (read from the code, not the text)
- probe_induced / probe_pauli2 lay the eight-gear G3/2 as a train {"kinds": ["A1"], "part": 8}: the engine knows no
  G3/2 kind (kinds.py has the 24's five); the 48 are applied from outside when checking the images, and J is laid
  through an external table built by the probe (IND.table). So "runner/files.py accepts G3/2's eight-gear form" is
  a reading of vocabulary's `wholes` on a kind the files cannot name: untested on the files as built.
- "Light" in probe_pauli2 is t1 at part 1 (no winding), laid a = b = v drawn in [-100, 100] independently at every
  Node-clock: a static white-noise field, not a propagating wave; no frequency, no beat; the half-speed family has no
  spring (massless): no threshold can be asked of this probe.
- The two "quanta": phi lay a = 40 phi0, b = a + 2 I phi0 -> w_I = 2 x 40 x |phi0|^2 = 2400; the "same state" lay
  2 phi0 at size 40 with k = 2 -> w_I = 9600; the "partner" 5 J phi0 with k = 1 -> w_I = 5 x 54 x 30 = 8100 (the
  text's lay totals 12000 and 10500 agree). In the engine's own quantum (a key of winding, TERM11) the two "quanta"
  are 1 : 4 and 1 : 3.4. Both lays turn FORWARD in I (k > 0): same sign of w_I = same charge, if w_I is the charge.
- The pair hand is read by THREE RUNS (phi alone, chi alone, both) and epsilon of the two separate runs' hands at
  each site: a comparison of counterfactual boards. The board holds h_phi + h_chi only.

## Checks to build (whole numbers, carry only)
c1_pairhand.py:
  1. the board holds the sum (gears where both != phi + chi, the largest gap: rounding);
  2. two splits of ONE board give two pair hands (the pair hand is the bookkeeping's, not the board's);
  3. the same reading on the engine's light kind, T1 at part 2 (the complex cross product, the engine's own
     antisymmetric channel T1 x T1 -> T1): one state 0, an orthogonal state full;
  4. I's cycles (4 signed 2-cycles): the 8 gears are 4 planes, so term 11's two parts are there;
  5. the residual of h_phi(x, t) off the plane (phi0, I phi0) under the free act: the "same state" result is the
     scalar propagation of 8 alike rows;
  6. the symmetric, T1-valued pair hand (the text's own table c8) for one state: not 0 (the stretched state).
c2_light.py: the pair hand and the books (w_I, w_J, w_K) under J for the generic and the I-averaged table, with
  light random per site (the text's) against light uniform over the board (my control); the free act beside.
c3_doublers.py: the 24-gear train: its commutant (rank 24), the right-regular 48 signed permutations commuting with
  the left 48 (the doublers' internal group), the whole-number isotypic pieces (E1/2 + E5/2: 8; G3/2 twice: 16),
  T1 in (E1/2 + E5/2) x G3/2 by characters, and the text's own 24-gear table's blocks between the two pieces (light
  converts the doublet content into quartet content).
