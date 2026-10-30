"""Sofer's gate on every package under src and the new engine's tools: the owner's rules as a script that refuses a push.

The owner's words of 2026-10-28, 04:3x, 04:5x and 05:0x UTC: no number in the code, whole numbers only, no cosine, sine or
circularity that makes a phenomenon happen, no state beyond the Node-clock; "your laws should be in scripts, so that they cannot
push at all what breaks our lawfulness, and let it be logical and smart".

How it decides. A push may not raise the count of any rule's hits, at any (rule, file, detail), above the same file's at the push's
merge base: what stands at the base stands, a new hit is a REFUSAL (BLOCK) or a NOTE (WARN) by the rule's tier. A hit leaves the list
by being removed and enters it only by the owner's word (scribe_scan_allowed.json, written by Sofer on that word, with the
row of the ledger that holds it). The key of a hit holds no line number, so a moved or reformatted line is no new hit. A note of
the rule KEYS (a key added to the files' format) leaves the list when Sofer has read the key through the law and listed it in
scribe_scan_keys.json, read from his published branch as the allowance is.

The ceiling. What stands at the merge base stands, so a fake that a stage of the new engine deletes could come back up to the base's own count (the merge
base holds an early Tensor24). For the rules that the stages delete (CEILED) in the new engine's src, the base's count is capped at the ceiling,
scribe_scan_ceiling.json: the most that stands per key at a live head, written by Sofer from the live heads, never raised, read from his published
branch as the allowance is. A hit above it is new; a key the ceiling does not hold stands at 0.

The hidden numbers and the probes (the owner's answers of 2026-10-30, 09:0x UTC). ENUM (a refusal) and LENGTH (a note) read the new engine and its tools for
a number behind a name: an enumeration, and a count spelt as a length. PROBE (a refusal) and DIVIDE (a note) read the probes under tools/derivations/ that a push
adds or changes: a float, a true division, a root, a circular call, an import of math, random, fractions, decimal, statistics, scipy or sympy (PROBE); a floor
division, a remainder or divmod, where the one division is Rule3's carry (DIVIDE). SEARCH (a note) reads the three shapes under which a probe makes a circular or
logarithmic function or a root without a call that names it: a series summed by a loop, a bracket halved by its midpoint, and a function or constant named a sine,
cosine, tangent, arctangent, artanh or ln (David's finding of 6528139344 item 5). The probes that stood at the live heads of 2026-10-30, 09:5x UTC are frozen in
scribe_scan_probes.json, read from the published branch as the ceiling is. SCRIBE-GATE-1.md, section The hidden numbers and the probes.

  python scribe_scan.py                        the working tree against its merge base (CHECK_BASE, else origin/engine-5.0-test)
  python scribe_scan.py TREE [--base REV]      TREE a directory or a git revision; the base a revision
  python scribe_scan.py --patch FILE           the patch applied on the base in a scratch worktree, then the same check
  python scribe_scan.py TREE --baseline FILE   the tree against the list of departures that stand (Sofer's audit of the whole)
  python scribe_scan.py TREE --all [--summary] every hit of the tree, by rule and file (--summary: the counts only)
  python scribe_scan.py --write-baseline FILE  [TREE]  the tree's hits written as the list that stands
  python scribe_scan.py --rules                the rules, their tiers and the law each one keeps
  python scribe_scan.py --install              the git pre-push hook of this clone
  python scribe_scan.py --hook                 git's pre-push call (the refs on stdin); --claude-hook: Claude Code's call before `git push`

The rule DECLARE reads data besides code: the families, trains and couplings a universe file names (.json) and the dicts of a train written with a name and a
pinion (.py), under examples, reader, tests, tools and src, in the files a push changes alone; a declaration a push adds over its merge base is a refusal unless the
owner's list holds it (decision 35: nothing is declared), and a train at pinion = den is the seed and no declaration.

Exit status 1 on a refusal, 0 otherwise (2: the call itself is wrong). Read with the repository's own interpreter, Python 3.14
(venv314/bin/python); an older one runs the script again under it.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import keyword
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tokenize
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Any

PACKAGE = "src/event_universe"
TESTS = "tests"
SCOPES = ("src", TESTS)  # every package under src, and the tests for the rule PIN alone
TOOLS = re.compile(
    r"tools/tensor24_[^/]*\.py"
)  # the new engine's tools, directly under tools/: the rules of TOOL_RULES alone
TOOLS_SPEC = ":(glob)tools/tensor24_*.py"  # the same files as git's pathspec
TOOL_RULES = frozenset(
    {"NUMBER", "FLOAT", "TWICE", "ROOT", "TABLE", "ENUM", "LENGTH"}
)  # no number beyond 0 and 1, no float, no two spelt as a sum, no root and no typed table, no enumeration and no count spelt as a length, in a tool as in the code (the Boss's word of 2026-10-28, 23:4x; the owner's "Forbidden" of 2026-10-29, 12:5x; decision 41, 2026-10-30, 02:1x: no root and no table, now or later, and not outside the logic either; the owner's question of 2026-10-30, 09:0x: no number hidden behind an enum)
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASELINE = HERE / "scribe_scan_baseline.json"
ALLOWED = HERE / "scribe_scan_allowed.json"
CEILING = (
    HERE / "scribe_scan_ceiling.json"
)  # the most that stands per key at a live head: what a stage deleted cannot return up to the base's count
KEYS_READ = (
    HERE / "scribe_scan_keys.json"
)  # the keys of the files' format that Sofer has read through the law, 'KEYS|file|path' per line
PROBES_LIST = (
    HERE / "scribe_scan_probes.json"
)  # the probes that stand: per key the most a probe holds at a live head, frozen on the owner's yes of 2026-10-30, 09:0x UTC (the rule PROBE)
BASES = ("origin/engine-5.0-test", "origin/main")
FLOOR = "526a5666d"  # the engine head the list that stands was taken at: no base is older (a pull request into main is read against it)
PUBLISHED = "origin/scribe-5"  # where the owner's approvals stand, written by Sofer alone
# the rule DECLARE reads the files a universe or a world is declared in, besides the code
DECLARED_SCOPES = ("examples", "reader", "tests", "tools", "src")
DECLARED_SKIP = frozenset({".git", "node_modules", "venv314", "__pycache__"})
DECLARED_LISTS = (
    ("families", "family"),
    ("trains", "train"),
    ("couplings", "coupling"),
)  # the lists of a universe file that declare
DECLARED_GEAR = (
    "pinion",
    "pair",
    "ratio",
)  # the key that carries the number a declaration stands for, the first an entry holds
# the gate's own files: a push that changes one needs the owner's word, and says so
OWN = (
    "tools/derivations/open_items/scribe_scan.py",
    "tools/derivations/open_items/scribe_scan_selftest.py",
    "tools/derivations/open_items/scribe_scan_allowed.json",
    "tools/derivations/open_items/scribe_scan_ceiling.json",
    "tools/derivations/open_items/scribe_scan_keys.json",
    "tools/derivations/open_items/scribe_scan_probes.json",
    "tools/derivations/open_items/scribe_scan_baseline.json",
    ".claude/settings.json",
)

# rule: (tier, the line the refusal prints with the law it keeps)
RULES: dict[str, tuple[str, str]] = {
    "NUMBER": (
        "BLOCK",
        "a number beyond 0 and 1: numbers stand in the world, universe and setting files, in the code and in tools/tensor24_*.py (law: No number in the code)",
    ),
    "FLOAT": (
        "BLOCK",
        "a float, a true division, round() or pow(): whole numbers only, in the code and in tools/tensor24_*.py (law: No float anywhere in the system)",
    ),
    "IMPORT": (
        "BLOCK",
        "math, random, fractions, decimal, statistics, scipy, sympy: integers and Rule3 only (law: No float anywhere)",
    ),
    "DTYPE": (
        "BLOCK",
        "a numpy constructor with no dtype makes a float (law: No float anywhere in the system)",
    ),
    "CIRCLE": (
        "BLOCK",
        "a cosine, sine, tangent, pi or other circular function (law: No circularity that makes a phenomenon happen)",
    ),
    "ROOT": (
        "BLOCK",
        "a call of an integer root, the integer sine by search: no new call (law: No circularity that makes a phenomenon happen)",
    ),
    "MASK": (
        "BLOCK",
        "a selection by a condition in the act, the loader or main.py: an array indexed by a comparison or a boolean expression, or np.flatnonzero, nonzero, argwhere, compress, extract: a mask is an if spelt as an index; where the weights are 0 or 1 a product does the work (Postulate 5: no mask; no train is told from another by a condition)",
    ),
    "BOOKS": (
        "BLOCK",
        "the word book in a name, an attribute, a keyword, an import alias or a string of the engine, its loader, its runner or main.py: no store of accounts beside the state; a push is read by the tensor operation from the state of every gear (law: No books in the engine)",
    ),
    "SPECIAL": (
        "BLOCK",
        "a name, an attribute, a keyword, an import alias or a string (a docstring spared) in the act, the loader or main.py that names a link's lengthening or shortening, a decoupling, a horizon, a clock's freezing or restoring, or a link's sending, receiving, emitting or absorbing: no special function, key or branch for any of them; they are the one act's own results (law: No special code and no specific law for a clock or a link, line 90)",
    ),
    "WORD": (
        "BLOCK",
        "a circular word in a name (cosine, sine, angle, theta, circle, quaternion ...): an angle or circle used as a rule",
    ),
    "TEXT": (
        "WARN",
        "a circular word in a string, docstring or comment: read it, a rotation or a closed form may be described there",
    ),
    "STATE": (
        "BLOCK",
        "state outside a Node-clock: a module-level container, a global, an id() key (law: Locality is never broken)",
    ),
    "MEMO": (
        "WARN",
        "a module-level cache is state beyond the Node-clock: only a pure function of integers may stand so, and say it",
    ),
    "TABLE": (
        "BLOCK",
        "a typed table of integers in the code (a quarter turn, a singlet): a world's data stands in the world file",
    ),
    "MIX": (
        "BLOCK",
        "a tuple of bilinear sums: a rotation or hypercomplex product by a setting outside Rule3 (law: No circularity ...)",
    ),
    "LOGREAD": (
        "BLOCK",
        "an act reads the great clock's log, a global read: only the readers read the record, and the runner reads the undo log in runner/rewind.py alone (law: Locality is never broken)",
    ),
    "LOOP": (
        "BLOCK",
        "a loop (for, while, a comprehension, map, filter, reduce, itertools, np.vectorize, a function that calls itself) in an engine module, and in the new engine's runner/board.py and runner/load.py: no loop that makes a formula, the machine is one tensor operation (the owner's words of 2026-10-28, 06:5x and 09:0x); the count per file and kind may not rise",
    ),
    "OPERATION": (
        "BLOCK",
        "a power, a shift, an exclusive or, or a floor division or remainder outside the carry's home (core/acts.py, core/rule3.py, and tensor24/algebra/carry.py in the new engine; the new engine's runner/board.py and runner/load.py write none of it, its wrap being the carry imported from there): the step does multiplication, addition and Rule3 alone (the owner's word of 2026-10-28, 09:0x); the same under a method's name (a.__mod__(b)), a name imported or aliased from numpy or operator, a getattr of an operation's name, and, in runner/board.py, numpy's own wraps (roll, pad, a call with mode=)",
    ),
    "TWICE": (
        "BLOCK",
        "a two spelt as a sum: an expression added to itself (1 + 1, teeth + teeth, spokes + spokes) in any module of the new engine, the runner and the decoder included, and in tools/tensor24_*.py: the rule NUMBER counts literals, so a thing added to itself is a 2 in disguise (the owner's word of 2026-10-29, 12:5x: forbidden); the count per file and spelling may not rise",
    ),
    "REFUSE": (
        "BLOCK",
        "a raise in an engine module, and in the new engine's runner/load.py: a refusal by name is a rule written for a phenomenon (the exclusion's refusals were such); the count per file may not rise (the owner's word of 2026-10-28, 09:0x: no declarations)",
    ),
    "CLAMP": (
        "BLOCK",
        "min, max, abs, clip or where in an engine module, and in the new engine's runner/board.py and runner/load.py: a bound or a branch written as a clamp, where the step does multiplication, addition and Rule3 alone (the owner's word of 2026-10-28, 08:0x, through David)",
    ),
    "PIN": (
        "WARN",
        "an assert against an integer beyond 0 and 1 in a test: a pinned value is a verdict the code wrote; the plan's tests read properties and two independent readings (the count per file may not rise)",
    ),
    "COMPARE": (
        "BLOCK",
        "an ordering comparison in an engine module, and in the new engine's runner/board.py and runner/load.py: a threshold read by order and not as the quotient of a carry (Postulate 5: the Node-clock has no if; the owner's word of 2026-10-28, 12:5x); the count per file may not rise",
    ),
    "ISOLATE": (
        "BLOCK",
        "an import that crosses the new engine's folders (the architect's table, eaf07f596; the standard library is always allowed): algebra imports algebra alone (no numpy), engine algebra, record and numpy, record the record alone (no numpy), readings algebra, record and readings (no numpy), runner algebra, readings, record and numpy (never the engine or the decoder: the step is passed in), decoder algebra, readings and record (never the engine, the runner or numpy), tensor24/main.py the engine and the runner alone, tensor24/__init__.py the standard library alone; a module at an unlisted path (directly under tensor24/ beside __init__.py and main.py, or in a folder the table does not name) has no wall written for it and is refused; a loader (importlib, runpy, imp, pkgutil, zipimport) imported, or a call that imports or runs text by a string (__import__, import_module, exec, eval, the builtin compile), in any folder of the new engine, since a module named by a string crosses a wall that reads import statements; nothing imports the current engine; a judge that runs the defendant's code cannot catch it (the owner's word of 2026-10-28, 10:1x: the decoder out of the engine)",
    ),
    "BRANCH": (
        "BLOCK",
        "a branch (if, a conditional expression, match) in an engine module, and in the new engine's runner/board.py and runner/load.py: the Node-clock has no if (Postulate 5; the owner's word of 2026-10-28, 12:5x: enforce it, never cross it; also The Node-clock and the Mesh are generic; there is no if), and a whether is Rule3's quotient (n < d exactly where the quotient of n by d is 0; the sign test [x >= 0] = 1 + x div (x x + 1)); a branch the formula does not hold is a declaration (the count per file may not rise)",
    ),
    "INDICATOR": (
        "WARN",
        "a quotient spelt as a mask or a cap (the quotient of a bit, 1 div x; 1 minus a quotient; the sign test x div (x x + 1)): an indicator that zeroes a term above a bound is a bound spelt as a quotient, and a floor or a bound is an if (law: A floor or a bound is an if, and the Node-clock has none); read each note for a mask (the count per file may not rise)",
    ),
    "BOUND": (
        "WARN",
        "a name that holds a floor, a bound, a clamp or a cap (floor, ceiling, cap, clamp, clip, limit, bound, saturate): no act, tool or reading of the system holds one (law: A floor or a bound is an if, and the Node-clock has none); a reader may name one to report; read each note (the count per file may not rise)",
    ),
    "KEYS": (
        "WARN",
        "a key added to the files' format (a string in the module-level collections of runner/files.py): each key is a name or a number a file may declare, and a key near the time gear is what Postulate 6 refuses (law: Postulate 6; The principle of the clock and the gear); read each note through the law; the keys Sofer has read stand in scribe_scan_keys.json on origin/scribe-5, so an unread key alone is a note",
    ),
    "INDEX": (
        "WARN",
        "a cast to numpy's index type as a gather's index (astype(np.intp) directly in take or in a subscript) in algebra/, engine/ or readings/, the one cast the closed list names: numpy gathers by an index of integer type and the engine's integers are Python integers in arrays of dtype=object; the cast is the identity on a whole number that fits the index type and an OverflowError on one that does not, so it changes no value and is no operation of the act (law: The Node-clock is one act, one gather; The rates compose, the count bounded by the width alone); read each note through the law at the push: the count it casts is held within the table's length by nonneg at both ends, and the cast is never a gear's value or kept in a name",
    ),
    "ALLOW": (
        "BLOCK",
        "not on the Node-clock's closed list: its only operations are addition, multiplication and Rule3's carry, on whole numbers (the owner's idea of 2026-10-28, 15:0x UTC; law: The Node-clock is one act; The Node-clock and the Mesh are generic; there is no if), so a construct, an operator, a call or an array not made with dtype=object that the list does not name is refused in algebra/, engine/ and readings/, and in runner/board.py against a list of its own (numpy's arange and stack, the index dtype np.intp, list displays); the architect's additions go through Sofer by a ledger entry that names the law line each serves (the count per file may not rise)",
    ),
    "DECLARE": (
        "BLOCK",
        "a family, a train or a coupling named in a universe file or in a world's code, with its pair, pinion or strength: no particle, mass or coupling is declared in any file (law: Nothing is declared: every particle appears by itself in the clicks; the owner's word of 2026-10-29, 10:54, decision 35); a train at pinion = den is the seed and declares no mass; the declarations that stand are on the owner's list (scribe_scan_allowed.json) as named breaches until the clicks build the particles, and a new one, or a changed number, is refused",
    ),
    "CHOOSE": (
        "BLOCK",
        "a call of choose or nonneg in the new engine's act (tensor24/engine) or its loader (runner/load.py): choose(k, x, y) = k x + (1 - k) y is an if spelt as arithmetic, a mask by a bit, and nonneg is a floor; the Node-clock has no if, no mask and no clamp (Postulate 5; the owner's word of 2026-10-29, 15:0x UTC, to David: no floors or bounds, no if; David's audit of tensor24-review 058512b2b, F8); the count per file may not rise",
    ),
    "POSITION": (
        "BLOCK",
        "a name indexed by a constant integer (trains[-1], rows[0]) in the new engine's act or its loader: a family found by its place in a list is a row apart (law: A gear like every gear; decision 38; the owner's word of 2026-10-29, 15:0x UTC: the code does not know what the families are); an array's dimension (x.shape[-1]) and a pair picked out of a call's result are no family; the count per file may not rise",
    ),
    "FAMILY": (
        "BLOCK",
        "a family's kind or operand named by a string ('A1', 'A2', 'E', 'T1', 'T2', 'gradient') in the new engine's act or its loader: the files name each family and the code reads every role from them (decision 38; the owner's word of 2026-10-29, 15:0x UTC: make sure the code does not know what the families are); the count per file may not rise",
    ),
    "ENUM": (
        "BLOCK",
        "an enumeration in the new engine or its tools (import enum, a class of Enum, IntEnum, StrEnum, Flag or IntFlag, enum.auto()): a number behind a name; numbers stand in the world, universe and setting files (the owner's question of 2026-10-30, 09:0x UTC: no number hidden behind an enum)",
    ),
    "LENGTH": (
        "WARN",
        "len() of a label tuple, a literal display or an all-capitals constant in the new engine or its tools: a count behind a name, a number spelt as a length (the owner's question of 2026-10-30, 09:0x UTC: no number hidden behind an enum and such); read each note, and derive the count from the star or the files (the count per file may not rise)",
    ),
    "PROBE": (
        "BLOCK",
        "a probe under tools/derivations/ that a push adds or changes holds a float, a true division, a root or a circular call, round() or float(), a negative power, a float dtype, or an import of math, random, fractions, decimal, statistics, scipy, sympy: whole numbers and Rule3 only, in a probe as in the code (law: No float anywhere in the system; the owner's words of 2026-10-30, 09:0x UTC: 'Yes' to the gate for probes, and a Fraction is two whole numbers while division is allowed only with Rule3); the probes that stand are frozen by scribe_scan_probes.json and the owner's list",
    ),
    "DIVIDE": (
        "WARN",
        "a floor division, a remainder or divmod in a probe under tools/derivations/ that a push adds or changes: the one division is Rule3's carry with its remainder kept (tensor24.algebra.carry.carry) (the owner's word of 2026-10-30, 09:0x UTC: division is allowed only with Rule3); a note, the count per file may not rise",
    ),
    "SEARCH": (
        "WARN",
        "a circular or logarithmic function, or a root, made by hand in a probe under tools/derivations/ that a push adds or changes, under a name that is no call of one: a loop that sums a series (a term updated by a division by an expression of the loop's counter, by // or by carry, and added to a total), a bracket halved (the midpoint of two ends, (lo + hi) // 2 with or without a one added, a shift by one or a carry of the sum by 2), and a function or constant named a sine, cosine, tangent, arctangent, artanh or ln (sine, cosine, arctan_inverse, artanh_inverse, LN_TWO): the law has no circular function that makes a phenomenon happen (line 102), no logarithm in a derivation (line 100) and no root found by search (decision 41), and a series or a bisection makes them under another name (David's finding of 2026-10-30, 16:4x UTC, #2187 6528139344 item 5; the writer's take, 6528504490); a note, the count per file may not rise, and a refusal when the owner answers whether a series used only to lay a state falls under line 102",
    ),
    "DOCLAYER": (
        "BLOCK",
        "a module of the new engine whose docstring lacks the four layers, Clock:, Algebra:, Board: and Clicks:, each at the start of a line and carrying a text or the one general flag n/a: a part is told in the clock, the algebra, the event board and the physics behind the clicks (law: item (10) (e) of the principle, line 35; the owner's word of 2026-10-30, 11:0x UTC); the standing modules convert and the count only falls",
    ),}

BAD_IMPORTS = frozenset("math cmath statistics random fractions decimal scipy sympy mpmath".split())
NUMPY_NAMES = frozenset({"np", "numpy"})
DISPLAY_NODES = (ast.Tuple, ast.List, ast.Set, ast.Dict)  # a label tuple, a list, a set or a dict written out
LAYERS = ("Clock", "Algebra", "Board", "Clicks")  # the four layers a part of the new engine states in its docstring (the rule DOCLAYER)
ENUM_NAMES = frozenset("Enum IntEnum StrEnum Flag IntFlag ReprEnum auto".split())  # the standard library's enumerations: a number behind a name
PROBES = "tools/derivations/"  # the probes (the derivations, toys and hands under it): the rules PROBE and DIVIDE read the files a push adds or changes
PROBE_CALLS = frozenset(
    "sqrt isqrt cbrt exp expm1 log log1p log2 log10 sin cos tan asin acos atan atan2 arcsin arccos arctan arctan2 sinh cosh tanh "
    "arcsinh arccosh arctanh hypot round float complex".split()
)  # a call that makes a real number, a root or a circular function in a probe
SEARCH_WORDS = frozenset(
    "sin cos tan sine cosine tangent arctan arcsin arccos atan asin acos artanh atanh arctanh arcsinh ln".split()
)  # a word of a snake_case name that makes a circular or logarithmic function by hand (the rule SEARCH): log is no word of it, a log being also a record
PROBE_DTYPES = frozenset(
    "float complex float16 float32 float64 float128 float_ double longdouble complex64 complex128 complex256".split()
)  # a dtype that holds a real number
PATHISH = (
    "path", "root", "dir", "here", "repo", "folder", "tmp", "parent", "examples", "output", "work",
)  # a name that holds a path: its / is a join, the left side of a division in a probe that this spares
NP_FLOAT = frozenset(
    "sqrt cbrt exp expm1 log log2 log10 log1p mean average median std var linspace logspace fft linalg random e inf nan "
    "float16 float32 float64 float_ double true_divide divide power complex_ complex64 complex128 complex256 csingle cdouble "
    "clongdouble floor ceil trunc rint around round fix".split()
)
CIRCULAR_FUNCTIONS = frozenset(
    "cos sin tan acos asin atan atan2 arccos arcsin arctan arctan2 sinh cosh tanh radians degrees deg2rad rad2deg "
    "hypot unwrap angle".split()
)
ROOTS = frozenset("largest_below isqrt integer_root sqrt cbrt sine_rim".split())
CLAMPS = frozenset(
    "min max abs clip where minimum maximum absolute fmin fmax sign select piecewise choose heaviside copysign".split()
)
QUOTIENT_CALLS = frozenset(
    "carry carries signed_carries quotient div floordiv floor_divide".split()
)  # the carry's quotient under a function's name (the indicator is made of one)
BOUND_WORDS = frozenset(
    "floor floors ceiling cap capped clamp clamped clip clipped limit limits limited bound bounds bounded "
    "saturate saturated saturation".split()
)  # the words of a name that holds a floor or a bound
ORDERING = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
FOREIGN_OPERATORS = {ast.Pow: "**", ast.LShift: "<<", ast.RShift: ">>", ast.BitXor: "^"}
OPERATION_CALLS = frozenset(
    "divmod floor_divide remainder mod fmod left_shift right_shift bitwise_xor floordiv lshift rshift xor".split()
)  # the foreign operations under their function names (np.mod, operator.xor ...)
OPERATION_DUNDERS = frozenset(
    "__mod__ __rmod__ __imod__ __floordiv__ __rfloordiv__ __ifloordiv__ __divmod__ __rdivmod__ __pow__ __rpow__ __ipow__ "
    "__lshift__ __rlshift__ __ilshift__ __rshift__ __rrshift__ __irshift__ __xor__ __rxor__ __ixor__".split()
)  # the foreign operators under their method names (a.__mod__(b))
BOARD_WRAPS = frozenset(
    {"roll", "pad"}
)  # numpy's own wraps: in the board's module the wrap is the carry's alone (and a call with mode=)
ITERATING_BARE = frozenset(
    "map filter iter reduce accumulate starmap vectorize permutations combinations groupby".split()
)
ITERATING_MODULES = {
    "itertools": frozenset(
        "product permutations combinations combinations_with_replacement groupby accumulate starmap takewhile dropwhile".split()
    ),
    "functools": frozenset({"reduce"}),
}  # a loop under a function's name (the comprehension rule's dodges)
ITERATING_NUMPY = frozenset("vectorize apply_along_axis apply_over_axes fromfunction frompyfunc".split())
NEW_ENGINE = "tensor24"  # the new engine's package under src (Tensor24's section 31): five folders and main.py, each gated by its own rules
STRICT = (
    NEW_ENGINE + "/algebra/",
    NEW_ENGINE + "/engine/",
    NEW_ENGINE + "/record/",
    NEW_ENGINE + "/readings/",
)  # a note of PROMOTED is a refusal here: it starts at 0 and stays
PROMOTED = frozenset({"MEMO"})
RUNNER = NEW_ENGINE + "/runner/"
REWIND = RUNNER + "rewind.py"  # the rewind check: the one module of the runner that reads the undo log
BOARD = (
    RUNNER + "board.py"
)  # the board's wrap is Rule3's carry, imported from algebra/carry.py: nothing else spells one there
LOADER = (
    RUNNER + "load.py"
)  # the loader makes every gear's coefficients from the files, so it keeps every rule of the engine (the owner's "5 approved" of 2026-10-29, 13:2x UTC); the rules count its loops, branches, comparisons, clamps and operations, and a mask or a per-row constant built from a table of bits passes them: the uniformity test (G0) is what sees that
BOARD_KEEPS = frozenset(
    {"OPERATION", "LOOP", "CLAMP", "COMPARE", "BRANCH"}
)  # the rules the board's module keeps and the rest of the runner is spared: a wrap by hand is a remainder, a quotient, a branch, a comparison, a clamp or a loop (the sixth hostile review, follow-up 2)
FORMAT = (
    RUNNER + "files.py"
)  # the files' format: the keys a universe, a piece and a setting file may hold, the checker refusing any other
KEY_CALLS = frozenset(
    "tuple list set frozenset".split()
)  # a collection made by a call of one argument holds what its argument holds
DECODER = NEW_ENGINE + "/decoder/"
DECODER_KEEPS = frozenset(
    {"OPERATION", "REFUSE", "CLAMP"}
)  # the rules the decoder keeps and the runner is spared (Animate's stricter set, the Boss's yes of 2026-10-28, 11:24 UTC)
# main.py: about 15 lines that pass the engine's functions into the runner, the one place that imports both; it is spared no rule
# (the architect's table, eaf07f596: refused, every rule but the imports), so it holds no loop, branch, comparison or number
MAIN = NEW_ENGINE + "/main.py"
MASK_CALLS = frozenset(
    "flatnonzero nonzero argwhere compress extract".split()
)  # numpy's selections by a condition
BOOK_SCOPE = (
    NEW_ENGINE + "/algebra/",
    NEW_ENGINE + "/engine/",
    RUNNER,
    MAIN,
)  # no books in the engine, its loader, its runner or main.py (law line 102, the owner's word of 2026-10-30, 04:1x); the record's schema and the decoder keep the ledger's name (his word of 04:3x)
SPECIAL_SCOPE = (
    NEW_ENGINE + "/algebra/",
    NEW_ENGINE + "/engine/",
    LOADER,
    MAIN,
)  # the Node-clock's code, its loader and main.py: no special code for a clock or a link (the owner's words of 2026-10-30, 07:1x UTC); the runner's other modules, the record and the decoder read from outside and may speak of them
SPECIAL_STEMS = (
    "lengthen",
    "shorten",
    "decoupl",
    "recoupl",
    "uncoupl",
    "horizon",
    "freez",
    "froze",
    "restor",
    "emit",
    "absorb",
    "send",
    "receiv",
)  # the words of the old engine's special rules for a link or a clock (BH-S1, The horizon, hold and restore, the sending and receiving of a link): a name that starts with one is refused in SPECIAL_SCOPE
CARRY_HOME = frozenset(
    {"core/acts.py", "core/rule3.py", NEW_ENGINE + "/algebra/carry.py"}
)  # where Rule3's division and remainder are written (the architect's design, approved at eaf07f596: algebra/carry.py alone in the new engine)
WALLS = {
    "algebra": {"algebra"},
    "engine": {"algebra", "engine", "record"},
    "record": {"record"},
    "readings": {"algebra", "readings", "record"},
    "runner": {"algebra", "readings", "record", "runner"},
    "decoder": {"algebra", "decoder", "readings", "record"},
    "main.py": {"engine", "runner"},
}  # the new engine's folders each may import (the standard library always); the architect's table, section 4 (eaf07f596)
NUMPY_FOLDERS = frozenset({"engine", "runner"})  # the folders that may import numpy
ACT = NEW_ENGINE + "/engine/"  # the new engine's act: the Node-clock's step, its Mesh and its state
SELECTIONS = frozenset(
    {"choose", "nonneg"}
)  # the engine's own selection by a bit and its floor: an if and a clamp spelt as arithmetic (David's audit, F8)
FAMILY_WORDS = frozenset(
    {"A1", "A2", "E", "T1", "T2", "gradient"}
)  # a kind or an operand named by a string: the code knows a family by name
ROOT_MODULES = frozenset(
    {"__init__.py", "main.py"}
)  # the only modules directly under tensor24/: the package's own file (the standard library alone) and main.py; any other path is unlisted
DYNAMIC_MODULES = frozenset(
    {"importlib", "runpy", "imp", "pkgutil", "zipimport"}
)  # the loaders: a module found by a string crosses a wall that reads import statements, so no folder of the new engine imports one
DYNAMIC_CALLS = frozenset(
    {"__import__", "import_module", "exec", "eval"}
)  # a call that imports or runs text by a string, the builtin compile read by its bare name beside them
COMPARE_CALLS = frozenset(
    "lt le gt ge less greater less_equal greater_equal sorted sort argsort lexsort partition searchsorted isclose "
    "bisect bisect_left bisect_right insort heappush heappop nlargest nsmallest".split()
)  # a comparison under a function's name, in the new engine
NEEDS_DTYPE_NEW = frozenset(
    "array asarray arange fromiter".split()
)  # an array of Python integers needs its dtype, in the new engine
NEEDS_DTYPE = frozenset("zeros ones empty full eye identity linspace".split())
# The closed list (the owner's idea of 2026-10-28, 15:0x UTC: say what a Node-clock may do, and what is not named is refused; the law:
# its only operations are addition, multiplication and Rule3's carry, on whole numbers). It holds in the folders below, which carry the
# Node-clock's acts and the readings' formulas; the architect's additions go through Sofer by a ledger entry naming the law line each serves.
CLOSED = (NEW_ENGINE + "/algebra/", NEW_ENGINE + "/engine/", NEW_ENGINE + "/readings/")
# a sum and a product (a difference is the sum of the opposite), Rule3's quotient and remainder in the carry's home alone
ALLOW_BINARY = (ast.Add, ast.Sub, ast.Mult, ast.MatMult)
ALLOW_CARRY = (ast.FloorDiv, ast.Mod)
ALLOW_UNARY = (ast.USub, ast.UAdd)
ALLOW_NUMPY = frozenset(
    "einsum tensordot matmul dot sum add subtract multiply negative take take_along_axis roll moveaxis swapaxes transpose "
    "reshape stack concatenate broadcast_to expand_dims squeeze zeros ones zeros_like ones_like full full_like array asarray "
    "arange eye identity diag trace outer kron tile repeat flip prod".split()
)  # the tensor vocabulary: a sum, a product (prod: a product over an axis, as sum is a sum over one), a gather, a shape; any other call of numpy is refused
# what an array may be asked to do, what it tells of itself, and the keywords of a call of numpy or of an array's method
ALLOW_METHODS = frozenset("reshape transpose astype copy take sum swapaxes".split())
ALLOW_ATTRIBUTES = frozenset("shape ndim T dtype size".split())
ALLOW_KEYWORDS = frozenset("axis axes dtype keepdims".split())
BOARD_NUMPY = frozenset(
    {"arange", "stack", "intp"}
)  # runner/board.py's own vocabulary under the closed list: the sites counted, the six neighbours stacked, the index dtype; every other name of numpy is refused there, its wrap being the carry's alone
CONSTRUCTORS = frozenset(
    "zeros ones full eye identity zeros_like ones_like full_like array asarray arange".split()
)  # the calls that make an array: each takes dtype=object (Python integers, whatever their width), the architect's rule
RECORD_BASES = frozenset("NamedTuple TypedDict Protocol".split())  # a class stands as a record alone
# what a call may name by import
SIBLINGS = tuple(NEW_ENGINE + "." + folder for folder in ("algebra", "engine", "readings", "record"))
SYMBOLS = {
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitAnd: "&",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.Not: "not",
    ast.Invert: "~",
}
CIRCULAR_WORDS = frozenset(
    "cos sin tan cosine sine tangent arccos arcsin arctan atan atan2 acos asin theta angle angles radian radians degree "
    "degrees circle circles circular quaternion quaternions trig trigonometric sinusoid sinusoidal tsirelson lorentz "
    "planck coulomb pi".split()
)
BORN = re.compile(r"\bBorn\b")
SHOWN = 40  # the hits a refusal prints, the rest counted
CONTAINERS = frozenset("dict list set defaultdict OrderedDict Counter deque".split())
MUTATORS = frozenset(
    "append extend insert pop remove clear update setdefault add discard popitem sort reverse".split()
)
MEMOS = frozenset({"cache", "lru_cache", "cached_property"})
# the modules that read a finished chart and run no step (Sofer's audit of 2026-10-28): they may read the log
READERS = frozenset(
    "run.py gates.py predicates.py reckoner.py rim.py swings.py great_clock.py strikes.py clicks.py events.py "
    "symmetries.py phenomena.py".split()
)


def exempt(rel: str, rule: str) -> bool:
    """Whether a module that reads a finished chart or record and runs no step is spared a rule: by name in the current
    engine, by folder in the new (the decoder keeps the rules of DECODER_KEEPS, the runner none but the loader, which keeps all)."""
    if rel in READERS:
        return True
    if rel.startswith(DECODER):
        return rule not in DECODER_KEEPS
    if rel.startswith(RUNNER):
        if rel == BOARD and rule in BOARD_KEEPS:
            return False  # the board's wrap is the carry's, imported
        if rel == LOADER:
            return False  # the loader is spared no rule: it builds the engine's coefficients (the files' format, the driver, the rewind check and the rounds stay spared)
        return rule != "LOGREAD" or rel == REWIND  # the undo log is read by the rewind check alone
    return False


def mask_name(node: ast.AST) -> str:
    """The selection by a condition in a node: an index that is a comparison, a boolean operation or a negation, or a call of a numpy selection; else nothing."""
    if isinstance(node, ast.Subscript) and isinstance(
        node.slice, ast.Compare | ast.BoolOp | ast.UnaryOp
    ):
        if not isinstance(node.slice, ast.UnaryOp) or isinstance(node.slice.op, ast.Not | ast.Invert):
            return "index by a condition"
    if isinstance(node, ast.Call):
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        if name in MASK_CALLS:
            return name
    return ""


def hidden_length(node: ast.AST, labels: set[str]) -> str:
    """A count spelt as a length: len() of a display written out, of a string, of a name the module binds to a display, or of an
    all-capitals constant (the convention for one bound in another module); else nothing."""
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "len"
        and len(node.args) == 1
    ):
        return ""
    arg = node.args[0]
    if isinstance(arg, DISPLAY_NODES) or (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return "len of a display"
    if isinstance(arg, ast.Name) and (arg.id in labels or (len(arg.id) > 1 and arg.id.isupper())):
        return f"len({arg.id})"
    return ""


def enum_name(node: ast.AST) -> str:
    """The enumeration a node spells: an import of enum, a class with an enumeration's base, a call of Enum, auto or their kin; else nothing."""
    if isinstance(node, ast.Import):
        return "import enum" if any(a.name.split(".")[0] == "enum" for a in node.names) else ""
    if isinstance(node, ast.ImportFrom):
        return "import enum" if (node.module or "").split(".")[0] == "enum" else ""
    if isinstance(node, ast.ClassDef):
        names = (b.attr if isinstance(b, ast.Attribute) else getattr(b, "id", "") for b in node.bases)
        return next((f"class of {n}" for n in names if n in ENUM_NAMES), "")
    if isinstance(node, ast.Call):
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        return f"call {name}" if name in ENUM_NAMES else ""
    return ""


