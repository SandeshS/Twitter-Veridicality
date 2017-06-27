# This script takes two files - one containing parse tree structure, the other containing tweets and concerned entities
# Combining the parse tree structure with the entities to help run DFS
import csv
import sys

fp1 = open(sys.argv[1])

fp2 = open(sys.argv[2])
data = csv.reader(fp2)

fp3 = open(sys.argv[3], 'w')
fout = csv.writer(fp3)

allParses = []
for line in fp1.readlines():
    allParses.append(line)

#Change this part dependign on structure of the file.
allEntities = []
for row in data:
    entityList = []
    len(row)
    if len(row) == 7:
        entityList.append(row[-5])#Adding event info)
        entityList.append(row[-4])
        entityList.append(row[-3])
    else:
        entityList.append(row[-4])
        entityList.append(row[-3])
    allEntities.append(entityList)

print len(allParses), len(allEntities)

for i in range(len(allParses)):
    dataForTweet = []
    dataForTweet.append(allParses[i])
    for j in range(len(allEntities[i])):
        dataForTweet.append(allEntities[i][j])
    fout.writerow(dataForTweet)
