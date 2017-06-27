# add start and end tags to a tweet.
# Author - Sandesh Swamy, 2016

import sys
import csv

fp = open(sys.argv[1], 'r')
data = csv.reader(fp)

fp2 = open("new_events_final_tweets_with_Stag.csv", 'w')
fout = csv.writer(fp2)

import ast
for row in data:
    dataToWrite = []
    tweet = ast.literal_eval(row[0])
    tags = ast.literal_eval(row[1])
    #print tweet
    #print tags
    #print row
    tweet.insert(0, "<S>")
    tags.insert(0, "START")
    tweet.append("</S>")
    tags.append("END")
    dataToWrite.append(tweet)
    dataToWrite.append(tags)
    for i in range(2, len(row)):
        dataToWrite.append(row[i])
    fout.writerow(dataToWrite)
