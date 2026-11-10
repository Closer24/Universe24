"""Candidate-coupling framework: 2O covariance, bit-for-bit reference equality, exact inverse, bands, files."""
import ast
import cmath
from contextlib import redirect_stderr, redirect_stdout
import io
import itertools
import json
import math
from pathlib import Path
import random
import sys
import tempfile
import unittest

from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.__main__ import main as reference_main
from universe24.core.group_2o import DIRECTIONS
from universe24.experiments import from_dict as reference_from_dict, load as reference_load
from universe24.observation import balance_residuals, expected_account_change, signed_account
from research.coupling_variants_v1 import (AXIAL_PAIRS, SIGN_TRIPLES, VariantCoupling, VariantEngine,
                                           axial_actions, chi_gauge_state, covariant_family, from_dict, load,
                                           pairing, read_checkpoint, staggered_state, write_init)
from research.coupling_variants_v1.__main__ import main as variant_main

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "research" / "coupling_variants_v1"
FAMILY = list(covariant_family())


def random_state(rng, side, background_r, cells=40, big=False):
    data = {}
    for _ in range(cells):
        address = (rng.randrange(side), rng.randrange(side), rng.randrange(side), rng.randrange(48))
        span = 10 ** 30 if big and rng.random() < 0.2 else 7
        data[address] = Channel(rng.randint(-span, span), rng.randint(-span, span), rng.randrange(6))
    return State(Cube(side), Channel(0, 0, background_r), data)


def random_member(rng, name="member"):
    actions, weights = rng.choice(FAMILY)
    return VariantCoupling.from_body_actions(name, actions, weights)


