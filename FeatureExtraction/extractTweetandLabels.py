# This script takes an input file which is the consoloidated tweets, and their labels as obtained from MACE.
# Extract the tweet, tweetID and the labels from the file for consolidationg and forming dataset

import csv
import sys

fp = open(sys.argv[1])
data = csv.reader(fp)

fp2 = open(sys.argv[1].replace(".csv", "_formodel.csv"), 'w')
fout = csv.writer(fp2)

event  = "Presidential Elections"

counter = 0
for row in data:
    #Handles the heading
    if counter == 0:
        counter += 1
        continue
    else:
        dataForTweet = []
        dataForTweet.append(row[3]) #Tweet ID
        dataForTweet.append(row[2]) #Tweet
        dataForTweet.append(event)
        if len(row[5].split(' ')) > 6:
            entity2 = row[5].split(' ')[-2] + " " + row[5].split(' ')[-1].replace("?", "")
        else:
            entity2 = row[4].split(' ')[-1].replace("?","")
        entity1 = row[4].split(' ')[0]
        dataForTweet.append(entity1) #entity for event
        dataForTweet.append(entity2) #extra entity for elections
        dataForTweet.append(row[-2]) #MACE Veridicality label
        dataForTweet.append(row[-1]) #MACE desire label
        fout.writerow(dataForTweet)
