#!/bin/bash
cd /tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad/wt_ec
export PYTHONPATH=src
PY=/home/user/Universe24/.venv/bin/python
echo "== gate $(date -u +%H:%M:%S)"
$PY -m pytest -q -p no:cacheprovider tests/test_board_properties.py tests/test_node_clock.py tests/test_emitter.py tests/test_flux_reading.py tests/test_detector_law.py tests/test_detector_law_tables.py tests/test_receiver_by_name.py tests/test_massive_record.py tests/test_body_conditions.py tests/test_preflight_worlds.py tests/test_initial_state.py tests/test_run_inputs.py tests/test_extents_and_face_slab.py tests/test_repository_language.py tests/test_repository_hygiene.py tests/test_charge.py tests/test_board_reversible.py tests/test_dark_body.py tests/test_seated_detector.py tests/test_support_box.py tests/test_weak_field_rule.py tests/test_toward_nature.py tests/test_body_record.py tests/test_hop_taking.py tests/test_point_emitter.py tests/test_engine_start.py tests/test_families_file.py tests/test_vector_holds.py tests/test_axis_paces.py > /tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad/proper/pytest_full.log 2>&1
tail -40 /tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad/proper/pytest_full.log
echo "== ruff"; /home/user/Universe24/.venv/bin/ruff check . 2>&1 | tail -3; /home/user/Universe24/.venv/bin/ruff format --check . 2>&1 | tail -3
echo "== mypy"; /home/user/Universe24/.venv/bin/mypy src/event_universe/events/world.py src/event_universe/events/detector_law.py src/event_universe/events/rule.py src/event_universe/diagnostics/massive_record_margin.py 2>&1 | tail -2
echo "== done $(date -u +%H:%M:%S)"
