#!/usr/bin/env python3

import sys

# We need to sort by count
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split('\t')
    if len(parts) >= 2:
        print(f"{parts[1]}\t{line}")