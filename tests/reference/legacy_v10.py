"""Strict integer-only 3D local event-field simulator core (v7).

HARD INVARIANTS
- Core dynamic state and physical update arithmetic use integers only.
- No float literals, true division, trig, sqrt, log, or vector normalization in the core.
- Every cell has a fixed-size state independent of particle/source count.
- Every local field update reads exactly six nearest neighbours: +/-x, +/-y, +/-z.
- Every occupied cell has a fixed particle-slot capacity K.
- One movement law is used at every speed; c_units is the universal integer speed cap.
- A stationary particle is a persistent source by occupancy, never repeated += emission.
- A field change propagates locally by at most one lattice edge per tick.
- Matter-field momentum exchange is local and exactly equal/opposite in integers.
- The 3D simulator can be inspected through a 2D XY slice at any integer z; slicing is diagnostic only.

This is a discrete scalar-field research simulator, not derived general relativity.
The field relaxation law remains provisional and is deliberately isolated in _field_step().
"""
from dataclasses import dataclass, asdict
from collections import defaultdict
import ast
import json

# Six cardinal directions in 3D.
PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)
DIRECTIONS = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)
MAX_CORE_INT = 2147483647


def checked(v):
    """Require one bounded core integer and return it unchanged."""
    if type(v) is not int:
        raise TypeError("core state must remain integer")
    if v < -MAX_CORE_INT or v > MAX_CORE_INT:
        raise OverflowError("fixed-width core integer range exceeded")
    return v


@dataclass(frozen=True)
class Config:
    """All simulator-core parameters are integers and documented here."""
    nx: int = 240
    ny: int = 240
    nz: int = 240
    c_units: int = 1000
    source_strength: int = 64
    # In 3D there are six neighbours. field_den=7 is the direct degree+1
    # analogue of the old 2D field_den=5. It is a provisional field-law choice.
    field_den: int = 7
    force_num: int = 1
    force_den: int = 64
    max_particles_per_cell: int = 4

    def __post_init__(self):
        values = (
            self.nx, self.ny, self.nz, self.c_units, self.source_strength,
            self.field_den, self.force_num, self.force_den,
            self.max_particles_per_cell,
        )
        if not all(type(v) is int for v in values):
            raise TypeError("all simulator configuration values must be integers")
        if min(self.nx, self.ny, self.nz, self.c_units, self.field_den,
               self.force_den, self.max_particles_per_cell) < 1:
            raise ValueError("positive integer configuration required")
        if self.source_strength < 0 or self.force_num < 0:
            raise ValueError("non-negative source/coupling required")


# Fixed cell state: scalar field, three field-momentum components, exact division remainder.
PHI, FIELD_PX, FIELD_PY, FIELD_PZ, FIELD_REM = range(5)
CELL_REGISTERS = 5

# Fixed particle state: position, momentum, movement budget, digital-axis phase,
# and exact force-division remainders in each axis.
X, Y, Z, PX, PY, PZ, MOVE_BUDGET, AXIS_PHASE, FORCE_RX, FORCE_RY, FORCE_RZ, LAST_UPDATE_TICK = range(12)
PARTICLE_REGISTERS = 12


