"""Clock: the plans every Node-clock reads, laid once at the load from the star, the kinds' tables and the universe file's CHOSEN strengths: the metric's push (the books' form, no strength: push 1 or 0), the volume's notch, the held hand's spring and tie, the hands' tie, the gradient vertex through the Mesh, the passing on every edge between two trains and the Mesh's edges.
Algebra: every plan is whole factors on rows of the readings: term 5's push in the books' form, the momenta in and out of every row the push does not land on onto the 00 slot and every row's six stretches squared onto the ii slots of their axes, the monomials of J's potential (term 9's notch, term 6's own spring (spring; rho, rho, 1, 1), tie (hold f C_yz; x_y, x_z, k_rho, k_rho) and hands' tie (tie C_yz; x_y, y_z, 1, 1) through K x K -> A1), the gradient vertex's two pushes of mesh M_j D_i L, L's difference onto a tied row and the tied row's difference onto L, through the table of its kind with the axes' kind onto A1, the table's entry the factor, and term 11 on the edges: each term of J's plan weighed onto every other train of its monomial, David's split as pair flows.
Board: one plan for every Node-clock alike; a train that lacks a term takes it at the factor 0, its places wrapped, so no plan names a train: which train is held, tied or the board's wave is read off its character by the load.
Clicks: the tied hand's beat, 2 hold f |k|^2 / W at the Node-clock, is what the clicks read as its mass, one beat per tied train (the frame's price, FRAMES 6); a plan reaches the clicks only through the act.
"""

import numpy as np

from tensor24.algebra.carry import Z, carry, lit


def pairs_of(trains: Z, c: Z, traces: Z, kept: Z) -> tuple[Z, Z, Z, Z]:
    """Every pair of rows of each train (the load's Trains) through its kind's form with itself onto A1, one form for every kind (selves), one pair per entry of the form and part: (the first row, the second row, the entry, the train), the parts running fastest within a component as the load lays them."""
    form = selves(c, traces, kept)
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
    factor = form[kind[entry], x, i]
    return one.astype(np.intp), two.astype(np.intp), factor[each], train[each]


def selves(c: Z, traces: Z, kept: Z) -> Z:
    """Every kind's form with itself onto A1, one array for every kind in the vocabulary's order (files.vocabulary): the five's from the 24's tables, A1 the kind whose character is its own square on every turn, each set in the kept forms' side, then each half-speed kind's kept form (load.kept_forms, SUM L^T L over the 48 lifts by their count), the dot derived."""
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))
    _, put = widening(c, kept)
    own = np.einsum("m,jjmyxi->jxi", trivial, c)
    return np.concatenate((np.einsum("ax,jxi,bi->jab", put, own, put), kept))


def widening(c: Z, kept: Z) -> tuple[Z, Z]:
    """The 24's tables set among every kind and in the kept forms' side: the five kinds' places first, as files.vocabulary lists them, then one per half-speed kind, which no table holds (0: no half-speed table is built in this build); and the axes' cube at the first rows of the kept forms' side."""
    every = np.eye(len(c) + len(kept), len(c), dtype=object)
    return every, np.eye(kept.shape[-1], c.shape[-1], dtype=object)


