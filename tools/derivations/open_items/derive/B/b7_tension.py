"""Probe B7: F2, the Mesh's tension held in [0, Gamma] (meshes.py:74), its two sides apart.

Modes:
  cone WORLD TICKS   the head unchanged; at every tick's start, at every clock: the light's hold S = 2w - SUM_j R_j
                     (the step's edge for the spring-0 hand, DAVID-LIGHT-CONE.md) and every gapped hand's edge
                     4w - D - 2 SUM_j R_j, read with the head's factors and with the factors whose tension below 0 is
                     read as itself (the lower clamp struck, the upper kept); the clocks past the edge in each; the
                     tensions' trace at a clock, |n_x + n_y + n_z|, against the largest |n_a| (the drive is traceless).
                     It can fail: the head's factors are claimed never past the edge, the struck ones past it.
  upper              the upper side as the tension's carry at the full rate: Q(t) = mesh_factor(t) (1 div (1 + t div
                     Gamma)) against the head's mesh_factor(min(max(t, 0), Gamma)), every t in [0, 5 Gamma] at the
                     toy's Gamma and G, and at random Gamma; and the same spelling below 0, where it is no factor.
  lockstep WORLD TICKS   the lower clamp struck against the head: the ticks whose state differs, the first one, the
                     course, the rewind of 20 from the setting.
No file edited: the struck factors are meshes.factors' own lines with max(t, 0) left out, installed in tick's namespace."""

import json
import random
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.core.rule3 import carries, mesh_factor, mesh_unit_of  # noqa: E402
from event_universe.core.spokes import AXES, SIDES, SPOKE_SIDES, across  # noqa: E402
from event_universe.meshes import even  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import run_back_exact  # noqa: E402

HEAD_FACTORS, HEAD_RATE = T.factors, T.Tick.rate_readings


def struck_factors(clock, axis_notches=None, stopped=None):
    """meshes.factors with the tension below 0 read as itself (the upper side kept at Gamma)."""
    notches = [g.now for g in clock.train(REGULATOR).gears[1:1 + AXES]] if axis_notches is None else axis_notches
    found = []
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        t = carries(even(notches[axis], spoke) + 1, SIDES)
        factor = mesh_factor(clock.full_rate, clock.G, np.minimum(t, clock.full_rate))
        at_teeth = None if stopped is None else stopped | across(stopped, spoke)
        found.append(factor if at_teeth is None else np.where(at_teeth, 0, factor))
    return tuple(found)


