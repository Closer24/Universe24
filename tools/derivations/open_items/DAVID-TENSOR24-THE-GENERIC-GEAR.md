# The generic gear: G1 in clocks, with the checks for each stage

David, 2026-10-29, 15:4x UTC, under decision 40 (the owner's words to the Boss of 15:0x UTC: "Start. Go with the recommendations if there are no fakes in them. Finish a generic engine."; tensor24-review 36087c95d), and under the owner's words to David:

- 15:0x UTC (in Hebrew; in translation): "No numbers in the code. No floors or bounds, no if. Everything in the universe file and the world: the numbers and the coupling family. Make sure the code does not know what the families are, and the doubled Node-clock performs a simple step."
- 15:1x UTC: "It is entirely tensor code, algebraic. In all places."

The Boss's asks of 15:22 (comment 6500777188) are answered here: N1, N3, the form of (a)'s toy and the exact read of (e).

Probes, each with its output beside it:
- derive/david_open/gear/: e1_ruler_read.py on integers; n1_slicing.py exact, with one float check named; n3_slots.py exact.
- derive/david_open/couplings/: norms.py on integers; virial.py in floats.

Only the Boss writes engine code (decision 40). This page is a specification and its checks, nothing more.

## 1. What G1 builds, and what waits

- **G1 builds (c) and (e):**
  - one gear type for every row, with the lapse an ordinary family (section 2);
  - the ruler's read, exact and computed (section 3);
  - the doubled Node-clock's one step (section 4).
- **G3 builds (d):** one drive, with the coupling family's leg (N4; section 8).
- **What waits:** G2 and later wait on N1 to N5 (sections 5 and 6). (a) waits on its toy (section 7).

## 2. One gear for every row, (c)

- **The act as built has two forms** (load.geared):
  - the file's rows read the ruler, at W = W+ = 2T and s = 2;
  - the time gear stands on its own teeth, at W = W+ = T and s = 1. Its pinion is den - den div Gamma, its kick is T, and its drive's teeth are (T div 2) key. It is found by position (trains[-1]) and typed as 'A1'.
- **The one form:**
  - every row has W = Z_b + Z_n and W+ = Z_n + Z_+, the ruler's teeth read at the counts the files name;
  - s = 2, which counts the teeth summed in W, so s / W = 1 / T at rest on every row;
  - the spring is its factor times Y_n^2.
- **The time gear is then a train of the file:** its kind and its part of the metric are named there, and its pinion is den.
- **Its notch comes from the vertex C[A1; A1, A1] with a steady leg** (my 6497717375, item 3), at G3. Until then its spring stays a named breach (N4, places 5 and 6).
- **The check at G1:**
  - the uniformity test (Animate's 6500345684): the record of a permuted file equals the permuted record, and the time gear laid as an ordinary family equals the loader's row;
  - no index by position, and no kind typed;
  - the 24-equivariance test.

## 3. The ruler's read, exact and computed, (e)

- **The walk the loader makes once is one carry per load.** Up one load:

      X Gamma + r = X+ (Gamma - 1) + r+

  The read at a load is X rounded at the resolution Gamma^2 (ruler_of: the hill and its tooth). Taken at the tick instead of once into a table, the same carry is the ruler's own dial (X, r):
  - **up** one load where the time gear's count rises: carry(X Gamma + r, Gamma - 1);
  - **down** where it falls: carry(X (Gamma - 1) + r, Gamma);
  - **held** where it stays: carry(X (Gamma - 1) + r, Gamma - 1), which is (X, r) itself.
- **In the closed list:** the step at the stride q is one carry, with the multiplier Gamma - 1 + u and the teeth Gamma - 1 + d.
  - u and d are the bits of q = +1 and q = -1: u = (q q + q) div 2 and d = (q q - q) div 2, each exact. The 2 is the mirror's order, as in home.
  - No branch, no table, no comparison.
  - It equals the three carries at every state of the chain and every stride -1, 0, +1 (e1, 6: 3,000 cases at Gamma 7 and 1,000).
- **e1 shows, on integers:**
  1. walked up from the seed's start, the dial equals the loader's table at all 3,793 loads (Gamma 1,000);
  2. it runs on past the table's last entry, 18,965 loads up to Y = 173,986,597,162, so nothing stops the walk: no table and no cap;
  3. over 20,000 ticks at strides -1, 0 and +1 at or above the start, the dial at each load is the chain's, and the walk run back returns every state exactly (Gamma 7 and 1,000).
- **Two limits.** Each is a requirement the files' checker reports by name, and no act clamps it (line 106).
  - **(i) The stride.** One carry moves one notch, so the time gear's stride must be at most one notch per tick. A two-notch carry at (Gamma + 2) / Gamma leaves the chain: X 1,002,000,000 against the chain's 1,002,003,004 (e1, 5). A loop of carries is refused, and so is a power.
  - **(ii) The start.** Below the chain's start the dial is no bijection. The first descent's remainder can be Gamma - 1, one past the next descent's range: at Gamma 7, (344, 0) goes down to (294, 6) and to (252, 6), and up again to (295, 0), not (294, 6) (e1, 4).
    - So the chain's start is a variable of the world file: the least load the run may reach, laid at or below the seed's count. The checker reports a run that passes it, and no act clamps it (line 106).
    - That the course's bounce stays above the load 0 is not derived. It is Sofer's (ii), with the owner's yes and the Boss consulted (6501286332): derive that the dynamics never take the count below 0.
    - On 7b's law the exact first integral turned the swing below the load 0 (q4: U -4.57 for matter, -5.30 for light), so it is to derive on the act under the new law.
- **A correction to my 6500079593, item 2.** "Stepped with the load and carried with its remainder" holds on the chain, at or above the start and at a stride of at most one notch per tick. The two limits are named here.
- **The teeth and the spring follow from Y:** Z = T Y^4 div Gamma^4 and the factor times Y^2, each a product and one carry.

## 4. The doubled Node-clock's one step

- **The mirror T:** a and b exchange, and every remainder flips, r -> w - 1 - r. W and W+ exchange with them, since the ruler's read at the before and after counts swaps.
- **One function:** backward = T tick T, and untick goes.
- **The test:** T tick T tick = identity on random states, with the ruler's dial in the state; the rewind check reads the log.

## 5. The sources: the books' tensor in ten slots (N3, confirmed)

- **Einstein's law in d + 1 dimensions,** R = kappa (T - eta T / (d - 1)), taken d - 1 times: every slot is pushed by its own component of (d - 1) T - eta T.
  - The coefficients are whole numbers, the same for every kind.
  - The 2 at d = 3 is d - 1, the board's axes less one, so no number is typed.
- **n3 shows, exactly:**
  1. **A fluid at rest, for every d from 1 to 5:** the 00 slot gets (d - 2) rho + d p, and each diagonal slot rho - p, so the diagonal's d slots get d (rho - p) in all. At d = 3 these are rho + 3p and 3 (rho - p).
  2. **One gear's books** (rate v, differences g_i, spring V; K = v^2 / 2, G = |g|^2 / 2): 00 = 4K - 2V, ii = 2 g_i^2 + 2V, 0i = -2 v g_i, and ij = 2 g_i g_j. These are products of the gear's own rates and differences, so they are rows of the one plan.
  3. The diagonal in all is 3 (rho - p) of the same books, and the 00 slot is rho + 3p.
- **No division:** the ruler, the A1 of the diagonal, is the sum of the three diagonal slots, not their mean, so nothing divides by 3.
- **The coupling's energy** is its own contraction, counted once (C phi phi phi). It is not phi . J / 3 (Euler's weight would divide by the legs' count).
- **The force form is not the books** (virial, floats): over one beat of a gear with a cubic coupling it gives +0.330195 against the books' +0.353626. The difference, -0.023431, is 2 <V_c> = -0.023432, so binding would gravitate wrongly.

## 6. The slicing (N1): the law's own, w = 1/2

- **Both lines check** (n1, exact at every w = k/12):
  - the course gives f = w / (1 - w);
  - the static field gives gamma = w / (3w - 1).
  - The float row, the divergence of (-g)^w g^ij about a point mass taken from the metric itself, is 0 at the line's gamma to the differences' size. At gamma = 1 it is of order 1 unless w = 1/2.
- **The free count's weight is 1/2.** Each board count as a free clock obeys Box_g x = (-g)^(-1/2) d_mu ((-g)^(1/2) g^(mu nu)) = 0. That is the measure's own weight, the four-volume sqrt(-g) = N a^3 = (Y / Gamma)^2.
  - Any other w is a typed weight.
  - f = 1/3 needs w = 1/4, which gives gamma = -1. Cassini holds gamma - 1 = (2.1 +- 2.3) x 10^-5 (Bertotti, Iess and Tortora, 2003).
- **Under (c),** every slot in wave form, pushed by its own source (section 5), is Einstein's law reduced in the free count's coordinates.
  - The tie, the count's residual, is the constraint the books' conservation keeps: where T is conserved, the residual obeys a free wave law of its own. So it is measured and not imposed.
  - So the course's slicing is the law's own: w = 1/2, f = 1, N ~ a^3.
- **Withdrawn:** my "the tie's f to be chosen by the act's run" (6499764995, item 3), as N1 strikes it.
- **The cost stays, named.** Under f = 1 the rate spans (1 + z)^3 over the course, and under (f) the range comes from den.
  - The light elements' 1 + z of about 10^9 asks den of at least 10^27.
  - The file's den, 1.5 x 10^16, spans 1 + z of about 2.5 x 10^5.

## 7. The form of (a)'s toy: the gears' own books at lambda = 1/Gamma

- **The form:** one A1 gear phi on the act's integer step, pushed by its own books through C[A1; A1, A1] at the notch's strength lambda = 1/Gamma, in three variants.
  - **(N), the books' Lagrangian density** (rates squared less differences squared): phi'' - Laplacian phi = lambda (phi'^2 - |grad phi|^2).
    - u = e^(-lambda phi) is then exactly a free wave, so phi stays bounded for every amplitude with u > 0.
    - This is the null form (Klainerman, 1986), and it is the form that must hold.
  - **(L), the 00 slot's own share alone,** 2 phi'^2 (the 4K of section 5): not a null form. This is John's case (1981): it grows without bound after a time of order exp(c / (lambda A)) for an amplitude A.
  - **(R), the diagonal slots' own share alone,** 2 |grad phi|^2 summed: not a null form either.
- **The ten slots together,** with the trace reversal, hold Einstein's weak null form in the free count's coordinates (Lindblad and Rodnianski, 2005), so small data stay bounded.
- **The conformal mode's sign:** general relativity's action weighs the conformal part's rates with the opposite sign. So the toy runs (N) at both signs (u = e^(-+lambda phi)), each bounded while u > 0.
- **The test** that gates (a): (N) on the act at lambda = 1/Gamma, read against the free wave's u, with (L) and (R) as the controls whose growth is read. It is the Boss's to build, as the architect's gate says.

## 8. The tables: one strength at G3, and the integrality point

- **The norms** (norms, on integers):
  - A1 and A2, T1 and T2 are orthogonal on the 24 in the act's basis. E is not: its basis (e1 - e2, e2 - e3) has the Gram matrix [[2, -1], [-1, 2]].
  - The 43 tables' scalar norms are 1, 2, 3 and 10. Every table through E whose norm the A1 leg does not fix has none.
- **One Schur lambda for all 43 is no integer rule:** k_1^2 = 2 k_2^2 has no solution in whole numbers. So "one strength" cannot be each table scaled to one lambda.
- **The strength comes from one invariant that holds all three legs at once:** the coupling family's vertex, the law owed at G3, under (d).
- **E's whole basis is the diagonal of section 5:** the three axes' stretches, A1 + E, which the 24 permute as whole numbers. So the metric's E needs no basis from the act's kinds.

## 9. The owner's words, item by item

- **No number in the code:** the 2 of the slots is d - 1, and the 2 of u and d is the mirror's order, as in home. Every other number is the files' (den, full_rate, key).
- **No floor, bound or if:** the ruler's two limits are requirements, reported by the checker and held by no act. The sign test leaves the act: Sofer's rule CHOOSE refuses a call of choose or nonneg there (scribe-5 0bcb22ac4), with the standing ones named until G1.
- **The code knows no family:** the time gear is a train of the file (section 2).
- **The doubled Node-clock's simple step:** T tick T (section 4).
- **Entirely tensor and algebraic:** each item above is in the closed list: products, sums and one carry, over the contraction.

## 10. The checks I read at each stage

| stage | item | the check |
| --- | --- | --- |
| G0 | the gates | the uniformity test, the 24-equivariance test, no row apart, DECLARE; the sign test's calls refused in the act |
| G1 | (c) one gear type | the uniformity test with the time gear as a file train; no trains[-1] and no typed kind |
| G1 | (e) the ruler's read | e1's five checks on the act: the read equals the table wherever the table reaches; no cap; the rewind exact with the dial in the state; the stride and the start reported |
| G1 | the one step | T tick T tick = identity on random states |
| G2 | N1 | in the course run, the tie's residual stays at the resolution and N goes as a^3 |
| G2 | N3 | each slot's source is the books' row of section 5; the force form is gone |
| G2 | N2 | a push that reads the stride runs back (the first-order form) |
| G3 | (d) | one drive with the coupling family's leg; the vertex pushes all three legs and the books close; one strength by the vertex's law (section 8) |
| G4 | E | the diagonal block whole under the 24; the shears' waves at light's speed with two polarizations |
| before (a) | the toy | section 7's (N) bounded at lambda = 1/Gamma; (L) and (R) read |

## 11. What does not follow

- **Not built:** that the act runs any of this. Each check is read on the Boss's code at its stage.
- **(i), the stride:** that the time gear's stride stays at one notch per tick near the bang.
- **(ii), the floor:** that the dynamics never take the load below 0 (Sofer's (ii), to derive; on 7b's law they did).
- **The coupling family's vertex law,** and so one strength for the tables (G3).
- **That den can reach 10^27 by the files alone** (a demand, named).
