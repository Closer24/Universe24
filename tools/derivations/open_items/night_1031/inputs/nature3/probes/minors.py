"""NATURE3's minors probe on node-all 9d75a4904's records and decoder (writer E's guard in records.read, shadow.books and
shadow.meetings). Each forged record is written to the forged folder and read back through the guard.
- S1's no: the silent edge (2, 4) at round 82, site 0, made to pass one quantum, its mate and both lines moved;
- H1's no: one mated pair moved by one quantum at round 115, site 0, both lines moved, so F1 is kept;
- G1's no: an in-site mated pair (held 1, tied 2) forged at site 150, round 21 on the mesh record;
- M1's yes: the click record cut to its one-quantum meeting places;
- R1's nos: run 2 with one mated pair moved at round 150, site 4; the 100-round record with one pair moved at round 60;
- C1' on NATURE2's forged mesh record (a mated across pair between quiet sites 110 and 111 at round 60);
- the guard's reach: a header dial forged even, and NATURE2's forged across pair on the click world (mesh 0);
- K1's dial check on the five records and on the forged dial;
- the local bounds: CHSH over its 16 local strategies, Mermin over its 64 local assignments.
Whole numbers only; Rule3's carry the one division; no //; paths by joinpath.

Usage: python3 -I minors.py <tree> <runs folder> <forged folder> <nature2 runs folder>
"""

import copy
import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.decoder import records, shadow  # noqa: E402

RUNS, FORGED, N2RUNS = Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])


def rows(path):
    return [json.loads(t) for t in Path(path).read_text(encoding="utf-8").splitlines() if t.strip()]


def write(name, body):
    path = FORGED.joinpath(name)
    path.write_text("".join(json.dumps(e) + "\n" for e in body), encoding="utf-8")
    return path


def guarded(path):
    held, cause = records.read(str(path))
    if held is None:
        return f"refused: {cause[:140]}", None
    return "admitted", held


def find_line(body, r, x, t):
    for n, e in enumerate(body):
        if e.get("kind") == "click" and (e["round"], e["site"], e["train"]) == (r, x, t):
            return n
    return None


def move_pair(body, r, x, t, u, d):
    """Move the in-site side (t to u) by d at place (r, x), its mate (u to t) by -d, and both lines' q with them."""
    nt, nu = find_line(body, r, x, t), find_line(body, r, x, u)
    for n, w, dd in ((nt, u, d), (nu, t, -d)):
        for s in body[n]["sides"]:
            if s[0] == w:
                s[1] += dd
        body[n]["q"] += dd


def structure(clicks):
    count = {}
    places = {}
    for e in clicks:
        p = places.setdefault((e["round"], e["site"]), set())
        for s in e.get("sides", []):
            if s[1] != 0:
                p.add((min(e["train"], s[0]), max(e["train"], s[0])))
    for p in places.values():
        count[len(p)] = count.get(len(p), 0) + 1
    return dict(sorted(count.items()))


def alike_rounds(clicks, n_sites):
    per = {}
    for e in clicks:
        per.setdefault(e["round"], {}).setdefault(e["site"], []).append(
            (e["train"], e["q"], tuple((s[0], s[1]) for s in e.get("sides", []))))
    apart = [r for r in sorted(per) if len({tuple(v) for v in per[r].values()}) != 1 or len(per[r]) != n_sites]
    return len(per) - len(apart), len(per), apart[:1]


