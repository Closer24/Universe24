"""Probe B3: F1, the regulator's drive held at plus or minus the hold (tick.py:255), on the head's charts.

Parts (each a mode of the command line):
  cap N1 N2 ...      the one big bang's setting at N quanta per clock: at the first tick the drive numerator N_d and the
                     hold H = X T_d at every clock, the forms F, the quotient X1 - X0 against (4/3) n X0 / Gamma, and
                     the first tick (of 40) at which the clamp acts. It can fail: the cap is claimed at (3/4) Gamma.
  free WORLD TICKS   the head against the head with the clamp struck (the drive's numerator as held_numerator gives it),
                     in lockstep: the ticks whose state differs, the first one, and the course of each (the stretch's
                     bits, turnovers, births, chimes); the struck variant's rewind over 20 ticks.
  turn WORLD TICKS   the threshold candidate: no clamp, and a clock whose drive passes the hold turns over (law 4's
                     act, a third trigger), in lockstep with the head as above.
The clamp struck is built from the head's own source (inspect.getsource) with that one line changed; no file edited."""

import inspect
import json
import sys
import textwrap

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core.rule3 import held_numerator  # noqa: E402
from event_universe.core.spokes import AXES  # noqa: E402
from event_universe.regulation import tensor_parts  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import run_back_exact  # noqa: E402

CLAMP = "numerators = [np.minimum(np.maximum(drive, -hold), hold)]"
HEAD_CARRY, HEAD_TURNOVER = T.Tick.carry, Clock.turnover


def struck(replacement):
    src = textwrap.dedent(inspect.getsource(HEAD_CARRY))
    assert src.count(CLAMP) == 1
    assert src.startswith("def carry(self)")
    src = src.replace("def carry(self)", "def struck_carry(self)", 1).replace(CLAMP, replacement)
    space = dict(vars(T))
    exec(compile(src, "struck_carry", "exec"), space)
    return space["struck_carry"]


FREE = struck("numerators = [drive]")
# the threshold candidate: the clamp struck, the clocks past the hold marked for the turnover
TURN = struck("numerators = [drive]; clk.past_hold = (drive > hold) | (drive < -hold)")


def turnover_with_hold(self, held, going=1, top=None):
    if going == -1:
        return HEAD_TURNOVER(self, held, going, top)
    past = getattr(self, "past_hold", None)
    if past is None or not past.any():
        return HEAD_TURNOVER(self, held, going, top)
    k = self.trains_.index(self.train(REGULATOR))
    x0, x1, x2 = held[k][0].before, held[k][0].now, self.train(REGULATOR).gears[0].now
    from event_universe import readings

    xf = readings.bottom(self)
    mask = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1)) | (x0 < xf) | (x2 < xf) | past
    self.turned_over = mask
    self.counts["turns"] += int(mask.sum())
    self.turnovers.append((self.ticks, int(mask.sum())))
    self.reverse(mask, held)
    return mask


def install(mode):
    if mode == "free":
        T.Tick.carry = FREE
    elif mode == "turn":
        T.Tick.carry, Clock.turnover = TURN, turnover_with_hold


def uninstall():
    T.Tick.carry, Clock.turnover = HEAD_CARRY, HEAD_TURNOVER


def bang(n):
    calibre, piece = B.world_of("world_bang.json")
    seed = [dict(piece["seed"][0], quanta=n)]
    return Clock(calibre, {**piece, "seed": seed})


def cap(ns):
    acted = {}

    def carry(self):
        clk, k = self.clock, self.where[id(self.regulator)]
        trace, _ = tensor_parts(self.stress[:AXES])
        drive = held_numerator(clk.trace, self.stretch_now, self.forms, trace, self.rate, clk.rim, clk.full_rate)
        hold = self.stretch_now * self.trains[k][0].dteeth
        if clk.ticks == 1:
            at = (0, 0, 0)
            acted["first"] = {"forms": int(self.forms[at]), "drive": int(drive[at]), "hold": int(hold[at]),
                              "X0": int(self.stretch_now[at]), "trace of the stress": int(trace[at]),
                              "rate": int(np.asarray(self.rate)[at]) if np.ndim(self.rate) else int(self.rate)}
        if ((drive > hold) | (drive < -hold)).any() and "tick" not in acted:
            acted["tick"] = clk.ticks
        HEAD_CARRY(self)

    T.Tick.carry = carry
    for n in ns:
        acted.clear()
        clock = bang(n)
        x0 = int(clock.train(REGULATOR).gears[0].now[0, 0, 0])
        clock.tick()
        x1 = int(clock.train(REGULATOR).gears[0].now[0, 0, 0])
        first = dict(acted["first"])
        for _ in range(39):
            clock.tick()
        gamma, key = clock.full_rate, clock.key
        print(json.dumps({
            "quanta": n, "X0": x0, "X1": x1, "X1 - X0": x1 - x0,
            "(4/3) n X0 div Gamma": (4 * n * x0) // (3 * gamma),
            "forms at (0,0,0), tick 1": first["forms"], "3 forms div n": (3 * first["forms"]) // n,
            "key": key, "drive div hold at tick 1 (floor)": first["drive"] // first["hold"],
            "drive > hold at tick 1": first["drive"] > first["hold"],
            "first tick the clamp acts (of 40)": acted.get("tick"),
        }), flush=True)
    T.Tick.carry = HEAD_CARRY


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def stretch_bits(clock):
    x = clock.train(REGULATOR).gears[0].now
    return max(int(abs(int(v))).bit_length() for v in x.reshape(-1))


def lockstep(mode, world, ticks, quanta=None):
    make = (lambda: bang(quanta)) if quanta else (lambda: B.make(world))
    head, var = make(), make()
    differ, first, course = 0, None, []
    for t in range(ticks):
        uninstall()
        head.tick()
        install(mode)
        try:
            var.tick()
        except Exception as e:  # noqa: BLE001  a refusal of the struck run is a result, kept by name
            uninstall()
            course.append({"tick": t + 1, "refused": f"{type(e).__name__}: {str(e)[:120]}"})
            break
        uninstall()
        if digest(head) != digest(var):
            differ += 1
            first = t + 1 if first is None else first
        if (t + 1) % max(1, ticks // 12) == 0 or t < 6:
            course.append({"tick": t + 1, "X bits head": stretch_bits(head), "X bits variant": stretch_bits(var),
                           "turns head": head.counts["turns"], "turns variant": var.counts["turns"],
                           "births head": head.counts["births"], "births variant": var.counts["births"]})
    install(mode)
    try:
        rewind = run_back_exact(make(), min(20, ticks))
    except Exception as e:  # noqa: BLE001
        rewind = f"refused: {type(e).__name__}"
    uninstall()
    print(json.dumps({"mode": mode, "world": world, "quanta": quanta, "ticks": ticks,
                      "ticks whose state differs": differ, "first tick differing": first,
                      "rewind exact (variant)": rewind, "course": course}), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "cap":
        cap([int(x) for x in sys.argv[2:]])
    else:
        q = int(sys.argv[4]) if len(sys.argv) > 4 else None
        lockstep(sys.argv[1], sys.argv[2], int(sys.argv[3]), q)
