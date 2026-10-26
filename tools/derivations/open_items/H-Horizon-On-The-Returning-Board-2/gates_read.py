"""The gates of the horizon and the recurring bang read by the engine's own readers on a record (board.py and clicks.py through the decoder's Record)."""
import json, sys
from event_universe import board, clicks
from event_universe.decoder import Record
rec = Record(json.load(open(sys.argv[1])))
for name, fn in (("14 the horizon", board.horizon), ("34 the horizon and the stopped clock", board.stopped_clock), ("61 the horizon radiates", clicks.horizon_radiates)):
    try:
        print(name, json.dumps(fn(rec))[:600])
    except Exception as e:
        print(name, "reader refused:", type(e).__name__, str(e)[:200])
for name, fn in (("1 the bang returns", board.returns), ("46 the recurring bang", board.recurring_bang)):
    try:
        print(name, json.dumps(fn(rec))[:700])
    except Exception as e:
        print(name, "reader refused:", type(e).__name__, str(e)[:200])
for n in ():
    if "bang" in n or "recur" in n:
        print("board:", n)
