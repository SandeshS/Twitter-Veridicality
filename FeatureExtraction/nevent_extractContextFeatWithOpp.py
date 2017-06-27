# This will be the final feature extractor based on Alan's code - now, the tweets have been preprocessed and no need to check for anything except TARGET and KEYWORD(optional)
# and generate the features. Need to ensure we get indices of all possible TARGET1 and TARGET2s
# Author - Sandesh Swamy, 2016

import sys
import csv
import ast
import nltk.sentiment.util

def isAscii(s):
    try:
        s.decode('ascii')
    except Exception:
        return False
    return True

def setFeature(features, feature):
    if isAscii(feature):
        features[feature] = 1

def computeEntityFeaturesTarget(tweet, tags, features):
	tgtidx = [i for i,x in enumerate(tweet) if x == "TARGET"]
	for idx in tgtidx:
		for k in [1, 2, 3, 4]:
			tarLeftContext = ""
			tarRightContext = ""
			leftContext = []
			rightContext = []
			for tidx in range(max(0,idx-k), idx):
				leftContext.append(tweet[tidx])
			for tidx in range(idx+1, min(idx+1+k, len(tweet))):
				rightContext.append(tweet[tidx])
			for item in leftContext:
				tarLeftContext += " " + item
			for item in rightContext:
				tarRightContext += " " + item
			tarLeftContext = tarLeftContext.strip()
			tarRightContext = tarRightContext.strip()
			setFeature(features, "CONTEXT: TARGET %s" % tarRightContext)
			setFeature(features, "CONTEXT: %s TARGET" % tarLeftContext)
			setFeature(features, "CONTEXT: %s TARGET %s" %(tarLeftContext, tarRightContext))

def computeOpponentFeatures(tweet, tags, features):
	tgtidx = [i for i,x in enumerate(tweet) if x == "OPPONENT"]
	for idx in tgtidx:
		for k in [1, 2, 3, 4]:
			oppLeftContext = ""
			oppRightContext = ""
			leftContext = []
			rightContext = []
			for tidx in range(max(0, idx-k), idx):
				leftContext.append(tweet[tidx])
			for tidx in range(idx+1, min(idx+1+k, len(tweet))):
				rightContext.append(tweet[tidx])
			for item in leftContext:
				oppLeftContext += " " + item
			for item in rightContext:
				oppRightContext += " " + item
			oppLeftContext = oppLeftContext.strip()
			oppRightContext = oppRightContext.strip()
			setFeature(features, "OPP CONTEXT: OPPONENT %s" % oppRightContext)
			setFeature(features, "OPP CONTEXT: %s OPPONENT" % oppLeftContext)
			setFeature(features, "OPP CONTEXT: %s OPPONENT %s" %(oppLeftContext, oppRightContext))


def computeEntityFeaturesTarget1(tweet, tags, features):
	tgtidx = [i for i,x in enumerate(tweet) if x == "TARGET1"]
	for idx in tgtidx:
		for k in [1, 2, 3, 4]:
			tarLeftContext = ""
			tarRightContext = ""
			leftContext = []
			rightContext = []
			for tidx in range(max(0, idx-k), idx):
				leftContext.append(tweet[tidx])
			for tidx in range(idx+1, min(idx+1+k, len(tweet))):
				rightContext.append(tweet[tidx])
			for item in leftContext:
				tarLeftContext += " " + item
			for item in rightContext:
				tarRightContext += " " + item
			tarLeftContext = tarLeftContext.strip()
			tarRightContext = tarRightContext.strip()
			setFeature(features, "CONTEXT: TARGET1 %s" % tarRightContext)
			setFeature(features, "CONTEXT: %s TARGET1" % tarLeftContext)
			setFeature(features, "CONTEXT: %s TARGET1 %s" %(tarLeftContext, tarRightContext))


def computeEntityFeaturesTarget2(tweet, tags, features):
	tgtidx = [i for i,x in enumerate(tweet) if x == "TARGET2"]
	for idx in tgtidx:
		for k in [1, 2, 3, 4]:
			tarLeftContext = ""
			tarRightContext = ""
			leftContext = []
			rightContext = []
			for tidx in range(max(0, idx-k), idx):
				leftContext.append(tweet[tidx])
			for tidx in range(idx+1, min(idx+1+k, len(tweet))):
				rightContext.append(tweet[tidx])
			for item in leftContext:
				tarLeftContext += " " + item
			for item in rightContext:
				tarRightContext += " " + item
			tarLeftContext = tarLeftContext.strip()
			tarRightContext = tarRightContext.strip()
			setFeature(features, "CONTEXT: TARGET2 %s" % tarRightContext)
			setFeature(features, "CONTEXT: %s TARGET2" % tarLeftContext)
			setFeature(features, "CONTEXT: %s TARGET2 %s" %(tarLeftContext, tarRightContext))

