import random
from learningProcess import *
import numpy as np

def buildPredecessors(cards) :
	predecessors = {}
	layerNb = len(cards)
	maxSuccessorNb = 2
	vertexIndexPerLayer = __getNodeIndexPerLayer(cards)
	remainingPredecessorsToLink = __getPredecessorsToLink(predecessors, vertexIndexPerLayer)
	for i in range(vertexIndexPerLayer[-1][-1] + 1) :
		predecessors[i] = []
	while len(remainingPredecessorsToLink) > 0 :
		predecessorId = remainingPredecessorsToLink.pop()
		layerOf = __getLayerOf(predecessorId, vertexIndexPerLayer)
		if layerOf < layerNb - 1 :
			verticesInNextLayer = vertexIndexPerLayer[layerOf + 1]
			remainingSuccessorsToLinkInLayer = __getUnlinkedSuccessorsInLayer(predecessors, verticesInNextLayer, (layerOf == layerNb - 2))
			if len(remainingSuccessorsToLinkInLayer) > 0 :
				successorId = remainingSuccessorsToLinkInLayer[random.randrange(len(remainingSuccessorsToLinkInLayer))]
				if predecessorId in predecessors[successorId] :
					remainingSuccessorsToLinkInLayer.remove(successorId)
					successorId = remainingSuccessorsToLinkInLayer[random.randrange(len(remainingSuccessorsToLinkInLayer))]
			else :
				adaptedSucessors = copy.copy(__getNodeIndexPerLayer(cards))[layerOf + 1]
				for potentialSuccessor in adaptedSucessors :
					if predecessorId in predecessors[potentialSuccessor] :
						adaptedSucessors.remove(potentialSuccessor)
				successorId = adaptedSucessors[random.randrange(len(adaptedSucessors))]
			predecessors[successorId].append(predecessorId)	
	return predecessors

def __getNodeIndexPerLayer(cards) :
	layerNb = len(cards)
	vertexIndexPerLayer = [[] for x in range(layerNb)]
	lastIndexPerLayer = [0 for x in range(layerNb)]
	lastIndexPerLayer[0] = cards[0] - 1
	for i in range(1, layerNb) :
		lastIndexPerLayer[i] = lastIndexPerLayer[i - 1] + cards[i]
	for i in range(layerNb) :
		if i == 0 :
			firstIndex = 0
		else :
			firstIndex = lastIndexPerLayer[i - 1]
		vertexIndexPerLayer[i].insert(0, lastIndexPerLayer[i])
		offset = 1
		while lastIndexPerLayer[i] - offset > firstIndex :
			vertexIndexPerLayer[i].insert(0, lastIndexPerLayer[i] - offset)
			offset += 1
	return vertexIndexPerLayer
			
def __getPredecessorsToLink(predecessors, vertexIndexPerLayer) :
	remainingPredecessorsToLink = []
	completeSuccessorsCard = [2 for x in range(vertexIndexPerLayer[-1][0])]
	for leafId in vertexIndexPerLayer[-1] :
		completeSuccessorsCard.append(0)
	currentSuccessorsCard = __getCurrentSuccessorsCards(predecessors, vertexIndexPerLayer)
	for predecessorId in range(len(currentSuccessorsCard)) :
		offset = 0
		while currentSuccessorsCard[predecessorId] + offset < completeSuccessorsCard[predecessorId] :
			remainingPredecessorsToLink.append(predecessorId)
			offset += 1
	return remainingPredecessorsToLink

def __getLayerOf(predecessorId, vertexIndexPerLayer) :
	layer = -1
	for verticesInLayer in vertexIndexPerLayer :
		for predId in verticesInLayer :
			if predId == predecessorId :
				layer = vertexIndexPerLayer.index(verticesInLayer)
	return layer

def __getUnlinkedSuccessorsInLayer(predecessors, vertexInNextLayer, isLeafLayer = False) :
	remainingSuccessorsToLinkInLayer = vertexInNextLayer
	for successorId in vertexInNextLayer :
		if predecessors[successorId] != [] :
			remainingSuccessorsToLinkInLayer.remove(successorId)
	return remainingSuccessorsToLinkInLayer

def __getCurrentSuccessorsCards(predecessors, vertexIndexPerLayer) :
	successorsCard = [0 for x in range(vertexIndexPerLayer[-1][-1] + 1)]
	if not __isEmpty(predecessors) :
		successors = __getSuccessors(predecessors)
		for predId in successors.keys() :
			successorsCard[predId] = len(successors[predId]) 
	return successorsCard

def __isEmpty(predecessors) :
	empty = True
	for i in predecessors.keys() :
		if len(predecessors[i]) > 0 :
			empty = False
	return empty

def __getSuccessors(predecessors) :
	successors = {}
	for successorId in predecessors.keys() :
		if successorId not in successors.keys() :
			successors[successorId] = []
		for predecessorId in predecessors[successorId] :
			if predecessorId in successors :
				successors[predecessorId].append(successorId)
			else :
				successors[predecessorId] = [successorId]
	return successors
				
def getNatures(predecessors, vertexNatures, layers) :
	natures = dict()
	for successorId in predecessors.keys() :
		layerOf = layers[successorId]
		if layerOf == -1 or layerOf == 3 :
			natures[successorId] = vertexNatures['leaf']
		elif layerOf == 0 :
			natures[successorId] = vertexNatures['while']
		elif layerOf == 1 :
			natures[successorId] = vertexNatures['before']
		else :
			natures[successorId] = vertexNatures['whileNot']
	return natures
	
