import numpy as np
import neurolab as nl
import csv, sys
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
			raise ValueError("Illegal character: " + string[i] + " (" + str(ord(string[i])) + ")")
 
		num /= 55.
 
		final.append(num)
	while len(final) < 20:
		final.append(0)
	#final.append(len(string))
	return np.array(final)
 
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
			raise ValueError("Number out of bounds: " + str(num) + " (" + num + ")\nIn list: " + str(list))
 
		if num != 0:
			final += chr(num)
	return final
 
import time
then = time.time()
def timeit (message):
	global now, then
	now = time.time()
	print str(message) + " took " + str(now - then) + "s\n"
	then = now
 
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
timeit("Tests")

examples = 0
with open('../data/misspellings.csv', 'rbU') as f:
	examples = len(f.readlines())

from math import log, ceil
binlength = int(ceil(log(examples, 2)))

def makeTarget(index):
	return [int(x) for x in bin(index)[2:].zfill(binlength)]

def breakTarget(list):
	return int(''.join([str(int(round(x))) if x > 0 else '0' for x in list]), 2)

input = []
target = []
words = []
used = {} #for optimization
with open('../data/misspellings.csv', 'rbU') as f:
	reader = csv.reader(f)
	i = -1
	for row in reader:
		if used.has_key(row[1]):
			input.append(convert(row[0]))
			target.append(makeTarget(words.index(row[1])))
		else:
			i += 1
			input.append(convert(row[0]))
			target.append(makeTarget(i))
			words.insert(i, row[1])
			used[row[1]] = True
input = np.array(input)
target = np.array(target)
#target /= len(target)

timeit("Loading the data")


inputLayerSize = 20
inputLayerBounds = [0, 55]
outputLayerSize = binlength
hiddenLayerSize = int(float(inputLayerSize) * (2./3.)) + outputLayerSize
net = nl.net.newff([inputLayerBounds] * inputLayerSize, [hiddenLayerSize, hiddenLayerSize, outputLayerSize])
#net = nl.net.newff(shape, [20, 20, 20, 1])
#net.trainf =
# Train process
#error = net.train(input, target, epochs=50, show=1)
for i in xrange(500):
	rng_state = np.random.get_state()
	np.random.shuffle(target)
	np.random.set_state(rng_state)
	np.random.shuffle(input)
	error = net.train(input[:2000], target[:2000], epochs=1, show=None)
	print "Epoch: " + str(i + 1) + "; Error: " + str(error[0]) + ";"

timeit("Training")
 
# Test
def test(word):
#	print word + " -> " + words[int(round(net.sim([convert(word)])[0][0] * examples))]
#	print word + " -> " + words[int(round(net.sim([convert(word)])[0][0]))]
	print word + " -> " + words[breakTarget(net.sim([convert(word)])[0])]
 
test("acuracy")