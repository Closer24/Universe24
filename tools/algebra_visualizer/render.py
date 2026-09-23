"""The algebra visualizer: one page in three layers (the geometry that is the
algebra; how it produces the physics; the clicks), every panel read from a
run's record alone (docs/designs/algebra_visualizer/DESIGN.md; the model
owner's word of 2026-09-23 through the Boss, record 1435).

Headless by default: the tool reads the two runs, builds the panels and
prints every number with its kind and its source, and writes nothing.
`--render OUT.html` writes the one static page (inline SVG and CSS, a few
lines of plain script for the sliders) and nothing else. The tool never
runs the engine: a missing run folder is refused with the line that makes
it (`tools/run_series.py`). Standard library only; nothing of
`event_universe` is imported.

    PYTHONPATH=src python tools/algebra_visualizer/render.py RUNS_DIR [--render OUT.html]
        [--light c_measured] [--detector slits_low]

`RUNS_DIR` holds one folder per world, `<name>/run` (the runner's output
through `tools/run_series.py`) or `<name>`. The registers are read from
`examples/events/` by the world's name (`REGISTERS`); a world without a
register prints no PIN.
"""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from panels import KIND_WORDS, KINDS, Panel, as_rows, build_panels, head_numbers  # noqa: E402
from record import MissingRun, RunRecord, load_run  # noqa: E402
from svg import figure  # noqa: E402

# The register of a registered world, by the world's name: the file beside
# the world and, where the register keeps one block per world, its block.
REGISTERS: dict[str, tuple[str, str | None]] = {
    "c_measured": ("examples/events/c_measured/expectations.json", None),
    "slits_low": ("examples/events/amplitude/expectations.json", "two_slits"),
}

LAYERS = {
    1: (
        "The geometry that is the algebra",
        "Everything generic, no physical name: the torus, a Node with its six Ports, a record's state vector, each of the six verbs on one Node with its integers, the light rule as one picture.",
    ),
    2: (
        "How it produces the physics",
        "The same verbs over many Nodes and many intervals: a record propagating and read at the faces, the pace c, a foreign object as a declared block with its own pair, a detector-emitter as a declared object, and a GameBoard view labelled a diagnostic.",
    ),
    3: (
        "The clicks",
        "How a click is born on the board, beside how it looks in our world: one record's birth, offers, gather and deletion; the screen as the experimenter sees it, the counts against the detector's clock, the interval between clicks. Every click a DETECTOR reading; nothing pinned or compared.",
    ),
}

WIDE = {"light_rule", "fan", "pace", "life", "screen", "clock", "objects", "gameboard", "block"}

