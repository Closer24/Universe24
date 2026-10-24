"""The conversion in the toy as a test (2026-10-21; ALGEBRA.md, The conversion, Only a click moves a quantum between families; src/event_universe/conversion.py): the exactness clause, every family's list derived from the pairs under the law's conservations with no key (the owner's word of 2026-10-21, the table's declaration deleted; the senses of a real-line parent's plane records out the one residual declaration, the row's key `senses`), the loader's refusals by name, and the chain world examples/events/conversion/neutron_chain.json run to its first conversion with the blind written before the run: no conversion before the packet reaches the target, one conversion per credited quantum at the window's close, the counts n -1, p +1, e +1, the Wronskian's sum 0 at the lay by the exact split and the rotations' identity exact in the integers."""

import json

from event_universe import conversion
from event_universe.features.click import plane_squares, two_squares
from tests.laws import EVENTS

FOLDER = EVENTS / "conversion"  # the record's universe file, read as a document of pairs and no world
UNIVERSE = json.loads((FOLDER / "nucleons_pythagorean.json").read_text(encoding="utf-8"))
NEUTRON, PROTON, ELECTRON, OLD_ELECTRON = (-4800, 6000), (0, 6000), (3600, 6000), (4000, 6000)
HALF_ACTION = 16384  # T div 2 at T = 32768, the Wronskian of one quantum at the quarter-turn lay


def test_the_rotations_sum_exactly_iff_every_pair_is_pythagorean_and_the_split_carries_the_quantum_whole():
    """The exactness clause: the neutron's point (-4800, 3600) is the proton's (0, 6000) times the electron's (3600, 4800) over den, so pi/2 + arccos(3/5) = arccos(-4/5) in the integers, and no list with the old electron [4000, 6000] is exact (its sine irrational); two parents' rotations the Gaussian product of their points over their dens, p + e summing to n exactly; the lay's exact split of T div 2 over three planes is (73, 11), (57, 47), (74, 0), the sums 5450 + 5458 + 5476 = 16384 within a spread of 26 where 3 x 73^2 falls 397 short; one plane takes (128, 0)."""
    assert conversion.gaussian(NEUTRON) == (-4800, 3600) and conversion.gaussian(PROTON) == (0, 6000)
    assert conversion.gaussian(ELECTRON) == (3600, 4800) and conversion.gaussian(OLD_ELECTRON) is None
    assert conversion.exact([NEUTRON], [PROTON, ELECTRON]) and conversion.exact(
        [NEUTRON], [ELECTRON, PROTON]
    )
    assert not conversion.exact([NEUTRON], [PROTON, OLD_ELECTRON]) and not conversion.exact(
        [NEUTRON], [PROTON]
    )
    assert not conversion.exact([NEUTRON], [ELECTRON, ELECTRON]) and not conversion.exact(
        [NEUTRON], [PROTON, PROTON]
    )
    assert conversion.exact([PROTON, ELECTRON], [NEUTRON]) and conversion.rotation(
        [PROTON, ELECTRON]
    ) == (
        (-28800000, 21600000),
        36000000,
    )
    split = plane_squares(HALF_ACTION, 3)
    assert split == [(73, 11), (57, 47), (74, 0)]
    sums = [a * a + b * b for a, b in split]
    assert sum(sums) == HALF_ACTION and max(sums) - min(sums) == 26 and 3 * 73 * 73 == HALF_ACTION - 397
    assert plane_squares(HALF_ACTION, 1) == [(128, 0)] and two_squares(5461) is None
    assert plane_squares(HALF_ACTION * 2, 2) == [(128, 0), (128, 0)]
