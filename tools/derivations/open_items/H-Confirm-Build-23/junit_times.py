"""The suite's times from artifacts/junit.xml: every test above 15 s, the chiral births test, the count and the sum (milliseconds, integers)."""
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
cases = [(int(round(float(c.get("time", "0")) * 1000)), c.get("classname", "") + "::" + c.get("name", ""), c) for c in root.iter("testcase")]
cases.sort(reverse=True)
fails = [n for _, n, c in cases if c.find("failure") is not None or c.find("error") is not None]
print("tests", len(cases), "sum ms", sum(t for t, _, _ in cases), "failed", len(fails))
for n in fails: print("FAILED", n)
for t, n, _ in cases:
    if t > 15000 or "chiral_seed_births" in n: print(t, "ms", n)
