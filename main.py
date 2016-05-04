from Graph import Graph
from simulate import simulate
from evaluation import *
from graphBuilder import *
from learningProcess import *
from svm import *
import time
import random
import os

try :
	clockStart = time.time()

	# Generate simulated data
	print('Generation of the simulated data generation with 2 classes')
	eventNb = 5
	keyframeNb = 3
	sampleNb = 1000
	classNb = 2
	dataFolder = './gen_data/'
	trainFile = 'train.txt'
	trainLabels = 'trainLabels.txt'
	testFile = 'test.txt'
	testLabels = 'testLabels.txt'
	if not os.path.isdir(dataFolder) :
		os.makedirs(dataFolder)
	(targetSeq1Tr, targetSeq2Tr) = simulate(eventNb, keyframeNb, sampleNb, dataFolder + trainFile, dataFolder + trainLabels, classNb)
	(targetSeq1Te, targetSeq2Te) = simulate(eventNb, keyframeNb, sampleNb, dataFolder + testFile, dataFolder + testLabels, classNb + 1, (targetSeq1Tr, targetSeq2Tr))	
	trainTargets = [targetSeq1Tr, targetSeq2Tr]
	print('Target sequences of')
	print('class 1 = ' + str(trainTargets[0]))
	print('class 2 = ' + str(trainTargets[1]))

	print('\nBuilding and Training the 2 graphs (2 classes example)')

	# Build graphs for each class with random edges
	vertexNatures = {'unlinkedLeaf' : -1, 'while' : 0, 'before' : 1, 'whileNot' : 2, 'leaf' : 3}
	commands = {'stop' : -1, 'swap' : 0, 'pivot' : 1}
	argsCard = {commands['swap'] : 4, commands['pivot'] : 3, commands['stop'] : 0}
	targetSeq = []
	valuesPerClass = []
	graphs = []
	pred = buildPredecessors([1, 2, 3, 15])
	
	for i in range(classNb) :
		targetSeq = trainTargets[i]
		graph = Graph(predecessors = pred)
		nat = getNatures(pred, vertexNatures, graph.m_layers)
		graphs.append(adaptEdges(graph, vertexNatures, nat))
		(posVal, negVal) = getValues(dataFolder + trainFile, dataFolder + trainLabels, graphs[i], vertexNatures, eventNb, keyframeNb, i + 1)
		(posVal, negVal) = bottomUp(posVal, negVal, graphs[i].m_successors, graphs[i].m_layers, nat, vertexNatures)
		ratio = evaluate(posVal[0], negVal[0])

		# Training the graphs for each class (target sequence) 
		epoch = 0
		while(epoch < 100) :
			(posVal, negVal, ratio) = inferenceProcess(graphs[i], posVal, negVal, ratio, nat, vertexNatures, commands, argsCard)
			epoch += 1
		valuesPerClass.append((posVal, negVal))
		graphs[i].visualize(dataFolder, nat, eventNb, trainTargets[i])
		print('ratio = ' + str(ratio))

	# Testing the method
	print('\nTesting the method by evaluating the Confusion matrix (of the testing dataset where a third class with random values has been introduced) and the MAP - Mean Average Precision')
	testValues = []
	rootValuesPerClass = [0 for x in range(classNb)]
	for i in range(classNb) :
		graph = graphs[i]
		nat = getNatures(pred, vertexNatures, graph.m_layers)
		testValues = getTestValues(dataFolder + testFile, dataFolder + testLabels, graph, vertexNatures, eventNb, keyframeNb, i + 1)
		rootValuesPerClass[i] = bottomUpOnTests(testValues, graph.m_successors, graph.m_layers, nat, vertexNatures)[0]
	predictionPath = dataFolder + 'prediction.txt'
	if not os.path.isfile(predictionPath) :
		predictionFile = open(predictionPath, 'w')
		predictionFile.close()
	writePredictionFile(rootValuesPerClass, predictionPath, 2)
	
	# Evaluation of the method
	confusionMatrix = getConfusionMatrix(classNb + 1, dataFolder, testLabels, 'prediction.txt')
	print('Confusion matrix of our method =')
	print(confusionMatrix)
	MAP3m = getMAP(confusionMatrix, classNb + 1, {})
	print('MAP3 = ' + str(MAP3m))
	MAP2m = getMAP(confusionMatrix, classNb + 1, {2})
	print('MAP2 = ' + str(MAP2m))

	# Apply the SVM classification method
	print('\nComparison with svm classification method from the scikit-learn library on the same simulated data : ')
	(MAP2, MAP3) = svmTraining(dataFolder, trainFile, testFile, trainLabels, testLabels, eventNb, keyframeNb, sampleNb)

	# Compare the MAPs
	print('\nStatement of the benefits of the method : (MAPmethod - MAPsvm)')
	print('MAP2 diff = ' + '{:.2f}'.format(float(MAP2m - MAP2)))
	print('MAP3 diff = ' + '{:.2f}'.format(float(MAP3m - MAP3)))

except IOError :
	print("File not found")
