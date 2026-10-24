"""The builders of the wrapped board's tests (tests/test_the_uniform_mode.py, tests/test_the_interval.py; beside tests/laws.py, whose size the tests' shape caps): the rule's own universe at gravity's level weight 1 with a held row's integers and the quantum action chosen (`universe_at_weight_one`), the matter record laid uniform over the 3-cube torus (`uniform_world`) and the same with its counts at the share the gate reads (`laid_torus`)."""

import json

from tests.laws import UNIVERSE

GAMMA, ACTION, CUBE, AMPLITUDE = 6000, 32768, 3, 435  # the rule's clock and quantum, a 3-cube torus
TORUS = {"x": "periodic", "y": "periodic", "z": "periodic"}
WIDTH = 92  # the width of the volume form, the record X inside 2^92 at the clock's last pace


def universe_at_weight_one(folder, action=ACTION, width=None, **rows):  # type: ignore[no-untyped-def]
    """The rule's own universe beside the world with gravity's level weight 1, so that the content moves within a test's intervals, at the quantum action `action` (the rule's 32,768; 36,000 the volume form's tests' integer), at the width `width` where given (92 for the volume form, whose record X = Gamma (Gamma / p_0)^4 outgrows the rule's 63-bit bound within ten intervals; the rule's own otherwise), with the held integers `rows` names per family (gravity={"rest": 60}: the row's rest), and without the binding holder: a row with a gap rests on a torus through its gap alone, and at the pair [2400, 2401] the division act's iteration contracts the uniform mode by 1 - 1 / 2,400 per act and cycles under the floors (the shipped tests' 170,000 passes at [24, 25]), a limit of the rest's iteration and nothing of the carried mode, left open by name."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    if width is not None:
        universe["integers"]["width"] = width
    universe["families"] = [f for f in universe["families"] if f["name"] != "binding"]
    for family in universe["families"]:
        family["reads"] = {name: w for name, w in family["reads"].items() if name != "binding"}
        if family["name"] == "gravity":
            family["held"]["level_weight"] = 1
        family.get("held", {}).update(rows.get(family["name"], {}))
    universe["integers"]["quantum_action"] = action
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")


def volume_universe(folder, **rows):  # type: ignore[no-untyped-def]
    """The rule's universe at the volume form's integers, T 36,000 and the width 92, the held rows' integers as `rows` names them (the one Node: every held row of the content carries its time line as the volume's level, its write at the carried factor, the stress's trace in its time line, no key)."""
    universe_at_weight_one(folder, 36000, WIDTH, **rows)
