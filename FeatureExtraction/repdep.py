# In this script, I try to find the separate parse tree representations for every tweet
# Using a particular tweet, we can separate it based on a new line with no content.
# All the content before the new line belongs to a particular tweet
# For now, we try to get the dependency edge information for every word.

import sys
import glob
import re

fp = open(sys.argv[1])
#the input file is tab separated. 0 indicates root, otherwise it indicates an incoming edge from the numbered node in dependency tree

storedData = []
for line in fp.readlines():
    #testing
    #print line
    #print line.split('\t')
    storedData.append(line.split('\t'))

#print storedData
#storedData now has a list of lists, for every word in tweets, and each tweet is seperated by a list of length = 1

fp2 = open("parsestructure_" + sys.argv[2] + ".txt", 'w')

tweetparse = []
for item in storedData:
    if len(item) == 1:
        fp2.writelines(str(tweetparse) + "\n")
        tweetparse = []
    else:
        wordData = []
        wordData.append(item[1]) #append the word
        wordData.append(item[-2]) #append the node number/incoming or outgoing
        wordData.append(item[3]) #append the POS tag
        tweetparse.append(wordData) #tweetparse will contain a list of lists for every tweet
