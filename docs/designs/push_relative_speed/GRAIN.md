# doppler-v1: the grain form for the star worlds, and the oblique weight (read-only, the mathematician, 2026-09-20)

On the Boss's two questions after the physics review of doppler-v1
([record 127](../../LOG_2026-09-20.md): the rule as built is the form of
[FORM.md section 6](FORM.md), the pair `(|N_d D_a - T_d s p_a|, N_d D_a)`
per (direction, column) floored off the reader's clock; the registered
star worlds of series G2 pass the load check and refuse at the first
weighted push by about 26 bits). Every integer is from `grain_map.py`
beside this file (`grain_map.out`), on the numbers of
`examples/events/hubble_stars/gravity_none.json` (`claude/series-g2-stars`
at 5322dc4): a star of amount 4096 holding 4 194 304 of `mass` (M =
4 198 400 = K), width S = 2^20, 64 units of mass per direction per
interval, momenta 9.7 x 10^12 to 1.14 x 10^14 on one axis. No run.

## 1. The grain form, exact and bounded

**Why the pair cannot fit a star.** `Q S M = 2^48`, so `D_a` is 2^48 and
the pair's numerator `32 D_a - 55 s p_a` is 2^53; one mass row of amount
64 gives `|V| = 2^12`, the gravity column `|E n| = M = 2^22`, and the
product `|V E n| x |num|` is **2^87** at every declared momentum
(`grain_map.out` 1: 87.0 to 86.5 bits), against 2^62. No width helps: the
pair's numerator scales with `D_a = Q S M + |p|`, and at S = 1 it is still
`2^28 x 32` on `|V E n| = 2^34`. The exact pair is the right number and
the wrong place to put it.