def getValues(trainFilePath, labelFilePath, graph, vertexNatures, conceptNb, keyframeNb, classId) :
	valuesNb = len(graph.m_successors)
	posValues = [[] for x in range(valuesNb)]
	negValues = [[] for x in range(valuesNb)]
	startLeafValues = valuesNb - conceptNb * keyframeNb
	for concept in range(conceptNb * keyframeNb) :
		(posValue, negValue) = getTrainingVectors(conceptNb, keyframeNb, trainFilePath, labelFilePath, classId, concept)
		posValues[startLeafValues + concept] = posValue
		negValues[startLeafValues + concept] = negValue
	return (posValues, negValues)

def getTestValues(trainFilePath, labelFilePath, graph, vertexNatures, conceptNb, keyframeNb, classId) :
	valuesNb = len(graph.m_successors)
	values = [[] for x in range(valuesNb)]
	startLeafValues = valuesNb - conceptNb * keyframeNb
	for concept in range(conceptNb * keyframeNb) :
		value = getTestTrainingVectors(conceptNb, keyframeNb, trainFilePath, labelFilePath, classId, concept)
		values[startLeafValues + concept] = value
	return values

def adaptEdges(graph, vertexNatures, natures) :
	for successorId in graph.m_predecessors.keys() :
		predecessors = copy.copy(graph.m_predecessors[successorId])
		if len(predecessors) > 1 and graph.m_layers[successorId] == vertexNatures['leaf'] - 1 :
			priorPred = -1
			for pred in predecessors :
				predOfPredecessors = graph.m_predecessors[pred][0]
				if graph.m_successors[predOfPredecessors][0] == pred :
					priorPred = pred
				indexInPred = graph.m_successors[pred].index(successorId)
				siblingSuccessorId = graph.m_successors[pred][1 - indexInPred]
				if (indexInPred == 0 and priorPred == pred) or (indexInPred == 1 and priorPred != pred) :
					swapBranches(graph, (pred, successorId, pred, siblingSuccessorId))
	adaptLeafEdges(graph, vertexNatures, natures)
	return graph

# for each predecessor of a leaf, get the appropriate batch according to its before predecessor
# check if the successors are in the right batch
# otherwise, replace the successor by a random successor in the batch
def adaptLeafEdges(graph, vertexNatures, natures) :
	predecessorOfLeaves = []
	for i in graph.m_successors :
		for successor in graph.m_successors[i] :
			if graph.m_layers[successor] == vertexNatures['leaf'] :
				predecessorOfLeaves.append(i)
	for pred in predecessorOfLeaves :
		beforePred = graph.m_predecessors[pred][0]
		edgePrio = 1
		if graph.m_successors[beforePred][0] == pred :
			edgePrio = 0
		listOfLeaves = getPotentialSuccessors(beforePred, edgePrio, natures, vertexNatures, graph.m_successors)
		for successorId in graph.m_successors[pred] :
			successorPos = graph.m_successors[pred].index(successorId)
			if successorId not in listOfLeaves :
				graph.m_successors[pred].remove(successorId)
				graph.m_predecessors[successorId].remove(pred)
				newSuccessor = listOfLeaves[random.randrange(len(listOfLeaves))]
				while newSuccessor in graph.m_successors[pred] :
					newSuccessor = listOfLeaves[random.randrange(len(listOfLeaves))]
				listOfLeaves.remove(newSuccessor)
				if successorPos == 0 :
					graph.m_successors[pred].insert(0, newSuccessor)
				else :
					graph.m_successors[pred].append(newSuccessor)
				graph.m_predecessors[newSuccessor].append(pred)
	return graph

def getTrainingVectors(eventNb, keyframeNb, trainFilePath, labelFilePath, classId, subEventTargetted) :
	positiveConcepts = []
	negativeConcepts = []
	sampleNb = sum(1 for line in open(trainFilePath))
	labels = [0 for x in range(sampleNb)]
	data = np.zeros((eventNb * keyframeNb, sampleNb))
	lineNb = -1
	with open(trainFilePath, 'r') as fTrain :
		for line in fTrain :
			lineNb += 1
			line = line.replace('[', '')
			line = line.replace(']', '')
			line = line.replace('\n', '')
			keyframeList = list(line.split(', '))
			for elem in keyframeList :
				data[keyframeList.index(elem), lineNb] = elem
	with open(labelFilePath, 'r') as fLabels :
		sample = 0
		for line in fLabels :
 			labels[sample] = int(line)
			sample += 1
	for sample in range(sampleNb) :
		if labels[sample] == classId :
			positiveConcepts.append(data[subEventTargetted, sample])
		else :
			negativeConcepts.append(data[subEventTargetted, sample])
	return (positiveConcepts, negativeConcepts)

def getTestTrainingVectors(eventNb, keyframeNb, trainFilePath, labelFilePath, classId, subEventTargetted) :
	sampleNb = sum(1 for line in open(trainFilePath))
	data = np.zeros((eventNb * keyframeNb, sampleNb))
	lineNb = -1
	with open(trainFilePath, 'r') as fTrain :
		for line in fTrain :
			lineNb += 1
			line = line.replace('[', '')
			line = line.replace(']', '')
			line = line.replace('\n', '')
			keyframeList = list(line.split(', '))
			for elem in keyframeList :
				data[keyframeList.index(elem), lineNb] = elem
	conceptsValues = data[subEventTargetted, :]
	return conceptsValues
