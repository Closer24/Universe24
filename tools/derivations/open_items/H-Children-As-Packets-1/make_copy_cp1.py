"""cp1's flagged copy of the engine: src/event_universe copied whole to /dev/shm/tmp/cp1/src_cp1/event_universe with one act behind one environment flag, empty for the head bit for bit.
CP1_FORM "1": the birth lays each child as a packet by the seed's own lay act (seed.envelope_of, seed.wave_of, seed.phases_of, seed.rest_record, seed.fitted: the raised cosine's envelope of the least half-width about the Link's end, one quantum of the child's unit, at rest at the far end and moving at the taker's end at the wave number the carried division of the recoil gives, MV-S1), laid Node by Node by the one lay act (take.lay) with each Node's momentum booked by the law's reading at that Node (take.momentum_of: the one-Node act, every act one Node and its six Links); the walls re-read with the packets (MS-S1: what is taken is what the lay books), the take then paid from the taken line; each end's lay momentum and its moment about its own centre logged, the packets' amplitudes and waves logged, the run back undoing the packets from the log by the one lay act at -1."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
root = os.environ.get("CP1_COPY", "/dev/shm/tmp/cp1/src_cp1")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:70])
    open(path, "w").write(text.replace(old, new))


close = os.path.join(dst, "close.py")
replace(
    close,
    "import numpy as np\n",
    "import numpy as np\nimport os\n\nCP1_FORM = os.environ.get(\"CP1_FORM\", \"\")  # cp1's flag: empty is the head bit for bit\nWAVE_0 = (0, 0, 0)  # the wave number of a packet at rest (one 0 per axis)\n",
)
replace(
    close,
    "from event_universe import gram, readings\n",
    "from event_universe import gram, readings\nfrom event_universe import seed as seed_module\nfrom event_universe.links import turn_pair\nfrom event_universe.core.rule3 import largest_below, signed_quotient\n",
)
replace(
    close,
    "def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:",
    '''cp1_close: dict[str, Any] = {"rule": {}, "amplitude": {}}


def packet_levels(
    node: Node, s: int, where: tuple[int, ...], sense: int, wave: tuple[int, ...], amplitude: int | None = None
) -> tuple[list[Line], int, list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    """cp1: the child as the seed's own packet (seed.lay_packet's forms, nothing of its own): the raised cosine's envelope of the least half-width the seed knows about the Link's end, at rest at the wave 0 (seed.rest_record, the rest lay) or moving at the wave number (MV-S1: seed.wave_of, seed.phases_of, the level before at the band's rotation), at the largest amplitude whose share summed over the packet is at most one quantum of the child's unit at the close's rule (seed.fitted's search, cached per close) where none is given; returns the lines over the board, the amplitude and the envelope's Nodes with their offsets from the centre."""
    row = node.records()[s]
    assert row.pair is not None
    h, vector, half_tops, pairs = seed_module.HALF_WIDTHS[0], [1, 0], (0,) * AXES, None
    if any(wave):
        half_tops, points, rotation = seed_module.wave_of(node, row, h, tuple(wave), 1)
    envelope, w0 = seed_module.envelope_of(node, where, h, half_tops)
    if any(wave):
        phases = seed_module.phases_of(node, where, h, half_tops, points)
        pairs = (phases, turn_pair(phases[0], phases[1], rotation[0], rotation[1], node.den))
    if amplitude is None:
        key = (s, where, tuple(wave))
        if key not in cp1_close["amplitude"]:
            rule = cp1_close["rule"].get(s)
            if rule is None:
                c, factors = cp1_close.get("read", (node.content(), node.link_factors()))
                rule = cp1_close["rule"][s] = node.rule(row.pair, c, factors)
            cp1_close["amplitude"][key] = cp1_fitted(node, row, envelope, w0, node.units[s], vector, pairs, rule)
        amplitude = cp1_close["amplitude"][key]
    lines = seed_module.rest_record(node, row, envelope, w0, amplitude, sense, vector, pairs)
    nodes = [
        (off, tuple(wrap(where[a] + off[a], node.cube) for a in range(AXES)))
        for off in seed_module.offsets(h, half_tops)
    ]
    return lines, amplitude, nodes


