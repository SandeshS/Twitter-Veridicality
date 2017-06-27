# Given that we have the dependency parse structure, how do we make the matrix representation?
# This file takes as input a file containing the structure - a list of lists
# We use ast.literal_eval to evaluate as a list of lists.

import sys
import numpy as np
import ast
import csv

ballonSet = set()
ballonFile = open("../../data/all_ballon_contenders.txt", 'r')
for line in ballonFile.readlines():
    ballonSet.add(line.strip())
ballonFile.close()
#print ballonSet

cricketSet = set()
cricketFile = open("../../data/all_cricket_contenders.txt", 'r')
for line in cricketFile.readlines():
    cricketSet.add(line.strip())
cricketFile.close()
#print cricketSet

eurovisionSet = set()
eurovisionFile = open("../../data/all_eurovision_contenders.txt", 'r')
for line in eurovisionFile.readlines():
    eurovisionSet.add(line.strip())
eurovisionFile.close()
#print eurovisionSet

footballSet = set()
footballFile = open("../../data/all_football_contenders.txt", 'r')
for line in footballFile.readlines():
    footballSet.add(line.strip())
footballFile.close()
#print footballSet

indelectionSet = set()
indelectionFile = open("../../data/all_indelection_contenders.txt", 'r')
for line in indelectionFile.readlines():
    indelectionSet.add(line.strip())
indelectionFile.close()
#print indelectionSet

presidentialSet = set()
presidentialFile = open("../../data/all_presidential_contenders.txt", 'r')
for line in presidentialFile.readlines():
    presidentialSet.add(line.strip())
presidentialFile.close()
#print presidentialSet

rugbySet = set()
rugbyFile = open("../../data/all_rugby_contenders.txt", 'r')
for line in rugbyFile.readlines():
    rugbySet.add(line.strip())
rugbyFile.close()
#print rugbySet

tennisSet = set()
tennisFile = open("../../data/all_tennis_contenders.txt", 'r')
for line in tennisFile.readlines():
    tennisSet.add(line.strip())
tennisFile.close()
#print tennisSet


#oscarSet = set()
#oscarFile = open("./data/Data_for_Mturk/all_oscar_nomination_candidates.txt", 'r')
#for line in oscarFile.readlines():
#        line = line.replace("The ", "")
        #need just the last name. Can get that index and dependency parse autmatically handles whole entity
#        if len(line.split(' ')) > 1:
#            oscarSet.add(line.split(' ')[-1])
#        else:
#            oscarSet.add(line.strip())
#oscarFile.close()
#oscarFile = open("./data/Data_all_nominations/all_oscar_nomination_candidates.txt", 'r')
#for line in oscarFile.readlines():
#        line = line.replace("The ", "")
        #need just the last name. Can get that index and dependency parse autmatically handles whole entity
#        if len(line.split(' ')) > 1:
#            oscarSet.add(line.split(' ')[-1])
#        else:
#            oscarSet.add(line.strip())
#oscarFile.close()

#electionSet = set()
#electionFile = open("./data/Data_for_Mturk/all_elections_nomination_candidates.txt", 'r')
#for line in electionFile.readlines():
#        electionSet.add(line.strip())
#electionFile.close()
#electionFile = open("./data/Data_all_nominations/all_elections_nomination_candidates.txt", 'r')
#for line in electionFile.readlines():
#        electionSet.add(line.strip())
#electionFile.close()
#
#nflSet = set()
#nflFile = open("./data/Data_for_Mturk/all_nfl_nomination_candidates.txt", 'r')
#for line in nflFile.readlines():
#        nflSet.add(str(line.strip().decode('ascii', 'ignore')))
#nflFile.close()
#nflFile = open("./data/Data_all_nominations/all_nfl_nomination_candidates.txt", 'r')
#for line in nflFile.readlines():
#        nflSet.add(str(line.strip().decode('ascii', 'ignore')))
#nflFile.close()
#
#oscarSet.remove("consolidated.tsv")
#nflSet.remove("NFLDraft")

####################################
# DFS function
####################################
def DFSwithsourceopponent(e, d, visited, path, words, source, keyword, store):
    #print "path before - " + path 
    #print visited
    visited.add(source)
