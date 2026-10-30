# The hostile physicist on G2's two texts: N2's second text (term 5) and term 13 blind

The report as the reader gave it, 2026-10-30, filed by the Boss. The reader's whole-number checks and outputs stand
beside this file: a_source_and_energy.py (with _lib, a_results.txt: a one-site integer replica of tick_first, exact
at every round), b_gamma_pushed.py, c_lump_well.py, d_virial_quartic.py, e_adiabatic.py, f_notch_floor.py, each with
its *_results.txt. All three shipped probes reproduce bit for bit (copies diffed under copy/).

VERDICT on term 5: NOT PASSED
VERDICT on term 13: NOT PASSED

## TERM 5 (n2_second/README.md)

1. BLOCKING. The ii/jk slots' push has the wrong sign, so the push is not gravity at the gamma level (sec. 2 bullet 4,
   sec. 3 bullet 3, OPEN bullet 2; n2b_lib gradient_part/potential; t13 energy_source). The grip is den Gamma^2 + ii,
   linear, so the slot is g^{ii}; g^{ii} = eta^{ii} - h^{ii} while the teeth are -g^{00} = 1/c^2 + h_00/c^4: one sign
   parts the teeth from the grip, and the texts push both by +J. Measured (b_results B1): on the metric the push
   itself makes at P2's depth (c00 = 606, ii = +524 where the chosen ratio wants -50), light's period^2 ratio is 0.378
   against the clock's 1.205: 1 + gamma = -3.0. gamma = 1 is measured only on slots laid by hand (P2); the OPEN list
   concedes "the gradient part's sign raises them". Nor is -1/12 CHOSEN: with one coupling and the lattice's own eta
   (c^2 = grip_rest/rest = 1/6, two ends per Mesh) it is -c^2/2 per slot, a unit ratio. Fix: push ii, jk (and 0i) by
   -(2T - eta T)^{ij}, re-measure gamma from pushed slots on a lump; then -1/12 and gamma = 1 are derived from the 6
   Spokes and the two-ended Mesh, or the measured ratio is reported.
2. BLOCKING. The Newtonian well is nowhere shown (sec. 3; the only board is t13 probe 3). The static Poisson well for
   the lump's actual push (about 300 p00-counts a round through T_d = 1000, grip 500) is 0.23 notch (c_results C1);
   the quoted "well" of +-50 equals the 00 wave's site-to-site spread off the lump (41-75); and nothing binds the hand
   in space: 81 percent of its sum p^2 has left the centre slab by round 25. Fix: a source with S/grip >> 1 (T_d = 1
   or many held counts), the mean subtracted, read against the lattice Green's function.
3. MINOR. P2's "about 2" is 2.49 = the slot form's own 2/(1 - u) at u = c00/rest = 0.2 (B2: at u = 0.02 the laid
   -c00/12 gives 2.05). State the law c^2 = (grip_rest - c00/6)/(rest + c00) and read gamma at small u. Beta: the bare
   form (-g^{00} linear in u) gives beta = 2; beta = 1 follows only if the 00 row's own Mesh grip reads lowered ii
   slots (div((1 - u) grad u) = 0 gives u = 2U + 2U^2), i.e. on finding 1's sign; do not lean on a NOT AGREED
   measurement.
4. MINOR. "A bound clock's active mass is its energy" (P3) is the harmonic spring's K-bar = V-bar: on the act a
   quartic hand sources 2.03 E (d_results; harmonic 1.02). Say harmonic-only; G3's vertex breaks it (4(n - 1)/(n + 2)).
