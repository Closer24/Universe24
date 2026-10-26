"""The function lines of the named modules at a sha: every def's own lines (its body to its end, the docstring within), the count of defs and the module's lines, so the mass leaving a fold is read per module and per name."""
import ast, subprocess, sys
tree, shas, mods = sys.argv[1], sys.argv[2].split(","), sys.argv[3].split(",")
def blob(sha, path):
    return subprocess.run(["git", "-C", tree, "show", sha + ":" + path], capture_output=True, text=True).stdout
for sha in shas:
    print("==", sha)
    tot_funcs, tot_lines, tot_mod = 0, 0, 0
    for m in mods:
        src = blob(sha, "src/event_universe/" + m)
        if not src:
            print("   ", m, "absent")
            continue
        t = ast.parse(src)
        funcs = [n for n in ast.walk(t) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        flines = sum(n.end_lineno - n.lineno + 1 for n in funcs)
        mod = len(src.splitlines())
        print("   ", m, "module", mod, "defs", len(funcs), "function lines", flines)
        tot_funcs += len(funcs); tot_lines += flines; tot_mod += mod
    print("    TOTAL module", tot_mod, "defs", tot_funcs, "function lines", tot_lines)
