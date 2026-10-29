"""Sofer's gate tested on itself: every rule of scribe_scan.py meets a snippet that must trip it and a snippet that must not.

  venv314/bin/python tools/derivations/open_items/scribe_scan_selftest.py

Each case names the module the snippet stands in (a reader, the carry's home and a tests file are treated apart by the gate),
the source, and the hits by rule it must give; the exit status is 1 on the first case that parts from its count. Run it at
every change of the gate (SCRIBE-GATE-1.md): a rule that stops tripping would let a push through unseen.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
from collections import Counter
from collections.abc import Iterator
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
NEW_CARRY = "tensor24/algebra/carry.py"
OLD_CARRY = "tensor24/engine/carry.py"
NEW_RING = "tensor24/algebra/ring.py"
NEW_MAIN = "tensor24/main.py"
NEW_REWIND = "tensor24/runner/rewind.py"
NEW_RECORD = "tensor24/record/schema.py"
NEW_RUNNER = "tensor24/runner/loop.py"
NEW_BOARD = "tensor24/runner/board.py"
NEW_DECODER = "tensor24/decoder/rows.py"
NEW_READING = "tensor24/readings/wind.py"
NEW_MESH = "tensor24/engine/mesh.py"
NEW_ROOT = "tensor24/__init__.py"
TOOL_FILES = "tools/tensor24_files.py"
TOOL_DECODE = "tools/tensor24_decode.py"
# runner/board.py as the Boss wrote it at 0ff2ae0dc: the closed list's own vocabulary holds it clean
BOARD_SOURCE = "\n".join(
    [
        '"""The board from its shape: each site\'s six neighbours, the wrap by Rule3 on each coordinate, and each Spoke\'s Mesh."""',
        '',
        'import numpy as np',
        '',
        'from tensor24.algebra.carry import Z, carry',
        '',
        '',
        'def site(x: Z, y: Z, z: Z, sy: Z, sz: Z) -> Z:',
        '    """The site at three coordinates, z the fastest: (x sy + y) sz + z."""',
        '    return (x * sy + y) * sz + z',
        '',
        '',
        'def wrap(x: Z, side: Z) -> Z:',
        '    """A coordinate brought onto the board\'s side by Rule3: the carry\'s remainder."""',
        '    _, kept = carry(x, side, 0)',
        '    return kept',
        '',
        '',
        'def board(shape: tuple[int, int, int]) -> tuple[Z, Z]:',
        '    """The six neighbours of every site, +x, -x, +y, -y, +z, -z, and the Mesh each Spoke holds, as index arrays."""',
        '    sx, sy, sz = shape',
        '    n = sx * sy * sz',
        '    sites = np.arange(n, dtype=np.intp)  # an index array: the sites counted, each a whole number below n',
        '    rest, z = carry(sites, sz, 0)',
        '    x, y = carry(rest, sy, 0)',
        '    nb = np.stack(',
        '        [',
        '            site(wrap(x + 1, sx), y, z, sy, sz),',
        '            site(wrap(x - 1, sx), y, z, sy, sz),',
        '            site(x, wrap(y + 1, sy), z, sy, sz),',
        '            site(x, wrap(y - 1, sy), z, sy, sz),',
        '            site(x, y, wrap(z + 1, sz), sy, sz),',
        '            site(x, y, wrap(z - 1, sz), sy, sz),',
        '        ]',
        '    )',
        '    _, mx, _, my, _, mz = nb',
        '    meshes = np.stack([sites, mx, n + sites, n + my, n + n + sites, n + n + mz])',
        '    return nb, meshes',
    ]
)
BOARD_SOURCE += "\n"

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
        "import numpy as np\nfrom tensor24.record import Row\nfrom tensor24.algebra.carry import carry\n",
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
        "import numpy as np\n\n\ndef f(a):\n    return np.array(a, dtype=object)\n",
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
    # the board's module keeps the rules a wrap by hand would break; the rest of the runner is spared them
    ("a remainder in the board's module", NEW_BOARD, "def f(a, b):\n    return a % b\n", {"OPERATION": 1}),
    ("a floor division in the board's module", NEW_BOARD, "def f(a, b):\n    return a // b\n", {"OPERATION": 1}),
    ("an augmented remainder in the board's module", NEW_BOARD, "def f(a, b):\n    a %= b\n    return a\n", {"OPERATION": 1}),
    ("divmod in the board's module", NEW_BOARD, "def f(a, b):\n    return divmod(a, b)\n", {"OPERATION": 1}),
    (
        "numpy's mod in the board's module",
        NEW_BOARD,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.mod(a, b)\n",
        {"OPERATION": 1},
    ),
    (
        "numpy's floor_divide in the board's module",
        NEW_BOARD,
        "import numpy as np\n\n\ndef f(a, b):\n    return np.floor_divide(a, b)\n",
        {"OPERATION": 1},
    ),
    ("a power in the board's module", NEW_BOARD, "def f(a):\n    return a ** a\n", {"OPERATION": 1}),
    ("a shift in the board's module", NEW_BOARD, "def f(a):\n    return a << a\n", {"OPERATION": 1}),
    ("a branch in the board's module", NEW_BOARD, "def f(a, b):\n    if a:\n        return b\n    return a\n", {"BRANCH": 1}),
    ("a conditional expression in the board's module", NEW_BOARD, "def f(a, b):\n    return b if a else a\n", {"BRANCH": 1}),
    ("an ordering comparison in the board's module", NEW_BOARD, "def f(a, b):\n    return a < b\n", {"COMPARE": 1}),
    ("a loop in the board's module", NEW_BOARD, "def f(a):\n    for x in a:\n        pass\n", {"LOOP": 1}),
    ("a comprehension in the board's module", NEW_BOARD, "def f(a):\n    return [x for x in a]\n", {"LOOP": 1}),
    ("max of a pair in the board's module", NEW_BOARD, "def f(a, b):\n    return max(a, b)\n", {"CLAMP": 1}),
    ("where in the board's module", NEW_BOARD, "def f(a, b):\n    return where(a, b, 0)\n", {"CLAMP": 1}),
    (
        "a wrap by hand in the board's module: a subtraction under a comparison",
        NEW_BOARD,
        "def f(a, b):\n    return a - b if a >= b else a\n",
        {"BRANCH": 1, "COMPARE": 1},
    ),
    (
        "the carry imported and called in the board's module",
        NEW_BOARD,
        "from tensor24.algebra.carry import carry\n\n\ndef f(a, b):\n    return carry(a, b, 0)\n",
        {},
    ),
    ("an equality as a whether in the board's module", NEW_BOARD, "def f(a, b):\n    return a == b\n", {"ALLOW": 1}),
    ("a raise in the board's module", NEW_BOARD, "def f(a):\n    raise ValueError(a)\n", {"ALLOW": 1}),
    ("a remainder in a module named for the board", "tensor24/runner/boards.py", "def f(a, b):\n    return a % b\n", {}),
    ("a remainder in a runner module whose name ends in the board's", "tensor24/runner/dashboard.py", "def f(a, b):\n    return a % b\n", {}),
    # the dodges of the board's rule: a method's name, a name imported or aliased, a getattr, numpy's own wraps
    ("numpy's divmod in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a, b):\n    return np.divmod(a, b)\n', {"OPERATION": 1}),
    ("numpy's divmod in the decoder", NEW_DECODER, 'import numpy as np\n\n\ndef f(a, b):\n    return np.divmod(a, b)\n', {"OPERATION": 1}),
    ("numpy's take with a mode in another runner module", NEW_RUNNER, "import numpy as np\n\n\ndef f(a, i):\n    return np.take(a, i, mode='wrap')\n", {}),
    ("a take with a mode in the decoder", NEW_DECODER, "def f(a, i):\n    return a.take(i, mode='wrap')\n", {}),
    ("numpy's unravel_index in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(x, side):\n    return np.unravel_index(x, (side, side))[1]\n', {"ALLOW": 1}),
    ("numpy's equal as a whether in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(x, side):\n    return x + side * np.equal(x, side)\n', {"ALLOW": 1}),
    ("numpy's digitize as a whether in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(x, side):\n    return x - side * np.digitize(x, [0, side])\n', {"ALLOW": 1}),
    ("a getattr of a built name in the board's module", NEW_BOARD, "import numpy as np\n\n\ndef f(x, side):\n    return getattr(np, 're' + 'mainder')(x, side)\n", {"ALLOW": 4}),
    ("vars of numpy by a key in the board's module", NEW_BOARD, "import numpy as np\n\n\ndef f(x, side):\n    return vars(np)['remainder'](x, side)\n", {"ALLOW": 3}),
    ("numpy's tile of the index range in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(x, side):\n    return np.tile(np.arange(side, dtype=np.intp), 1 + 1 + 1)[x + side]\n', {"ALLOW": 1}),
    ("an array's take method in the board's module", NEW_BOARD, 'def f(a, i):\n    return a.take(i)\n', {"ALLOW": 1}),
    ("numpy's arange with the index dtype in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(n):\n    return np.arange(n, dtype=np.intp)\n', {}),
    ("numpy's stack of a list in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a, b):\n    return np.stack([a, b])\n', {}),
    ("numpy's arange with another dtype in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(n):\n    return np.arange(n, dtype=np.int64)\n', {"ALLOW": 2}),
    ("numpy's arange with no dtype in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(n):\n    return np.arange(n)\n', {"ALLOW": 1, "DTYPE": 1}),
    ("numpy's equal in another runner module", NEW_RUNNER, 'import numpy as np\n\n\ndef f(x, side):\n    return x + side * np.equal(x, side)\n', {}),
    ('vars of numpy by a key in another runner module', NEW_RUNNER, "import numpy as np\n\n\ndef f(x, side):\n    return vars(np)['remainder'](x, side)\n", {}),
    ("numpy's unravel_index in another runner module", NEW_RUNNER, 'import numpy as np\n\n\ndef f(x, side):\n    return np.unravel_index(x, (side, side))[1]\n', {}),
    ("numpy's digitize in another runner module", NEW_RUNNER, 'import numpy as np\n\n\ndef f(x, side):\n    return x - side * np.digitize(x, [0, side])\n', {}),
    ("the board's module as the Boss wrote it (0ff2ae0dc)", NEW_BOARD, BOARD_SOURCE, {}),
    ("a method call of the remainder in the board's module", NEW_BOARD, 'def f(a, b):\n    return a.__mod__(b)\n', {"OPERATION": 1}),
    ("a method call of the floor division in the board's module", NEW_BOARD, 'def f(a, b):\n    return a.__floordiv__(b)\n', {"OPERATION": 1}),
    ("a method call of the reflected remainder in the board's module", NEW_BOARD, 'def f(a, b):\n    return a.__rmod__(b)\n', {"OPERATION": 1}),
    ("a method call of divmod in the board's module", NEW_BOARD, 'def f(a, b):\n    return a.__divmod__(b)\n', {"OPERATION": 1}),
    ("a method call of the power in the board's module", NEW_BOARD, 'def f(a, b):\n    return a.__pow__(b)\n', {"OPERATION": 1}),
    ("a getattr of the remainder's method in the board's module", NEW_BOARD, "def f(a, b):\n    return getattr(a, '__mod__')(b)\n", {"OPERATION": 1}),
    ("a getattr of numpy's mod in the board's module", NEW_BOARD, "import numpy as np\n\n\ndef f(a, b):\n    return getattr(np, 'mod')(a, b)\n", {"OPERATION": 1}),
    ("numpy's ndarray method of the remainder in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a, b):\n    return np.ndarray.__mod__(a, b)\n', {"OPERATION": 1}),
    ("numpy's mod imported by name in the board's module", NEW_BOARD, 'from numpy import mod as m\n\n\ndef f(a, b):\n    return m(a, b)\n', {"OPERATION": 1}),
    ("operator's floordiv imported by name in the board's module", NEW_BOARD, 'from operator import floordiv\n\n\ndef f(a, b):\n    return floordiv(a, b)\n', {"OPERATION": 1}),
    ("numpy's mod aliased in the board's module", NEW_BOARD, 'import numpy as np\n\ng = np.mod\n\n\ndef f(a, b):\n    return g(a, b)\n', {"OPERATION": 1}),
    ("numpy's remainder passed as a value in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a, g):\n    return g(np.remainder)\n', {"OPERATION": 1}),
    ("numpy's roll in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a):\n    return np.roll(a, 1)\n', {"OPERATION": 1}),
    ("numpy's pad in the board's module", NEW_BOARD, 'import numpy as np\n\n\ndef f(a):\n    return np.pad(a, 1)\n', {"OPERATION": 1}),
    ("numpy's roll imported by name in the board's module", NEW_BOARD, 'from numpy import roll\n\n\ndef f(a):\n    return roll(a, 1)\n', {"OPERATION": 1}),
    ("numpy's take with a mode in the board's module", NEW_BOARD, "import numpy as np\n\n\ndef f(a, i):\n    return np.take(a, i, mode='wrap')\n", {"OPERATION": 1}),
    ("numpy's take with no mode in the board's module", NEW_BOARD, "import numpy as np\n\n\ndef f(a, i):\n    return np.take(a, i)\n", {"ALLOW": 1}),
    ("methods that are no operation in the board's module", NEW_BOARD, "def f(a, i):\n    return a.__getitem__(i), a.__len__()\n", {"ALLOW": 2}),
    ("a numpy name that is no operation imported in the board's module", NEW_BOARD, 'from numpy import stack\n\n\ndef f(a):\n    return stack(a)\n', {}),
    ('a method call of the remainder in another runner module', NEW_RUNNER, 'def f(a, b):\n    return a.__mod__(b)\n', {}),
    ("numpy's mod in another runner module", NEW_RUNNER, 'import numpy as np\n\n\ndef f(a, b):\n    return np.mod(a, b)\n', {}),
    ("numpy's roll in another runner module", NEW_RUNNER, 'import numpy as np\n\n\ndef f(a):\n    return np.roll(a, 1)\n', {}),
    ('a method call of the remainder in the decoder', NEW_DECODER, 'def f(a, b):\n    return a.__mod__(b)\n', {"OPERATION": 1}),
    ("numpy's mod imported by name in the decoder", NEW_DECODER, 'from numpy import mod\n\n\ndef f(a, b):\n    return mod(a, b)\n', {"OPERATION": 1}),
    ('a method call of the remainder in the current engine', ENGINE, 'def f(a, b):\n    return a.__mod__(b)\n', {"OPERATION": 1}),
    ("a method call of the remainder in the carry's home", CARRY, 'def f(a, b):\n    return a.__mod__(b)\n', {}),
    ("a remainder in the board's name in the decoder", "tensor24/decoder/board.py", "def f(a, b):\n    return a % b\n", {"OPERATION": 1}),
    ("a loop in a module of the decoder named for the board", "tensor24/decoder/board.py", "def f(a):\n    for x in a:\n        pass\n", {}),
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
    (
        "a carry of two numbers",
        NEW_CARRY,
        "def carries(a, b):\n    return a // b\n\n\ndef f(a, b):\n    return carries(a, b)\n",
        {},
    ),
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
        "def f(capacity, boundary, flooring):\n    return capacity + boundary + flooring\n",
        {},
    ),
    ("a floor in a docstring", NEW_STEP, 'def f(a):\n    """the floor"""\n    return a\n', {}),
    ("a floor in a reader", READER, "def f(a):\n    return a.floor\n", {}),
    ("a floor in the decoder", NEW_DECODER, "def f(a):\n    return a.floor\n", {}),
    ("a floor in the runner", NEW_RUNNER, "def f(a):\n    return a.floor\n", {}),
]


# The closed list (the owner's idea of 2026-10-28, 15:0x UTC: say what a Node-clock may do, and what is not named is refused; the
# law: its only operations are addition, multiplication and Rule3's carry, on whole numbers). In the new engine's engine/ and
# readings/ a snippet that holds anything the list does not name gives a hit of ALLOW, and the same snippet gives none in the
# record, the runner, the decoder and the current engine (main() runs each snippet there too).
def fn(body: str, args: str = "a") -> str:
    """A module of one function f of `args`, its body the lines given."""
    return f"def f({args}):\n" + "".join(f"    {line}\n" for line in body.split("\n"))


NP = "import numpy as np\n\n\n"
LAWFUL_MESH = (
    "import numpy as np\n"
    "from .carry import carry\n\n\n"
    "def across(f, nb):\n"
    '    """The six Spokes at once: the stencil is one gather."""\n'
    "    return np.take(f, nb, axis=1)\n\n\n"
    "def link(ends, nb, coupling):\n"
    "    six = across(ends, nb)\n"
    '    pulled = np.einsum("gs,gns->gn", coupling, six)\n'
    "    shifted = np.roll(pulled, 1, axis=0)\n"
    "    quotient, remainder = carry(pulled, shifted)\n"
    "    return pulled * shifted + quotient, shifted - remainder\n"
)


def refused(label: str, source: str, allow: int = 1) -> tuple[str, str, str, dict[str, int]]:
    """A snippet that the closed list refuses `allow` times in the new engine's engine/ (the older rules may stand beside it)."""
    return (label, NEW_STEP, source, {"ALLOW": allow})


CASES += [
    # what the list names passes, with no hit of any rule
    (
        "a lawful Mesh act: a gather, a contraction, a roll, a carry, sums and products",
        NEW_MESH,
        LAWFUL_MESH,
        {},
    ),
    (
        "a lawful reading: an array's sum, its transpose, a keyword",
        NEW_READING,
        fn("return a.sum(axis=0) * a.T.sum(axis=1)"),
        {},
    ),
    (
        "an array's methods, a subscript, a slice and a negative one",
        NEW_STEP,
        fn("return a.reshape(b).T.sum(axis=0) + a[..., 1:] - a[..., :-1]", "a, b"),
        {},
    ),
    (
        "a record: a frozen dataclass",
        NEW_STEP,
        "from dataclasses import dataclass\n\n\n@dataclass(frozen=True)\nclass Layout:\n    nb: object\n    width: int = 1\n",
        {},
    ),
    (
        "a record: a named tuple",
        NEW_STEP,
        "from typing import NamedTuple\n\n\nclass Row(NamedTuple):\n    tick: int\n    site: int\n",
        {},
    ),
    (
        "an annotation is no code",
        NEW_STEP,
        "def f(a: int | None, b: 'tuple[int, ...]' = None) -> tuple[int, int]:\n    return a, b\n",
        {},
    ),
    (
        "a type-checking guard",
        NEW_STEP,
        "from typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from .carry import carry\n",
        {},
    ),
    (
        "einsum imported by name, and its subscripts",
        NEW_STEP,
        "from numpy import einsum\n\n\ndef f(a, b):\n    return einsum('a,a->a', a, b)\n",
        {},
    ),
    (
        "a function of the engine's own: a default 1 and a free keyword",
        NEW_STEP,
        "def g(a, going=1):\n    return a\n\n\ndef f(a):\n    return g(a, going=0)\n",
        {},
    ),
    ("True as a keyword's value", NEW_STEP, NP + fn("return np.sum(a, axis=0, keepdims=True)"), {}),
    ("a matrix product", NEW_STEP, fn("return a @ b + a * b - b", "a, b"), {}),
    # the statements and the expressions that are not on the list
    refused("an if", fn("if a:\n    return a\nreturn a")),
    refused("a conditional expression", fn("return a if a else a")),
    refused("a match", fn("match a:\n    case _:\n        return a")),
    refused("a for", fn("for x in a:\n    pass")),
    refused("a while", fn("while a:\n    a = 0")),
    refused("a list comprehension", fn("return [x for x in a]")),
    refused("a set comprehension", fn("return {x for x in a}")),
    refused("a dict comprehension", fn("return {x: x for x in a}")),
    refused("a generator", fn("return (x for x in a)")),
    refused("a lambda", fn("return lambda b: b")),
    refused("a try", fn("try:\n    return a\nexcept ValueError:\n    return a")),
    refused("a raise", fn("raise ValueError(a)")),
    refused("an assert", fn("assert a")),
    refused("a with", fn("with a:\n    pass")),
    refused("a delete", fn("del a")),
    refused("a global", "X = 1\n\n\ndef f():\n    global X\n    X = 0\n"),
    refused(
        "a nonlocal",
        "def f():\n    a = 0\n\n    def g():\n        nonlocal a\n        a = 1\n\n    return g\n",
    ),
    refused("a yield", fn("yield a")),
    refused("an async def with an await", "async def f(a):\n    return await a\n"),
    refused("a walrus", fn("return (b := a)")),
    refused("an f-string", fn('return f"{a}"')),
    refused("an ordering comparison", fn("return a < b", "a, b")),
    refused("an equality", fn("return a == b", "a, b")),
    refused("an inequality", fn("return a != b", "a, b")),
    refused("an identity test", fn("return a is b", "a, b")),
    refused("a membership test", fn("return a in b", "a, b")),
    refused("an and", fn("return a and b", "a, b")),
    refused("an or", fn("return a or b", "a, b")),
    refused("a not", fn("return not a")),
    refused("an invert", fn("return ~a")),
    refused("a true division", fn("return a / b", "a, b")),
    refused("a power", fn("return a ** b", "a, b")),
    refused("a left shift", fn("return a << b", "a, b")),
    refused("a right shift", fn("return a >> b", "a, b")),
    refused("a bit and", fn("return a & b", "a, b")),
    refused("a bit or", fn("return a | b", "a, b")),
    refused("an exclusive or", fn("return a ^ b", "a, b")),
    refused("a list display", fn("return [a]")),
    refused("a set display", fn("return {a}")),
    refused("a dict display", fn("return {a: a}")),
    refused("a star in a call", "def g(a):\n    return a\n\n\ndef f(a):\n    return g(*a)\n"),
    refused("an augmented assignment", fn("a += 1\nreturn a")),
    refused("a decorator", "def decorate(g):\n    return g\n\n\n@decorate\ndef f(a):\n    return a\n"),
    refused("a star parameter", "def f(*a):\n    return a\n"),
    refused("a double star parameter", "def f(**a):\n    return a\n"),
    refused("a positional-only parameter", "def f(a, /):\n    return a\n"),
    refused("a keyword-only parameter", "def f(a, *, b):\n    return a\n"),
    refused("a default that is no name, 0, 1 or None", "def f(a, b=a + 1):\n    return a\n"),
    refused("a class that is no record", "class C:\n    x = 1\n"),
    refused(
        "a dataclass that is not frozen",
        "from dataclasses import dataclass\n\n\n@dataclass\nclass C:\n    x: int\n",
    ),
    refused(
        "a record with a method",
        "from typing import NamedTuple\n\n\nclass R(NamedTuple):\n    a: int\n\n    def total(self):\n        return self.a\n",
    ),
    refused("an assignment to an attribute", fn("a.x = 1")),
    refused("an assignment to a nested tuple", fn("(a, (b, c)) = a")),
    refused("an import of everything", "from numpy import *\n"),
    refused("a name of numpy that is off the list", "from numpy import sort\n"),
    refused("a number beyond 0 and 1", "X = 5\n"),
    refused("a float", "X = 0.5\n"),
    refused("a string that is no docstring", 'X = "abc"\n'),
    refused("a bare True", "X = True\n"),
    refused("an expression statement", fn("print(a)")),
    refused("an attribute off the list", fn("return a.real")),
    # the calls that are not on the list (sorted, the clamps, the comparisons under a name, a loop under a name)
    refused("a call of sorted", fn("return sorted(a)")),
    refused("a call of min", fn("return min(a, b)", "a, b")),
    refused("a call of max", fn("return max(a, b)", "a, b")),
    refused("a call of np.where", NP + fn("return np.where(a, b, b)", "a, b")),
    refused("a call of np.sign", NP + fn("return np.sign(a)")),
    refused("a call of np.argsort", NP + fn("return np.argsort(a)")),
    refused("a call of np.fromfunction", NP + fn("return np.fromfunction(a, b)", "a, b")),
    refused("a call of len", fn("return len(a)")),
    refused("a call of int", fn("return int(a)")),
    refused("a call of a parameter", fn("return g(a)", "g, a")),
    refused("a method off the list", fn("return a.sort()")),
    refused("a call of np.linalg.norm", NP + fn("return np.linalg.norm(a)")),
    refused("a call of np.add.at", NP + fn("return np.add.at(a, b, a)", "a, b")),
    refused("a call of an expression", "def g(a):\n    return a\n\n\ndef f(a):\n    return g(a)(a)\n"),
    refused("a keyword off the tensor four", NP + fn("return np.sum(a, out=a)")),
    refused("a double star in a call", "def g(a):\n    return a\n\n\ndef f(a):\n    return g(**a)\n"),
    refused("a string in a call that is no einsum's", fn('return g("a", a)', "g, a"), 2),
    # Rule3's floor division and remainder stand in the carry's home alone
    (
        "a floor division and a remainder elsewhere in the engine",
        NEW_MESH,
        fn("return a // b, a % b", "a, b"),
        {"ALLOW": 2, "OPERATION": 2},
    ),
    (
        "a floor division and a remainder in the readings",
        NEW_READING,
        fn("return a // b, a % b", "a, b"),
        {"ALLOW": 2, "OPERATION": 2},
    ),
    # the masks (and, or, not, &, |, ~) were counted nowhere: the engine and the readings refuse them, the readers still use them
    (
        "the masks in the new engine",
        NEW_STEP,
        fn("return (a and b), (a or b), (not a), (a & b), (a | b), (~a)", "a, b"),
        {"ALLOW": 6},
    ),
    (
        "the masks in the readings",
        NEW_READING,
        fn("return (a and b), (a or b), (not a), (a & b), (a | b), (~a)", "a, b"),
        {"ALLOW": 6},
    ),
    (
        "the masks in the runner",
        NEW_RUNNER,
        fn("return (a and b), (a or b), (not a), (a & b), (a | b), (~a)", "a, b"),
        {},
    ),
    (
        "the masks in the decoder",
        NEW_DECODER,
        fn("return (a and b), (a or b), (not a), (a & b), (a | b), (~a)", "a, b"),
        {},
    ),
    (
        "the masks in the current engine",
        "tick.py",
        fn("return (a and b), (a or b), (not a), (a & b), (a | b), (~a)", "a, b"),
        {},
    ),
]

CASES += [
    # the carry's home (the architect's design, eaf07f596): Rule3's // and % stand in algebra/carry.py alone
    (
        "a floor division and a remainder in the new carry's home",
        NEW_CARRY,
        fn("return a // b, a % b", "a, b"),
        {},
    ),
    (
        "a floor division and a remainder in the ring",
        NEW_RING,
        fn("return a // b, a % b", "a, b"),
        {"ALLOW": 2, "OPERATION": 2},
    ),
    (
        "a floor division and a remainder in the old carry's home",
        OLD_CARRY,
        fn("return a // b, a % b", "a, b"),
        {"ALLOW": 2, "OPERATION": 2},
    ),
    ("a floor division in the current engine's carry home", CARRY, fn("return a // b", "a, b"), {}),
    # algebra/ is strict and under the closed list
    ("a sum, a product and a pair in algebra", NEW_RING, fn("return a * b + a, a - b", "a, b"), {}),
    ("a branch in algebra", NEW_RING, fn("if a:\n    return a\nreturn a"), {"BRANCH": 1, "ALLOW": 1}),
    ("a loop in algebra", NEW_RING, fn("for x in a:\n    pass"), {"LOOP": 1, "ALLOW": 1}),
    (
        "an ordering comparison in algebra",
        NEW_RING,
        fn("return a < b", "a, b"),
        {"COMPARE": 1, "ALLOW": 1},
    ),
    ("a clamp in algebra", NEW_RING, fn("return min(a, b)", "a, b"), {"CLAMP": 1, "ALLOW": 1}),
    ("a raise in algebra", NEW_RING, fn("raise ValueError(a)"), {"REFUSE": 1, "ALLOW": 1}),
    ("a number beyond 0 and 1 in algebra", NEW_RING, "X = 5\n", {"NUMBER": 1, "ALLOW": 1}),
    # the architect's own functions (design section 2): choose and nonneg of algebra/ called by their names, the due bit's product over the
    # Spoke axis (np.prod); numpy's choose stays a clamp
    (
        "a lawful beat and due bit: the algebra's carry, nonneg and choose, np.prod over the Spoke axis",
        NEW_STEP,
        "import numpy as np\n"
        "from tensor24.algebra.carry import carry, choose, nonneg\n\n\n"
        "def due(counts, nb, here):\n"
        "    seen = np.take(counts, nb, axis=1)\n"
        "    return np.prod(nonneg(seen - here), axis=0)\n\n\n"
        "def beat(ph, rate, gamma):\n"
        "    return carry(rate, gamma, ph)\n\n\n"
        "def turnover(q, moved, same):\n"
        "    return choose(q, moved, same)\n",
        {},
    ),
    (
        "numpy's choose is still a clamp, and no list name",
        NEW_STEP,
        NP + fn("return np.choose(a, b)", "a, b"),
        {"CLAMP": 1, "ALLOW": 1},
    ),
    (
        "a bare choose in the current engine is still a clamp",
        ENGINE,
        "def f(a, b):\n    return choose(a, b)\n",
        {"CLAMP": 1},
    ),
    # the scattered sum of a contraction: np.add.at(out, index, values) as a statement of its own, on an array the function made
    (
        "a lawful scatter-add: np.add.at on a fresh array, a statement of its own",
        NEW_MESH,
        NP
        + "def scatter(rows, vals, shape):\n"
        + "    out = np.zeros(shape, dtype=object)\n"
        + "    np.add.at(out, rows, vals)\n"
        + "    return out\n",
        {},
    ),
    refused(
        "a scatter-add whose result is used", NP + fn("x = np.add.at(a, b, c)\nreturn x", "a, b, c")
    ),
    refused("a scatter-add with two arguments", NP + fn("np.add.at(a, b)\nreturn a", "a, b")),
    refused(
        "a scatter-add with a keyword", NP + fn("np.add.at(a, b, c, dtype=object)\nreturn a", "a, b, c")
    ),
    refused("a scatter-add into an element", NP + fn("np.add.at(a[0], b, c)\nreturn a", "a, b, c")),
    refused("another ufunc's at method", NP + fn("np.multiply.at(a, b, c)\nreturn a", "a, b, c")),
    refused(
        "a bare call statement of a function of the module",
        NP + "def g(a):\n    return a\n\n\n" + fn("g(a)\nreturn a"),
    ),
    # main.py is spared no rule (the architect's table: every rule but the imports): it passes the engine's functions into the
    # runner and holds no loop, branch, comparison, remainder or number
    (
        "a loop, a branch, a comparison and a remainder in main.py are refused",
        NEW_MAIN,
        fn("for x in a:\n    if x < a:\n        return x % a\nreturn a"),
        {"LOOP": 1, "BRANCH": 1, "COMPARE": 1, "OPERATION": 1},
    ),
    (
        "main.py imports the engine, the runner and the standard library",
        NEW_MAIN,
        "import json\nfrom tensor24.engine import step\nfrom tensor24.runner import loop\n",
        {},
    ),
    ("a number in main.py", NEW_MAIN, "X = 5\n", {"NUMBER": 1}),
    ("a float in main.py", NEW_MAIN, "X = 0.5\n", {"FLOAT": 1}),
    ("a float import in main.py", NEW_MAIN, "import math\n", {"IMPORT": 1}),
    ("a circle in main.py", NEW_MAIN, "def cosine_count(a):\n    return a\n", {"WORD": 1}),
    ("a container in main.py", NEW_MAIN, "SEEN = {}\n", {"STATE": 1}),
    (
        "an array with no dtype in main.py",
        NEW_MAIN,
        "import numpy as np\n\nX = np.zeros(1)\n",
        {"DTYPE": 1, "ISOLATE": 1},
    ),
    # the undo log is read by runner/rewind.py alone; the decoder reads the record; nothing else reads a log
    ("the undo log in runner/rewind.py", NEW_REWIND, fn("return a.log"), {}),
    ("the undo log elsewhere in the runner", NEW_RUNNER, fn("return a.log"), {"LOGREAD": 1}),
    ("a log read in the engine", NEW_STEP, fn("return a.log"), {"LOGREAD": 1}),
    ("a log read in algebra", NEW_RING, fn("return a.log"), {"LOGREAD": 1}),
    ("a log read in the readings", NEW_READING, fn("return a.log"), {"LOGREAD": 1}),
    ("a log read in the record", NEW_RECORD, fn("return a.log"), {"LOGREAD": 1}),
    ("a loop in runner/rewind.py", NEW_REWIND, fn("for x in a:\n    pass"), {}),
    # every array is made with dtype=object (Python integers, whatever their width): the architect's rule
    ("an array made with dtype=object", NEW_STEP, NP + fn("return np.zeros(a, dtype=object)"), {}),
    (
        "an array made like another, with dtype=object",
        NEW_STEP,
        NP + fn("return np.zeros_like(a, dtype=object)"),
        {},
    ),
    ("an array cast to object", NEW_STEP, fn("return a.astype(object)"), {}),
    refused("np.zeros with no dtype", NP + fn("return np.zeros(a)")),
    refused("np.zeros_like with no dtype", NP + fn("return np.zeros_like(a)")),
    refused("np.full with no dtype", NP + fn("return np.full(a, 0)")),
    refused("np.arange with no dtype", NP + fn("return np.arange(a)")),
    refused("np.eye with no dtype", NP + fn("return np.eye(a)")),
    refused("np.asarray with no dtype", NP + fn("return np.asarray(a)")),
    refused("np.array with a dtype that is not object", NP + fn("return np.array(a, dtype=int)")),
    refused(
        "np.zeros by name with no dtype", "from numpy import zeros\n\n\ndef f(a):\n    return zeros(a)\n"
    ),
    refused("astype to something else", fn("return a.astype(int)")),
    refused(
        "a dtype that is not object on the engine's own call",
        "def g(a, dtype=None):\n    return a\n\n\ndef f(a):\n    return g(a, dtype=int)\n",
    ),
]

# a branch and an ordering comparison are refusals in every engine module (Postulate 5); a cache is a refusal in the new engine's strict folders (engine, record, readings) and a note elsewhere
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
        "BLOCK",
    ),
    (
        "a branch in the current engine",
        "tick.py",
        "def f(a):\n    return a if a else a\n",
        "BRANCH",
        "BLOCK",
    ),
    (
        "a cache in the current engine stays a note",
        "tick.py",
        "from functools import cache\n\n\n@cache\ndef f(a):\n    return a\n",
        "MEMO",
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
    (
        "a cache in algebra",
        NEW_RING,
        "from functools import cache\n\n\n@cache\ndef f(a):\n    return a\n",
        "MEMO",
        "BLOCK",
    ),
    ("a comparison in algebra", NEW_RING, "def f(a, b):\n    return a < b\n", "COMPARE", "BLOCK"),
    ("a branch in algebra", NEW_RING, "def f(a):\n    return a if a else a\n", "BRANCH", "BLOCK"),
    (
        "a construct off the closed list in algebra",
        NEW_RING,
        "def f(a):\n    return a & a\n",
        "ALLOW",
        "BLOCK",
    ),
    (
        "a construct off the closed list in the new engine",
        NEW_STEP,
        "def f(a):\n    return a & a\n",
        "ALLOW",
        "BLOCK",
    ),
    (
        "a construct off the closed list in the readings",
        NEW_READING,
        "def f(a):\n    return a & a\n",
        "ALLOW",
        "BLOCK",
    ),
]

# the paths the architect's table names: the package's own file and main.py at the root, the six folders (nested modules of a folder stand);
# any other path has no wall written for it and is refused (the first hostile review's F2 on dce3c56bd)
CASES += [
    ("the package's own file holds a docstring alone", NEW_ROOT, '"""The package."""\n', {}),
    ("the package's own file imports the standard library", NEW_ROOT, "import json\n", {}),
    (
        "the package's own file imports the engine",
        NEW_ROOT,
        "from tensor24 import engine\n",
        {"ISOLATE": 1},
    ),
    (
        "the package's own file imports the runner",
        NEW_ROOT,
        "import tensor24.runner.loop\n",
        {"ISOLATE": 1},
    ),
    (
        "the package's own file imports the current engine",
        NEW_ROOT,
        "import event_universe\n",
        {"ISOLATE": 1},
    ),
    ("the package's own file imports numpy", NEW_ROOT, "import numpy as np\n", {"ISOLATE": 1}),
    (
        "a root module beside main.py",
        "tensor24/extra.py",
        '"""A module the table does not name."""\n',
        {"ISOLATE": 1},
    ),
    (
        "a root module that imports the engine and the runner",
        "tensor24/extra.py",
        "import tensor24.engine.step\nimport tensor24.runner.loop\n",
        {"ISOLATE": 1},
    ),
    (
        "a folder the table does not name",
        "tensor24/misc/tool.py",
        '"""A folder the table does not name."""\n',
        {"ISOLATE": 1},
    ),
    (
        "a nested module of a listed folder stands",
        "tensor24/engine/inner/deep.py",
        '"""A listed folder."""\n',
        {},
    ),
    (
        "main.py is a listed path",
        NEW_MAIN,
        '"""The one place that imports the engine and the runner."""\n',
        {},
    ),
]


# the new engine's tools, tools/tensor24_*.py (the Boss's word of 2026-10-28, 23:4x): the rules NUMBER and FLOAT alone, a path joined by
# pathlib's slash no division; the scope itself (the two tools and no other file under tools/) is tested through git below
CASES += [
    ("a tool: the literal 2 as an index", TOOL_DECODE, "def f(argv):\n    return argv[2]\n", {"NUMBER": 1}),
    ("a tool: the literals 2 and 3 in a membership test", TOOL_DECODE, "def f(argv):\n    return len(argv) not in (2, 3)\n", {"NUMBER": 2}),
    ("a tool: a return of 2", TOOL_DECODE, "def f(argv):\n    return 2\n", {"NUMBER": 1}),
    ("a tool: 3 in an equality", TOOL_FILES, "def f(argv):\n    return len(argv) == 3\n", {"NUMBER": 1}),
    ("a tool: 2 spelt as 1 + 1 stands", TOOL_FILES, "def f(argv):\n    return 1 + 1\n", {}),
    ("a tool: 0, 1 and -1 stand", TOOL_DECODE, "import sys\n\n\ndef f(argv):\n    sys.set_int_max_str_digits(0)\n    return argv[1], argv[-1:], 1 + 0\n", {}),
    ("a tool: a float literal", TOOL_FILES, "def f():\n    return 0.5\n", {"FLOAT": 1, "NUMBER": 1}),
    ("a tool: a complex literal", TOOL_FILES, "def f():\n    return 1j\n", {"FLOAT": 1, "NUMBER": 1}),
    ("a tool: a true division of two names", TOOL_FILES, "def f(a, b):\n    return a / b\n", {"FLOAT": 1}),
    ("a tool: a true division of 1 by a name", TOOL_FILES, "def f(a):\n    return 1 / a\n", {"FLOAT": 1}),
    ("a tool: an augmented true division", TOOL_FILES, "def f(a, b):\n    a /= b\n    return a\n", {"FLOAT": 1}),
    ("a tool: round()", TOOL_FILES, "def f(a):\n    return round(a)\n", {"FLOAT": 1}),
    ("a tool: pow()", TOOL_FILES, "def f(a, b):\n    return pow(a, b)\n", {"FLOAT": 1}),
    ("a tool: a path joined by pathlib's slash with strings", TOOL_FILES, 'from pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1] / "examples" / "tensor24"\n', {}),
    ("a tool: a path joined with an f-string", TOOL_FILES, 'def f(root, name):\n    return root / f"{name}.json"\n', {}),
    ("a tool: an augmented path join", TOOL_FILES, 'def f(root):\n    root /= "x"\n    return root\n', {}),
    ("a slash with a string is still a division in the code", ENGINE, 'def f(root):\n    return root / "x"\n', {"FLOAT": 1}),
    (
        "a tool: no other rule reads it (math, a loop, a branch, a raise, a clamp, a power, a remainder, a circular name)",
        TOOL_DECODE,
        "import math\n\n\ndef sine(a, b):\n    for x in a:\n        if x < b:\n            raise ValueError(x)\n    return min(a, b) ** b, a % b\n",
        {},
    ),
    ("a tool: a table of 0 and 1 is no table here", TOOL_DECODE, "X = (1, 0, 1)\n", {}),
]


IMPORTERS = {
    "root": NEW_ROOT,
    "algebra": NEW_RING,
    "engine": NEW_STEP,
    "record": NEW_RECORD,
    "readings": NEW_READING,
    "runner": NEW_RUNNER,
    "decoder": NEW_DECODER,
    "main": NEW_MAIN,
}
IMPORTED = {
    "stdlib": "import json\n",
    "numpy": "import numpy as np\n",
    "algebra": "from tensor24.algebra import carry\n",
    "engine": "from tensor24.engine import step\n",
    "record": "from tensor24.record import schema\n",
    "readings": "from tensor24.readings import wind\n",
    "runner": "from tensor24.runner import loop\n",
    "decoder": "from tensor24.decoder import rows\n",
    "current engine": "from event_universe import clock\n",
    "main": "from tensor24 import main\n",
}
# the architect's table: what each folder may import besides the standard library (and numpy, where it is named)
MAY_IMPORT = {
    "root": set(),
    "algebra": {"algebra"},
    "engine": {"algebra", "record", "engine"},
    "record": {"record"},
    "readings": {"algebra", "record", "readings"},
    "runner": {"algebra", "readings", "record", "runner"},
    "decoder": {"algebra", "record", "readings", "decoder"},
    "main": {"engine", "runner"},
}
# a module named by a string crosses a wall that reads import statements: each snippet's hits of ISOLATE in every folder of the new engine
DYNAMIC = (
    (
        "importlib.import_module",
        "import importlib\n\n\ndef f(n):\n    return importlib.import_module(n)\n",
        2,
    ),
    (
        "a from-import of import_module",
        "from importlib import import_module\n\n\ndef f(n):\n    return import_module(n)\n",
        2,
    ),
    ("__import__", "def f(n):\n    return __import__(n)\n", 1),
    ("exec", "def f(t):\n    exec(t)\n", 1),
    ("eval", "def f(t):\n    return eval(t)\n", 1),
    ("the builtin compile", "def f(t):\n    return compile(t, t, t)\n", 1),
    ("runpy", "import runpy\n", 1),
    ("pkgutil", "import pkgutil\n", 1),
)
NOT_DYNAMIC = (
    ("a regular expression's compile", "import re\n\n\ndef f(t):\n    return re.compile(t)\n"),
)
# the floor is the engine head the list that stands was taken at; moving it is a change of the list and goes with the owner's word
PINNED_FLOOR = "526a5666d"


@contextlib.contextmanager
def without_git_variables() -> Iterator[None]:
    """The git variables a hook exports (GIT_DIR, GIT_INDEX_FILE and the like) set aside: git then finds a repository by the path it is given."""
    aside = {name: os.environ.pop(name) for name in [n for n in os.environ if n.startswith("GIT_")]}
    try:
        yield
    finally:
        os.environ.update(aside)


def counts(rel: str, source: str) -> dict[str, int]:
    return dict(Counter(hit.rule for hit in gate.scan(rel, source)))


TOOL_NAMES = (
    ("tools/tensor24_files.py", True),
    ("tools/tensor24_decode.py", True),
    ("tools/tensor24_.py", True),
    ("tools/tensor24.py", False),
    ("tools/check.py", False),
    ("tools/xtensor24_files.py", False),
    ("tools/derivations/tensor24_files.py", False),
    ("tools/tensor24_files.pyc", False),
    ("tools/tensor24_files.py.orig", False),
    ("tools/tensor24_dir/files.py", False),
    ("src/tools/tensor24_files.py", False),
)


def tool_cases() -> tuple[int, int]:
    """The tools' scope through git and through the working tree, each check a case: tools/tensor24_*.py read and no other file under
    tools/, a push that changes a tool alone read, a tool moved no new hit; the cases made and those that parted."""
    made = parted = 0

    def check(label: str, ok: bool) -> None:
        nonlocal made, parted
        made += 1
        parted += not ok
        print(f"{'ok     ' if ok else 'PARTED '} the tools' scope: {label}")

    for name, want in TOOL_NAMES:
        check(f"{name} is {'a' if want else 'no'} tool", bool(gate.TOOLS.fullmatch(name)) == want)
    with without_git_variables(), tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        git = ["git", "-C", scratch, "-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid"]

        def run(*args: str) -> str:
            return subprocess.run([*git, *args], capture_output=True, text=True, check=True).stdout.strip()

        def commit(files: dict[str, str]) -> str:
            for name, text in files.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text, encoding="utf-8")
            run("add", "-A")
            run("commit", "-q", "-m", "selftest")
            return run("rev-parse", "HEAD")

        def read(rev: str) -> tuple[int, str]:
            out = io.StringIO()
            return gate.check_revision(root, rev, base, out), out.getvalue()

        def branch(name: str, files: dict[str, str]) -> str:
            run("checkout", "-q", "-B", name, base)
            return commit(files)

        run("init", "-q")
        base = commit(
            {
                "src/tensor24/__init__.py": '"""A package."""\n',
                "tools/tensor24_files.py": "def main():\n    return 1 + 1\n",
                "tools/tensor24_old.py": "def main():\n    return 2\n",
                "tools/tensor24_dir.py/inner.py": "def main():\n    return 3\n",
                "tools/check.py": "def main():\n    return 5\n",
                "tools/derivations/open_items/tensor24_probe.py": "def main():\n    return 7\n",
            }
        )
        tools = {"tools/tensor24_files.py", "tools/tensor24_old.py"}
        check(
            "through git the two tools are read, and no other file under tools/ (a folder named for one included)",
            {k for k in gate.sources_at(root, base) if k.startswith("tools/")} == tools,
        )
        check(
            "in the working tree the same two",
            {k for k in gate.sources_in(root) if k.startswith("tools/")} == tools,
        )
        check("the code under src is read beside them", "tensor24/__init__.py" in gate.sources_at(root, base))
        status, text = read(branch("literal", {"tools/tensor24_files.py": "def main():\n    return 3\n"}))
        check("a literal 3 in a tool is refused", status == 1 and "NUMBER" in text and "tools/tensor24_files.py" in text)
        status, text = read(branch("float", {"tools/tensor24_new.py": "def main():\n    return 0.5\n"}))
        check("a float in a new tool is refused", status == 1 and "FLOAT" in text and "tools/tensor24_new.py" in text)
        status, text = read(
            branch(
                "other",
                {
                    "tools/check.py": "def main():\n    return 9\n",
                    "tools/derivations/open_items/tensor24_probe.py": "def main():\n    return 11\n",
                },
            )
        )
        check("a push that changes no tool is not read", status == 0 and text == "")
        status, _ = read(branch("stands", {"tools/tensor24_old.py": "# kept\ndef main():\n    return 2\n"}))
        check("a literal that stands at the base stands", status == 0)
        status, text = read(branch("more", {"tools/tensor24_old.py": "def main():\n    return 2 + 2\n"}))
        check("a second literal above the one that stands is refused", status == 1 and "NUMBER" in text)
        run("checkout", "-q", "-B", "moved", base)
        run("mv", "tools/tensor24_old.py", "tools/tensor24_moved.py")
        run("commit", "-q", "-m", "moved")
        status, _ = read(run("rev-parse", "HEAD"))
        check("a tool moved is no new hit", status == 0)
        slash = 'from pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1] / "examples"\n'
        status, _ = read(branch("slash", {"tools/tensor24_files.py": slash}))
        check("a path joined by a slash is no division", status == 0)
        status, text = read(branch("division", {"tools/tensor24_files.py": "def main(a, b):\n    return a / b\n"}))
        check("a division of names in a tool is refused", status == 1 and "FLOAT" in text)
    return made, parted


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
    # the closed list holds in engine/ and readings/ alike and nowhere else: each refused snippet gives its hits in the readings too,
    # and none in the record, the runner, the decoder, the current engine and a package of another name
    closed_cases = 0
    elsewhere = (NEW_RECORD, NEW_RUNNER, NEW_DECODER, NEW_MAIN, "tick.py", ENGINE)
    for label, rel, source, want in CASES:
        if rel not in (NEW_STEP, NEW_MESH) or not want.get("ALLOW"):
            continue
        closed_cases += 3
        for folder, path in (("readings", NEW_READING), ("algebra", NEW_RING)):
            found = counts(path, source).get("ALLOW", 0)
            if found != want["ALLOW"]:
                parted += 1
                print(
                    f"PARTED  {label}: {folder} gave {found} hits of ALLOW, the engine {want['ALLOW']}"
                )
            else:
                print(f"ok      {label}: the same in {folder}")
        outside = {path: n for path in elsewhere if (n := counts(path, source).get("ALLOW", 0))}
        if outside:
            parted += 1
            print(f"PARTED  {label}: hits of ALLOW outside the engine and the readings: {outside}")
        else:
            print(
                f"ok      {label}: no hit of ALLOW in the record, the runner, the decoder, main.py and the current engine"
            )
    # the walls between the new engine's folders, restated from the architect's table (eaf07f596, section 4): every folder against every
    # package, forward and back; the standard library is allowed everywhere, numpy in the engine and the runner alone
    wall_cases = 0
    for importer, rel in IMPORTERS.items():
        for target, statement in IMPORTED.items():
            wall_cases += 1
            may = (
                target == "stdlib"
                or (target == "numpy" and importer in ("engine", "runner"))
                or target in MAY_IMPORT[importer]
            )
            crossed = any(hit.rule == "ISOLATE" for hit in gate.scan(rel, statement))
            if crossed == may:
                parted += 1
                print(
                    f"PARTED  wall: {importer} importing {target}: the architect's table says {'yes' if may else 'no'}"
                )
    print(f"ok      the walls: {wall_cases} imports, every folder and the root against every package")
    # a module named by a string: the loaders and the calls that import or run text are refused in every folder of the new engine, the
    # root included, and a regular expression's compile or a loader outside the new engine is not (the fourth hostile review's follow-up)
    dynamic_cases = 0
    for importer, rel in IMPORTERS.items():
        for label, source, want in DYNAMIC:
            dynamic_cases += 1
            got = counts(rel, source).get("ISOLATE", 0)
            if got != want:
                parted += 1
                print(
                    f"PARTED  dynamic import: {label} in {importer} gave {got} hits of ISOLATE, wanted {want}"
                )
        for label, source in NOT_DYNAMIC:
            dynamic_cases += 1
            if counts(rel, source).get("ISOLATE", 0):
                parted += 1
                print(f"PARTED  dynamic import: {label} in {importer} is no dynamic import")
    for label, source, _ in DYNAMIC:
        dynamic_cases += 1
        if counts("run.py", source).get("ISOLATE", 0) or counts(ENGINE, source).get("ISOLATE", 0):
            parted += 1
            print(f"PARTED  dynamic import: {label} outside the new engine is refused")
    print(
        f"ok      dynamic imports: {dynamic_cases} cases, every folder and the root against the loaders and the calls that run text"
    )
    # the floor: a merge base older than the floor, on its own line, is read as the floor; one at or after it, or beside it, is read as found (the first hostile
    # review's F1 and the fourth's follow-up)
    floor_cases, kept_floor = 1, gate.FLOOR
    if kept_floor != PINNED_FLOOR:
        parted += 1
        print(
            f"PARTED  the floor is {kept_floor}, the engine head the list that stands was taken at is {PINNED_FLOOR}"
        )
    else:
        print(f"ok      the floor is {PINNED_FLOOR}, the engine head the list that stands was taken at")
    # a hook exports GIT_DIR and the like, and git then reads and writes the repository they name whatever path it is given: the section's
    # scratch repository is found by its path alone, with the git variables set aside, and a repository standing in for the one a hook
    # would name (GIT_DIR exported to it) must come out of the section with no commit in it
    with tempfile.TemporaryDirectory() as bait:
        with without_git_variables():
            subprocess.run(["git", "-C", bait, "init", "-q"], check=True)
        exported = os.environ.get("GIT_DIR")
        os.environ["GIT_DIR"] = f"{bait}/.git"  # as a hook exports it
        try:
            with without_git_variables():
                with tempfile.TemporaryDirectory() as scratch:
                    git = [
                        "git",
                        "-C",
                        scratch,
                        "-c",
                        "user.name=selftest",
                        "-c",
                        "user.email=selftest@example.invalid",
                    ]

                    def commit(message: str) -> str:
                        subprocess.run(
                            [*git, "commit", "-q", "--allow-empty", "-m", message], check=True
                        )
                        return subprocess.run(
                            [*git, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
                        ).stdout.strip()

                    subprocess.run([*git, "init", "-q"], check=True)
                    old, mid, new = commit("old"), commit("floor"), commit("new")
                    subprocess.run([*git, "checkout", "-q", "-b", "side", old], check=True)
                    side = commit("side")  # a line the floor is not part of
                    subprocess.run([*git, "checkout", "-q", "-b", "joined", new], check=True)
                    subprocess.run([*git, "merge", "-q", "--no-ff", "-m", "joined", side], check=True)
                    joined = subprocess.run(
                        [*git, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
                    ).stdout.strip()
                    gate.FLOOR = mid
                    for label, found, tree, want in (
                        ("older than the floor, the tree holding it", old, new, mid),
                        ("at the floor", mid, new, mid),
                        ("after the floor", new, new, new),
                        ("older than the floor, the tree not holding it", old, old, old),
                        ("beside the floor, on a line the floor is not part of", side, joined, side),
                        ("older than the floor, the tree joining a line beside it", old, joined, mid),
                    ):
                        floor_cases += 1
                        got = gate.floored(Path(scratch), found, tree)
                        if got != want:
                            parted += 1
                            print(
                                f"PARTED  the floor: a merge base {label} gave {got[:9]}, wanted {want[:9]}"
                            )
                        else:
                            print(f"ok      the floor: a merge base {label}")
                    # the merge base itself, through merge_base: never the tree, the base's own merge base, lifted to the floor only from behind it
                    for label, base, tree, want in (
                        (
                            "a base older than the floor, the tree holding it: lifted to the floor",
                            old,
                            new,
                            mid,
                        ),
                        (
                            "the base ahead of a side line: the common ancestor, not the tree",
                            new,
                            side,
                            old,
                        ),
                        (
                            "the base a side line the tree joined: that line's commit, not the tree",
                            side,
                            joined,
                            side,
                        ),
                        ("the base the tree holds: the base, not the tree", new, joined, new),
                    ):
                        floor_cases += 1
                        _, kept = gate.merge_base(Path(scratch), base, tree)
                        if kept != want:
                            parted += 1
                            print(f"PARTED  merge_base: {label} gave {kept[:9]}, wanted {want[:9]}")
                        else:
                            print(f"ok      merge_base: {label}")
        finally:
            if exported is None:
                os.environ.pop("GIT_DIR", None)
            else:
                os.environ["GIT_DIR"] = exported
        gate.FLOOR = kept_floor
        floor_cases += 1
        with without_git_variables():
            left = subprocess.run(
                ["git", "-C", bait, "rev-list", "--all"], capture_output=True, text=True, check=True
            ).stdout
        if left.strip():
            parted += 1
            print(
                "PARTED  the floor: the scratch repository wrote into the repository a hook's GIT_DIR names"
            )
        else:
            print(
                "ok      the floor: the scratch repository is found by its path, a hook's GIT_DIR names none of it"
            )
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
    tool_total, tool_parted = tool_cases()
    parted += tool_parted
    print(
        f"selftest: {len(CASES) + tier_cases + closed_cases + wall_cases + dynamic_cases + floor_cases + tool_total + 2} cases, {parted} parted"
    )
    return 1 if parted else 0


if __name__ == "__main__":
    sys.exit(main())
