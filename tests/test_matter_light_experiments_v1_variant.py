"""Curated experiments under an explicitly separate candidate variant: the manifest's variant coupling (label and
fingerprint), data loaded only by research.coupling_variants_v1, and the variant runner's audited log read by the
decoder."""
import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import shutil
import tempfile
import unittest

from research.coupling_variants_v1 import VariantCoupling, init_data, read_checkpoint, write_init
from research.coupling_variants_v1.__main__ import main as variant_main
from research.matter_light_experiments_v1 import verify as X

SOURCE = X.ROOT / "research/coupling_variants_v1/examples/impulse_axial_m017.json"      # a format example, no claim
FINGERPRINT = "fc4d2d79f6341c27348dda941edf1cce3366969bf2f8748de18de110a450ec0e"
LABEL = "variant:axial-m017-ppp@fc4d2d79f634"
COUPLING = {"kind": "variant", "label": LABEL, "fingerprint": FINGERPRINT}       # as in the blocks catalog
EID = "E99_variant_test"


def runner_record(config: Path, tmp: Path):
    """The variant runner's own CLI run of ``config``: (log SHA-256, final-state SHA-256, records)."""
    tmp.mkdir(parents=True, exist_ok=True)
    log, final = tmp / "cli.jsonl", tmp / "cli.final.json"
    with redirect_stdout(io.StringIO()):
        assert variant_main(["--config", str(config), "--events", str(log), "--output", str(final), "--audit"]) == 0
    state = read_checkpoint(final)[1]
    return hashlib.sha256(log.read_bytes()).hexdigest(), X.state_sha256(state), len(log.read_bytes().splitlines())


