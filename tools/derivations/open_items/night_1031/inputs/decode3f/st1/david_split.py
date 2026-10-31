"""David's split as pair flows, copied whole from toys-5 4b15b8b5b,
tools/derivations/open_items/derive/david_open/node/split_d.py (NOT_CLOSED 29's seventh text, NC29b PASSED by
both readers): the value-leg monomials sorted by the trains their legs lie in, and the split at the rest as one flow
per pair of trains. Nothing here is changed; Big Pic's edge click reads split_flows alone."""

from tensor24.algebra.carry import carry

UNIT = -1
KAPPA = 6


def value(row, x):
    return 1 if row == UNIT else x[row]


def prod(xs):
    p = 1
    for v in xs:
        p *= v
    return p


class World:
    """One Node-clock's value-leg monomials sorted by the trains their legs lie in: own, two-leg between two trains,
    and tie groups (four value legs joining the held train to one other, the held legs one row squared, one group per
    tied legs and factor covering every held row); the split at the rest and the act's own X on them."""

    def __init__(self, terms, train_of, held_rows):
        self.terms = [(f, tuple(legs)) for f, legs in terms if f != 0]
        self.train_of = train_of
        self.trains = sorted(set(train_of))
        self.held_rows = tuple(held_rows)
        held = {train_of[r] for r in held_rows}
        assert len(held) == 1
        self.held_t = next(iter(held))
        self.own, self.two, groups = [], [], {}
        for f, legs in self.terms:
            vals = [h for h in legs if h != UNIT]
            owners = {train_of[h] for h in vals}
            if len(owners) == 1:
                self.own.append((f, legs))
            elif len(vals) == 2:
                self.two.append((f, legs))
            else:
                held_legs = [h for h in vals if train_of[h] == self.held_t]
                tied_legs = tuple(sorted(h for h in vals if train_of[h] != self.held_t))
                assert len(vals) == 4 and len(owners) == 2 and self.held_t in owners, legs
                assert len(held_legs) == 2 and held_legs[0] == held_legs[1], legs
                groups.setdefault((f, tied_legs), set()).add(held_legs[0])
        for key, rows in groups.items():
            assert rows == set(self.held_rows), (key, rows)
        self.groups = sorted(groups)

    def work(self, legs, f, b, a, a1):
        out = {t: 0 for t in self.trains}
        for i, g in enumerate(legs):
            if g == UNIT:
                continue
            j = -f * prod(value(h, a) for k, h in enumerate(legs) if k != i)
            out[self.train_of[g]] += j * (a1[g] - b[g])
        return out

    def excursion_work(self, c, tied, n, b, a, a1):
        p = prod(a[h] for h in tied)
        w_held = 0
        for r in self.held_rows:
            w_held += -2 * c * p * a[r] * (a1[r] - b[r])
        e = sum(a[r] * a[r] for r in self.held_rows) - n
        w_tied = 0
        for i, h in enumerate(tied):
            other = prod(a[g] for k, g in enumerate(tied) if k != i)
            w_tied += -c * other * e * (a1[h] - b[h])
        return w_held, w_tied

    def split_s(self, n, b, a, a1):
        out = {t: 0 for t in self.trains}
        half = carry(KAPPA, 2, 0)[0]
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            out[t1] += half * (w[t1] - w[t2])
            out[t2] += half * (w[t2] - w[t1])
        third = carry(KAPPA, 3, 0)[0]
        for c, tied in self.groups:
            w_held, w_tied = self.excursion_work(c, tied, n, b, a, a1)
            s_held = third * (2 * w_held - w_tied)
            out[self.held_t] += s_held
            out[self.train_of[tied[0]]] -= s_held
        return out

    def split_flows(self, n, b, a, a1):
        """The same split as pair flows: per pair of trains (t1 < t2), what passes into t1 (t2 takes its negative)."""
        out = {}
        half = carry(KAPPA, 2, 0)[0]
        for f, legs in self.two:
            w = self.work(legs, f, b, a, a1)
            t1, t2 = sorted({self.train_of[h] for h in legs if h != UNIT})
            out[(t1, t2)] = out.get((t1, t2), 0) + half * (w[t1] - w[t2])
        third = carry(KAPPA, 3, 0)[0]
        for c, tied in self.groups:
            w_held, w_tied = self.excursion_work(c, tied, n, b, a, a1)
            s_held = third * (2 * w_held - w_tied)
            t1, t2 = sorted((self.held_t, self.train_of[tied[0]]))
            out[(t1, t2)] = out.get((t1, t2), 0) + (s_held if t1 == self.held_t else -s_held)
        return out

    def act_x(self, x, y, terms):
        out = {t: 0 for t in self.trains}
        for f, legs in terms:
            for i, g in enumerate(legs):
                if g == UNIT:
                    continue
                oy = prod(value(h, y) for k, h in enumerate(legs) if k != i)
                ox = prod(value(h, x) for k, h in enumerate(legs) if k != i)
                out[self.train_of[g]] += -f * (x[g] * oy - y[g] * ox)
        return out