def node_text(node: ast.AST, docstrings: set[ast.AST]) -> str:
    """The name, attribute, keyword, alias or string (a docstring spared) a node holds, else nothing."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        return node.name
    if isinstance(node, ast.arg):
        return node.arg
    if isinstance(node, ast.keyword):
        return node.arg or ""
    if isinstance(node, ast.alias):
        return node.asname or node.name
    if isinstance(node, ast.Constant) and isinstance(node.value, str) and node not in docstrings:
        return node.value
    return ""


def book_name(node: ast.AST, docstrings: set[ast.AST]) -> str:
    """The name, attribute, keyword, alias or string (a docstring spared) in a node that holds the word book, else nothing."""
    text = node_text(node, docstrings)
    return text if "book" in text.lower() else ""


def special_name(node: ast.AST, docstrings: set[ast.AST]) -> str:
    """The name, attribute, keyword, alias or string (a docstring spared) in a node with a word that starts like one of SPECIAL_STEMS, else nothing;
    the dataclass option frozen=True is spared."""
    if isinstance(node, ast.keyword) and node.arg == "frozen" and isinstance(node.value, ast.Constant):
        return ""
    text = node_text(node, docstrings)
    words = re.findall(r"[a-z]+", re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text).lower())
    return text if any(word.startswith(SPECIAL_STEMS) for word in words) else ""


def spelt_operation(node: ast.AST, numpy: set[str]) -> bool:
    """Whether an attribute is spelt by numpy's or the operator module's name: np.mod, operator.xor."""
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and (node.value.id in numpy or node.value.id == "operator")
    )


def own_choose(rel: str, name: str, node: ast.Call) -> bool:
    """The new engine's own choose(k, x, y) = k x + (1 - k) y of algebra/ (the architect's design, section 2), called by its bare name:
    numpy's choose, reached through an attribute, stays a clamp, and numpy's own name is no import there (the closed list)."""
    return name == "choose" and isinstance(node.func, ast.Name) and rel.startswith(NEW_ENGINE + "/")


def constant_index(node: ast.expr) -> bool:
    """A constant integer used as an index, signed: trains[-1], rows[0]."""
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
        node = node.operand
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
    )


def complement_of_a_name(node: ast.BinOp) -> bool:
    """1 less a name, an attribute or an element of one: the complement of a bit, with which a choose is spelt as arithmetic."""
    return (
        isinstance(node.op, ast.Sub)
        and isinstance(node.left, ast.Constant)
        and node.left.value == 1
        and isinstance(node.right, ast.Name | ast.Attribute | ast.Subscript)
    )


def indexed_by_place(node: ast.Subscript) -> bool:
    """A name or an attribute indexed by a constant, other than an array's dimension (x.shape[-1]): a family found by its place."""
    base = node.value
    return constant_index(node.slice) and (
        isinstance(base, ast.Name) or (isinstance(base, ast.Attribute) and base.attr != "shape")
    )


