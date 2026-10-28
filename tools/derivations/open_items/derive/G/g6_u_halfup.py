"""G6 (drafter G): the impulse's u = rounded(2 p + 1, 2 t X) (tick.py:231-232) is the half-up rounding of p
over t X, u = (p + t X div 2) div (t X), for every integer p when t X is even; and the head's driven carry
(p + mid W) div W (tick.py:266) is the same rounding at W. A property test against the head's own functions
(core/rates.rounded and core/acts.carry, pure integer functions; no clock is built), python -I.
The reflection about -1/2: u(-1 - p) = -u(p) at every p, and u(-p) = -u(p) fails exactly at the ties
p = t X / 2 mod t X."""
import random
import sys

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
from event_universe.core import acts, rates  # noqa: E402

rng = random.Random(28)
cases = ok_u = ok_carry = ok_refl = ties = odd_fail_at_ties = odd_fail_elsewhere = 0
t = 23290147981996629504000000  # the toy calibre's teeth, 6 rim Gamma^2 G^2
for k in range(100000):
    X = rng.choice([1000, 1006, 1998, 4991, 4992, rng.randint(1, 10 ** 7)])
    tX = t * X if k % 2 else 2 * rng.randint(1, 10 ** 6)  # even always: t is even
    if k % 5 == 0:
        p = (rng.randint(-10 ** 6, 10 ** 6) * 2 + 1) * (tX // 2)  # an exact tie
    else:
        p = rng.randint(-10 ** 40, 10 ** 40) if k % 3 else rng.randint(-3 * tX, 3 * tX)
    u = int(rates.rounded(2 * p + 1, 2 * tX))
    half_up = (p + tX // 2) // tX
    carried = int(acts.carry(p, tX, acts.mid(tX))[0])
    u_refl = int(rates.rounded(2 * (-1 - p) + 1, 2 * tX))
    u_neg = int(rates.rounded(2 * (-p) + 1, 2 * tX))
    tie = (p - tX // 2) % tX == 0
    cases += 1
    ok_u += u == half_up
    ok_carry += carried == half_up
    ok_refl += u_refl == -u
    ties += tie
    odd_fail_at_ties += tie and u_neg != -u
    odd_fail_elsewhere += (not tie) and u_neg != -u
print(f'{cases} cases ({ties} exact ties): u = (p + tX div 2) div tX at {ok_u}; the driven carry the same at'
      f' {ok_carry}; u(-1 - p) = -u(p) at {ok_refl}; u(-p) = -u(p) fails at {odd_fail_at_ties} of the {ties} ties'
      f' and at {odd_fail_elsewhere} of the {cases - ties} other cases')
