import random

def simulate(concepts, keyframes, videos, file, labelFileName, subsetSize, targets = None) :
	writer = open(file, 'w')
	writerLabel = open(labelFileName, 'w')
	# Building the sub-events sequences
	conceptList = []
	for i in range(0, concepts) :
		conceptList.append(i)
	ABCSequence = []
	BACSequence = []
	if targets == None :
		ABCSequence = random.sample(conceptList, 3)
		BACSequence = [ABCSequence[1], ABCSequence[0], ABCSequence[2]]
	else :
		for c in targets[0] :
			ABCSequence.append(ord(c) - ord('A'))
		for c in targets[1] :
			BACSequence.append(ord(c) - ord('A'))
	ABCPointer = -1
	BACPointer = -1
	subsetNb = 1

	for video in range(0, (subsetNb * videos / subsetSize)) :
		vidlist = []
		ABCPointer = -1
		for keyframe in range(0, keyframes) :
			conceptDetectedInFrameI = False
			for concept in range(0, concepts) :
				if (ABCPointer < len(ABCSequence) - 1 and concept == ABCSequence[ABCPointer + 1]) and conceptDetectedInFrameI == False :
					vidlist.append(random.uniform(0.5, 1.0))
					ABCPointer = ABCPointer + 1
					conceptDetectedInFrameI = True
				else :
					vidlist.append(random.uniform(0.0, 0.5))
		writer.write(str(vidlist))
		writer.write('\n')
		writerLabel.write('1')
		writerLabel.write('\n')
	
	for video in range((subsetNb * videos / subsetSize), (subsetNb + 1) * videos / subsetSize) :
		vidlist = []
		BACPointer = -1
		for keyframe in range(0, keyframes) :
			conceptDetectedInFrameI = False
			for concept in range(0, concepts) :
				if (BACPointer < len(BACSequence) - 1 and concept == BACSequence[BACPointer + 1]) and conceptDetectedInFrameI == False:
					vidlist.append(random.uniform(0.5, 1.0))
					BACPointer = BACPointer + 1
					conceptDetectedInFrameI = True
				else :
					vidlist.append(random.uniform(0.0, 0.5))
		writer.write(str(vidlist))
		writer.write('\n')
		writerLabel.write('2')
		writerLabel.write('\n')

# Executed when the test file is written (in that case, subsetSize = 3)
	subsetNb += 1
	if subsetNb < subsetSize :
		for video in range(subsetNb * videos / subsetSize, videos) :
			vidlist = []
			for keyframe in range(0, keyframes) :
				for concept in range(0, concepts) :
					vidlist.append(random.random())
			writer.write(str(vidlist))#			writer.write('\n')
			writer.write('\n')
			writerLabel.write('3')
			writerLabel.write('\n')

	writer.close()
	writerLabel.close()
	return ([chr(x + ord('A')) for x in ABCSequence], [chr(x + ord('A')) for x in BACSequence])
