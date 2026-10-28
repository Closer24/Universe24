"""Draft C's drives for the regulator's time gear, installed into a source tree's tick.Tick.carry by the harness.
The carry below is the head's tick.Tick.carry (S/t24/src/event_universe/tick.py:246-287) line for line, with its
first numerator (the time gear's drive) taken from the named drive function; every other line as the head's.
A drive function gets the Tick and the stress's trace and returns the time gear's numerator at every Node-clock.
Every drive also logs, at the Node-clock (0, 0, 0), the integers it read: TRACE[-1] = (X, forms, trace, rate, N, hold)."""
import numpy as np

TRACE = []
NO_RESTORE = {"vol0_free"}  # the drives run with BH-S1's restore of a stopped clock's gears struck (R10's "a zero, with no restore")


def head(tick, trace):
    """The head: held_numerator clamped at plus and minus the hold (E10, F1)."""
    from event_universe.core.rule3 import held_numerator

    clk = tick.clock
    k = tick.where[id(tick.regulator)]
    drive = held_numerator(clk.trace, tick.stretch_now, tick.forms, trace, tick.rate, clk.rim, clk.full_rate)
    hold = tick.stretch_now * tick.trains[k][0].dteeth
    return np.minimum(np.maximum(drive, -hold), hold), drive, hold


def nocap(tick, trace):
    """The head's held_numerator with the clamp F1 struck."""
    from event_universe.core.rule3 import held_numerator

    clk = tick.clock
    k = tick.where[id(tick.regulator)]
    drive = held_numerator(clk.trace, tick.stretch_now, tick.forms, trace, tick.rate, clk.rim, clk.full_rate)
    hold = tick.stretch_now * tick.trains[k][0].dteeth
    return drive, drive, hold


DRIVES = {"head": head, "nocap": nocap}


def install(T, name, extra=None):
    """Replace T.Tick.carry by the head's carry with the named time gear drive."""
    from event_universe import readings
    from event_universe.core.acts import carry as carry_act, mid
    from event_universe.core.spokes import AXES
    from event_universe.regulation import tensor_parts
    from event_universe.trains import Gear

    if extra:
        DRIVES.update(extra)
    drive_of = DRIVES[name]
    install_impulse(T)
    keep_spring = SPRING.get(name, True)

    def carry(self):
        clk, regulator = self.clock, self.regulator
        k = self.where[id(regulator)]
        p02, (trace, traceless) = self.rate * self.rate, tensor_parts(self.stress[:AXES])
        first, raw, hold = drive_of(self, trace)
        at = (0,) * len(clk.size)
        TRACE.append(
            (
                clk.ticks,
                self.going,
                int(np.asarray(self.stretch_now)[at]),
                int(np.asarray(self.forms)[at]),
                int(np.asarray(trace)[at]),
                int(np.asarray(self.rate)[at]),
                int(np.asarray(raw)[at]),
                int(np.asarray(hold)[at]),
                int(np.asarray(self.kin_num)[at]),
                int(np.asarray(self.grad_num)[at]),
                int(np.asarray(self.mass_num)[at]),
            )
        )
        numerators = [first]
        numerators += [part * p02 for part in (*traceless, *self.stress[AXES:])]
        gearing = regulator_gearing(self, keep_spring)
        self.out[k] = clk.act(self.trains[k], gearing, None, numerators, self.going, None, *self.ends(regulator))[-1]
        w_div = self.end_teeth(self.out[k][0])
        for r in self.driven:
            k = self.where[id(r)]
            new = []
            for a, p, gear in zip(self.starts[k], self.impelled[k], self.trains[k], strict=True):
                v, fine = carry_act(p, w_div, mid(w_div))
                now, before = (a + self.going * v, a)[:: self.going]
                new.append(Gear(now, before, fine, w_div, gear.dfine, gear.dteeth))
            if self.going == -1 and self.kept is not None:
                clk.restore(new, self.kept[k], self.top)
            self.out[k] = new
            if r in self.hands:
                start = self.trains[k] if self.going == 1 else new
                after = new if self.going == 1 else self.held[k]
                self.hand_starts.append(list(start))
                self.before_turnover.append([gear.copy() for gear in after])
        clk.before_turnover = self.before_turnover
        clk.set_trains(self.out)
        if self.going == 1:
            self.advances()
        if self.going == -1 and self.kept is not None:
            clk.restore(clk.all_gears(), [gear for train in self.kept for gear in train], self.stopped & self.top)
        if name not in NO_RESTORE:
            clk.restore(clk.all_gears(), [gear for train in self.held for gear in train], self.stopped & ~self.top)

    T.Tick.carry = carry


