from graphBuilder import *
import os
import time

class Graph :
	
	m_successors = {}
	m_predecessors = {}
	m_layers = {}
	m_depth = 0
	
	def __init__(self, predecessors = dict()) :
		if self.__isValid(predecessors) :
			if not self.__hasRoot(predecessors) :
				predecessors = self.__addRoot(predecessors)
			self.m_predecessors = predecessors
			self.m_successors = self.__initSuccessors()
			self.__initLayersAndDepth()

	# Check if there is only one root
	def __isValid(self, predecessors) :
		valid = True
		hasRoot = False
		if predecessors != dict() :
			for key in predecessors.keys() :
				# Check if values of vertices identifiers are pos integers 
				if not isinstance(key, int) or key < 0 :
					valid = False
					print('Predecessors not valid : check if keys are positive or null integers')
					break
				# Check if there is no loop in the graph
				if key in predecessors[key] :
					valid = False
					print('Predecessors not valid : loop detected in vertex ' + str(key))
				if predecessors[key] == [] :
					hasRoot = True
		# Check if there is only one root
		hiddenRoots = self.__hiddenRootList(predecessors)
		if (len(hiddenRoots) > 0 and hasRoot) or len(hiddenRoots) > 1 :
				valid = False
				print('Predecessors not valid : more than 2 root vertices')
		return valid

	def __hasRoot(self, predecessors) :
		hasRoot = False
		for key in predecessors.keys() :
			if predecessors[key] == [] :
				hasRoot = True
		return hasRoot

	def __hiddenRootList(self, predecessors) :
		keyList = predecessors.keys()
		hiddenRoots = []
		for key in keyList :
			for predecessorId in predecessors[key] :
				if predecessorId not in keyList :
					hiddenRoots.append(predecessorId)
		return hiddenRoots

	def __addRoot(self, predecessors) :
		hiddenRootList = self.__hiddenRootList(predecessors)
		if len(hiddenRootList) == 1 :
			predecessors[hiddenRootList[0]] = []
		return predecessors

	def __initSuccessors(self) :
		successors = {}
		if len(self.m_predecessors) > 0 :
			for successorId in self.m_predecessors.keys() :
				if successorId not in successors.keys() :
					successors[successorId] = []
				for predecessorId in self.m_predecessors[successorId] :
					if predecessorId in successors :
						successors[predecessorId].append(successorId)
					else :
						successors[predecessorId] = [successorId]
		return successors

	def __initLayersAndDepth(self) :
		toExplore = []
		visited = []
		layers = dict()
		depth = 0
		if len(self.m_predecessors) != 0 :
			for vertexId in self.m_predecessors.keys() :
				if self.m_predecessors[vertexId] == [] :
					if self.m_successors[vertexId] != [] :
						toExplore.append(vertexId)
						layers[vertexId] = 0
						depth += 1
					else :
						layers[vertexId] = -1
			while len(toExplore) > 0 :
				predecessorId = toExplore.pop()
				if predecessorId not in visited :
					visited.append(predecessorId)
					if len(self.m_successors[predecessorId]) != 0 :
						for successorId in self.m_successors[predecessorId] :
							toExplore.insert(0, successorId)
							layers[successorId] = layers[predecessorId] + 1
							if layers[successorId] + 1 > depth :
								depth = layers[successorId] + 1
					else :
						for pred in self.m_predecessors[predecessorId] :
							if pred not in visited :
								toExplore.insert(0, pred)
								layers[pred] = layers[predecessorId] - 1
		self.m_depth = depth
		self.m_layers = layers

	def addSuccessor(self, predecessorId, successorId, edgePrioPredecessor) :
		status = -1
		if predecessorId < 0 or successorId < 0 :
			print('Vertex indexes must be positive or null')
		elif predecessorId not in self.m_successors.keys() :
			print(str(predecessorId) + str(' not defined'))
		elif successorId not in self.m_predecessors.keys() :
			# new leaf
			self.m_predecessors[successorId] = [predecessorId]
			self.m_successors[predecessorId].append(successorId)
			self.m_successors[successorId] = []
			self.__addLeafLayer(successorId)
			status = 1
		else :
			self.m_predecessors[successorId].append(predecessorId)
			if edgePrioPredecessor == 0 :
				self.m_successors[predecessorId].insert(0, successorId)
			else :
				self.m_successors[predecessorId].append(successorId)
			status = 1
		return status

	def removeSuccessor(self, predecessorId, successorId) :
		status = -1
		if predecessorId in self.m_successors.keys() :
			if successorId in self.m_successors[predecessorId] :
				self.m_successors[predecessorId].remove(successorId)
				self.m_predecessors[successorId].remove(predecessorId)
				status = 1
			else :
				print(str(successorId) + ' not registered as successor of ' + str(predecessorId))
		else :
			print(str(predecessorId) + ' is not registered as a predecessor')
		return status

	def swapSuccessors(self, predecessorIdA, successorIdA, predecessorIdB, successorIdB) :
		status = -1
		successors = self.m_successors
		predecessors = self.m_predecessors
		if (successorIdB in predecessors.keys()) and (successorIdA in predecessors.keys()) :
			if (predecessorIdA not in predecessors[successorIdB] and predecessorIdB not in predecessors[successorIdA]) or predecessorIdA == predecessorIdB:
				edgePrioPredecessorA = self.m_successors[predecessorIdA].index(successorIdA)
				edgePrioPredecessorB = self.m_successors[predecessorIdB].index(successorIdB)
			   	if self.removeSuccessor(predecessorIdA, successorIdA) != -1 and self.removeSuccessor(predecessorIdB, successorIdB) != -1 :
					self.addSuccessor(predecessorIdA, successorIdB, edgePrioPredecessorA)
					self.addSuccessor(predecessorIdB, successorIdA, edgePrioPredecessorB)
					status = 1
				else :
				   print('remove issue')
		else :
		 	print(str(successorIdB) + ' or ' + str(successorIdA) + ' is not a key of predecessors : ' + str(self.m_predecessors))
		return status

	def pivot(self, predecessorId, oldSuccessorId, newSuccessorId) :
		status = -1
		if self.m_layers[predecessorId] == 2 and self.m_successors[newSuccessorId] == []:
			if predecessorId in self.m_predecessors[oldSuccessorId] and oldSuccessorId in self.m_successors[predecessorId] :
				status = 1
				edgePrioOldSuccessor = self.m_successors[predecessorId].index(oldSuccessorId)
				self.m_predecessors[oldSuccessorId].remove(predecessorId)
				self.m_successors[predecessorId].remove(oldSuccessorId)
				if self.m_predecessors[oldSuccessorId] == [] :
					self.m_layers[oldSuccessorId] = -1
				self.m_layers[newSuccessorId] = 3
				self.m_predecessors[newSuccessorId].append(predecessorId)
				if edgePrioOldSuccessor == 0 :
					self.m_successors[predecessorId].insert(0, newSuccessorId)
				else :
					self.m_successors[predecessorId].append(newSuccessorId)
			else : 
				print("Predecessor : " + str(predecessorId) + " not in predecessors[oldSuccessorId] : " + str(self.m_predecessors[oldSuccessorId]) + " or oldSuccessor : " + str(oldSuccessorId) + ' not in successors[predecessorId] : ' + str(self.m_successors[predecessorId]))
		return status

	def addRoot(self, rootId) :
		if rootId < 0 :
			print('Vertex indexes must be positive or null')
		else :
			self.m_depth += 1
			if len(self.m_layers) > 0 :
				for vertexId in self.m_layers.keys() :
					self.m_layers[vertexId] += 1
			self.m_layers[rootId] = 0
			self.m_successors[rootId] = []

	def __addLeafLayer(self, successorId) :
		self.m_depth += 1
		self.m_layers[successorId] = self.m_depth - 1

	def __getVisualizationParams(self, natures, labelsOfVertices, key, strSeq) :
		color = "black"
		label = '<' + str(key)
		fontColor = "white"
		if natures[key] == 0 :
			color = "#E8D317"
		elif natures[key] == 1 :
			color = "#009463"
		elif natures[key] == 2 :
			color = "#45EF8F"
		else :
			label = '<' + str(key) + ' : ' + labelsOfVertices[key]
		if key == 0 :
			label += '<FONT POINT-SIZE="10"><BR /> Targetted Sequence : ' + strSeq + ' </FONT>>'
			fontColor = "black"
		else :
			label += '>'
		return (label, color, fontColor)

	def __getStrSeq(self, targetSeq) :
		strSeq = ''
		for elem in range(len(targetSeq)) :
			strSeq += targetSeq[elem]
			if elem != len(targetSeq) - 1 :
				strSeq += ", "
		return strSeq

	def __getLeaves(self) :
		leaves = []
		layers = self.m_layers
		for vertex in layers :
			if layers[vertex] == 3 or layers[vertex] == -1 :
				leaves.append(vertex)
		return leaves

	def __getLabelsOfVertices(self, leaves, eventNb) :
		labelsOfVertices = {}
		for leaf in leaves :
			for event in range(eventNb) :
				if leaves.index(leaf) % eventNb == event :
					labelsOfVertices[leaf] = str(unichr(event + ord('A')))
		return labelsOfVertices

	def __getEdgeColor(self, predecessorId, successorId) :
		edgeColor = "blue"
		if successorId == self.m_successors[predecessorId][0] :
			edgeColor = "red"
		return edgeColor

	def visualize(self, dataFolder, natures, eventNb, targetSeq) :
		if self.m_depth != 0 :
			dot = open(dataFolder + 'graph.dot', 'w')
			dot.write('graph G { \n')
			dot.write('\tedge [color="black"];\n\tnode [shape="circle", color="white", fontcolor="black", style="filled"];\n')
			strSeq = self.__getStrSeq(targetSeq)
			leaves = self.__getLeaves()
			labelsOfVertices = self.__getLabelsOfVertices(leaves, eventNb)
			# specify definition of vertices
			for key in self.m_successors.keys() :
				(label, color, fontColor) = self.__getVisualizationParams(natures, labelsOfVertices, key, strSeq)
				dot.write('\t' + str(key) + ' [label=' + label + ', shape="box", color="' + str(color) +'", fontcolor="' + fontColor + '"];\n')
			# specify edges
			for predecessorId in self.m_successors.keys() :
				for successorId in self.m_successors[predecessorId] :
					edgeColor = self.__getEdgeColor(predecessorId, successorId)
					dot.write('\t' + str(predecessorId) + ' -- ' + str(successorId) + ' [color=' + str(edgeColor) + '] ;\n')
			dot.write('}')
			dot.close()
			os.system('dot -Tjpg -o' + dataFolder + 'graph.jpg ' + dataFolder + 'graph.dot')
			os.system('display ' + dataFolder + 'graph.jpg')	