def cp1_fitted(node: Node, row: Any, envelope: Any, w0: int, target: int, vector: list[int], pairs: Any, rule: Any) -> int:
    """seed.fitted at the close's rule (the same search by comparisons, doubling then halving)."""

    def share_of(amplitude: int) -> int:
        lines = seed_module.rest_record(node, row, envelope, w0, amplitude, 1, vector, pairs)
        return seed_module.packet_share(node, row, lines, rule)

    high = 1
    while share_of(high) <= target:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(rule3.half(low + high))
        if share_of(middle) <= target:
            low = middle
        else:
            high = middle
    return low


def packet_at(
    node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1, wave: tuple[int, ...] = WAVE_0, amplitude: int | None = None
) -> tuple[list[int], list[int], int, int, int]:
    """cp1: one child laid as a packet at one end, Node by Node by the one lay act (take.lay) in the envelope's order (reversed with the sign -1), each Node's momentum booked by the law's reading at that Node (take.momentum_of: the one-Node act); returns the booked momentum summed, its moment about the packet's centre (the offset times the momentum booked at the Node), the packet's charge (the Wronskian's change summed over its Nodes), the amplitude and the Nodes' count."""
    row = node.records()[s]
    re, im = row.lines
    assert row.pair is not None
    num = row.pair[0]
    lines, amplitude, nodes = packet_levels(node, s, where, sense, wave, amplitude)
    dp, moment, charge = [0] * AXES, [0] * AXES, 0
    for off, at in (nodes if sign == 1 else list(reversed(nodes))):
        levels = (int(lines[0].now[at]), int(lines[0].before[at]), int(lines[1].now[at]), int(lines[1].before[at]))
        d_re = momentum_of(node, re.now, re.before, at, d_now=sign * levels[0], d_before=sign * levels[1], num=num)
        d_im = momentum_of(node, im.now, im.before, at, d_now=sign * levels[2], d_before=sign * levels[3], num=num)
        w_was = int(cross(re.now[at], im.now[at], re.before[at], im.before[at]))
        lay(node, s, at, levels, sign)
        charge += int(cross(re.now[at], im.now[at], re.before[at], im.before[at])) - w_was
        booked = [a + b for a, b in zip(d_re, d_im, strict=True)]
        dp = [a + b for a, b in zip(dp, booked, strict=True)]
        moment = [a + b for a, b in zip(moment, cross3(list(off), booked), strict=True)]
    return dp, moment, charge, amplitude, len(nodes)


def cross3(r: list[int], p: list[int]) -> list[int]:
    """The moment r x p, the law's bilinear (links.cross) on each pair of axes."""
    return [cross(r[1], r[2], p[1], p[2]), cross(r[2], r[0], p[2], p[0]), cross(r[0], r[1], p[0], p[1])]


def pair_momentum(node: Node, kid: Kid, waves: tuple[tuple[int, ...], tuple[int, ...]]) -> list[int]:
    """cp1: the two packets' booked momentum read by a trial lay of both, taken back (the exact read of what the lay books)."""
    dp = [0] * AXES
    for where, sense, wave in ((kid.minus, -1, waves[0]), (kid.plus, 1, waves[1])):
        d = packet_at(node, kid.line_pair, where, sense, wave=wave)[0]
        dp = [a + b for a, b in zip(dp, d, strict=True)]
    for where, sense, wave in ((kid.plus, 1, waves[1]), (kid.minus, -1, waves[0])):
        packet_at(node, kid.line_pair, where, sense, -1, wave=wave)
    return dp