5. MINOR. Conservation is read as board sums (sum p, the act's energy identity), not in the clicks as the owner's rule
   asks, and the books do not close: the 00 gear ends probe 2 with 65 times the matter's starting energy (A1); the
   push is one-way. Mark it bookkeeping; the click reading is G5's.
6. MINOR. The h00 wave "real, at light's speed, sourcing nothing" (P5) is a propagating scalar gravitational wave, a
   departure from GR (polarization bounds) missing from "what stays OPEN"; "carries no energy" is wrong: it carries
   the act's energy and does not gravitate.
7. MINOR. The 0i "root" (P4) is the c = 1 normalization's. With the slots as g^{mu nu} in the lattice's eta the
   strengths are 1/c^4 : 1/c^2 : 1 = 36 : 6 : 1, whole. Check before owing it to G4.

## TERM 13 (term13/TERM13.md)

1. BLOCKING. What probes 2 and 3 measure is not the matter's energy winding the clock (sec. 2 "the zero mode",
   sec. 3). Where the swing is large the mechanism holds exactly as written (e_results E2/E3: E^2 W kept within 5
   percent while W grows 24-fold, <J00> = 2E within 5 percent). But the probes run at strides 0 to 1 from round 500
   on, and there the p-form is not its continuum: a gear's rest is p of about W/2 (the uncentred tooth; on the board
   sum p drifts to 7.6 million = 144 x W/2), a+ = a + floor(p/W) answers any negative push with a whole notch, the
   hand's energy on the 144-site board grows 100-fold by round 1200 and the total push is 60 times the hand's starting
   energy (c_results C2); probe 3's mean of 99,031 is about 125 times what that energy allows; on one site a hand laid
   with p = -1 (2E0 = 0.0003) winds W to 19,010 by round 12,000, and at the end every 00 gear merely coasts on an
   undamped p00 (f_results). Fix: measure the energy argument at strides >> 1 and name the sub-notch regime as the
   act's own; its half-tooth is the 24's (W - 1)/2.
2. BLOCKING. Two signs in one text, and the edge is at a radius. Probes 3 and 5 run the push that raises the grips (xx
   to +250, gamma < 0); probe 4 lays ii = -c00/12. With the lowered grips the form is not linear: the 00 row's Mesh
   grip is (1 - u) grip_rest, so the static exterior obeys div((1 - u) grad u) = 0, u = 1 - sqrt(1 - 4M/r): light's
   edge at r = 4M (u = 1, W = 2 rest, grad c00 diverging), no static solution inside, negative grips and the text's
   own runaway strides (probe 4, -100), which as matter source the 00 slot. "W unbounded only through the mean,
   nowhere at a Node-clock" is shown for a 0.23-notch well and contradicted by the form's own equation for any lump
   with 4M beyond its radius. Fix: one sign; a compact lump driven to u near 1 at its surface, W_lump/W_far over
   rounds.
3. MINOR. The mean's growth is the torus's zero mode with no constraint (the lattice's Jeans swindle; in GR the
   uniform mode is a scale factor, term 9's). In the clicks a uniform W is unobservable (every proper-time ratio
   unchanged); the observable is the grips' mean, a light-length, and under the written sign the Mesh shortens 6-fold
   in beats (A3: grip/rest x39): a contraction. The "lower edge" is the same zero mode under a Lambda-like source,
   with the same sign. Say the edges are statements about the round, and name the clicks' observable.
4. MINOR. Light's edge in the clicks is a throat, not a frozen clock: lengths from light make the Mesh's light-length
   infinite at grip 0 (g_ii = 1/(1 - u) diverges); the text's "a region light cannot cross while the clocks inside
   beat at N^2 = 1/2" should say so, and the EHT shadow is its test.

## SOUND

P1, period^2 proportional to W for the beat and for light (reproduced); M3's rho and pressure algebra; null dust at
993 permille, with 23.1 = 24 cos^2(k/2) the lattice's dispersion; the 00 wave at light's speed; the harmonic virial
(1.019; mine 1.024); the draining mechanism E^2 W where strides are large; the condition of the 24 named first,
measured in both forms and tied to DRAFTED in both texts; P6 honestly OPEN; the route to beta = 1 given gamma = 1
through the 00 row's grip reading the lowered ii slots, once the sign is fixed.

## For Solution24

Add to step 7: "a strength or a sign is measured on the pushed slots, never on laid ones, and every whole-number
measure states the stride it runs at: below one notch the act is not its continuum."
