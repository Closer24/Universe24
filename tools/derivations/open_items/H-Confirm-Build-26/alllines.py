"""Every src .py at a sha: its lines, its defs and its function lines; one table per sha, the totals last."""
import ast, subprocess, sys
tree, shas = sys.argv[1], sys.argv[2].split(",")
def git(*a):
    return subprocess.run(["git", "-C", tree, *a], capture_output=True, text=True).stdout
for sha in shas:
    names = sorted(n for n in git("ls-tree", "-r", "--name-only", sha, "src").splitlines() if n.endswith(".py"))
    tm = tf = td = 0
    print("==", sha, "files", len(names))
    for n in names:
        src = git("show", sha + ":" + n)
        mod = len(src.splitlines())
        funcs = [x for x in ast.walk(ast.parse(src)) if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))]
        fl = sum(x.end_lineno - x.lineno + 1 for x in funcs)
        print("   %-44s %4d %4d %4d" % (n.replace("src/event_universe/", ""), mod, len(funcs), fl))
        tm += mod; tf += fl; td += len(funcs)
    print("    TOTAL module", tm, "defs", td, "function lines", tf)