CSS = """
:root{--ground:#f5f6f8;--surface:#ffffff;--ink:#14181d;--muted:#5c6470;--rule:#d9dde3;--soft:#eceff3;
--detector:#1f3f9a;--gameboard:#6a707a;--computation:#0b7a6e;--host:#7a5b12;--conversion:#5a7a1f;--declaration:#7a2f74;--pin:#b0641c;
--c-axes:#2f5bd1;--c-face:#c9622a;--c-body:#2e8b57;--c-rest:#7b6fb0;--band:#e9edf3;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--ground:#14171b;--surface:#1c2026;--ink:#e6e4df;--muted:#a3a9b3;--rule:#2e343c;--soft:#252a31;
--detector:#8fa8ff;--gameboard:#9aa1ab;--computation:#5fcfc2;--host:#d9b25b;--conversion:#b6d16a;--declaration:#d78bd0;--pin:#f0a45c;
--c-axes:#7f9bff;--c-face:#f0925a;--c-body:#66c48f;--c-rest:#b3a7f0;--band:#1a1e24;}}
:root[data-theme="dark"]{color-scheme:dark;--ground:#14171b;--surface:#1c2026;--ink:#e6e4df;--muted:#a3a9b3;--rule:#2e343c;--soft:#252a31;
--detector:#8fa8ff;--gameboard:#9aa1ab;--computation:#5fcfc2;--host:#d9b25b;--conversion:#b6d16a;--declaration:#d78bd0;--pin:#f0a45c;
--c-axes:#7f9bff;--c-face:#f0925a;--c-body:#66c48f;--c-rest:#b3a7f0;--band:#1a1e24;}
body{background:var(--ground);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;margin:0;padding-block:24px 64px;padding-inline:16px;}
.wrap{max-width:1160px;margin:0 auto;}
h1,h2,h3{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;text-wrap:balance;font-weight:600;}
h1{font-size:2rem;margin:0 0 .4rem;} h2{font-size:1.5rem;margin:0;} h3{font-size:1.1rem;margin:0 0 .5rem;}
p{max-width:72ch;} .lede{color:var(--muted);max-width:80ch;margin:.2rem 0 1rem;}
.head{border-bottom:1px solid var(--rule);padding-bottom:1rem;margin-bottom:1.5rem;}
.runs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;margin:1rem 0;}
.run{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:12px 14px;}
.run h3{margin-bottom:.3rem;}
.legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:.6rem 0 0;padding:0;list-style:none;font-size:.85rem;color:var(--muted);}
.legend li{display:flex;align-items:center;gap:6px;}
.badge{display:inline-block;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.68rem;letter-spacing:.06em;padding:1px 6px;border-radius:3px;border:1px solid currentColor;line-height:1.4;white-space:nowrap;}
.k-DETECTOR{color:var(--detector);background:color-mix(in srgb,var(--detector) 12%,transparent);}
.k-GAMEBOARD{color:var(--gameboard);border-style:dashed;}
.k-COMPUTATION{color:var(--computation);}
.k-HOST{color:var(--host);}
.k-CONVERSION{color:var(--conversion);}
.k-DECLARATION{color:var(--declaration);}
.k-PIN{color:var(--pin);border-style:dashed;}
.layer{margin:2.2rem 0 0;padding-top:1.2rem;border-top:3px solid var(--rule);}
.layer-head{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:baseline;margin-bottom:1rem;}
.layer-n{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-size:2.6rem;line-height:1;color:var(--muted);}
.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:18px;}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:14px 16px 12px;display:flex;flex-direction:column;gap:10px;min-width:0;}
.panel.wide{grid-column:1 / -1;}
.panel.diag{background:var(--band);border-style:dashed;}
.panel .eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.alg{margin:0;padding:0 0 0 12px;border-left:2px solid var(--rule);font-size:.92rem;}
.alg p{margin:0 0 .4rem;} .alg .ref{color:var(--muted);font-size:.8rem;}
.fig{overflow-x:auto;} .figure{width:100%;height:auto;max-width:100%;display:block;}
.figure text{font-family:system-ui,sans-serif;fill:var(--ink);font-size:12px;}
.figure .t-small{font-size:11px;fill:var(--muted);} .figure .t-tiny{font-size:9px;fill:var(--muted);}
.figure .t-mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;}
.figure .t-label{font-weight:600;} .figure .t-on-node{fill:var(--surface);font-size:11px;}
.figure .line{stroke:var(--ink);stroke-width:1.2;fill:none;} .figure .line-strong{stroke:var(--ink);stroke-width:2;}
.figure .line-faint{stroke:var(--muted);stroke-width:.8;opacity:.6;} .figure .grid{stroke:var(--rule);stroke-width:1;fill:none;}
.figure .line-inference{stroke:var(--muted);stroke-width:.6;opacity:.14;}
.figure .line-c{stroke:var(--computation);stroke-width:2;stroke-dasharray:6 4;}
.figure .arrow{stroke:var(--detector);stroke-width:2;}
.figure .node{fill:var(--ink);} .figure .node-far{fill:var(--soft);stroke:var(--ink);stroke-width:1.2;}
.figure .box{fill:var(--soft);stroke:var(--rule);} .figure .face{fill:var(--soft);stroke:var(--rule);}
.figure .mark-detector{fill:var(--detector);} .figure .bar{fill:var(--detector);}
.figure .stair{fill:none;stroke:var(--detector);stroke-width:2;}
.figure .rung{stroke:var(--muted);stroke-width:1.5;} .figure .rung-chosen{stroke:var(--detector);stroke-width:3;}
.figure .mark{stroke:var(--surface);stroke-width:1;} .figure .m-axes{fill:var(--c-axes);} .figure .m-face{fill:var(--c-face);}
.figure .m-body{fill:var(--c-body);} .figure .m-rest{fill:var(--c-rest);}
.figure .cell-medium{fill:var(--soft);stroke:var(--rule);} .figure .cell-well{fill:var(--declaration);opacity:.75;}
.figure .obj-lamp{fill:var(--host);} .figure .obj-reemit{fill:var(--declaration);} .figure .obj-detector{fill:var(--detector);} .figure .obj-wall{fill:var(--muted);}
.figure .store-node{fill:var(--gameboard);}
dl.nums{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:4px 12px;margin:0;font-size:.88rem;}
dl.nums dt{color:var(--muted);} dl.nums dd{margin:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;word-break:break-all;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap;}
.note{font-size:.85rem;color:var(--muted);margin:0;}
.missing{font-size:.9rem;padding:8px 10px;border:1px dashed var(--rule);border-radius:4px;color:var(--muted);}
.sources{font-size:.75rem;color:var(--muted);border-top:1px solid var(--rule);padding-top:6px;margin-top:auto;}
.control{display:flex;gap:10px;align-items:center;font-size:.85rem;flex-wrap:wrap;}
.control input[type=range]{flex:1;min-width:160px;}
.control select{font:inherit;}
.stages{list-style:none;padding:0;margin:0;display:grid;gap:8px;counter-reset:s;}
.stage{border:1px solid var(--rule);border-radius:4px;padding:8px 10px;font-size:.9rem;}
.stage.on{border-color:var(--detector);background:color-mix(in srgb,var(--detector) 8%,transparent);}
.stage .st{font-weight:600;} .stage .sl{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.82rem;margin:.2rem 0 0;word-break:break-word;}
.foot{margin-top:2rem;font-size:.85rem;color:var(--muted);border-top:1px solid var(--rule);padding-top:1rem;}
:focus-visible{outline:2px solid var(--detector);outline-offset:2px;}
@media (prefers-reduced-motion: no-preference){.stage{transition:border-color .15s;}}
"""

