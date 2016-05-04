from sklearn.svm import SVC
from sklearn import svm
from evaluation import *
import os

def svmTraining(dataFolder, trainFile, testFile, trainLabels, testLabels, eventNb, keyframeNb, sampleNb) :
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
		print('Confusion matrix of the SVM method = \n' + str(cMat))

	# Process Mean Average Precision
		# taking the 3d class into account
		MAP3 = getMAP(cMat, 3, {})
		print('MAP3 = ' + str(MAP3))
		# ignoring the 3d class
		MAP2 = getMAP(cMat, 3, {2})
		print('MAP2 = ' + str(MAP2))

	except IOError:
		print('file not found')
	return (MAP2, MAP3)
