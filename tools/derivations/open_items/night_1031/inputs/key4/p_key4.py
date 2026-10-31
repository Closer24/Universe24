"""p_key4: the click's unit read from the world's initialization by a copy of node-all's loader, against node-all's
own runs (p_key4_all.py's output).

The copy: tree_key4, node-all 9d75a4904's src with key4_src.diff: the setting lays the world's one key as the key's
middle; load.keyed is the load's promise on it; load.dial computes the click's unit K = senses middle + 1; edging lays
every side's edge dial D = (kappa div senses) K from it and returns its scale with the remainder its carry leaves;
load.dialled lays every side's tooth at its birth, (D - 1) div senses, and refuses a remainder and an even D by name;
laid_out takes the crossing's scale from the load; the decoder names a card's key off the header's dial;
universe.chosen.key is retired by name. The worlds: the five shipped worlds'
files migrated by migrate.py. This process never reads a key from node-all's files, and nothing hands the read an
integer.

L  each migrated world's load on the copy: its middle, the node's K, every side's D, D over K, the births.
U  the click world, uniform: the copy's load reads the laid middle and computes K, D and the births; 200 rounds by the
   engine's act on the layout the read gives; the click lines one by one and the end digest against node-all's.
The no's, each a change to the read, the plan or the files:
E1 an even dial at one side of one tooth: D one more on the giver's side to the taker, at site 0 alone;
E2 an even unit everywhere: the read's form mutated to senses middle + senses; refused by name at the load (dialled),
   and with that promise mutated away, run;
O  another form, odd at this middle: axes middle + 1;
I  the key laid but the read ignoring it: keyed mutated to give the middle 0;
M  the read handing the middle as the click's unit: K = middle, even here; refused by name, and with the promise
   mutated away, run;
R1 to R6 a second key laid, or none: the copy's load promise and the copy's format on the files as written to no/, and
   the run tool (main.ran) on them;
R7 an edged monomial of four legs: J's potential joined with one live monomial (factor 1) on the giver's first two rows
   and the taker's, a plan no file lays (the probe adds it at the load's join): refused by name, nothing loaded; and with
   the promise mutated away, every edge's two teeth at birth, and 200 rounds' edge books;
R8 the scale's carry leaving a remainder, as kappa + 1 leaves it (the ninth code reader's K1, whose scale and shares are
   kappa's own): edging's remainder one more, refused by name;
S  kappa from the structure alone (the Boss's ruling on MIN1's case (c)): each world's scale as laid and with every
   chosen strength at 1; the click world with its hold at 0, both ways;
N  today's integer under the new name, middle 50,811,429 (the physicist's m6, the mathematician's MINOR 9): the format
   and the load, K and D, and the first-click record's cards and click lines against node-all's pins;
B  the width (the mathematician's MINOR 3): a middle of 2^width - 1 and of 2^width, the format's and the load's
   departures, K's and D's bits;
W  the five migrated worlds' records by main.ran on the copy (worlds4.py), each read by the copy's decoder, against
   node-all's: every line after the header byte for byte, the header but its files, the ledger, which file digests
   moved; the lines write.py would write, against node-all's and its tests/tensor24_prefixes.jsonl;
C  the copy's decoder on the records p_key4_all.py wrote: the click world's first-click record and its two mutants.
Whole numbers; Rule3's carry the one division; paths by joinpath; the probe's indices are the loader's flags.

Run: python -I p_key4.py <tree_key4> <tree_all> <node-all's out folder> <this run's out folder>, Python 3.14.
"""

import copy
import json
import sys
import tempfile
from pathlib import Path

TREE, ALL, TODAY, OUT = (Path(x) for x in sys.argv[1:5])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

import tensor24  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.decoder import records as decoding  # noqa: E402
from tensor24.main import ENGINE as engine  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner import run as runner  # noqa: E402
from tensor24.runner.files import NAMES, departures, sites_of, star  # noqa: E402

