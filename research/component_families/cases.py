"""Published initial preparations, reconstructed exclusively through components."""
from research.components import (BoardSpec, GuideSegment, LocalizedSixClock, CompactFiveClock,
                                 CooperativeClockPair, EvenPacketSource, place, finalize,
                                 assemble_scatterer, assemble_remainder_register)


def prepare(case):
    side, kind, params = case['side'], case['kind'], case['preparation']
    if kind in ('register', 'repeat'):
        return assemble_remainder_register(side=side, **params)
    if kind == 'scatterer':
        return assemble_scatterer(side=side, **params)
    if kind == 'packet':
        origin = tuple(case['origin'])
        return finalize(BoardSpec(side), [
            place(GuideSegment(start=0, stop=side - 1,
                               sockets=tuple(range(origin[0], origin[0] + 4)),
                               remainder_pair=(0, 0)), at=(0, *origin[1:]), name='guide'),
            place(EvenPacketSource(**params), at=origin, name='packet')])
    factories = {'six': LocalizedSixClock, 'five': CompactFiveClock,
                 'cooperative': CooperativeClockPair}
    if kind not in factories:
        raise ValueError('Unknown published family preparation')
    return finalize(BoardSpec(side), [place(factories[kind](**params), at=case['origin'], name='body')])
