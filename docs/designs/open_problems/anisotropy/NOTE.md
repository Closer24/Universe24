# The moving laboratory's anisotropy without contraction: what the arm is made of decides, and what closes it (the open-problems physicist, read-only, 2026-09-21)

Problem (3) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing): "the moving laboratory's
anisotropy without contraction (the paper's own row): no fix without
changing the model". NATURE row 5b: a light clock in motion at beta is
the classical ether clock, its round trip `gamma^2` along the motion and
`gamma` across, so two arms of one length differ by `gamma - 1 = beta^2 /
2`, `5 x 10^-9` at the Earth's orbital speed and `7.6 x 10^-7` against the
cosmic background, where the resonators bound it at `10^-17` to `10^-18`:
FAIL by nine to twelve orders. Read against `main` at be194aca and the
two notes before this one (the light-bending note, PR #602, and the
Lorentz note, PR #603, under docs/designs/open_problems/, on their
branches at the time of writing). Every number is from
anisotropy_map.py (`docs/designs/open_problems/anisotropy/anisotropy_map.py`, deleted 2026-09-26) beside this note and its output
[anisotropy_map.out](anisotropy_map.out): sections A, B and D closed
forms; section C a continuum integration in floating point, labelled so
(the method of DERIVATIONS 12b.2's `orbit_thrown.py`), a check of
closed forms and not a lattice reading; no run, nothing registered,
nothing decided. Notation as the workflow's rule: gamma the Lorentz
factor, beta the speed over c, **p** the momentum vector, E the energy,
A the age moment (the retarded potential), **V** the flow.

## 0. The verdicts, stated at the top

| Candidate for closing row 5b | What it is | Verdict |
| --- | --- | --- |
| (i) no change: the laboratory at rest in the lattice's frame | the anisotropy exists and the Earth does not move in the frame | **NOT ADMISSIBLE**: the orbital 30 km/s modulates any rest frame by `5 x 10^-9` over the year, eight orders above the bound; no mechanism drags a frame |
| (ii) a rigid arm of contact bonds (whole Links) contracted by a rule | the arm the law's bound sets are (BEAM_LAW note 31 (ix): the contact, a refused step) | **NOT ADMISSIBLE**: no verb shortens a Link (the position accumulator carries one Link per carry); the round trips `gamma^2` and `gamma` are exact on it; the FAIL is a theorem for this arm |
| (iii) a push-bound arm (an orbit) under covariant-readings-v1 alone | the relativistic dispersion with the push `-grad A` (17.6 M4) | **NOT ADMISSIBLE**: `-grad A` on a co-moving pair is `gamma^2` times Lorentz's force on every Node (section 3, an identity); the thrown orbit is stiffer and elongated ALONG the motion (1.06, 1.14 at beta 0.21, 0.43), the period shorter (0.96, 0.83): the wrong sign of contraction |
| (iv) a push-bound arm under covariant-readings-v1 with the magnetic term (`source-velocity-v1`) | the relativistic dispersion with Lorentz's force from Maxwell's field of the moving source | **ADMISSIBLE WITH CORRECTIONS** (section 3): the thrown orbit is the rest orbit contracted by `1 / gamma` along the motion with the period `gamma` (0.9768 / 0.9767, 0.9031 / 0.9030, 0.8001 / 0.8000 at beta 0.21, 0.43, 0.60; Lorentz 1904), so a laboratory built of push-bound matter reads no anisotropy; the corrections: `source-velocity-v1` is named, not designed, and its local road is section 4's |

So the honest answer to "no fix without changing the model" is sharper
than the row: the anisotropy is exact for whatever the law holds
together by contacts, and it closes exactly for whatever the law holds
together by pushes, provided the push is Lorentz's, which needs the one
identity nobody has designed. Nature's rulers are push-bound (crystals,
atoms); the law's registered bound sets (the deuteron of series I and N,
the contact pairs) are contact-bound. The row stays FAIL under the law
and under covariant-readings-v1, and its closure is one identity away,
the same one that closes E3 and E7 of the Einstein map.

## 1. The pins, before any number

- **Nature.** Michelson and Morley 1887; the resonator bounds Herrmann et
  al. 2009 (`10^-17`) and Nagel et al. 2015 (`9.2 +- 10.7 x 10^-19`), as
  NATURE 5b cites them (to verify against the sources). The laboratory's
  speed in any frame fixed in space: at least the orbital 30 km/s for
  part of the year (beta `10^-4`), 370 km/s against the cosmic
  background (beta `1.23 x 10^-3`).