#    print words[source-1][0]
    path += words[source-1][0].lower()
    #print keyword
    if keyword in path:
        if keyword == "win":
            path = path.split()
            path[0] = "OPPONENT"
            path[-1] = "KEYWORD"
        else:
            path = path.split()
            path[0] = "OPPONENT"
            path[-1] = "TARGET2"
        modPath = ""
        for i in range(len(path)):
            modPath += path[i] + " "
        modPath = modPath.strip()
        #print "path " + keyword + "\t" ,
        #print modPath + "\t" ,
        if modPath not in store:
            modPath = normalizePath(modPath)
            store.append(modPath)
        return
    for i,edge in enumerate(e[source]):
        if edge == 1 and i not in visited:
            if d[source][i] == 2:
                #path += " in "
                DFSwithsourceopponent(e, d, visited, path + " <- ", words, i, keyword, store)
            else:
                #path += " out "
                DFSwithsourceopponent(e, d, visited, path + " -> ", words, i, keyword, store)


def DFSwithsource(e, d, visited, path, words, source, keyword, store):
    #print "path before - " + path 
    #print visited
    visited.add(source)
#    print words[source-1][0]
    path += words[source-1][0].lower()
    #print keyword
    if keyword in path:
        if keyword == "win":
            path = path.split()
            path[0] = "TARGET1"
            path[-1] = "KEYWORD"
        else:
            path = path.split()
            path[0] = "TARGET1"
            path[-1] = "TARGET2"
        modPath = ""
        for i in range(len(path)):
            modPath += path[i] + " "
        modPath = modPath.strip()
        #print "path " + keyword + "\t" ,
        #print modPath + "\t" ,
        if modPath not in store:
            modPath = normalizePath(modPath)
            store.append(modPath)
        return
    for i,edge in enumerate(e[source]):
        if edge == 1 and i not in visited:
            if d[source][i] == 2:
                #path += " in "
                DFSwithsource(e, d, visited, path + " <- ", words, i, keyword, store)
            else:
                #path += " out "
                DFSwithsource(e, d, visited, path + " -> ", words, i, keyword, store)

def formtweet(lwords):
    tweet = ""
    for item in lwords:
        tweet += item[0] + " "
    return tweet.strip()

def checkDanglingNegationWord(word):
    if word.lower().strip() == "won't" or word.lower().strip() == "doesn't" or word.lower().strip() == "not" or word.lower().strip() == "'t" or word.lower().strip() == "cannot" or word.lower().strip() == "can't" or word.lower().strip() == "couldn't":
        return True
    return False


def danglingNegation(matrix, visited, tweetWords, kwd, store):#TODO pass adjacency matrix and tweet to get the index of the words connected to keyword
    #first find index of keyword
    winIndices = []
    for i in range(len(tweetWords)):
        if "win" == tweetWords[i][0].strip().lower():
            winIndices.append(i+1) #store index of keyword
    #once we have all the winIndices, check matrix for that particular row and find one-hop words
    for item in winIndices:
        getRow = matrix[item]
        for idx, val in enumerate(getRow):
            if val == 1: #connected
                #need to check word[idx-1]
                isDangling = checkDanglingNegationWord(tweetWords[idx-1][0])
                if isDangling:
                    store.append("Dangling Negation")
                    break

def normalizePath(path):
    # for the input path provided, convert to standard form
    if "cannot" in path or "cant" in path or "can't" in path:
        normpath = "can -> not"
        if "cannot" in path:
            path = path.replace("cannot", normpath)
        elif "cant" in path:
            path = path.replace("cant", normpath)
        else:
            path = path.replace("can't", normpath)
    elif "wouldn't" in path or "wouldnt" in path:
        normpath = "would -> not"
        if "wouldn't" in path:
            path = path.replace("wouldn't", normpath)
        else:
            path = path.replace("wouldnt", normpath)
    elif "didn't" in path or "didnt" in path or "dint" in path:
        normpath = "did -> not"
        if "didn't" in path:
            path = path.replace("didn't", normpath)
        elif "didnt" in path:
            path = path.replace("didnt", normpath)
        else:
            path = path.replace("dint", normpath)
    elif "won't" in path or "wont" in path:
        normpath = "will -> not"
        if "won't" in path:
            path = path.replace("won't", normpath)
        else:
            path = path.replace("wont", normpath)
    elif "doesn't" in path or "doesnt" in path:
        normpath = "does -> not"
        if "doesn't" in path:
            path = path.replace("doesn't", normpath)
        else:
            path = path.replace("doesnt", normpath)
    elif "don't" in path or "dont" in path:
        normpath = "do -> not"
        if "don't" in path:
            path = path.replace("don't", normpath)
        else:
            path = path.replace("dont", normpath)

    return path

####################################
# Main functions
####################################

#now this file is a csv file and it also has entities. Easy to find start indices.
fp = open(sys.argv[1])
data = csv.reader(fp)

fp2 = open(sys.argv[1].replace(".csv", "_depfeat.csv"),'w')
fout = csv.writer(fp2)

counter = 1

