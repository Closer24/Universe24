# Light and its echo, read in the clicks (Big Pic, the owner's ask of 07:1x UTC)

The records are node-edge 88b4d281c's runs of its mesh world (examples/tensor24-mesh: a ring of 180 Node-clocks, one
bump of the wave laid at rest on Node-clocks 17 to 23, the held hand laid at 1 everywhere, the tied train at every
Node-clock), and of seeds that change only its lay (variants.py). The probes read the record's click lines alone,
the wave's clicks across the Meshes (train 0's across lines), in whole numbers and Rule3's carry.

| probe | what it reads | output |
|---|---|---|
| fronts.py | each distance's first click across a Mesh, both ways; the bump's own clicks and the far side's, round by round | fronts_mesh_450.txt |
| echo.py | the far side's peak, the bump's return, Einstein's rule on them | echo_mesh_560.txt |
| mirror.py | two records compared, the plain lay and a held-hand patch: where the patch first answers the light, and the answer's way back | mirror_heldpatch_300.txt |
| variants.py | the seeds: the plain lay longer, the held patch, tied lumps of six sizes | lumps.txt (which hold, which run away) |

Commands, from a checkout of node-edge 88b4d281c (`S` the folder of these files):

    python3 -I S/variants.py examples/tensor24-mesh/setting.json OUT
    python3 -I tools/tensor24_run.py examples/tensor24-mesh/universe.json examples/tensor24-mesh/piece.json OUT/mesh560/setting.json mesh_560.jsonl
    python3 -I S/fronts.py src mesh_450.jsonl 180 20 25
    python3 -I S/echo.py src mesh_560.jsonl 180 20 300
    python3 -I S/mirror.py src mesh_560.jsonl heldpatch_300.jsonl 180 20 300

Rounds are read as order and, in place of each clock's own lines between two of its meetings, as a board check
(every clock here is laid alike). These clicks are the medium's own: by LIGHT2's rule (A's quiet, the relay linkage)
no shipped world shows light's lines, since at this key every move clicks (#2187 6540720252 item 4). The readings
are the numbers a lawful light reading must meet once the key comes from the structure.
