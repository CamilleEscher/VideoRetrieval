import random

def simulate(concepts, keyframes, videos, file, labelFileName, subsetSize) :
	writer = open(file, 'w')
	writerLabel = open(labelFileName, 'w')
	conceptList = []
	for i in range(0, concepts) :
		conceptList.append(i)
	ABCSequence = random.sample(conceptList, 3)
	BACSequence = [ABCSequence[1], ABCSequence[0], ABCSequence[2]]
	ABCPointer = -1
	BACPointer = -1
	subsetNb = 1

	for video in range(0, (subsetNb * videos / subsetSize)) :
		vidlist = []
		ABCPointer = -1
		for keyframe in range(0, keyframes) :
			for concept in range(0, concepts) :
				if (ABCPointer < len(ABCSequence) - 1 and concept == ABCSequence[ABCPointer + 1]) :
					vidlist.append(random.uniform(0.5, 1.0))
					ABCPointer = ABCPointer + 1
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
			for concept in range(0, concepts) :
				if (BACPointer < len(BACSequence) - 1 and concept == BACSequence[BACPointer + 1]):
					vidlist.append(random.uniform(0.5, 1.0))
				else :
					vidlist.append(random.uniform(0.0, 0.5))
					BACPointer = BACPointer + 1
		writer.write(str(vidlist))
		writer.write('\n')
		writerLabel.write('2')
		writerLabel.write('\n')

# Assignment 2, executed when the test file is written (in that case, subsetSize = 3)
	subsetNb += 1
	if subsetNb < subsetSize :
		for video in range(subsetNb * videos / subsetSize, videos) :
			vidlist = []
			for keyframe in range(0, keyframes) :
				for concept in range(0, concepts) :
					vidlist.append(random.random())
			writer.write(str(vidlist))
			writer.write('\n')
			writerLabel.write('3')
			writerLabel.write('\n')

	writer.close()
	writerLabel.close()
