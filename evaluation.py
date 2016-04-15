import numpy as np

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
