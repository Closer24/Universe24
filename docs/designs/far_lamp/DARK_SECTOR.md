# The dark sector against the law's own rules: does "no dark energy and no dark matter" close the picture?

The model owner, 2026-09-21 (translated): "look at what they say about dark
matter, why galaxies at the edge rotate the way they do and what the
measurements are; maybe they simply look at everything behind a detector
and that is what makes their shifts; check that it fits and then say
hypothesis or not: that with us there is no dark energy and no dark
matter, and that closes things nicely and cleanly." Written by the
mathematician, read-only, on the law as it stands on main; every number
made by the host script [dark_sector_map.py](dark_sector_map.py) with its
output [dark_sector_map.out](dark_sector_map.out); no run; nothing here is
a rule. Notation per record 184; rows and bodies, not light and matter.

**The verdict in one line.** Not a hypothesis: on the law's own rules the
detector adds nothing at a galaxy's edge, the field is Newton's in the
shell mean, the one route the law has to a flat curve without unseen
content (a short periodic dimension, [HYPOTHESES.md](../../HYPOTHESES.md)
entry 6) fails nature's Tully-Fisher slope and would repeat the sky, and
the brightness of a far lamp reads farther from the data than Milne
([BRIGHTNESS.md](BRIGHTNESS.md)); what the law admits is unseen content as
an input family, exactly as nature's model does.

## 1. What they say, and which of it rests on a detector's shift

The evidence for unseen content, in the order it came:

1. **The clusters** (Zwicky, 1933): the galaxies of the Coma cluster move
   too fast (a Doppler reading) for the visible content to hold them.
2. **The rotation curves** (Rubin and Ford, Bosma, 1970 to 1980): the
   speed of a disc galaxy's gas, read in the 21 cm line (a Doppler
   reading) out to several times the visible disc, stays flat at 100 to
   250 km/s where the visible content alone would give a Keplerian fall
   as `1 / sqrt r`. The relation between the flat speed and the visible
   content is tight, `M_b = 47 M_sun (v / km s^-1)^4` (the baryonic
   Tully-Fisher relation, McGaugh 2012, slope 3.9 +- 0.2), and the
   departure from Newton sets in at one acceleration, `a_0 = 1.2 x 10^-10
   m s^-2`, not at one radius (the radial acceleration relation, McGaugh,
   Lelli and Schombert 2016).
3. **The hot gas** of clusters (X-ray, from 1980): its temperature and
   profile (no Doppler) need a holding content several times the gas and
   the stars.
4. **The bending of rows** (lensing, from 1980; the Bullet Cluster, Clowe
   and others 2006): the images of far sources are bent by the clusters
   (no Doppler), and in the Bullet Cluster the bending mass sits where the
   galaxies are and not where the hot gas, which holds most of the
   visible content, was left by the collision.
5. **The acoustic peaks** of the microwave background (from 2000): the
   third peak's height (no Doppler) gives a content that does not couple
   to the rows six times the one that does.

