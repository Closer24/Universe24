"""A flagged copy of src for the measured form (TQ2_FORM=1 from the environment; off, the head bit for bit): the Link's reach read alike from both ends, R_ij = 2 num p_i p_j Q_ij in place of 2 num p_i^2 Q_ij (the one-end pace), the neighbour's pace read through the Link (one Link). Usage: python make_copy_tq2.py <worktree> <copy_dir>"""
import os, shutil, sys
src, dst = os.path.join(sys.argv[1], "src"), os.path.join(sys.argv[2], "src")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "event_universe", "node.py")
t = open(p).read()
old = """        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)"""
new = """        clock, pace = readings.paces_of(self, c)
        if os.environ.get("TQ2_FORM") == "1" and np.ndim(pace):
            # the measured form (H-Torque-Of-The-Step-2): the reach 2 num p_i p_j Q_ij, both ends' paces alike
            found = rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)
            reaches = tuple(
                (pace + pace) * across(pace, port) * f * pair[0] for port, f in enumerate(factors)
            )
            return rule3.Rule(reaches, found.wall + found.wall - found.mass - sum(reaches), found.wall, found.mass)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)"""
assert t.count(old) == 1
t = t.replace(old, new).replace("import hashlib\n", "import hashlib\nimport os\n", 1)
open(p, "w").write(t)
print("copy at", dst)
