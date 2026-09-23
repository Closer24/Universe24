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
| `record.py` | The readers: `run.json`, `events.jsonl`, `state.json`, the world file and a series' register, standard library only; exact differences of recorded integers |
| `panels.py` | One model per panel of the design's sections 2 to 4: the title, the algebra's lines with their sections, the numbers with their kinds and sources, the picture's data; the light rule's worked example and the block's declared table as labelled constants |
| `svg.py` | The pictures as inline SVG text; floats in drawing coordinates alone |
| `render.py` | The entry: headless by default (prints every number with its kind and source, writes nothing); `--render OUT.html` writes the one page |

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
