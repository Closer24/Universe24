"""Bounded exact algebra for translating packet words, not a runtime driver.

Run ``python -m research.staged_blocks.pulse_words``. The fixed finite check
enumerates all 3**8 cumulative words over {-1,0,1}, isolated pairs at distances
1..16, and one two-lane input-sum target. No board simulation or injected
signal experiment is performed.
"""
from itertools import product
import json


def scalar(old, u):
    """Exact Rule3 arithmetic used only to check the mathematical ansatz."""
    a,b,r = old
    ell,s = divmod(2*u+r,6)
    return b,ell-a,s


def profile(cumulative):
    """Rows for a unit-speed +X, positive-X-sign carrier on remainder-zero guide."""
    cumulative = tuple(cumulative)
    if any(type(v) is not int or v not in (-1,0,1) for v in cumulative):
        raise ValueError('The passive-halo ansatz requires cumulative values -1,0,1')
    def A(i):
        return cumulative[i] if 0 <= i < len(cumulative) else 0
    def row(i):
        return A(i)-A(i-1), A(i-1)-A(i-2), 4*(A(i)+A(i-2))
    for i in range(-2,len(cumulative)+3):
        if not 0 <= row(i)[2] < 6:
            raise ValueError(f'Invalid row remainder {row(i)[2]} at index {i}')
    def halo(i, weight):
        return 0,0,2-2*weight*A(i-1)
    return row,halo


def check_translation(cumulative):
    row,halo = profile(cumulative)
    for i in range(-2,len(cumulative)+3):
        u = row(i-1)[1]+row(i+1)[1]
        assert scalar(row(i),u) == row(i-1)
        for w in (-1,1):
            assert scalar(halo(i,w),w*row(i)[1]) == halo(i-1,w)
            assert (2*w*row(i)[1]+halo(i,w)[2])//6 == 0
    return True


def train_cumulative(starts):
    """Initial algebraic sum; profile() must validate it before acceptance."""
    starts = tuple(starts)
    if not starts or any(type(s) is not int or s < 0 for s in starts):
        raise ValueError('Packet starts must be nonnegative integers')
    values = [0]*(max(starts)+2)
    for start in starts:
        values[start] += 1
        values[start+1] += 1
    return values


def bipolar_word(arrivals, stop):
    return [sum((-1 if t == arrival else 0)+(1 if t == arrival+2 else 0)
                for arrival in arrivals) for t in range(stop+1)]


def verify():
    accepted = 0
    for word in product((-1,0,1),repeat=8):
        try:
            check_translation(word)
        except ValueError:
            continue
        accepted += 1
    distances = []
    for distance in range(1,17):
        try:
            check_translation([1]*distance)
            distances.append(distance)
        except ValueError:
            pass
    assert distances == [1,2]
    # These are individually valid same-direction packet trains. They have
    # not been combined into a physical two-lane board by this calculation.
    lane_a, lane_b = (0,4,8), (2,6)
    check_translation(train_cumulative(lane_a))
    check_translation(train_cumulative(lane_b))
    a,b = bipolar_word(lane_a,10),bipolar_word(lane_b,10)
    summed = [x+y for x,y in zip(a,b)]
    assert summed == [-1]+[0]*9+[1]
    state, trace, events = (-1,0,0), [(-1,0,0)], []
    for t,u in enumerate(summed,1):
        old=state
        state=scalar(state,u)
        ell=(2*u+old[2])//6
        if ell and state!=old:
            events.append(t)
        trace.append(state)
    assert all(state==(0,0,4) for state in trace[1:11])
    assert trace[11]==(0,1,0) and events==[1,11]
    return {'classification':'bounded exact arithmetic, no autonomous board experiment',
            'cumulative_words_checked':3**8,'valid_width_eight_words':accepted,
            'isolated_pair_distances_checked':list(range(1,17)),
            'admissible_isolated_pair_distances':distances,
            'two_individual_train_patterns_valid':True,
            'conditional_summed_inputs':summed,'conditional_receiver_trace':trace,
            'conditional_C_updates':events,'conditional_quiet_updates_between_events':9,
            'autonomous_two_lane_mechanism_established':False}


if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True,indent=2))