def install_impulse(T):
    """Replace T.Tick.impulse by the head's impulse (S/t24/src/event_universe/tick.py:203-244) line for line, with three
    readings booked beside the head's forms, each the exact integer sum over every driven train and gear before any carry:
    self.kin_num (the kinetic products u_in u_out), self.grad_num (the gradient's potential, -a pull - D a a, over the
    train's teeth) and self.mass_num (the springs' potential D a a over the train's teeth); the head's integers unchanged."""
    from event_universe import hands, readings
    from event_universe.core import rates
    from event_universe.core.acts import carry, mid
    from event_universe.core.rule3 import carries
    from event_universe.meshes import coupling_of, cross
    from event_universe.regulation import stress_of
    from event_universe.trains import REGULATOR, zeros

    def impulse(self):
        clock = self.clock
        self.forms = zeros(clock.size)
        self.kin_num = zeros(clock.size)
        self.grad_num = zeros(clock.size)
        self.mass_num = zeros(clock.size)
        self.impelled = {}
        d = (clock.teeth + clock.teeth) * self.stretch_now
        w_side = readings.mean_teeth(self.clock, self.regulator.gears[0])
        sweep = zeros(clock.size)
        self.stress = [zeros(clock.size) for _ in range(REGULATOR - 1)]
        self.masses = zeros(clock.size)
        for r in self.driven:
            k = self.where[id(r)]
            p_side = [w_side * (gear.now - gear.before) + gear.fine - mid(w_side) for gear in self.trains[k]]
            p_other = [p + self.going * self.stretch_now * f for p, f in zip(p_side, self.pull[k], strict=True)]
            if r is self.offset:
                clock.start_kicks = []
                for a, (gear, n) in enumerate(zip(self.trains[k], [sweep, *self.lead], strict=True)):
                    q, gear.dfine = carry(n, gear.dteeth, gear.dfine, self.going)
                    p_other[a] = p_other[a] + self.going * clock.teeth * self.stretch_now * q
                    clock.start_kicks.append(q)
            if r.weight is not None:
                gear = self.trains[k][0]
                q, gear.dfine = carry(r.weight * self.masses, gear.dteeth, gear.dfine, self.going)
                p_other[0] = p_other[0] + self.going * clock.teeth * self.stretch_now * q
            u_in = [rates.rounded(p + p + 1, d) for p in p_side]
            u_out = [rates.rounded(p + p + 1, d) for p in p_other]
            if r in self.hands:
                velocity = [x + y for x, y in zip(u_in, u_out, strict=True)]
                sweep = sweep + coupling_of(r) * cross(*velocity, *self.starts[k])
                found = stress_of(self.starts[k], velocity)
                self.stress = [s + r.ratio[0] * t for s, t in zip(self.stress, found, strict=True)]
            mass = self.train_spring[k] * hands.dot(self.starts[k], self.starts[k])
            self.masses = self.masses + carries(mass, self.train_teeth[k])
            pulls = hands.products(self.starts[k], self.pull[k])
            for product, pull in zip(hands.products(u_in, u_out), pulls, strict=True):
                self.forms = self.forms + product + carries(-pull, self.train_teeth[k])
                self.kin_num = self.kin_num + product
            for a, pull in zip(self.starts[k], pulls, strict=True):
                own = self.train_spring[k] * a * a
                self.grad_num = self.grad_num - pull - own
                self.mass_num = self.mass_num + own
            self.impelled[k] = p_other

    T.Tick.impulse = impulse


def regulator_gearing(tick, spring):
    """The regulator's gearing as the head reads it, or with its spring struck (David's item (c)): the hold 2 w - SUM R_j."""
    from event_universe import readings
    from event_universe.core.rule3 import Gearing

    g = readings.gearing_of(tick.clock, tick.regulator, tick.load, tick.factors)
    if spring:
        return g
    return Gearing(g.grips, g.teeth + g.teeth - sum(g.grips), g.teeth, 0)


