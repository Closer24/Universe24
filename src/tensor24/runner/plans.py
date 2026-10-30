"""Clock: the plans every Node-clock reads, laid once at the load from the kinds' tables and the universe file's CHOSEN strengths: the metric's push, the volume's notch and each train's passing.
Algebra: every plan is whole factors on rows of the readings: term 5's blocks of the matter's stress through K x K -> A1 onto the square's slots, term 9's monomials of J's potential, and term 11's pairs of each train's rows through its own form onto A1, the table's entry the factor.
Board: one plan for every Node-clock alike; a train that lacks a term takes it at the factor 0, its places wrapped, so no plan names a train.
Clicks: n/a: a plan reaches the clicks only through the act.
"""

import numpy as np

from tensor24.algebra.carry import Z, carry, lit


def pairs_of(trains: Z, c: Z, traces: Z) -> tuple[Z, Z, Z, Z]:
    """Every pair of rows of each train (the load's Trains) through its kinds' table with itself onto A1, the kind whose character is its own square on every turn, one pair per entry of the table and part: (the first row, the second row, the entry, the train), the parts running fastest within a component as the load lays them."""
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))
    form = np.einsum("m,jjmyxi->jxi", trivial, c)
    kind, dim, part = trains.kind, trains.dim.astype(np.intp), trains.part.astype(np.intp)
    of = np.repeat(np.arange(len(trains), dtype=np.intp), trains.count.astype(np.intp))
    before = np.cumsum(dim) - dim
    within = before - before[trains.start.astype(np.intp)][of]
    squares = dim * dim
    entry = np.repeat(np.arange(len(dim), dtype=np.intp), squares)
    place = np.arange(squares.sum(), dtype=np.intp) - np.repeat(np.cumsum(squares) - squares, squares)
    x, i = carry(place, np.repeat(dim, squares), 0)
    train = of[entry]
    # each entry once per part of its train, the part's offset counted within the entry's run
    parts = part[train]
    each = np.repeat(np.arange(len(entry), dtype=np.intp), parts)
    offset = np.arange(parts.sum(), dtype=np.intp) - np.repeat(np.cumsum(parts) - parts, parts)
    first = (trains.first[train] + within[entry] * part[train])[each]
    one, two = first + x[each] * parts[each] + offset, first + i[each] * parts[each] + offset
    return one.astype(np.intp), two.astype(np.intp), form[kind[entry], x, i][each], train[each]


def passing(trains: Z, c: Z, traces: Z, key: Z) -> tuple[Z, Z, Z, Z, Z]:
    """Term 11, every train's passing as the act reads it, with its key: each pair of the train's rows through its kinds' table with itself onto A1 (pairs_of), the entry the factor, so that the train's form over a J(b) - b J(a), the dot product for a vector hand and 1 for a scalar, is summed into the train; the key the universe file's one CHOSEN odd whole, the same for every train."""
    one, two, entry, train = pairs_of(trains, c, traces)
    return one, two, entry, train, key


def spread(*parts: Z) -> Z:
    """Arrays broadcast together and flattened, one row each: a block of terms over the pairs and an axis or two."""
    return np.stack(np.broadcast_arrays(*parts)).reshape(len(parts), -1)


