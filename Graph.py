import os
from graphBuilder import *

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
		cardinalities = getCards(leafNodeCard)
		self.m_size = getSize(cardinalities)
		# Get list of latest indexes per layer
		lastIndexesPerLayer = getLastIndexesPerLayer(cardinalities)
		# Fill layers
		self.m_layers = buildLayers(self.m_size, lastIndexesPerLayer)
		# Fill natures
		self.m_natures = buildNatures(self.m_vertexNature, self.m_size, self.m_layers)
		# Fill kernels
		self.m_kernels = initKernels(self.m_size, self.m_vertexNature, leafKernels)
		# Fill children with parents
			# Fill potentialChildrenCard
		self.m_potentialChildrenCard = getPotentialChildrenCard(self.m_size)
			# Fill nodeIndexPerLayer
		self.m_nodeIndexPerLayer = getNodeIndexPerLayer(self.m_size, self.m_layers)
		 	# Fill parents
		self.m_parents = getParents(self.m_size, self.m_layers, self.m_nodeIndexPerLayer, self.m_potentialChildrenCard)
			# Fill children
		self.m_children = getChildren(self.m_parents, self.m_size)
						
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
			if key == None :
				print("Null key")
				break
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
		os.system('dot -Tjpg -o' + dataFolder + 'graph.jpg ' + dataFolder + 'graph.dot')
		os.system('display ' + dataFolder + 'graph.jpg')
