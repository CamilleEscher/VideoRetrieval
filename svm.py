from sklearn.svm import SVC
from sklearn import svm
from simulate import simulate
import numpy as np
from evaluation import *
import os

dataFolder = './gen_data/'
trainFile = 'train.txt'
trainLabels = 'trainLabels.txt'
testFile = 'test.txt'
testLabels = 'testLabels.txt'
eventNb = 5
keyframeNb = 10
if not os.path.isdir(dataFolder) :
	os.makedirs(dataFolder)
simulate(5, 3, 100, dataFolder + 'train.txt', dataFolder + 'trainLabels.txt', 2)
simulate(5, 3, 100, dataFolder + 'test.txt', dataFolder + 'testLabels.txt', 3)

try :


#Training
	X = []
	Y = []
	with open(dataFolder + trainFile, 'r') as fTrain :
		for line in fTrain :
			line = line.replace('[', '')
			line = line.replace(']', '')
			line = line.replace('\n', '')
			keyframeList = list(line.split(', '))
			keyframeMean = []
			for x in range(0, eventNb) :
				keyframeMean.append(0.0)
			for elem in keyframeList :
				for x in range(0, eventNb) :
					if keyframeList.index(elem) % eventNb == x :
						keyframeMean[x] += float(elem)
			for x in range(0, eventNb) :
				keyframeMean[x] /= keyframeNb
			X.append(keyframeMean)
	with open(dataFolder + trainLabels, 'r') as labels :
		for line in labels :
			Y.append(float(line))
	svmClass = svm.SVC().fit(X, Y)

#Testing
	X = []
	Y = []
	with open(dataFolder + testFile, 'r') as fTest :
		for line in fTest :
			line = line.replace('[', '')
			line = line.replace(']', '')
			line = line.replace('\n', '')
			keyframeList = list(line.split(', '))
			keyframeMean = []
			for x in range(0, eventNb) :
				keyframeMean.append(0.0)
			for elem in keyframeList :
				for x in range(0, eventNb) :
					if keyframeList.index(elem) % eventNb == x :
						keyframeMean[x] += float(elem)
			for x in range(0, eventNb) :
				keyframeMean[x] /= keyframeNb
			X.append(keyframeMean)
	with open(dataFolder + testLabels, 'r') as labels :
		for line in labels :
			Y.append(float(line))

#Writing the results
	prediction = svmClass.predict(X)
	svmRes = open(dataFolder + 'testClassification.txt', 'w')
	for elem in prediction :
		svmRes.write(str(int(elem)))
		svmRes.write('\n')
	svmRes.close()

#Building the confusion matrix
	cMat = getConfusionMatrix(3, dataFolder, testLabels, 'testClassification.txt')
	print('Confusion matrix = ')
	print(cMat)

# Process Mean Average Precision
	# taking the 3d class into account
	MAP = getMAP(cMat, 3, {})
	print('MAP3 = ')
	print(MAP)
	# ignoring the 3d class
	MAP = getMAP(cMat, 3, {2})
	print('MAP2 = ')
	print(MAP)

except IOError:
	print('file not found')
