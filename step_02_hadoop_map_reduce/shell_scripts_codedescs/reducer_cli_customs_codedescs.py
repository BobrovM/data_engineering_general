#!/usr/bin/env python3

import sys

key = ""
prevKey = None
prevDesc = None

# we are basically outing the newest version of the description in this reducer, since shuffle sort sorts by asc
for line in sys.stdin:
    key, desc = line.split("\t")
    key = key[:4] # codeyyyymmdd, get rid of the date part
    if key != prevKey and prevKey is not None:
        print(prevKey+'\t'+prevDesc.strip())
    prevKey = key
    prevDesc = desc

print(prevKey+'\t'+prevDesc.strip())