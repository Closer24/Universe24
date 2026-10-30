# The push as built (load.pushing, 9868ae570) and what it is as physics

## As built (per unit strength f, S = scale = Spokes x senses = 12)
- 00 slot: +144 f (si^2 + so^2) + 12 f |Da|^2   (whole = S^2 f on the momenta, half = S f on the differences)
- ii slot: -12 f (si^2 + so^2) - f (D_i a)^2 + f sum_{j != i} (D_j a)^2   (less, back, other)
- jk slot: -2 f D_j a D_k a (both orders)
- 0i slot: -2 f (si + so) D_i a (four terms)
This is +S J00 and -J_ii, -J_jk, -J_0i with J = 2T - eta T, T00 = S(si^2+so^2), T_ij = D_i a D_j a, T_0i = (si+so) D_i a.
The matter's rows hold J1 = 0 in the example universe (no vertex, no spring): the matter is a FREE MASSLESS scalar with two parts.

## The identification
T = v (x) v with v = (sqrt(S) sigma, D a) (S = 12 the unit conversion making a null pulse traceless: text's P5, 17 permille).
Then J = 2 v v - eta (v.v) = 2 T^can where T^can = v v - (1/2) eta (v.v) is the conserved stress tensor of the free scalar.
The text itself says: "this J is twice the canonical massless scalar's stress tensor". That is the problem, not a reassurance:

## GR's first-order law for the METRIC (what the slots are: teeth = -g^00, grips = g^ii) sourced by a scalar
box h_{mu nu} = -16 pi G (T^can_{mu nu} - (1/2) eta_{mu nu} tr T^can).  For the free scalar tr T^can = -v.v, so
T^can - (1/2) eta tr T^can = v v - (1/2) eta (v.v) + (1/2) eta (v.v) = v_mu v_nu  EXACTLY.
So GR pushes the metric slots with v (x) v. The engine pushes them with 2 v v - eta (v.v).
The extra term, -eta (v.v) = +2 eta L_kin, is a coupling of every diagonal slot to the matter's kinetic Lagrangian density,
which GR cancels (the sqrt(-g) L term against the trace reversal). With a potential V (term 6, G3) GR's source is v v + eta V:
the potential survives, the kinetic Lagrangian never does.
NOTE: docs/ARCHITECTURE.md's term 5 row says "each square slot pushed by its part of 2T + 2 eta V" = 2 (v v + eta V) = GR's form.
The built and derived form is 2T - eta T. The head's two documents disagree with each other on the form of term 5.

## What the extra term does on the text's own cases (per unit, S = 12, centred differences)
| state | v.v | engine J00 | engine J_ii | GR source 00 | GR source ii |
| gliding hand ("dust"), sigma, no gradient | -S sigma^2 | S sigma^2 (x2 for si,so) | S sigma^2 (isotropic) | S sigma^2 | 0 |
| static tent along z, D_z a = 2g | +4g^2 | 4 g^2 (text: 48 g^2 = 12 x 4 g^2) | zz: 4g^2; xx = yy: -4g^2 | 0 | zz: 4g^2; xx = yy: 0 |
| null pulse along x (S sigma^2 = (D_x a)^2) | 0 | 2 S sigma^2 | xx: 2 S sigma^2; yy = zz: 0 | 2 S sigma^2 (same up to the 2) | same |
So: for NULL matter the engine's push is GR's (up to the strength). For the gliding hand the ii push IS the extra term:
the measured "-12 ii / c00 = 999 permille, gamma = 1 on dust" is the -eta(v.v) term, not GR's gamma.
In GR a uniform source with pressure p gives h_ii / h_00 = (rho - p)/(rho + 3p); the gliding hand's own conserved stress has
p = rho (stiff: T^can_00 = T^can_ii = (1/2) W v^2), so GR gives h_ii = 0 for it. The engine gives h_ii = h_00.
For the static tent GR gives NO 00 push (Tolman: rho + sum p = 0 for a pure gradient), the engine pushes 00 by 48 g^2.

## What the matter is
A free massless scalar: gliding = stiff (w = 1); standing waves = radiation (w = 1/3) in time-mean; a static gradient = tension.
It is NEVER dust (w = 0). The engine as shipped has no slow source. The "dust" of G1/G3 is dust only in the tensor v v, which
is not the matter's stress tensor (d_mu (v^mu v^nu) = (1/2) d^nu (v.v) != 0: not conserved).

## The joint-action view (what the act's own reads imply)
The matter's equation d_t (W d_t a) = sum grip (nb - own) comes from S_m = sum (1/2) W v^2 - (1/2) sum_Mesh grip (Delta a)^2,
W = rest + c00, grip = grip_rest + ii(x) + ii(x+1). Its dependence on the slots: dS_m/dc00 = +(1/2) v^2 per row reading it;
dS_m/d ii(x) = -(1/2) [ (Delta_i a)^2 at the two Meshes of x ] per row. That is v (x) v again, component by component, with
NO eta L term and NO free strength: the coefficients are the reads' factors (1). A push of this form with the slots' own free
dynamics is a conservative system (one energy, matter + slots). The built J is not: see 02_books.