def reduction(rel: str, name: str, node: ast.Call) -> bool:
    """min or max over one iterable in the decoder (a reduction), not a written-out pair (a clamp)."""
    return (
        rel.startswith(DECODER)
        and name in {"min", "max"}
        and len(node.args) == 1
        and not isinstance(node.args[0], ast.Tuple | ast.List | ast.Set | ast.Starred)
    )


TEXT_TOKENS = {tokenize.STRING, tokenize.COMMENT}
if hasattr(tokenize, "FSTRING_MIDDLE"):
    TEXT_TOKENS.add(tokenize.FSTRING_MIDDLE)


@dataclass(frozen=True)
class Hit:
    """One hit of one rule: its key holds no line, so a moved line is the same hit."""

    rule: str
    rel: str
    line: int
    detail: str
    where: str = ""
    col: int = 0  # keeps two hits of one kind on one line apart; not part of the key

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.rule, self.rel, self.detail)

    @property
    def tier(self) -> str:
        tier = RULES[self.rule][0]
        return (
            "BLOCK" if tier == "WARN" and self.rule in PROMOTED and self.rel.startswith(STRICT) else tier
        )


def words_of(text: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return [w.lower() for w in re.findall(r"[A-Za-z]+", spaced)]


def integer_leaves(node: ast.AST) -> list[int] | None:
    """The integers of a literal tuple or list of integers (nested, signed); None where a leaf is not one."""
    if isinstance(node, ast.Tuple | ast.List):
        found: list[int] = []
        for element in node.elts:
            leaves = integer_leaves(element)
            if leaves is None:
                return None
            found += leaves
        return found
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
        return integer_leaves(node.operand)
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
    ):
        return [node.value]
    return None


def products(node: ast.AST) -> int:
    return sum(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult) for n in ast.walk(node))


def sums(node: ast.AST) -> bool:
    return any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add | ast.Sub) for n in ast.walk(node))


def callee_name(call: ast.Call) -> str:
    f = call.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""


def dynamic_call(call: ast.Call) -> str:
    """The name of a call that imports or runs text by a string (__import__, import_module, exec, eval, the builtin compile), else ''."""
    name = callee_name(call)
    return (
        name if name in DYNAMIC_CALLS or (name == "compile" and isinstance(call.func, ast.Name)) else ""
    )


def path_join(node: ast.BinOp | ast.AugAssign) -> bool:
    """A division with a string operand: pathlib's / joining a path, which is a TypeError between numbers (a tool names its files so)."""
    operands = (node.left, node.right) if isinstance(node, ast.BinOp) else (node.value,)
    return any(
        isinstance(o, ast.JoinedStr) or (isinstance(o, ast.Constant) and isinstance(o.value, str))
        for o in operands
    )


def is_bit(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
        and node.value in (0, 1)
    )


