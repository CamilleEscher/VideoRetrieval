import random
import copy
import math

'''
def whileOp(successorA, successorB, posValues, negValues) :	
	posVector = [x + y for x, y in zip(posValues[successorA], posValues[successorB])]
	negVector = [x + y for x, y in zip(negValues[successorA], negValues[successorB])]
	return (posVector, negVector)
'''
def whileOp(successors, posValues, negValues) :
	posVector = []
	negVector = []
	for successorId in successors :
		if successors[0] == successorId :
			posVector = posValues[successorId]
			negVector = negValues[successorId]
		else :
			posVector = [x + y for x, y in zip(posVector, posValues[successorId])]
			negVector = [x + y for x, y in zip(negVector, negValues[successorId])]
	return (posVector, negVector)

def whileOpTest(successors, values) :	
	vector = []
	for successorId in successors :
		if successors[0] == successorId :
			vector = values[successorId]
		else :
			vector = [x + y for x, y in zip(vector, values[successorId])]
#	vector = [x + y for x, y in zip(values[successorA], values[successorB])]
	return vector

def whileNotOp(successorA, successorB, posValues, negValues) :
	posVectorB = [0 for x in range(len(posValues[successorB]))]
	negVectorB = [0 for x in range(len(negValues[successorB]))]
	for i in range(len(posValues[successorB])) :
		posVectorB[i] = 1 - posValues[successorB][i]
	for i in range(len(negValues[successorB])) :
		negVectorB[i] = 1 - negValues[successorB][i]
	posVector = [x + y for x, y in zip(posValues[successorA], posVectorB)]
	negVector = [x + y for x, y in zip(negValues[successorA], negVectorB)]
	return (posVector, negVector)

def whileNotOpTest(successorA, successorB, values) :
	vectorB = [0 for x in range(len(values[successorB]))]
	for i in range(len(values[successorB])) :
		vectorB[i] = 1 - values[successorB][i]
	vector = [x + y for x, y in zip(values[successorA], vectorB)]
	return vector

def beforeOp(successorA, successorB, posValues, negValues) :
	posVector = [x * y for x, y in zip(posValues[successorA], posValues[successorB])]
	negVector = [x * y for x, y in zip(negValues[successorA], negValues[successorB])]
	return (posVector, negVector)

def beforeOpTest(successorA, successorB, values) :
	vector = [x * y for x, y in zip(values[successorA], values[successorB])]
	return vector

def swapBranches(graph, args) :
	if len(args) == 4 :
		predecessorId1 = args[0]
		successorId1 = args[1]
		predecessorId2 = args[2]
		successorId2 = args[3]
		if successorId1 in graph.m_successors[predecessorId1] and successorId2 in graph.m_successors[predecessorId2] :
			graph.swapSuccessors(predecessorId1, successorId1, predecessorId2, successorId2)
		else :
			print('wrong operation : ' + str(successorId1) + ' is not a successor of ' + str(predecessorId1) + ' or ' + str(successorId2) + ' is not a successor of ' + str(predecessorId2))
	else :
		print('Number of arguments invalid : ' + str(args) + '4 args are required for swap op')

def pivotBranches(graph, args) :
	predecessorId = args[0]
	successorId1 = args[1]
	successorId2 = args[2]
	if len(args) == 3 :
		if successorId1 in graph.m_successors[predecessorId] and graph.m_successors[successorId2] == []:
			graph.pivot(predecessorId, successorId1, successorId2)
		else :
			print('wrong operation : ' + str(successorId1) + ' is not a successor of ' + str(predecessorId) + ' or ' + str(successorId2) + ' has predecessors or successors ')

def nextMove(graph, posVal, negVal, ratio, natures, vertexNatures, command, commands, args) :
	vertexId = args[0]
	if vertexId in graph.m_layers.keys() :
		layer = graph.m_layers[vertexId]
		if layer in range(3) :
			successors = graph.m_successors[vertexId]
			nature = natures[vertexId]
			if command == commands['swap'] and (nature == vertexNatures['before'] or nature == vertexNatures['while'] or nature == vertexNatures['whileNot']) :
				swapBranches(graph, args)
				(posVal, negVal) = bottomUp(posVal, negVal, graph.m_successors, graph.m_layers, natures, vertexNatures)
			elif command == commands['pivot'] and nature == vertexNatures['whileNot'] :
				pivotBranches(graph, args)
				(posVal, negVal) = bottomUp(posVal, negVal, graph.m_successors, graph.m_layers, natures, vertexNatures)
			else :
				print('operation : not allowed for this kind of node : ' + str(vertexId) + ' cannot handle : ' + str(command))	
	return (posVal, negVal, evaluate(posVal[0], negVal[0]))

