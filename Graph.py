import numpy as np
from math import *
import random
import copy
import os

class Graph :

# size, nature, layers, nodeIndexPerLayer and potentialChildrenCard are const after being initialized
# children, parents and kernels will change during the training 
	m_size = -1
	m_layers = []
	m_natures = []
	m_potentialChildrenCard = []
	m_nodeIndexPerLayer = []
	m_children = []
	m_parents = []
	m_kernels = []
	m_vertexNature = {
		'unknown' : -1,
		'before' : 0,
		'while' : 1,
		'whileNot' : 2,
		'leaf' : 3
	}

	def __init__(self, leafNodeCard, leafKernels) :
		# Get number of node per layer and set size
		cardOfCurrentLayer = leafNodeCard
		size = 0
		cardinalities = []
		while cardOfCurrentLayer > 1 :
			cardinalities.insert(0, cardOfCurrentLayer)
			cardOfCurrentLayer = int(ceil(cardOfCurrentLayer / 2.0))
			size += cardinalities[0]
		cardinalities.insert(0, 1)
		self.m_size = size + 1
		print("size = " + str(self.m_size))
		print("cardinalities = ")
		print(cardinalities)

		# Get list of latest indexes per layer
		lastIndexesPerLayer = [0 for x in range(len(cardinalities))]
		lastIndexesPerLayer[0] += cardinalities[0] - 1
		for i in range(1, len(cardinalities)) :
			lastIndexesPerLayer[i] += lastIndexesPerLayer[i - 1] + cardinalities[i]
		print("LastIndexesPerLayer = ")
		print(lastIndexesPerLayer)

		# Fill layers
		layers = [0 for x in range(self.m_size)]
		for i in range(self.m_size) :
			for j in range(len(lastIndexesPerLayer)) :
				if i <= lastIndexesPerLayer[j] :
					layers[i] = j
					break
		self.m_layers = layers
		print("layers = ")
		print(self.m_layers)

		# Fill natures
		natures = [self.m_vertexNature['unknown'] for x in range(self.m_size)]
		for i in range(self.m_size) :
			if self.m_layers[i] == self.m_layers[-1] :
				natures[i] = self.m_vertexNature['leaf']
			else :
				natures[i] = random.randrange(3)
		self.m_natures = natures
		print("natures = ")
		print(self.m_natures)

		# Fill kernels
		kernels = [np.zeros(leafKernels[0].shape) for x in range(self.m_size)]
		it = 0
		for i in range(self.m_size) :
			if self.m_natures[i] == self.m_vertexNature['leaf'] :
				kernels[i] = leafKernels[it]
				it += 1
		self.m_kernels = kernels
#print("kernels = ")
#print(self.m_kernels)

		# Fill children with parents
			# Fill m_potentialChildrenCard
		potentialChildrenCard = [(0, 0) for x in range(self.m_size)]
		for i in range(self.m_size) :
#			nat = self.m_natures[i]
# TEST
#if nat == self.m_vertexNature['beforeN'] or nat == self.m_vertexNature['whileNotN'] :
	   		potentialChildrenCard[i] = (2, 2)
