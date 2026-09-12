"""Integer initial conditions and preselected small-world measurement questions."""

import itertools
import math

from configuration import build_configuration


def plane(shape, mode, polarization, ticks=16, *, scatter_enabled=True):
    """Quantize a smooth initial profile; no host calculation is used during evolution."""
    moments = []
    for position in itertools.product(*(range(n) for n in shape)):
        phase = sum(m * x / n for m, x, n in zip(mode, position, shape, strict=True))
        amplitude = round(32 * math.cos(2 * math.pi * phase))
        electric = tuple(amplitude * v for v in polarization)
        moments.append((position, electric, (0, 0, 0)))
    return build_configuration(shape, ticks, moments, scatter_enabled=scatter_enabled)


def cases():
    result = {}
    for size in (9, 15):
        center = (size // 2,) * 3
        result[f"compact-{size}"] = {
            "input": build_configuration((size,) * 3, 3, [(center, (0, 32, 0), (0, 0, 0))]),
            "kind": "compact",
        }
        result[f"axial-{size}"] = {
            "input": plane((size, 3, 3), (1, 0, 0), (0, 1, 0)),
            "kind": "wave",
            "mode": (1, 0, 0),
            "polarization": (0, 1, 0),
        }
        result[f"oblique-{size}"] = {
            "input": plane((size, size, 3), (1, 2, 0), (2, -1, 0)),
            "kind": "wave",
            "mode": (1, 2, 0),
            "polarization": (2, -1, 0),
        }
    result["axial-second-polarization"] = {
        "input": plane((9, 3, 3), (1, 0, 0), (0, 0, 1)),
        "kind": "wave",
        "mode": (1, 0, 0),
        "polarization": (0, 0, 1),
    }
    result["axial-rotated"] = {
        "input": plane((3, 9, 3), (0, 1, 0), (0, 0, 1)),
        "kind": "wave",
        "mode": (0, 1, 0),
        "polarization": (0, 0, 1),
    }
    result["stream-only-control"] = {
        "input": plane((15, 3, 3), (1, 0, 0), (0, 1, 0), scatter_enabled=False),
        "kind": "control",
        "mode": (1, 0, 0),
        "polarization": (0, 1, 0),
    }
    result["longitudinal-control"] = {
        "input": plane((15, 3, 3), (1, 0, 0), (1, 0, 0)),
        "kind": "longitudinal",
        "mode": (1, 0, 0),
        "polarization": (1, 0, 0),
    }
    # A centered integer curl has exactly zero centered divergence initially.
    size = 9
    phi = {
        (x, y): round(16 * math.cos(2 * math.pi * (x + 2 * y) / size))
        for x in range(size)
        for y in range(size)
    }
    moments = []
    for x, y, z in itertools.product(range(size), range(size), range(3)):
        electric = (
            phi[x, (y + 1) % size] - phi[x, (y - 1) % size],
            phi[(x - 1) % size, y] - phi[(x + 1) % size, y],
            0,
        )
        moments.append(((x, y, z), electric, (0, 0, 0)))
    result["centered-gauss-control"] = {
        "input": build_configuration((size, size, 3), 4, moments),
        "kind": "gauss",
    }
    return result
