"""The local player reveals received prefixes without global or future-state hints."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ASSET = Path(__file__).resolve().parents[1] / "src/event_universe/ui_assets/playback.html"


def player(recording, actions):
    executable = shutil.which("node")
    if executable is None:
        pytest.skip("headless player checks require Node; simulation does not")
    source = ASSET.read_text(encoding="utf-8")
    script = source[source.index('"use strict";') : source.index("</script></body>")]
    setup = r"""
const input=JSON.parse(require('node:fs').readFileSync(0,'utf8'));
const context=new Proxy({}, {get(){return ()=>{}}});
function element(){return {children:[],style:{},value:'',textContent:'',
  set innerHTML(value){throw Error('Configured labels must not become HTML');},
  append(...children){this.children.push(...children)},replaceChildren(){this.children=[]}};}
const elements=new Map();
const document={querySelector(id){if(!elements.has(id))elements.set(id,element());
  return elements.get(id)},createElement:element,
  createTextNode(text){return {textContent:text}},addEventListener(){}};
document.querySelector('#recording').textContent=JSON.stringify(input);
document.querySelector('#plane').value='0,1';document.querySelector('#zoom').value='1';
document.querySelector('#speed').value='1';
Object.assign(document.querySelector('#scene'),{getContext(){return context},
  getBoundingClientRect(){return {width:640,height:360}}});
const window={devicePixelRatio:1},location={search:''};
class ResizeObserver{observe(){}}function requestAnimationFrame(){}
function textTree(node){return [node.textContent,...(node.children||[]).map(textTree)].join(' ')}
"""
    result = subprocess.run(
        [executable, "-e", setup + script + actions],
        input=json.dumps(recording),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        timeout=10,
    )
    return json.loads(result.stdout)


def recording():
    return {
        "frames": [
            {"tick": tick, "cells": [], "transfers": [], "spatial_baselines": {"remote": [99]}}
            for tick in [100, 102, 107]
        ],
        "metadata": {"model": "distant world", "shape": [9, 9, 9], "link_ticks": 1},
        "observation": {
            "position": [4, 4, 4],
            "clock_kind": "completed-local-cycles",
            "samples": [
                {"audit_tick": 100, "clock": 0, "received_count": 0},
                {"audit_tick": 102, "clock": 1, "received_count": 1},
                {"audit_tick": 107, "clock": 1, "received_count": 2},
            ],
            "receipts": [
                {
                    "sequence": 1,
                    "clock": 1,
                    "kind": "field",
                    "port": 0,
                    "label": '<img src=x onerror="bad()">',
                    "values": {"amplitude": [0, 0, 0]},
                },
                {
                    "sequence": 2,
                    "clock": 1,
                    "kind": "disturbance",
                    "port": 5,
                    "label": "later arrival",
                    "values": {"stock": [7]},
                },
            ],
        },
    }


def test_observer_receipts_are_causal_distinguish_zero_and_rewind_without_world_data():
    result = player(
        recording(),
        r"""
const initial={cards:textTree($('#receivers')),rows:$('#observer-records').children.length,
  worldInitialized,worldHidden:$('#world-stage').hidden,legendHidden:$('#legend').hidden};
selectFrame(1);
const first={cards:$('#receivers').children.map(textTree),history:textTree($('#observer-records')),
  clock:$('#observer-clock').textContent,newCount:$('#observer-new').textContent};
selectFrame(2);
const last={cards:$('#receivers').children.map(textTree),clock:$('#observer-clock').textContent,
  newCount:$('#observer-new').textContent,timeline:$('#tick').textContent};
selectFrame(0);
console.log(JSON.stringify({initial,first,last,rewound:textTree($('#observer-records')),
  unknown:$('#receivers').children.map(textTree),worldInitialized,
  unchanged:JSON.stringify({frames,metadata,observation})===JSON.stringify(input)}));
""",
    )
    assert result["initial"]["rows"] == 0
    assert result["initial"]["cards"].count("Unknown") == 6
    assert result["initial"]["worldInitialized"] is False
    assert result["initial"]["worldHidden"] is True
    assert result["initial"]["legendHidden"] is True
    assert "amplitude: [0,0,0]" in result["first"]["cards"][0]
    assert "Unknown" not in result["first"]["cards"][0]
    assert '<img src=x onerror="bad()">' in result["first"]["history"]
    assert "later arrival" not in result["first"]["history"]
    assert result["first"]["clock"] == result["last"]["clock"] == "1"
    assert result["first"]["newCount"] == result["last"]["newCount"] == "1"
    assert "Retained last receipt" in result["last"]["cards"][0]
    assert "New arrival" in result["last"]["cards"][5]
    assert result["last"]["timeline"] == "Sample 3/3 · local clock 1"
    assert result["rewound"].strip() == ""
    assert all("Unknown" in card for card in result["unknown"])
    assert result["worldInitialized"] is False
    assert result["unchanged"] is True


def test_observer_playback_keeps_waiting_samples_and_explicit_world_audit_separate():
    result = player(
        recording(),
        r"""
setPlaying(true);animate(0);animate(250);
const first={index,clock:$('#observer-clock').textContent};animate(500);
const last={index,clock:$('#observer-clock').textContent,playing};
$('#perspective').value='world';$('#perspective').onchange();
const world={timeline:$('#tick').textContent,observerHidden:$('#observer-panel').hidden,
  worldHidden:$('#world-stage').hidden,worldInitialized,legend:textTree($('#legend'))};
$('#perspective').value='observer';$('#perspective').onchange();
console.log(JSON.stringify({first,last,world,restored:$('#tick').textContent,
  hiddenLegend:$('#legend').hidden,coordinate:playbackCoordinate(index)}));
""",
    )
    assert result["first"] == {"index": 1, "clock": "1"}
    assert result["last"] == {"index": 2, "clock": "1", "playing": False}
    assert result["world"]["timeline"] == "Tick 107 · 3/3"
    assert result["world"]["observerHidden"] is True
    assert result["world"]["worldHidden"] is False
    assert result["world"]["worldInitialized"] is True
    assert "remote" in result["world"]["legend"]
    assert result["restored"] == "Sample 3/3 · local clock 1"
    assert result["hiddenLegend"] is True
    assert result["coordinate"] == 2
