import sys
import csv

# TNVED3 is encoded in cp866. The only other encoding which read this file was 1125.
sys.stdin.reconfigure(encoding='cp866')
# this is a mapper that expects CSV file input from BASH command line
reader = csv.reader(sys.stdin, delimiter='|')
# maybe there is a more efficient way to skip first row with headers
header = next(reader)
# category code (4 digits) + category description + year, since reducing will put out only the biggest year
for row in reader:
    # in TNVED3 dd.mm.yyyy, reform to yyyy.mm.dd for sort shuffle, where it will be code+yyyy+mm+dd
    datesplit = row[3].strip().split('.')
    date = datesplit[2].strip() + datesplit[1].strip() + datesplit[0].strip()
    print(row[0]+row[1]+date+'\t'+row[2])