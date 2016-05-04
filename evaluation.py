import numpy as np

def writePredictionFile(rootValuesPerClass, predictionFilePath, classNb) :
	# get prediction
	prediction = []
	for valC1, valC2 in zip(rootValuesPerClass[0], rootValuesPerClass[1]) :
		ratio1 = (valC1) / float(valC2)
		ratio2 = 1.0 / float(ratio1)
		if ratio1 > ratio2 * (3 / 2.0) and ratio1 > 1 :
			prediction.append(1)
		elif ratio2 > ratio1 * (3 / 2.0) and ratio2 > 1 :
			prediction.append(2)
		else :
			prediction.append(3)
	# write results of prediction
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