import worlds4  # noqa: E402

assert Path(tensor24.__file__).resolve().is_relative_to(TREE.resolve()), tensor24.__file__
SHOWN = 170  # the characters of a departure printed; its full length named beside it
examples = TREE.joinpath("examples")
OUT.mkdir(parents=True, exist_ok=True)


def say(line):
    print(line, flush=True)


def shown(line):
    return f"{line[:SHOWN]}{'' if len(line) <= SHOWN else f' ... ({len(line)} characters)'}"


def files(world):
    return [json.loads(examples.joinpath(world, f"{n}.json").read_text(encoding="utf-8")) for n in NAMES]


u, p, st = files("tensor24-click")
shape = p["shape"]
sites, axes = sites_of(shape), len(shape)
made = engine.made(star(axes))
senses, _ = carry(len(star(axes)), axes, 0)
today = [json.loads(x) for x in TODAY.joinpath("click_all.jsonl").read_text(encoding="utf-8").splitlines()]
summary, before = today[-1], today[:-1]


def read(universe, setting, **mutant):
    """The copy's load on the files as held, with the read's functions mutated where named: the loaded, its departures."""
    kept = {name: getattr(loading, name) for name in mutant}
    for name, value in mutant.items():
        setattr(loading, name, value)
    try:
        return loading.load(universe, setting, sites, *made)
    finally:
        for name, value in kept.items():
            setattr(loading, name, value)


def go(layout, s, rounds):
    """The rounds by the engine's act, the click lines by the runner's clicked() with the edges' partners, the end state
    and every round's quotients."""
    partners = runner.joined(layout.click, len(layout.click.weight[0]))
    events, read_, quotients = [], s, []
    for at in range(1, rounds + 1):
        end, clicks = engine.act(layout, read_)
        events += runner.clicked(at, read_, end, clicks, partners, layout.nb)
        quotients.append(clicks)
        read_ = end
    return events, read_, quotients


def against(name, layout, s):
    """A run's click lines one by one against node-all's, its end digest and its end's counts (a, b, r, rd) alone."""
    events, end, _ = go(layout, s, summary["rounds"])
    events = [json.loads(json.dumps(e)) for e in events]  # as node-all's were written and read
    differing = sum(1 for x, y in zip(events, before, strict=False) if x != y) + abs(len(events) - len(before))
    alike = int(runner.digest(runner.stated(end)) == summary["end"])
    counts = int(runner.digest(json.dumps([x.tolist() for x in end[:-1]])) == summary["counts"])
    say(f"{name}: lines {len(events)} against node-all's {len(before)}; lines differing {differing}; end digest alike"
        f" {alike}; the end's counts (a, b, r, rd) alike {counts}")
    return differing, alike


def facts(held):
    """The layout the read gives, the click's unit K read back as D over the load's scale (the remainder asserted 0),
    every side's dial D (its set), the births (their set), the state."""
    layout = engine.layout(u, shape, held)
    s = engine.state(*held.state)
    dials = sorted(set(layout.click.key.ravel().tolist()))
    unit, rest = carry(dials[0], held.scale, 0)
    assert rest == 0, rest
    return layout, unit, dials, sorted(set(s.k.ravel().tolist())), s


def unchecked(key, senses_, spare):
    """The dials' promise mutated away: the births alone, nothing named."""
    birth, _ = carry(key - 1, senses_, 0)
    return birth, []


