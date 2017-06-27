import csv
import sys

if len(sys.argv) != 2:
    print "Usage: python annotatedMace.py <csv>"

fp = open(sys.argv[1], "rb")
data = csv.reader(fp)

tweetDict = {}

for row in data:
    if not row[3] in tweetDict:
        tweetDict[row[3]] = {}
fp.seek(0,0)
data = csv.reader(fp)
for item in data:
    for key in tweetDict:
        if not item[1] in tweetDict[key]:
            tweetDict[key][item[1]] = ''
fpw = open(sys.argv[1].replace(".csv", "_mace_st1.csv"), "w")
csv_w = csv.writer(fpw, delimiter=',')

heading = ['tweetId']
fp.seek(0, 0)
data = csv.reader(fp)
for item in data:
    randrow = item
print randrow
for key in tweetDict[randrow[3]]:
    heading.append(key)
csv_w.writerow(heading)
    

fp.seek(0,0)
data = csv.reader(fp)
for row in data:
    tweetDict[row[3]][row[1]] = row[6]

for key in tweetDict:
    dataForItem = []
    dataForItem.append(key)
    for key2 in tweetDict[key]:
        dataForItem.append(tweetDict[key][key2])
    csv_w.writerow(dataForItem)
print tweetDict