def edging(trains: Z, potential: tuple[Z, tuple[Z, Z, Z, Z]], key: Z, spokes: Z) -> tuple[Z, Z, Z]:
    """Term 11 on the edges, every passing between two trains as the act reads it, with the edge key (the owner's shared tooth for every pair of clocks, NC29b on David's split): per term of J's plan, as contract.pushes lays them (leg by leg, each leg's monomials in their order), its weight on every train and the train of the leg it pushes; and every side's key. A monomial's legs: each position one leg, a held train's positions one leg together, its excursion |k|^2 (the held spring's rest, n = 0); a leg's weight kappa (L - l) / L, L the monomial's legs and l its own train's, so a two-leg monomial weighs kappa / 2 on both legs and a tie kappa 2 / 3 on its held legs and kappa / 3 on its tied pair, David's split in the work form (NC29b's 3, 4 and 2 at kappa 6); its weight on a train u is that times 1 where the monomial has a value leg in u (one scatter of its legs' trains, lit), 0 elsewhere, so the side (t, u) passes SUM over the monomials on both trains of SUM_i ([leg i in t] - [leg i in u]) w_i W_i and the side (u, t) its negative, the diagonal, an own monomial and a pair of trains no monomial joins weighing 0; a monomial with value legs in three trains lies on the triangle's three edges, each edge passing the difference of its two trains' weighed work, the third train's legs weighing 0 there (no plan lays one; the mathematician's count on every world, NC29b's minor 1). kappa: the product of two and of every legs count a live monomial on an edge holds, each once, so that every weight is whole (6 on every world laid: the hands' tie's two legs and the tie's three); every side's key the universe file's one CHOSEN key times kappa / two, 3 there (David's OPEN, a change of a declared number, NC29b), the same for every side at every reach, its own Node-clock and across each Spoke (crossing, the Mesh's edges), odd as the key is, so a side's two teeth born at (key - 1) div senses sum to key - 1 (load.load) and stay so by the carry's law; no count typed: two the senses of an axis, read from the star, the positions the legs' own."""
    factor, legs = potential
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    stacked = np.stack(legs)  # (positions, monomials): each monomial's legs, the unit -1
    positions, monomials = stacked.shape
    row, of, _, _, _ = rows_of(trains)
    count = len(trains)
    trained = np.full(
        trains.size.sum() + 1, count, dtype=np.intp
    )  # each row's train, the unit's last, past every train
    trained[row] = of
    train = trained[stacked]  # each leg's train
    value = lit(train - count)  # 1 on a value leg, 0 on the unit's
    incidence = np.full((monomials, count + 1), 0, dtype=object)
    np.add.at(incidence, (np.arange(monomials, dtype=np.intp)[None, :] + 0 * train, train), 1)
    positioned = incidence[:, :count]  # each monomial's positions on each train
    present = lit(positioned)
    own = positioned - trains.held[None, :] * (positioned - present)  # its legs on each train
    total = own.sum(axis=1)
    mine = np.concatenate((own, 0 * own[:, :1]), axis=1)[
        np.arange(monomials, dtype=np.intp)[None, :], train
    ]
    owners = present.sum(axis=1)
    # a live monomial with value legs in two trains or more, and the edge monomials holding each count of legs
    edged = lit(factor) * lit(owners * owners - owners)
    counts = np.arange(1, positions + 1, dtype=object)
    among = (edged[:, None] * (1 - lit(total[:, None] - counts[None, :]))).sum(axis=0)
    kappa = np.prod(1 + lit(among + 1 - lit(counts - senses)) * (counts - 1))
    # kappa over the monomial's legs, a constant monomial reading 1
    share, _ = carry(kappa, total + 1 - lit(total), 0)
    weight = (share * edged)[None, :] * (total[None, :] - mine) * value
    scale, _ = carry(kappa, senses, 0)
    return (
        (weight[:, :, None] * present[None, :, :]).reshape(positions * monomials, count),
        (train * value).reshape(-1),
        np.full(((1 + n) * count * count, 1), key * scale, dtype=object),
    )


