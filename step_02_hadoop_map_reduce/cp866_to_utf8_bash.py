import csv
import sys

filein = sys.stdin.buffer.read().decode('cp866')
filein = filein.splitlines()

reader = csv.reader(filein, delimiter='\x00')

for row in reader:
    print(row[0])