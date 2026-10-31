"""Tensor24's page tool (VIEW1, the owner's word of about 06:50 UTC): a short run of the click world drawn as one page
holding its record's count of click lines, and a record of no click line drawn as a page that says so."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24 import main
from tensor24.runner.files import NAMES

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "look" / "tensor24_page.py"


def test_the_page_holds_its_records_click_lines_and_says_so_where_the_record_holds_none(tmp_path):
    """Yes: the click world's first two rounds drawn, the page holding the record's count of click lines, never typed
    here, and the decoder's verdicts; no: that record with its click lines left out, a page that says it holds none."""
    *paths, setting = [ROOT / "examples" / "tensor24-click" / f"{name}.json" for name in NAMES]
    held = json.loads(setting.read_text(encoding="utf-8"))
    held["ticks"] = 2
    (tmp_path / "setting.json").write_text(json.dumps(held), encoding="utf-8")
    record, bare = tmp_path / "record.jsonl", tmp_path / "bare.jsonl"
    assert main.ran([*paths, tmp_path / "setting.json"], record) == []
    lines = record.read_text(encoding="utf-8").splitlines()
    clicks = len([x for x in lines if json.loads(x)["kind"] == "click"])
    bare.write_text(f"{lines[0]}\n{lines[-1]}\n", encoding="utf-8")
    pages = []
    for read, ledger in ((record, ["record.ledger.jsonl"]), (bare, [])):
        page = read.with_suffix(".html")
        named = [str(tmp_path / x) for x in ledger]
        tool = [sys.executable, "-I", str(TOOL), str(read), *named, "--page", str(page), "--world", "w"]
        assert subprocess.run(tool, capture_output=True, text=True).returncode == 0
        pages.append(page.read_text(encoding="ascii"))
    drawn, empty = pages
    assert clicks and f'id="summary">{clicks} click lines in the run\'s 2 rounds' in drawn
    assert f'"total":{clicks},' in drawn and '"kind":"HOLDS"' in drawn
    assert '"netted":' in drawn and "b.netted" in drawn  # the key the page's script reads
    assert "<title>w running</title>" in drawn
    assert 'id="summary">The record holds no click line: not in the click world.' in empty
    assert '"total":0,' in empty and '"kind":"NO CLICK"' in empty
    assert '"kind":"HOLDS"' not in empty
