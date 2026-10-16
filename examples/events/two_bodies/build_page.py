"""The page two_bodies.html built from the recorded runs.

The records are run_fall_long.py's fall_results_long_49x17.json (the pair, 900 intervals, with the slices every third
interval) and run_fall2.py's fall_results_49x17.json (the body alone, the control's centroid), both under runs/two_bodies/
at the repository root by default or at the paths given; the page's data are the long record pruned to what it draws,
the parameters X, YZ, mid, centres and stride, each row's t and per half the share (the key `count`), centroid, rms and
shed, and the three slices (the level now and the content on the middle plane, the share per layer of x), and the
control's rows pruned to t and the centroid's x; the total share and the content at the centroids stay in the records
alone. The template two_bodies.template.html holds the markup and the script; the data are written in its place as JSON
literals, or with --compressed as gzip in base64 that the page inflates with the browser's DecompressionStream (the same
page, a third of the size, no fetch). The page is written beside this script.

    python examples/events/two_bodies/build_page.py [--records runs/two_bodies/fall_results_long_49x17.json] [--control runs/two_bodies/fall_results_49x17.json] [--compressed] [--out two_bodies.html]
"""

import argparse
import base64
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PARAMS = ("X", "YZ", "mid", "centres", "stride")
BODY = ("count", "cx", "cy", "cz", "rms", "shed")
INFLATE = (
    "async function inflate(b64) { const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0)); "
    "const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')); "
    "return JSON.parse(await new Response(stream).text()); }"
)


def pruned(record: dict) -> dict:
    """The long record's part the page draws."""
    rows = [
        {"t": row["t"], "bodies": [{k: body[k] for k in BODY} for body in row["bodies"]]}
        for row in record["runs"]["pair"]
    ]
    return {
        "params": {k: record["params"][k] for k in PARAMS},
        "runs": {"pair": rows},
        "slices": record["slices"],
    }


def control(record: dict) -> list:
    """The body alone's centroid along x per interval, the control's trace."""
    return [
        {"t": row["t"], "bodies": [{"cx": row["bodies"][0]["cx"]}]} for row in record["runs"]["alone"]
    ]


def literal(data: object) -> str:
    return json.dumps(data, separators=(",", ":"))


def packed(data: object) -> str:
    return base64.b64encode(gzip.compress(literal(data).encode(), 9)).decode()


def page(template: str, data: dict, ctrl: list, compressed: bool) -> str:
    """The template with the data in place: JSON literals, or gzip in base64 inflated before the script runs."""
    if compressed:
        script = f'const DATA_GZ = "{packed(data)}";\nconst CONTROL_GZ = "{packed(ctrl)}";\n{INFLATE}'
        opening = "(async function () {\n  const DATA = await inflate(DATA_GZ), CONTROL = await inflate(CONTROL_GZ);"
    else:
        script = f"const DATA = {literal(data)};\nconst CONTROL = {literal(ctrl)};"
        opening = "(function () {"
    return template.replace("__DATA_SCRIPT__", script).replace("__OPEN__", opening)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--records", type=Path, default=REPO / "runs" / "two_bodies" / "fall_results_long_49x17.json"
    )
    parser.add_argument(
        "--control", type=Path, default=REPO / "runs" / "two_bodies" / "fall_results_49x17.json"
    )
    parser.add_argument(
        "--compressed", action="store_true", help="the data as gzip in base64, inflated by the page"
    )
    parser.add_argument("--out", type=Path, default=HERE / "two_bodies.html")
    args = parser.parse_args()
    long = json.loads(args.records.read_text(encoding="utf-8"))
    alone = json.loads(args.control.read_text(encoding="utf-8"))
    template = (HERE / "two_bodies.template.html").read_text(encoding="utf-8")
    args.out.write_text(page(template, pruned(long), control(alone), args.compressed), encoding="utf-8")
    print(f"{args.out}: {args.out.stat().st_size:,} bytes from {args.records} and {args.control}")


if __name__ == "__main__":
    main()
