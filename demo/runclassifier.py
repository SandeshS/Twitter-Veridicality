import sys
import os
import csv
import re

try:
    import json
except ImportError:
    import simplejson as json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

#things needed to run NER in background 

import subprocess
import platform
import time
import codecs
import redis
import nltk

from signal import *

from optparse import OptionParser

BASE_DIR = 'twitter_nlp.jar'
print os.environ
if os.environ.has_key('TWITTER_NLP'):
    BASE_DIR = os.environ['TWITTER_NLP']

sys.path.append('%s/python' % (BASE_DIR))
sys.path.append('%s/python/ner' % (BASE_DIR))
sys.path.append('%s/hbc/python' % (BASE_DIR))

import Features
import twokenize
from LdaFeatures import LdaFeatures
from Dictionaries import Dictionaries
from Vocab import Vocab

sys.path.append('%s/python' % (BASE_DIR))
sys.path.append('%s/python/cap' % (BASE_DIR))

print sys.path
import numpy as np
import cap_classifier
import pos_tagger_stdin
import chunk_tagger_stdin
import event_tagger_stdin

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import csv
import ast
from Vocab import *
import pickle
###########################################################
# Helper functions
###########################################################
class LRmulticlass(object):
        def __init__(self):
                self.model = None
        
        def json2Vocab(self, jsonInstance):
                vocabd = {}
                for k in jsonInstance.keys():
                        vocabd[self.vocab.GetID(k)] = jsonInstance[k]
                return vocabd
        
        def json2Vector(self, jsonInstance):
                result = np.zeros(self.vocab.GetVocabSize())
                for k in jsonInstance.keys():
                        if self.vocab.GetID(k) > 0:
                                result[self.vocab.GetID(k)-1] = jsonInstance[k]
                return result
        
        def Train(self, jsonDataset):
                x, y = [d[0] for d in jsonDataset], [int(d[1]) for d in jsonDataset]
                self.vocab = Vocab()
                x_vocabd = [self.json2Vocab(d) for d in x]
                self.vocab.Lock()
                X_matrix = np.zeros((len(x_vocabd), self.vocab.GetVocabSize()))
                for i in range(len(x_vocabd)):
                        for (j,v) in x_vocabd[i].items():
                                X_matrix[i,j-1] = v
                lrmulti = LogisticRegression(solver='lbfgs', multi_class='multinomial')
                lrmulti.fit(X_matrix, np.array(y))
                self.model = lrmulti
        
        def Predict(self, jsonInstance):
		fsvoc = open("vocab_train.save", 'rb')
		self.vocab = pickle.load(fsvoc)
		self.vocab.Lock()
		#print self.vocab.GetVocabSize()
                return self.model.predict(self.json2Vector(jsonInstance).reshape(1,-1))
        
        def PredictProba(self, jsonInstance):
                return self.model.predict_proba(self.json2Vector(jsonInstance).reshape(1,-1))
        
        def printWeights(self, outFile):
                fwout = open(outFile, 'w')
                classes = self.model.coef_.shape[0]
                for i in range(classes):
                        fwout.write("Class %s\n" % i)
                        curCatWeights = self.model.coef_[i]
                        for j in np.argsort(curCatWeights):
                                try:
                                        fwout.write("%s\t%s\n" % (self.vocab.GetWord(j+1), curCatWeights[j]))
                                except KeyError:
                                        pass


def isAscii(s): 
    try:        
        s.decode('ascii')
    except Exception:
        return False
    return True               

def setFeature(features, feature):
    if isAscii(feature):
        features[feature] = 1

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

def containsQuestion(tweet, tags, features):
        for i in range(len(tweet)-2):
                if "?" in tweet[i]:
                        setFeature(features, "Contains ?")
def containsExclamation(tweet, tags, features):
        for i in range(len(tweet)-2):
                if "!" in tweet[i]:
                        setFeature(features, "Contains !")
                        break                               

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

def collapseEntityTags(tags, indices):
        start = indices[0]
        end = indices[1]
        del tags[start:end]
        tags.insert(start, "MOD")
        return tags

def modTweetTarTags(tags, indices):
        start = indices[0]
        end = indices[1]
        del tags[start:end]
        tags.insert(start, "MOD")
        return tags

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

