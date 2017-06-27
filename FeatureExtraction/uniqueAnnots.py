import sys
import csv

dictOfids = set() #set using lists

fp = open(sys.argv[1], 'r')
data = csv.reader(fp)

fp2 = open("consolidated_unique_nomination_tweets.csv", 'w')
fout = csv.writer(fp2)

for row in data:
    if not row[3] in dictOfids:
        fout.writerow(row)
        dictOfids.add(row[3])

fp.close()
fp2.close()
