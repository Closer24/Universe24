import json, sys
o = json.load(open(sys.argv[1]))
print(o["record"], "births", o["births"], "counts", o["counts"])
for b in o["bangs"]:
    print({k: b.get(k) for k in ("bang", "from", "births", "plus_at_take", "minus_at_take", "excess_plus_at_take", "W_sum", "flip_plane", "emitter_births", "emitter_flip_plane", "planes_plain", "planes_mirror", "by_taken_row", "digits", "digits_flipped", "digits_F_divides_w", "digits_flipped_engine_base")})
print("total", o["total"])
