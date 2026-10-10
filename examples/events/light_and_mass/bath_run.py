"""The bath test on the engine itself: the world loaded and stepped exactly as tools/look/record.py does (the engine's own step), and after every interval the charge family's arrays read with record.frame: the engine's own form per Node (the holder's source), its count per Node, the level now; summed over the board per interval, and every `snap` intervals the spectrum of the level (|a_k|^2 by |k| bins, the packet's own k = (pi/2, 0) set apart) to see where the growth sits. Nothing is written from outside after the lay; the box is closed on x and y."""
import importlib.util, json, math, sys, time
sys.path.insert(0, "/home/user/Universe24/src")
spec = importlib.util.spec_from_file_location("look_record", "/home/user/Universe24/tools/look/record.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
import numpy as np
from pathlib import Path

world_path = Path(sys.argv[1]); N = int(sys.argv[2]); snap = int(sys.argv[3]); out = Path(sys.argv[4])
world = R.load_world(world_path)
lines = []
board = R.Lattice(world, lines.append)
fam_names = [f.name for f in board.families]
ci = fam_names.index("charge")
X, Y, Z = world.shape[0], world.shape[1], world.shape[2]
kx = 2 * math.pi * np.fft.fftfreq(X); ky = 2 * math.pi * np.fft.fftfreq(Y)
KX, KY = np.meshgrid(kx, ky, indexing="ij")
Kabs = np.sqrt(np.minimum(np.abs(KX), 2 * math.pi - np.abs(KX)) ** 2 + np.minimum(np.abs(KY), 2 * math.pi - np.abs(KY)) ** 2)
packet_k = (np.abs(KX) > 0.35) & (np.abs(KX) < 1.25) & (np.abs(KY) < 0.75)   # the laid wave: wavelength 8 along x (k_x = pi/4) with its envelope, 7 Nodes wide in y
bins = [(0, 0.35), (1.25, 1.8), (1.8, 2.4), (2.4, 3.0), (3.0, 3.6), (3.6, 4.5)]

def arr(a):
    a = np.asarray(a); return a.reshape(X, Y) if a.ndim == 3 else a

rows, snaps = [], []
prev_now = None; prev2 = None
f0 = R.frame(board, None)
now0 = arr(f0["families"]["charge"]["now"])
t_start = time.time()
for t in range(1, N + 1):
    kept = {index: [R.copied(line) for line in board.states[index].lines] for index in board.order}
    board.step()
    if board.ended is not None:
        print(json.dumps({"ended": str(board.ended), "interval": t})); break
    kept = {index: [R.grown(line, board) for line in lns] for index, lns in kept.items()}
    fr = R.frame(board, kept)
    ch = fr["families"]["charge"]
    now = arr(ch["now"]); form = arr(ch["form"]); count = arr(ch["count"])
    g = fr["families"]["gravity"]
    glevel = arr(g["level"]) if "level" in g else None
    row = {"t": t, "form_total": float(form.sum()), "count_total": float(count.sum()), "share": int(ch["share"]), "pace": int(ch["pace"]),
           "level_sq": float((now.astype(float) ** 2).sum()), "nonzero": int(np.count_nonzero(now)),
           "gravity_level_total": (float(glevel.sum()) if glevel is not None else None)}
    if prev2 is not None:
        D = prev_now.astype(float) ** 2 - now.astype(float) * prev2.astype(float)   # my form at t-1 from the three levels, exactly conserved by the real step at fixed paces
        row["D_total"] = float(D.sum())
    rows.append(row)
    if t % snap == 0 or t == 1:
        F = np.fft.fft2(now.astype(float)); P = np.abs(F) ** 2 / (X * Y)
        s = {"t": t, "packet_k": float(P[packet_k].sum()), "rest": float(P[~packet_k].sum()),
             "bins_mean_per_mode": [float(P[(Kabs >= a) & (Kabs < b) & ~packet_k].mean()) for a, b in bins],
             "staggered": float(P[np.abs(np.abs(KX) - math.pi) < 0.2].sum())}
        snaps.append(s)
        print(json.dumps({"t": t, "form": row["form_total"], "D": row.get("D_total"), "count": row["count_total"], "nonzero": row["nonzero"], "packet_k": s["packet_k"], "rest": s["rest"], "bins": [round(b, 2) for b in s["bins_mean_per_mode"]], "sec": round(time.time() - t_start, 1)}), flush=True)
    prev2 = prev_now; prev_now = now
events = {}
for l in lines:
    events[l.get("event", "?")] = events.get(l.get("event", "?"), 0) + 1
json.dump({"world": str(world_path), "shape": [X, Y, Z], "intervals": N, "rows": rows, "snaps": snaps, "events": events, "amplitude": 1241, "T": world.quantum_action if hasattr(world, "quantum_action") else None}, open(out, "w"))
print(json.dumps({"done": N, "events": events, "seconds": round(time.time() - t_start, 1)}))