def pushing(trains: Z, c: Z, traces: Z, spokes: Z, strength: Z) -> tuple[Z, Z, Z, Z, Z]:
    """Term 5, the metric's push, as a plan on the readings with the momenta in and out added before the unit: for every pair of a train not the square (the matter) and every square train, J = 2T - eta T from T00 = S (sigma_in sigma_in + sigma_out sigma_out), T_ij = D_i a D_j a and T_0i = (sigma_in + sigma_out) D_i a, S = Spokes x senses the slots' own ratio (c^2 = grip / rest at the loader's lay, two strides against two gradients); the 00 slot pushed by +S J00 (its unit the teeth), each ii, jk and 0i slot by -J (its unit the grips, at both ends of a Mesh), so gamma = 1 and the grips are lowered where matter is; the strength CHOSEN in the universe file; a train that is no square takes every term at the factor 0."""
    one, two, entry, train = pairs_of(trains, c, traces)
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    scale, rows, trained = n * senses, trains.size.sum(), len(trains)
    unit = (
        d + senses * senses
    ) * rows  # the planes: the value, the d differences, the force, the momenta in and out
    sigma_in, sigma_out = d + senses, d + senses + 1
    axis = np.arange(d, dtype=np.intp)
    _, after = carry(axis + 1, d, 0)  # the other two axes of a shear slot, named by its third axis
    _, before = carry(axis + senses, d, 0)
    # every matter pair against every train: the factor carries the pair's entry, the strength, the matter's flag and
    # the target's square flag; the target's slot rows wrap at the rows, harmless at the factor 0
    f = np.outer(entry * trains.matter[train] * strength, trains.square).reshape(-1)
    o, w = np.repeat(one, trained), np.repeat(two, trained)
    q00 = np.tile(trains.first, len(one))
    _, q0i = carry(q00[:, None] + 1 + axis[None, :], rows, 0)
    _, qii = carry(q00[:, None] + 1 + d + axis[None, :], rows, 0)
    _, qjk = carry(q00[:, None] + 1 + senses * d + axis[None, :], rows, 0)
    # the readings each term enters: the momenta's planes at the pair's rows, and the differences' along each axis
    so, sw = sigma_in * rows + o, sigma_in * rows + w
    to, tw = sigma_out * rows + o, sigma_out * rows + w
    grad = 1 + axis[None, :]  # the difference along each axis, a plane per axis
    go, gw = grad * rows + o[:, None], grad * rows + w[:, None]
    ao, aw = (1 + after) * rows + o[:, None], (1 + after) * rows + w[:, None]
    bo, bw = (1 + before) * rows + o[:, None], (1 + before) * rows + w[:, None]
    goo, gww = grad[:, None, :] * rows + o[:, None, None], grad[:, None, :] * rows + w[:, None, None]
    # the factors: S S f on the 00 slot's momenta, S f on its differences, -S f and -f on the ii slots, f on the
    # other axes' differences there, -f on the shears and the 0i slots
    whole, half, less, back = scale * scale * f, scale * f[:, None], -scale * f[:, None], -f[:, None]
    other = f[:, None, None] * lit(
        axis[None, :, None] - axis[None, None, :]
    )  # 1 where the two axes differ
    blocks = np.concatenate(
        (
            spread(so, sw, whole, q00),
            spread(to, tw, whole, q00),
            spread(go, gw, half, q00[:, None]),
            spread(so[:, None], sw[:, None], less, qii),
            spread(to[:, None], tw[:, None], less, qii),
            spread(go, gw, back, qii),
            spread(goo, gww, other, qii[:, :, None]),
            spread(ao, bw, back, qjk),
            spread(bo, aw, back, qjk),
            spread(so[:, None], gw, back, q0i),
            spread(go, sw[:, None], back, q0i),
            spread(to[:, None], gw, back, q0i),
            spread(go, tw[:, None], back, q0i),
        ),
        axis=1,
    )
    first, second, factor, target = blocks
    third = unit + 0 * first
    return (
        first.astype(np.intp),
        second.astype(np.intp),
        third.astype(np.intp),
        factor,
        target.astype(np.intp),
    )


def notching(trains: Z, spokes: Z, strength: Z) -> tuple[Z, tuple[Z, Z, Z, Z]]:
    """Term 9, the volume's notch, as the monomials of J's potential: for every square train, 2 h c00 c00 and h c_ii c_jj over every ordered pair of its ii slots (h tr^2), h the strength CHOSEN in the universe file and the 2 the senses of an axis, so that the vertex law pushes the 00 slot back by -4 h c00 and each ii slot by -2 h tr while the E part and the shears get none; a train that is no square takes its monomials at the factor 0, its places wrapped."""
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    rows, axis = trains.size.sum(), np.arange(d, dtype=np.intp)
    first, flag = trains.first.astype(np.intp), trains.square.astype(object) * strength
    _, qii = carry(first[:, None] + 1 + d + axis[None, :], rows, 0)
    one, two = np.broadcast_arrays(qii[:, :, None], qii[:, None, :])
    legs_one = np.concatenate((first, one.reshape(-1).astype(np.intp)))
    legs_two = np.concatenate((first, two.reshape(-1).astype(np.intp)))
    factor = np.concatenate((senses * flag, np.repeat(flag, d * d)))
    unit = 0 * legs_one - 1
    return factor, (legs_one, legs_two, unit, unit)
