import csv
import sys
import ast

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
        elif (annots[i] == 'O' or annots[i] =="MOD") and start != None:
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

def removeHashTags(tweet):
	mtweet = []
	for word in tweet:
		mtweet.append(word.replace("#", ""))
	return mtweet

def reinstateHT(modtweet, tweet):
	for i in range(len(modtweet)):
		if not "TARGET" in modtweet[i] and not "OPPONENT" in modtweet[i]:
			modtweet[i] = tweet[i]
	ntweet = []
	for w in modtweet:
		ntweet.append(w)
	return ntweet

def collapseEntities(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tweet[start:end]
	tweet.insert(start, "ENTITY")
	return tweet

def collapseEntityTags(tweet, indices):
	start = indices[0]
	end = indices[1]
	del tags[start:end]
	tags.insert(start, "MOD")
	return tags


fp = open("consolidated_tagged_preprocess2_ne.csv", 'r')
data = csv.reader(fp)

fpw = open("consolidated_tagged_preprocess3_ne.csv", 'w')
fout = csv.writer(fpw)

for row in data:
	dataForTweet = []
	tweet = ast.literal_eval(row[0])
	tags = ast.literal_eval(row[1])
	if len(row) == 7:
		entity = row[-3].split()[-1].strip()
		mtweet = removeHashTags(tweet)
		for i in range(len(mtweet)):
			#print mtweet[i].strip().lower(), entity.lower()
			if mtweet[i].strip().lower() == (entity.lower()):
				mtweet[i] = "TARGET1"
				tags[i] = "MOD"
	else:
		entity1 = row[-4].split(" ")[-1].strip()
		entity2 = row[-3].split(" ")[-1].strip()
		mtweet = removeHashTags(tweet)
		for i in range(len(mtweet)):
			#print mtweet[i].strip().lower(), entity1.lower()
			if mtweet[i].strip().lower() == entity1.lower():
				mtweet[i] = "TARGET1"
				tags[i] = "MOD"
		for i in range(len(mtweet)):
			#print mtweet[i].strip().lower(), entity2.lower()
			if mtweet[i].strip().lower() == entity2.lower():
				mtweet[i] = "TARGET2"
				tags[i] = "MOD"
	mtweet = reinstateHT(mtweet, tweet)
	dataForTweet.append(mtweet)
	dataForTweet.append(tags)
	for i in range(2, len(row)):
		dataForTweet.append(row[i])
	fout.writerow(dataForTweet)

fp.close()
fpw.close()
# now we can collapse all segments of named entities
fp = open("consolidated_tagged_preprocess3_ne.csv", 'r')
data = csv.reader(fp)

fpw = open("consolidated_tagged_preprocess4_ne.csv", 'w')
fout = csv.writer(fpw)

for row in data:
	dataForTweet = []
	tweet = ast.literal_eval(row[0])
	tags = ast.literal_eval(row[1])
	segments = getsegments(tweet, tags, "ENTITY")
	#print segments
	segment = None
	if len(segments) > 0:
		segment = segments[0]
	count = 1
	while segment != None:
		print segment
		if not "Oscar" in segment[0] and not "NFL" in segment[0] and not "Ballon" in segment[0] and not "Eurovision" in segment[0] and not "World" in segment[0]:
			tweet = collapseEntities(tweet, segment[1])
			tags = collapseEntityTags(tags, segment[1])
			segments = getsegments(tweet, tags, "ENTITY")
			if len(segments) > 0:
				segment = segments[0]
			else:
				segment = None
		elif count < len(segments):
			segment = segments[count]
			count += 1
		else:
			segment = None

	# for i in range(len(segments)):
	# 	if not "Oscar" in segments[i][0] and not "NFL" in segments[i][0]:
	# 		tweet = collapseEntities(tweet, segments[i][1])
	# 		tags = collapseEntityTags(tweet, segments[i][1])
	# 		segments2 = getsegments(tweet, tags, "ENTITY")
	# 		segments[i+1] = segments2[0]
	dataForTweet.append(tweet)
	dataForTweet.append(tags)
	for i in range(2, len(row)):
		dataForTweet.append(row[i])
	fout.writerow(dataForTweet)
