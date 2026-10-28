"""Sofer's gate tested on itself: every rule of scribe_scan.py meets a snippet that must trip it and a snippet that must not.

  venv314/bin/python tools/derivations/open_items/scribe_scan_selftest.py

Each case names the module the snippet stands in (a reader, the carry's home and a tests file are treated apart by the gate),
the source, and the hits by rule it must give; the exit status is 1 on the first case that parts from its count. Run it at
every change of the gate (SCRIBE-GATE-1.md): a rule that stops tripping would let a push through unseen.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("scribe_scan", HERE / "scribe_scan.py")
assert spec is not None and spec.loader is not None
gate = importlib.util.module_from_spec(spec)
sys.modules["scribe_scan"] = gate
spec.loader.exec_module(gate)

ENGINE = "new_engine/step.py"
CARRY = "core/acts.py"
READER = "run.py"
TESTS = "tests/test_step.py"
NEW_STEP = "tensor24/engine/step.py"
NEW_CARRY = "tensor24/engine/carry.py"
NEW_RECORD = "tensor24/record/schema.py"
NEW_RUNNER = "tensor24/runner/loop.py"
NEW_DECODER = "tensor24/decoder/rows.py"
NEW_READING = "tensor24/readings/wind.py"

CASES: list[tuple[str, str, str, dict[str, int]]] = [
    ("a for loop", ENGINE, "def f(a):\n    for x in a:\n        pass\n", {"LOOP": 1}),
    ("a while loop", ENGINE, "def f(a):\n    while a:\n        a = 0\n", {"LOOP": 1}),
    (
        "two comprehensions on one line",
        ENGINE,
        "def f(a):\n    return [x for x in a], {y for y in a}\n",
        {"LOOP": 2},
    ),
    ("map", ENGINE, "def f(a, g):\n    return map(g, a)\n", {"LOOP": 1}),
    ("filter", ENGINE, "def f(a, g):\n    return filter(g, a)\n", {"LOOP": 1}),
    (
        "reduce from functools",
        ENGINE,
        "import functools\n\n\ndef f(a, g):\n    return functools.reduce(g, a)\n",
        {"LOOP": 1},
    ),
    (
        "itertools.product",
        ENGINE,
        "import itertools\n\n\ndef f(a):\n    return itertools.product(a, a)\n",
        {"LOOP": 1},
    ),
    (
        "numpy's vectorize",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, g):\n    return np.vectorize(g)(a)\n",
        {"LOOP": 1},
    ),
    (
        "numpy's apply_along_axis",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, g):\n    return np.apply_along_axis(g, 0, a)\n",
        {"LOOP": 1},
    ),
    ("a function that calls itself", ENGINE, "def f(a):\n    return f(a) if a else a\n", {"LOOP": 1}),
    (
        "a method calling the module's function of its name",
        ENGINE,
        "class C:\n    def carry(self, a):\n        return carry(a)\n",
        {},
    ),
    (
        "numpy's prod and repeat",
        ENGINE,
        "import numpy as np\n\n\ndef f(a):\n    return np.prod(np.repeat(a, a))\n",
        {},
    ),
    ("the engine's own product function", ENGINE, "def f(a, product):\n    return product(a, a)\n", {}),
    ("a map in a reader", READER, "def f(a, g):\n    return map(g, a)\n", {}),
    ("a loop in a reader", READER, "def f(a):\n    for x in a:\n        pass\n", {}),
    ("a power", ENGINE, "def f(a):\n    return a ** a\n", {"OPERATION": 1}),
    ("a shift", ENGINE, "def f(a):\n    return a << a\n", {"OPERATION": 1}),
    ("an exclusive or", ENGINE, "def f(a, b):\n    return a ^ b\n", {"OPERATION": 1}),
    ("a floor division", ENGINE, "def f(a, b):\n    return a // b\n", {"OPERATION": 1}),
    ("a remainder", ENGINE, "def f(a, b):\n    return a % b\n", {"OPERATION": 1}),
    (
        "a floor division and a remainder in the carry's home",
        CARRY,
        "def f(a, b):\n    return a // b, a % b\n",
        {},
    ),
    ("divmod", ENGINE, "def f(a, b):\n    return divmod(a, b)\n", {"OPERATION": 1}),
    ("divmod in the carry's home", CARRY, "def f(a, b):\n    return divmod(a, b)\n", {}),
    (
        "numpy's remainder",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.remainder(a, b)\n",
        {"OPERATION": 1},
    ),
    (
        "numpy's mod",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.mod(a, b)\n",
        {"OPERATION": 1},
    ),
    (
        "numpy's floor_divide",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.floor_divide(a, b)\n",
        {"OPERATION": 1},
    ),
    (
        "operator's xor",
        ENGINE,
        "import operator\n\n\ndef f(a, b):\n    return operator.xor(a, b)\n",
        {"OPERATION": 1},
    ),
    (
        "the engine's own remainder function",
        ENGINE,
        "def f(a, b, remainder):\n    return remainder(a, b)\n",
        {},
    ),
    ("a raise", ENGINE, "def f(a):\n    raise ValueError(a)\n", {"REFUSE": 1}),
    ("a raise in a reader", READER, "def f(a):\n    raise ValueError(a)\n", {}),
    ("a minimum", ENGINE, "def f(a, b):\n    return min(a, b)\n", {"CLAMP": 1}),
    (
        "a maximum and an absolute value",
        ENGINE,
        "def f(a, b):\n    return max(a, abs(b))\n",
        {"CLAMP": 2},
    ),
    (
        "numpy's clip",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.clip(a, b, b)\n",
        {"CLAMP": 1},
    ),
    (
        "numpy's where",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.where(a, b, b)\n",
        {"CLAMP": 1},
    ),
    ("numpy's sign", ENGINE, "import numpy as np\n\n\ndef f(a):\n    return np.sign(a)\n", {"CLAMP": 1}),
    (
        "numpy's select",
        ENGINE,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.select(a, b)\n",
        {"CLAMP": 1},
    ),
    ("a clamp in a reader", READER, "def f(a, b):\n    return min(a, b)\n", {}),
    ("an ordering comparison", ENGINE, "def f(a, b):\n    return a < b\n", {"COMPARE": 1}),
    ("an if", ENGINE, "def f(a):\n    if a:\n        return a\n    return a\n", {"BRANCH": 1}),
    ("a conditional expression", ENGINE, "def f(a):\n    return a if a else a\n", {"BRANCH": 1}),
    (
        "an elif chain",
        ENGINE,
        "def f(a):\n    if a:\n        return a\n    elif a:\n        return a\n    return a\n",
        {"BRANCH": 2},
    ),
    (
        "a match",
        ENGINE,
        "def f(a):\n    match a:\n        case _:\n            return a\n",
        {"BRANCH": 1},
    ),
    (
        "a type-checking guard",
        ENGINE,
        "from typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    pass\n",
        {},
    ),
    ("a branch in a reader", READER, "def f(a):\n    if a:\n        return a\n    return a\n", {}),
    ("an equality", ENGINE, "def f(a, b):\n    return a == b\n", {}),
    ("a true division", ENGINE, "def f(a, b):\n    return a / b\n", {"FLOAT": 1}),
    ("a float literal", ENGINE, "X = 0.5\n", {"FLOAT": 1, "NUMBER": 0}),
    ("round", ENGINE, "def f(a):\n    return round(a)\n", {"FLOAT": 1}),
    ("a complex literal", ENGINE, "X = 1j\n", {"FLOAT": 1}),
    ("the complex type", ENGINE, "def f(a):\n    return complex(a)\n", {"FLOAT": 2}),
    ("a numpy complex dtype", ENGINE, "import numpy as np\n\nX = np.complex128\n", {"FLOAT": 1}),
    (
        "numpy's floor",
        ENGINE,
        "import numpy as np\n\n\ndef f(a):\n    return np.floor(a)\n",
        {"FLOAT": 1},
    ),
    ("a float import", ENGINE, "import math\n", {"IMPORT": 1}),
    ("a number beyond 0 and 1", ENGINE, "X = 5\n", {"NUMBER": 1}),
    ("0 and 1", ENGINE, "X = 0\nY = 1\n", {}),
    ("a constructor with no dtype", ENGINE, "import numpy as np\n\nX = np.zeros(1)\n", {"DTYPE": 1}),
    ("a cosine", ENGINE, "import numpy as np\n\n\ndef f(a):\n    return np.cos(a)\n", {"CIRCLE": 1}),
    ("a root", ENGINE, "def f(a, isqrt):\n    return isqrt(a)\n", {"ROOT": 1}),
    ("a circular name", ENGINE, "def cosine_count(a):\n    return a\n", {"WORD": 1}),
    ("a module-level container", ENGINE, "SEEN = {}\n", {"STATE": 1}),
    ("an id key", ENGINE, "def f(a, seen):\n    seen[id(a)] = a\n", {"STATE": 1}),
    ("a pinned number in a test", TESTS, "def test_f(f):\n    assert f() == 5\n", {"PIN": 1}),
    ("0 and 1 in a test", TESTS, "def test_f(f):\n    assert f() == 1\n    assert f() == 0\n", {}),
    (
        "a number outside an assert in a test",
        TESTS,
        "X = 7\n\n\ndef test_f(f):\n    assert f() == X\n",
        {},
    ),
    ("a loop in a test", TESTS, "def test_f(f):\n    for x in f():\n        assert x\n", {}),
    # the new engine's folders (Tensor24's section 31), each by its own rules
    ("the decoder imports numpy", NEW_DECODER, "import numpy as np\n", {"ISOLATE": 1}),
    (
        "the decoder imports the engine",
        NEW_DECODER,
        "from tensor24.engine import step\n",
        {"ISOLATE": 1},
    ),
    (
        "the decoder imports the engine, relative",
        NEW_DECODER,
        "from ..engine import step\n",
        {"ISOLATE": 1},
    ),
    (
        "the decoder imports the engine's package",
        NEW_DECODER,
        "from tensor24 import engine\n",
        {"ISOLATE": 1},
    ),
    ("the decoder imports the runner", NEW_DECODER, "import tensor24.runner.loop\n", {"ISOLATE": 1}),
    (
        "the decoder imports the current engine",
        NEW_DECODER,
        "from event_universe import clock\n",
        {"ISOLATE": 1},
    ),
    (
        "the decoder imports the standard library and the record",
        NEW_DECODER,
        "import json\nfrom tensor24.record import Row\n",
        {},
    ),
    (
        "the decoder imports the record, relative",
        NEW_DECODER,
        "from ..record import Row\nfrom . import helper\n",
        {},
    ),
    ("the decoder imports the record's package", NEW_DECODER, "from tensor24 import record\n", {}),
    ("the record imports numpy", NEW_RECORD, "import numpy as np\n", {"ISOLATE": 1}),
    (
        "the record imports the standard library",
        NEW_RECORD,
        "import json\nfrom dataclasses import dataclass\n",
        {},
    ),
    ("the engine imports the decoder", NEW_STEP, "from tensor24.decoder import rows\n", {"ISOLATE": 1}),
    ("the engine imports the runner, relative", NEW_STEP, "from ..runner import loop\n", {"ISOLATE": 1}),
    (
        "the engine imports the current engine",
        NEW_STEP,
        "from event_universe import clock\n",
        {"ISOLATE": 1},
    ),
    (
        "the engine imports numpy and the record",
        NEW_STEP,
        "import numpy as np\nfrom tensor24.record import Row\nfrom .carry import carry\n",
        {},
    ),
    (
        "the runner imports the decoder",
        NEW_RUNNER,
        "from tensor24.decoder import rows\n",
        {"ISOLATE": 1},
    ),
    (
        "the runner imports the engine",
        NEW_RUNNER,
        "from tensor24.engine import step\n",
        {"ISOLATE": 1},
    ),
    (
        "the runner imports the engine, relative",
        NEW_RUNNER,
        "from ..engine.step import step\n",
        {"ISOLATE": 1},
    ),
    (
        "the runner takes the step by argument",
        NEW_RUNNER,
        "from tensor24.record import Row\n\n\ndef run(step, ticks):\n    for t in ticks:\n        step(t)\n",
        {},
    ),
    (
        "the current engine imports numpy",
        "tick.py",
        "import numpy as np\nfrom event_universe import clock\n",
        {},
    ),
    ("the carry's home divides", NEW_CARRY, "def f(a, b):\n    return a // b, a % b\n", {}),
    (
        "the new engine elsewhere divides",
        NEW_STEP,
        "def f(a, b):\n    return a // b, a % b\n",
        {"OPERATION": 2},
    ),
    ("a loop in the runner", NEW_RUNNER, "def f(a):\n    for x in a:\n        pass\n", {}),
    ("a loop in the decoder", NEW_DECODER, "def f(a):\n    return [x for x in a]\n", {}),
    ("a loop in the new engine", NEW_STEP, "def f(a):\n    for x in a:\n        pass\n", {"LOOP": 1}),
    (
        "a branch in the decoder",
        NEW_DECODER,
        "def f(a):\n    if a:\n        return a\n    return a\n",
        {},
    ),
    (
        "a branch in the new engine",
        NEW_STEP,
        "def f(a):\n    if a:\n        return a\n    return a\n",
        {"BRANCH": 1},
    ),
    (
        "an ordering comparison in the new engine",
        NEW_STEP,
        "def f(a, b):\n    return a < b\n",
        {"COMPARE": 1},
    ),
    ("sorted in the new engine", NEW_STEP, "def f(a):\n    return sorted(a)\n", {"COMPARE": 1}),
    (
        "operator.lt in the new engine",
        NEW_STEP,
        "import operator\n\n\ndef f(a, b):\n    return operator.lt(a, b)\n",
        {"COMPARE": 1},
    ),
    (
        "numpy's greater in the new engine",
        NEW_STEP,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.greater(a, b)\n",
        {"COMPARE": 1},
    ),
    ("sorted in the current engine", "tick.py", "def f(a):\n    return sorted(a)\n", {}),
    ("sorted in the decoder", NEW_DECODER, "def f(a):\n    return sorted(a)\n", {}),
    (
        "an array with no dtype in the new engine",
        NEW_STEP,
        "import numpy as np\n\nX = np.array([1])\n",
        {"DTYPE": 1},
    ),
    (
        "arange with no dtype in the new engine",
        NEW_STEP,
        "import numpy as np\n\nX = np.arange(1)\n",
        {"DTYPE": 1},
    ),
    (
        "an array with its dtype in the new engine",
        NEW_STEP,
        "import numpy as np\n\nX = np.array([1], dtype=object)\n",
        {},
    ),
    (
        "an array with no dtype in the current engine",
        "tick.py",
        "import numpy as np\n\nX = np.array([1])\n",
        {},
    ),
    ("min over one iterable in the decoder", NEW_DECODER, "def f(a):\n    return min(a)\n", {}),
    (
        "max over a generator in the decoder",
        NEW_DECODER,
        "def f(a):\n    return max(x for x in a)\n",
        {},
    ),
    (
        "max of a written-out pair in the decoder",
        NEW_DECODER,
        "def f(a, b):\n    return max(a, b)\n",
        {"CLAMP": 1},
    ),
    (
        "max of a tuple in the decoder",
        NEW_DECODER,
        "def f(a, b):\n    return max((a, b))\n",
        {"CLAMP": 1},
    ),
    (
        "max of a list in the decoder",
        NEW_DECODER,
        "def f(a, b):\n    return min([a, b])\n",
        {"CLAMP": 1},
    ),
    ("max of a star in the decoder", NEW_DECODER, "def f(a):\n    return max(*a)\n", {"CLAMP": 1}),
    (
        "clip in the decoder",
        NEW_DECODER,
        "import numpy as np\n\n\ndef f(a):\n    return np.clip(a, 0, 1)\n",
        {"CLAMP": 1},
    ),
    ("abs in the decoder", NEW_DECODER, "def f(a):\n    return abs(a)\n", {"CLAMP": 1}),
    ("where in the decoder", NEW_DECODER, "def f(a, b):\n    return where(a, b, 0)\n", {"CLAMP": 1}),
    ("a remainder in the decoder", NEW_DECODER, "def f(a, b):\n    return a % b\n", {"OPERATION": 1}),
    ("divmod in the decoder", NEW_DECODER, "def f(a, b):\n    return divmod(a, b)\n", {"OPERATION": 1}),
    ("a refusal in the decoder", NEW_DECODER, "def f(a):\n    raise ValueError(a)\n", {"REFUSE": 1}),
    (
        "an ordering comparison in the decoder",
        NEW_DECODER,
        "def f(a, b):\n    return a < b\n",
        {},
    ),
    ("a log read in the decoder", NEW_DECODER, "def f(a):\n    return a.log\n", {}),
    ("a remainder in the runner", NEW_RUNNER, "def f(a, b):\n    return a % b\n", {}),
    ("a refusal in the runner", NEW_RUNNER, "def f(a):\n    raise ValueError(a)\n", {}),
    ("max of a pair in the runner", NEW_RUNNER, "def f(a, b):\n    return max(a, b)\n", {}),
    ("a loop in the readings", NEW_READING, "def f(a):\n    for x in a:\n        pass\n", {"LOOP": 1}),
    (
        "an ordering comparison in the readings",
        NEW_READING,
        "def f(a, b):\n    return a < b\n",
        {"COMPARE": 1},
    ),
    (
        "a branch in the readings",
        NEW_READING,
        "def f(a):\n    if a:\n        return a\n    return a\n",
        {"BRANCH": 1},
    ),
    ("max of a pair in the readings", NEW_READING, "def f(a, b):\n    return max(a, b)\n", {"CLAMP": 1}),
    ("a remainder in the readings", NEW_READING, "def f(a, b):\n    return a % b\n", {"OPERATION": 1}),
    ("the readings import numpy", NEW_READING, "import numpy as np\n", {"ISOLATE": 1}),
    (
        "the readings import the engine",
        NEW_READING,
        "from tensor24.engine import step\n",
        {"ISOLATE": 1},
    ),
    (
        "the readings import the runner",
        NEW_READING,
        "from tensor24.runner import loop\n",
        {"ISOLATE": 1},
    ),
    (
        "the readings import the decoder",
        NEW_READING,
        "from tensor24.decoder import rows\n",
        {"ISOLATE": 1},
    ),
    ("the readings import the record", NEW_READING, "from tensor24.record import schema\n", {}),
    ("the readings import the record, relative", NEW_READING, "from ..record import schema\n", {}),
    (
        "the readings import the standard library",
        NEW_READING,
        "import itertools\nfrom typing import Any\n",
        {},
    ),
    ("the readings import one another", NEW_READING, "from tensor24.readings import sweep\n", {}),
    (
        "the engine imports the readings",
        NEW_STEP,
        "from tensor24.readings import wind\n",
        {"ISOLATE": 1},
    ),
    (
        "the engine imports the readings, relative",
        NEW_STEP,
        "from ..readings import wind\n",
        {"ISOLATE": 1},
    ),
    (
        "the record imports the readings",
        NEW_RECORD,
        "from tensor24.readings import wind\n",
        {"ISOLATE": 1},
    ),
    ("the runner imports the readings", NEW_RUNNER, "from tensor24.readings import wind\n", {}),
    ("the runner imports the readings, relative", NEW_RUNNER, "from ..readings import wind\n", {}),
    ("the decoder imports the readings", NEW_DECODER, "from tensor24.readings import wind\n", {}),
    ("the decoder imports the readings, relative", NEW_DECODER, "from ..readings import wind\n", {}),
    ("the decoder imports the readings' package", NEW_DECODER, "from tensor24 import readings\n", {}),
    # a floor or a bound is an if (the owner's words of 2026-10-28, 12:0x): a quotient spelt as a mask, a name that holds one
    (
        "the quotient of a bit",
        NEW_CARRY,
        "def f(x):\n    return 1 // (x + 1)\n",
        {"INDICATOR": 1},
    ),
    (
        "1 minus a quotient",
        NEW_CARRY,
        "def f(a, b):\n    return 1 - a // b\n",
        {"INDICATOR": 1},
    ),
    (
        "the sign test",
        NEW_CARRY,
        "def f(x):\n    return 1 + x // (x * x + 1)\n",
        {"INDICATOR": 1},
    ),
    (
        "the sign test with the square first",
        NEW_CARRY,
        "def f(x):\n    return x // (1 + x * x)\n",
        {"INDICATOR": 1},
    ),
    (
        "the indicator 1 - 1 div (q + 1): the quotient of a bit and 1 minus a quotient",
        NEW_CARRY,
        "def f(q):\n    return 1 - 1 // (q + 1)\n",
        {"INDICATOR": 2},
    ),
    (
        "the carry's quotient of a bit",
        NEW_CARRY,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {"INDICATOR": 1},
    ),
    (
        "1 minus the carry's quotient",
        NEW_CARRY,
        "def f(carries, a, b):\n    return 1 - carries(a, b)\n",
        {"INDICATOR": 1},
    ),
    (
        "an indicator in the readings",
        NEW_READING,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {"INDICATOR": 1},
    ),
    (
        "an indicator in the current engine",
        "tick.py",
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {"INDICATOR": 1},
    ),
    ("an ordinary quotient", NEW_CARRY, "def f(a, b):\n    return a // b\n", {}),
    ("a quotient of a sum", NEW_CARRY, "def f(a, b):\n    return (a + 1) // b\n", {}),
    (
        "a quotient by a sum with one",
        NEW_CARRY,
        "def f(a, b):\n    return a // (b + 1)\n",
        {},
    ),
    (
        "a quotient by a square and one that are not one's square",
        NEW_CARRY,
        "def f(a, b, c):\n    return a // (b * c + 1)\n",
        {},
    ),
    ("a carry of two numbers", NEW_CARRY, "def f(carries, a, b):\n    return carries(a, b)\n", {}),
    (
        "an indicator in a reader",
        READER,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {},
    ),
    (
        "an indicator in the decoder",
        NEW_DECODER,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {},
    ),
    (
        "an indicator in the runner",
        NEW_RUNNER,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        {},
    ),
    ("a floor by name", NEW_STEP, "def floor_of(a):\n    return a\n", {"BOUND": 1}),
    ("a cap by name", NEW_STEP, "def f(a):\n    return a.cap\n", {"BOUND": 1}),
    ("a bound by a camel name", NEW_STEP, "def f(a):\n    return a.upperBound\n", {"BOUND": 1}),
    ("a clamp by name", NEW_STEP, "def f(a):\n    return a.clamped\n", {"BOUND": 1}),
    ("a limit by name", NEW_STEP, "def f(a):\n    return a.limit\n", {"BOUND": 1}),
    ("a floor in the readings", NEW_READING, "def f(a):\n    return a.floor\n", {"BOUND": 1}),
    ("a floor in the current engine", "tick.py", "def f(a):\n    return a.floor\n", {"BOUND": 1}),
    (
        "words that only contain one",
        NEW_STEP,
        "def f(a):\n    return a.capacity + a.boundary + a.flooring\n",
        {},
    ),
    ("a floor in a string", NEW_STEP, "X = 'the floor'\n", {}),
    ("a floor in a reader", READER, "def f(a):\n    return a.floor\n", {}),
    ("a floor in the decoder", NEW_DECODER, "def f(a):\n    return a.floor\n", {}),
    ("a floor in the runner", NEW_RUNNER, "def f(a):\n    return a.floor\n", {}),
]

# a note is a refusal in the new engine's strict folders (engine, record, readings) and a note elsewhere
TIERS: list[tuple[str, str, str, str, str]] = [
    ("a comparison in the new engine", NEW_STEP, "def f(a, b):\n    return a < b\n", "COMPARE", "BLOCK"),
    ("a branch in the new engine", NEW_STEP, "def f(a):\n    return a if a else a\n", "BRANCH", "BLOCK"),
    (
        "a cache in the new record",
        NEW_RECORD,
        "from functools import cache\n\n\n@cache\ndef f(a):\n    return a\n",
        "MEMO",
        "BLOCK",
    ),
    (
        "a comparison in the readings",
        NEW_READING,
        "def f(a, b):\n    return a < b\n",
        "COMPARE",
        "BLOCK",
    ),
    (
        "a branch in the readings",
        NEW_READING,
        "def f(a):\n    return a if a else a\n",
        "BRANCH",
        "BLOCK",
    ),
    (
        "a comparison in the current engine",
        "tick.py",
        "def f(a, b):\n    return a < b\n",
        "COMPARE",
        "WARN",
    ),
    (
        "a branch in the current engine",
        "tick.py",
        "def f(a):\n    return a if a else a\n",
        "BRANCH",
        "WARN",
    ),
    (
        "an indicator in the new engine stays a note",
        NEW_CARRY,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        "INDICATOR",
        "WARN",
    ),
    (
        "an indicator in the readings stays a note",
        NEW_READING,
        "def f(carries, x):\n    return carries(1, x + 1)\n",
        "INDICATOR",
        "WARN",
    ),
    (
        "a bound by name in the new engine stays a note",
        NEW_STEP,
        "def f(a):\n    return a.floor\n",
        "BOUND",
        "WARN",
    ),
    (
        "a bound by name in the record stays a note",
        NEW_RECORD,
        "def f(a):\n    return a.limit\n",
        "BOUND",
        "WARN",
    ),
]


def counts(rel: str, source: str) -> dict[str, int]:
    return dict(Counter(hit.rule for hit in gate.scan(rel, source)))


def main() -> int:
    parted = 0
    for label, rel, source, want in CASES:
        got = counts(rel, source)
        want = {rule: n for rule, n in want.items() if n}
        # a case names the rules it tests; a hit of another rule (the numbers in a snippet, the import) may stand beside it
        beside = {rule: n for rule, n in got.items() if rule in want or want == {}}
        extra = {rule: n for rule, n in got.items() if rule not in want}
        if want == {}:
            ok = not got
        else:
            ok = all(got.get(rule, 0) == n for rule, n in want.items())
        if not ok:
            parted += 1
            print(f"PARTED  {label}: wanted {want}, the gate gave {got}")
        elif extra and want:
            print(f"ok      {label} (beside it: {extra})")
        else:
            print(f"ok      {label}")
        del beside
    tier_cases = 0
    for label, rel, source, rule, tier in TIERS:
        tier_cases += 1
        got = {hit.tier for hit in gate.scan(rel, source) if hit.rule == rule}
        if got != {tier}:
            parted += 1
            print(f"PARTED  {label}: wanted the tier {tier}, the gate gave {got}")
        else:
            print(f"ok      {label}: {rule} is a {tier}")
    # the ratchet: a hit above the base's count is new, one at the base's count is not
    hits = gate.scan(ENGINE, "def f(a):\n    for x in a:\n        pass\n    for y in a:\n        pass\n")
    stands = Counter({("LOOP", ENGINE, "for"): 1})
    new = gate.above(hits, stands)
    if len(new) != 1:
        parted += 1
        print(f"PARTED  the ratchet: two loops against one that stands gave {len(new)} new")
    else:
        print("ok      the ratchet: two loops against one that stands give one new")
    # a new package starts at 0, so every hit in it is new
    fresh = gate.above(
        gate.scan("another_engine/core.py", "def f(a):\n    return min(a, 5)\n"), Counter()
    )
    if len(fresh) != 2:
        parted += 1
        print(f"PARTED  a new package: a clamp and a number gave {len(fresh)} new, not 2")
    else:
        print("ok      a new package: every hit in it is new")
    print(f"selftest: {len(CASES) + tier_cases + 2} cases, {parted} parted")
    return 1 if parted else 0


if __name__ == "__main__":
    sys.exit(main())
