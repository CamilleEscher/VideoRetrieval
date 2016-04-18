from math import *
import random
import numpy as np
import copy

def getCards(leafNodeCard) :
		cardOfCurrentLayer = leafNodeCard
		cardinalities = []
		while cardOfCurrentLayer > 1 :
			cardinalities.insert(0, cardOfCurrentLayer)
			cardOfCurrentLayer = int(ceil(cardOfCurrentLayer / 2.0))
		cardinalities.insert(0, 1)
		print("cardinalities = " + str(cardinalities))
		return cardinalities

def getSize(cardinalities) :
	size = 0
	i = 0
	while i < len(cardinalities) :
		size += cardinalities[i]
		i += 1
	print("size = " + str(size))
	return size

def getLastIndexesPerLayer(cardinalities) :
	lastIndexesPerLayer = [0 for x in range(len(cardinalities))]
	lastIndexesPerLayer[0] += cardinalities[0] - 1
	for i in range(1, len(cardinalities)) :
		lastIndexesPerLayer[i] += lastIndexesPerLayer[i - 1] + cardinalities[i]
	print("LastIndexesPerLayer = " + str(lastIndexesPerLayer))
	return lastIndexesPerLayer

def buildLayers(size, lastIndexesPerLayer) :
	layers = [0 for x in range(size)]
	layerCard = len(lastIndexesPerLayer)
	for i in range(size) :
		for j in range(layerCard) :
			if i <= lastIndexesPerLayer[j] :
				layers[i] = j
				break
	print("layers = " + str(layers))
	return layers

def buildNatures(vertexNature, size, layers) :
	natures = [vertexNature['unknown'] for x in range(size)]
	for i in range(size) :
		if layers[i] == layers[-1] :
			natures[i] = vertexNature['leaf']
		else :
			natures[i] = random.randrange(3)
	print("natures = " + str(natures))
	return natures

def initKernels(size, vertexNature, leafKernels) :
	kernels = [np.zeros(leafKernels[0].shape) for x in range(size)]
	natures = [-1 for x in range(size)]
	it = 0
	for i in range(size) :
		if natures[i] == vertexNature['leaf'] :
			kernels[i] = leafKernels[it]
			it += 1
#print("kernels = " + str(kernels))
	return kernels

def getPotentialChildrenCard(size) :
	potentialChildrenCard = [(0, 0) for x in range(size)]
	for i in range(size) :
	   	potentialChildrenCard[i] = (2, 2)
	print("potentialChildrenCard = " + str(potentialChildrenCard))
	return potentialChildrenCard

def getNodeIndexPerLayer(size, layers) :
	nodeIndexPerLayer = [[] for x in range(layers[-1] + 1)]
	currentLayer = 0
	for i in range(size) :
		if layers[i] != currentLayer :
			currentLayer = layers[i]
		nodeIndexPerLayer[currentLayer].append(i)
	print("nodeIndexPerLayer = " + str(nodeIndexPerLayer))
	return nodeIndexPerLayer

def getPotentialParents(layer, nodeIndexPerLayer, childrenCard, potentialChildrenCard) :
	extraPotentialParents = []
	priorPotentialParents = []
	for parentId in nodeIndexPerLayer[layer - 1] :
		i = 0
		currentCard = childrenCard[parentId]
		minPotentialCard = potentialChildrenCard[parentId][0]
		maxPotentialCard = potentialChildrenCard[parentId][1]
		while currentCard + i < minPotentialCard :
			priorPotentialParents.append(parentId)
			i += 1
		if (currentCard + i < maxPotentialCard) and (currentCard + i >= minPotentialCard) :
			j = 0
			while(currentCard + i + j < maxPotentialCard) :
				extraPotentialParents.append(parentId)
				j += 1
	print("extraPotentialParents = " + str(extraPotentialParents))
	print("priorPotentialParents = " + str(priorPotentialParents))
	return (extraPotentialParents, priorPotentialParents)

def getEdgesCardBoundaries(nodeIndexPerLayer, layer, potentialChildrenCard) :
	maxPotentialEdges = 0
	minPotentialEdges = 0
	for nodeId in nodeIndexPerLayer[layer - 1] :
		(minE, maxE) = potentialChildrenCard[nodeId]
		maxPotentialEdges += maxE
		minPotentialEdges += minE
	return (minPotentialEdges, maxPotentialEdges)

