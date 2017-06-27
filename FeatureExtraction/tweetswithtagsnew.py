# This is a script which takes the file with Named Entity tags and then separate the tags and the tokens
# 
# Author - Sandesh Swamy, 2016
import sys
import csv

fp = open(sys.argv[1], 'r')
#data = csv.reader(fp)

fp2 = open(sys.argv[2], 'r')
data2 = csv.reader(fp2)

remainingData = []

counter = 0
for row in data2:
    counter += 1
    remData = []
    remData.append(row[0])
    for i in range(2, len(row)):
        remData.append(row[i])
    remainingData.append(remData)

fp3 = open("new_event_tagged_data.csv", 'w')
fWrite = csv.writer(fp3)

finalData = []
idx = 0
for line in fp.readlines():
    tweet = []
    tags = []
    tweetData = line.strip().split(' ')
    for token in tweetData:
        splitData = token.split('/')
        datatweet = ''
        for i in range(0, len(splitData)-1):
            datatweet += splitData[i] + ' '
        tweet.append(datatweet)
        tags.append(splitData[-1])
    allData = []
    allData.append(tweet)
    allData.append(tags)
    for item in remainingData[idx]:
        allData.append(item)
    idx += 1
    finalData.append(allData)

for item in finalData:
    fWrite.writerow(item)
