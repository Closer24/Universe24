"""Probe B2 (faces): which fields of the chime's face move under the end-teeth variants ET and ET3, against the head.
Usage: python -I b2_faces.py <variant> <world> <ticks>"""
import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import b2_floor as F  # noqa: E402
import bcommon as B  # noqa: E402

variant, world, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3])
head, var = B.make(world), B.make(world)
for _ in range(ticks):
    F.uninstall()
    head.tick()
    F.install(variant)
    var.tick()
    F.uninstall()
fields = {}
for a, b in zip(head.log, var.log):
    fa, fb = a.get("frame"), b.get("frame")
    if fa is not None and fa != fb:
        for k in fa:
            if fa.get(k) != fb.get(k):
                fields[k] = fields.get(k, 0) + 1
print(json.dumps({"variant": variant, "world": world, "ticks": ticks, "face fields differing (entries)": fields}))
