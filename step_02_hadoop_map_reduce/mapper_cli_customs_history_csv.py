#!/usr/bin/env python3

import sys
import csv

def get_codes(file):
    map = {}
    with open(file) as f:
        for line in f:
            if not line:
                continue

            parts = line.split('\t')

            if len(parts) == 2:
                map[parts[0].strip()] = parts[1].strip()

    return map

# local cli test
#codes = get_codes(sys.argv[1])

# I feel like it would be better to do in a reduce stage, since the result would be the same
# yarn
codes = get_codes('customs_codes_descs')
# this is a mapper that expects CSV file input from BASH command line
reader = csv.reader(sys.stdin, delimiter='\t')
# maybe there is a more efficient way to skip first row with headers
header = next(reader)
# code (10-11 digits) + 1
for row in reader:
    # is used for Hadoop streaming, locally works without this if not row
    if not row:
        continue
    if row[0]:
        code = row[0].strip()
        desc = codes.get(code[:4], "ПРОЧЕЕ")
        print(row[0]+'\t1'+'\t'+desc.strip())