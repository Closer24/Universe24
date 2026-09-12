"""Native event schema discriminates causal, pure and mixed register contracts."""

from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator, ValidationError

from event_universe.schemas import schema_document

IDENTITY = [[1, 0], [0, 1]]


def validate(program):
    Draft202012Validator(schema_document("native-events")).validate(program)


@pytest.mark.parametrize("model", ["local-quantum-events-v1", "local-quantum-events-v2"])
def test_native_complex_coefficients_and_outcome_code_arity(model):
    program = {
        "model": model,
        "capacity": 100,
        "addresses": [[0, 0, 0]],
        "layers": [{"tick": 1, "operations": [{"sites": [0], "matrix": [[[0, 1], 0], [0, 1]]}]}],
        "bindings": [
            {
                "address": [0, 0, 0],
                "types": ["record"],
                "field": "outcome",
                "instrument": [IDENTITY],
                "codes": [7],
            }
        ],
    }
    validate(program)
    program["bindings"][0]["codes"].append(8)
    with pytest.raises(ValidationError):
        validate(program)


def test_v2_channels_grouped_instruments_and_shared_register_addresses():
    program = {
        "model": "local-quantum-events-v2",
        "capacity": 100,
        "addresses": [[0, 0, 0], [0, 0, 0]],
        "register_names": ["a", "b"],
        "dimensions": [2, 2],
        "initial_levels": [0, 1],
        "layers": [{"tick": 1, "operations": [{"sites": [0], "channel": [IDENTITY]}]}],
        "bindings": [
            {
                "address": [0, 0, 0],
                "types": ["record"],
                "field": "outcome",
                "site": 0,
                "grouped_instrument": [[IDENTITY]],
                "codes": [1],
            }
        ],
    }
    validate(program)
    malformed = deepcopy(program)
    del malformed["register_names"]
    with pytest.raises(ValidationError):
        validate(malformed)
    malformed = deepcopy(program)
    malformed["model"] = "local-quantum-events-v1"
    with pytest.raises(ValidationError):
        validate(malformed)


@pytest.mark.parametrize(
    "matrix", [[], [[1, 0]], [[1, 0], [0]], [[1, True], [0, 1]], [[[1, 0, 0], 0], [0, 1]]]
)
def test_malformed_matrix_shapes_are_rejected(matrix):
    with pytest.raises(ValidationError):
        validate(
            {
                "model": "local-quantum-events-v1",
                "capacity": 100,
                "addresses": [[0, 0, 0]],
                "layers": [{"tick": 1, "operations": [{"sites": [0], "matrix": matrix}]}],
            }
        )


def test_causal_schema_does_not_accept_quantum_payloads_or_unknown_keys():
    validate({"model": "causal-events-v1", "capacity": 8})
    with pytest.raises(ValidationError):
        validate({"model": "causal-events-v1", "capacity": 8, "addresses": []})