say(f"the tree: {TREE.name}, tensor24 from {Path(tensor24.__file__).resolve().relative_to(TREE.resolve())}")
# L: every migrated world's load on the copy
for world in sorted(f.name for f in examples.glob("*/")):
    wu, wp, ws = files(world)
    w_made = engine.made(star(len(wp["shape"])))
    w_held, w_found = loading.load(wu, ws, sites_of(wp["shape"]), *w_made)
    assert not w_found, w_found
    _, _, w_key = w_held.click
    w_d = sorted(set(w_key.ravel().tolist()))
    w_unit = loading.dial(carry(len(star(len(wp["shape"]))), len(wp["shape"]), 0)[0], ws["middle"])
    w_back, w_rest = carry(w_d[0], w_held.scale, 0)
    say(f"L {world}: universe.chosen holds a key {int('key' in wu['chosen'])}; setting.middle {ws['middle']}; the node's K"
        f" {w_unit}; edging's scale {w_held.scale}; the edge dial D {w_d} on {w_key.shape[0]} sides, D over the scale"
        f" {w_back} (remainder {w_rest}); every tooth born at {sorted(set(w_held.state[-1].ravel().tolist()))}")

# U: the read on the migrated click world, uniform
say(f"U: the files read: {examples.joinpath('tensor24-click').relative_to(TREE)}; universe.chosen holds a key:"
    f" {int('key' in u['chosen'])}; setting.middle {st['middle']}; the probe types no key")
held, found = read(u, st)
assert not found, found
layout, K, dials, born, s0 = facts(held)
scale, rest = held.scale, 0
assert K == loading.dial(senses, st["middle"])
say(f"U: the read: K = {senses} x {st['middle']} + 1 = {K}; edging's scale {scale}; every side's D {dials} = {scale} K, its"
    f" remainder by {senses} {sorted(set(carry(layout.click.key, senses, 0)[1].ravel().tolist()))}; every tooth born at"
    f" {born} ({s0.k.size} teeth), D's middle; the Mesh couplings laid not 0: {int((layout.click.across != 0).sum())}"
    f" (this world's mesh is 0)")
u_diff, u_alike = against("U uniform, by the read", layout, s0)

trains = held.trains
giver, taker = [t for t in range(len(trains)) if trains.tied[t]]  # the tied trains in the file's order
count = len(trains)
field = layout.click.key + 0 * s0.k
field[giver * count + taker, 0] = field[giver * count + taker, 0] + 1
say(f"E1: the giver is train {giver} and the taker {taker} by the loader's flags; the giver's side to the taker at its own"
    f" Node-clock, site 0, on the dial {field[giver * count + taker, 0]}, every other on {dials}")
against("E1 an even dial at one side of one tooth", layout._replace(click=layout.click._replace(key=field)), s0)

for name, mutant in (
    ("E2 an even unit everywhere, the form senses middle + senses", {"dial": lambda ends, middle: ends * middle + ends}),
    ("O another form, odd at this middle, axes middle + 1", {"dial": lambda ends, middle: axes * middle + 1}),
    ("I the key laid, the read ignoring it (middle 0)", {"keyed": lambda universe, setting: (0, [])}),
    ("M the read handing the middle as the click's unit", {"dial": lambda ends, middle: middle}),
):
    held_m, found_m = read(u, st, **mutant)
    tag = name.split()[0]
    if found_m:
        say(f"{tag}: refused at the load, loaded {int(held_m is not None)}; named {len(found_m)}:")
        for line in found_m:
            say(f"    load: {shown(line)}")
        held_m, found_m = read(u, st, dialled=unchecked, **mutant)
        assert not found_m, found_m
        name = f"{name}, the even-dial promise mutated away"
    layout_m, k_m, d_m, b_m, s_m = facts(held_m)
    say(f"{tag}: the mutated read's K {k_m}, every side's D {d_m}, its click teeth born at {b_m}")
    against(name, layout_m, s_m)