def getRandomEdgeCardForLayer(minPotentialEdges, maxPotentialEdges) :
	edgeCardForCurrentLayer = 0
	if maxPotentialEdges != minPotentialEdges :
	 	edgeCardForCurrentLayer = random.randrange(maxPotentialEdges - minPotentialEdges) + minPotentialEdges
	else :
		edgeCardForCurrentLayer = minPotentialEdges
	return edgeCardForCurrentLayer

def getChildrenOf(parents, parentId) :
	childrenOf = []
	for childId in range(len(parents)) :
		for p in parents[childId] :
			if p == parentId :
				childrenOf.append(childId)
	return childrenOf

def getParents(size, layers, nodeIndexPerLayer, potentialChildrenCard) :
	parents = [[] for x in range(size)]
	childrenCard = [0 for x in range(size)]
	print("childrenCard = " + str(childrenCard))
	layer = layers[-1]
	while(layer > layers[0]) :
		(minPotE, maxPotE) = getEdgesCardBoundaries(nodeIndexPerLayer, layer, potentialChildrenCard)
		edgeCardForCurrentLayer = getRandomEdgeCardForLayer(minPotE, maxPotE)
		(extraPotParents, priorPotParents) = getPotentialParents(layer, nodeIndexPerLayer, childrenCard, potentialChildrenCard)
		remainingNodes = len(nodeIndexPerLayer[layer])
		for childId in nodeIndexPerLayer[layer] :
			remainingNodes -= 1
			maxRemainingEdge = edgeCardForCurrentLayer - remainingNodes + 1
			if maxRemainingEdge > 1 :
				if childId == nodeIndexPerLayer[layer][-1] :
					edgeCard = maxRemainingEdge
				else :
					edgeCard = random.randrange(maxRemainingEdge - 1) + 1
			else :
				edgeCard = 1
			edgeCardForCurrentLayer -= edgeCard
# choose and set new edges
			(childrenCard, parents, extraPotParents, priorPotParents) = updateParents(childId, size, extraPotParents, priorPotParents, edgeCard, childrenCard, potentialChildrenCard, parents)
		structureIssue = False
		while (len(priorPotParents) > 0 and not structureIssue) :
			for i in priorPotParents :
				potentialChildren = nodeIndexPerLayer[layer]
				children = getChildrenOf(parents, i)
				for j in children :
					if j in potentialChildren :
						potentialChildren.remove(j)
					else :
						print("j = " + str(j))
						print("children of " + str(i) + " " + str(children))
						print("potentialChildren = " + str(potentialChildren))
						print("parents = " + str(parents))
				if len(potentialChildren) == 0 :
					structureIssue = True
					print("Structural issue : node " + str(i) + " in layer " + str(layer - 1) + " can not fit the cardinality requirements")
				else :
					newChild = potentialChildren[random.randrange(len(potentialChildren))]
					parents[newChild].append(i)
					priorPotParents.remove(i)
				
		layer = layer - 1
		print("edges : " + str(childrenCard))
	print("parents = " + str(parents))
	return parents

def removeDuplicates(iList) :
	newList = []
	for i in iList :
		if i not in newList :
			newList.append(i)
	return newList

def updateParents(childId, size, ePP, pPP, edgeCard, childrenCard, potentialChildrenCard, parents) :
	remainingEPP = removeDuplicates(ePP)
	remainingPPP = removeDuplicates(pPP)
	listOfInterest = remainingEPP
	refList = ePP

	for e in range(edgeCard) :
		if len(remainingEPP) == 0 and len(remainingPPP) == 0 :
			break
		else :
			if len(remainingPPP) > 0 :
				listOfInterest = remainingPPP
				refList = pPP
			if len(listOfInterest) > 0 :
				parentId = listOfInterest[random.randrange(len(listOfInterest))]
				childrenCard[parentId] += 1
				listOfInterest.remove(parentId)
				if refList == ePP :
					ePP.remove(parentId)
				else :
					pPP.remove(parentId)
				parents[childId].append(parentId)
			else :
				print("list Of interest empty")
	return (childrenCard, parents, ePP, pPP)

def getChildren(parents, size) :
	children = [[] for x in range(size)]
	for i in range(size) :
		for j in range(size) :
			if j in parents[i] :
				children[j].append(i)	
	print("children = " + str(children))
	return children
