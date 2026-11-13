"""Storage, adjacency and passive-read contracts for regular node views."""
import dataclasses
import unittest

import numpy as np

from universe24.algebra.group_2o import group
from universe24.core import Engine, State
from universe24.core.lattice import DIRECTIONS
from universe24.model import make_model_bundle
from universe24.node import EdgeRef, FacePort, NodeView, face_channels


class NodePortContractTests(unittest.TestCase):
    def fixture(self, L=3):
        values = np.arange(48 * L ** 3).reshape(48, L ** 3)
        return State(L, values + 10000, values + 20000, values % 6)

    def test_six_internal_faces_partition_all_retained_state(self):
        state = self.fixture()
        node = NodeView(state, 0)
        self.assertEqual(node.coordinates, (0, 0, 0))
        self.assertEqual(len(node.faces), 6)
        flattened = [g for face in node.faces for g in face.channels]
        self.assertEqual(sorted(flattened), list(range(48)))
        reconstructed = {}
        for face in node.faces:
            self.assertEqual(len(face.channels), 8)
            self.assertEqual(len(face.central_pairs), 4)
            self.assertEqual(sorted(g for pair in face.central_pairs for g in pair),
                             sorted(face.channels))
            for channel, triple in zip(face.channels, face.triples()):
                reconstructed[channel] = triple
            for bank in ("a", "b", "r"):
                self.assertEqual(face.values(bank),
                                 tuple(int(getattr(state, bank)[g, 0]) for g in face.channels))
        self.assertEqual(tuple(reconstructed[g] for g in range(48)), node.triples())
        self.assertEqual(sum(len(t) for t in reconstructed.values()), 144)

    def test_both_endpoints_share_one_edge_even_across_periodic_seam(self):
        state = self.fixture()
        edges = {}
        for n in range(state.N):
            for face in NodeView(state, n).faces:
                other = face.opposite
                self.assertEqual(face.edge, other.edge)
                self.assertEqual(face.edge.key, other.edge.key)
                self.assertEqual(other.neighbour_index, n)
                self.assertEqual(other.opposite.node_index, n)
                self.assertEqual(other.opposite.direction, face.direction)
                self.assertEqual(set(face.edge.endpoints), {n, face.neighbour_index})
                self.assertEqual({(p.node_index, p.direction) for p in face.edge.ports(state)},
                                 {(n, face.direction), (other.node_index, other.direction)})
                edges.setdefault(face.edge, []).append((n, face.direction))
        self.assertEqual(len(edges), 3 * state.N)
        self.assertTrue(all(len(ports) == 2 for ports in edges.values()))
        seam = NodeView(state, 0).face(1)
        self.assertEqual(seam.neighbour_index, state.lattice.index(2, 0, 0))
        self.assertEqual(seam.edge.base, seam.neighbour_index)
        self.assertIs(seam.opposite.state, state)

    def test_channel_partition_is_covariant_under_every_cube_action(self):
        algebra = group()
        groups = face_channels()
        for k, rotation in enumerate(algebra.rotations):
            for d, offset in enumerate(DIRECTIONS):
                rotated = tuple(sum(rotation[i][j] * offset[j] for j in range(3))
                                for i in range(3))
                target = DIRECTIONS.index(rotated)
                self.assertEqual({algebra.multiplication[k][g] for g in groups[d]},
                                 set(groups[target]))

    def test_views_do_not_copy_advance_or_write_retained_state(self):
        bundle = make_model_bundle(L=3)
        state = bundle.seed
        before = state.copy()
        node = NodeView(state, 0)
        face = node.face(0)
        self.assertIs(node.state, state)
        self.assertIs(face.state, state)
        self.assertEqual([f.name for f in dataclasses.fields(node)], ["state", "index"])
        self.assertEqual([f.name for f in dataclasses.fields(face)],
                         ["state", "node_index", "direction"])
        values = face.values()
        self.assertIsInstance(values, tuple)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            face.direction = 1
        after = Engine(bundle.tensor).step(state)
        self.assertTrue(state.same_as(before))
        self.assertIs(node.state, state)
        self.assertIsNot(NodeView(after, 0).state, state)
        self.assertEqual(face.values(), values)
        state.b[face.channels[0], 0] += 1
        self.assertEqual(face.values()[0], values[0] + 1)
        self.assertEqual(face.opposite.values(),
                         tuple(int(state.b[g, face.neighbour_index]) for g in face.opposite.channels))

    def test_derived_sums_and_contrasts_use_python_integer_arithmetic(self):
        state = self.fixture()
        face = NodeView(state, 0).face(0)
        left, right = face.central_pairs[0]
        state.b = state.b.astype(object)
        state.b[left, 0] = 1 << 130
        state.b[right, 0] = -(1 << 131)
        self.assertEqual(face.pair_sums()[0], -(1 << 130))
        self.assertEqual(face.central_contrasts()[0], 3 * (1 << 130))
        self.assertTrue(all(type(value) is int for value in face.values()))

    def test_invalid_views_and_unknown_banks_are_rejected(self):
        state = self.fixture()
        for n in (-1, state.N, True, 1.5):
            with self.assertRaises(ValueError):
                NodeView(state, n)
        for d in (-1, 6, True, 1.5):
            with self.assertRaises(ValueError):
                FacePort(state, 0, d)
        for bank in ("history", "__dict__", None, 0):
            with self.assertRaises(ValueError):
                NodeView(state, 0).values(bank)
            with self.assertRaises(ValueError):
                NodeView(state, 0).face(0).central_contrasts(bank)
        with self.assertRaises(ValueError):
            NodeView(State(3, [[1] * 27] * 47, [[1] * 27] * 47, [[1] * 27] * 47), 0)
        with self.assertRaises(TypeError):
            NodeView(None, 0)
        with self.assertRaises(ValueError):
            EdgeRef(3, 0, 0).ports(self.fixture(L=4))
        for args in ((2, 0, 0), (3, -1, 0), (3, 0, 3)):
            with self.assertRaises(ValueError):
                EdgeRef(*args)


if __name__ == "__main__":
    unittest.main()