def quotient_parts(node: ast.AST) -> tuple[ast.AST, ast.AST] | None:
    """The dividend and the divisor of a quotient (a floor division, or a call of the carry's quotient with both)."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.FloorDiv):
        return node.left, node.right
    if isinstance(node, ast.Call) and callee_name(node) in QUOTIENT_CALLS and len(node.args) >= 2:
        return node.args[0], node.args[1]
    return None


def sign_test(node: ast.AST) -> bool:
    """x div (x x + 1): the quotient that reads a sign."""
    parts = quotient_parts(node)
    divisor = parts[1] if parts else None
    return (
        isinstance(divisor, ast.BinOp)
        and isinstance(divisor.op, ast.Add)
        and any(
            is_bit(one)
            and isinstance(square, ast.BinOp)
            and isinstance(square.op, ast.Mult)
            and ast.dump(square.left) == ast.dump(square.right)
            for one, square in ((divisor.left, divisor.right), (divisor.right, divisor.left))
        )
    )


def indicator(node: ast.AST) -> str:
    """What makes a quotient a mask or a cap: the quotient of a bit, the sign test, 1 minus a quotient; '' where it is none."""
    parts = quotient_parts(node)
    if parts is not None:
        return "bit div" if is_bit(parts[0]) else "sign test" if sign_test(node) else ""
    if (
        isinstance(node, ast.BinOp)
        and isinstance(node.op, ast.Sub)
        and isinstance(node.left, ast.Constant)
        and node.left.value == 1
        and quotient_parts(node.right) is not None
    ):
        return "1 - quotient"
    return ""


def imported_names(rel: str, node: ast.Import | ast.ImportFrom) -> list[str]:
    """The full dotted names an import brings in; a relative import is resolved from the module's own folder."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    parts = rel.split("/")[:-1]
    base = (parts[: len(parts) - (node.level - 1)] if node.level else []) + (
        node.module.split(".") if node.module else []
    )
    stem = ".".join(base)
    return [stem if alias.name == "*" else f"{stem}.{alias.name}" for alias in node.names]


def import_ok(rel: str, name: str) -> bool:
    """Whether a module of the new engine may import `name` (the folders' walls; other modules import freely)."""
    top = name.split(".")[0]
    own = NEW_ENGINE + "."
    if not rel.startswith(NEW_ENGINE + "/"):
        return True
    if top in DYNAMIC_MODULES:
        return False  # a loader is refused in every folder of the new engine, the root included
    folder = rel.split("/")[1]
    if folder == "__init__.py":
        return top in sys.stdlib_module_names  # the package's own file: the standard library alone
    if folder not in WALLS:
        return True  # an unlisted path crosses no wall written for it: scan() refuses the path itself
    if top in sys.stdlib_module_names:
        return True
    if top == "numpy":
        return folder in NUMPY_FOLDERS
    return any(name == own + inside or name.startswith(own + inside + ".") for inside in WALLS[folder])


def root_of(node: ast.AST) -> str:
    """The name at the root of a dotted expression (np in np.linalg.norm); '' where there is none."""
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ""


def last_name(node: ast.AST) -> str:
    """The last name of a dotted or subscripted expression (NamedTuple in typing.NamedTuple, Protocol in Protocol[T])."""
    if isinstance(node, ast.Subscript):
        return last_name(node.value)
    return (
        node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else ""
    )


def is_object(node: ast.AST) -> bool:
    """The Name object: the dtype of Python integers of any width."""
    return isinstance(node, ast.Name) and node.id == "object"


def is_index(node: ast.AST, numpy: set[str]) -> bool:
    """numpy's intp, the dtype of an index: np.intp."""
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "intp"
        and isinstance(node.value, ast.Name)
        and node.value.id in numpy
    )


def index_cast(call: ast.Call, parents: dict[ast.AST, ast.AST], numpy: set[str]) -> bool:
    """astype(np.intp) standing as the index of a gather: the index type's one use in the engine's closed folders. The cast is the identity
    on a whole number that fits the index type and an OverflowError on one that does not, so it changes no value; the gather is take's index
    (an array's method takes it first, np.take second) or a subscript's (alone or in a tuple of indices)."""
    if not (
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "astype"
        and len(call.args) == 1
        and not call.keywords
        and is_index(call.args[0], numpy)
    ):
        return False
    held: ast.AST = call
    above = parents.get(held)
    if isinstance(above, ast.Tuple):  # table[x.astype(np.intp), 0]: the tuple is the subscript's index
        held, above = above, parents.get(above)
    if isinstance(above, ast.Subscript):
        return above.slice is held
    if (
        isinstance(above, ast.Call)
        and isinstance(above.func, ast.Attribute)
        and above.func.attr == "take"
    ):
        at = 1 if isinstance(above.func.value, ast.Name) and above.func.value.id in numpy else 0
        return len(above.args) > at and above.args[at] is held
    return False


def frozen_record(decorator: ast.AST) -> bool:
    """@dataclass(frozen=True): a record that cannot be written after it is made."""
    return (
        isinstance(decorator, ast.Call)
        and callee_name(decorator) == "dataclass"
        and any(
            k.arg == "frozen" and isinstance(k.value, ast.Constant) and k.value.value is True
            for k in decorator.keywords
        )
    )


def closed_list(tree: ast.Module, rel: str) -> list[tuple[ast.AST, str]]:
    """What the Node-clock's closed list does not name, in a module of engine/ or readings/: (node, detail), one hit to a refused
    construct (its parts are not read inside it) and a node class that nobody listed refused by default; an annotation is no code."""
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    numpy: set[str] = set(NUMPY_NAMES)
    vocabulary = (
        BOARD_NUMPY if rel == BOARD else ALLOW_NUMPY
    )  # the board's module has a narrower list than the engine's
    methods = frozenset[str]() if rel == BOARD else ALLOW_METHODS
    # known: the functions and classes of the module, and what numpy's tensor vocabulary was imported by name (imported: to its own
    # name); siblings: the names the engine's own folders were imported by; skipped: the annotations, the decorators and the parts
    # that a refusal already names
    known: set[str] = set()
    imported: dict[str, str] = {}
    siblings: set[str] = set()
    skipped: set[ast.AST] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.ClassDef):
            known.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "numpy":
                    numpy.add(alias.asname or alias.name)
                elif alias.name.startswith(NEW_ENGINE + "."):
                    siblings.add(alias.asname or NEW_ENGINE)
        elif isinstance(node, ast.ImportFrom):
            for full, alias in zip(imported_names(rel, node), node.names, strict=True):
                if any(full == folder or full.startswith(folder + ".") for folder in SIBLINGS):
                    siblings.add(alias.asname or alias.name)
                elif (
                    node.level == 0
                    and (node.module or "").split(".")[0] == "numpy"
                    and alias.name in vocabulary
                ):
                    known.add(alias.asname or alias.name)
                    imported[alias.asname or alias.name] = alias.name
        for annotation in (
            [node.returns]
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            else [node.annotation]
            if isinstance(node, ast.arg | ast.AnnAssign)
            else []
        ):
            if annotation is not None:
                skipped.update(ast.walk(annotation))
    found: list[tuple[ast.AST, str]] = []

    def docstring(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )

    def target_ok(target: ast.AST) -> bool:
        return (
            isinstance(target, ast.Name)
            or (isinstance(target, ast.Tuple) and all(isinstance(e, ast.Name) for e in target.elts))
            or (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name))
        )

    def is_scatter(call: ast.Call) -> bool:
        """np.add.at(out, index, values) as a statement of its own: the scattered sum of a contraction, addition at the receiving site,
        order-free because addition is associative; the one write into an array that the list names."""
        func = call.func
        return (
            isinstance(func, ast.Attribute)
            and func.attr == "at"
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "add"
            and isinstance(func.value.value, ast.Name)
            and func.value.value.id in numpy
            and isinstance(parents.get(call), ast.Expr)
            and len(call.args) == 3
            and isinstance(call.args[0], ast.Name)
            and not call.keywords
        )

    def callee(call: ast.Call) -> tuple[str, bool]:
        """The detail a call is refused for ('' where the list names its callee), and whether numpy or an array's method is called."""
        func = call.func
        if isinstance(func, ast.Name):
            return ("" if func.id in known | siblings else f"call {func.id}"), False
        if isinstance(func, ast.Attribute):
            root = root_of(func)
            if root in numpy:
                ok = is_scatter(call) or (isinstance(func.value, ast.Name) and func.attr in vocabulary)
                return ("" if ok else f"call {ast.unparse(func)}"), True
            if root in siblings:
                return "", False
            return ("" if func.attr in methods else f"call .{func.attr}"), True
        return "call of an expression", False

    def judge(node: ast.AST) -> tuple[list[str], bool]:
        """The details the list refuses in one node, and whether the node is read inside."""
        if isinstance(
            node,
            ast.expr_context
            | ast.operator
            | ast.unaryop
            | ast.Module
            | ast.Return
            | ast.Pass
            | ast.Import
            | ast.alias
            | ast.arguments
            | ast.arg
            | ast.Name
            | ast.Tuple
            | ast.Subscript
            | ast.Slice,
        ):
            return [], True
        if isinstance(node, ast.ImportFrom):
            numpy_import = node.level == 0 and (node.module or "").split(".")[0] == "numpy"
            return [
                "import *" if alias.name == "*" else f"numpy.{alias.name}"
                for alias in node.names
                if alias.name == "*" or (numpy_import and alias.name not in vocabulary)
            ], True
        if isinstance(node, ast.FunctionDef):
            args, problems = node.args, []
            if node.decorator_list:
                problems.append("decorator")
                for decorator in node.decorator_list:
                    skipped.update(ast.walk(decorator))
            for present, detail in (
                (args.vararg, "*args"),
                (args.kwarg, "**kwargs"),
                (args.posonlyargs, "positional-only parameter"),
                (args.kwonlyargs, "keyword-only parameter"),
            ):
                if present:
                    problems.append(detail)
            for default in [*args.defaults, *(d for d in args.kw_defaults if d is not None)]:
                if not (
                    isinstance(default, ast.Name)
                    or (isinstance(default, ast.Constant) and (default.value is None or is_bit(default)))
                ):
                    problems.append("default " + type(default).__name__)
                    skipped.update(ast.walk(default))
            return problems, True
        if isinstance(node, ast.ClassDef):
            clean = (
                any(frozen_record(d) for d in node.decorator_list)
                or any(last_name(b) in RECORD_BASES for b in node.bases)
            ) and (
                all(frozen_record(d) for d in node.decorator_list)
                and all(last_name(b) in RECORD_BASES for b in node.bases)
                and not node.keywords
            )
            problems = [] if clean else ["class"]
            for part in [*node.decorator_list, *node.bases, *node.keywords]:
                skipped.update(ast.walk(part))
            if not clean:
                return problems, False
            for stmt in node.body:
                record = (
                    isinstance(stmt, ast.Pass)
                    or docstring(stmt)
                    or (isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name))
                )
                if not record:
                    problems.append("class body " + type(stmt).__name__)
                    skipped.update(ast.walk(stmt))
            return problems, True
        if isinstance(node, ast.Assign):
            problems = []
            for target in node.targets:
                if not target_ok(target):
                    problems.append("assign to " + type(target).__name__)
                    skipped.update(ast.walk(target))
            return problems, True
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                return [], True
            skipped.update(ast.walk(node.target))
            return ["assign to " + type(node.target).__name__], True
        if isinstance(node, ast.Expr):
            if docstring(node):
                return [], False
            if isinstance(node.value, ast.Call) and is_scatter(node.value):
                return [], True  # np.add.at(out, index, values): the call is judged beside it
            return ["expression statement " + type(node.value).__name__], False
        if isinstance(node, ast.If):
            guard = (
                isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING" and not node.orelse
            )
            return ([], True) if guard else (["If"], False)
        if isinstance(node, ast.Constant):
            value, above = node.value, parents.get(node)
            allowed = (
                value is None
                or value is Ellipsis
                or (type(value) is bool and isinstance(above, ast.keyword))
                or (type(value) is int and value in (0, 1))
                or (
                    isinstance(value, str)
                    and isinstance(above, ast.Call)
                    and callee_name(above) == "einsum"
                    and bool(above.args)
                    and above.args[0] is node
                )
            )
            return ([] if allowed else [f"constant {value!r:.24}"]), False
        if isinstance(node, ast.Attribute):
            root = root_of(node)
            cast = parents.get(node)
            allowed = (
                (node.attr in ALLOW_ATTRIBUTES and isinstance(node.ctx, ast.Load))
                or root in siblings
                or (root in numpy and isinstance(node.value, ast.Name) and node.attr in vocabulary)
                or (
                    isinstance(cast, ast.Call)
                    and index_cast(cast, parents, numpy)
                    and cast.args[0] is node
                )  # np.intp, as the one argument of the index cast
            )
            detail = f"attribute {ast.unparse(node)}" if root in numpy else f"attribute .{node.attr}"
            return ([] if allowed else [detail]), True
        if isinstance(node, ast.Call):
            detail, tensor = callee(node)
            problems = [detail] if detail else []
            func = node.func
            made = (
                imported.get(func.id, "")
                if isinstance(func, ast.Name)
                else func.attr
                if isinstance(func, ast.Attribute)
                and root_of(func) in numpy
                and isinstance(func.value, ast.Name)
                else ""
            )
            objects = any(k.arg == "dtype" and is_object(k.value) for k in node.keywords)
            if made in CONSTRUCTORS and not any(k.arg == "dtype" for k in node.keywords):
                problems.append(f"np.{made} without dtype=object")
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "astype"
                and not (
                    objects
                    or (node.args and is_object(node.args[0]))
                    or index_cast(node, parents, numpy)
                )
            ):
                problems.append("astype without object")
            for keyword_ in node.keywords:
                if keyword_.arg is None:
                    problems.append("**kwargs in a call")
                elif tensor and keyword_.arg not in ALLOW_KEYWORDS:
                    problems.append(f"keyword {keyword_.arg}")
                elif keyword_.arg == "dtype" and not (
                    is_object(keyword_.value) or (rel == BOARD and is_index(keyword_.value, numpy))
                ):
                    problems.append("dtype other than object")
            return problems, True
        if isinstance(node, ast.UnaryOp):
            allowed = isinstance(node.op, ALLOW_UNARY)
            return ([] if allowed else [f"UnaryOp {SYMBOLS.get(type(node.op), '?')}"]), allowed
        if isinstance(node, ast.BinOp):
            allowed = isinstance(node.op, ALLOW_BINARY) or (
                isinstance(node.op, ALLOW_CARRY) and rel in CARRY_HOME
            )
            return ([] if allowed else [f"BinOp {SYMBOLS.get(type(node.op), '?')}"]), allowed
        if isinstance(node, ast.List) and rel == BOARD:
            return [], True  # np.stack's list of the six neighbours
        return [type(node).__name__], False  # a node class nobody listed

    def children(node: ast.AST) -> Iterator[ast.AST]:
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                if (
                    root_of(func) not in numpy | siblings
                ):  # a module's dotted path is judged with the call
                    yield func.value
            elif not isinstance(func, ast.Name):
                yield func
            yield from node.args
            yield from (k.value for k in node.keywords)
        else:
            yield from ast.iter_child_nodes(node)

    def visit(node: ast.AST) -> None:
        problems, inside = judge(node)
        found.extend((node, detail) for detail in problems)
        if inside:
            for child in children(node):
                if child not in skipped:
                    visit(child)

    visit(tree)
    return found


