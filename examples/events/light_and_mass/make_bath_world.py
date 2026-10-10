"""The periodic light-only world for the bath test: the packet of pass_fixed_alone (its generator-laid mode, the flat indices identical since Y = 31 and Z = 1), on a 41 x 31 x 1 board periodic on every axis, no bodies, one screen; intervals and the draw's window as given; the mode file's digest recomputed over the world document, as event_universe.world_files.input_digest does."""
import json, sys
sys.path.insert(0, "src")
from event_universe.world_files import input_digest
N = int(sys.argv[1])
src = json.load(open("examples/events/light_and_mass/pass_fixed_alone.json"))
mode_src = json.load(open("examples/events/light_and_mass/pass_fixed_alone.mode.json"))
w = {
 "shape": [41, 31, 1],
 "boundary": {"x": sys.argv[2], "y": sys.argv[3], "z": "periodic"},
 "intervals": N,
 "universe": (sys.argv[4] if len(sys.argv) > 4 else "examples/events/rule.json"),
 "engine": "examples/events/engine_start.json",
 "bodies": [],
 "packets": src["packets"],
 "node_detectors": [{"name": "screen", "positions": [[36, 14, 0], [36, 15, 0], [36, 16, 0], [36, 17, 0]]}],
 "draw": dict(src["draw"], window=N),
}
json.dump(w, open(sys.argv[5] if len(sys.argv) > 5 else "examples/events/light_and_mass/bath_periodic.json", "w"), indent=1)
mode = {"world_digest": input_digest(w), "bodies": [], "packets": mode_src["packets"]}
json.dump(mode, open((sys.argv[5] if len(sys.argv) > 5 else "examples/events/light_and_mass/bath_periodic.json").replace(".json", ".mode.json"), "w"))
print("world written, intervals", N, "digest", mode["world_digest"][:16], "packet count", mode_src["packets"][0]["count"])