def EndsWithExclamation(tweet, tags, features):
	last = tweet[-2].strip()
	if last == "!":
		setFeature(features, "Ends with !")

def EndsWithQuestion(tweet, tags, features):
	last = tweet[-2].strip()
	if last == "?":
		setFeature(features, "Ends with ?")

def EndsWithPeriod(tweet, tags, features):
	last = tweet[-2].strip()
	if last == ".":
		setFeature(features, "Ends with .")

def containsExclamation(twwet, tags, features):
	for i in range(len(tweet)-2):
		if "!" in tweet[i]:
			setFeature(features, "Contains !")
			break

def containsQuestion(tweet, tags, features):
	for i in range(len(tweet)-2):
		if "?" in tweet[i]:
			setFeature(features, "Contains ?")


def computeBOWFeatures(tweet, tags, features):
	#print len(tweet), len(tags)
	for i in range(len(tweet)):
		if not "MOD" in tags[i] and not "ENTITY" in tags[i] and not '@' in tweet[i] and not "START" in tags[i] and not "END" in tags[i]:
			setFeature(features, tweet[i])

def computeOpponentKeywordFeatures(o, k, tweet, tags, features):
	oidx = [i for i, x in enumerate(tweet) if x == o]
	kidx = [i for i,x in enumerate(tweet) if x.strip().lower() == k.lower()]
	for oid in oidx:
		for kid in kidx:
			fContext = []
			wordFeatures = ""
			if  oid<kid:
				for w in range(oid+1, kid):
					fContext.append(tweet[w])
			else:
				for w in range(kid+1, oid):
					fContext.append(tweet[w])
			for item in fContext:
				wordFeatures += " " + item
			wordFeatures = wordFeatures.strip()
			if len(wordFeatures) > 0:
				if oid < kid:
					setFeature(features, "PAIR CONTEXT: %s %s KEYWORD" % (o, wordFeatures))
				else:
					setFeature(features, "PAIR CONTEXT: KEYWORD %s %s" % (o, wordFeatures))

def distanceToKwd(entity, opp, kwd, tweet, tags, features):
	tidx = [i for i,x in enumerate(tweet) if x == entity]
	oppidx = [i for i,x in enumerate(tweet) if x == opp]
	kwdidx = [i for i,x in enumerate(tweet) if kwd in x.strip().lower()]
	print tweet
	print "target ids"
	print tidx
	print "opp ids"
	print oppidx
	print "kwd ids"
	print kwdidx
	if len(tidx) > 0 and len(kwdidx) > 0:
		tdistance = abs(tidx[0]-kwdidx[0])
		odistance = 99
		if len(oppidx) > 0:
			odistance = abs(oppidx[0]-kwdidx[0])
		if tdistance < odistance:
			setFeature(features, "TARGET closer to KEYWORD")
		else:
			setFeature(features, "OPPONENT closer to KEYWORD")

def entityHasNegation(t, k, tweet, tags, features):
	tidx = [i for i,x in enumerate(tweet) if x == t]
	kidx = [i for i,x in enumerate(tweet) if x.strip().lower() == k.lower()]
	tweetmod = nltk.sentiment.util.mark_negation(tweet)
	for tid in tidx:
		for kid in kidx:
			hasNegation = False
			if tid < kid:
				for w in range(tid, kid+1):
					if "NEG" in tweetmod[w]:
						hasNegation = True
						break
			else:
				for w in range(kid, tid+1):
					if "NEG" in tweetmod[w]:
						hasNegation = True
						break
			if hasNegation:
				setFeature(features, "Has Negation")


def computePairFeatures(t, k, tweet, tags, features):
	tidx = [i for i,x in enumerate(tweet) if x == t]
	kidx = [i for i,x in enumerate(tweet) if x.strip().lower() == k.lower()]
	for tid in tidx:
		for kid in kidx:
			fContext = []
			wordFeatures = ""
			if tid < kid:
				for w in range(tid+1, kid):
					fContext.append(tweet[w])
			else:
				for w in range(kid+1, tid):
					fContext.append(tweet[w])
			for item in fContext:
				wordFeatures += " " + item
			wordFeatures = wordFeatures.strip()
			if len(wordFeatures) > 0:
				if tid < kid:
					setFeature(features, "PAIR CONTEXT: %s %s KEYWORD" % (t,wordFeatures))
				else:
					setFeature(features, "PAIR CONTEXT: KEYWORD %s %s" % (wordFeatures,t))

