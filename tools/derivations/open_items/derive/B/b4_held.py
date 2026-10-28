"""Probe B4: the held field's load in D (tick.py:106) and its mass source (tick.py:229), on the one big bang
(the one calibre with a held field, universe_bang.json's row of shape 1 and weight 2).

Modes:
  head TICKS     the head unchanged; at every tick: (a) the generic held load, the load plus the contraction of every
                 train's calibre weight (0 where the file names none) with its first gear's start notch, against the
                 head's held load (must agree everywhere: the R14 form is the head's integers); (b) the masses' contraction
                 the held field reads (the trains met before it in the acts' order, R8) against the order-free one over
                 every driven train from the start board, and the sites where the two differ; (c) the held loads below
                 0 at the tick's start (F5 reached through the held field); (d) the held field's notch range.
  freerewind START N   the order-free variant's rewind of N ticks from the tick START.
  free TICKS     the held field's source from the order-free contraction (every train alike, its own mass among them),
                 in lockstep with the head: the ticks whose state differs, the first one, the course.
  energy         the two couplings of the one weight: the load's shift w phi in every spring D(c + w phi) and the source
                 T q = T carry(w M, key) on phi; the reaction the shift implies, -(1/2) dD/dphi |a|^2, over the source the
                 head writes, w D |a|^2 / key, read from the head's own rate table at several loads. It can fail: one
                 coupling (an action with its reaction) reads 1."""

import inspect
import json
import sys
import textwrap

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import hands  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.rule3 import carries  # noqa: E402

HEAD_IMPULSE = T.Tick.impulse
LINE = "q, gear.dfine = carry(r.weight * self.masses, gear.dteeth, gear.dfine, self.going)"


def order_free_mass(self):
    total = 0
    for r in self.driven:
        k = self.where[id(r)]
        total = total + carries(self.train_spring[k] * hands.dot(self.starts[k], self.starts[k]), self.train_teeth[k])
    return total


def struck_impulse():
    src = textwrap.dedent(inspect.getsource(HEAD_IMPULSE))
    assert src.count(LINE) == 1 and src.startswith("def impulse(self)")
    src = src.replace("def impulse(self)", "def struck_impulse(self)", 1)
    src = src.replace(LINE, LINE.replace("self.masses", "self._mass_all"))
    space = dict(vars(T))
    exec(compile(src, "struck_impulse", "exec"), space)
    inner = space["struck_impulse"]

    def impulse(self):
        self._mass_all = order_free_mass(self)
        inner(self)

    return impulse


FREE = struck_impulse()


def head(ticks):
    stats = {"generic held load mismatches": 0, "sites where the order-free mass differs": 0,
             "sites where the held field's own mass term is not 0": 0, "held loads below 0": 0,
             "loads below 0": 0, "clock-ticks": 0, "held notch min": 0, "held notch max": 0,
             "first tick the masses are not 0": None}

    def impulse(self):
        clock = self.clock
        generic = self.load + sum(((r.weight or 0) * self.at(r.gears[0]) for r in clock.trains_), start=0)
        stats["generic held load mismatches"] += B.n(generic != self.held_load)
        stats["held loads below 0"] += B.n(np.asarray(self.held_load) < 0)
        stats["loads below 0"] += B.n(np.asarray(self.load) < 0)
        stats["clock-ticks"] += self.load.size
        fields = [r for r in self.driven if r.weight is not None]
        before, own = 0, 0
        for r in self.driven:
            k = self.where[id(r)]
            term = carries(self.train_spring[k] * hands.dot(self.starts[k], self.starts[k]), self.train_teeth[k])
            if r is fields[0]:
                own = term
                break
            before = before + term
        total = order_free_mass(self)
        stats["sites where the order-free mass differs"] += B.n(total != before)
        stats["sites where the held field's own mass term is not 0"] += B.n(np.asarray(own) != 0)
        if stats["first tick the masses are not 0"] is None and B.n(np.asarray(before) != 0):
            stats["first tick the masses are not 0"] = clock.ticks
        phi = self.at(fields[0].gears[0])
        stats["held notch min"] = min(stats["held notch min"], int(np.min(phi)))
        stats["held notch max"] = max(stats["held notch max"], int(np.max(phi)))
        HEAD_IMPULSE(self)

    T.Tick.impulse = impulse
    clock = B.make("world_bang.json")
    for _ in range(ticks):
        clock.tick()
    T.Tick.impulse = HEAD_IMPULSE
    print(json.dumps({"mode": "head", "ticks": ticks, **stats}), flush=True)


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def free(ticks):
    a, b = B.make("world_bang.json"), B.make("world_bang.json")
    differ, first = 0, None
    for t in range(ticks):
        T.Tick.impulse = HEAD_IMPULSE
        a.tick()
        T.Tick.impulse = FREE
        b.tick()
        T.Tick.impulse = HEAD_IMPULSE
        if digest(a) != digest(b):
            differ += 1
            first = t + 1 if first is None else first
    print(json.dumps({"mode": "free", "ticks": ticks, "ticks whose state differs": differ, "first tick differing": first,
                      "counts head": {k: a.counts[k] for k in ("turns", "births", "body_clicks")},
                      "counts order-free": {k: b.counts[k] for k in ("turns", "births", "body_clicks")}}), flush=True)


def energy():
    calibre, _piece = B.world_of("world_bang.json")
    ints = calibre["integers"]
    gamma, key = int(ints["node_clock"]), int(ints["quantum_action"])
    weight = next(r["weight"] for r in calibre["rows"] if r.get("weight") is not None)
    for c in (0, 10, 100, 1000, 3000):
        p, q = rates.rate(gamma, c), rates.rate(gamma, c + weight)
        # -(1/2) dD/dphi over D, per notch of phi, from the rate table: (1/2)(1 - p(c + w)^2 / p(c)^2), as a fraction
        num, den = p * p - q * q, 2 * p * p
        # the head's source per unit of D |a|^2 (in T phi'' units): w / key
        # the ratio (num / den) / (w / key) = num key / (den w), printed as its quotient and remainder
        ratio_q, ratio_r = divmod(num * key, den * weight)
        print(json.dumps({"mode": "energy", "load": c, "weight": weight, "rate p0(c)": p, "rate p0(c + w)": q,
                          "reaction over the head's source, quotient": ratio_q,
                          "remainder over divisor": [ratio_r, den * weight],
                          "key div Gamma": key // gamma}), flush=True)


def free_rewind(start, n):
    """The order-free source's rewind: n ticks forward and back from the tick `start` (after the fittings)."""
    from tests.laws import run_back_exact

    T.Tick.impulse = FREE
    clock = B.make("world_bang.json")
    for _ in range(start):
        clock.tick()
    exact = run_back_exact(clock, n)
    T.Tick.impulse = HEAD_IMPULSE
    print(json.dumps({"mode": "freerewind", "from tick": start, "ticks": n, "rewind exact": exact}), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "freerewind":
        free_rewind(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == "head":
        head(int(sys.argv[2]))
    elif mode == "free":
        free(int(sys.argv[2]))
    else:
        energy()
