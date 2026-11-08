"""Data-only preparations. All evolution remains in the reference engine."""
from research.components import BoardSpec, Patch, TensorSpec, place, finalize


def _integer(value, label, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{label} must be an exact integer >= {minimum}')
    return value


def SourceClock(*, delay=0, present=True):
    if type(delay) is not int or delay not in (0, 1):
        raise ValueError('delay must be 0 or 1')
    if type(present) is not bool:
        raise ValueError('present must be Boolean')
    a, b = ((0, 1) if delay == 0 else (-1, 0)) if present else (0, 0)
    return Patch('clock-link-source', {(0, 0, 0, 0): (a, b, 2)},
                 ports={'clock': ((0, 0, 0, 0),)},
                 sources={'initial-clock': ((0, 0, 0, 0),)},
                 evidence_domains=('Counter pair period four; full source also carries echo parity; core native C is silent.',))


def RestingCorridor(*, length):
    length = _integer(length, 'length', 1)
    return Patch('clock-link-corridor',
                 {(x, 0, 0, 0): (0, 0, 4) for x in range(1, length + 1)},
                 ports={'port': ((1, 0, 0, 0),)},
                 evidence_domains=('Initially zero counters; prepared remainder guide, not an inserted moving packet.',))


def EchoBoundary(*, distance):
    distance = _integer(distance, 'distance', 2)
    return Patch('clock-link-boundary',
                 {(distance, 0, 0, 0): (0, 0, 4),
                  (distance + 1, 0, 0, 0): (0, 0, 2)},
                 ports={'endpoint': ((distance, 0, 0, 0),)},
                 evidence_domains=('Ordinary end of the prepared guide, not a runtime mirror rule.',))


def clock_link_parts(*, distance=20, side=389, origin=(4, 4, 4), delay=0,
                     source_present=True, terminated=True, control_extent=None,
                     orientation=0, name_prefix=''):
    """Return immutable placements; no runtime callback or observer feedback.

    The API requires even D>=14 for at least 24 unchanged record transitions.
    side>=extent+3 conservatively keeps exterior recipients distinct. Explicit
    proper rotation transforms both coordinates and channel labels.
    """
    distance = _integer(distance, 'distance', 14)
    side = _integer(side, 'side', 3)
    if distance % 2:
        raise ValueError('The exact family requires even distance')
    if type(terminated) is not bool:
        raise ValueError('terminated must be Boolean')
    if not isinstance(name_prefix, str):
        raise ValueError('name_prefix must be text')
    if terminated:
        if control_extent is not None:
            raise ValueError('control_extent applies only to the long-guide control')
        extent = distance
    else:
        extent = 8 * (distance + 1) + delay + 2 if control_extent is None else control_extent
        extent = _integer(extent, 'control_extent', distance + 1)
    if side < extent + 3:
        raise ValueError('side must be >= guide extent+3 to keep exterior recipients distinct')
    def put(patch, name):
        return place(patch, at=origin, orientation=orientation, name=name_prefix + name)
    parts = [put(SourceClock(delay=delay, present=source_present), 'source')]
    parts.append(put(RestingCorridor(length=distance - 1 if terminated else extent), 'corridor'))
    if terminated:
        parts.append(put(EchoBoundary(distance=distance), 'target'))
    else:
        parts.append(put(Patch('clock-link-target-marker',
                              {(distance, 0, 0, 0): (0, 0, 4)},
                              ports={'endpoint': ((distance, 0, 0, 0),)}), 'target'))
    return tuple(parts)


def assemble_clock_link(**parameters):
    return finalize(BoardSpec(parameters.get('side', 389)), clock_link_parts(**parameters))


def echo_parity(triple):
    """Raw cyclic source bit; undefined for a zero-counter source.

    Delay-one state zero is startup, not evidence of an earlier echo. Interpret
    only after launch calibration. This function never changes board state.
    """
    a, b, r = triple
    return None if a + b == 0 else int((r == 4) == (a + b > 0))


def target_record(triple):
    a, b, _ = triple
    return a*a + b*b