SCRIPT = """
(function(){
  document.querySelectorAll('[data-net]').forEach(function(box){
    var range=box.querySelector('input[type=range]'), out=box.querySelector('[data-out]'), svg=box.querySelector('svg');
    if(!range||!svg) return;
    function apply(){var t=parseInt(range.value,10); if(out) out.textContent=String(t);
      svg.querySelectorAll('[data-tick]').forEach(function(el){el.style.visibility=(parseInt(el.getAttribute('data-tick'),10)>t)?'hidden':'visible';});}
    range.addEventListener('input',apply); apply();
  });
  document.querySelectorAll('[data-stairs]').forEach(function(box){
    var sel=box.querySelector('select'); if(!sel) return;
    function apply(){box.querySelectorAll('.stair-series').forEach(function(el){el.hidden=(el.getAttribute('data-series')!==sel.value);});}
    sel.addEventListener('change',apply); apply();
  });
  document.querySelectorAll('[data-stepper]').forEach(function(box){
    var range=box.querySelector('input[type=range]'), stages=box.querySelectorAll('.stage'); if(!range) return;
    function apply(){var k=parseInt(range.value,10); stages.forEach(function(el,i){el.classList.toggle('on',i===k); el.style.opacity=(i<=k)?'1':'.45';});}
    range.addEventListener('input',apply); apply();
  });
})();
"""


def badge(kind: str) -> str:
    return f'<span class="badge k-{kind}">{kind}</span>'


def number_row(label: str, value: str, kind: str, source: str) -> str:
    return (
        f'<dt data-ref="label">{escape(label)}</dt>'
        f'<dd><span class="n" data-kind="{kind}" data-source="{escape(source, quote=True)}">{escape(value)}</span>{badge(kind)}</dd>'
    )


