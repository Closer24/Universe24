"""The one world's helpers shared by the Universe24 tests (tests/test_universe24_runs_its_cycle.py, tests/test_matter_is_born_from_light.py, tests/test_the_sign_holder_and_the_pairs_on_the_small_torus.py, tests/test_the_torus_page_draws_the_log.py): the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone), the declared seed's universe of 2026-10-23 kept by name (`DECLARED`, `declared_universe`: gravity [999, 1000], the sign holder, matter [600, 1000], light, the proton [0, 1000] and the electron [800, 1000] as planes, the absorber), the small structured board's constants as read on it, `small_world` (the declared seed's world cut to a small torus, with or without its detector and instrument bodies) and `flat`."""

from typing import Any

import numpy as np

from tests.laws import ROOT, load_file

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
LOG = FOLDER / "universe24.eras.jsonl"
ERAS = load_file("eras", ROOT / "tools" / "eras.py")
GAMMA, CUBE, LEVEL, SPEED, GAP = 1000, 3, 636, 190, 990
# the declared seed's lightest clump's levels at the pair [600, 1000] (the before level 0.6 of the now), the gate's count of its share on the 3-cube at T 36,000
CLUMP, COUNT, NOW, BEFORE = [1, 1, 1], 429, 3015, 1809
# the two instruments' clicks on the small structured board, before and after its top, read from the run under the content register (2026-10-24; 3 and 1 at the merge base c942951f2, where the register was the W = 0 sign holder's write room, an artefact removed by the Boss's word)
BEFORE_TOP, AFTER_TOP = 2, 2
# the declared seed's universe (examples/events/universe24/universe_universe24.json to 2026-10-23, kept by name on the fold of 2026-10-24: the one world's file is nature's den since, and the small structured board's tests read this seed)


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