# R1 to R6: a second key laid, or none: the copy's load promise, the copy's format and the run tool, on the files
nos = []
u1 = copy.deepcopy(u)
u1["trains"][giver]["key"] = K + senses  # another odd key, at the giver's teeth alone
nos.append(("R1 a second key at one train: the giver's card lays its own odd key", u1, st))
s2 = copy.deepcopy(st)
s2["middle"] = [st["middle"] + 1] + [st["middle"]] * (sites - 1)
nos.append(("R2 a second key at one site: the middle laid per site, site 0's one more", u, s2))
s3 = copy.deepcopy(st)
s3["middle"] = [[t, x, st["middle"] + int(t == giver and x == 0)] for t in range(count) for x in range(sites)]
nos.append(("R3 KEY2's form: the middle laid per tooth (train, site, middle), the giver's at site 0 one more", u, s3))
u4 = copy.deepcopy(u)
u4["chosen"]["key"] = K
nos.append(("R4 the retired key kept: universe.chosen.key beside the setting's middle", u4, st))
s5 = {k: v for k, v in st.items() if k != "middle"}
nos.append(("R5 no key laid: neither the setting's middle nor any other", u, s5))
s6 = {**s5, "key": K}
nos.append(("R6 today's integer moved under its old name, setting.key, with no middle", u, s6))


def tried(name, universe, setting):
    """The files written to no/, the copy's load promise, the copy's format and the run tool on them."""
    held_r, found_r = read(universe, setting)
    folder = OUT.joinpath("no", name.split()[0])
    folder.mkdir(parents=True, exist_ok=True)
    for n, held_file in zip(NAMES, (universe, p, setting), strict=True):
        folder.joinpath(f"{n}.json").write_text(json.dumps(held_file), encoding="utf-8")
    form = departures(*[folder.joinpath(f"{n}.json") for n in NAMES])
    say(f"{name}: loaded {int(held_r is not None)}; the load's promise names {len(found_r)}:")
    for line in found_r:
        say(f"    load: {shown(line)}")
    say(f"  the format names {len(form)}:")
    for line in form:
        say(f"    files: {shown(line)}")
    record = folder.joinpath("record.jsonl")
    named = main.ran([folder.joinpath(f"{n}.json") for n in NAMES], record)
    say(f"  the run tool (main.ran) names {len(named)}, the format's first (alike: {int(named == form)}); a record or"
        f" a ledger written: {int(record.exists() or runner.ledger_of(record).exists())}")
    return held_r, found_r, form, named


for name, universe, setting in nos:
    tried(name, universe, setting)

# R7: an edged monomial of four legs, the giver's first two rows and the taker's
real = loading.joined
rows = [int(trains.first[giver]), int(trains.first[giver]) + 1, int(trains.first[taker]), int(trains.first[taker]) + 1]
four = (np.array([1], dtype=object), tuple(np.array([r], dtype=np.intp) for r in rows))
say(f"R7: one live monomial of four legs laid at the load's join, factor 1, on the rows {rows} (the giver's first two and"
    f" the taker's), no file laying it")
held_7, found_7 = read(u, st, joined=lambda *potentials: real(*potentials, four))
say(f"R7 an edged monomial of four legs: loaded {int(held_7 is not None)}; the load's promise names {len(found_7)}:")
for line in found_7:
    say(f"    load: {shown(line)}")
held_7, found_7 = read(u, st, joined=lambda *potentials: real(*potentials, four), dialled=unchecked)
assert not found_7, found_7
layout_7, k_7, d_7, b_7, s_7 = facts(held_7)
sides_7 = s_7.k[: count * count].reshape(count, count, -1)
partners_7 = runner.joined(layout_7.click, count)
pairs_7 = [(t, v) for t in range(count) for v in partners_7[t] if t < v]
sums_7 = sorted({int(x) for t, v in pairs_7 for x in (sides_7[t, v] + sides_7[v, t]).tolist()})
say(f"R7, the promise mutated away: K {k_7}, every side's D {d_7} = {carry(d_7[0], k_7, 0)[0]} K, the teeth born at {b_7};"
    f" the edges {pairs_7}: an edge's two teeth sum to {sums_7} at birth, D - 1 = {d_7[0] - 1}")
