"""Check a file for the barred words, non-ASCII bytes, floats and runs of three all-capitals words."""
import re
import sys

BARRED = ["today", "tonight", "not yet", "pending", "as it stands", "we", "our", "us",
          "await", "awaiting", "experiment", "honestly"]
exit_code = 0
for path in sys.argv[1:]:
    data = open(path, "rb").read()
    if any(b > 127 for b in data):
        print(path, "non-ASCII byte")
        exit_code = 1
    text = data.decode("ascii", errors="replace")
    low = text.lower()
    for w in BARRED:
        for m in re.finditer(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            print(path, "barred word", repr(w), "at", m.start(), repr(text[max(0, m.start() - 30):m.end() + 30]))
            exit_code = 1
    for m in re.finditer(r"\d\.\d", text):
        print(path, "float", repr(text[max(0, m.start() - 20):m.end() + 20]))
        exit_code = 1
    for n, line in enumerate(text.splitlines(), 1):
      for words in (re.findall(r"[A-Za-z][A-Za-z'\-]*", line), line.split()):
        run = 0
        for w in words:
            letters = re.sub(r"[^A-Za-z]", "", w)
            if len(letters) >= 1 and letters.isupper():
                run += 1
                if run >= 3:
                    print(path, "line", n, "run of capitals:", w, "in", line[:120])
                    exit_code = 1
                    break
            else:
                run = 0
print("clean" if exit_code == 0 else "flagged")
sys.exit(exit_code)