def crossing(trains: Z, mesh: tuple[Z, Z, Z], spokes: Z, nb: Z, scale: Z) -> tuple[Z, Z]:
    """Term 11 across the Meshes, the wave's edges (term 6's gradient vertex, plans.meshing, split by the Spoke it reads across; the wave's edge note, onelaw sections 1 and 3, sound by both hostile readers): per Spoke, every pair of rows, r at a Node-clock and p at the Node-clock across the Spoke, its coupling, the Mesh contraction's matrix entry: the plan's factor times the Spoke's sense along the term's axis (the term reads the difference D_i p = p(s + e_i) - p(s - e_i), the Spokes + i and - i), summed over the plan's terms by one scatter, and 0 where a Spoke and its opposite reach one Node-clock (a side of 1 or 2: there the entries summed over the Spokes that reach the same partner cancel, + f - f; the mathematician's MINOR 1), so that summed over the Spokes the edges are the Mesh contraction itself; the two ends of an edge hold the same coupling, as the plan's two halves are adjoint (J_l = F C D m, J_m = -F C D l, D antisymmetric): the coupling of (r, p) across a Spoke is that of (p, r) across its opposite; each times scale, kappa / two, each end one leg as a two-leg monomial's, so a Mesh edge counts at the edge key in the act's own units; and the side (Spoke, t, u) each pair books on, at (Spoke trains + t) trains + u, t the row's train and u the partner's, the act laying these sides after every train's own Node-clock's (the Mesh plan's terms read one difference and the unit twice, as plans.meshing lays them)."""
    (first, *_), factor, target = mesh
    rows, count, n = trains.size.sum(), len(trains), len(spokes)
    plane, source = carry(
        first, rows, 0
    )  # the term's difference along the axis plane - 1, at the row source
    sense = spokes[:, plane - 1]  # each Spoke's sense along the term's axis: + 1, - 1, or 0 off it
    every = np.arange(n, dtype=np.intp)[:, None] + 0 * target[None, :]
    coupling = np.full((n, rows, rows), 0, dtype=object)
    np.add.at(coupling, (every, 0 * every + target, 0 * every + source), sense * factor[None, :])
    # each Spoke's opposite by the star, and whether the two reach two Node-clocks at every Node-clock
    turned = spokes[:, None, :] + spokes[None, :, :]
    opposite = 1 - lit((turned * turned).sum(axis=-1))
    gap = nb - opposite @ nb
    apart = lit((gap * gap).sum(axis=-1))
    row, of, _, _, _ = rows_of(trains)
    trained = np.full(rows, 0, dtype=np.intp)
    trained[row] = of
    spoke = np.arange(n, dtype=np.intp)[:, None, None]
    onto = (spoke * count + trained[None, :, None]) * count + trained[None, None, :]
    return scale * apart[:, None, None] * coupling, onto


def rows_of(trains: Z) -> tuple[Z, Z, Z, Z, Z]:
    """Every row of the board once, as the load lays them (a train's kinds in the file's order, each kind's components, the parts running fastest): the row, its train, its kind, its component within the kind and its part."""
    kind, dim, part = trains.kind, trains.dim.astype(np.intp), trains.part.astype(np.intp)
    of = np.repeat(
        np.arange(len(trains), dtype=np.intp), trains.count.astype(np.intp)
    )  # each entry's train
    before = np.cumsum(dim) - dim
    within = (
        before - before[trains.start.astype(np.intp)][of]
    )  # each entry's components before it in its train
    size = dim * part[of]  # each entry's rows: its components times its train's part
    each = np.repeat(np.arange(len(kind), dtype=np.intp), size)
    place = np.arange(size.sum(), dtype=np.intp) - np.repeat(np.cumsum(size) - size, size)
    component, offset = carry(place, part[of][each], 0)
    row = trains.first[of[each]] + (within[each] + component) * part[of][each] + offset
    return row.astype(np.intp), of[each], kind[each], component.astype(np.intp), offset.astype(np.intp)