def gather_advance(coupling, state):
    """Independent dense receiver-sum update (pull form of the six-port tensor)."""
    L, bg = state.cube.side, state.background
    old = {(x, y, z, g): state.cells.get((x, y, z, g), bg)
           for x in range(L) for y in range(L) for z in range(L) for g in range(48)}
    new = {}
    for (x, y, z, g), (a, b, r) in old.items():
        u = 0
        for d, (dx, dy, dz) in enumerate(DIRECTIONS):
            sender = ((x + dx) % L, (y + dy) % L, (z + dz) % L, coupling.ports[d][g])
            u += coupling.weights[d][g] * old[sender][1]
        total = 2 * u + r
        new[(x, y, z, g)] = Channel(b, total // 6 - a, total % 6)
    return State(state.cube, bg, new)


class ReferenceEquality(unittest.TestCase):
    def test_reference_tables_labels_and_fingerprints(self):
        fingerprints = set()
        for signs in SIGN_TRIPLES:
            variant, reference = VariantCoupling.reference(signs), Coupling(signs)
            self.assertEqual((variant.ports, variant.weights), (reference.ports, reference.weights))
            self.assertEqual(variant.reference_signs, signs)
            self.assertFalse(variant.is_variant)
            self.assertTrue(variant.label.startswith("reference:"))
            self.assertEqual(variant.reference_fingerprint, reference.fingerprint)
            self.assertEqual(variant.matrix(3), reference.matrix(3))
            self.assertEqual(variant.pairs, AXIAL_PAIRS)
            fingerprints.add(variant.fingerprint)
        self.assertEqual(len(fingerprints), 8)

    def test_bit_for_bit_equal_to_native_engine_on_random_states(self):
        rng = random.Random(20261109)
        for signs in SIGN_TRIPLES:
            native, variant = Engine(Coupling(signs)), VariantEngine(VariantCoupling.reference(signs))
            for trial in range(6):
                state = random_state(rng, 3 + trial % 3, rng.randrange(6), big=trial % 2 == 0)
                with self.subTest(signs=signs, trial=trial):
                    for component in (0, 1):
                        self.assertEqual(variant.input_sums(state, component), native.input_sums(state, component))
                    self.assertEqual(variant.rewind(state), native.rewind(state))
                    self.assertEqual(list(variant.evolve(state, 4)), list(native.evolve(state, 4)))


class CovariantFamily(unittest.TestCase):
    def test_degrees_of_freedom(self):
        members = set(FAMILY)
        self.assertEqual((len(FAMILY), len(members)), (61440, 61440))
        actions = {a for a, _ in FAMILY}
        self.assertEqual(len(actions), 7680)
        by_pairing = {}
        for a in actions:
            by_pairing.setdefault(pairing(a), set()).add(a)
        self.assertEqual(len(by_pairing), 15)
        self.assertEqual({len(v) for v in by_pairing.values()}, {512})
        self.assertEqual(by_pairing[AXIAL_PAIRS], {axial_actions(m) for m in itertools.product(range(8), repeat=3)})
        for signs in SIGN_TRIPLES:
            reference = VariantCoupling.reference(signs)
            self.assertIn((reference.body_actions, reference.body_weights), members)
            self.assertEqual(VariantCoupling.axial("axial-013", (0, 1, 3), signs).label, reference.label)
        rng = random.Random(1)
        for actions, weights in rng.sample(FAMILY, 40):
            member = VariantCoupling.from_body_actions("member", actions, weights)
            self.assertEqual((member.body_actions, member.body_weights), (actions, weights))
        self.assertTrue(VariantCoupling.axial("axial-017", (0, 1, 7)).is_variant)

    def test_validator_requires_covariance_reciprocity_and_unit_weights(self):
        good = VariantCoupling.reference((1, 1, 1))
        ports, weights = [list(r) for r in good.ports], [list(r) for r in good.weights]

        def variant(p=None, w=None, name="bad"):
            return VariantCoupling(name, p if p is not None else ports, w if w is not None else weights)

        bond_flip = [list(r) for r in weights]          # reciprocal, but one bond class only
        bond_flip[0][5] = bond_flip[1][ports[0][5]] = -1
        relabel = [list(r) for r in ports]               # reciprocal relabelling of one pair of ports
        g0, g1 = 0, 1
        h0, h1 = relabel[0][g0], relabel[0][g1]
        relabel[0][g0], relabel[0][g1] = h1, h0
        relabel[1][h1], relabel[1][h0] = g0, g1
        swapped = [list(r) for r in ports]
        swapped[0][0], swapped[0][1] = swapped[0][1], swapped[0][0]
        repeated = [list(r) for r in ports]
        repeated[2][5] = repeated[2][6]
        zero = [list(r) for r in weights]
        zero[1][3] = zero[0][ports[1][3]] = 0
        doubled = [[2 * w for w in r] for r in weights]
        boolean = [list(r) for r in weights]
        boolean[0][0] = True
        cases = (("reciprocal but not covariant (weights)", lambda: variant(w=bond_flip), "covariant"),
                 ("reciprocal but not covariant (ports)", lambda: variant(p=relabel), "covariant"),
                 ("nonreciprocal port", lambda: variant(p=swapped), "Nonreciprocal"),
                 ("not a permutation", lambda: variant(p=repeated), "permutation"),
                 ("deleted port", lambda: variant(w=zero), r"\+1 or -1"),
                 ("rescaled ports", lambda: variant(w=doubled), r"\+1 or -1"),
                 ("covariant, not reciprocal", lambda: VariantCoupling.from_body_actions(
                     "x", (1, 1, 2, 2, 46, 46), (1,) * 6), ""),
                 ("unequal pair signs", lambda: good.with_body_weights("x", (1, -1, 1, 1, 1, 1)), ""),
                 ("inconsistent z twist", lambda: good.z_twisted("x", (1, 0, 0, 0, 0, 0)), ""),
                 ("exponent outside Z/8Z", lambda: VariantCoupling.axial("a", (0, 1, 8)), ""),
                 ("five directions", lambda: variant(p=ports[:5]), ""),
                 ("47 channels", lambda: variant(p=[r[:47] for r in ports]), ""),
                 ("bad name", lambda: variant(name=" x"), ""),
                 ("false construction", lambda: VariantCoupling(
                     "x", ports, weights, {"kind": "reference", "signs": [1, -1, 1]}), "construction"))
        for label, call, message in cases:
            with self.subTest(label), self.assertRaisesRegex(ValueError, message):
                call()
        with self.assertRaises(TypeError):
            variant(w=boolean)
        with self.assertRaises(TypeError):
            VariantEngine(Coupling((1, 1, 1)))

    def test_constructors_stay_inside_the_algebra(self):
        reference = VariantCoupling.reference((1, 1, 1))
        twisted = reference.z_twisted("twist-x", (1, 1, 0, 0, 0, 0))
        self.assertEqual(twisted.fingerprint, VariantCoupling.axial("axial-413", (4, 1, 3)).fingerprint)
        self.assertTrue(twisted.is_variant)
        for signs in SIGN_TRIPLES:
            body = tuple(s for s in signs for _ in (0, 1))
            self.assertEqual(reference.with_body_weights("w", body).reference_signs, signs)
            gauged = VariantCoupling.reference(signs).chi_gauged("chi")
            self.assertEqual(gauged.reference_signs, (signs[0], -signs[1], -signs[2]))

    def test_chi_gauge_conjugates_the_dynamics(self):
        rng = random.Random(5)
        for trial in range(4):
            coupling = random_member(rng)
            forward, gauged = VariantEngine(coupling), VariantEngine(coupling.chi_gauged("chi"))
            state = random_state(rng, 3, 2 + trial % 2, cells=50)
            image = chi_gauge_state(state)
            self.assertEqual(chi_gauge_state(image), state)
            for _ in range(4):
                state, image = forward.advance(state), gauged.advance(image)
                self.assertEqual(chi_gauge_state(state), image)
        with self.assertRaises(ValueError):
            chi_gauge_state(random_state(rng, 3, 4))
        coupling = random_member(rng)
        negated = coupling.with_body_weights("negated", tuple(-w for w in coupling.body_weights))
        state = random_state(rng, 4, 2, cells=50)
        image = staggered_state(state)
        for _ in range(4):
            state, image = VariantEngine(coupling).advance(state), VariantEngine(negated).advance(image)
            self.assertEqual(staggered_state(state), image)
        with self.assertRaises(ValueError):
            staggered_state(random_state(rng, 3, 2))


class VariantMathematics(unittest.TestCase):
    def test_exact_inverse_and_identities_for_family_members(self):
        rng = random.Random(7)
        for trial in range(8):
            engine = VariantEngine(random_member(rng))
            state = random_state(rng, 3 + trial % 3, rng.randrange(6), cells=60, big=True)
            with self.subTest(trial=trial, coupling=engine.label):
                nxt = engine.advance(state)
                self.assertEqual(engine.rewind(nxt), state)
                self.assertEqual(engine.advance(engine.rewind(state)), state)
                self.assertEqual(balance_residuals(state, nxt, engine), {})
                self.assertEqual(signed_account(nxt) - signed_account(state),
                                 expected_account_change(state, engine))
                states = list(engine.evolve(state, 5))
                for before, after in zip(states, states[1:]):
                    self.assertEqual(engine.rewind(after), before)

    def test_sparse_scatter_equals_dense_gather(self):
        rng = random.Random(11)
        couplings = [random_member(rng), random_member(rng), VariantCoupling.axial("axial-075", (0, 7, 5), (1, -1, 1)),
                     VariantCoupling.reference((-1, 1, -1))]
        for coupling in couplings:
            state = random_state(rng, 3, 2, cells=30)
            with self.subTest(coupling=coupling.label):
                self.assertEqual(VariantEngine(coupling).advance(state), gather_advance(coupling, state))

    def test_bloch_matrix(self):
        rng = random.Random(13)
        reference = VariantCoupling.reference((1, 1, 1))
        k = (0.3, -1.1, 2.0)
        uniform = [sum(row) for row in reference.bloch_matrix(k)]
        expected = 2 * (math.cos(0.3) + math.cos(-1.1) + math.cos(2.0))
        self.assertTrue(all(abs(v - expected) < 1e-12 for v in uniform))
        for _ in range(3):
            coupling = random_member(rng)
            A = coupling.bloch_matrix([rng.uniform(-math.pi, math.pi) for _ in range(3)])
            self.assertTrue(all(abs(A[g][h] - A[h][g].conjugate()) < 1e-12 for g in range(48) for h in range(48)))
            # Fourier transform of the engine's own impulse responses (scatter form) on L = 3.
            engine, cube = VariantEngine(coupling), Cube(3)
            n = (1, 0, 2)
            q = tuple(2 * math.pi * c / 3 for c in n)
            A = coupling.bloch_matrix(q)
            for h in range(48):
                sums = engine.input_sums(State(cube, cells={(0, 0, 0, h): Channel(0, 1, 2)}))
                column = [0j] * 48
                for (x, y, z, g), u in sums.items():
                    column[g] += u * cmath.exp(-1j * (q[0] * x + q[1] * y + q[2] * z))
                self.assertTrue(all(abs(column[g] - A[g][h]) < 1e-9 for g in range(48)))


class InitFilesAndRunner(unittest.TestCase):
    def test_init_round_trip_fingerprint_and_reference_loader_refusal(self):
        coupling = VariantCoupling.axial("axial-017", (0, 1, 7))
        state = random_state(random.Random(3), 5, 2)
        with tempfile.TemporaryDirectory() as tmp:
            path = write_init(Path(tmp) / "v.json", coupling, state, 9)
            experiment = load(path)
            self.assertEqual(experiment.initial, state)
            self.assertEqual(experiment.steps, 9)
            self.assertEqual(experiment.engine.coupling, coupling)
            self.assertEqual(experiment.label, coupling.label)
            with self.assertRaises(FileExistsError):
                write_init(path, coupling, state, 9)
            data = json.loads(path.read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            reference_from_dict(data)
        tampered = json.loads(json.dumps(data))
        tampered["coupling"]["fingerprint"] = "0" * 64
        broken = json.loads(json.dumps(data))
        row = broken["coupling"]["ports"][0]
        row[0], row[1] = row[1], row[0]
        relabelled = json.loads(json.dumps(data))
        relabelled["coupling"]["construction"]["m"] = [0, 1, 3]
        for bad in (tampered, broken, relabelled, {**data, "format": "universe24-init"},
                    {**data, "coupling_signs": [1, 1, 1]}):
            with self.assertRaises(ValueError):
                from_dict(bad)

    def test_shipped_examples(self):
        native = reference_load(ROOT / "examples" / "impulse.json")
        same = load(PACKAGE / "examples" / "impulse_reference_ppp.json")
        other = load(PACKAGE / "examples" / "impulse_axial_m017.json")
        self.assertEqual((same.initial, same.steps), (native.initial, native.steps))
        self.assertEqual(same.label, "reference:+++")
        self.assertEqual((other.initial, other.steps), (native.initial, native.steps))
        self.assertTrue(other.label.startswith("variant:axial-m017-ppp@"))
        self.assertEqual(list(same.engine.evolve(same.initial, 12)), list(native.engine.evolve(native.initial, 12)))

    def test_runner_reproduces_the_official_cli_and_labels_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            out = io.StringIO()
            native = reference_load(ROOT / "examples" / "signed_impulse.json")
            config = write_init(tmp / "variant.json", VariantCoupling.reference((1, -1, 1)),
                                native.initial, native.steps)
            with redirect_stdout(out):
                self.assertEqual(reference_main(["--config", str(ROOT / "examples" / "signed_impulse.json"),
                                                 "--events", str(tmp / "ref.jsonl"),
                                                 "--output", str(tmp / "ref.json"), "--audit"]), 0)
                self.assertEqual(variant_main(["--config", str(config), "--events", str(tmp / "var.jsonl"),
                                               "--output", str(tmp / "var.json"),
                                               "--summary", str(tmp / "summary.json"), "--audit"]), 0)
            self.assertEqual((tmp / "var.jsonl").read_bytes(), (tmp / "ref.jsonl").read_bytes())
            self.assertGreater(len((tmp / "ref.jsonl").read_bytes()), 0)
            final = reference_from_dict(json.loads((tmp / "ref.json").read_text())["experiment"]).initial
            engine, state, completed = read_checkpoint(tmp / "var.json")
            self.assertEqual((state, completed), (final, 12))
            record = json.loads((tmp / "summary.json").read_text())
            self.assertEqual((record["model"], record["coupling_label"]), ("reference-equivalent", "reference:+-+"))
            self.assertEqual(record["reference_fingerprint"], Coupling((1, -1, 1)).fingerprint)
            variant = write_init(tmp / "axial.json", VariantCoupling.axial("axial-017", (0, 1, 7)), native.initial, 6)
            with redirect_stdout(out):
                self.assertEqual(variant_main(["--config", str(variant), "--summary", str(tmp / "axial_summary.json"),
                                               "--audit"]), 0)
            record = json.loads((tmp / "axial_summary.json").read_text())
            self.assertEqual(record["model"], "variant")
            self.assertTrue(record["coupling_label"].startswith("variant:axial-017@"))
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                self.assertEqual(reference_main(["--config", str(variant)]), 2)

    def test_package_imports_only_the_engine_and_the_standard_library(self):
        allowed = set(sys.stdlib_module_names) | {"universe24"}
        for path in PACKAGE.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".")[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    if node.module == "research.matter_light_blocks_v1" and path.name == "audit.py":
                        continue
                    roots = {node.module.split(".")[0]}
                else:
                    continue
                with self.subTest(file=path.name, imports=sorted(roots)):
                    self.assertLessEqual(roots, allowed)


if __name__ == "__main__":
    unittest.main()
