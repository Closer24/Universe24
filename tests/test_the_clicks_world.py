"""Four of the five kinds of clicks of the one law in one shipped world, examples/events/clicks/clicks_chain.json (2026-10-21; the blinds in examples/events/clicks/blind.md, written before the runs, their dated paragraph under the whether as one rule; ALGEBRA.md, The click writes on the lattice; The conversion): light's click at a region (the screen on a photon packet at the close 24, and on the body-emitted photon at 120), a region's plain credit of a massive record (the target on an electron packet at 48), the pixel's click (the one-Node absorber absorbing a photon at its derived window's close 32 and emitting one by the law's (5), a source in time at its Node, at the close 64) and a conversion (the neutron at the target at 60 into a proton and an electron at the senses 1 and -1); the bound body's click absent by name. The pinned numbers and their causes under the rule of 2026-10-21 (the count the floor of the window's inflow with the carried remainder, the remainder below one quantum drawn by the read of the board, the half-up rounding gone): the screen's credit at 24 (the booked share 0.046 at 12 drawn none, 0.887 with the carry at 24 drawn one), the target's credit of the electron at 48 (0.698 at 24 and 0.721 at 36 drawn none, 0.745 at 48 drawn one), the body's window 32 (the 17-Node lay's passage over one Node, lit at 1; the absorption's draw at the share 0.99999), the conversion at 60 (the neutron's 0.225 at 36 and 0.627 at 48 drawn none, 0.863 at 60 drawn one), the emission at 64 (the window's close, the digits' draw at the hazard 0.04125 per dark interval), the screen's credit of the emitted photon at 120 (0.359 carried from the first photon's remnant at the count 0, 0.492 with the light's inflow at 120, drawn one), the holes at the regions' one front Node each (88, 20) and the body's own (62), the planes' exact split 5450 + 5458 + 5476 = 16384 against -16384; every number the re-run's on the rule, none derived from the rounding's run."""

import json

from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
SCREEN, BODY, CELL, TARGET, EMISSION, LIGHT = (
    149,
    32,
    149,
    149,
    64,
    149,
)  # the closes of the seven lines under the window derived, the law's reading on the owner's decision of 2026-10-23: the regions' one window the lays' longest passage, 149, the body's 32; the former reading's 24, 32, 24, 60, 53, 60 under the declared window 12 and The stress is the Links'


def test_four_kinds_of_clicks_fall_at_their_closes_in_one_world():
    """The four kinds of clicks on the shipped world's record, examples/events/clicks/clicks_chain.clicks.json (re-recorded on 2026-10-23 under the swap reading the gapped time line alone, the folder's README; the run of 156 intervals, 37 s on the suite's clock, left on 2026-10-24): the body's absorption of a photon at its first close (kind 4, g to e, the window [1, 32]), its emission at the next (kind 5, e to g, the window [33, 64]), then at the regions' one close 149 the screen's credit of the body's own photon (kind 2, the source body 0), the target's credit of the neutron with its one conversion into proton and electron at the senses 1 and -1 (kind 1) and its plain credit of the electron laid there (kind 3), the body's second absorption and emission after it and the lay's second photon credited at the target at 298; the photon's count down at a take, up at a give, down at a credit; the world loads with the body's window derived as its own beat, 32, and the lifetime 24 to the photon."""
    log = json.loads((FOLDER / "clicks_chain.clicks.json").read_text(encoding="utf-8"))
    kinds = [
        (
            row["interval"],
            row["node_detector"],
            row["family"],
            row["event"],
            row.get("absorbed"),
            row.get("emitted"),
        )
        for row in log
    ]
    assert kinds[:6] == [
        (BODY, "body 0", "absorber", "credit", "photon", None),
        (EMISSION, "body 0", "absorber", "credit", None, "photon"),
        (LIGHT, "screen", "photon", "credit", None, None),
        (TARGET, "target", "neutron", "credit", None, None),
        (TARGET, "target", "neutron", "conversion", None, None),
        (CELL, "target", "electron", "credit", None, None),
    ]
    body, emitted, light, target, converted, cell = log[:6]
    assert (body["before"], body["realised"], body["window"], body["count"]) == ("g", "e", [1, BODY], 1)
    assert (emitted["before"], emitted["realised"], emitted["window"]) == (
        "e",
        "g",
        [BODY + 1, EMISSION],
    )
    assert (light["count"], light["window"], light["source"]) == (1, [1, LIGHT], "body 0")
    assert (target["count"], target["left"], target["window"]) == (1, 0, [1, TARGET])
    assert (converted["into"], converted["senses"]) == (["proton", "electron"], [1, -1])
    assert (cell["count"], cell["window"], cell["source"]) == (1, [1, CELL], "the lay")
    assert (
        light["left"] + 1 == body["left"] + 1 == emitted["left"]
    )  # down at the take, up at the give, down at the credit
    assert (
        [(row["interval"], row["family"], row["node_detector"]) for row in log[6:]]
        == [
            (180, "absorber", "body 0"),
            (191, "absorber", "body 0"),
            (212, "absorber", "body 0"),
            (298, "photon", "target"),
        ]
    )  # the second absorption and emission, a null window, and the lay's second photon's credit at the target
    assert [row["interval"] for row in log] == sorted(row["interval"] for row in log)
    world = load_shipped(FOLDER / "clicks_chain.json")
    body_row = world.bodies[0].detector
    assert body_row is not None and body_row.draw is not None and body_row.draw.window == BODY
    photon = [f.name for f in world.families].index("photon")
    assert [body_row.rates[0].lifetime, body_row.rates[0].light] == [
        24,
        photon,
    ]  # the law's (5), declared
