# The lapse's source on the lattice: general relativity's first item, checked

David, 2026-10-28, 12:0x UTC, for the Boss (Sofer and Animate copied). This is the first of general relativity's six, mine under section 19's protocol: DAVID-TENSOR24-THE-ONE-FORMULA.md's item 1 against Einstein, "the time gear's source has the wrong sign on the pressure". That page marked it OPEN on the lattice; here it is CHECKED. It is read on engine-5.0-test 987cacf4f, whose src is 8b657aa57's. A helper drafted the probes, and I reran every run: the 16 plane waves, the 600-tick settings in both modes, and the per-mode and gas predictions. Each is identical to the helper's (DAVID-TENSOR24-THE-LAPSE-SIGN_CHECKS.txt). The engine's side is exact integers; the lattice's law of x is compared in floating point. No src is pushed.

## The quantity

1. **The time gear's numerator** is N_0 = 4 X p0 (K rim Gamma^2 Phi - p0^2 tau), where Phi is the forms (the energy) and tau the stress's trace.
2. **Its source over the energy** is 1 - x on the head's sign and 1 + x on the flipped sign, where x = p0^2 tau / (K rim Gamma^2 Phi).
   - The probe recomputes Phi, tau and the numerator per train at every tick. They match the engine's arrays exactly on every tick of every run. CHECKED.
3. **Einstein's Newtonian source is rho + 3p.** Light, with rho = 3p, gravitates twice as much as dust per unit of energy. So the convergence asks for light / dust = 2.

## The lattice's law of x, exact per mode

1. **For a plane wave of a train with rho_h = pinion / rim:** x = rho_h 2 (sum over a of sin^2 k_a) / (K sin^2 omega), where cos omega = rho_h times the mean of cos k_a.
   - The engine's integers follow it to within 3 in a million, on 14 plane waves of light and dust: along an axis, a face diagonal and the body diagonal, on boards of 4 to 16. CHECKED.
2. **For light at K = 6,** 1 - x = Var(cos k_a) / (1 - mean^2), which is never below 0. PROVED from 1.
   - **Along an axis,** 1 - x = 2 (1 - cos k) / (5 + cos k), about k^2 / 6. So 1 - x goes to 0 at long waves. It reads 0.400, 0.260, 0.182, 0.103, 0.066, 0.046 and 0.026 on boards of 4, 5, 6, 8, 10, 12 and 16. CHECKED.
   - **Along the body diagonal,** 1 - x = 0 exactly, at any wavelength. CHECKED at 5 and 8.
3. **For dust,** x is small, since rho_h is near 0.16: 1 - x is 0.950 at 5 and 0.972 at 8, and exactly 1 for a sea at rest (k = 0).

## The verdict

1. **At long waves the head's sign gives light / dust -> 0, and the flipped sign gives 2,** Einstein's. CHECKED, in the limit of the lattice's own law of x.
2. **On the 5^3 board the lattice's dispersion holds light short of rho = 3p.** Packets at |k| of about 2 pi / 5 to 4 pi / 5 read x of 0.69 to 0.79. Over five light and six dust settings, light / dust is 0.21 to 0.36 on the head's sign and 1.55 to 1.79 flipped (the regulator held at the vacuum, 600 ticks). The per-mode law explains the packets to within 1 percent.
   - A lattice gas with equal forms per mode over the whole zone reads 0.37 against 1.63.
   - A long-wave gas with |k| below pi / 4 reads 0.024 against 1.976.
3. **So the item stands as found:** the pressure enters with the wrong sign. The fix is K rim Gamma^2 Phi + p0^2 tau, and its cut is in the formulas section with the others of the six.

## What the head's own run shows, and why the probe holds the regulator

1. **The vacuum is held by the turnover, not by the step.** In an empty world every node-clock's time gear falls from 1000 to 998 in the carry, under its own spring, and the turnover restores it to 1000. So all 125 node-clocks turn over at every tick. CHECKED over 4 ticks.
   - With a packet laid, the turnover fires at about 40 percent of a weak light packet's node-clocks each tick, and at 92 to 100 percent of a dust packet's.
   - At the turned node-clocks the hands are exchanged and mirrored instead of stepped. The light's kinetic forms average below 0, and the dust packet nearly freezes.
   - So the head's run is not an on-shell average. The probe's test mode holds the regulator at the vacuum (its act skipped, its gears reset each tick). It reads the source exactly as the engine reads it, and it gives the continuum's virial means.
   - In the head's run, light / dust is 0.33 to 0.46 on the head's sign and 1.47 to 1.67 flipped.
2. **The time gear's clamp never fires at the head's quanta,** on either sign: at most 0.023 of the hold for light and 0.004 for dust.
3. **This is cut 0's metric mass at work.** The typed pair's spring D (about 2 / Gamma of the teeth) is the fall of 2 a tick, so flat space is not a solution of the step. Cut 0's cut "the spring 0" makes the vacuum stand by itself, as it does in Einstein. Draft B's floor at the full rate (X_f = Gamma) is the place to read the two together.

## For the Boss

1. **General relativity's first item: CHECKED.** At long waves the head's sign gives light no source, and the flipped sign gives Einstein's factor 2. The cut: the stress term with the plus sign.
2. **Named for the plan's section 18:** the lattice's dispersion lowers light's 3p / rho at short waves. A 5^3 board holds light short of Einstein by its own law of x. This is a property of the lattice, not of the sign.
3. **For draft B and the vacuum:** an empty world turns over at all of its node-clocks every tick, under the time gear's spring. The spring 0 is the cut.
4. **Next of mine:** the rest of the six (the shears, the trace's source, the self-source, one kappa, the metric's mass), then Einstein from the clicks.
