"""Drop the per-interval Link currents from a record's Node lines so that the kept file stays below the kept size (the diag and the log keep every number read; a credit's frame dropped where the file is still above it)."""
import json, sys
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for line in d["nodes"]:
        line.pop("current", None)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)
