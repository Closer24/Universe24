"""The page body_motion.html built from the recorded run.

The record is run_viz.py's viz_results.json (under runs/body_motion/ at the repository root by default, or the path
given); the page's data are the record pruned to what it draws, the parameters v, X, YZ, mid, k, omega, omega0 and xc,
the rows' t, share (the key `count`), centroid, rms and shed, and the three slices per interval (the level now and the
content on the middle plane, the share per layer of x); the largest level and the content at the centroid stay in the
record alone. The template body_motion.template.html holds the markup and the script; the data are written in its place
as one JSON literal, or with --compressed as gzip in base64 that the page inflates with the browser's DecompressionStream
(the same page, a third of the size, no fetch). The page is written beside this script.

    python examples/events/body_motion/build_page.py [--records runs/body_motion/viz_results.json] [--compressed] [--out body_motion.html]
"""

import argparse
import base64
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PARAMS = ("v", "X", "YZ", "mid", "k", "omega", "omega0", "xc")
ROW = ("t", "count", "cx", "cy", "cz", "rms", "shed")
INFLATE = (
    "async function inflate(b64) { const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0)); "
    "const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')); "
    "return JSON.parse(await new Response(stream).text()); }"
)


def pruned(record: dict) -> dict:
    """The record's part the page draws."""
    return {
        "params": {k: record["params"][k] for k in PARAMS},
        "runs": {"boost": [{k: row[k] for k in ROW} for row in record["runs"]["boost"]]},
        "slices": record["slices"],
    }


def literal(data: object) -> str:
    return json.dumps(data, separators=(",", ":"))


def packed(data: object) -> str:
    return base64.b64encode(gzip.compress(literal(data).encode(), 9)).decode()


def page(template: str, data: dict, compressed: bool) -> str:
    """The template with the data in place: a JSON literal, or gzip in base64 inflated before the script runs."""
    if compressed:
        script = f'const DATA_GZ = "{packed(data)}";\n{INFLATE}'
        opening = "(async function () {\n  const DATA = await inflate(DATA_GZ);"
    else:
        script = f"const DATA = {literal(data)};"
        opening = "(function () {"
    return template.replace("__DATA_SCRIPT__", script).replace("__OPEN__", opening)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--records", type=Path, default=REPO / "runs" / "body_motion" / "viz_results.json"
    )
    parser.add_argument(
        "--compressed", action="store_true", help="the data as gzip in base64, inflated by the page"
    )
    parser.add_argument("--out", type=Path, default=HERE / "body_motion.html")
    args = parser.parse_args()
    record = json.loads(args.records.read_text(encoding="utf-8"))
    template = (HERE / "body_motion.template.html").read_text(encoding="utf-8")
    args.out.write_text(page(template, pruned(record), args.compressed), encoding="utf-8")
    print(f"{args.out}: {args.out.stat().st_size:,} bytes from {args.records}")


if __name__ == "__main__":
    main()