events_7, end_7, quotients_7 = go(layout_7, s_7, summary["rounds"])
open_7 = 0
for q in quotients_7:
    inner = q[: count * count].reshape(count, count, -1)
    open_7 += sum(int(x != 0) for t, v in pairs_7 for x in (inner[t, v] + inner[v, t]).tolist())
say(f"R7, the promise mutated away, {summary['rounds']} rounds: {len(events_7)} click lines; the places (round, site, edge)"
    f" where an edge's two quotients do not sum to 0: {open_7}")

# R8: the scale with a remainder, as kappa + 1 leaves it (the ninth code reader's K1)
real_edging = loading.edging
held_8, found_8 = read(u, st, edging=lambda *a: (lambda c, s_, r: (c, s_, r + 1))(*real_edging(*a)))
say(f"R8 the scale's carry leaving 1, as kappa + 1 = {senses * scale + 1} does ({senses * scale + 1} over {senses}:"
    f" {list(carry(senses * scale + 1, senses, 0))}, the scale as it was): loaded {int(held_8 is not None)}; the load's"
    f" promise names {len(found_8)}:")
for line in found_8:
    say(f"    load: {shown(line)}")

# S: kappa from the structure alone (the Boss's ruling on MIN1's case (c)): each world as laid and with every chosen
# strength at 1, and the click world with its hold at 0
for world in sorted(f.name for f in examples.glob("*/")):
    wu, wp, ws = files(world)
    w_made = engine.made(star(len(wp["shape"])))
    ones = copy.deepcopy(wu)
    ones["chosen"].update({k: 1 for k in ("notch", "hold", "spring", "tie", "mesh")})
    w_laid, _ = loading.load(wu, ws, sites_of(wp["shape"]), *w_made)
    w_one, _ = loading.load(ones, ws, sites_of(wp["shape"]), *w_made)
    say(f"S {world}: edging's scale as laid {w_laid.scale}, with every chosen strength at 1 {w_one.scale}")
zero = copy.deepcopy(u)
zero["chosen"]["hold"] = 0
held_z, found_z = read(zero, st)
ones = copy.deepcopy(zero)
ones["chosen"].update({k: 1 for k in ("notch", "hold", "spring", "tie", "mesh")})
held_o, _ = read(ones, st)
say(f"S the click world with hold 0: edging's scale {held_z.scale} (D {sorted(set(held_z.click[-1].ravel().tolist()))}),"
    f" by node-all's edging, which reads lit of the chosen factor; with every chosen strength at 1 {held_o.scale} (D"
    f" {sorted(set(held_o.click[-1].ravel().tolist()))})")

# N: today's integer under the new name
s_n = {**st, "middle": K}
held_n, found_n = read(u, s_n)
folder_n = OUT.joinpath("no", "N")
folder_n.mkdir(parents=True, exist_ok=True)
for n_, held_file in zip(NAMES, (u, p, {**s_n, "ticks": 1}), strict=True):
    folder_n.joinpath(f"{n_}.json").write_text(json.dumps(held_file), encoding="utf-8")
form_n = departures(*[folder_n.joinpath(f"{n_}.json") for n_ in NAMES])
_, k_n, d_n, b_n, _ = facts(held_n)
record_n = folder_n.joinpath("record.jsonl")
assert main.ran([folder_n.joinpath(f"{n_}.json") for n_ in NAMES], record_n) == []
text_n = record_n.read_text(encoding="utf-8").splitlines()
head_n = json.loads(text_n[0])
lines_n = worlds4.sha("\n".join(x for x in text_n if json.loads(x)["kind"] == "click"))
pins = [json.loads(x) for x in ALL.joinpath("tests", "tensor24_prefixes.jsonl").read_text(encoding="utf-8").splitlines()]
(pin,) = [x for x in pins if x["world"] == "tensor24-click"]
say(f"N today's integer under the new name, middle {K}: the format names {len(form_n)}, the load's promise"
    f" {len(found_n)}; K {k_n}, every side's D {d_n}, born at {b_n}; its first-click record ({head_n['dial']} the header's"
    f" dial, the cards' keys {sorted({t['key'] for t in head_n['trains']})}): its click lines' digest is node-all's pin's"
    f" {int(lines_n == pin['lines'])}, its end digest {int(json.loads(text_n[-1])['digest'] == pin['digest'])}")