#		 	elif nat == self.m_vertexNature['whileN'] :
#		 		maxCard = 0
#		 		layer = self.m_layers[i]
#		 		for l in self.m_layers :
#		 			if l == layer + 1 :
#		 				maxCard += 1
#		 		potentialChildrenCard[i] = (1, maxCard)
		self.m_potentialChildrenCard = potentialChildrenCard
		print("potentialChildrenCard = ")
		print(potentialChildrenCard)
		childrenCard = [0 for x in range(self.m_size)]
		print("childrenCard = ")
		print(childrenCard)
			# Fill m_nodeIndexPerLayer
		nodeIndexPerLayer = [[] for x in range(self.m_layers[-1] + 1)]
		currentLayer = 0
		for i in range(self.m_size) :
			if self.m_layers[i] != currentLayer :
				currentLayer = self.m_layers[i]
			nodeIndexPerLayer[currentLayer].append(i)
		self.m_nodeIndexPerLayer = nodeIndexPerLayer
		print("nodeIndexPerLayer = ")
		print(self.m_nodeIndexPerLayer)
		 	# Fill parents and children
		parents = [[] for x in range(self.m_size)]
		children = [[] for x in range(self.m_size)]
		layer = self.m_layers[-1]
		while(layer > self.m_layers[0]) :
			maxPotentialEdges = 0
			minPotentialEdges = 0
			for nodeId in self.m_nodeIndexPerLayer[layer - 1] :
				(minE, maxE) = self.m_potentialChildrenCard[nodeId]
				maxPotentialEdges += maxE
		   		minPotentialEdges += minE
		 	if maxPotentialEdges != minPotentialEdges :
	 			edgesCard = random.randrange(maxPotentialEdges - minPotentialEdges) + minPotentialEdges
			else :
				edgesCard = minPotentialEdges
			potentialParent = []
			priorPotentialParent = []
			for parentId in self.m_nodeIndexPerLayer[layer - 1] :
				if childrenCard[parentId] < potentialChildrenCard[parentId][1] :
					potentialParent.append(parentId)
					if childrenCard[parentId] < potentialChildrenCard[parentId][0] :
						priorPotentialParent.append(parentId)
			remainingNodes = len(self.m_nodeIndexPerLayer[layer])
			for childId in self.m_nodeIndexPerLayer[layer] :
				remainingNodes -= 1
				maxRemainingEdge = edgesCard - remainingNodes - 1
				if maxRemainingEdge > 0 :
					edgeCard = random.randrange(maxRemainingEdge) + 1
				else :
					edgeCard = 1
				edgesCard -= edgeCard
				totPotentialPar = copy.copy(potentialParent)
				priorPotentialPar = copy.copy(priorPotentialParent)
				for e in range(edgeCard) :
					if len(totPotentialPar) == 0 :
						break
					else :
						if len(priorPotentialPar) > 0 :
							parentId = priorPotentialPar[random.randrange(len(priorPotentialPar))]
							childrenCard[parentId] += 1
							if childrenCard[parentId] >= potentialChildrenCard[parentId][0] :
								priorPotentialParent.remove(parentId)
							if childrenCard[parentId] >= potentialChildrenCard[parentId][1] :
								potentialParent.remove(parentId)
								totPotentialPar.remove(parentId)
							priorPotentialPar.remove(parentId)
							parents[childId].append(parentId)
							children[parentId].append(childId)
						else :
							parentId = totPotentialPar[random.randrange(len(totPotentialPar))]
							childrenCard[parentId] += 1
							if childrenCard[parentId] == potentialChildrenCard[parentId][1] :
								potentialParent.remove(parentId)
							totPotentialPar.remove(parentId)
							parents[childId].append(parentId)
							children[parentId].append(childId)
				del priorPotentialPar
				del totPotentialPar
			layer = layer - 1
			print("edges : ")
			print(childrenCard)
		self.m_parents = parents
		print("parents = ")
		print(self.m_parents)
		self.m_children = children
		print("children = ")
		print(self.m_children)
						
#def addEdge(self, parentId, childId) :

#def removeEdge(self, parentId, childId) :

	def swap(self, parent1Id, child1Id, parent2Id, child2Id) :
		self.m_children[parent1Id].append(child2Id)
		self.m_children[parent2Id].append(child1Id)
		self.m_children[parent1Id].remove(child1Id)
		self.m_children[parent2Id].remove(child2Id)
		self.m_parents[child1Id].append(parent2Id)
		self.m_parents[child2Id].append(parent1Id)
		self.m_parents[child1Id].remove(parent1Id)
		self.m_parents[child2Id].remove(parent2Id)
		# TODO update kernels

	def size(self) :
		return self.m_size

	def hasEdge(self, parentId, childId) :
		return childId in self.m_children[parentId]

	def getChildren(self, parentId) :
		return self.m_children[parentId]

	def getParents(self, childId) :
		return self.m_parents[childId]

	def visualize(self, dataFolder) :
		dot = open(dataFolder + 'graph.dot', 'w')
		dot.write('graph G { \n')
		dot.write('\tedge [color="black"];\nnode [shape="circle", color="white", fontcolor="black", style="filled"];\n')
		for i in range(self.m_size) :
			key = [k for k, val in self.m_vertexNature.iteritems() if val == self.m_natures[i]][0]
			if key == 'whileNot' :
				dot.write('\t' + str(i) + ' [label="wN", ')
			else :
				dot.write('\t' + str(i) + ' [label="' + str(key)[0] + '", ')
			if key == 'leaf' :
				dot.write('shape="box", color="black", fontcolor="white"];\n')
			elif key == 'while' :
				dot.write('color="#E8D317"];\n')
			elif key == 'whileNot' :
				dot.write('color="#45EF8F"];\n')
			else :
				dot.write('color="#009463"];\n')

		for i in range(self.m_size - 1) :
			for j in self.m_children[i] :
				dot.write('\t' + str(i) + ' -- ' + str(j) + ' ;\n')
		dot.write('}')
		dot.close()
		os.system('dot -Tjpg -o' + dataFolder + 'graph.jpg graph.dot')
		os.system('display graph.jpg')
