"""Initial-only guide/scatterer/register assemblies using the strict composer."""
from .spec import BoardSpec, place
from .compose import finalize
from .recipes import GuideSegment
from .clocks import LocalizedSixClock, _positive_tensor, _boolean, _integer
from .packets import EvenPacketSource, RemainderTarget, RegisterWriter, SourceOverlapRegister


def _offset(value, label):
    value = tuple(value)
    if len(value) != 3 or any(type(x) is not int for x in value):
        raise ValueError(label + ' requires three exact integers')
    return value


def assemble_scatterer(*, side=129, gap=12, source_present=True,
                       target_present=True, translation=(0, 0, 0), wrap=False,
                       tensor=None):
    """Prepare a guided packet and downstream resting target, with true absence.

    The three-packet response is verified for gap 12, sides 129/145. Other
    valid placements are preparations only. Return one ordinary PreparedBoard;
    its manifest and named ports describe the actual translated assembly.
    """
    tensor = _positive_tensor(tensor)
    board = BoardSpec(side, tensor=tensor)
    _integer(gap, range(5, side), 'gap')
    _boolean(source_present, 'source_present')
    _boolean(target_present, 'target_present')
    _boolean(wrap, 'wrap')
    translation = _offset(translation, 'translation')
    m = side // 2
    origin = (m - 8, m, m)
    def put(patch, at, name):
        return place(patch, at=tuple(at[i] + translation[i] for i in range(3)),
                     name=name, wrap=wrap)
    parts = [put(GuideSegment(start=0, stop=side - 1,
                             sockets=tuple(range(origin[0], origin[0] + 4)),
                             remainder_pair=(0, 0), tensor=tensor), (0, m, m), 'guide'),
             put(EvenPacketSource(present=source_present, tensor=tensor), origin, 'source'),
             put(RemainderTarget(remainder=0 if target_present else 2, tensor=tensor),
                 (origin[0] + gap, m - 1, m), 'target')]
    return finalize(board, parts)


def assemble_remainder_register(*, side=233, probe_delays=(28,), writer_present=True,
                                probes_present=(True,), translation=(0, 0, 0),
                                reference_clock=True, reference_offset=(25, 35, 35),
                                wrap=False, tensor=None):
    """Prepare source-overlap register clearing followed by orthogonal read probes.

    The writer's initial remainder halo overlaps all four register addresses.
    One read is verified in the documented holdouts. Two probes with delays
    (28,60) fail the complete second-input contract; this API promises only
    composition validity, not reusable memory or remote writing. Delays and
    all source masks are set before evolution. No callback can change them.

    Return PreparedBoard only: ``initial``, ``ports`` and ``manifest`` are the
    actual final assembly, including translation and the optional reference.
    Whole-board translation can cross periodic boundaries only with wrap=True.
    """
    tensor = _positive_tensor(tensor)
    board = BoardSpec(side, tensor=tensor)
    _boolean(writer_present, 'writer_present')
    _boolean(reference_clock, 'reference_clock')
    _boolean(wrap, 'wrap')
    translation = _offset(translation, 'translation')
    reference_offset = _offset(reference_offset, 'reference_offset')
    delays, masks = tuple(probe_delays), tuple(probes_present)
    if not delays or len(delays) != len(masks):
        raise ValueError('Each positive probe delay needs one explicit presence flag')
    for delay in delays:
        _integer(delay, range(8, side // 2 - 1), 'probe delay')
    for mask in masks:
        _boolean(mask, 'probe presence')
    m = side // 2
    origin, target = (m - 8, m, m), (m - 7, m - 1, m)
    sockets = tuple(m - delay + j for delay in delays for j in range(4)) + (m,)
    if len(set(sockets)) != len(sockets):
        raise ValueError('Probe supports overlap; choose separate complete initial packets')
    def put(patch, at, name, orientation=0):
        return place(patch, at=tuple(at[i] + translation[i] for i in range(3)),
                     name=name, orientation=orientation, wrap=wrap)
    parts = [put(GuideSegment(start=0, stop=side - 1,
                             sockets=tuple(range(m - 8, m - 4)),
                             remainder_pair=(0, 0), tensor=tensor), (0, m, m), 'writer-guide'),
             put(RegisterWriter(present=writer_present, tensor=tensor), origin, 'writer'),
             put(SourceOverlapRegister(tensor=tensor), origin, 'register'),
             put(GuideSegment(start=0, stop=side - 1, sockets=sockets,
                             remainder_pair=(0, 0), tensor=tensor),
                 (target[0], target[1], 0), 'read-guide', 13)]
    parts.extend(put(EvenPacketSource(present=mask, tensor=tensor),
                     (target[0], target[1], m - delay), 'probe' + str(i + 1), 13)
                 for i, (delay, mask) in enumerate(zip(delays, masks)))
    if reference_clock:
        parts.append(put(LocalizedSixClock(tensor=tensor),
                         tuple(m + x for x in reference_offset), 'reference-clock'))
    return finalize(board, parts)
