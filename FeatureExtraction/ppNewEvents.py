# Preprocess the tweets. For every tweet, go through words, replace with TARGET, ENTITY or OPPONENT
#
# Author - Sandesh Swamy, 2016

import sys
import ast
import os
import csv

ballonSet = set()
ballonFile = open("../all_ballon_contenders.txt", 'r')
for line in ballonFile.readlines():
    ballonSet.add(line.strip())
ballonFile.close()
#print ballonSet

cricketSet = set()
cricketFile = open("../all_cricket_contenders.txt", 'r')
for line in cricketFile.readlines():
    cricketSet.add(line.strip())
cricketFile.close()
#print cricketSet

eurovisionSet = set()
eurovisionFile = open("../all_eurovision_contenders.txt", 'r')
for line in eurovisionFile.readlines():
    eurovisionSet.add(line.strip())
eurovisionFile.close()
#print eurovisionSet

footballSet = set()
footballFile = open("../all_football_contenders.txt", 'r')
for line in footballFile.readlines():        
    footballSet.add(line.strip())
footballFile.close()
#print footballSet

indelectionSet = set()
indelectionFile = open("../all_indelection_contenders.txt", 'r')
for line in indelectionFile.readlines():        
    indelectionSet.add(line.strip())
indelectionFile.close()
#print indelectionSet

presidentialSet = set()
presidentialFile = open("../all_presidential_contenders.txt", 'r')
for line in presidentialFile.readlines():
    presidentialSet.add(line.strip())
presidentialFile.close()
#print presidentialSet

rugbySet = set()
rugbyFile = open("../all_rugby_contenders.txt", 'r')
for line in rugbyFile.readlines():
    rugbySet.add(line.strip())
rugbyFile.close()
#print rugbySet

tennisSet = set()
tennisFile = open("../all_tennis_contenders.txt", 'r')
for line in tennisFile.readlines():
    tennisSet.add(line.strip())
tennisFile.close()
#print tennisSet

#oscarSet = set()
#oscarFile = open("../Data_for_Mturk/all_oscar_nomination_candidates.txt", 'r')
#for line in oscarFile.readlines():
#	line = line.replace("The ", "")
#	oscarSet.add(line.strip())
#oscarFile.close()
#oscarFile = open("../Data_all_nominations/all_oscar_nomination_candidates.txt", 'r')
#for line in oscarFile.readlines():
#	line = line.replace("The ", "")
#	oscarSet.add(line.strip())
#oscarFile.close()

#electionSet = set()
#electionFile = open("../Data_for_Mturk/all_elections_nomination_candidates.txt", 'r')
#for line in electionFile.readlines():
#	electionSet.add(line.strip())
#electionFile.close()
#electionFile = open("../Data_all_nominations/all_elections_nomination_candidates.txt", 'r')
#for line in electionFile.readlines():
#	electionSet.add(line.strip())
#electionFile.close()

#nflSet = set()
#nflFile = open("../Data_for_Mturk/all_nfl_nomination_candidates.txt", 'r')
#for line in nflFile.readlines():
#	nflSet.add(str(line.strip().decode('ascii', 'ignore')))
#nflFile.close()
#nflFile = open("../Data_all_nominations/all_nfl_nomination_candidates.txt", 'r')
#for line in nflFile.readlines():
#	nflSet.add(str(line.strip().decode('ascii', 'ignore')))
#nflFile.close()

#oscarSet.remove("consolidated.tsv")
#nflSet.remove("NFLDraft")

#print oscarSet, electionSet, nflSet

def getsegments(tweet, annots, tag, lower=False, getIndices=True):
    result = []
    start = None
    for i in range(len(tweet)):
        if annots[i] == "B-%s" % tag:
            if start != None:
                if getIndices:
                    result.append((' '.join(tweet[start:i]), (start,i)))
                else:
                    result.append(' '.join(tweet[start:i]))
            start = i
        elif annots[i] == 'O' and start != None:
            if getIndices:
                result.append((' '.join(tweet[start:i]), (start, i)))
            else:
                result.append(' '.join(tweet[start:i]))
            start = None
    if start != None:
        if getIndices:
            result.append((' '.join(tweet[start:i]), (start, i)))
        else:
            result.append(' '.join(tweet[start:i]))
    if lower:
        if getIndices:
            result = [(x[0].lower(), x[1]) for x in result]
        else:
            result = [(x.lower()) for x in result]
    return result