def getMagnitudeRootVal(val) :
	return (math.sqrt(sum(i**2 for i in val)) / float(len(val)))

def getRatio(pos, neg) :
	return ((float(pos) / float(neg)) * (float(pos)))

def evaluate(rootPosValues, rootNegValues) :
	magPosRootVal = getMagnitudeRootVal(rootPosValues)
	magNegRootVal = getMagnitudeRootVal(rootNegValues)
	return getRatio(magPosRootVal, magNegRootVal)

def __getSwapArgs(vertexId, listOfLeaves, successors, predecessors) :
	nonAlreadySuccessors = getNewPotentialSuccessors(vertexId, listOfLeaves, successors)
	rdm = random.randrange(2)
	rdm2 = random.randrange(len(nonAlreadySuccessors))
	oldSuccessor = successors[vertexId][rdm]
	newSucessor = nonAlreadySuccessors[rdm2]
	rdm3 = random.randrange(len(predecessors[newSucessor]))
	siblingPredecessor = predecessors[newSucessor][rdm3]
	return (vertexId, oldSuccessor, siblingPredecessor, newSucessor)

def  __getPivotArgs(vertexId, listOfLeaves, successors) :
	nonAlreadySuccessors = getNewPotentialSuccessors(vertexId, listOfLeaves, successors)
	rdm = random.randrange(2)
	rdm2 = random.randrange(len(nonAlreadySuccessors))
	return (vertexId, successors[vertexId][rdm], nonAlreadySuccessors[rdm2])

def __reverseSwapArgs(args) :
	return (args[0], args[3], args[2], args[1])

def __reversePivotArgs(args) :
	return (args[0], args[2], args[1])

def __getListOfLeaves(vertexId, predecessors, successors, natures, vertexNatures) :
	beforePred = predecessors[vertexId][0]
	edgePrio = 1
# CHAN
	if successors[beforePred][0] == vertexId :
		edgePrio = 0
	return getPotentialSuccessors(beforePred, edgePrio, natures, vertexNatures, successors)

def inferenceProcess(graph, posVal, negVal, ratio, natures, vertexNatures, commands, argsCards) :
	layer = 2
	vertexId = chooseRandomVertex(graph.m_successors, graph.m_layers, layer, -1)
	listOfLeaves = __getListOfLeaves(vertexId, graph.m_predecessors, graph.m_successors, natures, vertexNatures)
	if vertexId > -1 :
		successors = graph.m_successors[vertexId]
		nature = natures[vertexId]
		# {
		# Not used for now : just need to apply moves on successors of whileNot nodes : remains for discussion
		if nature == vertexNatures['before'] or nature == vertexNatures['while'] :
			command = commands['swap']
			args = __getSwapArgs(vertexId, listOfLeaves, graph.m_successors, graph.m_predecessors)
			(posValues, negValues, newRatio) = nextMove(graph, copy.copy(posVal), copy.copy(negVal), ratio, natures, vertexNatures, command, commands, args)
			(posVal, negVal, ratio, keptOp) = __updateResults(newRatio, ratio, posValues, negValues, posVal, negVal)
			if not keptOp :
				args = __reverseSwapArgs(args)
				(posValues, negValues, newRatio) = nextMove(graph, posValues, negValues, newRatio, natures, vertexNatures, command, commands, args)
		# }
		elif nature == vertexNatures['whileNot'] :
			chainOfCommand = [commands['swap'], commands['pivot']]
			for command in list(chainOfCommand) :
				if command == commands['swap'] :
					args = (vertexId, graph.m_successors[vertexId][0], vertexId, graph.m_successors[vertexId][1])
				elif command == commands['pivot'] :
					args = __getPivotArgs(vertexId, listOfLeaves, graph.m_successors)
				(posValues, negValues, newRatio) = nextMove(graph, copy.copy(posVal), copy.copy(negVal), ratio, natures, vertexNatures, command, commands, args)
				(posVal, negVal, ratio, keptOp) = __updateResults(newRatio, ratio, posValues, negValues, posVal, negVal)
				if not keptOp :
					if command == commands['swap'] :
						args = __reverseSwapArgs(args)
					else :
						args = __reversePivotArgs(args)
					(posValues, negValues, newRatio) = nextMove(graph, posValues, negValues, newRatio, natures, vertexNatures, command, commands, args)
		else :
			print('Nature ' + str(nature) + ' is not allowed in the inference process')
	return (posVal, negVal, ratio)

