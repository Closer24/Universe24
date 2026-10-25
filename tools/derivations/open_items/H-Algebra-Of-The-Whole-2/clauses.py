"""Pull named clauses of docs/ALGEBRA.md to a bounded length, for the hand's reading (a reader, no act)."""
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
names = sys.argv[3:]
limit = int(sys.argv[2])
for name in names:
    k = text.find("**" + name)
    if k < 0:
        print("== MISSING", name)
        continue
    print("== " + name + " @char " + str(k))
    print(text[k : k + limit])
    print()
