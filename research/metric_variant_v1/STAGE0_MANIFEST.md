# STAGE 0 MANIFEST — research/metric_variant_v1 (snapshots 0.0, 0.1, 0.2a, 0.2; CURRENT = 0.2 (final), see the last section)

Frozen: Tue Nov 10 09:06:23 UTC 2026 (`date -u`), by B0-BUILD. This is the exact snapshot the review board reviews. Any later change to
a listed code file must add a new section "stage 0.x" below, with new hashes, the reason and fresh test results.
Not part of this snapshot: `verify_b0/` (the independent verifier's own work) and `review/` (the reviewers' area).
No git was used; nothing else in the repository was created or changed (scratch files lived in the session
scratchpad, outside the repository). The `results/` files are evidence of the freeze run: every test run rewrites them
with new `date -u` stamps, so after a re-run only the code/doc hashes are expected to match.

## Test commands (from the repository root)
```bash
OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers -v
python research/metric_variant_v1/tools/export_fixtures.py      # fixtures for independent cross-checks
sha256sum -c <(sed -n 's/^| `\([^`]*\)` | `\([0-9a-f]*\)` .*/\2  \1/p' research/metric_variant_v1/STAGE0_MANIFEST.md | sed 's#  #  research/metric_variant_v1/#')
```
Last full run on this snapshot: 14 tests, OK, 23.8 s (09:04:53-09:05:17 UTC); T0.1-T0.10 all PASS (T0.7 reported:
34.7 updates/s at L = 16, 80 gears/node, 628 monomials, int64 path). Details: NOTES.md.

## Files (sha256, bytes)
| file | sha256 | bytes | role |
|---|---|---|---|
| `NOTES.md` | `c8f21eaabb0cad3e3958686db71f34266e0e9d36413f4c3f6b9a389456605d0c` | 16588 | pre-registrations and results log (append-only; hash at freeze time) |
| `README.md` | `e69edd42293701e0aa838663a8dd32ff03f449ec4a4c5db50039cd35e78d486c` | 15505 | package description, definition, tensor/state formats, layer contract |
| `__init__.py` | `a8ccfe8280b870aa07819af6195af9a3c0d37b2f62fe5ceced0b5265dba665aa` | 243 | package marker |
| `core/__init__.py` | `f6386fa0306ae71f8935f93c000437db19979122b80817c3cbb7e30fcee066f9` | 938 | core exports |
| `core/bridge.py` | `375e227db404e86895210e66597f9fdd5557d0193c48b6f62148f525854edaa8` | 1764 | read-only universe24 State <-> dense arrays (r x Q) |
| `core/engine.py` | `5fe06f85377c454ec3774caa3ef2c9874edee2aeac8a4be2c02832bfac03cc50` | 18872 | State, Engine (step, staged inverse, mirror, vacuum, inputs), passive clicks |
| `core/lattice.py` | `10cde9089e48d314b39d771d5a0f6213b415fac7b8a637b8e105f216a046f483` | 4013 | periodic L^3 indexing, 6 face directions, Yee link convention |
| `core/reciprocity.py` | `a5b6430127720729d791f174c127fb35bc8180dd2479d3ba17bf3627b223c5a4` | 5032 | reciprocity checker (gradient of one potential, field signs, one-way designations) |
| `core/tensor.py` | `41d72e7df095ac6b7c9112f3487499c387eb07352c25c00c29809b119b8d35ea` | 21674 | GearType/Factor/Monomial/Tensor, B3 locality, a-read stages, canonical form, JSON, Block, compose, reference_block |
| `layers/__init__.py` | `8fc22775814533b2b1273a239b66b4e3a5c52439f1e9dd2be995ec7351df3c5b` | 1816 | layer contract (tensor blocks only), LINKS FROZEN convention |
| `layers/reference.py` | `0e81b8e5d5428a5fe0aa05f6f3ac2fcfdc08314dcbfa808f15c324796654a3b1` | 1227 | build_reference (48 +++ channels, Q-scaled) |
| `observe/__init__.py` | `79e5c1367f6209576123f91f69024b366add002032b50cbe26c009bfb2ef1af0` | 765 | read-only observables |
| `observe/audit.py` | `e9fd04c2f3b0f8af7bd34fbdb354f283770dfb9fa7208f83f2599ed838d0b54d` | 2178 | frozen_equivalence audit harness (two independent runs compared) |
| `prepare/__init__.py` | `e7f535de4a45c4243058f6189bda5c3a45dd7d290ad9f381bc14cf640d5dabf2` | 2156 | initial-data helpers only |
| `tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | test package marker |
| `tests/randgen.py` | `0e44b0cf65fbcbb6b4feaa646110bcc5ea8ca6c7772cbf0e1a5e92d1608b5af2` | 7653 | seeded random B3-local tensors/states (test data) |
| `tests/test_core.py` | `19d825fac2dcd57c551552e5a2a586c4b3049f54fc4af8d227dea966f78490ff` | 21739 | acceptance tests T0.1-T0.7 |
| `tests/test_layers.py` | `9c3bb6c2d874078a8871a3eaa9d6e242ed550cdc804570f79d97ca3f8bf447de` | 9783 | acceptance tests T0.8-T0.10 |
| `tools/export_fixtures.py` | `10599c6834e39854a1178f44101ce260900b7050001105b403f72719fadab376` | 4281 | fixture export for independent cross-checks |
| `results/T0.1.json` | `7cc102faa1c154e08be9f03b96ddc2b200ca8123adb2d3d0a0798523115f307e` | 1844 | evidence (test output, written by the run) |
| `results/T0.10.json` | `6728cd45c254021cebb0367e3c1e0ee8d9c4dbdaa5a69b510a4e80aca47e1dd9` | 569 | evidence (test output, written by the run) |
| `results/T0.1_fixed_point.json` | `a12c39668767831be6a36722ac5ced70e7dfc4366baa559e5145ab0e368cc46c` | 227 | evidence (test output, written by the run) |
| `results/T0.2.json` | `8ff9f3d582314ecbe86188d2c1ce8344eae2c656dc639cf2cc693d8180dc7c7c` | 1283 | evidence (test output, written by the run) |
| `results/T0.3.json` | `c901a376addf3026fc373eb232edbbd9c9c1fb03f84fa44ae3c5c58db441807d` | 4759 | evidence (test output, written by the run) |
| `results/T0.3_extra.json` | `15f8e35a6da478e4028f0dc8bdb36754c118bf88b06a74ab591fda6012870c0d` | 665 | evidence (test output, written by the run) |
| `results/T0.4.json` | `f77ddb05c4cb7dd47a75c924734da3cd84b039e3823118a82586ddea0e7d609a` | 777 | evidence (test output, written by the run) |
| `results/T0.5.json` | `9a46b18cd9e5465db6fd1464dfb34d8c7d331da6c467352df8e060b6eeb6595d` | 1829 | evidence (test output, written by the run) |
| `results/T0.6a.json` | `b50c2bad787bc407a55a76fb088d813f6147e0e6298d37e6bbe0cee6beddc185` | 249 | evidence (test output, written by the run) |
| `results/T0.6b.json` | `d97f01c3c1a49b2bce262241ee2b8c17607c4f563feee5f2c04025e1b87ad36c` | 295 | evidence (test output, written by the run) |
| `results/T0.7.json` | `e00a07271464dec56bd04ec19b2fb8541e37f5a59c7e4d8be35aede570fbbd0c` | 560 | evidence (test output, written by the run) |
| `results/T0.8.json` | `deb996b0696a04780ed3358317eb545f16892c38a1ddb015ae2113fdb558fabd` | 1303 | evidence (test output, written by the run) |
| `results/T0.9.json` | `e6f49f5ed9346a2c071089b0a8c7923511284e903ae7149ccebb779330dfc4e9` | 177 | evidence (test output, written by the run) |
| `results/fixtures/INDEX.json` | `0658fea2dfd3e3cb19c082bf3400cd586e005f32c6154ac0dedecfedb7f70e6c` | 1692 | evidence (test output, written by the run) |
| `results/fixtures/cubic_Q1_bigint_seed32_L4.json` | `c54ca00bc2dddd75aea412ebae45ae21eb7f52071690e44065bb8a04e079d302` | 303440 | evidence (test output, written by the run) |
| `results/fixtures/rand_a_reads_seed11_L4.json` | `043ba6733811c4635da570717b9e95656cca67521579f3ffdebcc79e537e4ede` | 161989 | evidence (test output, written by the run) |
| `results/fixtures/rand_b_only_seed10_L4.json` | `89ca5b1b9a6680dcfbad1885d9c875d4591a18fb4d4f72f475f4aa598491b46b` | 191852 | evidence (test output, written by the run) |
| `results/fixtures/ref7_plus_32_new_coupled_L4.json` | `adb440ed4acc0ee7a45b223bf0dffae4263157ba81121732213a216d4e3dfd62` | 1087510 | evidence (test output, written by the run) |
| `results/fixtures/ref_Q1_L4.json` | `2d108805909f3a18adcc94956774761b0595e63acf29f14f48dc74f3c2a5b8f9` | 1048427 | evidence (test output, written by the run) |
| `results/fixtures/ref_Q7_L4.json` | `ba4b9fbea6f71ada7096582b8a7cd5974cc4ed1d9255e8a158c11c1a8c7c9121` | 1052584 | evidence (test output, written by the run) |

## STAGE 0.1 (frozen Tue Nov 10 09:11:43 UTC 2026, `date -u`) — superseded by 0.2
Reasons:
1. BUG FIX (found by B0-VERIFY X7, a real bug): `np.abs(int64(-2^63))` is -2^63. So the int64 guard could
   under-estimate a USER-GIVEN state entry equal to -2^63, and the step then wrapped silently. The engine's own
   evolution cannot reach it. Fix in `core/engine.py`: an exact max-abs `max(int(max), -int(min))` in `exact_array`,
   `_maxabs_rows` and `_fits`; plain lists are read as Python ints (never float-inferred).
2. Manager ruling 09:08 on X11: the storage rule stays BINDING. The strict physical-support rule is OPT-IN, as
   `strict_support=True` in `Tensor`, `compose`/`build`, `TensorBuilder.build` and `Tensor.from_dict`/`from_json`
   (`core/tensor.py`). Default behaviour is unchanged.

New tests (`tests/test_stage01.py`): T0.11 int64 extremes against a pure-Python oracle, 22/22. With the 0.0 guard
the test fails, so it reproduces X7. T0.12 opt-in strict support also PASSES.

Regression on 0.1:
- the full suite gives 16 tests OK in 23.1 s (09:10:42-09:11:05 UTC); T0.1-T0.10 have identical verdicts and
  numbers;
- T0.7 runs at 42.3 updates/s on the int64 path;
- the six fixtures reproduce their stage-0.0 per-update state hashes 6/6 (82 hashes identical).

Test command and hash check for 0.1 (from the repository root):
```bash
OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers research.metric_variant_v1.tests.test_stage01 -v
cd research/metric_variant_v1 && sed -n '/^## STAGE 0.1/,$p' STAGE0_MANIFEST.md | sed -n 's/^| `\([^`]*\)` | `\([0-9a-f]*\)` .*/\2  \1/p' | sha256sum -c
```

| file | sha256 | bytes | vs 0.0 |
|---|---|---|---|
| `NOTES.md` | `0bef44e9905bfb8e2c5e6534381f10fa2e5c947ca4394a026c695af73d5a585d` | 19989 | CHANGED |
| `README.md` | `6e7e2c9624c49b5a1f82ae82eeded1f739afa5e19d0755afe4b36c735d763ca1` | 16498 | CHANGED |
| `__init__.py` | `a8ccfe8280b870aa07819af6195af9a3c0d37b2f62fe5ceced0b5265dba665aa` | 243 | unchanged |
| `core/__init__.py` | `f6386fa0306ae71f8935f93c000437db19979122b80817c3cbb7e30fcee066f9` | 938 | unchanged |
| `core/bridge.py` | `375e227db404e86895210e66597f9fdd5557d0193c48b6f62148f525854edaa8` | 1764 | unchanged |
| `core/engine.py` | `da46bafa70964791aafd7c968a413052cf6a6139791f1469958d1c7ea066e2ce` | 19151 | CHANGED |
| `core/lattice.py` | `10cde9089e48d314b39d771d5a0f6213b415fac7b8a637b8e105f216a046f483` | 4013 | unchanged |
| `core/reciprocity.py` | `a5b6430127720729d791f174c127fb35bc8180dd2479d3ba17bf3627b223c5a4` | 5032 | unchanged |
| `core/tensor.py` | `828161e73a36806f326d85f1a06006d0bdae15534a3a4d3c30b876f2c36f6920` | 22892 | CHANGED |
| `layers/__init__.py` | `8fc22775814533b2b1273a239b66b4e3a5c52439f1e9dd2be995ec7351df3c5b` | 1816 | unchanged |
| `layers/reference.py` | `0e81b8e5d5428a5fe0aa05f6f3ac2fcfdc08314dcbfa808f15c324796654a3b1` | 1227 | unchanged |
| `observe/__init__.py` | `79e5c1367f6209576123f91f69024b366add002032b50cbe26c009bfb2ef1af0` | 765 | unchanged |
| `observe/audit.py` | `e9fd04c2f3b0f8af7bd34fbdb354f283770dfb9fa7208f83f2599ed838d0b54d` | 2178 | unchanged |
| `prepare/__init__.py` | `e7f535de4a45c4243058f6189bda5c3a45dd7d290ad9f381bc14cf640d5dabf2` | 2156 | unchanged |
| `tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | unchanged |
| `tests/randgen.py` | `0e44b0cf65fbcbb6b4feaa646110bcc5ea8ca6c7772cbf0e1a5e92d1608b5af2` | 7653 | unchanged |
| `tests/test_core.py` | `19d825fac2dcd57c551552e5a2a586c4b3049f54fc4af8d227dea966f78490ff` | 21739 | unchanged |
| `tests/test_layers.py` | `9c3bb6c2d874078a8871a3eaa9d6e242ed550cdc804570f79d97ca3f8bf447de` | 9783 | unchanged |
| `tests/test_stage01.py` | `faef096884822c1bbd6a1bc229729619833e060777fa19d056dcee2136e07171` | 7494 | new |
| `tools/export_fixtures.py` | `10599c6834e39854a1178f44101ce260900b7050001105b403f72719fadab376` | 4281 | unchanged |
| `results/T0.1.json` | `91b59fa98adbc084300b2cfc292da8be7dc468d1b38326d5c74498a2a4ecacf1` | 1844 | re-run evidence |
| `results/T0.10.json` | `5e7db597e2631a5d56dec20ec945deaa9567a02aa268bae8be88dd9b0e6b51bc` | 569 | re-run evidence |
| `results/T0.11.json` | `53e2805c23ef147a09b3a104cffe9e6c7bda4162fc7e08fa1b00e2f50cd8a495` | 1021 | new |
| `results/T0.12.json` | `cbf60ea41361adca9ed51b1dd3592801599e80969c3fc76b2d2bf799a55cabf6` | 368 | new |
| `results/T0.1_fixed_point.json` | `22e55f19b5484caf4c2f3205c2f7f4d700d4cbc9827f1f76c6df9591cae192bc` | 227 | re-run evidence |
| `results/T0.2.json` | `f2bf9149a61543f5aa4374becf203c53e8f19327b1cbea83328ec1472c55aee0` | 1283 | re-run evidence |
| `results/T0.3.json` | `925eb69cdb37fdf5089a2c224d0e39e68eb78805b8f48d6adf5998d94c8ddf5d` | 4759 | re-run evidence |
| `results/T0.3_extra.json` | `db945292d681bb76553ad8a71677aa4e146eac5ba7bf1b88dc74a26e6b4b3634` | 665 | re-run evidence |
| `results/T0.4.json` | `f8aaf23196ef94a34909e85411cb27bfe7d5001e251fb1f5aa36df8f939733df` | 777 | re-run evidence |
| `results/T0.5.json` | `307b6a1c9b748a6d066c3a23e5b8009a0d778bf5915694fd20f38104dc951e41` | 1829 | re-run evidence |
| `results/T0.6a.json` | `5a6b1f5dfa0445307744ae8256e9325bdeb41e9b08ac8614b4772b68a5e5c694` | 249 | re-run evidence |
| `results/T0.6b.json` | `d2d05f036c02f8479ff6e4e200d14301925e7b983d6a06394e1d7d877ff6a173` | 295 | re-run evidence |
| `results/T0.7.json` | `87e2c8000a97a138bf3771b05f83c1e3d113a84ac742f499e8c8b7dec4ad0e28` | 560 | re-run evidence |
| `results/T0.8.json` | `f1b61295892bf94b58ae503b3de542c399aae0b192cd1845c5d9dd90b063296d` | 1303 | re-run evidence |
| `results/T0.9.json` | `0b9561376e53db4545a12f9d12c9c38f838898e9896084ca334a1f09644e882e` | 177 | re-run evidence |
| `results/fixtures/INDEX.json` | `36bf742727a38d1ef080e1a636bd455e75996e82c852164eb1549899e039ee69` | 1692 | re-run evidence |
| `results/fixtures/cubic_Q1_bigint_seed32_L4.json` | `d6bd49eeb72a294938431ad14925c66d2698de2f96d8843c3f9a8c47d530cc56` | 303440 | re-run evidence |
| `results/fixtures/rand_a_reads_seed11_L4.json` | `e38b7d4ea422af79454b12be36c37f598a25a8325510458ef3a5f7dc7f852fa2` | 161989 | re-run evidence |
| `results/fixtures/rand_b_only_seed10_L4.json` | `55b85f114636f0886f4ac32f4248dcaeb0b43dc95b8d8e49ed1e3001f2c28551` | 191852 | re-run evidence |
| `results/fixtures/ref7_plus_32_new_coupled_L4.json` | `cdc4139bfd0df92e86435364326760ed98d6ce4c6a6f202e74bf3b52c8032260` | 1087510 | re-run evidence |
| `results/fixtures/ref_Q1_L4.json` | `a7baa4f7cd98c2fb2f29b4bbe6d767d78ad474a7376f9e132c1c6747c3f6623c` | 1048427 | re-run evidence |
| `results/fixtures/ref_Q7_L4.json` | `8fd8df9669b040fe6fb22287a49746d815f4528fc58227b296cd3ec579ed7793` | 1052584 | re-run evidence |

## STAGE 0.2a (frozen Tue Nov 10 09:20:32 UTC 2026, `date -u`) — superseded by 0.2 (never announced; reversors only)
Reason: manager request 09:14 for generic reversor building blocks, needed by the seed study, the reviewers' mirror
checks and the stage-1 layers. The new module `core/reversors.py` provides:
- (a) per-gear maps M, M′, J, JR = J∘M′, plus JM = J∘M and the parity-preserving Jp, with a per-gear choice given
  as data;
- (b) integer group linear maps (signed permutations, or matrices with an explicit remainder rule);
- (c) spatial inversions about a node, a cube centre or the box centre, with Yee link re-basing x → S − x − e_k;
- (d) `reversor_check`, with optional central elements;
- (e) `is_fixed`.

`core/__init__.py` exports them; README and NOTES are updated. The engine, tensor and all earlier code are unchanged,
and the default behaviour is unchanged.

New test: `tests/test_stage02.py`, T0.13. All 7 parts passed on the first run. Regression: 23 tests OK in 27.0 s.
Fixtures reproduce 6/6 (82 per-update hashes identical).

Test command and hash check (from the repository root):
```bash
OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers research.metric_variant_v1.tests.test_stage01 research.metric_variant_v1.tests.test_stage02 -v
cd research/metric_variant_v1 && sed -n '/^## STAGE 0.2/,$p' STAGE0_MANIFEST.md | sed -n 's/^| `\([^`]*\)` | `\([0-9a-f]*\)` .*/\2  \1/p' | sha256sum -c
```

| file | sha256 | bytes | vs 0.1 |
|---|---|---|---|
| `NOTES.md` | `5800ad3ed60f2df08fb8599377f18230a775c6c69430bcb6a52ee5fd7008f3de` | 25667 | CHANGED |
| `README.md` | `1da97f986efe30fb7a6760a926ea0d8d9d6259f26c10becb3988d0fcf0c4abab` | 19791 | CHANGED |
| `__init__.py` | `a8ccfe8280b870aa07819af6195af9a3c0d37b2f62fe5ceced0b5265dba665aa` | 243 | unchanged |
| `core/__init__.py` | `a4ff8d441d1e96c28d691d583f9161804a29a02ae8b725888823a05002ec023c` | 1531 | CHANGED |
| `core/bridge.py` | `375e227db404e86895210e66597f9fdd5557d0193c48b6f62148f525854edaa8` | 1764 | unchanged |
| `core/engine.py` | `da46bafa70964791aafd7c968a413052cf6a6139791f1469958d1c7ea066e2ce` | 19151 | unchanged |
| `core/lattice.py` | `10cde9089e48d314b39d771d5a0f6213b415fac7b8a637b8e105f216a046f483` | 4013 | unchanged |
| `core/reciprocity.py` | `a5b6430127720729d791f174c127fb35bc8180dd2479d3ba17bf3627b223c5a4` | 5032 | unchanged |
| `core/reversors.py` | `b311e60538c03c407356d349291cd950c2a058176efbd8f35ece404e8e69f02e` | 12320 | new |
| `core/tensor.py` | `828161e73a36806f326d85f1a06006d0bdae15534a3a4d3c30b876f2c36f6920` | 22892 | unchanged |
| `layers/__init__.py` | `8fc22775814533b2b1273a239b66b4e3a5c52439f1e9dd2be995ec7351df3c5b` | 1816 | unchanged |
| `layers/reference.py` | `0e81b8e5d5428a5fe0aa05f6f3ac2fcfdc08314dcbfa808f15c324796654a3b1` | 1227 | unchanged |
| `observe/__init__.py` | `79e5c1367f6209576123f91f69024b366add002032b50cbe26c009bfb2ef1af0` | 765 | unchanged |
| `observe/audit.py` | `e9fd04c2f3b0f8af7bd34fbdb354f283770dfb9fa7208f83f2599ed838d0b54d` | 2178 | unchanged |
| `prepare/__init__.py` | `e7f535de4a45c4243058f6189bda5c3a45dd7d290ad9f381bc14cf640d5dabf2` | 2156 | unchanged |
| `tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | unchanged |
| `tests/randgen.py` | `0e44b0cf65fbcbb6b4feaa646110bcc5ea8ca6c7772cbf0e1a5e92d1608b5af2` | 7653 | unchanged |
| `tests/test_core.py` | `19d825fac2dcd57c551552e5a2a586c4b3049f54fc4af8d227dea966f78490ff` | 21739 | unchanged |
| `tests/test_layers.py` | `9c3bb6c2d874078a8871a3eaa9d6e242ed550cdc804570f79d97ca3f8bf447de` | 9783 | unchanged |
| `tests/test_stage01.py` | `faef096884822c1bbd6a1bc229729619833e060777fa19d056dcee2136e07171` | 7494 | unchanged |
| `tests/test_stage02.py` | `94c6cf73d5b64a4ecf551953ffcaa904642c6ca0e7ecfc738241eefc2270d150` | 12760 | new |
| `tools/export_fixtures.py` | `10599c6834e39854a1178f44101ce260900b7050001105b403f72719fadab376` | 4281 | unchanged |
| `results/T0.1.json` | `d5e9083afabf06748fe2377800241f46e0615cf9f84c11beb20fb978c3c25508` | 1844 | re-run evidence |
| `results/T0.10.json` | `42e28b8f5462d22e242447b1fb684b55caec972137728355360e428493ca0435` | 569 | re-run evidence |
| `results/T0.11.json` | `56bc4ee728a9eb56daeb867424b3d00e60963c2772b0d309118da80869d44e4d` | 1021 | re-run evidence |
| `results/T0.12.json` | `70dd1689937b2ebba31d5e1c2f232fad75f6ada62947e2d1160226f94337f41e` | 368 | re-run evidence |
| `results/T0.13_1_involutions.json` | `97e8008d80d7f605adeab614afbc51bdf8121c921ec94408e1c6b978dce04f03` | 1833 | new |
| `results/T0.13_2_Mp_vs_time_reverse.json` | `1d8e4a03ad352e5956b6d20fce96fde968e288adfd0b1e4151e1ca4ddc649678` | 120 | new |
| `results/T0.13_3_reference_reversors.json` | `ecf1f3de80b7f606b4d07dba83f2da5eb1b9a307218a061c637229c30196c6ab` | 1614 | new |
| `results/T0.13_4_reference_inversion.json` | `e3fd9f5d8b0632ba4516920b33b44e9971884b43d312e95e4fb9a8e70d9c8127` | 568 | new |
| `results/T0.13_5_link_rebasing.json` | `6a3f2864a33f2e5bc841dc6369e80645918dbc97afccac948d96db787dc4c917` | 323 | new |
| `results/T0.13_6_central.json` | `515156dd93ccd2a779503156848d610e1ed2d467f95d24630841a845cfba341a` | 569 | new |
| `results/T0.13_7_is_fixed.json` | `9c596ef333398a5ee4d49907ce9b843756d85b9132cfe729ca4a0767ce3af916` | 142 | new |
| `results/T0.1_fixed_point.json` | `7f18e97ee108f96680888360c9b999de097c7ce168458cb7a886bb18d1100271` | 227 | re-run evidence |
| `results/T0.2.json` | `69217d0b53429bef6d60d9f1cae918e40c7aabbaacabb6d9e1141c82df662466` | 1283 | re-run evidence |
| `results/T0.3.json` | `cbf03df72e884002da978b192f930c97ab2d684846ca75fbde46fba5d3767717` | 4759 | re-run evidence |
| `results/T0.3_extra.json` | `e3582e9297ff3add28c3da0ed5e2e95cb6220e929acd38ff7dd8c8f3ac1ce4b8` | 665 | re-run evidence |
| `results/T0.4.json` | `3a7310a256d7c046917ec467318430b6dff8f001385d71072eb13aa6f6c61990` | 777 | re-run evidence |
| `results/T0.5.json` | `bf88c3b4a4a54371ffc535d38654fe418a14b218337f6debd9fdb9f74f73ab52` | 1829 | re-run evidence |
| `results/T0.6a.json` | `b11c78850ef033869700854840127cc214cd87911a08764e1fab54261d81dcbb` | 249 | re-run evidence |
| `results/T0.6b.json` | `2868729c15219fb2f93bd2c1f0ef912101c5fc8c1b297094d0930f7ef6ec3260` | 295 | re-run evidence |
| `results/T0.7.json` | `52eb9643aa3f751bbcaffb2193580a44935023cda3468b761d9fda41272cc0c8` | 560 | re-run evidence |
| `results/T0.8.json` | `22bef0ea73e8f75644fb9fc8227074ec2dd1b71c0525f3f34f5077cf035b4453` | 1303 | re-run evidence |
| `results/T0.9.json` | `fd717f3302f95005a3608a98406a2bf0305aea37472501a8346db1ad3ae20f57` | 177 | re-run evidence |
| `results/fixtures/INDEX.json` | `c68d946824c1588d26aed8f436e9a6ee21b32ccf035db4321ff3b57806973978` | 1692 | re-run evidence |
| `results/fixtures/cubic_Q1_bigint_seed32_L4.json` | `a30d281546dfda7bc46c07dea318ca7bf2ebe49895b9cebfbf4425af237d6ca8` | 303440 | re-run evidence |
| `results/fixtures/rand_a_reads_seed11_L4.json` | `6a934884d3d11be72566396bb5875324331798a1732db7e65a6434814a08ca88` | 161989 | re-run evidence |
| `results/fixtures/rand_b_only_seed10_L4.json` | `8637800acf006b58bc4ae9e926d2b29ea81a31facf3ff8540acb06496fc412d2` | 191852 | re-run evidence |
| `results/fixtures/ref7_plus_32_new_coupled_L4.json` | `16701e0f775118f2e4a19ab7866355372250fd9a08c4da99d0b615dc8e943922` | 1087510 | re-run evidence |
| `results/fixtures/ref_Q1_L4.json` | `95c9f986d361a975583236489568de80a82dfce2f1257f199c8c6d8306aeccc5` | 1048427 | re-run evidence |
| `results/fixtures/ref_Q7_L4.json` | `4a48f810ef5d502a77cb9df7ed798b73ab6e1f5b2a0e3d3cb8b05d97dbadc921` | 1052584 | re-run evidence |

## STAGE 0.2 (frozen Tue Nov 10 09:25:38 UTC 2026, `date -u`) — CURRENT snapshot
Contents: 0.2a (the generic reversor building blocks requested at 09:14) plus three review items.
- R1, architect, ONE Q enforced. `Block.Q` and `Tensor.Q` record the Q a block or tensor was built with.
  `compose` raises when blocks declare different Q. `Engine` and `prepare.vacuum_state` raise when a declared Q
  differs from the one they are given.
- R2, architect, field signs. A field sign −1 requires `GearType.sign_why`. The reciprocity report lists every
  s = −1 gear with its justification.
- R-M2 theorem. `rhoL0` is the per-gear L0 mirror (b, a, 4Q + 2(r mod 2Q) − r); it fixes 2Q. The opt-in validator
  `compose/Tensor(..., q_lattice=patterns)` and `Tensor.q_lattice_violations` check the condition. T0.15 shows that
  rhoL0 on L0 together with R′ on the new layers is an exact reversor fixing the joint vacuum.

Files changed vs 0.1:
- `core/engine.py`: the ONE-Q assertion in `Engine.__init__` only.
- `core/tensor.py`: Q, sign_why, q_lattice.
- `core/reciprocity.py`: lists s = −1 gears.
- `core/reversors.py`: new, with rhoL0.
- `core/__init__.py`, `layers/reference.py`, `prepare/__init__.py`.
- Tests: `tests/randgen.py` (records Q), `tests/test_layers.py` (T0.8(g) now gives a justification),
  `tests/test_stage02.py`, `tests/test_stage02_review.py`.
- README, NOTES.

The forward step, the staged inverse and the clicks are unchanged. The fixtures reproduce 6/6 (82 per-update
hashes).

Last full run on this snapshot: 27 tests, OK, 25.7 s (09:24:21-09:24:47 UTC).

Test command and hash check (from the repository root):
```bash
OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers research.metric_variant_v1.tests.test_stage01 research.metric_variant_v1.tests.test_stage02 research.metric_variant_v1.tests.test_stage02_review -v
cd research/metric_variant_v1 && sed -n '/^## STAGE 0.2 (frozen/,$p' STAGE0_MANIFEST.md | sed -n 's/^| `\([^`]*\)` | `\([0-9a-f]*\)` .*/\2  \1/p' | sha256sum -c
```

Scope: only the stage-0 files listed below. Stage-1 builders now write their own files into this package
(e.g. `NOTES_gravity.md`, `demos/`, `layers/gravity.py`); those are NOT part of the stage-0 snapshot. A first
draft of this section (09:25:17) had swept in `NOTES_gravity.md` by a directory walk; it was regenerated from an
explicit stage-0 file list before being announced.

| file | sha256 | bytes | vs 0.1 |
|---|---|---|---|
| `README.md` | `ce76a12188225d01e6f0b77c5c470b7848c017c923d685ea4c060dbd0ca6b885` | 21620 | CHANGED |
| `NOTES.md` | `fcb588d6b85bd602c84a16adda6cbcf15b393ba53838c85e8d48442b59065d61` | 30325 | CHANGED |
| `__init__.py` | `a8ccfe8280b870aa07819af6195af9a3c0d37b2f62fe5ceced0b5265dba665aa` | 243 | unchanged |
| `core/__init__.py` | `a4ff8d441d1e96c28d691d583f9161804a29a02ae8b725888823a05002ec023c` | 1531 | CHANGED |
| `core/bridge.py` | `375e227db404e86895210e66597f9fdd5557d0193c48b6f62148f525854edaa8` | 1764 | unchanged |
| `core/engine.py` | `9dc8f53db4c8c91c2226fb7ebc4139bf103ecebbedb621adf17dc22e327a6dc9` | 19319 | CHANGED |
| `core/lattice.py` | `10cde9089e48d314b39d771d5a0f6213b415fac7b8a637b8e105f216a046f483` | 4013 | unchanged |
| `core/reciprocity.py` | `f453375844c8b518c8c40961fbbb91a30fc9d723d72c031f0951127e7c95b57a` | 5521 | CHANGED |
| `core/reversors.py` | `858797b3b076ad1937cc8382ef0ff09cbf659976d3674c84141f4bf101b78a45` | 12934 | new |
| `core/tensor.py` | `ebb01379168b64eb277caeedce47a3b03c16ebaa19b0863ae0721ab3f6c7327b` | 25785 | CHANGED |
| `layers/__init__.py` | `8fc22775814533b2b1273a239b66b4e3a5c52439f1e9dd2be995ec7351df3c5b` | 1816 | unchanged |
| `layers/reference.py` | `6d1d89a2362628102a485817f0d2191c822d8ca864bfb4975a5690940fc61e25` | 1232 | CHANGED |
| `prepare/__init__.py` | `6f174e48f2262e977a6ff05d4b3e2f3efcf1d2e8a6d3e4960622d17ac962433d` | 2487 | CHANGED |
| `observe/__init__.py` | `79e5c1367f6209576123f91f69024b366add002032b50cbe26c009bfb2ef1af0` | 765 | unchanged |
| `observe/audit.py` | `e9fd04c2f3b0f8af7bd34fbdb354f283770dfb9fa7208f83f2599ed838d0b54d` | 2178 | unchanged |
| `tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | unchanged |
| `tests/randgen.py` | `515a20c2bcb0425fdc2faf3cf80d1d61cd70302ac19e66e60530fc9dd1129316` | 7663 | CHANGED |
| `tests/test_core.py` | `19d825fac2dcd57c551552e5a2a586c4b3049f54fc4af8d227dea966f78490ff` | 21739 | unchanged |
| `tests/test_layers.py` | `fa0adce1a66fad9d32e8033328c070752c71e02210b74a8d8d9394ea45629185` | 9937 | CHANGED |
| `tests/test_stage01.py` | `faef096884822c1bbd6a1bc229729619833e060777fa19d056dcee2136e07171` | 7494 | unchanged |
| `tests/test_stage02.py` | `94c6cf73d5b64a4ecf551953ffcaa904642c6ca0e7ecfc738241eefc2270d150` | 12760 | new |
| `tests/test_stage02_review.py` | `4e1b4d83c232e9d5aeda6adcd5653086097407ef350a5f9795527d7b57beb4c6` | 8843 | new |
| `tools/export_fixtures.py` | `10599c6834e39854a1178f44101ce260900b7050001105b403f72719fadab376` | 4281 | unchanged |
| `results/T0.1.json` | `efcf7e72c96b408032bffd6be2bccc0edfc967ff1700eecaecd25b8030c4dd4c` | 1844 | re-run evidence |
| `results/T0.10.json` | `92fa4f55b46ed9ec4d67c7e09baeede5c74c391bc70e4a5f31ad2d5e5a702061` | 569 | re-run evidence |
| `results/T0.11.json` | `7c639b87bb33c5d5567996e84b3d09d9691b9c5071911d000ee6766c272fd06d` | 1021 | re-run evidence |
| `results/T0.12.json` | `2af3dd798bf4ae2cbb037397e2952d1bc482d52ae5e39da74026c441ec62b01a` | 368 | re-run evidence |
| `results/T0.13_1_involutions.json` | `198b2f766ed6e75019cfde36af7f3176cbaf450e2b588f98e67a11cbef16821a` | 1833 | new |
| `results/T0.13_2_Mp_vs_time_reverse.json` | `48b1a307051b63ccebcd2c659d4ae173fe7131fa5e7ee52d72e03cd0be4c80bf` | 120 | new |
| `results/T0.13_3_reference_reversors.json` | `bb3e7d9b20ba36c4651321eca24d221a283f7031c4dafa55e7c3b32c6ff5e944` | 1614 | new |
| `results/T0.13_4_reference_inversion.json` | `746da2ab304fe7f19130c48fe718d2ebe0cc8d77dca6550ea4ca60ccba6ea54d` | 568 | new |
| `results/T0.13_5_link_rebasing.json` | `6bd9a6dc63f9c582f3ce135247440992a77edba2a7477d4bb5e0123249dc635d` | 323 | new |
| `results/T0.13_6_central.json` | `d344ffeb2ea7f661f18acfefb84cb8df21c14ef58bf7ccdd168a3b123b99482e` | 569 | new |
| `results/T0.13_7_is_fixed.json` | `39073516f580aa38de50af5d62a952263c5e122e21cf12af5f3509bd7791996e` | 142 | new |
| `results/T0.14a.json` | `907a11e9b944d76dc3f94b2b7bc2760c5f97202d6b0c86fc4404d1a71db5b372` | 255 | new |
| `results/T0.14b.json` | `e0e161618b11da435c67fce8415c2656d98b7169979fbbcd30f0b336dc5c3fc0` | 262 | new |
| `results/T0.15a.json` | `97f14ce5e1c37cb35f6170025e63170ae0c4ba75379de5787ef94bf3e632c8ef` | 384 | new |
| `results/T0.15b.json` | `39a438d30a60c43bf12591ddb6085e7d70317e4b5a35fb9a9050c4acb40b5497` | 1162 | new |
| `results/T0.1_fixed_point.json` | `de62af08aed0b321264583b7945d4aaedb4b793fc7ec35b1299ba544c7d87960` | 227 | re-run evidence |
| `results/T0.2.json` | `9c4f72dc86b11b1dfd30bc4304cf2ca390f1fec4c2d9d3e2ddf7e00ca1cc7efc` | 1283 | re-run evidence |
| `results/T0.3.json` | `8d62dcc5f21dcaed8f19d75c605382028382ead872bc9f65611827ec425a62b5` | 4759 | re-run evidence |
| `results/T0.3_extra.json` | `1225a500cca54a208fc8b0c5b757a256a7d78ebbf4f2e2dde6adbc9808c0de18` | 665 | re-run evidence |
| `results/T0.4.json` | `08b80e29a6b10c5f838ec10eadf9b46c825fde54ccefc42d49749b3dde6c8971` | 777 | re-run evidence |
| `results/T0.5.json` | `ff3c44b828d42cab2285f0747db97665ca45f52f92cb3da8c99991e79026c276` | 1829 | re-run evidence |
| `results/T0.6a.json` | `55c69e9e1d28a7e964ca46eabb59feee2311633a6c00e29ca3106dde030e94f4` | 249 | re-run evidence |
| `results/T0.6b.json` | `3e6a25b294a983044d49e0b3f06f1df695b96600d6d6f15715bc105d12fe0f1a` | 295 | re-run evidence |
| `results/T0.7.json` | `e4d95c254ad21cbb41c3f9bd5d772936049efa05d08e9a9166abdb3b3d8d3c3f` | 561 | re-run evidence |
| `results/T0.8.json` | `54cf1352ca9ec57130e1845b4e4660746d978263f80ba557da74670f32b65b28` | 1303 | re-run evidence |
| `results/T0.9.json` | `0cbb92c6ea1157a0a72456636e46e6fb296241e0c0d69e328e4f3592a0714c10` | 177 | re-run evidence |
| `results/fixtures/INDEX.json` | `1e704c21d350fb3d97b4a5e49103ed7a4173ee8974ed355143422c0f046a3886` | 1692 | re-run evidence |
| `results/fixtures/cubic_Q1_bigint_seed32_L4.json` | `41bda8e4b111ead669a9d84c30b3fc96a75250306ace18d7ee2d77245e8e8166` | 303516 | re-run evidence |
| `results/fixtures/rand_a_reads_seed11_L4.json` | `642ddaad5174e07c57195c948300887a9d821304c1e849ed7ac6c704fd042bd4` | 162085 | re-run evidence |
| `results/fixtures/rand_b_only_seed10_L4.json` | `3338648cb40282aa9896e95dc44472ec8f16816df95dc0afe35199736d866f28` | 191948 | re-run evidence |
| `results/fixtures/ref7_plus_32_new_coupled_L4.json` | `55560ae4b77cff00563a8f697bfd568cef36406b401db68cba28406f7155168d` | 1088636 | re-run evidence |
| `results/fixtures/ref_Q1_L4.json` | `e6c340f32a3b6ddd555a3582e4cdc422004a1210d45207d4ad5194a5ae8f9758` | 1049105 | re-run evidence |
| `results/fixtures/ref_Q7_L4.json` | `55d886848c281290d939f24251fddb83fba0a06b403f3ac58be3c94c205b1533` | 1053262 | re-run evidence |