def waves_of(
    node: Node, at: tuple[int, ...], kids: list[Kid], walls: dict[Any, tuple[int, int]], rule: rule3.Rule, rec: int, c: Any, factors: tuple[Any, ...]
) -> dict[Kid, tuple[tuple[int, ...], tuple[int, ...]]]:
    """cp1: the packets' wave numbers per kid from the predicted recoil of the take of the walls (fall_of read, nothing written; momentum_of of the predicted levels on the taken line): the taker's packet (the end at the take's Node) carries the whole recoil, the far end's packet is at rest (the letter: the far packet's transverse momentum would turn about the taker's Node by the Link's arm, so J closes at every centre only with it at 0); per axis the wave number is the carried division of the residual by the packet's momentum per unit of the wave number read by a trial lay (the secant over a bump of the wave's own size), within the band's half (|h|^2 <= den^2 div 2, where the lattice momentum rises with the wave number), carried to its fixed point with the walls re-read at every pass (MS-S1: the lay books what the take pays)."""
    row = node.records()[rec]
    assert row.pair is not None
    found = {kid: (WAVE_0, WAVE_0) for kid in kids}
    cap = largest_below(int(quotient(node.den * node.den, 2)))
    best: dict[Kid, tuple[int, tuple[tuple[int, ...], tuple[int, ...]]]] = {}
    for _pass in range(AXES + AXES):
        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        levels, _fall, k = fall_of(node, at, booked, rule, row)
        if levels is None:
            return found
        z = row.lines[k]
        toward = 1 if int(z.before[at]) > int(z.now[at]) else -1
        residual = [-x for x in momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=row.pair[0])]
        before = dict(found)
        for kid in kids:
            end = 0 if kid.minus == at else 1
            base = pair_momentum(node, kid, found[kid])
            left = [r - b for r, b in zip(residual, base, strict=True)]
            norm = sum(abs(x) for x in left)
            if kid not in best or norm < best[kid][0]:
                best[kid] = (norm, found[kid])
            w = list(found[kid][end])
            for a in range(AXES):
                bump = max(abs(w[a]) // (AXES + AXES + AXES - 1), cap // (AXES + AXES)) if w[a] else int(rule3.half(cap))  # the secant's bump: the band's quarter from rest (the lattice momentum unresolved at the levels of one quantum near the wave 0), a ninth of the wave after
                trial = list(w)
                trial[a] = max(-cap, min(cap, trial[a] + bump))
                if trial[a] == w[a]:
                    trial[a] = w[a] - bump
                waves = list(found[kid])
                waves[end] = tuple(trial)
                gain = pair_momentum(node, kid, (waves[0], waves[1]))[a] - base[a]
                if gain:
                    w[a] = max(-cap, min(cap, w[a] + int(signed_quotient(left[a] * (trial[a] - w[a]), gain))))
            waves = list(found[kid])
            waves[end] = tuple(w)
            found[kid] = (waves[0], waves[1])
            residual = [r - b for r, b in zip(residual, pair_momentum(node, kid, found[kid]), strict=True)]
            walls[Birth(at, *kid, rec)] = walls_of(node, kid.line_pair, kid.minus, kid.plus, c, factors, found[kid])
        if found == before:
            break
    for kid in kids:
        if best[kid][1] != found[kid]:
            base = pair_momentum(node, kid, found[kid])
            if sum(abs(r - b) for r, b in zip(residual, base, strict=True)) > best[kid][0]:
                found[kid] = best[kid][1]
                walls[Birth(at, *kid, rec)] = walls_of(node, kid.line_pair, kid.minus, kid.plus, c, factors, found[kid])
    return found


def child_at(node: Node, s: int, where: tuple[int, ...], sense: int, sign: int = 1) -> list[int]:''',
)
replace(
    close,
    "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...]\n) -> tuple[int, int]:",
    "    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], c: Any, factors: tuple[Any, ...], waves: tuple[tuple[int, ...], tuple[int, ...]] = (WAVE_0, WAVE_0)\n) -> tuple[int, int]:",
)
replace(
    close,
    """    before = total()
    child_at(node, s, minus, -1)
    middle = total()
    child_at(node, s, plus, 1)
    after = total()
    child_at(node, s, plus, 1, -1)
    child_at(node, s, minus, -1, -1)
""",
    """    before = total()
    if CP1_FORM == "1":
        packet_at(node, s, minus, -1, wave=waves[0])
        middle = total()
        packet_at(node, s, plus, 1, wave=waves[1])
        after = total()
        packet_at(node, s, plus, 1, -1, wave=waves[1])
        packet_at(node, s, minus, -1, -1, wave=waves[0])
        return middle - before, after - middle
    child_at(node, s, minus, -1)
    middle = total()
    child_at(node, s, plus, 1)
    after = total()
    child_at(node, s, plus, 1, -1)
    child_at(node, s, minus, -1, -1)
""",
)
replace(
    close,
    """def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...]
) -> tuple[list[int], list[int], list[list[int]]]:""",
    """def child_laid(
    node: Node, s: int, minus: tuple[int, ...], plus: tuple[int, ...], waves: tuple[tuple[int, ...], tuple[int, ...]] | None = None
) -> tuple[list[int], list[int], list[list[int]], dict[str, Any]]:""",
)
replace(
    close,
    """    dp_lay = [0, 0, 0]
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            dp_lay[a] += d
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood
""",
    """    dp_lay = [0, 0, 0]
    if waves is not None:
        ends, moments, charges, amplitudes, counts = [], [], [], [], []
        for where, sense, wave in ((minus, -1, waves[0]), (plus, 1, waves[1])):
            dp, moment, charge, amplitude, count = packet_at(node, s, where, sense, wave=wave)
            ends.append(dp)
            moments.append(moment)
            charges.append(charge)
            amplitudes.append(amplitude)
            counts.append(count)
            for a, d in enumerate(dp):
                dp_lay[a] += d
        extra = {"waves": [list(w) for w in waves], "dP_lay_ends": ends, "moment_ends": moments, "amplitude_packets": amplitudes, "packet_nodes": counts}
        return dp_lay, charges, stood, extra
    for where, sense in ((minus, -1), (plus, 1)):
        for a, d in enumerate(child_at(node, s, where, sense)):
            dp_lay[a] += d
    senses = [int(cross(re.now[w_], im.now[w_], re.before[w_], im.before[w_])) for w_ in (minus, plus)]
    return dp_lay, senses, stood, {}
""",
)
replace(
    close,
    """    by_node: dict[tuple[tuple[int, ...], int], list[Kid]] = {}
    for at, s, minus, plus, room, rec in kept:
        by_node.setdefault((at, rec), []).append(Kid(s, minus, plus, room))
""",
    """    by_node: dict[tuple[tuple[int, ...], int], list[Kid]] = {}
    cp1_close["rule"], cp1_close["amplitude"], cp1_close["read"] = {}, {}, (c, factors)
    for at, s, minus, plus, room, rec in kept:
        by_node.setdefault((at, rec), []).append(Kid(s, minus, plus, room))
""",
)
replace(
    close,
    """        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
        if one is None:
            continue
        levels, fall, now, before, k = one
        node.closes[at] -= 1
        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        taken.append((at, rec, kids, take))
""",
    """        waves = waves_of(node, at, kids, walls, rule, rec, c, factors) if CP1_FORM == "1" else None
        booked = sum(sum(walls[Birth(at, *kid, rec)]) for kid in kids)
        one = take_at(node, at, booked, rule, len(kids), rec)
        if one is None:
            continue
        levels, fall, now, before, k = one
        node.closes[at] -= 1
        take = take_line(fall, booked, levels, now, before, node.last_dp, k)
        if waves is not None:
            take["waves"] = waves
        taken.append((at, rec, kids, take))
""",
)
replace(
    close,
    """    for s, minus, plus, room in kids:
        dp_lay, w_children, stood = child_laid(node, s, minus, plus)
""",
    """    for s, minus, plus, room in kids:
        waves = None if "waves" not in take else take["waves"].get(Kid(s, minus, plus, room), (WAVE_0, WAVE_0))
        dp_lay, w_children, stood, extra = child_laid(node, s, minus, plus, waves)
""",
)
replace(
    close,
    """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
""",
    """                "dP_lay": dp_lay,
                **({"takes": take["takes"]} if "takes" in take else {}),
                **extra,
""",
)
replace(
    close,
    """            s, (a, b) = entry["line_pair"], entry["amplitude"]
            lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
            lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
""",
    """            s, (a, b) = entry["line_pair"], entry["amplitude"]
            if "waves" in entry:
                for where, sense, wave, amplitude in zip(("plus", "minus"), (1, -1), reversed(entry["waves"]), reversed(entry["amplitude_packets"]), strict=True):
                    lines, _amplitude, _nodes = packet_levels(node, s, tuple(entry[where]), sense, tuple(wave), amplitude)
                    lay(node, s, Ellipsis, tuple(x for line in lines for x in (line.now, line.before)), -1)
            else:
                lay(node, s, tuple(entry["minus"]), (a, 0, 0, -b), -1)
                lay(node, s, tuple(entry["plus"]), (a, 0, 0, b), -1)
""",
)
replace(close, "from event_universe.core.ports import AXES, across, port_of\n", "from event_universe.core.ports import AXES, across, port_of, wrap\n")
print("copied to", root)
