"""Census of the gravity blocks (manager rule 4): per block, monomials by degree, every monomial with an `a` factor,
constants, rank-4 (degree-3) monomials with their potential sign, designations, support facts. Writes
results/gravity/census.json. Usage: python universe24/demos/gravity/census.py"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from universe24.core import Block, compose
from universe24.observe import gravity as og
from universe24.tests import test_gravity as tg

OUT = ROOT / "universe24/results/gravity"


def block_census(blocks, blk):
    only = [Block(b.gears, b.terms if b is blk else (), name=b.name, vacuum=b.vacuum, Q=b.Q) for b in blocks]
    T = compose(*only)
    names = T.names
    deg = [0, 0, 0, 0]
    a_reads, quartic = [], []
    for m in T.monomials:
        deg[m.degree] += 1
        txt = f"u[{names[m.target]}] += {m.coeff} * " + " * ".join(
            f"{f.field}[{names[f.gear]}]{f.offset}" for f in m.factors)
        if any(f.field == "a" for f in m.factors):
            a_reads.append(txt)
        if m.degree == 3:
            quartic.append(txt)
    return {"monomials": len(T.monomials), "by_degree": deg, "constants": deg[0], "a_read_monomials": a_reads,
            "n_a_reads": len(a_reads), "rank4_monomials": len(quartic), "rank4_examples": quartic[:6],
            "designated": len(T.designations),
            "support_facts": {f"{k[0]} <- {list(k[1])}": v for k, v in og.support_report(T).items()}}


def main():
    out = {"written_utc": subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()}
    for name, mk in tg.ALL_SYSTEMS.items():
        Q, blocks = mk()
        out[name] = {blk.name: block_census(blocks, blk) for blk in blocks if blk.name != "ref"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "census.json").write_text(json.dumps(out, indent=1) + "\n")
    for name in out:
        if name == "written_utc":
            continue
        for b, c in out[name].items():
            print(name, b, c["by_degree"], "a-reads", c["n_a_reads"], "rank4", c["rank4_monomials"], "designated",
                  c["designated"], "support", sum(c["support_facts"].values()))


if __name__ == "__main__":
    main()
