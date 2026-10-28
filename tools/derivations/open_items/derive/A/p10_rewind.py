"""P10, the rewind of the running engine with the take F3 in place (P8's patch), against the head as it is.

tests/laws.run_back_exact: n ticks forward, n back, the count of the n states returned bit for bit.  The head's
undo (click.undo) reads each take's move back from its log line: the gear (`taken_line`), the count (`levels`) and
the direction toward the before (`taker`: now, before).  F3's move is along -sgn(G); where that is not toward the
before the head's undo would move it the wrong way.  So the undo is read twice: the head's as written, and with
the signed move F3 wrote kept on its log line (`f3_signed`) and read back by the undo (a probe's patch).

argv: the head's worktree, the world file, the ticks, 'head' | 'f3' | 'f3signed'.
"""
import sys
WT, WORLD, N, RUNMODE = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
src = open(__file__.replace("p10_rewind.py", "p8_images.py")).read()
head_part = src.split("CUBE = 5")[0].replace('MODE = sys.argv[3]', 'MODE = "f3" if sys.argv[4] != "head" else "head"')
head_part = head_part.replace("TICKS = int(sys.argv[2])", "TICKS = 0")
exec(compile(head_part, "p8_images.py (its patch)", "exec"))
from tests.laws import world_of, run_back_exact  # noqa: E402
from event_universe import click as C  # noqa: E402
from event_universe.clock import Clock  # noqa: E402

if RUNMODE == "f3signed":
    WRITTEN = {}  # (the tick, the Node-clock) -> the signed count F3's take moved there
    orig_unsprung_end = U.unsprung_end

    def unsprung_end_signed(clock, rec, read):
        entry = orig_unsprung_end(clock, rec, read)
        WRITTEN[(clock.ticks, read[0])] = SIGNED[(id(clock), read[0], 1)][1]
        return entry

    U.unsprung_end = unsprung_end_signed
    orig_move = C.move

    def move_back(clock, rec, k, where, count):
        """The undo's move with F3's own signed count, read at the tick being undone (ticks already counted down)."""
        key = (clock.ticks + 1, tuple(where))
        if key in WRITTEN and count != 0:
            return orig_move(clock, rec, k, where, -WRITTEN.pop(key))
        return orig_move(clock, rec, k, where, count)

    C.move = move_back

calibre, piece = world_of(WORLD)
clock = Clock(calibre, piece)
got = run_back_exact(clock, N)
print(f"P10 {WORLD}, {N} ticks forward and back, the engine {RUNMODE}: {got} of {N} states returned bit for bit; "
      f"fittings {clock.counts['births']}, chimes {clock.counts['body_clicks']}")