def run_card(run: RunRecord, role: str) -> str:
    rows = "".join(number_row(n.label, n.value, n.kind, n.source) for n in head_numbers(run))
    return (
        f'<section class="run"><h3 data-ref="run">{escape(role)}: <span class="ref">{escape(run.name)}</span></h3>'
        f'<p class="note" data-ref="folder">read from <span class="ref">{escape(str(run.folder))}</span></p><dl class="nums">{rows}</dl></section>'
    )


def legend() -> str:
    items = "".join(f"<li>{badge(kind)}<span>{escape(KIND_WORDS[kind])}</span></li>" for kind in KINDS)
    return f'<ul class="legend">{items}</ul>'


def panel_html(panel: Panel) -> str:
    classes = ["panel"]
    if panel.key in WIDE:
        classes.append("wide")
    if panel.key == "gameboard" or (panel.numbers and all(n.kind == "GAMEBOARD" for n in panel.numbers)):
        classes.append("diag")
    parts = [f'<article class="{" ".join(classes)}" id="p-{panel.key}">']
    eyebrow = "GAMEBOARD, a diagnostic" if "diag" in classes else f"Layer {panel.layer}"
    parts.append(f'<div class="eyebrow" data-ref="layer">{escape(eyebrow)}</div>')
    parts.append(f'<h3 data-ref="title">{escape(panel.title)}</h3>')
    if panel.algebra:
        parts.append('<blockquote class="alg">')
        for sentence, ref in panel.algebra:
            parts.append(
                f'<p data-ref="algebra">{escape(sentence)} <span class="ref" data-ref="{escape(ref, quote=True)}">({escape(ref)})</span></p>'
            )
        parts.append("</blockquote>")
    if panel.missing:
        parts.append(
            f'<div class="missing" data-ref="missing">Not recorded by these two runs: {escape(panel.missing)}.</div>'
        )
    else:
        fig = panel.figure
        kind = fig.get("kind")
        if kind == "cube_net":
            ticks = fig["ticks"]
            parts.append(
                f'<div data-net><div class="control"><label for="net-{panel.key}">the clicks up to the tick</label>'
                f'<input id="net-{panel.key}" type="range" min="{ticks[0]}" max="{ticks[-1]}" value="{ticks[-1]}" step="1">'
                f'<span class="n" data-kind="DETECTOR" data-source="events.jsonl: click.tick" data-out>{ticks[-1]}</span>{badge("DETECTOR")}</div>'
                f'<div class="fig">{figure(fig)}</div></div>'
            )
        elif kind == "staircase":
            options = "".join(
                f'<option value="{escape(s["name"], quote=True)}">{escape(s["name"])}</option>'
                for s in fig["series"]
            )
            parts.append(
                f'<div data-stairs><div class="control"><label for="stairs-{panel.key}">the set</label><select id="stairs-{panel.key}" data-ref="set">{options}</select></div>'
                f'<div class="fig">{figure(fig)}</div></div>'
            )
        elif kind == "stages":
            stages = fig["stages"]
            items = []
            for stage in stages:
                lines = "".join(
                    f'<p class="sl"><span class="n" data-kind="{stage["kind"]}" data-source="{escape(stage["source"], quote=True)}">{escape(line)}</span></p>'
                    for line in stage["lines"]
                )
                items.append(
                    f'<li class="stage"><div class="st">{escape(stage["title"])} {badge(stage["kind"])}</div>{lines}</li>'
                )
            parts.append(
                f'<div data-stepper><div class="control"><label for="step-{panel.key}">the record\'s life, step by step</label>'
                f'<input id="step-{panel.key}" type="range" min="0" max="{len(stages) - 1}" value="{len(stages) - 1}" step="1"></div>'
                f'<ol class="stages">{"".join(items)}</ol></div>'
            )
        elif fig:
            drawn = figure(fig)
            if drawn:
                parts.append(f'<div class="fig">{drawn}</div>')
        if panel.numbers:
            parts.append(
                '<dl class="nums">'
                + "".join(number_row(n.label, n.value, n.kind, n.source) for n in panel.numbers)
                + "</dl>"
            )
    if panel.note:
        parts.append(f'<p class="note" data-ref="note">{escape(panel.note)}</p>')
    sources = sorted({n.source for n in panel.numbers})
    if sources:
        parts.append(
            '<div class="sources">read from: '
            + "; ".join(f'<span class="ref" data-ref="src">{escape(s)}</span>' for s in sources)
            + "</div>"
        )
    parts.append("</article>")
    return "".join(parts)