def format_keys(tree: ast.Module) -> list[tuple[ast.AST, str]]:
    """Every string a module-level collection holds as a key, each with its path from the name the collection is bound to: the elements of
    a tuple, list or set (a star of a literal or of a name bound above stands in place), the keys of a dict with what lies beneath them,
    and the argument of a tuple, list, set or frozenset call; a number, a call of anything else and a name alone hold none."""
    bound: dict[str, list[str]] = {}

    def strings(node: ast.AST) -> list[str]:
        """The strings a flat collection holds, for a star of it."""
        if isinstance(node, ast.Name):
            return bound.get(node.id, [])
        if (
            isinstance(node, ast.Call)
            and callee_name(node) in KEY_CALLS
            and len(node.args) == 1
            and not node.keywords
        ):
            return strings(node.args[0])
        if isinstance(node, ast.Dict):
            return [
                k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
            ]
        held: list[str] = []
        if isinstance(node, ast.Tuple | ast.List | ast.Set):
            for item in node.elts:
                if isinstance(item, ast.Starred):
                    held += strings(item.value)
                elif isinstance(item, ast.Constant) and isinstance(item.value, str):
                    held.append(item.value)
        return held

    def walk(node: ast.AST, path: str) -> list[tuple[ast.AST, str]]:
        if (
            isinstance(node, ast.Call)
            and callee_name(node) in KEY_CALLS
            and len(node.args) == 1
            and not node.keywords
        ):
            return walk(node.args[0], path)
        found: list[tuple[ast.AST, str]] = []
        if isinstance(node, ast.Tuple | ast.List | ast.Set):
            for item in node.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    found.append((item, f"{path}.{item.value}"))
                elif isinstance(item, ast.Starred):
                    found += [(item, f"{path}.{held}") for held in strings(item.value)]
                else:
                    found += walk(item, path)
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values, strict=True):
                if key is None:
                    found += [(value, f"{path}.{held}") for held in strings(value)]
                elif isinstance(key, ast.Constant) and isinstance(key.value, str):
                    found.append((key, f"{path}.{key.value}"))
                    found += walk(value, f"{path}.{key.value}")
        return found

    keys: list[tuple[ast.AST, str]] = []
    for statement in tree.body:
        if (
            isinstance(statement, ast.Assign)
            and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
        ):
            name, value = statement.targets[0].id, statement.value
        elif (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.value is not None
        ):
            name, value = statement.target.id, statement.value
        else:
            continue
        keys += walk(value, name)
        bound[name] = strings(value)
    return keys


def layers_missing(doc: str | None) -> list[str]:
    """The layers a module's docstring does not state: a line that opens with the layer's label, a colon and a text (n/a is a text: the one general flag)."""
    text = doc or ""
    return [layer for layer in LAYERS if not re.search(rf"^[ \t]*{layer}:[ \t]*\S", text, re.MULTILINE)]


def scan(rel: str, source: str) -> list[Hit]:
    """Every hit of every rule in one module (rel: its path inside src/event_universe, another package's under its name; a test's under tests/, the rule PIN alone; a tool's under tools/, the rules NUMBER and FLOAT alone)."""
    tree = ast.parse(source)
    if rel.startswith(TESTS + "/"):
        return [
            Hit("PIN", rel, node.lineno, "assert", "", node.col_offset)
            for node in ast.walk(tree)
            if isinstance(node, ast.Assert)
            and any(
                isinstance(c, ast.Constant)
                and isinstance(c.value, int | float)
                and not isinstance(c.value, bool)
                and c.value not in (0, 1)
                for c in ast.walk(node.test)
            )
        ]
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    hits: list[Hit] = []

    def where(node: ast.AST) -> str:
        names: list[str] = []
        cursor: ast.AST | None = node
        while cursor is not None:
            if isinstance(cursor, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                names.append(cursor.name)
            cursor = parents.get(cursor)
        return ".".join(reversed(names)) or "<module>"

    def add(rule: str, node: ast.AST, detail: str) -> None:
        hits.append(
            Hit(
                rule,
                rel,
                getattr(node, "lineno", 0),
                detail,
                where(node),
                getattr(node, "col_offset", 0),
            )
        )

    if rel.startswith(NEW_ENGINE + "/"):
        parts = rel.split("/")
        if (len(parts) == 2 and parts[1] not in ROOT_MODULES) or (
            len(parts) > 2 and parts[1] not in WALLS
        ):
            add(
                "ISOLATE", tree, f"unlisted path {rel}"
            )  # the architect's table names the folders: no wall covers another
        if parts[-1] != "__init__.py" and (missing := layers_missing(ast.get_docstring(tree))):
            hits.append(Hit("DOCLAYER", rel, 1, "the four layers", "missing: " + ", ".join(missing)))  # one hit per module, its key constant
    numpy = set(NUMPY_NAMES)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            numpy |= {a.asname or a.name for a in node.names if a.name == "numpy"}
        if isinstance(node, ast.Import | ast.ImportFrom):
            for name in imported_names(rel, node):
                if not import_ok(rel, name):
                    add("ISOLATE", node, name)
        elif rel.startswith(NEW_ENGINE + "/") and isinstance(node, ast.Call) and dynamic_call(node):
            add(
                "ISOLATE", node, f"dynamic import {dynamic_call(node)}"
            )  # a string names the module: no wall reads it
    if rel.startswith(NEW_ENGINE + "/") or TOOLS.fullmatch(rel):
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Add)
                and ast.dump(node.left) == ast.dump(node.right)
            ):
                add(
                    "TWICE", node, ast.unparse(node)
                )  # not spared to the runner or the decoder: the loader's twos are the engine's
        labels = {
            statement.targets[0].id
            for statement in tree.body
            if isinstance(statement, ast.Assign)
            and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and isinstance(statement.value, DISPLAY_NODES)
        }  # the module's names bound to a label tuple, a list, a set or a dict
        for node in ast.walk(tree):
            if length := hidden_length(node, labels):
                add("LENGTH", node, length)
            if enum := enum_name(node):
                add("ENUM", node, enum)
    if rel.startswith(ACT) or rel in (LOADER, MAIN):
        for node in ast.walk(tree):
            if word := mask_name(node):
                add("MASK", node, word)
    if rel.startswith(BOOK_SCOPE):
        docstrings = {
            body[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
            and (body := node.body)
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        }
        special = rel.startswith(SPECIAL_SCOPE)
        for node in ast.walk(tree):
            if word := book_name(node, docstrings):
                add("BOOKS", node, word)
            if special and (word := special_name(node, docstrings)):
                add("SPECIAL", node, word)
    if rel.startswith(ACT) or rel == LOADER:
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and callee_name(node) in SELECTIONS
                and not spelt_operation(node.func, numpy)
            ):
                add(
                    "CHOOSE", node, callee_name(node)
                )  # an if spelt as arithmetic, or a floor: the act has neither (David's audit, F8)
            elif isinstance(node, ast.BinOp) and complement_of_a_name(node):
                add(
                    "CHOOSE", node, f"a complement {ast.unparse(node)}"
                )  # a choose spelt as arithmetic: r * a + (1 - r) * b (the hunter's finding at 36087c95d)
            elif isinstance(node, ast.Subscript) and indexed_by_place(node):
                add("POSITION", node, f"{ast.unparse(node.value)}[{ast.unparse(node.slice)}]")
            elif (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value in FAMILY_WORDS
            ):
                add("FAMILY", node, repr(node.value))
    module_containers: dict[str, ast.stmt] = {}
    for stmt in tree.body:
        value = stmt.value if isinstance(stmt, ast.Assign | ast.AnnAssign) else None
        targets = (
            stmt.targets
            if isinstance(stmt, ast.Assign)
            else [stmt.target]
            if isinstance(stmt, ast.AnnAssign)
            else []
        )
        names = [t.id for t in targets if isinstance(t, ast.Name)]
        if value is None or not names:
            continue
        literal = isinstance(
            value, ast.Dict | ast.List | ast.Set | ast.DictComp | ast.ListComp | ast.SetComp
        )
        built = isinstance(value, ast.Call) and callee_name(value) in CONTAINERS
        if literal or built:
            emptied = (
                (isinstance(value, ast.Dict) and not value.keys)
                or (isinstance(value, ast.List | ast.Set) and not value.elts)
                or (isinstance(value, ast.Call) and not value.args and not value.keywords)
            )
            for name in names:
                module_containers[name] = stmt
                if emptied:
                    add("STATE", stmt, f"module-level container {name}")
        if isinstance(value, ast.Call) and callee_name(value) in MEMOS:
            add("MEMO", stmt, f"{names[0]} = {callee_name(value)}(...)")

    written: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            add("STATE", node, "global " + ", ".join(node.names))
            written |= set(node.names)
        elif isinstance(node, ast.Assign | ast.AugAssign | ast.Delete):
            for target in node.targets if isinstance(node, ast.Assign | ast.Delete) else [node.target]:
                base = (
                    target.value
                    if isinstance(target, ast.Subscript)
                    else target
                    if isinstance(node, ast.AugAssign)
                    else None
                )
                if isinstance(base, ast.Name):
                    written.add(base.id)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in MUTATORS
        ):
            if isinstance(node.func.value, ast.Name):
                written.add(node.func.value.id)
    for name, stmt in module_containers.items():
        if name in written and not any(
            h.rule == "STATE" and h.detail == f"module-level container {name}" for h in hits
        ):
            add("STATE", stmt, f"module-level container {name}")

    for node in ast.walk(tree):
        found_indicator = indicator(node)
        if found_indicator and not exempt(rel, "INDICATOR"):
            add("INDICATOR", node, found_indicator)
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BAD_IMPORTS:
                    add("IMPORT", node, alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".")[0] in BAD_IMPORTS:
                add("IMPORT", node, module)
            if (
                rel not in CARRY_HOME
                and not exempt(rel, "OPERATION")
                and module.split(".")[0] in numpy | {"operator"}
            ):
                for alias in node.names:
                    if alias.name in OPERATION_CALLS | OPERATION_DUNDERS:
                        add("OPERATION", node, f"{module}.{alias.name}")
            if rel == BOARD and module.split(".")[0] in numpy:
                for alias in node.names:
                    if alias.name in BOARD_WRAPS:
                        add("OPERATION", node, f"numpy.{alias.name}")
            if module.split(".")[0] in numpy:
                for alias in node.names:
                    rule = (
                        "CIRCLE"
                        if alias.name in CIRCULAR_FUNCTIONS | {"pi"}
                        else "FLOAT"
                        if alias.name in NP_FLOAT
                        else ""
                    )
                    if rule:
                        add(rule, node, f"numpy.{alias.name}")
        elif isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, int | float | complex) and not isinstance(value, bool):
                if isinstance(value, float | complex):
                    add("FLOAT", node, f"literal {value!r}")
                if value not in (0, 1):
                    add("NUMBER", node, repr(value))
        elif isinstance(node, ast.BinOp | ast.AugAssign) and isinstance(node.op, ast.Div):
            if not (TOOLS.fullmatch(rel) and path_join(node)):
                add("FLOAT", node, "true division")
        elif (
            isinstance(node, ast.BinOp | ast.AugAssign)
            and not exempt(rel, "OPERATION")
            and (
                type(node.op) in FOREIGN_OPERATORS
                or (isinstance(node.op, ast.FloorDiv | ast.Mod) and rel not in CARRY_HOME)
            )
        ):
            add(
                "OPERATION",
                node,
                FOREIGN_OPERATORS.get(type(node.op), "//" if isinstance(node.op, ast.FloorDiv) else "%"),
            )
        elif isinstance(node, ast.Raise) and not exempt(rel, "REFUSE"):
            add("REFUSE", node, "raise")
        elif isinstance(node, ast.Call):
            name = callee_name(node)
            if isinstance(node.func, ast.Name) and name in {"round", "complex", "pow"}:
                add("FLOAT", node, f"{name}()")
            if rel not in CARRY_HOME and not exempt(rel, "OPERATION"):
                if name == "divmod":
                    add(
                        "OPERATION", node, "divmod"
                    )  # np.divmod too: the attribute rule gives the same hit, kept once
                if name in {"getattr", "attrgetter", "methodcaller"} and any(
                    isinstance(arg, ast.Constant) and arg.value in OPERATION_CALLS | OPERATION_DUNDERS
                    for arg in node.args
                ):
                    add("OPERATION", node, f"{name} of an operation's name")
            if rel == BOARD and any(k.arg == "mode" for k in node.keywords):
                add("OPERATION", node, "mode=")
            if not exempt(rel, "LOOP"):
                module = (
                    node.func.value.id
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                    else ""
                )
                if (
                    (isinstance(node.func, ast.Name) and name in ITERATING_BARE)
                    or name in ITERATING_MODULES.get(module, frozenset())
                    or (module in numpy and name in ITERATING_NUMPY)
                ):
                    add("LOOP", node, "call")
                if isinstance(node.func, ast.Name):
                    cursor: ast.AST | None = parents.get(node)
                    while cursor is not None and not isinstance(
                        cursor, ast.FunctionDef | ast.AsyncFunctionDef
                    ):
                        cursor = parents.get(cursor)
                    if (
                        isinstance(cursor, ast.FunctionDef | ast.AsyncFunctionDef)
                        and cursor.name == name
                        and not isinstance(parents.get(cursor), ast.ClassDef)
                    ):
                        add("LOOP", node, "recursion")
            if isinstance(node.func, ast.Name) and name == "id":
                add("STATE", node, "id()")
            if name in ROOTS:
                add("ROOT", node, name)
            if (
                name in CLAMPS
                and not exempt(rel, "CLAMP")
                and not reduction(rel, name, node)
                and not own_choose(rel, name, node)
            ):
                add("CLAMP", node, f"{name}()")
            if rel.startswith(NEW_ENGINE + "/") and not exempt(rel, "COMPARE") and name in COMPARE_CALLS:
                add("COMPARE", node, "call")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if (
                    node.func.value.id in numpy
                    and (
                        name in NEEDS_DTYPE
                        or (name in NEEDS_DTYPE_NEW and rel.startswith(NEW_ENGINE + "/"))
                    )
                    and not any(k.arg == "dtype" for k in node.keywords)
                ):
                    add("DTYPE", node, f"np.{name}")
        elif isinstance(node, ast.Attribute):
            if (
                rel not in CARRY_HOME
                and not exempt(rel, "OPERATION")
                and (
                    node.attr in OPERATION_DUNDERS
                    or (node.attr in OPERATION_CALLS and spelt_operation(node, numpy))
                )
            ):
                add("OPERATION", node, node.attr)
            if (
                rel == BOARD
                and node.attr in BOARD_WRAPS
                and isinstance(node.value, ast.Name)
                and node.value.id in numpy
            ):
                add("OPERATION", node, f"np.{node.attr}")
            if isinstance(node.value, ast.Name) and node.value.id in numpy:
                if node.attr in NP_FLOAT:
                    add("FLOAT", node, f"np.{node.attr}")
                if node.attr in CIRCULAR_FUNCTIONS or node.attr == "pi":
                    add("CIRCLE", node, f"np.{node.attr}")
            if node.attr == "log" and isinstance(node.ctx, ast.Load) and not exempt(rel, "LOGREAD"):
                above = parents.get(node)
                call = parents.get(above) if above is not None else None
                appends = (
                    isinstance(above, ast.Attribute)
                    and above.attr in MUTATORS
                    and isinstance(call, ast.Call)
                )
                if not appends:
                    add("LOGREAD", node, "log read")
        elif isinstance(node, ast.Name):
            if node.id in {"float", "complex"}:
                add("FLOAT", node, node.id)
            if node.id in CIRCULAR_FUNCTIONS or node.id == "pi":
                add("CIRCLE", node, node.id)
        elif isinstance(
            node,
            ast.For
            | ast.AsyncFor
            | ast.While
            | ast.ListComp
            | ast.SetComp
            | ast.DictComp
            | ast.GeneratorExp,
        ) and not exempt(rel, "LOOP"):
            add(
                "LOOP",
                node,
                "for"
                if isinstance(node, ast.For | ast.AsyncFor)
                else "while"
                if isinstance(node, ast.While)
                else "comprehension",
            )
        elif (
            isinstance(node, ast.Compare)
            and not exempt(rel, "COMPARE")
            and any(isinstance(op, ORDERING) for op in node.ops)
        ):
            add("COMPARE", node, "ordering")
        elif isinstance(node, ast.If | ast.IfExp | ast.Match) and not exempt(rel, "BRANCH"):
            guard = (
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Name)
                and node.test.id == "TYPE_CHECKING"
            )
            if not guard:
                add(
                    "BRANCH",
                    node,
                    "if"
                    if isinstance(node, ast.If)
                    else "match"
                    if isinstance(node, ast.Match)
                    else "ternary",
                )
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            for decorator in node.decorator_list:
                found = (
                    callee_name(decorator)
                    if isinstance(decorator, ast.Call)
                    else (
                        decorator.id
                        if isinstance(decorator, ast.Name)
                        else decorator.attr
                        if isinstance(decorator, ast.Attribute)
                        else ""
                    )
                )
                if found in MEMOS:
                    add("MEMO", node, f"@{found} {node.name}")
        if isinstance(node, ast.Tuple | ast.List):
            above = parents.get(node)
            indexing = isinstance(above, ast.Subscript) and above.slice is node
            if not indexing and not isinstance(above, ast.Tuple | ast.List):
                leaves = integer_leaves(node)
                if leaves is not None and len(leaves) >= 3 and any(leaves):
                    add("TABLE", node, "table " + ast.unparse(node)[:48])
            if isinstance(node, ast.Tuple) and not indexing and len(node.elts) >= 3:
                if all(products(e) >= 2 and sums(e) for e in node.elts):
                    add("MIX", node, f"{len(node.elts)} bilinear sums")

    if rel.startswith(CLOSED) or rel == BOARD:
        for node, detail in closed_list(tree, rel):
            add("ALLOW", node, detail)
    if rel.startswith(CLOSED):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and index_cast(node, parents, numpy):
                add("INDEX", node, "astype(np.intp) as a gather's index")

    if rel == FORMAT:
        for node, path in format_keys(tree):
            add("KEYS", node, path)

    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.NAME and not keyword.iskeyword(token.string):
                if any(w in CIRCULAR_WORDS for w in words_of(token.string)):
                    hits.append(Hit("WORD", rel, token.start[0], token.string))
                if not exempt(rel, "BOUND") and any(w in BOUND_WORDS for w in words_of(token.string)):
                    hits.append(Hit("BOUND", rel, token.start[0], token.string))
            elif token.type in TEXT_TOKENS:
                found_words = sorted({w for w in words_of(token.string) if w in CIRCULAR_WORDS})
                if BORN.search(token.string):
                    found_words.append("Born")
                if found_words:
                    hits.append(Hit("TEXT", rel, token.start[0], "/".join(found_words)))
    except tokenize.TokenError:
        pass
    kept = sorted(set(hits), key=lambda h: (h.rel, h.line, h.rule, h.detail))
    return [h for h in kept if h.rule in TOOL_RULES] if TOOLS.fullmatch(rel) else kept


