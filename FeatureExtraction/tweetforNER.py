# This script takes in a file - which has annotations with labels and the tweets
# This file  extracts just the tweets present in the input file and ignores  everything else

import sys
import csv

fp = open(sys.argv[1])
data = csv.reader(fp)

fp2 = open("new_event_tweets_for_ner.txt", 'w')

for row in data:
    fp2.writelines(row[1] + '\n')
