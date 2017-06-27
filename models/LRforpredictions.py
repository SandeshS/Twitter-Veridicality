from __future__ import division
import sys
import numpy as np 
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import csv
import ast
from Vocab import *
import pickle

# data = load_iris()
# X = data.data
# y = data.target

# classifier = LogisticRegression(solver='lbfgs', multi_class='multinomial')
# classifier.fit(X, y)
# print classifier.coef_

# X_test = np.array(([ 6.8,  3.2,  5.9,  2.3], [ 4.6,  3.4,  1.4,  0.3]))
# print classifier.predict(X_test)

# print classifier.predict_proba(X_test)

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
				#print self.vocab.GetID(k)
				result[self.vocab.GetID(k)-1] = jsonInstance[k]
		return result

	def Train(self, jsonDataset):
		x, y = [d[0] for d in jsonDataset], [int(d[1]) for d in jsonDataset]
		self.vocab = Vocab()
		x_vocabd = [self.json2Vocab(d) for d in x]
		with open("vocab_train.save", 'wb') as vocabfile:
		    pickle.dump(self.vocab, vocabfile)
		self.vocab.Lock()
		X_matrix = np.zeros((len(x_vocabd), self.vocab.GetVocabSize()))
		for i in range(len(x_vocabd)):
			for (j,v) in x_vocabd[i].items():
				X_matrix[i,j-1] = v
		lrmulti = LogisticRegression(solver='lbfgs', multi_class='multinomial')
		lrmulti.fit(X_matrix, np.array(y))
		self.model = lrmulti
		#fsvocab = open('vocab_train.save', 'wb')
		#pickle.dump(self.vocab, fsvocab)
		#fsvocab.flush()

	def Predict(self, jsonInstance):
		with open("vocab_train.save", 'rb') as vocabfile:
		    self.vocab = pickle.load(vocabfile)
		self.vocab.Lock()
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
		#wStar = np.argsort(-self.model.coef_)
		# for i in range(self.model.coef_.shape[0]):
		# 	print "Category %s:" % i
		# 	for j in range(wStar.shape[1]):
		# 		print "%s\t%s\n" % (self.vocab.GetWord(wStar[i][j]), self.model.coef_[i][j])


import glob

fileinput = open(sys.argv[1], 'r')
testData = csv.reader(fileinput)

fpmodelSaved = open('train.save', 'rb')
lrModel = pickle.load(fpmodelSaved)
jsonInstance = []
#goldLabelDev = []
# majClassClassifier = []
for row in testData:
    jsonInstance.append(ast.literal_eval(row[-1]))

results = []
probabilities = []
linenums = []
threshold = 0.64
posveridtweets = 0
print "Recognized " + str(len(jsonInstance)) + " lines. Predicting labels now..."
for i in range(len(jsonInstance)):
    results.append(lrModel.Predict(jsonInstance[i]))
    probabilities.append(lrModel.PredictProba(jsonInstance[i]))
    if results[i] == 3 and  probabilities[i][0][results[i]-1] > threshold:
        posveridtweets += 1
        linenums.append(i+1)
                        
posCount = 0
neutCount = 0
negCount = 0
for item in results:
    if item == 3:
        posCount += 1
    elif item == 2:
        neutCount +=1
    elif item == 1:
        negCount += 1

fileout = open(sys.argv[1].replace(".csv", ".predict.csv"), 'w')
fout = csv.writer(fileout)

for item in results:
    d2w = []
    if item == 3:
	d2w.append("positive")
    elif item == 2:
	d2w.append("neutral")
    elif item == 1:
	d2w.append("negative")
    fout.writerow(d2w)

#print "results"
#print results

#print results
#print ''
#print probabilities
#print posCount, neutCount, negCount
#print "pos veridicality tweets"
#print posveridtweets
#print linenums

