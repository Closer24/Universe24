"""Part D, Task 3, gate (1): no root anywhere (the owner, issue #1793, comments 6077053307 and 6077234684: "no root anywhere"; "is there a test that checks this?"). No .py of src/event_universe names `division_fixed_point`, `isqrt`, `sqrt` or `math.sqrt` as a token of the code, and no power `** 0.5` stands in any expression; the gate reads the tree recursively and names the file and line of every hit. The sister gates: no shear and no rotation act, tests/test_rule3.py (`test_no_shear_and_no_name_of_features_rotation_remains_in_src`); the acts table, tests/test_the_acts_table.py."""

import ast
import io
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "event_universe"
ROOT_NAMES = frozenset({"division_fixed_point", "isqrt", "sqrt"})


def test_no_root_anywhere_in_src():
    """No identifier `division_fixed_point`, `isqrt`, `sqrt` (so no `math.sqrt`, `np.sqrt` or a bare call) in the tokens of any .py of src (strings and comments aside, `tokenize`), and no `** 0.5` or `**0.5` (an `ast.Pow` whose right side is the float 0.5, which the float gate refuses too): the largest integer whose square is at most a count is `rule3.largest_below`, a search by comparisons of products, and nothing else."""
    hits = []
    for path in sorted(SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        name = path.relative_to(ROOT).as_posix()
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.NAME and token.string in ROOT_NAMES:
                hits.append(f"{name}:{token.start[0]} {token.string}")
        for item in ast.walk(ast.parse(text)):
            if isinstance(item, ast.BinOp) and isinstance(item.op, ast.Pow):
                right = item.right
                if isinstance(right, ast.Constant) and type(right.value) is float:
                    hits.append(f"{name}:{item.lineno} ** {right.value!r}")
    assert not hits, hits
    assert "largest_below" in (SOURCE / "core" / "rule3.py").read_text(encoding="utf-8")