def git(repo: Path, *args: str, stdin: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, input=stdin, check=False)


def resolve(repo: Path, rev: str) -> str | None:
    found = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return found.stdout.decode().strip() if found.returncode == 0 else None


def rel_of(path: str) -> str:
    """A file's key path: inside src/event_universe as it was, another package under its own name, a test under tests/."""
    for prefix in (PACKAGE + "/", "src/"):
        if path.startswith(prefix):
            return path[len(prefix) :]
    return path


def sources_at(repo: Path, rev: str) -> dict[str, str]:
    """The modules of every package under src, the tests and the new engine's tools at a revision, read from git without a checkout."""
    listing = git(repo, "ls-tree", "-r", "--name-only", rev, "--", *SCOPES).stdout.decode().split("\n")
    tools = [
        row.split("\t", 1) for row in git(repo, "ls-tree", rev, "tools/").stdout.decode().splitlines()
    ]
    paths = [p for p in listing if p.endswith(".py")] + [
        path for kind, path in tools if kind.split()[1] == "blob" and TOOLS.fullmatch(path)
    ]
    if not paths:
        return {}
    payload = git(
        repo, "cat-file", "--batch", stdin="".join(f"{rev}:{p}\n" for p in paths).encode()
    ).stdout
    stream = io.BytesIO(payload)
    found: dict[str, str] = {}
    for path in paths:
        _oid, _kind, size = stream.readline().split()
        found[rel_of(path)] = stream.read(int(size)).decode("utf-8")
        stream.read(1)
    return found


def sources_in(root: Path) -> dict[str, str]:
    found = {
        rel_of(p.relative_to(root).as_posix()): p.read_text(encoding="utf-8")
        for scope in SCOPES
        if (root / scope).is_dir()
        for p in sorted((root / scope).rglob("*.py"))
    }
    tools = [p for p in sorted((root / "tools").glob("tensor24_*.py")) if p.is_file()]
    return found | {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8") for p in tools}


def hits_of(sources: dict[str, str]) -> list[Hit]:
    found: list[Hit] = []
    for rel, text in sorted(sources.items()):
        try:
            found += scan(rel, text)
        except SyntaxError as error:
            raise SystemExit(
                f"the gate cannot parse {rel}: {error} (read it with venv314/bin/python)"
            ) from None
    return found


def standing(path: Path) -> Counter[tuple[str, str, str]]:
    """A list of hits that stands: 'RULE|file|detail' per line, a repeat a count."""
    if not path.is_file():
        return Counter()
    keys = [tuple(k.split("|", 2)) for k in json.loads(path.read_text(encoding="utf-8"))]
    return Counter((r, f, d) for r, f, d in keys)


def allowance(repo: Path = REPO) -> Counter[tuple[str, str, str]]:
    """What the owner's word lets stand: entries {rule, file, detail, count, word, row}, read from Sofer's published branch
    (origin/scribe-5), so that a push cannot approve itself by editing its own copy; the working file where that ref is absent."""
    relative = ALLOWED.relative_to(REPO).as_posix()
    shown = git(repo, "show", f"{PUBLISHED}:{relative}")
    if shown.returncode == 0:
        text = shown.stdout.decode()
    elif ALLOWED.is_file():
        text = ALLOWED.read_text(encoding="utf-8")
    else:
        return Counter()
    held: Counter[tuple[str, str, str]] = Counter()
    for entry in json.loads(text):
        held[(entry["rule"], entry["file"], entry["detail"])] += int(entry.get("count", 1))
    return held


def readings(repo: Path = REPO) -> Counter[tuple[str, str, str]]:
    """The keys Sofer has read through the law: 'KEYS|file|path' per line, read from his published branch as the allowance is (a push
    cannot read its own keys into the list), else the working file."""
    relative = KEYS_READ.relative_to(REPO).as_posix()
    shown = git(repo, "show", f"{PUBLISHED}:{relative}")
    if shown.returncode == 0:
        text = shown.stdout.decode()
    elif KEYS_READ.is_file():
        text = KEYS_READ.read_text(encoding="utf-8")
    else:
        return Counter()
    held: Counter[tuple[str, str, str]] = Counter()
    for line in json.loads(text):
        rule, file, detail = line.split("|", 2)
        held[(rule, file, detail)] += 1
    return held


CEILED = frozenset(
    {"TWICE", "CHOOSE", "BRANCH", "LOOP", "COMPARE", "CLAMP", "FAMILY", "POSITION"}
)  # the rules that the stages of the new engine delete


def ceiled(key: tuple[str, str, str]) -> bool:
    """A key the ceiling binds: one of the deleted-by-stages rules, in a file of the new engine's src."""
    return key[0] in CEILED and key[1].startswith(NEW_ENGINE + "/")


def ceiling(repo: Path = REPO) -> Counter[tuple[str, str, str]] | None:
    """What stands at most per key at a live head: entries {rule, file, detail, count}, read from Sofer's published branch (origin/scribe-5)
    as the allowance is, the working file where that ref is absent; None where there is no file (no ceiling binds)."""
    relative = CEILING.relative_to(REPO).as_posix()
    shown = git(repo, "show", f"{PUBLISHED}:{relative}")
    if shown.returncode == 0:
        text = shown.stdout.decode()
    elif CEILING.is_file():
        text = CEILING.read_text(encoding="utf-8")
    else:
        return None
    held: Counter[tuple[str, str, str]] = Counter()
    for entry in json.loads(text):
        held[(entry["rule"], entry["file"], entry["detail"])] += int(entry.get("count", 1))
    return held


def frozen(repo: Path = REPO) -> Counter[tuple[str, str, str]]:
    """The probes that stand: entries {rule, file, detail, count}, read from Sofer's published branch (origin/scribe-5) as the allowance is,
    the working file where that ref is absent (the rules PROBE and DIVIDE; the owner's yes of 2026-10-30, 09:0x UTC: the standing probes frozen)."""
    relative = PROBES_LIST.relative_to(REPO).as_posix()
    shown = git(repo, "show", f"{PUBLISHED}:{relative}")
    if shown.returncode == 0:
        text = shown.stdout.decode()
    elif PROBES_LIST.is_file():
        text = PROBES_LIST.read_text(encoding="utf-8")
    else:
        return Counter()
    held: Counter[tuple[str, str, str]] = Counter()
    for entry in json.loads(text):
        held[(entry["rule"], entry["file"], entry["detail"])] += int(entry.get("count", 1))
    return held


def above(now: Iterable[Hit], stands: Counter[tuple[str, str, str]]) -> list[Hit]:
    """The hits above what stands at their key (the last by line), less what the owner's word allows and the keys Sofer has read; what may
    stand at a key that the ceiling binds is capped at the ceiling, so that what a stage deleted does not come back up to the base's own."""
    stands = stands + allowance() + readings() + frozen()
    bound = ceiling()
    if bound is not None:
        stands = Counter(
            {
                key: min(count, bound.get(key, 0)) if ceiled(key) else count
                for key, count in stands.items()
            }
        )
    found: list[Hit] = []
    for key, group in groupby(sorted(now, key=lambda h: (h.key, h.line)), key=lambda h: h.key):
        members = list(group)
        extra = len(members) - stands.get(key, 0)
        if extra > 0:
            found += members[-extra:]
    return sorted(found, key=lambda h: (h.rel, h.line, h.rule))


def is_ancestor(repo: Path, old: str, new: str) -> bool:
    """Whether the commit `old` is `new` or lies behind it in its history."""
    return git(repo, "merge-base", "--is-ancestor", old, new).returncode == 0


def floored(repo: Path, found: str, tree_rev: str) -> str:
    """The merge base, or the floor where the merge base lies behind the floor and the tree holds the floor (a pull request into main).

    A merge base beside the floor, on a line the floor is not part of, stands as it is: only a base older than the floor on its own line is lifted to it."""
    floor = resolve(repo, FLOOR)
    lifted = bool(floor) and is_ancestor(repo, found, floor) and is_ancestor(repo, floor, tree_rev)
    return floor if lifted else found


def merge_base(repo: Path, base: str | None, tree_rev: str) -> tuple[str, str]:
    """The base ref (given, CHECK_BASE, else the first of BASES that resolves) and its merge base with the tree's revision, never older than FLOOR."""
    names = (
        [base] if base else [os.environ["CHECK_BASE"]] if os.environ.get("CHECK_BASE") else list(BASES)
    )
    for name in names:
        commit = resolve(repo, name)
        if commit:
            found = git(repo, "merge-base", commit, tree_rev)
            if found.returncode == 0:
                merged = found.stdout.decode().strip()
                kept = floored(repo, merged, tree_rev)
                return (name if kept == merged else f"{name}, floored at {FLOOR}"), kept
    raise SystemExit(
        f"the merge base of {tree_rev[:9]} with {names} cannot be found: fetch the base or set CHECK_BASE"
    )


def moved(repo: Path, *revs: str, cached: bool = False) -> dict[str, str]:
    """The modules git reads as moved between the revisions (or the index and the revision), new path to old."""
    flags = ["diff", "-M", "--name-status", "--diff-filter=R", *(["--cached"] if cached else [])]
    listing = git(repo, *flags, *revs, "--", *SCOPES, TOOLS_SPEC).stdout.decode().splitlines()
    found: dict[str, str] = {}
    for line in listing:
        _status, old, new = line.split("\t")
        if old.endswith(".py") and new.endswith(".py"):
            found[rel_of(new)] = rel_of(old)
    return found


def stood(hits: Iterable[Hit], moves: dict[str, str]) -> Counter[tuple[str, str, str]]:
    """The base's hits as counts per key, a moved module's under its new path (a rename is no new hit)."""
    renamed = {old: new for new, old in moves.items()}
    return Counter((h.rule, renamed.get(h.rel, h.rel), h.detail) for h in hits)


def report(label: str, new: list[Hit], base_label: str, out: Any = sys.stdout) -> int:
    """Print the refusals and the notes; 1 where a refusal stands."""
    refusals = [h for h in new if h.tier == "BLOCK"]
    notes = [h for h in new if h.tier == "WARN"]
    print(
        f"Sofer's gate: {label} against {base_label}: refusals {len(refusals)}, notes {len(notes)}",
        file=out,
    )
    for hit in (refusals + notes)[:SHOWN]:
        mark = "REFUSED" if hit.tier == "BLOCK" else "note   "
        place = f" in {hit.where}" if hit.where and hit.where != "<module>" else ""
        print(f"  {mark} {hit.rule:7s} {hit.rel}:{hit.line}{place}: {hit.detail}", file=out)
    if len(new) > SHOWN:
        print(
            f"  ... and {len(new) - SHOWN} more (scribe_scan.py TREE --base REV lists them all)",
            file=out,
        )
    for rule in sorted({h.rule for h in new}):
        print(f"  {rule}: {RULES[rule][1]}", file=out)
    if refusals:
        print(
            "  These are the owner's rules (docs/ALGEBRA.md): the push is refused and nothing was sent.\n"
            "  If a rule or a law must be broken, STOP and tell the owner, the Boss and David in the thread at once (his order of\n"
            "  2026-10-28, 04:5x UTC); only his word lets a hit stand (scribe_scan_allowed.json, written by Sofer on that word).\n"
            "  Do not weaken or go round this gate (--no-verify, an edited list or script): Sofer reads every push and reports it.",
            file=out,
        )
    return 1 if refusals else 0


def delta_line(before: list[Hit], after: list[Hit]) -> str:
    """The hits by rule from the base to the push: what falls toward the end state of 0 and what rises."""
    was, now = Counter(h.rule for h in before), Counter(h.rule for h in after)
    moved_rules = [
        f"{rule} {was[rule]} to {now[rule]}"
        for rule in sorted(set(was) | set(now))
        if was[rule] != now[rule]
    ]
    return "counts from the base: " + (", ".join(moved_rules) if moved_rules else "unchanged")


def declared_path(path: str) -> bool:
    """Whether the rule DECLARE reads a path: a .json or .py file under the declared scopes, outside an environment or a cache and outside
    the gate's own files, whose fixtures name trains to test the rule (they change only on the owner's word, OWN)."""
    parts = path.split("/")
    return (
        path.endswith((".json", ".py"))
        and parts[0] in DECLARED_SCOPES
        and not DECLARED_SKIP & set(parts)
        and path not in OWN
    )


def line_of(text: str, word: str) -> int:
    """The line a quoted name first stands on in a file's text, 1 where it is not found (no part of a hit's key)."""
    found = text.find(f'"{word}"')
    return text.count("\n", 0, found) + 1 if found >= 0 else 1


def declared_json(rel: str, text: str) -> list[Hit]:
    """The families, trains and couplings a universe file names, each with the number it carries as the file writes it; a train at
    pinion = den, the file's own integer, is the seed and declares no mass."""
    try:
        data = json.loads(text)
    except ValueError:
        return []
    if not isinstance(data, dict):
        return []
    integers = data.get("integers")
    den = integers.get("den") if isinstance(integers, dict) else None
    found: list[Hit] = []
    for key, kind in DECLARED_LISTS:
        entries = data.get(key)
        for entry in entries if isinstance(entries, list) else ():
            if not isinstance(entry, dict):
                continue
            if kind == "coupling":
                found.append(Hit("DECLARE", rel, 1, f"coupling {json.dumps(entry, sort_keys=True)}"))
                continue
            name = entry.get("name")
            if not isinstance(name, str):
                continue
            if kind == "train" and den is not None and entry.get("pinion") == den:
                continue
            number = next(
                (json.dumps(entry[g], sort_keys=True) for g in DECLARED_GEAR if g in entry), "-"
            )
            found.append(Hit("DECLARE", rel, line_of(text, name), f"{kind} {name} {number}"))
    return found


def coupling_name(node: ast.AST) -> bool:
    """Whether a name or an attribute is called a coupling list (couplings, self.coupling_rows): the rows a world's code lays as lists."""
    name = (
        node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else ""
    )
    return "coupling" in name.lower()


def fixed_value(node: ast.expr) -> bool:
    """Whether an expression holds literals and module constants (names in capitals) alone: a value the code writes, not one it forwards."""
    return all(n.id.isupper() for n in ast.walk(node) if isinstance(n, ast.Name))


def literal_integer(node: ast.expr) -> bool:
    """An integer literal, signed."""
    return integer_leaves(node) is not None and not isinstance(node, ast.Tuple | ast.List)


def declared_python(rel: str, text: str) -> list[Hit]:
    """The trains a world's code writes as a dict, a literal or a call of dict, with a name and a pinion, the pinion as the line writes it (unparsed, so that a
    reformatted line is the same declaration); a pinion spelt den, or as the attribute den of a module (rig.DEN), is the seed."""
    try:
        tree = ast.parse(text)
    # parenthesized, so that an older Python than 3.14 compiles the gate and re-runs it under 3.14
    except (SyntaxError, ValueError):  # fmt: skip
        return []
    found: list[Hit] = []
    for node in ast.walk(tree):
        rows: list[ast.expr] = []
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.List)
            and any(coupling_name(t) for t in node.targets)
        ):
            rows = [row for row in node.value.elts if isinstance(row, ast.List)]
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in ("append", "insert", "extend")
            and coupling_name(node.func.value)
        ):
            rows = [arg for arg in node.args if isinstance(arg, ast.List)]
        for row in rows:
            found.append(
                Hit("DECLARE", rel, row.lineno, f"coupling row {ast.unparse(row)}", "", row.col_offset)
            )
        if isinstance(node, ast.Call) and callee_name(node) not in ("dict", ""):
            keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg}
            callee = callee_name(node)
            pinion = keywords.get("pinion")
            if (
                pinion is not None
                and fixed_value(pinion)
                and ast.unparse(pinion).lower().rpartition(".")[2] != "den"
            ):
                found.append(
                    Hit(
                        "DECLARE",
                        rel,
                        node.lineno,
                        f"train call {callee} {ast.unparse(pinion)}",
                        "",
                        node.col_offset,
                    )
                )
            strength = keywords.get("strength")
            if strength is not None and literal_integer(strength):
                found.append(
                    Hit(
                        "DECLARE",
                        rel,
                        node.lineno,
                        f"coupling call {callee} strength {ast.unparse(strength)}",
                        "",
                        node.col_offset,
                    )
                )
        fields: dict[str, ast.expr]
        if isinstance(node, ast.Dict):
            fields = {
                k.value: v
                for k, v in zip(node.keys, node.values, strict=True)
                if isinstance(k, ast.Constant) and isinstance(k.value, str)
            }
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
            fields = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        else:
            continue
        name = fields.get("name")
        if isinstance(name, ast.Constant) and isinstance(name.value, str) and "pinion" in fields:
            number = ast.unparse(fields["pinion"])
            if number.lower().rpartition(".")[2] != "den":
                found.append(
                    Hit("DECLARE", rel, node.lineno, f"train {name.value} {number}", "", node.col_offset)
                )
    return found