**The form.** Quantise the reader's speed on each axis once per interval
from its own record, and put the weight on the ARRIVALS' FLOW per
direction, off the clock, before the columns:

    w_a  = (G x |p_a|) // D_a                         (per axis; 0 <= w_a < G; D_a = Q S M + |p_a|)
    f_d  = (G N_d - T_d s' w_a, G N_d)                 (per direction d, on the axis a of u_{d,a}; s' = sign(u_{d,a}) sign(p_a))
    V'_d = sign(V_d) x by_clock(age_A, |V_d| x |G N_d - T_d s' w_a|, G N_d)   (the row's label flow, weighted, per component)
    push = the columns as today on sum_d V'_d          (E n, D d, by_clock per column: untouched)

with **G = 2^12** (the grain 1 / 4096 Links per interval), a constant of
the law beside Q = 64, not a world key. Section 2 replaces `f_d` by the
flux form for fan directions; the bookkeeping is the same.

| Property | Statement |
| --- | --- |
| **bounds** | `|G N_d - T_d s' w_a| <= G (N_d + T_d) <= 2^12 x 16 384 = 2^26` on any direction of the table; `|V_d| x num <= amount x Q x 2^26 = amount x 2^32`: fits for an amount up to 2^30 per direction per interval, that is always (the label bound is tighter); then today's push on the weighted flow, 2^34 on the star (`grain_map.out` 1: the flow product 28.0 to 28.9 bits, the push as today). **The star worlds fit as registered**, no re-scaling. |
| **the remainder** | two, both bounded and stated: (i) the speed's, `(G |p_a|) mod D_a`, discarded each interval: the quantised `w_a / G` is below `|p_a| / D_a` by less than `1 / G = 2.4 x 10^-4` Links per interval, so the weight is biased toward 1 by less than `T_d / (G N_d)` = 4.2 x 10^-4 of the rate on a heading (a receding body reads at most that much too much, an approaching one too little); on the stars the bias measured 7 x 10^-5 to 1.9 x 10^-4 in v; systematic, a declared grain like S and Q, no owner needed because nothing accumulates; (ii) the flow's floor, `(|V_d| x num) mod (G N_d)`, read off the reader's clock by `by_clock`: exact on average, below one label unit per direction per interval, the same kind of remainder as every column's. |
| **bit-identity with the pair of section 6** | at p_a = 0 both are exactly 1 (w = 0, the pair `(G N_d, G N_d)`, the division exact): every fixed body and every free body at rest reads today's integers bit for bit, as the built form does. For p_a not 0 the two differ by the speed's grain (below 1 / G) and by where the floor sits (the flow against the column): never bit-identical in general, equal only where `G p_a / D_a` is whole. |
| **load-time bound** | none new: the weighted flow is at most `(1 + T_d / N_d)` times the flow (4.75 on a heading), so the static budget of the columns (today's, per reader, family and column) is taken on the largest release flow times that factor per direction; the pair's `(N + T) x D` budget goes. |
| **the number of floors** | one on the flow per (direction, component) and one per column as today: the reader's clock reads both; a fan of 290 directions costs 290 x 3 small products per family per interval, the host's, not a new bound. |

**Recommendation for the owner:** the grain form REPLACES the pair
(the pair fits no star and no body of content above 2^19 with rows of
amount 1, and fits the register's deuteron only at rest); one key
`doppler: true`, G a constant of the law beside Q, the identity
`doppler-v1` unchanged; the second value `"grain"` would keep a form that
can never run and is not worth a key.

## 2. The oblique weight: the flux form is the meeting rate; the per-axis form is exact on headings only

**Physically.** A body takes a message at the rate at which the message's
line crosses it: the flux of a stream of velocity `c_d` through a body of
velocity `v` is proportional to the relative velocity's component ALONG
the stream, `|c_d| - v . c_d / |c_d|`, so the factor on the arrivals' rate
is `1 - (v . c_d) / |c_d|^2`: a transverse motion changes nothing (the
body leaves one line of the fan and enters another), a co-moving one
takes less, a head-on one more. On the lattice the message's velocity on
the direction `D = (a, b, c)` is `(Q / T_d) D` per axis (the Bresenham
line's pace: `a / S_1` of `S_1 Q / T_d` Links per interval on x, and so on),
`|c_d|^2 = (Q / T_d)^2 |D|^2` (within 1.35 % of 1 / 3), and the body's
velocity is `(p_a / D_a)` per axis. So the exact factor is **one scalar per
(direction, body)**,

    f_d = 1 - (T_d / (Q |D|^2)) x sum_a (p_a / D_a) D_a   (D_a the divisor per axis; the same letter twice is the design's, kept here)

applied to the row's whole label vector. The per-axis form as built,
`1 - v_a / c_{d,a} = 1 - v_a T_d / (Q a)`, equals it exactly on a heading
(`|D|^2 = a^2`, one nonzero component) and on every other direction
overstates the Doppler term by the factor `|D|^2 / a^2` on the axis term
(`grain_map.out` 3): x 2 on a face diagonal (the review's 0.1875 against
0.594 at v = 1/3, reproduced), x 3 on a cube diagonal, x 5 on (1, 2, 0),
x 14 on (1, 3, 2) for a body moving on x, and it goes NEGATIVE on the
slanted directions at the stars' own speed (-0.11 on (1, 2, 0), -0.87 on
(1, 3, 2) at v = 0.289, where the flux form reads 0.78 and 0.87): the
built absolute value then reads a message coming at 8 degrees from the
body's motion as if the body outran it. It is not a different bookkeeping
of the same count over a period: the per-axis factor is a wrong rate on
every interval, and no period sum corrects a factor.

**The exact form in the grain's integers**, one scalar per (row
direction, body):

    f_d = (G Q |D|^2 - T_d x sum_a s_a w_a D_a,  G Q |D|^2)     (w_a = G |p_a| // D_a, s_a = sign(p_a), D_a here the vector's component)

the numerator at most `G (Q |D|^2 + T_d S_1) = 2^33.6` on the table's
worst direction, so `|V_d| x num <= amount x Q x 2^33.6`: fits for an
amount up to 2^22 per direction per interval (the star's rows are 64), the
floor and the rest as in section 1; on a heading it is section 1's pair
exactly (`|D|^2 = a = 1`, one term), so every heading reading of the
built form's tests stands; a transverse motion gives exactly 1 (the sum
is 0). **Yes, the built weight must change before any fan world runs
under the key**: the G2 stars read the 290-direction fan, and on it the
per-axis form is wrong by up to the ratio above and negative on the
slanted directions. The change is one scalar per (direction, body) in
place of one per (direction, axis), a smaller rule than the built one
(no per-axis case, no "only on an axis where the reader moves" rule,
which the flux form makes unnecessary: a zero component simply
contributes no term).

## 3. The four lines

1. The grain form: `w_a = G |p_a| // D_a` with G = 2^12 a constant of the
   law, the weight on the arrivals' flow per direction off the clock
   before the columns; the star worlds fit as registered (2^29 then 2^34
   against the pair's 2^87); bit-identical at p = 0, never in general
   otherwise; the speed's remainder below 1 / G, discarded and stated,
   the flow's read off the clock; no new load bound; REPLACE the pair.
2. The oblique weight: the meeting rate is the flux, `1 - (v . c_d) /
   |c_d|^2`, one scalar per (direction, body) on the whole label vector;
   the per-axis form is exact on headings and wrong by `|D|^2 / a^2` per
   term on every fan direction, negative on slanted ones at the stars'
   speed; it must change before any fan world runs under the key.
3. Exact integers for it: `(G Q |D|^2 - T_d sum_a s_a w_a D_a, G Q |D|^2)`,
   the numerator within 2^33.6, the products within the ceiling for an
   amount up to 2^22 per direction.
4. Nothing registered, no run; the owner decides G as a width of the law
   and the replacement of the pair.
