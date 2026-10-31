"""KEY4's migration of the four lay tools (node-all 9d75a4904's, read from tree_all/), written to a lay tree at the tree's
own depth: each lays its world's key once in the setting it writes, as the key's middle, and loads its own runs with
it; the click lay's key-1 runs pass the middle 0 and read the click's unit off the loader; its item 3 drops the parity
half (odd by construction, the mathematician's MINOR 4) and names the key's provenance in place of "a chosen unit"
(the physicist's m3, the audit's C7). Nothing else in a tool moves. Each edit is an exact text replacement whose count
is asserted. Run: python3 -I patch_lays4.py <tree_all's boss folder> <the lay tree's boss folder>.
"""

import sys
from pathlib import Path

TODAY, TREE = Path(sys.argv[1]), Path(sys.argv[2])

MIDDLE0 = "MIDDLE = 0  # the key, laid once as the key's middle: 0, for the click's unit 1, the file's key (KEY4)\n"
EDITS = {
    "click_lay": [
        ("The click world's lay, examples/tensor24-click/setting.json and its universe's key (the Boss's code writer,",
         "The click world's lay, examples/tensor24-click/setting.json with its key laid once (the Boss's code writer,"),
        ("on the act; the key CHOSEN in the universe file, read against the largest swing of the giver's course of S (its",
         "on the act; the key laid once in the setting, the key's middle MIDDLE, the file's key moved (set from a run at\n"
         "the key 1, about a seventh of the giver's swing there, the audit's C7, and the file's own until the owner rules,\n"
         "KEY4), the click's unit K = 2 MIDDLE + 1 read off the loader, read against the largest swing of the giver's course\n"
         "of S (its"),
        ("BEAT_RUN = 1000  # the run's window: the rounds the lone giver is run for its beat, a fixed run\n",
         "BEAT_RUN = 1000  # the run's window: the rounds the lone giver is run for its beat, a fixed run\n"
         "MIDDLE = 25405714  # the key, laid once as the key's middle: the file's key 50811429 moved, (key - 1) div 2, not\n"
         "# derived (KEY4; its value set from a run, the audit's C7); the click's unit 2 MIDDLE + 1 is the loader's\n"),
        ("def world(universe, shape, gears):", "def world(universe, shape, gears, middle):"),
        ('loading.load(universe, {"version": 1, "gears": gears}',
         'loading.load(universe, {"version": 1, "middle": middle, "gears": gears}'),
        ("    held, layout, _ = world(universe, shape, [])\n", "    held, layout, _ = world(universe, shape, [], MIDDLE)\n"),
        ("    one = json.loads(json.dumps(universe))\n    one[\"chosen\"][\"key\"] = 1\n", ""),
        ("    run_one(one, gears_of(hand, giver, 1), period, wind)\n    key = universe[\"chosen\"][\"key\"]\n"
         "    _, odd = carry(key, 2, 0)  # the key's parity by Rule3's carry\n    holds = odd == 1 and 1 <= key <= swing[0]\n",
         "    run_one(universe, gears_of(hand, giver, 1), period, wind, 0)  # the middle 0: the click's unit 1\n"
         "    edge = int(layout.click.key[0, 0])  # the edge dial D, every side's, read off the loader\n"
         "    key, _ = carry(edge, held.scale, 0)  # the click's unit K, D over edging's scale, the loader's\n"
         "    holds = 1 <= key <= swing[0]  # odd by construction, K = 2 MIDDLE + 1: no parity is read\n"),
        ('f"3. the key CHOSEN in the universe file, {key}, read against the act',
         'f"3. the key laid in the setting as the key\'s middle, {MIDDLE}, the click\'s unit {key} read off the loader (the edge dial {edge}), read against the act'),
        ('whole from 1 to that swing, holds it: {holds} (its remainder by 2, {odd}); about {carry(swing[0], key, 0)[0]} keys pass in that"\n'
         '        f" beat (a chosen unit of wind below the quantum, Planck\'s key being NOT_CLOSED 3; the lay computes no key, the audit\'s C7)"',
         'whole from 1 to that swing, holds it: {holds} (odd by construction, no parity read); about {carry(swing[0], key, 0)[0]} keys pass in that"\n'
         '        f" beat (the swing over the key, a clock fact; the key\'s value the file\'s own, set from a run at the key 1, the audit\'s C7,"\n'
         '        f" OPEN for the owner; Planck\'s key NOT_CLOSED 3; the lay computes no key)"'),
        ('    tenth["chosen"]["tie"], tenth["chosen"]["key"] = carry(2 * hold * f, 10, 0)[0], 1\n',
         '    tenth["chosen"]["tie"] = carry(2 * hold * f, 10, 0)[0]\n'),
        ("    quiet_wide = run_one(tenth, gears_of(hand, giver, 1), TICKS, quiet)\n",
         "    quiet_wide = run_one(tenth, gears_of(hand, giver, 1), TICKS, quiet, 0)  # the middle 0: the click's unit 1\n"),
        ("        + str(TICKS)\n        + ', \"gears\": [\\n'\n",
         "        + str(TICKS)\n        + ', \"middle\": '\n        + str(MIDDLE)\n        + ', \"gears\": [\\n'\n"),
        ('say(f"the setting written: {len(gears)} gears, ticks {TICKS}; the universe\'s key {key}")',
         'say(f"the setting written: {len(gears)} gears, ticks {TICKS}, the middle {MIDDLE}; the click\'s unit {key}, the edge dial {edge}")'),
        ("def run_one(universe, gears, rounds, reader):", "def run_one(universe, gears, rounds, reader, middle=MIDDLE):"),
        ("    held, layout, s = world(universe, ONE, gears)\n", "    held, layout, s = world(universe, ONE, gears, middle)\n"),
    ],
    "live_lay": [
        ('loading.load(universe, {"version": 1, "gears": gears}', 'loading.load(universe, {"version": 1, "middle": MIDDLE, "gears": gears}'),
        ("TICKS = 100  # the setting's ticks\n", "TICKS = 100  # the setting's ticks\n" + MIDDLE0),
        ("'{\"version\": 1, \"ticks\": ' + str(TICKS) + ', \"gears\": [\\n'",
         "'{\"version\": 1, \"ticks\": ' + str(TICKS) + ', \"middle\": ' + str(MIDDLE) + ', \"gears\": [\\n'"),
    ],
    "mesh_lay": [
        ('loading.load(universe, {"version": 1, "gears": gears}', 'loading.load(universe, {"version": 1, "middle": MIDDLE, "gears": gears}'),
        ("TICKS = 125  # the setting's ticks: inside the room at the file's mesh, measured below\n",
         "TICKS = 125  # the setting's ticks: inside the room at the file's mesh, measured below\n" + MIDDLE0),
        ("'{\"version\": 1, \"ticks\": ' + str(ticks) + ', \"gears\": [\\n'",
         "'{\"version\": 1, \"ticks\": ' + str(ticks) + ', \"middle\": ' + str(MIDDLE) + ', \"gears\": [\\n'"),
    ],
    "well_lay": [
        ('loading.load(universe, {"version": 1, "gears": gears}, sites',
         'loading.load(universe, {"version": 1, "middle": MIDDLE, "gears": gears}, sites'),
        ("TICKS = 128  # the setting's ticks, and the first run's rounds\n",
         "TICKS = 128  # the setting's ticks, and the first run's rounds\n" + MIDDLE0),
        ("        + str(TICKS)\n        + ', \"gears\": [\\n'\n",
         "        + str(TICKS)\n        + ', \"middle\": '\n        + str(MIDDLE)\n        + ', \"gears\": [\\n'\n"),
    ],
}

for tool, edits in EDITS.items():
    text = TODAY.joinpath(tool, "lay.py").read_text(encoding="utf-8")
    for old, new in edits:
        assert text.count(old) == 1, (tool, old[:70])
        text = text.replace(old, new)
    TREE.joinpath(tool).mkdir(parents=True, exist_ok=True)
    TREE.joinpath(tool, "lay.py").write_text(text, encoding="utf-8")
    print(f"{tool}: {len(edits)} edits")