def holding(
    trains: Z, c: Z, traces: Z, kept: Z, rest: Z, hold: Z, gamma: Z, spring: Z
) -> tuple[Z, tuple[Z, Z, Z, Z]]:
    """Term 6's frame, the held hand's monomials of J's potential: every held row's own spring (spring; rho, rho, 1, 1), spring the strength CHOSEN in the universe file, which pushes the row by -2 spring rho as the leg stands twice (its window 0 < 2 spring < 4 W, W the rest teeth, is not checked as such: a run that leaves it, as any runaway, is named by the run's promise of the width, runner/run.py's wide; 0 lays none), and every tied train's tie to the held hand's square, (hold x f x C_yz; x_y, x_z, k_rho, k_rho) for each pair of the train's rows through its form onto A1 (pairs_of's entry) and each held row, f = rest div Gamma the clock's one notch (CHOSEN with its reason, G3 2.4), so that a tied hand beats at 2 hold f |k|^2 / W in the dispersion's measure; hold the strength CHOSEN in the universe file, 1 the unit; a row that is not held and a train that is not tied take the factor 0. The tie is a monomial of four value legs: it enters no train's passing only while the held hand's turn is an exact quarter (now orthogonal to before, the norm exact: the room), which no plan lays; past the room the held train clicks alone and the books open (NOT_CLOSED 29)."""
    f, _ = carry(rest, gamma, 0)
    row, of, _, _, _ = rows_of(trains)
    held = trains.held[of]  # 1 at the held hand's rows
    unit = 0 * row - 1
    one, two, entry, train = pairs_of(trains, c, traces, kept)
    tie = hold * f * (entry * trains.tied[train])[:, None] * held[None, :]
    blocks = np.concatenate(
        (
            spread(row, row, unit, unit, spring * held),
            spread(one[:, None], two[:, None], row[None, :], row[None, :], tie),
        ),
        axis=1,
    )
    first, second, third, fourth, factor = blocks
    return factor, (
        first.astype(np.intp),
        second.astype(np.intp),
        third.astype(np.intp),
        fourth.astype(np.intp),
    )


def tying(trains: Z, c: Z, traces: Z, kept: Z, tie: Z) -> tuple[Z, tuple[Z, Z, Z, Z]]:
    """Term 6's frame, the hands' tie: for every two distinct tied trains X and Y, each unordered pair once, (tie x C_yz; x_y, y_z, 1, 1) over their rows of one part through the kinds' table of X's kind with Y's onto A1, the kind whose character is its own square (the dot product for T1 with T1 and T2 with T2, 1 for A1 with A1 and A2 with A2, 0 across two kinds); tie the strength CHOSEN in the universe file (a ground state below 2 hold f); a pair with no channel, two rows of different parts, an untied train and a train with itself take the factor 0."""
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))
    form = np.einsum(
        "m,jkmyxi->jkxi", trivial, c
    )  # each kind with each kind onto A1, component by component
    every, put = widening(c, kept)  # every kind, a half-speed one's places 0, its train untied
    wide = np.einsum("Jj,Kk,jkxi->JKxi", every, every, form)
    form = np.einsum("JKai,bi->JKab", np.einsum("ax,JKxi->JKai", put, wide), put)
    row, of, kind, component, offset = rows_of(trains)
    later = of[None, :] - of[:, None]  # how far the second row's train stands after the first's
    down, _ = carry(
        -later, later * later + 1, 0
    )  # -1 where it stands after, 0 where it does not: the sign test
    gap = offset[:, None] - offset[None, :]
    same, _ = carry(1, gap * gap + 1, 0)  # 1 where the two rows are of one part
    channel = form[kind[:, None], kind[None, :], component[:, None], component[None, :]]
    factor = tie * trains.tied[of][:, None] * trains.tied[of][None, :] * -down * same * channel
    unit = 0 * row[:, None] - 1
    first, second, third, fourth, factor = spread(row[:, None], row[None, :], unit, unit, factor)
    return factor, (
        first.astype(np.intp),
        second.astype(np.intp),
        third.astype(np.intp),
        fourth.astype(np.intp),
    )


def joined(*potentials: tuple[Z, tuple[Z, Z, Z, Z]]) -> tuple[Z, tuple[Z, Z, Z, Z]]:
    """Several potentials as one: their monomials' factors and four legs concatenated, in their order."""
    factors, legs = zip(*potentials, strict=True)
    first, second, third, fourth = zip(*legs, strict=True)
    return np.concatenate(factors), (
        np.concatenate(first),
        np.concatenate(second),
        np.concatenate(third),
        np.concatenate(fourth),
    )