def modTweetTarget(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tweet[start:end]
	tweet.insert(start, "TARGET")
	return tweet

def modTweetTargetEnt1(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tweet[start:end]
	tweet.insert(start, "TARGET1")
	return tweet

def modTweetTargetOpp(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tweet[start:end]
	tweet.insert(start, "OPPONENT")
	return tweet

def modTweetTargetEnt2(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tweet[start:end]
	tweet.insert(start, "TARGET2")
	return tweet


def modTweetTarTags(tags, indices):
	start = indices[0]
	end = indices[1]
	del tags[start:end]
	tags.insert(start, "MOD")
	return tags

###############################################################
# Main program
###############################################################

#input will be the file with tweet tokenized, tags, event, ID, entities and labels
fp = open(sys.argv[1], "r")
data = csv.reader(fp)

fpw = open("consolidated_tagged_preprocess1_ne.csv", 'w')
fout = csv.writer(fpw)

for row in data:
	dataForTweet = []
	tweet = ast.literal_eval(row[0])
	tags = ast.literal_eval(row[1])	
	
	#print segments
	if len(row) == 7: #all cases except elections - only one entity
		ent1 = row[-3].strip()
                if len(ent1.split()) > 1:
                    ent1 = ent1.split()[-1].strip()
		segments = getsegments(tweet, tags, "ENTITY")		
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
                        print segEnt
			#print segEnt.lower(), ent1.lower()
			if segEnt.lower().strip() == ent1.lower().strip():				
				tweet = modTweetTargetEnt1(tweet, segment[1])
				tags = modTweetTarTags(tags, segment[1])				
	else: #presidential and indian elections
		ent1 = row[-4].strip()
		ent2 = row[-3].split(" ")[-1].strip()
		segments = getsegments(tweet, tags, "ENTITY")	
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			#print segEnt.lower(), ent1.lower()
			if segEnt.lower().strip() == ent1.lower().strip():				
				tweet = modTweetTargetEnt1(tweet, segment[1])
				tags = modTweetTarTags(tags, segment[1])
		segments2 = getsegments(tweet, tags, "ENTITY")
		for segment in segments2:
			segEnt = segment[0].split()[-1].strip()
			print segEnt.lower(), ent2.lower()
			if segEnt.lower().strip() == ent2.lower().strip():				
				tweet =modTweetTargetEnt2(tweet, segment[1])
				tags = modTweetTarTags(tags, segment[1])		
	segments = []
	dataForTweet.append(tweet)
	dataForTweet.append(tags)
	for i in range(2, len(row)):
		dataForTweet.append(row[i])
	fout.writerow(dataForTweet)

fpw.close()
fp.close()

fp = open("consolidated_tagged_preprocess1_ne.csv", 'r')
data = csv.reader(fp)

fpw2 = open("consolidated_tagged_preprocess2_ne.csv", 'w')
fout2 = csv.writer(fpw2)


#oscarSet = list(oscarSet)
#for i in range(len(oscarSet)):
#	oscarSet[i] = oscarSet[i].split()[-1].strip()
#oscarSet = set(oscarSet)

for row in data:
	dataForTweet = []
	tweet = ast.literal_eval(row[0])
	tags = ast.literal_eval(row[1])
	segments =  getsegments(tweet, tags, "ENTITY")
	if "Ballon" in row[3]:#ballon case
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in ballonSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
	elif "Cricket" in row[3]:
		#cricket tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in cricketSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Eurovision" in row[3]:
		#eurovision tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in eurovisionSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Football" in row[3]:
		#football tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in footballSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Ind" in row[3]:
		#Indian Election tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in indelectionSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Presidential" in row[3]:
		#pres election tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in presidentialSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Rugby" in row[3]:
		#rugby tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in rugbySet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
        elif "Tennis" in row[3]:
		#eurovision tweet
		for segment in segments:
			segEnt = segment[0].split()[-1].strip()
			for oppEnt in tennisSet:
				#print segEnt.lower(), oppEnt.lower()
				if segEnt.lower().strip() == oppEnt.lower().strip():
					tweet = modTweetTargetOpp(tweet, segment[1])
					tags = modTweetTarTags(tags, segment[1])
					break
	#else:
		# NFL draft tweet
	#	for segment in segments:
	#		segEnt = segment[0].split()[-1].strip()
	#		for oppEnt in nflSet:
				#print segEnt.lower(), oppEnt.lower()
	#			if segEnt.lower() == oppEnt.lower():
	#				tweet = modTweetTargetOpp(tweet, segment[1])
	#				tags = modTweetTarTags(tags, segment[1])
	#				break
	segments = []
	dataForTweet.append(tweet)
	dataForTweet.append(tags)
	for i in range(2, len(row)):
		dataForTweet.append(row[i])
	fout2.writerow(dataForTweet)
fp.close()
fpw2.close()

# fp = open("consolidated_tagged_preprocess2.csv", 'r')
# data = csv.reader(fp)

# fpw = open("consolidated_tagged_preprocess3.csv", 'w')
# fout = csv.writer(fpw)

# for row in data:
# 	