for row in data:
    d2w = []
    #print "tweet " + str(counter)
    counter +=1
    modLine = ast.literal_eval(row[0])
    #testing
    #print modLine
    #print type(modLine)
    length = len(modLine)
    edge = np.zeros((length+1, length+1))
    direction = np.zeros((length+1, length+1))
    # The idea is to use two matrices. One will have just edges and the other one indicates incoming or outgoing
    # let 2 indicate incoming and 3 indicate outgoing
    for i in range(len(modLine)):
        curWordIndex = i+1
        edgeIndex = int(modLine[i][1])
        if edgeIndex <= 0:
            continue
        else:
            edge[curWordIndex][edgeIndex] = 1
            edge[edgeIndex][curWordIndex] =1
            direction[curWordIndex][edgeIndex] = 2
            direction[edgeIndex][curWordIndex] = 3
    #testing
    #print modLine
    #print edge
    #print direction
    #print '\n'
    #isNFL = False
    #for i in range(len(modLine)):
    #    if "NFL" in modLine[i][0]:
    #        isNFL = True

    entity1 = ""
    entity2 = ""
    #if len(row) == 3 and not isNFL:
    #    #there are two entities
    #    if len(row[1].strip().split(' ')) > 1:
    #        entity2 = str(row[1].strip().split(' ')[-1].lower())
    #    else:
    #        entity2 = str(row[1].strip().lower())
    #    entity1 = str(row[2].strip().lower())
        #print entity1, entity2
    #elif len(row) == 3 and isNFL:
        #there are two entities
    #    if len(row[1].strip().split(' ')) > 1:
    #        entity1 = str(row[1].strip().split(' ')[-1].lower())
    #    else:
    #        entity1 = str(row[1].strip().lower())
    #    entity2 = str(row[2].strip().lower())
        #print entity1, entity2
    #else:
    #    if len(row[1].strip().split(' ')) > 1:
    #        entity1 = str(row[1].strip().split(' ')[-1].lower())
    #    else:
    #        entity1 = str(row[1].strip().lower())
        #print entity1
    if len(row) == 4:
        #there are two entities
        if len(row[2].strip().split(' ')) > 1:
            entity1 = str(row[2].strip().split(' ')[-1].lower())
        else:
            entity1 = str(row[2].strip().lower())
        entity1 = str(row[3].strip().lower())
    else:
        #only one entity
        if len(row[2].strip().split(' ')) > 1:
            entity1 = str(row[2].strip().split(' ')[-1].lower())
        else:
            entity1 = str(row[2].strip().lower())

    startIndices = []
    for i,attr in enumerate(modLine):
        if entity1 in attr[0].lower():#and attr[-1] == "^":
            startIndices.append(i+1)
    #print startIndices
    #print str(modLine) + "\t" ,
    d2w.append(modLine)
    for idx in startIndices:
        visit = set()
        path = ""
        DFSwithsource(edge, direction, visit, path, modLine, idx, "win", d2w)
        if len(row) == 4:
            visit = set()
            path = ""
            DFSwithsource(edge, direction, visit, path, modLine, idx, entity2.lower(), d2w)
    #let us find indices of OPPONENT if present in tweet.
    curTweet = formtweet(modLine)
    print curTweet
    if "Cricket".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in cricketSet:
            if not item.strip().lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    elif "Tennis".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in tennisSet:
            if not item.strip().lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    elif "Rugby".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in rugbySet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    elif "Football".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in footballSet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    elif "Ballon".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in ballonSet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    elif "Eurovision".lower() in row[1].lower():
        #Oscar case opponents to be checked
        for item in eurovisionSet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    #print item.lower().strip(), attr[0].lower().strip()
                    if item.lower().strip() in attr[0].lower():
                        print "added"
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)

    elif "Indian".lower() in row[1].lower():
        #election opponents
        for item in indelectionSet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    if item.lower().strip()in attr[0].lower():
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
                    if len(row) == 4:
                        visit = set()
                        path = ""
                        DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, entity2.lower(), d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    else:
        #election opponents
        for item in presidentialSet:
            if not item.lower() == entity1.strip().lower():
                print item
                #Then it is an opponent entity
                oppIndices = []
                for i, attr in enumerate(modLine):
                    #print attr[0].lower()
                    if item.lower().strip()in attr[0].lower():
                        oppIndices.append(i+1)
                print oppIndices
                for idx in oppIndices:
                    visit = set()
                    path = ""
                    DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, "win", d2w)
                    if len(row) == 4:
                        visit = set()
                        path = ""
                        DFSwithsourceopponent(edge, direction, visit, path, modLine, idx, entity2.lower(), d2w)
        danglingNegation(edge, visit, modLine, "win", d2w)
    fout.writerow(d2w)