def declared_in(rel: str, text: str) -> list[Hit]:
    """The declarations one file holds: a universe file's lists, or a Python file's train dicts."""
    if rel.endswith(".json"):
        return declared_json(rel, text)
    return declared_python(rel, text) if rel.endswith(".py") else []


def declared_hits(sources: dict[str, str]) -> list[Hit]:
    return [hit for rel, text in sorted(sources.items()) for hit in declared_in(rel, text)]


def declared_sources_in(root: Path) -> dict[str, str]:
    """Every file the rule reads in a working tree (the audit's reading)."""
    found: dict[str, str] = {}
    for scope in DECLARED_SCOPES:
        if not (root / scope).is_dir():
            continue
        for path in sorted((root / scope).rglob("*")):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and declared_path(rel):
                found[rel] = path.read_text(encoding="utf-8", errors="replace")
    return found


def blobs_at(repo: Path, rev: str, paths: list[str]) -> dict[str, str]:
    """The text of each path at a revision, read from git in one call; a path the revision does not hold is left out."""
    if not paths:
        return {}
    payload = git(
        repo, "cat-file", "--batch", stdin="".join(f"{rev}:{p}\n" for p in paths).encode()
    ).stdout
    stream = io.BytesIO(payload)
    found: dict[str, str] = {}
    for path in paths:
        header = stream.readline().split()
        if len(header) != 3:
            continue
        data = stream.read(int(header[2]))
        stream.read(1)
        if header[1] == b"blob":
            found[path] = data.decode("utf-8", errors="replace")
    return found


def declared_sources_at(repo: Path, rev: str) -> dict[str, str]:
    """Every file the rule reads at a revision (the audit's reading)."""
    listing = (
        git(repo, "ls-tree", "-r", "--name-only", rev, "--", *DECLARED_SCOPES)
        .stdout.decode()
        .splitlines()
    )
    return blobs_at(repo, rev, [p for p in listing if declared_path(p)])


def changed_declared(
    repo: Path, *revs: str, cached: bool = False, untracked: bool = False
) -> list[tuple[str, str, str]]:
    """Every file under the declared scopes that differs between two revisions, the index and a revision, or a revision and the working
    tree: (status, old path, new path), a rename read as one and a deleted file left out; `untracked` adds the files git does not track."""
    flags = ["diff", "-M", "--name-status", *(["--cached"] if cached else [])]
    found: list[tuple[str, str, str]] = []
    for line in git(repo, *flags, *revs, "--", *DECLARED_SCOPES).stdout.decode().splitlines():
        parts = line.split("\t")
        if parts[0][0] != "D" and declared_path(parts[-1]):
            found.append((parts[0][0], parts[1], parts[-1]))
    if untracked:
        listing = git(
            repo, "ls-files", "--others", "--exclude-standard", "--", *DECLARED_SCOPES
        ).stdout.decode()
        found += [("A", p, p) for p in listing.splitlines() if declared_path(p)]
    return found


def declared_new(
    repo: Path, base: str, head: str | None = None, root: Path | None = None, cached: bool = False
) -> list[Hit]:
    """The declarations a push adds over its merge base, in the files it changes alone (a declaration is read from its own file, so a
    file that did not change holds what it held): above what the base held in the same file (a rename is no new hit), less what the
    owner's list allows. The head is a revision, else the working tree `root` (with the index when `cached`)."""
    changes = changed_declared(
        repo, base, *([head] if head else []), cached=cached, untracked=not head and not cached
    )
    if not changes:
        return []
    olds = blobs_at(repo, base, [old for status, old, _ in changes if status != "A"])
    if head:
        news = blobs_at(repo, head, [new for _, _, new in changes])
    else:
        assert root is not None
        news = {
            new: (root / new).read_text(encoding="utf-8", errors="replace")
            for _, _, new in changes
            if (root / new).is_file()
        }
    after: list[Hit] = []
    stands: Counter[tuple[str, str, str]] = Counter()
    for status, old, new in changes:
        if new not in news:
            continue
        after += declared_in(new, news[new])
        if status != "A" and old in olds:
            stands.update((h.rule, new, h.detail) for h in declared_in(old, olds[old]))
    return above(after, stands)


def pathlike(node: ast.AST) -> bool:
    """A name, an attribute or a call that holds a path: its / joins and divides nothing."""
    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        node = node.left
    if isinstance(node, ast.Call):
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        return name in {"Path", "resolve", "parent", "expanduser"}
    if isinstance(node, ast.Attribute):
        return node.attr in {"parent", "parents"} or any(k in node.attr.lower() for k in PATHISH)
    return isinstance(node, ast.Name) and any(k in node.id.lower() for k in PATHISH)


def float_dtype(node: ast.AST) -> bool:
    """A dtype argument that holds a real number: float, a numpy float name or the string of one."""
    if isinstance(node, ast.Name):
        return node.id in PROBE_DTYPES
    if isinstance(node, ast.Attribute):
        return node.attr in PROBE_DTYPES
    return isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in PROBE_DTYPES


def names_in(node: ast.AST) -> set[str]:
    """Every name an expression reads."""
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def divisor_of(node: ast.AST) -> ast.AST | None:
    """The divisor of a floor division or of Rule3's carry (its second argument), else None."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.FloorDiv):
        return node.right
    if isinstance(node, ast.Call):
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        if name == "carry" and len(node.args) > 1:
            return node.args[1]
    return None


def series_loop(loop: ast.For | ast.While) -> bool:
    """A loop that sums a series: a statement that divides by an expression of the loop's counter (the for's target, or a name the loop counts up by a constant) and a total that a name is added to or taken from."""
    counters: set[str] = set()
    if isinstance(loop, ast.For):
        counters |= names_in(loop.target)
    body = [n for stmt in loop.body for n in ast.walk(stmt)]
    for n in body:
        if isinstance(n, ast.AugAssign) and isinstance(n.op, ast.Add) and isinstance(n.value, ast.Constant):
            counters |= names_in(n.target)
    divides = any(
        (d := divisor_of(n)) is not None and counters & names_in(d) for n in body if isinstance(n, ast.BinOp | ast.Call)
    )
    adds = any(
        isinstance(n, ast.AugAssign) and isinstance(n.op, ast.Add | ast.Sub) and isinstance(n.value, ast.Name)
        for n in body
    )
    return divides and adds


def midpoint(node: ast.AST) -> bool:
    """The midpoint of two ends, which a bisection takes: (lo + hi) // 2, with a one added or not, as a floor division, a shift by one or a carry by 2."""
    whole: ast.AST | None = None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.FloorDiv | ast.RShift):
        half = node.right
        if isinstance(half, ast.Constant) and half.value == (2 if isinstance(node.op, ast.FloorDiv) else 1):
            whole = node.left
    elif isinstance(node, ast.Call) and divisor_of(node) is not None:
        half = divisor_of(node)
        if isinstance(half, ast.Constant) and half.value == 2 and node.args:
            whole = node.args[0]
    if not isinstance(whole, ast.BinOp) or not isinstance(whole.op, ast.Add):
        return False
    terms: list[ast.AST] = []
    stack: list[ast.AST] = [whole]
    while stack:
        part = stack.pop()
        if isinstance(part, ast.BinOp) and isinstance(part.op, ast.Add):
            stack += [part.left, part.right]
        else:
            terms.append(part)
    named = [x for x in terms if isinstance(x, ast.Name)]
    return len(named) >= 2 and all(isinstance(x, ast.Name | ast.Constant) for x in terms)


def made_by_hand(name: str) -> bool:
    """A name whose snake_case words include a sine, cosine, tangent, arctangent, artanh or ln."""
    return any(word in SEARCH_WORDS for word in name.lower().split("_"))