def __updateResults(newRatio, ratio, posValues, negValues, posVal, negVal) :
	keptOp = False
	if ratio < newRatio :
		negVal = negValues
		posVal = posValues
		ratio = newRatio
		keptOp = True
		
	return (posVal, negVal, ratio, keptOp)

def getNewPotentialSuccessors(vertexId, listOfLeaves, successors) :
	for successor in successors[vertexId] :
		if successor in listOfLeaves :
			listOfLeaves.remove(successor)
	return listOfLeaves

def getPotentialSuccessors(beforePredId, edgePrio, natures, vertexNatures, successors) :
	leaves = getVerticesPerNature(natures, vertexNatures['leaf'])
	unlinkedLeaves = getVerticesPerNature(natures, vertexNatures['unlinkedLeaf'])
	totLeaves = leaves + unlinkedLeaves
	beforeList = getVerticesPerNature(natures, vertexNatures['before'])
	leavesNb = len(totLeaves)
	beforeNb = len(beforeList)
	keyframeNb = beforeNb + 1
	batchSize = leavesNb / keyframeNb
	leavesPerBatch = [[] for x in range(keyframeNb)]
	leavesPerBatchPt = 0
	for i in totLeaves :
		if (i - totLeaves[0]) % batchSize == 0 and i > totLeaves[0] :
			leavesPerBatchPt += 1
		leavesPerBatch[leavesPerBatchPt].append(i)
	batchIndex = beforeList.index(beforePredId) + edgePrio
	batchOfInterest = leavesPerBatch[batchIndex]
	return batchOfInterest
	
	
def getVerticesPerNature(natures, nature) :
	vertices = []
	for i in natures.keys() :
		if natures[i] == nature :
			vertices.append(i)
	return vertices

def chooseRandomVertex(successors, layers, layer, vertexId) :
	layersCp = copy.copy(layers)
	siblingId = -1
	if len(layersCp) > 0 :
		verticesInLayer = []
		for vertex in layersCp.keys() :
			if layersCp[vertex] == layer :
				verticesInLayer.append(vertex)
		if len(verticesInLayer) > 0 :
			siblingIndex = random.randrange(len(verticesInLayer))
			siblingId = verticesInLayer[siblingIndex]
		else :
			print('Layer ' + str(layer) + 'contains no vertex')
	else :
		print('layers is empty')
	return siblingId

def bottomUp(posValues, negValues, successors, layers, natures, vertexNatures) :
	layer = vertexNatures['leaf'] - 1
	while(layer >= 0) :
		verticesInLayer = []
		for vertex in layers :
			if layers[vertex] == layer :
				verticesInLayer.append(vertex)
		for vertex in verticesInLayer :
			successorsOf = successors[vertex]
			nat = natures[vertex]
			if nat == vertexNatures['while'] :
				(posValues[vertex], negValues[vertex]) = whileOp(successorsOf, posValues, negValues)
			elif len(successorsOf) == 2 :
				if nat == vertexNatures['before'] :
					(posValues[vertex], negValues[vertex]) = beforeOp(successorsOf[0], successorsOf[1], posValues, negValues)
				elif nat == vertexNatures['whileNot'] :
					(posValues[vertex], negValues[vertex]) = whileNotOp(successorsOf[0], successorsOf[1], posValues, negValues)
				else :
					print(str(nat) + ' is not used in bottom-up inference')
					break
			else :
				print(str(vertex) + ' has ' + str(len(successorsOf)) + ' successors : should have 2 successors')
				break
		layer -= 1
	return (posValues, negValues)

def bottomUpOnTests(values, successors, layers, natures, vertexNatures) :
	layer = vertexNatures['leaf'] - 1
	while(layer >= 0) :
		verticesInLayer = []
		for vertex in layers :
			if layers[vertex] == layer :
				verticesInLayer.append(vertex)
		for vertex in verticesInLayer :
			successorsOf = successors[vertex]
			nat = natures[vertex]
			if nat == vertexNatures['while'] :
				values[vertex] = whileOpTest(successorsOf, values)
			elif len(successorsOf) == 2 :
				if nat == vertexNatures['before'] :
					values[vertex] = beforeOpTest(successorsOf[0], successorsOf[1], values)
				elif nat == vertexNatures['whileNot'] :
					values[vertex] = whileNotOpTest(successorsOf[0], successorsOf[1], values)
				else :
					print(str(natures[vertex]) + ' is not used in bottom-up inference')
					break
			else :
				print(str(vertex) + ' has ' + str(len(successorsOf)) + ' successors : should have 2 successors')
				break
		layer -= 1
	return values