def first_across(clicks):
    first, carries = {}, {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if e["site"] not in first:
            first[e["site"]] = e["round"]
    for e in clicks:
        if e["round"] == first[e["site"]] and e.get("across"):
            carries[e["site"]] = True
    return sum(1 for x in first if carries.get(x)), len(first)


def per_node(clicks):
    def meets(e):
        return [s for s in e.get("sides", []) if s[1] != 0] + [s for s in e.get("across", []) if s[2] != 0]
    first = {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if meets(e):
            first.setdefault(e["site"], e["round"])
    start = min(first.values())
    partners = {}
    for e in clicks:
        if first.get(e["site"]) == e["round"]:
            partners.setdefault(e["site"], set()).update(s[1] for s in e.get("across", []) if s[2] != 0)
    late = [x for x in first if first[x] > start]
    caused = [x for x in late if any(first.get(y, first[x]) < first[x] for y in partners.get(x, set()))]
    return len(caused), len(late)


def dial_check(body):
    head = body[0]
    files = {f["name"]: f["text"] for f in head.get("files", [])}
    key = json.loads(files["universe.json"])["chosen"]["key"]
    dial, birth = head.get("dial"), head.get("birth")
    end = body[-1]
    edged = bool(end.get("teeth")) or bool(end.get("across"))
    whole_multiple = carry(dial, key, 0)[1] == 0 if edged else dial == key
    ok = whole_multiple and birth + birth + 1 == dial
    return f"{'SHOWN' if ok else 'NOT SHOWN'}: dial {dial}, key {key}, edges {'stand' if edged else 'none'}, birth {birth}"


def main():
    click = rows(RUNS.joinpath("click200_1.jsonl"))
    mesh = rows(RUNS.joinpath("mesh_1.jsonl"))
    # S1's no
    f = copy.deepcopy(click)
    n2, n4 = find_line(f, 82, 0, 2), find_line(f, 82, 0, 4)
    side24 = [s for s in f[n2]["sides"] if s[0] == 4][0]
    base_q = side24[1]
    move_pair(f, 82, 0, 2, 4, 1)
    g, held = guarded(write("s1_no.jsonl", f))
    books = shadow.books(held)["kind"] if held else "-"
    print(f"S1's no (edge (2, 4) at round 82, site 0, q {base_q} to {base_q + 1}, mate and lines moved): the guard {g};"
          f" books {books}; structure by what passes {structure([e for e in f if e.get('kind') == 'click'])}"
          f" against {structure([e for e in click if e.get('kind') == 'click'])}")
    # H1's no
    f = copy.deepcopy(click)
    move_pair(f, 115, 0, 2, 3, 1)
    g, held = guarded(write("h1_no.jsonl", f))
    books = shadow.books(held)["kind"] if held else "-"
    al, tot, first_apart = alike_rounds([e for e in f if e.get("kind") == "click"], 27)
    print(f"H1's no (edge (2, 3) at round 115, site 0, moved by one, mate and lines moved): the guard {g}; books {books};"
          f" {al} of {tot} rounds alike, first apart {first_apart}")
    # G1's no
    f = copy.deepcopy(mesh)
    assert find_line(f, 21, 150, 1) is None and find_line(f, 21, 150, 2) is None
    birth = f[0]["birth"]
    fake = [{"kind": "click", "round": 21, "site": 150, "train": 1, "q": 1, "sides": [[2, 1, birth, birth]], "across": []},
            {"kind": "click", "round": 21, "site": 150, "train": 2, "q": -1, "sides": [[1, -1, birth, birth]], "across": []}]
    body = [f[0]] + sorted(f[1:-1] + fake, key=lambda e: (e["round"], e["site"], e["train"])) + [f[-1]]
    g, held = guarded(write("g1_no.jsonl", body))
    books = shadow.books(held)["kind"] if held else "-"
    c, n = first_across([e for e in body if e.get("kind") == "click"])
    c0, n0 = first_across([e for e in mesh if e.get("kind") == "click"])
    print(f"G1's no (an in-site mated pair, held and tied, at site 150, round 21): the guard {g}; books {books};"
          f" sites whose first line carries an across side {c} of {n} (the record: {c0} of {n0})")
    # M1's yes
    held, _ = records.read(str(RUNS.joinpath("click200_1.jsonl")))
    lines_ = [e for e in click if e.get("kind") == "click"]
    places = shadow.placed(lines_, set())
    good = {p for p, h in places.items() if shadow.met(h)}
    body = [click[0]] + [e for e in lines_ if (e["round"], e["site"]) in good] + [click[-1]]
    g, held2 = guarded(write("m1_yes.jsonl", body))
    if held2:
        v = shadow.meetings(held2)
        b = shadow.books(held2)
        print(f"M1's yes (the click record cut to its {len(good)} one-quantum places): the guard {g}; books {b['kind']};"
              f" meetings {v['kind']}: {v['cause'][:120]}")
    else:
        print(f"M1's yes: the guard {g}")
    # R1's nos
    f = rows(RUNS.joinpath("click200_2.jsonl"))
    base = [json.dumps(e) for e in f]
    move_pair(f, 150, 4, 2, 3, 1)
    moved = [json.dumps(e) for e in f]
    apart = [n for n, (x, y) in enumerate(zip(base, moved)) if x != y]
    print(f"R1's no (run 2 with one mated pair moved at round 150, site 4): the first line apart is line {apart[0]} after"
          f" the header, {len(apart)} lines apart")
    short = rows(RUNS.joinpath("click100_1.jsonl"))
    move_pair(short, 60, 0, 2, 3, 1)
    sc = [json.dumps(e) for e in short if e.get("kind") == "click"]
    lc = [json.dumps(e) for e in click if e.get("kind") == "click" and e["round"] <= 100]
    alike = sum(1 for x, y in zip(sc, lc) if x == y)
    print(f"R1's prefix no (the 100-round record with one pair moved at round 60): {alike} of {len(sc)} lines alike:"
          f" {'SHOWN' if alike == len(sc) == len(lc) else 'NOT SHOWN'}")
    # C1' on NATURE2's forged mesh record
    nc = rows(RUNS.joinpath("mesh_nocause_nature2.jsonl"))
    c, n = per_node([e for e in nc if e.get("kind") == "click"])
    c0, n0 = per_node([e for e in mesh if e.get("kind") == "click"])
    print(f"C1' (the per-Node-clock order) on NATURE2's forged mesh record: {c} of {n} later sites"
          f" ({'SHOWN' if c == n else 'NOT SHOWN'}); on the record {c0} of {n0}")
    # the guard's reach and K1's dial check
    f = copy.deepcopy(click)
    f[0]["dial"] = f[0]["dial"] + 1
    g, held = guarded(write("k1_dial_plus1.jsonl", f))
    books = shadow.books(held)["kind"] if held else "-"
    print(f"the guard's reach, a header dial forged even (152,434,288): the guard {g}; books {books}; K1's dial check"
          f" {dial_check(f)}")
    g, held = guarded(N2RUNS.parent.joinpath("probes", "forged", "click200_nocause_1.jsonl"))
    books = shadow.books(held)["kind"] if held else "-"
    print(f"the guard's reach, NATURE2's across pair forged on the click world (mesh 0, the end line lists no across):"
          f" the guard {g}; books {books}")
    for w in ("t24", "live", "well", "mesh", "click200"):
        print(f"K1's dial check, {w}: {dial_check(rows(N2RUNS.joinpath(f'{w}_1.jsonl')))}")
    # the local bounds
    signs = (1, -1)
    best_chsh = max(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1 for a0 in signs for a1 in signs for b0 in signs for b1 in signs)
    count_chsh = len([1 for a0 in signs for a1 in signs for b0 in signs for b1 in signs])
    best_m = max(a * b1 * c1 + a1 * b * c1 + a1 * b1 * c - a * b * c
                 for a in signs for a1 in signs for b in signs for b1 in signs for c in signs for c1 in signs)
    count_m = len([1 for a in signs for a1 in signs for b in signs for b1 in signs for c in signs for c1 in signs])
    print(f"the local bounds: CHSH {best_chsh} over its {count_chsh} local strategies ({1000 * best_chsh} per mille);"
          f" Mermin {best_m} over its {count_m} local assignments ({1000 * best_m} per mille)")


main()
