# The algebra visualizer

One static HTML page in three layers, read from two runs' records alone
(the design [docs/designs/algebra_visualizer/DESIGN.md](../../docs/designs/algebra_visualizer/DESIGN.md);
the model owner's word of 2026-09-23 through the Boss, record 1435): the
geometry that is the algebra, how it produces the physics, and the clicks.
Every number on the page carries its kind (DETECTOR, GAMEBOARD, COMPUTATION,
HOST, CONVERSION, DECLARATION, PIN) and the file and line it was read from;
the page computes no physics, moves no pin, runs nothing and compares
nothing with nature.

| Module | Responsibility |
| --- | --- |
| `record.py` | The readers: `run.json`, `events.jsonl`, `state.json`, the world file and a series' register, standard library only; exact differences of recorded integers; the engine a run came from, told from `run.json`'s `hypotheses` alone (`engine_of`) |
| `panels.py` | One model per panel: the title, the algebra's lines with their sections, the numbers with their kinds and sources, the picture's data; the first page's panels (DESIGN.md sections 2 to 4) and the one-run page's algebra and Outside panels (DESIGN_3D.md sections 2 and 4) |
| `board3d.py` | The GameBoard layer in 3-D (DESIGN_3D.md section 3): the box, the marks of the record over the intervals, the blocks or bodies at their recorded positions, the detectors' cells with their counts, the probes, the books per interval, the snapshot under a cap; the board's data as one JSON object; the projection's floats |
| `svg.py` | The pictures as inline SVG text, the 3-D board's pre-rendered picture among them; floats in drawing coordinates alone |
| `render.py` | The entry: headless by default (prints every number with its kind and source, writes nothing); `--render OUT.html` writes the one page; the inline script of the 3-D board (the rotation, the interval slider) |

## The 3-D page of one run (DESIGN_3D.md)

Any registered run folder of either engine, the Beam Law on `main` or the
detector law on its branch (told from `run.json`'s `hypotheses`, never from
a family name), renders as one page in the owner's three layers: the
algebra (the declared objects of ALGEBRA.md, every integer DECLARATION),
the GameBoard as the Inside in 3-D with a step control over the intervals
(GAMEBOARD, titled a diagnostic), and the clicks as the Outside (DETECTOR).
Neither engine records the board's state per Node per interval: the board
draws only what the record writes and says so on its face (DESIGN_3D.md,
Finding 1). No external library: inline SVG and one inline script.

    PYTHONPATH=src python -m event_universe --init examples/events/moving_detector/cart_k5.json --output RUN_FOLDER
    PYTHONPATH=src python tools/algebra_visualizer/render.py RUN_FOLDER                   # headless
    PYTHONPATH=src python tools/algebra_visualizer/render.py RUN_FOLDER --render OUT.html # the page

An EXPLORATORY run (the word in its folder's path or its model identity)
carries EXPLORATORY in the page's title and on every panel, never a result.

**Where the 3-D page is.** The page of 2026-09-23 from `cart_k5` (the one
registered world whose body steps and whose lines carry `clock`, the
detector's own count), made at the engine's fingerprint `e3270d0109`
(`run.json`'s `source_sha256`; the world file's sha256 `ce6f113c78...`,
600 intervals), is published for the model owner as one private page,
https://claude.ai/artifact/D99FfkGkYvq1bahWizD6rH (private; the owner shares
it from the page). The run stays outside the tree.

## The first page, two runs (DESIGN.md)

Make the two runs first, outside the tree, with the register's runner:

    PYTHONPATH=src python tools/run_series.py --out RUNS_DIR \
        examples/events/c_measured/c_measured.json examples/events/amplitude/slits_low.json

then

    PYTHONPATH=src python tools/algebra_visualizer/render.py RUNS_DIR                       # headless
    PYTHONPATH=src python tools/algebra_visualizer/render.py RUNS_DIR --render OUT.html     # the page

**Where the page is.** No page is committed (CONTRIBUTING.md keeps generated
outputs outside source commits). The page of 2026-09-23, made from the two
registered runs at the engine's fingerprint `e3270d0109` (`run.json`'s
`source_sha256`), is published for the model owner as one private page,
https://claude.ai/artifact/Nwr2XSwVxkSUFKGmm7qBQa (private; the owner shares
it from the page). Every number on it names its kind and its source line.

A missing run folder is refused with the line above; the tool never runs
the engine and imports nothing of `event_universe` (the test
`tests/test_algebra_visualizer.py` asserts it). The page test runs under
`pytest --visualize-runs` alone; the other tests are headless.