def probe_hits(rel: str, source: str) -> list[Hit]:
    """The hits of PROBE and DIVIDE in one probe: what makes a real number, a root or a circular function in a derivation (PROBE), and a
    floor division, a remainder or divmod that is not Rule3's carry (DIVIDE); a file that does not parse holds nothing to run."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return []
    hits: list[Hit] = []

    def add(rule: str, node: ast.AST, detail: str) -> None:
        hits.append(Hit(rule, rel, getattr(node, "lineno", 0), detail, "", getattr(node, "col_offset", 0)))

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and made_by_hand(node.name):
            add("SEARCH", node, f"function {node.name}")
        elif isinstance(node, ast.Assign | ast.AnnAssign):
            for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
                for name in [n.id for n in ast.walk(target) if isinstance(n, ast.Name)]:
                    if made_by_hand(name):
                        add("SEARCH", node, f"name {name}")
        elif isinstance(node, ast.For | ast.While) and series_loop(node):
            add("SEARCH", node, "series summed by a loop")
        if midpoint(node):
            add("SEARCH", node, "bracket halved")
        if isinstance(node, ast.Constant) and isinstance(node.value, float | complex):
            add("PROBE", node, "float literal")
        elif isinstance(node, ast.BinOp | ast.AugAssign):
            left = node.left if isinstance(node, ast.BinOp) else node.target
            right = node.right if isinstance(node, ast.BinOp) else node.value
            if isinstance(node.op, ast.Div):
                if not (path_join(node) or pathlike(left)):
                    add("PROBE", node, "true division")
            elif isinstance(node.op, ast.FloorDiv):
                add("DIVIDE", node, "floor division")
            elif isinstance(node.op, ast.Mod):
                if not (isinstance(left, ast.JoinedStr) or (isinstance(left, ast.Constant) and isinstance(left.value, str))):
                    add("DIVIDE", node, "remainder")
            elif isinstance(node.op, ast.Pow) and isinstance(right, ast.UnaryOp) and isinstance(right.op, ast.USub):
                add("PROBE", node, "negative power")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BAD_IMPORTS:
                    add("PROBE", node, f"import {alias.name.split('.')[0]}")
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in BAD_IMPORTS:
                add("PROBE", node, f"import {node.module.split('.')[0]}")
        elif isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            if name in PROBE_CALLS:
                add("PROBE", node, f"call {name}")
            elif name == "divmod":
                add("DIVIDE", node, "divmod")
            if any(k.arg == "dtype" and float_dtype(k.value) for k in node.keywords) or (
                name == "astype" and node.args and float_dtype(node.args[0])
            ):
                add("PROBE", node, "float dtype")
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in NUMPY_NAMES
            and (node.attr in NP_FLOAT or node.attr in PROBE_DTYPES or node.attr == "pi")
            and node.attr not in PROBE_CALLS
        ):
            add("PROBE", node, f"np.{node.attr}")
    return hits


def probe_path(path: str) -> bool:
    """Whether the rules PROBE and DIVIDE read a path: a .py file under tools/derivations/, outside a cache and outside the gate's own files."""
    return (
        path.startswith(PROBES)
        and path.endswith(".py")
        and "__pycache__" not in path.split("/")
        and path not in OWN
    )


def changed_probes(
    repo: Path, *revs: str, cached: bool = False, untracked: bool = False
) -> list[tuple[str, str, str]]:
    """Every probe that differs between two revisions, the index and a revision, or a revision and the working tree: (status, old path,
    new path), a rename read as one and a deleted file left out; `untracked` adds the files git does not track."""
    flags = ["diff", "-M", "--name-status", *(["--cached"] if cached else [])]
    found: list[tuple[str, str, str]] = []
    for line in git(repo, *flags, *revs, "--", PROBES).stdout.decode().splitlines():
        parts = line.split("\t")
        if parts[0][0] != "D" and probe_path(parts[-1]):
            found.append((parts[0][0], parts[1], parts[-1]))
    if untracked:
        listing = git(repo, "ls-files", "--others", "--exclude-standard", "--", PROBES).stdout.decode()
        found += [("A", p, p) for p in listing.splitlines() if probe_path(p)]
    return found


def probed_new(
    repo: Path, base: str, head: str | None = None, root: Path | None = None, cached: bool = False
) -> list[Hit]:
    """The probe hits a push adds over its merge base, in the probes it adds or changes alone: above what the base held in the same file
    (a rename is no new hit), less what the owner's list and the frozen probes allow. The head is a revision, else the working tree
    `root` (with the index when `cached`). A probe that is new is read whole: every hit of it is new."""
    changes = changed_probes(
        repo, base, *([head] if head else []), cached=cached, untracked=not head and not cached
    )
    if not changes:
        return []
    olds = blobs_at(repo, base, [old for status, old, _ in changes if status != "A"])
    if head:
        news = blobs_at(repo, head, [new for _, _, new in changes])
    else:
        assert root is not None
        news = {
            new: (root / new).read_text(encoding="utf-8", errors="replace")
            for _, _, new in changes
            if (root / new).is_file()
        }
    after: list[Hit] = []
    stands: Counter[tuple[str, str, str]] = Counter()
    for status, old, new in changes:
        if new not in news:
            continue
        after += probe_hits(new, news[new])
        if status != "A" and old in olds:
            stands.update((h.rule, new, h.detail) for h in probe_hits(old, olds[old]))
    return above(after, stands)


def check_revision(repo: Path, rev: str, base: str | None, out: Any = sys.stdout) -> int:
    """The tree at `rev` against its merge base: 1 on a refusal."""
    commit = resolve(repo, rev)
    if commit is None:
        print(f"the gate cannot resolve {rev}", file=out)
        return 0
    name, mb = merge_base(repo, base, commit)
    touched = (
        git(repo, "diff", "--name-only", mb, commit, "--", *SCOPES, TOOLS_SPEC, *OWN)
        .stdout.decode()
        .split()
    )
    declared = declared_new(repo, mb, commit) + probed_new(repo, mb, commit)
    if not touched and not declared:
        return 0
    before: list[Hit] = []
    after: list[Hit] = []
    new: list[Hit] = []
    if touched:
        before, after = hits_of(sources_at(repo, mb)), hits_of(sources_at(repo, commit))
        stands = stood(before, moved(repo, mb, commit))
        new = above(after, stands)
    new = new + declared
    own = [p for p in touched if p in OWN]
    status = report(f"{commit[:9]}", new, f"its merge base {mb[:9]} with {name}", out) if new else 0
    if touched:
        print(f"  {delta_line(before, after)}", file=out)
    if own:
        print(
            f"  note: this push changes the gate's own files {own}: the owner's word is needed for it",
            file=out,
        )
    return status


@contextmanager
def scratch(repo: Path, commit: str) -> Iterator[Path]:
    """A detached worktree of the commit, removed after."""
    with tempfile.TemporaryDirectory() as directory:
        place = Path(directory) / "tree"
        git(repo, "worktree", "add", "--detach", str(place), commit)
        try:
            yield place
        finally:
            git(repo, "worktree", "remove", "--force", str(place))


def check_patch(repo: Path, patch: Path, base: str | None) -> int:
    name, commit = merge_base(repo, base, "HEAD") if base is None else (base, resolve(repo, base) or "")
    with scratch(repo, commit) as tree:
        applied = git(tree, "apply", "--3way", str(patch.resolve()))
        if applied.returncode != 0:
            print(f"the patch does not apply on {commit[:9]}: {applied.stderr.decode().strip()}")
            return 2
        git(tree, "add", "-A")
        before, after = hits_of(sources_at(repo, commit)), hits_of(sources_in(tree))
        stands = stood(before, moved(tree, commit, cached=True))
        new = (
            above(after, stands)
            + declared_new(tree, commit, root=tree, cached=True)
            + probed_new(tree, commit, root=tree, cached=True)
        )
    base_label = name if name == commit[:9] else f"{name} ({commit[:9]})"
    status = (
        report(f"the patch {patch.name}", new, base_label) if new else _clean(patch.name, base_label)
    )
    print(f"  {delta_line(before, after)}")
    return status


def _clean(label: str, base: str) -> int:
    print(f"Sofer's gate: {label} against {base}: no refusal, no note")
    return 0


def pushes(command: str, cwd: str) -> list[tuple[Path, str]]:
    """The (directory, revision) of every `git push` in a shell command line: its refspecs' sources, else HEAD."""
    found: list[tuple[Path, str]] = []
    where = Path(cwd)
    for segment in re.split(r"&&|\|\||;|\n|\|", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            continue
        if words[:1] == ["cd"] and len(words) > 1:
            where = (where / words[1]) if not words[1].startswith("/") else Path(words[1])
            continue
        if words[:1] != ["git"] or "push" not in words:
            continue
        index, folder = 1, where
        while index < len(words) and words[index] != "push":
            if words[index] == "-C" and index + 1 < len(words):
                folder = (
                    (where / words[index + 1])
                    if not words[index + 1].startswith("/")
                    else Path(words[index + 1])
                )
                index += 1
            index += 1
        rest = [w for w in words[index + 1 :] if not w.startswith("-")]
        if "--delete" in words or "-d" in words:
            continue
        specs = rest[1:] or ["HEAD"]
        for spec in specs:
            source = spec.lstrip("+").split(":")[0]
            if source:
                found.append((folder, source))
    return found


def claude_hook(base: str | None) -> int:
    """Claude Code's PreToolUse call: a Bash command holding `git push` is checked before it runs; exit 2 refuses it."""
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    if event.get("tool_name") != "Bash":
        return 0
    command = str(event.get("tool_input", {}).get("command", ""))
    if "git" not in command or "push" not in command:
        return 0
    refused = False
    seen: set[tuple[str, str]] = set()
    for folder, rev in pushes(command, str(event.get("cwd") or os.getcwd())):
        top = git(folder, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if not top or (top, rev) in seen:
            continue
        seen.add((top, rev))
        try:
            refused |= check_revision(Path(top), rev, base, sys.stderr) == 1
        except SystemExit as error:
            print(f"the gate could not run ({error}); the push is not held by it", file=sys.stderr)
    return 2 if refused else 0


def push_hook(base: str | None) -> int:
    """Git's pre-push call: lines `<local ref> <local oid> <remote ref> <remote oid>` on stdin."""
    refused = False
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) == 4 and set(parts[1]) != {"0"}:
            try:
                refused |= check_revision(REPO, parts[1], base, sys.stderr) == 1
            except SystemExit as error:
                print(f"the gate could not run ({error}); the push is not held by it", file=sys.stderr)
    return 1 if refused else 0


def guarded(call: Callable[[str | None], int], base: str | None) -> int:
    """A caller's run: the gate's own fault never holds a push, it says so and lets it go (Sofer's scan reads it after)."""
    try:
        return call(base)
    except (Exception, SystemExit) as error:
        print(f"Sofer's gate could not run ({error!r}); this push is not held by it", file=sys.stderr)
        return 0


def install() -> int:
    """Write .git/hooks/pre-push for this clone (a foreign hook is never overwritten)."""
    hooks = Path(git(REPO, "rev-parse", "--git-path", "hooks").stdout.decode().strip())
    hooks = hooks if hooks.is_absolute() else REPO / hooks
    target = hooks / "pre-push"
    marker = "# installed by tools/derivations/open_items/scribe_scan.py --install"
    if target.exists() and marker not in target.read_text(encoding="utf-8"):
        print(
            f'{target} exists and is not Sofer\'s: chain `python {Path(__file__).resolve()} --hook "$@"` into it by hand'
        )
        return 2
    python = REPO / "venv314" / "bin" / "python"
    interpreter = str(python) if python.is_file() else sys.executable
    hooks.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"#!/bin/sh\n{marker} (the owner, 2026-10-28, 05:0x UTC: the laws in scripts that refuse the push)\n"
        f'script="{Path(__file__).resolve()}"\n[ -f "$script" ] || exit 0\n'
        f'exec "{interpreter}" "$script" --hook "$@"\n',
        encoding="utf-8",
    )
    target.chmod(0o755)
    print(
        f"installed {target}: a push that raises a count of Sofer's rules is refused (git push --no-verify goes round it, and is reported)"
    )
    return 0


def ensure_python() -> None:
    """The tree is Python 3.14's: an older interpreter runs this script again under the repository's own."""
    if (sys.version_info.major, sys.version_info.minor) >= (3, 14):
        return
    for candidate in (str(REPO / "venv314" / "bin" / "python"), shutil.which("python3.14") or ""):
        if candidate and Path(candidate).is_file():
            os.execv(candidate, [candidate, *sys.argv])


def summary(found: list[Hit]) -> None:
    by_rule = Counter(h.rule for h in found)
    print("hits by rule:", dict(sorted(by_rule.items())))
    by_file: dict[str, Counter[str]] = {}
    for h in found:
        by_file.setdefault(h.rel, Counter())[h.rule] += 1
    for rel in sorted(by_file):
        print(f"  {rel:34s} {dict(sorted(by_file[rel].items()))}")


def main(argv: list[str]) -> int:
    ensure_python()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "tree", nargs="?", help="a directory or a git revision (default: the working tree of this clone)"
    )
    parser.add_argument(
        "--base",
        help="the revision the merge base is taken with (default CHECK_BASE, else origin/engine-5.0-test)",
    )
    parser.add_argument(
        "--baseline",
        nargs="?",
        const=str(BASELINE),
        help="compare with the list that stands, not a merge base",
    )
    parser.add_argument(
        "--write-baseline", metavar="FILE", help="write the tree's hits as the list that stands"
    )
    parser.add_argument(
        "--patch", type=Path, help="a patch to apply on the base in a scratch worktree, then check"
    )
    parser.add_argument("--all", action="store_true", help="every hit of the tree")
    parser.add_argument("--summary", action="store_true", help="with --all: the counts only")
    parser.add_argument("--rules", action="store_true")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--hook", action="store_true")
    parser.add_argument("--claude-hook", action="store_true")
    args, extra = parser.parse_known_args(argv)  # git's pre-push call adds the remote's name and url
    if extra and not (args.hook or args.claude_hook):
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    if args.rules:
        for rule, (tier, line) in RULES.items():
            print(f"{rule:8s} {tier:5s} {line}")
        return 0
    if args.install:
        return install()
    if args.hook:
        return guarded(push_hook, args.base)
    if args.claude_hook:
        return guarded(claude_hook, args.base)
    if args.patch:
        return check_patch(REPO, args.patch, args.base)
    by_rev = bool(args.tree and not Path(args.tree).is_dir() and resolve(REPO, args.tree))
    if by_rev:
        repo, rev, sources, label = REPO, args.tree, sources_at(REPO, args.tree), args.tree
    else:
        root = Path(args.tree or REPO).resolve()
        top = git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()
        repo, rev, sources, label = (
            Path(top or root),
            "HEAD",
            sources_in(root),
            str(args.tree or "the working tree"),
        )
    found = hits_of(sources)
    if args.write_baseline:
        Path(args.write_baseline).write_text(
            json.dumps(sorted("|".join(h.key) for h in found), indent=0) + "\n", encoding="utf-8"
        )
        print(f"written: {len(found)} hits in {len(sources)} modules")
        return 0
    if args.all:
        listing = found + declared_hits(
            declared_sources_at(repo, rev) if by_rev else declared_sources_in(repo)
        )
        summary(listing) if args.summary else [
            print(f"{h.tier:5s} {h.rule:7s} {h.rel}:{h.line}  {h.detail}") for h in listing
        ]
        return 0
    if args.baseline:
        return report(
            label,
            above(found, standing(Path(args.baseline))),
            f"the list that stands ({Path(args.baseline).name})",
        )
    name, mb = merge_base(repo, args.base, rev)
    moves = moved(repo, mb, rev) if by_rev else moved(repo, mb)
    new = above(found, stood(hits_of(sources_at(repo, mb)), moves))
    new = new + (declared_new(repo, mb, rev) if by_rev else declared_new(repo, mb, root=repo))
    new = new + (probed_new(repo, mb, rev) if by_rev else probed_new(repo, mb, root=repo))
    return (
        report(label, new, f"its merge base {mb[:9]} with {name}")
        if new
        else _clean(label, f"its merge base {mb[:9]} with {name}")
    )


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)  # the reader of a pipe (head) closed it