def cone(world, ticks):
    st = {"clock-ticks": 0, "light past its edge, head": 0, "light past its edge, struck": 0,
          "matter past its edge, head": 0, "matter past its edge, struck": 0,
          "clocks with a tension below 0": 0, "largest |n_x + n_y + n_z|": 0, "largest |n_a|": 0,
          "largest light grips over the vacuum's, struck (quotient)": 0}

    def rate_readings(self):
        HEAD_RATE(self)
        clock = self.clock
        axis = [self.at(g) for g in self.regulator.gears[1:1 + AXES]]
        st["clock-ticks"] += self.load.size
        trace = axis[0] + axis[1] + axis[2]
        st["largest |n_x + n_y + n_z|"] = max(st["largest |n_x + n_y + n_z|"], int(np.max(np.abs(trace))))
        st["largest |n_a|"] = max(st["largest |n_a|"], max(int(np.max(np.abs(a))) for a in axis))
        struck = struck_factors(clock, axis, self.stopped)
        below = np.zeros(clock.size, dtype=bool)
        for spoke, (a, _s) in enumerate(SPOKE_SIDES):
            below |= carries(even(axis[a], spoke) + 1, SIDES) < 0
        st["clocks with a tension below 0"] += B.n(below)
        for r in clock.hands():
            for name, fac in (("head", self.factors), ("struck", struck)):
                g = readings.gearing_of(clock, r, self.load, fac)
                if r.spring == 0:
                    st[f"light past its edge, {name}"] += B.n(np.asarray(g.hold) < 0)
                    if name == "struck":
                        vac = readings.gearing_of(clock, r, self.load * 0, None)
                        ratio = max(int(x) for x in (np.asarray(sum(g.grips)) // sum(vac.grips)).reshape(-1))
                        key = "largest light grips over the vacuum's, struck (quotient)"
                        st[key] = max(st[key], ratio)
                else:
                    edge = 4 * g.teeth - g.spring - 2 * sum(g.grips)
                    st[f"matter past its edge, {name}"] += B.n(np.asarray(edge) < 0)

    T.Tick.rate_readings = rate_readings
    clock = B.make(world)
    for _ in range(ticks):
        clock.tick()
    T.Tick.rate_readings = HEAD_RATE
    print(json.dumps({"mode": "cone", "world": world, "ticks": ticks, **st}), flush=True)


def upper():
    out = {}
    for gamma in (1000, 6000, 23057):
        g = mesh_unit_of(gamma)
        same = sum(
            int(mesh_factor(gamma, g, t) * (1 // (1 + t // gamma))) == int(mesh_factor(gamma, g, min(max(t, 0), gamma)))
            for t in range(0, 5 * gamma + 1)
        )
        below = [t for t in range(-3, 0)]
        out[f"Gamma {gamma}"] = {"t in [0, 5 Gamma] equal": f"{same} of {5 * gamma + 1}",
                                 "below 0: 1 + t div Gamma": [1 + t // gamma for t in below]}
    rng = random.Random(3)
    agree = 0
    for _ in range(20000):
        gamma = rng.randrange(2, 10**6)
        g = mesh_unit_of(gamma) if gamma < 5000 else 16
        t = rng.randrange(0, 4 * gamma)
        agree += int(mesh_factor(gamma, g, t) * (1 // (1 + t // gamma))) == int(mesh_factor(gamma, g, min(t, gamma)))
    out["random (Gamma, t >= 0)"] = f"{agree} of 20000"
    print(json.dumps({"mode": "upper", **out}), flush=True)


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def lockstep(world, ticks):
    a, b = B.make(world), B.make(world)
    differ, first, course = 0, None, []
    for t in range(ticks):
        T.factors = HEAD_FACTORS
        a.tick()
        T.factors = struck_factors
        try:
            b.tick()
        except Exception as e:  # noqa: BLE001  a refusal is a result
            course.append({"tick": t + 1, "refused": f"{type(e).__name__}: {str(e)[:100]}"})
            T.factors = HEAD_FACTORS
            break
        T.factors = HEAD_FACTORS
        try:
            same = digest(a) == digest(b)
        except ValueError as e:  # an integer of the struck run past 4,300 decimal digits: the runaway, kept by name
            bits = max(int(abs(int(v))).bit_length() for v in b.train(REGULATOR).gears[0].now.reshape(-1))
            course.append({"tick": t + 1, "struck X bits": bits, "stopped": f"{type(e).__name__}: {str(e)[:60]}"})
            differ += 1
            break
        if not same:
            differ += 1
            first = t + 1 if first is None else first
        if t < 5 or (t + 1) % max(1, ticks // 10) == 0:
            bits = [max(int(abs(int(v))).bit_length() for v in c.train(REGULATOR).gears[0].now.reshape(-1)) for c in (a, b)]
            course.append({"tick": t + 1, "X bits head/struck": bits, "turns": [a.counts["turns"], b.counts["turns"]],
                           "births": [a.counts["births"], b.counts["births"]]})
    T.factors = struck_factors
    try:
        rewind = run_back_exact(B.make(world), min(20, ticks))
    except Exception as e:  # noqa: BLE001
        rewind = f"refused: {type(e).__name__}"
    T.factors = HEAD_FACTORS
    print(json.dumps({"mode": "lockstep", "world": world, "ticks": ticks, "ticks whose state differs": differ,
                      "first tick differing": first, "rewind (struck)": rewind, "course": course}), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "cone":
        cone(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "upper":
        upper()
    else:
        lockstep(sys.argv[2], int(sys.argv[3]))
