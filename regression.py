import time
then = time.time()
def timeit (message):
	global now, then
	now = time.time()
	print str(message) + " took " + str(now - then) + "s\n"
	then = now

import sys
sys.setcheckinterval(1000)

def convert(string):
	final = []
	for i in xrange(len(string)):
		if i >= 20:
			return final

		num = ord(string[i])
		if 97 <= num <= 122:
			num -= 96
		elif num == 32:
			num = 27
		elif num == 39:
			num = 28
		elif num == 45:
			num = 29
		else:
			raise ValueError("Illegal character: " + string[i])

		num /= 29.
		#num *= 500

		final.append(num)
	while len(final) < 20:
		final.append(0)
	#final.append(len(string))
	return final

def unconvert(num):
	num = int(num)
	if 1 <= num <= 26:
		num += 96
	elif num == 27:
		num = 32
	elif num == 28:
		num = 39
	elif num == 29:
		num = 45
	elif num != 0:
		raise ValueError("Number out of bounds: " + str(num))

	return chr(num)

import csv
X = []
Ys = []
for i in convert(""):
	Ys.append([])

with open('misspellings.csv', 'rbU') as f:
	reader = csv.reader(f)
	for row in reader:
		X.append(convert(row[0]))
		for i, Y in enumerate(Ys):
			Y.append(convert(row[1])[i])

timeit("Preparing the data")

'''
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

timeit("Standardizing the data")
'''

from sklearn import linear_model
#from sklearn import svm
clfs = []
for Y in Ys:
	clf = linear_model.SGDRegressor()
	#clf = svm.SVR(kernel='linear')

	clf.fit(X, Y)

	clfs.append(clf)

timeit("Training")

testwords = ["intillegent", "assurre", "onderstood", "spott", "lissten"]

def test (word):
	gen = ""
	converted = convert(word)
	for i, clf in enumerate(clfs):
		gen += str(clf.predict(converted)) + "\n"
	print word + " -> " + gen

for word in testwords:
	test(word)