def GetNer(ner_model):
    #return subprocess.Popen('java -Xmx256m -cp %s/mallet-2.0.6/lib/mallet-deps.jar:%s/mallet-2.0.6/class cc.mallet.fst.SimpleTaggerStdin --weights sparse --model-file %s/models/ner/%s' % (BASE_DIR, BASE_DIR, BASE_DIR, ner_model),
    return subprocess.Popen('java -Xmx512m -cp %s/mallet-2.0.6/lib/mallet-deps.jar:%s/mallet-2.0.6/class cc.mallet.fst.SimpleTaggerStdin --weights sparse --model-file %s/models/ner/%s' % (BASE_DIR, BASE_DIR, BASE_DIR, ner_model), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def GetLLda():
    return subprocess.Popen('%s/hbc/models/LabeledLDA_infer_stdin.out %s/hbc/data/combined.docs.hbc %s/hbc/data/combined.z.hbc 100 100' % (BASE_DIR, BASE_DIR, BASE_DIR), shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def recomputeScores():
    for item in scores:
	computedScores[item] = (scores[item]+ 1)/((scores[item] + len(scores))*1.0)

def displayScores():
    for item in computedScores:
	print str(item) + " : " + str(computedScores[item])


posTagger = pos_tagger_stdin.PosTagger()
chunkTagger = chunk_tagger_stdin.ChunkTagger()
eventTagger = event_tagger_stdin.EventTagger()
llda = GetLLda()

ner_model = 'ner.model'
ner = GetNer(ner_model)
fe = Features.FeatureExtractor('%s/data/dictionaries' % (BASE_DIR))


capClassifier = cap_classifier.CapClassifier()

vocab = Vocab('%s/hbc/data/vocab' % (BASE_DIR))

dictMap = {}
i = 1
for line in open('%s/hbc/data/dictionaries' % (BASE_DIR)):
    dictionary = line.rstrip('\n')
    dictMap[i] = dictionary
    i += 1

dict2index = {}
for i in dictMap.keys():
    dict2index[dictMap[i]] = i

if llda:
    dictionaries = Dictionaries('%s/data/LabeledLDA_dictionaries3' % (BASE_DIR), dict2index)
entityMap = {}
i = 0
if llda:
    for line in open('%s/hbc/data/entities' % (BASE_DIR)):
        entity = line.rstrip('\n')
        entityMap[entity] = i
        i += 1

dict2label = {}
for line in open('%s/hbc/data/dict-label3' % (BASE_DIR)):
    (dictionary, label) = line.rstrip('\n').split(' ')
    dict2label[dictionary] = label


#ACCESS_TOKEN = '38812730-H9OzvfbIIRZQL7VsIBKJxeSjEwyUv9jzUcM9XLcgt'
#ACCESS_SECRET = 'SJrwvxq4yWRsrAd7WptA5OykwyoiiWv7kUVAZ97486lBw'
#CONSUMER_KEY = 'WarwajW0eIduNIU2Kf64Ph2Ay'
#CONSUMER_SECRET = 'SEXzFbr8ArwuuGtrwE46dniq17SyDNXfHVqnWYfxj8u9pCsal0'

#oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

#twitter_stream = TwitterStream(auth=oauth)

#iterator = twitter_stream.statuses.filter(track="Trump", language="en")

infile = open(sys.argv[1])
print "Now processing event file....."
count = 0
event = ""
contenders = []
for line in infile.readlines():
    if count == 0:
        count += 1
        event = line.strip()
    else:
        contenders.append(line.strip())

#scores = {}
#for item in contenders:
#    scores[item] = 0

#computedScores = {}
#for item in contenders:
#    computedScores[item] = ((scores[item] + 1)*1.0)/len(contenders)

#formedQueries = []
#for item in contenders:
#    query = event + " " + item + " win"
#    formedQueries.append(query)

#print formedQueries

#completeTrack = ""
#for item in formedQueries:
#    completeTrack += item + ", "
#completeTrack.strip()


#print completeTrack, formedQueries
#iterator = twitter_stream.statuses.filter(track=completeTrack, language="en")

fp = open(sys.argv[2])
print "Now processing file with tweets....."
import csv
data = csv.reader(fp)

for row in data:
    tweet = row[0] #make sure the first column is tweet text
    #jdata = json.dumps(tweet)
    #ptweet = json.loads(jdata)
    #create a list with just the important fields of the tweet + metadata
    doi = []
    #print ptweet['id']
    #print ptweet['text']
    doi.append(event)
    foundEntity = False
    for item in contenders:
        if item.lower() in tweet.lower():
            doi.append(item)
            print "Found entity"
            foundEntity = True
        break
    if not foundEntity:
	continue
    doi.append(row[0]) #this is the tweet
    doi.append(row[1]) #this should be the created at timestamp
    doi.append(row[2]) #this should be the username
    doi.append(row[3]) #this should be the URL
    #doi[2] has the tweet data. We don't need to process for language and no need to remove dups since it is done one by one.
    fptname = "tweet.txt"
    #fpt = open("tweet.txt", 'w')
    print doi[2]
    #print type(doi[2])
    # fpt.writelines(str(doi[2].decode('utf-8')))
    #os.system('cd ../Twitter-NLP/twitter_nlp/')
    #os.system('export TWITTER_NLP=./')
    #os.system('cd -')
    #os.system('python python/ner/extractEntities.py ' + "../../demo/" + fptname + " > " + fptname.replace(".txt", ".out"))
    #os.system('cd -')
    #fpner = open("../Twitter-NLP/twitter_nlp/" + fptname.replace(".txt", ".out"))
    #need to create a new DS - tweet, tags, event, entities
    #dataForProcessing = []
    #keep track of items to be added
    tweetText = doi[2]
    tweetWords = twokenize.tokenize(tweetText)
    print tweetWords
    seq_features = []
    tags = []
        
    goodCap = capClassifier.Classify(tweetWords) > 0.9

    pos = posTagger.TagSentence(tweetWords)
    pos = [re.sub(r':[^:]*$', '', p) for p in pos]  # remove weights
    print pos

    word_pos = zip(tweetWords, [p.split(':')[0] for p in pos])
    chunk = chunkTagger.TagSentence(word_pos)
    chunk = [c.split(':')[0] for c in chunk]  # remove weights
    #print chunk

    events = eventTagger.TagSentence(tweetWords, [p.split(':')[0] for p in pos])
    events = [e.split(':')[0] for e in events]
    #print events

    quotes = Features.GetQuotes(tweetWords)
    for i in range(len(tweetWords)):
        features = fe.Extract(tweetWords, pos, chunk, i, goodCap) + ['DOMAIN=Twitter']
        if quotes[i]:
            features.append("QUOTED")
        seq_features.append(" ".join(features))
    ner.stdin.write(("\t".join(seq_features) + "\n").encode('utf8'))


    for i in range(len(tweetWords)):
        tags.append(ner.stdout.readline().rstrip('\n').strip(' '))
    #print "Tags before"
    #print tags
    tweetTags = []
    for i in range(len(tags)):
        tweetTags.append(tags[i])
    features = LdaFeatures(tweetWords, tags)

    for i in range(len(features.entities)):
        type = None
        wids = [str(vocab.GetID(x.lower())) for x in features.features[i] if vocab.HasWord(x.lower())]
        if llda and len(wids) > 0:
            entityid = "-1"
            if entityMap.has_key(features.entityStrings[i].lower()):
                entityid = str(entityMap[features.entityStrings[i].lower()])
            labels = dictionaries.GetDictVector(features.entityStrings[i])

            if sum(labels) == 0:
                labels = [1 for x in labels]
            llda.stdin.write("\t".join([entityid, " ".join(wids), " ".join([str(x) for x in labels])]) + "\n")
            sample = llda.stdout.readline().rstrip('\n')
            labels = [dict2label[dictMap[int(x)]] for x in sample[4:len(sample)-8].split(' ')]

            count = {}
            for label in labels:
                count[label] = count.get(label, 0.0) + 1.0
            maxL = None
            maxP = 0.0
            for label in count.keys():
                p = count[label] / float(len(count))
                if p > maxP or maxL == None:
                    maxL = label
                    maxP = p

            if maxL != 'None':
                tags[features.entities[i][0]] = "B-%s" % (maxL)
                for j in range(features.entities[i][0]+1,features.entities[i][1]):
                    tags[j] = "I-%s" % (maxL)
            else:
                tags[features.entities[i][0]] = "O"
                for j in range(features.entities[i][0]+1,features.entities[i][1]):
                    tags[j] = "O"
        else:
            tags[features.entities[i][0]] = "B-ENTITY"
            for j in range(features.entities[i][0]+1,features.entities[i][1]):
                tags[j] = "I-ENTITY"

    #print "Tags after"
    #print tags

    # now, we have tweet, tags, event, entity - we need to remove links from tweet
    tweetWords2 = []
    tweetTags2 = []

    for i in range(len(tweetTags)):
        if "http" in tweetWords[i] or "https" in tweetWords[i]:
            continue
        elif "pic." in tweetWords[i]:
            continue
        else:
            tweetWords2.append(tweetWords[i])
            tweetTags2.append(tweetTags[i])
    for i in range(len(tweetTags2)):
        if ":" in tweetTags2[i]:
            tweetTags2[i] = tweetTags2[i].split(":")[0]
        else:
            tweetTags2[i] = tweetTags2[i]
    #code below should be similar to ppnewevents.py and ppnewevents2.py - helps in replacing TARGET and OPPONENT
    # tweetWords2, tweetTags2, item = ent1, event
        
    ent1 = doi[1].strip()
    if len(ent1.split()) > 1:
        ent1 = ent1.split()[-1].strip()
    segments = getsegments(tweetWords2, tweetTags2, "ENTITY")
    for segment in segments:
        segEnt = segment[0].split()[-1].strip()
        print segEnt
        #print segEnt.lower(), ent1.lower()
        if segEnt.lower().strip() == ent1.lower().strip():
            tweetWords2 = modTweetTargetEnt1(tweetWords2, segment[1])
            tweetTags2 = modTweetTarTags(tweetTags2, segment[1])
    segments = getsegments(tweetWords2, tweetTags2, "ENTITY")
    for segment in segments:
        segEnt = segment[0].split()[-1].strip()
        for oppEnt in contenders:
            #print segEnt.lower(), oppEnt.lower()
            if segEnt.lower().strip() == oppEnt.lower().strip():
                tweetWords2 = modTweetTargetOpp(tweetWords2, segment[1])
                tweetTags2 = modTweetTarTags(tweetTags2, segment[1])
                break
    #print tweetWords2
    #print tweetTags2

    #now have code from pp2NewEvents.py
        
    ent1 = doi[1].strip()
    if len(ent1.split()) > 1:
        ent1 = ent1.split()[-1].strip()
    mtweetWords = removeHashTags(tweetWords2)
    for i in range(len(mtweetWords)):
        #print mtweet[i].strip().lower(), entity.lower()
        if ent1.lower() in mtweetWords[i].strip().lower():
            mtweetWords[i] = "TARGET1"
            tweetTags2[i] = "MOD"
	else:
	    for oppent in contenders:
		if oppent.lower() in mtweetWords[i].strip().lower():
		    mtweetWords[i] = "OPPONENT"
		    tweetTags2[i] = "MOD"
    mtweetWords = reinstateHT(mtweetWords, tweetWords2)

    segments = getsegments(mtweetWords, tweetTags2, "ENTITY")
    #print segments
    segment = None
    if len(segments) > 0:
            segment = segments[0]
    count = 1
    while segment != None:
            print segment
            #if not "Oscar" in segment[0] and not "NFL" in segment[0] and not "Ballon" in segment[0] and not "Eurovision" in segment[0] and not "World" in segment[0]:
            if not event in segment[0]:
                    mtweetWords = collapseEntities(mtweetWords, segment[1])
                    tweetTags2 = collapseEntityTags(tweetTags2, segment[1])
                    segments = getsegments(mtweetWords, tweetTags2, "ENTITY")
                    if len(segments) > 0:
                            segment = segments[0]
                    else:
                            segment = None
            elif count < len(segments):
                    segment = segments[count]
                    count += 1
            else:
                    segment = None

    print "Final  tweet and tags"
    # add START and END tags
    mtweetWords.insert(0, '<S>')
    mtweetWords.append('</S>')
    print tweetText
    print mtweetWords
    tweetTags2.insert(0, 'START')
    tweetTags2.append('END')
    print tweetTags2
    remainingData = []
    remainingData.append(event)
    remainingData.append(doi[1])
       
    #generate features using feature code
    tweetFeatures = {}
    keyword = "win"
    computeEntityFeaturesTarget1(mtweetWords, tweetTags2, tweetFeatures)
    computePairFeatures("TARGET1", keyword, mtweetWords, tweetTags2, tweetFeatures)
    computeOpponentFeatures(mtweetWords, tweetTags2, tweetFeatures)
    computeOpponentKeywordFeatures("OPPONENT", keyword, mtweetWords, tweetTags2, tweetFeatures)
    EndsWithExclamation(mtweetWords, tweetTags2, tweetFeatures)
    EndsWithQuestion(mtweetWords, tweetTags2, tweetFeatures)
    EndsWithPeriod(mtweetWords, tweetTags2, tweetFeatures)
    containsQuestion(mtweetWords, tweetTags2, tweetFeatures)
    containsExclamation(mtweetWords, tweetTags2, tweetFeatures)
    #entityHasNegation("TARGET1", keyword, mtweetWords, tweetTags2, tweetFeatures)
    distanceToKwd("TARGET1", "OPPONENT", keyword, mtweetWords, tweetTags2, tweetFeatures)
    print "generated features"
    print tweetFeatures
    fpdp = open("tweet1.txt", 'w')
    fpdp.writelines(str(tweetText.encode('utf-8')) + "\n")
    fpdp.close()
    os.system("bash tweeboparser/TweeboParser/run.sh tweet1.txt")
    storedDatadp = []
    fpdp = open("tweeboparser/TweeboParser/tweet1.txt.predict", 'r')
    for line in fpdp.readlines():
	storedDatadp.append(line.split('\t'))
    dpParse = []
    for item in storedDatadp:
	if len(item) == 1:
            break
	else:
	    wordData = []
	    wordData.append(item[1])
            wordData.append(item[-2])
	    wordData.append(item[3])
	    dpParse.append(wordData)
    #now, we can use dpParse, event and entity
    # code will be similar to nevent_creatematrix.py
    length = len(dpParse)
    edge = np.zeros((length+1, length+1))
    direction = np.zeros((length+1, length+1))
    for i in range(len(dpParse)):
        curWordIndex = i+1
        edgeIndex = int(dpParse[i][1])
        if edgeIndex <= 0:
            continue
        else:
            edge[curWordIndex][edgeIndex] = 1
            edge[edgeIndex][curWordIndex] =1
            direction[curWordIndex][edgeIndex] = 2
            direction[edgeIndex][curWordIndex] = 3
    #doi[1] is the entity
    curEntity = ""
    if len(doi[1].strip().split(' ')) > 1:
        curEntity = str(doi[1].strip().split(' ')[-1].lower())
    else:
        curEntity = str(doi[1].strip().lower())
    startIndices = []
    storePaths = []
    for i,attr in enumerate(dpParse):
        if curEntity in attr[0].lower():#and attr[-1] == "^":
            startIndices.append(i+1)
    for idx in startIndices:
        visit = set()
        path = ""
        DFSwithsource(edge, direction, visit, path, dpParse, idx, "win", storePaths)
    #print "store paths in between"
    #print storePaths
    for item in contenders:
        if not item.strip().lower() == curEntity.strip().lower():
            print item
            #Then it is an opponent entity
            oppIndices = []
            for i, attr in enumerate(dpParse):
                #print attr[0].lower()
                #print item.lower().strip(), attr[0].lower().strip()
                if item.lower().strip() in attr[0].lower():
                    print "added"
                    oppIndices.append(i+1)
            print oppIndices
            for idx in oppIndices:
                visit = set()
                path = ""
                DFSwithsourceopponent(edge, direction, visit, path, dpParse, idx, "win", storePaths)
    visit = set()
    danglingNegation(edge, visit, dpParse, "win", storePaths)
    print "parse tree features"
    print storePaths
    for item in storePaths:
	if not item in tweetFeatures:
	    tweetFeatures[item] = 1
    print "final features"
    print tweetFeatures
    fpmodelSaved = open('train.save', 'rb')
    lrModel = pickle.load(fpmodelSaved)
    resultVer = []
    probabilitiesVer = []
    threshold = 0.64
    resultVer.append(lrModel.Predict(tweetFeatures))
    probabilitiesVer.append(lrModel.PredictProba(tweetFeatures))
    if resultVer[0][0] == 1:
	print "predicted negative"
    elif resultVer[0][0] == 2:
	print "predicted neutral"
    else:
	print "predicted positive"
    #print "predicted label" + str(resultVer[0])
    print "predicted probability :" + str(probabilitiesVer[0][0][resultVer[0]-1])
    if resultVer[0] == 3 and probabilitiesVer[0][0][resultVer[0]-1] > threshold:
	print "Found positive veridicality for " + str(doi[1])
	#scores[item] = scores[item] + 1
	#recomputeScores()
    #print "Predictions for winners in %"
    #displayScores()
