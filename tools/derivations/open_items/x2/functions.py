"""Hand X2: every function of a Python tree with its line range, and the branches on a row's kind.

Usage: python functions.py <root> <subdir> <out.json>
The kind branches are counted exactly as U2's c_acts_by_kind.py counts them (the attributes wronskian, rotation,
plane, quanta, held, motion_volume, axes, flux; the calls turns(), charged(), reads_content(), carried(); world.seed),
one count per test line, so the 127 of U2 is reproduced; beside it a wider count (EXTRA) of the other tests that name
a row's kind in disguise: the pair's equality (num == den), .name, .records/.width/.parts/.planes/.laid/.record,
.link_read/.power/.exponent, the registry's row_of/records_of/quanta_records/rows_of/sourcing, `index == world.seed`,
`direction == 1` (the inverse as a branch), os.environ (the toy's switches) and link_birth (the toy's modes).
"""
import ast
import json
import sys
from pathlib import Path

KIND_NAMES = ("wronskian", "rotation", "plane", "quanta", "held", "motion_volume", "axes", "flux")
KIND_CALLS = ("turns", "charged", "reads_content", "carried")
EXTRA_ATTRS = ("name", "records", "width", "parts", "planes", "laid", "record", "link_read", "power", "exponent",
               "write_wall", "fill", "rest", "reads", "holders", "level_weight", "write_weight")
EXTRA_CALLS = ("row_of", "records_of", "quanta_records", "rows_of", "sourcing", "start_records", "readers_of",
               "weight_of", "by_charge", "charge_of", "count_read", "is_im")


def names_in(test):
    found = []
    for node in ast.walk(test):
        if isinstance(node, ast.Attribute) and node.attr in KIND_NAMES:
            found.append(node.attr)
        if isinstance(node, ast.Attribute) and node.attr == "seed" and isinstance(node.value, ast.Attribute) and node.value.attr == "world":
            found.append("world.seed")
        if isinstance(node, ast.Call):
            callee = node.func
            name = callee.id if isinstance(callee, ast.Name) else (callee.attr if isinstance(callee, ast.Attribute) else "")
            if name in KIND_CALLS:
                found.append(name + "()")
    return found


def extra_in(test):
    found = []
    for node in ast.walk(test):
        if isinstance(node, ast.Attribute) and node.attr in EXTRA_ATTRS:
            found.append("." + node.attr)
        if isinstance(node, ast.Call):
            callee = node.func
            name = callee.id if isinstance(callee, ast.Name) else (callee.attr if isinstance(callee, ast.Attribute) else "")
            if name in EXTRA_CALLS:
                found.append(name + "()")
            if isinstance(callee, ast.Attribute) and callee.attr == "get" and isinstance(callee.value, ast.Attribute) and callee.value.attr == "environ":
                found.append("os.environ")
        if isinstance(node, ast.Compare):
            left = ast.unparse(node.left)
            rights = [ast.unparse(c) for c in node.comparators]
            texts = [left] + rights
            if any("pair[0]" in t for t in texts) and any("pair[1]" in t for t in texts):
                found.append("pair[0]==pair[1]")
            if left == "num" and rights == ["den"] or left == "abs(num)" and rights == ["den"]:
                found.append("num==den")
            if left == "direction" or left == "sense":
                found.append(left + "==")
            if left == "shape_" or left == "row" and rights == ["0"] or left == "k % 2":
                found.append("kind-in-disguise:" + left)
        if isinstance(node, ast.Attribute) and node.attr == "link_birth":
            found.append("link_birth")
        if isinstance(node, ast.Compare) and isinstance(node.left, ast.Name) and node.left.id == "line" and any(isinstance(op, ast.Is) for op in node.ops):
            found.append("line is self.phi")
    return found


def branches(tree):
    found = []
    for node in ast.walk(tree):
        tests = []
        if isinstance(node, ast.If | ast.While):
            tests.append(("if" if isinstance(node, ast.If) else "while", node.test))
        elif isinstance(node, ast.IfExp):
            tests.append(("ternary", node.test))
        elif isinstance(node, ast.comprehension):
            tests.extend(("comprehension", t) for t in node.ifs)
        elif isinstance(node, ast.BoolOp):
            tests.append(("boolop", node))
        for shape, test in tests:
            names, extra = names_in(test), extra_in(test)
            if names or extra:
                found.append({"line": getattr(test, "lineno", getattr(node, "lineno", 0)), "shape": shape,
                              "names": sorted(set(names)), "extra": sorted(set(extra))})
    lines_seen, kept = set(), []
    for entry in sorted(found, key=lambda e: (e["line"], e["shape"] == "boolop")):
        if entry["shape"] == "boolop" and entry["line"] in lines_seen:
            continue
        lines_seen.add(entry["line"])
        kept.append(entry)
    return kept


def functions(tree):
    found = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            found.append((node.name, node.lineno, node.end_lineno))
        elif isinstance(node, ast.ClassDef):
            found.append((node.name, node.lineno, node.end_lineno))
            for inner in node.body:
                if isinstance(node, ast.ClassDef) and isinstance(inner, ast.FunctionDef):
                    found.append((node.name + "." + inner.name, inner.lineno, inner.end_lineno))
    return found


def main():
    root, sub, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    base = root / sub
    files = sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)
    report = {"root": str(root), "subdir": sub, "files": {}, "totals": {}}
    total_lines = total_kind = total_extra = total_functions = 0
    by_name, by_extra = {}, {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        lines = len(text.splitlines())
        funcs = functions(tree)
        kind = branches(tree)
        kind_only = [k for k in kind if k["names"]]
        extra_only = [k for k in kind if k["extra"] and not k["names"]]
        for k in kind_only:
            for n in k["names"]:
                by_name[n] = by_name.get(n, 0) + 1
        for k in kind:
            for n in k["extra"]:
                by_extra[n] = by_extra.get(n, 0) + 1
        rel = str(path.relative_to(base))
        per_function = []
        for name, start, end in funcs:
            inside_kind = [k["line"] for k in kind_only if start <= k["line"] <= end]
            inside_extra = [k["line"] for k in extra_only if start <= k["line"] <= end]
            per_function.append({"name": name, "start": start, "end": end, "lines": end - start + 1,
                                 "kind_branches": inside_kind, "extra_branches": inside_extra})
        report["files"][rel] = {"lines": lines, "functions": per_function, "kind_branches": kind_only,
                                "extra_branches": extra_only, "kind_count": len(kind_only), "extra_count": len(extra_only)}
        total_lines += lines
        total_kind += len(kind_only)
        total_extra += len(extra_only)
        total_functions += len([f for f in funcs if "." in f[0] or not f[0][0].isupper()])
    report["totals"] = {"files": len(files), "lines": total_lines, "functions_and_methods": total_functions,
                        "kind_branches_u2_method": total_kind, "extra_branches": total_extra,
                        "kind_by_attribute": dict(sorted(by_name.items())), "extra_by_term": dict(sorted(by_extra.items()))}
    Path(out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report["totals"], indent=1))
    for rel, entry in report["files"].items():
        if entry["kind_count"] or entry["extra_count"]:
            print(rel, "kind", entry["kind_count"], "extra", entry["extra_count"])


if __name__ == "__main__":
    main()
