"""Meshes that lengthen, read by clicks alone: a stand-in for G2's moving Meshes, in whole numbers, so the decoder's readings close."""

# The board's labels stay: a Node-clock keeps its site for ever. What lengthens is the Mesh, here as the rounds light
# needs to cross it. Light gains one unit a round and crosses a Mesh when its gain reaches the Mesh's length then,
# the rest kept (Rule3's carry), so it never crosses more than one Mesh a round. Every clock stands at its Node-clock
# and ticks once a round, so a clock's own count is its rounds: what changes is the Mesh, not the clock. A stand-in:
# the engine's Meshes move from G2 on, and its light is the act's; the decoder's readings here are counts alone.

ROUNDS = 6000  # the rounds the line is run
NODES = 40  # a line of Node-clocks, 0 at one end
BASE = 4  # a Mesh's length at the bang, in light's units
SLOW = 50  # the rounds per unit a Mesh lengthens by, where it grows by steps
DOUBLE = 400  # the rounds in which a Mesh doubles, where it grows by doubling
TOP = 1500  # the round of the top, where a swing turns
BEAT = 10  # the rounds between two quanta a far clock lays toward Node-clock 0


def still(r: int, mesh: int) -> int:
    """No Mesh lengthens."""
    return BASE


def growing(r: int, mesh: int) -> int:
    """Every Mesh lengthens by one unit every SLOW rounds."""
    return BASE + r // SLOW


def doubling(r: int, mesh: int) -> int:
    """Every Mesh doubles every DOUBLE rounds."""
    return BASE << (r // DOUBLE)


def swing(r: int, mesh: int) -> int:
    """Every Mesh lengthens until the top and shortens after it, at one unit every SLOW rounds."""
    return BASE + min(r, max(TOP + TOP - r, 0)) // SLOW


def flight(length, start: int, frm: int, to: int) -> int | None:
    """The round a quantum laid at Node-clock frm at round start is taken at Node-clock to, or None within the run."""
    way = 1 if to > frm else -1
    node, gained, r = frm, 0, start
    while node != to:
        r += 1
        if r > ROUNDS:
            return None
        gained += 1
        mesh = min(node, node + way)
        if gained >= length(r, mesh):
            gained -= length(r, mesh)
            node += way
    return r


def echo(length, start: int, far: int) -> int | None:
    """Node-clock 0's own count from its lay at round start to the take of the echo from Node-clock far."""
    there = flight(length, start, 0, far)
    back = None if there is None else flight(length, there, far, 0)
    return None if back is None else back - start


def arrivals(length, far: int, until: int) -> list[int]:
    """The rounds at which Node-clock 0 takes the quanta Node-clock far lays every BEAT rounds up to round until."""
    return [a for a in (flight(length, s, far, 0) for s in range(0, until, BEAT)) if a is not None]


def gaps(rounds: list[int]) -> list[int]:
    """The counts between two takes in a row."""
    return [b - a for a, b in zip(rounds, rounds[1:], strict=False)]


if __name__ == "__main__":
    print("Meshes that lengthen, read by clicks alone (a stand-in for G2), whole numbers only\n")
    sends = (0, 500, 1000, 1500, 2000)
    print(
        f"1. One label distance, Node-clock 0 to Node-clock 5, and its echo in Node-clock 0's own count, laid at rounds {sends}:"
    )
    for name, length in (("still", still), ("growing", growing), ("doubling", doubling)):
        print(f"   {name:8}: {[echo(length, s, 5) for s in sends]}")
    print(
        "   The label distance is 5 every time; the echo is a length, the label is none (a site's difference is no length)."
    )
    print(
        "\n2. The horizon, under doubling Meshes: the farthest Node-clock whose quantum, laid at a round, is ever taken at Node-clock 0"
    )
    for lay in (0, 800, 1600, 2400, 3200):
        reached = [f for f in range(1, NODES) if flight(doubling, lay, f, 0) is not None]
        taken = f"from Node-clocks 1 to {max(reached)}" if reached else "from no Node-clock"
        print(f"   laid at round {lay:4}: taken {taken}, and from none beyond it within {ROUNDS} rounds")
    print("   The horizon closes in, in labels: what is laid later beyond it is never taken here.")
    print(
        "\n3. The redshift: a clock at Node-clock 20 lays one quantum every 10 rounds; Node-clock 0 counts its own rounds between the takes"
    )
    for name, length in (("still", still), ("growing", growing)):
        g = gaps(arrivals(length, 20, 1000))
        print(
            f"   {name:8}: the first gaps {g[:5]}, the last {g[-3:]}; gaps above 10: {sum(1 for x in g if x > BEAT)} of {len(g)}"
        )
    print(
        "\n4. The swing: Meshes lengthen to the top at round 1500 and shorten after it; Node-clock 0 takes quanta laid every 10 rounds"
    )
    for far in (2, 10, 30):
        taken = arrivals(swing, far, ROUNDS)
        after = [(b, b - a) for a, b in zip(taken, taken[1:], strict=False) if b > TOP]
        first_blue = next((b for b, g in after if g < BEAT), None)
        red_after = sum(1 for b, g in after if g > BEAT and (first_blue is None or b < first_blue))
        print(
            f"   from Node-clock {far:2}: after the top, the first gap below 10 at round {first_blue}; before it, {red_after} gaps above 10 (still red)"
        )
    print(
        "   The nearest turns blue first, and the far light keeps arriving red long after the top: the clicks still see the expansion."
    )
    print(
        "\n5. The cone: light crosses at most one Mesh a round, under every law above, by its carry (one unit a round, a Mesh at least one unit)."
    )