def spread(*parts: Z) -> Z:
    """Arrays broadcast together and flattened, one row each: a block of terms over the pairs and an axis or two."""
    return np.stack(np.broadcast_arrays(*parts)).reshape(len(parts), -1)


def pushing(trains: Z, spokes: Z, push: Z) -> tuple[Z, Z, Z]:
    """Term 5, the metric's push in the books' form, as a plan on the push's readings (step.stress: the six stretches per row, Spoke s and row r at the plane s rows + r in the star's order, the momenta in and out in whole turns of the rest dial at the planes Spokes rows + r and (Spokes + 1) rows + r, the unit last): the act's energy is H = W v_in v_out / 2 + SUM over the Meshes of grip Delta^2 / 2 with the reads W = rest + k0 c00 into every row but the 00 and grip = grip_rest + ii at both ends, and the books close iff each slot is pushed by -dH / d slot, the derivative taken at fixed momentum, which a clock keeps as its teeth move (dH / dW = -v^2 / 2 there, so the 00 slot is pushed by +k0 v^2 / 2; at fixed velocity it would read +v^2 / 2 and push the wrong way); so for every square train one term (sigma_in, sigma_out, unit) at the factor k0 x push on the 00 slot for every row the push does not land on, the rows on the force's path at T_d = 1 (the sourcing trains' rows and the square's 0i and jk rows; its 00 and ii rows left out, as a pushed row's stride as the stress reads it is fictitious, read before the push's own kick and at the dial's remainder, so no plan reads it and the mirror swaps every stride a plan reads, the mirror theorem's hypothesis (d); the price: the metric's own kinetic share of the books, its self-stress, OPEN in G2, is not paid into the 00 slot), k0 the clock read's factor Spokes x senses from the star (the chain rule carries the read's factor into the push, so one number serves both; the board's wave, its grip reading the ii slots, needs it, gamma owed to the click world), and for every row and every Spoke one term (the stretch, the stretch, unit) at the factor -push on the ii slot of the Spoke's axis (the two Meshes' stretches squared, not the centred difference squared, which misses the Meshes at a crest or a foot), both halved by the drive's dial senses on those rows with the remainder kept (load.geared); no term on the jk and 0i slots, which nothing reads, so a push there would be energy from nothing; the momenta are read in whole turns of the rest dial by the centred split, a count a round at the rest teeth, so a row gliding below half a count a round pushes the 00 slot by nothing; push is 1 where the books close (gravity on) and 0 where there is none, and the files' format refuses any other value by name (it would open the books by that factor); a train that is no square takes every term at the factor 0, its places wrapped."""
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    scale, rows = n * senses, trains.size.sum()
    row = np.arange(rows, dtype=np.intp)
    first = trains.first.astype(np.intp)
    axis = np.arange(d, dtype=np.intp)
    along = (spokes * spokes) @ axis  # each Spoke's axis, as the grips' read has it
    # the rows the push lands on, each square's 00 slot and the ii slot of each Spoke's axis; a train that is no square
    # wraps at the factor 0
    _, slot = carry(first[:, None] + 1 + d + along[None, :], rows, 0)
    landed = np.concatenate((first[:, None], slot), axis=1)
    # the kinetic term on every square's 00 slot from every row it does not land on, the read's factor carried
    path = np.prod(lit((row[None, None, :] - landed[:, :, None]).astype(object)), axis=1)
    clock = scale * push * trains.square[:, None] * path
    kinetic = spread(n * rows + row[None, :], (n + 1) * rows + row[None, :], clock, first[:, None])
    # each Spoke's stretch squared on the ii slot of its axis, from every row
    stretch = np.arange(n, dtype=np.intp)[None, :, None] * rows + row[None, None, :]
    grip = -push * trains.square[:, None, None] + 0 * stretch
    strain = spread(stretch, stretch, grip, slot[:, :, None])
    one, two, factor, target = np.concatenate((kinetic, strain), axis=1)
    third = 0 * one - 1  # the unit, the readings' last row
    return np.stack((one, two, third)).astype(np.intp), factor, target.astype(np.intp)