def computePairFeatures2(t1, t2, tweet, tags, features):
	tidx = [i for i,x in enumerate(tweet) if x == t1]
	ttidx = [i for i,x in enumerate(tweet) if x == t2]
	for tid in tidx:
		for kid in ttidx:
			fContext = []
			wordFeatures = ""
			if tid < kid:
				for w in range(tid+1, kid):
					fContext.append(tweet[w])
			else:
				for w in range(kid+1, tid):
					fContext.append(tweet[w])
			for item in fContext:
				wordFeatures += " " + item
			wordFeatures = wordFeatures.strip()
			if len(wordFeatures) > 0:
				if tid < kid:
					setFeature(features, "PAIR CONTEXT: TARGET1 %s TARGET2" % wordFeatures)
				else:
					setFeature(features, "PAIR CONTEXT: TARGET2 %s TARGET1" % wordFeatures)


fp = open(sys.argv[1], 'r')
data = csv.reader(fp)

fp2 = open(sys.argv[1].replace(".csv", "_features.csv"), 'w')
fout = csv.writer(fp2)

fpneg = open("negative-words.txt", 'r')
#nwData = csv.reader(fpneg)

nWordDictionary = set()

for line in fpneg.readlines():
	nWordDictionary.add(line)

for row in data:
	dataForTweet = []
	features = {}
	tweet = ast.literal_eval(row[0])
	tags = ast.literal_eval(row[1])
	keyword = None
	if len(row) == 7:
		# need to check for TARGET, pair of TARGET and keyword
		keyword = "win"
		computeEntityFeaturesTarget1(tweet, tags, features)
		#computeBOWFeatures(tweet, tags, features)
		computePairFeatures("TARGET1", keyword, tweet, tags, features)
		computeOpponentFeatures(tweet, tags, features)
		computeOpponentKeywordFeatures("OPPONENT", keyword, tweet, tags, features)
		EndsWithExclamation(tweet, tags, features)
		EndsWithQuestion(tweet, tags, features)
		EndsWithPeriod(tweet, tags, features)
		containsQuestion(tweet, tags, features)
		containsExclamation(tweet, tags, features)
		# TODO - idea is to take the context between entity and keyword, check if negation exists
		# second is to check the distance of target to win and opponent to win and put a feature of closer distance 
		entityHasNegation("TARGET1", keyword, tweet, tags, features)
		distanceToKwd("TARGET1", "OPPONENT", keyword, tweet, tags, features)
	else:
		if "NFL" in row[-5]:
			computeEntityFeaturesTarget1(tweet, tags, features)
			computeEntityFeaturesTarget2(tweet, tags, features)
			#computeBOWFeatures(tweet, tags, features)
			computePairFeatures2("TARGET1", "TARGET2", tweet, tags, features)
			computeOpponentFeatures(tweet, tags, features)
			EndsWithExclamation(tweet, tags, features)
			EndsWithQuestion(tweet, tags, features)
			EndsWithPeriod(tweet, tags, features)
			containsQuestion(tweet, tags, features)
			containsExclamation(tweet, tags, features)
			entityHasNegation("TARGET1", "TARGET2", tweet, tags, features)
			distanceToKwd("TARGET1", "OPPONENT", "pick", tweet, tags, features)
			distanceToKwd("TARGET1", "OPPONENT", "choice", tweet, tags, features)
			distanceToKwd("TARGET1", "OPPONENT", "choose", tweet, tags, features)
		else:
			keyword = "win"
			computeEntityFeaturesTarget1(tweet, tags, features)
			computeEntityFeaturesTarget2(tweet, tags, features)
			#computeBOWFeatures(tweet, tags, features)
			computePairFeatures2("TARGET1", "TARGET2", tweet, tags, features)
			computePairFeatures("TARGET1", keyword, tweet, tags, features)
			computePairFeatures("TARGET2", keyword, tweet, tags, features)
			computeOpponentFeatures(tweet, tags, features)
			computeOpponentKeywordFeatures("OPPONENT", keyword, tweet, tags, features)
			EndsWithExclamation(tweet, tags, features)
			EndsWithQuestion(tweet, tags, features)
			EndsWithPeriod(tweet, tags, features)
			containsQuestion(tweet, tags, features)
			containsExclamation(tweet, tags, features)
			entityHasNegation("TARGET1", keyword, tweet, tags, features)
			entityHasNegation("TARGET2", keyword, tweet, tags, features)
			distanceToKwd("TARGET1", "OPPONENT", keyword, tweet, tags, features)
	for item in row:
		dataForTweet.append(item)
	dataForTweet.append(features)
	fout.writerow(dataForTweet)
