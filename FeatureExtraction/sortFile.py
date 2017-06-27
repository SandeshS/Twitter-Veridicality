# sort the consolidated annotations by the tweetid
import sys
import csv

fp =open(sys.argv[1], 'r')
data = csv.reader(fp)

dblList = []

for row in data:
    dblList.append(row)

dblList.sort(key=lambda x: x[3])
#sorted(dblList, key=itemgetter(3))

fp.close()

fp2 = open("consolidated_annot_930_nominations_sorted.csv", 'w')
fOut = csv.writer(fp2)

for item in dblList:
    fOut.writerow(item)