- **The register.** NATURE 5b, pinned by DERIVATIONS 12.3 (the round
  trips 1.375 and 1.140 at beta 0.4297 on the flight table, farther from
  `gamma` by the whole-Link steps); 24.3 row 6 (REFUTED on `main` by nine
  orders; the contraction not derived under covariant-readings-v1 either,
  17.6 M4); the Lorentz note's section 3 (the mechanism, exact:
  Pythagoras in the flight table).
- **What must not move.** The rows' one pace in the lattice's frame
  (4.1); NATURE 5b's FAIL under the law as the law's registered prediction.

## 2. The anisotropy on the GameBoard, and why it is exact for a rigid arm

**The pieces.** A laboratory's arm is two bodies held at a fixed
separation; a light clock is a row sent from one to the other and back.
On the GameBoard a body holds another at a fixed separation in one of
two ways: by the CONTACT (BEAM_LAW note 31 (ix): a refused step onto an
occupant hands the momentum component over; the pair stands one Link
apart, or a lifetime holds a set at whole Links), or by the PUSH (a
bound orbit, the probe's drive against the source's push at an
equilibrium radius: series D, 12b.2). A row's transit is the flight
table's, one pace in the lattice's frame (the Lorentz note's section 3:
`gamma^2` along, `gamma` across, exact in the continuum, to the grain on
the lattice). So the arm's round trips are fixed by its LENGTH in Links
and nothing else, and the anisotropy of a laboratory is the question
whether its arm along the motion is shorter, in Links, than its arm
across, by `1 / gamma`.

**The contact arm.** A contact bond is a whole Link, and every count of
the six verbs that moves a body carries one Link per carry of the
position accumulator; the drive under form B or under the identity
carries one Link per carry likewise; nothing in the counts table reads a
Link's length. A contact pair thrown along its bond stays one Link apart
(the leapfrog and the hand-over of 10.5 change the timing, not the
separation); thrown across it stays one Link apart. The map's section A
is then exact on it: `gamma^2 x 2 d / c` along and `gamma x 2 d / c`
across, the difference `gamma - 1` at every speed. **A theorem of the
declared rules**: the law's rigid arm cannot contract, and a laboratory
made of it fails 5b by exactly `beta^2 / 2`.

**The push arm.** An orbit's radius is an equilibrium of the push
against the drive, and both change in motion: the drive by the
dispersion (form B's `p / (m + p / c)` on `main`, the exact square's `p
c^2 / E` under the identity) and the push by the field of a moving
source (the retarded flux along `n_ret` on `main`, 12.1; `-grad A` under
the identity, 17.6 M4; Lorentz's force with the magnetic term under
`source-velocity-v1`). 12b.2 integrated the first pair: the thrown orbit
contracts along the motion by 0.87 to 0.96 against Lorentz's 0.977 at
beta 0.21, slows by 1.31 to 1.43 against 1.024, drifts and decays: the
law's own dispersion (the longitudinal mass `m (1 + v / (c - v))^2`)
and the flux's asymmetry. Section 3 integrates the other two.

## 3. Theorem: `-grad A` is `gamma^2` times Lorentz's force on a co-moving pair, so the identity alone elongates the arm; with the magnetic term the arm contracts by `1 / gamma` exactly