def signed_divrem(n, d):
    """Integer quotient toward zero plus exact integer remainder."""
    if n >= 0:
        q = n // d
    else:
        q = -((-n) // d)
    return q, n - q * d


class IntegerO1Field3D:
    """Sparse 3D simulator with fixed-state, six-neighbour local physics."""

    def __init__(self, config=Config()):
        self.config = config
        self.cells = {}          # (x,y,z) -> fixed list[int] of CELL_REGISTERS
        self.occupancy = {}      # (x,y,z) -> fixed list[int] of K particle ids
        self.particles = {}      # id -> fixed list[int] of PARTICLE_REGISTERS
        self.active = set()      # sparse scheduler; not part of one-cell physical state
        self.tick = 0
        self.paths = defaultdict(list)
        self.collisions = []
        self.force_records = []

    def addr(self, x, y, z):
        """Periodic 3D address. Coordinates are always integer lattice cells."""
        return (x % self.config.nx, y % self.config.ny, z % self.config.nz)

    def _cell(self, p):
        p = self.addr(*p)
        state = self.cells.get(p)
        if state is None:
            state = [0, 0, 0, 0, 0]
            self.cells[p] = state
        return state

    def _slots(self, p):
        p = self.addr(*p)
        slots = self.occupancy.get(p)
        if slots is None:
            slots = [-1] * self.config.max_particles_per_cell
            self.occupancy[p] = slots
        return slots

    def _source_count(self, p):
        slots = self.occupancy.get(self.addr(*p))
        if slots is None:
            return 0
        count = 0
        # K is a fixed model constant, so this loop is O(1) per cell.
        for i in range(self.config.max_particles_per_cell):
            if slots[i] >= 0:
                count += 1
        return count

    def _insert(self, pid, p):
        slots = self._slots(p)
        for i in range(self.config.max_particles_per_cell):
            if slots[i] < 0:
                slots[i] = pid
                return True
        return False

    def _remove(self, pid, p):
        slots = self._slots(p)
        for i in range(self.config.max_particles_per_cell):
            if slots[i] == pid:
                slots[i] = -1
                return True
        return False

    def add_particle(self, pid, x, y, z, px=0, py=0, pz=0):
        values = (pid, x, y, z, px, py, pz)
        if not all(type(v) is int for v in values):
            raise TypeError("particle id/position/momentum must be integers")
        if pid in self.particles:
            raise ValueError("duplicate particle id")
        p = self.addr(x, y, z)
        if not self._insert(pid, p):
            raise ValueError("cell particle capacity exceeded")
        self.particles[pid] = [p[0], p[1], p[2], px, py, pz, 0, 0, 0, 0, 0, -1]
        self.paths[pid].append((self.tick, p[0], p[1], p[2]))
        self._activate_with_neighbors(p)
        return self

    def _activate_with_neighbors(self, p):
        p = self.addr(*p)
        self.active.add(p)
        x, y, z = p
        for dx, dy, dz in DIRECTIONS:
            self.active.add(self.addr(x + dx, y + dy, z + dz))

    def phi(self, p):
        state = self.cells.get(self.addr(*p))
        return 0 if state is None else state[PHI]

    def _neighbor_phis(self, p, old_phi):
        x, y, z = p
        out = [0, 0, 0, 0, 0, 0]
        for d in range(6):
            dx, dy, dz = DIRECTIONS[d]
            out[d] = old_phi.get(self.addr(x + dx, y + dy, z + dz), 0)
        return out

    def _field_step(self):
        """One synchronous local field update over the sparse active frontier."""
        work = set(self.active)
        for p in tuple(self.active):
            x, y, z = p
            for dx, dy, dz in DIRECTIONS:
                work.add(self.addr(x + dx, y + dy, z + dz))

        old_phi = {}
        for p in work:
            state = self.cells.get(p)
            old_phi[p] = 0 if state is None else state[PHI]

        next_active = set()
        updates = []
        c = self.config
        for p in work:
            state = self._cell(p)
            sides = self._neighbor_phis(p, old_phi)
            rho = self._source_count(p)
            # Provisional 3D screened-Poisson relaxation:
            # phi_new = (sum6 + source_strength*rho + carried_remainder) / field_den
            # The exact remainder is retained, so no fractional state is discarded.
            raw = sum(sides) + c.source_strength * rho + state[FIELD_REM]
            phi_new, rem_new = signed_divrem(raw, c.field_den)
            if phi_new < 0:
                phi_new = 0
                rem_new = 0
            changed = phi_new != state[PHI]
            updates.append((p, phi_new, rem_new, changed, rho))

        self.active = set()
        for p, phi_new, rem_new, changed, rho in updates:
            state = self._cell(p)
            state[PHI] = checked(phi_new)
            state[FIELD_REM] = checked(rem_new)
            if changed or rho:
                next_active.add(p)

        for p in next_active:
            self._activate_with_neighbors(p)

    def _gradient(self, p):
        """Six-neighbour central difference without division: right-left on each axis."""
        x, y, z = p
        plus_x = self.phi(self.addr(x + 1, y, z))
        minus_x = self.phi(self.addr(x - 1, y, z))
        plus_y = self.phi(self.addr(x, y + 1, z))
        minus_y = self.phi(self.addr(x, y - 1, z))
        plus_z = self.phi(self.addr(x, y, z + 1))
        minus_z = self.phi(self.addr(x, y, z - 1))
        return plus_x - minus_x, plus_y - minus_y, plus_z - minus_z

    @staticmethod
    def _choose_axis(px, py, pz, phase):
        """Choose one of six cardinal hops from integer momentum ratios only."""
        ax, ay, az = abs(px), abs(py), abs(pz)
        total = ax + ay + az
        if total == 0:
            return -1, phase
        phase %= total
        slot = phase
        phase += 1
        if phase >= total:
            phase = 0
        if slot < ax:
            return (PLUS_X if px >= 0 else MINUS_X), phase
        if slot < ax + ay:
            return (PLUS_Y if py >= 0 else MINUS_Y), phase
        return (PLUS_Z if pz >= 0 else MINUS_Z), phase

    def _particle_step_in_cell(self, p):
        """Update every fixed particle slot in one cell with constant local work."""
        p = self.addr(*p)
        slots = self.occupancy.get(p)
        if slots is None:
            return
        c = self.config
        for slot in range(c.max_particles_per_cell):
            pid = slots[slot]
            if pid < 0:
                continue
            s = self.particles[pid]
            # A particle can enter a cell that also appears later in the occupancy
            # snapshot. This register guarantees exactly one physical update per tick.
            if s[LAST_UPDATE_TICK] == self.tick:
                continue
            s[LAST_UPDATE_TICK] = self.tick
            gx, gy, gz = self._gradient(p)

            # DISCRETE TURNING LAW:
            # A field imbalance parallel to the particle's current dominant motion
            # axis cannot rotate that motion. Only transverse neighbour imbalance
            # changes direction. This prevents an isolated mover's trailing own
            # scalar field from creating artificial longitudinal self-drag, while
            # preserving the raw six-neighbour field and all integer arithmetic.
            ax, ay, az = abs(s[PX]), abs(s[PY]), abs(s[PZ])
            if ax >= ay and ax >= az and ax != 0:
                turn_gx, turn_gy, turn_gz = 0, gy, gz
            elif ay >= az and ay != 0:
                turn_gx, turn_gy, turn_gz = gx, 0, gz
            elif az != 0:
                turn_gx, turn_gy, turn_gz = gx, gy, 0
            else:
                turn_gx, turn_gy, turn_gz = gx, gy, gz

            raw_x = c.force_num * turn_gx + s[FORCE_RX]
            raw_y = c.force_num * turn_gy + s[FORCE_RY]
            raw_z = c.force_num * turn_gz + s[FORCE_RZ]
            ix, rx = signed_divrem(raw_x, c.force_den)
            iy, ry = signed_divrem(raw_y, c.force_den)
            iz, rz = signed_divrem(raw_z, c.force_den)
            s[FORCE_RX], s[FORCE_RY], s[FORCE_RZ] = rx, ry, rz

            old_px, old_py, old_pz = s[PX], s[PY], s[PZ]
            s[PX] = checked(s[PX] + ix)
            s[PY] = checked(s[PY] + iy)
            s[PZ] = checked(s[PZ] + iz)

            # Exact local exchange: matter impulse and field impulse are equal/opposite.
            cell = self._cell(p)
            cell[FIELD_PX] = checked(cell[FIELD_PX] - ix)
            cell[FIELD_PY] = checked(cell[FIELD_PY] - iy)
            cell[FIELD_PZ] = checked(cell[FIELD_PZ] - iz)

            self.force_records.append(
                (self.tick, pid, p[0], p[1], p[2], gx, gy, gz, ix, iy, iz,
                 old_px, old_py, old_pz, s[PX], s[PY], s[PZ]))

            # L1 speed is an integer digital speed. min() is the universal c cap,
            # not a separate low/high-speed law.
            speed = min(abs(s[PX]) + abs(s[PY]) + abs(s[PZ]), c.c_units)
            s[MOVE_BUDGET] = checked(s[MOVE_BUDGET] + speed)
            if s[MOVE_BUDGET] < c.c_units:
                continue
            s[MOVE_BUDGET] -= c.c_units

            d, phase = self._choose_axis(s[PX], s[PY], s[PZ], s[AXIS_PHASE])
            s[AXIS_PHASE] = phase
            if d < 0:
                continue
            dx, dy, dz = DIRECTIONS[d]
            target = self.addr(p[0] + dx, p[1] + dy, p[2] + dz)
            target_slots = self._slots(target)
            free = -1
            for j in range(c.max_particles_per_cell):
                if target_slots[j] < 0:
                    free = j
                    break
            if free < 0:
                self.collisions.append((self.tick, pid, target[0], target[1], target[2]))
                continue

            # Atomic occupancy move. The old source stops here; the new source starts
            # at target on the next field update. No repeated source accumulation exists.
            slots[slot] = -1
            target_slots[free] = pid
            s[X], s[Y], s[Z] = target
            self.paths[pid].append((self.tick, target[0], target[1], target[2]))
            self._activate_with_neighbors(p)
            self._activate_with_neighbors(target)

    def step(self):
        self._field_step()
        # A snapshot prevents newly created occupancy keys from changing this tick's loop.
        occupied = tuple(self.occupancy.keys())
        for p in occupied:
            self._particle_step_in_cell(p)
        self.tick = checked(self.tick + 1)
        return self

    def run(self, ticks):
        if type(ticks) is not int or ticks < 0:
            raise TypeError("ticks must be a non-negative integer")
        for _ in range(ticks):
            self.step()
        return self

    def total_particle_momentum(self):
        px = 0
        py = 0
        pz = 0
        for s in self.particles.values():
            px += s[PX]
            py += s[PY]
            pz += s[PZ]
        return px, py, pz

    def total_field_momentum(self):
        px = 0
        py = 0
        pz = 0
        for state in self.cells.values():
            px += state[FIELD_PX]
            py += state[FIELD_PY]
            pz += state[FIELD_PZ]
        return px, py, pz

    def total_momentum(self):
        a = self.total_particle_momentum()
        b = self.total_field_momentum()
        return a[0] + b[0], a[1] + b[1], a[2] + b[2]

    # ---------- Diagnostics below: not part of the local physical law ----------
    def xy_slice(self, z):
        """Return sparse { (x,y): phi } for one integer z-plane."""
        if type(z) is not int:
            raise TypeError("slice z must be an integer")
        zz = z % self.config.nz
        out = {}
        for (x, y, cell_z), state in self.cells.items():
            if cell_z == zz and state[PHI] != 0:
                out[(x, y)] = state[PHI]
        return out

    def particles_on_xy_slice(self, z):
        """Return particle positions/momenta on one integer z-plane."""
        if type(z) is not int:
            raise TypeError("slice z must be an integer")
        zz = z % self.config.nz
        out = []
        for pid, s in self.particles.items():
            if s[Z] == zz:
                out.append((pid, s[X], s[Y], s[PX], s[PY], s[PZ]))
        return out

    def audit(self):
        c = self.config
        assert all(len(state) == CELL_REGISTERS for state in self.cells.values())
        assert all(type(v) is int and -MAX_CORE_INT <= v <= MAX_CORE_INT
                   for state in self.cells.values() for v in state)
        assert all(len(state) == PARTICLE_REGISTERS for state in self.particles.values())
        assert all(type(v) is int and -MAX_CORE_INT <= v <= MAX_CORE_INT
                   for state in self.particles.values() for v in state)
        assert all(len(slots) == c.max_particles_per_cell for slots in self.occupancy.values())
        assert all(type(v) is int for slots in self.occupancy.values() for v in slots)
        for pid, s in self.particles.items():
            slots = self.occupancy.get((s[X], s[Y], s[Z]), ())
            assert pid in slots
        return True

    def report(self):
        self.audit()
        return {
            "tick": self.tick,
            "config": asdict(self.config),
            "particles": len(self.particles),
            "active_cells": len(self.active),
            "materialized_cells": len(self.cells),
            "cell_registers": CELL_REGISTERS,
            "particle_registers": PARTICLE_REGISTERS,
            "particle_momentum": self.total_particle_momentum(),
            "field_momentum": self.total_field_momentum(),
            "total_momentum": self.total_momentum(),
            "all_core_state_integer": True,
            "bounded_core_integers": True,
            "fixed_cell_state": True,
            "nearest_neighbors": 6,
            "dimensions": 3,
            "local_update_O1": True,
            "xy_slice_available": True,
            "global_sparse_scheduler_O1_claimed": False,
        }


# Backward-friendly public alias: the active simulator is now 3D.
IntegerO1Field = IntegerO1Field3D


def static_integer_audit(source_path):
    """AST audit of the simulator file for forbidden core numeric constructs."""
    text = open(source_path, "r", encoding="utf-8").read()
    tree = ast.parse(text)
    forbidden = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            forbidden.append((node.lineno, "float literal"))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            forbidden.append((node.lineno, "true division /"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
            forbidden.append((node.lineno, "float()"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in ("sqrt", "log", "sin", "cos", "tan", "hypot"):
                forbidden.append((node.lineno, node.func.attr))
    return forbidden


def regression_two_particle_plane():
    """Mandatory symmetry regression at the standard force coupling: two offset head-on particles in z=mid plane."""
    cfg = Config(nx=64, ny=64, nz=32, c_units=12, source_strength=64,
                 field_den=7, force_num=1, force_den=12,
                 max_particles_per_cell=4)
    u = IntegerO1Field3D(cfg)
    z0 = 16
    # Same 2-cell lateral offset idea as the prior 2D regression, now embedded in 3D.
    u.add_particle(0, 22, 31, z0, 3, 0, 0)
    u.add_particle(1, 42, 33, z0, -3, 0, 0)
    initial_total = u.total_momentum()
    nonzero_impulses = 0
    common_event = False
    seen0 = {(0, 22, 31, z0)}
    seen1 = {(0, 42, 33, z0)}
    for _ in range(180):
        before = len(u.force_records)
        u.step()
        for rec in u.force_records[before:]:
            if rec[8] != 0 or rec[9] != 0 or rec[10] != 0:
                nonzero_impulses += 1
        if u.paths[0]:
            seen0.add(u.paths[0][-1])
        if u.paths[1]:
            seen1.add(u.paths[1][-1])
        if seen0.intersection(seen1):
            common_event = True
    p0 = u.particles[0]
    p1 = u.particles[1]
    assert nonzero_impulses > 0
    assert (p0[PX], p0[PY], p0[PZ]) == (-p1[PX], -p1[PY], -p1[PZ])
    assert u.total_momentum() == initial_total == (0, 0, 0)
    assert p0[Z] == z0 and p1[Z] == z0
    assert u.audit()
    return {
        "passed": True,
        "nonzero_impulses": nonzero_impulses,
        "particle_0_momentum": (p0[PX], p0[PY], p0[PZ]),
        "particle_1_momentum": (p1[PX], p1[PY], p1[PZ]),
        "total_momentum": u.total_momentum(),
        "remained_on_xy_plane": True,
        "common_spacetime_event_observed": common_event,
    }


def self_tests():
    cfg = Config(nx=48, ny=48, nz=48, c_units=1000, source_strength=64,
                 field_den=7, force_num=1, force_den=64,
                 max_particles_per_cell=4)

    # 1) Stationary isolated source: 3D six-way symmetry and zero self-force.
    s = IntegerO1Field3D(cfg)
    s.add_particle(1, 24, 24, 24, 0, 0, 0)
    s.run(60)
    side = [s.phi((24 + dx, 24 + dy, 24 + dz)) for dx, dy, dz in DIRECTIONS]
    assert len(set(side)) == 1
    assert s._gradient((24, 24, 24)) == (0, 0, 0)
    assert s.total_particle_momentum() == (0, 0, 0)
    center60 = s.phi((24, 24, 24))
    s.run(60)
    center120 = s.phi((24, 24, 24))
    assert abs(center120 - center60) <= 1

    # 2) Guaranteed non-zero +x impulse and exact equal/opposite field momentum.
    m = IntegerO1Field3D(cfg)
    m.add_particle(1, 10, 10, 10, 0, 0, 0)
    m._cell((11, 10, 10))[PHI] = 128
    m._cell((9, 10, 10))[PHI] = 0
    p_before = m.total_momentum()
    m._particle_step_in_cell((10, 10, 10))
    p_after = m.total_momentum()
    assert p_before == p_after
    assert m.particles[1][PX] == 2
    assert m._cell((10, 10, 10))[FIELD_PX] == -2
    assert m.particles[1][PY] == 0 and m.particles[1][PZ] == 0

    # 3) +z neighbour contributes only to z gradient.
    ztest = IntegerO1Field3D(cfg)
    ztest._cell((5, 5, 6))[PHI] = 9
    assert ztest._gradient((5, 5, 5)) == (0, 0, 9)

    # 4) 2D diagnostic slice must not alter 3D state.
    slice_before = dict(s.xy_slice(24))
    particle_before = tuple(s.particles[1])
    slice_after = dict(s.xy_slice(24))
    assert slice_before == slice_after
    assert tuple(s.particles[1]) == particle_before

    # 5) Isolated cardinal mover must not be slowed or turned by its own trail.
    solo_cfg = Config(nx=64, ny=64, nz=32, c_units=12, source_strength=64,
                      field_den=7, force_num=1, force_den=12,
                      max_particles_per_cell=4)
    solo = IntegerO1Field3D(solo_cfg)
    solo.add_particle(9, 20, 20, 16, 3, 0, 0)
    solo.run(100)
    assert tuple(solo.particles[9][PX:PZ+1]) == (3, 0, 0)
    assert all(rec[8] == 0 and rec[9] == 0 and rec[10] == 0
               for rec in solo.force_records)

    # 6) Offset head-on movers must receive equal/opposite transverse turning
    # from the overlapping field, without changing the field structure itself.
    turn_cfg = Config(nx=128, ny=96, nz=32, c_units=12, source_strength=64,
                      field_den=7, force_num=1, force_den=12,
                      max_particles_per_cell=4)
    turn = IntegerO1Field3D(turn_cfg)
    z0 = 16
    turn.add_particle(0, 44, 47, z0, 3, 0, 0)
    turn.add_particle(1, 84, 49, z0, -3, 0, 0)
    initial_turn_total = turn.total_momentum()
    turn.run(110)
    p0 = turn.particles[0]
    p1 = turn.particles[1]
    assert p0[PY] > 0 and p1[PY] < 0
    assert p0[PX] == 3 and p1[PX] == -3
    assert (p0[PY], p0[PZ]) == (-p1[PY], -p1[PZ])
    assert turn.total_momentum() == initial_turn_total == (0, 0, 0)

    # 7) Immediate transverse-contact regression.
    # With unit force denominator, the first non-zero transverse field imbalance
    # must change transverse momentum in the same physical tick. This catches
    # regressions where a particle visually crosses the other field without turning.
    contact_cfg = Config(nx=64, ny=48, nz=24, c_units=12, source_strength=64,
                         field_den=7, force_num=1, force_den=1,
                         max_particles_per_cell=4)
    contact = IntegerO1Field3D(contact_cfg)
    zc = 12
    contact.add_particle(0, 28, 23, zc, 3, 0, 0)
    contact.add_particle(1, 36, 25, zc, -3, 0, 0)
    contact_tick = -1
    turn_tick = -1
    for _ in range(24):
        before = len(contact.force_records)
        py0 = contact.particles[0][PY]
        py1 = contact.particles[1][PY]
        contact.step()
        for rec in contact.force_records[before:]:
            # rec[6] is gy: transverse to the initial +/-x motion.
            if contact_tick < 0 and rec[6] != 0:
                contact_tick = contact.tick
        if turn_tick < 0 and (contact.particles[0][PY] != py0 or
                              contact.particles[1][PY] != py1):
            turn_tick = contact.tick
    assert contact_tick > 0
    assert turn_tick == contact_tick
    assert contact.particles[0][PY] == -contact.particles[1][PY]
    assert contact.total_momentum() == (0, 0, 0)

    # 8) Mandatory prior two-particle symmetry regression embedded in z plane.
    pair = regression_two_particle_plane()

    return {
        "integer_only_runtime": True,
        "three_dimensions": True,
        "six_neighbor_locality": True,
        "bounded_core_integers": True,
        "stationary_source_persistent": True,
        "stationary_source_symmetric_3d": True,
        "stationary_self_force_zero": True,
        "fixed_cell_state": True,
        "one_speed_law_with_universal_c_cap": True,
        "matter_field_momentum_exact": True,
        "xy_surface_diagnostic_noninvasive": True,
        "isolated_mover_no_self_drag": True,
        "offset_pair_transverse_turning": True,
        "transverse_contact_turn_same_tick": True,
        "two_particle_regression": pair,
        "report": m.report(),
    }


if __name__ == "__main__":
    forbidden = static_integer_audit(__file__)
    if forbidden:
        raise AssertionError(forbidden)
    print(json.dumps(self_tests(), indent=2))