class VariantExperiments(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self._here, X.HERE = X.HERE, self.tmp / "package"             # a scratch package folder for this test only
        folder = X.HERE / EID
        (folder / "data").mkdir(parents=True)
        shutil.copy(SOURCE, folder / "data" / "impulse.json")
        start = X.load_data({"coupling": COUPLING}, SOURCE.read_bytes())
        earlier = X.rewind_preparation(start.engine, start.initial, 3)
        write_init(self.tmp / "earlier.json", start.engine.coupling, earlier, 3)
        (self.log_sha, final_sha, self.records), back = (runner_record(SOURCE, self.tmp / "a"),
                                                         runner_record(self.tmp / "earlier.json", self.tmp / "b"))
        frozen = json.loads((X.ROOT / "research/click_decoder_v1/FROZEN.json").read_text(encoding="utf-8"))
        from research import click_decoder_v1 as dec
        self.man = {
            "format": X.FORMAT, "id": EID, "card": "CARD.md", "coupling": dict(COUPLING),
            "composition": None, "compositions": {"impulse": "data/impulse.json"},
            "runs": [{"name": "file", "role": "main", "init": "data/impulse.json",
                      "init_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "steps": 12,
                      "final_state_sha256": final_sha, "log_sha256": self.log_sha},
                     {"name": "rewound", "role": "phase", "from_composition": {"composition": "impulse", "rewind": 3},
                      "steps": 3, "initial_state_sha256": X.state_sha256(earlier),
                      "final_state_sha256": back[1], "log_sha256": back[0]}],
            "checks": [{"claim": "V-1", "text": "the decoder reads the runner's log", "run": "file",
                        "pointer": "/input/events", "op": "eq", "value": self.records}],
            "decoder": {"name": "click_decoder_v1", "version": dec.VERSION, "code_sha256": frozen["code_sha256"]},
            "verdict": {"referee": "test", "id": "T", "result": "CONFIRMED"}}
        self.assertEqual(back[1], X.state_sha256(start.initial))        # 3 rewinds, then 3 updates: the file again
        self.write()

    def tearDown(self):
        X.HERE = self._here
        self._tmp.cleanup()

    def write(self, man=None):
        (X.HERE / EID / "experiment.json").write_text(json.dumps(man or self.man), encoding="utf-8")

    def test_runs_replay_through_the_audited_variant_runner(self):
        out = X.verify(EID, keep=str(self.tmp / "keep"))
        self.assertTrue(out["ok"] and out["ready"], out)
        self.assertEqual(out["coupling"], COUPLING)
        first, second = out["runs"]
        self.assertEqual((first["final_state"], first["log"], first["clicks"]), ("ok", "ok", self.records))
        self.assertEqual(first["runner"], {"model": "variant", "coupling_label": LABEL,
                                           "variant_fingerprint": FINGERPRINT, "audited": True})
        self.assertEqual((second["final_state"], second["log"]), ("ok", "ok"))
        self.assertIn("3 exact rewinds", second["composition"])
        self.assertEqual(out["checks"][0]["result"], "pass")
        kept = self.tmp / "keep" / EID / "file.events.jsonl"     # the log the decoder read is the runner's CLI log
        self.assertEqual(hashlib.sha256(kept.read_bytes()).hexdigest(), self.log_sha)

    def test_the_table_must_be_the_declared_one(self):
        def errors(man):
            self.write(man)
            return [r.get("error", "") for r in X.verify(EID)["runs"]]

        other = json.loads(json.dumps(self.man))
        other["coupling"] = {"kind": "variant", "label": "variant:axial-m017-ppp@000000000000", "fingerprint": "0" * 64}
        self.assertTrue(all("not the manifest's variant table" in e for e in errors(other)))
        renamed = json.loads(json.dumps(self.man))
        renamed["coupling"]["label"] = "variant:other-name@fc4d2d79f634"
        self.assertTrue(all("not the manifest's variant table" in e for e in errors(renamed)))
        for bad in ({"kind": "variant"}, {"kind": "variant", "label": LABEL},
                    {"kind": "variant", "label": "variant:axial-m017-ppp@000000000000", "fingerprint": FINGERPRINT},
                    {"kind": "variant", "label": LABEL, "fingerprint": FINGERPRINT[:12]},
                    {**COUPLING, "signs": [1, 1, 1]}, {**COUPLING, "label": 7}, {**COUPLING, "fingerprint": None}):
            with self.subTest(coupling=bad), self.assertRaises(ValueError):
                X.variant_model({"coupling": bad})
        self.assertEqual(X.variant_model({"coupling": COUPLING}), (LABEL, FINGERPRINT))
        folder = X.HERE / EID / "data"
        shutil.copy(X.ROOT / "examples" / "impulse.json", folder / "official.json")       # the reference format
        state = X.load_data(self.man, SOURCE.read_bytes()).initial
        (folder / "reference_table.json").write_text(json.dumps(init_data(VariantCoupling.reference((1, 1, 1)),
                                                                          state, 12)), encoding="utf-8")
        for name, message in (("official.json", "files only"), ("reference_table.json", "not the manifest's variant")):
            man = json.loads(json.dumps(self.man))
            man["runs"] = [dict(man["runs"][0], init=f"data/{name}",
                                init_sha256=hashlib.sha256((folder / name).read_bytes()).hexdigest())]
            with self.subTest(file=name):
                self.assertIn(message, errors(man)[0])
        reference = json.loads(json.dumps(self.man))
        reference["coupling"], reference["compositions"] = {"kind": "reference", "signs": [1, 1, 1]}, None
        reference["runs"] = reference["runs"][:1]
        self.assertIn("Unsupported keys", errors(reference)[0])   # the official loader refuses a variant file

    def test_variant_board_files(self):
        build = X._composition(EID, self.man)
        self.assertEqual(build(None, "impulse").engine.coupling.fingerprint, FINGERPRINT)
        for control, key in ((None, "undeclared"), ("a control", "impulse")):
            with self.subTest(control=control, key=key), self.assertRaises(ValueError):
                build(control, key)
        outside = dict(self.man, compositions={"up": "../../README.md"})
        with self.assertRaises(ValueError):
            X._composition(EID, outside)(None, "up")
        registry = json.loads(json.dumps(self.man))                 # a registry composition is not a variant file
        (X.HERE / EID / "data" / "comp.json").write_text(json.dumps({"format": "u24-composition-v1"}), encoding="utf-8")
        registry["compositions"] = {"c": "data/comp.json"}
        with self.assertRaisesRegex(ValueError, "files only"):
            X._composition(EID, registry)(None, "c")

    def test_shipped_manifests_keep_their_path(self):
        X.HERE = self._here
        for eid in X.experiment_ids():
            man = X.manifest(eid)
            with self.subTest(experiment=eid):
                if man["coupling"].get("kind") == "variant":
                    self.assertEqual(X.variant_model(man), (man["coupling"]["label"], man["coupling"]["fingerprint"]))
                else:
                    self.assertIsNone(X.variant_model(man))
                    self.assertEqual(man["coupling"]["kind"], "reference")


if __name__ == "__main__":
    unittest.main()
