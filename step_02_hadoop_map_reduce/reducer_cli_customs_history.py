import sys

key = ""
prevKey = None
prevDesc = None
sum = 0

for line in sys.stdin:
    key, value, desc = line.split("\t")
    if key != prevKey and prevKey is not None:
        print(prevKey+'\t'+str(sum)+'\t'+prevDesc.strip())
        sum = 0
    prevKey = key
    prevDesc = desc
    sum += int(value)

print(prevKey+'\t'+str(sum)+'\t'+prevDesc.strip())