def meshing(trains: Z, c: Z, traces: Z, square: Z, kept: Z, mesh: Z) -> tuple[Z, Z, Z]:
    """Term 6's gradient vertex (FRAMES 7), the board's wave on a tied hand through the Mesh, as a plan on the plan's readings (the value, the difference along each axis, the force, the unit last): for every row of the trivial kind (A1, whose character is its own square on every turn) in a train that is no square and not the held hand (the board's wave: the held hand, Mesh-less, takes none), every row of one part of a tied train and every axis, the potential V = mesh x SUM_i C_ji M_j D_i L through the table of the tied row's kind with the kind the board's axes turn by onto A1 (found by its character, the four-vector square's on its 0i block: the dot product for T1, nothing for T2, so a pair with no such channel takes the factor 0), laid as its two pushes, (L's difference along i at L's row, unit, unit) at -mesh C_ji onto M_j's row and (M_j's difference along i at M_j's row, unit, unit) at +mesh C_ji onto L's row (the push on a gradient leg is the gradient of the other leg, one potential's two pushes; A1 x T1 has no A1 channel at the value legs, so the board's wave reaches a vector hand through the Mesh alone); mesh the strength CHOSEN in the universe file, its ground state mesh^2 below grip x 2 hold f / 2 (COUNT5 P2); the drive reads the plan, and the passing reads it split by the Spoke on the Mesh's edges (crossing), so its wind, the Mesh flux, is counted by their clicks."""
    side = c.shape[-1]
    gap = traces * traces - traces
    trivial = 1 - lit((gap * gap).sum(axis=-1))  # 1 at A1, the kind whose character is its own square
    axes = np.einsum(
        "gii->g", square[:, 1 : 1 + side, 1 : 1 + side]
    )  # the 0i block's character, the axes' own
    off = traces - axes[None, :]
    turning = 1 - lit((off * off).sum(axis=-1))  # 1 at the kind the board's axes turn by
    form = np.einsum("m,a,kamyxi->kxi", trivial, turning, c)  # each kind with the axes' kind onto A1
    # every kind: a half-speed row has no table, so it is no trivial row and, its train untied, no M row; an odd count
    # of half-speed legs has no A1 channel, so it lays no term
    every, put = widening(c, kept)
    form, trivial = np.einsum("Kk,ax,kxi->Kai", every, put, form), every @ trivial
    row, of, kind, component, offset = rows_of(trains)
    rows, axis = trains.size.sum(), np.arange(side, dtype=np.intp)
    # a gripped clock's trivial row, no square's
    scalar = trivial[kind] * trains.sourcing[of] * trains.gripped[of]
    same = 1 - lit(offset[:, None] - offset[None, :])  # 1 where the two rows are of one part
    channel = form[kind[None, :, None], component[None, :, None], axis[None, None, :]]
    factor = mesh * (scalar[:, None] * trains.tied[of][None, :] * same)[:, :, None] * channel
    lrow = np.broadcast_to(row[:, None, None], factor.shape)
    mrow = np.broadcast_to(row[None, :, None], factor.shape)
    plane = (1 + axis[None, None, :]) * rows  # the value at plane 0, the differences along i at 1 + i
    unit = 0 * lrow - 1  # the unit, the readings' last row
    onto_m = spread(plane + lrow, unit, unit, -factor, mrow)
    onto_l = spread(plane + mrow, unit, unit, factor, lrow)
    first, second, third, terms, target = np.concatenate((onto_m, onto_l), axis=1)
    return np.stack((first, second, third)).astype(np.intp), terms, target.astype(np.intp)


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
