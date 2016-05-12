import numpy as np
import os

def getPrediction(rootValuesPerClass, predictionFilePath, sampleNb) :
	classNb = len(rootValuesPerClass)
	posRatio = [0 for x in range(classNb)]
	negRatio = [0 for x in range(classNb)]
	posVal = 0
	negVal = 0
	prediction = []
	for sampleId in range(sampleNb) :
		for classId in range(classNb) :
			if len(rootValuesPerClass[classId]) > sampleId :
				posVal = rootValuesPerClass[classId][sampleId]
				for negativeClassId in range(classNb) :
					if negativeClassId != classId :
						negVal += rootValuesPerClass[negativeClassId][sampleId]
			negVal /= float(classNb)
			posRatio[classId] = (posVal) / float(negVal)
			negRatio[classId] = (negVal) / float(posVal)
		maxVal = 0
		classLabel = -1
		for iR in range(classNb) :
			if negRatio[iR] == 0 :
				classLabel = iR
				break
			else :
				val = posRatio[iR]
				if val > maxVal and negRatio[iR] < 1.0:
					maxVal = val
					classLabel = iR
			if iR == classNb - 1 and classLabel == -1 :
				val = posRatio[iR]
				if val > maxVal :
					maxVal = val
					classLabel = iR
		prediction.append(classLabel + 1)
	return prediction

def writePredictionFile(prediction, predictionFilePath) :
	if not os.path.isfile(predictionFilePath) :
		predictionFile = open(predictionFilePath, 'w')
		predictionFile.close()
	res = open(predictionFilePath, 'w')
	for elem in prediction :
		res.write(str(int(elem)))
		res.write('\n')
	res.close()
			

def getConfusionMatrix(classNb, dataFolder, labelFileName, predictionFileName) :
	lab = []
	pred = []
	with open(dataFolder + labelFileName, 'r') as labels :
		for line in labels :
			lab.append(float(line))
	with open(dataFolder + predictionFileName, 'r') as predictions :
		for line in predictions :
			pred.append(float(line))
	confusionMatrix = np.zeros( (classNb, classNb) )
	cardinalities = [0 for x in range(classNb)]
	for elem in range(len(lab)) :
		for classId in range(1, classNb + 1) :
			if lab[elem] == classId :
				cardinalities[classId - 1] += 1
				for predictionClassId in range(1, classNb + 1) :
					if pred[elem] == predictionClassId :
						confusionMatrix[classId - 1, predictionClassId - 1] += 1
	for i in range(len(cardinalities)) :
		confusionMatrix[i, :] /= float(cardinalities[i])
	return (confusionMatrix)

def getMAP(confusionMatrix, classNb, ignoredClasses) :
	MAP = 0
	for i in range(classNb) :
		if i not in ignoredClasses :
		 	MAP += confusionMatrix[i][i]
	return (MAP / float(classNb - len(ignoredClasses)))

def getLabelOfClassI(classId, labelFile, dataFolder) :
	labelClassIFile = dataFolder + 'trainingLabelClass.txt'
	Y = []
	with open(dataFolder + labelFile, 'r') as labels, open(labelClassIFile, 'w') as newLabels:
		for line in labels :
			line = line.replace('\n', '')
			if line[0] == str(classId) :
				newLabels.write('1\n')
				Y.append(1)
			else :
				newLabels.write('0\n')
				Y.append(0)
	return Y
