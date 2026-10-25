"""pc2: the carried clock (K-S4 in form), a module of the hand pc2 beside the engine's core/paces.py, which it reads and never edits.

The clock as one carried division per content (The paces compose: p_0(c + 1) = p_0(c) lambda, lambda = 1 - 1 / Gamma, one act per unit of content;
Rule3's division act (c) with the remainder kept):
    Gamma p(c + 1) + r(c + 1) = (Gamma - 1) p(c) + r(c),   0 <= r(c + 1) < Gamma,   p(0) = Gamma, r(0) = Gamma div 2 (the half wall; Every Node's remainder is born at the half wall);
the hills' side (c < 0) by the inverse act, the numerator's and the wall's factors exchanged:
    (Gamma - 1) p(c - 1) + r(c - 1) = Gamma p(c) + r(c),   0 <= r(c - 1) < Gamma - 1,
so that the forward act carries every content to the next over the whole chain, forward(p(c - 1), r(c - 1)) = (p(c), r(c)) for every c.
The Link's pace from the clock, p_a = p_0^2 / Gamma rounded half up once (The two rounded integers of the rule), no remainder: a pace is a coefficient and no level.
The flag CARRIED chooses between this clock and the engine's memo (core/paces.clock_of, link_pace_of); off the flag every function here is the engine's, bit for bit.
The volume's two readings (features/volume.volume_of, level_of) are rewritten here on the chosen clock, the same form: X(a) = ceil(Gamma^5 / p_0(a)^4), a(X) the largest a with Gamma^5 <= X p_0(a)^4.
No float; integers only."""
from __future__ import annotations
import numpy as np
from event_universe.core import paces as engine_paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume as engine_volume

CARRIED = False  # the flag: True reads the carried clock, False the engine's memo
EXPONENT = 4  # the volume's power d + 1 = 4 (features/volume), read from the engine's module where it names it
try:
    EXPONENT = int(engine_volume.EXPONENT)
except Exception:
    pass

rounded = engine_paces.rounded
odd_rounded = engine_paces.odd_rounded
sine_den = engine_paces.sine_den
frozen_content_engine = engine_paces.frozen_content

_MEMO = {}  # per Gamma: {'hollows': [(p, r), ...], 'hills': [(p, r), ...]}


def _sides(gamma):
    found = _MEMO.get(gamma)
    if found is None:
        half = division_forward(gamma, 2, 0)[0]
        found = {'hollows': [(gamma, int(half))], 'hills': [(gamma, int(half))]}
        _MEMO[gamma] = found
    return found


def carried_forward(gamma, p, r):
    """The one carried division per content, hollows: (p, r) at c to (p', r') at c + 1."""
    total = (gamma - 1) * p + r
    q = total // gamma
    return q, total - gamma * q


def carried_back(gamma, p, r):
    """The inverse act, hills: (p, r) at c to (p', r') at c - 1, the division at the wall Gamma - 1."""
    total = gamma * p + r
    q = total // (gamma - 1)
    return q, total - (gamma - 1) * q


def carried_pair(gamma, content):
    """The clock and its remainder at a content from the carried chain, filled lazily on either side."""
    sides = _sides(gamma)
    if content >= 0:
        side = sides['hollows']
        while len(side) <= content:
            side.append(carried_forward(gamma, *side[-1]))
        return side[content]
    side = sides['hills']
    size = -content
    while len(side) <= size:
        side.append(carried_back(gamma, *side[-1]))
    return side[size]


def carried_clock(gamma, content):
    return carried_pair(gamma, int(content))[0]


def carried_link_pace(gamma, content):
    p = carried_clock(gamma, content)
    return int(rounded(p * p, gamma))


def clock(gamma, content):
    return carried_clock(gamma, content) if CARRIED else engine_paces.clock(gamma, int(content))


def link_pace(gamma, content):
    return carried_link_pace(gamma, content) if CARRIED else engine_paces.link_pace(gamma, int(content))


def _lookup(found, gamma, contents):
    values = np.asarray(contents)
    if values.ndim == 0:
        return found(gamma, int(values))
    if values.size == 0:
        return values
    flat = values.reshape(-1)
    table = np.array([found(gamma, int(c)) for c in flat.tolist()], dtype=values.dtype)
    return table.reshape(values.shape)


def clock_of(gamma, contents):
    return _lookup(carried_clock, gamma, contents) if CARRIED else engine_paces.clock_of(gamma, contents)


def link_pace_of(gamma, contents):
    return _lookup(carried_link_pace, gamma, contents) if CARRIED else engine_paces.link_pace_of(gamma, contents)


def frozen_content(gamma):
    """The least content at which the Link's pace is 0 on the chosen clock."""
    if not CARRIED:
        return engine_paces.frozen_content(gamma)
    c = 0
    while carried_link_pace(gamma, c) > 0:
        c += 1
    return c


def clock_zero(gamma):
    """The least content at which the clock itself is 0 on the chosen clock."""
    c = 0
    while clock(gamma, c) > 0:
        c += 1
    return c


_LEVELS = {}


def volume_of(gamma, levels):
    if not CARRIED:
        return engine_volume.volume_of(gamma, levels)
    found = np.asarray(levels)
    target = gamma ** (EXPONENT + 1)
    flat = found.reshape(-1)
    volumes = []
    for a in flat.tolist():
        p = carried_clock(gamma, int(a))
        volumes.append(int(division_forward(target + p ** EXPONENT - 1, p ** EXPONENT, 0)[0]))
    return np.array(volumes, dtype=object).reshape(found.shape)


def level_of(gamma, volume):
    """The level a of the volume X: the largest a with Gamma^5 <= X p_0(a)^4, a search by comparisons from the deepest hill upward (the engine's form on the chosen clock)."""
    if not CARRIED:
        return engine_volume.level_of(gamma, volume)
    volumes = np.asarray(volume, dtype=object).reshape(-1)
    if any(int(x) <= 0 for x in volumes.tolist()):
        raise ValueError('the volume X is at most 0 at a Node: the level has no reading, refused by name')
    memo = _LEVELS.setdefault(gamma, {})
    target = gamma ** (EXPONENT + 1)
    top = clock_zero(gamma)
    out = []
    for x in volumes.tolist():
        x = int(x)
        a = memo.get(x)
        if a is None:
            reached = lambda lev: x * carried_clock(gamma, lev) ** EXPONENT >= target
            low = -gamma
            if not reached(low):
                raise ValueError('the volume lies below the deepest hill: refused by name')
            step = 1
            while low + step < top and reached(low + step):
                low = low + step
                step = step + step
            high = min(low + step, top)
            while high - low > 1:
                middle = int(division_forward(low + high, 2, 0)[0])
                if reached(middle):
                    low = middle
                else:
                    high = middle
            a = low
            memo[x] = a
        out.append(a)
    return np.array(out, dtype=object).reshape(np.asarray(volume).shape)


def clear_memo():
    _MEMO.clear()
    _LEVELS.clear()
    engine_paces.clear_memo()
