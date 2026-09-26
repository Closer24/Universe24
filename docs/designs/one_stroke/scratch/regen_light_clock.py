"""Regenerate the shipped light clock alone (examples/events/massive_record/light_clock.json)
from the detector-law generator, leaving the held worlds (history) untouched."""

import importlib.util
import json

spec = importlib.util.spec_from_file_location("dl", "examples/events/detector_law/make_worlds.py")
dl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dl)
massive = dl.load_massive_generator()
worlds = dl.massive_worlds(massive)
print("massive worlds of the detector generator:", sorted(worlds))
for name in ("light_clock",):
    document = massive.bind_families_file(worlds[name])
    path = dl.MASSIVE / f"{name}.json"
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    print("written", path)
