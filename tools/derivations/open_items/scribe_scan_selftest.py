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

CASES: list[tuple[str, str, str, dict[str, int]]] = [
    ("a for loop", ENGINE, "def f(a):\n    for x in a:\n        pass\n", {"LOOP": 1}),
    ("a while loop", ENGINE, "def f(a):\n    while a:\n        a = 0\n", {"LOOP": 1}),
    (
        "two comprehensions on one line",
        ENGINE,
        "def f(a):\n    return [x for x in a], {y for y in a}\n",
        {"LOOP": 2},
    ),
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
    print(f"selftest: {len(CASES) + 2} cases, {parted} parted")
    return 1 if parted else 0


if __name__ == "__main__":
    sys.exit(main())