def vol_push(tick):
    """GR's A1 volume equation in the head's own gauge (N = 1/a, X = Gamma a^4): X'' = kappa X (F - S/3), with F - S/3 =
    (4/3) G + 2 V, the gradient's and the springs' potential: here kappa = 3 / (Gamma key), so that q = X ((d+1) G +
    2d V) / (Gamma key) over the head's drive teeth t rim Gamma^4 key; G and V the exact sums carried once at the teeth."""
    from event_universe.core.rule3 import carries
    from event_universe.core.spokes import AXES, SPOKES

    clk = tick.clock
    grad = carries(tick.grad_num, clk.teeth)
    mass = carries(tick.mass_num, clk.teeth)
    weight = clk.trace * clk.rim * clk.full_rate * clk.full_rate * clk.full_rate
    return tick.stretch_now * ((AXES + 1) * grad + SPOKES * mass) * weight


def vol0(tick, trace):
    """GR's volume push, the time gear's spring struck (item c), no clamp, no curvature: push only."""
    n = vol_push(tick)
    return n, n, n * 0


def volL(tick, trace):
    """GR's volume push with the regulator's spring kept as the head has it: in the A1 course a negative Lambda."""
    n = vol_push(tick)
    return n, n, n * 0


SPRING = {"head": True, "nocap": True, "vol0": False, "volL": True, "nocap0": False}


def nocap0(tick, trace):
    """The head's held_numerator, the clamp struck and the time gear's spring struck."""
    return nocap(tick, trace)


DRIVES.update({"vol0": vol0, "volL": volL, "nocap0": nocap0})


BRAKES = {}


def residual_brake(tick, part_num, part_den):
    """The A1 Friedmann constraint's residual of the seed, held: 8 Gamma k = (d+1) X F / (Gamma key) - (X - X-)^2 / (2 X)
    at the first tick forward (the seed), F the head's forms (the whole wind), kept per Node-clock and per clock (the
    rewind's fresh clock reads its own seed alike); scaled by part_num / part_den (1 / 1 the seed's own residual; any
    other fraction a declaration). Returns the brake b in notches per tick, at every Node-clock."""
    from event_universe.core.rule3 import carries
    from event_universe.core.spokes import AXES

    clk = tick.clock
    key = id(clk)
    if key not in BRAKES:
        gear = tick.regulator.gears[0]
        x, xb = tick.stretch_now, gear.before
        push = carries((AXES + 1) * x * tick.forms, clk.full_rate * clk.key)
        velocity = carries((x - xb) * (x - xb), x + x)
        BRAKES[key] = carries((push - velocity) * part_num, part_den)
    return BRAKES[key]


def volR(tick, trace):
    """GR's volume push with the seed's own constraint residual held as the curvature brake (the R_00 form's first
    integral): X'' = push - 8 Gamma k, k the seed's; the time gear's spring struck."""
    k = tick.where[id(tick.regulator)]
    td = tick.trains[k][0].dteeth
    n = vol_push(tick) - residual_brake(tick, 1, 1) * td
    return n, n, n * 0


def volK2(tick, trace):
    """GR's volume push with half the seed's residual as the curvature brake (a declared k): the time gear's spring struck."""
    k = tick.where[id(tick.regulator)]
    td = tick.trains[k][0].dteeth
    n = vol_push(tick) - residual_brake(tick, 1, 2) * td
    return n, n, n * 0


DRIVES.update({"volR": volR, "volK2": volK2})
SPRING.update({"volR": False, "volK2": False})


def seed_velocity(clock):
    """The seed's time gear given a velocity: its before notch at X - Gamma div 2 at every Node-clock (a seed integer the
    world file would declare; the probe's), so that the seed is overdense, k > 0, and rises."""
    from event_universe.core.rule3 import half
    from event_universe.trains import REGULATOR

    gear = clock.train(REGULATOR).gears[0]
    gear.before[:] = gear.now - half(clock.full_rate)


def volRv(tick, trace):
    """GR's 00 form as the volume push with the seed's own constraint residual held, on a seed with a velocity."""
    return volR(tick, trace)


PREPARE = {"volRv": seed_velocity}
DRIVES.update({"volRv": volRv})
SPRING.update({"volRv": False})


def vol0_free(tick, trace):
    """The derived push, the time gear's spring struck, and BH-S1's restore of a stopped clock struck (R10's zero)."""
    return vol0(tick, trace)


DRIVES.update({"vol0_free": vol0_free})
SPRING.update({"vol0_free": False})
