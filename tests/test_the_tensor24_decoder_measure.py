"""Tensor24's decoder, the measurement's rules: the Meshes between two sites, the shorter way round each of the board's
sides, read twice, and the past cone one Mesh a round on them, as the click world's cone check reads them."""

from tensor24.decoder import measure
from tests import frame as board


def test_the_meshes_are_the_shorter_way_round_each_side_and_the_past_cone_one_mesh_a_round():
    """The Meshes from every site against the board's own neighbours ring by ring, and the past cone on them, its edge in."""
    sides = [3, 4, 5]  # the site (x 4 + y) 5 + z, z the fastest
    near = board.board(tuple(sides))  # the board's own six neighbours: the second reading
    for a in range(near.shape[1]):
        far, ring, step = {a: 0}, [a], 0
        while ring:  # the Meshes from a, one ring of neighbours a step
            step += 1
            ring = [b for b in {int(b) for s in ring for b in near[:, s]} if b not in far]
            far.update(dict.fromkeys(ring, step))
        for b, meshes in far.items():
            assert measure.meshes(sides, a, b) == meshes
            for lag in (meshes - 1, meshes):  # one round short of the cone, and on it
                assert measure.past(sides, (1, a), (1 + lag, b)) == (lag >= meshes)