So the owner's question, "is it the shift read behind a detector?", can
reach items 1 and 2 only; items 3, 4 and 5 are not shifts. And for items 1
and 2 the law's own detector rule answers: section 2 of
[DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) reads the receiver's
Doppler as `1 +- v / c` exactly over whole Links, the source's as `1 / (1
-+ v / c)`, the transverse exactly 1, and the moving reader's count (12b)
as `1 - n . beta`. At a galaxy's edge `beta = v / c` is 3 to 7 parts in
`10^4`:

| v, km/s | beta | the receiver's ratio | the source's | the moving reader's factor | every departure from the classical Doppler |
| --- | --- | --- | --- | --- | --- |
| 80 | 2.7e-4 | 1.000267 | 1.000267 | 0.999733 | order `beta^2` = 7e-8 |
| 150 | 5.0e-4 | 1.000500 | 1.000501 | 0.999500 | 2.5e-7 |
| 220 | 7.3e-4 | 1.000734 | 1.000734 | 0.999266 | 5.4e-7 |

The curves are read to a few km/s out of 100 to 250, that is to a part in
100 of the shift; the law's readings differ from the classical Doppler by
parts in `10^4` of the shift (the departures `7 x 10^-8` to `5 x 10^-7`
over the shifts `2.7 x 10^-4` to `7.3 x 10^-4`, that is parts in `10^7`
of the reading), a hundred times below the curves' own precision. **No reading through a detector makes a Keplerian
edge look flat**: the shifts are what the law itself would read.

## 2. What the law's field does at a galaxy's edge

Section 3.2: the field along a beam does not fall (`1 / r^0` on a digital
line, 0 off it), and the inverse square is the density of beams over a
shell, `<V>(r) = q Q / N(r)` with `N(r) -> 4 pi r^2`; Gauss's law is
exact and Newton's `a = -G M / r^2` is reached in the shell mean (3.6). A
galaxy's edge is read over many stars at many angles from `10^11`
sources: the shell mean, Newton's, and the same Keplerian fall nature's
visible content gives. The two lattice departures of section 3.5 do not
help: the beam's non-dilution averages to the shell mean (the flux is
conserved, Gauss exact), and the six-heading shells depart at small r,
not large. The growing wall does not touch the push between bodies at
rest (15.4 (iii)), and the retarded force of a moving source is short by
`1 / gamma` (12b.3), a part in `10^7` at these speeds.

## 3. The one in-law route to a flat curve, and where it fails

HYPOTHESES 6 (measured 2026-09-16 on the earlier model, before `beam-v1`,
and true of `beam-v1` by section 3.2's shell count): in a periodic slab
whose third dimension is short, the shell beyond the slab's thickness is
a cylinder, `N(r) -> 2 pi r x thickness`, and the mean falls as `1 / r`:
a flat curve with nothing added to the law. The script counts the shells
on the lattice (the exponent p of the mean between successive radii):

| the board | `N(r)` at r = 4, 8, 16, 32 | p at r 4 to 8 | p at r 16 to 32 |
| --- | --- | --- | --- |
| open | 210, 762, 3338, 12606 | -1.9 | -1.9 |
| slab, thickness 3 | 80, 136, 320, 564 | -1.0, -0.4 (the lattice ripple) | -0.7, -0.9 |
| slab, thickness 9 | 210, 432, 920, 1756 | -1.2, -0.9 | -1.0, -0.9 |
| slab, thickness 27 | 210, 762, 2832, 5300 | -1.9 | -0.9, -1.0 |

(HYPOTHESES 6's own measurement: -0.97 +- 0.10 in the period-3 slab,
-2.04 +- 0.12 on the open cube.) The flat part begins at a radius set by
the thickness, **one length for every source**. Three things follow, each
against nature:

- **The Tully-Fisher slope.** Under a `1 / r` force beyond the thickness
  L, `v^2 = r F / m` is constant in r at `v^2` proportional to `M / L`:
  `v^4` proportional to `M^2`, slope 2, where nature's is 4. Anchored
  where both give 215 km/s at `10^11 M_sun`, a dwarf of `10^9 M_sun`
  rotates at 68 km/s in nature and would rotate at 22 under the slab
  (the ratio 0.32; at `10^8`, 0.18).
- **The scale.** Nature's departure from Newton sets in at one
  acceleration `a_0`, in dwarfs at a fraction of a kpc and in giants at
  tens of kpc; the slab's sets in at one radius.
- **The sky.** A periodic third dimension of 1 to 10 kpc, the thickness
  the curves need, shows every source again at 1, 2, 3 (or 10, 20, 30)
  kpc along that axis, the Milky Way included. Nature's sky does not
  repeat at any such spacing.

So the closed dimension is a real mechanism of the law and not a fit to
nature's curves.

## 4. The rows are not bent on main

Section 5.4: on main a row reads nothing of the crowd, "neither bent nor
delayed beside a mass, exactly" (series K, the deflection 0.000 pixel).
Under the world key `meeting-v1` (off by default) a row turns toward the
crowd it meets, in the form `M / b` with a grain constant, the value out of
reach by the grain. Either way item 4 of section 1 is not answered by the
law without unseen content: on main there is no bending at all (against
the 1.75 arcsecond of 1919 before any cluster), and under the meeting the
bending follows the content met, so a bending mass where no visible
content is (the Bullet Cluster) needs unseen content there, as nature's
model says. Items 3 and 5 the law does not speak to.

## 5. Dark energy: already answered on the register, and now after a detector

Record 124 (Highlights 5.4, series G2): "nothing in the law gives `q < 0`,
so what is observed today needs something added, as in general
relativity". [BRIGHTNESS.md](BRIGHTNESS.md) adds the detector: the far
lamp's brightness reads `q_eff = +1`, farther from the data than Milne,
and HYPOTHESES 7's own Pantheon+ fit found the one-factor reading "behind
at every exponent". The growing wall carries no dark energy and the
brightness says the law is short of it, not free of it.

## 6. Hypothesis or not

**Not a hypothesis** that the law supports, on its own rules and numbers:
the detector's shift is exact at these speeds (section 1), the field is
Newton's (2), the closed dimension fails the slope, the scale and the sky
(3), the rows are not bent (4), the far lamp is too bright (5). What the
law does admit, cleanly, is **unseen content as an input**: a family of
the table with a charge column 0 and no lamp pushes and is pushed by the
width S like every other content and releases no row a detector reads;
nothing in the six forbids it, nothing derives it, and its amount per
galaxy is an initial state, as in nature's model. The clean closure the
owner asks for would need a rule that is not one of the six (an
acceleration floor `a_0`, which is what the radial acceleration relation
measures), stated under its own identity and tested against the same
three tests; this note proposes none. The owner's second look, whether S can be
derived and whether the push's rounding is that floor, is
[S_AND_A0.md](S_AND_A0.md): neither, on the law's own arithmetic.

## 7. Links

- The Doppler of the receiver and the source: [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) section 2; the shell mean and what departs: 3.2, 3.5, 3.6; the rows beside a mass: 5.4; the moving reader: 12b; the growing wall: 15.
- The register's own dark sector: [HYPOTHESES.md](../../HYPOTHESES.md) entries 6 and 7; [HIGHLIGHTS.md](../../HIGHLIGHTS.md) section 5.4, series G2 (record 124).
- The far lamp after a detector: [BRIGHTNESS.md](BRIGHTNESS.md).
- The map: [dark_sector_map.py](dark_sector_map.py), [dark_sector_map.out](dark_sector_map.out).
