"""The flux reading (ALGEBRA.md #rule3): e_i(t) - e_i(t - 1) is the sum of G_ij over the reads of i, exactly up to the remainders' own term, on planted rows and on the engine's run."""

from event_universe.events.detector_law import DetectorLawSimulation

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line; the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}


def reads(simulation: DetectorLawSimulation, family: int, length: int) -> dict[tuple[int, int], int]:
    """The read matrix A of a chain (y and z of extent 1): (i, j) with the multiplicity of the reads of j among the six reads of i; the self-reads of the folded axes."""
    wrap = simulation.kind_wrap[family]
    out: dict[tuple[int, int], int] = {}
    for x in range(length):
        for axis in range(3):
            for sign in (1, -1):
                if axis > 0:
                    if wrap[axis]:
                        out[(x, x)] = out.get((x, x), 0) + 1
                    continue
                j = x + sign
                if 0 <= j < length:
                    out[(x, j)] = out.get((x, j), 0) + 1
                elif wrap[0]:
                    out[(x, j % length)] = out.get((x, j % length), 0) + 1
    return out
