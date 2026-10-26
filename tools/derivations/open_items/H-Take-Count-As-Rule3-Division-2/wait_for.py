"""Wait until a file holds a word, polling every 20 s (no shell loop). Usage: wait_for.py <file> <word>"""
import sys, time, os
while not (os.path.exists(sys.argv[1]) and sys.argv[2] in open(sys.argv[1]).read()):
    time.sleep(20)
print("seen", sys.argv[2])
