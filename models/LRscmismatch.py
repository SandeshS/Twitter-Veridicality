from __future__ import division
import sys
import numpy as np 
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import csv
import ast
from Vocab import *

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
		lrmulti = LogisticRegression(solver='lbfgs', multi_class='multinomial', C=0.3)
		lrmulti.fit(X_matrix, np.array(y))
		self.model = lrmulti

	def Predict(self, jsonInstance):
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

tweetFile = open("./test/combined_events_test_48_final_dep_3classes_only_sports.csv", 'r')
tweetData = csv.reader(tweetFile)

tweetsList = []
for row in tweetData:
	tweetsList.append(ast.literal_eval(row[0]))

fptrain = open("./train/combined_events_final_training_with_dependency_3classes.csv", 'r')
trainData = csv.reader(fptrain)

fpdev = open("./test/combined_events_test_48_final_dep_3classes_only_sports.csv", 'r')
devData = csv.reader(fpdev)

errorFile = open("classification_errors_combined_48_with_dependency_" + sys.argv[1] + ".csv", 'w')
errOut = csv.writer(errorFile)

lrModel = LRmulticlass()
jsonDataset = []
if sys.argv[1] == "veridicality":
	for row in trainData:
		rowData = []
		rowData.append(ast.literal_eval(row[-1]))
		rowData.append(int(row[-3]))
		jsonDataset.append(rowData)
elif sys.argv[1] == "desire":
	for row in trainData:
		rowData = []
		rowData.append(ast.literal_eval(row[-1]))
		rowData.append(int(row[-2]))
		jsonDataset.append(rowData)
else:
	print "Missing argument! Add veridicality/desire argument at the end"
lrModel.Train(jsonDataset)

#prepare data for dev data
majClass = 2
jsonInstance = []
goldLabelDev = []
majClassClassifier = []
if sys.argv[1] == "veridicality":
	for row in devData:
		jsonInstance.append(ast.literal_eval(row[-1]))
		goldLabelDev.append(int(row[-3]))
		majClassClassifier.append(majClass)
elif sys.argv[1] == "desire":
	for row in devData:
		jsonInstance.append(ast.literal_eval(row[-1]))
		goldLabelDev.append(int(row[-2]))
		majClassClassifier.append(majClass)
else:
	print "argument needs to be veridicality/desire"
goldLabelDev = np.asarray(goldLabelDev)

#print goldLabelDev
results = []
probscores = []
for i in range(len(jsonInstance)):
	results.append(lrModel.Predict(jsonInstance[i]))
	probscores.append(lrModel.PredictProba(jsonInstance[i]))

#print len(goldLabelDev), len(results)
count = 0
for i in range(len(results)):
	if int(results[i]) == int(goldLabelDev[i]):
		count += 1
	else:
		errorData = []
		fullTweet = ""
		for item in tweetsList[i]:
			fullTweet += item + " "
		errorData.append(fullTweet)
		errorData.append("Gold Label - " + str(goldLabelDev[i]))
		errorData.append("Predicted Label - " + str(results[i][0]))
		#print "mismatch- " + str(tweetsList[i]) + " Gold Label- " + str(goldLabelDev[i]) + " Predicted label- " + str(results[i][0])
		errOut.writerow(errorData)

print "gold labels"
for i in range(len(goldLabelDev)):
	print str(goldLabelDev[i])

print ' '
print "predicted labels with score"
for i in range(len(results)):
	print str(results[i][0]), str(probscores[i])
	
accuracy = count/len(results)
print "Accuracy is %s" % (accuracy)

bCount = 0
for i in range(len(goldLabelDev)):
	if int(goldLabelDev[i]) == int(majClassClassifier[i]):
		bCount += 1

bAccuracy = bCount/len(results)
print "Baseline accuracy is %s" % (bAccuracy)

if sys.argv[1] == "veridicality":
	lrModel.printWeights("all_category_weights_combined_48_with_dependency_veridicality_new.csv")
elif sys.argv[1] == "desire":
	lrModel.printWeights("all_category_weights_combined_48_with_dependency_desire_new.csv")
