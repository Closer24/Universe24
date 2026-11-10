# STAGE 1 MANIFEST (rolling, manager-announced sections only)

## STAGE 1-GAUGE (frozen Tue Nov 10 10:34:25 UTC 2026, `date -u`) — rolling stage-1 snapshot, layer: gauge (SU(2), SU(3), compact U(1), c2 default OFF, c1 exploratory)
- Core = STAGE 0.2 (its 23 code/doc/test rows verified unchanged at this freeze). Builder: B1-GAUGE (final 09:58).
- Builder suite at freeze: `OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_gauge` → 10 tests OK (2 skipped = long arms, run with GAUGE_LONG=1), 16.3 s (manager run 10:33:59–10:34:16).
- Other builders import `layers/gauge.py` read-only (B1-EM compact U(1)); no edits to these files without a new announced section.

| file | sha256 | bytes |
|---|---|---|
| `layers/gauge.py` | `9fbce17969759d789f56c4a295028131789a06f0819a89658cd2c679effab635` | 22685 |
| `layers/links.py` | `e5533b65f2d54fb3f6f6c65a812a5f1c41f260cdbb04eae9d568b1c89a6d94f9` | 11345 |
| `observe/gauge.py` | `4182a52d5f926117df816b9e32f7a2045b9780281eb73391f82523b5fa03b01a` | 22132 |
| `prepare/gauge.py` | `ddd4ca42d2c65de3359b5e863718c86d72899df646fde13e1c140807e3d4b326` | 4311 |
| `tests/test_gauge.py` | `78f47be24e4f7e480142b77a281c24ba478ee087edd5288a8329aa5f838450d2` | 25807 |
| `NOTES_gauge.md` | `8561425d495ee8231caf439d8922b026e8595fa930543a5ebf448d4fcf03cc3a` | 40339 |
| `demos/gauge/C1_stability.json` | `6cdf93c1670249ab1602978d2d4ecc1a7c417294c3b9504be52151690839e416` | 11351 |
| `demos/gauge/D1.json` | `dabee1ea6a5d524f35d184584d2ebcde134beafb23bc857ca90280d37da58be1` | 6906 |
| `demos/gauge/D2.json` | `5cccf1af8aa197c654ec5007ae88e09ac6134b308d0c749b3760715b33b30206` | 7501 |
| `demos/gauge/D3.json` | `959bddc0aef3aa7d1818d2ec2346a1468906dc8f6b19cc9c87c66a7b450286de` | 958 |
| `demos/gauge/G9_c2_stability.json` | `bea00309c785409a670004cfc389a2c96c23d2cfc7202d99a046574ac9a318bd` | 20058 |
| `demos/gauge/G9b_C1b_G9c_strong.json` | `a048b068f024b4f8419dd83050e82c034201f2c43e1b75f12c36e877922ac67d` | 6205 |
| `demos/gauge/M1_mechanism.json` | `b85bb3a0f3ab2f871c0c9acedde79112e4dede58442d53821c4e5b3d6bd54bf4` | 15120 |
| `demos/gauge/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `demos/gauge/c2_mechanism.py` | `494711348c919025d9c97223d10c44e40d3e7cf5b57fedb76241b83e20e4ba6a` | 5525 |
| `demos/gauge/links_stability.py` | `35343152f2afac0b847fcd3b1d1ec1b21ee0742d26281485c106f0248a250781` | 8004 |
| `demos/gauge/run_demos.py` | `af409e2f95fa7f0da1784c6a80aa6661273fe7943fa68f7c5ba3d8584efeed56` | 10925 |
| `demos/gauge/spring_select.py` | `0af264b50d4870f98cf50ebcd5868d974b1bbc41d577c8c4cf493087eb53e63c` | 5899 |
| `results/gauge/G1.json` | `cd73c805d017a7c20b70fae40eea4f9dc8c25108903122f304253bb69b0f5dd9` | 12257 |
| `results/gauge/G10.json` | `8a318dd81e05d398f713f67cf57676fc5a562eedcde2b3754c0763d47ddb36a7` | 968 |
| `results/gauge/G2.json` | `80b1ec1a3b8d80b8d7e17822e19a855b12ff354a7ab722a5506243d62a159747` | 324 |
| `results/gauge/G3.json` | `76b35564ccec1984db14e4b340ba939650f0d6b161b49bc2be52398744ad918d` | 2668 |
| `results/gauge/G4.json` | `d82e0472b7728c66f8368c73eae87b0dd14185c005516c19a70a9abc263a8814` | 978 |
| `results/gauge/G5.json` | `d0c4199404069e7db6a5db42fc8bb6bf5c10027bffef0f7c646b23a73c11d7e0` | 628 |
| `results/gauge/G6.json` | `0e86b1463559781aaeab2c85744eae98aa378ed6bc051558903a75fa5b6314d3` | 4004 |
| `results/gauge/G6b.json` | `fdc0569f855ca49376490b4cb743b9114043edeaae1625a8c8b9338995e71f27` | 15596 |
| `results/gauge/G7.json` | `4d49f2027dec463508bb994510824a85ecabfe3f6703e816b08e794b63083f47` | 1708 |
| `results/gauge/G8.json` | `f243d7a0afc413a0089e03fafa2a69fc31556859b6403fa33eb75a0077b90c90` | 724 |
| `results/gauge/S1_spring_default.json` | `04d493e98825b25c5bcc893ed3849163fa35b3dfb0031b869d00311b8ef21a8a` | 15544 |
| `results/gauge/S2_default_family_Q2p29.json` | `ee561eb48ea9b8bf9194a5d65cfcbfb5ebbd45db8b807323bd63a17ba092a1ff` | 1676 |
| `results/gauge/census.json` | `f0892a5af82ac048bfd6c1b14770ef8655cc4a9d9bf1b84164d85a4411a7c27c` | 8059 |

## STAGE 1-EM (frozen Tue Nov 10 10:38:02 UTC 2026, `date -u`) — rolling stage-1 snapshot
- Builder: B1-EM (FREEZE-READY 10:36). Matter (16-ch Dirac pair, Wilson parameter) + E1 (designated cross terms, documented variant) + compact-U(1) route (EM-C1–C3).
- Builder-declared sha256 of the 9 code files verified by the manager (0 mismatches). Builder run: 13/13 OK (10:06:45–10:06:50). Suite: `OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_em research.metric_variant_v1.tests.test_em_compact -v`.
- Status at freeze: compact route EM-C1 dressed Gauss 0 failures, C2 0 designations, C3 rewind + M′ exact, C4 Coulomb signs PASS; C5 Newton III FAIL (−0.50; early window −0.96); C6 no link wave in the gauge regime FAIL → compact U(1) NOT yet the EM block (owner approval ז was conditional); E1 remains the working EM.
- NOTES_em.md still open (docs; hashed at the final freeze). New work only in new files.

| file | sha256 | bytes |
|---|---|---|
| `layers/matter.py` | `078f38405fa67d1d0b2cb22d229d8ff725b9dfbb89bdf7ce320d0f6e9e25e1a2` | 16676 |
| `layers/em.py` | `9c13b9b87ca4563741e5bb70a93d976659185aaf3247645b159a9abfdea94b6b` | 16846 |
| `prepare/em.py` | `5aff316e01aeb43ddfd4c16cb24ef13d37c690c23fe9e4be9c50e2efdb379b48` | 13030 |
| `observe/em.py` | `fc2c1932b8f377fa8a5adee1946fdea917d691a11f7c7c95a4732b6cdbb04c29` | 9548 |
| `tests/test_em.py` | `2ea623ab9d9fe19d43dd1c39708dcfdaed2da836f6c1ea4b991fc9f7765f042f` | 28663 |
| `layers/em_compact.py` | `c7ce8d5db79672bd235edc0b07a598961c21f1bc23ad67d8870fb1111f7ff0f2` | 6606 |
| `prepare/em_compact.py` | `f5ca257ad0b0000328f10a044fe247f6f8b39eeaacb15f989c113d8303b33331` | 2429 |
| `observe/em_compact.py` | `c51b1b86317ad92f4df6755f1d0f4b50a54e807a1aa8b57813fc8ca325a2f104` | 4676 |
| `tests/test_em_compact.py` | `3210834d261898350ee5e614b81747b721cbac7f6820d21a2f76b8b18626a2f3` | 5045 |
| `demos/em/census.py` | `180f6c8bfc6c523fd7c08a3814fd251eb65080e9380d0a9a080b16ff53289bcc` | 2896 |
| `demos/em/compact_coulomb.py` | `6ba86387cbb0047eeac5ff35e8a4a9db1dcd0928979a384677825f962bc9dd75` | 4958 |
| `demos/em/compact_force.py` | `66f8fc5c08e65f9e564418a09e0b63b473226ddfaf54ed0ccfed66d60f4655ae` | 2589 |
| `demos/em/compact_wave.py` | `41aa61e3e63cfb5c73299eedc0383f092697b4fe8bb989928f7f0140023afd9e` | 3836 |
| `demos/em/coulomb.py` | `4cc2e6e2d3a6d5758517e3ecee632410eb48e9d39946ba7124b7c8c4679d3d51` | 5570 |
| `demos/em/dipole.py` | `f626439dc10a9829b0dd3df7b1c0f3c40235f6494b1217db49fbddfd8e4d9b52` | 6943 |
| `demos/em/emlib.py` | `7f920cf5246caec4102bfdcbd59e8160b9bbaac6edfcd1bbb4e10a3a6d06b51e` | 3431 |
| `demos/em/magnet.py` | `49991634e3457aacd3d6296a731f86465436af172a763fb547664a685fdb25d9` | 5599 |
| `demos/em/n3_charge_weighted.py` | `291c20775a588be7e010bb50e06dd8f4ab2bd10999406396bc59a099aae5c267` | 1295 |
| `demos/em/noncircular.py` | `d93b5acacee53185654cc4e3bc6858541b4a14365225a54ebb81db67b188ffdf` | 3975 |
| `demos/em/qclick.py` | `1536dbc46dec918a3da3947b8157a8899ecc025780a2eaf9297f9c3802bb4d50` | 3447 |
| `demos/em/slope.py` | `845a9110a0b4973a08688a4a9d45f85bafec8c2bb82bfedd29040ad84c38cf51` | 5520 |
| `demos/em/twoforces.py` | `30ca9480f91d492b6e980446a53a6523a122a4640844b35b8f6168ba03c5f28f` | 4418 |
| `demos/em/results/EM-C4_compact_coulomb_++_r10_w2_2.0.json` | `257a6df02f0fd94708e7edafc44503fc241a46aeecb4ebf9731c55d4d85e31fb` | 3877 |
| `demos/em/results/EM-C4_compact_coulomb_++_r10_w2_2.0_symPOSTHOC.json` | `b473a199630a986fc7fcaae59e61443426923f5c2a00943b415d23e76d13cd81` | 4030 |
| `demos/em/results/EM-C4_compact_coulomb_+-_r8_w2_2.0.json` | `04c8cc9f219a1bc5e1504de612b096cd9b38fc59218493e8ec23db84706d1b55` | 4056 |
| `demos/em/results/EM-C4_compact_coulomb_+-_r8_w2_2.4.json` | `eb6a5da4a9b91ef3019ea47b9ce40903929c941c8dea016b99f59fdd97821dd6` | 4047 |
| `demos/em/results/EM-C6_compact_wave.json` | `2d3d39a522d58395deae60311902363ae4c54e3476c98c0aaaf653558be6735d` | 740 |
| `demos/em/results/EM-C6_compact_waveb_kP32768.json` | `cfff1a8453bab3c72e55b43a20c00d03e3ef6902bb2e7062d3efa2d6d3b00095` | 882 |
| `demos/em/results/EM-C8_compact_force_POSTHOC.json` | `faba54efd5ca1347ad1e63e80e91accd1ee2f034dca21a1d0ce35dd8a33097ff` | 840 |
| `demos/em/results/EM-D1_coulomb_++_r12_T150.json` | `1938768d9e2b26dd51ab494fac7ae9f9e3acf004b653269db1c07ec18d37f522` | 7664 |
| `demos/em/results/EM-D1_coulomb_++_r8_T150.json` | `b17bdcc10fc9f5d664726b0cfba680fd4485efda5ec9bf306e59a2de432a6048` | 7607 |
| `demos/em/results/EM-D1_coulomb_+-_r10_T150.json` | `a577195e783622c5b97a3e64ba3c537f9313b2e288b812664e9dddb37b219da3` | 7772 |
| `demos/em/results/EM-D1_coulomb_+-_r12_T150.json` | `94cc7c7ad76a32de65a48f5af7beabaefbf503d953c23c619cdb4b6490ca6627` | 7753 |
| `demos/em/results/EM-D1_coulomb_+-_r6_T150.json` | `8c3cd5259962791687e02857b5e59315a07f3b4f271bf09b96ed65cf1342169d` | 7882 |
| `demos/em/results/EM-D1_coulomb_+-_r8_T150.json` | `8d8a2441c41eecf372673a4b9956f1818b5d194c0cde86adb3b5a5fc5b97ac57` | 7884 |
| `demos/em/results/EM-D1_coulomb_+-_r8_T150_blind2.json` | `ce518aac7166c008aa144882f04207a07690b5f2d149deb09b7f0fec61daac01` | 7888 |
| `demos/em/results/EM-D1_coulomb_+-_r8_T150_rem_even.json` | `9f89bf463dfde8c48a3b9b047600255f85aebe55bdd8f32385d1462e22735326` | 7926 |
| `demos/em/results/EM-D1_coulomb_+-_r8_T150_w2_2.4.json` | `6efa49d9f4fb3e137c237b429a172bf5adc4b09b2bcba0169fd250caece996e3` | 7796 |
| `demos/em/results/EM-D1_coulomb_--_r8_T150.json` | `7ceb25db138e1af60babad5ed1cf4cb9bcb26d693d4781fcdd24b339cb037232` | 7608 |
| `demos/em/results/EM-D1b_newton3_charge_weighted_POSTHOC.json` | `d719761942cf6f5f0eb0b122fec7beb2d199fd39f163d9d636f913ecd4467e98` | 339 |
| `demos/em/results/EM-D2_slope.json` | `05916a71059955d6da9fbac6366a1b65682d53336b39dc5b1f503fac507be3ac` | 3546 |
| `demos/em/results/EM-D2_slope_POSTHOC_T120.json` | `ebe83fee6d553aa04b7e1298e7702abee847fe141a1f09b5bfa2e86f1e77682f` | 3561 |
| `demos/em/results/EM-D2_slope_REGISTERED_run1.json` | `05916a71059955d6da9fbac6366a1b65682d53336b39dc5b1f503fac507be3ac` | 3546 |
| `demos/em/results/EM-D3_noncircular.json` | `3064c2632fa77b8851e89709cf3890fb52eb99da042c64f3872dfc12e9630fd2` | 14347 |
| `demos/em/results/EM-D4_dipole_y_Q1025_L48.json` | `c53203ea6d460619c15bf97d46fab79afe19397302b003ead797478594d5fe09` | 1565 |
| `demos/em/results/EM-D4_dipole_y_Q1025_L48_REGISTERED_run1.json` | `c53203ea6d460619c15bf97d46fab79afe19397302b003ead797478594d5fe09` | 1565 |
| `demos/em/results/EM-D4_dipole_z_Q1025_L48.json` | `85663c597d58ba98f616e54d3fcaaaa83a9f25608b8a191f27e1b4306897d044` | 1861 |
| `demos/em/results/EM-D4_dipole_z_Q1025_L48_REGISTERED_run1.json` | `cbcf02d896b2401856fd3bc8fdddc0ac7151a63a1478368df1fb0a365d06e096` | 1565 |
| `demos/em/results/EM-D4_dipole_z_Q5_L32.json` | `0c20513798a2fb85944db96c6eae535bdcdaf9d076cba5a16597586c829e6137` | 1373 |
| `demos/em/results/EM-D4_dipole_z_Q5_L32_REGISTERED_run1.json` | `0c20513798a2fb85944db96c6eae535bdcdaf9d076cba5a16597586c829e6137` | 1373 |
| `demos/em/results/EM-D4_dipole_z_Q5_L48.json` | `75a904e60e4e0ef3ec8a9068730c7506e3ad76ec40de476bab5bf3ce1c43ef57` | 1831 |
| `demos/em/results/EM-D5_magnet.json` | `1c3ff27728f59c241710d016511c3e932695e733621a988b8f0787f1b659662d` | 3489 |
| `demos/em/results/EM-D6_qclick.json` | `050dc14e14e52110909f9d97f8eae962b521f7b7630bae3b69b5aeae5ec5b1ca` | 820 |
| `demos/em/results/EM-D7_twoforces.json` | `c4c30c4a3ce9dfe97876dc4c6e49358327d539deda7788d2bd692be42861a730` | 1606 |
| `demos/em/results/EM-census.json` | `968c8a8e14954abb7c562a6739d1470f08e2dbebf4fac1ac0093c65ae287aabb` | 3553 |
| `results/EM-C1_C3.json` | `b018f475647915330d2a069faa0c3fcf7de574a5c3facd7e0d8e1f98ed30df44` | 1010 |
| `results/EM-C2.json` | `805960cbe27497903e20a8f4dae9d5f6778a949d11e15d503c8f39ac90f3352c` | 703 |
| `results/EM-T1.json` | `8be23f10e7e6be9e6915416699e2a3aab9e7d6219ef0309089e12e4aaf68c33d` | 625 |
| `results/EM-T10.json` | `f5cbd49614146789fbc54c0e7730cbe0b146523b34d3a15ea15160c8a41d16b0` | 375 |
| `results/EM-T2.json` | `b3fed4c0eed249baff59680ca9303f7e54a8941fa540354e97ef51a56b94d94a` | 763 |
| `results/EM-T3.json` | `3bdb84d435b664db58c24652a0515d617d6b318c78e93c4cb47ffd5f13d406e6` | 1933 |
| `results/EM-T4.json` | `d3e4550234168cadfa5f51e9b4b10ea51d55e760c7a219a84116028bf35f3644` | 337 |
| `results/EM-T5a_T6.json` | `0dd8de122adfab4babb874139ef23ab48719d3625b53362329df7dcc487ac247` | 1251 |
| `results/EM-T5b.json` | `3d47da2296e62d4b75f849e885d26d7c09bf268c792c18b8b96595e03dbcd6e2` | 256 |
| `results/EM-T5c.json` | `c87e392baaae5a2fd738a9d250ccc86958774ba444f78f7d8a0ced3e9d6d8cb2` | 232 |
| `results/EM-T7.json` | `9c25db77a9f31daaf9ec8b4b70c13de71cb724fcc51feefa91cad1ae43d057a9` | 2071 |
| `results/EM-T8.json` | `ddbef5619f68709a95e01504b4cd50a693843a45acc8288e3e1b83c39e61335c` | 175 |
| `results/EM-T9.json` | `882e1566e0b9cf44eaf7931c524dfdd3d55c0cb5c041715892d0b880f00b359e` | 824 |

## STAGE 1-GRAV (frozen Tue Nov 10 10:38:02 UTC 2026, `date -u`) — rolling stage-1 snapshot
- Builder: B1-GRAV (FREEZE-READY 10:36:24). Metric (10 h̄ gears), universal lapse, β default = agreed ONE-WAY G (designated), β rank-4 (unavailable at Q = 2^29+1), N-design (not in default), OD2 accumulators + staggered reversor.
- Builder-declared sha256 of the 4 code files verified (0 mismatches). Manager run 10:37:41: 11 tests OK (G1–G10 + G5b) in 7.7 s. Suite: `OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_gravity -v`.
- Integer constraints: Dirac mass/Wilson/hop entries ∈ 2^22·Z (4P·Z), second-order ∈ 2^21·Z, OD2 H·g00 divisible by P. Headroom 1/(3Q) (F1): 'gravity only slows' remedy under test (new files).
- NOTES_gravity.md, demos/gravity/ and new results still open (new files only).

| file | sha256 | bytes |
|---|---|---|
| `layers/gravity.py` | `d75f48026915577316c4030766d0fa8aaac425c88a26d8fa33a43bc7d5b6d39e` | 42941 |
| `prepare/gravity.py` | `3dc98696fbe85a8000ff618cf9f73977941f5e6a46f4bdee375f2a9decdab805` | 8056 |
| `observe/gravity.py` | `dd18de66d9981ff229eb5d18fa059bbccb990460ba3ed016e364431b53535f77` | 13692 |
| `tests/test_gravity.py` | `097c82052ee23575beaf97c2b25d77560187939ff12953d74b2bc86ce9b06dbf` | 27463 |
| `results/gravity/G1.json` | `d42f21043b21282a4e8ec0133e3fc15c4f5d0a12b3ec9ca6de85c7774b6cf2a2` | 1580 |
| `results/gravity/G10.json` | `26902a659f6be320ecb230c676e9d6b313f94cd70936c363a1aafae2184d5dbb` | 592 |
| `results/gravity/G2.json` | `7768e70faad2e388d28d6199746f7abf5a8fe85a6279d85734c99a220a47b432` | 4216 |
| `results/gravity/G3.json` | `c43e8778403d84788cca5287c882859542e91fa2467291fe738e7dde4511db41` | 2452 |
| `results/gravity/G4.json` | `9e49ff2d34641f35836eb135c399d7764444fe35636de72501a0d1e3ebbb2f1f` | 4910 |
| `results/gravity/G5.json` | `c54236494d3eb4332b8a01a9576fe299b76905fef7ddcc7d3b1372a41823b089` | 389 |
| `results/gravity/G5b.json` | `9fb80f2477646e120d9ba9bb79cfb06a230ccee31220d43474916ce38e4b4a60` | 252 |
| `results/gravity/G6.json` | `c5420424370a4c71df0af7b5358a57d7ce40236dddc58bbf3a501adcc05ba660` | 223 |
| `results/gravity/G7.json` | `f2134607ebed71d7f437eea37f480f582a12a4198513e434c44c0511b703936a` | 501 |
| `results/gravity/G8.json` | `a14dcf0e7eaa9d89e8033c0f5fe802c1d1e4eb96656dc477235f0927f7093cb2` | 158 |
| `results/gravity/G9.json` | `030389926fc2f67314162910fca6226895bdd5d935a517726936295d03959cf7` | 1326 |

## STAGE 1-CHOICE (frozen Tue Nov 10 10:45:19 UTC 2026, `date -u`) — rolling stage-1 snapshot
- Builder: B1-CHOICE (FREEZE-READY 10:44:39). Builder suite on these files: 19 tests OK (1 expected failure = TC.15 record), 607 s, 10:34:17–10:44:24. Suite: `OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_choice -v`.
- Builder-declared sha256 of 7 code files verified by the manager: mismatches = [].
- The C0-fibre F7 is in this set, labelled 'taxicab cone, MECHANISM TEST ONLY' (it realises the cone gap the owner did not adopt). The approved round-cone F7 is NOT finished (TC.17 probe: E = 0 through t_B = 8, gap max|S| ≤ 0.09, but E → cos not reached).
- Post-freeze NEW files (not in this section): layers/choice_oddq.py, tests/test_choice_oddq.py (TC.18 odd-Q router: at Q = 2^29+1, A = 1, P(none) = 1/(2^29+1) per one-shot readout). NOTES_choice.md still open.
- Integration notes: builders declare r0 = 0 (override Block.vacuum to 3Q−1 via dataclasses.replace); readers must be ONE-SHOT at odd Q; routers are rank-3 b-only DESIGNATED observers; no writes into ref.*.

| file | sha256 | bytes |
|---|---|---|
| `layers/choice.py` | `6e28fe434ab1f53fa6adde238eccf8d0b492f614db9ee7e914f8122914c0bf3b` | 27137 |
| `prepare/choice.py` | `bf36d3b1915086d749a6abe7660ed2852fcfc91b9ad919ec7133e1d2615d4c9c` | 3744 |
| `observe/choice.py` | `6b565d126e2b84cecc81b8be265ab264b69d6451b23f0fdbd5e34d6e7dcf7b7f` | 4325 |
| `tests/test_choice.py` | `25a822b264fbe58f9dcda43d23de3652bd32ee3e16ec6734c26d118e8f0146cc` | 18450 |
| `demos/choice/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `demos/choice/experiments.py` | `e22e989e9be1a3f739e109e47c9661801796d82ae121c54820d21ac4e4f8084f` | 67712 |
| `demos/choice/run_demos.py` | `20c858bcc35a1eea3eed5f1ccc02ad1fb1cf756b55c65473219a476eaeebacdb` | 5821 |
| `results/choice/TC.1.json` | `1e5ae9e29ed695c195386636d346a2c7d34ee0801e9cc1e0877f7e0c50618214` | 3041 |
| `results/choice/TC.10.json` | `e8a2c845af2a5400241cdc1ce44eca8b65494bd58fec41bea3c6031db64c09a0` | 9812 |
| `results/choice/TC.11.json` | `c3163d66bbfc9654b32f8b2e6f4ff9f950fbf9d41e3c3dd46b84c1919ea1813f` | 5042 |
| `results/choice/TC.11b.json` | `7e12bce57dde0a25974410ab783c53ff3713a1b2ea44671b8cfa0bf16c82f450` | 23922 |
| `results/choice/TC.12.json` | `f4039c780bd8498c014752ba14e8c896bb7c30bfa3e7110594396af333cc0f0b` | 578 |
| `results/choice/TC.13.json` | `6ddfed865d9a841fb41c228303e36b322f4d590ff084a27f9f134d79c7b87d18` | 5706 |
| `results/choice/TC.14.json` | `a2481326fb17220d95b1d6e4d5331b0d66a61d521a4ea219743125b1cc323e7a` | 5519 |
| `results/choice/TC.15.json` | `d07da5c03fc727d7ca4b79cceec03af0099ea98cad3be5a400eefe254de34925` | 4689 |
| `results/choice/TC.15_devrun_101201.json` | `fe7d2c0bd0b88d18461f111f5320057046a35939d837dc3f2772418c6e57f84b` | 1515 |
| `results/choice/TC.15b.json` | `cfcaeb82a8a772eda3b8d63f49d95e5f399e72403c735922e8a01e56133ff748` | 2841 |
| `results/choice/TC.16.json` | `a7f92b304f7a0535e4932ce2f9c8acc76153b354af40fe45f8426fb586ad2259` | 424 |
| `results/choice/TC.17.json` | `109286322852113a8285b950cc717a60083259a3c390e6b1633694371d3379d8` | 23951 |
| `results/choice/TC.18.json` | `d676193b95677800800b763ce28e4252988993d7d56ee6389435ff11af0c8e2f` | 1354 |
| `results/choice/TC.2.json` | `82190295953d023b48829dd1281f34a6bb1f391ac5dcc4191b6bd09c129f23ff` | 13421 |
| `results/choice/TC.3.json` | `260bb693360602fc066813fb99ee2e7768c7548b84c879383d7cd4673cb5005a` | 4585 |
| `results/choice/TC.4.json` | `87dffc1490cc1165d48530fcf84c252b178f826051b21a0a7ca3ac45ff7b18d2` | 4605 |
| `results/choice/TC.5.json` | `76066a72560d70e1b5838eb3fc11faf8a40afc1a0f079058582499254a6ab6aa` | 1470 |
| `results/choice/TC.6.json` | `8b47f27e61769a0bea82f0558aca9d19abc2c5aad163b1de34f7d62ed7f2688e` | 5493 |
| `results/choice/TC.7.json` | `a2a59928069aaeb991dca01f3f617152b3c9409be298135a99a0c40720aa527d` | 5191 |
| `results/choice/TC.8.json` | `27b70cdfae7c34900d25f83df15ca2725dfb0f93cefe37cbf2e61d53afcfe708` | 675 |
| `results/choice/TC.9.json` | `7dbe5dbfcc910c84ee9c4ed51c347b2aa701fcb94bf05b239f61959dd5b6a0b2` | 3313 |