**The identity, in three lines.** Let the source move at beta along x
and **x** = (x_par, x_perp) be a Node's position from the source's
PRESENT position. DERIVATIONS 12.1: the age moment is the
Lienard-Wiechert scalar potential, `A = q / D` with `D^2 = x_par^2 + (1
- beta^2) x_perp^2` (Heaviside's ellipsoids). Then

    -grad A = q (x_par, (1 - beta^2) x_perp) / D^3.

Maxwell's field of the same source is `E = q (1 - beta^2) (x_par,
x_perp) / D^3` and its magnetic field `B = beta x_hat x E` (c = 1), so
the Lorentz force on a probe co-moving at beta is `F = (E_par, (1 -
beta^2) E_perp) = q (1 - beta^2) (x_par, (1 - beta^2) x_perp) / D^3`.
Compare: `F = (1 - beta^2) (-grad A) = (-grad A) / gamma^2`, component by
component, at every Node. The magnetic term on a co-moving pair is one
isotropic factor `1 / gamma^2` on the gradient of the age moment; 17.6
M4's "the rest force along and `gamma` times the rest across" is the
same statement read on the two axes (`-grad A` along: `q / x_par^2`;
Lorentz's: `q (1 - beta^2) / x_par^2`; across: `gamma q / x_perp^2` and
`q / (gamma x_perp^2)`).

**What each push does to the arm** (the map's section C: a probe of mass
1 about a heavy source, both at beta along x, the relativistic
dispersion `v = p c^2 / E`, the rest orbit circular at r0 = 100 with the
orbital pace 0.1 c, the launch velocity added relativistically, three
rest periods; the extents along and across the motion over the rest
diameter, their ratio, the period over the rest period):

| beta | the push | along / across | the ratio (Lorentz `1 / gamma`) | the period (Lorentz `gamma`) | the end |
| --- | --- | --- | --- | --- | --- |
| 0.2148 | Lorentz's force (Maxwell's field, the probe's own velocity in `u x B`) | 0.982 / 1.005 | 0.9768 (0.9767) | 1.034 (1.024) | bound |
| 0.2148 | `-grad A` alone (covariant-readings-v1's (ii) as amended) | 1.018 / 0.959 | 1.061 (0.9767) | 0.965 (1.024) | bound |
| 0.4297 | Lorentz's force | 0.908 / 1.005 | 0.9031 (0.9030) | 1.119 (1.108) | bound |
| 0.4297 | `-grad A` alone | 0.957 / 0.843 | 1.136 (0.9030) | 0.828 (1.108) | bound |
| 0.6000 | Lorentz's force | 0.804 / 1.005 | 0.8001 (0.8000) | 1.263 (1.250) | bound |
| 0.6000 | `-grad A` alone | 0.793 / 0.726 | 1.092 (0.8000) | 0.711 (1.250) | falls in |

Under Lorentz's force the thrown orbit is the rest orbit contracted by
`1 / gamma` along the motion to four digits at three speeds (the period
1 percent above `gamma`, the rest orbit's own relativistic correction at
0.1 c: a check of the integrator, Lorentz's 1904 theorem). Under `-grad
A` alone the force is `gamma^2` times too strong on every Node, the
orbit is tighter across (0.96, 0.84, 0.73) than along (1.02, 0.96, 0.79),
the arm is LONGER along the motion than across by 6 to 14 percent, the
period shorter, and at 0.6 c the probe falls in. So the two arms of a
laboratory built of push-bound matter read: under the law, the
anisotropy of 12b.2 (larger than Lorentz's, unstable); under
covariant-readings-v1 alone, an anisotropy of the wrong sign; under the
identity with the magnetic term, none. The register's 5b is closed by
exactly one thing: the factor `1 / gamma^2` on the push of a moving
source, which is the magnetic term.

## 4. The magnetic term without a label on the row: a road for `source-velocity-v1`, named

17.6 M4 named `source-velocity-v1` as "a row carrying its source's
momentum label at release", a new component of the row's record. The
map's section D shows a second road that needs no new component: at a
Node beside a moving source the law already holds two readings of
different geometry, the flow **V** along the RETARDED direction `n_ret`
(the rows come from where the source was) and the gradient of the age
moment `-grad A` from the PRESENT position (12.1's ellipsoids are about
the present position). The angle between them is the source's
aberration, `asin(beta)` on the transverse Node (12.4 degrees at beta
0.2148, 25.45 at 0.4297) and a known function of beta and the angle
elsewhere; so beta is a reading of one Node, from the two moments the
identity already reads (LOCALITY-1: the record and its six neighbours,
nothing kept at a Node). The push that Lorentz's force needs is then
`(1 - beta^2)` times `-grad A` on a co-moving probe, and in general the
force on a probe of velocity **u**, `E + u x B`, with `E = -grad A - beta
(x_hat . grad A)`-like terms and `B = beta x_hat x E`, all bilinear in
the two readings and the probe's own momentum once beta is read. What
this road costs, stated so that its designer can weigh it: the angle
between two integer vectors is a comparison (the evaluation verb), not a
root; beta from it is a table at load (like `THETA_G`); the six-Port
gradient of A is a field only at a dense fan (the light-bending note's
section 4: at series K's fan it is a comb), so the road works where the
covariant push itself works and nowhere else. Named for the physicist,
not designed here; its three tests are the covariant push's with one
table more.

## 5. What each candidate gives for NATURE's rows

| Row | The law | covariant-readings-v1 | with `source-velocity-v1` |
| --- | --- | --- | --- |
| 5b, the frame's anisotropy, a contact arm | FAIL, `beta^2 / 2`, exact (section 2) | the same FAIL | the same FAIL: a contact bond never contracts |
| 5b, a push-bound arm (an orbit) | FAIL: the contraction 0.87 to 0.96 against 0.977, the period 1.31 to 1.43 against 1.024, unstable (12b.2) | FAIL, the wrong sign: elongated along the motion 1.06 to 1.14, the period 0.83 to 0.96 (section 3) | PASS in the continuum: `1 / gamma` and `gamma` to four digits (section 3); the lattice's grain to be read by a run |
| 5a, the grain's anisotropy of c | BOUND on Q (`Q >= 2^56`) | the same | the same: the pace's rounding is the table's, not the arm's |
| 4a, 4b | FAIL | PASS (the Lorentz note) | PASS |

**The pin for a run, when the two identities exist** (12b.2's thrown
orbit at beta 0.43 in the Newtonian regime S = 512 or 8192, 17.6 M5's
geometry, both identities on): the extents' ratio along over across
`0.903` within one Link on 26 (2.5 Links), the period `1.107` times the
rest within 2 percent; under the identity alone (`-grad A`) the ratio
above 1 by 5 to 15 percent and the period below the rest: the two
readings that tell the three pushes apart in one run (GAMEBOARD, the
step lines; DETECTOR, the source's click list as row 58's lamp worlds
read it). No world for a contact arm is needed: its FAIL is exact.

## 6. The owner's question on the conditional derivations, for this problem

- **Is the contraction derivable?** For a contact arm, no, and it never
  will be: the Link is the ruler. For a push-bound arm, yes, as a
  theorem once the push is Lorentz's (section 3, Lorentz 1904 on the
  law's own potential): the derivation exists and its condition is the
  magnetic term, `source-velocity-v1`.
- **What a derivation of the magnetic term would take**: either the
  row's source-momentum label (M4's road, one declared component) or
  section 4's reading of the aberration between the flow and the
  gradient (no new component, one table at load, a dense fan). Neither
  is in the six verbs as declared; both pass the three tests on paper
  as the covariant push does.
- **Can the paper stand with the conditional statement?** Yes, if it
  says which arm: "a laboratory held together by contacts reads the ether
  clock's anisotropy `beta^2 / 2`, registered FAIL; one held together by
  pushes reads none under covariant-readings-v1 with the magnetic term,
  a theorem on the law's own retarded potential, the magnetic term one
  identity not yet designed; under the identity alone the anisotropy has
  the wrong sign". The row as it stands ("no fix without changing the
  model") is true and incomplete: the change is named, it is one, and it
  is the same one E3 and E7 need.

## 7. Proposed lines for the documents I do not write

- **NATURE.md row 5b** (the physicist): the sentence "what would remove
  it is a contraction of the arm along the motion by `1 / gamma`, which
  is route B or C of record 230 and not the six verbs (12.5 (vi))" to
  read "which no verb gives a contact arm, and which a push-bound arm
  has exactly under covariant-readings-v1 with the magnetic term
  (`source-velocity-v1`, the open-problems note on the anisotropy,
  section 3) and with the wrong sign under the identity alone".
- **DERIVATIONS_BEAM 17.6 M4** (the mathematician): after "the rest force
  along and `gamma` times the rest across": "that is `gamma^2` times
  Lorentz's force on a co-moving pair on every Node, one isotropic
  factor; the thrown orbit under it is elongated along the motion, not
  contracted". And 21.4 rows E3 and E7: the second road of section 4
  beside the label.
- **DERIVATIONS_BEAM 24.3 row 6** (the same): the verdict column gains
  "closed for a push-bound arm by `source-velocity-v1` (a theorem on
  12.1's potential); exact FAIL for a contact arm under every identity".
- **The paper** (the coordinator): the open problems' item (3) restated
  as section 6's sentence.
- **HIGHLIGHTS 5.4**: nothing.

## 8. Questions, through the Boss

1. **For the owner (substantive)**: none the physics leaves open. The
   design of `source-velocity-v1` is the physicist's when the owner
   orders it; this note gives it a second road (section 4) and the pin
   (section 5).
2. **For the Boss**: none; no run is proposed before the two identities
   exist.

## 9. Links

[NATURE](../../../NATURE.md) rows 5a and 5b;
[DERIVATIONS_BEAM 12.1](../../../DERIVATIONS_BEAM.md#121-the-field-of-a-moving-source-the-laws-push-in-the-continuum-limit),
[12.3](../../../DERIVATIONS_BEAM.md#123-the-bond-clock-under-1-to-3),
[12b.2](../../../DERIVATIONS_BEAM.md#12b2-the-orbit-as-the-bond-the-registered-orbit-thrown),
[17.6](../../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes) (M4, M5),
[24.3](../../../DERIVATIONS_BEAM.md#243-the-delta-p-table-every-computable-difference-from-quantum-mechanics-or-relativity-as-the-law-is-declared) row 6;
[BEAM_LAW note 31](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (the contact);
the Lorentz note, docs/designs/open_problems/lorentz/NOTE.md on PR #603 (section 3, the transverse and longitudinal light clocks);
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).

> The scripts of this folder (`anisotropy_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/open_problems/anisotropy/<script>`).