def page_html(light: RunRecord, detector: RunRecord, panels: list[Panel]) -> str:
    parts = [
        "<title>The Algebra Visualizer</title>",
        f"<style>{CSS}</style>",
        '<div class="wrap">',
        '<header class="head">',
        "<h1>The Algebra Visualizer</h1>",
        '<p class="lede">One page in three layers, read from two runs\' records alone: the geometry that is the algebra, how it produces the physics, and the clicks. '
        "Every number carries its kind; nothing here is computed by the page, pinned, or compared with nature. "
        '<span class="ref" data-ref="design">docs/designs/algebra_visualizer/DESIGN.md</span>; the algebra quoted from <span class="ref" data-ref="algebra">docs/ALGEBRA.md</span>.</p>',
        legend(),
        '<div class="runs">',
        run_card(light, "Run 1, a light world"),
        run_card(detector, "Run 2, a world with a detector and clicks"),
        "</div></header>",
    ]
    for layer, (title, lede) in LAYERS.items():
        own = [p for p in panels if p.layer == layer]
        parts.append(
            f'<section class="layer" id="layer-{layer}"><div class="layer-head"><div class="layer-n" data-ref="layer">{layer}</div><div><h2>{escape(title)}</h2><p class="lede">{escape(lede)}</p></div></div>'
        )
        parts.append(legend())
        parts.append('<div class="panels">' + "".join(panel_html(p) for p in own) + "</div></section>")
    parts.append(
        '<footer class="foot"><p>A picture here is a diagnostic in every case; it is never compared with nature. Only a detector\'s reading is a measurement: a click, '
        "a count between clicks on the detector's own record, a ratio of such counts. A GameBoard reading is the host's view of the board. "
        "The page reads the record and computes no physics: no rule of the law is evaluated, no table of the engine is loaded, no record is stepped again; "
        "the only arithmetic is an exact difference or ratio of two recorded integers, labelled CONVERSION.</p></footer>"
    )
    parts.append("</div>")
    parts.append(f"<script>{SCRIPT}</script>")
    return "\n".join(parts)


def run_folder(runs: Path, name: str) -> Path:
    nested = runs / name / "run"
    return nested if nested.exists() else runs / name


def register_of(name: str) -> tuple[Path | None, str | None]:
    entry = REGISTERS.get(name)
    if entry is None:
        return None, None
    return ROOT / entry[0], entry[1]


def load_pair(runs: Path, light_name: str, detector_name: str) -> tuple[RunRecord, RunRecord]:
    light_register, light_block = register_of(light_name)
    detector_register, detector_block = register_of(detector_name)
    light = load_run(run_folder(runs, light_name), light_register, light_block)
    detector = load_run(run_folder(runs, detector_name), detector_register, detector_block)
    return light, detector


def print_rows(panels: list[Panel]) -> None:
    for key, label, value, kind, source in as_rows(panels):
        print(f"{kind:<11} {key:<10} {label}: {value}  [{source}]")
    for panel in panels:
        if panel.missing:
            print(f"{'(none)':<11} {panel.key:<10} not recorded by these two runs: {panel.missing}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("runs", type=Path, help="the runs directory (one folder per world, <name>/run)")
    parser.add_argument("--light", default="c_measured", help="the light world's folder name")
    parser.add_argument("--detector", default="slits_low", help="the detector world's folder name")
    parser.add_argument(
        "--render", type=Path, default=None, help="write the page to this file (headless without it)"
    )
    args = parser.parse_args(argv)
    try:
        light, detector = load_pair(args.runs, args.light, args.detector)
    except MissingRun as refused:
        print(str(refused), file=sys.stderr)
        return 2
    panels = build_panels(light, detector)
    if args.render is None:
        print_rows(panels)
        return 0
    args.render.write_text(page_html(light, detector, panels), encoding="utf-8")
    print(f"wrote {args.render} ({args.render.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