# B: the width
width = u["integers"]["width"]
for name, middle in (("B1 the format's largest middle, 2^width - 1", (1 << width) - 1), ("B2 a middle of 2^width", 1 << width)):
    s_b = {**st, "middle": middle}
    folder_b = OUT.joinpath("no", name.split()[0])
    folder_b.mkdir(parents=True, exist_ok=True)
    for n_, held_file in zip(NAMES, (u, p, s_b), strict=True):
        folder_b.joinpath(f"{n_}.json").write_text(json.dumps(held_file), encoding="utf-8")
    form_b = departures(*[folder_b.joinpath(f"{n_}.json") for n_ in NAMES])
    held_b, found_b = read(u, s_b)
    _, k_b, d_b, _, _ = facts(held_b)
    say(f"{name}: the middle's bits {middle.bit_length()} against the width {width}; the format names {len(form_b)}"
        f"{': ' + shown(form_b[0]) if form_b else ''}; the load's promise names {len(found_b)}; K's bits"
        f" {int(k_b).bit_length()}, D's bits {int(d_b[0]).bit_length()}")

# W: the five migrated worlds' records by the run tool on the copy, against node-all's
with tempfile.TemporaryDirectory(dir=OUT) as scratch:
    found_rows = worlds4.records(examples, scratch)
OUT.joinpath("records_key4.jsonl").write_text("".join(json.dumps(r) + "\n" for r in found_rows), encoding="utf-8")
OUT.joinpath("prefixes_key4.jsonl").write_text("\n".join(worlds4.pinned(found_rows)) + "\n", encoding="utf-8")
then = [json.loads(x) for x in TODAY.joinpath("records_all.jsonl").read_text(encoding="utf-8").splitlines()]
same = ("rounds", "clicks", "lines", "end", "keys", "dial", "birth", "head", "body", "ledger")
for now, old in zip(found_rows, then, strict=True):
    assert (now["world"], now["run"]) == (old["world"], old["run"])
    alike = {f: int(now[f] == old[f]) for f in same}
    moved = sorted(n for n in now["files"] if now["files"][n] != old["files"].get(n))
    say(f"W: {now['world']} ({now['run']}, {now['rounds']} rounds): click lines {now['clicks']}, end digest"
        f" {now['end']['digest'][:16]}, run back exact {now['end']['exact']}; alike with node-all's: {alike}; the cards'"
        f" keys {sorted(set(now['keys']))}, dial {now['dial']}, birth {now['birth']}; the header's file digests moved:"
        f" {moved}; the copy's decoder reads it: {now['cause'] or 'no cause'}")
pinned = OUT.joinpath("prefixes_key4.jsonl").read_text(encoding="utf-8")
say(f"W: the lines write.py would write, on the copy and the migrated worlds, equal node-all's byte for byte:"
    f" {int(pinned == TODAY.joinpath('prefixes_all.jsonl').read_text(encoding='utf-8'))}, and node-all's"
    f" tests/tensor24_prefixes.jsonl: {int(pinned == ALL.joinpath('tests', 'tensor24_prefixes.jsonl').read_text(encoding='utf-8'))}")

# C: the copy's decoder on the records node-all's run wrote
for name in ("click1.jsonl", "click1.card1.jsonl", "click1.card3.jsonl"):
    held_record, cause = decoding.read(str(TODAY.joinpath("decode", name)))
    say(f"C, the copy's decoder: {name}: read {int(held_record is not None)}; cause: {cause or 'none'}")
say(f"VERDICT: the read reproduces node-all's click world: {int(u_diff == 0 and u_alike == 1)}")
