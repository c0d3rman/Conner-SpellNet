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

		#num /= 29.

		final.append(num)
	while len(final) < 20:
		final.append(0)
	#final.append(len(string))
	return final

def unconvert(list):
	if len(list) > 20:
		raise ValueError("List too long (" + str(len(list)) + "): " + str(list))

	final = ""
	for num in list:
		#num *= 29.

		num = int(num)
		if 1 <= num <= 26:
			num += 96
		elif num == 27:
			num = 32
		elif num == 28:
			num = 39
		elif num == 29:
			num = 45
		elif num == 0:
			pass
		else:
			raise ValueError("Number out of bounds: " + str(num) + "\nIn list: " + str(list))

		if num != 0:
			final += chr(num)
	return final

import csv
X = []
Y = []
with open('misspellings.csv', 'rbU') as f:
	reader = csv.reader(f)
	for row in reader:
		X.append(convert(row[0]))
		Y.append(convert(row[1]))

from sklearn import cross_validation
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)

print "Training:   " + str(len(X_train)) + " x " + str(len(X_train[0]))
print "Validation: " + str(len(X_test)) + " x " + str(len(X_test[0]))

#timeit("Preparing the data")

'''
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

timeit("Standardizing the data")
'''

from sklearn.ensemble import ExtraTreesRegressor
#from sklearn.neighbors import KNeighborsRegressor

clf = ExtraTreesRegressor(n_estimators=2)
#clf = KNeighborsRegressor()

clf.fit(X_train, Y_train)

timeit("Training")

#print "Validation score: " + str(clf.score(X_test, Y_test))

#timeit("Validation")

score = 0.
for i, item in enumerate(X_test):
	if unconvert(clf.predict(item)[0]) == unconvert(Y_test[i]):
		score += 1
score /= len(X_test)
print "Manual validation score: " + str(score)

timeit("Manual validation")

import random
for word in random.sample(X, 10):
	print unconvert(word) + " (" + unconvert(Y[X.index(word)]) + ") -> " + unconvert(clf.predict(word)[0])
	#print unconvert(word) + " -> " + str(clf.predict(word))

def test (word):
	print word + " -> " + str(unconvert(clf.predict(convert(word))[0]))

#testwords = ["intillegent", "assurre", "onderstood", "spott", "lissten"]
#for word in testwords:
#	test(word)