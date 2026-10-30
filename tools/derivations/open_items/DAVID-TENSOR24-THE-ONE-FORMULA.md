# The node-clock's one formula, exactly: Tensor24's cut 0

David, 2026-10-28, 09:4x UTC, for the Boss. This answers his ask of 06:27 UTC: "Derive it exactly. Give each term's integers, where each carry's remainder goes, and the drive's teeth. I check it bit for bit against the head with a probe." It also answers the owner's word to David of 09:3x UTC: "Why not derive everything now?" It is read on toys-5; the step's code is 526a5666d's, unchanged through 55a3483e1. It is the second hand on law 2 of TENSOR24.md's section 19 (the Boss's formula0.py), with two probes of its own primitives. It adds the metric's half and what the letter says against Einstein (general relativity's six are David's by the plan's protocol). Each claim is marked PROVED, CHECKED or OPEN; the probes and their outputs are in DAVID-TENSOR24-THE-ONE-FORMULA_CHECKS.txt. No src is pushed.

## The integers

- **T = clock.teeth = 6 den Gamma^2 G^2,** always even. K is the file's trace weight, Gamma the node clock, G the mesh unit.
- **X-, X** are the regulator's time gear before and now, at the tick's start. **X+** is its now after its own act. **s = X**, the stretch.
- **W = (T div 2)(X- + X)** at the start. **W+ = (T div 2)(X + X+)**, or W where that is not above 0.
- **For a gear:** a- and a are its notches, r its fine tooth in [0, W), and delta its drive fine tooth. mid(n) = n div 2.
- **The rates** at the start load (a load below 0 is read at 0): p0, and p_i on the meshes. p_s is p0 at the held load: the load plus each held field's weight times its notch.
- **For a train:** g_j = 2 p_i^2 Q_j pinion and D = 12 (rim - pinion) p_s^2 G^2. Q_j is the link's factor from the regulator's tension on its axis.

## The matter's half: every driven train

The driven trains are the hands (the light among them), the offset and the held field.

    W+ (a+ - a) + (r+ - mid(W+)) = W (a - a-) + (r - mid(W)) + s [ sum over j of g_j (m_j - a) - D a + q_P ] + T s q_K

- **CHECKED:** 0 mismatches at every gear and every tick probed, on four worlds (the checks).
- **It is one carry.** a+ = a + floor((P + mid(W+)) / W+), and r+ is the remainder, in [0, W+).
- **PROVED:** the pull m - (2T - S) a equals the sum of g_j (m_j - a) - D a, since the hold is S = 2T - D - the sum of g_j.
- **m_j is the neighbour across spoke j.**
  - For a hand it is turned by the link's pawl, the offset's phase and the skew of the odd and flow gears, with two odd roundings.
  - For the offset and the held field it is the raw neighbour.
  - For the light the turn is the identity, by arithmetic.
- **q_P is the twins' Pauli quotient:** the carry of (sum of g_j)(Phi . sigma psi) at the drive teeth 12 Gamma, its remainder in delta.
- **q_K is the kicks:** the offset's sweep and lead, and the held field's weight times the masses. Each is carried at the key, with its remainder in delta.
- **After the carry,** the light's three gear takes its release, W+ q_R.

## The metric's half: the regulator's seven gears

    a+ = 2a - a- + floor((sum over j of R_j (a_j - a) - D a + r) / T) + floor((N + delta) / T_g),  r+ and delta+ the two remainders

- **The turn** runs at the fixed teeth T. **The drive** runs at its own teeth: T_0 = K rim Gamma^4 T on the time gear, and T_g = K rim Gamma^2 T on the axis gears.
- **The regulator's own gearing:** R_j = 2 p_i^2 Q_j (rim - rim div Gamma) and D = 12 (rim div Gamma) p_s^2 G^2.
- **The sources:**
  - **the forms** Phi = the sum over every driven gear of [u_in u_out + floor(-a F / T)]. Here u is the odd rounding of 2P + 1 over 2 T X, in and out, and F is the pull;
  - **the stress**, over the hands alone, weighted by each pinion p_h: S_aa = the sum of p_h (Delta_a z)^2, and S_0a = the sum of p_h v Delta_a z. Its trace is tau = S_xx + S_yy + S_zz;
  - **the numerators:** N_0 = 4 X p0 (K rim Gamma^2 Phi - p0^2 tau), clamped at plus and minus X T_0; N_a = (3 S_aa - tau) p0^2; and N_(3+a) = S_0a p0^2.
- **After the act** the flows take the recoils of the release, and of the click's lays and unwinds.
- **CHECKED:** 0 mismatching ticks on the toy (20), the bang (10), nature (20) and ga2 (10, trace weight 54).

## What the letter says against Einstein

This is the continuum reading, at the vacuum's rates.

1. **The time gear's source has the wrong sign on the pressure.** It is rim Gamma^2 (2K T_00 - 12 sigma_aa). At K = 6 this reads 12 (rho - 3p) on average over bounded fields, where Einstein's Newtonian source is rho + 3p.
   - So light, whose rho = 3p, does not source the lapse on average here. In Einstein, light gravitates twice as much as dust does.
   - For the convergence, the stress term must enter with the opposite sign: K rim Gamma^2 Phi + p0^2 tau.
   - **OPEN on the lattice:** this is the continuum reading, by the virial theorem. On a uniform light sea the forms read 2 T_00 within the floors (19,110,042 against 19,110,094, the second read's check).
2. **The tensions and flows read the right parts.** The tensions read 36 rim (T_aa - T_bb / 3), the traceless stress, exactly. The flows read -12 rim times the energy's flux.
3. **The two halves are two forms.** The regulator's turn runs at the fixed teeth T, with no factor s and no lapse in its force. The two halves agree only where X is constant: this is cut 6, one path.
4. **On the bang, the lapse is the clamp's.** The clamp on the time gear's drive fires at all 64 node-clocks at every tick probed (CHECKED).
5. **The metric has a mass and lacks a part.** The typed pair's spring D gives it a mass of about 2 / Gamma of its teeth, and the shears are absent.
6. **There is no self-source, and no single kappa.**
   - The regulator's own gradients source nothing.
   - The offset and the held field enter the forms but not the stress.
   - The stress is weighted by the pinion, and the forms are not.
   - The stress's gradient is not turned by the mesh, while the pull's is.

## Where the head departs from the plan's form in the matter's half

1. **The remainders are carried,** in and out: (r - mid(W)) and (r+ - mid(W+)).
2. **J is carried quotients.** q_P enters unscaled, the kicks enter times T, and the sweep comes from the same tick's P.
3. **The release comes after the carry.**
4. **The rest:**
   - the end teeth's fallback;
   - the stopped clocks' restore, and their links' factor 0;
   - the turnover's replacement of the step;
   - the click's writes after it.
5. **Every train's teeth equal T only because every file's pair has rim = den.** Nothing checks it.

## For the Boss

1. **Law 2: CONFIRMED by this second hand,** bit for bit on every world probed (the checks name them), with every term of the matter's half exercised on the twins' world. Sofer's law check is owed, then my sign-off.
2. **For Tensor24's formulas section, each with its cut:**
   - one path: the regulator in the matter's form, with W and s;
   - the time gear's source with Einstein's sign, rho + 3p;
   - the clamp out;
   - the spring 0;
   - the shears back;
   - the self-source;
   - one kappa.
