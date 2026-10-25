"""cl1's worlds: two bodies of row 2 (universe_middle: the heavy lift at the 31-bit den, as the kit's world_bodies_120) on the 15-cube,
width 2, 125 quanta each, the sea around them, at the distance d along z about the centre, like senses (1, 1), opposite (1, -1) and
neutral (the engine's conjugate pair, no field), 120 intervals; and the charge "T div 2" copies. Integers only."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CUBE, N, WIDTH, INTERVALS = 15, 125, 2, 120
for d in (3, 4, 6):
    za, zb = (CUBE - d) // 2, (CUBE - d) // 2 + d
    for name, senses in (("like", (1, 1)), ("opposite", (1, -1)), ("neutral", (None, None))):
        for charge in (None, "T div 2"):
            lays = [{"lay": "sea", "row": 0}]
            for z, s in zip((za, zb), senses):
                lay = {"lay": "at", "row": 2, "centre": [7, 7, z], "width": WIDTH, "quanta": N}
                if s is not None:
                    lay["sense"] = s
                if charge is not None:
                    lay["charge"] = charge
                lays.append(lay)
            world = {"universe": "universe_middle.json", "shape": [CUBE] * 3, "intervals": INTERVALS, "seed": lays}
            tag = f"{name}_d{d}" + ("_Tdiv2" if charge else "")
            json.dump(world, open(os.path.join(HERE, f"world_{tag}.json"), "w"))
            print(tag, za, zb)
