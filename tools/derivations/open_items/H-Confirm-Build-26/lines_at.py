"""The engine's own source lines at a sha (src/**.py, every line), and the footers of a range: one count per sha, one mark per commit."""
import subprocess, sys
tree = sys.argv[1]
def git(*a):
    return subprocess.run(["git", "-C", tree, *a], capture_output=True, text=True).stdout
for sha in sys.argv[2].split(","):
    names = [n for n in git("ls-tree", "-r", "--name-only", sha, "src").splitlines() if n.endswith(".py")]
    total = 0
    per = {}
    for n in names:
        c = len(git("show", sha + ":" + n).splitlines())
        per[n] = c
        total += c
    print(sha, "files", len(names), "src lines", total)
    for n, c in sorted(per.items(), key=lambda kv: -kv[1])[:4]:
        print("   ", n, c)
