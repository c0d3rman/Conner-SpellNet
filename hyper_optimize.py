import csv, sys
import numpy as np
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
from pybrain.optimization import CMAES
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance

def convert(string):
	final = []
	for i in xrange(len(string)):
		if i >= 20:
			return final

		num = ord(string[i])
		if 97 <= num <= 122:
			num -= 96
		elif 65 <= num <= 90:
			num -= 38
		elif num == 32:
			num = 53
		elif num == 39:
			num = 54
		elif num == 45:
			num = 55
		else:
			raise ValueError("Illegal character: " + string[i])

		num /= 55.

		final.append(np.float64(num))
	while len(final) < 20:
		final.append(0)
	#final.append(len(string))
	return final

def unconvert(list):
	if len(list) > 20:
		raise ValueError("List too long (" + str(len(list)) + "): " + str(list))

	final = ""
	for num in list:
		num *= 55.

		num = int(round(num))
		if 1 <= num <= 26:
			num += 96
		elif 27 <= num <= 52:
			num += 38
		elif num == 53:
			num = 32
		elif num == 54:
			num = 39
		elif num == 55:
			num = 45
		elif num <= 0 or num > 55:
			num = 0
		else:
			raise ValueError("Number out of bounds: " + str(num) + "\nIn list: " + str(list))

		if num != 0:
			final += chr(num)
	return final

def tests():
	if "conner" == unconvert(convert("conner")):
		print "Passed the plain text test."
	else: 
		sys.exit("Error! Convert function didn't pass the plain text test!")

	if "con-ner" == unconvert(convert("con-ner")):
		print "Passed the dash test."
	else:
		sys.exit("Error! Convert function didn't pass the dash test!")

	if "con ner" == unconvert(convert("con ner")):
		print "Passed the space test."
	else: 
		sys.exit("Error! Convert function didn't pass the space test!")

	if "CONNER" == unconvert(convert("CONNER")):
		print "Passed the capital test."
	else: 
		sys.exit("Error! Convert function didn't pass the capital test!")

	if "conner's" == unconvert(convert("conner's")):
		print "Passed the apostrophe test."
	else: 
		sys.exit("Error! Convert function didn't pass apostrophe test!")

	if 20 == len(convert("conner")):
		print "Passed the length test. (Convert outputs are 20 characters long.)"
	else:
		sys.exit("Error! Convert function isn't returning number that are 20 characters long!")

	print "Convert is returning:",type(convert("conner")).__name__

	print convert("Conner")
tests()

netNum = 0
def makeNet(learning_rate):
	ds = SupervisedDataSet(20, 20)
	with open('data/misspellings.csv', 'rbU') as f:
		reader = csv.reader(f)
		for row in reader:
			ds.addSample(convert(row[0]),convert(row[1]))

	testds, trainds = ds.splitWithProportion(0.2)

	net = buildNetwork(20, 20, 20)
	trainer = BackpropTrainer(net, dataset=trainds, learningrate=learning_rate)
	trainer.train()
	#trainer.trainEpochs(5)

	score = 0
	for x, y in testds:
		predict = unconvert(net.activate(x))
		score += damerau_levenshtein_distance(predict,unconvert(y))

	global lastNet
	lastNet = net

	global netNum
	netNum += 1

	if score == None:
		score = float("inf")
	print "Network " + str(netNum) + " done with score " + str(score)
	
	return score

x0 = [0.01]
optimizer = CMAES(makeNet, x0, minimize=True, maxEvaluations=10)
print optimizer.learn()