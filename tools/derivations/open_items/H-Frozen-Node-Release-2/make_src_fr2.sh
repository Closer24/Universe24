#!/bin/sh
# fr2: the flagged copy of src made from the worktree's src by the 59-line diff out/src_fr2.diff (two gated edits: node.swap's mask on the frozen Nodes struck under the flag; interval.division's backward restore of a Node both frozen and turned to the pre-state the exchange returned). The flag FR2_RELEASE is read from the environment; unset, the copy is the head bit for bit (hole 60 record equal in every key but the rows' milliseconds).
cd "$(dirname "$0")"
rm -rf src_fr2 && cp -r ../../../../src src_fr2 && patch -p1 -d src_fr2 < out/src_fr2.diff
