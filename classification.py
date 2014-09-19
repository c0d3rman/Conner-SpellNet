import time
now = time.time()

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

def unconvert(list):
	if len(list) > 20:
		raise ValueError("List too long (" + str(len(list)) + "): " + str(list))

	final = ""
	for num in list:
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

		num *= 29.
		if num != 0:
			final += chr(num)
	return final

import csv
X = []
Y = []
words = []
used = {} #for optimization
import numpy
with open('data/misspellings.csv', 'rbU') as f:
	reader = csv.reader(f)
	i = -1
	for row in reader:
		X.append(numpy.array(convert(row[0])))
		if used.has_key(row[1]):
			Y.append(words.index(row[1]))
		else:
			i += 1
			Y.append(i)
			words.insert(i, row[1])
			used[row[1]] = True

X = numpy.array(X)
Y = numpy.array(Y)

from sklearn import cross_validation
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)

print "Training:   " + str(len(X_train)) + " x " + str(len(X_train[0]))
print "Validation: " + str(len(X_test)) + " x " + str(len(X_test[0]))

now2 = time.time()
print "Preparing the data took " + str(now2 - now) + "s\n"

#from sklearn.naive_bayes import MultinomialNB
#from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
#clf = MultinomialNB()
#clf = SGDClassifier(loss="hinge", penalty="l2")
clf = KNeighborsClassifier(n_neighbors=1,p=1,leaf_size=1,metric='hamming')

clf.fit(X_train, Y_train)

now3 = time.time()
print "Training took " + str(now3 - now2) + "s\n"

print "Validation score: " + str(clf.score(X_test, Y_test))

now4 = time.time()
print "Validation took " + str(now4 - now3) + "s\n"

'''
score = 0.
for i, item in enumerate(X_test):
	if words[clf.predict(item)] == words[Y_test[i]]:
		score += 1
score /= len(X_test)
print "Manual validation score: " + str(score)
'''

testwords = ["intillegent", "assurre", "onderstood", "spott", "lissten"]

def test (word):
	print word + " -> " + words[clf.predict(convert(word))]

for word in testwords:
	test(word)

#print clf.predict_proba(X)