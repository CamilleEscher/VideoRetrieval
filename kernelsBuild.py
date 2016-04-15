from simulate import simulate
import numpy as np
from math import *
from Graph import Graph

dataFolder = './gen_data/'
trainFile = 'train.txt'
trainLabels = 'trainLabels.txt'
testFile = 'test.txt'
testLabels = 'testLabels.txt'

eventNb = 5
keyframeNb = 3
sampleNb = 100

simulate(eventNb, keyframeNb, sampleNb, dataFolder + 'train.txt', dataFolder + 'trainLabels.txt', 2)
simulate(eventNb, keyframeNb, sampleNb, dataFolder + 'test.txt', dataFolder + 'testLabels.txt', 3)

try :
	# Build kernels
	kernels = []
	data = np.zeros((eventNb * keyframeNb, sampleNb))
	lineNb = -1
	with open(dataFolder + trainFile, 'r') as fTrain :
		for line in fTrain :
			lineNb += 1
			line = line.replace('[', '')
			line = line.replace(']', '')
			line = line.replace('\n', '')
			keyframeList = list(line.split(', '))
			for elem in keyframeList :
				data[keyframeList.index(elem), lineNb] = elem
	kernel = np.ones((sampleNb, sampleNb))
	for elem in range(0, eventNb * keyframeNb) :
		dataSubEventI = data[elem, :]
		kernel = np.ones((sampleNb, sampleNb))
		for i in range(0, sampleNb) :
			for j in range(0, sampleNb) :
				kernel[i, j] -= abs(dataSubEventI[i] - dataSubEventI[j])
		kernels.append(np.copy(kernel))
		print("kernels :")
		print(kernels)
	g = Graph(eventNb * keyframeNb, kernels)
	g.visualize(dataFolder)

except IOError:
	print('file not found')
