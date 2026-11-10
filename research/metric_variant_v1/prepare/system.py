"""INTEGRATOR initial data for the composed default system (AGENTS item 9: data only; nothing here runs a step).
Reference remainders follow the declared L0 embedding r -> Q r1 + l0_offset (ONE-VACUUM option)."""
from __future__ import annotations

import random

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Tensor
from . import vacuum_state


def system_vacuum(system, tensor: Tensor, L: int) -> State:
    return vacuum_state(tensor, system.Q, L, *system.blocks)


def random_system_state(system, tensor: Tensor, L: int, seed: int, ref_amp: int = 20, matter_amp: int = 1 << 10,
                        field_amp: int = 1 << 10, gauge_matter_amp: int = 4000, link_noise: int = 8,
                        path_amp: int = 16, ring_amp: int = 3, random_r: bool = True) -> State:
    """Random data on every gear: ref a, b in [-ref_amp, ref_amp] with r = Q r1 + offset; gauge matter |psi| <=
    gauge_matter_amp, gauge link deviations |W| <= link_noise, 2-path deviations <= path_amp; Dirac matter <= matter_amp;
    every other field gear <= field_amp; choice rings and detectors <= ring_amp; new-gear remainders uniform."""
    Q = system.Q
    D = 6 * Q
    s0 = system_vacuum(system, tensor, L)
    rng = random.Random(seed)
    N = lattice(L).N
    a = s0.a.astype(OBJ)
    b = s0.b.astype(OBJ)
    r = s0.r.astype(OBJ)
    off = system.info.get("l0_offset", 0)
    for i, name in enumerate(tensor.names):
        ns, local = name.split(".", 1)
        if ns == "ref":
            amp = ref_amp
        elif ns in ("su2", "su3", "u1", "emu1"):
            amp = gauge_matter_amp if local.startswith("psi") else (path_amp if local.startswith("P") else link_noise)
        elif ns == "matter":
            amp = matter_amp
        elif ns in ("arm1", "arm2", "router", "drive", "seq", "gate", "exit"):
            amp = ring_amp
        else:
            amp = field_amp
        a[i] = [rng.randint(-amp, amp) for _ in range(N)]
        b[i] = [rng.randint(-amp, amp) for _ in range(N)]
        if ns == "ref":
            r[i] = [Q * rng.randrange(6) + off for _ in range(N)]
        elif random_r:
            r[i] = [rng.randrange(D) for _ in range(N)]
    return State(L, a, b, r)


def random_reference_state(Q: int, tensor_ref: Tensor, L: int, seed: int, amp: int = 20, offset: int = 0) -> State:
    """Dense random data for the reference block alone (r = Q r1 + offset)."""
    rng = random.Random(seed)
    N = lattice(L).N
    G = tensor_ref.G
    a = np.array([[rng.randint(-amp, amp) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    b = np.array([[rng.randint(-amp, amp) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    r1 = np.array([[rng.randrange(6) for _ in range(N)] for _ in range(G)], dtype=OBJ)
    return State(L, a, b, Q * r1 + offset)


__all__ = ["system_vacuum", "random_system_state", "random_reference_state"]
