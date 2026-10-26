"""Sleep until a file holds a word (the chain before this one done), polled every 15 s; no shell loop. Usage: python wait_file.py <file> <word>"""
import sys
import time

path, word = sys.argv[1], sys.argv[2]
while True:
    try:
        if word in open(path, encoding="utf-8").read():
            break
    except OSError:
        pass
    time.sleep(15)
