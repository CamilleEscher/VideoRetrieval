from Graph import Graph
from simulateMultiClasses import simulate
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
	eventNb = 15
	keyframeNb = 5
	sampleNb = 100
	classNb = 4
	print('Generation of the simulated data generation with ' + str(classNb) + ' classes')
	dataFolder = './gen_data/'
	trainFile = 'train.txt'
	trainLabels = 'trainLabels.txt'
	testFile = 'test.txt'
	testLabels = 'testLabels.txt'
	randomClasses = {classNb}
	if not os.path.isdir(dataFolder) :
		os.makedirs(dataFolder)
	print('training')
	trainTargets = simulate(eventNb, keyframeNb, sampleNb, classNb, dataFolder + trainFile, dataFolder + trainLabels)
	if trainTargets == None :
		print('Programm stopped in main')
	else :
		print('testing')
		testTargets = simulate(eventNb, keyframeNb, sampleNb, classNb, dataFolder + testFile, dataFolder + testLabels, trainTargets, 1)
		print('testTargets = ' + str(testTargets))
		print('Target sequences of training')
		for classId in range(classNb) :
			print('class ' + str(classId) + ' = ' + str(trainTargets[classId]))

		print('\nBuilding and Training the graphs (' + str(classNb) + ' classes example)')

		# Build graphs for each class with random edges
		vertexNatures = {'unlinkedLeaf' : -1, 'while' : 0, 'before' : 1, 'whileNot' : 2, 'leaf' : 3}
		commands = {'stop' : -1, 'swap' : 0, 'pivot' : 1}
		argsCard = {commands['swap'] : 4, commands['pivot'] : 3, commands['stop'] : 0}
		targetSeq = []
		valuesPerClass = []
		graphs = []
		pred = buildPredecessors([1, keyframeNb - 1, keyframeNb, eventNb * keyframeNb])

		for i in range(classNb) :
			targetSeq = trainTargets[i]
			graph = Graph(predecessors = pred)
			nat = getNatures(pred, vertexNatures, graph.m_layers)
			graphs.append(adaptLeafEdges(graph, vertexNatures, nat))
			(posVal, negVal) = getValues(dataFolder + trainFile, dataFolder + trainLabels, graphs[i], vertexNatures, eventNb, keyframeNb, i + 1)
			(posVal, negVal) = bottomUp(posVal, negVal, graphs[i].m_successors, graphs[i].m_layers, nat, vertexNatures)
			ratio = evaluate(posVal[0], negVal[0])

			# Training the graphs for each class (target sequence) 
			epoch = 0
			while(epoch < 1000) :
				(posVal, negVal, ratio) = inferenceProcess(graphs[i], posVal, negVal, ratio, nat, vertexNatures, commands, argsCard)
				epoch += 1
			valuesPerClass.append((posVal, negVal))
			graphs[i].visualize(dataFolder, nat, eventNb, trainTargets[i])
			print('ratio = ' + str(ratio))
			
		# Testing the method
		print('\nTesting the method by evaluating the Confusion matrix (of the testing dataset where a class have been defined in addition to previous training classes with random values) and the MAP - Mean Average Precision')
		testValues = []
		rootValuesPerClass = [0 for x in range(classNb)]
		for i in range(classNb) :
			graph = graphs[i]
			nat = getNatures(pred, vertexNatures, graph.m_layers)
			testValues = getTestValues(dataFolder + testFile, dataFolder + testLabels, graph, vertexNatures, eventNb, keyframeNb, i + 1)
			rootValuesPerClass[i] = bottomUpOnTests(testValues, graph.m_successors, graph.m_layers, nat, vertexNatures)[0]
		predictionPath = dataFolder + 'prediction.txt'
		prediction = getPrediction(rootValuesPerClass, predictionPath, sampleNb)
		writePredictionFile(prediction, predictionPath)

		# Evaluation of the method
		confusionMatrix = getConfusionMatrix(classNb + 1, dataFolder, testLabels, 'prediction.txt')
		print('Confusion matrix of our method =')
		print(confusionMatrix)
		MAPTotm = getMAP(confusionMatrix, classNb + 1, {})
		print('MAPWithRandom = ' + str(MAPTotm))
		MAPMinm = getMAP(confusionMatrix, classNb + 1, randomClasses)
		print('MAPWithoutRandom = ' + str(MAPMinm))

		# Apply the SVM classification method
		print('\nComparison with svm classification method from the scikit-learn library on the same simulated data : ')
		(MAPMin, MAPTot) = svmTraining(dataFolder, trainFile, testFile, trainLabels, testLabels, eventNb, keyframeNb, sampleNb, classNb, randomClasses)
		# Compare the MAPs
		print('\nStatement of the benefits of the method : (MAPmethod - MAPsvm)')
		print('MAPMin diff = ' + '{:.2f}'.format(float(MAPMinm - MAPMin)))
		print('MAPTot diff = ' + '{:.2f}'.format(float(MAPTotm - MAPTot)))

except IOError :
	print("File not found")
