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

for i, x in enumerate(X):
	if x in Y:
		print str(i) + ": " + unconvert(x)