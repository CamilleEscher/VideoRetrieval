import random
import copy
import itertools

def getPossibleSequences(fundamentalSeq) :
	return list(itertools.permutations(fundamentalSeq, len(fundamentalSeq)))

def getMaxPermutationNb(KEYFRAME_NB) :
	perm = 1
	for i in range(KEYFRAME_NB) :
		perm *= (KEYFRAME_NB - i)
	return perm

def getRemainingConcepts(startOfSequence, fundamentalSeq) :
	conceptsToContain = copy.copy(fundamentalSeq)
	for iEvent in startOfSequence :
		conceptsToContain.remove(iEvent)
	return conceptsToContain

def getRandomListOfConcept(conceptList, KEYFRAME_NB) :
	seq = []
	remainingKeyframe = KEYFRAME_NB
	while len(conceptList) <= KEYFRAME_NB :
		conceptList = conceptList + conceptList
	for i in range(KEYFRAME_NB) :
		conceptToAdd = conceptList[random.randrange(len(conceptList))]
		remainingKeyframe -= 1
		conceptList.remove(conceptToAdd)
		seq.append(conceptToAdd)	
	return seq

def simulate(CONCEPT_NB, KEYFRAME_NB, SAMPLE_NB, CLASS_NB, file, labelFileName, targets = None, extraClasses = 0) :
	if getMaxPermutationNb(KEYFRAME_NB) < CLASS_NB :
		print('Class number should be less than !keyframeNb')
		return
	writer = open(file, 'w')
	writerLabel = open(labelFileName, 'w')
	sequences = [[] for x in range(CLASS_NB + extraClasses)]
	# Building the sub-events sequences
	conceptList = []
	for i in range(0, CONCEPT_NB) :
		conceptList.append(i)
	if targets == None :
		sF = getRandomListOfConcept(conceptList, KEYFRAME_NB)
		possibleSequences = copy.copy(getPossibleSequences(sF))
		random.shuffle(possibleSequences)
		for i in range(CLASS_NB) :
			chosenSeq = possibleSequences[i]
			sequences[i] = chosenSeq
	else :
		for iTarget in range(len(targets)) :
			for c in targets[iTarget] :
				sequences[iTarget].append(ord(c) - ord('A'))
		if extraClasses > 0 :
			for classId in range(len(targets), len(targets) + extraClasses) :
				sequences[classId] = getRandomListOfConcept(conceptList, KEYFRAME_NB)
	# Write random values in training file and label them
	writeData(CLASS_NB, SAMPLE_NB, CONCEPT_NB, KEYFRAME_NB, sequences, writer, writerLabel, extraClasses)
	writer.close()
	writerLabel.close()
	letterSequences = getLetterSequences(sequences)
	return (tuple(letterSequences))

def getLetterSequences(sequences) :
	letterSequences = [[] for x in range(len(sequences))]
	for seq in sequences :
		for c in seq :
			letterSeq = [(chr(x + ord('A'))) for x in seq]
			letterSequences[sequences.index(seq)] = letterSeq
	return letterSequences

def writeData(CLASS_NB, SAMPLE_NB, CONCEPT_NB, KEYFRAME_NB, sequences, writer, writerLabel, extraClasses) :
	sPointer = -1
	totalClassNb = CLASS_NB + extraClasses
	for classIndex in range(totalClassNb) :
		BATCH_SIZE = int(SAMPLE_NB / float(totalClassNb))
		startIndex = classIndex * BATCH_SIZE
		stopIndex = (classIndex + 1) * (BATCH_SIZE)# - 1
		if classIndex == totalClassNb - 1 :
			stopIndex = SAMPLE_NB
		for sample in range(startIndex, stopIndex) :
			vidlist = []
			sPointer = -1
			for keyframe in range(0, KEYFRAME_NB) :
				conceptDetectedInFrameI = False
				for concept in range(0, CONCEPT_NB) :
					if (sPointer < len(sequences[classIndex]) - 1 and concept == sequences[classIndex][sPointer + 1]) and conceptDetectedInFrameI == False :
						vidlist.append(random.uniform(0.5, 1.0))
						sPointer = sPointer + 1
						conceptDetectedInFrameI = True
					else :
						vidlist.append(random.uniform(0.0, 0.5))
			writer.write(str(vidlist))
			writer.write('\n')
			writerLabel.write(str(classIndex + 1))
			writerLabel.write('\n')
