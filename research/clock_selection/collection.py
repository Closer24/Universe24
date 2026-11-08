"""Build a passive landing page for existing complete Presenter packages."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def build(manifest_path,output):
    manifest_path=Path(manifest_path).resolve();output=Path(output).resolve()
    if output.exists():raise FileExistsError(output)
    raw=manifest_path.read_bytes();data=json.loads(raw)
    if data.get("format")!="universe24-research-presentation-collection-v1":raise ValueError("Unsupported collection")
    cards=[];sources=[]
    def target(relative):
        path=(HERE/relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():raise ValueError("Missing repository evidence: "+relative)
        sources.append({"path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
        return html.escape(os.path.relpath(path,output),quote=True)
    for entry in data["studies"]:
        package=(HERE/entry["package"])
        package_manifest=json.loads((package/"manifest.json").read_text())
        if not package_manifest["complete_recordings"] or not package_manifest["read_only"]:
            raise ValueError("Collection requires a complete read-only package")
        viewer=target(str(package.relative_to(HERE)/"index.html"))
        report=target(entry["report"]);audit=target(entry["audit"])
        if json.loads((HERE/entry["audit"]).read_text()).get("passed") is not True:
            raise ValueError("This reviewed collection requires a passing audit certificate")
        target(str(package.relative_to(HERE)/"manifest.json"))
        count=len(package_manifest["experiments"]);frames=package_manifest["frames"]
        cards.append(f'<article><p class="status">Independent replay passed</p><h2>{html.escape(entry["title"])}</h2><p>{html.escape(entry["description"])}</p><p class="scope">{html.escape(entry["scope"])}</p><p>{count} complete examples · {frames:,} recorded states · {len(package_manifest["pages"])} page(s)</p><nav><a class="primary" href="{viewer}">Open experiments</a><a href="{report}">Read evidence</a><a href="{audit}">Audit record</a></nav></article>')
    ledger=target("decision_ledger.md");physics=target("physics_targets/README.md")
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Universe24 — Research recordings</title><style>
    :root{color-scheme:light;font:17px/1.55 system-ui,sans-serif;color:#20333b;background:#f4f2ea}body{margin:0 auto;max-width:1200px;padding:32px 22px 64px}h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;margin:10px 0 20px}header{max-width:850px;margin-bottom:30px}.eyebrow{letter-spacing:.22em;font-size:.8rem;color:#557077}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:20px}article{border:1px solid #b9c6c4;border-radius:16px;background:#fffef9;padding:24px}h2{line-height:1.2;font-size:1.35rem;margin:12px 0}.status{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:#35665b}.scope{color:#665544;border-left:3px solid #b1a183;padding-left:12px}nav{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;margin-top:20px}a{color:#214f65;text-underline-offset:3px}a.primary{padding:10px 15px;border-radius:8px;background:#203b47;color:white;text-decoration:none}footer{margin-top:32px;border-top:1px solid #b9c6c4;padding-top:20px;font-size:.92rem}code{font-size:.9em}
    </style><header><p class="eyebrow">UNIVERSE24 · ONE BOARD · ONE RULE</p><h1>Research recordings</h1><p>Choose a study, then choose an experiment. The unchanged Presenter displays the complete recorded cube through clocks and gears. Drag to rotate, reset the view to see the full cube, or inspect any of its 48 channels.</p><p>These are finite computational results. Every control remains available. A displayed arithmetic event is not automatically a photon, approval message or physical measurement.</p></header><main class="grid">'''+''.join(cards)+f'''</main><footer><p><a href="{ledger}">Hypotheses and next decisions</a> · <a href="{physics}">Physical targets and missing tests</a></p><p>Serve the repository with <code>python -m http.server 8000</code>, then open this page in a JavaScript-enabled browser. Attachment previews may not execute the Presenter. The landing page and viewer never evolve the model or select a route.</p></footer></html>'''
    output.mkdir(parents=True,exist_ok=False);(output/"index.html").write_text(page)
    result={"format":"universe24-research-presentation-collection-build-v1","manifest_sha256":hashlib.sha256(raw).hexdigest(),
        "builder_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"studies":len(cards),"inputs":sources,
        "index_sha256":hashlib.sha256(page.encode()).hexdigest(),"read_only":True,"scientific_assessment":"Use linked corrected reports and independent certificates; packaging is not validation."}
    (output/"manifest.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"studies":len(cards),"index":str(output/"index.html")}));return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest",type=Path,required=True);parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv);build(args.manifest,args.output)


if __name__=="__main__":main()
